# 2026-06-01 learnings

## Starlette TestClient 的 anyio 线程桥在当前环境会超时

- 现象：`TestClient(app).get("/health")` 在当前 backend venv 中超时，`pytest` 停在首个 TestClient 请求。
- 复现：`timeout 5 .venv/bin/python -c "from fastapi.testclient import TestClient; from airfoil_platform.main import app; TestClient(app).get('/health')"`。
- 线索：`faulthandler` 栈显示阻塞在 `anyio.from_thread` 的 blocking portal；单独调用 ASGI app 可以正常返回。
- 修复：收紧 FastAPI/Starlette/httpx/anyio 依赖范围，并将 API 行为测试切换到项目内 `SyncASGIClient`，避开线程桥。
- 结果：`cd backend && .venv/bin/python -m pytest` 恢复为 52 passed。
