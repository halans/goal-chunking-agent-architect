---
name: goal-chunking-agent-architect
description: >-
  Design and generate a new AI agent (or agentic workflow) that reliably reaches a
  specific goal. Use this when the user asks to create, design, architect, scaffold, 
  or "spin up" an agent or subagent aimed at a concrete outcome — and especially
  when they mention goal chunking, the Harada Method, mandala/OW64 goal decomposition, or want a
  rigorous, self-reliant agent instead of an ad-hoc prompt.
license: MIT
---

# Goal-Chunking Agent Architect

Turn a goal into a **deployable agent** by running the goal through the Harada Method.

The Harada Method is a disciplined system for reaching meaningful goals through small,
consistent, well-decomposed actions aligned to a clear purpose. 
This skill treats *agent design as goal achievement*: the same five
instruments that make a person reliably hit a goal are used to make an agent reliably
hit its objective.

You are not just writing a prompt. You are producing:

1. **The reasoning artifacts** — filled Harada worksheets (goal sheet, OW64 mandala,
   routine sheet, reflection loop, countermeasures) that show *why* the agent is built
   the way it is, and
2. **A deployable agent definition** — a subagent, or a generic system prompt, generated from those worksheets.

---

## When to use / when not to use

**Use it when** the request is goal-shaped and deserves rigor:
- "Create an agent that keeps our changelog up to date."
- "Design a subagent that triages incoming bug reports."
- "Build me an agent that reviews PRs for security issues."
- "Use the Harada Method to make an agent that…"

**Skip it (or go lighter)** for one-off asks that don't warrant a persistent agent
("summarize this file"), or when the user just wants a quick prompt tweak. You can still
borrow Phase 1 (charter) and Phase 2 (decomposition) informally.

---

## The model: Harada instrument → agent construct

Each Harada instrument produces one part of the agent. Read `references/mapping.md` for
the full rationale and examples; the short version:

| Harada instrument | What it produces in the agent |
| --- | --- |
| **Long-Term Goal Setting Sheet** | **Agent Charter** — mission, purpose ("why"), the persona the agent must *become*, four-quadrant success criteria, definition of done, non-goals, capability audit |
| **Open Window 64 (OW64) mandala** | **Capability Decomposition** — 1 central goal → 8 capability pillars → 64 concrete behaviors/tools/subtasks that become the agent's operating backbone |
| **Routine Check Sheet** | **Standard Operating Procedure** — the repeatable pre-flight → main-loop → post-flight checklist the agent runs *every* task |
| **Daily Diary** | **Reflection & Self-Evaluation Loop** — the post-run retrospective the agent writes to self-correct (and log to memory/evals where supported) |
| **Self-analysis & self-reliance** | **Obstacle/Countermeasure plan + Autonomy rules** — anticipated failure modes with pre-committed responses, escalation policy, and honesty guardrails |

The central philosophy carries over too: **self-reliance** (the agent recovers on its
own instead of stalling), **consistency over intensity** (deterministic guardrails beat
heroic one-off effort), and **character + performance together** (the agent is honest,
cites sources, and serves the user's real goal — not just the literal instruction).

---

## Workflow

Work through the phases in order. Keep the user in the loop at Phase 0 and Phase 7; the
middle phases you can draft and then show. Fill each template in `templates/` as you go —
either inline in the conversation or as files in the target repo.

### Phase 0 — Intake (align on the goal)
Capture the objective in **one sentence**. If any of the following are unclear, ask **up
to three** focused questions, then stop asking and proceed:
- **Goal & success criteria** — what outcome, measured how?
- **Environment & tools** — what can the agent actually use (repos, APIs, MCP servers, file access)?
- **Deployment target** — Claude Code subagent, GitHub Copilot agent profile, or a generic system prompt?

Record answers at the top of the goal sheet.

### Phase 1 — Long-Term Goal Setting Sheet → Agent Charter
Fill `templates/01-long-term-goal-sheet.md`. Produce: mission, purpose/why, the persona
the agent must embody, the **four-quadrant** success criteria (value that is
tangible/intangible × for-the-user/for-the-wider-system), an explicit **definition of
done**, **non-goals**, and a **capability audit** (what tools/knowledge the goal requires
vs. what's available — gaps become requirements).

### Phase 2 — Open Window 64 → Capability Decomposition
Fill `templates/02-open-window-64.md`. Put the goal in the center. Choose **8 pillars**.
A strong default set for agentic goals (adapt to the specific goal — do not use blindly):

1. Goal & Scope Mastery
2. Context & Knowledge
3. Planning & Decomposition
4. Tools & Actions
5. Execution Quality
6. Verification & Validation
7. Error Handling & Resilience
8. Communication & Handoff

For each pillar, write **8 concrete actions/behaviors/tools** (64 total). Be specific and
testable ("run the test suite and parse failures", not "be careful"). Optionally validate
completeness with the helper script (see *Tooling*).

### Phase 3 — Routine Check Sheet → Standard Operating Procedure
Fill `templates/03-routine-check-sheet.md`. Select the highest-leverage recurring actions
from the 64 and turn them into the agent's per-run checklist, grouped as **pre-flight**
(before acting), **main loop** (the core cycle), and **post-flight** (before declaring
done). These become explicit numbered steps in the generated system prompt.

### Phase 4 — Daily Diary → Reflection Loop
Fill `templates/04-reflection-diary.md`. Define the short retrospective the generated
agent writes after each run (what it did, what worked, what failed, what to change next
time). Where the platform supports memory/evaluation, wire the reflection into it.

### Phase 5 — Self-analysis → Obstacles, Countermeasures & Autonomy
Fill `templates/05-obstacles-countermeasures.md`. List the top likely failure modes and a
**pre-committed countermeasure** for each. Define the **escalation policy** (when to ask
the human vs. proceed) and the **honesty guardrails** (no fabrication, cite sources, state
uncertainty, never silently substitute resources).

### Phase 6 — Assemble the agent definition
Compose the worksheets into the chosen output artifact using `templates/output/`:
- **Claude Code subagent** → `claude-code-subagent.md` (place at `.claude/agents/<name>.md`)
- **GitHub Copilot agent profile** → `copilot-agent-profile.md` (place at `.github/agents/<name>.agent.md`)
- **Generic system prompt** → `generic-system-prompt.md`

The system prompt body is built from: Charter (Phase 1) → SOP (Phase 3) → key
behaviors/tools from the decomposition (Phase 2) → reflection loop (Phase 4) →
countermeasures & autonomy rules (Phase 5). Attach the filled worksheets as an appendix or
a sibling `*.harada.md` file so the design is auditable.

### Phase 7 — Review & iterate
Show the user (a) a one-paragraph summary of the agent, (b) the OW64 outline, and (c) the
generated agent file. Offer to deepen any single pillar, swap the deployment target, or
generate a companion evaluation rubric from the four-quadrant success criteria.

---

## Tooling (optional helper script)

`scripts/ow64.py` scaffolds, validates, and renders the Open Window 64 mandala. It is pure
Python 3 standard library (no dependencies). Running it needs shell/bash access, which the
host tool will ask you to approve.

```bash
# Emit a blank OW64 file (JSON) to fill in
python3 scripts/ow64.py blank --out my-agent.ow64.json

# Check that all 8 pillars have 8 non-empty actions (exits non-zero if incomplete)
python3 scripts/ow64.py validate my-agent.ow64.json

# Render the 9x9 mandala as a Markdown table + outline
python3 scripts/ow64.py render my-agent.ow64.json --out my-agent.ow64.md
```

---

## Guardrails for you (the architect)

- **Adapt, don't copy.** The 8 default pillars are a starting point. Re-derive them from
  the actual goal when the domain calls for it.
- **Concrete beats aspirational.** Every one of the 64 cells and every SOP step should be
  something an agent can actually *do* or *check*, not a vibe.
- **Right-size it.** A small goal doesn't need all 64 cells filled with filler — depth
  should match the goal's real complexity. Prefer 40 sharp actions over 64 padded ones.
- **Ground the persona in the goal.** "Who must this agent become?" should produce a role
  that materially changes behavior (e.g. "a skeptical security reviewer who assumes every
  input is hostile"), not a generic "helpful assistant."
- **Keep the worksheets.** They are the audit trail. Ship them alongside the agent.

## Resource index

- `references/harada-method.md` — the method itself, its five instruments, origin, sources.
- `references/mapping.md` — deep mapping from each instrument to agent architecture, with examples.
- `templates/01`–`05` — fillable worksheets for each phase.
- `templates/output/` — the three deployable output formats.
- `scripts/ow64.py` — scaffold / validate / render the OW64 mandala.
- `examples/example-research-agent.md` — a fully worked example (goal → filled charts → generated agent).
