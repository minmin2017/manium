"""
double_slit_01_intro_wave.py
Module 1: Young's Double-Slit Wave Interference
Scenes:
  - DS01_ParadoxHook (~25s)
  - DS02_Wave101 (~65s)
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Color Palette
C_SOURCE  = "#FFD54F"  # Amber/Yellow for source
C_BARRIER = "#78909C"  # Blue-Gray for physical barrier
C_SCREEN  = "#37474F"  # Dark Slate for screen
C_BRIGHT  = "#00E676"  # Vivid Green for bright fringe
C_DARK    = "#1A237E"  # Deep Indigo/Black for dark fringe
C_WAVE1   = "#42A5F5"  # Light Blue (Wave 1 / S1)
C_WAVE2   = "#FF7043"  # Deep Orange (Wave 2 / S2)
C_SUM     = "#26C6DA"  # Cyan for superposed sum
C_PROBE   = "#FFEA00"  # Yellow for detection probe


class DS01_ParadoxHook(SafeThreeDScene):
    """
    Beat 1: The Double-Slit Paradox (~25s)
    Establishes 3D physical apparatus, poses the novice question,
    and zooms through the dark stripe as a causal bridge.
    """
    def construct(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-52 * DEGREES)

        # Fixed HUD text
        pref = self.hud(page_ref("Beat 1 · ปริศนาสลิตคู่"))
        ttl = self.hud(title("The Double-Slit Paradox", size=26))
        cap1 = self.hud(caption_top("ถ้าคลื่นแสงผ่านช่องเปิด 2 ช่อง... เราควรเห็นเพียง 2 แถบใช่หรือไม่?"))

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 3D Apparatus Construction
        # 1. Light Source at Left
        src_pt = np.array([-4.5, 0.0, 0.0])
        src_sphere = Dot3D(point=src_pt, radius=0.22, color=C_SOURCE)
        src_lbl = self.world_text(Text("แหล่งกำเนิด", font_size=16, color=C_SOURCE).next_to(src_pt, LEFT, buff=0.15))

        # 2. Barrier with Two Apertures
        # We split the barrier into three plates to leave two physical slits
        b_x = -1.5
        top_plate = Rectangle(width=0.1, height=1.6, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, 1.3, 0])
        mid_plate = Rectangle(width=0.1, height=0.6, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, 0.0, 0])
        bot_plate = Rectangle(width=0.1, height=1.6, color=C_BARRIER, fill_opacity=0.85, fill_color=METAL).move_to([b_x, -1.3, 0])
        barrier = VGroup(top_plate, mid_plate, bot_plate)

        s1_pt = np.array([b_x, 0.45, 0.0])
        s2_pt = np.array([b_x, -0.45, 0.0])
        s1_lbl = self.world_text(Text("S1", font_size=15, color=WHITE).next_to(s1_pt, UP, buff=0.08))
        s2_lbl = self.world_text(Text("S2", font_size=15, color=WHITE).next_to(s2_pt, DOWN, buff=0.08))

        # 3. Detection Screen at Right
        scr_x = 3.5
        screen_surf = Rectangle(width=0.15, height=3.6, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([scr_x, 0, 0])
        scr_lbl = self.world_text(Text("ฉากรับภาพ", font_size=16, color=GRAYTXT).next_to(screen_surf, RIGHT, buff=0.2))

        apparatus = VGroup(src_sphere, src_lbl, barrier, s1_lbl, s2_lbl, screen_surf, scr_lbl)
        self.play(FadeIn(apparatus), run_time=1.2)
        self.wait(0.8)

        # Incident Wavefronts traveling from Source to Barrier
        in_waves = VGroup()
        for x_pos in np.linspace(-4.0, -1.7, 5):
            w = line3([x_pos, -1.4, 0], [x_pos, 1.4, 0], color=C_SOURCE, thickness=0.02)
            in_waves.add(w)

        self.play(Create(in_waves), run_time=1.2)

        # Alternating Bright/Dark Fringes appearing on Screen
        fringes = VGroup()
        f_ys = [1.2, 0.8, 0.4, 0.0, -0.4, -0.8, -1.2]
        is_bright = [False, True, False, True, False, True, False]
        for y_f, bright in zip(f_ys, is_bright):
            col = C_BRIGHT if bright else C_DARK
            bar = Rectangle(width=0.18, height=0.28, color=col, fill_opacity=0.92, fill_color=col)
            bar.move_to([scr_x, y_f, 0.02])
            fringes.add(bar)

        cap2 = self.hud(caption_top("แต่ของจริง: เกิดริ้วมืดและสว่างสลับกัน! แสงมาเจอกันแล้วมืดได้อย่างไร?"))
        self.play(
            ReplacementTransform(cap1, cap2),
            FadeIn(fringes),
            run_time=1.5
        )
        self.wait(1.5)

        # Highlight first dark stripe (y = 0.4)
        dark_target = fringes[2]  # y = 0.4
        box_warn = Rectangle(width=0.35, height=0.35, color=WARN, stroke_width=3).move_to(dark_target.get_center())
        lbl_dark = self.world_text(Text("แถบมืด!", font_size=15, color=WARN).next_to(box_warn, UP + RIGHT, buff=0.1))

        self.play(Create(box_warn), FadeIn(lbl_dark), run_time=0.8)
        self.wait(1.0)

        # Camera physically zooms straight into that dark stripe as the causal bridge
        cap3 = self.hud(caption_top("ซูมเข้าไปดูระดับคลื่น: ความลับซ่อนอยู่ที่การรวมกันของจังหวะคลื่น"))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.5)
        self.move_camera(frame_center=[scr_x, 0.4, 0.0], zoom=3.2, run_time=2.2)
        self.wait(0.8)

        # Clean exit to next scene
        self.fade_out_all(run_time=0.8)


class DS02_Wave101(SafeScene):
    """
    Beat 2: Wave Fundamentals & Superposition (~65s)
    Locked 2D side view. Defines amplitude, wavelength, and demonstrates
    constructive and destructive interference at a probe physically.
    """
    def construct(self):
        pref = page_ref("Beat 2 · ธรรมชาติของคลื่น")
        ttl = title("Wave Fundamentals & Superposition", size=26)
        cap1 = caption_top("เส้นโค้งนี้แทน 'แอมพลิจูดของสนาม' ไม่ใช่อนุภาควิ่งตามเส้น")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 1. Single Wave Anatomy
        axis = Line([-5.5, 0.8, 0], [4.5, 0.8, 0], color=GRAYTXT, stroke_width=1.5)
        k = 2 * PI / 3.0  # wavelength lambda = 3.0 units

        def wave_func(x):
            return 0.8 * np.sin(k * (x + 5.5)) + 0.8

        single_wave = FunctionGraph(wave_func, x_range=[-5.5, 4.5], color=C_WAVE1, stroke_width=3.5)
        self.play(Create(axis), Create(single_wave), run_time=1.5)

        # Labels for Crest, Trough, Wavelength lambda
        crest_pt = np.array([-5.5 + 3.0 * 0.25, 1.6, 0])
        trough_pt = np.array([-5.5 + 3.0 * 0.75, 0.0, 0])

        lbl_crest = Text("สันคลื่น (Crest)", font_size=18, color=C_WAVE1).next_to(crest_pt, UP, buff=0.15)
        lbl_trough = Text("ท้องคลื่น (Trough)", font_size=18, color=C_WAVE1).next_to(trough_pt, DOWN, buff=0.15)
        dot_c = Dot(crest_pt, color=WHITE, radius=0.06)
        dot_t = Dot(trough_pt, color=WHITE, radius=0.06)

        # Lambda Brace
        brace_lam = BraceBetweenPoints(crest_pt, crest_pt + np.array([3.0, 0, 0]), UP, color=WHITE)
        lbl_lam = MathTex("\\lambda", font_size=24, color=WHITE).next_to(brace_lam, UP, buff=0.08)

        self.play(
            FadeIn(dot_c), FadeIn(lbl_crest),
            FadeIn(dot_t), FadeIn(lbl_trough),
            Create(brace_lam), FadeIn(lbl_lam),
            run_time=1.2
        )
        self.wait(1.5)

        # 2. Transition to Superposition at a Probe
        cap2 = caption_top("เมื่อคลื่นสองขบวนมาถึงจุดเดียวกันพร้อมกัน: สันชนสันจะเสริมกันเป็น 2 เท่า")
        self.play(
            FadeOut(single_wave), FadeOut(dot_c), FadeOut(lbl_crest),
            FadeOut(dot_t), FadeOut(lbl_trough), FadeOut(brace_lam), FadeOut(lbl_lam),
            ReplacementTransform(cap1, cap2),
            run_time=0.8
        )

        # Dual Rails for Wave 1 and Wave 2 arriving at Probe
        probe_x = 2.0
        probe_line = Line([probe_x, -2.5, 0], [probe_x, 1.8, 0], color=GRAYTXT, stroke_width=1.5)
        probe_lbl = Text("โพรบตรวจวัด P", font_size=16, color=C_PROBE).next_to(probe_line.get_top(), UP, buff=0.08)

        # Case A: In-Phase (Constructive)
        # Top wave (Wave 1) and Middle wave (Wave 2)
        rail1 = Line([-5.5, 1.0, 0], [probe_x, 1.0, 0], color=GRAYTXT, stroke_width=1)
        rail2 = Line([-5.5, -0.2, 0], [probe_x, -0.2, 0], color=GRAYTXT, stroke_width=1)
        sum_rail = Line([-5.5, -1.8, 0], [probe_x, -1.8, 0], color=GRAYTXT, stroke_width=1.5)

        lbl_w1 = Text("คลื่น 1", font_size=16, color=C_WAVE1).next_to(rail1.get_left(), LEFT, buff=0.1)
        lbl_w2 = Text("คลื่น 2", font_size=16, color=C_WAVE2).next_to(rail2.get_left(), LEFT, buff=0.1)
        lbl_sum = Text("ผลรวม (Sum)", font_size=16, color=C_SUM).next_to(sum_rail.get_left(), LEFT, buff=0.1)

        w1_curve = FunctionGraph(lambda x: 0.45 * np.sin(2 * PI * (x + 5.5) / 2.5) + 1.0, x_range=[-5.5, probe_x], color=C_WAVE1, stroke_width=3)
        w2_curve_in = FunctionGraph(lambda x: 0.45 * np.sin(2 * PI * (x + 5.5) / 2.5) - 0.2, x_range=[-5.5, probe_x], color=C_WAVE2, stroke_width=3)
        sum_curve_in = FunctionGraph(lambda x: 0.90 * np.sin(2 * PI * (x + 5.5) / 2.5) - 1.8, x_range=[-5.5, probe_x], color=C_SUM, stroke_width=4)

        probe_dot_in = Dot([probe_x, -1.8 + 0.90, 0], color=C_PROBE, radius=0.1)
        brace_2A = BraceBetweenPoints([probe_x + 0.1, -1.8, 0], [probe_x + 0.1, -1.8 + 0.90, 0], RIGHT, color=C_PROBE)
        lbl_2A = MathTex("2A", font_size=20, color=C_PROBE).next_to(brace_2A, RIGHT, buff=0.08)

        # Phase dial showing in-phase (0 deg)
        dial_box = RoundedRectangle(width=1.8, height=1.8, corner_radius=0.15, color=GRAYTXT, stroke_width=1.5).move_to([4.8, 0.0, 0])
        dial_center = dial_box.get_center()
        dial_circle = Circle(radius=0.6, color=GRAYTXT, stroke_width=1.5).move_to(dial_center)
        dial_hand1 = Arrow(dial_center, dial_center + [0.55, 0, 0], color=C_WAVE1, buff=0, stroke_width=3, tip_length=0.15)
        dial_hand2 = Arrow(dial_center, dial_center + [0.55, 0, 0], color=C_WAVE2, buff=0, stroke_width=3, tip_length=0.15)
        dial_lbl = Text("เฟสตรงกัน (0°)", font_size=14, color=WHITE).next_to(dial_box, DOWN, buff=0.1)

        dial_group = VGroup(dial_box, dial_circle, dial_hand1, dial_hand2, dial_lbl)

        self.play(
            FadeIn(probe_line), FadeIn(probe_lbl),
            FadeIn(rail1), FadeIn(rail2), FadeIn(sum_rail),
            FadeIn(lbl_w1), FadeIn(lbl_w2), FadeIn(lbl_sum),
            Create(w1_curve), Create(w2_curve_in), Create(sum_curve_in),
            FadeIn(probe_dot_in), Create(brace_2A), FadeIn(lbl_2A),
            FadeIn(dial_group),
            run_time=2.0
        )
        self.wait(1.8)

        # Case B: Out-of-Phase / Half-Cycle shift (Destructive)
        cap3 = caption_top("แต่ถ้าคลื่นสองเหลื่อมกันครึ่งรอบ (lambda/2): สันจะชนท้อง หักล้างกันจนนิ่งสนิท!")
        w2_curve_out = FunctionGraph(lambda x: -0.45 * np.sin(2 * PI * (x + 5.5) / 2.5) - 0.2, x_range=[-5.5, probe_x], color=C_WAVE2, stroke_width=3)
        sum_curve_out = Line([-5.5, -1.8, 0], [probe_x, -1.8, 0], color=C_SUM, stroke_width=4)
        probe_dot_out = Dot([probe_x, -1.8, 0], color=C_PROBE, radius=0.1)

        dial_hand2_out = Arrow(dial_center, dial_center + [-0.55, 0, 0], color=C_WAVE2, buff=0, stroke_width=3, tip_length=0.15)
        dial_lbl_out = Text("เฟสตรงข้าม (180°)", font_size=14, color=WARN).next_to(dial_box, DOWN, buff=0.1)

        lbl_zero = MathTex("y_{\\text{sum}} = 0", font_size=20, color=WARN).next_to(probe_dot_out, RIGHT, buff=0.15)

        self.play(
            ReplacementTransform(cap2, cap3),
            ReplacementTransform(w2_curve_in, w2_curve_out),
            ReplacementTransform(sum_curve_in, sum_curve_out),
            ReplacementTransform(probe_dot_in, probe_dot_out),
            FadeOut(brace_2A), FadeOut(lbl_2A),
            FadeIn(lbl_zero),
            ReplacementTransform(dial_hand2, dial_hand2_out),
            ReplacementTransform(dial_lbl, dial_lbl_out),
            run_time=2.0
        )
        self.wait(2.2)

        # Summary badge before exit
        summary_box = RoundedRectangle(width=8.2, height=0.7, corner_radius=0.1, color=OK, fill_color=BLACK, fill_opacity=0.85).move_to([0, -3.1, 0])
        summary_txt = Text("หลักการแทรกสอด: เสริมกันเมื่อเฟสตรงกัน · หักล้างเมื่อเฟสตรงข้าม", font_size=17, color=WHITE).move_to(summary_box.get_center())
        self.play(FadeIn(summary_box), FadeIn(summary_txt), run_time=0.8)
        self.wait(1.5)

        self.fade_out_all(run_time=0.8)
