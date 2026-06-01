# Harness 模板符合性检查

> 检查日期：2026-05-27
> 模板来源：`agent-harness-operating-model.html` 的“模板集”章节

## 检查结论

当前 harness 已覆盖模板集中的 8 类工件。`AGENTS.md` 已收缩为路由入口；详细规则拆分到 `.harness/instruction/rules/`，符合渐进式披露原则。项目仍处于后端未创建阶段，因此启动、安装、测试类条目有明确的“尚未定义/尚未运行”说明。

## 对照表

| 模板项 | 当前文件 | 状态 | 说明 |
|---|---|---|---|
| `AGENTS.md` 路由文件 | `AGENTS.md` | 满足 | 只保留项目概览、入口索引、规则索引和当前入口，不承载详细规则。 |
| `PROGRESS.md` | `PROGRESS.md` | 满足 | 已按当前状态、已完成、进行中、已知问题、下一步、最近验证组织。 |
| `DECISIONS.md` | `DECISIONS.md` | 满足 | 已记录项目内 harness、`CONTEXT.md`、完整规格移动和 Git 初始化决策。 |
| 初始化契约 | `.harness/instruction/bootstrap-contract.md` | 满足 | 已记录启动命令、当前状态、项目结构和初始化验收清单。 |
| 功能清单 | `tasks/tasks.yaml` | 满足 | 使用 YAML 表达行为、验证、状态、证据和任务边界。 |
| 完成定义 | `.harness/feedback/definition-of-done.md` | 满足 | 已外部化通用完成条件和后端 MVP 完成条件。 |
| 冲刺合同 | `.harness/state/sprint-contracts/T001-backend-skeleton.md` | 满足 | 已为下一项任务 T001 写明范围、验证、排除项和观测信号。 |
| 会话退出检查清单 | `.harness/feedback/session-exit-checklist.md` | 满足 | 已列出清洁退出和交接要求。 |
| 专题规则 | `.harness/instruction/rules/` | 满足 | 已按 agent 工作流、领域约束、测试、artifact 和架构边界拆分。 |

## 发现与修正

- 发现：原 `tasks/tasks.yaml` 更像任务计划，缺少模板中的 `behavior` 和 `evidence` 字段。
- 修正：为所有任务补充 `behavior` 和 `evidence`。
- 发现：缺少 `DECISIONS.md`。
- 修正：新增 `DECISIONS.md` 并记录已有关键决策。
- 发现：缺少初始化契约、完成定义、冲刺合同和退出检查清单。
- 修正：新增 `.harness/instruction/`、`.harness/feedback/`、`.harness/state/` 下对应模板工件。
- 发现：`docs/spec.md` 和 `docs/api-contracts.md` 仍引用旧完整规格路径。
- 修正：改为引用 `docs/backend-mvp-full-spec.md`。
- 发现：`AGENTS.md` 曾包含工作规则、标准命令和领域硬约束，入口过重。
- 修正：新增 `.harness/instruction/rules/` 并将规则拆分到专题文件，`AGENTS.md` 只保留索引。
