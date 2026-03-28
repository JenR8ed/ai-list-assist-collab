import sys
from unittest.mock import MagicMock

# Mock loguru to allow importing the service without the dependency
sys.modules["loguru"] = MagicMock()

from app.services.telegram import escape_markdown  # noqa: E402

def test_escape_markdown_basic():
    """Verify basic character escaping."""
    assert escape_markdown("hello_world") == r"hello\_world"
    assert escape_markdown("hello*world") == r"hello\*world"
    assert escape_markdown("hello`world") == r"hello\`world"
    assert escape_markdown("hello[world") == r"hello\[world"

def test_escape_markdown_combined():
    """Verify combined character escaping."""
    assert escape_markdown("_[*`") == r"\_\[\* \`".replace(" ", "")

def test_escape_markdown_none_or_empty():
    """Verify handling of None or empty strings."""
    assert escape_markdown("") == ""
    assert escape_markdown(None) == ""

def test_escape_markdown_injection_prevention():
    """Verify it prevents markdown formatting injection."""
    title = "Awesome * Item"
    escaped_title = escape_markdown(title)
    assert escaped_title == r"Awesome \* Item"

    msg = f"*{escaped_title}*"
    assert msg == r"*Awesome \* Item*"
