# Rules of Development — template

> Copy to `CODE-OF-CONDUCT.md` in the project root and resolve every
> `{{PLACEHOLDER}}`. See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md).

Standards for how development work — bugs, requirements, house-keeping, and
meta-tags — gets proposed, tracked, and closed. Subordinate to
[`{{RULES_DIR}}/Rules-of-Rules.md`](../{{RULES_DIR}}/Rules-of-Rules.md):
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
2. That definition must satisfy `Rules-of-Rules.md` §1 (conflict check)
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

- **This is a hard requirement.** Bugs, requirements, house-keeping items, and
  meta-tags must each be stored as their own individual markdown file in the
  corresponding folder, not only as free-form notes or grouped content.
- **This is also a hard requirement.** Every item must be listed in the
  corresponding type index file so the repository has an authoritative catalog
  of the concrete documents that exist.
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
  `Rules-of-Rules.md` §6) inline in the requirement doc so rule and
  requirement are reviewed together.
- **House-keeping**: dev-support tooling/process, not product behavior.
  Still targets a rule where one exists — most commonly a `rr-META-*`
  process rule.
- **Meta-tag**: a lightweight annotation attached to an existing artifact.
  It stores one key/value pair whose key is one of `comment`, `version`, or
  `link-to`, and it is saved under the name `tag-<key>-<artefact-id>`.

## 3. Slash-command entry points

The framework exposes the following custom slash commands:

- `/create-bug` — create a new bug artifact immediately, register it in
  `bugs/bugs.md`, and track it in the same workflow as any other bug.
- `/create-req` or `/create-requirement` — create a new requirement artifact
  immediately, register it in `requirements/requirements.md`, and track it in
  the same workflow.
- `/create-epic` — create a new epic work item and register it in
  `epics/epics.md`.
- `/create-story` — create a new story work item and register it in
  `stories/stories.md`.
- `/create-task` — create a new task work item and register it in
  `tasks/tasks.md`.
- `/create-spike` — create a new spike work item and register it in
  `spikes/spikes.md`.
- `/create-sprint` — create a new sprint container and register it in
  `sprints/sprints.md`.
- `/meta-tag` — create a new meta-tag artifact, save it as
  `tag-<key>-<artefact-id>`, register it in `meta-tags/meta-tags.md`, and
  link it to the specified artifact.
- `/list <type> [--filter ...]` — list artifacts, work items, rules, or
  templates of the requested type. Use `all` to list everything. Each
  `--filter` is a property filter expressed as `key=value` or
  `key="value*"`; filters apply across the selected collection. If the
  requested type is `template`, the command requires an additional
  `--type <template-type>` argument to identify which template family to
  inspect.
- `/freeze <item-id|item-path|type|template-name>` — protect the resolved
  item from `/sync-framework` by recording its file path in a root-level
  `.frozen` file. The command accepts one of four argument forms: an item
  ID, an item path, a type, or a template name.
- `/catalyzer <subcommand>` — manage plugin installation and activation through
  the framework interface. Every subcommand resolves plugins against the
  registry file `plugins/<type>/catalog.md` (currently only
  `plugins/repository/catalog.md`, since the repository type is the only
  plugin type defined at this time), which is the sole source of truth for
  which plugins are registered, their git repository URL, the release/tag
  that ships with the current catalyst release, and their framework-version
  compatibility. Each catalog entry has a `Compatibility` field: a bare `*`
  means the plugin is compatible with every framework version — the default
  for a registered plugin, and never grounds for `/sync-framework` to
  deactivate it. A future convention allows specific version constraints in
  that field instead, expressed with the same range syntax used in a
  dependency lock file, to mark a plugin as excluded from named framework
  versions. Supported subcommands:
  - `list` — list all available plugins by type, read from each type's
    `catalog.md`, including each plugin's repository URL, pinned
    release/tag, and compatibility.
  - `activate <name> <version|latest>` — download or update the plugin to the
    specified version (or `latest`) and activate it. This command requires a
    version argument.
  - `download <name> <version|latest>` — download the plugin into the
    framework without activating it. The plugin remains installed and inactive
    until it is explicitly activated.
  - `deactivate <name>` — deactivate a plugin by its registered name, remove
    it from memory, and mark it inactive.
  - `upgrade <name|latest>` — upgrade an already installed plugin to a
    specified version or to the latest available version.
  - `downgrade <name> <version>` — downgrade an already installed plugin to
    the specified version.
  Plugins are not loaded into memory unless they are explicitly activated via
  this command, and on framework startup the framework must scan the installed
  plugin list and activate only those marked active. This is a hard rule.
  The framework defines the interface and lifecycle contract; the plugin itself
  owns its implementation details, operational guidance, and domain-specific
  behavior. Each plugin must live in its own repository, with no exceptions,
  and during framework deployment or synchronization plugins must be pulled
  directly from that plugin repository rather than from this repository.
- `/status` — update an artifact or work item's `Status` field.
- `/audit <file-name>` — analyze the change-impact of the specified file by
  checking the current repository state, the file's role in the framework,
  and the rules or artifacts that depend on it, then return a concise impact
  summary.
- `/run-analysis` — open and execute the analysis playbook from
  `ANALYSIS-PLAYBOOK.md` in the project root, following its steps and
  returning the resulting analysis summary.
- `/sync-framework [latest|<version>]` — synchronize the deployed framework
  with the requested framework version. If the argument is `latest`, use the
  newest framework version available from the framework source. If no argument
  is provided, synchronize against the currently installed local version.
- `/check-rules` — verify that rules, domains, and artifact links remain
  consistent and do not conflict.
- `/show-backlog` — summarize open work, blockers, and missing links.
- `/help` — return help documentation for the framework or for a specific
  command when provided.

When the user enters `/create-bug: ...`, create a new bug artifact immediately,
register it in `bugs/bugs.md`, and track it in the same workflow as any other
bug. If the domain cannot be inferred from context, prompt for the domain and
rule before creating the artifact.

When the user enters `/create-req:` or `/create-requirement: ...`, create a
new requirement artifact immediately, register it in
`requirements/requirements.md`, and track it in the same workflow. If the
domain or target rule cannot be inferred, prompt for both before creating the
artifact.

When the user enters `/create-epic`, `/create-story`, `/create-task`,
`/create-spike`, or `/create-sprint`, create the corresponding work-item
artifact immediately, register it in the matching index file under the
appropriate work-items folder, and preserve the required linkage to its parent
or target artifact.

When the user enters `/meta-tag <artefact-id>`, create a new meta-tag artifact
immediately, save it as `tag-<key>-<artefact-id>`, register it in
`meta-tags/meta-tags.md`, and link it to the specified artifact. If the key
is not supplied explicitly, prompt for it.

When the user enters `/list <type> [--filter ...]`, inspect the relevant
catalogs and return the matching items. If `type` is `all`, inspect every
supported collection and apply the same filters there. If `type` is
`template`, require `--type <template-type>` and list the matching templates
for that family. If no items match, return an empty result rather than
inventing matches.

When the user enters `/freeze <item-id|item-path|type|template-name>`, resolve
the item to its backing file path, append that path to the root-level
`.frozen` file if it is not already present, and report success. The item is
then protected from automatic framework synchronization until it is
explicitly removed from `.frozen` or re-synchronized with an override.

Every `/catalyzer` subcommand resolves plugin identity, repository URL, and
version information exclusively from the `catalog.md` registry of the
relevant plugin type (e.g. `plugins/repository/catalog.md`); a plugin
name with no matching entry in the registry is unregistered, and any
subcommand invoked against it must be refused with a message that the plugin
is not registered. When the user enters `/catalyzer list`, read every plugin
type's `catalog.md` and return the available plugins grouped by type,
each with its registered repository URL, pinned release/tag, and
compatibility. When the user
enters `/catalyzer activate <name> <version|latest>`, look up `<name>` in the
registry to resolve its repository URL, then download or update the plugin
into the framework at `plugins/<type>/` from that repository if it is not
already present, then load it into memory: read that plugin's own
`working-contract.md` and fulfill its Operational-loop section — starting
whatever persistent sub-agent or process it describes — always targeting
the deployed project's own repository root (the project this activation is
happening within), never the catalyst framework's own repository or the
plugin's installation directory. The command requires a version
argument; if the user supplies `latest`, resolve the newest available version
for that plugin from its repository rather than from the pinned tag in the
registry. If a plugin with the same name is already loaded, replace it in
memory with the new instance. When the user enters
`/catalyzer download <name> <version|latest>`, resolve `<name>` against the
registry the same way, then download the plugin into the framework without
activating it; the installed plugin remains inactive until it is explicitly
activated later. A plugin is considered invalid for activation unless its root
directory contains both a `README.md` file and a `working-contract.md` file;
if either file is missing, refuse activation and report the missing
requirement. When the user enters `/catalyzer deactivate <name>`, leave the
plugin installed in the framework but mark it inactive and flush it from
memory. When the user enters `/catalyzer upgrade <name|latest>`, resolve the
plugin's repository URL from the registry, then update the plugin to the
requested version or to the latest available version from that repository.
When the user enters `/catalyzer downgrade <name> <version>`, resolve the
plugin's repository URL from the registry, then downgrade the plugin to the
specified version. Plugins must remain inactive until they are explicitly
activated, and only the repository plugin type exists at this time. On
framework startup, the framework must scan the installed plugins and activate
each one whose `active` metadata flag is true the same way `/catalyzer
activate` loads a plugin into memory (see above). This is a hard rule.

When the user enters `/status <artefact-id> <status> [force]`, update the
artifact's `Status` field. If the supplied status is one of the valid statuses
for that artifact type, change it normally. If the status is invalid and the
command includes the word `force`, change it to that invalid value anyway. If
the status is invalid and `force` is not supplied, respond that the status
change is impossible and do not modify the artifact. If the artifact ID does
not resolve to an existing artifact, state that the artifact cannot be found.

Each plugin must be defined by the following minimum metadata fields: `name`,
`description`, `uuid`, `version`, `active`, and `type`. The plugin definition
template must be updated to include these fields and to record the plugin's
current state in the framework. The framework must read the plugin's
`active` flag at startup and activate only the plugins marked active; this is
mandatory and must not be bypassed. All plugin-specific functionality,
operational guidance, and implementation details must live inside the plugin
package itself; the framework only defines the interface and lifecycle contract.

When the user enters `/audit <file-name>`, inspect the repository and the
current framework state to determine the impact of changes against the named
file. The command must identify whether the file is a rule, template,
artifact, plugin contract, or other framework asset; inspect related indexes,
references, and dependent artifacts; and return a concise summary of likely
impact, affected areas, and any blocking concerns. If the file cannot be
resolved, report that it was not found and do not invent a result.

When the user enters `/run-analysis`, open and execute the analysis playbook
from `ANALYSIS-PLAYBOOK.md` in the project root, following its steps and
returning the resulting analysis summary. If the playbook is missing, report
that it is unavailable and do not invent missing content.

When the user enters `/sync-framework [latest|<version>] [--force <scope>]`,
inspect the requested framework version, compare it with the deployed
framework, and synchronize any missing or outdated files and version
information. If the first argument is `latest`, resolve the newest available
framework version from the framework source. If no version argument is
provided, synchronize against the currently installed local version. Before
synchronizing an item, check the root-level `.frozen` file. If the item's
path is listed there, skip it unless the command includes one of the valid
overrides: `--force <type>`, `--force <item-id>`, or `--force all`. When an
item is refreshed during the synchronization process, it must not remain in
`.frozen`; remove it from the list so the refreshed version no longer carries
the frozen protection. Synchronization must never deactivate an
already-active plugin as a side effect of a framework version change: a
plugin stays active across the sync unless its entry in the relevant
`plugins/<type>/catalog.md` explicitly excludes the target framework
version via the `Compatibility` field — a bare `*`, or an absent field, is
never grounds for deactivation. Only when that field names a version or
range that excludes the target version may the synchronization process
deactivate the plugin, and it must then report which plugin was deactivated
and why. Synchronization must also never treat a deployed project's
`plugins/<type>/catalog.md` or any installed plugin directory under
`plugins/<type>/<name>/` as framework template content to overwrite
wholesale: once a project has registered or activated any plugin, that
catalog and those directories are project-owned state, so synchronization
may only merge into `catalog.md` — adding rows for newly available plugins
not yet present, and refreshing the pinned `Release`/`Tag`/`Compatibility`
columns of a row that already exists — and must never delete an existing
row, blank the file, or delete or replace an installed plugin's directory
contents. A missing row or directory is something the user resolves
afterward via `/catalyzer activate` or `/catalyzer download`, never
something `/sync-framework` performs or silently corrects on its own. After
the refresh completes, perform a four-eyes
verification pass: one sub-agent verifies the newly deployed framework against
`INSTANTIATION-GUIDE.md` and the framework rules, and a second independent
sub-agent repeats the verification from a separate pass. The sync is not
complete until both sub-agents approve the deployment; any disagreement or
failed validation becomes a blocking issue.

When the user enters `/check-rules`, inspect the deployed framework for
missing rule targets, conflicting domains, missing indexes, and broken links,
then report the result.

When the user enters `/show-backlog`, inspect the current backlog documents and
artifact indexes, then summarize the relevant open work and blockers.

When the user enters `/help` without any additional entry, list all supported
custom slash commands and their purpose, then list every artifact type and its
purpose in a compact reference format. When the user enters `/help <command>`,
return the detailed help documentation for that command only, including its
syntax, behavior, and prerequisites. If the command is unknown, respond that
it is unsupported and suggest the available commands.

## 4. Domain field

Every item's `Domain` field is the `DOMAIN` code of the rule(s) it targets,
from `{{RULES_DIR}}/domains/` — not free text.

## 5. Development-artifact IDs

Per `Rules-of-Rules.md` §5: `(BUG|REQ|HK)-(NNNN)`, global per type,
sequential, zero-padded 4 digits, never reused. Meta-tags use a file-name
pattern of `tag-<key>-<artefact-id>` rather than a sequential numeric ID.
This is a hard requirement for all new artifacts and work items: every item
name must be more than the bare ID and must follow the format
**`<artifact-id>-<short-summary>`**. The corresponding markdown filename must
also follow the same descriptive pattern as
**`<artifact-id>-<short-summary>.md`**, not simply `<artifact-id>.md`.
Example: `BUG-0001-login-form-validation` or
`BUG-0001-login-form-validation.md`, and `REQ-0002-password-reset-flow` or
`REQ-0002-password-reset-flow.md`. The same rule must be applied
retroactively during framework deployment or synchronization to existing
deployed items whose names or filenames are still only the ID.

## 6. Closing an item

Before closing a bug or requirement, ensure the corresponding entry exists in
its individual file and is reflected in the relevant index file.

- **Bug**: not closeable as "fixed" without its test-plan item landing.
- **Requirement**: not closeable as "done" until the acceptance criteria and
  rule targets are reflected in the implementation and tests.
- **House-keeping**: closeable once its stated verification passes.

## 7. Retired rules and development work
