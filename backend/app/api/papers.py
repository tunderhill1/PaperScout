from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.paper import Paper
from app.services.search_service import semantic_search
from app.services.hybrid_search import hybrid_search
from typing import List, Optional

router = APIRouter()

@router.get("/")
def list_papers(db: Session = Depends(get_db)):
  papers = db.query(Paper).limit(10).all()
  return papers

@router.post("/ingest")
async def ingest(
  query: str,
  background_tasks: BackgroundTasks,
  pages: int = 5,
  db: Session = Depends(get_db)
):
  from app.services.ingest_papers import ingest_papers_from_query
  background_tasks.add_task(ingest_papers_from_query, db, query, pages)
  return {"status": "started", "query": query, "pages": pages}

@router.post("/ingest_and_wait")
async def ingest_and_wait(
    query: str,
    pages: int = 1,
    db: Session = Depends(get_db)
):
    # Direct import to avoid circular issues
    from app.services.ingest_papers import ingest_papers_from_query

    # Run ingestion synchronously
    result = await ingest_papers_from_query(db, query, max_pages=pages)

    return {
        "status": "completed",
        "query": query,
        "pages": result.get("pages_processed"),
        "added": result.get("added"),
        "log_id": result.get("log_id")
    }

@router.get("/search")
def search(
  query: str,
  limit: int = 10,
  db: Session = Depends(get_db)
):
  results = semantic_search(db, query, limit)
  return {"query": query, "results": results}

@router.get("/search/hybrid")
def hybrid(
  query: str,
  sort_by: str = "final_score",
  limit: int = 10,
  db: Session = Depends(get_db)
):
  results = hybrid_search(db, query, limit)
  results.sort(key = lambda x: x[sort_by], reverse = (sort_by == "published_year" or sort_by == "citation_count"))
  return {"query": query, "results": results}
