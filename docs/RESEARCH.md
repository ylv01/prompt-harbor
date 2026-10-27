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
[Sol 6.1](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
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
The v0.2.0 update admits tiered firsthand community records as described below.

Coverage is limited to verified candidates in this pass. Meta, Mistral, MiniMax,
and specialist audio/image/proof systems are future discovery targets,
not implicitly weaker models. Live routing should check relevant missing models.
No full benchmark dataset was copied and no paid API comparison was run.

## Community and frontend update · 2026-09-29

The [Arena WebDev overall page](https://arena.ai/leaderboard/code) provides a
dated task-specific crowd-preference comparison. Ten rows matching catalog
models were admitted with the displayed effort settings. This is formal
evaluation evidence, not an additional anecdotal popularity multiplier.

[neuralhub.dev's authored experiment index](https://neuralhub.dev/ai-test-results)
links Kimi3 web artifacts. They are admitted as an artifact-backed author report;
we did not rerun generation or independently verify the output's functionality.
The [UI usage report](https://www.reddit.com/r/kimi/comments/1vconet/comment/p157lwe/)
and [contrary UI preference](https://www.reddit.com/r/kimi/comments/1vconet/comment/p2cjso7/)
provide separately attributed firsthand signals. Relative dates are retained as
unknown exact dates, discounted and bounded by first-seen expiry. Old Opus
comparisons are not relabeled as evidence about Opus 5.5.

These reports informed narrower visual-design mapping and a community channel;
they do not support backend or reference-fidelity claims. The initial community
sample concentrates on Kimi because it was the specific research question;
other models require the same balanced search for favorable and adverse reports.
See [community methodology](../skills/promptharbor/references/community.md).

## All-model community update · 2026-09-30

This pass searched every catalog model and admitted original, task-specific
reports for all 15. The [community report](COMMUNITY.md) lists editorial 0–10
ratings, original URLs, authors, artifacts, dates and limitations. Favorable and
adverse outcomes remain separate evidence rows. Search queries and admitted
evidence IDs are stored in the portable `data/community_research.json` file.
These ratings are our judgments of reported task outcomes; no generation was
rerun and no rating is represented as a measured benchmark or broad consensus.

[GPT-6.1 Sol documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
establishes the new exact model ID, image input, context, prices and Responses
tool support. Its official positioning and exact-version community reports are
stored separately; older Sol benchmark results are not copied to it.

[Xiaomi’s model catalog](https://mimo.mi.com/docs/en-US/quick-start/model)
and [pricing documentation](https://mimo.mi.com/docs/en-US/price/pay-as-you-go)
establish MiMo-V2.6-Pro, Flash and the Pro-UltraSpeed serving tier. The
[September 27 tool-repetition update](https://mimo.xiaomi.com/blog/mimo-v2-6-tool-call-repetition)
says Pro/Flash API aliases changed on September 25 and links MOPD weights.
Original RL model-card measurements are retained as adjacent-version proxy
evidence, with their original checkpoint and protocol. They are not claimed
as MOPD or UltraSpeed measured results.

Only the dated [September 22 OpenCode issue](https://github.com/anomalyco/opencode/issues/50678)
gets a documented 0.25 relevance factor for the current revision. Its exact
tool-repetition failure predates the official update; this is an editorial
discount, not an independently verified fix. Reddit reports with unknown
revision/date retain their uncertainty rather than receiving an assumed fix.

## Catalog replacement and GLM update · 2026-10-08

GPT-6 Sol has been removed from the active catalog, its evidence and resource
examples. GPT-6.1 Sol remains a separate exact version. Historical attributed
comparisons retain their actual model names; measurements are never relabeled.
Planning defaults remain optional suggestions, restricted by the user's resources.

The [October 7 Arena WebDev cohort](https://arena.ai/leaderboard/code/webdev)
admits GPT-6.1 Sol at its displayed max setting and contemporary catalog peers.
September observations remain dated and separate. These are preference results;
they do not establish code correctness, design fidelity or identical tool setups.
MiMo serving entries are not interpreted as specific downloaded checkpoints.

[OpenAI's GPT-6.1 Sol documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
was checked again: standard input/output is $2/$10 per million tokens for inputs
up to 272K, with cached input $0.10. This does not support a blanket claim that
all requests cost less or every task improves over a predecessor. Effort, context
and service tiers still affect actual task cost.

[GLM-5.3](https://docs.z.ai/guides/llm/glm-5.3) and
[GLM-5.3-Flash](https://docs.z.ai/guides/vlm/glm-5.3-flash) add distinct text-only
and native multimodal choices. Context capacity, reasoning modes and account
protocol restrictions are recorded separately from task quality. The
[official USD price page](https://docs.z.ai/guides/overview/pricing) governs prices;
Arena's price/license labels are not used for model metadata. The flagship has a
dedicated weight license; Flash weights use MIT.

Vendor cards disclose coding, terminal, security and workflow settings. Flash's
[machine-readable results](https://huggingface.co/zai-org/GLM-5.3-Flash/raw/main/.eval_results/GLM-5.3-Flash.yaml)
date three measurements to August 26: the original dates are preserved and those
records expire under the 45-day vendor TTL. Other rows with unknown evaluation
dates explicitly say so. HLE results are multidisciplinary proxies, not dedicated
mathematical or scientific-workflow proof; different Terminal-Bench versions are
not put in the same comparison group.

Both GLM variants have three attributed community reports with task-scoped 0–10
editorial assessments. They include small public Python/frontend artifacts,
reported backend/debugging use, and contrary tool-recovery or writing outcomes.
Public report artifacts are not independent reproduction, and planner-assisted
coding is not credited as autonomous architecture design. Full sources,
limitations, search queries and Chinese summaries accompany each record.

## Haiku and price references · 2026-10-08

[Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5) is recorded as the
October 7 release, without borrowing earlier Haiku scores. Official terminal,
computer-use and chart results preserve unverified effort because the full
system-card PDF could not be retrieved. They have no cross-model comparison group.
[Plotly's original analytics exam](https://plotly.com/blog/claude-haiku-5-5-plotly-data-analytics-bench/)
is an independent evaluator result from one private exam and harness; its missed
statistical traps and hidden patterns remain visible.

Three original community task reports are admitted: Rundown's small routing
fixture, Kotwal's structured-extraction batch runs and an adverse book-attribution
report. Each has a task-scoped editorial assessment, exact-version attribution,
setup limitations and complete Chinese text. A public harness is an artifact,
not a rerun by PromptHarbor. Unknown publication dates remain unknown.

The catalog now includes 17 models, and every one has a dated community search
log. Search coverage is separate from the availability of evidence for each task.
[Community assessments](COMMUNITY.md) retain all supported scores and contrary results.

Official price pages were checked for display-only references, including context,
peak/off-peak and introductory tariffs. Existing budget/cost-priority inputs were
preserved. [Price rules](../skills/promptharbor/references/prices.md) explain the
separate fields and why open weights or missing prices never imply free inference.

## Gemini 4 Argon addition · 2026-10-14

The [stable API model](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
is `gemini-4-argon`. The September 30 restricted announcement and October 13
public API documentation are distinct. Input, thinking and output share a single
1,048,576-token window. Default synchronous output is 65,536 tokens; longer decode
needs background execution or client-side continuation and remaining window space.
Paid API eligibility and consumer app subscriptions are recorded separately.

Twelve formal task records include one capability declaration, seven qualified
vendor or vendor-relayed results and four original independent evaluations. The
[FrontierSWE operator](https://www.frontierswe.com/) reports mean@5, not pass@1;
its non-production Argon setup has an explicit limitation.
[Vals Finance v2](https://www.vals.ai/benchmarks/fabv2) uses dealbreaker-gated partial
credit; [Harvey LAB](https://www.vals.ai/benchmarks/hlab) reports 19.58% task pass,
which is distinct from its much higher per-criterion coverage.
[Ultralytics](https://www.ultralytics.com/blog/gemini-4-argon-auto-annotation) measures
object-box annotation on 108 selected images and has an annotation-product
interest. These results do not establish universal correctness or discovery.

Vendor results retain the September 30 first-report date. Vals rows retain their
October 12 early-access date; a later catalog check does not become a new run.
No old peer cohort, model record, evidence row, source date or weight was changed.
Artificial Analysis's aggregate index was inspected but not converted to specialty
scores; its accessible page did not expose the needed numeric task observations.

Four original [community reports](COMMUNITY.md#gemini-4-argon) retain task-scoped
editorial scores and mixed outcomes: sustained multi-tool work, deployment failures,
an inspectable visual prototype and effort-sensitive analysis. Earlier access,
provider and agent differences, human finishing, changed constraints and unsupported
sales promises remain visible. No paid cross-model run or independent reproduction
was performed. Repository/debugging tasks without suitable community reports stay
unrated in the Chinese example rather than inheriting workflow or visual scores.

[Official pricing](https://ai.google.dev/gemini-api/docs/pricing) supplies a display
reference of $2 / $10 through November 30 and announces $4 / $20 from December 1.
The offer has an expiry and is not used as a numeric budget-filter quote. Price
references still do not affect recommendation weights. The full catalog now has
18 models, with each model's actual search and check dates preserved. Older overdue
records remain in the maintenance queue; adding Argon does not refresh them.

## Kimi K3.1 Pro addition · 2026-10-27

The [official release](https://www.kimi.ai/blog/kimi-k3-1-pro) and
[API guide](https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart) identify
standard Pro as `kimi-k3.1-pro`. The hosted model is available, but its full weights
are still promised by November 4. It is excluded from local-weight-only requests
until downloadable weights and their terms are verified. Native text/image/video,
always-on thinking, low/high/max effort and context/output limits are recorded
separately from performance. Highspeed is a distinct serving option, not another
ranked candidate in this update.

Six vendor task measurements retain their October 23 first-report date and
explicit harness/effort. They cover terminal work, internal long-horizon coding,
BenchCAD geometry, OfficeQA document questions and financial workflows. Private
workbook tests do not establish real-market profitability; visual geometry is
not production CAD verification. Unreadable primary charts and secondhand copies
were not converted into additional scores.

The [October 22 Arena WebDev entry](https://arena.ai/leaderboard/code/webdev)
provides one independent, preliminary preference record. Its same mapping as
older catalog peers is preserved: direct frontend implementation, adjacent visual
design, no design-fidelity measurement. No old peer cohort was relabeled or
recomputed using the new row. The original score, vote count, effort and spread
are recorded separately from quality claims about a specific prompt.

Five original [community reports](COMMUNITY.md#kimi-k31-pro) include selected
Python repairs, small deterministic extraction/algorithm tasks, mixed visual
builds, adverse reference-heavy work and feedback-driven 3D repairs. Public
artifacts are not PromptHarbor reruns. Harness budget stops, requested-versus-
effective effort, quota recovery, shared directories, sponsored/affiliate content,
human visual feedback and different agents qualify the task scores. Directly
reading the AI for Mortals article revealed completed builds that its older search
snippet still described as pending; the current primary page governs the record.

[Official pricing](https://platform.kimi.ai/) lists standard uncached input/output
at $2/$10 per million tokens without a temporary promotion. The new model therefore
has a verified legacy budget quote as well as its display-only reference; the
reference never changes ranking or switching. Cache read/write, tools, taxes and
Kimi Code subscriptions remain distinct. No previous model, source, evidence,
search date or recommendation weight was changed. Existing overdue records remain
in the maintenance queue rather than receiving a cosmetic date renewal.

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
