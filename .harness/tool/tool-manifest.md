# 工具清单

## 开发期工具

- shell：pytest、uvicorn、python、pip
- 文件系统：`backend/` 读写
- 版本控制：git

## 权限边界

- 只读：`docs/`、`.harness/`、`.claude/`
- 可写：`backend/`、`tasks/tasks.yaml`、`PROGRESS.md`、`DECISIONS.md`
- 禁止：`/etc/`、`~/.ssh/`、外部网络出站（除 PyPI）

## CI 工具（计划）

- pytest（单元 + 集成）
- ruff（lint + format）
- mypy（typecheck）
