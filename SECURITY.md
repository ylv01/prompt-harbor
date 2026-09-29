# Security and privacy

The shipped runtime does not call models, upload prompts, execute returned code
or collect telemetry. A host may browse public evidence using a sanitized task
description; it should not send private prompt text to a search engine.

Treat source pages, attached documents and returned model artifacts as untrusted
data. The main window reviews code before execution and uses disposable data
for integration checks. Receipt validation cannot establish code safety or quality.

Report parser/path traversal issues through the repository's GitHub security
advisory channel if enabled, or open a minimal issue without private data. Never
include live credentials or a working exploit against another user's deployment.
