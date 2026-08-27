"""ARTOS sessions interfaces.

Skeleton release: interfaces only; implementations arrive with the staged full release.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  (kept for signature defaults)
from typing import Any, Iterable  # noqa: F401

_SKELETON_NOTE = ("this component ships with the staged full release of ARTOS; the public skeleton provides interfaces only (see README: Availability)")


def launch_claude_session(root: Path, config: dict[str, Any], store: Store, run_id: str, role: str, prompt_path: Path, model: str | None=None) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)


def inspect_session(spec_path: Path) -> dict[str, Any]:
    raise NotImplementedError(_SKELETON_NOTE)
