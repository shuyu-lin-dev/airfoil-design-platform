# 会话退出检查清单

> **主要流程见 `.harness/instruction/rules/agent-workflow.md` § 任务完成协议。**
> 本文为补充验证项，在完成协议第 10 步（自检）时逐项核对。

每次会话结束前执行。若某项无法完成，在 `PROGRESS.md` 说明原因。

## 补充验证项

- [ ] 测试通过：`cd backend && source .venv/bin/activate && pytest`
- [ ] 无调试代码残留：临时脚本、print 调试、未说明的半成品
- [ ] 标准启动路径可用：`cd backend && source .venv/bin/activate && uvicorn airfoil_platform.main:app --reload`
- [ ] `.harness/state/working/` 已清理（除 `.gitkeep`）
- [ ] 阻塞项和下一步已在 `PROGRESS.md` 明确记录
- [ ] 若涉及领域术语歧义，同步更新 `CONTEXT.md` § Flagged ambiguities
