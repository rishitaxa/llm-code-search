import os
from typing import List

def chunk_code(text: str, max_lines: int = 40) -> List[str]:
    lines = text.splitlines()
    chunks = []
    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i:i + max_lines])
        if chunk.strip():
            chunks.append(chunk)
    return chunks
