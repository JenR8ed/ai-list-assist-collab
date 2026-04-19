from unittest.mock import AsyncMock, patch
from app.schemas.listing import ValuationResult

def test_estimate_price_endpoint_success(client):
    """Verify happy path for valuation endpoint using TestClient."""
    payload = {"title": "Test Item", "condition": "New"}
    expected_result = ValuationResult(
        title="Test Item",
        price_low=10.0,
        price_high=20.0,
        price_median=15.0,
        comparable_sold_count=5
    )

    with patch("app.api.valuation.get_valuation", new=AsyncMock(return_value=expected_result)):
        response = client.post("/api/valuation/estimate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["price_median"] == 15.0
    assert data["comparable_sold_count"] == 5

def test_estimate_price_endpoint_failure(client):
    """Verify 502 error when valuation service fails."""
    payload = {"title": "Test Item"}

    with patch("app.api.valuation.get_valuation", new=AsyncMock(side_effect=Exception("Service Down"))):
        response = client.post("/api/valuation/estimate", json=payload)

    assert response.status_code == 502
    assert response.json()["detail"] == "Valuation service failed. Please try again later."

def test_estimate_price_invalid_request(client):
    """Verify 422 error for invalid request body."""
    # Missing required 'title' field
    payload = {"condition": "New"}
    response = client.post("/api/valuation/estimate", json=payload)
    assert response.status_code == 422
