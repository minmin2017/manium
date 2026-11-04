"""EPS11 (บทที่ 11: per-unit + reactance diagram) — 4 คลิปมูลค่าสูงสุดต่อการสอบ ดู eps8_lib.py\nP44_BaseQuantities (หน้า 40-46) · P49_ChangeOfBase (48-49,60,65-68) · P61_Ex_BaseZones (61-69) · P70_Ex_Diagram (70-73)\nตัวเลขทุกตัวมาจากสไลด์ PDF บทที่ 11  กฎ: MathTex ห้ามมีภาษาไทย\n"""
from eps8_lib import *


def _m(tex, color=WHITE, size=26):
    return MathTex(tex, font_size=size, color=color)


def _two(a, b, gap=0.5):
    return VGroup(a, b).arrange(RIGHT, buff=gap)


# =============================================================== P44  หน้า 40-46
class P44_BaseQuantities(Lesson):
    """ค่าฐาน 3 เฟส (Ib, Zb, V_LN, VA_1p) + ตัวอย่างพิสูจน์ 60,000 kVA / 230 kV ได้ p.u. เท่ากันทั้ง 1 เฟสและ 3 เฟส"""

    def construct(self):
        self.head("ค่าฐาน 3 เฟส + ค่าต่อหน่วย (p.u.)", "หน้า 40–46")
        self.say("p.u. = ค่าจริง ÷ ค่าฐาน  เลือกฐานแค่ 2 ตัว: กำลัง 3 เฟส กับ แรงดันสาย", color=OK)
        r1 = VGroup(Text("แรงดัน/กำลังต่อเฟส", font_size=18, color=GRAYTXT),
                    _m(r"V_{LN}=V_{LL}/\sqrt{3}\ \ ,\ \ VA_{1\phi}=VA_{3\phi}/3", C_IL, 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        r2 = VGroup(Text("กระแสฐาน", font_size=18, color=GRAYTXT),
                    _m(r"I_{b}=\frac{VA_{3\phi}}{\sqrt{3}\,V_{LL}}", C_IA, 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        r3 = VGroup(Text("อิมพีแดนซ์ฐาน", font_size=18, color=GRAYTXT),
                    _m(r"Z_{b}=\frac{V_{LL}^{2}}{VA_{3\phi}}", C_E, 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        panel = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        box = RoundedRectangle(width=panel.width + 0.5, height=panel.height + 0.4, corner_radius=0.12,
                               stroke_color=YEL, stroke_width=3, fill_color=YEL, fill_opacity=0.06)
        grp = VGroup(box, panel)
        panel.move_to(box)
        grp.move_to([4.0, -0.1, 0])
        self.play(FadeIn(grp), run_time=1.0)
        self.glow(r3[1], color=C_E)
        self.say("ตัวอย่างหน้า 44–46: ฐาน 60,000 kVA (3 เฟส) และ 230 kV (สาย)", color=OK)
        bd = Board(self, x=-6.6, y=2.0, gap=0.1)
        bd.add(1, "โจทย์ให้ (ฐาน)", VGroup(n_text("กำลัง 60,000 kVA", size=23), n_text("แรงดันสาย 230 kV", size=23)
                                            ).arrange(RIGHT, buff=0.5), color=OK, hold=1.1)
        bd.add(2, "ฐานต่อเฟส (kVA , kV)", _two(_m(r"60000/3=20000", WHITE, 28), _m(r"230/\sqrt{3}=132.8", WHITE, 28)),
               color=OK, hold=1.1)
        bd.add(3, "ค่าจริง 115 kV → p.u.", _two(_m(r"115/230=0.5", C_IL, 28), _m(r"66.4/132.8=0.5", C_IL, 28)),
               color=OK, hold=1.1)
        self.say("แรงดันสาย-สาย กับ สาย-นิวทรัล ได้ p.u. เท่ากัน = 0.5  (ตรวจ ✓)", color=C_IL)
        bd.add(4, "ค่าจริง 15,000 kVA → p.u.", _two(_m(r"15000/60000=0.25", C_IA, 28), _m(r"5000/20000=0.25", C_IA, 28)),
               color=OK, hold=1.1)
        self.say("กำลัง 3 เฟส กับ ต่อเฟส ได้ p.u. เท่ากัน = 0.25  จึงคิดแบบไหนก็ได้", color=C_IA)
        self.wait(2.5)
        self.exam("หาค่าฐาน 3 เฟส",
                  "I_b = VA3p / (sqrt3 x V_LL)    Z_b = V_LL² / VA3p\nV_LN = V_LL / sqrt3    VA1p = VA3p / 3\n(แรงดันที่บอก = แรงดันสาย, กำลังที่บอก = กำลัง 3 เฟส)")


# =============================================================== P49  หน้า 48-49, 60, 65-68
class P49_ChangeOfBase(Lesson):
    """สูตรเปลี่ยนฐาน + ตัวอย่าง X_T1 = 0.0857 และ X_T2 = 0.0915"""

    def construct(self):
        self.head("เปลี่ยนฐาน p.u. (Change of Base)", "หน้า 48–49, 60, 65–68")
        self.say("p.u. ของอุปกรณ์อิงพิกัดตัวเอง แต่ระบบมีฐานของระบบ → ต้องแปลงให้ฐานตรงกันก่อนรวมวงจร", color=OK)
        f = MathTex(r"Z_{new}", r"=", r"Z_{given}", r"\left(\frac{kV_{given}}{kV_{new}}\right)^{2}",
                    r"\frac{MVA_{new}}{MVA_{given}}", font_size=40)
        f[3].set_color(C_S)
        f[4].set_color(YEL)
        f.move_to([0, 0.7, 0])
        self.play(Write(f), run_time=1.6)
        n1 = Text("kV: กลับด้าน และยกกำลังสอง", font_size=21, color=C_S).move_to([f[3].get_center()[0], -0.9, 0])
        n2 = Text("MVA: ไม่กลับด้าน", font_size=21, color=YEL).move_to([f[4].get_center()[0] + 0.5, -1.6, 0])
        self.play(Indicate(f[3], color=WHITE), FadeIn(n1), run_time=1.2)
        self.play(Indicate(f[4], color=WHITE), FadeIn(n2), run_time=1.2)
        why = Text("เพราะ Z p.u. = Z จริง × MVA ÷ kV²", font_size=21, color=GRAYTXT).move_to([0, -2.4, 0])
        self.play(FadeIn(why), run_time=0.7)
        self.wait(3.0)
        # ---- ตัวอย่าง T1
        self.say("ตัวอย่าง T1 (หน้า 65–66): ฐานระบบ 300 MVA, 230 kV  แต่ T1 พิกัด 350 MVA", color=OK)
        self.play(FadeOut(VGroup(n1, n2, why)), f.animate.scale(0.62).move_to([3.9, 1.4, 0]), run_time=0.9)
        fit_width(f, 5.4)
        bd = Board(self, x=-6.6, y=2.0, gap=0.1)
        bd.add(1, "ข้อมูล T1", VGroup(n_text("350 MVA , 230 kV , X = 10 %", size=23), n_text("ฐานระบบ 300 MVA , 230 kV", size=23)
                                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), color=OK, hold=1.1)
        bd.add(2, "แทนค่า", _m(r"0.1\,(230/230)^{2}\,(300/350)", WHITE, 32), color=OK, hold=1.1)
        res = VGroup(_m(r"X_{T1}=0.0857", OK, 36), n_text("= 8.57 %", size=23, color=GRAYTXT)).arrange(RIGHT, buff=0.3)
        bd.add(3, "ผล", res, color=OK, hold=1.1)
        bd.add(4, "ตรวจ", n_text("ฐาน MVA เล็กลง (350→300) p.u. ต้องเล็กลง ✓", size=22, color=GRAYTXT), color=OK, hold=1.1)
        self.wait(3.0)
        # ---- ตัวอย่าง T2
        self.say("ตัวอย่าง T2 (หน้า 67–68): ฐานฝั่งนี้ 13.8 kV  พิกัด 300 MVA = ฐาน 300 MVA", color=OK)
        self.play(*[FadeOut(r) for r in bd.rows], run_time=0.6)
        bd2 = Board(self, x=-6.6, y=2.0, gap=0.1)
        bd2.add(1, "ข้อมูล T2", VGroup(n_text("1 เฟส 3 ตัว: 3×100 = 300 MVA", size=23),
                                      n_text("แรงดันสาย 220 / 13.2 kV · X = 10 %", size=23)
                                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), color=OK, hold=1.1)
        bd2.add(2, "แทนค่า", _m(r"0.1\,(13.2/13.8)^{2}\,(300/300)", WHITE, 32), color=OK, hold=1.1)
        res2 = VGroup(_m(r"X_{T2}=0.0915", OK, 36), n_text("= 9.15 %", size=23, color=GRAYTXT)).arrange(RIGHT, buff=0.3)
        bd2.add(3, "ผล", res2, color=OK, hold=1.1)
        bd2.add(4, "ตรวจ", _m(r"(13.2/13.8)^{2}=0.9149\ \rightarrow\ 0.0915", GRAYTXT, 26), color=OK, hold=1.1)
        self.wait(2.5)
        self.exam("p.u. ที่ฐานไม่ตรงระบบ → เปลี่ยนฐาน",
                  "Z_new = Z_given · (kV_given / kV_new)² · (MVA_new / MVA_given)\nตัวอย่าง: X_T1 = 0.0857 , X_T2 = 0.0915")


# =============================================================== P61  หน้า 61-69
def _xfmr(cx, cy, color=WHITE):
    a = Circle(radius=0.28, stroke_color=color, stroke_width=3).move_to([cx - 0.17, cy, 0])
    b = Circle(radius=0.28, stroke_color=color, stroke_width=3).move_to([cx + 0.17, cy, 0])
    return VGroup(a, b)


def _mach(cx, cy, letter, color):
    c = Circle(radius=0.33, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    t = Text(letter, font_size=22, color=color).move_to(c)
    return VGroup(c, t)


class P61_Ex_BaseZones(Lesson):
    """โจทย์หลัก: G 300MVA/20kV -> T1 230/20 -> สายส่ง -> T2 -> M1,M2 ; หาแรงดันฐานทุกโซน 20 / 230 / 13.8 kV"""

    def construct(self):
        self.head("ตัวอย่างหลัก: หาแรงดันฐานแต่ละโซน", "หน้า 61–69")
        self.say("โจทย์: เครื่องกำเนิด → T1 → สายส่ง 64 km → T2 → มอเตอร์ M1, M2  (วาด reactance diagram + p.u.)", color=OK)
        Y = 0.7
        g = _mach(-6.1, Y, "G", YEL)
        t1 = _xfmr(-3.9, Y)
        t2 = _xfmr(1.9, Y)
        w1 = wire((-5.77, Y), (-4.35, Y))
        w2 = wire((-3.45, Y), (1.45, Y))
        w3 = wire((2.35, Y), (3.4, Y))
        bus = Line([3.4, 1.5, 0], [3.4, -0.1, 0], color=WHITE, stroke_width=6)
        m1 = _mach(4.6, 1.5, "M", C_S)
        m2 = _mach(4.6, -0.1, "M", C_S)
        w4 = wire((3.4, 1.5), (4.27, 1.5))
        w5 = wire((3.4, -0.1), (4.27, -0.1))
        self.play(Create(VGroup(w1, w2, w3, bus, w4, w5)), FadeIn(g), Create(t1), Create(t2), FadeIn(m1), FadeIn(m2), run_time=1.6)
        lg = n_text("G  300 MVA\n20 kV  Xs = 20 %", size=16, color=YEL).move_to([-5.7, -0.55, 0])
        l1 = n_text("T1  3 เฟส  350 MVA\n230/20 kV  X = 10 %", size=16, color=GRAYTXT).move_to([-3.1, -0.55, 0])
        l2 = n_text("T2  1 เฟส 3 ตัว ตัวละ 100 MVA\n127/13.2 kV  X = 10 %", size=16, color=GRAYTXT).move_to([1.2, -0.6, 0])
        ll = n_text("สายส่ง 64 km  0.5 ohm/km", size=16, color=GRAYTXT).move_to([-0.8, 1.15, 0])
        lm1 = n_text("M1  200 MVA\n13.2 kV  X'' = 20 %", size=15, color=C_S).move_to([6.1, 1.5, 0])
        lm2 = n_text("M2  100 MVA\n13.2 kV  X'' = 20 %", size=15, color=C_S).move_to([6.1, -0.1, 0])
        self.play(*[FadeIn(x) for x in (lg, l1, l2, ll, lm1, lm2)], run_time=1.2)
        self.wait(4.0)
        self.say("ฐานเลือกจากพิกัดเครื่องกำเนิด: 300 MVA และ 20 kV  — แต่แต่ละโซนมีแรงดันฐานไม่เท่ากัน", color=YEL)
        self.play(*[FadeOut(x) for x in (lg, l1, l2, ll, lm1, lm2)], run_time=0.6)
        zl = [(-6.5, -4.4, "20 kV", YEL, -5.45), (-3.4, 1.4, "230 kV", OK, -1.0), (2.45, 5.2, "13.8 kV", C_S, 3.8)]
        brs, txts = [], []
        for a, b, s, c, cx in zl:
            brs.append(Line([a, -1.3, 0], [b, -1.3, 0], color=c, stroke_width=5))
            txts.append(Text(s, font_size=28, color=c).move_to([cx, -1.75, 0]))
        self.play(*[Create(x) for x in brs], *[FadeIn(x) for x in txts], run_time=1.0)
        c1 = n_text("ฐาน G: 20 kV, 300 MVA", size=18, color=YEL).move_to([-5.0, -2.5, 0])
        self.play(FadeIn(c1), run_time=0.6)
        self.say("ข้าม T1: แรงดันฐาน × อัตราส่วนแรงดันสาย 230/20", color=OK)
        c2 = _m(r"230=20\times\frac{230}{20}", OK, 28).move_to([-1.0, -2.55, 0])
        self.play(Write(c2), Indicate(t1, color=OK), run_time=1.4)
        self.say("ข้าม T2: 1 เฟส 3 ตัว → แรงดันสาย = sqrt3 × 127 = 220 kV  อัตราส่วน 220/13.2", color=C_S)
        c3 = _m(r"13.8=230\times\frac{13.2}{220}", C_S, 28).move_to([4.2, -2.55, 0])
        c3b = _m(r"\sqrt{3}\times127=220\,kV", C_S, 20).move_to([4.2, -3.3, 0])
        self.play(Write(c3), FadeIn(c3b), Indicate(t2, color=C_S), run_time=1.6)
        self.wait(2.5)
        self.say("กำลังฐาน 300 MVA เท่ากันทุกโซน  เปลี่ยนเฉพาะแรงดันฐาน", color=YEL)
        self.wait(2.5)
        self.exam("แรงดันฐานแต่ละโซน",
                  "ฐาน = พิกัดเครื่องกำเนิด (300 MVA, 20 kV)\nข้ามหม้อแปลง: คูณอัตราส่วนแรงดันสาย  20 → 230 → 13.8 kV\n(MVA ฐานเท่าเดิมทุกโซน)")


# =============================================================== P70  หน้า 70-73
def _rbox(cx, cy, name, val, color=WHITE, w=0.82, h=0.7):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08).move_to([cx, cy, 0])
    n = Text(name, font_size=17, color=GRAYTXT).move_to([cx, cy + 0.16, 0])
    v = Text(val, font_size=17, color=color).move_to([cx, cy - 0.15, 0])
    return VGroup(r, n, v)


def _src(cx, cy, label, color):
    c = Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    t = Text(label, font_size=14, color=color).move_to(c)
    return VGroup(c, t)


class P70_Ex_Diagram(Lesson):
    """ต่อจาก P61: X_line = 0.1815, X_M1 = 0.2745, X_M2 = 0.5490 แล้วประกอบ reactance diagram ครบ"""

    def construct(self):
        self.head("ตัวอย่างหลัก: คำนวณที่เหลือ + reactance diagram", "หน้า 70–73")
        self.say("ฐานทั้งระบบ 300 MVA · โซน 20 / 230 / 13.8 kV  ค่าที่ได้แล้ว: X_G = 0.2, X_T1 = 0.0857, X_T2 = 0.0915", color=OK)
        RY, NY = 1.2, -2.3
        gx, t1x, lx, t2x, m1x, m2x = 1.1, 2.15, 3.3, 4.45, 5.45, 6.4
        bG = _rbox(gx, -0.2, "G", "?", YEL)
        bT1 = _rbox(t1x, RY, "T1", "?", WHITE)
        bL = _rbox(lx, RY, "Line", "?", C_IL)
        bT2 = _rbox(t2x, RY, "T2", "?", WHITE)
        bM1 = _rbox(m1x, -0.2, "M1", "?", C_S)
        bM2 = _rbox(m2x, -0.2, "M2", "?", C_S)
        sG, sM1, sM2 = _src(gx, -1.55, "Eg", YEL), _src(m1x, -1.55, "Em1", C_S), _src(m2x, -1.55, "Em2", C_S)
        W = []
        W += [wire((gx, RY), (t1x - 0.4, RY)), wire((t1x + 0.4, RY), (lx - 0.4, RY)), wire((lx + 0.4, RY), (t2x - 0.4, RY)),
              wire((t2x + 0.4, RY), (m2x, RY))]
        for x, b, s in ((gx, bG, sG), (m1x, bM1, sM1), (m2x, bM2, sM2)):
            W.append(wire((x, RY), (x, -0.2 + 0.35)))
            W.append(wire((x, -0.2 - 0.35), (x, -1.55 + 0.28)))
            W.append(wire((x, -1.55 - 0.28), (x, NY)))
        W.append(wire((gx, NY), (m2x, NY)))
        tn = Text("neutral", font_size=15, color=GRAYTXT).move_to([3.5, NY - 0.3, 0])
        diag = VGroup(*W, bG, bT1, bL, bT2, bM1, bM2, sG, sM1, sM2, tn)
        self.play(Create(diag), run_time=1.6)
        for b, v in ((bG, "j0.2"), (bT1, "j0.0857"), (bT2, "j0.0915")):
            nv = Text(v, font_size=17, color=WHITE).move_to(b[2])
            self.play(ReplacementTransform(b[2], nv), run_time=0.4)
            b.remove(b[2])
            b.add(nv)
        base = n_text("ฐาน: 300 MVA · 20 / 230 / 13.8 kV", size=22, color=YEL).move_to([-3.3, -2.8, 0])
        self.play(FadeIn(base), run_time=0.5)

        def put(box, v, col):
            nv = Text(v, font_size=17, color=col).move_to(box[2])
            self.play(ReplacementTransform(box[2], nv), Indicate(box[0], color=col), run_time=0.8)
            box.remove(box[2])
            box.add(nv)

        # ---- สายส่ง
        self.say("สายส่ง: ใช้ฐานโซน 230 kV  Z_b = 230² / 300", color=C_IL)
        bd = Board(self, x=-6.6, y=2.0, gap=0.1)
        bd.add(1, "Z จริง", _m(r"0.5\times64=32\,\Omega", WHITE, 30), color=C_IL, hold=1.1)
        bd.add(2, "Z ฐาน (230 kV)", _m(r"230^{2}/300=176.3\,\Omega", WHITE, 30), color=C_IL, hold=1.1)
        bd.add(3, "p.u.", _m(r"X_{line}=32/176.3=0.1815", C_IL, 32), color=C_IL, hold=1.1)
        put(bL, "j0.1815", C_IL)
        self.wait(2.0)
        self.play(*[FadeOut(r) for r in bd.rows], run_time=0.5)
        # ---- M1
        self.say("M1: ทั้ง MVA (200≠300) และ kV (13.2≠13.8) ไม่ตรงฐาน → เปลี่ยนฐาน", color=C_S)
        bd = Board(self, x=-6.6, y=2.0, gap=0.1)
        bd.add(1, "ข้อมูล M1", VGroup(n_text("13.2 kV , 200 MVA , X'' = 20 %", size=23), n_text("ฐาน 13.8 kV , 300 MVA", size=23)
                                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), color=C_S, hold=1.1)
        bd.add(2, "แทนค่า", _m(r"0.2\times(300/200)\times(13.2/13.8)^{2}", WHITE, 30), color=C_S, hold=1.1)
        bd.add(3, "ผล", VGroup(_m(r"X_{M1}=0.2745", C_S, 34), n_text("(0.2×1.5 = 0.3 ; ×0.9149)", size=20, color=GRAYTXT)
                              ).arrange(RIGHT, buff=0.3), color=C_S, hold=1.1)
        put(bM1, "j0.2745", C_S)
        self.wait(2.0)
        self.play(*[FadeOut(r) for r in bd.rows], run_time=0.5)
        # ---- M2
        self.say("M2: 100 MVA → อัตรา 300/100 = 3 เท่า", color=C_S)
        bd = Board(self, x=-6.6, y=2.0, gap=0.1)
        bd.add(1, "ข้อมูล M2", VGroup(n_text("13.2 kV , 100 MVA , X'' = 20 %", size=23), n_text("ฐาน 13.8 kV , 300 MVA", size=23)
                                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), color=C_S, hold=1.1)
        bd.add(2, "แทนค่า", _m(r"0.2\times(300/100)\times(13.2/13.8)^{2}", WHITE, 30), color=C_S, hold=1.1)
        bd.add(3, "ผล", VGroup(_m(r"X_{M2}=0.5490", C_S, 34), n_text("(0.2×3 = 0.6 ; ×0.9149)", size=20, color=GRAYTXT)
                              ).arrange(RIGHT, buff=0.3), color=C_S, hold=1.1)
        put(bM2, "j0.5490", C_S)
        self.wait(2.5)
        self.say("ได้ reactance diagram ครบ: มีแต่ jX  ไม่มี R, ชันต์, ความจุ", color=OK)
        self.play(*[Indicate(b[0], color=WHITE) for b in (bG, bT1, bL, bT2, bM1, bM2)], run_time=1.4)
        self.wait(2.5)
        self.exam("reactance diagram ที่ฐาน 300 MVA",
                  "X_G 0.2 · X_T1 0.0857 · สายส่ง 0.1815 · X_T2 0.0915\nM1 0.2745 · M2 0.5490  (ทุกตัวเป็น j , ต่อนิวทรัลร่วม)")
