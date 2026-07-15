# RTK Savings Study Protocol

## Objective

Measure whether RTK materially reduces command-output tokens in AI coding workflows without hiding information developers need to complete work safely.

## Primary Metrics

| Metric | Formula |
| --- | --- |
| Tokens saved | `raw_tokens - rtk_tokens` |
| Savings rate | `(raw_tokens - rtk_tokens) / raw_tokens` |
| Pilot dollar savings | `tokens_saved / 1,000,000 * blended_price_per_1m_tokens` |
| Monthly projection | `pilot_dollar_savings / active_days * 22` |
| Adoption | `rtk_optimized_commands / total_candidate_commands` |
| Missed opportunity | Candidate raw commands not routed through RTK |

## Phase 1: Pre-RTK Baseline

Duration: 3 to 5 workdays.

1. Keep RTK hooks disabled.
2. Record normal AI coding command output in `data/baseline_commands.csv`.
3. Include git, search, test, build, logs, container, and package-manager commands.
4. Use provider billing data when available; otherwise estimate tokens as characters divided by 4.
5. Note whether the command output was actually useful to the AI task.

## Phase 2: Controlled Benchmark

Duration: 1 session per repo.

1. Install RTK, but keep the command list fixed.
2. Review `benchmark_commands.txt` and remove unsafe commands.
3. Run:

```bash
cd tokens/rtk-token-savings-study
scripts/run_benchmark.sh
```

4. Estimate output tokens:

```bash
scripts/estimate_tokens.py benchmark-output/*/*.txt
```

5. Enter raw and RTK measurements in `data/rtk_commands.csv`.

## Phase 3: Pilot

Duration: 5 to 10 workdays.

1. Initialize RTK for the agent under test. For Codex:

```bash
rtk init -g --codex
```

2. Restart the AI coding tool.
3. Work normally.
4. Export RTK analytics daily:

```bash
rtk gain --daily
rtk gain --history
rtk discover --all --since 7
rtk gain --all --format json > data/rtk_gain_export.json
```

## Phase 4: Dashboard Review

1. Open `dashboard/index.html`.
2. Upload the baseline CSV, RTK benchmark CSV, RTK gain JSON, and pricing assumptions.
3. Replace sample model pricing with approved internal rates.
4. Review whether savings are consistent by command family.
5. Review missed opportunities and workflow notes before recommending rollout.

## Quality Guardrails

- Preserve raw output for failed or ambiguous commands.
- Track reruns caused by missing detail.
- Do not count sample data in final results.
- Do not rely on advertised savings alone.
- Separate token reduction from business value; convert to dollars only after pricing is approved.

