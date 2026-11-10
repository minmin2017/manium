"""Fluid Power Control exam clips, batch D (2026-11-10, exam 11 Nov).

Worked problems for the formula pages of hydraulic06 (W06 Hydraulic Ancillary).
FXD1_NomographVelocity  page 16     14 gpm, ID 3/4 in -> v = 10.17 ft/s
FXD2_IntensifierWorked  page 24     1000 psi, A1:A2 = 10:2 -> 5000 psi ; 20 -> 4 gpm
FXD3_AccumWeightSpring  page 25     2000 kg on D100 -> 2.50 MPa ; spring 2.04 / 6.11 MPa
FXD4_AccumBoyleSizing   page 27-28  dV = 5 L -> V1 = 15.05 L (absolute pressures)

Every number on screen is copied from the note's verified steps
(W06 บทเรียน — Hydraulic Ancillary (hydraulic06 ทีละหน้า).md), rechecked with python.
Layout (same as fluid_exam_b.py): title + step tag + page_ref on top row, caption_top
under it, figure on the left stage, equations in the right panel (never on the figure).
"""
from mlib import *
import numpy as np

LIVE = "#42A5F5"   # low-pressure oil
HIGH = WARN        # high-pressure oil
YEL = "#FFD54F"
GAS = "#AED581"
DARK = "#37474F"
PX, PMW = 4.15, 5.2


def T(s, size=24, color=WHITE):
    return Text(s, font_size=size, color=color)


def M(*parts, size=34, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def harrow(x0, x1, y, color, sw=5):
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25)


def varrow(x, y0, y1, color, sw=4):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25)


def dim(p0, p1, color=GRAYTXT):
    return DoubleArrow([p0[0], p0[1], 0], [p1[0], p1[1], 0], buff=0, color=color,
                       stroke_width=3, tip_length=0.13)


def spring_mob(x, y0, y1, w=0.5, n=7, color=METAL):
    pts = [[x, y0, 0]]
    for i in range(1, 2 * n):
        yy = y0 + (y1 - y0) * i / (2 * n)
        pts.append([x + (w / 2 if i % 2 else -w / 2), yy, 0])
    pts.append([x, y1, 0])
    return VMobject(color=color, stroke_width=4).set_points_as_corners(
        [np.array(p, dtype=float) for p in pts])


class ExamScene(SafeScene):
    def head(self, ttl, ref):
        self.ttl = title(ttl, size=28)
        self.ref = page_ref(ref, size=18)
        self.cap_m = None
        self.step_m = None
        self.play(FadeIn(self.ttl), FadeIn(self.ref))

    def step(self, n, name):
        m = T(f"ขั้น {n} · {name}", 22, OK)
        m.move_to([-7.11 + 0.3 + m.width / 2, TITLE_Y, 0])
        if self.step_m is not None:
            self.play(FadeOut(self.step_m, run_time=0.3))
        self.play(FadeIn(m, shift=0.2 * RIGHT), run_time=0.5)
        self.step_m = m

    def cap(self, txt, color=GRAYTXT, wait=2.6):
        m = caption_top(txt, color=color, size=25, max_w=12.8)
        if self.cap_m is not None:
            self.play(FadeOut(self.cap_m, run_time=0.3))
        self.play(FadeIn(m), run_time=0.6)
        self.cap_m = m
        if wait:
            self.wait(wait)
        return m

    def glow(self, term, fig=None, color=YEL, rt=1.3):
        sf = 1.0 if (term.width > 3.2 or isinstance(term, Text)) else 1.2
        an = [Indicate(term, color=WHITE, scale_factor=sf),
              Circumscribe(term, color=color, buff=0.04, stroke_width=3,
                           fade_out=True)]
        if fig is not None:
            an.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*an, run_time=rt)

    def rows(self, rows, y0, gap=0.95, x=PX, max_w=PMW):
        for i, r in enumerate(rows):
            fit_width(r, max_w)
            r.move_to([x, y0 - i * gap, 0])
        return VGroup(*rows)

    def relabel(self, old, txt, size, color, left=False):
        new = T(txt, size, color).move_to(old.get_center())
        if left:
            new.align_to(old, LEFT)
        self.play(Transform(old, new))


# ======================================================================
class FXD1_NomographVelocity(ExamScene):
    """Page 16: 14 gpm in a 3/4 in ID pipe -> A = 0.4418 in^2 -> v = 10.17 ft/s."""

    def construct(self):
        self.head("ความเร็วในท่อ: nomograph กับสูตร", "W06 · หน้า 16")
        k, cR = 2.2, 1.0
        xL, xM, xR = -6.0, -4.0, -2.0

        def yQ(q):
            return -2.6 + k * np.log10(q)

        def yV(v):
            return cR - k * np.log10(v)

        cD = (-2.6 + cR) / 2 + (k / 2) * np.log10((np.pi / 4) / 0.3208)

        def yD(d):
            return cD + k * np.log10(d)

        axL = Line([xL, -2.75, 0], [xL, 1.95, 0], color=LIVE, stroke_width=4)
        axM = Line([xM, -1.85, 0], [xM, 0.85, 0], color=YEL, stroke_width=4)
        axR = Line([xR, -2.4, 0], [xR, 0.5, 0], color=WARN, stroke_width=4)

        def ticks(x, vals, f, side, shift=None):
            g = VGroup()
            shift = shift or {}
            for v, s in vals:
                y = f(v)
                g.add(Line([x - 0.1, y, 0], [x + 0.1, y, 0], color=METAL, stroke_width=3))
                lb = T(s, 18, GRAYTXT)
                dy = shift.get(s, 0.0)
                if side < 0:
                    lb.move_to([x - 0.2 - lb.width / 2, y + dy, 0])
                else:
                    lb.move_to([x + 0.2 + lb.width / 2, y + dy, 0])
                g.add(lb)
            return g

        tQ = ticks(xL, [(1, "1"), (2, "2"), (5, "5"), (10, "10"), (20, "20"),
                        (50, "50"), (100, "100")], yQ, -1)
        tD = ticks(xM, [(0.25, "1/4"), (0.75, "3/4"), (1, "1"), (1.5, "1.5"),
                        (2, "2"), (3, "3")], yD, -1, {"3/4": -0.2})
        tV = ticks(xR, [(2, "2"), (4, "4"), (10, "10"), (20, "20"), (30, "30")], yV, +1)
        hQ = T("Q (gpm)", 20, LIVE).move_to([xL, 2.22, 0])
        hD = T("D ภายใน (in)", 20, YEL).move_to([xM, 1.15, 0])
        hV = T("v (ft/s)", 20, WARN).move_to([xR, 0.8, 0])

        yq, yd = yQ(14), yD(0.75)
        yr = 2 * yd - yq
        dQ = Dot([xL, yq, 0], color=LIVE, radius=0.09)
        q14 = T("14", 20, LIVE).move_to([xL - 0.42, yq, 0])
        dD = Dot([xM, yd, 0], color=YEL, radius=0.09)
        dV = Dot([xR, yr, 0], color=WARN, radius=0.09)
        ruler = Line([xL, yq, 0], [xR, yr, 0], color=WHITE, stroke_width=3)
        read = T("อ่านได้ ≈ 10 ft/s", 20, WARN)
        read.move_to([xR + 0.65 + read.width / 2, yr, 0])

        # pipe cross-section: where D and A live
        pc = np.array([2.3, -2.7, 0])
        pipe_c = Circle(radius=0.5, color=METAL, stroke_width=4, fill_color=LIVE,
                        fill_opacity=0.35).move_to(pc)
        pipe_d = dim(pc + [-0.5, 0, 0], pc + [0.5, 0, 0], YEL)
        pipe_dl = T("D = 3/4 in", 20, YEL).move_to(pc + [0, -0.78, 0])
        pipe_al = M(r"A", r"=", r"\frac{\pi}{4}D^2", size=32, color=LIVE).move_to(
            pc + [2.2, 0, 0])
        pipe = VGroup(pipe_c, pipe_d)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(axL), Create(axM), Create(axR), run_time=1.0)
        self.play(FadeIn(tQ, tD, tV, hQ, hD, hV), run_time=1.0)
        self.cap("nomograph = 3 แกน: อัตราไหล Q · ขนาดท่อ D · ความเร็ว v")
        self.cap("โจทย์: น้ำมัน 14 gpm ไหลในท่อ ID 3/4 in ความเร็ว v เท่าไร?", color=WHITE)
        self.play(FadeIn(dQ, scale=1.5), FadeIn(q14))
        self.glow(q14, dQ, LIVE)
        self.play(FadeIn(dD, scale=1.5))
        self.glow(tD[3], dD, YEL)
        self.play(FadeIn(pipe), FadeIn(pipe_dl))
        self.cap("ท่อ ID 3/4 in = เส้นผ่านศูนย์กลางด้านใน (รูปตัดท่อมุมขวาล่าง)")
        self.play(Create(ruler), run_time=1.5)
        self.play(FadeIn(dV, scale=1.5), FadeIn(read))
        self.cap("วางไม้บรรทัดผ่าน 2 จุดที่รู้ → อ่านแกนที่ 3 ได้ ≈ 10 ft/s")
        self.cap("อ่านกราฟได้แค่คร่าวๆ → ตรวจด้วยสูตรที่หัวกราฟให้แม่น")

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"A", r"=", r"\frac{", r"Q", r"\times 0.3208", r"}{", r"v", r"}", size=40)
        e1[0].set_color(LIVE); e1[3].set_color(LIVE); e1[6].set_color(WARN)
        e2 = M(r"Q\,[\text{in}^3/\text{s}]", r"=", r"Q_{gpm}\times\frac{231}{60}", size=32)
        e3 = M(r"v\,[\text{in/s}]", r"=", r"12\,v_{ft/s}", size=32)
        e4 = M(r"\frac{231}{60\times 12}", r"=", r"\frac{231}{720}", r"=", r"0.3208",
               size=34)
        e4[4].set_color(YEL)
        g2 = self.rows([e1, e2, e3, e4], 1.85, 1.0)
        self.play(FadeIn(e1))
        self.cap("สูตรหัวกราฟ: พื้นที่ = อัตราไหล × 0.3208 ÷ ความเร็ว", wait=1.0)
        self.glow(e1[0], pipe_c, LIVE)
        self.glow(e1[3], dQ, LIVE)
        self.glow(e1[6], dV, WARN)
        self.cap("0.3208 มาจากไหน? Q = A·v แต่หน่วยไม่ตรงกัน ต้องแปลง")
        self.play(FadeIn(e2))
        self.cap("1 gal = 231 in³ และ 1 นาที = 60 s → gpm เป็น in³/s")
        self.play(FadeIn(e3))
        self.cap("1 ft = 12 in → ft/s เป็น in/s")
        self.play(FadeIn(e4))
        self.glow(e4[4])
        self.cap("รวมตัวแปลงหน่วย: 231 ÷ 720 = 0.3208 (แค่ตัวแปลงหน่วย ไม่ใช่ค่าฟิสิกส์ใหม่)")
        self.play(FadeOut(VGroup(e2, e3, e4)))
        e5 = M(r"v", r"=", r"\frac{0.3208\,Q}{A}", size=40)
        e5[0].set_color(WARN)
        self.rows([e5], 0.85)
        self.play(FadeIn(e5))
        self.play(FadeIn(pipe_al))
        self.cap("ย้ายข้างหา v และหา A ของท่อกลมจาก D", wait=2.0)
        self.glow(pipe_al[2], pipe_d, YEL)

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e5)))
        s1 = M(r"A", r"= \frac{\pi}{4}(0.75)^2", r"= 0.4418\ \text{in}^2", size=34)
        s1[0].set_color(LIVE)
        s2 = M(r"v", r"= \frac{0.3208\times 14}{0.4418}", size=36)
        s2[0].set_color(WARN)
        s3 = M(r"v = 10.17\ \text{ft/s}", size=46, color=WARN)
        self.rows([s1, s2, s3], 1.85, 1.15)
        box = SurroundingRectangle(s3, color=WARN, buff=0.15)
        self.play(FadeIn(s1))
        self.glow(s1[1], pipe_d, YEL)
        self.cap("D = 3/4 in = 0.75 in → A = 0.4418 in²")
        self.play(FadeIn(s2))
        self.glow(s2[1], VGroup(dQ, pipe_c), LIVE)
        self.cap("แทน Q = 14 gpm และ A = 0.4418 in² (ต้องเป็นหน่วย gpm · in²)")
        self.play(Write(s3), Create(box))
        self.relabel(read, "สูตร: 10.17 ft/s", 20, WARN)
        self.cap("คำตอบ: v = 10.17 ft/s", color=WARN)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(VGroup(s1, s2)))
        self.play(VGroup(s3, box).animate.move_to([PX, 1.85, 0]))
        mx4 = T("max ท่อดูด = 4", 18, LIVE)
        mx4.move_to([xR + 0.6 + mx4.width / 2, yV(4), 0])
        mx20 = T("max ท่อจ่าย = 20", 18, FORCE)
        mx20.move_to([xR + 0.6 + mx20.width / 2, yV(20), 0])
        c1 = T("nomograph ≈ 10 ตรงกับสูตร 10.17 ✓", 24, OK)
        c2 = T("10.17 < 20 → ใช้เป็นท่อจ่าย (pressure) ได้ ✓", 24, OK)
        c3 = T("10.17 > 4 → ใช้เป็นท่อดูด (intake) ไม่ได้", 24, WARN)
        self.rows([c1, c2, c3], 0.75, 0.7)
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.glow(c1, dV, OK)
        self.play(FadeIn(mx4, mx20))
        self.cap("แกนความเร็วมีขีดจำกัด: ท่อดูดไม่เกิน 4 ft/s · ท่อจ่ายไม่เกิน 20 ft/s")
        self.play(FadeIn(c2, shift=0.15 * UP))
        self.glow(mx20, tV[7], FORCE)
        self.play(FadeIn(c3, shift=0.15 * UP))
        self.glow(mx4, tV[3], LIVE)
        self.cap("ถ้าจะใช้เป็นท่อดูด ต้องเลือกท่อใหญ่ขึ้นจน v ≤ 4 ft/s", wait=2.0)
        self.cap("กับดัก: 0.3208 ใช้กับ gpm · in² · ft/s เท่านั้น — หน่วย SI ใช้ A = Q/v ตรงๆ",
                 color=YEL, wait=4.0)
        self.wait(1.5)


# ======================================================================
class FXD2_IntensifierWorked(ExamScene):
    """Page 24: P2 = 1000*10/2 = 5000 psi ; Q2 = 20*2/10 = 4 gpm ; P1Q1 = P2Q2 = 20,000."""

    def construct(self):
        self.head("Pressure intensifier: แทนค่าทีละขั้น", "W06 · หน้า 24")
        xl, xj, xe = -6.7, -3.5, -0.6
        R1 = 1.3
        R2 = R1 / np.sqrt(5)
        PW, d = 0.3, 3.0
        x0, x1 = -6.2, -4.8
        xb = ValueTracker(x0)
        A1C, A2C = YEL, GEAR_OUT

        big = Rectangle(width=xj - xl, height=2 * R1, color=METAL, stroke_width=4).move_to(
            [(xl + xj) / 2, 0, 0])
        small = Rectangle(width=xe - xj, height=2 * R2, color=METAL, stroke_width=4).move_to(
            [(xj + xe) / 2, 0, 0])
        low = always_redraw(lambda: Rectangle(
            width=max(xb.get_value() - PW / 2 - xl, 0.01), height=2 * R1 - 0.08,
            stroke_width=0, fill_color=LIVE, fill_opacity=0.45).move_to(
            [(xl + xb.get_value() - PW / 2) / 2, 0, 0]))
        exh = always_redraw(lambda: Rectangle(
            width=max(xj - xb.get_value() - PW / 2, 0.01), height=2 * R1 - 0.08,
            stroke_width=0, fill_color=DARK, fill_opacity=0.7).move_to(
            [(xj + xb.get_value() + PW / 2) / 2, 0, 0]))
        hig = always_redraw(lambda: Rectangle(
            width=max(xe - xb.get_value() - d - PW / 2, 0.01), height=2 * R2 - 0.06,
            stroke_width=0, fill_color=HIGH, fill_opacity=0.55).move_to(
            [(xe + xb.get_value() + d + PW / 2) / 2, 0, 0]))

        bigP = Rectangle(width=PW, height=2 * R1 - 0.08, stroke_width=0, fill_color=METAL,
                         fill_opacity=1).move_to([x0, 0, 0])
        rod = Rectangle(width=d - PW, height=0.24, stroke_width=0, fill_color="#CFD8DC",
                        fill_opacity=1).move_to([x0 + d / 2, 0, 0])
        smP = Rectangle(width=PW, height=2 * R2 - 0.06, stroke_width=0, fill_color=METAL,
                        fill_opacity=1).move_to([x0 + d, 0, 0])
        f_ar = harrow(x0 + 0.2, x0 + 0.95, 0.55, FORCE, 4)
        f_lb = M(r"F", size=30, color=FORCE).move_to([x0 + 0.575, 0.85, 0])
        mover = VGroup(bigP, rod, smP, f_ar, f_lb)

        inlet = varrow(-6.45, 2.2, 1.4, LIVE, 5)
        p1_lb = T("P1 = 1000 psi", 22, LIVE)
        p1_lb.move_to([-6.2 + p1_lb.width / 2, 2.0, 0])
        q1_lb = T("Q1 = 20 gpm", 22, LIVE)
        q1_lb.move_to([-6.2 + q1_lb.width / 2, 1.6, 0])
        outlet = harrow(xe, 0.8, 0, HIGH, 5)
        q2_lb = T("Q2 = ?", 22, HIGH)
        q2_lb.move_to([-0.45 + q2_lb.width / 2, 0.45, 0])
        p2_lb = T("P2 = ?", 22, HIGH).move_to([-2.0, 1.15, 0])
        p2_ar = varrow(-2.0, 0.95, 0.63, HIGH, 3)
        a1_lb = T("A1 = 10 in²", 22, A1C).move_to([-5.1, -1.7, 0])
        a2_lb = T("A2 = 2 in²", 22, A2C).move_to([-2.05, -1.7, 0])
        for m in (p1_lb, q1_lb, q2_lb, p2_lb, a1_lb, a2_lb, f_lb):
            m.set_z_index(3)
        xd1 = dim((x0, -2.3), (x1, -2.3), WHITE)
        xd2 = dim((x0 + d, -2.3), (x1 + d, -2.3), WHITE)
        xl1 = M(r"x", size=30).move_to([(x0 + x1) / 2, -2.6, 0])
        xl2 = M(r"x", size=30).move_to([(x0 + x1) / 2 + d, -2.6, 0])

        def stroke(a, b, rt=2.2):
            back = a - bigP.get_x()
            if abs(back) > 1e-3:
                self.play(xb.animate.set_value(a), mover.animate.shift(back * RIGHT),
                          run_time=0.9)
            self.play(xb.animate.set_value(b), mover.animate.shift((b - a) * RIGHT),
                      run_time=rt, rate_func=linear)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(big), Create(small), run_time=1.0)
        self.add(low, exh, hig)
        self.play(FadeIn(mover), run_time=0.8)
        self.cap("intensifier = ลูกสูบใหญ่กับลูกสูบเล็ก ต่อกันด้วยก้านเดียว")
        self.play(FadeIn(a1_lb), FadeIn(a2_lb))
        self.glow(a1_lb, bigP, A1C)
        self.glow(a2_lb, smP, A2C)
        self.cap("พื้นที่ลูกสูบใหญ่ A1 = 10 in² · ลูกสูบเล็ก A2 = 2 in²")
        self.play(GrowArrow(inlet), FadeIn(p1_lb), FadeIn(q1_lb))
        self.cap("น้ำมันความดันต่ำ P1 = 1000 psi ไหลเข้า Q1 = 20 gpm ด้านใหญ่ (สีฟ้า)")
        stroke(x0, x1)
        self.play(GrowArrow(outlet), FadeIn(p2_lb), GrowArrow(p2_ar), FadeIn(q2_lb))
        self.cap("ลูกสูบเล็กดันน้ำมันความดันสูงออก (สีส้ม) — หา P2 และ Q2", color=WHITE)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"F", r"=", r"P_1", r"A_1", r"=", r"P_2", r"A_2", size=40)
        e1[0].set_color(FORCE); e1[2].set_color(LIVE); e1[3].set_color(A1C)
        e1[5].set_color(HIGH); e1[6].set_color(A2C)
        e2 = M(r"P_2", r"=", r"P_1", r"\frac{A_1}{A_2}", size=40)
        e2[0].set_color(HIGH); e2[2].set_color(LIVE)
        e3 = M(r"\frac{Q_1}{A_1}", r"=", r"\frac{Q_2}{A_2}", size=40)
        e4 = M(r"Q_2", r"=", r"Q_1", r"\frac{A_2}{A_1}", size=40)
        e4[0].set_color(HIGH); e4[2].set_color(LIVE)
        self.rows([e1, e2, e3, e4], 1.85, 1.05)
        self.play(FadeIn(e1))
        self.cap("ก้านเดียวกัน → แรงที่ส่งผ่านก้านเท่ากันทั้งสองด้าน")
        self.glow(e1[0], f_ar, FORCE)
        self.glow(e1[2], p1_lb, LIVE)
        self.glow(e1[3], bigP, A1C)
        self.glow(e1[5], p2_lb, HIGH)
        self.glow(e1[6], smP, A2C)
        self.play(FadeIn(e2))
        self.cap("หาร A2 ทั้งสองข้าง: P2 = P1 × A1/A2 (พื้นที่เล็ก → ความดันสูง)")
        self.play(GrowFromCenter(xd1), GrowFromCenter(xd2), FadeIn(xl1, xl2))
        stroke(x0, x1, 1.8)
        self.cap("ก้านเดียวกัน → ลูกสูบทั้งสองเดินระยะ x เท่ากัน ในเวลาเท่ากัน")
        self.play(FadeIn(e3))
        self.glow(e3[0], bigP, LIVE)
        self.glow(e3[2], smP, HIGH)
        self.cap("ความเร็วลูกสูบ = Q/A เท่ากันทั้งสองด้าน")
        self.play(FadeIn(e4))
        self.cap("ได้ Q2 = Q1 × A2/A1 (การไหลลดลงตามอัตราส่วนพื้นที่)")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e2, e3, e4)))
        s1 = M(r"F", r"= 1000\times 10", r"= 10{,}000\ \text{lb}", size=36)
        s1[0].set_color(FORCE)
        s2 = M(r"P_2", r"= 1000\times\frac{10}{2}", r"= 5000\ \text{psi}", size=38)
        s2[0].set_color(HIGH); s2[2].set_color(HIGH)
        s3 = M(r"Q_2", r"= 20\times\frac{2}{10}", r"= 4\ \text{gpm}", size=38)
        s3[0].set_color(HIGH); s3[2].set_color(HIGH)
        self.rows([s1, s2, s3], 1.8, 1.25)
        self.play(FadeIn(s1))
        self.glow(s1[1], VGroup(p1_lb, a1_lb), FORCE)
        self.cap("แรงที่ก้าน F = P1·A1 = 10,000 lb (psi × in² = lb)")
        self.play(FadeIn(s2))
        self.glow(s2[1], VGroup(a1_lb, a2_lb), A1C)
        b2 = SurroundingRectangle(s2[2], color=HIGH, buff=0.12)
        self.play(Create(b2))
        self.relabel(p2_lb, "P2 = 5000 psi", 22, HIGH)
        self.cap("P2 = 5000 psi (สูงขึ้น 10/2 = 5 เท่า)", color=HIGH)
        self.play(FadeIn(s3))
        self.glow(s3[1], VGroup(q1_lb, a2_lb), LIVE)
        b3 = SurroundingRectangle(s3[2], color=HIGH, buff=0.12)
        self.play(Create(b3))
        self.relabel(q2_lb, "Q2 = 4 gpm", 22, HIGH, left=True)
        self.cap("Q2 = 4 gpm (ลดลง 5 เท่า)", color=HIGH)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(s1))
        c1 = M(r"P_1Q_1 = 1000\times 20 = 20{,}000", size=34, color=LIVE)
        c2 = M(r"P_2Q_2 = 5000\times 4 = 20{,}000", size=34, color=HIGH)
        c3 = T("กำลังเท่ากัน ✓ (ไม่คิดการสูญเสีย)", 24, OK)
        self.rows([c1, c2, c3], -1.6, 0.7)
        self.cap("ตรวจด้วยกำลัง: กำลังไฮดรอลิกขึ้นกับ P × Q")
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.glow(c1, VGroup(p1_lb, q1_lb), LIVE)
        self.play(FadeIn(c2, shift=0.15 * UP))
        self.glow(c2, VGroup(p2_lb, q2_lb), HIGH)
        self.play(FadeIn(c3, shift=0.15 * UP))
        self.cap("ความดัน ×5 แต่การไหล ÷5 → ไม่มีพลังงานฟรี")
        self.cap("ใช้งานจริง: ต้องการแรงสูงช่วงสั้นๆ (ตอกอัด, หนีบ) ด้วยปั๊มความดันต่ำ", wait=2.4)
        self.cap("กับดัก: อย่าคูณ Q ด้วย 5 ตามความดัน — Q2 = Q1 × A2/A1 (ลดลง)",
                 color=YEL, wait=4.0)
        self.wait(1.5)


# ======================================================================
class FXD3_AccumWeightSpring(ExamScene):
    """Page 25: (a) 2000 kg, D100 -> 2.50 MPa ; (b) k 200 N/mm, D50, x 20/60 -> 2.04/6.11 MPa."""

    def construct(self):
        self.head("Accumulator แบบน้ำหนัก vs แบบสปริง", "W06 · หน้า 25")
        # weighted
        cx, hw = -5.0, 0.8
        yb, ytop = -2.5, 0.4
        wp = ValueTracker(-1.0)
        wall_w = VGroup(Line([cx - hw, ytop, 0], [cx - hw, yb, 0]),
                        Line([cx - hw, yb, 0], [cx + hw, yb, 0]),
                        Line([cx + hw, yb, 0], [cx + hw, ytop, 0])).set_color(METAL).set_stroke(width=4)
        oil_w = always_redraw(lambda: Rectangle(
            width=2 * hw - 0.06, height=max(wp.get_value() - 0.12 - (yb + 0.03), 0.01),
            stroke_width=0, fill_color=LIVE, fill_opacity=0.45).move_to(
            [cx, (wp.get_value() - 0.12 + yb + 0.03) / 2, 0]))
        y0w = -1.0
        pist_w = Rectangle(width=2 * hw - 0.06, height=0.24, stroke_width=0,
                           fill_color=METAL, fill_opacity=1).move_to([cx, y0w, 0])
        rod_w = Rectangle(width=0.2, height=1.78, stroke_width=0, fill_color="#CFD8DC",
                          fill_opacity=1).move_to([cx, y0w + 0.12 + 0.89, 0])
        blk = Rectangle(width=2.2, height=0.9, color=GEAR_OUT, fill_color=GEAR_OUT,
                        fill_opacity=0.3, stroke_width=3).move_to([cx, y0w + 1.9 + 0.45, 0])
        blk_t = VGroup(T("m = 2000 kg", 20, GEAR_OUT), T("W = mg", 20, GEAR_OUT)).arrange(
            DOWN, buff=0.08).move_to(blk)
        a_w = M(r"A", size=30).move_to([cx - hw - 0.35, y0w, 0])
        mover_w = VGroup(pist_w, rod_w, blk, blk_t, a_w)
        pw_lb = T("P = ?", 20, WHITE).move_to([cx, -2.05, 0]).set_z_index(3)
        dw = dim((cx - hw, -2.75), (cx + hw, -2.75), YEL)
        dw_lb = T("D = 100 mm", 20, YEL).move_to([cx, -3.05, 0])
        name_w = T("(ก) แบบน้ำหนัก", 22, GEAR_OUT).move_to([cx, -3.48, 0])

        # spring
        cs, hs = -1.7, 0.4
        ycap = 1.3
        yfree, sc = -0.6, 0.02
        sp = ValueTracker(0.0)          # compression x in mm

        def yps():
            return yfree + sc * sp.get_value()
        wall_s = VGroup(Line([cs - hs, ycap, 0], [cs - hs, yb, 0]),
                        Line([cs - hs, yb, 0], [cs + hs, yb, 0]),
                        Line([cs + hs, yb, 0], [cs + hs, ycap, 0]),
                        Line([cs - hs, ycap, 0], [cs + hs, ycap, 0])).set_color(METAL).set_stroke(width=4)
        oil_s = always_redraw(lambda: Rectangle(
            width=2 * hs - 0.06, height=max(yps() - 0.12 - (yb + 0.03), 0.01),
            stroke_width=0, fill_color=LIVE, fill_opacity=0.45).move_to(
            [cs, (yps() - 0.12 + yb + 0.03) / 2, 0]))
        pist_s = always_redraw(lambda: Rectangle(
            width=2 * hs - 0.06, height=0.24, stroke_width=0, fill_color=METAL,
            fill_opacity=1).move_to([cs, yps(), 0]))
        spr = always_redraw(lambda: spring_mob(cs, yps() + 0.12, ycap, w=0.5, n=7,
                                               color=FORCE))
        free = DashedLine([cs - 0.55, yfree, 0], [cs + 0.8, yfree, 0], color=GRAYTXT,
                          stroke_width=2)
        a_s = M(r"A", size=30)
        a_s.add_updater(lambda m: m.move_to([cs - hs - 0.3, yps(), 0]))
        k_lb = T("k = 200 N/mm", 20, FORCE).move_to([-0.25, 1.0, 0])
        x_ar = always_redraw(lambda: DoubleArrow(
            [cs + 0.65, yfree, 0], [cs + 0.65, max(yps(), yfree + 0.05), 0], buff=0,
            color=WHITE, stroke_width=3, tip_length=0.1,
            max_tip_length_to_length_ratio=0.45))
        x_lb = always_redraw(lambda: M(r"x", size=30).move_to(
            [cs + 0.92, (yfree + max(yps(), yfree + 0.05)) / 2, 0]))
        ps_lb = T("P = ?", 20, WHITE)
        ps_lb.move_to([cs + 0.65 + ps_lb.width / 2, -1.95, 0])
        ps_ar = Arrow(ps_lb.get_left(), [cs + 0.15, -1.95, 0], buff=0.06, color=WHITE,
                      stroke_width=3, max_tip_length_to_length_ratio=0.3)
        ds = dim((cs - hs, -2.75), (cs + hs, -2.75), YEL)
        ds_lb = T("D = 50 mm", 20, YEL).move_to([cs, -3.05, 0])
        name_s = T("(ข) แบบสปริง", 22, FORCE).move_to([cs, -3.48, 0])
        for m in (pw_lb, ps_lb, k_lb, blk_t):
            m.set_z_index(3)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(wall_w), Create(wall_s), run_time=1.0)
        self.add(oil_w, oil_s)
        self.play(FadeIn(mover_w), FadeIn(pist_s), FadeIn(free), FadeIn(name_w, name_s))
        self.add(spr)
        self.cap("accumulator = ถังเก็บน้ำมันภายใต้ความดัน (แบตเตอรี่ของระบบไฮดรอลิก)")
        self.play(FadeIn(pw_lb), FadeIn(dw, dw_lb))
        self.cap("(ก) มวล 2000 kg กดลูกสูบ D = 100 mm → ความดันน้ำมัน P = ?", color=WHITE)
        self.glow(blk_t[0], blk, GEAR_OUT)
        self.play(FadeIn(a_s), FadeIn(k_lb), FadeIn(ds, ds_lb), FadeIn(ps_lb),
                  GrowArrow(ps_ar))
        self.add(x_ar, x_lb)
        self.play(sp.animate.set_value(20), run_time=1.5)
        self.cap("(ข) สปริง k = 200 N/mm ลูกสูบ D = 50 mm อัด x = 20 mm และ 60 mm → P = ?",
                 color=WHITE)
        self.glow(k_lb, None, FORCE)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"W", r"=", r"m", r"g", size=40)
        e1[0].set_color(GEAR_OUT); e1[2].set_color(GEAR_OUT)
        e2 = M(r"A", r"=", r"\frac{\pi}{4}", r"D^2", size=40)
        e2[3].set_color(YEL)
        e3 = M(r"P", r"=", r"\frac{W}{A}", size=40)
        e4 = M(r"P", r"=", r"\frac{F_{spring}}{A}", r"=", r"\frac{k\,x}{A}", size=40)
        e4[4].set_color(FORCE)
        self.rows([e1, e2, e3, e4], 1.85, 1.05)
        self.play(FadeIn(e1))
        self.glow(e1[0], blk, GEAR_OUT)
        self.cap("น้ำหนัก W = มวล × g (g = 9.81 m/s²) → หน่วยนิวตัน")
        self.play(FadeIn(e2))
        self.glow(e2[3], VGroup(dw, ds), YEL)
        self.cap("พื้นที่ลูกสูบกลม A = πD²/4")
        self.play(FadeIn(e3))
        self.glow(e3[2], VGroup(blk, pist_w), GEAR_OUT)
        self.cap("แบบน้ำหนัก: ความดัน = น้ำหนัก ÷ พื้นที่ลูกสูบ")
        self.play(FadeIn(e4))
        self.glow(e4[4], k_lb, FORCE)
        self.cap("แบบสปริง: แรงสปริง F = k·x (อัดมากแรงมาก) ÷ พื้นที่ลูกสูบ")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e2, e3, e4)))
        s1 = M(r"W = 2000(9.81) = 19{,}620\ \text{N}", size=34, color=GEAR_OUT)
        s2 = M(r"A = \frac{\pi}{4}(0.1)^2 = 7.854\times10^{-3}\ \text{m}^2", size=34)
        s3 = M(r"P = \frac{19{,}620}{7.854\times10^{-3}} = 2.50\times10^{6}\ \text{Pa}",
               size=34)
        s4 = M(r"P_{(a)} = 2.50\ \text{MPa}\ (25\ \text{bar})", size=40, color=GEAR_OUT)
        self.rows([s1, s2, s3, s4], 1.85, 1.05)
        self.cap("(ก) แบบน้ำหนัก", color=GEAR_OUT, wait=0.8)
        self.play(FadeIn(s1))
        self.glow(s1, blk_t, GEAR_OUT)
        self.play(FadeIn(s2))
        self.glow(s2, dw, YEL)
        self.cap("D = 100 mm = 0.1 m ต้องแปลงเป็นเมตรก่อน")
        self.play(FadeIn(s3))
        self.play(Write(s4))
        b4 = SurroundingRectangle(s4, color=GEAR_OUT, buff=0.12)
        self.play(Create(b4))
        self.relabel(pw_lb, "2.50 MPa", 20, WHITE)
        self.cap("ได้ P = 2.50 MPa = 25 bar", color=GEAR_OUT)

        self.play(FadeOut(VGroup(s1, s2, s3)))
        self.play(VGroup(s4, b4).animate.move_to([PX, 1.85, 0]))
        t1 = M(r"A = \frac{\pi}{4}(0.05)^2 = 1.963\times10^{-3}\ \text{m}^2", size=34)
        t2 = M(r"x=20:\ F = 200\times20 = 4000\ \text{N}", size=34, color=FORCE)
        t3 = M(r"P = \frac{4000}{1.963\times10^{-3}} = 2.04\ \text{MPa}", size=34)
        t4 = M(r"x=60:\ F = 12{,}000\ \text{N} \Rightarrow P = 6.11\ \text{MPa}", size=34)
        self.rows([t1, t2, t3, t4], 0.85, 1.0)
        self.cap("(ข) แบบสปริง", color=FORCE, wait=0.8)
        self.play(FadeIn(t1))
        self.glow(t1, ds, YEL)
        self.play(FadeIn(t2))
        self.glow(t2, k_lb, FORCE)
        self.cap("N/mm × mm = N → ไม่ต้องแปลง x เป็นเมตร")
        self.play(FadeIn(t3))
        b3 = SurroundingRectangle(t3, color=FORCE, buff=0.1)
        self.play(Create(b3))
        self.relabel(ps_lb, "2.04 MPa", 20, WHITE, left=True)
        self.play(sp.animate.set_value(60), run_time=2.0)
        self.cap("อัดต่อถึง x = 60 mm (น้ำมันเข้ามาเก็บมากขึ้น)")
        self.play(FadeIn(t4))
        b5 = SurroundingRectangle(t4, color=FORCE, buff=0.1)
        self.play(Create(b5))
        self.relabel(ps_lb, "6.11 MPa", 20, WHITE, left=True)
        self.cap("ได้ P = 2.04 MPa ที่ x = 20 mm และ 6.11 MPa ที่ x = 60 mm", color=FORCE)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(VGroup(t1, t2, b3, t3, b5, t4)))
        c1 = T("น้ำหนักคงที่ → P คงที่ 2.50 MPa ✓", 24, OK)
        c2 = T("อัด 3 เท่า (20→60 mm) → P 3 เท่า ✓", 24, OK)
        c3 = M(r"6.11 \div 2.04 \approx 3", size=34, color=OK)
        self.rows([c1, c2, c3], 0.6, 0.8)
        self.play(wp.animate.set_value(-1.35), mover_w.animate.shift(-0.35 * UP),
                  run_time=1.4)
        self.play(wp.animate.set_value(-0.85), mover_w.animate.shift(0.5 * UP),
                  run_time=1.4)
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.cap("น้ำมันเหลือมากหรือน้อย ความดันแบบน้ำหนักก็ไม่เปลี่ยน")
        self.play(sp.animate.set_value(20), run_time=1.4)
        self.relabel(ps_lb, "2.04 MPa", 20, WHITE, left=True)
        self.play(sp.animate.set_value(60), run_time=1.4)
        self.relabel(ps_lb, "6.11 MPa", 20, WHITE, left=True)
        self.play(FadeIn(c2, shift=0.15 * UP), FadeIn(c3, shift=0.15 * UP))
        self.cap("แบบสปริง: น้ำมันยิ่งมาก สปริงยิ่งถูกอัด ความดันยิ่งสูง ตรงกับสไลด์")
        self.cap("ออกสอบ: ความดันคงที่ = weighted · ไม่ต้อง pre-charge = spring", wait=2.6)
        self.cap("กับดัก: kg ต้องคูณ 9.81 เป็น N และ D (mm) ต้องแปลงเป็น m ก่อนคิด A",
                 color=YEL, wait=4.0)
        a_s.clear_updaters()
        self.wait(1.5)


# ======================================================================
class FXD4_AccumBoyleSizing(ExamScene):
    """Pages 27-28: dV = 5 L, 100/200/120 bar(g) -> abs -> V1 = 15.05, V2 = 12.56, V3 = 7.56 L."""

    def construct(self):
        self.head("ขนาด accumulator แก๊ส (กฎของ Boyle)", "W06 · หน้า 27–28")
        W, H = 1.4, 3.0
        yc = 0.15
        ytop, ybot = yc + H / 2 - 0.1, yc - H / 2 + 0.1     # inner top/bottom
        Hi = ytop - ybot
        g3 = 7.5633 / 15.0508
        g2 = 12.5633 / 15.0508
        xs = [-5.7, -3.3, -0.9]

        def parts(x, g, vtex, ly=None):
            gas = Rectangle(width=W - 0.16, height=max(g * Hi, 0.01), stroke_width=0,
                            fill_color=GAS, fill_opacity=0.4).move_to(
                [x, ytop - g * Hi / 2, 0])
            oil = Rectangle(width=W - 0.16, height=max((1 - g) * Hi, 0.01), stroke_width=0,
                            fill_color=LIVE, fill_opacity=0.5 if g < 0.999 else 0.0).move_to(
                [x, ybot + (1 - g) * Hi / 2, 0])
            dia = Line([x - (W - 0.16) / 2, ytop - g * Hi, 0],
                       [x + (W - 0.16) / 2, ytop - g * Hi, 0], color=METAL, stroke_width=5)
            v = M(vtex, size=34, color=WHITE).move_to(
                [x, ytop - g * Hi / 2 if ly is None else ly, 0])
            return VGroup(gas, oil, dia, v)

        def shell(x):
            return VGroup(
                RoundedRectangle(width=W, height=H, corner_radius=0.15, color=METAL,
                                 stroke_width=4).move_to([x, yc, 0]),
                Rectangle(width=0.3, height=0.18, stroke_width=0, fill_color=METAL,
                          fill_opacity=1).move_to([x, yc + H / 2 + 0.09, 0]),
                Rectangle(width=0.3, height=0.18, stroke_width=0, fill_color=METAL,
                          fill_opacity=1).move_to([x, yc - H / 2 - 0.09, 0]))

        def labels(x, name, p, v, col):
            a = T(name, 20, GRAYTXT).move_to([x, -1.85, 0])
            b = T(p, 20, col).move_to([x, -2.3, 0])
            c = T(v, 20, WHITE).move_to([x, -2.75, 0])
            return a, b, c

        sh = [shell(x) for x in xs]
        pb = parts(xs[0], 1.0, r"V_1")
        pd0 = parts(xs[1], 1.0, r"V_3")
        pd = parts(xs[1], g3, r"V_3")
        lyf = (ytop + (ytop - g3 * Hi)) / 2
        pf0 = parts(xs[2], g3, r"V_2", lyf)
        pf = parts(xs[2], g2, r"V_2", lyf)
        P1C, P2C, P3C = GAS, OK, WARN
        lb_b = labels(xs[0], "(b) pre-charge", "p1 = 100 bar(g)", "V1 = ?", P1C)
        lb_d = labels(xs[1], "(d) ชาร์จเต็ม", "p3 = 200 bar(g)", "V3", P3C)
        lb_f = labels(xs[2], "(f) ปล่อยถึงต่ำสุด", "p2 = 120 bar(g)", "V2", P2C)
        yV3 = ytop - g3 * Hi
        yV2 = ytop - g2 * Hi
        ghost = DashedLine([xs[2] - (W - 0.16) / 2, yV3, 0], [xs[2] + (W - 0.16) / 2, yV3, 0],
                           color=WARN, stroke_width=3)
        brace = BraceBetweenPoints([xs[2] + W / 2 + 0.05, yV3, 0],
                                   [xs[2] + W / 2 + 0.05, yV2, 0], direction=RIGHT,
                                   color=YEL)
        dv_lb = VGroup(M(r"\Delta V", size=32, color=YEL),
                       M(r"=5\ \text{L}", size=32, color=YEL)).arrange(DOWN, buff=0.1)
        dv_lb.next_to(brace, RIGHT, buff=0.12)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(*[Create(s) for s in sh], run_time=1.2)
        self.cap("accumulator แก๊ส: ไนโตรเจน (บน สีเขียว) กับน้ำมัน (ล่าง สีฟ้า) คั่นด้วยแผ่นยาง")
        self.play(FadeIn(pb), FadeIn(*lb_b))
        self.cap("(b) เติมแก๊สถึง pre-charge p1 = 100 bar(g) → แก๊สเต็มถัง: V1 = ขนาดถัง")
        self.play(FadeIn(pd0), FadeIn(*lb_d))
        self.play(Transform(pd0, pd), run_time=1.8)
        self.cap("(d) ปั๊มอัดน้ำมันเข้าจนถึงสูงสุด p3 = 200 bar(g) → แก๊สเหลือ V3")
        self.play(FadeIn(pf0), FadeIn(*lb_f))
        self.play(Transform(pf0, pf), FadeIn(ghost), run_time=1.8)
        self.cap("(f) ปล่อยน้ำมันไปใช้จนเหลือต่ำสุด p2 = 120 bar(g) → แก๊สขยายเป็น V2")
        self.play(GrowFromCenter(brace), FadeIn(dv_lb))
        self.cap("น้ำมันที่ได้ใช้ต่อรอบ = V2 − V3 ต้องได้ 5 L → ถังต้องใหญ่ V1 เท่าไร?",
                 color=WHITE)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"p_1", r"V_1", r"=", r"p_2", r"V_2", r"=", r"p_3", r"V_3", size=40)
        e1[0].set_color(P1C); e1[3].set_color(P2C); e1[6].set_color(P3C)
        e2 = M(r"\Delta V", r"=", r"V_2 - V_3", size=38)
        e2[0].set_color(YEL)
        e3 = M(r"\Delta V", r"=", r"p_1 V_1\left(\frac{1}{p_2}-\frac{1}{p_3}\right)", size=38)
        e3[0].set_color(YEL)
        e4 = M(r"V_1", r"=", r"\frac{\Delta V}{p_1\left(\frac{1}{p_2}-\frac{1}{p_3}\right)}",
               size=38)
        self.rows([e1, e2, e3, e4], 1.85, 1.22)
        self.play(FadeIn(e1))
        self.cap("กฎของ Boyle (อุณหภูมิคงที่): p × V ของแก๊สก้อนเดิมคงที่")
        self.glow(e1[0], lb_b[1], P1C)
        self.glow(e1[1], pb[3], P1C)
        self.glow(e1[6], lb_d[1], P3C)
        self.glow(e1[7], pd0[3], P3C)
        self.glow(e1[3], lb_f[1], P2C)
        self.glow(e1[4], pf0[3], P2C)
        self.play(FadeIn(e2))
        self.glow(e2[2], brace, YEL)
        self.cap("น้ำมันที่ปล่อยออก = ปริมาตรที่แก๊สขยายจาก V3 ไป V2")
        self.play(FadeIn(e3))
        self.cap("แทน V2 = p1V1/p2 และ V3 = p1V1/p3 ลงไป")
        self.play(FadeIn(e4))
        self.cap("ย้ายข้างได้สูตรหาขนาดถัง V1")
        self.play(FadeOut(VGroup(e1, e2, e3)))
        self.play(e4.animate.move_to([PX, 1.85, 0]))

        # why absolute
        nl = Line([2.2, 0.55, 0], [6.4, 0.55, 0], color=GRAYTXT, stroke_width=3)
        tk0 = Line([2.4, 0.42, 0], [2.4, 0.68, 0], color=WHITE, stroke_width=3)
        tk1 = Line([4.6, 0.42, 0], [4.6, 0.68, 0], color=WHITE, stroke_width=3)
        n0a = T("สุญญากาศ", 18, GRAYTXT).move_to([2.4, 0.95, 0])
        n0b = T("0 bar(abs)", 18, WHITE).move_to([2.4, 0.15, 0])
        n1a = T("บรรยากาศ", 18, GRAYTXT).move_to([4.6, 0.95, 0])
        n1b = T("1.013 bar(abs) = 0 bar(g)", 18, WHITE).move_to([4.75, 0.15, 0])
        absr = M(r"p_{abs} = p_{g} + 1.013\ \text{bar}", size=38, color=YEL).move_to(
            [PX, -0.65, 0])
        w1 = T("แก๊สที่ 0 bar(g) ยังมีแรงดันจริง 1.013 bar", 22, WHITE)
        w2 = T("Boyle นับจากสุญญากาศ → ต้องใช้ความดันสัมบูรณ์", 22, WHITE)
        self.rows([w1, w2], -1.55, 0.6)
        self.cap("ทำไมต้องใช้ความดันสัมบูรณ์ (absolute)?", color=WHITE, wait=1.2)
        self.play(Create(nl), Create(tk0), Create(tk1), FadeIn(n0a, n0b, n1a, n1b))
        self.cap("เกจวัดเทียบกับอากาศรอบตัว: อ่าน 0 ทั้งที่แก๊สยังมีแรงดัน 1.013 bar")
        self.play(FadeIn(w1))
        self.play(FadeIn(absr))
        self.glow(absr, tk1, YEL)
        self.play(FadeIn(w2))
        self.cap("p × V คงที่ใช้ได้กับความดันที่นับจากศูนย์จริง (สุญญากาศ) เท่านั้น")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(nl, tk0, tk1, n0a, n0b, n1a, n1b, absr, w1, w2)))
        s1 = M(r"p_1 = 100 + 1.013 = 101.013\ \text{bar}", size=34, color=P1C)
        s2 = M(r"p_2 = 121.013,\quad p_3 = 201.013\ \text{bar}", size=34)
        s3 = M(r"V_1 = \frac{5}{101.013\left(\frac{1}{121.013}-\frac{1}{201.013}\right)}",
               size=34)
        s4 = M(r"V_1 = \frac{5}{0.3322} = 15.05\ \text{L}", size=40, color=P1C)
        self.rows([s1, s2, s3, s4], 0.85, 1.1)
        self.play(FadeIn(s1))
        self.relabel(lb_b[1], "p1 = 101.013 abs", 18, P1C)
        self.cap("บวก 1.013 ทุกตัว: gauge → absolute")
        self.play(FadeIn(s2))
        self.relabel(lb_d[1], "p3 = 201.013 abs", 18, P3C)
        self.relabel(lb_f[1], "p2 = 121.013 abs", 18, P2C)
        self.play(FadeIn(s3))
        self.glow(s3, dv_lb, YEL)
        self.cap("ΔV = 5 L อยู่ข้างบน · ใส่ p2 (ต่ำสุด) และ p3 (สูงสุด) ให้ถูกช่อง")
        self.play(Write(s4))
        b4 = SurroundingRectangle(s4, color=P1C, buff=0.12)
        self.play(Create(b4))
        self.relabel(lb_b[2], "V1 = 15.05 L", 20, P1C)
        self.cap("ขนาดถัง V1 = 15.05 L", color=P1C)
        self.play(FadeOut(VGroup(e4, s1, s2, s3)))
        self.play(VGroup(s4, b4).animate.move_to([PX, 1.85, 0]))
        v2 = M(r"V_2 = \frac{p_1V_1}{p_2} = \frac{101.013(15.05)}{121.013} = 12.56\ \text{L}",
               size=32, color=P2C)
        v3 = M(r"V_3 = \frac{p_1V_1}{p_3} = \frac{101.013(15.05)}{201.013} = 7.56\ \text{L}",
               size=32, color=P3C)
        self.rows([v2, v3], 0.7, 1.1)
        self.play(FadeIn(v2))
        self.relabel(lb_f[2], "V2 = 12.56 L", 20, P2C)
        self.play(FadeIn(v3))
        self.relabel(lb_d[2], "V3 = 7.56 L", 20, P3C)
        self.cap("หาปริมาตรแก๊สที่ p2 และ p3 ไว้ตรวจคำตอบ")

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = M(r"V_2 - V_3 = 12.56 - 7.56 = 5.00\ \text{L}", size=34, color=OK)
        c2 = T("ใช้ gauge (ผิด): V1 = 15.00 L", 24, WHITE)
        c3 = T("1/2/4 bar(g): gauge 20.0 L · abs 18.76 L", 24, WHITE)
        self.rows([c1, c2, c3], -1.4, 0.7)
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.glow(c1, brace, OK)
        self.cap("V2 − V3 = 5.00 L ตรงกับที่โจทย์ต้องการ ✓", color=OK)
        self.play(FadeIn(c2, shift=0.15 * UP))
        self.cap("ที่ความดันสูง gauge กับ absolute ต่างกันน้อย (15.00 vs 15.05)")
        self.play(FadeIn(c3, shift=0.15 * UP))
        self.cap("ความดันต่ำ เช่น p1/p2/p3 = 1/2/4 bar(g): ต่างกัน ~7% → ต้องใช้ absolute เสมอ")
        self.cap("กับดัก: p1 = pre-charge (ต่ำสุด) · p2 = ใช้งานต่ำสุด · p3 = สูงสุด อย่าสลับ p2 กับ p3",
                 color=YEL, wait=4.0)
        self.wait(1.5)
