from .enums import Advisory, FindingClass, SourceState
from .models import Finding, Source


def aggregate_advisory(
    findings: list[Finding],
    sources: list[Source],
    *,
    has_material_unresolved_question: bool = False,
) -> Advisory:
    if has_material_unresolved_question:
        return Advisory.ABSTAIN

    if any(source.state is SourceState.CONFLICTING for source in sources):
        return Advisory.ABSTAIN

    if any(finding.finding_class is FindingClass.SPEC_AMBIGUITY for finding in findings):
        return Advisory.ABSTAIN

    if any(
        finding.finding_class in {FindingClass.CONFIRMED_ISSUE, FindingClass.POTENTIAL_RISK}
        for finding in findings
    ):
        return Advisory.REVIEW_REQUIRED

    return Advisory.PASS
