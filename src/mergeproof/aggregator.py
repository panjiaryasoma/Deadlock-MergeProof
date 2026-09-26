from .enums import Advisory, FindingClass, SourceAuthority, SourceState
from .models import Finding, SourceRecord


def aggregate_advisory(
    findings: list[Finding],
    sources: list[SourceRecord],
    *,
    has_material_unresolved_question: bool = False,
) -> Advisory:
    if has_material_unresolved_question:
        return Advisory.ABSTAIN

    if any(
        source.state is SourceState.CONFLICTING
        or source.authority is SourceAuthority.UNRESOLVED
        for source in sources
    ):
        return Advisory.ABSTAIN

    if any(f.finding_class is FindingClass.SPEC_AMBIGUITY for f in findings):
        return Advisory.ABSTAIN

    if any(
        f.finding_class in {FindingClass.CONFIRMED_ISSUE, FindingClass.POTENTIAL_RISK}
        for f in findings
    ):
        return Advisory.REVIEW_REQUIRED

    return Advisory.PASS
