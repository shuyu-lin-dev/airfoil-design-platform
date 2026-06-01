---
task: T007
scope:
  - write_step_artifact() 写入 STEP 到 runtime_artifacts/geometry/<id>.step
  - 同名 JSON sidecar 落盘（artifact_id/format/role/path/status/components）
  - ArtifactRegistry 可查询 STEP artifact
  - 测试使用 CadQuery 方盒验证，不涉及翼型几何
  - 不依赖任何 HTTP API
validation:
  - cd backend && pytest
exclude:
  - 不实现几何生成逻辑
  - 不提供 STEP 下载接口（T005 已覆盖）
  - 不验证 STEP 几何有效性
