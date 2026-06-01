# 项目进度

> 更新日期：2026-06-01
> 分支：`rebuild_from_harness_v0.2.0` — 基于 harness + spec 从零重建

## 当前状态

- 最新检查点：**T004 Artifact infrastructure with HDF5 store 完成**；62 passed。
- 测试状态：62 passed；harness pre-commit 单测 5 passed。
- 构建状态：后端包可编辑安装。
- 代码结构：`contracts/`、`config/`、`api/`、`core/`、`services/` 模块已创建。
- 当前 active 功能项：无。

## 已完成

- T000 初始化项目内 harness
- T001 Backend skeleton：FastAPI app + GET /health + pytest TestClient 验证通过。
- T002 Common contracts and config：cst_params 12数校验、ratio 0<r<=1、WingPlanform/StructureDesign/MaterialProperties/ConditionParams/ResultMeta 契约 + config/settings.py 默认值。
- T003 Geometry 2D API：POST /geometry/airfoil-2d 接收 12 CST 参数，返回 200 个二维翼型点（前 100 上表面+后 100 下表面），含 is_stub/model_version 元信息。
- T004 Artifact infrastructure with HDF5 store — artifact_id 生成（SHA-256 前 12 位）、HDF5 写入 + JSON sidecar 同步落盘、artifact_registry 查询。
- 2026-06-01 T004 验证通过：62 passed，代码结构合规。
- 2026-06-01 测试阻塞修复：约束 FastAPI/Starlette/httpx/anyio 版本范围，并改用项目内同步 ASGI 测试客户端，避开当前环境中 Starlette TestClient 的线程桥超时。

## 进行中

- 无。

## 下一步

1. T005 Artifact query and download API — artifact 元信息查询和文件下载 HTTP 接口。

## 最近验证

- `cd backend && .venv/bin/python -m pytest`：62 passed。
- `backend/.venv/bin/python -m pytest .harness/tool/test_pre_commit_check.py`：5 passed。
- `python3 .harness/tool/pre-commit-check.py backend/tests/api_client.py backend/tests/test_health.py backend/tests/test_geometry_api.py .harness/tool/pre-commit-check.py .harness/tool/test_pre_commit_check.py`：通过。
