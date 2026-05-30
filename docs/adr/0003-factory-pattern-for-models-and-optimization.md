# Factory Pattern for Prediction Models and Optimization Algorithms

The backend MVP uses a factory + abstract-interface pattern for swappable prediction models (`models/`) and optimization algorithms (`optimization/`), while deleting the unused `serialization/` directory.

## Decision

1. **Delete `serialization/`** — no corresponding code or foreseeable need for MessagePack/numpy bytes codec.
2. **`models/` as prediction model adapter layer** — abstract base (`base.py`) + factory registry (`factory.py`) + replaceable implementations (`aerodynamics/`, `structure/`). Weight files (`.pt`, `.onnx`) live under `models/weights/` as non-source data.
3. **`optimization/` as optimization algorithm adapter layer** — same pattern: abstract base + factory registry + replaceable algorithms (`algorithms/`).
4. **`core/` depends only on abstract interfaces** — imports from `models/base.py` and `optimization/base.py`, never from concrete implementations. Concrete classes are created via factory from config.

## Why

Prediction models (stub formula → GNN → PINN → transfer model) and optimization algorithms (perturbation → genetic → Bayesian) have **stable input/output contracts** but **replaceable internals** as the project matures. The factory pattern lets `core/` orchestrate without knowing which implementation is active — swap happens by changing config and registering a new implementation.

This is structurally identical to MODULAR-RAG-MCP-SERVER's LLM/Embedding factory pattern, except here we adapt replaceable **domain algorithm implementations** rather than external service providers.

## Alternatives rejected

1. **Keep all three empty directories** — wastes architecture slots and confuses intent.
2. **Put factory inside `core/`** — inflates `core/` from orchestration into a container; violates single responsibility.
3. **Leave prediction code directly in `core/`** — changing models touches `core/`; violates open-closed principle.

## Constraints

- `models/weights/` holds weight files only, not imported by Python.
- Factory uses import-time self-registration (same pattern as MODULAR-RAG-MCP-SERVER's `_register_builtin_providers()`).
- `core/` imports from `models/` and `optimization/` are limited to abstract base classes. Concrete class names never appear in `core/`.
- `serialization/` is removed from the tree, architecture docs, and directory listing.
