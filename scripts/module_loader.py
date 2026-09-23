#!/usr/bin/env python3
"""Module Loader & Registry Engine for Catalyst (Python).

Phase 2 implementation of the Catalyst Module Architecture.
Loads process modules (e.g. software-engineering), ETDs (Entity Type Definitions),
command registrations, and grounding rules.

Exposes query functions:
- load_module(project_root, module_id) -> ModuleManifest
- get_active_etds(manifest) -> dict[str, ETD]
- get_grounding_type(manifest) -> str
- resolve_command(manifest, name) -> CommandRegistration | None
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FieldDefinition:
    name: str
    kind: str  # text, enum, ref, ref-list, date, user, user-list
    required: bool = False
    allowed_values: list[str] = field(default_factory=list)
    target_type: str | None = None
    backref: str | None = None


@dataclass
class WorkflowTransition:
    from_state: str
    to_state: str


@dataclass
class WorkflowDefinition:
    initial: str
    states: list[str] = field(default_factory=list)
    closed_states: list[str] = field(default_factory=list)
    transitions: list[WorkflowTransition] = field(default_factory=list)


@dataclass
class ETD:
    id_prefix: str
    name: str
    plural_name: str
    folder: str
    grounding: str  # "required" | "inherited" | "none"
    grounding_field: str | None = None
    fields: list[FieldDefinition] = field(default_factory=list)
    workflow: WorkflowDefinition = field(
        default_factory=lambda: WorkflowDefinition(initial="Open", states=["Open"], closed_states=[])
    )


@dataclass
class CommandRegistration:
    name: str
    description: str
    argument_hint: str | None = None
    spec_path: str | None = None


@dataclass
class SkillRegistration:
    name: str
    spec_path: str


@dataclass
class TemplateRegistration:
    entity_type: str
    template_path: str


@dataclass
class ModuleManifest:
    id: str
    name: str
    version: str
    description: str
    grounding_type: str  # e.g., "rule"
    entity_types: dict[str, ETD] = field(default_factory=dict)
    commands: dict[str, CommandRegistration] = field(default_factory=dict)
    skills: list[SkillRegistration] = field(default_factory=list)
    templates: list[TemplateRegistration] = field(default_factory=list)


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Lightweight YAML parser for simple nested dicts/lists without external dependencies.
    Supports basic key: value, lists (- item), and simple nested maps. Also handles JSON fallback."""
    text = text.strip()
    if not text:
        return {}
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    try:
        import yaml
        res = yaml.safe_load(text)
        if isinstance(res, dict):
            return res
    except Exception:
        pass

    lines = text.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for line in lines:
        raw_line = line
        # Strip comments
        if "#" in line:
            parts = line.split("#", 1)
            if not (parts[0].count('"') % 2 == 1 or parts[0].count("'") % 2 == 1):
                line = parts[0]
        line_stripped = line.strip()
        if not line_stripped:
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))

        while stack and stack[-1][0] >= indent:
            stack.pop()

        parent = stack[-1][1] if stack else root

        if line_stripped.startswith("- "):
            val = line_stripped[2:].strip()
            # If parent is an empty dict that was created for a key with empty value,
            # convert stack parent or replace in grandparent to list
            if isinstance(parent, dict):
                # find grandparent key that points to this empty dict parent
                if len(stack) >= 2:
                    grandparent = stack[-2][1]
                    if isinstance(grandparent, dict):
                        for gk, gv in list(grandparent.items()):
                            if gv is parent:
                                new_list: list[Any] = []
                                grandparent[gk] = new_list
                                stack[-1] = (stack[-1][0], new_list)
                                parent = new_list
                                break

            if isinstance(parent, list):
                if ":" in val and not (val.startswith('"') or val.startswith("'")):
                    k, v = val.split(":", 1)
                    item_dict = {k.strip(): _parse_scalar(v.strip())}
                    parent.append(item_dict)
                    stack.append((indent, item_dict))
                else:
                    parent.append(_parse_scalar(val))
        elif ":" in line_stripped:
            k, v = line_stripped.split(":", 1)
            k = k.strip()
            v = v.strip()
            if not v:
                nested_container: dict[str, Any] | list[Any] = {}
                if isinstance(parent, dict):
                    parent[k] = nested_container
                elif isinstance(parent, list) and parent and isinstance(parent[-1], dict):
                    parent[-1][k] = nested_container
                stack.append((indent, nested_container))
            else:
                parsed_val = _parse_scalar(v)
                if isinstance(parent, dict):
                    parent[k] = parsed_val
                elif isinstance(parent, list) and parent and isinstance(parent[-1], dict):
                    parent[-1][k] = parsed_val

    return root


def _parse_scalar(val: str) -> Any:
    if val in ("true", "True", "TRUE"):
        return True
    if val in ("false", "False", "FALSE"):
        return False
    if val in ("null", "None", "~", ""):
        return None
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    if val.isdigit():
        return int(val)
    return val


def get_default_software_engineering_manifest() -> ModuleManifest:
    """Built-in default fallback for software-engineering process module."""
    etds: dict[str, ETD] = {
        "BUG": ETD(
            id_prefix="BUG",
            name="Bug",
            plural_name="Bugs",
            folder="bugs",
            grounding="required",
            grounding_field="Targets",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Open", "Under Review", "Fixed", "Closed", "WontFix"]),
                FieldDefinition("Targets", "ref-list", required=True, target_type="rule"),
                FieldDefinition("Domain", "ref", required=True, target_type="domain"),
                FieldDefinition("Steps", "ref-list", required=False, target_type="STEP"),
            ],
            workflow=WorkflowDefinition(
                initial="Open",
                states=["Open", "Under Review", "Fixed", "Closed", "WontFix"],
                closed_states=["Closed", "WontFix"],
            ),
        ),
        "REQ": ETD(
            id_prefix="REQ",
            name="Requirement",
            plural_name="Requirements",
            folder="requirements",
            grounding="required",
            grounding_field="Targets",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Draft", "Proposed", "Vetted", "Active", "Completed", "Abandoned"]),
                FieldDefinition("Targets", "ref-list", required=True, target_type="rule"),
                FieldDefinition("Domain", "ref", required=True, target_type="domain"),
                FieldDefinition("Feature", "ref", required=False, target_type="FEAT", backref="Requirements"),
                FieldDefinition("Tests", "ref-list", required=False, target_type="TEST", backref="Requirements"),
                FieldDefinition("Steps", "ref-list", required=False, target_type="STEP"),
            ],
            workflow=WorkflowDefinition(
                initial="Draft",
                states=["Draft", "Proposed", "Vetted", "Active", "Completed", "Abandoned"],
                closed_states=["Completed", "Abandoned"],
            ),
        ),
        "HK": ETD(
            id_prefix="HK",
            name="House-keeping",
            plural_name="House-keeping Items",
            folder="house-keeping",
            grounding="required",
            grounding_field="Targets",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Open", "Completed"]),
                FieldDefinition("Targets", "ref-list", required=True, target_type="rule"),
                FieldDefinition("Domain", "ref", required=True, target_type="domain"),
            ],
            workflow=WorkflowDefinition(
                initial="Open",
                states=["Open", "Completed"],
                closed_states=["Completed"],
            ),
        ),
        "TEST": ETD(
            id_prefix="TEST",
            name="Test",
            plural_name="Tests",
            folder="tests",
            grounding="required",
            grounding_field="Targets",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Draft", "Active", "Passing", "Failing", "Disabled"]),
                FieldDefinition("Targets", "ref-list", required=True, target_type="rule"),
                FieldDefinition("Domain", "ref", required=True, target_type="domain"),
                FieldDefinition("Requirements", "ref-list", required=False, target_type="REQ", backref="Tests"),
                FieldDefinition("Steps", "ref-list", required=False, target_type="STEP"),
            ],
            workflow=WorkflowDefinition(
                initial="Draft",
                states=["Draft", "Active", "Passing", "Failing", "Disabled"],
                closed_states=["Passing"],
            ),
        ),
        "STEP": ETD(
            id_prefix="STEP",
            name="Step",
            plural_name="Steps",
            folder="steps",
            grounding="inherited",
            grounding_field="Parent",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["planned", "in-progress", "done", "abandoned"]),
                FieldDefinition("Parent", "ref", required=True, target_type="REQ"),
            ],
            workflow=WorkflowDefinition(
                initial="planned",
                states=["planned", "in-progress", "done", "abandoned"],
                closed_states=["done", "abandoned"],
            ),
        ),
        "FEAT": ETD(
            id_prefix="FEAT",
            name="Feature",
            plural_name="Features",
            folder="features",
            grounding="none",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Draft", "Triaged", "Active", "Completed", "Abandoned"]),
            ],
            workflow=WorkflowDefinition(
                initial="Draft",
                states=["Draft", "Triaged", "Active", "Completed", "Abandoned"],
                closed_states=["Completed", "Abandoned"],
            ),
        ),
        "RM": ETD(
            id_prefix="RM",
            name="Roadmap",
            plural_name="Roadmaps",
            folder="roadmaps",
            grounding="none",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Not triaged", "Triaged", "In progress", "Done"]),
                FieldDefinition("Linked", "ref", required=False, target_type="FEAT"),
            ],
            workflow=WorkflowDefinition(
                initial="Not triaged",
                states=["Not triaged", "Triaged", "In progress", "Done"],
                closed_states=["Done"],
            ),
        ),
        "WORKFLOW": ETD(
            id_prefix="WORKFLOW",
            name="Workflow",
            plural_name="Workflows",
            folder="workflows",
            grounding="none",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Draft", "Active", "Deprecated"]),
            ],
            workflow=WorkflowDefinition(
                initial="Draft",
                states=["Draft", "Active", "Deprecated"],
                closed_states=["Deprecated"],
            ),
        ),
        "RECON": ETD(
            id_prefix="RECON",
            name="Reconciliation",
            plural_name="Reconciliations",
            folder="reconciliations",
            grounding="none",
            fields=[
                FieldDefinition("ID", "text", required=True),
                FieldDefinition("Status", "enum", required=True, allowed_values=["Open", "Under Review", "Resolved-Accepted", "Resolved-Rejected", "Closed"]),
                FieldDefinition("Entity", "ref", required=True),
                FieldDefinition("Workflow", "ref", required=False, target_type="WORKFLOW"),
            ],
            workflow=WorkflowDefinition(
                initial="Open",
                states=["Open", "Under Review", "Resolved-Accepted", "Resolved-Rejected", "Closed"],
                closed_states=["Resolved-Accepted", "Resolved-Rejected", "Closed"],
            ),
        ),
    }

    commands: dict[str, CommandRegistration] = {
        "create-req": CommandRegistration("create-req", "Create a new requirement artifact", argument_hint="[<rule-id>]"),
        "create-bug": CommandRegistration("create-bug", "Create a new bug artifact", argument_hint="[<rule-id>]"),
        "create-test": CommandRegistration("create-test", "Create a new test artifact", argument_hint="[<rule-id>]"),
        "create-feature": CommandRegistration("create-feature", "Create a new feature artifact"),
        "create-step": CommandRegistration("create-step", "Create a new step artifact", argument_hint="<parent-id>"),
        "check-rules": CommandRegistration("check-rules", "Validate rule link coverage across dev artifacts"),
        "show-backlog": CommandRegistration("show-backlog", "Display work item and artifact backlog"),
        "cut-release": CommandRegistration("cut-release", "Cut a release for catalyst or a submodule"),
    }

    return ModuleManifest(
        id="software-engineering",
        name="Software Engineering Process Module",
        version="1.0.0",
        description="Standard software engineering process module governing rules, requirements, bugs, tests, steps, features, and reconciliations.",
        grounding_type="rule",
        entity_types=etds,
        commands=commands,
    )


def resolve_module_id(project_root: Path | str | None) -> str:
    """Resolve active module ID from project pointer (*.catalyst or .criterion/config.yaml). Defaults to 'software-engineering'."""
    if not project_root:
        return "software-engineering"
    root = Path(project_root).resolve()

    # Search for *.catalyst pointer
    pointers = list(root.glob("*.catalyst"))
    if pointers:
        try:
            data = json.loads(pointers[0].read_text())
            if isinstance(data, dict) and data.get("module"):
                return str(data["module"])
        except Exception:
            pass

    # Search for .criterion/config.yaml or .criterion/module.yaml
    cfg_yaml = root / ".criterion" / "config.yaml"
    if cfg_yaml.is_file():
        parsed = parse_simple_yaml(cfg_yaml.read_text())
        if isinstance(parsed, dict) and parsed.get("module"):
            return str(parsed["module"])

    mod_yaml = root / ".criterion" / "module.yaml"
    if mod_yaml.is_file():
        parsed = parse_simple_yaml(mod_yaml.read_text())
        if isinstance(parsed, dict) and parsed.get("id"):
            return str(parsed["id"])

    return "software-engineering"


def parse_etd_dict(d: dict[str, Any]) -> ETD:
    id_prefix = d.get("id_prefix", "")
    name = d.get("name", id_prefix)
    plural_name = d.get("plural_name", f"{name}s")
    folder = d.get("folder", id_prefix.lower())
    grounding = d.get("grounding", "none")
    grounding_field = d.get("grounding_field")

    fields: list[FieldDefinition] = []
    for f in d.get("fields", []):
        if isinstance(f, dict):
            fields.append(
                FieldDefinition(
                    name=f.get("name", ""),
                    kind=f.get("kind", "text"),
                    required=bool(f.get("required", False)),
                    allowed_values=f.get("allowed_values", []) or [],
                    target_type=f.get("target_type"),
                    backref=f.get("backref"),
                )
            )

    wf_raw = d.get("workflow", {})
    if isinstance(wf_raw, dict):
        wf = WorkflowDefinition(
            initial=wf_raw.get("initial", "Open"),
            states=wf_raw.get("states", []),
            closed_states=wf_raw.get("closed_states", []),
        )
    else:
        wf = WorkflowDefinition(initial="Open", states=["Open"], closed_states=[])

    return ETD(
        id_prefix=id_prefix,
        name=name,
        plural_name=plural_name,
        folder=folder,
        grounding=grounding,
        grounding_field=grounding_field,
        fields=fields,
        workflow=wf,
    )


def load_module(project_root: Path | str | None = None, module_id: str | None = None) -> ModuleManifest:
    """Load module manifest by ID or project root. Falls back to software-engineering default."""
    target_id = module_id or resolve_module_id(project_root)

    # Search paths for module directory
    search_dirs: list[Path] = []
    if project_root:
        pr = Path(project_root).resolve()
        search_dirs.extend([
            pr / ".criterion" / "modules" / target_id,
            pr / "modules" / target_id,
            pr / "development-framework" / "modules" / target_id,
        ])

    # Also search relative to this file's repository
    repo_root = Path(__file__).resolve().parent.parent
    search_dirs.extend([
        repo_root / "development-framework" / "modules" / target_id,
        repo_root / "modules" / target_id,
    ])

    for mdir in search_dirs:
        mfile = mdir / "module.yaml"
        if mfile.is_file():
            data = parse_simple_yaml(mfile.read_text())
            if isinstance(data, dict):
                mid = data.get("id", target_id)
                mname = data.get("name", mid)
                mver = str(data.get("version", "1.0.0"))
                mdesc = data.get("description", "")
                mgnd = data.get("grounding_type", "rule")

                etds: dict[str, ETD] = {}
                etd_list = data.get("entity_types", [])
                if isinstance(etd_list, list):
                    for item in etd_list:
                        if isinstance(item, dict):
                            eid = item.get("id")
                            rel_schema = item.get("schema")
                            if eid and rel_schema:
                                schema_path = mdir / rel_schema
                                if schema_path.is_file():
                                    etd_dict = parse_simple_yaml(schema_path.read_text())
                                    if isinstance(etd_dict, dict):
                                        etds[eid] = parse_etd_dict(etd_dict)

                cmds: dict[str, CommandRegistration] = {}
                cmd_list = data.get("commands", [])
                if isinstance(cmd_list, list):
                    for c in cmd_list:
                        if isinstance(c, dict) and c.get("name"):
                            cname = c["name"]
                            cmds[cname] = CommandRegistration(
                                name=cname,
                                description=c.get("description", ""),
                                argument_hint=c.get("argument_hint"),
                                spec_path=c.get("spec_path"),
                            )

                return ModuleManifest(
                    id=mid,
                    name=mname,
                    version=mver,
                    description=mdesc,
                    grounding_type=mgnd,
                    entity_types=etds or get_default_software_engineering_manifest().entity_types,
                    commands=cmds or get_default_software_engineering_manifest().commands,
                )

    # Fall back to default software-engineering manifest if not loaded from file
    return get_default_software_engineering_manifest()


def get_active_etds(manifest: ModuleManifest) -> dict[str, ETD]:
    """Return dictionary of active ETDs keyed by ID prefix."""
    return manifest.entity_types


def get_grounding_type(manifest: ModuleManifest) -> str:
    """Return primary grounding artifact type for the module (e.g. 'rule')."""
    return manifest.grounding_type


def resolve_command(manifest: ModuleManifest, name: str) -> CommandRegistration | None:
    """Resolve command registration by name."""
    clean_name = name.lstrip("/")
    return manifest.commands.get(clean_name)
