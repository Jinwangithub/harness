---
name: business-wiki-curation
description: Extract business Wiki candidates from completed Harness change artifacts, request human confirmation, and update the formal Wiki only after explicit approval.
---

# Business Wiki Curation

## Harness Integration Constraint

This Skill is subordinate to Harness flow, gates, templates, wiki README, and skills README:

- Flow routing and finalization rules come from `.harness/rules/flow-lite.md` and `.harness/rules/flow-standard.md`.
- Gate requirements come from `.harness/rules/gates.md`.
- Artifact fields come from `.harness/changes/templates.md`.
- Candidate-first Wiki policy comes from `.harness/wiki/README.md`.
- Skill path convention comes from `.harness/skills/README.md`.

Do not use this Skill to bypass Flow, Gate, Human Approval, or archive requirements.

## Candidate-first Rule

Every completed requirement produces a change-local candidate artifact first:

```text
.harness/changes/{change-id}/wiki/candidates.md
```

Candidate content is not canonical knowledge. It is a proposal extracted from change artifacts for human review. Official `.harness/wiki/` updates require explicit human approval before any candidate content is copied into formal Wiki pages.

Rejected or deferred candidates remain in the change artifact and are not copied into `.harness/wiki/`.

## Candidate Knowledge

Extract durable business knowledge such as:

- Business terms and definitions.
- Domain rules and invariants.
- User or operational workflows.
- Data contracts and externally meaningful field semantics.
- Integration facts about upstream/downstream systems.
- Operational constraints that future requirements must respect.
- Testing knowledge that reflects business behavior.
- Durable exceptions that should be remembered for future work.

## Do Not Add

Do not add:

- Guesses or unverified assumptions.
- Secrets, credentials, tokens, customer data, or sensitive operational details.
- One-off implementation details without durable business meaning.
- Process lessons that belong in `.harness/memory/`.
- Temporary debugging observations.
- Facts contradicted by existing Wiki unless explicitly resolved by the user.

Unknown business rules must remain `{待确认}` or Phase 1 Open Questions. Do not guess.

## Workflow

1. Inspect the completed change artifacts for the current `{change-id}`.
2. Identify durable business knowledge and separate it from implementation-only details.
3. Search existing `.harness/wiki/` pages before proposing updates to avoid duplicates or contradictions.
4. Generate `.harness/changes/{change-id}/wiki/candidates.md` using the template in `.harness/changes/templates.md`.
5. At delivery, ask for human approval for any formal Wiki update.
6. If approved, update the relevant formal Wiki pages and synchronize:
   - `.harness/wiki/index.md`
   - `.harness/wiki/log.md`
7. If rejected, deferred, partially approved, or no candidates exist, record the decision and reason in `wiki/candidates.md` and delivery artifacts.

## Verification Checklist

- [ ] `wiki/candidates.md` exists for final delivery.
- [ ] Required headings are present.
- [ ] Candidates cite source change artifacts.
- [ ] Existing Wiki was checked before proposing official updates.
- [ ] Candidate content avoids guesses and secrets.
- [ ] Human Wiki Approval status is recorded.
- [ ] Formal Wiki was updated only after explicit human approval.
- [ ] If formal Wiki was updated, `.harness/wiki/index.md` and `.harness/wiki/log.md` were synchronized.
- [ ] If no durable knowledge exists, `none` and the reason are recorded.
