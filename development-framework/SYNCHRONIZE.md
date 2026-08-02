# Synchronize Framework With Deployment

This framework must be kept aligned with the deployed project that uses it.
If the deployed framework is missing, outdated, or has an older version than
this framework, synchronize it before continuing with project work.

## Rule

Whenever a project is active, it must check this framework for changes,
load the latest version into memory, and, if any changes are present,
offer to apply them using this synchronization process.

If the deployed framework does not exist, or if its version is missing or
lower than the current framework version, apply this synchronization process
immediately.

## Version rule

- Current framework version: `0.0.1`
- The source of truth for the latest framework version is the `release`
  branch of `git@github.com:oliben67/prompts.git` (or
  `https://github.com/oliben67/prompts.git`).
- The deployed framework must have a `version.txt` file.
- If `version.txt` is missing or contains a version lower than `0.0.1`,
  treat the deployment as out of date and synchronize it.

## Synchronization checklist

1. Check the framework repository on the `release` branch for the latest
   version and changes.
2. Compare the deployed framework files with the latest framework state.
3. Copy any changed templates, rules, guidance, or structure needed by the
   deployed project.
3. Ensure the deployed project contains the required artifacts:
   - `requirements/requirements.md`
   - `requirements/` individual requirement files
   - `bugs/bugs.md`
   - `bugs/` individual bug files
   - `BACKLOG.md`
   - `version.txt`
4. Update the deployed framework's `version.txt` to the latest released
   version once synchronization is complete.

## Expected outcome

After synchronization, the deployed framework should reflect the current
framework's rules, templates, and file structure, and its version should be
at least `0.0.1`.
