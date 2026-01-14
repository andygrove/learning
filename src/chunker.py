"""
Code chunking module for splitting source files into meaningful pieces.

Supports: Rust (.rs), Scala (.scala), Java (.java)
"""

import re
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator


@dataclass
class CodeChunk:
    """A chunk of code with metadata."""
    content: str
    file_path: str
    start_line: int
    end_line: int
    chunk_type: str  # 'function', 'class', 'impl', 'file', etc.
    name: str | None = None  # function/class name if applicable

    @property
    def id(self) -> str:
        """Unique identifier for this chunk."""
        return f"{self.file_path}:{self.start_line}-{self.end_line}"

    def to_document(self) -> str:
        """Format chunk for embedding with context."""
        header = f"// File: {self.file_path}\n"
        if self.name:
            header += f"// {self.chunk_type}: {self.name}\n"
        header += f"// Lines: {self.start_line}-{self.end_line}\n\n"
        return header + self.content


class CodeChunker:
    """Splits code files into semantic chunks."""

    def __init__(self, max_chunk_size: int = 2000, overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

        # Patterns for different languages
        self.patterns = {
            '.rs': {
                'function': re.compile(
                    r'^(\s*)(pub\s+)?(async\s+)?fn\s+(\w+)',
                    re.MULTILINE
                ),
                'impl': re.compile(
                    r'^(\s*)(pub\s+)?impl(<[^>]+>)?\s+(\w+)',
                    re.MULTILINE
                ),
                'struct': re.compile(
                    r'^(\s*)(pub\s+)?struct\s+(\w+)',
                    re.MULTILINE
                ),
                'enum': re.compile(
                    r'^(\s*)(pub\s+)?enum\s+(\w+)',
                    re.MULTILINE
                ),
                'trait': re.compile(
                    r'^(\s*)(pub\s+)?trait\s+(\w+)',
                    re.MULTILINE
                ),
            },
            '.scala': {
                'function': re.compile(
                    r'^(\s*)(override\s+)?(private|protected|public)?\s*def\s+(\w+)',
                    re.MULTILINE
                ),
                'class': re.compile(
                    r'^(\s*)(case\s+)?(class|object|trait)\s+(\w+)',
                    re.MULTILINE
                ),
            },
            '.java': {
                'function': re.compile(
                    r'^(\s*)(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\(',
                    re.MULTILINE
                ),
                'class': re.compile(
                    r'^(\s*)(public|private|protected)?\s*(abstract)?\s*(class|interface|enum)\s+(\w+)',
                    re.MULTILINE
                ),
            },
        }

    def get_language(self, file_path: str) -> str | None:
        """Determine language from file extension."""
        suffix = Path(file_path).suffix
        if suffix in self.patterns:
            return suffix
        return None

    def chunk_file(self, file_path: str, content: str) -> Iterator[CodeChunk]:
        """
        Split a file into chunks.

        Uses semantic chunking when possible (functions, classes),
        falls back to size-based chunking for large blocks.
        """
        lang = self.get_language(file_path)
        lines = content.split('\n')

        if not lang or len(content) < self.max_chunk_size:
            # Small file or unknown language: return as single chunk
            yield CodeChunk(
                content=content,
                file_path=file_path,
                start_line=1,
                end_line=len(lines),
                chunk_type='file',
            )
            return

        # Find all semantic boundaries
        boundaries = self._find_boundaries(content, lang)

        if not boundaries:
            # No semantic boundaries found, use size-based chunking
            yield from self._chunk_by_size(file_path, content, lines)
            return

        # Create chunks from boundaries
        yield from self._chunk_by_boundaries(file_path, content, lines, boundaries)

    def _find_boundaries(
        self, content: str, lang: str
    ) -> list[tuple[int, str, str | None]]:
        """Find semantic boundaries (functions, classes, etc.)."""
        boundaries = []

        for chunk_type, pattern in self.patterns[lang].items():
            for match in pattern.finditer(content):
                line_num = content[:match.start()].count('\n') + 1
                # Extract name from appropriate group
                groups = match.groups()
                name = groups[-1] if groups else None
                boundaries.append((line_num, chunk_type, name))

        return sorted(boundaries, key=lambda x: x[0])

    def _chunk_by_boundaries(
        self,
        file_path: str,
        content: str,
        lines: list[str],
        boundaries: list[tuple[int, str, str | None]],
    ) -> Iterator[CodeChunk]:
        """Create chunks based on semantic boundaries."""

        for i, (start_line, chunk_type, name) in enumerate(boundaries):
            # Determine end line
            if i + 1 < len(boundaries):
                end_line = boundaries[i + 1][0] - 1
            else:
                end_line = len(lines)

            chunk_content = '\n'.join(lines[start_line - 1:end_line])

            # If chunk is too large, split it
            if len(chunk_content) > self.max_chunk_size:
                yield from self._chunk_by_size(
                    file_path,
                    chunk_content,
                    lines[start_line - 1:end_line],
                    start_offset=start_line - 1,
                    chunk_type=chunk_type,
                    name=name,
                )
            else:
                yield CodeChunk(
                    content=chunk_content,
                    file_path=file_path,
                    start_line=start_line,
                    end_line=end_line,
                    chunk_type=chunk_type,
                    name=name,
                )

    def _chunk_by_size(
        self,
        file_path: str,
        content: str,
        lines: list[str],
        start_offset: int = 0,
        chunk_type: str = 'fragment',
        name: str | None = None,
    ) -> Iterator[CodeChunk]:
        """Fall back to size-based chunking."""
        current_chunk = []
        current_size = 0
        chunk_start = 0

        for i, line in enumerate(lines):
            line_size = len(line) + 1  # +1 for newline

            if current_size + line_size > self.max_chunk_size and current_chunk:
                yield CodeChunk(
                    content='\n'.join(current_chunk),
                    file_path=file_path,
                    start_line=start_offset + chunk_start + 1,
                    end_line=start_offset + i,
                    chunk_type=chunk_type,
                    name=name,
                )

                # Overlap: keep some lines
                overlap_lines = []
                overlap_size = 0
                for prev_line in reversed(current_chunk):
                    if overlap_size + len(prev_line) > self.overlap:
                        break
                    overlap_lines.insert(0, prev_line)
                    overlap_size += len(prev_line) + 1

                current_chunk = overlap_lines
                current_size = overlap_size
                chunk_start = i - len(overlap_lines)

            current_chunk.append(line)
            current_size += line_size

        # Emit final chunk
        if current_chunk:
            yield CodeChunk(
                content='\n'.join(current_chunk),
                file_path=file_path,
                start_line=start_offset + chunk_start + 1,
                end_line=start_offset + len(lines),
                chunk_type=chunk_type,
                name=name,
            )


def iter_source_files(repo_path: str) -> Iterator[tuple[str, str]]:
    """Iterate over source files in a repository."""
    repo = Path(repo_path)
    extensions = {'.rs', '.scala', '.java'}

    for ext in extensions:
        for file_path in repo.rglob(f'*{ext}'):
            # Skip test files and generated code
            path_str = str(file_path)
            if '/target/' in path_str or '/test/' in path_str.lower():
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                # Return relative path for cleaner display
                rel_path = str(file_path.relative_to(repo.parent))
                yield rel_path, content
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
