# `TEST-NNNNNN` — descriptive title

A development artifact like `BUG-`/`REQ-`/`HK-`: always carries its own
`Targets`/`Domain`, vetted the same way (`Rules-of-Rules.md` §1
conflict check, `rules-of-development.md` §1 — no development without a
targeted rule). `Requirements`/`Steps` are additional, independent,
optional `(0,n)` links to whichever `REQ-`/`STEP-` this test verifies —
see `Rules-of-Rules.md` §22.

| Field | Value |
|---|---|
| **ID** | `TEST-NNNNNN-<userid>` — the userid suffix is the resolved signer's (`Rules-of-Rules.md` §20) |
| **Name** | short descriptive summary of what this test verifies, e.g. `password-reset-token-expiry` — follows Rules of Rules naming conventions |
| **Filename** | descriptive kebab-case filename, e.g. `TEST-000003-Ab3xR9pQ-password-reset-token-expiry.md` — prefer specific problem/context over generic labels like `test.md` or `check.md` |
| **Status** | proposed / passing / failing / blocked |
| **Opened** | YYYY-MM-DD |
| **Targets** | one or more rule IDs this test verifies — **required, never empty** (see `rules-of-development.md` §1) |
| **Domain** | the `DOMAIN` code(s) of the targeted rule(s), from `rules/domains/` — **required, never free text** |
| **Requirements** | `REQ-NNNNNN` list this test verifies — optional, zero or more |
| **Steps** | `STEP-NNNNNN` list this test verifies — optional, zero or more |
| **Signed-off-by** | name of the registered user (`IAM/users/users.json`) who signed this test — see `CODE-OF-CONDUCT.md` §2 |

## Description

What this test verifies, and why it's worth tracking as its own
artifact rather than living only as an assertion inside a source file.

## Procedure

Concrete steps to execute this test — a command to run, a manual
sequence of actions, or a pointer to the automated test file/function
that implements it.

- ...
- ...

## Expected outcome

What must be true for this test to pass.

## Actual outcome

Blank until run. Filled in with the real result — `Status` should
already reflect this before this section does.

## Related

Other `TEST-`/`BUG-`/`REQ-`/`STEP-` IDs, or rule IDs.
