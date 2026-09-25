# `feature` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `feature` |
| **Version** | 1 |

## Description

A `FEAT-NNNNNN` entry documents a new or future piece of product functionality
— an idea, a roadmap item, a direction — before any work has actually started
on it. Unlike a requirement, a feature is never rule-linked or measured for
completion: no Domain, no Targets, exempt from the "no development without a
targeted rule" rule. Once work begins, a `REQ-NNNNNN` requirement is opened and
linked back to it. Lives in `features/`, registered in `features.md`.
