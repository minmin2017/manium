# -*- coding: utf-8 -*-
"""hook_common.py -- shared helpers for the two 3DP hook teaching clips (Q1 flat / Q2 upright).

Everything a clip needs that is NOT scene-specific lives here, so Q2 can import it unchanged:

  * Spec            every number on screen, derived from Common Spec 3.2 and asserted equal to the table
  * hook geometry   J-profile outline in mm (tangent points computed algebraically, SKILL 24),
                    inward offsets (wall loops), 45-degree hatch, filled profile mobject
  * make_hook_sheets(n_show=8, mode="flat"|"upright")   8 representative sheets standing for 40 layers
  * Deck / card_deck   row of thin tall cards (the "deck of cards" picture)
  * stress_diagram  uniform + triangular stress across the 8x8 section (trapezoid), Q2 uses it
  * BarPair         two live bars driven by callables (one ValueTracker drives numbers AND heights)
  * table_mob       row-by-row table
  * glow            equation term + figure part flash in ONE self.play (SKILL 51/52)
  * Beats           mixin: plan-time contract -- self.mark(t, label), self.until(t)  (prints [BEAT] lines)
  * cam_point / label helpers for fixed-in-frame text in a 3D scene

All Thai text comes from hook_captions.py (cap / CAPS / TABLE_*). Nothing Thai is typed in this file.
Colour convention (Common Spec 5) is fixed across all 8 episodes -- see the C_* aliases below.
"""
from mlib import *          # colours, SafeScene, SafeThreeDScene, title, page_ref, caption_top, fit_width, arrow3, line3
import numpy as np

from hook_captions import CAPS, cap, TABLE_Q1C, TABLE_Q2D

# ----------------------------------------------------------------------------- colours (Common Spec 5)
C_HOOK = GEAR_OUT        # plastic part
C_HOOK_EDGE = "#B26A00"  # darker outline of the plastic part (same hue family)
C_F = FORCE              # force F, weight
C_D = CURRENT            # distance d (moment arm)
C_M = TORQUE             # moment M
C_SIG_T = WARN           # tensile stress / inner fibre
C_SIG_C = FIELD          # compressive stress / outer fibre
C_AVG = OK               # average sigma = F/A, and "result / conclusion"
C_TAU = RING_G           # shear tau
C_BOND = CURRENT         # bond / interface between layers (thin line + dots)
C_REF = METAL            # reference lines, frames, rod
C_TXT2 = GRAYTXT         # secondary text

# ----------------------------------------------------------------------------- numbers (Common Spec 3.2)
F_N = 100.0              # N  (assumed example, about 10 kgf)
SEC_B = SEC_H = 8.0      # mm  section 8 x 8
A_MM2 = SEC_B * SEC_H    # 64 mm^2
I_MM4 = SEC_B * SEC_H ** 3 / 12.0     # 341.33 mm^4
C_MM = SEC_H / 2.0       # 4 mm
N_LAYERS = 40            # real layers (0.2 mm each) in the 8 mm thickness
N_SHOW = 8               # representative sheets drawn
D_CASE_A, D_CASE_B = 19.0, 5.0        # mm, cord position from the stem axis


def sigma_axial(F=F_N):
    return F / A_MM2


def sigma_bend(d, F=F_N):
    return F * d * C_MM / I_MM4


def sigma_inner(d, F=F_N):
    return sigma_axial(F) + sigma_bend(d, F)


def sigma_outer(d, F=F_N):
    return sigma_axial(F) - sigma_bend(d, F)


def tau_max(F=F_N):
    return 1.5 * F / A_MM2


# expected values straight from the Common Spec 3.2 table; the module refuses to import if the formulas drift
_SPEC = {"A": 64.0, "sigma_axial": 1.56, "I": 341.3, "bend19": 22.27, "bend5": 5.86,
         "inner19": 23.83, "inner5": 7.42, "tau": 2.34, "ratio19": 10.2, "ratio5": 3.2}
assert A_MM2 == _SPEC["A"]
assert round(sigma_axial(), 2) == _SPEC["sigma_axial"]
assert round(I_MM4, 1) == _SPEC["I"]
assert round(sigma_bend(19), 2) == _SPEC["bend19"] and round(sigma_bend(5), 2) == _SPEC["bend5"]
assert round(sigma_inner(19), 2) == _SPEC["inner19"] and round(sigma_inner(5), 2) == _SPEC["inner5"]
assert round(tau_max(), 2) == _SPEC["tau"]
assert round(sigma_inner(19) / tau_max(), 1) == _SPEC["ratio19"]
assert round(sigma_inner(5) / tau_max(), 1) == _SPEC["ratio5"]

# ----------------------------------------------------------------------------- hook geometry (mm)
EYE_C = np.array([0.0, 76.5])
EYE_RO, EYE_RI = 13.5, 5.5
STEM_HW, STEM_TOP = 4.0, 40.0
BASE_T = 8.0
BASE_X0, BASE_X1 = -4.0, 42.0
TIP_X0, TIP_X1, TIP_TOP = 34.0, 42.0, 38.0
R_OUT_CORNER, R_TIP, R_INNER = 6.0, 2.0, 2.0
HOOK_H = EYE_C[1] + EYE_RO                      # 90 mm
HOOK_CX = (BASE_X0 + BASE_X1) / 2.0             # 19 mm  centre of the bounding box
HOOK_CY = HOOK_H / 2.0                          # 45 mm
INNER_CORNER = np.array([STEM_HW, BASE_T])      # (4, 8) -- the critical point of both clips


def tangent_point(P, C=EYE_C, R=EYE_RO, side=+1):
    """Tangent point on circle (C,R) of the line through the external point P (algebraic, SKILL 24).
    side=+1 -> tangent on the +x side when P is on the +x side of the axis, side=-1 for the mirror one."""
    P = np.asarray(P, float)
    v = P - C
    d = float(np.hypot(v[0], v[1]))
    base = float(np.arctan2(v[1], v[0]))
    a = float(np.arccos(R / d))
    ang = base + side * a
    return C + R * np.array([np.cos(ang), np.sin(ang)]), ang


def _arc(c, r, a0, a1, step_deg=6.0):
    n = max(3, int(np.ceil(abs(a1 - a0) / np.radians(step_deg))) + 1)
    t = np.linspace(a0, a1, n)
    return np.stack([c[0] + r * np.cos(t), c[1] + r * np.sin(t)], axis=1)


def _join(parts):
    out = [np.asarray(parts[0], float)]
    for p in parts[1:]:
        p = np.asarray(p, float)
        if np.allclose(out[-1][-1], p[0], atol=1e-9):
            p = p[1:]
        out.append(p)
    return np.concatenate(out, axis=0)


def hook_outline_mm(step_deg=6.0):
    """Outer boundary (CCW, material on the left) and eye hole (CW) of the J profile, in mm."""
    t_r, a_r = tangent_point((STEM_HW, STEM_TOP), side=+1)
    t_l, a_l = tangent_point((-STEM_HW, STEM_TOP), side=-1)
    a_l = a_l + 2 * np.pi if a_l < a_r else a_l          # left tangent angle ~195 deg, so the arc runs CCW over the top
    outer = _join([
        [(BASE_X0 + R_OUT_CORNER, 0.0), (BASE_X1, 0.0), (BASE_X1, TIP_TOP - R_TIP)],
        _arc((BASE_X1 - R_TIP, TIP_TOP - R_TIP), R_TIP, 0.0, np.pi / 2, step_deg),
        _arc((TIP_X0 + R_TIP, TIP_TOP - R_TIP), R_TIP, np.pi / 2, np.pi, step_deg),
        [(TIP_X0, TIP_TOP - R_TIP), (TIP_X0, BASE_T), (STEM_HW + R_INNER, BASE_T)],
        _arc((STEM_HW + R_INNER, BASE_T + R_INNER), R_INNER, -np.pi / 2, -np.pi, step_deg),      # inner fillet r=2 at (4, 8)
        [(STEM_HW, BASE_T + R_INNER), (STEM_HW, STEM_TOP), tuple(t_r)],
        _arc(EYE_C, EYE_RO, a_r, a_l, step_deg),
        [tuple(t_l), (-STEM_HW, STEM_TOP), (BASE_X0, R_OUT_CORNER)],
        _arc((BASE_X0 + R_OUT_CORNER, R_OUT_CORNER), R_OUT_CORNER, np.pi, 1.5 * np.pi, step_deg),
    ])
    hole = _arc(EYE_C, EYE_RI, 0.0, -2 * np.pi, 7.5)[:-1]
    return outer, hole


def offset_loop(pts, d):
    """Offset a closed loop by d to its LEFT (material side for outer CCW / hole CW loops), miter joins."""
    p = np.asarray(pts, float)
    keep = np.ones(len(p), bool)
    keep[1:] = np.linalg.norm(np.diff(p, axis=0), axis=1) > 1e-9
    p = p[keep]
    e = np.roll(p, -1, axis=0) - p
    nrm = np.stack([-e[:, 1], e[:, 0]], axis=1)
    nrm /= np.linalg.norm(nrm, axis=1)[:, None]
    n_prev = np.roll(nrm, 1, axis=0)
    k = 1.0 + np.sum(n_prev * nrm, axis=1)
    return p + d * (n_prev + nrm) / k[:, None]


def hatch_segments(loops, angle_deg=45.0, spacing=1.0):
    """Hatch lines inside an even-odd region bounded by `loops` (list of Nx2 arrays). Returns [(p0, p1), ...]."""
    a = np.radians(angle_deg)
    u = np.array([np.cos(a), np.sin(a)])
    nv = np.array([-np.sin(a), np.cos(a)])
    allp = np.concatenate(loops, axis=0)
    cs = allp @ nv
    segs = []
    for c in np.arange(np.floor(cs.min() / spacing) * spacing + 1e-3, cs.max(), spacing):
        ss = []
        for lp in loops:
            q = np.roll(lp, -1, axis=0)
            sa, sb = lp @ nv - c, q @ nv - c
            hit = (sa * sb) < 0
            for i in np.nonzero(hit)[0]:
                t = sa[i] / (sa[i] - sb[i])
                pt = lp[i] + t * (q[i] - lp[i])
                ss.append(float(pt @ u))
        ss.sort()
        for j in range(0, len(ss) - 1, 2):
            p0 = c * nv + ss[j] * u
            p1 = c * nv + ss[j + 1] * u
            segs.append((p0, p1))
    return segs


def _pts3(p2, mm, origin, z=0.0, plane="xy"):
    p2 = np.asarray(p2, float)
    x, y = p2[..., 0] * mm, p2[..., 1] * mm
    o = np.asarray(origin, float)
    zz = np.full_like(x, z)
    if plane == "xy":
        return np.stack([x + o[0], y + o[1], zz + o[2]], axis=-1)
    return np.stack([x + o[0], zz + o[1], y + o[2]], axis=-1)       # "xz": profile y becomes world up (hanging pose)


def loop_mob(pts2, mm, origin=(0, 0, 0), z=0.0, plane="xy", closed=True, **style):
    m = VMobject(**style)
    q = _pts3(pts2, mm, origin, z, plane)
    if closed:
        q = np.concatenate([q, q[:1]], axis=0)
    m.set_points_as_corners(q)
    return m


def hook_profile(mm=0.05, origin=(0, 0, 0), z=0.0, plane="xy", color=C_HOOK, opacity=0.85,
                 stroke_color=C_HOOK_EDGE, stroke_width=2.0):
    """Filled J profile (outer boundary + eye hole as a second sub-path wound the other way)."""
    outer, hole = hook_outline_mm()
    m = loop_mob(outer, mm, origin, z, plane)
    h = loop_mob(hole, mm, origin, z, plane)
    m.append_points(h.points)
    m.set_fill(color, opacity=opacity)
    m.set_stroke(stroke_color, width=stroke_width)
    return m


def hook_centre_origin(mm, shift=(0, 0, 0)):
    """Origin that puts the bounding-box centre of the J at `shift` (so a model sits where we want on screen)."""
    return np.array([-HOOK_CX * mm, -HOOK_CY * mm, 0.0]) + np.asarray(shift, float)


# ----------------------------------------------------------------------------- representative sheets
def make_hook_sheets(n_show=N_SHOW, mode="flat", mm=0.05, z_exag=3.0, origin=None,
                     opacities=(0.85, 0.75), color=C_HOOK, stroke_width=1.6):
    """8 representative sheets standing for the 40 real layers (never draw all 40).

    mode="flat"    : J-profile plates in the XY plane, stacked along Z (the flat-print picture). The 8 mm real
                     thickness is drawn z_exag times thicker so the stack is legible at 480p (documented in the
                     scene; set z_exag=1.0 for true proportions). Centred on `origin` (default world origin) in Z.
    mode="upright" : the same J cut by horizontal planes: n_show bands stacked along the stem (profile plane XY,
                     z = 0); the base is the bottom band. Used by clip Q2.
    The group is ordered back-to-front for a camera that looks from +z (flat) so painter's order is right.
    """
    sheets = VGroup()
    if origin is None:
        origin = hook_centre_origin(mm)
    origin = np.asarray(origin, float)
    if mode == "flat":
        T = SEC_B * z_exag
        pitch = T / n_show
        for k in range(n_show):
            zk = (k + 0.5) * pitch - T / 2.0
            op = opacities[k % 2]
            s = hook_profile(mm, origin, z=zk * mm, color=color, opacity=op,
                             stroke_width=stroke_width)
            sheets.add(s)
        sheets.z_levels = [((k + 0.5) * pitch - T / 2.0) for k in range(n_show)]
        sheets.thickness_mm = T
        sheets.pitch_mm = pitch
    elif mode == "upright":
        full = hook_profile(mm, origin, color=color, opacity=1.0)
        band = HOOK_H / n_show
        gap = 0.08 * band
        for k in range(n_show):
            y0, y1 = k * band + gap / 2, (k + 1) * band - gap / 2
            rect = Rectangle(width=60 * mm, height=(y1 - y0) * mm, stroke_width=0, fill_opacity=1)
            rect.move_to(origin + np.array([HOOK_CX * mm, (y0 + y1) / 2 * mm, 0]))
            try:
                piece = Intersection(full, rect, color=color, fill_opacity=opacities[k % 2],
                                     stroke_color=C_HOOK_EDGE, stroke_width=stroke_width)
            except Exception:                                  # no boolean ops available: fall back to the band box
                piece = rect.set_fill(color, opacities[k % 2]).set_stroke(C_HOOK_EDGE, stroke_width)
            sheets.add(piece)
        sheets.pitch_mm = band
    else:
        raise ValueError(mode)
    sheets.mode = mode
    return sheets


# ----------------------------------------------------------------------------- deck of cards (2D side view)
class Deck(VGroup):
    """n thin tall cards standing side by side with a visible gap (= the interface between layers)."""

    def __init__(self, n=N_SHOW, w=0.42, h=2.2, gap=0.22, color=C_HOOK, edge=C_HOOK_EDGE,
                 opacities=(0.9, 0.78), **kw):
        super().__init__(**kw)
        self.n, self.cw, self.chh, self.gap = n, w, h, gap
        cards = VGroup()
        pitch = w + gap
        for i in range(n):
            r = Rectangle(width=w, height=h, stroke_width=1.6, stroke_color=edge,
                          fill_color=color, fill_opacity=opacities[i % 2])
            r.move_to([(i - (n - 1) / 2) * pitch, 0, 0])
            cards.add(r)
        self.add(cards)

    @property
    def cards(self):
        """The VGroup of cards (looked up from submobjects so it survives .copy() / .animate)."""
        return self.submobjects[0]

    def card(self, i):
        return self.cards[i]

    def iface_x(self, i):
        """x of the interface between card i and card i+1 (follows the current card positions)."""
        a, b = self.cards[i], self.cards[i + 1]
        return (a.get_right()[0] + b.get_left()[0]) / 2.0

    def tops(self):
        return [c.get_top() for c in self.cards]


def card_deck(n=N_SHOW, **kw):
    return Deck(n=n, **kw)


# ----------------------------------------------------------------------------- 2D force / shear marks
C_CORD = "#ECEFF1"


def force_arrow(p0, p1, color=C_F, width=4.0, tip=0.14):
    """Flat force arrow from p0 to p1 (screen or world points)."""
    return Arrow(np.array(p0, float), np.array(p1, float), buff=0, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.5)


def pull_arrows(deck, idxs=None, length=0.8, gap=0.04, **kw):
    """One upward force arrow standing on top of each (selected) card of a Deck."""
    out = VGroup()
    for i, c in enumerate(deck.cards):
        if idxs is not None and i not in idxs:
            continue
        top = c.get_top()
        out.add(force_arrow(top + UP * gap, top + UP * (gap + length), **kw))
    return out


def shear_pair(x, y, left_dir, length=0.4, sep=0.07, color=C_TAU, width=3.5, tip=0.1):
    """Two opposite arrows on the two faces of a vertical interface at x: left face points `left_dir` (UP/DOWN),
    right face the opposite -- action and reaction of the shear tau across the interface."""
    d = np.array(left_dir, float)
    a = force_arrow([x - sep, y - d[1] * length / 2, 0], [x - sep, y + d[1] * length / 2, 0], color, width, tip)
    b = force_arrow([x + sep, y + d[1] * length / 2, 0], [x + sep, y - d[1] * length / 2, 0], color, width, tip)
    return VGroup(a, b)


def check_mark(center=ORIGIN, size=0.3, color=C_AVG, width=7):
    """A drawn tick (no LaTeX)."""
    c = np.asarray(center, float)
    m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    m.set_points_as_corners([c + np.array([-0.55, 0.0, 0]) * size, c + np.array([-0.15, -0.45, 0]) * size,
                             c + np.array([0.6, 0.55, 0]) * size])
    return m


# ----------------------------------------------------------------------------- stress diagram (Q2, general)
def stress_diagram(sig_axial, sig_bend, height=2.2, scale=0.09, center=ORIGIN, show_labels=False):
    """Stress across the section depth (vertical line = section, x = stress). Positive stress to the RIGHT (inner
    fibre = side facing the hook cavity = TENSION, outer fibre = compression to the LEFT of the axis).
    Returns VGroup(uniform, triangle, trapezoid, axis) with attributes .inner_val / .outer_val / .zero_y."""
    c = np.asarray(center, float)
    top, bot = c + UP * height / 2, c - UP * height / 2
    s_in, s_out = sig_axial + sig_bend, sig_axial - sig_bend       # inner (tension) / outer (compression)
    # we draw the section horizontally: outer fibre on the LEFT edge, inner fibre on the RIGHT edge, stress up/down
    # -> keep it simple: horizontal section line of length `height`, stress along +y
    left, right = c + LEFT * height / 2, c + RIGHT * height / 2
    uniform = Polygon(left, right, right + UP * sig_axial * scale, left + UP * sig_axial * scale,
                      color=C_AVG, fill_opacity=0.35, stroke_width=2)
    tri = Polygon(left + UP * sig_axial * scale, right + UP * sig_axial * scale,
                  right + UP * (sig_axial + sig_bend) * scale, left + UP * (sig_axial - sig_bend) * scale,
                  color=C_SIG_T, fill_opacity=0.35, stroke_width=0)
    trap = Polygon(left, right, right + UP * s_in * scale, left + UP * s_out * scale,
                   color=WHITE, fill_opacity=0.0, stroke_width=3)
    axis = Line(left + LEFT * 0.3, right + RIGHT * 0.3, color=C_REF, stroke_width=2)
    g = VGroup(uniform, tri, trap, axis)
    g.inner_val, g.outer_val = s_in, s_out
    return g


# ----------------------------------------------------------------------------- live bars
class BarPair(VGroup):
    """Two bars sharing one baseline, heights and numbers driven by callables (one ValueTracker drives all).
    Remember .stop() before FadeOut (SKILL 3: clear_updaters before removing always_redraw objects)."""

    def __init__(self, get_a, get_b, color_a, color_b, base=ORIGIN, unit=0.12, bar_w=1.1, gap=1.4,
                 num_size=34, decimals=1, decimals_b=None):
        super().__init__()
        self.get_a, self.get_b, self.unit = get_a, get_b, unit
        self.base = np.asarray(base, float)
        xa, xb = self.base + LEFT * gap / 2, self.base + RIGHT * gap / 2
        self.ax, self.bx = xa, xb
        self.bar_a = always_redraw(lambda: self._bar(self.ax, self.get_a(), bar_w, color_a))
        self.bar_b = always_redraw(lambda: self._bar(self.bx, self.get_b(), bar_w, color_b))
        self.base_line = Line(self.base + LEFT * (gap / 2 + bar_w), self.base + RIGHT * (gap / 2 + bar_w),
                              color=C_REF, stroke_width=2)

        def mk_num(get, anchor_x, dec):
            n = DecimalNumber(get(), num_decimal_places=dec, font_size=num_size, color=WHITE, mob_class=Text)

            def place(m):
                m.set_value(get())
                m.move_to(anchor_x + UP * (get() * unit + 0.32))
            place(n)
            n.add_updater(place)
            return n
        self.num_a = mk_num(get_a, xa, decimals)
        self.num_b = mk_num(get_b, xb, decimals if decimals_b is None else decimals_b)
        self.add(self.base_line, self.bar_a, self.bar_b, self.num_a, self.num_b)

    def _bar(self, x, v, w, color):
        h = max(v * self.unit, 0.02)
        r = Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        r.move_to(x + UP * h / 2)
        return r

    def stop(self):
        for m in (self.bar_a, self.bar_b, self.num_a, self.num_b):
            m.clear_updaters()


# ----------------------------------------------------------------------------- table
def table_mob(rows, col_w, size=24, row_h=0.62, header_color=C_TXT2, colors=None, aligns=None):
    """Table as a VGroup of row-VGroups (row 0 = header). colors[r][c] overrides the text colour of a cell."""
    ncol = len(col_w)
    xs = np.cumsum([0] + list(col_w))
    rows_out = VGroup()
    for r, row in enumerate(rows):
        cells = VGroup()
        for c, txt in enumerate(row):
            col = header_color if r == 0 else WHITE
            if colors and colors.get(r, {}).get(c):
                col = colors[r][c]
            t = Text(txt, font_size=size - (2 if r == 0 else 0), color=col)
            fit_width(t, col_w[c] - 0.2)
            cx = (xs[c] + xs[c + 1]) / 2 - xs[-1] / 2
            t.move_to([cx, -r * row_h, 0])
            cells.add(t)
        line = Line([-xs[-1] / 2, -r * row_h - row_h / 2, 0], [xs[-1] / 2, -r * row_h - row_h / 2, 0],
                    color=C_REF, stroke_width=1.2, stroke_opacity=0.6)
        rows_out.add(VGroup(cells, line))
    return rows_out


# ----------------------------------------------------------------------------- title + page ref that never touch
def hook_title(key_title, key_ref, size=28, gap=0.4, ref_size=17, ref_max_w=3.5):
    """(title, page_ref) for the top bar. The cloud font (Loma) is ~19% wider than the local one (Leelawadee UI), so the
    title is fitted to the free width left of the ref at BUILD time, from the real measured widths: they cannot touch,
    in any font. (Cloud frame of A at t=1.5 s showed the title running into the ref before this helper.)"""
    ref = fit_width(page_ref(cap(key_ref), size=ref_size, color=GRAYTXT), ref_max_w)
    ref.move_to([X_MAX - ref.width / 2 - 0.28, REF_Y, 0])
    ttl = title(cap(key_title), size=size)
    fit_width(ttl, 2 * (ref.get_left()[0] - gap))          # the title is centred on x = 0, so the free width is symmetric
    return ttl, ref


# ----------------------------------------------------------------------------- centred caption (top zone)
def caption_c(key, size=24, color=GRAYTXT, max_w=11.0, y=CAP_TOP_Y, line_buff=0.1):
    """Top-zone caption from hook_captions, each line centred (the stock caption_top left-aligns line 2)."""
    lines = cap(key).split("\n")
    g = VGroup(*[Text(t, font_size=size, color=color) for t in lines]).arrange(DOWN, buff=line_buff)
    g.move_to([0, y, 0])
    return fit_width(g, max_w)


# ----------------------------------------------------------------------------- caption swap
def cap_swap(old, new, shift=UP * 0.1):
    """Caption change as ONE animation object: the old caption fades out, THEN the new one fades in (no cross-dissolve,
    which the layout linter -- rightly -- reports as text-on-text). Drop it into any self.play(...) call."""
    if old is None:
        return FadeIn(new, shift=shift)
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=1.0)


# ----------------------------------------------------------------------------- glow (SKILL 51/52)
def glow(scene, term, fig, color, run_time=1.5):
    """Equation term flashes WHITE and grows 25%, gets a sweeping box in its own variable colour, while the matching
    part of the figure flashes WHITE -- ONE self.play. `fig` may be a list of mobjects."""
    figs = fig if isinstance(fig, (list, tuple)) else [fig]
    scene.play(
        Indicate(term, color=WHITE, scale_factor=1.25),
        Circumscribe(term, color=color, buff=0.12, stroke_width=5, fade_out=True),
        *[Indicate(f, color=WHITE, scale_factor=1.0) for f in figs],
        run_time=run_time,
    )


# ----------------------------------------------------------------------------- plan-time contract
class Beats:
    """Mixin (put it BEFORE SafeScene in the bases).  self.mark(t, label) prints where the scene really is versus the
    plan's seconds; self.until(t) waits so a plan row ends exactly at t even though Manim rounds each animation
    up to whole frames.  Cloud logs therefore prove the contract: grep '[BEAT]'.  HOOK_TIMELINE=<file> dumps the
    per-animation timeline (index, start, end) for the local checkpoint extractor."""
    TOL = 0.12

    def play(self, *args, **kwargs):
        i, t0 = self.renderer.num_plays, float(self.time)
        super().play(*args, **kwargs)
        self.__dict__.setdefault("_tl", []).append(
            (i, round(t0, 3), round(float(self.time), 3), type(args[0]).__name__ if args else ""))

    def mark(self, t, label=""):
        now = float(self.time)
        flag = "ok" if abs(now - t) <= self.TOL else ("EARLY" if now < t else "LATE")
        print(f"[BEAT] plan {t:6.2f}s  actual {now:6.2f}s  {flag:5s} {label}", flush=True)

    def until(self, t, label=""):
        d = t - float(self.time)
        n = int(round(d * config.frame_rate))
        if n >= 1:                                   # wait(0) raises in Manim: skip gaps shorter than half a frame
            self.wait(n / config.frame_rate)
        elif d < -self.TOL:
            print(f"[BEAT] OVERRUN {-d:.2f}s before {t:.2f}s {label}", flush=True)

    def dump_timeline(self):
        import os, json
        path = os.environ.get("HOOK_TIMELINE")
        if path and hasattr(self, "_tl"):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"scene": type(self).__name__, "plays": self._tl}, f)

    def tear_down(self):
        self.dump_timeline()
        print(f"[BEAT] ===== {type(self).__name__} ends at {float(self.time):.2f}s =====", flush=True)
        super().tear_down()


# ----------------------------------------------------------------------------- 3D scene helpers
def cam_point(scene, p):
    """Where a 3D world point lands in frame coordinates under the CURRENT camera (for fixed-in-frame labels).
    The camera caches its rotation matrix until a frame is captured, so refresh it first (stale right after
    set_camera_orientation / in skipped animations)."""
    scene.camera.reset_rotation_matrix()
    return scene.camera.project_point(np.asarray(p, dtype=float))


def world_at_screen(scene, target_xy, z=0.0, start=(0.0, 0.0)):
    """World point on the plane Z=z that projects to the given screen position (used to park a legend triad)."""
    xy = np.array(start, float)

    def f(v):
        return cam_point(scene, np.array([v[0], v[1], z]))[:2]
    for _ in range(6):
        p0 = f(xy)
        jac = np.stack([(f(xy + [1e-3, 0]) - p0) / 1e-3, (f(xy + [0, 1e-3]) - p0) / 1e-3], axis=1)
        xy = xy + np.linalg.solve(jac, np.asarray(target_xy, float) - p0)
    return np.array([xy[0], xy[1], z])


def hud_label(scene, txt, anchor_world, offset=None, at=None, size=22, color=WHITE, leader=True,
              leader_color=C_TXT2, gap=0.08, stroke=2.0):
    """Fixed-in-frame label with a leader arrow from the label's border to a projected world point (SKILL 30: draw the
    line proving 'this is here'). Place it `offset` screen units from the point, or at absolute screen position `at`.
    scene.hud(...) is already called; FadeIn the returned (label, arrow) yourself. arrow is None if leader=False."""
    tgt = cam_point(scene, anchor_world)
    tgt2 = np.array([tgt[0], tgt[1], 0.0])
    lab = Text(txt, font_size=size, color=color)
    if at is not None:
        lab.move_to([at[0], at[1], 0.0])
    else:
        lab.move_to(tgt2 + np.array([offset[0], offset[1], 0.0]))
    arr = None
    if leader:
        c = lab.get_center()
        d = tgt2 - c
        u = d / (np.linalg.norm(d) + 1e-9)
        hw, hh = lab.width / 2 + gap, lab.height / 2 + gap
        t = min(hw / max(abs(u[0]), 1e-9), hh / max(abs(u[1]), 1e-9))
        arr = Arrow(c + u * t, tgt2, buff=0.0, color=leader_color, stroke_width=stroke,
                    tip_length=0.14, max_tip_length_to_length_ratio=0.5)
        scene.hud(lab, arr)
    else:
        scene.hud(lab)
    return lab, arr
