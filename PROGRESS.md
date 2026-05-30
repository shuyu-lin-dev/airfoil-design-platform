# 项目进度

> 更新日期：2026-05-30

## 当前状态

- 最新检查点：**MVP 第一版全部 15 个任务完成（T000-T015）** + **项目自检（2026-05-30）**。
- 测试状态：**104 passed**, 8 warnings（CadQuery FutureWarning + Starlette DeprecationWarning）。
- 构建状态：FastAPI 应用可启动，所有 12 个 API 端点已注册。
- 目录结构：已修复 `backend/backend/` 空嵌套目录问题。
- 当前 active 功能项：无。

## 已完成

- [x] T000 - 初始化项目内 harness
- [x] T001 - Backend skeleton（FastAPI + /health + pytest）
- [x] T002 - Common contracts and config（Pydantic 契约 + settings 默认值）
- [x] T003 - Geometry 2D API（CST 翼型生成，200 点）
- [x] T004 - Artifact infrastructure with HDF5 store
- [x] T005 - Artifact query and download API
- [x] T006 - Aerodynamic prediction API（升阻比 + Cp + HDF5）
- [x] T007 - STEP artifact store（CadQuery 方盒验证）
- [x] T008 - Geometry 3D API（CadQuery 三维机翼 STEP 生成）
- [x] T009 - Structure prediction API（max_stress + weight）
- [x] T010 - Aerodynamic optimization API
- [x] T011 - Structural optimization API
- [x] T012 - Coupled optimization API（fitness = L/D / weight）
- [x] T013 - Teaching airfoil generation API
- [x] T014 - Teaching CST inverse API
- [x] T015 - Documentation pass（README + .gitignore）

## 进行中

- 无。

## 已知问题

- ~~`backend/backend/` 空嵌套目录（已修复，2026-05-30 自检）~~
- StarletteDeprecationWarning: httpx 应升级为 httpx2（不影响功能）
- CadQuery FutureWarning: `save` will be removed in next release
- 依赖安装需使用 Tsinghua 镜像（网络不稳定）
- Python 3.10.12 低于环境声明 ≥3.11（pyproject.toml 写 ≥3.10，实际不阻塞）

## 下一步

1. 接入真实神经网络模型替代 stub
2. 实现前端可视化
3. LangGraph 智能体调度
4. 数据库/对象存储持久化

## 最近验证

- 命令：`cd backend && pytest`
- 结果：**104 passed**, 8 warnings
- 证据：全部 15 个任务验收标准满足，T000-T015 status=passing；`backend/backend/` 空嵌套目录已删除，目录结构符合 architecture-boundaries.md 规范。
