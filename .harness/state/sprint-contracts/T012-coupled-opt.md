---
task: T012
scope: POST /optimization/coupled — fitness = wing_lift_drag_ratio / weight 耦合排序
validation: cd backend && pytest
excludes: 真实多学科优化、Pareto front
---
