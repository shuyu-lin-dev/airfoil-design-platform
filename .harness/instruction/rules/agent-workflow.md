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

## 会话流程

1. 读取 `CONTEXT.md`、`PROGRESS.md`、`DECISIONS.md` 和 `tasks/tasks.yaml`。
2. 确认当前是否已有 `active` 任务。
3. 阅读当前任务的冲刺合同；若缺失，先在 `.harness/state/sprint-contracts/` 创建。
4. 执行任务时遵守 `allowed_paths`。
5. 运行任务验证命令。
6. 更新任务证据、进度和必要决策。
7. 按 `.harness/feedback/session-exit-checklist.md` 做交接。

## 会话交接

### 触发条件

当上下文窗口用量达到约 60% 时，主动触发交接：当前任务若已通过验证则标记 `passing` 并停止；若尚未完成则记录当前进度后停止。不开启新任务，立即执行交接记录并退出。

**说明**：60% 是估算值，agent 无法精确读取上下文百分比，依据对话轮数、文件读取量和剩余响应空间综合判断。宁可提前交接，不在窗口耗尽时丢失未记录的状态。

### 交接输出

交接记录写入 `.harness/state/runs/YYYY-MM-DD-HHMM-handoff.md`，包含：

- 当前任务 ID、状态和进度（已完成/未完成的具体事项）
- 已修改或新增的主要文件
- 实际运行的验证命令和结果
- 未运行验证的原因
- 阻塞项
- 下一步建议（下一个会话应从何处继续）

同时更新 `PROGRESS.md` 的当前状态、最近验证、阻塞和下一步，确保会话启动流程（读取 PROGRESS.md）能直接定位断点。

### 退出检查

无论普通结束还是 60% 主动交接，均执行 `.harness/feedback/session-exit-checklist.md`。

