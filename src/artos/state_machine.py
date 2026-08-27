from __future__ import annotations


TERMINAL_STATES = {"complete", "failed", "cancelled"}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "intake_created": {"inventory_ready", "failed", "cancelled"},
    "inventory_ready": {"oriented", "failed", "cancelled"},
    "oriented": {"routed_direct", "routed_hybrid", "routed_hypothesis", "failed", "cancelled"},
    "routed_direct": {"audit_running", "reporting", "failed", "cancelled"},
    "routed_hybrid": {"hypotheses_ranked", "failed", "cancelled"},
    "routed_hypothesis": {"hypotheses_ranked", "failed", "cancelled"},
    "hypotheses_ranked": {"contract_frozen", "failed", "cancelled"},
    "contract_frozen": {"primary_running", "failed", "cancelled"},
    "primary_running": {"primary_complete", "failed", "cancelled"},
    "primary_complete": {"audit_running", "failed", "cancelled"},
    "audit_running": {"audit_complete", "repair_required", "failed", "cancelled"},
    "audit_complete": {"reconciled", "reporting", "failed", "cancelled"},
    "repair_required": {"primary_running", "failed", "cancelled"},
    "reconciled": {"reporting", "failed", "cancelled"},
    "reporting": {"complete", "repair_required", "failed", "cancelled"},
    "complete": set(),
    "failed": set(),
    "cancelled": set(),
}


def validate_transition(current: str, requested: str) -> None:
    if requested not in ALLOWED_TRANSITIONS.get(current, set()):
        allowed = ", ".join(sorted(ALLOWED_TRANSITIONS.get(current, set()))) or "none"
        raise ValueError(f"Invalid transition {current!r} -> {requested!r}; allowed: {allowed}")
