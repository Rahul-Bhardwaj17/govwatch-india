import hashlib


def make_url_hash(url: str) -> str:
    """SHA-256 hash of normalised URL for deduplication."""
    normalised = url.strip().lower().rstrip("/")
    return hashlib.sha256(normalised.encode()).hexdigest()


def make_content_hash(title: str, summary: str = "") -> str:
    """Hash of title+summary to catch near-duplicates with different URLs."""
    content = (title.strip() + summary.strip()).lower()
    return hashlib.sha256(content.encode()).hexdigest()
