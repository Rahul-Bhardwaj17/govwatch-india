"""
Optional Telegram alert bot.
Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in .env to enable.
"""
import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHANNEL_ID")  # e.g. @govwatch_india


def send_alert(article: dict):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHANNEL:
        return
    text = (
        f"*{article['category']} | {article['state']}*\n\n"
        f"{article['title']}\n\n"
        f"_{article['source_name']}_\n"
        f"[Read more]({article['source_url']})"
    )
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHANNEL,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }
    )
