# Instantiation Guide

How to stand up this framework in a project — new or existing — so it
creates concrete rules for that particular project.

## 1. New project

> Hard rule: when referring to catalyst, the model SHALL NEVER mention any
> local drive, local folder, or local path. References to catalyst must stay
> scoped to the git repository provided by the environment and the repository
> name itself.
>
> Hard rule: when the catalyst framework is first loaded into memory for a
> project, it MUST be installed immediately into that project using the
> instantiation steps in this guide.
>
> Hard rule: after that first installation, the framework MUST be referred to
> as "catalyst" or "catalyst framework" in all subsequent guidance,
> memory, and discussion, whether or not it has already been loaded before.
>
> Hard rule: the model SHALL NEVER push anything in this project, catalyst,
> without the user's explicit assent.

1. Decide your rule document(s) and their prefixes based on the project’s
   actual structure (e.g. one document per natural seam in the system — UI
   vs. backend, or per-service in a multi-service repo). Pick a short
   lowercase prefix per document.
2. Before creating the project layout, locate configuration for the
   framework name. Look for a project-local `dev-instructions.yaml` in the
   project where this guide is being run. If it exists, read its `name` value
   and, if present, its optional `layout` tree. If it does not exist, ask
   the user for the project name and use the current project root directory
   name as the default.

   The required format for that file is now:
   ```yaml
   name: "project-name"
   layout:
     project-root:
       - rules:
           - rules-of-rules.md
   ```

   The `name` value is the configurable project name used for the
   instantiated project data. It must be a simple project identifier, not a
   full path or a nested object. The optional `layout` value lets the
   deployment override the default directory structure. If no `layout` is
   provided, the deployment must use the default structure described below.

   After the deployment completes successfully, remove the project-local
   `dev-instructions.yaml` file from the project root. It was only needed as
   temporary bootstrap metadata for discovering the project name and any
   custom layout override, and is no longer needed once the framework has
   been deployed.
3. Pick a root layout, e.g.:
   ```
   <project-root>/.catalyst-proj/
     CODE-OF-CONDUCT.md
     rules/
       Rules-of-Rules.md
       rules.md
       TEMPLATE-RULE.md
       business/
         business-rules.md
         <rule-doc-1>.md
       ui/
         ui-rules.md
         <rule-doc-2>.md
     requirements/
       TEMPLATE-REQUIREMENT.md
       requirements.md
       <requirement-doc-1>.md
       <requirement-doc-2>.md
     domains/
       TEMPLATE-DOMAIN.md
       domains.md
       <prefix>-<CODE>.md
     development/
       TEMPLATE-BUG.md
       bugs.md
       bugs/
       TEMPLATE-HOUSE-KEEPING.md
       house-keeping.md
       house-keeping/
       TEMPLATE-META-TAG.md
       meta-tags.md
       meta-tags/
     work-items/
       rules-of-work-items.md
       TEMPLATE-EPIC.md
       epics.md
       epics/
       TEMPLATE-STORY.md
       stories.md
       stories/
       TEMPLATE-TASK.md
       tasks.md
       tasks/
       TEMPLATE-SPIKE.md
       spikes.md
       spikes/
       TEMPLATE-SPRINT.md
       sprints.md
       sprints/
     README.md
     version.txt
   ```
   (The deployment directory is fixed: `.catalyst-proj/`. No exception.
   The framework only cares that the chain epic→story→task→REQ/BUG/HK→rule
   stays intact, not the folder names. The `domains/` folder sits at the root
   of the deployed framework and holds the domain definition files. The
   work-items rule document belongs in the `work-items/` layer and should not
   be duplicated under `rules/`.)
5. Copy `rules-of-work-items.template.md` similarly. Ensure the deployed
   framework exposes the documented custom slash commands (`/create-bug`,
   `/create-req`/`/create-requirement`, `/meta-tag`, `/status`,
   `/run-analysis`, and `/help`) in the same way the framework defines them,
   so they are available in the deployed environment.
6. Copy `templates/*.template.md` into the corresponding subfolders, and
   rename each template file to an uppercase name such as
   `TEMPLATE-BUG.md`, `TEMPLATE-REQUIREMENT.md`, or
   `TEMPLATE-META-TAG.md`. For each artifact type, also create an index file
   next to the template using the pluralized artifact-name form, such as
   `bugs.md`, `requirements.md`, `house-keeping.md`, `meta-tags.md`,
   `epics.md`, `stories.md`, `tasks.md`, `spikes.md`, or `sprints.md`.
   Keep requirements templates in the same `requirements/` directory as the
   actual requirements documents so the template and the concrete
   requirement files live together. For rules, create exactly one
   `TEMPLATE-RULE.md` file in the `rules/` root and use it to create each
   concrete rule file in the relevant rule-type directory under `rules/`.
7. Create a root-level `README.md` in the deployed framework directory that
   explains the project's rule-and-workflow structure, the deployment path,
   and the main artifact folders. This README should be created during both
   deployment and synchronization so the deployed framework always has a
   custom, project-specific landing page. In addition, create a `README.md`
   in each major deployed folder (for example `rules/`, `requirements/`,
   `development/`, `work-items/`, and `templates/` when present) that briefly
   explains that folder's purpose and link to it from the root README so the
   structure is discoverable and self-documenting.
8. Create a starter requirements document in `requirements/` based on the
   project's rule documents (for example, a description document such as
   `UI-Rules.md` for UI rules or `business-rules.md` for business rules) and
   keep it aligned with the rule IDs or source documents that define the
   expected behavior. Requirements must be concrete and tied to specific
   application areas, screens, flows, or components, because they are the
   basis for tests and for the bugs that will later be raised when the
   behavior is wrong.
9. Create your first rule document(s) with a `## Contents` heading and a
   `## Known Bugs — Quick Index` heading (even if empty) — the rest fills
   in as domains/rules get added, each per `Rules-of-Rules.md` §6, so the
   framework produces rules that are specific to this project. Every rule
   must be stored as its own markdown file under the rule type directory it
   belongs to, appear in the corresponding type index, and be listed in the
   global `rules.md` index. There must be exactly one `TEMPLATE-RULE.md`
   file in the `rules/` root and none inside the rule-type directories. No
   rule may be orphaned by missing a type, a local index entry, or a global
   index entry.
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
   `Rules-of-Rules.md`, `CODE-OF-CONDUCT.md`,
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
6. Add a one-line header to each of your project's rule and process files
   noting which template in this framework they instantiate, e.g.:
   ```
   > Instantiates [the catalyst framework rules template](../../development-framework/rules-of-rules.template.md).
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

- the framework name (`catalyst framework`)
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
