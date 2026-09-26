# Baseline Contract — MergeProof v1.0

## Input contract

Required:
- repository root;
- current commit SHA or explicit "unversioned";
- changed-file scope;
- registered sources;
- Bob mode version;
- skill version.

Optional:
- PR/issue text;
- manual reviewer question.

## Output contract

Machine-readable report:
- metadata;
- resolved sources;
- extracted requirements;
- findings;
- advisory;
- unresolved questions.

Human-readable summary:
- same conclusion set, no extra hidden findings.

## Allowed advisory

`PASS | REVIEW_REQUIRED | ABSTAIN`

## Authority contract

Human reviewer retains merge authority.

## Evidence contract

A confirmed issue with no valid source/repo anchor is invalid output.

## Mutation contract

Verification mode must not modify application code.
