from pydantic import BaseModel
from typing import Optional, List

class OpenAlexPaper(BaseModel):
  id: str
  doi: Optional[str] = None
  title: str
  abstract: Optional[str] = None
  publication_year: Optional[int] = None
  cited_by_count: int
  primary_location: Optional[dict] = None