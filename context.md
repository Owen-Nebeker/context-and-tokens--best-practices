# Understanding Context #

The context window is the amount of text an LLM can "see" and consider at once when generating a response — including your prompt, any files/code you've pasted, and the conversation history so far. It's measured in tokens (roughly ¾ of a word each, so ~750 words ≈ 1,000 tokens).

### The Core Mechanics ###
- Everything that's ever been said in a conversation — your messages, the model's replies, any documents attached — competes for space in that window.
- Once you exceed the limit, older content gets dropped, truncated, or (depending on the tool) summarized to make room. The model literally cannot "remember" what's outside the window unless something external (like the memory feature here) re-feeds it back in.
- It's not the same as long-term memory. A large context window lets the model reason over a lot of material in one go; it doesn't mean the model retains anything after the conversation/session ends unless a separate memory system is layered on top.

### Relevance to AI Coding ###
- Whole-codebase awareness: A small context window means the model only sees the file(s) you paste, not your whole repo — it can miss how a function is used elsewhere, or contradict conventions in files it never saw.
- Long files get truncated: If a file is huge (thousands of lines), it may not fit, or older parts of a long editing session get pushed out, causing the model to "forget" earlier decisions or code it wrote minutes ago.
- Cost and speed tradeoff: Bigger context windows mean more compute per request — larger windows are typically slower and pricier per call, so tools often chunk/retrieve only relevant snippets rather than dumping the whole repo in.
- Tools like Claude Code / Cursor manage this for you — they selectively pull in relevant files rather than relying on you to fit everything in the window manually.

### Bigger isn't always Better ###
- New LLM models like Opus, Fable, and GPT 5.5 have context windows of 1 million tokens, equivalent to several tokenized novels, but think of this more as a ceiling than a recommended benchmark with gauranteed performance benefits.
- *Lost in the Middle* [Liu et al. (2023, arXiv:2307.03172)](https://arxiv.org/pdf/2307.03172) was a foundational study exposing strong primacy and recency biases in context windows across all models -- in other words, in a large window, a model is much more likely to utilze context at the beginning and end of its window, skiming over the middle.
- A separate mechanism known as "context rot" describes decreasing accuracy even as position remains fixed as context size grows, likely due to 
the mathematical limits of tranformer architecture. 

### THE SINGLE BEST PRACTICE you can use to maximize the designed utility of context while minimizing token cost is simple: start a new chat / project whenever switching topics. 

A simple "hey" in the middle of an intense Claude Code session will use hundreds of thousands of tokens, not because of the messsage itself, but because the LLM will read through everything you've sent thinking that it's relevant information to your prompt. 

