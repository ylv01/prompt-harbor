# Task coverage and gaps

Snapshot: **2026-10-08**. Generated from the catalog; not a quality leaderboard.

Catalog: **17 models · 49 tasks · 149 evidence records · 101 sources**.

Direct means a task-mapped measurement, not guaranteed transfer to the user’s prompt.
Capability/proxy includes product support and adjacent-task inference. Missing means no admitted evidence.
All task mappings are editorial judgments. Community reports include signed counterevidence, not just endorsements.

| Task | Domain / subdomain | Independent measurement | Vendor measurement | Capability / proxy | Community reports |
|---|---|---|---|---|---|
| `software.debug` | Software / Maintenance | — | glm-5.3, glm-5.3-flash | claude-fable-5-1, claude-haiku-5-5, claude-opus-5-5, claude-sonnet-5-5, glm-5.3, glm-5.3-flash, gpt-6-astra, gpt-6.1-sol, grok-4.7, mimo-v2.6-flash, mimo-v2.6-pro | claude-opus-5-5 (mixed), claude-opus-5-5 (positive), claude-sonnet-5-5 (negative), claude-sonnet-5-5 (positive), deepseek-v4.1-flash (negative), deepseek-v4.1-flash (positive), glm-5.3 (positive), glm-5.3-flash (positive), grok-4.7 (mixed), mimo-v2.6-flash (negative), mimo-v2.6-flash (positive), mimo-v2.6-pro (positive) |
| `software.repo` | Software / Maintenance | — | claude-opus-5-5, deepseek-v4.1-flash, glm-5.3, glm-5.3-flash, qwen3.8-27b | claude-fable-5-1, claude-haiku-5-5, claude-opus-5-5, claude-sonnet-5-5, glm-5.3, glm-5.3-flash, gpt-6-astra, gpt-6.1-sol, grok-4.7, mimo-v2.6-flash, mimo-v2.6-pro, mimo-v2.6-pro-ultraspeed | claude-opus-5-5 (mixed), claude-opus-5-5 (negative), claude-opus-5-5 (positive), claude-sonnet-5-5 (negative), claude-sonnet-5-5 (positive), deepseek-v4.1-flash (negative), deepseek-v4.1-flash (positive), gemini-3.8-flash (mixed), gemini-3.8-flash (positive), glm-5.3 (positive), glm-5.3-flash (negative), glm-5.3-flash (positive), gpt-6-luna (mixed), grok-4.7 (mixed), kimi-k3 (mixed), mimo-v2.6-flash (mixed), mimo-v2.6-flash (positive), mimo-v2.6-pro (negative) |
| `software.algorithm` | Software / Algorithms | — | deepseek-v4.1-flash, qwen3.8-27b | — | glm-5.3 (positive) |
| `software.frontend` | Software / Interfaces | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, deepseek-v4.1-flash, gemini-3.8-flash, glm-5.3, glm-5.3-flash, gpt-6-astra, gpt-6-luna, gpt-6.1-sol, grok-4.7, kimi-k3, mimo-v2.6-flash, mimo-v2.6-pro, qwen3.8-27b | — | claude-sonnet-5-5, glm-5.3-flash, mimo-v2.6-flash, mimo-v2.6-pro, mimo-v2.6-pro-ultraspeed | claude-fable-5-1 (mixed), claude-fable-5-1 (positive), deepseek-v4.1-flash (positive), gemini-3.8-flash (mixed), glm-5.3 (positive), glm-5.3-flash (mixed), gpt-6-astra (positive), gpt-6.1-sol (negative), grok-4.7 (mixed), grok-4.7 (negative), kimi-k3 (negative), kimi-k3 (positive), mimo-v2.6-flash (negative), mimo-v2.6-pro (negative), mimo-v2.6-pro-ultraspeed (mixed) |
| `software.security` | Software / Security | — | glm-5.3 | — | kimi-k3 (mixed), mimo-v2.6-pro (negative) |
| `software.architecture` | Software / Architecture | — | — | glm-5.3, glm-5.3-flash, gpt-6-astra | gpt-6.1-sol (positive), grok-4.7 (mixed), kimi-k3 (mixed), mimo-v2.6-pro (negative) |
| `software.terminal` | Software / Tools | gpt-6-astra | claude-fable-5-1, claude-haiku-5-5, claude-opus-5-5, claude-sonnet-5-5, deepseek-v4.1-flash, glm-5.3, glm-5.3-flash | mimo-v2.6-flash, mimo-v2.6-pro | claude-opus-5-5 (mixed), claude-sonnet-5-5 (positive), glm-5.3-flash (negative), mimo-v2.6-flash (mixed), mimo-v2.6-flash (negative), mimo-v2.6-flash (positive), mimo-v2.6-pro (negative) |
| `software.testing` | Software / Quality | — | — | claude-opus-5-5, glm-5.3, glm-5.3-flash | claude-opus-5-5 (negative), claude-sonnet-5-5 (positive), grok-4.7 (negative), kimi-k3 (mixed) |
| `math.contest` | Mathematics / Problem solving | — | deepseek-v4.1-flash | glm-5.3, glm-5.3-flash | — |
| `math.proof` | Mathematics / Proof | — | — | deepseek-v4.1-flash, gpt-6-astra | — |
| `math.formal` | Mathematics / Formal verification | — | — | — | — |
| `math.numerical` | Mathematics / Computation | — | — | gpt-6-astra | — |
| `finance.filings` | Finance / Fundamental analysis | gemini-3.8-flash | — | glm-5.3-flash | — |
| `finance.valuation` | Finance / Fundamental analysis | — | — | gemini-3.8-flash, glm-5.3-flash | — |
| `finance.backtest` | Finance / Quantitative research | — | — | claude-opus-5-5, deepseek-v4.1-flash, qwen3.8-27b | — |
| `finance.factor` | Finance / Quantitative research | — | — | claude-opus-5-5, deepseek-v4.1-flash, qwen3.8-27b | — |
| `finance.derivatives` | Finance / Quantitative research | — | — | deepseek-v4.1-flash | — |
| `science.reasoning` | Science / Domain reasoning | — | deepseek-v4.1-flash | claude-opus-5-5, glm-5.3, glm-5.3-flash, gpt-6-astra | — |
| `science.compute` | Science / Computational research | — | claude-opus-5-5, kimi-k3 | gpt-6-astra | — |
| `science.literature` | Science / Literature | — | — | gemini-3.8-flash, kimi-k3 | — |
| `science.hypothesis` | Science / Discovery | — | — | — | — |
| `writing.creative` | Writing / Creative | — | — | claude-sonnet-5-5 | glm-5.3 (negative), gpt-6-astra (mixed), gpt-6.1-sol (mixed), mimo-v2.6-pro (positive) |
| `writing.edit` | Writing / Editing | — | — | claude-sonnet-5-5 | claude-fable-5-1 (mixed), claude-fable-5-1 (positive) |
| `writing.professional` | Writing / Professional | — | — | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, glm-5.3-flash, gpt-6-astra, gpt-6.1-sol, grok-4.7 | claude-fable-5-1 (mixed), claude-fable-5-1 (positive), claude-opus-5-5 (mixed), claude-sonnet-5-5 (positive) |
| `writing.translation` | Writing / Multilingual | — | — | gpt-6-luna | qwen3.8-27b (positive) |
| `context.retrieve` | Long context / Retrieval | — | — | — | claude-haiku-5-5 (negative) |
| `context.synthesis` | Long context / Synthesis | gpt-6-astra | kimi-k3 | claude-fable-5-1, claude-opus-5-5, glm-5.3-flash | qwen3.8-27b (negative) |
| `context.summary` | Long context / Compression | — | — | claude-haiku-5-5, gpt-6-luna | gemini-3.8-flash (positive), gpt-6-luna (positive) |
| `agent.workflow` | Agents / Tool use | gpt-6-astra | glm-5.3, glm-5.3-flash, kimi-k3 | gemini-3.8-flash, gpt-6.1-sol, grok-4.7, mimo-v2.6-flash, mimo-v2.6-pro, mimo-v2.6-pro-ultraspeed | claude-fable-5-1 (mixed), claude-haiku-5-5 (mixed), deepseek-v4.1-flash (negative), gpt-6-luna (positive), gpt-6.1-sol (positive), qwen3.8-27b (negative), qwen3.8-27b (positive) |
| `agent.computer` | Agents / Computer use | — | claude-haiku-5-5, qwen3.8-27b | glm-5.3-flash, gpt-6-astra, gpt-6.1-sol, mimo-v2.6-flash, mimo-v2.6-pro | qwen3.8-27b (positive) |
| `agent.long` | Agents / Planning | — | — | claude-fable-5-1, claude-opus-5-5, glm-5.3, glm-5.3-flash, gpt-6-astra, mimo-v2.6-flash, mimo-v2.6-pro, mimo-v2.6-pro-ultraspeed | claude-fable-5-1 (mixed), glm-5.3-flash (negative), glm-5.3-flash (positive), kimi-k3 (mixed), mimo-v2.6-flash (negative), mimo-v2.6-pro (negative), qwen3.8-27b (negative) |
| `vision.chart` | Vision / Reasoning | — | claude-haiku-5-5, claude-opus-5-5, claude-sonnet-5-5, deepseek-v4.1-flash, qwen3.8-27b | — | gemini-3.8-flash (positive) |
| `vision.document` | Vision / Documents | — | qwen3.8-27b | glm-5.3-flash | claude-fable-5-1 (positive), gemini-3.8-flash (positive) |
| `vision.video` | Vision / Temporal | — | — | gemini-3.8-flash, glm-5.3-flash, kimi-k3 | gemini-3.8-flash (positive) |
| `vision.spatial` | Vision / Spatial reasoning | — | — | glm-5.3-flash | — |
| `research.web` | Research / Web investigation | — | kimi-k3 | claude-fable-5-1, claude-opus-5-5, gemini-3.8-flash, gpt-6-astra | — |
| `research.facts` | Research / Verification | — | — | gemini-3.8-flash, gpt-6-astra | — |
| `data.analysis` | Data / Analysis | claude-haiku-5-5 | — | gemini-3.8-flash | — |
| `data.sql` | Data / Querying | claude-haiku-5-5 | — | — | — |
| `data.extract` | Data / Extraction | — | — | claude-haiku-5-5, gpt-6-luna | claude-haiku-5-5 (mixed), claude-haiku-5-5 (negative), gemini-3.8-flash (positive) |
| `data.spreadsheet` | Data / Spreadsheets | — | kimi-k3 | claude-sonnet-5-5, glm-5.3-flash | — |
| `audio.understand` | Audio / Understanding | — | — | gemini-3.8-flash | — |
| `education.tutor` | Education / Learning | — | — | gpt-6-luna | — |
| `professional.legal` | Professional / Legal | — | — | — | — |
| `professional.medical` | Professional / Medical | — | — | — | — |
| `general.everyday` | General / Everyday | — | — | gpt-6-luna | — |
| `data.schema` | Data / Database design | — | — | — | — |
| `software.frontend.design` | Software / Interface design | — | — | claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, deepseek-v4.1-flash, gemini-3.8-flash, glm-5.3, glm-5.3-flash, gpt-6-astra, gpt-6-luna, gpt-6.1-sol, grok-4.7, kimi-k3, mimo-v2.6-flash, mimo-v2.6-pro, qwen3.8-27b | claude-fable-5-1 (mixed), claude-fable-5-1 (positive), deepseek-v4.1-flash (positive), gemini-3.8-flash (mixed), glm-5.3-flash (mixed), gpt-6-astra (positive), gpt-6.1-sol (negative), grok-4.7 (mixed), grok-4.7 (negative), kimi-k3 (negative), kimi-k3 (positive) |
| `software.frontend.fidelity` | Software / Interface fidelity | — | — | glm-5.3-flash, mimo-v2.6-flash, mimo-v2.6-pro | mimo-v2.6-pro-ultraspeed (mixed) |

## Explicit gaps

`math.formal`, `science.hypothesis`, `professional.legal`, `professional.medical`, `data.schema`

These tasks are recognizable even when the catalog cannot establish a winner. Research live evidence, retain a feasible current model as a baseline, or propose a task trial.

## Admitted sources

- [GPT-6 Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) — OpenAI; checked 2026-09-29; publication not established.
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
- [Arena WebDev overall snapshot](https://arena.ai/leaderboard/code) — Arena; checked 2026-09-29; publication 2026-09-25.
- [AI Lab: authored web-generation experiments](https://neuralhub.dev/ai-test-results) — neuralhub.dev / Leandro; checked 2026-09-29; publication not established.
- [First-person Kimi UI usage and quota report](https://www.reddit.com/r/kimi/comments/1vconet/comment/p157lwe/) — Reddit / Cachesmr; checked 2026-09-29; publication not established.
- [First-person competing UI preference](https://www.reddit.com/r/kimi/comments/1vconet/comment/p2cjso7/) — Reddit / Bright_Spend6574; checked 2026-09-29; publication not established.
- [GPT-6.1 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol) — OpenAI; checked 2026-10-08; publication not established.
- [Xiaomi MiMo official API pricing](https://mimo.mi.com/docs/en-US/price/pay-as-you-go) — Xiaomi; checked 2026-09-30; publication not established.
- [Xiaomi MiMo model releases](https://mimo.mi.com/docs/en-US/updates/model) — Xiaomi; checked 2026-09-30; publication not established.
- [Xiaomi MiMo model deprecation schedule](https://mimo.mi.com/docs/en-US/updates/deprecate) — Xiaomi; checked 2026-09-30; publication not established.
- [Xiaomi MiMo model capability table](https://mimo.mi.com/docs/en-US/quick-start/model) — Xiaomi; checked 2026-09-30; publication not established.
- [MiMo-V2.6 launch announcement](https://mimo.mi.com/docs/en-US/news/latest/v2-6) — Xiaomi; checked 2026-09-30; publication 2026-09-22.
- [Diagnosing and Mitigating Tool-Call Repetition in MiMo-V2.6](https://mimo.xiaomi.com/blog/mimo-v2-6-tool-call-repetition) — Xiaomi; checked 2026-09-30; publication 2026-09-27.
- [MiMo-V2.6-Pro-MOPD official checkpoint](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-MOPD) — Xiaomi; checked 2026-09-30; publication not established.
- [MiMo-V2.6-Flash-MOPD official checkpoint](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-MOPD) — Xiaomi; checked 2026-09-30; publication not established.
- [Xiaomi MiMo-V2.6-Pro official model page](https://mimo.mi.com/models/zh-CN/mimo-v2.6-pro) — Xiaomi; checked 2026-09-30; publication not established.
- [Xiaomi MiMo-V2.6-Flash official model page](https://mimo.mi.com/models/zh-CN/mimo-v2.6-flash) — Xiaomi; checked 2026-09-30; publication not established.
- [Xiaomi MiMo-V2.6-Pro-UltraSpeed official model page](https://mimo.mi.com/models/zh-CN/mimo-v2.6-pro-ultraspeed) — Xiaomi; checked 2026-09-30; publication not established.
- [MiMo-V2.6-Pro-RL official model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL) — Xiaomi; checked 2026-09-30; publication 2026-09-22.
- [MiMo-V2.6-Flash-RL official model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL) — Xiaomi; checked 2026-09-30; publication 2026-09-22.
- [Astra built the author’s portfolio](https://www.najam.pk/blog/gpt-6-astra-review) — Najam Saeed; checked 2026-09-30; publication 2026-09-01.
- [Scriptwriting comparison: Astra](https://www.reddit.com/r/LLMDevs/comments/1wtmb3m/gpt61_sol_seems_like_a_step_back_for_writing/) — OnlyProggingForFun; checked 2026-09-30; publication not established.
- [Sol repaired an agentic wiki](https://www.reddit.com/r/openclaw/comments/1wrgu8e/how_is_gpt6luna_so_good/) — ilias_from_ilios; checked 2026-09-30; publication not established.
- [Ten engineering tasks: Luna version comparison](https://www.reddit.com/r/codex/comments/1wp7ckc/i_ab_tested_gpt56_luna_and_gpt6_luna_on_the_same/) — rundef; checked 2026-09-30; publication not established.
- [6.1 Sol planner with a local Qwen coder](https://www.reddit.com/r/ChatGPT/comments/1wtqp7l/using_gpt61_sol_only_as_the_planner_and_letting_a/) — GapNew4766; checked 2026-09-30; publication not established.
- [6.1 Sol medium: safari game complaint](https://www.reddit.com/r/OpenaiCodex/comments/1wtrad9/gpt_61_sol_has_been_pretty_disappointing_that_i/) — Upper-Animator-5067; checked 2026-09-30; publication not established.
- [Opus 5.5 found two defects in the author's Stackchan/Home Assistant code](https://digitalhandwerk.rocks/ki/testbericht-zu-claude-opus-5-5-und-fehleranalyse/) — Alex Januschewsky; checked 2026-09-30; publication 2026-09-23.
- [Three-run skill comparison: Opus 5.5 and Sonnet 5.5](https://www.reddit.com/r/ClaudeAI/comments/1wtend0/tested_sonnet_55_vs_opus_55_with_the_same_skills/) — maverick_man1111; checked 2026-09-30; publication not established.
- [Opus 5.5 versus Sonnet 5.5 on a large test refactor](https://www.reddit.com/r/ClaudeCode/comments/1wtdgwy/where_does_sonnet_55_actually_fit_into_your_agent/) — Outrageous-Issue9722 (comment); checked 2026-09-30; publication not established.
- [Sonnet 5.5 high left bugs and required expensive rework](https://www.reddit.com/r/ClaudeCode/comments/1wsqfzk/sonnet_55_is_not_worth_using_it_unless_at_lowmed/) — msw3age (comment); checked 2026-09-30; publication not established.
- [Fable 5.1 structured a draft from handwritten notes](https://aaronmakelky.com/blog/astra-vs-fable) — Aaron Makelky; checked 2026-09-30; publication 2026-09-15.
- [Seven-chapter Fable 5.1 rewrite still needed voice editing](https://ainativeproductmanager.com/field-notes/fable-5-1-first-impressions) — AI-Native PM authors (Girish PM origin); checked 2026-09-30; publication 2026-09-02.
- [Fable 5.1 animated SVG and rocket-page build-off](https://www.bitsminds.com/news/grok-4-7-vs-fable-5-1-vs-astra-6-build-off-2026) — BitsMinds hands-on reviewers; checked 2026-09-30; publication 2026-09-21.
- [Plotline screenshot-to-data app worked from one prompt](https://promptslove.com/blog/gemini-3-8-flash-review/) — Ramanpal Singh; checked 2026-09-30; publication 2026-09-03.
- [Gemini 3.8 Flash game prototypes: simpler worlds versus broken 3D action](https://rutinelabo.com/gemini-38-flash-review/) — せなお / Routine Labo; checked 2026-09-30; publication 2026-09-08.
- [Grok 4.7 on a large Rust repository in Cursor](https://www.reddit.com/r/cursor/comments/1wrktgc/am_i_the_only_one_who_thinks_grok_47_is_actually/) — akeebismail; checked 2026-09-30; publication not established.
- [Four Grok 4.7 visual builds shipped user-visible defects](https://www.bitsminds.com/reviews/grok-4-7-review) — BitsMinds hands-on reviewers; checked 2026-09-30; publication 2026-09-22.
- [Grok 4.7 animated SVG pelican comparison](https://www.reddit.com/r/grok/comments/1wp5iwr/grok_47_was_supposed_to_crush_opus_and_gpt6_then/) — Obligation19; checked 2026-09-30; publication not established.
- [DeepSeek 4.1 Flash surprised me — 6 minutes, one attempt, $0.07](https://www.reddit.com/r/DeepSeek/comments/1wcj9ux/deepseek_41_flash_surprised_me_6_minutes_one/) — nehuenpereyra; checked 2026-09-30; publication not established.
- [DeepSeek V4.1 Flash is cheap per token—but is it actually cheap per completed task?](https://www.reddit.com/r/DeepSeek/comments/1wdd9hh/deepseek_v41_flash_is_cheap_per_tokenbut_is_it/) — Logical_Catch_3207; checked 2026-09-30; publication not established.
- [DeepSeek v4.1 Flash is truly amazing](https://www.reddit.com/r/DeepSeek/comments/1wgohh2/deepseek_v41_flash_is_truly_amazing/) — danilofs; checked 2026-09-30; publication not established.
- [Qwen3.8-27B Trial Report (with Addendum)](https://note.com/a_matsukaze/n/n9796f33ac3c5?hl=en) — A. Matsukaze; checked 2026-09-30; publication 2026-08-15.
- [Disappointed in Ninfer + Qwen 3.8-27B:nvfp4](https://www.reddit.com/r/LocalLLM/comments/1wlze6z/disappointed_in_ninfer_qwen_3827bnvfp4/) — michmill1970; checked 2026-09-30; publication not established.
- [I gave a local Qwen3.8 27B agent my Amazon account — and it bought paper for me](https://www.reddit.com/r/LocalLLaMA/comments/1wn0mm4/i_gave_a_local_qwen38_27b_agent_my_amazon_account/) — fuzhongkai; checked 2026-09-30; publication not established.
- [LLM Benchmark: Has Kimi K3 Reached Claude Opus Level?](https://akitaonrails.com/en/2026/07/17/llm-benchmarks-kimi-k3/) — Fabio Akita; checked 2026-09-30; publication 2026-07-17.
- [Kimi K3 with Context Tree Beats GPT 5.6 Sol on a Real Engineering Task](https://www.reddit.com/r/kimi/comments/1vba5ie/kimi_k3_with_context_tree_beats_gpt_56_sol_on_a/) — Still_Amphibian545 / First Tree team; checked 2026-09-30; publication not established.
- [Short review about the mimo 2.6 pro model](https://www.reddit.com/r/opencodeCLI/comments/1wmv8nn/short_review_about_the_mimo_26_pro_model/) — irukadesune; checked 2026-09-30; publication not established.
- [Mimo 2.6 Pro feedback after 7 hours of testing](https://www.reddit.com/r/DeepSeek/comments/1wn3p6b/mimo_26_pro_feedback_after_7_hours_of_testing/) — Civil-Direction-6981; checked 2026-09-30; publication not established.
- [MiMo-V2.6 (both Pro and Flash) is a benchmaxxed scam](https://www.reddit.com/r/LocalLLaMA/comments/1woa5d3/mimov26_both_pro_and_flash_is_a_benchmaxxed_scam/) — crusaderky; checked 2026-09-30; publication not established.
- [Opinions on the new mimo 2.6? — Pro-version roleplay comment](https://www.reddit.com/r/SillyTavernAI/comments/1wn5nf4/opinions_on_the_new_mimo_26/) — LordVulpius; checked 2026-09-30; publication not established.
- [For me, DS v4.1 is way better than mimo v2.6](https://www.reddit.com/r/CommandCode/comments/1wmvmut/for_me_ds_v41_is_way_better_than_mimo_v26/) — choiyoh; checked 2026-09-30; publication not established.
- [Mimo 2.6 Flash is a beast and seems to use very low token count](https://www.reddit.com/r/opencode/comments/1wn191t/mimo_26_flash_is_a_beast_and_seems_to_use_very/) — Leather-Cod2129; checked 2026-09-30; publication not established.
- [Which do you choose: DeepSeek v4.1 Flash or MiMo V2.6 Flash — improvement comment](https://www.reddit.com/r/opencode/comments/1wp2ctx/which_do_you_choose_deepseek_v41_flash_or_mimo/) — oulu2006; checked 2026-09-30; publication not established.
- [Pretty poor results with MiMo v2.6 Flash + Hermes — opposite experience comment](https://www.reddit.com/r/hermesagent/comments/1wnkeak/pretty_poor_results_with_mimo_v26_flash_hermes/) — XKiiroiSenkoX; checked 2026-09-30; publication not established.
- [Bug: New MiMo 2.6 Flash is unusable due to it ending up in infinite loops](https://github.com/anomalyco/opencode/issues/50678) — omani; checked 2026-09-30; publication 2026-09-22.
- [MiMo 2.6 Pro UltraSpeed image-to-HTML comparison](https://news.ycombinator.com/item?id=49794584) — jjcm; checked 2026-09-30; publication not established.
- [Arena WebDev Overall — October 7, 2026](https://arena.ai/leaderboard/code/webdev) — Arena; checked 2026-10-08; publication 2026-10-07.
- [GLM-5.3 model documentation](https://docs.z.ai/guides/llm/glm-5.3) — Z.ai; checked 2026-10-08; publication not established.
- [GLM-5.3-Flash model documentation](https://docs.z.ai/guides/vlm/glm-5.3-flash) — Z.ai; checked 2026-10-08; publication not established.
- [Z.ai official USD API pricing](https://docs.z.ai/guides/overview/pricing) — Z.ai; checked 2026-10-08; publication not established.
- [GLM-5.3 official weights and evaluation card](https://huggingface.co/zai-org/GLM-5.3) — Z.ai; checked 2026-10-08; publication not established.
- [GLM-5.3-Flash official weights and evaluation settings](https://huggingface.co/zai-org/GLM-5.3-Flash) — Z.ai; checked 2026-10-08; publication not established.
- [GLM-5.3-Flash official machine-readable evaluation results](https://huggingface.co/zai-org/GLM-5.3-Flash/raw/main/.eval_results/GLM-5.3-Flash.yaml) — Z.ai; checked 2026-10-08; publication not established.
- [GLM-5.3 weight license](https://huggingface.co/zai-org/GLM-5.3/raw/main/LICENSE) — Z.ai; checked 2026-10-08; publication not established.
- [Z.ai official model release notes](https://docs.z.ai/release-notes/new-released) — Z.ai; checked 2026-10-08; publication not established.
- [GLM-5.3: nine executed Python functions, retained run aggregates](https://www.datallmlab.com/blog/glm-5-3-review.html) — Kevin Fan / DataLLM Lab; checked 2026-10-08; publication 2026-08-22.
- [GLM-5.3 daily use: coding, debugging and frontend](https://www.reddit.com/r/ZaiGLM/comments/1vs3bba/glm_53_is_my_daily_driver_and_has_a_little/) — Sensitive_Song4219; checked 2026-10-08; publication not established.
- [GLM-5.3 long roleplay: reported voice drift](https://www.reddit.com/r/SillyTavernAI/comments/1w8u98c/why_people_prefer_glm_52_than_glm_53/) — Ant-Hime; checked 2026-10-08; publication not established.
- [GLM-5.3-Flash implements planned backend and debugging work](https://www.reddit.com/r/opencode/comments/1wroplu/xiaomi_mimo_26_flash_vs_glm_53_flash/) — Winter-Bit2411; checked 2026-10-08; publication not established.
- [GLM-5.3-Flash Devin Desktop tool-schema error loop](https://www.reddit.com/r/CognitionLabs/comments/1whs4oj/bug_report_glm53_flash_model_gets_stuck_in_a/) — Sensitive-Bottle4165; checked 2026-10-08; publication 2026-09-16.
- [GLM-5.3-Flash frontend renders: strong simple pages, weak dense-dashboard accessibility](https://samihedhli.com/articles/glm-5-3-flash-frontend-benchmark/) — Sami Hedhli; checked 2026-10-08; publication not established.
- [Claude Haiku 5.5 model documentation](https://platform.claude.com/docs/en/models/haiku-5-5/overview) — Anthropic; checked 2026-10-08; publication 2026-10-07.
- [Claude Haiku 5.5 release evaluation](https://www.anthropic.com/claude-haiku-5-5) — Anthropic; checked 2026-10-08; publication 2026-10-07.
- [Plotly Haiku 5.5 data analytics exam](https://plotly.com/blog/claude-haiku-5-5-plotly-data-analytics-bench/) — Plotly; checked 2026-10-08; publication not established.
- [Rundown's Haiku 5.5 message-routing fixture](https://app.therundown.ai/guides/claude-haiku-workflows) — The Rundown; checked 2026-10-08; publication 2026-10-07.
- [Haiku 5.5 structured-extraction batch runs](https://github.com/kotwal-itpro/steadybatch) — Ankur Kotwal; checked 2026-10-08; publication 2026-10-07.
- [Haiku 5.5 book-line attribution and context reports](https://www.reddit.com/r/ClaudeAI/comments/1x0829f/haiku_55_token_usage/) — Reddit r/ClaudeAI; checked 2026-10-08; publication not established.
- [Claude API official pricing](https://platform.claude.com/docs/en/about-claude/pricing) — Anthropic; checked 2026-10-08; publication not established.
- [Xiaomi MiMo official API pricing](https://mimo.mi.com/docs/en-US/price/pay-as-you-go) — Xiaomi; checked 2026-10-08; publication not established.
- [Kimi API official model pricing](https://platform.kimi.ai/) — Moonshot AI; checked 2026-10-08; publication not established.
- [Gemini Developer API official pricing](https://ai.google.dev/gemini-api/docs/pricing) — Google; checked 2026-10-08; publication not established.
- [DeepSeek API official pricing](https://api-docs.deepseek.com/quick_start/pricing/) — DeepSeek; checked 2026-10-08; publication not established.
- [Grok 4.7 release and long-context pricing](https://docs.x.ai/developers/release-notes) — SpaceXAI; checked 2026-10-08; publication not established.
- [GPT-6 Astra model documentation — API pricing](https://developers.openai.com/api/docs/models/gpt-6-astra) — OpenAI; checked 2026-10-08; publication not established.
- [GPT-6 Luna model documentation — API pricing](https://developers.openai.com/api/docs/models/gpt-6-luna) — OpenAI; checked 2026-10-08; publication not established.
- [GPT-6.1 Sol model documentation — API pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol) — OpenAI; checked 2026-10-08; publication not established.
