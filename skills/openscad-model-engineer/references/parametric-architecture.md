# Parametric OpenSCAD Architecture

## Purpose

Use this reference when deciding how an OpenSCAD model should be organized, parameterized, and assembled. Good architecture makes a change predictable: changing one public dimension updates the related geometry without a manual hunt for duplicate numbers.

## Start with a parameter hierarchy

Organize values in this order:

1. **User-adjustable inputs**: dimensions, counts, material-fit allowances, quality settings, feature toggles, and export selector.
2. **Derived values**: radii from diameters, offsets from wall thickness, centers, pitch, and dimensions computed from inputs.
3. **Geometry modules**: named solids, cutters, repeated features, and assemblies.
4. **Top-level router**: the selected assembly or export part.

Example:

```scad
// User-adjustable inputs
outer_diameter = 60;
wall_thickness = 2.4;
height = 30;
clearance = 0.25;

// Derived values
outer_r = outer_diameter / 2;
inner_r = outer_r - wall_thickness;
lid_socket_r = inner_r + clearance;

// Top-level entry point
container();
```

Do not repeat `60`, `2.4`, or `30` inside modules after declaring them. If a repeated literal has intentional meaning, name it.

## Distinguish nominal dimensions from manufacturing allowances

Every fit has at least two dimensions:

- **nominal geometry**: the intended design diameter, width, or pitch
- **manufacturing allowance**: clearance, interference, shrink compensation, chamfer, or lead-in

Keep them separate:

```scad
pin_diameter = 6;
radial_clearance = 0.25;
pin_r = pin_diameter / 2;
socket_r = pin_r + radial_clearance;
```

Avoid embedding the allowance into the nominal dimension. A future user should be able to tune only `radial_clearance` without reinterpreting the entire model.

## Use modules as meaningful nouns

Modules should represent a meaningful physical or construction unit:

- `housing()`
- `mounting_holes()`
- `lid()`
- `hinge_pin()`
- `connector_socket()`
- `assembly()`

Avoid modules that only hide a single transformation unless that transformation has a stable semantic role.

Give module parameters useful names and defaults when the geometry is reusable:

```scad
module connector_socket(
    radius,
    depth,
    clearance = 0.25,
    lead_in = 0.6
) {
    // Geometry here.
}
```

Preserve public module names and argument order in an existing project unless a breaking change is requested.

## Keep coordinate systems explicit

Choose and document a coordinate convention:

- Z is usually vertical and the print-bed normal.
- Center symmetric parts around X/Y origin when it simplifies radial patterns.
- Put a part's natural reference surface at Z=0 for direct export where practical.
- For assemblies, choose one root coordinate system and locate children from named reference points.

Use points and vector helpers for complex assemblies:

```scad
function v_add(a, b) = [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
function v_sub(a, b) = [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
function v_len(v) = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
```

Use named points instead of scattering coordinate triples:

```scad
mount_center = [0, 0, base_height];
left_hole = [-hole_spacing / 2, 0, 0];
right_hole = [hole_spacing / 2, 0, 0];
```

## Multi-file layout

Use a constants file plus module files when a model has multiple independently meaningful parts or shared interfaces:

```text
project/
├── const.scad
├── module_utils.scad
├── module_base.scad
├── module_lid.scad
├── module_join.scad
└── assembly.scad
```

Recommended responsibilities:

- `const.scad`: inputs, derived values, named interface dimensions, quality controls
- `module_utils.scad`: vector math, common profiles, geometry helpers
- `module_<part>.scad`: one physical feature family per file
- `assembly.scad`: includes modules, defines assembly/exploded view, and routes exports

Use `include <file.scad>` when the included file needs values declared by the caller or contributes variables/modules. Use `use <file.scad>` when only imported modules/functions are wanted and its top-level variables must not leak into the current file.

Avoid circular includes and top-level geometry in module files. A module file should generally declare definitions; the assembly file should decide what is rendered.

## Export routers

For a multi-part printable model, keep one source file and route exports by an explicit selector:

```scad
part = "assembly";

if (part == "assembly") {
    full_assembly();
} else if (part == "base") {
    print_base();
} else if (part == "lid") {
    print_lid();
} else {
    echo(str("Unknown part: ", part));
    full_assembly();
}
```

Every selector should produce only the intended printable solid, positioned for export. Use direct print modules if the assembly orientation is not printer-friendly:

```scad
module print_lid() {
    rotate([180, 0, 0]) {
        translate([0, 0, -lid_height]) {
            lid();
        }
    }
}
```

Do not rely on a slicer user to discover a hidden orientation requirement.

## Assemblies and exploded views

Keep a complete assembly for spatial validation, but do not use it as the only export path. An exploded view can clarify interfaces:

```scad
module exploded_view() {
    translate([-60, 0, 0]) {
        base();
    }
    translate([60, 0, 0]) {
        lid();
    }
}
```

Exploded views are presentation aids. They do not prove that mating parts fit. Validate the assembled interface at nominal positions and export the individual parts separately.
