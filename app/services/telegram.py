"""Telegram bot service utilities shared with aiogram handlers."""
from loguru import logger


def escape_markdown(text: str) -> str:
    """Escape Markdown reserved characters: _, *, `, ["""
    if not text:
        return ""
    for char in ["_", "*", "`", "["]:
        text = text.replace(char, f"\\{char}")
    return text


async def send_listing_summary(bot, chat_id: int, analysis) -> None:
    """Format and send analysis result as a Telegram message."""
    title = escape_markdown(analysis.title)
    condition = escape_markdown(analysis.condition)
    category = escape_markdown(analysis.category)
    keywords = [escape_markdown(k) for k in analysis.keywords[:5]]
    model_used = escape_markdown(analysis.model_used)
    description = escape_markdown(analysis.description)

    msg = (
        f"🏷 *{title}*\n\n"
        f"📦 Condition: {condition}\n"
        f"🗂 Category: {category}\n"
        f"💰 Price estimate: ${analysis.price_estimate_low:.2f} – ${analysis.price_estimate_high:.2f}\n"
        f"🔑 Keywords: {', '.join(keywords)}\n"
        f"🤖 Model: `{model_used}`\n\n"
        f"📝 _{description}_"
    )
    await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
    logger.info(f"Sent listing summary to chat {chat_id}")
