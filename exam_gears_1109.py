"""
exam_gears_1109.py -- Mechanics of Machinery, exam 9 Nov 2026, gear topics 1-3.

Source note (all numbers taken from here, computed by the previous worker's python script
Attachments/gear_exam_calc_2026-11-08.py):
  Exam_Prep/Mechanics of Machinery/สอบ 9 พ.ย. — เฟือง (นิยาม + Reverted + Planetary).md

G40_ExamNomenclature   -- (ก) gear nomenclature: 4 circles, a/b/c/h_t, p/t/m/P, P/LOA/phi/Rb, Z/m_p, N_min
G41_ExamRevertedDesign -- (ข) reverted compound 30:1, P = 10, 18/108 + 21/105, C = 6.30 in
G42_ExamPlanetaryEx74  -- (ค.5) Example 7.4: formula + tabular methods, omega_21 = +150 rad/s

Tooth outlines are real involute profiles (phi = 20 deg, full depth a = m, b = 1.25 m).
"""

import numpy as np
from manim import *
from mlib import *

PHI = 20 * DEGREES
PITCH_C = OK            # pitch circle
BASE_C = "#AB47BC"      # base circle
LOA_C = "#EF5350"       # line of action
ADD_C = GEAR_OUT        # addendum circle
DED_C = GRAYTXT         # dedendum circle
A_C = "#FFD54F"         # addendum a
B_C = "#80CBC4"         # dedendum b
Z_C = "#FFD54F"


def P2(x, y):
    return np.array([x, y, 0.0])


def polar(c, r, a):
    return np.asarray(c, dtype=float) + r * np.array([np.cos(a), np.sin(a), 0.0])


def inv(a):
    return np.tan(a) - a


def gear_profile(N, m, phi=PHI, add=1.0, ded=1.25, rot=0.0, window=None, n_inv=9):
    """(r, angle) points of an involute spur-gear outline, angle unwrapped and increasing.
    tooth k is centred at rot + k*2pi/N; thickness on the pitch circle = p/2 (no backlash).
    window=(a0, a1) keeps only the points inside that angular range (for a close-up sector)."""
    R = m * N / 2.0
    rb = R * np.cos(phi)
    ro, ri = R + add * m, R - ded * m
    b0 = np.pi / (2 * N) + inv(phi)

    def half(r):
        return b0 if r <= rb else b0 - inv(np.arccos(rb / r))

    rs = np.linspace(max(rb, ri), ro, n_inv)
    step = TAU / N
    if window is None:
        ks = range(N)
    else:
        k0 = int(np.floor((window[0] - rot) / step)) - 1
        k1 = int(np.ceil((window[1] - rot) / step)) + 1
        ks = range(k0, k1 + 1)
    out = []
    hr = b0 if ri < rb else half(ri)
    for k in ks:
        g = rot + k * step
        if ri < rb:
            out.append((ri, g - b0))
        for r in rs:
            out.append((r, g - half(r)))
        h_o = half(ro)
        for a in np.linspace(g - h_o, g + h_o, 5)[1:-1]:
            out.append((ro, a))
        for r in rs[::-1]:
            out.append((r, g + half(r)))
        if ri < rb:
            out.append((ri, g + b0))
        for a in np.linspace(g + hr, g + step - hr, 6)[1:-1]:
            out.append((ri, a))
    if window is not None:
        out = [(r, a) for (r, a) in out if window[0] <= a <= window[1]]
    return out


def gear_mob(N, m, center, color, rot=0.0, fill=0.85, sw=2.0, add=1.0, ded=1.25):
    pts = [polar(center, r, a) for (r, a) in gear_profile(N, m, add=add, ded=ded, rot=rot)]
    return Polygon(*pts, color=color, fill_opacity=fill, stroke_width=sw, stroke_color=color)


def gear_sector(N, m, center, color, window, body_r, fill=0.35, sw=2.5):
    pts = [polar(center, r, a) for (r, a) in gear_profile(N, m, rot=PI / 2, window=window)]
    for a in np.linspace(window[1], window[0], 24):
        pts.append(polar(center, body_r, a))
    return Polygon(*pts, color=color, fill_opacity=fill, stroke_width=sw, stroke_color=color)


def ring_mob(N, m, center, r_out, color, rot=0.0, fill=0.75):
    """internal gear: its tooth SPACES are the teeth of an external involute outline with
    addendum 1.25m (ring root) and dedendum 1.0m (ring tip)."""
    pts = [polar(center, r, a) for (r, a) in gear_profile(N, m, add=1.25, ded=1.0, rot=rot)]
    hole = Polygon(*pts)
    disk = Circle(radius=r_out).move_to(center)
    return Difference(disk, hole, color=color, fill_opacity=fill, stroke_width=2,
                      stroke_color=color)


def T(txt, size=20, color=WHITE):
    return Text(txt, font_size=size, color=color)


def M(tex, size=30, color=WHITE):
    return MathTex(tex, font_size=size, color=color)


def row(a, b, buff=0.25, max_w=5.8):
    g = VGroup(a, b).arrange(RIGHT, buff=buff)
    return fit_width(g, max_w)


def stack(a, b, max_w=4.6):
    g = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    return fit_width(g, max_w)


def place_left(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


def bg(mob, op=0.85):
    mob.add_background_rectangle(color=BLACK, opacity=op, buff=0.04)
    return mob


def arc_arrow(center, r, start, sweep, color, sw=4):
    a = Arc(radius=r, start_angle=start, angle=sweep, arc_center=center, color=color,
            stroke_width=sw)
    a.add_tip(tip_length=0.16, tip_width=0.16)
    return a


class ExamScene(SafeScene):
    _cap = None

    def say(self, txt, size=21):
        new = caption_top(txt, size=size, max_w=13.0)
        if self._cap is not None:
            self.play(FadeOut(self._cap), run_time=0.3)
            self.play(FadeIn(new), run_time=0.4)
        else:
            self.play(FadeIn(new), run_time=0.6)
        self._cap = new

    def glow(self, term, fig, color, rt=1.4):
        anims = [Indicate(term, color=WHITE, scale_factor=1.2),
                 Circumscribe(term, color=color, buff=0.08, stroke_width=4, fade_out=True)]
        if fig is not None:
            anims.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*anims, run_time=rt)


# =====================================================================
# G40 -- gear nomenclature (ก)
# =====================================================================
class G40_ExamNomenclature(ExamScene):
    def construct(self):
        ttl = title("นิยามสรีระของเฟือง (Gear nomenclature)", size=28)
        ref = page_ref("สไลด์หน้า 13-14, 31, 35")
        self.add(ttl, ref)

        # ---------------- A: close-up of 3 real involute teeth (24T, m = 3 mm, scale 0.2/mm)
        k = 0.2
        mu = 3 * k
        N = 24
        CG = P2(-2.6, -6.5)
        R = mu * N / 2
        Ro, Rb, Ri, Rm = R + mu, R * np.cos(PHI), R - 1.25 * mu, R - mu
        W0, W1 = 68 * DEGREES, 112 * DEGREES
        sector = gear_sector(N, mu, CG, GEAR_IN, (W0, W1), Ri - 0.55)

        self.say("ซูมดูฟันเฟือง 3 ซี่ของ pinion 24 ฟัน, m = 3 mm (ตัวอย่างหน้า 38) โปรไฟล์อินโวลูทจริง")
        self.play(DrawBorderThenFill(sector), run_time=2.0)
        self.wait(1.0)

        circ = [  # radius, color, symbol, name
            (Ro, ADD_C, r"R_o", "Addendum circle — วงกลมยอดฟัน"),
            (R, PITCH_C, r"R", "Pitch circle — วงกลิ้ง (ทุกสูตรอ้างอิงวงนี้)"),
            (Rb, BASE_C, r"R_b", "Base circle — อินโวลูทเริ่มคลี่จากวงนี้"),
            (Ri, DED_C, r"R_i", "Dedendum circle — วงกลมโคนฟัน"),
        ]
        self.say("4 วงกลมของเฟือง เรียงจากนอกเข้าใน — ชื่อสีเดียวกับเส้นในรูป")
        arcs, tags, rows = VGroup(), VGroup(), VGroup()
        ys = [1.35, 0.6, -0.15, -0.9]
        for (r, c, sym, name), y in zip(circ, ys):
            arc = Arc(radius=r, start_angle=W0, angle=W1 - W0, arc_center=CG, color=c,
                      stroke_width=3.5)
            tag = M(sym, 24, c)
            tag.next_to(polar(CG, r, W1), LEFT, buff=0.12)
            rw = place_left(row(M(sym, 30, c), T(name, 19, c)), 1.0, y)
            arcs.add(arc)
            tags.add(tag)
            rows.add(rw)
            self.play(Create(arc), FadeIn(tag), FadeIn(rw, shift=LEFT * 0.2), run_time=0.9)
            self.glow(rw[0], VGroup(arc, tag), c, rt=1.1)
            self.wait(0.6)
        order = M(r"R_i < R_b < R < R_o", 36).move_to([3.9, -1.9, 0])
        self.play(FadeIn(order, shift=UP * 0.15))
        self.say("ใต้ base circle ไม่ใช่อินโวลูท — ถ้าฟันน้อยจน R_b เข้าใกล้ R_i จะเสี่ยง undercut")
        self.wait(2.5)

        # ---------------- A2: tooth heights a, b, c, h_t
        self.play(FadeOut(rows), FadeOut(order))
        self.say("ความสูงฟัน วัดตามแนวรัศมีระหว่างวงกลม (มาตรฐาน full-depth 20°, หน้า 31)")
        td, tc = 64 * DEGREES, 59 * DEGREES

        def cw(t):
            return np.array([np.sin(t), -np.cos(t), 0.0])

        ext = VGroup(*[Arc(radius=r, start_angle=td - 0.5 * DEGREES, angle=W0 - td + 0.5 * DEGREES,
                           arc_center=CG, color=c, stroke_width=2, stroke_opacity=0.8)
                       for (r, c) in ((Ro, ADD_C), (R, PITCH_C))])
        ext_i = Arc(radius=Ri, start_angle=tc - 0.5 * DEGREES, angle=W0 - tc + 0.5 * DEGREES,
                    arc_center=CG, color=DED_C, stroke_width=2, stroke_opacity=0.8)
        mate = DashedVMobject(Arc(radius=Rm, start_angle=tc - 0.5 * DEGREES,
                                  angle=W1 - tc + 0.5 * DEGREES, arc_center=CG, color=WARN,
                                  stroke_width=3), num_dashes=46)
        bar_a = Line(polar(CG, R, td), polar(CG, Ro, td), color=A_C, stroke_width=6)
        bar_b = Line(polar(CG, Ri, td), polar(CG, R, td), color=B_C, stroke_width=6)
        bar_c = Line(polar(CG, Ri, tc), polar(CG, Rm, tc), color=WARN, stroke_width=6)
        la = M("a", 30, A_C).move_to(polar(CG, (R + Ro) / 2, td) + 0.27 * cw(td))
        lb = M("b", 30, B_C).move_to(polar(CG, (Ri + R) / 2, td) + 0.27 * cw(td))
        lc = M("c", 30, WARN).move_to(polar(CG, (Ri + Rm) / 2, tc) + 0.25 * cw(tc))
        hrows = VGroup(
            row(M(r"a = 1.000\,m", 30, A_C), T("addendum: ยอดฟันเหนือวงพิตช์", 19, A_C)),
            row(M(r"b = 1.25\,m", 30, B_C), T("dedendum: โคนฟันใต้วงพิตช์ (British)", 19, B_C)),
            row(M(r"c = b - a = 0.25\,m", 30, WARN), T("clearance: ช่องว่างใต้ยอดฟันตัวที่ขบ", 19, WARN)),
            row(M(r"h_t = a + b = 2.25\,m", 30), T("whole depth: สูงทั้งฟัน", 19)),
        )
        for rw, y in zip(hrows, ys):
            place_left(rw, 1.0, y)
        self.play(Create(ext), Create(bar_a), FadeIn(la), FadeIn(hrows[0]))
        self.glow(hrows[0][0], VGroup(bar_a, la), A_C)
        self.play(Create(ext_i), Create(bar_b), FadeIn(lb), FadeIn(hrows[1]))
        self.glow(hrows[1][0], VGroup(bar_b, lb), B_C)
        self.say("เส้นประส้ม = ยอดฟันของเฟืองอีกตัวที่ขบอยู่ ลงมาลึกได้แค่ a ใต้วงพิตช์ ช่องที่เหลือถึงโคนฟัน = c")
        self.play(Create(mate), Create(bar_c), FadeIn(lc), FadeIn(hrows[2]), run_time=1.4)
        self.glow(hrows[2][0], VGroup(bar_c, lc, mate), WARN)
        self.play(FadeIn(hrows[3]))
        self.glow(hrows[3][0], VGroup(bar_a, bar_b), WHITE)
        ex = M(r"m = 3\,\text{mm}:\ a = 3,\ b = 3.75,\ c = 0.75,\ h_t = 6.75\ \text{mm}", 28, GRAYTXT)
        ex.move_to([3.9, -1.9, 0])
        fit_width(ex, 5.9)
        self.play(FadeIn(ex))
        self.wait(3.0)

        # ---------------- A3: p, t, m, P
        self.play(FadeOut(VGroup(hrows, ex, ext, ext_i, mate, bar_a, bar_b, bar_c, la, lb, lc)))
        self.say("ระยะตามส่วนโค้งของวงพิตช์: circular pitch p, ความหนาฟัน t และ module m")
        psi = PI / (2 * N)
        step = TAU / N
        a_t0, a_t1 = PI / 2 - psi, PI / 2 + psi
        t_arc = Arc(radius=R, start_angle=a_t0, angle=2 * psi, arc_center=CG, color=A_C,
                    stroke_width=7)
        s_arc = Arc(radius=R, start_angle=a_t1, angle=2 * psi, arc_center=CG, color=B_C,
                    stroke_width=7)
        Rp = Ro + 0.38
        p_arc = Arc(radius=Rp, start_angle=a_t0, angle=step, arc_center=CG, color=WHITE,
                    stroke_width=3)
        p_arc.add_tip(tip_length=0.14, tip_width=0.14)
        p_arc.add_tip(tip_length=0.14, tip_width=0.14, at_start=True)
        ticks = VGroup(Line(polar(CG, R, a_t0), polar(CG, Rp + 0.1, a_t0), stroke_width=1.5),
                       Line(polar(CG, R, a_t0 + step), polar(CG, Rp + 0.1, a_t0 + step),
                            stroke_width=1.5))
        lt = M("t", 28, A_C).move_to(polar(CG, R + 0.32, PI / 2))
        ls = T("space", 17, B_C).move_to(polar(CG, R + 0.32, PI / 2 + step / 2))
        lp = M("p", 30).move_to(polar(CG, Rp + 0.32, PI / 2 + step / 4))

        # inset: whole gear for D and N
        IC = P2(-5.2, -2.5)
        Rin = 0.95
        inset = gear_mob(24, 2 * Rin / 24, IC, GEAR_IN, rot=PI / 2, fill=0.35, sw=1.5)
        inset_p = Circle(radius=Rin, color=PITCH_C, stroke_width=2).move_to(IC)
        dline = DoubleArrow(IC + LEFT * Rin, IC + RIGHT * Rin, buff=0, color=PITCH_C,
                            stroke_width=3, tip_length=0.14)
        lD = M(r"D = 2R = mN", 26, PITCH_C).move_to(IC + DOWN * 1.33)
        lN = M(r"N = 24", 28).move_to(IC + RIGHT * 1.75)

        prow = VGroup(
            row(M(r"p = \frac{\pi D}{N} = \pi m", 30), T("circular pitch: วัดตามโค้งวงพิตช์", 19)),
            row(M(r"t = \frac{p}{2}", 30, A_C), T("ความหนาฟัน = ช่องฟัน (ไม่มี backlash)", 19, A_C)),
            row(M(r"m = \frac{D}{N} = \frac{p}{\pi}", 30, GEAR_IN), T("module (mm) = ขนาดฟัน", 19, GEAR_IN)),
            row(M(r"P = \frac{N}{D},\ \ pP = \pi", 30, GEAR_MID), T("diametral pitch (ฟัน/นิ้ว)", 19, GEAR_MID)),
            row(M(r"m\,[\text{mm}] = \frac{25.4}{P}", 30, WARN), T("กับดักหน่วย: P=10 → m=2.54 mm", 19, WARN)),
        )
        for rw, y in zip(prow, [1.35, 0.55, -0.25, -1.05, -1.85]):
            place_left(rw, 1.0, y)
        self.play(Create(ticks), Create(p_arc), FadeIn(lp), FadeIn(prow[0]))
        self.glow(prow[0][0], VGroup(p_arc, lp), WHITE)
        self.play(Create(t_arc), Create(s_arc), FadeIn(lt), FadeIn(ls), FadeIn(prow[1]))
        self.glow(prow[1][0], VGroup(t_arc, s_arc, lt, ls), A_C)
        self.say("D กับ N เป็นของเฟืองทั้งวง (รูปเล็กซ้ายล่าง): m = D/N ระบบเมตริก, P = N/D ระบบนิ้ว")
        self.play(FadeIn(inset), Create(inset_p), GrowFromCenter(dline), FadeIn(lD), FadeIn(lN))
        self.play(FadeIn(prow[2]))
        self.glow(prow[2][0], VGroup(dline, lD, lN, p_arc), GEAR_IN)
        self.play(FadeIn(prow[3]))
        self.glow(prow[3][0], VGroup(dline, lN), GEAR_MID)
        self.play(FadeIn(prow[4]))
        self.glow(prow[4][0], None, WARN)
        ex2 = M(r"m = 3:\ p = 9.42\ \text{mm},\ t = 4.71\ \text{mm}", 28, GRAYTXT).move_to([3.9, -2.75, 0])
        self.play(FadeIn(ex2))
        self.wait(3.0)

        # ---------------- B: a meshing pair -> P, C, line of action, phi, Rb, Z, interference
        self.play(FadeOut(Group(*[mo for mo in self.mobjects if mo not in (ttl, ref, self._cap)])),
                  run_time=0.8)
        self.say("เฟือง 2 ตัวขบกัน (รูปประกอบ 18T ขับ 24T): วงพิตช์ 2 วงกลิ้งกันโดยไม่ไถล")
        mb = 0.2
        N1, N2 = 18, 24
        R1, R2 = mb * N1 / 2, mb * N2 / 2
        O1, O2 = P2(-5.0, -0.5), P2(-5.0 + R1 + R2, -0.5)
        Pp = O1 + RIGHT * R1
        g1 = gear_mob(N1, mb, O1, GEAR_IN, rot=0.0, fill=0.8)
        g2 = gear_mob(N2, mb, O2, GEAR_OUT, rot=PI + PI / N2, fill=0.8)
        self.play(FadeIn(g1), FadeIn(g2))
        w = 0.6
        g1.add_updater(lambda mo, dt: mo.rotate(w * dt, about_point=O1))
        g2.add_updater(lambda mo, dt: mo.rotate(-w * N1 / N2 * dt, about_point=O2))
        self.wait(4.5)
        g1.clear_updaters()
        g2.clear_updaters()
        self.play(g1.animate.set_opacity(0.22), g2.animate.set_opacity(0.22))

        pc1 = Circle(radius=R1, color=PITCH_C, stroke_width=3).move_to(O1)
        pc2 = Circle(radius=R2, color=PITCH_C, stroke_width=3).move_to(O2)
        loc = Line(O1, O2, color=WHITE, stroke_width=2)
        dots = VGroup(Dot(O1, radius=0.06), Dot(O2, radius=0.06), Dot(Pp, radius=0.07, color=PITCH_C))
        lO1 = M("O_1", 26).move_to(O1 + DOWN * 0.32)
        lO2 = M("O_2", 26).move_to(O2 + DOWN * 0.32)
        lR1 = M("R_1", 26, PITCH_C).move_to((O1 + Pp) / 2 + UP * 0.25)
        lR2 = M("R_2", 26, PITCH_C).move_to((Pp + O2) / 2 + UP * 0.25)
        p_lead = DashedLine(Pp, Pp + DOWN * 2.35, color=PITCH_C, stroke_width=2)
        lP = VGroup(M("P", 28, PITCH_C), T("= pitch point", 18, PITCH_C)).arrange(RIGHT, buff=0.12)
        lP.move_to(Pp + DOWN * 2.62)
        yC = -3.62
        cbar = DoubleArrow(P2(O1[0], yC), P2(O2[0], yC), buff=0, stroke_width=3, tip_length=0.14)
        cext = VGroup(DashedLine(O1, P2(O1[0], yC - 0.1), stroke_width=1.5, stroke_opacity=0.8),
                      DashedLine(O2, P2(O2[0], yC - 0.1), stroke_width=1.5, stroke_opacity=0.8))
        lC = M(r"C", 30).next_to(cbar, LEFT, buff=0.15)

        brows = VGroup(
            stack(M(r"C = R_1 + R_2 = \frac{m(N_1+N_2)}{2}", 30), T("ระยะศูนย์กลาง (center distance)", 18)),
            stack(T("line of action: เส้นสัมผัสร่วม base circle", 19, LOA_C),
                  T("= ทิศแรงที่ฟันดันกัน", 19, LOA_C)),
            stack(M(r"R_{b1} = R_1\cos\phi,\ \ \phi = 20^\circ", 30, BASE_C),
                  T("pressure angle (มุมกด) มาตรฐาน 20 องศา", 19, BASE_C)),
            stack(M(r"m_p = \frac{Z}{p_b} > 1\ (\ge 1.4),\ \ p_b = p\cos\phi", 30, Z_C),
                  T("Z = ช่วงสัมผัสจริง (เส้นเหลือง)", 19, Z_C)),
            stack(M(r"N_{min} = \frac{2k}{\sin^2\phi} = 17.1 \Rightarrow 18", 30, WARN),
                  T("เลยจุดม่วง = สัมผัสใต้ base circle = interference", 19, WARN)),
        )
        for rw, y in zip(brows, [1.75, 0.75, -0.25, -1.25, -2.25]):
            place_left(rw, 2.25, y)

        self.say("P = จุดที่วงพิตช์ 2 วงสัมผัสกัน บนเส้นต่อศูนย์กลาง → ระยะศูนย์กลาง C = R1 + R2")
        self.play(Create(pc1), Create(pc2), Create(loc), FadeIn(dots), FadeIn(lO1), FadeIn(lO2),
                  FadeIn(lR1), FadeIn(lR2))
        self.play(Create(p_lead), FadeIn(lP), Create(cext), GrowFromCenter(cbar), FadeIn(lC),
                  FadeIn(brows[0]))
        self.glow(brows[0][0], VGroup(cbar, lC, lR1, lR2), WHITE)
        self.wait(1.0)

        d = np.array([np.sin(PHI), np.cos(PHI), 0.0])
        E1 = Pp + float(np.dot(O1 - Pp, d)) * d
        E2 = Pp + float(np.dot(O2 - Pp, d)) * d
        Rb1, Rb2 = R1 * np.cos(PHI), R2 * np.cos(PHI)
        loa = Line(Pp - 1.9 * d, Pp + 1.75 * d, color=LOA_C, stroke_width=4)
        lLOA = T("line of action", 17, LOA_C).move_to([-4.1, -2.62, 0])
        bc1 = Circle(radius=Rb1, color=BASE_C, stroke_width=2.5).move_to(O1)
        bc2 = Circle(radius=Rb2, color=BASE_C, stroke_width=2.5).move_to(O2)
        r_e1 = Line(O1, E1, color=BASE_C, stroke_width=3)
        r_e2 = Line(O2, E2, color=BASE_C, stroke_width=3)
        eds = VGroup(Dot(E1, radius=0.07, color=BASE_C), Dot(E2, radius=0.07, color=BASE_C))
        ra1 = RightAngle(Line(E1, O1), Line(E1, E1 + d), length=0.14, color=BASE_C, stroke_width=2)
        ra2 = RightAngle(Line(E2, O2), Line(E2, E2 - d), length=0.14, color=BASE_C, stroke_width=2)
        self.say("line of action = เส้นสัมผัสร่วมของ base circle ทั้งสอง (สีม่วง) แรงฟันส่งตามเส้นนี้เสมอ")
        self.play(Create(bc1), Create(bc2), run_time=1.0)
        self.play(Create(loa), FadeIn(lLOA), Create(r_e1), Create(r_e2), FadeIn(eds),
                  Create(ra1), Create(ra2), FadeIn(brows[1]))
        self.glow(brows[1][0], VGroup(loa, lLOA), LOA_C)
        self.wait(1.0)

        ang_o = Arc(radius=0.85, start_angle=-PHI, angle=PHI, arc_center=O1, color=WHITE,
                    stroke_width=3)
        ang_p = Arc(radius=0.45, start_angle=PI / 2 - PHI, angle=PHI, arc_center=Pp, color=WHITE,
                    stroke_width=3)
        lphi = M(r"\phi", 30).move_to(polar(O1, 1.22, -PHI / 2))
        lRb = M(r"R_{b1}", 26, BASE_C).move_to((O1 + E1) / 2 + 0.3 * np.array([-np.sin(PHI), -np.cos(PHI), 0]))
        self.say("สามเหลี่ยมมุมฉาก O1-P-จุดม่วง: มุมที่ O1 = pressure angle φ → R_b1 = R1 cos φ")
        self.play(Create(ang_o), Create(ang_p), FadeIn(lphi), FadeIn(lRb), FadeIn(brows[2]))
        self.glow(brows[2][0], VGroup(r_e1, lRb, ang_o, ang_p, lphi, lR1), BASE_C)
        self.wait(1.0)

        Ro1, Ro2 = R1 + mb, R2 + mb
        B = E1 + np.sqrt(Ro1 ** 2 - Rb1 ** 2) * d
        A = E2 - np.sqrt(Ro2 ** 2 - Rb2 ** 2) * d
        zseg = Line(A, B, color=Z_C, stroke_width=9)
        lZ = M("Z", 30, Z_C).move_to([-2.75, -0.78, 0])
        self.say("ฟันเริ่มสัมผัสที่ยอดฟันเฟืองตาม และเลิกสัมผัสที่ยอดฟันเฟืองขับ → ช่วงนั้นคือ Z (เส้นเหลือง)")
        self.play(g1.animate.set_opacity(0.45), g2.animate.set_opacity(0.45), run_time=0.5)
        self.play(Create(zseg), FadeIn(lZ), FadeIn(brows[3]), g1.animate.set_opacity(0.22),
                  g2.animate.set_opacity(0.22))
        self.glow(brows[3][0], VGroup(zseg, lZ), Z_C)
        self.wait(1.0)
        self.say("Z ต้องอยู่ระหว่างจุดม่วง 2 จุด ถ้าเลยออกไป = ฟันสัมผัสใต้ base circle = interference")
        self.play(FadeIn(brows[4]))
        self.play(Flash(E1, color=BASE_C, flash_radius=0.3), Flash(E2, color=BASE_C, flash_radius=0.3),
                  Indicate(bc1, color=WHITE, scale_factor=1.0), run_time=1.3)
        self.glow(brows[4][0], VGroup(eds, bc1, bc2), WARN)
        self.wait(4.0)


# =====================================================================
# G41 -- reverted compound gear train design, 30:1 (ข)
# =====================================================================
class G41_ExamRevertedDesign(ExamScene):
    def construct(self):
        self.add(title("ออกแบบ Reverted compound gear train 30:1", size=28))
        self.add(page_ref("HW6B ข้อ 1"))

        s = 0.27
        yA = 0.75
        C_in = 6.30
        yC = yA - C_in * s
        x23, x45 = -4.6, -2.3
        Rg = {2: 0.9 * s, 3: 5.4 * s, 4: 1.05 * s, 5: 5.25 * s}
        col = {2: GEAR_IN, 3: GEAR_MID, 4: GEAR_MID, 5: GEAR_OUT}
        cen = {2: P2(x23, yA), 3: P2(x23, yC), 4: P2(x45, yC), 5: P2(x45, yA)}
        gears = {i: Rectangle(width=0.2, height=2 * Rg[i], color=col[i], fill_opacity=0.7,
                              stroke_width=2).move_to(cen[i]) for i in (2, 3, 4, 5)}
        axis = DashedLine(P2(-6.75, yA), P2(-0.45, yA), color=GRAYTXT, stroke_width=1.5,
                          dash_length=0.12)
        sh_in = Line(P2(-6.6, yA), P2(x23 + 0.12, yA), color=METAL, stroke_width=7)
        sh_out = Line(P2(x45 - 0.12, yA), P2(-0.6, yA), color=METAL, stroke_width=7)
        sh_c = Line(P2(x23 - 0.3, yC), P2(x45 + 0.3, yC), color=METAL, stroke_width=7)
        l_in = T("เพลาเข้า", 18, GRAYTXT).move_to([-6.05, yA + 0.3, 0])
        l_out = T("เพลาออก", 18, GRAYTXT).move_to([-1.05, yA + 0.3, 0])
        l_c = T("เพลาทด (3+4)", 17, GRAYTXT).move_to([(x23 + x45) / 2 + 0.1, yC - 0.32, 0])
        tpos = {2: P2(-5.05, yA + 0.75), 3: P2(-5.25, yC - 1.0), 4: P2(-1.75, yC - 0.62),
                5: P2(-1.6, yA + 1.15)}
        tag = {i: M("N_%d" % i, 28, col[i]).move_to(tpos[i]) for i in (2, 3, 4, 5)}
        c1 = DoubleArrow(P2(-5.75, yA), P2(-5.75, yC), buff=0, stroke_width=3, tip_length=0.14)
        c2 = DoubleArrow(P2(-1.45, yA), P2(-1.45, yC), buff=0, stroke_width=3, tip_length=0.14)
        lc1 = M("C_1", 28).next_to(c1, LEFT, buff=0.12)
        lc2 = M("C_2", 28).next_to(c2, RIGHT, buff=0.12)

        self.say("ภาพด้านข้าง: เพลาเข้า → 2 ขบ 3 → (3, 4 อยู่เพลาทดเดียวกัน) → 4 ขบ 5 → เพลาออก")
        self.play(Create(axis), Create(sh_in), Create(sh_out), Create(sh_c),
                  *[FadeIn(g) for g in gears.values()], FadeIn(l_in), FadeIn(l_out), FadeIn(l_c),
                  run_time=1.6)
        self.play(*[FadeIn(t) for t in tag.values()])
        self.wait(1.5)

        X0 = 0.1

        def panel(*mobs, top=2.05, gap=0.22):
            g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=gap)
            fit_width(g, 6.75)
            g.move_to([X0 + g.width / 2, top - g.height / 2, 0])
            return g

        # step 1
        s1 = panel(T("ขั้น 1 — เข้าใจโจทย์", 22, OK),
                   M(r"e = \frac{\omega_{in}}{\omega_{out}} = \frac{\omega_2}{\omega_5} = 30", 32),
                   M(r"P = 10\ \text{teeth/in},\ \ \phi = 20^\circ\ \text{full depth}", 30),
                   T("reverted = เพลาเข้ากับเพลาออก อยู่แนวเดียวกัน (เส้นประ)", 19))
        self.say("ขั้น 1: อัตราทด 30 เท่า เฟืองขนาด P = 10 ฟัน/นิ้ว และเพลาเข้า-ออกต้องตรงแนวกัน")
        self.play(FadeIn(s1))
        self.glow(s1[1], VGroup(gears[2], gears[5]), WHITE)
        self.glow(s1[3], axis, GRAYTXT)
        self.wait(1.5)

        # step 2
        s2 = panel(T("ขั้น 2 — เขียน 2 สมการบังคับ", 22, OK),
                   M(r"\frac{N_3}{N_2}\cdot\frac{N_5}{N_4} = 30", 34),
                   M(r"C_1 = \frac{N_2 + N_3}{2P},\ \ C_2 = \frac{N_4 + N_5}{2P}", 32),
                   M(r"C_1 = C_2\ \Rightarrow\ N_2 + N_3 = N_4 + N_5", 34, WARN),
                   T("(module/P เท่ากัน ตัดกันหายไป)", 18, GRAYTXT))
        self.say("ขั้น 2: อัตราทดรวม = ผลคูณ 2 stage และเงื่อนไข coaxial: ระยะศูนย์กลาง C1 = C2")
        self.play(FadeOut(s1), run_time=0.35)
        self.play(FadeIn(s2))
        self.glow(s2[1], VGroup(*tag.values()), WHITE)
        self.play(GrowFromCenter(c1), FadeIn(lc1))
        self.glow(s2[2], VGroup(c1, lc1, gears[2], gears[3]), WHITE)
        self.play(GrowFromCenter(c2), FadeIn(lc2))
        self.glow(s2[2], VGroup(c2, lc2, gears[4], gears[5]), WHITE)
        self.glow(s2[3], VGroup(c1, c2, axis), WARN)
        self.wait(1.5)

        # step 3
        s3 = panel(T("ขั้น 3 — แบ่ง 30 เป็น 2 stage", 22, OK),
                   VGroup(M(r"\sqrt{30} = 5.48", 30), T("ไม่ลงตัว → แบ่งไม่เท่ากัน", 19)).arrange(RIGHT, buff=0.25),
                   M(r"30 = 6 \times 5:\ \ \frac{N_3}{N_2} = 6,\ \ \frac{N_5}{N_4} = 5", 32),
                   M(r"N_2 + 6N_2 = N_4 + 5N_4\ \Rightarrow\ 7N_2 = 6N_4", 32),
                   VGroup(M(r"\frac{N_4}{N_2} = \frac{7}{6}", 34, WARN),
                          T("→ N2 ต้องหาร 6 ลงตัว", 19, WARN)).arrange(RIGHT, buff=0.25))
        self.say("ขั้น 3: แทน N3 = 6N2, N5 = 5N4 ลงเงื่อนไข coaxial ได้สัดส่วนพินเนียน 2 ตัว")
        self.play(FadeOut(s2), run_time=0.35)
        self.play(FadeIn(s3))
        self.glow(s3[2], VGroup(gears[2], gears[3], gears[4], gears[5]), WHITE)
        self.glow(s3[3], VGroup(tag[2], tag[4]), WHITE)
        self.glow(s3[4][0], VGroup(gears[2], gears[4], tag[2], tag[4]), WARN)
        self.wait(1.5)

        # step 4
        s4 = panel(T("ขั้น 4 — เลือกจำนวนฟัน (กัน interference)", 22, OK),
                   M(r"N_{min} = \frac{2}{\sin^2 20^\circ} = 17.1\ \Rightarrow\ N \ge 18", 32),
                   M(r"N_2 = 18\ \Rightarrow\ N_4 = \tfrac{7}{6}(18) = 21", 32),
                   M(r"N_3 = 6(18) = 108,\ \ N_5 = 5(21) = 105", 32),
                   T("18 = ค่าเล็กสุดที่ ≥ 18 และหาร 6 ลงตัว → ชุดเฟืองเล็กสุด", 19, GRAYTXT))
        self.say("ขั้น 4: พินเนียนต้องไม่ต่ำกว่า 18 ฟัน (φ = 20° full-depth) เลือก N2 = 18 ที่หาร 6 ลงตัว")
        self.play(FadeOut(s3), run_time=0.35)
        self.play(FadeIn(s4))
        self.glow(s4[1], VGroup(gears[2], gears[4]), WHITE)
        new_tag = {i: M("N_%d = %d" % (i, n), 28, col[i]) for i, n in ((2, 18), (3, 108), (4, 21), (5, 105))}
        for i in (2, 3):
            new_tag[i].move_to([-4.85 - new_tag[i].width / 2, tpos[i][1], 0])
        for i in (4, 5):
            new_tag[i].move_to([-2.05 + new_tag[i].width / 2, tpos[i][1], 0])
        self.play(ReplacementTransform(tag[2], new_tag[2]), ReplacementTransform(tag[4], new_tag[4]))
        self.glow(s4[2], VGroup(new_tag[2], new_tag[4], gears[2], gears[4]), WHITE)
        self.play(ReplacementTransform(tag[3], new_tag[3]), ReplacementTransform(tag[5], new_tag[5]))
        self.glow(s4[3], VGroup(new_tag[3], new_tag[5], gears[3], gears[5]), WHITE)
        tag = new_tag
        self.wait(1.5)

        # step 5
        s5 = panel(T("ขั้น 5 — ขนาดเฟือง D = N/P (นิ้ว)", 22, OK),
                   M(r"D_2 = \frac{18}{10} = 1.80,\ \ D_3 = \frac{108}{10} = 10.80", 32),
                   M(r"D_4 = \frac{21}{10} = 2.10,\ \ D_5 = \frac{105}{10} = 10.50", 32),
                   M(r"a = \tfrac{1}{P} = 0.1\ \text{in},\ \ b = \tfrac{1.25}{P} = 0.125\ \text{in}", 30, GRAYTXT),
                   T("ความสูงแท่งในรูป = D ของแต่ละเฟือง (วาดตามสเกลจริง)", 19, GRAYTXT))
        self.say("ขั้น 5: เส้นผ่านศูนย์กลางพิตช์ D = N/P ความสูงแต่ละแท่งในรูปคือ D ตามสเกลจริง")
        self.play(FadeOut(s4), run_time=0.35)
        self.play(FadeIn(s5))
        self.glow(s5[1], VGroup(gears[2], gears[3]), WHITE)
        self.glow(s5[2], VGroup(gears[4], gears[5]), WHITE)
        self.wait(1.5)

        # step 6
        s6 = panel(T("ขั้น 6 — ตรวจ", 22, OK),
                   M(r"C_1 = \frac{1.80 + 10.80}{2} = 6.30\ \text{in}", 32),
                   M(r"C_2 = \frac{2.10 + 10.50}{2} = 6.30\ \text{in}\ \checkmark", 32, OK),
                   M(r"e = \frac{108}{18}\cdot\frac{105}{21} = 6 \times 5 = 30\ \checkmark", 32, OK),
                   T("พินเนียน 18 และ 21 ฟัน ≥ 18 → ไม่ interference (ตรวจละเอียดในโน้ต ข.4 ก็ผ่าน)", 19, OK))
        self.say("ขั้น 6: ตรวจ C1 = C2 = 6.30 นิ้ว (เพลาตรงแนว) อัตราทด = 30 และพินเนียนไม่ต่ำกว่า 18 ฟัน")
        self.play(FadeOut(s5), run_time=0.35)
        self.play(FadeIn(s6))
        self.glow(s6[1], VGroup(c1, lc1), WHITE)
        self.glow(s6[2], VGroup(c2, lc2), OK)
        self.glow(s6[3], VGroup(*tag.values()), OK)
        self.glow(s6[4], VGroup(gears[2], gears[4]), OK)
        self.wait(2.0)

        # step 7: direction, end views of each stage rotating
        self.say("ขั้น 7: ทิศ — ภาพมองตามแนวเพลา stage 1 (2→3) กับ stage 2 (4→5) ระยะ C เท่ากัน")
        side = VGroup(axis, sh_in, sh_out, sh_c, *gears.values(), l_in, l_out, l_c, *tag.values(),
                      c1, c2, lc1, lc2)
        self.play(FadeOut(side), FadeOut(s6))
        eA, eB = -5.0, -1.75
        oi1, oc1 = P2(eA, yA), P2(eA, yC)
        oi2, oc2 = P2(eB, yA), P2(eB, yC)
        e2 = gear_shape(Rg[2], 18, GEAR_IN, tooth_depth_frac=0.22, fill_opacity=0.85).move_to(oi1)
        e3 = gear_shape(Rg[3], 108, GEAR_MID, tooth_depth_frac=0.05, fill_opacity=0.45).move_to(oc1)
        e4 = gear_shape(Rg[4], 21, GEAR_MID, tooth_depth_frac=0.2, fill_opacity=0.85).move_to(oc2)
        e5 = gear_shape(Rg[5], 105, GEAR_OUT, tooth_depth_frac=0.05, fill_opacity=0.45).move_to(oi2)
        mk = VGroup(Dot(oi1 + UP * 0.16, radius=0.04), Dot(oc1 + UP * 1.2, radius=0.05),
                    Dot(oc2 + UP * 0.18, radius=0.04), Dot(oi2 + UP * 1.15, radius=0.05))
        st1 = T("stage 1 (2→3)", 19).move_to([eA - 1.0, yA + 0.95, 0])
        st2 = T("stage 2 (4→5)", 19).move_to([eB, yC - 0.85, 0])
        lev = VGroup(DashedLine(P2(-6.9, yA), P2(0.0, yA), stroke_width=1.5, color=GRAYTXT),
                     DashedLine(P2(-6.9, yC), P2(0.0, yC), stroke_width=1.5, color=GRAYTXT))
        self.play(FadeIn(e3), FadeIn(e2), FadeIn(e5), FadeIn(e4), FadeIn(mk), FadeIn(st1), FadeIn(st2),
                  Create(lev))
        w2 = 1.5
        rate = {0: w2, 1: -w2 / 6, 2: -w2 / 6, 3: w2 / 30}
        bodies = [(VGroup(e2, mk[0]), oi1, rate[0]), (VGroup(e3, mk[1]), oc1, rate[1]),
                  (VGroup(e4, mk[2]), oc2, rate[2]), (VGroup(e5, mk[3]), oi2, rate[3])]
        a2 = arc_arrow(oi1, 0.45, PI * 0.55, 0.8 * PI, GEAR_IN)
        a3 = arc_arrow(oc1, 1.62, PI * 1.6, -0.3 * PI, GEAR_MID)
        a5 = arc_arrow(oi2, 1.6, PI * 0.05, 0.3 * PI, GEAR_OUT)
        l2 = T("ccw", 17, GEAR_IN).move_to(oi1 + P2(-0.15, 0.62))
        l3 = T("cw", 17, GEAR_MID).move_to(polar(oc1, 1.9, PI * 1.45))
        l5 = T("ccw (ช้าลง 30 เท่า)", 17, GEAR_OUT).move_to(polar(oi2, 2.0, PI * 0.12) + RIGHT * 1.0)
        s7 = panel(T("ขั้น 7 — ทิศการหมุน", 22, OK),
                   M(r"\frac{\omega_5}{\omega_2} = \left(-\frac{N_2}{N_3}\right)\left(-\frac{N_4}{N_5}\right) = +\frac{1}{30}", 32),
                   T("ขบนอก 2 ครั้ง: (−)(−) = + → ทิศเดียวกับเพลาเข้า", 19),
                   T("เฟือง 3, 4 อยู่เพลาเดียวกัน หมุนเท่ากัน (cw)", 19, GEAR_MID),
                   T("ระดับแกน (เส้นประ) เท่ากันทั้ง 2 stage = coaxial", 19, GRAYTXT))
        fit_width(s7, 5.9)
        place_left(s7, 1.0, 0.9 - s7.height / 2)
        self.play(FadeIn(s7), Create(a2), Create(a3), Create(a5), FadeIn(l2), FadeIn(l3), FadeIn(l5))
        for mob, c, r in bodies:
            mob.add_updater(lambda mo, dt, c=c, r=r: mo.rotate(r * dt, about_point=c))
        self.wait(6.0)
        for mob, c, r in bodies:
            mob.clear_updaters()
        ans = VGroup(T("คำตอบ", 22, OK),
                     M(r"18/108\ +\ 21/105,\ \ C = 6.30\ \text{in},\ \ e = 30", 32, OK)).arrange(RIGHT, buff=0.3)
        fit_width(ans, 5.4)
        box = SurroundingRectangle(ans, color=OK, buff=0.15)
        VGroup(ans, box).move_to([3.85, -2.75, 0])
        self.play(FadeIn(ans), Create(box))
        self.wait(4.0)


# =====================================================================
# G42 -- planetary Example 7.4 (ค.5): formula + tabular
# =====================================================================
class G42_ExamPlanetaryEx74(ExamScene):
    def construct(self):
        self.add(title("Planetary gear train — Example 7.4 (2 วิธี)", size=28))
        self.add(page_ref("สไลด์หน้า 68, 73"))

        O = P2(-3.7, -0.55)
        ms = 0.06
        Ns, Np, Nr = 40, 20, 80
        Rs, Rp, Rr = ms * Ns / 2, ms * Np / 2, ms * Nr / 2
        Rring = Rr + 0.38
        th0 = PI / 2
        rot_s = th0
        rot_p = th0 + PI + PI / Np
        rot_r = th0 + PI / Nr
        ring0 = ring_mob(Nr, ms, O, Rring, RING_G, rot=rot_r, fill=0.6)
        sun0 = gear_mob(Ns, ms, O, GEAR_IN, rot=rot_s, fill=0.75)
        pc0 = polar(O, Rs + Rp, th0)
        pl0 = gear_mob(Np, ms, pc0, GEAR_MID, rot=rot_p, fill=0.8)
        sdot0 = Dot(polar(O, 0.95, th0 + PI * 0.75), radius=0.06, color=WHITE)
        pdot0 = Dot(polar(pc0, 0.38, th0), radius=0.05, color=WHITE)
        arm0 = VGroup(Line(O, pc0, color=ARM_G, stroke_width=12),
                      Dot(O, radius=0.09, color=ARM_G), Dot(pc0, radius=0.08, color=ARM_G))
        ring, sun, pl = ring0.copy(), sun0.copy(), pl0.copy()
        sdot, pdot, arm = sdot0.copy(), pdot0.copy(), arm0.copy()
        rig = VGroup(ring, sun, pl, sdot, pdot, arm)
        self.ang = dict(A=0.0, S=0.0, P=0.0, R=0.0)

        def pose(a):
            ring.become(ring0.copy().rotate(a["R"], about_point=O))
            sun.become(sun0.copy().rotate(a["S"], about_point=O))
            sdot.become(sdot0.copy().rotate(a["S"], about_point=O))
            pl.become(pl0.copy().rotate(a["P"] - a["A"], about_point=pc0).rotate(a["A"], about_point=O))
            pdot.become(pdot0.copy().rotate(a["P"] - a["A"], about_point=pc0).rotate(a["A"], about_point=O))
            arm.become(arm0.copy().rotate(a["A"], about_point=O))

        def run(rates, run_time):
            tk = ValueTracker(0.0)
            a0 = dict(self.ang)

            def upd(mo):
                t = tk.get_value()
                pose({k: a0[k] + rates[k] * t for k in a0})
            rig.add_updater(upd)
            self.play(tk.animate.set_value(run_time), run_time=run_time, rate_func=linear)
            rig.remove_updater(upd)
            self.ang = {k: a0[k] + rates[k] * run_time for k in a0}
            pose(self.ang)

        def tags_at():
            t1 = M("1", 30, RING_G).move_to(polar(O, Rring + 0.32, PI * 0.78))
            t2 = M("2", 30, WHITE).move_to(O + DOWN * 0.48)
            t3 = M("3", 30, GEAR_MID).move_to(pc0 + RIGHT * 0.9)
            t4 = M("4", 30, ARM_G).move_to(O + P2(-0.38, 0.75))
            return VGroup(bg(t1), bg(t2), bg(t3), bg(t4))

        self.say("ชุดเฟืองดาวเคราะห์: ring 1 (ฟันใน), sun 2, planet 3 บน arm 4 (โปรไฟล์อินโวลูทจริง)")
        self.play(FadeIn(ring), FadeIn(sun), FadeIn(pl), FadeIn(sdot), FadeIn(pdot), run_time=1.2)
        self.play(Create(arm[0]), FadeIn(arm[1:]))
        tags = tags_at()
        self.play(FadeIn(tags))

        X0 = -0.45

        def panel(*mobs, top=2.1, gap=0.2, max_w=7.2):
            g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=gap)
            fit_width(g, max_w)
            g.move_to([X0 + g.width / 2, top - g.height / 2, 0])
            return g

        # step 1: understand
        legend = panel(
            T("ขั้น 1 — เข้าใจโจทย์ (กำหนด ccw = +)", 22, OK),
            VGroup(T("1 ring 80T ตรึง", 20, RING_G), M(r"\omega_{11} = 0", 30, RING_G)).arrange(RIGHT, buff=0.3),
            VGroup(T("4 arm หมุน ccw", 20, ARM_G), M(r"\omega_{41} = +50\ \text{rad/s}", 30, ARM_G)).arrange(RIGHT, buff=0.3),
            VGroup(T("2 sun 40T หา", 20, GEAR_IN), M(r"\omega_{21} = ?", 30, GEAR_IN)).arrange(RIGHT, buff=0.3),
            VGroup(T("3 planet 20T", 20, GEAR_MID), M(r"N_3 = 20", 30, GEAR_MID)).arrange(RIGHT, buff=0.3),
            M(r"N_1 = N_2 + 2N_3:\ \ 80 = 40 + 2(20)\ \checkmark", 30, GRAYTXT),
            T("รู้ 2 ค่า (ring, arm) พอสำหรับระบบ 2 DOF", 19, GRAYTXT))
        self.say("ขั้น 1: ring ถูกตรึง (ω = 0), arm หมุนทวนเข็ม 50 rad/s → หาความเร็ว sun")
        self.play(FadeIn(legend))
        self.glow(legend[1][1], VGroup(ring, tags[0]), RING_G)
        self.glow(legend[2][1], VGroup(arm, tags[3]), ARM_G)
        self.glow(legend[3][1], VGroup(sun, tags[1]), GEAR_IN)
        self.glow(legend[4][1], VGroup(pl, tags[2]), GEAR_MID)
        self.glow(legend[5], VGroup(ring, sun, pl), GRAYTXT)
        self.wait(1.5)

        # step 2: formula method -- arm fixed motion gives e
        f1 = panel(
            T("วิธีที่ 1 — สูตร: นั่งไปกับ arm (ตรึง arm)", 22, OK),
            T("F = sun 2, L = ring 1 (แกนไม่โคจรทั้งคู่)", 19),
            VGroup(M(r"2\to3:\ \text{external}\ (-)", 30),
                   M(r"3\to1:\ \text{internal}\ (+)", 30)).arrange(RIGHT, buff=0.6),
            M(r"e = \frac{\omega_{14}}{\omega_{24}} = \left(-\frac{N_2}{N_3}\right)\left(+\frac{N_3}{N_1}\right)", 32),
            M(r"e = \left(-\frac{40}{20}\right)\left(+\frac{20}{80}\right) = -\frac{1}{2}", 32, WARN))
        self.say("ตรึง arm: กลายเป็นชุดเฟืองแกนตายตัวธรรมดา — ดูว่า ring หมุนเทียบกับ sun ยังไง")
        self.play(FadeOut(legend), run_time=0.35)
        self.play(FadeIn(f1[0]), FadeIn(f1[1]))
        self.glow(f1[1], VGroup(sun, ring), WHITE)
        w = 0.45
        run(dict(A=0.0, S=w, P=-2 * w, R=-w / 2), 5.0)
        cs = Circle(radius=0.16, color=WHITE, stroke_width=3).move_to(polar(O, Rs, th0))
        cr = Circle(radius=0.16, color=WHITE, stroke_width=3).move_to(polar(O, Rr, th0))
        self.play(FadeIn(f1[2]))
        self.play(Create(cs))
        self.play(Indicate(f1[2][0], color=WHITE), Indicate(cs, color=WARN, scale_factor=1.3), run_time=1.3)
        self.play(FadeOut(cs), Create(cr))
        self.play(Indicate(f1[2][1], color=WHITE), Indicate(cr, color=WARN, scale_factor=1.3), run_time=1.3)
        self.play(FadeOut(cr), FadeIn(f1[3]))
        self.glow(f1[3], VGroup(sun, pl, ring), WHITE)
        self.play(FadeIn(f1[4]))
        self.say("e = −1/2: ตอน arm นิ่ง ring หมุนสวนทาง sun ด้วยความเร็วครึ่งหนึ่ง (เห็นในแอนิเมชันข้างบน)")
        self.wait(2.0)

        f2 = panel(
            T("แทนค่าความเร็วสัมบูรณ์ (ทุกตัวเทียบโครง)", 22, OK),
            M(r"e = \frac{\omega_{11} - \omega_{41}}{\omega_{21} - \omega_{41}}", 34),
            M(r"-\frac{1}{2} = \frac{0 - 50}{\omega_{21} - 50}", 34),
            M(r"\omega_{21} - 50 = 100", 34),
            M(r"\omega_{21} = +150\ \text{rad/s (ccw)}", 36, OK))
        self.say("ขั้น 3: แทน ring = 0, arm = 50 ลงสูตรทอง แล้วแก้หา ω ของ sun")
        self.play(FadeOut(f1), run_time=0.35)
        self.play(FadeIn(f2[0]), FadeIn(f2[1]))
        gl = list(f2[1][0])
        cy = f2[1].get_y()
        num = sorted([g for g in gl if g.get_y() > cy + 0.08], key=lambda g: g.get_x())
        den = sorted([g for g in gl if g.get_y() < cy - 0.08], key=lambda g: g.get_x())
        self.glow(VGroup(*num[0:3]), VGroup(ring, tags[0]), RING_G)
        self.glow(VGroup(*num[4:7]), VGroup(arm, tags[3]), ARM_G)
        self.glow(VGroup(*den[0:3]), VGroup(sun, tags[1]), GEAR_IN)
        self.play(FadeIn(f2[2]))
        self.play(FadeIn(f2[3]))
        self.play(FadeIn(f2[4]))
        self.glow(f2[4], VGroup(sun, tags[1]), OK)
        self.wait(2.5)

        # step 4: tabular method
        self.say("วิธีที่ 2 — ตาราง: ความเร็วจริง = (ล็อกหมุนทั้งก้อน X) + (ตรึง arm หมุน planet Y)")
        self.play(FadeOut(f2))
        cols = ["ring 1", "sun 2", "planet 3", "arm 4"]
        ccol = [RING_G, GEAR_IN, GEAR_MID, ARM_G]
        cells = [
            [r"X", r"X", r"X", r"X"],
            [r"+\tfrac{20}{80}Y = \tfrac{Y}{4}", r"-\tfrac{20}{40}Y = -\tfrac{Y}{2}", r"Y", r"0"],
            [r"X + \tfrac{Y}{4}", r"X - \tfrac{Y}{2}", r"X + Y", r"X"],
        ]
        rlab = ["1. ล็อกทั้งก้อน", "2. ตรึง arm", "รวม (จริง)"]
        cw_ = [1.55, 1.45, 1.55, 1.1, 0.8]
        xs = [X0]
        for c in cw_[:-1]:
            xs.append(xs[-1] + c)
        yh, dy = 2.0, 0.62
        head = VGroup(*[T(c, 18, cc).move_to([xs[i + 1] + cw_[i + 1] / 2, yh, 0])
                        for i, (c, cc) in enumerate(zip(cols, ccol))])
        rows_m = []
        for r in range(3):
            lab = T(rlab[r], 18, OK if r == 2 else WHITE)
            lab.move_to([xs[0] + lab.width / 2, yh - (r + 1) * dy, 0])
            cs_ = [fit_width(M(cells[r][i], 26, ccol[i]), cw_[i + 1] - 0.1).move_to(
                [xs[i + 1] + cw_[i + 1] / 2, yh - (r + 1) * dy, 0]) for i in range(4)]
            rows_m.append(VGroup(lab, *cs_))
        hl = Line(P2(X0, yh - dy / 2), P2(X0 + sum(cw_), yh - dy / 2), stroke_width=1.5, color=GRAYTXT)
        hl2 = Line(P2(X0, yh - 2.5 * dy), P2(X0 + sum(cw_), yh - 2.5 * dy), stroke_width=1.5, color=GRAYTXT)
        self.play(FadeOut(tags), FadeIn(head), Create(hl))
        self.play(FadeIn(rows_m[0]))
        self.say("แถว 1: ล็อกทุกชิ้นติดกัน หมุนไปด้วยกันทั้งก้อนด้วยความเร็ว X (รวม arm)")
        run(dict(A=TAU / 6, S=TAU / 6, P=TAU / 6, R=TAU / 6), 6.0)
        self.play(FadeIn(rows_m[1]))
        self.say("แถว 2: ตรึง arm (= 0) ให้ planet หมุน Y แล้วไล่อัตราทด: ring ขบใน +, sun ขบนอก −")
        run(dict(A=0.0, S=-0.25, P=0.5, R=0.125), 4.0)
        self.glow(rows_m[1][3], pl, GEAR_MID)
        self.play(Create(hl2), FadeIn(rows_m[2]))
        self.wait(1.0)

        sol = panel(
            M(r"\text{arm: } X = 50", 30, ARM_G),
            M(r"\text{ring: } 50 + \frac{Y}{4} = 0\ \Rightarrow\ Y = -200", 30, RING_G),
            M(r"\text{sun: } 50 - \frac{1}{2}(-200) = +150\ \text{rad/s (ccw)}", 30, GEAR_IN),
            M(r"\text{planet: } 50 + (-200) = -150\ \text{rad/s (cw)}", 30, GEAR_MID),
            top=-0.5, gap=0.16)
        tags = tags_at()
        self.say("รู้ arm กับ ring → ตั้ง 2 สมการจากแถวรวม แก้ X, Y แล้วอ่านคำตอบ")
        self.play(FadeIn(tags))
        self.play(FadeIn(sol[0]))
        self.glow(sol[0], VGroup(arm, tags[3]), ARM_G)
        self.play(FadeIn(sol[1]))
        self.glow(sol[1], VGroup(ring, tags[0]), RING_G)
        self.play(FadeIn(sol[2]))
        self.glow(sol[2], VGroup(sun, tags[1]), GEAR_IN)
        self.play(FadeIn(sol[3]))
        self.glow(sol[3], VGroup(pl, tags[2]), GEAR_MID)
        self.wait(2.0)

        # step 5: check + real motion
        self.play(FadeOut(VGroup(head, hl, hl2, *rows_m, sol)))
        chk = panel(
            T("ขั้น 4 — ตรวจ", 22, OK),
            T("สูตร = 150, ตาราง = 150 → ตรงกัน", 20, OK),
            M(r"\text{ring fixed: } \frac{\omega_S}{\omega_A} = 1 + \frac{N_R}{N_S} = 1 + \frac{80}{40} = 3", 30),
            M(r"\omega_{21} = 3(50) = 150\ \checkmark", 32, OK),
            T("ของจริง: ring นิ่ง, arm 50 ccw, sun 150 ccw, planet 150 cw", 19, GRAYTXT))
        self.say("ตรวจด้วยสูตรลัด ring ตรึง: sun เร็วกว่า arm 1 + 80/40 = 3 เท่า → 150 rad/s")
        self.play(FadeIn(chk))
        self.glow(chk[2], VGroup(ring, sun), WHITE)
        self.play(FadeOut(tags))
        self.say("การเคลื่อนที่จริง: ring นิ่ง, arm พา planet โคจรทวนเข็ม, sun หมุนเร็วกว่า arm 3 เท่า")
        wa = 0.25
        run(dict(A=wa, S=3 * wa, P=-3 * wa, R=0.0), 8.0)
        ans = VGroup(T("คำตอบ", 22, OK), M(r"\omega_{21} = +150\ \text{rad/s (ccw)}", 34, OK)).arrange(RIGHT, buff=0.3)
        box = SurroundingRectangle(ans, color=OK, buff=0.18)
        VGroup(ans, box).move_to([3.0, -2.9, 0])
        self.play(FadeIn(ans), Create(box))
        self.wait(4.0)
