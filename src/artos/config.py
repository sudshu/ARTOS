from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any


CONFIG_NAME = "artos.json"


def find_root(start: Path | None = None) -> Path:
    configured = os.environ.get("ARTOS_PROJECT_ROOT")
    if configured:
        root = Path(configured).expanduser().resolve()
        if not (root / CONFIG_NAME).is_file():
            raise FileNotFoundError(f"ARTOS_PROJECT_ROOT has no {CONFIG_NAME}: {root}")
        return root

    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / CONFIG_NAME).is_file():
            return candidate
    raise FileNotFoundError(f"Could not find {CONFIG_NAME} from {current}")


def load_config(root: Path) -> dict[str, Any]:
    with (root / CONFIG_NAME).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def configured_path(root: Path, config: dict[str, Any], section: str, key: str) -> Path:
    raw = config[section][key]
    path = Path(raw).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def state_dir(root: Path, config: dict[str, Any]) -> Path:
    return configured_path(root, config, "project", "state_dir")


def projects_dir(root: Path, config: dict[str, Any]) -> Path:
    return configured_path(root, config, "project", "projects_dir")
