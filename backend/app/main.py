from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config.settings import settings
from app.core.database import engine, create_all

def create_app() -> FastAPI:
  app = FastAPI(
    title="PaperScout",
    version="0.1.0",
    description="Backend API for PaperScout: research paper search and recommendations.",
  )

  print(f"Running in: {settings.environment}")
  print(f"Database URL: {settings.database_url}")

  # Test DB connection at startup
  with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Database connected:", result.scalar())

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
  
  # Debug-only: ensure tables exist
  create_all()

  return app

app = create_app()
