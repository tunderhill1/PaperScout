from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.embedding_service import compute_paper_embedding

def semantic_search(db: Session, query: str, limit: int = 10):
  """
  Vector-based semantic search using pgvector cosine distance.
  """

  # Compute query embedding
  embedding = compute_paper_embedding(query, None)  # just one string

  sql = text("""
    SELECT
      id,
      title,
      abstract,
      url,
      published_year,
      citation_count,
      embedding <=> (:embedding)::vector AS distance
    FROM papers
    ORDER BY embedding <=> (:embedding)::vector
    LIMIT :limit
  """)

  # SQLAlchemy automatically converts Python lists to vector
  rows = db.execute(sql, {"embedding": embedding, "limit": limit}).mappings().all()

  return rows