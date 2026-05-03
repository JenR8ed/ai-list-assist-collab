"""Tests for images API."""

def test_analyze_image_unsupported_type(client):
    """Should return 415 when uploading an unsupported file type."""
    response = client.post(
        "/api/images/analyze",
        files={"file": ("test.pdf", b"dummy pdf content", "application/pdf")},
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Unsupported image type: application/pdf"
