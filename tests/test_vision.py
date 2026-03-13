"""Tests for vision service — mocked AI responses."""
import pytest
import io
from unittest.mock import AsyncMock, patch, MagicMock
from PIL import Image

from app.schemas.listing import ImageAnalysisResult


def make_test_image() -> Image.Image:
    return Image.new("RGB", (100, 100), color=(128, 64, 32))


MOCK_RESULT = ImageAnalysisResult(
    title="Vintage Barbie Doll 1980s Original Box",
    description="Classic 1980s Barbie doll in original box. Light play wear. Great for collectors.",
    category="Dolls & Bears > Dolls > Barbie Contemporary",
    condition="Good",
    keywords=["barbie", "vintage", "1980s", "collectible", "doll"],
    price_estimate_low=18.00,
    price_estimate_high=45.00,
    confidence=0.87,
    model_used="gemini-1.5-flash",
)


@pytest.mark.asyncio
async def test_analyze_image_returns_result():
    img = make_test_image()
    with patch("app.services.vision._analyze_with_gemini", new=AsyncMock(return_value=MOCK_RESULT)):
        from app.services.vision import analyze_image
        result = await analyze_image(img)
    assert result.title == MOCK_RESULT.title
    assert result.price_estimate_low > 0
    assert 0 <= result.confidence <= 1.0


@pytest.mark.asyncio
async def test_fallback_to_ollama_on_gemini_failure():
    img = make_test_image()
    ollama_result = MOCK_RESULT.model_copy(update={"model_used": "llava:7b"})
    with patch("app.services.vision._analyze_with_gemini", new=AsyncMock(side_effect=Exception("API error"))):
        with patch("app.services.vision._analyze_with_ollama", new=AsyncMock(return_value=ollama_result)):
            from app.services.vision import analyze_image
            result = await analyze_image(img)
    assert result.model_used == "llava:7b"
