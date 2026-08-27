"""ARTOS session_worker interfaces.

Skeleton release: interfaces only; implementations arrive with the staged full release.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  (kept for signature defaults)
from typing import Any, Iterable  # noqa: F401

_SKELETON_NOTE = ("this component ships with the staged full release of ARTOS; the public skeleton provides interfaces only (see README: Availability)")


def run(spec_path: Path) -> int:
    raise NotImplementedError(_SKELETON_NOTE)


def main(argv: list[str] | None=None) -> int:
    raise NotImplementedError(_SKELETON_NOTE)
