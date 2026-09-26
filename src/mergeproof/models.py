from __future__ import annotations

from pydantic import BaseModel, Field

from .enums import Advisory, EvidenceGrade, FindingClass, SourceAuthority, SourceState


class EvidenceAnchor(BaseModel):
    artifact: str
    locator: str
    excerpt: str | None = None


class SourceRecord(BaseModel):
    source_id: str
    path: str
    state: SourceState
    authority: SourceAuthority
    supersedes: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    finding_id: str
    finding_class: FindingClass
    evidence_grade: EvidenceGrade
    severity: str = "UNSPECIFIED_BY_PROJECT"
    source_evidence: list[EvidenceAnchor] = Field(default_factory=list)
    repository_evidence: list[EvidenceAnchor] = Field(default_factory=list)
    impact: str = ""
    human_check_required: str = ""


class Scope(BaseModel):
    changed_files: list[str] = Field(default_factory=list)
    notes: str = ""


class MergeProofReport(BaseModel):
    report_version: str
    run_id: str
    advisory: Advisory
    scope: Scope
    sources: list[SourceRecord] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
