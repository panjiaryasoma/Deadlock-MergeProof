# SOURCE EVALUATION SUITE 001–030

Purpose: test source provenance, authority, scope, and claim discipline.

## SOURCE-001
- Candidate: IBM custom modes official docs
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-001`
- Rationale: Official capability evidence

## SOURCE-002
- Candidate: IBM skills official docs
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-002`
- Rationale: Official capability evidence

## SOURCE-003
- Candidate: IBM subagents official docs
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-003`
- Rationale: Official capability evidence

## SOURCE-004
- Candidate: IBM modes official docs
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-004`
- Rationale: Official capability evidence

## SOURCE-005
- Candidate: IBM AGENTS.md official docs
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-005`
- Rationale: Official capability evidence

## SOURCE-006
- Candidate: Google engineering code review guide
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-006`
- Rationale: Strong practitioner guidance, not product requirement

## SOURCE-007
- Candidate: Pact official docs
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-007`
- Rationale: Established contract-testing mechanism

## SOURCE-008
- Candidate: Swagger/SmartBear Drift docs
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-008`
- Rationale: Vendor definition of API drift; useful but product-adjacent

## SOURCE-009
- Candidate: Stripe engineering API versioning
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-009`
- Rationale: Primary practitioner evidence for compatibility contracts

## SOURCE-010
- Candidate: SEC Knight Capital order/release
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-010`
- Rationale: Regulatory primary evidence of change/deployment-control failure

## SOURCE-011
- Candidate: CrowdStrike RCA
- Expected decision: `ACCEPT_CORE`
- Reference: `SRC-011`
- Rationale: Primary incident RCA with concrete interface mismatch

## SOURCE-012
- Candidate: OWASP REST guidance
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-012`
- Rationale: Security guidance, not project requirement by itself

## SOURCE-013
- Candidate: Traceability mapping study
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-013`
- Rationale: Research synthesis; supports problem framing

## SOURCE-014
- Candidate: 2026 traceability quality preprint
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-014`
- Rationale: Recent research; preprint status must be disclosed

## SOURCE-015
- Candidate: 2025 release artifact traceability preprint
- Expected decision: `ACCEPT_CONTEXT`
- Reference: `SRC-015`
- Rationale: Recent research; preprint status must be disclosed

## SOURCE-016
- Candidate: Anonymous Medium post with no sources
- Expected decision: `REJECT`
- Reference: `N/A`
- Rationale: Low authority and unverifiable

## SOURCE-017
- Candidate: Reddit anecdote about broken API
- Expected decision: `REJECT_CORE`
- Reference: `N/A`
- Rationale: May inspire discovery, cannot support core factual claim

## SOURCE-018
- Candidate: Vendor landing page claiming '10x productivity'
- Expected decision: `REJECT_METRIC`
- Reference: `N/A`
- Rationale: Marketing claim without evaluation method

## SOURCE-019
- Candidate: AI-generated summary without links
- Expected decision: `REJECT`
- Reference: `N/A`
- Rationale: No provenance

## SOURCE-020
- Candidate: Outdated PRD explicitly superseded by ADR
- Expected decision: `REJECT_AUTHORITY`
- Reference: `N/A`
- Rationale: Superseded project source

## SOURCE-021
- Candidate: Current OpenAPI contract in repo
- Expected decision: `ACCEPT_CORE`
- Reference: `project`
- Rationale: Machine-readable in-scope project contract

## SOURCE-022
- Candidate: Issue comment contradicting active OpenAPI with no decision record
- Expected decision: `DOWNRANK`
- Reference: `project`
- Rationale: Lower authority; flag conflict if material

## SOURCE-023
- Candidate: Acceptance criteria attached to current change
- Expected decision: `ACCEPT_CORE`
- Reference: `project`
- Rationale: Change-specific source when not superseded

## SOURCE-024
- Candidate: Test code only, no written requirement
- Expected decision: `ACCEPT_EVIDENCE_NOT_REQUIREMENT`
- Reference: `project`
- Rationale: Tests show behavior but are not automatically business authority

## SOURCE-025
- Candidate: Code comment contradicting implementation
- Expected decision: `ABSTAIN`
- Reference: `project`
- Rationale: Needs authority/context resolution

## SOURCE-026
- Candidate: Two active ADRs with no supersession metadata
- Expected decision: `ABSTAIN`
- Reference: `project`
- Rationale: Conflicting authoritative sources

## SOURCE-027
- Candidate: README older than current contract
- Expected decision: `DOWNRANK`
- Reference: `project`
- Rationale: Context only unless explicitly authoritative

## SOURCE-028
- Candidate: OWASP rule applied to a repo whose requirement is silent
- Expected decision: `POTENTIAL_RISK_ONLY`
- Reference: `SRC-012`
- Rationale: Do not promote to confirmed violation

## SOURCE-029
- Candidate: Stripe compatibility example applied to unrelated internal refactor
- Expected decision: `REJECT_ANALOGY`
- Reference: `SRC-009`
- Rationale: External analogy cannot create local issue

## SOURCE-030
- Candidate: CrowdStrike RCA used to claim MergeProof would have prevented outage
- Expected decision: `REJECT_CAUSAL_CLAIM`
- Reference: `SRC-011`
- Rationale: Incident supports pattern, not prevention counterfactual
