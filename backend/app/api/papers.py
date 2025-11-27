from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.paper import Paper

router = APIRouter()

@router.get("/")
def list_papers(db: Session = Depends(get_db)):
  papers = db.query(Paper).limit(10).all()
  return papers
