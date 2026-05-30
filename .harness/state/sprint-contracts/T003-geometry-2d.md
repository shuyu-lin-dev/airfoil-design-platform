---
task: T003
scope: POST /geometry/airfoil-2d — 12 个 CST 参数 → 200 个二维翼型点
validation: cd backend && pytest
excludes: 三维几何、真实 CFD、CAD kernel
---
