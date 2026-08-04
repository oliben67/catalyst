# Plugins

This folder contains optional extension modules for the catalyst workspace.

## Rule

- Plugins are not loaded into memory unless they are explicitly activated through the `/catalyzer` command.
- A plugin may not be activated unless it contains a `README.md` and a `working-contract.md` file in its root directory.
- A plugin contract template is available at [TEMPLATE-WORKING-CONTRACT.md](TEMPLATE-WORKING-CONTRACT.md).
- `/catalyzer list` lists available plugins by type.
- `/catalyzer activate <name>` activates a plugin by its registered name, such as `catalyst-git`.

## Available plugin area

- Global index: [plugins.md](plugins.md)
- Repository plugins: [repository/README.md](repository/README.md)
