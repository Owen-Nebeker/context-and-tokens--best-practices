# Token Efficiency Research

## Purpose

This document is a practical guide to saving money by using fewer tokens for the same work without lowering quality. It is organized around basic skills people can use in daily AI work, then broken out by Codex, Claude, and other models.

Use this as a living company guide. Add new examples, experiments, and decisions in the editable sections at the bottom.

## Core Rule

Do not optimize for the fewest tokens. Optimize for the lowest cost that still produces the required result.

That means teams should spend tokens on reasoning, grounding, and verification when those tokens improve outcomes. They should remove repeated instructions, unnecessary files, verbose logs, long outputs, excessive retries, and premium models when those things do not improve the task.

## Basic Token-Saving Skills

### 1. Measure Token Use First

Before changing prompts or models, measure where tokens are going.

- Track input tokens, output tokens, cached tokens, model, latency, retries, tool calls, and final task result.
- Compare cost per successful task, not only cost per request.
- Find the workflows with the most repeated input, longest outputs, highest retry rates, or most expensive model choices.
- Review high-spend workflows on a regular schedule.

Skill to teach: ask "Which tokens changed the outcome?" Anything else is a savings candidate.

### 2. Reuse Stable Prompt Parts

Many AI workflows repeat the same instructions, examples, schemas, policies, and tool descriptions. Repeated input is one of the easiest places to save money.

- Put stable instructions, examples, schemas, and tool definitions first.
- Put user-specific request data last.
- Avoid timestamps, request IDs, random wording, or changing examples inside the stable prefix.
- Use provider-specific prompt caching when available.
- Turn repeated high-volume prompts into standard templates.

Skill to teach: separate "same every time" from "new this time."

### 3. Keep Prompts Short And Specific

Shorter prompts are cheaper and often easier for models to follow.

- Give the task, constraints, and desired output format directly.
- Remove duplicate rules and stale examples.
- Do not paste broad documents when a short excerpt, file path, row ID, or field list will do.
- Prefer structured inputs for machine-to-machine tasks.
- Ask for the minimum useful answer.

Skill to teach: include what the model needs, not everything the human knows.

### 4. Control Output Length

Output tokens cost money too. Long answers, full-file rewrites, and verbose explanations add up quickly.

- Ask for concise answers by default.
- Use tables, JSON, bullets, or short sections when the output will be consumed by software or operators.
- Ask for diffs, patches, or changed sections instead of whole-file rewrites when safe.
- Use predicted outputs or similar features when most of the answer is already known.
- Only request detailed reasoning or explanations when they are needed for review, audit, or learning.

Skill to teach: define the output size before the model starts writing.

### 5. Route Work To The Right Model

One model should not handle every task. Simple tasks should usually use cheaper models, while hard tasks can escalate.

- Use smaller or cheaper models for classification, extraction, formatting, simple rewriting, and routine summaries.
- Use stronger models for ambiguous reasoning, planning, coding, regulated decisions, and high-impact user-facing work.
- Tune reasoning effort where available instead of always using the highest setting.
- Use evals to prove that cheaper routes still meet quality requirements.

Skill to teach: start with the cheapest model that passes the eval.

### 6. Limit Agent Loops

Agentic workflows can burn tokens through repeated tool calls, retries, file reads, and verbose logs.

- Set tool-call budgets by task type.
- Set retry limits.
- Summarize or filter long tool outputs before sending them back to a model.
- Ask agents to inspect targeted files or records instead of broad folders, logs, or datasets.
- Stop when progress stalls.
- Require approval before long-running or expensive agent runs.

Skill to teach: agents need budgets and stop conditions.

### 7. Use Cheaper Processing Modes

Some cost reductions do not reduce token count, but they reduce spend.

- Use batch processing for large offline jobs.
- Use lower-priority or flex processing when latency does not matter.
- Keep interactive paths fast, but move background enrichment, evaluations, and maintenance to cheaper modes.

Skill to teach: urgent and non-urgent AI work should not be priced the same way.

### 8. Test Quality Before Shipping Savings

Token savings are only useful if quality holds.

- Keep workflow-specific eval examples.
- Compare baseline versus optimized prompts, models, and output formats.
- Track cost, latency, accuracy, completeness, and failure modes.
- Watch for regressions after changing prompts, models, tools, or cacheable templates.

Skill to teach: every savings change needs a quality check.

## Codex Playbook

Use these habits when asking Codex to work in a repo or perform coding-agent tasks.

### Save Tokens In Codex Prompts

- Reference file paths instead of pasting full files when the files already exist in the workspace.
- Give Codex the exact task, expected behavior, and verification command.
- Scope the request to the smallest useful area of the repo.
- Say when you want only an explanation, only a patch, or only a review.
- Avoid sending long logs unless the exact error lines are needed.

Good pattern:

```text
Update tokens/research/token efficiency research.md so it teaches basic token-saving skills by platform. Keep it concise and push the change.
```

Less efficient pattern:

```text
Here is the entire repo, every previous idea, and several unrelated videos. Please figure out what to do.
```

### Save Tokens During Codex Work

- Let Codex search the repo with targeted commands instead of pasting large file contents into the prompt.
- Ask Codex to summarize only the files or diffs that matter.
- Request a short final summary instead of a full narrative of every command.
- Ask for focused tests or verification instead of broad unrelated test runs.
- Use separate tasks for unrelated changes.

### Codex Team Standards

- Keep repo guidance files concise and specific.
- Store durable project rules in repo docs instead of repeating them in every prompt.
- Ask for diffs or targeted edits when the desired change is small.
- Ask Codex to ignore unrelated files unless they affect the task.
- Prefer one clear task per turn for coding work.

## Claude Playbook

Claude-specific token savings are mostly about prompt caching, stable prompt structure, and avoiding repeated long instructions.

### Prompt Caching Basics

Claude supports prompt caching with explicit cache controls. Use this when the same long content appears across many requests.

- Cache stable system instructions, examples, tool definitions, and reference material.
- Keep cached content exactly the same across requests.
- Put dynamic user-specific content after the cached content.
- Avoid changing cached sections with timestamps, IDs, or per-user wording.
- Track cache reads and cache writes so teams can see whether caching is actually saving money.

### Claude Token-Savings Video

Source: [Give Me 10 Mins and I'll Save You Millions of Claude Tokens](https://www.youtube.com/watch?v=6cEQEba0i2A) by Nate Herk | AI Automation. Published May 21, 2026. Length: 10 minutes 43 seconds.

The public video metadata identifies this as a Claude-token savings video, and the description points to Claude prompt caching. The main company takeaway is to turn repeated Claude prompts into stable, cacheable templates.

Review checklist for this video:

- Identify the specific prompt-caching setup shown.
- Capture any before-and-after token or cost numbers.
- Add an internal Claude template example.
- Add any provider-specific settings, limits, or caveats.
- Test the pattern on one high-volume Claude workflow.

### Claude Team Standards

- Use cacheable templates for repeated Claude workflows.
- Keep long reusable instructions stable.
- Put request-specific data last.
- Use smaller Claude models for routine extraction, classification, and formatting when evals pass.
- Keep Claude outputs concise unless the business task requires detail.

## Other Models Playbook

This section covers OpenAI, Gemini, and other providers at a general level.

### OpenAI

- Use prompt caching for repeated stable prefixes.
- Use `prompt_cache_key` when it helps route similar requests for better cache hit rates.
- Use smaller models for simple tasks and stronger reasoning models only where needed.
- Tune reasoning effort by workflow.
- Use Batch API for large offline jobs.
- Use Flex processing when slower responses are acceptable.
- Use predicted outputs when regenerating mostly unchanged text or code.
- Use structured outputs for machine-consumed responses.

### Gemini

- Use Gemini caching for repeated large shared inputs.
- Put large reusable prompt sections before dynamic request data.
- Avoid changing the stable prefix when cache savings matter.
- Route simple tasks to cheaper models when quality is sufficient.

### Provider-Neutral Standards

- Log tokens, cost, model, latency, and outcome.
- Keep stable prompt parts stable.
- Control output length.
- Use structured outputs for automation.
- Route by task difficulty and risk.
- Test cheaper prompts and models against evals before rollout.
- Review expensive workflows monthly.

## Company-Wide Policy Draft

1. Every production AI workflow should log token usage, model, latency, cost estimate, cache hits where available, retries, and task outcome.
2. Shared prompt templates should separate stable reusable content from dynamic request data.
3. Teams should not send full documents, raw logs, broad folders, or long histories unless evals show the extra tokens improve results enough to justify the cost.
4. Agent workflows should define tool-call budgets, retry limits, and stop conditions.
5. Model choice should be tied to task complexity, risk, and eval results.
6. Long or repeated prompts should be reviewed for prompt caching.
7. Cost-reduction changes should be evaluated against quality before release.

## Quick Checklist

Use this before shipping or scaling an AI workflow.

- [ ] Are input tokens, output tokens, model, latency, and outcome logged?
- [ ] Is repeated prompt content stable and cacheable?
- [ ] Is dynamic request data placed after stable content?
- [ ] Is the output format concise enough for the task?
- [ ] Is this the cheapest model that passes evals?
- [ ] Are tool calls and retries budgeted?
- [ ] Can offline work use batch or flex processing?
- [ ] Did quality hold after the optimization?

## Source Rundown

| Source | Type | Date or Recency | What It Contributes | Best-Practice Takeaway |
| --- | --- | --- | --- | --- |
| [OpenAI Cost Optimization](https://developers.openai.com/api/docs/guides/cost-optimization) | Official docs | Current docs reviewed July 2026 | Reducing requests, minimizing input/output tokens, using smaller models, Batch API, and Flex processing. | Use cost controls at the architecture level, not only in prompts. |
| [OpenAI Prompt Caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Official docs | Current docs reviewed July 2026 | Automatic caching, exact prefix matches, cache retention, `prompt_cache_key`, and stable-prefix design. | Standardize prompt templates so stable prefixes are reused. |
| [OpenAI Reasoning Models](https://developers.openai.com/api/docs/guides/reasoning) | Official docs | Current docs reviewed July 2026 | Reasoning effort and when reasoning models are appropriate. | Tune reasoning effort by task instead of defaulting to maximum reasoning. |
| [OpenAI Predicted Outputs](https://developers.openai.com/api/docs/guides/predicted-outputs) | Official docs | Current docs reviewed July 2026 | Saving work when much of the response is already known. | Avoid regenerating expensive full outputs when most content is unchanged. |
| [Anthropic Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Official docs | Current docs reviewed July 2026 | Explicit cache controls, cache reads/writes, and stable reusable prompt sections. | Cache long repeated Claude prompt sections. |
| [Google Gemini Caching](https://ai.google.dev/gemini-api/docs/caching) | Official docs | Last updated July 7, 2026 | Reusing large repeated Gemini inputs. | Put stable shared content before dynamic request data. |
| [Give Me 10 Mins and I'll Save You Millions of Claude Tokens](https://www.youtube.com/watch?v=6cEQEba0i2A) | Video | Published May 21, 2026 | Claude token savings; public metadata and description point to prompt caching. | Review for practical Claude prompt-caching examples and convert them into templates. |
| [How Do AI Agents Spend Your Money?](https://arxiv.org/abs/2604.22750) | Research paper | Apr 24, 2026 | Token consumption in agentic coding tasks and weak relationship between more tokens and better accuracy. | Measure cost per successful task and set agent budgets. |
| [Compact Constraint Encoding](https://arxiv.org/abs/2604.07192) | Research paper | Apr 8, 2026 | Compact structured constraints can reduce prompt tokens without hurting compliance. | Keep reusable rules precise and compact. |
| [TSCG: Deterministic Tool-Schema Compilation](https://arxiv.org/abs/2605.04107) | Research paper | May 4, 2026 | Token-heavy tool schemas and compact tool representations. | Do not send irrelevant tools or oversized schemas to every request. |
| [Don't Break The Cache](https://arxiv.org/abs/2601.06007) | Research paper | Jan 9, 2026 | Prompt caching for long-horizon agentic tasks. | Avoid dynamic content in cacheable prefixes. |
| [Balancing Accuracy, Latency, And Cost At Scale](https://www.youtube.com/watch?v=Bx6sUDRMx-8) | Video | DevDay session | Tradeoffs between quality, speed, and cost. | Optimize against a quality target, not token count alone. |
| [Tuning Powerful Small Models With Distillation](https://www.youtube.com/watch?v=CqWpJFK-hOo) | Video | DevDay session | Moving repeated tasks to smaller models. | Use smaller specialized models for repeated high-volume workflows when evals justify it. |
| [Build Hour: Agentic Tool Calling](https://webinar.openai.com/on-demand/d1a99ac5-8de8-43c5-b209-21903d76b5b2) | Video/webinar | OpenAI Build Hour | Tool use, agents, and evals. | Agent architectures need task-level evaluation and controlled tool access. |

## Add More Research Here

### New Source Notes

Add source summaries below.

| Source | Date | Notes | Action |
| --- | --- | --- | --- |
|  |  |  |  |

### Internal Experiments

Record internal tests below.

| Workflow | Platform | Baseline Approach | Optimized Approach | Token Change | Quality Change | Decision |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

### Decisions

Record company decisions or standards below.

| Date | Decision | Owner | Review Date |
| --- | --- | --- | --- |
|  |  |  |  |

### Follow-Ups

- [ ] Identify top 10 token-consuming workflows.
- [ ] Add token and cache-hit logging standards.
- [ ] Build first workflow-specific eval set.
- [ ] Add one Codex example prompt.
- [ ] Add one Claude prompt-caching template.
- [ ] Add one OpenAI prompt-caching template.
- [ ] Define model routing tiers.
