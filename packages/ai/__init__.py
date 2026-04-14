# packages/ai/__init__.py
"""
BLUEPRINT: packages/ai/__init__.py

PURPOSE:
Package marker. Exports AI/RAG interfaces when the AI profile is enabled.
Provides graceful import failure when ChromaDB is not installed.
Optional per spec §26.9 item 242.
"""

# Graceful import: only available when ai-rag profile is enabled (chromadb installed)
try:
    from packages.ai.chromadb_client import ChromaDBClient
    from packages.ai.interfaces import (
        EmbeddingProvider,
        GenerationProvider,
        RetrievalProvider,
    )

    __all__ = [
        "EmbeddingProvider",
        "RetrievalProvider",
        "GenerationProvider",
        "ChromaDBClient",
    ]
except ImportError:
    # ChromaDB not installed — AI profile not enabled
    __all__ = []
