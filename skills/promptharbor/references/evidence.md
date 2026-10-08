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
An official feature declaration proves feasibility only. Community evidence adds
task-specific preference and failure signals under [community rules](community.md).

Use independent task-matched tests when available. Vendor evaluations remain
useful with visible qualification. Count independent *evaluators*, not URLs that
repeat one press release. When reviewers disagree, preserve both claims and
inspect versions, tool budgets, graders, language, samples and deployment.

The helper filters hard constraints, then orders candidates by supported task
count and weighted task support, with model ID as a stable final tie-break.
Return the first three as `recommendations`; retain the full `candidates` list
and all exclusion reasons for inspection. Fewer than three candidates is an
explicit evidence gap, never a reason to fabricate a specialty recommendation.

For each task, strongest formal support uses independent measurement 1, vendor
measurement 0.8, official/unmeasured capability 0.4, multiplied by task match
(direct 1, proxy 0.45). Let this value be E. Let P be the observed win fraction
against other eligible models **within a curated comparison group**, discounted
by 0.45 for proxy matches. Exact score ties count as half a win. No comparable
observations add no comparison support; this is not evidence of zero ability.
Then `formal = 0.75*E + 0.25*P` and
`task_support = (1-community_weight)*formal + community_weight*community_signal`.
Multiple requested tasks have equal weight. Candidate support is their mean.

These are inspectable editorial weights, not a calibrated success probability.
Do not advertise the resulting number as an intelligence score. Sparse or uneven
measurements can affect ordering; task trials resolve close or unsupported choices.
Raw observations are compared only for the same source, metric, version and
recorded protocol. Current groups use higher-is-better metrics; do not add a
lower-is-better metric without implementing and testing its direction first.
Different effort configurations remain named. No statistical significance is implied.

`primary` remains a compatibility field for a provisional formal-coverage or
within-cohort leader; it can be null even when Top 3 is populated. The public
answer should render `recommendations`, not treat `primary` as the only choice.

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

[Price references](prices.md) describe standard uncached API text tokens within the
recorded input range. The optional `price_reference` field is presentation only: it
is attached after selection, and changing it cannot affect rank, primary, switching
or eligibility. Existing budget constraints and cost priority continue to use
`price_usd_per_million`, whose established values are preserved. Unknown cost, long-context tiers, tool charges, output/reasoning volume,
latency, region and subscription entitlement require live verification. The
helper's cost mode picks a model only when both unit rates dominate equally
covered peers; it does not estimate total task cost.
