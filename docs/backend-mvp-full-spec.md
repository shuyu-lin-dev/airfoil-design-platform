# 翼型气动与强度智能设计平台后端 MVP Spec

> 版本：v0.1  
> 日期：2026-05-27

本文是翼型气动与强度智能设计平台后端 MVP 的单一事实源。长期产品愿景保留在“长期目标”小节中；后端第一版的范围、契约、目录、测试和完成定义均以本文为准。

## 1. 项目目标

### 长期目标

构建一个面向学生和翼型设计工程师的翼型气动与强度智能设计平台，支持翼型生成、气动预测、强度预测、优化设计和智能体调度，帮助用户快速上手并高效完成翼型设计迭代。

### 第一版目标

构建 FastAPI 后端 MVP，用占位算法打通翼型生成、气动预测、强度预测和优化设计的数据流，明确输入输出契约、artifact 策略、目录结构和测试工作流，为后续接入真实模型、前端可视化和智能体调度打基础。

第一版先不实现前端、不实现智能体、不接真实神经网络模型、不实现真实遗传算法、不做真实可视化渲染。所有预测、优化、生成逻辑先用简单占位函数实现，目标是保证数据流和工作流可以正常跑通。

## 2. 目标用户

### 学生 / 教学用户

学生用户主要用于理解翼型设计过程：

- CST 参数如何生成二维翼型。
- 中弧线、厚度分布如何影响翼型形状。
- 已知翼型坐标如何反推 CST 参数。
- 气动/强度预测结果与输入参数之间大致有什么关系。

### 翼型设计工程师 / 研究人员

工程用户主要用于快速迭代设计方案：

- 输入一组翼型参数和工况参数。
- 快速得到气动性能、压力场、速度场、强度和重量结果。
- 对气动、强度或耦合目标做优化。
- 拿到优化前后的参数和性能对比结果。

### 第一版实际使用者

第一版不做前端和智能体，因此实际使用者是：

- 后端调用者。
- 测试人员。
- 未来前端。
- 未来智能体工具封装层。

## 3. 用户常见完整使用路径

### 1. 二维翼型生成

输入 12 个 CST 参数，自动输出 200 个二维翼型 `xy` 几何坐标点。长期目标中支持绘制二维翼型并可视化展示；第一版只返回可视化所需数据。

### 2. 气动预测

输入 12 个 CST 参数和 2 个工况参数：

- 调用升阻比神经网络模型得到升阻比。
- 默认内置 200 个 `xy` 坐标点，调用气动神经网络模型得到 Cp 分布。
- 默认内置 1000 个三维坐标点，调用压力场神经网络模型得到压力场分布。
- 默认内置 1000 个三维坐标点，调用速度场神经网络模型得到速度场分布。

第一版中升阻比、Cp、压力场、速度场都由占位逻辑生成。

### 3. 单一气动优化

输入 12 个 CST 参数、2 个工况参数和优化幅度，例如 10%。工况参数作为评估条件传入优化算法，用于调用神经网络模型计算升阻比，但不作为优化变量。当优化后翼型的升阻比与原始翼型的升阻比相比提升 10% 后，输出：

- 优化后的 12 个 CST 参数。
- 原始评估工况参数。
- 原始翼型的升阻比。
- 优化后的升阻比。

第一版只实现占位优化流程。

### 4. 三维机翼生成

输入 12 个 CST 参数、机翼平面参数和完整结构设计参数，暂定先生成 1000 个三维机翼 `xyz` 坐标点。长期目标中支持绘制三维机翼并可视化展示；第一版只返回三维坐标数据。

### 5. 强度预测

输入 12 个 CST 参数、2 个工况参数、机翼平面参数、结构设计参数和材料属性，调用：

- 应力极值神经网络预测模型，得到应力极值。
- 重量神经网络预测模型，得到重量。

第一版只实现占位强度预测。

### 6. 单一强度优化

输入 12 个 CST 参数、2 个工况参数、机翼平面参数、结构设计参数、材料属性和优化幅度，例如 10%。工况参数作为评估条件传入优化算法，但不作为优化变量。调用遗传算法，仅优化结构设计参数。当优化后的重量减轻 10% 后优化停止，输出：

- 优化后的 12 个 CST 参数。
- 原始评估工况参数。
- 优化后的结构设计参数。
- 原始机翼的重量。
- 优化后的重量。

第一版只实现占位优化流程。

### 7. 气动强度耦合优化

输入 12 个 CST 参数、2 个工况参数、机翼平面参数、结构设计参数、材料属性和优化幅度，例如 10%。工况参数作为评估条件传入优化算法，但不作为优化变量。调用遗传算法，当气动与强度耦合适应度提升 10% 后优化停止。第一版耦合适应度定义为 `fitness = lift_drag_ratio / weight`，输出：

- 优化后的 12 个 CST 参数。
- 原始评估工况参数。
- 优化后的结构设计参数。
- 原始机翼的重量、升阻比和适应度。
- 优化后的重量、升阻比和适应度。

第一版只实现占位耦合优化流程。

### 8. 辅助教学二维翼型生成

通过输入两个中弧线教学控制点坐标和两个厚度分布教学控制点坐标，输出 200 个二维翼型 `xy` 几何坐标点。

第一版只实现占位教学生成逻辑。

### 9. 辅助教学翼型 CST 参数生成

通过输入 200 个二维翼型 `xy` 几何坐标点，输出 12 个 CST 参数。

第一版只实现占位反推逻辑。

### 10. 智能体调度

长期目标中使用 LangGraph 编写智能体调度，使用 LLM 调用 DeepSeek 模型 API 进行对话，理解用户需求，例如预测、优化、提问等，并根据用户需求按 ReAct 模式自动调用上述工具。

智能体调度不进入第一版 MVP。

## 4. MVP 范围

### 第一版包含

- FastAPI 后端项目骨架。
- REST API 输入输出契约。
- TDD 测试。
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

### 第一版不做

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

## 5. 核心对象和字段

### CST 参数

```text
cst_params: number[12]
```

约束：

- 必须正好 12 个数。
- 顺序固定：前 6 个为上表面 CST 系数，后 6 个为下表面 CST 系数。
- 第一版先不强制物理范围。

顺序定义：

```text
cst_params = [
  upper_0, upper_1, upper_2, upper_3, upper_4, upper_5,
  lower_0, lower_1, lower_2, lower_3, lower_4, lower_5
]
```

### 工况参数

```text
mach: number
angle_of_attack: number
```

单位：

- `mach`：无量纲。
- `angle_of_attack`：degree。

工况参数是预测和优化中的评估条件。优化算法需要接收工况参数以调用模型计算升阻比、应力或重量，但第一版优化器不改变工况参数。

### 结构设计参数

结构设计参数描述三维机翼中的梁、蒙皮和肋等结构几何。三维机翼生成、强度预测、强度优化和耦合优化都接收完整的 `structure_design`。

```text
spar_thickness: number
skin_thickness: number
rib_spacing: number
```

### 结构优化变量

结构优化变量是强度优化第一版允许改变的结构设计参数子集。第一版只优化：

```text
spar_thickness
rib_spacing
```

`skin_thickness` 属于结构设计参数，但第一版强度优化和耦合优化不自动改变它。

### 机翼平面参数

机翼平面参数描述三维机翼的基础尺度。强度预测、强度优化和耦合优化的对象是三维机翼；`cst_params` 只定义二维翼型截面。第一版可由用户覆盖 `span` 和 `chord`，否则使用配置默认值。

```text
span?: number
chord?: number
```

默认值：

```text
DEFAULT_WING_SPAN_M
DEFAULT_WING_CHORD_M
```

这些默认值统一由 `config/settings.py` 管理。

### 材料属性

材料属性参与强度和重量预测，但第一版不作为结构几何。用户可以覆盖默认值。

```text
elastic_modulus: number
material_density: number
```

默认值：

```text
DEFAULT_ELASTIC_MODULUS_PA = 70_000_000_000
DEFAULT_MATERIAL_DENSITY_KG_M3 = 2700
```

这些默认值统一由 `config/settings.py` 管理，业务代码不得在 service、model 或 core 中重复硬编码。

单位：

- `spar_thickness`：m。
- `skin_thickness`：m。
- `rib_spacing`：m。
- `elastic_modulus`：Pa。
- `material_density`：kg/m^3。

### 坐标系

```text
x = 弦向
y = 厚度方向
z = 展向
```

### 二维点

```json
{
  "x": 0.0,
  "y": 0.0
}
```

二维翼型生成固定返回 200 个二维翼型点，点序为闭合翼型轮廓顺序：

```text
points[0:100]   = 上表面，从前缘到后缘
points[100:200] = 下表面，从后缘回到前缘
```

不额外重复第一个点，因此总数保持 200。前端绘图可按顺序连线，并在需要闭合轮廓时自行连接最后一个点和第一个点。

### 三维点

```json
{
  "x": 0.0,
  "y": 0.0,
  "z": 0.0
}
```

### Cp 分布点

```json
{
  "x": 0.0,
  "y": 0.0,
  "cp": -0.5
}
```

单位：

- `cp`：无量纲。

Cp 分布固定返回 200 个点，与二维翼型点按索引一一对应，即 `cp_distribution[i]` 对应 `airfoil_points[i]`。

### 压力场点

```json
{
  "x": 0.0,
  "y": 0.0,
  "z": 0.0,
  "pressure": 101325.0
}
```

单位：

- `pressure`：Pa。

### 速度场点

```json
{
  "x": 0.0,
  "y": 0.0,
  "z": 0.0,
  "velocity": 30.0
}
```

单位：

- `velocity`：m/s。

第一版速度场只返回标量 `velocity`，不返回 `u/v/w` 三分量。

### 强度结果

```text
max_stress: number, unit: Pa
weight: number, unit: N
```

重量字段统一使用 `weight`，单位为 N。

第一版 API 不暴露 `mass` 字段。若未来真实模型输出质量 `mass`，模型适配层必须在内部按 `weight = mass * g` 转换为重量后再返回，默认 `g = 9.80665 m/s^2`。第一版占位模型直接输出单位为 N 的 `weight`。`g` 的默认值统一由 `config/settings.py` 管理。

### 结果元信息

所有生成、预测和优化响应长期保留结果元信息：

```text
is_stub: boolean
model_version?: string
```

第一版占位结果统一返回：

```text
is_stub: true
model_version: "stub-v0"
```

未来接入真实模型后，`is_stub` 改为 `false`，并返回真实模型版本，例如 `model_version: "aero-ld-v1.2"`。不要移除 `is_stub`，它是结果可信度边界的一部分。

## 6. API 契约

### 健康检查

```text
GET /health
```

输出：

```text
status
version
```

### 二维翼型生成

```text
POST /geometry/airfoil-2d
```

输入：

```text
cst_params: number[12]
```

输出：

```text
points: 200 个 {x, y}
is_stub: true
```

### 三维机翼生成

```text
POST /geometry/wing-3d
```

输入：

```text
cst_params: number[12]
wing_planform:
  span?: number
  chord?: number
structure_design:
  spar_thickness: number
  skin_thickness: number
  rib_spacing: number
```

输出：

```text
points: 1000 个 {x, y, z}
is_stub: true
```

### 气动预测

```text
POST /aerodynamics/predict
```

输入：

```text
cst_params: number[12]
condition:
  mach: number
  angle_of_attack: number
```

输出：

```text
lift_drag_ratio: number
cp_distribution: 200 个 {x, y, cp}
field_artifact: HDF5 artifact 元信息
is_stub: true
```

压力场和速度场不直接通过 JSON 返回，而是写入 HDF5 artifact。不同翼型或机翼设计样本对应的空间坐标点可能不同，因此 artifact 内必须保存该设计样本自己的坐标数据，不能假设存在全局默认坐标。

### 强度预测

```text
POST /structure/predict
```

输入：

```text
cst_params: number[12]
condition:
  mach: number
  angle_of_attack: number
wing_planform:
  span?: number
  chord?: number
structure_design:
  spar_thickness: number
  skin_thickness: number
  rib_spacing: number
material_properties:
  elastic_modulus?: number
  material_density?: number
```

输出：

```text
max_stress: number
weight: number
is_stub: true
```

### 单一气动优化

```text
POST /optimization/aerodynamic
```

输入：

```text
cst_params: number[12]
condition:
  mach: number
  angle_of_attack: number
target_improvement_ratio: number, 0 < target_improvement_ratio <= 1
```

输出：

```text
original:
  cst_params
  condition
  lift_drag_ratio
optimized:
  cst_params
  condition
  lift_drag_ratio
actual_improvement_ratio
is_stub: true
```

比例字段统一使用小数表达，不使用百分数字符串。`10%` 表示为 `0.10`。
气动优化只改变 `cst_params`，不改变 `condition`。

### 单一强度优化

```text
POST /optimization/structural
```

输入：

```text
cst_params: number[12]
condition
wing_planform
structure_design
material_properties
target_reduction_ratio: number, 0 < target_reduction_ratio <= 1
```

输出：

```text
original:
  cst_params
  condition
  wing_planform
  structure_design
  material_properties
  weight
optimized:
  cst_params
  condition
  wing_planform
  structure_design
  material_properties
  weight
actual_reduction_ratio
is_stub: true
```

比例字段统一使用小数表达，不使用百分数字符串。`10%` 表示为 `0.10`。
强度优化只改变结构优化变量 `spar_thickness` 和 `rib_spacing`，不自动改变 `structure_design.skin_thickness`，也不自动改变 `material_properties` 中的 `elastic_modulus`、`material_density`。
强度优化不改变 `wing_planform`。
强度优化不改变 `condition`。

### 气动强度耦合优化

```text
POST /optimization/coupled
```

第一版耦合适应度定义：

```text
fitness = lift_drag_ratio / weight
```

其中 `lift_drag_ratio` 无量纲，`weight` 单位为 N。耦合优化目标是让 `fitness` 相对原始方案提升 `target_improvement_ratio`。

输入：

```text
cst_params: number[12]
condition
wing_planform
structure_design
material_properties
target_improvement_ratio: number, 0 < target_improvement_ratio <= 1
```

输出：

```text
original:
  cst_params
  condition
  wing_planform
  structure_design
  material_properties
  weight
  lift_drag_ratio
  fitness
optimized:
  cst_params
  condition
  wing_planform
  structure_design
  material_properties
  weight
  lift_drag_ratio
  fitness
actual_improvement_ratio
is_stub: true
```

比例字段统一使用小数表达，不使用百分数字符串。`10%` 表示为 `0.10`。
耦合优化可以改变 `cst_params`、`structure_design.spar_thickness` 和 `structure_design.rib_spacing`，但不改变 `structure_design.skin_thickness`、`condition`、`wing_planform` 和 `material_properties`。

### 教学二维翼型生成

```text
POST /teaching/airfoil-from-control-points
```

输入：

```text
camber_control_points: 2 个 TeachingControlPoint
thickness_control_points: 2 个 TeachingControlPoint
```

`TeachingControlPoint` 是教学界面用于表达中弧线或厚度分布趋势的归一化平面点，不是严格的 Bezier 或 B-spline 控制点：

```text
x: number, normalized chord position, 0 <= x <= 1
y: number, normalized value
```

第一版不承诺真实曲线算法，只保证用这些教学控制点返回结构正确的 200 个二维翼型点。

输出：

```text
points: 200 个 {x, y}
is_stub: true
```

### 教学 CST 参数反推

```text
POST /teaching/cst-from-airfoil
```

输入：

```text
points: 200 个 {x, y}
```

输出：

```text
cst_params: number[12]
is_stub: true
```

### Artifact 查询

```text
GET /artifacts/{artifact_id}
```

输出：

```text
artifact_id
status
format
path
datasets
```

## 7. Artifact 策略

### REST JSON 用途

REST JSON 用于调试、小数据和元信息。

直接 JSON 返回：

- 请求参数。
- 标量预测结果。
- 200 个二维翼型点。
- 200 个 Cp 点。
- 优化前后参数。
- Artifact 元信息。

不通过 JSON 返回：

- 压力场。
- 速度场。
- 后续更大的三维场数据。
- 耦合优化循环中的大数组。

### HDF5 全场数据

压力场、速度场等全场数据写入本地 HDF5 文件。第一版采用“同步写入、异步语义”：接口返回前同步完成 HDF5 写入，通常返回 `ready` 状态；REST 契约保留 `pending / ready / failed` 和 artifact 查询接口，为后续真正异步任务队列预留空间。

每个 HDF5 artifact 表示一个具体翼型或机翼设计样本的全场数据。不同设计样本的坐标点不保证一致，因此坐标必须随 artifact 一起保存。

第一版 artifact 只保存单个设计样本的全场数据。优化接口不保存每一代候选样本或优化历史的 HDF5 数据，只返回原始/优化后的参数、指标和提升比例。未来如果需要保存优化历史，再新增独立的 `optimization_artifact` 契约。

第一版 HDF5 dataset 布局：

```text
/coordinates
  shape: (1000, 3)
  columns: [x, y, z]

/fields/pressure
  shape: (1000,)
  unit: Pa

/fields/velocity
  shape: (1000,)
  unit: m/s
```

`/fields/pressure` 和 `/fields/velocity` 与 `/coordinates` 按行一一对应。第 `i` 个压力值和第 `i` 个速度值都对应 `/coordinates[i]`。

本地输出目录：

```text
airfoil-design-platform/backend/runtime_artifacts/
```

Artifact 状态：

```text
pending
ready
failed
```

第一版不接任务队列，也不要求实现后台写入。测试应按同步写入验证：调用预测接口后，artifact 应立即可查询，状态为 `ready`，文件存在，dataset 信息正确。

Artifact 元信息不存数据库，第一版通过同名 JSON sidecar 落盘。每个 HDF5 文件旁边必须保存一个同名 `.json` 元信息文件，`GET /artifacts/{artifact_id}` 读取 sidecar 返回元信息。

示例：

```text
runtime_artifacts/aerodynamic/example-id.h5
runtime_artifacts/aerodynamic/example-id.json
```

Artifact 元信息：

```text
artifact_id
format: hdf5
path
datasets
status
```

气动预测 artifact 示例：

```json
{
  "artifact_id": "example-id",
  "format": "hdf5",
  "path": "runtime_artifacts/aerodynamic/example-id.h5",
  "status": "ready",
  "datasets": {
    "coordinates": "/coordinates",
    "pressure_field": "/fields/pressure",
    "velocity_field": "/fields/velocity"
  }
}
```

### 内部高频数据通道

耦合循环内不使用 JSON 传递大数组。后续优先使用：

- MessagePack。
- numpy bytes。

REST 接口保留 JSON 能力用于调试。

## 8. 实现边界和变化点

### 第一版固定选择

- 后端框架：FastAPI。
- 接口风格：REST API。
- 数据校验：Pydantic。
- 测试方式：TDD。
- 算法实现：全部占位函数。
- 模型调用：不接真实神经网络。
- 优化算法：不接真实遗传算法。
- 可视化：不做真实绘图，只返回可视化所需数据。
- 前端：不做。
- 智能体：不做。
- 数据库：不做。
- 文件上传下载：不做。
- 用户权限：不做。

### 后续可能变化点

- 真实模型框架：PyTorch、ONNX、TensorRT 等。
- 优化算法：遗传算法、贝叶斯优化、多目标优化。
- 可视化形式：前端实时渲染、后端生成图片、导出文件。
- 数据存储：SQLite、PostgreSQL、对象存储、NAS。
- 智能体调度：LangGraph + DeepSeek。
- 长耗时任务是否异步化。
- 参数单位和范围是否引入更严格校验。
- 三维几何是否引入真实 CAD / 网格格式。

## 9. 外部依赖和集成边界

### 第一版可使用依赖

```text
FastAPI
Pydantic
pytest
httpx / TestClient
numpy
h5py
msgpack，可选
```

### 第一版不接入

- 真实神经网络模型文件。
- PyTorch / TensorFlow / ONNX Runtime。
- 真实遗传算法库。
- LangGraph。
- DeepSeek API。
- 数据库。
- 对象存储。
- 任务队列。
- 用户认证。
- 云服务。
- 前端。

### 未来集成边界

模型推理边界：

- 升阻比模型。
- Cp 分布模型。
- 压力场模型。
- 速度场模型。
- 应力极值模型。
- 重量模型。

优化算法边界：

- 气动遗传算法。
- 强度遗传算法。
- 耦合优化遗传算法。

Artifact 存储边界：

- 第一版本地文件系统。
- 后续可替换为 NAS、S3、MinIO 或数据库元信息 + 对象存储。

智能体边界：

- 第一版只提供 API 和 service。
- 后续 LangGraph 智能体可以把 service 或 API 包装成工具。

## 10. 目录结构

项目单独放在新目录：

```text
airfoil-design-platform/
  backend/
    README.md
    pyproject.toml

    docs/
      spec.md
      api-contracts.md
      adr/
        0001-backend-mvp-boundaries.md
        0002-artifact-storage-hdf5.md

    tests/
      test_health.py
      test_geometry_api.py
      test_aerodynamics_api.py
      test_structure_api.py
      test_optimization_api.py
      test_teaching_api.py
      test_artifacts_api.py

    runtime_artifacts/
      aerodynamic/
      structure/
      optimization/

    src/
      airfoil_platform/
        __init__.py
        main.py

        api/
          __init__.py
          health.py
          geometry.py
          aerodynamics.py
          structure.py
          optimization.py
          teaching.py
          artifacts.py

        contracts/
          __init__.py
          common.py
          geometry.py
          aerodynamics.py
          structure.py
          optimization.py
          teaching.py
          artifacts.py

        core/
          __init__.py
          geometry.py
          aerodynamics.py
          structure.py
          optimization.py
          teaching.py

        services/
          __init__.py
          geometry_service.py
          aerodynamic_service.py
          structure_service.py
          optimization_service.py
          teaching_service.py
          artifact_service.py

        models/
          __init__.py
          aerodynamic_models.py
          structure_models.py
          model_registry.py

        optimization/
          __init__.py
          genetic_algorithm.py
          objectives.py

        artifacts/
          __init__.py
          hdf5_store.py
          artifact_registry.py

        serialization/
          __init__.py
          msgpack_codec.py
          numpy_codec.py

        config/
          __init__.py
          settings.py

        lib/
          __init__.py
          ids.py
          paths.py
          numeric.py
```

### 目录职责

- `api/`：FastAPI 路由，只做请求响应和调用 service。
- `contracts/`：Pydantic 数据契约，请求模型、响应模型、字段单位、校验。
- `core/`：翼型、气动、强度、优化的纯领域逻辑。
- `services/`：业务工作流编排。
- `models/`：神经网络模型适配层，第一版为 stub。
- `optimization/`：遗传算法、目标函数、停止条件，第一版为 stub。
- `artifacts/`：HDF5 artifact 代码。
- `backend/runtime_artifacts/`：HDF5 运行时输出文件，应由 `.gitignore` 忽略。
- `serialization/`：MessagePack / numpy bytes 编解码边界。
- `config/`：默认值和路径配置，是默认材料属性、重力加速度、artifact 根目录和 stub 模式的事实源。
- `lib/`：通用基础工具，只放脱离翼型业务也有意义的代码。

`contracts` 与 `models` 的边界必须明确：

- `contracts` 是 API 数据契约。
- `models` 是机器学习模型适配层。

## 11. 风险点

第一版需要优先用测试保护以下风险：

- `cst_params` 必须正好 12 个。
- `cst_params` 顺序必须固定为前 6 个上表面系数、后 6 个下表面系数。
- 工况参数单位固定。
- 强度预测、强度优化和耦合优化的对象是三维机翼，必须显式处理 `wing_planform` 或配置默认机翼尺度。
- 结构设计参数和材料属性边界不能混；`skin_thickness` 属于结构设计参数，不属于材料属性。
- 结构设计参数不等于结构优化变量；第一版结构优化变量只包含 `spar_thickness` 和 `rib_spacing`。
- `weight` 统一表示重量，单位 N。
- 第一版 API 不暴露 `mass`；若未来模型输出质量 kg，必须在模型适配层转换为 `weight`。
- 默认材料属性、重力加速度、artifact 根目录和 stub 模式必须统一从 `config/settings.py` 读取，不能散落硬编码。
- 速度场第一版是标量 `velocity`。
- 压力场和速度场不能误走 JSON。
- 所有生成、预测和优化响应必须长期保留 `is_stub`；第一版占位结果返回 `is_stub: true` 和 `model_version: "stub-v0"`。
- HDF5 artifact 状态、路径、dataset 信息必须稳定。
- HDF5 artifact 必须有同名 JSON sidecar 保存元信息，不能只依赖内存 registry。
- HDF5 artifact 必须保存设计样本自己的 `/coordinates`，压力场和速度场不得依赖全局默认坐标。
- 第一版 artifact 只保存单个设计样本，不保存优化候选历史。
- 三维坐标系必须固定为 `x/y/z = 弦向/厚度/展向`。
- 耦合适应度第一版必须固定为 `fitness = lift_drag_ratio / weight`。
- 所有比例字段必须使用小数表达，输入范围为 `0 < ratio <= 1`，例如 `10%` 写作 `0.10`。
- 气动优化、强度优化、耦合优化的停止条件字段不能混用。
- 教学接口和工程接口不能混在同一边界里。

## 12. 任务拆分

### TDD 测试策略

第一版 TDD 以 API 行为测试为主，service/core 测试为辅。每个核心接口至少有一个通过 FastAPI TestClient 的行为测试，验证请求、响应字段、数量、单位契约、`is_stub`、`model_version`、artifact sidecar 和 HDF5 dataset。只有纯函数规则才单独测 core，例如 `fitness = lift_drag_ratio / weight`、比例校验、CST 顺序解析。

MVP 最终必须交付 1 到 9 的全部占位 API，但开发顺序采用 tracer bullet。每个 tracer bullet 都是一条可通过 API 测试验证的纵向切片。

推荐 tracer bullet 顺序：

1. **Backend skeleton bullet**
   - 目标：建立 FastAPI 项目骨架、`/health`、pytest/TestClient。
   - 验收：`GET /health` 成功，测试命令可运行。

2. **Common contracts bullet**
   - 目标：建立公共 contracts，包括 CST 参数、工况参数、结构设计参数、材料属性、二维/三维点、结果元信息、比例字段、artifact 元信息。
   - 验收：核心输入校验可测，包括 `cst_params` 长度、比例范围、默认材料属性。

3. **Geometry 2D bullet**
   - 目标：实现 `/geometry/airfoil-2d`。
   - 验收：输入 12 个 CST 参数，返回 200 个二维翼型点；点序符合上表面 100 个、下表面 100 个；响应包含 `is_stub: true` 和 `model_version: "stub-v0"`。

4. **Aerodynamic artifact bullet**
   - 目标：实现 `/aerodynamics/predict` 与 `GET /artifacts/{artifact_id}`。
   - 验收：返回升阻比、200 个 Cp 点、HDF5 artifact 元信息；HDF5 包含 `/coordinates`、`/fields/pressure`、`/fields/velocity`；同名 JSON sidecar 存在；压力场和速度场不走 JSON。

5. **Geometry 3D bullet**
   - 目标：实现 `/geometry/wing-3d`。
   - 验收：输入 CST 参数、机翼平面参数和完整结构设计参数，返回 1000 个三维机翼几何点；坐标系为 `x = 弦向`、`y = 厚度方向`、`z = 展向`。

6. **Structure prediction bullet**
   - 目标：实现 `/structure/predict`。
   - 验收：输入 CST 参数、工况参数、机翼平面参数、结构设计参数和可选材料属性，返回 `max_stress` 和 `weight`；`weight` 单位为 N；不暴露 `mass`。

7. **Aerodynamic optimization bullet**
   - 目标：实现 `/optimization/aerodynamic`。
   - 验收：只改变 `cst_params`，不改变 `condition`；返回原始/优化后升阻比和 `actual_improvement_ratio`。

8. **Structural optimization bullet**
   - 目标：实现 `/optimization/structural`。
   - 验收：只改变 `structure_design.spar_thickness` 和 `structure_design.rib_spacing`，不改变 `structure_design.skin_thickness`、`condition`、`wing_planform` 和 `material_properties`；返回原始/优化后 `weight` 和 `actual_reduction_ratio`。

9. **Coupled optimization bullet**
   - 目标：实现 `/optimization/coupled`。
   - 验收：可改变 `cst_params`、`structure_design.spar_thickness` 和 `structure_design.rib_spacing`，不改变 `structure_design.skin_thickness`、`condition`、`wing_planform` 和 `material_properties`；`fitness = lift_drag_ratio / weight`；返回原始/优化后 `weight`、`lift_drag_ratio`、`fitness` 和 `actual_improvement_ratio`。

10. **Teaching generation bullet**
    - 目标：实现 `/teaching/airfoil-from-control-points`。
    - 验收：输入 2 个中弧线教学控制点和 2 个厚度分布教学控制点，返回 200 个二维翼型点；教学控制点不是 Bezier/B-spline 控制点。

11. **Teaching CST inverse bullet**
    - 目标：实现 `/teaching/cst-from-airfoil`。
    - 验收：输入 200 个二维翼型点，返回 12 个 CST 参数；顺序为前 6 个上表面系数、后 6 个下表面系数。

12. **Documentation bullet**
    - 目标：补充 README、spec、api-contracts、ADR 和 `.gitignore`。
    - 验收：文档说明目标、非目标、字段单位、目录边界、artifact 策略、运行和测试命令；`runtime_artifacts/` 被忽略。

每个任务都要包含：

- 目标。
- 允许修改路径。
- 预期产物。
- 验收标准。
- 验证命令。

## 13. 完成定义

第一版完成必须满足：

- `airfoil-design-platform/backend/` 项目目录存在。
- FastAPI 应用可启动。
- `/health` 可访问。
- 1 到 9 的 API 契约存在。
- 每个核心接口有 API 行为测试。
- Artifact 测试覆盖 HDF5 文件、JSON sidecar、dataset 路径和 dataset shape。
- 占位数据流跑通。
- 压力场和速度场写入 HDF5 artifact，不走 JSON。
- 所有占位响应带 `is_stub: true` 和 `model_version: "stub-v0"`。
- 文档说明目标、非目标、字段单位、目录边界、artifact 策略、运行和测试命令。

验证命令：

```bash
cd airfoil-design-platform/backend
pytest
```

可选启动命令：

```bash
cd airfoil-design-platform/backend
uvicorn airfoil_platform.main:app --reload
```
