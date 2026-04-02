import feedparser
import requests
from utils.db import get_client, insert_article, article_exists, update_source_last_scraped
from utils.dedup import make_url_hash
from utils.normalise import detect_ministry, detect_category, clean_text, normalise_date

PIB_RSS_FEEDS = [
    {
        "url": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
        "language": "en",
        "source_name": "PIB"
    },
]


def scrape_pib():
    client = get_client()
    total_new = 0

    for feed_config in PIB_RSS_FEEDS:
        print(f"Scraping {feed_config['source_name']}...")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
            response = requests.get(feed_config["url"], headers=headers, timeout=15, allow_redirects=True)
            print(f"  Final URL: {response.url}")
            print(f"  HTTP status: {response.status_code}")
            feed = feedparser.parse(response.content)
        except Exception as e:
            print(f"  ERROR fetching feed: {e}")
            continue

        print(f"  Entries found: {len(feed.entries)}")
        if feed.bozo:
            print(f"  Feed parse warning: {feed.bozo_exception}")

        for entry in feed.entries:
            url = entry.get("link", "")
            if not url:
                continue

            url_hash = make_url_hash(url)

            if article_exists(client, url_hash):
                continue

            title = clean_text(entry.get("title", ""))
            summary = clean_text(entry.get("summary", ""))
            published = normalise_date(entry.get("published", ""))

            article = {
                "title": title,
                "summary": summary[:500] if summary else None,
                "source_url": url,
                "source_name": feed_config["source_name"],
                "url_hash": url_hash,
                "language": feed_config["language"],
                "ministry": detect_ministry(title + " " + summary),
                "category": detect_category(title + " " + summary),
                "state": "Central",
                "published_at": published,
                "tags": []
            }

            if insert_article(client, article):
                total_new += 1
                print(f"  + {title[:60]}...")

        update_source_last_scraped(client, feed_config["source_name"])

    print(f"PIB scrape done. {total_new} new articles.")
    return total_new
