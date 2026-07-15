# Token Tooling

## Purpose

This note tracks tools and tool ideas that reduce token usage before, during, or after model calls. The focus is practical: what can help teams spend fewer tokens for the same work, what risks to watch, and what should be tested before adoption.

Initial scope:

- [juliusbrussee/caveman](https://github.com/JuliusBrussee/caveman)
- RTK / Rust-based harness ideas for token budgets and command wrappers

## Short Recommendation

Caveman is worth testing as an output-token reduction tool, especially for verbose coding agents and long explanatory replies. It should not be treated as a general token optimizer because it mainly shortens what the agent says. It does not reduce input tokens, files, tool output, or reasoning tokens by default.

For company-wide savings, the higher-leverage tooling idea is a deterministic harness that sits between tools and LLMs:

1. Capture raw CLI output.
2. Preserve exact error lines, exit codes, commands, file paths, and machine-readable artifacts.
3. Drop noise, progress bars, repeated logs, and low-value output.
4. Emit a compact summary plus an optional raw-output pointer.
5. Track token estimates and enforce budgets.

Caveman can inspire the style layer. A Rust-based harness should handle the safety, measurement, and compression layer.

## Tool Evaluation: Caveman

### What It Is

Caveman is a skill/plugin for AI coding agents including Claude Code, Codex, Gemini, Cursor, Windsurf, Cline, Copilot, and others. It tells agents to write shorter replies while preserving code, commands, paths, URLs, and errors exactly.

The repo positions Caveman as a way to make agents "talk like a caveman": fewer filler words, shorter explanations, same technical content.

### What It Claims

From the Caveman README:

- Average 65% output-token reduction across 10 benchmark prompts.
- Output-token savings range from 22% to 87% in those benchmarks.
- `/caveman-compress <file>` claims about 46% average input-token reduction on memory files such as `CLAUDE.md`.
- `caveman-shrink` is described as MCP middleware that compresses tool descriptions.
- `/caveman-stats` estimates real session token usage, lifetime savings, and USD savings.

From `docs/HONEST-NUMBERS.md`, the repo also gives important caveats:

- Caveman mostly reduces output tokens.
- It does not compress normal input tokens, files, or reasoning tokens.
- The skill itself can add about 1k to 1.5k input tokens per turn.
- Short already-terse replies can be net-negative.
- Per-request pricing systems may not get cheaper just because the answer is shorter.
- The only reliable proof is an A/B test against provider usage or billing.

### Where Caveman Fits

Caveman is strongest for:

- Long explanations.
- Architecture discussions.
- Code review comments.
- Debugging walkthroughs.
- Documentation drafts.
- Agents that tend to produce friendly filler before useful content.

Caveman is weaker for:

- Short coding Q&A.
- Workflows where output is already concise.
- Agents or products billed by request instead of tokens.
- Tasks where the extra skill prompt is larger than the saved output.
- Cases where the user needs polished prose, teaching, stakeholder communication, or audit-ready explanation.

### Company Adoption View

Adopt Caveman only as an optional mode until internal testing proves savings.

Recommended rollout:

1. Test on 20 to 50 representative coding-agent tasks.
2. Run each task with and without Caveman.
3. Compare total tokens, not only output tokens.
4. Compare quality, task completion, retries, and wall-clock time.
5. Disable it for short-answer workflows if the added prompt overhead costs more than the output savings.

Default policy:

- Use Caveman-style brevity for internal coding-agent replies.
- Do not use it for customer-facing or executive writing unless tone is reviewed.
- Do not count advertised output savings as actual cost savings without A/B data.

## RTK / Rust-Based Harness Ideas

This section now tracks both the public [rtk-ai/rtk](https://github.com/rtk-ai/rtk) project and the broader internal harness pattern it represents. RTK is a CLI proxy that filters command output before it reaches the LLM context and includes local savings analytics through commands such as `rtk gain`, `rtk gain --daily`, and `rtk gain --all --format json`.

For a company-facing evaluation kit, see [RTK Token Savings Study](../rtk-token-savings-study/README.md).

The useful idea is not only the tool name; it is the architecture.

### Why Rust

Rust is a good fit for token-control tooling because it can provide:

- Fast streaming over large CLI output.
- Safe handling of stdout, stderr, exit codes, and files.
- Deterministic rules for truncation and filtering.
- Strong tests around budget enforcement.
- Low overhead as a local CLI wrapper.
- Type-level patterns for budget ownership and spend limits.

The June 2026 paper [Token Budgets](https://arxiv.org/abs/2606.04056) supports the broader idea that budget enforcement should be hard to bypass. It describes a Rust crate that uses ownership patterns so budget delegation and double-spend mistakes become compile-time problems instead of operator discipline problems.

### Harness Goals

A useful Rust-based token harness should:

- Run commands and capture stdout/stderr separately.
- Preserve command, exit code, duration, and working directory.
- Detect common failure patterns.
- Collapse repeated lines.
- Strip progress bars, ANSI noise, spinners, and unhelpful banners.
- Keep first and last lines when middle output is repetitive.
- Preserve exact compiler errors, stack traces, failing test names, and file paths.
- Estimate model-specific token counts.
- Emit both compact output and a raw-output artifact path.
- Enforce maximum token budgets before output is sent to an LLM.

### Proposed Commands

```bash
tokentool run -- npm test
tokentool run -- pytest
tokentool compact build.log
tokentool budget --max-input-tokens 4000 build.log
tokentool explain-savings before.txt after.txt
```

### Output Contract

The harness should produce a compact, structured block:

```text
command: npm test
exit_code: 1
duration_ms: 18233
raw_output: .token-artifacts/npm-test-2026-07-08.log
token_estimate_raw: 18420
token_estimate_compact: 1320

summary:
- 1 test suite failed.
- Failure: src/auth/session.test.ts
- Main error: expected token to expire at boundary, received active session.

key_output:
src/auth/session.test.ts:42
Expected: expired
Received: active
```

This gives the model enough information to act while keeping the full output available when needed.

### Compression Rules

Good compression rules:

- Keep exact error messages.
- Keep exact file paths and line numbers.
- Keep exact commands and exit codes.
- Keep the first occurrence of repeated warnings.
- Collapse repeated stack frames.
- Drop progress bars, download logs, timestamps, and repeated success lines.
- Replace long passing-test lists with counts.
- Replace large JSON blobs with selected keys unless the full JSON is needed.
- Redact secrets before storage or model submission.

Bad compression rules:

- Rewriting error text in a way that changes meaning.
- Dropping line numbers.
- Dropping exit codes.
- Summarizing without raw output access.
- Using an LLM to compress logs before deterministic filtering has removed obvious noise.

### Suggested Pipeline

```text
CLI command
  -> raw capture
  -> secret scan
  -> deterministic cleanup
  -> failure/error extractor
  -> token estimator
  -> compact model payload
  -> raw artifact link for fallback
```

## Evaluation Matrix

| Tool or Idea | Saves Input Tokens | Saves Output Tokens | Best Fit | Main Risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Caveman skill | Limited; mainly `/caveman-compress` for memory files | Yes, especially long replies | Verbose coding-agent replies | Added prompt overhead can exceed savings | Test as optional mode |
| Caveman-shrink MCP middleware | Potentially, by shortening tool descriptions | No direct output effect | Large MCP tool catalogs | Tool descriptions may lose clarity | Test only with evals |
| Rust token harness | Yes | Indirectly | CLI output, logs, agent tool output | Bad filters may hide critical details | Highest priority prototype |
| Token budget enforcement | Yes, by stopping overspend | Indirectly | Agents, retries, multi-agent tasks | Overly strict budgets may block valid work | Add as guardrail |
| Foundry-style CLI compression | Yes | Indirectly | Test logs, build output, command output | Lossy summaries may mislead models | Use deterministic rules first |

## Source Notes

| Source | Notes |
| --- | --- |
| [juliusbrussee/caveman](https://github.com/JuliusBrussee/caveman) | Skill/plugin that shortens agent replies; claims 65% average output-token reduction in benchmarks, with support for many coding agents. |
| [Caveman Honest Numbers](https://raw.githubusercontent.com/JuliusBrussee/caveman/main/docs/HONEST-NUMBERS.md) | Important caveats: output-only by default, adds about 1k to 1.5k input tokens per turn, can be net-negative on short replies, A/B billing data is the real proof. |
| [Token Budgets](https://arxiv.org/abs/2606.04056) | Rust-based budget-enforcement paper; useful support for making token budgets harder to bypass in agentic systems. |

## Add More Tooling Here

| Tool | Category | What It Saves | Status | Decision |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
