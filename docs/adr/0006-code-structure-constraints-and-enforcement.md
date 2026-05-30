# ADR 0006: 代码结构约束与自动化执行

> 日期：2026-05-29（原始），2026-05-30（从 DECISIONS.md 提炼为 ADR）
> 状态：accepted

## 背景

Agent 可能写出 god file、单体函数或悄悄引入新库。需要硬性约束在代码生成前生效，属于结构性防线而非 code review 事后纠正。

## 决策

1. **文件 ≤200 行**，**函数 ≤50 行**——硬性上限，不是建议。合理的文件组织可能自然远低于上限。
2. **新增第三方依赖必须经用户确认**——无论是 `pip install` 还是写入 `pyproject.toml`。
3. **pre-commit 自动检查**：`.pre-commit-config.yaml` + `pre-commit-check.py` 在每次 `git commit` 时自动检查 `backend/src/` 和 `backend/tests/` 下的 Python 文件——文件行数、函数长度、无 `print()` 调试残留。违反时阻止提交。

## 原因

- 这些约束在 agent 生成代码前就生效，是结构性防线。
- pre-commit hook 将"被动规则"变为"主动拦截"——代码进入仓库前就阻止违规。
- 200 行和 50 行是经过验证的实用上限——不是让每个文件/函数都接近上限，而是防止个别文件膨胀失控。

## 约束

- pre-commit hook 只检查 `backend/src/` 和 `backend/tests/` 下的 `.py` 文件。
- 若任务需要正当超标（如 CAD kernel 初始化代码），需在 `DECISIONS.md` 中记录例外并说明原因。
- 上限是硬性的，不是建议。

## 否决方案

- 不做硬性上限，仅作为建议——模型对"建议"的遵守率远低于硬约束。
- 设更严格的限制（100 行/30 行）——会过度碎片化，增加模块间通信成本。
- 在 CI 中做检查而非 pre-commit——CI 反馈太慢，违规代码已经 push。
