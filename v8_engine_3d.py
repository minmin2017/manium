"""
v8_engine_3d.py — เครื่องยนต์ V8 แบบ 3 มิติ (3D V8 Engine Kinematics & Firing Order)

Production Manim Community 3D teaching video following Min's house style,
SafeThreeDScene layout constraints, exact slider-crank kinematics,
and pedagogy storyboard requirements.
"""

from mlib import *
import numpy as np

# ── Colors (Strictly consistent across concepts) ─────────────────────────────
C_LEFT   = "#4FC3F7"   # แบงค์ซ้าย (ฟ้าสว่าง) — สูบ 1, 3, 5, 7
C_RIGHT  = "#FFB74D"   # แบงค์ขวา (ส้มอมเหลือง) — สูบ 2, 4, 6, 8
C_POWER  = "#FF7043"   # จังหวะระเบิด / ส่งกำลัง (ส้มแดงเพลิง)
C_SPARK  = "#FFF176"   # ประกายไฟหัวเทียน (เหลืองสว่าง)
C_ROD    = "#ECEFF1"   # ก้านสูบ (โลหะสีสว่าง)
C_BLOCK  = "#37474F"   # โครงสร้างเสื้อสูบ (เทาเข้มอมฟ้า)
C_CRANK  = "#78909C"   # แขนเพลาข้อเหวี่ยง / ตุ้มถ่วงน้ำหนัก


# ── Kinematics & Geometry Constants ──────────────────────────────────────────
CRANK_R = 0.40         # รัศมีข้อเหวี่ยง (crank throw radius)
ROD_L   = 1.20         # ความยาวก้านสูบ (connecting rod length, approx 3x r)
Z_CRANK = -0.70        # ระดับแกนกลางเพลาข้อเหวี่ยง (Z axis in scene)
BANK_ANG = 45 * DEGREES

# Unit vectors along the two cylinder banks (45 deg from vertical Z axis in XZ plane)
# Left bank tilts toward -X, Right bank tilts toward +X; angle between them is 90 deg.
U_LEFT  = np.array([-np.sin(BANK_ANG), 0.0, np.cos(BANK_ANG)])
U_RIGHT = np.array([ np.sin(BANK_ANG), 0.0, np.cos(BANK_ANG)])

# 4 Crank throw longitudinal positions along Y axis (front to back)
Y_THROWS = np.array([-1.35, -0.45, 0.45, 1.35])

# Cross-plane crankshaft: 4 throws spaced 90 deg apart around crankshaft
# Pin base angles in XZ plane so that cylinders reach TDC at their firing events:
PIN_BASES = np.array([-np.pi / 4, 5 * np.pi / 4, np.pi / 4, 3 * np.pi / 4])

# Cylinder specs: (cyl_id, throw_idx, bank, name_th)
CYLINDER_SPECS = [
    (1, 0, "L", "สูบ 1"),
    (2, 0, "R", "สูบ 2"),
    (3, 1, "L", "สูบ 3"),
    (4, 1, "R", "สูบ 4"),
    (5, 2, "L", "สูบ 5"),
    (6, 2, "R", "สูบ 6"),
    (7, 3, "L", "สูบ 7"),
    (8, 3, "R", "สูบ 8"),
]

# Standard V8 Firing Order
FIRING_ORDER = [1, 8, 4, 3, 6, 5, 7, 2]


def slider_crank_offset(theta_rel, r=CRANK_R, L=ROD_L):
    """
    Exact kinematics of the slider-crank mechanism:
    piston_offset(theta) = r*cos(theta) + sqrt(L**2 - (r*sin(theta))**2)
    theta = 0 at Top Dead Center (TDC, outermost position = r + L).
    theta = pi at Bottom Dead Center (BDC, innermost position = L - r).
    Connecting rod length is strictly L at all angles theta.
    """
    return r * np.cos(theta_rel) + np.sqrt(L**2 - (r * np.sin(theta_rel))**2)


def build_v8_engine():
    """
    Build a genuine 3D V8 engine model with:
    - Crankshaft running along Y axis with 4 crank throws (spaced 90 deg, cross-plane).
    - 2 cylinder banks at 90 deg V-angle (45 deg on each side).
    - 8 pistons moving strictly along their respective bank axes.
    - 8 connecting rods (2 rods sharing each crank throw).
    - Spark plugs and ignition glow bursts at cylinder heads.
    Returns dictionary containing all static and moving components, plus an update function.
    """
    static_mobs = VGroup()
    moving_mobs = VGroup()

    # 1. Crankshaft main line & end features
    crank_main = line3([0, -2.15, Z_CRANK], [0, 2.15, Z_CRANK], color=METAL, thickness=0.06)
    pulley_front = Circle(radius=0.45, color=METAL, stroke_width=2.5).rotate(90 * DEGREES, axis=UP).move_to([0, -2.15, Z_CRANK])
    flywheel_rear = Circle(radius=0.62, color=METAL, stroke_width=2.5).rotate(90 * DEGREES, axis=UP).move_to([0, 2.15, Z_CRANK])
    static_mobs.add(crank_main, pulley_front, flywheel_rear)

    # 2. Engine Block V-frame rails (giving realistic solid structure)
    d_head = CRANK_R + ROD_L + 0.22
    p_head_L_front = np.array([0, -1.85, Z_CRANK]) + d_head * U_LEFT
    p_head_L_rear  = np.array([0,  1.85, Z_CRANK]) + d_head * U_LEFT
    p_head_R_front = np.array([0, -1.85, Z_CRANK]) + d_head * U_RIGHT
    p_head_R_rear  = np.array([0,  1.85, Z_CRANK]) + d_head * U_RIGHT

    rail_deck_L = line3(p_head_L_front, p_head_L_rear, color=C_BLOCK, thickness=0.025)
    rail_deck_R = line3(p_head_R_front, p_head_R_rear, color=C_BLOCK, thickness=0.025)
    rail_valley = line3([0, -1.85, Z_CRANK + 0.55], [0, 1.85, Z_CRANK + 0.55], color=C_BLOCK, thickness=0.02)
    rib_front_L = line3([0, -1.85, Z_CRANK], p_head_L_front, color=C_BLOCK, thickness=0.035)
    rib_front_R = line3([0, -1.85, Z_CRANK], p_head_R_front, color=C_BLOCK, thickness=0.035)
    rib_rear_L  = line3([0,  1.85, Z_CRANK], p_head_L_rear,  color=C_BLOCK, thickness=0.035)
    rib_rear_R  = line3([0,  1.85, Z_CRANK], p_head_R_rear,  color=C_BLOCK, thickness=0.035)
    static_mobs.add(rail_deck_L, rail_deck_R, rail_valley, rib_front_L, rib_front_R, rib_rear_L, rib_rear_R)

    # 3. Static Cylinder Sleeves and Spark Plugs
    d_top = CRANK_R + ROD_L + 0.16
    d_bot = ROD_L - CRANK_R - 0.10
    bore_r = 0.30

    left_bank_mobs = VGroup()
    right_bank_mobs = VGroup()
    spark_plugs = {}
    spark_glows = {}

    for (cid, throw_idx, bank, _name) in CYLINDER_SPECS:
        y_pos = Y_THROWS[throw_idx]
        u_bank = U_LEFT if bank == "L" else U_RIGHT
        rot_ang = -45 * DEGREES if bank == "L" else 45 * DEGREES
        bank_col = C_LEFT if bank == "L" else C_RIGHT
        p_shaft = np.array([0.0, y_pos, Z_CRANK])

        # Bore top and bottom guide rings
        p_top = p_shaft + d_top * u_bank
        p_bot = p_shaft + d_bot * u_bank

        ring_top = Circle(radius=bore_r, color=bank_col, stroke_width=2.0, stroke_opacity=0.7)
        ring_top.rotate(rot_ang, axis=UP).move_to(p_top)
        ring_bot = Circle(radius=bore_r, color=bank_col, stroke_width=1.5, stroke_opacity=0.35)
        ring_bot.rotate(rot_ang, axis=UP).move_to(p_bot)

        # Bore wall lines (along Y offset)
        w1 = line3(p_top + [0,  bore_r * 0.9, 0], p_bot + [0,  bore_r * 0.9, 0], color=bank_col, thickness=0.015)
        w2 = line3(p_top + [0, -bore_r * 0.9, 0], p_bot + [0, -bore_r * 0.9, 0], color=bank_col, thickness=0.015)
        w1.set_opacity(0.4)
        w2.set_opacity(0.4)

        # Spark plug at cylinder head deck
        p_spark_tip = p_shaft + (d_top + 0.05) * u_bank
        p_spark_top = p_spark_tip + 0.16 * u_bank
        sp_line = line3(p_spark_top, p_spark_tip, color=WHITE, thickness=0.035)
        spark_plugs[cid] = sp_line

        # Ignition flash burst (Dot + outer glow halo)
        glow_dot = Dot(p_spark_tip, radius=0.14, color=C_SPARK)
        glow_dot.set_opacity(0.0)
        glow_outer = Circle(radius=0.32, color=C_POWER, fill_color=C_POWER, fill_opacity=0.0, stroke_opacity=0.0).move_to(p_spark_tip)
        glow_outer.rotate(rot_ang, axis=UP)
        spark_glows[cid] = VGroup(glow_dot, glow_outer)

        cyl_group = VGroup(ring_top, ring_bot, w1, w2, sp_line, spark_glows[cid])
        if bank == "L":
            left_bank_mobs.add(cyl_group)
        else:
            right_bank_mobs.add(cyl_group)

    static_mobs.add(left_bank_mobs, right_bank_mobs)

    # 4. Moving Crank Throws (4 throws, 90 deg cross-plane)
    crank_arms = []
    crank_cws  = []
    crank_pins = []

    for k in range(4):
        y_pos = Y_THROWS[k]
        p_shaft = np.array([0.0, y_pos, Z_CRANK])
        arm = line3(p_shaft, p_shaft + [0, 0, CRANK_R], color=C_CRANK, thickness=0.045)
        cw  = line3(p_shaft, p_shaft - [0, 0, CRANK_R * 0.4], color=C_CRANK, thickness=0.065)
        pin = Dot(p_shaft + [0, 0, CRANK_R], radius=0.06, color=WHITE)
        crank_arms.append(arm)
        crank_cws.append(cw)
        crank_pins.append(pin)
        moving_mobs.add(arm, cw, pin)

    # 5. Moving Pistons & Connecting Rods (8 pairs)
    pistons = {}
    wrists  = {}
    rods    = {}

    for (cid, throw_idx, bank, _name) in CYLINDER_SPECS:
        y_pos = Y_THROWS[throw_idx]
        u_bank = U_LEFT if bank == "L" else U_RIGHT
        rot_ang = -45 * DEGREES if bank == "L" else 45 * DEGREES
        bank_col = C_LEFT if bank == "L" else C_RIGHT

        # Piston assembly: crown disc + skirt ring + side struts + wrist pin dot
        crown = Circle(radius=0.27, color=bank_col, fill_color=bank_col, fill_opacity=0.75, stroke_width=2)
        crown.rotate(rot_ang, axis=UP).move_to(0.12 * u_bank)
        skirt = Circle(radius=0.27, color=bank_col, stroke_width=1.5, stroke_opacity=0.45)
        skirt.rotate(rot_ang, axis=UP).move_to(-0.10 * u_bank)
        st1 = Line(0.12 * u_bank + [0, 0.24, 0], -0.10 * u_bank + [0, 0.24, 0], color=bank_col, stroke_width=1.5)
        st2 = Line(0.12 * u_bank - [0, 0.24, 0], -0.10 * u_bank - [0, 0.24, 0], color=bank_col, stroke_width=1.5)
        wrist_dot = Dot([0, 0, 0], radius=0.055, color=WHITE)

        piston_grp = VGroup(crown, skirt, st1, st2, wrist_dot)
        pistons[cid] = piston_grp
        wrists[cid] = wrist_dot

        # Connecting rod: line from crank pin to wrist pin
        rod = line3([0, y_pos, Z_CRANK], [0, y_pos, Z_CRANK + ROD_L], color=C_ROD, thickness=0.034)
        rods[cid] = rod
        moving_mobs.add(rod, piston_grp)

    def update_engine(theta_val, active_cyl=None, flash_intensity=0.0):
        """Update all 4 crank throws, 8 pistons, and 8 rods from one master theta."""
        for k in range(4):
            y_pos = Y_THROWS[k]
            p_shaft = np.array([0.0, y_pos, Z_CRANK])
            psi = PIN_BASES[k] - theta_val
            p_pin = np.array([CRANK_R * np.sin(psi), y_pos, Z_CRANK + CRANK_R * np.cos(psi)])
            p_cw  = np.array([-0.38 * CRANK_R * np.sin(psi), y_pos, Z_CRANK - 0.38 * CRANK_R * np.cos(psi)])

            crank_arms[k].put_start_and_end_on(p_shaft, p_pin)
            crank_cws[k].put_start_and_end_on(p_shaft, p_cw)
            crank_pins[k].move_to(p_pin)

        for (cid, throw_idx, bank, _name) in CYLINDER_SPECS:
            y_pos = Y_THROWS[throw_idx]
            p_shaft = np.array([0.0, y_pos, Z_CRANK])
            psi = PIN_BASES[throw_idx] - theta_val
            p_pin = np.array([CRANK_R * np.sin(psi), y_pos, Z_CRANK + CRANK_R * np.cos(psi)])

            u_bank = U_LEFT if bank == "L" else U_RIGHT
            bank_ref = -np.pi / 4 if bank == "L" else np.pi / 4
            theta_rel = (bank_ref - psi) % (2 * np.pi)

            dist = slider_crank_offset(theta_rel)
            p_wrist = p_shaft + dist * u_bank

            rods[cid].put_start_and_end_on(p_pin, p_wrist)
            pistons[cid].shift(p_wrist - wrists[cid].get_center())

            # Spark ignition flash update
            glow_grp = spark_glows[cid]
            if active_cyl == cid and flash_intensity > 0.01:
                glow_grp[0].set_opacity(flash_intensity)
                glow_grp[1].set_fill(opacity=flash_intensity * 0.75).set_stroke(opacity=flash_intensity * 0.85)
            else:
                glow_grp[0].set_opacity(0.0)
                glow_grp[1].set_fill(opacity=0.0).set_stroke(opacity=0.0)

    # Apply initial position at theta = 0
    update_engine(0.0)

    return {
        "static": static_mobs,
        "moving": moving_mobs,
        "crank_main": crank_main,
        "left_bank": left_bank_mobs,
        "right_bank": right_bank_mobs,
        "pistons": pistons,
        "rods": rods,
        "spark_plugs": spark_plugs,
        "spark_glows": spark_glows,
        "update": update_engine,
    }


def make_firing_chain():
    """
    Build on-screen HUD badge chain for 1-8-4-3-6-5-7-2 firing order.
    Returns VGroup of badges and list of individual badge controls.
    """
    chain_group = VGroup()
    badge_boxes = []
    badge_texts = []

    for i, cid in enumerate(FIRING_ORDER):
        bank_col = C_LEFT if cid % 2 != 0 else C_RIGHT
        box = RoundedRectangle(
            width=0.74, height=0.50, corner_radius=0.09,
            stroke_color=bank_col, stroke_width=2.0,
            fill_color="#1A2126", fill_opacity=0.88
        )
        txt = Text(str(cid), font_size=18, color=WHITE).move_to(box.get_center())
        badge = VGroup(box, txt)
        chain_group.add(badge)
        badge_boxes.append(box)
        badge_texts.append(txt)

        if i < 7:
            arrow = Arrow(
                [0, 0, 0], [0.30, 0, 0], buff=0,
                stroke_width=2.0, color=GRAYTXT,
                tip_length=0.10, max_tip_length_to_length_ratio=0.5
            )
            chain_group.add(arrow)

    chain_group.arrange(RIGHT, buff=0.10)
    chain_group.move_to([0, 2.05, 0])

    def highlight_step(active_step):
        for idx, (b_box, b_txt) in enumerate(zip(badge_boxes, badge_texts)):
            cid = FIRING_ORDER[idx]
            b_col = C_LEFT if cid % 2 != 0 else C_RIGHT
            if idx == active_step:
                b_box.set_fill(color=C_POWER, opacity=0.95)
                b_box.set_stroke(color=WHITE, width=2.8)
                b_txt.set_color(BLACK)
            else:
                b_box.set_fill(color="#1A2126", opacity=0.88)
                b_box.set_stroke(color=b_col, width=2.0)
                b_txt.set_color(WHITE)

    return chain_group, highlight_step


class V8Engine3D(SafeThreeDScene):
    """
    Genuine 3D V8 engine teaching explainer:
    1. 3D Model introduction & slow ambient camera rotation
    2. Brief labeling pass (crankshaft, left/right banks, piston, rod)
    3. 90-degree V-angle explanation & bank highlights
    4. 1-8-4-3-6-5-7-2 Firing order sequence (real slider-crank kinematics)
    5. Closing comparison card with 4-cylinder inline engine
    """

    def construct(self):
        # ── INITIAL CAMERA SETUP ─────────────────────────────────────────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES)

        # ── BEAT 1: Title & 3D V8 Engine Block Introduction ──────────────────
        main_title = self.hud(title("เครื่องยนต์ V8 แบบ 3 มิติ", size=28))
        cap1 = self.hud(caption_top("เครื่องยนต์ V8: วางลูกสูบ 8 สูบ แบ่งเป็น 2 แถว ทำมุมรูปตัว V รอบเพลาข้อเหวี่ยงเดียว", size=20))

        engine = build_v8_engine()

        self.play(
            FadeIn(main_title, shift=DOWN * 0.15),
            FadeIn(cap1, shift=DOWN * 0.15),
            FadeIn(engine["static"]),
            FadeIn(engine["moving"]),
            run_time=1.4
        )

        # Begin slow ambient camera rotation so the 3D V shape reads clearly
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(1.5)

        # ── BEAT 2: Brief Labeling Pass (1-1.5s) ──────────────────────────────
        # Standing house-style rule: first appearance of multi-part model gets labeled
        lbl_crank  = self.hud(Text("เพลาข้อเหวี่ยง (Crankshaft)", font_size=16, color=METAL).move_to([0, -2.70, 0]))
        lbl_left   = self.hud(Text("แบงค์ซ้าย (Left Bank)", font_size=16, color=C_LEFT).move_to([-4.65, 1.20, 0]))
        lbl_right  = self.hud(Text("แบงค์ขวา (Right Bank)", font_size=16, color=C_RIGHT).move_to([4.65, 1.20, 0]))
        lbl_piston = self.hud(Text("ลูกสูบ (Piston)", font_size=16, color=WHITE).move_to([-4.45, -0.40, 0]))
        lbl_rod    = self.hud(Text("ก้านสูบ (Connecting Rod)", font_size=16, color=WHITE).move_to([4.45, -0.40, 0]))

        arr_crank  = self.hud(Arrow([0, -2.42, 0], [0, -1.80, 0], color=METAL, stroke_width=2.0, tip_length=0.14))
        arr_left   = self.hud(Arrow([-3.40, 1.20, 0], [-1.80, 0.82, 0], color=C_LEFT, stroke_width=2.0, tip_length=0.14))
        arr_right  = self.hud(Arrow([3.40, 1.20, 0], [1.80, 0.82, 0], color=C_RIGHT, stroke_width=2.0, tip_length=0.14))
        arr_piston = self.hud(Arrow([-3.35, -0.40, 0], [-1.35, -0.15, 0], color=WHITE, stroke_width=2.0, tip_length=0.14))
        arr_rod    = self.hud(Arrow([3.15, -0.40, 0], [0.85, -0.48, 0], color=WHITE, stroke_width=2.0, tip_length=0.14))

        labels_hud = VGroup(
            lbl_crank, lbl_left, lbl_right, lbl_piston, lbl_rod,
            arr_crank, arr_left, arr_right, arr_piston, arr_rod
        )

        # Flash the mentioned elements rule in the same play call
        self.play(
            FadeIn(labels_hud),
            Indicate(engine["crank_main"], color=WARN, scale_factor=1.06),
            Indicate(engine["left_bank"], color=C_LEFT, scale_factor=1.04),
            Indicate(engine["right_bank"], color=C_RIGHT, scale_factor=1.04),
            Indicate(engine["pistons"][1], color=WARN, scale_factor=1.08),
            Indicate(engine["rods"][2], color=WHITE, scale_factor=1.08),
            run_time=1.3
        )
        self.wait(1.5)

        # Fade labels out together before continuing
        self.play(FadeOut(labels_hud), run_time=0.5)

        # ── BEAT 3: Explain the V-angle (90 degrees) ──────────────────────────
        # Sequential caption swap to prevent layout linter overlap
        self.play(FadeOut(cap1), run_time=0.3)
        cap2 = self.hud(caption_top("แบงค์กระบอกสูบ 2 ฝั่ง ทำมุมกัน 90 องศา", color=WHITE, size=21))

        self.play(
            FadeIn(cap2, shift=DOWN * 0.15),
            Indicate(engine["left_bank"], color=C_LEFT, scale_factor=1.06),
            run_time=1.2
        )
        self.play(
            Indicate(engine["right_bank"], color=C_RIGHT, scale_factor=1.06),
            run_time=1.2
        )
        self.wait(2.0)

        # ── BEAT 4: Firing-Order Sequence (Main Payoff) ───────────────────────
        # Stop ambient rotation before firing sequence so viewer isn't distracted
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=65 * DEGREES, theta=-55 * DEGREES, run_time=1.0)

        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = self.hud(caption_top(
            "ลำดับการจุดระเบิด V8 มาตรฐาน: 1-8-4-3-6-5-7-2 — สลับข้างซ้ายขวาตลอด ให้แรงหมุนสม่ำเสมอ",
            size=19
        ))

        chain_mob, highlight_step = make_firing_chain()
        self.hud(chain_mob)

        self.play(
            FadeIn(cap3, shift=DOWN * 0.15),
            FadeIn(chain_mob, shift=UP * 0.10),
            run_time=0.8
        )
        self.wait(0.6)

        # Kinematic ValueTracker for master crankshaft rotation
        theta_crank = ValueTracker(0.0)

        def crank_with_torque_pulse(base_th):
            """Power stroke is visibly faster: torque acceleration pulse after TDC ignition."""
            return base_th - 0.055 * np.sin(4 * base_th)

        def engine_updater(_m):
            raw_th = theta_crank.get_value()
            pulsed_th = crank_with_torque_pulse(raw_th)

            # Determine active cylinder in firing order: 8 steps per 720 deg (4*pi)
            cycle_phase = pulsed_th % (4 * np.pi)
            step_float = cycle_phase / (np.pi / 2)
            step_idx = int(step_float) % 8
            active_cyl = FIRING_ORDER[step_idx]

            # Flash intensity peaks at start of power stroke (TDC) then fades
            window_frac = step_float - int(step_float)
            if window_frac < 0.48:
                flash_val = float(np.sin(np.pi * (window_frac / 0.48)))
            else:
                flash_val = 0.0

            engine["update"](pulsed_th, active_cyl=active_cyl, flash_intensity=flash_val)
            highlight_step(step_idx)

        # Attach updater to the crankshaft
        engine["crank_main"].add_updater(engine_updater)

        # Cycle 1: 1 full 720-degree cycle (all 8 cylinders fire once, deliberate pace)
        self.play(
            theta_crank.animate.set_value(4 * np.pi),
            run_time=16.0,
            rate_func=linear
        )
        self.wait(0.6)

        # Cycle 2: 1 faster continuous 720-degree cycle showing smooth rhythmic operation
        self.play(
            theta_crank.animate.set_value(8 * np.pi),
            run_time=8.0,
            rate_func=linear
        )
        self.wait(1.0)

        engine["crank_main"].remove_updater(engine_updater)

        # ── BEAT 5: Closing Comparison Card ──────────────────────────────────
        self.play(
            FadeOut(chain_mob),
            FadeOut(cap3),
            FadeOut(engine["static"]),
            FadeOut(engine["moving"]),
            FadeOut(main_title),
            run_time=1.0
        )

        title_close = self.hud(title("เปรียบเทียบ: 4 สูบแถวเรียง vs V8", size=26))

        card = RoundedRectangle(
            width=10.6, height=2.5, corner_radius=0.15,
            stroke_color=OK, stroke_width=2.5,
            fill_color="#1A2126", fill_opacity=0.92
        ).move_to([0, 0.4, 0])

        t1 = Text("หลักการเดียวกัน: จุดระเบิดสลับจังหวะเพื่อให้เพลาหมุนได้ต่อเนื่อง", font_size=20, color=OK).move_to(card.get_top() + DOWN * 0.48)
        t2 = Text("เครื่องยนต์ V8 เพิ่มเป็น 8 สูบ 2 แบงค์ จุดระเบิดทุก 90 องศา (แทนที่ทุก 180 องศา)", font_size=18, color=WHITE).next_to(t1, DOWN, buff=0.25)
        t3 = Text("เพลาข้อเหวี่ยงจึงได้รับแรงผลักสม่ำเสมอ ส่งกำลังนุ่มนวลและต่อเนื่องยิ่งขึ้นเป็น 2 เท่า", font_size=18, color=CURRENT).next_to(t2, DOWN, buff=0.22)

        card_grp = self.hud(VGroup(card, t1, t2, t3))

        self.play(
            FadeIn(title_close, shift=DOWN * 0.15),
            FadeIn(card_grp, shift=UP * 0.15),
            run_time=0.9
        )
        self.wait(3.2)

        # Clean complete scene exit
        self.fade_out_all(run_time=0.9)
