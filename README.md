# skills

Public Agent Skills repository for use with [skills.sh](https://skills.sh).

[![skills.sh](https://skills.sh/b/largorate/skills)](https://skills.sh/largorate/skills)

## Available skills

### amigurumi-pattern-designer

Designs, validates, revises, scales, and localizes original crochet amigurumi patterns:

- calculates and validates round-by-round stitch counts
- plans shaping, symmetry, assembly, color changes, and placement
- supports US English, UK English, and Danish crochet terminology

Use this skill when you need a technically coherent plush crochet pattern or want to audit an existing one.

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

### goodnight

Late-night wrap-up automation:

- finishes remaining work
- commits and pushes final changes
- hibernates Windows at the end (`shutdown /h`)
- falls back to timed shutdown when hibernate is unavailable

Use this skill when you want the agent to complete and close down your machine after final success.

### openscad-model-engineer

Creates, revises, debugs, reviews, and prepares generic OpenSCAD models for reliable preview, STL export, and 3D printing:

- structures models with clear parameters, derived values, modules, assemblies, and export routes
- makes CSG operations robust with deliberate overlaps and extended cutters
- designs printable interfaces, tolerances, joints, orientations, and split assemblies
- validates source, OpenSCAD render/export output, and delivery readiness without overstating results

Use this skill whenever an agent needs to create or modify a `.scad` model from a concept, dimensions, sketch, reference image, or an existing draft.

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

Install only the `goodnight` skill:

```bash
npx skills add largorate/skills --skill goodnight
```

Install only the `amigurumi-pattern-designer` skill:

```bash
npx skills add largorate/skills --skill amigurumi-pattern-designer
```

Install only the `openscad-model-engineer` skill:

```bash
npx skills add largorate/skills --skill openscad-model-engineer
```

## Repository layout

```text
skills/
├── amigurumi-pattern-designer/
│   ├── agents/
│   ├── references/
│   ├── scripts/
│   └── SKILL.md
├── goodnight/
│   └── SKILL.md
├── openscad-model-engineer/
│   ├── references/
│   └── SKILL.md
├── thoughts/
│   └── SKILL.md
└── yolocat/
    └── SKILL.md
```

## License

MIT
