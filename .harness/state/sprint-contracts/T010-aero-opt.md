---
task: T010
scope: POST /optimization/aerodynamic — 只改 cst_params，不改 condition
validation: cd backend && pytest
excludes: 真实优化算法、多目标优化、耦合优化
---
