"""Pydantic schemas for listing generation and valuation."""
from typing import List, Optional
from pydantic import BaseModel, Field


class ImageAnalysisRequest(BaseModel):
    prompt: Optional[str] = Field(
        default=None,
        description="Optional extra context about the item (e.g. brand, condition)",
    )


class ImageAnalysisResult(BaseModel):
    title: str = Field(description="Suggested eBay listing title (80 chars max)")
    description: str = Field(description="Full HTML-ready item description")
    category: str = Field(description="Suggested eBay category")
    condition: str = Field(description="Item condition: New / Like New / Good / Fair / Poor")
    keywords: List[str] = Field(description="SEO keywords for the listing")
    price_estimate_low: float = Field(description="Low end price estimate (USD)")
    price_estimate_high: float = Field(description="High end price estimate (USD)")
    confidence: float = Field(description="Model confidence score 0.0–1.0")
    model_used: str = Field(description="AI model that generated this result")


class ListingDraft(BaseModel):
    analysis: ImageAnalysisResult
    ebay_listing_url: Optional[str] = None
    draft_id: Optional[str] = None


class ValuationRequest(BaseModel):
    title: str
    category: Optional[str] = None
    condition: Optional[str] = None
    keywords: Optional[List[str]] = None


class ValuationResult(BaseModel):
    title: str
    price_low: float
    price_high: float
    price_median: float
    comparable_sold_count: int
    source: str = "eBay Finding API"
