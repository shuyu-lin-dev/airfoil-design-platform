# 环境声明

## 运行时

- Python：≥3.10（当前 3.10.12，pyproject.toml requires-python 一致）
- 虚拟环境：venv（`backend/.venv/`）
- 包管理：pip + pyproject.toml

## 依赖

- FastAPI + uvicorn（Web 框架）
- pytest + httpx2（测试）
- h5py（HDF5 artifact 读写）
- numpy（数值计算）
- cadquery（三维 CAD 几何生成，可选）
- CadQuery 2.7.0 内部 `@deprecate` 装饰器产生 FutureWarning，pytest filterwarnings 已抑制

## 服务

- 无外部服务依赖（第一版单进程）

## 启动序列

1. `cd backend && python3.10 -m venv .venv && source .venv/bin/activate`
2. `pip install -e ".[dev,cad]"`
3. `source .venv/bin/activate && uvicorn airfoil_platform.main:app --reload`

## 验证

- `cd backend && source .venv/bin/activate && pytest`

## 冷启动自检

新会话能否仅凭仓库内容回答以下五个问题？若能，冷启动通过。

- [ ] **这是什么系统？** → `AGENTS.md` 第一节「项目概览」
- [ ] **如何组织？** → `AGENTS.md` § 专题文档 + `.harness/state/knowledge-index.md`
- [ ] **如何启动？** → `.harness/environment/environment.md` § 启动序列
- [ ] **如何验证？** → `cd backend && pytest`（及 `tasks/tasks.yaml` 中各任务的 `validation.commands`）
- [ ] **当前做到哪里？** → `PROGRESS.md` § 当前状态 + § 下一步
