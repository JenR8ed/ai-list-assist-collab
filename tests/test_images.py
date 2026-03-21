from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_analyze_image_sanitizes_filename():
    malicious_filename = "test\nfile\rname.jpg"
    with patch("app.api.images.logger.info") as mock_logger, \
         patch("app.api.images.analyze_image") as mock_analyze:
        mock_analyze.return_value = {
            "title": "Test Title",
            "description": "Test Desc",
            "category": "Test Cat",
            "condition": "New",
            "keywords": ["test"],
            "price_estimate_low": 10,
            "price_estimate_high": 20,
            "confidence": 0.9,
            "model_used": "gemini"
        }

        # Valid image content
        # creating a dummy 1x1 image
        import io
        from PIL import Image
        img = Image.new('RGB', (1, 1))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        response = client.post(
            "/api/images/analyze",
            files={"file": (malicious_filename, img_byte_arr, "image/jpeg")},
            data={"prompt": ""}
        )

        assert response.status_code == 200
        # Check that the logger was called and no newlines/returns were in the logged filename
        mock_logger.assert_called_once()
        log_message = mock_logger.call_args[0][0]
        assert "testfilename.jpg" in log_message
        assert "\n" not in log_message
        assert "\r" not in log_message

def test_analyze_image_decode_error_generic_response():
    with patch("app.api.images.logger.error") as mock_logger_error:
        response = client.post(
            "/api/images/analyze",
            files={"file": ("test.jpg", b"not a real image", "image/jpeg")},
            data={"prompt": ""}
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Could not decode image"}
        # Ensure the actual error was logged
        mock_logger_error.assert_called_once()
        log_message = mock_logger_error.call_args[0][0]
        assert "Could not decode image:" in log_message
