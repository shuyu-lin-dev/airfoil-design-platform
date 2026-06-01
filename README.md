# 翼型气动与强度智能设计平台

后端 MVP v0.2.0 — 基于 FastAPI + cadquery，提供翼型生成、气动/强度预测、优化和教学接口。

## 技术栈

`Python 3.10` `FastAPI` `Pydantic v2` `cadquery` `h5py` `numpy` `pytest`

## 快速开始

```bash
git clone https://github.com/shuyu-lin-dev/airfoil-design-platform.git
cd airfoil-design-platform/backend
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,cad]"
pytest  # 101 passed
```

```bash
uvicorn airfoil_platform.main:app --reload
# FastAPI docs: http://127.0.0.1:8000/docs
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/geometry/airfoil-2d` | CST 参数 → 200 个翼型点 |
| POST | `/geometry/wing-3d` | CST + 平面 + 结构 → STEP 装配 |
| POST | `/aerodynamics/predict` | 气动预测（升阻比 + Cp + HDF5） |
| POST | `/structure/predict` | 强度预测（max_stress + weight） |
| POST | `/optimization/aerodynamic` | 气动优化 |
| POST | `/optimization/structural` | 结构优化 |
| POST | `/optimization/coupled` | 耦合优化 |
| GET | `/artifacts/{id}` | Artifact 元信息 |
| GET | `/artifacts/{id}/download` | Artifact 下载 |
| POST | `/teaching/airfoil-from-control-points` | 控制点翼型生成 |
| POST | `/teaching/cst-from-airfoil` | 翼型点 → CST 反推 |

## Artifact 存储

- **HDF5** — 压力场/速度场（`/coordinates` `/fields/pressure` `/fields/velocity`）
- **STEP** — 三维机翼结构几何（蒙皮/前梁/后梁/翼肋多组件装配）
- 每个 artifact 配 JSON sidecar 元信息，查询/下载分离

## 目录结构

```
backend/
├── src/airfoil_platform/
│   ├── api/          # FastAPI 路由
│   ├── contracts/    # Pydantic 请求/响应模型
│   ├── core/         # 纯计算函数
│   ├── services/     # 编排层
│   ├── artifacts/    # HDF5/STEP 存储
│   ├── config/       # 默认值、硬校验边界
│   └── main.py       # FastAPI 应用入口
├── tests/
│   ├── api_client.py # 同步 ASGI 测试客户端
│   └── test_*.py     # 行为测试
└── runtime_artifacts/
    ├── aerodynamic/  # HDF5 + JSON sidecar
    └── geometry/     # STEP + JSON sidecar
```

## 架构约束

- `api/` 不写业务逻辑，只做路由
- `core/` 纯函数，不依赖实现类
- `artifacts/` 不依赖业务层
- 单文件 ≤200 行，函数 ≤50 行

## 文档

- [AGENTS.md](AGENTS.md) — Agent 入口，会话路由
- [PROGRESS.md](PROGRESS.md) — 任务进度和当前状态
- [DECISIONS.md](DECISIONS.md) — 设计决策记录
- [CONTEXT.md](CONTEXT.md) — 领域语言、字段边界
- [docs/spec.md](docs/spec.md) — MVP 规格摘要
- [docs/api-contracts.md](docs/api-contracts.md) — API 契约
- [backend/README.md](backend/README.md) — 后端开发指南
