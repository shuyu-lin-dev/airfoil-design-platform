# 项目进度

> 更新日期：2026-06-01
> 分支：`rebuild_from_harness_v0.2.0` — 基于 harness + spec 从零重建

## 当前状态

- 最新检查点：**T005 Artifact query and download API 完成**；67 passed。
- 测试状态：67 passed；harness pre-commit 单测 5 passed。
- 构建状态：后端包可编辑安装。
- 代码结构：`contracts/`、`config/`、`api/`、`core/`、`services/`、`artifacts/` 模块已创建。
- 当前 active 功能项：无。

## 已完成

- T000 初始化项目内 harness
- T001 Backend skeleton：FastAPI app + GET /health + pytest TestClient 验证通过。
- T002 Common contracts and config：cst_params 12数校验、ratio 0<r<=1、WingPlanform/StructureDesign/MaterialProperties/ConditionParams/ResultMeta 契约 + config/settings.py 默认值。
- T003 Geometry 2D API：POST /geometry/airfoil-2d 接收 12 CST 参数，返回 200 个二维翼型点（前 100 上表面+后 100 下表面），含 is_stub/model_version 元信息。
- T004 Artifact infrastructure with HDF5 store — artifact_id 生成（SHA-256 前 12 位）、HDF5 写入 + JSON sidecar 同步落盘、artifact_registry 查询。
- T005 Artifact query and download API — GET /artifacts/{id} 从 JSON sidecar 返回元信息、GET /artifacts/{id}/download 返回 HDF5 文件、路由器在 main.py 注册。
- 2026-06-01 T005 验证通过：67 passed，代码结构合规。

## 进行中

- 无。

## 下一步

1. T006 Aerodynamic prediction API — 提交 CST 参数和工况，获得升阻比、Cp 分布和 HDF5 场数据 artifact。

## 最近验证

- `cd backend && .venv/bin/python -m pytest`：67 passed。
- `backend/.venv/bin/python -m pytest .harness/tool/test_pre_commit_check.py`：5 passed。
