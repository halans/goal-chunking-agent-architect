# Long-Term Goal Setting Sheet → Agent Charter

> Fill this first. It defines *who the agent is* and *what "done" means*. Everything else
> is derived from it. Replace the prompts in _italics_ with real content.

## 0. Intake (from Phase 0)
- **One-sentence goal:** _What outcome must this agent produce?_
- **Success measured by:** _The observable signal that the goal was met._
- **Environment & tools available:** _Repos, APIs, MCP servers, file access, network, etc._
- **Deployment target:** _Claude Code subagent | GitHub Copilot agent profile | generic system prompt_

## 1. Mission (the goal, concretely)
_State the goal measurably, with any deadline/cadence. e.g. "On each run, ensure every
merged PR since the last release is reflected in CHANGELOG.md, grouped by type."_

## 2. Purpose — why this matters
_Why does the outcome matter, and to whom? This is the context the agent uses for judgment
calls when the instructions run out._

## 3. Persona — who the agent must become
_The role/character that materially changes behavior. Be specific. e.g. "A meticulous
release engineer who distrusts vague commit messages and refuses to guess version bumps."_

## 4. Four-quadrant success criteria
_What good looks like across four kinds of value. These also seed an evaluation rubric._

| | For the user | For the wider system |
| --- | --- | --- |
| **Tangible** | _e.g. correct, complete entries_ | _e.g. clean, conventional git history_ |
| **Intangible** | _e.g. user trusts the changelog_ | _e.g. maintainers trust the automation_ |

## 5. Definition of Done (and Non-Goals)
- **Done when:** _Checklist of conditions that must all be true._
- **Explicitly NOT doing:** _Scope boundaries. What this agent must never attempt._

## 6. Capability audit
_What the goal requires vs. what's available. Gaps become setup requirements._

| Required capability / knowledge | Available? | Gap / requirement |
| --- | --- | --- |
| _e.g. read git history_ | _yes_ | _—_ |
| _e.g. call PR API_ | _no_ | _needs a token / MCP server, or fall back to git log only_ |

## 7. Supporters & handoff
_What/who the agent depends on, and who it reports or escalates to._
