from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.ingestion_logs import IngestionLog
from app.services.ingestion_logger import list_logs

router = APIRouter()

@router.get("/ingestion/status")
def ingestion_status(db: Session = Depends(get_db)):
  logs = db.query(IngestionLog).order_by(IngestionLog.id.desc()).limit(20).all()
  return [
    {
      "id": log.id,
      "query": log.query,
      "pages_processed": log.pages_processed,
      "papers_added": log.papers_added,
      "created_at": log.created_at
    }
    for log in logs
  ]


@router.get("/ingestion/logs")
def get_ingestion_logs(db: Session = Depends(get_db)):
  return [
    {
      "id": log.id,
      "query": log.query,
      "pages": log.pages_processed,
      "added": log.papers_added,
      "created_at": log.created_at,
    }
    for log in list_logs(db)
  ]