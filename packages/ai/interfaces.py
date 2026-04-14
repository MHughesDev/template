# packages/ai/interfaces.py
"""

PURPOSE:
Abstract Protocol interfaces for AI/RAG operations: embedding generation,
document retrieval, and text generation. Provider-agnostic — ChromaDB and
OpenAI are concrete implementations behind these abstractions.
Kill switch check is built into the base decorator.
Optional per spec §26.9 item 243.

DEPENDS ON:
- typing — Protocol, runtime_checkable, Any
- functools — wraps (for kill switch decorator)
- apps.api.src.config — get_settings (for AI_ENABLED kill switch)

DEPENDED ON BY:
- packages.ai.chromadb_client — implements these protocols
- apps.api.src.*/service.py — uses these interfaces for AI features

CLASSES:

  EmbeddingProvider(Protocol):
    PURPOSE: Protocol for embedding vector generation from text.
    METHODS:
      - async embed_texts(texts: list[str]) -> list[list[float]]
        Generate embeddings for a list of texts.
      - async embed_query(query: str) -> list[float]
        Generate embedding for a single query text.

  RetrievalProvider(Protocol):
    PURPOSE: Protocol for document retrieval from a vector store.
    METHODS:
      - async add_documents(documents: list[dict], collection: str) -> None
        Add documents (with embeddings) to the specified collection.
      - async query(query_embedding: list[float], collection: str, n_results: int) -> list[dict]
        Find the n_results most similar documents to the query embedding.
      - async delete_documents(ids: list[str], collection: str) -> None
        Delete documents by ID from the collection.

  GenerationProvider(Protocol):
    PURPOSE: Protocol for LLM text generation (optional — not all RAG systems need this).
    METHODS:
      - async generate(prompt: str, context: list[str] | None = None) -> str
        Generate text given a prompt and optional context documents.

FUNCTIONS:

  requires_ai_enabled(func):
    PURPOSE: Decorator that checks AI_ENABLED setting before executing AI operations.
    STEPS:
      1. Check settings.ai_enabled
      2. If False: raise RuntimeError("AI features are disabled (AI_ENABLED=false)")
      3. If True: execute the decorated function
    NOTES: Applied to all AI provider method implementations as a kill switch

DESIGN DECISIONS:
- Protocol (not ABC): structural typing; swap providers without base class inheritance
- Kill switch via decorator: single point of enforcement for AI_ENABLED=false
- Provider-agnostic: ChromaDB is one implementation; swap for Pinecone/Weaviate without code changes
- RuntimeError on disabled: surfaces clearly in logs; caught by global error handler → 503
"""
