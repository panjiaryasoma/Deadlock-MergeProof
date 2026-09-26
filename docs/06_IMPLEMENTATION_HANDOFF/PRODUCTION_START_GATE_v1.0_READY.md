# Production Start Gate v1.0

Status: **READY**

## First commandment, because apparently we need one
Do not build the dashboard first.

## Block 1 acceptance
Production officially starts only after:
- project opens in Bob;
- `.bob/custom_modes.yaml` is detected;
- `mergeproof` mode appears;
- skill is loadable;
- mode remains read-only against application code.

After this smoke test, freeze Bob configuration v0.1 and continue to report validation.
