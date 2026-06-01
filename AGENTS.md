# 翼型气动与强度智能设计平台 Agent 入口

本文是本仓库的 agent 入口文件，只做路由，不承载详细规则、命令或领域硬约束。

## 项目概览

"翼型气动与强度智能设计平台"后端 MVP。第一版用 FastAPI + 占位算法打通翼型生成、气动预测、强度预测、优化设计、教学接口和 HDF5/STEP artifact 存储的数据流。

## 快速开始

- 安装依赖：`cd backend && python3.10 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev,cad]"`
- 启动开发：`cd backend && source .venv/bin/activate && uvicorn airfoil_platform.main:app --reload`
- 运行测试：`cd backend && source .venv/bin/activate && pytest`
- 完整验证：见各任务的 `validation.commands`。

当前状态和下一步见 `PROGRESS.md`。

## 硬约束

以下规则分布在 `.harness/instruction/rules/` 中，按需读取：

- `.harness/instruction/rules/agent-workflow.md`：WIP=1、代码结构约束、工作状态管理和交接规则。
- `.harness/instruction/rules/io-hygiene.md`：工具输出截断、抽帧、落盘规则，防止上下文窗口被长输出污染。
- `.harness/instruction/rules/domain-constraints.md`：CST 参数顺序、比例字段小数表达、重量单位 N 等领域硬约束。
- `.harness/instruction/rules/testing.md`：TDD、API 行为测试、`cd backend && pytest` 标准验证命令。
- `.harness/instruction/rules/artifact-policy.md`：HDF5/STEP 存储、JSON sidecar、同步写入异步语义和下载接口。
- `.harness/instruction/rules/architecture-boundaries.md`：目录职责和依赖方向，`api` 不写业务逻辑，`lib` 不依赖业务层。

涉及 API 变更必须更新对应测试。不要绕过既有架构边界；需要例外时先在 `DECISIONS.md` 记录决策。

## 专题文档

- `CONTEXT.md`：领域语言、字段边界和已解决歧义——**按需读取**，遇到不认识的术语时查阅。
- `docs/spec.md`：后端 MVP 规格摘要。
- `docs/api-contracts.md`：API 输入输出契约摘要。
- `docs/backend-mvp-full-spec.md`：完整后端 MVP 原始规格。
- `docs/adr/`：架构决策记录。
- `.harness/instruction/`：规则文件（rules/）。
- `.harness/feedback/`：会话退出检查清单。
- `.harness/state/`：冲刺合同和会话运行记录。
- `.harness/environment/`：环境声明和启动脚本。
- `.harness/tool/`：pre-commit 自动检查脚本。

## 会话流程

0. **环境自检**：确认 Python ≥3.10、`.venv/` 已激活、`fastapi` 可导入。任一不满足先搭建环境（见 `.harness/environment/environment.md`）。
1. 读取 `PROGRESS.md`、`DECISIONS.md`、`tasks/tasks.yaml`。`CONTEXT.md` 按需查阅。
2. 确认当前 `active` 任务；若无，选取下一个 `not_started` 任务。
3. 阅读/创建对应冲刺合同（`.harness/state/sprint-contracts/`），缺失则先创建。
4. 执行任务，遵守 `allowed_paths` 和 WIP=1。
5. 按 **任务完成协议** 收尾（详见 `.harness/instruction/rules/agent-workflow.md` § 任务完成协议）。

**注意**：步骤 5 的"任务完成协议"是硬性流程——包含 git commit、tracking 更新、遥测记录和自检。不可跳过，不可批量补更。
