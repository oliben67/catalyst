# TEMPLATE-WORKING-CONTRACT

Use this template to define the working contract for a plugin.

## Metadata

Every plugin must carry these six fields — this is the minimum metadata
`rules-of-development.md` requires, and the framework reads the `Active`
field at startup to decide which plugins to load into memory. Generate the
UUID once, when the plugin is first defined, and never change it afterward.

- Name: <plugin-name>
- Description: <one-line description of what the plugin does>
- UUID: <generate a UUID once; never change it afterward>
- Version: <the plugin's current version, matching its own version.txt>
- Active: <true|false — whether the framework should load this plugin into memory at startup>
- Type: <plugin type, e.g. repository>

## Purpose

- Describe the plugin's purpose and the repository capability it provides.

## Scope

- List the functional area(s) this plugin covers.

## Responsibilities

- Describe what the plugin is responsible for.

## Constraints

- Describe any limitations, dependencies, or safety constraints.

## Activation requirements

- State whether the plugin requires explicit activation before use.
