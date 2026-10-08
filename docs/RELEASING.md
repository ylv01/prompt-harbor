# Release preparation

Public repository: [ylv01/prompt-harbor](https://github.com/ylv01/prompt-harbor).
The default branch is `main`. Publishing source commits and creating a tagged
release are separate steps.

1. Read README and coverage gaps. Confirm the desired public repository name,
   account and visibility. PromptHarbor is a project name, not trademark clearance.
2. Run local tests, `harbor.py validate`, `scripts/check_repo.py` and freshness
   audit. A stale model-data snapshot needs review, not a cosmetic date bump.
3. Review all files for private paths/prompts and credentials. The example's
   current model is hypothetical and its stack is explicitly scoped.
4. Run `python scripts/package_skill.py`; inspect archive contents.
   The installed skill includes code, data, references, artwork and licensing.
5. Push reviewed commits to the repository above. Keep the description focused
   on task-specific Top 3 recommendations and multi-model project handoffs.
6. Set topics such as `agent-skill`, `llm`, `model-selection`, `ai-agents` and
   `prompt-engineering`. Upload `assets/brand/social-preview.png` as social preview.
   The avatar is available for a project organization or other avatar surface.
7. Let remote CI run. Create a tag matching the skill metadata version and a release with the skill ZIP
   after checks pass. Do not use an unrun CI status badge.

Future releases: bump skill metadata, CHANGELOG and generated version badge
together. Evidence snapshot date is separate. Regenerate docs and recompile the
checked-in historical handoff example if its fixture contracts or compiler change.
Preserve previous factual report dates. Do not claim full model recommendation
accuracy until the host-level/outcome evaluation has actually been performed.
