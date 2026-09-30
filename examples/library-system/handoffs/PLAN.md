# 项目分工计划

制作一个本地图书管理系统：浏览和新增图书、查看详情、提交评分与书评。此示例不包含账号、借阅或公开部署。

集成负责人：**当前主窗口**。模型由用户选择和使用，本计划不会自动调用或切换模型。

| 项目部分 | Top 3 候选模型 | 计划默认模型 | 依赖 | 提示词 |
|---|---|---|---|---|
| 前端：图书列表、详情与书评 (`frontend`) | 1. GPT-6 Astra, 2. Claude Opus 5.5, 3. Claude Fable 5.1 | gpt-6-sol | 无 | [复制提示词](prompts/frontend.md) |
| 数据库：结构、约束与样例数据 (`database`) | 证据不足，先保留当前模型 | gpt-6-sol | 无 | [复制提示词](prompts/database.md) |
| 后端：API 与事务 (`backend`) | 1. Claude Opus 5.5, 2. DeepSeek-V4.1-Flash, 3. Qwen3.8-27B | claude-opus-5-5 | database | [复制提示词](prompts/backend.md) |
| 集成测试：真实端到端流程 (`qa`) | 1. Claude Opus 5.5, 2. GPT-6 Sol, 3. Kimi K3 | gpt-6-sol | frontend, database, backend | [复制提示词](prompts/qa.md) |

## 分工依据

- **前端：图书列表、详情与书评:** 继续以当前可用模型作为计划默认，Top 3 仍可自由选择。尚无针对同一任务的实测证明切换值得，建议先试做再决定。 [证据与缺口](prompts/frontend.evidence.json)
  来源: [Arena WebDev overall snapshot](https://arena.ai/leaderboard/code)
- **数据库：结构、约束与样例数据:** 继续以当前可用模型作为默认，尚无证据证明其他模型在该任务上更合适。 [证据与缺口](prompts/database.evidence.json)
- **后端：API 与事务:** 仓库实现有供应商测评可参考；数据库与本项目业务规则仍需独立验收，不声称它是数据库领域冠军。 [证据与缺口](prompts/backend.evidence.json)
  来源: [Claude Opus 5.5 release evaluation](https://www.anthropic.com/claude-opus-5-5), [Opus 5.5 found two defects in the author's Stackchan/Home Assistant code](https://digitalhandwerk.rocks/ki/testbericht-zu-claude-opus-5-5-und-fehleranalyse/)
- **集成测试：真实端到端流程:** 继续以当前可用模型作为计划默认，Top 3 仍可自由选择。尚无针对同一任务的实测证明切换值得，建议先试做再决定。 [证据与缺口](prompts/qa.evidence.json)
  来源: [GPT-6 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-6-sol)

## 执行顺序

1. frontend, database
2. backend
3. qa

## 主窗口集成步骤

1. 收集各模型返回的完整文件和回执，保留原始交付。
2. 运行 verify-deliveries 核对交付；回执通过仅表示交付结构完整。
3. 审查实现、修正接口不一致，在临时数据库中验证迁移，再组装项目。
4. 执行下方验收检查，修复集成问题；若契约有变更，将新版本发给受影响的任务负责人。
5. 汇报实际验证结果和剩余问题，模型自述不能代替验收。

- 主窗口对照接口约定审阅全部返回文件；把各目录拼接到新的本地演示工程。
- 在可丢弃的 PostgreSQL 16 库应用 schema、seed 与 checks.sql；复跑 seed 验证幂等。
- 安装后端依赖，执行 pytest backend/tests，再启动 API；检查 /health。
- 前端 npm install 与 npm run build；将 VITE_API_BASE_URL 指向真实服务。
- 按照 e2e/RUNBOOK.md 执行 Playwright 场景，保存真实结果；失败先修复再宣布完成。
