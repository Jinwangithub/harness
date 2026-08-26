---
name: business-wiki-curation
description: Ingest sources into the Harness Wiki, compile evidence into canonical pages, answer read-only queries, archive requested knowledge, and lint evidence, links, conflicts, and orphan pages without silently changing facts.
---

# Business Wiki Curation

This is the single Harness Wiki entry point. It uses the Karpathy-style
`raw → wiki → index/log → query/lint` lifecycle while preserving Harness
change artifacts, approvals, gates, validation, and memory requirements.

## Harness Integration

This Skill is subordinate to the Orchestrator, selected Flow, Gate rules,
`.harness/changes/templates.md`, `.harness/wiki/README.md`, and the tools in
`.harness/tools/`. It does not replace artifact templates, create another Wiki
Skill, or bypass Mechanical Gate, Human Approval, Delivery Approval, Formal
Wiki Decision, or Change Retirement Authorization. The global
`/Users/apple/.claude/skills/karpathy-llm-wiki-main` is not modified.

## Initialization and boundaries

- Keep all Wiki data under `.harness/wiki/`.
- Initialize only a missing `.harness/wiki/raw/` directory; never create a
  project-root `raw/` or `wiki/` directory.
- Never overwrite an existing source, page, index, log, or artifact. Add a new
  source/version or record a conflict instead.
- Formal pages use only `project/`, `domains/`, `modules/`, and
  `integrations/`. Their existing frontmatter schema, stable rule IDs,
  `sources`, `approval`, and `supersedes` conventions remain authoritative.
- `raw/` is immutable input. `index.md` is generated. `log.md` is append-only.
- `.harness/changes/{change-id}/wiki/candidates.md` is a change-local compile
  draft, evidence list, and approval snapshot, not a second knowledge model.

## Ingest

1. Receive or fetch a source and save its original content plus metadata under
   `.harness/wiki/raw/` (source ID, URI or origin, capture date, content hash,
   and provenance). Do not edit the saved original.
2. Read `.harness/wiki/index.md`, then search module → domain → integration →
   keyword fallback. Record search terms, pages read, missing knowledge, and
   open questions in the current change artifact.
3. Compare the source with canonical pages and raw history. Classify each
   source as `New`, `Update`, `Disputed`, or `No material` before compiling.
4. Compile one source at a time. Preserve source identity and evidence links in
   the change-local draft and eventual page frontmatter.

## Compile

- Write durable knowledge only to the matching canonical page or to the
  current change-local draft until Formal Wiki Decision is approved.
- For every number, date, version, threshold, or citation, locate the exact
  source evidence before writing it. If it cannot be located, mark an open
  question or omit it; do not infer.
- A contradiction never silently overwrites history. Preserve both evidence
  records, mark the affected rule/page `Disputed` or `Outdated`, and record the
  resolution, `supersedes`, or open question.
- Approved formal pages must remain free of placeholders, guesses, secrets,
  and one-off implementation details.

## Cascade update

After a compile, use the generated index and full-text search to inspect all
affected domain, module, and integration pages. A formal update synchronizes:
source metadata, `approval`, stable rule IDs and `supersedes`, generated
`index.md`, and an appended `log.md` decision record. Rejected or deferred
material remains only in the change-local evidence/draft.

## Query

Query is read-only unless the user explicitly requests ingest, compile, or
archive. Search in this order: module → domain → integration → keyword. Answer
from approved canonical pages and cite `.harness/wiki/...` paths and stable
rule IDs. Do not write files for ordinary questions; distinguish missing,
disputed, and outdated knowledge from confirmed facts.

## Archive

Only an explicit archive request may create or update an archive page or query
record. Use the current Harness page schema, canonical directories, generated
index, append-only log, and change-local evidence. Archive is not permission to
promote unapproved facts into formal Wiki pages.

## Lint and report-only checks

Lint borrows evidence, link, conflict, and orphan-page checks from the Karpathy
workflow. It is report-only: it never repairs facts, rewrites formal pages,
or resolves conflicts automatically. Use `validate_wiki.py` for structure and
canonical-page validation, and `generate_wiki_index.py` for the index. Broken
links, missing evidence, unresolved conflicts, or orphan pages are findings to
record and review. Any Gate failure is Stop-the-Line; do not waive it.

## Harness change integration

Within the current change, record source capture, discovery/search, compile
classification, evidence, candidate/draft content, lint results, and the
Human Wiki Decision in the prescribed artifacts. Keep Delivery Approval,
Formal Wiki Decision, and Retirement Authorization separate. The candidate
artifact documents the compilation work; it is not the primary Wiki model.

## Required verification order

Run and record the command, exit code, output summary, and artifact path in the
Gate Record:

1. `python3 .harness/tools/validate_wiki.py --repo {repo}`
2. `python3 .harness/tools/generate_wiki_index.py`
3. `python3 .harness/tools/validate_wiki.py --repo {repo}`
4. `python3 .harness/tools/validate_change.py --change {change-id}`

If there is no active change, run the validator without `--change`, record its
actual idle result, and do not fabricate change artifacts.
