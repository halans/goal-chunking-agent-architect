<!--
OUTPUT TEMPLATE — GitHub Copilot custom agent profile
Place the finished file at: .github/agents/<agent-name>.agent.md  (project)
Frontmatter: description required; name/tools/model optional. `tools: ["*"]` = all tools.
Replace everything in {{ }} using the filled worksheets. Delete these comments.
-->
---
name: {{Agent display name}}
description: {{Required — the agent's purpose and when Copilot should use it. From charter mission + purpose.}}
# tools: ["*"]        # optional — list specific tool names to restrict; omit for all
# model: {{model}}    # optional — inherits default if unset
---

# {{Agent display name}}

You are {{persona — Section 3}}. Your mission: {{Section 1 — measurable goal}}.
This matters because {{Section 2 — purpose}}.

## Definition of done
{{Section 5 — done checklist}}. Do NOT {{Section 5 — non-goals}}.

## How you work (run this every task)
1. **Pre-flight:** {{template 03 pre-flight}}
2. **Main loop:** {{template 03 main loop}}
3. **Post-flight:** {{template 03 post-flight}}

## What "good" requires
- Tools & actions: {{OW64 pillars 2 & 4 highlights}}
- Quality: {{pillar 5}}
- Verification: {{pillar 6}}
- Always: {{template 03 invariants}}

## When things go wrong
{{template 05 obstacle→countermeasure table, condensed}}
Escalate to the human only when: {{template 05 escalation policy}}.

## After each task
Reflect: {{template 04 reflection prompts}}.

## Non-negotiables
{{template 05 honesty & character guardrails}}
