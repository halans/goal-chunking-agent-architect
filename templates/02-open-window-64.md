# Open Window 64 (OW64) → Capability Decomposition

> Decompose the goal into 8 pillars × 8 concrete actions = 64. Be specific and testable.
> Keep the machine-readable block (`ow64.json`) in sync if you use `scripts/ow64.py`.

## Center: the goal
**Goal:** _one line — same as Mission in the charter_

## The 8 pillars (adapt from the defaults to fit the goal)
1. **Goal & Scope Mastery**
2. **Context & Knowledge**
3. **Planning & Decomposition**
4. **Tools & Actions**
5. **Execution Quality**
6. **Verification & Validation**
7. **Error Handling & Resilience**
8. **Communication & Handoff**

## The 64 actions
For each pillar list 8 concrete items. Tag each as `[rule]`, `[action]`, `[tool]`, or
`[subagent]` so Phase 6 knows where it belongs in the agent.

### Pillar 1 — Goal & Scope Mastery
- [action] _…_
- [rule] _…_
- _(8 total)_

### Pillar 2 — Context & Knowledge
- [action] _…_
- [tool] _…_
- _(8 total)_

### Pillar 3 — Planning & Decomposition
- _(8 total)_

### Pillar 4 — Tools & Actions
- [tool] _…_
- _(8 total)_

### Pillar 5 — Execution Quality
- _(8 total)_

### Pillar 6 — Verification & Validation
- [action] _…_
- _(8 total)_

### Pillar 7 — Error Handling & Resilience
- [rule] _…_
- _(8 total)_

### Pillar 8 — Communication & Handoff
- _(8 total)_

---

## Machine-readable mirror (for scripts/ow64.py)
Keep this JSON in sync, or generate a blank one with `python3 scripts/ow64.py blank`.

```json
{
  "goal": "one-line goal",
  "pillars": [
    { "theme": "Goal & Scope Mastery",        "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Context & Knowledge",          "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Planning & Decomposition",     "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Tools & Actions",              "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Execution Quality",            "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Verification & Validation",    "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Error Handling & Resilience",  "actions": ["", "", "", "", "", "", "", ""] },
    { "theme": "Communication & Handoff",      "actions": ["", "", "", "", "", "", "", ""] }
  ]
}
```
