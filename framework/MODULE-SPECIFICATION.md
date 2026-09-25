# Catalyst Module & ETD Specification

**Version:** 1.0.0  
**Status:** Phase 1 Standard  
**Scope:** Core Catalyst Framework (`framework/`)

---

## 1. Overview

This document specifies the architecture, manifest schema, Entity Type Definition (ETD) schema, and directory layout for **Catalyst Modules**.

A Catalyst Module encapsulates a complete process domain (such as `software-engineering`, `scrum`, `itil`, `legal-compliance`, or `product-management`). Decoupling domain concepts from the Catalyst kernel allows the core engine to remain process-agnostic while enabling deployments to load, swap, or extend process models with 100% behavioral parity.

---

## 2. Module Directory Layout Specification

A Catalyst module resides under the `modules/` directory in the framework repository or `.criterion/modules/` in a project deployment:

```
modules/
└── <module-id>/
    ├── module.yaml             # Primary module manifest
    ├── schemas/                # Entity Type Definitions (ETDs)
    │   ├── <entity-1>.yaml
    │   ├── <entity-2>.yaml
    │   └── ...
    ├── templates/              # Document templates for human-facing markdown
    │   ├── template-<entity-1>.md
    │   └── ...
    ├── commands/               # Slash command prompt specs (.md)
    │   ├── create-<entity-1>.md
    │   └── ...
    └── skills/                 # Agent skill specifications
        └── <skill-name>/
            └── SKILL.md
```

---

## 3. Module Manifest Schema (`module.yaml`)

The `module.yaml` file defines the identity, grounding rules, entity schemas, command registrations, skills, and templates exported by a module.

### 3.1 Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | Yes | Unique module identifier (e.g. `software-engineering`). Lowercase, hyphen-separated. |
| `name` | `string` | Yes | Human-readable name of the process module. |
| `version` | `string` | Yes | SemVer format version string (e.g. `1.0.0`). |
| `description` | `string` | Yes | Concise description of the module's domain and purpose. |
| `grounding_type` | `string` | Yes | The primary grounding artifact type for the module (e.g. `rule` for software engineering, `policy` for governance). |
| `entity_types` | `list[object]` | Yes | List of ETD schema files included in this module. |
| `commands` | `list[object]` | No | List of slash commands provided by this module. |
| `skills` | `list[object]` | No | List of agent skills exported by this module. |
| `templates` | `list[object]` | No | List of document templates for generating human-facing artifacts. |

### 3.2 Manifest Example

```yaml
id: software-engineering
name: Software Engineering Process Module
version: 1.0.0
description: Standard software engineering process module governing rules, requirements, bugs, tests, steps, features, and reconciliations.
grounding_type: rule

entity_types:
  - id: BUG
    schema: schemas/bug.yaml
  - id: REQ
    schema: schemas/requirement.yaml
  - id: TEST
    schema: schemas/test.yaml
  - id: STEP
    schema: schemas/step.yaml
  - id: FEAT
    schema: schemas/feature.yaml
  - id: HK
    schema: schemas/house-keeping.yaml
  - id: RM
    schema: schemas/roadmap.yaml
  - id: WORKFLOW
    schema: schemas/workflow.yaml
  - id: RECON
    schema: schemas/reconciliation.yaml

commands:
  - name: create-req
    description: Create a new rule-linked requirement artifact
    argument_hint: "[<rule-id>]"
    spec_path: commands/create-req.md
  - name: create-bug
    description: Create a new rule-linked bug artifact
    argument_hint: "[<rule-id>]"
    spec_path: commands/create-bug.md
  - name: check-rules
    description: Validate chain completeness across all dev artifacts
    spec_path: commands/check-rules.md

skills:
  - name: python-fact-grounded-coding
    spec_path: skills/python-fact-grounded-coding/SKILL.md

templates:
  - entity_type: REQ
    template_path: templates/template-requirement.md
  - entity_type: BUG
    template_path: templates/template-bug.md
```

---

## 4. Entity Type Definition (ETD) Schema (`<type>.yaml`)

An ETD schema specifies an individual artifact type's ID prefix, storage directory, grounding behavior, fields, relationship links, backreferences, and state workflow.

### 4.1 Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `id_prefix` | `string` | Yes | Uppercase prefix for entity IDs (e.g. `BUG`, `REQ`, `TEST`). |
| `name` | `string` | Yes | Singular human-readable name (e.g. `Requirement`). |
| `plural_name` | `string` | Yes | Plural human-readable name (e.g. `Requirements`). |
| `folder` | `string` | Yes | Directory name relative to working copy root (e.g. `requirements`, `bugs`). |
| `grounding` | `string` | Yes | Grounding rule requirement: `required` (must link directly to grounding type), `inherited` (inherits from parent entity), or `none` (roadmap/standalone). |
| `grounding_field` | `string` | Conditional | Name of the field containing the grounding link (e.g. `Targets` or `Parent`). Required when `grounding` is `required` or `inherited`. |
| `fields` | `list[object]` | Yes | Ordered list of field definitions. |
| `workflow` | `object` | Yes | Lifecycle states and transition rules. |

### 4.2 Field Definition Structure (`fields[]`)

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | Yes | Exact header/key name in the artifact file (e.g. `Status`, `Targets`, `Requirements`). |
| `kind` | `string` | Yes | Data type: `text`, `enum`, `ref`, `ref-list`, `date`, `user`, `user-list`. |
| `required` | `boolean` | Yes | Whether the field must be present in every artifact instance. |
| `allowed_values` | `list[string]` | Conditional | Allowed enum values when `kind` is `enum`. |
| `target_type` | `string` | Conditional | Target entity prefix when `kind` is `ref` or `ref-list` (e.g. `REQ` or `rule`). |
| `backref` | `string` | Optional | Corresponding back-reference field name on target entity (e.g. `TEST.Requirements` back-populates `REQ.Tests`). |

### 4.3 Workflow Structure (`workflow`)

| Field | Type | Required | Description |
|---|---|---|---|
| `initial` | `string` | Yes | Initial status assigned upon entity creation (e.g. `Draft` or `Open`). |
| `states` | `list[string]` | Yes | Complete set of valid status values. |
| `closed_states` | `list[string]` | Yes | Status values that signify the entity is done or resolved (e.g. `Closed`, `Resolved-Accepted`). |
| `transitions` | `list[object]` | No | Optional transition constraints defining allowed `from` $\rightarrow$ `to` state moves. |

### 4.4 ETD Schema Example (`schemas/requirement.yaml`)

```yaml
id_prefix: REQ
name: Requirement
plural_name: Requirements
folder: requirements
grounding: required
grounding_field: Targets

fields:
  - name: ID
    kind: text
    required: true
  - name: Status
    kind: enum
    required: true
    allowed_values:
      - Draft
      - Proposed
      - Vetted
      - Active
      - Completed
      - Abandoned
  - name: Targets
    kind: ref-list
    required: true
    target_type: rule
  - name: Domain
    kind: ref
    required: true
    target_type: domain
  - name: Feature
    kind: ref
    required: false
    target_type: FEAT
    backref: Requirements
  - name: Tests
    kind: ref-list
    required: false
    target_type: TEST
    backref: Requirements
  - name: Steps
    kind: ref-list
    required: false
    target_type: STEP

workflow:
  initial: Draft
  states:
    - Draft
    - Proposed
    - Vetted
    - Active
    - Completed
    - Abandoned
  closed_states:
    - Completed
    - Abandoned
  transitions:
    - from: Draft
      to: Proposed
    - from: Proposed
      to: Vetted
    - from: Vetted
      to: Active
    - from: Active
      to: Completed
    - from: Active
      to: Abandoned
```

---

## 5. Grounding Model & Invariant Generalization

Under the Catalyst Module architecture:
1. **Generalized Grounding (INV-5):** The chain invariant is generalized from requiring a hardcoded `rule` link to requiring a link to the active module's `grounding_type` (or inheriting it via `grounding: inherited`). For the `software-engineering` module, `grounding_type` defaults to `rule`.
2. **Backward Compatibility:** If no module is explicitly declared in a project pointer, the engine defaults to `software-engineering` with `rule` grounding, preserving complete compatibility for existing deployments.
