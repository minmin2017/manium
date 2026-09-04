"""Fluid Power Control — W07 Hydraulic Circuit Design (hydraulic05.pdf)
Page-by-page clips (skill rule: one clip per lecture-slide page) for the 11
pages NOT already covered by HC01_Regenerative (p.4), HC02_SeriesVsParallel
(p.11-12), HC03_MeterInOut (p.13).

DESIGN DECISION (full spec: `Desktop/Main_note/Claude_Specs/Manim — Hydraulic
Circuit Design (W07) Geometry Spec.md`): pages 2/3/5/9/10/14/15 pack 2-3
complete valve+cylinder(+pump) circuits into one 14.222-wide frame. The
cutaway mechanisms in hydraulic_valves.py (four_way_housing, branch_t_body)
are ~7 units wide EACH — three side by side would need 22+ units. So this
file uses COMPACT ISO-style schematic symbols (box + colored port stubs +
internal flow-path line) instead — matching the note's own framing that this
chapter's skill is "reading a schematic and tracing flow", not re-deriving
valve internals (W06/HV01-25 already covered internals in full cutaway detail).

Style: current house style (title()+page_ref()+caption_top() from mlib,
matching HV01-25 and the task brief's pointer at HV01_Title/HV14_Title) — NOT
the older ad-hoc style of the already-shipped HC01-03 clips (no page_ref,
"Week N —" titles). This is a deliberate, noted evolution, not an oversight.

Content verified against the lesson note text (page-by-page, cited inline in
each class docstring) plus, for the two circuits with no direct textbook
walkthrough in the note, an external source check (2026-09-04):
- HC12 bottom (4-check-valve bridge / hydraulic "rectifier"): confirmed real
  topology via powermotiontech.com "Bridge Circuit Provides One-Way Flow" —
  4 check valves in a diamond give unidirectional output regardless of which
  supply line is pressurized. Matches the note's own electrical-rectifier
  analogy.
- HC13 (hydrostatic transmission replenishing circuit): confirmed via patent
  literature (US4185521 family) that a closed-loop charge circuit is charge
  pump + relief valve + TWO check valves (one per loop line, each opens only
  when its own line is the low side) — matches building 2 check valves, not 1.
"""
from mlib import *
import numpy as np
from hydraulic_valves import SUPPLY, RETURN, BLOCKED, SECONDARY, spring_zigzag

PILOT = WARN            # pilot/control signal line (matches HV18/HV20 convention)
CYL2 = SECONDARY        # "second" actuator / second circuit, distinguishing color
HI_FLOW = OK            # high-flow pump path (page 5 hi-lo)
LOAD_COL = GRAYTXT


# =====================================================================
# Reusable compact ISO-style symbol builders
# Every builder returns (VGroup, ports) where ports maps a name -> absolute
# [x,y,0] np.array — every pipe in a scene is drawn FROM these returned
# coordinates, never a second hand-guess (skill §24).
# =====================================================================

def pipe(points, color=METAL, width=2.5):
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [np.asarray(p, dtype=float) for p in points])


def elbow_pts(p1, p2, via="y", frac=0.5):
    """Two straight legs meeting at one right-angle bend — the standard pipe
    shape used throughout the W06 HV-series (never a diagonal wire)."""
    p1 = np.asarray(p1, dtype=float)
    p2 = np.asarray(p2, dtype=float)
    if via == "y":
        my = p1[1] + (p2[1] - p1[1]) * frac
        return [p1, [p1[0], my, 0], [p2[0], my, 0], p2]
    my = p1[0] + (p2[0] - p1[0]) * frac
    return [p1, [my, p1[1], 0], [my, p2[1], 0], p2]


def flow_dots(points, color, n=4, run_time=1.6, radius=0.06):
    path = VMobject().set_points_as_corners([np.asarray(p, dtype=float) for p in points])
    dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(n)])
    anims = [MoveAlongPath(d, path, rate_func=linear, run_time=run_time) for d in dots]
    return dots, anims


def rotor_symbol(center, angle=PI / 2, r=0.34, color=SUPPLY, filled=True, bidir=False):
    """Generic ISO pump/motor glyph: circle + triangle pointing along `angle`.
    filled=True -> pump (solid triangle, flow OUT). filled=False -> motor
    (open triangle, flow IN). bidir also draws the opposite-pointing triangle
    (reversible pump/motor, page 15). Ports 'a' (inlet side, angle+180) and
    'b' (outlet side, angle), each r from center."""
    cx, cy = center[0], center[1]
    circle = Circle(radius=r, color=color, stroke_width=3).move_to([cx, cy, 0])

    def tri(a):
        t = Triangle(color=color, fill_color=color,
                     fill_opacity=1 if filled else 0, stroke_width=3)
        t.scale(r * 0.55)
        t.rotate(a - PI / 2)
        t.move_to([cx, cy, 0])
        return t

    grp = VGroup(circle, tri(angle))
    if bidir:
        grp.add(tri(angle + PI))
    a_pt = np.array([cx + r * np.cos(angle + PI), cy + r * np.sin(angle + PI), 0])
    b_pt = np.array([cx + r * np.cos(angle), cy + r * np.sin(angle), 0])
    return grp, {"a": a_pt, "b": b_pt}


def variable_slash(center, r=0.34, color=WHITE):
    """ISO 'adjustable' diagonal-arrow overlay for a variable-displacement pump."""
    cx, cy = center[0], center[1]
    return Arrow([cx - r * 0.95, cy - r * 0.95, 0], [cx + r * 0.95, cy + r * 0.95, 0],
                 color=color, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.35)


def tank_symbol(center, w=0.7, h=0.5, color=METAL):
    cx, cy = center[0], center[1]
    body = VMobject(color=color, stroke_width=2.5).set_points_as_corners([
        [cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0],
        [cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0],
    ])
    vent = Line([cx, cy + h / 2, 0], [cx, cy + h / 2 + 0.15, 0], color=color, stroke_width=2.5)
    return VGroup(body, vent), {"top": np.array([cx, cy + h / 2, 0])}


def cylinder_double(center, w=2.0, h=0.62, piston_frac=0.5, rod_len=0.45,
                     stub=0.22, color=METAL, tint=None):
    cx, cy = center[0], center[1]
    left, right = cx - w / 2, cx + w / 2
    fill = VGroup()
    if tint is not None:
        fill.add(Rectangle(width=w, height=h - 0.06, fill_color=tint, fill_opacity=0.18,
                            stroke_width=0).move_to([cx, cy, 0]))
    barrel = Rectangle(width=w, height=h, color=color, stroke_width=2.5).move_to([cx, cy, 0])
    piston_x = left + w * piston_frac
    piston = Line([piston_x, cy - h / 2 + 0.04, 0], [piston_x, cy + h / 2 - 0.04, 0],
                  color=WHITE, stroke_width=5)
    rod = Line([right, cy, 0], [right + rod_len, cy, 0], color=WHITE, stroke_width=6)
    he_top = np.array([left + w * 0.18, cy - h / 2, 0])
    re_top = np.array([right - w * 0.18, cy - h / 2, 0])
    he_bot = he_top + np.array([0, -stub, 0])
    re_bot = re_top + np.array([0, -stub, 0])
    stubs = VGroup(Line(he_top, he_bot, color=color, stroke_width=2.5),
                   Line(re_top, re_bot, color=color, stroke_width=2.5))
    grp = VGroup(fill, barrel, piston, rod, stubs)
    return grp, {"he": he_bot, "re": re_bot, "piston": piston}


def cylinder_single(center, w=1.4, h=0.55, stub=0.22, color=METAL):
    """Single-acting cylinder, spring-return — ONE working port only (bottom
    of the cap end); the rod side is open/vented, matching the note's own
    'ถอยด้วยแรงภายนอก/สปริง' description for page 2's left circuit."""
    cx, cy = center[0], center[1]
    left, right = cx - w / 2, cx + w / 2
    barrel = Rectangle(width=w, height=h, color=color, stroke_width=2.5).move_to([cx, cy, 0])
    piston_x = left + w * 0.32
    piston = Line([piston_x, cy - h / 2 + 0.04, 0], [piston_x, cy + h / 2 - 0.04, 0],
                  color=WHITE, stroke_width=5)
    spring = spring_zigzag(piston_x + 0.05, right - 0.05, cy, coils=4, amp=0.08)
    rod = Line([right, cy, 0], [right + 0.35, cy, 0], color=WHITE, stroke_width=6)
    p_top = np.array([left + w * 0.2, cy - h / 2, 0])
    p_bot = p_top + np.array([0, -stub, 0])
    stub_line = Line(p_top, p_bot, color=color, stroke_width=2.5)
    grp = VGroup(barrel, piston, spring, rod, stub_line)
    return grp, {"p": p_bot}


def cylinder_vertical(center, h=1.8, w=0.55, stub=0.2, color=METAL, load=True):
    """Vertical lift cylinder — rod exits DOWNWARD to a hanging load (mirrors
    HV20_Counterbalance's own already-verified layout exactly: cap-end port
    at the TOP = direct line, rod-end port near the BOTTOM = routed via the
    counterbalance valve). Retracting the rod lifts the load toward the
    barrel."""
    cx, cy = center[0], center[1]
    top, bot = cy + h / 2, cy - h / 2
    barrel = Rectangle(width=w, height=h, color=color, stroke_width=2.5).move_to([cx, cy, 0])
    piston_y = cy + h * 0.18
    piston = Line([cx - w / 2 + 0.04, piston_y, 0], [cx + w / 2 - 0.04, piston_y, 0],
                  color=WHITE, stroke_width=5)
    rod = Line([cx, bot, 0], [cx, bot - 0.5, 0], color=WHITE, stroke_width=6)
    grp = VGroup(barrel, piston, rod)
    if load:
        load_blk = Rectangle(width=0.85, height=0.42, color=LOAD_COL, fill_color=LOAD_COL,
                              fill_opacity=0.55, stroke_width=2).move_to([cx, bot - 0.9, 0])
        load_lbl = Text("โหลด", font_size=12, color=LOAD_COL).move_to([cx, bot - 0.9, 0])
        grp.add(load_blk, load_lbl)
    cap_stub_top = np.array([cx, top, 0])
    cap_stub_bot = cap_stub_top + np.array([0, stub, 0])
    rod_stub_top = np.array([cx + w / 2, bot + h * 0.12, 0])
    rod_stub_bot = rod_stub_top + np.array([stub, 0, 0])
    stubs = VGroup(Line(cap_stub_top, cap_stub_bot, color=color, stroke_width=2.5),
                   Line(rod_stub_top, rod_stub_bot, color=color, stroke_width=2.5))
    grp.add(stubs)
    return grp, {"cap": cap_stub_bot, "rod": rod_stub_bot}


def dcv_box(center, w=1.5, h=0.95, ways=4, labeled=True, stub=0.22):
    """Directional-control-valve body: rectangle + colored port stubs
    (P=red/SUPPLY bottom-left, T=blue/RETURN bottom-right, A=top-left,
    B=top-right if ways==4). Returns (VGroup, ports) where each port value is
    the OUTER tip of its stub (pipes attach here)."""
    cx, cy = center[0], center[1]
    body = Rectangle(width=w, height=h, fill_color=METAL, fill_opacity=0.15,
                      stroke_color=WHITE, stroke_width=2.5).move_to([cx, cy, 0])
    off = w * 0.27
    base = {"P": np.array([cx - off, cy - h / 2, 0]),
            "T": np.array([cx + off, cy - h / 2, 0]),
            "A": np.array([cx - off, cy + h / 2, 0])}
    if ways == 4:
        base["B"] = np.array([cx + off, cy + h / 2, 0])
    pcolor = {"P": SUPPLY, "T": RETURN, "A": WHITE, "B": WHITE}
    grp = VGroup(body)
    ports = {}
    for name, pt in base.items():
        direction = DOWN if name in ("P", "T") else UP
        end = pt + direction * stub
        grp.add(Line(pt, end, color=pcolor[name], stroke_width=3.5))
        if labeled:
            lbl = Text(name, font_size=13, color=pcolor[name]).next_to(end, direction, buff=0.05)
            grp.add(lbl)
        ports[name] = end
    return grp, ports


def dcv_path(ports, pairs, stub=0.22):
    """Internal flow-path line(s) inside a dcv_box, connecting named ports'
    INNER base points (undoes the stub extension so the line reads as
    'inside the body', not floating past the wall). pairs = [(a,b,color),..]."""
    grp = VGroup()
    for a, b, color in pairs:
        pa = np.array(ports[a], dtype=float).copy()
        pb = np.array(ports[b], dtype=float).copy()
        pa[1] += stub if a in ("P", "T") else -stub
        pb[1] += stub if b in ("P", "T") else -stub
        mid_y = (pa[1] + pb[1]) / 2
        grp.add(pipe([pa, [pa[0], mid_y, 0], [pb[0], mid_y, 0], pb], color=color, width=4))
    return grp


def blocked_mark(pt, size=0.09):
    return VGroup(
        Line(pt + np.array([-size, -size, 0]), pt + np.array([size, size, 0]),
             color=BLOCKED, stroke_width=3),
        Line(pt + np.array([-size, size, 0]), pt + np.array([size, -size, 0]),
             color=BLOCKED, stroke_width=3),
    )


def check_valve_symbol(center, angle=0, size=0.32, color=WHITE):
    """Ball-and-seat check-valve glyph. angle=0 -> free flow runs left-to-right."""
    ball = Circle(radius=size * 0.28, color=color, stroke_width=2.5)
    seat1 = Line([-size * 0.32, size * 0.22, 0], [-size * 0.02, 0.0, 0], color=color, stroke_width=2.5)
    seat2 = Line([-size * 0.32, -size * 0.22, 0], [-size * 0.02, 0.0, 0], color=color, stroke_width=2.5)
    grp = VGroup(ball, seat1, seat2)
    grp.rotate(angle)
    grp.move_to([center[0], center[1], 0])
    in_pt = np.array([center[0] - size / 2 * np.cos(angle), center[1] - size / 2 * np.sin(angle), 0])
    out_pt = np.array([center[0] + size / 2 * np.cos(angle), center[1] + size / 2 * np.sin(angle), 0])
    return grp, {"in": in_pt, "out": out_pt}


def pilot_check_valve_symbol(center, angle=0, pilot_angle=None, pilot_len=0.5,
                              size=0.32, color=WHITE):
    if pilot_angle is None:
        pilot_angle = angle + PI / 2
    chk, ports = check_valve_symbol(center, angle=angle, size=size, color=color)
    p_end = np.array([center[0] + pilot_len * np.cos(pilot_angle),
                       center[1] + pilot_len * np.sin(pilot_angle), 0])
    pilot_line = DashedLine([center[0], center[1], 0], p_end, color=PILOT,
                            stroke_width=2.5, dash_length=0.08)
    piston = Rectangle(width=0.13, height=0.13, color=PILOT, fill_color=PILOT,
                        fill_opacity=0.85, stroke_width=1).move_to(p_end)
    ports["pilot"] = p_end
    return VGroup(chk, pilot_line, piston), ports


_PC_NAMES = {"relief": "Relief", "sequence": "Sequence", "counterbalance": "Counterbalance",
             "unloading": "Unloading", "reducing": "PRV", "flowcontrol": "FCV"}


def pc_valve_box(center, w=0.62, h=0.52, kind="relief", color=METAL, label_color=GRAYTXT,
                 label=True):
    """Generic pressure/flow-control valve glyph (box + spring + diagonal
    orifice arrow) shared by relief/sequence/counterbalance/unloading/
    reducing/flow-control — matching real ISO practice where these are
    near-identical base symbols told apart by label + pilot-line routing."""
    cx, cy = center[0], center[1]
    body = Rectangle(width=w, height=h, color=color, stroke_width=2.5,
                      fill_color=color, fill_opacity=0.12).move_to([cx, cy, 0])
    spring = spring_zigzag(cx - w * 0.16, cx + w * 0.16, cy + h / 2 + 0.09, coils=3, amp=0.055)
    arrow = Arrow([cx - w * 0.28, cy - h * 0.28, 0], [cx + w * 0.28, cy + h * 0.28, 0],
                  color=color, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.35)
    grp = VGroup(body, spring, arrow)
    full = VGroup(grp)
    if label:
        lbl = Text(_PC_NAMES.get(kind, kind), font_size=12, color=label_color)
        lbl.next_to(grp, DOWN, buff=0.08)
        full.add(lbl)
    ports = {"left": np.array([cx - w / 2, cy, 0]), "right": np.array([cx + w / 2, cy, 0]),
             "top": np.array([cx, cy + h / 2, 0]), "bottom": np.array([cx, cy - h / 2, 0])}
    return full, ports


def bridge_rectifier(center, size=1.1, color=METAL):
    """4-check-valve bridge (hydraulic 'rectifier') — verified topology
    (powermotiontech.com, 2026-09-04): diamond of 4 nodes (top=motor_in,
    bottom=motor_out, left/right=the two swap-able supply lines), diagonal
    check valves oriented left->top, right->top, bot->left, bot->right, so
    whichever side (left/right) is currently pressurized always feeds the
    TOP node and the LOW side always receives the BOTTOM node's return —
    output direction at top/bottom never changes."""
    cx, cy = center[0], center[1]
    top = np.array([cx, cy + size / 2, 0])
    bot = np.array([cx, cy - size / 2, 0])
    left = np.array([cx - size / 2, cy, 0])
    right = np.array([cx + size / 2, cy, 0])

    def ang(p, q):
        d = np.asarray(q) - np.asarray(p)
        return float(np.arctan2(d[1], d[0]))

    chk_TL, _ = check_valve_symbol((left + top) / 2, angle=ang(left, top), size=0.26)
    chk_TR, _ = check_valve_symbol((right + top) / 2, angle=ang(right, top), size=0.26)
    chk_BL, _ = check_valve_symbol((left + bot) / 2, angle=ang(bot, left), size=0.26)
    chk_BR, _ = check_valve_symbol((right + bot) / 2, angle=ang(bot, right), size=0.26)
    edges = VGroup(
        Line(left, top, color=color, stroke_width=2), Line(right, top, color=color, stroke_width=2),
        Line(left, bot, color=color, stroke_width=2), Line(right, bot, color=color, stroke_width=2),
    )
    checks = VGroup(chk_TL, chk_TR, chk_BL, chk_BR)
    return VGroup(edges, checks), {"top": top, "bot": bot, "left": left, "right": right}


# =====================================================================
# HC14 — page 1: cover slide
# =====================================================================

class HC14_Title(SafeScene):
    """Page 1 — cover slide. Matches HV01_Title/HV14_Title exactly."""

    def construct(self):
        pref = page_ref("หน้า 1 · Hydraulic Circuit Design")
        t = Text("Hydraulic Circuit Design", font_size=48, color=WHITE)
        sub = fit_width(Text("เอาวาล์วจาก W06 มาประกอบเป็นวงจรใช้งานจริง — อ่านผังวงจร ไล่ทิศทางการไหล",
                              font_size=20, color=GRAYTXT), 11.0)
        sub.next_to(t, DOWN, buff=0.6)
        self.play(FadeIn(pref), Write(t), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.4), run_time=0.8)
        self.wait(1.6)
        self.fade_out_all(run_time=0.8)


# =====================================================================
# HC04 — page 2: Basic Cylinder Control (3 zones)
# =====================================================================

class HC04_BasicCylinderControl(SafeScene):
    """Page 2 — Basic Cylinder Control: 3 simplest circuits side by side.
    (L) 3-way valve on a single-acting cylinder (pushes one way, spring/
    external-force return). (M) two independent 3-way valves, one per end of
    a double-rod cylinder. (R) one standard 4-way valve on a double-acting
    cylinder, + an optional pressure-reducing valve add-on. Verified against
    the note's own text for page 2 — no new components vs W06 (HV07 three-way,
    HV08 four-way, HV17 pressure-reducing)."""

    def construct(self):
        ttl = title("Basic Cylinder Control")
        pref = page_ref("หน้า 2 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        cap0 = caption_top("3 วงจรพื้นฐานที่สุด — ทุกอันคือวาล์วจาก W06 เดิม แค่ต่อสายต่างแบบ")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(cap0), run_time=0.3)

        # ---- LEFT: 3-way + single-acting cylinder ----------------------
        vL, pL = dcv_box([-4.6, 0.85, 0], w=1.25, h=0.8, ways=3)
        cylL, pcL = cylinder_single([-4.6, -1.15, 0], w=1.2, h=0.48)
        pipeL = pipe(elbow_pts(pL["A"], pcL["p"]))
        lblL = Text("3-way + single-acting\n(ถอยด้วยสปริง)", font_size=13, color=GRAYTXT,
                    line_spacing=0.9).move_to([-4.6, -2.15, 0])
        zoneL = VGroup(vL, cylL, pipeL, lblL)

        # ---- MID: 2x 3-way valves + double-rod cylinder -----------------
        vM1, pM1 = dcv_box([0, 1.55, 0], w=1.1, h=0.7, ways=3, labeled=False)
        vM2, pM2 = dcv_box([0, 0.05, 0], w=1.1, h=0.7, ways=3, labeled=False)
        barrelM = Rectangle(width=1.7, height=0.5, color=METAL, stroke_width=2.5).move_to([0, -1.35, 0])
        pistonM = Line([0, -1.6, 0], [0, -1.1, 0], color=WHITE, stroke_width=5)
        rodM_L = Line([-0.85, -1.35, 0], [-1.25, -1.35, 0], color=WHITE, stroke_width=6)
        rodM_R = Line([0.85, -1.35, 0], [1.25, -1.35, 0], color=WHITE, stroke_width=6)
        cylM = VGroup(barrelM, pistonM, rodM_L, rodM_R)
        portM_L = np.array([-0.6, -1.6, 0])
        portM_R = np.array([0.6, -1.6, 0])
        stubM = VGroup(Line([-0.6, -1.6, 0], [-0.6, -1.82, 0], color=METAL, stroke_width=2.5),
                       Line([0.6, -1.6, 0], [0.6, -1.82, 0], color=METAL, stroke_width=2.5))
        portM_L = np.array([-0.6, -1.82, 0])
        portM_R = np.array([0.6, -1.82, 0])
        pipeM1 = pipe(elbow_pts(pM1["A"], portM_L, via="y", frac=0.7))
        pipeM2 = pipe(elbow_pts(pM2["A"], portM_R, via="y", frac=0.35))
        lblM = Text("2x 3-way — คุมอิสระคนละฝั่ง\n(double-rod cylinder)", font_size=13,
                    color=GRAYTXT, line_spacing=0.9).move_to([0, -2.15, 0])
        zoneM = VGroup(vM1, vM2, cylM, stubM, pipeM1, pipeM2, lblM)

        # ---- RIGHT: 4-way + double-acting cylinder + optional PRV -------
        vR, pR = dcv_box([4.6, 0.85, 0], w=1.35, h=0.85, ways=4)
        cylR, pcR = cylinder_double([4.6, -1.15, 0], w=1.5, h=0.5)
        pipeR_A = pipe(elbow_pts(pR["A"], pcR["he"], via="y", frac=0.7))
        pipeR_B = pipe(elbow_pts(pR["B"], pcR["re"], via="y", frac=0.55))
        prv, prv_ports = pc_valve_box([4.6, 1.85, 0], kind="reducing")
        prv_tap = pipe([[4.6, pR["A"][1] + 0.42, 0], prv_ports["bottom"]])
        lblR = Text("4-way + double-acting\n(+PRV ออปชัน)", font_size=13, color=GRAYTXT,
                    line_spacing=0.9).move_to([4.6, -2.15, 0])
        zoneR = VGroup(vR, cylR, pipeR_A, pipeR_B, prv, prv_tap, lblR)

        self.play(FadeIn(zoneL, shift=UP * 0.4), run_time=0.8)
        self.play(FadeIn(zoneM, shift=UP * 0.4), run_time=0.8)
        self.play(FadeIn(zoneR, shift=UP * 0.4), run_time=0.8)

        cap1 = caption_top("ซ้าย: ดันทางเดียวด้วยแรงดันน้ำมัน — ถอยกลับด้วยสปริง/แรงภายนอก")
        self.play(FadeIn(cap1), run_time=0.6)
        # start the flow slightly above P's own port-glyph label (buff=0.05,
        # dot radius=0.06 -> t=0 dot would otherwise sit on top of the label,
        # caught by [LAYOUT] on the 2026-09-04 draft render)
        dotsL, animsL = flow_dots([pL["P"] + np.array([0, 0.15, 0]), pL["A"],
                                   *elbow_pts(pL["A"], pcL["p"])[1:]],
                                  SUPPLY, n=3, run_time=1.3)
        self.play(LaggedStart(*animsL, lag_ratio=0.25))
        self.play(FadeOut(dotsL), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("กลาง: วาล์วคนละตัวคุมปลายคนละฝั่ง — สั่งเคลื่อนไหวได้อิสระต่อกัน")
        self.play(FadeIn(cap2), run_time=0.6)
        dotsM1, animsM1 = flow_dots([pM1["P"], pM1["A"], *elbow_pts(pM1["A"], portM_L, via="y", frac=0.7)[1:]],
                                    SUPPLY, n=3, run_time=1.2)
        self.play(LaggedStart(*animsM1, lag_ratio=0.25))
        self.play(FadeOut(dotsM1), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("ขวา: มาตรฐานที่สุด — วาล์วเดียวคุมยืด-หดครบทั้ง 2 ทิศ")
        self.play(FadeIn(cap3), run_time=0.6)
        dotsR, animsR = flow_dots([pR["P"], pR["A"], *elbow_pts(pR["A"], pcR["he"], via="y", frac=0.7)[1:]],
                                  SUPPLY, n=3, run_time=1.2)
        dotsR2, animsR2 = flow_dots([pcR["re"], *elbow_pts(pcR["re"], pR["B"], via="y", frac=0.45)[1:-1], pR["B"]],
                                    RETURN, n=3, run_time=1.2)
        self.play(LaggedStart(*animsR, *animsR2, lag_ratio=0.2))
        self.play(FadeOut(dotsR), FadeOut(dotsR2), run_time=0.3)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("3 แบบนี้คือฐานของวงจรทั้งบท — ที่เหลือคือการเพิ่มเงื่อนไขเข้าไป")
        self.play(FadeIn(cap4), run_time=0.7)
        self.wait(1.5)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC05 — page 3: Open Center vs Closed Center Control
# =====================================================================

class HC05_OpenClosedCenter(SafeScene):
    """Page 3 — Open Center and Closed Center Control: compares (L)
    open/closed-center valve + VARIABLE-displacement pump (self-adjusts
    output to load, no relief needed) vs (R) standard valve + FIXED-
    displacement pump (must always carry a relief valve, since a fixed pump
    always makes constant flow regardless of demand). Verified against the
    note's own [!tip] callout — the physical reason (not just the two
    pictures) is stated on screen."""

    def construct(self):
        ttl = title("Open vs Closed Center")
        pref = page_ref("หน้า 3 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        # ---- LEFT: variable pump, no relief needed ----------------------
        pumpL, ppL = rotor_symbol([-3.3, 1.5, 0], angle=PI / 2, color=SUPPLY)
        slashL = variable_slash([-3.3, 1.5, 0])
        tankL, ptL = tank_symbol([-4.3, 0.4, 0])
        vL, pvL = dcv_box([-3.3, -0.6, 0], w=1.4, h=0.85, ways=4)
        lineL_up = pipe(elbow_pts(ppL["b"], pvL["P"]))
        lineL_tank = pipe(elbow_pts([-4.3, 1.2, 0], ptL["top"], via="y"))
        lblL = Text("ปั๊ม Variable Displacement", font_size=14, color=SUPPLY).move_to([-3.3, 2.15, 0])
        lblL2 = Text("ไม่ต้องมี relief — ปั๊มปรับ output เอง", font_size=13, color=GRAYTXT).move_to([-3.3, -1.75, 0])
        zoneL = VGroup(pumpL, slashL, tankL, vL, lineL_up, lineL_tank, lblL, lblL2)

        # ---- RIGHT: fixed pump, relief mandatory -------------------------
        pumpR, ppR = rotor_symbol([3.3, 1.5, 0], angle=PI / 2, color=SUPPLY)
        tankR, ptR = tank_symbol([2.3, 0.4, 0])
        vR, pvR = dcv_box([3.3, -0.6, 0], w=1.4, h=0.85, ways=4)
        relief, relief_p = pc_valve_box([4.5, 0.9, 0], kind="relief")
        lineR_up = pipe(elbow_pts(ppR["b"], pvR["P"]))
        lineR_relief = pipe([ppR["b"] + np.array([0, 0.15, 0]), [4.5, ppR["b"][1] + 0.15, 0], relief_p["top"]])
        lineR_reliefdrain = pipe(elbow_pts(relief_p["bottom"], [2.3, 1.2, 0], via="x"))
        lineR_tank = pipe(elbow_pts([2.3, 1.2, 0], ptR["top"], via="y"))
        lblR = Text("ปั๊ม Fixed Displacement", font_size=14, color=SUPPLY).move_to([3.3, 2.15, 0])
        lblR2 = Text("ต้องมี relief เสมอ — ปั๊มไหลคงที่ตลอด", font_size=13, color=GRAYTXT).move_to([3.3, -1.75, 0])
        zoneR = VGroup(pumpR, tankR, vR, relief, lineR_up, lineR_relief, lineR_reliefdrain,
                       lineR_tank, lblR, lblR2)

        self.play(FadeIn(zoneL, shift=UP * 0.4), run_time=1.0)
        self.play(FadeIn(zoneR, shift=UP * 0.4), run_time=1.0)

        cap1 = caption_top("ซ้าย: วาล์วอยู่กลาง (ไม่ทำงาน) — ปั๊ม variable ปรับตัวเองให้ไหลน้อยลงพอดี")
        self.play(FadeIn(cap1), run_time=0.7)
        dotsL, animsL = flow_dots([ppL["b"], pvL["P"]], SUPPLY, n=2, run_time=1.0)
        self.play(LaggedStart(*animsL, lag_ratio=0.3))
        self.play(FadeOut(dotsL), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("ขวา: วาล์วอยู่กลาง — ปั๊ม fixed ยังไหลเท่าเดิม น้ำมันส่วนเกินต้องมีทางไป")
        self.play(FadeIn(cap2), run_time=0.7)
        dotsR, animsR = flow_dots([ppR["b"], relief_p["top"], relief_p["bottom"],
                                   [2.3, 1.2, 0], ptR["top"]], WARN, n=4, run_time=1.8)
        self.play(LaggedStart(*animsR, lag_ratio=0.22))
        self.play(FadeOut(dotsR), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = fit_width(caption_top(
            "กฎ: ปั๊ม fixed = flow คงที่เสมอไม่ว่าโหลดต้องการเท่าไหร่ ⇒ ต้องมี relief ระบายทิ้ง"
            " | ปั๊ม variable = ปรับ output ตามโหลดจริง ⇒ ประหยัดพลังงานกว่า"), 12.6)
        self.play(FadeIn(cap3), run_time=0.8)
        self.wait(2.0)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC06 — page 5: Drilling Machine Application (callback to HC01)
# =====================================================================

class HC06_DrillingMachineApplication(SafeScene):
    """Page 5 — Drilling Machine Application: two real uses that both solve
    "fast approach, then slow/controlled work stroke" — (L) the SAME
    regenerative circuit from page 4 (HC01), applied to drilling; (R) an
    alternative that doesn't use regeneration at all — a double-pump (hi-lo)
    circuit where an unloading valve automatically cuts the high-flow pump
    out once pressure rises. Opens with an explicit callback to HC01 per
    skill §21 rule 2 (segments/clips on the same underlying idea must
    reference what was just shown, not hard-cut to an unrelated picture)."""

    def construct(self):
        ttl = title("Drilling Machine Application")
        pref = page_ref("หน้า 5 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        cap0 = caption_top("จากวงจร regenerative ที่เพิ่งเห็นในหน้าที่แล้ว (HC01) — เอามาใช้งานจริงตรงนี้")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.1)
        self.play(FadeOut(cap0), run_time=0.4)

        # ---- LEFT: regenerative circuit reused for drilling --------------
        vL, pvL = dcv_box([-3.3, 1.3, 0], w=1.35, h=0.85, ways=4)
        cylL, pcL = cylinder_double([-3.3, -0.9, 0], w=1.7, h=0.55)
        pipeL_he = pipe(elbow_pts(pvL["A"], pcL["he"], via="y", frac=0.7))
        # Loop A<->B together (regen): straight elbow segments routed AROUND
        # the cylinder/valve on the far left (x=-4.4, clear of cylL's left
        # edge at -4.15) — never a smooth diagonal curve, matching every
        # other pipe in this file (a set_points_smoothly version of this
        # overshot badly and crossed the caption text, caught in review).
        loop_pts = [pcL["re"], [pcL["re"][0], -1.9, 0], [-4.4, -1.9, 0],
                    [-4.4, pvL["B"][1], 0], pvL["B"]]
        loop = pipe(loop_pts, color=WARN, width=4)
        loop_lbl = fit_width(Text("A กับ B ต่อรวมกัน (regen)", font_size=12, color=WARN), 1.7)
        loop_lbl.move_to([-3.6, -2.15, 0])
        bit = Triangle(color=METAL, fill_color=METAL, fill_opacity=1, stroke_width=0)
        bit.scale(0.14).rotate(PI).move_to([-3.3, -1.42, 0])
        bit_lbl = Text("หัวเจาะ", font_size=12, color=GRAYTXT).move_to([-3.3, -1.65, 0])
        lblL = fit_width(Text("Regenerative — เร็วตอนเข้าใกล้ ช้าลงตอนเจาะจริง", font_size=12,
                    color=GRAYTXT), 1.7)
        lblL.move_to([-2.7, 0.15, 0])
        zoneL = VGroup(vL, cylL, pipeL_he, loop, loop_lbl, bit, bit_lbl, lblL)

        self.play(FadeIn(zoneL, shift=UP * 0.4), run_time=1.0)
        cap1 = caption_top("ซ้าย: วิธีเดิมจากหน้าที่แล้ว — วิ่งเข้าเร็วตอนยังไม่ชนงาน ช้าลงเองตอนเจาะจริง")
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(cap1), run_time=0.3)

        # ---- RIGHT: double-pump hi-lo circuit -----------------------------
        pumpHi, pHi = rotor_symbol([3.0, 1.55, 0], angle=PI / 2, color=HI_FLOW)
        pumpLo, pLo = rotor_symbol([4.6, 1.55, 0], angle=PI / 2, color=SUPPLY)
        lblHi = Text("Hi-flow", font_size=11, color=HI_FLOW).next_to(pumpHi, UP, buff=0.08)
        lblLo = Text("Lo-flow", font_size=11, color=SUPPLY).next_to(pumpLo, UP, buff=0.08)
        unload, unload_p = pc_valve_box([3.0, 0.9, 0], kind="unloading")
        junction = np.array([3.8, 1.3, 0])
        lineHi = pipe(elbow_pts(pHi["b"], unload_p["top"], via="y"))
        lineLo = pipe(elbow_pts(pLo["b"], junction, via="y"))
        lineJoin = pipe([unload_p["bottom"], [3.0, 1.3, 0], junction])
        vR, pvR = dcv_box([3.8, -0.4, 0], w=1.3, h=0.8, ways=4)
        lineToValve = pipe(elbow_pts(junction, pvR["P"], via="y"))
        cylR, pcR = cylinder_double([3.8, -1.9, 0], w=1.5, h=0.5)
        pipeR_A = pipe(elbow_pts(pvR["A"], pcR["he"]))
        tankUL, tpUL = tank_symbol([1.9, 0.9, 0])
        drainUL = pipe(elbow_pts(unload_p["left"], tpUL["top"], via="x"))
        # NOTE: originally at (3.8, 0.15) which sits right on lineToValve's
        # horizontal jog + vR's top edge -- moved clear below the whole zone
        # ([LAYOUT] flagged 4 overlaps against that Line/VMobject cluster).
        lblR = Text("Double-pump (hi-lo)", font_size=12, color=GRAYTXT).move_to([3.8, -2.55, 0])
        zoneR = VGroup(pumpHi, pumpLo, lblHi, lblLo, unload, lineHi, lineLo, lineJoin, vR,
                       lineToValve, cylR, pipeR_A, tankUL, drainUL, lblR)

        self.play(FadeIn(zoneR, shift=UP * 0.4), run_time=1.0)
        cap2 = caption_top("ขวา: อีกทางเลือก — ปั๊ม 2 ตัววิ่งพร้อมกันตอนความดันต่ำ (เร็ว เพราะ flow รวมมาก)")
        self.play(FadeIn(cap2), run_time=0.7)
        dotsR, animsR = flow_dots([pHi["b"], unload_p["top"], unload_p["bottom"],
                                   [3.0, 1.3, 0], junction, pvR["P"]], HI_FLOW, n=3, run_time=1.6)
        dotsR2, animsR2 = flow_dots([pLo["b"], junction, pvR["P"]], SUPPLY, n=2, run_time=1.4)
        self.play(LaggedStart(*animsR, *animsR2, lag_ratio=0.2))
        self.play(FadeOut(dotsR), FadeOut(dotsR2), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("พอความดันขึ้น (ชนงาน/เจาะจริง) — unloading valve ตัด pump ตัว hi-flow ออกอัตโนมัติ")
        self.play(FadeIn(cap3), run_time=0.8)
        dotsCut, animsCut = flow_dots([pHi["b"], unload_p["top"], unload_p["left"], tpUL["top"]],
                                      WARN, n=3, run_time=1.3)
        dotsLo2, animsLo2 = flow_dots([pLo["b"], junction, pvR["P"]], SUPPLY, n=2, run_time=1.3)
        self.play(LaggedStart(*animsCut, *animsLo2, lag_ratio=0.2))
        self.play(FadeOut(dotsCut), FadeOut(dotsLo2), run_time=0.3)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("เหลือแค่ pump lo-flow ทำงานต่อ — ไม่ต้องฝืนปั๊มใหญ่ดันความดันสูง = ประหยัดพลังงาน")
        self.play(FadeIn(cap4), run_time=0.8)
        self.wait(1.7)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC07 — page 6: Counterbalance Valve Application (vertical lift)
# =====================================================================

class HC07_CounterbalanceApplication(SafeScene):
    """Page 6 — Counterbalance Valve Application: vertical cylinder lifting
    a load, 4-way/3-position valve, counterbalance valve sits between the
    valve and the cylinder's LOWER (rod-end) port with a pilot line tapped
    from the UPPER (cap-end) line — free flow up through its internal check,
    but flow down must push through the back-pressure setting, so the load
    can't free-fall when the main valve is centered. Directly reuses
    HV20_Counterbalance's own already-verified cap-end(top,direct)/
    rod-end(bottom,via-valve) topology (that scene's docstring cites the
    book's p.20 symbol + powermotiontech — this page is that exact valve
    applied to a real cylinder, per the note: 'ทฤษฎีจาก W06 หน้า 20')."""

    def construct(self):
        # shortened from "Counterbalance Valve Application" (33 chars) --
        # confirmed via zoomed frame at native 1080p that it ran into
        # page_ref's corner badge (skill sec.20: long titles + page_ref
        # collide; the automated [LAYOUT] linter missed this one, caught
        # by Gemini review + manual pixel zoom instead).
        ttl = title("Counterbalance Valve")
        pref = page_ref("หน้า 6 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        v, pv = dcv_box([-1.6, 1.3, 0], w=1.4, h=0.85, ways=4)
        cyl, pc = cylinder_vertical([2.8, -0.2, 0], h=1.6, w=0.55)
        cb, cbp = pc_valve_box([0.7, -1.3, 0], kind="counterbalance")

        cap_line = pipe(elbow_pts(pv["A"], pc["cap"], via="y", frac=0.75))
        rod_line1 = pipe(elbow_pts(pv["B"], cbp["left"], via="y", frac=0.4))
        rod_line2 = pipe(elbow_pts(cbp["right"], pc["rod"], via="x"))
        pilot_tap_pt = np.array([0.7, pv["A"][1] - 0.15, 0])
        pilot_line = DashedLine(pilot_tap_pt, cbp["top"], color=PILOT, stroke_width=2.5, dash_length=0.08)
        pilot_tap_dot = Dot(pilot_tap_pt, radius=0.05, color=PILOT)

        grp = VGroup(v, cyl, cb, cap_line, rod_line1, rod_line2, pilot_line, pilot_tap_dot)
        self.play(FadeIn(grp, shift=UP * 0.4), run_time=1.1)

        cap0 = caption_top("โหลดแขวนอยู่ที่ก้านสูบ — กันไม่ให้ไหลตกเองตอนวาล์วหลักอยู่ตำแหน่งกลาง")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(cap0), run_time=0.3)

        cap1 = caption_top("ยก (retract): น้ำมันเข้า rod-end ผ่าน check ในตัว counterbalance ได้อิสระ")
        self.play(FadeIn(cap1), run_time=0.7)
        dots1, anims1 = flow_dots([pv["B"], cbp["left"], cbp["right"], pc["rod"]], SUPPLY, n=3, run_time=1.5)
        self.play(LaggedStart(*anims1, lag_ratio=0.25))
        self.play(FadeOut(dots1), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("ลง (extend): ปั๊มดันเข้า cap-end (บน) — แรงดันนี้แยกไปตามเส้นไพลอต (สีส้ม)")
        self.play(FadeIn(cap2), run_time=0.7)
        dots2, anims2 = flow_dots([pv["A"], pc["cap"]], SUPPLY, n=2, run_time=1.0)
        dots2p, anims2p = flow_dots([pilot_tap_pt, cbp["top"]], PILOT, n=2, run_time=1.0)
        self.play(LaggedStart(*anims2, *anims2p, lag_ratio=0.25))
        self.play(FadeOut(dots2), FadeOut(dots2p), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("ไพลอตชนะสปริง เปิด throttle — น้ำมัน rod-end ไหลออกได้แบบมีแรงต้าน (คุมความเร็วลง)")
        self.play(FadeIn(cap3), run_time=0.8)
        dots3, anims3 = flow_dots([pc["rod"], cbp["right"], cbp["left"], pv["B"]], WARN, n=3, run_time=1.8)
        self.play(LaggedStart(*anims3, lag_ratio=0.25))
        self.play(FadeOut(dots3), run_time=0.3)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("ไม่มีสัญญาณไพลอต = throttle ปิดสนิท — โหลดถูกล็อกค้าง ไม่ไหลตกเองตอนวาล์วอยู่กลาง")
        self.play(FadeIn(cap4), run_time=0.8)
        self.wait(1.8)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC08 — page 7: Cylinder Locking using Pilot Check Valve
# =====================================================================

class HC08_CylinderLocking(SafeScene):
    """Page 7 — Cylinder Locking using Pilot Check Valve: a PAIR of
    pilot-operated check valves, one on each side of the cylinder, blocks
    the cylinder from drifting when the main valve is centered (even if the
    main valve leaks internally) — a pilot signal from the OPPOSITE line
    forces the needed direction open on command. Verified against the note's
    own text ('สัญญาณไพลอตจากฝั่งตรงข้ามจะบังคับเปิด')."""

    def construct(self):
        ttl = title("Cylinder Locking (Pilot Check)")
        pref = page_ref("หน้า 7 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        v, pv = dcv_box([0, 1.6, 0], w=1.4, h=0.85, ways=4)
        cyl, pc = cylinder_double([0, -1.3, 0], w=3.0, h=0.55)
        pcvL, portsL = pilot_check_valve_symbol([-1.7, -0.1, 0], angle=0, pilot_angle=-PI / 2)
        pcvR, portsR = pilot_check_valve_symbol([1.7, -0.1, 0], angle=PI, pilot_angle=-PI / 2)

        # frac lowered 0.6->0.35: A and P share the valve's left-side x
        # (same for B/T on the right), so the old mid_y=0.6 jog dropped the
        # vertical leg straight through P's/T's own port-glyph label before
        # turning sideways ([LAYOUT] caught this on the draft render).
        # frac=0.35 keeps the horizontal jog above the P/T label band.
        lineA1 = pipe(elbow_pts(pv["A"], portsL["in"], via="y", frac=0.35))
        lineA2 = pipe(elbow_pts(portsL["out"], pc["he"], via="y", frac=0.5))
        lineB1 = pipe(elbow_pts(pv["B"], portsR["in"], via="y", frac=0.35))
        lineB2 = pipe(elbow_pts(portsR["out"], pc["re"], via="y", frac=0.5))
        # cross-pilot: left valve's pilot comes from the RIGHT (RE) line;
        # right valve's pilot comes from the LEFT (HE) line
        pilotL = DashedLine(portsL["pilot"], [portsL["pilot"][0], -1.05, 0], color=PILOT, stroke_width=2.5, dash_length=0.07)
        pilotL2 = DashedLine([portsL["pilot"][0], -1.05, 0], [1.7, -1.05, 0], color=PILOT, stroke_width=2.5, dash_length=0.07)
        pilotL3 = DashedLine([1.7, -1.05, 0], portsR["out"] + np.array([0, -0.15, 0]), color=PILOT, stroke_width=2.5, dash_length=0.07)
        pilotR = DashedLine(portsR["pilot"], [portsR["pilot"][0], -1.15, 0], color=PILOT, stroke_width=2.5, dash_length=0.07)
        pilotR2 = DashedLine([portsR["pilot"][0], -1.15, 0], [-1.7, -1.15, 0], color=PILOT, stroke_width=2.5, dash_length=0.07)
        pilotR3 = DashedLine([-1.7, -1.15, 0], portsL["out"] + np.array([0, -0.25, 0]), color=PILOT, stroke_width=2.5, dash_length=0.07)

        grp = VGroup(v, cyl, pcvL, pcvR, lineA1, lineA2, lineB1, lineB2)
        self.play(FadeIn(grp, shift=UP * 0.4), run_time=1.1)
        cap0 = caption_top("pilot check valve คู่หนึ่ง ติดตั้งคนละฝั่งกระบอกสูบ — ปกติกันไหลย้อนสนิททั้ง 2 ทิศ")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.3)
        self.play(FadeOut(cap0), run_time=0.3)

        cap1 = caption_top("วาล์วหลักอยู่กลาง (หรือรั่วภายใน) — check ทั้งคู่ปิดกั้นไว้ กระบอกสูบไม่ขยับ")
        self.play(FadeIn(cap1), run_time=0.7)
        blockL = blocked_mark(portsL["out"])
        blockR = blocked_mark(portsR["out"])
        self.play(FadeIn(blockL), FadeIn(blockR), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(cap1), FadeOut(blockL), FadeOut(blockR), run_time=0.4)

        cap2 = caption_top("สั่งยืดออก: P→A ปกติ + สัญญาณไพลอต (จากฝั่ง B) บังคับเปิด check ฝั่งซ้าย")
        self.play(FadeIn(cap2), run_time=0.8)
        self.play(Create(pilotL), Create(pilotL2), Create(pilotL3), run_time=0.9)
        dotsA, animsA = flow_dots([pv["A"], portsL["in"], portsL["out"], pc["he"]], SUPPLY, n=3, run_time=1.4)
        self.play(LaggedStart(*animsA, lag_ratio=0.25))
        self.play(FadeOut(dotsA), FadeOut(pilotL), FadeOut(pilotL2), FadeOut(pilotL3), run_time=0.4)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("สั่งหดกลับ: P→B ปกติ + สัญญาณไพลอต (จากฝั่ง A) บังคับเปิด check ฝั่งขวา")
        self.play(FadeIn(cap3), run_time=0.8)
        self.play(Create(pilotR), Create(pilotR2), Create(pilotR3), run_time=0.9)
        dotsB, animsB = flow_dots([pv["B"], portsR["in"], portsR["out"], pc["re"]], SUPPLY, n=3, run_time=1.4)
        self.play(LaggedStart(*animsB, lag_ratio=0.25))
        self.play(FadeOut(dotsB), FadeOut(pilotR), FadeOut(pilotR2), FadeOut(pilotR3), run_time=0.4)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("ล็อกแน่นกว่า pilot check เดี่ยว — ใช้ตอนต้องรับโหลดค้างไว้เฉยๆ ปลอดภัยแม้วาล์วรั่ว")
        self.play(FadeIn(cap4), run_time=0.8)
        self.wait(1.7)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC09 — page 8: Cylinder Reciprocating Circuit
# =====================================================================

class HC09_ReciprocatingCircuit(SafeScene):
    """Page 8 — Cylinder Reciprocating Circuit: cylinder runs back and forth
    automatically — limit valves/pilot signals at both ends of the stroke
    flip the main valve every time the cylinder bottoms out, no operator
    needed; paired relief valves guard both directions (per note text)."""

    def construct(self):
        ttl = title("Cylinder Reciprocating Circuit")
        pref = page_ref("หน้า 8 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        v, pv = dcv_box([0, 1.4, 0], w=1.5, h=0.85, ways=4)
        cyl, pc = cylinder_double([0, -1.2, 0], w=3.6, h=0.55, piston_frac=0.15, rod_len=0.5)
        piston = pc["piston"]
        reliefP, rpP = pc_valve_box([-2.4, 0.5, 0], kind="relief")
        reliefT, rpT = pc_valve_box([2.4, 0.5, 0], kind="relief")
        # The actual [LAYOUT] culprit (not pipeA/pipeB below): these two
        # connectors' final approach leg runs vertically straight into P/T
        # at their own x -- default frac=0.5 put that leg's lower end right
        # in the P/T port-glyph label's zone. frac near the PORT end (0.9
        # for lineP since its 2nd point is P; 0.1 for lineT since its 1st
        # point is T) shrinks that leg so it stays above the label band.
        lineP = pipe(elbow_pts(rpP["right"], pv["P"], via="y", frac=0.9))
        lineT = pipe(elbow_pts(pv["T"], rpT["left"], via="y", frac=0.1))
        # frac lowered (0.7/0.55 -> 0.25): same P/T-label-crossing bug as
        # HC08's lineA1/lineB1 -- A and P (B and T) share x, old fracs
        # dropped the vertical leg through P's/T's port-glyph label.
        pipeA = pipe(elbow_pts(pv["A"], pc["he"], via="y", frac=0.25))
        pipeB = pipe(elbow_pts(pv["B"], pc["re"], via="y", frac=0.25))

        limL = Triangle(color=WARN, fill_color=WARN, fill_opacity=1, stroke_width=0)
        limL.scale(0.1).rotate(PI / 2).move_to([-1.7, -1.5, 0])
        limR = Triangle(color=WARN, fill_color=WARN, fill_opacity=1, stroke_width=0)
        limR.scale(0.1).rotate(-PI / 2).move_to([1.7, -1.5, 0])
        pilotEndL = Rectangle(width=0.26, height=0.26, color=PILOT, fill_color=PILOT,
                              fill_opacity=0.4, stroke_width=2).move_to([-2.7, 1.4, 0])
        pilotEndR = Rectangle(width=0.26, height=0.26, color=PILOT, fill_color=PILOT,
                              fill_opacity=0.4, stroke_width=2).move_to([2.7, 1.4, 0])
        pilotWireL = DashedLine([-1.7, -1.65, 0], [-2.7, 1.27, 0], color=PILOT, stroke_width=2, dash_length=0.08)
        pilotWireR = DashedLine([1.7, -1.65, 0], [2.7, 1.27, 0], color=PILOT, stroke_width=2, dash_length=0.08)

        grp = VGroup(v, cyl, reliefP, reliefT, lineP, lineT, pipeA, pipeB,
                     limL, limR, pilotEndL, pilotEndR)
        self.play(FadeIn(grp, shift=UP * 0.4), run_time=1.1)

        cap0 = caption_top("limit valve/pilot ที่ปลายช่วงชักทั้ง 2 ข้าง สั่งสลับวาล์วเองทุกครั้งที่ชนสุดทาง")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(cap0), run_time=0.3)

        cap1 = caption_top("ยืดออก: P→A จนลูกสูบชนปลายขวา — trip limit ขวา ส่งไพลอตสลับวาล์วเอง")
        self.play(FadeIn(cap1), run_time=0.7)
        dotsA, animsA = flow_dots([pv["A"], pc["he"]], SUPPLY, n=2, run_time=1.0)
        self.play(LaggedStart(*animsA, lag_ratio=0.3), piston.animate.move_to([1.35, -1.2, 0]),
                  run_time=2.0, rate_func=linear)
        self.play(FadeOut(dotsA), run_time=0.2)
        self.play(Indicate(limR, color=WARN, scale_factor=1.8), Create(pilotWireR), run_time=0.6)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("วาล์วสลับอัตโนมัติ: P→B แทน — ลูกสูบวิ่งกลับ จนชนปลายซ้าย สลับอีกครั้ง")
        self.play(FadeIn(cap2), run_time=0.7)
        dotsB, animsB = flow_dots([pv["B"], pc["re"]], SUPPLY, n=2, run_time=1.0)
        self.play(LaggedStart(*animsB, lag_ratio=0.3), piston.animate.move_to([-1.35, -1.2, 0]),
                  run_time=2.0, rate_func=linear)
        self.play(FadeOut(dotsB), run_time=0.2)
        self.play(Indicate(limL, color=WARN, scale_factor=1.8), Create(pilotWireL), run_time=0.6)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("วนซ้ำแบบนี้ไปเรื่อยๆ โดยไม่ต้องมีคนคอยสลับ — relief คู่ป้องกันความดันเกินทั้ง 2 ทิศ")
        self.play(FadeIn(cap3), run_time=0.8)
        self.wait(1.8)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC10 — page 9: Cylinder Sequencing Circuit
# =====================================================================

class HC10_SequencingCircuit(SafeScene):
    """Page 9 — Cylinder Sequencing Circuit: forces cylinder 1 to fully
    finish before cylinder 2 starts. Topology follows HV19_SequenceValve's
    own already-verified T-body model (primary flows straight through
    unrestricted to cylinder 1, secondary branches off through the
    spring-loaded poppet to cylinder 2 — the SAME supply-line pressure,
    not a signal from cylinder 1's output) — oil takes the lower-resistance
    path into cylinder 1 first; once cylinder 1 bottoms out, pressure rises
    (nowhere else to go) to the sequence valve's setting and opens flow to
    cylinder 2."""

    def construct(self):
        ttl = title("Cylinder Sequencing Circuit")
        pref = page_ref("หน้า 9 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        v, pv = dcv_box([-4.2, 1.3, 0], w=1.4, h=0.85, ways=4)
        cyl1, pc1 = cylinder_double([-2.2, -1.0, 0], w=1.6, h=0.5)
        seq, seqp = pc_valve_box([0.4, -1.0, 0], kind="sequence")
        cyl2, pc2 = cylinder_double([3.0, -1.0, 0], w=1.6, h=0.5, tint=CYL2)
        t_junction = np.array([-1.0, -1.0, 0])

        lineMain = pipe(elbow_pts(pv["A"], t_junction, via="y", frac=0.6))
        line1 = pipe([t_junction, pc1["he"]])
        line2a = pipe([t_junction, seqp["left"]])
        line2b = pipe([seqp["right"], pc2["he"]])
        retLine = pipe(elbow_pts(pc1["re"], pv["B"], via="y", frac=0.3))
        retLine2 = pipe(elbow_pts(pc2["re"], pv["B"], via="y", frac=0.15))

        lbl1 = Text("Cylinder 1", font_size=13, color=GRAYTXT).move_to([-2.2, -1.75, 0])
        lbl2 = Text("Cylinder 2", font_size=13, color=CYL2).move_to([3.0, -1.75, 0])

        grp = VGroup(v, cyl1, seq, cyl2, lineMain, line1, line2a, line2b, retLine, retLine2, lbl1, lbl2)
        self.play(FadeIn(grp, shift=UP * 0.4), run_time=1.1)

        cap0 = caption_top("sequence valve คั่นก่อนกระบอกสูบตัวที่ 2 — บังคับให้ตัวที่ 1 เสร็จก่อนเสมอ")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(cap0), run_time=0.3)

        block_mark = blocked_mark(seqp["right"])
        cap1 = caption_top("แรงดันยังต่ำ (cyl1 กำลังวิ่ง): น้ำมันเลือกทางต้านน้อยกว่า — ไหลเข้า cyl1 อย่างเดียว")
        self.play(FadeIn(cap1), run_time=0.7)
        self.play(FadeIn(block_mark), run_time=0.3)
        dots1, anims1 = flow_dots([pv["A"], t_junction, pc1["he"]], SUPPLY, n=3, run_time=1.4)
        self.play(LaggedStart(*anims1, lag_ratio=0.25))
        self.play(FadeOut(dots1), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("cyl1 ชนสุดทาง — ไม่มีทางไปต่อ ความดันพุ่งขึ้นถึงค่าตั้งของ sequence valve")
        self.play(FadeIn(cap2), run_time=0.8)
        self.play(Indicate(pc1["piston"], color=WARN, scale_factor=1.15), run_time=0.8)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("sequence valve เปิด — เปิดให้ไหลต่อไปยัง cyl2 ได้ในที่สุด")
        self.play(FadeIn(cap3), run_time=0.7)
        self.play(FadeOut(block_mark), run_time=0.2)
        dots2, anims2 = flow_dots([t_junction, seqp["left"], seqp["right"], pc2["he"]], CYL2, n=3, run_time=1.6)
        self.play(LaggedStart(*anims2, lag_ratio=0.25))
        self.play(FadeOut(dots2), run_time=0.3)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("ลำดับถูกบังคับด้วยความดัน ไม่ใช่เวลา — ต่างจาก tandem/series ที่ไหลพร้อมกันตรงนี้เอง")
        self.play(FadeIn(cap4), run_time=0.8)
        self.wait(1.7)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC11 — page 10: Double-Cylinder Open Tandem Center Circuit
# =====================================================================

class HC11_TandemCenter(SafeScene):
    """Page 10 — Double-Cylinder Open Tandem Center Circuit: two valves in
    series on ONE pump line. If the first valve (closer to the pump) is
    centered, tandem-center lets flow pass through it freely to the second
    valve (independent operation, sharing one pump); closed-center would
    block flow to the second valve entirely. Contrast shown via Transform
    of the SAME internal-path mobject (skill §25 — same idea evolving)."""

    def construct(self):
        ttl = title("Tandem Center Circuit")
        pref = page_ref("หน้า 10 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        v1, pv1 = dcv_box([-3.0, 0.8, 0], w=1.4, h=0.85, ways=4)
        cyl1, pc1 = cylinder_double([-3.0, -1.4, 0], w=1.6, h=0.5)
        v2, pv2 = dcv_box([2.6, 0.8, 0], w=1.4, h=0.85, ways=4)
        cyl2, pc2 = cylinder_double([2.6, -1.4, 0], w=1.6, h=0.5, tint=CYL2)

        pass_line = pipe(elbow_pts(pv1["T"], pv2["P"], via="y", frac=0.5))
        pipeA1 = pipe(elbow_pts(pv1["A"], pc1["he"], via="y", frac=0.6))
        pipeB1 = pipe(elbow_pts(pv1["B"], pc1["re"], via="y", frac=0.45))
        pipeA2 = pipe(elbow_pts(pv2["A"], pc2["he"], via="y", frac=0.6))
        pipeB2 = pipe(elbow_pts(pv2["B"], pc2["re"], via="y", frac=0.45))
        # shifted left of straight-down from P: the flow-dots path below
        # starts directly under P, and a bare next_to(DOWN) put this label
        # right in that path's way ([LAYOUT] caught it against both the
        # static stub and the moving flow dots on the draft render).
        lbl_pump = Text("จากปั๊ม", font_size=13, color=SUPPLY).next_to(pv1["P"], DOWN, buff=0.22).shift(LEFT * 0.5)
        lbl_tank = Text("กลับถัง", font_size=13, color=RETURN).next_to(pv2["T"], DOWN, buff=0.22)
        lbl_v1 = Text("วาล์ว 1 (ใกล้ปั๊ม)", font_size=12, color=GRAYTXT).next_to(v1, UP, buff=0.15)
        lbl_v2 = Text("วาล์ว 2", font_size=12, color=GRAYTXT).next_to(v2, UP, buff=0.15)

        grp = VGroup(v1, cyl1, v2, cyl2, pipeA1, pipeB1, pipeA2, pipeB2, pass_line,
                     lbl_pump, lbl_tank, lbl_v1, lbl_v2)
        self.play(FadeIn(grp, shift=UP * 0.4), run_time=1.1)

        cap0 = caption_top("2 วาล์วต่ออนุกรมบนสายปั๊มเดียว — วาล์วตัวแรกอยู่ใกล้ปั๊มสุด")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.1)
        self.play(FadeOut(cap0), run_time=0.3)

        path_tandem = dcv_path(pv1, [("P", "T", SUPPLY)])
        cap1 = caption_top("Tandem center: วาล์ว 1 อยู่กลาง — P ไหลผ่านตรงไปหาวาล์ว 2 ได้ฟรี")
        self.play(FadeIn(cap1), run_time=0.7)
        self.play(Create(path_tandem), run_time=0.6)
        # A straight vertical approach from below P still transits P's own
        # port-glyph label (a small y-nudge on the P waypoint doesn't help
        # -- the SEGMENT from below still crosses through the label's zone
        # on the way up). Jog sideways (x+0.3) while below/level with the
        # label, THEN rise, THEN jog back onto the port from above --
        # this never puts the path inside the label's x-column while its
        # y is anywhere near the label's height.
        p1_lo = pv1["P"] + np.array([0.3, -0.3, 0])
        p1_hi = pv1["P"] + np.array([0.3, 0.15, 0])
        p1_in = pv1["P"] + np.array([0, 0.15, 0])
        dots1, anims1 = flow_dots([p1_lo, p1_hi, p1_in, pv1["T"], pv2["P"]],
                                  SUPPLY, n=3, run_time=1.6)
        self.play(LaggedStart(*anims1, lag_ratio=0.25))
        self.play(FadeOut(dots1), run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("ผลคือ 2 กระบอกสูบทำงานอิสระต่อกัน แต่ใช้ปั๊มตัวเดียวร่วมกัน — ไม่ต้องมี 2 ปั๊ม")
        self.play(FadeIn(cap2), run_time=0.8)
        # a 0.15 nudge above P still measured a residual overlap on the
        # previous render (label bbox likely taller than assumed) --
        # doubled to 0.3 for real margin.
        dots2, anims2 = flow_dots([pv2["P"] + np.array([0, 0.3, 0]), pv2["A"], pc2["he"]],
                                  SUPPLY, n=3, run_time=1.3)
        self.play(LaggedStart(*anims2, lag_ratio=0.25))
        self.play(FadeOut(dots2), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("ถ้าใช้ closed center แทน — สปูลตัดขาดทุกพอร์ตตอนอยู่กลาง")
        self.play(FadeIn(cap3), run_time=0.7)
        self.play(Transform(path_tandem, dcv_path(pv1, [])), run_time=0.9)
        block1 = blocked_mark(pv1["P"])
        block2 = blocked_mark(pv1["T"])
        self.play(FadeIn(block1), FadeIn(block2), run_time=0.4)
        self.wait(0.4)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("...flow ถูกบล็อกตั้งแต่วาล์ว 1 ทันที — ไปไม่ถึงวาล์ว 2 เลย ต่างจาก tandem ชัดเจน")
        self.play(FadeIn(cap4), run_time=0.8)
        # same sideways-jog fix as anims1 above (straight vertical approach
        # from below still transits P's label zone) -- dot still ends up
        # right at/on block1's X mark, just approached from the side.
        dotsX, animsX = flow_dots([p1_lo, p1_hi, p1_in], BLOCKED, n=2, run_time=0.8)
        self.play(LaggedStart(*animsX, lag_ratio=0.3))
        self.play(FadeOut(dotsX), run_time=0.3)
        self.wait(1.3)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC12 — page 14: Motor Control
# =====================================================================

class HC12_MotorControl(SafeScene):
    """Page 14 — Motor Control: two ways to control a hydraulic motor's
    speed/direction. (TOP) adjustable flow-control valve with a reverse-
    direction check-valve bypass — one-way speed control (reuses HV23's own
    verified needle+check layout, relabeled for a motor). (BOTTOM) a
    4-check-valve bridge circuit (hydraulic 'rectifier', verified real —
    powermotiontech.com 'Bridge Circuit Provides One-Way Flow', 2026-09-04)
    that makes the motor always spin the SAME direction regardless of which
    way the main valve routes flow, with a flow-control valve in the shared
    output path."""

    def construct(self):
        ttl = title("Motor Control")
        pref = page_ref("หน้า 14 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        # ---- TOP: one-way flow control + check bypass ---------------------
        vT, pvT = dcv_box([-4.4, 1.3, 0], w=1.2, h=0.7, ways=4)
        fcvT, fcvTp = pc_valve_box([-1.8, 1.3, 0], kind="flowcontrol")
        chkT, chkTp = check_valve_symbol([-1.8, 1.85, 0], angle=0, size=0.3)
        motorT, mpT = rotor_symbol([0.7, 1.3, 0], angle=0, r=0.32, color=OK, filled=False)
        # frac raised 0.5->0.9: the default mid_y sat only ~0.065 below vT's
        # own top edge, so the horizontal jog visually hugged/rode the box's
        # top border instead of reading as a clean internal path (caught by
        # Gemini review + confirmed by zooming the native-1080p frame).
        # frac=0.9 pulls that jog down near the box's vertical center.
        lineT1 = pipe(elbow_pts(pvT["A"], fcvTp["left"], via="y", frac=0.9))
        lineT2 = pipe([fcvTp["right"], mpT["a"]])
        bypass1 = pipe(elbow_pts(fcvTp["left"], chkTp["in"], via="y"))
        bypass2 = pipe(elbow_pts(chkTp["out"], fcvTp["right"], via="y"))
        # shifted right 0.3 (was centered at -1.7): its left edge crept to
        # within a few pixels of vT's own "T" port-glyph label -- confirmed
        # by zooming the native-1080p frame (Gemini also flagged this).
        lblT = Text("บน: FCV ปรับได้ + check bypass — ปรับความเร็วได้ทางเดียว",
                    font_size=13, color=GRAYTXT).move_to([-1.4, 0.55, 0])
        zoneT = VGroup(vT, fcvT, chkT, motorT, lineT1, lineT2, bypass1, bypass2, lblT)

        # ---- BOTTOM: 4-check bridge — motor spins one direction always ----
        vB, pvB = dcv_box([-4.4, -1.75, 0], w=1.2, h=0.7, ways=4)
        bridge, bnode = bridge_rectifier([-1.8, -1.75, 0], size=1.1)
        fcvB, fcvBp = pc_valve_box([0.2, -1.75, 0], kind="flowcontrol")
        motorB, mpB = rotor_symbol([2.6, -1.75, 0], angle=0, r=0.32, color=OK, filled=False)
        # same top-edge-hugging fix as lineT1 above (default frac=0.5 put
        # the jog ~0.015 below vB's top edge -- even tighter).
        lineB1 = pipe(elbow_pts(pvB["A"], bnode["left"], via="y", frac=0.9))
        lineB2 = pipe(elbow_pts(pvB["B"], bnode["right"], via="y", frac=0.9))
        lineB3 = pipe([bnode["top"], fcvBp["left"]])
        lineB4 = pipe([fcvBp["right"], mpB["a"]])
        lineB5 = pipe(elbow_pts(mpB["b"], bnode["bot"], via="y"))
        rot_arrow = Arc(radius=0.48, start_angle=PI * 0.2, angle=PI * 1.2,
                        arc_center=[2.6, -1.75, 0], color=OK, stroke_width=3)
        rot_arrow.add_tip(tip_length=0.12, tip_width=0.1)
        lblB = Text("ล่าง: สะพาน 4 check valve — มอเตอร์หมุนทิศเดียวเสมอ",
                    font_size=13, color=GRAYTXT).move_to([-1.7, -3.15, 0])
        zoneB = VGroup(vB, bridge, fcvB, motorB, lineB1, lineB2, lineB3, lineB4, lineB5, lblB)

        divider = DashedLine([-6.9, -0.35, 0], [6.9, -0.35, 0], color=GRAYTXT, stroke_width=1.5, dash_length=0.15)
        self.play(FadeIn(zoneT, shift=UP * 0.4), run_time=1.0)
        self.play(Create(divider), run_time=0.5)
        self.play(FadeIn(zoneB, shift=UP * 0.4), run_time=1.0)

        cap1 = caption_top("บน: ปรับความเร็วได้ทางเดียว — อีกทางไหลอิสระผ่าน check bypass เต็มที่")
        self.play(FadeIn(cap1), run_time=0.7)
        dotsT, animsT = flow_dots([pvT["A"], fcvTp["left"], fcvTp["right"], mpT["a"]], SUPPLY, n=3, run_time=1.5)
        self.play(LaggedStart(*animsT, lag_ratio=0.25))
        self.play(FadeOut(dotsT), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("ล่าง: วาล์วสั่ง P→A — สะพานส่งน้ำมันเข้ามอเตอร์จากขั้วบนเสมอ (หมุนตามลูกศร)")
        self.play(FadeIn(cap2), run_time=0.8)
        dotsB1, animsB1 = flow_dots([pvB["A"], bnode["left"], bnode["top"], fcvBp["left"],
                                    fcvBp["right"], mpB["a"]], SUPPLY, n=4, run_time=1.8)
        self.play(LaggedStart(*animsB1, lag_ratio=0.2), Create(rot_arrow))
        self.play(FadeOut(dotsB1), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        cap3 = caption_top("สลับวาล์ว: P→B แทน — สะพานยังส่งน้ำมันเข้ามอเตอร์จากขั้วบนเดิม หมุน 'ทิศเดิม' ไม่เปลี่ยน")
        self.play(FadeIn(cap3), run_time=0.8)
        dotsB2, animsB2 = flow_dots([pvB["B"], bnode["right"], bnode["top"], fcvBp["left"],
                                    fcvBp["right"], mpB["a"]], SUPPLY, n=4, run_time=1.8)
        self.play(LaggedStart(*animsB2, lag_ratio=0.2))
        self.play(FadeOut(dotsB2), run_time=0.3)
        self.play(FadeOut(cap3), run_time=0.3)

        cap4 = caption_top("นี่คือ 'วงจรเรียงกระแส' แบบไฮดรอลิก — คล้ายวงจร rectifier ในไฟฟ้าเป๊ะ")
        self.play(FadeIn(cap4), run_time=0.8)
        self.wait(1.7)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# HC13 — page 15: Hydrostatic Transmission
# =====================================================================

class HC13_HydrostaticTransmission(SafeScene):
    """Page 15 — Hydrostatic Transmission: electric motor drives a
    reversible variable-displacement pump, driving a fixed-displacement
    motor in a CLOSED loop (oil circulates pump<->motor, not through the
    main tank every cycle). Built left-to-right per skill §23 (trace the
    conserved quantity — mechanical power in, hydraulic power through the
    loop, mechanical power out — stage by stage through each component).
    Required extras, all verified 2026-09-04 against patent literature
    (US4185521 family, 'closed loop control for hydrostatic transmission'):
    a replenishing pump feeding the loop through TWO check valves (one per
    loop line — each opens only when its own line is the low side, so the
    pump 'automatically picks whichever side is low pressure'), a
    replenishing relief valve, and a PAIR of overload relief valves
    (protecting both directions, since the pump can reverse)."""

    def construct(self):
        ttl = title("Hydrostatic Transmission")
        pref = page_ref("หน้า 15 · Hydraulic Circuit Design")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        elecM, ep = rotor_symbol([-5.6, 0.3, 0], angle=PI / 2, r=0.3, color=GRAYTXT, filled=True)
        elecM_lbl = Text("M (มอเตอร์ไฟฟ้า)", font_size=13, color=WHITE).move_to([-5.6, 1.25, 0])
        pump, pp = rotor_symbol([-3.2, 0.3, 0], angle=PI / 2, r=0.4, color=SUPPLY, bidir=True)
        slash = variable_slash([-3.2, 0.3, 0])
        motor, mp = rotor_symbol([1.6, 0.3, 0], angle=PI / 2, r=0.4, color=OK, filled=False)
        shaft = Line([-5.3, 0.3, 0], [-3.6, 0.3, 0], color=METAL, stroke_width=5)

        top_line = pipe([pp["b"], mp["b"]], width=3)
        bot_line = pipe([pp["a"], mp["a"]], width=3)

        # both relief valves dropped 0.15 lower (0.3 -> 0.15): at the
        # original height their spring_zigzag's own top edge (cy+h/2+0.09+
        # amp = 0.705) sat almost exactly ON the pump-motor header line
        # (y=0.7) -- Gemini review + a native-1080p zoom confirmed the
        # spring visibly crossed the header. 0.15 lower clears it with a
        # real gap. Bottom stub + label shifted down to match.
        relief1, r1p = pc_valve_box([-2.3, 0.15, 0], kind="relief", label=False)
        relief1_top = pipe([[-2.3, 0.7, 0], r1p["top"]])
        relief1_bot = pipe([r1p["bottom"], [-2.3, -0.25, 0]])
        relief1_lbl = Text("Overload", font_size=11, color=GRAYTXT).move_to([-2.3, -1.0, 0])
        relief2, r2p = pc_valve_box([0.6, 0.15, 0], kind="relief", label=False)
        relief2_top = pipe([[0.6, 0.7, 0], r2p["top"]])
        relief2_bot = pipe([r2p["bottom"], [0.6, -0.25, 0]])
        relief2_lbl = Text("Overload", font_size=11, color=GRAYTXT).move_to([0.6, -1.0, 0])

        rep_pump, repp = rotor_symbol([-0.9, -2.5, 0], angle=PI / 2, r=0.26, color=SUPPLY, filled=True)
        rep_lbl = Text("Replenishing pump", font_size=11, color=GRAYTXT).move_to([-0.9, -2.85, 0])
        chkA, chkAp = check_valve_symbol([-1.6, -1.6, 0], angle=PI / 2, size=0.26)
        chkB, chkBp = check_valve_symbol([-0.2, -1.6, 0], angle=PI / 2, size=0.26)
        rep_relief, rrp = pc_valve_box([-0.9, -1.6, 0], kind="relief", label=False)
        rep_relief_lbl = fit_width(Text("Repl. relief", font_size=11, color=GRAYTXT), 0.95)
        rep_relief_lbl.move_to([-0.9, -1.05, 0])
        lineRepA = pipe(elbow_pts(repp["b"], chkAp["in"], via="y"))
        lineRepA2 = pipe([chkAp["out"], [-1.6, -0.1, 0]])
        lineRepB = pipe(elbow_pts(repp["b"], chkBp["in"], via="y"))
        lineRepB2 = pipe([chkBp["out"], [-0.2, -0.1, 0]])
        lineRepR = pipe([repp["b"], rrp["bottom"]])

        pump_lbl = fit_width(Text("Reversible Variable Pump", font_size=12, color=SUPPLY), 2.6)
        pump_lbl.move_to([-3.2, 1.25, 0])
        motor_lbl = fit_width(Text("Fixed-Displacement Motor", font_size=12, color=OK), 2.6)
        motor_lbl.move_to([1.6, 1.25, 0])

        stage1 = VGroup(elecM, elecM_lbl, shaft, pump, slash)
        self.play(FadeIn(stage1, shift=RIGHT * 0.4), run_time=1.0)
        cap0 = caption_top("ไล่กำลังทีละช่วง: มอเตอร์ไฟฟ้าขับปั๊ม reversible variable displacement")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.1)
        self.play(FadeOut(cap0), run_time=0.3)

        stage2 = VGroup(top_line, bot_line, motor, pump_lbl, motor_lbl)
        self.play(FadeIn(stage2, shift=RIGHT * 0.4), run_time=1.0)
        cap1 = caption_top("ปั๊มส่งกำลังผ่านน้ำมันในวงปิด (closed loop) ไปขับมอเตอร์ fixed displacement โดยตรง")
        self.play(FadeIn(cap1), run_time=0.7)
        dots1, anims1 = flow_dots([pp["b"], mp["b"]], SUPPLY, n=3, run_time=1.4)
        self.play(LaggedStart(*anims1, lag_ratio=0.25))
        self.play(FadeOut(dots1), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("ไม่ผ่านถังหลักทุกรอบ — วนเฉพาะระหว่างปั๊มกับมอเตอร์เท่านั้น (วงปิดจริง)")
        self.play(FadeIn(cap2), run_time=0.8)
        dots2, anims2 = flow_dots([mp["a"], pp["a"]], OK, n=3, run_time=1.4)
        self.play(LaggedStart(*anims2, lag_ratio=0.25))
        self.play(FadeOut(dots2), run_time=0.3)
        self.play(FadeOut(cap2), run_time=0.3)

        stage3 = VGroup(relief1, relief1_top, relief1_bot, relief1_lbl,
                        relief2, relief2_top, relief2_bot, relief2_lbl)
        self.play(FadeIn(stage3, shift=UP * 0.3), run_time=0.9)
        cap3 = caption_top("Overload relief คู่ — ป้องกันความดันเกินได้ทั้ง 2 ทิศ เพราะปั๊มย้อนทิศได้")
        self.play(FadeIn(cap3), run_time=0.8)
        self.wait(1.3)
        self.play(FadeOut(cap3), run_time=0.3)

        stage4 = VGroup(rep_pump, rep_lbl, chkA, chkB, rep_relief, rep_relief_lbl,
                        lineRepA, lineRepA2, lineRepB, lineRepB2, lineRepR)
        self.play(FadeIn(stage4, shift=UP * 0.3), run_time=1.0)
        cap4 = caption_top("Replenishing pump เติมชดเชยน้ำมันรั่ว — check valve คู่เลือกฝั่งที่ความดันต่ำกว่าเอง")
        self.play(FadeIn(cap4), run_time=0.8)
        dots4, anims4 = flow_dots([repp["b"], chkAp["in"], chkAp["out"], [-1.5, -0.1, 0]],
                                  SUPPLY, n=2, run_time=1.3)
        self.play(LaggedStart(*anims4, lag_ratio=0.3))
        self.play(FadeOut(dots4), run_time=0.3)
        self.play(FadeOut(cap4), run_time=0.3)

        cap5 = fit_width(caption_top(
            "สรุปทั้งบท: ทุกวงจรที่เห็นมาคือวาล์วจาก W06 แค่จัดเรียงต่อกัน — ระบบนี้รวมเกือบทุกอย่างไว้ในที่เดียว"), 12.8)
        self.play(FadeIn(cap5), run_time=0.9)
        self.wait(2.0)
        self.fade_out_all(run_time=0.9)
