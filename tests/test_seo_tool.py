from tools import seo_tool

def test_fetch_page_returns_soup():
    url = "https://example.com"
    soup = seo_tool.fetch_page(url)
    assert soup is not None
    assert hasattr(soup, "find")
