"""
news_monitor.py
Checks Google News RSS for new press mentions of each competitor.
This is the easiest data source: Google News publishes a public,
structured RSS (XML) feed - no HTML page-scraping or login needed.
"""

import feedparser

# The 8 competitors from Task 1/2 research.
COMPETITORS = [
    "Morph Electric",
    "GoGoA1",
    "Indofast Energy",
    "Astrix EV",
    "RACEnergy",
    "Austin EV Retrofit",
    "e-Vidyut",
    "ETrio",
]


def build_rss_url(company_name):
    """Build a Google News RSS search URL for a given company name."""
    query = company_name.replace(" ", "+")  # URLs can't contain spaces
    return f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"


def get_latest_articles(company_name, limit=5):
    """Fetch the most recent news articles for one competitor as a list of dicts."""
    url = build_rss_url(company_name)
    feed = feedparser.parse(url)  # handles the HTTP request + XML parsing in one step

    articles = []
    for entry in feed.entries[:limit]:  # feed.entries is newest-first
        articles.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", "Unknown date"),
        })
    return articles


def check_all_competitors():
    """Run the news check for every competitor. Returns {name: [articles]}."""
    results = {}
    for name in COMPETITORS:
        print(f"Checking news for: {name}")
        results[name] = get_latest_articles(name)
    return results


# Only runs when this file is executed directly, not when imported by run_all.py
if __name__ == "__main__":
    data = check_all_competitors()
    for company, articles in data.items():
        print(f"\n{company}:")
        for a in articles:
            print(f"  - {a['title']} ({a['published']})")