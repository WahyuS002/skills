# skills

[![skills.sh](https://skills.sh/b/WahyuS002/skills)](https://skills.sh/WahyuS002/skills)

Public [Claude Code](https://claude.ai/code) skills.

## Skills

| Skill                                | Description                                                                                               |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [`/unvibe`](./skills/unvibe/SKILL.md) | Turn AI-written code into code you actually own. Explain it, reimplement it from scratch, pass the tests. |
| [`/study`](./skills/study/SKILL.md)  | Interactive active-recall learning & note distillation into your personal knowledge base.|
| [`/tldr`](./skills/tldr/SKILL.md)    | Direct, high-signal, zero-fluff technical explanations using BLUF and structured bullet points.           |

## Install

### Recommended

```bash
npx skills@latest add WahyuS002/skills
```

Then run:

```text
/unvibe
/study <topic>
/tldr <file/function/concept>
```

### Manual fallback

Use this if you want to install without `skills.sh`:

```bash
mkdir -p ~/.claude/skills
cp -r skills/unvibe ~/.claude/skills/
```

Inspired by [Matt Pocock's skills repo](https://github.com/mattpocock/skills).
