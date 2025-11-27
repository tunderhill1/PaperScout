from sqlalchemy.orm import Session
from app.models.author import Author
from app.models.field import Field
from app.models.paper_author import PaperAuthor
from app.models.paper_field import PaperField

def get_or_create_author(db: Session, external_id: str, name: str) -> Author:
  author = db.query(Author).filter_by(external_id=external_id).first()
  if author:
    return author

  author = Author(
    external_id=external_id,
    name=name
  )
  db.add(author)
  db.flush()   # ensures author.id is available
  return author


def get_or_create_field(db: Session, external_id: str, name: str, level: int) -> Field:
  field = db.query(Field).filter_by(external_id=external_id).first()
  if field:
    return field

  field = Field(
    external_id=external_id,
    name=name,
    level=level
  )
  db.add(field)
  db.flush()   # ensures field.id is available
  return field