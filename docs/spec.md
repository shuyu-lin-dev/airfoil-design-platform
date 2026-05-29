# 后端 MVP 规格摘要

> 更新日期：2026-05-27
> 完整需求原文：`docs/backend-mvp-full-spec.md`

本文是 harness 友好的规格摘要，用于让 agent 快速理解第一版后端的目标、范围、边界和完成定义。若本文与完整需求原文冲突，先暂停并指出冲突。

## 项目目标

构建一个 FastAPI 后端 MVP，用占位算法打通翼型生成、气动预测、强度预测、优化设计和 artifact 存储的数据流，为后续真实模型、前端可视化和智能体调度打基础。

长期产品愿景是服务学生、翼型设计工程师和研究人员，支持翼型生成、气动预测、强度预测、优化设计和智能体调度。

## 第一版包含

- FastAPI 后端项目骨架。
- REST API 输入输出契约。
- pytest + TestClient 行为测试。
- 二维翼型生成，占位逻辑。
- 三维机翼生成，占位逻辑。
- 气动预测，占位逻辑。
- 强度预测，占位逻辑。
- 单一气动优化，占位逻辑。
- 单一强度优化，占位逻辑。
- 气动强度耦合优化，占位逻辑。
- 教学翼型生成与 CST 参数反推，占位逻辑。
- HDF5 artifact 存储边界。
- MessagePack / numpy bytes 内部高频数据通道预留。

## 第一版不做

- 前端页面。
- 真实可视化渲染。
- 真实神经网络模型。
- 真实遗传算法。
- LangGraph 智能体。
- DeepSeek API 调用。
- 用户登录权限。
- 数据库。
- 对象存储。
- 文件上传下载。

## 核心领域约束

- `cst_params` 正好 12 个数。
- CST 顺序固定：前 6 个为上表面系数，后 6 个为下表面系数。
- 工况参数包含 `mach` 和 `angle_of_attack`，单位分别为无量纲和 degree。
- 工况参数是评估条件，优化时不作为优化变量。
- 比例字段使用小数表达，范围为 `0 < ratio <= 1`。
- 二维翼型点固定 200 个，前 100 个为上表面，后 100 个为下表面。
- 三维机翼几何点固定 1000 个。
- 三维坐标系固定为 `x = 弦向`、`y = 厚度方向`、`z = 展向`。
- 结构设计参数包含 `spar_thickness`、`skin_thickness` 和 `rib_spacing`。
- 结构优化变量第一版只包含 `spar_thickness` 和 `rib_spacing`。
- 材料属性包含 `elastic_modulus` 和 `material_density`。
- API 使用 `weight` 表示重量，单位 N，不暴露 `mass`。
- 所有占位响应包含 `is_stub: true` 和 `model_version: "stub-v0"`。
- 耦合适应度第一版固定为 `fitness = lift_drag_ratio / weight`。

## Artifact 策略

REST JSON 用于请求参数、标量结果、小数组、优化参数和 artifact 元信息。压力场、速度场和后续大型场数据不直接通过 JSON 返回。

第一版气动预测将压力场和速度场写入本地 HDF5 artifact：

```text
backend/runtime_artifacts/aerodynamic/<artifact_id>.h5
backend/runtime_artifacts/aerodynamic/<artifact_id>.json
```

HDF5 dataset 布局：

```text
/coordinates
  shape: (1000, 3)

/fields/pressure
  shape: (1000,)

/fields/velocity
  shape: (1000,)
```

同名 JSON sidecar 保存 artifact 元信息，使 `GET /artifacts/{artifact_id}` 在进程重启后仍可查询。

第一版采用同步写入、异步语义：接口返回前写完文件，但保留 `pending / ready / failed` 状态契约。

## 推荐实现目录

```text
backend/
  README.md
  pyproject.toml
  tests/
  runtime_artifacts/
  src/
    airfoil_platform/
      main.py
      api/
      contracts/
      core/
      services/
      models/
      optimization/
      artifacts/
      serialization/
      config/
      lib/
```

目录职责：

- `api/`：FastAPI 路由，只做请求响应和调用 service。
- `contracts/`：Pydantic 数据契约。
- `core/`：翼型、气动、强度、优化的纯领域逻辑。
- `services/`：业务工作流编排。
- `models/`：模型适配层，第一版为 stub。
- `optimization/`：优化算法和目标函数，第一版为 stub。
- `artifacts/`：HDF5 artifact 存储。
- `serialization/`：MessagePack / numpy bytes 编解码边界。
- `config/`：默认值和路径配置。
- `lib/`：通用基础工具。

## Tracer bullet 顺序

1. Backend skeleton。
2. Common contracts。
3. Geometry 2D API。
4. Aerodynamic artifact API。
5. Geometry 3D API。
6. Structure prediction API。
7. Aerodynamic optimization API。
8. Structural optimization API。
9. Coupled optimization API。
10. Teaching airfoil generation API。
11. Teaching CST inverse API。
12. Documentation pass。

机器可读任务清单见 `tasks/tasks.yaml`。

## MVP 完成定义

- `backend/` 项目目录存在。
- FastAPI 应用可启动。
- `GET /health` 可访问。
- 1 到 9 的核心 API 契约存在。
- 每个核心接口有 API 行为测试。
- Artifact 测试覆盖 HDF5 文件、JSON sidecar、dataset 路径和 dataset shape。
- 占位数据流跑通。
- 压力场和速度场写入 HDF5 artifact，不走 JSON。
- 所有占位响应带 `is_stub: true` 和 `model_version: "stub-v0"`。
- 文档说明目标、非目标、字段单位、目录边界、artifact 策略、运行和测试命令。

## 标准验证命令

后端目录创建后：

```bash
cd backend && pytest
```

可选启动命令：

```bash
cd backend && uvicorn airfoil_platform.main:app --reload
```
