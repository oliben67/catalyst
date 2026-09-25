# `step` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `step` |
| **Version** | 1 |

## Description

A `STEP-NNNNNN` records one concrete unit of implementation work performed
toward a specific `REQ-NNNNNN` — the files touched, commands run, and how
it was verified. Never a rule-linked claim of its own: it inherits its
parent requirement's already-vetted rule target and exists purely to give
that requirement's real implementation history a structured, itemized
record instead of only prose. A requirement accumulates zero to many
steps over its lifecycle and isn't closeable as `done` until every listed
step is `done` or `abandoned`. Lives in `steps/`, created via
`/create-step`.
