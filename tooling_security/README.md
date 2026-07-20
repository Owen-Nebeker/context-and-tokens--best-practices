# Tooling Security Review

High-level data-safety review for three GitHub repositories:

- `Vexa-ai/vexa` at commit `bf13dc54a968989eb1764dc229e917dfd2145c7f`
- `rtk-ai/rtk` at commit `625d23a32c60e44cffeddb7ee7ffda0ee912ad4c`
- `VasiHemanth/tokentelemetry` at commit `1f65c23238439fe43d649282acd55f32c19c4f5e`

Review date: 2026-07-20.

## Short Answer

None of these should be treated as "super safe" for sensitive data without configuration and operational controls.

Best fit by data-safety posture:

| Repo | Data-safety verdict | Main reason |
| --- | --- | --- |
| `rtk-ai/rtk` | Safest of the three for normal local developer use, with telemetry/tracking/tee settings reviewed. | It is a local CLI proxy, telemetry is documented as opt-in, and project filters are trust-gated. |
| `VasiHemanth/tokentelemetry` | Reasonable for local-only observability, but not strict-private by default. | It reads AI agent logs/prompts locally and has default-on outbound product telemetry and update checks. |
| `Vexa-ai/vexa` | High-value but high-sensitivity system; only safe after production hardening. | It handles meeting audio, recordings, transcripts, workspaces, model credentials, and bot/agent containers. |

## Recommended Use Decision

| Scenario | Vexa | RTK | TokenTelemetry |
| --- | --- | --- | --- |
| Personal/local experimentation | OK with throwaway data | OK | OK |
| Private source-code work | Use only if self-hosted and hardened | OK with tee/tracking reviewed | OK only if local-only and egress disabled |
| Confidential company meetings | Do not use defaults; harden first | Not applicable | Avoid storing full traces unless policy allows |
| Regulated or highly sensitive data | Needs formal security review | Likely acceptable after local config review | Needs egress lock-down, remote access disabled, and local summarizer only |

## Minimum Safe Baseline

For all three:

- Pin a reviewed commit or release. Do not install from an unpinned `curl | sh` command in production.
- Run from a dedicated user account or sandbox where possible.
- Block outbound network traffic unless a specific endpoint is required and approved.
- Confirm local data retention and deletion behavior before feeding real secrets, prompts, meetings, or customer data.
- Run dependency and container vulnerability scans before production use. This review did not include a full CVE audit.

## Report Files

- [Vexa security notes](./vexa.md)
- [RTK security notes](./rtk.md)
- [TokenTelemetry security notes](./tokentelemetry.md)

