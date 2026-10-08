# Price references

Every Top 3 table shows a price reference, including the question answer, project
PLAN and each complete handoff prompt. Use **USD per million standard text API
input / output tokens**, uncached rates, from the official provider. Include the
applicable input-length tier, source URL and actual price check date. Use the
user's language for labels and notes.

Prices are a reference for choosing among resources. They do not change task
weights, community influence, candidate order, `primary`, switching advice or
resource eligibility. The helper attaches `price_reference` only after selection.
Existing explicit budget caps and `priority: "cost"` still use the separate
`price_usd_per_million` field; display tiers do not expand those established budget
inputs. A long-input display rate can therefore be known while the legacy budget
filter remains unknown for that length.

## Catalog format

An optional model record contains:

```json
"price_reference": {
  "currency": "USD",
  "unit": "per_million_tokens",
  "source_id": "claude-pricing",
  "verified_on": "2026-10-08",
  "tiers": [
    {"max_input_tokens": 100000, "input": 0.10, "output": 0.50},
    {"max_input_tokens": 1000000, "input": 0.50, "output": 2.50}
  ]
}
```

Tiers are contiguous upper bounds: the first applies through 100K input tokens;
the next applies above 100K through 1M. A provided input size selects its matching
tier; an unknown size shows all recorded tiers. Do not assume a token count or
quote the cheapest tier for an entire long request. Missing optional references
fall back to the legacy rate and its model verification date.

Optional `notes: {"en": "...", "zh-CN": "..."}` qualifies time-of-day, regional or
offer differences; `valid_until: "YYYY-MM-DD"` ends a temporary tariff. A reference
older than `metadata_max_age_days`, future-dated, expired or outside its recorded
range is shown as unknown. Empty `tiers` means no verified standard quote, not
free inference. `audit` reports stale priced records without making permanently
missing quotes overdue.

## Scope and current distinctions

- Catalog OpenAI models apply 2× input and 1.5× output rates to the full request
  above 272K input tokens. The display records both tiers through the model context
  limit; legacy budget inputs are unchanged.
  [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra),
  [Sol 6.1](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
  [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna).

- Claude Haiku 5.5 uses $0.10 / $0.50 through 100K input and $0.50 / $2.50 above
  100K, through its 1M context. Other catalog Claude models use standard rates
  across 1M. [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing).
- DeepSeek V4.1 Flash shows the peak reference $0.30 / $1.20, with off-peak
  $0.15 / $0.60 in the same cell. Peak hours are Mon–Fri 01:00–04:00 and
  06:00–10:00 UTC, excluding Chinese public holidays.
  [Official tariff](https://api-docs.deepseek.com/quick_start/pricing/).
- Gemini 3.8 Flash's $0.75 / $3.75 standard tariff ends on 2026-12-31; the offer
  expiration is recorded separately from the normal metadata freshness window.
  [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing).
- Xiaomi references use the overseas USD tariff. Domestic RMB rates are distinct,
  and API balances are separate from Token Plan quota.
  [MiMo pricing](https://mimo.mi.com/docs/en-US/price/pay-as-you-go).
- Open weights have provider-dependent hosted prices and local infrastructure
  costs. Qwen3.8-27B has no single verified standard hosted USD quote in this
  snapshot, so its column says unknown instead of $0.

These observations were checked on 2026-10-08; each catalog entry retains its own
verification date. Cached tokens, batch/fast/priority service, audio/image billing,
server tools, extra reasoning/output volume, regional rates and consumer app
subscriptions can change the bill. A unit price is not an estimate of total task
cost or proof of subscription access. Verify the chosen endpoint before spending.
