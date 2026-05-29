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

- 结构设计参数包含 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`，单位均为 m，三个字段全部必填。
- 结构尺寸硬校验范围为：`rear_spar_web_thickness` 0.002–0.020，`rib_thickness` 0.002–0.005，`rib_spacing` 0.300–1.000。
- `rib_spacing` 表示最大目标肋距；翼根和半翼翼尖都必须布置翼肋，实际均匀肋距可小于或等于请求值。
- 前梁腹板厚度由 `rear_spar_web_thickness * 1.5` 派生，不作为请求字段或优化变量。
- 蒙皮厚度固定为 0.0015 m，不作为请求字段或优化变量。
- 前梁弦向位置固定为 0.15，后梁弦向位置固定为 0.70，不作为请求字段或优化变量。
- 结构优化变量第一版包含 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`。
- 强度优化和耦合优化后的结构设计参数必须落在结构尺寸硬校验范围内。
- 材料属性区分 `skin` 和 `internal_structure` 两组；出现的材料组必须同时提供 `elastic_modulus` 和 `material_density`。
- 蒙皮默认材料为铝合金：`elastic_modulus = 70_000_000_000 Pa`，`material_density = 2700 kg/m^3`。
- 内部结构默认材料为结构钢：`elastic_modulus = 200_000_000_000 Pa`，`material_density = 7850 kg/m^3`。
- 第一版优化器不改变材料属性。

## 三维几何与 Artifact

- 三维机翼生成返回结构 STEP artifact，不返回 1000 个点云。
- 结构 STEP artifact 必须覆盖蒙皮、前梁、后梁和翼肋，并能被 CAD/网格工具打开。
- `wing_planform.span` 表示全展长；第一版结构 STEP 只生成右半翼。
- `wing_planform.span` 和 `wing_planform.chord` 单位均为 m，字段名不带单位后缀。
- 机翼平面默认值为 `DEFAULT_WING_SPAN = 10.0` 和 `DEFAULT_WING_CHORD = 1.0`，统一来自 settings。
- `wing_planform.span` 和 `wing_planform.chord` 出现时必须是有限正数，硬校验范围分别为 `0 < span <= 100` 和 `0 < chord <= 20`。
- 第一版结构 STEP 使用矩形直半翼假设，`chord` 为恒定弦长，锥度、后掠、上反和扭转均固定。
- 结构 STEP 是多组件结构装配，蒙皮、前梁、后梁和翼肋保持独立实体，不布尔融合。
- 蒙皮外表面使用 CST 截面，按固定蒙皮厚度向内部偏置；偏置失败或局部厚度不足时必须拒绝请求。
- 梁和翼肋必须裁剪在蒙皮内部并接触蒙皮内表面，不生成连接件、开槽或倒角细节。
- 结构 STEP 生成必须使用 CAD kernel，优先 CadQuery/OpenCascade，禁止手写 STEP 文本伪造几何。
- 第一版结构 STEP 只用于三维机翼几何生成、下载和导出；强度预测不依赖 STEP。
- 面向外流场 CFD 的气动外形 STEP artifact 不进入第一版。
- Artifact 元信息通过 `GET /artifacts/{artifact_id}` 查询，文件内容通过 `GET /artifacts/{artifact_id}/download` 下载。

## 重量与适应度

- `lift_drag_ratio` 表示二维翼型升阻比。
- `weight` 表示全翼结构重量，单位 N，只包含蒙皮、前梁、后梁和翼肋。
- `max_stress` 表示整个结构装配的最大等效应力，单位 Pa。
- 第一版 API 不暴露 `mass`。
- 若未来模型输出质量，需要在模型适配层转换为 `weight`。
<!-- FACT-SOURCE: docs/spec.md line 72: fitness = wing_lift_drag_ratio / weight -->
<!-- FACT-SOURCE: docs/backend-mvp-full-spec.md §7 (气动强度耦合优化): 第一版矩形等截面直翼假设下展向积分退化为恒等映射 wing_lift_drag_ratio = lift_drag_ratio -->
- 耦合适应度第一版固定为 `fitness = lift_drag_ratio / weight`，是 MVP 排序指标。

## 结果元信息

- 所有生成、预测和优化响应长期保留 `is_stub` 和 `model_version`。
- 第一版占位响应统一使用 `is_stub: true` 和 `model_version: "stub-v0"`。
