# 环境声明

## 运行时

- Python：3.11+
- 虚拟环境：venv（项目本地 `.venv/`）
- 包管理：pip + pyproject.toml

## 依赖

- FastAPI + uvicorn（Web 框架）
- pytest + httpx（测试）
- h5py（HDF5 artifact 读写）
- numpy（数值计算）

## 服务

- 无外部服务依赖（第一版单进程）

## 启动序列

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -e .`
3. `uvicorn airfoil_platform.main:app --reload`

## 验证

- `cd backend && pytest`
