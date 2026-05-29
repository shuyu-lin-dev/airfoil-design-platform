# API 契约摘要

> 更新日期：2026-05-27
> 完整需求原文：`docs/backend-mvp-full-spec.md`

本文记录第一版后端 API 的输入输出边界。详细字段校验以实现中的 Pydantic contracts 和测试为准。

## 通用响应元信息

所有生成、预测和优化响应都长期保留：

```text
is_stub: boolean
model_version?: string
```

第一版占位结果统一返回：

```text
is_stub: true
model_version: "stub-v0"
```

## GET /health

输出：

```text
status: string
version: string
```

## POST /geometry/airfoil-2d

输入：

```text
cst_params: number[12]
```

输出：

```text
points: 200 个 {x, y}
is_stub: true
model_version: "stub-v0"
```

约束：

- `cst_params` 正好 12 个数。
- 前 6 个为上表面 CST 系数，后 6 个为下表面 CST 系数。
- 前 100 个点为上表面，后 100 个点为下表面。

## POST /geometry/wing-3d

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
model_version: "stub-v0"
```

约束：

- 坐标系固定为 `x = 弦向`、`y = 厚度方向`、`z = 展向`。
- 缺省机翼平面参数来自 settings：`DEFAULT_WING_SPAN = 10.0`、`DEFAULT_WING_CHORD = 1.0`。
- `span` 表示全展长，单位为 m；第一版 STEP 只生成右半翼，`z` 范围为 `0 <= z <= span / 2`。
- `chord` 是恒定弦长，单位为 m；第一版为矩形直半翼，锥度比 1.0，后掠角、上反角和扭转角均为 0。
- `span` 和 `chord` 字段名不带单位后缀；出现时必须是有限正数，硬校验范围为 `0 < span <= 100`、`0 < chord <= 20`。
- `structure_design` 三个字段全部必填，单位均为 m。
- `rear_spar_web_thickness` 范围为 0.002 到 0.020。
- `rib_thickness` 范围为 0.002 到 0.005。
- `rib_spacing` 范围为 0.300 到 1.000。
- `rib_spacing` 是最大目标肋距；翼根和半翼翼尖都必须有翼肋，实际均匀肋距可小于或等于请求值。
- 前梁腹板厚度由 `rear_spar_web_thickness * 1.5` 派生。
- 蒙皮厚度固定为 0.0015 m，不作为请求字段。
- 前梁位置固定为 0.15 chord，后梁位置固定为 0.70 chord。
- 返回有效结构 STEP artifact，不返回 1000 个点云。
- STEP 生成应使用 CAD kernel，优先 CadQuery/OpenCascade。
- STEP 是多组件结构装配，蒙皮、前梁、后梁和翼肋保持独立实体，不布尔融合。
- 蒙皮外表面使用 CST 截面并按固定蒙皮厚度向内部偏置；偏置失败或局部厚度不足时返回 422。
- 梁和翼肋必须裁剪在蒙皮实体内部并接触蒙皮内表面，不生成连接件、开槽或倒角细节。
- MVP 自动验收的有效 STEP 最低口径是 CAD kernel 可回读、组件可识别、组件几何非空、整体外包盒符合 `chord` 和 `span / 2`，以及翼肋数量符合 `rib_spacing` 推导规则。

## POST /aerodynamics/predict

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
field_artifact:
  artifact_id: string
  status: pending | ready | failed
  format: hdf5
  role: aerodynamic_field
  path: string
  datasets: object
is_stub: true
model_version: "stub-v0"
```

约束：

- Cp 分布与二维翼型点按索引一一对应。
- `lift_drag_ratio` 表示二维翼型升阻比。
- 压力场和速度场不直接通过 JSON 返回。
- HDF5 artifact 必须包含 `/coordinates`、`/fields/pressure`、`/fields/velocity`。
- 同名 JSON sidecar 必须落盘。

## GET /artifacts/{artifact_id}

输出：

```text
artifact_id: string
status: pending | ready | failed
format: hdf5 | step
role: string
path: string
datasets?: object
components?: [string]
```

约束：

- 第一版从同名 JSON sidecar 读取元信息。
- 不依赖内存 registry 才能查询历史 artifact。

## GET /artifacts/{artifact_id}/download

输出：

```text
artifact 文件内容
```

约束：

- 对 STEP artifact 返回 `.step` 文件内容。
- 对 HDF5 artifact 返回 `.h5` 文件内容。
- 元信息查询和文件下载分离。

## POST /structure/predict

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

输出：

```text
max_stress: number
weight: number
is_stub: true
model_version: "stub-v0"
```

约束：

- `max_stress` 表示整个结构装配的最大等效应力，单位 Pa。
- `weight` 表示全翼结构重量，单位 N，只包含蒙皮、前梁、后梁和翼肋。
- API 不暴露 `mass`。
- 缺省材料属性来自 settings：蒙皮默认铝合金 70 GPa / 2700 kg/m^3，内部结构默认结构钢 200 GPa / 7850 kg/m^3。
- 缺省机翼平面参数来自 settings：`DEFAULT_WING_SPAN = 10.0`、`DEFAULT_WING_CHORD = 1.0`。
- `material_properties` 整体可省略；`skin` 和 `internal_structure` 可单独覆盖，但出现的材料组必须同时提供 `elastic_modulus` 和 `material_density`。
- 强度预测不依赖结构 STEP artifact。
- `structure_design` 字段和范围与 `/geometry/wing-3d` 一致。

## POST /optimization/aerodynamic

输入：

```text
cst_params: number[12]
condition:
  mach: number
  angle_of_attack: number
target_improvement_ratio: number
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
actual_improvement_ratio: number
is_stub: true
model_version: "stub-v0"
```

约束：

- `target_improvement_ratio` 满足 `0 < ratio <= 1`。
- 只改变 `cst_params`。
- 不改变 `condition`。

## POST /optimization/structural

输入：

```text
cst_params: number[12]
condition
wing_planform
structure_design
material_properties?
target_reduction_ratio: number
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
actual_reduction_ratio: number
is_stub: true
model_version: "stub-v0"
```

约束：

- `target_reduction_ratio` 满足 `0 < ratio <= 1`。
- 只改变 `structure_design.rear_spar_web_thickness`、`structure_design.rib_thickness` 和 `structure_design.rib_spacing`。
- 优化后的结构设计参数必须落在结构尺寸硬校验范围内。
- 不改变 `condition`、`wing_planform` 和 `material_properties`。

## POST /optimization/coupled

输入：

```text
cst_params: number[12]
condition
wing_planform
structure_design
material_properties?
target_improvement_ratio: number
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
actual_improvement_ratio: number
is_stub: true
model_version: "stub-v0"
```

约束：

- `fitness = wing_lift_drag_ratio / weight`，其中 `wing_lift_drag_ratio` 是展向积分后的三维机翼升阻比，`weight` 是全翼结构重量 (N)。
- 可改变 `cst_params`、`rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`。
- 优化后的结构设计参数必须落在结构尺寸硬校验范围内。
- 不改变 `condition`、`wing_planform` 和 `material_properties`。

## POST /teaching/airfoil-from-control-points

输入：

```text
camber_control_points: 2 个 TeachingControlPoint
thickness_control_points: 2 个 TeachingControlPoint
```

`TeachingControlPoint`：

```text
x: number, 0 <= x <= 1
y: number
```

输出：

```text
points: 200 个 {x, y}
is_stub: true
model_version: "stub-v0"
```

约束：

- 教学控制点只是归一化趋势点。
- 第一版不承诺 Bezier 或 B-spline 算法。

## POST /teaching/cst-from-airfoil

输入：

```text
points: 200 个 {x, y}
```

输出：

```text
cst_params: number[12]
is_stub: true
model_version: "stub-v0"
```

约束：

- 返回 12 个 CST 参数。
- 顺序为前 6 个上表面系数，后 6 个下表面系数。
