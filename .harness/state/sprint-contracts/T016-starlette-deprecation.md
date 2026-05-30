---
task: T016
scope: pyproject.toml dev deps httpx→httpx2，消除 StarletteDeprecationWarning
validation: cd backend && pytest，零 StarletteDeprecationWarning
excludes: 不涉及业务代码变更
---
