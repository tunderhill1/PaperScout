from sentence_transformers import SentenceTransformer
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# MiniLM-L6-v2 produces 384-dim embeddings
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
  """
  Load the embedding model once (singleton).
  Using LRU cache avoids reloading the model.
  """
  logger.info(f"Loading embedding model: {MODEL_NAME}")
  model = SentenceTransformer(MODEL_NAME)
  return model


def compute_paper_embedding(title: str, abstract: str | None) -> list[float]:
  """
  Compute a dense embedding using title + abstract.
  """
  model = get_embedding_model()

  # Combine text fields
  text = title
  if abstract:
    text = title + " " + abstract

  vec = model.encode(text, convert_to_numpy=True)
  return vec.tolist()