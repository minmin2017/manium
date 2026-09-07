"""
dc_motor_3d.py — มอเตอร์ไฟฟ้า DC ทำงานยังไง (How a DC Electric Motor Works)

Production Manim Community 3D teaching video following Min's house style:
- Subclasses SafeThreeDScene with full layout checking across the timeline.
- Flat 3D vectors via arrow3() and line3() from mlib (no slow Arrow3D/Line3D).
- ALL captions/labels registered via self.hud() or self.world_text().
- Sequential caption transitions (FadeOut then FadeIn).
- Exact physics conventions:
    Shaft along Y. Field B along +X (N pole at -X, S pole at +X).
    Conductor at +X with +Y current -> F = -Z (down), torque = +Y.
    Conductor at -X with -Y current -> F = +Z (up), torque = +Y.
    Dead point at z = +/-r, x = 0: forces purely radial, torque = 0.
    Commutator flip at dead point reverses current -> torque stays +Y.
"""

from mlib import *
import numpy as np

# ── Color Palette (Strictly consistent throughout) ───────────────────────────
C_N_POLE   = "#E53935"   # ขั้วเหนือ N (แดง)
C_S_POLE   = "#1E88E5"   # ขั้วใต้ S (น้ำเงิน)
C_FIELD    = FIELD       # สนามแม่เหล็ก B (#42A5F5 ฟ้าสว่าง)
C_CURRENT  = "#FFEA00"   # กระแส I (เหลืองสว่างสดใส เห็นชัดเจน)
C_FORCE    = "#00E676"   # แรง F (เขียวนีออนสว่างสดใส ชัดเจนทุกมุม)
C_TORQUE   = TORQUE      # ทอร์ก tau (#AB47BC ม่วง)
C_METAL    = METAL       # โครงสร้างโลหะ / เพลา (#90A4AE เทาโลหะ)
C_BRUSH    = "#37474F"   # แปรงถ่านคาร์บอน (เทาดำเข้ม)
C_WIRE     = "#D84315"   # ลวดทองแดงเข้ม (ตัดกับลูกศรกระแสสีเหลือง)
C_COMM     = "#FFA726"   # ซีกคอมมิวเทเตอร์ (ส้มทองเหลือง)
C_BAT_POS  = "#EF5350"   # ขั้วบวก / สายไฟบวก
C_BAT_NEG  = "#42A5F5"   # ขั้วลบ / สายไฟลบ

Y_AXIS = np.array([0.0, 1.0, 0.0])

# ── Geometric Constants ──────────────────────────────────────────────────────
R_ARM       = 1.25       # รัศมีขดลวดอาร์เมเจอร์
L_ARM       = 2.70       # ความยาวขดลวดตามแกน Y
Y_ARM_F     = -1.35      # ปลายหน้าขดลวด
Y_ARM_B     =  1.35      # ปลายหลังขดลวด

R_CORE      = 0.80       # รัศมีแกนอาร์เมเจอร์
L_CORE      = 2.50       # ความยาวแกนอาร์เมเจอร์ตามแกน Y

R_COMM      = 0.40       # รัศมีซีกคอมมิวเทเตอร์
L_COMM      = 0.45       # ความยาวคอมมิวเทเตอร์ตามแกน Y
Y_COMM      = -1.90      # ตำแหน่งกึ่งกลางคอมมิวเทเตอร์บนแกน Y
GAP_ANG     = 18.0 * DEGREES  # มุมช่องว่างฉนวนระหว่างสองซีก

Y_POLE_MIN  = -1.35
Y_POLE_MAX  =  1.35

Y_SHAFT_MIN = -3.00
Y_SHAFT_MAX =  2.30

# Solid mesh resolution: (10, 10) as required by cloud benchmark constraint
CYL_RES     = (10, 10)


def build_dc_motor():
    """
    Build solid 3D DC Motor model:
    - 2 solid pole blocks (N at -X, S at +X) with N/S labels
    - Solid yoke / base frame
    - 9 static parallel magnetic field arrows pointing in +X
    - Shaft along Y (solid Cylinder)
    - Armature core along Y (solid Cylinder, translucent during physics beats)
    - Commutator: 2 half-cylinders at Y = -1.90 with visible insulating gap
    - 2 carbon brushes pressing on commutator at +Z and -Z (solid Prisms)
    - DC battery source at Y = -1.90, Z = -1.85 (solid Prism) with wires & supply current arrow
    - Rectangular armature coil rotating on shaft (solid thin Cylinders)
    - Current direction arrows on conductors (offset outside cylinder silhouette)
    - Force arrows on conductors (offset outside cylinder silhouette)
    - Brush spark glow bursts
    """
    # 1. Base / Yoke frame (Solid Prism)
    base_frame = Prism(dimensions=[5.10, 4.40, 0.30]).move_to([0.0, -0.30, -1.60]).set_fill("#263238", 1).set_stroke(width=0)

    # 2. Pole Pieces (N at -X, S at +X - Solid Prisms)
    pole_n_body = Prism(dimensions=[1.00, 2.70, 2.90]).move_to([-2.05, 0.0, 0.0]).set_fill(C_N_POLE, 1).set_stroke(width=0)
    lbl_n = Text("N", font_size=32, color=WHITE).move_to([-2.05, -1.37, 0.0]).rotate(90 * DEGREES, axis=RIGHT)
    lbl_n.set_z_index(20)
    pole_n_group = VGroup(pole_n_body, lbl_n)

    pole_s_body = Prism(dimensions=[1.00, 2.70, 2.90]).move_to([ 2.05, 0.0, 0.0]).set_fill(C_S_POLE, 1).set_stroke(width=0)
    lbl_s = Text("S", font_size=32, color=WHITE).move_to([ 2.05, -1.37, 0.0]).rotate(90 * DEGREES, axis=RIGHT)
    lbl_s.set_z_index(20)
    pole_s_group = VGroup(pole_s_body, lbl_s)

    # 3. Magnetic Field Lines (Static geometry! Drawn ONCE)
    field_lines = VGroup()
    ys_field = [-0.70, 0.0, 0.70]
    zs_field = [-0.55, 0.0, 0.55]
    for yf in ys_field:
        for zf in zs_field:
            arr_fld = arrow3([-1.45, yf, zf], [1.45, yf, zf], color=C_FIELD,
                             thickness=0.016, height=0.18, opacity=0.45)
            field_lines.add(arr_fld)
    field_lines.set_z_index(10)

    # 4. Brushes (Solid Prisms fixed in space at Y = Y_COMM = -1.90)
    brush_top = Prism(dimensions=[0.22, 0.26, 0.30]).move_to([0.0, Y_COMM, R_COMM + 0.15]).set_fill(C_BRUSH, 1).set_stroke(width=0)
    holder_top = Prism(dimensions=[0.14, 0.16, 0.20]).move_to([0.0, Y_COMM, R_COMM + 0.30 + 0.10]).set_fill(C_METAL, 1).set_stroke(width=0)

    brush_bot = Prism(dimensions=[0.22, 0.26, 0.30]).move_to([0.0, Y_COMM, -R_COMM - 0.15]).set_fill(C_BRUSH, 1).set_stroke(width=0)
    holder_bot = Prism(dimensions=[0.14, 0.16, 0.20]).move_to([0.0, Y_COMM, -R_COMM - 0.30 - 0.10]).set_fill(C_METAL, 1).set_stroke(width=0)

    brushes_group = VGroup(brush_top, holder_top, brush_bot, holder_bot)
    brushes_group.set_z_index(5)

    # 5. DC Battery Source & Supply Wires (Solid Prism + lines)
    bat_body = Prism(dimensions=[0.75, 0.35, 0.35]).move_to([0.0, Y_COMM, -1.85]).set_fill("#263238", 1).set_stroke(width=0)
    bat_pos = Prism(dimensions=[0.16, 0.16, 0.12]).move_to([-0.20, Y_COMM, -1.62]).set_fill(C_BAT_POS, 1).set_stroke(width=0)
    bat_neg = Prism(dimensions=[0.16, 0.16, 0.12]).move_to([ 0.20, Y_COMM, -1.62]).set_fill(C_BAT_NEG, 1).set_stroke(width=0)

    lbl_plus = Text("+", font_size=20, color=WHITE).move_to([-0.20, Y_COMM - 0.19, -1.62]).rotate(90 * DEGREES, axis=RIGHT)
    lbl_minus = Text("-", font_size=22, color=WHITE).move_to([ 0.20, Y_COMM - 0.19, -1.62]).rotate(90 * DEGREES, axis=RIGHT)
    lbl_plus.set_z_index(30)
    lbl_minus.set_z_index(30)

    w_pos1 = line3([-0.20, Y_COMM, -1.56], [-1.15, Y_COMM, -1.56], color=C_BAT_POS, thickness=0.030)
    w_pos2 = line3([-1.15, Y_COMM, -1.56], [-1.15, Y_COMM, R_COMM + 0.40], color=C_BAT_POS, thickness=0.030)
    w_pos3 = line3([-1.15, Y_COMM, R_COMM + 0.40], [0.0, Y_COMM, R_COMM + 0.40], color=C_BAT_POS, thickness=0.030)

    w_neg1 = line3([0.20, Y_COMM, -1.56], [0.0, Y_COMM, -1.56], color=C_BAT_NEG, thickness=0.030)
    w_neg2 = line3([0.0, Y_COMM, -1.56], [0.0, Y_COMM, -R_COMM - 0.40], color=C_BAT_NEG, thickness=0.030)

    arr_supply = arrow3([-1.15, Y_COMM, -0.70], [-1.15, Y_COMM, 0.20], color=C_CURRENT,
                        thickness=0.032, height=0.22)
    arr_supply.set_z_index(30)

    battery_group = VGroup(bat_body, bat_pos, bat_neg, lbl_plus, lbl_minus,
                           w_pos1, w_pos2, w_pos3, w_neg1, w_neg2, arr_supply)
    battery_group.set_z_index(5)

    static_mobs = VGroup(base_frame, pole_n_group, pole_s_group, field_lines, brushes_group, battery_group)

    # 6. Moving Rotor Assembly:
    # a. Shaft (Solid Cylinder along Y)
    shaft_len = Y_SHAFT_MAX - Y_SHAFT_MIN
    shaft_center_y = (Y_SHAFT_MAX + Y_SHAFT_MIN) / 2
    shaft = Cylinder(
        radius=0.10, height=shaft_len, direction=Y_AXIS,
        resolution=CYL_RES
    ).move_to([0.0, shaft_center_y, 0.0]).set_fill(C_METAL, 1).set_stroke(width=0)
    shaft.set_z_index(3)

    # b. Armature Core (Solid Cylinder along Y, opacity animated between shots)
    armature_core = Cylinder(
        radius=R_CORE, height=L_CORE, direction=Y_AXIS,
        resolution=CYL_RES
    ).move_to([0.0, 0.0, 0.0]).set_fill(GREY_B, 1).set_stroke(width=0)
    armature_core.set_z_index(2)

    # c. Armature Coil (Solid thin Cylinders)
    cond1 = Cylinder(
        radius=0.06, height=L_ARM, direction=Y_AXIS,
        resolution=CYL_RES
    ).move_to([R_ARM, 0.0, 0.0]).set_fill(C_WIRE, 1).set_stroke(width=0)

    cond2 = Cylinder(
        radius=0.06, height=L_ARM, direction=Y_AXIS,
        resolution=CYL_RES
    ).move_to([-R_ARM, 0.0, 0.0]).set_fill(C_WIRE, 1).set_stroke(width=0)

    turn_back = Cylinder(
        radius=0.06, height=2 * R_ARM, direction=np.array([1.0, 0.0, 0.0]),
        resolution=CYL_RES
    ).move_to([0.0, Y_ARM_B, 0.0]).set_fill(C_WIRE, 1).set_stroke(width=0)

    p_lead1_start = np.array([R_ARM, Y_ARM_F, 0.0])
    p_lead1_end   = np.array([0.0, Y_COMM, R_COMM])
    v_lead1 = p_lead1_end - p_lead1_start
    h_lead1 = np.linalg.norm(v_lead1)
    lead1 = Cylinder(
        radius=0.05, height=h_lead1, direction=v_lead1 / h_lead1,
        resolution=CYL_RES, show_ends=True
    ).move_to((p_lead1_start + p_lead1_end) / 2).set_fill(C_WIRE, 1).set_stroke(width=0)

    p_lead2_start = np.array([-R_ARM, Y_ARM_F, 0.0])
    p_lead2_end   = np.array([0.0, Y_COMM, -R_COMM])
    v_lead2 = p_lead2_end - p_lead2_start
    h_lead2 = np.linalg.norm(v_lead2)
    lead2 = Cylinder(
        radius=0.05, height=h_lead2, direction=v_lead2 / h_lead2,
        resolution=CYL_RES, show_ends=True
    ).move_to((p_lead2_start + p_lead2_end) / 2).set_fill(C_WIRE, 1).set_stroke(width=0)

    loop_group = VGroup(cond1, cond2, turn_back, lead1, lead2)
    loop_group.set_z_index(15)

    # d. Commutator: Two half-cylinders with visible insulating gap
    half_gap = GAP_ANG / 2
    seg1 = Cylinder(
        radius=R_COMM, height=L_COMM, direction=Y_AXIS,
        v_range=[np.pi / 2 + half_gap, 3 * np.pi / 2 - half_gap],
        resolution=CYL_RES, show_ends=False
    ).move_to([0.0, Y_COMM, 0.0]).set_fill(C_COMM, 1).set_stroke(width=0)

    seg2 = Cylinder(
        radius=R_COMM, height=L_COMM, direction=Y_AXIS,
        v_range=[-np.pi / 2 + half_gap, np.pi / 2 - half_gap],
        resolution=CYL_RES, show_ends=False
    ).move_to([0.0, Y_COMM, 0.0]).set_fill(C_COMM, 1).set_stroke(width=0)

    comm_insulator = Cylinder(
        radius=R_COMM - 0.02, height=L_COMM, direction=Y_AXIS,
        resolution=CYL_RES
    ).move_to([0.0, Y_COMM, 0.0]).set_fill("#212121", 1).set_stroke(width=0)

    comm_group = VGroup(seg1, seg2, comm_insulator)
    comm_group.set_z_index(5)

    rotor_group = VGroup(shaft, armature_core, loop_group, comm_group)

    # 7. Moving Current & Force Arrows (Offset outside conductor cylinder)
    curr_arr1 = arrow3([R_ARM + 0.10, -0.40, 0], [R_ARM + 0.10, 0.40, 0], color=C_CURRENT, thickness=0.048, height=0.30)
    curr_arr2 = arrow3([-R_ARM - 0.10, 0.40, 0], [-R_ARM - 0.10, -0.40, 0], color=C_CURRENT, thickness=0.048, height=0.30)
    curr_arr1.set_z_index(50)
    curr_arr2.set_z_index(50)

    force_arr1 = arrow3([R_ARM, 0, -0.07], [R_ARM, 0, -1.22], color=C_FORCE, thickness=0.052, height=0.32)
    force_arr2 = arrow3([-R_ARM, 0, 0.07], [-R_ARM, 0, 1.22], color=C_FORCE, thickness=0.052, height=0.32)
    force_arr1.set_z_index(60)
    force_arr2.set_z_index(60)

    # 8. Commutator Flash / Sparks at Brushes
    spark_top = Dot([0.0, Y_COMM, R_COMM], radius=0.16, color=YELLOW)
    spark_bot = Dot([0.0, Y_COMM, -R_COMM], radius=0.16, color=YELLOW)
    spark_top_halo = Circle(radius=0.32, color=WARN, stroke_width=3.5).rotate(90 * DEGREES, axis=RIGHT).move_to([0.0, Y_COMM, R_COMM])
    spark_bot_halo = Circle(radius=0.32, color=WARN, stroke_width=3.5).rotate(90 * DEGREES, axis=RIGHT).move_to([0.0, Y_COMM, -R_COMM])
    spark_top.set_opacity(0.0)
    spark_bot.set_opacity(0.0)
    spark_top_halo.set_stroke(opacity=0.0)
    spark_bot_halo.set_stroke(opacity=0.0)
    spark_group = VGroup(spark_top, spark_bot, spark_top_halo, spark_bot_halo)
    spark_group.set_z_index(70)

    moving_mobs = VGroup(rotor_group, curr_arr1, curr_arr2, force_arr1, force_arr2, spark_group)

    # ── Master Update Function ───────────────────────────────────────────────
    current_theta = [0.0]

    def update_motor(theta_val, commutator_on=True, show_forces=True, show_current=True,
                     force_opacity=1.0, current_opacity=1.0, flash_intensity=0.0):
        # 1. Rotate rigid rotor geometry (shaft, core, coil, commutator)
        d_th = theta_val - current_theta[0]
        if abs(d_th) > 1e-6:
            rotor_group.rotate(d_th, axis=Y_AXIS, about_point=ORIGIN)
            current_theta[0] = theta_val

        # 2. Conductor positions
        x1 =  R_ARM * np.cos(theta_val)
        z1 = -R_ARM * np.sin(theta_val)
        x2 = -R_ARM * np.cos(theta_val)
        z2 =  R_ARM * np.sin(theta_val)

        # 3. Handedness & Physics:
        # B is along +X: [1, 0, 0]
        # F = I x B
        # When current is +Y: F = (+Y) x (+X) = -Z (down)
        # When current is -Y: F = (-Y) x (+X) = +Z (up)
        if commutator_on:
            half_turn = int(np.floor((theta_val + np.pi / 2) / np.pi))
            if half_turn % 2 == 0:
                dir1 = +1
                dir2 = -1
            else:
                dir1 = -1
                dir2 = +1
        else:
            dir1 = +1
            dir2 = -1

        # 4. Current direction arrows (offset radially outward to avoid cylinder silhouette)
        u1 = np.array([x1, 0.0, z1]) / R_ARM
        u2 = np.array([x2, 0.0, z2]) / R_ARM
        p1_mid = np.array([x1, 0.0, z1]) + u1 * 0.10
        p2_mid = np.array([x2, 0.0, z2]) + u2 * 0.10
        arr_len = 0.40

        if dir1 == +1:
            curr_arr1.put_start_and_end_on(p1_mid + [0, -arr_len, 0], p1_mid + [0, arr_len, 0])
        else:
            curr_arr1.put_start_and_end_on(p1_mid + [0, arr_len, 0], p1_mid + [0, -arr_len, 0])

        if dir2 == +1:
            curr_arr2.put_start_and_end_on(p2_mid + [0, -arr_len, 0], p2_mid + [0, arr_len, 0])
        else:
            curr_arr2.put_start_and_end_on(p2_mid + [0, arr_len, 0], p2_mid + [0, -arr_len, 0])

        # 5. Force arrows (drawn outward from conductor surface to stay fully visible)
        f_len = 1.15
        fz1 = -dir1 * f_len
        fz2 = -dir2 * f_len
        sgn1 = np.sign(fz1)
        sgn2 = np.sign(fz2)

        force_arr1.put_start_and_end_on([x1, 0.0, z1 + sgn1 * 0.07], [x1, 0.0, z1 + fz1])
        force_arr2.put_start_and_end_on([x2, 0.0, z2 + sgn2 * 0.07], [x2, 0.0, z2 + fz2])

        curr_arr1.set_opacity(current_opacity if show_current else 0.0)
        curr_arr2.set_opacity(current_opacity if show_current else 0.0)

        force_arr1.set_opacity(force_opacity if show_forces else 0.0)
        force_arr2.set_opacity(force_opacity if show_forces else 0.0)

        if flash_intensity > 0.01:
            spark_top.set_opacity(flash_intensity)
            spark_bot.set_opacity(flash_intensity)
            spark_top_halo.set_stroke(opacity=flash_intensity * 0.9)
            spark_bot_halo.set_stroke(opacity=flash_intensity * 0.9)
        else:
            spark_top.set_opacity(0.0)
            spark_bot.set_opacity(0.0)
            spark_top_halo.set_stroke(opacity=0.0)
            spark_bot_halo.set_stroke(opacity=0.0)

    update_motor(0.0, commutator_on=True, show_forces=False, show_current=False)

    return {
        "static": static_mobs,
        "moving": moving_mobs,
        "rotor": rotor_group,
        "shaft": shaft,
        "core": armature_core,
        "pole_n": pole_n_group,
        "pole_s": pole_s_group,
        "lbl_n": lbl_n,
        "lbl_s": lbl_s,
        "lbl_plus": lbl_plus,
        "lbl_minus": lbl_minus,
        "field_lines": field_lines,
        "loop": loop_group,
        "cond1": cond1,
        "cond2": cond2,
        "comm": comm_group,
        "brushes": brushes_group,
        "battery": battery_group,
        "curr1": curr_arr1,
        "curr2": curr_arr2,
        "force1": force_arr1,
        "force2": force_arr2,
        "sparks": spark_group,
        "update": update_motor,
    }


class DCMotor3D(SafeThreeDScene):
    """
    Detailed 3D Explainer: มอเตอร์ไฟฟ้า DC ทำงานยังไง (How a DC Motor Works)
    Following the strict 5-shot pedagogy spine:
    - SHOT A: Establish model + name parts + ambient rotation
    - SHOT B: The Force (F = I x B couple, locked camera)
    - SHOT C: Dead point & failure case without commutator (locked end-on camera)
    - SHOT D: Commutator solution (flash + current reversal -> continuous torque)
    - SHOT E: Continuous running (3/4 view) + summary card
    """

    def construct(self):
        # ── INITIAL CAMERA SETUP ─────────────────────────────────────────────
        # 3/4 view: phi about 65 deg, theta about -50 deg
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        # ── SHOT A: Establish + Name the Parts ───────────────────────────────
        main_title = self.hud(title("มอเตอร์ไฟฟ้า DC ทำงานยังไง", size=28))
        cap_a = self.hud(caption_top(
            "มอเตอร์ไฟฟ้า DC: เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานกล โดยอาศัยแรงแม่เหล็กกระทำต่อขดลวด",
            size=19
        ))

        motor = build_dc_motor()

        # Register 3D world labels with SafeThreeDScene layout checker
        self.world_text(motor["lbl_n"], motor["lbl_s"], motor["lbl_plus"], motor["lbl_minus"])

        self.play(
            FadeIn(main_title, shift=DOWN * 0.15),
            FadeIn(cap_a, shift=DOWN * 0.15),
            FadeIn(motor["static"]),
            FadeIn(motor["moving"]),
            run_time=1.4
        )

        # Slow ambient camera rotation allowed in Shot A ONLY
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(2.0)

        # Brief labelling pass (1.5-2.0 s): HUD labels with pointer arrows
        lbl_pole = self.hud(Text("ขั้วแม่เหล็ก N / S", font_size=16, color=WHITE).move_to([-5.05, 1.70, 0]))
        arr_pole = self.hud(Arrow([-3.85, 1.70, 0], [-2.35, 1.45, 0], color=WHITE, stroke_width=2.0, tip_length=0.14))

        lbl_loop = self.hud(Text("ขดลวดอาร์เมเจอร์", font_size=16, color=C_COMM).move_to([-5.05, 0.40, 0]))
        arr_loop = self.hud(Arrow([-3.75, 0.40, 0], [-1.45, 0.35, 0], color=C_COMM, stroke_width=2.0, tip_length=0.14))

        lbl_comm = self.hud(Text("คอมมิวเทเตอร์", font_size=16, color=C_COMM).move_to([-5.05, -0.90, 0]))
        arr_comm = self.hud(Arrow([-3.90, -0.90, 0], [-0.85, -1.25, 0], color=C_COMM, stroke_width=2.0, tip_length=0.14))

        lbl_shaft = self.hud(Text("เพลา (Shaft)", font_size=16, color=C_METAL).move_to([5.05, 1.70, 0]))
        arr_shaft = self.hud(Arrow([4.15, 1.70, 0], [1.85, 1.45, 0], color=C_METAL, stroke_width=2.0, tip_length=0.14))

        lbl_brush = self.hud(Text("แปรงถ่าน (Brushes)", font_size=16, color=GRAYTXT).move_to([5.05, 0.40, 0]))
        arr_brush = self.hud(Arrow([3.80, 0.40, 0], [0.65, -0.45, 0], color=GRAYTXT, stroke_width=2.0, tip_length=0.14))

        lbl_bat = self.hud(Text("แบตเตอรี่ (DC Source)", font_size=16, color=C_BAT_POS).move_to([5.05, -0.90, 0]))
        arr_bat = self.hud(Arrow([3.65, -0.90, 0], [0.75, -1.65, 0], color=C_BAT_POS, stroke_width=2.0, tip_length=0.14))

        labels_hud = VGroup(lbl_pole, arr_pole, lbl_loop, arr_loop, lbl_comm, arr_comm,
                            lbl_shaft, arr_shaft, lbl_brush, arr_brush, lbl_bat, arr_bat)

        # Highlight named parts in the SAME play call
        self.play(
            FadeIn(labels_hud),
            Indicate(motor["pole_n"], color=C_N_POLE, scale_factor=1.05),
            Indicate(motor["pole_s"], color=C_S_POLE, scale_factor=1.05),
            Indicate(motor["loop"], color=C_COMM, scale_factor=1.06),
            Indicate(motor["shaft"], color=WHITE, scale_factor=1.06),
            Indicate(motor["comm"], color=C_COMM, scale_factor=1.08),
            Indicate(motor["brushes"], color=WHITE, scale_factor=1.08),
            Indicate(motor["battery"], color=C_BAT_POS, scale_factor=1.05),
            run_time=1.4
        )
        self.wait(2.0)

        # Fade out labels together and STOP ambient rotation
        self.play(FadeOut(labels_hud), run_time=0.6)
        self.stop_ambient_camera_rotation()

        # ── SHOT B: The Force (F = I x B Couple) ─────────────────────────────
        # Lock camera at angle where B (+X), I (along Y), F (along Z) are all distinct
        # Smoothly fade armature core to see-through (0.28) so coil and arrows remain fully visible
        self.move_camera(
            phi=68 * DEGREES, theta=-40 * DEGREES,
            added_anims=[motor["core"].animate.set_opacity(0.28)],
            run_time=1.2
        )
        self.wait(0.3)

        # Caption swap: Sequential!
        self.play(FadeOut(cap_a), run_time=0.3)
        cap_b1 = self.hud(caption_top(
            "เมื่อกระแสไหลผ่านตัวนำในสนามแม่เหล็ก จะเกิดแรง F = I × B ตั้งฉากกับทั้งกระแสและสนาม",
            size=19
        ))
        self.play(FadeIn(cap_b1, shift=DOWN * 0.15), run_time=0.5)

        # Labels for current and force in 3D world (raised z_index to prevent occlusion)
        lbl_i1 = Text("I", font_size=24, color=C_CURRENT).move_to([R_ARM, 0.15, 0.35]).rotate(90 * DEGREES, axis=RIGHT)
        lbl_f1 = Text("F", font_size=24, color=C_FORCE).move_to([R_ARM, 0.0, -1.35]).rotate(90 * DEGREES, axis=RIGHT)
        lbl_i2 = Text("I", font_size=24, color=C_CURRENT).move_to([-R_ARM, -0.15, -0.35]).rotate(90 * DEGREES, axis=RIGHT)
        lbl_f2 = Text("F", font_size=24, color=C_FORCE).move_to([-R_ARM, 0.0, 1.35]).rotate(90 * DEGREES, axis=RIGHT)
        for lbl in (lbl_i1, lbl_f1, lbl_i2, lbl_f2):
            lbl.set_z_index(80)
        self.world_text(lbl_i1, lbl_f1, lbl_i2, lbl_f2)

        # 1. Conductor 1 (+X): current +Y -> force -Z (pushed down)
        motor["update"](0.0, commutator_on=True, show_forces=True, show_current=True,
                        force_opacity=1.0, current_opacity=1.0)
        motor["curr2"].set_opacity(0.0)
        motor["force2"].set_opacity(0.0)

        self.play(
            Indicate(motor["cond1"], color=C_CURRENT, scale_factor=1.08),
            motor["curr1"].animate.set_opacity(1.0),
            FadeIn(lbl_i1),
            run_time=0.9
        )
        self.play(
            motor["force1"].animate.set_opacity(1.0),
            FadeIn(lbl_f1),
            run_time=0.9
        )
        self.wait(1.5)

        self.play(FadeOut(cap_b1), run_time=0.3)
        cap_b2 = self.hud(caption_top(
            "ตัวนำฝั่งขวา (+X): กระแสพุ่งไปข้างหน้า (+Y)  →  แรงแม่เหล็กผลักลง (-Z)",
            size=19, color=WHITE
        ))
        self.play(FadeIn(cap_b2, shift=DOWN * 0.15), run_time=0.5)
        self.wait(1.4)

        # 2. Conductor 2 (-X): current -Y -> force +Z (pushed up)
        self.play(
            Indicate(motor["cond2"], color=C_CURRENT, scale_factor=1.08),
            motor["curr2"].animate.set_opacity(1.0),
            motor["force2"].animate.set_opacity(1.0),
            FadeIn(lbl_i2),
            FadeIn(lbl_f2),
            run_time=1.0
        )

        self.play(FadeOut(cap_b2), run_time=0.3)
        cap_b3 = self.hud(caption_top(
            "ตัวนำฝั่งซ้าย (-X): กระแสไหลย้อนกลับ (-Y)  →  แรงผลักขึ้น (+Z) เกิด 'แรงคู่ควบ' หมุนเพลา",
            size=19, color=OK
        ))
        self.play(FadeIn(cap_b3, shift=DOWN * 0.15), run_time=0.5)

        # Show torque indicator (radius 1.40 loops around the armature, visible from all angles)
        torque_arc = Arc(radius=1.40, start_angle=-30 * DEGREES, angle=140 * DEGREES,
                         color=C_TORQUE, stroke_width=4.5)
        torque_arc.rotate(90 * DEGREES, axis=RIGHT).move_to([0, 0.4, 0])
        torque_arc.set_z_index(90)
        self.play(Create(torque_arc), run_time=0.9)
        self.wait(2.0)
        self.play(
            FadeOut(torque_arc),
            FadeOut(lbl_i1), FadeOut(lbl_f1),
            FadeOut(lbl_i2), FadeOut(lbl_f2),
            run_time=0.5
        )

        # ── SHOT C: Dead Point & The Problem (Failure without Commutator) ─────
        # Lock camera looking straight down shaft axis Y (end-on view: phi=89.9, theta=-90)
        self.move_camera(phi=89.9 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        self.wait(0.3)

        # Make sure both force arrows and current arrows are visible at theta = 0
        motor["update"](0.0, commutator_on=True, show_forces=True, show_current=True,
                        force_opacity=1.0, current_opacity=1.0)

        # VERIFICATION FRAME BEAT: Max torque position in end-on view
        # Screen horizontal = X (field points right, N left, S right)
        # Screen vertical = Z (forces point straight up on left, straight down on right)
        self.play(FadeOut(cap_b3), run_time=0.3)
        cap_c1 = self.hud(caption_top(
            "มุมมองตามแนวเพลา: ระนาบนอน แรงคู่ควบมีแขนโมเมนต์ยาวสุด  →  เกิดทอร์กสูงสุด",
            size=19, color=WHITE
        ))
        self.play(FadeIn(cap_c1, shift=DOWN * 0.15), run_time=0.5)
        self.wait(2.5)  # Steady frame for verification!

        # Rotate loop to Dead Point (theta = pi/2: conductors at top +Z and bottom -Z)
        self.play(FadeOut(cap_c1), run_time=0.3)
        cap_c2 = self.hud(caption_top(
            "เมื่อหมุนถึงแนวตั้ง (Dead Point): แรงทั้งสองชี้เข้าหาแกนเพลา  →  ทอร์กเป็นศูนย์!",
            size=19, color=WARN
        ))
        self.play(FadeIn(cap_c2, shift=DOWN * 0.15), run_time=0.5)

        # Animate rotation to dead point
        th_tracker = ValueTracker(0.0)

        def upd_motor_normal(_m):
            th = th_tracker.get_value()
            motor["update"](th, commutator_on=True, show_forces=True, show_current=True,
                            force_opacity=1.0, current_opacity=1.0)

        motor["shaft"].add_updater(upd_motor_normal)
        self.play(th_tracker.animate.set_value(np.pi / 2), run_time=2.4, rate_func=smooth)
        motor["shaft"].remove_updater(upd_motor_normal)
        motor["update"](np.pi / 2, commutator_on=True, show_forces=True, show_current=True,
                        force_opacity=1.0, current_opacity=1.0)
        self.wait(2.0)

        # Show failure case: What happens WITHOUT a commutator?
        self.play(FadeOut(cap_c2), run_time=0.3)
        cap_c3 = self.hud(caption_top(
            "กรณีไม่มีคอมมิวเทเตอร์: ตัวนำหมุนเลยจุดบอด แต่กระแสไม่กลับทิศ  →  ทอร์กกลับทิศผลักย้อนกลับ!",
            size=18, color=WARN
        ))
        self.play(FadeIn(cap_c3, shift=DOWN * 0.15), run_time=0.5)

        # Animate overshoot and damped rocking oscillation (stall)
        def upd_motor_fail(_m):
            th = th_tracker.get_value()
            motor["update"](th, commutator_on=False, show_forces=True, show_current=True,
                            force_opacity=1.0, current_opacity=1.0)

        motor["shaft"].add_updater(upd_motor_fail)

        # Damped oscillation around dead point pi/2
        self.play(th_tracker.animate.set_value(np.pi / 2 + 32 * DEGREES), run_time=0.9, rate_func=smooth)
        self.play(th_tracker.animate.set_value(np.pi / 2 - 20 * DEGREES), run_time=0.9, rate_func=smooth)
        self.play(th_tracker.animate.set_value(np.pi / 2 + 10 * DEGREES), run_time=0.8, rate_func=smooth)
        self.play(th_tracker.animate.set_value(np.pi / 2), run_time=0.8, rate_func=smooth)

        motor["shaft"].remove_updater(upd_motor_fail)
        motor["update"](np.pi / 2, commutator_on=False, show_forces=True, show_current=True,
                        force_opacity=1.0, current_opacity=1.0)

        self.play(FadeOut(cap_c3), run_time=0.3)
        cap_c4 = self.hud(caption_top(
            "ผลลัพธ์: ขดลวดแกว่งไปมาแล้วหยุดนิ่ง (Stall) — ไม่สามารถหมุนต่อเนื่องเป็นวงกลมได้",
            size=19, color=WARN
        ))
        self.play(FadeIn(cap_c4, shift=DOWN * 0.15), run_time=0.5)
        self.wait(2.5)

        # ── SHOT D: The Commutator Fix ───────────────────────────────────────
        # KEEP same end-on camera as Shot C so viewer stays oriented
        self.play(FadeOut(cap_c4), run_time=0.3)
        cap_d1 = self.hud(caption_top(
            "ทางแก้คือ 'คอมมิวเทเตอร์': แหวนผ่าซีก 2 ชิ้น จะสลับขั้วกระแสที่จุดบอดพอดีเป๊ะ!",
            size=19, color=OK
        ))
        self.play(FadeIn(cap_d1, shift=DOWN * 0.15), run_time=0.5)

        # Highlight commutator segments, insulating gap, and brushes
        self.play(
            Indicate(motor["comm"], color=YELLOW, scale_factor=1.12),
            Indicate(motor["brushes"], color=WHITE, scale_factor=1.10),
            run_time=1.4
        )
        self.wait(1.2)

        # Reset loop to just before dead point (45 degrees before pi/2)
        th_tracker.set_value(np.pi / 4)
        motor["update"](np.pi / 4, commutator_on=True, show_forces=True, show_current=True,
                        force_opacity=1.0, current_opacity=1.0)
        self.wait(0.6)

        # Rotate slowly through the dead point
        # At exact instant brushes cross gap (theta = pi/2), trigger bright FLASH and flip arrows
        def upd_motor_flip(_m):
            th = th_tracker.get_value()
            diff = abs(th - np.pi / 2)
            flash = float(np.exp(- (diff / 0.08)**2)) if diff < 0.15 else 0.0
            motor["update"](th, commutator_on=True, show_forces=True, show_current=True,
                            force_opacity=1.0, current_opacity=1.0, flash_intensity=flash)

        motor["shaft"].add_updater(upd_motor_flip)

        # Step 1: approach and cross dead point with flash
        self.play(th_tracker.animate.set_value(np.pi / 2 + 0.02), run_time=2.2, rate_func=linear)

        self.play(FadeOut(cap_d1), run_time=0.3)
        cap_d2 = self.hud(caption_top(
            "กระแสถูกสลับทิศทันที! แรงบนตัวนำเปลี่ยนทิศ  →  เกิดทอร์กผลักไปข้างหน้าอย่างต่อเนื่อง",
            size=18, color=OK
        ))
        self.play(FadeIn(cap_d2, shift=DOWN * 0.15), run_time=0.5)

        # Step 2: continue forward past dead point with positive driving torque
        self.play(th_tracker.animate.set_value(np.pi), run_time=2.4, rate_func=smooth)
        motor["shaft"].remove_updater(upd_motor_flip)
        motor["update"](np.pi, commutator_on=True, show_forces=True, show_current=True,
                        force_opacity=1.0, current_opacity=1.0)
        self.wait(2.0)

        # ── SHOT E: Continuous Running + Summary Card ────────────────────────
        # Return to 3/4 view (phi = 65 deg, theta = -50 deg)
        # Restore armature core to fully opaque solid (1.0)
        self.move_camera(
            phi=65 * DEGREES, theta=-50 * DEGREES,
            added_anims=[motor["core"].animate.set_opacity(1.0)],
            run_time=1.8
        )
        self.wait(0.3)

        self.play(FadeOut(cap_d2), run_time=0.3)
        cap_e = self.hud(caption_top(
            "การทำงานต่อเนื่อง: คอมมิวเทเตอร์สลับกระแสทุกๆ ครึ่งรอบ ทำให้เพลาหมุนทิศเดิมไม่สิ้นสุด",
            size=19, color=WHITE
        ))
        self.play(FadeIn(cap_e, shift=DOWN * 0.15), run_time=0.5)

        # Continuous spinning: 3.5 full revolutions with commutator flash every half-turn
        def upd_motor_spin(_m):
            th = th_tracker.get_value()
            phase = (th - np.pi / 2) % np.pi
            flash_dist = min(phase, np.pi - phase)
            flash = float(np.exp(- (flash_dist / 0.09)**2)) if flash_dist < 0.18 else 0.0
            motor["update"](th, commutator_on=True, show_forces=True, show_current=True,
                            force_opacity=1.0, current_opacity=1.0, flash_intensity=flash)

        motor["shaft"].add_updater(upd_motor_spin)

        # Spin smoothly for 7*pi radians (3.5 full turns) over 11.5 seconds
        start_th = th_tracker.get_value()
        self.play(
            th_tracker.animate.set_value(start_th + 7 * np.pi),
            run_time=11.5,
            rate_func=linear
        )
        self.wait(1.0)
        motor["shaft"].remove_updater(upd_motor_spin)

        # Transition to Closing Summary Card
        self.play(
            FadeOut(cap_e),
            FadeOut(motor["static"]),
            FadeOut(motor["moving"]),
            FadeOut(main_title),
            run_time=1.0
        )

        title_close = self.hud(title("สรุปหลักการทำงาน: มอเตอร์ไฟฟ้า DC", size=26))

        summary_box = RoundedRectangle(
            width=11.4, height=3.5, corner_radius=0.18,
            stroke_color=OK, stroke_width=2.5,
            fill_color="#1A2126", fill_opacity=0.94
        ).move_to([0, 0.45, 0])

        t1 = fit_width(
            Text("1. กระแสในขดลวด + สนามแม่เหล็ก  →  เกิดแรงแม่เหล็ก (F = I × B)",
                 font_size=18, color=OK).move_to(summary_box.get_top() + DOWN * 0.60),
            10.6
        )
        t2 = fit_width(
            Text("2. แรงสองฝั่งมีทิศตรงข้ามกัน (แรงคู่ควบ)  →  สร้างแรงบิด (ทอร์ก) ให้เพลาหมุน",
                 font_size=18, color=WHITE).next_to(t1, DOWN, buff=0.35),
            10.6
        )
        t3 = fit_width(
            Text("3. คอมมิวเทเตอร์สลับทิศกระแสทุกครึ่งรอบ  →  ทอร์กผลักทิศเดิม เพลาจึงหมุนต่อเนื่อง",
                 font_size=18, color=CURRENT).next_to(t2, DOWN, buff=0.35),
            10.6
        )

        summary_grp = self.hud(VGroup(summary_box, t1, t2, t3))

        self.play(
            FadeIn(title_close, shift=DOWN * 0.15),
            FadeIn(summary_grp, shift=UP * 0.15),
            run_time=1.0
        )
        self.wait(5.5)

        # Clean complete scene exit
        self.fade_out_all(run_time=0.9)
