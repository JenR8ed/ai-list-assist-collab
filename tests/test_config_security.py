import os
import unittest.mock
import pytest
import secrets
from pydantic import ValidationError
from app.core.config import Settings

def test_secret_key_default_is_random():
    """Verify that a random secret key is generated if not provided."""
    with unittest.mock.patch.dict(os.environ, {}, clear=True):
        settings1 = Settings(_env_file=None)
        settings2 = Settings(_env_file=None)

    assert settings1.secret_key is not None
    assert len(settings1.secret_key) == 64  # hex string from 32 bytes
    assert settings1.secret_key != settings2.secret_key

def test_secret_key_rejects_changeme():
    """Verify that 'changeme' is rejected by the validator."""
    with unittest.mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValidationError) as excinfo:
            Settings(secret_key="changeme", _env_file=None)
    assert "Insecure SECRET_KEY detected" in str(excinfo.value)

def test_secret_key_accepts_custom_value():
    """Verify that a custom secure key can be provided."""
    with unittest.mock.patch.dict(os.environ, {}, clear=True):
        custom_key = secrets.token_hex(32)
        settings = Settings(secret_key=custom_key, _env_file=None)
    assert settings.secret_key == custom_key
