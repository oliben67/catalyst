import json
import zipfile
from pathlib import Path

import package_release as pr


def test_package_release_framework_and_modules(tmp_path: Path, monkeypatch):
    # Setup dummy root structure
    (tmp_path / "version.txt").write_text("0.33.0\n")

    fw_dir = tmp_path / "framework"
    fw_dir.mkdir()
    (fw_dir / "README.md").write_text("# Catalyst Framework\n")
    (fw_dir / "INVARIANTS.md").write_text("# Invariants\n")

    mod_dir = fw_dir / "modules" / "software-engineering"
    mod_dir.mkdir(parents=True)
    (mod_dir / "version.txt").write_text("1.0.0\n")
    (mod_dir / "module.yaml").write_text("id: software-engineering\n")
    (mod_dir / "README.md").write_text("# Module\n")

    # Mock run_cmd to prevent git push in unit test
    monkeypatch.setattr(pr, "run_cmd", lambda cmd, cwd: "")

    # Run release packaging
    pr.package_software_engineering_module(tmp_path)
    pr.package_framework(tmp_path)

    # 1. Verify module output
    mod_release_dir = mod_dir / "catalyst" / "modules" / "software-engineering" / "v1.0.0"
    assert mod_release_dir.is_dir()

    manifest_file = mod_release_dir / "manifest.json"
    assert manifest_file.is_file()
    manifest_data = json.loads(manifest_file.read_text())
    assert manifest_data["id"] == "software-engineering"
    assert manifest_data["version"] == "1.0.0"

    zip_file = mod_release_dir / "software-engineering-v1.0.0.zip"
    assert zip_file.is_file()
    with zipfile.ZipFile(zip_file) as zf:
        namelist = zf.namelist()
        assert "manifest.json" in namelist
        assert "module.yaml" in namelist

    # 2. Verify framework output
    fw_release_dir = tmp_path / "catalyst" / "framework" / "v0.33.0"
    assert fw_release_dir.is_dir()

    fw_manifest_file = fw_release_dir / "manifest.json"
    assert fw_manifest_file.is_file()
    fw_manifest_data = json.loads(fw_manifest_file.read_text())
    assert fw_manifest_data["id"] == "catalyst-framework"
    assert fw_manifest_data["version"] == "0.33.0"

    fw_zip_file = fw_release_dir / "framework-v0.33.0.zip"
    assert fw_zip_file.is_file()
    with zipfile.ZipFile(fw_zip_file) as zf:
        namelist = zf.namelist()
        assert "manifest.json" in namelist
        assert "README.md" in namelist
        assert "INVARIANTS.md" in namelist
        assert not any(n.startswith("modules/") for n in namelist)

    # 3. Verify cantica-tech deployment
    cantica_dir = tmp_path.parent / "cantica-tech"
    cantica_dir.mkdir()
    pr.deploy_to_cantica_tech(tmp_path)

    cantica_fw_dir = cantica_dir / "catalyst" / "framework" / "v0.33.0"
    assert (cantica_fw_dir / "manifest.json").is_file()
    assert (cantica_fw_dir / "framework-v0.33.0.zip").is_file()

    cantica_mod_dir = cantica_dir / "catalyst" / "modules" / "software-engineering" / "v1.0.0"
    assert (cantica_mod_dir / "manifest.json").is_file()
    assert (cantica_mod_dir / "software-engineering-v1.0.0.zip").is_file()
