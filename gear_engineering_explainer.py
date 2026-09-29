"""W06 engineering-explainer style sample: external spur-gear speed ratio.

The gears are schematic trapezoid-tooth silhouettes. Tooth count and speed ratio
are exact; tooth profiles are not intended as an involute geometry lesson.
"""

import numpy as np
from manim import *
from mlib import SafeScene, gear_shape


BG = "#F7FBFF"
GRID = "#4DA8E4"
GRID_MAJOR = "#147DBB"
NAVY = "#173B57"
GOLD = "#FFC247"
ORANGE = "#F28C28"
AMBER = "#D96A1D"


def blueprint_grid():
    lines = VGroup()
    for x in np.arange(-7.2, 7.3, 0.5):
        major = abs(x - round(x)) < 0.01
        lines.add(Line([x, -4.1, 0], [x, 4.1, 0],
                       color=GRID_MAJOR if major else GRID,
                       stroke_width=1.6 if major else 1.0,
                       stroke_opacity=0.47 if major else 0.43))
    for y in np.arange(-4.0, 4.1, 0.5):
        major = abs(y - round(y)) < 0.01
        lines.add(Line([-7.2, y, 0], [7.2, y, 0],
                       color=GRID_MAJOR if major else GRID,
                       stroke_width=1.6 if major else 1.0,
                       stroke_opacity=0.47 if major else 0.43))
    return lines


class W06_EngineeringGearRatio(SafeScene):
    def construct(self):
        self.camera.background_color = BG
        self.add(blueprint_grid())

        title = Text("เฟืองตรง: 12 ฟัน ขับ 24 ฟัน", font_size=34,
                     color=NAVY).move_to([0, 3.38, 0])
        subtitle = Text("หัวข้อที่ 6  •  อัตราทดของเฟืองภายนอก", font_size=23,
                        color=NAVY).move_to([0, 2.76, 0])
        self.play(FadeIn(title), FadeIn(subtitle), run_time=1.0)

        r1, r2 = 1.05, 2.10
        c1 = np.array([-3.55, -0.25, 0])
        c2 = np.array([-0.40, -0.25, 0])
        driver = gear_shape(r1, 12, GOLD, tooth_depth_frac=0.13,
                            stroke_width=3).move_to(c1)
        follower = gear_shape(r2, 24, ORANGE, tooth_depth_frac=0.065,
                              stroke_width=3).move_to(c2)
        driver[1].set_fill(AMBER, opacity=1)
        follower[1].set_fill(AMBER, opacity=1)
        spoke1 = Line(c1, c1 + r1 * UP * 0.72, color=AMBER, stroke_width=7)
        spoke2 = Line(c2, c2 + r2 * UP * 0.72, color=AMBER, stroke_width=7)
        driver.add(spoke1)
        follower.add(spoke2)

        lab1 = MathTex(r"N_1=12", color=NAVY, font_size=38).move_to([-3.55, -2.18, 0])
        lab2 = MathTex(r"N_2=24", color=NAVY, font_size=38).move_to([-0.40, -2.85, 0])
        note = Text("ฟันขบกัน → หมุนสวนทาง", font_size=23,
                    color=NAVY).move_to([-3.2, 2.18, 0])
        self.play(DrawBorderThenFill(driver), DrawBorderThenFill(follower),
                  run_time=1.6)
        self.play(FadeIn(lab1), FadeIn(lab2), FadeIn(note), run_time=0.8)

        # The marked spokes make one turn versus half a turn visible.
        self.play(Rotate(driver, angle=-TAU, about_point=c1),
                  Rotate(follower, angle=PI, about_point=c2),
                  run_time=5.0, rate_func=linear)

        ratio_head = Text("อัตราส่วนความเร็ว", font_size=27,
                          color=NAVY).move_to([4.55, 1.90, 0])
        eq1 = MathTex(r"\frac{\omega_2}{\omega_1}", r"=",
                      r"-\frac{N_1}{N_2}", color=NAVY,
                      font_size=43).move_to([4.55, 0.87, 0])
        eq1[2].set_color(AMBER)
        eq2 = MathTex(r"=", r"-\frac{12}{24}", color=NAVY,
                      font_size=43).move_to([4.55, -0.13, 0])
        eq2[1].set_color(AMBER)
        eq3 = MathTex(r"=", r"-\frac{1}{2}", color=NAVY,
                      font_size=50).move_to([4.55, -1.15, 0])
        eq3[1].set_color(AMBER)

        self.play(FadeIn(ratio_head), FadeIn(eq1), run_time=1.2)
        self.play(Indicate(driver, color=WHITE, scale_factor=1.0),
                  Indicate(eq1[2], color=WHITE, scale_factor=1.18),
                  run_time=1.5)
        self.play(FadeIn(eq2), run_time=0.8)
        self.play(FadeIn(eq3), run_time=0.8)

        conclusion = Text("เฟืองใหญ่หมุนช้าลงครึ่งหนึ่ง • ทิศตรงข้าม",
                          font_size=24, color=NAVY).move_to([0, -3.46, 0])
        self.play(FadeIn(conclusion), run_time=0.8)
        self.wait(2.0)
