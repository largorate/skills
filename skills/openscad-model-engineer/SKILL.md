---
name: openscad-model-engineer
description: Create, revise, debug, review, and prepare generic OpenSCAD models for reliable preview, render, STL export, and 3D printing. Use whenever a task involves writing or changing .scad files; converting a sketch, concept, dimensions, or reference image into parametric geometry; diagnosing OpenSCAD warnings or broken booleans; improving printability, fit, modularity, or export workflows; or auditing OpenSCAD code for robust CSG geometry.
license: MIT
---

# OpenSCAD Model Engineer

Create models that are parameterized, understandable, renderable, and practical to fabricate. Do not treat a visually plausible preview as proof that an OpenSCAD model is correct or printable.

Use this skill for new designs, focused changes, code review, debugging, print preparation, and export setup. It applies to generic OpenSCAD projects and does not assume a particular model, repository, library, printer, or slicer.

## Core principles

1. **Model a family of parts, not one accidental shape.** Put meaningful adjustable dimensions at the top of the model and derive related values from them.
2. **Separate the concern layers.** Keep configuration, derived dimensions, reusable geometry, assembly, and export routing distinct.
3. **Prefer simple, robust CSG.** Use deliberate overlap for unions and cutters that extend past the body. Avoid faces that merely touch.
4. **Design for fabrication intentionally.** Name clearance, wall thickness, minimum feature, and fit parameters. Do not hide print assumptions in magic numbers.
5. **Validate with the real engine.** Preview is useful; a CGAL render and representative STL exports are stronger evidence.
6. **State uncertainty honestly.** If a dimension, material, printer, or assembly method is unknown, choose a conservative default and identify it as an assumption.

## Required workflow

### 1. Understand the request before changing geometry

Extract or infer:

- the object's purpose and loading conditions
- real-world dimensions, units, and scale
- required interfaces: holes, mating parts, fasteners, electronics, liquids, moving parts, or mounting surfaces
- material and printing process, if known
- visual requirements versus functional requirements
- whether the result is an assembly, a single print, or multiple exported parts

Read the existing model before editing. Locate configuration variables, module calls, includes, export selectors, and any shared constants. Preserve public module names and call signatures unless a rename is explicitly requested.

Do not stop for non-critical missing details. Use a practical default, expose it as a parameter, and describe the assumption in the handoff. Ask only when a decision materially changes safety, geometry, cost, or the intended behavior.

### 2. Choose a maintainable model architecture

For a small independent part, one file may be enough:

```scad
// Configuration
plate_length = 80;
plate_width = 40;
plate_height = 5;

// Derived dimensions
mount_hole_r = 2.2;

// Assembly
mounting_plate();

module mounting_plate() {
    difference() {
        cube([plate_length, plate_width, plate_height], center = true);
        mounting_holes();
    }
}

module mounting_holes() {
    for (x = [-25, 25]) {
        translate([x, 0, 0]) {
            cylinder(h = plate_height + 2, r = mount_hole_r, center = true, $fn = 24);
        }
    }
}
```

For a multi-part design, prefer:

```text
project/
├── const.scad
├── module_utils.scad
├── module_base.scad
├── module_feature.scad
└── assembly.scad
```

Use `include <...>` for files that intentionally share variables and module definitions. Use `use <...>` only when importing modules/functions without variable side effects. Do not mix these modes casually.

Read `references/parametric-architecture.md` before organizing a multi-file model.

### 3. Build solid geometry before decorative geometry

Implement in this order:

1. primary envelope and mounting/reference surfaces
2. functional interfaces and internal clearances
3. structural reinforcement, ribs, bosses, and joints
4. print-specific details such as bridges, chamfers, or support-free angles
5. optional visual detail, labels, textures, and presentation-only geometry

At every stage, keep the part usable with optional presentation layers disabled. Decorative geometry must never conceal an unverified mechanical conflict.

### 4. Use reliable transformations and booleans

Write transformations in a readable sequence. A nested transformation acts inside-out: the innermost object is transformed first. Split long chains into separate indented blocks when that makes local coordinates obvious.

Prefer:

```scad
difference() {
    body();

    translate([0, 0, -0.1]) {
        cylinder(h = body_height + 0.2, r = hole_r, $fn = 32);
    }
}
```

over equal-height cutters that leave coincident faces. Add a named `boolean_overlap` or `epsilon` parameter instead of repeatedly writing arbitrary offsets.

When connecting two solids, overlap them by a small, intentional distance. Do not rely on a point, edge, or exact planar contact to make a manifold union.

Read `references/geometry-and-printability.md` before creating complex booleans, organic branches, hollow channels, snap fits, sockets, or split assemblies.

### 5. Make printability an explicit design layer

For every print-oriented model:

- identify the intended print orientation
- ensure the selected export has a sensible Z=0 contact surface
- name the clearance used by mating parts
- check unsupported overhangs, bridges, thin walls, and fragile features
- split oversized or support-heavy shapes at functional seams
- provide keys, pins, sockets, screws, or other registration features for multi-part assemblies
- distinguish structural joints from display-only alignment aids

Default clearances are printer- and material-dependent. Use a named parameter and document it; do not claim a universal value. For a first FDM prototype, a configurable radial clearance around `0.2` to `0.35 mm` is often a reasonable starting point, but it must be test-printed for the actual printer and material.

### 6. Validate progressively

Use the smallest relevant validation after each meaningful change:

```powershell
# Syntax/CSG smoke output
openscad -o output.csg "assembly.scad"

# Render representative printable part
openscad -o part.stl -D 'part="base"' "assembly.scad"

# Render the complete assembly when practical
openscad -o assembly.stl "assembly.scad"
```

Use a selector or `-D` value to validate each exported part route, not only the default assembly. Treat OpenSCAD warnings as evidence to investigate, especially warnings about undefined operations, non-finite values, invalid polygons, or objects with no top-level geometry.

If OpenSCAD CLI is unavailable:

1. verify file paths and include/use references
2. check selector strings and module names
3. inspect balanced delimiters and all changed transformations
4. review the model in the OpenSCAD GUI if available
5. report that no CLI render or STL validation was performed

Never claim that an STL is valid if it was not generated and inspected.

Read `references/validation-and-delivery.md` for commands, diagnosis, and handoff criteria.

### 7. Deliver a practical handoff

Report:

- files created or changed
- the main parameters users should adjust
- assembly and print orientation expectations
- which export selector(s) produce each print part
- validation performed and its result
- remaining fabrication risks, including tolerance or support assumptions

Keep the final response concise unless the user asks for design rationale or detailed fabrication instructions.

## Revision and debugging workflow

When modifying an existing model:

1. reproduce the issue with the smallest selector or module that exposes it
2. trace the geometry back to the controlling parameters and transformations
3. fix the root cause rather than covering a gap with visual-only geometry
4. update dependent dimensions, mating clearances, and export routes together
5. validate both the changed part and the complete assembly if interfaces changed

For missing geometry, check whether the object is actually called, whether a `difference()` removes it, whether the cutter intersects it, and whether a transformation moved it outside the view.

For broken joins, check world-space positions, not just local coordinates. Verify that male/female parts use one source of truth for their nominal dimensions and a named clearance for the fit.

For slow renders, reduce unnecessary `$fn`, remove decorative detail from print paths, simplify deeply nested booleans, and use low-resolution preview controls. Do not lower precision globally when it would compromise critical circular fits or visible surfaces.

## Modeling rules

- Use millimeters unless the project explicitly uses another unit.
- Put user-adjustable parameters before derived values and modules.
- Use explicit, configurable `$fn`; select it by feature purpose rather than setting it excessively high.
- Use curly braces for control flow and transformation blocks.
- Prefer named modules over duplicated geometry.
- Use functions for deterministic calculations and vector operations.
- Keep cutter geometry slightly larger than the body it removes.
- Avoid zero-thickness features, exact tangent unions, and hidden unsupported fragments.
- Keep preview-only colors and labels optional; they should not affect exported solid geometry.
- Do not add third-party libraries unless the project already uses them or the user requests one.
- Do not fabricate engineering certification, load ratings, waterproofness, food safety, pressure ratings, or safety claims.

## Resource map

- `references/parametric-architecture.md`: scalable file layout, parameter design, coordinate systems, modules, and assemblies.
- `references/geometry-and-printability.md`: robust CSG, manifold solids, tolerances, split parts, joints, and print-oriented geometry.
- `references/validation-and-delivery.md`: OpenSCAD CLI commands, warning diagnosis, export routing, and handoff checklist.
