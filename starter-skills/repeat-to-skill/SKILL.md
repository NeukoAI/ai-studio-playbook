---
name: repeat-to-skill
description: Review the last week of work for tasks done more than once, propose a skill for each, and write the ones the user approves as SKILL.md files. Use for /repeat-to-skill, as a weekly habit, or when the user says they keep explaining the same thing to the agent.
disable-model-invocation: true
---

# Repeat to skill

Anything you do twice should become a skill, so the agent stops starting from scratch. This skill finds the repeats and writes them down.

## Steps

1. **Collect the week.** Read what is in reach: Claude Code session history for this user (`~/.claude/projects/*/*.jsonl`, newest first, the last 7 days), the current project's recent files and git log, and any notes the user points you to. Read summaries and the user's own messages first; skim tool output only when needed. Done when you can list the tasks the user asked for this week.
2. **Find repeats.** Group tasks that share a goal and most of their steps, even if the wording differed: "write the caption for this reel" three times is one repeat. Also count corrections the user gave more than once ("no em dashes", "use the real logo"), because those belong in a skill too. Skip one-offs. Done when each repeat has a count and an example from the history.
3. **Check what exists.** List the user's skills (`~/.claude/skills/` and the project's `.claude/skills/`). A repeat that an existing skill already covers becomes an edit to that skill, not a new one. Done when each repeat is marked new or edit.
4. **Propose.** Show a table `| Skill | New or edit | Seen | What it would do | Example |` and ask which to write. Wait for the answer.
5. **Write the approved skills.** One folder per skill with a `SKILL.md`:
   - Frontmatter: `name` (lowercase, hyphens) and a `description` that says what it does and when to use it, in the words the user actually used.
   - A short purpose line, numbered steps, and a "Done when" for each step so the agent knows when to stop.
   - The user's repeated corrections as rules, each with its reason.
   - No API keys, passwords or private paths in the file.
   - Save to `~/.claude/skills/<name>/SKILL.md` for personal skills, or the project's `.claude/skills/` if it only applies there.
6. **Report.** List what you wrote or changed, with paths, and one prompt to try each new skill. Done when the user can try every new skill from that list.

## Rules

- Write only the skills the user approved in step 4.
- Keep each skill to one job. Two jobs means two skills.
- Prefer editing an existing skill over adding a near-duplicate, because two skills for one job confuse the agent.
