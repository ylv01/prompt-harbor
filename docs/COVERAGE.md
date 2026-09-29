# Task coverage and gaps

Snapshot: **2026-09-29**. Generated from the catalog; not a quality leaderboard.

Direct means a task-mapped measurement, not guaranteed transfer to the user’s prompt.
Capability/proxy includes product support and adjacent-task inference. Missing means no admitted evidence.
All task mappings are editorial judgments. Vendor and independent measurements are separated.

| Task | Domain / subdomain | Independent measurement | Vendor measurement | Capability / proxy |
|---|---|---|---|---|
| `software.debug` | Software / Maintenance | — | — | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, gpt-6-astra, gpt-6-sol, grok-4.7 |
| `software.repo` | Software / Maintenance | — | claude-opus-5-5, deepseek-v4.1-flash, qwen3.8-27b | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, gpt-6-astra, gpt-6-sol, grok-4.7 |
| `software.algorithm` | Software / Algorithms | — | deepseek-v4.1-flash, qwen3.8-27b | — |
| `software.frontend` | Software / Interfaces | — | — | claude-sonnet-5-5 |
| `software.security` | Software / Security | — | — | — |
| `software.architecture` | Software / Architecture | — | — | gpt-6-astra, gpt-6-sol |
| `software.terminal` | Software / Tools | gpt-6-astra | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, deepseek-v4.1-flash | — |
| `software.testing` | Software / Quality | — | — | claude-opus-5-5, gpt-6-sol |
| `math.contest` | Mathematics / Problem solving | — | deepseek-v4.1-flash | — |
| `math.proof` | Mathematics / Proof | — | — | deepseek-v4.1-flash, gpt-6-astra |
| `math.formal` | Mathematics / Formal verification | — | — | — |
| `math.numerical` | Mathematics / Computation | — | — | gpt-6-astra |
| `finance.filings` | Finance / Fundamental analysis | gemini-3.8-flash | — | — |
| `finance.valuation` | Finance / Fundamental analysis | — | — | gemini-3.8-flash |
| `finance.backtest` | Finance / Quantitative research | — | — | claude-opus-5-5, deepseek-v4.1-flash, qwen3.8-27b |
| `finance.factor` | Finance / Quantitative research | — | — | claude-opus-5-5, deepseek-v4.1-flash, qwen3.8-27b |
| `finance.derivatives` | Finance / Quantitative research | — | — | deepseek-v4.1-flash |
| `science.reasoning` | Science / Domain reasoning | — | deepseek-v4.1-flash | claude-opus-5-5, gpt-6-astra |
| `science.compute` | Science / Computational research | — | claude-opus-5-5, kimi-k3 | gpt-6-astra |
| `science.literature` | Science / Literature | — | — | gemini-3.8-flash, kimi-k3 |
| `science.hypothesis` | Science / Discovery | — | — | — |
| `writing.creative` | Writing / Creative | — | — | claude-sonnet-5-5 |
| `writing.edit` | Writing / Editing | — | — | claude-sonnet-5-5 |
| `writing.professional` | Writing / Professional | — | — | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, gpt-6-astra, grok-4.7 |
| `writing.translation` | Writing / Multilingual | — | — | gpt-6-luna |
| `context.retrieve` | Long context / Retrieval | — | — | — |
| `context.synthesis` | Long context / Synthesis | gpt-6-astra | kimi-k3 | claude-fable-5-1, claude-opus-5-5 |
| `context.summary` | Long context / Compression | — | — | gpt-6-luna |
| `agent.workflow` | Agents / Tool use | gpt-6-astra | kimi-k3 | gemini-3.8-flash, gpt-6-sol, grok-4.7 |
| `agent.computer` | Agents / Computer use | — | qwen3.8-27b | gpt-6-astra |
| `agent.long` | Agents / Planning | — | — | claude-fable-5-1, claude-opus-5-5, gpt-6-astra, gpt-6-sol |
| `vision.chart` | Vision / Reasoning | — | claude-opus-5-5, claude-sonnet-5-5, deepseek-v4.1-flash, qwen3.8-27b | — |
| `vision.document` | Vision / Documents | — | qwen3.8-27b | — |
| `vision.video` | Vision / Temporal | — | — | gemini-3.8-flash, kimi-k3 |
| `vision.spatial` | Vision / Spatial reasoning | — | — | — |
| `research.web` | Research / Web investigation | — | kimi-k3 | claude-fable-5-1, claude-opus-5-5, gemini-3.8-flash, gpt-6-astra |
| `research.facts` | Research / Verification | — | — | gemini-3.8-flash, gpt-6-astra |
| `data.analysis` | Data / Analysis | — | — | gemini-3.8-flash |
| `data.sql` | Data / Querying | — | — | — |
| `data.extract` | Data / Extraction | — | — | gpt-6-luna |
| `data.spreadsheet` | Data / Spreadsheets | — | kimi-k3 | claude-sonnet-5-5 |
| `audio.understand` | Audio / Understanding | — | — | gemini-3.8-flash |
| `education.tutor` | Education / Learning | — | — | gpt-6-luna |
| `professional.legal` | Professional / Legal | — | — | — |
| `professional.medical` | Professional / Medical | — | — | — |
| `general.everyday` | General / Everyday | — | — | gpt-6-luna |
| `data.schema` | Data / Database design | — | — | — |

## Explicit gaps

`software.security`, `math.formal`, `science.hypothesis`, `context.retrieve`, `vision.spatial`, `data.sql`, `professional.legal`, `professional.medical`, `data.schema`

These tasks are recognizable even when the catalog cannot establish a winner. Research live evidence, retain a feasible current model as a baseline, or propose a task trial.

## Admitted sources

- [GPT-6 Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) — OpenAI; checked 2026-09-29; publication not established.
- [GPT-6 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-6-sol) — OpenAI; checked 2026-09-29; publication not established.
- [GPT-6 Luna model documentation](https://developers.openai.com/api/docs/models/gpt-6-luna) — OpenAI; checked 2026-09-29; publication not established.
- [Claude model overview](https://platform.claude.com/docs/en/models/overview) — Anthropic; checked 2026-09-29; publication not established.
- [Claude Opus 5.5 release evaluation](https://www.anthropic.com/claude-opus-5-5) — Anthropic; checked 2026-09-29; publication 2026-09-22.
- [Claude Sonnet 5.5 release evaluation](https://www.anthropic.com/claude-sonnet-5-5) — Anthropic; checked 2026-09-29; publication 2026-09-28.
- [Gemini 3.8 Flash documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) — Google; checked 2026-09-29; publication 2026-09-02.
- [Gemini 3.8 Flash launch](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) — Google; checked 2026-09-29; publication 2026-09-02.
- [Benchmarking GPT-6 Astra](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra) — Artificial Analysis; checked 2026-09-29; publication not established.
- [Finance Agent v2 results and methodology](https://www.vals.ai/benchmarks/fabv2) — Vals AI; checked 2026-09-29; publication 2026-09-27.
- [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) — DeepSeek; checked 2026-09-29; publication not established.
- [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B) — Qwen; checked 2026-09-29; publication not established.
- [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) — Moonshot AI; checked 2026-09-29; publication not established.
- [Grok 4.7 model documentation](https://docs.x.ai/developers/models/grok-4.7) — SpaceXAI; checked 2026-09-29; publication not established.
- [FrontierMath Tier 4 v2 methodology](https://epoch.ai/benchmarks/frontiermath-tier-4-v2) — Epoch AI; checked 2026-09-29; publication not established.
- [richard-gyiko/which-llm README](https://github.com/richard-gyiko/which-llm) — richard-gyiko; checked 2026-09-29; publication not established.
- [RouteLLM repository](https://github.com/lm-sys/RouteLLM) — LMSYS; checked 2026-09-29; publication not established.
- [RouterBench paper](https://arxiv.org/abs/2403.12031) — RouterBench authors; checked 2026-09-29; publication 2024-03-18.
