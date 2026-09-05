from pathlib import Path

import check_command_parity as ccp


def make_coc(tmp_path: Path, section4_body: str, *, before="", after="") -> Path:
    coc = tmp_path / "CODE-OF-CONDUCT.md"
    coc.write_text(
        f"{before}"
        "## 4. Slash-command entry points\n\n"
        f"{section4_body}"
        f"{after}"
    )
    return coc


def make_commands(tmp_path: Path, names: list[str]) -> Path:
    commands_dir = tmp_path / ".claude" / "commands"
    commands_dir.mkdir(parents=True)
    for name in names:
        (commands_dir / f"{name}.md").write_text(f"# /{name}\n")
    return commands_dir


def make_taskfile(tmp_path: Path, names: list[str], *, filename="Taskfile.common.yml") -> Path:
    taskfile = tmp_path / filename
    body = "\n".join(f'  {name}:\n    desc: "..."\n    cmds:\n      - "true"' for name in names)
    taskfile.write_text(f'version: "3"\n\ntasks:\n{body}\n')
    return taskfile


def test_extract_section4_commands_parses_simple_bullets():
    text = (
        "## 4. Slash-command entry points\n\n"
        "- `/create-bug` — create a new bug artifact.\n"
        "- `/list <type>` — list artifacts.\n"
    )
    assert ccp.extract_section4_commands(text) == {"create-bug", "list"}


def test_extract_section4_commands_handles_alias_bullet():
    text = (
        "## 4. Slash-command entry points\n\n"
        "- `/create-req` or `/create-requirement` — create a requirement.\n"
    )
    assert ccp.extract_section4_commands(text) == {"create-req", "create-requirement"}


def test_extract_section4_commands_collapses_repeated_subcommand_bullets():
    text = (
        "## 4. Slash-command entry points\n\n"
        "- `/criterion create <name> <git-info>` — bootstrap.\n"
        "- `/criterion get <repo> <username>` — join.\n"
        "- `/criterion push [--force]` — sync.\n"
    )
    assert ccp.extract_section4_commands(text) == {"criterion"}


def test_extract_section4_commands_ignores_indented_subcommand_bullets():
    text = (
        "## 4. Slash-command entry points\n\n"
        "- `/catalyzer <subcommand>` — manage plugins. Supported subcommands:\n"
        "  - `list` — list all available plugins by type.\n"
        "  - `activate <name> <version|latest>` — download and activate.\n"
    )
    assert ccp.extract_section4_commands(text) == {"catalyzer"}


def test_extract_section4_commands_ignores_bold_prose_naming_commands():
    text = (
        "## 4. Slash-command entry points\n\n"
        "- `/role-modify <role> <actions>` — replace a role's actions.\n"
        "**`/create-epic`, `/create-story`, `/create-task` are not core\n"
        "commands.** They are plugin-territory.\n"
        "- `/meta-tag` — create a new meta-tag artifact.\n"
    )
    assert ccp.extract_section4_commands(text) == {"role-modify", "meta-tag"}


def test_extract_section4_commands_stops_at_next_top_level_section():
    text = (
        "## 4. Slash-command entry points\n\n"
        "- `/create-bug` — create a new bug artifact.\n"
        "## 5. Something else\n\n"
        "- `/not-a-real-command` — should not be picked up.\n"
    )
    assert ccp.extract_section4_commands(text) == {"create-bug"}


def test_extract_section4_commands_returns_none_when_section_missing():
    text = "## 1. Something else\n\nNo section 4 here.\n"
    assert ccp.extract_section4_commands(text) is None


def test_find_command_files_excludes_dogfood(tmp_path: Path):
    commands_dir = make_commands(tmp_path, ["create-bug", "dogfood"])
    assert ccp.find_command_files(commands_dir) == {"create-bug"}


def test_find_command_files_missing_dir_returns_empty(tmp_path: Path):
    assert ccp.find_command_files(tmp_path / "nope") == set()


def test_check_command_parity_clean_baseline_has_no_errors(tmp_path: Path):
    coc = make_coc(
        tmp_path,
        "- `/create-bug` — create a bug.\n"
        "- `/list <type>` — list artifacts.\n",
    )
    commands_dir = make_commands(tmp_path, ["create-bug", "list", "dogfood"])
    assert ccp.check_command_parity(commands_dir, coc) == []


def test_check_command_parity_flags_documented_command_missing_file(tmp_path: Path):
    coc = make_coc(tmp_path, "- `/create-bug` — create a bug.\n")
    commands_dir = make_commands(tmp_path, [])
    errors = ccp.check_command_parity(commands_dir, coc)
    assert any("references /create-bug but" in e for e in errors)


def test_check_command_parity_flags_undocumented_command_file(tmp_path: Path):
    coc = make_coc(tmp_path, "- `/create-bug` — create a bug.\n")
    commands_dir = make_commands(tmp_path, ["create-bug", "mystery-command"])
    errors = ccp.check_command_parity(commands_dir, coc)
    assert any("mystery-command.md exists but is not referenced" in e for e in errors)


def test_check_command_parity_does_not_flag_dogfood_as_undocumented(tmp_path: Path):
    coc = make_coc(tmp_path, "- `/create-bug` — create a bug.\n")
    commands_dir = make_commands(tmp_path, ["create-bug", "dogfood"])
    assert ccp.check_command_parity(commands_dir, coc) == []


def test_check_command_parity_alias_bullet_requires_both_files(tmp_path: Path):
    coc = make_coc(
        tmp_path,
        "- `/create-req` or `/create-requirement` — create a requirement.\n",
    )
    commands_dir = make_commands(tmp_path, ["create-req"])
    errors = ccp.check_command_parity(commands_dir, coc)
    assert len(errors) == 1
    assert "create-requirement" in errors[0]


def test_check_command_parity_missing_code_of_conduct_file(tmp_path: Path):
    commands_dir = make_commands(tmp_path, ["create-bug"])
    errors = ccp.check_command_parity(commands_dir, tmp_path / "CODE-OF-CONDUCT.md")
    assert any("is missing" in e for e in errors)


def test_check_command_parity_missing_section4(tmp_path: Path):
    coc = tmp_path / "CODE-OF-CONDUCT.md"
    coc.write_text("## 1. Something else\n\nNo section 4 here.\n")
    commands_dir = make_commands(tmp_path, ["create-bug"])
    errors = ccp.check_command_parity(commands_dir, coc)
    assert any("has no '## 4.' section" in e for e in errors)


def test_extract_taskfile_commands_parses_top_level_tasks():
    text = (
        'version: "3"\n\n'
        "tasks:\n"
        "  create-bug:\n"
        '    desc: "..."\n'
        "    cmds:\n"
        '      - "true"\n'
        "  list:\n"
        '    desc: "..."\n'
    )
    assert ccp.extract_taskfile_commands(text) == {"create-bug", "list"}


def test_extract_taskfile_commands_stops_at_dedent():
    text = (
        "tasks:\n"
        "  create-bug:\n"
        '    desc: "..."\n'
        "vars:\n"
        "  should-not-count: true\n"
    )
    assert ccp.extract_taskfile_commands(text) == {"create-bug"}


def test_extract_taskfile_commands_returns_none_when_no_tasks_block():
    assert ccp.extract_taskfile_commands('version: "3"\n') is None


def test_check_taskfile_parity_clean_baseline_has_no_errors(tmp_path: Path):
    coc = make_coc(
        tmp_path,
        "- `/create-bug` — create a bug.\n"
        "- `/list <type>` — list artifacts.\n",
    )
    taskfile = make_taskfile(tmp_path, ["create-bug", "list"])
    assert ccp.check_taskfile_parity(taskfile, coc) == []


def test_check_taskfile_parity_flags_documented_command_missing_task(tmp_path: Path):
    coc = make_coc(tmp_path, "- `/create-bug` — create a bug.\n")
    taskfile = make_taskfile(tmp_path, [])
    errors = ccp.check_taskfile_parity(taskfile, coc)
    assert any("references /create-bug but" in e for e in errors)


def test_check_taskfile_parity_flags_undocumented_task(tmp_path: Path):
    coc = make_coc(tmp_path, "- `/create-bug` — create a bug.\n")
    taskfile = make_taskfile(tmp_path, ["create-bug", "mystery-task"])
    errors = ccp.check_taskfile_parity(taskfile, coc)
    assert any("'mystery-task' task but it is not referenced" in e for e in errors)


def test_check_taskfile_parity_missing_taskfile(tmp_path: Path):
    coc = make_coc(tmp_path, "- `/create-bug` — create a bug.\n")
    errors = ccp.check_taskfile_parity(tmp_path / "Taskfile.common.yml", coc)
    assert any("is missing" in e for e in errors)


def test_main_returns_zero_when_no_deployment(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert ccp.main() == 0


def test_main_returns_zero_for_valid_parity(tmp_path: Path, monkeypatch):
    deploy_root = tmp_path / ".criterion"
    deploy_root.mkdir()
    make_coc(deploy_root, "- `/create-bug` — create a bug.\n")
    commands_dir = make_commands(tmp_path, ["create-bug", "dogfood"])
    taskfile = make_taskfile(tmp_path, ["create-bug"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(ccp, "COMMANDS_DIR", commands_dir)
    monkeypatch.setattr(ccp, "TASKFILE_PATH", taskfile)
    assert ccp.main() == 0


def test_main_returns_one_for_mismatched_parity(tmp_path: Path, monkeypatch):
    deploy_root = tmp_path / ".criterion"
    deploy_root.mkdir()
    make_coc(deploy_root, "- `/create-bug` — create a bug.\n")
    commands_dir = make_commands(tmp_path, ["dogfood"])
    taskfile = make_taskfile(tmp_path, ["create-bug"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(ccp, "COMMANDS_DIR", commands_dir)
    monkeypatch.setattr(ccp, "TASKFILE_PATH", taskfile)
    assert ccp.main() == 1


def test_main_returns_one_for_missing_taskfile(tmp_path: Path, monkeypatch):
    deploy_root = tmp_path / ".criterion"
    deploy_root.mkdir()
    make_coc(deploy_root, "- `/create-bug` — create a bug.\n")
    commands_dir = make_commands(tmp_path, ["create-bug", "dogfood"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(ccp, "COMMANDS_DIR", commands_dir)
    monkeypatch.setattr(ccp, "TASKFILE_PATH", tmp_path / "Taskfile.common.yml")
    assert ccp.main() == 1
