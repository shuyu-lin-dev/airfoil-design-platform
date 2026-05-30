# 冲刺合同：T001 Backend skeleton

## 范围

- 创建 `backend/pyproject.toml`：FastAPI + uvicorn + pytest + httpx 依赖声明，`[project.optional-dependencies]` 预留 dev/cad 分组。
- 创建 `backend/README.md`：项目说明、安装命令、启动命令、测试命令。
- 创建 `backend/src/airfoil_platform/__init__.py`：空包标记。
- 创建 `backend/src/airfoil_platform/main.py`：FastAPI app 实例，`GET /health` 返回 `{"status": "ok", "version": "0.2.0"}`。
- 创建 `backend/tests/__init__.py`：空包标记。
- 创建 `backend/tests/test_health.py`：用 TestClient 验证 `/health` 返回 200、status 和 version 字段。

## 验证标准

- FastAPI 应用可被 TestClient 加载，不抛导入错误。
- `GET /health` 返回 200，响应体含 `status` 和 `version`。
- `cd backend && pytest` 通过。

## 排除项

- 不创建 contracts/、config/、api/ 等其他模块目录。
- 不引入除 fastapi、uvicorn、pytest、httpx 外的第三方依赖。
- 不做任何业务逻辑。

## 观测信号

- 日志：第一版不要求结构化日志。
- 任务轨迹：`tasks/tasks.yaml` T001.evidence 和 `PROGRESS.md` 的最近验证。

## 失败反馈格式

- WHAT：哪条命令或测试失败。
- WHY：从错误消息判断的直接原因。
- FIX：下一步应修改的文件或配置。
