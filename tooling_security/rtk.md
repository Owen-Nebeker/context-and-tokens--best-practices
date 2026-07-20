# RTK Security Review

Repository: `rtk-ai/rtk`  
Reviewed commit: `625d23a32c60e44cffeddb7ee7ffda0ee912ad4c`  
Verdict: generally safe for local developer use, but review local telemetry/tracking/tee behavior.

## What It Handles

RTK is a Rust CLI proxy that runs shell commands and filters command output before it reaches an AI assistant context. It can see:

- commands issued through supported hooks or explicit `rtk` invocations
- stdout/stderr from wrapped commands
- project paths
- local command history and token-savings metadata
- raw failed output written to tee recovery logs

It is not primarily a data platform, but it sits directly on the developer command path, so it can observe sensitive output.

## Positive Security Signals

- Telemetry is documented as disabled by default and requiring explicit consent.
- Telemetry code checks for a compiled telemetry URL, `RTK_TELEMETRY_DISABLED=1`, config consent, and enabled state before sending.
- The telemetry docs state that source code, file contents, full command lines, arguments, paths, secrets, repo names, and URLs are not collected.
- Rust `unsafe_code` is denied in `Cargo.toml`.
- Project and global custom filters are trust-gated by hash. Edited filters require re-trust, and the CI override is limited to detected CI environments.
- Permission checking attempts to defer to host allow/ask/deny rules and treats unattestable shell constructs as ask.
- Tee files rotate and are size-limited.

## Main Data-Safety Risks

1. Local tracking stores more than telemetry sends.

The SQLite schema stores `original_cmd`, `rtk_cmd`, and `project_path`. This is local, but command strings and project paths can contain sensitive names, hostnames, table names, or accidental secrets.

2. Tee recovery files can contain raw sensitive output.

RTK saves raw output for failures by default, with a recovery path. If a failing command prints secrets, env vars, database rows, cloud output, or logs, that data may be persisted locally.

3. Hooks intercept shell commands.

That is RTK's purpose, but it means install-time trust matters. A compromised binary, hook, or filter can manipulate what the AI sees or what command is run.

4. Installer convenience increases supply-chain risk.

The README advertises `curl ... | sh`. That is convenient for personal use, but production or enterprise installs should pin a release, verify checksums/signatures if available, or build from a reviewed commit.

## Safe Configuration Checklist

For sensitive projects:

- Set `RTK_TELEMETRY_DISABLED=1` unless telemetry is explicitly approved.
- Consider disabling tracking or relocating its database to an encrypted location.
- Set tee mode to `never` for projects where failed command output may include secrets.
- Run `rtk trust` only after reviewing `.rtk/filters.toml`; do not blanket-trust repo filters.
- Avoid passing secrets directly in command arguments, since local command history can capture them.
- Install from a pinned release or reviewed source commit.

## Bottom Line

RTK has the best data-safety posture of the three repos for normal developer tooling. It is not zero-risk because it intercepts commands and stores local metadata/raw output, but its outbound telemetry posture is comparatively conservative. With telemetry disabled and tee/tracking reviewed, it is reasonable for everyday private-code use.

