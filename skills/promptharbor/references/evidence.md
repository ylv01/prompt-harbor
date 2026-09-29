# Evidence and recommendation policy

The bundled catalog is a curated seed, not a census of current models. Host
browsing should consider missing providers and newly released versions. Do not
default to one company or extrapolate from another member of a model family.

Each evidence record has a source, model version, report/review dates, exact
setup, direct/proxy task mappings, limitations and an optional raw measurement.
Mappings are PromptHarbor editorial judgments; measured results are source facts.
Apply the same proxy rationale consistently across models: repository implementation
results may inform the coding part of a backtest for every tested model, not just
one favored provider. They do not establish financial-methodology expertise.
An official feature declaration proves feasibility only. Community evidence can
surface a failure mode but cannot alone establish superiority.

Use independent task-matched tests when available. Vendor evaluations remain
useful with visible qualification. Count independent *evaluators*, not URLs that
repeat one press release. When reviewers disagree, preserve both claims and
inspect versions, tool budgets, graders, language, samples and deployment.

No synthetic intelligence score is calculated. The helper orders candidates by
complete task coverage, number of directly measured tasks, independently measured
tasks, then any supported tasks. This is retrieval prioritization, **not a model
quality ranking**. Model ID only stabilizes remaining ties. A unique evidence
coverage leader is a provisional suggestion; unequal coverage can reflect
unequal measurement, not unequal skill. Raw scores are compared only in a curated
comparison group with the same source, metric, version and recorded protocol.
Different configurations are always named. No statistical significance is implied.

Confidence is deliberately capped at `limited` for seeded recommendations.
Higher confidence in the host answer requires convergent independent evidence
and a close match to the actual task; it is qualitative, not a probability.

Missing evidence remains missing, not a zero score. A 1M context capacity does
not establish 1M-token recall. GPQA is not proof of research discovery. Finance
Agent filing work does not establish quant alpha. A writing preference on one
language or style does not establish universal writing quality. A browser agent
benchmark is not a base-model-only result. An image-capable model is not an image
generator. Agent tool access and a consumer app subscription are separate facts.

The snapshot defaults to 30-day metadata validity and kind-specific evidence
windows in `data/policy.json`. Freshness uses both report and review dates when
known. Re-reading an old result does not renew its evaluation age. Unknown report
dates are shown as unknown. Old evidence is excluded from current shortlists but
retained for historical inspection. `--as-of` is for reproducible snapshots,
never a workaround to hide stale data from a current user.

Prices describe standard uncached API text tokens within the recorded input
range. Unknown cost, long-context tiers, tool charges, output/reasoning volume,
latency, region and subscription entitlement require live verification. The
helper's cost mode picks a model only when both unit rates dominate equally
covered peers; it does not estimate total task cost.
