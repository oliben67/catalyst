# Artifact Layout Reference

The canonical, illustrative tree for a deployed `.criterion/` under
the uniform artifact-type layout (`Rules-of-Rules.md` §15, `INVARIANTS.md`
INV-20). `INSTANTIATION-GUIDE.md` §1 is the authoritative prose — this
file exists as a clean, standalone reference to the shape alone, without
the surrounding deploy-procedure text.

## Legend

- `...` — this directory accepts **files only**. Used under every
  `templates/`: a new template version is a new file
  (`TEMPLATE-<TYPE>-v2.md`), never a subfolder, and never an edit to an
  existing version.
- `[...]` — this directory accepts **files and folders, at any depth** —
  the artifact type's own choice of sub-organization for its actual
  instances (e.g. rule documents nested by domain, one file per named
  roadmap).

## The tree

```
/
    .ledger/                    # deployment ledger — unaffected by INV-20
    CODE-OF-CONDUCT.md
    DEPLOYMENT.md
    README.md
    version.txt
    rules/
        templates/
            README.md
            templates-rule.md            # templates catalog: Version | File | Timestamp | Notes
            TEMPLATE-RULE-v1.md
            ...
        domains/                         # nested here — domains exist only to group rules
            templates/
                README.md
                templates-domain.md
                TEMPLATE-DOMAIN-v1.md
                ...
            README.md
            domains.md                   # domains catalog
            [...]
        README.md
        Rules-of-Rules.md
        rules.md                         # rules catalog
        [...]                            # actual rule documents, typically nested by domain
    requirements/
        templates/
            README.md
            templates-requirement.md
            TEMPLATE-REQUIREMENT-v1.md
            ...
        README.md
        requirements.md
        [...]
    features/
        templates/
            README.md
            templates-feature.md
            TEMPLATE-FEATURE-v1.md
            ...
        README.md
        features.md
        [...]
    reconciliations/
        templates/
            README.md
            templates-reconciliation.md
            TEMPLATE-RECONCILIATION-v1.md
            ...
        README.md
        reconciliations.md            # reconciliations catalog
        [...]
    IAM/
        users/
            templates/
                README.md
                templates-users.md       # templates catalog: Version | File | Timestamp | Notes
                TEMPLATE-USERS-v1.json   # versions the registry's seed shape, not a per-instance doc
                ...
            README.md
            users.json                   # users registry (one JSON array)
        roles/
            templates/
                README.md
                templates-roles.md
                TEMPLATE-ROLES-v1.json
                ...
            README.md
            roles.json                   # roles registry (one JSON array)
    plugins/                             # unaffected by INV-20 — a plugin owns its own layout
        <type>/
            [...]
    development/
        roadmaps/
            templates/
                README.md
                templates-roadmap.md
                TEMPLATE-ROADMAP-v1.md
                ...
            README.md
            roadmaps.md                  # roadmaps catalog
            [...]
        bugs/
            templates/
                README.md
                templates-bug.md
                TEMPLATE-BUG-v1.md
                ...
            README.md
            bugs.md                      # bugs catalog
            [...]
        house-keeping/
            templates/
                README.md
                templates-house-keeping.md
                TEMPLATE-HOUSE-KEEPING-v1.md
                ...
            README.md
            house-keeping.md             # house-keeping items catalog
            [...]
        meta-tags/
            templates/
                README.md
                templates-meta-tag.md
                TEMPLATE-META-TAG-v1.md
                ...
            README.md
            meta-tags.md                 # meta-tags catalog
            [...]
        BACKLOG.md                       # not an artifact type (INV-14) — no templates/ of its own
        README.md
        journal.jsonl                    # not an artifact type (INV-17) — no templates/ of its own
```

`work-items/` is **not** part of this core tree — see "Optional,
plugin-provided: `work-items/`" below.

## Exceptions to the pattern

A handful of files are deliberately **not** artifact types and so carry
no `templates/` of their own, even though they sit inside a directory
that has one:

- `development/BACKLOG.md` (INV-14) — machine-regenerated in full by
  `/show-backlog` on every run, never hand-edited, never versioned as a
  template.
- `development/journal.jsonl` (INV-17) — an append-only log, not a
  document type with versions.
- `rules/Rules-of-Rules.md` — the document that *governs* an artifact
  type, sibling to its `templates/` and instance catalog, not an
  instance itself.
- `plugins/` — a plugin's own repository owns its internal structure;
  INV-20 does not reach into it.

## Optional, plugin-provided: `work-items/`

Unlike everything above, `work-items/` is never part of a fresh
deployment by default (`Rules-of-Rules.md` §8, INV-22) — it only exists
once a project-management-type plugin extending
`plugins/_prototyping/project-management/agile/`'s schema is activated.
When one is, the shape it deploys is the same INV-20 pattern as every
core type:

```
    work-items/
        boards/                          # Kanban/Scrumban flavor only
            templates/
                README.md
                templates-board.md
                TEMPLATE-BOARD-v1.md
                ...
            README.md
            boards.md
            [...]
        epics/
            templates/ ...
            README.md
            epics.md
            [...]
        spikes/, sprints/ (Scrum flavor only), stories/, tasks/  # same shape
        tickets/                         # no templates/ — no core semantics (§8)
        workflows/
            templates/ ...
            README.md
            workflows.md
            [...]
        README.md
        rules-of-work-items.md           # governs this type, siblings to its templates/
```

Exactly which of `boards/`/`epics/`/`spikes/`/`sprints/`/`stories/`/
`tasks/`/`tickets/`/`workflows/` actually deploys, and their template
content, is that plugin's own `working-contract.md` `## Contributes`
section — this tree is illustrative of the shape, not a guarantee any
given plugin deploys all of it. No concrete plugin exists yet.

## See also

- [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md) §1 — the full deploy
  procedure this tree is built by.
- [`INSTANTIATION-CHECKLIST.md`](INSTANTIATION-CHECKLIST.md) — the
  tickable version of the same steps.
- [`rules-of-rules.template.md`](rules-of-rules.template.md) §15 — the
  rule this layout satisfies.
- [`migrations/`](migrations/) — how an existing deployment built under
  an older layout gets here.
