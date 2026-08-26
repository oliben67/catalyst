# `FEAT-NNNNNN` — short title

> Copy this file to `{{FEATURES_DIR}}/templates/TEMPLATE-FEATURE-v1.md` and resolve every `{{PLACEHOLDER}}` (INV-20). See [`INSTANTIATION-GUIDE.md`](../INSTANTIATION-GUIDE.md).

A feature entry documents a new or future piece of functionality for the
app — an idea, a roadmap item, a product direction. It is **not** a
rule-linked, measured artifact: it is never "done" against a rule, it
never requires a `Domain` or `Targets` field, and it is exempt from
`CODE-OF-CONDUCT.md` §1 ("no development without a targeted rule") and
the `Rules-of-Rules.md` §1 conflict check. Rules are what implementation
is measured against — see [`rule.template.md`](rule.template.md) — not
features. Per `Rules-of-Rules.md` §9, this scheme is separate from the
`BUG-`/`REQ-`/`HK-` development-artifact chain.

Once work on a feature actually starts, open a `REQ-NNNNNN` requirement
(see [`requirements.template.md`](requirements.template.md)) that
targets or proposes the rule(s) the feature requires. The requirement —
not this entry — is what gets vetted against existing rules, assigned a
domain, and measured for completion. Link the requirement back here once
it exists.

| Field | Value |
|---|---|
| **ID** | `FEAT-NNNNNN` |
| **Filename** | descriptive kebab-case filename, e.g. `FEAT-000004-bulk-export.md` — prefer specific product intent over generic labels like `feature.md` or `export.md` |
| **Status** | idea / proposed / planned / in-development / shipped / dropped |
| **Opened** | YYYY-MM-DD |
| **Area** | free-text product/functional area label |
| **Roadmap** | `RM-NNNNNN` this feature was triaged from, if any — empty if it didn't originate from an ingested `development/roadmaps/<name>.md` item |
| **Requirement(s)** | `REQ-NNNNNN` list, filled in once development starts — empty while still an idea |
| **Signed-off-by** | name of the registered user (`IAM/users/users.json`) who signed this entry — see `CODE-OF-CONDUCT.md` §2 |

## Description

What the feature does, from the user's/operator's point of view.

## Motivation

Why this is worth building — the problem or opportunity. A feature may
sit entirely outside current rule coverage; that's expected here, not a
gap to resolve in this document.

## Rough scope

What's likely in, what's likely out. Not a commitment — refined and made
concrete when a `REQ-NNNNNN` requirement is opened.

## Open questions

- ...

## Related

Other `FEAT-` IDs this relates to, supersedes, or is superseded by, and,
once opened, the `REQ-NNNNNN` requirement(s) that implement it.
