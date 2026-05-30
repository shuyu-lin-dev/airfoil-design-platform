---
task: T006
scope: POST /aerodynamics/predict — 升阻比 + Cp 分布 + HDF5 场数据 artifact
validation: cd backend && pytest
excludes: 真实神经网络、三维气动、优化循环
---
