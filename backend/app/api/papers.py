from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.paper import Paper
from app.services.search_service import semantic_search

router = APIRouter()

@router.get("/")
def list_papers(db: Session = Depends(get_db)):
  papers = db.query(Paper).limit(10).all()
  return papers

@router.get("/search")
def search(
  query: str,
  limit: int = 10,
  db: Session = Depends(get_db)
):
  results = semantic_search(db, query, limit)
  return {"query": query, "results": results}

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