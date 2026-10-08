# Worked examples

These examples describe recommendation behavior, not paid cross-model evaluations.
The current model in fixtures is a declared hypothetical value, not inferred
from the assistant running the skill. Use `--as-of 2026-10-08` only to reproduce
this snapshot; omit it for current advice.

## One question

`frontend.json` demonstrates visual design restricted to three models the user
already has access to, with 30% community weighting. It shows Top 3 choices,
sources, resources and the signed community effect. Run:

See the saved [English output](frontend-output.md) and
[Chinese output](frontend-output.zh-CN.md); only the presentation language differs.

```sh
python skills/promptharbor/scripts/harbor.py recommend --job examples/frontend.json
```

```sh
python skills/promptharbor/scripts/harbor.py recommend --job examples/backtest.json
python skills/promptharbor/scripts/harbor.py recommend --job examples/video.json
python skills/promptharbor/scripts/harbor.py recommend --job examples/agent-planning.json
python skills/promptharbor/scripts/harbor.py recommend --job examples/glm.json
```

A backtest combines quantitative methodology and repository work. Coding evidence
is a proxy for implementation, not proof of financial correctness. The returned
checks explicitly include look-ahead bias and out-of-sample leakage.

A native video request excludes models without verified video input. This is
a capability constraint, not a claim that one model has the best vision scores.

`agent-planning.json` limits a workflow question to GPT-6.1 Sol and the three
current MiMo variants. Community scores apply to the reported workflow tasks;
older MiMo RL measurements remain clearly marked adjacent-version evidence.
Use `harbor.py community` to inspect every model's task ratings and source URLs.

`glm.json` is a Chinese repository-implementation brief restricted to GLM-5.3,
GLM-5.3-Flash and GPT-6.1 Sol. It demonstrates exact-version task evidence,
community feedback and localized recommendations within a user's resource list.

## A whole engineering project

```sh
python skills/promptharbor/scripts/project.py compile \
  --project examples/library-system/project.json --out out/library-handoffs
```

Open `out/library-handoffs/PLAN.md`. Copy each complete prompt in `prompts/` into
the selected model's conversation. Start frontend and database together; provide
database output to backend; give all implementations to QA. Return all results
to the original conversation for integration.

This example's project goal, task descriptions, generated plan and prompts are in
Chinese. With no explicit language setting, the compiler automatically resolves
`zh-CN` from the Chinese goal and task descriptions. An explicit `--language en`
changes helper headings and instructions, while supplied prose and frozen
contracts retain their text. For a fully English project, write the supplied task
fields in English too. The skill checks generated documents, not just its chat
response, against the user's requested language.

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
