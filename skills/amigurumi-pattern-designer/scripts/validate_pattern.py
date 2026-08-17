#!/usr/bin/env python3
"""Validate round-by-round stitch arithmetic for amigurumi patterns."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Flow:
    consumed: int = 0
    produced: int = 0
    foundation: bool = False

    def scaled(self, n: int) -> "Flow":
        return Flow(self.consumed * n, self.produced * n, self.foundation)

    def add(self, other: "Flow") -> None:
        self.consumed += other.consumed
        self.produced += other.produced
        self.foundation = self.foundation or other.foundation


FIXED = {
    "sc": (1, 1),
    "hdc": (1, 1),
    "dc": (1, 1),
    "tr": (1, 1),
    "slst": (1, 1),
    "inc": (1, 2),
    "inc3": (1, 3),
    "dec": (2, 1),
    "dec3": (3, 1),
    "skip": (1, 0),
}


def positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def eval_node(node: Any, context: str) -> Flow:
    if not isinstance(node, dict):
        raise ValueError(f"{context}: operation must be an object")

    if "repeat" in node:
        repeat = positive_int(node["repeat"], f"{context}.repeat")
        seq = node.get("sequence")
        if not isinstance(seq, list) or not seq:
            raise ValueError(f"{context}: repeat requires a non-empty sequence")
        total = Flow()
        for idx, child in enumerate(seq, 1):
            total.add(eval_node(child, f"{context}.sequence[{idx}]"))
        return total.scaled(repeat)

    kind = node.get("type")
    if kind in FIXED:
        count = positive_int(node.get("count", 1), f"{context}.count")
        consume, produce = FIXED[kind]
        return Flow(consume * count, produce * count)

    if kind in {"mr", "foundation"}:
        count = positive_int(node.get("count", 0), f"{context}.count")
        return Flow(0, count, foundation=True)

    if kind == "custom":
        consume = positive_int(node.get("consume"), f"{context}.consume")
        produce = positive_int(node.get("produce"), f"{context}.produce")
        return Flow(consume, produce)

    raise ValueError(f"{context}: unsupported operation type {kind!r}")


def validate(data: Any) -> tuple[list[str], list[str], dict[str, list[int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    sequences: dict[str, list[int]] = {}

    if not isinstance(data, dict):
        return ["Top-level JSON value must be an object."], warnings, sequences

    parts = data.get("parts")
    if not isinstance(parts, list) or not parts:
        return ["Top-level 'parts' must be a non-empty list."], warnings, sequences

    seen_names: set[str] = set()

    for pidx, part in enumerate(parts, 1):
        if not isinstance(part, dict):
            errors.append(f"Part {pidx}: must be an object.")
            continue
        name = part.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"Part {pidx}: missing non-empty string 'name'.")
            name = f"Part {pidx}"
        if name in seen_names:
            errors.append(f"Part {name!r}: duplicate part name.")
        seen_names.add(name)

        try:
            previous = positive_int(part.get("initial_stitches", 0), f"{name}.initial_stitches")
        except ValueError as exc:
            errors.append(str(exc))
            previous = 0

        rounds = part.get("rounds")
        if not isinstance(rounds, list) or not rounds:
            errors.append(f"{name}: 'rounds' must be a non-empty list.")
            continue

        seq_counts: list[int] = []
        for ridx, rnd in enumerate(rounds, 1):
            if not isinstance(rnd, dict):
                errors.append(f"{name} round {ridx}: must be an object.")
                continue
            label = rnd.get("label", f"round {ridx}")
            ops = rnd.get("ops")
            if not isinstance(ops, list) or not ops:
                errors.append(f"{name} {label}: 'ops' must be a non-empty list.")
                continue

            flow = Flow()
            try:
                for oidx, op in enumerate(ops, 1):
                    flow.add(eval_node(op, f"{name} {label} op {oidx}"))
            except ValueError as exc:
                errors.append(str(exc))
                continue

            allow_partial = bool(rnd.get("allow_partial", False))
            if previous == 0 and flow.foundation:
                if flow.consumed != 0:
                    errors.append(f"{name} {label}: foundation round unexpectedly consumes {flow.consumed} stitches.")
            elif not allow_partial and flow.consumed != previous:
                errors.append(
                    f"{name} {label}: consumes {flow.consumed} stitches but previous count is {previous}."
                )
            elif allow_partial and flow.consumed > previous:
                errors.append(
                    f"{name} {label}: partial round consumes {flow.consumed}, exceeding previous count {previous}."
                )

            expected = rnd.get("expected")
            if expected is None:
                warnings.append(f"{name} {label}: no 'expected' count; using computed {flow.produced}.")
                current = flow.produced
            else:
                try:
                    expected_int = positive_int(expected, f"{name} {label}.expected")
                except ValueError as exc:
                    errors.append(str(exc))
                    current = flow.produced
                else:
                    current = expected_int
                    if flow.produced != expected_int:
                        errors.append(
                            f"{name} {label}: operations produce {flow.produced} stitches but expected is {expected_int}."
                        )

            if previous > 0 and current > previous * 2:
                warnings.append(
                    f"{name} {label}: stitch count jumps from {previous} to {current}; confirm this is intentional."
                )
            seq_counts.append(current)
            previous = current

        sequences[name] = seq_counts

    groups = data.get("symmetry_groups", [])
    if groups is not None and not isinstance(groups, list):
        errors.append("'symmetry_groups' must be a list of name lists.")
    elif isinstance(groups, list):
        for gidx, group in enumerate(groups, 1):
            if not isinstance(group, list) or len(group) < 2 or not all(isinstance(x, str) for x in group):
                errors.append(f"symmetry_groups[{gidx}] must contain at least two part-name strings.")
                continue
            missing = [name for name in group if name not in sequences]
            if missing:
                errors.append(f"symmetry_groups[{gidx}] references missing parts: {', '.join(missing)}.")
                continue
            baseline = sequences[group[0]]
            for other in group[1:]:
                if sequences[other] != baseline:
                    errors.append(
                        f"Symmetry mismatch: {group[0]!r} counts {baseline} != {other!r} counts {sequences[other]}."
                    )

    return errors, warnings, sequences


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path, help="Pattern validation JSON file")
    parser.add_argument("--show-counts", action="store_true", help="Print resulting count sequence for each part")
    args = parser.parse_args()

    try:
        data = json.loads(args.json_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.json_file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 1

    errors, warnings, sequences = validate(data)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if args.show_counts:
        for name, counts in sequences.items():
            print(f"COUNTS: {name}: {counts}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"PASS: 0 errors, {len(warnings)} warning(s); validated {len(sequences)} part(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
