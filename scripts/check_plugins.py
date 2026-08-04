#!/usr/bin/env python3
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITMODULES = ROOT / '.gitmodules'
PLUGINS_DIR = ROOT / 'plugins'


def run_git(args: list[str]) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True)


def load_submodule_entries() -> list[tuple[str, str]]:
    if not GITMODULES.exists():
        return []
    entries: list[tuple[str, str]] = []
    current = None
    for raw in GITMODULES.read_text().splitlines():
        line = raw.strip()
        if line.startswith('[') and line.endswith(']'):
            current = line[1:-1]
        elif current and line.startswith('path = '):
            path = line.split('=', 1)[1].strip()
            entries.append((current, path))
    return entries


def validate_plugin_structure() -> list[str]:
    errors: list[str] = []
    plugin_root = PLUGINS_DIR / 'repository'
    if not plugin_root.exists():
        return ['plugins/repository directory is missing']

    for path in sorted(plugin_root.iterdir()):
        if not path.is_dir():
            continue
        if path.name.startswith('.'):
            continue
        readme = path / 'README.md'
        contract = path / 'working-contract.md'
        if not readme.exists():
            errors.append(f'{path.relative_to(ROOT)}/README.md is missing')
        if not contract.exists():
            errors.append(f'{path.relative_to(ROOT)}/working-contract.md is missing')

    return errors


def validate_submodule_policy() -> list[str]:
    errors: list[str] = []
    entries = load_submodule_entries()
    plugin_entries = [(name, path) for name, path in entries if path.startswith('plugins/')]
    for _, path in plugin_entries:
        if not (ROOT / path).exists():
            errors.append(f'{path} is not present in the workspace')
    return errors


def validate_plugin_sources() -> list[str]:
    errors: list[str] = []
    entries = load_submodule_entries()
    plugin_paths = {path for _, path in entries if path.startswith('plugins/')}
    try:
        status = run_git(['submodule', 'status'])
    except subprocess.CalledProcessError as exc:
        return [f'git submodule status failed: {exc}']

    for line in status.splitlines():
        if not line.strip():
            continue
        prefix = line[0]
        path = line[1:].split()[1]
        if path in plugin_paths and prefix == '-':
            errors.append(f'{path} is not initialized or checked out')
    return errors


def main() -> int:
    errors = []
    errors.extend(validate_plugin_structure())
    errors.extend(validate_submodule_policy())
    errors.extend(validate_plugin_sources())

    if errors:
        print('Plugin rule validation failed:')
        for error in errors:
            print(f'- {error}')
        return 1

    print('Plugin rules validated successfully.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
