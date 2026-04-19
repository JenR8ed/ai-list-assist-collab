import io
import pytest
from unittest.mock import AsyncMock, patch
from PIL import Image
from app.schemas.listing import ImageAnalysisResult

@pytest.fixture
def test_image_bytes():
    """Generate valid 1x1 pixel JPEG bytes for testing."""
    img = Image.new("RGB", (1, 1), color="red")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    return img_byte_arr.getvalue()

MOCK_ANALYSIS = ImageAnalysisResult(
    title="Mock Title",
    description="Mock Description",
    category="Mock Category",
    condition="Good",
    keywords=["mock", "test"],
    price_estimate_low=10.0,
    price_estimate_high=20.0,
    confidence=0.9,
    model_used="gemini-1.5-flash",
)

def test_analyze_image_success(client, test_image_bytes):
    files = {"file": ("test.jpg", io.BytesIO(test_image_bytes), "image/jpeg")}
    data = {"prompt": "test prompt"}

    with patch("app.api.images.analyze_image", new=AsyncMock(return_value=MOCK_ANALYSIS)):
        response = client.post("/api/images/analyze", files=files, data=data)

    assert response.status_code == 200
    assert response.json()["title"] == "Mock Title"

def test_analyze_image_unsupported_type(client):
    files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    response = client.post("/api/images/analyze", files=files)
    assert response.status_code == 415
    assert "Unsupported image type" in response.json()["detail"]

def test_analyze_image_large_size(client):
    # Construct a file larger than 10MB
    large_bytes = b"0" * (10 * 1024 * 1024 + 1)
    files = {"file": ("large.jpg", io.BytesIO(large_bytes), "image/jpeg")}
    response = client.post("/api/images/analyze", files=files)
    assert response.status_code == 413
    assert "Image exceeds 10MB limit" in response.json()["detail"]

def test_analyze_image_decode_error(client):
    # Valid content type but invalid image data
    invalid_bytes = b"corrupted image data"
    files = {"file": ("test.jpg", io.BytesIO(invalid_bytes), "image/jpeg")}
    response = client.post("/api/images/analyze", files=files)
    assert response.status_code == 422
    assert "Could not decode image" in response.json()["detail"]
