#!/usr/bin/env bash
# Per-exercise runner for TypeScript / vitest exercises.
#
# Usage:
#   ./run.sh                         Run all tests (verbose reporter)
#   ./run.sh -q                      Run all tests (default reporter, quiet)
#   ./run.sh --list                  List tests with index numbers, then exit
#   ./run.sh -l                      Alias for --list
#   ./run.sh <N>                     Run test #N from --list (exact)
#   ./run.sh -q <N>                  Run test #N quietly
#   ./run.sh "<name pattern>"        Run tests by name (vitest -t, substring)
#   ./run.sh -h | --help             Show help and exit
#
# Why two ways to select a single test:
#   vitest -t is a regex/substring match against the it() description, not
#   an exact-name lookup. For one specific test, prefer the numeric index
#   (./run.sh 3) — it is exact and immune to substring over-matching.
#   The "<name pattern>" form stays for power use (regex, fuzzy match).
#
# Quoting reminder:
#   Multi-word name patterns MUST be quoted. Unquoted, bash splits them
#   into separate args and only the first reaches vitest as a -t arg.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_FILE="$DIR/exercise.test.ts"

show_help() {
  cat <<'EOF'
Per-exercise runner for TypeScript / vitest exercises.

Usage:
  ./run.sh                         Run all tests (verbose reporter)
  ./run.sh -q                      Run all tests (default reporter, quiet)
  ./run.sh --list                  List tests with index numbers, then exit
  ./run.sh -l                      Alias for --list
  ./run.sh <N>                     Run test #N from --list (exact)
  ./run.sh -q <N>                  Run test #N quietly
  ./run.sh "<name pattern>"        Run tests by name (vitest -t, substring)
  ./run.sh -h | --help             Show this help

Recommended workflow for "run one specific test":
  1) ./run.sh --list      # see numbered list of every it()
  2) ./run.sh 3           # run #3 — exact, no substring guessing

Notes:
  vitest -t is a SUBSTRING/regex match — it will run every test whose name
  contains the pattern. For exact selection, use the numeric index above.
  Multi-word name patterns MUST be quoted, e.g.:
      ./run.sh "applies a single delta at step 1"
EOF
  exit 0
}

# List every it(...) / test(...) name from the exercise's test file.
# Handles both single- and double-quoted names. One name per line.
list_tests() {
  if [ ! -f "$TEST_FILE" ]; then
    echo "run.sh: test file not found: $TEST_FILE" >&2
    return 1
  fi
  grep -nE "^[[:space:]]*(it|test)\([\"']" "$TEST_FILE" \
    | sed -E "s/^[0-9]+:[[:space:]]*(it|test)\([\"']([^\"']+)[\"'].*/\2/"
}

show_list() {
  local rows
  rows="$(list_tests)" || exit 1
  if [ -z "$rows" ]; then
    echo "run.sh: no it() / test() declarations found in $TEST_FILE" >&2
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
    TEST="$(resolve_index "$SELECTOR")"
    if [ -z "$TEST" ]; then
      echo "run.sh: no test at index $SELECTOR — try './run.sh --list'" >&2
      exit 2
    fi
  else
    TEST="$SELECTOR"
  fi
fi

# --- exec vitest ------------------------------------------------------------
ARGS=(run "$TEST_FILE")
[ -n "$TEST" ] && ARGS+=(-t "$TEST")
if [ "$QUIET" = 1 ]; then
  exec npx vitest "${ARGS[@]}"
else
  exec npx vitest "${ARGS[@]}" --reporter verbose
fi
