"""Multimodal vision service.
Primary:  Google Gemini 1.5 Flash (gemini-1.5-flash)
Fallback: Ollama LLaVA (local, offline)
"""
import json
import base64
import io
from typing import Optional

from PIL import Image
from loguru import logger

from app.core.config import settings
from app.schemas.listing import ImageAnalysisResult


LISTING_PROMPT = """
You are an expert eBay reseller. Analyze this product image and return ONLY valid JSON
matching this schema exactly — no markdown, no explanation:
{
  "title": "<eBay listing title, 80 chars max, keyword-rich>",
  "description": "<2-3 sentence HTML-ready description>",
  "category": "<most relevant eBay category>",
  "condition": "<New|Like New|Good|Fair|Poor>",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "price_estimate_low": <float>,
  "price_estimate_high": <float>,
  "confidence": <float 0.0-1.0>
}
"""


def _pil_to_base64(img: Image.Image, fmt: str = "JPEG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode()


async def _analyze_with_gemini(img: Image.Image, prompt: Optional[str]) -> ImageAnalysisResult:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold

    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    full_prompt = LISTING_PROMPT
    if prompt:
        full_prompt += f"\nExtra context from seller: {prompt}"

    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_data = {"mime_type": "image/jpeg", "data": buf.getvalue()}

    response = await model.generate_content_async(
        [full_prompt, image_data],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    raw = response.text.strip().lstrip("```json").rstrip("```").strip()
    data = json.loads(raw)
    data["model_used"] = "gemini-1.5-flash"
    return ImageAnalysisResult(**data)


async def _analyze_with_ollama(img: Image.Image, prompt: Optional[str]) -> ImageAnalysisResult:
    import httpx

    b64 = _pil_to_base64(img)
    full_prompt = LISTING_PROMPT
    if prompt:
        full_prompt += f"\nExtra context from seller: {prompt}"

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            f"{settings.ollama_base_url}/api/generate",
            json={
                "model": settings.ollama_model,
                "prompt": full_prompt,
                "images": [b64],
                "stream": False,
            },
        )
        resp.raise_for_status()
        raw = resp.json()["response"].strip().lstrip("```json").rstrip("```").strip()

    data = json.loads(raw)
    data["model_used"] = settings.ollama_model
    return ImageAnalysisResult(**data)


async def analyze_image(img: Image.Image, prompt: Optional[str] = None) -> ImageAnalysisResult:
    """Try Gemini first; fall back to local Ollama LLaVA if unavailable."""
    if settings.google_api_key:
        try:
            logger.info("Vision: using Gemini 1.5 Flash")
            return await _analyze_with_gemini(img, prompt)
        except Exception as e:
            logger.warning(f"Gemini failed ({e}), falling back to Ollama")

    logger.info(f"Vision: using Ollama ({settings.ollama_model})")
    return await _analyze_with_ollama(img, prompt)
