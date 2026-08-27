# ARTOS implementation plan

## v0.1 — foundation

- Project-local `aro-*` skills and cross-agent entry instructions.
- SQLite run, event, resource, and session records.
- Compute snapshots and persistent data/artifact catalog exports.
- Email/question intake records and immutable source hashes.
- Direct, hybrid, and hypothesis state-machine branches.
- Blind ranking packets, deterministic ranking, and frozen contract hashes.
- Budget-locked Claude/tmux launcher, logs, status records, and human watch.
- Adversarial audit and reporting skeletons with artifact manifests.

Acceptance: pass unit tests, all skill validators, a disposable email-to-route
smoke test, and a fresh-agent forward test without external side effects.

## v0.2 — semantic inventory

- Extract NetCDF, HDF5, Zarr, GeoTIFF, Parquet, and checkpoint metadata.
- Group related files into dataset products instead of only file resources.
- Add temporal/spatial/variable catalog search and duplicate detection.
- Add acquisition receipts, licenses, quarantine validation, and lineage DAGs.
- Add incremental scan cursors so unchanged trees are not re-enumerated.

Acceptance: correctly identify version, variables, units, coverage, cadence,
resolution, and lineage for representative scientific datasets.

## v0.3 — research agent lifecycle

- Resolve and record the exact Claude model returned by each session.
- Support durable follow-ups and provider-session resume.
- Add heartbeat and stall classification independent of terminal output.
- Enforce role write isolation through permissions or disposable worktrees.
- Add CPU/GPU reservation, queueing, budget accounting, and recovery policies.

Acceptance: survive a killed tmux pane, resume from artifacts, and retain a
complete intervention and cost record.

## v0.4 — scientific verification

- Add domain-neutral evaluation-contract validation.
- Add independent numerical-reproduction task generation.
- Add statistical, leakage, circularity, sign/unit, and time-alignment checks.
- Add repair-round enforcement and audit gates in the controller.

Acceptance: detect seeded sign, unit, time-axis, sample-selection, and leakage
errors before finalization.

## v0.5 — presentation production

- Build PowerPoint from validated result tables and a reusable visual system.
- Render to PDF/images and inspect layout programmatically and visually.
- Cross-check slide numbers against machine-readable results.
- Add optional, separately authorized Drive upload and email-draft workflows.

Acceptance: generate a readable methods-before-results deck whose data versions,
claims, and audit status match the run manifest exactly.
