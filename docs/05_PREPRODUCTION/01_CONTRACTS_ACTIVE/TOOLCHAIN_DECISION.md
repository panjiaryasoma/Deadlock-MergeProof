# Toolchain Decision

## Required
- IBM Bob 2.0 IDE
- project-level `.bob/custom_modes.yaml`
- project-level `.bob/skills/mergeproof/SKILL.md`
- Git repository
- Python 3.12+ for deterministic validation/evaluation scripts

## Preferred Python dependency policy
Start with standard library.
Add a package only when it removes more complexity than it creates.

## Explicitly deferred
- database
- message queue
- vector database
- external LLM API
- GitHub App
- frontend framework

## Optional after gate
A static HTML report can be generated from validated JSON if time remains.
