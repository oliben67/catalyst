# Rules of Development — template

> Copy to `{{DEV_DIR}}/rules-of-development.md` and resolve every
> `{{PLACEHOLDER}}`. See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md).

Standards for how development work — bugs, features, and house-keeping —
gets proposed, tracked, and closed. Subordinate to
[`{{RULES_DIR}}/rules-of-rules.md`](../{{RULES_DIR}}/rules-of-rules.md):
that file governs the rules themselves; this file governs the work items
that reference those rules.

---

## 1. No development without a targeted rule

**No bug, feature, or house-keeping work may start without citing one or
more existing rule IDs in its `Targets` field.** If no rule currently
covers the behavior in question:

1. Define the rule(s) first, as a normal edit to the relevant rule
   document.
2. That definition must satisfy `rules-of-rules.md` §1 (conflict check)
   and follow the ID scheme in §3.
3. Only then open the `BUG-`/`FEAT-`/`HK-` item, citing the new ID(s).

House-keeping is the one category where "no rule applies" is a legitimate
answer (pure repo hygiene with no bearing on any documented behavior or
process) — but it must be stated explicitly, not left blank.

## 2. Standard document types

| Type | Folder | Template | ID prefix |
|---|---|---|---|
| Bug | `bugs/` | `templates/bug.template.md` | `BUG-NNNN` |
| Feature | `features/` | `templates/feature.template.md` | `FEAT-NNNN` |
| House-keeping | `house-keeping/` | `templates/house-keeping.template.md` | `HK-NNNN` |

### Hard rule: individual files and indexes

- **Bugs** must be stored as individual files in `bugs/`, not only as free-form notes.
- **Requirements** must be stored as individual files in `requirements/`, not only as abstract definitions.
- Each item directory must also contain an index file named after the item type:
  - `bugs/bugs.md` for the bug index.
  - `requirements/requirements.md` for the requirements index.
- These index files are the canonical indexes for their directory and must be kept up to date.
- `BACKLOG.md` remains the go-to document for developers to review work to be done and current status.

- **Bug**: an existing ✅ rule doesn't actually hold in the running system,
  or formalizes an already-known ⚠️/❌ rule into trackable, closeable work.
  Never introduces a new rule by itself.
- **Feature**: new or changed behavior. May target existing rules and/or
  propose new ones (and, if needed, a new section — see
  `rules-of-rules.md` §6) inline in the feature doc, so rule and feature
  are reviewed together.
- **House-keeping**: dev-support tooling/process, not product behavior.
  Still targets a rule where one exists — most commonly a `rr-META-*`
  process rule.

## 3. Section field

Every item's `Section` field is the `SECTION` code of the rule(s) it
targets, from `{{RULES_DIR}}/sections/` — not free text.

## 4. Development-artifact IDs

Per `rules-of-rules.md` §5: `(BUG|FEAT|HK)-(NNNN)`, global per type,
sequential, zero-padded 4 digits, never reused.

## 5. Closing an item

Before closing a bug or requirement, ensure the corresponding entry exists in
its individual file and is reflected in the relevant index file.

- **Bug**: not closeable as "fixed" without its test-plan item landing.
- **Feature**: not closeable as "shipped" until every rule in its targets/
  new-rules sections is itself ✅ and tested.
- **House-keeping**: closeable once its stated verification passes.

## 6. Retired rules and development work

An item targeting a rule later retired is not retroactively invalidated —
it stays as historical record. New items should not target an
already-retired rule unless the item is specifically about the
retirement itself.
