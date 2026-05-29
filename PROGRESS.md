# 项目进度

> 更新日期：2026-05-29

## 当前状态

- 最新检查点：可观测性与治理阶段三完成——运行遥测模板、多 Agent 并行化预留接口已就位。
- 测试状态：后端测试未运行（`backend/` 尚未创建）。
- 构建状态：无构建（`backend/` 尚未创建）。
- 当前 active 功能项：无。

## 已完成

- [x] `CONTEXT.md` 建立领域语言和关键歧义处理规则。
- [x] 完整后端 MVP 规格移动到 `docs/backend-mvp-full-spec.md`。
- [x] `.harness/instruction/adr/0001-store-field-data-as-hdf5-artifacts.md` 记录 HDF5 artifact 决策。
- [x] `AGENTS.md`、`PROGRESS.md`、`DECISIONS.md`、`tasks/tasks.yaml`、`docs/spec.md`、`docs/api-contracts.md` 创建完成。
- [x] `.harness/` 子系统目录（instruction/、feedback/、state/）及文件创建完成。
- [x] `.harness/instruction/rules/` 五个规则文件创建完成，规则已从 `AGENTS.md` 拆分到专题文件。
- [x] `AGENTS.md` 收缩为入口索引，不再承载详细规则。
- [x] Git 仓库初始化完成。
- [x] `AGENTS.md` 按模板优化，补充快速开始、硬约束、专题文档和会话流程章节。
- [x] `.harness/tool/tool-manifest.md` 已细化默认只读、常规可写和条件可写范围。
- [x] 50% 主动交接已补充架构决策、任务状态、待办、验证证据、阻塞项和已改文件保留清单。
- [x] 强度结构设计参数更新为 `rear_spar_web_thickness`、`rib_thickness` 和 `rib_spacing`，并同步规格、API 契约、任务清单和领域规则。
- [x] `.harness/instruction/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md` 记录结构 STEP artifact 决策。
- [x] 结构 STEP 细化为右半翼多组件结构装配，材料属性细化为 `skin` 和 `internal_structure` 两组。
- [x] 任务按原子化要求重新拆分：T000–T015 共 16 个任务，旧 T004（三合一）拆为 T004/T005/T006，旧 T005（最重单任务）拆为 T007/T008。
- [x] I/O 卫生规则（`.harness/instruction/rules/io-hygiene.md`）就位：截断、抽帧、落盘三层过滤。
- [x] 代码结构约束就位：单文件 ≤200 行、函数 ≤50 行、新增依赖需确认。
- [x] 工作状态管理约定就位：`.harness/state/working/` 目录和生命周期规则。
- [x] 知识类型/成熟度标注：`DECISIONS.md` 12 项决策标注 `[decision] [verified]`，`CONTEXT.md` 三个章节标注 `[model]`/`[pitfall]`。
- [x] 知识全景目录：`.harness/state/knowledge-index.md`（56 行，6 种知识类型，覆盖所有知识制品）。
- [x] 知识提取闭环：`session-exit-checklist.md` 新增 ARCHIVE 步骤，会话发现写入 `runs/YYYY-MM-DD-learnings.md`。
- [x] 冷启动自检：`environment.md` 新增五问题冷启动自检。
- [x] 运行遥测：`.harness/state/runs/telemetry.yaml` 模板，含单次运行记录和累积统计，`session-exit-checklist.md` 已添加遥测记录步骤。
- [x] 多 Agent 并行化预留：`tasks.yaml` 新增 `parallelizable_group` 字段，7 个任务标记为两个并行组（post-t002: T003/T004/T009/T010；post-t004: T005/T006/T007），`agent-workflow.md` 新增预留章节，`DECISIONS.md` 新增对应 ADR。

## 进行中

- [ ] 无 active 后端实现任务。

## 已知问题

- 后端依赖尚未安装。创建 `backend/pyproject.toml` 后确定安装方式。
- `backend/` 代码目录尚未创建。

## 下一步

1. 激活 `tasks/tasks.yaml` 中的 `T001 - Backend skeleton`。
2. 阅读 `.harness/state/sprint-contracts/T001-backend-skeleton.md`。
3. 创建 `backend/` 目录和最小 FastAPI 项目（`GET /health` + pytest/TestClient）。
4. 运行 `cd backend && pytest` 通过后更新 `tasks/tasks.yaml` 和本文。

## 最近验证

- 命令：`python3 -c "import yaml; ..."`
- 结果：通过；`tasks/tasks.yaml` 可解析，任务数为 16。
- 证据：命令输出 `tasks ok 16`。

- 命令：`rg -n 'elastic_modulus\\?: number|material_density\\?: number|DEFAULT_ELASTIC_MODULUS_PA|DEFAULT_MATERIAL_DENSITY_KG_M3|默认材料属性|structure_design\\.skin_thickness|structure_design\\.spar_thickness|skin_thickness: number|spar_thickness: number' docs/*.md tasks/tasks.yaml .harness/instruction/rules CONTEXT.md DECISIONS.md`
- 结果：通过；权威 Markdown 和规则文件中未发现旧材料/旧强度字段契约短语。
- 证据：命令无输出，退出码为 1（无匹配）。

- 命令：`git diff --check -- AGENTS.md CONTEXT.md DECISIONS.md PROGRESS.md docs/spec.md docs/api-contracts.md docs/backend-mvp-full-spec.md tasks/tasks.yaml .harness/instruction/rules/domain-constraints.md .harness/instruction/rules/artifact-policy.md .harness/instruction/rules/architecture-boundaries.md .harness/instruction/rules/testing.md .harness/instruction/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md`
- 结果：通过；本次文档改动无空白错误。
- 证据：命令无输出且退出码为 0。

- 命令：`python3 -c "import yaml; ..."`
- 结果：通过；`tasks/tasks.yaml` 可解析，任务数为 16，T003→T002、T008→[T007,T003]。
- 证据：命令输出 `tasks ok 16 ['T002'] ['T007', 'T003']`。

- 命令：`rg -n "structure_design\\.spar_thickness|structure_design\\.skin_thickness|points: 1000|返回 1000 个三维机翼几何点|结构优化变量第一版只包含|HDF5 artifact 存储边界|文件上传下载" docs/*.md tasks/tasks.yaml .harness/instruction/rules AGENTS.md CONTEXT.md`
- 结果：通过；权威 Markdown 和规则文件中未发现旧字段/旧点云契约短语。
- 证据：命令无输出，退出码为 1（无匹配）。

- 命令：`git diff --check -- AGENTS.md CONTEXT.md DECISIONS.md PROGRESS.md docs/spec.md docs/api-contracts.md docs/backend-mvp-full-spec.md tasks/tasks.yaml .harness/instruction/rules/domain-constraints.md .harness/instruction/rules/artifact-policy.md .harness/instruction/rules/architecture-boundaries.md .harness/instruction/rules/testing.md .harness/instruction/adr/0002-generate-structural-wing-geometry-as-step-artifacts.md`
- 结果：通过；本次规格和规则改动无空白错误。
- 证据：命令无输出且退出码为 0。

- 命令：`python3 -c "import yaml; ..."`
- 结果：通过；`tasks/tasks.yaml` 可解析，16 个任务均包含 `behavior/status/evidence`。
- 证据：`tasks/tasks.yaml` 第 1–25 行 workflow 和 feature_schema 定义完整。

- 命令：`test -f .harness/instruction/rules/agent-workflow.md ...`（五个规则文件）
- 结果：通过；五个规则文件和核心 harness 文件均存在。
- 证据：`.harness/instruction/rules/` 目录含 agent-workflow.md、domain-constraints.md、testing.md、artifact-policy.md、architecture-boundaries.md。

- 命令：后端测试 `cd backend && pytest`
- 结果：未运行。
- 证据：`backend/` 尚未创建，无测试可运行。

- 命令：`rg -n "60%|50%|上下文" .harness DECISIONS.md PROGRESS.md AGENTS.md`
- 结果：通过；`.harness` 与 `DECISIONS.md` 中的主动交接阈值已统一为 50%，仅决策记录中保留 60% 作为否决方案说明。
- 证据：`.harness/instruction/rules/agent-workflow.md` 和 `.harness/feedback/session-exit-checklist.md` 均写明 50% 主动交接。

- 命令：`rg -n "默认只读|常规任务可写|条件可写|state/runs|state/sprint-contracts" .harness/tool/tool-manifest.md DECISIONS.md`
- 结果：通过；工具权限已拆分为默认只读、常规任务可写和条件可写，状态运行目录不再被 `.harness/` 整体只读规则覆盖。
- 证据：`.harness/tool/tool-manifest.md` 和 `DECISIONS.md` 均记录 `.harness/state/runs/`、`.harness/state/sprint-contracts/` 可写边界。

- 命令：`rg -n "主动压缩保留清单|架构决策|当前任务 ID|验证命令|阻塞项|已修改" .harness/instruction/rules/agent-workflow.md .harness/feedback/session-exit-checklist.md`
- 结果：通过；50% 主动交接和 `/compact` 的最低保留内容已覆盖架构决策、任务状态、待办、验证证据、阻塞项和已改文件。
- 证据：`.harness/instruction/rules/agent-workflow.md` 有主动压缩保留清单，`.harness/feedback/session-exit-checklist.md` 有对应检查项。

- 命令：`git diff --check -- .harness/tool/tool-manifest.md .harness/instruction/rules/agent-workflow.md .harness/feedback/session-exit-checklist.md DECISIONS.md PROGRESS.md`
- 结果：通过；本次文档改动无空白错误。
- 证据：命令无输出且退出码为 0。

- 命令：`python3 -c "import yaml; ..."` 验证 `tasks.yaml` 可解析、`parallelizable_group` 字段正确、两组内代码路径互不相交
- 结果：通过；16 个任务可解析，7 个任务标记为并行组（post-t002: T003/T004/T009/T010，post-t004: T005/T006/T007），组内 backend/ 路径无重叠。
- 证据：`tasks ok 16`，post-t002 组内 6 对代码路径全部 disjoint，post-t004 组内 3 对代码路径全部 disjoint。
