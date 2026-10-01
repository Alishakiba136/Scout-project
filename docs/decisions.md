# SCOUT Product Decisions

This note complements the decision log and captures the high-level product direction for the project.

- SCOUT is local-first and privacy-conscious.
- The phone is the initial runtime target.
- The architecture must remain modular and maintainable.
- M0 is intentionally limited to bootstrap and diagnostics.
- The LLM never directly controls motors or other physical safety-critical hardware.
- SQLite is the default choice for local memory and metadata.
- Development is driven by tests and logs rather than ad hoc prototype growth.
