import sys
import os

# Since main.py is inside src/, crawler.py is in the same directory
sys.path.insert(0, os.path.dirname(__file__))

from crawler import fetch_page, get_quote_pages, collect_author_urls, crawl
from indexer import build_index, save_index, load_index
if __name__ == "__main__":
    # Comment/uncomment tests as you build each function
    
    # fetch_page("http://quotes.toscrape.com/")  # test_fetch_page()
    # test_collect_author_urls()
    # test_get_quote_pages()
    pages = crawl()
    index = build_index(pages)
    print(index)
