from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.embedding_service import compute_paper_embedding

def hybrid_search(db: Session, query: str, limit: int = 10):
  emb = compute_paper_embedding(query, None)

  sql = text("""
    WITH ranked AS (
      SELECT
        id,
        title,
        abstract,
        url,
        published_year,
        citation_count,
        -- semantic distance
        (embedding <=> (:emb)::vector) AS distance,

        -- recency score (0 to 1)
        CASE 
          WHEN published_year IS NULL THEN 1
          ELSE LEAST(1.0, (2025 - published_year) / 10.0)
        END AS recency_score,

        -- popularity score (0 to 1)
        CASE 
          WHEN citation_count IS NULL THEN 1
          ELSE 1.0 / (1 + citation_count)
        END AS popularity_score
      FROM papers
    )

    SELECT
      *,
      -- Weighted final score
      (0.65 * distance) +
      (0.20 * recency_score) +
      (0.15 * popularity_score) AS final_score

    FROM ranked
    ORDER BY final_score ASC
    LIMIT :limit;
  """)

  results = db.execute(sql, {"emb": emb, "limit": limit}).mappings().all()
  return results