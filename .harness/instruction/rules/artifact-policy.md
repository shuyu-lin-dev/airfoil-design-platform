# Artifact 策略

本文定义后端 MVP 的 HDF5 与 STEP artifact 规则。架构决策背景见 `.harness/instruction/adr/0001-store-field-data-as-hdf5-artifacts.md` 和 `.harness/instruction/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md`。

## REST JSON 边界

REST JSON 用于：

- 请求参数。
- 标量预测结果。
- 200 个二维翼型点。
- 200 个 Cp 点。
- 优化前后参数。
- Artifact 元信息。

REST JSON 不用于直接返回：

- 压力场。
- 速度场。
- 结构 STEP 几何文件。
- 后续更大的三维场数据。
- 耦合优化循环中的大数组。

Artifact 文件内容通过 `GET /artifacts/{artifact_id}/download` 下载。

## HDF5 存储

- 压力场和速度场写入 HDF5 artifact。
- 每个 HDF5 artifact 表示单个设计样本的全场数据。
- 第一版 artifact 只保存单个设计样本，不保存优化候选历史。
- 不同设计样本的坐标可能不同，因此 artifact 必须保存自己的 `/coordinates`。
- 不能依赖全局默认坐标。

## STEP 存储

- 三维机翼生成写入结构 STEP artifact，不返回 1000 个点云。
- 每个结构 STEP artifact 表示单个设计样本的结构几何。
- 结构 STEP artifact 角色为 `structural_step`，组件覆盖蒙皮、前梁、后梁和翼肋。
- 结构 STEP 只生成右半翼，采用矩形直半翼假设。
- 结构 STEP 是多组件结构装配，蒙皮、前梁、后梁和翼肋保持独立实体，不布尔融合。
- 蒙皮外表面使用 CST 截面并按固定蒙皮厚度向内部偏置。
- 梁和翼肋必须裁剪在蒙皮内部并接触蒙皮内表面。
- 结构 STEP 必须能被 CAD/网格工具打开。
- 结构 STEP 生成必须使用 CAD kernel，优先 CadQuery/OpenCascade，禁止手写 STEP 文本伪造几何。
- MVP 自动验收结构 STEP 的最低口径是 CAD kernel 可回读、组件可识别、组件几何非空、整体外包盒符合 `chord` 和 `span / 2`，以及翼肋数量符合 `rib_spacing` 推导规则。
- 梁/肋与蒙皮内表面精确贴合和结构网格划分可用性属于几何生成目标，不作为第一版自动测试硬门槛。
- 第一版结构 STEP 只用于三维机翼几何生成、下载和导出；强度预测不依赖 STEP。
- 面向外流场 CFD 的气动外形 STEP artifact 不进入第一版。

## Dataset 布局

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

`/fields/pressure` 和 `/fields/velocity` 与 `/coordinates` 按行一一对应。

## Sidecar 元信息

- HDF5 和 STEP artifact 必须有同名 JSON sidecar 元信息。
- `GET /artifacts/{artifact_id}` 第一版读取 sidecar 返回元信息。
- `GET /artifacts/{artifact_id}/download` 第一版返回 artifact 文件内容。
- 元信息不能只依赖内存 registry。

示例：

```text
backend/runtime_artifacts/aerodynamic/example-id.h5
backend/runtime_artifacts/aerodynamic/example-id.json
backend/runtime_artifacts/geometry/example-id.step
backend/runtime_artifacts/geometry/example-id.json
```

## 状态语义

- 第一版同步写入 artifact。
- REST 契约保留 `pending / ready / failed` 状态。
- 调用预测接口返回后，测试应按同步写入验证文件已存在且状态为 `ready`。

## 运行时文件

- `backend/runtime_artifacts/` 是运行时输出目录。
- `backend/runtime_artifacts/` 应由 `.gitignore` 忽略。
