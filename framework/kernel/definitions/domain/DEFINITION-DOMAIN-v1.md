# `domain` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `domain` |
| **Version** | 1 |

## Description

A domain groups related rules under one short code (e.g. `AUTH`, `INSPECTOR`)
so rules sharing a concern can be found, indexed, and reasoned about together.
Domains nest under `rules/domains/` — never a top-level sibling of `rules/` —
and may declare a parent/sub-domain relationship, but rules in one domain never
supersede or contradict rules in another unless explicitly stated against that
rule's own ID.
