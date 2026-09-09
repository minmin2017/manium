"""
double_slit_04_lab_real.py
Module 4: Young's Double-Slit Wave Interference
Scenes:
  - DS07_ParameterLab (~100s)
  - DS08_SlitEnvelope (~75s)
  - DS09_CausalSummary (~40s)
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
C_GHOST   = "#616161"  # Dashed gray ghost reference
C_LAMBDA  = "#FF5252"  # Wavelength lambda (Red/Vivid)
C_L_DIST  = "#448AFF"  # Distance L (Blue)
C_D_SLIT  = "#26A69A"  # Slit separation d (Teal)
C_A_WIDTH = "#FFA726"  # Slit width a (Orange/Amber)
C_ENV     = "#AB47BC"  # Diffraction Envelope (Purple)


class DS07_ParameterLab(SafeScene):
    """
    Beat 7: Interactive Parameter Lab (~100s)
    Locked Front-on screen view with parameter controls.
    Tests:
      1. lambda up (Red vs Blue) -> wider fringe spacing Delta y.
      2. L up (Screen moved back) -> wider fringe spacing Delta y.
      3. d up (Slits further apart) -> narrower fringe spacing Delta y.
    Always preserves dashed gray ghost markers of baseline before each change.
    """
    def construct(self):
        pref = page_ref("Beat 7 · ห้องทดลองพารามิเตอร์")
        ttl = title("Interactive Parameter Lab: Delta y approx lambda L / d", size=24)
        cap1 = caption_top("ทดสอบผลของตัวแปร: มีเส้นประสีเทา (Ghost) ล็อกตำแหน่งเดิมไว้เปรียบเทียบเสมอ")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # Baseline Screen Representation at Left (x = -3.2, y = -0.8 to stay well below caption_top)
        scr_box = Rectangle(width=2.4, height=4.2, color=C_SCREEN, fill_opacity=0.9, fill_color=C_SCREEN).move_to([-3.2, -0.8, 0])
        scr_lbl = Text("ฉากรับภาพ", font_size=15, color=WHITE).next_to(scr_box.get_top(), UP, buff=0.1)

        # Baseline Fringes (spacing dy0 = 0.65)
        dy0 = 0.65
        baseline_ys = [-2*dy0, -dy0, 0.0, dy0, 2*dy0]

        # Active fringes
        active_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.25, color=C_BRIGHT, fill_opacity=0.9, fill_color=C_BRIGHT).move_to([-3.2, y - 0.8, 0])
            for y in baseline_ys
        ])

        # Persistent Ghost Fringes (dashed gray markers)
        ghost_fringes = VGroup(*[
            DashedLine([-4.2, y - 0.8, 0], [-2.2, y - 0.8, 0], color=C_GHOST, stroke_width=2.5)
            for y in baseline_ys
        ])

        # Formula Card at Right (placed safely below caption_top)
        formula_box = RoundedRectangle(width=4.8, height=1.3, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.85).move_to([3.4, 1.2, 0])
        formula_txt = MathTex("\\Delta y \\approx \\frac{\\lambda L}{d}", font_size=26, color=WHITE).move_to(formula_box.get_center())

        self.play(
            FadeIn(scr_box), FadeIn(scr_lbl),
            FadeIn(ghost_fringes), FadeIn(active_fringes),
            FadeIn(formula_box), FadeIn(formula_txt),
            run_time=1.4
        )
        self.wait(1.0)

        # Experiment 1: Increase lambda (Wavelength) -> Wider spacing
        cap2 = caption_top("การทดลองที่ 1: เพิ่ม lambda (แสงสีแดง) -> ริ้วบานกว้างขึ้นกว่าเส้นประเดิม")
        dy_lam = 0.95
        lam_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.28, color=C_LAMBDA, fill_opacity=0.9, fill_color=C_LAMBDA).move_to([-3.2, y - 0.8, 0])
            for y in [-dy_lam, 0.0, dy_lam]
        ])

        highlight_lam = MathTex("\\Delta y \\uparrow \\;\\approx\\; \\frac{\\lambda \\uparrow \\cdot L}{d}", font_size=22, color=C_LAMBDA).move_to([3.4, 0.0, 0])

        self.play(
            ReplacementTransform(cap1, cap2),
            Transform(active_fringes, lam_fringes),
            FadeIn(highlight_lam),
            run_time=1.8
        )
        self.wait(1.8)

        # Reset to baseline
        active_reset = VGroup(*[
            Rectangle(width=2.0, height=0.25, color=C_BRIGHT, fill_opacity=0.9, fill_color=C_BRIGHT).move_to([-3.2, y - 0.8, 0])
            for y in baseline_ys
        ])
        self.play(
            Transform(active_fringes, active_reset),
            FadeOut(highlight_lam),
            run_time=1.0
        )

        # Experiment 2: Increase L (Screen Distance) -> Wider spacing
        cap3 = caption_top("การทดลองที่ 2: ถอยฉากรับภาพออกไปไกล (เพิ่ม L) -> ริ้วบานกว้างขึ้นเป็นสัดส่วนตรง")
        dy_L = 1.05
        L_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.28, color=C_L_DIST, fill_opacity=0.9, fill_color=C_L_DIST).move_to([-3.2, y - 0.8, 0])
            for y in [-dy_L, 0.0, dy_L]
        ])

        highlight_L = MathTex("\\Delta y \\uparrow \\;\\approx\\; \\frac{\\lambda \\cdot L \\uparrow}{d}", font_size=22, color=C_L_DIST).move_to([3.4, 0.0, 0])

        self.play(
            ReplacementTransform(cap2, cap3),
            Transform(active_fringes, L_fringes),
            FadeIn(highlight_L),
            run_time=1.8
        )
        self.wait(1.8)

        # Reset to baseline
        self.play(
            Transform(active_fringes, active_reset),
            FadeOut(highlight_L),
            run_time=1.0
        )

        # Experiment 3: Increase d (Slit Separation) -> Narrower spacing
        cap4 = caption_top("การทดลองที่ 3: เพิ่มระยะห่างสลิต d (ช่องห่างกันขึ้น) -> ริ้วบีบแคบชิดเข้าหากัน!")
        dy_d = 0.42
        d_fringes = VGroup(*[
            Rectangle(width=2.0, height=0.18, color=C_D_SLIT, fill_opacity=0.9, fill_color=C_D_SLIT).move_to([-3.2, y - 0.8, 0])
            for y in [-4*dy_d, -3*dy_d, -2*dy_d, -dy_d, 0.0, dy_d, 2*dy_d, 3*dy_d, 4*dy_d]
        ])

        highlight_d = MathTex("\\Delta y \\downarrow \\;\\approx\\; \\frac{\\lambda L}{d \\uparrow}", font_size=22, color=C_D_SLIT).move_to([3.4, 0.0, 0])

        self.play(
            ReplacementTransform(cap3, cap4),
            Transform(active_fringes, d_fringes),
            FadeIn(highlight_d),
            run_time=1.8
        )
        self.wait(2.2)

        self.fade_out_all(run_time=0.8)


class DS08_SlitEnvelope(SafeScene):
    """
    Beat 8: Finite Slit Width & Diffraction Envelope (~75s)
    Introduces slit width 'a' (color distinct from 'd').
    Shows real double-slit pattern = interference factor * single-slit envelope.
    Physically slides a shutter over one slit -> modulation disappears, leaving broad envelope.
    """
    def construct(self):
        pref = page_ref("Beat 8 · สลิตจริงและม่านเลี้ยวเบน")
        ttl = title("Finite Slit Width & Diffraction Envelope", size=24)
        cap1 = caption_top("สลิตจริงมีความกว้าง a: เกิดการเลี้ยวเบนเดี่ยวเป็น 'ม่านครอบ' (Envelope) บีบริ้วข้างๆ ให้จางลง")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # Legend distinguishing d and a
        legend_box = RoundedRectangle(width=5.8, height=1.0, corner_radius=0.1, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.85).move_to([0, 1.8, 0])
        txt_d = Text("d: ระยะห่างระหว่างสลิต (Interference)", font_size=13, color=C_D_SLIT).move_to([0, 2.05, 0])
        txt_a = Text("a: ความกว้างของแต่ละช่อง (Diffraction Envelope)", font_size=13, color=C_A_WIDTH).move_to([0, 1.55, 0])
        legend_grp = VGroup(legend_box, txt_d, txt_a)

        self.play(FadeIn(legend_grp), run_time=1.0)

        # Plot Coordinate Frame
        axes = Axes(
            x_range=[-3.0, 3.0, 1], y_range=[0, 4.5, 1],
            x_length=9.0, y_length=3.0,
            axis_config={"include_ticks": False, "stroke_color": GRAYTXT, "stroke_width": 1.5}
        ).move_to([0, -0.8, 0])

        lbl_axis_c = Text("y = 0", font_size=13, color=GRAYTXT).next_to(axes.c2p(0, 0), DOWN, buff=0.1)

        # 1. Ideal Two-Source Curve (Equal Heights)
        curve_ideal = axes.plot(
            lambda y: 4.0 * (np.cos(PI * y / 0.6) ** 2),
            x_range=[-2.8, 2.8], color=C_BRIGHT, stroke_width=1.5
        )
        lbl_ideal = Text("แบบจำลองอุดมคติ (ยอดเท่ากัน)", font_size=14, color=C_BRIGHT).move_to([-3.2, 1.0, 0])

        self.play(Create(axes), FadeIn(lbl_axis_c), Create(curve_ideal), FadeIn(lbl_ideal), run_time=1.5)
        self.wait(1.0)

        # 2. Introduce Sinc^2 Diffraction Envelope
        cap2 = caption_top("ม่านเลี้ยวเบน (Envelope): แถบสว่างกลางเด่นชัดที่สุด ขณะที่แถบข้างๆ ถูกกดลงตามสูตร sinc^2")

        # envelope curve: sinc^2(beta)
        def envelope_func(y):
            beta = PI * 0.45 * y
            if abs(beta) < 1e-4:
                return 4.0
            return 4.0 * ((np.sin(beta) / beta) ** 2)

        curve_env = axes.plot(envelope_func, x_range=[-2.8, 2.8], color=C_ENV, stroke_width=2.5)
        lbl_env = Text("Diffraction Envelope", font_size=14, color=C_ENV).move_to([3.4, 1.0, 0])

        # Combined Real Curve: I_real = ideal * (sinc(beta))^2
        def real_func(y):
            interf = np.cos(PI * y / 0.6) ** 2
            beta = PI * 0.45 * y
            diff = 1.0 if abs(beta) < 1e-4 else (np.sin(beta) / beta) ** 2
            return 4.0 * interf * diff

        curve_real = axes.plot(real_func, x_range=[-2.8, 2.8], color=OK, stroke_width=3.5)

        self.play(
            ReplacementTransform(cap1, cap2),
            Create(curve_env), FadeIn(lbl_env),
            ReplacementTransform(curve_ideal, curve_real),
            FadeOut(lbl_ideal),
            run_time=2.0
        )
        self.wait(1.8)

        # 3. Slide Shutter to Block One Slit
        cap3 = caption_top("เมื่อเลื่อนแผ่นทึบมาปิดสลิตหนึ่งช่อง: ริ้วแทรกสอดสลายตัวทันที เหลือเพียงแถบมัวของสลิตเดี่ยว!")

        # Single slit curve (no interference ripples)
        curve_single = axes.plot(
            lambda y: 1.0 * (1.0 if abs(PI * 0.45 * y) < 1e-4 else (np.sin(PI * 0.45 * y) / (PI * 0.45 * y)) ** 2),
            x_range=[-2.8, 2.8], color=WARN, stroke_width=3.5
        )

        shutter = Rectangle(width=0.8, height=1.4, color=WARN, fill_color=WARN, fill_opacity=0.85).move_to([-5.2, 0.8, 0])
        lbl_shutter = Text("ปิด S2", font_size=14, color=WHITE).move_to(shutter.get_center())

        self.play(
            ReplacementTransform(cap2, cap3),
            FadeIn(shutter), FadeIn(lbl_shutter),
            ReplacementTransform(curve_real, curve_single),
            FadeOut(curve_env), FadeOut(lbl_env),
            run_time=2.0
        )
        self.wait(2.2)

        self.fade_out_all(run_time=0.8)


class DS09_CausalSummary(SafeThreeDScene):
    """
    Beat 9: Causal Summary & 3 Prediction Reviews (~40s)
    3D Perspective returning to full apparatus.
    Light cascades sequentially through 4 causal stages:
      Source -> Coherent Slits -> Path Difference -> Fringes on Screen.
    Clarifies spatial redistribution of energy without loss, followed by 3 prediction cards.
    """
    def construct(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES)

        pref = self.hud(page_ref("Beat 9 · สรุปกระบวนการคิด"))
        ttl = self.hud(title("Causal Chain & Master Summary", size=25))
        cap1 = self.hud(caption_top("พลังงานไม่ได้ถูกทำลาย: การแทรกสอดคือการกระจายความเข้มใหม่ จากแถบมืดไปรวมที่แถบสว่าง"))

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # 4-Step Causal Diagram (HUD, safely positioned)
        c_box = RoundedRectangle(width=11.2, height=1.1, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.9).move_to([0, 1.7, 0])
        self.hud(c_box)

        step_txt = self.hud(Text(
            "1. แหล่งกำเนิดเดี่ยว  -->  2. สองช่องอาพันธ์  -->  3. ผลต่างเส้นทาง  -->  4. ริ้วสว่าง-มืดบนฉาก",
            font_size=16, color=WHITE
        ).move_to(c_box.get_center()))

        self.play(FadeIn(c_box), FadeIn(step_txt), run_time=1.2)

        # 3D Apparatus Representation in lower stage
        src_pt = np.array([-3.5, 0, -1.0])
        b_x = -0.5
        scr_x = 3.0

        src_dot = Dot3D(point=src_pt, radius=0.2, color=C_SOURCE)
        barrier = Rectangle(width=0.1, height=2.2, color=C_BARRIER, fill_opacity=0.8).move_to([b_x, 0, -1.0])
        screen_surf = Rectangle(width=0.12, height=2.4, color=C_SCREEN, fill_opacity=0.9).move_to([scr_x, 0, -1.0])

        app_grp = VGroup(src_dot, barrier, screen_surf)
        self.play(FadeIn(app_grp), run_time=1.0)

        # Sequential Lighting Pulse
        pulse1 = line3(src_pt, [b_x, 0.4, -1.0], color=C_SOURCE, thickness=0.03)
        pulse2 = line3(src_pt, [b_x, -0.4, -1.0], color=C_SOURCE, thickness=0.03)
        pulse3 = line3([b_x, 0.4, -1.0], [scr_x, 0.2, -1.0], color=C_BRIGHT, thickness=0.03)
        pulse4 = line3([b_x, -0.4, -1.0], [scr_x, 0.2, -1.0], color=C_BRIGHT, thickness=0.03)

        self.play(Create(pulse1), Create(pulse2), run_time=0.8)
        self.play(Create(pulse3), Create(pulse4), run_time=0.8)

        # 3 Quick Prediction Review Cards (HUD)
        cap2 = self.hud(caption_top("ทบทวน 3 คำถามทำนาย: lambda มากขึ้น -> กว้างขึ้น, L มากขึ้น -> กว้างขึ้น, d มากขึ้น -> แคบลง!"))
        card_pred = RoundedRectangle(width=9.5, height=1.1, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.9).move_to([0, -2.6, 0])
        self.hud(card_pred)

        txt_pred = self.hud(Text(
            "lambda ขึ้น: ริ้วบานออก   |   L ขึ้น: ริ้วบานออก   |   d ขึ้น: ริ้วบีบแคบลง",
            font_size=17, color=OK
        ).move_to(card_pred.get_center()))

        self.play(
            ReplacementTransform(cap1, cap2),
            FadeIn(card_pred), FadeIn(txt_pred),
            run_time=1.4
        )
        self.wait(2.5)

        self.fade_out_all(run_time=0.8)
