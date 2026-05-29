# 项目进度

> 更新日期：2026-05-27

## 当前状态

- 最新检查点：项目内 harness 已补齐，Git 仓库已初始化，`AGENTS.md` 已按模板优化。
- 测试状态：后端测试未运行（`backend/` 尚未创建）。
- 构建状态：无构建（`backend/` 尚未创建）。
- 当前 active 功能项：无。

## 已完成

- [x] `CONTEXT.md` 建立领域语言和关键歧义处理规则。
- [x] 完整后端 MVP 规格移动到 `docs/backend-mvp-full-spec.md`。
- [x] `.harness/instruction/adr/0001-store-field-data-as-hdf5-artifacts.md` 记录 HDF5 artifact 决策。
- [x] `AGENTS.md`、`PROGRESS.md`、`DECISIONS.md`、`tasks/tasks.yaml`、`docs/spec.md`、`docs/api-contracts.md` 创建完成。
- [x] `.harness/` 子系统目录（instruction/、feedback/、state/）及文件创建完成。
- [x] `.harness/instruction/rules/` 五个规则文件创建完成，规则已从 `AGENTS.md` 拆分到专题文件。
- [x] `AGENTS.md` 收缩为入口索引，不再承载详细规则。
- [x] Git 仓库初始化完成。
- [x] `AGENTS.md` 按模板优化，补充快速开始、硬约束、专题文档和会话流程章节。

## 进行中

- [ ] 无 active 后端实现任务。

## 已知问题

- 后端依赖尚未安装。创建 `backend/pyproject.toml` 后确定安装方式。
- `backend/` 代码目录尚未创建。

## 下一步

1. 激活 `tasks/tasks.yaml` 中的 `T001 - Backend skeleton`。
2. 阅读 `.harness/state/sprint-contracts/T001-backend-skeleton.md`。
3. 创建 `backend/` 目录和最小 FastAPI 项目（`GET /health` + pytest/TestClient）。
4. 运行 `cd backend && pytest` 通过后更新 `tasks/tasks.yaml` 和本文。

## 最近验证

- 命令：`python3 -c "import yaml; ..."`
- 结果：通过；`tasks/tasks.yaml` 可解析，13 个任务均包含 `behavior/status/evidence`。
- 证据：`tasks/tasks.yaml` 第 1–25 行 workflow 和 feature_schema 定义完整。

- 命令：`test -f .harness/instruction/rules/agent-workflow.md ...`（五个规则文件）
- 结果：通过；五个规则文件和核心 harness 文件均存在。
- 证据：`.harness/instruction/rules/` 目录含 agent-workflow.md、domain-constraints.md、testing.md、artifact-policy.md、architecture-boundaries.md。

- 命令：后端测试 `cd backend && pytest`
- 结果：未运行。
- 证据：`backend/` 尚未创建，无测试可运行。
