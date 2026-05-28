package <PACKAGE_NAME>

// Behavioral judge for <PIECE_NAME>.
// Every t.Errorf / t.Fatalf carries a case label + expected vs actual so a
// failure explains itself. Edge and failure cases live HERE only, not in the
// README.

import (
	"testing"
)

// recoverPanic catches a panic from an unimplemented stub so each test prints
// a clean failure line instead of a stack trace.
func recoverPanic(t *testing.T, label string) {
	t.Helper()
	if r := recover(); r != nil {
		t.Fatalf("%s: implementation panicked (likely unimplemented stub): %v", label, r)
	}
}

// --- happy path -----------------------------------------------------------

func Test<HappyScenario>(t *testing.T) {
	defer recoverPanic(t, "Test<HappyScenario>")
	got := <PIECE_NAME>(<args>)
	if got != <expected> {
		t.Errorf("Test<HappyScenario>: <case label>: expected %v, got %v", <expected>, got)
	}
}

// --- hidden edge case -----------------------------------------------------

func Test<EdgeScenario>(t *testing.T) {
	defer recoverPanic(t, "Test<EdgeScenario>")
	got := <PIECE_NAME>(<edge_args>)
	if got != <edge_expected> {
		t.Errorf("Test<EdgeScenario>: <edge case label>: expected %v, got %v", <edge_expected>, got)
	}
}
