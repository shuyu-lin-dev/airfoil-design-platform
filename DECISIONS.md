# 设计决策

本文记录项目的关键设计决策。每条决策标注日期和状态。

详细决策记录见 `docs/adr/`：

- [ADR 0001](docs/adr/0001-store-field-data-as-hdf5-artifacts.md) — HDF5 格式存储气动场数据 artifact
- [ADR 0002](docs/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md) — 三维机翼结构几何生成为 STEP artifact
- [ADR 0003](docs/adr/0003-factory-pattern-for-models-and-optimization.md) — `models/` 和 `optimization/` 采用工厂模式
- [ADR 0004](docs/adr/0004-harness-project-internal-documentation-system.md) — Harness 架构：项目内文档系统
- [ADR 0005](docs/adr/0005-multi-agent-parallelization-task-model.md) — 多 Agent 并行化任务模型预留
- [ADR 0006](docs/adr/0006-code-structure-constraints-and-enforcement.md) — 代码结构约束与自动化执行

## 补充决策

### 2026-05-30 — 任务激活时同步更新 PROGRESS.md

**决策**：在 `agent-workflow.md` 工作规则中增加约束——任务激活时（status 从 `not_started` 变为 `active`）必须同步更新 `PROGRESS.md` 的「当前 active 功能项」和「当前状态」。

**原因**：T001 执行过程中发现，任务在 `tasks.yaml` 中标记为 `active` 后，`PROGRESS.md` 未同步更新，导致外部观测者无法通过该文件感知当前 WIP。`PROGRESS.md` 是会话启动流程的首要读取文件，其信息必须与 `tasks.yaml` 保持同步。

**影响**：任务生命周期的三个关键节点均需更新 `PROGRESS.md`——激活时、完成时、阻塞时。

### 2026-05-30 — 任务激活时 PROGRESS.md 更新范围补全

**决策**：原规则只提到更新「当前 active 功能项」和「当前状态」，但遗漏了「进行中」。T002 激活时因未更新「进行中」导致该字段仍显示"无"，与 active 状态不一致。规则已补全为三个位置。

**原因**：这三个字段各自独立对观测者有意义，缺一个就会造成信息不一致。

**影响**：`agent-workflow.md` 对应条目已更新。

### 2026-05-30 — Bash 权限规则前缀匹配失效问题

**决策**：项目 `.claude/settings.json` 中的 Bash 权限规则采用前缀匹配。当 agent 执行的命令含 `cd backend &&` 前缀时，无法命中以 `source .venv/bin/activate &&` 起手的规则。解决方式：(1) 利用 CWD 持久性，先 `cd` 到 `backend/`，后续命令直接从 `source .venv/bin/activate &&` 起手；(2) 补 `cd backend &&` 前缀的规则作为兜底。

**原因**：`cd backend && source .venv/bin/activate && pytest --tb=short 2>&1` 无法匹配 `Bash(source .venv/bin/activate && pytest *)`，因为规则从命令首字符开始做前缀匹配，`cd` 破坏了前缀。每次执行都要人批权限。

**影响**：`.claude/settings.json` 已补 `cd backend && source .venv/bin/activate && *` 系列规则。agent 工作流规则中增加约定——后端测试/启动命令统一先 `cd backend` 改变 CWD，再执行无需 cd 前缀的命令。

### 2026-05-30 — Bash 权限规则覆盖缺口补全（三层根因）

**决策**：T003 执行过程中发现，即使已修复 `cd backend &&` 前缀问题，仍有 8 条命令触发人工审批。根因有三层：

1. **无 wildcard 后缀的规则被 `2>&1` 破坏**：`Bash(python3.10 --version)` 无法匹配 `python3.10 --version 2>&1`，因为规则不含 `*` 后缀，`2>&1` 被视为命令的一部分导致前缀匹配失败。修复：所有固定命令规则追加 `*` 后缀。
2. **缺少 `timeout` 前缀规则**：`timeout 3 uvicorn ...` 和 `source .venv/bin/activate && timeout 3 uvicorn ...` 无任何规则覆盖。修复：新增 `Bash(timeout *)` 和 `Bash(source .venv/bin/activate && timeout *)`。
3. **缺少基础开发工具规则**：`ls`、`pwd`、`find`、`grep`、`wc`、`cat`、`test`、`echo` 等日常开发命令无覆盖，每次均需审批。修复：新增上述命令的允许规则。

**原因**：上一轮修复只关注了 `cd backend &&` 前缀问题（CWD 层），未审查规则覆盖度（规则完备性层）和 wildcard 使用规范（匹配语义层）。三层独立但叠加作用，导致实际体验改善有限。

**影响**：`.claude/settings.json` 新增 17 条规则，覆盖 venv 激活后的 timeout 命令、python3.10 所有子命令和常用开发工具命令。规则总数从 34 增至 51。

### 2026-05-31 — Harness 精简：T003 复盘驱动的一轮清理

**决策**：基于 T003 执行复盘，识别出 harness 中 13/22 文件存在冗余/过期/错误信息。执行以下清理：

- **删除 3 个文件**：`tool-manifest.md`（含错误 auto-allow 声明且与 settings.json 不同步）、`knowledge-index.md`（与 AGENTS.md 冗余）、`_TEMPLATE-light.md`（从未被使用）。
- **归档 2 个文件**：`template-compliance.md` → `.harness/state/runs/`（一次性审计记录）；`bootstrap-contract.md` → `.harness/state/runs/2026-05-27-bootstrap-contract.md`（项目 genesis 历史参考，非活跃指导）。
- **恢复并重定义 1 个文件**：`definition-of-done.md` 恢复为质量门槛文档，与 `agent-workflow.md` 完成协议形成互补——完成协议定义执行步骤，DoD 定义完成标准。
- **修正 3 处不一致**：agent-workflow.md Python 版本 3.11→3.10；完成协议 9→10 步（增加"提交状态"步骤以反映实际的双 commit 模式）；tasks.yaml checklist "单任务单 commit"→"代码变更单 commit + 状态文件 chore commit"。
- **新增 allowed_paths 检查门**：`pre-commit-check.py` 增加 `check_allowed_paths()`，在 commit 时对活跃任务的 staged files 做 allowed_paths 匹配检查（warn-only，暂不阻断）。

**原因**：T003 复盘暴露了三个问题——(1) 条件规则文件（io-hygiene/artifact-policy）被误判为 dead，但实际属于"本轮未激活"；(2) `allowed_paths` 靠文字规则约束，无自动执行，T003 commit 实际触碰了未在允许列表的 `__init__.py` 和 sprint contract；(3) `tool-manifest.md` 包含错误信息（声称 ls/find/grep 等已 auto-allow）。

**影响**：harness 活跃文件从 22 减至 17 个（不含 runs/ 归档和 __pycache__），AGENTS.md 专题文档索引同步更新。agent-workflow.md "唯一事实源"表述改为定义三大互补文档的角色。pre-commit hook 新增 allowed_paths warn-only 检查。

### 2026-06-01 — pre-commit allowed_paths 从软提醒升级为阻断

**决策**：pre-commit hook 改为每次 commit 都运行，并由脚本自行读取所有 staged files；`check_allowed_paths()` 对 active task 范围外文件返回非零值，阻断提交。移除 `.harness/` 整体白名单，仅保留流程追踪文件、runs 记录和文档 ADR 等小范围白名单。各任务的 `allowed_paths` 补充对应 `.harness/state/sprint-contracts/T00X-*.md`。

**原因**：T003 后的 warn-only 只能提示，不能防止越界提交；同时 `.harness/` 整体放行会绕过任务范围约束。sprint contract 是任务生命周期文件，应明确纳入任务范围，而不是依赖宽泛白名单。

**影响**：后续 active task 若 staged 了未列入 `allowed_paths` 且不属于流程白名单的文件，pre-commit 将失败。无 active task 时允许 harness 维护类提交继续进行。

### 2026-06-01 — API 测试改用项目内同步 ASGI 测试客户端

**决策**：后端 API 行为测试不再直接依赖 Starlette `TestClient`，改用 `backend/tests/api_client.py` 中的最小同步 ASGI 客户端。依赖范围同步收紧为 `fastapi>=0.110,<0.116`、`starlette>=0.37.2,<0.42`、`httpx>=0.27,<0.28`、`anyio>=3.7,<4`。

**原因**：当前环境中 `anyio.from_thread.start_blocking_portal().call(...)` 会超时

### 2026-06-01 — cadquery Assembly 导出使用 save() 而非 exporters.export()

**决策**：`geometry_service.py` 中的 `_save_assembly_and_sidecar()` 使用 `assy.save(path)` 导出 STEP，而不是 `cq.exporters.export(assy, path)`。cadquery 2.7 中 `exporters.export()` 的 DispatchError 不支持 Assembly 类型的 multi-compound 导出。

**原因**：`cq.exporters.export()` 期望单个 Shape/Workplane 对象，Assembly 内部以 tuple 形式组织子组件，exporter 无法识别。`save()` 方法虽在 2.7 中标记 FutureWarning，但目前是唯一能保留组件名称的 Assembly STEP 导出方式。

**影响**：后续 cadquery 版本升级时需关注 `save()` 的替代方案（如 `exportAssembly()` 独立 API）。，Starlette `TestClient` 依赖该线程桥，导致 `TestClient(app).get("/health")` 挂住。直接 ASGI 调用可覆盖项目当前需要的 API 行为测试，不引入线程桥。

**影响**：现有 health 和 geometry API 测试恢复为稳定快速回归。后续新增 API 测试优先复用项目内 `SyncASGIClient`；若未来需要 WebSocket、streaming 或 lifespan 语义，再单独扩展测试客户端或重新评估 Starlette TestClient。
