"""
linkedin_monitor.py
Attempts to check each competitor's LinkedIn company page for new posts.

IMPORTANT: LinkedIn actively blocks automated requests and requires a
logged-in session to view company page content at all. This script does
NOT silently skip LinkedIn - it makes a real attempt for every competitor
and reports exactly how the request failed, instead of pretending data
was collected. See README.md "Known Limitations".
"""

import requests

# Best-effort LinkedIn company page URLs (not all independently confirmed,
# since LinkedIn requires login to verify a page exists).
LINKEDIN_PAGES = {
    "Morph Electric": "https://www.linkedin.com/company/morph-electric/",
    "GoGoA1": "https://www.linkedin.com/company/gogoa1/",
    "Indofast Energy": "https://www.linkedin.com/company/indofast-energy/",
    "Astrix EV": "https://www.linkedin.com/company/astrixev/",
    "RACEnergy": "https://www.linkedin.com/company/racenergy/",
    "Austin EV Retrofit": "Not found - no LinkedIn company page identified",
    "e-Vidyut": "https://www.linkedin.com/company/eevv/",
    "ETrio": "https://www.linkedin.com/company/e-trio-automobiles/",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def check_linkedin_page(url):
    """Attempt to fetch a LinkedIn company page and report what actually happened."""
    if not url.startswith("http"):
        return "NO_URL_AVAILABLE"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # LinkedIn shows a login wall to logged-out requests, usually via
        # a 403/999 status or a redirect to the login page.
        if response.status_code in (403, 999):
            return f"BLOCKED (HTTP {response.status_code} - LinkedIn requires login)"
        elif "login" in response.url.lower():
            return "BLOCKED (redirected to LinkedIn login page)"
        else:
            return f"UNEXPECTED_RESPONSE (HTTP {response.status_code}) - manual check needed"
    except requests.exceptions.RequestException as e:
        return f"REQUEST_FAILED ({e})"


def check_all_linkedin_pages():
    """Attempt the LinkedIn check for every competitor. Returns {name: status}."""
    results = {}
    for name, url in LINKEDIN_PAGES.items():
        print(f"Checking LinkedIn for: {name}")
        results[name] = check_linkedin_page(url)
    return results


if __name__ == "__main__":
    data = check_all_linkedin_pages()
    for company, status in data.items():
        print(f"{company}: {status}")