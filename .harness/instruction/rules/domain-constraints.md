# 领域约束

本文记录后端 MVP 的领域和 API 语义硬约束。领域术语以 `CONTEXT.md` 为事实源。

## CST 参数

- `cst_params` 必须正好 12 个数。
- 顺序固定：前 6 个为上表面 CST 系数，后 6 个为下表面 CST 系数。
- 第一版先不强制物理范围。

## 工况参数

- 工况参数包含 `mach` 和 `angle_of_attack`。
- `mach` 无量纲。
- `angle_of_attack` 单位为 degree。
- 优化时工况参数作为评估条件，不作为优化变量。

## 比例字段

- 比例字段必须使用小数表达。
- 有效范围为 `0 < ratio <= 1`。
- `10%` 应表达为 `0.10`，不能用 `"10%"` 或 `10`。

## 结构与材料

- 结构设计参数包含 `spar_thickness`、`skin_thickness` 和 `rib_spacing`。
- 结构优化变量第一版只包含 `spar_thickness` 和 `rib_spacing`。
- 强度优化不改变 `skin_thickness`。
- 材料属性包含 `elastic_modulus` 和 `material_density`。
- 第一版优化器不改变材料属性。

## 重量与适应度

- `weight` 表示重量，单位 N。
- 第一版 API 不暴露 `mass`。
- 若未来模型输出质量，需要在模型适配层转换为 `weight`。
- 耦合适应度第一版固定为 `fitness = lift_drag_ratio / weight`。

## 结果元信息

- 所有生成、预测和优化响应长期保留 `is_stub` 和 `model_version`。
- 第一版占位响应统一使用 `is_stub: true` 和 `model_version: "stub-v0"`。

