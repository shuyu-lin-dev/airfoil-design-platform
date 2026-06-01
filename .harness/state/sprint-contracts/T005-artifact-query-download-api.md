---
task: T005
scope:
  - 创建 GET /artifacts/{artifact_id} 从 JSON sidecar 读取返回 artifact 元信息，不依赖内存 registry
  - 创建 GET /artifacts/{artifact_id}/download 返回 artifact 文件（HDF5）内容
  - 元信息查询和文件下载分离为两个独立端点
  - 测试通过 SyncASGIClient 验证，使用 T004 的 write_hdf5_artifact 预创建测试 artifact
  - 在 main.py 注册 artifacts router
validation:
  - cd backend && pytest
exclude:
  - 不支持 STEP 文件下载（T007 未完成）
  - 不支持范围查询、分页、过滤等高级查询
  - 不支持 Range 请求或流式传输
  - 不改动 artifacts/ 存储层代码
