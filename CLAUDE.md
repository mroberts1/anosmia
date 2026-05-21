# Instructions for Claude (and other agents)

This file is the authoritative governance document for the Perfume vault. Read it in full before performing any operation on this vault. The rules below are non-negotiable.

Before acting, also read:
1. `content/_meta/index.md` — catalog of pages, keywords, open questions, candidates
2. `content/_meta/log.md` — last 20-30 entries for recent vault state
3. `content/_meta/eval.md` — stable evaluation questions (read only; don't answer unless running `/foundry-eval`)
4. `content/_meta/eval-usage.md` — explains the eval loop

If you're unsure, ask the user before doing anything destructive or structural.

---

This is an autonomous knowledge vault maintained by Claude. It follows the Karpathy wiki pattern: raw sources are ingested and compiled into a wiki of concepts, connections, and open questions. This file is the single source of truth for how Claude operates inside it.

**v2 changes from v1:** adds source tiering, conflict handling, freshness/re-ingest, pruning, voice anchor, query→concept promotion, cross-wiki linking, and an eval loop. See `## Changes from v1` at the bottom for a concise diff.

---

## Voice anchor

Concepts in this vault read like **field notes from a practitioner**, not gallery wall text, not academic survey, not marketing copy. Favour sharp claims, tight evidence, and honest open questions. Never write a sentence you wouldn't say out loud to a peer. When in doubt, write less.

Each vault pinned to this MANIFEST should replace this paragraph with one domain-specific sentence. The paragraph is load-bearing — it's what Claude reaches for when a source drags the voice toward its own register.

---

## Companion vault (optional)

If you keep a personal vault (a commonplace, Zettelkasten, or notes folder), you can link it alongside this one. The contract:

- **Your vault** — read-only for Claude. Never write, edit, move, or delete anything there. Cross-link into it with `[[YourVault/Path/Note Title]]` style references when a Foundry note is informed by your writing.
- **Foundry** — Claude writes, maintains, reorganises. You read, query, and occasionally correct.

One-way read, cross-linkable. That's the contract.

## Sibling vaults (new in v2)

Multiple agent-run Foundries may cross-link. Declare them in front-matter of this file:

```
Linked-vaults: ~/city-pop, ~/interasia-pop
```

Sibling vaults are **read-only** to Claude from this vault's perspective. Cross-link with `[[SiblingVaultName/content/Concept Title]]`. Never edit a sibling vault from inside another. Use a concept's home vault as the canonical location; all others link inward.

---

## Directory structure

Three layers, following the Karpathy wiki pattern:

| Directory | Purpose | Who writes |
|---|---|---|
| `inbox/` | Staging for unprocessed drops (PDFs, URLs, screenshots, pasted text) | You drop, Claude clears |
| `sources/` | Immutable atomic source notes — one per article/paper/transcript | Claude on ingest; minor edits only after creation; see `## Source freshness` |
| `content/` | LLM-maintained pages: concepts, queries, people, index, log, health | Claude maintains |
| `content/_archive/` | Superseded or pruned content, kept for provenance | Claude on prune; never deleted |

Special files in `content/_meta/`:
- **`index.md`** — catalog of every page, keyword glossary, research threads, open questions, prompts, candidates. Claude reads this first when answering a query. Updated on every operation.
- **`log.md`** — append-only chronological record. Each entry: `## [YYYY-MM-DD] operation | Title`. Never rewritten, only appended.
- **`health.md`** — lint dashboard. Overwritten each `/foundry-lint` run.
- **`eval.md`** — evaluation questions and latest answers. Overwritten each `/foundry-eval` run. See `## Evaluation loop`.

---

## File naming

- **Source notes**: Title Case — `The Rosetta Stone of Design Engineering.md`
- **Concept articles**: Title Case, descriptive — `Design-engineering handoff.md`
- **People**: `FirstName LastName.md` with hyphens only inside compound names. If surname unknown, `FirstName.md` and note the uncertainty.
- **Queries**: `YYYY-MM-DD-slug.md`
- **Archived**: original name preserved, moved into `content/_archive/YYYY-MM/`
- No emoji, no unicode hacks, no date prefixes in titles (dates go in front-matter)

---

## Front-matter

Plain key-value lines, not YAML. Blank line then `---` then body.

### Source notes (`sources/`)

```
Type: #type/source
Tier: #source/peer-reviewed
Area: #area/craft/ai
Keyword: #keyword/knowledge-management #keyword/llms
Date created: [[2026-04-14]]
Last verified: [[2026-04-14]]
Source: https://example.com/article
Superseded by:

---

**Summary**
3-5 sentences. Core claim.

**Key points**
- 5-10 tight bullets

**Claude's notes**
One paragraph: what's interesting, where it connects, what it contradicts.
```

`Tier:` is mandatory and picks exactly one of:

| Tier tag | When to use |
|---|---|
| `#source/peer-reviewed` | Journal article, academic book, conference paper with review |
| `#source/primary` | Created by the practitioner/artist/insider being discussed — interviews, artist statements, code, technical docs |
| `#source/journalism` | Edited publication with editorial oversight (trade press, magazines, curated blogs) |
| `#source/secondary` | Commentary, analysis, survey, synthesis by a non-primary voice |
| `#source/informal` | Tweets, forum posts, unedited blogs, Discord snippets, video comments |

`Last verified:` is the date Claude last confirmed the source URL resolves and content matches what was ingested. Set on ingest; update on re-verify.

`Superseded by:` is empty by default. On re-ingest of a newer version, point to the new source note and move this file untouched — see `## Source freshness`.

### Wiki pages — concepts (`content/`)

```
Type: #type/concept
Area: #area/craft/ai
Keyword: #keyword/knowledge-management
Date created: [[2026-04-14]]
Updated: [[2026-04-14]]
Sources: [[Source One]], [[Source Two]]
Related: [[Concept A]], [[Concept B]]
Contested: false
Confidence: medium

---
```

Body: `What it is` > `Why it matters` > `Key points` > `Evidence across sources` > `Disagreements` (if Contested: true) > `Open questions` > `Prompts`.

**`Contested:`** — `true` when two or more sources make incompatible claims about the concept. When true, add a `Disagreements` section quoting each side with attribution, and never silently pick a winner. Contested concepts are surfaced in `health.md`.

**`Confidence:`** — `high | medium | low`, reflecting the weakest claim in the concept.
- `high` — core claims rest on 2+ sources, at least one `#source/peer-reviewed` or `#source/primary`
- `medium` — 2+ sources, mixed tiers, no major contradictions
- `low` — minimum threshold met but sourcing is thin, tiered low, or partially contested

Per-claim annotations: append `^[tier]` after a sentence when the source for that specific claim is weaker than the concept's overall confidence. Example: *"Vera Molnar began using computers in 1968.^[#source/informal]"*

**Voice.** See `## Voice anchor`. Key points should be pithy — one line each, claim-shaped.

**Prompts.** Essay-shaped prompts where the concept intersects your existing notes. Distinct from Open questions (research gaps): Prompts are *"you could write this now."* One or two sentences each, pointed and specific. Empty is fine.

### Wiki pages — queries

```
Type: #type/query
Area: #area/craft/management
Keyword: #keyword/leadership
Date created: [[2026-04-14]]
Question: the question asked
Promotion: pending | promoted | declined

---
```

`Promotion:` — see `## Query → concept promotion`.

### Wiki pages — people

```
Type: #type/person
Area: #area/craft/ai
Keyword: #keyword/llms
Date created: [[2026-04-14]]

---

One-line identifier. Topic description.

**Sources in the Foundry**
- [[Source Title]]

**Concepts they inform**
- [[Concept Title]]
```

---

## Tag taxonomy

**`#area/`** — examples: Self, Craft, Work, Health, Finances, Meta (whatever top-level areas fit your life)
**`#area/craft/`** — design, engineering, management, ai, product, writing

**`#type/`** — each note gets exactly one: `source`, `concept`, `query`, `person`, `meta`.

**`#source/`** — each note in `sources/` gets exactly one tier tag (see front-matter table above).

**`#keyword/`** — free-form but curated via the Keywords section of `content/_meta/index.md`. Before creating a new keyword: check index > reuse near-match if it exists > otherwise add with a one-line definition.

---

## People — when to create a page

| Tier | Trigger | Action |
|---|---|---|
| Author | Person authored a source in `sources/` | Always create a page in `content/` on ingest |
| Subject | Source is substantively about a person | Create page with a richer profile |
| Passing reference | Mentioned in passing | Use `[[Name]]` wikilink without creating a file. Create only on the **second** independent citation |

People pages stay thin — connector nodes, not essays.

---

## Citation & linking

- **Every claim in a concept must be traceable.** `Sources:` front-matter lists the source notes the claim rests on.
- **Backlink rule**: every new concept links at least 2 existing concepts in `Related:`, or notes why it's an island (flagged in health).
- **Cross-vault links**: `[[VaultName/Path/Note Title]]` for companion or sibling vaults.
- **Never break a link.** If renaming, update all backlinks. If archiving, leave a stub that redirects.

---

## Source freshness (new in v2)

Sources aren't eternal. Three rules:

1. **`Last verified:`** is set on ingest and updated whenever Claude re-confirms the source. Sources older than 18 months with no re-verification are surfaced in `health.md` under "Stale sources."
2. **Re-ingest**: when a source has a meaningfully updated version (v2 of a paper, rewritten article, new edition), Claude ingests the new version as a separate source note and sets the old one's `Superseded by:` field. **Never edit the old source's body** — it's a historical artifact.
3. **Revision propagation**: after re-ingest, Claude checks every concept citing the old source and decides per concept whether the new version changes the claim. If yes, update the concept, append to `Updated:`, and log the revision. If no, leave the concept pinned to the old source (older claim still stands on older evidence).

Sources are never deleted. Retractions get a `Retracted:` field and are kept; the concepts citing them are re-evaluated.

---

## Conflict resolution (new in v2)

When ingesting or compiling, Claude detects when two sources make incompatible claims about the same concept. Three-step rule:

1. **Never silently resolve.** Don't pick a winner based on which source Claude read last, which tier is higher, or which sounds more authoritative.
2. **Flag it.** Set `Contested: true` on the concept and add a `Disagreements` section. Each side gets at least one direct quote and a `[[Source]]` attribution. Tier tags flow through — the reader sees `#source/peer-reviewed` disagreeing with `#source/informal` at a glance.
3. **Preserve the dispute.** A contested concept is a feature of the domain, not a bug in the wiki. Don't try to collapse it into consensus unless new sources genuinely resolve it — and even then, keep the history visible in `Disagreements` (struck through or moved to a `Historical disagreement` subsection).

Contested concepts are listed in `health.md` so you can decide when to intervene.

---

## Query → concept promotion (new in v2)

Queries can graduate to concepts. Rule:

- After a query is written, Claude sets `Promotion: pending`.
- If the query answer rests on **2+ sources** and the question reflects a durable concept (not a one-off of-the-moment ask), Claude creates a concept from it on the next `/foundry-compile` run and sets `Promotion: promoted` on the query with a link to the new concept.
- If the query is too narrow, time-bound, or thinly sourced, Claude sets `Promotion: declined` with a one-line reason. Declined queries remain in the wiki as-is.
- Pending queries older than 60 days are surfaced in `health.md`.

Exploration compounds, but only when the exploration earned its keep.

---

## Pruning & archival (new in v2)

Claude does not delete. Claude archives.

Triggers for archival (all run during `/foundry-lint`, acted on during `/foundry-prune`):

| Trigger | Action |
|---|---|
| Candidate in `index.md` for > 18 months with no second source | Move to `content/_meta/candidates-archive.md`, note in log |
| Orphan concept (zero inbound links) for > 12 months | Surface in health; archive only with your confirmation |
| Source with `Retracted:` and no remaining citing concepts | Move to `content/_archive/YYYY-MM/` |
| Concept fully superseded by a newer concept | Move to `content/_archive/YYYY-MM/`, leave stub with forwarding link |

Archived files keep their history. A stub at the original path lists where the content moved and why. `/foundry-prune` requires explicit confirmation from you — Claude never prunes unattended.

---

## Evaluation loop (new in v2)

The vault needs a qualitative health check, not just lint stats.

`content/_meta/eval.md` holds 5-10 questions that should be answerable from the wiki. Examples for a generative-art vault: *"Who are the key figures of first-generation computer art and what distinguishes them?"*, *"How did plotter-based practice differ between Europe and the US in the 1970s?"*

`/foundry-eval` (run quarterly, or on demand):

1. For each question, Claude writes a short answer citing only wiki pages (not sources directly).
2. For each answer, Claude rates coverage: `strong` (wiki has the concepts and they cite ≥2 tiered sources), `thin` (wiki has the concepts but sourcing is weak), `missing` (wiki can't answer).
3. `thin` and `missing` feed directly into `index.md` Open Questions and Candidates.

The eval questions are stable across runs so you can track whether the wiki is getting better at answering them.

---

## Operations

### Ingest (`/foundry-ingest`)

Process anything in `inbox/` into clean atomic source notes in `sources/`.

Flow: read source > assign tier > normalise into source note > fill front-matter (including `Tier:` and `Last verified:`) > write summary + key points + Claude's notes > cross-reference companion and sibling vaults > update `content/_meta/index.md` > append to `content/_meta/log.md` > clear inbox.

On re-ingest of a superseded version: new source note created, old source's `Superseded by:` set, citing concepts reviewed (see `## Source freshness`).

Won't do: write into companion or sibling vaults, create concept articles (that's compile's job), invent work if inbox is empty, ingest without a tier.

### Compile (`/foundry-compile`)

Scan `sources/` for un-compiled sources (not cited in any concept's `Sources:` field). Either extend an existing concept or spin out a new one — but only when the 2-source rule is met. Otherwise, log the theme to Candidates and wait.

During compile, Claude actively checks for conflicts against existing concepts (see `## Conflict resolution`). If a new source contradicts a concept, `Contested: true` is set.

After each run: update Research Threads, append new Prompts, update keyword counts, reassess Confidence on touched concepts, process pending queries for promotion. Append to log.

Won't do: write into companion or sibling vaults, spin out a concept from a single source, silently resolve contradictions, break links.

### Query (`/foundry-ask`)

Research a question across the Foundry, companion vault, and sibling vaults (all read-only except this Foundry). Write report to `content/YYYY-MM-DD-slug.md` with `Promotion: pending`. Every claim cites its source.

Findings with 2+ sources feed back to Candidates. Open gaps feed to Open Questions. Essay prompts to Prompts.

Won't do: write into companion or sibling vaults, invent citations, pad thin answers, mark a query `promoted` without going through compile.

### Lint (`/foundry-lint`)

Health-check the whole vault. Overwrite `content/_meta/health.md` with: Stats, Orphans, Candidates needing attention, Stale sources, Contested concepts, Pending queries >60 days, Keyword drift.

### Prune (`/foundry-prune`, new in v2)

Run only on your explicit request. Walks through each archival candidate from the latest `health.md`, asks for confirmation per item, archives confirmed ones into `content/_archive/YYYY-MM/` with stubs in place. Appends to log.

### Eval (`/foundry-eval`, new in v2)

Run the evaluation loop against `content/_meta/eval.md`. Rewrite that file with fresh answers and ratings. Feed thin/missing findings into `index.md`. Append to log.

---

## What NOT to do

- Don't write into the companion vault or sibling vaults.
- Don't create files outside `sources/`, `content/`, `content/_archive/`, or `inbox/`.
- Don't speculatively create concepts from a single source.
- Don't silently resolve contradictions between sources.
- Don't ingest a source without a `Tier:`.
- Don't delete anything — archive with a stub.
- Don't use emojis.
- Don't add TODO comments. If something's missing, log it in Candidates.
- Don't create helpers, templates, or meta-infrastructure beyond what this MANIFEST names.

---

## Changes from v1

- **Voice anchor**: explicit per-vault one-liner at the top, load-bearing.
- **Source tiers**: mandatory `Tier:` tag on every source (`peer-reviewed`, `primary`, `journalism`, `secondary`, `informal`).
- **Per-concept confidence**: `Confidence: high | medium | low` in front-matter; per-claim `^[tier]` annotation when a specific claim is weaker than the concept overall.
- **Conflict resolution**: `Contested:` field, `Disagreements` section, never silently resolve.
- **Source freshness**: `Last verified:` and `Superseded by:` fields; re-ingest protocol; stale-source surfacing.
- **Query → concept promotion**: `Promotion:` field on queries; explicit rule for when queries graduate.
- **Pruning & archival**: `content/_archive/`, `/foundry-prune` operation, stubs, never-delete rule.
- **Sibling vaults**: cross-linking between multiple agent-run Foundries.
- **Evaluation loop**: `content/_meta/eval.md`, `/foundry-eval` operation, stable eval questions tracked over time.
