# Starter skills for Claude Code

Five skills we wrote at NEUKO and use to run a 3-person studio with agents. Each one is a single text file that teaches the agent one job. Copy the folder, restart Claude Code, and they show up as slash commands.

## What's inside

| Skill | What it does | How it starts |
|---|---|---|
| `explainer-script` | Writes a 2-minute on-camera explainer as a beat table (what you say, what's on screen), with a fact-check list, caption and shot list | You type `/explainer-script`, or ask for an explainer script |
| `news-post` | Turns a news story into a carousel or reel plan built on real sources, logos, footage and quotes, with credits and a caption | You type `/news-post`, or ask to turn a story into a post |
| `objective-report-card` | Grades a piece of work against your goal, criterion by criterion, and says what it would take to get an A | You type `/objective-report-card` |
| `deeper` | Written by Austin. Rewrites a prompt into a deeper version of the same task: what an expert would add, the raw material to start from, the tools, and a check that proves it's right | You type `/deeper`, or ask for a deeper version of a prompt |
| `repeat-to-skill` | Looks back over your week, finds tasks you did more than once, and writes the approved ones as new skills | You type `/repeat-to-skill` |

`objective-report-card` and `repeat-to-skill` only run when you type them. The other three can also start on their own when your request matches.

## Before you start

- Claude Code installed and signed in. Check with `claude --version` in a terminal. Install guide: https://code.claude.com/docs/en/setup
- A terminal on macOS or Linux. On Windows, use WSL.
- No API keys. None of these skills call a paid service on their own.

## Install

1. Download or clone this folder.
2. In a terminal, go into the `starter-skills` folder:

   ```bash
   cd path/to/starter-skills
   ```

3. Copy each skill into your personal skills folder:

   ```bash
   mkdir -p ~/.claude/skills
   cp -R explainer-script news-post objective-report-card deeper repeat-to-skill ~/.claude/skills/
   ```

4. Start Claude Code (or restart it if it was open):

   ```bash
   claude
   ```

5. Type `/` and check that the five names appear in the list.

You should see `/deeper`, `/explainer-script`, `/news-post`, `/objective-report-card` and `/repeat-to-skill`. If they're missing, check that each file sits at `~/.claude/skills/<name>/SKILL.md`, one level deep.

To use a skill in one project only, copy it into that project's `.claude/skills/` folder instead.

## First prompts to try

Paste one of these into Claude Code.

**explainer-script**

```
/explainer-script why AI video still can't keep a character consistent. Write it in my voice: short, plain, first person.
```

Expect a 12 to 15 row table of what you say and what's on screen, a list of every claim with its source, a caption, and a shot list.

**news-post**

```
/news-post <paste a link to today's AI or creator news story>
```

Expect the format pick (carousel or reel), a slide-by-slide plan with one real visual and credit per slide, the asset list, and a caption that ends on a question.

**objective-report-card**

```
/objective-report-card My objective: this script makes a creator who has never used agents want to try one this week. Grade the script you just wrote.
```

Expect a table of criteria, each with a grade, the evidence, and what earns an A, then the next steps. Ask it to "do the plan" if you want it to fix the work.

**deeper**

```
/deeper make me a thumbnail for my next video
```

Expect four short answers (the expert move, the raw material, the methods, the outside check) and a rewritten prompt you can paste back in.

**repeat-to-skill** (run it once a week)

```
/repeat-to-skill
```

Expect a table of tasks you repeated this week, each marked new skill or edit. Nothing gets written until you say which ones to keep.

## Make them yours

Each skill is plain text. Open `~/.claude/skills/<name>/SKILL.md` and edit it like any document: change the word count, add your rules ("no stock footage", "always lowercase captions"), or point it at your own style notes. The agent reads the new version next session.

## Other skills we use, from other people

We didn't write these, so we link to them instead of copying them. All are MIT licensed. Credit to the authors.

| Skill | What it does | Author and link |
|---|---|---|
| `grilling` | The agent interviews you in rounds about a plan, with its recommended answer for each question, until nothing is left assumed | Matt Pocock, https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling |
| `writing-for-agents` | How to write a skill file that triggers at the right time and tells the agent when it's done | Matt Pocock, https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents |
| `handoff` | Writes a note so a fresh session can pick up where this one stopped | Matt Pocock, https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff |
| `unslop` | Edits writing so it stops reading as machine-written | Lauren Tan (poteto), pstack: https://github.com/cursor/plugins/tree/main/harness/pstack/claude-code/skills/unslop |
| `sharpen` | Thinks like an expert about the task, then does it | Lauren Tan (poteto), pstack: https://github.com/cursor/plugins/tree/main/harness/pstack/claude-code/skills/sharpen |
| `automate-me` | Turns your working habits into a personal skill by mining your recent chats | Lauren Tan (poteto), pstack: https://github.com/cursor/plugins/tree/main/harness/pstack/claude-code/skills/automate-me |
