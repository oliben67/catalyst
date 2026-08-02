# Rules of Development — template

> Copy to `{{DEV_DIR}}/rules-of-development.md` and resolve every
> `{{PLACEHOLDER}}`. See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md).

Standards for how development work — bugs, requirements, house-keeping, and
meta-tags — gets proposed, tracked, and closed. Subordinate to
[`{{RULES_DIR}}/rules-of-rules.md`](../{{RULES_DIR}}/rules-of-rules.md):
that file governs the rules themselves; this file governs the work items
that reference those rules.

---

## 1. No development without a targeted rule

**No bug, requirement, house-keeping work, or meta-tag may start without
citing one or more existing rule IDs in its `Targets` field when the tag is
used to annotate a rule-linked artifact.** If no rule currently covers the
behavior in question:

1. Define the rule(s) first, as a normal edit to the relevant rule
document.
2. That definition must satisfy `rules-of-rules.md` §1 (conflict check)
and follow the ID scheme in §3.
3. Only then open the `BUG-`/`REQ-`/`HK-` item, citing the new ID(s).

House-keeping is the one category where "no rule applies" is a legitimate
answer (pure repo hygiene with no bearing on any documented behavior or
process) — but it must be stated explicitly, not left blank.

## 2. Standard document types

| Type | Folder | Template | ID prefix |
|---|---|---|---|
| Bug | `bugs/` | `templates/bug.template.md` | `BUG-NNNN` |
| Requirement | `requirements/` | `templates/requirements.template.md` | `REQ-NNNN` |
| House-keeping | `house-keeping/` | `templates/house-keeping.template.md` | `HK-NNNN` |
| Meta-tag | `meta-tags/` | `templates/meta-tag.template.md` | `TAG-<KEY>-<ARTEFACT-ID>` |

### Hard rule: individual files and indexes

- **Bugs** must be stored as individual files in `bugs/`, not only as free-form notes.
- **Requirements** must be stored as individual files in `requirements/`, not only as abstract definitions.
- Each item directory must also contain an index file named after the item type:
  - `bugs/bugs.md` for the bug index.
  - `requirements/requirements.md` for the requirements index.
  - `house-keeping/house-keeping.md` for the house-keeping index.
  - `meta-tags/meta-tags.md` for the meta-tag index.
- These index files are the canonical indexes for their directory and must be kept up to date.
- `BACKLOG.md` remains the go-to document for developers to review work to be done and current status.

- **Bug**: an existing ✅ rule doesn't actually hold in the running system,
  or formalizes an already-known ⚠️/❌ rule into trackable, closeable work.
  Never introduces a new rule by itself.
- **Requirement**: an explicit, tracked requirement that captures
  user/business behavior that must be implemented and tested. It may target
  existing rules and/or propose new ones (and, if needed, a new domain — see
  `rules-of-rules.md` §6) inline in the requirement doc so rule and
  requirement are reviewed together.
- **House-keeping**: dev-support tooling/process, not product behavior.
  Still targets a rule where one exists — most commonly a `rr-META-*`
  process rule.
- **Meta-tag**: a lightweight annotation attached to an existing artifact.
  It stores one key/value pair whose key is one of `comment`, `version`, or
  `link-to`, and it is saved under the name `tag-<key>-<artefact-id>`.

## 3. Slash-command entry points

When the user enters `/create-bug: ...`, create a new bug artifact immediately,
register it in `bugs/bugs.md`, and track it in the same workflow as any other
bug. If the domain cannot be inferred from context, prompt for the domain and
rule before creating the artifact.

When the user enters `/create-req:` or `/create-requirement: ...`, create a
new requirement artifact immediately, register it in
`requirements/requirements.md`, and track it in the same workflow. If the
domain or target rule cannot be inferred, prompt for both before creating the
artifact.

When the user enters `/meta-tag <artefact-id>`, create a new meta-tag artifact
immediately, save it as `tag-<key>-<artefact-id>`, register it in
`meta-tags/meta-tags.md`, and link it to the specified artifact. If the key
is not supplied explicitly, prompt for it.

When the user enters `/status <artefact-id> <status> [force]`, update the
artifact's `Status` field. If the supplied status is one of the valid statuses
for that artifact type, change it normally. If the status is invalid and the
command includes the word `force`, change it to that invalid value anyway. If
the status is invalid and `force` is not supplied, respond that the status
change is impossible and do not modify the artifact. If the artifact ID does
not resolve to an existing artifact, state that the artifact cannot be found.

When the user enters `/help` without any additional entry, list all supported
custom slash commands and their purpose, then list every artifact type and its
purpose in a compact reference format.

## 4. Domain field

Every item's `Domain` field is the `DOMAIN` code of the rule(s) it targets,
from `{{RULES_DIR}}/domains/` — not free text.

## 5. Development-artifact IDs

Per `rules-of-rules.md` §5: `(BUG|REQ|HK)-(NNNN)`, global per type,
sequential, zero-padded 4 digits, never reused. Meta-tags use a file-name
pattern of `tag-<key>-<artefact-id>` rather than a sequential numeric ID.

## 6. Closing an item

Before closing a bug or requirement, ensure the corresponding entry exists in
its individual file and is reflected in the relevant index file.

- **Bug**: not closeable as "fixed" without its test-plan item landing.
- **Requirement**: not closeable as "done" until the acceptance criteria and
  rule targets are reflected in the implementation and tests.
- **House-keeping**: closeable once its stated verification passes.

## 7. Retired rules and development work
