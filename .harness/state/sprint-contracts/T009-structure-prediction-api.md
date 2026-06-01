---
task: T009
scope:
  - POST /structure/predict 返回 max_stress(Pa) 和 weight(N)
  - weight = 各组件(蒙皮/前梁/后梁/翼肋)体积×密度×g 之和
  - max_stress stub 计算基于简化梁理论
  - 可选 material_properties 缺省时使用 settings 默认值
  - 不依赖 STEP artifact
validation: cd backend && pytest
