# RTK Token Savings Study

This folder is a practical research kit for measuring whether RTK reduces AI coding token usage enough to justify rollout to senior leadership.

RTK should be evaluated with two sources of evidence:

- A pre-install baseline that measures normal command output before RTK hooks are enabled.
- RTK analytics from `rtk gain` after the pilot starts.

The dashboard in `dashboard/index.html` includes sample data so the executive view is visible immediately. Replace the sample files with real exports before presenting results.

## Study Design

### 1. Baseline Before RTK

Run representative AI-coding commands without RTK hooks enabled. Capture command, task type, output character count, estimated tokens, duration, and quality notes in `data/baseline_commands.csv`.

Recommended command families:

- `git status`, `git diff`, `git log`
- `rg`, `grep`, `find`, `cat`
- `npm test`, `pytest`, `cargo test`, `go test`
- `docker ps`, `docker logs`, build logs, lint output

Use this estimate unless provider-specific tokenizer data is available:

```text
estimated_tokens = output_characters / 4
```

### 2. Controlled Raw vs RTK Benchmark

After RTK is installed, run the same command list in raw and RTK form:

```bash
git status
rtk git status

git diff
rtk git diff

rg "TODO" .
rtk grep "TODO" .
```

Track results in `data/rtk_commands.csv`.

### 3. Pilot RTK Usage

Install and initialize RTK for the AI tool being tested. For Codex:

```bash
rtk init -g --codex
```

During the pilot, capture:

```bash
rtk gain
rtk gain --daily
rtk gain --history
rtk discover --all --since 7
rtk gain --all --format json > tokens/rtk-token-savings-study/data/rtk_gain_export.json
```

### 4. Dashboard

Open:

```text
tokens/rtk-token-savings-study/dashboard/index.html
```

Use the file upload controls to load:

- `data/baseline_commands.csv`
- `data/rtk_commands.csv`
- `data/rtk_gain_export.json`
- `data/model_pricing.csv`

The dashboard is intentionally static and offline-friendly, so it can be reviewed without a server.

## Executive Narrative

Use this framing:

```text
We measured normal AI coding command output before RTK, introduced RTK in a pilot, and compared raw command-output tokens against RTK-filtered tokens.

RTK reduced command-output tokens by X%, saving Y tokens over Z days. At current model pricing, that projects to approximately $A monthly and $B annually across N developers.

The largest savings came from tests, git diffs, search results, and logs. Workflow risk was low when raw output remained available for failed commands or audit needs.
```

## Decision Criteria

Recommend rollout when:

- Observed token savings exceed the internal threshold, for example 40% or more.
- Developers report no material loss of diagnostic detail.
- Raw-output fallback is available for failed or ambiguous commands.
- Savings are not isolated to a single unusual repo or task.
- Privacy and telemetry settings match company policy.

## Files

| Path | Purpose |
| --- | --- |
| `data/baseline_commands.csv` | Pre-RTK baseline template and sample rows |
| `data/rtk_commands.csv` | Raw vs RTK benchmark template and sample rows |
| `data/sample_rtk_gain_export.json` | Sample RTK-style dashboard data |
| `data/model_pricing.csv` | Pricing assumptions for savings estimates |
| `scripts/estimate_tokens.py` | Token estimation utility |
| `scripts/run_benchmark.sh` | Controlled command benchmark helper |
| `scripts/summarize_study.py` | CLI summary for baseline, RTK, and pricing files |
| `dashboard/index.html` | Static executive dashboard |

