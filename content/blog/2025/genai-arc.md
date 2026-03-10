---
title: "The GenAI Arc"
description: "GenAI follows the same democratization arc as 4GLs and SQL, but the blast radius is larger. The promise and the threat are both real."
author: "Chris Grobauskas"
date: "2025-06-16"
updated: "2026-02-27"
tags:
  - Coding
  - AI
  - GenAI
  - Technical History
  - Security
  - Risk
---

SQL changed everything with one idea: describe what you want, not how to get it.

`SELECT * FROM users WHERE age > 25`

No loops. No conditionals. Just intent. That idea, declare the goal and let the system figure out the implementation, is the core of Fourth Generation Languages (4GLs). SQL emerged from it in the 1970s and was commercialized alongside other 4GLs in the 1980s.

<!-- more -->

GenAI takes the same arc further: natural language instead of SQL syntax, spanning every domain instead of just data. 4GLs democratized access to *data*. GenAI democratizes access to *systems*, and that difference is what makes both the promise and the threat real.

## The Promise

Computing has been moving toward democratization for fifty years. I find that exciting and hopeful.

Desktop publishing moved us away from typist pools, paper memos, and a small number of publishing houses controlling all publishing. GenAI is following the same pattern. Individuals without technical backgrounds can now ask for code, request explanations, or summarize documents without needing to know R or Python. Small businesses can automate routine tasks that once required a developer.

Those new participants will produce buggy code, security vulnerabilities, and logic errors. So do professionals. The potential for broader participation is a future worth building toward.

## The Threat Vector

The promise comes with real peril, especially for agentic AI systems that connect to external systems.

> **For decision-makers:** A compromised AI agent can exfiltrate data the same way malware does. The difference is that nobody installed it maliciously ... it was invited in to do a job. That means the business owns the breach: regulatory fines, litigation exposure, and reputational damage.

Agentic GenAI has the same capabilities as malware for data exfiltration. The difference is intent: malware acts deliberately, while GenAI becomes a threat vector through prompt injection (tricking the model with malicious input), context poisoning (corrupting the data it reasons over), and hallucinations (confidently wrong output). 

Simon Willison calls the combination of private data, untrusted content, and external system access the [the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).


The obvious response is that existing infosec controls ... network segmentation, least-privilege access, audit logging ... should provide a defense. For traditional deterministic software, they do, but GenAI agents are non-deterministic. The same input can produce different outputs, and an agent that behaves correctly a thousand times can fail unpredictably on the next run. 

> A related objection: "Just sandbox it." Sandboxing GenAI systems is rarely practical. Models run on someone else's infrastructure, and agents must connect to systems to take actions ... that's the whole point of agentic AI. If the agent can't reach anything, it can't do anything useful.

Your main control over data exfiltration is to limit what GenAI agents can access. Limit prompt injection surface, mitigate context poisoning, and keep a [human in the loop](/blog/2023/human-in-the-loop/) for consequential decisions. This is not a reason to avoid AI. It is a reason to be prudent.

## The Agent Access Test

What might an **Agent Access Test** look like?

- **What's the blast radius?** If the agent is compromised, what can it reach? Limit access to the minimum needed for the task. Classify the change as [reversible or irreversible](/blog/2025/willing-to-fail/) before granting write access.
- **Is a human in the loop for irreversible actions?** Agents that can read are safer than agents that can write. Agents that can write need more oversight.
- **Have you tested adversarial inputs?** Prompt injection and context poisoning are not theoretical. Test for them the way you'd test for SQL injection.
- **Do you have an audit trail?** You need to know what an agent did, when it did it, and why. Without logging of agent actions and the inputs that drove them, you can't verify correct behavior, investigate failures, or meet compliance obligations. Confidence in an AI system requires evidence, not faith.

4GLs let anyone with access query data. GenAI lets anyone command systems. The arc is the same; the blast radius isn't.

## Links

- [The Lethal Trifecta - Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) - private data, untrusted content, and external system access: why the combination is dangerous
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - reference for prompt injection, data poisoning, and related LLM threats
- [Principles for Responsible Algorithmic Systems - ACM](https://www.acm.org/binaries/content/assets/public-policy/ustpc-approved-generative-ai-principles) - governance framework for algorithmic accountability, including the principle that organizations are responsible for decisions made by algorithms they use
- [Human in the Loop](/blog/2023/human-in-the-loop/) - when AI decisions need human oversight and how to think about the audit trail
- [Risk and Reversibility](/blog/2025/willing-to-fail/) - how to classify decisions before granting write access to automated systems
- [The Constraint Test: When Code Generation Masks the Real Problem](/blog/2026/tool-creation/) - GenAI makes creating tools easier, which amplifies both the promise and the risk
- [Where the Collapsed Lifecycle Breaks](/blog/2026/collapsed-lifecycle/) - what happens to production state when an AI-driven deployment goes wrong and why the blast radius is larger when it reaches data
