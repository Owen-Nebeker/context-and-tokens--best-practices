#!/usr/bin/env python3
"""Estimate token counts for files, stdin, or study CSV rows.

The default heuristic is four characters per token. Use provider billing exports
when available; this utility is for repeatable baseline estimates.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def estimate_tokens(char_count: int, chars_per_token: float) -> int:
    return round(char_count / chars_per_token)


def estimate_text(text: str, chars_per_token: float) -> tuple[int, int]:
    chars = len(text)
    return chars, estimate_tokens(chars, chars_per_token)


def update_csv(path: Path, output: Path | None, chars_per_token: float) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    if "estimated_tokens" not in fieldnames:
        fieldnames.append("estimated_tokens")

    for row in rows:
        raw_chars = row.get("raw_output_chars") or row.get("output_chars") or "0"
        try:
            char_count = int(float(raw_chars))
        except ValueError:
            char_count = 0
        row["estimated_tokens"] = str(estimate_tokens(char_count, chars_per_token))

    target = output or path
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate token counts for the RTK savings study.")
    parser.add_argument("inputs", nargs="*", help="Files to estimate. Reads stdin when omitted.")
    parser.add_argument("--chars-per-token", type=float, default=4.0, help="Default: 4.0")
    parser.add_argument("--csv", action="store_true", help="Update estimated_tokens in a study CSV.")
    parser.add_argument("--output", type=Path, help="Output path for --csv mode. Defaults to in-place.")
    args = parser.parse_args()

    if args.csv:
        if len(args.inputs) != 1:
            parser.error("--csv expects exactly one CSV input path")
        update_csv(Path(args.inputs[0]), args.output, args.chars_per_token)
        return 0

    if not args.inputs:
        text = sys.stdin.read()
        chars, tokens = estimate_text(text, args.chars_per_token)
        print(f"chars={chars} estimated_tokens={tokens}")
        return 0

    for item in args.inputs:
        path = Path(item)
        text = path.read_text(encoding="utf-8", errors="replace")
        chars, tokens = estimate_text(text, args.chars_per_token)
        print(f"{path}: chars={chars} estimated_tokens={tokens}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
