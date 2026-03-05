# Tendency Vocabulary

> **Iri to write.** This file defines A(DAI)'s directional forces vocabulary — the language the system uses to describe movement, tension, and tendency in the field. The signal processor loads this at runtime.

---

## Purpose

When the processor extracts intelligence from a signal, it needs vocabulary that captures *direction* — not just what something is, but where it's moving. This file defines that vocabulary.

## Structure

For each tendency, provide:
- **Name** — the force or direction (e.g., "decentralisation pressure", "institutional capture")
- **Charge** — `generative` | `negative` | `ambivalent`
  - *generative* — opens possibility, creates new conditions
  - *negative* — closes down, extracts, consolidates power
  - *ambivalent* — direction depends on context, could go either way
- **Description** — what this tendency looks like in practice
- **Signals** — what kinds of evidence suggest this tendency is active
- **Anti-tendency** — what opposes or complicates it

### Example entry (replace with real vocabulary)

```
Name: Decentralisation pressure
Charge: generative
Description: Movement toward distributed ownership, away from platform capture
Signals: New DAOs, cooperative models, artist-run infrastructure, exit from major platforms
Anti-tendency: Platform re-aggregation, convenience pull, network effects
```

## Tendencies

(Iri to populate — aim for 10-20 directional forces that recur across the field)

## Anti-vocabulary

Words and framings the system should **avoid** when extracting intelligence:
- (Iri to populate — e.g., marketing language, hype terms, reductive labels, VC framing applied to art)

---

*This file is read by `scripts/process_signals.py` during signal extraction. The processor passes it to Claude as editorial context — the vocabulary shapes what gets named and how.*
