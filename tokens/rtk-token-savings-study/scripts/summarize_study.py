#!/usr/bin/env python3
"""Summarize RTK savings study files for quick CLI validation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def number(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "") or 0)
    except ValueError:
        return 0.0


def load_pricing(path: Path) -> tuple[str, float]:
    rows = read_csv_rows(path)
    if not rows:
        return "no-pricing", 0.0
    preferred = rows[1] if len(rows) > 1 else rows[0]
    return preferred.get("model", "pricing"), number(preferred, "blended_usd_per_1m_tokens")


def summarize(args: argparse.Namespace) -> dict[str, object]:
    baseline = read_csv_rows(args.baseline)
    rtk = read_csv_rows(args.rtk)
    model, price = load_pricing(args.pricing)

    baseline_tokens = sum(number(row, "estimated_tokens") for row in baseline)
    raw_tokens = sum(number(row, "raw_estimated_tokens") for row in rtk)
    rtk_tokens = sum(number(row, "rtk_estimated_tokens") for row in rtk)

    if args.gain_export.exists():
        gain = json.loads(args.gain_export.read_text(encoding="utf-8"))
    else:
        gain = {}

    tokens_saved = max(raw_tokens - rtk_tokens, 0)
    savings_pct = (tokens_saved / raw_tokens * 100) if raw_tokens else 0
    estimated_usd_saved = tokens_saved / 1_000_000 * price

    return {
        "baseline_rows": len(baseline),
        "baseline_estimated_tokens": round(baseline_tokens),
        "benchmark_rows": len(rtk),
        "benchmark_raw_tokens": round(raw_tokens),
        "benchmark_rtk_tokens": round(rtk_tokens),
        "benchmark_tokens_saved": round(tokens_saved),
        "benchmark_savings_pct": round(savings_pct, 1),
        "pricing_model": model,
        "price_per_1m_tokens": price,
        "benchmark_estimated_usd_saved": round(estimated_usd_saved, 2),
        "rtk_gain_summary_available": bool(gain.get("summary")),
        "rtk_gain_summary": gain.get("summary", {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize RTK savings study files.")
    parser.add_argument("--baseline", type=Path, default=Path("data/baseline_commands.csv"))
    parser.add_argument("--rtk", type=Path, default=Path("data/rtk_commands.csv"))
    parser.add_argument("--gain-export", type=Path, default=Path("data/rtk_gain_export.json"))
    parser.add_argument("--pricing", type=Path, default=Path("data/model_pricing.csv"))
    args = parser.parse_args()

    print(json.dumps(summarize(args), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
