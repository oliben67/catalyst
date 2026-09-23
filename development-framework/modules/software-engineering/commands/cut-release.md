---
description: Cut a release for the catalyst repo, or for one of its plugin submodules, entirely via gh
argument-hint: "[submodule <name>]"
---

Command for cutting releases in catalyst-governed repositories.

## Determine the target repo

- No arguments (`$ARGUMENTS` empty): the target is the catalyst repo itself,
  root at the current project directory. Its version file is `version.txt`.
- `submodule <name>`: the target is the plugin repo checked out at
  `plugins/repository/<name>/`.

## Steps

1. **Fix any branch drift first:** Ensure checkout is on `development`.
2. **Handle uncommitted changes:** Ask user how to proceed if dirty.
3. **Ask about the version bump:** Prompt user for patch/minor/no-bump.
4. **Push development:** `git push origin development`.
5. **development -> main:** Create and merge PR via `gh`.
6. **main -> release:** Create and merge PR via `gh`.
7. **Tag the release:** `gh release create <version> --target release`.
8. Report status.
