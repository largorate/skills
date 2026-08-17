# Crochet Pattern Localization

Localize crochet patterns semantically, not word-for-word. Crochet terminology is convention-dependent, especially between US and UK English.

## Localization procedure

1. Identify the source convention and target locale.
2. Convert source abbreviations into internal semantic stitch names.
3. Preserve all numeric values, repeat structure, stitch consumption/production, part names, round references, and color IDs.
4. Translate prose instructions into natural target-language crochet wording.
5. Render stitch names and abbreviations using the target profile.
6. Print an abbreviation/glossary section in the target language.
7. Recheck every translated round against the validated master counts.

Never translate an abbreviation by visual similarity. For example, US `sc` and UK `dc` are the same stitch semantics but different labels.

## Internal semantic names

Use these concepts internally:

- chain
- slip stitch
- single crochet
- half double crochet
- double crochet
- treble crochet
- increase
- three-stitch increase
- decrease
- three-to-one decrease
- front loop only
- back loop only
- magic ring

## en-US profile

| Semantic stitch | Preferred term | Abbreviation |
|---|---|---|
| chain | chain | ch |
| slip stitch | slip stitch | sl st |
| single crochet | single crochet | sc |
| half double crochet | half double crochet | hdc |
| double crochet | double crochet | dc |
| treble crochet | treble crochet | tr |
| increase in sc | increase | inc |
| decrease in sc | decrease | dec |
| magic ring | magic ring | MR |
| stitch(es) | stitch(es) | st(s) |
| round | round | Rnd / R |
| front loop only | front loop only | FLO |
| back loop only | back loop only | BLO |

## en-GB profile

Be explicit that UK stitch names are being used.

| Semantic stitch | UK term | Common abbreviation |
|---|---|---|
| chain | chain | ch |
| slip stitch | slip stitch | sl st |
| single crochet | double crochet | dc |
| half double crochet | half treble crochet | htr |
| double crochet | treble crochet | tr |
| treble crochet | double treble crochet | dtr |

Keep increases/decreases tied to the underlying stitch, e.g. "dc inc" in UK terminology when the master operation is a single-crochet increase.

## da-DK profile

Use natural Danish crochet language. Danish abbreviations vary somewhat by publisher, so define the chosen abbreviations in every standalone pattern. Prefer the following defaults for this skill:

| Semantic stitch/concept | Danish term | Default abbreviation |
|---|---|---|
| chain | luftmaske | lm |
| slip stitch | kædemaske | km |
| single crochet | fastmaske | fm |
| half double crochet | halvstangmaske | hstgm |
| double crochet | stangmaske | stgm |
| treble crochet | dobbeltstangmaske | dstgm |
| stitch | maske | m |
| round | omgang | omg. |
| increase | udtagning | udt. |
| decrease | indtagning | indt. |
| magic ring | magisk ring | MR |
| front loop only | forreste maskeled | fml |
| back loop only | bagerste maskeled | bml |
| stitch marker | maskemarkør | - |
| yarn over | slå om | - |
| stuff | fyld / fyld med bamsefyld | - |
| fasten off | bryd garnet og træk igennem | - |
| sew on | sy fast | - |
| repeat | gentag | - |

### Danish rendering rules

- Write `6 fm i MR` rather than translating the English word order mechanically.
- For an sc increase, `udt.` means 2 fm in the same stitch. Define this in the abbreviation key. For maximum clarity, write `2 fm i samme m` the first time.
- For an sc decrease, define `indt.` as 2 fm crocheted together. If using an invisible decrease, say so explicitly rather than assuming `indt.` implies it.
- Use `omg.` for rounds and `rk.` only for rows if rows are present.
- Keep final stitch counts in parentheses, e.g. `Omg. 5: (3 fm, udt.) x 6 (30)`.
- Prefer `gentag ... x 6` or parenthesized repeat notation consistently throughout one pattern.
- Use `næste m` for "next stitch" and `i hver m omgangen rundt` for "in each stitch around" where natural.
- Keep technical abbreviations such as MR only when they are defined in the glossary.

### Danish example

Validated semantic master:

`R3: (sc, inc) x 6 (18)`

Danish rendering:

`Omg. 3: (1 fm, udt.) x 6 (18)`

The numeric result remains 18. Translation must not change repeat count or stitch math.

## Other languages

For a locale without a bundled profile:

1. State the target country/locale, not only the language when terminology differs regionally.
2. Build a short glossary mapping internal semantic names to local terms.
3. Ask for or honor the user's preferred publisher/terminology convention if supplied.
4. If an abbreviation is uncertain, use the full stitch name rather than inventing a shorthand.
5. Keep the validated semantic master available so the localized version can be checked against it.
