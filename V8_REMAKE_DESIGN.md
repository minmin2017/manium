# V8 Engine — from one combustion event to smooth crankshaft torque

## Goal

Create a brand-new Manim CE teaching clip in Thai that lets a zero-background viewer answer:

1. What makes the pistons move?
2. How does piston motion become crankshaft rotation?
3. Why does a V8 have two banks and eight cylinders?
4. Why do the cylinders fire one after another instead of together?

The core misconception to defeat is: “eight pistons all explode together.” The aha moment is that one cylinder needs 720 degrees of crank rotation for a four-stroke cycle, while eight staggered power strokes can be spaced every 90 degrees, giving the crankshaft a much smoother stream of torque.

Use a representative 90-degree, cross-plane Ford Coyote-style V8 for the firing-order example. Explicitly label the firing order as an example, not a universal V8 order.

## Verified content facts

- Four strokes: intake, compression, power, exhaust.
- One complete four-stroke cycle requires two crankshaft revolutions (720 degrees).
- During the power stroke, combustion pressure drives the piston down; the connecting rod turns the crankshaft.
- Example Ford Coyote firing order: 1-5-4-8-6-3-7-2.
- Traditional cross-plane V8 crankpins/counterweights appear at 90-degree intervals when viewed down the crank axis. Flat-plane V8s also exist, so do not imply every V8 uses one crank type.

Sources checked by the designer: Briggs & Stratton official four-stroke explanation; Ford Performance official Coyote engine documentation and Ford Media explanation of cross-plane versus flat-plane V8 crankshafts.

## Format and visual language

- One scene class: `V8EngineRemake(SafeThreeDScene)` in `v8_engine_remake.py`.
- 16:9, final cloud render 1080p25, approximately 70–85 seconds.
- Dark navy background. Intake blue/cyan, compression amber, combustion orange/red, exhaust gray, mechanical motion white, active cylinder neon yellow.
- Thai captions in the top zone with `caption_top()`. MathTex remains ASCII-only.
- Use native `Prism`, `Cylinder`, `Dot3D`/flat VMobjects and `arrow3()`/`line3()`; cylinder resolution `(10,10)` or lower. Never use `Arrow3D`, `Line3D`, imported OBJ, or bare `Scene`.
- Solids are opaque in establishing shots, then engine block/head opacity drops to 0.25–0.35 in teaching shots so pistons, rods, valves and crankshaft remain visible.
- Every first appearance of a component gets a short pointer label. Every caption that names a component flashes that exact object in the same beat.
- Camera must lock for explanatory beats. Ambient rotation is allowed only in the opening/closing beauty shot.

## Geometry contract

Coordinate convention:

- Crankshaft axis is world +Y/-Y.
- The two banks open upward from the crank axis, symmetric about the vertical center plane.
- Bank axes are separated by exactly 90 degrees: left cylinder travel direction `normalize((-1,0,1))`, right direction `normalize((1,0,1))`.
- Four throws lie at `y = [-2.25, -0.75, 0.75, 2.25]`.
- Each throw owns one left-bank and one right-bank cylinder: the atomic V pair. Build and reveal one pair first, then replicate four times.
- Crank radius `r = 0.42`, rod length `L = 1.45`, with `L > r` asserted.
- Piston travel uses exact slider-crank displacement, not a sine approximation. The crank pin, rod endpoints and piston center must share the same tracked crank angle.
- Use a single master `ValueTracker` for crank angle and derive every cylinder phase from it.
- Add assertions for bank angle (90 degrees), bank symmetry, throw spacing, rod length, and the eight unique 90-degree firing phases over 720 degrees.

## Shot list — the shot list is the plan

### 1. Hook: eight pistons, one output shaft (0–7 s)

Start on a polished solid engine silhouette at a readable three-quarter view. A slow 1-second orbit establishes 3D, then lock. Explode/fade the block translucent to expose eight pistons, rods and the crankshaft. Title: “V8 ทำงานอย่างไร?” Caption: “8 ลูกสูบไม่ได้ระเบิดพร้อมกัน—มันผลัดกันส่งแรงให้เพลา”.

### 2. Atomic unit: one cylinder makes torque (7–27 s)

Hide the other seven cylinders. Frame one cylinder in a clear side cutaway with intake valve, exhaust valve, spark plug, piston, connecting rod and crank throw all visible. Name components with pointer arrows.

Animate one complete 720-degree cycle as four sequential beats; each must change the model itself, not only text:

- Intake: intake valve opens, piston descends, cyan mixture particles flow through a literal point-by-point intake path into the chamber.
- Compression: both valves close, piston rises, particle cloud visibly compresses and changes cyan → amber.
- Power: spark plug flashes, chamber changes orange/red, pressure arrows push piston down, rod turns crank. Freeze briefly at the strongest lever-arm moment and draw the force-to-torque causal path.
- Exhaust: exhaust valve opens, piston rises, gray particles leave through a literal point-by-point exhaust path.

Alongside, use a compact 720-degree circular timeline split into four equal 180-degree sectors. Highlight the current sector in sync. Caption must state the supporting fact: one cycle equals two crank revolutions.

### 3. Why the V exists: package cylinders around one crank (27–39 s)

Return to one atomic V pair sharing a crank throw. Move camera to the designated proving shot nearly straight down the crankshaft axis (`phi≈88°, theta≈-83°`, tune only if projection check shows a clearer result). Lock camera. Draw two bank-axis lines and a literal 90-degree angle arc. Caption: “สองแถวเอียง 90° ทำให้ 8 สูบวางสั้นและกะทัดรัด”.

Only after the angle is clearly visible, label “Bank L” and “Bank R”. Then pull camera back along the crank axis while replicating the atomic pair at the other three throws. This is a causal reveal, not eight cylinders appearing at once.

### 4. Staggered firing: 720° divided among eight cylinders (39–61 s)

Show the full transparent engine in a fixed three-quarter view where both banks remain distinguishable. Use the representative Ford Coyote numbering and label it clearly. Display `ตัวอย่าง Ford Coyote: 1–5–4–8–6–3–7–2`.

Animate the master crank through 720 degrees. Every 90 degrees:

- exactly one cylinder flashes yellow/red,
- its combustion chamber expands,
- its rod visibly adds a torque pulse to the same crankshaft,
- the corresponding number in the firing-order rail lights up,
- a small pulse is added to a professional torque-vs-crank-angle chart.

Compare a faint single-cylinder pulse train with the denser eight-cylinder aggregate. The chart must have direct labels and a Thai caption explaining the point: eight staggered power strokes reduce the gaps between pushes; do not claim perfectly constant torque.

### 5. Payoff: combustion becomes wheel-driving rotation (61–76 s)

Follow the conserved energy/mechanical path visually: expanding gas → piston force → connecting rod → crankshaft torque → flywheel/output shaft. Use a moving highlight along the actual connected components, never a floating teleport arrow. End on the complete solid V8 running smoothly, with subtle repeated cylinder flashes and the output shaft rotating.

Final summary card, three short lines:

- “1 สูบ: ดูด → อัด → กำลัง → คาย (720°)”
- “8 สูบ: ผลัดกันจุดระเบิดทุก 90° ในตัวอย่างนี้”
- “แรงเป็นจังหวะ → เพลาหมุนต่อเนื่องขึ้น”

## Quality gates

- No local Manim rendering. Local checks are limited to `python -m py_compile` and import checks.
- Before dispatch, grep for Thai inside `MathTex` `\\text{}` blocks.
- `[LAYOUT]` must finish clean. Fix all reported overlap/off-frame issues.
- Cloud render only through `render_manim.yml` on branch `agy-v8-remake`; pass `--ref agy-v8-remake`.
- The delegated job must dispatch the workflow, print the run id, and stop. It must not wait/watch the cloud render.
- Final verification by Codex: inspect frames at component labeling, each of four strokes, the end-on 90-degree proving shot, at least three firing events across both banks, torque chart, and final summary. Any 3D structural claim needs more than one angle/frame.
- Do not modify or reuse `v8_engine_3d.py`; this is a clean redesign in a new file.
