from sqlalchemy.orm import Session
from app.services.openalex_client import OpenAlexClient
from app.services.openalex_schemas import OpenAlexPaper
from app.models.paper import Paper

async def ingest_papers_from_query(db: Session, query: str):
  client = OpenAlexClient()
  data = await client.get_works(query=query)

  results = data.get("results", [])

  papers_added = 0

  for item in results:
    paper = OpenAlexPaper(**item)

    # prevent duplicates
    exists = db.query(Paper).filter_by(external_id=paper.id).first()
    if exists:
      continue

    db.add(Paper(
      external_id=paper.id,
      doi=paper.doi,
      title=paper.title,
      abstract=paper.abstract,
      published_year=paper.publication_year,
      citation_count=paper.cited_by_count,
      url=(paper.primary_location or {}).get("landing_page_url"),
    ))

    papers_added += 1

  db.commit()

  return {"added": papers_added, "total": len(results)}