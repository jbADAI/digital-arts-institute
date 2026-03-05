# Scout Editorial Judgment

> **Iri to write.** This file defines the Scout agent's editorial policy — what to look for, what to ignore, and how to judge relevance. The scout loads this at runtime.

---

## Purpose

The Scout agent searches the web for signals relevant to the digital arts field. This file defines its editorial lens — the difference between noise and intelligence.

## What counts as a signal

(Iri to populate — e.g., practitioner interviews, exhibition announcements, tool releases, policy changes, market shifts, critical writing)

## What to ignore

(Iri to populate — e.g., promotional content, affiliate marketing, engagement bait, repackaged press releases)

## Source quality

### Preferred sources
(Iri to populate — e.g., practitioner blogs, institutional publications, academic papers, field-specific platforms)

### Caution sources
(Iri to populate — e.g., aggregator sites, mainstream tech press writing about art)

### Excluded sources
(Iri to populate — e.g., SEO farms, AI-generated content mills)

## Relevance thresholds

- **High relevance:** (what makes a signal clearly worth capturing?)
- **Marginal:** (when should the scout include vs skip?)
- **Out of scope:** (what's clearly outside the field?)

## Deduplication

How to handle signals that overlap with existing corpus: (Iri to define)

---

*This file is read by `scripts/scout.py` at runtime. The scout passes it to Claude as editorial context — the guidance shapes what gets found and what gets filtered out.*
