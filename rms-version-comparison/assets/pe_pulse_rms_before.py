import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# ==============================================================================
# AUTHORITATIVE PRODUCTION DIRECTION: Power Electronics — RMS Pulse Lesson
# Source: Erickson, Fundamentals of Power Electronics, Appendix 1 (Figure A1.5)
# Conceptual Source: EE328 Power Computations, Pages 6–7 (Effective Value: RMS)
# Script Spec: Claude_Specs/Power Electronics — RMS Pulse Director Brief.md
# ==============================================================================

# Strict Color Palette per Director Brief
COL_VOLT   = "#42A5F5"   # Muted electric blue: DC source / voltage
COL_CURR   = "#FFB300"   # Warm yellow: pulse current i(t) / current dots
COL_HEAT   = "#FF5722"   # Orange-red: i(t)^2 and instantaneous heating
COL_DUTY   = "#AB47BC"   # Violet-purple: duty time and synchronized cursor
COL_RMS    = "#4CAF50"   # Emerald green: equivalent DC / RMS / validated equality
COL_TRAP   = "#EF5350"   # Red: misconception / invalid calculation
COL_WIRE   = "#94A3B8"   # Slate gray: neutral structure / axes / wires
COL_BG_BOX = "#1E293B"   # Dark card background


class PulseRmsTeachingScene(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # Persistent Top HUD
        # ----------------------------------------------------------------------
        ttl = title("RMS ของกระแสพัลส์: ทำไม I_rms = I_pk sqrt(D)", size=26).shift(UP * 0.35)
        pref = page_ref("Power Electronics · RMS A1.5", size=15, color=COL_WIRE)

        # ----------------------------------------------------------------------
        # SHOT 1 — 0:00–0:05 — Cold open / question
        # ----------------------------------------------------------------------
        self.wait(0.3)
        self.play(ttl.animate.shift(DOWN * 0.35), FadeIn(pref), run_time=0.6)

        # Left 40% Zone (Circuit / Thermal World, centered at x = -4.0, y = 0.5)
        cx = -4.0
        cy = 0.5
        src_circ = Circle(radius=0.45, color=COL_VOLT, stroke_width=3).move_to([cx - 1.3, cy, 0])
        src_txt = Text("12 V", font_size=14, color=COL_VOLT).move_to(src_circ.get_center())
        src_grp = VGroup(src_circ, src_txt)

        # Resistor on right side of loop
        res_rect = Rectangle(width=0.55, height=1.1, color=COL_HEAT, fill_color=COL_BG_BOX, fill_opacity=0.9, stroke_width=2.5).move_to([cx + 1.3, cy, 0])
        res_txt = Text("R\n1 Ω", font_size=12, color=WHITE).move_to(res_rect.get_center())
        res_grp = VGroup(res_rect, res_txt)

        # Switch at top rail
        sw_l = Dot([cx - 0.35, cy + 1.0, 0], radius=0.06, color=COL_DUTY)
        sw_r = Dot([cx + 0.35, cy + 1.0, 0], radius=0.06, color=COL_DUTY)
        sw_arm = Line([cx - 0.35, cy + 1.0, 0], [cx + 0.3, cy + 1.35, 0], color=COL_DUTY, stroke_width=3)
        sw_grp = VGroup(sw_l, sw_r, sw_arm)

        # Wires
        w1 = Line(src_circ.get_top(), [cx - 1.3, cy + 1.0, 0], color=COL_WIRE, stroke_width=2)
        w2 = Line([cx - 1.3, cy + 1.0, 0], sw_l.get_center(), color=COL_WIRE, stroke_width=2)
        w3 = Line(sw_r.get_center(), [cx + 1.3, cy + 1.0, 0], color=COL_WIRE, stroke_width=2)
        w4 = Line([cx + 1.3, cy + 1.0, 0], res_rect.get_top(), color=COL_WIRE, stroke_width=2)
        w5 = Line(res_rect.get_bottom(), [cx + 1.3, cy - 1.0, 0], color=COL_WIRE, stroke_width=2)
        w6 = Line([cx + 1.3, cy - 1.0, 0], [cx - 1.3, cy - 1.0, 0], color=COL_WIRE, stroke_width=2)
        w7 = Line([cx - 1.3, cy - 1.0, 0], src_circ.get_bottom(), color=COL_WIRE, stroke_width=2)
        wires = VGroup(w1, w2, w3, w4, w5, w6, w7)

        circuit_hero = VGroup(src_grp, sw_grp, res_grp, wires)

        # Callout labels outside the loop with routed leaders
        leader_src = Line([cx - 2.3, cy + 0.5, 0], [cx - 1.4, cy + 0.2, 0], color=COL_VOLT, stroke_width=1.5)
        lbl_call_src = Text("แหล่งจ่าย", font_size=13, color=COL_VOLT).next_to(leader_src.get_start(), LEFT, buff=0.08)

        leader_sw = Line([cx, cy + 1.8, 0], [cx, cy + 1.2, 0], color=COL_DUTY, stroke_width=1.5)
        lbl_call_sw = Text("สวิตช์", font_size=13, color=COL_DUTY).next_to(leader_sw.get_start(), UP, buff=0.08)

        leader_res = Line([cx + 2.3, cy + 0.5, 0], [cx + 1.4, cy + 0.2, 0], color=COL_HEAT, stroke_width=1.5)
        lbl_call_res = Text("R = 1 Ω", font_size=13, color=COL_HEAT).next_to(leader_res.get_start(), RIGHT, buff=0.08)

        callouts_grp = VGroup(leader_src, lbl_call_src, leader_sw, lbl_call_sw, leader_res, lbl_call_res)

        # Right 60% Zone (Time / Waveform World, centered at x = 2.8, y = 0.5)
        ax_x = 2.8
        ax_y = 0.5
        ax_wave = Axes(
            x_range=[0, 4.2, 1], y_range=[0, 2.5, 1],
            x_length=4.8, y_length=2.3,
            tips=True,
            axis_config={"color": COL_WIRE, "stroke_width": 2}
        ).move_to([ax_x, ax_y, 0])
        lbl_ax_i = Text("i(t)", font_size=14, color=COL_CURR).next_to(ax_wave.y_axis.get_top(), LEFT, buff=0.08)
        lbl_ax_t = Text("t", font_size=14, color=COL_WIRE).next_to(ax_wave.x_axis.get_right(), DOWN, buff=0.08)
        lbl_ts = Text("Ts", font_size=13, color=WHITE).next_to(ax_wave.c2p(3.6, 0), DOWN, buff=0.1)
        axes_hero = VGroup(ax_wave, lbl_ax_i, lbl_ax_t, lbl_ts)

        cap = caption_top("กระแสเปิดเป็นช่วง ๆ — แล้ว R ร้อนเท่ากับ DC กี่แอมป์?", size=20)

        # Play shot 1
        self.play(Create(wires), Create(src_circ), FadeIn(src_txt), Create(sw_grp), Create(res_grp), run_time=1.3)
        self.play(
            FadeIn(leader_src), FadeIn(lbl_call_src),
            FadeIn(leader_sw), FadeIn(lbl_call_sw),
            FadeIn(leader_res), FadeIn(lbl_call_res),
            FadeIn(axes_hero), FadeIn(cap),
            run_time=0.8
        )
        # Orange pulse on resistor on the word 'R'
        self.play(
            res_rect.animate.set_fill(color=COL_HEAT, opacity=0.85),
            Flash(res_rect, color=COL_HEAT, flash_radius=0.35),
            run_time=0.6
        )
        self.play(res_rect.animate.set_fill(color=COL_BG_BOX, opacity=0.9), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(callouts_grp), run_time=0.4)

        # ----------------------------------------------------------------------
        # SHOT 2 — 0:05–0:13 — Meaning before definition
        # ----------------------------------------------------------------------
        cap2 = caption_top("RMS คือค่า DC ที่ทำให้ตัวต้านทานร้อนเฉลี่ยเท่ากัน", size=20)
        self.play(
            Transform(cap, cap2),
            circuit_hero.animate.scale(0.9).move_to([cx, cy + 0.15, 0]),
            run_time=0.5
        )

        # Two-card thermal comparator rising from below in lower-left / center
        card_l = RoundedRectangle(corner_radius=0.15, width=4.0, height=1.6, color=COL_RMS, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([-3.8, -2.1, 0])
        r_dc = Rectangle(width=0.45, height=0.8, color=COL_HEAT, fill_color="#FF5722", fill_opacity=0.3).move_to([-5.0, -2.1, 0])
        lbl_dc = Text("DC 5 A ต่อเนื่อง", font_size=13, color=COL_RMS).next_to(r_dc, RIGHT, buff=0.2)
        card_l_grp = VGroup(card_l, r_dc, lbl_dc)

        card_r = RoundedRectangle(corner_radius=0.15, width=4.0, height=1.6, color=COL_CURR, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([1.2, -2.1, 0])
        r_pulse = Rectangle(width=0.45, height=0.8, color=COL_HEAT, fill_color="#FF5722", fill_opacity=0.3).move_to([0.0, -2.1, 0])
        lbl_pulse = Text("กระแสพัลส์สลับ", font_size=13, color=COL_CURR).next_to(r_pulse, RIGHT, buff=0.2)
        card_r_grp = VGroup(card_r, r_pulse, lbl_pulse)

        lbl_eq = Text("ความร้อนเฉลี่ยเท่ากัน!", font_size=13, color=COL_HEAT).move_to([-1.3, -1.1, 0])
        comp_cards = VGroup(card_l_grp, card_r_grp, lbl_eq).shift(DOWN * 0.8)

        self.play(comp_cards.animate.shift(UP * 0.8), run_time=0.8)

        # Warm orange glow on both resistors settling into matched intensity
        self.play(
            r_dc.animate.set_fill(color=COL_HEAT, opacity=0.95),
            r_pulse.animate.set_fill(color=COL_HEAT, opacity=0.95),
            Flash(r_dc, color=COL_HEAT, flash_radius=0.3),
            Flash(r_pulse, color=COL_HEAT, flash_radius=0.3),
            run_time=0.9
        )
        self.wait(1.0)
        self.play(
            comp_cards.animate.shift(DOWN * 1.5).set_opacity(0),
            circuit_hero.animate.scale(1.0 / 0.9).move_to([cx, cy, 0]),
            run_time=0.6
        )
        self.remove(comp_cards)

        # ----------------------------------------------------------------------
        # SHOT 3 — 0:13–0:22 — Define the pulse in time
        # ----------------------------------------------------------------------
        cap3 = caption_top("สวิตช์เปิดนาน D Ts จากหนึ่งคาบ Ts: กระแสมี Ipk เฉพาะช่วง ON", size=19)
        self.play(Transform(cap, cap3), run_time=0.5)

        # Narrow switch-state rail below circuit (x from cx - 1.3 to cx + 1.3, y = -1.05)
        rail_w = 2.6
        rail_y = -1.05
        rail_on = Rectangle(width=rail_w * 0.25, height=0.28, color=COL_DUTY, fill_color=COL_DUTY, fill_opacity=0.85).move_to([cx - 1.3 + (rail_w * 0.25) / 2, rail_y, 0])
        lbl_on = Text("ON", font_size=11, color=WHITE).move_to(rail_on.get_center())
        rail_off = Rectangle(width=rail_w * 0.75, height=0.28, color=COL_WIRE, fill_color=COL_BG_BOX, fill_opacity=0.85).move_to([cx - 1.3 + rail_w * 0.25 + (rail_w * 0.75) / 2, rail_y, 0])
        lbl_off = Text("OFF", font_size=11, color=COL_WIRE).move_to(rail_off.get_center())
        switch_rail = VGroup(rail_on, lbl_on, rail_off, lbl_off)

        # Waveform parameters: Ts = 3.6, D = 0.25 -> Ton = 0.9, Ipk = 1.8
        ts_w = 3.6
        d_val = 0.25
        ton_w = d_val * ts_w  # 0.9

        pw0 = ax_wave.c2p(0, 0)
        pw1 = ax_wave.c2p(0, 1.8)
        pw2 = ax_wave.c2p(ton_w, 1.8)
        pw3 = ax_wave.c2p(ton_w, 0)
        pw4 = ax_wave.c2p(ts_w, 0)
        pulse_path = VMobject(color=COL_CURR, stroke_width=3.5).set_points_as_corners([pw0, pw1, pw2, pw3, pw4])

        lbl_ipk_tag = Text("Ipk", font_size=13, color=COL_CURR).next_to(pw1, LEFT, buff=0.08)
        brk_dts = BraceBetweenPoints(pw1, pw2, UP, color=COL_DUTY, buff=0.08)
        lbl_dts = Text("D Ts", font_size=12, color=COL_DUTY).next_to(brk_dts, UP, buff=0.06)
        brk_ts = BraceBetweenPoints(ax_wave.c2p(0, -0.08), ax_wave.c2p(ts_w, -0.08), DOWN, color=COL_WIRE, buff=0.12)
        lbl_ts_b = Text("Ts", font_size=12, color=COL_WIRE).next_to(brk_ts, DOWN, buff=0.05)

        lbl_d_def = Text("D = เวลาเปิด / 1 คาบ", font_size=12, color=COL_DUTY).move_to([ax_x + 1.2, ax_y + 1.6, 0])

        self.play(
            FadeIn(switch_rail),
            Create(pulse_path),
            FadeIn(lbl_ipk_tag), FadeIn(brk_dts), FadeIn(lbl_dts), FadeIn(brk_ts), FadeIn(lbl_ts_b), FadeIn(lbl_d_def),
            run_time=1.0
        )

        # Synchronized cursor moving across 3s
        cursor_val = ValueTracker(0.0)
        cursor_wave = always_redraw(lambda: Line(
            [ax_wave.c2p(cursor_val.get_value(), 0)[0], ax_wave.c2p(0, 2.2)[1], 0],
            [ax_wave.c2p(cursor_val.get_value(), 0)[0], ax_wave.c2p(0, -0.1)[1], 0],
            color=COL_DUTY, stroke_width=2.0
        ))

        # Current circulating dots along wires
        dot_c1 = Dot([cx - 0.35, cy + 1.0, 0], radius=0.07, color=COL_CURR)
        dot_c2 = Dot([cx + 0.4, cy + 1.0, 0], radius=0.07, color=COL_CURR)
        dots_grp = VGroup(dot_c1, dot_c2)

        sw_arm_shut = Line([cx - 0.35, cy + 1.0, 0], [cx + 0.35, cy + 1.0, 0], color=COL_DUTY, stroke_width=3)
        sw_arm_shut_back = Line([cx - 0.35, cy + 1.0, 0], [cx + 0.3, cy + 1.35, 0], color=COL_DUTY, stroke_width=3)

        self.add(cursor_wave)
        # Quarter 1 (0 -> ton_w): switch closes, dots flow, pulse high
        self.play(
            Transform(sw_arm, sw_arm_shut),
            FadeIn(dots_grp),
            dot_c1.animate.move_to([cx + 1.3, cy + 0.5, 0]),
            dot_c2.animate.move_to([cx + 1.3, cy - 0.5, 0]),
            cursor_val.animate.set_value(ton_w),
            run_time=1.0, rate_func=linear
        )
        # Remaining 3 quarters: switch opens, dots fade, pulse zero
        self.play(
            Transform(sw_arm, sw_arm_shut_back),
            FadeOut(dots_grp),
            cursor_val.animate.set_value(ts_w),
            run_time=1.8, rate_func=linear
        )
        self.wait(0.5)
        cursor_wave.clear_updaters()
        self.remove(cursor_wave)
        # no brace fadeout

        # ----------------------------------------------------------------------
        # SHOT 4 — 0:22–0:32 — Show why the square matters
        # ----------------------------------------------------------------------
        cap4 = caption_top("ความร้อนของ R ขึ้นกับ i²: ช่วง ON จึงให้ Ipk² R, ช่วง OFF ให้ศูนย์", size=19)
        self.play(Transform(cap, cap4), run_time=0.5)

        # Lower panel for i(t)^2 at x = 2.8, y = -1.45 (in right world!)
        ax_sq = Axes(
            x_range=[0, 4.2, 1], y_range=[0, 2.5, 1],
            x_length=4.8, y_length=1.4,
            tips=True,
            axis_config={"color": COL_WIRE, "stroke_width": 1.8}
        ).move_to([ax_x, -1.45, 0])
        lbl_ax_isq = Text("i(t)^2", font_size=13, color=COL_HEAT).next_to(ax_sq.y_axis.get_top(), LEFT, buff=0.08)

        sq_p0 = ax_sq.c2p(0, 0)
        sq_p1 = ax_sq.c2p(0, 1.8)
        sq_p2 = ax_sq.c2p(ton_w, 1.8)
        sq_p3 = ax_sq.c2p(ton_w, 0)
        sq_p4 = ax_sq.c2p(ts_w, 0)
        sq_path = VMobject(color=COL_HEAT, stroke_width=3.2).set_points_as_corners([sq_p0, sq_p1, sq_p2, sq_p3, sq_p4])
        lbl_ipksq = Text("Ipk^2", font_size=13, color=COL_HEAT).next_to(sq_p1, LEFT, buff=0.08)

        # Tiny physical relation beside resistor in left world
        lbl_pr_formula = Text("P_R(t) = i(t)^2 R", font_size=13, color=COL_HEAT).move_to([cx, -1.8, 0])

        self.play(
            Create(ax_sq), FadeIn(lbl_ax_isq),
            TransformFromCopy(pulse_path, sq_path), FadeIn(lbl_ipksq),
            FadeIn(lbl_pr_formula),
            res_rect.animate.set_fill(color=COL_HEAT, opacity=0.9),
            Flash(sq_path, color=COL_HEAT, flash_radius=0.35),
            run_time=1.2
        )
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # SHOT 5 — 0:32–0:45 — Mean over the whole period
        # ----------------------------------------------------------------------
        cap5 = caption_top("เฉลี่ยทั้งคาบ แต่มีพื้นที่ความร้อนแค่ D Ts จึงเหลือ Ipk² D", size=20)
        self.play(
            Transform(cap, cap5),
            circuit_hero.animate.set_opacity(0.3),
            switch_rail.animate.set_opacity(0.3),
            lbl_pr_formula.animate.set_opacity(0.3),
            run_time=0.5
        )

        # Shade orange i^2 ON rectangle
        sq_shade = Polygon(sq_p0, sq_p1, sq_p2, sq_p3, color=COL_HEAT, fill_color=COL_HEAT, fill_opacity=0.35, stroke_width=0)
        # Green horizontal strip at height 1.8 * d_val = 0.45 across entire Ts
        mean_h = 1.8 * d_val
        strip_start = ax_sq.c2p(0, mean_h)
        strip_end = ax_sq.c2p(ts_w, mean_h)
        mean_line = Line(strip_start, strip_end, color=COL_RMS, stroke_width=3.5)
        lbl_mean_line = Text("mean(i²)", font_size=12, color=COL_RMS).next_to(strip_end, RIGHT, buff=0.08)

        self.play(FadeIn(sq_shade), Create(mean_line), FadeIn(lbl_mean_line), run_time=0.8)

        # Build derivation in 3 steps at bottom-right (x = 2.8, y = -2.7)
        deriv_box = RoundedRectangle(corner_radius=0.15, width=5.6, height=1.3, color="#475569", fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([ax_x, -2.75, 0])
        eq_st1 = Text("mean(i²) = (1 / Ts) × area under i²", font_size=13, color=WHITE).move_to(deriv_box.get_center())
        eq_st2 = Text("mean(i²) = (1 / Ts) × (Ipk² × D Ts)", font_size=13, color=COL_DUTY).move_to(deriv_box.get_center())
        eq_st3 = Text("mean(i²) = Ipk² D", font_size=16, color=COL_RMS).move_to(deriv_box.get_center())

        self.play(FadeIn(deriv_box), FadeIn(eq_st1), run_time=0.6)
        self.wait(0.8)
        self.play(Transform(eq_st1, eq_st2), run_time=0.6)
        self.wait(0.8)
        self.play(Transform(eq_st1, eq_st3), run_time=0.6)
        self.wait(0.7)

        # ----------------------------------------------------------------------
        # SHOT 6 — 0:45–0:55 — Root restores current units
        # ----------------------------------------------------------------------
        cap6 = caption_top("ถอดรากเพื่อกลับจาก A² เป็น A: นี่คือ RMS", size=20)
        self.play(Transform(cap, cap6), run_time=0.5)

        # DC resistor card returns at lower left (x = -4.0, y = -2.5)
        card_mini = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.1, color=COL_RMS, fill_color=COL_BG_BOX, fill_opacity=0.9).move_to([cx, -2.5, 0])
        lbl_bridge = Text("Irms² = mean(i²)", font_size=13, color=COL_RMS).move_to(card_mini.get_center())
        card_mini_grp = VGroup(card_mini, lbl_bridge)

        # Morph derivation panel to large centered formula at bottom-right (x = 2.8, y = -2.75)
        formula_hero = Text("Irms = Ipk sqrt(D)", font_size=22, color=COL_RMS).move_to(deriv_box.get_center())

        # Three tiny word-cards: Square -> Mean -> Root placed above formula at y = -2.0
        w_sq = Text("Square", font_size=11, color=COL_HEAT).move_to([ax_x - 1.4, -2.0, 0])
        arr_m1 = Text("->", font_size=11, color=COL_WIRE).move_to([ax_x - 0.7, -2.0, 0])
        w_mean = Text("Mean", font_size=11, color=COL_DUTY).move_to([ax_x, -2.0, 0])
        arr_m2 = Text("->", font_size=11, color=COL_WIRE).move_to([ax_x + 0.7, -2.0, 0])
        w_root = Text("Root", font_size=11, color=COL_RMS).move_to([ax_x + 1.4, -2.0, 0])
        cards_smr = VGroup(w_sq, arr_m1, w_mean, arr_m2, w_root)

        unit_cue = Text("A² -> sqrt -> A", font_size=12, color=WHITE).move_to([ax_x, -1.6, 0])

        self.play(
            FadeIn(card_mini_grp),
            Transform(eq_st1, formula_hero),
            run_time=0.8
        )
        self.play(FadeIn(cards_smr), FadeIn(unit_cue), run_time=0.8)
        self.wait(1.2)

        # Clear i^2 graph and transient cards to make room for Shot 7
        self.play(
            FadeOut(card_mini_grp), FadeOut(cards_smr), FadeOut(unit_cue),
            FadeOut(ax_sq), FadeOut(lbl_ax_isq), FadeOut(sq_path), FadeOut(lbl_ipksq), FadeOut(sq_shade),
            FadeOut(mean_line), FadeOut(lbl_mean_line),
            run_time=0.6
        )

        # ----------------------------------------------------------------------
        # SHOT 7 — 0:55–1:07 — Numerical proof with equal heat
        # ----------------------------------------------------------------------
        cap7 = caption_top("10 A ที่เปิด 25% ของเวลา ร้อนเท่ากับ DC 5 A: ทั้งคู่เฉลี่ย 25 W", size=19)
        self.play(Transform(cap, cap7), run_time=0.5)

        # Direct labels on waveform: Ipk = 10 A, D = 0.25
        lbl_ipk_10 = Text("Ipk = 10 A", font_size=13, color=COL_CURR).next_to(pw1, LEFT, buff=0.08)
        lbl_dts_25 = Text("D = 0.25", font_size=12, color=COL_DUTY).next_to(brk_dts, UP, buff=0.06)
        self.play(
            Transform(lbl_ipk_tag, lbl_ipk_10),
            Transform(lbl_dts, lbl_dts_25),
            run_time=0.5
        )

        # Substitute formula in right world: Irms = Ipk sqrt(D) -> 10 sqrt(0.25) -> 5 A
        f_sub1 = Text("Irms = 10 sqrt(0.25)", font_size=17, color=WHITE).move_to(deriv_box.get_center())
        f_sub2 = Text("Irms = 5 A", font_size=20, color=COL_RMS).move_to(deriv_box.get_center())

        self.play(Transform(eq_st1, f_sub1), run_time=0.7)
        self.wait(0.6)
        self.play(Transform(eq_st1, f_sub2), run_time=0.7)

        # Two heat bars in the left thermal world (under circuit at y = -2.1)
        h_bg_l = Rectangle(width=1.4, height=1.3, color="#334155", fill_color=COL_BG_BOX, fill_opacity=0.6).move_to([cx - 0.9, -2.1, 0])
        h_bg_r = Rectangle(width=1.4, height=1.3, color="#334155", fill_color=COL_BG_BOX, fill_opacity=0.6).move_to([cx + 0.9, -2.1, 0])

        h_bar_l = Rectangle(width=1.1, height=0.01, color=COL_RMS, fill_color=COL_RMS, fill_opacity=0.9).move_to([cx - 0.9, -2.7, 0])
        h_bar_r = Rectangle(width=1.1, height=0.01, color=COL_HEAT, fill_color=COL_HEAT, fill_opacity=0.9).move_to([cx + 0.9, -2.7, 0])

        lbl_hl = Text("DC: 5² × 1 Ω = 25 W", font_size=11, color=COL_RMS).next_to(h_bg_l, DOWN, buff=0.08)
        lbl_hr = Text("pulse: 10² × 1 × 0.25 = 25 W", font_size=11, color=COL_HEAT).next_to(h_bg_r, DOWN, buff=0.08)
        hbars_grp = VGroup(h_bg_l, h_bg_r, lbl_hl, lbl_hr)

        self.play(FadeIn(hbars_grp), run_time=0.6)

        # Animate bars growing to exactly equal height (1.0 units) and turn emerald green
        h_bar_l_target = Rectangle(width=1.1, height=1.0, color=COL_RMS, fill_color=COL_RMS, fill_opacity=0.9).move_to([cx - 0.9, -2.2, 0])
        h_bar_r_target = Rectangle(width=1.1, height=1.0, color=COL_RMS, fill_color=COL_RMS, fill_opacity=0.9).move_to([cx + 0.9, -2.2, 0])

        self.play(
            Transform(h_bar_l, h_bar_l_target),
            Transform(h_bar_r, h_bar_r_target),
            lbl_hr.animate.set_color(COL_RMS),
            res_rect.animate.set_fill(color=COL_RMS, opacity=0.9),
            run_time=1.0
        )
        self.wait(1.2)
        self.play(FadeOut(hbars_grp), FadeOut(h_bar_l), FadeOut(h_bar_r), run_time=0.4)

        # ----------------------------------------------------------------------
        # SHOT 8 — 1:07–1:17 — Duty as an intuitive control
        # ----------------------------------------------------------------------
        cap8 = caption_top("เปิดนานขึ้น = RMS สูงขึ้น = R ร้อนขึ้น", size=20)
        self.play(Transform(cap, cap8), run_time=0.5)

        # Compact right-bottom table: D | Irms | heat at y = -1.45
        tbl_rect = RoundedRectangle(corner_radius=0.12, width=4.8, height=1.5, color="#475569", fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([ax_x, -1.45, 0])
        th = Text("D             Irms          ความร้อน (W)", font_size=12, color=COL_DUTY).move_to([ax_x, -1.0, 0])
        tr1 = Text("0.25         5.00 A            25 W", font_size=12, color=COL_RMS).move_to([ax_x, -1.3, 0])
        tr2 = Text("0.50         7.07 A            50 W", font_size=12, color=WHITE).move_to([ax_x, -1.6, 0])
        tr3 = Text("1.00        10.00 A           100 W", font_size=12, color=COL_HEAT).move_to([ax_x, -1.9, 0])
        tbl_all = VGroup(tbl_rect, th, tr1, tr2, tr3)

        self.play(FadeIn(tbl_all), run_time=0.6)
        # State A: D = 0.25 (hold 1.0s)
        self.wait(1.0)

        # State B: D = 0.50
        pw2_b = ax_wave.c2p(0.50 * ts_w, 1.8)
        pw3_b = ax_wave.c2p(0.50 * ts_w, 0)
        pulse_b = VMobject(color=COL_CURR, stroke_width=3.5).set_points_as_corners([pw0, pw1, pw2_b, pw3_b, pw4])
        brk_b = BraceBetweenPoints(pw1, pw2_b, UP, color=COL_DUTY, buff=0.08)
        lbl_b = Text("D = 0.50", font_size=12, color=COL_DUTY).next_to(brk_b, UP, buff=0.06)

        self.play(
            Transform(pulse_path, pulse_b),
            Transform(brk_dts, brk_b),
            Transform(lbl_dts, lbl_b),
            tr2.animate.set_color(COL_RMS),
            run_time=0.4
        )
        self.wait(1.0)

        # State C: D = 1.00 (pure DC 10A!)
        pw2_c = ax_wave.c2p(ts_w, 1.8)
        pw3_c = ax_wave.c2p(ts_w, 0)
        pulse_c = VMobject(color=COL_CURR, stroke_width=3.5).set_points_as_corners([pw0, pw1, pw2_c, pw3_c])
        brk_c = BraceBetweenPoints(pw1, pw2_c, UP, color=COL_DUTY, buff=0.08)
        lbl_c = Text("D = 1.00 (DC เต็มคลื่น)", font_size=12, color=COL_DUTY).next_to(brk_c, UP, buff=0.06)

        self.play(
            Transform(pulse_path, pulse_c),
            Transform(brk_dts, brk_c),
            Transform(lbl_dts, lbl_c),
            tr3.animate.set_color(COL_RMS),
            run_time=0.4
        )
        self.wait(1.0)
        self.play(FadeOut(tbl_all), run_time=0.4)

        # ----------------------------------------------------------------------
        # SHOT 9 — 1:17–1:25 — The specific misconception
        # ----------------------------------------------------------------------
        cap9 = caption_top("Iavg บอกค่าเฉลี่ยของกระแส แต่การเลือกความร้อน/เรตติ้งต้องใช้ RMS", size=19)
        self.play(Transform(cap, cap9), run_time=0.5)

        # Restore waveform to D = 0.25
        self.play(
            Transform(pulse_path, VMobject(color=COL_CURR, stroke_width=3.5).set_points_as_corners([pw0, pw1, pw2, pw3, pw4])),
            Transform(brk_dts, BraceBetweenPoints(pw1, pw2, UP, color=COL_DUTY, buff=0.08)),
            Transform(lbl_dts, Text("D Ts (D=0.25)", font_size=12, color=COL_DUTY).next_to(brk_dts, UP, buff=0.06)),
            run_time=0.4
        )

        # Red Left Card in thermal world (x = -4.0, y = -2.2)
        c_wrong = RoundedRectangle(corner_radius=0.15, width=4.4, height=1.6, color=COL_TRAP, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([cx, -2.2, 0])
        t_w_h = Text("WRONG for heat", font_size=12, color=COL_TRAP).move_to([cx, -1.6, 0])
        t_w_form = Text("Iavg = Ipk D = 2.5 A", font_size=13, color=WHITE).move_to([cx, -1.95, 0])
        t_w_calc = Text("2.5² × 1 Ω = 6.25 W (ผิด! หายไป 4 เท่า)", font_size=11, color=COL_TRAP).move_to([cx, -2.4, 0])
        wrong_grp = VGroup(c_wrong, t_w_h, t_w_form, t_w_calc)

        # Green Right Card in formula world (x = 2.8, y = -1.45)
        c_right = RoundedRectangle(corner_radius=0.15, width=4.4, height=1.6, color=COL_RMS, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([ax_x, -1.45, 0])
        t_r_h = Text("RIGHT for heat", font_size=12, color=COL_RMS).move_to([ax_x, -0.85, 0])
        t_r_form = Text("Irms = Ipk sqrt(D) = 5 A", font_size=13, color=WHITE).move_to([ax_x, -1.2, 0])
        t_r_calc = Text("5² × 1 Ω = 25 W (ถูกต้อง! เท่าพัลส์จริง)", font_size=11, color=COL_RMS).move_to([ax_x, -1.65, 0])
        right_grp = VGroup(c_right, t_r_h, t_r_form, t_r_calc)

        self.play(FadeIn(wrong_grp), FadeIn(right_grp), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(wrong_grp), FadeOut(right_grp), run_time=0.5)

        # ----------------------------------------------------------------------
        # SHOT 10 — 1:25–1:30 — Retrieval ending
        # ----------------------------------------------------------------------
        cap10 = caption_top("สรุปหลักการสำคัญ และคำถามทบทวนความเข้าใจ", size=20)
        self.play(
            Transform(cap, cap10),
            circuit_hero.animate.set_opacity(0.25),
            ttl.animate.set_opacity(0.25),
            FadeOut(axes_hero), FadeOut(pulse_path), FadeOut(brk_dts), FadeOut(lbl_dts),
            FadeOut(lbl_d_def), FadeOut(lbl_ipk_tag), FadeOut(lbl_pr_formula),
            FadeOut(deriv_box), FadeOut(eq_st1), FadeOut(switch_rail),
            run_time=0.6
        )

        # Centered recap card rising 0.35 units
        recap_box = RoundedRectangle(corner_radius=0.18, width=9.6, height=2.0, color=COL_RMS, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([0, 0.65, 0]).shift(DOWN * 0.35)
        rc1 = Text("1. RMS = DC ที่ร้อนเท่ากัน", font_size=16, color=WHITE).move_to([0, 1.15, 0]).shift(DOWN * 0.35)
        rc2 = Text("2. พัลส์สูง Ipk นาน D Ts", font_size=16, color=COL_CURR).move_to([0, 0.65, 0]).shift(DOWN * 0.35)
        rc3 = Text("3. Irms = Ipk sqrt(D)", font_size=18, color=COL_RMS).move_to([0, 0.15, 0]).shift(DOWN * 0.35)
        recap_card = VGroup(recap_box, rc1, rc2, rc3)

        self.play(recap_card.animate.shift(UP * 0.35), run_time=0.8)
        self.wait(0.8)

        # Retrieval prompt below it
        ret_box = RoundedRectangle(corner_radius=0.15, width=9.6, height=1.4, color=COL_DUTY, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([0, -1.4, 0])
        ret_q = Text("ลองตอบ: Ipk = 8 A, D = 0.25 -> Irms = ?", font_size=17, color=COL_DUTY).move_to([0, -1.4, 0])
        ret_card = VGroup(ret_box, ret_q)

        self.play(FadeIn(ret_card), run_time=0.7)
        # Hold quietly for 1.5s as required. Answer (4 A) is NOT revealed in the video.
        self.wait(1.5)

        self.fade_out_all(run_time=0.8)
