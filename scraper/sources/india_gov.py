"""
india.gov.in news scraper.
Scrapes the latest news section from the National Portal of India.
"""
import requests
from bs4 import BeautifulSoup
from utils.db import get_client, insert_article, article_exists, update_source_last_scraped
from utils.dedup import make_url_hash
from utils.normalise import clean_text, detect_category, detect_ministry, normalise_date

BASE_URL = "https://www.india.gov.in"
NEWS_URL = "https://www.india.gov.in/news"
SOURCE_NAME = "India.gov.in"


def scrape_india_gov():
    client = get_client()
    total_new = 0

    print(f"Scraping {SOURCE_NAME}...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; GovWatchBot/1.0)"}
        response = requests.get(NEWS_URL, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Adjust selector based on actual site structure
        news_items = soup.select("div.news-item, li.news-list-item, article")

        for item in news_items:
            link_tag = item.find("a", href=True)
            if not link_tag:
                continue

            href = link_tag["href"]
            url = href if href.startswith("http") else BASE_URL + href
            url_hash = make_url_hash(url)

            if article_exists(client, url_hash):
                continue

            title = clean_text(link_tag.get_text())
            if not title:
                continue

            date_tag = item.find("span", class_="date") or item.find("time")
            published = normalise_date(date_tag.get_text() if date_tag else "")

            article = {
                "title": title,
                "summary": None,
                "source_url": url,
                "source_name": SOURCE_NAME,
                "url_hash": url_hash,
                "language": "en",
                "ministry": detect_ministry(title),
                "category": detect_category(title),
                "state": "Central",
                "published_at": published,
                "tags": []
            }

            if insert_article(client, article):
                total_new += 1
                print(f"  + {title[:60]}...")

    except Exception as e:
        print(f"  ERROR scraping {SOURCE_NAME}: {e}")

    update_source_last_scraped(client, SOURCE_NAME)
    print(f"{SOURCE_NAME} scrape done. {total_new} new articles.")
    return total_new
