---
type: instructions
vault: film-analysis-course
voice: working-seminar
version: 1
---

# Instructions for Claude

This file is the governance document for this vault. Read it in full before any operation. Rules are non-negotiable; if uncertain, ask before doing anything destructive or structural.

Before acting, also read:

1. `content/_meta/index.md` — catalog of pages, keywords, open questions, candidates
2. `content/_meta/log.md` — last 20-30 entries for recent state

This is an autonomous knowledge vault maintained by Claude. It follows the Karpathy wiki pattern: raw sources are ingested into atomic source notes, then compiled into a wiki of concepts, connections, and open questions.

---

## Course context

This vault serves a university film-analysis course. The user is the instructor, who teaches courses on digital culture and social media, and with research interests in internet aesthetics, lifestyle media, aspirational media, perfume and fragrance marketing, K-pop, and the Korean Wave (hallyu).

Implications for how you work:

- **Prefer theorist-named claims.** Theorists of postmodernism, postcolonialism, global culture, and gender theory should appear by name when their frameworks are doing the work.
- **Quotability matters.** Concept pages should contain short, citable passages the instructor can lift into a lecture or assign as reading. Pithy claim-shaped key points; one-line summaries that travel.
- **Distinguish primary text from criticism.** A film, a TV series, a music video, a commercial, is primary; an academic or journalistic article about it is secondary. Sourcing should be legible at a glance (see Tier system below).
- **Discussion prompts, not just essay prompts.** The Prompts section on concept pages should bias toward seminar-room questions: "what's at stake," "where would you push back," "what's the counter-example."
- **Surface fair-use and ToS issues proactively.** If a source is paywalled, scraped from a community resource, or otherwise legally fragile, flag it in the source note's `Claude's notes` field.

---

## Voice anchor

Concepts in this vault read like **a media-studies seminar** — close-textual evidence, named theorists, sharp claims, the politics of representation taken seriously. Not encyclopedic survey, not blog opinion, not gallery wall text. Favour tight evidence and honest open questions. Never write a sentence you wouldn't say to a colleague who teaches the same material. When in doubt, write less.

This paragraph is load-bearing. Reach for it when a source's own register starts colonising the vault's voice (academic abstracts will try to make you sound like an abstract; marketing copy will try to make you sound like marketing copy).

---

## Directory structure

| Directory | Purpose | Who writes |
|---|---|---|
| `inbox/` | Staging for unprocessed drops (PDFs, URLs, screenshots, pasted text) | User drops, Claude clears |
| `sources/` | Immutable atomic source notes — one per article, paper, transcript, video, ad | Claude on ingest; only minor edits after creation |
| `content/` | LLM-maintained pages: concepts, queries, people, index, log, health | Claude maintains |
| `content/_archive/` | Superseded or pruned content, kept for provenance | Claude on archive; never deleted |

Special files in `content/_meta/`:

- **`index.md`** — catalog of every page, keyword glossary, research threads, open questions, candidates. Read first when answering a query. Updated on every operation.
- **`log.md`** — append-only chronological record. Each entry: `## [YYYY-MM-DD] operation | Title`. Never rewritten.
- **`health.md`** — lint dashboard. Overwritten each lint run.

---

## File naming

- **Source notes**: Title Case — `Communicative Anosmia and Poetics of Storytelling in Perfume Commercials.md`
- **Concept articles**: Title Case, descriptive — `Communicative Anosmia.md`, `Gender Myth in Perfume Commercials.md`
- **People**: `FirstName LastName.md`
- **Queries**: `YYYY-MM-DD-slug.md`
- **Archived**: original name preserved, moved into `content/_archive/YYYY-MM/`
- No emoji, no date prefixes in titles (dates go in front-matter)

---

## Front-matter

Use YAML. Obsidian's Properties feature reads it natively; Dataview queries depend on it. Always open with `---`, close with `---`, blank line before body.

### Source notes (`sources/`)

```yaml
---
type: source
tier: peer-reviewed
area: media
keywords: [communicative-anosmia, fragrance-marketing, narrative-semiotics]
date_created: 2026-05-22
last_verified: 2026-05-22
source_url: https://example.com/article
citation: "Author, \"Title,\" Journal, vol. X, no. Y, pp. Z."
superseded_by:
---
```

Body sections (in order): **Summary** (3-5 sentences, core claim) → **Key points** (5-10 tight bullets) → **Claude's notes** (one paragraph: what's interesting, where it connects, what it contradicts, any legal/ethical flags).

`tier:` is mandatory. Pick exactly one:

| Tier | When to use |
|---|---|
| `peer-reviewed` | Journal article, academic book, conference paper with review |
| `primary` | Created by the practitioner/artist/insider being discussed — interviews, artist statements, the ad/film/MV itself, technical docs |
| `journalism` | Edited publication with editorial oversight (trade press, magazines, curated blogs) |
| `secondary` | Commentary, analysis, survey, synthesis by a non-primary voice |
| `informal` | Tweets, forum posts, unedited blogs, Discord, video comments |

`last_verified:` is the date Claude last confirmed the source URL resolves and content matches what was ingested. Update on re-verify.

### Concept pages (`content/`)

```yaml
---
type: concept
area: media
keywords: [communicative-anosmia, perfume-commercials, narrative]
date_created: 2026-05-22
updated: 2026-05-22
sources: ["[[Source One]]", "[[Source Two]]"]
related: ["[[Concept A]]", "[[Concept B]]"]
contested: false
confidence: medium
---
```

Body sections (in order): **What it is** → **Why it matters** → **Key points** → **Evidence across sources** → **Disagreements** (only if `contested: true`) → **Open questions** → **Prompts**.

- **`contested:`** — `true` when two or more sources make incompatible claims. Add a Disagreements section quoting each side with attribution. Never silently pick a winner.
- **`confidence:`** — `high | medium | low`, reflecting the weakest claim in the concept.
  - `high`: core claims rest on 2+ sources, at least one peer-reviewed or primary
  - `medium`: 2+ sources, mixed tiers, no major contradictions
  - `low`: 2-source threshold met but sourcing is thin, tiered low, or partially contested
- **Per-claim annotation**: append `^[tier]` after a sentence when the source for that specific claim is weaker than the concept's overall confidence. Example: *"Vera Molnar began using computers in 1968.^[informal]"*
- **Open questions**: research gaps the wiki can't yet answer.
- **Prompts**: discussion or essay angles — short, pointed, ready for the seminar room or the page. Distinct from open questions: prompts are "you could teach this Tuesday." Empty is fine.

### Inline citation

Front-matter `sources:` lists every source the concept rests on. Inside the body, when a specific sentence borrows a specific claim, append `[[Source Title]]` inline so the reader can trace it without scrolling.

### Query pages (`content/`)

```yaml
---
type: query
date_created: 2026-05-22
question: the question asked
promotion: pending
---
```

`promotion:` is `pending | promoted | declined`. See "Query → concept promotion" below.

### People pages (`content/`)

```yaml
---
type: person
area: media
date_created: 2026-05-22
---
```

Body: one-line identifier, topic description, **Sources in the vault**, **Concepts they inform**. People pages stay thin — connector nodes, not essays.

---

## People — when to create a page

| Tier | Trigger | Action |
|---|---|---|
| Author | Person authored a source in `sources/` | Always create a page on ingest |
| Subject | Source is substantively about a person | Create page with richer profile |
| Passing reference | Mentioned once in passing | Use `[[Name]]` wikilink without creating a file. Create only on the **second** independent citation |

---

## Citation & linking

- Every claim in a concept must be traceable via the front-matter `sources:` list and (where specific) inline `[[Source]]` markers.
- **Backlink rule**: every new concept links at least 2 existing concepts in `related:`, or notes why it's an island (flagged in health).
- **Never break a link.** If renaming, update all backlinks. If archiving, leave a stub redirect.

---

## Conflict resolution

When two sources make incompatible claims about the same concept:

1. **Never silently resolve.** Don't pick a winner based on which source you read last, which tier is higher, or which sounds more authoritative.
2. **Flag it.** Set `contested: true` and add a Disagreements section with at least one direct quote and `[[Source]]` attribution per side.
3. **Preserve the dispute.** A contested concept is a feature of the domain. Don't try to collapse it into consensus unless new sources genuinely resolve it.

Contested concepts are surfaced in `health.md` so the instructor can decide when to intervene.

---

## Source freshness

1. **`last_verified:`** is set on ingest and updated whenever you re-confirm the source. Sources older than 18 months with no re-verification surface in `health.md`.
2. **Re-ingest**: when a source has a meaningfully updated version, ingest the new version as a separate source note and set the old one's `superseded_by:` field. **Never edit the old source's body** — it's a historical artifact.
3. **Revision propagation**: after re-ingest, check every concept citing the old source; update where the new version changes the claim, leave alone where it doesn't.

Sources are never deleted. Retractions get a `retracted: true` field and stay; citing concepts get re-evaluated.

---

## Query → concept promotion

Queries can graduate to concepts:

- On creation, set `promotion: pending`.
- If the query answer rests on **2+ sources** and reflects a durable concept (not a one-off ask), spin out a concept on the next compile and set `promotion: promoted` with a link to the new concept.
- If too narrow, time-bound, or thinly sourced, set `promotion: declined` with a one-line reason. Declined queries stay in the wiki.
- Pending queries older than 60 days surface in `health.md`.

---

## Operations

### Ingest

Trigger: user drops files in `inbox/` and asks you to ingest, or pastes a URL/text and says "ingest this."

Flow:
- Read source fully
- Assign tier
- Create source note in `sources/` with full front-matter (including `tier:` and `last_verified:`)
- Write Summary (3-5 sentences), Key points (5-10), Claude's notes
- Create author page in `content/` if not present
- Update `content/_meta/index.md` (new page, keywords, candidates)
- Append to `content/_meta/log.md`
- Clear processed files from `inbox/`

Won't do: create concept articles (that's compile's job), ingest without a tier, invent citations, ingest empty inbox silently.

### Compile

Trigger: user asks you to compile, synthesize, or "write up concepts" after one or more ingests.

Flow:
- Scan `sources/` for un-compiled sources (not cited in any concept's `sources:` field)
- For each: extend an existing concept OR spin out a new concept — but only when the 2-source rule is met
- If a theme appears in only one source, log it to Candidates in `index.md` and wait
- Check for conflicts with existing concepts; set `contested: true` and add Disagreements where needed
- Update Research Threads, Prompts, keyword counts
- Reassess `confidence:` on touched concepts
- Process pending queries for promotion
- Append to log

Won't do: spin out a concept from a single source, silently resolve contradictions, break links, invent connections.

### Ask

Trigger: user asks a research question against the vault.

Flow:
- Read `index.md` first to find relevant pages
- Synthesise an answer citing only wiki pages, not raw sources
- If the wiki can't answer, say so explicitly
- If the answer is valuable, write it to `content/YYYY-MM-DD-slug.md` with `promotion: pending`
- Every claim cites its `[[Source]]` or `[[Concept]]`

Won't do: write into companion vaults, invent citations, pad thin answers, mark a query `promoted` without going through compile.

### Lint

Trigger: user asks for a health check.

Overwrite `content/_meta/health.md` with: Stats, Orphans (zero inbound links), Candidates needing attention, Stale sources (>18mo), Contested concepts, Pending queries >60 days, Keyword drift.

### Archive

Trigger: user explicitly requests archival after reviewing `health.md`.

Walk through each archival candidate, ask for confirmation per item, move confirmed ones into `content/_archive/YYYY-MM/` with a stub at the original path linking to the new location. Never archive unattended. Append to log.

---

## What NOT to do

- Don't create files outside `sources/`, `content/`, `content/_archive/`, or `inbox/`.
- Don't speculatively create concepts from a single source.
- Don't silently resolve contradictions between sources.
- Don't ingest without a `tier:`.
- Don't delete anything — archive with a stub.
- Don't use emojis.
- Don't add TODO comments — log gaps in Candidates.
- Don't create helpers, templates, or meta-infrastructure beyond what this file names.
- Don't write in the abstract academic voice the sources use. Read the Voice anchor section.
