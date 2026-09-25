import json
import zipfile
from pathlib import Path

import package_release as pr


def test_package_release_kernel_and_modules(tmp_path: Path, monkeypatch):
    # Setup dummy workspace: catalyst, its sibling module repo, and cantica-tech
    workspace = tmp_path
    tmp_path = workspace / "catalyst"
    tmp_path.mkdir()
    (tmp_path / "version.txt").write_text("0.33.0\n")

    kernel_dir = tmp_path / "framework" / "kernel"
    kernel_dir.mkdir(parents=True)
    (kernel_dir / "README.md").write_text("# Catalyst Kernel\n")
    (kernel_dir / "INVARIANTS.md").write_text("# Invariants\n")

    mod_dir = workspace / "catalyst-software-engineering"
    mod_dir.mkdir(parents=True)
    (mod_dir / "version.txt").write_text("1.0.0\n")
    (mod_dir / "module.yaml").write_text("id: software-engineering\n")
    (mod_dir / "README.md").write_text("# Module\n")

    # Mock run_cmd to prevent git push in unit test
    monkeypatch.setattr(pr, "run_cmd", lambda cmd, cwd: "")

    # Run release packaging
    pr.package_software_engineering_module(tmp_path)
    pr.package_kernel(tmp_path)

    # 1. Verify module output
    mod_release_dir = mod_dir / "catalyst" / "modules" / "software-engineering" / "v1.0.0"
    assert mod_release_dir.is_dir()

    manifest_file = mod_release_dir / "manifest.json"
    assert manifest_file.is_file()
    manifest_data = json.loads(manifest_file.read_text())
    assert manifest_data["id"] == "software-engineering"
    assert manifest_data["version"] == "1.0.0"
    assert manifest_data["kernelVersion"] == ">=0.33.0"
    assert "frameworkVersion" not in manifest_data

    zip_file = mod_release_dir / "software-engineering-v1.0.0.zip"
    assert zip_file.is_file()
    with zipfile.ZipFile(zip_file) as zf:
        namelist = zf.namelist()
        assert "manifest.json" in namelist
        assert "module.yaml" in namelist

    # 2. Verify kernel output
    kernel_release_dir = tmp_path / "catalyst" / "kernel" / "v0.33.0"
    assert kernel_release_dir.is_dir()

    kernel_manifest_file = kernel_release_dir / "manifest.json"
    assert kernel_manifest_file.is_file()
    kernel_manifest_data = json.loads(kernel_manifest_file.read_text())
    assert kernel_manifest_data["id"] == "catalyst-kernel"
    assert kernel_manifest_data["version"] == "0.33.0"

    kernel_zip_file = kernel_release_dir / "kernel-v0.33.0.zip"
    assert kernel_zip_file.is_file()
    with zipfile.ZipFile(kernel_zip_file) as zf:
        namelist = zf.namelist()
        assert "manifest.json" in namelist
        assert "README.md" in namelist
        assert "INVARIANTS.md" in namelist
        assert not any(n.startswith("modules/") for n in namelist)

    # 3. Verify cantica-tech deployment
    cantica_dir = tmp_path.parent / "cantica-tech"
    cantica_dir.mkdir()
    pr.deploy_to_cantica_tech(tmp_path)

    cantica_kernel_dir = cantica_dir / "catalyst" / "kernel" / "v0.33.0"
    assert (cantica_kernel_dir / "manifest.json").is_file()
    assert (cantica_kernel_dir / "kernel-v0.33.0.zip").is_file()

    cantica_mod_dir = cantica_dir / "catalyst" / "modules" / "software-engineering" / "v1.0.0"
    assert (cantica_mod_dir / "manifest.json").is_file()
    assert (cantica_mod_dir / "software-engineering-v1.0.0.zip").is_file()


def test_package_module_skipped_when_not_checked_out(tmp_path: Path):
    root = tmp_path / "catalyst"
    root.mkdir()
    (root / "version.txt").write_text("0.35.0\n")
    assert pr.package_software_engineering_module(root) is None
