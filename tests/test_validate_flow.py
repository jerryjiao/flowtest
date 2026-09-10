"""Tests for the .flow.yaml schema validator (skills/flowtest/scripts/validate_flow.py).

The flow format contract lives in skills/flowtest/references/flow-format.md;
these tests pin the validator to that contract.
"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = REPO_ROOT / "skills" / "flowtest" / "scripts"

sys.path.insert(0, str(SCRIPT_DIR))
import validate_flow  # noqa: E402


def make_flow(**overrides):
    """A minimal valid flow; overrides replace or add top-level keys."""
    flow = {
        "flow": "guest-checkout",
        "title": "Guest can add a product to the cart and check out",
        "steps": [
            {"id": "open-catalog", "action": "goto", "target": "/products"},
            {
                "id": "see-catalog",
                "action": "check",
                "expect": [{"text": "All products"}],
            },
        ],
    }
    flow.update(overrides)
    return flow


class ValidFlows(unittest.TestCase):
    def assertValid(self, flow):
        issues = validate_flow.validate(flow)
        self.assertEqual(issues, [], f"expected valid, got issues: {issues}")

    def test_minimal_flow(self):
        self.assertValid(make_flow())

    def test_full_flow(self):
        self.assertValid(
            make_flow(
                description="Happy-path guest checkout against the demo site.",
                sut="demo-site",
                baseUrl="http://localhost:4173",
                tags=["smoke", "cart"],
                timeout=300,
                stepTimeout=60,
                vars={"USERNAME": "demo-user", "QUANTITY": 2},
                steps=[
                    {
                        "id": "open-catalog",
                        "action": "goto",
                        "target": "/products",
                        "phase": "verify",
                        "expect": [{"url": "/products"}, {"element": "main"}],
                        "screenshot": True,
                    },
                    {
                        "id": "add-first-product",
                        "action": "click",
                        "target": "button 'Add to cart' (first)",
                        "expect": [{"text": "Added to cart"}, {"not_text": "Error"}],
                    },
                    {
                        "id": "set-quantity",
                        "action": "fill",
                        "target": "textbox 'Quantity'",
                        "value": "2",
                    },
                    {
                        "id": "pick-shipping",
                        "action": "select",
                        "target": "combobox 'Shipping'",
                        "value": "standard",
                    },
                    {"id": "open-menu", "action": "hover", "target": "link 'Account'"},
                    {"id": "submit", "action": "press", "value": "Enter"},
                    {"id": "settle", "action": "wait", "value": 500},
                    {
                        "id": "grab-summary",
                        "action": "extract",
                        "value": ["order-number", "total"],
                    },
                ],
            )
        )

    def test_step_note_key_allowed(self):
        flow = make_flow()
        flow["steps"][0]["note"] = "Catalog is server-rendered; no wait needed."
        self.assertValid(flow)


class _IssueAssertions(unittest.TestCase):
    """Shared assertion: the flow must produce an issue containing fragment."""

    def assertIssueIn(self, flow, fragment):
        issues = validate_flow.validate(flow)
        self.assertTrue(
            any(fragment in i for i in issues),
            f"expected an issue containing {fragment!r}, got {issues}",
        )


class TopLevelRules(_IssueAssertions):
    def test_flow_must_be_mapping(self):
        self.assertIssueIn(["not", "a", "map"], "flow file must be a mapping")

    def test_missing_flow(self):
        flow = make_flow()
        del flow["flow"]
        self.assertIssueIn(flow, "flow")

    def test_missing_title(self):
        flow = make_flow()
        del flow["title"]
        self.assertIssueIn(flow, "title")

    def test_missing_steps(self):
        flow = make_flow()
        del flow["steps"]
        self.assertIssueIn(flow, "steps")

    def test_empty_steps(self):
        self.assertIssueIn(make_flow(steps=[]), "steps")

    def test_flow_slug_rules(self):
        self.assertIssueIn(make_flow(flow="Guest Checkout"), "slug")
        self.assertIssueIn(make_flow(flow=""), "flow")

    def test_unknown_top_level_key(self):
        self.assertIssueIn(make_flow(extra=1), "unknown key 'extra'")

    def test_bad_types(self):
        self.assertIssueIn(make_flow(title=42), "title")
        self.assertIssueIn(make_flow(timeout=-1), "timeout")
        self.assertIssueIn(make_flow(stepTimeout="fast"), "stepTimeout")
        self.assertIssueIn(make_flow(tags="smoke"), "tags")
        self.assertIssueIn(make_flow(vars={"X": ["nested"]}), "vars")

    def test_baseurl_must_be_string(self):
        self.assertIssueIn(make_flow(baseUrl=8080), "baseUrl")


class StepRules(_IssueAssertions):
    def assertIssue(self, steps, fragment):
        self.assertIssueIn(make_flow(steps=steps), fragment)

    def valid_step(self, **overrides):
        step = {"id": "s1", "action": "click", "target": "button 'Go'"}
        step.update(overrides)
        return step

    def test_step_must_be_mapping(self):
        self.assertIssue(["not-a-map"], "step must be a mapping")

    def test_missing_id(self):
        self.assertIssue([{"action": "click", "target": "b"}], "id")

    def test_missing_action(self):
        self.assertIssue([{"id": "s1", "target": "b"}], "action")

    def test_bad_id_slug(self):
        self.assertIssue(
            [{"id": "Step One", "action": "check", "expect": [{"text": "x"}]}], "slug"
        )

    def test_duplicate_ids(self):
        self.assertIssue(
            [
                {"id": "s1", "action": "check", "expect": [{"text": "a"}]},
                {"id": "s1", "action": "check", "expect": [{"text": "b"}]},
            ],
            "duplicate",
        )

    def test_unknown_action(self):
        self.assertIssue([{"id": "s1", "action": "teleport"}], "action")

    def test_unknown_step_key(self):
        self.assertIssue([self.valid_step(selector="css:#x")], "unknown key 'selector'")

    def test_target_required_per_action(self):
        for action in ("goto", "click", "fill", "select", "hover"):
            with self.subTest(action=action):
                self.assertIssue(
                    [{"id": "s1", "action": action, "value": "v"}],
                    "target",
                )

    def test_value_required_per_action(self):
        for action in ("fill", "select", "press", "wait", "extract"):
            with self.subTest(action=action):
                self.assertIssue(
                    [{"id": "s1", "action": action, "target": "t"}],
                    "value",
                )

    def test_check_requires_expect(self):
        self.assertIssue([{"id": "s1", "action": "check"}], "expect")

    def test_bad_phase(self):
        self.assertIssue([self.valid_step(phase="final")], "phase")

    def test_bad_screenshot_flag(self):
        self.assertIssue([self.valid_step(screenshot="yes")], "screenshot")

    def test_bad_step_timeout(self):
        self.assertIssue([self.valid_step(timeout=0)], "timeout")


class ExpectRules(_IssueAssertions):
    def assertIssue(self, expect, fragment):
        self.assertIssueIn(
            make_flow(steps=[{"id": "s1", "action": "check", "expect": expect}]),
            fragment,
        )

    def test_valid_condition_keys(self):
        for key in ("text", "not_text", "url", "title", "element"):
            with self.subTest(key=key):
                issues = validate_flow.validate(
                    make_flow(
                        steps=[{"id": "s1", "action": "check", "expect": [{key: "x"}]}]
                    )
                )
                self.assertEqual(issues, [])

    def test_condition_must_be_single_key(self):
        self.assertIssue([{"text": "a", "url": "b"}], "exactly one key")
        self.assertIssue([{}], "exactly one key")

    def test_unknown_condition_key(self):
        self.assertIssue([{"vibe": "good"}], "unknown condition")

    def test_condition_value_must_be_string(self):
        self.assertIssue([{"text": 3}], "string")

    def test_expect_must_be_list(self):
        self.assertIssue({"text": "a"}, "expect")


class ShippedExamplesValidate(unittest.TestCase):
    def test_every_shipped_example_is_valid(self):
        examples = sorted(
            (REPO_ROOT / "skills" / "flowtest" / "examples").glob("*.flow.yaml")
        )
        self.assertTrue(examples, "no shipped examples found")
        for path in examples:
            with self.subTest(example=path.name):
                issues = validate_flow.validate_file(path)
                self.assertEqual(issues, [], f"{path.name}: {issues}")


class Cli(unittest.TestCase):
    """Exercise the real CLI entry point (main(argv)) in-process."""

    def run_cli(self, *args):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = validate_flow.main(list(args))
        return code, stdout.getvalue()

    def test_exit_0_on_valid_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ok.flow.yaml"
            path.write_text(
                "flow: t\ntitle: T\nsteps:\n  - id: s1\n    action: check\n"
                "    expect:\n      - text: hi\n",
                encoding="utf-8",
            )
            code, out = self.run_cli(str(path))
            self.assertEqual(code, 0, out)

    def test_exit_1_on_invalid_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.flow.yaml"
            path.write_text("flow: t\nsteps: []\n", encoding="utf-8")
            code, out = self.run_cli(str(path))
            self.assertEqual(code, 1)
            self.assertIn("issue", out.lower())

    def test_exit_2_on_missing_file(self):
        code, _ = self.run_cli("/nonexistent/flow.yaml")
        self.assertEqual(code, 2)

    def test_exit_2_without_args(self):
        code, _ = self.run_cli()
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
