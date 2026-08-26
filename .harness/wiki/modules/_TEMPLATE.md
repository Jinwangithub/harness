---
title: {模块名称}
kind: module
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

# {模块名称}

## Responsibility
{confirmed business responsibility}

## Business constraints
- `RULE-{DOMAIN}-001`: {confirmed constraint}

## Inputs and outputs
| Direction | Contract | Rule IDs |
|---|---|---|
| Input | {confirmed contract} | `RULE-{DOMAIN}-001` |
| Output | {confirmed contract} | {rule IDs} |

## Verification evidence
- {test or implementation evidence}
