# Repository Execution Plan

Proposed repository layout:

```text
mergeproof/
├── .bob/
│   ├── custom_modes.yaml
│   ├── rules-mergeproof/
│   │   ├── 01-authority.md
│   │   ├── 02-source-precedence.md
│   │   └── 03-report-contract.md
│   └── skills/
│       └── mergeproof/
│           ├── SKILL.md
│           ├── severity-guide.md
│           └── report-template.md
├── schemas/
│   └── mergeproof_report.schema.json
├── scripts/
│   ├── validate_report.py
│   └── summarize_eval.py
├── demo/
│   ├── docs/
│   ├── src/
│   └── tests/
├── eval/
│   ├── fixtures/
│   └── expected/
├── reports/
└── README.md
```

Branching/remote mutation is deliberately outside this document. Repository actions follow the owner's explicit approval process.
