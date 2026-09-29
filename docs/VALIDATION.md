# Validation record · 2026-09-29

Observed locally on Windows with Python 3.13.9:

- 49 unittest cases passed, covering catalog links, task filters, incompatible
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
  and user-selected project handoffs. The 15 host behavioral cases remain fixtures.
- The library-system fixture compiled into four complete prompts with three
  execution batches, a frozen interface and evidence sidecars. Receipt checks
  rejected missing work and mismatched interface versions. No library implementation was
  claimed to have been built by this example.
- Logo, wordmark, avatar and social preview were inspected together, including
  the mark at 24, 48, 96 and 128 pixels. SVG assets are self-contained.
- Freshness audit found no due sources or expired catalog records on this date.

Not performed: remote GitHub CI, Linux/Python 3.10 execution, independent host
behavioral evaluation, paid multi-provider output comparison, production library
deployment, public GitHub publishing or a trademark clearance search. CI is
configured to cover Linux/Windows and Python 3.10/3.13 once the repository is pushed.

These checks establish implementation behavior and packaging integrity, not the
accuracy of model recommendations across arbitrary future prompts. The host
evaluation fixtures and scoring process are in `evals/`.
