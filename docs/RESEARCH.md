# Research log · 2026-09-29

The design began with ordinary-prompt model advice and was extended to
user-mediated project handoffs with a persistent main-window integrator.

## Related work inspected

| Project | What its inspected source describes | Design implication |
|---|---|---|
| [richard-gyiko/which-llm](https://github.com/richard-gyiko/which-llm) | CLI and skill; task classification, benchmark/capability/cost queries and recommendations | Credit existing task classification. PromptHarbor emphasizes narrow evidence scope and shared-contract project handoffs. |
| [RouteLLM](https://github.com/lm-sys/RouteLLM) | Learned routing between strong and weak models; serving and evaluation tooling | Useful for automatic cost-quality dispatch, but this project produces human-readable advice and portable prompts. |
| [RouterBench](https://arxiv.org/abs/2403.12031) | Multi-model routing benchmark and quality-cost evaluation | Evaluate routing on outcomes; do not mistake a transparent heuristic for a trained, validated router. |

The name “which-llm” can refer to different projects. The comparison above applies
only to the linked repository, not to hardware-fitting projects with similar
names. PromptHarbor does not default to local deployment or hardware selection.
No competitor source code was copied.

## Sources admitted

Official catalogs were inspected for exact names, modalities, context and
availability: [OpenAI Astra](https://developers.openai.com/api/docs/models/gpt-6-astra),
[Sol](https://developers.openai.com/api/docs/models/gpt-6-sol),
[Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
[Claude](https://platform.claude.com/docs/en/models/overview),
[Gemini](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash),
and [Grok](https://docs.x.ai/developers/models/grok-4.7).
Provider cards were inspected for
[DeepSeek](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash),
[Qwen](https://huggingface.co/Qwen/Qwen3.8-27B) and
[Kimi](https://huggingface.co/moonshotai/Kimi-K3).
These cards are vendor evidence even when hosted on Hugging Face.

[Artificial Analysis's Astra evaluation](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra)
illustrates why harnesses matter: its coding-agent and general evaluation setups
report different terminal results. PromptHarbor stores one explicitly named
setup rather than merging scores.

[Vals Finance Agent v2](https://www.vals.ai/benchmarks/fabv2) concerns analyst work
on company filings. Its partial-credit and all-pass orderings differ. The catalog
does not extend these results to strategy returns, factor robustness or backtest
correctness.

[Opus 5.5](https://www.anthropic.com/claude-opus-5-5) and
[Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) release reports disclose
effort and fallback details. The catalog preserves vendor provenance instead of
presenting release comparisons as independently reproduced scores.

[FrontierMath Tier 4 v2](https://epoch.ai/benchmarks/frontiermath-tier-4-v2)
documents research-level mathematical tasks and a versioned methodology. A
readable current per-model result was not established from the inspected page,
so no numeric FrontierMath winner was admitted.

## What was deliberately not promoted

Search results exposed model rankings, news roundups and community anecdotes.
Those were discovery leads only. No third-party roundup, search snippet, rumored
model or anonymous style claim is used as an admitted performance observation.
The seed has no community-test records; the format supports reproducible ones.

Coverage is limited to verified candidates in this pass. Meta, Mistral, MiniMax,
Z.ai, Xiaomi and specialist audio/image/proof systems are future discovery targets,
not implicitly weaker models. Live routing should check relevant missing models.
No full benchmark dataset was copied and no paid API comparison was run.

## Architecture decisions

1. **Semantic host, deterministic helpers.** The existing agent interprets intent
   and reads current sources. No extra API credential is needed. Regex fallback
   is visibly limited and not marketed as arbitrary-prompt intelligence.
2. **Atomic claims.** Store sources, model facts, task vocabulary and evidence
   separately. Unknowns stay unknown. Raw scores are not combined into one number.
3. **Project interfaces before assignment.** Frozen shared contracts and ownership
   prevent separately generated components from becoming incompatible projects.
4. **Main-window integration.** Portable prompts let the user choose platforms;
   returning artifacts have an explicit review and acceptance path.
5. **Conservative updates.** Review dates, result dates and lifecycle checks are
   different. Scheduled checks report work; reviewers admit evidence changes.

These decisions are engineering judgments, not externally validated claims of
superior recommendation accuracy. See the behavioral evaluation rubric before
making such a claim.
