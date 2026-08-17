---
name: amigurumi-pattern-designer
description: Design, audit, revise, scale, and localize original crochet amigurumi patterns for plush animals, dolls, characters, toys, and other stuffed 3D forms. Use when ChatGPT must turn a concept, sketch, reference image, size target, or existing user-owned draft into a crochet pattern; calculate or verify round-by-round stitch counts; plan shaping, symmetry, assembly, color changes, or placement; troubleshoot a pattern; adapt difficulty or size; or translate/localize crochet instructions, especially between US English, UK English, and Danish terminology.
---

# Amigurumi Pattern Designer

Create technically coherent amigurumi patterns, not merely plausible-looking prose. Treat stitch counts, shape construction, assembly order, and localization as separate layers. Validate the construction before translating it.

## Core workflow

1. Establish the design brief.
   - Capture subject, target finished size, visual proportions, yarn/fiber, hook, gauge if known, difficulty, color palette, construction preferences, and output language/terminology.
   - If non-critical details are missing, choose conservative defaults and label them as assumptions instead of blocking progress.
   - If a reference image is supplied, infer major shapes and proportions from it, but call out hidden or ambiguous construction choices.

2. Decompose the design into crochetable forms.
   - Break the model into head, body, limbs, ears, muzzle, tail, accessories, or other parts.
   - For each part, choose a construction primitive such as sphere/ellipsoid, tapered cylinder, cone, flattened oval, tube, disk, cup, or shaped flat piece.
   - Decide which parts are crocheted continuously, separately and sewn, or joined as-you-go.
   - Read `references/construction-and-qa.md` for shaping heuristics, proportional planning, placement, assembly, and QA rules.

3. Build the stitch plan before polishing prose.
   - Default to US crochet semantics internally: `sc`, `hdc`, `dc`, `tr`, `inc`, `dec`, regardless of final output language.
   - Keep a round ledger for every shaped part: previous stitch count, operation sequence, resulting stitch count, and purpose of the round.
   - Prefer deterministic, countable operations. Avoid vague instructions such as "increase evenly" unless the exact distribution is also stated.
   - Stagger increases/decreases when a visibly polygonal shape is undesirable.

4. Validate all countable parts.
   - Encode shaped rounds in the JSON format documented in `references/validation-schema.md`.
   - Run `python scripts/validate_pattern.py <validation.json>`.
   - Fix every error before publishing the pattern. Review warnings rather than automatically ignoring them.
   - Use symmetry groups for paired parts when the left/right construction should match.
   - Do not claim a pattern is validated if the validator was not run or if unvalidated custom shaping remains.

5. Render the pattern in the requested format.
   - Follow `references/pattern-format.md` unless the user requests another structure.
   - Give stitch totals at the end of every countable round/row.
   - Explain special stitches before first use.
   - Separate crochet instructions from stuffing, positioning, embroidery, and assembly directions.
   - Include explicit placement references using rounds/rows and stitch positions where practical.

6. Localize only after the master construction is stable.
   - Read `references/localization.md` when the requested output is not US English, when translating an existing pattern, or when terminology is ambiguous.
   - Preserve stitch semantics and numeric counts exactly during translation.
   - For Danish, use the `da-DK` profile in that reference and print a localized abbreviation key in the finished pattern.
   - For unsupported languages, establish a glossary first and state which crochet convention is being used.

7. Perform final QA.
   - Recheck stitch totals, round references, color changes, mirrored/paired parts, stuffing timing, closing instructions, and assembly placement.
   - Check that the written repeat syntax expands to the validated operation sequence.
   - Check that the materials list matches every item used later.
   - Flag safety-sensitive choices for items intended for small children; prefer embroidered facial features over detachable small components when appropriate.

## Pattern design rules

- Prioritize structural correctness over decorative detail.
- Keep one semantic source of truth for stitch operations. Translation must never alter the math.
- State whether rounds are continuous spirals or joined rounds.
- Mark whether turning chains count as stitches.
- State whether increases/decreases are standard or invisible.
- When gauge is unknown, describe final dimensions as estimates and explain that yarn, hook, tension, and stuffing change size.
- When scaling, prefer recalculating geometry and placement rather than multiplying every round mechanically.
- For paired limbs/ears, either use one shared pattern twice or validate both as a symmetry group.
- When color changes occur mid-round, ensure the segment counts sum to the round total.
- Do not reconstruct or imitate a paid/commercial pattern line-by-line from its title, photograph, or sparse excerpt. Create an original construction from requested visual traits instead. It is fine to transform, audit, or localize a pattern the user provides and has permission to use.

## Editing and troubleshooting existing patterns

When the user supplies a draft pattern:

1. Preserve the user's intended shape and terminology unless asked to redesign it.
2. Extract each round into a stitch-count ledger.
3. Validate count transitions with the bundled script where possible.
4. Identify the earliest inconsistent round; later errors may be consequences rather than independent mistakes.
5. Propose the smallest correction that restores the intended count and repeat rhythm.
6. If the user asks for a clean rewrite, regenerate the full affected part so stale counts do not remain.

## Resource map

- `references/construction-and-qa.md`: shaping, geometry heuristics, sizing, placement, assembly, and quality checks.
- `references/pattern-format.md`: default publication structure and repeat notation.
- `references/localization.md`: localization method plus US English, UK English, and Danish terminology profiles.
- `references/validation-schema.md`: machine-checkable stitch-count schema and supported operations.
- `scripts/validate_pattern.py`: deterministic round-count and symmetry validator.
