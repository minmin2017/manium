# -*- coding: utf-8 -*-
from manim import *
from mlib import SafeScene, caption_top, title, page_ref
from gear_law_similar import pt, tag, ra_mark
from spur_gears import g20_geom, arc_near, side_label, ADD_C, BASE_C, LOA_C
from g21c_captions import CAP, TITLE, PAGE


class G21C_TermGlow(SafeScene):
    def swap_cap(self, old, txt, size=19):
        self.play(FadeOut(old), run_time=0.35)
        new = caption_top(txt, size=size)
        self.play(FadeIn(new), run_time=0.5)
        return new

    def construct(self):
        g = g20_geom(k=1.0, P_screen=(-3.6, 0.55, 0.0))
        P, O1, O2, E1, E2, A, B = (g[k_] for k_ in ("P", "O1", "O2", "E1", "E2", "A", "B"))
        w = g["w"]

        # ---------------------------------------------------------
        # Row 1 (0-4s): Header, title, page_ref, LOA and 5 dots
        # ---------------------------------------------------------
        self.add(title(TITLE, size=26))
        self.add(page_ref(PAGE))

        cap = caption_top(CAP["intro"], size=19)
        formula = MathTex(r"Z=E_1B+E_2A-E_1E_2", font_size=34, color=WHITE).move_to([3.3, 2.0, 0])
        self.play(FadeIn(cap), FadeIn(formula), run_time=0.8)

        loa = Line(E1 - w * 0.3, E2 + w * 0.3, color=LOA_C, stroke_width=3)
        dots = {nm: pt(p_, c_, 0.055) for nm, p_, c_ in (("E1", E1, BASE_C), ("A", A, WARN), ("P", P, WHITE),
                                                        ("B", B, WARN), ("E2", E2, BASE_C))}
        self.play(Create(loa), FadeIn(VGroup(*dots.values())), run_time=1.0)
        self.wait(1.0)

        # ---------------------------------------------------------
        # Row 2 (4-9s): Gear 1 triangle O1-E1-B, segments, arcs, labels
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g1_tri"])
        d_O1 = pt(O1, WHITE, 0.07)
        lb_O1 = tag("O1", O1, UP, WHITE, 20, 0.12)
        s_b1 = Line(O1, E1, color=BASE_C, stroke_width=4)
        s_o1 = Line(O1, B, color=ADD_C, stroke_width=4)
        s_e1b = Line(E1, B, color=WARN, stroke_width=6)
        tri1 = Polygon(O1, E1, B, color=WHITE, stroke_width=0, fill_color=WHITE, fill_opacity=0.10)
        lb_E1 = tag("E1", E1, DL, BASE_C, 20, 0.1)
        lb_B = tag("B", B, DOWN, WARN, 20, 0.14)

        self.play(FadeIn(d_O1), FadeIn(lb_O1), FadeIn(lb_E1), FadeIn(lb_B), FadeIn(tri1), run_time=0.8)
        self.play(Create(s_b1), Create(s_o1), Create(s_e1b), run_time=1.2)

        cen1 = (O1 + E1 + B) / 3
        tb1 = side_label("Rb1", O1, E1, cen1, BASE_C)
        to1 = side_label("Ro1", O1, B, cen1, ADD_C)
        te1 = side_label("E1B", E1, B, cen1, WARN)
        arc_b1, _, _ = arc_near(O1, g["Rb1"], E1, 0.5, BASE_C, 2.5, dashes=16)
        arc_o1, _, _ = arc_near(O1, g["Ro1"], B, 0.45, ADD_C, 2.5, dashes=16)

        self.play(FadeIn(tb1), FadeIn(to1), FadeIn(te1), Create(arc_b1), Create(arc_o1), run_time=1.0)
        self.wait(0.6)

        # ---------------------------------------------------------
        # Row 3 (9-12s): Right-angle mark at E1
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g1_right"])
        ra1 = ra_mark(E1, O1 - E1, B - E1, BASE_C, 0.16)
        self.play(Create(ra1), run_time=0.8)
        self.wait(1.0)

        # ---------------------------------------------------------
        # Row 4 (12-14s): Full formula E1B = sqrt(Ro1^2 - Rb1^2)
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g1_formula"])
        eq1 = MathTex(r"\overline{E_1B}", r"=", r"\sqrt{", r"R_{o1}^{2}", r"-", r"R_{b1}^{2}", r"}", font_size=38).move_to([3.3, 0.9, 0])
        eq1[0].set_color(WARN)
        eq1[3].set_color(ADD_C)
        eq1[5].set_color(BASE_C)
        self.play(FadeIn(eq1, shift=UP * 0.15), run_time=0.8)
        self.wait(0.8)

        # ---------------------------------------------------------
        # Row 5 (14-17s): Glow Ro1 (term eq1[3] + line s_o1)
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g1_ro"])
        self.play(
            Indicate(eq1[3], color=ADD_C, scale_factor=1.15),
            Indicate(s_o1, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        # ---------------------------------------------------------
        # Row 6 (17-20s): Glow Rb1 (term eq1[5] + line s_b1)
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g1_rb"])
        self.play(
            Indicate(eq1[5], color=BASE_C, scale_factor=1.15),
            Indicate(s_b1, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        # ---------------------------------------------------------
        # Row 7 (20-23s): Glow result E1B (term eq1[0] + line s_e1b)
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g1_res"])
        self.play(
            Indicate(eq1[0], color=WARN, scale_factor=1.15),
            Indicate(s_e1b, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        # ---------------------------------------------------------
        # Row 8 (23-32s): Numbers row E1B = sqrt(1.625^2 - 1.4095^2) = 0.809 in
        # ---------------------------------------------------------
        num1 = MathTex(
            r"\overline{E_1B}", r"=", r"\sqrt{", r"1.625^{2}", r"-", r"1.4095^{2}", r"}", r"=", r"\mathbf{0.809}\ \mathrm{in}",
            font_size=32
        ).move_to([3.3, 0.0, 0])
        num1[0].set_color(WARN)
        num1[3].set_color(ADD_C)
        num1[5].set_color(BASE_C)
        num1[8].set_color(WARN)
        self.play(FadeIn(num1, shift=UP * 0.1), run_time=0.8)
        self.wait(0.6)

        cap = self.swap_cap(cap, CAP["g1_n_ro"])
        self.play(
            Indicate(num1[3], color=ADD_C, scale_factor=1.15),
            Indicate(s_o1, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(0.8)

        cap = self.swap_cap(cap, CAP["g1_n_rb"])
        self.play(
            Indicate(num1[5], color=BASE_C, scale_factor=1.15),
            Indicate(s_b1, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(0.8)

        cap = self.swap_cap(cap, CAP["g1_n_res"])
        self.play(
            Indicate(num1[8], color=WARN, scale_factor=1.15),
            Indicate(s_e1b, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        # ---------------------------------------------------------
        # Row 9 (32-34s): Fade gear 1, keep boxed result E1B
        # ---------------------------------------------------------
        r1_box = SurroundingRectangle(eq1, color=WARN, buff=0.14, stroke_width=3)
        res1_group = VGroup(eq1, r1_box)
        self.play(Create(r1_box), run_time=0.6)
        self.play(
            FadeOut(VGroup(tri1, s_b1, s_o1, s_e1b, tb1, to1, te1, ra1, d_O1, lb_O1, lb_E1, lb_B, arc_b1, arc_o1, num1)),
            res1_group.animate.scale(0.70).move_to([3.3, 1.05, 0]),
            formula.animate.move_to([3.3, 2.15, 0]),
            run_time=1.0
        )
        self.wait(0.5)

        # ---------------------------------------------------------
        # Row 10 (34-50s): Gear 2 O2, E2, A, Ro2, Rb2, E2A and glowing
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["g2_tri"])
        d_O2 = pt(O2, WHITE, 0.07)
        lb_O2 = tag("O2", O2, LEFT, WHITE, 20, 0.12)
        s_b2 = Line(O2, E2, color=BASE_C, stroke_width=4)
        s_o2 = Line(O2, A, color=ADD_C, stroke_width=4)
        s_e2a = Line(E2, A, color=WARN, stroke_width=6)
        tri2 = Polygon(O2, E2, A, color=WHITE, stroke_width=0, fill_color=WHITE, fill_opacity=0.10)
        lb_E2 = tag("E2", E2, RIGHT, BASE_C, 20, 0.12)
        lb_A = tag("A", A, UP, WARN, 20, 0.14)

        self.play(FadeIn(d_O2), FadeIn(lb_O2), FadeIn(lb_E2), FadeIn(lb_A), FadeIn(tri2), run_time=0.8)
        self.play(Create(s_b2), Create(s_o2), Create(s_e2a), run_time=1.2)

        cen2 = (O2 + E2 + A) / 3
        tb2 = side_label("Rb2", O2, E2, cen2, BASE_C)
        to2 = side_label("Ro2", O2, A, cen2, ADD_C)
        te2 = side_label("E2A", E2, A, cen2, WARN, off=0.45)
        ra2 = ra_mark(E2, O2 - E2, A - E2, BASE_C, 0.16)
        arc_b2, _, _ = arc_near(O2, g["Rb2"], E2, 0.16, BASE_C, 2.5, dashes=14)
        arc_o2, _, _ = arc_near(O2, g["Ro2"], A, 0.14, ADD_C, 2.5, dashes=14)

        self.play(FadeIn(tb2), FadeIn(to2), FadeIn(te2), Create(arc_b2), Create(arc_o2), run_time=1.0)
        self.wait(0.6)

        cap = self.swap_cap(cap, CAP["g2_right"])
        self.play(Create(ra2), run_time=0.8)
        self.wait(0.8)

        cap = self.swap_cap(cap, CAP["g2_formula"])
        eq2 = MathTex(r"\overline{E_2A}", r"=", r"\sqrt{", r"R_{o2}^{2}", r"-", r"R_{b2}^{2}", r"}", font_size=38).move_to([3.3, 0.0, 0])
        eq2[0].set_color(WARN)
        eq2[3].set_color(ADD_C)
        eq2[5].set_color(BASE_C)
        self.play(FadeIn(eq2, shift=UP * 0.15), run_time=0.8)
        self.wait(0.8)

        cap = self.swap_cap(cap, CAP["g2_ro"])
        self.play(
            Indicate(eq2[3], color=ADD_C, scale_factor=1.15),
            Indicate(s_o2, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        cap = self.swap_cap(cap, CAP["g2_rb"])
        self.play(
            Indicate(eq2[5], color=BASE_C, scale_factor=1.15),
            Indicate(s_b2, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        cap = self.swap_cap(cap, CAP["g2_res"])
        self.play(
            Indicate(eq2[0], color=WARN, scale_factor=1.15),
            Indicate(s_e2a, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        # Numbers for Gear 2: 3.875, 3.5238, 1.612
        num2 = MathTex(
            r"\overline{E_2A}", r"=", r"\sqrt{", r"3.875^{2}", r"-", r"3.5238^{2}", r"}", r"=", r"\mathbf{1.612}\ \mathrm{in}",
            font_size=32
        ).move_to([3.3, -0.9, 0])
        num2[0].set_color(WARN)
        num2[3].set_color(ADD_C)
        num2[5].set_color(BASE_C)
        num2[8].set_color(WARN)
        self.play(FadeIn(num2, shift=UP * 0.1), run_time=0.8)
        self.wait(0.6)

        cap = self.swap_cap(cap, CAP["g2_n_ro"])
        self.play(
            Indicate(num2[3], color=ADD_C, scale_factor=1.15),
            Indicate(s_o2, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(0.8)

        cap = self.swap_cap(cap, CAP["g2_n_rb"])
        self.play(
            Indicate(num2[5], color=BASE_C, scale_factor=1.15),
            Indicate(s_b2, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(0.8)

        cap = self.swap_cap(cap, CAP["g2_n_res"])
        self.play(
            Indicate(num2[8], color=WARN, scale_factor=1.15),
            Indicate(s_e2a, color=WHITE, scale_factor=1.0),
            run_time=1.0
        )
        self.wait(1.0)

        r2_box = SurroundingRectangle(eq2, color=WARN, buff=0.14, stroke_width=3)
        res2_group = VGroup(eq2, r2_box)
        self.play(Create(r2_box), run_time=0.6)
        self.play(
            FadeOut(VGroup(tri2, s_b2, s_o2, s_e2a, tb2, to2, te2, ra2, d_O2, lb_O2, lb_E2, lb_A, arc_b2, arc_o2, num2)),
            res2_group.animate.scale(0.70).move_to([3.3, 0.20, 0]),
            run_time=1.0
        )
        self.wait(0.5)

        # ---------------------------------------------------------
        # Row 11 (50-54s): Outro, both boxed results visible
        # ---------------------------------------------------------
        cap = self.swap_cap(cap, CAP["outro"], size=19)
        self.wait(2.5)
