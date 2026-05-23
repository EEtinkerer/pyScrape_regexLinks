
from linkregex import convert_url_to_regex


def test_basic_url():
    result = convert_url_to_regex(
        "https://example.com/products/widget-123.html"
    )

    assert "example\\.com" in result
