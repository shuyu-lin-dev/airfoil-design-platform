# 项目进度

> 更新日期：2026-05-30

## 当前状态

- 最新检查点：**MVP 第一版全部 15 个任务完成（T000-T015）** + **项目自检（2026-05-30 #1）** + **项目自检（2026-05-30 #2，非任务维护活动：代码结构修复 + 冲刺合同补建）**。
- 测试状态：**104 passed**, 8 warnings（CadQuery FutureWarning + Starlette DeprecationWarning）。
- 构建状态：FastAPI 应用可启动，所有 12 个 API 端点已注册。
- 代码结构：**全部 ≤200 行/文件，≤50 行/函数**（pre-commit 检查零违规）。
- 冲刺合同：**16/16 全覆盖**（T000-T015，含轻量模板）。
- 当前 active 功能项：无。

## 已完成

- [x] T000 - 初始化项目内 harness
- [x] T001 - Backend skeleton（FastAPI + /health + pytest）
- [x] T002 - Common contracts and config（Pydantic 契约 + settings 默认值）
- [x] T003 - Geometry 2D API（CST 翼型生成，200 点）
- [x] T004 - Artifact infrastructure with HDF5 store
- [x] T005 - Artifact query and download API
- [x] T006 - Aerodynamic prediction API（升阻比 + Cp + HDF5）
- [x] T007 - STEP artifact store（CadQuery 方盒验证）
- [x] T008 - Geometry 3D API（CadQuery 三维机翼 STEP 生成）
- [x] T009 - Structure prediction API（max_stress + weight）
- [x] T010 - Aerodynamic optimization API
- [x] T011 - Structural optimization API
- [x] T012 - Coupled optimization API（fitness = L/D / weight）
- [x] T013 - Teaching airfoil generation API
- [x] T014 - Teaching CST inverse API
- [x] T015 - Documentation pass（README + .gitignore）

## 进行中

- 无。

## 维护活动记录

- **2026-05-30 自检 #2**（非任务维护活动）：无对应 tasks.yaml 条目。豁免原因：代码结构修复、冲刺合同补建和规则一致性检查是 harness 基础设施维护，不属于功能开发类 tracer bullet。按 DECISIONS.md pitfall 约定，此类活动在 PROGRESS.md 明确标注即可。
- **2026-05-30 已知问题修复**（T016-T018）：消除 8 条 pytest 警告（StarletteDeprecationWarning + CadQuery FutureWarning）至零，删除 3 个空死目录，验证 2 个非阻塞问题。pytest 104 passed, 0 warnings。**自评违规**：Plan 获批后跳过了"先在 tasks.yaml 新建任务条目"这步，直接写代码并在三任务全部 commit 后才批量补更 tasks.yaml/PROGRESS.md/telemetry。违反了任务完成协议"禁止批量补更 tracking"的约束。详情见 DECISIONS.md pitfall 和 `.harness/state/runs/2026-05-30-learnings-3.md`。
- **2026-05-30 权限清单精简**：`.claude/settings.json` 删 19 条全局 `python3`/`python`/裸 `pytest` 权限，新增 10 条 venv 上下文安全命令。核心原则：只允许 venv 隔离环境内操作，禁止使用系统全局 Python。详见 `.harness/tool/tool-manifest.md`。

## 已知问题

- ~~`backend/backend/` 空嵌套目录（已修复，2026-05-30 自检 #1）~~
- ~~代码结构违规：`core/geometry.py` 355 行、`generate_wing_3d_step()` 62 行、`coupled_optimize()` 61 行、3 个测试文件 >200 行（已修复，2026-05-30 自检 #2）~~
- ~~冲刺合同缺失：12/16 任务无合同（已补建，2026-05-30 自检 #2）~~
- ~~StarletteDeprecationWarning: httpx 应升级为 httpx2（已修复，2026-05-30 T016：pyproject.toml `httpx`→`httpx2`）~~
- ~~CadQuery FutureWarning: `save` will be removed in next release（已修复，2026-05-30 T017：pytest filterwarnings 抑制 CadQuery 内部 FutureWarning）~~
- Python 3.10.12 低于环境声明 ≥3.11（已验证不阻塞：pyproject.toml 写 ≥3.10 自洽，系统无 3.11+ 可用，功能不受限）
- ~~无 .venv 虚拟环境隔离~~（已修复，2026-05-30 自检 #2 环境修复）
- ~~`serialization/`、`models/`、`optimization/` 目录仅含 `__init__.py`，无实际实现~~（已修复，2026-05-30 T018：删除空死目录）
- ~~uvicorn 启动需先 `pip install -e .`（当前未安装 editable 模式）~~（已验证已解决：.venv 中 `pip show airfoil-platform` 确认 0.1.0 已安装）

## 下一步

1. 接入真实神经网络模型替代 stub
2. 实现前端可视化
3. LangGraph 智能体调度
4. 数据库/对象存储持久化

## 最近验证

- 命令：`source backend/.venv/bin/activate && pytest`
- 结果：**104 passed**, 0 warnings
- 证据：T016 消除 StarletteDeprecationWarning（httpx→httpx2）；T017 抑制 CadQuery 内部 FutureWarning（pytest filterwarnings）；T018 删除 3 个空死目录；Python 版本和 uvicorn 已验证不阻塞。
