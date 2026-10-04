# -*- coding: utf-8 -*-
"""Q2 -- upright-printed hook: "is the pull really direct tension with no angle?"

Four scenes, one cloud render each (plan = the contract: Main_note/Claude_Specs/3DP Hook Q2 Upright Direct Tension Plan.md):
  HookQ2_A_Straight   (SafeScene,       45 s)  the straight bar: the doubter is right about a bar (sigma = F/A)
  HookQ2_B_Offset     (SafeScene,       75 s)  the J hook: the weight hangs d away from the stem -> M = F*d, inner fibre in tension
  HookQ2_C_Layers     (SafeThreeDScene, 55 s)  which way does that stress run relative to the layers (3-D, camera move)
  HookQ2_D_BaseShear  (SafeScene,       55 s)  shear at the base acts ON the layer interfaces; tension vs shear numbers; table

All Thai text comes from hook_captions.py (cap / CAPS / TABLE_Q2D); no Thai is typed here and none goes in MathTex.
Every number is the Common Spec 3.2 value (hook_common asserts them at import) and is an ASSUMED example.
Row starts are announced with self.mark(plan_seconds) and row ends pinned with self.until(plan_seconds) ([BEAT] lines).
"""
from hook_common import *
from hook_q1_flat import wall_loop, top_view_layer, inset_strands, magnifier_cone      # proven Q1 helpers, reused unchanged

# =====================================================================================================================
# shared helpers
# =====================================================================================================================
MM2 = 0.048                              # world units per mm of the flat 2-D J figure (A ghost, B)
HOOK_SCR = (-5.0, -0.45)                 # screen position of the J's bounding-box centre
ORG2 = hook_centre_origin(MM2, (HOOK_SCR[0], HOOK_SCR[1], 0.0))
BRIDGE_POS = [1.1, 0.3, 0]               # A ends with q2_a_bridge here, B starts with it (continuity)
ASSUME_Y = -3.78                         # the 'assumed example' tag line, bottom of the frame


def hp(x, y):
    """J-profile mm -> screen point for the figure of scenes A (ghost) and B."""
    return ORG2 + np.array([x * MM2, y * MM2, 0.0])


def ghost_hook():
    return hook_profile(MM2, ORG2, color=GRAYTXT, opacity=0.30, stroke_color=GRAYTXT, stroke_width=2.0)


def full_hook():
    return hook_profile(MM2, ORG2)


def bridge_text():
    return Text(cap("q2_a_bridge"), font_size=40, color=GRAYTXT).move_to(BRIDGE_POS)


def assume_tag():
    return fit_width(Text(cap("q2_assumptions"), font_size=16, color=GRAYTXT), 12.8).move_to([0, ASSUME_Y, 0])


def mtex(parts, colors, size=44, **kw):
    """MathTex split into term pieces, one colour per piece (the colour of a variable never changes, SKILL 51)."""
    m = MathTex(*parts, font_size=size, **kw)
    for p, c in zip(m, colors):
        p.set_color(c)
    return m


def left_at(m, x0, y):
    return m.move_to([x0, y, 0]).align_to([x0, 0, 0], LEFT)


def leader(label, target, color=GRAYTXT, side=LEFT):
    """Thin arrow from the border of a label to a point (SKILL 30: the line that proves 'this is here')."""
    start = label.get_edge_center(side) + side * 0.08
    return Arrow(start, np.array(target, float), buff=0, color=color, stroke_width=2, tip_length=0.14,
                 max_tip_length_to_length_ratio=0.5)


def wrap2(txt):
    """Break one caption string into two lines at the space nearest its middle (no text is typed)."""
    if "\n" in txt or " " not in txt:
        return txt
    mid = len(txt) / 2.0
    spaces = [i for i, ch in enumerate(txt) if ch == " "]
    k = min(spaces, key=lambda i: abs(i - mid))
    return txt[:k] + "\n" + txt[k + 1:]


# =====================================================================================================================
# A -- the straight bar (2D)
# =====================================================================================================================
BAR_X, BAR_W = -5.0, 1.0
PL_H, PL_GAP, N_PL = 0.36, 0.06, 8
BAR_Y0 = -2.55


def plate_y(k):
    """Centre y of plate k (0 = bottom) of the straight bar."""
    return BAR_Y0 + k * (PL_H + PL_GAP) + PL_H / 2


def straight_bar():
    plates = VGroup()
    for k in range(N_PL):
        r = Rectangle(width=BAR_W, height=PL_H, stroke_width=1.6, stroke_color=C_HOOK_EDGE, fill_color=C_HOOK,
                      fill_opacity=(0.9, 0.78)[k % 2])
        r.move_to([BAR_X, plate_y(k), 0])
        plates.add(r)
    return plates


class HookQ2_A_Straight(Beats, SafeScene):
    def construct(self):
        # ============================================================ 0.0-3.0  title + page ref
        ttl, ref = hook_title("q2_title", "q2_ref", size=28, ref_size=15)
        self.mark(0.0, "title")
        self.play(FadeIn(ttl, shift=UP * 0.4), FadeIn(ref, shift=UP * 0.4), run_time=1.0)
        self.until(3.0)

        # ============================================================ 3.0-10.0  the doubt as a quotation card
        self.mark(3.0, "claim card")
        q = fit_width(Text(cap("q2_claim"), font_size=36, color=WHITE), 10.5)
        frame = SurroundingRectangle(q, color=METAL, buff=0.45, corner_radius=0.25, stroke_width=3)
        q_open = Text("“", font_size=80, color=METAL).next_to(frame.get_corner(UL), UL, buff=0.02)
        q_close = Text("”", font_size=80, color=METAL).next_to(frame.get_corner(DR), DR, buff=0.02)
        card = VGroup(frame, q, q_open, q_close).move_to([0, 0.1, 0])
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.until(9.0)
        self.play(FadeOut(card, shift=DOWN * 0.2), run_time=1.0)
        self.until(10.0)

        # ============================================================ 10.0-25.0  the straight bar, 8 plates, axial pull
        self.mark(10.0, "bar of 8 plates")
        cap1 = caption_c("q2_a_straight")
        plates = straight_bar()
        top_y = BAR_Y0 + N_PL * PL_H + (N_PL - 1) * PL_GAP
        f_up = force_arrow([BAR_X, top_y + 0.07, 0], [BAR_X, top_y + 0.77, 0], width=6, tip=0.2)
        f_dn = force_arrow([BAR_X, BAR_Y0 - 0.07, 0], [BAR_X, BAR_Y0 - 0.77, 0], width=6, tip=0.2)
        lab_fu = MathTex("F", font_size=34, color=C_F).next_to(f_up, RIGHT, buff=0.1)
        lab_fd = MathTex("F", font_size=34, color=C_F).next_to(f_dn, RIGHT, buff=0.1)
        self.play(FadeIn(cap1, shift=UP * 0.2),
                  LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in plates], lag_ratio=0.25), run_time=2.5)
        self.play(GrowArrow(f_up), GrowArrow(f_dn), FadeIn(lab_fu), FadeIn(lab_fd), run_time=1.5)
        y_if = BAR_Y0 + 2 * (PL_H + PL_GAP) - PL_GAP / 2                    # an interface of the LOWER half (it never moves)
        lab_layers = fit_width(Text(cap("q2_lab_layers"), font_size=22, color=WHITE), 2.4).move_to([-2.85, y_if + 0.2, 0])
        arr_layers = leader(lab_layers, [BAR_X + BAR_W / 2 + 0.03, y_if, 0])
        self.play(FadeIn(lab_layers), Create(arr_layers), Indicate(plates, color=WHITE, scale_factor=1.0), run_time=1.0)
        self.until(15.0)
        # cut the bar across one interface, open the gap, show equal stress arrows on the cut face
        y_cut = BAR_Y0 + 4 * (PL_H + PL_GAP) - PL_GAP / 2
        cut = DashedLine([BAR_X - 0.9, y_cut, 0], [BAR_X + 0.9, y_cut, 0], color=WHITE, stroke_width=3, dash_length=0.1)
        self.play(Create(cut), run_time=1.0)
        upper = VGroup(*plates[4:], f_up, lab_fu)
        y_lo = y_cut - PL_GAP / 2
        xs_st = [BAR_X + (i - 3) * 0.125 for i in range(7)]
        stress = VGroup(*[force_arrow([x, y_lo + 0.02, 0], [x, y_lo + 0.5, 0], color=C_AVG, width=4, tip=0.1) for x in xs_st])
        self.play(upper.animate.shift(UP * 0.5), FadeOut(cut),
                  LaggedStart(*[GrowArrow(a) for a in stress], lag_ratio=0.1), run_time=2.0)
        lab_uni = fit_width(Text(cap("q2_lab_uniform"), font_size=22, color=WHITE), 2.6).move_to([-2.85, y_lo + 0.25, 0])
        arr_uni = leader(lab_uni, [xs_st[-1] + 0.12, y_lo + 0.25, 0])
        self.play(FadeIn(lab_uni), Create(arr_uni), Indicate(stress, color=WHITE, scale_factor=1.0), run_time=1.0)
        self.until(25.0)

        # ============================================================ 25.0-40.0  sigma = F/A term by term, then the bond
        self.mark(25.0, "formula")
        cap2 = caption_c("q2_a_calc")
        assume = assume_tag()
        x0 = -2.3
        eq1 = left_at(mtex([r"\sigma", r"=", r"F", r"/", r"A"], [C_AVG, WHITE, C_F, WHITE, C_AVG], size=48), x0, 1.15)
        eq_rest = mtex([r"=", r"100", r"/", r"64", r"=", r"1.56\ \mathrm{MPa}"], [WHITE, C_F, WHITE, C_AVG, WHITE, C_AVG], size=48)
        eq_rest.next_to(eq1, RIGHT, buff=0.2)
        sq = Square(side_length=1.3, stroke_width=3, stroke_color=C_AVG, fill_color=C_AVG, fill_opacity=0.2)
        sq.move_to([-0.2, -0.95, 0])                 # clear of the two Thai labels that are still fading out at 25-26 s
        d1 = Text("8 mm", font_size=20, color=GRAYTXT).next_to(sq, DOWN, buff=0.12)
        d2 = Text("8 mm", font_size=20, color=GRAYTXT).next_to(sq, RIGHT, buff=0.12)
        sq_g = VGroup(sq, d1, d2)
        self.play(cap_swap(cap1, cap2), FadeOut(lab_layers), FadeOut(arr_layers), FadeOut(lab_uni), FadeOut(arr_uni),
                  FadeIn(eq1, shift=UP * 0.1), FadeIn(sq_g), FadeIn(assume), run_time=1.5)
        self.until(28.2)
        self.mark(28.2, "glow F")
        glow(self, eq1[2], [f_up, f_dn], C_F, run_time=1.5)
        self.until(32.2)
        self.mark(32.2, "glow A")
        glow(self, eq1[4], sq, C_AVG, run_time=1.5)
        self.until(34.0)
        self.play(Write(eq_rest), run_time=1.5)
        self.until(35.5)
        # 35.5-40.0  the bond between two layers (magnifier on an interface of the lower half)
        self.mark(35.5, "neck")
        cap3 = caption_c("q2_a_neck")
        sc = np.array([BAR_X + BAR_W / 2, y_if, 0.0])
        bc = np.array([1.6, -0.9, 0.0])
        sr, br = 0.2, 1.6
        circ_s = Circle(radius=sr, color=GRAYTXT, stroke_width=2.5).move_to(sc)
        circ_b = Circle(radius=br, color=GRAYTXT, stroke_width=2.5).move_to(bc)
        cone = magnifier_cone(sc, sr, bc, br)
        top_s, bot_s, bond = inset_strands(bc)
        pull_up = force_arrow(bc + np.array([-0.55, 0.62, 0]), bc + np.array([-0.55, 1.28, 0]), color=C_F, width=5, tip=0.16)
        pull_dn = force_arrow(bc + np.array([-0.55, -0.62, 0]), bc + np.array([-0.55, -1.28, 0]), color=C_F, width=5, tip=0.16)
        self.play(FadeOut(eq1), FadeOut(eq_rest), FadeOut(sq_g), cap_swap(cap2, cap3), run_time=0.6)
        self.play(Create(circ_s), Create(cone), Indicate(plates, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.play(FadeIn(circ_b), FadeIn(top_s), FadeIn(bot_s), FadeIn(bond), run_time=0.8)
        self.play(GrowArrow(pull_up), GrowArrow(pull_dn), run_time=1.0)
        self.play(Indicate(bond, color=WHITE, scale_factor=1.0), run_time=1.0)
        self.until(40.0)

        # ============================================================ 40.0-45.0  fade, keep a ghost J + the bridge sentence
        self.mark(40.0, "bridge")
        self.play(FadeOut(Group(*self.mobjects), shift=DOWN * 0.3), run_time=1.0)
        ghost, bridge = ghost_hook(), bridge_text()
        self.play(FadeIn(ghost), FadeIn(bridge, shift=UP * 0.2), run_time=1.5)
        self.until(45.0)


# =====================================================================================================================
# B -- the J hook: the weight hangs d away from the stem (2D)
# =====================================================================================================================
DIM_Y = 18.0                      # mm: height of the d dimension line on the hook figure
ARC_Y = 31.0                      # mm: centre of the moment arc on the stem axis
CUT_Y = 36.0                      # mm: the stem section used by the stress-diagram part
X0_EQ = -2.7                      # left edge of the equation column
DIAG_C = np.array([2.6, -0.5, 0.0])      # centre of the stress diagram (section line)
DIAG_W, DIAG_S = 3.4, 0.09               # section width on screen, screen units per MPa
B_BARS = dict(base=[0.6, -2.6, 0], unit=0.10, bar_w=1.2, gap=3.0, num_size=34)
LAYER_YS = (11.5, 23.5, 35.5, 47.5, 59.5, 71.5)       # layer interfaces (mm) drawn on the hook figure


def fmt_ratio(r):
    return (f"{r:.1f}" if r >= 10 else f"{r:.2f}") + "×"


def hook_load_marks(d):
    """Cord arrow (force F down on the base), weight block and the d dimension for a cord position d (mm from the stem axis)."""
    cord = force_arrow(hp(d, BASE_T), hp(d, -11.0), color=C_F, width=6, tip=0.18)
    weight = Rectangle(width=0.5, height=0.34, stroke_width=1.5, stroke_color=WHITE, fill_color=METAL, fill_opacity=1.0)
    weight.move_to([hp(d, 0)[0], hp(d, -11.0)[1] - 0.17, 0])
    dim = VGroup(Line(hp(0, DIM_Y), hp(d, DIM_Y), color=C_D, stroke_width=5),
                 Line(hp(0, DIM_Y - 1.6), hp(0, DIM_Y + 1.6), color=C_D, stroke_width=3),
                 Line(hp(d, DIM_Y - 1.6), hp(d, DIM_Y + 1.6), color=C_D, stroke_width=3),
                 DashedLine(hp(d, BASE_T + 1.0), hp(d, DIM_Y - 1.6), color=C_D, stroke_width=2, dash_length=0.06))
    return cord, weight, dim


def hline_segments(y, loops):
    """x-intervals (mm) of the J profile (outer loop + eye hole) at height y."""
    xs = []
    for lp in loops:
        q = np.roll(lp, -1, axis=0)
        for a, b in zip(lp, q):
            if (a[1] - y) * (b[1] - y) < 0:
                xs.append(a[0] + (y - a[1]) / (b[1] - a[1]) * (b[0] - a[0]))
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


def layer_lines():
    """Thin dark lines across the hook at the layer interfaces (the layers are horizontal slices of the upright part)."""
    outer, hole = hook_outline_mm()
    g = VGroup()
    for y in LAYER_YS:
        for x0, x1 in hline_segments(y, [outer, hole]):
            g.add(Line(hp(x0, y), hp(x1, y), color=BLACK, stroke_width=2.5))
    return g


def section_icon(center=(5.4, 1.05), side=1.4):
    """8x8 mm stem section seen from above: inner fibre (cavity side) on the RIGHT, outer on the LEFT."""
    cx, cy = center
    sq = Square(side_length=side, stroke_width=3, stroke_color=C_AVG, fill_color=C_AVG, fill_opacity=0.18).move_to([cx, cy, 0])
    axis = DashedLine([cx, cy - side / 2 - 0.12, 0], [cx, cy + side / 2 + 0.12, 0], color=C_REF, stroke_width=2, dash_length=0.08)
    cdim = VGroup(Line([cx, cy, 0], [cx + side / 2, cy, 0], color=C_REF, stroke_width=4),
                  Line([cx, cy - 0.1, 0], [cx, cy + 0.1, 0], color=C_REF, stroke_width=3),
                  Line([cx + side / 2, cy - 0.1, 0], [cx + side / 2, cy + 0.1, 0], color=C_REF, stroke_width=3))
    c_lab = MathTex("c", font_size=30, color=C_REF).move_to([cx + side / 4, cy + 0.24, 0])
    edge_in = Line([cx + side / 2, cy - side / 2, 0], [cx + side / 2, cy + side / 2, 0], color=C_SIG_T, stroke_width=7)
    edge_out = Line([cx - side / 2, cy - side / 2, 0], [cx - side / 2, cy + side / 2, 0], color=C_SIG_C, stroke_width=7)
    dims = Text("8 × 8 mm", font_size=20, color=GRAYTXT).move_to([cx, cy - side / 2 - 0.36, 0])
    return dict(sq=sq, axis=axis, cdim=cdim, c_lab=c_lab, edge_in=edge_in, edge_out=edge_out, dims=dims)


def stress_parts(sig_a, sig_b, width, scale, center, n=18):
    """Pieces of the stress diagram across the section (section line horizontal, stress drawn UP = tension, inner fibre RIGHT):
    uniform sigma_axial block, the two bending triangles (tension right / compression left), the gradient trapezoid that
    replaces them (WARN -> FIELD, SKILL 21.6), its outline, and the zero line."""
    c = np.asarray(center, float)
    w2 = width / 2.0
    s_in, s_out = sig_a + sig_b, sig_a - sig_b
    L = sig_a * scale
    uniform = Polygon(c + [-w2, 0, 0], c + [w2, 0, 0], c + [w2, L, 0], c + [-w2, L, 0],
                      stroke_color=C_AVG, stroke_width=2, fill_color=C_AVG, fill_opacity=0.45)
    tri_r = Polygon(c + [0, L, 0], c + [w2, L, 0], c + [w2, L + sig_b * scale, 0],
                    stroke_width=0, fill_color=C_SIG_T, fill_opacity=0.55)
    tri_l = Polygon(c + [0, L, 0], c + [-w2, L, 0], c + [-w2, L - sig_b * scale, 0],
                    stroke_width=0, fill_color=C_SIG_C, fill_opacity=0.55)
    xs = np.linspace(-w2, w2, n + 1)

    def sig(x):
        return s_out + (s_in - s_out) * (x + w2) / width
    strips = VGroup()
    for i in range(n):
        xa, xb = xs[i], xs[i + 1] + (0.012 if i < n - 1 else 0.0)
        pa, pb = sig(xs[i]), sig(xs[i + 1])
        frac = float(np.clip(((pa + pb) / 2.0 - s_out) / (s_in - s_out), 0.0, 1.0))
        col = interpolate_color(ManimColor(C_SIG_C), ManimColor(C_SIG_T), frac)
        strips.add(Polygon(c + [xa, 0, 0], c + [xb, 0, 0], c + [xb, pb * scale, 0], c + [xa, pa * scale, 0],
                           stroke_width=0, fill_color=col, fill_opacity=0.8))
    outline = Polygon(c + [-w2, 0, 0], c + [w2, 0, 0], c + [w2, s_in * scale, 0], c + [-w2, s_out * scale, 0],
                      color=WHITE, stroke_width=3, fill_opacity=0)
    axis = Line(c + [-w2 - 0.3, 0, 0], c + [w2 + 0.3, 0, 0], color=C_REF, stroke_width=2)
    return uniform, VGroup(tri_r, tri_l), strips, outline, axis


def b_chart(get_b):
    """The bar pair of B's last row (average F/A vs the inner-fibre sigma). C replays its final frame with this same builder."""
    return BarPair(lambda: sigma_axial(), get_b, C_AVG, C_SIG_T, decimals=2, decimals_b=1, **B_BARS)


class HookQ2_B_Offset(Beats, SafeScene):
    def construct(self):
        # ============================================================ 0.0-3.0  ghost J -> full colour, bridge -> title (continuity from A)
        ghost, bridge = ghost_hook(), bridge_text()
        self.add(ghost, bridge)
        ttl, ref = hook_title("q2_b_title", "q2_ref", size=28, ref_size=15)
        hook = full_hook()
        self.mark(0.0, "ghost J -> hook, bridge -> title")
        self.play(ReplacementTransform(ghost, hook), ReplacementTransform(bridge, ttl),
                  FadeIn(ref, shift=UP * 0.2), run_time=1.5)
        self.until(3.0)

        # ============================================================ 3.0-20.0  two forces not on one line
        self.mark(3.0, "rod force up on the stem line, weight d away")
        cap1 = caption_c("q2_b_offset")
        assume = assume_tag()
        rod = Circle(radius=0.215, stroke_color=WHITE, stroke_width=1.5, fill_color=METAL, fill_opacity=1.0)
        rod.move_to(hp(0, EYE_C[1]))
        f_rod = force_arrow(hp(0, 91.0), hp(0, 102.0), color=C_F, width=6, tip=0.18)
        cord, weight, dim = hook_load_marks(D_CASE_A)
        axis = DashedLine(hp(0, 5.0), hp(0, 90.0), color=C_REF, stroke_width=2, dash_length=0.1)
        lab_f1 = MathTex("F", font_size=34, color=C_F).next_to(f_rod, RIGHT, buff=0.1)
        lab_f2 = MathTex("F", font_size=34, color=C_F).move_to(hp(D_CASE_A, -4.0) + RIGHT * 0.3)
        arc = Arc(radius=0.3, start_angle=160 * DEGREES, angle=-250 * DEGREES, color=C_M, stroke_width=5)
        arc.move_arc_center_to(hp(0, ARC_Y))
        arc.add_tip(tip_length=0.15)
        lab_m = MathTex("M", font_size=32, color=C_M).move_to(hp(0, ARC_Y) + RIGHT * 0.55)
        d_txt = Text("d = 19 mm", font_size=26, color=C_D).move_to([-1.9, -1.85, 0])
        lab_rodf = fit_width(Text(cap("q2_lab_rodf"), font_size=22, color=WHITE), 2.6).move_to([-3.1, 1.5, 0])
        arr_rodf = leader(lab_rodf, hp(0, 97.0) + RIGHT * 0.07)
        lab_arm = fit_width(Text(cap("q2_lab_arm"), font_size=22, color=WHITE), 3.6).move_to([-1.9, -1.3, 0])
        arr_arm = leader(lab_arm, hp(D_CASE_A / 2, DIM_Y) + UP * 0.03)
        self.play(FadeIn(cap1, shift=UP * 0.2), FadeIn(rod), GrowArrow(f_rod), GrowArrow(cord), FadeIn(weight),
                  FadeIn(lab_f1), FadeIn(lab_f2), run_time=1.5)                                      # 3.0-4.5
        self.play(Create(axis), run_time=1.0)                                                          # 4.5-5.5
        self.play(GrowFromCenter(dim), FadeIn(d_txt), FadeIn(assume), run_time=1.5)                    # 5.5-7.0
        self.play(Create(arc), FadeIn(lab_m), run_time=1.5)                                            # 7.0-8.5
        self.play(Indicate(dim, color=WHITE, scale_factor=1.0), run_time=1.0)                          # 8.5-9.5
        self.play(FadeIn(lab_rodf), Create(arr_rodf), FadeIn(lab_arm), Create(arr_arm), run_time=1.0)  # 9.5-10.5
        self.play(Indicate(f_rod, color=WHITE, scale_factor=1.0), Indicate(cord, color=WHITE, scale_factor=1.0),
                  run_time=1.0)                                                                        # 10.5-11.5
        self.until(19.0)
        self.play(FadeOut(lab_rodf), FadeOut(arr_rodf), FadeOut(lab_arm), FadeOut(arr_arm), FadeOut(cap1), run_time=1.0)
        self.until(20.0)

        # ============================================================ 20.0-45.0  four equations, term by term (SKILL 51)
        self.mark(20.0, "four equations")
        icon = section_icon()
        yL, yA, yB, yC = 1.75, 0.85, 0.0, -1.0              # step label / symbolic line / numbers line / calc line

        def step_label(key):
            return left_at(fit_width(Text(cap(key), font_size=26, color=WHITE), 6.8), X0_EQ, yL)
        st1, st2, st3, st4 = [step_label(f"q2_b_step{i}") for i in (1, 2, 3, 4)]
        eq1a = left_at(mtex([r"M", r"=", r"F", r"\cdot", r"d"], [C_M, WHITE, C_F, WHITE, C_D], 44), X0_EQ, yA)
        eq1b = left_at(mtex([r"=", r"100", r"\times", r"19", r"=", r"1{,}900\ \mathrm{N{\cdot}mm}"],
                            [WHITE, C_F, WHITE, C_D, WHITE, C_M], 44), X0_EQ, yB)
        eq2a = left_at(mtex([r"\sigma_{\mathrm{axial}}", r"=", r"F", r"/", r"A"], [C_AVG, WHITE, C_F, WHITE, C_AVG], 44), X0_EQ, yA)
        eq2b = left_at(mtex([r"=", r"100", r"/", r"64", r"=", r"1.56\ \mathrm{MPa}"],
                            [WHITE, C_F, WHITE, C_AVG, WHITE, C_AVG], 44), X0_EQ, yB)
        eq3a = left_at(mtex([r"\sigma_{\mathrm{bend}}", r"=", r"M", r"\cdot", r"c", r"/", r"I"],
                            [C_SIG_T, WHITE, C_M, WHITE, C_REF, WHITE, C_REF], 44), X0_EQ, yA)
        eq3b = left_at(mtex([r"=", r"1{,}900", r"\times", r"4", r"/", r"341", r"=", r"22.3\ \mathrm{MPa}"],
                            [WHITE, C_M, WHITE, C_REF, WHITE, C_REF, WHITE, C_SIG_T], 44), X0_EQ, yB)
        eq4a = left_at(mtex([r"\sigma_{\mathrm{inner}}", r"=", r"\sigma_{\mathrm{axial}}", r"+", r"\sigma_{\mathrm{bend}}"],
                            [C_SIG_T, WHITE, C_AVG, WHITE, C_SIG_T], 44), X0_EQ, yA)
        eq4b = left_at(mtex([r"=", r"1.56", r"+", r"22.3", r"=", r"23.8\ \mathrm{MPa}"],
                            [WHITE, C_AVG, WHITE, C_SIG_T, WHITE, C_SIG_T], 44), X0_EQ, yB)
        calc1 = left_at(fit_width(Text(cap("q2_b_calc1"), font_size=22, color=GRAYTXT), 9.6), X0_EQ, yC)
        calc2 = left_at(fit_width(Text(cap("q2_b_calc2"), font_size=22, color=WHITE), 9.6), X0_EQ, yC)
        # step 1 (20-26): M = F d
        self.play(FadeIn(st1, shift=UP * 0.1), FadeIn(eq1a, shift=UP * 0.1), run_time=1.0)
        glow(self, eq1a[2], [f_rod, cord], C_F, run_time=1.2)
        glow(self, eq1a[4], dim, C_D, run_time=1.2)
        glow(self, eq1a[0], arc, C_M, run_time=1.2)
        self.play(Write(eq1b), run_time=1.0)
        self.until(26.0)
        # step 2 (26-32): sigma_axial = F / A
        self.mark(26.0, "step 2")
        self.play(TransformMatchingTex(eq1a, eq2a), FadeOut(eq1b), cap_swap(st1, st2),
                  FadeIn(icon["sq"]), FadeIn(icon["dims"]), run_time=1.0)
        glow(self, eq2a[2], [f_rod, cord], C_F, run_time=1.2)
        glow(self, eq2a[4], icon["sq"], C_AVG, run_time=1.2)
        self.play(Write(eq2b), run_time=1.0)
        self.until(32.0)
        # step 3 (32-39): sigma_bend = M c / I
        self.mark(32.0, "step 3")
        self.play(TransformMatchingTex(eq2a, eq3a), FadeOut(eq2b), cap_swap(st2, st3), FadeIn(icon["axis"]),
                  FadeIn(icon["cdim"]), FadeIn(icon["c_lab"]), FadeIn(icon["edge_in"]), FadeIn(icon["edge_out"]),
                  run_time=1.0)
        glow(self, eq3a[2], arc, C_M, run_time=1.0)
        glow(self, eq3a[4], icon["cdim"], C_REF, run_time=1.0)
        glow(self, eq3a[6], icon["sq"], C_REF, run_time=1.0)
        self.play(FadeIn(calc1, shift=UP * 0.1), run_time=0.8)
        self.play(Write(eq3b), run_time=1.0)
        self.until(39.0)
        # step 4 (39-45): sigma_inner = sigma_axial + sigma_bend
        self.mark(39.0, "step 4")
        self.play(TransformMatchingTex(eq3a, eq4a), FadeOut(eq3b), cap_swap(st3, st4), run_time=1.0)
        glow(self, eq4a[2], icon["sq"], C_AVG, run_time=1.0)
        glow(self, eq4a[4], [icon["edge_in"], icon["edge_out"]], C_SIG_T, run_time=1.0)
        self.play(Write(eq4b), cap_swap(calc1, calc2), run_time=1.2)
        self.play(Indicate(eq4b[5], color=WHITE, scale_factor=1.2), run_time=0.8)
        self.until(45.0)

        # ============================================================ 45.0-60.0  stress across the section
        self.mark(45.0, "stress diagram")
        cap2 = caption_c("q2_b_diagram")
        uniform, tri, strips, outline, base_ax = stress_parts(sigma_axial(), sigma_bend(D_CASE_A), DIAG_W, DIAG_S, DIAG_C)
        lines = layer_lines()
        cut_line = DashedLine(hp(-8, CUT_Y), hp(10, CUT_Y), color=WHITE, stroke_width=2.5, dash_length=0.08)
        dot_in = Dot(hp(STEM_HW, CUT_Y), radius=0.06, color=C_SIG_T)
        dot_out = Dot(hp(-STEM_HW, CUT_Y), radius=0.06, color=C_SIG_C)
        top_y = DIAG_C[1] + sigma_inner(D_CASE_A) * DIAG_S
        bot_y = DIAG_C[1] + sigma_outer(D_CASE_A) * DIAG_S
        xr, xl = DIAG_C[0] + DIAG_W / 2 + 1.05, DIAG_C[0] - DIAG_W / 2 - 1.05
        val_in = Text(f"+{sigma_inner(D_CASE_A):.1f} MPa", font_size=26, color=C_SIG_T).move_to([xr, top_y, 0])
        lab_in = fit_width(Text(cap("q2_lab_inner"), font_size=22, color=C_SIG_T), 2.0).move_to([xr, top_y - 0.5, 0])
        val_out = Text(f"−{abs(sigma_outer(D_CASE_A)):.1f} MPa", font_size=26, color=C_SIG_C).move_to([xl, bot_y, 0])
        lab_out = fit_width(Text(cap("q2_lab_outer"), font_size=22, color=C_SIG_C), 2.0).move_to([xl, bot_y + 0.5, 0])
        x_zero = DIAG_C[0] - (sigma_axial() * I_MM4 / (F_N * D_CASE_A)) * (DIAG_W / SEC_H)       # -0.28 mm towards the outer side
        zero_dot = Dot([x_zero, DIAG_C[1], 0], radius=0.07, color=WHITE)
        zero_lab = fit_width(Text(wrap2(cap("q2_b_zero")), font_size=20, color=WHITE), 5.0).move_to([DIAG_C[0], -3.15, 0])
        zero_lead = Line([x_zero, zero_lab.get_top()[1] + 0.05, 0], [x_zero, DIAG_C[1] - 0.08, 0], color=WHITE, stroke_width=1.5)
        gone = [eq4a, eq4b, st4, calc2, arc, lab_m] + [icon[k] for k in icon]
        self.play(*[FadeOut(m) for m in gone], FadeIn(cap2, shift=UP * 0.2), run_time=1.0)             # 45-46
        self.play(Create(uniform), Create(base_ax), FadeIn(cut_line), FadeIn(dot_in), FadeIn(dot_out), run_time=1.5)   # 46-47.5
        self.play(Create(tri), run_time=1.5)                                                           # 47.5-49
        self.play(ReplacementTransform(VGroup(uniform, *tri), strips), Create(outline), FadeIn(lines), run_time=2.0)   # 49-51
        self.play(FadeIn(val_in), FadeIn(lab_in), FadeIn(val_out), FadeIn(lab_out),
                  Indicate(VGroup(*strips[-3:]), color=WHITE, scale_factor=1.0),
                  Indicate(VGroup(*strips[:3]), color=WHITE, scale_factor=1.0), run_time=1.5)          # 51-52.5
        self.play(FadeIn(zero_dot), Create(zero_lead), FadeIn(zero_lab), run_time=1.5)                 # 52.5-54
        self.until(60.0)

        # ============================================================ 60.0-75.0  one ValueTracker d drives picture and numbers
        self.mark(60.0, "bars, d: 19 -> 5")
        cap3 = caption_c("q2_b_ratio")
        d = ValueTracker(D_CASE_A)
        bars = b_chart(lambda: sigma_inner(d.get_value()))
        lab_avg = fit_width(Text(cap("q2_lab_avg"), font_size=22, color=WHITE), 2.6).move_to(bars.ax + DOWN * 0.4)
        lab_surf = fit_width(Text(cap("q2_lab_surf"), font_size=22, color=WHITE), 2.6).move_to(bars.bx + DOWN * 0.4)
        r_lab = mtex([r"\sigma_{\mathrm{inner}}", r"/", r"\sigma_{\mathrm{axial}}"], [C_SIG_T, WHITE, C_AVG], 34).move_to([5.3, 0.7, 0])
        ratio = always_redraw(lambda: Text(fmt_ratio(sigma_inner(d.get_value()) / sigma_axial()), font_size=52,
                                           color=WHITE).move_to([5.3, -0.1, 0]))
        live_cw = always_redraw(lambda: VGroup(*hook_load_marks(d.get_value())[:2]))
        live_dm = always_redraw(lambda: hook_load_marks(d.get_value())[2])
        live_txt = always_redraw(lambda: Text(f"d = {d.get_value():.0f} mm", font_size=26, color=C_D).move_to([-1.9, -1.85, 0]))
        fades = [strips, outline, base_ax, val_in, lab_in, val_out, lab_out, zero_dot, zero_lead, zero_lab, cut_line,
                 dot_in, dot_out, lines]
        self.play(*[FadeOut(m) for m in fades], cap_swap(cap2, cap3), run_time=1.0)                    # 60-61
        self.remove(cord, weight, dim, d_txt)                                  # identical live copies take over (d = 19)
        self.add(live_cw, live_dm, live_txt)
        self.play(FadeIn(bars, shift=UP * 0.2), FadeIn(lab_avg), FadeIn(lab_surf), FadeIn(r_lab), FadeIn(ratio),
                  run_time=1.5)                                                                        # 61-62.5
        self.play(Indicate(bars.num_a, color=WHITE, scale_factor=1.25), run_time=1.0)                  # 62.5-63.5
        self.play(Indicate(bars.num_b, color=WHITE, scale_factor=1.25), run_time=1.0)                  # 63.5-64.5
        self.until(65.0)
        self.mark(65.0, "d 19 -> 5")
        self.play(d.animate.set_value(D_CASE_B), run_time=6.0, rate_func=smooth)                       # 65-71
        cap4 = caption_c("q2_b_caseB")
        self.play(cap_swap(cap3, cap4), run_time=1.0)                                                  # 71-72
        self.play(Indicate(ratio, color=WHITE, scale_factor=1.15), run_time=1.5)                       # 72-73.5
        self.until(75.0)


# =====================================================================================================================
# C -- which way does the stress run relative to the layers? (3D, camera move)
# =====================================================================================================================
MM3 = 0.05                           # world units per mm
ALPHA = 45 * DEGREES                 # the J plane is turned 45 deg about the vertical, so the camera at theta = -45 sees it face-on
PHI0 = 80 * DEGREES                  # camera elevation 10 deg while the model is introduced
PHI_CRACK = 66 * DEGREES             # steeper view for the crack: the horizontal fracture plane must be visible
TH0, TH1 = -45 * DEGREES, -25 * DEGREES
ZS = (-4.0, -2.0, 0.0, 2.0, 4.0)     # depth levels (mm) of the flat copies that make each band a slab (SKILL 2: flat shapes only)
ZOPS = (0.5, 0.5, 0.55, 0.65, 0.95)
BANDS = [(0, 10), (13, 22), (25, 34), (37, 46), (49, 58), (61, 70), (73, 81), (84, 90)]   # mm along the stem; gaps = layer interfaces
CRACK_Y = 11.5                       # middle of the gap between band 0 and band 1: the one layer plane the crack runs along
SCR_C = (-3.7, -0.35)                # screen position of the J's bounding-box centre
MM_CMP = 0.04                        # scale of the two pictograms of the comparison (C 38-55) and of D's first frame
CMP_CY = -0.55
CMP_LEFT_X, CMP_RIGHT_X = -3.4, 3.4
_BANDS2D = []


def band_pieces():
    """The 8 horizontal slices of the upright J (profile coordinates, mm), cut with a boolean intersection once."""
    if not _BANDS2D:
        full = hook_profile(1.0, np.zeros(3), color=C_HOOK, opacity=1.0, stroke_width=0)
        for y0, y1 in BANDS:
            rect = Rectangle(width=120, height=y1 - y0, stroke_width=0, fill_opacity=1).move_to([HOOK_CX, (y0 + y1) / 2.0, 0])
            _BANDS2D.append(Intersection(full, rect, color=C_HOOK, fill_opacity=1.0, stroke_width=0))
    return _BANDS2D


def to_world(P, zp, W0):
    """J-profile point(s) (mm) at depth zp (mm, positive = towards the camera) -> world coordinates of scene C."""
    P = np.asarray(P, float)
    c, s = np.cos(ALPHA), np.sin(ALPHA)
    u = P[..., 0] - HOOK_CX
    return np.stack([W0[0] + (u * c + zp * s) * MM3, W0[1] + (u * s - zp * c) * MM3,
                     W0[2] + (P[..., 1] - HOOK_CY) * MM3], axis=-1)


def bands_3d(W0):
    """One VGroup per band: 5 flat copies back-to-front (opacity ramps up, only the front one has an outline)."""
    out = []
    for k, piece in enumerate(band_pieces()):
        g = VGroup()
        for zp, op in zip(ZS, ZOPS):
            m = piece.copy()
            m.points = to_world(piece.points, zp, W0)
            m.set_fill(C_HOOK, opacity=op * (1.0 if k % 2 == 0 else 0.88))
            m.set_stroke(C_HOOK_EDGE, width=1.4 if zp == ZS[-1] else 0)
            g.add(m)
        out.append(g)
    return out


def prof_poly(W0, pts_mm, zp, closed=False, **style):
    """Flat polyline in the J plane at depth zp (markers, reference lines)."""
    m = VMobject(**style)
    q = to_world(np.asarray(pts_mm, float), zp, W0)
    if closed:
        q = np.concatenate([q, q[:1]], axis=0)
    m.set_points_as_corners(q)
    return m


def circle_pts(cx, cy, r, n=41):
    t = np.linspace(0.0, 2 * np.pi, n)
    return np.stack([cx + r * np.cos(t), cy + r * np.sin(t)], axis=1)


def upright_icon_2d(mm, center):
    """The upright hook as 8 flat bands (screen-space pictogram, identical in the end of C and the start of D)."""
    org = hook_centre_origin(mm, (center[0], center[1], 0.0))
    g = VGroup()
    for k, piece in enumerate(band_pieces()):
        m = piece.copy()
        m.points = np.stack([org[0] + piece.points[:, 0] * mm, org[1] + piece.points[:, 1] * mm,
                             np.zeros(len(piece.points))], axis=1)
        m.set_fill(C_HOOK, opacity=(0.9, 0.78)[k % 2])
        m.set_stroke(C_HOOK_EDGE, width=1.2)
        g.add(m)
    return g


class HookQ2_C_Layers(Beats, SafeThreeDScene):
    # ---------------------------------------------------------------- small helpers (all text is fixed-in-frame, SKILL 4)
    def caption_hud(self, key, size=24):
        m = caption_c(key, size=size)
        m.set_z_index(100)
        self.hud(m)
        return m

    def label_to(self, txt, world_pt, at, size=22, color=WHITE, leader_color=GRAYTXT):
        lab, arr = hud_label(self, txt, world_pt, at=at, size=size, color=color, leader_color=leader_color)
        lab.set_z_index(100)
        arr.set_z_index(99)
        return lab, arr

    def construct(self):
        # the J's centre lands on SCR_C for the MEAN camera azimuth, so it hardly drifts while theta swings -45 -> -25
        self.set_camera_orientation(phi=PHI0, theta=-35 * DEGREES, zoom=1.0)
        W0 = world_at_screen(self, SCR_C, z=0.0)
        self.set_camera_orientation(phi=PHI0, theta=TH0)

        def pt(x, y, zp=0.0):
            return to_world(np.array([x, y], float), zp, W0)

        # ============================================================ 0.0-3.0  B's last frame (the sigma bar) -> the question
        chart = b_chart(lambda: sigma_inner(D_CASE_B))
        chart.stop()
        lab_avg = fit_width(Text(cap("q2_lab_avg"), font_size=22, color=WHITE), 2.6).move_to(chart.ax + DOWN * 0.4)
        lab_surf = fit_width(Text(cap("q2_lab_surf"), font_size=22, color=WHITE), 2.6).move_to(chart.bx + DOWN * 0.4)
        r_lab = mtex([r"\sigma_{\mathrm{inner}}", r"/", r"\sigma_{\mathrm{axial}}"], [C_SIG_T, WHITE, C_AVG], 34)
        r_lab.move_to([5.3, 0.7, 0])
        ratio_t = Text(fmt_ratio(sigma_inner(D_CASE_B) / sigma_axial()), font_size=52, color=WHITE).move_to([5.3, -0.1, 0])
        ttl, ref = hook_title("q2_c_title", "q2_ref", size=28, ref_size=15)
        ttl.set_z_index(100), ref.set_z_index(100)
        replica = [chart.base_line, chart.bar_a, chart.bar_b, chart.num_a, chart.num_b, lab_avg, lab_surf, r_lab, ratio_t]
        for m in replica:
            m.set_z_index(100)
        self.hud(ttl, ref)
        self.hud(*replica, show=True)
        self.mark(0.0, "B's sigma bar -> title")
        self.play(ReplacementTransform(chart.bar_b, ttl), *[FadeOut(m) for m in replica if m is not chart.bar_b],
                  FadeIn(ref, shift=UP * 0.2), run_time=1.5)
        self.until(3.0)

        # ============================================================ 3.0-6.0  the upright hook: 8 horizontal slices along the stem
        self.mark(3.0, "8 slices")
        cap1 = self.caption_hud("q2_c_dir")
        bands = bands_3d(W0)
        for g in bands:
            g.set_z_index(1)
        sig = ValueTracker(0.0)

        def hot():
            frac = float(np.clip(sig.get_value() / sigma_inner(D_CASE_A), 0.0, 1.0))
            return interpolate_color(ManimColor(C_SIG_C), ManimColor(C_SIG_T), frac)       # cool -> hot with sigma (SKILL 21.6)
        strip_f = Polygon(pt(2.4, 13.0, 4.06), pt(4.0, 13.0, 4.06), pt(4.0, 38.0, 4.06), pt(2.4, 38.0, 4.06),
                          stroke_width=0, fill_color=hot(), fill_opacity=0.95)
        strip_s = Polygon(pt(4.03, 13.0, -4.0), pt(4.03, 13.0, 4.0), pt(4.03, 38.0, 4.0), pt(4.03, 38.0, -4.0),
                          stroke_width=0, fill_color=hot(), fill_opacity=0.95)
        for s_ in (strip_f, strip_s):
            s_.set_z_index(10)
            s_.add_updater(lambda m: m.set_fill(hot()))
        self.play(FadeIn(cap1, shift=UP * 0.2), LaggedStart(*[FadeIn(g, shift=OUT * 0.2) for g in bands], lag_ratio=0.25),
                  FadeIn(strip_f), FadeIn(strip_s), run_time=3.0)
        self.until(6.0)

        # ============================================================ 6.0-9.0  name the parts (first time in this clip, SKILL 21.8)
        self.mark(6.0, "names")
        names = []
        for txt, wp, at in [(cap("q1_lab_stem"), pt(-4.0, 26.0, 4.0), (-6.1, 0.1)),
                            (cap("q1_lab_base"), pt(-3.0, 4.0, 4.0), (-6.1, -2.95)),
                            ("r = 2 mm", pt(4.9, 8.9, 4.1), (-3.7, -1.3)),
                            (cap("q2_lab_layers"), pt(4.2, 41.5, 4.0), (-1.7, 0.1))]:
            lab, arr = self.label_to(txt, wp, at)
            names += [lab, arr]
        self.play(*[FadeIn(m) for m in names], run_time=1.0)
        self.until(8.5)
        self.play(*[FadeOut(m) for m in names], run_time=0.5)
        self.until(9.0)

        # ============================================================ 9.0-14.0  camera swings; the tension arrow grows along the stem, 90 deg to the layers
        self.mark(9.0, "camera move + stress arrow")
        s_arrow = arrow3(pt(6.4, 14.0, 4.1), pt(6.4, 37.0, 4.1), C_SIG_T, thickness=0.03, height=0.2)
        ref_line = DashedLine(pt(-6.0, 23.5, 4.12), pt(14.0, 23.5, 4.12), color=WHITE, stroke_width=2.5, dash_length=0.08)
        right_angle = prof_poly(W0, [(6.4, 26.1), (9.0, 26.1), (9.0, 23.5)], 4.12, stroke_color=WHITE, stroke_width=3,
                                fill_opacity=0)
        plane_q = Polygon(pt(-8, 23.5, -7), pt(16, 23.5, -7), pt(16, 23.5, 7), pt(-8, 23.5, 7),
                          stroke_color=WHITE, stroke_width=1, fill_color=WHITE, fill_opacity=0.10)
        s_arrow.set_z_index(20), right_angle.set_z_index(20), ref_line.set_z_index(12), plane_q.set_z_index(5)
        self.move_camera(theta=TH1, run_time=5.0, added_anims=[
            Succession(GrowArrow(s_arrow), Create(right_angle), Create(ref_line)),
            UpdateFromAlphaFunc(sig, lambda m, a: m.set_value(a * sigma_inner(D_CASE_A))),
            FadeIn(plane_q)])

        # ============================================================ 14.0-20.0  what is pulled apart is the narrow bond between layers
        self.mark(14.0, "neck")
        cap2 = self.caption_hud("q2_c_neck")
        p_neck = cam_point(self, pt(4.0, 23.5, 4.0))
        sc = np.array([p_neck[0], p_neck[1], 0.0])
        bc = np.array([3.9, -0.9, 0.0])
        sr, br = 0.2, 1.7
        circ_s = Circle(radius=sr, color=GRAYTXT, stroke_width=2.5).move_to(sc)
        circ_b = Circle(radius=br, color=GRAYTXT, stroke_width=2.5).move_to(bc)
        cone = magnifier_cone(sc, sr, bc, br)
        top_s, bot_s, bond = inset_strands(bc)
        pull_up = force_arrow(bc + np.array([-0.55, 0.66, 0]), bc + np.array([-0.55, 1.34, 0]), color=C_SIG_T, width=5, tip=0.16)
        pull_dn = force_arrow(bc + np.array([-0.55, -0.66, 0]), bc + np.array([-0.55, -1.34, 0]), color=C_SIG_T, width=5, tip=0.16)
        lab_in, arr_in = self.label_to(cap("q2_lab_inner"), pt(6.4, 36.0, 4.1), (-1.5, 0.1), color=C_SIG_T)
        mag = [circ_s, circ_b, cone, top_s, bot_s, bond, pull_up, pull_dn]
        for m in mag:
            m.set_z_index(100)
        self.hud(*mag)
        self.play(cap_swap(cap1, cap2), FadeIn(lab_in), FadeIn(arr_in), run_time=1.0)
        self.play(Create(circ_s), Create(cone), run_time=0.8)
        self.play(FadeIn(circ_b), FadeIn(top_s), FadeIn(bot_s), FadeIn(bond), run_time=0.8)
        self.play(GrowArrow(pull_up), GrowArrow(pull_dn), run_time=1.0)
        self.play(Indicate(bond, color=WHITE, scale_factor=1.0), run_time=1.0)
        self.until(19.0)
        self.play(*[FadeOut(m) for m in mag], FadeOut(lab_in), FadeOut(arr_in), run_time=1.0)
        self.until(20.0)

        # ============================================================ 20.0-38.0  the crack starts at the inner corner and runs along ONE layer
        self.mark(20.0, "notch marker")
        cap3 = self.caption_hud("q2_c_crack")
        ring = prof_poly(W0, circle_pts(4.6, 8.6, 3.0), 4.2, closed=True, stroke_color=C_SIG_T, stroke_width=4, fill_opacity=0)
        ring.set_z_index(30)
        lab_r, arr_r = self.label_to("r = 2 mm", pt(7.6, 8.6, 4.2), (-1.2, -1.45))
        cx = ValueTracker(STEM_HW)

        def crack_pts():
            xf = cx.get_value()
            return [pt(STEM_HW, CRACK_Y, -4.0), pt(STEM_HW, CRACK_Y, 4.0), pt(xf, CRACK_Y, 4.0), pt(xf, CRACK_Y, -4.0),
                    pt(STEM_HW, CRACK_Y, -4.0)]
        crack = VMobject(stroke_width=0, fill_color=C_SIG_T, fill_opacity=0.9)
        crack.set_points_as_corners(crack_pts())
        crack.add_updater(lambda m: m.set_points_as_corners(crack_pts()))
        crack.set_z_index(25)
        face_lo = Polygon(pt(-4, 10, -4), pt(4, 10, -4), pt(4, 10, 4), pt(-4, 10, 4),
                          stroke_color=WHITE, stroke_width=1, fill_color=METAL, fill_opacity=0.9)
        face_up = Polygon(pt(-4, 13, -4), pt(4, 13, -4), pt(4, 13, 4), pt(-4, 13, 4),
                          stroke_color=WHITE, stroke_width=1, fill_color=METAL, fill_opacity=0.9)
        face_lo.set_z_index(26), face_up.set_z_index(26)
        self.play(cap_swap(cap2, cap3), Create(ring), FadeIn(lab_r), FadeIn(arr_r), run_time=1.0)       # 20-21
        self.play(Indicate(ring, color=WHITE, scale_factor=1.6), run_time=1.0)                          # 21-22
        self.until(22.0)
        self.play(FadeOut(lab_r), FadeOut(arr_r), run_time=0.3)
        self.move_camera(phi=PHI_CRACK, run_time=3.0, added_anims=[Indicate(ring, color=WHITE, scale_factor=1.3)])
        self.until(26.0)
        self.mark(26.0, "crack grows across one layer")
        self.add(crack)
        self.play(cx.animate.set_value(-STEM_HW), run_time=4.0, rate_func=linear)                       # 26-30
        self.mark(30.0, "upper part lifts")
        crack.clear_updaters()
        self.play(FadeOut(crack), FadeIn(face_lo), FadeIn(face_up), run_time=0.5)
        upper = VGroup(*bands[1:], strip_f, strip_s, s_arrow, ref_line, right_angle, plane_q, face_up)
        self.play(upper.animate.shift(OUT * 0.15), run_time=1.5)
        self.until(32.0)
        self.mark(32.0, "zoom to the fracture face")
        model = VGroup(*bands, strip_f, strip_s, s_arrow, ref_line, right_angle, plane_q, ring, face_lo, face_up)
        mid_gap = (pt(0.0, 10.0, 0.0) + pt(0.0, 13.0, 0.0)) / 2.0 + np.array([0.0, 0.0, 0.075])
        self.move_camera(zoom=2.0, run_time=3.0, added_anims=[model.animate.shift(-mid_gap)])       # centre the gap, then it magnifies
        self.until(38.0)

        # ============================================================ 38.0-55.0  same hook, same sigma, a different direction relative to the layers
        self.mark(38.0, "compare flat vs upright")
        cap4 = self.caption_hud("q2_c_compare", size=26)
        strip_f.clear_updaters(), strip_s.clear_updaters()
        divider = Line([0, 1.5, 0], [0, -3.1, 0], color=C_REF, stroke_width=2)
        org_l = hook_centre_origin(MM_CMP, (CMP_LEFT_X, CMP_CY, 0.0))
        V = top_view_layer(MM_CMP, org_l)                       # Q1's one-layer top view: body, wall loops, load path, chevrons
        body_l = V["body"].set_fill(C_HOOK, opacity=0.45)
        walls_l = [wall_loop(o, MM_CMP, org_l, stroke_color=C_HOOK, stroke_width=2.0) for o in (0.0, 1.0, 1.9)]
        path_l, chev_l = V["path"], V["chevrons"]
        path_l.set_color(C_AVG), chev_l.set_color(C_AVG)
        icon_r = upright_icon_2d(MM_CMP, (CMP_RIGHT_X, CMP_CY))
        org_r = hook_centre_origin(MM_CMP, (CMP_RIGHT_X, CMP_CY, 0.0))

        def PR(x, y):
            return org_r + np.array([x * MM_CMP, y * MM_CMP, 0.0])
        arrow_r = force_arrow(PR(7.0, 13.0), PR(7.0, 37.0), color=C_SIG_T, width=5, tip=0.13)
        ref_r = DashedLine(PR(-6.0, 23.5), PR(16.0, 23.5), color=WHITE, stroke_width=2, dash_length=0.07)
        ra_r = VMobject(stroke_color=WHITE, stroke_width=2.5, fill_opacity=0)
        ra_r.set_points_as_corners([PR(7.0, 25.2), PR(8.7, 25.2), PR(8.7, 23.5)])
        sig_parts = ([r"\sigma_{\mathrm{inner}}", r"=", r"23.8\ \mathrm{MPa}"], [C_SIG_T, WHITE, C_SIG_T])
        sig_l = mtex(*sig_parts, size=32).move_to([CMP_LEFT_X, 1.65, 0])
        sig_r = mtex(*sig_parts, size=32).move_to([CMP_RIGHT_X, 1.65, 0])
        tag_l = Text(cap("q2_c_flat"), font_size=24, color=C_AVG).move_to([CMP_LEFT_X, -2.95, 0])
        tag_r = Text(cap("q2_c_up"), font_size=24, color=C_SIG_T).move_to([CMP_RIGHT_X, -2.95, 0])
        assume = assume_tag()
        panel = [divider, body_l, *walls_l, path_l, chev_l, icon_r, arrow_r, ref_r, ra_r, sig_l, sig_r, tag_l, tag_r, assume]
        for m in panel:
            m.set_z_index(100)
        self.hud(*panel)
        self.play(FadeOut(model), cap_swap(cap3, cap4), run_time=1.0)                                   # 38-39
        self.set_camera_orientation(phi=PHI0, theta=TH0, zoom=1.0)                                      # the model is gone: reset silently
        self.play(FadeIn(divider), FadeIn(body_l), *[FadeIn(w) for w in walls_l], FadeIn(icon_r), run_time=1.0)    # 39-40
        self.play(Create(path_l), LaggedStart(*[GrowArrow(a) for a in chev_l], lag_ratio=0.25), FadeIn(tag_l),
                  run_time=2.0)                                                                         # 40-42
        self.play(GrowArrow(arrow_r), Create(ref_r), Create(ra_r), FadeIn(tag_r), run_time=2.0)         # 42-44
        self.play(FadeIn(sig_l), FadeIn(sig_r), FadeIn(assume), run_time=1.0)                           # 44-45
        self.play(Indicate(sig_l, color=WHITE, scale_factor=1.15), Indicate(sig_r, color=WHITE, scale_factor=1.15),
                  run_time=1.5)                                                                         # 45-46.5
        self.until(54.0)
        self.mark(54.0, "hand-over to D")
        keep = (icon_r, cap4)
        self.play(*[FadeOut(m) for m in panel if m is not icon_r], FadeOut(ttl), FadeOut(ref), run_time=1.0)
        self.until(55.0)


# =====================================================================================================================
# D -- shear at the base acts ON the layer interfaces; tension versus shear; summary table (2D)
# =====================================================================================================================
BM_X0, BM_LEN, BM_TOP, BM_H = -4.7, 4.8, 1.9, 1.9       # the base seen from the side as a cantilever: root x, length, top y, height
SHEAR_RATIO = 0.55                                      # ASSUMED shear strength = 0.55 x tensile strength (Common Spec 3.2)
GR_X, GR_W = 3.3, 2.6                                   # axis x and peak width of the tau parabola graph
D_BASE_Y, D_UNIT = -2.45, 0.09                          # baseline and screen units per MPa of the bar chart
THUMB_MM, THUMB_C = 0.026, (-6.0, 0.15)                 # the small upright icon kept at the left while the base is examined


def bm_x(mm):
    """J-profile x (mm) -> screen x of the cantilever drawing (root = stem face x 4 mm, free end = tip x 34 mm)."""
    return BM_X0 + (mm - STEM_HW) / (TIP_X0 - STEM_HW) * BM_LEN


def shear_beam():
    """The base as a cantilever: 8 horizontal plates, the 7 interfaces in the bond colour, load F at the cord position,
    a section line, and one tau pair ON every interface (length follows the parabola 1 - eta^2)."""
    ph = BM_H / 8.0
    plates = VGroup(*[Rectangle(width=BM_LEN, height=ph - 0.014, stroke_width=1.2, stroke_color=C_HOOK_EDGE, fill_color=C_HOOK,
                                fill_opacity=(0.9, 0.78)[k % 2]).move_to([BM_X0 + BM_LEN / 2, BM_TOP - (k + 0.5) * ph, 0])
                      for k in range(8)])
    ys = [BM_TOP - (i + 1) * ph for i in range(7)]                 # interface heights, top -> bottom
    ifaces = VGroup(*[Line([BM_X0, y, 0], [BM_X0 + BM_LEN, y, 0], color=C_BOND, stroke_width=2.2) for y in ys])
    wall = Rectangle(width=0.18, height=BM_H + 0.5, stroke_width=0, fill_color=METAL, fill_opacity=0.6)
    wall.move_to([BM_X0 - 0.09, BM_TOP - BM_H / 2, 0])
    hatch = VGroup(*[Line([BM_X0 - 0.18, BM_TOP + 0.2 - 0.25 * k, 0], [BM_X0 - 0.45, BM_TOP + 0.2 - 0.25 * k - 0.3, 0],
                          color=METAL, stroke_width=2) for k in range(9)])
    xc = bm_x(D_CASE_A)
    f_arr = force_arrow([xc, BM_TOP, 0], [xc, BM_TOP - BM_H - 0.8, 0], width=6, tip=0.2)
    weight = Rectangle(width=0.55, height=0.32, stroke_width=1.5, stroke_color=WHITE, fill_color=METAL, fill_opacity=1.0)
    weight.move_to([xc, BM_TOP - BM_H - 0.8 - 0.16, 0])
    f_lab = MathTex("F", font_size=34, color=C_F).move_to([xc + 0.35, BM_TOP - BM_H - 0.45, 0])
    x_s = bm_x(10.0)
    sec_line = DashedLine([x_s, BM_TOP + 0.15, 0], [x_s, BM_TOP - BM_H - 0.15, 0], color=WHITE, stroke_width=2.5, dash_length=0.1)
    taus = VGroup()
    for i, y in enumerate(ys):
        eta = 1.0 - 2.0 * (i + 1) / 8.0
        ln = 0.9 * (1.0 - eta * eta)
        up = force_arrow([x_s - ln / 2, y + 0.045, 0], [x_s + ln / 2, y + 0.045, 0], color=C_TAU, width=3.5, tip=0.09)
        dn = force_arrow([x_s + ln / 2, y - 0.045, 0], [x_s - ln / 2, y - 0.045, 0], color=C_TAU, width=3.5, tip=0.09)
        taus.add(VGroup(up, dn))
    return dict(plates=plates, ifaces=ifaces, wall=wall, hatch=hatch, f_arr=f_arr, weight=weight, f_lab=f_lab,
                sec_line=sec_line, taus=taus, xc=xc)


def shear_diagram(xc):
    """V = F, constant between the root and the load (a block), baseline, guide down from the load."""
    y0, y1 = -1.55, -2.45
    block = Polygon([BM_X0, y0, 0], [xc, y0, 0], [xc, y1, 0], [BM_X0, y1, 0],
                    stroke_color=C_F, stroke_width=3, fill_color=C_F, fill_opacity=0.3)
    base = Line([BM_X0, y0, 0], [BM_X0 + BM_LEN, y0, 0], color=C_REF, stroke_width=2)
    guide = DashedLine([xc, BM_TOP - BM_H - 1.15, 0], [xc, y1, 0], color=C_REF, stroke_width=1.5, dash_length=0.08)
    v_lab = mtex([r"V", r"=", r"F"], [C_F, WHITE, C_F], 38).move_to([(BM_X0 + xc) / 2, (y0 + y1) / 2, 0])
    return block, base, guide, v_lab


def tau_graph():
    """tau over the section height: a parabola, maximum at mid-height; dotted guides tie each interface to its point."""
    y_bot, y_top = BM_TOP - BM_H, BM_TOP
    ymid = (y_bot + y_top) / 2.0
    axis = Line([GR_X, y_bot, 0], [GR_X, y_top, 0], color=C_REF, stroke_width=2)
    para = ParametricFunction(lambda t: np.array([GR_X + GR_W * (1 - t * t), ymid + t * BM_H / 2, 0]),
                              t_range=[-1, 1, 0.05], color=C_TAU, stroke_width=4)
    guides, dots = VGroup(), VGroup()
    for i in range(7):
        y = BM_TOP - (i + 1) * BM_H / 8.0
        eta = (y - ymid) / (BM_H / 2.0)
        xg = GR_X + GR_W * (1 - eta * eta)
        guides.add(DashedLine([BM_X0 + BM_LEN + 0.08, y, 0], [xg, y, 0], color=GRAYTXT, stroke_width=1.2,
                              dash_length=0.06).set_opacity(0.6))
        dots.add(Dot([xg, y, 0], radius=0.05, color=C_TAU))
    lab = mtex([r"\tau_{\max}"], [C_TAU], 34).move_to([GR_X + GR_W + 0.55, ymid, 0])
    return axis, para, guides, dots, lab


class Bars3(VGroup):
    """Live bars on one baseline: items = [(getter, colour, decimals)], xs = bar centres; heights and numbers follow the callables."""

    def __init__(self, items, xs, base_y, unit, bar_w=1.0, num_size=30):
        super().__init__()
        self.unit = unit
        self.bars, self.nums = [], []
        for (get, color, dec), x in zip(items, xs):
            p0 = np.array([x, base_y, 0.0])
            bar = always_redraw(lambda get=get, color=color, p0=p0: self._bar(p0, get(), bar_w, color))
            num = DecimalNumber(get(), num_decimal_places=dec, font_size=num_size, color=WHITE, mob_class=Text)

            def place(m, get=get, p0=p0):
                m.set_value(get())
                m.move_to(p0 + UP * (get() * self.unit + 0.32))
            place(num)
            num.add_updater(place)
            self.bars.append(bar)
            self.nums.append(num)
        self.add(*self.bars, *self.nums)

    def _bar(self, p0, v, w, color):
        h = max(v * self.unit, 0.02)
        r = Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        r.move_to(p0 + UP * h / 2)
        return r

    def stop(self):
        for m in (*self.bars, *self.nums):
            m.clear_updaters()


class HookQ2_D_BaseShear(Beats, SafeScene):
    def construct(self):
        # ============================================================ 0.0-3.0  C's upright icon shrinks to the left, C's sentence becomes the title
        icon_big = upright_icon_2d(MM_CMP, (CMP_RIGHT_X, CMP_CY))
        cap_c = caption_c("q2_c_compare", size=26)
        self.add(icon_big, cap_c)
        ttl, ref = hook_title("q2_d_title", "q2_ref", size=28, ref_size=15)
        icon_small = upright_icon_2d(THUMB_MM, THUMB_C)
        self.mark(0.0, "C's icon shrinks left, its sentence becomes the title")
        self.play(ReplacementTransform(icon_big, icon_small), ReplacementTransform(cap_c, ttl),
                  FadeIn(ref, shift=UP * 0.2), run_time=1.5)
        self.until(3.0)

        # ============================================================ 3.0-20.0  the base as a cantilever: V = F, tau parabola, tau ON the interfaces
        self.mark(3.0, "the base as a cantilever")
        B = shear_beam()
        cap1 = caption_c("q2_d_shear")
        org_s = hook_centre_origin(THUMB_MM, (THUMB_C[0], THUMB_C[1], 0.0))
        ring_s = Circle(radius=0.22, color=C_SIG_T, stroke_width=3)
        ring_s.move_to(org_s + np.array([19 * THUMB_MM, 4 * THUMB_MM, 0]))
        lab_base = Text(cap("q1_lab_base"), font_size=20, color=WHITE).move_to([THUMB_C[0], -1.45, 0])
        self.play(FadeIn(cap1, shift=UP * 0.2), FadeIn(B["plates"]), FadeIn(B["ifaces"]), FadeIn(B["wall"]), FadeIn(B["hatch"]),
                  Create(ring_s), FadeIn(lab_base), GrowArrow(B["f_arr"]), FadeIn(B["weight"]), FadeIn(B["f_lab"]),
                  run_time=1.5)                                                                           # 3.0-4.5
        sd_block, sd_base, sd_guide, sd_lab = shear_diagram(B["xc"])
        self.play(Create(sd_block), Create(sd_base), Create(sd_guide), FadeIn(sd_lab), run_time=2.5)       # 4.5-7.0
        g_axis, g_para, g_guides, g_dots, g_lab = tau_graph()
        self.play(Create(g_axis), Create(g_para), LaggedStart(*[Create(g) for g in g_guides], lag_ratio=0.1),
                  FadeIn(g_dots), FadeIn(g_lab), run_time=3.0)                                            # 7.0-10.0
        self.play(Create(B["sec_line"]), LaggedStart(*[GrowArrow(a) for pr in B["taus"] for a in pr], lag_ratio=0.1),
                  run_time=3.0)                                                                           # 10.0-13.0
        self.play(Indicate(B["ifaces"], color=WHITE, scale_factor=1.0), run_time=1.5)                      # 13.0-14.5
        self.until(20.0)

        # ============================================================ 20.0-40.0  tau_max = 1.5 V / A, then tension against shear
        self.mark(20.0, "tau_max = 1.5 V / A")
        cap2 = caption_c("q2_d_formula", size=24)
        assume = assume_tag()
        beam_grp = VGroup(B["plates"], B["ifaces"], B["wall"], B["hatch"], B["f_arr"], B["weight"], B["f_lab"],
                          B["sec_line"], B["taus"])
        eqa = left_at(mtex([r"\tau_{\max}", r"=", r"1.5", r"\cdot", r"V", r"/", r"A"],
                           [C_TAU, WHITE, WHITE, WHITE, C_F, WHITE, C_AVG], 40), -2.4, 1.5)
        eqb = left_at(mtex([r"=", r"1.5", r"\times", r"100", r"/", r"64", r"=", r"2.34\ \mathrm{MPa}"],
                           [WHITE, WHITE, WHITE, C_F, WHITE, C_AVG, WHITE, C_TAU], 40), -2.4, 0.65)
        gone = [sd_block, sd_base, sd_guide, sd_lab, g_axis, g_para, g_guides, g_dots, g_lab, ring_s, lab_base, icon_small]
        self.play(cap_swap(cap1, cap2), *[FadeOut(m) for m in gone], beam_grp.animate.scale(0.5).move_to([-5.2, 0.9, 0]),
                  run_time=1.0)                                                                           # 20-21
        self.play(FadeIn(eqa, shift=UP * 0.1), FadeIn(assume), run_time=1.0)                               # 21-22
        glow(self, eqa[4], B["f_arr"], C_F, run_time=1.5)                                                  # 22-23.5
        glow(self, eqa[6], B["sec_line"], C_AVG, run_time=1.5)                                             # 23.5-25
        self.play(Write(eqb), run_time=1.5)                                                                # 25-26.5
        self.until(26.5)
        # 26.5-32.5  bars: sigma_inner (follows d) against tau_max
        self.mark(26.5, "bars sigma_inner vs tau_max")
        cap3 = caption_c("q2_d_compare")
        d = ValueTracker(D_CASE_A)
        eq_on = ValueTracker(0.0)
        xs3 = [0.5, 2.7, 4.9]
        bars = Bars3([(lambda: sigma_inner(d.get_value()), C_SIG_T, 1), (lambda: tau_max(), C_TAU, 2)], xs3[:2], D_BASE_Y, D_UNIT)
        bar_eq = Bars3([(lambda: tau_max() / SHEAR_RATIO * eq_on.get_value(), C_TAU, 2)], xs3[2:], D_BASE_Y, D_UNIT)
        base_ln = Line([-0.3, D_BASE_Y, 0], [5.7, D_BASE_Y, 0], color=C_REF, stroke_width=2)
        lab_b1 = mtex([r"\sigma_{\mathrm{inner}}"], [C_SIG_T], 30).move_to([xs3[0], D_BASE_Y - 0.42, 0])
        lab_b2 = mtex([r"\tau_{\max}"], [C_TAU], 30).move_to([xs3[1], D_BASE_Y - 0.42, 0])
        lab_b3 = mtex([r"\tau_{\max}/0.55"], [C_TAU], 30).move_to([xs3[2], D_BASE_Y - 0.42, 0])
        unit_t = Text("MPa", font_size=18, color=GRAYTXT).move_to([-0.75, D_BASE_Y + 0.18, 0])
        lab_r1 = mtex([r"\sigma_{\mathrm{inner}}", r"/", r"\tau_{\max}"], [C_SIG_T, WHITE, C_TAU], 30).move_to([5.5, 0.85, 0])
        lab_r2 = mtex([r"\sigma_{\mathrm{inner}}", r"/", r"(\tau_{\max}/0.55)"], [C_SIG_T, WHITE, C_TAU], 28).move_to([5.5, 0.85, 0])

        def ratio_val():
            s = sigma_inner(d.get_value())
            return s / (tau_max() / SHEAR_RATIO) if eq_on.get_value() > 0.5 else s / tau_max()
        ratio_n = always_redraw(lambda: Text(f"{ratio_val():.1f}×", font_size=48, color=WHITE).move_to([5.5, 0.15, 0]))
        self.play(cap_swap(cap2, cap3), FadeIn(bars), FadeIn(base_ln), FadeIn(lab_b1), FadeIn(lab_b2), FadeIn(unit_t),
                  FadeIn(lab_r1), FadeIn(ratio_n), run_time=1.0)                                          # 26.5-27.5
        self.play(d.animate.set_value(D_CASE_B), run_time=5.0, rate_func=smooth)                           # 27.5-32.5 (d: 19 -> 5)
        # 32.5-36.0  the assumed shear strength turns tau into an equivalent tension
        self.mark(32.5, "assumed shear strength -> equivalent tension")
        cap4 = caption_c("q2_d_assume", size=22)
        self.play(cap_swap(cap3, cap4), FadeIn(bar_eq), FadeIn(lab_b3), FadeOut(lab_r1), run_time=0.8)     # 32.5-33.3
        self.play(eq_on.animate.set_value(1.0), FadeIn(lab_r2), run_time=1.2)                              # 33.3-34.5
        self.play(Indicate(bar_eq.nums[0], color=WHITE, scale_factor=1.25), run_time=1.0)                  # 34.5-35.5
        self.until(36.0)
        # 36.0-40.0  result: both values of the ratio
        self.mark(36.0, "result")
        cap5 = caption_c("q2_d_result", size=24)
        v19 = sigma_inner(D_CASE_A) / (tau_max() / SHEAR_RATIO)
        v5 = sigma_inner(D_CASE_B) / (tau_max() / SHEAR_RATIO)
        res19 = mtex([r"d=19\ \mathrm{mm}:", f"{v19:.1f}" + r"\times"], [C_D, WHITE], 32).move_to([5.3, 1.75, 0])
        res5 = mtex([r"d=5\ \mathrm{mm}:", f"{v5:.1f}" + r"\times"], [C_D, WHITE], 32).move_to([5.3, 1.3, 0])
        self.play(cap_swap(cap4, cap5), FadeIn(res19), FadeIn(res5), run_time=1.5)                         # 36-37.5
        self.play(Indicate(res19, color=WHITE, scale_factor=1.15), Indicate(res5, color=WHITE, scale_factor=1.15),
                  run_time=1.5)                                                                           # 37.5-39
        self.until(40.0)

        # ============================================================ 40.0-55.0  summary table, the test, the sources
        self.mark(40.0, "summary table")
        bars.stop(), bar_eq.stop(), ratio_n.clear_updaters()
        cap6 = caption_c("q2_d_table_title", size=28, color=WHITE)
        colors = {r: {1: C_AVG, 2: C_SIG_T} for r in (1, 2, 3, 4)}
        table = table_mob(TABLE_Q2D, col_w=[4.4, 3.4, 3.4], size=24, row_h=0.62, colors=colors).move_to([0, 0.6, 0])
        test = fit_width(Text(cap("q2_d_test"), font_size=24, color=WHITE), 11.5).move_to([0, -1.85, 0])
        src = fit_width(Text(cap("q2_d_src"), font_size=16, color=GRAYTXT), 13.0).move_to([0, -3.3, 0])
        stage = [beam_grp, eqa, eqb, bars, bar_eq, base_ln, lab_b2, lab_b1, lab_b3, unit_t, lab_r2, ratio_n, res19, res5]
        self.play(cap_swap(cap5, cap6), *[FadeOut(m) for m in stage], run_time=1.0)                        # 40-41
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.2) for row in table], lag_ratio=0.5), run_time=5.0)   # 41-46
        self.play(FadeIn(test, shift=UP * 0.2), run_time=1.5)                                              # 46-47.5
        self.play(FadeIn(src), run_time=1.0)                                                               # 47.5-48.5
        self.until(55.0)
