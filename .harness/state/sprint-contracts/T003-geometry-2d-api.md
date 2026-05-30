# 冲刺合同：T003 Geometry 2D API

## 范围

- 创建 `backend/src/airfoil_platform/contracts/geometry.py`：`Airfoil2DRequest`（cst_params 12 数校验）、`AirfoilPoint`（x,y）、`Airfoil2DResponse`（points + ResultMeta 继承）。
- 创建 `backend/src/airfoil_platform/core/geometry.py`：纯函数 `cst_to_airfoil_points(cst_params, n_points=100)`，实现 CST class/shape function 数学，返回 (upper_points, lower_points) 各 100 个 `AirfoilPoint`。
- 创建 `backend/src/airfoil_platform/services/geometry_service.py`：`generate_airfoil_2d(request) -> Airfoil2DResponse`，编排 core 调用、组装响应。
- 创建 `backend/src/airfoil_platform/api/geometry.py`：`APIRouter`，`POST /airfoil-2d`，收 `Airfoil2DRequest`，调 service，返回 `Airfoil2DResponse`。
- 创建 `backend/tests/test_geometry_api.py`：TDD 先写测试，用 TestClient 挂载 geometry router 的独立 app 测试。

## 验证标准

- POST /geometry/airfoil-2d 接收 12 个 CST 参数。
- 返回 200 个二维翼型点，前 100 个为上表面，后 100 个为下表面。
- 响应包含 `is_stub: true` 和 `model_version: "stub-v0"`。
- cst_params 非 12 个时返回 422。
- `cd backend && pytest` 全部通过。

## 排除项

- 不注册路由到 `main.py`（测试用独立 app 挂载 router）。
- 不引入新第三方依赖（CST 数学只用 `math` 标准库）。
- 不做三维几何、不做气动预测、不做 artifact 存储。

## 观测信号

- 日志：第一版不要求结构化日志。
- 任务轨迹：`tasks/tasks.yaml` T003.evidence 和 `PROGRESS.md` 的最近验证。

## 失败反馈格式

- WHAT：哪条命令或测试失败。
- WHY：从错误消息判断的直接原因。
- FIX：下一步应修改的文件或配置。
