"""Behavioral judge for <PIECE_NAME>.

These tests are the spec. Every assertion carries a descriptive message
(case label + expected vs actual) so a failure explains itself without
needing -s / print statements. Edge and failure cases live here only,
NOT in the README.
"""

import pytest

from exercise import <PIECE_NAME>


# --- happy path -------------------------------------------------------------

def test_<happy_scenario>():
    got = <PIECE_NAME>(<args>)
    assert got == <expected>, (
        f"<case label>: expected <expected_repr>, got {got!r}"
    )


# --- hidden edge case -------------------------------------------------------

def test_<edge_scenario>():
    got = <PIECE_NAME>(<edge_args>)
    assert got == <edge_expected>, (
        f"<edge case label>: expected <edge_expected_repr>, got {got!r}"
    )


# --- hidden failure case ----------------------------------------------------

def test_<failure_scenario>_raises():
    with pytest.raises(<ErrorType>):
        <PIECE_NAME>(<bad_args>)
