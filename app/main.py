"""AI List Assist — FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.api import images, listings, valuation


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🤖 AI List Assist starting up...")
    yield
    logger.info("AI List Assist shutting down.")


app = FastAPI(
    title="AI List Assist",
    description=(
        "Generative AI-powered eBay listing assistant. "
        "Upload a product image → get title, description, category, "
        "price estimate, and a ready-to-post eBay listing."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(listings.router, prefix="/api/listings", tags=["listings"])
app.include_router(valuation.router, prefix="/api/valuation", tags=["valuation"])


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "service": "ai-list-assist", "version": "0.1.0"}
