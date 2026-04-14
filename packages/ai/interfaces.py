# packages/ai/interfaces.py
"""Protocols for embedding, retrieval, and generation (provider-agnostic)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Generate dense vectors from text."""

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding per input string."""
        ...

    async def embed_query(self, query: str) -> list[float]:
        """Return a single query embedding."""
        ...


@runtime_checkable
class RetrievalProvider(Protocol):
    """Vector store read/write for RAG."""

    async def add_documents(
        self,
        documents: list[dict[str, Any]],
        collection: str,
    ) -> None:
        """Ingest documents (must include text and stable ids)."""
        ...

    async def query(
        self,
        query_embedding: list[float],
        collection: str,
        n_results: int,
    ) -> list[dict[str, Any]]:
        """Return nearest neighbors with scores and metadata."""
        ...

    async def delete_documents(self, ids: list[str], collection: str) -> None:
        """Remove documents by id."""
        ...


@runtime_checkable
class GenerationProvider(Protocol):
    """Optional LLM text generation."""

    async def generate(self, prompt: str, context: list[str] | None = None) -> str:
        """Produce text from a prompt and optional retrieved context."""
        ...
