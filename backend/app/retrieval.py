import hashlib
import re
from pathlib import Path
from typing import Protocol

import chromadb

from .schemas import SimilarIncident


class Retriever(Protocol):
    def retrieve(self, query: str, top_k: int = 3) -> list[SimilarIncident]: ...


class VectorRetriever:
    def __init__(
        self,
        corpus_dir: str | Path,
        threshold: float = 0.15,
        store_path: str | Path = ".chroma",
    ):
        self.corpus_dir = Path(corpus_dir)
        self.threshold = threshold
        self._incidents = self._load_incidents()
        self._collection = None
        if self._incidents:
            client = chromadb.PersistentClient(path=str(store_path))
            self._collection = client.get_or_create_collection(
                name="incidents",
                metadata={"hnsw:space": "cosine"},
            )
            self._collection.upsert(
                ids=[str(incident["id"]) for incident in self._incidents],
                documents=[str(incident["text"]) for incident in self._incidents],
                metadatas=[
                    {
                        "id": str(incident["id"]),
                        "title": str(incident["title"]),
                    }
                    for incident in self._incidents
                ],
                embeddings=[self._embed(str(incident["text"])) for incident in self._incidents],
            )

    def _load_incidents(self) -> list[dict[str, object]]:
        incidents = []
        for path in sorted(self.corpus_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = next(
                (
                    line.removeprefix("# ").strip()
                    for line in text.splitlines()
                    if line.startswith("# ")
                ),
                path.stem,
            )
            incidents.append({"id": path.stem, "title": title, "text": text})
        return incidents

    @staticmethod
    def _embed(text: str) -> list[float]:
        vector = [0.0] * 128
        for token in re.findall(r"[a-z0-9_]+", text.lower()):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:2], "big") % len(vector)
            vector[index] += 1.0
        magnitude = sum(value * value for value in vector) ** 0.5
        return [value / magnitude for value in vector] if magnitude else vector

    def retrieve(self, query: str, top_k: int = 3) -> list[SimilarIncident]:
        if not self._collection or not query.strip():
            return []
        result = self._collection.query(
            query_embeddings=[self._embed(query)],
            n_results=min(top_k, len(self._incidents)),
            include=["metadatas", "distances"],
        )
        scored = [
            (1 - distance, metadata)
            for distance, metadata in zip(
                result["distances"][0], result["metadatas"][0], strict=True
            )
            if 1 - distance >= self.threshold
        ]
        return [
            SimilarIncident(id=str(metadata["id"]), title=str(metadata["title"]))
            for _, metadata in scored
        ]
