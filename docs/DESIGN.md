# Architecture

Prompt → host semantic task profile → evidence retrieval + hard capability
filters → qualified recommendation. For projects: profile → deliverable DAG →
shared contracts → model assignments → portable prompts → returned artifacts →
main-window integration.

There is no backend service, hidden model call, embedding index or telemetry.
The default runtime is Python's standard library plus the host agent's existing
reading/browsing abilities. Model selection is not tied to the user's hardware.

## Data ownership

- taxonomy.json: domain, subdomain, leaf, meaning and acceptance-test suggestion.
- models.json: exact public identifiers, lifecycle, verified capabilities and prices.
- sources.json: primary URL, publisher, publication/check dates and review interval.
- evidence.json: atomic claims with direct/proxy mappings and raw observations.
- policy.json: freshness policy; no universal ability weights.

The helper uses readable JSON and explicit joins, suitable for small human-reviewed
catalogs. Split by domain or add an index only when scale justifies it. There is
one source of truth per field. Generated coverage and badges must be regenerated
when the catalog changes.

## Project artifacts

Project JSON defines a DAG, contracts, owned files and acceptance checks. Compiler
outputs are reviewable text, not provider-specific API requests. Contract hashes
detect drift. Receipts make missing work visible, but are not trusted as proof
of code behavior. Integration remains an active host-agent task.

The compiler does not select an architecture, infer requirements or generate a
project JSON from text. Those are host skill responsibilities. It validates and
packages a proposed decomposition. No unattended execution is implied.

## Evaluation boundary

Unit tests exercise exclusion, staleness, comparisons, paths, dependency ordering
and delivery validation. Host behavioral cases exercise interpretation and
communication. A future outcome study should blind-grade task outputs from the
recommended model and baselines, measuring regret, total cost, latency and handoff
defects. Until such a study is run, do not publish recommendation accuracy numbers.
