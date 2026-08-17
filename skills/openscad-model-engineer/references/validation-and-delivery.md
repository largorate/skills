# Validation and Delivery

## Validation levels

Use the strongest relevant level available. Each level catches different defects.

| Level | Method | What it establishes |
| --- | --- | --- |
| Source inspection | Review parameters, transforms, includes, and selectors | Obvious logic, reference, and structural issues |
| OpenSCAD preview | Open in GUI or export CSG | Parse and preview-level geometry |
| CGAL render | Export STL or render in OpenSCAD | Boolean evaluation and final solid generation |
| Slicer inspection | Load STL in target slicer | Orientation, supports, thin walls, and toolpath plausibility |
| Test print | Print fit coupon or critical feature | Actual tolerances and material behavior |

Do not confuse one level with another. A successful preview does not guarantee a printable STL, and a valid STL does not guarantee a successful mechanical fit.

## OpenSCAD CLI commands

Run commands from the project directory and quote paths containing spaces:

```powershell
# Preview-oriented CSG smoke export
openscad -o output.csg "assembly.scad"

# Export the default top-level result as STL
openscad -o assembly.stl "assembly.scad"

# Export a selected part when the model supports a selector
openscad -o lid.stl -D 'part="lid"' "assembly.scad"

# Reduce render detail when the model exposes a quality setting
openscad -o base.stl -D 'part="base"' -D 'detail_mode="print"' "assembly.scad"
```

Keep exports out of source directories unless the project convention says otherwise. Do not commit generated STL, CSG, PNG, or temporary render artifacts unless the user explicitly requests them.

## Validate export routers systematically

If a model has an export selector, compile all defined routes:

1. assembly
2. exploded/presentation view, if present
3. each printable body
4. each repeatable or indexed part
5. special presentation geometry only if it is intentionally exported

For each expected print part, verify:

- output exists and is non-empty
- no warnings or errors were emitted
- it contains only the intended geometry
- it rests at or above Z=0 in its export orientation
- it has no accidental presentation overlays

The default assembly often has overlapping parts by design, so export each part separately for fabrication.

## Diagnose common warnings

### Undefined operation or non-finite value

Likely causes:

- division by zero
- indexing outside a vector/list
- undefined variable due to include order
- invalid square root, trigonometric input, or generated range

Fix the first source warning. Later geometry failures may only be consequences.

### Object may not be a valid 2-manifold

Investigate:

- point or edge-only connections
- self-intersections
- zero-thickness walls
- coplanar boolean boundaries
- disconnected internal fragments
- duplicate surfaces from unions

Add intentional overlap, simplify the boolean sequence, or split the geometry into clean solids.

### No top-level geometry

Check:

- the selector value
- spelling of `if`/`else if` branches
- whether the final module is called
- include/use path correctness
- a `difference()` accidentally removing the whole body

### Slow render or CGAL failure

First reduce the problem:

1. export the smallest failing selector
2. disable optional decorative detail
3. lower `$fn` only for non-critical preview geometry
4. isolate nested differences or repeated high-resolution primitives
5. replace fragile tangent intersections with robust overlaps

Avoid declaring success based only on a lower-detail model if the production configuration still fails.

## No-CLI fallback

If OpenSCAD CLI is not installed or unavailable:

1. confirm that file paths, includes, and top-level router references resolve
2. inspect every changed `difference()`, `union()`, and transform sequence
3. check all selector strings against the router
4. inspect the model in the GUI if possible
5. state exactly that CLI/CGAL/STL validation could not be run

Do not install unrelated tools merely to produce a superficial check. Prefer the official OpenSCAD CLI or GUI.

## Delivery checklist

Before completing work, confirm:

- [ ] User-adjustable parameters are grouped and named.
- [ ] Derived values replace duplicated dimensions.
- [ ] Every public module and export selector remains available unless intentionally changed.
- [ ] Male and female interfaces share a nominal source of truth and named clearance.
- [ ] Cutters extend beyond the bodies they subtract.
- [ ] Structural joins have volume overlap and adequate reinforcement.
- [ ] Printable parts have explicit export routes and sensible orientations.
- [ ] Presentation-only geometry is disabled or separated from print exports.
- [ ] Representative CSG/STL renders passed, or unavailable validation is disclosed.
- [ ] The handoff explains key parameters, print/assembly expectations, and remaining risks.

## Handoff wording

A concise but useful model handoff identifies:

```text
Changed: assembly.scad and module_lid.scad.
Adjust: clearance, wall_thickness, and latch_count at the top of const.scad.
Export: set part to "base" or "lid"; each route is placed for printing.
Assembly: glue the tongue-and-groove seam after confirming the fit coupon.
Validation: rendered base, lid, and assembly to STL with OpenSCAD CLI.
Risk: the latch clearance is a starting value and should be tested on the target printer.
```

Report only validations actually performed. If the part is not safety-rated or material-tested, say so plainly.
