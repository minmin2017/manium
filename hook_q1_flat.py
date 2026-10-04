# -*- coding: utf-8 -*-
"""Q1 -- flat-printed hook: when you pull the hook down, do the layers slide apart?

Four scenes, one cloud render each:
  HookQ1_A_Setup   (SafeThreeDScene, 55 s)  lying hook -> hanging hook, forces enter every sheet equally
  HookQ1_B_Cards   (SafeScene,       60 s)  deck of cards + layer-by-layer free-body proof
  HookQ1_C_Cases   (SafeScene,       65 s)  when the interface DOES carry load (the part Min got right)
  HookQ1_D_InPlane (SafeScene,       55 s)  residual shear stays inside the layer + the numbers

Plan (the contract): Main_note/Claude_Specs/3DP Hook Q1 Flat Layers Plan.md  -- one row = one QA checkpoint.
All Thai comes from hook_captions.py (cap / CAPS / TABLE_Q1C); no Thai is typed in this file and none goes in MathTex.
Every row start is announced with self.mark(plan_seconds) and every row end is pinned with self.until(plan_seconds)
so the cloud log ([BEAT] lines) proves the render follows the plan's time table.
"""
from hook_common import *


# =====================================================================================================================
# A -- lying hook -> hanging hook (3D)
# =====================================================================================================================
MM3 = 0.04                    # world units per mm in scene A
ZEX = 4.0                     # the 8 mm thickness is drawn 4x thicker so 8 sheets stay legible at 480p (documented)
T_EQ = SEC_B * ZEX            # drawn thickness in mm-equivalents (32)
# NOTE: do NOT use camera frame_center here -- the cairo 3D camera applies it to fixed-in-frame text as well
# (it shifted the title by the same amount). The model is parked with a world offset W0 instead.
W0 = np.array([0.6, 0.0, -0.35])
CAM_LYING = dict(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=1.4)
CAM_HANG = dict(phi=75 * DEGREES, theta=-30 * DEGREES, zoom=1.0)
CORD_C = "#ECEFF1"
Z_BED = -T_EQ / 2 - 0.6


def flat_pt(x, y, z=0.0):
    """J-profile mm (x, y) + stack coordinate z (mm-eq, centred on 0) -> world point, hook lying flat."""
    return W0 + np.array([(x - HOOK_CX) * MM3, (y - HOOK_CY) * MM3, z * MM3])


def stand_pt(x, y, z=0.0):
    """Same point after the hook is rotated +90 deg about X (through W0) to hang: profile y -> up, stack z -> -y."""
    return W0 + np.array([(x - HOOK_CX) * MM3, -z * MM3, (y - HOOK_CY) * MM3])


class HookQ1_A_Setup(Beats, SafeThreeDScene):
    # ---------------------------------------------------------------- small helpers
    def hud_text(self, txt, size=22, color=WHITE, pos=None, z=100):
        m = Text(txt, font_size=size, color=color)
        if pos is not None:
            m.move_to([pos[0], pos[1], 0])
        m.set_z_index(z)
        self.hud(m)
        return m

    def caption_hud(self, key, size=24):
        m = caption_c(key, size=size)
        m.set_z_index(100)
        self.hud(m)
        return m

    def label_to(self, key, world_pt, at, size=22, color=WHITE, leader_color=GRAYTXT):
        lab, arr = hud_label(self, cap(key), world_pt, at=at, size=size, color=color, leader_color=leader_color)
        lab.set_z_index(100)
        arr.set_z_index(99)
        return lab, arr

    # ---------------------------------------------------------------- scene
    def construct(self):
        self.set_camera_orientation(**CAM_LYING)

        # ============================================================ 0.0-3.0  title + page ref
        ttl, ref = hook_title("q1_title", "q1_ref", size=28, ref_size=15)
        ttl.set_z_index(100), ref.set_z_index(100)
        self.hud(ttl, ref)
        self.mark(0.0, "title")
        self.play(FadeIn(ttl, shift=UP * 0.4), FadeIn(ref, shift=UP * 0.4), run_time=1.0)
        self.until(3.0)

        # ============================================================ 3.0-9.0  question card + small lying hook
        self.mark(3.0, "question card")
        q = Text(cap("q1_question"), font_size=36, color=WHITE)
        frame = SurroundingRectangle(q, color=METAL, buff=0.45, corner_radius=0.25, stroke_width=3)
        card = VGroup(frame, q).move_to([1.3, 0.0, 0])
        icon = hook_profile(0.022, origin=hook_centre_origin(0.022, (-4.6, 0.0, 0.0)), opacity=0.9)
        card.set_z_index(100), icon.set_z_index(100)
        self.hud(card, icon)
        self.play(FadeIn(card, shift=UP * 0.3), FadeIn(icon, shift=UP * 0.3), run_time=1.0)
        self.until(8.0)
        self.play(FadeOut(card, shift=DOWN * 0.2), FadeOut(icon, shift=DOWN * 0.2), run_time=1.0)
        self.until(9.0)

        # ============================================================ 9.0-15.0  bed, 8 sheets stack up, axes
        self.mark(9.0, "bed + stack")
        bed = Polygon(*[flat_pt(x, y, Z_BED) for x, y in [(-11, -7), (49, -7), (49, 97), (-11, 97)]],
                      color=METAL, fill_color=METAL, fill_opacity=0.35, stroke_width=1.5)
        bed.set_z_index(0)
        sheets = make_hook_sheets(N_SHOW, "flat", MM3, ZEX, origin=hook_centre_origin(MM3, W0))
        for i, s in enumerate(sheets):
            s.set_z_index(1 + i)
        zt = sheets.z_levels[-1]
        cap1 = self.caption_hud("q1_a_stack")
        self.play(FadeIn(bed, shift=OUT * 0.2), FadeIn(cap1, shift=UP * 0.2), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, shift=OUT * 0.25) for s in sheets], lag_ratio=0.25, run_time=3.0))
        # axis legend (triad parked bottom-left): X, Y in the plane of the layer (grey), Z = stacking direction (yellow)
        o = world_at_screen(self, (-4.4, -1.9), z=Z_BED * MM3 + W0[2])
        ax_x = arrow3(o, o + np.array([16, 0, 0]) * MM3, GRAYTXT, thickness=0.02, height=0.2)
        ax_y = arrow3(o, o + np.array([0, 16, 0]) * MM3, GRAYTXT, thickness=0.02, height=0.2)
        ax_z = arrow3(o, o + np.array([0, 0, 30]) * MM3, C_D, thickness=0.02, height=0.2)
        for a in (ax_x, ax_y, ax_z):
            a.set_z_index(20)
        self.play(GrowArrow(ax_x), GrowArrow(ax_y), GrowArrow(ax_z), run_time=1.0)
        tags = []
        for ch, a, col in (("X", ax_x, GRAYTXT), ("Y", ax_y, GRAYTXT), ("Z", ax_z, C_D)):
            m = self.hud_text(ch, 22, col)
            p = cam_point(self, a.get_end())
            d = p - cam_point(self, a.get_start())
            d = d / (np.linalg.norm(d[:2]) + 1e-9)
            m.move_to([p[0] + d[0] * 0.3, p[1] + d[1] * 0.3, 0])
            tags.append(m)
        lab_xy = self.hud_text(cap("q1_ax_xy"), 20, GRAYTXT)
        lab_z = self.hud_text(cap("q1_ax_z"), 20, C_D)
        po = cam_point(self, o)
        lab_xy.move_to([po[0] - 0.3 + lab_xy.width / 2, po[1] - 0.8, 0])
        lab_z.move_to([po[0] - 0.25 - lab_z.width / 2, po[1] + 0.9, 0])
        self.play(*[FadeIn(m) for m in tags], FadeIn(lab_xy), FadeIn(lab_z), run_time=0.6)
        self.until(15.0)

        # ============================================================ 15.0-19.0  name the parts (arrows + labels)
        self.mark(15.0, "name the parts")
        parts = []
        for key, wp, at in [("q1_lab_stem", flat_pt(0, 24, zt), (-3.0, 0.7)),
                            ("q1_lab_base", flat_pt(18, 4, zt), (-0.5, -3.5)),      # the J's base BAR (top sheet), not the bed
                            ("q1_lab_tip", flat_pt(38, 26, zt), (3.3, -0.3)),
                            ("q1_lab_eye", flat_pt(0, 76.5, zt), (-1.1, 1.8))]:
            lab, arr = self.label_to(key, wp, at)
            parts += [lab, arr]
        self.play(*[FadeIn(m) for m in parts], run_time=1.5)
        self.until(18.0)
        self.play(*[FadeOut(m) for m in parts], run_time=1.0)
        self.until(19.0)

        # ============================================================ 19.0-27.0  one layer = ? -> 8 mm = 40 layers
        self.mark(19.0, "layer count")
        cap2 = self.caption_hud("q1_a_layer")
        self.play(cap_swap(cap1, cap2), Indicate(sheets[-1], color=WHITE, scale_factor=1.0), run_time=1.5)
        # brace along the left edge of the stem: the stack's 8 sheets are visible there as stripes
        p_top = cam_point(self, flat_pt(-4, 22, T_EQ / 2))
        p_bot = cam_point(self, flat_pt(-4, 22, -T_EQ / 2))
        brace = BraceBetweenPoints(np.array([p_bot[0] - 0.08, p_bot[1], 0]), np.array([p_top[0] - 0.08, p_top[1], 0]),
                                   direction=LEFT, color=C_D)
        brace.set_z_index(100)
        dim = Text("8 mm", font_size=22, color=C_D)
        dim.next_to(brace, LEFT, buff=0.12).set_z_index(100)
        self.hud(brace, dim)
        lay_lab, lay_arr = self.label_to("q1_lab_layer", flat_pt(38, 34, zt), (3.3, 0.8))
        self.play(FadeIn(brace, shift=LEFT * 0.2), FadeIn(dim, shift=LEFT * 0.2), FadeIn(lay_lab), FadeIn(lay_arr),
                  run_time=2.0)
        self.until(25.5)
        self.play(FadeOut(brace), FadeOut(dim), FadeOut(lay_lab), FadeOut(lay_arr), run_time=1.5)
        self.until(27.0)

        # ============================================================ 27.0-41.0  rotate the hook to hang it
        self.mark(27.0, "hang it")
        cap3 = self.caption_hud("q1_a_hang")
        self.play(FadeOut(bed), FadeOut(ax_x), FadeOut(ax_y), FadeOut(ax_z), *[FadeOut(m) for m in tags],
                  FadeOut(lab_xy), FadeOut(lab_z), cap_swap(cap2, cap3), run_time=1.0)
        # +PI/2 about X (right-hand rule): profile y -> world up, so the eye ends on top (the plan text says -PI/2,
        # which would hang the eye DOWN -- see report)
        self.play(Rotate(sheets, angle=PI / 2, axis=RIGHT, about_point=W0, run_time=4.0, rate_func=smooth))
        self.move_camera(**CAM_HANG, run_time=3.0)
        eye_c = stand_pt(0, EYE_C[1])
        yb = (T_EQ / 2 + 7) * MM3
        rod = Line(np.array([eye_c[0], yb, eye_c[2]]), np.array([eye_c[0], -yb, eye_c[2]]), color=METAL, stroke_width=26)
        rod.set_z_index(30)
        g_arrow = arrow3(stand_pt(58, 68), stand_pt(58, 40), C_F, thickness=0.03, height=0.22)
        g_arrow.set_z_index(30)
        g_lab = self.hud_text("g", 24, C_F)
        pg = cam_point(self, stand_pt(58, 54))
        g_lab.move_to([pg[0] + 0.3, pg[1], 0])
        self.play(FadeIn(rod, shift=np.array([0, 0.9, 0])), GrowArrow(g_arrow), FadeIn(g_lab), run_time=2.0)
        self.until(41.0)

        # ============================================================ 41.0-52.0  forces enter every sheet
        self.mark(41.0, "forces")
        cap4 = self.caption_hud("q1_a_inplane")
        zs = sheets.z_levels
        # cord laid across the FULL thickness on the base's top face, strands down the faces, weight below
        y_f, y_b = -(T_EQ / 2 + 1.5) * MM3, (T_EQ / 2 + 1.5) * MM3
        xc = stand_pt(19, 0)[0]
        z_top = stand_pt(0, BASE_T)[2] + 0.02
        z_wt = stand_pt(0, -12)[2]
        cord_top = Line([xc, y_f, z_top], [xc, y_b, z_top], color=CORD_C, stroke_width=7)
        strand_f = Line([xc, y_f, z_top], [xc, y_f, z_wt], color=CORD_C, stroke_width=3)
        strand_b = Line([xc, y_b, z_top], [xc, y_b, z_wt], color=CORD_C, stroke_width=3)
        cord = VGroup(cord_top, strand_f, strand_b)
        cord.set_z_index(31)
        weight = Prism(dimensions=[0.6, (y_b - y_f) + 0.1, 0.55]).set_fill(METAL, 1.0).set_stroke(WHITE, 1.0)
        weight.move_to([xc, 0.0, z_wt - 0.275])
        arrows_up = VGroup(*[arrow3(stand_pt(0, 82, z), stand_pt(0, 98, z), C_F, thickness=0.012, height=0.1) for z in zs])
        arrows_dn = VGroup(*[arrow3(stand_pt(19, BASE_T, z), stand_pt(19, -7, z), C_F, thickness=0.012, height=0.1) for z in zs])
        for a in list(arrows_up) + list(arrows_dn):
            a.set_z_index(40)
        self.play(cap_swap(cap3, cap4),
                  LaggedStart(FadeIn(cord), FadeIn(weight),
                              *[GrowArrow(a) for a in arrows_up], *[GrowArrow(a) for a in arrows_dn],
                              lag_ratio=0.08, run_time=2.5), run_time=2.5)
        # the plane of the J (all forces lie in it) + names for rod / cord / weight, each with its leader
        plane = Polygon(stand_pt(-12, -6, 0), stand_pt(48, -6, 0), stand_pt(48, 96, 0), stand_pt(-12, 96, 0),
                        color=C_SIG_C, fill_color=C_SIG_C, fill_opacity=0.15, stroke_width=1.5)
        plane.set_z_index(12)
        rod_l = np.array([eye_c[0], -yb, eye_c[2]])         # -Y end = nearest the camera = screen-left end
        names = []
        for key, wp, at in [("q1_lab_rod", rod_l, (-3.2, 1.35)),
                            ("q1_lab_cord", np.array([xc, y_b, z_top]), (-3.2, -1.9)),
                            ("q1_lab_weight", np.array([xc - 0.3, 0.0, z_wt - 0.3]), (-2.4, -3.3))]:
            lab, arr = self.label_to(key, wp, at)
            names += [lab, arr]
        self.play(Create(plane), *[FadeIn(m) for m in names], run_time=1.5)
        self.play(Indicate(rod, color=WHITE, scale_factor=1.0), Indicate(cord, color=WHITE, scale_factor=1.0),
                  run_time=1.5)
        self.until(52.0)

        # ============================================================ 52.0-55.0  bridge to B
        self.mark(52.0, "bridge")
        self.play(FadeOut(Group(*self.mobjects), shift=DOWN * 0.3), run_time=1.0)
        bridge = Text(cap("q1_a_bridge"), font_size=40, color=WHITE).move_to([0, 0.3, 0])
        self.hud(bridge)
        self.play(FadeIn(bridge, shift=UP * 0.2), run_time=1.0)
        self.until(55.0)


# =====================================================================================================================
# B -- deck of cards + layer-by-layer proof (2D)
# =====================================================================================================================
BRIDGE_POS = [0, 0.3, 0]                 # A ends with q1_a_bridge here, B starts with it (continuity)
DECK_Y = -1.3                            # y of the card centres in the two-deck comparison
EQ_FINAL_POS = [0, 0.3, 0]               # B ends with F_interface = 0 here, C starts with it


def eq_final():
    """The result equation that B hands over to C (identical object/position/size in both scenes)."""
    m = MathTex(r"F_{\mathrm{interface}}", r"=", r"0", font_size=56)
    m[0].set_color(C_TAU)
    m[2].set_color(C_AVG)
    return m.move_to(EQ_FINAL_POS)


def oblique_rack(mm=0.032, centre=(2.7, -0.55), step=(0.115, 0.045), n=N_SHOW):
    """The hook as a rack of n J-sheets in a cabinet-style oblique view (depth runs up-right): sheets, rod through
    the eye holes, cord laid across the full thickness on the base, one equal force arrow per sheet at rod and cord."""
    org = hook_centre_origin(mm, (centre[0], centre[1], 0.0))

    def pt(k, x, y):
        return np.array([org[0] + x * mm + step[0] * k, org[1] + y * mm + step[1] * k, 0.0])
    sheets = VGroup()
    for k in reversed(range(n)):                       # far sheet first, near sheet last (painter's order)
        sheets.add(hook_profile(mm, org + np.array([step[0] * k, step[1] * k, 0.0]), opacity=(0.85, 0.75)[k % 2],
                                stroke_width=1.4))
    rod = Line(pt(-0.9, 0, EYE_C[1]), pt(n - 0.1, 0, EYE_C[1]), color=METAL, stroke_width=11)
    cord = Line(pt(-0.35, 19, BASE_T + 0.4), pt(n - 0.65, 19, BASE_T + 0.4), color=C_CORD, stroke_width=7)
    ups = VGroup(*[force_arrow(pt(k, 0, EYE_C[1] + EYE_RI), pt(k, 0, EYE_C[1] + EYE_RI + 20), width=3.5, tip=0.1)
                   for k in range(n)])
    dns = VGroup(*[force_arrow(pt(k, 19, BASE_T), pt(k, 19, -11), width=3.5, tip=0.1) for k in range(n)])
    return sheets, rod, cord, ups, dns, pt


class HookQ1_B_Cards(Beats, SafeScene):
    def construct(self):
        # ============================================================ 0.0-3.0  bridge -> title (continuity from A)
        bridge = Text(cap("q1_a_bridge"), font_size=40, color=WHITE).move_to(BRIDGE_POS)
        self.add(bridge)
        ttl, ref = hook_title("q1_b_title", "q1_ref", size=28, ref_size=15)
        self.mark(0.0, "bridge -> title")
        self.play(ReplacementTransform(bridge, ttl), FadeIn(ref, shift=UP * 0.2), run_time=1.5)
        self.until(3.0)

        # ============================================================ 3.0-19.0  left deck: pull ALL cards equally
        self.mark(3.0, "equal pull")
        cap1 = caption_c("q1_b_equal")
        deck = Deck().move_to([0, DECK_Y, 0])
        ups = pull_arrows(deck)
        x_l, x_r = deck.get_left()[0] - 0.3, deck.get_right()[0] + 0.3
        y0 = deck.cards[0].get_top()[1]
        ghost = DashedLine([x_l, y0, 0], [x_r, y0, 0], color=C_REF, stroke_width=1.6, dash_length=0.12)
        ghost.set_stroke(opacity=0.6)
        self.play(FadeIn(cap1, shift=UP * 0.2),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in deck.cards], lag_ratio=0.2), run_time=2.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.1), FadeIn(ghost), run_time=1.5)
        self.play(VGroup(deck, ups).animate.shift(UP * 0.8), run_time=2.5)
        y1 = y0 + 0.8
        ref_line = DashedLine([x_l, y1, 0], [x_r, y1, 0], color=WHITE, stroke_width=2.5, dash_length=0.14)
        tick = check_mark([x_r + 0.5, y1, 0], size=0.34)
        self.play(Create(ref_line), run_time=0.5)
        self.play(Indicate(ref_line, color=WHITE, scale_factor=1.0), FadeIn(tick, scale=1.4), run_time=1.5)
        self.until(19.0)

        # ============================================================ 19.0-35.0  right deck: pull ONE card
        self.mark(19.0, "one card")
        cap2 = caption_c("q1_b_unequal")
        deck_l = VGroup(deck, ups, ghost, ref_line, tick)
        self.play(cap_swap(cap1, cap2), deck_l.animate.scale(0.6).to_edge(LEFT, buff=0.5).shift(DOWN * 1.41), run_time=1.5)
        deck_r = Deck().move_to([2.6, DECK_Y, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in deck_r.cards], lag_ratio=0.15), run_time=1.5)
        c4 = deck_r.card(3)
        one = force_arrow(c4.get_top() + UP * 0.04, c4.get_top() + UP * 0.84)
        self.play(GrowArrow(one), run_time=1.0)
        self.play(VGroup(c4, one).animate.shift(UP * 0.8), run_time=2.5)
        # shear tau across the two interfaces of the pulled card: neighbour face dragged UP, pulled card face DOWN
        lo, hi = deck_r.card(2).get_bottom()[1] + 0.8, deck_r.card(2).get_top()[1]
        ys = [lo + (hi - lo) * f for f in (0.2, 0.5, 0.8)]
        x_a, x_b = deck_r.iface_x(2), deck_r.iface_x(3)
        taus = VGroup(*[shear_pair(x_a, y, UP, length=0.5, width=4.0, tip=0.12) for y in ys],
                      *[shear_pair(x_b, y, DOWN, length=0.5, width=4.0, tip=0.12) for y in ys])
        self.play(LaggedStart(*[GrowArrow(a) for pr in taus for a in pr], lag_ratio=0.08), run_time=2.0)
        tag = Text(cap("q1_c_tag_shear"), font_size=22, color=C_TAU)
        tag.move_to([x_b + 0.9, DECK_Y - 1.65, 0])
        lead = Line(tag.get_top() + UP * 0.05, [x_b + 0.07, ys[0] - 0.25, 0], color=C_TAU, stroke_width=2)
        self.play(FadeIn(tag, shift=UP * 0.15), Create(lead), run_time=0.5)
        self.until(35.0)

        # ============================================================ 35.0-45.0  link to the hook
        self.mark(35.0, "link to the hook")
        cap3 = caption_c("q1_b_link")
        sheets, rod, cord, h_ups, h_dns, hpt = oblique_rack()
        right_deck = VGroup(deck_r, one, taus, tag, lead)
        self.play(cap_swap(cap2, cap3), FadeOut(right_deck, shift=DOWN * 0.3), FadeIn(sheets, shift=UP * 0.3),
                  FadeIn(rod), FadeIn(cord), run_time=1.5)
        lab_rod = Text(cap("q1_lab_rod"), font_size=20, color=WHITE).move_to([-0.8, 1.45, 0])
        lab_cord = fit_width(Text(cap("q1_lab_cord"), font_size=20, color=WHITE), 3.7).move_to([4.95, -2.35, 0])
        arr_rod = Arrow(lab_rod.get_right() + RIGHT * 0.08, hpt(-0.5, 0, EYE_C[1]), buff=0.05, color=GRAYTXT, stroke_width=2,
                        tip_length=0.14, max_tip_length_to_length_ratio=0.5)
        arr_cord = Arrow(lab_cord.get_left() + LEFT * 0.08, hpt(6.2, 19, BASE_T + 0.4), buff=0.05, color=GRAYTXT,
                         stroke_width=2, tip_length=0.14, max_tip_length_to_length_ratio=0.5)
        self.play(*[GrowArrow(a) for a in list(h_ups) + list(h_dns)], FadeIn(lab_rod), FadeIn(lab_cord),
                  Create(arr_rod), Create(arr_cord), run_time=1.5)
        self.play(Indicate(rod, color=WHITE, scale_factor=1.0), Indicate(cord, color=WHITE, scale_factor=1.0),
                  Indicate(VGroup(h_ups, h_dns), color=WHITE, scale_factor=1.0), Indicate(ups, color=WHITE, scale_factor=1.0),
                  run_time=2.0)
        self.until(45.0)

        # ============================================================ 45.0-60.0  free-body proof, one layer
        self.mark(45.0, "proof")
        ass = Text(cap("q1_b_assume"), font_size=20, color=GRAYTXT).move_to([0, -3.65, 0])
        ptitle = caption_c("q1_b_proof_title", size=26, color=WHITE)
        core = VGroup(deck, ups)
        big = Rectangle(width=0.8, height=2.0, stroke_width=2.5, stroke_color=C_HOOK_EDGE, fill_color=C_HOOK,
                        fill_opacity=0.9).move_to([-1.8, -0.35, 0])
        f_up = force_arrow(big.get_top() + UP * 0.04, big.get_top() + UP * 0.9, width=5, tip=0.18)
        f_dn = force_arrow(big.get_bottom() + DOWN * 0.9, big.get_bottom() + DOWN * 0.04, width=5, tip=0.18)
        t_up = MathTex(r"F/n", font_size=34, color=C_F).next_to(f_up, RIGHT, buff=0.12)
        t_dn = MathTex(r"F/n", font_size=34, color=C_F).next_to(f_dn, RIGHT, buff=0.12)
        side_l = DashedLine(big.get_corner(UL) + LEFT * 0.35, big.get_corner(DL) + LEFT * 0.35, color=C_TAU,
                            stroke_width=2.5, dash_length=0.12)
        side_r = DashedLine(big.get_corner(UR) + RIGHT * 0.35, big.get_corner(DR) + RIGHT * 0.35, color=C_TAU,
                            stroke_width=2.5, dash_length=0.12)
        joints = VGroup(side_l, side_r)
        x0 = 0.55                                           # left edge of the equation column
        ys_t = [1.9, 0.85, -0.2, -1.25]

        def step_text(key, y):
            t = fit_width(Text(cap(key), font_size=22, color=WHITE), 6.3)      # cloud font is ~19% wider: fit, never overflow
            return t.move_to([x0, y, 0]).align_to([x0, 0, 0], LEFT)

        def put_eq(eq, y):
            return eq.move_to([x0, y - 0.5, 0]).align_to([x0, 0, 0], LEFT)
        st = [step_text(f"q1_b_step{i + 1}", ys_t[i]) for i in range(4)]
        eq1 = MathTex(r"F_{i}", r"=", r"F", r"/", r"n", font_size=44)
        eq2 = MathTex(r"100", r"/", r"40", r"=", r"2.5\ \mathrm{N}", font_size=44)
        eq3 = MathTex(r"\Sigma F", r"=", r"F/n", r"-", r"F/n", font_size=44)
        eq4 = MathTex(r"F_{\mathrm{interface}}", r"=", r"0", font_size=44)
        for eq, cols in ((eq1, [C_F, WHITE, C_F, WHITE, C_REF]), (eq2, [C_F, WHITE, C_REF, WHITE, C_F]),
                         (eq3, [WHITE, WHITE, C_F, WHITE, C_F]), (eq4, [C_TAU, WHITE, C_AVG])):
            for part, col in zip(eq, cols):
                part.set_color(col)
        for eq, y in ((eq1, ys_t[0]), (eq2, ys_t[1]), (eq3, ys_t[2]), (eq4, ys_t[3])):
            put_eq(eq, y)
        for m in st:
            m.align_to([x0, 0, 0], LEFT)
        gone = [lab_rod, lab_cord, arr_rod, arr_cord, sheets, rod, cord, h_ups, h_dns, ghost, ref_line, tick]
        # step 1 (45-48): isolate layer i -- its own two arrows -- then F and n of  F_i = F/n
        self.play(cap_swap(cap3, ptitle), FadeOut(*gone), FadeIn(ass), core.animate.move_to([-5.0, 0.3, 0]),
                  run_time=0.5)
        self.play(TransformFromCopy(deck.card(3), big), GrowArrow(f_up), GrowArrow(f_dn), FadeIn(t_up), FadeIn(t_dn),
                  FadeIn(st[0], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(eq1, shift=UP * 0.1), run_time=0.3)
        glow(self, eq1[2], list(ups), C_F, run_time=0.85)
        glow(self, eq1[4], list(deck.cards), C_REF, run_time=0.85)
        # step 2 (48-51)
        self.mark(48.0, "step 2")
        self.play(FadeIn(st[1], shift=UP * 0.1), FadeIn(eq2, shift=UP * 0.1), run_time=0.3)
        glow(self, eq2[0], list(ups), C_F, run_time=0.9)
        glow(self, eq2[2], list(deck.cards), C_REF, run_time=0.9)
        glow(self, eq2[4], f_up, C_F, run_time=0.9)
        # step 3 (51-54)
        self.mark(51.0, "step 3")
        self.play(FadeIn(st[2], shift=UP * 0.1), FadeIn(eq3, shift=UP * 0.1), run_time=0.3)
        glow(self, eq3[0], big, WHITE, run_time=0.9)
        glow(self, eq3[2], f_up, C_F, run_time=0.9)
        glow(self, eq3[4], f_dn, C_F, run_time=0.9)
        # step 4 (54-57)
        self.mark(54.0, "step 4")
        self.play(FadeIn(st[3], shift=UP * 0.1), FadeIn(eq4, shift=UP * 0.1), FadeIn(joints), run_time=0.3)
        glow(self, eq4[0], list(joints), C_TAU, run_time=1.35)
        glow(self, eq4[2], list(joints), C_AVG, run_time=1.35)
        # result (57-60)
        self.mark(57.0, "result")
        result = Text(cap("q1_b_result"), font_size=24, color=C_AVG).move_to([0, -3.0, 0])
        box = SurroundingRectangle(eq4, color=C_AVG, buff=0.14, stroke_width=3)
        self.play(Write(result), Create(box), run_time=1.5)
        self.until(59.0)
        # hand over to C: everything fades except the result equation, which moves to centre and grows
        self.mark(59.0, "hand-over")
        keep = eq_final()
        others = [m for m in self.mobjects if m not in (eq4, box)]
        self.play(*[FadeOut(m) for m in others], FadeOut(box), ReplacementTransform(eq4, keep), run_time=1.0)
        self.until(60.0)


# =====================================================================================================================
# C -- when the interface DOES carry load (2D)
# =====================================================================================================================
def q1c_table(size=24):
    """TABLE_Q1C as rows (0 = header); the same object is rebuilt in D so row 1 hands over seamlessly."""
    colors = {1: {1: C_AVG, 2: C_AVG}, 2: {1: WARN, 2: WARN}, 3: {1: WARN, 2: WARN}, 4: {1: WARN, 2: WARN}}
    return table_mob(TABLE_Q1C, col_w=[4.6, 2.2, 3.6], size=size, row_h=0.7, colors=colors).move_to([0, 0.35, 0])


def beam_strips(R, L=5.4, n=N_SHOW, t=0.22, pitch=0.27, x0=-3.2, y_mid=0.1, npts=28, opac=(0.9, 0.78)):
    """n horizontal strips (i = 0 top ... n-1 bottom) clamped at x0 and bent about a centre R below the beam.
    Every strip keeps its own length L (a loose stack, like a bent deck of cards): end angle phi_i = L / R_i, so the
    strip ends slip against each other. R = 1e6 gives the straight beam with the SAME point count (clean Transform)."""
    strips = VGroup()
    cx, cy = x0, y_mid - R
    for i in range(n):
        h = ((n - 1) / 2 - i) * pitch
        Ri = R + h
        th = np.linspace(0.0, L / Ri, npts)
        outer = np.stack([cx + (Ri + t / 2) * np.sin(th), cy + (Ri + t / 2) * np.cos(th), np.zeros(npts)], 1)
        inner = np.stack([cx + (Ri - t / 2) * np.sin(th), cy + (Ri - t / 2) * np.cos(th), np.zeros(npts)], 1)[::-1]
        m = VMobject()
        m.set_points_as_corners(np.concatenate([outer, inner, outer[:1]], 0))
        m.set_fill(C_HOOK, opacity=opac[i % 2]).set_stroke(C_HOOK_EDGE, width=1.4)
        strips.add(m)
    return strips


def beam_pt(R, i, theta_frac, n=N_SHOW, pitch=0.27, L=5.4, x0=-3.2, y_mid=0.1, off=0.0):
    """Point on strip i's centre line (off = radial offset) at a fraction of that strip's own end angle; also returns
    the polar angle."""
    h = ((n - 1) / 2 - i) * pitch
    Ri = R + h + off
    th = theta_frac * L / (R + h)
    return np.array([x0 + Ri * np.sin(th), y_mid - R + Ri * np.cos(th), 0.0]), th


class HookQ1_C_Cases(Beats, SafeScene):
    def construct(self):
        # ============================================================ 0.0-3.0  result of B -> new question
        eq = eq_final()
        self.add(eq)
        ttl, ref = hook_title("q1_c_title", "q1_ref", size=28, ref_size=15)
        self.mark(0.0, "F_interface = 0 -> title")
        self.play(TransformFromCopy(eq, ttl), FadeIn(ref, shift=UP * 0.2), run_time=1.5)
        self.until(3.0)

        # ============================================================ 3.0-19.0  case 1: only a few layers are loaded
        self.mark(3.0, "case 1")
        cap1 = caption_c("q1_c_case1")
        deck = Deck().move_to([0, -0.5, 0])
        ups = pull_arrows(deck, length=0.32)                       # the rod pulls every card equally (F/8 each)
        big_dn = VGroup(*[force_arrow(deck.card(i).get_bottom() + DOWN * 0.04, deck.card(i).get_bottom() + DOWN * 1.24,
                                      width=7, tip=0.24) for i in (0, 7)])   # the cord loads the 2 outer cards (F/2 each)
        self.play(FadeOut(eq, shift=UP * 0.4), FadeIn(cap1, shift=UP * 0.2),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in deck.cards], lag_ratio=0.15), run_time=1.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.1), run_time=1.0)
        self.play(*[GrowArrow(a) for a in big_dn], run_time=1.5)
        outer = [VGroup(deck.card(0), big_dn[0], ups[0]), VGroup(deck.card(7), big_dn[1], ups[7])]
        self.play(*[g.animate.shift(DOWN * 0.4) for g in outer], run_time=2.5)
        # shear across the joints: 3, 2, 1, 0, 1, 2, 3 (x F/8) -- the force has to flow inward through the interfaces
        mags = [3, 2, 1, 0, 1, 2, 3]
        taus = VGroup()
        for i in (0, 6, 1, 5, 2, 4):
            lo = max(deck.card(i).get_bottom()[1], deck.card(i + 1).get_bottom()[1])
            hi = min(deck.card(i).get_top()[1], deck.card(i + 1).get_top()[1])
            for f in (0.3, 0.7):
                taus.add(shear_pair(deck.iface_x(i), lo + (hi - lo) * f, UP if i < 3 else DOWN,
                                    length=0.22 * mags[i], width=4.0, tip=0.11))
        self.play(LaggedStart(*[GrowArrow(a) for pr in taus for a in pr], lag_ratio=0.2), run_time=3.0)
        tag1 = Text(cap("q1_c_tag_shear"), font_size=22, color=WARN).move_to([0, -3.1, 0])
        lead1 = Line(tag1.get_top() + UP * 0.05, [deck.iface_x(2) + 0.07, -1.75, 0], color=WARN, stroke_width=2)
        self.play(FadeIn(tag1, shift=UP * 0.15), Create(lead1), run_time=0.5)
        self.until(19.0)

        # ============================================================ 19.0-36.0  case 2: pull across the layers
        self.mark(19.0, "case 2")
        cap2 = caption_c("q1_c_case2")
        self.play(cap_swap(cap1, cap2), FadeOut(taus), FadeOut(big_dn), FadeOut(ups), FadeOut(tag1), FadeOut(lead1),
                  *[g[0].animate.shift(UP * 0.4) for g in outer], run_time=1.5)
        ys_b = [deck.card(0).get_bottom()[1] + 2.2 * (j + 0.5) / 5 for j in range(5)]
        c6, c7 = deck.card(6), deck.card(7)

        def bond67(y):
            def mk():
                a = np.array([c6.get_right()[0], y, 0.0])
                b = np.array([c7.get_left()[0], y, 0.0])
                s = float(np.clip((b[0] - a[0] - 0.22) / 1.2, 0, 1))
                col = interpolate_color(ManimColor(C_BOND), ManimColor(WARN), s)
                return VGroup(Line(a, b, color=col, stroke_width=3.5), Dot(a, radius=0.05, color=col),
                              Dot(b, radius=0.05, color=col))
            return always_redraw(mk)
        static_bonds = VGroup(*[VGroup(Line([deck.card(i).get_right()[0], y, 0], [deck.card(i + 1).get_left()[0], y, 0],
                                            color=C_BOND, stroke_width=3.5),
                                       Dot([deck.card(i).get_right()[0], y, 0], radius=0.05, color=C_BOND),
                                       Dot([deck.card(i + 1).get_left()[0], y, 0], radius=0.05, color=C_BOND))
                                for i in range(6) for y in ys_b])
        live_bonds = VGroup(*[bond67(y) for y in ys_b])
        self.mark(20.5, "bonds appear")
        self.play(LaggedStart(FadeIn(static_bonds), FadeIn(live_bonds), lag_ratio=0.3), run_time=1.5)
        self.play(Indicate(static_bonds, color=WHITE, scale_factor=1.0), Indicate(live_bonds, color=WHITE, scale_factor=1.0),
                  run_time=1.5)
        self.until(26.5)
        pull = force_arrow(c7.get_right(), c7.get_right() + RIGHT * 1.0, width=7, tip=0.24)
        self.play(GrowArrow(pull), run_time=1.5)
        self.mark(28.0, "stretch")
        self.play(VGroup(c7, pull).animate.shift(RIGHT * 1.2), run_time=3.0, rate_func=linear)
        self.mark(31.0, "break")
        pts_flash = [np.array([(c6.get_right()[0] + c7.get_left()[0]) / 2, y, 0.0]) for y in ys_b]
        for m in live_bonds:
            m.clear_updaters()
        self.play(*[Flash(p, color=WARN, flash_radius=0.3, line_length=0.16, num_lines=10) for p in pts_flash],
                  FadeOut(live_bonds), run_time=1.0)
        self.play(VGroup(c7, pull).animate.shift(RIGHT * 0.8), run_time=1.0, rate_func=rush_from)
        tag2 = Text(cap("q1_c_tag_peel"), font_size=22, color=WARN).move_to([c6.get_right()[0] + 0.9, -2.55, 0])
        lead2 = Line(tag2.get_top() + UP * 0.05, [c6.get_right()[0] + 0.5, -1.2, 0], color=WARN, stroke_width=2)
        self.play(FadeIn(tag2, shift=UP * 0.15), Create(lead2), run_time=0.5)
        self.until(36.0)

        # ============================================================ 36.0-51.0  case 3: bend out of the plane
        self.mark(36.0, "case 3")
        cap3 = caption_c("q1_c_case3")
        R_B = 9.0
        flat = beam_strips(1e6)
        bent = beam_strips(R_B)
        wall = Rectangle(width=0.3, height=3.0, stroke_width=0, fill_color=METAL, fill_opacity=0.55).move_to([-3.35, 0.1, 0])
        hatch = VGroup(*[Line([-3.5, 0.1 + 1.5 - 0.3 * k, 0], [-3.9, 0.1 + 1.5 - 0.3 * k + 0.4, 0], color=METAL, stroke_width=2)
                         for k in range(11)])
        self.play(cap_swap(cap2, cap3), FadeOut(static_bonds), FadeOut(pull), FadeOut(tag2), FadeOut(lead2),
                  Transform(deck.cards, flat), FadeIn(wall), FadeIn(hatch), run_time=1.5)
        tip_flat = np.array([-3.2 + 5.4, 0.1 + 3.5 * 0.27 + 0.11, 0])
        f_pt, _ = beam_pt(R_B, 0, 1.0, off=0.11)
        f_arr = force_arrow(tip_flat + UP * 1.0, tip_flat + UP * 0.06, width=7, tip=0.24)
        self.play(GrowArrow(f_arr), run_time=1.0)
        self.mark(38.5, "bend")
        self.play(Transform(deck.cards, bent), f_arr.animate.shift(f_pt - tip_flat), run_time=3.5)
        taus3 = VGroup()
        for j in range(N_SHOW - 1):
            p, th = beam_pt(R_B, j, 0.6, off=-0.135)                 # on the interface between strip j and j+1
            nrm = np.array([np.sin(th), np.cos(th), 0.0])
            tg = np.array([np.cos(th), -np.sin(th), 0.0])
            taus3.add(VGroup(force_arrow(p + nrm * 0.05 - tg * 0.2, p + nrm * 0.05 + tg * 0.2, C_TAU, 3.5, 0.1),
                             force_arrow(p - nrm * 0.05 + tg * 0.2, p - nrm * 0.05 - tg * 0.2, C_TAU, 3.5, 0.1)))
        self.play(LaggedStart(*[GrowArrow(a) for pr in taus3 for a in pr], lag_ratio=0.06), run_time=2.0)
        tag3 = Text(cap("q1_c_tag_shear"), font_size=22, color=WARN).move_to([3.6, -2.7, 0])
        p_t, _ = beam_pt(R_B, 4, 0.6, off=-0.135)
        lead3 = Line(tag3.get_left() + LEFT * 0.05, p_t + RIGHT * 0.1, color=WARN, stroke_width=2)
        self.play(FadeIn(tag3, shift=UP * 0.15), Create(lead3), run_time=0.5)
        self.until(51.0)

        # ============================================================ 51.0-65.0  summary table
        self.mark(51.0, "table")
        cap4 = caption_c("q1_c_table_title", size=28, color=WHITE)
        table = q1c_table()
        self.play(cap_swap(cap3, cap4), FadeOut(deck.cards), FadeOut(taus3), FadeOut(f_arr), FadeOut(wall), FadeOut(hatch),
                  FadeOut(tag3), FadeOut(lead3), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.2) for row in table], lag_ratio=0.5), run_time=6.0)
        box = SurroundingRectangle(table[1][0], color=C_AVG, buff=0.12, stroke_width=3)
        self.play(Create(box), run_time=1.5)
        foot = Text(cap("q1_c_foot"), font_size=24, color=C_AVG).move_to([0, -2.3, 0])
        self.play(FadeIn(foot, shift=UP * 0.2), run_time=1.0)
        self.until(64.0)
        # hand over to D: only row 1 (the in-plane case) stays on screen
        self.mark(64.0, "hand-over")
        self.play(FadeOut(table[0]), FadeOut(table[2]), FadeOut(table[3]), FadeOut(table[4]), FadeOut(foot),
                  FadeOut(ttl), FadeOut(ref), FadeOut(cap4), run_time=1.0)
        self.until(65.0)


# =====================================================================================================================
# D -- the shear that remains lives INSIDE the layer, plus the numbers (2D)
# =====================================================================================================================
MM_D = 0.058                      # world units per mm in the big top view of one layer
J_CY = -0.78                      # screen y of the J's bounding-box centre in the big view
SLIDE = 3.9                       # the big view slides left by this much when the magnifier arrives
WALL_OFFS = (0.0, 0.85, 1.7)      # mm inward from the outline: 3 wall loops (drawn ~2x the real pitch so they read at 480p;
                                  # they must stay < 2 mm = radius of the tip corners, or the offset loops invert)
INFILL_OFF = 1.95                 # mm: the infill region starts just inside the last wall loop
LOAD_OFF = 0.85                   # mm: the tension load path runs along the middle wall loop
ICON_MM = 0.036                   # the small hook icon of the numbers part
ICON_C = (-4.9, -0.55)
SUM_X = 1.9                       # centre x of the three summary statements
ASSUME_Y = -3.65                  # the 'assumed example' tag stays here from the moment numbers appear


def wall_loop(off, mm, org, **style):
    """One wall loop = the outline offset `off` mm inward, plus the same offset around the eye hole (2 sub-paths)."""
    outer, hole = hook_outline_mm()
    m = loop_mob(offset_loop(outer, off), mm, org, **style)
    m.append_points(loop_mob(offset_loop(hole, off), mm, org, **style).points)
    return m


def hatch_mob(loops, mm, org, spacing=2.2, angles=(45.0, -45.0), **style):
    """Infill lines as ONE VMobject with many sub-paths (hundreds of Line objects would make the fade slow)."""
    m = VMobject(**style)
    for ang in angles:
        for p0, p1 in hatch_segments(loops, angle_deg=ang, spacing=spacing):
            m.start_new_path(org + np.array([p0[0] * mm, p0[1] * mm, 0.0]))
            m.add_line_to(org + np.array([p1[0] * mm, p1[1] * mm, 0.0]))
    return m


def top_view_layer(mm, org):
    """One printed layer seen from above, as separate mobjects so the scene can reveal them one by one: faint body,
    3 wall loops, +/-45 degree infill, tension load path (+ chevrons) along the middle wall loop, marker on the inner
    fillet, the two force arrows (rod up in the eye, cord down on the base)."""
    outer, hole = hook_outline_mm()

    def P(x, y):
        return org + np.array([x * mm, y * mm, 0.0])

    body = hook_profile(mm, org, color=C_HOOK, opacity=0.16, stroke_color=C_HOOK, stroke_width=0)
    walls = [wall_loop(o, mm, org, stroke_color=C_HOOK, stroke_width=2.4) for o in WALL_OFFS]
    infill = hatch_mob([offset_loop(outer, INFILL_OFF), offset_loop(hole, INFILL_OFF)], mm, org,
                       stroke_color=C_HOOK, stroke_width=1.3, stroke_opacity=0.4)
    # load path: from the cord side along the base, round the inner fillet (centre (6, 10), radius 2 + offset), up the stem
    r = R_INNER + LOAD_OFF
    cen = np.array([STEM_HW + R_INNER, BASE_T + R_INNER])
    ang = np.linspace(-np.pi / 2, -np.pi, 16)
    arc = np.stack([cen[0] + r * np.cos(ang), cen[1] + r * np.sin(ang)], axis=1)
    pts = np.concatenate([[[17.0, BASE_T - LOAD_OFF]], arc, [[STEM_HW - LOAD_OFF, 34.0]]], axis=0)
    scr = np.stack([org[0] + pts[:, 0] * mm, org[1] + pts[:, 1] * mm, np.zeros(len(pts))], axis=1)
    path = VMobject(stroke_color=C_SIG_T, stroke_width=4.5, stroke_opacity=0.9, fill_opacity=0)
    path.set_points_as_corners(scr)
    seg = np.linalg.norm(np.diff(scr, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    chevrons = VGroup()
    for s_mm in (4.5, 13.0, 22.0, 31.0):                  # distance along the path (mm): base, fillet, stem, stem
        s = s_mm * mm
        i = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(seg) - 1))
        p = scr[i] + (s - cum[i]) / seg[i] * (scr[i + 1] - scr[i])
        u = (scr[i + 1] - scr[i]) / seg[i]
        chevrons.add(Arrow(p - u * 0.17, p + u * 0.17, buff=0, color=C_SIG_T, stroke_width=5, tip_length=0.17,
                           max_tip_length_to_length_ratio=0.5))
    ring = Circle(radius=0.17, color=C_SIG_T, stroke_width=3.5).move_to(P(4.6, 8.6))
    f_cord = force_arrow(P(19.0, BASE_T), P(19.0, -6.0), color=C_F, width=5, tip=0.14)
    f_rod = force_arrow(P(0.0, 77.0), P(0.0, 81.4), color=C_F, width=4, tip=0.1)
    return dict(body=body, walls=walls, infill=infill, path=path, chevrons=chevrons, ring=ring, f_cord=f_cord,
                f_rod=f_rod)


def magnifier_cone(c1, r1, c2, r2, color=GRAYTXT, width=2):
    """External tangents of two circles (small one on the part, big one = the inset): the classic magnifier cone."""
    c1, c2 = np.asarray(c1, float)[:2], np.asarray(c2, float)[:2]
    v = c2 - c1
    dist = float(np.hypot(v[0], v[1]))
    u = v / dist
    n = np.array([-u[1], u[0]])
    k = (r1 - r2) / dist
    s = float(np.sqrt(1.0 - k * k))
    out = VGroup()
    for sg in (1.0, -1.0):
        m = k * u + sg * s * n
        a, b = c1 + r1 * m, c2 + r2 * m
        out.add(Line([a[0], a[1], 0.0], [b[0], b[1], 0.0], color=color, stroke_width=width))
    return out


def inset_strands(c, w=2.3, h=0.5):
    """Two neighbouring strands (stadium shapes, fused along their contact line) + the thin bond line with dots."""
    c = np.asarray(c, float)
    kw = dict(width=w, height=h, corner_radius=h / 2 - 0.01, stroke_color=C_HOOK_EDGE, stroke_width=2,
              fill_color=C_HOOK, fill_opacity=0.85)
    top = RoundedRectangle(**kw).move_to(c + UP * (h / 2 - 0.02))
    bot = RoundedRectangle(**kw).move_to(c + DOWN * (h / 2 - 0.02))
    bond = VGroup(Line(c + LEFT * 0.95, c + RIGHT * 0.95, color=C_BOND, stroke_width=3),
                  *[Dot(c + RIGHT * x, radius=0.045, color=C_BOND) for x in (-0.95, -0.475, 0.0, 0.475, 0.95)])
    return top, bot, bond


class HookQ1_D_InPlane(Beats, SafeScene):
    def construct(self):
        # ============================================================ 0.0-3.0  row 1 of C's table -> title (continuity from C)
        table = q1c_table()
        row1 = table[1]
        box = SurroundingRectangle(row1[0], color=C_AVG, buff=0.12, stroke_width=3)
        self.add(row1, box)
        ttl, ref = hook_title("q1_d_title", "q1_ref", size=28, ref_size=15)
        self.mark(0.0, "row 1 of C -> title")
        self.play(TransformFromCopy(row1, ttl), FadeIn(ref, shift=UP * 0.2), run_time=1.5)
        self.until(3.0)

        # ============================================================ 3.0-20.0  one layer seen from above
        self.mark(3.0, "one layer from above")
        org = hook_centre_origin(MM_D, (0.0, J_CY, 0.0))
        V = top_view_layer(MM_D, org)
        body, walls, infill, path = V["body"], V["walls"], V["infill"], V["path"]
        chevrons, ring, f_cord, f_rod = V["chevrons"], V["ring"], V["f_cord"], V["f_rod"]
        cap1 = caption_c("q1_d_inplane")
        # 3.0-6.0 the table row goes first (no overlap with the layer), then the layer appears (faint body + the two
        # force arrows), then the 3 wall loops in turn
        self.play(FadeOut(row1, shift=DOWN * 0.3), FadeOut(box, shift=DOWN * 0.3), FadeIn(cap1, shift=UP * 0.2),
                  run_time=0.6)
        self.play(FadeIn(body), FadeIn(f_cord), FadeIn(f_rod), run_time=0.6)
        self.play(LaggedStart(*[Create(w) for w in walls], lag_ratio=0.5), run_time=1.8)
        self.until(6.0)
        # 6.0-8.0 the +/-45 degree infill
        self.play(FadeIn(infill), run_time=2.0)
        self.until(8.0)
        # 8.0-13.5 strands + the tension path round the inner fillet
        self.mark(8.0, "strands + tension path")
        cap2 = caption_c("q1_d_strands")
        self.play(cap_swap(cap1, cap2), Indicate(VGroup(*walls), color=WHITE, scale_factor=1.0), run_time=1.0)
        self.play(Create(path), LaggedStart(*[GrowArrow(a) for a in chevrons], lag_ratio=0.25), run_time=2.0)
        self.until(11.0)
        self.play(Create(ring), run_time=0.5)
        self.play(Flash(ring.get_center(), color=C_SIG_T, flash_radius=0.3, line_length=0.14, num_lines=10), run_time=0.8)
        self.until(13.5)
        # 13.5-20.0 the layer slides left; magnifier on the base: two neighbouring strands and the shear tau between them
        self.mark(13.5, "magnifier")
        cap3 = caption_c("q1_d_infill")
        j_items = [body, *walls, infill, path, *chevrons, ring, f_cord, f_rod]
        self.play(cap_swap(cap2, cap3), *[m.animate.shift(LEFT * SLIDE) for m in j_items], run_time=0.8)
        org2 = org + np.array([-SLIDE, 0.0, 0.0])
        sc = org2 + np.array([39.5 * MM_D, 2.2 * MM_D, 0.0])                 # small circle: the base, bottom-right
        bc = np.array([2.2, -1.9, 0.0])                                      # the inset
        sr, br = 0.2, 1.8
        circ_s = Circle(radius=sr, color=GRAYTXT, stroke_width=2.5).move_to(sc)
        circ_b = Circle(radius=br, color=GRAYTXT, stroke_width=2.5).move_to(bc)
        cone = magnifier_cone(sc, sr, bc, br)
        top_s, bot_s, bond = inset_strands(bc)
        tau_up = force_arrow(bc + LEFT * 0.7 + UP * 0.17, bc + RIGHT * 0.7 + UP * 0.17, color=C_TAU, width=5, tip=0.16)
        tau_dn = force_arrow(bc + RIGHT * 0.7 + DOWN * 0.17, bc + LEFT * 0.7 + DOWN * 0.17, color=C_TAU, width=5, tip=0.16)
        tau_lab = MathTex(r"\tau", font_size=44, color=C_TAU).move_to(bc + RIGHT * 1.45)
        self.play(Indicate(infill, color=WHITE, scale_factor=1.0), Create(circ_s), Create(cone), run_time=0.8)
        self.play(FadeIn(circ_b), FadeIn(top_s), FadeIn(bot_s), FadeIn(bond), run_time=1.0)
        self.play(GrowArrow(tau_up), GrowArrow(tau_dn), Write(tau_lab), run_time=1.5)
        self.until(18.5)
        self.play(Indicate(VGroup(tau_up, tau_dn), color=WHITE, scale_factor=1.0), run_time=1.0)
        self.until(20.0)

        # ============================================================ 20.0-40.0  the numbers (assumed example)
        self.mark(20.0, "numbers")
        cap4 = caption_c("q1_d_numbers")
        org_i = hook_centre_origin(ICON_MM, (ICON_C[0], ICON_C[1], 0.0))

        def ipt(x, y):
            return org_i + np.array([x * ICON_MM, y * ICON_MM, 0.0])
        d = ValueTracker(D_CASE_A)
        icon = hook_profile(ICON_MM, org_i, opacity=0.9)
        axis_i = DashedLine(ipt(0, BASE_T + 1.0), ipt(0, 36.0), color=C_REF, stroke_width=2, dash_length=0.08)
        cord = always_redraw(lambda: force_arrow(ipt(d.get_value(), BASE_T), ipt(d.get_value(), -7.0), color=C_F,
                                                 width=5, tip=0.13))

        def dim_mk():
            x, y = d.get_value(), BASE_T + 4.0
            return VGroup(Line(ipt(0, y), ipt(x, y), color=C_D, stroke_width=5),
                          Line(ipt(0, y - 1.6), ipt(0, y + 1.6), color=C_D, stroke_width=3),
                          Line(ipt(x, y - 1.6), ipt(x, y + 1.6), color=C_D, stroke_width=3),
                          Line(ipt(x, BASE_T), ipt(x, y), color=C_D, stroke_width=2))
        dim = always_redraw(dim_mk)
        d_txt = always_redraw(lambda: Text(f"d = {d.get_value():.0f} mm", font_size=26, color=C_D)
                              .move_to([ICON_C[0], -2.85, 0]))
        bars = BarPair(lambda: sigma_inner(d.get_value()), lambda: tau_max(), C_SIG_T, C_TAU, base=[1.6, -2.45, 0],
                       unit=0.14, bar_w=1.2, gap=2.9, num_size=34, decimals=1, decimals_b=2)
        lab_s = fit_width(Text(cap("q1_d_bar_sigma"), font_size=22, color=WHITE), 2.6).move_to(bars.ax + DOWN * 0.4)
        lab_t = fit_width(Text(cap("q1_d_bar_tau"), font_size=22, color=WHITE), 2.6).move_to(bars.bx + DOWN * 0.4)
        r_lab = MathTex(r"\sigma", r"/", r"\tau", font_size=44)
        r_lab[0].set_color(C_SIG_T)
        r_lab[2].set_color(C_TAU)
        r_lab.move_to([5.55, 0.75, 0])
        ratio = always_redraw(lambda: Text(f"{sigma_inner(d.get_value()) / tau_max():.1f}×", font_size=52, color=WHITE)
                              .move_to([5.55, -0.15, 0]))
        ass = Text(cap("q1_b_assume"), font_size=20, color=GRAYTXT).move_to([0, ASSUME_Y, 0])
        # 20.0-21.5 the big top view shrinks into the small hook icon, every detail of it leaves
        detail = [*walls, infill, path, *chevrons, ring, f_cord, f_rod, circ_s, circ_b, cone, top_s, bot_s, bond,
                  tau_up, tau_dn, tau_lab]
        self.play(cap_swap(cap3, cap4), ReplacementTransform(body, icon), *[FadeOut(m) for m in detail], run_time=1.5)
        # 21.5-23.0 bars, labels, and the live d marker on the icon (ONE ValueTracker drives numbers, bars and picture)
        self.play(FadeIn(bars, shift=UP * 0.2), FadeIn(lab_s), FadeIn(lab_t), FadeIn(ass), FadeIn(axis_i), FadeIn(cord),
                  FadeIn(dim), FadeIn(d_txt), FadeIn(r_lab), FadeIn(ratio), run_time=1.5)
        self.until(23.0)
        self.mark(23.0, "numbers at d = 19")
        self.play(Indicate(bars.num_a, color=WHITE, scale_factor=1.25), run_time=1.2)
        self.play(Indicate(bars.num_b, color=WHITE, scale_factor=1.25), run_time=1.2)
        self.play(Indicate(ratio, color=WHITE, scale_factor=1.15), run_time=1.2)
        self.until(27.0)
        self.mark(27.0, "d: 19 -> 5")
        self.play(d.animate.set_value(D_CASE_B), run_time=6.0, rate_func=smooth)
        self.until(33.0)
        self.mark(33.0, "conclusion")
        cap5 = caption_c("q1_d_conclude")
        self.play(cap_swap(cap4, cap5), run_time=1.0)
        self.play(Indicate(ratio, color=WHITE, scale_factor=1.15), run_time=1.5)
        self.until(40.0)

        # ============================================================ 40.0-55.0  summary: 3 statements, 5 s each
        self.mark(40.0, "summary")
        bars.stop()
        ratio.clear_updaters()
        line1 = caption_c("q1_d_conclude", size=28, color=C_AVG, max_w=9.4, y=1.05).shift(RIGHT * SUM_X)
        self.play(ReplacementTransform(cap5, line1), FadeOut(bars, shift=DOWN * 0.2), FadeOut(lab_s), FadeOut(lab_t),
                  FadeOut(r_lab), FadeOut(ratio), run_time=1.0)
        self.until(45.0)
        self.mark(45.0, "final")
        line2 = caption_c("q1_d_final", size=28, color=C_AVG, max_w=9.4, y=-0.35).shift(RIGHT * SUM_X)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.8)
        self.until(50.0)
        self.mark(50.0, "caveat")
        line3 = caption_c("q1_d_caveat", size=28, color=WARN, max_w=9.4, y=-1.65).shift(RIGHT * SUM_X)
        self.play(FadeIn(line3, shift=UP * 0.2), run_time=0.8)
        self.until(55.0)

