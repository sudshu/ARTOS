from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from . import __version__
from .audit import create_audit_template
from .config import find_root, load_config, projects_dir, state_dir
from .hypotheses import (
    aggregate_judge_panel,
    create_blind_ranking_packet,
    create_hypothesis_template,
    rank_scored_hypotheses,
)
from .inventory import export_catalog, refresh_compute, refresh_data_catalog, register_path
from .reporting import build_artifact_manifest, create_report_skeleton
from .runs import create_run, freeze_contract, snapshot_inventories
from .sessions import inspect_session, launch_claude_session
from .store import Store


def _json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _context(args: argparse.Namespace) -> tuple[Path, dict[str, Any], Path, Path]:
    root = find_root(args.root)
    config = load_config(root)
    state = state_dir(root, config)
    projects = projects_dir(root, config)
    state.mkdir(parents=True, exist_ok=True)
    projects.mkdir(parents=True, exist_ok=True)
    return root, config, state, projects


def _stale(path: Path, ttl_hours: float) -> bool:
    if not path.exists():
        return True
    return (time.time() - path.stat().st_mtime) > ttl_hours * 3600


def _configured_roots(root: Path, values: list[str]) -> list[Path]:
    paths = []
    for value in values:
        path = Path(value).expanduser()
        paths.append(path if path.is_absolute() else root / path)
    return paths


def _ensure_inventories(
    root: Path, config: dict[str, Any], state: Path, store: Store
) -> dict[str, Any]:
    inventory = config["inventory"]
    refreshed: dict[str, Any] = {}
    compute_latest = state / "compute" / "latest.json"
    if _stale(compute_latest, float(inventory["compute_ttl_hours"])):
        refreshed["compute"] = refresh_compute(root, state)
    data_last_scan = state / "data" / "last_scan.json"
    if _stale(data_last_scan, float(inventory["data_incremental_ttl_hours"])):
        configured = list(inventory.get("data_roots", [])) + list(
            inventory.get("artifact_roots", [])
        )
        roots = _configured_roots(root, list(dict.fromkeys(configured)))
        refreshed["data"] = refresh_data_catalog(
            store, state, roots,
            int(inventory["max_scan_files"]), int(inventory["hash_file_limit_mb"]),
        )
    elif not (state / "data" / "catalog.json").exists():
        refreshed["catalog"] = export_catalog(store, state)
    return refreshed


def cmd_doctor(args: argparse.Namespace) -> int:
    root, config, state, projects = _context(args)
    checks = {
        "artos_version": __version__,
        "root": str(root),
        "configuration": str(root / "artos.json"),
        "state_dir": str(state),
        "projects_dir": str(projects),
        "python": {"path": sys.executable, "version": sys.version.split()[0]},
        "tmux": {"path": shutil.which("tmux")},
        "claude": {"path": shutil.which("claude")},
        "configured_models": {
            role: config["agents"][f"{role}_model"] for role in ("ranker", "primary", "adversary")
        },
        "allow_model_fallback": bool(config["agents"].get("allow_model_fallback", False)),
    }
    for tool in ("tmux", "claude"):
        path = checks[tool]["path"]
        if path:
            command = [path, "-V"] if tool == "tmux" else [path, "--version"]
            result = subprocess.run(command, capture_output=True, text=True, timeout=8, check=False)
            checks[tool]["version"] = (result.stdout or result.stderr).strip()
            checks[tool]["ok"] = result.returncode == 0
        else:
            checks[tool]["ok"] = False
    checks["ok"] = bool(checks["tmux"]["ok"] and checks["claude"]["ok"])
    _json(checks)
    return 0 if checks["ok"] else 1


def cmd_inventory_refresh(args: argparse.Namespace) -> int:
    root, config, state, _ = _context(args)
    inventory = config["inventory"]
    with Store(state / "artos.sqlite") as store:
        result: dict[str, Any] = {}
        run_compute = args.compute or not args.data_root
        if run_compute:
            result["compute"] = refresh_compute(root, state)
        if args.data_root is not None:
            roots = [Path(value) for value in args.data_root]
            if not roots:
                configured = list(inventory.get("data_roots", [])) + list(
                    inventory.get("artifact_roots", [])
                )
                roots = _configured_roots(root, list(dict.fromkeys(configured)))
            result["data"] = refresh_data_catalog(
                store, state, roots,
                int(inventory["max_scan_files"]), int(inventory["hash_file_limit_mb"]),
            )
        _json(result)
    return 0


def cmd_inventory_show(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        payload = {
            "compute": json.loads((state / "compute" / "latest.json").read_text())
            if (state / "compute" / "latest.json").exists() else None,
            "resources": store.list_resources(args.kind),
        }
    _json(payload)
    return 0


def cmd_data_register(args: argparse.Namespace) -> int:
    _, config, state, _ = _context(args)
    inventory = config["inventory"]
    with Store(state / "artos.sqlite") as store:
        resource = register_path(
            store, args.path, int(inventory["hash_file_limit_mb"]),
            int(inventory["max_scan_files"]), args.kind,
        )
        export_catalog(store, state)
    _json(resource)
    return 0


def cmd_run_create(args: argparse.Namespace) -> int:
    root, config, state, projects = _context(args)
    if args.email:
        source_text = args.email.read_text(encoding="utf-8", errors="replace")
        source_type = "email"
    else:
        source_text = args.question
        source_type = "question"
    with Store(state / "artos.sqlite") as store:
        record = create_run(store, projects, source_text, source_type, args.project, args.title)
        refreshed = _ensure_inventories(root, config, state, store)
        copied = snapshot_inventories(Path(record["run_dir"]), state)
        store.transition(record["run_id"], "inventory_ready", {
            "inventory_snapshots": copied, "inventories_refreshed": sorted(refreshed),
        })
        record = store.get_run(record["run_id"])
    _json({"run": record, "inventory_snapshots": copied, "inventories_refreshed": sorted(refreshed)})
    return 0


def cmd_run_list(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        _json(store.list_runs(args.limit))
    return 0


def cmd_run_show(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run = store.get_run(args.run_id)
        sessions = []
        for session in store.sessions_for_run(args.run_id):
            spec = Path(session["spec_path"])
            sessions.append(inspect_session(spec) if spec.exists() else session)
    _json({"run": run, "sessions": sessions})
    return 0


def cmd_run_transition(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        store.transition(args.run_id, args.status, {"reason": args.reason} if args.reason else {})
        _json(store.get_run(args.run_id))
    return 0


def cmd_run_snapshot(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run = store.get_run(args.run_id)
    copied = snapshot_inventories(Path(run["run_dir"]), state)
    _json({"copied": copied})
    return 0


def cmd_run_freeze(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        digest = freeze_contract(store, args.run_id, args.contract)
        if store.get_run(args.run_id)["status"] == "hypotheses_ranked":
            store.transition(args.run_id, "contract_frozen", {"sha256": digest})
    _json({"run_id": args.run_id, "contract_sha256": digest})
    return 0


def _run_dir(store: Store, run_id: str) -> Path:
    return Path(store.get_run(run_id)["run_dir"])


def cmd_hypotheses_init(args: argparse.Namespace) -> int:
    _, config, state, _ = _context(args)
    count = args.count or int(config["research"]["default_hypothesis_count"])
    with Store(state / "artos.sqlite") as store:
        path = create_hypothesis_template(_run_dir(store, args.run_id), count)
    _json({"path": str(path), "count": count})
    return 0


def cmd_hypotheses_packet(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run_dir = _run_dir(store, args.run_id)
    path = create_blind_ranking_packet(run_dir / "questions" / "hypotheses.json", args.seed)
    _json({"path": str(path), "seed": args.seed})
    return 0


def cmd_hypotheses_rank(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run_dir = _run_dir(store, args.run_id)
        input_path = args.input or run_dir / "questions" / "hypotheses_scored_panel.json"
        json_path, markdown_path = rank_scored_hypotheses(input_path, run_dir / "questions")
        current = store.get_run(args.run_id)["status"]
        if current in {"routed_hybrid", "routed_hypothesis"}:
            store.transition(args.run_id, "hypotheses_ranked", {"ranking": str(json_path)})
    _json({"json": str(json_path), "markdown": str(markdown_path)})
    return 0


def cmd_hypotheses_aggregate(args: argparse.Namespace) -> int:
    _, config, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run_dir = _run_dir(store, args.run_id)
    research = config["research"]
    packet_path = args.packet or run_dir / "questions" / "ranking_packet.json"
    output_path = args.output or run_dir / "questions" / "hypotheses_scored_panel.json"
    path = aggregate_judge_panel(
        packet_path,
        args.judge,
        output_path,
        int(research.get("minimum_hypothesis_judges", 4)),
        int(research.get("minimum_codex_judges", 2)),
    )
    _json({"path": str(path), "judges": len(args.judge)})
    return 0


def cmd_session_launch(args: argparse.Namespace) -> int:
    root, config, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        spec = launch_claude_session(
            root, config, store, args.run_id, args.role, args.prompt, args.model
        )
    _json({
        "session": spec["session_name"], "tmux": spec["tmux_name"],
        "model": spec["model"], "watch": f"tmux attach-session -r -t {spec['tmux_name']}",
        "log": spec["log_path"],
    })
    return 0


def cmd_session_status(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        sessions = store.sessions_for_run(args.run_id)
    payload = []
    for session in sessions:
        path = Path(session["spec_path"])
        payload.append(inspect_session(path) if path.exists() else session)
    _json(payload)
    return 0


def cmd_session_watch(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        matches = [item for item in store.sessions_for_run(args.run_id) if item["role"] == args.role]
    if not matches:
        raise KeyError(f"No {args.role} session for {args.run_id}")
    name = matches[-1]["tmux_name"]
    os.execvp("tmux", ["tmux", "attach-session", "-r", "-t", name])
    return 0


def cmd_audit_init(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run_dir = _run_dir(store, args.run_id)
    json_path, markdown_path = create_audit_template(run_dir)
    _json({"json": str(json_path), "markdown": str(markdown_path)})
    return 0


def cmd_report_init(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run_dir = _run_dir(store, args.run_id)
    paths = create_report_skeleton(run_dir)
    _json({"created": [str(path) for path in paths]})
    return 0


def cmd_report_manifest(args: argparse.Namespace) -> int:
    _, _, state, _ = _context(args)
    with Store(state / "artos.sqlite") as store:
        run_dir = _run_dir(store, args.run_id)
    path = build_artifact_manifest(run_dir)
    _json({"manifest": str(path)})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="artos", description="ARTOS research orchestrator")
    parser.add_argument("--root", type=Path, help="ARTOS project root")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check ARTOS, Claude, and tmux readiness")
    doctor.set_defaults(func=cmd_doctor)

    inventory = sub.add_parser("inventory", help="Manage compute and data inventories")
    inventory_sub = inventory.add_subparsers(dest="inventory_command", required=True)
    refresh = inventory_sub.add_parser("refresh")
    refresh.add_argument("--compute", action="store_true")
    refresh.add_argument("--data-root", action="append", default=None)
    refresh.set_defaults(func=cmd_inventory_refresh)
    show = inventory_sub.add_parser("show")
    show.add_argument("--kind", action="append")
    show.set_defaults(func=cmd_inventory_show)

    data = sub.add_parser("data", help="Register data or artifacts")
    data_sub = data.add_subparsers(dest="data_command", required=True)
    register = data_sub.add_parser("register")
    register.add_argument("path", type=Path)
    register.add_argument("--kind")
    register.set_defaults(func=cmd_data_register)

    run = sub.add_parser("run", help="Create and manage research runs")
    run_sub = run.add_subparsers(dest="run_command", required=True)
    create = run_sub.add_parser("create")
    source = create.add_mutually_exclusive_group(required=True)
    source.add_argument("--question")
    source.add_argument("--email", type=Path)
    create.add_argument("--project")
    create.add_argument("--title")
    create.set_defaults(func=cmd_run_create)
    listing = run_sub.add_parser("list")
    listing.add_argument("--limit", type=int, default=25)
    listing.set_defaults(func=cmd_run_list)
    show_run = run_sub.add_parser("show")
    show_run.add_argument("run_id")
    show_run.set_defaults(func=cmd_run_show)
    transition = run_sub.add_parser("transition")
    transition.add_argument("run_id")
    transition.add_argument("status")
    transition.add_argument("--reason")
    transition.set_defaults(func=cmd_run_transition)
    snapshot = run_sub.add_parser("snapshot-inventory")
    snapshot.add_argument("run_id")
    snapshot.set_defaults(func=cmd_run_snapshot)
    freeze = run_sub.add_parser("freeze-contract")
    freeze.add_argument("run_id")
    freeze.add_argument("contract", type=Path)
    freeze.set_defaults(func=cmd_run_freeze)

    hypotheses = sub.add_parser("hypotheses", help="Prepare and rank hypotheses")
    hypotheses_sub = hypotheses.add_subparsers(dest="hypotheses_command", required=True)
    init_h = hypotheses_sub.add_parser("init")
    init_h.add_argument("run_id")
    init_h.add_argument("--count", type=int)
    init_h.set_defaults(func=cmd_hypotheses_init)
    packet = hypotheses_sub.add_parser("packet")
    packet.add_argument("run_id")
    packet.add_argument("--seed", type=int, default=20260816)
    packet.set_defaults(func=cmd_hypotheses_packet)
    aggregate = hypotheses_sub.add_parser("aggregate")
    aggregate.add_argument("run_id")
    aggregate.add_argument("--packet", type=Path)
    aggregate.add_argument("--judge", action="append", type=Path, required=True)
    aggregate.add_argument("--output", type=Path)
    aggregate.set_defaults(func=cmd_hypotheses_aggregate)
    rank = hypotheses_sub.add_parser("rank")
    rank.add_argument("run_id")
    rank.add_argument("--input", type=Path)
    rank.set_defaults(func=cmd_hypotheses_rank)

    session = sub.add_parser("session", help="Launch and monitor tmux agents")
    session_sub = session.add_subparsers(dest="session_command", required=True)
    launch = session_sub.add_parser("launch")
    launch.add_argument("run_id")
    launch.add_argument("--role", choices=("ranker", "primary", "adversary"), required=True)
    launch.add_argument("--prompt", type=Path, required=True)
    launch.add_argument("--model")
    launch.set_defaults(func=cmd_session_launch)
    status = session_sub.add_parser("status")
    status.add_argument("run_id")
    status.set_defaults(func=cmd_session_status)
    watch = session_sub.add_parser("watch")
    watch.add_argument("run_id")
    watch.add_argument("--role", choices=("ranker", "primary", "adversary"), required=True)
    watch.set_defaults(func=cmd_session_watch)

    audit = sub.add_parser("audit", help="Create adversarial audit records")
    audit_sub = audit.add_subparsers(dest="audit_command", required=True)
    audit_init = audit_sub.add_parser("init")
    audit_init.add_argument("run_id")
    audit_init.set_defaults(func=cmd_audit_init)

    report = sub.add_parser("report", help="Create reporting artifacts")
    report_sub = report.add_subparsers(dest="report_command", required=True)
    report_init = report_sub.add_parser("init")
    report_init.add_argument("run_id")
    report_init.set_defaults(func=cmd_report_init)
    manifest = report_sub.add_parser("manifest")
    manifest.add_argument("run_id")
    manifest.set_defaults(func=cmd_report_manifest)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"artos: error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
