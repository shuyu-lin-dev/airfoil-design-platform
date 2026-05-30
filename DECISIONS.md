# 设计决策

本文记录项目和 harness 的关键决策，回答”为什么这样做”。当实现需要偏离既有规则时，先在这里补充决策，再修改代码或任务。

每条决策标注知识类型和成熟度：
- 类型：`[decision]`（ADR）、`[guideline]`（操作指南）、`[pitfall]`（陷阱/反模式）、`[process]`（流程约定）
- 成熟度：`[draft]`（提议中）、`[verified]`（已实施并验证）、`[proven]`（长期运行验证）

## [decision] [verified] 2026-05-27: 第一版先采用项目内 harness

- 背景：项目处于后端 MVP 起步阶段，当前最缺的是 agent 可读的事实源、任务边界、验证命令和跨会话状态。
- 决策：第一版不先创建项目外通用 harness，而是在当前仓库内建立 `AGENTS.md`、`PROGRESS.md`、`tasks/tasks.yaml`、`.harness/` 和 `docs/`。
- 原因：项目内 harness 更贴近当前需求，能马上约束后端 tracer bullet；通用 harness 过早抽象会把注意力从业务契约和验证闭环上移走。
- 否决方案：先在 `/home/lsy/workspace/dev/` 下创建独立 harness 项目，再反向生成本项目结构。
- 约束：项目内 harness 的规则必须足够轻量，不能变成阻碍实现的流程负担。
- 后续检查：完成 T001 到 T004 后，复盘哪些模板和校验逻辑值得抽到项目外复用。

## [decision] [verified] 2026-05-27: `CONTEXT.md` 保留在仓库根目录

- 背景：`CONTEXT.md` 记录领域语言、字段边界和已解决歧义，是 agent 冷启动最重要的项目语境。
- 决策：`CONTEXT.md` 长期保留在根目录，不移动到 `docs/`。
- 原因：根目录可发现性最高，能让新会话先建立领域词汇，再进入规格和任务。
- 否决方案：将 `CONTEXT.md` 移动到 `docs/context.md`。
- 约束：`AGENTS.md` 只做入口索引，并突出 `CONTEXT.md` 是领域语境入口。
- 后续检查：若未来根目录文件过多，可以创建根目录短入口并把长上下文迁入 `docs/`。

## [decision] [verified] 2026-05-27: 规则拆分到 `.harness/instruction/rules/`

- 背景：`AGENTS.md` 曾包含工作规则、标准命令和领域硬约束，入口文件变得过重，不符合“入口文件是路由器，细节渐进披露”的 harness 原则。
- 决策：将规则拆分到 `.harness/instruction/rules/`，并按工作流、领域、测试、artifact 和架构边界分文件维护。
- 原因：规则会随项目增长，分文件能降低冷启动阅读成本，也便于 agent 按任务类型读取相关约束。
- 否决方案：继续把所有规则放在 `AGENTS.md`，或集中到单个 `docs/constraints.md`。
- 约束：`AGENTS.md` 不承载详细规则、标准命令或领域硬约束，只保留索引。
- 后续检查：T001 完成后确认后端 README 是否需要指向 `.harness/instruction/rules/testing.md` 和 `.harness/instruction/rules/architecture-boundaries.md`。

## [decision] [verified] 2026-05-27: 完整后端规格移动到 `docs/backend-mvp-full-spec.md`

- 背景：完整后端 MVP spec 内容较长，适合放入文档目录；根目录保留入口类和状态类文件。
- 决策：完整规格文件使用 `docs/backend-mvp-full-spec.md`，`docs/spec.md` 和 `docs/api-contracts.md` 作为 harness 友好摘要。
- 原因：英文文件名便于命令行和链接引用，摘要文件方便 agent 快速读取，完整规格保留原始意图。
- 否决方案：删除完整规格，只保留摘要。
- 约束：摘要与完整规格冲突时，先暂停并指出冲突。
- 后续检查：后端 MVP 跑通后，确认摘要是否需要反向同步完整规格中的新增约束。

## [decision] [verified] 2026-05-29: 上下文约 50% 时主动触发交接

- 背景：原 harness 只定义了会话结束后的交接内容，未定义何时主动触发交接。长任务（如连续跑完 MVP 全部 T001–T012）可能在上下文窗口耗尽时才被动退出，导致断点状态未记录、下一个会话无法准确定位继续点。
- 决策：在 `agent-workflow.md` 的「会话交接」章节增加触发条件——上下文用量达到约 50% 时，完成当前任务或记录进度后主动停止，写交接记录到 `.harness/state/runs/YYYY-MM-DD-HHMM-handoff.md`，并同步更新 `PROGRESS.md`。
- 原因：个人 wiki 的上下文与记忆管理资料指出，长上下文窗口并不等于可靠可用窗口，可靠部分常在前 30% 到 50%，并建议约 50% 时主动压缩且明确保留架构决策、待办事项、验证证据和阻塞点。选择 50% 而非 60% 或 80%，是为了把交接放在能力退化前完成。
- 否决方案：(1) 不做主动交接，依赖系统自动压缩——风险是压缩后丢失关键状态；(2) 阈值设为 60% 或 80%——风险是已经进入可靠性下降区间，余量不足写完整交接记录。
- 约束：50% 是估算值，agent 无法精确读取上下文百分比，需综合对话轮数、文件读取量和剩余响应空间判断。交接输出格式在 `agent-workflow.md` 中定义，不在此重复。
- 后续检查：连续执行 T001–T004 后，复盘 50% 阈值是否在长任务中实际触发了交接，以及交接记录的断点是否足够让下一个会话无缝继续。

## [decision] [verified] 2026-05-29: 工具权限按生命周期拆分

- 背景：`tool-manifest.md` 曾将 `.harness/` 整体标为只读，但工作流要求写入 `.harness/state/runs/` 和 `.harness/state/sprint-contracts/`；维护 harness 规则时也需要修改 `.harness/instruction/`、`.harness/feedback/` 或 `.harness/tool/`。
- 决策：按生命周期拆分权限边界：运行状态目录常规可写；规则、反馈、环境和工具清单默认只读；当当前任务 `allowed_paths` 明确包含，或用户明确要求维护 harness/文档时，才允许修改对应规则或文档文件。
- 原因：状态文件是每次运行的输出，必须可写；规则文件是持久约束，默认应稳定，但不能阻止显式的 harness 维护任务修正规则冲突。
- 否决方案：继续把 `.harness/` 整体标为只读——会与运行记录和冲刺合同写入冲突；把 `.harness/` 整体标为可写——会削弱规则文件的保护边界。
- 约束：关键规则变更必须同步更新 `DECISIONS.md` 和 `PROGRESS.md`；普通业务任务不得顺手修改默认只读的 harness 规则文件。
- 后续检查：T001 完成后复盘 `allowed_paths` 与 `tool-manifest.md` 是否仍存在冲突，尤其是 `docs/` 文档维护任务。

## [decision] [verified] 2026-05-29: 任务拆分必须满足原子化要求

- 背景：当前 `tasks/tasks.yaml` 中存在多关注点合并的单任务——T004 同时承担气动预测 API、HDF5 artifact 基础设施和 artifact 查询/下载 API 三个关注点；T005 被标注为"MVP 中最重的单任务"，内含 5 步实现顺序。这违反了单任务应可在一个会话内独立完成并验证的原则。
- 决策：后续任务拆分（包括新项目初始化和现有项目补任务）必须满足原子化要求——每个任务只承担一个可独立验证的关注点，单次会话内可完成，有明确的 `allowed_paths`、`expected_outputs` 和 `validation.commands`。
- 原因：非原子化任务会导致：(1) 单任务跨多个会话，交接成本高且容易丢失中间状态；(2) 验证边界模糊，无法精准定位失败点；(3) 并行化受限，大任务阻塞后续依赖链；(4) 与 WIP=1 规则冲突——名义上一个任务，实际做了多件事。
- 否决方案：继续允许多关注点合并——理由曾是"artifact 通用框架随第一个消费者一起建立"，但正确的做法是把通用基础设施拆为独立的前置任务，消费者作为后续任务依赖它。
- 约束：原子化不意味着任务粒度越小越好——一个任务应是对外有完整行为的可验证单元（如一个 API endpoint + 其 contracts + 其 service + 其 tests），而不是按文件拆分。判断标准：能否用一句话描述这个任务做什么，且这句话里没有"和"。
- 后续检查：T004 和 T005 完成后复盘拆分粒度；后续项目首次拆分任务时以此决策为基线审查。

## [decision] [verified] 2026-05-29: 三维结构几何改为 STEP artifact

- 背景：原规格将 `/geometry/wing-3d` 定义为返回 1000 个三维点云，但点云缺少 CAD 拓扑，不能可靠导出可在三维建模和网格前处理工具中使用的几何。
- 决策：第一版三维机翼生成改为返回右半翼结构 STEP artifact，覆盖蒙皮、前梁、后梁和翼肋；STEP 通过统一 artifact 查询和下载接口暴露，强度预测仍使用参数化输入，不依赖 STEP。
- 原因：STEP 能表达 CAD 几何和拓扑，更适合后续下载、导出和结构网格划分；点云只适合轻量预览，不适合作为工程几何事实源。
- 否决方案：继续返回点云，或将结构 STEP 与面向外流场 CFD 的气动外形 STEP 混在同一个 artifact。
- 约束：STEP 必须由 CAD kernel 生成，优先 CadQuery/OpenCascade；禁止手写 STEP 文本伪造几何。结构 STEP 是多组件结构装配，不布尔融合；蒙皮外表面保持 CST 截面，内部梁肋裁剪在蒙皮内。面向外流场 CFD 的干净外表面 STEP 后续单独生成。
- 后续检查：实现 T005 时确认 CAD 依赖、CI 环境和 STEP 文件有效性验证方式。

## [decision] [verified] 2026-05-27: 初始化 Git 仓库并保留默认初始分支名

- 背景：目录中原有 `.git` 为空且只读，`git status` 无法识别仓库。
- 决策：修复 `.git` 写权限并执行 `git init`，当前初始分支保持为 `master`。
- 原因：先让本地 Git 可用，支持后续提交、checkpoint 和 worktree；分支命名不是当前阻塞点。
- 否决方案：删除 `.git` 后重新建仓，或立即改名为 `main`。
- 约束：后续如要引入远端仓库或团队分支规范，再统一重命名。
- 后续检查：首次提交前确认是否需要 `.gitignore`。

## [decision] [verified] 2026-05-29: 新增 I/O 卫生规则

- 背景：agent 循环中工具输出直接回灌进上下文，长输出（pytest 全量日志、pip install 输出、CAD kernel 错误）会在几轮内耗尽上下文窗口，导致推理质量下降。Wiki「Agent 循环策略与 Harness 设计原则」将 I/O 卫生列为 harness 的基础职责，要求截断、抽帧和落盘三层过滤。
- 决策：新增 `.harness/instruction/rules/io-hygiene.md`，规定：命令输出默认保留尾部 2000 行；Python traceback 抽帧只保留报错帧和失败测试名；>5MB 输出落盘到 `.harness/state/working/`；错误方向超过两轮时 rewind 清理错误分支。
- 原因：在 T001 开始前补上这一层，防止首次实现任务就被长输出淹没上下文。规则是确定性工程边界，不依赖 agent 临场判断。
- 否决方案：(1) 不做 I/O 卫生，依赖 agent 自行判断——风险是 agent 倾向保留完整输出，不会主动截断；(2) 只做截断不做抽帧和落盘——栈追踪中最有价值的就是报错帧和测试名，其余帧纯属噪声。
- 约束：所有工具输出自动适用，agent 无需每次判断是否触发。I/O 卫生不替代错误分析——agent 仍可通过 grep/tail 读取被截断的输出文件。
- 后续检查：T001-T004 执行后，复盘是否有真实场景触发了落盘规则（>5MB 输出），以及截断是否导致关键信息丢失。

## [decision] [verified] 2026-05-29: 新增代码结构约束

- 背景：Wiki「Agent 循环策略」引用 OpenAI 观点——开发者应通过硬性约束管理 AI 系统，而非在代码 review 时逐一纠正。当前 harness 缺少文件大小、函数长度和依赖引入的边界限制，agent 可能写出 god file、单体函数或悄悄引入新库。
- 决策：在 `agent-workflow.md` 中新增「代码结构约束」章节：单文件不超过 200 行，函数不超过 50 行，新增第三方依赖必须经用户确认。
- 原因：这些约束在 agent 生成代码前就生效，属于结构性防线。200 行和 50 行是经过验证的实用上限——不是让每个文件都接近上限，而是防止个别文件膨胀失控。
- 否决方案：(1) 不做硬性上限，仅作为建议——模型对"建议"的遵守率远低于硬约束；(2) 设更严格的限制（100 行/30 行）——会过度碎片化，增加模块间通信成本。
- 约束：上限是硬性的，不是建议。合理的文件组织可能自然远低于上限。新依赖确认机制不阻塞开发——用户确认后即可继续。
- 后续检查：T001-T004 完成后，检查生成文件的行数分布，确认约束是否合理触发。

## [decision] [verified] 2026-05-29: 新增工作状态管理约定

- 背景：Wiki「AI Agent 上下文与记忆管理」提出三层记忆模型——Active Context Window 管现在，Working State 管本次任务，Durable Memory 管项目长期知识。当前 harness 有完善的 Durable Memory（CONTEXT.md、DECISIONS.md、tasks.yaml），但缺少 Working State 层的约定。长任务执行中产生的计划、检索结果、调试笔记没有指定位置，也没有清理规则。
- 决策：创建 `.harness/state/working/`（含 `.gitkeep`）作为工作状态目录。在 `agent-workflow.md` 中定义典型 working files（plan.md、search-results.md、debug-notes.md、long-output.log）和生命周期规则：任务执行中按需读写，任务通过后清理，下一个任务开始时目录为空。
- 原因：给 agent 一个比上下文窗口大得多的外部草稿区，同时防止临时文件污染项目根目录。清理规则确保每次会话不把上一次任务的中间状态带入新任务。
- 否决方案：(1) 不设专门目录，让 agent 自行选择临时文件位置——会散落各处，清理不彻底；(2) 把 working state 放在项目根目录——增加噪音，与业务文件混淆。
- 约束：`.gitignore` 应忽略 `.harness/state/working/` 中除 `.gitkeep` 外的所有文件。值得长期保留的发现必须升级到 PROGRESS.md 或 DECISIONS.md，不能留在 working files 中。
- 后续检查：T001 完成后检查 working 目录是否被正确清理。

## [decision] [verified] 2026-05-29: 运行遥测记录

- 背景：Wiki 评估指标体系强调每次运行都应记录 trace id、模型、token、工具调用、延迟和错误，用于趋势分析和治理。当前 state/runs/ 记录是叙事性的，不便于聚合统计。
- 决策：新增 `.harness/state/runs/telemetry.yaml` 作为运行遥测模板，包含单次运行记录模板（task_id、status、duration_min、model、token_estimate、tool_calls、failures）和累积统计滚动更新区块。每次会话结束时按模板填充并保存为 `runs/YYYY-MM-DD-telemetry.yaml`。
- 原因：粗略的结构化记录足以支撑趋势分析，不需要精确到 API 调用级。累积统计让治理决策（如"平均每个任务的 token 趋势"）有数据基础。
- 否决方案：(1) 不做结构化遥测，依赖叙事性 session 记录——无法聚合统计；(2) 引入完整的 Langfuse/Braintrust 等可观测平台——过早引入外部依赖，增加运维负担。
- 约束：所有字段均为人工估算值，不追求 API 调用级精度。token_estimate 从对话轮数和文件读取量粗略估算。累积统计每次运行后滚动更新。
- 后续检查：T004 完成后复盘遥测数据是否足以支撑"平均 token 趋势"和"任务难度校准"两个基本分析。

## [pitfall] [verified] 2026-05-29: 任务完成后必须同步更新 tracking 文件

- 背景：2026-05-29 会话中，连续执行 T001-T006 六个任务时，只专注于代码实现而忽略了 `tasks/tasks.yaml` 和 `PROGRESS.md` 的同步更新。用户在第六个任务完成后发现并指出该问题，agent 才批量补更。这违反了 harness 的工作流规则（"每次任务结束必须更新 tasks.tasks[].evidence 和 PROGRESS.md"）。
- 教训：代码变更（implementation）和跟踪更新（tracking）是一个原子操作——任务完成 = 代码通过验证 + status 设为 passing + evidence 填写 + PROGRESS.md 更新。不能先做完所有代码再回过头补 tracking。
- 根本原因：agent 把"完成任务"理解为"通过 pytest"，而 harness 定义的"完成"包括 status、evidence 和 PROGRESS.md 的更新。这是对完成定义的理解偏差，不是疏忽。
- 纠正措施：
  1. 每个任务的最后一步永远是更新 `tasks/tasks.yaml` 和 `PROGRESS.md`，在运行 `pytest` 验证通过后立即执行。
  2. 使用 TodoWrite 跟踪任务时，最后一个 todo item 始终是"更新 tracking 文件"。
  3. 禁止连续执行多个任务后才批量补更 tracking——每完成一个任务就更新。
  4. 若用户明确指出 tracking 未更新，立即停止当前任务，补更后再继续。
- 约束：此规则适用于所有后续任务，不做例外。若未来引入自动化脚本更新 tracking，仍需 agent 确认更新内容正确。

## [pitfall] [verified] 2026-05-29: 违反 AGENTS.md 会话流程——跳步执行

- 背景：2026-05-29 会话中，agent 接到"开始执行任务，完成项目第一版构建"指令后，直接跳入 T001 代码实现，完全忽略了 AGENTS.md 定义的 6 步会话流程。用户在 T006 完成时首次指出 tracking 未更新，在 T008 执行中再次指出冲刺合同未创建、harness 状态和反馈未记录。
- 具体违规：
  1. **Step 1 跳步**：未先读 PROGRESS.md、DECISIONS.md、tasks.yaml 确认当前状态（直接凭 spec.md 开始写代码）
  2. **Step 3 跳步**：每个任务开始前未阅读对应冲刺合同（`.harness/state/sprint-contracts/`），缺失时也未创建——T002-T007 共 6 个任务均无冲刺合同
  3. **Step 5 跳步**：T001-T006 连续执行后才批量补更 tasks.yaml 的 status 和 evidence，违反了"每次任务结束必须更新"
  4. **Step 6 跳步**：PROGRESS.md 只在 T006 后被用户指出后才更新，session-exit-checklist 完全未执行
- 根本原因：agent 把"执行任务"理解为"写代码 + 跑测试"，但 harness 定义的"执行任务"是一个包含状态准备（Steps 1-3）和状态同步（Steps 5-6）的完整闭环。这不是疏忽，是对 harness 工作流的根本性误解。
- 纠正措施（强制性，不可跳步）：
  1. **任务前**：先读 PROGRESS.md → DECISIONS.md → tasks.yaml 确认当前 active 任务 → 读/创建对应冲刺合同
  2. **任务中**：遵守 WIP=1 和 allowed_paths
  3. **任务后**（pytest 通过后立即执行）：更新 tasks.yaml status + evidence → 更新 PROGRESS.md → 检查 session-exit-checklist 是否需要交接
  4. **绝不**：连续执行多个任务后才批量补 tracking
- 约束：此 pitfall 等级高于普通操作失误——它是工作流层面的系统性违规。后续所有会话必须严格遵循 AGENTS.md 的 6 步流程，不做任何例外或"先做再补"。

## [pitfall] [verified] 2026-05-30: 整个会话零 git 提交

- 背景：2026-05-29 会话完成了 T001-T015 共 15 个任务的代码实现（104 tests pass, ~50 个文件），但全程未执行任何 git commit。用户在次日打开项目后发现 git status 显示所有文件均为未跟踪/未暂存状态。
- 具体违规：从 T001 开始创建 `backend/` 目录到 T015 文档完成，每个任务都产生了大量文件变更，但 agent 从未将其提交到 git。所有工作成果处于 uncommitted 状态，丢失风险高，也无法按任务粒度回溯变更历史。
- 根本原因：agent 把"完成任务"定义缩小为"代码通过 pytest + tracking 文件更新"，完全忽略了 git commit 是任务完成的一个必要组成部分。虽然 AGENTS.md 和 harness 规则中未明确列出 commit 步骤，但任务原子化天然意味着每个任务应对应一个可独立回溯的 commit。
- 纠正措施：
  1. 每个任务完成后、更新 tracking 文件前，必须执行 `git add` + `git commit`。
  2. Commit message 格式：`feat: <任务标题> (T00X)`，body 引用 evidence。
  3. 禁止跨任务批量 commit——一个任务一个 commit。若单任务改动过大可在任务内拆分，但至少保证任务边界有 commit。
  4. 若任务无实际文件变更（纯文档/配置任务），仍需 commit tracking 文件的更新。
- 约束：此规则即刻生效。后续所有任务必须按此粒度提交，不做例外。

## [pitfall] [verified] 2026-05-30: Harness 全量审计——13 项违规/遗漏

2026-05-30 对 2026-05-29 会话进行全量 harness 合规审计，逐条对照 6 个规则文件 + 3 个反馈文件 + 环境声明 + 工具清单 + 模板符合性检查 + 知识索引。以下为发现的全部违规和遗漏（已发现的 3 条 pitfall 不计入）。

### 一、代码结构约束违规（agent-workflow.md § 代码结构约束）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 1 | `core/geometry.py` 355 行 | 单文件 ≤200 行 | 超标 77%，17 个函数挤在一个文件 |
| 2 | `generate_wing_3d_step()` 63 行 | 函数 ≤50 行 | 超标 26%，内含 CAD 生成全流程 |

**纠正**：将 `core/geometry.py` 拆分为 `core/geometry_2d.py`（CST 参数化）+ `core/geometry_3d.py`（CadQuery CAD 生成）。将 `generate_wing_3d_step()` 拆分为编排函数 + 独立步骤函数。

### 二、工作状态管理违规（agent-workflow.md § 工作状态管理）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 3 | 从未写 `plan.md` | "长任务或复杂任务先写 plan.md 再动手" | T008（三维 CAD 生成）是 MVP 最复杂任务，直接上手写代码，无分步计划 |
| 4 | 从未使用 `.harness/state/working/` | "中间产物应放入 working/" | 整个会话的调试输出、CAD 测试脚本全部直接跑在终端，未落盘 |
| 5 | session 结束未清理 working | "任务 passing 后清理本任务临时文件" | working 目录虽为空（因从未使用），但清理步骤被跳过了 |

### 三、会话退出检查清单违规（session-exit-checklist.md）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 6 | 未执行 session-exit-checklist | "无论普通结束还是 50% 主动交接，均执行" | 清单中 12 项检查完全未执行 |
| 7 | 未记录运行遥测 | "复制 telemetry.yaml 模板，填写本次会话 run 记录" | `telemetry.yaml` 仍为初始模板，无本次会话记录 |

### 四、环境声明违规（environment.md）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 8 | 未创建 venv | "虚拟环境：venv（项目本地 .venv/）" | 直接 `pip install --user`，未隔离环境 |
| 9 | Python 版本不符 | "Python：3.11+" | 实际运行 Python 3.10.12 |

### 五、冲刺合同缺口（agent-workflow.md § 会话流程 Step 3）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 10 | 15 个任务中仅 3 个有冲刺合同 | "阅读当前任务的冲刺合同；若缺失，先在 sprint-contracts/ 创建" | 仅 T001/T008/T009 有，T002-T007, T010-T015 共 12 个任务缺失 |

### 六、依赖引入未确认（agent-workflow.md § 代码结构约束）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 11 | CadQuery 安装未确认 | "新增第三方依赖必须先经用户确认" | T007 直接 `pip install cadquery`，未询问用户 |

### 七、完成定义违规（definition-of-done.md）

| # | 违规 | 规则 | 现状 |
|---|------|------|------|
| 12 | 无静态检查 | "静态检查通过：lint/typecheck/format（阶段未定义时在 PROGRESS.md 说明）" | 项目无 lint/typecheck 配置，PROGRESS.md 也未说明原因 |

### 八、规则文件内部冲突

| # | 冲突 | 涉及文件 | 现状 |
|---|------|----------|------|
| 13 | `/coordinates` shape 不一致 | `artifact-policy.md` 写 `(1000, 3)` columns `[x,y,z]`；`spec.md` 和 `backend-mvp-full-spec.md` 写 `(1000, 2)` | 实现按 spec 使用 `(1000, 2)`，但 artifact-policy.md 未修正 |

### 根因分析

以上 13 项可归为三类根因：

1. **"任务完成"定义过窄**（#1-5, #7, #10, #12）：把完成等同于"测试通过"，忽略了计划、工作状态管理、环境合规、冲刺合同和退出检查清单。
2. **环境搭建跳过规范**（#8, #9, #11）：直接使用系统 Python + --user 安装，未按 environment.md 创建 venv；引入新库未确认。
3. **规则文件维护滞后**（#13）：实现过程中发现了 spec 与规则文件的冲突但未回溯修正规则文件。

### 纠正措施

1. 复杂任务（>3 个新文件或涉及外部 kernel）必须先写 `.harness/state/working/plan.md`，至少包含实现步骤、关键 API 调用和风险点。
2. 每个任务完成后，对照 `definition-of-done.md` 和 `session-exit-checklist.md` 逐项自检。
3. 后续新任务开始前必须先创建冲刺合同，不可跳过。
4. 环境搭建必须按 `environment.md` 执行：`python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`。
5. 新增第三方依赖前必须经用户确认，无论是 pip install 还是写入 pyproject.toml。
6. 每次会话结束必须填写 `telemetry.yaml`。
7. 发现规则文件与实际实现不一致时，立即修正规则文件并记录到 DECISIONS.md。

## [decision] [verified] 2026-05-30: Harness P0 优化——完成协议合并 + 环境自检

- 背景：2026-05-30 全量审计发现 13 项违规，根因是 harness 为被动文档系统——完成定义散落 4 个文件、环境声明存在但无强制检查、agent 自觉遵守但容易跳步。
- 决策（P0 两项，立即实施）：
  1. **完成协议合并**：在 `agent-workflow.md` 新增"任务完成协议"章节（9 步硬性流程），作为唯一事实源。`AGENTS.md` 会话流程引用该协议，`session-exit-checklist.md` 收缩为补充验证项。
  2. **会话启动自检**：`AGENTS.md` 新增 Step 0（环境自检），确认 Python 版本、venv 激活、依赖安装后才进入任务流程。`agent-workflow.md` 同步更新。
- 原因：将"被动文档"变为"主动流程"——agent 不需要跨 4 个文件自行拼凑完成定义，按单一协议的 9 步顺序执行即可。自检步骤在任务开始前就拦截环境类违规。
- 否决方案：(1) 不做优化，继续依赖 agent 自觉——审计已证明不可行；(2) 引入完整 CI/CD pipeline 做自动化检查——当前 MVP 阶段过重。
- 约束：完成协议是硬性流程，不可跳步；自检在每次会话开始时执行。

## [decision] [verified] 2026-05-30: Harness P1 优化——pre-commit 自动检查 + tasks.yaml checklist

- 背景：P0 优化解决了流程层面的跳步问题，但代码结构约束（文件 ≤200 行、函数 ≤50 行）和 harness 步骤确认仍靠 agent 自觉。审计中发现的 `core/geometry.py` 355 行超标和 `generate_wing_3d_step()` 62 行超标，在编码时完全未被察觉。
- 决策（P1 两项）：
  1. **pre-commit 自动检查**：新增 `.pre-commit-config.yaml` + `.harness/tool/pre-commit-check.py`，在每次 `git commit` 时自动检查暂存区中 `backend/src/` 和 `backend/tests/` 下的 Python 文件——文件行数 ≤200、函数长度 ≤50、无 `print()` 调试残留。违反时阻止提交。
  2. **tasks.yaml checklist 字段**：`feature_schema.required_fields` 新增 `checklist`，`workflow` 新增 `default_checklist`（8 项：pytest/git commit/status更新/PROGRESS更新/DECISIONS补充/learnings写入/telemetry填写/working清理）。所有 16 个任务的 `checklist: default` 已填充。标记 passing 前必须逐项确认。
- 原因：将"被动规则"变为"主动拦截"——pre-commit hook 在代码进入仓库前就阻止违规；checklist 把完成协议的 9 步绑定到每个任务定义上，agent 读取任务时就能看到该做什么。
- 否决方案：(1) 在 CI 中做检查而非 pre-commit——CI 反馈太慢，违规代码已经 push；(2) 完全自动化 checklist 确认——大部分步骤（git commit、learnings 内容）仍需 agent 判断。
- 约束：pre-commit hook 只检查 `backend/src/` 和 `backend/tests/` 下的 `.py` 文件。若任务需要正当超标，需在 DECISIONS.md 中记录例外并说明原因。

## [decision] [verified] 2026-05-30: Harness P2 优化——冲刺合同分级 + 规则一致性标注

- 背景：审计发现 15 个任务中仅 3 个有冲刺合同（12 个缺失），原因是按 T001 的 37 行完整模板写合同太重。另外 artifact-policy.md 与 spec.md 的 coordinates shape 冲突直到审计才发现，说明跨文件约束一致性缺少检查机制。
- 决策（P2 两项）：
  1. **冲刺合同分级**：新增两级模板——`_TEMPLATE-full.md`（完整合同，复杂任务用）和 `_TEMPLATE-light.md`（5 行 YAML frontmatter，简单任务用）。复杂任务判定标准：新建文件 >3 个，或依赖 CAD kernel/外部系统，或跨 ≥3 个模块。`agent-workflow.md` Step 3 已更新分级规则。
  2. **规则一致性标注**：在 `artifact-policy.md`（coordinates shape）、`domain-constraints.md`（fitness 公式）和 `config/settings.py`（所有硬编码值）中添加 `FACT-SOURCE:` 注释，指向 `docs/backend-mvp-full-spec.md` 或 `docs/spec.md` 的权威行号。修改规则文件时可交叉验证。
- 原因：分级合同降低简单任务的流程负担（从 37 行降到 5 行）；FACT-SOURCE 标注让"这个数字从哪里来"可追溯，减少 spec 与规则文件的漂移。
- 否决方案：(1) 全部用轻量合同——复杂任务需要明确排除项和观测信号；(2) 引入 JSON Schema 或结构化检查工具做一致性校验——当前阶段过重。
- 约束：轻量合同仅用于简单任务；一旦任务涉及 CAD kernel、优化算法或多模块协调，必须用完整合同。FACT-SOURCE 标注是注释约定，不强制机器校验，但 agent 修改约束值时必须验证源头。若任务需要正当超标（如 CAD kernel 初始化代码），需在 DECISIONS.md 中记录例外并说明原因。

## [decision] [draft] 2026-05-29: 多 Agent 并行化预留设计

- 背景：Wiki 多智能体 Git 协作模式提供了 worktree 隔离 + 任务分支 + integration branch 的完整模式。当前项目有意推迟多 Agent（WIP=1），但任务依赖图和路径隔离设计应提前预留并行化接口，避免后续重构。
- 决策：在 `tasks.yaml` 的 `feature_schema` 中新增 `parallelizable_group` 可选字段——同一 group 内的任务具有相同的 `depends_on` 且 `allowed_paths` 互不相交，可在独立 worktree 中由不同 agent 并行处理。当前单 agent 模式下忽略此字段；多 agent 场景下，group 内的任务由不同 agent 并行执行，通过 integration branch 汇合。
- 原因：当前项目的任务依赖图已自然形成两个并行窗口：(1) T002 完成后的 post-t002 组（T003/T004/T009/T010，4 个任务路径完全隔离）；(2) T004 完成后的 post-t004 组（T005/T006/T007，3 个任务路径完全隔离）。不需要为了并行化重新切分任务——现有原子化拆分已经满足并行条件。将此信息显式记录在任务契约中，让未来的并行化调度不再需要人工推断。
- 否决方案：(1) 现在就引入多 Agent 并行执行——违反 WIP=1 当前约束，且项目尚在骨架阶段，多 Agent 协调成本超过收益；(2) 不做任何预留，等到需要并行时再分析——会增加调度 agent 的推断负担和出错概率。
- 约束：`parallelizable_group` 是声明性字段，不改变当前单 agent 执行流程。同一 group 内任务必须满足三个条件：相同依赖集、allowed_paths 互不相交、expected_outputs 无重叠文件。添加或修改任务时必须维护 group 标记的正确性。
- 后续检查：首次启动多 Agent 并行执行前，验证 worktree 隔离是否生效、integration branch 汇合是否无冲突。

## [pitfall] [verified] 2026-05-30: 项目自检暴露 9 步协议 6 步遗漏

- 背景：用户在 T000-T015 全部 passing 后要求"使用 harness 开启新任务进行项目自检"。执行了 `backend/backend/` 空嵌套目录删除 + pytest 验证 + PROGRESS.md 更新后，直接宣告完成。用户指出未 git commit，暴露协议执行系统性遗漏。
- 遗漏项（9 步中 6 步未执行）：git commit、tasks.yaml 状态更新、DECISIONS.md 检查、learnings 写入、telemetry.yaml 填写、session-exit-checklist 自检。另外未创建冲刺合同。
- 根因：
  1. **"验证通过 = 完成"的错误心智模型**——pytest 通过后心理上认为任务结束。
  2. **自检/维护类活动无任务模板**——tasks.yaml 只建模功能开发任务，目录清理、环境自检等维护活动游离在任务模型外，导致"建不建任务条目"成为模糊地带。
  3. **遥测从未被实际使用**——telemetry.yaml 自创建以来 runs 列表为空，沦为空骨架。
- 改进：
  1. 任何改动，验证通过后立即逐项对照 9 步协议，不跳步。
  2. 非功能开发类活动（自检、修复、清理）若不需要创建新任务条目，必须在 PROGRESS.md 中明确标注为"非任务维护活动"并说明豁免原因。
  3. 遥测：要么实际填充，要么在下次复盘时降级为可选。本次会话已填充 telemetry.yaml 作为示范。
- 证据：`.harness/state/runs/2026-05-30-learnings.md` 详细记录。

## [decision] [draft] 2026-05-30: 自检 #2 — 代码结构合规拆分

- 背景：2026-05-30 自检 #2 发现 4 个文件 >200 行、2 个函数 >50 行。这是 2026-05-30 全量审计中已知违规（#1-2）未修复的延续，且发现新增违规（`coupled_optimize()` 61 行、3 个测试文件超标）。
- 决策：
  1. `core/geometry.py`（355 行）拆分为 `geometry_2d.py`（CST 参数化，53 行）+ `geometry_3d.py`（CAD 编排，74 行）+ `geometry_3d_builders.py`（CAD 原语 + STEP 读取，192 行）。原 `geometry.py` 改为 re-export 兼容层，保持所有现有 import 不受影响。
  2. `core/optimization.py` 提取 `_perturb_cst_params()` 和 `_perturb_structure_params()` 共享辅助函数，`coupled_optimize()` 从 62→48 行。
  3. 测试文件拆分：`test_contracts.py`→验证 + 模型两文件；`test_geometry_api.py`→2D + 3D 两文件；`test_optimization_api.py`→气动/结构 + 耦合两文件。
- 原因：代码结构约束是硬性上限（≤200 行/文件、≤50 行/函数），必须在进入下一阶段前清零所有违规。拆分原则：按领域边界拆分（2D vs 3D、编排 vs 原语），不按文件行数机械切割。
- 否决方案：(1) 不做拆分，在 DECISIONS.md 记录例外——违反硬约束；(2) 更细粒度拆分（3D builders 再分成 skin/spar/rib 三文件）——当前 192 行在 200 行限制内，过度拆分增加模块通信成本。
- 约束：`geometry.py` 作为 re-export 兼容层长期保留，不承载业务逻辑。后续涉及 CST 逻辑修改只动 `geometry_2d.py`，涉及 CAD 原语只动 `geometry_3d_builders.py`。
- 后续检查：下一阶段（真实模型接入）时确认拆分边界是否依然合理，尤其是 `geometry_3d_builders.py` 是否会随 CAD 功能增加而再次超标。

## [pitfall] [verified] 2026-05-30: 自检 #2 全过程使用系统 python3 而非项目 .venv

- 背景：2026-05-30 自检 #2 从环境检查、pytest 运行、pip install 到 pre-commit 检查，全程使用 `python3`（系统 /usr/bin/python3）和 `pip --user` 全局包，未创建项目级 `.venv/`。用户明确指出"不应使用 python3 命令，应先创建环境"。
- 具体违规：
  1. 环境自检（Step 0）时明知无 .venv 且 Python 3.10.12 < 3.11，但仅作为"已知问题"记录，未尝试修复。
  2. 所有 `python3 -m pytest`、`pip install cadquery`、`python3 pre-commit-check.py` 均在 venv 外执行。
  3. 系统全局安装了 CadQuery 全家桶（cadquery, cadquery-ocp, vtk, ezdxf 等），污染了全局 Python 环境。
- 根因分析：
  1. **"已知问题 = 已处理"的错误心智模型**：PROGRESS.md 中记录了"无 .venv"，心理上将其归档为"已记录"而不再处理。但 harness 的「环境自检」要求是**搭建环境**而非仅**记录问题**。
  2. **工具惯性**：`python3` 是 shell 中最短路径，创建 venv + source activate + pip install 是三步操作，agent 倾向于选择一步到位的命令。
  3. **缺乏环境自检拦截**：AGENTS.md Step 0 定义了环境自检，但 agent 在自检 #2 时完全跳过了这一步，直接开始了审计。
- 纠正措施：
  1. 已创建 `backend/.venv/`，使用 `python3.10 -m venv .venv` + `pip install -e ".[dev,cad]"`（Tsinghua 镜像）。
  2. `backend/.gitignore` 已添加 `.venv/`。
  3. 后续所有命令必须通过 `source backend/.venv/bin/activate && python ...` 或 `backend/.venv/bin/python ...` 执行。
  4. Python 3.10.12 vs 3.11 差距：pyproject.toml 允许 ≥3.10，功能不受限。若后续需要 3.11+ 特性再升级。
- 约束：此规则即刻生效。每次会话 Step 0 必须检查 `.venv/bin/python` 可用，不可跳过。

## [pitfall] [verified] 2026-05-30: tasks.yaml 事后批量补更——Plan 获批后跳过任务建模直接编码

- 背景：用户要求将已知问题写成任务并用 harness 控制完成。进入 Plan 模式→获批→直接开始 T016/T017/T018 编码和 commit→三个任务全部完成后才一次性将 T016-T018 写入 tasks.yaml（全部 `passing`）。
- 违规项：
  1. Plan 中定义了 T016-T018，但未同步到 tasks.yaml 就开始编码。
  2. T016/T017/T018 三个任务连续执行后才批量补更 tasks.yaml 的 status 和 evidence。
  3. PROGRESS.md 和 telemetry.yaml 也是最后一批更新的。
- 根因：**tasks.yaml 被当成"事后归档文档"而非"事前任务模型"**。Plan 获批后的心理状态是"可以开始写代码"，而正确的下一步是"先将 plan 中的任务条目写入 tasks.yaml（事实源），再开始写代码"。这是 `[pitfall] 2026-05-29` 的变体——上次是"验证=完成"，这次是"plan 获批=可以跳过 tracking 直接编码"。
- 纠正措施：Plan 获批后的第一个动作必须是：将 plan 中拆分的任务条目添加至 tasks.yaml（status=`active` 或 `not_started`）并提交。此后才能开始第一个任务的代码实现。tasks.yaml 是执行的前置依赖，不是执行后的归档。
- 约束：此规则即刻生效。无 tasks.yaml 条目 = 无任务执行权。
- 补充发现（同 session）：PROGRESS.md「进行中」在 T016-T018 整个执行期间始终为 `无`。该字段应在**任务开始时**更新为活动任务 ID，**任务完成时**移入「已完成」——它是跨会话断点定位的核心字段。措施：任务开始第一步 = 更新 PROGRESS.md 进行中 + tasks.yaml status→active；任务完成最后一步 = 更新 PROGRESS.md 进行中→已完成/无。

## [decision] [verified] 2026-05-30: ADR 目录从 .harness/instruction/adr/ 迁移到 docs/adr/

- 背景：ADR（架构决策记录）之前放在 `.harness/instruction/adr/` 中，属于 harness 内部目录。用户指出 ADR 应放在 `docs/adr/` 便于查阅和决策追溯。
- 决策：将 `0001-store-field-data-as-hdf5-artifacts.md` 和 `0002-generate-structural-wing-geometry-as-step-artifacts.md` 从 `.harness/instruction/adr/` 迁移到 `docs/adr/`，删除旧目录，更新所有引用路径。
- 原因：`docs/` 是项目文档的自然入口，ADRs 放在这里可发现性更高；`.harness/instruction/` 更适合放规则和工作流指引，而非业务架构决策。
- 否决方案：保持原位，或在两处各放一份副本。
- 约束：后续新增 ADR 一律放入 `docs/adr/`，按 `NNNN-title.md` 编号。引用 ADR 时使用 `docs/adr/` 路径。
