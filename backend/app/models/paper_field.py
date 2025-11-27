from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

# many papers to many fields
class PaperField(Base):
  __tablename__ = "paper_fields"

  id: Mapped[int] = mapped_column(primary_key=True)
  paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id"))
  field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"))