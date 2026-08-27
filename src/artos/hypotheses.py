"""ARTOS hypotheses interfaces.

Skeleton release: interfaces only; implementations arrive with the staged full release.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  (kept for signature defaults)
from typing import Any, Iterable  # noqa: F401

_SKELETON_NOTE = ("this component ships with the staged full release of ARTOS; the public skeleton provides interfaces only (see README: Availability)")


def create_hypothesis_template(run_dir: Path, count: int=10) -> Path:
    raise NotImplementedError(_SKELETON_NOTE)


def create_blind_ranking_packet(hypotheses_path: Path, seed: int=20260816) -> Path:
    raise NotImplementedError(_SKELETON_NOTE)


def aggregate_judge_panel(packet_path: Path, judge_paths: list[Path], output_path: Path, minimum_judges: int=4, minimum_codex_judges: int=2) -> Path:
    """Aggregate isolated judge files into one deterministically scored packet.

General judges score every criterion except novelty. Exactly one local-novelty
judge supplies the novelty score and evidence of prior local runs."""
    raise NotImplementedError(_SKELETON_NOTE)


def rank_scored_hypotheses(scored_path: Path, output_dir: Path) -> tuple[Path, Path]:
    raise NotImplementedError(_SKELETON_NOTE)
