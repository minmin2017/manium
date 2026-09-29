# G21C_TermGlow — build brief for Gemini (Sender: Claude)  [plan file per manim-teaching-video §42]

You are writing ONE new Manim CE 0.20 scene class `G21C_TermGlow` in a NEW file `spur_g21c.py` (repo root, this worktree, branch `agy-g21c-termglow`).
Audience: a Thai engineering student. Topic (lecture page 21-22 of spur gears): the two right triangles that give
`E1B = sqrt(Ro1^2 - Rb1^2)` and `E2A = sqrt(Ro2^2 - Rb2^2)`. An earlier version of this clip exists (`G21B_TriangleEnds` in `spur_gears.py`, lines ~1890-2000) and shows the
whole formula at once. **The student's complaint (the reason for this job): people do not understand the variables/numbers.** So the NEW clip must walk the formula
**one variable at a time: the term glows in the equation AND the matching real line in the figure glows at the same moment, in the same `self.play`**, then the next term. Same for the numbers.

## Hard rules (Gemini cannot see Claude's skills, so they are inlined here)
1. Subclass `SafeScene` (from `mlib`), never bare `Scene`. `from manim import *`, `from mlib import *`, `from gear_law_similar import pt, tag, ra_mark`,
   `from spur_gears import g20_geom, arc_near, side_label, ADD_C, BASE_C, LOA_C`, `from g21c_captions import CAP, TITLE, PAGE`.
2. ALL Thai text comes from `g21c_captions.py` (import it, use `caption_top(CAP["key"], size=19)` for captions, `title(TITLE, size=26)`, `page_ref(PAGE)`). NEVER type or retype Thai characters
   in your code (your Thai output gets corrupted to '???'). ASCII labels like "Ro1", "Rb1", "E1B" are fine (`Text("Ro1", ...)`).
3. Captions: swap them SEQUENTIALLY (`self.play(FadeOut(old), run_time=0.35)` then `self.play(FadeIn(new), run_time=0.5)`), never cross-fade two captions in one `self.play` (layout linter flags overlap).
4. Layout: keep everything inside x in [-7, 7], y in [-2.7, 2.3] (caption zone is y~2.72, title y=3.45, bottom of frame is reserved for the video player controls). Text must not sit on top of strokes. Static camera.
5. Colors (identical in equation and figure from the very first frame that shows the variable): Ro* = `ADD_C` (yellow #FFEE58), Rb* = `BASE_C` (purple #AB47BC), the result segment/term (E1B, E2A) = `WARN` (orange, from mlib),
   the red line of action = `LOA_C`. Never reuse a color for a second meaning.
6. Formula pieces: build each equation as separate MathTex parts so you can address terms, e.g.
   `eq = MathTex(r"\overline{E_2A}", r"=", r"\sqrt{", r"R_{o2}^{2}", r"-", r"R_{b2}^{2}", r"}", font_size=40)` then `eq[3].set_color(ADD_C)`, `eq[5].set_color(BASE_C)`, `eq[0].set_color(WARN)`
   (if the split does not compile in LaTeX, use `MathTex(..., substrings_to_isolate=[...])` or several separate MathTex objects arranged with `.arrange(RIGHT)`; you cannot render locally, so prefer the most conservative construction).
   Glow = `Indicate(part, color=..., scale_factor=1.12)` together with `Indicate(figure_segment, color=WHITE, scale_factor=1.0)` inside ONE `self.play(...)`, then `self.wait(0.6-1.0)` so the viewer can follow.
7. NO local rendering (project rule: renders only on the cloud). Allowed locally: `python -m py_compile spur_g21c.py`, `python -c "import spur_g21c"`, numpy/geometry asserts.
8. Do not edit any existing file (spur_gears.py, mlib.py, gear_law_similar.py, g21c_captions.py...). Only create `spur_g21c.py`. Do not create tracker/progress files.
9. Use only native 2D primitives (Line, Polygon, Dot, Arc, Text, MathTex). No `Arrow3D`.

## Geometry (already verified — reuse, do not re-derive)
`g = g20_geom(k=1.0, P_screen=(-3.6, 0.55, 0.0))` returns numpy 3-vectors `P,O1,O2,E1,E2,A,B` (screen units = inches), unit vectors `w,n`, radii `Rb1,Rb2,Ro1,Ro2`, etc.
Read `class G21B_TriangleEnds` in `spur_gears.py`: it already draws the line of action, dots, triangle O1-E1-B / O2-E2-A, side labels (`side_label`), the right-angle marks (`ra_mark`) and short circle arcs
(`arc_near`) at positions that pass the layout linter (label directions for E1/B/A/E2 were tuned — keep them). Reuse that figure code; what you are building is the NEW glow-by-term presentation on the right panel.
Math panel on the right side of the frame (x ~ 1.0..7.0): header `Z = E1B + E2A - E1E2` at (3.3, 2.0) (small, as in G21B), working equations at y ~ 0.9 / 0.0 / -1.0.

## Beat table (target ~50 s; Claude will render and check every row)
| t (s) | what happens | animation calls | on screen |
|---|---|---|---|
| 0-4 | title, page_ref, caption `intro`; header formula; line of action + 5 dots | FadeIn/Create | LOA_C |
| 4-9 | gear 1: O1, triangle O1-E1-B (faint white fill), segments O1E1 (purple), O1B (yellow), E1B (orange) drawn one by one; arcs; side labels Rb1/Ro1/E1B in their colors; caption `g1_tri` | Create per segment, FadeIn labels | colors per rule 5 |
| 9-12 | right-angle mark at E1, caption `g1_right` | Create(ra_mark) | purple |
| 12-14 | the FULL formula `E1B = sqrt(Ro1^2 - Rb1^2)` appears on the right with every term already in its variable color; caption `g1_formula` | FadeIn | eq |
| 14-17 | **glow Ro1**: `eq` part Ro1 AND segment O1B glow together; caption `g1_ro`; wait | one `self.play` | yellow |
| 17-20 | **glow Rb1**: part Rb1 AND segment O1E1 together; caption `g1_rb`; wait | one `self.play` | purple |
| 20-23 | **glow the result**: part `E1B` AND orange segment E1B together; caption `g1_res`; wait | one `self.play` | orange |
| 23-32 | numbers row appears below: `E1B = sqrt(1.625^2 - 1.4095^2) = 0.809 in` built as parts; glow `1.625` + O1B (caption `g1_n_ro`), then `1.4095` + O1E1 (`g1_n_rb`), then `0.809` + E1B (`g1_n_res`) | three `self.play` | same colors |
| 32-34 | fade gear-1 figure/labels/equations except a small boxed result `E1B = sqrt(...)` moved up-right (scale 0.7, y ~ 1.05) | FadeOut + animate.move_to/scale | |
| 34-50 | gear 2: exactly the same sequence with O2, E2, A, `Ro2/Rb2/E2A` (captions `g2_*`, numbers 3.875 / 3.5238 / 1.612); triangle O2-E2-A is tall (Rb2 = 3.52) — keep O2 label to the LEFT | same | |
| 50-54 | caption `outro`; both boxed results visible | | |

Numbers to display (verified): Ro1 = 1.625, Rb1 = 1.4095, E1B = 0.809; Ro2 = 3.875, Rb2 = 3.5238, E2A = 1.612 (inches).

## Definition of done / output contract
1. `python -m py_compile spur_g21c.py` and `python -c "import spur_g21c"` both pass (run them from the repo root with `D:\Desktop\manium\.venv_community\Scripts\python.exe`).
2. `git add spur_g21c.py && git commit -m "feat(g21c): term-by-term glow version of pages 21-22"` and `git push -u origin agy-g21c-termglow`.
3. **Do NOT dispatch any GitHub workflow and do NOT wait for renders** — Claude renders and verifies. STOP after the push.
4. Final message (English): file path, class name, commit hash, and for each beat-table row the line number(s) in `spur_g21c.py`, plus a list of anything you were unsure about (e.g. MathTex splitting).
