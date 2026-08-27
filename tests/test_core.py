"""Skeleton test suite: science-gate state machine and CLI surface."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from artos.cli import build_parser, main
from artos.state_machine import validate_transition


class SkeletonTest(unittest.TestCase):
    def test_state_machine_rejects_skipped_science_gate(self) -> None:
        validate_transition("intake_created", "inventory_ready")
        with self.assertRaises(ValueError):
            validate_transition("contract_frozen", "complete")

    def test_cli_surface_parses(self) -> None:
        parser = build_parser()
        for argv in (["doctor"], ["run", "list"], ["hypotheses", "init", "RUN-1"]):
            args = parser.parse_args(argv)
            self.assertTrue(callable(args.func))

    def test_skeleton_commands_exit_cleanly(self) -> None:
        example = Path(__file__).resolve().parents[1] / "artos.example.json"
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "artos.json").write_text(example.read_text(encoding="utf-8"))
            with self.assertRaises(SystemExit) as ctx:
                main(["--root", tmp, "run", "list"])
            self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
