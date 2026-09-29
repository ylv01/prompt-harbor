# Release preparation

The repository is prepared locally. A repository owner/remote has not been
selected, and no GitHub upload or release is implied by these files.

1. Read README and coverage gaps. Confirm the desired public repository name,
   account and visibility. PromptHarbor is a project name, not trademark clearance.
2. Run local tests, `harbor.py validate`, `scripts/check_repo.py` and freshness
   audit. A stale model-data snapshot needs review, not a cosmetic date bump.
3. Review all files for private paths/prompts and credentials. The example's
   current model is hypothetical and its stack is explicitly scoped.
4. Run `python scripts/package_skill.py`; inspect archive contents.
   The installed skill includes code, data, references, artwork and licensing.
5. Create the public repository and push the reviewed local commits once the
   destination is authorized. Set repository description to:
   `Task-aware model advice and contract-based multi-model project handoffs.`
6. Set topics such as `agent-skill`, `llm`, `model-selection`, `ai-agents` and
   `prompt-engineering`. Upload `assets/brand/social-preview.png` as social preview.
   The avatar is available for a project organization or other avatar surface.
7. Let remote CI run. Create tag `v0.2.1` and a release with the skill ZIP
   after checks pass. Do not use an unrun CI status badge.

Future releases: bump skill metadata, CHANGELOG and generated version badge
together. Evidence snapshot date is separate. Regenerate docs and recompile the
checked-in historical handoff example if its fixture contracts or compiler change.
Preserve previous factual report dates. Do not claim full model recommendation
accuracy until the host-level/outcome evaluation has actually been performed.
