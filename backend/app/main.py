from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings

def create_app() -> FastAPI:
  app = FastAPI(
    title="PaperScout",
    version="0.1.0",
    description="Backend API for PaperScout: research paper search and recommendations.",
  )

  print(f"Running in: {settings.environment}")
  print(f"DB URL: {settings.database_url}")

  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  @app.get("/health")
  async def health_check():
    return {"status": "ok"}

  return app

app = create_app()
