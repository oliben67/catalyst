# `test` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `test` |
| **Version** | 1 |

## Description

A `TEST-NNNNNN` verifies that a targeted rule actually holds — a
development artifact like `BUG-`/`REQ-`/`HK-`, always carrying its own
`Targets`/`Domain` and subject to the same "no development without a
targeted rule" gate. On top of that, a test may independently name
`(0,n)` requirements and `(0,n)` steps it verifies — both optional, and
neither implies the other: one requirement or step may be verified by
several tests, and one test may verify several requirements and/or
steps at once. Lives in `tests/`, created via `/create-test`.
