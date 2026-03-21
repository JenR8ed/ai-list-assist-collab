from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_analyze_image_invalid_type():
    # Create a dummy text file to simulate an invalid image type
    file_content = b"This is not an image."

    response = client.post(
        "/api/images/analyze",
        files={"file": ("test.txt", file_content, "text/plain")},
        data={"prompt": "Describe this item"}
    )

    assert response.status_code == 415
    assert response.json() == {"detail": "Unsupported image type: text/plain"}


def test_analyze_image_too_large():
    # 10MB + 1 byte
    large_content = b"0" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/api/images/analyze",
        files={"file": ("large.jpg", large_content, "image/jpeg")},
        data={"prompt": "Describe this item"}
    )

    assert response.status_code == 413
    assert response.json() == {"detail": "Image exceeds 10MB limit"}
