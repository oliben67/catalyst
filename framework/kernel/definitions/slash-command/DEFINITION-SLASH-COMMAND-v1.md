# `slash-command` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `slash-command` |
| **Version** | 1 |

## Description

A slash-command file (`.claude/commands/<name>.md`) is the literal prompt an
agent runs when a user types `/<name>` — kept as a thin, procedural pointer
back to `CODE-OF-CONDUCT.md` §4's canonical behavior spec, rather than
duplicating that spec's prose, so the command stays correct across a `/sync-
framework` without needing its own edit.
