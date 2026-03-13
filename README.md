# AI List Assist

> **Generative AI multimodal eBay listing assistant** — snap a photo, get a complete, SEO-optimized eBay listing in seconds.

[![CI](https://github.com/JenR8ed/ai-list-assist-collab/actions/workflows/ci.yml/badge.svg)](https://github.com/JenR8ed/ai-list-assist-collab/actions/workflows/ci.yml)

## How It Works

1. 📸 **Upload a product image** (API endpoint or Telegram bot)
2. 🤖 **Gemini 1.5 Flash** analyzes the image → returns structured JSON (title, description, category, condition, keywords, price range)
3. 💰 **eBay Finding API** cross-references sold comps to validate/refine the price estimate
4. 📋 **Draft listing** is returned ready to post to eBay
5. 💬 **Telegram bot** delivers results directly in chat

## Stack

| Layer | Tech |
|---|---|
| Vision (primary) | Google Gemini 1.5 Flash |
| Vision (offline fallback) | Ollama LLaVA 7B (local) |
| Backend API | FastAPI + Uvicorn + Pydantic v2 |
| eBay integration | `ebaysdk` Finding + Trading API |
| Telegram bot | `aiogram` v3 |
| Image processing | Pillow, OpenCV, rembg, imagehash |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Cache | Redis 7 |
| Container | Docker + docker-compose |
| CI | GitHub Actions (ruff + pytest) |

## Quick Start

### 1. Clone & configure

```bash
git clone git@github.com:JenR8ed/ai-list-assist-collab.git
cd ai-list-assist-collab
cp .env.example .env
# Fill in GOOGLE_API_KEY, EBAY_APP_ID, TELEGRAM_BOT_TOKEN
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

API available at `http://localhost:8000`  
Swagger UI at `http://localhost:8000/docs`

### 3. Run locally (dev)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

### 4. Start the Telegram bot

```bash
python bot/telegram_bot.py
```

### 5. Pull the local LLaVA model (offline fallback)

```bash
docker compose up ollama -d
docker exec -it <ollama-container> ollama pull llava:7b
# or if running Ollama natively:
ollama pull llava:7b
```

## API Reference

### `POST /api/images/analyze`
Upload a product image → returns full `ImageAnalysisResult`.

```bash
curl -X POST http://localhost:8000/api/images/analyze \
  -F "file=@product.jpg" \
  -F "prompt=1980s Barbie doll, original box"
```

### `POST /api/valuation/estimate`
Get eBay sold-comps price estimate.

```bash
curl -X POST http://localhost:8000/api/valuation/estimate \
  -H "Content-Type: application/json" \
  -d '{"title": "Daisy Red Ryder BB Gun", "condition": "Good"}'
```

### `POST /api/listings/draft`
Convert an analysis result into an eBay listing draft.

## Project Structure

```
ai-list-assist-collab/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── api/                 # Route handlers
│   ├── services/            # Vision, eBay, Telegram logic
│   ├── schemas/             # Pydantic models
│   └── core/config.py       # Settings
├── bot/telegram_bot.py      # Aiogram Telegram bot
├── tests/                   # pytest suite
├── .github/workflows/ci.yml # Lint + test CI
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## Roadmap

- [ ] Image deduplication (imagehash)
- [ ] Background removal (rembg) before analysis
- [ ] eBay Trading API AddItem (live listing creation)
- [ ] Multi-image support per listing
- [ ] React frontend
- [ ] Fine-tuned Gemini model on eBay listing dataset
- [ ] Bulk listing mode (CSV upload)
