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
  spar_thickness: number
  skin_thickness: number
  rib_spacing: number
```

输出：

```text
points: 1000 个 {x, y, z}
is_stub: true
model_version: "stub-v0"
```

约束：

- 坐标系固定为 `x = 弦向`、`y = 厚度方向`、`z = 展向`。
- 缺省机翼平面参数来自 settings。

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
  path: string
  datasets: object
is_stub: true
model_version: "stub-v0"
```

约束：

- Cp 分布与二维翼型点按索引一一对应。
- 压力场和速度场不直接通过 JSON 返回。
- HDF5 artifact 必须包含 `/coordinates`、`/fields/pressure`、`/fields/velocity`。
- 同名 JSON sidecar 必须落盘。

## GET /artifacts/{artifact_id}

输出：

```text
artifact_id: string
status: pending | ready | failed
format: hdf5
path: string
datasets: object
```

约束：

- 第一版从同名 JSON sidecar 读取元信息。
- 不依赖内存 registry 才能查询历史 artifact。

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
model_version: "stub-v0"
```

约束：

- `weight` 单位为 N。
- API 不暴露 `mass`。
- 缺省材料属性来自 settings。

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
material_properties
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
- 只改变 `structure_design.spar_thickness` 和 `structure_design.rib_spacing`。
- 不改变 `skin_thickness`、`condition`、`wing_planform` 和 `material_properties`。

## POST /optimization/coupled

输入：

```text
cst_params: number[12]
condition
wing_planform
structure_design
material_properties
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

- `fitness = lift_drag_ratio / weight`。
- 可改变 `cst_params`、`spar_thickness` 和 `rib_spacing`。
- 不改变 `skin_thickness`、`condition`、`wing_planform` 和 `material_properties`。

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
