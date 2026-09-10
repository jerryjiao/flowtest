"""Repository structure gates for flowtest.

Covers: plugin manifest correctness, SKILL.md frontmatter sanity, internal
link integrity, and the pre-publish scrub gate (release gate #2 in
docs/plans/2026-09-10-rebirth-consensus.md — zero legacy identifiers,
credentials, or hardcoded service IPs anywhere in the repo).
"""

import json
import re
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("flowtest", "flowtest-kb")
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".txt", ".sh", ".cfg", ".toml"}
IGNORED_DIRS = {".git", ".mimosa", "node_modules", "__pycache__", "dist", "build"}

# Legacy-project identifiers that must never reappear in this repo. Built
# from fragments so this file itself contains no complete banned literal.
BANNED_WORDS = (
    "ma" "bang",
    "\u9a6c\u5e2e",
    "open" "viking",
    "open" "claw",
    "clawd" "bot",
    "fei" "shu",
    "\u98de\u4e66",
    "coding" ".net",
    "coding" "_sync",
)

# Secret-looking assignments. Values containing these tokens are placeholders.
PLACEHOLDER_TOKENS = ("placeholder", "example", "demo", "your", "changeme", "xxx", "{{")
SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"\bsk-[a-zA-Z0-9]{20,}"),
    re.compile(r"\bghp_[a-zA-Z0-9]{30,}"),
    re.compile(r"\bxox[baprs]-[a-zA-Z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"(?i)\b(password|passwd|secret|token|api[_-]?key)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
)
IPV4 = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")
ALLOWED_IPS = {"127.0.0.1", "0.0.0.0", "255.255.255.255"}


def repo_text_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        yield path


class PluginManifest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(
            (REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

    def test_manifest_basics(self):
        for key in ("name", "version", "description", "author", "license"):
            self.assertIn(key, self.manifest)
        # `skills` must NOT be declared: Claude Code rejects the field in its
        # manifest schema and both hosts auto-discover skills/<name>/ anyway.
        self.assertNotIn("skills", self.manifest)
        # zcode manifest rule: name matches ^[a-z0-9][a-z0-9._-]{0,127}$
        self.assertRegex(self.manifest["name"], r"^[a-z0-9][a-z0-9._-]{0,127}$")

    def test_skills_discoverable_by_convention(self):
        for name in SKILLS:
            skill_md = REPO_ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(skill_md.exists(), f"missing {skill_md}")

    def test_marketplace_json_registers_the_plugin(self):
        market = json.loads(
            (REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(market["name"], "flowtest")
        self.assertEqual(len(market["plugins"]), 1)
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], self.manifest["name"])
        self.assertEqual(entry["source"], "./")

    def test_manifest_registers_both_skills(self):
        # Skills are auto-discovered from skills/<name>/ (both Claude Code and
        # zcode); the manifest itself must not carry a `skills` field.
        self.assertNotIn("skills", self.manifest)
        self.assertTrue(
            all(
                (REPO_ROOT / "skills" / name / "SKILL.md").exists()
                for name in SKILLS
            )
        )


class SkillFrontmatter(unittest.TestCase):
    def test_frontmatter_parses_and_names_match_dirs(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                text = (REPO_ROOT / "skills" / name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertTrue(text.startswith("---\n"), "must start with frontmatter")
                _, fm_raw, _ = text.split("---\n", 2)
                frontmatter = yaml.safe_load(fm_raw)
                self.assertEqual(frontmatter["name"], name)
                self.assertTrue(frontmatter.get("description", "").strip())


class InternalLinks(unittest.TestCase):
    def test_markdown_links_resolve(self):
        docs = [
            *(
                path
                for name in SKILLS
                for path in (REPO_ROOT / "skills" / name).rglob("*.md")
            ),
            *(REPO_ROOT / "docs").rglob("*.md"),
            REPO_ROOT / "README.md",
        ]
        self.assertTrue(docs)
        link = re.compile(r"\[[^\]]*\]\(([^)#\s]+)[)#]")
        for doc in docs:
            for match in link.finditer(doc.read_text(encoding="utf-8")):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (doc.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(), f"{doc.name} links to missing {target}"
                )


class DemoSite(unittest.TestCase):
    """The demo site is the quickstart SUT — guard the semantic anchors the
    shipped example flows target, so a refactor cannot silently break the
    first flow a newcomer runs."""

    def setUp(self):
        self.html = (REPO_ROOT / "demo" / "index.html").read_text(encoding="utf-8")

    def test_semantic_anchors_exist(self):
        anchors = (
            "<h1>Sign in</h1>",
            "<h1>Tasks</h1>",
            "<label for=\"email\">Email</label>",
            "<label for=\"password\">Password</label>",
            "<label for=\"new-task\" class=\"sr-only\">New task</label>",
            ">Sign in</button>",
            ">Add</button>",
            ">Sign out</button>",
            ">Reset demo data</button>",
            "data-field=\"open-count\"",
            "data-field=\"done-count\"",
            "aria-label\", task.name",
        )
        for anchor in anchors:
            self.assertIn(anchor, self.html, f"demo site lost anchor: {anchor!r}")

    def test_demo_credentials_and_error_string(self):
        self.assertIn("demo@flowtest.dev", self.html)
        self.assertIn("demo-password", self.html)
        self.assertIn("Invalid credentials", self.html)


class ScrubGate(unittest.TestCase):
    """Release gate #2: zero legacy identifiers, secrets, hardcoded IPs."""

    def test_no_legacy_identifiers(self):
        for path in repo_text_files():
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            for word in BANNED_WORDS:
                self.assertNotIn(
                    word, text, f"legacy identifier {word!r} found in {path}"
                )

    def test_no_hardcoded_service_ips(self):
        for path in repo_text_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for match in IPV4.finditer(text):
                ip = match.group(1)
                self.assertIn(
                    ip,
                    ALLOWED_IPS,
                    f"hardcoded IP {ip} in {path} (only loopback/broadcast allowed)",
                )

    def test_no_secrets(self):
        for path in repo_text_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in SECRET_PATTERNS:
                match = pattern.search(text)
                if not match:
                    continue
                if any(token in match.group(0).lower() for token in PLACEHOLDER_TOKENS):
                    continue
                self.fail(f"secret-looking value in {path}: {match.group(0)!r}")

    def test_no_hardcoded_home_paths_in_skills(self):
        for path in (REPO_ROOT / "skills").rglob("*"):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                text = path.read_text(encoding="utf-8", errors="replace")
                self.assertNotIn(
                    "~/", text, f"host-specific home path in {path} — use relative paths"
                )


if __name__ == "__main__":
    unittest.main()
