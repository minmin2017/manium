"""
double_slit_02_apparatus_paths.py
Module 2: Young's Double-Slit Wave Interference
Scenes:
  - DS03_ApparatusCoherence (~65s)
  - DS04_PointPInvestigation (~100s)
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Color Palette
C_SOURCE  = "#FFD54F"  # Light Source (Amber)
C_BARRIER = "#78909C"  # Barrier (Slate)
C_SCREEN  = "#37474F"  # Screen (Dark Slate)
C_S1      = "#42A5F5"  # Slit S1 (Blue)
C_S2      = "#FF7043"  # Slit S2 (Orange)
C_DIFF    = "#E91E63"  # Path difference delta (Magenta/Rose)
C_BRIGHT  = "#00E676"  # Constructive / Bright (Neon Green)
C_DARK    = "#1A237E"  # Destructive / Dark (Deep Indigo)
C_PROBE   = "#FFEA00"  # Point P (Yellow)


class DS03_ApparatusCoherence(SafeThreeDScene):
    """
    Beat 3: Apparatus & Coherence (~65s)
    Builds the apparatus in 3D, names all physical components,
    and proves that secondary circular wavefronts emit only after the
    incident plane wave reaches the two slits in lockstep (Coherence).
    """
    def construct(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-55 * DEGREES)

        pref = self.hud(page_ref("Beat 3 · อุปกรณ์และคลื่นอาพันธ์"))
        ttl = self.hud(title("Apparatus & Coherent Sources", size=26))
        cap1 = self.hud(caption_top("โมเดลอุดมคติ: แหล่งกำเนิดเดี่ยว แตกเป็น 2 ช่องสลิตแคบ เพื่อสร้าง 'คลื่นอาพันธ์'"))

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 1. 3D Model Coordinates
        src_x = -4.2
        b_x = -1.2
        scr_x = 3.2
        d_val = 1.2  # distance between slits

        # Physical Source
        src_pt = np.array([src_x, 0.0, 0.0])
        src_sphere = Dot3D(point=src_pt, radius=0.2, color=C_SOURCE)
        src_tag = self.world_text(Text("แหล่งกำเนิด", font_size=15, color=C_SOURCE).next_to(src_pt, LEFT, buff=0.12))

        # Physical Barrier with two openings S1 and S2
        top_blk = Rectangle(width=0.12, height=1.3, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, 1.25, 0])
        mid_blk = Rectangle(width=0.12, height=0.6, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, 0.0, 0])
        bot_blk = Rectangle(width=0.12, height=1.3, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, -1.25, 0])
        barrier = VGroup(top_blk, mid_blk, bot_blk)

        s1_pt = np.array([b_x, d_val / 2, 0.0])
        s2_pt = np.array([b_x, -d_val / 2, 0.0])
        dot_s1 = Dot3D(point=s1_pt, radius=0.08, color=C_S1)
        dot_s2 = Dot3D(point=s2_pt, radius=0.08, color=C_S2)
        lbl_s1 = self.world_text(Text("S1", font_size=16, color=C_S1).next_to(s1_pt, UP, buff=0.08))
        lbl_s2 = self.world_text(Text("S2", font_size=16, color=C_S2).next_to(s2_pt, DOWN, buff=0.08))

        # Distance d between slits
        brace_d = BraceBetweenPoints([b_x - 0.2, -d_val / 2, 0], [b_x - 0.2, d_val / 2, 0], LEFT, color=WHITE)
        lbl_d = self.world_text(MathTex("d", font_size=20, color=WHITE).next_to(brace_d, LEFT, buff=0.08))

        # Screen at distance L
        screen_plane = Rectangle(width=0.15, height=3.4, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([scr_x, 0, 0])
        lbl_scr = self.world_text(Text("ฉากรับภาพ", font_size=16, color=GRAYTXT).next_to(screen_plane, RIGHT, buff=0.15))

        # Distance L between barrier and screen
        line_L = Line([b_x, -1.9, 0], [scr_x, -1.9, 0], color=GRAYTXT, stroke_width=1.5)
        lbl_L = self.world_text(MathTex("L", font_size=20, color=GRAYTXT).next_to(line_L, DOWN, buff=0.08))

        apparatus_grp = VGroup(src_sphere, src_tag, barrier, dot_s1, dot_s2, lbl_s1, lbl_s2, brace_d, lbl_d, screen_plane, lbl_scr, line_L, lbl_L)

        self.play(FadeIn(apparatus_grp), run_time=1.4)
        self.wait(0.8)

        # 2. Incoming Plane Waves (Arriving at Barrier)
        # Demonstrates strict acceptance rule: NO outgoing waves until incoming front reaches slits
        cap2 = self.hud(caption_top("คลื่นระนาบเดินทางจากแหล่งกำเนิด เข้าชนแผ่นกั้นพร้อมกันทั้งสองช่อง"))
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)

        pw1 = line3([-3.6, -1.3, 0], [-3.6, 1.3, 0], color=C_SOURCE, thickness=0.02)
        pw2 = line3([-2.8, -1.3, 0], [-2.8, 1.3, 0], color=C_SOURCE, thickness=0.02)
        pw3 = line3([-2.0, -1.3, 0], [-2.0, 1.3, 0], color=C_SOURCE, thickness=0.02)
        pw_hit = line3([b_x, -1.3, 0], [b_x, 1.3, 0], color=C_SOURCE, thickness=0.028)

        self.play(Create(pw1), run_time=0.6)
        self.play(Create(pw2), run_time=0.6)
        self.play(Create(pw3), run_time=0.6)
        self.play(Create(pw_hit), run_time=0.6)
        self.wait(0.4)

        # 3. Synchronized Secondary Waves emission from S1 and S2
        cap3 = self.hud(caption_top("ทันทีที่หน้าคลื่นชน: S1 และ S2 ปล่อยคลื่นชุดใหม่ขยายตัวออกพร้อมกันในจังหวะเดียวกัน"))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.5)

        # Expanding arcs from S1 and S2
        arcs_s1 = VGroup(*[Arc(radius=r, start_angle=-PI/3, angle=2*PI/3, arc_center=s1_pt, color=C_S1, stroke_width=2.5) for r in [0.4, 0.8, 1.2, 1.6]])
        arcs_s2 = VGroup(*[Arc(radius=r, start_angle=-PI/3, angle=2*PI/3, arc_center=s2_pt, color=C_S2, stroke_width=2.5) for r in [0.4, 0.8, 1.2, 1.6]])

        # Coherent Phase Clocks
        clock1_bg = Circle(radius=0.3, color=C_S1, stroke_width=1.5).move_to([b_x - 0.7, d_val / 2 + 0.6, 0])
        clock2_bg = Circle(radius=0.3, color=C_S2, stroke_width=1.5).move_to([b_x - 0.7, -d_val / 2 - 0.6, 0])
        clock1_h = Arrow(clock1_bg.get_center(), clock1_bg.get_center() + [0.22, 0, 0], color=WHITE, buff=0, stroke_width=2.5, tip_length=0.1)
        clock2_h = Arrow(clock2_bg.get_center(), clock2_bg.get_center() + [0.22, 0, 0], color=WHITE, buff=0, stroke_width=2.5, tip_length=0.1)
        clock_lbl = self.world_text(Text("เฟสตรงกัน", font_size=13, color=WHITE).next_to(clock1_bg, UP, buff=0.08))

        clocks = VGroup(clock1_bg, clock2_bg, clock1_h, clock2_h, clock_lbl)

        self.play(
            Create(arcs_s1), Create(arcs_s2),
            FadeIn(clocks),
            run_time=2.2
        )
        self.wait(1.5)

        # Transition smoothly to Top View for next beat
        cap4 = self.hud(caption_top("เปลี่ยนสู่มุมมองด้านบน (Top View) เพื่อวิเคราะห์เส้นทางเดินคลื่นไปยังจุด P"))
        self.play(ReplacementTransform(cap3, cap4), run_time=0.5)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.8)
        self.wait(0.8)

        self.fade_out_all(run_time=0.8)


class DS04_PointPInvestigation(SafeScene):
    """
    Beat 4: Investigating Point P on Screen (~100s)
    Locked Top View (first 60s without insets).
    Demonstrates:
      1. Center P (r1 = r2): Crest meets crest -> Bright sample.
      2. First Dark P (r2 - r1 = lambda/2): Crest meets trough -> Sum = 0.
      3. Live sweeping P with front-screen inset building intensity profile.
    """
    def construct(self):
        pref = page_ref("Beat 4 · สังเกตที่จุด P บนฉาก")
        ttl = title("Point P Investigation: Path Difference", size=26)
        cap1 = caption_top("ที่จุดกึ่งกลาง P0: ระยะทาง r1 = r2 ผลต่างทางเดินเป็นศูนย์ สันชนสันเกิดแถบสว่างกลาง")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 1. Top View Geometry Setup
        # Slit barrier at x = -3.5, Screen at x = 2.5
        b_x = -3.5
        scr_x = 2.5
        d_val = 2.0  # visual slit separation

        s1_pt = np.array([b_x, d_val / 2, 0])
        s2_pt = np.array([b_x, -d_val / 2, 0])

        # Barrier & Slit Points
        b_line = Line([b_x, -2.5, 0], [b_x, 2.5, 0], color=C_BARRIER, stroke_width=4)
        dot_s1 = Dot(s1_pt, color=C_S1, radius=0.1)
        dot_s2 = Dot(s2_pt, color=C_S2, radius=0.1)
        lbl_s1 = Text("S1", font_size=16, color=C_S1).next_to(dot_s1, LEFT, buff=0.12)
        lbl_s2 = Text("S2", font_size=16, color=C_S2).next_to(dot_s2, LEFT, buff=0.12)

        # Screen Line
        scr_line = Line([scr_x, -2.5, 0], [scr_x, 2.5, 0], color=C_SCREEN, stroke_width=5)
        scr_tag = Text("ฉาก (Screen)", font_size=16, color=GRAYTXT).next_to(scr_line.get_top(), UP, buff=0.1)

        # Center Axis
        c_axis = DashedLine([b_x, 0, 0], [scr_x, 0, 0], color=GRAYTXT, stroke_width=1.5)

        self.play(
            Create(b_line), FadeIn(dot_s1), FadeIn(dot_s2), FadeIn(lbl_s1), FadeIn(lbl_s2),
            Create(scr_line), FadeIn(scr_tag), Create(c_axis),
            run_time=1.2
        )

        # 2. Case 1: Point P at Center (y = 0)
        p0_pt = np.array([scr_x, 0.0, 0.0])
        dot_p = Dot(p0_pt, color=C_PROBE, radius=0.12)
        lbl_p = Text("P (ศูนย์กลาง)", font_size=15, color=C_PROBE).next_to(dot_p, RIGHT, buff=0.12)

        ray1_p0 = Line(s1_pt, p0_pt, color=C_S1, stroke_width=2.5)
        ray2_p0 = Line(s2_pt, p0_pt, color=C_S2, stroke_width=2.5)

        self.play(FadeIn(dot_p), FadeIn(lbl_p), Create(ray1_p0), Create(ray2_p0), run_time=1.0)

        # Animate traveling wave packets reaching P0 simultaneously
        pkt1 = Dot(s1_pt, color=C_S1, radius=0.08)
        pkt2 = Dot(s2_pt, color=C_S2, radius=0.08)
        self.add(pkt1, pkt2)
        self.play(
            pkt1.animate.move_to(p0_pt),
            pkt2.animate.move_to(p0_pt),
            rate_func=linear, run_time=1.5
        )
        self.remove(pkt1, pkt2)

        # Visual Proof: Constructive Flash at P0
        flash_p0 = Dot(p0_pt, color=C_BRIGHT, radius=0.25).set_opacity(0.9)
        lbl_bright = Text("สว่างมาก! (สันชนสัน)", font_size=16, color=C_BRIGHT).next_to(dot_p, RIGHT, buff=0.15)
        self.play(FadeIn(flash_p0), ReplacementTransform(lbl_p, lbl_bright), run_time=0.6)
        self.wait(1.5)

        # 3. Case 2: Move P to First Minimum (y = 1.0)
        cap2 = caption_top("เลื่อนจุด P ขึ้น: เส้นทาง r2 ยาวกว่า r1 เมื่อส่วนต่างเท่ากับ lambda/2 สันจะชนท้อง หักล้างเป็นแถบมืด")
        p1_pt = np.array([scr_x, 1.0, 0.0])
        ray1_p1 = Line(s1_pt, p1_pt, color=C_S1, stroke_width=2.5)
        ray2_p1 = Line(s2_pt, p1_pt, color=C_S2, stroke_width=2.5)

        # Calculate exact geometric point for perpendicular extra length lambda/2
        r1_len = np.linalg.norm(p1_pt - s1_pt)
        r2_len = np.linalg.norm(p1_pt - s2_pt)
        # Point on ray2 at distance r1_len from P
        u2 = (s2_pt - p1_pt) / r2_len
        extra_start = p1_pt + u2 * r1_len  # this segment [s2_pt, extra_start] is the extra length Delta r
        extra_seg = Line(s2_pt, extra_start, color=C_DIFF, stroke_width=4.5)
        lbl_delta = MathTex("\\Delta r = \\frac{\\lambda}{2}", font_size=18, color=C_DIFF).next_to(extra_seg, DOWN, buff=0.08)

        lbl_dark = Text("มืดสนิท! (สันชนท้อง)", font_size=16, color=WARN).next_to(p1_pt, RIGHT, buff=0.15)
        dark_marker = Dot(p1_pt, color=C_DARK, radius=0.15)

        self.play(
            ReplacementTransform(cap1, cap2),
            FadeOut(flash_p0), FadeOut(lbl_bright),
            ReplacementTransform(ray1_p0, ray1_p1),
            ReplacementTransform(ray2_p0, ray2_p1),
            dot_p.animate.move_to(p1_pt),
            run_time=1.2
        )
        self.play(Create(extra_seg), FadeIn(lbl_delta), run_time=0.8)

        # Moving Packets: Wave 1 sends crest, Wave 2 sends trough (arrive in exact same frame)
        pkt1_dark = Dot(s1_pt, color=C_S1, radius=0.09)
        pkt2_dark = Dot(s2_pt, color=C_S2, radius=0.09)
        self.add(pkt1_dark, pkt2_dark)
        self.play(
            pkt1_dark.animate.move_to(p1_pt),
            pkt2_dark.animate.move_to(p1_pt),
            rate_func=linear, run_time=1.5
        )
        self.remove(pkt1_dark, pkt2_dark)

        # Destructive Result
        self.play(FadeIn(dark_marker), FadeIn(lbl_dark), run_time=0.6)
        self.wait(1.8)

        # 4. Open Live Dashboard & Screen Inset on the Right
        cap3 = caption_top("กวาดจุด P ตลอดแนวฉาก: สะสมความเข้มแสงเป็นริ้วสว่าง-มืดต่อเนื่องตามฟังก์ชันโคไซน์")
        self.play(
            ReplacementTransform(cap2, cap3),
            FadeOut(extra_seg), FadeOut(lbl_delta), FadeOut(lbl_dark), FadeOut(dark_marker),
            run_time=0.8
        )

        # Dashboard HUD: Path difference and Phase dial at Top-Left
        dash_box = RoundedRectangle(width=3.2, height=1.3, corner_radius=0.1, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.85).move_to([-4.8, 2.7, 0])
        r1_txt = Text("r1: ทางเดินจาก S1", font_size=13, color=C_S1).move_to([-4.8, 3.0, 0])
        r2_txt = Text("r2: ทางเดินจาก S2", font_size=13, color=C_S2).move_to([-4.8, 2.7, 0])
        diff_txt = Text("Delta r = |r2 - r1|", font_size=14, color=C_DIFF).move_to([-4.8, 2.35, 0])
        dash_grp = VGroup(dash_box, r1_txt, r2_txt, diff_txt)

        # Front-Screen Strip & Intensity Curve on Right (x = 3.8 to 6.2)
        inset_box = Rectangle(width=2.5, height=4.5, color=GRAYTXT, stroke_width=1.5).move_to([5.0, 0, 0])
        inset_title = Text("ริ้วแสงบนฉาก", font_size=14, color=WHITE).next_to(inset_box.get_top(), UP, buff=0.08)

        # Intensity Graph I(y)
        axes = Axes(
            x_range=[0, 4.2, 1], y_range=[-2.2, 2.2, 1],
            x_length=1.8, y_length=4.0,
            axis_config={"include_ticks": False, "stroke_color": GRAYTXT, "stroke_width": 1}
        ).move_to([5.0, 0, 0])

        # Plot cos^2 curve
        intensity_curve = axes.plot(
            lambda y: 4.0 * (np.cos(PI * y / 1.0) ** 2),
            x_range=[-2.0, 2.0],
            color=C_BRIGHT, stroke_width=2.5
        )

        self.play(FadeIn(dash_grp), FadeIn(inset_box), FadeIn(inset_title), Create(axes), Create(intensity_curve), run_time=1.5)

        # Sweep P from y = -2.0 to y = 2.0
        p_track = Dot([scr_x, -2.0, 0], color=C_PROBE, radius=0.1)
        r1_sweep = Line(s1_pt, [scr_x, -2.0, 0], color=C_S1, stroke_width=2)
        r2_sweep = Line(s2_pt, [scr_x, -2.0, 0], color=C_S2, stroke_width=2)

        self.play(
            ReplacementTransform(ray1_p1, r1_sweep),
            ReplacementTransform(ray2_p1, r2_sweep),
            ReplacementTransform(dot_p, p_track),
            run_time=0.5
        )

        # Sweep animation
        self.play(
            p_track.animate.move_to([scr_x, 2.0, 0]),
            r1_sweep.animate.put_start_and_end_on(s1_pt, [scr_x, 2.0, 0]),
            r2_sweep.animate.put_start_and_end_on(s2_pt, [scr_x, 2.0, 0]),
            rate_func=linear, run_time=3.5
        )
        self.wait(1.5)

        self.fade_out_all(run_time=0.8)
