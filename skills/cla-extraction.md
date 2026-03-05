# CLA Extraction Guide

> **Iri to write.** This file tells the signal processor how to classify signals across the four Causal Layered Analysis (CLA) layers. The processor loads this at runtime.

---

## Purpose

Every processed signal is tagged with a `cla_layer` in its frontmatter. This file defines how the processor decides which layer a signal belongs to — and what to look for at each depth.

## The Four Layers

### L1 — Litany
- **What it is:** The visible surface — events, announcements, launches, news
- **Signals look like:** (Iri to populate — e.g., "new platform launches", "funding announcements")
- **Confidence cues:** (what makes a litany classification confident?)

### L2 — Social / Systemic
- **What it is:** The systems and structures beneath events — markets, institutions, incentives, power dynamics
- **Signals look like:** (Iri to populate)
- **Confidence cues:**

### L3 — Discourse / Worldview
- **What it is:** The assumptions and framings that shape how the field talks about itself — values, narratives, ideologies
- **Signals look like:** (Iri to populate)
- **Confidence cues:**

### L4 — Myth / Metaphor
- **What it is:** The deep stories and unconscious patterns — what the field takes for granted, what it can't see about itself
- **Signals look like:** (Iri to populate)
- **Confidence cues:**

## Edge Cases

- Signals that span multiple layers: (Iri to define — tag primary layer, note secondary?)
- When confidence is low: (default to litany? flag for review?)

---

*This file is read by `scripts/process_signals.py` during signal extraction.*
