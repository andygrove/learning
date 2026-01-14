"""
Query interface for the code RAG system.

Supports multiple LLM backends:
- Claude API (requires ANTHROPIC_API_KEY)
- Local transformers models
- Context-only mode (returns retrieved code without LLM)
"""

import os
from typing import Protocol, Iterator

from .indexer import CodeIndex


class LLMBackend(Protocol):
    """Protocol for LLM backends."""

    def generate(self, prompt: str, context: str) -> str:
        """Generate a response given a prompt and context."""
        ...


class ContextOnlyBackend:
    """Returns just the retrieved context without LLM generation."""

    def generate(self, prompt: str, context: str) -> str:
        return f"Query: {prompt}\n\n{'='*50}\nRetrieved Context:\n{'='*50}\n\n{context}"


class ClaudeBackend:
    """Claude API backend."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Install anthropic: pip install anthropic")

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, context: str) -> str:
        system_prompt = """You are an expert on the Apache DataFusion, DataFusion Comet, and Apache Spark codebases.
You help developers understand the code, find relevant implementations, and answer questions about architecture and design.

When answering questions:
1. Reference specific files and line numbers when relevant
2. Explain the code in context of the broader system
3. Point out related code or concepts the user might want to explore
4. Be precise and technical

You will be provided with relevant code snippets from these codebases as context."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Context from the codebase:\n\n{context}\n\n---\n\nQuestion: {prompt}",
                }
            ],
        )
        return message.content[0].text


class LocalModelBackend:
    """Local transformers model backend with quantization support."""

    # Model presets with their prompt templates
    MODEL_PRESETS = {
        "deepseek-coder-1.3b": {
            "name": "deepseek-ai/deepseek-coder-1.3b-instruct",
            "quantize": False,  # Small enough to run in fp16
            "template": "deepseek",
        },
        "deepseek-coder-6.7b": {
            "name": "deepseek-ai/deepseek-coder-6.7b-instruct",
            "quantize": True,  # Needs 4-bit quantization for 10GB VRAM
            "template": "deepseek",
        },
        "codellama-7b": {
            "name": "codellama/CodeLlama-7b-Instruct-hf",
            "quantize": True,
            "template": "llama",
        },
        "qwen-coder-1.5b": {
            "name": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
            "quantize": False,
            "template": "qwen",
        },
    }

    def __init__(self, model_name: str = "deepseek-coder-1.3b"):
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
            import torch
        except ImportError:
            raise ImportError("Install transformers: pip install transformers accelerate bitsandbytes")

        # Check if it's a preset or a full model name
        if model_name in self.MODEL_PRESETS:
            preset = self.MODEL_PRESETS[model_name]
            full_name = preset["name"]
            quantize = preset["quantize"]
            self.template = preset["template"]
        else:
            full_name = model_name
            quantize = False  # Default to no quantization for unknown models
            self.template = "generic"

        print(f"Loading local model: {full_name}")
        if quantize:
            print("  Using 4-bit quantization to fit in VRAM")

        self.tokenizer = AutoTokenizer.from_pretrained(full_name, trust_remote_code=True)

        # Set up quantization config if needed
        if quantize:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                full_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                full_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )

        self.model_name = model_name

        # Set pad token if not set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def _format_prompt(self, question: str, context: str) -> str:
        """Format prompt based on model template."""

        # Truncate context if too long (roughly 6k tokens worth)
        max_context = 8000
        if len(context) > max_context:
            context = context[:max_context] + "\n... [truncated]"

        system_msg = """You are an expert on the Apache DataFusion, DataFusion Comet, and Apache Spark codebases.
Answer questions based on the provided code context. Reference specific files and line numbers when relevant."""

        if self.template == "deepseek":
            return f"""You are an AI programming assistant.
{system_msg}

### Context:
{context}

### Question:
{question}

### Answer:
"""
        elif self.template == "llama":
            return f"""<s>[INST] <<SYS>>
{system_msg}
<</SYS>>

Context from the codebase:
{context}

Question: {question} [/INST]
"""
        elif self.template == "qwen":
            return f"""<|im_start|>system
{system_msg}<|im_end|>
<|im_start|>user
Context from the codebase:
{context}

Question: {question}<|im_end|>
<|im_start|>assistant
"""
        else:  # generic
            return f"""{system_msg}

Context:
{context}

Question: {question}

Answer:"""

    def generate(self, prompt: str, context: str) -> str:
        import torch

        full_prompt = self._format_prompt(prompt, context)
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                temperature=0.7,
                do_sample=True,
                top_p=0.95,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        # Decode only the new tokens
        response = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )
        return response.strip()


class CodeRAG:
    """Main RAG interface for querying the codebase."""

    def __init__(
        self,
        index: CodeIndex | None = None,
        backend: LLMBackend | None = None,
        persist_dir: str = "./chroma_db",
    ):
        self.index = index or CodeIndex(persist_dir=persist_dir)
        self.backend = backend or ContextOnlyBackend()

    def query(
        self,
        question: str,
        n_results: int = 5,
        repo_filter: str | None = None,
        show_context: bool = False,
    ) -> str:
        """
        Query the codebase.

        Args:
            question: Natural language question about the code
            n_results: Number of code chunks to retrieve
            repo_filter: Optional filter by repo name
            show_context: Whether to include retrieved context in output

        Returns:
            Generated answer (or just context in context-only mode)
        """
        # Retrieve relevant code
        results = self.index.search(
            query=question,
            n_results=n_results,
            repo_filter=repo_filter,
        )

        # Format context
        context_parts = []
        for r in results:
            meta = r["metadata"]
            context_parts.append(
                f"[{meta['repo']}] {meta['file_path']}:{meta['start_line']}-{meta['end_line']}"
                f" ({r['similarity']:.2f})\n{r['content']}"
            )
        context = "\n\n---\n\n".join(context_parts)

        # Generate response
        response = self.backend.generate(question, context)

        if show_context and not isinstance(self.backend, ContextOnlyBackend):
            return f"{response}\n\n{'='*50}\nRetrieved Context:\n{'='*50}\n\n{context}"

        return response

    def interactive(self):
        """Start an interactive query session."""
        print("Code RAG Interactive Session")
        print("Type 'quit' to exit, 'stats' for index stats")
        print("Prefix with @repo to filter by repository (e.g., @datafusion)")
        print("-" * 50)

        while True:
            try:
                query = input("\nQuestion: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not query:
                continue
            if query.lower() == 'quit':
                break
            if query.lower() == 'stats':
                stats = self.index.get_stats()
                print(f"\nTotal chunks: {stats['total_chunks']}")
                for repo, count in stats['by_repo'].items():
                    print(f"  {repo}: {count}")
                continue

            # Parse repo filter
            repo_filter = None
            if query.startswith('@'):
                parts = query.split(' ', 1)
                repo_filter = parts[0][1:]  # Remove @
                query = parts[1] if len(parts) > 1 else ""
                if not query:
                    print("Please provide a question after the repo filter")
                    continue

            # Query
            print("\nSearching...")
            response = self.query(query, repo_filter=repo_filter)
            print("\n" + response)


def create_rag(
    backend_type: str = "context",
    model_name: str | None = None,
    persist_dir: str = "./chroma_db",
) -> CodeRAG:
    """
    Factory function to create a CodeRAG instance.

    Args:
        backend_type: One of "context", "claude", "local"
        model_name: Model name for claude or local backends
        persist_dir: ChromaDB persistence directory
    """
    if backend_type == "context":
        backend = ContextOnlyBackend()
    elif backend_type == "claude":
        backend = ClaudeBackend(model=model_name or "claude-sonnet-4-20250514")
    elif backend_type == "local":
        backend = LocalModelBackend(model_name=model_name or "deepseek-coder-1.3b")
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")

    return CodeRAG(backend=backend, persist_dir=persist_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query the code index")
    parser.add_argument("--backend", choices=["context", "claude", "local"], default="context")
    parser.add_argument("--model", help="Model name for claude/local backends")
    parser.add_argument("--query", "-q", help="Single query (otherwise interactive mode)")
    args = parser.parse_args()

    rag = create_rag(backend_type=args.backend, model_name=args.model)

    if args.query:
        print(rag.query(args.query))
    else:
        rag.interactive()
