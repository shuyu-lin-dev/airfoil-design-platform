---
task: T011
scope: POST /optimization/structural — 只改结构优化变量，不改 condition/wing_planform/material
validation: cd backend && pytest
excludes: 真实优化算法、FEA 仿真
---
