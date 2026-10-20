# NEUKO agent skills and creator kits

NEUKO is 3 people with no engineers. Our AI characters and series have passed 100M views, and this repo holds the files behind our learning series so you can copy how we work.

Each folder is one workflow. Open its `README.md` for the steps.

## I want to...

| I want to... | Folder |
|---|---|
| Pick which video model to use for each kind of shot, and test new ones | [`pick-a-video-model/`](pick-a-video-model/) |
| Run a small studio with agents, starting with 5 Claude Code skills | [`starter-skills/`](starter-skills/) |
| Keep my character looking the same in every image | [`train-a-character-lora/`](train-a-character-lora/) |
| Know what a shot or an episode costs before I generate it | [`price-a-shot/`](price-a-shot/) |
| Post a story as numbered parts instead of re-uploading clips | [`numbered-parts/`](numbered-parts/) |
| Let fans remix my character and turn their work into marketing | [`models-as-memes/`](models-as-memes/) |

`models-as-memes/` links to `train-a-character-lora/` for the training step. If you copy one folder out of this repo, copy both.

## Install the skills into Claude Code

The folders in `starter-skills/` are Claude Code skills. The other folders are guides, templates and scripts that you open and follow.

1. Install Claude Code and sign in. To check, run `claude --version`. The setup guide is at https://code.claude.com/docs/en/setup.
2. Clone this repo:

   ```bash
   git clone https://github.com/NeukoAI/agent-skills.git
   cd agent-skills/starter-skills
   ```

3. Copy the skills into your personal skills folder:

   ```bash
   mkdir -p ~/.claude/skills
   cp -R explainer-script news-post objective-report-card deeper repeat-to-skill ~/.claude/skills/
   ```

4. Start or restart Claude Code with `claude`, then type `/`. You should see `/deeper`, `/explainer-script`, `/news-post`, `/objective-report-card` and `/repeat-to-skill`.

To use a skill in one project only, copy it into that project's `.claude/skills/` folder instead. [`starter-skills/README.md`](starter-skills/README.md) has a first prompt to try for each skill.

## Skills we use from other people

We didn't write these, so we link to them instead of copying them. All are MIT licensed. Credit goes to their authors.

| Skill | What it does | Author and link |
|---|---|---|
| `grilling` | Interviews you in rounds about a plan until nothing is left assumed | Matt Pocock, https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling |
| `writing-for-agents` | Shows how to write a skill file that triggers at the right time | Matt Pocock, https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents |
| `handoff` | Writes a note so a fresh session can pick up where this one stopped | Matt Pocock, https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff |
| `unslop` | Edits writing so it stops reading as machine-written | Lauren Tan (poteto), https://github.com/cursor/plugins/tree/main/harness/pstack/claude-code/skills/unslop |
| `sharpen` | Works out how an expert would approach the task, then does it | Lauren Tan (poteto), https://github.com/cursor/plugins/tree/main/harness/pstack/claude-code/skills/sharpen |
| `automate-me` | Mines your recent chats and turns your habits into a personal skill | Lauren Tan (poteto), https://github.com/cursor/plugins/tree/main/harness/pstack/claude-code/skills/automate-me |

## Archive

Skills we no longer maintain are in [`archive/`](archive/), each with a note on why.

## License

MIT
