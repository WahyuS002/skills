/**
 * Behavioral judge for <PIECE_NAME>.
 *
 * Every expect() carries a 2nd-argument message with case label + expected vs
 * actual so a failure explains itself. Edge and failure cases live HERE only,
 * not in the README.
 */

import { describe, it, expect } from "vitest";
import { <PIECE_NAME> } from "./exercise";

describe("<PIECE_NAME> — happy path", () => {
  it("<happy scenario description>", () => {
    const got = <PIECE_NAME>(<args>);
    expect(
      got,
      `<case label>: expected <expected_repr>, got ${JSON.stringify(got)}`,
    ).toEqual(<expected>);
  });
});

describe("<PIECE_NAME> — hidden edge cases", () => {
  it("<edge case description>", () => {
    const got = <PIECE_NAME>(<edge_args>);
    expect(
      got,
      `<edge case label>: expected <edge_expected_repr>, got ${JSON.stringify(got)}`,
    ).toEqual(<edge_expected>);
  });
});

describe("<PIECE_NAME> — hidden failure cases", () => {
  it("<failure scenario description>", () => {
    expect(
      () => <PIECE_NAME>(<bad_args>),
      "<failure case label>: must return a structured failure, must not throw",
    ).not.toThrow();
  });
});
