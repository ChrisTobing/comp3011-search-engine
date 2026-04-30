import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://quotes.toscrape.com"
POLITENESS_WINDOW = 6  # seconds between requests


def fetch_page(url):
    """
    Fetches the HTML content of a given URL.
    
    Args:
        url (str): The URL to fetch
        
    Returns:
        BeautifulSoup object if successful, None if request fails
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_quote_pages():
    """
    Crawls all main paginated quote pages starting from BASE_URL.
    Follows 'Next' links until the last page is reached.
    
    Returns:
        A list of dicts: [{"url": ..., "content": ...}, ...]
    """
    pages = []
    current_url = BASE_URL

    while current_url:
        # TODO: Print which URL is being fetched (helpful for debugging)
        # TODO: Call fetch_page(current_url)
        # TODO: If fetch fails, break out of loop
        
        # TODO: Extract text content from this page
        #       Hint: look at quote divs and extract their text
        
        # TODO: Append {"url": current_url, "content": page_text} to pages
        
        # TODO: Look for the next page link
        #       Hint: soup.find("li", class_="next")
        #       If found, update current_url to BASE_URL + href
        #       If not found, set current_url to None (stops the loop)
        
        # TODO: Respect the politeness window — time.sleep(POLITENESS_WINDOW)
        pass

    return pages


def get_author_pages(author_urls):
    """
    Crawls each author page and extracts biography content.
    
    Args:
        author_urls (list): List of author page URLs to crawl
        
    Returns:
        A list of dicts: [{"url": ..., "content": ...}, ...]
    """
    pages = []

    for url in author_urls:
        # TODO: Call fetch_page(url)
        # TODO: If fetch fails, skip this author with continue
        
        # TODO: Extract the author description text
        #       Hint: soup.find("div", class_="author-description")
        
        # TODO: Append {"url": url, "content": description_text} to pages
        
        # TODO: Respect the politeness window
        pass

    return pages


def collect_author_urls(soup):
    """
    Extracts all author page URLs from a quote page.
    
    Args:
        soup (BeautifulSoup): Parsed HTML of a quote page
        
    Returns:
        A list of full author URLs (strings)
    """
    # TODO: Find all quote divs
    # TODO: Within each, find the author link <a> tag
    # TODO: Build the full URL using BASE_URL + href
    # TODO: Return the list of URLs
    pass


def crawl():
    """
    Main crawl function. Orchestrates the full crawl of the website.
    Crawls all quote pages, collects author URLs, then crawls author pages.
    
    Returns:
        A list of all page dicts [{"url": ..., "content": ...}, ...]
        representing every page crawled.
    """
    all_pages = []
    author_urls = []

    # TODO: Call get_quote_pages() and store results
    # TODO: As you crawl quote pages, collect author URLs using collect_author_urls()
    # TODO: Deduplicate author_urls (same author may appear multiple times)
    #       Hint: list(set(author_urls))
    # TODO: Call get_author_pages() with the deduplicated URLs
    # TODO: Combine quote pages and author pages into all_pages
    # TODO: Return all_pages
    pass