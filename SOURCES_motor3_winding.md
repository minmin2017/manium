# Sources — 3-tooth brushed DC motor winding

- ROHM TechWeb, “Construction of Brushed Motors” — a common two-pole / three-slot motor has
  three commutator segments spaced 120° apart; every segment joins one end of two neighboring
  coils; the three coils and segments form a ring network.
  https://techweb.rohm.com/product/motor/motor-types/87/
- Precision Microdrives, “A Short Illustrated Primer On Brushed DC Motors” — a three-pole rotor
  has three windings wired as a triangle (delta) to the three commutator sections; brushes select
  coils in turn as the rotor moves.
  https://www.precisionmicrodrives.com/a-short-illustrated-primer-on-brushed-dc-motors
- Purdue University, “DC Machines and the DC Drive — Commutation” — commutator segments rotate
  with the rotor while brushes remain stationary; commutation redirects armature current as the
  rotor turns.
  https://engineering.purdue.edu/KWPO/animationA/index.html
- Nissan K11 service-manual armature check (mirrored manual page) — adjoining commutator segments
  should have continuity; commutator bar to shaft should not.
  https://manuals.sucatisse.com/k11/el/el-30

The animation deliberately does not prescribe a universal wire gauge or turn count. Those values
depend on the original motor design, target voltage/current, available slot fill, and thermal limits.

