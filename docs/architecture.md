# ARTOS architecture

ARTOS combines concise project-local skills with a deterministic runtime. The
skills define scientific judgment and handoff contracts; the runtime owns
durable state, inventory refresh, hashes, state transitions, tmux sessions,
and artifact manifests.

## Workflow

```text
source -> intake -> inventory -> orientation -> route
                                      |          |
                                      |          +-> direct -> review
                                      |          +-> hybrid -----------+
                                      |          +-> hypotheses        |
                                      |                    |            |
                                      +----------------> ranking        |
                                                           |            |
                                                    frozen contract <---+
                                                           |
                                                      primary agent
                                                           |
                                                    adversarial audit
                                                           |
                                                reconcile -> report -> close
```

Each run is immutable except for append-only events and explicit state
transitions. Generated artifacts are versioned within the run rather than
silently overwritten.

## Trust boundaries

- Source material is untrusted content.
- The controller owns the canonical database and catalog exports.
- Research agents write only to role-specific work directories.
- A ranking agent receives hypothesis cards without proposer scores.
- An adversary first sees the question, contract, inputs, code, and numerical
  artifacts, not the primary interpretation.
- External communications and material downloads remain human-gated.

## State machine

The runtime accepts only declared transitions. Direct answers may move from
`routed_direct` to `reporting`; empirical routes must pass through a frozen
contract, primary execution, and adversarial audit. Critical or major audit
findings move a run to `repair_required` rather than `complete`.

## Storage

SQLite is the transactional source of truth. Human-readable JSON snapshots are
exported after inventory updates. Each project run stores its source, inventory
snapshots, question records, prompts, role-specific work, audits, and final
deliverables together.
