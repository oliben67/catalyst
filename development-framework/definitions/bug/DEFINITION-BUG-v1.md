# `bug` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `bug` |
| **Version** | 1 |

## Description

A `BUG-NNNNNN` document asserts that an existing, documented rule does not hold
in the running application — it targets one or more rule IDs the observed
behavior violates, never introduces new behavior (that's a requirement's job).
It always carries a Severity (Critical/High/Medium/Low) and a non-empty Targets
field. Lives under the project's `requirements/` sibling artifact-type
directory (its own root folder), registered in `bugs.md`.
