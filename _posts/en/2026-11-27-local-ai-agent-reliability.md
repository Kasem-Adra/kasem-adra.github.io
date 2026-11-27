---
title: "Can We Trust a Local AI Assistant?"
seo_title: "Local AI Assistant Reliability and Task Verification | Kasem Adra"
description: "An evidence-based guide to local AI assistant reliability, silent tool failures, independent verification, and the ACO-LLM evaluation and its limits."
subtitle: "From running language models locally to building agents that execute tasks and verify their outcomes"
summary: "A success message does not prove that an AI agent completed a task. This article explains silent tool failures, task routing, verification and bounded repair, then examines the ACO-LLM evaluation, its reported results and the limits of their interpretation."
lang: "en"
permalink: "/en/blog/local-ai-agent-reliability/"
date_published: "2026-11-27"
date_modified: "2026-11-27"
published_label: "27 November 2026"
modified_label: "27 November 2026"
category: "Technology and research"
author: "Kasem Adra"
author_display: "Kasem Adra"
image: "/assets/local-ai-agent-reliability-hero.webp"
image_alt: "A computer workstation for local AI research, with an illustrative workflow showing a local model, tool action, state check and independent evaluation."
image_caption: "AI-generated illustrative image. The interface on the monitor is representational, not an actual screenshot of the evaluation environment."
editorial_note: "This is an explanatory article. It does not replace the research protocol or the original results preprint."
article_section: "Artificial intelligence; local models; AI agents; reliability engineering"
keywords: ["local AI", "local AI assistant reliability", "AI agent reliability", "silent tool failure", "independent verification", "ACO-LLM", "Gemma 4", "local language models"]
about: ["Local artificial intelligence", "AI agents", "task execution verification", "reliability engineering"]
citations: [{"name":"ACO-LLM Research Protocol","url":"https://doi.org/10.5281/zenodo.24488951"},{"name":"ACO-LLM Evaluation Results preprint","url":"https://doi.org/10.5281/zenodo.24549236"},{"name":"Gemma 4 model overview","url":"https://deepmind.google/models/gemma/gemma-4/"},{"name":"NIST AI 600-1 Generative AI Profile","url":"https://doi.org/10.6028/NIST.AI.600-1"},{"name":"OWASP Top 10 for Agentic Applications 2026","url":"https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"}]
---
## Overview

It is now possible to run capable language models on personal computers and connect them to tools that read and write files, transform data, and carry out multi-step operations. Yet the ability to issue a command or call a tool does not mean that the requested task has been completed correctly. An assistant may display a success message even when the requested change did not occur, or when the resulting output is incomplete or incorrect.

This article examines local AI assistant reliability from a systems-engineering and agent-evaluation perspective. It uses **Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM)** as a research case study: what problem does it address, how was it evaluated, what did the reported results show, and what limits should be placed on their interpretation?

## At a glance

| Item | Description |
|---|---|
| Subject | Reliability of local AI assistants and tool-using agents |
| Author | Kasem Adra |
| Research case study | ACO-LLM |
| Model used in the evaluation | Gemma 4 12B IT QAT, identifier gemma4:12b-it-qat |
| Task set | 96 base tasks, each with Arabic and English variants |
| Evaluation size | 8,064 episodes across six experimental arms |
| Primary comparison | Arm D versus arm B |
| Main estimate | +20.83 percentage points in equally weighted task success |
| Publication status | Results preprint; not peer reviewed |

## 1. What is local artificial intelligence?

**Local inference** means running a model and processing its inputs on a user's device or within infrastructure under the user's control, rather than sending the model-inference request to an externally hosted service. Open-weight models allow developers to download model weights and run or adapt them subject to the relevant licence.

Google DeepMind's **Gemma 4** family is one example of open-weight models designed for a range of uses, including reasoning, coding, agentic workflows and function calling. The resources required to run a model depend on its size, weight precision, context window and available hardware. [3](https://deepmind.google/models/gemma/gemma-4/)

Three concepts should nevertheless be kept separate:

- **Local execution:** where the model runs and its resources are managed.
- **Privacy:** how data is processed, stored or transmitted to other services.
- **Reliability:** whether a task is completed correctly and whether that outcome can be demonstrated.

Running a model locally does not prove that every part of the system is offline. An agent may still use a browser, search service or external API. Privacy therefore has to be assessed across the complete data flow, not inferred from the location of model inference alone.

## 2. From a language model to an AI agent

A conventional language model generates text in response to input. An **AI agent** adds mechanisms that allow it to plan, use tools and interact with an external environment. Its execution cycle can be summarized as follows:

1. Understand the user's request and the conditions for success.
2. Decide whether direct reasoning or interaction with the environment is required.
3. Select appropriate tools and permissions.
4. Execute an action and observe the response.
5. Inspect the resulting state against the acceptance criteria.
6. Repair a recoverable failure within defined limits, or report that the task was not completed.

This changes how the system must be evaluated. A response can be linguistically convincing while the file was never created, the data was not saved, or an unintended path was modified. The system must therefore distinguish **what the model says it did** from **what the environment demonstrates after execution**.

## 3. Silent failure: when a tool reports success without doing the work

A **silent failure** occurs when a tool returns a response that suggests success even though the requested state change did not take place. One example is a file-writing tool that acknowledges a write while the file remains unchanged or the specified data is absent.

The sequence can be represented as follows:

- A user requests a file containing specified data.
- The agent sends a write command to a tool.
- The tool returns a success acknowledgement.
- The file is missing or does not contain the requested data.
- The agent reports completion based only on the tool's acknowledgement.

The problem is not merely a wording error. It is an invalid inference from the available evidence. A tool acknowledgement proves that a particular response was returned; by itself, it does not prove that the requested state now exists.

The appropriate check depends on the task. For a file-writing operation, it may include confirming that the file exists at the correct path, reading its contents and comparing them with the expected data. For a data-transformation task, it may require checking the schema, record count, final values and whether unrelated files remained unchanged.

## 4. The ACO-LLM methodology

**Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM)** investigates whether task-contract-driven routing, outcome verification and bounded repair can improve independently assessed task completion.

The method does not assume that every request needs extended planning or tool use. It distinguishes between tasks that can be handled through direct inference and tasks that require a change to the environment.

### 4.1 Task contracts and routing

A **task contract** describes the required outcome, whether environmental interaction is necessary, which tools are permitted, which observable acceptance conditions must be met, and which side effects are prohibited.

Routing uses this information to select an execution path. The intention is to avoid unnecessary processing for simple tasks while applying additional controls when a task requires external action.

### 4.2 Outcome verification

A task is not considered successful simply because the model or a tool reports completion. The resulting state must be compared with defined acceptance criteria, ideally by an evaluator independent of the model's success claim.

It is important to distinguish **runtime structural checks**, such as confirming that a file exists or has a particular format, from an **independent reference evaluator** that checks expected values and final state. An output can pass a structural check without being correct in substance.

### 4.3 Bounded repair

When a recoverable failure is detected, the system may attempt a correction within predefined limits on the number of attempts, elapsed time, tool calls and resource use. The aim is to prevent uncontrolled retries, particularly when actions are costly or may have side effects.

### 4.4 Experimental arms

The evaluation was designed to compare six arms with different routing, verification and repair policies:

| Arm | Execution policy |
|---|---|
| A | Direct inference without entering the tool loop |
| B | Fixed-path tool-capable loop relying on ordinary tool feedback |
| C | Task-contract routing without a mandatory verification gate |
| D | Task-contract routing with mandatory verification and bounded repair on tool tasks |
| E | Arm D plus structured, episode-local failure memory |
| F | Fixed-path tool-capable loop with mandatory verification and bounded repair |

These comparisons help examine different parts of the policy. The primary comparison, **D versus B**, estimates the effect of the combined policy; it does not isolate routing from verification and repair on its own. Other planned contrasts, including C versus B, D versus F, F versus B and D versus C, help interpret the components. [1](https://doi.org/10.5281/zenodo.24488951)

## 5. Experimental design

The evaluation used one local model: **Gemma 4 12B IT QAT**, with the identifier gemma4:12b-it-qat. The test set contained 96 base tasks, each with an Arabic and an English variant:

- 32 deterministic-reasoning tasks, evaluated in the clean condition.
- 64 tool-required tasks, evaluated under three conditions: clean execution, a controlled explicit failure, and a silent no-op in which the tool acknowledges an action without making the state change.

Each scheduled case was repeated three times across six experimental arms. This produced 1,344 episodes per arm and **8,064 episodes in total**. The evaluation used simulated tools in a controlled environment; it was not a test of real services or production APIs. [2](https://doi.org/10.5281/zenodo.24549236)

## 6. Main results

### 6.1 Primary estimate

The primary estimate showed that arm D increased task success, as judged by the independent evaluator, by **20.83 percentage points** compared with arm B. The 95% confidence interval ranged from 18.23 to 23.44 percentage points.

The estimate was calculated from paired differences within each of the 96 base tasks, with equal weight assigned to every base task. A cluster bootstrap with 10,000 resamples of base tasks within their strata was used to estimate the confidence interval.

### 6.2 Raw success rates

| Metric | Arm B | Arm D |
|---|---:|---:|
| Successful episodes | 834 of 1,344 | 1,192 of 1,344 |
| Raw success rate | 62.05% | 88.69% |
| Raw difference | — | +26.64 percentage points |

The raw difference of 26.64 points is not the same as the primary estimate of 20.83 points because the two calculations use different weighting. The raw rate counts every episode, whereas the primary estimate gives each base task equal weight. Tool tasks were run under three conditions and therefore contribute more episodes to the raw rate.

### 6.3 Silent-failure condition

For episodes assigned to the silent-failure condition, the results were:

| Metric | Arm B | Arm D |
|---|---:|---:|
| Successful episodes | 0 of 384 | 363 of 384 |
| Success rate | 0.00% | 94.53% |
| Unsuccessful episodes | 384 | 21 |

This is a substantial improvement for arm D under the specific tested condition. It does not mean that every silent failure was resolved: 21 of the 384 arm-D episodes remained unsuccessful.

### 6.4 Execution cost

The improvement was accompanied by higher resource use in arm D compared with arm B:

| Metric | Arm B | Arm D | Increase in D |
|---|---:|---:|---:|
| Mean time per episode | 2.096 s | 2.279 s | 0.183 s (+8.73%) |
| Mean generated tokens | 44.57 | 49.83 | 5.26 (+11.80%) |

These figures show that verification and repair can add time and token consumption. They should not be described as cost-free or as improving every metric simultaneously.

## 7. What does “verification” mean in this evaluation?

Not all checks provide the same level of evidence. A runtime check that an agent can use during execution is different from an independent evaluator that determines whether the final result is correct.

In one evaluation example, an output passed a structural check because it contained integers, but it did not match the correct value checked by the independent evaluator: the expected product was 1908, while the output contained 1938. The example illustrates why structural validity is not equivalent to substantive correctness.

Acceptance criteria must therefore match the task. File existence is insufficient when the requested content must also be checked. A valid CSV schema does not prove that every value is correct, and completion of an intermediate step does not prove that an entire workflow succeeded.

The strength of an evaluation also depends on the quality of its evaluator and its ability to reject incorrect outputs and prohibited side effects.

## 8. Limits of the results and claims that are not established

The results support a bounded conclusion: within the tested task set, environment and model, policy D achieved a higher independently assessed success rate than reference arm B. They do not establish that the same result will occur in every deployment.

Key limitations include:

- **One model:** The evaluation used only Gemma 4 12B IT QAT. The findings cannot automatically be generalized to other models.
- **Simulated tools:** Simulated tools do not reproduce every issue involving real services, networks or permissions.
- **A defined task set:** The 96 base tasks do not necessarily represent all long-horizon tasks or professional workflows.
- **Specific fault types:** The evaluation included controlled explicit failures and silent no-op failures; it does not establish robustness to every attack or persistent fault.
- **Limits of verification:** A structural check alone cannot prove semantic correctness or open-ended factual accuracy.
- **Additional cost:** Arm D used more time and generated tokens per episode on average than arm B.
- **Publication status:** The results are reported in a preprint that has not been peer reviewed.

The research protocol and the results paper are separate documents: the protocol describes the design and analysis rules, while the results preprint reports the evaluation and its outputs. [1](https://doi.org/10.5281/zenodo.24488951) [2](https://doi.org/10.5281/zenodo.24549236)

## 9. Engineering and security considerations for reliable agents

Reliability is not limited to checking output correctness. An agent that can read or modify files or execute commands also needs explicit security boundaries.

Core practices include:

- **Least privilege:** Give an agent only the access required for its task, and restrict permitted paths and commands.
- **Separate planning from execution:** A model's decision alone should not authorize a sensitive or irreversible operation.
- **Human approval where appropriate:** Require confirmation before deletion, publication, data transmission or significant changes.
- **Auditable logs:** Record commands, outcomes, errors and repair attempts while avoiding unnecessary storage of secrets or personal data.
- **Time and resource limits:** Define execution deadlines, tool-call limits and repair budgets.
- **Treat external content as untrusted:** Files, web pages and tool messages may contain misleading instructions and should not automatically be treated as trusted commands.

Frameworks such as the NIST Generative AI Risk Management Profile and the OWASP Top 10 for Agentic Applications address related aspects of governance and security, including tool misuse, privilege abuse and context manipulation. They are complementary references, not evidence that the ACO-LLM evaluation tested all of these risks. [4](https://doi.org/10.6028/NIST.AI.600-1) [5](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

## 10. Relationship to previous research

ACO-LLM sits within a broader research area concerned with moving language models from text generation to interaction with tools and environments.

- **ReAct** introduced an approach that combines reasoning, actions and environmental interaction. [6](https://arxiv.org/abs/2210.03629)
- **Reflexion** studied the use of feedback and verbal memory to improve agents across attempts. [7](https://arxiv.org/abs/2303.11366)
- **AgentBench** introduced a framework for evaluating language models as agents in interactive environments. [8](https://arxiv.org/abs/2308.03688)
- **τ-bench** focused on tool-agent-user interaction and outcome evaluation in practical domains. [9](https://arxiv.org/abs/2406.12045)
- **AgentDojo** provided an environment for studying prompt injection and attacks on tool-using agents. [10](https://arxiv.org/abs/2406.13352)

ACO-LLM does not claim that tool use, external verification or adaptive routing are individually new ideas. Its research question concerns a specific integration of task-contract routing, verification and bounded repair on a fixed local model, evaluated with bilingual tasks, controlled fault injection and resource accounting. [1](https://doi.org/10.5281/zenodo.24488951)

## 11. Frequently asked questions

### Does running a local AI assistant guarantee privacy?

No. Local inference can reduce the need to send model inputs to an external inference service, but an agent may still use online tools or services. Privacy assessment requires reviewing data flows, permissions, storage and logs.

### Does the 20.83-percentage-point improvement mean that the model became more intelligent?

No. The result compares two execution policies, D and B, using the same local model. It indicates improved task success under the evaluation conditions, not an increase in the intelligence of the underlying model.

### Why is the primary difference different from the raw difference?

The primary estimate gives equal weight to the 96 base tasks, whereas the raw rate counts every execution episode. Tool tasks have three conditions and therefore contribute more episodes to the raw rate.

### Did the evaluation prove that ACO-LLM works with real tools?

No. The evaluation used simulated tools in a controlled environment. A separate evaluation using real services is required before generalizing the findings to production settings.

### Has the results paper been peer reviewed?

No. It is a results preprint that has not been peer reviewed. Its methods and results are available on Zenodo and should be interpreted with that status in mind.

## Original research and related pages

For the underlying research documents, rather than this explanatory overview alone, see:
- [ACO-LLM protocol page on this website](https://kasemadra.com/en/publications/aco-llm/).
- [ACO-LLM evaluation results page on this website](https://kasemadra.com/en/publications/aco-llm-results/).
- [ACO-LLM research protocol on Zenodo](https://doi.org/10.5281/zenodo.24488951).
- [ACO-LLM results preprint on Zenodo](https://doi.org/10.5281/zenodo.24549236).

## Conclusion

The reliability of an AI assistant should not be measured by how confidently it responds or how readily it announces completion. The more important criterion is whether the final state matches the request and whether appropriate evidence can be provided.

The ACO-LLM evaluation indicates that task-aware routing, verification and bounded repair can improve task success in a controlled local setting. It also reveals additional resource costs and limits related to the single model, simulated tools and scope of the test set.

**Trust in an agent does not come from saying “completed”. It comes from reviewable evidence that the execution satisfied the task requirements.**

## References

1. Adra, K. (2026). *Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM): Research Protocol.* [Zenodo: 10.5281/zenodo.24488951](https://doi.org/10.5281/zenodo.24488951).
2. Adra, K. (2026). *ACO-LLM: Evaluation Results.* Results preprint, not peer reviewed. [Zenodo: 10.5281/zenodo.24549236](https://doi.org/10.5281/zenodo.24549236).
3. Google DeepMind. *Gemma 4.* [Official model page](https://deepmind.google/models/gemma/gemma-4/).
4. Autio, C. et al. (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile.* NIST AI 600-1. [DOI](https://doi.org/10.6028/NIST.AI.600-1).
5. OWASP GenAI Security Project. *Top 10 for Agentic Applications 2026.* [Source](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).
6. Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* [arXiv:2210.03629](https://arxiv.org/abs/2210.03629).
7. Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* [arXiv:2303.11366](https://arxiv.org/abs/2303.11366).
8. Liu, X. et al. (2023). *AgentBench: Evaluating LLMs as Agents.* [arXiv:2308.03688](https://arxiv.org/abs/2308.03688).
9. Yao, S. et al. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* [arXiv:2406.12045](https://arxiv.org/abs/2406.12045).
10. Debenedetti, E. et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* [arXiv:2406.13352](https://arxiv.org/abs/2406.13352).