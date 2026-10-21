
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once and reuse it."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 64,
        },
    )


def generate_embeddings(texts):
    """Generate embeddings for a list of documents."""
    if not texts:
        return []

    return get_embedding_model().embed_documents(texts)


def generate_query_embedding(query):
    """Generate an embedding for a search query."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query cannot be empty.")

    return get_embedding_model().embed_query(query.strip())
