from sqlalchemy.orm import Session
from app.models.ingestion_logs import IngestionLog

def log_ingestion(db: Session, *, query: str, pages: int, added: int):
  entry = IngestionLog(
    query=query,
    pages_processed=pages,
    papers_added=added
  )
  db.add(entry)
  db.commit()
  return entry