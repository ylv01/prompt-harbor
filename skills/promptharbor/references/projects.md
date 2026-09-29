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
  "goal": "A small library system with book reviews",
  "constraints": {"current_model": "gpt-6-sol"},
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

Optional task `recommended_model` must be evidence-eligible and accompanied by
`assignment_reason`. This allows the host to choose on task-specific grounds
instead of treating helper sort order as authority. Shared hard constraints
cannot be overridden by tasks. With no established winner, the current feasible
model can be a baseline; clearly label that as no demonstrated comparative edge.

The compiler emits PLAN.md, manifest.json, frozen contract copies, full task
prompts and evidence JSON. It rejects duplicate owners, unsafe paths, missing
contracts, dependency cycles and output overwrites. Render its full prompts in
the current window. The user can then send each prompt to a different model or
reuse one model. No external messages or paid model calls are implicit.

Use the library-system example in the repository as a worked example, not a
mandatory stack. A production system may need authentication, authorization,
privacy, migrations and deployment design absent from a small demonstration.
