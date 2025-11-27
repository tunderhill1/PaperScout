from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.paper import Paper

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