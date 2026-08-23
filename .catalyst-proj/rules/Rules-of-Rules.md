Meta-rules governing how any rule gets added to, changed in, or retired
from one of this project's rule documents: `rules/framework/fw-framework-rules.md`
(the only rule document — catalyst's own repo has one natural seam: the
framework itself). These apply to the *process* of maintaining that
document and the code it describes, not to the app's behavior itself.
Binding on anyone (human or agent) adding to it, at any point after this
file exists.

Each rule must belong to a rule type directory under `rules/`, be stored
as its own markdown file in that directory, be listed in the corresponding
type index, and be referenced from the global index `rules/rules.md`.
There must be exactly one template file at `rules/TEMPLATE-RULE.md` and no
`TEMPLATE-RULE.md` files inside the rule-type directories. No rule may be
orphaned by missing a type, a local index entry, or a global index entry.

---

## 1. `rr-META-001` Check for conflicts before adding a new rule

Before a new rule is implemented, check it against the rules already
recorded in the rule document — not just the section that seems most
relevant, since the same underlying behavior is sometimes governed from
more than one angle, and a change to one side can silently break the
other. Check, in order:

1. The same functionality area in the domain(s) affected.
2. The document's Cross-Cutting Notes heading (or equivalent).
3. The document's Known Bugs / Quick Index heading — a "new" rule is
   sometimes actually a conflicting rewrite of an existing one.

If the new rule **contradicts, narrows, silently overrides, or would
break** an existing ✅ rule, **stop and prompt for a decision** — do not
silently override it, and do not silently implement both side by side and
let whichever runs last win.

## 2. `rr-META-002` A new rule is never done until it's gathered, implemented, tested, and documented

All four, no exceptions:

- **Gathered** — the rule's actual current/intended behavior is
  understood and written down before code changes.
- **Implemented** — the rule actually exists in the code, not just in a
  comment, commit message, or this documentation.
- **Tested** — it has **at least one test** exercising it. Test
  locations: `tests/` (the pytest suite covering `scripts/check_deployment.py`,
  `scripts/check_plugins.py`, `scripts/check_plugin_contracts.py`). A rule
  with zero test coverage is not "done" — it's "implemented but
  untested," and marked as such (see status markers below). Several of
  this project's own invariants are **behavioral** — enforced by agent
  discipline (this file, `INVARIANTS.md`, `BOOTSTRAP.md`), not by a test —
  and are marked ⚠️ rather than ✅ for that reason; that's an honest
  status, not a gap to silently paper over.
- **Documented** — added to the rule document, under the functionality
  domain it belongs to and the right rule category, with a `file:line`
  citation and a status marker, in the same format every existing entry
  already uses.

**Status markers**: ✅ working · ⚠️ buggy/incomplete · ❌ not implemented
/ regressed · 🗑 retired (see §4).

## Which document does a rule belong in?

There is currently only one rule document, `fw-framework-rules.md` — this
section is a placeholder for if the repo ever grows a second natural seam
(e.g. a separate document for a specific plugin's own rules, should one
ever need rules distinct from the framework's).

## 3. `rr-META-003` Every rule has a unique, stable ID

Format: **`(DOC_PREFIX)-(DOMAIN)-(NNN)[-(parent-id)]`**

- **`DOC_PREFIX`** — `fw` for the framework rule document, plus the fixed
  `rr` prefix reserved for this file itself.
- **Name format** — every rule name must be more than the bare ID. The
  canonical name format is **`<rule-id>-<short-summary>`**, where the suffix
  is a lowercase slug that briefly describes what the rule is about. Example:
  `fw-STRUCTURE-002-fixed-deploy-dir`. This is a hard requirement for all new
  rules and must also be applied retroactively to existing deployed rules
  during framework deployment or synchronization. Existing names that are
  only the ID must be renamed to include a summary suffix, and every index
  entry and link that references the old name must be updated.
- **`DOMAIN`** — a short, stable mnemonic code for the `##` functional
domain the rule sits under. Fixed once assigned — renaming a domain's
prose heading does not change its code, since existing IDs (in code
comments, tests, Known Bugs indexes, cross-references) must keep
resolving.
- **`NNN`** — a zero-padded 3-digit sequence number, unique within that
  `DOMAIN`, assigned in document order the first time IDs are
  retrofitted (or in creation order thereafter). Never reused, never
  renumbered, even if an earlier rule in the same domain is later
deleted/retired.
- **`[-parent-id]`** — optional. Used two ways: (a) a rule that is a
  specialization/consequence of another rule references that rule's full
  ID as its own suffix; (b) a numbered sub-item inside a single rule
  bullet that enumerates several concretely distinct behaviors gets the
  parent's ID plus its own position. Prefer this over inventing a new
  top-level rule when the sub-items are only meaningful in the context of
  the parent bullet.

Rules with no sub-items or parent never have the trailing segment — it's
absent, not empty.

### Domain codes — `fw-framework-rules.md`

| Code | Domain |
|------|--------|
| `BEHAVIOR` | Behavioural invariants — how an agent must act (repo-scoped references, install-on-first-load, naming, assent-before-push) |
| `STRUCTURE` | Structural invariants — the deployed tree's own shape (chain, deploy dir, naming, indexing, backlog/roadmap/user persistence) |
| `PLUGINS` | Plugin system invariants — activation gate, provenance, contract stability, deployment-vs-framework operation boundary |

### Domain code — this file

| Code | Domain |
|------|--------|
| `META` | This file's own numbered rules (`rr-META-NNN`) |

### Adding a new rule

1. Pick (or confirm) the `DOMAIN` it belongs to.
2. Take the next unused `NNN` in that domain — check both the domain's
   existing bullets and the Known Bugs index.
3. Only add `[-parent-id]` if the rule is a numbered sub-case of one
   existing bullet, or an explicit specialization of another rule.

## 4. `rr-META-004` Retiring a rule

A rule ID, once assigned, is **never deleted and never reused** —
deleting the bullet outright breaks every cross-reference to it with no
trace of why. Instead, retire it in place:

1. Change its status marker to **🗑 retired**.
2. Leave the rule's text as-is (don't rewrite it to match new behavior —
   that's a *new* rule with a *new* ID) and append a one-line reason plus
the date, e.g. `🗑 retired 2026-08-23 — superseded by \`fw-STRUCTURE-009\``.
3. If something replaces it, the replacement is a normal new rule (next
   `NNN` in its domain) — retirement does not imply the new rule
   inherits the old number, even via `[-parent-id]`.
4. Never repurpose a retired rule's ID for an unrelated rule later, even
   in the same domain.
5. A retired rule can still be a valid target for dev-artifact work (e.g.
   a bug explaining why it had to be retired) — retirement is a status
   change, not removal from the graph of things development work can
   cite.

## 5. `rr-META-005` Rules use typed directories and indexes

Every rule must live in a type-specific directory under `rules/` — for
this project, `framework/`. This is a hard requirement. Each rule must be
stored as its own markdown file in that directory, and that file must be
listed in the corresponding local type index and the global `rules/rules.md`
index. A rule that is not present in its type index or the global index
is considered invalid until it is added to both. The only rule-template
file allowed at the rules root is `rules/TEMPLATE-RULE.md`; concrete rule
files belong under the type folders, not under the rules root. Aggregating
multiple rules into one file or relying on unindexed notes is not
permitted.

## 6. `rr-META-006` Development artifacts have their own ID scheme

Format: **`(BUG|REQ|HK)-(NNNN)`** — see [`CODE-OF-CONDUCT.md`](../CODE-OF-CONDUCT.md).
`NNNN` is a zero-padded 4-digit sequence number, global within its own
type, assigned in creation order, never reused. See §9 for the separate,
non-rule-linked `FEAT-` scheme used for feature entries — it is not a
fourth member of this format.

## 7. `rr-META-007` Defining a new `##` domain

A bug or requirement is not required to fit an existing domain — it may
propose a new one, but only by following this standard.

**Domains are defined in their own directory, not inline in the rule
document.** Each domain gets one file at
`domains/fw-{{CODE}}-{{short-description}}.md` (e.g.
`domains/fw-STRUCTURE-deployed-tree-shape.md`). This is a hard
requirement, the same as for artifact and work-item filenames: the bare
`fw-{{CODE}}.md` is not a valid filename, the file must carry a short
description of what the domain covers as part of its name. The `{{CODE}}`
used inside rule IDs (`fw-{{CODE}}-{{NNN}}`) is unaffected by this — only
the on-disk filename gains the description suffix. See
[`../development-framework/templates/domain.template.md`](../development-framework/templates/domain.template.md)
for the exact file structure (`Document`, `Defined`, `Parent`,
`Sub-domains`, `Scope`, `Relationship to other domains`).

### Sub-domains

Not currently used in this deployment — none of the three domains
(`BEHAVIOR`, `STRUCTURE`, `PLUGINS`) is large enough yet to need
splitting. If one ever grows past the point where "which part of
STRUCTURE does this belong to" stops being obvious, split it per the
general sub-domain mechanism (see the framework's own
`rules-of-rules.template.md` §7 for the full mechanism this project
inherits).

The `##` heading in the rule document itself carries only a one-line
pointer back to the domain file, not the full metadata:

```
## Structural invariants

> **Domain:** `STRUCTURE` — see [`domains/fw-STRUCTURE-deployed-tree-shape.md`](../domains/fw-STRUCTURE-deployed-tree-shape.md).
```

This keeps the rule document itself readable (just rules) while the
domain's scope/conflict metadata lives in one findable, greppable place —
`domains/` is the authoritative index of every domain that exists,
independent of which document's prose you happen to be reading.

### Creating a new domain

1. **Conflict check first**, at the domain level: does an existing
domain already cover this scope, even partially, under a different
name? Check `domains/` directly — it's the complete list. Extend the
existing domain instead of duplicating it.
2. **Pick a code** — uppercase mnemonic, 3–7 characters, not already used
   as a `DOMAIN` code.
3. **Add the code to the canonical table** in this file, and create its
   `domains/fw-{{CODE}}-{{short-description}}.md` file, in the same
   change that adds the domain.
4. **Write the domain file's Scope and Relationship-to-other-domains**,
declaring either no conflict or the specific supersede/amend/
contradict relationship to named existing rule IDs.
5. Add the one-line pointer under the `##` heading in the rule document.
6. Only then add the domain's first rule bullet(s), `NNN` starting at
   `001`.

A domain's code is permanent, same as a rule ID — never reused for an
unrelated domain even if the original is later emptied out or retired
(its `domains/` file gets the same 🗑 retired treatment as a rule, §4).

## 8. `rr-META-008` Scrum/agile work items have their own ID scheme

Format: **`(EPIC|STORY|TASK|SPIKE)-(NNNN)`** and **`SPRINT-(NNN)`** — see
[`work-items/rules-of-work-items.md`](../work-items/rules-of-work-items.md).
Work items are the process layer sitting above `BUG-`/`REQ-`/`HK-` docs.

## 9. `rr-META-009` Feature entries have their own, non-rule-linked scheme

Format: **`FEAT-(NNNN)`** — zero-padded 4-digit sequence number, global,
assigned in creation order, never reused. Same descriptive-naming
requirement as every other artifact and work-item ID: the name and
filename are `FEAT-NNNN-<short-summary>` / `FEAT-NNNN-<short-summary>.md`,
never the bare ID. Stored one file per entry under `features/`, indexed in
`features/features.md`, using
[`../development-framework/templates/features.template.md`](../development-framework/templates/features.template.md)
→ `features/TEMPLATE-FEATURE.md`.

A feature entry documents a possible future capability — an idea or
roadmap item, not a claim about current or required behavior. It is
**not** one of the development artifacts in §6 and is exempt from:

- §1 (`rr-META-001`)'s conflict check,
- `CODE-OF-CONDUCT.md` §1 ("no development without a targeted rule"), and
- ever carrying a `Targets` or `Domain` field.

It is never "done" against a rule and is never itself implemented. Once
work on a feature actually starts, open a `REQ-NNNN` requirement (§6)
that targets or proposes the rule(s) the feature requires — that
requirement, not the feature entry, is what gets vetted against existing
rules, assigned a domain, and measured for completion. The feature entry
records which requirement(s) resulted from it, for traceability back to
the original idea, but that link is informational, not a rule target.

## 10. `rr-META-010` Roadmap items have their own, source-tracked scheme

Format: **`RM-(NNNN)`** — zero-padded 4-digit sequence number, global
across every named roadmap, assigned in the order `/roadmap-add`/
`/roadmap-update`/`/roadmap-merge` first adds each item, never reused.
Roadmap rows are partitioned across one file per named roadmap:
`development/roadmaps/<name>.md`, each registered in
`development/roadmaps/roadmaps.md`.

A roadmap item records that an external source named this as a future
direction — not a claim about current or required behavior, and not
itself one of the development artifacts in §6. It is exempt from the
same three things as a feature entry (§9). Once a human decides it's
worth tracking, `/create-feature` opens a `FEAT-NNNN` for it (§9), citing
the `RM-NNNN` ID in the feature's `Roadmap` field. A named roadmap itself
is never hard-deleted once any of its rows carry a `Linked` value —
`/roadmap-remove` retires it in place instead (§4's principle).

## 11. `rr-META-011` Users and roles are advisory, not access control

`development/users.json` is the registry of people who can sign work — a
JSON array of `{name, roles, registered, active, notes}` objects, managed
exclusively by `/user-add`/`/user-remove`/`/user-modify`/`/user-assign-role`/
`/user-list`. `development/roles.json` maps each role to the
actions/commands it typically performs, extended via `/role-add`/
`/role-modify`.

**`development/users.json` must contain at least one entry with
`"active": true`** — a hard requirement; a project with zero active users
has nobody to sign work. Beyond that, role checks are **advisory**: a
mismatch prompts for confirmation, never a hard block, since this project
has no way to verify who is actually typing. Every dev-artifact, feature
entry, roadmap item, and work item carries a `Signed-off-by` field
recording the outcome. `/user-remove` never deletes a user's entry — it
sets `active` to `false` so every `Signed-off-by` reference stays
resolvable.
