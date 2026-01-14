"""
Code indexing module using embeddings and ChromaDB.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
from tqdm import tqdm

from .chunker import CodeChunker, CodeChunk, iter_source_files


class CodeIndex:
    """Vector index for code search."""

    def __init__(
        self,
        persist_dir: str = "./chroma_db",
        model_name: str = "all-MiniLM-L6-v2",
        collection_name: str = "code",
    ):
        self.persist_dir = Path(persist_dir)
        self.model_name = model_name
        self.collection_name = collection_name

        # Initialize embedding model
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index_repository(
        self,
        repo_path: str,
        batch_size: int = 100,
        skip_existing: bool = True,
    ) -> int:
        """
        Index all source files in a repository.

        Returns the number of chunks indexed.
        """
        chunker = CodeChunker()
        repo_name = Path(repo_path).name

        # Collect all chunks first
        print(f"Scanning {repo_name}...")
        chunks: list[CodeChunk] = []

        for file_path, content in iter_source_files(repo_path):
            for chunk in chunker.chunk_file(file_path, content):
                chunks.append(chunk)

        print(f"Found {len(chunks)} chunks in {repo_name}")

        if skip_existing:
            # Filter out already indexed chunks
            existing_ids = set(self.collection.get()["ids"])
            chunks = [c for c in chunks if c.id not in existing_ids]
            print(f"Indexing {len(chunks)} new chunks (skipping existing)")

        if not chunks:
            return 0

        # Process in batches
        indexed = 0
        for i in tqdm(range(0, len(chunks), batch_size), desc="Indexing"):
            batch = chunks[i:i + batch_size]

            # Prepare batch data
            ids = [c.id for c in batch]
            documents = [c.to_document() for c in batch]
            metadatas = [
                {
                    "file_path": c.file_path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "chunk_type": c.chunk_type,
                    "name": c.name or "",
                    "repo": c.file_path.split("/")[0],
                }
                for c in batch
            ]

            # Generate embeddings
            embeddings = self.model.encode(documents, show_progress_bar=False)

            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
            )

            indexed += len(batch)

        return indexed

    def search(
        self,
        query: str,
        n_results: int = 10,
        repo_filter: str | None = None,
        chunk_type_filter: str | None = None,
    ) -> list[dict]:
        """
        Search for relevant code chunks.

        Args:
            query: Natural language query or code snippet
            n_results: Number of results to return
            repo_filter: Filter by repository name (e.g., "datafusion")
            chunk_type_filter: Filter by chunk type (e.g., "function")

        Returns:
            List of results with content, metadata, and similarity score
        """
        # Build where clause for filtering
        where = None
        if repo_filter or chunk_type_filter:
            conditions = []
            if repo_filter:
                conditions.append({"repo": repo_filter})
            if chunk_type_filter:
                conditions.append({"chunk_type": chunk_type_filter})

            if len(conditions) == 1:
                where = conditions[0]
            else:
                where = {"$and": conditions}

        # Embed query
        query_embedding = self.model.encode(query).tolist()

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        # Format results
        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "similarity": 1 - results["distances"][0][i],  # cosine distance to similarity
            })

        return formatted

    def get_stats(self) -> dict:
        """Get statistics about the index."""
        all_data = self.collection.get(include=["metadatas"])

        stats = {
            "total_chunks": len(all_data["ids"]),
            "by_repo": {},
            "by_type": {},
        }

        for meta in all_data["metadatas"]:
            repo = meta.get("repo", "unknown")
            chunk_type = meta.get("chunk_type", "unknown")

            stats["by_repo"][repo] = stats["by_repo"].get(repo, 0) + 1
            stats["by_type"][chunk_type] = stats["by_type"].get(chunk_type, 0) + 1

        return stats


def build_index(repos_dir: str = ".", persist_dir: str = "./chroma_db") -> CodeIndex:
    """
    Build or update the code index for all repositories.

    Args:
        repos_dir: Directory containing the repositories
        persist_dir: Directory to persist the ChromaDB index
    """
    index = CodeIndex(persist_dir=persist_dir)

    repos = ["datafusion", "datafusion-comet", "spark"]

    for repo in repos:
        repo_path = Path(repos_dir) / repo
        if repo_path.exists():
            print(f"\n{'='*50}")
            print(f"Indexing {repo}")
            print('='*50)
            count = index.index_repository(str(repo_path))
            print(f"Indexed {count} chunks from {repo}")
        else:
            print(f"Warning: {repo_path} not found, skipping")

    # Print stats
    stats = index.get_stats()
    print(f"\n{'='*50}")
    print("Index Statistics")
    print('='*50)
    print(f"Total chunks: {stats['total_chunks']}")
    print("\nBy repository:")
    for repo, count in sorted(stats['by_repo'].items()):
        print(f"  {repo}: {count}")
    print("\nBy chunk type:")
    for chunk_type, count in sorted(stats['by_type'].items()):
        print(f"  {chunk_type}: {count}")

    return index


if __name__ == "__main__":
    build_index()
