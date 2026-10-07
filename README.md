# ReVithalize Competitor Monitor

Task 4 — Python Scraper — Competitor Web & Pricing Monitor
Competitor Intelligence Sprint | Ref. RMPL/FOF/CI/2026/SRINIDHI/01

## What this does
Checks all 8 competitors weekly for:
1. Website/product-page changes (text-hash comparison between runs)
2. New Google News mentions (via public RSS feed)
3. IndiaMART listing changes, for the 2 competitors listed there
4. LinkedIn company page posts (attempted; see Known Limitations)

## Folder structure
- `scraper/` — all Python scripts (news_monitor.py, website_monitor.py,
  indiamart_monitor.py, linkedin_monitor.py, run_all.py)
- `output/` — generated reports and state files (gitignored; created
  automatically the first time you run the scraper)

## How to run

Run this weekly. The first run captures a baseline (nothing to compare
yet); from the second run onward, changed pages are flagged.

## Known Limitations
- **LinkedIn blocks automated access entirely.** It requires a logged-in
  session to view company page content, so `linkedin_monitor.py` cannot
  retrieve real posts - every competitor reports BLOCKED. This is a
  platform restriction, not a bug; a future version would need an
  authenticated LinkedIn API integration (official LinkedIn API access,
  which requires partner approval) to do this properly.
- **Astrix EV's website** returned limited/blocked content during prior
  research (robots.txt restrictions) and may show as FAILED_TO_FETCH.
- **RACEnergy's website** (racenergy.in) was found in Task 1 research to
  be a "Launching Soon" placeholder, not a real product site - its
  hash may simply never change.
- **Austin EV Retrofit** has no official website, only an IndiaMART
  listing, so it's excluded from `website_monitor.py` and only checked
  via `indiamart_monitor.py`.
- **Change detection is whole-page-text based**, not field-specific - a
  "CHANGED" result means *something* on the page changed (could be a
  price, or could be an unrelated banner/date), so flagged pages should
  be manually reviewed rather than trusted automatically.
- Not scheduled automatically in this version - run manually, or set up
  Windows Task Scheduler to run `python scraper/run_all.py` weekly.
  