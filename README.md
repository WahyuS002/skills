# skills

Personal [Claude Code](https://claude.ai/code) skills — slash commands that extend Claude's behavior for specific workflows.

## What is a skill?

A skill is a `SKILL.md` file that Claude Code loads as a slash command. When you type `/skill-name`, Claude reads the skill's instructions and runs a structured session — asking questions, reading files, writing code — according to the spec you defined.

## Skills

| Skill | Description |
|---|---|
| [`/unvibe`](./unvibe/SKILL.md) | Turn AI-written code into code you actually own. Explain it, reimplement it from scratch, pass the tests. |

## Install

Copy any skill folder into your project's `.claude/skills/` directory:

```bash
cp -r unvibe /path/to/your-project/.claude/skills/
```

Or install globally (available in all projects):

```bash
cp -r unvibe ~/.claude/skills/
```

Then invoke it in Claude Code:

```
/unvibe
```

## Inspiration

Inspired by [Matt Pocock's skills repo](https://github.com/mattpocock/skills).
