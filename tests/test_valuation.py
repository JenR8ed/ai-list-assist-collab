"""Tests for eBay valuation service."""
import pytest
from unittest.mock import patch, MagicMock

from app.schemas.listing import ValuationRequest, ValuationResult


@pytest.mark.asyncio
async def test_valuation_no_results():
    """Should return zeros when no eBay comps found."""
    mock_api = MagicMock()
    mock_response = MagicMock()
    mock_response.reply.searchResult.item = []
    mock_api.execute.return_value = mock_response

    with patch("app.services.ebay._get_finding_api", return_value=mock_api):
        from app.services.ebay import get_valuation
        result = await get_valuation(ValuationRequest(title="obscure item xyz"))

    assert result.price_median == 0.0
    assert result.comparable_sold_count == 0
