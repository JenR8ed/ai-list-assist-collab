import os
import unittest.mock
from app.core.config import Settings

def test_settings_debug_mode_is_false_by_default():
    # Use unittest.mock.patch.dict to ensure default_factory values and defaults are triggered
    # instead of host env variables overriding them
    with unittest.mock.patch.dict(os.environ, {}, clear=True):
        settings = Settings(_env_file=None)
        assert settings.debug is False
