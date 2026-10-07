"""
indiamart_monitor.py
Checks IndiaMART listing pages for the 2 competitors who are actually
listed there (GoGoA1, Austin EV Retrofit), using the same page-hashing
approach as website_monitor.py, since IndiaMART's page structure is
complex and can change without notice - hashing the whole visible text
is simpler and more robust than trying to isolate just the price.
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os

INDIAMART_LISTINGS = {
    "GoGoA1": "https://www.indiamart.com/gogoa1/",
    "Austin EV Retrofit": "https://www.indiamart.com/austin-ev-retrofit-hyderabad/",
}

STATE_FILE = "output/indiamart_state.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_page_text(url):
    """Download a page and return its visible text, or None if the request fails."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except requests.exceptions.RequestException as e:
        print(f"  Could not fetch {url}: {e}")
        return None


def hash_text(text):
    """Return a short fingerprint of the text, used to detect any change cheaply."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_state():
    """Load previously saved listing hashes, or an empty dict on first run."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    """Save current listing hashes so the next run can compare against them."""
    os.makedirs("output", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def check_all_listings():
    """Check every IndiaMART listing for changes. Returns {name: {status, url}}."""
    previous_state = load_state()
    new_state = {}
    results = {}

    for name, url in INDIAMART_LISTINGS.items():
        print(f"Checking IndiaMART listing: {name}")
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
            results[name] = {"status": "CHANGED since last check (verify price manually)", "url": url}
        else:
            results[name] = {"status": "NO_CHANGE", "url": url}

    save_state(new_state)
    return results


if __name__ == "__main__":
    data = check_all_listings()
    for company, result in data.items():
        print(f"{company}: {result['status']}")