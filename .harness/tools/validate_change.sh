#!/bin/sh
set -u

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" 2>/dev/null && pwd -P)
PY_VALIDATOR="$SCRIPT_DIR/validate_change.py"

if command -v python3 >/dev/null 2>&1; then
    if [ -f "$PY_VALIDATOR" ]; then
        exec python3 "$PY_VALIDATOR" "$@"
    fi
    echo "FAIL: validator.python_missing: Missing full validator: $PY_VALIDATOR"
    echo "FAIL: 1 failure(s), 0 warning(s)."
    exit 1
fi

fail_count=0
warn_count=0
issues=""

add_issue() {
    level=$1
    code=$2
    message=$3
    issues=${issues}${level}': '${code}': '${message}'
'
    if [ "$level" = "FAIL" ]; then
        fail_count=$((fail_count + 1))
    else
        warn_count=$((warn_count + 1))
    fi
}

fail() {
    add_issue "FAIL" "$1" "$2"
}

warn() {
    add_issue "WARN" "$1" "$2"
}

print_report() {
    if [ "$fail_count" -eq 0 ] && [ "$warn_count" -eq 0 ]; then
        echo "PASS: Harness changes validation passed."
        return
    fi
    printf '%s' "$issues"
    if [ "$fail_count" -gt 0 ]; then
        echo "FAIL: $fail_count failure(s), $warn_count warning(s)."
    else
        echo "PASS: 0 failure(s), $warn_count warning(s)."
    fi
}

repo_arg=""
change_arg=""
all_arg=0

while [ "$#" -gt 0 ]; do
    case "$1" in
        --repo)
            if [ "$#" -lt 2 ]; then
                fail "args.missing_value" "Missing value for --repo"
                break
            fi
            repo_arg=$2
            shift 2
            ;;
        --repo=*)
            repo_arg=${1#--repo=}
            shift
            ;;
        --change)
            if [ "$#" -lt 2 ]; then
                fail "args.missing_value" "Missing value for --change"
                break
            fi
            change_arg=$2
            shift 2
            ;;
        --change=*)
            change_arg=${1#--change=}
            shift
            ;;
        --all)
            all_arg=1
            shift
            ;;
        *)
            fail "args.unknown" "Unknown fallback option: $1"
            shift
            ;;
    esac
done

warn "fallback.reduced" "python3 unavailable; running reduced POSIX shell validation only. Full validator is .harness/tools/validate_change.py."

find_repo_root() {
    current=$1
    while :; do
        if [ -f "$current/.harness/changes/INDEX.md" ]; then
            printf '%s\n' "$current"
            return 0
        fi
        parent=$(dirname "$current")
        if [ "$parent" = "$current" ]; then
            printf '%s\n' "$1"
            return 0
        fi
        current=$parent
    done
}

if [ -n "$repo_arg" ]; then
    repo_root=$(CDPATH= cd "$repo_arg" 2>/dev/null && pwd -P)
    if [ -z "${repo_root:-}" ]; then
        repo_root=$repo_arg
        fail "repo.invalid" "Repository path is not accessible: $repo_arg"
    fi
else
    cwd=$(pwd -P)
    repo_root=$(find_repo_root "$cwd")
fi

harness_dir="$repo_root/.harness"
changes_dir="$harness_dir/changes"
index_path="$changes_dir/INDEX.md"

if [ ! -f "$index_path" ]; then
    fail "index.missing" "Missing registry: $index_path"
fi
if [ ! -f "$harness_dir/tools/validate_change.py" ]; then
    fail "validator.python_missing" "Missing full validator: $harness_dir/tools/validate_change.py"
fi

change_name_valid() {
    printf '%s\n' "$1" | awk '
        /^(feat|fix|refactor|perf|test|docs|chore)-[a-z0-9][a-z0-9-]*-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$/ { valid=1 }
        END { exit !valid }
    '
}

entries=""
active_count=0

if [ -f "$index_path" ]; then
    while IFS= read -r line; do
        case "$line" in
            \|*Change*\|*|\|*---*\|*|'')
                continue
                ;;
            \|*)
                trimmed=$(printf '%s\n' "$line" | awk '{$1=$1; print}')
                cols=$(printf '%s\n' "$trimmed" | awk -F'|' '{print NF-1}')
                if [ "$cols" -ne 5 ]; then
                    fail "index.row_malformed" "Malformed INDEX row: $trimmed"
                    continue
                fi
                change=$(printf '%s\n' "$trimmed" | awk -F'|' '{gsub(/^[ `]+|[ `]+$/, "", $2); print $2}')
                status=$(printf '%s\n' "$trimmed" | awk -F'|' '{gsub(/^[ `]+|[ `]+$/, "", $3); print $3}')
                case "$status" in
                    active|done|abandoned) ;;
                    *) fail "index.status_invalid" "$change: invalid status \`$status\`" ;;
                esac
                if [ "$status" = "active" ]; then
                    active_count=$((active_count + 1))
                fi
                if ! change_name_valid "$change"; then
                    fail "change.name_invalid" "$change: expected {type}-{name}-YYYYMMDD"
                fi
                if [ ! -d "$changes_dir/$change" ]; then
                    fail "change.dir_missing" "$change: directory listed in INDEX.md does not exist"
                fi
                resume_point=$(printf '%s\n' "$trimmed" | awk -F'|' '{gsub(/^[ `]+|[ `]+$/, "", $4); print $4}')
                entries=${entries}${change}'|'${status}'|'${resume_point}'
'
                ;;
        esac
    done < "$index_path"
fi

if [ "$active_count" -gt 1 ]; then
    fail "index.multiple_active" "INDEX.md has $active_count active changes; at most one is allowed"
fi

extract_summary_field() {
    file=$1
    field=$2
    awk -v field="$field" '
        $0 ~ "^- \\*\\*" field "\\*\\*:" {
            sub("^- \\*\\*" field "\\*\\*: *", "")
            gsub(/^`+|`+$/, "")
            print
            exit
        }
    ' "$file"
}

has_gate_record() {
    grep -E '^## Gate Record[[:space:]]*[—-]' "$1" >/dev/null 2>&1
}

final_gate_value() {
    file=$1
    field=$2
    awk -v field="$field" '
        /^## Gate Record[[:space:]]*[—-]/ { in_final=1; value=""; next }
        in_final && $0 ~ "^[[:space:]]*-[[:space:]]*" field ":" {
            line=$0
            sub("^[[:space:]]*-[[:space:]]*" field ":[[:space:]]*", "", line)
            gsub(/^`+|`+$/, "", line)
            value=line
        }
        END { print value }
    ' "$file"
}

validate_change_dir() {
    change=$1
    index_status=$2
    index_resume=$3
    change_dir="$changes_dir/$change"
    summary_path="$change_dir/summary.md"

    if [ ! -d "$change_dir" ]; then
        return
    fi
    if ! change_name_valid "$change"; then
        fail "change.name_invalid" "$change: expected {type}-{name}-YYYYMMDD"
    fi
    if [ ! -f "$summary_path" ]; then
        fail "summary.missing" "$change: missing summary.md"
        return
    fi

    for field in "需求" "类型" "日期" "状态" "Flow" "Current step" "Resume point"; do
        value=$(extract_summary_field "$summary_path" "$field")
        if [ -z "$value" ]; then
            fail "summary.field_missing" "$change: missing summary field \`$field\`"
        fi
    done

    summary_status=$(extract_summary_field "$summary_path" "状态")
    summary_resume=$(extract_summary_field "$summary_path" "Resume point")
    flow=$(extract_summary_field "$summary_path" "Flow")

    if [ -n "$summary_status" ]; then
        case "$summary_status" in
            active|done|abandoned) ;;
            *) fail "summary.status_invalid" "$change: invalid summary status \`$summary_status\`" ;;
        esac
    fi
    if [ -n "$index_status" ] && [ -n "$summary_status" ] && [ "$summary_status" != "$index_status" ]; then
        fail "summary.index_status_mismatch" "$change: summary status \`$summary_status\` differs from INDEX status \`$index_status\`"
    fi
    if [ -n "$summary_resume" ] && [ -n "$index_resume" ] && [ "$summary_resume" != "$index_resume" ]; then
        fail "summary.index_resume_mismatch" "$change: summary Resume point \`$summary_resume\` differs from INDEX \`$index_resume\`"
    fi
    if [ "$summary_status" = "done" ] && [ "$summary_resume" != "none" ]; then
        fail "summary.done_resume_not_none" "$change: done summary requires Resume point \`none\`, got \`$summary_resume\`"
    fi
    if [ "$index_status" = "done" ] && [ "$index_resume" != "none" ]; then
        fail "index.done_resume_not_none" "$change: done INDEX entry requires Resume point \`none\`, got \`$index_resume\`"
    fi
    if [ -n "$flow" ]; then
        case "$flow" in
            Lite-flow|Standard-flow) ;;
            *) fail "summary.flow_invalid" "$change: invalid Flow \`$flow\`" ;;
        esac
    fi

    if [ "$summary_status" = "done" ] && ! has_gate_record "$summary_path"; then
        fail "gate.none" "$change: done change requires at least one Gate Record"
    elif [ "$summary_status" = "active" ] && ! has_gate_record "$summary_path"; then
        warn "gate.none" "$change: no Gate Record found yet"
    fi

    if has_gate_record "$summary_path"; then
        final_mechanical=$(final_gate_value "$summary_path" "Mechanical Gate")
        final_human=$(final_gate_value "$summary_path" "Human Approval")
        case "$final_mechanical" in
            pass|fail|blocked) ;;
            *) fail "gate.mechanical_invalid" "$change: invalid final Mechanical Gate \`$final_mechanical\`" ;;
        esac
        case "$final_human" in
            approved|rejected|pending) ;;
            *) fail "gate.human_invalid" "$change: invalid final Human Approval \`$final_human\`" ;;
        esac
        if [ "$summary_status" = "done" ] && [ "$final_mechanical" != "pass" ]; then
            fail "gate.final_mechanical_not_pass" "$change: done change requires final Mechanical Gate \`pass\`, got \`$final_mechanical\`"
        fi
        if [ "$summary_status" = "done" ] && [ "$final_human" != "approved" ]; then
            fail "gate.final_approval_not_approved" "$change: done change requires final Human Approval \`approved\`, got \`$final_human\`"
        fi
        if [ "$summary_status" = "done" ] && { [ "$final_human" = "pending" ] || [ "$final_human" = "rejected" ]; }; then
            fail "gate.final_approval_done_conflict" "$change: done change cannot have final Human Approval \`$final_human\`"
        fi
    fi
}

listed_change_found=0
selected_count=0

if [ -n "$change_arg" ]; then
    old_ifs=$IFS
    IFS='
'
    for entry in $entries; do
        IFS=$old_ifs
        change=${entry%%|*}
        remainder=${entry#*|}
        status=${remainder%%|*}
        resume_point=${remainder#*|}
        if [ "$change" = "$change_arg" ]; then
            listed_change_found=1
            selected_count=$((selected_count + 1))
            validate_change_dir "$change" "$status" "$resume_point"
        fi
        IFS='
'
    done
    IFS=$old_ifs
    if [ "$listed_change_found" -eq 0 ]; then
        fail "change.not_in_index" "Change is not listed in INDEX.md: $change_arg"
    fi
else
    old_ifs=$IFS
    IFS='
'
    for entry in $entries; do
        IFS=$old_ifs
        change=${entry%%|*}
        remainder=${entry#*|}
        status=${remainder%%|*}
        resume_point=${remainder#*|}
        if [ "$all_arg" -eq 1 ] || [ "$status" = "active" ]; then
            selected_count=$((selected_count + 1))
            validate_change_dir "$change" "$status" "$resume_point"
        fi
        IFS='
'
    done
    IFS=$old_ifs
    if [ "$selected_count" -eq 0 ] && [ "$all_arg" -eq 0 ]; then
        warn "index.no_active" "No active change in INDEX.md; registry is idle."
    fi
fi

print_report
if [ "$fail_count" -gt 0 ]; then
    exit 1
fi
exit 0
