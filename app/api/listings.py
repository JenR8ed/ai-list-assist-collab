"""eBay listing generation and draft management endpoints."""
from fastapi import APIRouter, HTTPException
from loguru import logger

from app.schemas.listing import ImageAnalysisResult, ListingDraft
from app.services.ebay import create_draft_listing

router = APIRouter()


@router.post("/draft", response_model=ListingDraft)
async def create_listing_draft(analysis: ImageAnalysisResult):
    """Convert an image analysis result into an eBay listing draft."""
    logger.info(f"Creating eBay draft for: {analysis.title}")
    try:
        draft = await create_draft_listing(analysis)
        return draft
    except Exception as e:
        logger.error(f"eBay draft creation failed: {e}")
        raise HTTPException(status_code=502, detail=str(e))
