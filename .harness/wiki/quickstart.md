# Wiki Quickstart

This repository is a Harness governance template. It does not define real business rules. Business projects that adopt Harness must fill the minimum wiki path before asking Orchestrator to make business-rule decisions.

## Minimum Fill Path

1. Create or update `.harness/wiki/project-overview.md`.
2. Fill only facts that are known.
3. Mark unknown business rules as `{待确认}`.
4. If a requirement depends on `{待确认}`, record it in Phase 1 `Open Questions` instead of guessing.
5. Add domain or integration pages only when they are needed by current work.

## Minimum `project-overview.md` Fields

```markdown
# Project Overview

## Project
- Name: {项目名或待确认}
- Purpose: {项目目标或待确认}

## Tech Stack
- Runtime: {语言/框架或待确认}
- Build command: {命令或待确认}
- Test command: {命令或待确认}

## Boundaries
- In scope modules: {列表或待确认}
- Out of scope modules: {列表或待确认}

## Business Domains
- {领域名}: {一句话说明或待确认}

## External Dependencies
- {系统名}: {用途、接口、环境或待确认}

## Rules That Must Not Be Guessed
- {规则}: {待确认}
```

## Orchestrator Rule

When a business concept is missing or marked `{待确认}`, Orchestrator must either ask the user in Phase 1 or record the uncertainty in Open Questions. It must not invent domain facts to unblock implementation.
