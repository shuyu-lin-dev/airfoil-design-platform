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
- 默认内置 1000 个二维坐标点，调用压力场神经网络模型得到压力场分布。
- 默认内置 1000 个二维坐标点，调用速度场神经网络模型得到速度场分布。

第一版中升阻比、Cp、压力场、速度场都由占位逻辑独立生成，不要求 Cp 表面值与 HDF5 场数据之间存在物理自洽关系。

### 3. 单一气动优化

输入 12 个 CST 参数、2 个工况参数和优化幅度，例如 10%。工况参数作为评估条件传入优化算法，用于调用神经网络模型计算升阻比，但不作为优化变量。当优化后翼型的升阻比与原始翼型的升阻比相比提升 10% 后，输出：

- 优化后的 12 个 CST 参数。
- 原始评估工况参数。
- 原始翼型的升阻比。
- 优化后的升阻比。

第一版只实现占位优化流程。

### 4. 三维机翼生成

输入 12 个 CST 参数、机翼平面参数和完整结构设计参数，生成可下载和导出的结构 STEP artifact。结构 STEP 覆盖蒙皮、前梁、后梁和翼肋，必须是 CAD/网格工具可打开的有效几何；第一版不再返回 1000 个三维点云。

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

输入 12 个 CST 参数、2 个工况参数、机翼平面参数、结构设计参数、材料属性和优化幅度，例如 10%。工况参数作为评估条件传入优化算法，但不作为优化变量。调用遗传算法，当气动与强度耦合适应度提升 10% 后优化停止。第一版耦合适应度定义为 `fitness = wing_lift_drag_ratio / weight`，输出：

- 优化后的 12 个 CST 参数。
- 原始评估工况参数。
- 优化后的结构设计参数。
- 原始机翼的重量、三维升阻比和适应度。
- 优化后的重量、三维升阻比和适应度。

第一版只实现占位耦合优化流程。

### 8. 辅助教学二维翼型生成

通过输入两个中弧线教学控制点坐标和两个厚度分布教学控制点坐标，输出 200 个二维翼型 `xy` 几何坐标点。

第一版只实现占位教学生成逻辑。

### 9. 辅助教学翼型 CST 参数生成

通过输入 200 个二维翼型 `xy` 几何坐标点，输出 12 个 CST 参数。

第一版 CST 反推 stub 忽略输入翼型点，始终返回同一组固定的 12 个 CST 参数。

### 10. 智能体调度

长期目标中使用 LangGraph 编写智能体调度，使用 LLM 调用 DeepSeek 模型 API 进行对话，理解用户需求，例如预测、优化、提问等，并根据用户需求按 ReAct 模式自动调用上述工具。

智能体调度不进入第一版 MVP。

## 4. MVP 范围

### 第一版包含

- FastAPI 后端项目骨架。
- REST API 输入输出契约。
- TDD 测试。
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
- 文件上传。

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

结构设计参数描述三维机翼中由用户显式输入并可参与结构优化的梁和肋几何。三维机翼生成、强度预测、强度优化和耦合优化都接收完整的 `structure_design`。

```text
rear_spar_web_thickness: number
rib_thickness: number
rib_spacing: number
```

单位均为 m，且三个字段全部必填，不提供默认值。

硬校验范围：

```text
0.002 <= rear_spar_web_thickness <= 0.020
0.002 <= rib_thickness <= 0.005
0.300 <= rib_spacing <= 1.000
```

`rib_spacing` 表示最大目标肋距，不表示最终精确肋距。第一版必须布置翼根翼肋和半翼翼尖翼肋；翼肋数量基于 `semi_span = span / 2`，按 `floor(semi_span / rib_spacing) + 1` 取初值，若最后一个翼肋不在半翼翼尖则增加翼尖翼肋，并令 `actual_rib_spacing = semi_span / (rib_count - 1)`。实际均匀肋距必须小于或等于请求的 `rib_spacing`。

固定和派生结构假设：

```text
front_spar_web_thickness = 1.5 * rear_spar_web_thickness
skin_thickness = 0.0015 m
front_spar_chord_fraction = 0.15
rear_spar_chord_fraction = 0.70
```

`front_spar_web_thickness`、`skin_thickness`、`front_spar_chord_fraction` 和 `rear_spar_chord_fraction` 不作为请求字段或优化变量。

### 结构优化变量

结构优化变量是强度优化第一版允许改变的结构设计参数子集。第一版优化：

```text
rear_spar_web_thickness
rib_thickness
rib_spacing
```

优化后的结构设计参数必须仍落在结构尺寸硬校验范围内。

### 机翼平面参数

机翼平面参数描述三维机翼的基础尺度。强度预测、强度优化和耦合优化的对象是三维机翼；`cst_params` 只定义二维翼型截面。第一版可由用户覆盖 `span` 和 `chord`，否则使用配置默认值。

```text
span?: number
chord?: number
```

`span` 表示全展长，单位为 m。第一版结构 STEP 只生成右半翼，展向坐标范围为 `0 <= z <= span / 2`。`chord` 表示沿展向恒定弦长，单位为 m；第一版采用矩形直半翼假设，锥度比固定为 1.0，后掠角、上反角和扭转角固定为 0。字段名不带单位后缀。

硬校验范围：

```text
0 < span <= 100
0 < chord <= 20
```

出现时，`span` 和 `chord` 必须是有限正数。

默认值：

```text
DEFAULT_WING_SPAN = 10.0
DEFAULT_WING_CHORD = 1.0
```

这些默认值统一由 `config/settings.py` 管理。

### 材料属性

材料属性参与强度和重量预测，但第一版不作为结构几何。第一版区分蒙皮材料和内部结构材料；内部结构材料统一作用于前梁、后梁和翼肋。

```text
material_properties?:
  skin?:
    elastic_modulus: number
    material_density: number
  internal_structure?:
    elastic_modulus: number
    material_density: number
```

默认值：

```text
DEFAULT_SKIN_ELASTIC_MODULUS_PA = 70_000_000_000
DEFAULT_SKIN_MATERIAL_DENSITY_KG_M3 = 2700
DEFAULT_INTERNAL_STRUCTURE_ELASTIC_MODULUS_PA = 200_000_000_000
DEFAULT_INTERNAL_STRUCTURE_MATERIAL_DENSITY_KG_M3 = 7850
```

蒙皮默认材料为铝合金，内部结构默认材料为结构钢。`material_properties` 整体可省略；`skin` 和 `internal_structure` 可单独覆盖，但出现的材料组必须同时提供 `elastic_modulus` 和 `material_density`，且值必须为严格正数（`> 0`）。这些默认值统一由 `config/settings.py` 管理，业务代码不得在 service、model 或 core 中重复硬编码。

单位：

- `rear_spar_web_thickness`：m。
- `rib_thickness`：m。
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

三维点用于场数据坐标等数值数据。第一版三维机翼生成不返回三维点云，而是返回结构 STEP artifact。

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
  "pressure": 101325.0
}
```

压力场点是翼型周围二维流场中的采样点，不含展向坐标。单位：

- `pressure`：Pa。

### 速度场点

```json
{
  "x": 0.0,
  "y": 0.0,
  "velocity": 30.0
}
```

速度场点是翼型周围二维流场中的采样点，不含展向坐标。单位：

- `velocity`：m/s。

第一版速度场只返回标量 `velocity`，不返回 `u/v/w` 三分量。

### 强度结果

```text
max_stress: number, unit: Pa
weight: number, unit: N
```

`max_stress` 表示整个结构装配的最大等效应力标量，第一版不返回部件级应力分解或结构应力场 artifact。

重量字段统一使用 `weight`，单位为 N。第一版 `weight` 表示全翼结构重量，尽管结构 STEP 只生成右半翼；重量只包含蒙皮、前梁、后梁和翼肋，不包含燃油、载荷、发动机、舵面、紧固件、起落架、机身或其他整机重量。

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

### 错误响应格式

所有错误响应的 JSON body 必须包含 `error` 对象，其中 `message` 描述错误原因，`resolution` 给出可操作的解决建议：

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "具体错误描述",
    "resolution": "如何修复该错误的可操作建议"
  }
}
```

校验失败（HTTP 422）也使用此格式包装 Pydantic 校验细节。

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
  rear_spar_web_thickness: number
  rib_thickness: number
  rib_spacing: number
```

输出：

```text
geometry_artifact:
  artifact_id: string
  status: pending | ready | failed
  format: step
  role: structural_step
  path: string
  components: [skin, front_spar, rear_spar, ribs]
is_stub: true
```

第一版返回结构 STEP artifact，不返回 1000 个三维点云。STEP 必须覆盖蒙皮、前梁、后梁和翼肋，且必须是 CAD/网格工具可打开的有效几何。STEP 生成应使用 CAD kernel，首选 CadQuery/OpenCascade，备选 pythonocc-core。如果首选库在当前环境不可用，可降级到备选库，但产出 STEP 必须满足有效结构 STEP 的最低验收口径（CAD kernel 可回读、组件可识别、几何非空、外包盒合理、翼肋数量正确）。不得手写 STEP 文本伪造几何。面向外流场 CFD 的干净外表面 STEP 后续单独生成，不混入第一版结构 STEP。

结构 STEP 使用矩形直半翼假设：`span` 为全展长但 STEP 只生成右半翼，`chord` 为恒定弦长。蒙皮实体沿弦向全程做内偏置：外表面由 CST 参数缩放后沿展向拉伸得到，外表面每个点沿曲面法线方向向内平移 `skin_thickness`，偏移后的点连接形成内表面。偏置结果分三段处理：

- **翼盒段（弦向 `front_spar_chord_fraction` 到 `rear_spar_chord_fraction`）**：上下表面间距较大，偏置后保持分离，形成空心蒙皮实体。此段全程每个弦向站位都必须满足上下表面间距 >= `2 * skin_thickness`，否则接口必须拒绝请求，不自动修补。
- **前缘段（弦向 0 到 `front_spar_chord_fraction`）**：前缘驻点沿法线向内偏置后，上下表面偏置面迅速交叉，交叉区域融合为实心填充体。
- **尾缘段（弦向 `rear_spar_chord_fraction` 到 1.0）**：尾缘尖点沿法线向内偏置后，上下表面偏置面迅速交叉，交叉区域融合为实心填充体。

前梁、后梁和翼肋保持独立实体，裁剪在蒙皮实体内部并接触蒙皮内表面，不做布尔融合、铆钉、胶接、开槽、倒角或连接件细节。前缘段和尾缘段的实心填充体与梁、肋之间不做裁剪交互。

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

`lift_drag_ratio` 表示二维翼型升阻比，不表示三维机翼或全机升阻比。

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
  rear_spar_web_thickness: number
  rib_thickness: number
  rib_spacing: number
material_properties?:
  skin?:
    elastic_modulus: number
    material_density: number
  internal_structure?:
    elastic_modulus: number
    material_density: number
```

第一版强度预测使用参数化输入，不要求调用方先生成结构 STEP artifact。结构 STEP 当前只用于三维机翼几何生成、下载和导出。

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
material_properties?
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
强度优化只改变结构优化变量 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`，不自动改变 `material_properties`。优化后的结构设计参数必须落在结构尺寸硬校验范围内。
强度优化不改变 `wing_planform`。
强度优化不改变 `condition`。

### 气动强度耦合优化

```text
POST /optimization/coupled
```

第一版耦合适应度定义：

```text
fitness = wing_lift_drag_ratio / weight
```

其中 `wing_lift_drag_ratio` 是展向积分后的三维机翼升阻比，`weight` 是全翼结构重量，单位为 N。`wing_lift_drag_ratio` 由耦合优化器内部通过展向积分 stub 从二维翼型升阻比和 `wing_planform` 计算得到，不作为独立 API 暴露。第一版矩形等截面直翼假设下，展向积分退化为恒等映射：`wing_lift_drag_ratio = lift_drag_ratio`。`fitness` 是第一版 MVP 排序指标，不宣称是真实全机耦合目标。耦合优化目标是让 `fitness` 相对原始方案提升 `target_improvement_ratio`。

输入：

```text
cst_params: number[12]
condition
wing_planform
structure_design
material_properties?
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
  wing_lift_drag_ratio
  fitness
optimized:
  cst_params
  condition
  wing_planform
  structure_design
  material_properties
  weight
  wing_lift_drag_ratio
  fitness
actual_improvement_ratio
is_stub: true
```

比例字段统一使用小数表达，不使用百分数字符串。`10%` 表示为 `0.10`。
耦合优化可以改变 `cst_params`、`structure_design.rear_spar_web_thickness`、`structure_design.rib_thickness` 和 `structure_design.rib_spacing`，但不改变 `condition`、`wing_planform` 和 `material_properties`。优化后的结构设计参数必须落在结构尺寸硬校验范围内。

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

第一版教学翼型生成 stub 忽略输入控制点，始终返回一套固定翼型的 200 个二维翼型点。

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
role
path
datasets?
components?
```

### Artifact 下载

```text
GET /artifacts/{artifact_id}/download
```

输出：

```text
artifact 文件内容
```

## 7. Artifact 策略

### Artifact ID 生成

`artifact_id` 由请求输入参数的规范化 JSON 序列化后取 SHA-256 前 12 字符（hex）生成。相同输入产生相同 artifact_id，天然幂等；覆盖写入，不累积重复文件。

各接口用于 hash 的输入字段：

- 气动预测：`cst_params` + `condition`（`mach`、`angle_of_attack`）。
- 三维机翼生成：`cst_params` + `wing_planform`（`span`、`chord` 使用展开后的实际值）+ `structure_design`（全部三个字段）。
- 其他接口暂不产生 artifact。

输入在序列化前先按字段名排序，数值使用 IEEE 754 双精度规范表示，确保跨平台一致。

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
- 结构 STEP 几何文件。
- 后续更大的三维场数据。
- 耦合优化循环中的大数组。

Artifact 文件内容通过 `GET /artifacts/{artifact_id}/download` 下载，元信息通过 `GET /artifacts/{artifact_id}` 查询。

### HDF5 全场数据

压力场、速度场等全场数据写入本地 HDF5 文件。第一版采用“同步写入、异步语义”：接口返回前同步完成 HDF5 写入，通常返回 `ready` 状态；REST 契约保留 `pending / ready / failed` 和 artifact 查询接口，为后续真正异步任务队列预留空间。

每个 HDF5 artifact 表示一个具体翼型或机翼设计样本的全场数据。不同设计样本的坐标点不保证一致，因此坐标必须随 artifact 一起保存。

第一版 artifact 只保存单个设计样本的数据。优化接口不保存每一代候选样本或优化历史的 HDF5/STEP 数据，只返回原始/优化后的参数、指标和提升比例。未来如果需要保存优化历史，再新增独立的 `optimization_artifact` 契约。

第一版 HDF5 dataset 布局：

```text
/coordinates
  shape: (1000, 2)
  columns: [x, y]

/fields/pressure
  shape: (1000,)
  unit: Pa

/fields/velocity
  shape: (1000,)
  unit: m/s
```

`/fields/pressure` 和 `/fields/velocity` 与 `/coordinates` 按行一一对应。第 `i` 个压力值和第 `i` 个速度值都对应 `/coordinates[i]`。坐标不包含展向维度，因为第一版气动预测是二维翼型绕流场。

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

### STEP 结构几何

三维机翼结构几何写入本地 STEP 文件。第一版结构 STEP 角色为 `structural_step`，覆盖蒙皮、前梁、后梁和翼肋，必须能被 CAD/网格工具打开，并作为后续结构网格划分的几何基础。

第一版结构 STEP 是右半翼多组件结构装配：蒙皮、前梁、后梁和翼肋保持独立实体，不布尔融合为单一实体。蒙皮实体外表面保持 CST 截面，内表面按固定蒙皮厚度向内部偏置；梁和翼肋裁剪在蒙皮实体内部并接触蒙皮内表面，不允许穿出蒙皮外表面或留下明显间隙。第一版不生成铆钉、胶接、开槽、倒角或连接件细节。

MVP 自动验收“有效结构 STEP”的最低口径是：STEP 可被 CadQuery/OpenCascade 回读；`skin`、`front_spar`、`rear_spar` 和 `ribs` 组件可识别；各组件有非零体积或有效 shape；整体外包盒满足 `x` 约为 `0..chord`、`z` 约为 `0..span / 2` 且 `y` 有正厚度范围；翼肋数量符合 `rib_spacing` 推导规则。梁/肋与蒙皮内表面精确贴合和结构网格划分成功属于几何生成目标，不作为第一版自动测试硬门槛。

第一版结构 STEP 不用于强度预测输入；强度预测仍使用参数化结构输入。面向外流场 CFD 的干净 **气动外形 STEP artifact** 后续单独生成。

结构 STEP 生成应使用 CAD kernel，优先 CadQuery/OpenCascade。不得通过手写 STEP 文本或不可用假文件满足接口。

示例：

```text
runtime_artifacts/geometry/example-id.step
runtime_artifacts/geometry/example-id.json
```

结构 STEP artifact 示例：

```json
{
  "artifact_id": "example-id",
  "format": "step",
  "role": "structural_step",
  "path": "runtime_artifacts/geometry/example-id.step",
  "status": "ready",
  "components": ["skin", "front_spar", "rear_spar", "ribs"]
}
```

### Artifact 元信息和下载

Artifact 元信息不存数据库，第一版通过同名 JSON sidecar 落盘。每个 HDF5 或 STEP 文件旁边必须保存一个同名 `.json` 元信息文件，`GET /artifacts/{artifact_id}` 读取 sidecar 返回元信息，`GET /artifacts/{artifact_id}/download` 返回文件内容。

示例：

```text
runtime_artifacts/aerodynamic/example-id.h5
runtime_artifacts/aerodynamic/example-id.json
```

Artifact 元信息：

```text
artifact_id
format: hdf5 | step
role
path
datasets?
components?
status
```

气动预测 artifact 示例：

```json
{
  "artifact_id": "example-id",
  "format": "hdf5",
  "role": "aerodynamic_field",
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
- 算法实现：预测、优化和教学逻辑为占位函数；结构 STEP 生成必须产出有效 CAD 几何。
- 占位优化行为：确定性固定微扰。
  - 气动优化：`optimized_cst_params[i] = cst_params[i] * (1 + 0.05 * (i + 1) / 12)`，升阻比按 `original_lift_drag_ratio * (1 + target_improvement_ratio)` 返回。
  - 强度优化：对每个结构优化变量向减轻重量方向微扰 3%，`optimized_weight = original_weight * (1 - target_reduction_ratio)`。
  - 耦合优化：CST 和结构变量同时微扰（规则同上），`wing_lift_drag_ratio` 由展向积分 stub 从二维升阻比和 `wing_planform` 计算，`fitness = wing_lift_drag_ratio / weight`，优化后 fitness 按 `original_fitness * (1 + target_improvement_ratio)` 返回。
  - 若 `target_improvement_ratio` 或 `target_reduction_ratio` 导致优化后参数超出硬校验范围，stub 应将参数截断到边界值。
  - `actual_improvement_ratio` / `actual_reduction_ratio` 必须反映优化前后指标的实际变化，不直接复制输入的目标比例。
- 模型调用：不接真实神经网络。
- 优化算法：不接真实遗传算法。
- 可视化：不做真实绘图，只返回可视化所需数据。
- 前端：不做。
- 智能体：不做。
- 数据库：不做。
- 文件上传：不做。
- 用户权限：不做。

### 后续可能变化点

- 真实模型框架：PyTorch、ONNX、TensorRT 等。
- 优化算法：遗传算法、贝叶斯优化、多目标优化。
- 可视化形式：前端实时渲染、后端生成图片、导出文件。
- 数据存储：SQLite、PostgreSQL、对象存储、NAS。
- 智能体调度：LangGraph + DeepSeek。
- 长耗时任务是否异步化。
- 后续是否从结构 STEP 派生 glTF、STL 或 OBJ 预览 artifact。
- 后续是否新增面向外流场 CFD 的气动外形 STEP artifact。

## 9. 外部依赖和集成边界

### 第一版可使用依赖

```text
FastAPI
Pydantic
pytest
httpx / TestClient
numpy
h5py
CadQuery / OpenCascade
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
	      geometry/
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
	          step_store.py
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
- `artifacts/`：HDF5 与 STEP artifact 代码。
- `backend/runtime_artifacts/`：HDF5 与 STEP 运行时输出文件，应由 `.gitignore` 忽略。
- `serialization/`：MessagePack / numpy bytes 编解码边界。
- `config/`：默认值和路径配置，是默认蒙皮材料、默认内部结构材料、重力加速度、artifact 根目录和 stub 模式的事实源。
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
- 结构设计参数和材料属性边界不能混；`skin_thickness` 是固定结构假设，不是请求字段或材料属性。
- 结构设计参数不等于所有固定结构假设；第一版结构优化变量包含 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`。
- 结构尺寸字段单位均为 m，字段名不带 `_m` 后缀。
- 结构尺寸参考范围是 API 硬校验边界。
- `span` 是全展长，结构 STEP 只生成右半翼。
- 第一版三维机翼平面形状是矩形直半翼，不支持锥度、后掠、上反或扭转。
- `rib_spacing` 是最大目标肋距，实际均匀肋距可小于或等于请求值。
- 三维机翼生成必须返回有效结构 STEP artifact，不返回 1000 个点云。
- 结构 STEP 生成必须使用 CAD kernel，首选 CadQuery/OpenCascade，备选 pythonocc-core，禁止手写 STEP 文本。
- 结构 STEP 是多组件结构装配，不做布尔融合；梁和翼肋必须在蒙皮内部裁剪并接触蒙皮内表面。
- 翼盒段蒙皮内偏置必须满足 `2 * skin_thickness` 约束，不满足时拒绝请求；前缘段和尾缘段偏置后上下表面相交处融合为实心填充体。
- 结构 STEP 只用于三维机翼几何生成、下载和导出；第一版强度预测不依赖 STEP。
- 结构 STEP 和气动外形 STEP 不能混用；第一版只生成结构 STEP。
- `lift_drag_ratio` 表示二维翼型升阻比，不表示三维机翼或全机升阻比。
- `weight` 统一表示全翼结构重量，单位 N，只包含蒙皮、前梁、后梁和翼肋。
- `max_stress` 表示整个结构装配的最大等效应力，不返回部件级应力。
- 第一版 API 不暴露 `mass`；若未来模型输出质量 kg，必须在模型适配层转换为 `weight`。
- 默认蒙皮材料、默认内部结构材料、重力加速度、artifact 根目录和 stub 模式必须统一从 `config/settings.py` 读取，不能散落硬编码。
- 速度场第一版是标量 `velocity`。
- 压力场和速度场不能误走 JSON。
- 所有生成、预测和优化响应必须长期保留 `is_stub`；第一版占位结果返回 `is_stub: true` 和 `model_version: "stub-v0"`。
- Artifact 状态、路径、dataset/component 信息必须稳定。
- HDF5 和 STEP artifact 必须有同名 JSON sidecar 保存元信息，不能只依赖内存 registry。
- HDF5 artifact 必须保存设计样本自己的二维 `/coordinates`（shape: `(1000, 2)`），压力场和速度场不得依赖全局默认坐标。
- Artifact 文件内容通过 `/artifacts/{artifact_id}/download` 下载，不能由元信息接口直接返回。
- 第一版 artifact 只保存单个设计样本，不保存优化候选历史。
- 三维坐标系必须固定为 `x/y/z = 弦向/厚度/展向`。
- 耦合适应度第一版必须固定为 `fitness = wing_lift_drag_ratio / weight`。
- 所有比例字段必须使用小数表达，输入范围为 `0 < ratio <= 1`，例如 `10%` 写作 `0.10`。
- 气动优化、强度优化、耦合优化的停止条件字段不能混用。
- 教学接口和工程接口不能混在同一边界里。

## 12. 任务拆分

### TDD 测试策略

第一版 TDD 以 API 行为测试为主，service/core 测试为辅。每个核心接口至少有一个通过 FastAPI TestClient 的行为测试，验证请求、响应字段、数量、单位契约、`is_stub`、`model_version`、artifact sidecar、artifact 下载、HDF5 dataset 和 STEP 文件存在性。只有纯函数规则才单独测 core，例如 `fitness = wing_lift_drag_ratio / weight`、比例校验、CST 顺序解析、结构尺寸范围校验。

MVP 最终必须交付工程核心 API 1 到 9，以及教学 API 10 到 11。开发顺序采用 tracer bullet，每个 tracer bullet 都是一条可通过 API 测试验证的纵向切片。

推荐 tracer bullet 顺序（原子化拆分后共 15 个实现任务，T000 为 harness 初始化已完成）：

1. **Backend skeleton bullet（T001）**
   - 目标：建立 FastAPI 项目骨架、`/health`、pytest/TestClient。
   - 验收：`GET /health` 成功，测试命令可运行。

2. **Common contracts bullet（T002）**
   - 目标：建立公共 contracts，包括 CST 参数、工况参数、结构设计参数、材料属性、二维/三维点、结果元信息、比例字段、artifact 元信息，以及 config/settings。
   - 验收：核心输入校验可测，包括 `cst_params` 长度、比例范围、结构尺寸范围、材料组字段完整性、默认蒙皮材料和默认内部结构材料。

3. **Geometry 2D bullet（T003）**
   - 目标：实现 `/geometry/airfoil-2d`。
   - 验收：输入 12 个 CST 参数，返回 200 个二维翼型点；点序符合上表面 100 个、下表面 100 个；响应包含 `is_stub: true` 和 `model_version: "stub-v0"`。

4. **Artifact infrastructure + HDF5 store bullet（T004）**
   - 目标：建立格式无关的 artifact_registry 和 HDF5 存储层，不暴露 HTTP API。
   - 验收：HDF5 文件可写入；JSON sidecar 同步落盘；registry 可查询 artifact 元信息；dataset 布局正确（/coordinates、/fields/pressure、/fields/velocity）。

5. **Artifact query/download API bullet（T005）**
   - 目标：实现 `GET /artifacts/{artifact_id}` 与 `GET /artifacts/{artifact_id}/download`。
   - 验收：从 JSON sidecar 读取元信息；artifact 文件可下载；元信息查询和文件下载分离。

6. **Aerodynamic prediction bullet（T006）**
   - 目标：实现 `/aerodynamics/predict`。
   - 验收：返回升阻比、200 个 Cp 点、HDF5 artifact 元信息；HDF5 包含 `/coordinates`、`/fields/pressure`、`/fields/velocity`；同名 JSON sidecar 存在；压力场和速度场不走 JSON。

7. **STEP artifact store bullet（T007）**
   - 目标：为 artifact 系统增加 STEP 格式存储支持，不涉及翼型几何生成。
   - 验收：STEP 文件可写入；JSON sidecar 同步落盘；registry 可查询 STEP artifact 的元信息和组件列表；测试使用简单 CAD 实体验证存储层。

8. **Geometry 3D bullet（T008）**
   - 目标：实现 `/geometry/wing-3d`。
   - 验收：输入 CST 参数、机翼平面参数和完整结构设计参数，返回结构 STEP artifact 元信息；STEP 文件和同名 JSON sidecar 存在；STEP 可被 CAD kernel 回读；STEP 角色为 `structural_step`，组件包含蒙皮、前梁、后梁和翼肋；组件几何非空；整体外包盒符合 `chord` 和 `span / 2`；翼肋数量符合 `rib_spacing` 推导规则；STEP 表示右半翼多组件结构装配；不返回 1000 个点云；坐标系为 `x = 弦向`、`y = 厚度方向`、`z = 展向`。

9. **Structure prediction bullet（T009）**
   - 目标：实现 `/structure/predict`。
   - 验收：输入 CST 参数、工况参数、机翼平面参数、结构设计参数和可选材料属性，返回 `max_stress` 和 `weight`；`max_stress` 表示最大等效应力；`weight` 表示全翼结构重量且单位为 N；不暴露 `mass`。

10. **Aerodynamic optimization bullet（T010）**
    - 目标：实现 `/optimization/aerodynamic`。
    - 验收：只改变 `cst_params`，不改变 `condition`；返回原始/优化后升阻比和 `actual_improvement_ratio`。

11. **Structural optimization bullet（T011）**
    - 目标：实现 `/optimization/structural`。
    - 验收：只改变 `structure_design.rear_spar_web_thickness`、`structure_design.rib_thickness` 和 `structure_design.rib_spacing`，不改变 `condition`、`wing_planform` 和 `material_properties`；优化后结构尺寸仍在硬校验范围内；返回原始/优化后 `weight` 和 `actual_reduction_ratio`。

12. **Coupled optimization bullet（T012）**
    - 目标：实现 `/optimization/coupled`。
    - 验收：可改变 `cst_params`、`structure_design.rear_spar_web_thickness`、`structure_design.rib_thickness` 和 `structure_design.rib_spacing`，不改变 `condition`、`wing_planform` 和 `material_properties`；优化后结构尺寸仍在硬校验范围内；`fitness = wing_lift_drag_ratio / weight`，其中 `wing_lift_drag_ratio` 为三维机翼升阻比、`weight` 为全翼结构重量；返回原始/优化后 `weight`、`wing_lift_drag_ratio`、`fitness` 和 `actual_improvement_ratio`。

13. **Teaching generation bullet（T013）**
    - 目标：实现 `/teaching/airfoil-from-control-points`。
    - 验收：输入 2 个中弧线教学控制点和 2 个厚度分布教学控制点，返回 200 个二维翼型点；教学控制点不是 Bezier/B-spline 控制点。

14. **Teaching CST inverse bullet（T014）**
    - 目标：实现 `/teaching/cst-from-airfoil`。
    - 验收：输入 200 个二维翼型点，返回 12 个 CST 参数；顺序为前 6 个上表面系数、后 6 个下表面系数。

15. **Documentation bullet（T015）**
    - 目标：补充 README、spec、api-contracts、ADR 和 `.gitignore`。
    - 验收：文档说明目标、非目标、字段单位、目录边界、artifact 策略、运行和测试命令；`runtime_artifacts/` 被忽略。

T003 与 T004 可并行（均只依赖 T002）；T005/T006/T007 可并行（均只依赖 T004）；T009/T010/T011 可并行（均只依赖 T002）。

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
- 工程核心 API 1 到 9 和教学 API 10 到 11 的契约都存在。
- 每个核心接口和教学接口都有 API 行为测试。
- Artifact 测试覆盖 HDF5/STEP 文件、JSON sidecar、dataset 路径、dataset shape、STEP 回读、组件/外包盒基本合理性和文件下载。
- 占位数据流跑通。
- 压力场和速度场写入 HDF5 artifact，不走 JSON。
- 三维机翼结构几何写入有效 STEP artifact，不走点云 JSON。
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
