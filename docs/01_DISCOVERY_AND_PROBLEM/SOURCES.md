# Source Register

- **SRC-001 — IBM Bob - Custom modes**  
  https://bob.ibm.com/docs/ide/configuration/custom-modes  
  Authority: `official_vendor`  
  Used claim: Bob supports project-level YAML custom modes with role definitions, tool permissions, custom instructions, and allowed subagents.

- **SRC-002 — IBM Bob - Skills**  
  https://bob.ibm.com/docs/ide/features/skills  
  Authority: `official_vendor`  
  Used claim: Bob skills are reusable instruction sets stored in .bob/skills and can include supporting files/scripts.

- **SRC-003 — IBM Bob - Subagents**  
  https://bob.ibm.com/docs/shell/features/subagents  
  Authority: `official_vendor`  
  Used claim: Bob can spawn focused independent subagents and return summaries to the main conversation, with approval.

- **SRC-004 — IBM Bob - Modes**  
  https://bob.ibm.com/docs/ide/features/modes  
  Authority: `official_vendor`  
  Used claim: Ask is read-oriented, Plan is for design, Agent is for modifications; mode permissions can restrict tools.

- **SRC-005 — IBM Bob - /init and AGENTS.md**  
  https://bob.ibm.com/docs/ide/tutorials/start-a-project  
  Authority: `official_vendor`  
  Used claim: Bob can generate AGENTS.md project context and mode-specific rules for consistent repository understanding.

- **SRC-006 — Google Engineering Practices - Code Review**  
  https://google.github.io/eng-practices/review/  
  Authority: `official_engineering_practice`  
  Used claim: Code review is used to maintain code/product quality and should examine design, functionality, complexity, tests, and related concerns.

- **SRC-007 — Pact Docs - Contract Testing**  
  https://docs.pact.io/  
  Authority: `official_project_docs`  
  Used claim: Contract testing verifies a shared understanding between consumer/provider and can verify provider behavior conforms to documented contracts.

- **SRC-008 — Swagger Contract Testing - Drift**  
  https://support.smartbear.com/swagger/contract-testing/docs/en/drift.html  
  Authority: `official_vendor`  
  Used claim: API drift occurs when implementation diverges from specification and can cause broken integrations, inaccurate docs, and unintended breaking changes.

- **SRC-009 — Stripe - APIs as infrastructure: versioning**  
  https://stripe.com/blog/api-versioning  
  Authority: `official_vendor_engineering`  
  Used claim: API fields and types form compatibility expectations; backward-incompatible changes can break integrations, motivating review and versioning.

- **SRC-010 — SEC - Knight Capital enforcement release**  
  https://www.sec.gov/newsroom/press-releases/2013-222  
  Authority: `regulator`  
  Used claim: Knight Capital's deployment/control failures triggered millions of orders and losses exceeding $460M, illustrating high cost of unverified change/deployment state.

- **SRC-011 — CrowdStrike - Channel File 291 RCA**  
  https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf  
  Authority: `primary_incident_report`  
  Used claim: A 21-vs-20 input mismatch evaded multiple validation/testing layers and contributed to system crashes.

- **SRC-012 — OWASP REST Security Cheat Sheet**  
  https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html  
  Authority: `security_guidance`  
  Used claim: REST APIs should validate input type/length/range/format and reject unexpected content.

- **SRC-013 — The Impact of Traceability on Software Maintenance and Evolution**  
  https://arxiv.org/abs/2108.02133  
  Authority: `research_mapping_study`  
  Used claim: A mapping study of 63 studies reports traceability supports maintenance/evolution, especially change management, while maintaining trace links is costly.

- **SRC-014 — How Requirements Quality Makes (or Breaks) Traceability Link Recovery**  
  https://arxiv.org/abs/2606.11834  
  Authority: `research_preprint`  
  Used claim: Requirement quality defects affect automated traceability-link recovery performance; approach choice depends on source quality.

- **SRC-015 — Traceability Links between Release Notes & Software Artifacts**  
  https://arxiv.org/abs/2511.18187  
  Authority: `research_preprint`  
  Used claim: Study reports missing/broken traceability links in open-source release artifacts and explores LLM-assisted recovery.
