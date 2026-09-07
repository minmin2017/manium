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
C_CURRENT  = CURRENT     # กระแส I (#FFB300 เหลืองอำพัน)
C_FORCE    = FORCE       # แรง F (#66BB6A เขียวสว่าง)
C_TORQUE   = TORQUE      # ทอร์ก tau (#AB47BC ม่วง)
C_METAL    = METAL       # โครงสร้างโลหะ / เพลา (#90A4AE เทาโลหะ)
C_BRUSH    = "#37474F"   # แปรงถ่านคาร์บอน (เทาดำเข้ม)
C_COPPER   = "#FFA726"   # ทองแดง / ซีกคอมมิวเทเตอร์ (ส้มทองแดง)
C_BAT_POS  = "#EF5350"   # ขั้วบวก / สายไฟบวก
C_BAT_NEG  = "#42A5F5"   # ขั้วลบ / สายไฟลบ

# ── Geometric Constants ──────────────────────────────────────────────────────
R_ARM       = 1.25       # รัศมีขดลวดอาร์เมเจอร์
L_ARM       = 2.70       # ความยาวขดลวดตามแกน Y
Y_ARM_F     = -1.35      # ปลายหน้าขดลวด
Y_ARM_B     =  1.35      # ปลายหลังขดลวด

R_COMM      = 0.40       # รัศมีซีกคอมมิวเทเตอร์
Y_COMM      = -1.90      # ตำแหน่งกึ่งกลางคอมมิวเทเตอร์บนแกน Y
GAP_ANG     = 22.0 * DEGREES  # มุมช่องว่างฉนวนระหว่างสองซีก

R_POLE_IN   = 1.60       # รัศมีผิวด้านในขั้วแม่เหล็ก (โค้งเว้าเข้าหาแกน)
Y_POLE_MIN  = -1.35
Y_POLE_MAX  =  1.35

Y_SHAFT_MIN = -3.00
Y_SHAFT_MAX =  2.30


def build_dc_motor():
    """
    Build detailed 3D DC Motor model:
    - 2 curved pole shoes (N at -X, S at +X) with N/S labels
    - 9 static parallel magnetic field arrows pointing in +X
    - Shaft along Y with 2 end bearing pedestals and base rails
    - Commutator: 2 split half-rings on shaft at Y = -1.90 with insulating gap
    - 2 fixed carbon brushes pressing on commutator at +Z and -Z
    - DC battery source at Y = -1.90, Z = -1.45 with wires & supply current arrow
    - Rectangular armature loop rotating on shaft
    - Current direction arrows on the two long conductors
    - Force arrows on the conductors
    - Brush spark glow bursts
    """
    static_mobs = VGroup()
    moving_mobs = VGroup()

    # 1. Shaft and Bearings
    shaft = line3([0, Y_SHAFT_MIN, 0], [0, Y_SHAFT_MAX, 0], color=C_METAL, thickness=0.055)
    static_mobs.add(shaft)

    # Bearings at front and rear
    y_bearings = [-2.60, 1.95]
    for y_b in y_bearings:
        b_ring = Circle(radius=0.28, color=C_METAL, stroke_width=2.5)
        b_ring.rotate(90 * DEGREES, axis=RIGHT).move_to([0, y_b, 0])
        leg_l = line3([0, y_b, -0.28], [-0.55, y_b, -1.20], color=C_METAL, thickness=0.035)
        leg_r = line3([0, y_b, -0.28], [ 0.55, y_b, -1.20], color=C_METAL, thickness=0.035)
        foot  = line3([-0.65, y_b, -1.20], [0.65, y_b, -1.20], color=C_METAL, thickness=0.045)
        static_mobs.add(b_ring, leg_l, leg_r, foot)

    # Base rails
    rail_l = line3([-0.65, -2.75, -1.20], [-0.65, 2.10, -1.20], color=C_METAL, thickness=0.030)
    rail_r = line3([ 0.65, -2.75, -1.20], [ 0.65, 2.10, -1.20], color=C_METAL, thickness=0.030)
    static_mobs.add(rail_l, rail_r)

    # 2. Curved Pole Shoes (N at -X, S at +X)
    # N Pole (Red, -X side)
    n_pts_in_f = [
        np.array([R_POLE_IN * np.cos(a), Y_POLE_MIN, R_POLE_IN * np.sin(a)])
        for a in np.linspace(145 * DEGREES, 215 * DEGREES, 16)
    ]
    n_pts_in_b = [
        np.array([R_POLE_IN * np.cos(a), Y_POLE_MAX, R_POLE_IN * np.sin(a)])
        for a in np.linspace(145 * DEGREES, 215 * DEGREES, 16)
    ]
    arc_n_f = VMobject(color=C_N_POLE, stroke_width=3).set_points_smoothly(n_pts_in_f)
    arc_n_b = VMobject(color=C_N_POLE, stroke_width=2, stroke_opacity=0.6).set_points_smoothly(n_pts_in_b)

    x_back_n = -2.60
    z_top_n  = R_POLE_IN * np.sin(145 * DEGREES)   # ~ +0.918
    z_bot_n  = R_POLE_IN * np.sin(215 * DEGREES)   # ~ -0.918
    x_tip_top_n = R_POLE_IN * np.cos(145 * DEGREES) # ~ -1.31
    x_tip_bot_n = R_POLE_IN * np.cos(215 * DEGREES) # ~ -1.31

    n_face_f = Polygon(
        [x_tip_top_n, Y_POLE_MIN, z_top_n],
        [x_back_n,    Y_POLE_MIN, z_top_n],
        [x_back_n,    Y_POLE_MIN, z_bot_n],
        [x_tip_bot_n, Y_POLE_MIN, z_bot_n],
        *[np.array([R_POLE_IN * np.cos(a), Y_POLE_MIN, R_POLE_IN * np.sin(a)])
          for a in np.linspace(215 * DEGREES, 145 * DEGREES, 12)],
        color=C_N_POLE, fill_color=C_N_POLE, fill_opacity=0.35, stroke_width=2.5
    )
    n_face_b = Polygon(
        [x_tip_top_n, Y_POLE_MAX, z_top_n],
        [x_back_n,    Y_POLE_MAX, z_top_n],
        [x_back_n,    Y_POLE_MAX, z_bot_n],
        [x_tip_bot_n, Y_POLE_MAX, z_bot_n],
        color=C_N_POLE, stroke_width=1.5, stroke_opacity=0.45, fill_opacity=0.0
    )
    edge_n1 = line3([x_back_n, Y_POLE_MIN, z_top_n], [x_back_n, Y_POLE_MAX, z_top_n], color=C_N_POLE, thickness=0.02)
    edge_n2 = line3([x_back_n, Y_POLE_MIN, z_bot_n], [x_back_n, Y_POLE_MAX, z_bot_n], color=C_N_POLE, thickness=0.02)
    edge_n3 = line3([x_tip_top_n, Y_POLE_MIN, z_top_n], [x_tip_top_n, Y_POLE_MAX, z_top_n], color=C_N_POLE, thickness=0.02)
    edge_n4 = line3([x_tip_bot_n, Y_POLE_MIN, z_bot_n], [x_tip_bot_n, Y_POLE_MAX, z_bot_n], color=C_N_POLE, thickness=0.02)

    lbl_n = Text("N", font_size=32, color=WHITE).move_to([-2.05, Y_POLE_MIN - 0.02, 0.0])
    lbl_n.rotate(90 * DEGREES, axis=RIGHT)

    pole_n_group = VGroup(arc_n_f, arc_n_b, n_face_f, n_face_b, edge_n1, edge_n2, edge_n3, edge_n4, lbl_n)
    static_mobs.add(pole_n_group)

    # S Pole (Blue, +X side)
    s_pts_in_f = [
        np.array([R_POLE_IN * np.cos(a), Y_POLE_MIN, R_POLE_IN * np.sin(a)])
        for a in np.linspace(-35 * DEGREES, 35 * DEGREES, 16)
    ]
    s_pts_in_b = [
        np.array([R_POLE_IN * np.cos(a), Y_POLE_MAX, R_POLE_IN * np.sin(a)])
        for a in np.linspace(-35 * DEGREES, 35 * DEGREES, 16)
    ]
    arc_s_f = VMobject(color=C_S_POLE, stroke_width=3).set_points_smoothly(s_pts_in_f)
    arc_s_b = VMobject(color=C_S_POLE, stroke_width=2, stroke_opacity=0.6).set_points_smoothly(s_pts_in_b)

    x_back_s = 2.60
    z_top_s  = R_POLE_IN * np.sin(35 * DEGREES)    # ~ +0.918
    z_bot_s  = R_POLE_IN * np.sin(-35 * DEGREES)   # ~ -0.918
    x_tip_top_s = R_POLE_IN * np.cos(35 * DEGREES)  # ~ +1.31
    x_tip_bot_s = R_POLE_IN * np.cos(-35 * DEGREES) # ~ +1.31

    s_face_f = Polygon(
        [x_tip_top_s, Y_POLE_MIN, z_top_s],
        [x_back_s,    Y_POLE_MIN, z_top_s],
        [x_back_s,    Y_POLE_MIN, z_bot_s],
        [x_tip_bot_s, Y_POLE_MIN, z_bot_s],
        *[np.array([R_POLE_IN * np.cos(a), Y_POLE_MIN, R_POLE_IN * np.sin(a)])
          for a in np.linspace(-35 * DEGREES, 35 * DEGREES, 12)],
        color=C_S_POLE, fill_color=C_S_POLE, fill_opacity=0.35, stroke_width=2.5
    )
    s_face_b = Polygon(
        [x_tip_top_s, Y_POLE_MAX, z_top_s],
        [x_back_s,    Y_POLE_MAX, z_top_s],
        [x_back_s,    Y_POLE_MAX, z_bot_s],
        [x_tip_bot_s, Y_POLE_MAX, z_bot_s],
        color=C_S_POLE, stroke_width=1.5, stroke_opacity=0.45, fill_opacity=0.0
    )
    edge_s1 = line3([x_back_s, Y_POLE_MIN, z_top_s], [x_back_s, Y_POLE_MAX, z_top_s], color=C_S_POLE, thickness=0.02)
    edge_s2 = line3([x_back_s, Y_POLE_MIN, z_bot_s], [x_back_s, Y_POLE_MAX, z_bot_s], color=C_S_POLE, thickness=0.02)
    edge_s3 = line3([x_tip_top_s, Y_POLE_MIN, z_top_s], [x_tip_top_s, Y_POLE_MAX, z_top_s], color=C_S_POLE, thickness=0.02)
    edge_s4 = line3([x_tip_bot_s, Y_POLE_MIN, z_bot_s], [x_tip_bot_s, Y_POLE_MAX, z_bot_s], color=C_S_POLE, thickness=0.02)

    lbl_s = Text("S", font_size=32, color=WHITE).move_to([2.05, Y_POLE_MIN - 0.02, 0.0])
    lbl_s.rotate(90 * DEGREES, axis=RIGHT)

    pole_s_group = VGroup(arc_s_f, arc_s_b, s_face_f, s_face_b, edge_s1, edge_s2, edge_s3, edge_s4, lbl_s)
    static_mobs.add(pole_s_group)

    # 3. Magnetic Field Lines (Static geometry! Drawn ONCE)
    field_lines = VGroup()
    ys_field = [-0.70, 0.0, 0.70]
    zs_field = [-0.55, 0.0, 0.55]
    for yf in ys_field:
        for zf in zs_field:
            arr_fld = arrow3([-1.22, yf, zf], [1.22, yf, zf], color=C_FIELD,
                             thickness=0.016, height=0.18, opacity=0.45)
            field_lines.add(arr_fld)
    static_mobs.add(field_lines)

    # 4. Brushes (Fixed in space at Y = Y_COMM = -1.90)
    brush_top = Rectangle(
        width=0.22, height=0.34, color=C_METAL,
        fill_color=C_BRUSH, fill_opacity=0.92, stroke_width=2.0
    ).rotate(90 * DEGREES, axis=RIGHT).move_to([0.0, Y_COMM, R_COMM + 0.17])
    holder_top = line3([0.0, Y_COMM, R_COMM + 0.34], [0.0, Y_COMM, R_COMM + 0.52], color=C_METAL, thickness=0.035)

    brush_bot = Rectangle(
        width=0.22, height=0.34, color=C_METAL,
        fill_color=C_BRUSH, fill_opacity=0.92, stroke_width=2.0
    ).rotate(90 * DEGREES, axis=RIGHT).move_to([0.0, Y_COMM, -R_COMM - 0.17])
    holder_bot = line3([0.0, Y_COMM, -R_COMM - 0.34], [0.0, Y_COMM, -R_COMM - 0.52], color=C_METAL, thickness=0.035)

    brushes_group = VGroup(brush_top, holder_top, brush_bot, holder_bot)
    static_mobs.add(brushes_group)

    # 5. DC Battery Source & Supply Wires
    y_bat = Y_COMM
    z_bat_pos = -1.35
    z_bat_neg = -1.48

    bat_plate_pos = line3([-0.30, y_bat, z_bat_pos], [0.30, y_bat, z_bat_pos], color=C_BAT_POS, thickness=0.035)
    bat_plate_neg = line3([-0.18, y_bat, z_bat_neg], [0.18, y_bat, z_bat_neg], color=C_BAT_NEG, thickness=0.065)

    lbl_plus = Text("+", font_size=18, color=C_BAT_POS).move_to([-0.45, y_bat - 0.02, z_bat_pos]).rotate(90 * DEGREES, axis=RIGHT)
    lbl_minus = Text("-", font_size=20, color=C_BAT_NEG).move_to([-0.45, y_bat - 0.02, z_bat_neg]).rotate(90 * DEGREES, axis=RIGHT)

    w_pos1 = line3([-0.30, y_bat, z_bat_pos], [-1.00, y_bat, z_bat_pos], color=C_BAT_POS, thickness=0.025)
    w_pos2 = line3([-1.00, y_bat, z_bat_pos], [-1.00, y_bat, R_COMM + 0.52], color=C_BAT_POS, thickness=0.025)
    w_pos3 = line3([-1.00, y_bat, R_COMM + 0.52], [0.0, y_bat, R_COMM + 0.52], color=C_BAT_POS, thickness=0.025)

    w_neg1 = line3([0.0, y_bat, z_bat_neg], [0.0, y_bat, -R_COMM - 0.52], color=C_BAT_NEG, thickness=0.025)

    arr_supply = arrow3([-1.00, y_bat, -0.65], [-1.00, y_bat, 0.25], color=C_CURRENT,
                        thickness=0.030, height=0.22)

    battery_group = VGroup(bat_plate_pos, bat_plate_neg, lbl_plus, lbl_minus,
                           w_pos1, w_pos2, w_pos3, w_neg1, arr_supply)
    static_mobs.add(battery_group)

    # 6. Moving Armature Loop (Rectangular wire on shaft)
    wire_cond1 = line3([R_ARM, Y_ARM_F, 0], [R_ARM, Y_ARM_B, 0], color=C_COPPER, thickness=0.060)
    wire_cond2 = line3([-R_ARM, Y_ARM_F, 0], [-R_ARM, Y_ARM_B, 0], color=C_COPPER, thickness=0.060)
    wire_back  = line3([R_ARM, Y_ARM_B, 0], [-R_ARM, Y_ARM_B, 0], color=C_COPPER, thickness=0.050)
    wire_lead1 = line3([R_ARM, Y_ARM_F, 0], [0, Y_COMM, R_COMM], color=C_COPPER, thickness=0.040)
    wire_lead2 = line3([-R_ARM, Y_ARM_F, 0], [0, Y_COMM, -R_COMM], color=C_COPPER, thickness=0.040)

    loop_group = VGroup(wire_cond1, wire_cond2, wire_back, wire_lead1, wire_lead2)
    moving_mobs.add(loop_group)

    # 7. Moving Commutator Half-Rings (Segments 1 & 2)
    seg1_f = VMobject(color=C_COPPER, stroke_width=5)
    seg1_b = VMobject(color=C_COPPER, stroke_width=3, stroke_opacity=0.7)
    seg2_f = VMobject(color=C_COPPER, stroke_width=5)
    seg2_b = VMobject(color=C_COPPER, stroke_width=3, stroke_opacity=0.7)
    gap_edge1a = line3([0, Y_COMM - 0.12, 0], [0, Y_COMM + 0.12, 0], color=C_COPPER, thickness=0.02)
    gap_edge1b = line3([0, Y_COMM - 0.12, 0], [0, Y_COMM + 0.12, 0], color=C_COPPER, thickness=0.02)
    gap_edge2a = line3([0, Y_COMM - 0.12, 0], [0, Y_COMM + 0.12, 0], color=C_COPPER, thickness=0.02)
    gap_edge2b = line3([0, Y_COMM - 0.12, 0], [0, Y_COMM + 0.12, 0], color=C_COPPER, thickness=0.02)

    comm_group = VGroup(seg1_f, seg1_b, seg2_f, seg2_b,
                        gap_edge1a, gap_edge1b, gap_edge2a, gap_edge2b)
    moving_mobs.add(comm_group)

    # 8. Moving Current-Direction Arrows ON the Long Conductors
    curr_arr1 = arrow3([R_ARM, -0.35, 0], [R_ARM, 0.35, 0], color=C_CURRENT, thickness=0.038, height=0.24)
    curr_arr2 = arrow3([-R_ARM, 0.35, 0], [-R_ARM, -0.35, 0], color=C_CURRENT, thickness=0.038, height=0.24)
    moving_mobs.add(curr_arr1, curr_arr2)

    # 9. Moving Force Arrows ON the Long Conductors
    force_arr1 = arrow3([R_ARM, 0, 0], [R_ARM, 0, -1.10], color=C_FORCE, thickness=0.042, height=0.26)
    force_arr2 = arrow3([-R_ARM, 0, 0], [-R_ARM, 0, 1.10], color=C_FORCE, thickness=0.042, height=0.26)
    moving_mobs.add(force_arr1, force_arr2)

    # 10. Commutator Flash / Sparks at Brushes
    spark_top = Dot([0.0, Y_COMM, R_COMM], radius=0.15, color=YELLOW)
    spark_bot = Dot([0.0, Y_COMM, -R_COMM], radius=0.15, color=YELLOW)
    spark_top_halo = Circle(radius=0.30, color=WARN, stroke_width=3).rotate(90 * DEGREES, axis=RIGHT).move_to([0.0, Y_COMM, R_COMM])
    spark_bot_halo = Circle(radius=0.30, color=WARN, stroke_width=3).rotate(90 * DEGREES, axis=RIGHT).move_to([0.0, Y_COMM, -R_COMM])
    spark_top.set_opacity(0.0)
    spark_bot.set_opacity(0.0)
    spark_top_halo.set_stroke(opacity=0.0)
    spark_bot_halo.set_stroke(opacity=0.0)
    spark_group = VGroup(spark_top, spark_bot, spark_top_halo, spark_bot_halo)
    moving_mobs.add(spark_group)

    # ── Update Function ──────────────────────────────────────────────────────
    def update_motor(theta_val, commutator_on=True, show_forces=True, force_opacity=1.0, flash_intensity=0.0):
        """
        Update positions of all moving parts from master rotation angle theta_val.
        - theta_val = 0: Conductor 1 at +X, Conductor 2 at -X (max torque position)
        - theta_val = pi/2: Conductor 1 at -Z (bottom), Conductor 2 at +Z (top) (dead point)
        """
        x1 =  R_ARM * np.cos(theta_val)
        z1 = -R_ARM * np.sin(theta_val)
        x2 = -R_ARM * np.cos(theta_val)
        z2 =  R_ARM * np.sin(theta_val)

        p1_f = np.array([x1, Y_ARM_F, z1])
        p1_b = np.array([x1, Y_ARM_B, z1])
        p2_f = np.array([x2, Y_ARM_F, z2])
        p2_b = np.array([x2, Y_ARM_B, z2])

        wire_cond1.put_start_and_end_on(p1_f, p1_b)
        wire_cond2.put_start_and_end_on(p2_f, p2_b)
        wire_back.put_start_and_end_on(p1_b, p2_b)

        ang_seg1 = np.pi / 2 - theta_val
        ang_seg2 = 3 * np.pi / 2 - theta_val
        p_comm1 = np.array([R_COMM * np.cos(ang_seg1), Y_COMM, R_COMM * np.sin(ang_seg1)])
        p_comm2 = np.array([R_COMM * np.cos(ang_seg2), Y_COMM, R_COMM * np.sin(ang_seg2)])

        wire_lead1.put_start_and_end_on(p1_f, p_comm1)
        wire_lead2.put_start_and_end_on(p2_f, p_comm2)

        half_span = (np.pi - GAP_ANG) / 2
        a1_start = ang_seg1 - half_span
        a1_end   = ang_seg1 + half_span
        a2_start = ang_seg2 - half_span
        a2_end   = ang_seg2 + half_span

        y_c_f = Y_COMM - 0.12
        y_c_b = Y_COMM + 0.12

        pts_s1_f = [np.array([R_COMM * np.cos(a), y_c_f, R_COMM * np.sin(a)]) for a in np.linspace(a1_start, a1_end, 14)]
        pts_s1_b = [np.array([R_COMM * np.cos(a), y_c_b, R_COMM * np.sin(a)]) for a in np.linspace(a1_start, a1_end, 14)]
        pts_s2_f = [np.array([R_COMM * np.cos(a), y_c_f, R_COMM * np.sin(a)]) for a in np.linspace(a2_start, a2_end, 14)]
        pts_s2_b = [np.array([R_COMM * np.cos(a), y_c_b, R_COMM * np.sin(a)]) for a in np.linspace(a2_start, a2_end, 14)]

        seg1_f.set_points_smoothly(pts_s1_f)
        seg1_b.set_points_smoothly(pts_s1_b)
        seg2_f.set_points_smoothly(pts_s2_f)
        seg2_b.set_points_smoothly(pts_s2_b)

        gap_edge1a.put_start_and_end_on(pts_s1_f[0], pts_s1_b[0])
        gap_edge1b.put_start_and_end_on(pts_s1_f[-1], pts_s1_b[-1])
        gap_edge2a.put_start_and_end_on(pts_s2_f[0], pts_s2_b[0])
        gap_edge2b.put_start_and_end_on(pts_s2_f[-1], pts_s2_b[-1])

        # Handedness & Physics:
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

        arr_len = 0.35
        if dir1 == +1:
            curr_arr1.put_start_and_end_on([x1, -arr_len, z1], [x1, arr_len, z1])
        else:
            curr_arr1.put_start_and_end_on([x1, arr_len, z1], [x1, -arr_len, z1])

        if dir2 == +1:
            curr_arr2.put_start_and_end_on([x2, -arr_len, z2], [x2, arr_len, z2])
        else:
            curr_arr2.put_start_and_end_on([x2, arr_len, z2], [x2, -arr_len, z2])

        f_len = 1.05
        fz1 = -dir1 * f_len
        fz2 = -dir2 * f_len

        force_arr1.put_start_and_end_on([x1, 0.0, z1], [x1, 0.0, z1 + fz1])
        force_arr2.put_start_and_end_on([x2, 0.0, z2], [x2, 0.0, z2 + fz2])

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

    update_motor(0.0)

    return {
        "static": static_mobs,
        "moving": moving_mobs,
        "shaft": shaft,
        "pole_n": pole_n_group,
        "pole_s": pole_s_group,
        "lbl_n": lbl_n,
        "lbl_s": lbl_s,
        "lbl_plus": lbl_plus,
        "lbl_minus": lbl_minus,
        "field_lines": field_lines,
        "loop": loop_group,
        "cond1": wire_cond1,
        "cond2": wire_cond2,
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

        # Initially hide force arrows during establish shot
        motor["update"](0.0, commutator_on=True, show_forces=False)

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

        lbl_loop = self.hud(Text("ขดลวดอาร์เมเจอร์", font_size=16, color=C_COPPER).move_to([-5.05, 0.40, 0]))
        arr_loop = self.hud(Arrow([-3.75, 0.40, 0], [-1.45, 0.35, 0], color=C_COPPER, stroke_width=2.0, tip_length=0.14))

        lbl_comm = self.hud(Text("คอมมิวเทเตอร์", font_size=16, color=C_COPPER).move_to([-5.05, -0.90, 0]))
        arr_comm = self.hud(Arrow([-3.90, -0.90, 0], [-0.85, -1.25, 0], color=C_COPPER, stroke_width=2.0, tip_length=0.14))

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
            Indicate(motor["loop"], color=C_COPPER, scale_factor=1.06),
            Indicate(motor["shaft"], color=WHITE, scale_factor=1.06),
            Indicate(motor["comm"], color=C_COPPER, scale_factor=1.08),
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
        self.move_camera(phi=68 * DEGREES, theta=-40 * DEGREES, run_time=1.2)
        self.wait(0.3)

        # Caption swap: Sequential!
        self.play(FadeOut(cap_a), run_time=0.3)
        cap_b1 = self.hud(caption_top(
            "เมื่อกระแสไหลผ่านตัวนำในสนามแม่เหล็ก จะเกิดแรง F = I × B ตั้งฉากกับทั้งกระแสและสนาม",
            size=19
        ))
        self.play(FadeIn(cap_b1, shift=DOWN * 0.15), run_time=0.5)

        # Conductor 1 (+X): current +Y -> force -Z (pushed down)
        motor["update"](0.0, commutator_on=True, show_forces=True, force_opacity=0.0)
        self.play(
            Indicate(motor["cond1"], color=C_CURRENT, scale_factor=1.08),
            FadeIn(motor["curr1"]),
            run_time=0.8
        )
        self.play(
            FadeIn(motor["force1"]),
            run_time=0.8
        )
        self.wait(1.5)

        self.play(FadeOut(cap_b1), run_time=0.3)
        cap_b2 = self.hud(caption_top(
            "ตัวนำฝั่งขวา (+X): กระแสพุ่งไปข้างหน้า (+Y)  →  แรงแม่เหล็กผลักลง (-Z)",
            size=19, color=WHITE
        ))
        self.play(FadeIn(cap_b2, shift=DOWN * 0.15), run_time=0.5)
        self.wait(1.4)

        # Conductor 2 (-X): current -Y -> force +Z (pushed up)
        self.play(
            Indicate(motor["cond2"], color=C_CURRENT, scale_factor=1.08),
            FadeIn(motor["curr2"]),
            FadeIn(motor["force2"]),
            run_time=1.0
        )

        self.play(FadeOut(cap_b2), run_time=0.3)
        cap_b3 = self.hud(caption_top(
            "ตัวนำฝั่งซ้าย (-X): กระแสไหลย้อนกลับ (-Y)  →  แรงผลักขึ้น (+Z) เกิด 'แรงคู่ควบ' หมุนเพลา",
            size=19, color=OK
        ))
        self.play(FadeIn(cap_b3, shift=DOWN * 0.15), run_time=0.5)

        # Show torque indicator
        torque_arc = Arc(radius=0.55, start_angle=-30 * DEGREES, angle=140 * DEGREES,
                         color=C_TORQUE, stroke_width=4)
        torque_arc.rotate(90 * DEGREES, axis=RIGHT).move_to([0, 0.4, 0])
        self.play(Create(torque_arc), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(torque_arc), run_time=0.5)

        # ── SHOT C: Dead Point & The Problem (Failure without Commutator) ─────
        # Lock camera looking straight down shaft axis Y (end-on view: phi=89.9, theta=-90)
        self.move_camera(phi=89.9 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        self.wait(0.3)

        # VERIFICATION FRAME BEAT: Max torque position in end-on view
        # Screen horizontal = X (field points right, N left, S right)
        # Screen vertical = Z (forces point straight up on left, straight down on right)
        self.play(FadeOut(cap_b3), run_time=0.3)
        cap_c1 = self.hud(caption_top(
            "มุมมองตามแนวเพลา: ระนาบนอน แรงคู่ควบมีแขนโมเมนต์ยาวสุด  →  เกิดทอร์กสูงสุด",
            size=19, color=WHITE
        ))
        self.play(FadeIn(cap_c1, shift=DOWN * 0.15), run_time=0.5)
        self.wait(2.5)  # Steady frame for verification

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
            motor["update"](th, commutator_on=True, show_forces=True)

        motor["shaft"].add_updater(upd_motor_normal)
        self.play(th_tracker.animate.set_value(np.pi / 2), run_time=2.4, rate_func=smooth)
        motor["shaft"].remove_updater(upd_motor_normal)
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
            motor["update"](th, commutator_on=False, show_forces=True)

        motor["shaft"].add_updater(upd_motor_fail)

        # Damped oscillation around dead point pi/2
        self.play(th_tracker.animate.set_value(np.pi / 2 + 32 * DEGREES), run_time=0.9, rate_func=ease_out_sine)
        self.play(th_tracker.animate.set_value(np.pi / 2 - 20 * DEGREES), run_time=0.9, rate_func=ease_in_out_sine)
        self.play(th_tracker.animate.set_value(np.pi / 2 + 10 * DEGREES), run_time=0.8, rate_func=ease_in_out_sine)
        self.play(th_tracker.animate.set_value(np.pi / 2), run_time=0.8, rate_func=ease_in_out_sine)

        motor["shaft"].remove_updater(upd_motor_fail)

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
            Indicate(motor["comm"], color=WARN, scale_factor=1.12),
            Indicate(motor["brushes"], color=WHITE, scale_factor=1.10),
            run_time=1.4
        )
        self.wait(1.2)

        # Reset loop to just before dead point (45 degrees before pi/2)
        th_tracker.set_value(np.pi / 4)
        motor["update"](np.pi / 4, commutator_on=True, show_forces=True)
        self.wait(0.6)

        # Rotate slowly through the dead point
        # At exact instant brushes cross gap (theta = pi/2), trigger bright FLASH and flip arrows
        def upd_motor_flip(_m):
            th = th_tracker.get_value()
            diff = abs(th - np.pi / 2)
            flash = float(np.exp(- (diff / 0.08)**2)) if diff < 0.15 else 0.0
            motor["update"](th, commutator_on=True, show_forces=True, flash_intensity=flash)

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
        self.wait(2.0)

        # ── SHOT E: Continuous Running + Summary Card ────────────────────────
        # Return to 3/4 view (phi = 65 deg, theta = -50 deg)
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, run_time=1.8)
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
            motor["update"](th, commutator_on=True, show_forces=True, flash_intensity=flash)

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
