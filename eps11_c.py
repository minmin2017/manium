"""EPS11 ชุดที่ 3 (worker W2): บทที่ 11 หน้า 40-73 แบบสอนช้า ทีละหน้า — ดูอย่างเดียวก็เข้าใจ
คลิป: P40_Base3ph(40-42) P43_Proof(43-46) P47_WhyChange(47-48) P49_Derive(49) P50_XfmrBase(50-51) P52_YY(52-53)
      P54_YDelta(54-55) P56_Diagrams(56-58) P59_Principles(59-60) P61_Problem(61-64) P65_T1(65-66) P67_T2(67-68)
      P69_Zones(69) P70_Line(70) P71_Motors(71-72) P73_Final(73)
ตัวเลขทุกตัวมาจากสไลด์ PDF บทที่ 11 (ค่าที่คำนวณเสริมเพื่ออธิบายระบุว่า 'คำนวณเอง')  กฎ: MathTex ห้ามมีภาษาไทย / Text ห้าม Delta phi sqrt-glyph
"""
from eps8_lib import *

KM, KT, SLOW = 1.28, 1.18, 1.45


def MX(*parts, font_size=26, **kw):
    return MathTex(*parts, font_size=font_size * KM, **kw)


def _m(tex, color=WHITE, size=26):
    return MX(tex, font_size=size, color=color)


def _two(a, b, gap=0.5):
    return VGroup(a, b).arrange(RIGHT, buff=gap)


def T(txt, size=20, color=WHITE):
    return Text(txt, font_size=size * KT, color=color, line_spacing=0.9)


class B(Board):
    """Board ตัวใหญ่ขึ้น (อ่านง่ายตอนดูอย่างเดียว)"""

    def add(self, num, head, body=None, color=OK, run=0.9, hold=0.4):
        badge = VGroup(Circle(radius=0.25, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.2),
                       Text(str(num), font_size=25, color=color))
        badge[1].move_to(badge[0])
        h = Text(head, font_size=28, color=color)
        top = VGroup(badge, h).arrange(RIGHT, buff=0.18)
        row = VGroup(top)
        if body is not None:
            body.next_to(top, DOWN, buff=0.1).align_to(top, LEFT).shift(RIGHT * 0.45)
            row.add(body)
        row.move_to([0, 0, 0])
        prev_bottom = self.rows[-1].get_bottom()[1] - self.gap if self.rows else self.y
        row.align_to([self.x, 0, 0], LEFT)
        row.shift(UP * (prev_bottom - row.get_top()[1]))
        self.rows.append(row)
        self.sc.mark("step")
        self.sc.play(FadeIn(top, shift=RIGHT * 0.25), run_time=0.5)
        if body is not None:
            self.sc.play(Write(body) if isinstance(body, MathTex) else FadeIn(body), run_time=run)
        if hold:
            self.sc.wait(hold)
        return row


class L(Lesson):
    """Lesson + หน้าสรุป 'ประโยคหลัก + จำแบบนี้' + จังหวะช้าลง (SLOW) + ตัวหนังสือใหญ่"""

    def play(self, *a, **k):
        if "run_time" in k:
            k["run_time"] = k["run_time"] * SLOW
        return super().play(*a, **k)

    def wait(self, *a, **k):
        if a:
            a = (a[0] * SLOW,) + tuple(a[1:])
        elif "duration" in k:
            k["duration"] = k["duration"] * SLOW
        return super().wait(*a, **k)

    def say(self, txt, color=GRAYTXT, hold=0.0, size=26):
        return super().say(txt, color=color, hold=hold, size=size)

    def keep(self, sentence, rule, hold=3.6):
        self.fade_out_all(run_time=0.6)
        self._cap = None
        self.mark("keep")
        h1 = Text("ประโยคหลักของหน้านี้", font_size=20, color=GRAYTXT)
        s = fit_width(Text(sentence, font_size=27, color=WHITE, line_spacing=0.95), 12.0)
        h2 = Text("จำแบบนี้", font_size=26, color=YEL)
        r = fit_width(Text(rule, font_size=29, color=YEL, line_spacing=0.95), 12.0)
        card = VGroup(h1, s, h2, r).arrange(DOWN, buff=0.35).move_to([0, 0.1, 0])
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(hold)


# ------------------------------------------------------------------ ชิ้นส่วนรูป
def ystar(cx, cy, r=1.0, color=WHITE, w=4):
    c = np.array([cx, cy, 0.0])
    pts = [c + r * np.array([np.cos(a), np.sin(a), 0.0]) for a in (PI / 2, 7 * PI / 6, 11 * PI / 6)]
    legs = VGroup(*[Line(c, p, color=color, stroke_width=w) for p in pts])
    ends = VGroup(*[Dot(p, radius=0.07, color=color) for p in pts])
    g = VGroup(legs, ends, Dot(c, radius=0.09, color=color))
    g.pts, g.c, g.leg_top = pts, c, legs[0]
    return g


def delta_tri(cx, cy, r=1.0, color=WHITE, w=4):
    c = np.array([cx, cy, 0.0])
    pts = [c + r * np.array([np.cos(a), np.sin(a), 0.0]) for a in (PI / 2, 7 * PI / 6, 11 * PI / 6)]
    tri = Polygon(*pts, stroke_color=color, stroke_width=w)
    ends = VGroup(*[Dot(p, radius=0.07, color=color) for p in pts])
    g = VGroup(tri, ends)
    g.pts = pts
    return g


def dim(p0, p1, color=YEL):
    return DoubleArrow(np.array([*p0[:2], 0.0]), np.array([*p1[:2], 0.0]), buff=0, color=color, stroke_width=3,
                       tip_length=0.15, max_tip_length_to_length_ratio=0.2)


def xf(cx, cy, color=WHITE):
    a = Circle(radius=0.28, stroke_color=color, stroke_width=3).move_to([cx - 0.17, cy, 0])
    b = Circle(radius=0.28, stroke_color=color, stroke_width=3).move_to([cx + 0.17, cy, 0])
    return VGroup(a, b)


def mach(cx, cy, letter, color):
    c = Circle(radius=0.33, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    t = Text(letter, font_size=22, color=color).move_to(c)
    return VGroup(c, t)


def rbox(cx, cy, name, val, color=WHITE, w=1.25, h=0.72, fs=17):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08).move_to([cx, cy, 0])
    n = Text(name, font_size=fs, color=GRAYTXT).move_to([cx, cy + 0.17, 0])
    v = Text(val, font_size=fs, color=color).move_to([cx, cy - 0.16, 0])
    return VGroup(r, n, v)


def src(cx, cy, label, color):
    c = Circle(radius=0.3, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    t = Text(label, font_size=15, color=color).move_to(c)
    return VGroup(c, t)


def sline(Y=0.9):
    """single-line ของโจทย์หลัก (G - T1 - สายส่ง - T2 - บัส p,r - M1,M2) พิกัดเหมือน eps11_a"""
    d = {}
    d["g"] = mach(-6.1, Y, "G", YEL)
    d["t1"] = xf(-3.9, Y)
    d["t2"] = xf(1.9, Y)
    d["wires"] = VGroup(wire((-5.77, Y), (-4.35, Y)), wire((-3.45, Y), (1.45, Y)), wire((2.35, Y), (3.4, Y)),
                        Line([3.4, Y + 0.8, 0], [3.4, Y - 0.8, 0], color=WHITE, stroke_width=6),
                        wire((3.4, Y + 0.8), (4.27, Y + 0.8)), wire((3.4, Y - 0.8), (4.27, Y - 0.8)))
    d["m1"] = mach(4.6, Y + 0.8, "M", C_S)
    d["m2"] = mach(4.6, Y - 0.8, "M", C_S)
    return d


def zone_bars(Y=-1.3):
    zl = [(-6.5, -4.4, "20 kV", YEL, -5.45), (-3.4, 1.4, "230 kV", OK, -1.0), (2.45, 5.2, "13.8 kV", C_S, 3.8)]
    out = []
    for a, b, s, c, cx in zl:
        out.append((Line([a, Y, 0], [b, Y, 0], color=c, stroke_width=5), Text(s, font_size=28, color=c).move_to([cx, Y - 0.45, 0])))
    return out


# =============================================================== P40  หน้า 40-42
class P40_Base3ph(L):
    """ค่าฐาน 3 เฟส ทีละตัว: V_LN, VA_1phase, I_base, Z_base"""

    def construct(self):
        self.head("ค่าฐาน 3 เฟส ทีละตัว", "หน้า 40–42")
        self.say("ภาพก่อน: ระบบ 3 เฟสต่อ Y มีแรงดัน 2 แบบ — แรงดันสาย V_LL กับแรงดันเฟส V_LN", color=OK)
        fy = ystar(4.4, -0.1, 1.3, METAL)
        pts = fy.pts
        vll = dim([pts[1][0], pts[1][1] - 0.45], [pts[2][0], pts[2][1] - 0.45], YEL)
        lll = _m(r"V_{LL}", YEL, 30).move_to([4.4, pts[1][1] - 0.95, 0])
        lln = _m(r"V_{LN}", C_IL, 30).move_to([3.7, 0.75, 0])
        self.play(Create(fy), run_time=1.0)
        self.play(GrowFromCenter(vll), FadeIn(lll), run_time=0.8)
        self.play(FadeIn(lln), Indicate(fy.leg_top, color=C_IL), run_time=0.8)
        self.wait(1.0)
        bd = B(self, x=-6.6, y=2.0, gap=0.08)
        self.say("เลือกฐานแค่ 2 ตัว: กำลัง 3 เฟส (VA 3 เฟส) กับ แรงดันสาย V_LL", color=YEL)
        r1 = bd.add(1, "เลือกฐาน 2 ตัว", _two(_m(r"VA_{3\phi}", YEL, 30), _m(r"V_{LL}", YEL, 30)), color=YEL, hold=0.6)
        self.glow(r1[1], fig=VGroup(vll, lll), color=YEL)
        self.say("แรงดันเฟส = แรงดันสาย หาร sqrt3  ·  กำลังต่อเฟส = กำลัง 3 เฟส หาร 3", color=C_IL)
        r2 = bd.add(2, "ฐานต่อเฟส", _two(_m(r"V_{LN}=\frac{V_{LL}}{\sqrt{3}}", C_IL, 28), _m(r"VA_{1\phi}=\frac{VA_{3\phi}}{3}", C_IL, 28), 0.4),
                    color=C_IL, hold=0.6)
        self.glow(r2[1][0], fig=VGroup(fy.leg_top, lln), color=C_IL)
        self.say("กระแสฐาน: จาก S = sqrt3 × V × I  ย้ายข้าง", color=C_IA)
        r3 = bd.add(3, "กระแสฐาน", _m(r"I_{b}=\frac{VA_{3\phi}}{\sqrt{3}\,V_{LL}}", C_IA, 32), color=C_IA, hold=0.8)
        self.glow(r3[1], color=C_IA)
        self.say("Z ฐาน: ใช้ค่าต่อเฟส  เลข 3 ตัดกันพอดี เหลือ V_LL กำลังสอง หาร VA 3 เฟส", color=C_E)
        r4 = bd.add(4, "Z ฐาน (ตัวเลข 3 ตัดกัน)",
                    _m(r"Z_{b}=\frac{(V_{LL}/\sqrt{3})^{2}}{VA_{3\phi}/3}=\frac{V_{LL}^{2}}{VA_{3\phi}}", C_E, 28), color=C_E, hold=0.8)
        self.glow(r4[1], color=C_E)
        self.wait(1.5)
        self.keep("หน้า 40–42: ฐาน 3 เฟส = กำลัง 3 เฟส + แรงดันสาย  ที่เหลือคำนวณจากสองตัวนี้",
                  "I_b = VA3เฟส / (sqrt3 × V_LL)      Z_b = V_LL² / VA3เฟส\nV_LN = V_LL / sqrt3      VA1เฟส = VA3เฟส / 3")


# =============================================================== P43  หน้า 43-46
class P43_Proof(L):
    """พิสูจน์ด้วยตัวเลข 60,000 kVA / 230 kV: สาย-สาย กับ ต่อเฟส ได้ p.u. เท่ากัน"""

    def construct(self):
        self.head("พิสูจน์: 3 เฟส กับ ต่อเฟส ได้ p.u. เท่ากัน", "หน้า 43–46")
        self.say("ประโยคหลักหน้า 43: แรงดันที่บอก = แรงดันสาย · กำลังที่บอก = กำลัง 3 เฟส", color=OK)
        XA, XB, XL = -1.0, 4.4, -6.7
        hA = T("แบบ 3 เฟส / สายต่อสาย", 20, YEL).move_to([XA, 1.75, 0])
        hB = T("แบบ 1 เฟส / สายต่อนิวทรัล", 20, C_IL).move_to([XB, 1.75, 0])
        self.play(FadeIn(hA), FadeIn(hB), run_time=0.7)

        def row(y, label, a, b, ca=WHITE, cb=WHITE):
            lb = T(label, 21, GRAYTXT)
            lb.move_to([XL + lb.width / 2, y, 0])
            ma, mb = _m(a, ca, 27).move_to([XA, y, 0]), _m(b, cb, 27).move_to([XB, y, 0])
            self.mark("row")
            self.play(FadeIn(lb), run_time=0.4)
            self.play(Write(ma), run_time=0.9)
            self.play(Write(mb), run_time=0.9)
            return lb, ma, mb

        self.say("หน้า 44: ฐาน 60,000 kVA และ 230 kV  → คิดเป็นต่อเฟส: หาร 3 และ หาร sqrt3", color=YEL)
        row(1.05, "ฐาน", r"60000\,kVA\ ,\ 230\,kV", r"20000\,kVA\ ,\ 132.8\,kV", YEL, YEL)
        ar = Arrow([1.1, 1.05, 0], [2.3, 1.05, 0], buff=0.05, color=GRAYTXT, stroke_width=3, tip_length=0.15)
        ar_t = T("÷3 , ÷sqrt3", 15, GRAYTXT).move_to([1.7, 1.4, 0])
        self.play(GrowArrow(ar), FadeIn(ar_t), run_time=0.8)
        self.say("หน้า 45: แรงดันจริง 115 kV  (สาย)  ต่อเฟสคือ 115 ÷ sqrt3 = 66.4 kV", color=C_IL)
        row(0.35, "ค่าจริง (แรงดัน)", r"115\,kV", r"66.4\,kV")
        _, ma, mb = row(-0.35, "p.u. แรงดัน", r"\frac{115}{230}=0.5", r"\frac{66.4}{132.8}=0.5", OK, OK)
        bx = SurroundingRectangle(VGroup(ma, mb), color=OK, buff=0.15)
        eq = T("เท่ากัน!", 22, OK).move_to([XB + 0.0, -1.3, 0])
        self.play(Create(bx), FadeIn(eq), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(VGroup(bx, eq)), run_time=0.4)
        self.say("หน้า 46: กำลังจริง 15,000 kVA (3 เฟส)  ต่อเฟสคือ 15,000 ÷ 3 = 5,000 kVA", color=C_IA)
        row(-1.05, "ค่าจริง (กำลัง)", r"15000\,kVA", r"5000\,kVA")
        _, mc, md = row(-1.75, "p.u. กำลัง", r"\frac{15000}{60000}=0.25", r"\frac{5000}{20000}=0.25", OK, OK)
        bx2 = SurroundingRectangle(VGroup(mc, md), color=OK, buff=0.15)
        eq2 = T("เท่ากัน!", 22, OK).move_to([XB + 0.0, -2.6, 0])
        self.play(Create(bx2), FadeIn(eq2), run_time=0.8)
        self.wait(2.0)
        self.keep("p.u. ไม่สนว่าคิดแบบ 3 เฟส หรือต่อเฟส — ได้ค่าเดียวกันเสมอ",
                  "ข้อสอบให้แรงดันสาย + กำลัง 3 เฟส  ใช้ตรงๆ ได้เลย\nตัวอย่าง: 115/230 = 0.5   15,000/60,000 = 0.25")


# =============================================================== P47  หน้า 47-48
class P47_WhyChange(L):
    """ทำไม p.u. เปลี่ยนเมื่อเปลี่ยนฐาน: Z จริงเท่าเดิม ตัวหาร (Z ฐาน) เปลี่ยน — ใช้ตัวเลข T1 หน้า 65-66"""

    def construct(self):
        self.head("ทำไมต้องเปลี่ยนฐาน: Z จริงเท่าเดิม แต่ p.u. เปลี่ยน", "หน้า 47–48", size=27)
        self.say("หน้า 47 ในไฟล์ PDF เป็นหน้าว่าง (ไม่มีเนื้อหา) — เนื้อหาต่อที่หน้า 48", color=GRAYTXT)
        self.wait(1.5)
        self.say("หน้า 48: p.u. Z = Z จริง × MVA ฐาน ÷ (kV ฐาน)²  = Z จริง ÷ Z ฐาน", color=OK)
        f = _m(r"Z_{pu}=\frac{Z_{real}}{Z_{b}}\ ,\ \ Z_{b}=\frac{kV_{b}^{2}}{MVA_{b}}", WHITE, 32).move_to([0, 1.5, 0])
        self.play(Write(f), run_time=1.4)
        self.wait(1.0)
        self.play(f.animate.scale(0.75).move_to([2.3, 2.0, 0]), run_time=0.7)
        self.say("ตัวอย่างหม้อแปลง T1 (หน้า 65–66, ฝั่ง 230 kV): X = 10 % บนฐาน 350 MVA", color=YEL)
        x0 = -6.5
        L1 = 6.0
        L2 = 6.0 * (230 ** 2 / 300) / (230 ** 2 / 350)
        zr = 0.1 * L1
        tA = T("ฐาน 350 MVA :  Z ฐาน = 230² / 350 = 151.1 โอห์ม", 21, YEL).move_to([x0 + 3.5, 0.95, 0])
        bA = Rectangle(width=L1, height=0.5, stroke_color=YEL, stroke_width=3).move_to([x0 + L1 / 2, 0.35, 0])
        sA = Rectangle(width=zr, height=0.5, stroke_width=0, fill_color=C_E, fill_opacity=0.9).move_to([x0 + zr / 2, 0.35, 0])
        pA = _m(r"\frac{15.11}{151.1}=0.1", YEL, 28).move_to([3.6, 0.35, 0])
        self.play(FadeIn(tA), Create(bA), run_time=0.9)
        self.play(FadeIn(sA), run_time=0.7)
        zt = T("Z จริง = 0.1 × 151.1 = 15.11 โอห์ม (คำนวณเอง)", 19, C_E).move_to([x0 + 3.4, -0.3, 0])
        self.play(FadeIn(zt), Write(pA), run_time=1.0)
        self.wait(1.2)
        self.say("เปลี่ยนฐานเป็น 300 MVA: Z ฐาน ใหญ่ขึ้น  Z จริงเท่าเดิม → ส่วนที่ได้เล็กลง", color=C_E)
        tB = T("ฐาน 300 MVA :  Z ฐาน = 230² / 300 = 176.3 โอห์ม", 21, OK).move_to([x0 + 3.5, -1.2, 0])
        bB = Rectangle(width=L2, height=0.5, stroke_color=OK, stroke_width=3).move_to([x0 + L2 / 2, -1.8, 0])
        sB = Rectangle(width=zr, height=0.5, stroke_width=0, fill_color=C_E, fill_opacity=0.9).move_to([x0 + zr / 2, -1.8, 0])
        pB = _m(r"\frac{15.11}{176.3}=0.0857", OK, 28).move_to([3.7, -1.8, 0])
        self.play(FadeIn(tB), Create(bB), run_time=0.9)
        self.play(FadeIn(sB), run_time=0.7)
        self.play(Write(pB), run_time=1.0)
        self.play(Indicate(sA, color=WHITE), Indicate(sB, color=WHITE), run_time=1.2)
        note = T("แถบแดง (Z จริง) ยาวเท่ากัน แต่แถบฐานยาวไม่เท่า → p.u. ไม่เท่า", 21, WHITE).move_to([0, -2.85, 0])
        self.play(FadeIn(note), run_time=0.7)
        self.wait(3.0)
        self.keep("ค่า p.u. ผูกกับฐานที่ใช้ — เปลี่ยนฐานเมื่อไหร่ ค่า p.u. ต้องเปลี่ยนตาม",
                  "ฐานเปลี่ยน → ตัวหาร Z ฐาน เปลี่ยน → p.u. เปลี่ยน\nตัวอย่าง: 0.1 (ฐาน 350 MVA) → 0.0857 (ฐาน 300 MVA)")


# =============================================================== P49  หน้า 49 (สอนช้า: ที่มาของสูตร)
class P49_Derive(L):
    """ที่มาสูตรเปลี่ยนฐาน: หารสองสมการ Z ตัดกัน + ตรวจทิศทาง"""

    def construct(self):
        self.head("สูตรเปลี่ยนฐาน มาจากไหน", "หน้า 49")
        self.say("เริ่มจากสูตร p.u. ของค่าเดิม (given) กับค่าใหม่ (new) — Z จริงตัวเดียวกัน", color=OK)
        bd = B(self, x=-6.6, y=2.0, gap=0.1)
        r1 = bd.add(1, "เขียน 2 สมการ",
                    VGroup(_m(r"Z_{given}=\frac{Z\cdot MVA_{given}}{kV_{given}^{2}}", WHITE, 27),
                           _m(r"Z_{new}=\frac{Z\cdot MVA_{new}}{kV_{new}^{2}}", WHITE, 27)).arrange(RIGHT, buff=0.5),
                    color=OK, hold=1.0)
        self.say("เอาสมการใหม่ ÷ สมการเดิม → Z จริง ตัดกันหายไป", color=YEL)
        r2 = bd.add(2, "หารกัน (Z ตัดกัน)",
                    _m(r"\frac{Z_{new}}{Z_{given}}=\frac{MVA_{new}}{MVA_{given}}\cdot\frac{kV_{given}^{2}}{kV_{new}^{2}}", YEL, 29),
                    color=YEL, hold=1.0)
        self.glow(r2[1], color=YEL)
        self.say("ย้าย Z_given ไปคูณ ได้สูตรสุดท้าย (สูตรหน้า 49)", color=OK)
        f = MX(r"Z_{new}", r"=", r"Z_{given}", r"\left(\frac{kV_{given}}{kV_{new}}\right)^{2}",
                    r"\frac{MVA_{new}}{MVA_{given}}", font_size=34)
        f[3].set_color(C_S)
        f[4].set_color(YEL)
        r3 = bd.add(3, "สูตรเปลี่ยนฐาน", f, color=OK, hold=1.0)
        self.say("จำ: kV  กลับด้าน และ ยกกำลังสอง (ให้ given อยู่บน)  ·  MVA  ไม่กลับ (new อยู่บน)", color=OK)
        self.play(Indicate(f[3], color=WHITE), Circumscribe(f[3], color=C_S), run_time=1.2)
        self.play(Indicate(f[4], color=WHITE), Circumscribe(f[4], color=YEL), run_time=1.2)
        self.wait(1.0)
        cd = card(["ตรวจทิศทางด้วยตัวเลขจากตัวอย่างหลัก",
                   ("MVA ฐาน 350 → 300 : คูณ 300/350", YEL),
                   ("  p.u. เล็กลง  (0.1 → 0.0857)", YEL),
                   ("kV ฐาน 13.8 > 13.2 : คูณ (13.2/13.8)²", C_S),
                   ("  = 0.9149  p.u. เล็กลง", C_S)], w=5.3, color=GRAYTXT, size=18)
        cd.move_to([3.9, -3.0, 0])
        cd2 = None
        self.play(FadeIn(cd), run_time=0.8)
        self.wait(3.0)
        self.keep("p.u. ใหม่ = p.u. เดิม × (kV เดิม / kV ใหม่)² × (MVA ใหม่ / MVA เดิม)",
                  "kV: เดิมอยู่บน ใหม่อยู่ล่าง แล้วยกกำลังสอง\nMVA: ใหม่อยู่บน เดิมอยู่ล่าง")


# =============================================================== P50  หน้า 50-51
class P50_XfmrBase(L):
    """ฐานของหม้อแปลง: อ้างอิงด้านแรงสูง/ต่ำ + base MVA = พิกัด + หม้อแปลง 3 เฟส = 1 เฟส 3 ตัว (4 แบบต่อ)"""

    def construct(self):
        self.head("ฐานของหม้อแปลง: เลือก kV ด้านไหน Z ก็อ้างอิงด้านนั้น", "หน้า 50–51", size=27)
        self.say("ภาพก่อน: หม้อแปลงมี 2 ด้าน  ด้านแรงสูง (HV)  กับ ด้านแรงต่ำ (LV)", color=OK)
        cx, cy = 3.9, 0.6
        t = xf(cx, cy)
        wl = wire((1.4, cy), (cx - 0.45, cy))
        wr = wire((cx + 0.45, cy), (6.4, cy))
        hv = T("HV แรงสูง", 22, C_N).move_to([1.9, cy + 0.5, 0])
        lv = T("LV แรงต่ำ", 22, C_S).move_to([5.9, cy + 0.5, 0])
        self.play(Create(VGroup(wl, wr, t)), FadeIn(hv), FadeIn(lv), run_time=1.2)
        self.wait(0.6)
        self.say("หน้า 50: ค่า Z p.u. ขึ้นกับว่าฐาน kV ที่ใช้เป็นด้านแรงสูง หรือด้านแรงต่ำ", color=OK)
        bd = B(self, x=-6.6, y=2.0, gap=0.15)
        r1 = bd.add(1, "ฐาน kV = ด้านแรงสูง", T("→ Z อ้างอิงด้านแรงสูง", 22, C_N), color=C_N, hold=0.3)
        self.play(Indicate(hv, color=C_N, scale_factor=1.3), Circumscribe(wl, color=C_N), run_time=1.2)
        r2 = bd.add(2, "ฐาน kV = ด้านแรงต่ำ", T("→ Z อ้างอิงด้านแรงต่ำ", 22, C_S), color=C_S, hold=0.3)
        self.play(Indicate(lv, color=C_S, scale_factor=1.3), Circumscribe(wr, color=C_S), run_time=1.2)
        r3 = bd.add(3, "ฐาน MVA", T("= พิกัด MVA ของหม้อแปลงตัวนั้น", 22, YEL), color=YEL, hold=0.3)
        self.play(Indicate(t, color=YEL, scale_factor=1.3), run_time=1.2)
        self.wait(2.0)
        # ---- หน้า 51
        self.say("หน้า 51: หม้อแปลง 3 เฟส = หม้อแปลง 1 เฟส 3 ตัว มาต่อกัน", color=OK)
        self.play(FadeOut(VGroup(*bd.rows)), FadeOut(VGroup(t, wl, wr, hv, lv)), run_time=0.7)
        ts = VGroup(*[xf(-4.8, yy) for yy in (1.2, 0.2, -0.8)])
        nm = VGroup(*[T(n, 18, GRAYTXT).move_to([-3.5, yy, 0]) for n, yy in (("เฟส a", 1.2), ("เฟส b", 0.2), ("เฟส c", -0.8))])
        bank = Rectangle(width=2.4, height=1.4, stroke_color=YEL, stroke_width=3, fill_color=YEL, fill_opacity=0.08).move_to([0.2, 0.2, 0])
        bt = T("หม้อแปลง 3 เฟส", 20, YEL).move_to(bank)
        a1 = Arrow([-2.7, 0.2, 0], [-1.05, 0.2, 0], buff=0, color=GRAYTXT, stroke_width=3, tip_length=0.18)
        self.play(FadeIn(ts), FadeIn(nm), run_time=0.8)
        self.play(GrowArrow(a1), FadeIn(bank), FadeIn(bt), run_time=0.9)
        self.say("ต่อได้ 4 แบบ  (ด้านแรงสูง - ด้านแรงต่ำ)", color=YEL)
        opts = VGroup(*[T(s, 28, WHITE) for s in ("1. Y - Y", "2. Y - Delta", "3. Delta - Y", "4. Delta - Delta")]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        opts.move_to([4.7, 0.2, 0])
        for o in opts:
            self.play(FadeIn(o, shift=LEFT * 0.2), run_time=0.5)
        self.wait(1.0)
        pr = T("ต่อไป: กรณี Y-Y (หน้า 52–53)  และ  Y-Delta (หน้า 54–55)", 21, OK).move_to([0, -2.2, 0])
        self.play(FadeIn(pr), run_time=0.6)
        self.wait(2.5)
        self.keep("ฐาน kV เลือกด้านไหน Z ก็อ้างอิงด้านนั้น · ฐาน MVA คือพิกัดของหม้อแปลง",
                  "3 เฟส = 1 เฟส 3 ตัว  ต่อได้ Y-Y / Y-Delta / Delta-Y / Delta-Delta")


# =============================================================== P52  หน้า 52-53
class P52_YY(L):
    """หม้อแปลง 1 เฟส 3 ตัว 25 MVA 39.8/3.98 kV ต่อ Y-Y: 75 MVA, 69/6.9 kV, Z_HV = 60 ohm"""

    def construct(self):
        self.head("หม้อแปลง 3 ตัวต่อ Y-Y: พิกัดรวม + อ้างอิง Z ไปด้านแรงสูง", "หน้า 52–53", size=27)
        self.say("โจทย์หน้า 52: 1 เฟส 3 ตัว ตัวละ 25 MVA , 39.8/3.98 kV ต่อ Y-Y  โหลด Y 0.6 โอห์ม/เฟส", color=OK)
        y1 = ystar(2.4, -0.1, 1.0, C_N)
        y2 = ystar(5.7, -0.1, 1.0, C_S)
        p1, p2 = y1.pts, y2.pts
        h1, h2 = T("HV (แรงสูง)", 18, C_N).move_to([2.4, 1.4, 0]), T("LV (แรงต่ำ)", 18, C_S).move_to([5.7, 1.4, 0])
        ph1 = T("39.8 kV", 18, WHITE).move_to([1.65, 0.45, 0])
        ph2 = T("3.98 kV", 18, WHITE).move_to([4.95, 0.45, 0])
        d1 = dim([p1[1][0], p1[1][1] - 0.4], [p1[2][0], p1[2][1] - 0.4])
        d2 = dim([p2[1][0], p2[1][1] - 0.4], [p2[2][0], p2[2][1] - 0.4])
        l1 = T("69 kV", 20, YEL).move_to([2.4, p1[1][1] - 0.75, 0])
        l2 = T("6.9 kV", 20, YEL).move_to([5.7, p2[1][1] - 0.75, 0])
        ld = T("โหลด Y: 0.6 โอห์ม/เฟส", 18, WARN).move_to([5.7, -2.5, 0])
        self.play(Create(y1), Create(y2), FadeIn(h1), FadeIn(h2), run_time=1.2)
        self.play(FadeIn(ph1), FadeIn(ph2), run_time=0.6)
        self.play(GrowFromCenter(d1), GrowFromCenter(d2), FadeIn(l1), FadeIn(l2), FadeIn(ld), run_time=0.9)
        self.wait(0.8)
        bd = B(self, x=-6.6, y=2.0, gap=0.1)
        self.say("พิกัด 3 เฟส = 3 × 25 = 75 MVA", color=YEL)
        r1 = bd.add(1, "พิกัด 3 เฟส", _m(r"3\times25=75\,MVA", YEL, 30), color=YEL, hold=0.6)
        self.play(Indicate(VGroup(y1, y2), color=YEL, scale_factor=1.05), run_time=1.0)
        self.say("แรงดันสาย = sqrt3 × แรงดันเฟส  (ทั้งสองด้าน)", color=C_IL)
        r2 = bd.add(2, "แรงดันสาย",
                    _m(r"\frac{\sqrt{3}\times39.8}{\sqrt{3}\times3.98}=\frac{69}{6.9}\,kV", C_IL, 28), color=C_IL, hold=0.6)
        self.play(Indicate(VGroup(d1, l1, d2, l2), color=C_IL), run_time=1.0)
        self.wait(1.0)
        self.say("หน้า 53: ต่อโหลดด้านแรงต่ำ แต่คิด Z ต่อเฟสที่ด้านแรงสูงได้ — MVA สองด้านเท่ากัน", color=OK)
        r3 = bd.add(3, "MVA เท่ากันสองด้าน", _m(r"\frac{kV_{LV}^{2}}{Z_{LV}}=\frac{kV_{HV}^{2}}{Z_{HV}}", OK, 30), color=OK, hold=0.6)
        self.say("แก้หา Z_HV แล้วแทนค่า — kV ใช้แรงดันเฟสคู่กัน (39.8 กับ 3.98) หรือแรงดันสาย (69 กับ 6.9) ก็ได้", color=OK)
        f = MX(r"Z_{HV}", r"=", r"0.6", r"\left(\frac{39.8}{3.98}\right)^{2}", r"=", r"0.6", r"\left(\frac{69}{6.9}\right)^{2}",
                    font_size=28)
        r4 = bd.add(4, "Z ที่ด้านแรงสูง", f, color=OK, hold=0.6)
        self.glow(f[3], fig=VGroup(ph1, ph2), color=C_IL)
        self.glow(f[6], fig=VGroup(l1, l2), color=YEL)
        r5 = bd.add(5, "ผล", VGroup(_m(r"0.6\times100=60\,\Omega", OK, 32), T("(10² = 100)", 20, GRAYTXT)).arrange(RIGHT, buff=0.3),
                    color=OK, hold=1.0)
        self.wait(2.5)
        self.keep("Y-Y: อัตราส่วนแรงดันเฟส = อัตราส่วนแรงดันสาย (10 เท่า) → Z ด้านแรงสูง = Z ด้านแรงต่ำ × 10²",
                  "Z_HV = Z_LV × (kV_HV / kV_LV)²\n0.6 × (39.8/3.98)² = 0.6 × 100 = 60 โอห์ม")


# =============================================================== P54  หน้า 54-55
class P54_YDelta(L):
    """Y-Delta: ด้านต่ำเป็น Delta 3.98 kV (สาย=เฟส) Z_HV = 0.6 (69/3.98)^2 = 180 ; ทางที่สอง วาด Y-Y แล้ว 3.98/sqrt3 = 2.3"""

    def construct(self):
        self.head("หม้อแปลงต่อ Y-Delta: อัตราส่วนแรงดันสายเปลี่ยนไป sqrt3 เท่า", "หน้า 54–55", size=27)
        self.say("หน้า 54: ด้านแรงสูงต่อ Y (69 kV สาย, 39.8 kV เฟส)  ด้านแรงต่ำต่อ Delta (3.98 kV)  โหลด Y 0.6 โอห์ม", color=OK)
        y1 = ystar(2.4, 0.0, 1.0, C_N)
        d2 = delta_tri(5.7, 0.0, 1.0, C_S)
        p1, p2 = y1.pts, d2.pts
        h1, h2 = T("HV  Y", 20, C_N).move_to([2.4, 1.45, 0]), T("LV  Delta", 20, C_S).move_to([5.7, 1.45, 0])
        d1 = dim([p1[1][0], p1[1][1] - 0.4], [p1[2][0], p1[2][1] - 0.4])
        dd = dim([p2[1][0], p2[1][1] - 0.4], [p2[2][0], p2[2][1] - 0.4])
        l1 = T("69 kV (สาย)", 18, YEL).move_to([2.4, p1[1][1] - 0.75, 0])
        l2 = T("3.98 kV (สาย)", 18, YEL).move_to([5.7, p2[1][1] - 0.75, 0])
        ph = T("39.8 kV", 18, WHITE).move_to([1.65, 0.45, 0])
        self.play(Create(y1), Create(d2), FadeIn(h1), FadeIn(h2), run_time=1.2)
        self.play(FadeIn(ph), GrowFromCenter(d1), GrowFromCenter(dd), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.wait(0.8)
        bd = B(self, x=-6.6, y=2.0, gap=0.1)
        self.say("Delta: แรงดันบนขดลวด = แรงดันสาย  ดังนั้นด้านต่ำใช้ 3.98 kV (ไม่หาร sqrt3)", color=YEL)
        r1 = bd.add(1, "อัตราส่วนแรงดันสาย", _m(r"\frac{69}{3.98}=17.3", YEL, 30), color=YEL, hold=0.6)
        self.play(Indicate(VGroup(l1, l2), color=YEL), run_time=1.0)
        cmp_ = T("เทียบ Y-Y: 69/6.9 = 10   Y-Delta: 17.3 = 10 × sqrt3", 20, GRAYTXT)
        cmp_.move_to([0.0, -3.4, 0])
        self.play(FadeIn(cmp_), run_time=0.7)
        self.say("แทนในสูตรเดิม  Z ด้านแรงสูง = 0.6 × (69 / 3.98)²", color=OK)
        f = MX(r"Z_{HV}", r"=", r"0.6", r"\left(\frac{69}{3.98}\right)^{2}", font_size=32)
        r2 = bd.add(2, "แทนค่า", f, color=OK, hold=0.6)
        self.glow(f[3], fig=VGroup(l1, l2), color=YEL)
        r3 = bd.add(3, "ผล (สไลด์หน้า 54)", VGroup(_m(r"\approx 180\,\Omega", OK, 34), T("(คำนวณละเอียด 180.3)", 19, GRAYTXT)).arrange(RIGHT, buff=0.3),
                    color=OK, hold=1.2)
        self.wait(1.0)
        # ---- หน้า 55
        self.say("หน้า 55: ถ้าไม่สนมุมเฟสที่เลื่อน เปลี่ยน Delta ให้เป็น Y ได้  แรงดันเฟสด้านต่ำ = 3.98 / sqrt3 = 2.3 kV", color=OK)
        self.play(FadeOut(VGroup(d2, h2, dd, l2)), run_time=0.5)
        y2 = ystar(5.7, 0.0, 1.0, C_S)
        q = y2.pts
        h2b = T("LV  Y (วาดใหม่)", 20, C_S).move_to([5.7, 1.45, 0])
        ph2 = T("2.3 kV", 18, C_S).move_to([5.05, 0.45, 0])
        self.play(Create(y2), FadeIn(h2b), FadeIn(ph2), run_time=1.0)
        r4 = bd.add(4, "หน้า 55: เทียบทางที่สอง",
                    _m(r"Z_{HV}=0.6\left(\frac{39.8}{2.3}\right)^{2}\approx180\,\Omega", C_IL, 28), color=C_IL, hold=0.6)
        self.play(Indicate(ph, color=WHITE), Indicate(ph2, color=WHITE), run_time=1.0)
        cm = T("ได้ 180 เท่ากันทั้งสองทาง  (179.6 ถึง 180.3 = ปัดเศษ)", 21, OK).move_to([0.0, -2.75, 0])
        self.play(FadeIn(cm), run_time=0.6)
        self.wait(3.0)
        self.keep("Y-Delta: แรงดันสายสองด้านเทียบกันตรงๆ (69 กับ 3.98) — ไม่ใช่ 69 กับ 6.9",
                  "Z_HV = 0.6 × (69 / 3.98)² ≈ 180 โอห์ม\nหรือ 0.6 × (39.8 / 2.3)² ≈ 180  (ได้ค่าเดียวกัน)")


# =============================================================== P56  หน้า 56-58
class P56_Diagrams(L):
    """หน้า 56 หัวข้อ (รวม) · 57 ใช้ reactance diagram วิเคราะห์ลัดวงจร · 58 เปรียบเทียบ 3 แผนภาพของระบบเดียวกัน"""

    def construct(self):
        self.head("แผนภาพรีแอคแตนซ์: ใช้ทำอะไร และหน้าตาเป็นยังไง", "หน้า 56–58", size=27)
        self.say("หน้า 56 เป็นหน้าหัวข้อ (รวมเข้ากับหน้า 57)  →  หน้า 57: ใช้แผนภาพรีแอคแตนซ์เพื่อวิเคราะห์การลัดวงจร", color=OK)
        b1 = card(["ลัดวงจร (Fault) ใช้ แผนภาพรีแอคแตนซ์", ("ถ้าใช้โปรแกรมคอมพิวเตอร์ วิเคราะห์ Fault", GRAYTXT),
                   ("อาจใช้ แผนภาพอิมพีแดนซ์ แทนได้", GRAYTXT)], w=7.0, color=OK, size=22).move_to([0, 0.6, 0])
        self.play(FadeIn(b1), run_time=0.9)
        self.wait(3.0)
        self.play(FadeOut(b1), run_time=0.5)
        self.say("หน้า 58: ระบบเดียวกัน 3 รูป — เส้นเดียว (บน) · อิมพีแดนซ์ (กลาง) · รีแอคแตนซ์ (ล่าง)", color=OK)
        names = ["G1+G2+โหลดA", "T1", "สายส่ง", "T2", "G3+โหลดB"]
        xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
        # แถวบน: single line
        r1y, r2y, r3y = 1.4, -0.15, -1.9

        def strip(y, color, labels):
            bs = VGroup()
            for x, n in zip(xs, labels):
                r = Rectangle(width=2.0, height=0.55, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08).move_to([x, y, 0])
                t = fit_width(Text(n, font_size=16, color=color), 1.85).move_to(r)
                bs.add(VGroup(r, t))
            ws = VGroup(*[Line([xs[i] + 1.0, y, 0], [xs[i + 1] - 1.0, y, 0], color=GRAYTXT, stroke_width=3) for i in range(4)])
            return VGroup(bs, ws)
        s1 = strip(r1y, WHITE, names)
        t1 = T("แผนภาพเส้นเดียว", 19, GRAYTXT).move_to([-5.9, r1y + 0.55, 0])
        self.play(FadeIn(s1), FadeIn(t1), run_time=1.0)
        self.wait(1.5)
        names2 = ["R+X, โหลด, ชันต์", "R+X, ชันต์", "R+X", "R+X, ชันต์", "R+X, โหลด, ชันต์"]
        s2 = strip(r2y, C_IL, names2)
        t2 = T("แผนภาพอิมพีแดนซ์ (ละเอียดสุด)", 19, GRAYTXT).move_to([-4.4, r2y + 0.55, 0])
        self.play(FadeIn(s2), FadeIn(t2), run_time=1.0)
        self.wait(1.5)
        names3 = ["E1,E2 + X", "X", "X", "X", "X + E3"]
        s3 = strip(r3y, YEL, names3)
        t3 = T("แผนภาพรีแอคแตนซ์ (เหลือแค่ X + แหล่งกำเนิด E)", 19, YEL).move_to([-3.2, r3y + 0.55, 0])
        self.play(FadeIn(s3), FadeIn(t3), run_time=1.0)
        self.wait(1.2)
        self.say("ในรูปล่างสุดของสไลด์: เหลือเครื่องกำเนิด E1 E2 E3 ที่มี X อนุกรม  T1  สายส่ง  T2  ต่อนิวทรัลร่วม — ไม่มีโหลด A, B", color=YEL)
        self.play(Indicate(s3, color=YEL, scale_factor=1.03), run_time=1.4)
        self.wait(3.0)
        self.keep("แผนภาพรีแอคแตนซ์ = แผนภาพอิมพีแดนซ์ ที่ตัดทิ้งเหลือแค่ X กับแหล่งกำเนิด E",
                  "เส้นเดียว → อิมพีแดนซ์ → รีแอคแตนซ์  (ใช้วิเคราะห์ลัดวงจร)\n(หน้า 58 ป้ายล่างขวาในสไลด์มีตัวหนังสือซ้อนกัน เป็นข้อบกพร่องของไฟล์)")


# =============================================================== P59  หน้า 59-60
class P59_Principles(L):
    """หลักการคำนวณเขียนแผนภาพรีแอคแตนซ์ 5 ข้อ — แต่ละข้อมีภาพ"""

    def construct(self):
        self.head("หลักคำนวณเขียนรีแอคแตนซ์ 5 ข้อ", "หน้า 59–60")
        self.say("ท่องทีละข้อ  ซ้าย = หลักการ  ขวา = ภาพประกอบ (ใช้เลขจากตัวอย่างหลัก)", color=OK)
        XR = 3.6
        rules = [
            ("1. ฐาน 3 เฟส = แรงดันสาย (V_line)\n    + กำลังรวม 3 เฟส (S)", YEL),
            ("2. อีกด้านของหม้อแปลง: kV ตามอัตราส่วนแรงดันสาย\n    MVA เท่ากันทุกจุด", OK),
            ("3. Z/X ของหม้อแปลง 3 เฟส ปกติบอกเป็น p.u. หรือ %\n    ของพิกัดตัวมันเอง", C_IL),
            ("4. หม้อแปลง 1 เฟส 3 ตัว: S จริง = ผลรวม 3 ตัว\n    Z 3 เฟส = Z 1 เฟส", C_IA),
            ("5. p.u. ที่ฐานไม่ตรงระบบ\n    → เปลี่ยนฐานให้ตรงฐานระบบ", C_E),
        ]
        ys = [1.55, 0.5, -0.55, -1.6, -2.65]
        items = []
        vis = None
        for k, ((txt, col), y) in enumerate(zip(rules, ys)):
            tt = fit_width(T(txt, 21, col), 6.9)
            tt.move_to([-6.9 + tt.width / 2, y, 0])
            self.mark("rule")
            self.play(FadeIn(tt, shift=RIGHT * 0.2), run_time=0.6)
            items.append(tt)
            if vis is not None:
                self.play(FadeOut(vis), run_time=0.3)
            if k == 0:
                vis = VGroup(_m(r"V_{line}", YEL, 38), _m(r"S_{3\phi}", YEL, 38)).arrange(RIGHT, buff=0.8).move_to([XR, 0.4, 0])
            elif k == 1:
                tf = xf(XR, 0.3)
                vis = VGroup(tf, wire((XR - 2.4, 0.3), (XR - 0.45, 0.3)), wire((XR + 0.45, 0.3), (XR + 2.4, 0.3)),
                             T("20 kV", 22, YEL).move_to([XR - 1.6, 0.8, 0]), T("230 kV", 22, OK).move_to([XR + 1.6, 0.8, 0]),
                             T("300 MVA", 20, YEL).move_to([XR - 1.6, -0.3, 0]), T("300 MVA (เท่ากัน)", 20, YEL).move_to([XR + 1.7, -0.3, 0]))
            elif k == 2:
                vis = VGroup(T("T1: X = 10 %", 28, C_IL), T("(ของพิกัดตัวเอง 350 MVA)", 20, GRAYTXT)).arrange(DOWN, buff=0.25).move_to([XR, 0.3, 0])
            elif k == 3:
                tfs = VGroup(*[xf(XR - 1.4, 1.1 - i * 0.75) for i in range(3)])
                vis = VGroup(tfs, T("3 × 100 = 300 MVA", 24, C_IA).move_to([XR + 1.3, 0.5, 0]),
                             T("Z 3 เฟส = Z 1 เฟส", 22, C_IA).move_to([XR + 1.3, -0.3, 0]))
            else:
                vis = _m(r"Z_{new}=Z_{given}\left(\frac{kV_{g}}{kV_{n}}\right)^{2}\frac{MVA_{n}}{MVA_{g}}", C_E, 30).move_to([XR, 0.3, 0])
            self.play(FadeIn(vis), run_time=0.7)
            self.wait(2.0)
        self.wait(1.5)
        self.keep("ฐานทั้งระบบ: กำลังเดียวกันทุกจุด  แรงดันเปลี่ยนตามหม้อแปลง  แล้วเปลี่ยนฐานทุกชิ้นให้ตรง",
                  "1 เลือกฐาน (MVA, kV)   2 หา kV ทุกโซน\n3 เปลี่ยนฐาน X ทุกชิ้น   4 วาด jX")


# =============================================================== P61  หน้า 61-64
class P61_Problem(L):
    """อ่านโจทย์หลักช้าๆ ทีละอุปกรณ์ + แผนการ 4 ข้อ + ฐานที่โจทย์กำหนด"""

    def construct(self):
        self.head("โจทย์หลักของบท: อ่านให้ครบก่อนคำนวณ", "หน้า 61–64")
        self.say("หน้า 61: เครื่องกำเนิด → T1 → สายส่ง 64 km → T2 → มอเตอร์ M1, M2  (จุด k l m n p r)", color=OK)
        d = sline(0.9)
        Y = 0.9
        self.play(Create(d["wires"]), FadeIn(d["g"]), Create(d["t1"]), Create(d["t2"]), FadeIn(d["m1"]), FadeIn(d["m2"]), run_time=1.6)
        nodes = VGroup(*[T(s, 17, GRAYTXT).move_to([x, Y + 0.3, 0]) for s, x in (("k", -5.1), ("l", -3.1), ("m", 1.1), ("n", 2.9))],
                       T("p", 17, GRAYTXT).move_to([3.15, Y + 1.1, 0]), T("r", 17, GRAYTXT).move_to([3.15, Y - 0.5, 0]))
        self.play(FadeIn(nodes), run_time=0.5)
        self.wait(1.0)
        lab = {
            "g": ("G  3 เฟส 300 MVA\n20 kV   Xs = 20 %", YEL, [-5.7, -0.55]),
            "t1": ("T1  3 เฟส 350 MVA\n230/20 kV   X = 10 %", WHITE, [-2.9, -0.55]),
            "t2": ("T2  1 เฟส 3 ตัว ตัวละ 100 MVA\n127/13.2 kV   X = 10 %", WHITE, [1.0, -0.6]),
            "ln": ("สายส่ง 64 km\n0.5 โอห์ม/km", C_IL, [-0.8, 1.45]),
            "m1": ("M1  200 MVA\n13.2 kV  X'' = 20 %", C_S, [6.0, Y + 0.8]),
            "m2": ("M2  100 MVA\n13.2 kV  X'' = 20 %", C_S, [6.0, Y - 0.8]),
        }
        order = [("g", d["g"], "เครื่องกำเนิด: 300 MVA , 20 kV , Xs = 20 %"),
                 ("t1", d["t1"], "T1: หม้อแปลง 3 เฟส ตัวเดียว 350 MVA  230/20 kV  X = 10 %"),
                 ("ln", d["wires"][1], "สายส่ง 64 km  รีแอคแตนซ์ 0.5 โอห์ม ต่อ km (หน้า 63)"),
                 ("t2", d["t2"], "T2: เป็น 1 เฟส 3 ตัว ตัวละ 100 MVA  127/13.2 kV  X = 10 % — สังเกตว่า 127 คือแรงดันเฟส"),
                 ("m1", d["m1"], "M1: 200 MVA 13.2 kV X'' = 20 %   (สายกลางต่อดินผ่านรีแอคแตนซ์)"),
                 ("m2", d["m2"], "M2: 100 MVA 13.2 kV X'' = 20 %   (สายกลางไม่ต่อดิน)")]
        shown = []
        for key, sym, sc in order:
            txt, col, pos = lab[key]
            lb = n_text(txt, size=15 if key in ("m1", "m2") else 16, color=col).move_to([pos[0], pos[1], 0])
            self.say(sc, color=OK if col is WHITE else col)
            self.play(FadeIn(lb), Indicate(sym, color=col, scale_factor=1.25), run_time=1.0)
            self.wait(1.4)
            shown.append(lb)
        self.say("หน้า 63: จงหา แผนภาพรีแอคแตนซ์พร้อมค่า p.u.  โดยใช้ฐาน = พิกัดเครื่องกำเนิด 300 MVA , 20 kV", color=YEL)
        self.wait(1.5)
        self.play(FadeOut(VGroup(*shown)), run_time=0.6)
        self.say("หน้า 64: แผนการ — ต้องหาค่า X 4 กลุ่ม", color=OK)
        plan = VGroup(T("① X เครื่องกำเนิด", 24, YEL), T("② X หม้อแปลง T1 , T2", 24, WHITE),
                      T("③ X สายส่ง", 24, C_IL), T("④ X มอเตอร์ M1 , M2", 24, C_S)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        plan.move_to([-3.4, -2.0, 0])
        base = card(["ฐานที่โจทย์กำหนด", ("300 MVA , 20 kV", YEL)], w=3.6, color=YEL, size=24).move_to([3.4, -2.0, 0])
        for p in plan:
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(base), run_time=0.7)
        self.wait(3.0)
        self.keep("ก่อนคำนวณ: จดฐานระบบ (ฐานเครื่องกำเนิด) แล้วหา kV ทุกโซนก่อน  แล้วค่อยเปลี่ยนฐานทีละชิ้น",
                  "ฐาน = 300 MVA , 20 kV\nต้องหา X ของ G , T1 , T2 , สายส่ง , M1 , M2")


# =============================================================== P65  หน้า 65-66
class P65_T1(L):
    """ขั้น 1-2: ฐานโซน 230 kV จาก T1 + X_T1 = 0.0857 (ทีละตัวเลข)"""

    def construct(self):
        self.head("ขั้น 1–2: ข้าม T1 ไปโซน 230 kV แล้วหา X ของ T1", "หน้า 65–66", size=27)
        self.say("ฐานเริ่มที่ฝั่งเครื่องกำเนิด: 20 kV , 300 MVA  แล้วเดินข้าม T1", color=OK)
        Y = 0.8
        g = mach(1.9, Y, "G", YEL)
        t1 = xf(4.0, Y)
        w1 = wire((2.25, Y), (3.55, Y))
        w2 = wire((4.45, Y), (6.8, Y))
        z1 = Line([1.5, -0.35, 0], [3.4, -0.35, 0], color=YEL, stroke_width=5)
        z2 = Line([4.6, -0.35, 0], [6.8, -0.35, 0], color=OK, stroke_width=5)
        k1 = T("20 kV", 22, YEL).move_to([2.45, -0.8, 0])
        k2 = T("230 kV ?", 22, OK).move_to([5.7, -0.8, 0])
        self.play(FadeIn(g), Create(VGroup(w1, w2, t1)), run_time=1.0)
        self.play(Create(z1), FadeIn(k1), run_time=0.8)
        bd = B(self, x=-6.6, y=2.0, gap=0.06)
        r1 = bd.add(1, "เข้าใจ: ฐานฝั่ง G", T("20 kV , 300 MVA", 22, YEL), color=YEL, hold=0.4)
        self.say("สูตร: kV ฐานอีกด้าน = kV ฐานเดิม × อัตราส่วนแรงดันสายของหม้อแปลง  (230/20)", color=OK)
        f = MX(r"20", r"\times", r"\frac{230}{20}", r"=", r"230\,kV", font_size=32)
        r2 = bd.add(2, "แรงดันฐานอีกด้าน", f, color=OK, hold=0.4)
        self.play(Create(z2), FadeIn(k2), run_time=0.8)
        self.glow(f[4], fig=VGroup(z2, k2), color=OK)
        self.say("กำลังฐาน 300 MVA เท่าเดิม แต่พิกัด T1 = 350 MVA ไม่เท่า → ต้องเปลี่ยนฐาน X", color=YEL)
        r3 = bd.add(3, "เช็คกำลัง", T("ฐาน 300  ≠  พิกัด T1 350  → เปลี่ยนฐาน", 21, YEL), color=YEL, hold=0.6)
        self.say("หน้า 66: X ใหม่ = X เดิม × (kV เดิม / kV ใหม่)² × (MVA ใหม่ / MVA เดิม)", color=OK)
        g2 = MX(r"0.1", r"\times", r"\left(\frac{230}{230}\right)^{2}", r"\times", r"\frac{300}{350}", font_size=32)
        r4 = bd.add(4, "แทนค่า", g2, color=OK, hold=0.5)
        self.glow(g2[0], fig=t1, color=WHITE)
        self.glow(g2[2], fig=VGroup(k2), color=OK)
        self.glow(g2[4], color=YEL)
        r5 = bd.add(5, "ผล", VGroup(_m(r"X_{T1}=0.0857\,p.u.", OK, 34), T("= 8.57 %", 22, GRAYTXT)).arrange(RIGHT, buff=0.3), color=OK, hold=0.5)
        self.say("ตรวจ: ฐาน MVA เล็กลง (350 → 300) ค่า p.u. ต้องเล็กลง  0.1 → 0.0857 ✓", color=C_IL)
        self.wait(3.5)
        self.keep("ข้าม T1: kV ฐานคูณอัตราส่วนสาย (20 → 230) · กำลังฐานไม่เปลี่ยน",
                  "X_T1 = 0.1 × (230/230)² × (300/350) = 0.0857 p.u.")


# =============================================================== P67  หน้า 67-68
class P67_T2(L):
    """ขั้น 3-4: T2 เป็น 1 เฟส 3 ตัว (Y-Delta) แรงดันสาย 220/13.2 → ฐาน 13.8 kV → X_T2 = 0.0915"""

    def construct(self):
        self.head("ขั้น 3–4: T2 (1 เฟส 3 ตัว Y-Delta) ฐาน 13.8 kV และ X_T2", "หน้า 67–68", size=27)
        self.say("ระวัง: 127/13.2 kV คือแรงดันต่อเฟสของหม้อแปลงตัวเดียว  ต้องแปลงเป็นแรงดันสายก่อน", color=WARN)
        y1 = ystar(2.2, 0.2, 1.0, C_N)
        d2 = delta_tri(5.6, 0.2, 1.0, C_S)
        p1, p2 = y1.pts, d2.pts
        h1, h2 = T("ด้านสูง Y", 20, C_N).move_to([2.2, 1.6, 0]), T("ด้านต่ำ Delta", 20, C_S).move_to([5.6, 1.6, 0])
        ph = T("127 kV", 18, WHITE).move_to([1.5, 0.65, 0])
        a1 = dim([p1[1][0], p1[1][1] - 0.4], [p1[2][0], p1[2][1] - 0.4])
        a2 = dim([p2[1][0], p2[1][1] - 0.4], [p2[2][0], p2[2][1] - 0.4])
        l1 = T("? kV (สาย)", 18, YEL).move_to([2.2, p1[1][1] - 0.75, 0])
        l2 = T("13.2 kV (สาย = เฟส)", 18, YEL).move_to([5.6, p2[1][1] - 0.75, 0])
        self.play(Create(y1), Create(d2), FadeIn(h1), FadeIn(h2), FadeIn(ph), run_time=1.2)
        self.play(GrowFromCenter(a1), GrowFromCenter(a2), FadeIn(l1), FadeIn(l2), run_time=0.8)
        bd = B(self, x=-6.6, y=2.0, gap=0.06)
        self.say("ด้าน Y: แรงดันสาย = sqrt3 × แรงดันเฟส   ด้าน Delta: แรงดันสาย = แรงดันบนขดลวด", color=YEL)
        f1 = _m(r"\sqrt{3}\times127=220\,kV", YEL, 30)
        r1 = bd.add(1, "แรงดันสาย สองด้าน", VGroup(f1, T("ด้าน Delta 13.2 kV  →  อัตราส่วนสาย 220/13.2", 21, C_S)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
                    color=YEL, hold=0.4)
        l1n = T("220 kV (สาย)", 18, YEL).move_to(l1)
        self.play(Transform(l1, l1n), run_time=0.5)
        self.glow(f1, fig=VGroup(a1, l1), color=YEL)
        self.say("kV ฐานด้านนี้ = 230 × (13.2 / 220)  (ข้าม T2 ลงมา)", color=OK)
        f2 = MX(r"230", r"\times", r"\frac{13.2}{220}", r"=", r"13.8\,kV", font_size=32)
        r3 = bd.add(2, "แรงดันฐานด้านต่ำ", f2, color=OK, hold=0.5)
        self.glow(f2[4], fig=VGroup(a2, l2), color=OK)
        r4 = bd.add(3, "พิกัดรวม T2", _m(r"3\times100=300\,MVA", YEL, 28), color=YEL, hold=0.4)
        self.say("พิกัด 300 MVA เท่ากับฐาน 300 MVA → ส่วนกำลังไม่ต้องปรับ", color=YEL)
        self.wait(1.5)
        self.play(*[FadeOut(r) for r in bd.rows], run_time=0.5)
        bd = B(self, x=-6.6, y=2.0, gap=0.06)
        self.say("หน้า 68: แทนในสูตรเปลี่ยนฐาน  kV เดิม = 13.2   kV ใหม่ = 13.8", color=OK)
        g = MX(r"0.1", r"\times", r"\left(\frac{13.2}{13.8}\right)^{2}", r"\times", r"\frac{300}{300}", font_size=32)
        r5 = bd.add(1, "แทนค่า X_T2", g, color=OK, hold=0.4)
        self.glow(g[2], fig=VGroup(a2, l2), color=C_S)
        r6 = bd.add(2, "ผล", VGroup(_m(r"X_{T2}=0.0915\,p.u.", OK, 32), T("= 9.15 %", 22, GRAYTXT)).arrange(RIGHT, buff=0.3), color=OK, hold=0.5)
        self.say("ตรวจ: (13.2/13.8)² = 0.9149  → 0.1 × 0.9149 = 0.0915 ✓", color=C_IL)
        self.wait(3.5)
        self.keep("T2 แบบ 1 เฟส 3 ตัว: คูณ sqrt3 ที่ด้าน Y ก่อนเสมอ (127 → 220)  กำลังรวม = 3 เท่า (300 MVA)",
                  "ฐานหลัง T2 = 230 × 13.2/220 = 13.8 kV\nX_T2 = 0.1 × (13.2/13.8)² = 0.0915 p.u.")


# =============================================================== P69  หน้า 69
class P69_Zones(L):
    """สรุปแรงดันฐานทุกโซน เป็นตาราง 20 / 230 / 13.8 kV ; MVA ฐาน 300 ทุกโซน"""

    def construct(self):
        self.head("สรุปฐานทุกโซน (ตารางที่ต้องจดทุกครั้ง)", "หน้า 69")
        self.say("เดินจากเครื่องกำเนิดไปทีละหม้อแปลง  คูณอัตราส่วนแรงดันสาย  ส่วน MVA ฐานคงที่", color=OK)
        XN, XK, XM = -6.8, 0.0, 4.0
        hd = [T("โซน", 21, GRAYTXT).move_to([XN + 0.4, 1.7, 0]), T("kV ฐาน", 21, GRAYTXT).move_to([XK, 1.7, 0]),
              T("MVA ฐาน", 21, GRAYTXT).move_to([XM, 1.7, 0])]
        self.play(*[FadeIn(h) for h in hd], run_time=0.5)
        rows = [("ฝั่ง G (ก่อน T1)  จุด k", "20", YEL, 0.8), ("สายส่ง  จุด l–m", "230", OK, -0.5), ("หลัง T2  จุด n p r + มอเตอร์", "13.8", C_S, -1.8)]
        cells = []
        for i, (nm, kv, col, y) in enumerate(rows):
            a = fit_width(T(nm, 21, col), 6.2)
            a.move_to([XN + a.width / 2, y, 0])
            b = _m(kv + r"\,kV", col, 34).move_to([XK, y, 0])
            c = _m(r"300\,MVA", col, 30).move_to([XM, y, 0])
            self.mark("row")
            self.play(FadeIn(a), run_time=0.4)
            self.play(Write(b), Write(c), run_time=0.9)
            cells.append((a, b, c))
            if i < 2:
                ar = Arrow([XK, y - 0.35, 0], [XK, y - 0.95, 0], buff=0, color=GRAYTXT, stroke_width=3, tip_length=0.15)
                tx = _m(r"\times\frac{230}{20}" if i == 0 else r"\times\frac{13.2}{220}", GRAYTXT, 24).move_to([XK + 1.5, y - 0.65, 0])
                tt = T("ข้าม T1" if i == 0 else "ข้าม T2", 17, GRAYTXT).move_to([XK - 1.2, y - 0.65, 0])
                self.play(GrowArrow(ar), FadeIn(tx), FadeIn(tt), run_time=0.8)
                self.wait(0.6)
        self.wait(1.0)
        self.say("ลองถาม: บัส p อยู่โซนไหน?  คำตอบ: โซนหลัง T2 → 13.8 kV  (เหมือนมอเตอร์)", color=C_S)
        self.play(Indicate(cells[2][1], color=WHITE, scale_factor=1.3), Circumscribe(cells[2][0], color=C_S), run_time=1.6)
        self.wait(1.2)
        self.say("ใช้ตารางนี้ทุกครั้ง: ชิ้นอยู่โซนไหน ใช้ kV ฐานของโซนนั้น", color=YEL)
        self.wait(3.0)
        self.keep("แรงดันฐานทุกโซน: 20 kV (G) → 230 kV (สายส่ง) → 13.8 kV (มอเตอร์)  กำลังฐาน 300 MVA ทุกโซน",
                  "ชิ้นไหนอยู่โซนไหน ใช้ kV ฐานโซนนั้น\nไม่ใช้ kV ของโซนอื่น")


# =============================================================== P70  หน้า 70
class P70_Line(L):
    """ขั้น 5: สายส่ง Z จริง 32 ohm / Z ฐานโซน 230 kV = 176.3 / X = 0.1815 + กับดักใช้ฐานผิดโซน"""

    def construct(self):
        self.head("ขั้น 5: รีแอคแตนซ์สายส่ง p.u.", "หน้า 70")
        self.say("สายส่งอยู่โซน 230 kV  ต้องหารด้วย Z ฐานของโซน 230 kV เท่านั้น", color=OK)
        Y = 1.0
        a, b = -3.0, 3.0
        ln = wire((a, Y), (b, Y))
        ta, tb = Dot([a, Y, 0], radius=0.08, color=WHITE), Dot([b, Y, 0], radius=0.08, color=WHITE)
        km = dim([a, Y + 0.35], [b, Y + 0.35], C_IL)
        kt = T("64 km  ×  0.5 โอห์ม/km", 22, C_IL).move_to([0, Y + 0.8, 0])
        zb = Line([a, -1.2, 0], [b, -1.2, 0], color=OK, stroke_width=5)
        zt = T("โซน 230 kV  ·  300 MVA ฐาน", 20, OK).move_to([0, -1.6, 0])
        self.play(Create(ln), FadeIn(ta), FadeIn(tb), run_time=0.8)
        self.play(GrowFromCenter(km), FadeIn(kt), run_time=0.8)
        self.play(Create(zb), FadeIn(zt), run_time=0.7)
        self.wait(0.4)
        pic = VGroup(ln, ta, tb, km, kt, zb, zt)
        self.play(pic.animate.scale(0.55).move_to([3.9, 0.9, 0]), run_time=0.9)
        bd = B(self, x=-6.6, y=2.0, gap=0.1)
        self.say("ขั้น 1: Z จริงทั้งสาย = 0.5 × 64", color=C_IL)
        r1 = bd.add(1, "Z จริงทั้งสาย", _m(r"0.5\times64=32\,\Omega", C_IL, 30), color=C_IL, hold=0.6)
        self.glow(r1[1], fig=pic, color=C_IL)
        self.say("ขั้น 2: Z ฐาน = kV ฐาน² ÷ MVA ฐาน  ใช้ 230 kV (โซนสายส่ง)", color=OK)
        r2 = bd.add(2, "Z ฐาน ของโซน 230 kV", _m(r"Z_{b}=\frac{230^{2}}{300}=176.3\,\Omega", OK, 30), color=OK, hold=0.6)
        self.say("ขั้น 3: p.u. = Z จริง ÷ Z ฐาน", color=YEL)
        f = MX(r"X_{line}", r"=", r"\frac{32}{176.3}", r"=", r"0.1815", font_size=34)
        r3 = bd.add(3, "p.u.", f, color=YEL, hold=0.6)
        self.glow(f[4], color=YEL)
        self.say("ตรวจกับดัก: ถ้าเผลอใช้ kV ของโซนอื่น จะได้ผลผิดมาก", color=WARN)
        r4 = bd.add(4, "ใช้ฐานผิดโซน (คำนวณเอง)",
                    VGroup(_m(r"32/(20^{2}/300)=24.0", WARN, 26), _m(r"32/(13.8^{2}/300)=50.4", WARN, 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                    color=WARN, hold=1.0)
        cr = T("ผิดทั้งคู่ — ต้อง 0.1815", 22, WARN)
        cr.move_to([3.9, -1.9, 0])
        self.play(FadeIn(cr), run_time=0.6)
        self.wait(3.0)
        self.keep("สายส่งอยู่โซนไหน ใช้ฐาน kV ของโซนนั้น (230 kV)  ไม่ใช่ 20 หรือ 13.8",
                  "X_line = (0.5 × 64) / (230² / 300) = 32 / 176.3 = 0.1815 p.u.")


# =============================================================== P71  หน้า 71-72
class P71_Motors(L):
    """ขั้น 6-7: M1 = 0.2745 และ M2 = 0.5490 เคียงกัน + ตรวจ M2 = 2 x M1"""

    def construct(self):
        self.head("ขั้น 6–7: รีแอคแตนซ์มอเตอร์ M1 และ M2", "หน้า 71–72")
        self.say("ฐานโซนมอเตอร์: 13.8 kV , 300 MVA  แต่มอเตอร์พิกัด 13.2 kV  และ 200 / 100 MVA — ไม่ตรงทั้งคู่", color=OK)
        fac = _m(r"\left(\frac{13.2}{13.8}\right)^{2}=0.9149", C_S, 30).move_to([0, -3.0, 0])
        facl = T("ตัวคูณแรงดัน (ใช้ร่วมกันทั้ง M1 และ M2)", 18, GRAYTXT).move_to([0, -3.55, 0])
        self.play(Write(fac), FadeIn(facl), run_time=1.2)
        self.wait(0.6)
        b1 = B(self, x=-6.8, y=2.0, gap=0.08)
        b2 = B(self, x=0.3, y=2.0, gap=0.08)
        H1 = T("M1", 26, C_S).move_to([-4.6, 2.2, 0])
        H2 = T("M2", 26, C_S).move_to([2.5, 2.2, 0])
        self.play(FadeIn(H1), FadeIn(H2), run_time=0.4)
        b1.y = b2.y = 1.7
        self.say("แถวซ้าย M1 (200 MVA)  แถวขวา M2 (100 MVA)  สูตรเดียวกัน  ต่างกันที่ MVA", color=OK)
        b1.add(1, "ข้อมูล", T("13.2 kV , 200 MVA , X'' = 20 %", 20, WHITE), color=C_S, hold=0.3)
        b2.add(1, "ข้อมูล", T("13.2 kV , 100 MVA , X'' = 20 %", 20, WHITE), color=C_S, hold=0.6)
        f1 = MX(r"0.2", r"\times", r"\frac{300}{200}", r"\times", r"\left(\frac{13.2}{13.8}\right)^{2}", font_size=26)
        f2 = MX(r"0.2", r"\times", r"\frac{300}{100}", r"\times", r"\left(\frac{13.2}{13.8}\right)^{2}", font_size=26)
        r1 = b1.add(2, "แทนค่า", f1, color=C_S, hold=0.3)
        r2 = b2.add(2, "แทนค่า", f2, color=C_S, hold=0.6)
        self.say("ส่วนกำลัง: M1 = 300/200 = 1.5   M2 = 300/100 = 3", color=YEL)
        self.play(Indicate(f1[2], color=YEL), Indicate(f2[2], color=YEL), Circumscribe(f1[2], color=YEL), Circumscribe(f2[2], color=YEL), run_time=1.4)
        self.say("ส่วนแรงดัน: ทั้งคู่ × 0.9149", color=C_S)
        self.play(Indicate(f1[4], color=C_S), Indicate(f2[4], color=C_S), Circumscribe(f1[4], color=C_S), Circumscribe(f2[4], color=C_S), run_time=1.4)
        b1.add(3, "คิดทีละก้อน", _m(r"0.2\times1.5=0.3\ ;\ \ 0.3\times0.9149", WHITE, 24), color=C_S, hold=0.4)
        b2.add(3, "คิดทีละก้อน", _m(r"0.2\times3=0.6\ ;\ \ 0.6\times0.9149", WHITE, 24), color=C_S, hold=0.6)
        rr1 = b1.add(4, "ผล", _m(r"X_{M1}=0.2745", OK, 34), color=OK, hold=0.4)
        rr2 = b2.add(4, "ผล", _m(r"X_{M2}=0.5490", OK, 34), color=OK, hold=0.6)
        self.say("ตรวจ: M2 มี MVA ครึ่งเดียวของ M1 → X ต้องเป็น 2 เท่า  0.5490 = 2 × 0.2745 ✓", color=C_IL)
        self.play(Indicate(rr1[1], color=WHITE), Indicate(rr2[1], color=WHITE), Circumscribe(VGroup(rr1[1], rr2[1]), color=C_IL), run_time=1.6)
        self.wait(3.5)
        self.keep("มอเตอร์: ปรับทั้งสองส่วน — MVA (ฐาน/พิกัด) และ kV กำลังสอง (พิกัด/ฐาน)",
                  "X_M1 = 0.2 × (300/200) × (13.2/13.8)² = 0.2745\nX_M2 = 0.2 × (300/100) × (13.2/13.8)² = 0.5490")


# =============================================================== P73  หน้า 73
class P73_Final(L):
    """ขั้น 8: ประกอบ reactance diagram สุดท้าย ทีละชิ้น + สูตรสำเร็จ"""

    def construct(self):
        self.head("ขั้น 8: ประกอบ reactance diagram สุดท้าย", "หน้า 73")
        self.say("ทุกชิ้นเป็น jX ที่ฐาน 300 MVA ; ต่อนิวทรัลร่วม ; เหลือแหล่งกำเนิด E ของเครื่องจักรหมุน", color=OK)
        RY, NY = 1.15, -3.0
        nx = {"k": -5.4, "l": -2.9, "m": -0.4, "n": 2.1}
        px, rx = 3.8, 5.9
        rail = VGroup(wire((nx["k"], RY), (rx, RY)))
        bT1 = rbox((nx["k"] + nx["l"]) / 2, RY, "T1", "?", WHITE)
        bL = rbox((nx["l"] + nx["m"]) / 2, RY, "Line", "?", C_IL)
        bT2 = rbox((nx["m"] + nx["n"]) / 2, RY, "T2", "?", WHITE)
        bG = rbox(nx["k"], -0.55, "G", "?", YEL)
        bM1 = rbox(px, -0.55, "M1", "?", C_S)
        bM2 = rbox(rx, -0.55, "M2", "?", C_S)
        sG, sM1, sM2 = src(nx["k"], -1.85, "Eg", YEL), src(px, -1.85, "Em1", C_S), src(rx, -1.85, "Em2", C_S)
        W = []
        for x in (nx["k"], px, rx):
            W += [wire((x, RY), (x, -0.55 + 0.36)), wire((x, -0.55 - 0.36), (x, -1.85 + 0.3)), wire((x, -1.85 - 0.3), (x, NY))]
        W.append(wire((nx["k"], NY), (rx, NY)))
        nodes = VGroup(*[T(s, 17, GRAYTXT).move_to([nx[s], RY + 0.55, 0]) for s in "klmn"], T("p", 17, GRAYTXT).move_to([px, RY + 0.55, 0]),
                       T("r", 17, GRAYTXT).move_to([rx, RY + 0.55, 0]))
        # กล่องซ้อนบนเส้น rail: ลบช่วง rail ใต้กล่องไม่ต้อง (กล่องทึบ-โปร่ง) ใช้เส้นแยกช่วงแทน
        segs = VGroup(wire((nx["k"], RY), (bT1.get_left()[0], RY)), wire((bT1.get_right()[0], RY), (bL.get_left()[0], RY)),
                      wire((bL.get_right()[0], RY), (bT2.get_left()[0], RY)), wire((bT2.get_right()[0], RY), (rx, RY)))
        tn = T("neutral (นิวทรัลร่วม)", 17, GRAYTXT).move_to([0.2, NY - 0.35, 0])
        diag = VGroup(*W, segs, bG, bT1, bL, bT2, bM1, bM2, sG, sM1, sM2, nodes, tn)
        self.play(Create(diag), run_time=1.8)
        base = T("ฐาน: 300 MVA · 20 / 230 / 13.8 kV", 20, YEL).move_to([-3.6, 2.1, 0])
        self.play(FadeIn(base), run_time=0.5)

        def put(box, v, col, say_txt):
            self.say(say_txt, color=col)
            nv = Text(v, font_size=17, color=col).move_to(box[2])
            self.play(ReplacementTransform(box[2], nv), Indicate(box[0], color=col), run_time=0.9)
            box.remove(box[2])
            box.add(nv)
            self.wait(0.8)

        put(bG, "j0.2", YEL, "เครื่องกำเนิด G (จุด k): X = 0.2 ตรงๆ — ฐาน = พิกัดตัวเองจึงไม่ต้องแปลง")
        put(bT1, "j0.0857", WHITE, "T1 (k–l): 0.0857  จากหน้า 66")
        put(bL, "j0.1815", C_IL, "สายส่ง (l–m): 0.1815  จากหน้า 70")
        put(bT2, "j0.0915", WHITE, "T2 (m–n): 0.0915  จากหน้า 68")
        put(bM1, "j0.2745", C_S, "M1 (บัส p): 0.2745  จากหน้า 71")
        put(bM2, "j0.5490", C_S, "M2 (บัส r): 0.5490  จากหน้า 72")
        self.say("ทุกกล่องมีแต่ jX  ไม่มี R ไม่มีชันต์  และต่อนิวทรัลร่วมด้านล่าง", color=OK)
        self.play(*[Indicate(b[0], color=WHITE) for b in (bG, bT1, bL, bT2, bM1, bM2)], run_time=1.5)
        self.wait(3.0)
        self.keep("reactance diagram: jX อนุกรมตามทางผ่าน + แหล่งกำเนิด E ของเครื่องจักร + นิวทรัลร่วม",
                  "สูตรสำเร็จ: ① จดฐาน (MVA, kV เครื่องกำเนิด)  ② หา kV ทุกโซน\n③ เปลี่ยนฐาน X ทุกชิ้น  ④ วาดกล่อง jX  ⑤ ตรวจ: ฐานเล็กลง → p.u. เล็กลง", hold=4.5)
