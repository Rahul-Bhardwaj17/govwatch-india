import re
from datetime import datetime, timezone

MINISTRY_KEYWORDS = {
    "finance": "Ministry of Finance",
    "education": "Ministry of Education",
    "health": "Ministry of Health",
    "agriculture": "Ministry of Agriculture",
    "defence": "Ministry of Defence",
    "home": "Ministry of Home Affairs",
    "external affairs": "Ministry of External Affairs",
    "railway": "Ministry of Railways",
    "road transport": "Ministry of Road Transport",
    "environment": "Ministry of Environment",
    "women": "Ministry of Women and Child Development",
    "tribal": "Ministry of Tribal Affairs",
}

CATEGORY_KEYWORDS = {
    "scheme": "Scheme",
    "yojana": "Scheme",
    "award": "Award",
    "tender": "Tender",
    "result": "Result",
    "exam": "Exam",
    "notification": "Notification",
    "circular": "Circular",
    "policy": "Policy",
    "budget": "Budget",
    "launch": "Launch",
}


def detect_ministry(text: str) -> str:
    text_lower = text.lower()
    for keyword, ministry in MINISTRY_KEYWORDS.items():
        if keyword in text_lower:
            return ministry
    return "Government of India"


def detect_category(text: str) -> str:
    text_lower = text.lower()
    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in text_lower:
            return category
    return "General"


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def normalise_date(date_str: str) -> str:
    """Try to parse various date formats and return ISO string."""
    if not date_str:
        return datetime.now(timezone.utc).isoformat()
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        return dt.isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()
