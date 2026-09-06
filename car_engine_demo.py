"""
car_engine_demo.py — เครื่องยนต์รถทำงานยังไง (How a Car Engine Works)

Production Manim Community teaching video following Min's house style,
SafeScene layout constraints, exact kinematic slider-crank equations,
and pedagogy storyboard requirements.
"""

from mlib import *
import numpy as np

# ── Colors (Strictly consistent across all segments and summary) ──────────────
C_INTAKE    = "#4FC3F7"   # อากาศ+น้ำมัน (ฟ้าสดใส)
C_COMPRESS  = "#FFB74D"   # การอัด/ความดันและความร้อนเพิ่มขึ้น (ส้มอมเหลือง)
C_POWER     = "#FF7043"   # ระเบิด/ประกายไฟ/จังหวะส่งกำลัง (ส้มแดงเพลิง)
C_EXHAUST   = "#90A4AE"   # ไอเสีย/ก๊าซที่เผาไหม้แล้ว (เทา)

C_BLOCK     = "#263238"   # เสื้อสูบ / ห้องเพลาข้อเหวี่ยง (เทาเข้มอมฟ้า)
C_CYL_WALL  = "#78909C"   # ผนังกระบอกสูบ
C_PISTON    = "#546E7A"   # ลูกสูบ
C_ROD       = "#ECEFF1"   # ก้านสูบ (โลหะสีสว่าง)
C_CRANK     = "#455A64"   # จานเพลาข้อเหวี่ยง
C_VALVE     = "#B0BEC5"   # วาล์ว

C_BLUE_MC   = ManimColor(C_INTAKE)
C_ORANGE_MC = ManimColor(C_COMPRESS)



def slider_crank(theta, r=0.42, L=1.26, crank_center=ORIGIN):
    """
    Exact kinematics of the slider-crank mechanism:
    piston_x(theta) = r*cos(theta) + sqrt(L**2 - (r*sin(theta))**2)
    theta: 0 = Top Dead Center (TDC), pi = Bottom Dead Center (BDC).
    Measured along the vertical axis from crankshaft center.
    Connecting rod length is strictly L at all angles theta.
    """
    piston_dist = r * np.cos(theta) + np.sqrt(L**2 - (r * np.sin(theta))**2)
    p_wrist = crank_center + np.array([0.0, piston_dist, 0.0])
    p_crank = crank_center + np.array([r * np.sin(theta), r * np.cos(theta), 0.0])
    return p_wrist, p_crank


def build_engine(center=ORIGIN, scale=1.0):
    """
    Build a 2D cutaway single-cylinder engine model.
    Returns a dictionary of all components and helper state.
    """
    r = 0.42 * scale
    L = 1.26 * scale
    crank_center = center + np.array([0.0, -1.75 * scale, 0.0])
    y_head = center[1] + 1.05 * scale
    bore_half = 0.67 * scale
    wall_thick = 0.10 * scale

    # 1. Crankcase housing & cylinder walls
    left_wall = Rectangle(
        width=wall_thick, height=2.35 * scale,
        color=C_CYL_WALL, fill_color=C_BLOCK, fill_opacity=0.75, stroke_width=2
    ).move_to(center + np.array([-bore_half - wall_thick / 2, -0.125 * scale, 0]))

    right_wall = Rectangle(
        width=wall_thick, height=2.35 * scale,
        color=C_CYL_WALL, fill_color=C_BLOCK, fill_opacity=0.75, stroke_width=2
    ).move_to(center + np.array([bore_half + wall_thick / 2, -0.125 * scale, 0]))

    # Crankcase outer ring
    crankcase = Circle(
        radius=0.90 * scale, color=C_CYL_WALL, fill_color=C_BLOCK,
        fill_opacity=0.45, stroke_width=2
    ).move_to(crank_center)

    # 2. Cylinder head and intake/exhaust ducts
    head_left = Line(
        center + np.array([-bore_half - wall_thick, y_head, 0]),
        center + np.array([-0.50 * scale, y_head, 0]),
        color=C_CYL_WALL, stroke_width=4
    )
    head_mid = Line(
        center + np.array([-0.22 * scale, y_head, 0]),
        center + np.array([0.22 * scale, y_head, 0]),
        color=C_CYL_WALL, stroke_width=4
    )
    head_right = Line(
        center + np.array([0.50 * scale, y_head, 0]),
        center + np.array([bore_half + wall_thick, y_head, 0]),
        color=C_CYL_WALL, stroke_width=4
    )

    # Intake duct (angled tube entering from top-left)
    in_duct = VMobject(color=C_CYL_WALL, stroke_width=2.5)
    in_duct.set_points_as_corners([
        center + np.array([-1.25 * scale, y_head + 0.45 * scale, 0]),
        center + np.array([-0.50 * scale, y_head + 0.15 * scale, 0]),
        center + np.array([-0.50 * scale, y_head, 0])
    ])
    in_duct_lower = VMobject(color=C_CYL_WALL, stroke_width=2.5)
    in_duct_lower.set_points_as_corners([
        center + np.array([-1.20 * scale, y_head + 0.20 * scale, 0]),
        center + np.array([-0.22 * scale, y_head + 0.08 * scale, 0]),
        center + np.array([-0.22 * scale, y_head, 0])
    ])

    # Exhaust duct (angled tube exiting to top-right)
    ex_duct = VMobject(color=C_CYL_WALL, stroke_width=2.5)
    ex_duct.set_points_as_corners([
        center + np.array([0.50 * scale, y_head, 0]),
        center + np.array([0.50 * scale, y_head + 0.15 * scale, 0]),
        center + np.array([1.25 * scale, y_head + 0.45 * scale, 0])
    ])
    ex_duct_lower = VMobject(color=C_CYL_WALL, stroke_width=2.5)
    ex_duct_lower.set_points_as_corners([
        center + np.array([0.22 * scale, y_head, 0]),
        center + np.array([0.22 * scale, y_head + 0.08 * scale, 0]),
        center + np.array([1.20 * scale, y_head + 0.20 * scale, 0])
    ])

    # 3. Spark plug (top center)
    sp_body = Rectangle(
        width=0.18 * scale, height=0.22 * scale,
        color=METAL, fill_color=C_BLOCK, fill_opacity=1, stroke_width=2
    ).move_to(center + np.array([0, y_head + 0.11 * scale, 0]))
    sp_insulator = Rectangle(
        width=0.13 * scale, height=0.24 * scale,
        color=WHITE, fill_color="#ECEFF1", fill_opacity=1, stroke_width=1.5
    ).move_to(center + np.array([0, y_head + 0.32 * scale, 0]))
    sp_terminal = Rectangle(
        width=0.08 * scale, height=0.08 * scale,
        color=METAL, fill_color=METAL, fill_opacity=1, stroke_width=1
    ).move_to(center + np.array([0, y_head + 0.47 * scale, 0]))
    sp_electrode = Line(
        center + np.array([0, y_head, 0]),
        center + np.array([0, y_head - 0.10 * scale, 0]),
        color=WHITE, stroke_width=3 * scale
    )
    spark_plug = VGroup(sp_body, sp_insulator, sp_terminal, sp_electrode)

    # 4. Valves (hinged flaps at intake and exhaust ports)
    hinge_in = center + np.array([-0.50 * scale, y_head, 0])
    valve_in = Line(
        hinge_in, hinge_in + np.array([0.28 * scale, 0, 0]),
        color=C_VALVE, stroke_width=5 * scale
    )

    hinge_ex = center + np.array([0.50 * scale, y_head, 0])
    valve_ex = Line(
        hinge_ex, hinge_ex + np.array([-0.28 * scale, 0, 0]),
        color=C_VALVE, stroke_width=5 * scale
    )

    # 5. Crankshaft disc & counterweight
    crank_disc = Circle(
        radius=0.65 * scale, color=C_CYL_WALL,
        fill_color="#1E272C", fill_opacity=0.9, stroke_width=2
    ).move_to(crank_center)

    crank_hub = Dot(crank_center, radius=0.10 * scale, color=METAL)

    # Initial positions at theta = 0 (TDC)
    pw0, pc0 = slider_crank(0.0, r, L, crank_center)

    crank_arm = Line(crank_center, pc0, color=C_ROD, stroke_width=4 * scale)
    counter_arm = Line(
        crank_center,
        crank_center - 0.65 * (pc0 - crank_center),
        color=C_PISTON, stroke_width=10 * scale
    )
    crank_pin = Dot(pc0, radius=0.08 * scale, color=WHITE)

    # 6. Connecting rod
    rod = Line(pc0, pw0, color=C_ROD, stroke_width=7 * scale)
    rod_pin_bottom = Dot(pc0, radius=0.10 * scale, color=C_ROD)
    rod_pin_top = Dot(pw0, radius=0.09 * scale, color=C_ROD)

    # 7. Piston block
    piston_h = 0.55 * scale
    piston_w = 1.30 * scale
    piston_body = Rectangle(
        width=piston_w, height=piston_h,
        color=C_CYL_WALL, fill_color=C_PISTON, fill_opacity=0.95, stroke_width=2
    ).move_to(pw0)
    piston_ring1 = Line(
        pw0 + np.array([-piston_w / 2 + 0.05 * scale, 0.15 * scale, 0]),
        pw0 + np.array([piston_w / 2 - 0.05 * scale, 0.15 * scale, 0]),
        color="#37474F", stroke_width=2 * scale
    )
    piston_ring2 = Line(
        pw0 + np.array([-piston_w / 2 + 0.05 * scale, 0.05 * scale, 0]),
        pw0 + np.array([piston_w / 2 - 0.05 * scale, 0.05 * scale, 0]),
        color="#37474F", stroke_width=2 * scale
    )
    wrist_pin = Dot(pw0, radius=0.07 * scale, color=WHITE)
    piston = VGroup(piston_body, piston_ring1, piston_ring2, wrist_pin)

    # 8. Mixture / combustion dots inside cylinder
    dots_rel = []
    for row in range(5):
        for col in range(5):
            if row == 4 and (col == 0 or col == 4):
                continue
            u = (-0.45 + col * 0.225 + (0.03 if row % 2 == 1 else -0.03)) * scale
            v = 0.12 + row * 0.18
            dots_rel.append((u, v))

    dots = VGroup(*[
        Dot(
            center + np.array([u, (pw0[1] + piston_h / 2) + v * (y_head - (pw0[1] + piston_h / 2)), 0]),
            radius=0.045 * scale, color=C_INTAKE
        )
        for u, v in dots_rel
    ])

    engine = {
        "center": center,
        "scale": scale,
        "r": r,
        "L": L,
        "crank_center": crank_center,
        "y_head": y_head,
        "piston_h": piston_h,
        "hinge_in": hinge_in,
        "hinge_ex": hinge_ex,
        "dots_rel": dots_rel,
        "left_wall": left_wall,
        "right_wall": right_wall,
        "crankcase": crankcase,
        "head_left": head_left,
        "head_mid": head_mid,
        "head_right": head_right,
        "in_duct": in_duct,
        "in_duct_lower": in_duct_lower,
        "ex_duct": ex_duct,
        "ex_duct_lower": ex_duct_lower,
        "spark_plug": spark_plug,
        "valve_in": valve_in,
        "valve_ex": valve_ex,
        "crank_disc": crank_disc,
        "crank_hub": crank_hub,
        "crank_arm": crank_arm,
        "counter_arm": counter_arm,
        "crank_pin": crank_pin,
        "rod": rod,
        "rod_pin_bottom": rod_pin_bottom,
        "rod_pin_top": rod_pin_top,
        "piston": piston,
        "dots": dots,
    }

    # Helper function to update state based on theta and valve positions
    def update_mechanism(theta_val, in_open_frac=0.0, ex_open_frac=0.0,
                         dot_color=None, dot_opacity=None):
        pw, pc = slider_crank(theta_val, r, L, crank_center)
        piston.move_to(pw)
        rod.put_start_and_end_on(pc, pw)
        rod_pin_bottom.move_to(pc)
        rod_pin_top.move_to(pw)
        crank_arm.put_start_and_end_on(crank_center, pc)
        counter_arm.put_start_and_end_on(
            crank_center,
            crank_center - 0.65 * (pc - crank_center)
        )
        crank_pin.move_to(pc)

        # Valves
        a_in = -35 * DEGREES * in_open_frac
        valve_in.put_start_and_end_on(
            hinge_in,
            hinge_in + 0.28 * scale * np.array([np.cos(a_in), np.sin(a_in), 0])
        )

        a_ex = -35 * DEGREES * ex_open_frac
        valve_ex.put_start_and_end_on(
            hinge_ex,
            hinge_ex + 0.28 * scale * np.array([-np.cos(a_ex), np.sin(a_ex), 0])
        )

        # Dots
        y_top = pw[1] + piston_h / 2
        span = y_head - y_top
        for d, (u, v) in zip(dots, dots_rel):
            d.move_to(center + np.array([u, y_top + v * span, 0]))
            if dot_color is not None:
                d.set_color(dot_color)
            if dot_opacity is not None:
                d.set_opacity(dot_opacity)

    engine["update"] = update_mechanism
    return engine


class HowEngineWorks(SafeScene):
    def construct(self):
        # ── BEAT 1: Title Card & Model Construction with Labeling Pass ───────
        main_title = title("เครื่องยนต์รถทำงานยังไง", size=28)
        self.play(Write(main_title), run_time=1.4)
        self.wait(0.6)

        eng = build_engine(center=ORIGIN, scale=1.0)

        fixed_mobs = VGroup(
            eng["crankcase"], eng["left_wall"], eng["right_wall"],
            eng["head_left"], eng["head_mid"], eng["head_right"],
            eng["in_duct"], eng["in_duct_lower"],
            eng["ex_duct"], eng["ex_duct_lower"],
            eng["crank_disc"], eng["crank_hub"], eng["spark_plug"]
        )
        moving_mobs = VGroup(
            eng["counter_arm"], eng["crank_arm"], eng["crank_pin"],
            eng["rod"], eng["rod_pin_bottom"], eng["rod_pin_top"],
            eng["piston"], eng["valve_in"], eng["valve_ex"]
        )

        self.play(
            FadeIn(fixed_mobs, shift=DOWN * 0.2),
            FadeIn(moving_mobs, shift=UP * 0.2),
            run_time=1.8
        )
        self.wait(0.6)

        # Mandatory labeling pass with arrows (House style: name parts first appearance)
        l_in  = Text("วาล์วไอดี", font_size=20, color=WHITE).move_to([-2.7, 1.25, 0])
        l_pis = Text("ลูกสูบ", font_size=20, color=WHITE).move_to([-2.7, 0.20, 0])
        l_crk = Text("เพลาข้อเหวี่ยง", font_size=20, color=WHITE).move_to([-2.7, -1.75, 0])

        l_spk = Text("หัวเทียน", font_size=20, color=WHITE).move_to([2.7, 1.45, 0])
        l_ex  = Text("วาล์วไอเสีย", font_size=20, color=WHITE).move_to([2.7, 0.65, 0])
        l_rod = Text("ก้านสูบ", font_size=20, color=WHITE).move_to([2.7, -0.75, 0])

        labels = VGroup(l_in, l_pis, l_crk, l_spk, l_ex, l_rod)
        arrows = VGroup(
            Arrow(l_in.get_right(), eng["hinge_in"] + [0.14, 0, 0], buff=0.15,
                  color=GRAYTXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.25),
            Arrow(l_pis.get_right(), [-0.67, 0.20, 0], buff=0.15,
                  color=GRAYTXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.25),
            Arrow(l_crk.get_right(), [-0.65, -1.75, 0], buff=0.15,
                  color=GRAYTXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.25),
            Arrow(l_spk.get_left(), eng["spark_plug"].get_center() + [0.10, 0, 0], buff=0.15,
                  color=GRAYTXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.25),
            Arrow(l_ex.get_left(), eng["hinge_ex"] + [-0.14, 0, 0], buff=0.15,
                  color=GRAYTXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.25),
            Arrow(l_rod.get_left(), [0.08, -0.75, 0], buff=0.15,
                  color=GRAYTXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.25),
        )

        self.play(
            LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in [l_in, l_pis, l_crk]], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l, shift=LEFT * 0.1) for l in [l_spk, l_ex, l_rod]], lag_ratio=0.15),
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12),
            run_time=1.2
        )
        self.wait(1.6)
        self.play(FadeOut(labels), FadeOut(arrows), run_time=0.6)
        self.wait(0.4)

        # ── BEAT 2: Intake Stroke (จังหวะที่ 1: ดูด) ─────────────────────────
        cap1 = caption_top("จังหวะที่ 1: ดูด (Intake) — วาล์วไอดีเปิด ดูดส่วนผสมอากาศและน้ำมันเข้า", color=C_INTAKE)

        # Target open valve geometry
        v_in_open = Line(
            eng["hinge_in"],
            eng["hinge_in"] + 0.28 * np.array([np.cos(-35 * DEGREES), np.sin(-35 * DEGREES), 0]),
            color=C_INTAKE, stroke_width=5
        )
        v_in_closed = Line(
            eng["hinge_in"], eng["hinge_in"] + np.array([0.28, 0, 0]),
            color=C_VALVE, stroke_width=5
        )

        # Temporal contiguity & flash rule: valve opening + highlight + caption in SAME self.play()
        self.play(
            FadeIn(cap1, shift=DOWN * 0.15),
            Flash(eng["hinge_in"] + [0.14, 0, 0], color=WARN, flash_radius=0.35, line_length=0.18),
            Transform(eng["valve_in"], v_in_open),
            run_time=1.0
        )

        # Mixture dots flow into the cylinder as piston descends
        for d in eng["dots"]:
            d.set_color(C_INTAKE)
            d.set_opacity(0.0)
        self.add(eng["dots"])

        theta_trk = ValueTracker(0.0)

        def upd_intake(_m):
            th = theta_trk.get_value()
            eng["update"](th, in_open_frac=1.0, ex_open_frac=0.0)
            # Dots appear progressively as piston moves down
            prog = th / PI
            for i, dot in enumerate(eng["dots"]):
                if i / len(eng["dots"]) <= prog:
                    dot.set_opacity(1.0)

        eng["piston"].add_updater(upd_intake)
        self.play(theta_trk.animate.set_value(PI), run_time=3.2, rate_func=linear)
        eng["piston"].remove_updater(upd_intake)

        # Intake valve closes
        self.play(
            Transform(eng["valve_in"], v_in_closed),
            run_time=0.5
        )
        self.wait(0.8)

        # ── BEAT 3: Compression Stroke (จังหวะที่ 2: อัด) ────────────────────
        cap2 = caption_top("จังหวะที่ 2: อัด (Compression) — วาล์วปิดสนิท ลูกสูบเลื่อนขึ้นอัดไอดีจนร้อนจัด", color=C_COMPRESS)
        self.play(
            FadeOut(cap1),
            FadeIn(cap2, shift=DOWN * 0.15),
            run_time=0.8
        )

        def upd_compress(_m):
            th = theta_trk.get_value()
            eng["update"](th, in_open_frac=0.0, ex_open_frac=0.0)
            frac = np.clip((th - PI) / PI, 0.0, 1.0)
            col = interpolate_color(C_BLUE_MC, C_ORANGE_MC, frac)
            for d in eng["dots"]:
                d.set_color(col)

        eng["piston"].add_updater(upd_compress)
        self.play(theta_trk.animate.set_value(2 * PI), run_time=3.2, rate_func=linear)
        eng["piston"].remove_updater(upd_compress)
        self.wait(0.8)

        # ── BEAT 4: Power Stroke (จังหวะที่ 3: ระเบิด) ───────────────────────
        cap3 = caption_top("จังหวะที่ 3: ระเบิด (Power) — หัวเทียนจุดประกายไฟ ระเบิดดันลูกสูบลงเร็วมาก", color=C_POWER)
        spark_tip = eng["spark_plug"].get_bottom() + UP * 0.03

        # Ignition blast burst
        burst = Circle(
            radius=0.08, color="#FFF9C4", fill_color="#FFEE58",
            fill_opacity=0.95, stroke_width=2
        ).move_to(spark_tip)

        # Flash rule: highlight spark plug when mentioned in caption
        self.play(
            FadeOut(cap2),
            FadeIn(cap3, shift=DOWN * 0.15),
            Indicate(eng["spark_plug"], color=WARN, scale_factor=1.2),
            FadeIn(burst),
            Flash(spark_tip, color=YELLOW, line_length=0.25, num_lines=8, flash_radius=0.3),
            run_time=1.2
        )

        # Expanding explosion burst
        self.play(
            burst.animate.scale(6.0).set_fill(color=C_POWER, opacity=0.0).set_stroke(opacity=0.0),
            run_time=0.4
        )
        self.remove(burst)

        # Dots turn into fiery flame
        for d in eng["dots"]:
            d.set_color(C_POWER)

        # Power stroke: noticeably faster (1.1s vs 3.2s) - real kinematics speedup
        def upd_power(_m):
            th = theta_trk.get_value()
            eng["update"](th, in_open_frac=0.0, ex_open_frac=0.0)

        eng["piston"].add_updater(upd_power)
        self.play(theta_trk.animate.set_value(3 * PI), run_time=1.1, rate_func=linear)
        eng["piston"].remove_updater(upd_power)
        self.wait(1.0)

        # ── BEAT 5: Exhaust Stroke (จังหวะที่ 4: คาย) ────────────────────────
        cap4 = caption_top("จังหวะที่ 4: คาย (Exhaust) — วาล์วไอเสียเปิด ดันก๊าซไอเสียที่เผาไหม้แล้วออกไป", color=C_EXHAUST)
        # Recolor dots to burnt gray
        for d in eng["dots"]:
            d.set_color(C_EXHAUST)

        v_ex_open = Line(
            eng["hinge_ex"],
            eng["hinge_ex"] + 0.28 * np.array([-np.cos(-35 * DEGREES), np.sin(-35 * DEGREES), 0]),
            color=C_EXHAUST, stroke_width=5
        )
        v_ex_closed = Line(
            eng["hinge_ex"], eng["hinge_ex"] + np.array([-0.28, 0, 0]),
            color=C_VALVE, stroke_width=5
        )

        # Exhaust valve opening + highlight
        self.play(
            FadeOut(cap3),
            FadeIn(cap4, shift=DOWN * 0.15),
            Flash(eng["hinge_ex"] + [-0.14, 0, 0], color=WARN, flash_radius=0.35, line_length=0.18),
            Transform(eng["valve_ex"], v_ex_open),
            run_time=1.0
        )

        # Piston ascends, pushing burnt gas dots out through exhaust duct
        def upd_exhaust(_m):
            th = theta_trk.get_value()
            eng["update"](th, in_open_frac=0.0, ex_open_frac=1.0)
            # As dots reach upper head, they fade out as if vented
            th_frac = (th - 3 * PI) / PI
            for i, dot in enumerate(eng["dots"]):
                if i / len(eng["dots"]) < th_frac * 0.95:
                    dot.set_opacity(max(0.0, 1.0 - (th_frac - i / len(eng["dots"])) * 3))

        eng["piston"].add_updater(upd_exhaust)
        self.play(theta_trk.animate.set_value(4 * PI), run_time=3.2, rate_func=linear)
        eng["piston"].remove_updater(upd_exhaust)

        # Exhaust valve closes
        self.play(
            Transform(eng["valve_ex"], v_ex_closed),
            run_time=0.5
        )
        self.wait(1.0)

        # ── BEAT 6: 4-Cylinder Payoff Segment ────────────────────────────────
        # Clean transition: fade out single cylinder, bring in 4 cylinders
        self.play(
            FadeOut(cap4),
            FadeOut(fixed_mobs),
            FadeOut(moving_mobs),
            FadeOut(eng["dots"]),
            run_time=1.2
        )

        cap_4cyl_1 = caption_top("ทำไมเครื่องยนต์จริงจึงหมุนได้เรียบสม่ำเสมอ ไม่กระตุก?", color=WHITE)
        self.play(FadeIn(cap_4cyl_1, shift=DOWN * 0.15), run_time=0.8)

        # Create 4 mini cylinders side by side
        xs = [-4.5, -1.5, 1.5, 4.5]
        # Staggered firing order phase offsets (180 deg = PI interval)
        # At start: Cyl 1=Power, Cyl 2=Compression, Cyl 3=Exhaust, Cyl 4=Intake
        phases = [2 * PI, PI, 3 * PI, 0.0]
        c_names = ["สูบ 1", "สูบ 2", "สูบ 3", "สูบ 4"]
        s_names = ["ระเบิด (Power)", "อัด (Compression)", "คาย (Exhaust)", "ดูด (Intake)"]
        s_cols  = [C_POWER, C_COMPRESS, C_EXHAUST, C_INTAKE]

        cylinders = []
        mini_mobs = VGroup()
        badges = VGroup()

        for x, ph, c_n, s_n, s_c in zip(xs, phases, c_names, s_names, s_cols):
            mini = build_engine(center=np.array([x, -0.6, 0]), scale=0.52)
            mini["phase"] = ph
            # Apply initial phase and set dots
            in_op = 1.0 if (0 <= ph < PI) else 0.0
            ex_op = 1.0 if (3 * PI <= ph < 4 * PI) else 0.0
            mini["update"](ph, in_open_frac=in_op, ex_open_frac=ex_op, dot_color=s_c, dot_opacity=0.85)
            cylinders.append(mini)

            # Mini engine group
            m_fixed = VGroup(
                mini["crankcase"], mini["left_wall"], mini["right_wall"],
                mini["head_left"], mini["head_mid"], mini["head_right"],
                mini["in_duct"], mini["ex_duct"],
                mini["crank_disc"], mini["crank_hub"], mini["spark_plug"]
            )
            m_moving = VGroup(
                mini["counter_arm"], mini["crank_arm"], mini["crank_pin"],
                mini["rod"], mini["rod_pin_bottom"], mini["rod_pin_top"],
                mini["piston"], mini["valve_in"], mini["valve_ex"],
                mini["dots"]
            )
            mini_mobs.add(m_fixed, m_moving)

            # Badge above cylinder
            box = RoundedRectangle(
                corner_radius=0.12, width=2.25, height=0.58,
                stroke_color=s_c, fill_color=s_c, fill_opacity=0.25, stroke_width=2
            ).move_to([x, 0.75, 0])
            txt = Text(s_n, font_size=15, color=s_c).move_to(box.get_center())
            c_lbl = Text(c_n, font_size=17, color=WHITE).next_to(box, UP, buff=0.12)
            badges.add(VGroup(box, txt, c_lbl))

        # Shared crankshaft connecting bar at bottom
        crank_y = cylinders[0]["crank_center"][1]
        shared_crank_bar = Line([-5.6, crank_y, 0], [5.6, crank_y, 0], color=METAL, stroke_width=5)
        mini_mobs.add(shared_crank_bar)

        self.play(
            FadeIn(mini_mobs, shift=UP * 0.2),
            LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in badges], lag_ratio=0.15),
            run_time=1.6
        )
        self.wait(1.5)

        cap_4cyl_2 = caption_top("สูบเดี่ยวสร้างแรงขับแค่ 1 ใน 4 จังหวะ (มีแรงแค่ 25% ของเวลา)", color=GRAYTXT)
        self.play(FadeOut(cap_4cyl_1), FadeIn(cap_4cyl_2, shift=DOWN * 0.15), run_time=0.8)
        self.wait(1.8)

        cap_4cyl_3 = caption_top("เครื่องยนต์ 4 สูบ จุดระเบิดสลับกัน → จะมีสูบส่งกำลังขับตลอดเวลา เพลาจึงหมุนเรียบ!", color=OK)
        self.play(FadeOut(cap_4cyl_2), FadeIn(cap_4cyl_3, shift=DOWN * 0.15), run_time=0.8)

        # Animate continuous rotation of 4 cylinders (2 full engine cycles = 8 * PI)
        theta_4cyl = ValueTracker(0.0)

        def upd_4cyl_all(_m):
            t_val = theta_4cyl.get_value()
            for mini in cylinders:
                eff_th = (t_val + mini["phase"]) % (4 * PI)
                in_open = 1.0 if (0 <= eff_th < PI) else 0.0
                ex_open = 1.0 if (3 * PI <= eff_th < 4 * PI) else 0.0

                if 0 <= eff_th < PI:
                    d_col = C_INTAKE
                elif PI <= eff_th < 2 * PI:
                    frac = (eff_th - PI) / PI
                    d_col = interpolate_color(C_BLUE_MC, C_ORANGE_MC, frac)
                elif 2 * PI <= eff_th < 3 * PI:
                    d_col = C_POWER
                else:
                    d_col = C_EXHAUST

                mini["update"](eff_th, in_open_frac=in_open, ex_open_frac=ex_open,
                               dot_color=d_col, dot_opacity=0.85)

        self.add(shared_crank_bar)
        shared_crank_bar.add_updater(upd_4cyl_all)
        self.play(theta_4cyl.animate.set_value(4 * PI), run_time=6.0, rate_func=linear)
        shared_crank_bar.remove_updater(upd_4cyl_all)
        self.wait(1.4)

        # ── BEAT 7: Summary Card ─────────────────────────────────────────────
        self.play(
            FadeOut(cap_4cyl_3),
            FadeOut(mini_mobs),
            FadeOut(badges),
            FadeOut(main_title),
            run_time=1.0
        )

        sum_title = title("สรุป: การทำงานของเครื่องยนต์ 4 จังหวะ (4-Stroke Engine)", size=26)
        self.play(FadeIn(sum_title, shift=DOWN * 0.2), run_time=0.8)

        # 4 Summary Rows
        summary_data = [
            ("1. ดูด (Intake)", C_INTAKE, "วาล์วไอดีเปิด ลูกสูบเลื่อนลง ดูดไอดีเข้ากระบอกสูบ"),
            ("2. อัด (Compression)", C_COMPRESS, "วาล์วปิดสนิท ลูกสูบเลื่อนขึ้น อัดไอดีจนร้อนและแรงดันสูง"),
            ("3. ระเบิด (Power)", C_POWER, "หัวเทียนจุดระเบิด ดันลูกสูบลงอย่างรวดเร็ว (จังหวะส่งกำลัง)"),
            ("4. คาย (Exhaust)", C_EXHAUST, "วาล์วไอเสียเปิด ลูกสูบเลื่อนขึ้น ขับก๊าซไอเสียออกไป"),
        ]

        row_ys = [1.75, 0.75, -0.25, -1.25]
        row_groups = []

        for (name_t, col_t, desc_t), y in zip(summary_data, row_ys):
            pill = RoundedRectangle(
                corner_radius=0.15, width=3.0, height=0.68,
                stroke_color=col_t, fill_color=col_t, fill_opacity=0.25, stroke_width=2
            ).move_to([-3.4, y, 0])
            lbl = Text(name_t, font_size=19, color=col_t).move_to(pill.get_center())
            desc = Text(desc_t, font_size=19, color=WHITE).next_to(pill, RIGHT, buff=0.35)
            row_groups.append(VGroup(pill, lbl, desc))

        self.play(
            LaggedStart(*[FadeIn(rg, shift=RIGHT * 0.25) for rg in row_groups], lag_ratio=0.25),
            run_time=2.2
        )
        self.wait(1.2)

        # Highlight Power stroke row as the unique power producing stroke
        self.play(
            Indicate(row_groups[2], color=WARN, scale_factor=1.06),
            run_time=1.2
        )

        takeaway = Text(
            "วัฏจักร 4 จังหวะ = เพลาข้อเหวี่ยงหมุนครบ 2 รอบ (720°) อย่างสมบูรณ์",
            font_size=20, color=OK
        ).move_to([0, -2.55, 0])

        self.play(FadeIn(takeaway, shift=UP * 0.2), run_time=0.9)
        self.wait(2.2)

        # Final fade out
        self.fade_out_all(run_time=1.2)
