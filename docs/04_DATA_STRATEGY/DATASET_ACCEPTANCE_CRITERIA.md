# Evaluation Corpus Acceptance Criteria

Corpus is accepted when:

- [ ] every case has immutable case ID;
- [ ] every seeded defect has known mutation operator;
- [ ] expected class/advisory are fixed before run;
- [ ] clean controls exist;
- [ ] ambiguity controls exist;
- [ ] no fixture filename leaks the answer;
- [ ] expected outputs are hidden from Bob during analysis;
- [ ] all source and code anchors can be manually verified;
- [ ] at least one case tests explicit supersession;
- [ ] at least one case tests best-practice-vs-requirement distinction;
- [ ] frozen 8-case triage suite is unchanged after implementation starts.
