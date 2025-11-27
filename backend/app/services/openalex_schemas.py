from pydantic import BaseModel
from typing import Optional, List

class OpenAlexAuthor(BaseModel):
  author: dict  # contains id, display_name, etc.
  institutions: Optional[list] = None

class OpenAlexField(BaseModel):
  id: str
  display_name: str
  level: int

class OpenAlexPaper(BaseModel):
  id: str
  doi: Optional[str] = None
  title: Optional[str] = None
  abstract: Optional[str] = None
  publication_year: Optional[int] = None
  cited_by_count: Optional[int] = 0
  primary_location: Optional[dict] = None

  authorships: List[OpenAlexAuthor] = []
  concepts: List[OpenAlexField] = []