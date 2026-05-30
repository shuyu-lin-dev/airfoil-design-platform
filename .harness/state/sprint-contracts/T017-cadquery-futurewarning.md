---
task: T017
scope: pyproject.toml pytest filterwarnings 抑制 CadQuery 内部 FutureWarning
validation: cd backend && pytest，零 FutureWarning
excludes: 不修复 CadQuery 上游代码，不引入新依赖
---
