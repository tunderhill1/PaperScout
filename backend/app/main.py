from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
  app = FastAPI(
    title="PaperScout",
    version="0.1.0",
    description="Backend API for PaperScout: research paper search and recommendations.",
  )

  # CORS – will later restrict to frontend domain
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