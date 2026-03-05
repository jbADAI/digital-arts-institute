# A(DAI) — Session Context

Paste this at the start of every Claude session working on A(DAI).

---

## What A(DAI) is

A(DAI) addresses the semantic gap in digital arts — the absence of a shared knowledge layer that can represent practitioner knowledge, lived experience, and field intelligence in a form that machines can reason over.

The result is a knowledge commons and semantic graph that powers cognitive applications: decision support, curatorial tools, semantic search, and field intelligence interfaces — built on a substrate that is transparent, provenance-tracked, and owned by no single actor.

## Design principles

- **Agent-native.** Designed for machines to read and write. The human surface is minimal — three pages on the website.
- **Git-first.** Intelligence lives in this repo as structured markdown files. Every change is versioned. Every agent action is a commit.
- **Commons-first.** The knowledge commons is never sold. Mode 1 (Commons Intelligence) is public good. Mode 2 (Advisory Intelligence) is commissioned services built on top.
- **Provenance as infrastructure.** Every node carries full lineage — who contributed it, how, when, with what confidence.
- **Schema is provisional.** The ontology evolves. After every 20 processed signals, the schema is reviewed.

## Repository structure

```
inbox/              ← all signals land here first
signals/            ← processed signal files
concepts/           ← one .md per concept
practitioners/      ← one .md per person or org
scenes/             ← one .md per scene
threads/            ← active investigations
outputs/            ← sensemaking outputs
skills/             ← agent behaviours as markdown (editable without code)
config/             ← scout-queries.yaml, example.env
scripts/            ← process_signals.py, export_graph.py, scout.py
graph-data.json     ← auto-generated, never edit manually
```

## The three agents

1. **Scout** — finds signals online, writes raw files to `/inbox/`
2. **Processor** — reads `/inbox/`, extracts structured intelligence, writes to `/signals/` and related files. One Claude API call per signal, fresh context each time.
3. **Synthesis** — answers queries across the corpus. Claude reading the repo directly.

## Signal file format

Every processed signal is a markdown file with YAML frontmatter:
- `id`, `title`, `date`, `source_type`, `submitted_by`
- `protocol_stage`: SENSE | QUERY | SPECULATE | REACT | COLLABORATE | EXPERIMENT
- `intelligence_tier`: primary | secondary | tertiary
- `cla_layer`: litany | social | discourse | myth
- `provenance`: contributor, method, confidence, lived_experience, consent, license
- `tendencies`: directional forces with charge (generative/negative/ambivalent)
- `themes`, `summary`

See `SCHEMA.md` for full spec and `graph-data.json` format.

## Team

- **Iri** — coordination, curatorial, strategic
- **JB** — distributed systems, market formation, artist
- **Piyush** — generative/algorithmic artist, art history, generative brand
- **Gio** — core developer, artist
