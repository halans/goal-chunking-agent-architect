<!--
OUTPUT TEMPLATE — Claude Code subagent
Place the finished file at: .claude/agents/<agent-name>.md  (project)  or  ~/.claude/agents/<agent-name>.md (personal)
Frontmatter: name + description required-ish; tools and model optional.
Replace everything in {{ }} using the filled worksheets. Delete these comments.
-->
---
name: {{agent-name-lowercase-hyphenated}}
description: {{One or two sentences: what the agent does AND when Claude should delegate to it. Pulled from the charter mission + purpose.}}
# tools: Read, Grep, Bash, Edit   # optional — omit to inherit all; narrow to what the capability audit requires
# model: inherit                  # optional
---

# {{Agent display name}}

## Charter
- **Mission:** {{Section 1 — measurable goal}}
- **You are:** {{Section 3 — persona}}
- **Why it matters:** {{Section 2 — purpose}}
- **Definition of done:** {{Section 5 — done conditions}}
- **Non-goals:** {{Section 5 — non-goals}}
- **Success criteria:** {{Section 4 — the four quadrants, condensed}}

## Operating procedure
**Pre-flight**
1. {{template 03 pre-flight steps}}

**Main loop**
1. {{template 03 main-loop steps}}

**Post-flight**
1. {{template 03 post-flight steps}}

## Capabilities & rules
- **Tools/actions:** {{key [tool]/[action] cells from OW64 pillars 2 & 4}}
- **Quality bar:** {{pillar 5 highlights}}
- **Verification:** {{pillar 6 checks}}
- **Invariants:** {{template 03 invariants}}

## Reflection (after each task)
{{template 04 post-run reflection — bullet prompts; note memory/eval wiring if available}}

## Obstacles & autonomy
{{template 05 obstacle→countermeasure table + escalation policy + honesty guardrails}}

<!-- Keep the filled worksheets alongside this file as <agent-name>.harada.md for auditability. -->
