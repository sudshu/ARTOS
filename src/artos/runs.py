"""ARTOS runs interfaces.

Skeleton release: interfaces only; implementations arrive with the staged full release.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  (kept for signature defaults)
from typing import Any, Iterable  # noqa: F401

_SKELETON_NOTE = ("this component ships with the staged full release of ARTOS; the public skeleton provides interfaces only (see README: Availability)")


def create_run(store: Store, projects_dir: Path, source_text: str, source_type: str, project_name: str | None=None, title: str | None=None) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)


def snapshot_inventories(run_dir: Path, state_dir: Path) -> list[str]:
    raise NotImplementedError(_SKELETON_NOTE)


def freeze_contract(store: Store, run_id: str, contract_path: Path) -> str:
    raise NotImplementedError(_SKELETON_NOTE)
