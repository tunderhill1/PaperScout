import httpx
from typing import Optional

OPENALEX_BASE_URL = "https://api.openalex.org"

class OpenAlexClient:
  def __init__(self):
    self.base_url = OPENALEX_BASE_URL

  async def get_works_page(self, query: str, per_page: int = 20, page: int = 1) -> dict:
    async with httpx.AsyncClient() as client:
      response = await client.get(
        f"{self.base_url}/works",
        params={
          "search": query,
          "per-page": per_page,
          "page": page,
        },
        timeout=30.0
      )
      response.raise_for_status()
      return response.json()