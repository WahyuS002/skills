# skills

Public [Claude Code](https://claude.ai/code) skills.

## Skills

| Skill                                      | Description                                                                                               |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [`/unvibe:unvibe`](./unvibe/SKILL.md)      | Turn AI-written code into code you actually own. Explain it, reimplement it from scratch, pass the tests. |

## Install

### Recommended: plugin marketplace

Run these inside Claude Code:

```text
/plugin marketplace add WahyuS002/skills
/plugin install unvibe@wahyu-skills
/reload-plugins
```

Use the plugin namespaced command:

```text
/unvibe:unvibe
```

### Manual fallback

Use this if you prefer the clean `/unvibe` command and do not need plugin updates:

```bash
mkdir -p ~/.claude/skills
cp -r unvibe ~/.claude/skills/
```

Inspired by [Matt Pocock's skills repo](https://github.com/mattpocock/skills).
