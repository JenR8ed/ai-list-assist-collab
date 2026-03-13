"""AI List Assist — Telegram bot (aiogram v3).
Send a product photo → receive a full eBay listing draft.
"""
import asyncio
import io
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, PhotoSize
from loguru import logger
from PIL import Image

from app.core.config import settings
from app.services.vision import analyze_image
from app.services.telegram import send_listing_summary

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Welcome to *AI List Assist*!\n\n"
        "📸 Send me a photo of any item and I'll generate a complete eBay listing for you.\n"
        "Include a caption with extra details (brand, model, condition) for better results.",
        parse_mode="Markdown",
    )


@dp.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("🔍 Analyzing your image... hang tight!")

    photo: PhotoSize = message.photo[-1]  # largest resolution
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)

    img = Image.open(io.BytesIO(file_bytes.read())).convert("RGB")
    prompt = message.caption or None

    try:
        analysis = await analyze_image(img, prompt=prompt)
        await send_listing_summary(bot, message.chat.id, analysis)
    except Exception as e:
        logger.error(f"Bot analysis failed: {e}")
        await message.answer(f"❌ Analysis failed: {e}")


@dp.message()
async def handle_other(message: Message):
    await message.answer("📸 Please send a product photo to generate a listing.")


async def main():
    logger.info("🤖 AI List Assist bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
