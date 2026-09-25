# `ledger` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `ledger` |
| **Version** | 1 |

## Description

A deployment ledger (`.criterion/.ledger/<task>.todo.md`) is a state file for
one in-progress install/analysis run — a checklist of atomic, verifiable items
the agent reads before and writes after each unit of work, so progress survives
a context loss and any drift is visible against a written record. It is agent-
working-state, not a product artifact.
