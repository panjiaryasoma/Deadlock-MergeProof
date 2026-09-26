# MergeProof

**Team:** Deadlock  
**Status:** IBM Bob 2.0 Hackathon MVP scaffold

MergeProof is a Bob-native pre-merge evidence workflow. It checks whether a proposed
software change still aligns with active requirements, contracts, acceptance criteria,
implementation, and tests.

Final advisories:
- `PASS`
- `REVIEW_REQUIRED`
- `ABSTAIN`

Human reviewers retain merge authority.

## Layout

```text
.
├── .bob/
│   ├── custom_modes.yaml
│   ├── rules-mergeproof/
│   └── skills/mergeproof/
├── src/mergeproof/
├── tests/
├── eval/
├── demo/
├── reports/
├── schemas/
├── scripts/
└── docs/  # keep the preproduction pack you already moved here
```

## Block 1 first

Open this repo in IBM Bob and confirm the `MergeProof` mode appears.

Expected permissions:
- Read
- Skill
- Subagent

Intentionally absent:
- Edit
- Execute
- MCP

Do not broaden permissions just to make the smoke test convenient.
