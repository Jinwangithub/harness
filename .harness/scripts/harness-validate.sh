#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HARNESS="$ROOT/.harness"
FAILS=0
WARNS=0

pass() { printf 'PASS %s\n' "$1"; }
warn() { printf 'WARN %s\n' "$1"; WARNS=$((WARNS + 1)); }
fail() { printf 'FAIL %s\n' "$1"; FAILS=$((FAILS + 1)); }

require_file() {
  if [ -f "$1" ]; then
    pass "file exists: ${1#$ROOT/}"
  else
    fail "missing file: ${1#$ROOT/}"
  fi
}

require_dir() {
  if [ -d "$1" ]; then
    pass "directory exists: ${1#$ROOT/}"
  else
    fail "missing directory: ${1#$ROOT/}"
  fi
}

require_file "$HARNESS/AGENTS.md"
require_file "$HARNESS/agents/orchestrator.md"
require_file "$HARNESS/rules/02-development-workflow.md"
require_file "$HARNESS/rules/04-quality-gates.md"
require_file "$HARNESS/changes/README.md"
require_file "$HARNESS/changes/INDEX.md"
require_file "$HARNESS/memory/README.md"
require_file "$HARNESS/skills/README.md"
require_file "$HARNESS/wiki/README.md"
require_file "$HARNESS/USAGE.md"
require_file "$HARNESS/wiki/quickstart.md"
require_file "$HARNESS/wiki/minimal-example.md"
require_file "$HARNESS/skills/project/README.md"
require_dir "$HARNESS/changes"

INDEX="$HARNESS/changes/INDEX.md"
if [ -f "$INDEX" ]; then
  active_count=$(grep -E '^\| [^|]+ \| active \| auto-resume \|' "$INDEX" | wc -l | tr -d ' ')
  if [ "$active_count" = "1" ]; then
    pass "INDEX has exactly one active auto-resume change"
  else
    fail "INDEX active auto-resume count is $active_count"
  fi

  if grep -E '^\| [^|]+ \| legacy-(unfinished|conflict) \| auto-resume \|' "$INDEX" >/dev/null; then
    fail "legacy change is marked auto-resume in INDEX"
  else
    pass "legacy changes are not auto-resume"
  fi
else
  fail "INDEX checks skipped because INDEX is missing"
fi

running_count=0
for summary in "$HARNESS"/changes/*/summary.md; do
  [ -f "$summary" ] || continue
  if grep -E '^[-*] \*\*状态\*\*: 进行中' "$summary" >/dev/null; then
    running_count=$((running_count + 1))
  fi

  change_dir="$(basename "$(dirname "$summary")")"
  if grep -E 'approved-by-user-plan|not-required-by-policy-until-L4|pending user|approved-by-user' "$summary" >/dev/null; then
    case "$change_dir" in
      chore-harness-operability-index-validation-20260526)
        fail "new summary contains non-canonical Human Approval wording: $change_dir"
        ;;
      *)
        warn "legacy summary contains non-canonical Human Approval wording: $change_dir"
        ;;
    esac
  else
    pass "canonical Human Approval wording check: $change_dir"
  fi

  if grep -E '^[-*] \*\*resume_from\*\*:' "$summary" >/dev/null; then
    case "$change_dir" in
      chore-harness-operability-index-validation-20260526)
        fail "new summary uses deprecated resume_from: $change_dir"
        ;;
      *)
        warn "legacy summary uses deprecated resume_from: $change_dir"
        ;;
    esac
  fi

  if grep -E '^[-*] \*\*状态\*\*: 已完成' "$summary" >/dev/null && grep -E 'pending-human' "$summary" >/dev/null; then
    warn "legacy or manual review needed: completed summary has pending-human: $change_dir"
  fi
done

if [ "$running_count" -gt 1 ]; then
  if [ -f "$INDEX" ] && grep -E '^\| [^|]+ \| active \| auto-resume \|' "$INDEX" >/dev/null; then
    warn "multiple summaries are still 进行中 ($running_count); INDEX selects active change"
  else
    fail "multiple summaries are 进行中 ($running_count) and no INDEX active change exists"
  fi
else
  pass "multiple in-progress summary check"
fi

if [ -x "$HARNESS/scripts/harness-validate.sh" ]; then
  pass "validator script is executable"
else
  fail "validator script is not executable"
fi

# 检查1：skills/ 每个子目录（除 project/）都在 skills/README.md 中有对应行
SKILLS_README="$HARNESS/skills/README.md"
if [ -f "$SKILLS_README" ]; then
  for skill_dir in "$HARNESS"/skills/*/; do
    skill_name="$(basename "$skill_dir")"
    [ "$skill_name" = "project" ] && continue
    if grep -qF "$skill_name" "$SKILLS_README"; then
      pass "skill registered in README: $skill_name"
    else
      warn "skill directory not found in skills/README.md: $skill_name"
    fi
  done
else
  fail "skills/README.md missing, cannot verify skill registry"
fi

printf 'SUMMARY PASS/WARN/FAIL: warnings=%s failures=%s\n' "$WARNS" "$FAILS"
if [ "$FAILS" -gt 0 ]; then
  exit 1
fi
exit 0
