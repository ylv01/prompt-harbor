# Changelog

## 0.4.0 — 2026-10-08

- Add Claude Haiku 5.5 with exact-version official capabilities, qualified vendor
  results, a Plotly analytics evaluation and three original community task reports.
- Add input/output price reference columns to single-task Top 3 tables, project
  plans and every handoff prompt, with context tiers, source links and check dates.
- Keep display prices separate from ranking, switching, resource eligibility and
  existing budget/cost-priority behavior; missing or expired references stay unknown.
- Cover all catalog models with qualified price references or explicit unknowns,
  including Haiku long-input rates, DeepSeek time rates and Gemini offer expiry.
- Extend price refresh auditing, bilingual documentation, examples and regression checks.

## 0.3.2 — 2026-10-08

- Remove GPT-6 Sol from active recommendations and resource examples; use the
  separately evidenced GPT-6.1 Sol. Keep replaceable project planning defaults.
- Add GLM-5.3 and GLM-5.3-Flash with exact-version capabilities, task evaluations,
  attributed positive/adverse community assessments and full Chinese catalog text.
- Admit a separate October 7 WebDev cohort, including GPT-6.1 Sol and both GLM
  variants. Preserve historical observations without relabeling measurements.
- Refresh bilingual examples, coverage, badges and standalone packaging.

## 0.3.1 — 2026-09-30

- Fixed Chinese requests producing English saved plans and handoff prompts.
- Added automatic Chinese/English output language selection, explicit job/project
  language settings and CLI overrides; localized recommendation explanations,
  plan sections, prompt instructions and return guidance.
- Preserved model IDs, machine-readable fields, source titles and frozen contract
  text; the host writes supplied task prose in the user's language.
- Added a Chinese project-document regression case and refreshed the worked example.

## 0.3.0 — 2026-09-30

- Added GPT-6.1 Sol and MiMo-V2.6-Pro, Flash and Pro-UltraSpeed; the catalog now
  contains 15 exact models.
- Researched community reports for every catalog model, with a per-model search
  log, task-specific editorial scores out of 10, reasons, dates and confidence.
- Added `harbor.py community` and a generated community assessment table with
  source-linked model/task ratings; unsupported tasks remain unrated.
- Community ranking now uses the signed editorial score alongside report quality,
  task match, origin deduplication and freshness. Negative and mixed findings stay
  visible; existing task weights and the 40% override limit are preserved.
- Distinguished MiMo launch-period tool-loop complaints, corrected current API
  aliases and original RL checkpoints instead of combining their results.
- Updated the portable skill, bilingual documentation, attribution and examples.

## 0.2.1 — 2026-09-29

- Simplified handoffs to interface versions and actual implementation review.
- Removed cryptographic contract fingerprints, package checksum sidecars, arbitrary
  contract-size limits and forced byte-identical ZIP generation.
- Packaging now writes a normal ZIP and supports rebuilding the same output.

## 0.2.0 — 2026-09-29

- Default Top 3 recommendations with resource details, source-backed reasons and full audit output.
- Top 3 choices per project part; portable prompts preserve contracts and record the actual model used.
- Task-specific community weights, positive/negative reports, independent-origin deduplication,
  age decay, undated-report expiry and strict resource filters.
- Kimi K3 creative-web artifacts and conflicting firsthand UI reports; Arena WebDev snapshot
  evaluated once in the formal channel across ten catalog models.
- Separate creative visual design and reference fidelity tasks; catalog now has 49 tasks,
  50 evidence records and 22 sources.
- Consolidated README boundaries, documented weighting formula and new regression checks.

## 0.1.0 — 2026-09-29

- Initial portable Agent Skill with semantic-host single-question and project modes.
- Curated 47-task taxonomy, 11-model snapshot, 37 evidence records and 18 sources.
- Conservative evidence retrieval, capability filters, freshness and switch advice.
- Contract-based project handoffs, dependency checks and delivery receipt validation.
- Library-system worked example, behavioral cases and deterministic tests.
- English/Chinese READMEs, original vector brand, avatar/social images and local badges.
- Installer, reproducible skill archive, CI and scheduled review reporting.

Entries record repository changes; a release tag and GitHub release are separate
publication steps.
