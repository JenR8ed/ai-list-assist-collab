"""Telegram bot service utilities shared with aiogram handlers."""
from loguru import logger


async def send_listing_summary(bot, chat_id: int, analysis) -> None:
    """Format and send analysis result as a Telegram message."""
    msg = (
        f"🏷 *{analysis.title}*\n\n"
        f"📦 Condition: {analysis.condition}\n"
        f"🗂 Category: {analysis.category}\n"
        f"💰 Price estimate: ${analysis.price_estimate_low:.2f} – ${analysis.price_estimate_high:.2f}\n"
        f"🔑 Keywords: {', '.join(analysis.keywords[:5])}\n"
        f"🤖 Model: `{analysis.model_used}`\n\n"
        f"📝 _{analysis.description}_"
    )
    await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
    logger.info(f"Sent listing summary to chat {chat_id}")
