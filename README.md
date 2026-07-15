# context-and-tokens--best-practices

This repo is a shared research hub for practical best practices around AI context management and token efficiency. The goal is to collect clear, source-backed notes that help teams use LLMs more effectively while reducing unnecessary token spend.

Use the `tokens/` folder for research on token savings, prompt caching, tooling, model routing, and cost reduction. Use the `context/` area for research on context management, retrieval, memory, and related workflows.

## RTK Token Savings Study

The repo includes a ready-to-run study kit for evaluating RTK command-output compression:

- [RTK Token Savings Study](tokens/rtk-token-savings-study/README.md)
- [Static Executive Dashboard](tokens/rtk-token-savings-study/dashboard/index.html)

Use it to capture a pre-RTK baseline, run controlled raw-vs-RTK benchmarks, export `rtk gain --all --format json`, and present savings to leadership with clear assumptions.
