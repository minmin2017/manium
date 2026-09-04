"""Rubik's Cube 3x3x3 demo — Min's request 2026-09-04 (single standalone video).

Builds all 26 outer cubies from manim's own Cube mobject (already made of 6
Square faces in a fixed [IN, OUT, LEFT, RIGHT, UP, DOWN] order — see
Cube.generate_points in the manim source), recolors only the outward-facing
squares per the standard sticker scheme, then demonstrates layer turns.

Layer-turn correctness note: after each 90-degree turn, the 9 cubies in that
layer must be re-keyed to their new grid slot using the SAME rotation manim's
Rotating animation applies (manim.utils.space_ops.rotate_vector), not a
hand-derived sign convention — otherwise a later turn on a different axis
would grab the wrong physical pieces (see mlib skill notes, "layout linter
does not catch graphic-vs-graphic defects").
"""

from mlib import *
import numpy as np
from manim.utils.space_ops import rotate_vector

UNIT = 1.05
CUBIE = 0.95

U_COL, D_COL = "#FFFFFF", "#FDD835"   # up / down
F_COL, B_COL = "#43A047", "#1E88E5"   # front (OUT) / back (IN)
R_COL, L_COL = "#E53935", "#FB8C00"   # right / left
BODY = "#141414"                       # unseen plastic


def make_cubie(ix, iy, iz):
    c = Cube(side_length=CUBIE, fill_opacity=1, fill_color=BODY,
              stroke_width=1.5, stroke_color=BLACK)
    # Cube.generate_points order: IN, OUT, LEFT, RIGHT, UP, DOWN.
    # Verified empirically (draft render, phi=65deg/theta=-50deg camera):
    # OUT renders at the visual top, DOWN renders lower-left-visible,
    # RIGHT renders lower-right-visible -- so map colors here (not the
    # face-index names) to land on the classic white-top/green/red look.
    if iz == -1:
        c[0].set_fill(D_COL, 1)   # IN -> yellow (opposite of white)
    if iz == 1:
        c[1].set_fill(U_COL, 1)   # OUT -> white (visible top)
    if ix == -1:
        c[2].set_fill(L_COL, 1)
    if ix == 1:
        c[3].set_fill(R_COL, 1)   # RIGHT -> red (visible)
    if iy == 1:
        c[4].set_fill(B_COL, 1)   # UP -> blue (opposite of green)
    if iy == -1:
        c[5].set_fill(F_COL, 1)   # DOWN -> green (visible)
    c.move_to(np.array([ix, iy, iz]) * UNIT)
    return c


class RubiksCube3D(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        cubies = {}
        for ix in (-1, 0, 1):
            for iy in (-1, 0, 1):
                for iz in (-1, 0, 1):
                    if ix == 0 and iy == 0 and iz == 0:
                        continue  # hidden center mechanism, never visible
                    cubies[(ix, iy, iz)] = make_cubie(ix, iy, iz)

        heading = title("ลูกบาศก์คิวบิก 3x3x3")
        self.hud(heading)
        self.play(FadeIn(heading), run_time=0.6)

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in cubies.values()], lag_ratio=0.03),
            run_time=2.5,
        )
        self.wait(0.3)

        cap1 = caption_top("26 ชิ้นเล็ก (cubies) รอบแกนกลางที่มองไม่เห็น")
        self.hud(cap1)
        self.play(FadeIn(cap1), run_time=0.5)

        self.begin_ambient_camera_rotation(rate=0.35)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(cap1), run_time=0.4)

        cap2 = caption_top('แต่ละ "ชั้น" หมุนอิสระทีละ 90 องศา')
        self.hud(cap2)
        self.play(FadeIn(cap2), run_time=0.5)

        self.turn_layer(cubies, axis="z", layer=1, axis_vec=OUT, run_time=1.1)
        self.wait(0.2)
        self.turn_layer(cubies, axis="y", layer=1, axis_vec=UP, run_time=1.1)
        self.wait(0.2)
        self.turn_layer(cubies, axis="x", layer=1, axis_vec=RIGHT, run_time=1.1)
        self.wait(0.4)

        self.play(FadeOut(cap2), run_time=0.4)

        cap3 = caption_top("6 หน้า x 9 ช่องสี - ปริศนาของ Erno Rubik ปี 1974")
        self.hud(cap3)
        self.play(FadeIn(cap3), run_time=0.5)

        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(cap3), FadeOut(heading), run_time=0.6)

    def turn_layer(self, cubies, axis, layer, axis_vec, run_time=1.2, angle=PI / 2):
        idx = {"x": 0, "y": 1, "z": 2}[axis]
        keys = [k for k in cubies if k[idx] == layer]
        group = VGroup(*[cubies[k] for k in keys])
        self.play(Rotating(group, angle=angle, axis=axis_vec,
                             about_point=ORIGIN, run_time=run_time))

        updates = {}
        for k in keys:
            rotated = rotate_vector(np.array(k, dtype=float), angle, axis=axis_vec)
            new_k = tuple(int(round(v)) for v in rotated)
            updates[new_k] = cubies[k]
        for k in keys:
            del cubies[k]
        cubies.update(updates)
