"""
Transformer teaching video ? 4 scenes:
1. TransformerPrimary: Electrical power at primary coil (V1, I1 -> P1 = V1 * I1)
2. TransformerFlux: Magnetic flux through the shared iron core (Conserved Link)
3. TransformerVoltageRatio: Voltage step-up/down derivation (V2/V1 = N2/N1)
4. TransformerCurrentInverse: Current inverse ratio via power conservation (I2/I1 = N1/N2)
"""

import numpy as np
import os
from manim import *
from mlib import *

# Set Thai font for cross-platform support (Loma on Linux cloud, Leelawadee UI on Windows)
Text.set_default(font=os.environ.get("MANIM_THAI_FONT", "Leelawadee UI"))

def make_transformer_rig(center=np.array([-3.3, -0.35, 0]), n1=5, n2=10):
    """
    Builds a physically plausible 2D transformer with a closed iron core loop
    and continuous helical winding paths wrapped around the core limbs.
    """
    cx, cy, _ = center
    w_core, h_core = 3.6, 4.0
    t_core = 0.75
    w_leg = t_core

    left_x = cx - (w_core/2.0 - t_core/2.0)
    right_x = cx + (w_core/2.0 - t_core/2.0)
    top_y = cy + (h_core/2.0 - t_core/2.0)
    bot_y = cy - (h_core/2.0 - t_core/2.0)

    left_limb = Rectangle(width=t_core, height=h_core, color=METAL, stroke_width=2.5)
    left_limb.set_fill(METAL).set_opacity(0.35).move_to([left_x, cy, 0])

    right_limb = Rectangle(width=t_core, height=h_core, color=METAL, stroke_width=2.5)
    right_limb.set_fill(METAL).set_opacity(0.35).move_to([right_x, cy, 0])

    top_limb = Rectangle(width=w_core, height=t_core, color=METAL, stroke_width=2.5)
    top_limb.set_fill(METAL).set_opacity(0.35).move_to([cx, top_y, 0])

    bot_limb = Rectangle(width=w_core, height=t_core, color=METAL, stroke_width=2.5)
    bot_limb.set_fill(METAL).set_opacity(0.35).move_to([cx, bot_y, 0])

    core_group = VGroup(left_limb, right_limb, top_limb, bot_limb)

    def build_coil(leg_x, n_turns, color, dark_color, y_span=2.4):
        backs = VGroup()
        fronts = VGroup()
        w_wire = w_leg + 0.24
        h_turn = y_span / float(n_turns)
        y_bot = cy - y_span / 2.0

        for i in range(n_turns):
            y_i = y_bot + i * h_turn
            # Back wire passing behind the iron core limb
            b = Line(
                [leg_x + w_wire/2.0, y_i + h_turn * 0.25, 0],
                [leg_x - w_wire/2.0, y_i + h_turn * 0.75, 0],
                color=dark_color, stroke_width=3
            )
            # Front wire wrapping in front of the iron core limb
            f = Line(
                [leg_x - w_wire/2.0, y_i + h_turn * 0.75, 0],
                [leg_x + w_wire/2.0, y_i + h_turn * 1.25, 0],
                color=color, stroke_width=5
            )
            backs.add(b)
            fronts.add(f)

        # Terminal leads (top and bottom)
        sign = -1 if leg_x < cx else 1
        top_lead = Line(
            [leg_x + w_wire/2.0 * sign, y_bot + n_turns * h_turn + h_turn * 0.25, 0],
            [leg_x + (w_wire/2.0 + 0.5) * sign, y_bot + n_turns * h_turn + h_turn * 0.25, 0],
            color=color, stroke_width=4
        )
        bot_lead = Line(
            [leg_x - w_wire/2.0 * sign, y_bot + h_turn * 0.75, 0],
            [leg_x + (w_wire/2.0 + 0.5) * sign, y_bot + h_turn * 0.75, 0],
            color=color, stroke_width=4
        )
        fronts.add(top_lead, bot_lead)
        return backs, fronts

    p_backs, p_fronts = build_coil(left_x, n1, CURRENT, "#B78103", y_span=2.2)
    s_backs, s_fronts = build_coil(right_x, n2, OK, "#00838F", y_span=2.5)

    primary_all = VGroup(p_backs, p_fronts)
    secondary_all = VGroup(s_backs, s_fronts)

    # Flux loop path centered in the iron core limbs
    loop_w = w_core - t_core
    loop_h = h_core - t_core
    flux_loop = RoundedRectangle(
        corner_radius=0.4,
        width=loop_w,
        height=loop_h,
        color=FIELD,
        stroke_width=3
    ).move_to([cx, cy, 0])

    # Flux direction arrows circulating CCW
    arrow_l = Arrow([left_x, cy - 0.45, 0], [left_x, cy + 0.45, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    arrow_t = Arrow([cx - 0.45, top_y, 0], [cx + 0.45, top_y, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    arrow_r = Arrow([right_x, cy + 0.45, 0], [right_x, cy - 0.45, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    arrow_b = Arrow([cx + 0.45, bot_y, 0], [cx - 0.45, bot_y, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    flux_arrows = VGroup(arrow_l, arrow_t, arrow_r, arrow_b)

    rig = {
        "p_backs": p_backs,
        "s_backs": s_backs,
        "core": core_group,
        "p_fronts": p_fronts,
        "s_fronts": s_fronts,
        "primary": primary_all,
        "secondary": secondary_all,
        "flux_loop": flux_loop,
        "flux_arrows": flux_arrows,
        "left_x": left_x,
        "right_x": right_x,
        "top_y": top_y,
        "bot_y": bot_y,
        "center": center
    }
    return rig


class TransformerPrimary(SafeScene):
    """Clip 1: Electrical power at primary coil"""

    def construct(self):
        self.add(title("????????????? ? ?????? 1: ???????????????? (Primary)", size=27))
        cap = caption_top("???????????? (N1 = 5 ???): ????????? V1 ???????????? I1 ???????????", size=21)
        self.add(cap)

        rig = make_transformer_rig()
        rig["s_backs"].set_opacity(0.2)
        rig["s_fronts"].set_opacity(0.2)

        self.play(
            FadeIn(rig["p_backs"]),
            FadeIn(rig["s_backs"]),
            FadeIn(rig["core"]),
            FadeIn(rig["p_fronts"]),
            FadeIn(rig["s_fronts"]),
            run_time=1.0
        )

        lx = rig["left_x"]
        v1_tag = Text("V1 = 230 V", font_size=20, color=CURRENT).move_to([lx - 1.45, 1.0, 0])
        i1_tag = Text("I1 = 10 A", font_size=20, color=WARN).move_to([lx - 1.45, -1.0, 0])
        n1_tag = Text("N1 = 5 ???", font_size=21, color=CURRENT).move_to([lx, -2.7, 0])
        current_arrow = Arrow([lx - 1.1, -0.6, 0], [lx - 0.5, -0.6, 0], color=WARN, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)

        self.play(FadeIn(v1_tag), FadeIn(i1_tag), FadeIn(current_arrow), FadeIn(n1_tag), run_time=0.8)

        p_x = 3.6
        box_title = Text("1. ???????????????? (Input Power)", font_size=22, color=CURRENT).move_to([p_x, 2.0, 0])
        step1 = Text("? ????????????????????????????? AC", font_size=19, color=GRAYTXT).move_to([p_x, 1.45, 0])
        step2 = Text("? ?????????????: V1 = 230 V", font_size=19, color=CURRENT).move_to([p_x, 1.05, 0])
        step3 = Text("? ???????????????: I1 = 10 A", font_size=19, color=WARN).move_to([p_x, 0.65, 0])

        eq_label = Text("??????????????:", font_size=20, color=WHITE).move_to([p_x, 0.05, 0])
        eq_math = Text("P1 = V1 ? I1", font_size=25, color=WHITE).move_to([p_x, -0.45, 0])
        eq_sub = Text("P1 = 230 V ? 10 A", font_size=22, color=YELLOW).move_to([p_x, -0.95, 0])
        eq_res = Text("P1 = 2300 W", font_size=27, color=OK).move_to([p_x, -1.5, 0])
        res_box = SurroundingRectangle(eq_res, color=OK, buff=0.15)

        note_foot = Text("???????? 2300 W ??? ???????????????????????????????????????", font_size=17, color=GRAYTXT).move_to([p_x, -2.15, 0])

        self.play(FadeIn(box_title), FadeIn(step1), FadeIn(step2), FadeIn(step3), run_time=0.9)
        self.wait(0.5)
        self.play(FadeIn(eq_label), FadeIn(eq_math), FadeIn(eq_sub), run_time=0.8)
        self.play(FadeIn(eq_res), run_time=0.6)
        self.play(Indicate(eq_res, color=OK, scale_factor=1.0), run_time=0.6)
        self.play(Create(res_box), FadeIn(note_foot), run_time=0.8)
        self.wait(1.5)


class TransformerFlux(SafeScene):
    """Clip 2: Magnetic flux through the core"""

    def construct(self):
        self.add(title("????????????? ? ?????? 2: ???????????????????????? (Flux ?)", size=27))
        cap = caption_top("???????????????????????????? ? ?????????????????????????", size=21)
        self.add(cap)

        rig = make_transformer_rig()
        self.play(
            FadeIn(rig["p_backs"]),
            FadeIn(rig["s_backs"]),
            FadeIn(rig["core"]),
            FadeIn(rig["p_fronts"]),
            FadeIn(rig["s_fronts"]),
            run_time=0.8
        )

        flux_loop = rig["flux_loop"]
        flux_arrows = rig["flux_arrows"]
        cx, cy = rig["center"][0], rig["center"][1]
        flux_tag = VGroup(
            Text("?????????????? ?", font_size=17, color=FIELD),
            Text("(??????? Conserved)", font_size=14, color=FIELD)
        ).arrange(DOWN, buff=0.1).move_to([cx, cy, 0])

        self.play(Create(flux_loop), FadeIn(flux_arrows), FadeIn(flux_tag), run_time=1.0)
        self.play(Indicate(flux_tag, color=FIELD, scale_factor=1.0), run_time=0.7)

        p_x = 3.6
        box_title = Text("2. ????????????????????? (Conserved Link)", font_size=22, color=FIELD).move_to([p_x, 2.0, 0])
        b1 = Text("? ??????????????????????????????????????????????", font_size=18, color=GRAYTXT).move_to([p_x, 1.45, 0])
        b2 = Text("? ?????????????? ? ???????????????????????????", font_size=18, color=WHITE).move_to([p_x, 1.05, 0])
        b3 = Text("? ????????? 2 ??????????????????????????????? 100%", font_size=18, color=OK).move_to([p_x, 0.65, 0])

        faraday_title = Text("????????????????????????? (Faraday's Law):", font_size=19, color=WARN).move_to([p_x, 0.05, 0])
        f_eq = Text("?????????????????? 1 ??? = ?? / ?t", font_size=22, color=YELLOW).move_to([p_x, -0.45, 0])
        f_box = SurroundingRectangle(f_eq, color=YELLOW, buff=0.12)
        f_sub = Text("???? 1 ??????????? ???????????????????????????", font_size=18, color=GRAYTXT).move_to([p_x, -1.0, 0])
        f_sub2 = Text("??????????????????????????????????!", font_size=19, color=OK).move_to([p_x, -1.35, 0])

        takeaway = Text("?????????????????????????????????????????????????????????", font_size=17, color=GRAYTXT).move_to([p_x, -2.0, 0])

        self.play(FadeIn(box_title), FadeIn(b1), FadeIn(b2), FadeIn(b3), run_time=0.9)
        self.wait(0.5)
        self.play(FadeIn(faraday_title), FadeIn(f_eq), run_time=0.8)
        self.play(Indicate(f_eq, color=YELLOW, scale_factor=1.0), run_time=0.6)
        self.play(Create(f_box), FadeIn(f_sub), FadeIn(f_sub2), FadeIn(takeaway), run_time=0.9)
        self.wait(1.5)


class TransformerVoltageRatio(SafeScene):
    """Clip 3: Voltage step-up/down relationship"""

    def construct(self):
        self.add(title("????????????? ? ?????? 3: ??????????????? (Voltage Ratio)", size=27))
        cap = caption_top("?????????????????: ???????????????????? ?????????????????????????????", size=21)
        self.add(cap)

        rig = make_transformer_rig()
        self.play(
            FadeIn(rig["p_backs"]),
            FadeIn(rig["s_backs"]),
            FadeIn(rig["core"]),
            FadeIn(rig["p_fronts"]),
            FadeIn(rig["s_fronts"]),
            FadeIn(rig["flux_loop"]),
            FadeIn(rig["flux_arrows"]),
            run_time=0.8
        )

        lx, rx = rig["left_x"], rig["right_x"]
        n1_lbl = Text("N1 = 5 ???", font_size=20, color=CURRENT).move_to([lx, -2.7, 0])
        n2_lbl = Text("N2 = 10 ??? (2 ????)", font_size=20, color=OK).move_to([rx, -2.7, 0])
        v1_lbl = Text("V1 = 230 V", font_size=20, color=CURRENT).move_to([lx - 1.4, 0.6, 0])
        v2_lbl = Text("V2 = ?", font_size=22, color=OK).move_to([rx + 1.35, 0.6, 0])

        self.play(FadeIn(n1_lbl), FadeIn(n2_lbl), FadeIn(v1_lbl), FadeIn(v2_lbl), run_time=0.8)

        p_x = 3.6
        p_title = Text("3. ????????????????? (Voltage Ratio)", font_size=22, color=OK).move_to([p_x, 2.05, 0])
        r1 = Text("?????????????????????????????????????????:", font_size=18, color=GRAYTXT).move_to([p_x, 1.55, 0])
        r2 = Text("V1 = N1 ? (??/?t)   ?   ??/?t = V1 / N1", font_size=20, color=CURRENT).move_to([p_x, 1.1, 0])
        r3 = Text("V2 = N2 ? (??/?t)   ?   ??/?t = V2 / N2", font_size=20, color=OK).move_to([p_x, 0.65, 0])

        link_txt = Text("????????? ??/?t ???????????????????????:", font_size=18, color=WHITE).move_to([p_x, 0.15, 0])
        ratio_box = Text("V2 / V1 = N2 / N1", font_size=26, color=YELLOW).move_to([p_x, -0.35, 0])
        box_rect = SurroundingRectangle(ratio_box, color=YELLOW, buff=0.12)

        calc_txt = Text("?????????????????? (Step-Up 2 ????):", font_size=18, color=GRAYTXT).move_to([p_x, -0.9, 0])
        calc_eq = Text("V2 = (10 / 5) ? 230 V", font_size=21, color=WHITE).move_to([p_x, -1.3, 0])
        res_v2 = Text("V2 = 460 V", font_size=26, color=OK).move_to([p_x, -1.75, 0])
        res_v2_box = SurroundingRectangle(res_v2, color=OK, buff=0.12)

        self.play(FadeIn(p_title), FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.9)
        self.wait(0.4)
        self.play(FadeIn(link_txt), FadeIn(ratio_box), run_time=0.8)
        self.play(Indicate(ratio_box, color=YELLOW, scale_factor=1.0), run_time=0.6)
        self.play(Create(box_rect), FadeIn(calc_txt), FadeIn(calc_eq), FadeIn(res_v2), run_time=0.8)
        self.play(Indicate(res_v2, color=OK, scale_factor=1.0), run_time=0.6)
        self.play(Create(res_v2_box), run_time=0.5)

        v2_real = Text("V2 = 460 V", font_size=22, color=OK).move_to([rx + 1.45, 0.6, 0])
        self.play(Transform(v2_lbl, v2_real), run_time=0.8)
        self.wait(1.5)


class TransformerCurrentInverse(SafeScene):
    """Clip 4: Current relationship (power conservation)"""

    def construct(self):
        self.add(title("????????????? ? ?????? 4: ????????????????????????? (Current)", size=26))
        cap = caption_top("????????????????? ???????????????????: P_in = P_out (V ????? -> I ??????)", size=21)
        self.add(cap)

        rig = make_transformer_rig()
        self.play(
            FadeIn(rig["p_backs"]),
            FadeIn(rig["s_backs"]),
            FadeIn(rig["core"]),
            FadeIn(rig["p_fronts"]),
            FadeIn(rig["s_fronts"]),
            FadeIn(rig["flux_loop"]),
            FadeIn(rig["flux_arrows"]),
            run_time=0.8
        )

        lx, rx = rig["left_x"], rig["right_x"]
        p1_tag = Text("P1 = 2300 W", font_size=19, color=CURRENT).move_to([lx - 1.4, 0.7, 0])
        i1_tag = Text("I1 = 10 A", font_size=19, color=WARN).move_to([lx - 1.4, 0.2, 0])
        p2_tag = Text("P2 = 2300 W", font_size=19, color=OK).move_to([rx + 1.45, 0.7, 0])
        i2_tag = Text("I2 = ?", font_size=21, color=WARN).move_to([rx + 1.45, 0.2, 0])

        self.play(FadeIn(p1_tag), FadeIn(i1_tag), FadeIn(p2_tag), FadeIn(i2_tag), run_time=0.8)

        p_x = 3.6
        p_title = Text("4. ????????????????? (P1 = P2)", font_size=22, color=WARN).move_to([p_x, 2.05, 0])
        c1 = Text("???????????????? ??????????????????????????:", font_size=18, color=GRAYTXT).move_to([p_x, 1.6, 0])
        c2 = Text("V1 ? I1 = V2 ? I2", font_size=23, color=WHITE).move_to([p_x, 1.15, 0])
        c3 = Text("230 V ? 10 A = 460 V ? I2", font_size=20, color=YELLOW).move_to([p_x, 0.7, 0])
        c4 = Text("2300 W = 460 V ? I2  ?  I2 = 5 A", font_size=22, color=WARN).move_to([p_x, 0.25, 0])
        c4_box = SurroundingRectangle(c4, color=WARN, buff=0.12)

        self.play(FadeIn(p_title), FadeIn(c1), FadeIn(c2), FadeIn(c3), FadeIn(c4), run_time=0.9)
        self.play(Indicate(c4, color=WARN, scale_factor=1.0), run_time=0.6)
        self.play(Create(c4_box), run_time=0.5)

        i2_real = Text("I2 = 5 A", font_size=21, color=WARN).move_to([rx + 1.45, 0.2, 0])
        self.play(Transform(i2_tag, i2_real), run_time=0.6)

        sum_title = Text("????????????????????? (Master Formula):", font_size=19, color=WHITE).move_to([p_x, -0.4, 0])
        master_eq = Text("V2 / V1 = N2 / N1 = I1 / I2", font_size=25, color=OK).move_to([p_x, -0.9, 0])
        master_box = SurroundingRectangle(master_eq, color=OK, buff=0.15)

        note_v = Text("? ?????? V ???????????????????? N", font_size=18, color=CURRENT).move_to([p_x, -1.5, 0])
        note_i = Text("? ????? I ??????????????????? N", font_size=18, color=WARN).move_to([p_x, -1.88, 0])
        note_final = Text("??????????? 2 ???? ? ??????????????????? ???????? P ?????", font_size=17, color=GRAYTXT).move_to([p_x, -2.3, 0])

        self.play(FadeIn(sum_title), FadeIn(master_eq), run_time=0.8)
        self.play(Indicate(master_eq, color=OK, scale_factor=1.0), run_time=0.6)
        self.play(Create(master_box), FadeIn(note_v), FadeIn(note_i), FadeIn(note_final), run_time=0.8)
        self.wait(1.5)
