# Roadmap: Modularization & Separation of Software Engineering

**Status:** Draft / Proposed  
**Target Framework:** Catalyst (`development-framework/`)  
**Objective:** Decouple all Software Engineering-specific concepts (entity types, templates, slash commands, agent skills, validators, and rule invariants) into a standalone, pluggable module (`software-engineering`). Upon completion of this roadmap, Catalyst's kernel will be fully process-agnostic, and all existing software engineering workflows will function with **100% feature parity and identical behavior**.

---

## Key Invariants for this Roadmap

1. **Zero Downtime / Zero Regression:** Every existing command (`/create-req`, `/create-bug`, `/check-rules`, `/cut-release`, etc.) and artifact type (`BUG`, `REQ`, `HK`, `TEST`, `STEP`, `FEAT`, `RM`, `WORKFLOW`, `RECON`) must function identically before and after module separation.
2. **Explicit Fallbacks:** Until cutover is complete, the kernel maintains legacy fallback paths to ensure uninterrupted dogfooding and synchronization.
3. **Equal Citizen:** The `software-engineering` module is authored using the exact same public Module Spec & ETD mechanism available to any future non-software domain module (e.g., Scrum, ITIL, Legal, Product Management).

---

## Phase 1: Module Specification & Architecture Design

### 1.1 Module Manifest Schema (`module.yaml`)
Define the structure for a Catalyst Module:
- `id`: Unique module identifier (e.g., `software-engineering`).
- `name` & `version`: Human-readable name and semver.
- `grounding_type`: Default grounding artifact (e.g., `rule`).
- `entity_types`: List of ETD schema references (`BUG`, `REQ`, `HK`, `TEST`, etc.).
- `commands`: List of slash command registrations and prompt mappings.
- `skills`: Agent skill definitions exported by the module.
- `templates`: Document templates for human-facing markdown generation.

### 1.2 Module Directory Layout Specification
Define canonical folder structure within Catalyst framework & project deployments:
```
modules/
└── software-engineering/
    ├── module.yaml
    ├── schemas/              # Entity Type Definitions (ETDs)
    │   ├── bug.yaml
    │   ├── requirement.yaml
    │   ├── test.yaml
    │   └── ...
    ├── templates/            # Markdown document templates
    ├── commands/             # Slash command prompt specs (.md)
    └── skills/               # Agent skill definitions
```

---

## Phase 2: Kernel Decoupling & Dynamic Engine Initialization

### 2.1 Generalized Invariants (Kernel Layer)
- Generalize `INV-5` ("no work without a link to a documented rule") to evaluate `grounding_type` from the active module manifest rather than hardcoding `rule`.
- Generalize `INV-20` (uniform artifact layout) and ID validation to rely on active ETDs.

### 2.2 Module Loader & Registry Engine
- Implement a lightweight Module Loader in `catalyst-core` (TypeScript) and `scripts/` (Python):
  - Load active module declared in project pointer (`*.catalyst` or `.criterion/config.yaml`).
  - Register ETD schemas, relationships, backreferences, and commands dynamically in memory.
  - Expose query functions: `getActiveETDs()`, `getGroundingType()`, `resolveCommand(name)`.

---

## Phase 3: Extraction of Software Engineering Artifacts & Prompts

### 3.1 ETD Schema Extraction
Convert hardcoded prose definitions of all 9 software engineering entities into machine-readable ETDs (`.yaml`):
- `BUG` (Bug report schema, severity, reproduction steps, target rules).
- `REQ` (Requirement schema, status, targets, feature links, test plan).
- `HK` (House-keeping item schema).
- `TEST` (Test case schema, target requirements/bugs, execution criteria).
- `STEP` (Step schema, parent requirement/bug).
- `FEAT` (Feature schema, requirement links).
- `RM` (Risk Management schema).
- `WORKFLOW` (Workflow specification schema).
- `RECON` (Reconciliation item schema).

### 3.2 Prompts & Commands Extraction
Move software development slash commands and skills out of core framework templates into `modules/software-engineering/`:
- Slash commands: `/create-req`, `/create-bug`, `/create-test`, `/create-feature`, `/create-step`, `/check-rules`, `/show-backlog`, `/cut-release`.
- Prompt templates and agent instructions.

### 3.3 Default Bundling
Package `modules/software-engineering/` inside the Catalyst framework repository as the default bundled module.

---

## Phase 4: Validation Engine & Harness Integration

### 4.1 Script & Validator Generalization
- Update `scripts/check_deployment.py` to inspect `module.yaml` + ETDs instead of reading static `ENTITY_TYPES` tuples.
- Update `scripts/check_command_parity.py` to compare active module command registrations against Taskfiles and `.claude/commands/`.
- Generalize TypeScript validators in `catalyst-core` (`validator.ts`, `parser.ts`) to operate on dynamic ETDs.

### 4.2 Taskfile Generator & Command Router
- Update `Taskfile.common.template.yml` to route slash commands dynamically through the active module command registry.

---

## Phase 5: Verification, Testing & Parity Audit

### 5.1 Automated Test Parity
- Run full test suite (`pytest tests/`, `vitest` in `catalyst-ui`) against module-backed project setups.
- Verify byte-for-byte output identity for generated templates and command dispatches.

### 5.2 Four-Eyes Regression Audit against Dogfood Deployment (`.criterion`)
- Execute comprehensive dogfooding check across all 9 entity types and slash commands.
- Verify existing artifacts (`REQ-0001..`, `BUG-0001..`, etc.) maintain exact parsing, validation, back-reference linking, and journal history integrity.

### 5.3 Non-Software Engineering Module Validation (Proof of Isolation)
- Create a minimal sample non-software module (e.g., `modules/sample-process/`) with custom ETDs (e.g., `POLICY`, `TASK`) to confirm the kernel loads, validates, and runs a completely different domain without any software engineering assumptions.

---

## Phase 6: Cutover & Documentation Synchronization

### 6.1 Project Pointer Cutover
- Update `.catalyst` project pointers to explicitly declare `module: software-engineering`.
- Update framework version and migration script (`SYNCHRONIZE.md` & `migrations/`) for upgrading existing deployments seamlessly.

### 6.2 Documentation & Instantiation Synchronization
- Update `INSTANTIATION-GUIDE.md`, `INSTANTIATION-CHECKLIST.md`, `BOOTSTRAP.md`, `CLAUDE.md`, and top-level `README.md` to reflect the kernel + module architecture.
- Mark legacy hardcoded entity prose as deprecated in favor of module specification.
