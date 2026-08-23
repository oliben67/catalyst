# Rules of Rules — template

> Copy this file to `{{RULES_DIR}}/Rules-of-Rules.md` in the target
> project and resolve every `{{PLACEHOLDER}}`. Delete this notice once
> instantiated. See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md).

Meta-rules governing how any rule gets added to, changed in, or retired
from one of this project's rule documents: {{RULE_DOCS_LIST}}. These
apply to the *process* of maintaining those documents and the code they
describe, not to the app's behavior itself. Binding on anyone (human or
agent) adding to any of them, at any point after this file exists.

Each rule must belong to a rule type directory under `{{RULES_DIR}}/`, be
stored as its own markdown file in that directory, be listed in the
corresponding type index, and be referenced from the global index
`{{RULES_DIR}}/rules.md`. There must be exactly one template file at
`{{RULES_DIR}}/TEMPLATE-RULE.md` and no `TEMPLATE-RULE.md` files inside the
rule-type directories. No rule may be orphaned by missing a type, a local
index entry, or a global index entry.

---

## 1. `rr-META-001` Check for conflicts before adding a new rule

Before a new rule is implemented, check it against the rules already
recorded in **every** rule document in {{RULE_DOCS_LIST}} — not just the
document that seems most relevant, since the same underlying behavior is
sometimes governed from more than one angle (e.g. a UI-visible
enabled/disabled state and the backend constraint it's supposed to
reflect), and a change to one side can silently break the other. Check,
in order:

1. The same functionality area in whichever document(s) are relevant.
2. Each document's Cross-Cutting Notes heading (or equivalent).
3. Each document's Known Bugs / Quick Index heading — a "new" rule is
   sometimes actually a conflicting rewrite of an existing one.

If the new rule **contradicts, narrows, silently overrides, or would
break** an existing ✅ rule in any document, **stop and prompt for a
decision** — do not silently override it, and do not silently implement
both side by side and let whichever runs last win.

## 2. `rr-META-002` A new rule is never done until it's gathered, implemented, tested, and documented

All four, no exceptions:

- **Gathered** — the rule's actual current/intended behavior is
  understood and written down before code changes.
- **Implemented** — the rule actually exists in the code, not just in a
  comment, commit message, or this documentation.
- **Tested** — it has **at least one test** exercising it. Name the
  project's test locations here: {{TEST_LOCATIONS}}. A rule with zero
  test coverage is not "done" — it's "implemented but untested," and
  should be marked as such (see status markers below), not treated as an
  acceptable end state.
- **Documented** — added to the correct rule document, under the
  functionality domain it belongs to and the right rule category, with a
  `file:line` citation and a status marker, in the same format every
  existing entry already uses.

**Status markers**: ✅ working · ⚠️ buggy/incomplete · ❌ not implemented
/ regressed · 🗑 retired (see §4).

## Which document does a rule belong in?

Project-specific tiebreaker guidance goes here — e.g.:

- **{{RULE_DOC_1}}**: {{tiebreaker description}}.
- **{{RULE_DOC_2}}**: {{tiebreaker description}}.

Not a hard wall — some rules legitimately have entries in more than one
document (one for how it's surfaced, one for the constraint it enforces)
and should cross-reference rather than pick just one.

## 3. `rr-META-003` Every rule has a unique, stable ID

Format: **`(DOC_PREFIX)-(DOMAIN)-(NNN)[-(parent-id)]`**

- **`DOC_PREFIX`** — which rule document the rule lives in. Define one
  short lowercase prefix per document in {{RULE_DOCS_LIST}} (e.g. `ui`,
  `br`), plus the fixed `rr` prefix reserved for this file itself.
- **Name format** — every rule name must be more than the bare ID. The
  canonical name format is **`<rule-id>-<short-summary>`**, where the suffix
  is a lowercase slug that briefly describes what the rule is about. Example:
  `br-AUTH-003-login-flow`. This is a hard requirement for all new rules and
  must also be applied retroactively to existing deployed rules during
  framework deployment or synchronization. Existing names that are only the ID
  must be renamed to include a summary suffix, and every index entry and link
  that references the old name must be updated.
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
  parent's ID plus its own position (e.g. `br-EVTO-015-1`). Prefer this
over inventing a new top-level rule when the sub-items are only
  meaningful in the context of the parent bullet.

Rules with no sub-items or parent never have the trailing segment — it's
absent, not empty.

### Domain codes — {{RULE_DOC_1}}

| Code | Domain |
|------|--------|
| `{{CODE}}` | {{Domain name}} |

### Domain codes — {{RULE_DOC_2}}

| Code | Domain |
|------|--------|
| `{{CODE}}` | {{Domain name}} |

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
the date, e.g. `🗑 retired {{DATE}} — superseded by \`{{new-id}}\``.
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

Every rule must live in a type-specific directory under `{{RULES_DIR}}/`, for
example `business/`, `ui/`, or `infra/`. This is a hard requirement. Each
rule must be stored as its own markdown file in that directory, and that file
must be listed in the corresponding local type index and the global
`{{RULES_DIR}}/rules.md` index. A rule that is not present in its type index
or the global index is considered invalid until it is added to both. The
only rule-template file allowed at the rules root is
`{{RULES_DIR}}/TEMPLATE-RULE.md`; concrete rule files belong under the type
folders, not under the rules root. Aggregating multiple rules into one file or
relying on unindexed notes is not permitted.

## 6. `rr-META-006` Development artifacts have their own ID scheme

If the deployed framework is missing `version.txt`, or if its version is
missing or lower than the current framework version (`0.1.10`), the deployed
framework must be synchronized before further work proceeds. See
[`SYNCHRONIZE.md`](SYNCHRONIZE.md).

Format: **`(BUG|REQ|HK)-(NNNN)`** — see
[`rules-of-development.template.md`](rules-of-development.template.md).
`NNNN` is a zero-padded 4-digit sequence number, global within its own
type, assigned in creation order, never reused. See §9 for the separate,
non-rule-linked `FEAT-` scheme used for feature entries — it is not a
fourth member of this format.

## 7. `rr-META-007` Defining a new `##` domain

A bug or requirement is not required to fit an existing domain — it may
propose a new one, but only by following this standard, in every rule
document.

**Domains are defined in their own directory, not inline in the rule
document.** Each domain gets one file at
`{{RULES_DIR}}/domains/{{DOC_PREFIX}}-{{CODE}}-{{short-description}}.md` (e.g.
`domains/br-REDIS-caching-layer.md`). This is a hard requirement, the same as
for artifact and work-item filenames (see `INSTANTIATION-GUIDE.md` §1): the
bare `{{DOC_PREFIX}}-{{CODE}}.md` is not a valid filename, the file must carry
a short description of what the domain covers as part of its name. The
`{{CODE}}` used inside rule IDs (`{{DOC_PREFIX}}-{{CODE}}-{{NNN}}`) is
unaffected by this — only the on-disk filename gains the description suffix.
See [`templates/domain.template.md`](templates/domain.template.md) for the
exact file structure (`Document`, `Defined`, `Parent`, `Sub-domains`,
`Scope`, `Relationship to other domains`).

### Sub-domains

A domain may be split into sub-domains when its scope is genuinely
large enough that "which part of GATE does this rule belong to" stops
being obvious from the flat list — not by default, and not just to make a
domain file shorter.

- **Code**: `{{PARENT}}.{{SUB}}` — parent code, a literal `.`, then a
  short sub-mnemonic (e.g. `GATE.DOCKER`). This is still one `DOMAIN`
  value for ID purposes: a rule under it is
  `{{DOC_PREFIX}}-{{PARENT}}.{{SUB}}-{{NNN}}` (e.g. `ui-GATE.DOCKER-004`),
  with `NNN` scoped to the sub-domain, not the parent.
- **File**: `domains/{{DOC_PREFIX}}-{{PARENT}}.{{SUB}}-{{short-description}}.md`,
  alongside (not nested under) the parent's own
  `domains/{{DOC_PREFIX}}-{{PARENT}}-{{short-description}}.md` — the
  directory itself stays flat; the nesting is expressed by the code and by
  the `Parent`/`Sub-domains` fields cross-linking the two files.
- **Parent file** lists every child in its `Sub-domains` field. **Child
  file** names its `Parent` and inherits the parent's Scope/Relationship
  statements unless it explicitly narrows or overrides them.
- A sub-domain is subject to every other rule in this domain (conflict
  check, permanence, retirement) exactly like a top-level domain — it is
  not a lesser or informal category, just a narrower one.
- Sub-domains do not nest further than one level. If a sub-domain needs
  its own sub-domains, that's a sign the parent domain should be split
  into multiple top-level domains instead.

The `##` heading in the rule document itself carries only a one-line
pointer back to this file, not the full metadata:

```
## {{Domain name}}

> **Domain:** `CODE` — see [`domains/{{DOC_PREFIX}}-{{CODE}}-{{short-description}}.md`](domains/{{DOC_PREFIX}}-{{CODE}}-{{short-description}}.md).
```

This keeps the rule document itself readable (just rules) while the
domain's scope/conflict metadata lives in one findable, greppable place
per domain — `{{RULES_DIR}}/domains/` is the authoritative index of
every domain that exists across every rule document, independent of
which document's prose you happen to be reading.

### Creating a new domain

1. **Conflict check first**, at the domain level: does an existing
domain already cover this scope, even partially, under a different
name? Check `{{RULES_DIR}}/domains/` directly — it's the complete
list. Extend the existing domain instead of duplicating it.
2. **Pick a code** — uppercase mnemonic, 3–7 characters, not already used
   as a `DOMAIN` code in the same document.
3. **Add the code to the canonical table** in this file, and create its
   `domains/{{DOC_PREFIX}}-{{CODE}}-{{short-description}}.md` file, in the
   same change that adds the domain.
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

The framework version is tracked in `version.txt` at the framework root.
If a deployed framework has no `version.txt`, or its version is lower than
`0.1.10`, it is considered out of date and must be synchronized using
[`SYNCHRONIZE.md`](SYNCHRONIZE.md).

Format: **`(EPIC|STORY|TASK|SPIKE)-(NNNN)`** and **`SPRINT-(NNN)`** — see
[`rules-of-work-items.template.md`](rules-of-work-items.template.md).
Work items are the process layer sitting above `BUG-`/`REQ-`/`HK-` docs.

## 9. `rr-META-009` Feature entries have their own, non-rule-linked scheme

Format: **`FEAT-(NNNN)`** — zero-padded 4-digit sequence number, global,
assigned in creation order, never reused. Same descriptive-naming
requirement as every other artifact and work-item ID (`INSTANTIATION-GUIDE.md`
§1): the name and filename are `FEAT-NNNN-<short-summary>` /
`FEAT-NNNN-<short-summary>.md`, never the bare ID. Stored one file per
entry under `features/`, indexed in `features/features.md`, using
[`templates/features.template.md`](templates/features.template.md) →
`features/TEMPLATE-FEATURE.md`.

A feature entry documents a possible future capability — an idea or
roadmap item, not a claim about current or required behavior. It is
**not** one of the development artifacts in §6 and is exempt from:

- §1 (`rr-META-001`)'s conflict check,
- `rules-of-development.md` §1 ("no development without a targeted
  rule"), and
- ever carrying a `Targets` or `Domain` field.

It is never "done" against a rule and is never itself implemented. Once
work on a feature actually starts, open a `REQ-NNNN` requirement (§6)
that targets or proposes the rule(s) the feature requires — that
requirement, not the feature entry, is what gets vetted against existing
rules, assigned a domain, and measured for completion. The feature entry
records which requirement(s) resulted from it, for traceability back to
the original idea, but that link is informational, not a rule target.

## 10. `rr-META-010` Roadmap items have their own, source-tracked scheme

Format: **`RM-(NNNN)`** — zero-padded 4-digit sequence number, **global
across every named roadmap**, assigned in the order `/roadmap-add`/
`/roadmap-update`/`/roadmap-merge` first adds each item, never reused.
Unlike a rule or a dev-artifact but like `FEAT-NNNN`, an `RM-` item is a
table row, not its own file — but unlike `FEAT-NNNN` (one flat
`features/features.md`), roadmap rows are partitioned across **one file
per named roadmap**: `development/roadmaps/<name>.md`
(`templates/roadmap.template.md`), each registered in
`development/roadmaps/roadmaps.md`. A project may hold several named
roadmaps at once (e.g. a product roadmap and an infra roadmap, ingested
and updated independently); an `RM-NNNN` ID stays unique and resolvable
regardless of which named roadmap's file it lives in.

A roadmap item records that an external source (a product roadmap, a
planning doc, a stakeholder request) named this as a future direction —
not a claim about current or required behavior, and not itself one of the
development artifacts in §6. It is exempt from:

- §1 (`rr-META-001`)'s conflict check,
- `rules-of-development.md` §1 ("no development without a targeted
  rule"), and
- ever carrying a `Targets` or `Domain` field.

A roadmap item is never "done" against a rule and is never itself
implemented. Once a human decides it's worth tracking inside catalyst,
`/create-feature` opens a `FEAT-NNNN` for it (§9), citing the `RM-NNNN` ID
in the feature's `Roadmap` field — that feature entry, and the `REQ-NNNN`
it may later become, are what actually get vetted, assigned a domain, and
measured. Each roadmap file's `Status`/`Linked` columns mirror whichever
of those is currently linked, refreshed by `/show-backlog`, so a roadmap
item's progress stays visible without becoming a second, competing source
of truth for completion.

A named roadmap itself is never hard-deleted once any of its rows carry a
`Linked` value — see §4's retirement principle. `/roadmap-remove` retires
it in place instead (marks it retired, keeps every row and ID resolvable)
whenever removing it outright would break a `FEAT-`/`REQ-` cross-reference.

## 11. `rr-META-011` Users and roles are advisory, not access control

`development/users.json` (`templates/users.template.json`) is the registry
of people who can sign work — a JSON array of `{name, roles, registered,
active, notes}` objects, kept as data rather than a hand-edited document
because it is managed exclusively by commands:
`/user-add`/`/user-remove`/`/user-modify`/`/user-assign-role`/`/user-list`
— see `rules-of-development.md` §4. `development/roles.json`
(`templates/roles.template.json`) maps each role to the actions/commands
it typically performs — a JSON array of `{name, actions}` objects, seeded
with a default agile-role mapping and then extended via `/role-add`
(new role) and `/role-modify` (change an existing role's actions).

**`development/users.json` must contain at least one entry with `"active":
true`.** This is a hard requirement, unlike `roadmaps.md`'s "empty is
fine": a project with zero active users has nobody to sign work, so
deployment is not complete until `/user-add` has registered at least one
person. `/user-remove` refuses (or warns, per the command's own spec) if
removing the last active user would leave zero.

Catalyst has no way to verify who is actually typing, so beyond that one
hard existence requirement, this scheme is **advisory**: before an
artifact-creating or status-changing command completes, the agent
resolves who is signing it, checks their role(s) against `roles.json`,
and — if the action isn't one their role covers, or they aren't
registered at all — asks for confirmation rather than refusing outright.
Every dev-artifact, feature entry, roadmap item, and work item carries a
`Signed-off-by` field recording the outcome (`rules-of-development.md`
§2).

`/user-remove` never deletes a user's entry, the same "never delete,
retire in place" principle as §4 and §10: it sets `active` to `false` so
every `Signed-off-by` reference already recorded against that name stays
resolvable. A changed or removed role in `roles.json` likewise never
retroactively changes a `Signed-off-by` value already recorded — that
value reflects who signed it under the mapping in effect at the time.
