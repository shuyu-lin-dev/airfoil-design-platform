# 会话退出检查清单

每次会话结束前执行（包括普通结束和 50% 上下文主动交接）。若某项无法完成，在 `PROGRESS.md` 说明原因。

- [ ] 测试通过：`cd backend && pytest`（`backend/` 未创建时说明原因）
- [ ] 完整验证通过：见当前任务 `validation.commands`
- [ ] `tasks/tasks.yaml` 状态和 `evidence` 已更新
- [ ] `PROGRESS.md` 已更新当前状态、最近验证、阻塞和下一步
- [ ] `DECISIONS.md` 已补充关键选择
- [ ] 若为 50% 主动交接：`.harness/state/runs/YYYY-MM-DD-HHMM-handoff.md` 已写入
- [ ] 若为 50% 主动交接或 `/compact`：已保留架构决策、当前任务状态、待办、验证证据、阻塞项和已改文件
- [ ] 无调试代码残留：临时脚本、print 调试、未说明的半成品
- [ ] `.harness/state/working/` 已清理（除 `.gitkeep`），值得保留的发现已升级到 `PROGRESS.md` 或 `DECISIONS.md`
- [ ] 标准启动路径可用：`cd backend && uvicorn airfoil_platform.main:app --reload`
- [ ] 阻塞项和下一步已明确记录
- [ ] 若本次会话发现新的陷阱、反模式、边界条件或规则改进：
      写入 `.harness/state/runs/YYYY-MM-DD-learnings.md`
      并在 `PROGRESS.md` 的「下一步」中标注待审核的知识条目
      若涉及领域术语歧义，同步更新 `CONTEXT.md` § Flagged ambiguities
- [ ] 运行遥测已记录：复制 `.harness/state/runs/telemetry.yaml` 模板，填写本次会话的 run 记录（task_id、status、duration_min、model、token_estimate、tool_calls、failures），并滚动更新 cumulative 区块
