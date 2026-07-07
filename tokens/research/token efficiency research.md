# Token Efficiency Research

## Purpose

This note summarizes recent documentation, videos, articles, and papers about reducing token spend while preserving performance and accuracy. It is intended as a living company-wide best-practices document for token efficiency and AI cost reduction. Add new findings, experiments, and policy decisions in the editable sections near the bottom.

## Executive Summary

The strongest theme across the sources is that token efficiency is mostly a systems problem, not just a prompt-writing problem. The most reliable cost reductions come from measuring token usage, reducing repeated input tokens, controlling output length, routing tasks to the right model, and using evals to verify that cheaper or shorter workflows still meet quality standards.

For company-wide practice, the goal should not be "use fewer tokens at all costs." The better target is "spend tokens where they change outcomes." High-value reasoning, grounding, and verification should remain available for hard tasks, while routine, repetitive, or low-risk work should use cheaper models, cached prefixes, shorter prompts, batch/flex processing, or deterministic workflows.

## Main Themes Across Sources

### 1. Measure Before Optimizing

Several sources emphasize that organizations often lack visibility into AI spend until after bills arrive. Token costs can vary dramatically across tasks, tools, users, models, and retries. Company-wide token efficiency starts with instrumentation:

- Track input tokens, output tokens, reasoning tokens where available, cached tokens, tool-call counts, retries, model, latency, and task outcome.
- Report cost per successful task, not only cost per request.
- Compare token usage against quality metrics so teams can see where spend improves accuracy and where it is waste.
- Create dashboards by team, product area, workflow, and model.

Best-practice implication: every production AI workflow should log token usage and outcome quality before token limits are enforced.

### 2. Prompt Caching Is A First-Line Cost Optimization

OpenAI, Anthropic, Google, and the Claude-token video all point toward prompt caching as a core way to reduce repeated input-token cost. The shared design pattern is:

- Put stable content first: system instructions, policies, examples, tool definitions, schemas, reusable reference material.
- Put variable content last: user-specific data, fresh retrieval results, current turn details, timestamps, and dynamic tool outputs.
- Avoid changing the prefix unnecessarily, because cache hits depend on stable shared prefixes.
- Use provider-specific controls where available, such as OpenAI `prompt_cache_key`, Anthropic `cache_control`, or Gemini implicit/explicit caching.

Best-practice implication: prompt templates should be structured for cacheability by default. Treat cache-breaking changes as a cost-impacting change.

### 3. Model Routing Beats One-Model-For-Everything

Cost-focused articles and provider docs point toward routing tasks by complexity and risk. Simple tasks often do not need the most expensive model. Hard tasks, ambiguous tasks, regulated tasks, or tasks requiring deep reasoning may justify premium models.

Useful routing dimensions:

- Task complexity: classify, extract, rewrite, summarize, plan, code, reason, verify.
- Risk level: low-risk internal draft versus customer-facing or compliance-sensitive output.
- Input size: short prompt versus large-document or long-agent workflow.
- Quality requirement: approximate answer versus high-accuracy decision support.
- Latency tolerance: interactive versus asynchronous.

Best-practice implication: define default model tiers and escalation criteria. Use evals to prove where cheaper models are acceptable.

### 4. Agentic Workflows Need Special Guardrails

Agentic coding and tool-using workflows can consume orders of magnitude more tokens than normal chat because they loop, inspect files, call tools, retry failures, and verify work. Research shows that more agent tokens do not always correlate with better accuracy.

Company-wide controls should include:

- Tool-call budgets by task type.
- Maximum retry limits.
- Summarized tool outputs instead of full raw logs when possible.
- Retrieval that targets relevant files, rows, or documents instead of dumping everything into the prompt.
- Human approval before expensive long-horizon runs.
- Stop conditions when progress stalls.
- Evaluation based on final task success, not token volume.

Best-practice implication: agent token budgets should be workflow-specific, not global. A debugging agent and a classification endpoint should not share the same policy.

### 5. Output Tokens Matter Too

Most discussion focuses on input tokens, but output tokens can dominate for verbose reporting, code generation, and reasoning-heavy tasks. Practical controls:

- Request concise output unless the workflow truly needs detail.
- Use structured outputs for machine-consumed responses.
- Ask for diffs or patches instead of whole-file rewrites when safe.
- Use predicted outputs or similar approaches when regenerating mostly unchanged files.
- Separate internal reasoning/analysis from final user-visible response where APIs support it.

Best-practice implication: default response styles should be task-specific. A customer support classifier should not produce a narrative essay.

### 6. Batch, Flex, And Asynchronous Processing Reduce Cost Without Changing Quality

Provider docs describe lower-cost processing modes for non-urgent work. These do not necessarily reduce token count, but they reduce spend:

- Batch APIs for large asynchronous jobs.
- Flex or lower-priority service tiers where slower responses are acceptable.
- Background processing for evaluations, data enrichment, offline analysis, and internal maintenance tasks.

Best-practice implication: interactive product paths and offline jobs should use different service tiers.

### 7. Evals Are The Safety Net

Every serious optimization needs evals. Shorter prompts, cheaper models, prompt caching, tighter tool outputs, and routing can all preserve quality, but only if tested.

Minimum eval practice:

- Maintain representative examples for each workflow.
- Track accuracy, completeness, refusal behavior, latency, token usage, and cost.
- Compare baseline versus optimized prompts or model routes.
- Monitor regressions after prompt, model, retrieval, or tool-schema changes.

Best-practice implication: no major token-saving change should ship on cost reduction alone.

## Source Rundown

| Source | Type | Date or Recency | What It Contributes | Best-Practice Takeaway |
| --- | --- | --- | --- | --- |
| [OpenAI Cost Optimization](https://developers.openai.com/api/docs/guides/cost-optimization) | Official docs | Current docs reviewed July 2026 | Summarizes reducing requests, minimizing input/output tokens, smaller models, Batch API, and Flex processing. | Use cost controls at the architecture level, not only in prompts. |
| [OpenAI Prompt Caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Official docs | Current docs reviewed July 2026 | Explains automatic caching, exact prefix matches, cache retention, `prompt_cache_key`, and putting static content first. | Standardize prompt templates so stable prefixes are reused. |
| [OpenAI Reasoning Models](https://developers.openai.com/api/docs/guides/reasoning) | Official docs | Current docs reviewed July 2026 | Covers reasoning effort and when reasoning models are appropriate. | Tune reasoning effort by task instead of defaulting to maximum reasoning. |
| [OpenAI Predicted Outputs](https://developers.openai.com/api/docs/guides/predicted-outputs) | Official docs | Current docs reviewed July 2026 | Useful when much of the response is known, such as small edits to code or documents. | Avoid regenerating expensive full outputs when most content is unchanged. |
| [Anthropic Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Official docs | Current docs reviewed July 2026 | Explains automatic caching, explicit breakpoints, TTLs, and tools/system/messages cache ordering. | Use explicit cache boundaries for long-lived instructions, tools, and examples. |
| [Google Gemini Caching](https://ai.google.dev/gemini-api/docs/caching) | Official docs | Last updated July 7, 2026 | Describes implicit caching for Gemini models and placing large common content at the beginning. | Cross-provider confirmation that stable shared prefixes are valuable. |
| [Give Me 10 Mins and I'll Save You Millions of Claude Tokens](https://www.youtube.com/watch?v=6cEQEba0i2A) | Video | Published May 21, 2026 | Nate Herk video about reducing Claude token usage; visible metadata and description point to Claude prompt caching. | Review for practical Claude prompt-caching patterns and convert useful examples into internal templates. |
| [How Do AI Agents Spend Your Money?](https://arxiv.org/abs/2604.22750) | Research paper | Apr 24, 2026 | Studies token consumption in agentic coding tasks and finds high variability, high input-token costs, and weak relationship between more tokens and better accuracy. | Measure cost per successful task and do not assume more agent tokens means better outcomes. |
| [Compact Constraint Encoding](https://arxiv.org/abs/2604.07192) | Research paper | Apr 8, 2026 | Finds compact structured constraints can reduce prompt tokens without hurting constraint compliance. | Keep reusable rules precise and compact, especially in coding prompts. |
| [TSCG: Deterministic Tool-Schema Compilation](https://arxiv.org/abs/2605.04107) | Research paper | May 4, 2026 | Studies token-heavy tool schemas and compact representations for tool catalogs. | Large tool catalogs need schema compression or routing so irrelevant tools do not bloat every request. |
| [Don't Break The Cache](https://arxiv.org/abs/2601.06007) | Research paper | Jan 9, 2026 | Evaluates prompt caching for long-horizon agentic tasks across major providers. | Caching strategy matters; avoid dynamic content in cacheable prefixes. |
| [Balancing Accuracy, Latency, And Cost At Scale](https://www.youtube.com/watch?v=Bx6sUDRMx-8) | Video | DevDay session | Covers tradeoffs between quality, speed, and cost. | Optimize against a quality target, not token count alone. |
| [Tuning Powerful Small Models With Distillation](https://www.youtube.com/watch?v=CqWpJFK-hOo) | Video | DevDay session | Discusses distillation as a way to move repeated tasks to smaller models. | Use smaller specialized models for repeated high-volume workflows when evals justify it. |
| [Build Hour: Agentic Tool Calling](https://webinar.openai.com/on-demand/d1a99ac5-8de8-43c5-b209-21903d76b5b2) | Video/webinar | OpenAI Build Hour | Shows how agentic tools, tasks, and evals fit together. | Agent architectures need task-level evaluation and controlled tool access. |

## Video Notes: Claude Token Savings

Source: [Give Me 10 Mins and I'll Save You Millions of Claude Tokens](https://www.youtube.com/watch?v=6cEQEba0i2A) by Nate Herk | AI Automation. Published May 21, 2026. Length: 10 minutes 43 seconds.

Verified metadata identifies this as a Claude-token savings video, and the public description points to Claude prompt caching. The transcript was not available from this environment, so these notes should be expanded after manual review of the video.

Company interpretation for token-efficiency practice:

- Treat Claude prompt caching as a reusable-prefix optimization: stable system prompts, examples, tool schemas, process rules, and reference blocks should be reused exactly when possible.
- Separate stable prompt sections from dynamic request data so routine runs do not rebill the same long instructions at full cost.
- Avoid unnecessary changes to cached prefixes, such as timestamps, request IDs, user-specific wording, or reordered examples.
- Convert high-volume Claude workflows into standard templates so the same cacheable prefix is shared across runs.
- Measure cache hit rate, input tokens, output tokens, and cost per completed task before and after applying the pattern.
- Add a follow-up review to capture any concrete implementation steps shown in the video.

## Company-Wide Best Practices

### Governance

- Define approved model tiers and default routes.
- Require token and cost logging for production AI workflows.
- Review high-spend workflows monthly.
- Track cost per successful task, not only total tokens.
- Create an escalation path for workflows that need premium models or high reasoning effort.

### Prompt And Input Design

- Put stable reusable content first.
- Put dynamic request-specific content last.
- Keep instructions short, explicit, and non-duplicative.
- Remove outdated examples and unused policies from shared prompts.
- Store long-lived reference material outside prompts when only a small piece is needed for the current task.
- Use concise structured inputs instead of verbose natural-language wrappers for machine-to-machine workflows.

### Agent Design

- Limit tool catalogs to relevant tools for the task.
- Summarize or filter verbose tool outputs.
- Set retry and tool-call budgets.
- Prefer targeted retrieval over broad file, log, or document dumps.
- Add stop conditions for stalled or repetitive loops.
- Require human confirmation before expensive long-running agent runs.

### Model Routing

- Use small or low-cost models for classification, extraction, formatting, and simple summarization.
- Use stronger models for ambiguous reasoning, planning, coding, regulated decisions, and high-impact user-facing output.
- Use reasoning models only when the task benefits from reasoning.
- Tune reasoning effort by workflow and measure the quality difference.

### Processing Mode

- Use Batch APIs for large offline workloads.
- Use Flex or lower-priority processing for non-urgent jobs.
- Keep interactive product paths on latency-appropriate service tiers.
- Use predicted outputs or diff-based editing when most output is already known.

### Evaluation

- Maintain workflow-specific eval sets.
- Include both easy and hard examples.
- Compare token usage, latency, cost, and quality.
- Require eval evidence before switching models, shortening prompts, or compressing instructions.
- Monitor production drift after changes.

## Initial Company Policy Draft

1. Every production AI workflow must log token usage, model, latency, cost estimate, cache hits where available, and task outcome.
2. Shared prompt templates must be structured for cacheability, with stable instructions and examples before dynamic request data.
3. Teams should not include full conversation history, raw logs, or broad document dumps unless evals show they improve results enough to justify the extra tokens.
4. New agent workflows must define tool-call budgets, retry limits, and stop conditions.
5. Model choice must be tied to task complexity and risk, with cheaper defaults for routine tasks and escalation paths for complex tasks.
6. Cost-reduction changes must be evaluated against task quality before release.

## Open Questions

- Which internal workflows currently consume the most tokens?
- Which workflows have enough examples to build eval sets?
- Which prompts have stable prefixes large enough to benefit from prompt caching?
- Which agent tools return verbose outputs that should be summarized or filtered before being sent back to a model?
- Which tasks can move to smaller models without quality loss?
- Which workloads can be moved to Batch or Flex processing?

## Add More Research Here

### New Source Notes

Add source summaries below.

| Source | Date | Notes | Action |
| --- | --- | --- | --- |
|  |  |  |  |

### Internal Experiments

Record internal tests below.

| Workflow | Baseline Model/Prompt | Optimized Approach | Token Change | Quality Change | Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Decisions

Record company decisions or standards below.

| Date | Decision | Owner | Review Date |
| --- | --- | --- | --- |
|  |  |  |  |

### Follow-Ups

- [ ] Identify top 10 token-consuming workflows.
- [ ] Add token and cache-hit logging standards.
- [ ] Build first workflow-specific eval set.
- [ ] Test prompt caching on shared templates.
- [ ] Review the Claude token-savings video and add transcript-backed implementation notes.
- [ ] Define model routing tiers.
