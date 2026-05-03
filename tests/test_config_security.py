import os
import pytest
from pydantic import ValidationError
from unittest.mock import patch
from app.core.config import Settings

def test_default_secret_key_is_secure():
    # Ensure no env var is overriding
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings(_env_file=None)
        assert settings.secret_key != "changeme"
        assert len(settings.secret_key) == 64  # 32 bytes hex encoded is 64 chars

def test_secret_key_cannot_be_changeme():
    with patch.dict(os.environ, {"SECRET_KEY": "changeme"}, clear=True):
        with pytest.raises(ValidationError) as exc_info:
            Settings(_env_file=None)
        assert "secret_key cannot be 'changeme'" in str(exc_info.value)
