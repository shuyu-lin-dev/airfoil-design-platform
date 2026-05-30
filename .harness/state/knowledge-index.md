# 知识全景目录

Agent 冷启动或知识检索时，按此目录定位对应知识制品。类型和成熟度定义见 `DECISIONS.md` 前言。

## 领域模型 [model]

| 制品 | 成熟度 | 内容 |
|------|--------|------|
| `CONTEXT.md` § Language | verified | 40+ 术语定义，含 Avoid 指引 |
| `CONTEXT.md` § Relationships | verified | 概念间结构关系和约束 |
| `CONTEXT.md` § Example dialogue | verified | 对话式歧义消解示例 |
| `docs/spec.md` | draft | MVP 规格摘要 |
| `docs/api-contracts.md` | draft | API 输入输出契约摘要 |
| `docs/backend-mvp-full-spec.md` | draft | 完整原始规格（权威细节源） |

## 设计决策 [decision]

| 制品 | 成熟度 | 内容 |
|------|--------|------|
| `DECISIONS.md` | verified | 14 项关键决策（harness 架构到多 Agent 并行化） |
| `docs/adr/0001-*.md` | verified | HDF5 artifact 存储决策 |
| `docs/adr/0002-*.md` | verified | 结构 STEP 几何决策 |

## 操作指南 [guideline]

| 制品 | 成熟度 | 内容 |
|------|--------|------|
| `.harness/instruction/rules/io-hygiene.md` | verified | 截断/抽帧/落盘规则 |
| `.harness/instruction/rules/testing.md` | verified | TDD、pytest 标准验证 |
| `.harness/instruction/rules/artifact-policy.md` | verified | HDF5/STEP 存储契约 |
| `.harness/instruction/rules/architecture-boundaries.md` | verified | 目录职责和依赖方向 |
| `.harness/instruction/rules/domain-constraints.md` | verified | 字段格式/单位/范围硬约束 |

## 流程约定 [process]

| 制品 | 成熟度 | 内容 |
|------|--------|------|
| `.harness/instruction/rules/agent-workflow.md` | verified | WIP=1、交接规则、工作状态管理 |
| `.harness/feedback/session-exit-checklist.md` | verified | 会话退出检查项 |
| `.harness/environment/environment.md` | verified | 运行时、依赖和启动序列 |
| `tasks/tasks.yaml` | verified | 16 个机器可读任务契约 |
| `.harness/state/sprint-contracts/` | draft | 各任务冲刺合同 |

## 陷阱与反模式 [pitfall]

| 制品 | 成熟度 | 内容 |
|------|--------|------|
| `CONTEXT.md` § Flagged ambiguities | verified | 50+ 已解决的术语歧义和混用 |

## 运行时记录

| 制品 | 性质 |
|------|------|
| `PROGRESS.md` | 当前进度、阻塞和下一步（每次会话更新） |
| `.harness/state/runs/` | 会话交接记录和运行日志 |
| `.harness/state/runs/telemetry.yaml` | 运行遥测记录（每次会话填充模板，含 task_id、status、token/tool 估算和累积统计） |
| `.harness/state/working/` | 当前任务临时草稿区（任务结束清空） |
