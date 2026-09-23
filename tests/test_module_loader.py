from pathlib import Path
from module_loader import (
    get_active_etds,
    get_default_software_engineering_manifest,
    get_grounding_type,
    load_module,
    resolve_command,
)


def test_default_software_engineering_manifest():
    manifest = get_default_software_engineering_manifest()
    assert manifest.id == "software-engineering"
    assert manifest.grounding_type == "rule"

    etds = get_active_etds(manifest)
    assert "REQ" in etds
    assert "BUG" in etds
    assert "TEST" in etds
    assert "STEP" in etds
    assert "FEAT" in etds

    req_etd = etds["REQ"]
    assert req_etd.id_prefix == "REQ"
    assert req_etd.folder == "requirements"
    assert req_etd.grounding == "required"
    assert req_etd.grounding_field == "Targets"

    step_etd = etds["STEP"]
    assert step_etd.grounding == "inherited"
    assert step_etd.grounding_field == "Parent"

    feat_etd = etds["FEAT"]
    assert feat_etd.grounding == "none"

    assert get_grounding_type(manifest) == "rule"


def test_resolve_command():
    manifest = get_default_software_engineering_manifest()
    cmd = resolve_command(manifest, "/create-req")
    assert cmd is not None
    assert cmd.name == "create-req"

    cmd2 = resolve_command(manifest, "check-rules")
    assert cmd2 is not None
    assert cmd2.name == "check-rules"

    assert resolve_command(manifest, "unknown-cmd") is None


def test_load_module_fallback(tmp_path: Path):
    manifest = load_module(tmp_path)
    assert manifest.id == "software-engineering"
    assert "REQ" in manifest.entity_types


def test_load_bundled_software_engineering_module():
    repo_root = Path(__file__).resolve().parent.parent
    manifest = load_module(project_root=repo_root, module_id="software-engineering")
    assert manifest.id == "software-engineering"
    assert "REQ" in manifest.entity_types
    assert "BUG" in manifest.entity_types
    assert "TEST" in manifest.entity_types
    assert manifest.entity_types["REQ"].folder == "requirements"


def test_load_sample_process_module():
    repo_root = Path(__file__).resolve().parent.parent
    manifest = load_module(project_root=repo_root, module_id="sample-process")
    assert manifest.id == "sample-process"
    assert manifest.grounding_type == "policy"
    assert "POLICY" in manifest.entity_types
    assert "TASK" in manifest.entity_types
    assert manifest.entity_types["TASK"].grounding == "required"
    assert manifest.entity_types["TASK"].grounding_field == "Policy"


