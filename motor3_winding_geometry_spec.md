# Motor 3-Tooth Winding — Geometry Spec

## Model coordinate system

- Shaft axis: Z
- Front / commutator side: +Z
- Back side: -Z
- Rotor center: `(0, -0.35, 0)`
- Three tooth centerlines: `90°`, `210°`, `330°`

## Named dimensions

| Name | Value | Meaning |
|---|---:|---|
| `CORE_R` | 0.42 | hub radius |
| `TOOTH_R0` | 0.45 | inner tooth edge |
| `TOOTH_R1` | 1.28 | outer tooth edge |
| `TOOTH_W` | 0.58 | tangential tooth width |
| `HALF_Z` | 0.68 | half length of lamination stack |
| `COMM_Z` | 1.08 | commutator plane |
| `COMM_R` | 0.50 | commutator contact radius |
| `WIRE_GAP` | 0.075 | teaching separation between turns |

Checks encoded in Python:

- `TOOTH_R0 > CORE_R`
- `TOOTH_R1 > TOOTH_R0`
- `COMM_Z > HALF_Z`
- every coil has the same turn count
- commutator sequence closes exactly `1→2→3→1`
- every turn is a point chain with front/back Z values exactly `+HALF_Z/-HALF_Z`

## One-turn path, local tooth coordinates

`bar_i → front-left → back-left → back-right → front-right → bar_j`

The four tooth corners are derived from radial unit vector `u`, tangential unit vector `v`,
the tooth radial center, `TOOTH_W/2`, and `±HALF_Z`. No freehand wire shortcut is allowed.

## Camera proving shots

| Claim | Shot |
|---|---|
| front and back segments are different | 3/4 view, fixed camera |
| all three teeth are 120° apart | end-on view down +Z |
| final circuit closes | end-on view + fixed triangle HUD |
| commutator changes active coils | end-on motor section with stationary brushes |

