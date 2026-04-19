from unittest.mock import AsyncMock, patch
from app.schemas.listing import ImageAnalysisResult, ListingDraft

MOCK_ANALYSIS = ImageAnalysisResult(
    title="Vintage BB Gun",
    description="Vintage BB gun in good condition.",
    category="Sporting Goods > Hunting > Air Guns",
    condition="Good",
    keywords=["bb gun", "vintage"],
    price_estimate_low=50.0,
    price_estimate_high=100.0,
    confidence=0.95,
    model_used="gemini-1.5-flash",
)

def test_create_listing_draft_success(client):
    """Verify happy path for creating a listing draft."""
    expected_draft = ListingDraft(
        analysis=MOCK_ANALYSIS,
        ebay_listing_url=None,
        draft_id="12345"
    )

    with patch("app.api.listings.create_draft_listing", new=AsyncMock(return_value=expected_draft)):
        response = client.post("/api/listings/draft", json=MOCK_ANALYSIS.model_dump())

    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["title"] == MOCK_ANALYSIS.title
    assert data["draft_id"] == "12345"

def test_create_listing_draft_failure(client):
    """Verify 502 error when draft creation fails."""
    with patch("app.api.listings.create_draft_listing", new=AsyncMock(side_effect=Exception("eBay API error"))):
        response = client.post("/api/listings/draft", json=MOCK_ANALYSIS.model_dump())

    assert response.status_code == 502
    assert "Failed to create eBay draft" in response.json()["detail"]
