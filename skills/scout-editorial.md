# Scout Editorial Judgment

This file defines the editorial lens for the A(DAI) scout agent.
Read by `scripts/scout.py` and `scripts/rss_reader.py` at runtime.
The difference between noise and intelligence lives here.

---

## What A(DAI) Is Tracking

The Digital Arts refers to artistic practices in which digital technologies
play an essential role in the conception, creation, performance, distribution,
or experience of the work.

This is not a medium. It is a system of artistic production spanning code,
networks, sensors, AI models, robotics, and interactive environments.
Computation is both material and method. The field runs from the early 1960s
(Nees, Nake, Molnár, Whitney) to the present.

### The Six Pillars

**1. Generative & Algorithmic Art**
Artworks that emerge from code, rules, data, or autonomous systems.
Includes: algorithmic drawing, plotter art, creative coding (Processing, p5.js,
TouchDesigner, openFrameworks), on-chain generative projects (Art Blocks, fxhash),
AI-assisted image/text/video generation, procedural and evolutionary artworks.

**2. Immersive & Experiential Art**
Works that create spatial, multi-sensory environments.
Includes: projection mapping, LED architecture (teamLab, Outernet), VR/AR/MR,
multi-channel sound, embodied interaction via sensors and motion tracking.

**3. Live Digital Performance**
Code, visuals, sound, and embodiment in real time.
Includes: live coding (Algorave, TidalCycles, Sonic Pi, TOPLAP), VJ performance,
audiovisual mixing, streaming-native performance (Twitch/YouTube Live as art space),
virtual performers and avatars, AI improvisation, robotic and biofeedback performance.

**4. Networked, Online & Web-Based Art**
The network as material, not gallery.
Includes: net art, browser-native works, blockchain and NFT-based art,
virtual worlds, metaverse performances, game-engine art, smart contracts as medium,
social media performance, post-internet art.

**5. Robotic, Sensorial & Machine-Integrated Art**
Digital art extended into embodied, mechanical, environmental form.
Includes: robotic and kinetic installations, biofeedback art, cybernetic ecosystems,
machine vision and computer vision responsive works, interactive sculpture.

**6. Hybrid & Post-Digital Practice**
Digital processes permeating the entire creative pipeline.
Includes: CNC/laser-cut/3D-printed sculpture, AI-assisted choreography, motion capture
for dance and theatre, data-driven architecture, hybrid exhibitions.

---

## What counts as a signal

- **Practitioner profiles** — artists, collectives, researchers working in the field
- **New works and commissions** — exhibitions, premieres, publications, releases
- **Tool and platform releases** — new software, hardware, platforms relevant to practice
- **Institutional moves** — programmes, residencies, grants, policy
- **Critical and theoretical writing** — essays, papers, interviews
- **Historical recovery** — documentation of overlooked or early practitioners
- **Field events** — festivals, symposia, conferences (Ars Electronica, ISEA, Eyeo, etc.)
- **Market and ecosystem signals** — significant sales, platform shifts, NFT ecosystem developments

---

## What to ignore

### Hard exclusions
- Digital marketing, digital transformation, digital banking
- NFT price speculation, floor price tracking, crypto trading
- AI productivity tools with no artistic framing
- Press releases with no editorial content
- SEO content farms, AI-generated article mills
- Celebrity tech news unrelated to art practice
- Social media engagement bait ("10 artists you need to follow")

### Soft exclusions (require judgment)
- Mainstream tech coverage of AI that doesn't engage with art practice
- Architecture and design using digital tools purely instrumentally
- Academic papers outside art/technology intersection
- Gaming coverage with no art/artist framing

---

## Source quality

### Preferred sources
Rhizome, Creative Applications Network, We Make Money Not Art, Neural.it,
Ars Electronica, ZKM, V&A Digital, Serpentine, Tate Research,
TOPLAP, Processing Foundation, ISEA, DAM Berlin, fxhash blog, Art Blocks blog, Eyeo Festival

### Caution sources
Hyperallergic, Dezeen, The Art Newspaper, Artforum, Frieze,
Wired (Design), MIT Media Lab, Vice Arts, Medium publications

### Excluded sources
SEO aggregators, press release wires (PR Newswire, BusinessWire),
crypto/NFT trading platforms, AI hype blogs with no art focus

---

## Relevance thresholds

- **High relevance:** Named practitioner in the six pillars; institutional commission or major exhibition; new tool/platform built for or by artists; critical writing from established field publications; historical documentation of pre-2000 digital art
- **Marginal:** General AI art coverage without practitioner focus; tech art that is decorative/commercial rather than critical; single-mention practitioners with no other signal context
- **Out of scope:** Anything matching the hard exclusion list; digital illustration/graphic design/UI-UX not framed as art practice; traditional art with digitally produced catalogue images only

---

## Deduplication

- Same URL from multiple sources: keep first, discard subsequent
- Same story covered by multiple outlets: keep highest-tier source
- Event announcement + review of same event: keep both (different signal types)
- Updated versions of the same work: keep if substantively new information

---

## Historical Coverage Note

Signals about historical practitioners are high-value even when the source is
a recent retrospective, obituary, archive, or academic recovery project.
The `practitioners_always_include` list in `config/keyword-filters.yaml` ensures
these names always pass the relevance gate regardless of surrounding context.

---

*This file is read by `scripts/scout.py` at runtime. The scout passes it to Claude as
editorial context — the guidance shapes what gets found and what gets filtered out.*
