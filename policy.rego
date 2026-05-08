package vaas.authz

import rego.v1

default allow := false

# Rule 1: Always allow 'read' operations
allow if {
    input.action == "read"
}

# Rule 2: Allow 'delete' ONLY in 'sandbox' environments
allow if {
    input.action == "delete"
    input.metadata.env == "sandbox"
}

# Rule 3: Kill Switch (Critical for AI Safety)
# Overrides all other rules if risk_score is too high
allow := false if {
    input.metadata.risk_score >= 10
}