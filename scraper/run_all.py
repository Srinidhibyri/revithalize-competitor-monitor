"""
run_all.py
Main entry point for the weekly competitor monitor. Runs all four checks
(news, website, IndiaMART, LinkedIn) and saves one combined, timestamped
JSON report to output/.

Run this weekly: python scraper/run_all.py   (from the project root folder)
"""

import json
import os
from datetime import datetime

import news_monitor
import website_monitor
import indiamart_monitor
import linkedin_monitor


def run_full_check():
    """Run all four monitoring checks and combine results into one dict."""
    print("=== Starting weekly competitor monitor run ===\n")
    report = {
        "run_timestamp": datetime.now().isoformat(),
        "news_mentions": news_monitor.check_all_competitors(),
        "website_changes": website_monitor.check_all_websites(),
        "indiamart_changes": indiamart_monitor.check_all_listings(),
        "linkedin_checks": linkedin_monitor.check_all_linkedin_pages(),
    }
    return report


def save_report(report):
    """Save the combined report as a timestamped JSON file in output/."""
    os.makedirs("output", exist_ok=True)
    filename = f"output/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved to: {filename}")


if __name__ == "__main__":
    full_report = run_full_check()
    save_report(full_report)
    print("\n=== Run complete ===")