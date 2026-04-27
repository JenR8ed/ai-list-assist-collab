"""Tests for valuation API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.schemas.listing import ValuationResult

client = TestClient(app)

def test_estimate_price_success():
    """Test successful price estimation."""
    mock_result = ValuationResult(
        title="Test Item",
        price_low=10.0,
        price_high=20.0,
        price_median=15.0,
        comparable_sold_count=5,
        source="eBay Finding API"
    )

    with patch("app.api.valuation.get_valuation", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_result

        response = client.post(
            "/api/valuation/estimate",
            json={"title": "Test Item"}
        )

        assert response.status_code == 200
        assert response.json()["price_median"] == 15.0
        assert response.json()["comparable_sold_count"] == 5

def test_estimate_price_error():
    """Test error handling when valuation service fails."""
    with patch("app.api.valuation.get_valuation", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("Service failure")

        response = client.post(
            "/api/valuation/estimate",
            json={"title": "Test Item"}
        )

        assert response.status_code == 502
        assert response.json()["detail"] == "Valuation service failed. Please try again later."
