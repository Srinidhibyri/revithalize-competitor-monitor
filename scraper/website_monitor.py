"""
website_monitor.py
Checks each competitor's official website for changes by fetching the page,
hashing its text, and comparing that hash to the one saved last run.
A different hash = the page content changed since the last check.
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os

# Competitor websites. Some of these were found in earlier research to be
# JavaScript-rendered or to block automated access - they're still included
# so the scraper attempts them and reports the real failure (see README).
WEBSITES = {
    "Morph Electric": "https://www.morphelectric.com/scooter-conversion",
    "GoGoA1": "https://gogoa1.com/",
    "Indofast Energy": "https://www.indofastenergy.com/retrofit",
    "Astrix EV": "https://www.astrixev.com/",
    "RACEnergy": "https://racenergy.in/",
    "e-Vidyut": "https://evidyut.in/",
    "ETrio": "https://www.etrio.in/",
    # Austin EV Retrofit has no official website - see indiamart_monitor.py instead.
}

STATE_FILE = "output/website_state.json"  # stores last-seen hash per site
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}  # some sites block requests with no browser-like header


def fetch_page_text(url):
    """Download a page and return its visible text, or None if the request fails."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # raises an error on 4xx/5xx responses
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except requests.exceptions.RequestException as e:
        print(f"  Could not fetch {url}: {e}")
        return None


def hash_text(text):
    """Return a short fingerprint of a text string, used to detect changes cheaply."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_state():
    """Load previously saved hashes, or an empty dict on the very first run."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    """Save current hashes so the next run has something to compare against."""
    os.makedirs("output", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def check_all_websites():
    """Check every competitor website for changes. Returns {name: {status, url}}."""
    previous_state = load_state()
    new_state = {}
    results = {}

    for name, url in WEBSITES.items():
        print(f"Checking website: {name}")
        text = fetch_page_text(url)

        if text is None:
            results[name] = {"status": "FAILED_TO_FETCH", "url": url}
            continue

        current_hash = hash_text(text)
        new_state[name] = current_hash
        previous_hash = previous_state.get(name)

        if previous_hash is None:
            results[name] = {"status": "BASELINE_CAPTURED (first run, nothing to compare yet)", "url": url}
        elif previous_hash != current_hash:
            results[name] = {"status": "CHANGED since last check", "url": url}
        else:
            results[name] = {"status": "NO_CHANGE", "url": url}

    save_state(new_state)
    return results


if __name__ == "__main__":
    data = check_all_websites()
    for company, result in data.items():
        print(f"{company}: {result['status']}")