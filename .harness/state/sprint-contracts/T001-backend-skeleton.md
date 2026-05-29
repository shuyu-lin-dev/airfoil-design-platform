# 冲刺合同：T001 Backend skeleton

## 范围

- 创建 `backend/` 最小 FastAPI 项目骨架。
- 创建 `GET /health`。
- 创建 pytest + TestClient 的健康检查行为测试。
- 让 `cd backend && pytest` 成为可运行验证命令。
- 更新 `tasks/tasks.yaml` 和 `PROGRESS.md`。

## 验证标准

- `backend/README.md` 存在并说明运行与测试命令。
- `backend/pyproject.toml` 存在并声明最小后端依赖。
- `backend/src/airfoil_platform/main.py` 暴露 FastAPI app。
- `backend/tests/test_health.py` 能通过 TestClient 验证 `/health`。
- `cd backend && pytest` 通过。

## 排除项

- 不实现除 `/health` 之外的业务 API。
- 不实现 HDF5 artifact。
- 不接真实模型、真实优化算法或前端。
- 不引入数据库、任务队列或认证。

## 观测信号

- 日志：第一版不要求结构化日志。
- 健康检查：`GET /health` 返回 `status` 和 `version`。
- 任务轨迹：`tasks/tasks.yaml` 的 `T001.evidence` 和 `PROGRESS.md` 的最近验证。

## 失败反馈格式

- WHAT：哪条命令或测试失败。
- WHY：从错误消息判断的直接原因。
- FIX：下一步应修改的文件或配置。

