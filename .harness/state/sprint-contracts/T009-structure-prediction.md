# 冲刺合同：T009 Structure prediction API

## 范围

- 新建 `api/structure.py`、`contracts/structure.py`、`core/structure.py`、`services/structure_service.py`。
- 实现 `POST /structure/predict`。
- 返回 max_stress (Pa) 和 weight (N)。
- 不暴露 mass，不依赖 STEP artifact。

## 验证标准

- 返回 max_stress (Pa) 和 weight (N)。
- weight 只包含蒙皮、前梁、后梁和翼肋。
- 可选材料属性缺省时使用 settings 默认值。
- is_stub / model_version 正确。

## 排除项

- 不接真实神经网络模型。
- 不依赖结构 STEP artifact。
