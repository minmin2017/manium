"""
double_slit_02_apparatus_paths.py
Module 2: Young's Double-Slit Wave Interference
Scenes:
  - DS03_ApparatusCoherence (Target: >= 65s, Planned: ~68s)
  - DS04_PointPInvestigation (Target: >= 105s, Planned: ~115s)
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
    Beat 3: Apparatus & Coherence (~68s)
    Builds the apparatus in 3D, names all physical components with pointers/flashes,
    proves incident wavefront hits openings before outgoing circular fronts,
    and visualizes coherent clocks before transitioning to Top View.
    """
    def construct(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-55 * DEGREES)

        # 1. Title & Physical Apparatus Setup (Micro-beat 1: ~20s)
        pref = self.hud(page_ref("Beat 3 · อุปกรณ์และคลื่นอาพันธ์"))
        ttl = self.hud(title("Apparatus & Coherent Sources", size=26))
        cap1 = self.hud(caption_top("โครงสร้างอุปกรณ์การทดลองของยัง: แหล่งกำเนิด, แผ่นกั้นสองช่อง (สลิตคู่), และฉากรับภาพ"))

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.2)
        self.wait(4.5)

        src_x = -4.2
        b_x = -1.2
        scr_x = 3.2
        d_val = 1.2  # distance between slits

        src_pt = np.array([src_x, 0.0, 0.0])
        src_sphere = Dot3D(point=src_pt, radius=0.22, color=C_SOURCE)
        src_tag = self.world_text(Text("แหล่งกำเนิดแสงเดี่ยว", font_size=15, color=C_SOURCE).next_to(src_pt, LEFT, buff=0.15))

        top_blk = Rectangle(width=0.12, height=1.3, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, 1.25, 0])
        mid_blk = Rectangle(width=0.12, height=0.6, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, 0.0, 0])
        bot_blk = Rectangle(width=0.12, height=1.3, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, -1.25, 0])
        barrier = VGroup(top_blk, mid_blk, bot_blk)

        s1_pt = np.array([b_x, d_val / 2, 0.0])
        s2_pt = np.array([b_x, -d_val / 2, 0.0])
        dot_s1 = Dot3D(point=s1_pt, radius=0.1, color=C_S1)
        dot_s2 = Dot3D(point=s2_pt, radius=0.1, color=C_S2)
        lbl_s1 = self.world_text(Text("S1", font_size=16, color=C_S1).next_to(s1_pt, UP, buff=0.1))
        lbl_s2 = self.world_text(Text("S2", font_size=16, color=C_S2).next_to(s2_pt, DOWN, buff=0.1))

        brace_d = BraceBetweenPoints([b_x - 0.2, -d_val / 2, 0], [b_x - 0.2, d_val / 2, 0], LEFT, color=WHITE)
        lbl_d = self.world_text(MathTex("d", font_size=22, color=WHITE).next_to(brace_d, LEFT, buff=0.08))

        screen_plane = Rectangle(width=0.15, height=3.4, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([scr_x, 0, 0])
        lbl_scr = self.world_text(Text("ฉากรับภาพ (Screen)", font_size=16, color=GRAYTXT).next_to(screen_plane, RIGHT, buff=0.15))

        line_L = Line([b_x, -1.9, 0], [scr_x, -1.9, 0], color=GRAYTXT, stroke_width=1.5)
        lbl_L = self.world_text(MathTex("L", font_size=22, color=GRAYTXT).next_to(line_L, DOWN, buff=0.08))

        # Flash & introduce Source
        cap_src = self.hud(caption_top("1. แหล่งกำเนิดแสงเดี่ยว (Single Source): ส่งคลื่นแสงที่มีความถี่และความยาวคลื่นเดียวกัน"))
        self.play(ReplacementTransform(cap1, cap_src), FadeIn(src_sphere), FadeIn(src_tag), run_time=1.5)
        self.wait(5.0)

        # Flash & introduce Slits and separation d
        cap_slit = self.hud(caption_top("2. แผ่นสลิตคู่ (Double Slits): มีช่องเปิดแคบ 2 ช่อง S1 และ S2 ห่างกันเป็นระยะ d"))
        self.play(
            ReplacementTransform(cap_src, cap_slit),
            FadeIn(barrier),
            FadeIn(dot_s1), FadeIn(dot_s2), FadeIn(lbl_s1), FadeIn(lbl_s2),
            Create(brace_d), FadeIn(lbl_d),
            run_time=2.0
        )
        self.wait(5.5)

        # Flash & introduce Screen and distance L
        cap_scr_intro = self.hud(caption_top("3. ฉากรับภาพ (Screen): วางห่างออกไปเป็นระยะ L (ในการทดลองจริง L >> d อย่างมาก)"))
        self.play(
            ReplacementTransform(cap_slit, cap_scr_intro),
            FadeIn(screen_plane), FadeIn(lbl_scr),
            Create(line_L), FadeIn(lbl_L),
            run_time=1.8
        )
        self.wait(5.5)

        # 2. Incident Wavefronts Arriving at Slits First (Micro-beat 2: ~18s)
        cap2 = self.hud(caption_top("คลื่นระนาบเดินทางจากแหล่งกำเนิดเดี่ยว: หน้าคลื่นชนสองช่อง S1 และ S2 พร้อมกันสนิท"))
        self.play(ReplacementTransform(cap_scr_intro, cap2), run_time=1.0)

        pw1 = line3([-3.6, -1.3, 0], [-3.6, 1.3, 0], color=C_SOURCE, thickness=0.02)
        pw2 = line3([-2.8, -1.3, 0], [-2.8, 1.3, 0], color=C_SOURCE, thickness=0.02)
        pw3 = line3([-2.0, -1.3, 0], [-2.0, 1.3, 0], color=C_SOURCE, thickness=0.02)
        pw_hit = line3([b_x, -1.3, 0], [b_x, 1.3, 0], color=C_SOURCE, thickness=0.032)

        self.play(Create(pw1), run_time=1.2)
        self.play(Create(pw2), run_time=1.2)
        self.play(Create(pw3), run_time=1.2)
        self.play(Create(pw_hit), run_time=1.4)

        flash_s1 = Dot3D(point=s1_pt, radius=0.18, color=WHITE)
        flash_s2 = Dot3D(point=s2_pt, radius=0.18, color=WHITE)
        self.play(FadeIn(flash_s1), FadeIn(flash_s2), run_time=0.6)
        self.play(FadeOut(flash_s1), FadeOut(flash_s2), run_time=0.6)

        cap_dist_check = self.hud(caption_top("เพราะระยะทางจากแหล่งกำเนิดถึง S1 และ S2 เท่ากัน สันคลื่นจึงชนทั้งสองช่องในเวลาเดียวกันเป๊ะ"))
        self.play(ReplacementTransform(cap2, cap_dist_check), run_time=1.0)
        self.wait(6.0)

        # 3. Synchronized Secondary Wavefronts & Coherent Clocks (Micro-beat 3: ~18s)
        cap3 = self.hud(caption_top("หลักการของฮอยเกนส์: S1 และ S2 ทำหน้าที่เป็นแหล่งกำเนิดใหม่ ปล่อยคลื่นชุดใหม่ออกมาพร้อมกัน"))
        self.play(ReplacementTransform(cap_dist_check, cap3), run_time=1.0)

        arcs_s1 = VGroup(*[Arc(radius=r, start_angle=-PI/3, angle=2*PI/3, arc_center=s1_pt, color=C_S1, stroke_width=2.5) for r in [0.4, 0.8, 1.2, 1.6]])
        arcs_s2 = VGroup(*[Arc(radius=r, start_angle=-PI/3, angle=2*PI/3, arc_center=s2_pt, color=C_S2, stroke_width=2.5) for r in [0.4, 0.8, 1.2, 1.6]])

        clock1_bg = Circle(radius=0.32, color=C_S1, stroke_width=1.8).move_to([b_x - 0.8, d_val / 2 + 0.65, 0])
        clock2_bg = Circle(radius=0.32, color=C_S2, stroke_width=1.8).move_to([b_x - 0.8, -d_val / 2 - 0.65, 0])
        clock1_h = Arrow(clock1_bg.get_center(), clock1_bg.get_center() + [0.24, 0, 0], color=WHITE, buff=0, stroke_width=2.5, tip_length=0.1)
        clock2_h = Arrow(clock2_bg.get_center(), clock2_bg.get_center() + [0.24, 0, 0], color=WHITE, buff=0, stroke_width=2.5, tip_length=0.1)
        clock_lbl = self.world_text(Text("เฟสตรงกันตลอดเวลา", font_size=13, color=WHITE).next_to(clock1_bg, UP, buff=0.08))
        clocks = VGroup(clock1_bg, clock2_bg, clock1_h, clock2_h, clock_lbl)

        self.play(
            Create(arcs_s1), Create(arcs_s2),
            FadeIn(clocks),
            run_time=3.0
        )
        self.wait(4.5)

        cap_cohere_def = self.hud(caption_top("นิยามคลื่นอาพันธ์ (Coherence): คลื่นมีความถี่เท่ากัน และความต่างเฟสคงที่ตลอดเวลา"))
        self.play(ReplacementTransform(cap3, cap_cohere_def), run_time=1.0)
        self.wait(6.5)

        # 4. Transition to Top View (Micro-beat 4: ~14s)
        cap4 = self.hud(caption_top("เปลี่ยนสู่มุมมองระนาบด้านบน (Top View) เพื่อวิเคราะห์เรขาคณิตของผลต่างเส้นทางเดินแสง"))
        self.play(ReplacementTransform(cap_cohere_def, cap4), run_time=1.0)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=3.5)
        self.wait(6.0)

        self.fade_out_all(run_time=1.0)


class DS04_PointPInvestigation(SafeScene):
    """
    Beat 4: Investigating Point P on Screen (~115s)
    Locked Top View.
    Micro-beats:
      1. Top View geometry setup, center point P0, paths r1 and r2 (20s)
      2. Wave packets travel to P0, same-frame arrival, bright flash (22s)
      3. Move P to first minimum P1, compute r1, r2, Delta r = lambda/2, dark sum (26s)
      4. Move P to first maximum P2 (m=1), Delta r = lambda, bright sum (22s)
      5. Live path difference dashboard & phase dial (16s)
      6. Front-screen inset & continuous sweep accumulation (22s)
    """
    def construct(self):
        # 1. Top View Geometry & Center Point P0 (Micro-beat 1: ~20s)
        pref = page_ref("Beat 4 · สังเกตที่จุด P บนฉาก")
        ttl = title("Point P Investigation: Path Difference", size=26)
        cap1 = caption_top("กรณีที่ 1: ตรวจวัดที่จุดกึ่งกลางฉาก P0 (y = 0) สองเส้นทางมีระยะทางเท่ากันพอดี")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.2)
        self.wait(3.5)

        b_x = -3.5
        scr_x = 2.5
        d_val = 2.0

        s1_pt = np.array([b_x, d_val / 2, 0])
        s2_pt = np.array([b_x, -d_val / 2, 0])

        b_line = Line([b_x, -2.5, 0], [b_x, 2.5, 0], color=C_BARRIER, stroke_width=4)
        dot_s1 = Dot(s1_pt, color=C_S1, radius=0.1)
        dot_s2 = Dot(s2_pt, color=C_S2, radius=0.1)
        lbl_s1 = Text("S1", font_size=16, color=C_S1).next_to(dot_s1, LEFT, buff=0.12)
        lbl_s2 = Text("S2", font_size=16, color=C_S2).next_to(dot_s2, LEFT, buff=0.12)

        scr_line = Line([scr_x, -2.5, 0], [scr_x, 2.5, 0], color=C_SCREEN, stroke_width=5)
        scr_tag = Text("ฉาก (Screen)", font_size=16, color=GRAYTXT).next_to(scr_line.get_top(), UP, buff=0.1)
        c_axis = DashedLine([b_x, 0, 0], [scr_x, 0, 0], color=GRAYTXT, stroke_width=1.5)

        self.play(
            Create(b_line), FadeIn(dot_s1), FadeIn(dot_s2), FadeIn(lbl_s1), FadeIn(lbl_s2),
            Create(scr_line), FadeIn(scr_tag), Create(c_axis),
            run_time=2.0
        )

        p0_pt = np.array([scr_x, 0.0, 0.0])
        dot_p = Dot(p0_pt, color=C_PROBE, radius=0.13)
        lbl_p = Text("P0 (ศูนย์กลาง y = 0)", font_size=15, color=C_PROBE).next_to(dot_p, RIGHT, buff=0.12)

        ray1_p0 = Line(s1_pt, p0_pt, color=C_S1, stroke_width=2.5)
        ray2_p0 = Line(s2_pt, p0_pt, color=C_S2, stroke_width=2.5)
        lbl_r1_p0 = MathTex("r_1", font_size=18, color=C_S1).move_to([-0.8, 0.65, 0])
        lbl_r2_p0 = MathTex("r_2", font_size=18, color=C_S2).move_to([-0.8, -0.65, 0])

        self.play(
            FadeIn(dot_p), FadeIn(lbl_p),
            Create(ray1_p0), Create(ray2_p0),
            FadeIn(lbl_r1_p0), FadeIn(lbl_r2_p0),
            run_time=2.0
        )
        self.wait(4.0)

        proof_p0 = MathTex("r_1 = r_2 \\implies \\Delta r = |r_2 - r_1| = 0", font_size=20, color=WHITE).move_to([0, -2.7, 0])
        self.play(FadeIn(proof_p0), run_time=1.2)
        self.wait(5.5)

        # 2. Wave Packets Travel to P0, Same-Frame Arrival, Bright Flash (Micro-beat 2: ~22s)
        cap_travel_p0 = caption_top("ก้อนคลื่นออกจาก S1 และ S2 พร้อมกัน เดินทางระยะทางเท่ากัน มาถึง P0 ในเฟรมเดียวกัน!")
        self.play(ReplacementTransform(cap1, cap_travel_p0), run_time=1.0)

        pkt1 = Dot(s1_pt, color=C_S1, radius=0.1)
        pkt2 = Dot(s2_pt, color=C_S2, radius=0.1)
        self.add(pkt1, pkt2)
        self.play(
            pkt1.animate.move_to(p0_pt),
            pkt2.animate.move_to(p0_pt),
            rate_func=linear, run_time=3.5
        )
        self.remove(pkt1, pkt2)

        flash_p0 = Dot(p0_pt, color=C_BRIGHT, radius=0.28).set_opacity(0.9)
        lbl_bright = Text("สว่างจ้า! สันชนสัน เสริมกัน 4 เท่า", font_size=15, color=C_BRIGHT).next_to(dot_p, RIGHT, buff=0.15)
        self.play(FadeIn(flash_p0), ReplacementTransform(lbl_p, lbl_bright), run_time=1.2)
        self.wait(5.5)

        note_bright = Text("แถบสว่างกลาง (Central Maximum): ผลต่างเส้นทางเป็นศูนย์เสมอ", font_size=13.5, color=C_BRIGHT).move_to([0, -3.1, 0])
        self.play(FadeIn(note_bright), run_time=1.0)
        self.wait(6.0)

        # 3. Move P to First Minimum P1, Paths, Extra Path Delta r = lambda/2 (Micro-beat 3: ~26s)
        cap2 = caption_top("กรณีที่ 2: เลื่อนจุดตรวจวัดขึ้นไปที่จุด P1 -> เส้นทาง r2 ยาวกว่า r1 เกิดผลต่างทางเดิน")
        p1_pt = np.array([scr_x, 1.0, 0.0])
        ray1_p1 = Line(s1_pt, p1_pt, color=C_S1, stroke_width=2.5)
        ray2_p1 = Line(s2_pt, p1_pt, color=C_S2, stroke_width=2.5)

        r1_len = np.linalg.norm(p1_pt - s1_pt)
        r2_len = np.linalg.norm(p1_pt - s2_pt)
        u2 = (s2_pt - p1_pt) / r2_len
        extra_start = p1_pt + u2 * r1_len
        extra_seg = Line(s2_pt, extra_start, color=C_DIFF, stroke_width=5.0)
        lbl_delta = MathTex("\\Delta r = \\frac{\\lambda}{2}", font_size=20, color=C_DIFF).next_to(extra_seg, DOWN, buff=0.1)

        self.play(
            ReplacementTransform(cap_travel_p0, cap2),
            FadeOut(flash_p0), FadeOut(lbl_bright), FadeOut(proof_p0), FadeOut(note_bright),
            FadeOut(lbl_r1_p0), FadeOut(lbl_r2_p0),
            ReplacementTransform(ray1_p0, ray1_p1),
            ReplacementTransform(ray2_p0, ray2_p1),
            dot_p.animate.move_to(p1_pt),
            run_time=2.2
        )
        self.play(Create(extra_seg), FadeIn(lbl_delta), run_time=1.8)
        self.wait(4.5)

        cap_dark_travel = caption_top("เพราะ r2 ยาวกว่าอยู่ครึ่งความยาวคลื่น (lambda/2): คลื่นสองจึงมาถึงแบบสันชนท้อง หักล้างหมดจด!")
        self.play(ReplacementTransform(cap2, cap_dark_travel), run_time=1.0)

        pkt1_dark = Dot(s1_pt, color=C_S1, radius=0.1)
        pkt2_dark = Dot(s2_pt, color=C_S2, radius=0.1)
        self.add(pkt1_dark, pkt2_dark)
        self.play(
            pkt1_dark.animate.move_to(p1_pt),
            pkt2_dark.animate.move_to(p1_pt),
            rate_func=linear, run_time=3.5
        )
        self.remove(pkt1_dark, pkt2_dark)

        dark_marker = Dot(p1_pt, color=C_DARK, radius=0.16)
        lbl_dark = Text("มืดสนิท! สันชนท้อง หักล้างเป็นศูนย์", font_size=15, color=WARN).next_to(p1_pt, RIGHT, buff=0.15)
        self.play(FadeIn(dark_marker), FadeIn(lbl_dark), run_time=1.2)
        self.wait(7.0)

        # 4. Move P to First Side Maximum P2 (m=1) (Micro-beat 4: ~22s)
        cap_p2 = caption_top("กรณีที่ 3: เลื่อนจุดตรวจวัดขึ้นไปอีกจน Delta r = 1 lambda เต็ม: สันจะวนกลับมาชนสันอีกครั้ง!")
        p2_pt = np.array([scr_x, 2.0, 0.0])
        ray1_p2 = Line(s1_pt, p2_pt, color=C_S1, stroke_width=2.5)
        ray2_p2 = Line(s2_pt, p2_pt, color=C_S2, stroke_width=2.5)

        r1_len2 = np.linalg.norm(p2_pt - s1_pt)
        r2_len2 = np.linalg.norm(p2_pt - s2_pt)
        u2_p2 = (s2_pt - p2_pt) / r2_len2
        extra_start2 = p2_pt + u2_p2 * r1_len2
        extra_seg2 = Line(s2_pt, extra_start2, color=C_DIFF, stroke_width=5.0)
        lbl_delta2 = MathTex("\\Delta r = 1\\lambda", font_size=20, color=C_DIFF).next_to(extra_seg2, DOWN, buff=0.1)

        self.play(
            ReplacementTransform(cap_dark_travel, cap_p2),
            FadeOut(extra_seg), FadeOut(lbl_delta), FadeOut(lbl_dark), FadeOut(dark_marker),
            ReplacementTransform(ray1_p1, ray1_p2),
            ReplacementTransform(ray2_p1, ray2_p2),
            dot_p.animate.move_to(p2_pt),
            run_time=2.2
        )
        self.play(Create(extra_seg2), FadeIn(lbl_delta2), run_time=1.8)
        self.wait(3.5)

        pkt1_p2 = Dot(s1_pt, color=C_S1, radius=0.1)
        pkt2_p2 = Dot(s2_pt, color=C_S2, radius=0.1)
        self.add(pkt1_p2, pkt2_p2)
        self.play(
            pkt1_p2.animate.move_to(p2_pt),
            pkt2_p2.animate.move_to(p2_pt),
            rate_func=linear, run_time=3.5
        )
        self.remove(pkt1_p2, pkt2_p2)

        flash_p2 = Dot(p2_pt, color=C_BRIGHT, radius=0.25).set_opacity(0.9)
        lbl_bright2 = Text("แถบสว่างที่ 1 (m = 1) สันชนสันอีกครั้ง", font_size=15, color=C_BRIGHT).next_to(p2_pt, RIGHT, buff=0.15)
        self.play(FadeIn(flash_p2), FadeIn(lbl_bright2), run_time=1.2)
        self.wait(7.0)

        # 5. Live Path Difference Dashboard (Micro-beat 5: ~16s)
        cap3 = caption_top("แดชบอร์ดความสัมพันธ์: ผลต่างเส้นทาง Delta r เป็นตัวตัดสินเฟสและความสว่างอย่างสมบูรณ์")
        self.play(
            ReplacementTransform(cap_p2, cap3),
            FadeOut(extra_seg2), FadeOut(lbl_delta2), FadeOut(lbl_bright2), FadeOut(flash_p2),
            run_time=1.2
        )

        dash_box = RoundedRectangle(width=5.2, height=1.6, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.88).move_to([-4.1, 2.3, 0])
        r_info1 = Text("Delta r = m*lambda  -->  เฟสตรงกัน (แถบสว่าง)", font_size=13, color=C_BRIGHT).move_to([-4.1, 2.7, 0])
        r_info2 = Text("Delta r = (m+1/2)*lambda  -->  เฟสตรงข้าม (แถบมืด)", font_size=13, color=WARN).move_to([-4.1, 2.2, 0])
        r_info3 = Text("ทุกๆ 0.5 lambda จะสลับระหว่างสว่างและมืด", font_size=12.5, color=WHITE).move_to([-4.1, 1.7, 0])
        dash_grp = VGroup(dash_box, r_info1, r_info2, r_info3)

        self.play(FadeIn(dash_grp), run_time=1.5)
        self.wait(7.5)

        # 6. Front-Screen Inset & Continuous Sweep Accumulation (Micro-beat 6: ~22s)
        cap4 = caption_top("กวาดจุด P ตลอดแนวฉาก: สะสมความเข้มแสงเป็นริ้วสว่าง-มืดต่อเนื่องตามฟังก์ชันโคไซน์")
        self.play(ReplacementTransform(cap3, cap4), run_time=1.0)

        inset_box = Rectangle(width=2.5, height=4.5, color=GRAYTXT, stroke_width=1.5).move_to([5.0, 0, 0])
        inset_title = Text("ริ้วแสงบนฉาก", font_size=14, color=WHITE).next_to(inset_box.get_top(), UP, buff=0.08)

        axes = Axes(
            x_range=[0, 4.2, 1], y_range=[-2.2, 2.2, 1],
            x_length=1.8, y_length=4.0,
            axis_config={"include_ticks": False, "stroke_color": GRAYTXT, "stroke_width": 1}
        ).move_to([5.0, 0, 0])

        intensity_curve = axes.plot(
            lambda y: 4.0 * (np.cos(PI * y / 1.0) ** 2),
            x_range=[-2.0, 2.0],
            color=C_BRIGHT, stroke_width=2.5
        )

        self.play(FadeIn(inset_box), FadeIn(inset_title), Create(axes), Create(intensity_curve), run_time=2.0)

        p_track = Dot([scr_x, -2.0, 0], color=C_PROBE, radius=0.1)
        r1_sweep = Line(s1_pt, [scr_x, -2.0, 0], color=C_S1, stroke_width=2)
        r2_sweep = Line(s2_pt, [scr_x, -2.0, 0], color=C_S2, stroke_width=2)

        self.play(
            ReplacementTransform(ray1_p2, r1_sweep),
            ReplacementTransform(ray2_p2, r2_sweep),
            ReplacementTransform(dot_p, p_track),
            FadeOut(dash_grp),
            run_time=1.2
        )

        self.play(
            p_track.animate.move_to([scr_x, 2.0, 0]),
            r1_sweep.animate.put_start_and_end_on(s1_pt, [scr_x, 2.0, 0]),
            r2_sweep.animate.put_start_and_end_on(s2_pt, [scr_x, 2.0, 0]),
            rate_func=linear, run_time=7.5
        )
        self.wait(6.5)

        self.fade_out_all(run_time=1.0)
