# Validation record · 2026-09-30

Observed locally on Windows with Python 3.13.9:

- **70 unittest cases passed**, covering catalog links, task filters, incompatible
  metrics, missing and stale data, unknown current models, proxy consistency,
  dependency cycles, artifact ownership, interface versions and missing deliveries.
- Skill Creator's `quick_validate.py` accepted the portable skill. Windows
  default GBK decoding required rerunning that external validator with `-X utf8`;
  the project's own readers explicitly use UTF-8.
- `scripts/check_repo.py` passed: required artifacts, JSON, SVG, generated data
  documentation, local links and machine-specific path checks.
- Both a copied installation and an extracted ZIP ran `harbor.py validate`
  outside the repository. The extracted skill runs independently of the repository.
- Top 3 checks cover resource filtering, changing rank with community weights,
  duplicate suppression, negative evidence, unknown-date expiry, hard constraints
  and user-selected project handoffs. The 16 host behavioral cases remain fixtures.
- Chinese requests generate Chinese plans, handoff instructions, recommendation
  explanations, evidence summaries and validation guidance. Explicit English and
  CLI overrides work, language does not change ranking, frozen contract bytes
  remain unchanged, and the standalone ZIP includes the locale data and helper.
- New community checks cover 0–10 task ratings, missing scores, artifact/directness
  weighting, future assessment exclusion, all-model search coverage and source-linked
  CLI reports. GPT-6.1 Sol and all three MiMo variants pass explicit resource filtering.
- A known pre-update MiMo report retains its negative result and original score
  while its influence on the current revision is reduced by the documented 0.25 factor.
- Local open-weight filtering includes MiMo Pro/Flash and excludes the exact
  hosted UltraSpeed tier, whose acceleration is not a downloadable checkpoint.
- The library-system fixture compiled into four complete prompts with three
  execution batches, a frozen interface and evidence sidecars. Receipt checks
  rejected missing work and mismatched interface versions. No library implementation was
  claimed to have been built by this example.
- Logo, wordmark, avatar and social preview were inspected together, including
  the mark at 24, 48, 96 and 128 pixels. SVG assets are self-contained.
- Freshness audit found no due sources, expired records or overdue community searches.

The previous published revision passed GitHub CI on Linux/Windows and Python
3.10/3.13. The same matrix validates each new push; current results are in
[GitHub Actions](https://github.com/ylv01/prompt-harbor/actions).

Not performed: independent host behavioral evaluation, community-test reproduction,
paid multi-provider output comparison, production library deployment or trademark
clearance. The logo and layout inspections above were completed for the initial release.

These checks establish implementation behavior and packaging integrity, not the
accuracy of model recommendations across arbitrary future prompts. The host
evaluation fixtures and scoring process are in `evals/`.
