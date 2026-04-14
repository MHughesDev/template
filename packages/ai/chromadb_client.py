# packages/ai/chromadb_client.py
"""ChromaDB-backed embedding and retrieval (optional ``chromadb`` dependency)."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Any

from packages.ai.interfaces import EmbeddingProvider, RetrievalProvider

if TYPE_CHECKING:
    from apps.api.src.config import Settings


def _stable_fake_embedding(text: str, dim: int = 64) -> list[float]:
    """Deterministic pseudo-embedding when no ML model is configured."""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    out: list[float] = []
    while len(out) < dim:
        h = hashlib.sha256(h).digest()
        for b in h:
            out.append((b / 255.0) * 2.0 - 1.0)
            if len(out) >= dim:
                break
    return out[:dim]


class ChromaDBClient(EmbeddingProvider, RetrievalProvider):
    """HTTP Chroma client with a lightweight local embedding fallback."""

    def __init__(self, host: str, port: int, *, ai_enabled: bool) -> None:
        try:
            import chromadb  # noqa: PLC0415
        except ImportError as exc:
            msg = "chromadb is not installed; enable the ai-rag optional dependency"
            raise RuntimeError(msg) from exc

        self._chromadb = chromadb
        self._client = chromadb.HttpClient(host=host, port=port)
        self._ai_enabled = ai_enabled

    def _require_ai(self) -> None:
        if not self._ai_enabled:
            msg = "AI features are disabled (AI_ENABLED=false)"
            raise RuntimeError(msg)

    @classmethod
    async def from_settings(cls, settings: Settings) -> ChromaDBClient:
        """Build a client from application settings."""
        return cls(
            host=settings.chroma_host,
            port=settings.chroma_port,
            ai_enabled=settings.ai_enabled,
        )

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        self._require_ai()
        return [_stable_fake_embedding(t) for t in texts]

    async def embed_query(self, query: str) -> list[float]:
        self._require_ai()
        return _stable_fake_embedding(query)

    async def add_documents(
        self,
        documents: list[dict[str, Any]],
        collection: str,
    ) -> None:
        self._require_ai()
        coll = self._client.get_or_create_collection(collection)
        ids: list[str] = []
        texts: list[str] = []
        metadatas: list[dict[str, Any]] = []
        embeddings: list[list[float]] = []
        for doc in documents:
            doc_id = str(doc.get("id", ""))
            text = str(doc.get("text", ""))
            if not doc_id or not text:
                msg = "each document needs id and text"
                raise ValueError(msg)
            ids.append(doc_id)
            texts.append(text)
            meta = {k: v for k, v in doc.items() if k not in {"id", "text"}}
            metadatas.append(meta)
            embeddings.append(_stable_fake_embedding(text))
        coll.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,  # type: ignore[arg-type]
            embeddings=embeddings,  # type: ignore[arg-type]
        )

    async def query(
        self,
        query_embedding: list[float],
        collection: str,
        n_results: int,
    ) -> list[dict[str, Any]]:
        self._require_ai()
        coll = self._client.get_collection(collection)
        result = coll.query(
            query_embeddings=[query_embedding],  # type: ignore[arg-type]
            n_results=n_results,
        )
        out: list[dict[str, Any]] = []
        ids_list = result.get("ids") or []
        dist_list = result.get("distances") or []
        docs_list = result.get("documents") or []
        metas_list = result.get("metadatas") or []
        if not ids_list or not ids_list[0]:
            return out
        for i, doc_id in enumerate(ids_list[0]):
            out.append(
                {
                    "id": doc_id,
                    "distance": dist_list[0][i] if dist_list and dist_list[0] else None,
                    "text": docs_list[0][i] if docs_list and docs_list[0] else None,
                    "metadata": (
                        metas_list[0][i] if metas_list and metas_list[0] else {}
                    ),
                }
            )
        return out

    async def delete_documents(self, ids: list[str], collection: str) -> None:
        self._require_ai()
        coll = self._client.get_collection(collection)
        coll.delete(ids=ids)
