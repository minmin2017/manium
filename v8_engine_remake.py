"""
v8_engine_remake.py — Brand-new V8 Engine teaching video scene for Manim CE.
Fully implements V8_REMAKE_DESIGN.md following mlib.py and Manim CE standards.

- Scene class: V8EngineRemake(SafeThreeDScene)
- 90-degree cross-plane Ford Coyote firing order: 1-5-4-8-6-3-7-2
- Exact slider-crank kinematics (s = r*cos(theta) + sqrt(L^2 - r^2*sin^2(theta)))
- All geometry contract assertions enforced at module load.
- 5 comprehensive pedagogical shots covering:
    1. Hook: 8 pistons, 1 crankshaft, solid to translucent reveal.
    2. Atomic unit: 4-stroke cycle with physical valve/particle changes,
       720° circular timeline, force-to-torque causal vectors.
    3. Why the V exists: end-on 90° proving shot (phi≈88°, theta≈-83°),
       Bank L/R labels, causal replication along crankshaft.
    4. Staggered firing: 720° divided among 8 cylinders, Coyote firing rail,
       live torque vs crank angle comparison (1 cylinder vs 8 cylinders).
    5. Payoff: mechanical energy path highlight, high-speed running finale,
       3-line summary card.
"""

from manim import *
from mlib import (
    SafeThreeDScene,
    title,
    caption_top,
    fit_width,
    arrow3,
    line3,
    GRAYTXT,
    TORQUE,
    FORCE,
    WARN,
    OK,
)
import numpy as np

# ==============================================================================
# 1. GEOMETRY CONTRACT & VERIFIED CONSTANTS
# ==============================================================================

# Crank radius r = 0.42, rod length L = 1.45 (L > r asserted)
CRANK_R = 0.42
ROD_L = 1.45
assert ROD_L > CRANK_R, "Connecting rod length must exceed crank radius (L > r)"

# Bank angle: exactly 90 degrees separated, symmetric about X=0 (Y-Z vertical plane)
# Left cylinder travel direction: normalize((-1, 0, 1))
# Right cylinder travel direction: normalize((1, 0, 1))
U_L = np.array([-1.0, 0.0, 1.0]) / np.sqrt(2.0)
U_R = np.array([1.0, 0.0, 1.0]) / np.sqrt(2.0)

# Perpendicular vectors in the rotation plane (Y_hat x U)
V_L = np.array([1.0, 0.0, 1.0]) / np.sqrt(2.0)
V_R = np.array([1.0, 0.0, -1.0]) / np.sqrt(2.0)

# Assertions required by geometry contract
assert np.isclose(np.dot(U_L, U_R), 0.0), "Bank axes must be separated by exactly 90 degrees"
assert np.isclose(np.linalg.norm(U_L), 1.0) and np.isclose(np.linalg.norm(U_R), 1.0), "Bank vectors must be normalized"
assert np.isclose(U_L[0], -U_R[0]) and np.isclose(U_L[2], U_R[2]), "Banks must be symmetric about vertical plane X=0"

# Four throws lie at y = [-2.25, -0.75, 0.75, 2.25]
THROWS_Y = np.array([-2.25, -0.75, 0.75, 2.25])
assert np.allclose(np.diff(THROWS_Y), 1.5), "Throw spacing must be uniform at 1.5"

# Representative Ford Coyote Firing Order: 1-5-4-8-6-3-7-2
# Cylinders 1-4: Bank R (Throws 0, 1, 2, 3)
# Cylinders 5-8: Bank L (Throws 0, 1, 2, 3)
FIRING_ORDER = [1, 5, 4, 8, 6, 3, 7, 2]

# Firing phases over 720 degrees (spaced by 90 degrees)
FIRING_PHASES = {
    1: 0.0,
    5: 90.0,
    4: 180.0,
    8: 270.0,
    6: 360.0,
    3: 450.0,
    7: 540.0,
    2: 630.0,
}
assert len(set(FIRING_PHASES.values())) == 8, "Must have 8 unique firing phases"
assert sorted(FIRING_PHASES.values()) == [
    0.0,
    90.0,
    180.0,
    270.0,
    360.0,
    450.0,
    540.0,
    630.0,
], "Firing phases must be spaced at 90-degree intervals across 720 degrees"

# Cylinder specification table
# cyl_id: (bank_key, throw_index, bank_vector_U, bank_perp_V)
CYLINDER_SPECS = {
    1: ("R", 0, U_R, V_R),
    2: ("R", 1, U_R, V_R),
    3: ("R", 2, U_R, V_R),
    4: ("R", 3, U_R, V_R),
    5: ("L", 0, U_L, V_L),
    6: ("L", 1, U_L, V_L),
    7: ("L", 2, U_L, V_L),
    8: ("L", 3, U_L, V_L),
}

# Cross-plane throw angles around crank axis (traditional 90-degree cross pattern)
THROW_ANGLES = {
    0: 0.0,
    1: np.pi / 2.0,
    2: 3.0 * np.pi / 2.0,
    3: np.pi,
}

# Color palette adhering to design contract
COLOR_BG = "#080C16"
COLOR_INTAKE = "#00E5FF"       # Cyan
COLOR_COMPRESSION = "#FFA726"  # Amber
COLOR_POWER = "#FF3D00"        # Combustion orange/red
COLOR_EXHAUST = "#90A4AE"      # Gray
COLOR_ACTIVE = "#FFFF00"       # Neon yellow
COLOR_METAL = "#CFD8DC"        # Polished metallic
COLOR_DARK_METAL = "#37474F"   # Block casting
COLOR_CRANK = "#78909C"        # Crankshaft steel


# ==============================================================================
# 2. EXACT SLIDER-CRANK KINEMATICS
# ==============================================================================

def slider_crank_displacement(theta_rad, r=CRANK_R, L=ROD_L):
    """
    Exact slider-crank wristpin displacement s(theta) from crankshaft axis:
        s(theta) = r * cos(theta) + sqrt(L^2 - r^2 * sin^2(theta))
    At theta = 0 (TDC): s = L + r = 1.87
    At theta = pi (BDC): s = L - r = 1.03
    """
    sin_t = np.sin(theta_rad)
    cos_t = np.cos(theta_rad)
    radical = L**2 - (r * sin_t)**2
    return r * cos_t + np.sqrt(np.maximum(radical, 1e-9))


def get_piston_wrist_pos(theta_rad, y_throw, bank_u):
    """3D coordinates of piston wristpin."""
    s = slider_crank_displacement(theta_rad)
    return np.array([0.0, y_throw, 0.0]) + s * bank_u


def get_crankpin_pos(theta_rad, y_throw, bank_u, bank_v):
    """3D coordinates of crankpin journal for this cylinder."""
    r_vec = CRANK_R * (np.cos(theta_rad) * bank_u + np.sin(theta_rad) * bank_v)
    return np.array([0.0, y_throw, 0.0]) + r_vec


# ==============================================================================
# 3. 3D MECHANICAL MODEL BUILDERS
# ==============================================================================

def build_crankshaft():
    """
    Constructs the 3D cross-plane crankshaft assembly:
    main journals along Y axis, 4 throws, counterweights, and rear flywheel.
    """
    crank_group = Group()

    # Main journal shaft through the center
    main_shaft = Cylinder(
        radius=0.16,
        height=6.2,
        direction=np.array([0.0, 1.0, 0.0]),
        resolution=(8, 8),
        color=COLOR_CRANK,
    ).move_to(ORIGIN)
    crank_group.add(main_shaft)

    # Crank webs and counterweights at each throw
    for t_idx, y_val in enumerate(THROWS_Y):
        angle = THROW_ANGLES[t_idx]
        pin_dir = np.array([np.sin(angle), 0.0, np.cos(angle)])

        # Crankpin
        pin = Cylinder(
            radius=0.13,
            height=0.36,
            direction=np.array([0.0, 1.0, 0.0]),
            resolution=(8, 8),
            color="#B0BEC5",
        ).move_to(np.array([0.0, y_val, 0.0]) + CRANK_R * pin_dir)

        # Counterweight opposite to crankpin
        cweight = Prism(
            dimensions=[0.24, 0.38, 0.65]
        ).move_to(np.array([0.0, y_val, 0.0]) - (CRANK_R * 0.7) * pin_dir)
        cweight.set_color("#455A64")

        # Crank web
        web = Prism(
            dimensions=[0.18, 0.16, CRANK_R * 1.8]
        ).move_to(np.array([0.0, y_val, 0.0]) + (CRANK_R * 0.2) * pin_dir)
        web.set_color("#607D8B")

        crank_group.add(pin, cweight, web)

    # Rear flywheel at y = 2.85
    flywheel = Cylinder(
        radius=0.82,
        height=0.22,
        direction=np.array([0.0, 1.0, 0.0]),
        resolution=(10, 10),
        color="#546E7A",
    ).move_to(np.array([0.0, 2.85, 0.0]))
    crank_group.add(flywheel)

    return crank_group


def build_engine_block(opacity=0.30):
    """
    Constructs the V8 engine block structure:
    Bank L and Bank R casings, heads, and crankcase base.
    """
    block_group = Group()

    # Bank R block casing (tilted 45 degrees along U_R)
    bank_r = Prism(dimensions=[1.15, 5.6, 1.35])
    bank_r.rotate(45.0 * DEGREES, axis=np.array([0.0, 1.0, 0.0]))
    bank_r.move_to(1.45 * U_R)
    bank_r.set_color(COLOR_DARK_METAL).set_opacity(opacity)

    # Bank L block casing (tilted -45 degrees along U_L)
    bank_l = Prism(dimensions=[1.15, 5.6, 1.35])
    bank_l.rotate(-45.0 * DEGREES, axis=np.array([0.0, 1.0, 0.0]))
    bank_l.move_to(1.45 * U_L)
    bank_l.set_color(COLOR_DARK_METAL).set_opacity(opacity)

    # Lower crankcase pan
    oil_pan = Prism(dimensions=[1.3, 5.8, 0.55])
    oil_pan.move_to(np.array([0.0, 0.0, -0.42]))
    oil_pan.set_color("#263238").set_opacity(opacity * 1.1)

    block_group.add(bank_r, bank_l, oil_pan)
    return block_group


def build_cylinder_sleeves():
    """Builds 8 translucent cylinder sleeves guiding the pistons."""
    sleeves = Group()
    for cyl_id, (bank, t_idx, u_vec, _) in CYLINDER_SPECS.items():
        y_val = THROWS_Y[t_idx]
        sleeve = Cylinder(
            radius=0.40,
            height=1.45,
            direction=u_vec,
            resolution=(8, 8),
            color="#90A4AE",
        ).move_to(np.array([0.0, y_val, 0.0]) + 1.48 * u_vec)
        sleeve.set_opacity(0.18)
        sleeves.add(sleeve)
    return sleeves


def build_piston_assembly(bank_u):
    """
    Builds one piston body with crown rings and wristpin marker.
    """
    piston_body = Cylinder(
        radius=0.37,
        height=0.34,
        direction=bank_u,
        resolution=(8, 8),
        color=COLOR_METAL,
    )
    piston_ring = Cylinder(
        radius=0.375,
        height=0.06,
        direction=bank_u,
        resolution=(8, 8),
        color="#78909C",
    ).move_to(0.08 * bank_u)

    return Group(piston_body, piston_ring)


# ==============================================================================
# 4. SCENE CLASS: V8EngineRemake
# ==============================================================================

class V8EngineRemake(SafeThreeDScene):
    """
    Master V8 Engine teaching clip in Thai answering:
      1. What makes the pistons move?
      2. How does piston motion become crankshaft rotation?
      3. Why does a V8 have two banks and eight cylinders?
      4. Why do the cylinders fire one after another instead of together?
    """

    def construct(self):
        # Set dark navy background per format contract
        self.camera.background_color = COLOR_BG

        # Master ValueTracker for crankshaft rotation angle
        # All cylinder phases and kinematic states derive strictly from this tracker.
        self.master_angle = ValueTracker(0.0)

        # ----------------------------------------------------------------------
        # SHOT 1: HOOK — EIGHT PISTONS, ONE OUTPUT SHAFT (0–7 s)
        # ----------------------------------------------------------------------
        self.play_shot_1_hook()

        # ----------------------------------------------------------------------
        # SHOT 2: ATOMIC UNIT — ONE CYLINDER MAKES TORQUE (7–27 s)
        # ----------------------------------------------------------------------
        self.play_shot_2_atomic_cylinder()

        # ----------------------------------------------------------------------
        # SHOT 3: WHY THE V EXISTS — 90° PACKAGING (27–39 s)
        # ----------------------------------------------------------------------
        self.play_shot_3_v_geometry()

        # ----------------------------------------------------------------------
        # SHOT 4: STAGGERED FIRING — 720° DIVIDED AMONG 8 CYLINDERS (39–61 s)
        # ----------------------------------------------------------------------
        self.play_shot_4_staggered_firing()

        # ----------------------------------------------------------------------
        # SHOT 5: PAYOFF — COMBUSTION TO WHEEL-DRIVING ROTATION (61–76 s)
        # ----------------------------------------------------------------------
        self.play_shot_5_payoff()

    # ==========================================================================
    # SHOT 1 IMPLEMENTATION
    # ==========================================================================
    def play_shot_1_hook(self):
        # Establish three-quarter view
        self.set_camera_orientation(phi=68.0 * DEGREES, theta=-52.0 * DEGREES)

        # Build solid engine block and internal components
        block_solid = build_engine_block(opacity=0.92)
        crankshaft = build_crankshaft()
        sleeves = build_cylinder_sleeves()

        # Build 8 pistons and connecting rods
        pistons = {}
        rods = {}
        wrist_dots = {}

        for cyl_id, (_, t_idx, u_vec, v_vec) in CYLINDER_SPECS.items():
            y_val = THROWS_Y[t_idx]
            piston = build_piston_assembly(u_vec)
            p_wrist = get_piston_wrist_pos(0.0, y_val, u_vec)
            p_pin = get_crankpin_pos(0.0, y_val, u_vec, v_vec)

            piston.move_to(p_wrist + 0.17 * u_vec)
            rod = line3(p_pin, p_wrist, color="#ECEFF1", thickness=0.06)
            w_dot = Dot(p_wrist, radius=0.06, color="#90A4AE")

            pistons[cyl_id] = piston
            rods[cyl_id] = rod
            wrist_dots[cyl_id] = w_dot

        internal_group = Group(crankshaft, sleeves, *pistons.values(), *rods.values(), *wrist_dots.values())

        # Title and opening caption
        hook_title = title("V8 ทำงานอย่างไร?", size=30)
        hook_cap = caption_top("8 ลูกสูบไม่ได้ระเบิดพร้อมกัน—มันผลัดกันส่งแรงให้เพลา", max_w=12.0)
        self.hud(hook_title, hook_cap)

        # Start with solid engine model
        self.add(block_solid)
        self.play(FadeIn(hook_title), run_time=0.8)

        # Slow 1-second orbit to establish 3D silhouette
        self.begin_ambient_camera_rotation(rate=0.22)
        self.wait(1.0)
        self.stop_ambient_camera_rotation()

        # Explode/fade block translucent to expose 8 pistons, rods, crankshaft
        self.add(internal_group)
        self.play(
            block_solid.animate.set_opacity(0.28),
            FadeIn(hook_cap),
            run_time=1.4,
        )

        # First-appearance pointer labels for components
        piston_ptr = arrow3(
            start=np.array([2.3, -2.25, 2.3]),
            end=np.array([1.5, -2.25, 1.7]),
            color=COLOR_ACTIVE,
            thickness=0.03,
        )
        piston_label = Text("ลูกสูบ (Piston)", font_size=18, color=COLOR_ACTIVE)
        piston_label.next_to(piston_ptr.get_start(), UP + RIGHT, buff=0.1)
        self.hud(piston_label)

        crank_ptr = arrow3(
            start=np.array([-2.2, -0.75, -1.2]),
            end=np.array([-0.6, -0.75, -0.2]),
            color="#4FC3F7",
            thickness=0.03,
        )
        crank_label = Text("เพลาข้อเหวี่ยง (Crankshaft)", font_size=18, color="#4FC3F7")
        crank_label.next_to(crank_ptr.get_start(), DOWN + LEFT, buff=0.1)
        self.hud(crank_label)

        # Flash components as they are named
        self.play(
            FadeIn(piston_ptr),
            FadeIn(piston_label),
            FadeIn(crank_ptr),
            FadeIn(crank_label),
            pistons[1].animate.set_color(COLOR_ACTIVE),
            run_time=1.2,
        )
        self.wait(1.2)

        # Clear Shot 1 objects for Shot 2
        self.play(
            FadeOut(hook_title),
            FadeOut(hook_cap),
            FadeOut(piston_ptr),
            FadeOut(piston_label),
            FadeOut(crank_ptr),
            FadeOut(crank_label),
            FadeOut(block_solid),
            FadeOut(internal_group),
            run_time=0.8,
        )

    # ==========================================================================
    # SHOT 2 IMPLEMENTATION
    # ==========================================================================
    def play_shot_2_atomic_cylinder(self):
        # Camera side cutaway view focusing on Cylinder 1 (Throw 0, front)
        self.move_camera(
            phi=78.0 * DEGREES,
            theta=-18.0 * DEGREES,
            frame_center=np.array([0.7, -2.25, 1.0]),
            zoom=1.25,
            run_time=1.4,
        )

        y_val = THROWS_Y[0]
        u_vec = U_R
        v_vec = V_R

        # Single cylinder cutaway sleeve
        cyl_sleeve = Cylinder(
            radius=0.42,
            height=1.55,
            direction=u_vec,
            resolution=(8, 8),
            color="#90A4AE",
        ).move_to(np.array([0.0, y_val, 0.0]) + 1.48 * u_vec)
        cyl_sleeve.set_opacity(0.22)

        # Single crank throw assembly
        crank_journal = Cylinder(
            radius=0.15,
            height=1.2,
            direction=np.array([0.0, 1.0, 0.0]),
            resolution=(8, 8),
            color=COLOR_CRANK,
        ).move_to(np.array([0.0, y_val, 0.0]))

        # Piston and connecting rod
        piston = build_piston_assembly(u_vec)
        rod = line3(ORIGIN, ORIGIN, color="#FFFFFF", thickness=0.07)
        wrist_pin = Dot(ORIGIN, radius=0.07, color="#B0BEC5")
        crank_pin = Dot(ORIGIN, radius=0.08, color="#90A4AE")

        # Cylinder head assembly: Valves & Spark plug
        head_pos = np.array([0.0, y_val, 0.0]) + (ROD_L + CRANK_R + 0.42) * u_vec

        # Spark plug at center of head
        spark_body = Cylinder(
            radius=0.08,
            height=0.35,
            direction=u_vec,
            resolution=(6, 6),
            color=WHITE,
        ).move_to(head_pos + 0.22 * u_vec)
        spark_tip = Dot(head_pos + 0.02 * u_vec, radius=0.05, color=YELLOW)
        spark_group = Group(spark_body, spark_tip)

        # Intake valve (left/front offset)
        v_offset_in = np.array([0.0, 0.22, 0.0]) - 0.12 * v_vec
        intake_pos_closed = head_pos + v_offset_in
        intake_stem = line3(intake_pos_closed + 0.4 * u_vec, intake_pos_closed, color=COLOR_INTAKE, thickness=0.045)
        intake_disc = Circle(radius=0.14, color=COLOR_INTAKE, fill_opacity=0.8).rotate(45.0 * DEGREES, axis=UP).move_to(intake_pos_closed)
        intake_valve = Group(intake_stem, intake_disc)

        # Exhaust valve (right/rear offset)
        v_offset_ex = np.array([0.0, -0.22, 0.0]) + 0.12 * v_vec
        exhaust_pos_closed = head_pos + v_offset_ex
        exhaust_stem = line3(exhaust_pos_closed + 0.4 * u_vec, exhaust_pos_closed, color=COLOR_EXHAUST, thickness=0.045)
        exhaust_disc = Circle(radius=0.14, color=COLOR_EXHAUST, fill_opacity=0.8).rotate(45.0 * DEGREES, axis=UP).move_to(exhaust_pos_closed)
        exhaust_valve = Group(exhaust_stem, exhaust_disc)

        # Combustion chamber glow volume
        chamber_glow = Cylinder(
            radius=0.38,
            height=0.25,
            direction=u_vec,
            resolution=(8, 8),
            color=COLOR_POWER,
        ).move_to(head_pos - 0.15 * u_vec)
        chamber_glow.set_opacity(0.0)

        single_cyl_group = Group(
            cyl_sleeve, crank_journal, piston, rod, wrist_pin, crank_pin,
            spark_group, intake_valve, exhaust_valve, chamber_glow
        )
        self.add(single_cyl_group)

        # Pointers for newly introduced components
        ptr_spark = arrow3(head_pos + np.array([0.8, 0.0, 0.8]), head_pos + 0.25 * u_vec, color=YELLOW, thickness=0.025)
        lbl_spark = Text("หัวเทียน", font_size=18, color=YELLOW).next_to(ptr_spark.get_start(), UP, buff=0.08)

        ptr_in = arrow3(intake_pos_closed + np.array([-0.7, 0.3, 0.5]), intake_pos_closed + 0.1 * u_vec, color=COLOR_INTAKE, thickness=0.025)
        lbl_in = Text("วาล์วไอดี", font_size=18, color=COLOR_INTAKE).next_to(ptr_in.get_start(), UP + LEFT, buff=0.08)

        ptr_ex = arrow3(exhaust_pos_closed + np.array([0.7, -0.3, 0.5]), exhaust_pos_closed + 0.1 * u_vec, color=COLOR_EXHAUST, thickness=0.025)
        lbl_ex = Text("วาล์วไอเสีย", font_size=18, color=COLOR_EXHAUST).next_to(ptr_ex.get_start(), UP + RIGHT, buff=0.08)

        ptr_rod = arrow3(np.array([1.5, y_val, 0.2]), np.array([0.7, y_val, 0.6]), color="#ECEFF1", thickness=0.025)
        lbl_rod = Text("ก้านสูบ", font_size=18, color="#ECEFF1").next_to(ptr_rod.get_start(), RIGHT, buff=0.08)

        self.hud(lbl_spark, lbl_in, lbl_ex, lbl_rod)

        # Title for Shot 2
        shot2_title = title("1 กระบอกสูบ: วัฏจักร 4 จังหวะ (720°)", size=27)
        self.hud(shot2_title)
        self.play(FadeIn(shot2_title), run_time=0.6)

        self.play(
            FadeIn(ptr_spark), FadeIn(lbl_spark),
            FadeIn(ptr_in), FadeIn(lbl_in),
            FadeIn(ptr_ex), FadeIn(lbl_ex),
            FadeIn(ptr_rod), FadeIn(lbl_rod),
            run_time=1.4,
        )
        self.wait(1.0)
        self.play(
            FadeOut(ptr_spark), FadeOut(lbl_spark),
            FadeOut(ptr_in), FadeOut(lbl_in),
            FadeOut(ptr_ex), FadeOut(lbl_ex),
            FadeOut(ptr_rod), FadeOut(lbl_rod),
            run_time=0.6,
        )

        # ----------------------------------------------------------------------
        # Compact 720-Degree Circular Timeline HUD
        # ----------------------------------------------------------------------
        tl_center = np.array([4.8, -0.8, 0.0])
        tl_radius = 1.05

        # 4 Quadrants on 360-degree HUD ring representing 720 degrees (each quadrant = 180°)
        # Q1: 0°-180° Intake (Cyan)
        # Q2: 180°-360° Compression (Amber)
        # Q3: 360°-540° Power (Red)
        # Q4: 540°-720° Exhaust (Gray)
        arc_intake = Arc(radius=tl_radius, start_angle=90.0 * DEGREES, angle=-90.0 * DEGREES, arc_center=tl_center, color=COLOR_INTAKE, stroke_width=6)
        arc_comp = Arc(radius=tl_radius, start_angle=0.0 * DEGREES, angle=-90.0 * DEGREES, arc_center=tl_center, color=COLOR_COMPRESSION, stroke_width=6)
        arc_power = Arc(radius=tl_radius, start_angle=-90.0 * DEGREES, angle=-90.0 * DEGREES, arc_center=tl_center, color=COLOR_POWER, stroke_width=6)
        arc_exhaust = Arc(radius=tl_radius, start_angle=-180.0 * DEGREES, angle=-90.0 * DEGREES, arc_center=tl_center, color=COLOR_EXHAUST, stroke_width=6)

        tl_bg = Circle(radius=tl_radius, color="#1E293B", fill_opacity=0.4, stroke_width=1.5).move_to(tl_center)
        lbl_tl_center = Text("720°", font_size=18, color=WHITE).move_to(tl_center + UP * 0.14)
        lbl_tl_sub = Text("2 รอบเพลา", font_size=13, color=GRAYTXT).move_to(tl_center + DOWN * 0.18)

        lbl_s1 = Text("1.ดูด", font_size=14, color=COLOR_INTAKE).next_to(tl_center + np.array([0.7, 0.7, 0.0]), RIGHT, buff=0.05)
        lbl_s2 = Text("2.อัด", font_size=14, color=COLOR_COMPRESSION).next_to(tl_center + np.array([0.7, -0.7, 0.0]), RIGHT, buff=0.05)
        lbl_s3 = Text("3.กำลัง", font_size=14, color=COLOR_POWER).next_to(tl_center + np.array([-0.7, -0.7, 0.0]), LEFT, buff=0.05)
        lbl_s4 = Text("4.คาย", font_size=14, color=COLOR_EXHAUST).next_to(tl_center + np.array([-0.7, 0.7, 0.0]), LEFT, buff=0.05)

        timeline_hud = Group(tl_bg, arc_intake, arc_comp, arc_power, arc_exhaust, lbl_tl_center, lbl_tl_sub, lbl_s1, lbl_s2, lbl_s3, lbl_s4)
        self.hud(timeline_hud)
        self.play(FadeIn(timeline_hud), run_time=0.8)

        # Kinematic updater linking piston, rod, and crankpin to angle_tracker
        def update_single_cylinder(theta_val):
            pw = get_piston_wrist_pos(theta_val, y_val, u_vec)
            pp = get_crankpin_pos(theta_val, y_val, u_vec, v_vec)
            piston.move_to(pw + 0.17 * u_vec)
            rod.put_start_and_end_on(pp, pw)
            wrist_pin.move_to(pw)
            crank_pin.move_to(pp)

        update_single_cylinder(0.0)

        # ----------------------------------------------------------------------
        # BEAT 1: INTAKE (0° to 180°)
        # ----------------------------------------------------------------------
        cap_intake = caption_top("1. จังหวะดูด (0°–180°): วาล์วไอดีเปิด ลูกสูบเลื่อนลง ดูดไอดีเข้าห้องเผาไหม้", color=COLOR_INTAKE)
        self.hud(cap_intake)

        # Cyan fuel-air mixture particles flowing along intake runner
        intake_particles = VGroup(*[
            Dot(head_pos + v_offset_in + np.array([0.0, 0.3 + 0.15 * i, 0.2 + 0.1 * i]), radius=0.04, color=COLOR_INTAKE)
            for i in range(7)
        ])

        self.play(
            FadeIn(cap_intake),
            arc_intake.animate.set_stroke(width=10, opacity=1.0),
            intake_valve.animate.shift(-0.16 * u_vec),  # Valve opens into chamber
            run_time=0.6,
        )

        # Crank sweeps 0 -> PI; piston descends TDC -> BDC; particles enter
        p_target = head_pos - 0.3 * u_vec
        self.play(
            UpdateFromAlphaFunc(
                piston,
                lambda m, a: update_single_cylinder(a * np.pi),
            ),
            chamber_glow.animate.set_opacity(0.35).set_color(COLOR_INTAKE),
            intake_particles.animate.move_to(p_target),
            run_time=2.4,
            rate_func=linear,
        )
        self.play(
            intake_valve.animate.shift(0.16 * u_vec),  # Valve closes at BDC
            FadeOut(intake_particles),
            FadeOut(cap_intake),
            arc_intake.animate.set_stroke(width=5, opacity=0.4),
            run_time=0.5,
        )

        # ----------------------------------------------------------------------
        # BEAT 2: COMPRESSION (180° to 360°)
        # ----------------------------------------------------------------------
        cap_comp = caption_top("2. จังหวะอัด (180°–360°): วาล์วปิดสนิท ลูกสูบเลื่อนขึ้น บีบอัดไอดีให้ร้อนและแน่น", color=COLOR_COMPRESSION)
        self.hud(cap_comp)

        self.play(
            FadeIn(cap_comp),
            arc_comp.animate.set_stroke(width=10, opacity=1.0),
            run_time=0.5,
        )

        # Crank sweeps PI -> 2*PI; piston rises BDC -> TDC; chamber compresses cyan -> amber
        self.play(
            UpdateFromAlphaFunc(
                piston,
                lambda m, a: update_single_cylinder(np.pi + a * np.pi),
            ),
            chamber_glow.animate.set_color(COLOR_COMPRESSION).scale(0.6).shift(0.08 * u_vec),
            run_time=2.4,
            rate_func=linear,
        )
        self.play(
            FadeOut(cap_comp),
            arc_comp.animate.set_stroke(width=5, opacity=0.4),
            run_time=0.5,
        )

        # ----------------------------------------------------------------------
        # BEAT 3: POWER (360° to 540°)
        # ----------------------------------------------------------------------
        cap_power = caption_top("3. จังหวะกำลัง (360°–540°): หัวเทียนจุดระเบิด ก๊าซขยายตัวดันลูกสูบ หมุนเพลา", color=COLOR_POWER)
        self.hud(cap_power)

        # Spark flash at TDC (theta = 360 degrees)
        spark_burst = Flash(
            spark_tip.get_center(),
            color=YELLOW,
            line_length=0.25,
            num_lines=12,
            flash_radius=0.35,
        )

        self.play(
            FadeIn(cap_power),
            arc_power.animate.set_stroke(width=10, opacity=1.0),
            spark_burst,
            chamber_glow.animate.set_color(COLOR_POWER).set_opacity(0.85).scale(1.5),
            run_time=0.6,
        )

        # Pressure arrows driving piston downward
        p_wrist_curr = get_piston_wrist_pos(2.0 * np.pi, y_val, u_vec)
        press_arrow1 = arrow3(p_wrist_curr + 0.45 * u_vec - 0.12 * v_vec, p_wrist_curr + 0.18 * u_vec - 0.12 * v_vec, color=COLOR_POWER, thickness=0.035)
        press_arrow2 = arrow3(p_wrist_curr + 0.45 * u_vec + 0.12 * v_vec, p_wrist_curr + 0.18 * u_vec + 0.12 * v_vec, color=COLOR_POWER, thickness=0.035)
        self.add(press_arrow1, press_arrow2)

        # Piston descends to maximum torque lever-arm moment (~90° after spark = 450° crank angle)
        self.play(
            UpdateFromAlphaFunc(
                piston,
                lambda m, a: update_single_cylinder(2.0 * np.pi + a * (0.5 * np.pi)),
            ),
            run_time=1.2,
            rate_func=linear,
        )
        self.remove(press_arrow1, press_arrow2)

        # Freeze briefly at strongest lever-arm moment and draw force-to-torque causal path
        p_wrist_mid = get_piston_wrist_pos(2.5 * np.pi, y_val, u_vec)
        p_pin_mid = get_crankpin_pos(2.5 * np.pi, y_val, u_vec, v_vec)

        # Downward force on piston: F_gas
        vec_f_gas = arrow3(p_wrist_mid + 0.6 * u_vec, p_wrist_mid + 0.15 * u_vec, color=COLOR_POWER, thickness=0.04)
        lbl_f_gas = Text("แรงดันก๊าซ (F)", font_size=16, color=COLOR_POWER).next_to(vec_f_gas.get_start(), UP + RIGHT, buff=0.08)

        # Force along connecting rod: F_rod
        vec_f_rod = arrow3(p_wrist_mid, p_pin_mid, color=COLOR_COMPRESSION, thickness=0.045)
        lbl_f_rod = Text("แรงส่งผ่านก้านสูบ", font_size=15, color=COLOR_COMPRESSION).next_to(p_pin_mid, RIGHT, buff=0.12)

        # Rotational torque arrow around crankshaft axis
        torque_arc = Arc(radius=0.45, start_angle=45.0 * DEGREES, angle=-180.0 * DEGREES, color=TORQUE, stroke_width=6)
        torque_arc.rotate(90.0 * DEGREES, axis=RIGHT).move_to(np.array([0.0, y_val, 0.0]))
        lbl_torque = Text("ทอร์กหมุนเพลา (τ)", font_size=17, color=TORQUE).next_to(torque_arc, DOWN + RIGHT, buff=0.1)

        self.hud(lbl_f_gas, lbl_f_rod, lbl_torque)
        self.play(
            FadeIn(vec_f_gas), FadeIn(lbl_f_gas),
            FadeIn(vec_f_rod), FadeIn(lbl_f_rod),
            FadeIn(torque_arc), FadeIn(lbl_torque),
            run_time=1.4,
        )
        self.wait(1.2)

        # Resume sweep to BDC (540°)
        self.play(
            FadeOut(vec_f_gas), FadeOut(lbl_f_gas),
            FadeOut(vec_f_rod), FadeOut(lbl_f_rod),
            FadeOut(torque_arc), FadeOut(lbl_torque),
            UpdateFromAlphaFunc(
                piston,
                lambda m, a: update_single_cylinder(2.5 * np.pi + a * (0.5 * np.pi)),
            ),
            chamber_glow.animate.set_opacity(0.4).scale(1.2),
            run_time=1.2,
            rate_func=linear,
        )
        self.play(
            FadeOut(cap_power),
            arc_power.animate.set_stroke(width=5, opacity=0.4),
            run_time=0.4,
        )

        # ----------------------------------------------------------------------
        # BEAT 4: EXHAUST (540° to 720°)
        # ----------------------------------------------------------------------
        cap_exhaust = caption_top("4. จังหวะคาย (540°–720°): วาล์วไอเสียเปิด ลูกสูบดันก๊าซไอเสียทิ้ง", color=COLOR_EXHAUST)
        self.hud(cap_exhaust)

        # Gray exhaust particles flowing out
        exhaust_particles = VGroup(*[
            Dot(head_pos - 0.15 * u_vec, radius=0.04, color=COLOR_EXHAUST)
            for _ in range(7)
        ])

        self.play(
            FadeIn(cap_exhaust),
            arc_exhaust.animate.set_stroke(width=10, opacity=1.0),
            exhaust_valve.animate.shift(-0.16 * u_vec),  # Exhaust valve opens
            FadeIn(exhaust_particles),
            run_time=0.6,
        )

        p_ex_exit = exhaust_pos_closed + np.array([0.0, -0.4, 0.4])
        self.play(
            UpdateFromAlphaFunc(
                piston,
                lambda m, a: update_single_cylinder(3.0 * np.pi + a * np.pi),
            ),
            chamber_glow.animate.set_opacity(0.0),
            exhaust_particles.animate.move_to(p_ex_exit).set_opacity(0.1),
            run_time=2.4,
            rate_func=linear,
        )

        self.play(
            exhaust_valve.animate.shift(0.16 * u_vec),  # Valve closes at TDC
            FadeOut(exhaust_particles),
            FadeOut(cap_exhaust),
            arc_exhaust.animate.set_stroke(width=5, opacity=0.4),
            run_time=0.5,
        )

        # Supporting fact summary line
        cap_720_fact = caption_top("สรุป: 1 สูบ ต้องหมุนเพลาถึง 2 รอบ (720°) แต่ได้จังหวะส่งกำลังเพียงครั้งเดียว!", color=WARN)
        self.hud(cap_720_fact)
        self.play(FadeIn(cap_720_fact), run_time=0.6)
        self.wait(1.5)

        # Clear Shot 2 objects
        self.play(
            FadeOut(shot2_title),
            FadeOut(cap_720_fact),
            FadeOut(timeline_hud),
            FadeOut(single_cyl_group),
            run_time=0.8,
        )

    # ==========================================================================
    # SHOT 3 IMPLEMENTATION
    # ==========================================================================
    def play_shot_3_v_geometry(self):
        # Return to atomic V pair sharing Throw 0: Cyl 1 (Bank R) & Cyl 5 (Bank L)
        y_val = THROWS_Y[0]

        # Build atomic V-pair at Throw 0
        piston_r = build_piston_assembly(U_R)
        piston_l = build_piston_assembly(U_L)
        pw_r = get_piston_wrist_pos(0.0, y_val, U_R)
        pw_l = get_piston_wrist_pos(np.pi / 2.0, y_val, U_L)
        pp_r = get_crankpin_pos(0.0, y_val, U_R, V_R)
        pp_l = get_crankpin_pos(np.pi / 2.0, y_val, U_L, V_L)

        piston_r.move_to(pw_r + 0.17 * U_R)
        piston_l.move_to(pw_l + 0.17 * U_L)
        rod_r = line3(pp_r, pw_r, color="#FFFFFF", thickness=0.065)
        rod_l = line3(pp_l, pw_l, color="#FFFFFF", thickness=0.065)

        sleeve_r = Cylinder(radius=0.41, height=1.5, direction=U_R, resolution=(8, 8), color="#90A4AE").move_to(1.48 * U_R + np.array([0, y_val, 0])).set_opacity(0.25)
        sleeve_l = Cylinder(radius=0.41, height=1.5, direction=U_L, resolution=(8, 8), color="#90A4AE").move_to(1.48 * U_L + np.array([0, y_val, 0])).set_opacity(0.25)

        crank_throw_0 = Cylinder(radius=0.16, height=0.6, direction=np.array([0, 1, 0]), resolution=(8, 8), color=COLOR_CRANK).move_to(np.array([0, y_val, 0]))

        v_pair_0 = Group(sleeve_r, sleeve_l, piston_r, piston_l, rod_r, rod_l, crank_throw_0)
        self.add(v_pair_0)

        # Designated proving shot nearly straight down crankshaft axis (phi≈88°, theta≈-83°)
        self.move_camera(
            phi=88.0 * DEGREES,
            theta=-83.0 * DEGREES,
            frame_center=np.array([0.0, y_val, 0.75]),
            zoom=1.35,
            run_time=1.8,
        )

        # Title and caption for Shot 3
        shot3_title = title("ทำไมต้องเป็นตัว V? จัดวาง 8 สูบให้กะทัดรัด", size=27)
        shot3_cap = caption_top("สองแถวเอียง 90° ทำให้ 8 สูบวางสั้นและกะทัดรัด", max_w=12.0)
        self.hud(shot3_title, shot3_cap)
        self.play(FadeIn(shot3_title), FadeIn(shot3_cap), run_time=0.8)

        # Bank axis lines in 3D world space
        axis_origin = np.array([0.0, y_val, 0.0])
        axis_line_l = line3(axis_origin, axis_origin + 2.3 * U_L, color=YELLOW, thickness=0.04)
        axis_line_r = line3(axis_origin, axis_origin + 2.3 * U_R, color=YELLOW, thickness=0.04)

        # Literal 90-degree right angle indicator
        # Corner square in the plane of the V (X-Z plane)
        sq_size = 0.35
        p_c = axis_origin
        p_l = p_c + sq_size * U_L
        p_r = p_c + sq_size * U_R
        p_corner = p_l + sq_size * U_R
        right_angle_sq = VGroup(
            line3(p_l, p_corner, color=COLOR_ACTIVE, thickness=0.035),
            line3(p_r, p_corner, color=COLOR_ACTIVE, thickness=0.035),
        )

        lbl_90deg = Text("90°", font_size=20, color=COLOR_ACTIVE)
        lbl_90deg.move_to(axis_origin + 0.65 * np.array([0.0, 0.0, 1.0]))
        self.world_text(lbl_90deg)

        self.play(
            FadeIn(axis_line_l),
            FadeIn(axis_line_r),
            FadeIn(right_angle_sq),
            FadeIn(lbl_90deg),
            run_time=1.2,
        )
        self.wait(1.0)

        # Only after angle is clearly visible, label Bank L and Bank R
        lbl_bank_l = Text("Bank L (แถวซ้าย)", font_size=18, color="#4FC3F7")
        lbl_bank_r = Text("Bank R (แถวขวา)", font_size=18, color="#81C784")
        lbl_bank_l.move_to(axis_origin + 2.1 * U_L + np.array([-0.3, 0.0, 0.2]))
        lbl_bank_r.move_to(axis_origin + 2.1 * U_R + np.array([0.3, 0.0, 0.2]))
        self.world_text(lbl_bank_l, lbl_bank_r)

        self.play(FadeIn(lbl_bank_l), FadeIn(lbl_bank_r), run_time=0.8)
        self.wait(1.0)

        # Pull camera back along crankshaft axis while replicating atomic pair at other 3 throws
        self.play(
            FadeOut(axis_line_l), FadeOut(axis_line_r),
            FadeOut(right_angle_sq), FadeOut(lbl_90deg),
            FadeOut(lbl_bank_l), FadeOut(lbl_bank_r),
            run_time=0.5,
        )

        # Pull back camera along Y axis
        self.move_camera(
            phi=68.0 * DEGREES,
            theta=-55.0 * DEGREES,
            frame_center=np.array([0.0, 0.0, 0.5]),
            zoom=0.95,
            run_time=1.8,
        )

        # Replicate atomic pair at Throw 1, Throw 2, Throw 3
        cap_replicate = caption_top("4 ข้อเหวี่ยง × 2 สูบต่อข้อ = 8 สูบในความยาวเครื่องเท่ากับ 4 สูบเรียง", color=OK)
        self.hud(cap_replicate)
        self.play(Transform(shot3_cap, cap_replicate), run_time=0.6)

        replicated_pairs = []
        for t_idx in [1, 2, 3]:
            y_t = THROWS_Y[t_idx]
            pr = build_piston_assembly(U_R).move_to(get_piston_wrist_pos(0.0, y_t, U_R) + 0.17 * U_R)
            pl = build_piston_assembly(U_L).move_to(get_piston_wrist_pos(0.0, y_t, U_L) + 0.17 * U_L)
            rr = line3(get_crankpin_pos(0.0, y_t, U_R, V_R), get_piston_wrist_pos(0.0, y_t, U_R), color="#FFFFFF", thickness=0.065)
            rl = line3(get_crankpin_pos(0.0, y_t, U_L, V_L), get_piston_wrist_pos(0.0, y_t, U_L), color="#FFFFFF", thickness=0.065)
            sr = Cylinder(radius=0.41, height=1.5, direction=U_R, resolution=(8, 8), color="#90A4AE").move_to(1.48 * U_R + np.array([0, y_t, 0])).set_opacity(0.25)
            sl = Cylinder(radius=0.41, height=1.5, direction=U_L, resolution=(8, 8), color="#90A4AE").move_to(1.48 * U_L + np.array([0, y_t, 0])).set_opacity(0.25)
            pair_mob = Group(pr, pl, rr, rl, sr, sl)
            replicated_pairs.append(pair_mob)

        # Reveal pairs sequentially along the crank axis
        for p in replicated_pairs:
            self.play(FadeIn(p), run_time=0.5)

        full_crank = build_crankshaft()
        self.play(FadeIn(full_crank), run_time=0.8)
        self.wait(1.2)

        # Clear Shot 3
        self.play(
            FadeOut(shot3_title),
            FadeOut(shot3_cap),
            FadeOut(v_pair_0),
            FadeOut(Group(*replicated_pairs)),
            FadeOut(full_crank),
            run_time=0.8,
        )

    # ==========================================================================
    # SHOT 4 IMPLEMENTATION
    # ==========================================================================
    def play_shot_4_staggered_firing(self):
        # Three-quarter view where both banks remain distinguishable
        self.move_camera(
            phi=68.0 * DEGREES,
            theta=-52.0 * DEGREES,
            frame_center=np.array([0.0, 0.0, 0.4]),
            zoom=0.95,
            run_time=1.0,
        )

        # Title and representative Ford Coyote firing order banner
        shot4_title = title("การจุดระเบิดสลับจังหวะ: 720° หารด้วย 8 สูบ", size=26)
        coyote_banner = Text("ตัวอย่าง Ford Coyote: 1–5–4–8–6–3–7–2", font_size=20, color=YELLOW).move_to(np.array([0.0, 3.05, 0.0]))
        coyote_disclaimer = Text("(ตัวอย่างลำดับการจุดระเบิด — ไม่ได้เหมือนกันทุกเครื่องยนต์ V8)", font_size=14, color=GRAYTXT).move_to(np.array([0.0, 2.75, 0.0]))
        shot4_cap = caption_top("8 สูบผลัดกันจุดระเบิดทุก 90° ลดช่องว่างการส่งแรง—เพลาหมุนต่อเนื่อง", max_w=12.0).move_to(np.array([0.0, 2.42, 0.0]))

        self.hud(shot4_title, coyote_banner, coyote_disclaimer, shot4_cap)
        self.play(
            FadeIn(shot4_title),
            FadeIn(coyote_banner),
            FadeIn(coyote_disclaimer),
            FadeIn(shot4_cap),
            run_time=1.0,
        )

        # Firing-Order Rail HUD across screen
        rail_badges = []
        rail_labels = []
        rail_sublabels = []
        badge_start_x = -4.2
        badge_spacing = 1.2

        for idx, cyl_num in enumerate(FIRING_ORDER):
            bank_letter = CYLINDER_SPECS[cyl_num][0]
            bx = badge_start_x + idx * badge_spacing
            by = 1.88
            bg = RoundedRectangle(width=0.92, height=0.52, corner_radius=0.1, fill_color="#1E293B", fill_opacity=0.85, stroke_color="#475569", stroke_width=1.5).move_to(np.array([bx, by, 0.0]))
            t_num = Text(f"{cyl_num}", font_size=18, color=WHITE).move_to(np.array([bx - 0.12, by, 0.0]))
            t_bank = Text(f"{bank_letter}", font_size=12, color="#94A3B8").move_to(np.array([bx + 0.22, by, 0.0]))
            rail_badges.append(bg)
            rail_labels.append(t_num)
            rail_sublabels.append(t_bank)

        rail_group = Group(*rail_badges, *rail_labels, *rail_sublabels)
        self.hud(rail_group)
        self.play(FadeIn(rail_group), run_time=0.8)

        # ----------------------------------------------------------------------
        # Professional Torque-vs-Crank-Angle Comparison Chart (HUD lower zone)
        # ----------------------------------------------------------------------
        c_x_min, c_x_max = -4.5, 4.5
        c_y_base = -3.4
        c_y_height = 1.15

        # Chart axes
        axis_x = line3(np.array([c_x_min, c_y_base, 0.0]), np.array([c_x_max, c_y_base, 0.0]), color="#64748B", thickness=0.02)
        axis_y = line3(np.array([c_x_min, c_y_base, 0.0]), np.array([c_x_min, c_y_base + c_y_height, 0.0]), color="#64748B", thickness=0.02)

        # Axis ticks and labels
        ticks = []
        tick_labels = []
        for deg_val in [0, 180, 360, 540, 720]:
            tx = c_x_min + (deg_val / 720.0) * (c_x_max - c_x_min)
            tick_line = line3(np.array([tx, c_y_base - 0.06, 0.0]), np.array([tx, c_y_base + 0.06, 0.0]), color="#64748B", thickness=0.015)
            t_lbl = Text(f"{deg_val}°", font_size=12, color=GRAYTXT).move_to(np.array([tx, c_y_base - 0.22, 0.0]))
            ticks.append(tick_line)
            tick_labels.append(t_lbl)

        lbl_chart_x = Text("มุมหมุนของเพลาข้อเหวี่ยง (องศา)", font_size=13, color=GRAYTXT).move_to(np.array([0.0, c_y_base - 0.44, 0.0]))
        lbl_chart_y = Text("ทอร์ก (Torque)", font_size=13, color=TORQUE).next_to(np.array([c_x_min, c_y_base + c_y_height, 0.0]), UP, buff=0.08)

        # Single cylinder pulse curve (only 1 pulse between 0° and 180°, then zero for 540°)
        pts_single = []
        for d in np.linspace(0, 720, 140):
            x_pos = c_x_min + (d / 720.0) * (c_x_max - c_x_min)
            t_val = np.sin(np.radians(d)) if (0 <= d <= 180) else 0.0
            y_pos = c_y_base + t_val * 0.75
            pts_single.append([x_pos, y_pos, 0.0])
        curve_single = VMobject(color="#475569", stroke_width=2.0)
        curve_single.set_points_smoothly([np.array(p) for p in pts_single])

        lbl_single_desc = Text("1 สูบ (ว่าง 540°)", font_size=12, color="#64748B").move_to(np.array([-2.5, c_y_base + 0.85, 0.0]))

        # 8-cylinder aggregate curve (continuous stream of torque pulses every 90°)
        pts_v8 = []
        for d in np.linspace(0, 720, 200):
            x_pos = c_x_min + (d / 720.0) * (c_x_max - c_x_min)
            # Sum pulses from all 8 firing events
            tot = 0.0
            for j in range(8):
                rel_d = (d - j * 90.0) % 720.0
                if 0 <= rel_d <= 180.0:
                    tot += np.sin(np.radians(rel_d)) * (1.0 + 0.25 * np.cos(np.radians(rel_d)))
            y_pos = c_y_base + (tot * 0.42 + 0.15)
            pts_v8.append([x_pos, y_pos, 0.0])
        curve_v8 = VMobject(color=TORQUE, stroke_width=3.5)
        curve_v8.set_points_smoothly([np.array(p) for p in pts_v8])

        lbl_v8_desc = Text("8 สูบ (ส่งแรงทุก 90° ต่อเนื่อง)", font_size=13, color=TORQUE).move_to(np.array([2.3, c_y_base + 0.95, 0.0]))

        chart_group = Group(axis_x, axis_y, *ticks, *tick_labels, lbl_chart_x, lbl_chart_y, curve_single, lbl_single_desc, curve_v8, lbl_v8_desc)
        self.hud(chart_group)
        self.play(FadeIn(chart_group), run_time=1.0)

        # Build full transparent 3D engine model
        block_trans = build_engine_block(opacity=0.22)
        crankshaft = build_crankshaft()
        sleeves = build_cylinder_sleeves()

        pistons = {}
        rods = {}
        wrist_dots = {}
        chamber_flashes = {}

        for cyl_id, (bank, t_idx, u_vec, v_vec) in CYLINDER_SPECS.items():
            y_t = THROWS_Y[t_idx]
            p = build_piston_assembly(u_vec)
            r = line3(ORIGIN, ORIGIN, color="#FFFFFF", thickness=0.065)
            wd = Dot(ORIGIN, radius=0.06, color="#B0BEC5")

            flash_mob = Cylinder(
                radius=0.38,
                height=0.22,
                direction=u_vec,
                resolution=(6, 6),
                color=COLOR_ACTIVE,
            ).move_to(np.array([0, y_t, 0]) + 1.8 * u_vec).set_opacity(0.0)

            pistons[cyl_id] = p
            rods[cyl_id] = r
            wrist_dots[cyl_id] = wd
            chamber_flashes[cyl_id] = flash_mob

        engine_3d = Group(block_trans, crankshaft, sleeves, *pistons.values(), *rods.values(), *wrist_dots.values(), *chamber_flashes.values())
        self.add(engine_3d)

        # Master updater for all 8 cylinders linked to master crank angle
        def update_all_cylinders(crank_deg):
            theta_rad = np.radians(crank_deg)
            for cid, (_, t_idx, u_vec, v_vec) in CYLINDER_SPECS.items():
                psi = FIRING_PHASES[cid]
                c_angle = np.radians((crank_deg - psi) % 360.0)
                y_t = THROWS_Y[t_idx]
                pw = get_piston_wrist_pos(c_angle, y_t, u_vec)
                pp = get_crankpin_pos(c_angle, y_t, u_vec, v_vec)

                pistons[cid].move_to(pw + 0.17 * u_vec)
                rods[cid].put_start_and_end_on(pp, pw)
                wrist_dots[cid].move_to(pw)

        update_all_cylinders(0.0)

        # Tracking cursor on torque chart
        cursor_line = line3(np.array([c_x_min, c_y_base, 0.0]), np.array([c_x_min, c_y_base + c_y_height, 0.0]), color=YELLOW, thickness=0.025)
        self.hud(cursor_line)
        self.add(cursor_line)

        # Animate master crank through 720 degrees, stepping through all 8 firing events
        # Every 90 degrees: exactly one cylinder flashes, badge lights up, torque pulse added
        for step_idx, cyl_fire in enumerate(FIRING_ORDER):
            deg_start = step_idx * 90.0
            deg_end = (step_idx + 1) * 90.0

            # Highlight current badge on firing rail
            curr_badge = rail_badges[step_idx]
            curr_num = rail_labels[step_idx]
            flash_cyl = chamber_flashes[cyl_fire]

            self.play(
                curr_badge.animate.set_fill(color=COLOR_POWER, opacity=1.0).set_stroke(color=YELLOW, width=2.5),
                curr_num.animate.set_color(WHITE),
                flash_cyl.animate.set_opacity(0.85).set_color(COLOR_ACTIVE),
                pistons[cyl_fire].animate.set_color(COLOR_ACTIVE),
                UpdateFromAlphaFunc(
                    engine_3d,
                    lambda m, a: update_all_cylinders(deg_start + a * 90.0),
                ),
                UpdateFromAlphaFunc(
                    cursor_line,
                    lambda m, a: cursor_line.put_start_and_end_on(
                        np.array([c_x_min + ((deg_start + a * 90.0) / 720.0) * (c_x_max - c_x_min), c_y_base, 0.0]),
                        np.array([c_x_min + ((deg_start + a * 90.0) / 720.0) * (c_x_max - c_x_min), c_y_base + c_y_height, 0.0]),
                    ),
                ),
                run_time=1.35,
                rate_func=linear,
            )

            # Dim previous flash back to normal
            self.play(
                curr_badge.animate.set_fill(color="#334155", opacity=0.85).set_stroke(color="#64748B", width=1.5),
                flash_cyl.animate.set_opacity(0.0),
                pistons[cyl_fire].animate.set_color(COLOR_METAL),
                run_time=0.15,
            )

        self.wait(1.0)

        # Clear Shot 4
        self.play(
            FadeOut(shot4_title),
            FadeOut(coyote_banner),
            FadeOut(coyote_disclaimer),
            FadeOut(shot4_cap),
            FadeOut(rail_group),
            FadeOut(chart_group),
            FadeOut(cursor_line),
            FadeOut(engine_3d),
            run_time=0.8,
        )

    # ==========================================================================
    # SHOT 5 IMPLEMENTATION
    # ==========================================================================
    def play_shot_5_payoff(self):
        # Establish dynamic perspective for payoff
        self.move_camera(
            phi=66.0 * DEGREES,
            theta=-48.0 * DEGREES,
            frame_center=np.array([0.2, 0.0, 0.4]),
            zoom=1.05,
            run_time=1.0,
        )

        shot5_title = title("เส้นทางการถ่ายทอดพลังงานกล", size=28)
        shot5_cap = caption_top("พลังงานเคมีจากการระเบิด → แรงดันลูกสูบ → ทอร์กเพลา → หมุนล้อขับเคลื่อน", max_w=12.0)
        self.hud(shot5_title, shot5_cap)
        self.play(FadeIn(shot5_title), FadeIn(shot5_cap), run_time=0.8)

        # Engine model for energy flow demonstration
        block = build_engine_block(opacity=0.30)
        crankshaft = build_crankshaft()
        sleeves = build_cylinder_sleeves()

        y_t0 = THROWS_Y[0]
        piston1 = build_piston_assembly(U_R).move_to(get_piston_wrist_pos(0.0, y_t0, U_R) + 0.17 * U_R)
        pp0 = get_crankpin_pos(0.0, y_t0, U_R, V_R)
        pw0 = get_piston_wrist_pos(0.0, y_t0, U_R)
        rod1 = line3(pp0, pw0, color="#FFFFFF", thickness=0.075)

        self.add(block, crankshaft, sleeves, piston1, rod1)

        # Moving highlight along literal connected components:
        # Step 1: Expanding gas at crown
        glow_crown = Dot(pw0 + 0.35 * U_R, radius=0.18, color=COLOR_POWER)
        lbl_step1 = Text("1. ก๊าซระเบิดขยายตัว", font_size=17, color=COLOR_POWER).move_to(np.array([-3.8, 1.8, 0.0]))
        self.hud(lbl_step1)
        self.play(FadeIn(glow_crown), FadeIn(lbl_step1), run_time=0.7)

        # Step 2: Piston force
        force_piston = arrow3(pw0 + 0.4 * U_R, pw0 + 0.1 * U_R, color=YELLOW, thickness=0.04)
        lbl_step2 = Text("2. ดันลูกสูบเลื่อนลง", font_size=17, color=YELLOW).move_to(np.array([-3.8, 1.3, 0.0]))
        self.hud(lbl_step2)
        self.play(FadeIn(force_piston), FadeIn(lbl_step2), run_time=0.7)

        # Step 3: Connecting rod transmission
        glow_rod = line3(pw0, pp0, color=COLOR_ACTIVE, thickness=0.09)
        lbl_step3 = Text("3. ก้านสูบถ่ายทอดแรง", font_size=17, color=COLOR_ACTIVE).move_to(np.array([-3.8, 0.8, 0.0]))
        self.hud(lbl_step3)
        self.play(FadeIn(glow_rod), FadeIn(lbl_step3), run_time=0.7)

        # Step 4: Crankshaft torque
        torque_ring = Arc(radius=0.48, start_angle=0.0, angle=270.0 * DEGREES, color=TORQUE, stroke_width=6)
        torque_ring.rotate(90.0 * DEGREES, axis=RIGHT).move_to(np.array([0.0, y_t0, 0.0]))
        lbl_step4 = Text("4. เกิดทอร์กหมุนเพลา", font_size=17, color=TORQUE).move_to(np.array([-3.8, 0.3, 0.0]))
        self.hud(lbl_step4)
        self.play(FadeIn(torque_ring), FadeIn(lbl_step4), run_time=0.7)

        # Step 5: Output shaft / flywheel rotation towards wheels
        flywheel_pos = np.array([0.0, 2.85, 0.0])
        spin_arrow = Arrow(flywheel_pos + np.array([0.6, 0.0, 0.0]), flywheel_pos + np.array([0.6, 0.8, 0.0]), color=OK, stroke_width=5)
        lbl_step5 = Text("5. ส่งกำลังสู่ล้อรถ", font_size=17, color=OK).move_to(np.array([-3.8, -0.2, 0.0]))
        self.hud(lbl_step5)
        self.play(FadeIn(spin_arrow), FadeIn(lbl_step5), run_time=0.7)
        self.wait(1.0)

        # Clear energy path callouts
        self.play(
            FadeOut(glow_crown), FadeOut(lbl_step1),
            FadeOut(force_piston), FadeOut(lbl_step2),
            FadeOut(glow_rod), FadeOut(lbl_step3),
            FadeOut(torque_ring), FadeOut(lbl_step4),
            FadeOut(spin_arrow), FadeOut(lbl_step5),
            FadeOut(shot5_title), FadeOut(shot5_cap),
            run_time=0.6,
        )

        # Smooth high-speed running finale with slow ambient rotation
        cap_smooth = caption_top("เมื่อ 8 สูบทำงานประสานกัน เพลาข้อเหวี่ยงจึงได้รับแรงขับเคลื่อนที่สม่ำเสมอและทรงพลัง", color=WHITE)
        self.hud(cap_smooth)
        self.play(FadeIn(cap_smooth), block.animate.set_opacity(0.65), run_time=0.8)

        # Fast rotation with ambient beauty orbit
        self.begin_ambient_camera_rotation(rate=0.18)
        self.play(
            crankshaft.animate.rotate(4.0 * TAU, axis=np.array([0.0, 1.0, 0.0]), about_point=ORIGIN),
            run_time=3.2,
            rate_func=linear,
        )
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(cap_smooth), run_time=0.4)

        # ----------------------------------------------------------------------
        # FINAL SUMMARY CARD
        # ----------------------------------------------------------------------
        card_bg = RoundedRectangle(
            width=9.2,
            height=3.4,
            corner_radius=0.18,
            fill_color="#0B132B",
            fill_opacity=0.92,
            stroke_color="#F59E0B",
            stroke_width=2.5,
        ).move_to(ORIGIN)

        card_title = Text("สรุปหัวใจสำคัญของเครื่องยนต์ V8", font_size=23, color="#F59E0B").move_to(np.array([0.0, 1.05, 0.0]))

        line1 = Text("1 สูบ: ดูด → อัด → กำลัง → คาย (720° ต่อรอบกำลัง)", font_size=19, color=WHITE).move_to(np.array([0.0, 0.42, 0.0]))
        line2 = Text("8 สูบ: ผลัดกันจุดระเบิดทุก 90° ในตัวอย่างนี้", font_size=19, color="#38BDF8").move_to(np.array([0.0, -0.15, 0.0]))
        line3 = Text("แรงเป็นจังหวะ → เพลาหมุนต่อเนื่องขึ้นอย่างเห็นได้ชัด", font_size=19, color="#4ADE80").move_to(np.array([0.0, -0.72, 0.0]))

        summary_card = Group(card_bg, card_title, line1, line2, line3)
        self.hud(summary_card)

        self.play(FadeIn(summary_card), run_time=1.0)
        self.wait(3.0)

        # Fade out all to conclude cleanly
        self.fade_out_all(run_time=1.0)
