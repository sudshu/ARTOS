from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .utils import atomic_write_json, sha256_file, utc_now


REPORT_FILES = {
    "08_execution_summary.md": "# Execution summary\n\nPending.\n",
    "09_results.md": "# Results\n\nPending validated results.\n",
    "11_reconciliation.md": "# Reconciliation\n\nPending audit reconciliation.\n",
    "12_final_summary.md": "# Final research summary\n\nPending.\n",
    "13_email_draft.md": "# Email draft\n\nPending. Do not send without explicit authorization.\n",
}


def create_report_skeleton(run_dir: Path) -> list[Path]:
    created: list[Path] = []
    for name, content in REPORT_FILES.items():
        path = run_dir / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(path)
    outline = run_dir / "deliverables" / "slides_outline.md"
    if not outline.exists():
        outline.write_text(
            "# ARTOS presentation outline\n\n"
            "1. Mother research question and decision context\n"
            "2. Trigger and source provenance\n"
            "3. Available data and compute\n"
            "4. Dataset products, versions, coverage, variables, and processing\n"
            "5. Methods and frozen analysis contract\n"
            "6. Hypothesis space and relationship to the mother question\n"
            "7. Independent ranking and selection\n"
            "8. Analyses performed\n"
            "9. Results\n"
            "10. Adversarial verification and repairs\n"
            "11. Limitations and unresolved questions\n"
            "12. Conclusions and next steps\n"
            "13. Technical appendix\n",
            encoding="utf-8",
        )
        created.append(outline)
    return created


def build_artifact_manifest(run_dir: Path, paths: Iterable[Path] | None = None) -> Path:
    if paths is None:
        candidates = [
            path for path in run_dir.rglob("*")
            if path.is_file() and path.name != "artifact_manifest.json"
        ]
    else:
        candidates = [path for path in paths if path.is_file()]
    entries = []
    for path in sorted(candidates):
        entries.append({
            "path": str(path.relative_to(run_dir)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    manifest = {
        "schema_version": 1,
        "run_id": run_dir.name,
        "generated_at": utc_now(),
        "artifacts": entries,
    }
    output = run_dir / "deliverables" / "artifact_manifest.json"
    atomic_write_json(output, manifest)
    return output
