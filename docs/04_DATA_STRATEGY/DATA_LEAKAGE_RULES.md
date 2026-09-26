# Data Leakage Rules

1. Bob must not read `expected_output` files before producing a candidate report.
2. Ground-truth fixture metadata must live outside the analysis-visible subtree during evaluation.
3. Evaluation prompts must not reveal the expected advisory.
4. File names must not encode the defect label (avoid `broken_deadline.py`).
5. Real-world incident summaries are not included in the demo repo if they hint at the seeded mutation.
6. Manual evaluator notes are stored outside the repository opened in Bob.
