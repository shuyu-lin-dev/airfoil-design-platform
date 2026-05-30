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

## 权限预授权清单（`.claude/settings.json`）

> 2026-05-30 精简：删除 19 条全局 `python3`/`python`/裸 `pytest` 权限，新增 venv 上下文命令。
> 核心原则：**只允许 venv 隔离环境内的操作，禁止使用系统全局 Python。**

### 版本控制

| 条目 | 覆盖范围 |
|------|---------|
| `Bash(git *)` | git add/commit/rm/stash 等全部操作 |

### 项目目录管理

| 条目 | 覆盖范围 |
|------|---------|
| `Bash(mkdir *)` | 创建项目目录 |

### 包管理

| 条目 | 覆盖范围 |
|------|---------|
| `Bash(pip *)` | pip install/uninstall/list（配合 venv 使用） |
| `Bash(uv *)` | uv 包管理 |

### 运行与测试（venv 上下文）

| 条目 | 覆盖范围 |
|------|---------|
| `Bash(cd backend && pytest *)` | 标准测试命令 |
| `Bash(cd backend && uvicorn *)` | 标准启动命令 |
| `Bash(source .venv/bin/activate && pytest *)` | venv 内测试（backend/ 目录） |
| `Bash(source .venv/bin/activate && python *)` | venv Python（隔离安全） |
| `Bash(source .venv/bin/activate && pip *)` | venv 内 pip |
| `Bash(source .venv/bin/activate && uvicorn *)` | venv 内启动 |
| `Bash(source backend/.venv/bin/activate && pytest *)` | venv 内测试（项目根目录） |
| `Bash(source backend/.venv/bin/activate && python *)` | venv Python（项目根目录） |
| `Bash(source backend/.venv/bin/activate && pip *)` | venv 内 pip（项目根目录） |

### venv Python 直接调用

| 条目 | 覆盖范围 |
|------|---------|
| `Bash(.venv/bin/python *)` | venv Python（backend/ 目录） |
| `Bash(backend/.venv/bin/python *)` | venv Python（项目根目录） |

### 只读检查

| 条目 | 覆盖范围 |
|------|---------|
| `Bash(python3.11 --version)` | Python 版本检查 |
| `Bash(python3.12 --version)` | Python 版本检查 |
| `Bash(.venv/bin/python3 --version)` | venv Python 版本 |
| `Bash(/home/lsy/.../backend/.venv/bin/python --version)` | venv Python 版本（绝对路径） |
| `Bash(python3.10 -m venv .venv)` | 一次性 venv 创建 |
| `Bash(pre-commit install *)` | pre-commit hook 安装 |

### 外部知识库（只读）

| 条目 | 覆盖范围 |
|------|---------|
| `Read(//home/lsy/workspace/notes/wiki/**)` | Wiki 读取 |
| `Bash(ls -la /home/lsy/workspace/notes/wiki/)` | Wiki 目录列表 |
| `Bash(find ... notes/wiki/ ... -iname '*agent*')` | Wiki 搜索 |
| `Bash(find ... notes/wiki/ ... -iname '*harness*')` | Wiki 搜索 |
| `Bash(grep -rl ... notes/wiki/ ...)` | Wiki 全文搜索 |

### 已移除的权限（及原因）

| 原条目 | 移除原因 |
|--------|---------|
| `Bash(python3 *)` | 使用全局 Python，绕过 .venv 隔离 |
| `Bash(python *)` | 同上 |
| `Bash(pytest)` / `Bash(pytest -v)` / `Bash(pytest -q)` | 裸 pytest 无 venv 保证；已替换为 `source .venv/bin/activate && pytest *` |
| `Bash(PYTHONPATH=src python3 *)` ×6 | 全局 Python + 内联代码，双重风险 |
| `Bash(pytest tests/test_*.py -v)` ×9 | 裸 pytest，无 venv 上下文 |
| `Bash(ls *)` `Bash(find *)` `Bash(cat *)` `Bash(rg *)` `Bash(echo *)` `Bash(wc *)` `Bash(grep *)` `Bash(test *)` | Claude Code 已 auto-allow，无需显式配置 |
| `Read(//usr/bin/**)` | 过宽的文件系统读取权限 |
