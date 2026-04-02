"""
myScheme.gov.in scraper — stub for future implementation.
myScheme lists government schemes for citizens across categories.
"""
import requests
from bs4 import BeautifulSoup
from utils.db import get_client, insert_article, article_exists, update_source_last_scraped
from utils.dedup import make_url_hash
from utils.normalise import clean_text, detect_category, detect_ministry, normalise_date

BASE_URL = "https://www.myscheme.gov.in"
SOURCE_NAME = "myScheme"


def scrape_myscheme():
    client = get_client()
    total_new = 0

    print(f"Scraping {SOURCE_NAME}...")
    # TODO: implement full scraper once site structure is confirmed
    # myScheme may require JS rendering — consider using requests-html or playwright
    print(f"{SOURCE_NAME} scraper not yet implemented.")

    update_source_last_scraped(client, SOURCE_NAME)
    print(f"{SOURCE_NAME} scrape done. {total_new} new articles.")
    return total_new
