"""
building_flyin.py — Cinematic 3D Architectural Fly-In.

Scene: BuildingFlyIn
Visual piece: Modern dusk/night skyscraper architectural visualization
with a cinematic camera fly-in that starts outside with a wide establishing
shot and glides smoothly into the brightly illuminated podium lobby.
Built for Manim Community Edition using mlib.SafeThreeDScene.
"""

from manim import *
from mlib import SafeThreeDScene
import numpy as np


# =============================================================================
# COLOR PALETTE (Dusk / Night Architectural Palette)
# =============================================================================
# Sky & Atmosphere
BG_SKY = "#0B1020"           # Deep twilight / night sky

# Hero Skyscraper Geometry
HERO_FACADE = "#1E2A3A"      # Main building mass (dark slate blue-grey)
HERO_ACCENT = "#243447"      # Setback reveals & trim bands
HERO_CROWN = "#2C3E52"       # Mechanical penthouse & rooftop crown

# Context / Neighbour Buildings
NEIGHBOR_MASS_1 = "#121924"  # Background building mass 1 (deeper navy)
NEIGHBOR_MASS_2 = "#151F2C"  # Background building mass 2
NEIGHBOR_MASS_3 = "#101620"  # Background building mass 3

# Facade Windows
WIN_WARM_1 = "#FFD48A"       # Warm golden interior light (majority)
WIN_WARM_2 = "#FFC46B"       # Warm amber interior light (majority)
WIN_COOL_ACC = "#80DEEA"     # Subtle cool office display glow (rare accent)
WIN_DARK = "#101826"         # Unlit / dark window (minority)

# Plaza, Street & Landscape
GROUND_PLAZA = "#0E1520"     # Dark stone plaza surface
WALKWAY_COLOR = "#16202D"    # Pedestrian approach walkway
ROAD_ASPHALT = "#070B12"     # Street asphalt strip
ROAD_MARKING = "#455A64"     # Road center dashed line
TAIL_LIGHT_RED = "#E53935"   # Long exposure car tail-light streak
HEAD_LIGHT_AMB = "#FFE082"   # Long exposure car headlight streak
BOLLARD_LIGHT = "#FFD54F"    # Plaza pathway light bollards
TREE_TRUNK_COL = "#3E2723"   # Low-poly tree trunk
TREE_CANOPY_1 = "#1B3B2B"    # Deep pine green canopy
TREE_CANOPY_2 = "#234E37"    # Forest green canopy

# Podium & Entrance
PODIUM_CANOPY = "#222D38"    # Thin cantilevered entrance canopy
CANOPY_LIGHT = "#FFE082"     # Underside canopy illumination strip
GLASS_DOORS = "#80DEEA"      # Semi-transparent glass entrance doors

# Interior Lobby (Warm, Glowing, Inviting)
LOBBY_FLOOR = "#26201B"      # Polished dark timber / stone floor
LOBBY_POOL_1 = "#FFE1B0"     # Warm floor light reflection pool (bright)
LOBBY_POOL_2 = "#FFD285"     # Warm floor light reflection pool (amber)
LOBBY_CEILING = "#171D27"    # Dark recessed ceiling slab
CEILING_LIGHT = "#FFF4DA"    # Glowing ceiling light panels
CEILING_LIGHT_HI = "#FFFDF5" # High-intensity central troffer
COLUMN_BODY = "#37474F"      # Fluted architectural pillars
COLUMN_TRIM = "#D4AF37"      # Satin brass column collar rings
RECEPTION_BODY = "#2E1D13"   # Dark walnut reception desk
RECEPTION_GLOW = "#FFE3A8"   # Backlit glowing onyx front feature panel
DESK_COUNTER = "#C5A059"     # Satin brass reception counter
TERMINAL_SCREEN = "#80D8FF"  # Reception desk screen accent
LOUNGE_LEATHER = "#1B2632"   # Navy leather seating blocks
LOUNGE_BRASS = "#B7950B"     # Brushed brass accent coffee table
ELEVATOR_PANEL = "#1E1712"   # Dark architectural wood feature backdrop
ELEVATOR_BRASS = "#D4AF37"   # Metallic gold elevator doors
ELEVATOR_SEAM = "#120D0A"    # Door gap center seam
ELEVATOR_INDIC = "#FFF9C4"   # Illuminated elevator floor indicator displays
PLANT_LEAVES = "#2E7D32"     # Lobby interior architectural planter


# =============================================================================
# GEOMETRY HELPERS
# =============================================================================
def make_3d_polygon(pts, color, opacity=1.0):
    """Creates a flat polygon in 3D coordinates with shade_in_3d enabled."""
    poly = Polygon(*pts, fill_color=color, fill_opacity=opacity, stroke_width=0, stroke_opacity=0)
    poly.shade_in_3d = True
    return poly


def make_window_poly(center, width, height, plane, color, opacity=1.0):
    """
    Creates a flat 2D rectangular window polygon placed in 3D space.
    plane: '-Y' (faces front, in XZ plane)
           '+X' (faces right, in YZ plane)
           '+Z' (faces up, in XY plane)
    """
    cx, cy, cz = center
    w2 = width / 2.0
    h2 = height / 2.0
    if plane == "-Y":
        pts = [
            np.array([cx - w2, cy, cz - h2]),
            np.array([cx + w2, cy, cz - h2]),
            np.array([cx + w2, cy, cz + h2]),
            np.array([cx - w2, cy, cz + h2]),
        ]
    elif plane == "+X":
        pts = [
            np.array([cx, cy - w2, cz - h2]),
            np.array([cx, cy + w2, cz - h2]),
            np.array([cx, cy + w2, cz + h2]),
            np.array([cx, cy - w2, cz + h2]),
        ]
    elif plane == "+Z":
        pts = [
            np.array([cx - w2, cy - h2, cz]),
            np.array([cx + w2, cy - h2, cz]),
            np.array([cx + w2, cy + h2, cz]),
            np.array([cx - w2, cy + h2, cz]),
        ]
    else:
        raise ValueError(f"Unsupported plane orientation: {plane}")

    return make_3d_polygon(pts, color, opacity=opacity)


def pick_window_color(rng: np.random.Generator) -> str:
    """Randomises window lighting: mostly warm lit, minority dark, rare cool."""
    r = rng.random()
    if r < 0.17:
        return WIN_DARK
    elif r < 0.21:
        return WIN_COOL_ACC
    elif r < 0.65:
        return WIN_WARM_1
    else:
        return WIN_WARM_2


def make_window_grid(xs, ys, zs, plane, w, h, rng, offset_dist=0.08):
    """Generates a list of flat window polygons on a facade plane."""
    windows = []
    if plane == "-Y":
        y_coord = ys - offset_dist
        for x in xs:
            for z in zs:
                c = pick_window_color(rng)
                windows.append(make_window_poly(np.array([x, y_coord, z]), w, h, "-Y", c))
    elif plane == "+X":
        x_coord = xs + offset_dist
        for y in ys:
            for z in zs:
                c = pick_window_color(rng)
                windows.append(make_window_poly(np.array([x_coord, y, z]), w, h, "+X", c))
    return windows


def make_tree(x: float, y: float, scale: float = 1.0, foliage_color: str = TREE_CANOPY_1):
    """Creates a stylized low-poly architectural tree (Cylinder trunk + Sphere canopy)."""
    trunk_h = 0.46 * scale
    trunk_r = 0.05 * scale
    trunk = Cylinder(
        radius=trunk_r,
        height=trunk_h,
        resolution=(6, 6),
        fill_color=TREE_TRUNK_COL,
        fill_opacity=1.0,
        stroke_width=0,
    )
    trunk.move_to([x, y, trunk_h / 2.0])
    trunk.shade_in_3d = True

    canopy_r = 0.36 * scale
    canopy = Sphere(
        radius=canopy_r,
        resolution=(8, 8),
        fill_color=foliage_color,
        fill_opacity=1.0,
        stroke_width=0,
    )
    canopy.move_to([x, y, trunk_h + canopy_r * 0.72])
    canopy.shade_in_3d = True
    return VGroup(trunk, canopy)


# =============================================================================
# SCENE CLASS
# =============================================================================
class BuildingFlyIn(SafeThreeDScene):
    """
    Cinematic 3D architectural fly-in sequence:
    1. Establishing wide shot & smooth 3/4 orbital sweep of skyscraper.
    2. Descending approach towards brightly illuminated podium entrance.
    3. The Entry: front facade & canopy dissolve to near-transparent as camera glides in.
    4. Inside the Lobby: slow architectural drift past reception and columns to elevator wall.
    5. Final serene held beauty shot.
    """

    def construct(self):
        # 1. Dark atmospheric sky
        self.camera.background_color = BG_SKY

        # Fixed random seed for reproducible window pattern
        rng = np.random.default_rng(42)

        # Groups for rendering & animation control
        all_static_mobjects = []
        front_facade_mobjects = []
        total_window_count = 0

        # ---------------------------------------------------------------------
        # A. GROUND PLAZA & URBAN CONTEXT
        # ---------------------------------------------------------------------
        # Ground plaza slab
        plaza_slab = Prism(
            dimensions=[18.0, 14.0, 0.10],
            fill_color=GROUND_PLAZA,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, -1.0, -0.05])
        all_static_mobjects.append(plaza_slab)

        # Entrance approach stone walkway
        walkway = make_window_poly([0.0, -3.8, 0.01], 2.4, 3.8, "+Z", WALKWAY_COLOR, opacity=1.0)
        all_static_mobjects.append(walkway)

        # Subtle glowing walkway bollards
        for bx in (-1.25, 1.25):
            for by in (-2.6, -3.8, -5.0):
                bollard_glow = make_window_poly([bx, by, 0.015], 0.10, 0.10, "+Z", BOLLARD_LIGHT, opacity=0.85)
                all_static_mobjects.append(bollard_glow)

        # Road asphalt strip
        road_strip = make_window_poly([0.0, -6.8, 0.01], 18.0, 2.2, "+Z", ROAD_ASPHALT, opacity=1.0)
        all_static_mobjects.append(road_strip)

        # Road dashed center markings
        for rx in np.linspace(-7.5, 7.5, 7):
            dash = make_window_poly([rx, -6.8, 0.015], 1.2, 0.10, "+Z", ROAD_MARKING, opacity=0.6)
            all_static_mobjects.append(dash)

        # Long-exposure traffic light trails
        car_tail = make_window_poly([-1.5, -6.35, 0.02], 5.6, 0.07, "+Z", TAIL_LIGHT_RED, opacity=0.85)
        car_head = make_window_poly([ 1.5, -7.25, 0.02], 5.6, 0.07, "+Z", HEAD_LIGHT_AMB, opacity=0.75)
        all_static_mobjects.extend([car_tail, car_head])

        # Architectural landscape trees (6 trees flanking plaza)
        tree_configs = [
            (-3.6, -3.2, 1.05, TREE_CANOPY_1),
            (-4.6, -1.8, 0.90, TREE_CANOPY_2),
            (-2.7, -4.8, 0.85, TREE_CANOPY_1),
            ( 3.6, -3.2, 1.05, TREE_CANOPY_1),
            ( 4.6, -1.8, 0.90, TREE_CANOPY_2),
            ( 2.7, -4.8, 0.85, TREE_CANOPY_1),
        ]
        for tx, ty, ts, tc in tree_configs:
            all_static_mobjects.append(make_tree(tx, ty, scale=ts, foliage_color=tc))

        # ---------------------------------------------------------------------
        # B. NEIGHBOUR CONTEXT BUILDINGS (Background Massing)
        # ---------------------------------------------------------------------
        neighbor_specs = [
            # N1: Left-rear
            (-5.8, 2.8, 2.8, 3.2, 3.2, 5.6, NEIGHBOR_MASS_1, 1.2, -4.2, 3, 4, 3, 4, 0.32, 0.30),
            # N2: Left-mid
            (-6.2, -2.6, 2.1, 2.8, 2.6, 4.2, NEIGHBOR_MASS_2, -3.9, -4.8, 3, 3, 3, 3, 0.30, 0.28),
            # N3: Right-rear
            ( 5.8, 2.4, 3.2, 3.4, 3.0, 6.4, NEIGHBOR_MASS_1, 0.9, 7.5, 3, 5, 0, 0, 0.34, 0.32),
            # N4: Right-front
            ( 6.5, -3.0, 2.3, 2.6, 2.6, 4.6, NEIGHBOR_MASS_3, -4.3, 7.8, 3, 3, 0, 0, 0.30, 0.28),
        ]

        for (nb_x, nb_y, nb_z, nb_dx, nb_dy, nb_dz, nb_col,
             front_y, right_x, n_front_x, n_front_z, n_right_y, n_right_z,
             win_w, win_h) in neighbor_specs:
            nb_prism = Prism(
                dimensions=[nb_dx, nb_dy, nb_dz],
                fill_color=nb_col,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to([nb_x, nb_y, nb_z])
            all_static_mobjects.append(nb_prism)

            # Neighbor front windows
            if n_front_x > 0 and n_front_z > 0:
                xs = np.linspace(nb_x - nb_dx * 0.35, nb_x + nb_dx * 0.35, n_front_x)
                zs = np.linspace(nb_z - nb_dz * 0.35, nb_z + nb_dz * 0.35, n_front_z)
                n_wins = make_window_grid(xs, front_y, zs, "-Y", win_w, win_h, rng)
                all_static_mobjects.extend(n_wins)
                total_window_count += len(n_wins)

            # Neighbor right windows
            if n_right_y > 0 and n_right_z > 0:
                ys = np.linspace(nb_y - nb_dy * 0.35, nb_y + nb_dy * 0.35, n_right_y)
                zs = np.linspace(nb_z - nb_dz * 0.35, nb_z + nb_dz * 0.35, n_right_z)
                n_wins = make_window_grid(right_x, ys, zs, "+X", win_w, win_h, rng)
                all_static_mobjects.extend(n_wins)
                total_window_count += len(n_wins)

        # ---------------------------------------------------------------------
        # C. HERO TOWER: UPPER TIERS & ROOFTOP CROWN
        # ---------------------------------------------------------------------
        # Tier 1 (Lower Tower): Z from 1.9 to 4.7
        t1_mass = Prism(
            dimensions=[3.6, 2.8, 2.8],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.1, 3.3])
        t1_trim = Prism(
            dimensions=[3.66, 2.86, 0.08],
            fill_color=HERO_ACCENT,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.1, 4.70])
        all_static_mobjects.extend([t1_mass, t1_trim])

        # Tier 1 Windows: Front (-Y at Y = -1.30) & Right (+X at X = 1.80)
        t1_xs = np.linspace(-1.35, 1.35, 6)
        t1_zs = np.linspace(2.25, 4.35, 5)
        t1_front_wins = make_window_grid(t1_xs, -1.30, t1_zs, "-Y", 0.32, 0.28, rng)
        all_static_mobjects.extend(t1_front_wins)
        total_window_count += len(t1_front_wins)

        t1_ys = np.linspace(-0.90, 1.10, 5)
        t1_right_wins = make_window_grid(1.80, t1_ys, t1_zs, "+X", 0.28, 0.28, rng)
        all_static_mobjects.extend(t1_right_wins)
        total_window_count += len(t1_right_wins)

        # Tier 2 (Mid Tower, setback): Z from 4.7 to 7.2
        t2_mass = Prism(
            dimensions=[2.8, 2.3, 2.5],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.15, 5.95])
        t2_trim = Prism(
            dimensions=[2.86, 2.36, 0.08],
            fill_color=HERO_ACCENT,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.15, 7.20])
        all_static_mobjects.extend([t2_mass, t2_trim])

        # Tier 2 Windows: Front (-Y at Y = -1.00) & Right (+X at X = 1.40)
        t2_xs = np.linspace(-0.95, 0.95, 5)
        t2_zs = np.linspace(5.05, 6.85, 5)
        t2_front_wins = make_window_grid(t2_xs, -1.00, t2_zs, "-Y", 0.26, 0.24, rng)
        all_static_mobjects.extend(t2_front_wins)
        total_window_count += len(t2_front_wins)

        t2_ys = np.linspace(-0.65, 0.95, 4)
        t2_right_wins = make_window_grid(1.40, t2_ys, t2_zs, "+X", 0.24, 0.24, rng)
        all_static_mobjects.extend(t2_right_wins)
        total_window_count += len(t2_right_wins)

        # Tier 3 (Upper Tower / Crown setback): Z from 7.2 to 9.2
        t3_mass = Prism(
            dimensions=[2.1, 1.8, 2.0],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.20, 8.20])
        t3_trim = Prism(
            dimensions=[2.16, 1.86, 0.08],
            fill_color=HERO_ACCENT,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.20, 9.20])
        all_static_mobjects.extend([t3_mass, t3_trim])

        # Tier 3 Windows: Front (-Y at Y = -0.70) & Right (+X at X = 1.05)
        t3_xs = np.linspace(-0.65, 0.65, 4)
        t3_zs = np.linspace(7.55, 8.85, 4)
        t3_front_wins = make_window_grid(t3_xs, -0.70, t3_zs, "-Y", 0.22, 0.22, rng)
        all_static_mobjects.extend(t3_front_wins)
        total_window_count += len(t3_front_wins)

        t3_ys = np.linspace(-0.35, 0.75, 3)
        t3_right_wins = make_window_grid(1.05, t3_ys, t3_zs, "+X", 0.22, 0.22, rng)
        all_static_mobjects.extend(t3_right_wins)
        total_window_count += len(t3_right_wins)

        # Rooftop Mechanical Penthouse & Beacon Spire
        penthouse = Prism(
            dimensions=[1.3, 1.1, 0.45],
            fill_color=HERO_CROWN,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.20, 9.465])

        spire = Cylinder(
            radius=0.03,
            height=0.90,
            resolution=(6, 6),
            fill_color="#90A4AE",
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.20, 10.15])
        spire.shade_in_3d = True

        beacon = Sphere(
            radius=0.06,
            resolution=(6, 6),
            fill_color="#FF1744",
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.20, 10.63])
        beacon.shade_in_3d = True
        all_static_mobjects.extend([penthouse, spire, beacon])

        # ---------------------------------------------------------------------
        # D. PODIUM STRUCTURE (Ground Level & Envelope)
        # ---------------------------------------------------------------------
        # Podium envelope dimensions: dx = 4.8, dy = 3.8, dz = 1.8 (Z from 0 to 1.8)
        # Left wall (X = -2.34) & Right wall (X = +2.34)
        podium_left_wall = Prism(
            dimensions=[0.12, 3.8, 1.8],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([-2.34, 0.0, 0.9])

        podium_right_wall = Prism(
            dimensions=[0.12, 3.8, 1.8],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([ 2.34, 0.0, 0.9])

        # Podium back wall (Y = +1.84)
        podium_back_wall = Prism(
            dimensions=[4.8, 0.12, 1.8],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 1.84, 0.9])

        # Podium ceiling slab / roof deck (Z = 1.80 to 1.90)
        podium_roof_slab = Prism(
            dimensions=[4.9, 3.9, 0.10],
            fill_color=HERO_ACCENT,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.0, 1.85])

        all_static_mobjects.extend([podium_left_wall, podium_right_wall, podium_back_wall, podium_roof_slab])

        # Podium right wall windows (visible during orbital establishing shot)
        pod_ys = np.linspace(-1.20, 1.20, 4)
        pod_zs = np.array([0.65, 1.25])
        pod_right_wins = make_window_grid(2.40, pod_ys, pod_zs, "+X", 0.32, 0.32, rng)
        all_static_mobjects.extend(pod_right_wins)
        total_window_count += len(pod_right_wins)

        # ---------------------------------------------------------------------
        # E. PODIUM FRONT FACADE & CANOPY (DISSOLVES ON ENTRY)
        # ---------------------------------------------------------------------
        # Entrance opening in center: width 1.6 (X in [-0.8, 0.8]), clear height 1.42
        # Left front wall: X in [-2.4, -0.8]
        front_wall_l = Prism(
            dimensions=[1.6, 0.12, 1.8],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([-1.60, -1.84, 0.90])

        # Right front wall: X in [0.8, 2.4]
        front_wall_r = Prism(
            dimensions=[1.6, 0.12, 1.8],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([ 1.60, -1.84, 0.90])

        # Entrance top lintel: X in [-0.8, 0.8], Z in [1.42, 1.80]
        front_lintel = Prism(
            dimensions=[1.6, 0.12, 0.38],
            fill_color=HERO_FACADE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, -1.84, 1.61])

        # Cantilevered entrance canopy slab over opening
        canopy_slab = Prism(
            dimensions=[2.2, 0.80, 0.05],
            fill_color=PODIUM_CANOPY,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, -2.20, 1.42])

        # Canopy underside warm illumination light strip
        canopy_glow = make_window_poly([0.0, -2.20, 1.39], 2.10, 0.70, "+Z", CANOPY_LIGHT, opacity=0.92)

        # Glass doors in opening (semi-transparent)
        glass_l = make_window_poly([-0.38, -1.84, 0.70], 0.75, 1.38, "-Y", GLASS_DOORS, opacity=0.25)
        glass_r = make_window_poly([ 0.38, -1.84, 0.70], 0.75, 1.38, "-Y", GLASS_DOORS, opacity=0.25)

        # Front wall windows on left and right piers
        front_pod_wins = []
        for fwx in (-1.85, -1.35, 1.35, 1.85):
            for fwz in (0.65, 1.15):
                c = pick_window_color(rng)
                front_pod_wins.append(make_window_poly(np.array([fwx, -1.905, fwz]), 0.32, 0.30, "-Y", c))
        total_window_count += len(front_pod_wins)

        # Collect all front elements into the dissolve group
        front_facade_mobjects = [
            front_wall_l, front_wall_r, front_lintel,
            canopy_slab, canopy_glow, glass_l, glass_r,
            *front_pod_wins
        ]

        # ---------------------------------------------------------------------
        # F. LOBBY INTERIOR (Warm, Glowing, Detailed Architectural Space)
        # ---------------------------------------------------------------------
        # 1. Lobby Floor Slab & Ceiling Underside
        lobby_floor = make_window_poly([0.0, 0.0, 0.02], 4.6, 3.6, "+Z", LOBBY_FLOOR, opacity=1.0)
        lobby_ceiling = make_window_poly([0.0, 0.0, 1.785], 4.6, 3.6, "+Z", LOBBY_CEILING, opacity=1.0)
        all_static_mobjects.extend([lobby_floor, lobby_ceiling])

        # 2. Warm Floor Light Reflection Pools (sells the inviting interior glow)
        pool_entrance = make_window_poly([0.0, -0.90, 0.025], 2.0, 1.10, "+Z", LOBBY_POOL_1, opacity=0.48)
        pool_reception = make_window_poly([0.0, -0.15, 0.026], 1.8, 0.85, "+Z", LOBBY_POOL_2, opacity=0.55)
        pool_elevators = make_window_poly([0.0,  1.15, 0.027], 2.4, 0.75, "+Z", LOBBY_POOL_1, opacity=0.50)
        pool_lounge = make_window_poly([-1.40,  0.25, 0.028], 1.0, 1.10, "+Z", LOBBY_POOL_2, opacity=0.42)
        all_static_mobjects.extend([pool_entrance, pool_reception, pool_elevators, pool_lounge])

        # 3. Ceiling Light Fixtures (bright glowing panels)
        ceil_troffer_c = make_window_poly([ 0.0, 0.0, 1.780], 0.45, 2.60, "+Z", CEILING_LIGHT_HI, opacity=0.98)
        ceil_troffer_l = make_window_poly([-1.1, 0.0, 1.780], 0.35, 2.60, "+Z", CEILING_LIGHT, opacity=0.95)
        ceil_troffer_r = make_window_poly([ 1.1, 0.0, 1.780], 0.35, 2.60, "+Z", CEILING_LIGHT, opacity=0.95)
        ceil_cross_f = make_window_poly([0.0, -1.0, 1.778], 2.60, 0.30, "+Z", CEILING_LIGHT, opacity=0.90)
        ceil_cross_b = make_window_poly([0.0,  1.0, 1.778], 2.60, 0.30, "+Z", CEILING_LIGHT, opacity=0.90)
        all_static_mobjects.extend([ceil_troffer_c, ceil_troffer_l, ceil_troffer_r, ceil_cross_f, ceil_cross_b])

        # 4. Lobby Columns (4 cylindrical pillars with brass trim rings, resolution 8x8)
        col_coords = [
            (-1.25, -0.65),
            ( 1.25, -0.65),
            (-1.25,  0.65),
            ( 1.25,  0.65),
        ]
        for col_x, col_y in col_coords:
            col_shaft = Cylinder(
                radius=0.10,
                height=1.74,
                resolution=(8, 8),
                fill_color=COLUMN_BODY,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to([col_x, col_y, 0.88])
            col_shaft.shade_in_3d = True

            col_base = Prism(
                dimensions=[0.24, 0.24, 0.05],
                fill_color=COLUMN_TRIM,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to([col_x, col_y, 0.035])

            col_cap = Prism(
                dimensions=[0.24, 0.24, 0.05],
                fill_color=COLUMN_TRIM,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to([col_x, col_y, 1.725])
            all_static_mobjects.extend([col_shaft, col_base, col_cap])

        # 5. Reception Desk & Backlit Onyx Glow Feature
        desk_body = Prism(
            dimensions=[1.50, 0.50, 0.42],
            fill_color=RECEPTION_BODY,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.25, 0.22])

        desk_glow_panel = make_window_poly([0.0, -0.005, 0.21], 1.40, 0.34, "-Y", RECEPTION_GLOW, opacity=0.95)

        desk_top = Prism(
            dimensions=[1.54, 0.54, 0.04],
            fill_color=DESK_COUNTER,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 0.25, 0.44])

        terminal_housing = Prism(
            dimensions=[0.24, 0.04, 0.16],
            fill_color="#37474F",
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.25, 0.28, 0.54])

        terminal_glow = make_window_poly([0.25, 0.255, 0.54], 0.20, 0.13, "-Y", TERMINAL_SCREEN, opacity=0.90)
        all_static_mobjects.extend([desk_body, desk_glow_panel, desk_top, terminal_housing, terminal_glow])

        # 6. Lounge Seating Blocks (Left) & Planter (Right)
        lounge_sofa = Prism(
            dimensions=[0.70, 1.10, 0.25],
            fill_color=LOUNGE_LEATHER,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([-1.50, 0.25, 0.135])

        lounge_table = Prism(
            dimensions=[0.40, 0.60, 0.16],
            fill_color=LOUNGE_BRASS,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([-1.50, 0.25, 0.09])

        plant_pot = Cylinder(
            radius=0.12,
            height=0.28,
            resolution=(6, 6),
            fill_color="#3E2723",
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([1.50, 0.25, 0.14])
        plant_pot.shade_in_3d = True

        plant_shrub = Sphere(
            radius=0.22,
            resolution=(8, 8),
            fill_color=PLANT_LEAVES,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([1.50, 0.25, 0.40])
        plant_shrub.shade_in_3d = True
        all_static_mobjects.extend([lounge_sofa, lounge_table, plant_pot, plant_shrub])

        # 7. Elevator Feature Wall (Back Wall Accent)
        elevator_backdrop = Prism(
            dimensions=[3.60, 0.06, 1.55],
            fill_color=ELEVATOR_PANEL,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, 1.72, 0.85])
        all_static_mobjects.append(elevator_backdrop)

        # Gold decorative vertical dividers between elevator bays
        div_l = make_window_poly([-0.42, 1.685, 0.75], 0.04, 1.35, "-Y", "#B7950B", opacity=0.85)
        div_r = make_window_poly([ 0.42, 1.685, 0.75], 0.04, 1.35, "-Y", "#B7950B", opacity=0.85)
        all_static_mobjects.extend([div_l, div_r])

        # 3 Elevator Doors in Metallic Satin Gold
        elevator_xs = (-0.85, 0.0, 0.85)
        for ed_x in elevator_xs:
            door_prism = Prism(
                dimensions=[0.52, 0.04, 1.15],
                fill_color=ELEVATOR_BRASS,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to([ed_x, 1.68, 0.65])

            door_slit = make_window_poly([ed_x, 1.655, 0.65], 0.016, 1.14, "-Y", ELEVATOR_SEAM, opacity=0.95)
            floor_display = make_window_poly([ed_x, 1.670, 1.30], 0.18, 0.06, "-Y", ELEVATOR_INDIC, opacity=0.96)
            all_static_mobjects.extend([door_prism, door_slit, floor_display])

        # Assemble the front facade group for entry dissolve animation
        front_facade_group = VGroup(*front_facade_mobjects)

        # ---------------------------------------------------------------------
        # G. SCENE POPULATION (Add all static geometry ONCE)
        # ---------------------------------------------------------------------
        self.add(*all_static_mobjects)
        self.add(front_facade_group)

        print(f"[SCENE STATS] Total windows: {total_window_count} (Budget: 350)")

        # =====================================================================
        # CAMERA CHOREOGRAPHY (Total Duration: 26.5s)
        # =====================================================================
        # Initial Camera: High 3/4 establishing wide perspective
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-44 * DEGREES,
            zoom=0.85,
            frame_center=[0.0, -0.20, 3.80],
        )

        # ---------------------------------------------------------------------
        # SHOT 1: Establishing Wide Orbit (~0.0s – 7.0s | run_time = 7.0s)
        # Slowly orbit around the hero skyscraper to read its 3D setbacks & mass
        # ---------------------------------------------------------------------
        self.move_camera(
            phi=65 * DEGREES,
            theta=-70 * DEGREES,
            zoom=0.98,
            frame_center=[0.0, -0.60, 3.00],
            run_time=7.0,
            rate_func=smooth,
        )

        # ---------------------------------------------------------------------
        # SHOT 2: Descend & Approach (~7.0s – 13.0s | run_time = 6.0s)
        # Swoop down towards eye level, pushing into the illuminated entrance
        # ---------------------------------------------------------------------
        self.move_camera(
            phi=78 * DEGREES,
            theta=-85 * DEGREES,
            zoom=1.85,
            frame_center=[0.0, -1.85, 1.15],
            run_time=6.0,
            rate_func=smooth,
        )

        # ---------------------------------------------------------------------
        # SHOT 3: The Entry (~13.0s – 17.5s | run_time = 4.5s)
        # Fade front facade pieces to near-transparent (0.06) as camera passes through
        # ---------------------------------------------------------------------
        self.move_camera(
            phi=84 * DEGREES,
            theta=-90 * DEGREES,
            zoom=2.60,
            frame_center=[0.0, -0.20, 0.82],
            run_time=4.5,
            rate_func=smooth,
            added_anims=[front_facade_group.animate.set_opacity(0.06)],
        )

        # ---------------------------------------------------------------------
        # SHOT 4: Lobby Reveal & Drift (~17.5s – 25.0s | run_time = 7.5s)
        # Glide past reception desk, panning across columns toward elevator wall
        # ---------------------------------------------------------------------
        self.move_camera(
            phi=83 * DEGREES,
            theta=-84 * DEGREES,
            zoom=2.90,
            frame_center=[0.15, 0.65, 0.76],
            run_time=7.5,
            rate_func=smooth,
        )

        # ---------------------------------------------------------------------
        # SHOT 5: Held Interior Beauty Shot (~25.0s – 26.5s | wait = 1.5s)
        # Calm resting frame inside the luminous lobby
        # ---------------------------------------------------------------------
        self.wait(1.5)
