# 初始化契约

## 启动命令

- 安装依赖：待 `T001` 创建 `backend/pyproject.toml` 后确定。
- 启动开发服务器：`cd backend && uvicorn airfoil_platform.main:app --reload`
- 运行测试：`cd backend && pytest`
- 完整验证：第一版同运行测试，后续扩展 lint / typecheck。

## 当前状态

- 依赖状态：未安装，`backend/` 尚未创建。
- 测试框架：pytest + FastAPI TestClient（计划）。
- 示例测试：无，`T001` 将创建 `backend/tests/test_health.py`。
- Lint / 类型检查：未定义。

## 项目结构

- `AGENTS.md`：agent 入口和专题路由。
- `CONTEXT.md`：领域语言和已解决歧义。
- `PROGRESS.md`：跨会话进度。
- `DECISIONS.md`：设计决策记录。
- `tasks/tasks.yaml`：功能清单和任务契约。
- `docs/`：规格和 API 契约。
- `.harness/instruction/`：初始化契约、规则（rules/）。
- `.harness/feedback/`：完成定义和退出检查清单。
- `.harness/state/`：冲刺合同和运行记录。
- `.harness/environment/`：环境声明和启动脚本。
- `.harness/tool/`：工具权限和 CI 配置。
- `backend/`：FastAPI 后端目录（计划，尚未创建）。

## 初始化验收清单

- [ ] 从零安装成功
- [ ] 标准启动路径可用
- [ ] 至少一个示例测试通过
- [x] 任务分解文件存在（`tasks/tasks.yaml`，13 个任务）
- [x] 进度和决策工件存在（`PROGRESS.md`、`DECISIONS.md`）
