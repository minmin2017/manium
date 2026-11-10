"""Fluid Power Control exam clips, batch F (2026-11-10, exam 11 Nov).

W08 Pneumatic 01 (Properties of Air & Gas Laws), lesson note
"W08 บทเรียน — Pneumatic 01 (Properties of Air & Gas Laws).md".
FX17_AbsPressureTemp  pages 2-3   100 psig -> 114.7 psia ; 80 F -> 540 R ; standard air 68 F 14.7 psia
FX18_GasLaws3         page 4      Boyle / Charles / Gay-Lussac ; closed tank 114.7 psia 540 R -> 528 R
                                  -> 112.15 psia = 97.45 psig (gauge+F gives wrong 85 psig)
FX19_ScfmCylinder     pages 5-6   1.75 in x 6 in, 30 cpm -> 0.251 cfm -> 1.91 scfm
FX20_MoistureMass     pages 7-10  100 m3, 100 kPa, 35/30 C -> Pv 3.94, w 0.0255, ma 108.7, mv 2.77 kg

Every number is copied from the note's worked steps and rechecked with python
(ma = 96.06*100/(0.287*308) = 108.67 kg; the note rounds it to 108.6).
Layout follows fluid_exam_d.py: title + step tag + page_ref top row, caption_top under it,
figure on the left stage, equations in the right panel.
"""
from mlib import *
import numpy as np

LIVE = "#42A5F5"
HIGH = WARN
YEL = "#FFD54F"
GAS = "#AED581"
AIRC = "#90A4AE"
FLAME = "#FF7043"
PX, PMW = 4.15, 5.2


def T(s, size=24, color=WHITE):
    return Text(s, font_size=size, color=color)


def M(*parts, size=34, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def dim(p0, p1, color=GRAYTXT):
    return DoubleArrow([p0[0], p0[1], 0], [p1[0], p1[1], 0], buff=0, color=color,
                       stroke_width=3, tip_length=0.13)


def tick(x, y, w=0.14, color=WHITE):
    return Line([x - w, y, 0], [x + w, y, 0], color=color, stroke_width=3)


def lab_left(s, x, y, size=18, color=GRAYTXT):
    m = T(s, size, color)
    m.move_to([x - 0.36 - m.width / 2, y, 0])
    return m


def lab_right(s, x, y, size=18, color=GRAYTXT):
    m = T(s, size, color)
    m.move_to([x + 0.36 + m.width / 2, y, 0])
    return m


def liquid(x, ybot, ytop, color=WARN, w=0.12):
    return Rectangle(width=w, height=max(ytop - ybot, 0.01), stroke_width=0,
                     fill_color=color, fill_opacity=0.95).move_to([x, (ybot + ytop) / 2, 0])


def thermo(x, y0, y1, color=WARN):
    tube = RoundedRectangle(width=0.28, height=y1 - y0, corner_radius=0.13, color=METAL,
                            stroke_width=3).move_to([x, (y0 + y1) / 2, 0])
    bulb = Circle(radius=0.21, color=METAL, stroke_width=3, fill_color=color,
                  fill_opacity=0.95).move_to([x, y0 - 0.12, 0])
    return VGroup(tube, bulb)


class ExamScene(SafeScene):
    def head(self, ttl, ref):
        self.ttl = title(ttl, size=28)
        fit_width(self.ttl, 7.2)
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
              Circumscribe(term, color=color, buff=0.04, stroke_width=3, fade_out=True)]
        if fig is not None:
            an.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*an, run_time=rt)

    def place(self, mobs, ys, x=PX, max_w=PMW):
        for m, y in zip(mobs, ys):
            fit_width(m, max_w)
            m.move_to([x, y, 0])
        return VGroup(*mobs)

    def relabel(self, old, txt, size, color, side=None, anchor_x=None):
        new = T(txt, size, color)
        if side == "right":
            new.move_to([anchor_x + 0.25 + new.width / 2, old.get_y(), 0])
        elif side == "left":
            new.move_to([anchor_x - 0.25 - new.width / 2, old.get_y(), 0])
        else:
            new.move_to(old.get_center()).align_to(old, LEFT)
        self.play(Transform(old, new))


# ======================================================================
class FX17_AbsPressureTemp(ExamScene):
    """Pages 2-3: absolute pressure / absolute temperature / standard air."""

    def construct(self):
        self.head("ลมต้องใช้ค่าสัมบูรณ์: psia และ °R", "W08 · หน้า 2-3")
        xb, xt = -5.3, -1.3

        def yp(p):
            return -2.5 + p * 4.3 / 114.7

        def yf(f):
            return -1.3 + (f - 32) * 0.0583

        # pressure column
        col = Rectangle(width=0.42, height=yp(114.7) + 0.05 - yp(0), color=METAL,
                        stroke_width=3).move_to([xb, (yp(0) + yp(114.7) + 0.05) / 2, 0])

        def fill(p, color):
            h = yp(p) - yp(0)
            return Rectangle(width=0.36, height=h, stroke_width=0, fill_color=color,
                             fill_opacity=0.6).move_to([xb, yp(0) + h / 2, 0])

        f_atm = fill(14.7, AIRC)
        f_hi = fill(114.7, WARN)
        tk = VGroup(*[tick(xb, yp(p)) for p in (0, 14.7, 114.7)])
        hp = T("ความดัน", 22, WHITE).move_to([xb, 2.25, 0])
        la0 = lab_left("0 psia", xb, yp(0))
        la1 = lab_left("14.7 psia", xb, yp(14.7))
        la2 = lab_left("114.7 psia", xb, yp(114.7), color=WARN)
        lg0 = lab_right("−14.7 psig", xb, yp(0))
        lg1 = lab_right("0 psig (บรรยากาศ)", xb, yp(14.7), color=AIRC)
        lg2 = lab_right("100 psig", xb, yp(114.7), color=WARN)
        vac = T("สุญญากาศ = ศูนย์จริง", 18, GRAYTXT).move_to([xb, -2.92, 0])

        # thermometer with a broken scale
        th = thermo(xt, -2.6, yf(80) + 0.25)
        brk = VGroup(Line([xt - 0.25, -2.05, 0], [xt + 0.25, -1.95, 0], color=WHITE,
                          stroke_width=3),
                     Line([xt - 0.25, -1.9, 0], [xt + 0.25, -1.8, 0], color=WHITE,
                          stroke_width=3))
        merc = liquid(xt, -2.8, yf(80))
        ht = T("อุณหภูมิ", 22, WHITE).move_to([xt, 2.25, 0])
        ttk = VGroup(*[tick(xt, y) for y in (-2.5, yf(32), yf(68), yf(80))])
        lf0 = lab_left("−460 °F", xt, -2.5)
        lf1 = lab_left("32 °F", xt, yf(32))
        lf2 = lab_left("68 °F", xt, yf(68), color=LIVE)
        lf3 = lab_left("80 °F", xt, yf(80), color=WARN)
        lr0 = lab_right("0 °R", xt, -2.5, color=YEL)
        lr1 = lab_right("492 °R", xt, yf(32), color=YEL)
        lr2 = lab_right("528 °R", xt, yf(68), color=LIVE)
        lr3 = lab_right("540 °R", xt, yf(80), color=WARN)
        az = T("ศูนย์สัมบูรณ์", 18, GRAYTXT).move_to([xt, -3.3, 0])

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(col), FadeIn(hp), FadeIn(tk))
        self.play(FadeIn(f_atm), FadeIn(la0, la1, vac))
        self.cap("ความดันจริงนับจากสุญญากาศ (ไม่มีโมเลกุลเลย) = 0 psia")
        self.cap("อากาศรอบตัวเราก็มีแรงดันอยู่แล้ว 14.7 psia")
        self.play(FadeIn(lg1))
        self.glow(lg1, f_atm, AIRC)
        self.cap("แต่เกจวัดเทียบกับอากาศรอบตัว → ตรงนี้เกจอ่าน 0 psig")
        self.play(FadeIn(lg0))
        self.play(FadeIn(f_hi), FadeIn(la2, lg2))
        self.cap("โจทย์ (ชุดหน้า 6): ลมในกระบอกสูบ 100 psig ที่ 80 °F", color=WHITE)
        self.play(Create(th), FadeIn(merc), FadeIn(ht, ttk, brk))
        self.play(FadeIn(lf0, lf1, lf2, lf3, az))
        self.cap("ถาม: ความดันสัมบูรณ์ + อุณหภูมิสัมบูรณ์ เท่าไร? (กฎก๊าซใช้ได้แค่ค่าสัมบูรณ์)",
                 color=WHITE, wait=3.2)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"P_{abs}", r"=", r"P_{gage}", r"+", r"P_{atm}", size=40)
        e1[0].set_color(WARN); e1[4].set_color(AIRC)
        e2 = M(r"\text{psia} = \text{psig} + 14.7", size=34)
        e3 = M(r"\text{kPa abs} = \text{kPa gage} + 101.3", size=34)
        e4 = M(r"1\ \text{atm} = 14.7\ \text{psi} = 1.013\ \text{bar}", size=32, color=AIRC)
        e5 = M(r"= 101.3\ \text{kPa} = 1.033\ \text{kg/cm}^2", size=32, color=AIRC)
        self.place([e1, e2, e3, e4, e5], [1.9, 0.95, 0.1, -0.85, -1.55])
        self.play(FadeIn(e1))
        self.cap("ความดันสัมบูรณ์ = ค่าที่เกจอ่าน + ความดันบรรยากาศ", wait=1.2)
        self.glow(e1[0], VGroup(f_hi, la2), WARN)
        self.glow(e1[2], lg2, WARN)
        self.glow(e1[4], f_atm, AIRC)
        self.play(FadeIn(e2))
        self.cap("หน่วยอังกฤษ: บวก 14.7 psi")
        self.play(FadeIn(e3))
        self.cap("หน่วย SI: บวก 101.3 kPa")
        self.play(FadeIn(e4), FadeIn(e5))
        self.cap("ความดันบรรยากาศที่ระดับน้ำทะเลเขียนได้หลายหน่วย จำไว้ทั้งชุด")
        self.play(FadeOut(VGroup(e1, e2, e3, e4, e5)))
        t1 = M(r"T\,(^\circ\text{R})", r"=", r"T\,(^\circ\text{F})", r"+ 460", size=38)
        t1[0].set_color(YEL)
        t2 = M(r"T\,(\text{K})", r"=", r"T\,(^\circ\text{C})", r"+ 273", size=38)
        t2[0].set_color(YEL)
        self.place([t1, t2], [1.9, 0.95])
        self.play(FadeIn(t1))
        self.play(FadeIn(lr0, lr1))
        self.cap("อุณหภูมิก็เหมือนกัน: นับจากศูนย์สัมบูรณ์ −460 °F = 0 °R (แรงคิน)")
        self.glow(t1[0], VGroup(lr0, lr1), YEL)
        self.glow(t1[3], lf0, YEL)
        self.play(FadeIn(t2))
        self.cap("หน่วย SI: เคลวิน K = °C + 273")
        sa = [T("อากาศมาตรฐาน (Standard Air)", 24, LIVE),
              T("68 °F (20 °C)", 22, WHITE),
              T("14.7 psia (101.3 kPa abs)", 22, WHITE),
              T("ความชื้นสัมพัทธ์ RH 36%", 22, WHITE),
              T("ปริมาตรที่สภาวะนี้ → หน่วย scfm", 22, YEL)]
        self.place(sa, [-0.05, -0.6, -1.1, -1.6, -2.15])
        sbox = SurroundingRectangle(VGroup(*sa), color=LIVE, buff=0.12)
        self.play(FadeIn(sa[0]), Create(sbox))
        self.play(FadeIn(sa[1], sa[2], sa[3]))
        self.cap("อากาศขยาย/หดตามความดันและอุณหภูมิ → ต้องมีสภาวะกลางไว้เทียบ")
        self.play(FadeIn(sa[4]))
        self.glow(sa[1], lf2, LIVE)
        self.cap("scfm = standard cubic feet per minute (ฟุต³/นาที ที่อากาศมาตรฐาน)")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(t1, t2, sbox, *sa)))
        h2 = T("สภาวะใช้งานจริง (2)", 22, WARN)
        s1 = M(r"P_2 = 100 + 14.7 = 114.7\ \text{psia}", size=34, color=WARN)
        s2 = M(r"T_2 = 80 + 460 = 540\ ^\circ\text{R}", size=34, color=WARN)
        h1 = T("อากาศมาตรฐาน (1)", 22, LIVE)
        s3 = M(r"P_1 = 14.7\ \text{psia}", size=34, color=LIVE)
        s4 = M(r"T_1 = 68 + 460 = 528\ ^\circ\text{R}", size=34, color=LIVE)
        self.place([h2, s1, s2, h1, s3, s4], [1.95, 1.3, 0.55, -0.35, -1.0, -1.75])
        self.play(FadeIn(h2), FadeIn(s1))
        self.glow(s1, VGroup(f_hi, lg2), WARN)
        self.cap("100 psig + 14.7 = 114.7 psia")
        self.play(FadeIn(s2), FadeIn(lr3))
        self.glow(s2, merc, WARN)
        self.cap("80 °F + 460 = 540 °R")
        self.play(FadeIn(h1), FadeIn(s3), FadeIn(s4), FadeIn(lr2))
        self.glow(s4, lr2, LIVE)
        self.cap("อากาศมาตรฐาน: 14.7 psia และ 68 + 460 = 528 °R", color=WHITE)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(VGroup(h2, s1, s2, h1, s3, s4)))
        c1 = M(r"\frac{P_2}{P_1} = \frac{114.7}{14.7} = 7.80", size=36, color=OK)
        c1t = T("ลมอัดแน่นกว่าอากาศปกติ 7.8 เท่า ✓", 22, OK)
        c2 = T("ใช้ gauge: 100 ÷ 0 → หารไม่ได้ ✗", 22, WARN)
        c3 = M(r"\frac{T_2}{T_1} = \frac{540}{528} = 1.023", size=36, color=OK)
        c4 = T("ใช้ °F: 80 ÷ 68 = 1.18 ผิดไป 15% ✗", 22, WARN)
        c5 = T("SI: 20 °C + 273 = 293 K", 22, LIVE)
        self.place([c1, c1t, c2, c3, c4, c5], [1.9, 1.05, 0.5, -0.4, -1.25, -1.85])
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.play(FadeIn(c1t))
        self.cap("อัตราส่วนความดันสัมบูรณ์ = ลมถูกอัดกี่เท่า")
        self.play(FadeIn(c2))
        self.glow(c2, lg1, WARN)
        self.cap("ถ้าใช้ psig อากาศรอบตัว = 0 → อัตราส่วนไร้ความหมาย", color=WARN)
        self.play(FadeIn(c3, shift=0.15 * UP))
        self.play(FadeIn(c4))
        self.cap("อุณหภูมิก็ห้ามใช้ °F/°C ตรงๆ ในกฎของก๊าซ", color=WARN)
        self.play(FadeIn(c5))
        self.cap("สรุป: psia = psig + 14.7 · °R = °F + 460 · K = °C + 273", color=YEL, wait=4.0)


# ======================================================================
CY_TOP, CY_BOT = 0.5, -1.9


def walls(x):
    return VMobject(color=METAL, stroke_width=5).set_points_as_corners(
        [np.array(p, dtype=float) for p in
         [[x - 0.65, CY_TOP, 0], [x - 0.65, CY_BOT, 0], [x + 0.65, CY_BOT, 0],
          [x + 0.65, CY_TOP, 0]]])


def moving(x, h, gas_col=GAS, rod=0.6, weight=False, push=False):
    yb = CY_BOT + 0.04
    top = yb + h + 0.18
    gas = Rectangle(width=1.2, height=h, stroke_width=0, fill_color=gas_col,
                    fill_opacity=0.45).move_to([x, yb + h / 2, 0])
    pis = Rectangle(width=1.22, height=0.18, stroke_width=0, fill_color=METAL,
                    fill_opacity=1).move_to([x, yb + h + 0.09, 0])
    rd = Line([x, top, 0], [x, top + rod, 0], color=METAL, stroke_width=6)
    g = VGroup(gas, pis, rd)
    if weight:
        g.add(Rectangle(width=0.7, height=0.4, stroke_width=0, fill_color="#78909C",
                        fill_opacity=1).move_to([x, top + rod + 0.2, 0]))
    if push:
        g.add(Arrow([x, top + rod + 0.75, 0], [x, top + rod + 0.05, 0], buff=0,
                    color=FORCE, stroke_width=6, max_tip_length_to_length_ratio=0.3))
    return g


def flame(x):
    return Polygon([x - 0.2, -2.3, 0], [x + 0.2, -2.3, 0], [x, -1.98, 0], stroke_width=0,
                   fill_color=FLAME, fill_opacity=1)


def p_arrows(x, yc, L, color=WHITE):
    return VGroup(*[Arrow([x, yc, 0], [x + dx * L, yc + dy * L, 0], buff=0, color=color,
                          stroke_width=4, max_tip_length_to_length_ratio=0.35)
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))])


class FX18_GasLaws3(ExamScene):
    """Page 4: Boyle / Charles / Gay-Lussac, then a closed-tank Gay-Lussac example."""

    def construct(self):
        self.head("กฎของก๊าซ 3 ข้อ (มวลคงที่ ระบบปิด)", "W08 · หน้า 4")
        xB, xC, xG = -5.6, -3.3, -1.0
        wB, wC, wG = walls(xB), walls(xC), walls(xG)
        mB0 = moving(xB, 2.0, push=True)
        mB1 = moving(xB, 1.0, push=True)
        mC0 = moving(xC, 1.0, rod=1.2, weight=True)
        mC1 = moving(xC, 1.4, rod=1.2, weight=True)
        mG0 = moving(xG, 1.6, rod=0.5)
        mG1 = moving(xG, 1.6, gas_col="#FF8A65", rod=0.5)
        pin_y = CY_BOT + 0.04 + 1.6 + 0.3
        pins = VGroup(*[Rectangle(width=0.3, height=0.12, stroke_width=0, fill_color=WARN,
                                  fill_opacity=1).move_to([xG + s * 0.55, pin_y, 0])
                        for s in (-1, 1)])
        ycG = CY_BOT + 0.04 + 0.8
        pa0 = p_arrows(xG, ycG, 0.25)
        pa1 = p_arrows(xG, ycG, 0.52, WARN)
        fC, fG = flame(xC), flame(xG)
        nB = T("Boyle", 22, WHITE).move_to([xB, -2.7, 0])
        nC = T("Charles", 22, WHITE).move_to([xC, -2.7, 0])
        nG = T("Gay-Lussac", 22, WHITE).move_to([xG, -2.7, 0])
        kB = T("T คงที่", 20, YEL).move_to([xB, -3.12, 0])
        kC = T("P คงที่", 20, YEL).move_to([xC, -3.12, 0])
        kG = T("V คงที่", 20, YEL).move_to([xG, -3.12, 0])
        eB = T("P×2 → V÷2", 22, FORCE).move_to([xB, 2.05, 0])
        eC = T("T↑ → V↑", 22, FLAME).move_to([xC, 2.05, 0])
        eG = T("T↑ → P↑", 22, FLAME).move_to([xG, 2.05, 0])

        # ---------------- concept part
        self.cap("ก๊าซก้อนเดิม (มวลคงที่) ในกระบอกปิด มีตัวแปร 3 ตัว: P · V · T")
        self.play(Create(wB), FadeIn(mB0), FadeIn(nB, kB))
        self.cap("Boyle: อุณหภูมิคงที่ กดลูกสูบให้ปริมาตรเล็กลง")
        self.play(Transform(mB0, mB1), run_time=2.0)
        self.play(FadeIn(eB))
        self.cap("ปริมาตรเหลือครึ่ง → ความดันเพิ่ม 2 เท่า (ผกผันกัน)")
        lB = VGroup(T("Boyle", 22, WHITE), M(r"P_1V_1 = P_2V_2", size=36))
        lB.arrange(RIGHT, buff=0.35)
        lC = VGroup(T("Charles", 22, WHITE), M(r"\frac{V_1}{T_1} = \frac{V_2}{T_2}", size=36))
        lC.arrange(RIGHT, buff=0.35)
        lG = VGroup(T("Gay-Lussac", 22, WHITE),
                    M(r"\frac{P_1}{T_1} = \frac{P_2}{T_2}", size=36))
        lG.arrange(RIGHT, buff=0.35)
        self.place([lB, lC, lG], [1.9, 0.75, -0.55])
        self.play(FadeIn(lB))
        self.glow(lB[1], mB0[0], GAS)

        self.play(Create(wC), FadeIn(mC0), FadeIn(nC, kC))
        self.cap("Charles: ตุ้มน้ำหนักกดลูกสูบไว้ → ความดันคงที่")
        self.play(FadeIn(fC))
        self.play(Transform(mC0, mC1), run_time=2.0)
        self.play(FadeIn(eC))
        self.cap("ให้ความร้อน → อากาศขยายตัว ดันลูกสูบขึ้น (V ตาม T)")
        self.play(FadeIn(lC))
        self.glow(lC[1], VGroup(mC0[0], fC), GAS)

        self.play(Create(wG), FadeIn(mG0), FadeIn(pins), FadeIn(nG, kG))
        self.play(FadeIn(pa0))
        self.cap("Gay-Lussac: ล็อกลูกสูบด้วยสลัก (สีแดง) → ปริมาตรคงที่")
        self.play(FadeIn(fG))
        self.play(Transform(mG0, mG1), Transform(pa0, pa1), run_time=2.0)
        self.play(FadeIn(eG))
        self.cap("ให้ความร้อน → ขยายไม่ได้ → ความดันข้างในเพิ่ม (P ตาม T)")
        self.play(FadeIn(lG))
        self.glow(lG[1], pa0, WARN)
        self.cap("ทั้ง 3 ข้อ: P และ T ต้องเป็นค่าสัมบูรณ์ (psia, °R หรือ kPa abs, K)",
                 color=YEL, wait=3.0)

        # ---------------- worked example
        self.play(FadeOut(VGroup(wB, mB0, nB, kB, eB, wC, mC0, fC, nC, kC, eC, eG,
                                 lB, lC, lG, fG)))
        tank = VGroup(wG, mG0, pins, pa0, nG, kG)
        self.play(tank.animate.scale(1.15, about_point=np.array([xG, -1.0, 0]))
                  .shift(np.array([-3.0, 0.15, 0])), run_time=1.2)
        xT = xG - 3.0
        qx = -2.5
        q1 = T("P1 = 100 psig", 22, WARN)
        q2 = T("T1 = 80 °F", 22, WARN)
        q3 = T("เย็นลงเหลือ T2 = 68 °F", 22, LIVE)
        q4 = T("P2 = ?", 22, YEL)
        for m, y in zip([q1, q2, q3, q4], [0.9, 0.35, -0.2, -0.75]):
            m.move_to([qx + m.width / 2, y, 0])
        self.step(1, "เข้าใจโจทย์")
        self.cap("ตัวอย่างฝึก (ตัวเลขชุดหน้า 6): ถังลมปิดสนิท 100 psig ที่ 80 °F", color=WHITE)
        self.play(FadeIn(q1, q2))
        self.cap("ตั้งทิ้งไว้จนเย็นลงเหลือ 68 °F → ความดันในถังเหลือเท่าไร?", color=WHITE)
        self.play(FadeIn(q3, q4))
        pa_c = p_arrows(xT, -1.0 + (ycG + 1.0) * 1.15 + 0.15, 0.3)
        self.play(Transform(pa0, pa_c), mG0[0].animate.set_fill(LIVE, opacity=0.45))
        self.cap("ถังปิด = ปริมาตรคงที่ → ใช้ Gay-Lussac")
        self.glow(kG, pins, YEL)

        self.step(2, "สูตร")
        g1 = M(r"\frac{P_1}{T_1}", r"=", r"\frac{P_2}{T_2}", size=40)
        g2 = M(r"P_2", r"=", r"P_1", r"\times", r"\frac{T_2}{T_1}", size=40)
        g2[0].set_color(YEL)
        gw = T("P, T ต้องเป็นค่าสัมบูรณ์ (psia, °R)", 22, YEL)
        self.place([g1, g2, gw], [1.85, 0.65, -0.35])
        self.play(FadeIn(g1))
        self.glow(g1[0], VGroup(q1, q2), WARN)
        self.glow(g1[2], VGroup(q3, q4), LIVE)
        self.play(FadeIn(g2))
        self.cap("ย้ายข้างหา P2: คูณด้วยอัตราส่วนอุณหภูมิ T2/T1")
        self.play(FadeIn(gw))
        self.cap("ก่อนแทน: แปลงทุกตัวเป็นค่าสัมบูรณ์ก่อน", color=YEL)

        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(g1, gw)))
        self.play(g2.animate.move_to([PX, 1.95, 0]))
        s1 = M(r"P_1 = 100 + 14.7 = 114.7\ \text{psia}", size=32, color=WARN)
        s2 = M(r"T_1 = 80 + 460 = 540\ ^\circ\text{R}", size=32, color=WARN)
        s3 = M(r"T_2 = 68 + 460 = 528\ ^\circ\text{R}", size=32, color=LIVE)
        s4 = M(r"P_2 = 114.7 \times \frac{528}{540} = 112.15\ \text{psia}", size=32)
        s5 = M(r"P_2 = 112.15 - 14.7 = 97.45\ \text{psig}", size=36, color=YEL)
        self.place([s1, s2, s3, s4, s5], [1.05, 0.35, -0.35, -1.3, -2.3])
        self.play(FadeIn(s1))
        self.relabel(q1, "P1 = 114.7 psia", 22, WARN)
        self.play(FadeIn(s2))
        self.relabel(q2, "T1 = 540 °R", 22, WARN)
        self.play(FadeIn(s3))
        self.relabel(q3, "เย็นลงเหลือ T2 = 528 °R", 22, LIVE)
        self.cap("บวก 14.7 ให้ความดัน · บวก 460 ให้อุณหภูมิ")
        self.play(FadeIn(s4))
        self.glow(s4, pa0, WHITE)
        self.cap("114.7 × 528 ÷ 540 = 112.15 psia (ค่าสัมบูรณ์)")
        self.play(Write(s5))
        b5 = SurroundingRectangle(s5, color=YEL, buff=0.12)
        self.play(Create(b5))
        self.relabel(q4, "P2 = 97.45 psig", 22, YEL)
        self.cap("ลบ 14.7 กลับเป็นค่าที่เกจอ่าน: 97.45 psig", color=YEL)

        self.step(4, "ตรวจ")
        self.play(FadeOut(VGroup(g2, s1, s2, s3, s4)))
        self.play(VGroup(s5, b5).animate.move_to([PX, 1.9, 0]))
        c1 = T("เย็นลง → ความดันลด: 97.45 < 100 ✓", 22, OK)
        c2 = M(r"100 \times \frac{68}{80} = 85\ \text{psig}", size=34, color=WARN)
        c3 = T("ใช้ gauge + °F ตรงๆ → ผิดไป 12 psi ✗", 22, WARN)
        c4 = T("Boyle / Charles ก็ต้องใช้ค่าสัมบูรณ์เหมือนกัน", 22, YEL)
        self.place([c1, c2, c3, c4], [0.95, -0.05, -0.9, -1.6])
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.glow(c1, q3, OK)
        self.cap("ทิศทางถูก: อากาศเย็นลงในถังปิด ความดันต้องลดลง ✓", color=OK)
        self.play(FadeIn(c2))
        self.play(FadeIn(c3))
        self.cap("กับดัก: แทน 100 psig กับ 80/68 °F ตรงๆ ได้ 85 psig — ผิด!", color=WARN)
        self.play(FadeIn(c4))
        self.cap("สรุป: Boyle (T คงที่) · Charles (P คงที่) · Gay-Lussac (V คงที่)",
                 color=YEL, wait=4.0)


# ======================================================================
def hspring(x0, x1, y=0.6, amp=0.38, n=8, color=METAL):
    pts = [[x0, y, 0]]
    for i in range(1, 2 * n):
        pts.append([x0 + (x1 - x0) * i / (2 * n), y + (amp if i % 2 else -amp), 0])
    pts.append([x1, y, 0])
    return VMobject(color=color, stroke_width=3).set_points_as_corners(
        [np.array(p, dtype=float) for p in pts])


class FX19_ScfmCylinder(ExamScene):
    """Pages 5-6: general gas law, cylinder air consumption 0.251 cfm -> 1.91 scfm."""

    def construct(self):
        self.head("กระบอกสูบกินลมกี่ scfm?", "W08 · หน้า 5-6")
        bx0, bx1, by = -6.0, -1.9, 0.6
        xr, xe = -5.4, -3.2
        barrel = Rectangle(width=bx1 - bx0, height=1.2, color=METAL, stroke_width=4)
        barrel.move_to([(bx0 + bx1) / 2, by, 0])
        inlet = Line([-6.8, by, 0], [bx0, by, 0], color=WARN, stroke_width=8)
        in_lb = T("ลมเข้า 100 psig · 80 °F", 20, WARN).move_to([-5.3, -0.35, 0])
        xp = ValueTracker(xr)

        def air():
            x = xp.get_value()
            return Rectangle(width=x - 0.11 - (bx0 + 0.03), height=1.14, stroke_width=0,
                             fill_color=WARN, fill_opacity=0.45).move_to(
                [(x - 0.11 + bx0 + 0.03) / 2, by, 0])

        def piston():
            x = xp.get_value()
            return VGroup(
                Rectangle(width=0.22, height=1.14, stroke_width=0, fill_color=METAL,
                          fill_opacity=1).move_to([x, by, 0]),
                Line([x + 0.11, by, 0], [x + 4.0, by, 0], color=METAL, stroke_width=8),
                hspring(x + 0.11, bx1 - 0.03))

        a_m = always_redraw(air)
        p_m = always_redraw(piston)
        Ld = dim([xr, 1.5], [xe, 1.5], YEL)
        Ll = T("L = 6 in", 20, YEL).move_to([(xr + xe) / 2, 1.85, 0])
        Nl = T("N = 30 รอบ/นาที", 20, FORCE).move_to([-0.4, 1.65, 0])
        cc = np.array([-5.0, -1.75, 0])
        circ = Circle(radius=0.5, color=METAL, stroke_width=4, fill_color=LIVE,
                      fill_opacity=0.35).move_to(cc)
        Dd = dim(cc + [-0.5, 0, 0], cc + [0.5, 0, 0], LIVE)
        Dl = T("D = 1.75 in", 20, LIVE).move_to(cc + [1.45, 0, 0])
        Al = M(r"A = \tfrac{\pi}{4}D^2", size=28, color=LIVE).move_to(cc + [0, -0.85, 0])

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(barrel), Create(inlet), FadeIn(in_lb))
        self.add(a_m, p_m)
        self.cap("กระบอกสูบ single-acting: ลมดันออก · สปริงดันกลับ")
        for _ in range(2):
            self.play(xp.animate.set_value(xe), run_time=1.0)
            self.play(xp.animate.set_value(xr), run_time=0.8)
        self.play(GrowFromCenter(Ld), FadeIn(Ll))
        self.play(FadeIn(circ), GrowFromCenter(Dd), FadeIn(Dl))
        self.play(FadeIn(Nl))
        self.cap("โจทย์: ลูกสูบ 1.75 in · ระยะชัก 6 in · 100 psig · 80 °F · 30 รอบ/นาที",
                 color=WHITE, wait=3.2)
        self.cap("ถาม: กินลมกี่ scfm (= ลูกบาศก์ฟุต/นาที ของอากาศที่สภาวะมาตรฐาน)",
                 color=WHITE, wait=3.0)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"\frac{P_1Q_1}{T_1}", r"=", r"\frac{P_2Q_2}{T_2}", size=40)
        e1[0].set_color(LIVE); e1[2].set_color(WARN)
        e2 = M(r"Q_1", r"=", r"Q_2", r"\left(\frac{P_2}{P_1}\right)",
               r"\left(\frac{T_1}{T_2}\right)", size=38)
        e2[0].set_color(LIVE); e2[2].set_color(WARN)
        e3 = M(r"Q_2", r"=", r"A", r"\times", r"L", r"\times", r"N", size=40)
        e3[0].set_color(WARN); e3[2].set_color(LIVE); e3[4].set_color(YEL)
        e3[6].set_color(FORCE)
        self.place([e1, e2, e3], [1.85, 0.6, -0.55])
        self.play(FadeIn(e1))
        self.cap("กฎก๊าซทั่วไป (หน้า 5): PV/T คงที่ · หารด้วยเวลา → ใช้กับอัตราไหล Q ได้")
        self.cap("สภาวะ 2 = ลมอัดในกระบอกสูบ · สภาวะ 1 = อากาศมาตรฐาน (scfm)")
        self.glow(e1[2], barrel, WARN)
        self.play(FadeIn(e2))
        self.cap("ย้ายข้างหา Q1 = scfm ที่ต้องการ")
        self.play(FadeIn(e3))
        self.cap("Q2 = ปริมาตรลมอัดที่ใช้ต่อนาที = พื้นที่ × ระยะชัก × รอบ")
        self.play(FadeIn(Al))
        self.glow(e3[2], VGroup(circ, Al), LIVE)
        self.glow(e3[4], Ld, YEL)
        self.glow(e3[6], Nl, FORCE)

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e3)))
        self.play(e2.animate.move_to([PX, 1.9, 0]))
        s1 = M(r"A = \frac{\pi}{4}\left(\frac{1.75}{12}\right)^2 = 0.01670\ \text{ft}^2",
               size=32, color=LIVE)
        s2 = M(r"Q_2 = 0.01670 \times \frac{6}{12} \times 30 = 0.251\ \text{cfm}", size=32,
               color=WARN)
        s3 = M(r"P_2 = 114.7\ \text{psia},\ T_2 = 540\ ^\circ\text{R}", size=32, color=WARN)
        s4 = M(r"P_1 = 14.7\ \text{psia},\ T_1 = 528\ ^\circ\text{R}", size=32, color=LIVE)
        self.place([s1, s2, s3, s4], [0.7, -0.45, -1.4, -2.05])
        self.play(FadeIn(s1))
        self.glow(s1, Dd, LIVE)
        self.cap("÷12 แปลงนิ้วเป็นฟุต (เพราะคำตอบเป็น ft³/min)", color=YEL)
        self.play(FadeIn(s2))
        self.glow(s2, VGroup(Ld, Nl), WARN)
        self.cap("ลมอัดที่ 100 psig ใช้ 0.251 ft³ ต่อนาที")
        sq2 = Square(side_length=0.5, stroke_width=0, fill_color=WARN, fill_opacity=0.7)
        sq2.move_to([-1.9, -1.6, 0])
        sq2l = T("0.251 cfm (ลมอัด)", 18, WARN).move_to([-1.9, -2.2, 0])
        self.play(FadeIn(sq2), FadeIn(sq2l))
        self.play(FadeIn(s3), FadeIn(s4))
        self.cap("ค่าสัมบูรณ์จากหน้า 2-3: 114.7 psia · 540 °R · 14.7 psia · 528 °R")
        self.play(FadeOut(VGroup(s1, s2, s3, s4)))
        s5 = M(r"Q_1 = 0.251\left(\frac{114.7}{14.7}\right)\left(\frac{528}{540}\right)",
               size=34)
        s6 = M(r"Q_1 = 0.251 \times 7.803 \times 0.9778", size=34)
        s7 = M(r"Q_1 = 1.91\ \text{scfm}", size=46, color=LIVE)
        self.place([s5, s6, s7], [0.75, -0.4, -1.45])
        self.play(FadeIn(s5))
        self.cap("แทนลงสูตร: ความดันสูงกว่า → พองตัวมาก · อุณหภูมิมาตรฐานต่ำกว่า → หดนิดหน่อย")
        self.play(FadeIn(s6))
        self.play(Write(s7))
        b7 = SurroundingRectangle(s7, color=LIVE, buff=0.14)
        self.play(Create(b7))
        side = 0.5 * np.sqrt(1.91 / 0.251)
        sq1 = Square(side_length=side, stroke_width=0, fill_color=LIVE, fill_opacity=0.55)
        sq1.move_to([0.15, -1.6 + (side - 0.5) / 2, 0])
        sq1l = T("1.91 scfm (อากาศมาตรฐาน)", 18, LIVE).move_to([0.15, -2.6, 0])
        self.play(TransformFromCopy(sq2, sq1), FadeIn(sq1l), run_time=1.5)
        self.cap("คำตอบ: กินลม 1.91 scfm", color=LIVE)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(VGroup(e2, s5, s6)))
        self.play(VGroup(s7, b7).animate.move_to([PX, 1.9, 0]))
        c1 = M(r"\frac{1.91}{0.251} = 7.6 \approx 7.80 \times 0.978", size=34, color=OK)
        c2 = T("= อัตราส่วนความดัน × อัตราส่วนอุณหภูมิ ✓", 22, OK)
        c3 = T("single-acting: ใช้ลมแค่จังหวะดันออก", 22, WHITE)
        c4 = T("→ 1 ปริมาตร (A×L) ต่อ 1 รอบ", 22, WHITE)
        c5 = T("กับดัก: ลืม ÷12 หรือใช้ 100 psig ตรงๆ ✗", 22, WARN)
        self.place([c1, c2, c3, c4, c5], [0.8, 0.05, -0.65, -1.15, -1.85])
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.play(FadeIn(c2))
        self.glow(c1, VGroup(sq1, sq2), OK)
        self.cap("ลมอิสระมากกว่าลมอัด ~7.6 เท่า สมเหตุสมผล ✓", color=OK)
        self.play(FadeIn(c3), FadeIn(c4))
        self.play(xp.animate.set_value(xe), run_time=1.0)
        self.play(xp.animate.set_value(xr), run_time=0.8)
        self.cap("ขากลับใช้สปริง ไม่กินลม (ถ้า double-acting ต้องคิดขากลับด้วย)")
        self.play(FadeIn(c5))
        self.cap("สรุป: Q2 = A·L·N แล้วแปลงด้วย (P2/P1)(T1/T2) แบบค่าสัมบูรณ์", color=YEL,
                 wait=4.0)


# ======================================================================
class FX20_MoistureMass(ExamScene):
    """Pages 7-10: dry/wet bulb, phi, omega, dew point, mass of dry air and water."""

    def construct(self):
        self.head("ความชื้นในอากาศ: ω · จุดน้ำค้าง · มวลน้ำ", "W08 · หน้า 7-10")
        xd, xw = -6.1, -5.1
        y0, y1 = -0.6, 1.9

        def yT(t):
            return y0 + (t - 20) * 0.12

        thd = thermo(xd, y0, y1)
        thw = thermo(xw, y0, y1, color=LIVE)
        wick = RoundedRectangle(width=0.56, height=0.62, corner_radius=0.12, stroke_width=0,
                                fill_color=LIVE, fill_opacity=0.45).move_to(
            [xw, y0 - 0.12, 0])
        md = liquid(xd, y0 - 0.12, yT(35))
        mw0 = liquid(xw, y0 - 0.12, yT(35), color=LIVE)
        mw1 = liquid(xw, y0 - 0.12, yT(30), color=LIVE)
        nd = T("แห้ง", 20, WHITE).move_to([xd, 2.2, 0])
        nw = T("เปียก", 20, LIVE).move_to([xw, 2.2, 0])
        ld = T("Tdb = 35 °C", 18, WARN).move_to([xd, -1.35, 0])
        lw = T("Twb = 30 °C", 18, LIVE).move_to([xw, -1.78, 0])
        wind = Arrow([xw + 0.95, y0 - 0.12, 0], [xw + 0.4, y0 - 0.12, 0], buff=0,
                     color=GRAYTXT, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        ydp = yT(28.6)
        dpl = DashedLine([xd - 0.3, ydp, 0], [xw + 0.3, ydp, 0], color=YEL, stroke_width=3)
        dpt = T("Tdp ≈ 28.6 °C", 18, YEL)
        dpt.move_to([xw + 0.35 + dpt.width / 2, ydp, 0])

        bx0, bx1, by0, by1 = -3.3, 1.1, -2.6, 1.85
        box = Rectangle(width=bx1 - bx0, height=by1 - by0, color=METAL, stroke_width=4)
        box.move_to([(bx0 + bx1) / 2, (by0 + by1) / 2, 0])
        bl = T("V = 100 m³ · P = 100 kPa", 20, WHITE).move_to([(bx0 + bx1) / 2, 2.2, 0])
        rng = np.random.default_rng(7)
        pts = []
        while len(pts) < 46:
            p = np.array([rng.uniform(bx0 + 0.25, bx1 - 0.25),
                          rng.uniform(by0 + 0.25, by1 - 0.25), 0])
            if all(np.linalg.norm(p - q) > 0.42 for q in pts):
                pts.append(p)
        air_d = VGroup(*[Dot(p, radius=0.07, color=AIRC) for p in pts[:38]])
        vap_d = VGroup(*[Dot(p, radius=0.09, color=LIVE) for p in pts[38:]])
        lg1 = T("● อากาศแห้ง → Pa, ma", 18, AIRC).move_to([(bx0 + bx1) / 2, -2.95, 0])
        lg2 = T("● ไอน้ำ → Pv, mv", 18, LIVE).move_to([(bx0 + bx1) / 2, -3.35, 0])

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(thd), Create(thw), FadeIn(md), FadeIn(mw0), FadeIn(nd, nw))
        self.cap("กระเปาะแห้ง (dry-bulb) = เทอร์โมมิเตอร์ธรรมดา วัดได้ 35 °C")
        self.play(FadeIn(ld))
        self.play(FadeIn(wick), GrowArrow(wind))
        self.cap("กระเปาะเปียก: หุ้มผ้าเปียกแล้วเป่าลม → น้ำระเหยดึงความร้อนออก")
        self.play(Transform(mw0, mw1), run_time=2.0)
        self.play(FadeIn(lw))
        self.cap("อุณหภูมิลดเหลือ 30 °C · ยิ่งอากาศแห้ง น้ำยิ่งระเหยเร็ว ยิ่งลดมาก")
        self.cap("ถ้าอากาศอิ่มตัว 100% น้ำระเหยไม่ได้ → Twb = Tdb")
        self.play(Create(box), FadeIn(bl))
        self.play(FadeIn(air_d), FadeIn(vap_d), FadeIn(lg1, lg2))
        self.cap("ห้อง 100 m³ ความดันรวม 100 kPa: มีอากาศแห้ง (เทา) + ไอน้ำ (ฟ้า) ปนกัน",
                 color=WHITE, wait=3.0)
        self.cap("ถาม: φ · ω · จุดน้ำค้าง Tdp · มวลอากาศแห้ง ma · มวลน้ำ mv", color=WHITE,
                 wait=3.0)

        # ---------------- step 2
        self.step(2, "สูตร")
        f1 = M(r"P", r"=", r"P_a", r"+", r"P_v", size=40)
        f1[2].set_color(AIRC); f1[4].set_color(LIVE)
        f2 = M(r"\phi", r"=", r"\frac{P_v}{P_g}", size=40)
        f3 = M(r"\omega", r"=", r"0.622", r"\frac{P_v}{P_a}", size=40)
        f4 = M(r"m_a", r"=", r"\frac{P_a V}{R_a T}", size=40)
        f4[0].set_color(AIRC)
        f5 = M(r"m_v", r"=", r"\omega\, m_a", size=40)
        f5[0].set_color(LIVE)
        self.place([f1, f2, f3, f4, f5], [1.95, 0.85, -0.25, -1.35, -2.45])
        self.play(FadeIn(f1))
        self.cap("ความดันรวม = ความดันย่อยของอากาศแห้ง + ของไอน้ำ")
        self.glow(f1[2], air_d, AIRC)
        self.glow(f1[4], vap_d, LIVE)
        self.play(FadeIn(f2))
        self.cap("φ (ความชื้นสัมพัทธ์) = ไอน้ำจริง ÷ ไอน้ำอิ่มตัวที่อุณหภูมิเดียวกัน")
        self.glow(f2[2], VGroup(vap_d, md), LIVE)
        self.play(FadeIn(f3))
        self.cap("ω (humidity ratio) = มวลน้ำต่อมวลอากาศแห้ง 1 kg · 0.622 = 18.015/28.97")
        self.play(FadeIn(f4))
        self.cap("กฎก๊าซอุดมคติ PV = mRT (หน้า 5) · อากาศ R = 0.287 kJ/kg·K · T เป็น K")
        self.glow(f4[2], VGroup(box, md), AIRC)
        self.play(FadeIn(f5))
        self.cap("มวลน้ำ = ω × มวลอากาศแห้ง")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(f1, f2, f3, f4, f5)))
        a1 = VGroup(M(r"\phi \approx 0.70", size=34), T("(ชาร์ต 35/30 °C)", 20, GRAYTXT))
        a1.arrange(RIGHT, buff=0.3)
        a2 = VGroup(M(r"P_g = 5.628\ \text{kPa}", size=34), T("(ตารางไอน้ำ 35 °C)", 20, GRAYTXT))
        a2.arrange(RIGHT, buff=0.3)
        a3 = M(r"P_v = 0.70 \times 5.628 = 3.94\ \text{kPa}", size=34, color=LIVE)
        a4 = VGroup(M(r"T_{dp} \approx 28.6\ ^\circ\text{C}", size=34, color=YEL),
                    T("(ตาราง ที่ 3.94 kPa)", 20, GRAYTXT))
        a4.arrange(RIGHT, buff=0.3)
        self.place([a1, a2, a3, a4], [1.95, 1.0, 0.05, -0.9])
        self.play(FadeIn(a1))
        self.glow(a1[0], VGroup(ld, lw), WHITE)
        self.cap("อ่านชาร์ตไซโครเมตริกที่ Tdb 35 °C, Twb 30 °C → φ ≈ 70%")
        self.play(FadeIn(a2))
        self.glow(a2[0], md, WARN)
        self.cap("เปิดตารางไอน้ำอิ่มตัวที่ 35 °C → Pg = 5.628 kPa")
        self.play(FadeIn(a3))
        self.glow(a3, vap_d, LIVE)
        self.play(FadeIn(a4))
        self.play(Create(dpl), FadeIn(dpt))
        self.cap("จุดน้ำค้าง = อุณหภูมิที่ไอน้ำ 3.94 kPa เริ่มกลั่นเป็นหยดน้ำ ≈ 28.6 °C")
        self.play(FadeOut(VGroup(a1, a2, a4)))
        self.play(a3.animate.move_to([PX, 2.0, 0]))
        b1 = M(r"P_a = 100 - 3.94 = 96.06\ \text{kPa}", size=34, color=AIRC)
        b2 = M(r"\omega = 0.622 \times \frac{3.94}{96.06} = 0.0255", size=34)
        b3 = M(r"m_a = \frac{96.06 \times 100}{0.287 \times 308} = 108.7\ \text{kg}", size=34,
               color=AIRC)
        b4 = M(r"m_v = 0.0255 \times 108.7 = 2.77\ \text{kg}", size=38, color=LIVE)
        self.place([b1, b2, b3, b4], [1.05, -0.05, -1.25, -2.4])
        self.play(FadeIn(b1))
        self.glow(b1, air_d, AIRC)
        self.play(FadeIn(b2))
        self.cap("ω = 0.0255 kg น้ำ ต่ออากาศแห้ง 1 kg")
        self.play(FadeIn(b3))
        self.glow(b3, box, AIRC)
        self.cap("T = 35 + 273 = 308 K · ma = 108.7 kg (โน้ตปัดเป็น 108.6)", color=YEL)
        self.play(Write(b4))
        bb = SurroundingRectangle(b4, color=LIVE, buff=0.12)
        self.play(Create(bb))
        self.glow(b4, vap_d, LIVE)
        self.cap("ในห้องนี้มีน้ำปนในอากาศ 2.77 kg", color=LIVE)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(VGroup(a3, b1, b2, b3)))
        self.play(VGroup(b4, bb).animate.move_to([PX, 1.95, 0]))
        c1 = T("Tdb 35 > Twb 30 > Tdp 28.6 ✓", 22, OK)
        c2 = M(r"\frac{m_v}{m_a} = \frac{2.77}{108.7} = 0.0255 = \omega\ \checkmark", size=32,
               color=OK)
        c3 = T("Pv 3.94 < Pg 5.628 → φ < 1 ✓", 22, OK)
        c4 = T("กับดัก: T ในสูตรมวลต้องเป็น K (308)", 22, WARN)
        c5 = T("หน้า 13: อัดลม → อุ้มน้ำได้น้อยลง → น้ำกลั่นในท่อ", 22, YEL)
        self.place([c1, c2, c3, c4, c5], [1.0, 0.05, -0.85, -1.5, -2.15])
        self.play(FadeIn(c1, shift=0.15 * UP))
        self.glow(c1, VGroup(ld, lw, dpt), OK)
        self.cap("ลำดับนี้ต้องจริงเสมอ: แห้ง ≥ เปียก ≥ จุดน้ำค้าง", color=OK)
        self.play(FadeIn(c2))
        self.play(FadeIn(c3))
        self.play(FadeIn(c4))
        self.cap("ใส่ 35 แทน 308 → มวลผิดไปเกือบ 9 เท่า", color=WARN)
        self.play(FadeIn(c5))
        self.cap("เพราะเหตุนี้ระบบลมต้องมีที่ดักน้ำ (drain, dryer) เสมอ", color=YEL, wait=4.0)
