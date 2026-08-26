import json
import shutil
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
    (rules / "templates").mkdir()

    (rules / "templates" / "TEMPLATE-RULE-v1.md").write_text("# Rule template\n")
    (rules / "rules.md").write_text(
        "# Rules index\n\n- br-AUTH-001-login-flow\n"
    )
    (business / "br-AUTH-001-login-flow.md").write_text(
        "# br-AUTH-001-login-flow\n\n"
        "## Contents\n\n...\n\n"
        "## Known Bugs — Quick Index\n\n(none)\n"
    )
    development = root / "development"
    development.mkdir()
    (development / "BACKLOG.md").write_text(
        "# Backlog\n\n**Last refreshed:** 2026-08-23 by `/show-backlog`.\n"
    )
    roadmaps = development / "roadmaps"
    roadmaps.mkdir()
    (roadmaps / "roadmaps.md").write_text("# Roadmaps index\n\n*(none)*\n")
    iam = root / "IAM"
    users_dir = iam / "users"
    roles_dir = iam / "roles"
    users_dir.mkdir(parents=True)
    roles_dir.mkdir()
    (users_dir / "users.json").write_text(json.dumps({
        "users": [
            {"name": "Ada", "roles": ["Developer"], "registered": "2026-08-23",
             "active": True, "notes": ""},
        ]
    }))
    (roles_dir / "roles.json").write_text(json.dumps({
        "roles": [{"name": "Developer", "actions": ["/create-bug"]}]
    }))
    (development / "journal.jsonl").write_text(
        json.dumps({
            "timestamp": "2026-08-23T19:00:00Z",
            "actor": "Ada",
            "command": "/create-bug",
            "action": "create",
            "artifact": "BUG-000001",
            "targets": ["br-AUTH-001"],
            "intent": ["fix a real bug"],
            "files": [
                {"path": "development/bugs/BUG-000001-x.md",
                 "before": None,
                 "after": "a" * 40},
            ],
        }) + "\n"
    )
    return root


def test_find_deploy_root_locates_from_nested_dir(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    nested = root / "rules" / "business"
    assert cd.find_deploy_root(nested) == root


def test_find_deploy_root_returns_none_when_absent(tmp_path: Path):
    assert cd.find_deploy_root(tmp_path) is None


def test_find_deploy_root_follows_pointer_file(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    agent_owned = tmp_path / "agent-space" / ".catalyst-proj"
    agent_owned.mkdir(parents=True)
    (project / "myapp.catalyst").write_text(json.dumps({
        "project_name": "myapp",
        "agent-source": str(agent_owned),
    }))
    assert cd.find_deploy_root(project) == agent_owned


def test_find_deploy_root_pointer_resolved_from_nested_dir(tmp_path: Path):
    project = tmp_path / "project"
    nested = project / "some" / "nested" / "dir"
    nested.mkdir(parents=True)
    agent_owned = tmp_path / "agent-space" / ".catalyst-proj"
    agent_owned.mkdir(parents=True)
    (project / "myapp.catalyst").write_text(json.dumps({
        "project_name": "myapp",
        "agent-source": str(agent_owned),
    }))
    assert cd.find_deploy_root(nested) == agent_owned


def test_find_deploy_root_falls_back_to_legacy_dir_on_stale_pointer(tmp_path: Path):
    """A pointer whose agent-source no longer exists (moved/deleted) must not
    mask a legacy in-tree .catalyst-proj/ that's actually still there."""
    root = make_valid_deployment(tmp_path)
    (tmp_path / "myapp.catalyst").write_text(json.dumps({
        "project_name": "myapp",
        "agent-source": str(tmp_path / "nowhere"),
    }))
    assert cd.find_deploy_root(tmp_path) == root


def test_find_deploy_root_ignores_malformed_pointer(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (tmp_path / "myapp.catalyst").write_text("not json{")
    assert cd.find_deploy_root(tmp_path) == root


def test_valid_deployment_has_no_errors(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    assert cd.check_naming(root) == []
    assert cd.check_single_rule_template(root) == []
    assert cd.check_rule_indexing(root) == []
    assert cd.check_required_headings(root) == []
    assert cd.check_backlog_exists(root) == []
    assert cd.check_roadmaps_index_exists(root) == []
    assert cd.check_users_and_roles_exist(root) == []
    assert cd.check_journal_exists(root) == []


def test_check_naming_rejects_bare_id_filename(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    bad = root / "rules" / "business" / "br-AUTH-002.md"
    bad.write_text("# bare id, no summary\n")
    errors = cd.check_naming(root)
    assert any("br-AUTH-002.md" in e for e in errors)


def test_check_naming_ignores_index_and_template_files(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    # rules.md and rules/templates/TEMPLATE-RULE-v1.md are already present
    # and bare-named; a clean tree must not flag them.
    assert cd.check_naming(root) == []


def test_check_naming_ignores_named_roadmap_files(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    # A named roadmap is keyed by a free-form name (Rules-of-Rules.md §10),
    # not the sequential <id>-<summary> scheme — a trailing-digits name like
    # this must not be flagged as a bare ID (INV-7) the way br-AUTH-002.md
    # would be.
    (root / "development" / "roadmaps" / "product-2026.md").write_text(
        "# product-2026\n"
    )
    assert cd.check_naming(root) == []


def test_check_single_rule_template_missing(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "templates" / "TEMPLATE-RULE-v1.md").unlink()
    errors = cd.check_single_rule_template(root)
    assert any("no TEMPLATE-RULE" in e for e in errors)


def test_check_single_rule_template_multiple_versions_is_fine(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    # INV-20: versioning means adding a new file, never editing in place —
    # v1 and v2 coexisting in templates/ is the normal, expected state.
    (root / "rules" / "templates" / "TEMPLATE-RULE-v2.md").write_text("v2\n")
    assert cd.check_single_rule_template(root) == []


def test_check_single_rule_template_wrong_location(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "business" / "TEMPLATE-RULE-v1.md").write_text("misplaced\n")
    errors = cd.check_single_rule_template(root)
    assert any("must live in rules/templates/" in e for e in errors)


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


def test_check_rule_indexing_ignores_domain_files(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    domains = root / "rules" / "domains"
    domains.mkdir()
    (domains / "br-AUTH-user-authentication.md").write_text(
        "# br-AUTH — User authentication\n\n**Document:** ...\n"
    )
    # Domain files are not rule documents (INV-20) — exempt from both the
    # rules.md orphan check and the ## Contents / Known Bugs heading check.
    assert cd.check_rule_indexing(root) == []
    assert cd.check_required_headings(root) == []


def test_check_naming_ignores_templates_catalog_files(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "rules" / "templates" / "templates-rule.md").write_text(
        "| Version | File | Timestamp | Notes |\n|---|---|---|---|\n"
        "| v1 | TEMPLATE-RULE-v1.md | 2026-08-23 | Initial version. |\n"
    )
    assert cd.check_naming(root) == []


def test_check_naming_ignores_tickets_boards_workflows_indexes(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    work_items = root / "work-items"
    (work_items / "tickets").mkdir(parents=True)
    (work_items / "tickets" / "tickets.md").write_text("# Tickets index\n")
    (work_items / "boards").mkdir(parents=True)
    (work_items / "boards" / "boards.md").write_text("# Boards index\n")
    (work_items / "workflows").mkdir(parents=True)
    (work_items / "workflows" / "workflows.md").write_text("# Workflows index\n")
    assert cd.check_naming(root) == []


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


def test_check_backlog_exists_missing(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "development" / "BACKLOG.md").unlink()
    errors = cd.check_backlog_exists(root)
    assert any("INV-14" in e and "development/BACKLOG.md is missing" in e
               for e in errors)


def test_check_backlog_exists_missing_development_dir(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    shutil.rmtree(root / "development")
    errors = cd.check_backlog_exists(root)
    assert any("INV-14" in e for e in errors)


def test_check_roadmaps_index_exists_missing(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "development" / "roadmaps" / "roadmaps.md").unlink()
    errors = cd.check_roadmaps_index_exists(root)
    assert any(
        "INV-15" in e and "development/roadmaps/roadmaps.md is missing" in e
        for e in errors
    )


def test_check_roadmaps_index_exists_missing_roadmaps_dir(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    shutil.rmtree(root / "development" / "roadmaps")
    errors = cd.check_roadmaps_index_exists(root)
    assert any("INV-15" in e for e in errors)


def test_check_roadmaps_index_exists_missing_development_dir(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    shutil.rmtree(root / "development")
    errors = cd.check_roadmaps_index_exists(root)
    assert any("INV-15" in e for e in errors)


def test_check_users_and_roles_exist_missing_users(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "IAM" / "users" / "users.json").unlink()
    errors = cd.check_users_and_roles_exist(root)
    assert any("INV-16" in e and "IAM/users/users.json is missing" in e
               for e in errors)
    assert not any("roles.json" in e for e in errors)


def test_check_users_and_roles_exist_missing_roles(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "IAM" / "roles" / "roles.json").unlink()
    errors = cd.check_users_and_roles_exist(root)
    assert any("INV-16" in e and "IAM/roles/roles.json is missing" in e
               for e in errors)
    assert not any("users.json is missing" in e for e in errors)


def test_check_users_and_roles_exist_missing_both(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "IAM" / "users" / "users.json").unlink()
    (root / "IAM" / "roles" / "roles.json").unlink()
    errors = cd.check_users_and_roles_exist(root)
    assert len(errors) == 2


def test_check_users_and_roles_exist_missing_iam_dir(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    shutil.rmtree(root / "IAM")
    errors = cd.check_users_and_roles_exist(root)
    assert len(errors) == 2


def test_check_users_and_roles_exist_no_active_user(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "IAM" / "users" / "users.json").write_text(json.dumps({
        "users": [
            {"name": "Ada", "roles": ["Developer"], "registered": "2026-08-23",
             "active": False, "notes": ""},
        ]
    }))
    errors = cd.check_users_and_roles_exist(root)
    assert any("INV-16" in e and "no active user" in e for e in errors)


def test_check_users_and_roles_exist_empty_users_array(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "IAM" / "users" / "users.json").write_text(json.dumps({"users": []}))
    errors = cd.check_users_and_roles_exist(root)
    assert any("no active user" in e for e in errors)


def test_check_users_and_roles_exist_invalid_json(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "IAM" / "users" / "users.json").write_text("{not valid json")
    errors = cd.check_users_and_roles_exist(root)
    assert any("not valid JSON" in e for e in errors)


def test_check_journal_exists_missing(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "development" / "journal.jsonl").unlink()
    errors = cd.check_journal_exists(root)
    assert any("INV-17" in e and "development/journal.jsonl is missing" in e
               for e in errors)


def test_check_journal_exists_empty_file_is_valid(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "development" / "journal.jsonl").write_text("")
    assert cd.check_journal_exists(root) == []


def test_check_journal_exists_rejects_malformed_json_line(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "development" / "journal.jsonl").write_text("{not valid json\n")
    errors = cd.check_journal_exists(root)
    assert any("journal.jsonl:1 is not valid JSON" in e for e in errors)


def test_check_journal_exists_rejects_non_object_line(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    (root / "development" / "journal.jsonl").write_text("[1, 2, 3]\n")
    errors = cd.check_journal_exists(root)
    assert any("journal.jsonl:1 is not a JSON object" in e for e in errors)


def test_check_journal_exists_rejects_missing_required_field(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    entry = json.loads(
        (root / "development" / "journal.jsonl").read_text().strip()
    )
    del entry["intent"]
    (root / "development" / "journal.jsonl").write_text(json.dumps(entry) + "\n")
    errors = cd.check_journal_exists(root)
    assert any("missing field 'intent'" in e for e in errors)


def test_check_journal_exists_rejects_bad_file_hash(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    entry = json.loads(
        (root / "development" / "journal.jsonl").read_text().strip()
    )
    entry["files"][0]["after"] = "not-a-hash"
    (root / "development" / "journal.jsonl").write_text(json.dumps(entry) + "\n")
    errors = cd.check_journal_exists(root)
    assert any("not a 40-hex git hash or null" in e for e in errors)


def test_check_journal_exists_null_hash_is_valid(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    entry = json.loads(
        (root / "development" / "journal.jsonl").read_text().strip()
    )
    entry["files"][0]["after"] = None
    (root / "development" / "journal.jsonl").write_text(json.dumps(entry) + "\n")
    assert cd.check_journal_exists(root) == []


def test_check_journal_exists_rejects_files_entry_missing_path(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    entry = json.loads(
        (root / "development" / "journal.jsonl").read_text().strip()
    )
    entry["files"] = [{"before": None, "after": "a" * 40}]
    (root / "development" / "journal.jsonl").write_text(json.dumps(entry) + "\n")
    errors = cd.check_journal_exists(root)
    assert any("missing 'path'" in e for e in errors)


def test_check_journal_exists_ignores_blank_lines(tmp_path: Path):
    root = make_valid_deployment(tmp_path)
    existing = (root / "development" / "journal.jsonl").read_text()
    (root / "development" / "journal.jsonl").write_text(existing + "\n\n   \n")
    assert cd.check_journal_exists(root) == []


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
    (root / "rules" / "templates" / "TEMPLATE-RULE-v1.md").unlink()
    monkeypatch.chdir(tmp_path)
    assert cd.main() == 1
