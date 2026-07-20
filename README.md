# 🎯 goal-chunking-agent-architect

> Turn a goal into a **deployable agent** by running it through the **Harada Method** — the Japanese self-reliance goal-achievement system.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-6E56CF)](https://code.claude.com/docs/en/skills)
[![Works with Claude Code](https://img.shields.io/badge/Claude%20Code-✓-D97757)](https://code.claude.com/docs/en/skills)
[![Works with GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot%20CLI-✓-24292e)](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)

`goal-chunking-agent-architect` is an **Agent Skill** that teaches your
coding agent to *design other agents well*. Instead of hand-writing a one-off prompt, you point
it at a goal and it runs that goal through the five instruments of the Harada Method, producing
**both** the reasoning worksheets **and** a ready-to-deploy agent definition.

---

## Why the Harada Method?

The Harada Method is a disciplined system for reaching hard goals through small, 
consistent, well-decomposed actions aligned to a clear purpose.

An agent chasing an objective faces the *same* problem a person does: a goal too big to act on
directly, a need to work **reliably rather than heroically**, and a need to recover from
setbacks without giving up. 

## The core idea: five instruments → five parts of an agent

| Harada instrument | What it produces in the agent |
| --- | --- |
| **Long-Term Goal Setting Sheet** | **Agent Charter** — mission, purpose, the persona it must *become*, four-quadrant success criteria, definition of done, capability audit |
| **Open Window 64 (OW64) mandala** | **Capability decomposition** — 1 goal → 8 pillars → **64** concrete behaviors, tools & subtasks |
| **Routine Check Sheet** | **Standard operating procedure** — a pre-flight → main-loop → post-flight checklist run *every* task |
| **Daily Diary** | **Reflection & self-evaluation loop** — a post-run retrospective that feeds memory/evals |
| **Self-analysis & self-reliance** | **Obstacle→countermeasure table + autonomy & honesty rules** |

The philosophy carries over too: **self-reliance** (recover before escalating), **consistency
over intensity** (deterministic guardrails beat one-off effort), and **character + performance
together** (honest, cites sources, serves the user's real goal). The full rationale with worked
examples lives in [`references/mapping.md`](./references/mapping.md).

---

## Quickstart

Clone the repo and drop the skill into your tool's skills directory.

```bash
git clone https://github.com/halans/goal-chunking-agent-architect.git
```

**Claude Code**
```bash
# personal (all projects)
cp -r goal-chunking-agent-architect ~/.claude/skills/
# or project-local
cp -r goal-chunking-agent-architect .claude/skills/
```

**GitHub Copilot CLI** — any of these directories work:
```bash
mkdir -p .github/skills && cp -r goal-chunking-agent-architect .github/skills/   # project
# or personal:  ~/.copilot/skills/   |   or shared:  .agents/skills/
```

> The directory name must stay `goal-chunking-agent-architect` and the entry file must be `SKILL.md`.

## Usage

Invoke it by intent, or directly in Claude Code with `/goal-chunking-agent-architect`:

```text
Use the Harada Method to design an agent that keeps our CHANGELOG.md up to date.
```

The skill walks through seven phases and keeps you in the loop at the start and the end:

| Phase | Harada instrument | Output |
| --- | --- | --- |
| 0 · Intake | — | goal in one sentence, tools, deployment target |
| 1 · Charter | Goal Setting Sheet | mission, persona, success criteria, definition of done |
| 2 · Decompose | Open Window 64 | 8 pillars × 8 actions = 64 behaviors |
| 3 · SOP | Routine Check Sheet | pre-flight / loop / post-flight checklist |
| 4 · Reflect | Daily Diary | post-run self-evaluation loop |
| 5 · Resilience | Self-analysis | obstacle→countermeasure table + autonomy rules |
| 6 · Assemble | — | the deployable agent file |
| 7 · Review | — | summary + OW64 outline + iterate |

### What you get

1. **The reasoning worksheets** (the filled Harada charts) — kept alongside the agent as an audit trail.
2. **A deployable agent definition**, in whichever format you choose:
   - a **Claude Code subagent** → `.claude/agents/<name>.md`
   - a **GitHub Copilot agent profile** → `.github/agents/<name>.agent.md`
   - a **generic system prompt** (portable plain text)

See a full run in [`examples/example-research-agent.md`](./examples/example-research-agent.md).

## The OW64 helper

`scripts/ow64.py` scaffolds, validates, and renders the Open Window 64 mandala. Pure Python 3
standard library — no dependencies.

```bash
python3 scripts/ow64.py blank    --out my.ow64.json          # scaffold 8×8 empty grid
python3 scripts/ow64.py validate my.ow64.json               # check completeness (exit 1 if gaps)
python3 scripts/ow64.py render   my.ow64.json --out my.md    # render the 9×9 mandala
```

OW64 file schema:
```json
{ "goal": "one-line goal",
  "pillars": [ { "theme": "Pillar name", "actions": ["a1", "...", "a8"] } ] }
```

## Repository structure

```
goal-chunking-agent-architect/
├── SKILL.md                      # entry point (frontmatter + workflow)
├── README.md                     # this file
├── LICENSE                       # MIT
├── references/
│   ├── harada-method.md          # the method, its five instruments, origin & sources
│   └── mapping.md                # deep Harada → agent-architecture mapping
├── templates/
│   ├── 01-long-term-goal-sheet.md
│   ├── 02-open-window-64.md
│   ├── 03-routine-check-sheet.md
│   ├── 04-reflection-diary.md
│   ├── 05-obstacles-countermeasures.md
│   └── output/
│       ├── claude-code-subagent.md
│       ├── copilot-agent-profile.md
│       └── generic-system-prompt.md
├── scripts/
│   └── ow64.py                   # scaffold / validate / render the OW64 mandala
└── examples/
    ├── example-research-agent.md
    ├── example-research-agent.ow64.json
    └── example-research-agent.ow64.md
```

## License

[MIT](./LICENSE). The Harada Method is the work of **Takashi Harada / Harada Education
Institute**; this project is an independent, unaffiliated adaptation of its publicly described
principles for the purpose of agent design.

## 🙏 Credits & sources

- The Harada Method — theharadamethod.com, haradato.com, harada-educate.jp, frakxion.com
- Widely reported accounts of Shohei Ohtani's 64-chart
- The Agent Skills open standard — [Claude Code](https://code.claude.com/docs/en/skills) · [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
