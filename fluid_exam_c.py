"""Fluid Power Control exam clips, batch C (2026-11-10, exam 11 Nov).

Worked problems for the formula pages of hydraulic06 (W06 Hydraulic Ancillary):
FXC1_ReservoirSizing     page 4   10 gpm -> 30 gal -> 113.6 L
FXC2_ConductorSize       page 5   0.002 m3/s -> D suction 46.1 mm / delivery 20.4 mm
FXC3_PressureRating      page 6   tube 1 x 0.065 in, S 55,000 psi -> BP 8,218 -> WP 1,370
FXC4_PipeTableBP         page 7+10  sched 40 vs 80: t 0.133 / 0.179 in, BP ~13,950 / ~20,580

Every number on screen is copied from the note's verified steps
(Exam_Prep/Fluid Power Control/W06 บทเรียน — Hydraulic Ancillary).
Layout (same as fluid_exam_b.py): step tag + title + page_ref on top row,
caption_top under it, figure on the left stage, equations in the right panel.
"""
from mlib import *
import numpy as np

LIVE = "#42A5F5"
YEL = "#FFD54F"
BG = "#1C2329"
PX, PMW = 4.15, 5.2


def T(s, size=24, color=WHITE):
    return Text(s, font_size=size, color=color)


def M(*parts, size=34, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def pipe(points, color=METAL, width=4):
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [np.array([p[0], p[1], 0.0]) for p in points])


def arr(a, b, color, sw=3):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.05, color=color,
                 stroke_width=sw, max_tip_length_to_length_ratio=0.2)


def dim(a, b, color=GRAYTXT, sw=3, tip=0.13):
    return DoubleArrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0, color=color,
                       stroke_width=sw, tip_length=tip)


def ring(c, ro, ri, color=METAL):
    outer = Circle(radius=ro, color=color, stroke_width=2, fill_color=color,
                   fill_opacity=1).move_to(c)
    inner = Circle(radius=ri, color=color, stroke_width=2, fill_color=BG,
                   fill_opacity=1).move_to(c)
    return VGroup(outer, inner)


class ExamScene(SafeScene):
    def head(self, ttl, ref):
        self.ttl = fit_width(title(ttl, size=30), 7.0)
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

    def cap(self, txt, color=GRAYTXT, wait=2.8):
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

    def show_rows(self, g, wait=1.2):
        for r in g:
            self.play(FadeIn(r, shift=0.15 * UP))
            self.wait(wait)

    def answer(self, mob, y, color=WARN):
        mob.move_to([PX, y, 0])
        fit_width(mob, PMW - 0.3)
        box = SurroundingRectangle(mob, color=color, buff=0.16, stroke_width=4)
        self.play(Write(mob), Create(box))
        return VGroup(mob, box)


# ======================================================================
class FXC1_ReservoirSizing(ExamScene):
    """page 4: V = 3Q. 10 gpm -> 30 gal -> 113.6 L ; SI 40 L/min -> 0.12 m3."""

    def construct(self):
        self.head("ขนาดถังน้ำมัน (Reservoir sizing)", "W06 · hydraulic06 หน้า 4")
        tx, tb, tw, th = -3.6, -1.9, 3.2, 2.6
        tank = Rectangle(width=tw, height=th, color=METAL, stroke_width=5).move_to(
            [tx, tb + th / 2, 0])
        LH = 0.7
        layers = VGroup(*[
            Rectangle(width=tw - 0.12, height=LH - 0.04, stroke_width=0,
                      fill_color=LIVE, fill_opacity=op).move_to(
                [tx, tb + 0.04 + LH * (i + 0.5), 0])
            for i, op in enumerate([0.55, 0.42, 0.30])])
        lay_lb = VGroup(*[
            T("1 นาทีของปั๊ม", 18, WHITE).move_to(layers[i]) for i in range(3)])
        pc = np.array([-0.9, -1.5, 0])
        pump = Circle(radius=0.38, color=CURRENT, stroke_width=4, fill_color=CURRENT,
                      fill_opacity=0.25).move_to(pc)
        pump_lb = T("ปั๊ม", 20, CURRENT).move_to(pc + 0.62 * DOWN)
        suction = pipe([(tx + 1.1, tb + 0.4), (pc[0] - 0.38, tb + 0.4)], LIVE, 5)
        deliv = pipe([(pc[0], pc[1] + 0.38), (pc[0], 1.1), (0.5, 1.1)], LIVE, 5)
        deliv_tip = Arrow([0.3, 1.1, 0], [1.1, 1.1, 0], buff=0, color=LIVE,
                          stroke_width=5, max_tip_length_to_length_ratio=0.3)
        sys_lb = T("ไประบบ", 20, GRAYTXT).move_to([0.5, 1.45, 0])
        ret = Arrow([-4.7, 1.75, 0], [-4.7, 0.8, 0], buff=0, color=LIVE,
                    stroke_width=5, max_tip_length_to_length_ratio=0.25)
        ret_lb = T("น้ำมันกลับถัง", 20, GRAYTXT).move_to([-4.7, 2.05, 0])
        q_lb = T("Q = 10 gpm", 22, CURRENT).move_to([0.35, -0.55, 0])
        q_ar = arr((0.1, -0.75), (pc[0] + 0.3, pc[1] + 0.3), CURRENT)
        v_dim = dim((tx - tw / 2 - 0.3, tb), (tx - tw / 2 - 0.3, tb + 3 * LH), YEL)
        v_lb = T("V = ?", 22, YEL).move_to([tx - tw / 2 - 0.85, tb + 1.5 * LH + 0.0, 0])
        v_lb.rotate(PI / 2)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(tank), run_time=1.0)
        self.play(FadeIn(pump, pump_lb), Create(suction), Create(deliv),
                  GrowArrow(deliv_tip), FadeIn(sys_lb), run_time=1.2)
        self.play(GrowArrow(ret), FadeIn(ret_lb))
        self.cap("ปั๊มดูดน้ำมันจากถัง ส่งไประบบ แล้วน้ำมันไหลกลับถัง")
        self.play(FadeIn(q_lb), GrowArrow(q_ar))
        self.cap("โจทย์: ปั๊มจ่าย Q = 10 gpm (แกลลอนต่อนาที)")
        self.play(GrowFromCenter(v_dim), FadeIn(v_lb))
        self.cap("ถาม: ถังต้องจุ V เท่าไร? ตอบเป็น gal และลิตร (L)", color=YEL)
        g1 = self.rows([T("ให้: Q = 10 gpm", 26, CURRENT),
                        T("หา: V (gal) และ V (L)", 26, YEL)], PX, 1.6, 0.7, PMW)
        self.show_rows(g1, 0.6)

        # ---------------- step 2
        self.step(2, "สูตร")
        self.play(FadeOut(g1))
        e1 = M(r"V_{tank}", r"=", r"3", r"\times", r"Q_{pump}", size=44)
        e1[0].set_color(YEL); e1[2].set_color(OK); e1[4].set_color(CURRENT)
        e2 = M(r"[\text{gal}] = 3\times[\text{gpm}]", size=32, color=GRAYTXT)
        e3 = M(r"[\text{m}^3] = 3\times[\text{m}^3/\text{min}]", size=32, color=GRAYTXT)
        panel = self.rows([e1, e2, e3], PX, 1.6, 0.95, PMW)
        self.play(FadeIn(e1))
        self.cap("กฎหัวแม่มือบนสไลด์: ถังจุอย่างน้อย 3 เท่าของอัตราไหลปั๊ม (ต่อนาที)")
        self.glow(e1[0], tank, YEL)
        self.glow(e1[4], q_lb, CURRENT)
        self.cap("ทำไมเลข 3? แบ่งถังเป็นชั้น ชั้นละ = น้ำมันที่ปั๊มดูดใน 1 นาที", wait=1.5)
        for i in range(3):
            self.play(FadeIn(layers[i], shift=0.2 * UP), FadeIn(lay_lb[i]), run_time=0.8)
        self.glow(e1[2], layers, OK)
        self.cap("3 ชั้น → น้ำมันได้พักในถังเฉลี่ยราว 3 นาทีก่อนถูกดูดกลับ")
        self.cap("พอให้ความร้อนระบาย ฟองอากาศลอย ตะกอนตก (เหตุผลจากหน้า 3)")
        self.play(FadeIn(e2), FadeIn(e3))
        self.cap("ใช้ได้ทั้ง 2 ระบบหน่วย: gal คู่ gpm หรือ m³ คู่ m³/min")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(panel))
        s1 = M(r"V", r"=", r"3\times 10", r"= 30\ \text{gal}", size=40)
        s1[0].set_color(YEL)
        s2 = M(r"1\ \text{gal} = 3.785\ \text{L}", size=34, color=GRAYTXT)
        s3 = M(r"V = 30\times 3.785", r"= 113.6\ \text{L}", size=38)
        g3 = self.rows([s1, s2, s3], PX, 1.6, 1.0, PMW)
        self.play(FadeIn(s1))
        self.glow(s1[2], q_lb, CURRENT)
        self.play(Transform(lay_lb, VGroup(*[
            T("10 gal", 20, WHITE).move_to(layers[i]) for i in range(3)])))
        self.cap("แต่ละชั้น = 10 gal (ปั๊ม 10 gpm × 1 นาที) → 3 ชั้น = 30 gal")
        self.play(FadeIn(s2))
        self.cap("แปลงเป็นลิตร: 1 แกลลอน (US) = 3.785 ลิตร")
        self.play(FadeIn(s3))
        self.glow(s3[1], tank, YEL)
        new_v = T("V = 30 gal", 22, YEL).rotate(PI / 2).move_to(v_lb)
        self.play(Transform(v_lb, new_v))
        ans = M(r"V \ge 30\ \text{gal} \approx 113.6\ \text{L}", size=44, color=WARN)
        self.answer(ans, -1.55)
        self.cap("คำตอบ: ถังอย่างน้อย 30 gal ≈ 113.6 L", color=WARN)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        self.play(FadeOut(g3))
        c1 = T("หน่วย: gpm × นาที = gal ✓", 24, OK)
        c2 = T("SI: 40 L/min = 0.04 m³/min", 24, OK)
        c3 = T("V = 3 × 0.04 = 0.12 m³ = 120 L ✓", 24, OK)
        g4 = self.rows([c1, c2, c3], PX, 1.6, 0.7, PMW)
        self.show_rows(g4, 1.5)
        self.cap("ฉบับ SI ก็ได้สัดส่วนเดียวกัน: ถัง = 3 นาทีของปั๊ม")
        self.cap("กับดัก: หน่วยต้องคู่กัน ถ้าโจทย์ให้ L/min ต้องใช้ L หรือแปลงก่อน",
                 color=YEL, wait=3.5)
        self.cap("และ 3 เท่าคือ 'อย่างน้อย' (กฎหัวแม่มือ) ไม่ใช่ค่าตายตัว",
                 color=YEL, wait=3.0)
        self.wait(1.0)


# ======================================================================
class FXC2_ConductorSize(ExamScene):
    """page 5: A = Q/v, D = sqrt(4A/pi). 0.002 m3/s -> 46.1 mm / 20.4 mm."""

    def construct(self):
        self.head("ความเร็วสูงสุด → ขนาดท่อ", "W06 · hydraulic06 หน้า 5")
        yc = -0.7
        rs, rd = 0.45, 0.199           # drawn half-heights (46.1 : 20.4)
        xs0, xs1 = -5.45, -3.4
        pc = np.array([-2.95, yc, 0])
        xd0, xd1 = -2.5, 0.75
        tank = Rectangle(width=1.3, height=1.9, color=METAL, stroke_width=4).move_to(
            [-6.15, yc - 0.1, 0])
        oil = Rectangle(width=1.2, height=1.4, stroke_width=0, fill_color=LIVE,
                        fill_opacity=0.35).move_to([-6.15, yc - 0.35, 0])
        sp = Rectangle(width=xs1 - xs0, height=2 * rs, color=METAL, stroke_width=3,
                       fill_color=LIVE, fill_opacity=0.15).move_to(
            [(xs0 + xs1) / 2, yc, 0])
        dp = Rectangle(width=xd1 - xd0, height=2 * rd, color=METAL, stroke_width=3,
                       fill_color=LIVE, fill_opacity=0.15).move_to(
            [(xd0 + xd1) / 2, yc, 0])
        pump = Circle(radius=0.45, color=CURRENT, stroke_width=4, fill_color=CURRENT,
                      fill_opacity=0.25).move_to(pc)
        out_tip = Arrow([xd1 - 0.05, yc, 0], [1.25, yc, 0], buff=0, color=LIVE,
                        stroke_width=5, max_tip_length_to_length_ratio=0.4)
        s_lb = VGroup(T("ท่อดูด", 20, WHITE), T("v ≤ 1.2 m/s", 20, LIVE)).arrange(
            DOWN, buff=0.08).move_to([-4.45, 0.3, 0])
        d_lb = VGroup(T("ท่อจ่าย", 20, WHITE), T("v ≤ 6.1 m/s", 20, WARN)).arrange(
            DOWN, buff=0.08).move_to([-0.85, 0.0, 0])
        q_lb = T("Q = 0.002 m³/s", 20, CURRENT).move_to([-2.95, 1.0, 0])
        q_ar = arr((-2.95, 0.82), (-2.95, yc + 0.47), CURRENT, 2)
        ds_dim = dim((-3.75, yc - rs), (-3.75, yc + rs), YEL, tip=0.1)
        dd_dim = dim((0.35, yc - rd), (0.35, yc + rd), YEL, sw=2, tip=0.07)
        DSP, DDP = [-4.45, -1.7, 0], [0.35, -1.6, 0]
        ds_lb = T("Ds = ?", 22, YEL).move_to(DSP)
        dd_lb = T("Dd = ?", 22, YEL).move_to(DDP)
        ds_ar = arr((-4.15, -1.5), (-3.8, yc - rs + 0.05), YEL, 2)
        dd_ar = arr((0.35, -1.42), (0.35, yc - rd - 0.03), YEL, 2)

        tt = ValueTracker(0.0)
        VS, VD = 0.25, 0.25 * 6.1 / 1.2

        def dots():
            g = VGroup()
            L1 = xs1 - xs0 - 0.2
            for k in range(6):
                x = xs0 + 0.1 + ((k * L1 / 6 + VS * tt.get_value()) % L1)
                for dy in (-0.15, 0.15):
                    g.add(Dot([x, yc + dy, 0], radius=0.045, color=LIVE))
            L2 = xd1 - xd0 - 0.2
            for k in range(5):
                x = xd0 + 0.1 + ((k * L2 / 5 + VD * tt.get_value()) % L2)
                g.add(Dot([x, yc, 0], radius=0.045, color=WARN))
            return g
        flow = always_redraw(dots)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(FadeIn(tank, oil), Create(sp), FadeIn(pump), Create(dp),
                  GrowArrow(out_tip), run_time=1.4)
        self.add(flow)
        self.play(FadeIn(q_lb), GrowArrow(q_ar))
        self.cap("ปั๊มจ่าย Q = 0.002 m³/s (= 120 L/min) ผ่านท่อดูดแล้วออกท่อจ่าย")
        self.play(tt.animate.set_value(4), FadeIn(s_lb), FadeIn(d_lb), run_time=4,
                  rate_func=linear)
        self.cap("ความเร็วสูงสุดที่แนะนำ: ท่อดูด 4 ft/s, ท่อจ่าย 20 ft/s", wait=1.0)
        g1 = self.rows([M(r"4\ \text{ft/s}\times0.3048 = 1.22 \approx 1.2\ \text{m/s}",
                          size=30, color=LIVE),
                        M(r"20\ \text{ft/s}\times0.3048 = 6.10 \approx 6.1\ \text{m/s}",
                          size=30, color=WARN)], PX, 1.6, 0.8, PMW)
        self.show_rows(g1, 0.8)
        self.play(tt.animate.set_value(8), run_time=4, rate_func=linear)
        self.cap("ท่อดูดต้องช้า: ความดันขาดูดต่ำอยู่แล้ว ไหลเร็ว → cavitation")
        self.play(GrowFromCenter(ds_dim), GrowFromCenter(dd_dim),
                  FadeIn(ds_lb, dd_lb), GrowArrow(ds_ar), GrowArrow(dd_ar))
        self.cap("ถาม: เส้นผ่านศูนย์กลางใน (ID) ขั้นต่ำ Ds และ Dd เท่าไร?", color=YEL)

        # ---------------- step 2
        self.step(2, "สูตร")
        self.play(FadeOut(g1))
        e1 = M(r"Q", r"=", r"A", r"\,", r"v", size=46)
        e1[0].set_color(CURRENT); e1[2].set_color(YEL); e1[4].set_color(LIVE)
        e2 = M(r"A", r"=", r"\frac{Q}{v_{max}}", size=40)
        e3 = M(r"D", r"=", r"\sqrt{\frac{4A}{\pi}}", size=40)
        e3[0].set_color(YEL)
        panel = self.rows([e1, e2, e3], PX, 1.7, 1.1, PMW)
        self.play(FadeIn(e1))
        self.cap("อัตราไหล = พื้นที่หน้าตัด × ความเร็ว (น้ำมันเท่าเดิมทั้งเส้น)")
        self.glow(e1[0], q_lb, CURRENT)
        self.glow(e1[2], VGroup(ds_dim, dd_dim), YEL)
        self.play(tt.animate.set_value(11), run_time=2.5, rate_func=linear)
        self.glow(e1[4], VGroup(s_lb[1], d_lb[1]), LIVE)
        self.play(FadeIn(e2))
        self.cap("Q เท่ากัน แต่ v ต่างกัน → ท่อที่ต้องช้ากว่าต้องใหญ่กว่า")
        self.play(FadeIn(e3))
        self.cap("ได้ A แล้วแปลงเป็น D จาก A = πD²/4 → D = √(4A/π)")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(panel))
        s1 = M(r"A_s = \frac{0.002}{1.2}", r"= 1.667\times10^{-3}\ \text{m}^2", size=32)
        s2 = M(r"D_s = \sqrt{\frac{4(1.667\times10^{-3})}{\pi}}", r"= 46.1\ \text{mm}",
               size=32)
        s3 = M(r"A_d = \frac{0.002}{6.1}", r"= 3.279\times10^{-4}\ \text{m}^2", size=32)
        s4 = M(r"D_d = \sqrt{\frac{4(3.279\times10^{-4})}{\pi}}", r"= 20.4\ \text{mm}",
               size=32)
        s2[1].set_color(YEL); s4[1].set_color(YEL)
        g3 = self.rows([s1, s2, s3, s4], PX, 1.75, 1.1, PMW)
        self.cap("ท่อดูด: ใช้ v = 1.2 m/s", color=LIVE, wait=0.8)
        self.play(FadeIn(s1)); self.glow(s1[0], s_lb[1], LIVE)
        self.play(FadeIn(s2)); self.glow(s2[1], ds_dim, YEL)
        self.play(Transform(ds_lb, T("Ds = 46.1 mm", 22, YEL).move_to(DSP)))
        self.cap("ท่อจ่าย: ใช้ v = 6.1 m/s", color=WARN, wait=0.8)
        self.play(FadeIn(s3)); self.glow(s3[0], d_lb[1], WARN)
        self.play(FadeIn(s4)); self.glow(s4[1], dd_dim, YEL)
        self.play(Transform(dd_lb, T("Dd = 20.4 mm", 22, YEL).move_to(DDP)))
        self.cap("ระวัง m → mm: 0.0461 m = 46.1 mm , 0.0204 m = 20.4 mm", wait=2.0)
        self.play(FadeOut(g3))
        ans = VGroup(M(r"D_s \ge 46.1\ \text{mm}", size=42, color=WARN),
                     M(r"D_d \ge 20.4\ \text{mm}", size=42, color=WARN)).arrange(
            DOWN, buff=0.3)
        self.answer(ans, 1.3)
        self.cap("คำตอบ: ID ท่อดูด ≥ 46.1 mm , ID ท่อจ่าย ≥ 20.4 mm", color=WARN)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        cs = Circle(radius=0.85, color=LIVE, stroke_width=4, fill_color=LIVE,
                    fill_opacity=0.2).move_to([-4.3, -3.0, 0])
        cd = Circle(radius=0.376, color=WARN, stroke_width=4, fill_color=WARN,
                    fill_opacity=0.2).move_to([-1.6, -3.0, 0])
        cs_lb = T("46.1", 20, WHITE).move_to(cs)
        cd_lb = T("20.4 mm", 20, WHITE).next_to(cd, RIGHT, buff=0.15)
        self.play(FadeIn(cs, cd, cs_lb, cd_lb))
        self.cap("หน้าตัดจริงตามสัดส่วน: ท่อดูดใหญ่กว่าชัดเจน", wait=1.5)
        c1 = M(r"\frac{D_s}{D_d} = \frac{46.1}{20.4} = 2.26", size=34, color=OK)
        c2 = M(r"\sqrt{\frac{6.1}{1.2}} = 2.25\ \checkmark", size=34, color=OK)
        g4 = self.rows([c1, c2], PX, -0.6, 1.05, PMW)
        self.show_rows(g4, 1.0)
        self.cap("ช้ากว่า 5 เท่า → พื้นที่ใหญ่ 5 เท่า → D ใหญ่ √5 ≈ 2.25 เท่า ✓")
        self.cap("เลือกท่อจริงที่ ID ใหญ่กว่าหรือเท่ากับค่าที่คำนวณ")
        self.cap("กับดัก: สลับ 4 กับ 20 ft/s = ผิดทั้งข้อ / ห้ามเลือกท่อเล็กกว่าค่าที่ได้",
                 color=YEL, wait=3.5)
        self.play(tt.animate.set_value(15), run_time=3, rate_func=linear)


# ======================================================================
class FXC3_PressureRating(ExamScene):
    """page 6: Di 0.870, BP = 2tS/Di = 8,218 psi, FS 6, WP = 1,370 psi."""

    def construct(self):
        self.head("ความดันแตก / ความดันใช้งาน (BP, WP, FS)",
                  "W06 · hydraulic06 หน้า 6")
        rc = np.array([-4.6, -0.3, 0])
        RO, RI = 1.25, 1.0
        tube = ring(rc, RO, RI)
        do_dim = dim((rc[0] - RO, -1.85), (rc[0] + RO, -1.85), GRAYTXT)
        do_lb = T("Do = 1 in", 22, GRAYTXT).move_to([rc[0], -2.2, 0])
        di_dim = dim((rc[0] - RI, rc[1]), (rc[0] + RI, rc[1]), YEL)
        di_lb = T("Di = ?", 22, YEL).move_to([rc[0], rc[1] + 0.35, 0])
        wp45 = rc + (RO + RI) / 2 * np.array([np.cos(PI / 4), np.sin(PI / 4), 0])
        t_lb = T("t = 0.065 in", 22, LIVE).move_to([-2.45, 1.4, 0])
        t_ar = arr((-2.9, 1.2), wp45[:2], LIVE)
        wp135 = rc + (RO + RI) / 2 * np.array([np.cos(3 * PI / 4), np.sin(3 * PI / 4), 0])
        s_lb = T("S = 55,000 psi", 22, METAL).move_to([-5.95, 1.6, 0])
        s_ar = arr((-5.75, 1.38), wp135[:2], METAL)

        # half-tube free body
        hc = np.array([-0.55, -1.35, 0])
        half = AnnularSector(inner_radius=RI, outer_radius=RO, angle=PI, start_angle=0,
                             color=METAL, fill_opacity=1, stroke_width=0).move_arc_center_to(hc)
        cut = DashedLine(hc + RI * LEFT, hc + RI * RIGHT, color=GRAYTXT)
        p_ars = VGroup(*[Arrow(hc + [x, 0.05, 0], hc + [x, 0.6, 0], buff=0,
                               color=FORCE, stroke_width=3,
                               max_tip_length_to_length_ratio=0.25)
                         for x in (-0.7, -0.35, 0, 0.35, 0.7)])
        f_lb = T("F = P · Di · L", 22, FORCE).move_to([hc[0], 0.35, 0])
        wl = hc + (RO + RI) / 2 * LEFT
        wr = hc + (RO + RI) / 2 * RIGHT
        fl = Arrow(wl, wl + 0.75 * DOWN, buff=0, color=OK, stroke_width=4,
                   max_tip_length_to_length_ratio=0.25)
        fr = Arrow(wr, wr + 0.75 * DOWN, buff=0, color=OK, stroke_width=4,
                   max_tip_length_to_length_ratio=0.25)
        fl_lb = T("F/2", 22, OK).next_to(fl, DOWN, buff=0.08)
        fr_lb = T("F/2", 22, OK).next_to(fr, DOWN, buff=0.08)
        fbd = VGroup(half, cut, p_ars, f_lb, fl, fr, fl_lb, fr_lb)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(FadeIn(tube), run_time=1.0)
        self.cap("หน้าตัด tube เหล็ก (วาดผนังหนากว่าจริงให้เห็นชัด)", wait=1.5)
        self.play(GrowFromCenter(do_dim), FadeIn(do_lb))
        self.play(GrowArrow(t_ar), FadeIn(t_lb))
        self.play(GrowArrow(s_ar), FadeIn(s_lb))
        self.cap("ให้: OD 1 in, หนา t = 0.065 in, วัสดุ S = 55,000 psi")
        g1 = self.rows([T("ให้: Do = 1 in , t = 0.065 in", 24, WHITE),
                        T("S = 55,000 psi", 24, METAL),
                        T("ถาม: ใช้ที่ 1,200 psi ได้ไหม?", 26, YEL)], PX, 1.7, 0.7, PMW)
        self.show_rows(g1, 0.8)
        self.play(GrowFromCenter(di_dim), FadeIn(di_lb))
        self.cap("สูตรใช้เส้นผ่านศูนย์กลาง 'ใน' Di ซึ่งโจทย์ไม่ได้ให้ตรงๆ", color=YEL)

        # ---------------- step 2
        self.step(2, "สูตร")
        self.play(FadeOut(g1))
        self.play(FadeIn(half), Create(cut))
        self.cap("ผ่าท่อครึ่งตามยาว (ยาว L) ดูแรงที่กระทำกับครึ่งบน", wait=1.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in p_ars], lag_ratio=0.15),
                  FadeIn(f_lb))
        self.cap("ความดันดันครึ่งท่อขึ้น: F = P × พื้นที่ฉาย = P · Di · L")
        self.play(GrowArrow(fl), GrowArrow(fr), FadeIn(fl_lb, fr_lb))
        self.cap("ผนัง 2 ข้างดึงไว้ ข้างละ F/2 เนื้อโลหะรวม 2 · t · L")
        e1 = M(r"\sigma", r"=", r"\frac{F}{2tL}", r"=", r"\frac{P D_i}{2t}", size=40)
        e1[2].set_color(OK)
        e2 = M(r"\sigma = S", r"\;\Rightarrow\;", r"BP = \frac{2tS}{D_i}", size=38)
        e2[2].set_color(WARN)
        e3 = M(r"WP", r"=", r"\frac{BP}{FS}", size=40)
        tb = VGroup(T("0–1000 psi → FS = 8", 22, GRAYTXT),
                    T("1000–2500 psi → FS = 6", 22, GRAYTXT),
                    T("> 2500 psi → FS = 4", 22, GRAYTXT))
        panel = self.rows([e1, e2, e3], PX, 1.75, 1.05, PMW)
        self.rows(list(tb), PX, -1.25, 0.48, PMW)
        self.play(FadeIn(e1))
        self.glow(e1[2], VGroup(fl, fr), OK)
        self.glow(e1[4], di_dim, YEL)
        self.cap("ความเค้นในผนัง σ = แรง ÷ เนื้อโลหะ = P·Di / (2t)")
        self.play(FadeIn(e2))
        self.glow(e2[2], VGroup(t_lb, s_lb), WARN)
        self.cap("ท่อแตกเมื่อ σ = S → ได้ความดันแตก BP = 2tS / Di")
        self.play(FadeIn(e3))
        self.cap("ใช้งานจริงต้องหารด้วยค่าความปลอดภัย FS: WP = BP / FS")
        self.show_rows(tb, 0.5)
        self.cap("เลือก FS จากความดันใช้งาน: ยิ่งความดันต่ำ FS ยิ่งสูง (กันแรงกระแทก)")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(panel), FadeOut(tb), FadeOut(fbd))
        s1 = M(r"D_i = D_o - 2t = 1 - 2(0.065)", r"= 0.870\ \text{in}", size=32)
        s1[1].set_color(YEL)
        s2 = M(r"BP = \frac{2(0.065)(55{,}000)}{0.870}", r"= 8{,}218\ \text{psi}", size=32)
        s2[1].set_color(WARN)
        s3 = T("1,200 psi อยู่ช่วง 1000–2500 → FS = 6", 24, WHITE)
        s4 = M(r"WP = \frac{8{,}218}{6}", r"= 1{,}370\ \text{psi}", size=34)
        s4[1].set_color(OK)
        g3 = self.rows([s1, s2, s3, s4], PX, 1.75, 1.05, PMW)
        self.play(FadeIn(s1)); self.glow(s1[0], VGroup(do_dim, t_ar), YEL)
        self.play(Transform(di_lb, T("Di = 0.870 in", 22, YEL).move_to(di_lb)))
        self.cap("Di = 1 − 2(0.065) = 0.870 in (ตรงกับตาราง tube หน้า 10)")
        self.play(FadeIn(s2)); self.glow(s2[0], VGroup(t_lb, s_lb, di_lb), WARN)
        self.cap("ความดันที่ทำให้ท่อแตก BP = 8,218 psi")
        self.play(FadeIn(s3))
        self.cap("ระบบใช้ 1,200 psi → อยู่ช่วง 1000–2500 psi → FS = 6")
        self.play(FadeIn(s4)); self.glow(s4[1], tube, OK)
        self.cap("ความดันใช้งานที่ปลอดภัย WP = 8,218 / 6 = 1,370 psi")
        self.play(FadeOut(g3))
        ans = VGroup(M(r"BP = 8{,}218\ \text{psi}", size=38, color=WARN),
                     M(r"WP = 1{,}370\ \text{psi} \ge 1{,}200", size=38, color=WARN),
                     T("→ ใช้ได้", 30, WARN)).arrange(DOWN, buff=0.25)
        self.answer(ans, 1.0)
        self.cap("คำตอบ: WP = 1,370 psi ≥ 1,200 psi → ใช้ tube นี้ได้", color=WARN)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = T("1,370 ≥ 1,200 psi → ใช้ได้ ✓", 24, OK)
        c2 = T("Di = 0.870 in ตรงตารางหน้า 10 ✓", 24, OK)
        g4 = self.rows([c1, c2], PX, -1.35, 0.6, PMW)
        self.show_rows(g4, 1.2)
        wrong = M(r"\frac{2(0.065)(55{,}000)}{1} = 7{,}150", size=32, color=FORCE)
        wrong.move_to([PX, -2.75, 0])
        fit_width(wrong, PMW)
        x_mark = Cross(wrong, stroke_color=FORCE, stroke_width=5)
        self.play(FadeIn(wrong))
        self.play(Create(x_mark))
        self.cap("กับดัก: ใช้ Do = 1 in แทน Di → BP = 7,150 psi ผิด ต้องใช้ Di เสมอ",
                 color=YEL, wait=3.5)
        self.cap("และเลือก FS จากความดันระบบ แล้วเทียบ WP ≥ ความดันระบบ", color=YEL,
                 wait=3.0)
        self.wait(1.0)


# ======================================================================
class FXC4_PipeTableBP(ExamScene):
    """pages 7+10: 1 in pipe, OD 1.315; sched 40 ID 1.049 t 0.133 BP~13,950;
    sched 80 ID 0.957 t 0.179 BP~20,580 (S = 55,000 psi assumed, not on slide)."""

    def construct(self):
        self.head("ตาราง pipe → t → BP (Sch 40 vs 80)",
                  "W06 · หน้า 7+10")
        cols = [-6.3, -4.65, -2.85, -1.0]
        hdr = ["Nominal", "OD", "ID Sch40", "ID Sch80"]
        data = [["1/2", "0.840", "0.622", "0.546"],
                ["3/4", "1.050", "0.824", "0.742"],
                ["1", "1.315", "1.049", "0.957"],
                ["1-1/4", "1.660", "1.380", "1.278"]]
        y0, rh = 1.9, 0.55
        head_row = VGroup(*[T(h, 23, OK).move_to([cols[i], y0, 0])
                            for i, h in enumerate(hdr)])
        cells = [VGroup(*[T(v, 25, WHITE).move_to([cols[i], y0 - (r + 1) * rh, 0])
                          for i, v in enumerate(row)]) for r, row in enumerate(data)]
        grid = VGroup(
            Line([-7.0, y0 - rh / 2, 0], [-0.25, y0 - rh / 2, 0], color=GRAYTXT,
                 stroke_width=2),
            Line([-5.5, y0 + rh / 2, 0], [-5.5, y0 - 4.5 * rh, 0], color=GRAYTXT,
                 stroke_width=2),
            Line([-3.8, y0 + rh / 2, 0], [-3.8, y0 - 4.5 * rh, 0], color=GRAYTXT,
                 stroke_width=2))
        table = VGroup(head_row, *cells, grid)
        row1 = cells[2]
        hl = SurroundingRectangle(row1, color=YEL, buff=0.08, stroke_width=3)

        RO = 0.85
        c40 = np.array([-4.7, -2.45, 0])
        c80 = np.array([-2.5, -2.45, 0])
        r40 = ring(c40, RO, RO * 1.049 / 1.315)
        r80 = ring(c80, RO, RO * 0.957 / 1.315)
        l40 = T("Sch 40", 24, LIVE).move_to(c40 + [-1.6, 0, 0])
        l80 = T("Sch 80", 24, WARN).move_to(c80 + [1.6, 0, 0])
        do40 = VGroup(dim(c40 + [-RO, RO + 0.17, 0], c40 + [RO, RO + 0.17, 0], GRAYTXT,
                          sw=2, tip=0.1),
                      dim(c80 + [-RO, RO + 0.17, 0], c80 + [RO, RO + 0.17, 0], GRAYTXT,
                          sw=2, tip=0.1))
        do_lb = T("OD 1.315 เท่ากัน", 20, GRAYTXT).move_to([-3.6, -1.08, 0])
        t40_lb = T("t40 = ?", 22, LIVE).move_to(c40 + [0, -1.25, 0])
        t80_lb = T("t80 = ?", 22, WARN).move_to(c80 + [0, -1.25, 0])
        t40_ar = arr((c40[0], c40[1] - 1.07), (c40[0], c40[1] - RO * 0.88), LIVE, 2)
        t80_ar = arr((c80[0], c80[1] - 1.07), (c80[0], c80[1] - RO * 0.86), WARN, 2)

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(FadeIn(table), run_time=1.2)
        self.cap("ตารางท่อเหล็ก pipe (หน้า 7) — ตัดมา 4 แถว หน่วยนิ้ว")
        g1 = self.rows([T("ท่อ pipe ขนาด 1 in", 26, WHITE),
                        T("Schedule 40 กับ 80", 26, WHITE),
                        T("หา t และ BP ของแต่ละแบบ", 26, YEL),
                        T("สมมติ S = 55,000 psi (ไม่ได้อยู่บนสไลด์)", 22, GRAYTXT)],
                       PX, 1.75, 0.7, PMW)
        self.show_rows(g1, 0.6)
        self.cap("โจทย์: pipe 1 in แบบ Sch 40 กับ Sch 80 หนาเท่าไร ทนได้เท่าไร", color=YEL)
        self.play(FadeIn(r40, r80, l40, l80))
        self.cap("Schedule สูงขึ้น = ผนังหนาขึ้นไปทางด้านใน รูเล็กลง")
        self.play(GrowFromCenter(do40), FadeIn(do_lb))
        self.cap("ขนาดเดียวกัน OD เท่ากันเสมอ (ใช้เกลียว/ข้อต่อเดียวกัน)")
        self.play(FadeIn(t40_lb, t80_lb), GrowArrow(t40_ar), GrowArrow(t80_ar))

        # ---------------- step 2
        self.step(2, "สูตร")
        self.play(FadeOut(g1))
        e1 = M(r"t", r"=", r"\frac{D_o - D_i}{2}", size=42)
        e1[0].set_color(YEL)
        e2 = M(r"BP", r"=", r"\frac{2tS}{D_i}", size=42)
        e2[0].set_color(WARN)
        panel = self.rows([e1, e2], PX, 1.6, 1.25, PMW)
        self.play(FadeIn(e1))
        self.glow(e1[2], VGroup(do40, t40_ar), YEL)
        self.cap("ผนังมี 2 ข้าง: OD − ID = 2t → t = (OD − ID) / 2")
        self.play(FadeIn(e2))
        self.cap("แล้วเอา t กับ Di ไปเข้าสูตรความดันแตกของหน้า 6")

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(panel))
        self.play(Create(hl))
        self.cap("เปิดตารางแถว Nominal = 1 → OD 1.315 , ID 1.049 (40) , 0.957 (80)")
        self.glow(row1[1], do40, YEL)
        self.glow(row1[2], r40, LIVE)
        self.glow(row1[3], r80, WARN)
        s1 = M(r"t_{40} = \frac{1.315-1.049}{2}", r"= 0.133\ \text{in}", size=32)
        s2 = M(r"t_{80} = \frac{1.315-0.957}{2}", r"= 0.179\ \text{in}", size=32)
        s3 = M(r"BP_{40} = \frac{2(0.133)(55{,}000)}{1.049}", r"\approx 13{,}950\ \text{psi}",
               size=30)
        s4 = M(r"BP_{80} = \frac{2(0.179)(55{,}000)}{0.957}", r"\approx 20{,}580\ \text{psi}",
               size=30)
        s1[1].set_color(LIVE); s2[1].set_color(WARN)
        s3[1].set_color(LIVE); s4[1].set_color(WARN)
        g3 = self.rows([s1, s2, s3, s4], PX, 1.8, 1.05, PMW)
        self.play(FadeIn(s1)); self.glow(s1[0], VGroup(row1[1], row1[2]), LIVE)
        self.play(Transform(t40_lb, T("t40 = 0.133", 22, LIVE).move_to(t40_lb)))
        self.play(FadeIn(s2)); self.glow(s2[0], VGroup(row1[1], row1[3]), WARN)
        self.play(Transform(t80_lb, T("t80 = 0.179", 22, WARN).move_to(t80_lb)))
        self.cap("Sch 80 หนากว่า: 0.179 in เทียบกับ 0.133 in")
        self.play(FadeIn(s3)); self.glow(s3[1], r40, LIVE)
        self.play(FadeIn(s4)); self.glow(s4[1], r80, WARN)
        self.cap("ระวัง: ตัวหารใช้ ID ของ schedule นั้นๆ (1.049 กับ 0.957)")
        self.play(FadeOut(g3))
        ans = VGroup(M(r"\text{Sch 40: } t = 0.133,\ BP \approx 13{,}950\ \text{psi}",
                       size=34, color=LIVE),
                     M(r"\text{Sch 80: } t = 0.179,\ BP \approx 20{,}580\ \text{psi}",
                       size=34, color=WARN)).arrange(DOWN, buff=0.3)
        self.answer(ans, 1.3)
        self.cap("คำตอบ: Sch 80 ทนความดันได้มากกว่า (หนากว่า รูเล็กกว่า)", color=WARN)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = T("OD เท่ากัน 1.315 → ข้อต่อเดียวกัน ✓", 23, OK)
        c2 = T("หนาขึ้น → BP สูงขึ้น ✓", 23, OK)
        c3 = T("ใช้งานจริง: WP = BP / FS (แบบคลิป FX_11)", 23, GRAYTXT)
        g4 = self.rows([c1, c2, c3], PX, -0.25, 0.6, PMW)
        self.show_rows(g4, 1.2)
        self.cap("เทียบ tube (หน้า 10): บอกขนาดด้วย OD จริง เช่น OD 1 in หนา 0.065")
        tube_n = M(r"\text{tube: } ID = 1 - 2(0.065) = 0.870\ \text{in}", size=30,
                   color=GRAYTXT).move_to([PX, -2.35, 0])
        fit_width(tube_n, PMW)
        self.play(FadeIn(tube_n))
        self.wait(2.0)
        self.cap("กับดัก: pipe '1 นิ้ว' ไม่ใช่ OD หรือ ID = 1 in — OD จริง 1.315 ต้องเปิดตาราง",
                 color=YEL, wait=3.5)
        self.cap("โจทย์เลือกท่อ: ID ต้องพอ (ความเร็ว หน้า 5) และผนังต้องพอ (ความดัน หน้า 6)",
                 color=YEL, wait=3.5)
        self.wait(1.0)
