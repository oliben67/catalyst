from pathlib import Path

import check_deployment as cd


def make_valid_deployment(tmp_path: Path) -> Path:
    """A minimal `.catalyst-proj/` tree that satisfies every check in
    check_deployment.py, so each test can start from a known-good baseline
    and break exactly one thing."""
    root = tmp_path / ".catalyst-proj"
    rules = root / "rules"
    business = rules / "business"
    business.mkdir(parents=True)

    (rules / "TEMPLATE-RULE.md").write_text("# Rule template\n")
    (rules / "rules.md").write_text(
        "# Rules index\n\n- br-AUTH-001-login-flow\n"
    )
    (business / "br-AUTH-001-login-flow.md").write_text(
        "# br-AUTH-001-login-flow\n\n"
        "## Contents\n\n...\n\n"
        "## Known Bugs — Quick Index\n\n(none)\n"
    )
    return root


def test_find_deploy_root_locates_from_nested_dir(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    nested = root / "rules" / "business"
    assert cd.find_deploy_root(nested) == root


def test_find_deploy_root_returns_none_when_absent(tmp_path: Path):
    assert cd.find_deploy_root(tmp_path) is None


def test_valid_deployment_has_no_errors(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    assert cd.check_naming(root) == []
    assert cd.check_single_rule_template(root) == []
    assert cd.check_rule_indexing(root) == []
    assert cd.check_required_headings(root) == []


def test_check_naming_rejects_bare_id_filename(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    bad = root / "rules" / "business" / "br-AUTH-002.md"
    bad.write_text("# bare id, no summary\n")
    errors = cd.check_naming(root)
    assert any("br-AUTH-002.md" in e for e in errors)


def test_check_naming_ignores_index_and_template_files(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    # rules.md and TEMPLATE-RULE.md are already present and bare-named;
    # a clean tree must not flag them.
    assert cd.check_naming(root) == []


def test_check_single_rule_template_missing(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "TEMPLATE-RULE.md").unlink()
    errors = cd.check_single_rule_template(root)
    assert any("expected exactly one" in e for e in errors)


def test_check_single_rule_template_duplicated(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "business" / "TEMPLATE-RULE.md").write_text("dup\n")
    errors = cd.check_single_rule_template(root)
    assert any("expected exactly one" in e for e in errors)


def test_check_single_rule_template_wrong_location(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "TEMPLATE-RULE.md").unlink()
    (root / "rules" / "business" / "TEMPLATE-RULE.md").write_text("misplaced\n")
    errors = cd.check_single_rule_template(root)
    assert any("must live in rules/ root" in e for e in errors)


def test_check_single_rule_template_missing_rules_dir(tmp_path: Path):
    root = tmp_path / ".catalyst-proj"
    root.mkdir()
    errors = cd.check_single_rule_template(root)
    assert errors == ["INV-8: rules/ directory is missing"]


def test_check_rule_indexing_flags_orphan_rule(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "business" / "br-AUTH-002-logout-flow.md").write_text(
        "# br-AUTH-002-logout-flow\n\n## Contents\n\n## Known Bugs — Quick Index\n"
    )
    errors = cd.check_rule_indexing(root)
    assert any("br-AUTH-002-logout-flow" in e and "orphan" in e for e in errors)


def test_check_rule_indexing_missing_global_index(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "rules.md").unlink()
    errors = cd.check_rule_indexing(root)
    assert any("rules/rules.md global index is missing" in e for e in errors)


def test_check_required_headings_missing_contents(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    rule = root / "rules" / "business" / "br-AUTH-001-login-flow.md"
    rule.write_text("# br-AUTH-001-login-flow\n\n## Known Bugs — Quick Index\n")
    errors = cd.check_required_headings(root)
    assert any("missing '## Contents'" in e for e in errors)


def test_check_required_headings_missing_known_bugs(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    rule = root / "rules" / "business" / "br-AUTH-001-login-flow.md"
    rule.write_text("# br-AUTH-001-login-flow\n\n## Contents\n")
    errors = cd.check_required_headings(root)
    assert any("missing '## Known Bugs" in e for e in errors)


def test_main_returns_zero_when_no_deployment(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cd.main() == 0
    assert "skipping deployment validation" in capsys.readouterr().out


def test_main_returns_zero_for_valid_deployment(tmp_path: Path, monkeypatch):
    make_valid_deployment(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert cd.main() == 0


def test_main_returns_one_for_broken_deployment(tmp_path: Path, monkeypatch):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "TEMPLATE-RULE.md").unlink()
    monkeypatch.chdir(tmp_path)
    assert cd.main() == 1
