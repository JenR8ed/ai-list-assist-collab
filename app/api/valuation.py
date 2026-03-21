"""Price valuation endpoints using eBay sold listings data."""
from fastapi import APIRouter, HTTPException
from loguru import logger

from app.schemas.listing import ValuationRequest, ValuationResult
from app.services.ebay import get_valuation

router = APIRouter()


@router.post("/estimate", response_model=ValuationResult)
async def estimate_price(request: ValuationRequest):
    """Return price estimate based on eBay recently-sold comparable listings."""
    logger.info(f"Valuation request for: {request.title}")
    try:
        result = await get_valuation(request)
        return result
    except Exception as e:
        logger.error(f"Valuation failed: {e}")
        raise HTTPException(status_code=502, detail="Valuation service failed. Please try again later.")
