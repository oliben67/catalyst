# Framework rules

Retrofitted from `development-framework/INVARIANTS.md` (the canonical
invariants list) against the actual enforcement in `scripts/check_deployment.py`,
`scripts/check_plugins.py`, and `scripts/check_plugin_contracts.py`, per
`Rules-of-Rules.md` §2's gathered/implemented/tested/documented bar. Each
rule's status marker reflects that bar honestly — several invariants are
**behavioural** (agent conduct during a session) rather than structural
(verifiable from a tree snapshot), and are marked ⚠️ rather than ✅ for
that reason, per `scripts/check_deployment.py`'s own documented scope
note.

## Contents

- [`BEHAVIOR`](#behavioural-invariants) — `fw-BEHAVIOR-001`..`004`
- [`STRUCTURE`](#structural-invariants) — `fw-STRUCTURE-001`..`008`
- [`PLUGINS`](#plugin-system-invariants) — `fw-PLUGINS-001`..`004`

## Behavioural invariants

> **Domain:** `BEHAVIOR` — see [domains/fw-BEHAVIOR-agent-conduct.md](../../domains/fw-BEHAVIOR-agent-conduct.md).

### `fw-BEHAVIOR-001` Repo-scoped references

✅ working. When referring to catalyst, never mention a local drive,
folder, or path — only the git repository and repository name.
`development-framework/INVARIANTS.md:15`. ⚠️ Behavioural: agent-followed,
not machine-tested — no automated check can verify what an agent said in
a conversation.

### `fw-BEHAVIOR-002` Install on first load

⚠️ buggy/incomplete. The first time catalyst is loaded into memory for a
project, it must be installed immediately via the instantiation
procedure. `development-framework/INVARIANTS.md:17`,
`development-framework/BOOTSTRAP.md` §0. Behavioural, not machine-tested.
(Marked ⚠️ rather than ✅ per `rr-META-002`'s honest-status bar: this
project's own repo went a long time without this deployment existing —
this very deployment is the first real instance of the rule actually
being followed for catalyst's own repo.)

### `fw-BEHAVIOR-003` Name it "catalyst"

⚠️ buggy/incomplete. After first install, always refer to the framework
as "catalyst" or "catalyst framework" in guidance, memory, and
discussion. `development-framework/INVARIANTS.md:19`. Behavioural, not
machine-tested.

### `fw-BEHAVIOR-004` Assent before push

⚠️ buggy/incomplete. Never push anything (project or catalyst) without
the user's explicit assent; no target-repo commit without assent.
`development-framework/INVARIANTS.md:21`. Behavioural, not
machine-tested — followed by session discipline (this deployment itself
has not been committed or pushed), not verified by a script.

## Structural invariants

> **Domain:** `STRUCTURE` — see [domains/fw-STRUCTURE-deployed-tree-shape.md](../../domains/fw-STRUCTURE-deployed-tree-shape.md).

### `fw-STRUCTURE-001` Chain invariant

⚠️ buggy/incomplete. No work without a traceable link down to a
documented rule: epic → story → task → REQ/BUG/HK → rule → domain. Every
document, domain, and rule has a stable, permanent, never-reused ID.
`development-framework/INVARIANTS.md:26`. Partially machine-checked:
naming (`fw-STRUCTURE-003`) and indexing (`fw-STRUCTURE-004`) pieces are
verified by `scripts/check_deployment.py:47` (`check_naming`) and `:87`
(`check_rule_indexing`), tested in `tests/test_check_deployment.py`. The
full end-to-end chain (a story actually links to a real REQ/BUG that
targets a real rule) is not verified by any single check — ⚠️ until it
is.

### `fw-STRUCTURE-002` Fixed deploy dir

✅ working. The deployment directory is `.catalyst-proj/`, no exception.
`development-framework/INVARIANTS.md:29`. Implemented:
`scripts/check_deployment.py:21` (`DEPLOY_DIRNAME`), `:38-43`
(`find_deploy_root`, only ever looks for `.catalyst-proj`). Tested:
`tests/test_check_deployment.py::test_find_deploy_root_locates_from_nested_dir`,
`::test_find_deploy_root_returns_none_when_absent`.

### `fw-STRUCTURE-003` Descriptive naming

✅ working. Every rule, dev-artifact, and domain file is
`<id>-<short-summary>.md`; bare-ID filenames are invalid.
`development-framework/INVARIANTS.md:31`. Implemented:
`scripts/check_deployment.py:47` (`check_naming`), `NAME_RE`/`BARE_ID_RE`
at `:23-27`. Tested:
`tests/test_check_deployment.py::test_check_naming_rejects_bare_id_filename`
and siblings.

### `fw-STRUCTURE-004` No orphan rules

✅ working. Every rule lives in its type directory, appears in its local
type index, and appears in the global `rules.md`; exactly one
`TEMPLATE-RULE.md`, in the `rules/` root.
`development-framework/INVARIANTS.md:34`. Implemented:
`scripts/check_deployment.py:71` (`check_single_rule_template`), `:87`
(`check_rule_indexing`), `:105` (`check_required_headings`). Tested:
`tests/test_check_deployment.py` (`test_check_single_rule_template_*`,
`test_check_rule_indexing_*`, `test_check_required_headings_*`).

### `fw-STRUCTURE-005` Requirements, not bugs, for new work

⚠️ buggy/incomplete. `FEAT-` entries are non-rule-linked roadmap. When
work on one starts it becomes a `REQ-` (never a `BUG-`), which is vetted
against every rule, assigned a domain, and measured.
`development-framework/INVARIANTS.md:37`. Behavioural — no script
verifies that a promoted `FEAT-`/`RM-` item became a `REQ-` rather than a
`BUG-`.

### `fw-STRUCTURE-006` Persisted backlog

✅ working. `development/BACKLOG.md` always exists, seeded from
`templates/backlog.template.md`; never hand-edited — `/show-backlog`
overwrites it in full every run. `development-framework/INVARIANTS.md:40`.
Implemented: `scripts/check_deployment.py:122` (`check_backlog_exists`).
Tested: `tests/test_check_deployment.py::test_check_backlog_exists_missing`
and sibling.

### `fw-STRUCTURE-007` Machine-maintained roadmap tracking

✅ working. `development/roadmaps/` and its `roadmaps.md` index always
exist (empty is fine); individual named roadmaps created only via
`/roadmap-add`; Status/Linked columns machine-maintained.
`development-framework/INVARIANTS.md:44`. Implemented:
`scripts/check_deployment.py:131` (`check_roadmaps_index_exists`); the
naming-check exemption for `development/roadmaps/<name>.md` files (free-form
names, not `<id>-<summary>`) at `:59-63`. Tested:
`tests/test_check_deployment.py::test_check_roadmaps_index_exists_missing`
and `::test_check_naming_ignores_named_roadmap_files` (regression test for
a real bug caught during this rule's own retrofit: a name like
`product-2026.md` was initially misflagged as a bare numeric ID by
`fw-STRUCTURE-003`'s `BARE_ID_RE`).

### `fw-STRUCTURE-008` At least one active user; advisory role signing

✅ working. `development/users.json` and `development/roles.json` always
exist, and `users.json` must contain at least one entry with `"active":
true`. `development-framework/INVARIANTS.md:51`. Implemented:
`scripts/check_deployment.py:140` (`check_users_and_roles_exist`) —
parses `users.json` and fails the deployment if no entry has
`"active": true`, not just checking file existence. Tested:
`tests/test_check_deployment.py::test_check_users_and_roles_exist_no_active_user`,
`::test_check_users_and_roles_exist_empty_users_array`,
`::test_check_users_and_roles_exist_invalid_json`, and siblings. This
project's own `development/users.json` satisfies it: at least one
`"active": true` entry as of this deployment.

## Plugin system invariants

> **Domain:** `PLUGINS` — see [domains/fw-PLUGINS-lifecycle-and-provenance.md](../../domains/fw-PLUGINS-lifecycle-and-provenance.md).

### `fw-PLUGINS-001` Activation gate

⚠️ buggy/incomplete. A plugin is not loaded unless activated via
`/catalyzer`, and only if it carries `README.md` + `working-contract.md`.
`development-framework/INVARIANTS.md:64`. Partially implemented:
`scripts/check_plugins.py:32` (`validate_plugin_structure`) verifies the
README/working-contract presence precondition. The activation-gating
behavior itself (nothing loads into memory without an explicit
`/catalyzer activate`) is behavioural, not machine-checked from a tree
snapshot — ⚠️ for that half.

### `fw-PLUGINS-002` Plugin provenance

✅ working. Every plugin has its own repository; no plugin is sourced
from the framework repository. `development-framework/INVARIANTS.md:66`.
Implemented: `scripts/check_plugins.py:53` (`validate_submodule_policy`),
`:78` (`validate_plugin_sources`, via `:63` `parse_submodule_status`)
verify the submodule is actually checked out; `scripts/check_plugin_contracts.py:95`
(`origin_url`)/`:86` (`normalize_url`) compare a plugin's declared origin
against the framework's own, done defensively so a missing origin never
false-fails. Tested: `tests/test_check_plugins.py` (`test_validate_submodule_policy_*`,
`test_parse_submodule_status_*`, `test_validate_plugin_sources_*`) and
`tests/test_check_plugin_contracts.py::test_normalize_url_variants_are_equal`
(this test caught a real bug: `.git`-suffix stripping was case-sensitive,
so a `.GIT`-suffixed URL wasn't recognized as the same repo — fixed
alongside this rule's own retrofit).

### `fw-PLUGINS-003` Contract is canonical + stable

✅ working. Every plugin's `working-contract.md` carries the six metadata
fields (Name, Description, UUID, Version, Active, Type); UUID generated
once, never changes; Version matches the plugin's own `version.txt` and
its catalog pin. `development-framework/INVARIANTS.md:68`. Implemented:
`scripts/check_plugin_contracts.py:121` (`validate_plugin`). Tested:
`tests/test_check_plugin_contracts.py` — 14 tests covering missing
fields, leftover placeholders, malformed UUIDs, `Active` not
`true`/`false`, `Version`/`version.txt`/catalog mismatches.

### `fw-PLUGINS-004` Operate on the deployment, not on catalyst

⚠️ buggy/incomplete. A plugin's runtime target (monitoring, auditing,
mutation) is the *deployed project's* repository, resolved at activation
time — never catalyst's own repository and never the plugin's own
installation directory under `plugins/<type>/<name>/`.
`development-framework/INVARIANTS.md:73`. Behavioural, not
machine-checked from a tree snapshot — no plugin is currently activated
in this deployment to verify this against.

## Known Bugs — Quick Index

*(none yet — this is a fresh retrofit, not an audit of a running system)*
