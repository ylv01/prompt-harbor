<p align="center">
  <img src="assets/brand/hero.svg" width="900" alt="PromptHarbor — Understand the work. Choose the model. Bring the pieces together.">
</p>
<p align="center">
  <a href="LICENSE"><img src="assets/badges/license.svg" alt="license Apache 2.0"></a>
  <a href="CHANGELOG.md"><img src="assets/badges/version.svg" alt="version 0.2.0"></a>
  <a href="skills/promptharbor/SKILL.md"><img src="assets/badges/skill.svg" alt="Agent Skill"></a>
  <a href="docs/COVERAGE.md"><img src="assets/badges/data.svg" alt="model data 2026-09-29"></a>
</p>
<p align="center"><b>Give it a question. Choose from its Top 3 models.<br>Give it a project. Get coordinated model handoffs.</b></p>
<p align="center">English · <a href="README.zh-CN.md">简体中文</a></p>

PromptHarbor is an Agent Skill that identifies the **domain, subdomain and task**
behind an ordinary prompt, then recommends suitable language models using
task-specific evaluations and weighted community reports. It offers **Top 3 choices**
so you can use the subscriptions, APIs and tools you already have. For a larger
project, it splits the work, offers Top 3 per part, and writes copyable prompts
with shared interfaces. The
original conversation brings the returned work together.

The host performs semantic classification and live research; local helpers
produce inspectable choices and validate handoffs without API keys.

## See the difference

> “Design an interactive landing page. I have GPT-6 Sol, Kimi K3 and DeepSeek V4.1 Flash.”

| Top 3 | Task-fit reason | Resource consideration |
|---|---|---|
| GPT-6 Sol | Stronger same-cohort WebDev support in this snapshot | Account tools and quota |
| Kimi K3 | WebDev evidence plus artifact-backed visual-web reports | Style fit, quota and conflicting feedback |
| DeepSeek V4.1 Flash | Another available candidate with task evaluation evidence | Deployment, cost and interaction checks |

This visual-design example is restricted to the stated resources. See its
[complete output with sources and dates](examples/frontend-output.md).
Without a resource list, the skill offers a broader Top 3; with one, it filters.

**A question**

> “Check this Python trading backtest for look-ahead bias.”

→ Quantitative finance + repository analysis. Shortlist models with relevant
coding evidence, identify finance-specific evidence gaps, and decide whether a
switch is justified. Validate time splits, costs and leakage; a coding score
does not prove trading profitability.

**A project**

> “Build a library management system with book ratings and reviews.”

| Part | How choices work | Handoff boundary |
|---|---|---|
| Frontend | Top 3 from task evaluations and community reports | UI states, typed API client, exact routes |
| Database | Keep declared current GPT-6 Sol as a baseline | Schema, constraints, seed and SQL checks |
| Backend | Top 3; user selects one for the shared contract | API contract, transactions, error responses |
| Tests | Keep current model unless evidence supports moving | End-to-end scenarios and observed results |
| Integration | Original conversation | Review, assemble, fix mismatches, run checks |

Each part uses the same interfaces whichever candidate you choose. See the [source-backed example](examples/library-system/project.json) and
[complete generated prompts](examples/library-system/handoffs/PLAN.md).

```mermaid
flowchart LR
    P[Ordinary prompt] --> T[Understand task and constraints]
    T --> S[Single question: evidence and model advice]
    T --> C[Project: freeze shared contracts]
    C --> F[Frontend prompt]
    C --> D[Database prompt]
    D --> B[Backend prompt]
    F --> Q[Integration tests]
    B --> Q
    Q --> I[Main conversation integrates returned work]
```

## What it does

- **Recognizes intent:** the host classifies ordinary prompts, mixed tasks and
  long projects; users do not need to choose a benchmark first.
- **Offers three choices:** exact versions, concise reasons, sources and resource
  tradeoffs; optionally restrict to models you can already access.
- **Uses community experience:** task-specific weights, artifact quality,
  author deduplication, conflicting reports and freshness decay.
- **Handles handoffs:** complete prompts printed in the current conversation,
  contracts, file ownership, dependency order and return receipts.
- **Keeps switching practical:** stay, test first, consider switching, or unknown.
  Reusing one model across components is often reasonable.
- **Works across providers:** cloud and open-weight candidates are considered.
  Hardware only matters when local deployment is explicitly required.

## Install

Download or clone this repository, open a terminal in its root, then:

```sh
# Codex (respects CODEX_HOME if set)
python scripts/install.py --host codex

# Claude Code directory convention
python scripts/install.py --host claude

# Any compatible host's skill directory
python scripts/install.py --dest /path/to/your/skills
```

Use Python 3.10+ (`python3` on some systems). The installer copies only the
self-contained `skills/promptharbor` directory and refuses to overwrite an
existing installation. Reload the host's skills or start a new conversation.
Other hosts can load that folder directly. Host-specific discovery behavior
varies; a skill does not independently intercept every message.

No Python is needed for the host to read the skill and evidence. Python enables
the optional CLI, packaging and handoff validators. No model API calls, account
credentials, telemetry or automatic model switching are included.

## Use it

```text
Use $promptharbor to give me Top 3 models for each problem in this conversation.
For projects, split the work and print separate copyable prompts. Keep this
conversation responsible for integration when I return the outputs.
```

Then send a normal question or project brief. For a one-off request:

```text
$promptharbor Which model fits this task: prove the lemma below in Lean?
```

Project prompts include goals, frozen contracts, dependencies, owned files and
acceptance tests. Send them to the chosen models, then bring their complete files
and receipts back to the main conversation. The skill reviews and integrates
them in the authorized workspace. This is user-mediated coordination, not a
service that logs into model providers or dispatches API calls.

## Try the local helpers

```sh
python skills/promptharbor/scripts/harbor.py validate
python skills/promptharbor/scripts/harbor.py recommend --job examples/frontend.json
python skills/promptharbor/scripts/harbor.py recommend --job examples/backtest.json
python skills/promptharbor/scripts/harbor.py recommend --prompt "Summarize this video"
python skills/promptharbor/scripts/project.py compile --project examples/library-system/project.json --out out/handoffs
python -m unittest discover -s tests -v
```

`--prompt` is a conservative English/Chinese keyword fallback with explicitly
low confidence. Semantic classification and project decomposition belong to
the host skill. For reliable CLI use, pass a host-authored structured job.
See [job format](skills/promptharbor/references/job-format.md) and
[project format](skills/promptharbor/references/projects.md).

For reproducible historical examples, use `--as-of 2026-09-29`; omit it for
current advice. Expired records are excluded and may yield no recommendation.

## Evidence and community feedback

The snapshot covers **49 task leaves, 11 models, 50 evidence records and
22 source references**. [Coverage and gaps](docs/COVERAGE.md) show
where measured evidence exists and where only proxies or no evidence exist.

Sources include official documentation, model cards, independent evaluations
and attributed firsthand community reports. [Research notes](docs/RESEARCH.md) explain
what was inspected, including related projects. Every admitted claim links to
its source; original tables, articles and model weights are not redistributed.

Current recommendations require the host to check availability, versions and
fresh task-specific evidence online. Offline output is snapshot-based. The
[refresh process](skills/promptharbor/references/refresh.md) and weekly freshness
workflow identify review work; they never auto-promote scraped claims.
See [methodology](skills/promptharbor/references/evidence.md) and
[third-party attribution](THIRD_PARTY.md).

Community weights default to **30% for visual frontend work, 25% for most writing,
15% generally, and 5% for financial/medical/legal tasks**. These are adjustable
editorial defaults, not empirically calibrated optima. Linked artifacts receive
more support than anecdotes; duplicates add nothing, negative reports subtract,
and undated reports are discounted and expire. Arena crowd evaluations enter the
formal channel once, not again as community anecdotes.

Kimi K3 has both [public web-generation artifacts](https://neuralhub.dev/ai-test-results)
and mixed [firsthand UI feedback](https://www.reddit.com/r/kimi/comments/1vconet/is_kimi_k3_actually_good_or_was_it_overhyped/).
These inform visual-web recommendations without extending to reference fidelity
or backend reliability. [Community policy and formula](skills/promptharbor/references/community.md)
· [resource-filtered frontend example](examples/frontend.json).

## Working boundaries

- **Conditional Top 3:** task, setup and your resources determine the shortlist.
  Fewer than three supported candidates means fewer suggestions, with a reason.
- **Current evidence:** verify versions and access live; offline advice uses the
  dated snapshot. Missing providers and new releases can be added through research.
- **Task fit needs validation:** aesthetic preference, reference fidelity and
  production correctness require different checks. Recommendation accuracy has
  not yet been measured in a blinded cross-model outcome study.
- **You choose; the main window integrates:** prompts move between models through
  you. Shared contracts and actual integration tests govern acceptance; API prices
  and a model name alone do not establish subscription access or total cost.

## Repository

```text
skills/promptharbor/    Portable skill, evidence data, helpers and references
examples/              Single-task jobs and a complete project handoff example
tests/                 Deterministic recommendation and delivery validation
evals/                 Host-level behavioral cases and evaluation rubric
assets/                Original logo, avatar, social preview and local badges
scripts/               Installer, packaging, documentation and freshness checks
docs/                  Research, coverage, design and release guide
.github/               CI, freshness reporting and contribution templates
```

## Develop and release

```sh
python scripts/check_repo.py
python scripts/freshness.py
python scripts/package_skill.py
```

The archive is written to `dist/` with a SHA-256 checksum. See
[CONTRIBUTING.md](CONTRIBUTING.md), [brand assets](assets/brand/README.md) and
[release preparation](docs/RELEASING.md).

## License

Original code, documentation, data curation and artwork are licensed under
[Apache License 2.0](LICENSE). Third-party source materials and model weights
retain their own terms. PromptHarbor is independent and is not endorsed by the
model providers or benchmark publishers.
