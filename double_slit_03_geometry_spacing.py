"""
double_slit_03_geometry_spacing.py
Module 3: Young's Double-Slit Wave Interference
Scenes:
  - DS05_GeometryDerivation (~90s)
  - DS06_SmallAngleSpacing (~80s)
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Color Palette
C_BARRIER = "#78909C"
C_SCREEN  = "#37474F"
C_S1      = "#42A5F5"  # Slit S1 (Blue)
C_S2      = "#FF7043"  # Slit S2 (Orange)
C_DIFF    = "#E91E63"  # Path difference delta (Magenta)
C_BRIGHT  = "#00E676"  # Bright maxima
C_DARK    = "#1A237E"  # Dark minima
C_ANGLE   = "#FFD54F"  # Angle theta (Yellow)
C_PERP    = "#26C6DA"  # Perpendicular line (Cyan)


class DS05_GeometryDerivation(SafeScene):
    """
    Beat 5: Geometry Derivation (Delta r approx d sin theta) (~90s)
    Locked Top/Orthographic view with zoom on slits.
    Proves why the apex angle of triangle S1 S2 H equals theta,
    leading to Delta r approx d sin theta under the Fraunhofer condition (L >> d).
    """
    def construct(self):
        pref = page_ref("Beat 5 · การพิสูจน์เรขาคณิต")
        ttl = title("Geometry Derivation: Delta r approx d sin(theta)", size=25)
        cap1 = caption_top("เมื่อระยะฉาก L >> d: รังสีแสงสองเส้นแทบจะขนานกันทำมุม theta กับแนวกึ่งกลาง")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 1. Slit Plane and Parallel Ray Geometry
        # Zoomed view of slits: S1 at [-3.0, 1.2, 0], S2 at [-3.0, -1.2, 0]
        s_x = -3.0
        d_val = 2.4
        s1_pt = np.array([s_x, d_val / 2, 0])
        s2_pt = np.array([s_x, -d_val / 2, 0])

        barrier_line = Line([s_x, -2.4, 0], [s_x, 2.4, 0], color=C_BARRIER, stroke_width=4)
        dot_s1 = Dot(s1_pt, color=C_S1, radius=0.1)
        dot_s2 = Dot(s2_pt, color=C_S2, radius=0.1)
        lbl_s1 = Text("S1", font_size=18, color=C_S1).next_to(dot_s1, LEFT, buff=0.12)
        lbl_s2 = Text("S2", font_size=18, color=C_S2).next_to(dot_s2, LEFT, buff=0.12)

        # Hypotenuse d between S1 and S2
        brace_d = BraceBetweenPoints([s_x - 0.25, -d_val / 2, 0], [s_x - 0.25, d_val / 2, 0], LEFT, color=WHITE)
        lbl_d = MathTex("d", font_size=22, color=WHITE).next_to(brace_d, LEFT, buff=0.08)

        # Central Horizontal Reference Line
        center_line = DashedLine([s_x, 0, 0], [4.5, 0, 0], color=GRAYTXT, stroke_width=1.5)
        lbl_c = Text("แนวกึ่งกลาง", font_size=14, color=GRAYTXT).next_to(center_line.get_end(), RIGHT, buff=0.1)

        self.play(
            Create(barrier_line), FadeIn(dot_s1), FadeIn(dot_s2), FadeIn(lbl_s1), FadeIn(lbl_s2),
            Create(brace_d), FadeIn(lbl_d), Create(center_line), FadeIn(lbl_c),
            run_time=1.2
        )

        # 2. Parallel Rays at Angle theta
        theta = 24 * DEGREES  # visual angle for clarity
        ray_len = 7.0
        u_ray = np.array([np.cos(theta), np.sin(theta), 0])

        ray1 = Line(s1_pt, s1_pt + u_ray * ray_len, color=C_S1, stroke_width=2.5)
        ray2 = Line(s2_pt, s2_pt + u_ray * ray_len, color=C_S2, stroke_width=2.5)

        # Angle theta arc with horizontal at S1
        ref_h1 = DashedLine(s1_pt, s1_pt + [3.0, 0, 0], color=GRAYTXT, stroke_width=1)
        arc_theta1 = Arc(radius=1.0, start_angle=0, angle=theta, arc_center=s1_pt, color=C_ANGLE, stroke_width=2)
        lbl_theta1 = MathTex("\\theta", font_size=18, color=C_ANGLE).next_to(arc_theta1, RIGHT, buff=0.08)

        self.play(
            Create(ray1), Create(ray2),
            Create(ref_h1), Create(arc_theta1), FadeIn(lbl_theta1),
            run_time=1.4
        )
        self.wait(1.0)

        # 3. Construct Perpendicular from S1 to Ray 2 (Point H)
        cap2 = caption_top("ลากเส้นตั้งฉากจาก S1 ไปยังรังสีที่สอง: เกิดสามเหลี่ยมมุมฉาก Delta S1 S2 H")
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)

        # Point H is on ray2 such that (H - S1) is perpendicular to u_ray
        # vector S2 -> S1 = [0, d_val, 0]
        # projection of (S1 - S2) onto u_ray = (d_val * sin(theta)) * u_ray
        # Therefore H = s2_pt + (d_val * sin(theta)) * u_ray
        delta_geom = d_val * np.sin(theta)
        h_pt = s2_pt + delta_geom * u_ray

        perp_line = Line(s1_pt, h_pt, color=C_PERP, stroke_width=3.5)
        dot_h = Dot(h_pt, color=C_PERP, radius=0.08)
        lbl_h = Text("H", font_size=16, color=C_PERP).next_to(dot_h, DOWN + RIGHT, buff=0.08)

        # Right angle symbol at H
        u_norm = (s1_pt - h_pt) / np.linalg.norm(s1_pt - h_pt)
        sq_size = 0.25
        sq_corner = h_pt + u_ray * sq_size + u_norm * sq_size
        right_ang = VMobject(color=C_PERP, stroke_width=2).set_points_as_corners([
            h_pt + u_ray * sq_size, sq_corner, h_pt + u_norm * sq_size
        ])

        # Extra path difference segment S2 H
        extra_segment = Line(s2_pt, h_pt, color=C_DIFF, stroke_width=5)
        lbl_delta_seg = MathTex("\\Delta r \\approx d\\sin\\theta", font_size=20, color=C_DIFF).next_to(extra_segment, DOWN + LEFT, buff=0.08)

        self.play(
            Create(perp_line), FadeIn(dot_h), FadeIn(lbl_h), Create(right_ang),
            run_time=1.2
        )
        self.play(Create(extra_segment), FadeIn(lbl_delta_seg), run_time=1.0)
        self.wait(1.2)

        # 4. Prove Angle in Triangle is theta
        cap3 = caption_top("พิสูจน์มุม: แนวสลิตตั้งฉากกับกึ่งกลาง (90°) มุมยอดจึงเป็น 90° - (90° - theta) = theta")
        arc_apex = Arc(radius=0.7, start_angle=-PI/2, angle=theta, arc_center=s1_pt, color=C_ANGLE, stroke_width=2.5)
        lbl_apex = MathTex("\\theta", font_size=18, color=C_ANGLE).next_to(arc_apex, DOWN + RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(cap2, cap3),
            Create(arc_apex), FadeIn(lbl_apex),
            run_time=1.2
        )
        self.wait(1.5)

        # 5. Conditions for Bright and Dark Fringes
        cap4 = caption_top("สรุปเงื่อนไข: แถบสว่างเมื่อครบจำนวนเต็มคลื่น · แถบมืดเมื่อเหลือเศษครึ่งคลื่น")
        card_box = RoundedRectangle(width=5.8, height=1.6, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.9).move_to([2.2, 1.8, 0])
        eq_bright = MathTex("d\\sin\\theta = m\\lambda \\quad (\\text{Bright: } m=0,\\pm 1,\\pm 2)", font_size=18, color=C_BRIGHT).move_to([2.2, 2.2, 0])
        eq_dark = MathTex("d\\sin\\theta = \\left(m + \\frac{1}{2}\\right)\\lambda \\quad (\\text{Dark: } m=0,\\pm 1)", font_size=18, color=C_DIFF).move_to([2.2, 1.5, 0])
        card_grp = VGroup(card_box, eq_bright, eq_dark)

        self.play(ReplacementTransform(cap3, cap4), FadeIn(card_grp), run_time=1.2)
        self.wait(2.0)

        self.fade_out_all(run_time=0.8)


class DS06_SmallAngleSpacing(SafeScene):
    """
    Beat 6: Small-Angle Approximation & Fringe Spacing (~80s)
    Locked Front-on view of screen with intensity plot.
    Derives:
      y = L tan(theta)
      sin(theta) approx tan(theta) approx y/L
      y_m approx m (lambda L / d)
      Delta y approx lambda L / d (strictly using approx)
      Exact angular formula vs approximate spatial formula.
    """
    def construct(self):
        pref = page_ref("Beat 6 · ระยะห่างระหว่างริ้วแถบ")
        ttl = title("Fringe Spacing & Small-Angle Approximation", size=25)
        cap1 = caption_top("เมื่อมุม theta มีขนาดเล็กมาก (theta << 1 rad): ประมาณว่า sin(theta) approx tan(theta) approx y/L")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 1. Screen Representation with Bright/Dark Stripes (Left Side: x = -4.5 to -1.5)
        scr_bg = Rectangle(width=2.6, height=5.2, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([-3.2, -0.2, 0])
        scr_title = Text("ภาพจริงบนฉาก", font_size=16, color=WHITE).next_to(scr_bg.get_top(), UP, buff=0.1)

        # Fringe stripes at y = 0, +/- 0.9, +/- 1.8
        fringes = VGroup()
        fringe_data = [
            (1.8, "m = +2", C_BRIGHT),
            (0.9, "m = +1", C_BRIGHT),
            (0.0, "m = 0 (สว่างกลาง)", C_BRIGHT),
            (-0.9, "m = -1", C_BRIGHT),
            (-1.8, "m = -2", C_BRIGHT),
        ]

        fringe_labels = VGroup()
        for y_pos, m_txt, col in fringe_data:
            bar = Rectangle(width=2.2, height=0.35, color=col, fill_opacity=0.85, fill_color=col).move_to([-3.2, y_pos - 0.2, 0])
            lbl = Text(m_txt, font_size=13, color=WHITE).next_to(bar, LEFT, buff=0.12)
            fringes.add(bar)
            fringe_labels.add(lbl)

        # Distance Delta y brace between m = 0 and m = 1
        brace_dy = BraceBetweenPoints([-3.2 + 1.2, -0.2, 0], [-3.2 + 1.2, 0.7, 0], RIGHT, color=C_ANGLE)
        lbl_dy = MathTex("\\Delta y \\approx \\frac{\\lambda L}{d}", font_size=18, color=C_ANGLE).next_to(brace_dy, RIGHT, buff=0.08)

        self.play(
            FadeIn(scr_bg), FadeIn(scr_title),
            FadeIn(fringes), FadeIn(fringe_labels),
            Create(brace_dy), FadeIn(lbl_dy),
            run_time=1.5
        )
        self.wait(1.0)

        # 2. Mathematical Derivation Panel (Right Side: x = 1.0 to 5.8)
        cap2 = caption_top("แทนค่าลงในเงื่อนไขแถบสว่าง: ตำแหน่ง y_m approx m (lambda L / d) ทุกแถบห่างเท่ากันคงที่")
        deriv_box = RoundedRectangle(width=5.0, height=4.2, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.85).move_to([3.4, -0.2, 0])

        step1 = MathTex("y = L \\tan\\theta", font_size=20, color=WHITE).move_to([3.4, 1.4, 0])
        step2 = MathTex("\\sin\\theta \\approx \\tan\\theta \\approx \\frac{y}{L}", font_size=20, color=C_ANGLE).move_to([3.4, 0.8, 0])
        step3 = MathTex("d\\left(\\frac{y}{L}\\right) \\approx m\\lambda \\implies y_m \\approx m\\frac{\\lambda L}{d}", font_size=20, color=C_BRIGHT).move_to([3.4, 0.1, 0])
        step4 = MathTex("\\Delta y = y_{m+1} - y_m \\approx \\frac{\\lambda L}{d}", font_size=21, color=OK).move_to([3.4, -0.6, 0])

        # Exact angular formula vs approximate spatial formula
        law_exact = MathTex("I(\\theta) = 4I_0 \\cos^2\\left(\\frac{\\pi d\\sin\\theta}{\\lambda}\\right)", font_size=18, color=WHITE).move_to([3.4, -1.3, 0])
        law_approx = MathTex("I(y) \\approx 4I_0 \\cos^2\\left(\\frac{\\pi d y}{\\lambda L}\\right)", font_size=18, color=C_DIFF).move_to([3.4, -1.8, 0])

        deriv_grp = VGroup(deriv_box, step1, step2, step3, step4, law_exact, law_approx)

        self.play(
            ReplacementTransform(cap1, cap2),
            FadeIn(deriv_box),
            Write(step1), Write(step2),
            run_time=1.8
        )
        self.play(Write(step3), Write(step4), run_time=1.8)
        self.play(FadeIn(law_exact), FadeIn(law_approx), run_time=1.2)
        self.wait(2.2)

        self.fade_out_all(run_time=0.8)
