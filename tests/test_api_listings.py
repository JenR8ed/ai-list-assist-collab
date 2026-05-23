"""Tests for listing API endpoints."""
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.schemas.listing import ListingDraft
from tests.test_listings import MOCK_ANALYSIS

client = TestClient(app)

def test_create_listing_draft_success():
    """Test successful listing draft creation."""
    mock_draft = ListingDraft(
        analysis=MOCK_ANALYSIS,
        draft_id="12345",
        ebay_listing_url="https://ebay.com/draft/123"
    )

    with patch("app.api.listings.create_draft_listing", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_draft

        response = client.post(
            "/api/listings/draft",
            json=MOCK_ANALYSIS.model_dump()
        )

        assert response.status_code == 200
        data = response.json()
        assert data["draft_id"] == "12345"
        assert data["ebay_listing_url"] == "https://ebay.com/draft/123"
        assert data["analysis"]["title"] == MOCK_ANALYSIS.title

def test_create_listing_draft_error():
    """Test error handling when draft creation fails."""
    with patch("app.api.listings.create_draft_listing", new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = Exception("Service failure")

        response = client.post(
            "/api/listings/draft",
            json=MOCK_ANALYSIS.model_dump()
        )

        assert response.status_code == 502
        assert response.json()["detail"] == "Failed to create eBay draft. Please try again later."
