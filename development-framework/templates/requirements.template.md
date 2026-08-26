# `REQ-NNNNNN` — <project or requirement name>

> Copy this file to `{{REQUIREMENTS_DIR}}/templates/TEMPLATE-REQUIREMENT-v1.md` and resolve every `{{PLACEHOLDER}}` (INV-20). See [`INSTANTIATION-GUIDE.md`](../INSTANTIATION-GUIDE.md).

This document captures concrete, application-bound requirements derived
from the project's rule documents, especially UI and business rules. Use
it to translate documented expectations into testable behavior that is
directly tied to specific parts of the application. These requirements are
the main input for tests, acceptance criteria, and the bugs that will be
raised when behavior is incorrect.

This is also the artifact to open when a **new feature** needs to be
developed — never a `BUG-NNNNNN` for that (a bug asserts an existing rule
doesn't hold; a requirement introduces or extends behavior). A `FEAT-NNNNNN`
entry (see [`features.template.md`](features.template.md)) may have
motivated it, but a requirement stands on its own: it must be vetted
against every existing rule document before it's opened, it always
carries a `Domain`, and it always answers — targets or proposes — one or
more rules. None of those three are optional.

| Field | Value |
|---|---|
| **ID** | `REQ-NNNNNN` |
| **Filename** | descriptive kebab-case filename, e.g. `REQ-000002-password-reset-flow.md` — prefer specific problem/context over generic labels like `requirement.md` or `auth.md` |
| **Status** | proposed / approved / in-progress / done / rejected |
| **Opened** | YYYY-MM-DD |
| **Targets** | one or more rule IDs this requirement implements or extends — **required, never empty** (see `CODE-OF-CONDUCT.md` §1). If none exist yet, define them first (see New rules proposed below) |
| **Domain** | the `DOMAIN` code(s) of the targeted/new rule(s), from `{{RULES_DIR}}/domains/` — **required, never free text** |
| **Feature** | `FEAT-NNNNNN`, if this requirement was motivated by a documented feature — omit if none |
| **Signed-off-by** | name of the registered user (`IAM/users/users.json`) who signed this requirement — see `CODE-OF-CONDUCT.md` §2 |

## Vetted against existing rules

Per `Rules-of-Rules.md` §1: confirm this requirement was checked against
every rule document in `{{RULE_DOCS_LIST}}`, not only the one that seems
most relevant, and record the outcome — no conflict found, or the
specific existing rule ID(s) this requirement narrows/amends (and the
decision that authorized that).

## New domain proposed

*(omit if this requirement fits an existing domain.)* Per
`Rules-of-Rules.md` §7: domain-level conflict check performed; proposed
code; the domain file content (`rules/domains/<prefix>-<CODE>-<short-description>.md`)
this will create, including Scope and Relationship to other domains.

## New rules proposed

*(omit if none — only valid when the `Targets` field above already cites
existing rule IDs instead.)* List each new rule here **before**
implementation starts, in the exact form it will take once added to the
rule document: proposed ID, rule text, starting status marker (almost
always ❌). Run the `Rules-of-Rules.md` §1 conflict check first.

## Source rules

Capture the rule documents and rule IDs that informed this requirements
set. Examples include a UI-rules description such as `UI-Rules.md` and a
business-rules description such as `business-rules.md`. Each requirement
should point to the specific screen, flow, component, or domain behavior it
governs.

- **UI rules**: list relevant rule IDs or source files
- **Business rules**: list relevant rule IDs or source files
- **Application area**: name the specific screen, feature, form, or workflow

## Summary

Describe the user problem, requirement scope, or change being requested.

## Functional requirements

List the requirements in a structured way. Each item should reference one or
more source rules, name the relevant application area, and include
acceptance criteria that can be tested directly.

### Requirement 1 — <short title>

- **Source rule(s)**: `RULE-ID` or document name
- **Application area**: screen, form, component, workflow, or domain area
- **Description**: what must be true in that specific part of the app
- **Acceptance criteria**:
  - ...
  - ...

## UI requirements

Capture any requirements that affect the interface in a specific UI area.

- **Presentation Logic**: controls how a particular interface element looks
  or appears based on user actions or screen states.
- **Validation Rules**: checks whether specific typed data is correct
  before the user can continue in that flow.
- **Interaction/Behavior Rules**: defines dynamic screen changes for a
  specific screen or component based on user selections or state.
- **Initialization Rules**: sets default values for a specific form or
  screen state.

## Business rules

Capture the domain or workflow constraints that govern the feature.

- ...
- ...

## Non-functional requirements

- **Accessibility**: ...
- **Security**: ...
- **Performance**: ...
- **Observability**: ...

## Design / implementation plan

Brief — files touched, approach.

## Test plan

Per rule targeted or introduced, the specific test that will cover it. A
rule with no test is not "done" regardless of whether the code exists.

## Open questions

- ...

## Related

Other `BUG-`/`REQ-`/`HK-`/`FEAT-` IDs, or rule IDs.
