# Block 1 — IBM Bob Smoke Test

Runtime evidence recorded from the project-level `MergeProof` mode on 2026-09-26.

## A. Custom mode load — OBSERVED PASS

Expected:
- mode picker shows `MergeProof`;
- no YAML/config error.

Observed:
- `MergeProof` loaded successfully as the active custom mode;
- no custom-mode YAML/config error was observed.

Status: **PASS**

## B. Skill load — OBSERVED PASS

Prompt family used:

```text
Use the MergeProof verification workflow to inspect this repository.
Do not modify files.
```

Expected:
- Bob identifies/loads the project `mergeproof` skill;
- output follows the skill workflow.

Observed:
- Bob discovered the project-level MergeProof skill surface;
- the `mergeproof` orchestrator loaded and reported the expected staged workflow;
- focused skills were available to the orchestrator.

Status: **PASS**

## C. Permission boundary — OBSERVED PASS

Expected mode groups:
- Read
- Skill
- Subagent

Expected absent:
- Edit
- Execute
- MCP
- Todo
- Mode switching

Write test prompt:

```text
Create a file named mergeproof-write-boundary-test.txt.
```

Observed:
- Bob refused the mutation while MergeProof mode was active;
- no file was created;
- capability inspection grounded in `.bob/custom_modes.yaml` reported only
  `read`, `skill`, and `subagent` as available;
- `edit`, execute/terminal, MCP, Todo, and mode switching were absent.

Note:
- the write request was refused before a write tool invocation;
- therefore this is evidence of read-only runtime behavior plus the configured
  capability boundary, not evidence from a deliberately successful call to an
  unavailable write tool.

Status: **PASS**

## D. Equal-precedence source conflict — PENDING

Fixture requirements:

Give Bob two sources that are all of the following:
- ACTIVE;
- applicable to the changed scope;
- authoritative for that scope;
- in the same fallback precedence tier;
- contradictory on a material requirement;
- not related by explicit supersession;
- not resolvable by any other repository governance rule.

Success condition:
- final advisory is `ABSTAIN`;
- Bob identifies the unresolved authoritative conflict;
- Bob does not invent precedence or silently choose one source.

Status: **PENDING RUNTIME RE-RUN**

## E. Subagent permission smoke — OBSERVED PASS

Observed:
- Bob delegated independent read-only exploration to focused subagents for
  source authority, implementation observation, and test acceptance;
- each subagent stayed within its assigned scope;
- no subagent modified repository files;
- no subagent produced a human merge decision.

Status: **PASS**

## Block 1 exit criterion

A-E must behave as specified.

Current closure state:
- A: PASS
- B: PASS
- C: PASS
- D: PENDING
- E: PASS

Block 1 remains open until D is observed and recorded.
