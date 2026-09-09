"""
double_slit_04_lab_real.py
Module 4: Young's Double-Slit Wave Interference
Scenes:
  - DS07_ParameterLab (Target: 90-120s, Planned: ~98s)
  - DS08_SlitEnvelope (Target: 70-95s, Planned: ~82s)
  - DS09_CausalSummary (Target: 35-55s, Planned: ~44s)
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
C_BRIGHT  = "#00E676"  # Bright maxima
C_DARK    = "#1A237E"  # Dark minima
C_GHOST   = "#757575"  # Dashed gray ghost reference
C_LAMBDA  = "#FF5252"  # Wavelength lambda (Red/Vivid)
C_L_DIST  = "#448AFF"  # Distance L (Blue)
C_D_SLIT  = "#26A69A"  # Slit separation d (Teal)
C_A_WIDTH = "#FFA726"  # Slit width a (Orange/Amber)
C_ENV     = "#AB47BC"  # Diffraction Envelope (Purple)


class DS07_ParameterLab(SafeScene):
    """
    Beat 7: Interactive Parameter Lab (~98s)
    Locked Front-on screen view with parameter controls.
    Tests:
      1. lambda up (Red vs Green) -> wider fringe spacing Delta y.
      2. L up (Screen moved back) -> wider fringe spacing Delta y.
      3. d up (Slits further apart) -> narrower fringe spacing Delta y.
    Always preserves dashed gray ghost markers of baseline before each change.
    """
    def construct(self):
        # 1. Setup & Baseline Ghost Markers (Micro-beat 1: ~18s)
        pref = page_ref("Beat 7 · ห้องทดลองพารามิเตอร์")
        ttl = title("Interactive Parameter Lab: Delta y approx lambda L / d", size=24)
        cap1 = caption_top("ห้องทดลองพารามิเตอร์: ทดสอบผลของตัวแปร lambda, L, d ต่อระยะห่างริ้ว Delta y")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.0)
        self.wait(2.8)

        # Baseline Screen Representation at Left (x = -3.2, y = -0.8)
        scr_box = Rectangle(width=2.4, height=4.2, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([-3.2, -0.8, 0])
        scr_lbl = Text("ฉากรับภาพ", font_size=15, color=WHITE).next_to(scr_box.get_top(), UP, buff=0.12)

        # Baseline Fringes (spacing dy0 = 0.65)
        dy0 = 0.65
        baseline_ys = [-2*dy0, -dy0, 0.0, dy0, 2*dy0]

        # Active fringes (Green baseline)
        active_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.24, color=C_BRIGHT, fill_opacity=0.9, fill_color=C_BRIGHT).move_to([-3.2, y - 0.8, 0])
            for y in baseline_ys
        ])

        # Baseline Fringe Labels
        lbl_m0 = MathTex("m = 0", font_size=16, color=WHITE).move_to([-1.6, -0.8, 0])
        lbl_m1 = MathTex("m = 1", font_size=16, color=WHITE).move_to([-1.6, dy0 - 0.8, 0])
        brace_dy0 = Brace(Line([-2.0, -0.8, 0], [-2.0, dy0 - 0.8, 0]), RIGHT, buff=0.1)
        txt_dy0 = MathTex("\\Delta y_0", font_size=18, color=C_BRIGHT).next_to(brace_dy0, RIGHT, buff=0.1)
        base_labels = VGroup(lbl_m0, lbl_m1, brace_dy0, txt_dy0)

        # Persistent Ghost Fringes (dashed gray markers)
        ghost_fringes = VGroup(*[
            DashedLine([-4.3, y - 0.8, 0], [-2.1, y - 0.8, 0], color=C_GHOST, stroke_width=2.5)
            for y in baseline_ys
        ])

        # Formula Card at Right (y = 1.3 to stay well below caption_top)
        formula_box = RoundedRectangle(width=5.0, height=1.3, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.88).move_to([3.3, 1.3, 0])
        formula_txt = MathTex("\\Delta y \\approx \\frac{\\lambda L}{d}", font_size=28, color=WHITE).move_to(formula_box.get_center())

        self.play(
            FadeIn(scr_box), FadeIn(scr_lbl),
            FadeIn(ghost_fringes), FadeIn(active_fringes),
            FadeIn(base_labels),
            FadeIn(formula_box), FadeIn(formula_txt),
            run_time=1.8
        )

        cap_ghost = caption_top("เส้นประสีเทา (Ghost) ถูกตรึงไว้เป็นตำแหน่งอ้างอิงเดิม เพื่อสังเกตการเปลี่ยนแปลงชัดเจน")
        self.play(ReplacementTransform(cap1, cap_ghost), run_time=1.0)
        self.wait(3.5)

        card_vars = RoundedRectangle(width=5.0, height=1.6, corner_radius=0.1, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.85).move_to([3.3, -0.4, 0])
        txt_v1 = Text("lambda = ความยาวคลื่นแสง", font_size=13, color=C_LAMBDA).move_to([3.3, 0.15, 0])
        txt_v2 = Text("L = ระยะห่างจากสลิตถึงฉาก", font_size=13, color=C_L_DIST).move_to([3.3, -0.35, 0])
        txt_v3 = Text("d = ระยะห่างระหว่างช่องสลิต", font_size=13, color=C_D_SLIT).move_to([3.3, -0.85, 0])
        var_grp = VGroup(card_vars, txt_v1, txt_v2, txt_v3)

        self.play(FadeIn(var_grp), run_time=1.2)
        self.wait(4.0)

        # 2. Experiment 1: lambda up (Red light) (Micro-beat 2: ~24s)
        cap2 = caption_top("การทดลองที่ 1: เพิ่มความยาวคลื่น lambda (เปลี่ยนเป็นแสงสีแดง) -> ริ้วบานกว้างขึ้น!")
        self.play(ReplacementTransform(cap_ghost, cap2), run_time=1.0)
        self.wait(3.0)

        highlight_lam = MathTex("\\Delta y \\uparrow \\;\\approx\\; \\frac{\\lambda \\uparrow \\cdot L}{d}", font_size=24, color=C_LAMBDA).move_to([3.3, 1.3, 0])
        self.play(
            ReplacementTransform(formula_txt, highlight_lam),
            run_time=1.2
        )
        self.wait(2.2)

        # Active fringes expand to red (spacing dy_lam = 0.98)
        dy_lam = 0.98
        lam_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.26, color=C_LAMBDA, fill_opacity=0.9, fill_color=C_LAMBDA).move_to([-3.2, y - 0.8, 0])
            for y in [-dy_lam, 0.0, dy_lam]
        ])

        brace_dy_lam = Brace(Line([-2.0, -0.8, 0], [-2.0, dy_lam - 0.8, 0]), RIGHT, buff=0.1)
        txt_dy_lam = MathTex("\\Delta y_{\\text{red}} > \\Delta y_0", font_size=17, color=C_LAMBDA).next_to(brace_dy_lam, RIGHT, buff=0.1)
        new_labels_lam = VGroup(brace_dy_lam, txt_dy_lam)

        self.play(
            Transform(active_fringes, lam_fringes),
            ReplacementTransform(base_labels, new_labels_lam),
            run_time=2.0
        )
        self.wait(4.5)

        note_lam = Text("คลื่นยาวกว่า ต้องใช้มุมกว้างขึ้นเพื่อให้เกิดผลต่างเส้นทาง lambda", font_size=13, color=C_LAMBDA).move_to([3.3, -1.5, 0])
        self.play(FadeIn(note_lam), run_time=1.0)
        self.wait(4.5)

        # Reset to baseline
        active_reset = VGroup(*[
            Rectangle(width=2.0, height=0.24, color=C_BRIGHT, fill_opacity=0.9, fill_color=C_BRIGHT).move_to([-3.2, y - 0.8, 0])
            for y in baseline_ys
        ])
        formula_txt_reset = MathTex("\\Delta y \\approx \\frac{\\lambda L}{d}", font_size=28, color=WHITE).move_to(formula_box.get_center())

        self.play(
            Transform(active_fringes, active_reset),
            ReplacementTransform(highlight_lam, formula_txt_reset),
            FadeOut(new_labels_lam),
            FadeOut(note_lam),
            run_time=1.5
        )
        self.wait(1.5)

        # 3. Experiment 2: L up (Screen Distance) (Micro-beat 3: ~24s)
        cap3 = caption_top("การทดลองที่ 2: ถอยฉากรับภาพออกไปไกลขึ้น (เพิ่ม L) -> ริ้วบานกว้างขึ้นเป็นสัดส่วนตรง")
        self.play(ReplacementTransform(cap2, cap3), run_time=1.0)
        self.wait(3.0)

        highlight_L = MathTex("\\Delta y \\uparrow \\;\\approx\\; \\frac{\\lambda \\cdot L \\uparrow}{d}", font_size=24, color=C_L_DIST).move_to([3.3, 1.3, 0])
        self.play(
            ReplacementTransform(formula_txt_reset, highlight_L),
            run_time=1.2
        )
        self.wait(2.2)

        # Active fringes expand to blue (spacing dy_L = 1.08)
        dy_L = 1.08
        L_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.26, color=C_L_DIST, fill_opacity=0.9, fill_color=C_L_DIST).move_to([-3.2, y - 0.8, 0])
            for y in [-dy_L, 0.0, dy_L]
        ])

        brace_dy_L = Brace(Line([-2.0, -0.8, 0], [-2.0, dy_L - 0.8, 0]), RIGHT, buff=0.1)
        txt_dy_L = MathTex("\\Delta y_{L} > \\Delta y_0", font_size=17, color=C_L_DIST).next_to(brace_dy_L, RIGHT, buff=0.1)
        new_labels_L = VGroup(brace_dy_L, txt_dy_L)

        self.play(
            Transform(active_fringes, L_fringes),
            FadeIn(new_labels_L),
            run_time=2.0
        )
        self.wait(4.5)

        note_L = Text("มุมคงที่ แต่เมื่อถอยฉากไกลขึ้น ลำแสงเดินทางบานออกตกบนฉากห่างกันขึ้น", font_size=13, color=C_L_DIST).move_to([3.3, -1.5, 0])
        self.play(FadeIn(note_L), run_time=1.0)
        self.wait(4.5)

        # Reset to baseline
        formula_txt_reset2 = MathTex("\\Delta y \\approx \\frac{\\lambda L}{d}", font_size=28, color=WHITE).move_to(formula_box.get_center())
        self.play(
            Transform(active_fringes, active_reset),
            ReplacementTransform(highlight_L, formula_txt_reset2),
            FadeOut(new_labels_L),
            FadeOut(note_L),
            run_time=1.5
        )
        self.wait(1.5)

        # 4. Experiment 3: d up (Slit Gap) (Micro-beat 4: ~32s)
        cap4 = caption_top("การทดลองที่ 3: เพิ่มระยะห่างสลิต d (เจาะช่องห่างกันขึ้น) -> ริ้วบีบแคบลง!")
        self.play(ReplacementTransform(cap3, cap4), run_time=1.0)
        self.wait(3.0)

        highlight_d = MathTex("\\Delta y \\downarrow \\;\\approx\\; \\frac{\\lambda L}{d \\uparrow}", font_size=24, color=C_D_SLIT).move_to([3.3, 1.3, 0])
        self.play(
            ReplacementTransform(formula_txt_reset2, highlight_d),
            run_time=1.2
        )
        self.wait(2.2)

        # Active fringes compress to teal (spacing dy_d = 0.38)
        dy_d = 0.38
        d_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.16, color=C_D_SLIT, fill_opacity=0.9, fill_color=C_D_SLIT).move_to([-3.2, y - 0.8, 0])
            for y in [-4*dy_d, -3*dy_d, -2*dy_d, -dy_d, 0.0, dy_d, 2*dy_d, 3*dy_d, 4*dy_d]
        ])

        brace_dy_d = Brace(Line([-2.0, -0.8, 0], [-2.0, dy_d - 0.8, 0]), RIGHT, buff=0.1)
        txt_dy_d = MathTex("\\Delta y_{d} < \\Delta y_0", font_size=17, color=C_D_SLIT).next_to(brace_dy_d, RIGHT, buff=0.1)
        new_labels_d = VGroup(brace_dy_d, txt_dy_d)

        self.play(
            Transform(active_fringes, d_fringes),
            FadeIn(new_labels_d),
            run_time=2.2
        )
        self.wait(4.0)

        note_d = Text("ระวัง: d อยู่ที่ตัวหาร! ช่องห่างกัน มุมต่างทางเดินครบ lambda เร็วขึ้น ริ้วจึงแคบลง", font_size=12.5, color=C_D_SLIT).move_to([3.3, -1.5, 0])
        self.play(FadeIn(note_d), run_time=1.0)
        self.wait(4.5)

        # Comprehensive Summary Table
        summary_card = RoundedRectangle(width=10.5, height=1.3, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.92).move_to([0, -2.6, 0])
        txt_sum = Text(
            "สรุปผล 3 ปัจจัย:   lambda เพิ่ม -> ริ้วบาน   |   L เพิ่ม -> ริ้วบาน   |   d เพิ่ม -> ริ้วแคบลง",
            font_size=15, color=OK
        ).move_to(summary_card.get_center())

        self.play(FadeIn(summary_card), FadeIn(txt_sum), run_time=1.5)
        self.wait(6.5)

        self.fade_out_all(run_time=1.0)


class DS08_SlitEnvelope(SafeScene):
    """
    Beat 8: Finite Slit Width & Diffraction Envelope (~82s)
    Introduces slit width 'a' (color distinct from 'd').
    Shows real double-slit pattern = interference factor * single-slit envelope.
    Physically slides a shutter over one slit -> modulation disappears, leaving broad envelope.
    """
    def construct(self):
        # 1. Dimension a vs d distinction & Ideal Profile (Micro-beat 1: ~22s)
        pref = page_ref("Beat 8 · สลิตจริงและม่านเลี้ยวเบน")
        ttl = title("Finite Slit Width & Diffraction Envelope", size=24)
        cap1 = caption_top("สลิตจริงในโลกกายภาพ: ช่องไม่ได้เป็นจุดอุดมคติ แต่มีความกว้างจริง a")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.0)
        self.wait(3.0)

        # Legend distinguishing d and a
        legend_box = RoundedRectangle(width=6.8, height=1.1, corner_radius=0.1, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.88).move_to([0, 1.6, 0])
        txt_d = Text("d : ระยะห่างระหว่างสลิต (สร้างการแทรกสอด ริ้วถี่)", font_size=13, color=C_D_SLIT).move_to([0, 1.85, 0])
        txt_a = Text("a : ความกว้างของแต่ละช่อง (สร้างการเลี้ยวเบน ม่านครอบ)", font_size=13, color=C_A_WIDTH).move_to([0, 1.35, 0])
        legend_grp = VGroup(legend_box, txt_d, txt_a)

        self.play(FadeIn(legend_grp), run_time=1.2)
        self.wait(3.5)

        # Plot Coordinate Frame (Lower section)
        axes = Axes(
            x_range=[-3.0, 3.0, 1], y_range=[0, 4.5, 1],
            x_length=9.2, y_length=2.8,
            axis_config={"include_ticks": False, "stroke_color": GRAYTXT, "stroke_width": 1.5}
        ).move_to([0, -0.9, 0])

        lbl_axis_c = Text("y = 0", font_size=13, color=GRAYTXT).next_to(axes.c2p(0, 0), DOWN, buff=0.1)

        # Ideal Two-Source Curve (Equal Heights)
        curve_ideal = axes.plot(
            lambda y: 4.0 * (np.cos(PI * y / 0.6) ** 2),
            x_range=[-2.8, 2.8], color=C_BRIGHT, stroke_width=1.6
        )
        lbl_ideal = Text("แบบจำลองจุดอุดมคติ: ทุกริ้วสว่างเท่ากันตลอดแนว", font_size=13, color=C_BRIGHT).move_to([-2.6, 0.8, 0])

        self.play(Create(axes), FadeIn(lbl_axis_c), Create(curve_ideal), FadeIn(lbl_ideal), run_time=1.8)
        self.wait(4.5)

        cap_q = caption_top("แต่ในการทดลองจริง ริ้วที่อยู่ห่างจากจุดศูนย์กลางจะค่อยๆ จางมืดลง ทำไมจึงเป็นเช่นนั้น?")
        self.play(ReplacementTransform(cap1, cap_q), run_time=1.0)
        self.wait(5.0)

        # 2. Introduce Sinc^2 Diffraction Envelope (Micro-beat 2: ~28s)
        cap2 = caption_top("การเลี้ยวเบนจากช่องเดี่ยวความกว้าง a ก่อตัวเป็น 'ม่านครอบ' (Diffraction Envelope)")
        self.play(ReplacementTransform(cap_q, cap2), run_time=1.0)
        self.wait(3.0)

        # envelope curve: sinc^2(beta)
        def envelope_func(y):
            beta = PI * 0.45 * y
            if abs(beta) < 1e-4:
                return 4.0
            return 4.0 * ((np.sin(beta) / beta) ** 2)

        curve_env = axes.plot(envelope_func, x_range=[-2.8, 2.8], color=C_ENV, stroke_width=2.8)
        lbl_env = MathTex("I_{\\text{envelope}} \\propto \\left(\\frac{\\sin\\beta}{\\beta}\\right)^2", font_size=18, color=C_ENV).move_to([3.0, 0.8, 0])

        # Combined Real Curve: I_real = ideal * (sinc(beta))^2
        def real_func(y):
            interf = np.cos(PI * y / 0.6) ** 2
            beta = PI * 0.45 * y
            diff = 1.0 if abs(beta) < 1e-4 else (np.sin(beta) / beta) ** 2
            return 4.0 * interf * diff

        curve_real = axes.plot(real_func, x_range=[-2.8, 2.8], color=OK, stroke_width=3.2)

        self.play(
            Create(curve_env), FadeIn(lbl_env),
            ReplacementTransform(curve_ideal, curve_real),
            FadeOut(lbl_ideal),
            run_time=2.2
        )
        self.wait(4.5)

        cap_real = caption_top("ริ้วแทรกสอดจริงจึงถูกกดให้อยู่ใต้กรอบม่านเลี้ยวเบน: แถบกลางสว่างสุด ริ้วข้างๆ ค่อยๆ จางลง")
        self.play(ReplacementTransform(cap2, cap_real), run_time=1.0)
        self.wait(5.5)

        lbl_real_pat = Text("ลวดลายจริง = แทรกสอด x เลี้ยวเบน", font_size=13, color=OK).move_to([-2.6, 0.8, 0])
        self.play(FadeIn(lbl_real_pat), run_time=1.0)
        self.wait(5.0)

        # 3. Slide Shutter to Block One Slit (Micro-beat 3: ~32s)
        cap3 = caption_top("การทดลองตัดสิน: หากเลื่อนแผ่นทึบมาปิดสลิตหนึ่งช่อง (ปิด S2) อะไรจะเกิดขึ้น?")
        self.play(ReplacementTransform(cap_real, cap3), run_time=1.0)
        self.wait(3.5)

        # Single slit curve (no interference ripples)
        curve_single = axes.plot(
            lambda y: 1.0 * (1.0 if abs(PI * 0.45 * y) < 1e-4 else (np.sin(PI * 0.45 * y) / (PI * 0.45 * y)) ** 2),
            x_range=[-2.8, 2.8], color=WARN, stroke_width=3.2
        )

        shutter = Rectangle(width=1.6, height=0.9, color=WARN, fill_color=WARN, fill_opacity=0.88).move_to([-4.8, 0.8, 0])
        lbl_shutter = Text("ปิด S2 (Shutter)", font_size=13, color=WHITE).move_to(shutter.get_center())

        self.play(
            FadeIn(shutter), FadeIn(lbl_shutter),
            ReplacementTransform(curve_real, curve_single),
            FadeOut(curve_env), FadeOut(lbl_env),
            FadeOut(lbl_real_pat),
            run_time=2.4
        )
        self.wait(4.5)

        cap_collapse = caption_top("ริ้วลายทางแทรกสอดสลายตัวทันที! เหลือเพียงแถบมัวกว้างของการเลี้ยวเบนสลิตเดี่ยว")
        self.play(ReplacementTransform(cap3, cap_collapse), run_time=1.0)
        self.wait(4.5)

        # Contrast Card
        contrast_card = RoundedRectangle(width=9.6, height=1.3, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.92).move_to([0, -2.6, 0])
        txt_c1 = Text("เปิดสองช่อง (S1 + S2) : คลื่นสองขบวนซ้อนทับ เกิดริ้วลายทางถี่ (Interference)", font_size=13, color=OK).move_to([0, -2.35, 0])
        txt_c2 = Text("เปิดช่องเดียว (S1 เท่านั้น) : ไร้คู่แทรกสอด เหลือเพียงแถบกระจายมัวเดี่ยว (Single-slit)", font_size=13, color=WARN).move_to([0, -2.85, 0])
        contrast_grp = VGroup(contrast_card, txt_c1, txt_c2)

        self.play(FadeIn(contrast_grp), run_time=1.5)
        self.wait(7.0)

        self.fade_out_all(run_time=1.0)


class DS09_CausalSummary(SafeThreeDScene):
    """
    Beat 9: Causal Summary & 3 Prediction Reviews (~44s)
    3D Perspective returning to full apparatus.
    Light cascades sequentially through 4 causal stages:
      Source -> Coherent Slits -> Path Difference -> Fringes on Screen.
    Clarifies spatial redistribution of energy without loss, followed by 3 prediction cards.
    """
    def construct(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES)

        # 1. Causal Chain & Energy Redistribution (Micro-beat 1: ~16s)
        pref = self.hud(page_ref("Beat 9 · สรุปกระบวนการคิด"))
        ttl = self.hud(title("Causal Chain & Master Summary", size=25))
        cap1 = self.hud(caption_top("พลังงานไม่ได้ถูกทำลาย: การแทรกสอดคือการจัดสรรความเข้มแสงใหม่ (Spatial Redistribution)"))

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=1.0)
        self.wait(3.5)

        # 4-Step Causal Diagram (HUD, safely positioned below title)
        c_box = RoundedRectangle(width=11.6, height=1.1, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.9).move_to([0, 1.65, 0])
        self.hud(c_box)

        step_txt = self.hud(Text(
            "1. แหล่งกำเนิดเดี่ยว  -->  2. สองช่องอาพันธ์  -->  3. ผลต่างเส้นทาง delta r  -->  4. ริ้วสว่าง-มืดบนฉาก",
            font_size=15, color=WHITE
        ).move_to(c_box.get_center()))

        self.play(FadeIn(c_box), FadeIn(step_txt), run_time=1.4)
        self.wait(4.5)

        cap_energy = self.hud(caption_top("แถบมืดไม่ได้กลืนแสงหายไป แต่แสงถูกนำไปรวมพลังกันที่แถบสว่าง สว่างขึ้นถึง 4 เท่า!"))
        self.play(ReplacementTransform(cap1, cap_energy), run_time=1.0)
        self.wait(4.5)

        # 2. Sequential Lighting Cascade in 3D (Micro-beat 2: ~14s)
        src_pt = np.array([-3.8, 0, -1.0])
        b_x = -0.5
        scr_x = 3.2

        src_dot = Dot3D(point=src_pt, radius=0.22, color=C_SOURCE)
        barrier = Rectangle(width=0.1, height=2.2, color=C_BARRIER, fill_opacity=0.85).move_to([b_x, 0, -1.0])
        screen_surf = Rectangle(width=0.12, height=2.4, color=C_SCREEN, fill_opacity=0.9).move_to([scr_x, 0, -1.0])

        s1_pt = np.array([b_x, 0.45, -1.0])
        s2_pt = np.array([b_x, -0.45, -1.0])
        p0_pt = np.array([scr_x, 0.0, -1.0])

        app_grp = VGroup(src_dot, barrier, screen_surf)
        self.play(FadeIn(app_grp), run_time=1.2)

        # Light Cascade: Stage 1 -> Stage 2 (Source to Slits)
        pulse1 = line3(src_pt, s1_pt, color=C_SOURCE, thickness=0.035)
        pulse2 = line3(src_pt, s2_pt, color=C_SOURCE, thickness=0.035)
        self.play(Create(pulse1), Create(pulse2), run_time=1.5)

        # Stage 2 -> Stage 3 & 4 (Slits to Center Bright Fringe P0)
        ray1 = line3(s1_pt, p0_pt, color=C_BRIGHT, thickness=0.035)
        ray2 = line3(s2_pt, p0_pt, color=C_BRIGHT, thickness=0.035)
        dot_p0 = Dot3D(point=p0_pt, radius=0.18, color=C_BRIGHT)
        lbl_p0 = self.world_text(Text("จุดสว่างกลาง (เสริมกัน)", font_size=13, color=C_BRIGHT).next_to(p0_pt, RIGHT, buff=0.15))

        self.play(Create(ray1), Create(ray2), run_time=1.8)
        self.play(FadeIn(dot_p0), FadeIn(lbl_p0), run_time=1.2)
        self.wait(3.5)

        # 3. Master Prediction Review Cards (Micro-beat 3: ~16s)
        cap_pred = self.hud(caption_top("สรุป 3 กฎทองทำนายผล: จดจำความสัมพันธ์เพื่อการใช้งานที่แม่นยำ"))
        self.play(ReplacementTransform(cap_energy, cap_pred), run_time=1.0)
        self.wait(2.5)

        card_pred = RoundedRectangle(width=11.2, height=1.3, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.92).move_to([0, -2.5, 0])
        self.hud(card_pred)

        txt_p1 = self.hud(Text("lambda ขึ้น: ริ้วบานออก (แปรผันตรง)", font_size=13.5, color=C_LAMBDA).move_to([-3.6, -2.5, 0]))
        txt_p2 = self.hud(Text("L ขึ้น: ริ้วบานออก (แปรผันตรง)", font_size=13.5, color=C_L_DIST).move_to([0.0, -2.5, 0]))
        txt_p3 = self.hud(Text("d ขึ้น: ริ้วบีบแคบลง (แปรผันผกผัน)", font_size=13.5, color=C_D_SLIT).move_to([3.6, -2.5, 0]))

        self.play(
            FadeIn(card_pred),
            FadeIn(txt_p1), FadeIn(txt_p2), FadeIn(txt_p3),
            run_time=1.5
        )
        self.wait(5.5)

        cap_final = self.hud(caption_top("เข้าใจคลื่น เข้าใจแสง: จากเรขาคณิตผลต่างเส้นทาง สู่ความเข้าใจธรรมชาติของเอกภพ"))
        self.play(ReplacementTransform(cap_pred, cap_final), run_time=1.0)
        self.wait(4.0)

        self.fade_out_all(run_time=1.0)
