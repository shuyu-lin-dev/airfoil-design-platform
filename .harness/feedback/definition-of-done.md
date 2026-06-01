# 完成定义

> 本文定义任务完成的质量门槛。执行顺序和流程步骤见 `.harness/instruction/rules/agent-workflow.md` § 任务完成协议。两者互补：完成协议定义"按什么顺序做"，本文定义"做到什么标准才算完"。

任务完成必须同时满足：

- 范围内功能行为已实现
- 只修改当前任务 `allowed_paths` 允许的路径
- 静态检查通过：lint / typecheck / format（阶段未定义时在 `PROGRESS.md` 说明）
- 行为验证通过：`validation.commands` 已运行并通过
- 涉及跨组件修改时，端到端主流程通过
- `tasks/tasks.yaml` 中对应任务状态、证据和验证结果已更新
- `PROGRESS.md` 已记录当前状态和下一步
- 产生关键架构或流程选择时，`DECISIONS.md` 已补充
- 无临时调试代码、过期 TODO 或未说明的半成品
