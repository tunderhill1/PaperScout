from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, String
from app.models.base import Base

class IngestionLog(Base):
  __tablename__ = "ingestion_logs"

  id: Mapped[int] = mapped_column(primary_key=True)
  query: Mapped[str] = mapped_column(String, nullable=False)
  pages_processed: Mapped[int] = mapped_column(Integer, nullable=False)
  papers_added: Mapped[int] = mapped_column(Integer, nullable=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=datetime.utcnow
  )