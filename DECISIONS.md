# 设计决策

本文记录项目的关键设计决策。每条决策标注日期和状态。

详细决策记录见 `docs/adr/`：

- [ADR 0001](docs/adr/0001-store-field-data-as-hdf5-artifacts.md) — HDF5 格式存储气动场数据 artifact
- [ADR 0002](docs/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md) — 三维机翼结构几何生成为 STEP artifact
- [ADR 0003](docs/adr/0003-factory-pattern-for-models-and-optimization.md) — `models/` 和 `optimization/` 采用工厂模式
- [ADR 0004](docs/adr/0004-harness-project-internal-documentation-system.md) — Harness 架构：项目内文档系统
- [ADR 0005](docs/adr/0005-multi-agent-parallelization-task-model.md) — 多 Agent 并行化任务模型预留
- [ADR 0006](docs/adr/0006-code-structure-constraints-and-enforcement.md) — 代码结构约束与自动化执行

## 补充决策

### 2026-05-30 — 任务激活时同步更新 PROGRESS.md

**决策**：在 `agent-workflow.md` 工作规则中增加约束——任务激活时（status 从 `not_started` 变为 `active`）必须同步更新 `PROGRESS.md` 的「当前 active 功能项」和「当前状态」。

**原因**：T001 执行过程中发现，任务在 `tasks.yaml` 中标记为 `active` 后，`PROGRESS.md` 未同步更新，导致外部观测者无法通过该文件感知当前 WIP。`PROGRESS.md` 是会话启动流程的首要读取文件，其信息必须与 `tasks.yaml` 保持同步。

**影响**：任务生命周期的三个关键节点均需更新 `PROGRESS.md`——激活时、完成时、阻塞时。
