# Agent 工作流规则

本文定义 agent 如何在本仓库内选择任务、限制范围、验证完成和交接状态。

## 任务状态

`tasks/tasks.yaml` 是功能清单和任务状态的事实源。任务状态只能使用：

- `not_started`
- `active`
- `blocked`
- `passing`

## 工作规则

- 默认 WIP=1，一次只激活一个任务。
- 若已有 `active` 任务，继续该任务，不启动新任务。
- 任务只能修改 `allowed_paths` 中列出的路径。
- 每个任务都必须有 `behavior`、`validation.commands`、`status` 和 `evidence`。
- 只有验证命令通过后，任务才能标记为 `passing`。
- 不能凭“看起来完成”或 agent 自我判断标记 `passing`。
- 任务结束必须更新 `tasks/tasks.yaml` 的 `status` 和 `evidence`。
- 任务结束必须更新 `PROGRESS.md` 的当前状态、最近验证、阻塞和下一步。
- 涉及关键设计选择时，更新 `DECISIONS.md`。
- 所有工具输出遵守 `.harness/instruction/rules/io-hygiene.md` 的截断、抽帧和落盘规则。

## 多 Agent 并行化（预留）

当前 WIP=1 约束针对单 agent 会话。`tasks/tasks.yaml` 中的 `parallelizable_group` 字段为多 agent 并行化预留接口——同一 group 内的任务可在独立 worktree 中由不同 agent 并行处理，通过 integration branch 汇合。当前阶段忽略此字段，不启动并行执行。详见 `DECISIONS.md` 对应决策。

## 代码结构约束

- 单文件不超过 200 行。超出时必须拆分为模块内多文件或提取公共逻辑。
- 函数不超过 50 行。超出时提取私有辅助函数。
- 新增第三方依赖（pyproject.toml 新增包）必须先经用户确认。不得在无确认情况下引入新库。
- 这些约束是硬性上限，不是建议。

## 工作状态管理

长任务执行中产生的中间产物、检索结果、长日志和临时笔记应放入 `.harness/state/working/`，不塞进上下文窗口，也不散落在项目根目录。

### 典型 working files

- `plan.md`：当前任务的分步执行计划和当前进度。
- `search-results.md`：代码搜索或文档查阅的原始结果摘要。
- `debug-notes.md`：调试过程中发现的线索和诊断结论。
- `long-output.log`：被 io-hygiene 落盘规则写入的超大命令输出。

### 生命周期

- 任务执行中按需读写 working files。
- 任务 `passing` 后、会话退出前，清理本任务的 working files。将值得保留的发现写入 `PROGRESS.md` 或 `DECISIONS.md`，其余删除。
- `.gitkeep` 保留不动。
- 下一个任务开始时，`.harness/state/working/` 应为空（除 `.gitkeep`）。

## 会话流程

1. 读取 `CONTEXT.md`、`PROGRESS.md`、`DECISIONS.md` 和 `tasks/tasks.yaml`。
2. 确认当前是否已有 `active` 任务。
3. 阅读当前任务的冲刺合同；若缺失，先在 `.harness/state/sprint-contracts/` 创建。
4. 执行任务时遵守 `allowed_paths`、代码结构约束和 `.harness/instruction/rules/io-hygiene.md`。
5. 长任务或复杂任务先写 `.harness/state/working/plan.md` 再动手。
6. 运行任务验证命令。
7. 更新任务证据、进度和必要决策。
8. 清理 `.harness/state/working/` 中本任务的临时文件。
9. 按 `.harness/feedback/session-exit-checklist.md` 做交接。

## 会话交接

### 触发条件

当上下文窗口用量达到约 50% 时，主动触发交接：当前任务若已通过验证则标记 `passing` 并停止；若尚未完成则记录当前进度后停止。不开启新任务，立即执行交接记录并退出。

**说明**：50% 是估算值，agent 无法精确读取上下文百分比，依据对话轮数、文件读取量和剩余响应空间综合判断。长上下文可靠使用区间通常早于窗口耗尽，宁可提前交接，不在窗口后半段丢失未记录的状态。

### 主动压缩保留清单

50% 主动交接或手动 `/compact` 前，最低限度保留：

- 架构决策、规则变更和仍未解决的设计分歧
- 当前任务 ID、状态、完成进度和未完成事项
- 待办事项和下一步执行顺序
- 已运行的验证命令、结果、证据和未运行原因
- 阻塞项、待确认问题和重要假设
- 已修改或新增的主要文件，以及会影响后续工作的未提交状态

### 交接输出

交接记录写入 `.harness/state/runs/YYYY-MM-DD-HHMM-handoff.md`，包含：

- 当前任务 ID、状态和进度（已完成/未完成的具体事项）
- 架构决策、规则变更和仍未解决的设计分歧
- 待办事项和下一步执行顺序
- 已修改或新增的主要文件
- 实际运行的验证命令和结果
- 未运行验证的原因
- 阻塞项、待确认问题和重要假设

同时更新 `PROGRESS.md` 的当前状态、最近验证、阻塞和下一步，确保会话启动流程（读取 PROGRESS.md）能直接定位断点。

### 退出检查

无论普通结束还是 50% 主动交接，均执行 `.harness/feedback/session-exit-checklist.md`。
