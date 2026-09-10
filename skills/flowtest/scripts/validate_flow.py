#!/usr/bin/env python3
"""Validate .flow.yaml files against the flowtest v1 flow format.

The format contract is skills/flowtest/references/flow-format.md. This script
is the mechanical enforcement of that contract: it is used by the Plan step
before a draft is formalized, by the Run step before execution, and by CI.

Usage:
    python3 validate_flow.py <flow.yaml> [<flow.yaml> ...]

Exit codes:
    0  all files valid
    1  at least one file invalid (issues printed)
    2  usage error or file not found
    3  PyYAML not installed (validation skipped)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ACTIONS = {
    "goto": "navigate to target (URL or path)",
    "click": "click the element named by target",
    "fill": "type value into the input named by target",
    "select": "choose value in the dropdown named by target",
    "hover": "hover the element named by target",
    "press": "press the key given in value (target optional)",
    "wait": "pause for value milliseconds",
    "check": "assert the expect conditions without acting",
    "extract": "read the fields listed in value into the result",
}
TARGET_REQUIRED = {"goto", "click", "fill", "select", "hover"}
VALUE_REQUIRED = {"fill", "select", "press", "wait", "extract"}
EXPECT_CONDITIONS = ("text", "not_text", "url", "title", "element")
PHASES = ("precheck", "setup", "verify", "conclude")
TOP_LEVEL_KEYS = {
    "flow",
    "title",
    "description",
    "sut",
    "baseUrl",
    "tags",
    "timeout",
    "stepTimeout",
    "vars",
    "steps",
}
STEP_KEYS = {
    "id",
    "action",
    "target",
    "value",
    "expect",
    "screenshot",
    "phase",
    "timeout",
    "note",
}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _is_scalar(value) -> bool:
    return isinstance(value, (str, int, float, bool))


def _is_slug(value) -> bool:
    return isinstance(value, str) and bool(SLUG_RE.fullmatch(value))


def _is_positive_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def validate(flow) -> list[str]:
    """Return a list of issue strings; empty means the parsed flow is valid."""
    issues: list[str] = []
    if not isinstance(flow, dict):
        issues.append(f"flow file must be a mapping, got {type(flow).__name__}")
        return issues

    for key in flow:
        if key not in TOP_LEVEL_KEYS:
            issues.append(f"unknown key {key!r} (top level)")

    if "flow" not in flow:
        issues.append("missing required key 'flow'")
    elif not _is_slug(flow["flow"]):
        issues.append("flow must be a non-empty kebab-case slug (e.g. guest-checkout)")

    if "title" not in flow:
        issues.append("missing required key 'title'")
    elif not isinstance(flow["title"], str) or not flow["title"].strip():
        issues.append("title must be a non-empty string")

    if "tags" in flow and (
        not isinstance(flow["tags"], list)
        or not all(isinstance(tag, str) and tag for tag in flow["tags"])
    ):
        issues.append("tags must be a list of non-empty strings")

    for key in ("timeout", "stepTimeout"):
        if key in flow and not _is_positive_number(flow[key]):
            issues.append(f"{key} must be a positive number (seconds)")

    if "baseUrl" in flow and not isinstance(flow["baseUrl"], str):
        issues.append("baseUrl must be a string")

    for key in ("description", "sut"):
        if key in flow and not isinstance(flow[key], str):
            issues.append(f"{key} must be a string")

    if "vars" in flow:
        variables = flow["vars"]
        if not isinstance(variables, dict) or not all(
            isinstance(name, str) and name and _is_scalar(value)
            for name, value in variables.items()
        ):
            issues.append("vars must be a mapping of names to scalar values")

    if "steps" not in flow:
        issues.append("missing required key 'steps'")
        return issues
    steps = flow["steps"]
    if not isinstance(steps, list) or not steps:
        issues.append("steps must be a non-empty list")
        return issues

    seen_ids: set[str] = set()
    for index, step in enumerate(steps):
        issues.extend(_validate_step(step, index, seen_ids))
    return issues


def _validate_step(step, index: int, seen_ids: set[str]) -> list[str]:
    where = f"steps[{index}]"
    if not isinstance(step, dict):
        return [f"{where}: step must be a mapping, got {type(step).__name__}"]

    issues: list[str] = []
    for key in step:
        if key not in STEP_KEYS:
            issues.append(f"{where}: unknown key {key!r}")

    step_id = step.get("id")
    if "id" not in step:
        issues.append(f"{where}: missing required key 'id'")
    elif not _is_slug(step_id):
        issues.append(f"{where}: id must be a kebab-case slug (e.g. add-to-cart)")
    elif step_id in seen_ids:
        issues.append(f"{where}: duplicate step id {step_id!r}")
    else:
        seen_ids.add(step_id)

    action = step.get("action")
    if "action" not in step:
        issues.append(f"{where}: missing required key 'action'")
    elif action not in ACTIONS:
        valid = ", ".join(sorted(ACTIONS))
        issues.append(f"{where}: unknown action {action!r} (valid: {valid})")

    if "target" in step and not isinstance(step["target"], str):
        issues.append(f"{where}: target must be a string")
    if action in TARGET_REQUIRED and "target" not in step:
        issues.append(f"{where}: action {action!r} requires 'target'")

    if action in VALUE_REQUIRED and "value" not in step:
        issues.append(f"{where}: action {action!r} requires 'value'")
    if "value" in step:
        issues.extend(_validate_value(step, action, where))

    if "expect" in step:
        issues.extend(_validate_expect(step["expect"], where))
    elif action == "check":
        issues.append(f"{where}: action 'check' requires a non-empty 'expect'")

    if "screenshot" in step and not isinstance(step["screenshot"], bool):
        issues.append(f"{where}: screenshot must be a boolean")
    if "phase" in step and step["phase"] not in PHASES:
        issues.append(
            f"{where}: phase must be one of: {', '.join(PHASES)}"
        )
    if "timeout" in step and not _is_positive_number(step["timeout"]):
        issues.append(f"{where}: timeout must be a positive number (seconds)")
    if "note" in step and not isinstance(step["note"], str):
        issues.append(f"{where}: note must be a string")
    return issues


def _validate_value(step: dict, action, where: str) -> list[str]:
    value = step["value"]
    if action == "wait":
        if not _is_positive_number(value):
            return [f"{where}: wait value must be a positive number (milliseconds)"]
        return []
    if action == "extract":
        if not isinstance(value, list) or not value or not all(
            isinstance(field, str) and field for field in value
        ):
            return [f"{where}: extract value must be a non-empty list of field names"]
        return []
    if isinstance(value, str) and value:
        return []
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return []
    return [f"{where}: value must be a non-empty string or number"]


def _validate_expect(expect, where: str) -> list[str]:
    if not isinstance(expect, list) or not expect:
        return [f"{where}: expect must be a non-empty list of conditions"]
    issues: list[str] = []
    for index, condition in enumerate(expect):
        place = f"{where}.expect[{index}]"
        if not isinstance(condition, dict) or len(condition) != 1:
            issues.append(
                f"{place}: each condition must be a mapping with exactly one key"
            )
            continue
        (key, value), = condition.items()
        if key not in EXPECT_CONDITIONS:
            issues.append(
                f"{place}: unknown condition {key!r} (valid: "
                f"{', '.join(EXPECT_CONDITIONS)})"
            )
        elif not isinstance(value, str) or not value:
            issues.append(f"{place}: {key} must be a non-empty string")
    return issues


def validate_file(path: Path) -> list[str]:
    """Parse path as YAML and validate it. YAML parse errors become issues."""
    import yaml

    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as error:
        return [f"cannot read file: {error}"]
    try:
        flow = yaml.safe_load(text)
    except yaml.YAMLError as error:
        return [f"not valid YAML: {error}"]
    return validate(flow)


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate_flow.py <flow.yaml> [<flow.yaml> ...]", file=sys.stderr)
        return 2

    any_invalid = False
    for raw_path in argv:
        path = Path(raw_path)
        if not path.is_file():
            print(f"{path}: file not found", file=sys.stderr)
            return 2
        try:
            issues = validate_file(path)
        except ImportError:
            print(
                f"{path}: validation skipped — install PyYAML to validate flows",
                file=sys.stderr,
            )
            return 3
        if issues:
            any_invalid = True
            for issue in issues:
                print(f"{path}: {issue}")
            print(f"{path}: {len(issues)} issue(s) found")
        else:
            print(f"{path}: OK")
    return 1 if any_invalid else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
