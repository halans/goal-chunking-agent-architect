# Routine Check Sheet → Standard Operating Procedure

> Pull the highest-leverage recurring items from the 64 actions and turn them into the
> agent's per-run checklist. This becomes the "Operating procedure" section of the prompt.

## Pre-flight (before taking any action)
1. _Restate the goal and confirm success criteria._
2. _Load required context (files/docs/state) — list which._
3. _Check preconditions (tools available, resources exist)._
4. _State the plan before acting._

## Main loop (the core act → observe → adjust cycle)
1. _Take the next planned action using the right tool._
2. _Observe the result; compare against expectation._
3. _Adjust the plan if reality differs._
4. _Repeat until the definition of done is in reach._

## Post-flight (before declaring "done")
1. _Run the verification checks (from Pillar 6)._
2. _Self-review against the Definition of Done and the four-quadrant criteria._
3. _Prepare the handoff/report (from Pillar 8)._
4. _Write the reflection entry (see template 04)._

## Invariants (checked every run, no exceptions)
- _e.g. never perform a destructive action without confirmation_
- _e.g. always cite the source file/line for any claim_
