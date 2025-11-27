from sqlalchemy.orm import Session
from app.services.openalex_client import OpenAlexClient
from app.services.openalex_schemas import OpenAlexPaper
from app.models.paper import Paper
from app.services.ingestion_helpers import get_or_create_author, get_or_create_field
from app.models.paper_author import PaperAuthor
from app.models.paper_field import PaperField

import logging
logger = logging.getLogger(__name__)

async def ingest_papers_from_query(db: Session, query: str, max_pages: int = 5):
  client = OpenAlexClient()
  total_added = 0

  for page in range(1, max_pages + 1):
    data = await client.get_works_page(query=query, page=page)

    results = data.get("results", [])
    if not results:
      break

    for item in results:
      paper_data = OpenAlexPaper(**item)

      # Skip malformed entries
      if not paper_data.id or not paper_data.title:
        continue

      # Prevent duplicates
      existing_paper = db.query(Paper).filter_by(external_id=paper_data.id).first()
      if existing_paper:
        continue

      # Insert paper
      paper = Paper(
        external_id=paper_data.id,
        doi=paper_data.doi,
        title=paper_data.title,
        abstract=paper_data.abstract,
        published_year=paper_data.publication_year,
        citation_count=paper_data.cited_by_count or 0,
        url=(paper_data.primary_location or {}).get("landing_page_url"),
      )

      db.add(paper)
      db.flush()  # ensures paper.id is available

      # Add authors
      for author_entry in paper_data.authorships:
        author_info = author_entry.author
        if not author_info:
          continue

        author = get_or_create_author(
          db=db,
          external_id=author_info["id"],
          name=author_info.get("display_name", "Unknown")
        )

        db.add(PaperAuthor(
          paper_id=paper.id,
          author_id=author.id
        ))

      # Add fields (concepts)
      for field_entry in paper_data.concepts:
        field = get_or_create_field(
          db=db,
          external_id=field_entry.id,
          name=field_entry.display_name,
          level=field_entry.level
        )

        db.add(PaperField(
          paper_id=paper.id,
          field_id=field.id
        ))

      total_added += 1

    db.commit()

  return {
    "added": total_added,
    "pages_processed": page
  }
