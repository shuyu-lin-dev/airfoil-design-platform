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
- 三维机翼结构 STEP 生成。
- 气动预测，占位逻辑。
- 强度预测，占位逻辑。
- 单一气动优化，占位逻辑。
- 单一强度优化，占位逻辑。
- 气动强度耦合优化，占位逻辑。
- 教学翼型生成与 CST 参数反推，占位逻辑。
- HDF5 与 STEP artifact 存储边界。
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
- 文件上传。

## 核心领域约束

- `cst_params` 正好 12 个数。
- CST 顺序固定：前 6 个为上表面系数，后 6 个为下表面系数。
- 工况参数包含 `mach` 和 `angle_of_attack`，单位分别为无量纲和 degree。
- 工况参数是评估条件，优化时不作为优化变量。
- 比例字段使用小数表达，范围为 `0 < ratio <= 1`。
- 二维翼型点固定 200 个，前 100 个为上表面，后 100 个为下表面。
- 三维机翼生成返回结构 STEP artifact，不返回 1000 个点云。
- 三维坐标系固定为 `x = 弦向`、`y = 厚度方向`、`z = 展向`。
- `wing_planform.span` 表示全展长；第一版结构 STEP 只生成右半翼，`z` 范围为 `0 <= z <= span / 2`。
- 第一版结构 STEP 使用矩形直半翼假设：`chord` 为恒定弦长，锥度比 1.0，后掠角、上反角和扭转角均为 0。
- `wing_planform.span` 和 `wing_planform.chord` 单位均为 m，字段名不带单位后缀；默认值为 `DEFAULT_WING_SPAN = 10.0`、`DEFAULT_WING_CHORD = 1.0`。
- `wing_planform.span` 和 `wing_planform.chord` 出现时必须是有限正数，硬校验范围为 `0 < span <= 100`、`0 < chord <= 20`。
- 结构设计参数包含 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`，单位均为 m，三个字段全部必填。
- 结构设计参数范围为：`rear_spar_web_thickness` 0.002–0.020 m，`rib_thickness` 0.002–0.005 m，`rib_spacing` 0.300–1.000 m。
- `rib_spacing` 是最大目标肋距；翼根和半翼翼尖都必须有翼肋，实际均匀肋距可小于或等于请求值。
- 前梁腹板厚度固定派生为后梁腹板厚度的 1.5 倍。
- 蒙皮厚度固定为 0.0015 m，不作为请求字段或优化变量。
- 前梁弦向位置固定为 0.15，后梁弦向位置固定为 0.70。
- 结构优化变量第一版包含 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`。
- 三维机翼 STEP 生成必须使用 CAD kernel，首选 CadQuery/OpenCascade，备选 pythonocc-core，禁止手写 STEP 文本伪造几何。
- 蒙皮沿弦向全程按固定蒙皮厚度向内部偏置；翼盒段厚度不足时拒绝请求；前缘段和尾缘段偏置后上下表面相交时融合为实心填充体。
- 结构 STEP 是多组件结构装配，蒙皮、前梁、后梁和翼肋保持独立实体并接触，不做布尔融合或连接件细节。
- 材料属性区分 `skin` 和 `internal_structure` 两组；出现的材料组必须同时提供 `elastic_modulus` 和 `material_density`，值必须为严格正数（`> 0`）；蒙皮默认铝合金 70 GPa / 2700 kg/m^3，内部结构默认结构钢 200 GPa / 7850 kg/m^3。
- API 使用 `weight` 表示全翼结构重量，单位 N，不暴露 `mass`，只包含蒙皮、前梁、后梁和翼肋。
- `max_stress` 表示整个结构装配的最大等效应力，单位 Pa。
- `lift_drag_ratio` 表示二维翼型升阻比，不表示三维机翼或全机升阻比。
- 所有占位响应包含 `is_stub: true` 和 `model_version: "stub-v0"`。
- 耦合适应度第一版固定为 `fitness = wing_lift_drag_ratio / weight`，其中分子为展向积分后的三维机翼升阻比，是 MVP 排序指标。

## Artifact 策略

`artifact_id` 由输入参数的规范化 JSON 序列化后取 SHA-256 前 12 字符生成，相同输入产生相同 ID，天然幂等。

REST JSON 用于请求参数、标量结果、小数组、优化参数和 artifact 元信息。压力场、速度场、STEP 几何和后续大型数据不直接通过 JSON 返回。

第一版气动预测将压力场和速度场写入本地 HDF5 artifact：

```text
backend/runtime_artifacts/aerodynamic/<artifact_id>.h5
backend/runtime_artifacts/aerodynamic/<artifact_id>.json
```

第一版三维机翼生成将结构几何写入本地 STEP artifact：

```text
backend/runtime_artifacts/geometry/<artifact_id>.step
backend/runtime_artifacts/geometry/<artifact_id>.json
```

STEP artifact 的角色为 `structural_step`，覆盖蒙皮、前梁、后梁和翼肋，必须是 CAD/网格工具可打开的有效 STEP 文件。第一版 STEP 是右半翼多组件结构装配；面向外流场 CFD 的干净外表面 STEP 不进入第一版。MVP 自动验收的最低口径是 CAD kernel 可回读、组件可识别、组件几何非空、整体外包盒符合 `chord` 和 `span / 2`，以及翼肋数量符合 `rib_spacing` 推导规则；梁/肋与蒙皮内表面精确贴合和结构网格划分可用性先作为几何生成目标，不作为自动测试硬门槛。

HDF5 dataset 布局（二维翼型绕流场）：

```text
/coordinates
  shape: (1000, 2)

/fields/pressure
  shape: (1000,)

/fields/velocity
  shape: (1000,)
```

同名 JSON sidecar 保存 artifact 元信息，使 `GET /artifacts/{artifact_id}` 在进程重启后仍可查询。`GET /artifacts/{artifact_id}/download` 返回 artifact 文件内容。

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
- `artifacts/`：HDF5 与 STEP artifact 存储。
- `serialization/`：MessagePack / numpy bytes 编解码边界。
- `config/`：默认值和路径配置。
- `lib/`：通用基础工具。

## Tracer bullet 顺序

任务按原子化原则拆分，每个任务只承担一个可独立验证的关注点。机器可读任务清单见 `tasks/tasks.yaml`。

1. Backend skeleton（T001）。
2. Common contracts and config（T002）。
3. Geometry 2D API（T003）。
4. Artifact infrastructure with HDF5 store（T004）。
5. Artifact query and download API（T005）。
6. Aerodynamic prediction API（T006）。
7. STEP artifact store（T007）。
8. Geometry 3D API（T008）。
9. Structure prediction API（T009）。
10. Aerodynamic optimization API（T010）。
11. Structural optimization API（T011）。
12. Coupled optimization API（T012）。
13. Teaching airfoil generation API（T013）。
14. Teaching CST inverse API（T014）。
15. Documentation pass（T015）。

T003 与 T004 可并行（均只依赖 T002）；T005/T006/T007 可并行（均只依赖 T004）；T009/T010/T011 可并行（均只依赖 T002）。

## MVP 完成定义

- `backend/` 项目目录存在。
- FastAPI 应用可启动。
- `GET /health` 可访问。
- 工程核心 API 1 到 9 和教学 API 10 到 11 的契约都存在。
- 每个核心接口和教学接口都有 API 行为测试。
- Artifact 测试覆盖 HDF5/STEP 文件、JSON sidecar、dataset 路径、dataset shape、STEP 回读、组件/外包盒基本合理性和文件下载。
- 占位数据流跑通。
- 压力场和速度场写入 HDF5 artifact，不走 JSON。
- 三维机翼结构几何写入有效 STEP artifact，不走点云 JSON。
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
