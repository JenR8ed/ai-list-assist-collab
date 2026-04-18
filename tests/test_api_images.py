"""Tests for image API endpoints."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_analyze_image_invalid_image_data():
    """Verify that uploading a file with valid extension but invalid image data returns 422."""
    # Send a request with a valid content type (image/jpeg) but invalid binary data
    response = client.post(
        "/api/images/analyze",
        files={"file": ("test.jpg", b"not a real image", "image/jpeg")},
        data={"prompt": "test prompt"}
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Could not decode image. Please ensure you are uploading a valid image file."
