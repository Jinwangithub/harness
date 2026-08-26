---
title: {系统名称}
kind: integration
domain: {domain-name}
modules:
  - {src/path}
integrations:
  - {system-id}
tags:
  - integration
status: approved
updated: {YYYY-MM-DD}
sources:
  - change_id: {change-id}
    evidence: {artifact path#section}
approval:
  log_ref: .harness/wiki/log.md#{stable-decision-id}
---

# {系统名称}

## Contract
- Protocol: {confirmed protocol}
- Data contract: {confirmed schema}
- Failure semantics: {confirmed timeout/retry/degradation behavior}

## Business impact
- `RULE-{DOMAIN}-001`: {confirmed dependency rule}

## Security
- {no secrets; approved authentication contract summary}
