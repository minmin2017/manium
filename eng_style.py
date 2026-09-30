"""Engineering-style (blueprint) helpers for Manim.

Blue canvas + white grid + warm (orange/yellow) objects with bold white strokes.
Import:  sys.path.insert(0, r"C:\\Users\\wicha\\.claude\\skills\\engineering-style"); from eng_style import *
"""
import numpy as np
from manim import (VMobject, VGroup, Line, Circle, Rectangle, Text, DashedVMobject,
                   config, UP, DOWN, LEFT, RIGHT, ORIGIN)

# ---- palette -------------------------------------------------------------
BG        = "#1456A8"   # blueprint blue canvas
BG_DEEP   = "#0C3F82"   # vignette / panels
GRID      = "#FFFFFF"   # white grid lines (opacity does the work)
STROKE    = "#FFFFFF"   # bold outline on every physical object
TEXT      = "#FFFFFF"
YELLOW    = "#FFD23F"   # input / active part
ORANGE    = "#FF9F1C"   # main subject
AMBER     = "#F26B1D"   # output / secondary part
HOT       = "#FF6B2C"   # highlight, contact, result
PALETTE_WARM = [YELLOW, ORANGE, AMBER, HOT]

STROKE_W = 5            # bold white outline (Manim 480p-1080p all read fine)
GRID_MINOR_OP, GRID_MAJOR_OP = 0.16, 0.34


def set_blueprint_background(scene):
    scene.camera.background_color = BG


def blueprint_grid(step=0.5, major_every=5, extent=None):
    """White grid; minor every `step` units, major every `major_every` steps.
    Opacity < 0.5 so mlib.LayoutGuard ignores it. Keep at z_index -10."""
    w = extent[0] if extent else config.frame_width
    h = extent[1] if extent else config.frame_height
    minor, major = VGroup(), VGroup()
    n_x, n_y = int(w / 2 / step) + 1, int(h / 2 / step) + 1
    for i in range(-n_x, n_x + 1):
        (major if i % major_every == 0 else minor).add(
            Line([i * step, -h / 2, 0], [i * step, h / 2, 0]))
    for j in range(-n_y, n_y + 1):
        (major if j % major_every == 0 else minor).add(
            Line([-w / 2, j * step, 0], [w / 2, j * step, 0]))
    minor.set_stroke(GRID, width=1.0, opacity=GRID_MINOR_OP)
    major.set_stroke(GRID, width=1.8, opacity=GRID_MAJOR_OP)
    g = VGroup(minor, major)
    g.set_z_index(-10)
    return g


def blueprint(scene, step=0.5):
    """One call: set background + add grid. Returns the grid."""
    set_blueprint_background(scene)
    g = blueprint_grid(step)
    scene.add(g)
    return g


def eng_style(mob, fill=ORANGE, stroke_w=STROKE_W, fill_opacity=1.0):
    """Apply the house look: warm fill + bold white stroke."""
    mob.set_fill(fill, opacity=fill_opacity)
    mob.set_stroke(STROKE, width=stroke_w)
    return mob


def label(txt, size=28, color=TEXT, **kw):
    return Text(txt, font_size=size, color=color, **kw)


# ---- 2D gear -------------------------------------------------------------
def _ring_points(r, n=48, clockwise=False):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    if clockwise:
        a = a[::-1]
    return [np.array([r * np.cos(t), r * np.sin(t), 0]) for t in a]


def gear_2d(teeth=20, module=0.2, fill=ORANGE, stroke_w=STROKE_W,
            bore=0.28, lightening_holes=0, keyway=False, hub_ring=True):
    """Filled 2D spur gear centred on ORIGIN with a white outline.

    pitch radius r = module*teeth/2, tip = r+module, root = r-1.25*module.
    Holes (bore, lightening holes) are real cut-outs so the grid shows through.
    Returns a VGroup: [body, hub_ring?, tooth_marker]. body.gear_r = pitch radius.
    """
    N = teeth
    r = module * N / 2
    ra, rf = r + module, r - 1.25 * module
    p = 2 * np.pi / N
    pts = []
    for k in range(N):
        c = k * p
        # root-left, tip-left, tip-right, root-right  (half-angles in units of pitch)
        for rad, ang in ((rf, c - 0.31 * p), (ra, c - 0.13 * p),
                         (ra, c + 0.13 * p), (rf, c + 0.31 * p)):
            pts.append(np.array([rad * np.cos(ang), rad * np.sin(ang), 0]))
        # root arc to next tooth (straight is fine at this tooth count; add midpoint)
        a_mid = c + 0.5 * p
        pts.append(np.array([rf * np.cos(a_mid), rf * np.sin(a_mid), 0]))

    body = VMobject()
    body.set_points_as_corners(pts + [pts[0]])
    # cut-outs: opposite winding so cairo's non-zero fill leaves a hole
    holes = [_ring_points(bore, 32, clockwise=True)]
    if lightening_holes:
        hr = (rf - bore) * 0.30
        hc = (rf + bore) / 2
        for i in range(lightening_holes):
            a = i * 2 * np.pi / lightening_holes
            centre = np.array([hc * np.cos(a), hc * np.sin(a), 0])
            holes.append([centre + q for q in _ring_points(hr, 28, clockwise=True)])
    if keyway:
        kw_, kh = bore * 0.28, bore * 0.55
        holes[0] = [np.array([-kw_, bore * 0.98, 0]), np.array([-kw_, bore + kh, 0]),
                    np.array([kw_, bore + kh, 0]), np.array([kw_, bore * 0.98, 0])] + holes[0]
    for h in holes:
        body.start_new_path(h[0])
        body.add_points_as_corners(h[1:] + [h[0]])

    body.set_fill(fill, opacity=1)
    body.set_stroke(STROKE, width=stroke_w, opacity=1)
    parts = [body]
    if hub_ring:
        ring = Circle(radius=(rf + bore) / 2 + 0.0, stroke_width=1.6, color=STROKE)
        ring.set_stroke(STROKE, width=1.6, opacity=0.55)
        ring.set_fill(opacity=0)
        parts.append(ring)
    # single dark spoke marking one tooth so rotation is visible
    marker = Line(ORIGIN + np.array([bore * 1.4, 0, 0]),
                  np.array([rf * 0.9, 0, 0]), stroke_width=stroke_w)
    marker.set_stroke(STROKE, width=stroke_w * 0.8, opacity=0.9)
    parts.append(marker)
    g = VGroup(*parts)
    g.gear_r, g.gear_teeth, g.gear_tip, g.gear_root = r, N, ra, rf
    return g


def pitch_circle(gear, dashed=True):
    c = Circle(radius=gear.gear_r, stroke_width=1.8)
    c.set_stroke(STROKE, width=1.8, opacity=0.75)
    c.move_to(gear.get_center())
    return DashedVMobject(c, num_dashes=60, dashed_ratio=0.5) if dashed else c


def mesh_angle(theta1, n1, n2):
    """Angle of gear 2 (right of gear 1 on the x-axis) that meshes with gear 1 at theta1."""
    return np.pi + np.pi / n2 - theta1 * n1 / n2
