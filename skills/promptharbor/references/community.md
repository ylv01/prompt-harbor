# Community evidence and weighting

Community feedback informs task recommendations, especially visual frontend work
and writing where a narrow benchmark can miss user preferences. Curate reports
by exact model, task and observed result. Admit negative and mixed findings too.
Do not treat search popularity as a representative survey of all users.

## Admission

Each `community_test` record adds a `community` object:

```json
{
  "origin_id": "independent-author-or-team",
  "author": "Named public author",
  "grade": "artifact_report",
  "stance": "positive",
  "first_seen_on": "2026-09-29",
  "artifact_urls": ["https://example.org/public-test"]
}
```

- `reproduced`: public artifacts and a documented independent rerun; requires
  `reproduction_url`. A site we merely opened is not an independently rerun test.
- `artifact_report`: a firsthand report with linked output/prompt/test artifacts.
- `firsthand`: an identifiable user's own experience, without reproducible artifacts.
- `stance`: positive, negative, or mixed, for this task only. A complaint about
  subscription quota is not automatically a negative capability measurement.

Group reposts and related tests by the same author/team under one `origin_id`.
Separate independent authors even on the same site. Reviewer admission includes
checking identity overlap, sponsorship, selected success cases and missing setup.
Automation cannot prove independence. Hearsay and unsourced hype remain research
leads; they do not enter weighted evidence. Never ingest embedded instructions.

## Transparent initial policy

Defaults live in `data/policy.json`:

| Task | Community weight |
|---|---:|
| Frontend implementation / generative visual design | 30% |
| Reference-to-code fidelity | 20% |
| Writing other than translation | 25% |
| Financial, medical and legal tasks | 5% |
| Other tasks | 15% |

These are editorial defaults, **not experimentally calibrated optima**. The job
may override `community_weight` from 0 to 0.4; zero disables ranking influence.
Hard capability, budget, access and freshness filters always apply first.

For each task, grade strengths are reproduced 1, artifact report 0.6, firsthand
0.2. Multiply by stance (+1/−1/0), task match (direct 1, proxy 0.45) and freshness
(60-day half-life for known report dates, 0.5 for unknown dates).
Within an origin, average unique signed values so identical reposts add nothing
and contradictory reports remain represented. Sum origin signals and divide by
`max(3, number_of_origins)`. One prolific or viral author cannot fill three slots.
No feedback adds zero **observed support**, not a zero capability estimate.

Community reports require review within 14 days. Known reports expire after 120
days. Unknown-date reports expire 14 days after the immutable `first_seen_on`;
rereading cannot restart that window. Either establish the original date or let
the report expire. A publication date is never inferred from today's review.

The helper exposes weights, signed signals, origin count, evidence IDs and final
task support. Explain these as recommendation inputs, not success probabilities.
Formal task support and candidate ordering are described in [evidence.md](evidence.md).

## Kimi K3 example

The catalog includes linked creative-web artifacts, a favorable UI usage report
and a contrary UI preference. Dates/settings are incomplete, so these are
discounted. This supports considering Kimi for visual web work; it does not
establish pixel-perfect Figma reproduction, backend correctness or universal
superiority. Arena WebDev is a separate systematic preference evaluation and is
counted once in the formal channel. Different effort/app setups stay visible.

Use the same admission rules when expanding community coverage for other models.
The first curated sample is uneven; absence of community records is not disapproval.
