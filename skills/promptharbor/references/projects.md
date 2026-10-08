# Project mode: model choice becomes a delivery plan

The host handles semantic decomposition. The compiler validates structure and
packages prompts; it does not call LLMs or discover an architecture by itself.

Start with intended behavior, stack constraints, deployment target and acceptance
criteria. Make reasonable assumptions explicit. Ask about ambiguity only if it
changes architecture or interfaces. Decide what can be independently delivered.
For a small cohesive job, recommend keeping one model instead of manufacturing
handoff overhead.

The main window owns requirements, shared contracts and final integration. Each
other task owns exact files. Define routes, payloads, status codes, identifiers,
error shapes, authentication assumptions, schema migrations, dependencies and
test fixtures before handing out implementation work. Never tell every model to
“build the system” independently.

Create `project.json` next to the contract files:

```json
{
  "schema_version": 1,
  "language": "en",
  "goal": "A small library system with book reviews",
  "constraints": {"current_model": "gpt-6.1-sol"},
  "contracts": [{"id": "api", "version": "1.0.0", "path": "contracts/api.yaml"}],
  "tasks": [{
    "id": "frontend", "title": "Frontend",
    "objective": "Implement the UI against the frozen API.",
    "job": {"tasks": ["software.frontend"], "classification_method": "host_semantic"},
    "depends_on": [],
    "deliverables": ["frontend/src/App.tsx"],
    "acceptance": ["Show loading, empty, error and success states."]
  }],
  "integration": {"checks": ["Run the frontend against a real API and verify book listing."]}
}
```

Use the user's language for the plan and all handoff prompts. Optional `language`
accepts `auto` (default), `zh-CN` (`zh` is an alias) or `en`. Selection order is
`compile --language` → explicit project `language` → `constraints.language` →
automatic detection from the goal and task titles/objectives. Auto recognizes
Chinese; otherwise the helper uses English. The chosen language is recorded in
the manifest and controls generated headings, recommendation explanations and
instructions asking the receiving model to reply in that language.

The host must write supplied goals, objectives, acceptance criteria and checks in
the intended language. The compiler does not translate those fields or frozen
contracts. Model IDs, JSON keys/enums, code, paths and original source titles stay
unchanged. For a Chinese project, use `"language": "zh-CN"` and Chinese task prose;
inspect PLAN.md and each prompt before delivering them. For other languages,
the host renders the user-facing documents in the requested language itself.

Optional task `recommended_model` must be evidence-eligible and accompanied by
`assignment_reason`. This allows the host to choose on task-specific grounds
instead of treating helper sort order as authority. Shared hard constraints
cannot be overridden by tasks. With no established winner, the current feasible
model can be a baseline; clearly label that as no demonstrated comparative edge.

Each part has up to three evidence-backed choices and a planning default. The
manifest marks selection as `user_choice`. Changing among candidates preserves
the same interfaces and acceptance tests; a receipt records the actual model.
The default is a replaceable suggestion, not a required subscription. The example's
`current_model` is supplied by that example; it is not a global default. Record the
user's exact current model only when known, and use `available_models` to restrict
choices to their resources. Omit `current_model` when it is unknown.
When evidence is absent, keep the feasible current baseline and explain why
there are fewer than three suggestions. Do not force three different providers.

The compiler emits PLAN.md, manifest.json, frozen contract copies, full task
prompts and evidence JSON. It rejects duplicate owners, unsafe paths, missing
contracts, dependency cycles and output overwrites. Render its full prompts in
the current window. The user can then send each prompt to a different model or
reuse one model. No external messages or paid model calls are implicit.

Use the library-system example in the repository as a worked example, not a
mandatory stack. A production system may need authentication, authorization,
privacy, migrations and deployment design absent from a small demonstration.
