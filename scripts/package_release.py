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

    dest_dir = module_dir / "catalyst" / "modules" / "software-engineering" / f"v{version}"
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

    # Remove legacy unversioned zip if present
    canonical_zip_path = dest_dir / "software-engineering.zip"
    if canonical_zip_path.is_file():
        canonical_zip_path.unlink()

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

    # Remove legacy unversioned zip if present
    canonical_zip_path = dest_dir / "framework.zip"
    if canonical_zip_path.is_file():
        canonical_zip_path.unlink()

    print(f"Packaged framework (without modules) v{fw_version} -> {dest_dir}")
    return dest_dir


def update_cantica_tech_readmes(cantica_dir: Path) -> None:
    catalyst_dir = cantica_dir / "catalyst"
    catalyst_dir.mkdir(parents=True, exist_ok=True)

    # 1. Root cantica-tech/README.md
    root_readme = cantica_dir / "README.md"
    root_readme.write_text(
        "# CanticaTech Release Artifacts Repository\n\n"
        "This repository serves as the central distribution repository for CanticaTech release artifacts, specifications, framework releases, and process modules.\n\n"
        "## Repository Structure\n\n"
        "- **[catalyst/](catalyst/README.md)**: Official release archives, versioned manifests, and distribution packages for the Catalyst Framework and process modules.\n",
        encoding="utf-8"
    )

    # 2. catalyst/README.md
    cat_readme = catalyst_dir / "README.md"
    cat_readme.write_text(
        "# Catalyst Framework & Module Releases\n\n"
        "This directory contains official versioned release packages and manifests for the Catalyst Framework specification and its associated process modules.\n\n"
        "## Release Categories\n\n"
        "- **[framework/](framework/README.md)**: Catalyst Framework core releases (specifications, templates, definitions, and plugins without modules).\n"
        "- **[modules/](modules/README.md)**: Catalyst Process Modules (e.g. Software Engineering process module).\n",
        encoding="utf-8"
    )

    # 3. catalyst/framework/README.md
    fw_dir = catalyst_dir / "framework"
    fw_dir.mkdir(parents=True, exist_ok=True)
    fw_releases = []
    for v_dir in sorted(fw_dir.glob("v*"), reverse=True):
        if not v_dir.is_dir():
            continue
        manifest_file = v_dir / "manifest.json"
        if manifest_file.is_file():
            try:
                m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
                v_name = v_dir.name
                version = m_data.get("version", v_name.lstrip("v"))
                desc = m_data.get("description", "Catalyst Framework release")
                zip_file = f"{v_name}/framework-{v_name}.zip"
                manifest_rel = f"{v_name}/manifest.json"
                fw_releases.append(f"| `{v_name}` | [`{manifest_rel}`]({manifest_rel}) | [`{zip_file}`]({zip_file}) | {desc} |")
            except Exception:
                pass

    fw_readme_lines = [
        "# Catalyst Framework Releases",
        "",
        "This directory contains versioned releases of the Catalyst Framework (core specification, templates, definitions, and plugins without modules).",
        "",
        "## Available Framework Releases",
        "",
        "| Version | Manifest | Archive | Description |",
        "| ------- | -------- | ------- | ----------- |",
    ]
    if fw_releases:
        fw_readme_lines.extend(fw_releases)
    else:
        fw_readme_lines.append("| *(none)* | - | - | - |")

    (fw_dir / "README.md").write_text("\n".join(fw_readme_lines) + "\n", encoding="utf-8")

    # 4. catalyst/modules/README.md & 5. catalyst/modules/<module>/README.md
    mod_root_dir = catalyst_dir / "modules"
    mod_root_dir.mkdir(parents=True, exist_ok=True)

    module_overview_rows = []

    for mod_dir in sorted(mod_root_dir.iterdir()):
        if not mod_dir.is_dir():
            continue
        mod_id = mod_dir.name
        mod_v_dirs = sorted(mod_dir.glob("v*"), reverse=True)
        if not mod_v_dirs:
            continue

        mod_releases = []
        latest_info = None

        for v_dir in mod_v_dirs:
            if not v_dir.is_dir():
                continue
            manifest_file = v_dir / "manifest.json"
            if manifest_file.is_file():
                try:
                    m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
                    v_name = v_dir.name
                    mod_name = m_data.get("name", mod_id)
                    fw_req = m_data.get("frameworkVersion", "*")
                    desc = m_data.get("description", f"{mod_name} release")
                    zip_file = f"{v_name}/{mod_id}-{v_name}.zip"
                    manifest_rel = f"{v_name}/manifest.json"
                    mod_releases.append(f"| `{v_name}` | `{fw_req}` | [`{manifest_rel}`]({manifest_rel}) | [`{zip_file}`]({zip_file}) | {desc} |")

                    if latest_info is None:
                        latest_info = {
                            "name": mod_name,
                            "version": v_name,
                            "fw_req": fw_req,
                            "rel_dir": f"{mod_id}/",
                        }
                except Exception:
                    pass

        # Write module-specific README
        mod_readme_lines = [
            f"# {latest_info['name'] if latest_info else mod_id} Releases",
            "",
            f"This directory contains versioned releases for the `{mod_id}` process module.",
            "",
            "## Available Releases",
            "",
            "| Version | Framework Requirement | Manifest | Archive | Description |",
            "| ------- | --------------------- | -------- | ------- | ----------- |",
        ]
        if mod_releases:
            mod_readme_lines.extend(mod_releases)
        else:
            mod_readme_lines.append("| *(none)* | - | - | - | - |")

        (mod_dir / "README.md").write_text("\n".join(mod_readme_lines) + "\n", encoding="utf-8")

        if latest_info:
            module_overview_rows.append(
                f"| {latest_info['name']} | `{latest_info['version']}` | `{latest_info['fw_req']}` | [`{latest_info['rel_dir']}`]({latest_info['rel_dir']}README.md) |"
            )

    mod_overview_lines = [
        "# Catalyst Process Modules",
        "",
        "This directory contains versioned process modules for the Catalyst Framework.",
        "",
        "## Available Process Modules",
        "",
        "| Module | Latest Version | Framework Requirement | Directory |",
        "| ------ | -------------- | --------------------- | --------- |",
    ]
    if module_overview_rows:
        mod_overview_lines.extend(module_overview_rows)
    else:
        mod_overview_lines.append("| *(none)* | - | - | - |")

    (mod_root_dir / "README.md").write_text("\n".join(mod_overview_lines) + "\n", encoding="utf-8")


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
    mod_src = module_dir / "catalyst" / "modules" / "software-engineering" / f"v{mod_version}"

    # Target directories in cantica-tech
    fw_dest = cantica_dir / "catalyst" / "framework" / f"v{fw_version}"
    mod_dest = cantica_dir / "catalyst" / "modules" / "software-engineering" / f"v{mod_version}"

    fw_dest.mkdir(parents=True, exist_ok=True)
    mod_dest.mkdir(parents=True, exist_ok=True)

    # Copy release files and clean up obsolete ones
    for src, dest in [(fw_src, fw_dest), (mod_src, mod_dest)]:
        if src.is_dir():
            src_names = {f.name for f in src.glob("*") if f.is_file()}
            for f in dest.glob("*"):
                if f.is_file() and f.name not in src_names:
                    f.unlink()
            for f in src.glob("*"):
                if f.is_file():
                    (dest / f.name).write_bytes(f.read_bytes())

    # Update README documentation and release tables in cantica-tech
    update_cantica_tech_readmes(cantica_dir)

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
