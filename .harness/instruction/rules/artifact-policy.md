# Artifact 策略

本文定义后端 MVP 的 HDF5 artifact 规则。架构决策背景见 `.harness/instruction/adr/0001-store-field-data-as-hdf5-artifacts.md`。

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
- 后续更大的三维场数据。
- 耦合优化循环中的大数组。

## HDF5 存储

- 压力场和速度场写入 HDF5 artifact。
- 每个 HDF5 artifact 表示单个设计样本的全场数据。
- 第一版 artifact 只保存单个设计样本，不保存优化候选历史。
- 不同设计样本的坐标可能不同，因此 artifact 必须保存自己的 `/coordinates`。
- 不能依赖全局默认坐标。

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

- HDF5 artifact 必须有同名 JSON sidecar 元信息。
- `GET /artifacts/{artifact_id}` 第一版读取 sidecar 返回元信息。
- 元信息不能只依赖内存 registry。

示例：

```text
backend/runtime_artifacts/aerodynamic/example-id.h5
backend/runtime_artifacts/aerodynamic/example-id.json
```

## 状态语义

- 第一版同步写入 artifact。
- REST 契约保留 `pending / ready / failed` 状态。
- 调用预测接口返回后，测试应按同步写入验证文件已存在且状态为 `ready`。

## 运行时文件

- `backend/runtime_artifacts/` 是运行时输出目录。
- `backend/runtime_artifacts/` 应由 `.gitignore` 忽略。

