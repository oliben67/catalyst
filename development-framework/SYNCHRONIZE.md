# Synchronize Framework With Deployment

This framework must be kept aligned with the deployed project that uses it.
If the deployed framework is missing, outdated, or has an older version than
this framework, synchronize it before continuing with project work.

## Rule

Whenever a project is active, it must check the catalyst framework for
changes, load the latest version into memory, and, if any changes are
present, offer to apply them using this synchronization process.

Synchronization requires exactly one confirmation from the user before it
starts. After that confirmation, all subsequent framework updates for the
files and folders in the deployed framework directory must proceed without
any further authorization from the user. The synchronization process must
apply the changes automatically and repeatedly as needed to keep the
deployed framework aligned.

If the deployed framework does not exist, or if its version is missing or
lower than the current framework version, apply this synchronization process
immediately.

## Version rule

- Current framework version: `0.1.10`
- The source of truth for the latest framework version is the `release`
  branch of `git@github.com:oliben67/catalyst.git` (or
  `https://github.com/oliben67/catalyst.git`).
- The deployed framework must have a `version.txt` file.
- If `version.txt` is missing or contains a version lower than `0.1.10`,
  treat the deployment as out of date and synchronize it.

## Slash-command behavior for `/sync-framework`

When the command `/sync-framework [latest|<version>] [--force <scope>]` is entered:

1. If the first argument is `latest`, inspect the `release` branch and resolve
   the newest available tagged release. If a specific version is supplied,
   inspect the `release` branch for the matching tagged release. If that tag
   exists, load that version into memory and use it as the synchronization
   target.
2. If no version argument is provided, synchronize against the currently
   installed local version rather than looking up a remote release.
3. Build a diff between the currently installed deployment and the target
   framework version before applying changes, and use that diff as the basis
   for the synchronization plan.
4. If the requested version differs from the version currently deployed,
   synchronize the deployment using the already-present deployment state as
   the baseline, preserving any project-local adjustments that are still
   valid.
5. If the requested version is the same as the currently deployed version,
   load that version into memory, discard the old in-memory copy, and perform
   a synchronization against the already-present deployment contents.
6. If a requested version does not exist as a tag, stop and report that the
   requested release is unavailable rather than silently falling back to an
   unrelated version.
7. Before applying any per-item refresh, inspect the project root `.frozen`
   file. If the target item path is listed there, skip it unless the command
   includes `--force <type>`, `--force <item-id>`, or `--force all`.
8. When an item is refreshed successfully, remove its path from `.frozen` so
   the refreshed version is no longer considered frozen.
9. Before the sync is considered complete, normalize the names and markdown
   filenames of any deployed items whose current names are only the bare ID or
   otherwise lack a summary suffix. Rename them to the required format
   **`<id>-<short-summary>`** and their corresponding files to
   **`<id>-<short-summary>.md`** using their existing title/description
   content, then update every index entry, link, and reference that points to
   the old name or old filename. The same normalization is a hard requirement
   for domain files under `domains/`: any file still named only
   `<prefix>-<CODE>.md` (or `<prefix>-<PARENT>.<SUB>.md` for a sub-domain)
   must be renamed to `<prefix>-<CODE>-<short-summary>.md` (or
   `<prefix>-<PARENT>.<SUB>-<short-summary>.md`), using the domain's own
   `Scope` field as the source for the summary, then every reference to the
   old filename updated accordingly.
10. Never deactivate an already-active plugin as a side effect of applying a
    new framework version. A plugin stays active across the sync unless its
    entry in the relevant `plugins/<type>/catalog.md` explicitly excludes
    the target framework version via the `Compatibility` field — a bare `*`,
    or an absent field, is never grounds for deactivation. Only deactivate a
    plugin when that field names a version or range that excludes the
    target version, and report which plugin was deactivated and why.
11. Never treat a deployed project's `plugins/<type>/catalog.md` or any
    installed plugin directory under `plugins/<type>/<name>/` as framework
    template content to overwrite wholesale. Once a project has registered
    or activated any plugin, that catalog and those directories are
    project-owned state, not framework state: synchronization may only
    merge into a `catalog.md` — adding rows for newly available plugins
    not yet present there, and refreshing the pinned `Release`/`Tag`/
    `Compatibility` columns of a row that already exists — and must never
    delete an existing row, blank the file, or delete or replace an
    installed plugin's directory contents as a side effect of the sync.
    If a plugin's row or directory would otherwise be missing, that is a
    `/catalyzer activate`/`download` action for the user to take
    afterward; `/sync-framework` must never perform or silently correct it.
12. At the end of the synchronization run, perform a four-eyes verification
   pass: one sub-agent verifies the deployment against the checklist in
   [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md), and a second
   independent sub-agent repeats the verification from a fresh perspective.
   The sync is not complete until both verifiers approve the deployment. If
   their findings conflict or either verifier reports a violation, stop and
   report the issue rather than treating the sync as complete.

## Synchronization checklist

1. Check the framework repository on the `release` branch for the latest
   version and changes.
2. Ask for exactly one confirmation before beginning the synchronization.
3. Compare the deployed framework files with the latest framework state.
4. Copy any changed templates, rules, guidance, or structure needed by the
   deployed project, including plugin content pulled directly from each
   plugin's own repository when plugin updates are required. No plugin may be
   sourced from this repository; every plugin must have its own repository.
   A deployed project's own `plugins/<type>/catalog.md` and installed plugin
   directories are project-owned state, not framework template content —
   merge into them (see item 11 of the slash-command behavior below), never
   overwrite or delete them wholesale.
5. Ensure the deployed project contains a custom root-level `README.md` that
   describes the deployed framework's structure and the project's artifact
   layout.
6. Ensure the deployed project contains the required artifacts:
   - `requirements/requirements.md`
   - `requirements/` individual requirement files
   - `bugs/bugs.md`
   - `bugs/` individual bug files
   - `house-keeping/house-keeping.md`
   - `meta-tags/meta-tags.md`
   - `BACKLOG.md`
   - `version.txt`
   - the documented slash commands (`/create-bug`, `/create-req`/
     `/create-requirement`, `/meta-tag`, `/status`, and `/help`) must be
     available in the deployed environment after synchronization.
7. Update the deployed framework's `version.txt` to the latest released
   version once synchronization is complete.

## Expected outcome

After synchronization, the deployed framework should reflect the current
framework's rules, templates, and file structure, and its version should be
at least `0.1.10`.
