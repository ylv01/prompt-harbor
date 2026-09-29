# Worked examples

These examples describe recommendation behavior, not paid cross-model evaluations.
The current model in fixtures is a declared hypothetical value, not inferred
from the assistant running the skill. Use `--as-of 2026-09-29` only to reproduce
this snapshot; omit it for current advice.

## One question

`frontend.json` demonstrates visual design restricted to three models the user
already has access to, with 30% community weighting. It shows Top 3 choices,
sources, resources and the signed community effect. Run:

```sh
python skills/promptharbor/scripts/harbor.py recommend --job examples/frontend.json
```

```sh
python skills/promptharbor/scripts/harbor.py recommend --job examples/backtest.json
python skills/promptharbor/scripts/harbor.py recommend --job examples/video.json
```

A backtest combines quantitative methodology and repository work. Coding evidence
is a proxy for implementation, not proof of financial correctness. The returned
checks explicitly include look-ahead bias and out-of-sample leakage.

A native video request excludes models without verified video input. This is
a capability constraint, not a claim that one model has the best vision scores.

## A whole engineering project

```sh
python skills/promptharbor/scripts/project.py compile \
  --project examples/library-system/project.json --out out/library-handoffs
```

Open `out/library-handoffs/PLAN.md`. Copy each complete prompt in `prompts/` into
the selected model's conversation. Start frontend and database together; provide
database output to backend; give all implementations to QA. Return all results
to the original conversation for integration.

The example interprets “评价” as user ratings and book reviews. It is a small
local demonstration, not a complete production library system. Technology choices
are example assumptions. The skill chooses contracts suitable for the real user.

Database design has no direct comparative evidence in the seed catalog: the
example retains the declared current model as a baseline and supplies SQL checks.
This is intentional honesty, not an unsupported specialty recommendation.

## Session routing

```text
Use $promptharbor for this conversation. For each problem I send, first identify
the task and recommend Top 3 models. For engineering projects, split the work
and print separate copyable prompts, keeping this conversation as integrator.
```

Then simply send an ordinary prompt, for example:

```text
帮我制作一个图书管理系统，包括书评和评分。
```

The host performs semantic decomposition; the CLI does not turn this sentence
into the project JSON by itself. See `evals/host-cases.json` for behavioral cases
covering mixed tasks, negative instructions, unknown fields and integration.
