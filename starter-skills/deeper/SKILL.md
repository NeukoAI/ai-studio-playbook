---
name: deeper
description: Rewrite a task prompt into a deeper version of the same task, not a bigger one, by naming what a top professional would add, the raw material they would start from, their methods and tools, and an outside check that the result is right. Use for /deeper.
argument-hint: "[prompt or task to deepen]"
---

# Deeper

Task to deepen: $ARGUMENTS

With no arguments, use the task the user most recently asked for in this conversation. If there is none, ask for it.

Deeper means the same goal, the same deliverable and the same scope, done the way an expert would do it. Name the field and what the user is really after, then answer the four questions for this task specifically. Generic answers ("follow best practices", "use reliable sources") add nothing, so each answer names something concrete.

1. **The expert move.** What would a top professional in this field do here that the prompt doesn't ask for? Keep only moves that improve this deliverable. A move that adds a new deliverable is scope growth: list it as optional or leave it out.
2. **The rawest material.** What would they start from instead of what has already been digested: primary data, source files, original footage, transcripts, raw logs, the people involved, rather than summaries, secondhand reports or earlier AI output. Check the workspace for it and say where it lives, or how to get it.
3. **Methods and tools.** Name the specific techniques, standards and tools they would use.
4. **The outside check.** What, other than the model or the user, would show the result is right before it is handed back: a test, a measurement against a baseline, a primary source, a comparison against the best past work, a domain expert's review. Say how to run it and what result counts as a pass. Evidence that only exists after release (audience metrics, sales) goes in as a follow-up with its baseline, not as the done-when, because the agent can't wait for it.

Then rewrite the prompt. It must stand alone, so a fresh agent with no chat history can run it. It keeps the user's goal, voice and the constraints that serve the goal, turns answers 1 to 4 into concrete asks, and ends with the outside check as its done-when. A constraint that works against the goal, and any choice that belongs to the user, becomes an open question in the prompt rather than a decision you make for them.

## Output

- `## Deeper, not bigger`: the field, then the four answers, each as short as it can be while staying specific.
- `## Rewritten prompt`: the new prompt in a fenced block, ready to paste.
- Close with a numbered **What I need from you** section: first, say go to run the rewritten prompt now; then anything only the user can supply (access to raw material, an expert's time, answers to the open questions).

## Done when

Each of the four answers names something concrete, the rewritten prompt asks for the same deliverable as the original, and its outside check can be run before handback and relies on something other than the model's or the user's own judgment.
