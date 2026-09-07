"""Benchmark: how expensive are native Manim 3D solids for a motor-sized assembly?

Reason this exists: skill sec.2/sec.26 measured Arrow3D at ~62x and Polyhedron-from-.obj at
~20x the cost of native primitives (52s PER FRAME for a 2k-face model). Before rebuilding the
DC motor clip out of solid parts we need a real number for THIS part count at THIS resolution,
not an assumption. Two scenes, identical geometry, only `resolution` differs.
"""
from manim import *
import numpy as np

Y_AXIS = np.array([0.0, 1.0, 0.0])


def build_motor(res):
    """A realistic solid-motor part count: 2 poles, yoke, shaft, armature core,
    2 commutator segments, 2 brushes, 4 coil conductors."""
    static = VGroup()
    # pole pieces (boxes -- cheapest solid)
    for x, col in ((-1.55, RED_E), (1.55, BLUE_E)):
        static.add(Prism(dimensions=[0.7, 2.6, 2.2]).move_to([x, 0, 0]).set_fill(col, 1).set_stroke(width=0))
    # yoke / frame
    static.add(Prism(dimensions=[4.6, 2.8, 0.35]).move_to([0, 0, -1.55]).set_fill(GREY_D, 1).set_stroke(width=0))
    # brushes
    for z in (0.42, -0.42):
        static.add(Prism(dimensions=[0.16, 0.16, 0.30]).move_to([0, 1.85, z]).set_fill(GREY_B, 1).set_stroke(width=0))

    rotor = VGroup()
    rotor.add(Cylinder(radius=0.10, height=5.2, direction=Y_AXIS, resolution=res)
              .set_fill(GREY_C, 1).set_stroke(width=0))                      # shaft
    rotor.add(Cylinder(radius=0.58, height=2.3, direction=Y_AXIS, resolution=res)
              .set_fill(GREY_B, 1).set_stroke(width=0))                      # armature core
    for v0, col in ((0, GOLD_E), (PI, GOLD_A)):                              # commutator halves
        rotor.add(Cylinder(radius=0.30, height=0.45, direction=Y_AXIS,
                           v_range=[v0, v0 + PI], resolution=res, show_ends=False)
                  .move_to([0, 1.85, 0]).set_fill(col, 1).set_stroke(width=0))
    for x in (-0.72, 0.72):                                                  # coil conductors
        rotor.add(Cylinder(radius=0.07, height=2.4, direction=Y_AXIS, resolution=res)
                  .move_to([x, 0, 0]).set_fill(ORANGE, 1).set_stroke(width=0))
    for y in (-1.2, 1.2):                                                    # coil end turns
        rotor.add(Cylinder(radius=0.07, height=1.44,
                           direction=np.array([1.0, 0.0, 0.0]), resolution=res)
                  .move_to([0, y, 0]).set_fill(ORANGE, 1).set_stroke(width=0))
    return static, rotor


class SolidBenchLow(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        static, rotor = build_motor((6, 6))
        self.add(static, rotor)
        self.play(Rotating(rotor, axis=Y_AXIS, angle=TAU, about_point=ORIGIN),
                  run_time=2, rate_func=linear)


class SolidBenchHigh(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        static, rotor = build_motor((18, 18))
        self.add(static, rotor)
        self.play(Rotating(rotor, axis=Y_AXIS, angle=TAU, about_point=ORIGIN),
                  run_time=2, rate_func=linear)
