# Robust Geometry and Printability

## Reliable constructive solid geometry

OpenSCAD combines solids with `union()`, `difference()`, and `intersection()`. Robust output depends on real volume overlap, not visual coincidence.

### Use extended cutters

For a through-hole, make the cutter longer than the target:

```scad
epsilon = 0.1;

difference() {
    cube([40, 20, 10], center = true);
    cylinder(h = 10 + 2 * epsilon, r = 3, center = true, $fn = 24);
}
```

Do not use a cutter with exactly the same limits as the target. Coincident surfaces can cause fragile preview or CGAL behavior.

### Overlap unions deliberately

If two solids are intended as one part, overlap them:

```scad
union() {
    cube([20, 20, 5]);
    translate([0, 0, 4.8]) {
        cylinder(h = 10, r = 6, $fn = 32);
    }
}
```

Do not depend on the cylinder beginning exactly at Z=5 to connect it to the cube. Point and edge contacts are especially unsafe for STL export.

### Avoid zero-thickness details

Every printable feature needs volume. Watch for:

- polygons with repeated or collinear points
- `linear_extrude(height = 0)`
- walls that collapse after subtractive operations
- a cutter leaving only a coplanar face
- scaled primitives with a zero scale component
- profile intersections that only touch at a tangent

Use a named `boolean_overlap` or `epsilon` throughout a project.

## Transforms and direction-dependent geometry

OpenSCAD transformations nest inside-out:

```scad
translate([20, 0, 0]) {
    rotate([0, 0, 45]) {
        cube([20, 10, 5], center = true);
    }
}
```

The cube rotates first, then translates. For a feature joining two arbitrary points, create or reuse a vector-aligned cylinder helper rather than guessing Euler angles:

```scad
module cylinder_between(p1, p2, radius, facets = 12) {
    vector = p2 - p1; // Illustrative only: OpenSCAD needs a vector helper.
    // Compute length and an axis-angle rotation before placing the cylinder.
}
```

Test a direction helper using vertical, horizontal, and diagonal cases. Guard against zero-length vectors before dividing by length.

## Fit and tolerance strategy

Name all fit allowances:

```scad
clearance = 0.25;
press_fit_interference = 0.10;
lead_in = 0.6;
```

Use clearance as a radial allowance for cylindrical fits unless the design specifically defines a diametral value. Be explicit in comments or names if needed:

```scad
radial_clearance = 0.25;
socket_r = pin_r + radial_clearance;
```

Practical fit depends on:

- printer calibration
- nozzle width and layer height
- material shrinkage and warping
- part orientation
- filament age and humidity
- slicer compensation settings

For unknown FDM setups, expose the value and recommend a small fit coupon before final production. Do not claim that a single tolerance works for every printer.

## Joints for modular assemblies

Choose a joint based on load, alignment, print orientation, and service requirements:

| Joint | Good for | Main caution |
| --- | --- | --- |
| Cylindrical pin/socket | Alignment and light load | Can rotate unless keyed |
| D-profile or hex pin | Orientation control | Needs generous lead-in and clearance |
| Dovetail | Sliding assembly | Print direction and elephant-foot sensitivity matter |
| Screw boss | Serviceable assemblies | Wall thickness and heat-set insert requirements |
| Tongue and groove | Large panel alignment | Needs anti-rattle clearance |
| Snap fit | Tool-free latching | Material fatigue and print-layer direction |

For a structural branch, arm, or cantilever, do not attach the part with a narrow pin alone. Add a root fillet, tapered flare, gusset, or overlapping collar so load transfers over a meaningful area.

For liquid channels, distinguish:

- a decorative visible line
- a non-watertight routing cue
- a functional sealed fluid path

Functional channels need continuous bores, wall thickness around the channel, a path for trapped material to clear, and a sealing strategy at every modular joint. A geometric channel is not automatically watertight after printing.

## FDM-oriented geometry

Treat the intended print orientation as a model requirement.

Check:

- flat bed-contact surface
- first-layer contact and elephant-foot risk
- unsupported overhangs
- bridge length and direction
- tall slender part stability
- wall count at the chosen nozzle width
- minimum feature size
- support removal access
- strength relative to layer direction

As a conservative starting point for common FDM printing:

- make load-bearing walls at least several extrusion widths
- avoid long horizontal bridges when a chamfer, arch, or split can remove the need
- use 45-degree or gentler self-supporting slopes when the printer/material supports that assumption
- orient tensile loading to avoid layer separation where practical

These are heuristics, not guarantees. Validate against the actual machine and slicer profile.

## Splitting a model for printing

Split only where the assembly can tolerate a seam:

1. choose a naturally hidden or mechanically reinforced plane
2. add registration geometry, not just a flat butt joint
3. leave room for glue, screws, or fasteners when used
4. ensure the separate parts fit the build volume
5. export each part in its intended print orientation
6. print a representative joint before a long print

When a part contains a continuous internal channel, split it so the channel alignment is keyed and can be sealed after assembly. Avoid routing a channel through a press-fit joint without a planned gasket, adhesive, or mechanical seal.

## Presentation geometry versus manufacturing geometry

Colors, labels, arrows, transparent water paths, plant textures, and exploded layouts can improve communication. Keep them optional and separate from the printable body:

```scad
show_presentation = true;

manufacturing_geometry();

if (show_presentation) {
    presentation_overlay();
}
```

Do not let visual overlays mask missing walls, broken joints, or disconnected components. STL export usually receives all top-level geometry unless the router explicitly selects only the manufacturing body.
