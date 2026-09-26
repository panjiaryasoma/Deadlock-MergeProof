# Evidence Discipline

An AI finding is a candidate claim, not a verified fact.

For every material claim keep these separate:

1. observed implementation behavior;
2. documented expected behavior;
3. test evidence;
4. engineering opinion;
5. unresolved uncertainty.

Evidence grades:
- `DIRECT`
- `CORROBORATED`
- `INFERRED`
- `INSUFFICIENT`

A `CONFIRMED_ISSUE` requires:
- DIRECT or CORROBORATED evidence;
- at least one applicable source anchor;
- at least one implementation or test anchor.

External guidance may support `POTENTIAL_RISK`.
It cannot silently become a local project requirement.
