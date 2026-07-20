# Vexa Security Review

Repository: `Vexa-ai/vexa`  
Reviewed commit: `bf13dc54a968989eb1764dc229e917dfd2145c7f`  
Verdict: not super safe out of the box; potentially safe only after hardening.

## What It Handles

Vexa is a self-hosted meeting bot, transcription API, and agent/workspace platform. It can process:

- meeting audio and recordings
- live and historical transcripts
- speaker attribution
- generated meeting notes and workspace Markdown
- LLM and STT provider credentials
- authenticated browser/userdata for bots
- workspace/git credentials for agents

This is highly sensitive data. Treat the stack like production collaboration infrastructure, not like a small CLI utility.

## Positive Security Signals

- The project has an explicit `SECURITY.md` with private vulnerability reporting and an OpenSSF/OSPS baseline claim.
- The docs describe a self-hosted and air-gapped model: with self-hosted transcription and owned LLM endpoints, "no request leaves your network" (`docs/docs/security-compliance.mdx`).
- The gateway is intended to derive identity from API keys server-side, rather than trusting client-provided identity fields.
- Docker Compose binds several infrastructure/admin ports to `127.0.0.1`, reducing accidental LAN exposure in local deployments.
- The Helm chart has stronger production-oriented defaults than Compose, including gateway/admin guard settings and pod hardening defaults.
- The codebase contains tests and comments around previous cross-tenant transcript leak fixes, webhook SSRF, Redis client hardening, and ownership checks.

## Main Data-Safety Risks

1. At-rest encryption is not shipped.

The security docs explicitly state that at-rest encryption for workspaces, transcripts, and tokens is planned, not shipped. Operators must bring disk or volume encryption. For confidential meetings, this is a major gap.

2. Compose defaults are development secrets.

`deploy/compose/.env.example` includes default `postgres`, MinIO, admin, internal API, dispatch signing, and NextAuth secrets, with a comment saying to change them for non-local use. Any non-local deployment using these defaults is unsafe.

3. Runtime can mount the host Docker socket.

The Compose runtime mounts `/var/run/docker.sock`. A compromised runtime component or worker-spawn path can become host-level risk because Docker socket access is effectively administrative on many hosts.

4. External STT and LLM endpoints can receive sensitive data.

The docs support air-gapped operation, but the normal configuration can point at hosted transcription and model providers. Meeting audio/transcripts and agent prompts may leave the environment unless endpoints are self-hosted or explicitly approved.

5. Kubernetes model credentials may be exposed via pod/spec access.

The Helm values warn that spec-env values are readable from spawned worker pods and chart-managed Secrets. This is workable, but only if RBAC tightly limits pod and secret reads.

6. Some credentials are stored plaintext by design.

The agent control-plane git credential helper documents plaintext-at-rest storage with `0600` permissions and no envelope encryption. That is not suitable for high-value credentials unless the host/volume layer is encrypted and access-controlled.

## Safe Configuration Checklist

Use this only for sensitive data if all of these are true:

- Replace every Compose/dev secret before use.
- Prefer Kubernetes with external secret management over local Compose for shared/team use.
- Use self-hosted STT and LLM endpoints, or approve vendor endpoints through a data-processing review.
- Enable disk/volume encryption for Postgres, MinIO, Redis persistence, workspaces, and any credential paths.
- Do not expose admin, MinIO, Postgres, Redis, runtime, or agent APIs directly to the network.
- Avoid Docker socket mode for production if a safer Kubernetes backend is available.
- Scope Kubernetes RBAC so users cannot read worker pod specs, logs, or Secrets unless operationally required.
- Configure retention and deletion for recordings, transcripts, and generated workspaces.
- Verify webhook SSRF controls, tenant isolation tests, and auth checks in CI before upgrades.

## Bottom Line

Vexa is security-conscious in design language and has useful audit artifacts, but the data it handles is extremely sensitive and several protections are operator-owned rather than built in. It is not "super safe" by default. It can be made reasonably safe for internal use only with disciplined self-hosting, secret management, egress controls, encryption, and access controls.

