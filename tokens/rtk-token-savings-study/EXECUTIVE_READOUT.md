# Executive Readout Template

## Recommendation

Adopt RTK for a broader coding-agent pilot if observed savings exceed the internal threshold and developers report no material loss of diagnostic detail.

## Headline

RTK reduced command-output tokens by `X%` in the pilot, saving `Y` tokens across `Z` active days. At approved blended model pricing, this projects to approximately `$A` per month and `$B` per year for `N` developers.

## Evidence

| Evidence Area | Result |
| --- | --- |
| Pre-RTK baseline | `baseline_tokens` command-output tokens measured |
| Controlled benchmark | `raw_tokens` raw vs `rtk_tokens` RTK-filtered tokens |
| RTK analytics | `rtk gain` export showed `tokens_saved` tokens saved |
| Biggest savings categories | Tests, git diffs, search output, logs |
| Missed opportunities | Commands from `rtk discover` or manual raw-command review |
| Workflow impact | Developer notes and rerun rate |

## Business Impact

| Scenario | Assumption | Monthly Savings | Annual Savings |
| --- | --- | ---: | ---: |
| Conservative | 40% savings | `$` | `$` |
| Observed | Pilot result | `$` | `$` |
| Aggressive | 80% savings | `$` | `$` |

## Risks And Controls

| Risk | Control |
| --- | --- |
| Useful detail hidden by filtering | Keep raw-output fallback for failed commands |
| Savings overstated by sample workload | Use multiple repos and task types |
| Pricing assumptions wrong | Use approved internal pricing table |
| Tool adoption incomplete | Track `rtk discover` and shell-command coverage |
| Privacy or telemetry concerns | Confirm RTK telemetry setting before rollout |

## Decision Ask

Approve a team-level RTK rollout for `N` developers over `M` weeks, with dashboard reporting on token savings, adoption, missed opportunities, and developer workflow impact.

