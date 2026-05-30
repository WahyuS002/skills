#!/usr/bin/env bash
# Per-exercise runner for Go / `go test` exercises.
#
# Usage:
#   ./run.sh                         Run all tests (-v streams t.Log output)
#   ./run.sh -q                      Run all tests (no -v, summary only)
#   ./run.sh --list                  List tests with index numbers, then exit
#   ./run.sh -l                      Alias for --list
#   ./run.sh <N>                     Run test #N from --list (exact)
#   ./run.sh -q <N>                  Run test #N quietly
#   ./run.sh TestName                Run tests matching a regex (go test -run)
#   ./run.sh -h | --help             Show help and exit
#
# Why two ways to select a single test:
#   `go test -run` is a regex match. Go test names are normally identifiers
#   (TestFoo), so name-based selection works. But the numeric index resolves
#   to an anchored ^TestName$ regex — exact and safe from sibling-name
#   collisions (e.g. TestFoo also matches TestFooBar without anchors).
#
# Bash-3.2 safety:
#   Branches are written out explicitly so this script stays portable to
#   macOS bash 3.2 — empty arrays + "${ARGS[@]}" + `set -u` would error.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"; cd "$DIR"

show_help() {
  cat <<'EOF'
Per-exercise runner for Go / `go test` exercises.

Usage:
  ./run.sh                         Run all tests (-v streams t.Log)
  ./run.sh -q                      Run all tests (no -v, summary only)
  ./run.sh --list                  List tests with index numbers, then exit
  ./run.sh -l                      Alias for --list
  ./run.sh <N>                     Run test #N from --list (exact)
  ./run.sh -q <N>                  Run test #N quietly
  ./run.sh TestName                Run tests matching a regex (go test -run)
  ./run.sh -h | --help             Show this help

Recommended workflow for "run one specific test":
  1) ./run.sh --list      # numbered list of every Test* function
  2) ./run.sh 3           # run #3 — exact, anchored ^Name$

Notes:
  go test -run is a regex match. Without anchors, TestFoo also matches
  TestFooBar. The numeric index above passes an anchored ^TestName$
  pattern so a single specific test runs.
EOF
  exit 0
}

# List every Test* function name in the current package(s).
# `go test -list <regex>` returns one name per line plus a trailing line
# like "ok  <pkg> 0.001s" / "FAIL  <pkg>"; strip those so only Test names
# survive.
list_tests() {
  go test -list '.*' ./... 2>/dev/null | grep -E '^Test'
}

show_list() {
  local rows
  rows="$(list_tests)"
  if [ -z "$rows" ]; then
    echo "run.sh: no Test* functions found in $DIR" >&2
    exit 1
  fi
  echo "$rows" | awk '{ printf "  %2d) %s\n", NR, $0 }'
  exit 0
}

resolve_index() {
  list_tests | sed -n "${1}p"
}

# --- arg parsing ------------------------------------------------------------
case "${1:-}" in
  -h|--help) show_help ;;
  -l|--list) show_list ;;
esac

QUIET=0
[ "${1:-}" = "-q" ] && { QUIET=1; shift; }

SELECTOR="${1:-}"
TEST=""
if [ -n "$SELECTOR" ]; then
  if [[ "$SELECTOR" =~ ^[0-9]+$ ]]; then
    NAME="$(resolve_index "$SELECTOR")"
    if [ -z "$NAME" ]; then
      echo "run.sh: no test at index $SELECTOR — try './run.sh --list'" >&2
      exit 2
    fi
    TEST="^${NAME}$"   # anchored — exactly this test
  else
    TEST="$SELECTOR"
  fi
fi

# --- exec go test -----------------------------------------------------------
if [ "$QUIET" = 1 ]; then
  if [ -n "$TEST" ]; then exec go test -run "$TEST" ./...
  else                    exec go test ./...; fi
else
  if [ -n "$TEST" ]; then exec go test -v -run "$TEST" ./...
  else                    exec go test -v ./...; fi
fi
