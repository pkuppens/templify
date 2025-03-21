"""
Tests for utility functions
"""
from templify.utils import is_placeholder, extract_placeholder_value


def test_is_placeholder():
    """Test placeholder detection"""
    assert is_placeholder("{user.name}")
    assert is_placeholder("{{ products | jmespath('max_by(@, &sales).name') }}")
    assert not is_placeholder("regular text")
    assert not is_placeholder("{unclosed")
    assert not is_placeholder("unopened}")


def test_extract_placeholder_value():
    """Test placeholder value extraction"""
    assert extract_placeholder_value("{user.name}") == "user.name"
    assert (
        extract_placeholder_value("{{ products | jmespath('max_by(@, &sales).name') }}")
        == "products | jmespath('max_by(@, &sales).name')"
    )
    assert extract_placeholder_value("regular text") == "regular text"
