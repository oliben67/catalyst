# Requirements — <project or requirement name>

This document captures concrete, application-bound requirements derived
from the project's rule documents, especially UI and business rules. Use
it to translate documented expectations into testable behavior that is
directly tied to specific parts of the application. These requirements are
the main input for tests, acceptance criteria, and the bugs that will be
raised when behavior is incorrect.

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

## Open questions

- ...
