"""
double_slit_03_geometry_spacing.py
Module 3: Young's Double-Slit Wave Interference
Scenes:
  - DS05_GeometryDerivation (Target: >= 90s, Planned: ~98s)
  - DS06_SmallAngleSpacing (Target: >= 80s, Planned: ~85s)
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
    Beat 5: Geometry Derivation (Delta r approx d sin theta) (~98s)
    Locked Top/Orthographic view with zoom on slits.
    Micro-beats:
      1. Slit zoom & Far-field condition L >> d (18s)
      2. Parallel rays at angle theta, construct perpendicular S1 H (20s)
      3. Geometric angle proof for triangle Delta S1 S2 H (20s)
      4. Triangle projection and sine relation (18s)
      5. Constructive condition: whole wavelengths m lambda (12s)
      6. Destructive condition: half wavelength remainder (12s)
    """
    def construct(self):
        # 1. Slit Plane Setup & Far-Field Condition L >> d (Micro-beat 1: ~18s)
        pref = page_ref("Beat 5 · การพิสูจน์เรขาคณิต")
        ttl = title("Geometry Derivation: Delta r approx d sin(theta)", size=25)
        cap1 = caption_top("เงื่อนไขสนามไกล (Far-field): ระยะฉาก L กว้างใหญ่กว่าระยะสลิต d มหาศาล (L >> d)")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.2)
        self.wait(5.0)

        s_x = -3.2
        d_val = 2.4
        s1_pt = np.array([s_x, d_val / 2, 0])
        s2_pt = np.array([s_x, -d_val / 2, 0])

        barrier_line = Line([s_x, -2.5, 0], [s_x, 2.5, 0], color=C_BARRIER, stroke_width=4)
        dot_s1 = Dot(s1_pt, color=C_S1, radius=0.1)
        dot_s2 = Dot(s2_pt, color=C_S2, radius=0.1)
        lbl_s1 = Text("S1", font_size=18, color=C_S1).next_to(dot_s1, LEFT, buff=0.12)
        lbl_s2 = Text("S2", font_size=18, color=C_S2).next_to(dot_s2, LEFT, buff=0.12)

        brace_d = BraceBetweenPoints([s_x - 0.25, -d_val / 2, 0], [s_x - 0.25, d_val / 2, 0], LEFT, color=WHITE)
        lbl_d = MathTex("d", font_size=22, color=WHITE).next_to(brace_d, LEFT, buff=0.08)

        center_line = DashedLine([s_x, 0, 0], [4.5, 0, 0], color=GRAYTXT, stroke_width=1.5)
        lbl_c = Text("แนวกึ่งกลาง (Center Axis)", font_size=13, color=GRAYTXT).next_to(center_line.get_end(), RIGHT, buff=0.1)

        self.play(
            Create(barrier_line), FadeIn(dot_s1), FadeIn(dot_s2), FadeIn(lbl_s1), FadeIn(lbl_s2),
            Create(brace_d), FadeIn(lbl_d), Create(center_line), FadeIn(lbl_c),
            run_time=2.0
        )
        self.wait(3.5)

        cap_ray_intro = caption_top("เพราะ L >> d มากๆ: ลำแสงสองเส้นที่เดินทางไปยังจุด P เดียวกัน จึงถือว่าขนานกันทำมุม theta")
        self.play(ReplacementTransform(cap1, cap_ray_intro), run_time=1.0)
        self.wait(5.5)

        # 2. Parallel Rays at Angle theta & Construct Perpendicular (Micro-beat 2: ~20s)
        cap2 = caption_top("ลากเส้นจาก S1 ไปตั้งฉากกับรังสีที่สองที่จุด H: เกิดสามเหลี่ยมมุมฉาก Delta S1 S2 H")
        theta = 24 * DEGREES
        ray_len = 7.0
        u_ray = np.array([np.cos(theta), np.sin(theta), 0])

        ray1 = Line(s1_pt, s1_pt + u_ray * ray_len, color=C_S1, stroke_width=2.5)
        ray2 = Line(s2_pt, s2_pt + u_ray * ray_len, color=C_S2, stroke_width=2.5)

        ref_h1 = DashedLine(s1_pt, s1_pt + [3.0, 0, 0], color=GRAYTXT, stroke_width=1)
        arc_theta1 = Arc(radius=1.0, start_angle=0, angle=theta, arc_center=s1_pt, color=C_ANGLE, stroke_width=2)
        lbl_theta1 = MathTex("\\theta", font_size=18, color=C_ANGLE).next_to(arc_theta1, RIGHT, buff=0.08)

        self.play(
            ReplacementTransform(cap_ray_intro, cap2),
            Create(ray1), Create(ray2),
            Create(ref_h1), Create(arc_theta1), FadeIn(lbl_theta1),
            run_time=2.2
        )
        self.wait(4.0)

        delta_geom = d_val * np.sin(theta)
        h_pt = s2_pt + delta_geom * u_ray

        perp_line = Line(s1_pt, h_pt, color=C_PERP, stroke_width=3.5)
        dot_h = Dot(h_pt, color=C_PERP, radius=0.08)
        lbl_h = Text("H", font_size=16, color=C_PERP).next_to(dot_h, DOWN + RIGHT, buff=0.08)

        u_norm = (s1_pt - h_pt) / np.linalg.norm(s1_pt - h_pt)
        sq_size = 0.25
        sq_corner = h_pt + u_ray * sq_size + u_norm * sq_size
        right_ang = VMobject(color=C_PERP, stroke_width=2).set_points_as_corners([
            h_pt + u_ray * sq_size, sq_corner, h_pt + u_norm * sq_size
        ])

        extra_segment = Line(s2_pt, h_pt, color=C_DIFF, stroke_width=5)
        lbl_delta_seg = MathTex("\\Delta r \\approx d\\sin\\theta", font_size=20, color=C_DIFF).next_to(extra_segment, DOWN + LEFT, buff=0.08)

        self.play(
            Create(perp_line), FadeIn(dot_h), FadeIn(lbl_h), Create(right_ang),
            Create(extra_segment), FadeIn(lbl_delta_seg),
            run_time=2.5
        )

        cap_after_h = caption_top("จากจุด H เป็นต้นไป รังสีทั้งสองเดินทางเป็นระยะทางเท่ากันพอดี ส่วนต่างทั้งหมดจึงอยู่ที่ S2 H")
        self.play(ReplacementTransform(cap2, cap_after_h), run_time=1.0)
        self.wait(5.0)

        # 3. Geometric Angle Proof for Triangle (Micro-beat 3: ~20s)
        cap3 = caption_top("พิสูจน์มุม: แนวสลิตตั้งฉากกับกึ่งกลาง (90°) มุมยอดสามเหลี่ยมจึงเท่ากับมุมเบน theta พอดีเป๊ะ")
        arc_apex = Arc(radius=0.7, start_angle=-PI/2, angle=theta, arc_center=s1_pt, color=C_ANGLE, stroke_width=2.5)
        lbl_apex = MathTex("\\theta", font_size=18, color=C_ANGLE).next_to(arc_apex, DOWN + RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(cap_after_h, cap3),
            Create(arc_apex), FadeIn(lbl_apex),
            run_time=2.2
        )
        self.wait(8.5)

        # 4. Triangle Projection & Sine Relation (Micro-beat 4: ~18s)
        cap_trig = caption_top("การฉายเรขาคณิต: ด้านตรงข้ามมุม theta คือ Delta r ด้านตรงข้ามมุมฉากคือ d")
        self.play(ReplacementTransform(cap3, cap_trig), run_time=1.0)

        proof_trig = MathTex(r"\sin\theta = \frac{\Delta r}{d} \implies \Delta r \approx d\sin\theta", font_size=21, color=WHITE).move_to([2.0, -2.6, 0])
        self.play(FadeIn(proof_trig), run_time=1.5)
        self.wait(7.5)

        note_triangle = Text("สามเหลี่ยม Delta S1 S2 H: ด้าน S1 S2 = d (ฉาก) และ S2 H = Delta r (ข้าม)", font_size=13, color=C_ANGLE).move_to([2.0, -3.1, 0])
        self.play(FadeIn(note_triangle), run_time=1.0)
        self.wait(5.5)

        # 5. Constructive Condition: Whole Wavelengths m lambda (Micro-beat 5: ~18s)
        cap4 = caption_top("เงื่อนไขแถบสว่าง (Constructive): ผลต่างเส้นทางต้องเป็นจำนวนเต็มเท่าของความยาวคลื่น (m lambda)")
        card_bright = RoundedRectangle(width=5.8, height=1.3, corner_radius=0.12, color=C_BRIGHT, fill_color=BLACK, fill_opacity=0.9).move_to([2.2, 2.0, 0])
        eq_bright = MathTex("d\\sin\\theta = m\\lambda \\quad (m = 0, \\pm 1, \\pm 2, \\dots)", font_size=20, color=C_BRIGHT).move_to(card_bright.get_center())
        grp_bright = VGroup(card_bright, eq_bright)

        self.play(
            ReplacementTransform(cap_trig, cap4),
            FadeOut(proof_trig), FadeOut(note_triangle),
            FadeIn(grp_bright),
            run_time=1.8
        )

        pkt1_b = Dot(s1_pt, color=C_S1, radius=0.1)
        pkt2_b = Dot(h_pt, color=C_S2, radius=0.1)
        self.add(pkt1_b, pkt2_b)
        self.play(
            pkt1_b.animate.move_to(s1_pt + u_ray * 3.5),
            pkt2_b.animate.move_to(h_pt + u_ray * 3.5),
            rate_func=linear, run_time=2.5
        )
        self.remove(pkt1_b, pkt2_b)

        note_inphase = Text("เมื่อส่วนต่าง S2 H = 1 lambda: สันคลื่นจากทั้งสองช่องวิ่งคู่ขนานเข้าเสริมกัน", font_size=13, color=C_BRIGHT).move_to([2.0, -2.6, 0])
        self.play(FadeIn(note_inphase), run_time=1.0)
        self.wait(5.5)

        # 6. Destructive Condition: Half Wavelength Remainder (Micro-beat 6: ~18s)
        cap5 = caption_top("เงื่อนไขแถบมืด (Destructive): ผลต่างเส้นทางเหลือเศษครึ่งคลื่น สันชนท้องหักล้างกันสนิท")
        card_dark = RoundedRectangle(width=5.8, height=1.3, corner_radius=0.12, color=C_DIFF, fill_color=BLACK, fill_opacity=0.9).move_to([2.2, 0.4, 0])
        eq_dark = MathTex("d\\sin\\theta = \\left(m + \\frac{1}{2}\\right)\\lambda \\quad (m = 0, \\pm 1, \\dots)", font_size=20, color=C_DIFF).move_to(card_dark.get_center())
        grp_dark = VGroup(card_dark, eq_dark)

        self.play(
            ReplacementTransform(cap4, cap5),
            FadeOut(note_inphase),
            FadeIn(grp_dark),
            run_time=1.8
        )

        pkt1_d = Dot(s1_pt, color=C_S1, radius=0.1)
        pkt2_d = Dot(h_pt, color=C_S2, radius=0.1)
        self.add(pkt1_d, pkt2_d)
        self.play(
            pkt1_d.animate.move_to(s1_pt + u_ray * 3.5),
            pkt2_d.animate.move_to(h_pt + u_ray * 3.5),
            rate_func=linear, run_time=2.5
        )
        self.remove(pkt1_d, pkt2_d)

        note_outphase = Text("เมื่อส่วนต่าง S2 H = 0.5 lambda: สันคลื่นชนท้องคลื่น หักล้างเป็นศูนย์เกิดแถบมืด", font_size=13, color=C_DIFF).move_to([2.0, -2.6, 0])
        self.play(FadeIn(note_outphase), run_time=1.0)
        self.wait(6.5)

        # Master Summary hold
        cap_master_geo = caption_top("สองสมการหลัก: กำหนดตำแหน่งเชิงมุม theta ของแถบสว่างและแถบมืดทั้งหมดในการทดลอง")
        self.play(ReplacementTransform(cap5, cap_master_geo), FadeOut(note_outphase), run_time=1.0)
        self.wait(6.5)

        self.fade_out_all(run_time=1.0)


class DS06_SmallAngleSpacing(SafeScene):
    """
    Beat 6: Small-Angle Approximation & Fringe Spacing (~85s)
    Locked Front-on view of screen with intensity plot.
    Micro-beats:
      1. Screen view & fringe orders m (18s)
      2. Small-angle approximation sin(theta) approx tan(theta) approx y/L (20s)
      3. Step-by-step derivation of y_m and constant Delta y (22s)
      4. Screen dimension brace aligned with intensity peaks (25s)
    """
    def construct(self):
        # 1. Screen Representation with Stripes & Orders m (Micro-beat 1: ~18s)
        pref = page_ref("Beat 6 · ระยะห่างระหว่างริ้วแถบ")
        ttl = title("Fringe Spacing & Small-Angle Approximation", size=25)
        cap1 = caption_top("การสังเกตจริงบนฉากรับภาพ: วัดระยะห่างระหว่างริ้วสว่างแต่ละแถบ (y)")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.2)
        self.wait(3.5)

        scr_bg = Rectangle(width=2.6, height=5.2, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([-3.4, -0.2, 0])
        scr_title = Text("ภาพจริงบนฉาก", font_size=16, color=WHITE).next_to(scr_bg.get_top(), UP, buff=0.1)

        fringe_data = [
            (1.8, "m = +2", C_BRIGHT),
            (0.9, "m = +1", C_BRIGHT),
            (0.0, "m = 0 (แถบสว่างกลาง)", C_BRIGHT),
            (-0.9, "m = -1", C_BRIGHT),
            (-1.8, "m = -2", C_BRIGHT),
        ]

        fringes = VGroup()
        fringe_labels = VGroup()
        for y_pos, m_txt, col in fringe_data:
            bar = Rectangle(width=2.2, height=0.32, color=col, fill_opacity=0.88, fill_color=col).move_to([-3.4, y_pos - 0.2, 0])
            lbl = Text(m_txt, font_size=12, color=WHITE).next_to(bar, LEFT, buff=0.1)
            fringes.add(bar)
            fringe_labels.add(lbl)

        brace_dy = BraceBetweenPoints([-3.4 + 1.2, -0.2, 0], [-3.4 + 1.2, 0.7, 0], RIGHT, color=C_ANGLE)
        lbl_dy = MathTex("\\Delta y", font_size=18, color=C_ANGLE).next_to(brace_dy, RIGHT, buff=0.08)

        self.play(
            FadeIn(scr_bg), FadeIn(scr_title),
            FadeIn(fringes), FadeIn(fringe_labels),
            Create(brace_dy), FadeIn(lbl_dy),
            run_time=2.2
        )
        self.wait(6.5)

        # 2. Geometry of Screen Distance & Small-Angle Approx (Micro-beat 2: ~20s)
        cap2 = caption_top("เมื่อมุม theta มีขนาดเล็กมาก (theta << 1 rad): ประมาณว่า sin(theta) approx tan(theta) approx y/L")
        self.play(ReplacementTransform(cap1, cap2), run_time=1.0)
        self.wait(4.5)

        deriv_box = RoundedRectangle(width=5.6, height=4.8, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.88).move_to([3.1, -0.2, 0])

        step1 = MathTex("\\tan\\theta = \\frac{y}{L}", font_size=20, color=WHITE).move_to([3.1, 1.7, 0])
        step2 = MathTex(r"\sin\theta \approx \tan\theta \approx \frac{y}{L} \quad (\theta \ll 1)", font_size=19, color=C_ANGLE).move_to([3.1, 1.05, 0])

        self.play(
            FadeIn(deriv_box),
            Write(step1),
            run_time=1.5
        )
        self.wait(3.5)

        self.play(Write(step2), run_time=1.8)

        ex_angle = Text("ตัวอย่างจริง: y = 5 mm, L = 1.5 m -> theta approx 0.19 deg คลาดเคลื่อนน้อยกว่า 0.01%", font_size=11.5, color=GRAYTXT).move_to([3.1, 0.5, 0])
        self.play(FadeIn(ex_angle), run_time=1.2)
        self.wait(7.0)

        # 3. Step-by-Step Derivation of y_m and Constant Delta y (Micro-beat 3: ~26s)
        cap3 = caption_top("แทนค่าลงในเงื่อนไขแถบสว่าง: หาตำแหน่ง y_m และระยะห่าง Delta y ระหว่างแถบติดกัน")
        self.play(ReplacementTransform(cap2, cap3), FadeOut(ex_angle), run_time=1.0)

        step3 = MathTex("d\\left(\\frac{y}{L}\\right) \\approx m\\lambda \\implies y_m \\approx m\\frac{\\lambda L}{d}", font_size=19, color=C_BRIGHT).move_to([3.1, 0.45, 0])
        step4 = MathTex("y_{m+1} \\approx (m+1)\\frac{\\lambda L}{d}, \\quad y_m \\approx m\\frac{\\lambda L}{d}", font_size=18, color=WHITE).move_to([3.1, -0.15, 0])
        step5 = MathTex("\\Delta y = y_{m+1} - y_m \\approx \\frac{\\lambda L}{d}", font_size=21, color=OK).move_to([3.1, -0.75, 0])

        self.play(Write(step3), run_time=2.0)
        self.wait(5.0)

        self.play(Write(step4), run_time=2.0)
        self.wait(4.5)

        self.play(Write(step5), run_time=2.0)
        self.wait(8.0)

        # 4. Screen Dimension Brace Aligned with Intensity Peaks (Micro-beat 4: ~25s)
        cap4 = caption_top("ทาบระยะวัด: ปีกกา Delta y บนฉากตรงกับระยะห่างระหว่างยอดกราฟความเข้ม (Peak-to-Peak) พอดี")
        self.play(ReplacementTransform(cap3, cap4), run_time=1.0)

        law_exact = MathTex("I(\\theta) = 4I_0 \\cos^2\\left(\\frac{\\pi d\\sin\\theta}{\\lambda}\\right)", font_size=16.5, color=WHITE).move_to([3.1, -1.4, 0])
        law_approx = MathTex("I(y) \\approx 4I_0 \\cos^2\\left(\\frac{\\pi d y}{\\lambda L}\\right)", font_size=16.5, color=C_DIFF).move_to([3.1, -1.95, 0])

        self.play(FadeIn(law_exact), FadeIn(law_approx), run_time=2.0)
        self.wait(9.5)

        note_const = Text("ข้อสังเกต: Delta y เป็นค่าคงที่ ทุกริ้วสว่างจึงเว้นช่องไฟเท่ากันเสมอ", font_size=13, color=OK).move_to([0, -3.1, 0])
        self.play(FadeIn(note_const), run_time=1.0)
        self.wait(8.0)

        self.fade_out_all(run_time=1.0)
