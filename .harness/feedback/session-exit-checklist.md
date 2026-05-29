# 会话退出检查清单

每次会话结束前执行（包括普通结束和 60% 上下文主动交接）。若某项无法完成，在 `PROGRESS.md` 说明原因。

- [ ] 测试通过：`cd backend && pytest`（`backend/` 未创建时说明原因）
- [ ] 完整验证通过：见当前任务 `validation.commands`
- [ ] `tasks/tasks.yaml` 状态和 `evidence` 已更新
- [ ] `PROGRESS.md` 已更新当前状态、最近验证、阻塞和下一步
- [ ] `DECISIONS.md` 已补充关键选择
- [ ] 若为 60% 主动交接：`.harness/state/runs/YYYY-MM-DD-HHMM-handoff.md` 已写入
- [ ] 无调试代码残留：临时脚本、print 调试、未说明的半成品
- [ ] 标准启动路径可用：`cd backend && uvicorn airfoil_platform.main:app --reload`
- [ ] 阻塞项和下一步已明确记录
