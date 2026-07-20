# Mapping the Harada Method onto agent architecture

This is the intellectual core of the skill: a one-to-one mapping from each Harada
instrument to a concrete part of an agent definition, with the reasoning and worked
examples. When you build an agent, you are effectively *coaching it through the Harada
Method once, up front*, and then freezing the result into its system prompt and operating
procedure.

---

## Instrument 1 — Long-Term Goal Setting Sheet → **Agent Charter**

**Human version:** clarify the goal, why it matters, who you must become, and what value it
creates across four quadrants.

**Agent version:** the top of the system prompt — the agent's identity and contract.

| Goal-sheet field | Becomes | Example |
| --- | --- | --- |
| The goal (measurable, deadline) | The agent's **mission statement** + explicit **definition of done** | "Keep `CHANGELOG.md` accurate: every merged PR is reflected within one run, grouped by type." |
| Purpose / why | The **motivating context** that lets the agent make judgment calls | "Readers rely on the changelog to decide when to upgrade; omissions erode trust." |
| Who you must become | The agent's **persona/role** — chosen to change behavior | "A meticulous release engineer who distrusts vague commit messages." |
| Four-quadrant value | The agent's **success criteria** across dimensions (and a natural eval rubric) | tangible-for-user: correct entries; intangible-for-user: confidence; tangible-for-system: clean git history; intangible-for-system: maintainer trust |
| Current vs. required ability | The **capability audit** → required **tools/knowledge**; gaps become setup requirements | "Needs: git log access, PR API, write access to one file. Gap: no network → use local git only." |
| Supporters / giving back | **Escalation & handoff** relationships — who/what the agent depends on and reports to | "Escalate ambiguous version bumps to the human maintainer." |

**Why it matters for agents:** most weak agents fail here — they get a task but no
*contract*. The charter gives the agent stable identity, judgment criteria, and a crisp
definition of done, which is what lets it act autonomously without drifting.

---

## Instrument 2 — Open Window 64 → **Capability Decomposition**

**Human version:** 1 goal → 8 themes → 64 concrete actions.

**Agent version:** the backbone of the agent's competence. The 8 pillars become the
sections of the operating procedure and the checklist of what "good" requires; the 64
actions become concrete behaviors, tool calls, sub-tasks, or (for a multi-agent workflow)
sub-agents.

**Default 8 pillars for an agentic goal** (adapt per goal):

1. **Goal & Scope Mastery** — restate objective, confirm success criteria, mark boundaries and non-goals.
2. **Context & Knowledge** — locate inputs, read relevant files/docs, load prior state, gather domain facts.
3. **Planning & Decomposition** — order the work, sequence dependencies, choose an approach, timebox.
4. **Tools & Actions** — the concrete capabilities: which tools/APIs/commands, with what arguments and safeguards.
5. **Execution Quality** — the standards for the actual work product (style, correctness, idioms, formatting).
6. **Verification & Validation** — tests, checks, cross-references, and evals that prove the outcome is real.
7. **Error Handling & Resilience** — detect failures, retry, fall back, and avoid destructive actions.
8. **Communication & Handoff** — reporting, citations, questions, and the shape of the final deliverable.

This set intentionally traces the agent loop (understand → contextualize → plan → act →
verify → recover → communicate) plus goal mastery. Learning/reflection is handled by
Instrument 4.

**From 64 cells to agent parts:**
- A cell that is a *rule* ("never force-push") → a guardrail line in the prompt.
- A cell that is an *action* ("run `pytest -q` and parse failures") → an SOP step / tool call.
- A cell that is a *capability* ("query the GitHub PR API") → a required tool/integration.
- A cluster of related cells → a candidate **sub-agent** in a multi-agent workflow.

**Why it matters:** this is the antidote to shallow prompts. Forcing 8×8 coverage surfaces
the boundary conditions and support tasks (the "pick up trash / say thanks" cells in
Ohtani's chart) that separate a robust agent from a demo.

---

## Instrument 3 — Routine Check Sheet → **Standard Operating Procedure (SOP)**

**Human version:** the handful of daily routines you tick off to stay consistent.

**Agent version:** an explicit, ordered checklist the agent runs on **every** task —
the deterministic spine that makes behavior repeatable instead of improvised.

Group the selected high-leverage actions into three phases:
- **Pre-flight** (before acting): confirm understanding, load context, check preconditions, state the plan.
- **Main loop** (the core cycle): the act → observe → adjust cycle, with the tools from Pillar 4.
- **Post-flight** (before "done"): run the Pillar-6 checks, self-review against the definition of done, prepare the handoff.

Render this directly as a numbered "Operating procedure" section in the system prompt.

**Why it matters:** "consistency over intensity" is exactly what you want from an agent. A
written routine turns the best-case behavior into the every-case behavior and is the single
biggest lever on reliability.

---

## Instrument 4 — Daily Diary → **Reflection & Self-Evaluation Loop**

**Human version:** nightly reflection — what worked, what didn't, tomorrow's focus.

**Agent version:** a post-run retrospective step. After finishing (or failing) a task, the
agent writes a short structured note:
- What was the goal and what did I actually do?
- What worked / what failed, and why?
- What will I do differently next time?

Where the runtime supports it, persist this to **memory** or an **evaluation log** so the
improvement compounds across runs. Even without persistence, an in-context reflection step
measurably improves multi-step task quality (it is a structured self-critique).

**Why it matters:** it closes the loop. Agents without reflection repeat the same mistakes;
a diary step is cheap and turns each run into training data for the next.

---

## Instrument 5 — Self-analysis & self-reliance → **Obstacles, Countermeasures & Autonomy rules**

**Human version:** take responsibility, anticipate obstacles, pre-decide countermeasures,
hold the right attitude.

**Agent version:** two things baked into the prompt:

1. **Obstacle → countermeasure table.** Enumerate the most likely failure modes for *this*
   goal and pre-commit a response, so the agent recovers on its own:

   | Likely obstacle | Pre-committed countermeasure |
   | --- | --- |
   | Tool/API returns an error or empty result | Retry once; if still failing, try the documented alternative; only then report the blocker |
   | Required resource (file/ID/channel) not found | **Stop and ask** — never silently substitute a different resource |
   | Ambiguous instruction | Proceed on the most reasonable interpretation for low-risk steps; ask before irreversible ones |

2. **Autonomy & honesty rules** (the "character" layer): recover before escalating; escalate
   only when genuinely blocked or when an action is irreversible; never fabricate; cite
   sources; state uncertainty; serve the user's real goal, not just the literal words.

**Why it matters:** self-reliance is what makes an agent *autonomous* rather than needy,
and the honesty guardrails are what make it *trustworthy*. Together they are the difference
between an agent you can leave running and one you have to babysit.

---

## Putting it together

The generated system prompt is assembled in this order:

```
[Charter]              ← Instrument 1  (identity, mission, definition of done, success criteria)
[Operating procedure]  ← Instrument 3  (pre-flight / loop / post-flight, drawn from Instrument 2)
[Capabilities & rules] ← Instrument 2  (key behaviors, required tools, guardrail rules)
[Reflection]           ← Instrument 4  (post-run retrospective, + memory/eval wiring)
[Obstacles & autonomy] ← Instrument 5  (countermeasures, escalation policy, honesty rules)
[Appendix: worksheets] ← the filled Harada charts, kept for auditability
```

The four-quadrant success criteria (Instrument 1) double as a ready-made **evaluation
rubric** — offer to generate one so the agent can be scored and improved over time.
