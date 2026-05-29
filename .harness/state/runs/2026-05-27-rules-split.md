# Harness Rules Split Run

> 日期：2026-05-27

## 目标

将 `AGENTS.md` 从规则合集收缩为入口路由文件，并把工作规则、领域约束、测试规则、artifact 策略和架构边界拆分到 `docs/rules/`。

## 更新内容

- 新增 `docs/rules/agent-workflow.md`。
- 新增 `docs/rules/domain-constraints.md`。
- 新增 `docs/rules/testing.md`。
- 新增 `docs/rules/artifact-policy.md`。
- 新增 `docs/rules/architecture-boundaries.md`。
- 重写 `AGENTS.md`，只保留项目概览、入口索引、规则索引和当前入口。
- 更新 `DECISIONS.md`，记录规则拆分决策。
- 更新 `PROGRESS.md`、`.harness/bootstrap-contract.md`、`.harness/template-compliance.md` 和 `tasks/tasks.yaml`。

## 结论

当前 `AGENTS.md` 不再承载详细工作规则、标准命令或领域硬约束；规则按专题进入 `docs/rules/`，更符合渐进式披露。

