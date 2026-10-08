# PromptHarbor

Generative visual web design

**Decision:** shortlist · **Confidence:** limited
**Top 3:** choose using task fit and the models you can access.

**Switch:** unknown — Current model was not provided; do not infer it from the assistant's identity.

| Rank | Model | Task fit | Price reference |
|---|---|---|---|
| 1 | **GPT-6.1 Sol** (`gpt-6.1-sol`) | Capability or adjacent-task support for Generative visual web design; weighted community reports included (see signed signal and sources) | $2 / $10 (≤272,000 input tokens); $4 / $15 (>272,000–≤1,050,000 input tokens)<br>[Price source](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · 2026-10-08 |
| 2 | **Kimi K3** (`kimi-k3`) | Capability or adjacent-task support for Generative visual web design; weighted community reports included (see signed signal and sources) | $3 / $15 (≤1,000,000 input tokens)<br>[Price source](https://platform.kimi.ai/) · 2026-10-08 |
| 3 | **DeepSeek-V4.1-Flash** (`deepseek-v4.1-flash`) | Capability or adjacent-task support for Generative visual web design; weighted community reports included (see signed signal and sources) | $0.3 / $1.2 (≤1,000,000 input tokens) · Peak reference; off-peak $0.15 / $0.60. Peak: Mon–Fri 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays.<br>[Price source](https://api-docs.deepseek.com/quick_start/pricing/) · 2026-10-08 |

Price reference: USD per million standard text API input / output tokens, uncached rates. Display only; recommendation weights are unchanged. Subscriptions, local hosting, audio, images, tools and cache charges are separate.

## 1. GPT-6.1 Sol

Capability or adjacent-task support for Generative visual web design; weighted community reports included (see signed signal and sources)

Access: user_listed; open weights: no; context: 1050000 tokens.
Price reference: $2 / $10 (≤272,000 input tokens); $4 / $15 (>272,000–≤1,050,000 input tokens)<br>[Price source](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · 2026-10-08
Community: software.frontend.design, 3.0/10 (low confidence; proxy mapping), weight 30%, origins 1.
- gpt-6.1-sol-max: WebDev preference rating 1757 (displayed interval ±15). (independent_eval; gpt-6.1-sol-max; Arena deployment with the displayed effort setting.). [Source](https://arena.ai/leaderboard/code/webdev)
  Limit: Preference evaluation does not establish functional correctness or reference fidelity. Configurations differ; intervals can overlap. Serving aliases do not identify local checkpoints. Report date: 2026-10-07; reviewed 2026-10-08.
- The author reports a medium-effort safari game iteration missed music and delivered poorly working gameplay, with another follow-up not fixing it. (community_test; Author-reported exact model version; deployment, effort and harness are unverified unless stated in claim/limitations.). [Source](https://www.reddit.com/r/OpenaiCodex/comments/1wtrad9/gpt_61_sol_has_been_pretty_disappointing_that_i/)
  Limit: No returned code or acceptance log inspected; inspiration link is input, not proof of generated output. Medium effort and one early task only. Report date: not reported; reviewed 2026-09-30.
  Editorial assessment: 3/10 — Specific missing requirements and unusable reported interaction warrant a negative frontend signal; a single early medium-effort run is not a general verdict.

Limits: Tool calling is supported through Responses API; Chat Completions does not support tools for this model. 128000 maximum output tokens. Reasoning efforts: low, medium, high, xhigh, max. Exact-version evaluations are maintained separately from predecessor results. Account access and tool environment require checking. Standard input/output rates remain $2/$10 per million tokens up to 272000 input tokens; cached input is $0.10. Longer requests, effort and service tier affect total cost.

## 2. Kimi K3

Capability or adjacent-task support for Generative visual web design; weighted community reports included (see signed signal and sources)

Access: user_listed; open weights: yes; context: 1048576 tokens.
Price reference: $3 / $15 (≤1,000,000 input tokens)<br>[Price source](https://platform.kimi.ai/) · 2026-10-08
Community: software.frontend.design, 7.0/10 (low confidence; direct_and_proxy mapping), weight 30%, origins 3.
- kimi-k3-max: observed WebDev preference rating 1660. (independent_eval; kimi-k3-max; Arena deployment, not every consumer app setting). [Source](https://arena.ai/leaderboard/code)
  Limit: Crowd preference, not a functional acceptance test. Effort differs by entry; error intervals and preliminary labels are on source. Ranking differences are not significance tests. Overall results are only a proxy for visual design, not reference fidelity. Report date: 2026-09-25; reviewed 2026-09-29.
- kimi-k3-max: WebDev preference rating 1655 (displayed interval ±6). (independent_eval; kimi-k3-max; Arena deployment with the displayed effort setting.). [Source](https://arena.ai/leaderboard/code/webdev)
  Limit: Preference evaluation does not establish functional correctness or reference fidelity. Configurations differ; intervals can overlap. Serving aliases do not identify local checkpoints. Report date: 2026-10-07; reviewed 2026-10-08.
- The author lists two Kimi3 React/Vite web outputs as successful and links the generated sites. (community_test; Author identifies Kimi K3; exact deployment and effort unverified). [Source](https://neuralhub.dev/ai-test-results)
  Limit: Self-reported artifacts, not rerun by PromptHarbor. Small creative-web sample; model settings and exact run date unknown. Older comparison models do not establish superiority over current versions. Mirrors by the same author count as one origin. Report date: not reported; reviewed 2026-09-29.
  Editorial assessment: 7.5/10 — Linked creative-web outputs support a positive bounded design result; outputs were not independently rerun.
- A user favors Kimi for frontend work and reports using it as a UI subagent. (community_test; Author identifies Kimi K3; exact deployment and effort unverified). [Source](https://www.reddit.com/r/kimi/comments/1vconet/comment/p157lwe/)
  Limit: No public prompt, code or controlled comparison. The same author reports quota constraints; subscription access and speed require current verification. Relative date only. Report date: not reported; reviewed 2026-09-29.
  Editorial assessment: 7.0/10 — A specific frontend subagent usage account is positive but lacks code or matched prompts.
- Another user reports preferring Opus 5 results for visual effects and UI. (community_test; Author identifies Kimi K3; exact deployment and effort unverified). [Source](https://www.reddit.com/r/kimi/comments/1vconet/comment/p2cjso7/)
  Limit: A relative preference against Kimi in this discussion, not proof of failure. No task artifacts or exact settings. It is not evidence for the newer Opus 5.5; relative date only. Report date: not reported; reviewed 2026-09-29.
  Editorial assessment: 4.0/10 — Preserves an adverse visual preference; no output or controlled task comparison supports a stronger negative conclusion.

Limits: Kimi K3 has its own weights license. Native video support and deployment-specific frame limits require verification.

## 3. DeepSeek-V4.1-Flash

Capability or adjacent-task support for Generative visual web design; weighted community reports included (see signed signal and sources)

Access: user_listed; open weights: yes; context: 1000000 tokens.
Price reference: $0.3 / $1.2 (≤1,000,000 input tokens) · Peak reference; off-peak $0.15 / $0.60. Peak: Mon–Fri 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays.<br>[Price source](https://api-docs.deepseek.com/quick_start/pricing/) · 2026-10-08
Community: software.frontend.design, 8.0/10 (low confidence; direct mapping), weight 30%, origins 1.
- deepseek-v4.1-flash-max: observed WebDev preference rating 1621. (independent_eval; deepseek-v4.1-flash-max; Arena deployment, not every consumer app setting). [Source](https://arena.ai/leaderboard/code)
  Limit: Crowd preference, not a functional acceptance test. Effort differs by entry; error intervals and preliminary labels are on source. Ranking differences are not significance tests. Overall results are only a proxy for visual design, not reference fidelity. Report date: 2026-09-25; reviewed 2026-09-29.
- deepseek-v4.1-flash-max: WebDev preference rating 1619 (displayed interval ±11). (independent_eval; deepseek-v4.1-flash-max; Arena deployment with the displayed effort setting.). [Source](https://arena.ai/leaderboard/code/webdev)
  Limit: Preference evaluation does not establish functional correctness or reference fidelity. Configurations differ; intervals can overlap. Serving aliases do not identify local checkpoints. Report date: 2026-10-07; reviewed 2026-10-08.
- The author reports a successful first-pass responsive website using DeepSeek Harness at maximum reasoning, with HTML, vanilla JavaScript, Tailwind, GSAP and Lucide. Mobile adaptation and visual feedback were satisfactory, while token consumption was high. (community_test; Author-reported exact model version; deployment, effort and harness are unverified unless stated in claim/limitations.). [Source](https://www.reddit.com/r/DeepSeek/comments/1wcj9ux/deepseek_41_flash_surprised_me_6_minutes_one/)
  Limit: Single author and website; original prompt and source project are not linked. A media poster is present but the video was not replayed or validated. Reported time, spend and token totals are self-reports. Page exposes only a relative timestamp, so no exact publication date is inferred. Does not establish reference fidelity or production correctness. Report date: not reported; reviewed 2026-09-30.
  Editorial assessment: 8.0/10 — A concrete frontend stack, first-pass result and mobile outcome support a strong reported result; missing prompt, source and independent execution keep confidence limited.

Limits: Open weights do not imply laptop suitability. Verify serving precision, hardware, license and API alias.

## Validation

- Render the same brief at mobile and desktop sizes; inspect visual coherence, accessibility and working interactions.

As of 2026-10-08; bundled snapshot 2026-10-08.
