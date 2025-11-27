import httpx
from typing import Optional

OPENALEX_BASE_URL = "https://api.openalex.org"

class OpenAlexClient:
  def __init__(self):
    self.base_url = OPENALEX_BASE_URL

  async def get_works(self, query: str, per_page: int = 20, page: int = 1) -> dict:
    """
    Fetch papers ('works') from OpenAlex using a search query.
    """
    async with httpx.AsyncClient() as client:
      response = await client.get(
        f"{self.base_url}/works",
        params={
          "search": query,
          "per-page": per_page,
          "page": page
        }
      )
      response.raise_for_status()
      return response.json()