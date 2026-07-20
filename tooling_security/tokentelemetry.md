# TokenTelemetry Security Review

Repository: `VasiHemanth/tokentelemetry`  
Reviewed commit: `1f65c23238439fe43d649282acd55f32c19c4f5e`  
Verdict: useful local observability, but not strict-private by default.

## What It Handles

TokenTelemetry scans local AI coding-agent and autonomous-agent logs. Depending on agent and enabled features, it may read or display:

- prompts and model outputs
- reasoning traces
- tool calls
- project paths and names
- token usage and costs
- generated summaries
- optional archived full transcript blobs

This is sensitive developer telemetry. Even if it stays local, it needs the same care as shell history, IDE logs, and AI chat transcripts.

## Positive Security Signals

- The product is local-first and binds to `127.0.0.1` by default.
- Non-loopback remote access auto-generates a token unless `--insecure-no-auth` is explicitly used.
- The backend has a remote-auth middleware requiring `Authorization: Bearer <token>` or a token query parameter for remote requests when `TT_AUTH_TOKEN` is set.
- Product telemetry is strongly allowlisted in code, with tests asserting paths, prompts, project names, costs, and secrets do not appear in telemetry payloads.
- The telemetry session id is random per process launch and not persisted.
- `DO_NOT_TRACK=1` and `TT_NO_TELEMETRY=1` force product telemetry off. `TT_NO_UPDATE_CHECK=1` forces update checks off.
- Backend Python dependencies prefer a hash-pinned `requirements.lock`; frontend installs prefer `npm ci` from `package-lock.json`.

## Main Data-Safety Risks

1. Anonymous product telemetry is on by default.

The README and privacy docs state that anonymous feature-usage telemetry is default-on and opt-out. It is content-free by design, but strict privacy environments generally require opt-in or disabled-by-policy telemetry.

2. Update checks are on by default.

The dashboard fetches GitHub for latest version and release notes unless disabled. This does not send agent data, but it is still outbound network traffic.

3. The local dashboard reads sensitive agent logs.

The core value is showing prompts, traces, tool calls, costs, and project activity. Anyone who can access the dashboard or its local data directory may see sensitive context.

4. Full transcripts can be archived locally.

The history store has an opt-in compressed transcript blob tier. Compression is not encryption. Archived transcripts must be treated as sensitive local data.

5. Summaries may send sensitive briefs to a model backend.

The summarizer prompt is a structured brief rather than the full transcript, but it can still include sensitive session details. If the configured summarizer is a remote OpenAI-compatible endpoint, that brief leaves the machine.

6. Remote access can become dangerous if misused.

The launcher warns that `--insecure-no-auth` exposes the dashboard without an access token. Because the dashboard can reveal prompts and traces, this flag should not be used for real private work.

## Safe Configuration Checklist

For sensitive projects:

- Launch with `DO_NOT_TRACK=1 TT_NO_TELEMETRY=1 TT_NO_UPDATE_CHECK=1`.
- Keep the default loopback bind. Do not use `--host 0.0.0.0` unless remote access is required.
- Never use `--insecure-no-auth` with real agent logs.
- Use a strong `--auth-token` if remote access is required, and expose it only over a trusted private network or VPN.
- Use a local summarizer backend such as Ollama for sensitive traces, or disable summaries.
- Do not enable transcript archiving unless the data directory is encrypted and retention is defined.
- Protect `~/.tokentelemetry` or the configured data directory with OS permissions and disk encryption.

## Bottom Line

TokenTelemetry makes a credible effort to keep content local, but its default-on product telemetry and update check mean it is not strict-private by default. It can be acceptable for local developer observability after disabling outbound features and keeping remote access closed. It should not be used for highly sensitive agent traces unless egress, summarization, remote access, and local retention are explicitly controlled.

