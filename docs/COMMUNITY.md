# Community task ratings

Reviewed: **2026-10-27**. All **19** catalog models were searched.

Scores are PromptHarbor editorial judgments of specific reported outcomes, on a 0–10 scale. They are not benchmark measurements or global model ratings.
Unknown task ratings remain unknown. A **proxy** label means only adjacent-task reports support that rating; it is not a direct observation of that task.
Confidence reflects corroboration and evidence quality; same-origin reposts do not add votes.
See the [rating rubric and weighting rules](../skills/promptharbor/references/community.md).

| Model | Task ratings (0–10) | Distinct report origins |
|---|---|---|
| GPT-6 Astra | No admitted task reports | 2 |
| GPT-6.1 Sol | No admitted task reports | 3 |
| GPT-6 Luna | No admitted task reports | 2 |
| Claude Opus 5.5 | No admitted task reports | 3 |
| Claude Sonnet 5.5 | No admitted task reports | 3 |
| Claude Fable 5.1 | No admitted task reports | 3 |
| Gemini 3.8 Flash | No admitted task reports | 2 |
| DeepSeek-V4.1-Flash | No admitted task reports | 3 |
| Qwen3.8-27B | No admitted task reports | 3 |
| Kimi K3 | No admitted task reports | 5 |
| Grok 4.7 | No admitted task reports | 3 |
| MiMo-V2.6-Pro | No admitted task reports | 5 |
| MiMo-V2.6-Flash | No admitted task reports | 6 |
| MiMo-V2.6-Pro-UltraSpeed | No admitted task reports | 1 |
| GLM-5.3 | No admitted task reports | 3 |
| GLM-5.3-Flash | No admitted task reports | 3 |
| Claude Haiku 5.5 | No admitted task reports | 3 |
| Gemini 4 Argon | `agent.long` **7.5**; `agent.workflow` **7.5**; `context.retrieve` **7.0**; `context.synthesis` **7.0** (proxy); `data.analysis` **7.0**; `software.frontend` **5.5**; `software.frontend.design` **5.5**; `software.terminal` **3.5**; `writing.professional` **7.0** (proxy) | 4 |
| Kimi K3.1 Pro | `data.extract` **7.5**; `software.algorithm` **7.5**; `software.debug` **6.8**; `software.frontend` **6.8**; `software.frontend.design` **5.2**; `software.frontend.fidelity` **4.0**; `software.repo` **6.5** | 5 |

## GPT-6 Astra

Search: 2026-09-30 · status: reviewed

Queries: `"GPT-6 Astra" review portfolio coding`; `"GPT-6 Astra" writing firsthand Reddit`


### [Astra built the author’s portfolio](https://www.najam.pk/blog/gpt-6-astra-review)

**8/10** · positive · artifact_report · low confidence. Author: Najam Saeed.
Reported: 2026-09-01 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend`. Proxy tasks: `software.frontend.design`.

The author reports building his portfolio with Astra in Codex, with strong coding results but rapid subscription quota consumption.

**Rating reason:** A published personal website supports a strong bounded frontend result; one project and quota anecdotes do not establish broader superiority.

**Limits:** One personal project; no matched prompts or test suite. The explicit September 1 article date is retained as an early personal report; release/access timing is not independently established. Subscription quota anecdotes are not API prices.

Artifacts: [artifact 1](https://www.najam.pk/).

### [Scriptwriting comparison: Astra](https://www.reddit.com/r/LLMDevs/comments/1wtmb3m/gpt61_sol_seems_like_a_step_back_for_writing/)

**6.5/10** · mixed · firsthand · low confidence. Author: OnlyProggingForFun.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `writing.creative`. Proxy tasks: None.

The author’s internal AI-judged script study places Astra near 6.1 Sol but below the older 6 Sol.

**Rating reason:** Useful scripts with a reported preference gap to older Sol; a small private AI-judged comparison supports only a cautious mixed rating.

**Limits:** Private 10-task scriptwriting study, five generations per task and three AI judges; no public prompts or evaluation code. Efforts differ (6.1 Sol xhigh, Astra max). AI-judge preference is not human consensus. Original page only exposes relative age; absolute date is unknown.

## GPT-6.1 Sol

Search: 2026-09-30 · status: reviewed

Queries: `"gpt-6.1-sol" official model`; `"GPT-6.1 Sol" review writing`; `"GPT-6.1 Sol" planner Qwen`; `"GPT 6.1 Sol" disappointing game`


### [Scriptwriting comparison: Astra](https://www.reddit.com/r/LLMDevs/comments/1wtmb3m/gpt61_sol_seems_like_a_step_back_for_writing/)

**6.5/10** · mixed · firsthand · low confidence. Author: OnlyProggingForFun.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `writing.creative`. Proxy tasks: None.

The author’s internal AI-judged script study places 6.1 Sol close to Astra but below older 6 Sol, with higher reported generation expense than older Sol.

**Rating reason:** A new model can still be weaker for a specific writing preference; retain the mixed result without treating private Elo as public benchmark evidence.

**Limits:** Private 10-task scriptwriting study, five generations per task and three AI judges; no public prompts or evaluation code. Efforts differ (6.1 Sol xhigh, Astra max). AI-judge preference is not human consensus. Original page only exposes relative age; absolute date is unknown.

### [6.1 Sol planner with a local Qwen coder](https://www.reddit.com/r/ChatGPT/comments/1wtqp7l/using_gpt61_sol_only_as_the_planner_and_letting_a/)

**7.5/10** · positive · firsthand · low confidence. Author: GapNew4766.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `agent.workflow`. Proxy tasks: `software.architecture`.

The author reports building three small games with Sol planning and local Qwen coding, reducing API spend while taking much longer than Sol alone.

**Rating reason:** The bounded planning/coding split produced reported deliverables and cost savings; latency and acceptance uncertainty constrain the recommendation.

**Limits:** One run per game; no inspected output artifacts or functional tests. Local hardware/electricity omitted from API savings. Author develops the promoted AtomicAgent/Fusion orchestration tool, a commercial-interest confound.

### [6.1 Sol medium: safari game complaint](https://www.reddit.com/r/OpenaiCodex/comments/1wtrad9/gpt_61_sol_has_been_pretty_disappointing_that_i/)

**3/10** · negative · firsthand · low confidence. Author: Upper-Animator-5067.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend`. Proxy tasks: `software.frontend.design`.

The author reports a medium-effort safari game iteration missed music and delivered poorly working gameplay, with another follow-up not fixing it.

**Rating reason:** Specific missing requirements and unusable reported interaction warrant a negative frontend signal; a single early medium-effort run is not a general verdict.

**Limits:** No returned code or acceptance log inspected; inspiration link is input, not proof of generated output. Medium effort and one early task only.

## GPT-6 Luna

Search: 2026-09-30 · status: reviewed

Queries: `"GPT-6 Luna" AB tested repo`; `"GPT-6 Luna" OpenClaw context firsthand`


### [Sol repaired an agentic wiki](https://www.reddit.com/r/openclaw/comments/1wrgu8e/how_is_gpt6luna_so_good/)

**7.5/10** · positive · firsthand · low confidence. Author: ilias_from_ilios.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `agent.workflow`. Proxy tasks: `context.summary`.

The author reports useful Luna context continuity after Discord-session compaction in a mixed-model agent workflow.

**Rating reason:** A concrete extended-session account supports useful workflow participation; mixed-model effects and unverified retention prevent a stronger score.

**Limits:** No transcripts or controlled context-retention test. Other models/subagents contributed; claimed session token counts are not model specifications.

### [Ten engineering tasks: Luna version comparison](https://www.reddit.com/r/codex/comments/1wp7ckc/i_ab_tested_gpt56_luna_and_gpt6_luna_on_the_same/)

**5/10** · mixed · firsthand · low confidence. Author: rundef.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`. Proxy tasks: None.

On ten bounded C++/Python tasks in separate worktrees, the author reports faster 6 Luna execution but an AI judge often preferred the older Luna’s final engineering work.

**Rating reason:** Speed and narrow execution were useful, while integration quality was mixed; this is task-specific feedback, not a universal downgrade.

**Limits:** One 60k-line repository, high rather than max effort, ten tasks and GPT-5.6 Sol judging; no independent replay. Speed is workload-specific.

## Claude Opus 5.5

Search: 2026-09-30 · status: reviewed

Queries: `"Claude Opus 5.5" review coding Reddit`; `"Claude Opus 5.5" firsthand code review`; `"Sonnet 5.5" "review" -opus`


### [Opus 5.5 found two defects in the author's Stackchan/Home Assistant code](https://digitalhandwerk.rocks/ki/testbericht-zu-claude-opus-5-5-und-fehleranalyse/)

**8.0/10** · positive · firsthand · low confidence. Author: Alex Januschewsky.
Reported: 2026-09-23 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.debug`. Proxy tasks: `software.repo`.

In Claude Desktop, Opus 5.5 traced corrupted speech to two upstream Home Assistant entity-query defects in the author's existing robot project.

**Rating reason:** Concrete symptom-to-cause success supports debugging usefulness; the single private case does not support a near-perfect general rating.

**Limits:** One project/session; no matched comparison or public patch inspected. Author uses AI for editing but states editorial responsibility.

### [Three-run skill comparison: Opus 5.5 and Sonnet 5.5](https://www.reddit.com/r/ClaudeAI/comments/1wtend0/tested_sonnet_55_vs_opus_55_with_the_same_skills/)

**7.0/10** · mixed · firsthand · low confidence. Author: maverick_man1111.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.debug`, `writing.professional`. Proxy tasks: `software.repo`, `software.terminal`.

The author reran code-review, Git-workflow and documentation tasks three times; Opus 5.5 performed well with skills but unassisted outputs varied.

**Rating reason:** Repeated task results are more useful than enthusiasm; variability and rubric saturation limit stronger conclusions.

**Limits:** Small checklist tasks; Opus 5 judge; model defaults use different effort levels. Git rubric can saturate; raw-file link returned a fetch error, so it was not independently inspected.

Artifacts: [artifact 1](https://driftproofhq.com/reports/013/).

### [Opus 5.5 versus Sonnet 5.5 on a large test refactor](https://www.reddit.com/r/ClaudeCode/comments/1wtdgwy/where_does_sonnet_55_actually_fit_into_your_agent/)

**4.0/10** · negative · firsthand · low confidence. Author: Outrageous-Issue9722 (comment).
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`, `software.testing`. Proxy tasks: None.

A commenter reports a 17-slice refactor of 120k lines of tests on separate branches: Opus 5.5 high left more rule violations and took longer than Sonnet 5.5 high.

**Rating reason:** Retains a concrete adverse implementation report despite positive Opus feedback elsewhere; low confidence prevents overgeneralization.

**Limits:** Self-reported private repository and three-layer review; no patches, prompts or timings independently inspected. One refactor workload does not establish a model-wide ordering.

## Claude Sonnet 5.5

Search: 2026-09-30 · status: reviewed

Queries: `"Claude Sonnet 5.5" experience frontend reddit`; `"Sonnet 5.5" "I" "tested"`; `"Sonnet 5.5" site:reddit.com`; `"Sonnet 5.5" -opus -grok`


### [Three-run skill comparison: Opus 5.5 and Sonnet 5.5](https://www.reddit.com/r/ClaudeAI/comments/1wtend0/tested_sonnet_55_vs_opus_55_with_the_same_skills/)

**7.5/10** · positive · firsthand · low confidence. Author: maverick_man1111.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.debug`, `writing.professional`. Proxy tasks: `software.repo`, `software.terminal`.

On the author's repeated review, Git-workflow and docs/ADR tasks, Sonnet 5.5 with skills was comparable to Opus 5.5 and cheaper in estimated generation cost.

**Rating reason:** Three runs and stated caveats support a positive practical report, while grading and effort confounds cap confidence.

**Limits:** Small checklist tasks, model judge, differing default effort and potentially saturated Git rubric. Public raw-file link could not be fetched; author acknowledges equivalence on this test does not prove equal overall capability.

Artifacts: [artifact 1](https://driftproofhq.com/reports/013/).

### [Opus 5.5 versus Sonnet 5.5 on a large test refactor](https://www.reddit.com/r/ClaudeCode/comments/1wtdgwy/where_does_sonnet_55_actually_fit_into_your_agent/)

**8.0/10** · positive · firsthand · low confidence. Author: Outrageous-Issue9722 (comment).
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`, `software.testing`. Proxy tasks: None.

A commenter reports fewer violations and faster slices for Sonnet 5.5 high than Opus 5.5 high on separate branches refactoring a 120k-line test suite.

**Rating reason:** Concrete branch comparison and review criteria support the task fit; insufficient replication for a higher score.

**Limits:** Private code; reviewer methodology described but not independently verified. One workload, release-day usage and no public patches.

### [Sonnet 5.5 high left bugs and required expensive rework](https://www.reddit.com/r/ClaudeCode/comments/1wsqfzk/sonnet_55_is_not_worth_using_it_unless_at_lowmed/)

**3.5/10** · negative · firsthand · low confidence. Author: msw3age (comment).
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`. Proxy tasks: `software.debug`.

In two low/medium difficulty coding tasks, the commenter reports Sonnet 5.5 high was initially faster/cheaper but left bugs or omissions; Opus review and rework erased that advantage.

**Rating reason:** Specific residual-defect and rework complaint is an adverse signal; weak reproducibility keeps the confidence limited.

**Limits:** Only two unspecified tasks; no prompts, patches, invoice or code artifacts. Anecdote concerns total cost after review, not a verified token-rate comparison.

## Claude Fable 5.1

Search: 2026-09-30 · status: reviewed

Queries: `"Claude Fable 5.1" writing review`; `"Fable 5.1" firsthand writing tests`


### [Fable 5.1 structured a draft from handwritten notes](https://aaronmakelky.com/blog/astra-vs-fable)

**8.0/10** · positive · firsthand · low confidence. Author: Aaron Makelky.
Reported: 2026-09-15 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `writing.edit`, `writing.professional`. Proxy tasks: `vision.document`.

Given 17 scanned handwritten pages, the author preferred Fable 5.1's draft structure and opening; processing took substantially longer than the Astra setup.

**Rating reason:** Clear transformation task and explicit quality/time tradeoff support writing fit, with comparison confounds retained.

**Limits:** One personal task; different applications and tools; subjective preference, no blind grading. Author discloses receiving OpenAI promotional merchandise.

Artifacts: [artifact 1](https://aaronmakelky.com/blog/astra-vs-fable).

### [Fable 5.1 structured a draft from handwritten notes](https://aaronmakelky.com/blog/astra-vs-fable)

**5.0/10** · mixed · artifact_report · low confidence. Author: Aaron Makelky reporting tests with Ryan Doser.
Reported: 2026-09-15 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend.design`. Proxy tasks: `software.frontend`.

The shown tests retained an existing page's branding, but a new business homepage had readability/spacing faults and a weaker complete brand package than the author's preferred Astra result.

**Rating reason:** Brand retention is useful, while visible layout faults warrant a mixed task assessment.

**Limits:** Two briefs, subjective preference, no conversion measurement; different harnesses and image-generation access. Same origin as the writing test; do not count as an independent second reviewer.

Artifacts: [artifact 1](https://aaronmakelky.com/blog/astra-vs-fable).

### [Seven-chapter Fable 5.1 rewrite still needed voice editing](https://ainativeproductmanager.com/field-notes/fable-5-1-first-impressions)

**5.5/10** · mixed · artifact_report · low confidence. Author: AI-Native PM authors (Girish PM origin).
Reported: 2026-09-02 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `writing.edit`. Proxy tasks: `writing.professional`.

On a seven-chapter course rewrite, the authors found only marginal prose improvement and still edited every chapter to restore their voice.

**Rating reason:** Modest improvement and necessary line editing support a mixed score for preserving a specific author voice.

**Limits:** Before/after excerpt is public, but complete session outputs were not inspected; fleet mode confounds model attribution.

Artifacts: [artifact 1](https://ainativeproductmanager.com/field-notes/fable-5-1-first-impressions).

### [Seven-chapter Fable 5.1 rewrite still needed voice editing](https://ainativeproductmanager.com/field-notes/fable-5-1-first-impressions)

**6.0/10** · mixed · firsthand · low confidence. Author: AI-Native PM authors (Girish PM origin).
Reported: 2026-09-02 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `agent.long`, `agent.workflow`. Proxy tasks: None.

The course workflow needed less steering and recovered cached agent results, but underestimated usage and exhausted its subscription allowance before completion.

**Rating reason:** Recovery is a practical gain; usage estimation and interrupted delivery offset it for long-running work.

**Limits:** One workflow with fleet mode; resumption and allowance accounting also belong to Claude Code/product behavior. Same origin as the course rewrite; do not count twice per task.

### [Fable 5.1 animated SVG and rocket-page build-off](https://www.bitsminds.com/news/grok-4-7-vs-fable-5-1-vs-astra-6-build-off-2026)

**8.0/10** · positive · artifact_report · low confidence. Author: BitsMinds hands-on reviewers.
Reported: 2026-09-21 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend.design`. Proxy tasks: `software.frontend`.

In three visible animation briefs, Fable 5.1 had a fault-free interchange and a correctly rotating carousel, and kept the launch vehicle in frame, with remaining rocket defects.

**Rating reason:** Concrete motion correctness is useful evidence for visual prototypes; residual defects and small sample cap the score.

**Limits:** Single attempt per brief; non-blind judging and different maker harnesses. Live builds are linked, but exact prompt files were not published; no production/accessibility validation.

Artifacts: [artifact 1](https://www.bitsminds.com/news/grok-4-7-vs-fable-5-1-vs-astra-6-build-off-2026).

## Gemini 3.8 Flash

Search: 2026-09-30 · status: reviewed

Queries: `"Gemini 3.8 Flash" experience review`; `"Gemini 3.8 Flash" hands-on video app tests`


### [Plotline screenshot-to-data app worked from one prompt](https://promptslove.com/blog/gemini-3-8-flash-review/)

**8.0/10** · positive · artifact_report · low confidence. Author: Ramanpal Singh.
Reported: 2026-09-03 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `data.extract`, `vision.chart`, `vision.document`. Proxy tasks: `software.repo`.

The author built Plotline in OpenCode and reports successful mixed screenshot extraction, editable tables and working re-extraction using Gemini 3.8 Flash.

**Rating reason:** Working extraction workflow supports this task; one demo does not justify 10/10 accuracy.

**Limits:** Prompt/demo are published; no extraction error dataset or source repository independently inspected. Author-operated single build, OpenCode/high effort.

Artifacts: [artifact 1](https://promptslove.com/blog/gemini-3-8-flash-review/).

### [Plotline screenshot-to-data app worked from one prompt](https://promptslove.com/blog/gemini-3-8-flash-review/)

**4.5/10** · mixed · artifact_report · low confidence. Author: Ramanpal Singh.
Reported: 2026-09-03 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend`. Proxy tasks: `software.frontend.design`, `software.repo`.

Figures had working data views but broken upload/navigation; Parallax had loading, readability and theme defects despite some successful page design.

**Rating reason:** Working parts offset serious user-visible failures; preserves adverse evidence alongside extraction success.

**Limits:** Same author/build series as Plotline; limited samples and different comparator harness. Do not turn successful application construction into proof of financial reasoning.

Artifacts: [artifact 1](https://promptslove.com/blog/gemini-3-8-flash-review/).

### [Gemini 3.8 Flash game prototypes: simpler worlds versus broken 3D action](https://rutinelabo.com/gemini-38-flash-review/)

**5.5/10** · mixed · artifact_report · low confidence. Author: せなお / Routine Labo.
Reported: 2026-09-08 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend`. Proxy tasks: `software.repo`.

A seven-task demo comparison produced usable websites and a walkable voxel world, but platformer fall detection and complex 3D action failed.

**Rating reason:** Simple prototypes are usable but interaction failures limit confidence for complex frontends.

**Limits:** Screenshots and video linked; complete prompts require LINE subscription and were not inspected. Small heterogeneous prototypes, unspecified independent acceptance tests; affiliate disclosure.

Artifacts: [artifact 1](https://rutinelabo.com/gemini-38-flash-review/).

### [Gemini 3.8 Flash game prototypes: simpler worlds versus broken 3D action](https://rutinelabo.com/gemini-38-flash-review/)

**7.0/10** · positive · firsthand · low confidence. Author: せなお / Routine Labo.
Reported: 2026-09-08 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `vision.video`. Proxy tasks: `context.summary`.

The author describes using recorded video to choose screenshot positions that correspond to a blog article's explanation.

**Rating reason:** Concrete author workflow suggests video usefulness without establishing measured temporal accuracy.

**Limits:** No timestamp accuracy or video question dataset; benchmark assertions in the same article are excluded from this anecdote. Same reviewer as the prototype series.

## DeepSeek-V4.1-Flash

Search: 2026-09-30 · status: reviewed

Queries: `"DeepSeek V4.1 Flash" review Reddit coding`; `"DeepSeek-V4.1-Flash" "surprised" "UI bug"`


### [DeepSeek 4.1 Flash surprised me — 6 minutes, one attempt, $0.07](https://www.reddit.com/r/DeepSeek/comments/1wcj9ux/deepseek_41_flash_surprised_me_6_minutes_one/)

**8.0/10** · positive · firsthand · low confidence. Author: nehuenpereyra.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend`, `software.frontend.design`. Proxy tasks: None.

The author reports a successful first-pass responsive website using DeepSeek Harness at maximum reasoning, with HTML, vanilla JavaScript, Tailwind, GSAP and Lucide. Mobile adaptation and visual feedback were satisfactory, while token consumption was high.

**Rating reason:** A concrete frontend stack, first-pass result and mobile outcome support a strong reported result; missing prompt, source and independent execution keep confidence limited.

**Limits:** Single author and website; original prompt and source project are not linked. A media poster is present but the video was not replayed or validated. Reported time, spend and token totals are self-reports. Page exposes only a relative timestamp, so no exact publication date is inferred. Does not establish reference fidelity or production correctness.

### [DeepSeek V4.1 Flash is cheap per token—but is it actually cheap per completed task?](https://www.reddit.com/r/DeepSeek/comments/1wdd9hh/deepseek_v41_flash_is_cheap_per_tokenbut_is_it/)

**3.5/10** · negative · firsthand · low confidence. Author: Logical_Catch_3207.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`, `agent.workflow`. Proxy tasks: `software.debug`.

The author reports code that passes immediate checks but accumulates nested branches, duplicated logic and local fixes. On PDF/slide workflows the model reportedly took unnecessary tool detours, weakening total task efficiency despite fast generation.

**Rating reason:** The reported work completes but maintainability and workflow discipline repeatedly disappoint. The score describes this author's account; missing artifacts make it low-confidence evidence.

**Limits:** No prompts, repository, tool traces or timed logs are published. Harness and reasoning settings are unspecified; comparator is only called GPT-6 and is not an exact catalog model. Page timestamp is relative. The report is an adverse task observation, not a verified causal claim about model training or a controlled cost comparison.

### [DeepSeek v4.1 Flash is truly amazing](https://www.reddit.com/r/DeepSeek/comments/1wgohh2/deepseek_v41_flash_is_truly_amazing/)

**7.0/10** · positive · firsthand · low confidence. Author: danilofs.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.debug`, `software.repo`. Proxy tasks: None.

The author reports continuous use in OpenCode to repair problems left in an existing project by several coding agents.

**Rating reason:** Repeated repair use is a positive task signal, but broad praise without reviewable patches warrants a moderate editorial score and low confidence.

**Limits:** No specific defect, repository, prompt, patch or test result is provided. Earlier agents are product names, so comparisons cannot be assigned to exact model versions. The page exposes only a relative timestamp. Replies include hallucination cautions, but those are separate authors and must not be treated as this report's verified failures.

## Qwen3.8-27B

Search: 2026-09-30 · status: reviewed

Queries: `"Qwen3.8-27B" review Reddit`; `"Qwen3.8-27B" "Trial Report"`; `"Qwen3.8-27B" "Ninfer"`; `"Qwen3.8 27B" "Amazon"`


### [Qwen3.8-27B Trial Report (with Addendum)](https://note.com/a_matsukaze/n/n9796f33ac3c5?hl=en)

**8.0/10** · positive · firsthand · low confidence. Author: A. Matsukaze.
Reported: 2026-08-15 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `writing.translation`. Proxy tasks: None.

The author reports a successful English-to-Japanese translation test using Vontra's Qwen3.8-27B-oQ8 MLX quant in LM Studio 0.4.21 Build 2, default XHigh reasoning, on a MacBook Pro M5 Max. The author's grader awarded a perfect result; reasoning took several minutes.

**Rating reason:** A concrete language direction and reproducible environment support a strong reported translation result. Missing test text and LLM grading limit generalization, and slow XHigh reasoning is a practical cost.

**Limits:** Specific quantization and runtime, one author's translation test, no complete source/translation pair or grading rubric in this article. Grading uses an LLM rather than a bilingual blinded panel. The English page is machine translated. The score is an editorial assessment, not the author's raw score divided by ten. No claim is admitted from the secondhand benchmark addendum.

### [Disappointed in Ninfer + Qwen 3.8-27B:nvfp4](https://www.reddit.com/r/LocalLLM/comments/1wlze6z/disappointed_in_ninfer_qwen_3827bnvfp4/)

**3.0/10** · negative · firsthand · low confidence. Author: michmill1970.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `agent.workflow`, `agent.long`. Proxy tasks: `context.synthesis`.

After extensive Hermes agent use, the author reports repetitive long tool-call loops and forgotten instructions with Ninfer plus Qwen3.8-27B NVFP4. Re-running the same prompts with llama-server plus Unsloth UD-Q4_K_XL reportedly avoided those loops, despite similar small evaluation results.

**Rating reason:** Repeated interruptions and instruction reminders make the reported setup unreliable for extended tool work; the contrasting quantization result requires preserving the deployment condition.

**Limits:** This is an adverse report about a particular quantization/inference-engine combination, not every Qwen3.8 deployment. Quantization and engine changed together, so their effects are confounded. Prompts and traces are not linked. Exact timestamp is not exposed. Do not extend the negative score to original precision or Unsloth/llama-server settings without new evidence.

### [I gave a local Qwen3.8 27B agent my Amazon account — and it bought paper for me](https://www.reddit.com/r/LocalLLaMA/comments/1wn0mm4/i_gave_a_local_qwen38_27b_agent_my_amazon_account/)

**8.0/10** · positive · artifact_report · low confidence. Author: fuzhongkai.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `agent.computer`, `agent.workflow`. Proxy tasks: None.

A local Qwen3.8-27B agent in TensorSharp with a Playwright skill reportedly searched, compared and prepared an Amazon paper purchase in one run. The author handled login and final purchase approval; a video with tool trace and the runtime repository are linked.

**Rating reason:** A concrete completed workflow with available runtime and trace supports practical tool use, while human intervention, developer interest and a single run limit confidence.

**Limits:** One task and one run; no repeated success rate. Browser operations use Playwright code, so this does not prove native screenshot-driven GUI skill. Author develops the demonstrated runtime. The linked video was not replayed and the workflow was not reproduced. Quantization is unspecified; exact page timestamp is relative. Human login and transaction approval are part of the successful setup.

Artifacts: [artifact 1](https://github.com/zhongkaifu/TensorSharp).

## Kimi K3

Search: 2026-09-30 · status: reviewed

Queries: `"Kimi K3" coding review Reddit`; `"Kimi K3" "Context Tree" reviewer agent`; `"Kimi K3" "backend" "reddit.com" review`; `"Kimi K3" "math" "review" reddit`


### [AI Lab: authored web-generation experiments](https://neuralhub.dev/ai-test-results)

**7.5/10** · positive · artifact_report · low confidence. Author: Leandro / neuralhub.dev.
Reported: absolute date unknown · first seen: 2026-09-29 · assessed: 2026-09-30.
Direct tasks: `software.frontend.design`. Proxy tasks: `software.frontend`.

The author lists two Kimi3 React/Vite web outputs as successful and links the generated sites.

**Rating reason:** Linked creative-web outputs support a positive bounded design result; outputs were not independently rerun.

**Limits:** Self-reported artifacts, not rerun by PromptHarbor. Small creative-web sample; model settings and exact run date unknown. Older comparison models do not establish superiority over current versions. Mirrors by the same author count as one origin.

Artifacts: [artifact 1](https://neuralhub.dev/test-sites/biggy-kimi3), [artifact 2](https://neuralhub.dev/test-sites/websites-kimi3).

### [First-person Kimi UI usage and quota report](https://www.reddit.com/r/kimi/comments/1vconet/comment/p157lwe/)

**7.0/10** · positive · firsthand · low confidence. Author: Cachesmr.
Reported: absolute date unknown · first seen: 2026-09-29 · assessed: 2026-09-30.
Direct tasks: `software.frontend`. Proxy tasks: `software.frontend.design`.

A user favors Kimi for frontend work and reports using it as a UI subagent.

**Rating reason:** A specific frontend subagent usage account is positive but lacks code or matched prompts.

**Limits:** No public prompt, code or controlled comparison. The same author reports quota constraints; subscription access and speed require current verification. Relative date only.

### [First-person competing UI preference](https://www.reddit.com/r/kimi/comments/1vconet/comment/p2cjso7/)

**4.0/10** · negative · firsthand · low confidence. Author: Bright_Spend6574.
Reported: absolute date unknown · first seen: 2026-09-29 · assessed: 2026-09-30.
Direct tasks: `software.frontend`. Proxy tasks: `software.frontend.design`.

Another user reports preferring Opus 5 results for visual effects and UI.

**Rating reason:** Preserves an adverse visual preference; no output or controlled task comparison supports a stronger negative conclusion.

**Limits:** A relative preference against Kimi in this discussion, not proof of failure. No task artifacts or exact settings. It is not evidence for the newer Opus 5.5; relative date only.

### [LLM Benchmark: Has Kimi K3 Reached Claude Opus Level?](https://akitaonrails.com/en/2026/07/17/llm-benchmarks-kimi-k3/)

**8.0/10** · mixed · artifact_report · low confidence. Author: Fabio Akita.
Reported: 2026-07-17 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`. Proxy tasks: `software.testing`, `software.architecture`.

Kimi K3 via Kimi Code CLI delivered a Rails 8/RubyLLM/Hotwire/Docker chat app with correct conversation replay, bounded history and working chat validation. Review found missing system instructions, weak persistence/concurrency handling and insufficient error coverage. A public result commit and project links are available.

**Rating reason:** A functioning reviewed repository with concrete strengths and defects merits a strong but incomplete task assessment; this is editorial judgment rather than a conversion of the author's 89/100 rubric.

**Limits:** One app run; Kimi Code subscription harness at a 256K plan limit. Original OpenCode/Moonshot tool schema was incompatible and the harness was changed. Published model comparisons concern older competitors, not current catalog successors. Project was inspected by the author; we opened the result commit but did not rerun it. Does not cover migrations, background jobs or production tool actions. Evidence is dated July and must retain its age.

Artifacts: [artifact 1](https://github.com/akitaonrails/llm-coding-benchmark/commit/2bf1d7b3e3bbc7e6ff9a18a07390333c86bda615), [artifact 2](https://github.com/akitaonrails/llm-coding-benchmark).

### [Kimi K3 with Context Tree Beats GPT 5.6 Sol on a Real Engineering Task](https://www.reddit.com/r/kimi/comments/1vba5ie/kimi_k3_with_context_tree_beats_gpt_56_sol_on_a/)

**5.5/10** · mixed · artifact_report · low confidence. Author: Still_Amphibian545 / First Tree team.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.security`, `software.repo`. Proxy tasks: `software.testing`, `agent.long`.

The First Tree team reports that standalone Kimi K3 left permissive security headers and weak QA on one repository issue. Adding a reviewer and shared Context Tree produced stricter origin restrictions and tests after many more iterations. The post links the compared pull requests.

**Rating reason:** The report shows substantial task failure in the standalone setup and improvement with intensive review. A middling editorial outcome and low confidence preserve both findings without treating framework-assisted success as intrinsic superiority.

**Limits:** Self-promotion with explicit team disclosure; reviewer, shared context, iterations and spending changed together. GPT comparator is an older exact version without the added harness. Claude Opus supplied grading. Both PR summaries were opened and support the described policy differences; tests were not reproduced. The PRs date to July 22/27, 2026, while the report's exact date remains unknown. Cross-posts count as the same origin.

Artifacts: [artifact 1](https://github.com/agent-team-foundation/first-tree/pull/1932), [artifact 2](https://github.com/agent-team-foundation/first-tree/pull/2026).

## Grok 4.7

Search: 2026-09-30 · status: reviewed

Queries: `"Grok 4.7" review coding experience`; `"Grok 4.7" site:reddit.com`


### [Grok 4.7 on a large Rust repository in Cursor](https://www.reddit.com/r/cursor/comments/1wrktgc/am_i_the_only_one_who_thinks_grok_47_is_actually/)

**7.0/10** · mixed · firsthand · low confidence. Author: akeebismail.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`, `software.debug`. Proxy tasks: `software.architecture`.

With clear context, the author reports usable multi-file changes and debugging in a Rust codebase with distributed workflows and data pipelines, with occasional overcomplication/architectural drift.

**Rating reason:** Concrete existing-repository use is positive; architectural mistakes and lack of public outcomes cap the score.

**Limits:** Private repository, no prompts or tests inspected; Cursor routing/harness may affect experience.

### [Four Grok 4.7 visual builds shipped user-visible defects](https://www.bitsminds.com/reviews/grok-4-7-review)

**3.5/10** · negative · artifact_report · low confidence. Author: BitsMinds hands-on reviewers.
Reported: 2026-09-22 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend.design`, `software.frontend`. Proxy tasks: `software.testing`.

Four xhigh Grok Build briefs had sound mechanisms but visible animation/game defects; the Hill Climb build reported completion with known faults.

**Rating reason:** Repeated visible failures support an adverse visual-build score; scope stays on those briefs.

**Limits:** One attempt per brief; non-blind human scoring; tools differed in the earlier round. Independent benchmark and vendor claims on the page are excluded from this community record.

Artifacts: [artifact 1](https://www.bitsminds.com/news/grok-4-7-vs-fable-5-1-vs-astra-6-build-off-2026), [artifact 2](https://www.bitsminds.com/news/claude-opus-5-vs-gpt-5-6-sol-vs-grok-4-7-hill-climb-2026).

### [Grok 4.7 animated SVG pelican comparison](https://www.reddit.com/r/grok/comments/1wp5iwr/grok_47_was_supposed_to_crush_opus_and_gpt6_then/)

**4.5/10** · mixed · artifact_report · low confidence. Author: Obligation19.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend.design`. Proxy tasks: `software.frontend`.

The author rendered same-prompt SVG animations from Grok 4.7, Opus 5.5 and GPT-6 Sol; Grok produced movement but its pose was less convincing to that reviewer.

**Rating reason:** Correct broad elements but weaker perceived composition justify a slightly adverse task-specific signal.

**Limits:** One toy animation and subjective aesthetic preference; TokenRouter effort/settings not specified. Rendered GIF is linked on the original post; it was not executed locally.

Artifacts: [artifact 1](https://www.reddit.com/r/grok/comments/1wp5iwr/grok_47_was_supposed_to_crush_opus_and_gpt6_then/).

## MiMo-V2.6-Pro

Search: 2026-09-30 · status: reviewed

Queries: `MiMo Xiaomi models official September2026 MiMoV2 modelcard`; `site:github.com XiaomiMiMo MiMoV2ProFlash`; `MiMoV2Pro reviewcoding firsthandreddit`; `"MiMo-V2.6-Pro" "review"`; `"mimo-v2.6-flash" review`; `site:reddit.com "mimo" "2.6"`; `site:linux.do "MiMo" "2.6"`; `"mimo-v2.6-pro" "fixed" "reddit"`; `"mimo-v2.6-pro-ultraspeed" reviewreddit`; `site:mimo.mi.com "mimo-v2.6-pro-ultraspeed" "1M"`; `"mimo" "2.6 flash" "fixed" reddit`; `site:mimo.xiaomi.com "tool-call" "repetition"`


### [Short review about the mimo 2.6 pro model](https://www.reddit.com/r/opencodeCLI/comments/1wmv8nn/short_review_about_the_mimo_26_pro_model/)

**8/10** · positive · firsthand · low confidence. Author: irukadesune.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.debug`. Proxy tasks: None.

The author reports that MiMo-V2.6-Pro repaired an Instagram following-list script that could log in but could not retrieve the list.

**Rating reason:** The reported failure and repair outcome are concrete, supporting a positive debugging assessment. Missing reproduction artifacts limit confidence. This is our editorial judgment, not the author's numerical rating or a measured success rate.

**Limits:** One repair experience, with no public repository or execution logs. The previous model wrote the initial script while MiMo repaired it; these are different tasks and do not establish a matched win rate. The opened original shows only relative timestamps; the absolute report date is unverified.

### [Mimo 2.6 Pro feedback after 7 hours of testing](https://www.reddit.com/r/DeepSeek/comments/1wn3p6b/mimo_26_pro_feedback_after_7_hours_of_testing/)

**3/10** · negative · firsthand · low confidence. Author: Civil-Direction-6981.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.repo`, `software.architecture`, `software.frontend`. Proxy tasks: `agent.long`.

The author reports that MiMo-V2.6-Pro failed an agent architecture refactor involving a JEV state layer and also missed explicit requirements in a separate frontend change to a file tree and chat panel.

**Rating reason:** Reported failures in following requirements and maintaining architectural consistency provide a negative signal for longer engineering tasks. One person's tasks do not establish a general failure rate.

**Limits:** Two private tasks, without code, complete prompts or acceptance logs. The approximately seven-hour duration is author-reported and does not establish typical latency. The Astra comparison relies on previous experience. Only relative timestamps are shown; no absolute date is inferred.

### [MiMo-V2.6 (both Pro and Flash) is a benchmaxxed scam](https://www.reddit.com/r/LocalLLaMA/comments/1woa5d3/mimov26_both_pro_and_flash_is_a_benchmaxxed_scam/)

**2.5/10** · negative · firsthand · low confidence. Author: crusaderky.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.security`. Proxy tasks: `software.repo`.

The author reports bypasses involving environment variables and command aliases in Pro-generated bubblewrap/Git write restrictions and provides examples.

**Rating reason:** The report describes bypassable security boundaries on the stated task. Retain these specific failures without adopting the title's blanket condemnation; an overall leaderboard score cannot establish correctness of this implementation.

**Limits:** The original includes selected failure examples but no complete patch. Some of the nine alleged vulnerabilities were identified by another model and have not been reproduced by this project. The title's benchmaxxing accusation is not an established fact.

### [Opinions on the new mimo 2.6? — Pro-version roleplay comment](https://www.reddit.com/r/SillyTavernAI/comments/1wn5nf4/opinions_on_the_new_mimo_26/)

**8/10** · positive · firsthand · low confidence. Author: LordVulpius.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `writing.creative`. Proxy tasks: None.

The commenter explicitly used regular Pro, rather than Flash or UltraSpeed, and reports livelier character interactions and better prompt adherence than in their own V2.5-Pro experience.

**Rating reason:** The variant is explicit and the report describes character interaction and prompt adherence, supporting a trial for conversational creative writing. It does not establish factual accuracy or a general writing advantage.

**Limits:** Personal roleplay preference, without a complete conversation or common writing rubric. It does not establish professional-writing ability. Other comments express opposing preferences and concerns about overthinking.

### [For me, DS v4.1 is way better than mimo v2.6](https://www.reddit.com/r/CommandCode/comments/1wmvmut/for_me_ds_v41_is_way_better_than_mimo_v26/)

**2.5/10** · negative · firsthand · low confidence. Author: choiyoh.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.terminal`, `software.frontend`. Proxy tasks: `agent.long`.

The author gave Pro and Flash the same UI/UX maintenance request for a live website; both reportedly stalled in terminal grep loops, after which another model completed the change.

**Rating reason:** The reported tool loop prevented delivery and supplies a negative signal for this terminal-assisted frontend maintenance task. It is not a conclusion about general model intelligence.

**Limits:** No repository, tool trace or model configuration is public. Model behavior and the CommandCode integration can both affect the result. Third-party retellings of this author's test must retain the same origin and add no independent weight. Xiaomi updated the Pro/Flash API aliases on September 25, 2026 and released MOPD weights. This report does not pin a checkpoint, so the loop may concern the earlier revision. Any reduction in current-deployment relevance requires an explicit assessment; the announcement alone does not establish that this specific failure was fixed.

## MiMo-V2.6-Flash

Search: 2026-09-30 · status: reviewed

Queries: `MiMo Xiaomi models official September2026 MiMoV2 modelcard`; `site:github.com XiaomiMiMo MiMoV2ProFlash`; `MiMoV2Pro reviewcoding firsthandreddit`; `"MiMo-V2.6-Pro" "review"`; `"mimo-v2.6-flash" review`; `site:reddit.com "mimo" "2.6"`; `site:linux.do "MiMo" "2.6"`; `"mimo-v2.6-pro" "fixed" "reddit"`; `"mimo-v2.6-pro-ultraspeed" reviewreddit`; `site:mimo.mi.com "mimo-v2.6-pro-ultraspeed" "1M"`; `"mimo" "2.6 flash" "fixed" reddit`; `site:mimo.xiaomi.com "tool-call" "repetition"`


### [For me, DS v4.1 is way better than mimo v2.6](https://www.reddit.com/r/CommandCode/comments/1wmvmut/for_me_ds_v41_is_way_better_than_mimo_v26/)

**2.5/10** · negative · firsthand · low confidence. Author: choiyoh.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.terminal`, `software.frontend`. Proxy tasks: `agent.long`.

The same author explicitly reports that Flash, as well as Pro, stalled in grep loops during the website UI/UX maintenance task.

**Rating reason:** The task is identifiable but not reproducible from the available materials. The assessment is negative for reliability in the reported harness.

**Limits:** No repository or complete trace is public. This shares the same test origin; third-party summaries are not independent replications. Xiaomi updated the Pro/Flash API aliases on September 25, 2026 and released MOPD weights. This report does not pin a checkpoint, so the loop may concern the earlier revision. Any reduction in current-deployment relevance requires an explicit assessment; the announcement alone does not establish that this specific failure was fixed.

### [MiMo-V2.6 (both Pro and Flash) is a benchmaxxed scam](https://www.reddit.com/r/LocalLLaMA/comments/1woa5d3/mimov26_both_pro_and_flash_is_a_benchmaxxed_scam/)

**2.5/10** · negative · firsthand · low confidence. Author: crusaderky.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.terminal`. Proxy tasks: `software.debug`, `agent.long`.

The author requested a new branch and a cherry-pick in an unexpectedly corrupted worktree, reporting that Flash failed to recover the task and performed many unproductive terminal operations.

**Rating reason:** Failure to recover an unusual repository state is a relevant terminal-agent task signal. The assessment retains the reported failure without assuming unverified damage.

**Limits:** The unusual repository state was part of the actual task. No complete run trace is public, and the author's fear of possible damage is not evidence that damage occurred. Other users in the same thread report positive experiences. Xiaomi updated the Pro/Flash API aliases on September 25, 2026 and released MOPD weights. This report does not pin a checkpoint, so the loop may concern the earlier revision. Any reduction in current-deployment relevance requires an explicit assessment; the announcement alone does not establish that this specific failure was fixed.

### [Mimo 2.6 Flash is a beast and seems to use very low token count](https://www.reddit.com/r/opencode/comments/1wn191t/mimo_26_flash_is_a_beast_and_seems_to_use_very/)

**7/10** · positive · firsthand · low confidence. Author: Leather-Cod2129.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: None (adjacent task only). Proxy tasks: `software.repo`, `software.terminal`.

An OpenCode user reports an encouraging first impression of Flash as fast, inexpensive and requiring less thinking.

**Rating reason:** Retain the favorable firsthand experience, but the unspecified task makes it only a weak proxy for coding-tool workflows.

**Limits:** No concrete task, token counts or latency measurements are provided. This is a low-confidence usage impression, not a speed test.

### [Which do you choose: DeepSeek v4.1 Flash or MiMo V2.6 Flash — improvement comment](https://www.reddit.com/r/opencode/comments/1wp2ctx/which_do_you_choose_deepseek_v41_flash_or_mimo/)

**7.5/10** · mixed · firsthand · low confidence. Author: oulu2006.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.terminal`. Proxy tasks: `software.repo`.

A user of both models prefers MiMo-V2.6-Flash's outputs and reports that early loops improved through a combination of upstream changes and loop detection in their own router.

**Rating reason:** Retain the later positive experience and practical improvement alongside the harness contribution and revision uncertainty, rather than collecting only early failures.

**Limits:** No specific deliverable or reproducible trace is provided. Improvement combines model updates and user-built routing safeguards, so it cannot be attributed to the model alone. The report date and checkpoint are not pinned.

### [Pretty poor results with MiMo v2.6 Flash + Hermes — opposite experience comment](https://www.reddit.com/r/hermesagent/comments/1wnkeak/pretty_poor_results_with_mimo_v26_flash_hermes/)

**8/10** · positive · firsthand · low confidence. Author: XKiiroiSenkoX.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.debug`. Proxy tasks: `software.repo`.

A commenter reports that Flash fixed problems another model had not resolved. A main agent divided the work into clearly scoped subtasks; the commenter still reports overthinking.

**Rating reason:** The reported outcome supports debugging with clearly scoped assignments, subject to the stated thinking-time concern and assistance from the main agent's decomposition.

**Limits:** The defects are not public. Success on bounded subtasks does not establish independent architectural design ability, and the benefit of the main agent's decomposition cannot be attributed entirely to Flash.

### [Bug: New MiMo 2.6 Flash is unusable due to it ending up in infinite loops](https://github.com/anomalyco/opencode/issues/50678)

**2.5/10** · negative · firsthand · low confidence. Author: omani.
Reported: 2026-09-22 · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.terminal`. Proxy tasks: `agent.long`.

A user reports repeated Glob/Find/Read operations after several iterations with MiMo-V2.6-Flash in OpenCode 1.18.32 on Alpine Linux 3.23 and lists reproduction steps.

**Rating reason:** The specified environment and steps support a negative assessment of the historical tool loop. Xiaomi subsequently announced an MOPD mitigation for this failure class, reducing this report's relevance to ranking the updated deployment.

**Limits:** The opened original issue identifies the date, environment and steps, but supplies no complete trace or concrete repository. Its open status in the retrieved snapshot does not establish that the subsequent fix has been independently verified.

**Current-revision relevance:** 0.25 ×. The original issue was opened on September 22, before the official September 25 API update, and concerns the tool-repetition failure class addressed by MOPD. This discounts relevance of the historical revision; it does not claim that this project reproduced the fix. [Update source](https://mimo.xiaomi.com/blog/mimo-v2-6-tool-call-repetition).

## MiMo-V2.6-Pro-UltraSpeed

Search: 2026-09-30 · status: reviewed

Queries: `MiMo Xiaomi models official September2026 MiMoV2 modelcard`; `site:github.com XiaomiMiMo MiMoV2ProFlash`; `MiMoV2Pro reviewcoding firsthandreddit`; `"MiMo-V2.6-Pro" "review"`; `"mimo-v2.6-flash" review`; `site:reddit.com "mimo" "2.6"`; `site:linux.do "MiMo" "2.6"`; `"mimo-v2.6-pro" "fixed" "reddit"`; `"mimo-v2.6-pro-ultraspeed" reviewreddit`; `site:mimo.mi.com "mimo-v2.6-pro-ultraspeed" "1M"`; `"mimo" "2.6 flash" "fixed" reddit`; `site:mimo.xiaomi.com "tool-call" "repetition"`


### [MiMo 2.6 Pro UltraSpeed image-to-HTML comparison](https://news.ycombinator.com/item?id=49794584)

**4.5/10** · mixed · artifact_report · low confidence. Author: jjcm.
Reported: absolute date unknown · first seen: 2026-09-30 · assessed: 2026-09-30.
Direct tasks: `software.frontend`, `software.frontend.fidelity`. Proxy tasks: None.

The author links a reference design and three generated webpages, reporting weaker reference fidelity from UltraSpeed, a long total build time attributed to overthinking, and distorted dynamic background effects.

**Rating reason:** Inspectable outputs and an explicit model variant support a task-specific assessment. The page is accessible, while the author identifies reference-fidelity and dynamic-effect defects. This score is an editorial signal, not a visual-quality score from our own rerun.

**Limits:** The MiMo output page was opened and confirmed accessible, but this project performed no browser visual acceptance test. Complete prompts, equal budgets and blind ratings are unavailable. The author says mobile support was not requested; other commenters dispute the mobile ranking. The Astra variant is unspecified and cannot be mapped to GPT-6.1-Sol.

Artifacts: [artifact 1](https://html.non.io/annui-mimo/), [artifact 2](https://html.non.io/Annui-grok/), [artifact 3](https://html.non.io/annui/), [artifact 4](https://non.io/video/annui-comparison.mp4).

## GLM-5.3

Search: 2026-10-08 · status: reviewed

Queries: `"GLM 5.3" "I tested" coding`; `"GLM 5.3" daily driver debugging frontend`; `"GLM 5.3" long roleplay voice drift`; `"GLM 5.3" coding failed review`


### [GLM-5.3: nine executed Python functions, retained run aggregates](https://www.datallmlab.com/blog/glm-5-3-review.html)

**7.5/10** · positive · artifact_report · low confidence. Author: Kevin Fan.
Reported: 2026-08-22 · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `software.algorithm`. Proxy tasks: `software.debug`.

The author reports nine of nine self-contained Python functions passing hidden assertions and publishes a dated aggregate record.

**Rating reason:** Executed tests and retained aggregates support a positive bounded algorithm result; nine familiar functions cannot establish frontier engineering superiority.

**Limits:** Standard tasks may occur in training data. Aggregates retain no per-task responses or variance. Short Python prompts do not test repositories, agents or long context. The publisher operates an LLM gateway; PromptHarbor did not rerun it.

Artifacts: [artifact 1](https://www.datallmlab.com/blog/data/benchmark-evidence-2026-10-03.json).

### [GLM-5.3 daily use: coding, debugging and frontend](https://www.reddit.com/r/ZaiGLM/comments/1vs3bba/glm_53_is_my_daily_driver_and_has_a_little/)

**8/10** · positive · firsthand · low confidence. Author: Sensitive_Song4219.
Reported: absolute date unknown · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `software.debug`, `software.frontend`. Proxy tasks: `software.repo`.

The user describes GLM-5.3 as a daily coding, debugging and frontend model, while keeping Sol-High for review and general administration.

**Rating reason:** Specific recurring development use supports a positive coding report, with low confidence because outputs and settings are not public.

**Limits:** Personal ongoing usage with no shared code or matched test suite. World knowledge is described as weaker. Only relative dates were visible; no version-specific claim is inferred for the review model.

### [GLM-5.3 long roleplay: reported voice drift](https://www.reddit.com/r/SillyTavernAI/comments/1w8u98c/why_people_prefer_glm_52_than_glm_53/)

**3.5/10** · negative · firsthand · low confidence. Author: Ant-Hime.
Reported: absolute date unknown · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `writing.creative`. Proxy tasks: None.

A user reports that GLM-5.3 character voice softens and drifts during extended roleplay, despite finding it smarter than 5.2.

**Rating reason:** Repeated voice drift is adverse for sustained character writing, but absent transcripts limit the strength of the negative judgment.

**Limits:** No public conversation, target-length threshold or controlled style rubric. Presets and content filters affect this use case; the report does not establish performance on ordinary short fiction. Relative date only.

## GLM-5.3-Flash

Search: 2026-10-08 · status: reviewed

Queries: `"GLM 5.3 Flash" review Reddit`; `"GLM 5.3 Flash" backend debugging refactoring`; `"glm-5.3-flash" tool-call loop issue`; `"GLM 5.3 Flash" OCR`; `"GLM 5.3 Flash" frontend benchmark`; `"GLM 5.3 Flash" roleplay`


### [GLM-5.3-Flash implements planned backend and debugging work](https://www.reddit.com/r/opencode/comments/1wroplu/xiaomi_mimo_26_flash_vs_glm_53_flash/)

**8/10** · positive · firsthand · low confidence. Author: Winter-Bit2411.
Reported: absolute date unknown · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `software.repo`, `software.debug`. Proxy tasks: `agent.long`.

The user reports successful backend development, debugging, refactoring and feature implementation with GLM-5.3-Flash following plans made with Opus.

**Rating reason:** Specific successful plan-following development is useful for implementation handoffs, but unshared outputs prevent a strong superiority claim.

**Limits:** No public repository, acceptance results or matched prompts. The upstream planner contributes to the result; this does not demonstrate GLM independently creating the architecture. Relative date only.

### [GLM-5.3-Flash Devin Desktop tool-schema error loop](https://www.reddit.com/r/CognitionLabs/comments/1whs4oj/bug_report_glm53_flash_model_gets_stuck_in_a/)

**3/10** · negative · firsthand · low confidence. Author: Sensitive-Bottle4165.
Reported: 2026-09-16 · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `agent.long`, `software.terminal`. Proxy tasks: `software.repo`.

The author reports repeated invalid grep parameters and fabricated paths during Java code review; more than fifteen tool failures required manual interruption before a correct context-only answer.

**Rating reason:** Specific failure sequences and an intervention support a negative tool-recovery report; they do not show that the model cannot understand Java code.

**Limits:** No complete session trace or repository is available. Model, tool-schema integration and context handling are not isolated. The successful answer after intervention limits the claim to recovery/tool-use behavior.

### [GLM-5.3-Flash frontend renders: strong simple pages, weak dense-dashboard accessibility](https://samihedhli.com/articles/glm-5-3-flash-frontend-benchmark/)

**6.5/10** · mixed · artifact_report · low confidence. Author: Sami Hedhli.
Reported: 2026-08-29 · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `software.frontend`. Proxy tasks: `software.frontend.design`.

The author publishes strong simple-page outputs but a dense dashboard with severe accessibility defects. The live profile shows nine runs, including dashboard 10/100 and landing-page 100/100 accessibility.

**Rating reason:** Public task outputs expose meaningful complexity-dependent strengths and defects; a mixed score avoids treating fast rendering as reliable complex UI implementation.

**Limits:** Accessibility is not visual quality or complete interaction correctness. Different harnesses and reruns affect results; small public sample. PromptHarbor opened the profile but did not visually accept or rerun outputs.

Artifacts: [artifact 1](https://openvibeeval.com/models/glm-5-3-flash/).

## Claude Haiku 5.5

Search: 2026-10-08 · status: reviewed

Queries: `"Haiku 5.5" experience coding benchmark`; `"Haiku 5.5" reddit coding`; `"Haiku 5.5" "I tested" -site:haiku55.com -site:datacamp.com`; `"Haiku 5.5" "frontend" "tested"`; `"Haiku 5.5" "classification" "I" site:reddit.com`; `"Haiku 5.5" "tested" "code" "Oct 7"`; `"Haiku 5.5" "I" "built" frontend`


### [Rundown's Haiku 5.5 message-routing fixture](https://app.therundown.ai/guides/claude-haiku-workflows)

**7/10** · mixed · artifact_report · low confidence. Author: The Rundown.
Reported: 2026-10-07 · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `data.extract`. Proxy tasks: `agent.workflow`.

Rundown's helper matched 8/8 initial routing records and 11/12 challenge records, preserving IDs and quotes.

**Rating reason:** Clear fixture and execution records support bounded extraction; tiny sample and one miss cap confidence.

**Limits:** Small fixture, no speed/billing comparison; missed one resolved-ticket label. We did not reproduce the run.

Artifacts: [artifact 1](https://app.therundown.ai/guides/claude-haiku-workflows).

### [Haiku 5.5 structured-extraction batch runs](https://github.com/kotwal-itpro/steadybatch)

**6.5/10** · mixed · artifact_report · low confidence. Author: Ankur Kotwal.
Reported: 2026-10-07 · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `data.extract`. Proxy tasks: None.

On 1,000 synthetic support chats, the author reports 999 returned and 89.1% sentiment accuracy by default; disabling thinking returned 1,000 with 91.0%.

**Rating reason:** Public harness and concrete outcomes support verification, but default truncation and setting sensitivity limit task reliability.

**Limits:** Fixed output cap caused incomplete replies; differing thinking settings change error direction. Public harness available, raw result files not fetched, no rerun here.

Artifacts: [artifact 1](https://github.com/kotwal-itpro/steadybatch), [artifact 2](https://github.com/kotwal-itpro/steadybatch/blob/main/results/latest/summary.md).

### [Haiku 5.5 book-line attribution and context reports](https://www.reddit.com/r/ClaudeAI/comments/1x0829f/haiku_55_token_usage/)

**3/10** · negative · firsthand · low confidence. Author: Strange-Pin-2998 (comment).
Reported: absolute date unknown · first seen: 2026-10-08 · assessed: 2026-10-08.
Direct tasks: `data.extract`, `context.retrieve`. Proxy tasks: None.

A commenter reports finding book lines correctly but assigning their attributions incorrectly with Haiku 5.5.

**Rating reason:** Specific attribution failure is relevant, but missing artifacts and setup keep confidence low.

**Limits:** Single early anecdote, no source text or outputs; no measured error rate.

## Gemini 4 Argon

Search: 2026-10-14 · status: reviewed

Queries: `"Gemini 4 Argon" firsthand tested review coding`; `"Gemini 4 Argon" "Tiny World" same prompt`; `"Gemini 4 Argon" production backend planning review`; `"Gemini 4 Argon" "DevOps" manifests backup`

- `agent.long`: **7.5/10**, low confidence, direct mapping, 1 origin(s).
- `agent.workflow`: **7.5/10**, low confidence, direct mapping, 1 origin(s).
- `context.retrieve`: **7.0/10**, low confidence, direct mapping, 1 origin(s).
- `context.synthesis`: **7.0/10**, low confidence, proxy mapping, 1 origin(s).
- `data.analysis`: **7.0/10**, low confidence, direct mapping, 1 origin(s).
- `software.frontend`: **5.5/10**, low confidence, direct mapping, 1 origin(s).
- `software.frontend.design`: **5.5/10**, low confidence, direct mapping, 1 origin(s).
- `software.terminal`: **3.5/10**, low confidence, direct mapping, 1 origin(s).
- `writing.professional`: **7.0/10**, low confidence, proxy mapping, 1 origin(s).

### [Gemini 4 Argon, Tested: A Week as My Daily Driver](https://theoreticallymedia.com/blog/gemini-4-argon-tested-800-million-tokens/)

**7.5/10** · positive · artifact_report · low confidence. Author: Tim Simmons.
Reported: 2026-10-13 · first seen: 2026-10-14 · assessed: 2026-10-14.
Direct tasks: `agent.long`, `agent.workflow`. Proxy tasks: None.

Simmons reports an unattended overnight Skyrim mod workflow and an MCP-assisted interview edit, with human finishing work.

**Rating reason:** Concrete sustained workflows support persistence; selected early-access demonstrations and human finishing limit confidence.

**Limits:** Early-access integration, selected demonstrations, no controlled comparison; producer review remained necessary. We did not rerun the workflows.

Artifacts: [artifact 1](https://www.youtube.com/watch?v=DD4oHSH5SEI).

### [Gemini 4 Argon: Pricing, Benchmarks, API and Real Tests](https://computingforgeeks.com/gemini-4-argon-released-features-benchmarks/)

**3.5/10** · mixed · artifact_report · medium confidence. Author: Josphat Mutai / ComputingForGeeks.
Reported: 2026-10-13 · first seen: 2026-10-14 · assessed: 2026-10-14.
Direct tasks: `software.terminal`. Proxy tasks: None.

All 12 first-pass nginx manifests passed linting but failed deployment; three feedback repairs ran, with two changing specified image/port constraints.

**Rating reason:** Repeated runtime failures outweigh lint success; repairs helped but often changed requirements. Evidence is narrow and environment-specific.

**Limits:** One deployment prompt; backup scripts and OpenTofu validation succeeded. Published manifest and errors, no rerun here; does not establish failure on all DevOps tasks.

Artifacts: [artifact 1](https://computingforgeeks.com/gemini-4-argon-released-features-benchmarks/).

### [Gemini 4 Argon vs Claude Opus 5.5: same prompt, same notes, one planet](https://ohmyunicorn.com/labs/dream-loop/planet-argon/)

**5.5/10** · mixed · artifact_report · low confidence. Author: Timisageek / OhMyUnicorn.
Reported: 2026-10-13 · first seen: 2026-10-14 · assessed: 2026-10-14.
Direct tasks: `software.frontend`, `software.frontend.design`. Proxy tasks: None.

An unedited Three.js planet artifact was produced in one run; its author found creativity limited and the agent's browser inspection failed.

**Rating reason:** An inspectable single-run artifact supports bounded implementation; author criticism, failed inspection and uncontrolled visual comparison limit the rating.

**Limits:** One run per Argon/Opus, different agents and dates, subjective visual judgment. Public HTML opened; rendered interaction/accessibility not tested here.

Artifacts: [artifact 1](https://ohmyunicorn.com/labs/dream-loop/planet-argon/argon.html), [artifact 2](https://ohmyunicorn.com/labs/dream-loop/planet-argon/opus.html), [artifact 3](https://www.reddit.com/r/ClaudeCode/comments/1x56wuh/gemini_4_argon_vs_claude_opus_55_same_prompt_tiny/).

### [Gemini 4 Argon tested: what it costs and how good it is](https://aiwiz.uk/blog/gemini-4-argon/)

**7/10** · mixed · artifact_report · low confidence. Author: AIWIZ.
Reported: 2026-10-13 · first seen: 2026-10-14 · assessed: 2026-10-14.
Direct tasks: `data.analysis`, `context.retrieve`. Proxy tasks: `context.synthesis`, `writing.professional`.

On 16 jobs run twice, AIWIZ reports high 32/32 versus medium 28/32 checks; medium mis-summed a 99K-token archive, while high still invented 2/10 copywriting promises.

**Rating reason:** Useful high-effort analysis is offset by default-setting errors and unsupported sales claims; internal checks are not universal accuracy.

**Limits:** Small author-designed checks missed copy truthfulness; strong results require high and do not establish 1M-token performance. No public harness or rerun here.

Artifacts: [artifact 1](https://aiwiz.uk/blog/gemini-4-argon/).

## Kimi K3.1 Pro

Search: 2026-10-27 · status: reviewed

Queries: `Kimi K3.1 official model pricing benchmark October 2026`; `"Kimi K3.1" tested review frontend coding`; `"Kimi K3.1 Pro" "I tested" coding original`; `"Kimi K3.1 Pro" "3D" "failed" reviewer`

- `data.extract`: **7.5/10**, low confidence, direct mapping, 1 origin(s).
- `software.algorithm`: **7.5/10**, low confidence, direct mapping, 1 origin(s).
- `software.debug`: **6.8/10**, low confidence, direct mapping, 2 origin(s).
- `software.frontend`: **6.8/10**, low confidence, direct mapping, 2 origin(s).
- `software.frontend.design`: **5.2/10**, low confidence, direct mapping, 2 origin(s).
- `software.frontend.fidelity`: **4.0/10**, low confidence, direct mapping, 1 origin(s).
- `software.repo`: **6.5/10**, low confidence, direct mapping, 1 origin(s).

### [Kimi K3.1 Pro in Our Five-Model Test: Useful Patches, Incomplete Handoffs](https://kingy.ai/blog/kimi-k3-1-pro-five-model-coding-research-test/)

**6.5/10** · mixed · artifact_report · medium confidence. Author: Curtis Pyke / Kingy AI.
Reported: 2026-10-23 · first seen: 2026-10-27 · assessed: 2026-10-27.
Direct tasks: `software.repo`, `software.debug`. Proxy tasks: None.

Kingy reports four of eight saved patches passed every required test; none completed the formal handoff before the runner input-reservation stop.

**Rating reason:** Verified saved repairs support supervised debugging; small reused issues and harness-limited delivery prevent a stronger reliability claim.

**Limits:** Only four public issues; accounting stopped the passing runs, so incomplete handoff is not a pure model failure. Public audit summaries inspected, full patches/traces private; no rerun here.

Artifacts: [artifact 1](https://kingy.ai/wp-content/uploads/2026/10/kingy-kimi-k31-five-model-audit-20261023.zip).

### [Kimi K3.1 Pro review: benchmarks, pricing and original test evidence](https://www.tokrace.com/en/guides/kimi-k3-1-pro)

**7.5/10** · positive · artifact_report · medium confidence. Author: TOKRACE.
Reported: 2026-10-24 · first seen: 2026-10-27 · assessed: 2026-10-27.
Direct tasks: `data.extract`, `software.algorithm`. Proxy tasks: None.

TOKRACE publishes 45 text and nine short JavaScript results passing fixed checks across requested default/low/max groups after quota recovery.

**Rating reason:** Original prompts, responses and deterministic checks support bounded extraction/algorithm work; tiny tasks, retries and uncertain effective effort limit transfer.

**Limits:** Default effective effort is unverified and some diagnostics accepted invalid effort. Recovery reuses successes and changes budgets; HTTP 429 and unsent tasks are not scored as incorrect. No large repository or 1M-context test; no rerun here.

Artifacts: [artifact 1](https://www.tokrace.com/evaluations/kimi-k3-1-pro-resume-20261024.json).

### [Kimi K3.1 Pro : je l’ai testé contre Opus 5.5 et GPT-6.1 Sol, mon verdict](https://www.codelynx.dev/posts/kimi-k3-1-pro-test-verdict)

**6.5/10** · mixed · artifact_report · low confidence. Author: Melvynx / Codelynx.
Reported: 2026-10-25 · first seen: 2026-10-27 · assessed: 2026-10-27.
Direct tasks: `software.frontend`, `software.frontend.design`. Proxy tasks: None.

The author reports a strong interactive lava lamp, but max-effort car physics failed while high improved; visual style remained less distinctive than Opus in his tests.

**Rating reason:** Interactive 3D features support visual implementation, but physics errors and high/max reversals make the result mixed rather than a design-leadership claim.

**Limits:** Shared nonisolated directory; author says a transcript audit found no peer-script reads. Subjective selected demos, differing agents, affiliate link; no controlled superiority or rerun here.

Artifacts: [artifact 1](https://www.codelynx.dev/posts/kimi-k3-1-pro-test-verdict), [artifact 2](https://www.youtube-nocookie.com/embed/EzVoDlg6Awo).

### [Kimi K3.1 Pro: No-Hype Full Review & Testing](https://www.aiformortals.co/blog/kimi-k3-1-pro-review)

**4.0/10** · negative · artifact_report · low confidence. Author: Pat Simmons / AI for Mortals.
Reported: 2026-10-26 · first seen: 2026-10-27 · assessed: 2026-10-27.
Direct tasks: `software.frontend.design`, `software.frontend.fidelity`. Proxy tasks: None.

Simmons publishes three heavy builds and ranks Kimi last in his billiards, website-clone and launch-video comparisons.

**Rating reason:** Concrete public outputs provide counterevidence for demanding visual/reference work; subjective ranking and differing environments keep confidence low.

**Limits:** Author-ranked outcomes rather than fixed acceptance scores; tool environments differ and the article is sponsored. Public billiards HTML read, interaction not tested here. API-equivalent costs are not subscription invoices; no rerun.

Artifacts: [artifact 1](https://www.aiformortals.co/builds/club-no9-billiards-kimi-k3-1-pro), [artifact 2](https://www.aiformortals.co/builds/morpho-clone-kimi-k3-1-pro), [artifact 3](https://www.aiformortals.co/builds/kimi-launch-video-clone-kimi-k3-1-pro).

### [Kimi K3.1 Pro Test: A 3D Ark in OpenCode](https://www.michaelleung.info/latest-news/kimi-k3-1-pro-opencode-3d-ark-test)

**7.0/10** · mixed · artifact_report · low confidence. Author: Michael Leung.
Reported: 2026-10-26 · first seen: 2026-10-27 · assessed: 2026-10-27.
Direct tasks: `software.frontend`, `software.debug`. Proxy tasks: None.

Leung reports an interactive Three.js ark with working controls; screenshot feedback repaired hull gaps and an overly tight mobile camera.

**Rating reason:** Published scene and specific successful repairs support bounded frontend/debugging; human corrections and unmeasured swarm effects limit broader claims.

**Limits:** One iterative demo, no agent-count, speed, cost or single-agent control; human visual review was necessary. Article AI-assisted. Public HTML opened, rendered interaction not independently tested or rerun here.

Artifacts: [artifact 1](https://www.michaelleung.info/noah/).
