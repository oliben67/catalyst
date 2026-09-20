# `STEP-NNNNNN` — short title

> One concrete unit of implementation work performed toward a specific
> requirement — never a rule-linked claim of its own (`Rules-of-Rules.md`
> §21). Opened as work on a requirement actually starts, not in advance
> of it; a requirement accumulates zero (not yet started) to many steps
> over its lifecycle.

| Field | Value |
|---|---|
| **ID** | `STEP-NNNNNN-<userid>` — the userid suffix is the resolved signer's (`Rules-of-Rules.md` §20) |
| **Name** | short descriptive summary of what this step does, e.g. `parse-corpus-fixtures` — follows Rules of Rules naming conventions |
| **Filename** | descriptive kebab-case filename, e.g. `STEP-000001-Ab3xR9pQ-parse-corpus-fixtures.md` — prefer specific work over generic labels like `step.md` or `work.md` |
| **Requirement** | `REQ-NNNNNN` this step implements — **required, never empty** |
| **Status** | planned / in-progress / done / abandoned |
| **Opened** | YYYY-MM-DD |
| **Closed** | YYYY-MM-DD — blank until `done` or `abandoned` |
| **Tests** | `TEST-NNNNNN` list of tests that verify this step — empty until `/create-test` names it; back-populated automatically, never hand-edited (`Rules-of-Rules.md` §22) |
| **Signed-off-by** | name of the registered user (`IAM/users/users.json`) who signed this step — see `CODE-OF-CONDUCT.md` §2 |

## Description

What this concrete unit of work does, and why it's its own step rather
than folded into another one — usually because it's independently
verifiable, or a natural checkpoint in the requirement's implementation.

## Actions performed

The literal record: files changed, commands run, decisions made, in the
order they happened. Concrete enough that someone reconstructing this
work from scratch could follow it — not a restatement of the
Description above.

- ...
- ...

## Verification

How this step's result was actually confirmed — a test run, a manual
check, a script's output against a known-good fixture. `abandoned`
steps explain why here instead.

## Related

Other `STEP-`/`REQ-`/`TEST-` IDs this depends on, blocks, or was split from.
