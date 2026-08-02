# Instantiation Guide

How to stand up this framework in a project — new or existing — so it
creates concrete rules for that particular project.

## 1. New project

1. Decide your rule document(s) and their prefixes based on the project’s
   actual structure (e.g. one document per natural seam in the system — UI
   vs. backend, or per-service in a multi-service repo). Pick a short
   lowercase prefix per document.
2. Before creating the project layout, locate configuration for the
   framework name. Look for a project-local `.dev-instructions.json` in the
   project where this guide is being run. If it exists, read only its `name`
   value. If it does not exist, ask the user for the project name and use
   the current project root directory name as the default.

   The required format for that file is now:
   ```json
   {
     "name": "project-name"
   }
   ```

   The `name` value is the configurable project name used for the
   instantiated project data. It must be a simple project identifier, not a
   full path or a nested object.

   After the deployment completes successfully, remove the project-local
   `.dev-instructions.json` file from the project root. It was only needed as
   temporary bootstrap metadata for discovering the project name and is no
   longer needed once the framework has been deployed.
3. Pick a root layout, e.g.:
   ```
   <project-root>/.catalyst-proj/
     rules/
       rules-of-rules.md
       domains/
       <rule-doc-1>.md
       <rule-doc-2>.md
     requirements/
       requirements-template.md
       <requirement-doc-1>.md
       <requirement-doc-2>.md
     development/
       rules-of-development.md
       bugs/
       house-keeping/
       domains/
     work-items/
       rules-of-work-items.md
       epics/  stories/  tasks/  spikes/  sprints/
   ```
   (The deployment directory is fixed: `.catalyst-proj/`. No exception.
   The framework only cares that the chain epic→story→task→REQ/BUG/HK→rule
   stays intact, not the folder names. In deployed instances, the old
   `sections/` folder should now be represented as `development/domains/`.)
4. Copy `rules-of-rules.template.md` → `rules/rules-of-rules.md`, resolve
   placeholders: `{{RULE_DOCS_LIST}}`, `{{TEST_LOCATIONS}}`, the domain-
   code tables (start empty — filled in as domains get created per §6).
   If the project already has relevant practices, policies, or working
   conventions, merge them into these rules rather than replacing them.
   If there is a conflict between the framework and an existing project
   practice, stop and ask the user clarifying questions before deciding
   how to resolve it.
5. Copy `rules-of-development.template.md` and
   `rules-of-work-items.template.md` similarly.
6. Copy `templates/*.template.md` into the corresponding subfolders,
   dropping the `.template` from the name if you want a ready-to-copy
   starting file per type. Keep requirements templates in the same
   `requirements/` directory as the actual requirements documents so the
   template and the concrete requirement files live together.
7. Create a starter requirements document in `requirements/` based on the
   project's rule documents (for example, UI rules such as
   `UI-Rules.md` or business rules such as `business-rules.md`) and keep
   it aligned with the rule IDs or source documents that define the
   expected behavior. Requirements must be concrete and tied to specific
   application areas, screens, flows, or components, because they are the
   basis for tests and for the bugs that will later be raised when the
   behavior is wrong.
8. Create your first rule document(s) with a `## Contents` heading and a
   `## Known Bugs — Quick Index` heading (even if empty) — the rest fills
   in as domains/rules get added, each per `rules-of-rules.md` §6, so the
   framework produces rules that are specific to this project.
## 2. Choosing your agile flavor

Nothing below the work-items layer changes. Above it:

- Using Scrum → keep everything as templated (sprints included).
- Using Kanban → skip `sprints/`; add a WIP-limited `Status` value set to
  stories/tasks instead.
- Using something else entirely → the framework's hard requirement is
  only §1 of `rules-of-development.md` (no development without a
  targeted rule) — everything above that is replaceable with whatever
  process vocabulary your team actually uses, as long as it still
  bottoms out in `FEAT-`/`BUG-`/`HK-` docs.

## 3. Retrofitting an existing project

1. Do **not** try to write every rule up front. Start with
   `rules-of-rules.md`, `rules-of-development.md`,
   `rules-of-work-items.md` (or your project's equivalents) and an empty
   `domains/` directory.
2. Gather rules incrementally — per functional area, as you touch it, or
   via a dedicated audit pass (parallel research agents/subagents
   covering one rule category each, cross-checked against the codebase
   and test suite, is one effective way to bootstrap a first pass quickly
   — but the resulting rules still need the §1 conflict check and the
   gathered/implemented/tested/documented bar from §2 before they count
   as real, not just an audit report). If the project already has
   established practices, merge them into the new ruleset and preserve
   what is still valuable rather than discarding it. If conflicts arise,
   pause and ask the user questions so the final rule reflects the
   project’s intent rather than an arbitrary choice.
3. As each functional domain is identified, create its
   `domains/<prefix>-<CODE>.md` file per §6 before adding rule bullets
   under it.
4. Retrofit IDs onto existing prose bullets (if a rules doc already
   exists in some other form) in document order, per §3 — top-level
   bullets get `NNN`; enumerated sub-cases inside one bullet get
   `-1`/`-2`/... suffixes rather than new top-level IDs.
5. Once rules exist, retrofit `BUG-`/`FEAT-`/`HK-` docs for any
   already-known issues (a "Known Bugs" index is a good source), citing
   the rule IDs from step 4.
6. Add a one-line header to each of your project's `rules-of-*.md` files
   noting which template in this framework they instantiate, e.g.:
   ```
   > Instantiates [`development-framework/rules-of-rules.template.md`](../../development-framework/rules-of-rules.template.md).
   ```
   This keeps the project's concrete process traceable back to the
   generic framework as the framework itself evolves.

## 4. Keeping the two in sync

When a process rule changes in a project (e.g. this repo adds a new
`rr-META-NNN`), evaluate whether it's project-specific or a generally
useful addition to this framework. If general, port it back into the
`.template.md` files here so the next project instantiation starts from
the improved version. When the project already has existing practices,
merge them into the framework rather than treating the framework as a
replacement for what is already there. If a conflict cannot be resolved
from the existing context, stop and ask the user targeted questions
before continuing.

## 5. Remember the deployment target across sessions

After a successful instantiation, record the project root path and the
project deployment path (`.catalyst-proj/`) in the persistent memory store
so later sessions can recover which project this framework was deployed
into without having to rediscover it.

Keep a compact note with at least:

- the framework name (`development-framework`)
- the deployed project path
- the deployment directory path for that project (`.catalyst-proj/`)
- the date or context of the instantiation
- any short notes that help identify the project later

When this guide is used again for the same project, check memory first and
reuse the existing note as the default project context. If a prior note
already exists for that project, update it instead of creating a duplicate.
This makes the association durable across sessions and keeps the project's
instantiated ruleset available whenever the guide is used again.

At the end of a successful instantiation, if the new project currently has
no bugs, features, house-keeping items, or other tracked work items yet,
propose running [`analysis-playbook.md`](analysis-playbook.md) next to help
bootstrap the first round of project-specific rules and evidence.
