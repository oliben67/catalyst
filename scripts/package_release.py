#!/usr/bin/env python3
"""Package framework and modules into versioned zipped archives with manifests.

1. Module software-engineering:
   - Zips the module contents (excluding .git, node_modules, catalyst output).
   - Includes manifest.json inside the zip and alongside it.
   - Saves to framework/modules/software-engineering/catalyst/module/software-engineering/v[version]/
   - Commits and pushes changes to origin main for the submodule.

2. Catalyst Framework (without modules):
   - Zips framework contents excluding framework/modules/.
   - Includes manifest.json inside the zip and alongside it.
   - Saves to catalyst/framework/v[version]/ at the root workspace.
"""
from __future__ import annotations

import json
import os
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_cmd(cmd: list[str], cwd: Path) -> str:
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=True)
    return res.stdout.strip()


def package_software_engineering_module(root: Path) -> Path:
    module_dir = root / "framework" / "modules" / "software-engineering"
    version_file = module_dir / "version.txt"
    version = version_file.read_text(encoding="utf-8").strip() if version_file.is_file() else "1.0.0"

    fw_version_file = root / "version.txt"
    fw_version = fw_version_file.read_text(encoding="utf-8").strip() if fw_version_file.is_file() else "0.33.0"

    dest_dir = module_dir / "catalyst" / "module" / "software-engineering" / f"v{version}"
    dest_dir.mkdir(parents=True, exist_ok=True)

    manifest_data = {
        "id": "software-engineering",
        "name": "Software Engineering Process Module",
        "version": version,
        "description": "Standard software engineering process module governing rules, requirements, bugs, tests, steps, features, roadmaps, workflows, and reconciliations.",
        "frameworkVersion": f">={fw_version}",
        "entry": "ui/index.js"
    }

    manifest_json_bytes = json.dumps(manifest_data, indent=2).encode("utf-8")

    # Save manifest.json outside zip
    manifest_file = dest_dir / "manifest.json"
    manifest_file.write_bytes(manifest_json_bytes)

    # Save zip
    zip_path = dest_dir / f"software-engineering-v{version}.zip"
    canonical_zip_path = dest_dir / "software-engineering.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add manifest.json to zip
        zf.writestr("manifest.json", manifest_json_bytes)

        # Add module contents
        for file in module_dir.rglob("*"):
            if not file.is_file():
                continue
            rel_path = file.relative_to(module_dir)
            parts = rel_path.parts
            if any(p.startswith(".") or p in ("node_modules", "dist", "catalyst") for p in parts):
                continue
            zf.write(file, arcname=str(rel_path))

    # Also create canonical software-engineering.zip copy
    canonical_zip_path.write_bytes(zip_path.read_bytes())

    print(f"Packaged software-engineering module v{version} -> {dest_dir}")

    # Commit and push in submodule
    try:
        run_cmd(["git", "add", "catalyst"], cwd=module_dir)
        status = run_cmd(["git", "status", "--porcelain"], cwd=module_dir)
        if status:
            run_cmd(["git", "commit", "-m", f"Release software-engineering module v{version}"], cwd=module_dir)
            run_cmd(["git", "push", "origin", "main"], cwd=module_dir)
            print("Committed and pushed module release to git@github.com:oliben67/calatalyst-software-engineering.git")
        else:
            print("No changes to commit in software-engineering module repository.")
    except Exception as exc:
        print(f"Warning: Git commit/push in module repository failed: {exc}")

    return dest_dir


def package_framework(root: Path) -> Path:
    fw_dir = root / "framework"
    fw_version_file = root / "version.txt"
    fw_version = fw_version_file.read_text(encoding="utf-8").strip() if fw_version_file.is_file() else "0.33.0"

    dest_dir = root / "catalyst" / "framework" / f"v{fw_version}"
    dest_dir.mkdir(parents=True, exist_ok=True)

    manifest_data = {
        "id": "catalyst-framework",
        "name": "Catalyst Framework",
        "version": fw_version,
        "description": "Core Catalyst Framework specification, templates, definitions, and plugins without modules."
    }

    manifest_json_bytes = json.dumps(manifest_data, indent=2).encode("utf-8")

    # Save manifest.json outside zip
    manifest_file = dest_dir / "manifest.json"
    manifest_file.write_bytes(manifest_json_bytes)

    # Save zip
    zip_path = dest_dir / f"framework-v{fw_version}.zip"
    canonical_zip_path = dest_dir / "framework.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add manifest.json to zip
        zf.writestr("manifest.json", manifest_json_bytes)

        # Add framework contents EXCLUDING modules/
        for file in fw_dir.rglob("*"):
            if not file.is_file():
                continue
            rel_path = file.relative_to(fw_dir)
            parts = rel_path.parts
            if parts[0] == "modules" or any(p.startswith(".") or p in ("node_modules", "dist", "catalyst") for p in parts):
                continue
            zf.write(file, arcname=str(rel_path))

    # Also create canonical framework.zip copy
    canonical_zip_path.write_bytes(zip_path.read_bytes())

    print(f"Packaged framework (without modules) v{fw_version} -> {dest_dir}")
    return dest_dir


def deploy_to_cantica_tech(root: Path) -> Path | None:
    cantica_dir = root.parent / "cantica-tech"
    if not cantica_dir.is_dir():
        print(f"Warning: cantica-tech repository directory not found at {cantica_dir}")
        return None

    fw_version_file = root / "version.txt"
    fw_version = fw_version_file.read_text(encoding="utf-8").strip() if fw_version_file.is_file() else "0.34.0"

    module_dir = root / "framework" / "modules" / "software-engineering"
    version_file = module_dir / "version.txt"
    mod_version = version_file.read_text(encoding="utf-8").strip() if version_file.is_file() else "1.0.0"

    # Source directories
    fw_src = root / "catalyst" / "framework" / f"v{fw_version}"
    mod_src = module_dir / "catalyst" / "module" / "software-engineering" / f"v{mod_version}"

    # Target directories in cantica-tech
    fw_dest = cantica_dir / "catalyst" / "framework" / f"v{fw_version}"
    mod_dest = cantica_dir / "catalyst" / "module" / "software-engineering" / f"v{mod_version}"

    fw_dest.mkdir(parents=True, exist_ok=True)
    mod_dest.mkdir(parents=True, exist_ok=True)

    # Copy release files
    for src, dest in [(fw_src, fw_dest), (mod_src, mod_dest)]:
        if src.is_dir():
            for f in src.glob("*"):
                if f.is_file():
                    (dest / f.name).write_bytes(f.read_bytes())

    print(f"Deployed release artifacts to cantica-tech repository at {cantica_dir}")

    # Commit and push in cantica-tech
    try:
        run_cmd(["git", "add", "catalyst"], cwd=cantica_dir)
        status = run_cmd(["git", "status", "--porcelain"], cwd=cantica_dir)
        if status:
            run_cmd(["git", "commit", "-m", f"Deploy release: framework v{fw_version}, software-engineering module v{mod_version}"], cwd=cantica_dir)
            run_cmd(["git", "push", "origin", "main"], cwd=cantica_dir)
            print("Committed and pushed release to git@github.com:oliben67/cantica-tech.git")
        else:
            print("No changes to commit in cantica-tech repository.")
    except Exception as exc:
        print(f"Warning: Git commit/push in cantica-tech repository failed: {exc}")

    return cantica_dir


def main() -> int:
    print("Starting release packaging...")
    package_software_engineering_module(ROOT)
    package_framework(ROOT)
    deploy_to_cantica_tech(ROOT)
    print("Release packaging and deployment completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
