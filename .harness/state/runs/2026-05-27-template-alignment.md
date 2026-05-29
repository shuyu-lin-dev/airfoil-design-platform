# Harness Template Alignment Run

> 日期：2026-05-27

## 目标

按照 `agent-harness-operating-model.html` 中“模板集”的 8 类模板，检查并更新当前项目内 harness。

## 模板来源

- `AGENTS.md` 路由文件
- `PROGRESS.md`
- `DECISIONS.md`
- 初始化契约
- 功能清单
- 完成定义
- 冲刺合同
- 会话退出检查清单

## 更新内容

- 新增 `DECISIONS.md`。
- 新增 `.harness/bootstrap-contract.md`。
- 新增 `.harness/definition-of-done.md`。
- 新增 `.harness/session-exit-checklist.md`。
- 新增 `.harness/sprint-contracts/T001-backend-skeleton.md`。
- 新增 `.harness/template-compliance.md`。
- 更新 `AGENTS.md`，补齐快速开始、专题文档和会话流程。
- 更新 `PROGRESS.md`，改为更贴近模板的进度日记结构。
- 更新 `tasks/tasks.yaml`，为功能项补充 `behavior` 和 `evidence` 字段。
- 更新 `docs/spec.md` 和 `docs/api-contracts.md` 的完整规格引用路径。

## 结论

当前 harness 已满足模板集的最小写法。后续实现任务开始前，应先阅读当前任务对应的冲刺合同；任务结束前，应检查会话退出清单。

