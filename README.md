# skills

Public Agent Skills repository for use with [skills.sh](https://skills.sh).

[![skills.sh](https://skills.sh/b/largorate/skills)](https://skills.sh/largorate/skills)

## Available skills

### thoughts

Creates and maintains project thought narratives that capture:

- what changed and why
- what worked and what failed (with exact errors/commands)
- tricky implementation details
- focused review/validation guidance

Use this skill for non-trivial implementation work, bug fixing, refactoring, and research spikes.

### yolocat

High-velocity delivery with a cat-harness workflow:

- commits local progress after each completed prompt
- keeps a running ledger of commit IDs
- avoids pushing intermediate commits
- asks for explicit confirmation before squash + push

Use this skill when you want fast execution with controlled history cleanup at the end.

## Installation

Install all skills from this repository:

```bash
npx skills add largorate/skills
```

List discoverable skills:

```bash
npx skills add largorate/skills --list
```

Install only the `thoughts` skill:

```bash
npx skills add largorate/skills --skill thoughts
```

Install only the `yolocat` skill:

```bash
npx skills add largorate/skills --skill yolocat
```

## Repository layout

```text
skills/
├── thoughts/
│   └── SKILL.md
└── yolocat/
    └── SKILL.md
```

## License

MIT
