#!/usr/bin/env bash
# Per-exercise runner for Go / `go test` exercises.
# Branches written out explicitly so the script stays safe under macOS
# bash 3.2 + `set -u` (an empty array + "${ARGS[@]}" would error there).
# Usage:
#   ./run.sh                  # all tests, verbose (-v streams t.Log)
#   ./run.sh <TestName>       # one test function, verbose
#   ./run.sh -q               # all tests, quiet summary
#   ./run.sh -q <TestName>    # one test function, quiet
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"; cd "$DIR"
QUIET=0; [ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
if [ "$QUIET" = 1 ]; then
  if [ -n "$TEST" ]; then exec go test -run "$TEST" ./...
  else                    exec go test ./...; fi
else
  if [ -n "$TEST" ]; then exec go test -v -run "$TEST" ./...
  else                    exec go test -v ./...; fi
fi
