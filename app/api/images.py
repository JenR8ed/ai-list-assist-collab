"""Image upload and multimodal AI analysis endpoints."""
import io
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image
from loguru import logger

from app.schemas.listing import ImageAnalysisResult
from app.services.vision import analyze_image

router = APIRouter()

MAX_SIZE_MB = 10
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@router.post("/analyze", response_model=ImageAnalysisResult)
async def analyze_listing_image(
    file: UploadFile = File(..., description="Product image to analyze"),
    prompt: str = Form(default="", description="Optional context about the item"),
):
    """Upload a product image and receive AI-generated listing details."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported image type: {file.content_type}")

    contents = await file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"Image exceeds {MAX_SIZE_MB}MB limit")

    try:
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        logger.exception("Could not decode image")
        raise HTTPException(status_code=422, detail="Could not decode image")

    logger.info(f"Analyzing image: {file.filename} ({file.content_type}, {len(contents)//1024}KB)")

    result = await analyze_image(img, prompt=prompt or None)
    return result
