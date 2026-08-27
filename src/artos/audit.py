from __future__ import annotations

from pathlib import Path

from .utils import atomic_write_json, utc_now


def create_audit_template(run_dir: Path) -> tuple[Path, Path]:
    json_path = run_dir / "reviews" / "audit_findings.json"
    markdown_path = run_dir / "10_adversarial_audit.md"
    if not json_path.exists():
        atomic_write_json(json_path, {
            "schema_version": 1,
            "run_id": run_dir.name,
            "created_at": utc_now(),
            "auditor_session": None,
            "independence": {
                "separate_agent_session": True,
                "primary_interpretation_withheld_on_first_pass": True,
                "headline_results_independently_recomputed": [],
            },
            "checks": {
                "data_identity_and_versions": "not_checked",
                "sample_counts_and_filters": "not_checked",
                "time_space_units_and_sign": "not_checked",
                "leakage_and_circularity": "not_checked",
                "baselines_nulls_and_uncertainty": "not_checked",
                "table_figure_text_consistency": "not_checked",
            },
            "findings": [],
            "gate": "not_ready",
        })
    if not markdown_path.exists():
        markdown_path.write_text(
            "# Adversarial audit\n\n"
            "Status: **not checked**\n\n"
            "Do not label this work independently reproduced until the audit record identifies "
            "the independently recomputed results and methods.\n",
            encoding="utf-8",
        )
    return json_path, markdown_path
