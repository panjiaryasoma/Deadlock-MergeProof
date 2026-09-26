from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import (
    Advisory,
    EvidenceGrade,
    FindingClass,
    FindingType,
    RequirementAmbiguity,
    RequirementCriticality,
    Severity,
    SourceState,
    SourceType,
)


class MergeProofModel(BaseModel):
    """Base model preserving unknown input fields until validator policy evaluates them."""

    model_config = ConfigDict(extra="allow")


class Anchor(MergeProofModel):
    artifact: str
    locator: str
    excerpt: str | None = None
    commit_sha: str | None = None


class Source(MergeProofModel):
    source_id: str
    source_type: SourceType
    location: str
    authority: str
    state: SourceState
    scope: list[str]
    version: str | None = None
    effective_at: str | None = None
    supersedes: list[str] | None = None
    content_hash: str | None = None


class Requirement(MergeProofModel):
    requirement_id: str
    source_id: str
    statement: str
    scope: list[str]
    criticality: RequirementCriticality
    ambiguity: RequirementAmbiguity = RequirementAmbiguity.NONE


class Finding(MergeProofModel):
    finding_id: str
    finding_class: FindingClass
    finding_type: FindingType
    title: str
    evidence_grade: EvidenceGrade
    severity: Severity
    repo_anchors: list[Anchor]
    rationale: str
    requirement_ids: list[str] = Field(default_factory=list)
    source_anchors: list[Anchor] = Field(default_factory=list)
    test_anchors: list[Anchor] = Field(default_factory=list)
    suggested_human_check: str | None = None


class Repository(MergeProofModel):
    commit_sha: str
    changed_files: list[str]


class HumanOverride(MergeProofModel):
    """Optional human-override object.

    The frozen schema declares this as an object/null without freezing nested keys yet.
    Unknown nested data is therefore preserved rather than silently discarded.
    """


class MergeProofReport(MergeProofModel):
    report_version: str
    run_id: str
    advisory: Advisory
    repository: Repository
    sources: list[Source]
    findings: list[Finding]
    generated_at: str
    requirements: list[Requirement] = Field(default_factory=list)
    human_override: HumanOverride | None = None


# Compatibility aliases for downstream pre-Block-2 code.
# They do not alter the canonical wire field names above.
EvidenceAnchor = Anchor
SourceRecord = Source
