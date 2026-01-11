import os
import faiss
import numpy as np
from typing import List, Dict
from .chunker import chunk_code
from .embeddings import get_model
from .llm_reranker import explain

class CodeSearchEngine:
    def __init__(self):
        self.model = get_model()
        self.index = None
        self.chunks = []

    def index_directory(self, path: str):
        texts = []
        self.chunks = []

        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith((".py", ".js", ".ts")):
                    full = os.path.join(root, f)
                    with open(full, encoding="utf-8", errors="ignore") as file:
                        for chunk in chunk_code(file.read()):
                            texts.append(chunk)
                            self.chunks.append({
                                "file": full,
                                "content": chunk
                            })

        emb = self.model.encode(texts, normalize_embeddings=True)
        self.index = faiss.IndexFlatIP(emb.shape[1])
        self.index.add(emb.astype("float32"))

    def search(self, query: str, k: int = 5) -> List[Dict]:
        q_emb = self.model.encode([query], normalize_embeddings=True)
        scores, ids = self.index.search(q_emb.astype("float32"), k)

        results = []
        for idx, score in zip(ids[0], scores[0]):
            chunk = self.chunks[idx]
            results.append({
                "file": chunk["file"],
                "score": float(score),
                "content": chunk["content"],
                "explanation": explain(query, chunk["content"])
            })
        return results
