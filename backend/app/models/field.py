from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.models.base import Base

class Field(Base):
  __tablename__ = "fields"

  id: Mapped[int] = mapped_column(primary_key=True)
  external_id: Mapped[str] = mapped_column(String, unique=True, index=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  level: Mapped[int] = mapped_column(Integer)