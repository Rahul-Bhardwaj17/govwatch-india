import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)


def insert_article(client: Client, article: dict) -> bool:
    """Insert article, return True if new, False if duplicate."""
    try:
        client.table("articles").insert(article).execute()
        return True
    except Exception as e:
        if "duplicate" in str(e).lower():
            return False
        raise e


def article_exists(client: Client, url_hash: str) -> bool:
    result = client.table("articles").select("id").eq("url_hash", url_hash).execute()
    return len(result.data) > 0


def update_source_last_scraped(client: Client, source_name: str):
    from datetime import datetime, timezone
    client.table("sources").update({
        "last_scraped_at": datetime.now(timezone.utc).isoformat()
    }).eq("name", source_name).execute()
