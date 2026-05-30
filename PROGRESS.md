# 项目进度

> 更新日期：2026-05-30
> 分支：`rebuild_from_harness_v0.2.0` — 基于 harness + spec 从零重建

## 当前状态

- 最新检查点：**T003 Geometry 2D API 完成**，CST → 200 个二维翼型点 API 就绪。
- 测试状态：52 passed（1 health + 40 contracts + 11 geometry）。
- 构建状态：后端包可编辑安装。
- 代码结构：`contracts/`、`config/`、`api/`、`core/`、`services/` 模块已创建。
- 当前 active 功能项：无。

## 已完成

- T000 初始化项目内 harness
- T001 Backend skeleton：FastAPI app + GET /health + pytest TestClient 验证通过。
- T002 Common contracts and config：cst_params 12数校验、ratio 0<r<=1、WingPlanform/StructureDesign/MaterialProperties/ConditionParams/ResultMeta 契约 + config/settings.py 默认值。
- T003 Geometry 2D API：POST /geometry/airfoil-2d 接收 12 CST 参数，返回 200 个二维翼型点（前 100 上表面+后 100 下表面），含 is_stub/model_version 元信息。

## 进行中

- 无。

## 下一步

1. T004 Artifact infrastructure with HDF5 store — HDF5 存储基础设施。

## 最近验证

- `cd backend && pytest`：52 passed（test_health + test_contracts + test_contracts_material + test_geometry_api）。
