# Stitch Validation Schema

The validator checks stitch arithmetic. It does not prove that a physical object will have the desired artistic shape.

## File structure

```json
{
  "parts": [
    {
      "name": "Head",
      "initial_stitches": 0,
      "rounds": [
        {
          "label": "R1",
          "ops": [{"type": "mr", "count": 6}],
          "expected": 6
        },
        {
          "label": "R2",
          "ops": [
            {"repeat": 6, "sequence": [{"type": "inc"}]}
          ],
          "expected": 12
        }
      ]
    }
  ],
  "symmetry_groups": [["Arm", "Arm Copy"]]
}
```

## Supported operations

Count defaults to 1.

| Type | Consumes | Produces | Meaning |
|---|---:|---:|---|
| `sc` | 1 | 1 | single crochet |
| `hdc` | 1 | 1 | half double crochet |
| `dc` | 1 | 1 | double crochet |
| `tr` | 1 | 1 | treble crochet |
| `slst` | 1 | 1 | slip stitch counted as a stitch |
| `inc` | 1 | 2 | two stitches in one stitch |
| `inc3` | 1 | 3 | three stitches in one stitch |
| `dec` | 2 | 1 | two stitches combined to one |
| `dec3` | 3 | 1 | three stitches combined to one |
| `skip` | 1 | 0 | intentionally skip an existing stitch |
| `mr` | 0 | count | foundation stitches made into magic ring |
| `foundation` | 0 | count | generic foundation that creates countable working stitches |
| `custom` | explicit | explicit | manually supply `consume` and `produce` |

Examples:

```json
{"type": "sc", "count": 5}
{"type": "dec", "count": 3}
{"repeat": 6, "sequence": [{"type": "sc", "count": 2}, {"type": "inc"}]}
{"type": "custom", "consume": 4, "produce": 5}
```

For a normal full round, consumed stitches must equal the previous round count. The resulting produced stitches must equal `expected`.

## Partial or unconventional rounds

Set `"allow_partial": true` on a round only when it intentionally does not consume the entire previous round. Use this sparingly and explain the construction in the published pattern.

For turning chains, surface crochet, chain spaces, or other actions that do not map cleanly to countable working stitches, either omit the non-counting action from `ops` or use `custom` with carefully chosen consume/produce values.

## Symmetry groups

A symmetry group compares the resulting stitch-count sequence of named parts. Use it for parts that should be numerically identical. Do not use it for deliberately mirrored shaping that has identical totals but different stitch positions unless count-sequence equivalence is still useful.

## Exit status

- `0`: no validation errors.
- `1`: one or more validation errors.
- Warnings do not change the exit status.
