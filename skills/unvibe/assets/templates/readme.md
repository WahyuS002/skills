# [<DIFFICULTY>] <PIECE_NAME>

**Source:** `<SOURCE_PATH>` -> `<SYMBOL>`

## Problem

<PROBLEM_DESCRIPTION>

## Examples

<EXAMPLES_BLOCK>

## Constraints

<CONSTRAINTS_LIST>

## Signature

```<LANG>
<SIGNATURE_BLOCK>
```

## How to run

The bundled `run.sh` knows your language. Common modes:

```
./run.sh                # all tests, verbose
./run.sh -q             # all tests, quiet
./run.sh --list         # numbered list of every test  (TS / Go runners)
./run.sh 3              # run test #3 from --list      (TS / Go, exact)
./run.sh <name>         # run by name pattern          (pytest ::, vitest -t, go -run)
./run.sh --help         # full usage + language notes
```

Prefer the numeric index for "run exactly this one test" — vitest `-t` and
`go test -run` are regex/substring matches and can over-fire. `pytest`
test names are real identifiers, so `./run.sh test_<name>` is already exact.
