# packages/ai/__init__.py
"""AI/RAG exports when ChromaDB and optional deps are available."""

from __future__ import annotations

try:
    from packages.ai.chromadb_client import ChromaDBClient
    from packages.ai.interfaces import (
        EmbeddingProvider,
        GenerationProvider,
        RetrievalProvider,
    )

    __all__ = [
        "ChromaDBClient",
        "EmbeddingProvider",
        "GenerationProvider",
        "RetrievalProvider",
    ]
except ImportError:
    __all__ = []
