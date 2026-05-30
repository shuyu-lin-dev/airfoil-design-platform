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

### 2026-05-30 — 任务激活时 PROGRESS.md 更新范围补全

**决策**：原规则只提到更新「当前 active 功能项」和「当前状态」，但遗漏了「进行中」。T002 激活时因未更新「进行中」导致该字段仍显示"无"，与 active 状态不一致。规则已补全为三个位置。

**原因**：这三个字段各自独立对观测者有意义，缺一个就会造成信息不一致。

**影响**：`agent-workflow.md` 对应条目已更新。

### 2026-05-30 — Bash 权限规则前缀匹配失效问题

**决策**：项目 `.claude/settings.json` 中的 Bash 权限规则采用前缀匹配。当 agent 执行的命令含 `cd backend &&` 前缀时，无法命中以 `source .venv/bin/activate &&` 起手的规则。解决方式：(1) 利用 CWD 持久性，先 `cd` 到 `backend/`，后续命令直接从 `source .venv/bin/activate &&` 起手；(2) 补 `cd backend &&` 前缀的规则作为兜底。

**原因**：`cd backend && source .venv/bin/activate && pytest --tb=short 2>&1` 无法匹配 `Bash(source .venv/bin/activate && pytest *)`，因为规则从命令首字符开始做前缀匹配，`cd` 破坏了前缀。每次执行都要人批权限。

**影响**：`.claude/settings.json` 已补 `cd backend && source .venv/bin/activate && *` 系列规则。agent 工作流规则中增加约定——后端测试/启动命令统一先 `cd backend` 改变 CWD，再执行无需 cd 前缀的命令。
