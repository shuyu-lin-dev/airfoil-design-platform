# 测试规则

本文定义后端 MVP 的测试和验证规则。

## 测试策略

- 第一版采用 TDD。
- API 行为测试优先。
- 每个核心接口至少有一个 FastAPI TestClient 行为测试。
- 纯函数规则可单独测 core，例如比例校验、CST 顺序解析、`fitness = lift_drag_ratio / weight`。
- service/core 测试服务于行为风险，不提前扩成大测试矩阵。

## 标准命令

后端目录创建后，标准验证命令是：

```bash
cd backend && pytest
```

后端目录创建后，可选启动命令是：

```bash
cd backend && uvicorn airfoil_platform.main:app --reload
```

当前 `backend/` 尚未创建时，不运行后端测试；必须在 `PROGRESS.md` 写明未运行原因。

## API 行为测试

API 测试应覆盖：

- 请求字段校验。
- 响应字段。
- 关键数组数量。
- 单位契约。
- `is_stub` 和 `model_version`。
- 优化前后不应改变的字段。

## Artifact 验证

涉及 artifact 的测试必须覆盖：

- HDF5 文件存在。
- 同名 JSON sidecar 存在。
- dataset 路径正确。
- dataset shape 正确。
- `GET /artifacts/{artifact_id}` 能通过 sidecar 返回元信息。
- 压力场和速度场不直接走 REST JSON。

## 验证记录

每次验证后，更新：

- `tasks/tasks.yaml` 中当前任务的 `evidence`。
- `PROGRESS.md` 的“最近验证”。

未运行验证时必须说明原因。

