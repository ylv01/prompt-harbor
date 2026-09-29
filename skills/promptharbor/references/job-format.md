# Structured job format

All fields except `tasks` are optional. Unknown fields fail validation.

```json
{
  "tasks": ["finance.backtest", "software.repo"],
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

Example output includes classification, provisional primary (or null), evidence
records, source links, switch decision, excluded models with reasons, stale record
IDs and task-specific validation checks. Helper JSON is intended for the host;
the skill renders a concise answer in the user's language.
