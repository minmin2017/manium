"""
exam_dfa_1109.py -- Mechanics of Machinery, exam 9 Nov 2026, topic 4: Dynamic force analysis.

Every number comes from the verified note (checker: powerfull_note/tools/slider_crank_dfa.py):
  Exam_Prep/Mechanics of Machinery/สอบ 9 พ.ย. — Dynamic Force Analysis.md

D40_ExamDFAMethod   -- the 5-step method on the slider-crank (Fig 10.9), unknown count 8 = 8
D41_ExamDFASP106    -- Sample Problem 10.6 worked on the FBD, T1 = 0.308 N m (ccw)
D42_ExamDFABarDrill -- practice 1: single bar pinned at O, F_O = (-23.21, -3.01) N, T = 2.40 N m

Geometry is the real SP 10.6 slider-crank: r = 0.05, r_G = 0.025, l = 0.094, l_G = 0.047 m, phi = 70 deg.
"""

import numpy as np
from manim import *
from mlib import *

L1_C = "#4FC3F7"     # crank (1)
L2_C = "#81C784"     # rod (2)
L3_C = "#FFB74D"     # slider (3)
UNK_C = "#EF5350"    # unknown joint forces
INR_C = "#CE93D8"    # D'Alembert inertia terms
ACC_C = "#FFD54F"    # accelerations
ALP_C = "#FF8A65"    # angular accelerations
W_C = "#80DEEA"      # angular velocity
TQ_C = "#FFF176"     # driving torque T1
DIM_C = GRAYTXT

R_, RG_, L_, LG_ = 0.05, 0.025, 0.094, 0.047
PHI0 = 70 * DEGREES
K = 55                                   # drawing units per metre
O_I = np.array([-4.1, -0.9, 0.0])        # crank pivot during the turning intro
O_A = np.array([-5.6, -2.6, 0.0])        # crank pivot on the assembled figure
O1E = np.array([-5.9, -2.7, 0.0])        # exploded FBD anchors
BRE = np.array([-2.9, 1.2, 0.0])
CSE = np.array([4.2, -2.2, 0.0])
PX = 1.25                                # left edge of the right-hand panel


def P2(x, y):
    return np.array([x, y, 0.0])


def U(deg):
    a = deg * DEGREES
    return np.array([np.cos(a), np.sin(a), 0.0])


def T(txt, size=20, color=WHITE):
    return Text(txt, font_size=size, color=color)


def M(tex, size=30, color=WHITE):
    return MathTex(tex, font_size=size, color=color)


def MP(*parts, size=30, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def row(*ms, buff=0.22, max_w=5.55):
    return fit_width(VGroup(*ms).arrange(RIGHT, buff=buff), max_w)


def place_left(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


def prow(mob, i, y0=2.0, dy=0.6, x=PX, max_w=5.55):
    fit_width(mob, max_w)
    return place_left(mob, x, y0 - dy * i)


def arc_arrow(center, r, start, sweep, color, sw=4):
    a = Arc(radius=r, start_angle=start * DEGREES, angle=sweep * DEGREES, arc_center=center,
            color=color, stroke_width=sw)
    a.add_tip(tip_length=0.16, tip_width=0.16)
    return a


def geo(phi, O, k=K):
    O = np.asarray(O, dtype=float)
    B = O + k * R_ * np.array([np.cos(phi), np.sin(phi), 0.0])
    th = np.arcsin(R_ * np.sin(phi) / L_)
    C = B + k * L_ * np.array([np.cos(th), -np.sin(th), 0.0])
    return O, B, C, O + (B - O) * RG_ / R_, B + (C - B) * LG_ / L_, th


def gdot(p):
    return Circle(radius=0.08, color=WHITE, stroke_width=2.5).set_fill(BLACK, 1).move_to(p)


def pin(p):
    return Dot(p, radius=0.07, color=WHITE)


def pieces(phi, O, k=K, ground=True):
    """(crank, rod, slider, ground) as separate groups so they can be pulled apart."""
    O, B, C, G1, G2, th = geo(phi, O, k)
    crank = VGroup(Line(O, B, color=L1_C, stroke_width=9), pin(O), pin(B), gdot(G1))
    rod = VGroup(Line(B, C, color=L2_C, stroke_width=9), pin(B), pin(C), gdot(G2))
    slider = VGroup(Rectangle(width=1.0, height=0.6, color=L3_C, fill_opacity=0.35,
                              stroke_width=3).move_to(C), pin(C))
    gnd = VGroup()
    if ground:
        y = C[1] - 0.3
        x0, x1 = O[0] + k * 0.03, O[0] + k * 0.155
        gnd.add(Line([x0, y, 0], [x1, y, 0], color=GRAYTXT, stroke_width=3))
        for x in np.arange(x0 + 0.2, x1, 0.32):
            gnd.add(Line([x, y, 0], [x - 0.14, y - 0.14, 0], color=GRAYTXT, stroke_width=2))
        gnd.add(Polygon(O, O + P2(-0.22, -0.32), O + P2(0.22, -0.32), color=GRAYTXT,
                        stroke_width=3))
    return VGroup(crank, rod, slider, gnd)


def farrow(p, vec, color, tex, ldir, size=26, end_at_p=False, sw=5, lab_at="tip"):
    p = np.asarray(p, dtype=float)
    vec = np.asarray(vec, dtype=float)
    tail, tip = (p - vec, p) if end_at_p else (p, p + vec)
    a = Arrow(tail, tip, buff=0, color=color, stroke_width=sw, tip_length=0.2,
              max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12)
    anchor = {"tip": tip, "tail": tail, "mid": (tail + tip) / 2}[lab_at]
    lab = M(tex, size, color).next_to(anchor, ldir, buff=0.1)
    return VGroup(a, lab)


def tag(n, color):
    c = Circle(radius=0.2, color=color, stroke_width=2.5)
    return VGroup(c, Text(str(n), font_size=20, color=color).move_to(c))


# ---------------------------------------------------------------- assembled figure (at O_A)
def point_labels():
    O, B, C, G1, G2, th = geo(PHI0, O_A)
    return dict(
        O=M("O_1", 26).move_to(O + P2(0.45, -0.5)),
        B=M("B", 26).next_to(B, UP, buff=0.15),
        C=M("C", 26).move_to(C + P2(0, 0.62)),
        G1=M("G_1", 24).move_to(G1 + 0.42 * U(-20)),
        G2=M("G_2", 24).move_to(G2 + 0.44 * U(-120)),
        G3=M("G_3", 24).move_to(C + P2(0.8, 0.5)),
    )


def link_tags():
    O, B, C, G1, G2, th = geo(PHI0, O_A)
    return VGroup(tag(1, L1_C).move_to((G1 + B) / 2 + 0.45 * U(-20)),
                  tag(2, L2_C).move_to((G2 + C) / 2 + 0.5 * U(60)),
                  tag(3, L3_C).move_to(C + P2(0.85, -0.05)))


def angle_marks():
    O, B, C, G1, G2, th = geo(PHI0, O_A)
    href1 = DashedLine(O, O + P2(1.2, 0), color=GRAYTXT, stroke_width=2)
    pa = Arc(radius=0.55, start_angle=0, angle=PHI0, arc_center=O, color=WHITE, stroke_width=3)
    pl = M(r"\phi", 28).move_to(O + 0.85 * U(35))
    href2 = DashedLine(C, C + P2(-1.6, 0), color=GRAYTXT, stroke_width=2)
    ta = Arc(radius=1.0, start_angle=PI - th, angle=th, arc_center=C, color=WHITE, stroke_width=3)
    tl = M(r"\theta", 28).move_to(C + 1.5 * U(168))
    return VGroup(href1, pa, pl), VGroup(href2, ta, tl)


def accel_marks():
    """a_G arrows (directions of SP 10.6) and alpha arcs, labels placed clear of the links."""
    O, B, C, G1, G2, th = geo(PHI0, O_A)
    d1 = np.array([-1.79, -1.99, 0]); d2 = np.array([-2.65, -2.0, 0])
    aG1 = farrow(G1, 0.75 * d1 / np.linalg.norm(d1), ACC_C, r"\vec a_{G1}", LEFT)
    aG2 = farrow(G2, 0.8 * d2 / np.linalg.norm(d2), ACC_C, r"\vec a_{G2}", LEFT)
    aG3 = farrow(C, P2(-0.8, 0), ACC_C, r"\vec a_{G3}", LEFT)
    al1 = VGroup(arc_arrow(O, 0.9, 10, 45, ALP_C), M(r"\alpha_1", 26, ALP_C).move_to(O + 1.2 * U(28)))
    al2 = VGroup(arc_arrow(G2, 0.5, 20, 100, ALP_C), M(r"\alpha_2", 26, ALP_C).move_to(G2 + 0.8 * U(70)))
    return aG1, aG2, aG3, al1, al2


def inertia_marks():
    O, B, C, G1, G2, th = geo(PHI0, O_A)
    d1 = np.array([1.79, 1.99, 0]); d2 = np.array([2.65, 2.0, 0])
    Fi1 = farrow(G1, 0.75 * d1 / np.linalg.norm(d1), INR_C, r"\vec F_{i1}", RIGHT)
    Fi2 = farrow(G2, 0.8 * d2 / np.linalg.norm(d2), INR_C, r"\vec F_{i2}", RIGHT)
    Fi3 = farrow(C, P2(0.8, 0), INR_C, r"\vec F_{i3}", RIGHT)
    Ci1 = VGroup(arc_arrow(O, 0.9, 55, -45, INR_C), M(r"C_{i1}", 26, INR_C).move_to(O + 1.25 * U(25)))
    Ci2 = VGroup(arc_arrow(G2, 0.5, 120, -100, INR_C), M(r"C_{i2}", 26, INR_C).move_to(G2 + 0.85 * U(70)))
    return Fi1, Fi2, Fi3, Ci1, Ci2


def mass_labels():
    O, B, C, G1, G2, th = geo(PHI0, O_A)
    return VGroup(M(r"m_1,\ I_{G1}", 24, L1_C).move_to((G1 + B) / 2 + 0.95 * U(160)),
                  M(r"m_2,\ I_{G2}", 24, L2_C).move_to(P2(-1.0, -0.15)),
                  M(r"m_3", 24, L3_C).move_to(C + P2(1.05, 1.0)))


# ---------------------------------------------------------------- exploded FBD
def fbd(num=False):
    """FBD of the three links (Fig 10.9b). Unknowns red, drawn +x / +y / ccw.
    num=True: inertia terms labelled with the SP 10.6 values instead of symbols."""
    o, b, c, g1, g2, th = geo(PHI0, O1E)
    O1, Bc, G1 = O1E, b, g1
    Br = BRE
    Cr = Br + (c - b)
    G2 = Br + (g2 - b)
    Cs = CSE
    crank = VGroup(Line(O1, Bc, color=L1_C, stroke_width=9), pin(O1), pin(Bc), gdot(G1))
    rod = VGroup(Line(Br, Cr, color=L2_C, stroke_width=9), pin(Br), pin(Cr), gdot(G2))
    slider = VGroup(Rectangle(width=1.1, height=0.7, color=L3_C, fill_opacity=0.35,
                              stroke_width=3).move_to(Cs), pin(Cs))
    names = VGroup(M("O_1", 24).move_to(O1 + P2(0.05, -0.4)),
                   M("B", 24).next_to(Bc, LEFT, buff=0.18),
                   M("B", 24).next_to(Br, LEFT, buff=0.36),
                   M("C", 24).next_to(Cr, DOWN, buff=0.18))
    tags = VGroup(VGroup(tag(1, L1_C), T("ข้อเหวี่ยง", 20, L1_C)).arrange(RIGHT, buff=0.15).move_to(P2(-5.9, 1.55)),
                  VGroup(tag(2, L2_C), T("ก้านสูบ", 20, L2_C)).arrange(RIGHT, buff=0.15).move_to(P2(-0.9, 2.05)),
                  VGroup(tag(3, L3_C), T("สไลเดอร์", 20, L3_C)).arrange(RIGHT, buff=0.15).move_to(P2(5.75, -1.45)))
    s = 0.85
    il = (dict(i1x=r"0.895\,\text{N}", i1y=r"0.995\,\text{N}", c1=r"-0.05\,\text{N m}",
               i2x=r"2.65\,\text{N}", i2y=r"2.0\,\text{N}", c2=r"-0.115\,\text{N m}",
               i3=r"2.625\,\text{N}") if num else
          dict(i1x=r"-m_1a_{G1x}", i1y=r"-m_1a_{G1y}", c1=r"-I_{G1}\alpha_1",
               i2x=r"-m_2a_{G2x}", i2y=r"-m_2a_{G2y}", c2=r"-I_{G2}\alpha_2", i3=r"-m_3a_{G3}"))
    F = {}
    F["F01x"] = farrow(O1, P2(s, 0), UNK_C, "F_{01x}", DOWN)
    F["F01y"] = farrow(O1, P2(0, s), UNK_C, "F_{01y}", LEFT)
    t1 = arc_arrow(O1, 0.45, 100, 120, TQ_C)
    F["T1"] = VGroup(t1, M("T_1", 26, TQ_C).next_to(O1 + 0.45 * U(160), LEFT, buff=0.22))
    F["F21x"] = farrow(Bc, P2(s, 0), UNK_C, "F_{21x}", RIGHT)
    F["F21y"] = farrow(Bc, P2(0, s), UNK_C, "F_{21y}", UP)
    F["i1x"] = farrow(G1, P2(0.7, 0), INR_C, il["i1x"], RIGHT, size=24)
    F["i1y"] = farrow(G1, P2(0, 0.7), INR_C, il["i1y"], LEFT, size=24)
    c1 = arc_arrow(G1, 0.38, 275, 70, INR_C)
    F["c1"] = VGroup(c1, M(il["c1"], 24, INR_C).move_to(G1 + 0.62 * U(310) + P2(0.35, -0.12)))
    F["F12x"] = farrow(Br, P2(0.9, 0), UNK_C, "F_{12x}", RIGHT)
    F["F12y"] = farrow(Br, P2(0, s), UNK_C, "F_{12y}", LEFT)
    F["F32x"] = farrow(Cr, P2(0.9, 0), UNK_C, "F_{32x}", RIGHT)
    F["F32y"] = farrow(Cr, P2(0, s), UNK_C, "F_{32y}", RIGHT)
    F["i2x"] = farrow(G2, P2(0.8, 0), INR_C, il["i2x"], RIGHT, size=24)
    F["i2y"] = farrow(G2, P2(0, 0.8), INR_C, il["i2y"], RIGHT, size=24)
    c2 = arc_arrow(G2, 0.42, 190, 100, INR_C)
    F["c2"] = VGroup(c2, M(il["c2"], 24, INR_C).move_to(G2 + 0.8 * U(240) + P2(-0.25, -0.05)))
    F["F23x"] = farrow(Cs, P2(0.95, 0), UNK_C, "F_{23x}", LEFT, end_at_p=True, lab_at="tail")
    F["F23y"] = farrow(Cs, P2(0, s), UNK_C, "F_{23y}", UP)
    F["F03y"] = farrow(Cs + P2(0, -0.35), P2(0, 0.95), UNK_C, "F_{03y}", RIGHT, end_at_p=True,
                       lab_at="mid")
    F["i3"] = farrow(Cs, P2(0.9, 0), INR_C, il["i3"], RIGHT, size=24)
    return dict(crank=crank, rod=rod, slider=slider, names=names, tags=tags, F=F,
                O1=O1, Bc=Bc, Br=Br, Cr=Cr, Cs=Cs, G1=G1, G2=G2)


def ring(p, lab, ldir=DOWN):
    c = Circle(radius=0.24, color=WHITE, stroke_width=4).move_to(p)
    return c


class ExamScene(SafeScene):
    _cap = None
    SAY_HOLD = 1.2
    PACE = 1.8   # reading time: every wait() is stretched (exam-cram clip, Min reads Thai captions)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * self.PACE, *args, **kwargs)

    def say(self, txt, size=21):
        new = caption_top(txt, size=size, max_w=13.0)
        if self._cap is not None:
            self.play(FadeOut(self._cap), run_time=0.3)
            self.play(FadeIn(new), run_time=0.4)
        else:
            self.play(FadeIn(new), run_time=0.6)
        self._cap = new
        super().wait(self.SAY_HOLD)

    def glow(self, term, fig, color, rt=1.4):
        wide = term.width > 3.2 or isinstance(term, Text)
        anims = [Indicate(term, color=WHITE, scale_factor=1.0 if wide else 1.2),
                 Circumscribe(term, color=color, buff=0.04, stroke_width=3, fade_out=True)]
        if fig is not None:
            anims.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*anims, run_time=rt)

    def swap(self, old, new, rt=0.5):
        """same-spot replacement in two plays (SKILL §54: never FadeOut+FadeIn together)."""
        if old is not None:
            self.play(FadeOut(old, run_time=0.35))
        self.play(FadeIn(new), run_time=rt)
        return new

    def intro_motion(self, run=5.0):
        phi = ValueTracker(PHI0 - TAU)
        live = always_redraw(lambda: pieces(phi.get_value(), O_I))
        self.add(live)
        self.play(phi.animate.set_value(PHI0), run_time=run, rate_func=linear)
        static = pieces(PHI0, O_I)
        self.remove(live)
        self.add(static)
        self.play(static.animate.shift(O_A - O_I), run_time=1.0)
        return static

    def explode(self, mech, keep=()):
        """pull the assembled links apart onto the FBD anchors."""
        O, B, C, G1, G2, th = geo(PHI0, O_A)
        self.play(FadeOut(mech[3]), *[FadeOut(m) for m in keep], run_time=0.5)
        self.play(mech[0].animate.shift(O1E - O), mech[1].animate.shift(BRE - B),
                  mech[2].animate.shift(CSE - C), run_time=1.6)
        d = fbd()
        # swap the moved links for the FBD-styled ones (same geometry, bigger slider box)
        self.remove(mech[0], mech[1], mech[2])
        self.add(d["crank"], d["rod"], d["slider"])
        return d


# =====================================================================
# D40 -- the method
# =====================================================================
class D40_ExamDFAMethod(ExamScene):
    def construct(self):
        ttl = fit_width(title("Dynamic force analysis — วิธีทำทีละขั้น", size=28), 8.2)
        self.add(ttl, page_ref("สไลด์ W8 หน้า 8–15"))

        self.say("กลไก slider-crank (รูป 10.9): ข้อเหวี่ยง (1) หมุนรอบ O1 ดันก้านสูบ (2) ให้สไลเดอร์ (3) วิ่งบนราง")
        mech = self.intro_motion()
        Lb = point_labels()
        names = VGroup(*Lb.values())
        tags = link_tags()
        self.play(FadeIn(names), FadeIn(tags))
        self.say("G1, G2, G3 = จุดศูนย์กลางมวลของแต่ละชิ้น — แรงเฉื่อยของชิ้นนั้นกระทำที่จุด G")
        self.glow(VGroup(Lb["G1"], Lb["G2"], Lb["G3"]), VGroup(mech[0][3], mech[1][3], mech[2][1]), WHITE)
        phm, thm = angle_marks()
        self.say("มุมแบบสไลด์: φ วัดจากแกน +x ทวนเข็ม, θ = มุมก้านสูบใต้แนวนอน ; บวก = ทวนเข็ม (CCW)")
        self.play(Create(phm), Create(thm), run_time=1.2)
        self.wait(1.5)

        steps = VGroup(
            T("ขั้น 1  Kinematics: หาความเร่ง a_G และ α ของทุกชิ้น", 21),
            T("ขั้น 2  D'Alembert: ใส่แรงเฉื่อย และแรงบิดเฉื่อย", 21),
            T("ขั้น 3  วาด FBD แยกทีละชิ้น", 21),
            T("ขั้น 4  นับตัวแปร = จำนวนสมการ", 21),
            T("ขั้น 5  แก้: สไลเดอร์ → ก้านสูบ → ข้อเหวี่ยง → T1", 21))
        for i, s in enumerate(steps):
            prow(s, i, y0=1.9, dy=0.62)
        self.say("ภาพรวม 5 ขั้น — ลำดับนี้ใช้ได้กับทุกโจทย์แรงพลศาสตร์ในบทนี้")
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.2) for s in steps], lag_ratio=0.3), run_time=2.5)
        self.wait(3.0)
        self.play(FadeOut(steps), FadeOut(tags), FadeOut(phm), FadeOut(thm))

        # ---------------- step 1: kinematics
        aG1, aG2, aG3, al1, al2 = accel_marks()
        O, B, C, G1, G2, th = geo(PHI0, O_A)
        w1 = VGroup(arc_arrow(O, 0.5, 15, 40, W_C), M(r"\omega_1", 24, W_C).move_to(O + P2(0.98, -0.15)))
        seg = Line(O, G1, color=WHITE, stroke_width=5)
        self.say("ขั้น 1 Kinematics: หาความเร่งของจุด G ทุกชิ้น และ α ทุกชิ้น (สูตรเดียวกับ W04)")
        e1 = prow(MP(r"\vec a_{G1}", "=", r"\vec\alpha_1", r"\times\vec r_{O_1G_1}", r"-\omega_1^2",
                     r"\,\vec r_{O_1G_1}", size=32), 0)
        e1b = prow(T("O1 เป็นหมุดตายตัว → a_O1 = 0 จึงไม่มีพจน์นี้", 19, GRAYTXT), 1)
        self.play(FadeIn(e1), FadeIn(e1b))
        self.play(GrowArrow(aG1[0]), FadeIn(aG1[1]))
        self.glow(e1[0], aG1, ACC_C)
        self.play(FadeIn(al1), FadeIn(w1))
        self.glow(e1[2], al1, ALP_C)
        self.play(Create(seg), run_time=0.5)
        self.glow(VGroup(e1[3], e1[5]), seg, WHITE)
        self.play(FadeOut(seg, run_time=0.3))
        self.glow(e1[4], w1, W_C)
        e2 = prow(row(M(r"a_{Cy}=0", 30, L3_C), T("สไลเดอร์อยู่บนราง → แก้ได้ α2 → a_G2", 19)), 2.2)
        e3 = prow(row(M(r"\vec a_{G3}=\vec a_C", 30, ACC_C), T("แนวนอนอย่างเดียว", 19)), 3.2)
        self.say("ก้านสูบ: จุด C วิ่งตามราง a_Cy = 0 ใช้หา α2 แล้วได้ a_G2 ; สไลเดอร์มีแค่ a_G3 แนวนอน")
        self.play(FadeIn(e2), FadeIn(al2), GrowArrow(aG2[0]), FadeIn(aG2[1]))
        self.glow(e2[0], mech[2], L3_C)
        self.glow(e2[1], VGroup(al2, aG2), ALP_C)
        self.play(FadeIn(e3), GrowArrow(aG3[0]), FadeIn(aG3[1]))
        self.glow(e3[0], aG3, ACC_C)
        warn1 = prow(T("ข้อสอบอาจให้ a_G, α มาแล้ว (สไลด์หน้า 16) → ข้ามขั้นนี้ได้เลย", 19, WARN), 4.2)
        self.say("ถ้าโจทย์ให้ความเร่งมาแล้ว ไม่ต้องหาใหม่ — ขั้นนี้กินเวลาที่สุดในห้องสอบ")
        self.play(FadeIn(warn1))
        self.wait(2.0)
        self.play(FadeOut(VGroup(e1, e1b, e2, e3, warn1, w1)))

        # ---------------- step 2: D'Alembert
        Fi1, Fi2, Fi3, Ci1, Ci2 = inertia_marks()
        ml = mass_labels()
        self.say("ขั้น 2 D'Alembert: เติมแรงเฉื่อย F_i = −m a_G ที่จุด G — ทิศสวนทางความเร่งเสมอ")
        d1 = prow(MP(r"\vec F_i", "=", "-m", r"\,\vec a_G", size=34, color=INR_C), 0)
        d1b = prow(T("ที่ G สวนทาง a_G (ลูกศรม่วง)", 19, INR_C), 0, x=PX + 3.0, max_w=2.6)
        self.play(FadeIn(d1), FadeIn(d1b), FadeIn(ml))
        for Fi, aG in ((Fi1, aG1), (Fi2, aG2), (Fi3, aG3)):
            self.play(GrowArrow(Fi[0]), FadeIn(Fi[1]), run_time=0.7)
        self.glow(d1[0], VGroup(Fi1, Fi2, Fi3), INR_C)
        self.glow(d1[2], ml, WHITE)
        self.glow(d1[3], VGroup(aG1, aG2, aG3), ACC_C)
        self.say("แรงบิดเฉื่อย C_i = −I_G α — หมุนสวนทาง α ของชิ้นนั้น")
        d2 = prow(MP(r"C_i", "=", r"-I_G", r"\,\alpha", size=34, color=INR_C), 1)
        self.play(FadeIn(d2))
        self.play(FadeOut(al1, run_time=0.35))
        self.play(FadeOut(al2, run_time=0.35))
        self.play(Create(Ci1[0]), FadeIn(Ci1[1]), Create(Ci2[0]), FadeIn(Ci2[1]))
        self.glow(d2[0], VGroup(Ci1, Ci2), INR_C)
        self.glow(d2[2], ml, WHITE)
        d3 = prow(M(r"\Sigma\vec F+\vec F_i=0,\qquad \Sigma M+C_i=0", 32), 2.1)
        d3b = prow(T("ใส่เทอมเฉื่อยครบแล้ว → ทำเหมือนโจทย์สถิตยศาสตร์ (สมดุล)", 19, OK), 3.0)
        self.say("พอเติมเทอมเฉื่อยครบ ชิ้นส่วนที่กำลังเร่ง = โจทย์สมดุลธรรมดา ΣF = 0, ΣM = 0")
        self.play(FadeIn(d3), FadeIn(d3b))
        self.glow(d3, VGroup(Fi1, Fi2, Fi3, Ci1, Ci2), WHITE)
        self.wait(1.5)
        self.play(FadeOut(VGroup(d1, d1b, d2, d3, d3b, aG1, aG2, aG3, Fi1, Fi2, Fi3, Ci1, Ci2, ml)))

        # ---------------- step 3: FBD
        self.say("ขั้น 3 แยกชิ้นวาด FBD: ตัดที่ข้อต่อทุกจุด แล้วใส่แรงที่ข้อต่อ + เทอมเฉื่อย")
        d = self.explode(mech, keep=[names])
        F = d["F"]
        self.play(FadeIn(d["names"]), FadeIn(d["tags"]))
        self.say("สไลเดอร์ (3): F23 จากก้านสูบที่ C, F03y จากราง (ไม่มีแรงเสียดทาน → ไม่มี F03x), เทอมเฉื่อยแนวนอน")
        for k_ in ("F23x", "F23y", "F03y", "i3"):
            self.play(GrowArrow(F[k_][0]), FadeIn(F[k_][1]), run_time=0.6)
        self.say("ก้านสูบ (2): F12 ที่ B, F32 ที่ C, แรงเฉื่อย + แรงบิดเฉื่อยที่ G2")
        for k_ in ("F12x", "F12y", "F32x", "F32y", "i2x", "i2y"):
            self.play(GrowArrow(F[k_][0]), FadeIn(F[k_][1]), run_time=0.5)
        self.play(Create(F["c2"][0]), FadeIn(F["c2"][1]), run_time=0.6)
        self.say("ข้อเหวี่ยง (1): F01 ที่ O1, F21 ที่ B, แรงบิดขับ T1 (ที่ต้องหา), เทอมเฉื่อยที่ G1")
        for k_ in ("F01x", "F01y", "F21x", "F21y", "i1x", "i1y"):
            self.play(GrowArrow(F[k_][0]), FadeIn(F[k_][1]), run_time=0.5)
        self.play(Create(F["c1"][0]), FadeIn(F["c1"][1]), Create(F["T1"][0]), FadeIn(F["T1"][1]))
        self.say("กติกา: แรงไม่รู้ค่าวาดไปทาง +x, +y (โมเมนต์ทวนเข็ม) เสมอ — คำตอบติดลบ = ทิศจริงกลับด้าน")
        self.glow(F["F01x"][1], F["F01x"][0], UNK_C)
        self.glow(F["T1"][1], F["T1"][0], TQ_C)
        q1 = prow(M(r"F_{ij}:\ \text{force of } i \text{ on } j", 30), 0, x=1.4)
        q2 = prow(M(r"F_{12}=-F_{21},\qquad F_{23}=-F_{32}", 32, UNK_C), 1, x=1.4)
        self.say("F_ij = แรงที่ชิ้น i กระทำต่อชิ้น j ; คู่กิริยา-ปฏิกิริยา (กฎข้อ 3): F12 = −F21, F23 = −F32")
        self.play(FadeIn(q1), FadeIn(q2))
        self.glow(q2, VGroup(F["F12y"], F["F21y"]), UNK_C)
        self.glow(q2, VGroup(F["F23x"], F["F32x"]), UNK_C)
        self.wait(1.0)

        # ---------------- step 4: count
        self.play(FadeOut(VGroup(q1, q2)))
        self.say("ขั้น 4 นับตัวแปร: ข้อเหวี่ยง 5 ตัว (F01x, F01y, F21x, F21y, T1)")
        c5 = T("5 ตัวแปร", 22, UNK_C).move_to(P2(-5.9, 1.05))
        self.play(FadeIn(c5))
        self.glow(c5, VGroup(F["F01x"], F["F01y"], F["F21x"], F["F21y"], F["T1"]), UNK_C)
        self.say("ก้านสูบเพิ่มอีก 2 ตัวที่ C (F32x, F32y) — F12 ไม่นับซ้ำเพราะ = −F21")
        c2 = T("2 ตัวแปร", 22, UNK_C).move_to(P2(3.2, -0.55))
        self.play(FadeIn(c2))
        self.glow(c2, VGroup(F["F32x"], F["F32y"]), UNK_C)
        self.say("สไลเดอร์เพิ่ม 1 ตัว (F03y) — F23 = −F32 นับไปแล้ว")
        c1 = T("1 ตัวแปร", 22, UNK_C).move_to(P2(5.75, -3.25))
        self.play(FadeIn(c1))
        self.glow(c1, F["F03y"], UNK_C)
        k1 = prow(row(T("ตัวแปร", 21, UNK_C), M(r"5+2+1=8", 32, UNK_C)), 0, x=1.4)
        k2 = prow(row(T("สมการ", 21), M(r"2+3+3=8", 32), T("(สไลเดอร์ไม่หมุน: มีแค่ ΣFx, ΣFy)", 18, GRAYTXT)), 1, x=1.4)
        k3 = prow(row(M(r"8=8", 32, OK), T("แก้ได้พอดี (สไลด์หน้า 13)", 20, OK)), 2, x=1.4)
        self.say("สมการ: สไลเดอร์ 2 + ก้านสูบ 3 + ข้อเหวี่ยง 3 = 8 เท่ากับจำนวนตัวแปร → แก้ได้")
        self.play(FadeIn(k1))
        self.play(FadeIn(k2))
        self.glow(k2[1], VGroup(d["slider"], d["rod"], d["crank"]), WHITE)
        self.play(FadeIn(k3))
        self.wait(2.0)
        self.play(FadeOut(VGroup(k1, k2, k3, c5, c2, c1)))

        # ---------------- step 5: solve order
        hdr = None
        eq = None
        seq = [
            ("ลำดับ 1/6 — สไลเดอร์ (3) ΣFx: มีตัวแปรเดียว",
             M(r"F_{23x}+(-m_3a_{G3})=0\ \Rightarrow\ F_{32x}=-F_{23x}", 32),
             ["F23x", "i3", "F32x"], None),
            ("ลำดับ 2/6 — ก้านสูบ (2) ΣM รอบ B: F12 ผ่าน B โมเมนต์เป็นศูนย์ ตัดทิ้ง",
             M(r"\Sigma M_B=0\ \Rightarrow\ F_{32y}", 34),
             ["F32y", "F32x", "i2x", "i2y", "c2"], ("Br", ["F12x", "F12y"])),
            ("ลำดับ 3/6 — สไลเดอร์ (3) ΣFy",
             M(r"F_{03y}+F_{23y}=0\ \Rightarrow\ F_{03y}=F_{32y}", 32),
             ["F03y", "F23y"], None),
            ("ลำดับ 4/6 — ก้านสูบ (2) ΣFx, ΣFy",
             M(r"\Sigma F_x,\ \Sigma F_y\ \Rightarrow\ F_{12x},\ F_{12y}\ \Rightarrow\ F_{21}=-F_{12}", 32),
             ["F12x", "F12y", "F21x", "F21y"], None),
            ("ลำดับ 5/6 — ข้อเหวี่ยง (1) ΣFx, ΣFy",
             M(r"\Sigma F_x,\ \Sigma F_y\ \Rightarrow\ F_{01x},\ F_{01y}", 32),
             ["F01x", "F01y"], None),
            ("ลำดับ 6/6 — ข้อเหวี่ยง (1) ΣM รอบ O1 (ไม่ใช่รอบ G1 — ลายมืออาจารย์หน้า 12) → T1",
             M(r"\Sigma M_{O_1}=0\ \Rightarrow\ T_1", 34, TQ_C),
             ["T1", "F21x", "F21y", "i1x", "i1y", "c1"], ("O1", ["F01x", "F01y"])),
        ]
        self.say("ขั้น 5 แก้ตามลำดับ: เริ่มจากชิ้นที่มีตัวแปรน้อยสุด ไม่ต้องแก้เมทริกซ์ 8×8")
        for cap, eqm, keys, mom in seq:
            self.say(cap, size=20 if len(cap) > 60 else 21)
            new = prow(eqm, 0, x=1.4)
            eq = self.swap(eq, new)
            extra = []
            if mom is not None:
                rg = Circle(radius=0.26, color=WHITE, stroke_width=4).move_to(d[mom[0]])
                self.play(Create(rg), *[F[k_].animate.set_opacity(0.25) for k_ in mom[1]])
                extra.append(rg)
            self.glow(eq, VGroup(*[F[k_] for k_ in keys]), UNK_C if mom is None or mom[0] == "Br" else TQ_C)
            self.wait(0.8)
            if mom is not None:
                self.play(FadeOut(extra[0]), *[F[k_].animate.set_opacity(1) for k_ in mom[1]])
        self.play(FadeOut(eq, run_time=0.35))

        # ---------------- traps
        self.say("กับดักที่ต้องจำ (1): สมการโมเมนต์ก้านสูบต้องมี −I_G2 α2 — เมทริกซ์สไลด์หน้า 15 แถว 6 ลืมเทอมนี้")
        w1_ = prow(M(r"\text{drop } {-I_{G2}\alpha_2}\ \Rightarrow\ T_1=0.332\ \text{(wrong)},\ \text{keep}\Rightarrow 0.308", 30, WARN), 0, x=1.4)
        self.play(FadeIn(w1_))
        self.glow(w1_, F["c2"], WARN)
        self.say("(2) สมการ 10.8f, 10.8g ของข้อเหวี่ยงใช้ m1, a_G1 (สไลด์พิมพ์ m2 — อาจารย์วงแก้หน้า 14)")
        w2_ = prow(M(r"F_{01x}+F_{21x}-m_1a_{G1x}=0", 32, WARN), 1, x=1.4)
        self.play(FadeIn(w2_))
        self.glow(w2_, VGroup(F["F01x"], F["F21x"], F["i1x"]), WARN)
        self.say("(3) สไลด์ให้ mm/s² → หาร 1000 เป็น m/s² ก่อนคูณมวล ; คำตอบบวก = ทวนเข็ม")
        self.glow(F["i3"][1], F["i3"][0], INR_C)
        self.wait(3.0)


# =====================================================================
# D41 -- Sample Problem 10.6
# =====================================================================
class D41_ExamDFASP106(ExamScene):
    def construct(self):
        ttl = fit_width(title("Sample Problem 10.6 — หาแรงบิดขับ T1", size=28), 8.2)
        self.add(ttl, page_ref("สไลด์ W8 หน้า 16–19"))
        self.say("โจทย์ตัวอย่างในสไลด์: slider-crank ขณะ φ = 70° — หาแรงทุกข้อต่อ และแรงบิดขับ T1")
        mech = self.intro_motion(run=3.5)
        Lb = point_labels()
        names = VGroup(*Lb.values())
        self.play(FadeIn(names))

        # ---------------- page A: geometry + mass
        O, B, C, G1, G2, th = geo(PHI0, O_A)
        ml = mass_labels()
        phm, thm = angle_marks()
        rl = M("r", 26, L1_C).move_to((G1 + B) / 2 + 0.42 * U(-20))
        ll = M("l", 26, L2_C).move_to((G2 + C) / 2 + 0.42 * U(60))
        dimG1 = VGroup(Line(O + 0.35 * U(160), G1 + 0.35 * U(160), color=DIM_C, stroke_width=2.5),
                       M("r_G", 24, DIM_C).move_to((O + G1) / 2 + 0.62 * U(160)))
        dimG2 = VGroup(Line(B + 0.35 * U(60), G2 + 0.35 * U(60), color=DIM_C, stroke_width=2.5),
                       M("l_G", 24, DIM_C).move_to((B + G2) / 2 + 0.62 * U(60)))
        self.say("ขั้น 1 เข้าใจโจทย์: เขียนข้อมูลให้ครบ เป็นหน่วย SI (เมตร, kg)")
        a1 = prow(M(r"m_1=0.5,\ m_2=1.0,\ m_3=1.5\ \text{kg}", 30), 0)
        a2 = prow(M(r"I_{G1}=1.25\times10^{-3},\ I_{G2}=2.5\times10^{-3}\ \text{kg m}^2", 30), 1)
        a3 = prow(M(r"r=0.05,\ r_G=0.025\ \text{m}", 30, L1_C), 2)
        a4 = prow(M(r"l=0.094,\ l_G=0.047\ \text{m}", 30, L2_C), 3)
        a5 = prow(M(r"\phi=70^\circ,\ \theta=30^\circ", 30), 4)
        self.play(FadeIn(a1), FadeIn(ml))
        self.glow(a1, ml, WHITE)
        self.play(FadeIn(a2))
        self.glow(a2, VGroup(ml[0], ml[1]), WHITE)
        self.play(FadeIn(a3), FadeIn(rl), Create(dimG1))
        self.glow(a3, VGroup(rl, dimG1, mech[0]), L1_C)
        self.play(FadeIn(a4), FadeIn(ll), Create(dimG2))
        self.glow(a4, VGroup(ll, dimG2, mech[1]), L2_C)
        self.play(FadeIn(a5), Create(phm), Create(thm))
        self.glow(a5, VGroup(phm, thm), WHITE)
        self.wait(1.5)
        self.play(FadeOut(VGroup(a1, a2, a3, a4, a5, rl, ll, dimG1, dimG2, phm, thm, ml)))

        # ---------------- page B: given accelerations
        aG1, aG2, aG3, al1, al2 = accel_marks()
        self.say("ความเร่งโจทย์ให้มาแล้ว (หน้า 16) → ไม่ต้องทำ kinematics เอง")
        b1 = prow(M(r"\vec a_{G1}=(-1.79,\ -1.99)\ \text{m/s}^2", 30, ACC_C), 0)
        b2 = prow(M(r"\vec a_{G2}=(-2.65,\ -2.00)\ \text{m/s}^2", 30, ACC_C), 1)
        b3 = prow(M(r"a_{G3}=-1.75\ \text{m/s}^2", 30, ACC_C), 2)
        b4 = prow(M(r"\alpha_1=40,\ \alpha_2=46\ \text{rad/s}^2", 30, ALP_C), 3)
        for bb, fig in ((b1, aG1), (b2, aG2), (b3, aG3)):
            self.play(FadeIn(bb), GrowArrow(fig[0]), FadeIn(fig[1]), run_time=0.7)
            self.glow(bb, fig, ACC_C)
        self.play(FadeIn(b4), FadeIn(al1), FadeIn(al2))
        self.glow(b4, VGroup(al1, al2), ALP_C)
        self.wait(1.0)
        self.play(FadeOut(VGroup(b1, b2, b3, b4)))

        # ---------------- page C: inertia terms
        Fi1, Fi2, Fi3, Ci1, Ci2 = inertia_marks()
        ml = mass_labels()
        self.say("ขั้น 2 เทอมเฉื่อย: −m a_G และ −I_G α ทุกชิ้น (ทำเป็นตารางก่อน แบบสไลด์หน้า 17)")
        c1 = prow(M(r"\vec F_{i1}=-m_1\vec a_{G1}=-(0.5)(-1.79,\,-1.99)=(0.895,\ 0.995)\ \text{N}", 30, INR_C), 0, dy=0.56)
        c2 = prow(M(r"C_{i1}=-I_{G1}\alpha_1=-(1.25\times10^{-3})(40)=-0.05\ \text{N m}", 30, INR_C), 1, dy=0.56)
        c3 = prow(M(r"\vec F_{i2}=-m_2\vec a_{G2}=(2.65,\ 2.0)\ \text{N}", 30, INR_C), 2, dy=0.56)
        c4 = prow(M(r"C_{i2}=-I_{G2}\alpha_2=-(2.5\times10^{-3})(46)=-0.115\ \text{N m}", 30, INR_C), 3, dy=0.56)
        c5 = prow(M(r"F_{i3}=-m_3a_{G3}=-(1.5)(-1.75)=2.625\ \text{N}", 30, INR_C), 4, dy=0.56)
        self.play(FadeIn(ml))
        self.play(FadeIn(c1), GrowArrow(Fi1[0]), FadeIn(Fi1[1]))
        self.glow(c1, VGroup(Fi1, aG1), INR_C)
        self.say("ระวังเครื่องหมาย: a ติดลบ → แรงเฉื่อยเป็นบวก เช่น −(0.5)(−1.79) = +0.895 (ลูกศรม่วงสวนลูกศรเหลือง)")
        self.play(FadeOut(al1, run_time=0.35))
        self.play(FadeIn(c2), Create(Ci1[0]), FadeIn(Ci1[1]))
        self.glow(c2, Ci1, INR_C)
        self.play(FadeIn(c3), GrowArrow(Fi2[0]), FadeIn(Fi2[1]))
        self.glow(c3, VGroup(Fi2, aG2), INR_C)
        self.play(FadeOut(al2, run_time=0.35))
        self.play(FadeIn(c4), Create(Ci2[0]), FadeIn(Ci2[1]))
        self.glow(c4, Ci2, INR_C)
        self.play(FadeIn(c5), GrowArrow(Fi3[0]), FadeIn(Fi3[1]))
        self.glow(c5, VGroup(Fi3, aG3), INR_C)
        self.wait(1.5)
        self.play(FadeOut(VGroup(c1, c2, c3, c4, c5, aG1, aG2, aG3, Fi1, Fi2, Fi3, Ci1, Ci2, ml)))

        # ---------------- FBD with numbers
        self.say("ขั้น 3 แยก FBD — เทอมเฉื่อยใส่เป็นตัวเลขแล้ว (ม่วง) ตัวไม่รู้ค่าสีแดง")
        self.explode(mech, keep=[names])
        d = fbd(num=True)
        F = d["F"]
        self.play(FadeIn(d["names"]), FadeIn(d["tags"]),
                  *[FadeIn(F[k_]) for k_ in F], run_time=1.5)
        self.wait(1.0)
        eqs = VGroup()

        def show(*rows_):
            nonlocal eqs
            if len(eqs):
                self.play(FadeOut(eqs, run_time=0.35))
            eqs = VGroup(*[prow(r_, i, y0=2.0, dy=0.55, x=1.4) for i, r_ in enumerate(rows_)])
            self.play(FadeIn(eqs), run_time=0.5)
            return eqs

        def solved(*keys):
            self.play(*[F[k_].animate.set_color(OK) for k_ in keys], run_time=0.6)

        # 1 slider sum Fx
        self.say("(1) สไลเดอร์ ΣFx = 0 → ได้ F32x ทันที")
        e = show(MP(r"F_{23x}", r"+2.625", "=0", size=32),
                 M(r"F_{23x}=-2.625\ \Rightarrow\ F_{32x}=+2.625\ \text{N}", 32, OK))
        self.glow(e[0][0], F["F23x"], UNK_C)
        self.glow(e[0][1], F["i3"], INR_C)
        solved("F23x", "F32x")

        # 2 rod moment about B
        self.say("(2) ก้านสูบ ΣM รอบ B = 0 (F12 ผ่าน B จึงหายไป) ; sin30° = 0.5, cos30° = 0.86603")
        rg = Circle(radius=0.26, color=WHITE, stroke_width=4).move_to(d["Br"])
        self.play(Create(rg), F["F12x"].animate.set_opacity(0.25), F["F12y"].animate.set_opacity(0.25))
        e = show(MP(r"2.625(0.094)(0.5)", r"+F_{32y}(0.094)(0.86603)", size=30),
                 MP(r"+2.65(0.047)(0.5)", r"+2.0(0.047)(0.86603)", r"-0.115", "=0", size=30),
                 M(r"0.12338+0.08141F_{32y}+0.06228+0.08141-0.115=0", 30),
                 M(r"F_{32y}=-0.15206/0.08141=-1.868\ \text{N}", 32, OK))
        self.glow(e[0][0], F["F32x"], OK)
        self.glow(e[0][1], F["F32y"], UNK_C)
        self.glow(e[1][0], F["i2x"], INR_C)
        self.glow(e[1][1], F["i2y"], INR_C)
        self.glow(e[1][2], F["c2"], INR_C)
        solved("F32y")
        self.play(FadeOut(rg), F["F12x"].animate.set_opacity(1), F["F12y"].animate.set_opacity(1))
        self.say("ติดลบ = ทิศจริงกลับด้านกับลูกศรที่วาด (ก้านสูบโดนสไลเดอร์ดึงลง 1.868 N)")
        self.wait(1.0)

        # 3 slider sum Fy
        self.say("(3) สไลเดอร์ ΣFy = 0 → แรงจากราง F03y")
        e = show(M(r"F_{03y}+F_{23y}=0,\quad F_{23y}=-F_{32y}=+1.868", 30),
                 M(r"F_{03y}=F_{32y}=-1.868\ \text{N}", 32, OK),
                 T("ก้านสูบดันสไลเดอร์ขึ้น → รางต้องกดลง 1.87 N", 19, GRAYTXT))
        self.glow(e[0], VGroup(F["F23y"], F["F03y"]), UNK_C)
        solved("F23y", "F03y")

        # 4 rod sum F
        self.say("(4) ก้านสูบ ΣFx, ΣFy → F12 แล้วกลับเครื่องหมายเป็น F21 (แรงที่ก้านสูบกระทำต่อข้อเหวี่ยง)")
        e = show(M(r"F_{12x}+2.625+2.65=0\ \Rightarrow\ F_{12x}=-5.275", 30),
                 M(r"F_{12y}-1.868+2.0=0\ \Rightarrow\ F_{12y}=-0.132", 30),
                 M(r"F_{21x}=5.275,\quad F_{21y}=0.132\ \text{N}", 32, OK))
        self.glow(e[0], VGroup(F["F12x"], F["F32x"], F["i2x"]), UNK_C)
        self.glow(e[1], VGroup(F["F12y"], F["F32y"], F["i2y"]), UNK_C)
        solved("F12x", "F12y")
        self.glow(e[2], VGroup(F["F21x"], F["F21y"]), OK)
        solved("F21x", "F21y")

        # 5 crank sum F
        self.say("(5) ข้อเหวี่ยง ΣFx, ΣFy → แรงที่หมุด O1")
        e = show(M(r"F_{01x}+5.275+0.895=0\ \Rightarrow\ F_{01x}=-6.170\ \text{N}", 30, OK),
                 M(r"F_{01y}+0.132+0.995=0\ \Rightarrow\ F_{01y}=-1.127\ \text{N}", 30, OK))
        self.glow(e[0], VGroup(F["F01x"], F["F21x"], F["i1x"]), UNK_C)
        self.glow(e[1], VGroup(F["F01y"], F["F21y"], F["i1y"]), UNK_C)
        solved("F01x", "F01y")

        # 6 crank moment about O1
        self.say("(6) ข้อเหวี่ยง ΣM รอบ O1 (ตัด F01 ทิ้ง) ; sin70° = 0.93969, cos70° = 0.34202")
        rg = Circle(radius=0.26, color=WHITE, stroke_width=4).move_to(d["O1"])
        self.play(Create(rg), F["F01x"].animate.set_opacity(0.25), F["F01y"].animate.set_opacity(0.25))
        e = show(MP(r"T_1=", r"5.275(0.05)(0.93969)", r"-0.132(0.05)(0.34202)", size=30),
                 MP(r"+0.895(0.025)(0.93969)", r"-0.995(0.025)(0.34202)", r"+0.05", size=30),
                 M(r"=0.24784-0.00226+0.02103-0.00851+0.05", 30),
                 M(r"T_1=0.308\ \text{N m}\ \ (\text{ccw})", 36, TQ_C))
        self.glow(e[0][1], F["F21x"], OK)
        self.glow(e[0][2], F["F21y"], OK)
        self.glow(e[1][0], F["i1x"], INR_C)
        self.glow(e[1][1], F["i1y"], INR_C)
        self.glow(e[1][2], F["c1"], INR_C)
        box = SurroundingRectangle(e[3], color=TQ_C, buff=0.12)
        self.play(Create(box))
        self.glow(e[3], F["T1"], TQ_C)
        solved("T1")
        self.play(FadeOut(rg), F["F01x"].animate.set_opacity(1), F["F01y"].animate.set_opacity(1))
        self.say("T1 บวก → มอเตอร์ต้องบิดข้อเหวี่ยงทวนเข็ม 0.308 N·m ตรงกับสไลด์")
        self.wait(1.5)

        # ---------------- summary + traps
        self.play(FadeOut(box, run_time=0.3))
        e = show(M(r"F_{32x}=2.625,\ \ F_{32y}=F_{03y}=-1.868", 30),
                 M(r"F_{21x}=5.275,\ \ F_{21y}=0.132", 30),
                 M(r"F_{01x}=-6.170,\ \ F_{01y}=-1.127\ \text{N}", 30),
                 M(r"T_1=0.308\ \text{N m (ccw)}", 32, TQ_C))
        self.say("สรุปคำตอบ (หน่วย N) — สไลด์ปัด F32y = −1.88, F21y = 0.12, F01y = −1.115 ต่างแค่การปัดเศษ, T1 ตรงกัน")
        self.wait(2.5)
        self.say("กับดัก: ถ้าลืม −I_G2 α2 = −0.115 ในสมการรอบ B (เมทริกซ์สไลด์หน้า 15 แถว 6) จะได้ T1 = 0.332 ผิด")
        self.glow(F["c2"][1], F["c2"][0], WARN)
        self.wait(3.0)


# =====================================================================
# D42 -- practice 1: single bar pinned at O
# =====================================================================
class D42_ExamDFABarDrill(ExamScene):
    PACE = 2.6
    SAY_HOLD = 2.4

    def construct(self):
        ttl = fit_width(title("โจทย์ฝึก 1 — แท่งเดี่ยวหมุนรอบหมุด O", size=28), 8.2)
        self.add(ttl, page_ref("โจทย์ฝึก (ผู้ช่วยแต่ง)"))
        k = 11.0
        O = P2(-5.6, -2.4)
        ang0 = 30 * DEGREES

        def bar(a):
            A = O + k * 0.4 * np.array([np.cos(a), np.sin(a), 0.0])
            G = (O + A) / 2
            return VGroup(Line(O, A, color=L1_C, stroke_width=10), pin(O), pin(A), gdot(G))

        sup = Polygon(O, O + P2(-0.22, -0.32), O + P2(0.22, -0.32), color=GRAYTXT, stroke_width=3)
        A = O + k * 0.4 * U(30)
        G = (O + A) / 2
        self.say("แท่งสม่ำเสมอ OA ยาว 0.4 m มวล 3 kg หมุดที่ O วางในระนาบนอน (ไม่คิดน้ำหนัก)")
        tr = ValueTracker(75 * DEGREES)
        live = always_redraw(lambda: bar(tr.get_value()))
        self.add(sup, live)
        self.play(tr.animate.set_value(ang0), run_time=3.0, rate_func=smooth)
        b = bar(ang0)
        self.remove(live)
        self.add(b)
        lab = VGroup(M("O", 26).move_to(O + P2(-0.3, 0.32)),
                     M("A", 26).next_to(A, RIGHT, buff=0.15),
                     M("G", 26).move_to(G + 0.4 * U(-60)))
        Lm = M(r"L=0.4\ \text{m},\ m=3\ \text{kg}", 26, L1_C).move_to(A + P2(-1.75, 0.7))
        w = VGroup(arc_arrow(O, 0.7, 45, 50, W_C), M(r"\omega", 26, W_C).move_to(O + 0.95 * U(75)))
        al = VGroup(arc_arrow(O, 1.15, 48, 47, ALP_C), M(r"\alpha", 26, ALP_C).move_to(O + 1.42 * U(68)))
        ang = VGroup(DashedLine(O, O + P2(0.65, 0), color=GRAYTXT, stroke_width=2),
                     Arc(radius=0.45, start_angle=0, angle=ang0, arc_center=O, color=WHITE, stroke_width=3),
                     M(r"30^\circ", 22).move_to(O + P2(0.62, -0.22)))
        self.play(FadeIn(lab), FadeIn(Lm), FadeIn(ang))
        q = prow(M(r"\omega=6\ \text{rad/s},\ \ \alpha=15\ \text{rad/s}^2\ \ (\text{ccw})", 30), 0, x=-0.4, max_w=7.0)
        q2 = prow(T("หา: แรงที่หมุด O กระทำต่อแท่ง และแรงบิดขับ T", 21), 1, x=-0.4, max_w=7.0)
        self.play(FadeIn(q), FadeIn(w), FadeIn(al))
        self.glow(q, VGroup(w, al), W_C)
        self.play(FadeIn(q2))
        self.wait(1.0)

        # step 1-2: r_OG, I_G, a_G
        dim = VGroup(Line(O, G, color=WHITE, stroke_width=5),
                     M(r"\vec r_{OG}", 24, DIM_C).move_to((O + G) / 2 + 0.45 * U(-60)))
        self.say("ขั้น 1: G อยู่กลางแท่ง ; I_G ของแท่ง = mL²/12")
        s1 = prow(M(r"\vec r_{OG}=0.2(\cos30^\circ,\ \sin30^\circ)=(0.17321,\ 0.1)\ \text{m}", 30), 2, x=-0.4, max_w=7.0)
        s2 = prow(M(r"I_G=\tfrac{1}{12}mL^2=\tfrac{1}{12}(3)(0.4)^2=0.04\ \text{kg m}^2", 30), 3, x=-0.4, max_w=7.0)
        self.play(FadeIn(s1), Create(dim[0]), FadeIn(dim[1]))
        self.glow(s1, dim, DIM_C)
        self.play(FadeOut(dim[0], run_time=0.35))
        self.play(FadeIn(s2))
        self.glow(s2, VGroup(lab[2], b[3]), WHITE)
        d1 = np.array([-7.735, -1.002, 0])
        aG = farrow(G, 0.1 * d1, ACC_C, r"\vec a_G", UP)
        self.say("ขั้น 2: a_G = α×r − ω²r → a_Gx = α(−r_y) − ω² r_x, a_Gy = α r_x − ω² r_y")
        s3 = prow(M(r"a_{Gx}=15(-0.1)-36(0.17321)=-7.735\ \text{m/s}^2", 30, ACC_C), 4, x=-0.4, max_w=7.0)
        s4 = prow(M(r"a_{Gy}=15(0.17321)-36(0.1)=-1.002\ \text{m/s}^2", 30, ACC_C), 5, x=-0.4, max_w=7.0)
        self.play(FadeIn(s3), FadeIn(s4), GrowArrow(aG[0]), FadeIn(aG[1]))
        self.glow(VGroup(s3, s4), aG, ACC_C)
        self.wait(2.0)

        # step 3: D'Alembert
        Fi = farrow(G, -0.035 * np.array([-23.21, -3.01, 0]) * 1.0, INR_C, r"\vec F_i", RIGHT)
        Ci = VGroup(arc_arrow(G, 0.45, 280, -80, INR_C), M(r"C_i", 26, INR_C).move_to(G + P2(0.75, -0.6)))
        self.say("ขั้น 3 D'Alembert: F_i = −m a_G (สวนความเร่ง), C_i = −I_G α")
        self.play(FadeOut(VGroup(q2, s1, s2), run_time=0.35))
        s5 = prow(M(r"\vec F_i=-3(-7.735,\ -1.002)=(23.21,\ 3.01)\ \text{N}", 30, INR_C), 1, x=-0.4, max_w=7.0)
        s6 = prow(M(r"C_i=-0.04(15)=-0.6\ \text{N m}\ \ (\text{cw})", 30, INR_C), 2, x=-0.4, max_w=7.0)
        self.play(FadeIn(s5), GrowArrow(Fi[0]), FadeIn(Fi[1]))
        self.glow(s5, VGroup(Fi, aG), INR_C)
        self.play(FadeIn(s6), Create(Ci[0]), FadeIn(Ci[1]))
        self.glow(s6, Ci, INR_C)
        self.wait(1.5)

        # step 4: pin force + torque
        self.play(FadeOut(VGroup(s3, s4), run_time=0.35))
        self.play(FadeOut(VGroup(w, al), run_time=0.35))
        FO = farrow(O, 0.035 * np.array([-23.21, -3.01, 0]), UNK_C, r"\vec F_O", LEFT)
        Tq = VGroup(arc_arrow(O, 0.55, 200, 100, TQ_C), M("T", 26, TQ_C).move_to(O + 0.88 * U(255)))
        self.say("ขั้น 4 สมดุล: ΣF = 0 ได้แรงหมุด ; ΣM รอบ O ตัดแรงหมุดทิ้ง ได้ T")
        s7 = prow(M(r"\Sigma\vec F=0:\ \vec F_O=-\vec F_i=(-23.21,\ -3.01)\ \text{N}", 30, UNK_C), 3, x=-0.4, max_w=7.0)
        self.play(FadeIn(s7), GrowArrow(FO[0]), FadeIn(FO[1]))
        self.glow(s7, FO, UNK_C)
        self.wait(1.5)
        s8 = prow(MP(r"\Sigma M_O:\ T", r"+(0.17321\cdot3.006-0.1\cdot23.206)", r"-0.6", "=0", size=30), 4, x=-0.4, max_w=7.0)
        s9 = prow(M(r"T-1.80-0.6=0\ \Rightarrow\ T=2.40\ \text{N m (ccw)}", 32, TQ_C), 5, x=-0.4, max_w=7.0)
        self.play(FadeIn(s8), Create(Tq[0]), FadeIn(Tq[1]))
        self.glow(s8[0], Tq, TQ_C)
        self.glow(s8[1], VGroup(Fi, dim[1]), INR_C)
        self.glow(s8[2], Ci, INR_C)
        self.play(FadeIn(s9))
        box = SurroundingRectangle(s9, color=TQ_C, buff=0.1)
        self.play(Create(box))
        self.wait(2.0)
        self.say("ขั้น 5 ตรวจ: แท่งหมุนรอบจุดตายตัว → T = I_O α ต้องได้เท่ากัน (แกนขนาน หน้า 6)")
        s10 = prow(M(r"I_O=\tfrac13mL^2=0.16,\quad I_O\alpha=0.16(15)=2.40\ \checkmark", 30, OK), 6, x=-0.4, max_w=7.0)
        self.play(FadeIn(s10))
        self.glow(s10, VGroup(Tq, b), OK)
        self.say("สังเกต: T ไม่ขึ้นกับ ω และมุม — แรงเฉื่อยจาก ω² ชี้ผ่านจุด O ไม่มีโมเมนต์")
        self.wait(3.0)
