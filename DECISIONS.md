# 设计决策

本文记录项目的关键设计决策。每条决策标注日期和状态。

详细决策记录见 `docs/adr/`：

- [ADR 0001](docs/adr/0001-store-field-data-as-hdf5-artifacts.md) — HDF5 格式存储气动场数据 artifact
- [ADR 0002](docs/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md) — 三维机翼结构几何生成为 STEP artifact
- [ADR 0003](docs/adr/0003-factory-pattern-for-models-and-optimization.md) — `models/` 和 `optimization/` 采用工厂模式
- [ADR 0004](docs/adr/0004-harness-project-internal-documentation-system.md) — Harness 架构：项目内文档系统
- [ADR 0005](docs/adr/0005-multi-agent-parallelization-task-model.md) — 多 Agent 并行化任务模型预留
- [ADR 0006](docs/adr/0006-code-structure-constraints-and-enforcement.md) — 代码结构约束与自动化执行

当实现需要偏离既有规则时，先在这里补充决策，再修改代码或任务。
