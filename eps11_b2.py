"""EPS11 ชุด 2 (หน้า 1-39) ล็อต 2 — สัญลักษณ์ / แบบจำลอง / แผนภาพ 4 แบบ
P03_Symbols1 (1-3) · P04_Symbols2 (4) · P05_SingleLineSystem (5-6) · P08_IdealModel (7-9) · P15_FourDiagrams (15-16)
P17_ThreePhase (17-19) · P20_SingleLine (20) · P21_Impedance (21) · P22_Reactance (22-23)
"""
from eps11_lib import *


def _row(sym, text, x0, y, color=WHITE, size=21):
    sym.move_to([x0, y, 0])
    t = T(text, size, color)
    t.move_to([x0 + 1.15, y, 0]).align_to([x0 + 0.95, 0, 0], LEFT)
    return VGroup(sym, t)


def _ground(x, y, color=WHITE):
    return VGroup(Line([x - 0.15, y, 0], [x + 0.15, y, 0], color=color, stroke_width=3),
                  Line([x - 0.09, y - 0.07, 0], [x + 0.09, y - 0.07, 0], color=color, stroke_width=3),
                  Line([x - 0.04, y - 0.14, 0], [x + 0.04, y - 0.14, 0], color=color, stroke_width=3))


def _ysym(grounded=False, color=WHITE):
    a = Line([0, 0, 0], [-0.3, 0.3, 0], color=color, stroke_width=3)
    b = Line([0, 0, 0], [0.3, 0.3, 0], color=color, stroke_width=3)
    c = Line([0, 0, 0], [0, -0.35, 0], color=color, stroke_width=3)
    g = VGroup(a, b, c)
    if grounded:
        g.add(Line([0, -0.35, 0], [0, -0.55, 0], color=color, stroke_width=3), _ground(0, -0.55, color))
    return g


def _mach(letter, color=YEL):
    c = Circle(radius=0.3, stroke_color=color, stroke_width=3)
    return VGroup(c, Text(letter, font_size=22, color=color).move_to(c))


# =============================================================== P03  หน้า 1-3
class P03_Symbols1(Lesson):
    """สารบัญบท (หน้า 1-2 รวมกับหน้านี้) + ตารางสัญลักษณ์ (1): เครื่องจักร สายส่ง หม้อแปลง Y Δ คาปาซิเตอร์"""

    def construct(self):
        self.head("สัญลักษณ์อุปกรณ์ในระบบไฟฟ้ากำลัง (1)", "หน้า 1–3")
        self.say("บทที่ 11 มี 5 หัวข้อ  (หน้า 1–2 เป็นสารบัญ/ชื่อหัวข้อ จึงรวมไว้ในคลิปนี้)", color=OK)
        topics = ["1  สัญลักษณ์อุปกรณ์ในระบบไฟฟ้ากำลัง", "2  แบบจำลองเครื่องกำเนิดไฟฟ้าและหม้อแปลง", "3  การแทนระบบด้วยแผนภาพ",
                  "4  ค่าต่อหน่วย (Per-Unit)", "5  การคำนวณระบบเพื่อทำแผนภาพแบบต่างๆ"]
        tl = VGroup(*[T(t, 25, WHITE) for t in topics]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0, 0])
        for i, t in enumerate(tl):
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.45)
        self.play(Indicate(tl[0], color=YEL), run_time=0.9)
        self.wait(1.0)
        self.say("หน้า 3: จำสัญลักษณ์ที่จะเจอบนแผนภาพเส้นเดี่ยว  (ทีละแถว)", color=OK)
        self.play(FadeOut(tl), run_time=0.6)
        two = VGroup(*[coil_sym((0, 0.4), (0, -0.4), n=3, r=0.11, color=WHITE) for _ in range(2)]).arrange(RIGHT, buff=0.12)
        three = VGroup(*[coil_sym((0, 0.4), (0, -0.4), n=3, r=0.11, color=WHITE) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        tri = Triangle(color=WHITE, stroke_width=3).scale(0.33)
        cap = VGroup(Line([0, 0.45, 0], [0, 0.08, 0], color=WHITE, stroke_width=3), Line([-0.25, 0.08, 0], [0.25, 0.08, 0], color=WHITE, stroke_width=3),
                     Line([-0.25, -0.05, 0], [0.25, -0.05, 0], color=WHITE, stroke_width=3), Line([0, -0.05, 0], [0, -0.3, 0], color=WHITE, stroke_width=3), _ground(0, -0.3))
        rows = [
            (VGroup(_mach("M"), T("หรือ", 16, GRAYTXT), _mach("G")).arrange(RIGHT, buff=0.1), "เครื่องจักรไฟฟ้า (M = มอเตอร์ , G = เครื่องกำเนิด)", -6.6, 1.55),
            (Line([-0.5, 0, 0], [0.5, 0, 0], color=WHITE, stroke_width=3), "สายส่ง", -6.6, 0.3),
            (two, "หม้อแปลงไฟฟ้ากำลัง 2 ขดลวด", -6.6, -0.95),
            (three, "หม้อแปลงไฟฟ้ากำลัง 3 ขดลวด", -6.6, -2.2),
            (_ysym(False), "ระบบ 3 เฟส แบบ Y  ไม่ต่อลงดิน", 0.4, 1.55),
            (_ysym(True), "ระบบ 3 เฟส แบบ Y  ต่อลงดิน", 0.4, 0.3),
            (tri, "ระบบ 3 เฟส แบบเดลต้า (Δ)", 0.4, -0.95),
            (cap, "คาปาซิเตอร์ (C)", 0.4, -2.2),
        ]
        for sym, txt, x0, y in rows:
            r = _row(sym, txt, x0 + 0.5, y)
            fit_width(r[1], 5.6)
            self.play(FadeIn(r, shift=UP * 0.15), run_time=0.7)
            self.wait(0.9)
        self.wait(1.0)
        remember(self, "วงกลม G/M · เส้นตรง = สายส่ง · ขดคู่ = หม้อแปลง · Y · Y ต่อดิน · Δ · C", "ถ้าข้อสอบให้จับคู่ ดูตารางต้นฉบับหน้า 3 ซ้ำ")


# =============================================================== P04  หน้า 4
class P04_Symbols2(Lesson):
    """ตารางสัญลักษณ์ (2): เบรกเกอร์ PT CT มิเตอร์ บัส โหลด สวิตช์"""

    def construct(self):
        self.head("สัญลักษณ์อุปกรณ์ในระบบไฟฟ้ากำลัง (2)", "หน้า 4")
        self.say("อุปกรณ์ตัดต่อ / วัด / บัส  — 10 ตัว", color=OK)
        ln = lambda: Line([-0.55, 0, 0], [0.55, 0, 0], color=WHITE, stroke_width=3)

        def on_line(*extra):
            return VGroup(ln(), *extra)
        air = on_line(Arc(radius=0.25, start_angle=0, angle=PI, color=WHITE, stroke_width=3).shift(UP * 0.0))
        pt = VGroup(coil_sym((-0.45, 0), (-0.05, 0), n=2, r=0.1), coil_sym((0.05, 0), (0.45, 0), n=2, r=0.1))
        ct = on_line(Arc(radius=0.2, start_angle=0, angle=PI, color=WHITE, stroke_width=3), Arc(radius=0.2, start_angle=PI, angle=PI, color=WHITE, stroke_width=3).shift(RIGHT * 0.0))
        oil = on_line(Square(0.38, color=WHITE, stroke_width=3))
        am = VGroup(ln(), Circle(radius=0.26, color=WHITE, stroke_width=3), Text("A", font_size=20, color=WHITE))
        vm = VGroup(ln(), Circle(radius=0.26, color=WHITE, stroke_width=3), Text("V", font_size=20, color=WHITE))
        bus = VGroup(Line([-0.5, 0, 0], [0.5, 0, 0], color=WHITE, stroke_width=3), Line([0, -0.25, 0], [0, 0.25, 0], color=WHITE, stroke_width=3))
        load = VGroup(Line([0, -0.25, 0], [0, 0.25, 0], color=WHITE, stroke_width=3), Arrow([0, 0, 0], [0.45, 0, 0], buff=0, color=WHITE, stroke_width=3, tip_length=0.15))
        sw = VGroup(Line([-0.5, 0, 0], [-0.15, 0, 0], color=WHITE, stroke_width=3), Line([-0.15, 0, 0], [0.25, 0.25, 0], color=WHITE, stroke_width=3), Line([0.25, 0, 0], [0.5, 0, 0], color=WHITE, stroke_width=3))
        fsw = VGroup(Line([-0.5, 0, 0], [-0.15, 0, 0], color=WHITE, stroke_width=3), Line([-0.15, 0, 0], [0.25, 0.25, 0], color=WHITE, stroke_width=3), Line([0.25, 0, 0], [0.5, 0, 0], color=WHITE, stroke_width=3),
                     Square(0.14, color=YEL, stroke_width=3).move_to([0.05, 0.0, 0]))
        items = [(air, "เซอร์กิตเบรกเกอร์แบบอากาศ"), (pt, "หม้อแปลงแรงดัน (PT)"), (ct, "หม้อแปลงกระแส (CT)"), (oil, "เซอร์กิตเบรกเกอร์แบบน้ำมัน / ของเหลว"),
                 (am, "เครื่องวัดกระแส"), (vm, "เครื่องวัดแรงดัน"), (bus, "บัส (Bus)"), (load, "โหลดคงที่"), (sw, "สวิตช์ตัดตอน"), (fsw, "สวิตช์ตัดตอนแบบมีฟิวส์")]
        for i, (sym, txt) in enumerate(items):
            col, row = divmod(i, 5)
            x0 = -6.4 + 6.7 * col
            y = 1.6 - row * 1.0
            r = _row(sym, txt, x0 + 0.5, y, size=20)
            self.play(FadeIn(r, shift=UP * 0.12), run_time=0.55)
            self.wait(0.55)
        self.wait(1.2)
        remember(self, "ที่ใช้บ่อยในแผนภาพ: บัส (เส้นตรง/แท่ง) · เบรกเกอร์ · PT / CT · มิเตอร์ A, V", "ตารางนี้ไว้อ่านสัญลักษณ์ ไม่ต้องคำนวณ")


# =============================================================== P05  หน้า 5-6
class P05_SingleLineSystem(Lesson):
    """แบบจำลองระบบไฟฟ้ากำลัง: ผลิต -> ส่ง -> จำหน่าย + ตัวอย่าง single-line โรงงาน"""

    def construct(self):
        self.head("ระบบไฟฟ้ากำลังเขียนเป็นแผนภาพได้", "หน้า 5–6")
        self.say("ระบบที่ผลิตและส่งไฟไปโหลด เขียนเป็นวงจรแทนได้  (Single Line Diagram)", color=OK)
        Y = 0.9
        g = _mach("G")
        g.move_to([-6.3, Y, 0])
        t1 = VGroup(*[Circle(radius=0.26, color=WHITE, stroke_width=3).move_to([-4.55 + dx, Y, 0]) for dx in (-0.15, 0.15)])
        t2 = VGroup(*[Circle(radius=0.26, color=WHITE, stroke_width=3).move_to([0.45 + dx, Y, 0]) for dx in (-0.15, 0.15)])
        w = VGroup(wire((-6.0, Y), (-4.96, Y)), wire((-4.14, Y), (0.04, Y)), wire((0.86, Y), (2.2, Y)))
        bus = Line([2.2, Y + 0.9, 0], [2.2, Y - 1.0, 0], color=WHITE, stroke_width=7)
        loads = VGroup(*[VGroup(wire((2.2, y), (3.0, y)), Arrow([3.0, y, 0], [3.5, y, 0], buff=0, color=OK, stroke_width=3, tip_length=0.15)) for y in (Y + 0.6, Y + 0.1, Y - 0.4)])
        t3 = VGroup(*[Circle(radius=0.2, color=WHITE, stroke_width=3).move_to([4.6 + dx, Y - 0.9, 0]) for dx in (-0.12, 0.12)])
        w3 = VGroup(wire((2.2, Y - 0.9), (4.28, Y - 0.9)), wire((4.92, Y - 0.9), (5.4, Y - 0.9)), Arrow([5.4, Y - 0.9, 0], [5.9, Y - 0.9, 0], buff=0, color=OK, stroke_width=3, tip_length=0.15))
        self.play(Create(VGroup(w, bus, loads, w3)), FadeIn(g), Create(t1), Create(t2), Create(t3), run_time=1.8)
        lb = VGroup(T("เครื่องกำเนิด", 17, YEL).move_to([-6.3, Y + 0.65, 0]), T("หม้อแปลงเพิ่มแรงดัน\n11–115 kV (ลานไฟฟ้า)", 16, GRAYTXT).move_to([-4.55, Y + 0.95, 0]),
                    T("สายส่ง", 17, GRAYTXT).move_to([-2.0, Y + 0.4, 0]), T("หม้อแปลงลดแรงดัน\n115–22 kV (สถานีไฟฟ้า)", 16, GRAYTXT).move_to([0.45, Y + 0.95, 0]),
                    T("22,000–400 V", 16, GRAYTXT).move_to([4.6, Y - 1.4, 0]))
        self.play(FadeIn(lb), run_time=1.0)
        self.wait(1.2)
        # 3 ระบบ
        self.say("แบ่งเป็น 3 ระบบ: ผลิต → ส่ง → จำหน่าย", color=YEL)
        spans = [(-7.0, -3.3, "ระบบกำเนิดไฟฟ้า", YEL), (-3.3, 1.5, "ระบบส่งจ่ายไฟฟ้า", OK), (1.5, 6.6, "ระบบจำหน่ายไฟฟ้า", C_S)]
        for a, b, s, c in spans:
            br = Line([a + 0.1, -1.25, 0], [b - 0.1, -1.25, 0], color=c, stroke_width=5)
            tt = T(s, 22, c).move_to([(a + b) / 2, -1.7, 0])
            self.play(Create(br), FadeIn(tt), run_time=0.8)
            self.wait(0.5)
        self.wait(1.0)
        # หน้า 6
        self.newpage("หน้า 6")
        self.say("หน้า 6: ตัวอย่างจริง — โรงงาน 115 kV → 13.8 kV → 2.4 kV / 0.48 kV  (มีหม้อแปลง TX-1…TX-4 , มอเตอร์ M-1…M-4)", color=OK)
        self.fade_out_all(run_time=0.6)
        self._cap = None
        lv = [(115, "115 kV", C_E, 1.9), (13.8, "13.8 kV", C_IA, 0.5), (2.4, "2.4 kV / 0.48 kV", C_IL, -0.9)]
        t = title("ตัวอย่าง single-line ของโรงงานจริง", size=28)
        pr = page_ref("หน้า 6")
        self.play(FadeIn(t), FadeIn(pr), run_time=0.5)
        self._ttl, self._ref = t, pr
        cap = caption_top("ไล่จากบนลงล่าง: แหล่งจ่าย 115 kV → TX-1 → บัส 13.8 kV → TX-2, TX-3, TX-4 → บัสแรงต่ำ → มอเตอร์", color=OK)
        self.play(FadeIn(cap), run_time=0.5)
        self._cap = cap
        bus1 = Line([-4.0, 1.0, 0], [4.0, 1.0, 0], color=WHITE, stroke_width=7)
        src_ = VGroup(Line([0, 2.3, 0], [0, 1.7, 0], color=WHITE, stroke_width=3), T("115 kV", 20, C_E).move_to([1.0, 2.1, 0]))
        tx1 = VGroup(*[Circle(radius=0.2, color=WHITE, stroke_width=3).move_to([dx, 1.35, 0]) for dx in (-0.1, 0.1)])
        tx1.shift(LEFT * 0.0)
        b1 = T("13.8 kV", 20, C_IA).move_to([4.9, 1.0, 0])
        w1 = VGroup(wire((0, 1.7), (0, 1.6)), wire((0, 1.1), (0, 1.0)))
        tx_x = [-3.0, 0.0, 3.0]
        names = ["TX-3", "TX-4", "TX-2"]
        low = []
        for x, nm in zip(tx_x, names):
            a = VGroup(Line([x, 1.0, 0], [x, 0.4, 0], color=WHITE, stroke_width=3),
                       *[Circle(radius=0.2, color=WHITE, stroke_width=3).move_to([x, 0.15 + dy, 0]) for dy in (0.0, -0.22)],
                       Line([x, -0.18, 0], [x, -0.6, 0], color=WHITE, stroke_width=3), T(nm, 17, GRAYTXT).move_to([x + 0.7, 0.05, 0]))
            low.append(a)
        busL = Line([-4.0, -0.6, 0], [4.0, -0.6, 0], color=WHITE, stroke_width=7)
        mot = VGroup(*[VGroup(Line([x, -0.6, 0], [x, -1.4, 0], color=WHITE, stroke_width=3), _mach("M", C_S).scale(0.8).move_to([x, -1.7, 0]),
                              T(f"M-{i + 1}", 16, C_S).move_to([x + 0.55, -1.7, 0])) for i, x in enumerate([-3.5, -1.2, 1.2, 3.5])])
        self.play(Create(VGroup(bus1, src_, w1)), Create(tx1), FadeIn(b1), run_time=1.0)
        self.play(*[Create(a) for a in low], run_time=1.0)
        self.play(Create(busL), *[FadeIn(m) for m in mot], run_time=1.0)
        self.wait(1.3)
        hw = T("ลายมือ Min: ใช้ Software วาด/คำนวณได้ (โหลดฟรี แต่ต้องฝึก)", 20, YEL).move_to([0, -2.95, 0])
        self.play(FadeIn(hw), run_time=0.8)
        self.wait(2.0)
        remember(self, "single-line = ผลิต → ส่ง → จำหน่าย  ใช้เส้นเดียวแทนระบบ 3 เฟส", "ระดับแรงดันลดลงเป็นขั้นด้วยหม้อแปลง")


# =============================================================== P08  หน้า 7-9
class P08_IdealModel(Lesson):
    """หม้อแปลง: 1 เฟส/3 เฟส + แบบจำลองอุดมคติ N1:N2 ไม่มีการสูญเสีย"""

    def construct(self):
        self.head("แบบจำลองหม้อแปลง: อุดมคติ", "หน้า 7–9")
        self.say("หม้อแปลงไฟฟ้ากำลัง มี 2 แบบ: 1 เฟส และ 3 เฟส  (หน้า 7 เป็นชื่อหัวข้อ จึงรวมไว้ที่นี่)", color=OK)
        c1 = VGroup(T("หม้อแปลง 1 เฟส", 24, C_IL), T("1 ชุดขดลวด ปฐมภูมิ-ทุติยภูมิ", 18, GRAYTXT)).arrange(DOWN, buff=0.2)
        c2 = VGroup(T("หม้อแปลง 3 เฟส", 24, C_B), T("ใช้กับระบบ 3 เฟส (a, b, c)", 18, GRAYTXT)).arrange(DOWN, buff=0.2)
        cc = VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to([0, 0.6, 0])
        fr = VGroup(*[RoundedRectangle(width=4.2, height=1.5, corner_radius=0.12, stroke_color=c, stroke_width=3).move_to(m) for m, c in ((c1, C_IL), (c2, C_B))])
        self.play(FadeIn(cc), Create(fr), run_time=1.0)
        self.wait(1.6)
        self.say("หน้า 9: แบบจำลองอุดมคติ — ไม่มีการสูญเสียเลย", color=OK)
        self.play(FadeOut(VGroup(cc, fr)), run_time=0.6)
        p = core_pic(-3.2, 0.1)
        p["all"].scale(1.2, about_point=np.array([-3.2, 0.1, 0]))
        n1 = M(r"N_1", C_R, 26).next_to(p["c1"], LEFT, buff=0.1).shift(UP * 0.1)
        n2 = M(r"N_2", C_S, 26).next_to(p["c2"], RIGHT, buff=0.1).shift(UP * 0.1)
        lab = VGroup(T("แหล่งจ่าย", 17, GRAYTXT).next_to(p["src"], DOWN, buff=0.15), T("โหลด", 17, GRAYTXT).next_to(p["load"], DOWN, buff=0.15))
        self.play(FadeIn(p["all"]), run_time=1.0)
        self.play(FadeIn(n1), FadeIn(n2), FadeIn(lab), run_time=0.6)
        self.wait(0.8)
        # สัญลักษณ์
        self.say("เขียนเป็นสัญลักษณ์: ขดปฐมภูมิ N₁ ต่อแหล่งจ่าย  ขดทุติยภูมิ N₂ ต่อโหลด", color=YEL)
        top, bot = 1.2, -0.9
        xf = xf_ideal(4.0, 0.15, h=2.1)
        sy = VGroup(wire((2.0, top), (3.83, top)), wire((2.0, bot), (3.83, bot)), wire((4.17, top), (6.0, top)), wire((4.17, bot), (6.0, bot)), xf,
                    varrow(2.0, bot, top, C_A, r"v_1", LEFT), varrow(6.0, bot, top, C_A, r"v_2", RIGHT), M(r"N_1:N_2", WHITE, 24).move_to([4.0, -1.5, 0]))
        self.play(Create(sy), run_time=1.5)
        self.wait(0.8)
        self.say("อุดมคติ = ไม่มีความต้านทาน ไม่มีฟลักซ์รั่ว ไม่เสียกำลังในแกน  แรงดันเป็นไปตามอัตราส่วนรอบ", color=C_IL)
        rel = M(r"\frac{v_1}{v_2}=\frac{N_1}{N_2}", C_IL, 30).move_to([4.0, -2.55, 0])
        self.play(Write(rel), Indicate(p["c1"], color=C_R), Indicate(p["c2"], color=C_S), run_time=1.4)
        self.wait(1.8)
        remember(self, "หม้อแปลงอุดมคติ = N₁ : N₂ อย่างเดียว ไม่มีการสูญเสีย", "ของจริงมีของแถมอีก 6 อย่าง (R₁R₂ · L_l1 L_l2 · R_c L_m) → คลิปหน้า 10")


# =============================================================== P15  หน้า 15-16
class P15_FourDiagrams(Lesson):
    """แผนภาพ 4 แบบ: Three-Phase -> Single Line -> Impedance -> Reactance และใช้เมื่อไร"""

    def construct(self):
        self.head("แผนภาพ 4 แบบ ของระบบไฟฟ้ากำลัง", "หน้า 15–16")
        self.say("ระบบไฟฟ้ากำลังเขียนเป็นแผนภาพได้ 4 แบบ — ไล่จากละเอียดไปง่าย", color=OK)
        data = [("1", "วงจรสามเฟส", "Three-Phase Diagram", "ครบ a b c n", C_E),
                ("2", "เส้นเดียว", "Single Line Diagram", "ใช้เส้นเดียวแทน 3 เฟส", C_IL),
                ("3", "อิมพีแดนซ์", "Impedance Diagram", "ต่อเฟสเดียว: R, X_L, X_C", C_IA),
                ("4", "รีแอคแตนซ์", "Reactance Diagram", "เหลือเฉพาะ jX", C_B)]
        cards = []
        for i, (n, th, en, ds, c) in enumerate(data):
            num = Text(n, font_size=40, color=c)
            tx = VGroup(T(th, 24, c), T(en, 17, GRAYTXT), T(ds, 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            body = VGroup(num, tx).arrange(RIGHT, buff=0.35)
            fr = RoundedRectangle(width=5.6, height=1.5, corner_radius=0.12, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.07).move_to(body)
            cards.append(VGroup(fr, body))
        grid = VGroup(*cards)
        cards[0].move_to([-3.3, 0.9, 0]); cards[1].move_to([3.3, 0.9, 0]); cards[2].move_to([-3.3, -1.0, 0]); cards[3].move_to([3.3, -1.0, 0])
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.8)
            self.wait(0.8)
        ar = VGroup(*[Arrow(cards[a].get_edge_center(RIGHT if a % 2 == 0 else DOWN), cards[b].get_edge_center(LEFT if a % 2 == 0 else UP), buff=0.1, color=GRAYTXT, stroke_width=3)
                      for a, b in ((0, 1),)])
        self.play(Create(ar), run_time=0.6)
        self.say("ยิ่งไปทางท้าย ยิ่งตัดรายละเอียดทิ้ง — แต่ละแบบเหมาะกับงานต่างกัน", color=YEL)
        self.wait(2.0)
        self.say("ที่ต้องวาดเองในข้อสอบ: เส้นเดียว → รีแอคแตนซ์  (ดูคลิปหน้า 24–25)", color=OK)
        self.play(Indicate(cards[1], color=C_IL), Indicate(cards[3], color=C_B), run_time=1.4)
        self.wait(1.8)
        remember(self, "4 แบบ: 3 เฟส → เส้นเดียว → อิมพีแดนซ์ → รีแอคแตนซ์", "รีแอคแตนซ์ใช้คำนวณกระแสลัดวงจร (Fault)")


# =============================================================== P17  หน้า 17-19
class P17_ThreePhase(Lesson):
    """Three-Phase Diagram: วงจรครบ a b c n + ใช้เมื่อไร"""

    def construct(self):
        self.head("แผนภาพวงจร 3 เฟส (Three-Phase Diagram)", "หน้า 17–19")
        self.say("แบบที่ 1: วาดครบทั้ง 3 เฟส a, b, c และนิวทรัล n", color=OK)
        ys = [1.5, 0.3, -0.9]
        NY = -2.1
        parts = VGroup()
        sx = [-6.5, -6.1, -5.7]
        ex = [4.6, 4.1, 3.6]
        seq = [("zig", -5.2, -4.7), ("coil", -4.6, -4.0), ("zig", -3.4, -2.9), ("coil", -2.8, -2.2), ("zig", -1.4, -0.9), ("coil", -0.8, -0.1)]
        for k, y in enumerate(ys):
            parts.add(src(sx[k], y, "", YEL, r=0.22))
            lastx = sx[k] + 0.22
            for kind, a_, b_ in seq:
                if a_ <= lastx:
                    continue
                parts.add(wire((lastx, y), (a_, y)))
                parts.add(res_zig((a_, y), (b_, y), n=3, amp=0.07, color=C_R) if kind == "zig" else coil_sym((a_, y), (b_, y), n=3, r=0.07, color=C_IF))
                lastx = b_
            parts.add(wire((lastx, y), (ex[k], y)))
            parts.add(res_zig((ex[k], y), (ex[k], NY), n=3, amp=0.07, color=C_IA))
            parts.add(wire((sx[k], y - 0.22), (sx[k], NY)))
        parts.add(wire((sx[0], NY), (ex[0], NY)))
        hdr = VGroup(T("Generator", 18, YEL).move_to([-4.6, 2.35, 0]), T("Transformer", 18, WHITE).move_to([-2.8, 2.35, 0]),
                     T("Transmission Line", 18, C_IL).move_to([-0.75, 2.35, 0]), T("Load", 18, C_IA).move_to([4.1, 2.35, 0]))
        nlab = VGroup(*[M(s_, GRAYTXT, 22).move_to([x_, y_, 0]) for s_, x_, y_ in (("a", -6.5, 1.95), ("b", -6.1, 0.75), ("c", -5.7, -0.45))], M("n", GRAYTXT, 22).move_to([-6.9, NY, 0]))
        self.play(Create(parts), run_time=2.0)
        self.play(FadeIn(hdr), FadeIn(nlab), run_time=0.8)
        self.wait(1.0)
        for h, c in zip(hdr, (YEL, WHITE, C_IL, C_IA)):
            self.play(Indicate(h, color=c, scale_factor=1.2), run_time=0.7)
        self.wait(0.8)
        self.say("ทุกท่อนวาดซ้ำทั้ง 3 เฟส: ความต้านทาน (ซิกแซก) + ขดลวด (L)  (ของจริงยังมี C สายส่ง/สาขาขนานหม้อแปลง)", color=GRAYTXT)
        self.wait(1.8)
        # หน้า 19
        self.newpage("หน้า 19")
        self.say("หน้า 19: ใช้เมื่อไร? — เห็นการต่อทั้ง 3 เฟส แต่ซับซ้อนเกินจำเป็นสำหรับวิเคราะห์ทั่วไป", color=OK)
        self.play(FadeOut(VGroup(parts, hdr, nlab)), run_time=0.7)
        pts = [("ใช้หาค่าทางไฟฟ้าของสายส่ง", C_IL), ("ดูการต่ออุปกรณ์ไฟฟ้าทั้งสามเฟส", C_B), ("ซับซ้อนเกินความจำเป็นในการวิเคราะห์ระบบทั่วไป", C_E)]
        for tx, c in pts:
            row = VGroup(Dot(color=c), T(tx, 26, WHITE)).arrange(RIGHT, buff=0.3)
            row.move_to([0, 0.5 - pts.index((tx, c)) * 1.0, 0])
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(1.2)
        self.wait(1.0)
        remember(self, "Three-Phase Diagram = วาดครบ 3 เฟส  ละเอียดแต่ซับซ้อนเกินใช้วิเคราะห์ทั่วไป", "ปกติเราไม่วาดแบบนี้ในโจทย์")


# =============================================================== P20  หน้า 20
class P20_SingleLine(Lesson):
    """Single Line Diagram: G - T1(Δ-Y) - สายส่ง - T2(Y-Δ) - บัส p - M1, M2"""

    def construct(self):
        self.head("แผนภาพเส้นเดี่ยว (Single Line Diagram)", "หน้า 20")
        self.say("เส้นเดียวแทนระบบ 3 เฟส — ใช้ดูว่าอุปกรณ์ต่อกันอย่างไร และลดจำนวนเส้นลง", color=OK)
        Y = 0.5
        g = _mach("G").move_to([-5.6, Y, 0])
        gy = _ysym(True).scale(0.8).move_to([-6.6, Y - 0.1, 0])
        t1 = VGroup(*[Circle(radius=0.3, color=WHITE, stroke_width=3).move_to([-3.35 + dx, Y, 0]) for dx in (-0.17, 0.17)])
        t2 = VGroup(*[Circle(radius=0.3, color=WHITE, stroke_width=3).move_to([1.35 + dx, Y, 0]) for dx in (-0.17, 0.17)])
        wl = VGroup(wire((-5.3, Y), (-3.82, Y)), wire((-2.88, Y), (0.88, Y)), wire((1.82, Y), (3.3, Y)), wire((3.3, Y + 0.9), (3.3, Y - 0.9)),
                    wire((3.3, Y + 0.9), (4.0, Y + 0.9)), wire((3.3, Y - 0.9), (4.0, Y - 0.9)))
        m1 = _mach("M", C_S).move_to([4.3, Y + 0.9, 0])
        m2 = _mach("M", C_S).move_to([4.3, Y - 0.9, 0])
        nodes = VGroup(*[Dot([x, Y, 0], radius=0.06, color=GRAYTXT) for x in (-4.1, -2.6, 0.6, 2.1, 3.3)])
        nl = VGroup(*[T(s, 17, GRAYTXT).move_to([x, Y + 0.35, 0]) for s, x in (("k", -4.1), ("l", -2.6), ("m", 0.6), ("n", 2.1))], T("p", 17, GRAYTXT).move_to([3.0, Y + 0.45, 0]))
        names = VGroup(M(r"T_1", WHITE, 22).move_to([-3.35, Y + 0.8, 0]), M(r"T_2", WHITE, 22).move_to([1.35, Y + 0.8, 0]),
                       M(r"M_1", C_S, 20).move_to([5.0, Y + 0.9, 0]), M(r"M_2", C_S, 20).move_to([5.0, Y - 0.9, 0]))
        self.play(Create(wl), FadeIn(g), FadeIn(gy), Create(t1), Create(t2), FadeIn(m1), FadeIn(m2), run_time=1.8)
        self.play(FadeIn(nodes), FadeIn(nl), FadeIn(names), run_time=0.8)
        self.wait(1.0)
        # การต่อขดลวด
        self.say("สัญลักษณ์ใต้หม้อแปลงบอกการต่อขดลวด: T₁ เป็น Δ–Y(ต่อดิน)  ,  T₂ เป็น Y(ต่อดิน)–Δ", color=YEL)
        d1 = VGroup(Triangle(color=YEL, stroke_width=3).scale(0.2).move_to([-3.8, Y - 0.95, 0]), _ysym(True).scale(0.5).move_to([-2.9, Y - 0.95, 0]))
        d2 = VGroup(_ysym(True).scale(0.5).move_to([0.9, Y - 0.95, 0]), Triangle(color=YEL, stroke_width=3).scale(0.2).move_to([1.8, Y - 0.95, 0]))
        self.play(FadeIn(d1), FadeIn(d2), Indicate(t1, color=YEL), Indicate(t2, color=YEL), run_time=1.4)
        self.wait(1.4)
        self.say("อ่านจากซ้ายไปขวา: เครื่องกำเนิด → T₁ → สายส่ง → T₂ → บัส p → มอเตอร์ M₁ , M₂", color=OK)
        for m in (g, t1, t2, m1, m2):
            self.play(Indicate(m, color=OK), run_time=0.6)
        self.wait(1.5)
        remember(self, "single-line: 1 เส้น = ระบบ 3 เฟส  บอกว่าอุปกรณ์ต่อกันยังไง (G → T₁ → สายส่ง → T₂ → โหลด)", "การต่อขดลวด Δ / Y / Y ต่อดิน เขียนไว้ใต้หม้อแปลง")


# =============================================================== P21  หน้า 21
class P21_Impedance(Lesson):
    """Impedance Diagram: ต่อเฟสเดียว ประกอบด้วย R, X_L, X_C"""

    def construct(self):
        self.head("แผนภาพอิมพีแดนซ์ (Impedance Diagram)", "หน้า 21")
        self.say("เหมือนระบบเปอร์เฟส: วาดแค่เฟสเดียว  แต่เขียนพารามิเตอร์ครบตามแผนภาพเส้นเดี่ยว", color=OK)
        top, bot = 0.9, -1.7
        parts = VGroup()
        s1, s2 = src(-6.4, -0.4, "", YEL, r=0.24), src(-5.4, -0.4, "", YEL, r=0.24)
        parts.add(s1, s2)
        parts.add(MathTex("E_1", font_size=20, color=YEL).next_to(s1, LEFT, buff=0.1), MathTex("E_2", font_size=20, color=YEL).next_to(s2, DOWN, buff=0.1))
        parts.add(wire((-6.4, -0.14), (-6.4, top), (-5.4, top)), wire((-5.4, -0.14), (-5.4, top)))
        parts.add(wire((-6.4, -0.66), (-6.4, bot), (6.2, bot)), wire((-5.4, -0.66), (-5.4, bot)))
        la = ebox(-4.2, -0.4, "A", C_IA, w=0.6, h=0.7, size=22)
        parts.add(la, wire((-4.2, top), (-4.2, -0.05)), wire((-4.2, -0.75), (-4.2, bot)))
        blocks = [(-2.7, "T_1", WHITE), (0.2, r"\text{Line}", C_IL), (2.9, "T_2", WHITE)]
        parts.add(wire((-5.4, top), (-3.45, top)), wire((-1.95, top), (-0.55, top)), wire((0.95, top), (2.15, top)), wire((3.65, top), (5.0, top)))
        for x, nm, c in blocks:
            parts.add(ebox(x, top, nm, c, w=1.5, h=0.55, size=22))
        lb = ebox(5.0, -0.4, "B", C_IA, w=0.6, h=0.7, size=22)
        e3 = src(6.2, -0.4, "", YEL, r=0.24)
        parts.add(lb, e3, MathTex("E_3", font_size=20, color=YEL).next_to(e3, RIGHT, buff=0.1),
                  wire((5.0, top), (5.0, -0.05)), wire((5.0, -0.75), (5.0, bot)), wire((6.2, -0.14), (6.2, top), (5.0, top)), wire((6.2, -0.66), (6.2, bot)))
        names = VGroup(T("เครื่องกำเนิด 1 และ 2", 15, GRAYTXT).move_to([-5.9, -2.2, 0]), T("โหลด A", 15, GRAYTXT).move_to([-4.2, -2.2, 0]),
                       T("หม้อแปลง T1", 15, GRAYTXT).move_to([-2.7, -2.2, 0]), T("สายส่ง", 15, GRAYTXT).move_to([0.2, -2.2, 0]),
                       T("หม้อแปลง T2", 15, GRAYTXT).move_to([2.9, -2.2, 0]), T("โหลด B", 15, GRAYTXT).move_to([5.0, -2.2, 0]), T("เครื่องกำเนิด 3", 15, GRAYTXT).move_to([6.2, -2.55, 0]))
        self.play(Create(parts), run_time=2.0)
        self.play(FadeIn(names), run_time=0.8)
        self.wait(1.2)
        self.say("แต่ละท่อนมี 3 อย่าง: ความต้านทาน R , รีแอคแตนซ์เหนี่ยวนำ X_L , รีแอคแตนซ์ความจุ X_C", color=YEL)
        ex = VGroup(M(r"R", C_R, 40), M(r"jX_L", C_IF, 40), M(r"-jX_C", C_PHI, 40)).arrange(RIGHT, buff=1.2).move_to([0, 1.9, 0]).shift(DOWN * 0.0)
        ex.move_to([0, -3.15, 0])
        tt = VGroup(T("ต้านทาน", 18, C_R).next_to(ex[0], UP, buff=0.1), T("เหนี่ยวนำ", 18, C_IF).next_to(ex[1], UP, buff=0.1), T("ความจุ", 18, C_PHI).next_to(ex[2], UP, buff=0.1))
        self.play(FadeIn(ex), FadeIn(tt), run_time=1.0)
        self.play(*[Indicate(parts[i], color=YEL) for i in (0, 1)], run_time=0.8)
        self.wait(2.0)
        self.say("พารามิเตอร์ต้องเขียนให้ตรงกับแผนภาพเส้นเดี่ยว  (ครบกว่าแบบ reactance ซึ่งตัดทิ้งหลายอย่าง)", color=OK)
        self.wait(2.0)
        remember(self, "Impedance diagram = เฟสเดียว + R, X_L, X_C ครบ  ตรงตาม single-line", "ถัดไป: ตัดเหลือเฉพาะ jX → reactance diagram")


# =============================================================== P22  หน้า 22-23
class P22_Reactance(Lesson):
    """Reactance Diagram: ใช้คำนวณ fault ไม่เหมาะ load flow + ตัด R, magnetizing, capacitive + เหตุผล"""

    def construct(self):
        self.head("แผนภาพรีแอคแตนซ์ (Reactance Diagram)", "หน้า 22–23")
        self.say("ใช้คำนวณกระแสลัดวงจร (Fault Calculation)  ไม่เหมาะกับการศึกษา Load Flow", color=OK)
        top, bot = 1.0, -1.7
        e1, e2, e3 = src(-5.6, -0.7, "", YEL, r=0.27), src(-4.5, -0.7, "", YEL, r=0.27), src(5.6, -0.7, "", YEL, r=0.27)
        x1, x2, x3 = coil_sym((-5.6, top), (-5.6, -0.2), n=3, color=C_IF), coil_sym((-4.5, top), (-4.5, -0.2), n=3, color=C_IF), coil_sym((5.6, top), (5.6, -0.2), n=3, color=C_IF)
        t1 = coil_sym((-3.4, top), (-2.4, top), n=3, color=C_IF)
        ln = coil_sym((-0.5, top), (0.8, top), n=4, color=C_IF)
        t2 = coil_sym((2.8, top), (3.8, top), n=3, color=C_IF)
        base = VGroup(e1, e2, e3, x1, x2, x3, t1, ln, t2,
                      wire((-5.6, top), (-3.4, top)), wire((-2.4, top), (-0.5, top)), wire((0.8, top), (2.8, top)), wire((3.8, top), (5.6, top)),
                      wire((-5.6, -0.97), (-5.6, bot), (5.6, bot)), wire((-4.5, -0.97), (-4.5, bot)), wire((5.6, -0.97), (5.6, bot)))
        labs = VGroup(M(r"E_1", YEL, 20).next_to(e1, LEFT, buff=0.12), M(r"E_2", YEL, 20).next_to(e2, RIGHT, buff=0.12), M(r"E_3", YEL, 20).next_to(e3, RIGHT, buff=0.12),
                      M(r"T_1", WHITE, 22).move_to([-2.9, 1.4, 0]), T("สายส่ง", 20, C_E).move_to([0.15, 1.4, 0]), M(r"T_2", WHITE, 22).move_to([3.3, 1.4, 0]),
                      T("นิวทรัล", 20, C_E).move_to([0.2, bot - 0.35, 0]))
        self.play(Create(base), FadeIn(labs), run_time=1.8)
        self.wait(1.0)
        # รายการตัด
        self.say("ตัดได้ 3 อย่าง: ความต้านทาน · กระแส magnetizing ของหม้อแปลง · รีแอคแตนซ์ความจุของสายส่ง", color=YEL)
        rr = VGroup(M(r"R", C_R, 26), T("ความต้านทาน", 17, C_R)).arrange(DOWN, buff=0.1).move_to([-4.0, -2.5, 0])
        mm = VGroup(M(r"I_E", C_PHI, 26), T("กระแส magnetizing", 17, C_PHI)).arrange(DOWN, buff=0.1).move_to([0.0, -2.5, 0])
        cc = VGroup(M(r"X_C", C_PHI, 26), T("ความจุของสายส่ง", 17, C_PHI)).arrange(DOWN, buff=0.1).move_to([4.0, -2.5, 0])
        bars = []
        for g_, col in ((rr, C_R), (mm, C_PHI), (cc, C_PHI)):
            self.play(FadeIn(g_), run_time=0.7)
            self.play(Create(Cross(g_, stroke_color=C_E, stroke_width=5)), run_time=0.5)
            self.wait(0.5)
        self.wait(0.8)
        # หน้า 23 เหตุผล
        self.newpage("หน้า 23")
        self.say("หน้า 23: ทำไมตัดได้?  เพราะแต่ละอย่าง 'น้อยมาก' เมื่อเทียบกับของใหญ่", color=OK)
        self.play(FadeOut(VGroup(base, labs, rr, mm, cc, *[m for m in self.mobjects if isinstance(m, Cross)])), run_time=0.8)
        why = [("ความต้านทาน", "น้อยมากเมื่อเทียบกับรีแอคแตนซ์รวมของทั้งระบบ", C_R),
               ("โหลดคงที่ และ คาปาซิเตอร์", "ตอนลัดวงจร กระแสส่วนนี้น้อยมากเมื่อเทียบกับกระแสรวมของสาย (total line current)", C_B),
               ("ชันต์แอดมิตแตนซ์ในหม้อแปลง", "กระแสกระตุ้นน้อยมากเมื่อเทียบกับกระแสโหลดเต็มพิกัด (full load current)", C_PHI)]
        y = 1.2
        for h, d, c in why:
            blk = VGroup(T(h, 26, c), fit_width(T(d, 20, WHITE), 11.5)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, y, 0])
            blk.align_to([-6.2, 0, 0], LEFT)
            self.play(FadeIn(blk, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.6)
            y -= 1.35
        self.wait(1.0)
        remember(self, "reactance diagram = เหลือแค่ jX (+ แหล่ง E) ตัด R · I_E · X_C ทิ้ง  ใช้กับ Fault ไม่ใช้กับ Load Flow",
                 "เหตุผล: ของที่ตัดน้อยมากเมื่อเทียบกับกระแส/รีแอคแตนซ์รวม")
