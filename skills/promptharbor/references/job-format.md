# Structured job format

All fields except `tasks` are optional. Unknown fields fail validation.

```json
{
  "tasks": ["finance.backtest", "software.repo"],
  "language": "auto",
  "classification_method": "host_semantic",
  "classification_confidence": "high",
  "current_model": "gpt-6-sol",
  "available_models": ["gpt-6-sol", "claude-opus-5-5", "deepseek-v4.1-flash"],
  "input_modalities": ["text"],
  "tools_required": true,
  "context_tokens": 24000,
  "open_weights_only": false,
  "allow_preview": false,
  "priority": "quality",
  "community_weight": 0.15,
  "notes": ["Classification confidence is separate from evidence confidence."]
}
```

`tasks`: 1–6 unique IDs from taxonomy.json. `available_models`: exact catalog IDs;
an empty list means no available models, not all models. `current_model`: exact
ID if known; unknown IDs yield unknown switch advice. `input_modalities`: text,
image, video, audio. If omitted, visual/audio task leaves add their input modality.
`context_tokens`: nonnegative integer for required total context, including output
headroom; unknown should be omitted. `priority`: quality (default), cost or latency.
`max_input_price` and `max_output_price`: nonnegative USD per million text tokens;
not subscription prices or total request budgets. Unknown pricing fails a hard cap.
`prompt`: optional original request, local only; omit sensitive text when sharing.

`language`: `auto` (default), `zh-CN` (`zh` alias) or `en`. An explicit
`recommend --language` overrides the job setting. Auto recognizes Chinese in the
job's prompt; otherwise helper output is English. The resolved language is
included in the result and applies to recommendation reasons, explanations and
Markdown headings. Supplied notes and original source titles retain their text;
the host writes its explanations and saved documents in the user's language.

`community_weight`: optional number from 0 to 0.4. Omit to use task-specific
defaults; 0 disables community influence. See [community policy](community.md).
Tell the host which exact models your subscriptions/APIs provide when you want
Top 3 restricted to existing resources; model availability does not imply quota,
tool entitlement or an automatic purchase.

Example output includes three ranked `recommendations` (or the actual smaller
count), each with `reason`, `resources`, evidence and a `ranking` audit breakdown.
`candidates` retains the complete shortlist. It also includes classification,
provisional primary (or null), evidence
records, source links, switch decision, excluded models with reasons, stale record
IDs and task-specific validation checks. Helper JSON is intended for the host;
the skill renders a concise answer in the user's language, including saved files.
