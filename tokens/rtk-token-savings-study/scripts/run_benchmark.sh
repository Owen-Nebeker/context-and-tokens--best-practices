#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${ROOT_DIR}/benchmark-output/$(date +%Y%m%d-%H%M%S)"
mkdir -p "${OUT_DIR}"

COMMAND_FILE="${1:-${ROOT_DIR}/benchmark_commands.txt}"

if [[ ! -f "${COMMAND_FILE}" ]]; then
  cat > "${COMMAND_FILE}" <<'COMMANDS'
git status
git diff
git log -n 20
rg "TODO" .
COMMANDS
  echo "Created ${COMMAND_FILE}. Review it, then rerun this script."
  exit 0
fi

if ! command -v rtk >/dev/null 2>&1; then
  echo "rtk is not installed or not on PATH. Raw outputs will be captured only."
fi

echo "output_dir=${OUT_DIR}"
while IFS= read -r command_line || [[ -n "${command_line}" ]]; do
  [[ -z "${command_line}" || "${command_line}" =~ ^# ]] && continue
  safe_name="$(echo "${command_line}" | tr -cs 'A-Za-z0-9_' '_' | sed 's/^_//;s/_$//')"

  raw_file="${OUT_DIR}/${safe_name}.raw.txt"
  rtk_file="${OUT_DIR}/${safe_name}.rtk.txt"

  echo "raw: ${command_line}"
  set +e
  bash -lc "${command_line}" >"${raw_file}" 2>&1
  raw_exit=$?
  set -e
  echo "${raw_exit}" >"${raw_file}.exit"

  if command -v rtk >/dev/null 2>&1; then
    echo "rtk: rtk ${command_line}"
    set +e
    bash -lc "rtk ${command_line}" >"${rtk_file}" 2>&1
    rtk_exit=$?
    set -e
    echo "${rtk_exit}" >"${rtk_file}.exit"
  fi
done < "${COMMAND_FILE}"

echo "Benchmark capture complete. Use scripts/estimate_tokens.py on files in ${OUT_DIR}."
