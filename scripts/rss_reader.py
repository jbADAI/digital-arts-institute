#!/usr/bin/env python3
"""
scripts/rss_reader.py

Reads curated RSS feeds, filters entries against the A(DAI) digital arts
keyword taxonomy, and writes matching signals to /inbox/ as markdown files.

Idempotent: tracks processed URLs in config/.rss-processed so re-runs
never duplicate inbox entries.

Usage:
    python scripts/rss_reader.py
    python scripts/rss_reader.py --dry-run       # preview matches, no writes
    python scripts/rss_reader.py --tier 1        # tier-1 feeds only
    python scripts/rss_reader.py --reset         # clear processed log (re-scan all)
"""

import os
import re
import sys
import yaml
import hashlib
import argparse
import feedparser
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser


# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT           = Path(__file__).parent.parent
INBOX          = ROOT / "inbox"
CONFIG         = ROOT / "config"
FEEDS_FILE     = CONFIG / "rss-feeds.yaml"
FILTERS_FILE   = CONFIG / "keyword-filters.yaml"
PROCESSED_FILE = CONFIG / ".rss-processed"

INBOX.mkdir(exist_ok=True)


# ── HTML stripping ─────────────────────────────────────────────────────────────
class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, d):
        self._parts.append(d)

    def get_text(self):
        return " ".join(self._parts)


def strip_html(html: str) -> str:
    s = _HTMLStripper()
    try:
        s.feed(html or "")
    except Exception:
        pass
    return " ".join(s.get_text().split())  # collapse whitespace


# ── Config loading ─────────────────────────────────────────────────────────────
def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_processed() -> set:
    if not PROCESSED_FILE.exists():
        return set()
    return set(line.strip() for line in PROCESSED_FILE.read_text().splitlines() if line.strip())


def save_processed(urls: set) -> None:
    PROCESSED_FILE.write_text("\n".join(sorted(urls)) + "\n", encoding="utf-8")


# ── Practitioner matching ──────────────────────────────────────────────────────
def matches_practitioner(text: str, practitioners: list) -> str | None:
    """Return the first practitioner name found in text, or None."""
    text_lower = text.lower()
    for name in practitioners:
        if name.lower() in text_lower:
            return name
    return None


# ── Keyword filtering ──────────────────────────────────────────────────────────
def score_entry(title: str, description: str, filters: dict) -> tuple[bool, list[str], str]:
    """
    Returns (passes: bool, matched_categories: list, reason: str)

    Logic:
      1. Exclude if any `exclude` term matches.
      2. Auto-pass if a named practitioner matches.
      3. Require at least one `required_any` term.
      4. Score against `categories`; accept if >= threshold categories match.
    """
    text = (title + " " + description).lower()

    # 1. Exclusion
    for term in filters.get("exclude", []):
        if term.lower() in text:
            return False, [], f"excluded by: {term}"

    # 2. Practitioner fast-pass
    practitioner = matches_practitioner(
        text, filters.get("practitioners_always_include", [])
    )
    if practitioner:
        # Still score categories for tagging, but always pass
        cats = _score_categories(text, filters)
        if not cats:
            cats = ["hybrid_postdigital"]  # fallback tag
        return True, cats, f"practitioner match: {practitioner}"

    # 3. Required gate
    required = filters.get("required_any", [])
    if required and not any(term.lower() in text for term in required):
        return False, [], "no required_any match"

    # 4. Category scoring
    cats = _score_categories(text, filters)
    threshold = filters.get("threshold", 1)
    if len(cats) < threshold:
        return False, [], f"below threshold ({len(cats)}/{threshold} categories)"

    return True, cats, "keyword match"


def _score_categories(text: str, filters: dict) -> list[str]:
    matched = []
    for cat_name, cat_data in filters.get("categories", {}).items():
        keywords = cat_data.get("keywords", []) if isinstance(cat_data, dict) else cat_data
        if any(kw.lower() in text for kw in keywords):
            matched.append(cat_name)
    return matched


# ── Filename generation ────────────────────────────────────────────────────────
def make_slug(title: str, url: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower())
    base = base.strip("-")[:50]
    if not base:
        base = hashlib.md5(url.encode()).hexdigest()[:8]
    return base


def unique_filename(date_str: str, slug: str) -> Path:
    candidate = INBOX / f"{date_str}-{slug}.md"
    counter = 1
    while candidate.exists():
        candidate = INBOX / f"{date_str}-{slug}-{counter}.md"
        counter += 1
    return candidate


# ── Inbox write ────────────────────────────────────────────────────────────────
def write_inbox_file(entry: dict, source_name: str, categories: list) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug  = make_slug(entry.get("title", ""), entry.get("link", ""))
    path  = unique_filename(today, slug)

    title       = entry.get("title", "Untitled").strip()
    url         = entry.get("link", "").strip()
    summary_raw = entry.get("summary", entry.get("description", ""))
    summary     = strip_html(summary_raw)[:600].strip()
    cats_str    = ", ".join(categories)

    # Published date from feed if available
    published = ""
    if hasattr(entry, "published"):
        published = entry.published

    content = f"""---
source_url: {url}
source_name: {source_name}
captured: {today}
published: {published}
intake_method: rss
categories: [{cats_str}]
protocol_stage: inbox
---

# {title}

{summary}

---
*Source: {source_name} — captured {today}*
"""

    path.write_text(content, encoding="utf-8")
    return path.name


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="A(DAI) RSS reader")
    parser.add_argument("--dry-run", action="store_true", help="Preview matches without writing")
    parser.add_argument("--tier",    type=int, default=0,  help="Only process feeds of this tier (0 = all)")
    parser.add_argument("--reset",   action="store_true", help="Clear processed log before running")
    args = parser.parse_args()

    if not FEEDS_FILE.exists():
        print(f"✗ Feeds config not found: {FEEDS_FILE}")
        sys.exit(1)

    if not FILTERS_FILE.exists():
        print(f"✗ Keyword filters not found: {FILTERS_FILE}")
        sys.exit(1)

    feeds_config = load_yaml(FEEDS_FILE)
    filters      = load_yaml(FILTERS_FILE)

    if args.reset and PROCESSED_FILE.exists():
        PROCESSED_FILE.unlink()
        print("↺  Cleared processed log\n")

    processed = load_processed()
    feeds     = feeds_config.get("feeds", [])

    if args.tier:
        feeds = [f for f in feeds if f.get("tier") == args.tier]
        print(f"── Tier {args.tier} feeds only ({len(feeds)} sources) ──\n")
    else:
        print(f"── Processing {len(feeds)} feeds ──\n")

    new_count  = 0
    skip_count = 0
    fail_count = 0

    for feed in feeds:
        name = feed.get("name", "Unknown")
        url  = feed.get("url", "")

        if not url:
            print(f"  ⚠  {name}: no URL, skipping")
            continue

        print(f"→ {name}")

        try:
            parsed = feedparser.parse(url, request_headers={"User-Agent": "ADAI-Scout/1.0"})
        except Exception as e:
            print(f"  ✗ fetch error: {e}")
            fail_count += 1
            continue

        if parsed.bozo and not parsed.entries:
            print(f"  ✗ feed error: {parsed.bozo_exception}")
            fail_count += 1
            continue

        feed_new = 0
        for entry in parsed.entries:
            link = entry.get("link", "").strip()
            if not link:
                continue

            if link in processed:
                skip_count += 1
                continue

            title       = entry.get("title", "")
            summary_raw = entry.get("summary", entry.get("description", ""))
            summary     = strip_html(summary_raw)

            passes, categories, reason = score_entry(title, summary, filters)

            if not passes:
                skip_count += 1
                processed.add(link)  # mark as seen even if filtered
                continue

            if args.dry_run:
                print(f"  ✓ [DRY] {title[:70]}")
                print(f"         categories: {', '.join(categories)}")
            else:
                fname = write_inbox_file(entry, name, categories)
                print(f"  ✓ {title[:70]}")
                processed.add(link)
                save_processed(processed)

            new_count += 1
            feed_new  += 1

        if feed_new == 0:
            print("    (no new signals)")

    print(f"\n── Done ──────────────────────────────────────────────────")
    print(f"   {new_count} new signals {'(dry run — not written)' if args.dry_run else 'written to /inbox/'}")
    print(f"   {skip_count} skipped (seen or filtered)")
    if fail_count:
        print(f"   {fail_count} feed fetch failures")
    print()


if __name__ == "__main__":
    main()
