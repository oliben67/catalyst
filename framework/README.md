# framework/

The catalyst framework has two parts:

| Folder | What it is | Versioned by |
|---|---|---|
| [`kernel/`](kernel/README.md) | The **kernel**: everything independent of process modules — invariants, rules-of-rules and development templates, instantiation and synchronization guides, entity definitions, schemas, templates, migrations, and plugins. | The repository's root [`version.txt`](../version.txt) |
| [`modules/`](modules/) | In-repo sample process modules (`sample-process`). Production modules live in their own `catalyst-<module-id>` repositories, checked out next to catalyst (e.g. `catalyst-software-engineering`), never as submodules. | Each module's own `version.txt` |

See [`kernel/MODULE-SPECIFICATION.md`](kernel/MODULE-SPECIFICATION.md) for
how a module plugs into the kernel.
