import requests
from bs4 import BeautifulSoup, soup
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
        print(f"Successfully fetched {url}")
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
        print(f"Crawling {current_url}...")
        soup = fetch_page(current_url)
        if not soup:
            break

        quotes = soup.find_all("div", class_="quote")
        page_text = " ".join(quote.get_text(strip=True) for quote in quotes)
        pages.append({"url": current_url, "content": page_text})
        
        # Look for the next page link
        next_link = soup.find("li", class_="next")

        if next_link and next_link.a:
            next_url = next_link.a['href']
            current_url = BASE_URL + next_url
        else:
            current_url = None  # No more pages to crawl

        time.sleep(POLITENESS_WINDOW)
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
        soup = fetch_page(url)

        if not soup:
            continue  # Skip this author if fetch fails
        else:
            description = soup.find("div", class_="author-description")

            pages.append({"url": url, "content": description.get_text(strip=True) if description else ""})
        
        time.sleep(POLITENESS_WINDOW)
    return pages


def collect_author_urls(soup):
    """
    Extracts all author page URLs from a quote page.
    
    Args:
        soup (BeautifulSoup): Parsed HTML of a quote page
        
    Returns:
        A list of full author URLs (strings)
    """
    quotes = soup.find_all("div", class_="quote")
    author_urls = []

    for quote in quotes:
        author_class = quote.find("small", class_="author")
        author_url = author_class.find_next_sibling("a") if author_class else None
        if author_url and 'href' in author_url.attrs:
            full_url = BASE_URL + author_url['href']
            author_urls.append(full_url)
    
    return author_urls


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