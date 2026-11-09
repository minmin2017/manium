"""Fluid Power Control exam clips, batch B (2026-11-10, exam 11 Nov).

FXB1_Cushion   6-31E cushion pressure       (W05 การบ้าน บท 6-7 — เฉลย.md)
FXB2_Moisture  hw08 water in compressed air (W08-09 การบ้าน hw08 — เฉลย.md)
FXB3_PumpEff   pump efficiency recap, 5-51E (W04 การบ้าน — Pump Efficiency.md)
FXB4_Cascade   cascade circuit A+ B+ B- A-  (W10 บทเรียน — Pneumatic 03)

Every number on screen is copied from the note's verified steps.
Layout: title + step tag + page_ref on top row, caption_top under it,
figure on the stage, equations in their own zone (never on the figure).
"""
from mlib import *
import numpy as np

LIVE = "#42A5F5"
DEAD = "#546E7A"
SIG = WARN
YEL = "#FFD54F"


def T(s, size=24, color=WHITE):
    return Text(s, font_size=size, color=color)


def M(*parts, size=34, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def pipe(points, color=DEAD, width=3):
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [np.array([p[0], p[1], 0.0]) for p in points])


def harrow(x0, x1, y, color, sw=5):
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25)


class ExamScene(SafeScene):
    def head(self, ttl, ref):
        self.ttl = title(ttl, size=30)
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

    def rows(self, rows, x, y0, gap, max_w):
        for i, r in enumerate(rows):
            fit_width(r, max_w)
            r.move_to([x, y0 - i * gap, 0])
        return VGroup(*rows)


# ======================================================================
class FXB1_Cushion(ExamScene):
    """6-31E: cylinder cushion. p2 = (1570.8 - 150 + 777.4)/2.6998 = 814 psi."""

    def construct(self):
        self.head("6-31E ความดันใน cushion", "W05 · ข้อ 6-31E")
        R, r_pl, r_rod, PW, S = 0.6, 0.225, 0.14, 0.3, 0.6
        xl, xr = -5.4, -2.6
        xp_c = xr - PW / 2 - S          # plunger tip at pocket mouth
        xp0 = xp_c - 1.2
        xp_mid = xp_c + 0.15
        L_rod = 0.05 - (xr - PW / 2 + PW / 2 + S)
        xp = ValueTracker(xp0)
        trap = ValueTracker(0.0)

        barrel = Rectangle(width=xr - xl, height=2 * R, color=METAL,
                           stroke_width=4).move_to([(xl + xr) / 2, 0, 0])
        capL = Rectangle(width=0.25, height=2 * R + 0.3, stroke_width=0,
                         fill_color=METAL, fill_opacity=1).move_to([xl - 0.125, 0, 0])
        capR = Rectangle(width=0.7, height=2 * R + 0.3, stroke_width=0,
                         fill_color=METAL, fill_opacity=1).move_to([xr + 0.35, 0, 0])
        dark = "#1C2329"
        pocket = Rectangle(width=S, height=2 * r_pl + 0.04, stroke_width=0,
                           fill_color=dark, fill_opacity=1).move_to([xr + S / 2, 0, 0])
        hole = Rectangle(width=0.1, height=2 * r_rod + 0.03, stroke_width=0,
                         fill_color=dark, fill_opacity=1).move_to([xr + 0.65, 0, 0])
        chan = Rectangle(width=0.12, height=R + 0.15 - r_pl, stroke_width=0,
                         fill_color=dark, fill_opacity=1).move_to(
            [xr + 0.3, (R + 0.15 + r_pl) / 2, 0])
        outp = pipe([(xr + 0.3, R + 0.15), (xr + 0.3, 1.3), (xr + 1.1, 1.3)],
                    color=LIVE, width=4)
        out_lb = T("ไปถัง", 20, GRAYTXT).next_to(outp.get_end(), RIGHT, buff=0.12)
        inp = pipe([(xl + 0.2, R), (xl + 0.2, 1.3)], color=LIVE, width=4)
        floor = Line([-1.85, -0.5, 0], [1.2, -0.5, 0], color=GRAYTXT, stroke_width=3)

        head_ch = always_redraw(lambda: Rectangle(
            width=max(xp.get_value() - PW / 2 - xl, 0.01), height=2 * R - 0.06,
            stroke_width=0, fill_color=LIVE, fill_opacity=0.35).move_to(
            [(xl + xp.get_value() - PW / 2) / 2, 0, 0]))
        ann_ch = always_redraw(lambda: Rectangle(
            width=max(xr - xp.get_value() - PW / 2, 0.01), height=2 * R - 0.06,
            stroke_width=0, fill_opacity=0.55,
            fill_color=interpolate_color(ManimColor(LIVE), ManimColor(WARN),
                                         trap.get_value())).move_to(
            [(xr + xp.get_value() + PW / 2) / 2, 0, 0]))

        x0 = xp0
        piston = Rectangle(width=PW, height=2 * R - 0.06, stroke_width=0,
                           fill_color=METAL, fill_opacity=1).move_to([x0, 0, 0])
        plunger = Rectangle(width=S, height=2 * r_pl, stroke_width=0,
                            fill_color=CURRENT, fill_opacity=1).move_to(
            [x0 + PW / 2 + S / 2, 0, 0])
        rod = Rectangle(width=L_rod, height=2 * r_rod, stroke_width=0,
                        fill_color="#CFD8DC", fill_opacity=1).move_to(
            [x0 + PW / 2 + S + L_rod / 2, 0, 0])
        rod_end = x0 + PW / 2 + S + L_rod
        box = Rectangle(width=1.0, height=1.0, color=GEAR_OUT, fill_color=GEAR_OUT,
                        fill_opacity=0.25).move_to([rod_end + 0.5, 0, 0])
        w_lb = T("W = 1000 lb", 20, GEAR_OUT).next_to(box, UP, buff=0.12)
        f_ar = harrow(rod_end + 0.9, rod_end + 0.1, -0.68, GRAYTXT, 4)
        f_lb = T("f = 0.15W", 20, GRAYTXT).move_to([rod_end + 0.5, -0.98, 0])
        mover = VGroup(piston, plunger, rod, box, w_lb, f_ar, f_lb)

        q_lb = T("Q = 20 gpm", 22, LIVE).move_to([xl + 0.2, 1.6, 0])
        bore = DoubleArrow([xl - 0.45, -R, 0], [xl - 0.45, R, 0], buff=0,
                           color=GRAYTXT, stroke_width=3, tip_length=0.15)
        bore_lb = T("2 in", 20, GRAYTXT).next_to(bore, LEFT, buff=0.1)
        pl_lb = T("plunger ⌀ 3/4 in", 20, CURRENT).move_to([-3.6, 1.05, 0])
        pl_ar = Arrow(pl_lb.get_bottom(), [xp0 + PW / 2 + S / 2, r_pl, 0], buff=0.06,
                      color=CURRENT, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(barrel), FadeIn(capL, capR, pocket, hole, chan, floor),
                  run_time=1.2)
        self.add(head_ch, ann_ch)
        self.play(FadeIn(mover), Create(inp), Create(outp), FadeIn(out_lb), run_time=1.0)
        self.play(FadeIn(q_lb, bore, bore_lb))
        self.cap("ปั๊มส่งน้ำมัน 20 gpm ดันลูกสูบ (โต 2 in) → ก้านดันกล่อง 1000 lb ไถลบนพื้น")
        self.play(FadeIn(pl_lb), GrowArrow(pl_ar))
        self.cap("ที่ก้านมี plunger ⌀3/4 in ยาว 1 in ติดอยู่หน้าลูกสูบ (สีส้ม)")
        self.play(FadeOut(pl_lb, pl_ar))
        dx = xp_c - xp0
        self.play(xp.animate.set_value(xp_c), mover.animate.shift(dx * RIGHT),
                  run_time=2.4, rate_func=linear)
        self.cap("ใกล้สุดระยะ: plunger เสียบเข้ารูทางออก → น้ำมันฝั่งก้านออกไม่ได้", wait=1.5)
        self.play(xp.animate.set_value(xp_mid), mover.animate.shift(0.15 * RIGHT),
                  trap.animate.set_value(1.0), run_time=1.5)
        p2_lb = T("p2 = ?", 24, WARN).move_to([-3.3, 1.0, 0])
        p2_ar = Arrow(p2_lb.get_bottom(), [-2.9, 0.42, 0], buff=0.05, color=WARN,
                      stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a2_lb = T("A2", 24, WARN).move_to([-3.3, -1.05, 0])
        a2_ar = Arrow(a2_lb.get_top(), [-2.9, -0.42, 0], buff=0.05, color=WARN,
                      stroke_width=3, max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(p2_lb, a2_lb), GrowArrow(p2_ar), GrowArrow(a2_ar))
        self.cap("น้ำมันถูกขังในช่องวงแหวน (พื้นที่ A2) → ความดัน p2 พุ่งสูง = เบรก")
        s_dim = DoubleArrow([xr, -0.95, 0], [xr + S, -0.95, 0], buff=0, color=YEL,
                            stroke_width=3, tip_length=0.12)
        s_lb = T("S = 1 in", 20, YEL).move_to([xr + 0.3, -1.25, 0])
        self.play(GrowFromCenter(s_dim), FadeIn(s_lb))
        self.cap("ต้องหยุดมวลให้ได้ภายในระยะ S = 1 in (ยาวเท่า plunger)")
        p1_lb = T("p1 = 500 psi", 20, WHITE).move_to([(xl + xp_mid - PW / 2) / 2, 0, 0])
        self.play(FadeIn(p1_lb))
        self.cap("ปั๊มยังดันต่อ ลูกสูบรับไม่หมด → relief valve เปิด → p1 = 500 psi")

        # ---------------- step 2
        self.step(2, "สูตร")
        blk = Rectangle(width=2.0, height=0.8, color=GEAR_OUT, fill_color=GEAR_OUT,
                        fill_opacity=0.2).move_to([-3.0, -2.55, 0])
        blk_lb = T("m = W/g", 20, GEAR_OUT).move_to(blk)
        fa = harrow(-5.6, -4.0, -2.45, FORCE)
        fa_lb = M(r"p_1 A", size=30, color=FORCE).move_to([-4.8, -2.05, 0])
        fb = harrow(-0.4, -2.0, -2.35, WARN)
        fb_lb = M(r"p_2 A_2", size=30, color=WARN).move_to([-1.2, -1.97, 0])
        fc = harrow(-0.4, -2.0, -2.8, GRAYTXT)
        fc_lb = M(r"f", size=30, color=GRAYTXT).move_to([-0.15, -2.8, 0])
        fm = DashedLine([-2.3, -3.2, 0], [-3.7, -3.2, 0], color=CURRENT).add_tip(
            tip_length=0.18)
        fm_lb = M(r"a", size=30, color=CURRENT).move_to([-4.0, -3.2, 0])
        self.play(FadeIn(blk, blk_lb))
        self.cap("ตัดเป็นก้อนเดียว: ลูกสูบ + ก้าน + กล่อง (มวล m) ดูแรงที่กระทำ", wait=1.5)
        self.play(GrowArrow(fa), FadeIn(fa_lb))
        self.play(GrowArrow(fb), FadeIn(fb_lb), GrowArrow(fc), FadeIn(fc_lb))
        self.play(Create(fm), FadeIn(fm_lb))
        self.cap("p1A ดันไปหน้า | p2A2 กับ f ต้าน | ความหน่วง a ชี้ถอยหลัง (กำลังเบรก)")

        PX, PMW = 4.15, 5.2
        e1 = M(r"v", r"=", r"\frac{Q}{A}", color=WHITE)
        e2 = M(r"a", r"=", r"\frac{v^2}{2S}")
        e3 = M(r"p_2 A_2", r"+", r"f", r"-", r"p_1 A", r"=", r"m a", size=38)
        e3[0].set_color(WARN); e3[2].set_color(GRAYTXT); e3[4].set_color(FORCE)
        e3[6].set_color(CURRENT)
        e4 = M(r"A_2", r"=", r"A - A_{pl}", r",\quad m=\frac{W}{g}")
        e4[0].set_color(WARN)
        panel = self.rows([e1, e2, e3, e4], PX, 1.75, 0.95, PMW)
        self.play(FadeIn(e1))
        self.glow(e1[2], q_lb, LIVE)
        self.cap("ความเร็วก่อนเบรก v = Q/A (น้ำมันเข้าเท่าไร ลูกสูบเดินเท่านั้น)")
        self.play(FadeIn(e2))
        self.glow(e2[2], s_dim, YEL)
        self.cap("เบรกจาก v ถึง 0 ในระยะ S: v² = 2aS → a = v²/(2S)")
        self.play(FadeIn(e3))
        self.cap("กฎนิวตัน: แรงต้าน − แรงดัน = มวล × ความหน่วง", wait=1.0)
        self.glow(e3[0], fb, WARN)
        self.glow(e3[2], fc, GRAYTXT)
        self.glow(e3[4], fa, FORCE)
        self.glow(e3[6], fm, CURRENT)
        self.play(FadeIn(e4))
        self.glow(e4[2], a2_lb, WARN)
        self.cap("A2 = พื้นที่ลูกสูบ − พื้นที่ plunger (ช่องวงแหวนที่น้ำมันถูกขัง)")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(panel))
        s1 = M(r"Q = 20\times\frac{231}{60}", r"= 77.0\ \text{in}^3/\text{s}", size=32)
        s2 = M(r"A = \frac{\pi (2)^2}{4} = 3.1416\ \text{in}^2", size=32)
        s3 = M(r"A_{pl} = \frac{\pi (0.75)^2}{4} = 0.4418\ \text{in}^2", size=32)
        s4 = M(r"A_2", r"= 3.1416 - 0.4418 = 2.6998\ \text{in}^2", size=32)
        s4[0].set_color(WARN)
        s5 = M(r"v = \frac{77.0}{3.1416} = 24.51\ \text{in/s}", r"= 2.042\ \text{ft/s}",
               size=32)
        g1 = self.rows([s1, s2, s3, s4, s5], PX, 1.85, 0.88, PMW)
        self.cap("แปลง gpm เป็น in³/s ก่อน: 1 gal = 231 in³, 1 min = 60 s", wait=0.5)
        self.play(FadeIn(s1)); self.glow(s1[1], q_lb, LIVE)
        self.play(FadeIn(s2)); self.glow(s2, bore_lb, GRAYTXT)
        self.play(FadeIn(s3)); self.glow(s3, plunger, CURRENT)
        self.play(FadeIn(s4)); self.glow(s4[0], a2_lb, WARN)
        self.play(FadeIn(s5))
        self.cap("v = 24.51 in/s = 2.042 ft/s (หาร 12 เพื่อใช้หน่วย ft กับ g = 32.2)")
        self.play(FadeOut(g1))
        t1 = M(r"a = \frac{(2.042)^2}{2(1/12)} = 25.03\ \text{ft/s}^2", size=32)
        t2 = M(r"m = \frac{1000}{32.2} = 31.06\ \text{slug}", size=32)
        t3 = M(r"m a = 31.06\times 25.03 = 777.4\ \text{lb}", size=32, color=CURRENT)
        t4 = M(r"f = 0.15\times 1000 = 150\ \text{lb}", size=32, color=GRAYTXT)
        t5 = M(r"p_1 A = 500\times 3.1416 = 1570.8\ \text{lb}", size=32, color=FORCE)
        g2 = self.rows([t1, t2, t3, t4, t5], PX, 1.85, 0.88, PMW)
        self.play(FadeIn(t1)); self.glow(t1, s_dim, YEL)
        self.play(FadeIn(t2)); self.glow(t2, blk, GEAR_OUT)
        self.play(FadeIn(t3)); self.glow(t3, fm, CURRENT)
        self.play(FadeIn(t4)); self.glow(t4, fc, GRAYTXT)
        self.play(FadeIn(t5)); self.glow(t5, fa, FORCE)
        self.cap("ได้แรงครบ 3 ตัว แล้วย้ายข้างหา p2", wait=1.5)
        self.play(FadeOut(g2))
        u1 = M(r"p_2", r"=", r"\frac{1570.8 - 150 + 777.4}{2.6998}", size=40)
        u1[0].set_color(WARN)
        u2 = M(r"p_2 \approx 814\ \text{psi}", size=48, color=WARN)
        box2 = SurroundingRectangle(u2, color=WARN, buff=0.15)
        self.rows([u1, u2], PX, 1.3, 1.5, PMW)
        box2.move_to(u2)
        self.play(FadeIn(u1))
        self.glow(u1[2], VGroup(fa, fc, fm), YEL)
        self.play(Write(u2), Create(box2))
        self.play(Transform(p2_lb, T("p2 ≈ 814 psi", 24, WARN).move_to([-3.3, 1.0, 0])))
        self.cap("คำตอบ: p2 ≈ 814 psi", color=WARN)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = T("ตำรา 816 psi → ต่าง 0.25 % (ปัดเศษ v กับ a)", 22, OK)
        c2 = T("SI: p2 = 5.615 MPa = 814.4 psi ✓", 22, OK)
        c3 = T("p2 > p1 เพราะ A2 < A และยังต้องหยุดมวลด้วย ✓", 22, OK)
        g3 = self.rows([c1, c2, c3], PX, -1.3, 0.6, PMW)
        for c in g3:
            self.play(FadeIn(c, shift=0.15 * UP))
            self.wait(1.4)
        self.cap("กับดัก: ใช้ A2 (วงแหวน) ไม่ใช่ A เต็ม และ ma อยู่ฝั่งแรงต้าน", color=YEL,
                 wait=3.5)
        self.wait(1.5)


# ======================================================================
class FXB2_Moisture(ExamScene):
    """hw08: water in 87.0, drain2 30.4, drain3 50.2, water sys 6.4 L/day."""

    def construct(self):
        self.head("hw08 น้ำในลมอัด", "W08-09 · hw08")
        yb = -1.35
        BLU = "#4FC3F7"
        intake = Arrow([-6.85, yb, 0], [-4.35, yb, 0], buff=0, color=LIVE, stroke_width=6)
        in_lb1 = T("300 cfm, 1 atm", 19, GRAYTXT).move_to([-5.65, -1.95, 0])
        in_lb2 = T("30°C, 40%RH", 19, GRAYTXT).move_to([-5.65, -2.3, 0])

        def unit(x, l1, l2, col):
            b = RoundedRectangle(width=2.0, height=0.85, corner_radius=0.12, color=col,
                                 fill_color=col, fill_opacity=0.15).move_to([x, yb, 0])
            t = VGroup(T(l1, 19, WHITE), T(l2, 19, col)).arrange(DOWN, buff=0.06).move_to(b)
            return VGroup(b, t)
        comp = unit(-3.3, "คอมเพรสเซอร์", "6.5 barg", METAL)
        aft = unit(-0.4, "aftercooler", "42°C", BLU)
        dry = unit(2.5, "air dryer", "6°C", OK)
        links = VGroup(pipe([(-2.3, yb), (-1.4, yb)], LIVE, 5),
                       pipe([(0.6, yb), (1.5, yb)], LIVE, 5))
        out = Arrow([3.5, yb, 0], [6.85, yb, 0], buff=0, color=LIVE, stroke_width=6)
        out_lb = T("ท่อลมใช้งาน", 19, GRAYTXT).move_to([5.2, -1.95, 0])

        def drop(x, y):
            return VGroup(Triangle(color=BLU, fill_color=BLU, fill_opacity=1).scale(0.09)
                          .move_to([x, y + 0.07, 0]),
                          Circle(radius=0.09, color=BLU, fill_color=BLU,
                                 fill_opacity=1).move_to([x, y, 0]))
        d2 = VGroup(Line([-0.4, yb - 0.43, 0], [-0.4, -2.25, 0], color=BLU), drop(-0.4, -2.4))
        d3 = VGroup(Line([2.5, yb - 0.43, 0], [2.5, -2.25, 0], color=BLU), drop(2.5, -2.4))
        dw = drop(-5.65, -1.05)
        ds = drop(5.2, -1.05)
        lw = T("Water in = ?", 21, BLU).move_to([-5.65, -2.95, 0])
        l2 = T("Drain 2 = ?", 21, BLU).move_to([-0.4, -2.95, 0])
        l3 = T("Drain 3 = ?", 21, BLU).move_to([2.5, -2.95, 0])
        ls = T("Water sys = ?", 21, BLU).move_to([5.2, -2.95, 0])

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(GrowArrow(intake), FadeIn(in_lb1, in_lb2), run_time=1.0)
        self.play(FadeIn(comp), Create(links[0]), FadeIn(aft), Create(links[1]),
                  FadeIn(dry), GrowArrow(out), FadeIn(out_lb), run_time=1.6)
        self.cap("ดูดอากาศ 300 cfm → บีบอัด 6.5 barg → aftercooler 42°C → dryer 6°C")
        self.play(FadeIn(dw, d2, d3, ds, lw, l2, l3, ls))
        self.cap("ถาม: น้ำเข้ามาเท่าไร และ drain แต่ละจุดทิ้งกี่ลิตรต่อวัน (ทำงาน 14 ชม.)")
        # capacity bar: Pg = full, Pv = 40 %
        bx, by, bw, bh = -4.6, 0.9, 3.4, 0.5
        full = Rectangle(width=bw, height=bh, color=WHITE).move_to([bx, by, 0])
        fill = Rectangle(width=0.4 * bw, height=bh, stroke_width=0, fill_color=BLU,
                         fill_opacity=0.8).align_to(full, LEFT).set_y(by)
        pg_lb = M(r"P_g(30^\circ\text{C}) = 4.265\ \text{kPa}", size=28).next_to(full, UP, buff=0.12)
        pv_lb = M(r"P_v = 1.706", size=28, color=BLU).next_to(full, DOWN, buff=0.12).align_to(full, LEFT)
        self.play(Create(full), FadeIn(pg_lb))
        self.cap("อากาศ 30°C อุ้มไอน้ำได้สูงสุดค่าหนึ่ง = P_g (เปิดตารางไอน้ำ) ยิ่งร้อนยิ่งอุ้มได้มาก")
        self.play(GrowFromEdge(fill, LEFT), FadeIn(pv_lb))
        self.cap("40 %RH = มีไอน้ำอยู่ 40 % ของที่อุ้มได้ → P_v = 0.40 × P_g")
        idea = VGroup(T("บีบอัด → ไอน้ำแน่นขึ้น ~7.4 เท่า", 22, WHITE),
                      T("ทำให้เย็น → อุ้มไม่ไหว → กลั่นเป็นหยดน้ำ → drain", 22, BLU)
                      ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([2.6, 0.9, 0])
        fit_width(idea, 6.3)
        self.play(FadeIn(idea[0]))
        self.glow(idea[0], comp, METAL)
        self.play(FadeIn(idea[1]))
        self.glow(idea[1], VGroup(d2, d3), BLU)
        self.cap("อากาศแห้งไม่หายไปไหน → นับ ω = kg น้ำ ต่อ kg อากาศแห้ง ทีละจุด")
        self.play(FadeOut(full, fill, pg_lb, pv_lb, idea))

        # ---------------- step 2
        self.step(2, "สูตร")
        f1 = M(r"P_v", r"=", r"\phi", r"P_g(T)", size=36)
        f1[0].set_color(BLU); f1[3].set_color(YEL)
        f2 = M(r"\omega", r"= 0.622\,\frac{P_v}{P - P_v}", size=36)
        f2[0].set_color(OK)
        f3 = M(r"m_a", r"= \frac{P_a V}{R_a T}", r"\quad (T\ \text{in K})", size=36)
        g = self.rows([f1, f2, f3], 0, 1.9, 0.78, 12.0)
        self.play(FadeIn(f1)); self.glow(f1[3], aft, YEL)
        self.cap("P_g ดูที่อุณหภูมิของจุดนั้น (30, 42 หรือ 6°C) ไม่ใช่ 30°C ทุกจุด")
        self.play(FadeIn(f2))
        w_lbs = VGroup(*[T(s, 20, OK).move_to([x, -0.6, 0]) for s, x in
                         (("ω1", -5.65), ("ω1", -3.3), ("ω2", -0.4), ("ω3", 2.5))])
        self.play(FadeIn(w_lbs))
        self.glow(f2[0], w_lbs, OK)
        self.cap("ω ที่แต่ละจุด: หลังอุปกรณ์ที่น้ำกลั่น อากาศอิ่มตัว → ใช้ P_v = P_g(T)")
        self.play(FadeIn(f3))
        self.glow(f3[0], intake, LIVE)
        self.cap("m_a = มวลอากาศแห้งต่อนาที (กฎแก๊สกับความดันย่อย P_a = P − P_v)")
        self.play(FadeOut(f1, f2, f3))
        f4 = M(r"\text{Drain}", r"=", r"(\omega_{before} - \omega_{after})", r"\, m_a\, t",
               size=38)
        f4[0].set_color(BLU); f4[2].set_color(OK)
        self.rows([f4], 0, 1.5, 0.8, 12.0)
        self.play(FadeIn(f4))
        self.glow(f4[0], d2, BLU)
        self.cap("น้ำที่ทิ้ง = ω ที่ลดลง × มวลอากาศแห้ง × เวลา (น้ำ 1 kg ≈ 1 L)")
        self.play(FadeOut(f4))

        # ---------------- step 3
        self.step(3, "แทนค่า")
        a1 = M(r"P_g(30) = 4 + \frac{30 - 28.96}{32.88 - 28.96}(1) = 4.265\ \text{kPa}", size=32)
        a2 = M(r"P_v = 0.40\times 4.265 = 1.706,\quad P_a = 101.325 - 1.706 = 99.62\ \text{kPa}", size=32)
        a3 = M(r"\omega_1 = 0.622\times\frac{1.706}{99.62} = 0.010653", size=32, color=OK)
        g = self.rows([a1, a2, a3], 0, 1.95, 0.8, 12.4)
        self.cap("จุดที่ 1 อากาศเข้า: เปิดตาราง (สไลด์ W08 หน้า 12) แล้ว interpolate", wait=0.8)
        self.play(FadeIn(a1)); self.glow(a1, in_lb2, YEL)
        self.play(FadeIn(a2)); self.play(FadeIn(a3))
        self.play(Transform(w_lbs[0], T("ω1 = 10.65 g/kg", 19, OK).move_to([-5.65, -0.6, 0])),
                  Transform(w_lbs[1], T("10.65 g/kg", 19, OK).move_to([-3.3, -0.6, 0])))
        self.glow(a3, w_lbs[0], OK)
        self.play(FadeOut(g))
        b1 = M(r"V = 300\times 0.028317 = 8.495\ \text{m}^3/\text{min},\quad T = 303.15\ \text{K}", size=32)
        b2 = M(r"m_a = \frac{99.62\times 8.495}{0.287\times 303.15} = 9.727\ \text{kg/min}", size=32)
        b3 = M(r"\text{Water in} = 0.010653\times 9.727\times 840 = 87.0\ \text{L/day}", size=32, color=BLU)
        g = self.rows([b1, b2, b3], 0, 1.95, 0.8, 12.4)
        self.play(FadeIn(b1)); self.glow(b1, in_lb1, YEL)
        self.play(FadeIn(b2))
        self.cap("เวลา 14 hr × 60 = 840 min ต่อวัน (ไม่ใช่ 24 hr)", wait=0.8)
        self.play(FadeIn(b3))
        self.play(Transform(lw, T("Water in = 87.0", 21, BLU).move_to(lw)))
        self.glow(b3, lw, BLU)
        self.play(FadeOut(g))
        c1 = M(r"P_2 = 650 + 101.325 = 751.3\ \text{kPa abs}", size=32)
        c2 = M(r"\text{no condensing: } P_v = 1.706\times\frac{751.3}{101.325} = 12.65 > P_g(42) = 8.274", size=32, color=WARN)
        c3 = M(r"\omega_2 = 0.622\times\frac{8.274}{751.3 - 8.274} = 0.006926", size=32, color=OK)
        g = self.rows([c1, c2, c3], 0, 1.95, 0.8, 12.4)
        self.cap("จุดที่ 2 aftercooler: ความดันต้องเป็นสัมบูรณ์ 6.5 barg → 751.3 kPa", wait=0.8)
        self.play(FadeIn(c1)); self.glow(c1, comp, METAL)
        self.play(FadeIn(c2)); self.glow(c2, aft, WARN)
        self.cap("ไอน้ำ 12.65 kPa > ที่ 42°C อุ้มได้ 8.274 kPa → อุ้มไม่ไหว น้ำกลั่นจริง")
        self.play(FadeIn(c3))
        self.play(Transform(w_lbs[2], T("ω2 = 6.93 g/kg", 19, OK).move_to([-0.4, -0.6, 0])))
        self.glow(c3, w_lbs[2], OK)
        self.play(FadeOut(g))
        e1 = M(r"\text{Drain 2} = (0.010653 - 0.006926)(9.727)(840) = 30.4\ \text{L/day}", size=32, color=BLU)
        e2 = M(r"P_g(6) = 0.6113 + \frac{6 - 0.01}{6.98 - 0.01}(0.3887) = 0.9453\ \text{kPa}", size=32)
        e3 = M(r"\omega_3 = 0.622\times\frac{0.9453}{751.3 - 0.945} = 0.000784", size=32, color=OK)
        g = self.rows([e1, e2, e3], 0, 1.95, 0.8, 12.4)
        self.play(FadeIn(e1))
        self.play(Transform(l2, T("Drain 2 = 30.4", 21, BLU).move_to(l2)))
        self.glow(e1, d2, BLU)
        self.cap("จุดที่ 3 dryer: เย็นถึง 6°C ที่ความดันเดิม → อิ่มตัวที่ 6°C", wait=0.8)
        self.play(FadeIn(e2)); self.glow(e2, dry, OK)
        self.play(FadeIn(e3))
        self.play(Transform(w_lbs[3], T("ω3 = 0.78 g/kg", 19, OK).move_to([2.5, -0.6, 0])))
        self.glow(e3, w_lbs[3], OK)
        self.play(FadeOut(g))
        h1 = M(r"\text{Drain 3} = (0.006926 - 0.000784)(9.727)(840) = 50.2\ \text{L/day}", size=32, color=BLU)
        h2 = M(r"\text{Water sys} = 0.000784\times 9.727\times 840 = 6.4\ \text{L/day}", size=32, color=BLU)
        g = self.rows([h1, h2], 0, 1.75, 0.85, 12.4)
        self.play(FadeIn(h1))
        self.play(Transform(l3, T("Drain 3 = 50.2", 21, BLU).move_to(l3)))
        self.glow(h1, d3, BLU)
        self.play(FadeIn(h2))
        self.play(Transform(ls, T("Water sys = 6.4", 21, BLU).move_to(ls)))
        self.glow(h2, ds, BLU)
        self.cap("น้ำที่เหลือหลุดเข้าท่อลมใช้งาน ~6.4 ลิตรต่อวัน (หน่วย L/day ทุกค่า)")
        self.play(FadeOut(g))

        # ---------------- step 4
        self.step(4, "ตรวจ")
        k1 = M(r"30.4 + 50.2 + 6.4 = 87.0", r"\ \checkmark", size=44, color=BLU)
        k1[1].set_color(OK)
        self.rows([k1], 0, 1.75, 0.8, 12.0)
        self.play(FadeIn(k1))
        self.glow(k1, VGroup(lw, l2, l3, ls), BLU)
        self.cap("น้ำที่ทิ้ง + น้ำที่หลุด = น้ำที่เข้า → มวลน้ำอนุรักษ์ คำตอบถูก", color=OK)
        traps = VGroup(T("กับดัก ① ความดันสัมบูรณ์ 751.3 kPa  ② T เป็น K", 22, YEL),
                       T("③ P_g ดูที่อุณหภูมิของจุดนั้น  ④ 14 hr = 840 min", 22, YEL)
                       ).arrange(DOWN, buff=0.2)
        self.rows([traps], 0, 0.6, 0.8, 12.0)
        self.play(FadeIn(traps))
        self.wait(4.0)


# ======================================================================
class FXB3_PumpEff(ExamScene):
    """Pump efficiency recap on 5-51E: eta_o 80 %, T_T 954.9, eta_m 86.8 %."""

    def construct(self):
        self.head("ประสิทธิภาพปั๊ม: สูตรสอบ + กับดัก", "W04 · ข้อ 5-51E")
        yb = -1.65
        elec = Arrow([-6.85, yb, 0], [-5.65, yb, 0], buff=0, color=CURRENT, stroke_width=6)
        el_lb = T("ไฟฟ้า", 19, CURRENT).move_to([-6.25, yb - 0.45, 0])
        mot = VGroup(RoundedRectangle(width=1.8, height=0.9, corner_radius=0.12, color=METAL,
                                      fill_color=METAL, fill_opacity=0.15),
                     T("มอเตอร์", 20)).move_to([-4.7, yb, 0])
        shaft = Rectangle(width=2.2, height=0.16, stroke_width=0, fill_color="#CFD8DC",
                          fill_opacity=1).move_to([-2.7, yb, 0])
        sh_lb = M(r"T_A,\ N", size=30, color=TORQUE).move_to([-2.7, yb + 0.42, 0])
        pump = VGroup(Circle(radius=0.6, color=GEAR_IN, fill_color=GEAR_IN, fill_opacity=0.15),
                      M(r"V_D", size=28, color=GEAR_IN)).move_to([-0.95, yb, 0])
        oil = Arrow([-0.35, yb, 0], [3.4, yb, 0], buff=0, color=LIVE, stroke_width=6)
        oil_lb = M(r"P,\ Q_A", size=30, color=LIVE).move_to([1.5, yb + 0.42, 0])
        fl_lb = T("กำลังของไหล", 19, LIVE).move_to([4.5, yb, 0])
        fric = Arrow([-1.35, yb - 0.5, 0], [-2.0, -2.85, 0], buff=0, color=WARN, stroke_width=4)
        fr_lb = T("เสียดทาน → ηm", 19, WARN).move_to([-2.7, -3.15, 0])
        leak = Arrow([-0.55, yb - 0.5, 0], [0.1, -2.85, 0], buff=0, color=WARN, stroke_width=4)
        lk_lb = T("รั่วไหล → ηv", 19, WARN).move_to([0.8, -3.15, 0])

        self.step(1, "เข้าใจ")
        self.play(GrowArrow(elec), FadeIn(el_lb, mot), run_time=0.9)
        self.play(FadeIn(shaft, sh_lb, pump), run_time=0.9)
        self.play(GrowArrow(oil), FadeIn(oil_lb, fl_lb), run_time=0.9)
        self.cap("กำลังไหล: ไฟฟ้า → มอเตอร์ → เพลา (T_A, N) → ปั๊ม → น้ำมัน (P, Q_A)")
        self.play(GrowArrow(fric), FadeIn(fr_lb))
        self.cap("เสียที่ 1: แรงเสียดทานในปั๊ม → ต้องใช้แรงบิดจริง T_A มากกว่าทฤษฎี T_T")
        self.play(GrowArrow(leak), FadeIn(lk_lb))
        self.cap("เสียที่ 2: น้ำมันรั่วภายใน → ไหลออกจริง Q_A น้อยกว่าทฤษฎี Q_T")

        self.step(2, "สูตร")
        r1 = M(r"\eta_v", r"=", r"\frac{Q_A}{Q_T}", r",\quad Q_T =", r"V_D N", size=34)
        r1[0].set_color(WARN)
        r2 = M(r"\eta_m", r"=", r"\frac{T_T}{T_A}", r",\quad T_T =", r"\frac{P V_D}{2\pi}", size=34)
        r2[0].set_color(WARN)
        r3 = M(r"\eta_o", r"=", r"\eta_v\,\eta_m", r"=", r"\frac{HP_{out}}{HP_{in}}", size=34)
        r3[0].set_color(OK)
        r4 = M(r"HP_{out} = \frac{P(\text{psi})\,Q(\text{gpm})}{1714}", r"\qquad",
               r"HP_{in} = \frac{T(\text{in lb})\,N(\text{rpm})}{63025}", size=32)
        g = self.rows([r1, r2, r3, r4], 0.6, 2.0, 0.82, 11.0)
        self.play(FadeIn(r1)); self.glow(r1[2], oil_lb, LIVE); self.glow(r1[4], pump, GEAR_IN)
        self.cap("ηv = ไหลจริง / ไหลทฤษฎี (Q_T = ปริมาตรต่อรอบ × รอบ)", wait=1.8)
        self.play(FadeIn(r2)); self.glow(r2[2], sh_lb, TORQUE)
        self.cap("ηm = แรงบิดทฤษฎี / แรงบิดจริง (สลับเศษส่วนกับ ηv ระวัง!)", color=YEL)
        self.play(FadeIn(r3)); self.glow(r3[2], VGroup(fric, leak), OK)
        self.cap("ηo = ηv × ηm = กำลังของไหลออก / กำลังเพลาเข้า")
        self.play(FadeIn(r4))
        self.glow(r4[0], oil_lb, LIVE); self.glow(r4[2], sh_lb, TORQUE)
        self.cap("ทางลัดหน่วยอังกฤษ: 1714 (psi·gpm → hp) และ 63025 (in·lb·rpm → hp)")
        self.play(FadeOut(g))

        self.step(3, "แทนค่า 5-51E")
        giv = M(r"V_D = 6\ \text{in}^3,\ Q_A = 24\ \text{gpm},\ N = 1000\ \text{rpm},\ "
                r"P = 1000\ \text{psi},\ T_A = 1100\ \text{in lb}", size=30, color=GRAYTXT)
        q1 = M(r"HP_{out} = \frac{1000\times 24}{1714} = 14.0\ \text{hp}", size=32, color=LIVE)
        q2 = M(r"HP_{in} = \frac{1100\times 1000}{63025} = 17.45\ \text{hp}", size=32, color=TORQUE)
        q3 = M(r"\eta_o = \frac{14.0}{17.45} = 80\%", size=36, color=OK)
        g = self.rows([giv, q1, q2, q3], 0.6, 2.0, 0.82, 11.5)
        self.play(FadeIn(giv))
        self.cap("โจทย์ให้: ปั๊ม 6 in³/rev ส่ง 24 gpm ที่ 1000 rpm, 1000 psi, แรงบิดเข้า 1100 in·lb",
                 wait=2.0)
        self.play(FadeIn(q1)); self.glow(q1, oil_lb, LIVE)
        self.play(FadeIn(q2)); self.glow(q2, sh_lb, TORQUE)
        self.play(FadeIn(q3))
        self.cap("(a) ηo = 80 %", color=OK, wait=1.5)
        self.play(FadeOut(q1, q2, q3))
        w1 = M(r"T_T = \frac{1000\times 6}{2\pi} = 954.9\ \text{in lb}", size=32, color=TORQUE)
        w2 = M(r"\eta_m = \frac{954.9}{1100} = 86.8\%", size=32, color=WARN)
        w3 = M(r"Q_T = \frac{6\times 1000}{231} = 25.97\ \text{gpm}", r",\quad \eta_v = \frac{24}{25.97} = 92.4\%",
               size=32, color=WARN)
        self.rows([w1, w2, w3], 0.6, 1.18, 0.82, 11.5)
        self.play(FadeIn(w1)); self.glow(w1, pump, GEAR_IN)
        self.cap("(b) แรงบิดทฤษฎี T_T = 954.9 in·lb — ไม่ใช่ 1100 ที่โจทย์ให้", color=YEL)
        self.play(FadeIn(w2)); self.glow(w2, fric, WARN)
        self.play(FadeIn(w3)); self.glow(w3, leak, WARN)
        self.cap("แปลง in³/min เป็น gpm: หาร 231 แล้วเทียบกับ 24 gpm ที่ไหลจริง")
        self.play(FadeOut(giv, w1, w2, w3))

        self.step(4, "ตรวจ + กับดัก")
        k = M(r"\eta_v\,\eta_m = 0.924\times 0.868 = 0.802 \approx \eta_o", r"\ \checkmark",
              size=38, color=OK)
        self.rows([k], 0.6, 1.95, 0.8, 11.0)
        self.play(FadeIn(k))
        self.cap("ηv × ηm ต้องได้ ηo กลับมา → ตัวเลขสอดคล้องกัน", color=OK)
        tr = VGroup(T("① T_A > T_T เสมอ (1100 > 954.9) ส่วนต่างคือเสียดทาน", 22, YEL),
                    T("② ย้อนจากกำลังออก → เข้า: หารด้วย η (ไม่ใช่คูณ)", 22, YEL),
                    T("③ ได้ η เกิน 100 % = คิดผิดแน่นอน", 22, YEL),
                    T("④ โจทย์อาจให้ข้อมูลเกิน เช่น V_D ใน 5-55E ไม่ได้ใช้", 22, YEL)
                    ).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        self.rows([tr], 0.6, 0.35, 0.8, 11.0)
        for t in tr:
            self.play(FadeIn(t, shift=0.15 * UP))
            self.wait(1.6)
        self.wait(2.0)


# ======================================================================
class FXB4_Cascade(ExamScene):
    """Cascade A+ B+ / B- A-: 2 groups -> 2 lines, 1 cascade valve."""

    def construct(self):
        self.head("วงจร Cascade: A+ B+ B− A−", "W10 · Pneumatic 03 หน้า 2-9")
        yc, yv, y1, y2 = 1.5, 0.3, -1.0, -1.6

        def cylinder(x0, x1, name, col):
            barrel = Rectangle(width=x1 - x0, height=0.55, color=col).move_to([(x0 + x1) / 2, yc, 0])
            pist = Rectangle(width=0.14, height=0.5, stroke_width=0, fill_color=col,
                             fill_opacity=1).move_to([x0 + 0.25, yc, 0])
            rod = Rectangle(width=x1 - x0 + 0.05, height=0.12, stroke_width=0,
                            fill_color="#CFD8DC", fill_opacity=1)
            rod.move_to([x0 + 0.25 + rod.width / 2, yc, 0])
            nm = T(name, 24, col).move_to([(x0 + x1) / 2, yc + 0.48, 0])
            return barrel, VGroup(pist, rod), nm

        bA, mA, nA = cylinder(-6.2, -3.8, "A", GEAR_IN)
        bB, mB, nB = cylinder(-1.8, 0.6, "B", GEAR_OUT)

        def marker(x, name, col):
            tri = Triangle(color=col, fill_color=col, fill_opacity=1).scale(0.09).rotate(PI)
            tri.move_to([x, yc + 0.26, 0])
            lb = T(name, 20, col).move_to([x, yc + 0.5, 0])
            return VGroup(tri, lb)
        tipA0 = mA[1].get_right()[0]
        tipB0 = mB[1].get_right()[0]
        mk = {"a0": marker(tipA0, "a0", GEAR_IN), "a1": marker(tipA0 + 1.0, "a1", GEAR_IN),
              "b0": marker(tipB0, "b0", GEAR_OUT), "b1": marker(tipB0 + 1.0, "b1", GEAR_OUT)}

        def valve(xc, name, col):
            sq_l = Square(0.6, color=col).move_to([xc - 0.3, yv, 0])
            sq_r = Square(0.6, color=col).move_to([xc + 0.3, yv, 0])
            return VGroup(sq_l, sq_r)
        vA = valve(-5.0, "VA", GEAR_IN)
        vB = valve(-0.6, "VB", GEAR_OUT)
        vA_lb = T("วาล์ว A", 18, GEAR_IN).move_to([-5.0, yv - 0.5, 0])
        vB_lb = T("วาล์ว B", 18, GEAR_OUT).move_to([-0.6, yv - 0.5, 0])
        feeds = VGroup(
            pipe([(-5.3, yv + 0.3), (-5.3, 0.95), (-6.0, 0.95), (-6.0, yc - 0.275)], METAL, 2),
            pipe([(-4.7, yv + 0.3), (-4.7, 0.95), (-4.0, 0.95), (-4.0, yc - 0.275)], METAL, 2),
            pipe([(-0.9, yv + 0.3), (-0.9, 0.95), (-1.6, 0.95), (-1.6, yc - 0.275)], METAL, 2),
            pipe([(-0.3, yv + 0.3), (-0.3, 0.95), (0.4, 0.95), (0.4, yc - 0.275)], METAL, 2))
        pil = {"A+": T("A+", 18, WHITE).move_to([-6.15, 0.66, 0]),
               "A-": T("A−", 18, WHITE).move_to([-3.85, 0.66, 0]),
               "B+": T("B+", 18, WHITE).move_to([-1.75, 0.66, 0]),
               "B-": T("B−", 18, WHITE).move_to([0.55, 0.66, 0])}

        def cyl_fig():
            return VGroup(bA, mA, nA, bB, mB, nB, *mk.values(), vA, vB, vA_lb, vB_lb,
                          feeds, *pil.values())

        def shift_valve(v, side, col):
            on, off = (v[0], v[1]) if side == "L" else (v[1], v[0])
            return AnimationGroup(on.animate.set_fill(col, 0.45), off.animate.set_fill(col, 0.0))

        # ---------------- step 1: the problem
        self.step(1, "เข้าใจปัญหา")
        self.play(FadeIn(cyl_fig()), run_time=1.2)
        self.cap("ลำดับงาน A+ B+ B− A− : ลิมิตวาล์ว a0 a1 b0 b1 อยู่ที่ปลายก้าน")
        self.play(mA.animate.shift(RIGHT), shift_valve(vA, "L", GEAR_IN), run_time=1.2)
        self.play(mB.animate.shift(RIGHT), shift_valve(vB, "L", GEAR_OUT), run_time=1.2)
        bad1 = pipe([(-2.5, yc - 0.12), (-2.5, -0.35), (-1.75, -0.35), (-1.75, yv), (-1.2, yv)], SIG, 4)
        bad2 = pipe([(1.9, yc - 0.12), (1.9, yv), (0.0, yv)], SIG, 4)
        self.play(Create(bad1))
        self.cap("ถ้าต่อตรง: a1 ยังถูกกดอยู่ (A ยังยืด) → ลมสั่ง B+ ค้างอยู่ตลอด", wait=2.0)
        self.play(Create(bad2))
        x_lb = T("ลมชน 2 ฝั่ง!", 22, WARN).move_to([0.2, -0.6, 0])
        self.play(FadeIn(x_lb), Indicate(vB, color=WARN, scale_factor=1.0))
        self.cap("b1 สั่ง B− แต่ B+ ยังมีลมดันอีกฝั่ง → วาล์ว B ไม่ขยับ = สัญญาณค้าง", color=WARN)
        self.play(FadeOut(bad1, bad2, x_lb))
        self.play(mB.animate.shift(LEFT), mA.animate.shift(LEFT),
                  vA[0].animate.set_fill(GEAR_IN, 0), vB[0].animate.set_fill(GEAR_OUT, 0),
                  run_time=1.0)

        # ---------------- step 2: grouping
        self.step(2, "แบ่งกรุ๊ป")
        PX = 4.75
        grp = M(r"\underbrace{A+\ B+}_{G1}", r"\ /\ ", r"\underbrace{B-\ A-}_{G2}", size=36)
        grp[0].set_color(LIVE); grp[2].set_color(OK)
        rule = T("ตัวอักษรเดียวกันห้ามอยู่กรุ๊ปเดียวกัน", 20, YEL)
        cnt = VGroup(T("2 กรุ๊ป → เส้นลม 2 เส้น", 20, WHITE),
                     T("วาล์วคาสเคด = 2 − 1 = 1 ตัว", 20, WHITE)).arrange(DOWN, buff=0.1)
        self.rows([grp, rule, cnt], PX, 1.75, 0.85, 4.0)
        cnt.move_to([PX, 0.35, 0])
        self.play(FadeIn(grp))
        self.cap("ตัด B+ กับ B− ไว้คนละกรุ๊ป: A+ B+ | B− A−")
        self.play(FadeIn(rule))
        self.glow(rule)
        self.play(FadeIn(cnt))
        self.cap("แต่ละกรุ๊ปมีเส้นลมของตัวเอง มีลมได้ทีละเส้นเดียว")
        L1 = Line([-6.4, y1, 0], [2.2, y1, 0], color=DEAD, stroke_width=5)
        L2 = Line([-6.4, y2, 0], [2.2, y2, 0], color=LIVE, stroke_width=5)
        L1_lb = T("L1", 20, LIVE).move_to([-6.75, y1, 0])
        L2_lb = T("L2", 20, OK).move_to([-6.75, y2, 0])
        cv = VGroup(Square(0.6, color=WHITE).move_to([-2.3, -2.65, 0]),
                    Square(0.6, color=WHITE).move_to([-1.7, -2.65, 0]))
        cv[1].set_fill(OK, 0.45)
        cv_lb = T("วาล์วคาสเคด", 18, WHITE).move_to([-0.15, -3.05, 0])
        sup = Arrow([-2.0, -3.6, 0], [-2.0, -2.95, 0], buff=0, color=LIVE, stroke_width=4)
        sup_lb = T("ลมหลัก", 18, LIVE).move_to([-3.0, -3.45, 0])
        cvo1 = pipe([(-2.3, -2.35), (-2.3, y1)], DEAD, 3)
        cvo2 = pipe([(-1.7, -2.35), (-1.7, y2)], LIVE, 3)
        self.play(Create(L1), Create(L2), FadeIn(L1_lb, L2_lb), run_time=1.0)
        self.play(FadeIn(cv, cv_lb), GrowArrow(sup), FadeIn(sup_lb), Create(cvo1), Create(cvo2))
        self.cap("วาล์วคาสเคดเลือกจ่ายลมหลักให้ L1 หรือ L2 — ตอนเริ่มลมค้างที่ L2 (กรุ๊ปสุดท้าย)")

        def sbox(x, y, name):
            b = Rectangle(width=0.62 if len(name) < 4 else 1.1, height=0.36, color=WHITE,
                          fill_color=BLACK, fill_opacity=1).move_to([x, y, 0])
            return VGroup(b, T(name, 17, WHITE).move_to(b))
        r_A1 = pipe([(-6.2, y1), (-6.2, yv), (-5.6, yv)])
        s_a1 = sbox(-3.0, y1, "a1")
        r_a1 = pipe([(-3.0, y1 + 0.18), (-3.0, -0.2), (-1.75, -0.2), (-1.75, yv), (-1.2, yv)])
        s_b1 = sbox(1.5, y1, "b1")
        r_b1 = pipe([(1.5, y1 - 0.18), (1.5, -2.65), (-1.4, -2.65)])
        r_B2 = pipe([(0.6, y2), (0.6, yv), (0.0, yv)])
        s_b0 = sbox(-4.6, y2, "b0")
        r_b0 = pipe([(-4.6, y2 + 0.18), (-4.6, -0.55), (-3.85, -0.55), (-3.85, yv), (-4.4, yv)])
        s_st = sbox(-3.4, y2, "START·a0")
        r_st = pipe([(-3.4, y2 - 0.18), (-3.4, -2.65), (-2.6, -2.65)])
        routes = VGroup(r_A1, r_a1, r_b1, r_B2, r_b0, r_st)
        boxes = VGroup(s_a1, s_b1, s_b0, s_st)
        self.play(Create(routes), FadeIn(boxes), run_time=1.5)
        self.cap("ลิมิตวาล์วแต่ละตัวรับลมจากเส้นของกรุ๊ปที่มันอยู่ (กล่องวางบนเส้นนั้น)")

        # ---------------- step 3: step-through
        self.step(3, "เดินทีละสเต็ป")
        tbl = VGroup(*[T(s, 19, WHITE) for s in (
            "1) START·a0 → L1 มีลม → A+",
            "2) a1 (จาก L1) → B+",
            "3) b1 (จาก L1) → L2 มีลม → B−",
            "4) b0 (จาก L2) → A−",
            "จบ: L2 ค้างไว้ รอ START")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        fit_width(tbl, 4.0)
        tbl.move_to([PX, -1.55, 0])
        self.play(FadeOut(cnt))

        # 1
        self.play(FadeIn(tbl[0]))
        self.play(r_st.animate.set_color(SIG), Indicate(s_st, color=SIG, scale_factor=1.0),
                  Indicate(mk["a0"], color=WHITE, scale_factor=1.0))
        self.play(cv[0].animate.set_fill(LIVE, 0.45), cv[1].animate.set_fill(OK, 0),
                  L1.animate.set_color(LIVE), L2.animate.set_color(DEAD),
                  cvo1.animate.set_color(LIVE), cvo2.animate.set_color(DEAD),
                  r_st.animate.set_color(DEAD), run_time=1.0)
        self.cap("กด START (และ a0 ยืนยันว่า A อยู่บ้าน) → วาล์วคาสเคดสลับ → L1 มีลม", wait=1.5)
        self.play(r_A1.animate.set_color(SIG), Indicate(pil["A+"], color=SIG))
        self.play(shift_valve(vA, "L", GEAR_IN), mA.animate.shift(RIGHT), run_time=1.4)
        self.cap("L1 ต่อตรงเข้า A+ (สเต็ปแรกของกรุ๊ป 1) → A ยืดออก")
        # 2
        self.play(FadeIn(tbl[1]))
        self.play(Indicate(mk["a1"], color=WHITE, scale_factor=1.0), r_a1.animate.set_color(SIG),
                  Indicate(s_a1, color=SIG, scale_factor=1.0))
        self.play(shift_valve(vB, "L", GEAR_OUT), mB.animate.shift(RIGHT), run_time=1.4)
        self.cap("A ชน a1 → a1 รับลมจาก L1 ส่งไป B+ → B ยืดออก (ยังอยู่กรุ๊ป 1)")
        # 3
        self.play(FadeIn(tbl[2]))
        self.play(Indicate(mk["b1"], color=WHITE, scale_factor=1.0), r_b1.animate.set_color(SIG),
                  Indicate(s_b1, color=SIG, scale_factor=1.0))
        self.cap("B ชน b1 → ถัดไปคือ B− คนละกรุ๊ป → b1 ไม่สั่ง B− ตรงๆ แต่สั่งวาล์วคาสเคด", wait=2.0)
        self.play(cv[1].animate.set_fill(OK, 0.45), cv[0].animate.set_fill(LIVE, 0),
                  L2.animate.set_color(LIVE), L1.animate.set_color(DEAD),
                  cvo2.animate.set_color(LIVE), cvo1.animate.set_color(DEAD),
                  r_A1.animate.set_color(DEAD), r_a1.animate.set_color(DEAD),
                  r_b1.animate.set_color(DEAD), run_time=1.2)
        self.glow(pil["B+"], r_a1, WARN)
        self.cap("L1 หมดลม → สาย a1 → B+ ไม่มีลมแล้ว แม้ a1 ยังถูกกดอยู่ = ไม่มีลมชน", color=OK)
        self.play(r_B2.animate.set_color(SIG), Indicate(pil["B-"], color=SIG))
        self.play(shift_valve(vB, "R", GEAR_OUT), mB.animate.shift(LEFT), run_time=1.4)
        self.cap("L2 ต่อตรงเข้า B− (สเต็ปแรกของกรุ๊ป 2) → B หดกลับได้ทันที")
        # 4
        self.play(FadeIn(tbl[3]))
        self.play(Indicate(mk["b0"], color=WHITE, scale_factor=1.0), r_b0.animate.set_color(SIG),
                  Indicate(s_b0, color=SIG, scale_factor=1.0), r_B2.animate.set_color(DEAD))
        self.play(shift_valve(vA, "R", GEAR_IN), mA.animate.shift(LEFT), run_time=1.4)
        self.cap("B ชน b0 → b0 รับลมจาก L2 ส่งไป A− → A หดกลับ")
        self.play(FadeIn(tbl[4]), r_b0.animate.set_color(DEAD))
        self.cap("ครบรอบ: L2 ยังมีลมค้าง รอกด START รอบใหม่ (a0 ถูกกดอีกครั้ง)")

        # ---------------- step 4: check
        self.step(4, "ตรวจ")
        self.play(FadeOut(rule))
        chk = T("ทุกขณะ มีลมแค่เส้นเดียว\n→ สัญญาณกรุ๊ปเก่าถูกตัดเอง", 20, OK)
        self.rows([chk], PX, 1.0, 0.8, 4.2)
        self.play(FadeIn(chk))
        self.glow(chk, VGroup(L1, L2), OK)
        self.cap("สูตรสอบ: เส้นลม = จำนวนกรุ๊ป, วาล์วคาสเคด = กรุ๊ป − 1 (ตัวอย่าง 3 กรุ๊ป → 2 ตัว)",
                 color=YEL, wait=4.0)
        self.wait(1.5)
