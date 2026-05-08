import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from crawler import fetch_page, collect_author_urls, get_author_pages, get_quote_pages, crawl

# ---- Shared HTML Fixtures ----

# A minimal fake HTML page with two quotes and a next button
FAKE_QUOTE_PAGE = """
<html>
<body>
    <div class="quote">
        <span class="text">The world is a book</span>
        <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">about</a>
    </div>
    <div class="quote">
        <span class="text">Life is good</span>
        <small class="author">Jane Austen</small>
        <a href="/author/Jane-Austen">about</a>
    </div>
    <nav>
        <ul class="pager">
            <li class="next"><a href="/page/2/">Next →</a></li>
        </ul>
    </nav>
</body>
</html>
"""

# A fake last page — no next button
FAKE_LAST_PAGE = """
<html>
<body>
    <div class="quote">
        <span class="text">Be yourself</span>
        <small class="author">Oscar Wilde</small>
        <a href="/author/Oscar-Wilde">about</a>
    </div>
</body>
</html>
"""

# A fake author page
FAKE_AUTHOR_PAGE = """
<html>
<body>
    <div class="author-details">
        <div class="author-description">
            A famous author born in Germany who loved physics.
        </div>
    </div>
</body>
</html>
"""


class TestFetchPage:

    @patch("crawler.requests.get")
    def test_successful_fetch(self, mock_get):
        """Test that fetch_page returns a BeautifulSoup object on success"""
        # Set up the mock to return a fake successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = FAKE_QUOTE_PAGE
        mock_response.raise_for_status = MagicMock()  # Does nothing
        mock_get.return_value = mock_response

        result = fetch_page("http://test.com")

        assert result is not None
        assert isinstance(result, BeautifulSoup)

    @patch("crawler.requests.get")
    def test_failed_fetch_returns_none(self, mock_get):
        """Test that fetch_page returns None on a failed request"""
        # Make requests.get raise an exception
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")

        result = fetch_page("http://test.com")

        assert result is None

    @patch("crawler.requests.get")
    def test_fetch_calls_correct_url(self, mock_get):
        """Test that fetch_page calls requests.get with the correct URL"""
        mock_response = MagicMock()
        mock_response.text = FAKE_QUOTE_PAGE
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        fetch_page("https://quotes.toscrape.com/")

        mock_get.assert_called_once_with(
            "https://quotes.toscrape.com/",
            timeout=10
        )


class TestCollectAuthorUrls:

    def test_extracts_correct_number_of_urls(self):
        """Test that correct number of author URLs are extracted"""
        soup = BeautifulSoup(FAKE_QUOTE_PAGE, "html.parser")
        urls = collect_author_urls(soup)
        # FAKE_QUOTE_PAGE has two quotes so should have two author URLs
        assert len(urls) == 2

    def test_extracts_correct_urls(self):
        """Test that correct full author URLs are extracted"""
        soup = BeautifulSoup(FAKE_QUOTE_PAGE, "html.parser")
        urls = collect_author_urls(soup)
        assert "https://quotes.toscrape.com/author/Albert-Einstein" in urls
        assert "https://quotes.toscrape.com/author/Jane-Austen" in urls

    def test_empty_page_returns_empty_list(self):
        """Test that a page with no quotes returns empty list"""
        empty_page = "<html><body></body></html>"
        soup = BeautifulSoup(empty_page, "html.parser")
        urls = collect_author_urls(soup)
        assert urls == []


class TestGetQuotePages:

    @patch("crawler.fetch_page")
    @patch("crawler.time.sleep")  # Mock sleep so tests don't wait 6 seconds!
    def test_stops_on_last_page(self, mock_sleep, mock_fetch):
        """Test that crawling stops when there is no next button"""
        # Return last page (no next button) on first call
        mock_fetch.return_value = BeautifulSoup(FAKE_LAST_PAGE, "html.parser")

        pages = get_quote_pages()

        assert len(pages) == 1  # Only one page crawled

    @patch("crawler.fetch_page")
    @patch("crawler.time.sleep")
    def test_follows_next_page_link(self, mock_sleep, mock_fetch):
        """Test that crawler follows next page links correctly"""
        # First call returns page with next button
        # Second call returns last page
        mock_fetch.side_effect = [
            BeautifulSoup(FAKE_QUOTE_PAGE, "html.parser"),
            BeautifulSoup(FAKE_LAST_PAGE, "html.parser")
        ]

        pages = get_quote_pages()

        assert len(pages) == 2  # Two pages crawled


    @patch("crawler.fetch_page")
    @patch("crawler.time.sleep")
    def test_handles_failed_fetch(self, mock_sleep, mock_fetch):
        """Test that crawler handles a failed page fetch gracefully"""
        mock_fetch.return_value = None  # Simulate failed fetch

        pages = get_quote_pages()

        assert pages == []