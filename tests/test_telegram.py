"""Tests for telegram service utilities."""
import pytest
from unittest.mock import AsyncMock

from app.services.telegram import send_listing_summary
from tests.test_listings import MOCK_ANALYSIS


@pytest.mark.asyncio
async def test_send_listing_summary():
    """Test sending listing summary formats correctly and calls bot send_message."""
    bot_mock = AsyncMock()
    chat_id = 123456789

    await send_listing_summary(bot_mock, chat_id, MOCK_ANALYSIS)

    bot_mock.send_message.assert_called_once()

    call_args = bot_mock.send_message.call_args.kwargs
    assert call_args["chat_id"] == chat_id
    assert call_args["parse_mode"] == "Markdown"

    # Check text content
    text = call_args["text"]
    assert MOCK_ANALYSIS.title in text
    assert MOCK_ANALYSIS.condition in text
    assert MOCK_ANALYSIS.category in text
    assert f"${MOCK_ANALYSIS.price_estimate_low:.2f}" in text
    assert f"${MOCK_ANALYSIS.price_estimate_high:.2f}" in text
    assert MOCK_ANALYSIS.model_used in text
    assert MOCK_ANALYSIS.description in text

    # Check keywords (first 5)
    for keyword in MOCK_ANALYSIS.keywords[:5]:
        assert keyword in text
