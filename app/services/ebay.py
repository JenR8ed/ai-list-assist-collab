"""eBay API service — listing drafts and price valuation via sold comps."""
import statistics

from loguru import logger

from app.core.config import settings
from app.schemas.listing import ImageAnalysisResult, ListingDraft, ValuationRequest, ValuationResult


def _get_finding_api():
    from ebaysdk.finding import Connection
    return Connection(
        appid=settings.ebay_app_id,
        config_file=None,
        siteid="EBAY-US",
        sandbox=settings.ebay_sandbox,
    )


async def get_valuation(request: ValuationRequest) -> ValuationResult:
    """Search eBay completed/sold listings to estimate resale value."""
    api = _get_finding_api()
    query = request.title
    if request.keywords:
        query += " " + " ".join(request.keywords[:3])

    response = api.execute(
        "findCompletedItems",
        {
            "keywords": query,
            "itemFilter": [
                {"name": "SoldItemsOnly", "value": "true"},
                {"name": "Condition", "value": request.condition or "Used"},
            ],
            "sortOrder": "EndTimeSoonest",
            "paginationInput": {"entriesPerPage": 20},
        },
    )

    items = response.reply.searchResult.item if hasattr(response.reply.searchResult, "item") else []
    prices = [float(i.sellingStatus.currentPrice.value) for i in items]

    if not prices:
        return ValuationResult(
            title=request.title,
            price_low=0.0,
            price_high=0.0,
            price_median=0.0,
            comparable_sold_count=0,
        )

    return ValuationResult(
        title=request.title,
        price_low=round(min(prices), 2),
        price_high=round(max(prices), 2),
        price_median=round(statistics.median(prices), 2),
        comparable_sold_count=len(prices),
    )


async def create_draft_listing(analysis: ImageAnalysisResult) -> ListingDraft:
    """Return a listing draft — full eBay AddItem integration wired here."""
    logger.info(f"Draft listing: {analysis.title} @ ${analysis.price_estimate_low}–${analysis.price_estimate_high}")
    # TODO: wire Trading API AddItem call with ebay_user_token
    return ListingDraft(
        analysis=analysis,
        ebay_listing_url=None,
        draft_id=None,
    )
