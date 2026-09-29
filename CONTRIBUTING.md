# Contributing

Useful contributions improve a task mapping, add verifiable evidence, expose a
routing failure, or make project handoffs easier to integrate.

For evidence changes, include the exact model, primary URL, dates, task, setup,
metric and limitations. Mark vendor results as vendor results. Link a reproducible
community test before admitting community claims. Do not copy full articles or
leaderboard datasets; respect source terms and attribute publishers.

For code changes, use Python 3.10+ and the standard library unless a dependency
solves a demonstrated problem. Run:

```sh
python -m unittest discover -s tests -v
python skills/promptharbor/scripts/harbor.py validate
python scripts/build_docs.py
python scripts/check_repo.py
```

Add behavioral coverage when changing a decision boundary. Avoid tests that
merely compare wording. Keep English and Chinese READMEs consistent. Do not
submit private prompts, API keys, copyrighted full documents or user outputs
without permission. Contribution is under the project's Apache-2.0 license.
