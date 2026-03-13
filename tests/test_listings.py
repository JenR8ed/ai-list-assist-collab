"""Tests for listing draft creation."""
import pytest
from unittest.mock import AsyncMock, patch

from app.schemas.listing import ImageAnalysisResult, ListingDraft


MOCK_ANALYSIS = ImageAnalysisResult(
    title="Daisy Red Ryder BB Gun Vintage",
    description="Vintage Daisy Red Ryder BB gun. Good working condition. Classic collectible.",
    category="Sporting Goods > Hunting > Air Guns & Rifles",
    condition="Good",
    keywords=["daisy", "red ryder", "bb gun", "vintage", "collectible"],
    price_estimate_low=35.00,
    price_estimate_high=95.00,
    confidence=0.91,
    model_used="gemini-1.5-flash",
)


@pytest.mark.asyncio
async def test_create_draft_listing():
    from app.services.ebay import create_draft_listing
    draft = await create_draft_listing(MOCK_ANALYSIS)
    assert isinstance(draft, ListingDraft)
    assert draft.analysis.title == MOCK_ANALYSIS.title
