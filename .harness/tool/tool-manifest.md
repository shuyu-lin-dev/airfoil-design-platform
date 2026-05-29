# 工具清单

## 开发期工具

- shell：pytest、uvicorn、python、pip
- 文件系统：`backend/` 读写；`.harness/state/` 写运行状态
- 版本控制：git

## 权限边界

- 默认只读：`docs/`、`.claude/`、`.harness/instruction/`、`.harness/feedback/`、`.harness/environment/`、`.harness/tool/`
- 常规任务可写：`backend/`、`tasks/tasks.yaml`、`PROGRESS.md`、`DECISIONS.md`、`.harness/state/runs/`、`.harness/state/sprint-contracts/`
- 条件可写：当当前任务 `allowed_paths` 明确包含，或用户明确要求维护 harness/文档时，可修改对应 `docs/`、`.harness/instruction/`、`.harness/feedback/` 或 `.harness/tool/` 文件；关键规则变更必须同步更新 `DECISIONS.md` 和 `PROGRESS.md`
- 禁止：`/etc/`、`~/.ssh/`、外部网络出站（除 PyPI）

## CI 工具（计划）

- pytest（单元 + 集成）
- ruff（lint + format）
- mypy（typecheck）
