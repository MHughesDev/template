# packages/ai/chromadb_client.py
"""

PURPOSE:
ChromaDB client implementation of EmbeddingProvider and RetrievalProvider.
Manages ChromaDB connection, collection operations, document ingestion, and
similarity queries. Behind packages/ai/interfaces.py abstractions.
Optional per spec §26.9 item 244.

DEPENDS ON:
- chromadb — ChromaDB client (installed only in ai-rag profile)
- apps.api.src.config — settings for CHROMA_HOST, CHROMA_PORT
- packages.ai.interfaces — EmbeddingProvider, RetrievalProvider protocols
- sentence_transformers or openai — embedding model (based on EMBEDDING_PROVIDER setting)

DEPENDED ON BY:
- packages.ai.__init__ — exports ChromaDBClient
- (future): ai service layers that need retrieval

CLASSES:

  ChromaDBClient:
    PURPOSE: Production ChromaDB client implementing EmbeddingProvider and RetrievalProvider.
    FIELDS:
      - _client: chromadb.HttpClient — connection to ChromaDB server
      - _embedding_fn — embedding function (OpenAI, local model, or ChromaDB default)
    METHODS:

      @classmethod
      async from_settings(settings: Settings) -> ChromaDBClient:
        PURPOSE: Factory method creating client from application settings.
        STEPS:
          1. Create chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
          2. Determine embedding function from settings.embedding_provider
          3. Return initialized ChromaDBClient

      async embed_texts(texts: list[str]) -> list[list[float]]:
        PURPOSE: Generate embeddings for multiple texts.
        STEPS: Use configured embedding function to embed all texts.
        RETURNS: list of embedding vectors

      async embed_query(query: str) -> list[float]:
        PURPOSE: Generate embedding for a single query.
        RETURNS: Embedding vector

      async add_documents(documents: list[dict], collection: str) -> None:
        PURPOSE: Add documents to a ChromaDB collection.
        STEPS:
          1. Get or create collection with get_or_create_collection()
          2. Extract: ids, texts, metadatas from documents
          3. Generate embeddings for texts
          4. collection.add(embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids)

      async query(query_embedding: list[float], collection: str, n_results: int) -> list[dict]:
        PURPOSE: Find similar documents by embedding similarity.
        STEPS:
          1. Get collection
          2. collection.query(query_embeddings=[query_embedding], n_results=n_results)
          3. Parse results into list of dicts with id, text, metadata, distance
        RETURNS: list of matching documents with similarity scores

      async delete_documents(ids: list[str], collection: str) -> None:
        PURPOSE: Delete documents by ID from a collection.
        STEPS: Get collection; collection.delete(ids=ids)

DESIGN DECISIONS:
- HttpClient (not in-process): ChromaDB runs in separate container (persistent volumes)
- Embedding function is configurable: OpenAI (production) or local model (offline/dev)
- Persistent volume: data survives ChromaDB container restarts
- Kill switch: all methods decorated with @requires_ai_enabled (from interfaces.py)
"""
