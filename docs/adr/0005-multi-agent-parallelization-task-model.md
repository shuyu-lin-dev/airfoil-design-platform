# ADR 0005: 多 Agent 并行化任务模型预留

> 日期：2026-05-29（原始），2026-05-30（从 DECISIONS.md 提炼为 ADR）
> 状态：accepted

## 背景

项目有意推迟多 Agent（当前 WIP=1），但任务依赖图和路径隔离设计应提前预留并行化接口，避免后续重构时重新分析整个任务图。

## 决策

在 `tasks.yaml` 的 `feature_schema` 中新增 `parallelizable_group` 可选字段：

- 同一 group 内的任务具有相同的 `depends_on` 且 `allowed_paths` 互不相交。
- 可在独立 git worktree 中由不同 agent 并行处理，通过 integration branch 汇合。
- 当前单 agent 模式下忽略此字段；多 agent 场景下按 group 调度。

当前项目已自然形成两个并行窗口：
- **post-t002 组**：T003/T004/T009/T010（T002 完成后，4 个任务路径完全隔离）
- **post-t004 组**：T005/T006/T007（T004 完成后，3 个任务路径完全隔离）

## 原因

- 现有原子化拆分已经满足并行条件——不需要为了并行化重新切分任务。
- 将此信息显式记录在任务契约中，让未来的并行化调度不再需要人工推断。
- worktree 隔离 + 任务分支 + integration branch 是 Wiki 多智能体 Git 协作模式的已验证模式。

## 约束

- `parallelizable_group` 是声明性字段，不改变当前单 agent 执行流程。
- 同一 group 内任务必须满足三个条件：相同依赖集、`allowed_paths` 互不相交、`expected_outputs` 无重叠文件。
- 添加或修改任务时必须维护 group 标记的正确性。

## 否决方案

- 现在就引入多 Agent 并行执行——违反 WIP=1 约束，当前阶段协调成本超收益。
- 不做任何预留，等到需要并行时再分析——增加调度 agent 的推断负担和出错概率。
