from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from app.models.base import Base

class Paper(Base):
  __tablename__ = "papers"

  # Columns in the database
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String, nullable=False)
  abstract: Mapped[str] = mapped_column(Text, nullable=False)
  published_year: Mapped[int] = mapped_column(Integer, nullable=True)
