FROM python:3.12-slim

LABEL org.opencontainers.image.title="ai-list-assist"
LABEL org.opencontainers.image.description="Generative AI multimodal eBay listing assistant"
LABEL org.opencontainers.image.source="https://github.com/JenR8ed/ai-list-assist-collab"

WORKDIR /app

# System deps for OpenCV, pytesseract, rembg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1 \
    tesseract-ocr tesseract-ocr-eng \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
