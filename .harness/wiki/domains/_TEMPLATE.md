---
title: {业务域名称}
kind: domain
domain: {domain-name}
modules:
  - {src/path}
integrations:
  - {system-id}
tags:
  - {tag}
status: approved
updated: {YYYY-MM-DD}
sources:
  - change_id: {change-id}
    evidence: {artifact path#section}
approval:
  log_ref: .harness/wiki/log.md#{stable-decision-id}
---

# {业务域名称}

## Rules
- `RULE-{DOMAIN}-001`: {confirmed business rule}

## Terms and invariants
| Term / invariant | Definition | Source rule |
|---|---|---|
| {term} | {confirmed definition} | `RULE-{DOMAIN}-001` |

## State machine
{confirmed states and transitions}

## Superseded rules
- {none or stable rule IDs with deprecation reason}
