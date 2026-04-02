#!/usr/bin/env python3
"""
GovWatch scraper entry point.
Run: python main.py
Or triggered by GitHub Actions cron.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sources.pib import scrape_pib
# Uncomment as you build them:
# from sources.myscheme import scrape_myscheme
# from sources.india_gov import scrape_india_gov


def run_all():
    print("=" * 50)
    print("GovWatch Scraper Starting...")
    print("=" * 50)

    results = {}
    results["pib"] = scrape_pib()
    # results["myscheme"] = scrape_myscheme()
    # results["india_gov"] = scrape_india_gov()

    print("\nScrape Summary:")
    for source, count in results.items():
        print(f"  {source}: {count} new articles")
    print("=" * 50)


if __name__ == "__main__":
    run_all()
