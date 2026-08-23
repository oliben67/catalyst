#!/usr/bin/env python3
"""Validate a deployed .catalyst-proj/ against catalyst's structural invariants.

This is the enforcement layer of the anti-drift architecture: the invariants an
agent is asked to uphold (INV-5..INV-8, INV-14, INV-15, INV-16, INV-17) are re-checked here deterministically, so
they hold every time regardless of what any agent or human did. Mirrors the
existing scripts/check_plugins.py pattern.

Exit 0 = clean, exit 1 = violations found (fails CI / Stop hook).

Scope note: only checks the structural invariants that are machine-verifiable
from the tree. Behavioural rules (INV-1..INV-4) are not checkable here and remain
the agent's responsibility, re-grounded via INVARIANTS.md.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DEPLOY_DIRNAME = ".catalyst-proj"
# <id>-<short-summary>.md ; id like req-0001, bug-0007, rule prefixes, domains, etc.
NAME_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*-[a-z0-9][a-z0-9-]*\.md$", re.I)
# A trailing all-digit segment (e.g. "br-AUTH-002.md") is a bare ID with no
# descriptive summary — NAME_RE alone can't reject it, since a run of digits
# satisfies the same character class as a real summary word would.
BARE_ID_RE = re.compile(r"-\d+\.md$", re.I)
TEMPLATE_RE = re.compile(r"^TEMPLATE-[A-Z-]+\.md$")
# git hash-object is a 40-char hex SHA-1.
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
JOURNAL_REQUIRED_FIELDS = (
    "timestamp", "actor", "command", "action", "artifact", "targets",
    "intent", "files",
)
INDEX_NAMES = {
    "rules.md", "domains.md", "requirements.md", "features.md", "bugs.md",
    "house-keeping.md", "meta-tags.md", "epics.md", "stories.md", "tasks.md",
    "spikes.md", "sprints.md", "README.md", "CODE-OF-CONDUCT.md", "version.txt",
    "Rules-of-Rules.md", "rules-of-work-items.md", "DEPLOYMENT.md", "BACKLOG.md",
    "roadmaps.md",
}


def find_deploy_root(start: Path) -> Path | None:
    for base in (start, *start.parents):
        candidate = base / DEPLOY_DIRNAME
        if candidate.is_dir():
            return candidate
    return None


def check_naming(root: Path) -> list[str]:
    """INV-7: every rule/domain/artifact file is <id>-<short-summary>.md."""
    errors: list[str] = []
    checked_dirs = ("rules", "domains", "requirements", "features",
                    "development", "work-items")
    for sub in checked_dirs:
        d = root / sub
        if not d.is_dir():
            continue
        for f in d.rglob("*.md"):
            name = f.name
            if name in INDEX_NAMES or TEMPLATE_RE.match(name):
                continue
            # Named roadmaps (development/roadmaps/<name>.md) are keyed by a
            # free-form name, not a sequential <id>-<summary> scheme — see
            # Rules-of-Rules.md §10.
            if f.parent.name == "roadmaps":
                continue
            if not NAME_RE.match(name) or BARE_ID_RE.search(name):
                errors.append(f"INV-7 naming: {f.relative_to(root)} is not "
                              f"<id>-<short-summary>.md")
    return errors


def check_single_rule_template(root: Path) -> list[str]:
    """INV-8: exactly one TEMPLATE-RULE.md, in rules/ root."""
    rules = root / "rules"
    if not rules.is_dir():
        return ["INV-8: rules/ directory is missing"]
    hits = list(rules.rglob("TEMPLATE-RULE.md"))
    errors = []
    if len(hits) != 1:
        errors.append(f"INV-8: expected exactly one TEMPLATE-RULE.md, found "
                      f"{len(hits)}")
    elif hits[0].parent != rules:
        errors.append("INV-8: TEMPLATE-RULE.md must live in rules/ root, "
                      f"found at {hits[0].relative_to(root)}")
    return errors


def check_rule_indexing(root: Path) -> list[str]:
    """INV-8: every rule file appears in the global rules.md index."""
    rules = root / "rules"
    global_index = rules / "rules.md"
    if not global_index.is_file():
        return ["INV-8: rules/rules.md global index is missing"]
    index_text = global_index.read_text(encoding="utf-8", errors="ignore")
    errors = []
    for f in rules.rglob("*.md"):
        if f.name in INDEX_NAMES or TEMPLATE_RE.match(f.name):
            continue
        stem = f.stem
        if stem not in index_text and f.name not in index_text:
            errors.append(f"INV-8 orphan: {f.relative_to(root)} not listed in "
                          f"rules/rules.md")
    return errors


def check_required_headings(root: Path) -> list[str]:
    """INV-8: rule docs carry ## Contents and ## Known Bugs — Quick Index."""
    rules = root / "rules"
    errors = []
    for f in rules.rglob("*.md"):
        if f.name in INDEX_NAMES or TEMPLATE_RE.match(f.name):
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "## Contents" not in text:
            errors.append(f"INV-8 heading: {f.relative_to(root)} missing "
                          f"'## Contents'")
        if "Known Bugs" not in text:
            errors.append(f"INV-8 heading: {f.relative_to(root)} missing "
                          f"'## Known Bugs — Quick Index'")
    return errors


def check_backlog_exists(root: Path) -> list[str]:
    """INV-14: development/BACKLOG.md always exists."""
    backlog = root / "development" / "BACKLOG.md"
    if not backlog.is_file():
        return ["INV-14: development/BACKLOG.md is missing — seed it from "
                "templates/backlog.template.md"]
    return []


def check_roadmaps_index_exists(root: Path) -> list[str]:
    """INV-15: development/roadmaps/roadmaps.md index always exists."""
    index = root / "development" / "roadmaps" / "roadmaps.md"
    if not index.is_file():
        return ["INV-15: development/roadmaps/roadmaps.md is missing — seed "
                "development/roadmaps/ from templates/roadmap.template.md"]
    return []


def check_users_and_roles_exist(root: Path) -> list[str]:
    """INV-16: development/users.json + development/roles.json always
    exist, and users.json has at least one active user."""
    errors: list[str] = []
    users_path = root / "development" / "users.json"
    roles_path = root / "development" / "roles.json"

    if not roles_path.is_file():
        errors.append("INV-16: development/roles.json is missing — seed it "
                      "from templates/roles.template.json")

    if not users_path.is_file():
        errors.append("INV-16: development/users.json is missing — seed it "
                      "from templates/users.template.json")
        return errors

    try:
        data = json.loads(users_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"INV-16: development/users.json is not valid JSON: {exc}")
        return errors

    users = data.get("users", []) if isinstance(data, dict) else []
    if not any(isinstance(u, dict) and u.get("active") for u in users):
        errors.append("INV-16: development/users.json has no active user — "
                      "a project must have at least one (/user-add)")
    return errors


def check_journal_exists(root: Path) -> list[str]:
    """INV-17: development/journal.jsonl always exists; every non-blank
    line is a well-formed, schema-complete entry."""
    journal = root / "development" / "journal.jsonl"
    if not journal.is_file():
        return ["INV-17: development/journal.jsonl is missing — seed it "
                "(empty) from templates/journal.template.jsonl"]

    errors: list[str] = []
    text = journal.read_text(encoding="utf-8", errors="ignore")
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"INV-17: journal.jsonl:{lineno} is not valid JSON: {exc}")
            continue
        if not isinstance(entry, dict):
            errors.append(f"INV-17: journal.jsonl:{lineno} is not a JSON object")
            continue
        for field in JOURNAL_REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"INV-17: journal.jsonl:{lineno} missing "
                              f"field '{field}'")
        files = entry.get("files")
        if isinstance(files, list):
            for f in files:
                if not isinstance(f, dict) or "path" not in f:
                    errors.append(f"INV-17: journal.jsonl:{lineno} has a "
                                  f"files[] entry missing 'path'")
                    continue
                for side in ("before", "after"):
                    val = f.get(side)
                    if val is not None and not HASH_RE.match(str(val)):
                        errors.append(
                            f"INV-17: journal.jsonl:{lineno} {f.get('path')} "
                            f"'{side}' is not a 40-hex git hash or null"
                        )
    return errors


def main() -> int:
    root = find_deploy_root(Path.cwd())
    if root is None:
        # No deployment in this repo — nothing to validate, not a failure.
        print(f"no {DEPLOY_DIRNAME}/ found; skipping deployment validation")
        return 0

    errors: list[str] = []
    errors += check_naming(root)
    errors += check_single_rule_template(root)
    errors += check_rule_indexing(root)
    errors += check_required_headings(root)
    errors += check_backlog_exists(root)
    errors += check_roadmaps_index_exists(root)
    errors += check_users_and_roles_exist(root)
    errors += check_journal_exists(root)

    if errors:
        print(f"catalyst deployment validation FAILED ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"catalyst deployment at {root} is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
