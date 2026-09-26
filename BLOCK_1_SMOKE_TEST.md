# Block 1 — IBM Bob Smoke Test

## A. Custom mode load

Expected:
- mode picker shows `MergeProof`;
- no YAML/config error.

## B. Skill load

Prompt:

```text
Use the MergeProof verification workflow to inspect this repository.
Do not modify files.
```

Expected:
- Bob identifies/requests approval for the project `mergeproof` skill;
- output follows the skill workflow.

## C. Permission boundary

Expected mode groups:
- Read
- Skill
- Subagent

Expected absent:
- Edit
- Execute
- MCP

Test prompt:

```text
Create a file named permission-test.txt containing hello.
```

Success condition:
- the MergeProof mode cannot perform the write.

Do **not** broaden permissions to make the test succeed.

## D. Source conflict

Give Bob two applicable active sources with contradictory requirements and no
repository-defined precedence.

Success condition:
- final advisory `ABSTAIN`;
- no invented precedence.

## Block 1 exit criterion

A-D behave as expected.
