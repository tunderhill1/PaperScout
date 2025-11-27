from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime
from datetime import datetime
from pgvector.sqlalchemy import Vector

from app.models.base import Base


class Paper(Base):
  __tablename__ = "papers"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  external_id: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
  doi: Mapped[str | None] = mapped_column(String, nullable=True)
  title: Mapped[str] = mapped_column(String, nullable=False)
  abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
  published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
  citation_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  url: Mapped[str | None] = mapped_column(String, nullable=True)
  ingested_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=datetime.utcnow,
  )

  # vector embedding (MiniLM = 384 dimensions)
  embedding: Mapped[list[float] | None] = mapped_column(
    Vector(384),
    nullable=True,
  )