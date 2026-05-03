import sys
import pytest
from unittest.mock import MagicMock, AsyncMock

# Mock loguru to allow importing the service without the dependency
sys.modules["loguru"] = MagicMock()

from app.services.telegram import send_listing_summary  # noqa: E402
from app.schemas.listing import ImageAnalysisResult  # noqa: E402

@pytest.fixture
def mock_analysis_with_markdown():
    """Fixture providing an analysis result with markdown characters to ensure they are escaped."""
    return ImageAnalysisResult(
        title="Test * Item_",
        description="A [test] `description`",
        category="Test Category",
        condition="Good",
        keywords=["test", "item", "keyword_1"],
        price_estimate_low=10.0,
        price_estimate_high=20.0,
        confidence=0.9,
        model_used="gemini-1.5-flash"
    )

@pytest.mark.asyncio
async def test_send_listing_summary(mock_analysis_with_markdown):
    """Verify send_listing_summary correctly formats and sends a markdown message."""
    mock_bot = AsyncMock()
    chat_id = 12345

    await send_listing_summary(mock_bot, chat_id, mock_analysis_with_markdown)

    mock_bot.send_message.assert_called_once()

    # Verify arguments
    call_args = mock_bot.send_message.call_args[1]
    assert call_args["chat_id"] == chat_id
    assert call_args["parse_mode"] == "Markdown"

    # Verify the escaped text is in the message
    text = call_args["text"]
    assert r"Test \* Item\_" in text
    assert r"A \[test] \`description\`" in text
    assert "$10.00 – $20.00" in text
    assert r"keyword\_1" in text
