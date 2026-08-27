"""ARTOS inventory interfaces.

Skeleton release: interfaces only; implementations arrive with the staged full release.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  (kept for signature defaults)
from typing import Any, Iterable  # noqa: F401

_SKELETON_NOTE = ("this component ships with the staged full release of ARTOS; the public skeleton provides interfaces only (see README: Availability)")


def refresh_compute(root: Path, state_dir: Path) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)


def register_path(store: Store, path: Path, hash_limit_mb: int=64, max_files: int=250000, kind: str | None=None, verify_content: bool=True) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)


def discover_paths(root: Path, max_files: int) -> Iterator[tuple[Path, str]]:
    raise NotImplementedError(_SKELETON_NOTE)


def refresh_data_catalog(store: Store, state_dir: Path, roots: list[Path], max_files: int, hash_limit_mb: int) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)


def export_catalog(store: Store, state_dir: Path) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)
