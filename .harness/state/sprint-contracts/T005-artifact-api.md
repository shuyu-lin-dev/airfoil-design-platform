---
task: T005
scope: GET /artifacts/{id} + GET /artifacts/{id}/download — 元信息查询和文件下载
validation: cd backend && pytest
excludes: artifact 写入（由 T004/T007 承担）
---
