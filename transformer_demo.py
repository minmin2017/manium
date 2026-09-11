"""
Transformer teaching video — 4 scenes refined with Motion Doctrine:
1. TransformerPrimary: Electrical power at primary coil (V1, I1 -> P1 = V1 * I1)
2. TransformerFlux: Magnetic flux through the shared iron core (Conserved Link)
3. TransformerVoltageRatio: Voltage step-up/down derivation (V2/V1 = N2/N1)
4. TransformerCurrentInverse: Current inverse ratio via power conservation (I2/I1 = N1/N2)
"""

import numpy as np
import os
from manim import *
from mlib import *

# Cross-platform font: Loma on Linux container (GitHub Actions), Leelawadee UI on Windows
Text.set_default(font=os.environ.get("MANIM_THAI_FONT", "Leelawadee UI"))

# Focal stage coordinates for seamless camera vector continuity (Vector Law)
STAGE_FULL = np.array([-3.3, -0.35, 0])
STAGE_PRIMARY = np.array([-1.6, -0.35, 0])    # Focus on primary limb (scale 1.22)
STAGE_SECONDARY = np.array([-4.8, -0.35, 0])  # Focus on secondary limb (scale 1.22)
SCALE_ZOOM = 1.22


def make_transformer_rig(n1=5, n2=10):
    """
    Builds the transformer mobjects centered at ORIGIN so the stage assembly
    can be placed, scaled, and translated seamlessly across scene seams.
    """
    w_core, h_core = 3.6, 4.0
    t_core = 0.75
    w_leg = t_core

    left_x = -(w_core / 2.0 - t_core / 2.0)
    right_x = (w_core / 2.0 - t_core / 2.0)
    top_y = (h_core / 2.0 - t_core / 2.0)
    bot_y = -(h_core / 2.0 - t_core / 2.0)

    left_limb = Rectangle(width=t_core, height=h_core, color=METAL, stroke_width=2.5)
    left_limb.set_fill(METAL).set_opacity(0.35).move_to([left_x, 0, 0])

    right_limb = Rectangle(width=t_core, height=h_core, color=METAL, stroke_width=2.5)
    right_limb.set_fill(METAL).set_opacity(0.35).move_to([right_x, 0, 0])

    top_limb = Rectangle(width=w_core, height=t_core, color=METAL, stroke_width=2.5)
    top_limb.set_fill(METAL).set_opacity(0.35).move_to([0, top_y, 0])

    bot_limb = Rectangle(width=w_core, height=t_core, color=METAL, stroke_width=2.5)
    bot_limb.set_fill(METAL).set_opacity(0.35).move_to([0, bot_y, 0])

    core_group = VGroup(left_limb, right_limb, top_limb, bot_limb)

    def build_coil(leg_x, n_turns, color, dark_color, y_span=2.4):
        backs = VGroup()
        fronts = VGroup()
        w_wire = w_leg + 0.24
        h_turn = y_span / float(n_turns)
        y_bot = -y_span / 2.0

        for i in range(n_turns):
            y_i = y_bot + i * h_turn
            b = Line(
                [leg_x + w_wire / 2.0, y_i + h_turn * 0.25, 0],
                [leg_x - w_wire / 2.0, y_i + h_turn * 0.75, 0],
                color=dark_color, stroke_width=3
            )
            f = Line(
                [leg_x - w_wire / 2.0, y_i + h_turn * 0.75, 0],
                [leg_x + w_wire / 2.0, y_i + h_turn * 1.25, 0],
                color=color, stroke_width=5
            )
            backs.add(b)
            fronts.add(f)

        sign = -1 if leg_x < 0 else 1
        top_lead = Line(
            [leg_x + w_wire / 2.0 * sign, y_bot + n_turns * h_turn + h_turn * 0.25, 0],
            [leg_x + (w_wire / 2.0 + 0.5) * sign, y_bot + n_turns * h_turn + h_turn * 0.25, 0],
            color=color, stroke_width=4
        )
        bot_lead = Line(
            [leg_x - w_wire / 2.0 * sign, y_bot + h_turn * 0.75, 0],
            [leg_x + (w_wire / 2.0 + 0.5) * sign, y_bot + h_turn * 0.75, 0],
            color=color, stroke_width=4
        )
        fronts.add(top_lead, bot_lead)

        # Wire centerline path for flowing current particles (internal invisible track)
        pts = [[leg_x + (w_wire / 2.0 + 0.45) * sign, y_bot + n_turns * h_turn + h_turn * 0.25, 0]]
        for i in range(n_turns - 1, -1, -1):
            y_i = y_bot + i * h_turn
            pts.append([leg_x - w_wire / 2.0, y_i + h_turn * 0.75, 0])
            pts.append([leg_x + w_wire / 2.0, y_i + h_turn * 0.25, 0])
        pts.append([leg_x + (w_wire / 2.0 + 0.45) * sign, y_bot + h_turn * 0.75, 0])
        path = VMobject().set_points_as_corners(pts)
        path.set_opacity(0)

        return backs, fronts, path

    p_backs, p_fronts, p_path = build_coil(left_x, n1, CURRENT, "#B78103", y_span=2.2)
    s_backs, s_fronts, s_path = build_coil(right_x, n2, OK, "#00838F", y_span=2.5)

    loop_w = w_core - t_core
    loop_h = h_core - t_core
    flux_loop = RoundedRectangle(
        corner_radius=0.4,
        width=loop_w,
        height=loop_h,
        color=FIELD,
        stroke_width=3
    ).move_to([0, 0, 0])

    arrow_l = Arrow([left_x, -0.45, 0], [left_x, 0.45, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    arrow_t = Arrow([-0.45, top_y, 0], [0.45, top_y, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    arrow_r = Arrow([right_x, 0.45, 0], [right_x, -0.45, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    arrow_b = Arrow([0.45, bot_y, 0], [-0.45, bot_y, 0], color=FIELD, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25)
    flux_arrows = VGroup(arrow_l, arrow_t, arrow_r, arrow_b)

    # All components including wire tracking paths bundled into one synchronized group
    rig = VGroup(p_backs, s_backs, core_group, flux_loop, flux_arrows, p_fronts, s_fronts, p_path, s_path)

    return {
        "group": rig,
        "p_backs": p_backs,
        "s_backs": s_backs,
        "core": core_group,
        "p_fronts": p_fronts,
        "s_fronts": s_fronts,
        "primary": VGroup(p_backs, p_fronts),
        "secondary": VGroup(s_backs, s_fronts),
        "flux_loop": flux_loop,
        "flux_arrows": flux_arrows,
        "p_path": p_path,
        "s_path": s_path,
        "left_x": left_x,
        "right_x": right_x
    }


class TransformerPrimary(SafeScene):
    """Clip 1: Electrical power at primary coil — establishes transformer and zooms into primary"""

    def construct(self):
        self.add(title("หม้อแปลงไฟฟ้า — ตอนที่ 1: กำลังไฟฟ้าขาเข้า (Primary)", size=27))
        cap = caption_top("ขดลวดปฐมภูมิ (N1 = 5 รอบ): รับแรงดัน V1 และจ่ายกระแส I1 เข้าสู่วงจร", size=21)
        self.add(cap)

        rig_data = make_transformer_rig()
        stage = rig_data["group"]
        rig_data["flux_loop"].set_opacity(0)
        rig_data["flux_arrows"].set_opacity(0)
        rig_data["s_backs"].set_opacity(0.2)
        rig_data["s_fronts"].set_opacity(0.2)

        # 1. Establish wide view
        stage.scale(1.0).move_to(STAGE_FULL)
        self.play(FadeIn(stage), run_time=0.8)

        # 2. Camera with intent: zoom & pan into Primary coil (Vector Law exit staging)
        self.play(stage.animate.scale(SCALE_ZOOM).move_to(STAGE_PRIMARY), run_time=1.0)

        # Visual labels on primary
        v1_tag = Text("V1 = 230 V", font_size=20, color=CURRENT).move_to([-4.6, 0.8, 0])
        i1_tag = Text("I1 = 10 A", font_size=20, color=WARN).move_to([-4.6, -1.2, 0])
        n1_tag = Text("N1 = 5 รอบ", font_size=21, color=CURRENT).move_to([-3.2, -2.8, 0])
        self.play(FadeIn(v1_tag), FadeIn(i1_tag), FadeIn(n1_tag), run_time=0.6)

        # Continuous current motion (No Idle Wobble)
        i_tracker = ValueTracker(0.0)
        p_path = rig_data["p_path"]
        cur_dots = always_redraw(lambda: VGroup(*[
            Dot(p_path.point_from_proportion((i_tracker.get_value() + k * 0.25) % 1.0), radius=0.07, color=WARN)
            for k in range(4)
        ]))
        self.add(cur_dots)

        # Right reasoning panel
        p_x = 3.6
        box_title = Text("1. กำลังไฟฟ้าขาเข้า (Input Power)", font_size=22, color=CURRENT).move_to([p_x, 2.0, 0])
        step1 = Text("• ขดลวดปฐมภูมิต่อกับแหล่งจ่ายไฟ AC", font_size=19, color=GRAYTXT).move_to([p_x, 1.45, 0])
        step2 = Text("• แรงดันที่ป้อน: V1 = 230 V", font_size=19, color=CURRENT).move_to([p_x, 1.05, 0])
        step3 = Text("• กระแสที่ไหลเข้า: I1 = 10 A", font_size=19, color=WARN).move_to([p_x, 0.65, 0])

        eq_label = Text("สูตรกำลังไฟฟ้า:", font_size=20, color=WHITE).move_to([p_x, 0.05, 0])
        eq_math = Text("P1 = V1 × I1", font_size=25, color=WHITE).move_to([p_x, -0.45, 0])
        eq_sub = Text("P1 = 230 V × 10 A", font_size=22, color=YELLOW).move_to([p_x, -0.95, 0])
        eq_res = Text("P1 = 2300 W", font_size=27, color=OK).move_to([p_x, -1.5, 0])
        res_box = SurroundingRectangle(eq_res, color=OK, buff=0.15)
        note_foot = fit_width(Text("กำลังงาน 2300 W นี้ จะถูกส่งผ่านแกนเหล็กไปยังขดลวดทุติยภูมิ", font_size=17, color=GRAYTXT), 6.5).move_to([p_x, -2.15, 0])

        self.play(FadeIn(box_title), FadeIn(step1), FadeIn(step2), FadeIn(step3),
                  i_tracker.animate.increment_value(0.5), run_time=1.0)
        self.play(FadeIn(eq_label), FadeIn(eq_math), FadeIn(eq_sub),
                  i_tracker.animate.increment_value(0.5), run_time=0.9)

        # Stillness before climax: dramatic pause (0.5s) before revealing the number
        self.wait(0.5)

        self.play(FadeIn(eq_res), i_tracker.animate.increment_value(0.3), run_time=0.5)
        self.play(Indicate(eq_res, color=OK, scale_factor=1.0), run_time=0.5)
        self.play(Create(res_box), FadeIn(note_foot), i_tracker.animate.increment_value(0.4), run_time=0.7)

        # Scene exits mid-motion at STAGE_PRIMARY (Seam Carrier ready for Scene 2)
        self.play(i_tracker.animate.increment_value(0.4), run_time=0.6)
        cur_dots.clear_updaters()


class TransformerFlux(SafeScene):
    """Clip 2: Magnetic flux — OPENS at STAGE_PRIMARY (matching Clip 1 exit) then travels to STAGE_SECONDARY"""

    def construct(self):
        self.add(title("หม้อแปลงไฟฟ้า — ตอนที่ 2: ฟลักซ์แม่เหล็กในแกนเหล็ก (Flux Φ)", size=27))
        cap = caption_top("กระแสสลับสร้างฟลักซ์แม่เหล็ก Φ ไหลวนครบวงจรในแกนเหล็กปิด", size=21)
        self.add(cap)

        rig_data = make_transformer_rig()
        stage = rig_data["group"]
        rig_data["s_backs"].set_opacity(0.3)
        rig_data["s_fronts"].set_opacity(0.3)
        rig_data["flux_loop"].set_opacity(0)
        rig_data["flux_arrows"].set_opacity(0)

        # Vector Law: Exactly match ending framing of Scene 1 (STAGE_PRIMARY, SCALE_ZOOM)
        stage.scale(SCALE_ZOOM).move_to(STAGE_PRIMARY)
        self.add(stage)

        # Carrier: Incoming current particles arrive at core boundary
        p_path = rig_data["p_path"]
        cur_dots = VGroup(*[
            Dot(p_path.point_from_proportion(0.7 + k * 0.08), radius=0.07, color=WARN)
            for k in range(3)
        ])
        self.add(cur_dots)

        # Causal motion: Current particles arrive at core -> ignites flux loop ON THE SAME BEAT
        flux_loop = rig_data["flux_loop"]
        flux_arrows = rig_data["flux_arrows"]
        self.play(
            FadeOut(cur_dots),
            flux_loop.animate.set_opacity(1.0),
            flux_arrows.animate.set_opacity(1.0),
            run_time=0.6
        )

        # Carrier travels: Camera travels along top limb from Primary to Secondary (STAGE_SECONDARY)
        flux_tag = VGroup(
            Text("ฟลักซ์แม่เหล็ก Φ", font_size=17, color=FIELD),
            Text("(แกนร่วม Conserved)", font_size=14, color=FIELD)
        ).arrange(DOWN, buff=0.1).move_to([stage.get_center()[0], stage.get_center()[1], 0])

        self.play(
            stage.animate.move_to(STAGE_SECONDARY),
            flux_tag.animate.shift(STAGE_SECONDARY - STAGE_PRIMARY),
            run_time=1.4
        )

        # Right reasoning panel
        p_x = 3.6
        box_title = Text("2. ทางเดินฟลักซ์แม่เหล็ก (Conserved Link)", font_size=22, color=FIELD).move_to([p_x, 2.0, 0])
        b1 = Text("• แกนเหล็กนำสนามแม่เหล็กได้ดีกว่าอากาศนับพันเท่า", font_size=18, color=GRAYTXT).move_to([p_x, 1.45, 0])
        b2 = Text("• ฟลักซ์แม่เหล็ก Φ ถูกขังให้ไหลวนในแกนเหล็กปิด", font_size=18, color=WHITE).move_to([p_x, 1.05, 0])
        b3 = Text("• ขดลวดทั้ง 2 สัมผัสฟลักซ์แม่เหล็กชุดเดียวกัน 100%", font_size=18, color=OK).move_to([p_x, 0.65, 0])

        faraday_title = Text("กฎการเหนี่ยวนำของฟาราเดย์ (Faraday's Law):", font_size=19, color=WARN).move_to([p_x, 0.05, 0])
        f_eq = Text("แรงดันเหนี่ยวนำต่อ 1 รอบ = ΔΦ / Δt", font_size=22, color=YELLOW).move_to([p_x, -0.45, 0])
        f_box = SurroundingRectangle(f_eq, color=YELLOW, buff=0.12)
        f_sub = Text("ทุกๆ 1 รอบของขดลวด ไม่ว่าจะอยู่ฝั่งซ้ายหรือขวา", font_size=18, color=GRAYTXT).move_to([p_x, -1.0, 0])
        f_sub2 = Text("จะได้รับแรงดันเหนี่ยวนำเท่ากันเป๊ะ!", font_size=19, color=OK).move_to([p_x, -1.35, 0])
        takeaway = fit_width(Text("นี่คือจุดเชื่อมต่อสำคัญที่ทำให้เราคำนวณอัตราส่วนแรงดันได้", font_size=17, color=GRAYTXT), 6.5).move_to([p_x, -2.0, 0])

        self.play(FadeIn(box_title), FadeIn(b1), FadeIn(b2), FadeIn(b3), run_time=0.9)

        # Stillness before climax (0.4s) before Faraday formula locks in
        self.wait(0.4)

        self.play(FadeIn(faraday_title), FadeIn(f_eq), run_time=0.7)
        self.play(Indicate(f_eq, color=YELLOW, scale_factor=1.0), run_time=0.6)
        self.play(Create(f_box), FadeIn(f_sub), FadeIn(f_sub2), FadeIn(takeaway), run_time=0.9)

        # Scene exits mid-motion at STAGE_SECONDARY with flux entering secondary coil
        self.wait(0.8)


class TransformerVoltageRatio(SafeScene):
    """Clip 3: Voltage ratio — OPENS at STAGE_SECONDARY (matching Clip 2 exit), then pulls back to STAGE_FULL"""

    def construct(self):
        self.add(title("หม้อแปลงไฟฟ้า — ตอนที่ 3: อัตราส่วนแรงดัน (Voltage Ratio)", size=27))
        cap = caption_top("แต่ละรอบอนุกรมกัน: ขดลวดที่มีรอบมากกว่า ย่อมเหนี่ยวนำแรงดันได้มากกว่า", size=21)
        self.add(cap)

        rig_data = make_transformer_rig()
        stage = rig_data["group"]

        # Vector Law: Exactly match ending framing of Scene 2 (STAGE_SECONDARY, SCALE_ZOOM)
        stage.scale(SCALE_ZOOM).move_to(STAGE_SECONDARY)
        self.add(stage)

        # Causal motion: Flux arrives at secondary -> secondary turns light up with induced EMF
        rig_data["s_fronts"].set_color(YELLOW)
        self.play(rig_data["s_fronts"].animate.set_color(OK), run_time=0.6)

        # Visual pull-back to STAGE_FULL to compare primary vs secondary side-by-side
        self.play(stage.animate.scale(1.0 / SCALE_ZOOM).move_to(STAGE_FULL), run_time=1.2)

        lx, rx = STAGE_FULL[0] - 1.425, STAGE_FULL[0] + 1.425
        n1_lbl = Text("N1 = 5 รอบ", font_size=20, color=CURRENT).move_to([lx, -2.7, 0])
        n2_lbl = Text("N2 = 10 รอบ (2 เท่า)", font_size=20, color=OK).move_to([rx, -2.7, 0])
        v1_lbl = Text("V1 = 230 V", font_size=20, color=CURRENT).move_to([lx - 1.4, 0.6, 0])
        v2_lbl = Text("V2 = ?", font_size=22, color=OK).move_to([rx + 1.35, 0.6, 0])
        self.play(FadeIn(n1_lbl), FadeIn(n2_lbl), FadeIn(v1_lbl), FadeIn(v2_lbl), run_time=0.8)

        # Right reasoning panel
        p_x = 3.6
        p_title = Text("3. อนุมานสมการแรงดัน (Voltage Ratio)", font_size=22, color=OK).move_to([p_x, 2.05, 0])
        r1 = Text("แรงดันแต่ละฝั่งเกิดจากการรวมแรงดันทีละรอบ:", font_size=18, color=GRAYTXT).move_to([p_x, 1.55, 0])
        r2 = Text("V1 = N1 × (ΔΦ/Δt)   ⟹   ΔΦ/Δt = V1 / N1", font_size=20, color=CURRENT).move_to([p_x, 1.1, 0])
        r3 = Text("V2 = N2 × (ΔΦ/Δt)   ⟹   ΔΦ/Δt = V2 / N2", font_size=20, color=OK).move_to([p_x, 0.65, 0])

        link_txt = Text("เนื่องจาก ΔΦ/Δt มีค่าเท่ากันทั้งสองฝั่ง:", font_size=18, color=WHITE).move_to([p_x, 0.15, 0])
        ratio_box = Text("V2 / V1 = N2 / N1", font_size=26, color=YELLOW).move_to([p_x, -0.35, 0])
        box_rect = SurroundingRectangle(ratio_box, color=YELLOW, buff=0.12)

        calc_txt = Text("แทนค่าจำนวนรอบจริง (Step-Up 2 เท่า):", font_size=18, color=GRAYTXT).move_to([p_x, -0.9, 0])
        calc_eq = Text("V2 = (10 / 5) × 230 V", font_size=21, color=WHITE).move_to([p_x, -1.3, 0])
        res_v2 = Text("V2 = 460 V", font_size=26, color=OK).move_to([p_x, -1.75, 0])
        res_v2_box = SurroundingRectangle(res_v2, color=OK, buff=0.12)

        self.play(FadeIn(p_title), FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.9)
        self.play(FadeIn(link_txt), FadeIn(ratio_box), run_time=0.7)
        self.play(Indicate(ratio_box, color=YELLOW, scale_factor=1.0), run_time=0.5)
        self.play(Create(box_rect), FadeIn(calc_txt), FadeIn(calc_eq), run_time=0.7)

        # Stillness before climax (0.5s pause) before V2 numeric result
        self.wait(0.5)

        self.play(FadeIn(res_v2), run_time=0.5)
        self.play(Indicate(res_v2, color=OK, scale_factor=1.0), run_time=0.5)
        self.play(Create(res_v2_box), run_time=0.5)

        v2_real = Text("V2 = 460 V", font_size=22, color=OK).move_to([rx + 1.45, 0.6, 0])
        self.play(Transform(v2_lbl, v2_real), run_time=0.6)

        # Scene exits mid-motion at STAGE_FULL (Ready for Scene 4)
        self.wait(0.8)


class TransformerCurrentInverse(SafeScene):
    """Clip 4: Current ratio — OPENS at STAGE_FULL (matching Clip 3 exit), active power flow"""

    def construct(self):
        self.add(title("หม้อแปลงไฟฟ้า — ตอนที่ 4: กฎอนุรักษ์พลังงานและกระแส (Current)", size=26))
        cap = caption_top("หม้อแปลงในอุดมคติ กำลังไฟฟ้าไม่สูญหาย: P_in = P_out (V เพิ่ม -> I ต้องลด)", size=21)
        self.add(cap)

        rig_data = make_transformer_rig()
        stage = rig_data["group"]

        # Vector Law: Exactly match ending framing of Scene 3 (STAGE_FULL, scale 1.0)
        stage.scale(1.0).move_to(STAGE_FULL)
        self.add(stage)

        lx, rx = STAGE_FULL[0] - 1.425, STAGE_FULL[0] + 1.425
        p1_tag = Text("P1 = 2300 W", font_size=19, color=CURRENT).move_to([lx, 2.0, 0])
        i1_tag = Text("I1 = 10 A", font_size=19, color=WARN).move_to([lx - 1.45, -1.0, 0])
        p2_tag = Text("P2 = 2300 W", font_size=19, color=OK).move_to([rx, 2.0, 0])
        i2_tag = Text("I2 = ?", font_size=21, color=WARN).move_to([rx + 1.45, -1.0, 0])
        self.play(FadeIn(p1_tag), FadeIn(i1_tag), FadeIn(p2_tag), FadeIn(i2_tag), run_time=0.7)

        # Causal Motion: Both coils have live current flow (No Idle Wobble)
        t_tracker = ValueTracker(0.0)
        p_path = rig_data["p_path"]
        s_path = rig_data["s_path"]

        live_dots = always_redraw(lambda: VGroup(
            # Primary current dots (10A, faster/denser)
            *[Dot(p_path.point_from_proportion((t_tracker.get_value() * 1.5 + k * 0.25) % 1.0), radius=0.06, color=WARN) for k in range(4)],
            # Secondary current dots (5A, half speed)
            *[Dot(s_path.point_from_proportion((t_tracker.get_value() * 0.75 + k * 0.5) % 1.0), radius=0.06, color=OK) for k in range(2)]
        ))
        self.add(live_dots)

        # Right reasoning panel
        p_x = 3.6
        p_title = Text("4. กฎอนุรักษ์พลังงาน (P1 = P2)", font_size=22, color=WARN).move_to([p_x, 2.05, 0])
        c1 = Text("กำลังไฟฟ้าขาเข้า ต้องเท่ากับกำลังไฟฟ้าขาออก:", font_size=18, color=GRAYTXT).move_to([p_x, 1.6, 0])
        c2 = Text("V1 × I1 = V2 × I2", font_size=23, color=WHITE).move_to([p_x, 1.15, 0])
        c3 = Text("230 V × 10 A = 460 V × I2", font_size=20, color=YELLOW).move_to([p_x, 0.7, 0])
        c4 = Text("2300 W = 460 V × I2  ⟹  I2 = 5 A", font_size=22, color=WARN).move_to([p_x, 0.25, 0])
        c4_box = SurroundingRectangle(c4, color=WARN, buff=0.12)

        self.play(FadeIn(p_title), FadeIn(c1), FadeIn(c2), FadeIn(c3),
                  t_tracker.animate.increment_value(0.5), run_time=1.0)

        # Stillness before climax (0.5s pause) before solving I2
        self.wait(0.5)

        self.play(FadeIn(c4), t_tracker.animate.increment_value(0.3), run_time=0.5)
        self.play(Indicate(c4, color=WARN, scale_factor=1.0), run_time=0.5)
        self.play(Create(c4_box), run_time=0.5)

        i2_real = Text("I2 = 5 A", font_size=21, color=WARN).move_to([rx + 1.45, 0.2, 0])
        self.play(Transform(i2_tag, i2_real), t_tracker.animate.increment_value(0.3), run_time=0.6)

        sum_title = Text("สรุปอัตราส่วนหม้อแปลง (Master Formula):", font_size=19, color=WHITE).move_to([p_x, -0.4, 0])
        master_eq = Text("V2 / V1 = N2 / N1 = I1 / I2", font_size=25, color=OK).move_to([p_x, -0.9, 0])
        master_box = SurroundingRectangle(master_eq, color=OK, buff=0.15)

        note_v = Text("• แรงดัน V แปรผันตรงกับจำนวนรอบ N", font_size=18, color=CURRENT).move_to([p_x, -1.5, 0])
        note_i = Text("• กระแส I แปรผกผันกับจำนวนรอบ N", font_size=18, color=WARN).move_to([p_x, -1.88, 0])
        note_final = fit_width(Text("แรงดันเพิ่ม 2 เท่า ⟹ กระแสลดลงครึ่งหนึ่ง เพื่อให้ P คงที่", font_size=17, color=GRAYTXT), 6.2).move_to([p_x, -2.3, 0])

        self.play(FadeIn(sum_title), FadeIn(master_eq), t_tracker.animate.increment_value(0.4), run_time=0.8)
        self.play(Indicate(master_eq, color=OK, scale_factor=1.0), run_time=0.5)
        self.play(Create(master_box), FadeIn(note_v), FadeIn(note_i), FadeIn(note_final),
                  t_tracker.animate.increment_value(0.4), run_time=0.8)

        self.wait(1.5)
        live_dots.clear_updaters()
