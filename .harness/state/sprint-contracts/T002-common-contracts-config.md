---
task: T002
scope: 创建公共 Pydantic 请求响应契约（cst_params 12 数校验、比例字段 0<ratio<=1、wing_planform/结构设计参数/材料属性/结果元信息模型）和 config/settings.py 默认值。
validation: cd backend && pytest
excludes: 不创建 api/ 路由、不创建 core/ 业务逻辑、不创建 services/ 编排、不引入新第三方依赖。
---
