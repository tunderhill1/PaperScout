from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

# many papers to many authors
class PaperAuthor(Base):
  __tablename__ = "paper_authors"

  id: Mapped[int] = mapped_column(primary_key=True)
  paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id"))
  author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))