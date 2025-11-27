from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.paper import Paper
from app.services.ingest_papers import ingest_papers_from_query

router = APIRouter()

@router.get("/")
def list_papers(db: Session = Depends(get_db)):
  papers = db.query(Paper).limit(10).all()
  return papers

@router.post("/ingest")
async def ingest(query: str, db: Session = Depends(get_db)):
  result = await ingest_papers_from_query(db, query)
  return result