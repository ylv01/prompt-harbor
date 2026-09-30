# Project handoffs

制作一个本地图书管理系统：浏览和新增图书、查看详情、提交评分与书评。此示例不包含账号、借阅或公开部署。

Integration owner: **this conversation**. No models are called or changed automatically.

| Part | Top 3 choices | Planning default | Dependencies | Prompt |
|---|---|---|---|---|
| frontend | 1. GPT-6 Astra, 2. Claude Opus 5.5, 3. Claude Fable 5.1 | gpt-6-sol | None | [Copy prompt](prompts/frontend.md) |
| database | Evidence gap; baseline only | gpt-6-sol | None | [Copy prompt](prompts/database.md) |
| backend | 1. Claude Opus 5.5, 2. DeepSeek-V4.1-Flash, 3. Qwen3.8-27B | claude-opus-5-5 | database | [Copy prompt](prompts/backend.md) |
| qa | 1. Claude Opus 5.5, 2. GPT-6 Sol, 3. Kimi K3 | gpt-6-sol | frontend, database, backend | [Copy prompt](prompts/qa.md) |

## Assignment basis

- **frontend:** Keep the current feasible model as the planning baseline; Top 3 remain available choices. No matched task trial establishes a worthwhile improvement over the current model. [Evidence and gaps](prompts/frontend.evidence.json)
  Sources: [Arena WebDev overall snapshot](https://arena.ai/leaderboard/code)
- **database:** Keep the current feasible model as a baseline; no comparative task advantage is established. [Evidence and gaps](prompts/database.evidence.json)
- **backend:** 仓库实现有供应商测评可参考；数据库与本项目业务规则仍需独立验收，不声称它是数据库领域冠军。 [Evidence and gaps](prompts/backend.evidence.json)
  Sources: [Claude Opus 5.5 release evaluation](https://www.anthropic.com/claude-opus-5-5), [Opus 5.5 found two defects in the author's Stackchan/Home Assistant code](https://digitalhandwerk.rocks/ki/testbericht-zu-claude-opus-5-5-und-fehleranalyse/)
- **qa:** Keep the current feasible model as the planning baseline; Top 3 remain available choices. No matched task trial establishes a worthwhile improvement over the current model. [Evidence and gaps](prompts/qa.evidence.json)
  Sources: [GPT-6 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-6-sol)

## Execution batches

1. frontend, database
2. backend
3. qa

## Main-window integration

1. Collect exact files and receipts from each model; retain originals.
2. Run verify-deliveries. A valid receipt only means the handoff is structurally ready.
3. Review implementations, resolve interface mismatches, apply migrations in a disposable database, and assemble the project.
4. Execute the checks below. Fix integration defects; return changed contracts to affected task owners.
5. Report observed results and remaining gaps. Do not equate model self-reports with verification.

- 主窗口对照接口约定审阅全部返回文件；把各目录拼接到新的本地演示工程。
- 在可丢弃的 PostgreSQL 16 库应用 schema、seed 与 checks.sql；复跑 seed 验证幂等。
- 安装后端依赖，执行 pytest backend/tests，再启动 API；检查 /health。
- 前端 npm install 与 npm run build；将 VITE_API_BASE_URL 指向真实服务。
- 按照 e2e/RUNBOOK.md 执行 Playwright 场景，保存真实结果；失败先修复再宣布完成。
