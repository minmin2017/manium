"""
A clear, comprehensive F1 engineering explainer:
hybrid power to drivetrain, aero downforce from wings and floor,
tyre grip (F_grip <= mu * N), and braking energy recovery plus active aero.
"""

from mlib import *
import numpy as np

# -----------------------------------------------------------------------------
# Color Palette (adhering to Mayer signaling principle)
# -----------------------------------------------------------------------------
BG_COLOR = "#0D1117"        # Dark slate background
CAR_RED = "#E10600"         # F1 chassis bodywork
AIR_BLUE = "#4FC3F7"        # Aerodynamic airflow & low-drag DRS
FORCE_GREEN = "#66BB6A"     # Downforce and normal force vectors
ENERGY_GOLD = "#FFD54F"     # Electrical energy & MGU-K recovery
ICE_ORANGE = "#FF7043"      # Combustion thermal power & brake heat
COMBUSTION = ICE_ORANGE     # Alias for combustion / brake thermal
OK_CYAN = "#26C6DA"         # Drivetrain torque & tyre friction interface
TYRE_GRAY = "#263238"       # Tyre compound
RIM_WHITE = "#ECEFF1"       # Wheel rim & details


def make_label(text, point, color=WHITE, size=18):
    """Clean label helper positioned at a specific point."""
    return Text(text, font_size=size, color=color).move_to(point)


def top_view_f1(scale=0.85):
    """Clean, high-legibility top-view F1 car schematic."""
    floor = RoundedRectangle(
        width=5.8, height=1.1, corner_radius=0.22,
        color="#1E232A", fill_opacity=1.0, stroke_width=2, stroke_color="#30363D"
    )
    sidepods = RoundedRectangle(
        width=2.4, height=1.55, corner_radius=0.25,
        color=CAR_RED, fill_opacity=1.0, stroke_width=0
    ).move_to([-0.3, 0, 0])
    nose = Polygon(
        [2.9, 0.0, 0], [1.7, 0.35, 0], [1.7, -0.35, 0],
        color=CAR_RED, fill_opacity=1.0, stroke_width=0
    )
    cockpit = Ellipse(
        width=1.2, height=0.52,
        color="#11161D", fill_opacity=1.0, stroke_width=1.5, stroke_color="#455A64"
    ).move_to([-0.2, 0, 0])
    halo = Arc(
        radius=0.28, start_angle=-PI/2, angle=PI,
        color="#90A4AE", stroke_width=4
    ).move_to([0.2, 0, 0])

    # Aerodynamic wings
    front_wing = RoundedRectangle(
        width=0.28, height=2.5, corner_radius=0.06,
        color=CAR_RED, fill_opacity=1.0, stroke_width=0
    ).move_to([2.75, 0, 0])
    rear_wing = RoundedRectangle(
        width=0.35, height=2.1, corner_radius=0.08,
        color=CAR_RED, fill_opacity=1.0, stroke_width=0
    ).move_to([-2.65, 0, 0])

    # 4 Tyres
    wheel_coords = [
        (1.75, 1.05, 0), (1.75, -1.05, 0),    # Front wheels
        (-1.95, 1.0, 0), (-1.95, -1.0, 0)     # Rear wheels
    ]
    wheels = VGroup(*[
        RoundedRectangle(
            width=0.55, height=0.92, corner_radius=0.15,
            color=TYRE_GRAY, fill_opacity=1.0, stroke_width=1.5, stroke_color="#546E7A"
        ).move_to(pos)
        for pos in wheel_coords
    ])

    car = VGroup(floor, sidepods, nose, cockpit, halo, front_wing, rear_wing, wheels)
    return car.scale(scale)


def side_profile_f1(scale=1.0):
    """Side profile schematic highlighting wings and underfloor ground-effect channels."""
    f_wheel = Circle(radius=0.45, color=TYRE_GRAY, fill_opacity=1.0, stroke_width=2, stroke_color="#546E7A").move_to([2.0, -0.95, 0])
    r_wheel = Circle(radius=0.45, color=TYRE_GRAY, fill_opacity=1.0, stroke_width=2, stroke_color="#546E7A").move_to([-2.0, -0.95, 0])
    f_rim = Circle(radius=0.20, color=RIM_WHITE, fill_opacity=0.3, stroke_width=2, stroke_color=RIM_WHITE).move_to([2.0, -0.95, 0])
    r_rim = Circle(radius=0.20, color=RIM_WHITE, fill_opacity=0.3, stroke_width=2, stroke_color=RIM_WHITE).move_to([-2.0, -0.95, 0])

    chassis_pts = [
        [2.8, -1.15, 0],    # Nose tip
        [1.5, -0.70, 0],    # Nose ramp up
        [0.3, -0.55, 0],    # Cockpit rim
        [-0.4, -0.15, 0],   # Airbox intake
        [-1.7, -0.55, 0],   # Engine cover spine
        [-2.3, -0.85, 0],   # Rear deck
        [-1.8, -1.05, 0],   # Diffuser exit (expanded upward)
        [-0.4, -1.30, 0],   # Venturi throat (lowest point)
        [1.6, -1.25, 0],    # Underfloor inlet
    ]
    chassis = Polygon(*chassis_pts, color=CAR_RED, fill_opacity=0.9, stroke_width=0)

    # Front Wing profile
    fw_pts = [[2.6, -1.25, 0], [3.1, -1.20, 0], [3.1, -1.05, 0], [2.7, -1.15, 0]]
    f_wing = Polygon(*fw_pts, color=CAR_RED, fill_opacity=1.0, stroke_width=0)

    # Rear Wing assembly
    rw_endplate = Rectangle(width=0.2, height=0.75, color=CAR_RED, fill_opacity=1.0, stroke_width=0).move_to([-2.5, -0.3, 0])
    rw_element = RoundedRectangle(width=0.55, height=0.12, corner_radius=0.04, color=AIR_BLUE, fill_opacity=1.0, stroke_width=0).move_to([-2.45, -0.1, 0])

    # Venturi underfloor tunnel outline
    floor_tunnel = VMobject(color=AIR_BLUE, stroke_width=3)
    floor_tunnel.set_points_as_corners([[1.6, -1.28, 0], [-0.4, -1.33, 0], [-1.9, -1.05, 0]])

    car = VGroup(f_wheel, r_wheel, f_rim, r_rim, chassis, f_wing, rw_endplate, rw_element, floor_tunnel)
    return car.scale(scale)


class F1EngineeringExplainer(SafeScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # =====================================================================
        # Section 0: Hook & High-level Engineering Overview (~4.5s)
        # =====================================================================
        s0_title = title("F1 Car Engineering — How Physics Drives Lap Time", color=WHITE, size=28)
        s0_cap = caption_top("A Formula 1 car is an integrated system of energy, aerodynamics, and tyre grip.", color=GRAYTXT, size=20)
        car_top = top_view_f1(scale=0.82).move_to([0.0, -0.45, 0])

        tag_aero_f = make_label("Front Wing & Floor\n(Downforce)", [3.6, 1.5, 0], AIR_BLUE, 16)
        tag_aero_r = make_label("Rear Wing & DRS\n(Active Aero)", [-3.6, 1.5, 0], AIR_BLUE, 16)
        tag_tyre_f = make_label("Front Tyres\n(Steering & Braking)", [3.6, -1.9, 0], OK_CYAN, 16)
        tag_power = make_label("Hybrid Power Unit\n(ICE + MGU-K)", [-3.6, -1.9, 0], ENERGY_GOLD, 16)
        tags_group = VGroup(tag_aero_f, tag_aero_r, tag_tyre_f, tag_power)

        self.play(FadeIn(s0_title, shift=UP*0.25), FadeIn(s0_cap, shift=UP*0.15),
                  FadeIn(car_top, shift=DOWN*0.2), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.1) for t in tags_group], lag_ratio=0.15), run_time=1.0)
        self.wait(2.2)
        self.fade_out_all(run_time=0.7)

        # =====================================================================
        # Section 1: Hybrid Power to Drivetrain (~10.5s)
        # =====================================================================
        s1_title = title("1. Hybrid Power Unit to Drivetrain", color=WHITE, size=28)
        s1_cap = caption_top("Combustion engine and electric motor combine torque to drive the rear wheels.", color=ENERGY_GOLD, size=20)

        # ICE Block
        ice_box = RoundedRectangle(width=2.8, height=1.2, corner_radius=0.15,
                                   color=ICE_ORANGE, fill_opacity=0.85, stroke_width=0).move_to([-4.0, 0.7, 0])
        ice_lbl = Text("V6 Turbo ICE", font_size=18, color=WHITE, weight=BOLD).move_to([-4.0, 0.92, 0])
        ice_sub = Text("Continuous Fuel Power", font_size=14, color="#FFE0B2").move_to([-4.0, 0.52, 0])
        ice_group = VGroup(ice_box, ice_lbl, ice_sub)

        # Battery & MGU-K Block
        batt_box = RoundedRectangle(width=2.8, height=1.2, corner_radius=0.15,
                                    color=ENERGY_GOLD, fill_opacity=0.85, stroke_width=0).move_to([-4.0, -0.9, 0])
        batt_lbl = Text("Battery & MGU-K", font_size=18, color=BLACK, weight=BOLD).move_to([-4.0, -0.68, 0])
        batt_sub = Text("Instant Electric Torque", font_size=14, color="#37474F").move_to([-4.0, -1.08, 0])
        batt_group = VGroup(batt_box, batt_lbl, batt_sub)

        # Transmission / Drivetrain Box
        trans_box = RoundedRectangle(width=2.5, height=1.4, corner_radius=0.15,
                                     color=OK_CYAN, fill_opacity=0.85, stroke_width=0).move_to([-0.3, -0.1, 0])
        trans_lbl = Text("Drivetrain", font_size=19, color=BLACK, weight=BOLD).move_to([-0.3, 0.15, 0])
        trans_sub = Text("Torque Blending Node", font_size=14, color="#004D40").move_to([-0.3, -0.28, 0])
        trans_group = VGroup(trans_box, trans_lbl, trans_sub)

        # Rear Axle & Tyres
        rear_axle = Line([3.6, 0.8, 0], [3.6, -1.0, 0], color=WHITE, stroke_width=5)
        tyre_top = RoundedRectangle(width=0.55, height=0.85, corner_radius=0.12,
                                    color=TYRE_GRAY, fill_opacity=1.0, stroke_width=2, stroke_color=WHITE).move_to([3.6, 0.8, 0])
        tyre_bot = RoundedRectangle(width=0.55, height=0.85, corner_radius=0.12,
                                    color=TYRE_GRAY, fill_opacity=1.0, stroke_width=2, stroke_color=WHITE).move_to([3.6, -1.0, 0])
        axle_lbl = Text("Rear Drive Wheels", font_size=17, color=WHITE).move_to([3.6, 1.5, 0])
        traction_arrow_1 = Arrow([3.9, 0.8, 0], [4.9, 0.8, 0], color=OK_CYAN, buff=0, stroke_width=5)
        traction_arrow_2 = Arrow([3.9, -1.0, 0], [4.9, -1.0, 0], color=OK_CYAN, buff=0, stroke_width=5)
        axle_group = VGroup(rear_axle, tyre_top, tyre_bot, axle_lbl, traction_arrow_1, traction_arrow_2)

        # Power Flow Arrows
        arrow_ice = Arrow(ice_box.get_right(), trans_box.get_left() + UP*0.25, color=ICE_ORANGE, buff=0.12, stroke_width=5)
        arrow_elec = Arrow(batt_box.get_right(), trans_box.get_left() + DOWN*0.25, color=ENERGY_GOLD, buff=0.12, stroke_width=5)
        arrow_prop = Arrow(trans_box.get_right(), [3.3, -0.1, 0], color=OK_CYAN, buff=0.12, stroke_width=6)

        # Engineering explanation text
        s1_note1 = Text("• ICE provides sustained high-RPM horsepower", font_size=17, color=GRAYTXT).move_to([0, -2.1, 0])
        s1_note2 = Text("• MGU-K injects instant electric torque to eliminate turbo lag", font_size=17, color=GRAYTXT).move_to([0, -2.55, 0])

        self.play(FadeIn(s1_title), FadeIn(s1_cap),
                  FadeIn(ice_group), FadeIn(batt_group), FadeIn(trans_group), FadeIn(axle_group),
                  run_time=1.2)
        self.play(GrowArrow(arrow_ice), GrowArrow(arrow_elec), run_time=1.0)
        self.play(GrowArrow(arrow_prop), run_time=0.8)
        self.play(FadeIn(s1_note1), FadeIn(s1_note2), run_time=1.0)
        self.wait(3.8)
        self.play(Indicate(trans_box, color=WHITE), Indicate(traction_arrow_1, color=WHITE), Indicate(traction_arrow_2, color=WHITE), run_time=0.8)
        self.wait(1.0)
        self.fade_out_all(run_time=0.7)

        # =====================================================================
        # Section 2: Aero Downforce from Wings and Floor (~11.0s)
        # =====================================================================
        s2_title = title("2. Aerodynamics: Downforce from Wings and Floor", color=WHITE, size=28)
        s2_cap = caption_top("Wings deflect air upward; underfloor Venturi tunnels create ground suction.", color=AIR_BLUE, size=20)

        # Tarmac line & Car side profile
        track = Line([-6.0, -1.45, 0], [0.5, -1.45, 0], color="#455A64", stroke_width=3)
        car_side = side_profile_f1(scale=0.9).move_to([-2.6, -0.4, 0])

        # Streamlines
        stream_top = CurvedArrow(np.array([0.0, -0.9, 0]), np.array([-4.5, 0.8, 0]), radius=-4.0, color=AIR_BLUE, stroke_width=3)
        stream_floor = CurvedArrow(np.array([-0.8, -1.35, 0]), np.array([-4.3, -1.0, 0]), radius=5.0, color=AIR_BLUE, stroke_width=3.5)

        # Downforce arrows (pointing down)
        f_front = Arrow([-0.1, -0.3, 0], [-0.1, -1.15, 0], color=FORCE_GREEN, buff=0, stroke_width=5)
        f_floor = Arrow([-2.6, 0.4, 0], [-2.6, -0.85, 0], color=FORCE_GREEN, buff=0, stroke_width=7)
        f_rear = Arrow([-4.8, 1.2, 0], [-4.8, 0.25, 0], color=FORCE_GREEN, buff=0, stroke_width=5)
        downforce_arrows = VGroup(f_front, f_floor, f_rear)

        lbl_f_front = Text("Front Wing", font_size=15, color=FORCE_GREEN).move_to([-0.1, -0.1, 0])
        lbl_f_floor = Text("Floor Suction (Venturi)", font_size=16, color=FORCE_GREEN).move_to([-2.6, 0.65, 0])
        lbl_f_rear = Text("Rear Wing", font_size=15, color=FORCE_GREEN).move_to([-4.8, 1.45, 0])
        df_labels = VGroup(lbl_f_front, lbl_f_floor, lbl_f_rear)

        # Pressure callouts
        p_top = Text("P_ambient", font_size=14, color=AIR_BLUE).move_to([-2.6, 1.25, 0])
        p_under = Text("P_under < P_ambient", font_size=15, color=ENERGY_GOLD).move_to([-2.6, -1.75, 0])
        p_labels = VGroup(p_top, p_under)

        # Formula & Physics Panel (Right side)
        s2_box = RoundedRectangle(width=4.4, height=3.8, corner_radius=0.18,
                                  color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color="#30363D").move_to([4.3, -0.4, 0])
        s2_panel_title = Text("Aerodynamic Downforce", font_size=18, color=AIR_BLUE, weight=BOLD).move_to([4.3, 1.15, 0])
        s2_eq = MathTex(r"F_{\mathrm{down}} = \frac{1}{2}\rho v^2 A C_L", color=FORCE_GREEN).scale(0.85).move_to([4.3, 0.55, 0])
        s2_line1 = Text("• Scales with speed squared (v^2)", font_size=16, color=WHITE).move_to([4.3, -0.05, 0])
        s2_line2 = Text("• Air deflection creates down reaction", font_size=15, color=GRAYTXT).move_to([4.3, -0.45, 0])
        s2_line3 = Text("• Venturi tunnels generate suction", font_size=15, color=GRAYTXT).move_to([4.3, -0.85, 0])
        s2_line4 = Text("• Adds tyre load with zero added mass", font_size=15, color=ENERGY_GOLD).move_to([4.3, -1.35, 0])
        s2_panel = VGroup(s2_box, s2_panel_title, s2_eq, s2_line1, s2_line2, s2_line3, s2_line4)

        self.play(FadeIn(s2_title), FadeIn(s2_cap), Create(track), FadeIn(car_side), run_time=1.2)
        self.play(Create(stream_top), Create(stream_floor), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in downforce_arrows], lag_ratio=0.15),
                  FadeIn(df_labels), FadeIn(p_labels), run_time=1.2)
        self.play(FadeIn(s2_panel, shift=LEFT*0.2), run_time=1.0)
        self.wait(3.8)
        self.play(Indicate(s2_eq, color=FORCE_GREEN), Indicate(f_floor, color=WHITE), run_time=0.8)
        self.wait(1.0)
        self.fade_out_all(run_time=0.7)

        # =====================================================================
        # Section 3: Tyre Grip Interface (~11.0s)
        # =====================================================================
        s3_title = title("3. Tyre Grip Interface: F_grip <= mu * N", color=WHITE, size=28)
        s3_cap = caption_top("Tyres convert vertical load into extreme cornering and braking forces.", color=FORCE_GREEN, size=20)

        # Free Body Diagram of Tyre on Track Surface
        track_s3 = Line([-6.2, -1.8, 0], [-0.5, -1.8, 0], color="#455A64", stroke_width=4)
        tyre_body = RoundedRectangle(width=1.6, height=2.2, corner_radius=0.35,
                                     color=TYRE_GRAY, fill_opacity=1.0, stroke_width=2, stroke_color="#78909C").move_to([-3.4, -0.7, 0])
        hub_center = Dot([-3.4, -0.7, 0], radius=0.12, color=WHITE)
        contact_patch = RoundedRectangle(width=1.2, height=0.14, corner_radius=0.04,
                                         color=OK_CYAN, fill_opacity=1.0, stroke_width=0).move_to([-3.4, -1.8, 0])
        contact_lbl = Text("Contact Patch", font_size=14, color=OK_CYAN).move_to([-3.4, -2.15, 0])
        tyre_fbd = VGroup(track_s3, tyre_body, hub_center, contact_patch, contact_lbl)

        # Force Vectors acting on Tyre
        arrow_w = Arrow([-4.1, 0.4, 0], [-4.1, -0.6, 0], color="#B0BEC5", buff=0, stroke_width=5)
        lbl_w = MathTex(r"W = mg", color="#B0BEC5").scale(0.75).move_to([-4.8, -0.1, 0])

        arrow_aero = Arrow([-2.7, 0.8, 0], [-2.7, -0.6, 0], color=FORCE_GREEN, buff=0, stroke_width=6)
        lbl_aero = MathTex(r"F_{\mathrm{down}}", color=FORCE_GREEN).scale(0.75).move_to([-2.0, 0.1, 0])

        arrow_n = Arrow([-3.4, -1.8, 0], [-3.4, 0.5, 0], color=FORCE_GREEN, buff=0, stroke_width=7)
        lbl_n = MathTex(r"N = mg + F_{\mathrm{down}}", color=FORCE_GREEN).scale(0.8).move_to([-3.4, 0.85, 0])

        arrow_grip = Arrow([-3.4, -1.8, 0], [-1.0, -1.8, 0], color=OK_CYAN, buff=0, stroke_width=7)
        lbl_grip = MathTex(r"F_{\mathrm{grip}}", color=OK_CYAN).scale(0.85).move_to([-1.0, -1.45, 0])

        # Physics & Equations Panel (Right side)
        s3_box = RoundedRectangle(width=5.2, height=3.8, corner_radius=0.18,
                                  color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color="#30363D").move_to([3.8, -0.4, 0])
        s3_p_title = Text("Friction & Cornering Limits", font_size=18, color=OK_CYAN, weight=BOLD).move_to([3.8, 1.15, 0])
        s3_eq1 = MathTex(r"F_{\mathrm{grip}} \le \mu N = \mu (m g + F_{\mathrm{down}})", color=FORCE_GREEN).scale(0.80).move_to([3.8, 0.55, 0])
        s3_eq2 = MathTex(r"a_{\mathrm{corner}} = \frac{F_{\mathrm{grip}}}{m} \le \mu \left( g + \frac{F_{\mathrm{down}}}{m} \right)", color=OK_CYAN).scale(0.80).move_to([3.8, -0.15, 0])

        s3_note1 = Text("• Friction limit scales directly with normal load N", font_size=15, color=WHITE).move_to([3.8, -0.75, 0])
        s3_note2 = Text("• Downforce increases N without adding mass m", font_size=15, color=GRAYTXT).move_to([3.8, -1.15, 0])
        s3_note3 = Text("• Enables 4-5g lateral acceleration at high speed", font_size=15, color=ENERGY_GOLD).move_to([3.8, -1.55, 0])
        s3_panel = VGroup(s3_box, s3_p_title, s3_eq1, s3_eq2, s3_note1, s3_note2, s3_note3)

        self.play(FadeIn(s3_title), FadeIn(s3_cap), FadeIn(tyre_fbd), run_time=1.2)
        self.play(GrowArrow(arrow_w), FadeIn(lbl_w), GrowArrow(arrow_aero), FadeIn(lbl_aero), run_time=1.2)
        self.play(GrowArrow(arrow_n), FadeIn(lbl_n), GrowArrow(arrow_grip), FadeIn(lbl_grip), run_time=1.2)
        self.play(FadeIn(s3_panel, shift=LEFT*0.2), run_time=1.0)
        self.wait(3.8)
        self.play(Indicate(s3_eq1, color=FORCE_GREEN), Indicate(arrow_grip, color=WHITE), run_time=0.8)
        self.wait(1.0)
        self.fade_out_all(run_time=0.7)

        # =====================================================================
        # Section 4: Braking Energy Recovery & Active Aero (~11.0s)
        # =====================================================================
        s4_title = title("4. Energy Recovery & Active Aerodynamics", color=WHITE, size=28)
        s4_cap = caption_top("Braking harvests battery energy; active wings trade downforce for straight-line speed.", color=ICE_ORANGE, size=20)

        # Left Column: Braking Energy Recovery
        s4_left_box = RoundedRectangle(width=5.0, height=3.8, corner_radius=0.18,
                                       color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color="#30363D").move_to([-3.4, -0.4, 0])
        s4_l_title = Text("Regenerative Braking (MGU-K)", font_size=17, color=ICE_ORANGE, weight=BOLD).move_to([-3.4, 1.15, 0])

        # Brake wheel & MGU-K diagram
        wheel_s4 = Circle(radius=0.55, color=TYRE_GRAY, fill_opacity=1.0, stroke_width=2, stroke_color=WHITE).move_to([-4.8, 0.25, 0])
        disc_s4 = Circle(radius=0.28, color=ICE_ORANGE, fill_opacity=0.85, stroke_width=0).move_to([-4.8, 0.25, 0])
        wheel_lbl = Text("Braking Wheel", font_size=13, color=WHITE).move_to([-4.8, -0.48, 0])

        mguk_box = RoundedRectangle(width=1.5, height=0.75, corner_radius=0.1,
                                    color=ENERGY_GOLD, fill_opacity=0.85, stroke_width=0).move_to([-2.2, 0.25, 0])
        mguk_lbl = Text("MGU-K", font_size=15, color=BLACK, weight=BOLD).move_to([-2.2, 0.25, 0])

        batt_s4 = RoundedRectangle(width=2.0, height=0.65, corner_radius=0.1,
                                   color=ENERGY_GOLD, fill_opacity=0.85, stroke_width=0).move_to([-3.4, -1.0, 0])
        batt_s4_lbl = Text("Battery Store", font_size=15, color=BLACK, weight=BOLD).move_to([-3.4, -1.0, 0])

        arrow_regen_1 = Arrow([-4.1, 0.25, 0], [-3.1, 0.25, 0], color=ICE_ORANGE, buff=0.1, stroke_width=5)
        arrow_regen_2 = Arrow([-2.2, -0.2, 0], [-2.8, -0.65, 0], color=ENERGY_GOLD, buff=0.1, stroke_width=5)

        s4_l_note = Text("Kinetic energy -> Stored electrical energy", font_size=14, color=GRAYTXT).move_to([-3.4, -1.65, 0])
        left_group = VGroup(s4_left_box, s4_l_title, wheel_s4, disc_s4, wheel_lbl, mguk_box, mguk_lbl, batt_s4, batt_s4_lbl, s4_l_note)

        # Right Column: Active Aero (Drag vs Downforce)
        s4_right_box = RoundedRectangle(width=5.0, height=3.8, corner_radius=0.18,
                                        color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color="#30363D").move_to([3.4, -0.4, 0])
        s4_r_title = Text("Active Aero: Drag vs Downforce", font_size=17, color=AIR_BLUE, weight=BOLD).move_to([3.4, 1.15, 0])
        s4_drag_eq = MathTex(r"F_{\mathrm{drag}} = \frac{1}{2}\rho v^2 A C_D", color=AIR_BLUE).scale(0.80).move_to([3.4, 0.55, 0])

        # Active wing schematic
        wing_main = Line([1.8, -0.15, 0], [3.2, -0.15, 0], color="#90A4AE", stroke_width=6)
        wing_flap = Line([3.2, -0.15, 0], [4.6, 0.35, 0], color=AIR_BLUE, stroke_width=7)

        mode_corner = Text("Cornering: High wing angle -> Maximum Downforce", font_size=14, color=FORCE_GREEN).move_to([3.4, -0.75, 0])
        mode_straight = Text("Straight (DRS): Flap opens -> Sheds Drag for Speed", font_size=14, color=AIR_BLUE).move_to([3.4, -1.15, 0])
        s4_r_note = Text("Balancing lap time: Grip in turns vs Speed on straights", font_size=14, color=GRAYTXT).move_to([3.4, -1.65, 0])
        right_group = VGroup(s4_right_box, s4_r_title, s4_drag_eq, wing_main, wing_flap, mode_corner, mode_straight, s4_r_note)

        self.play(FadeIn(s4_title), FadeIn(s4_cap), FadeIn(left_group), FadeIn(right_group), run_time=1.2)
        self.play(GrowArrow(arrow_regen_1), GrowArrow(arrow_regen_2),
                  Indicate(disc_s4, color=WHITE), run_time=1.2)
        # DRS flap rotates to flat/open low drag position
        self.play(Rotate(wing_flap, angle=-25*DEGREES, about_point=np.array([3.2, -0.15, 0])),
                  Indicate(mode_straight, color=WHITE), run_time=1.2)
        self.wait(3.8)
        self.play(Indicate(batt_s4, color=WHITE), Indicate(wing_flap, color=WHITE), run_time=0.8)
        self.wait(1.0)
        self.fade_out_all(run_time=0.7)

        # =====================================================================
        # Section 5: Engineering Synthesis & System Balance (~5.8s)
        # =====================================================================
        s5_title = title("F1 Engineering: Integrated System Balance", color=WHITE, size=28)
        s5_cap = caption_top("Every fast lap is a closed-loop balance of energy, aerodynamics, and tyre grip.", color=WHITE, size=20)

        # 4 System summary cards
        c1 = RoundedRectangle(width=5.2, height=1.3, corner_radius=0.15, color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color=ICE_ORANGE).move_to([-3.0, 0.8, 0])
        c1_t = Text("1. Hybrid Power Unit", font_size=16, color=ICE_ORANGE, weight=BOLD).move_to([-3.0, 1.15, 0])
        c1_d = Text("ICE continuous propulsion blended with instant MGU-K electric torque.", font_size=13, color=GRAYTXT).move_to([-3.0, 0.65, 0])
        card1 = VGroup(c1, c1_t, c1_d)

        c2 = RoundedRectangle(width=5.2, height=1.3, corner_radius=0.15, color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color=AIR_BLUE).move_to([3.0, 0.8, 0])
        c2_t = Text("2. Aerodynamics", font_size=16, color=AIR_BLUE, weight=BOLD).move_to([3.0, 1.15, 0])
        c2_d = Text("Wings and underfloor Venturi suction generate downforce scaling with v^2.", font_size=13, color=GRAYTXT).move_to([3.0, 0.65, 0])
        card2 = VGroup(c2, c2_t, c2_d)

        c3 = RoundedRectangle(width=5.2, height=1.3, corner_radius=0.15, color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color=FORCE_GREEN).move_to([-3.0, -0.85, 0])
        c3_t = Text("3. Tyre Friction Interface", font_size=16, color=FORCE_GREEN, weight=BOLD).move_to([-3.0, -0.5, 0])
        c3_d = Text("Downforce raises normal force N, multiplying tyre grip without extra mass.", font_size=13, color=GRAYTXT).move_to([-3.0, -1.0, 0])
        card3 = VGroup(c3, c3_t, c3_d)

        c4 = RoundedRectangle(width=5.2, height=1.3, corner_radius=0.15, color="#1E232A", fill_opacity=0.9, stroke_width=1.5, stroke_color=OK_CYAN).move_to([3.0, -0.85, 0])
        c4_t = Text("4. Energy & Drag Management", font_size=16, color=OK_CYAN, weight=BOLD).move_to([3.0, -0.5, 0])
        c4_d = Text("Braking kinetic energy is recovered; active aero sheds drag on straights.", font_size=13, color=GRAYTXT).move_to([3.0, -1.0, 0])
        card4 = VGroup(c4, c4_t, c4_d)

        summary_banner = Text("Performance = continuous physical optimization across all four systems.", font_size=17, color=WHITE, weight=BOLD).move_to([0, -2.1, 0])

        self.play(FadeIn(s5_title), FadeIn(s5_cap),
                  FadeIn(card1, shift=UP*0.2), FadeIn(card2, shift=UP*0.2),
                  FadeIn(card3, shift=DOWN*0.2), FadeIn(card4, shift=DOWN*0.2),
                  run_time=1.2)
        self.play(FadeIn(summary_banner, shift=UP*0.15), run_time=0.8)
        self.wait(3.5)
        self.fade_out_all(run_time=0.7)
