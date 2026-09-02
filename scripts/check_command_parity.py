#!/usr/bin/env python3
"""Validate .claude/commands/*.md against CODE-OF-CONDUCT.md's §4 command list.

CLAUDE.md's own instructions require one native command file per §4 entry,
kept in sync so a deployment's actual command set never silently drifts from
its own documented spec. Nothing previously checked this mechanically.

`.claude/commands/` lives in the outer project repo; §4's canonical list
lives in the deployed CODE-OF-CONDUCT.md, resolved via the same pointer-file
mechanism check_deployment.py already implements (`find_deploy_root`) — the
two roots are usually different directories (agent-owned space vs. the
project tree), so both are resolved independently rather than assumed to
coincide.

`dogfood.md` is the one documented exception: catalyst-development-only,
deliberately absent from §4 (Rules-of-Rules.md §13).

Exit 0 = clean (including when no deployment resolves), exit 1 = drift found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from check_deployment import find_deploy_root

ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = ROOT / ".claude" / "commands"
DOGFOOD_EXCEPTION = "dogfood"

SECTION_HEADING_RE = re.compile(r"^## \d+\. ")
SECTION4_RE = re.compile(r"^## 4\. ")
# Only a leading `/name` right after the opening backtick is a real command
# reference — this deliberately excludes indented sub-bullets like
# /catalyzer's `list` / `activate <name> <version>` (no leading slash) and
# any bold prose paragraph mentioning a command name mid-sentence, since
# both are filtered out upstream by the column-0 "- " bullet check below.
COMMAND_TOKEN_RE = re.compile(r"`/([a-z][a-z0-9-]*)")


def extract_section4_commands(coc_text: str) -> set[str] | None:
    """Command names referenced by top-level bullets under CODE-OF-CONDUCT.md's
    '## 4.' heading, up to the next '## N.' heading. Returns None if no
    '## 4.' heading is found at all (reported distinctly from an empty
    section by the caller)."""
    lines = coc_text.splitlines()
    start = end = None
    for i, line in enumerate(lines):
        if SECTION4_RE.match(line):
            start = i
        elif start is not None and SECTION_HEADING_RE.match(line):
            end = i
            break
    if start is None:
        return None

    names: set[str] = set()
    for line in lines[start:end or len(lines)]:
        # Column-0 "- " only: a 2-space-indented sub-bullet (/catalyzer's
        # subcommands) or a bold prose paragraph naming commands mid-sentence
        # (e.g. the work-items-are-plugin-territory callout) must not count.
        if line.startswith("- "):
            names.update(COMMAND_TOKEN_RE.findall(line))
    return names


def find_command_files(commands_dir: Path) -> set[str]:
    if not commands_dir.is_dir():
        return set()
    return {f.stem for f in commands_dir.glob("*.md")} - {DOGFOOD_EXCEPTION}


def check_command_parity(commands_dir: Path, code_of_conduct: Path) -> list[str]:
    if not code_of_conduct.is_file():
        return [f"command parity: {code_of_conduct} is missing"]

    coc_names = extract_section4_commands(
        code_of_conduct.read_text(encoding="utf-8", errors="ignore")
    )
    if coc_names is None:
        return [f"command parity: {code_of_conduct} has no '## 4.' section"]

    file_names = find_command_files(commands_dir)
    errors: list[str] = []
    for name in sorted(coc_names - file_names):
        errors.append(
            f"command parity: CODE-OF-CONDUCT.md §4 references /{name} but "
            f".claude/commands/{name}.md is missing"
        )
    for name in sorted(file_names - coc_names):
        errors.append(
            f"command parity: .claude/commands/{name}.md exists but is not "
            f"referenced in CODE-OF-CONDUCT.md §4"
        )
    return errors


def main() -> int:
    root = find_deploy_root(Path.cwd())
    if root is None:
        print("no *.catalyst pointer or .criterion/ found; skipping command "
              "parity validation")
        return 0

    errors = check_command_parity(COMMANDS_DIR, root / "CODE-OF-CONDUCT.md")

    if errors:
        print(f"command parity validation FAILED ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"command parity valid ({len(find_command_files(COMMANDS_DIR))} "
          f"command(s) checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
