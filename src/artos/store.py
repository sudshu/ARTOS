"""ARTOS store interfaces.

Skeleton release: interfaces only; implementations arrive with the staged full release.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  (kept for signature defaults)
from typing import Any, Iterable  # noqa: F401

_SKELETON_NOTE = ("this component ships with the staged full release of ARTOS; the public skeleton provides interfaces only (see README: Availability)")


class Store:
    def __init__(self, path: Path):
        raise NotImplementedError(_SKELETON_NOTE)

    def close(self) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def __enter__(self) -> 'Store':
        raise NotImplementedError(_SKELETON_NOTE)

    def __exit__(self, *_: object) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def create_run(self, record: dict[str, Any]) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def get_run(self, run_id: str) -> dict[str, Any]:
        raise NotImplementedError(_SKELETON_NOTE)

    def list_runs(self, limit: int=25) -> list[dict[str, Any]]:
        raise NotImplementedError(_SKELETON_NOTE)

    def transition(self, run_id: str, requested: str, payload: dict[str, Any] | None=None) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def record_event(self, event_type: str, payload: dict[str, Any], run_id: str | None=None) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def upsert_resource(self, resource: dict[str, Any]) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def list_resources(self, kinds: Iterable[str] | None=None) -> list[dict[str, Any]]:
        raise NotImplementedError(_SKELETON_NOTE)

    def record_session(self, session: dict[str, Any]) -> None:
        raise NotImplementedError(_SKELETON_NOTE)

    def sessions_for_run(self, run_id: str) -> list[dict[str, Any]]:
        raise NotImplementedError(_SKELETON_NOTE)
