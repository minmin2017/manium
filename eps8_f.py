"""EPS8 หน้า 1 และ 27-29 (P01 สมการแรงเคลื่อน 8-1/8-2 · P27 8-15 เครื่องกำเนิดอนุกรม รูป 8-14 · P28 การใช้งาน + คำถามท้ายบท) — ดู eps8_lib.py
ข้อกำหนดจากบทเรียนเรนเดอร์คลาวด์ (ฟอนต์ Loma กว้างกว่า Leelawadee ~25-30%): เว้นขอบเฟรม >= 0.4, ป้ายอย่าวางทับสาย/แกน/เส้นประ, ข้อความยาวใช้ fit_width"""
from eps8_lib import *
from eps8_c import _lv

K_OVER = OK
K_DIFF = WARN


def chip(tex, th, col, w=2.3, h=0.62):
    sym = MathTex(tex, font_size=28, color=col)
    nm = Text(th, font_size=18, color=WHITE)
    inner = VGroup(sym, nm).arrange(RIGHT, buff=0.12)
    box = RoundedRectangle(width=max(w, inner.width + 0.4), height=h, corner_radius=0.12, stroke_color=col, stroke_width=3,
                           fill_color=col, fill_opacity=0.14)
    inner.move_to(box)
    return VGroup(box, inner)


def tchip(th, col, size=20):
    t = Text(th, font_size=size, color=WHITE)
    box = RoundedRectangle(width=t.width + 0.5, height=0.62, corner_radius=0.12, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.16)
    t.move_to(box)
    return VGroup(box, t)


def ser_funcs():
    """เคอร์ฟรูป 8-14 (x = IL/Irated): E ไม่มีโหลด, หักแรงดันตก Ra+Rs, หักอาร์เมเจอร์รีแอคชั่น"""
    E0 = lambda x: 0.06 + 0.92 * (1 - np.exp(-4.2 * x)) - 0.10 * x ** 2
    V2 = lambda x: E0(x) - 0.12 * x
    V3 = lambda x: max(0.0, V2(x) - 2.6 * max(0.0, x - 0.58) ** 2.3)
    return E0, V2, V3


def scv(ax, f, col, w=5, x0=0.0, x1=1.18, n=40):
    m = VMobject(stroke_color=col, stroke_width=w)
    m.set_points_smoothly([ax.c2p(float(x), float(f(x))) for x in np.linspace(x0, x1, n)])
    return m


def dotted(m, col, w=3, n=44):
    d = DashedVMobject(m, num_dashes=n, dashed_ratio=0.5)
    d.set_stroke(color=col, width=w)
    return d


# =============================================================== P01  หน้า 1
class P01_EMFFormula(Lesson):
    """8-1 บทนำ + 8-2: E = (ZP/60a) φ n = k φ n  (Z, P, a คงที่ → ตัวแปรมีแค่ φ และ n)"""

    def construct(self):
        self.head("8-2 แรงเคลื่อนที่ถูกเหนี่ยวนำในอาร์เมเจอร์", "หน้า 1 · 8-1, 8-2, สมการ 8-1, 8-2")
        # ---------- 8-1 บทนำ
        self.say("8-1: เครื่องกำเนิดกระแสตรงมีหลายแบบ ลักษณะการทำงานต่างกัน → ต้องรู้ลักษณะสมบัติก่อนเลือกใช้ (บทนี้เทียบทุกแบบ)")
        lead = fit_width(Text("เครื่องกำเนิดไฟฟ้ากระแสตรง: ชนิดที่จะเรียนในบทนี้", font_size=22, color=GRAYTXT), 11).move_to([0, 1.4, 0])
        kinds = VGroup(tchip("กระตุ้นแยก", WHITE), tchip("ขนาน (shunt)", C_IF), tchip("ผสม cumulative", K_OVER),
                       tchip("ผสม differential", K_DIFF), tchip("อนุกรม (series)", C_IS)).arrange(RIGHT, buff=0.25)
        kinds = fit_width(kinds, 12.4).move_to([0, 0.3, 0])
        self.play(FadeIn(lead), LaggedStart(*[FadeIn(k, shift=UP * 0.2) for k in kinds], lag_ratio=0.3), run_time=2.2)
        self.wait(1.2)
        self.play(FadeOut(VGroup(lead, kinds)), run_time=0.5)

        # ---------- 8-2 สมการ
        m = machine(0.85).move_to([-4.3, 0.3, 0])
        eq = MathTex(r"E", r"=", r"\frac{Z\,P}{60\,a}", r"\phi", r"n", font_size=58)
        eq[0].set_color(C_E)
        eq[3].set_color(C_PHI)
        eq[4].set_color(YEL)
        t81 = Text("(8-1)", font_size=20, color=GRAYTXT)
        eqg = VGroup(eq, t81).arrange(RIGHT, buff=0.4).move_to([3.1, 1.85, 0])
        rows = [(r"E", "แรงเคลื่อนที่ถูกเหนี่ยวนำในอาร์เมเจอร์", C_E, None),
                (r"Z", "จำนวนของตัวนำทั้งหมด", C_IA, m.cond),
                (r"a", "จำนวนของเส้นทางที่ขนานกัน", WHITE, None),
                (r"\phi", "ฟลักซ์ต่อขั้วแม่เหล็ก", C_PHI, m.flux),
                (r"P", "จำนวนของขั้วแม่เหล็ก", WHITE, VGroup(m.poleN, m.poleS)),
                (r"n", "ความเร็วรอบของอาร์เมเจอร์", YEL, m.rot)]
        defs = VGroup(*[lab(tx, th, WHITE, 22, col) for tx, th, col, _ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        defs = fit_width(defs, 6.6).move_to([3.1, -0.45, 0])
        self.say("แรงเคลื่อนที่ถูกเหนี่ยวนำให้เกิดขึ้นในอาร์เมเจอร์ เขียนเป็นสมการได้ดังนี้ (สมการ 8-1)", color=C_E)
        self.play(FadeIn(m), run_time=1.0)
        self.play(Write(eq), FadeIn(t81), run_time=1.6)
        self.say("ความหมายของตัวแปรแต่ละตัว (ดูตำแหน่งในภาพเครื่อง)", color=GRAYTXT)
        for i, (_, _, col, part) in enumerate(rows):
            anims = [FadeIn(defs[i], shift=LEFT * 0.15)]
            if part is not None:
                anims.append(Indicate(part, color=col, scale_factor=1.12))
            self.play(*anims, run_time=0.9)
        self.wait(1.0)

        # ---------- ค่าคงที่ -> k
        self.say("Z, P, a เป็นค่าคงที่ของเครื่องแต่ละเครื่อง → ตัวแปรจริงมีแค่ 2 ตัว คือ ฟลักซ์ φ และความเร็วรอบ n", color=YEL)
        self.play(FadeOut(defs), eqg.animate.move_to([3.1, 0.9, 0]), run_time=0.9)
        brc = Brace(eq[2], DOWN, buff=0.12, color=GRAYTXT)
        cst = Text("Z, P, a = ค่าคงที่ของเครื่อง", font_size=20, color=GRAYTXT).next_to(brc, DOWN, buff=0.1)
        self.play(Create(brc), FadeIn(cst), run_time=0.9)
        self.play(Indicate(eq[3], color=C_PHI, scale_factor=1.3), Indicate(eq[4], color=YEL, scale_factor=1.3), run_time=1.0)
        self.say("รวมค่าคงที่เป็น k → สมการ 8-2:  E = k φ n  (E แปรตามฟลักซ์ และตามความเร็วรอบ)", color=OK)
        eq2 = MathTex(r"E", r"=", r"k", r"\phi", r"n", font_size=58)
        eq2[0].set_color(C_E)
        eq2[2].set_color(GRAYTXT)
        eq2[3].set_color(C_PHI)
        eq2[4].set_color(YEL)
        t82 = Text("(8-2)", font_size=20, color=GRAYTXT)
        kdef = MathTex(r"k=\frac{Z\,P}{60\,a}", font_size=34, color=GRAYTXT)
        e2g = VGroup(eq2, t82).arrange(RIGHT, buff=0.4).move_to([2.2, -1.65, 0])
        kdef.move_to([6.2, -1.65, 0])
        self.play(Write(eq2), FadeIn(t82), run_time=1.3)
        self.play(FadeIn(kdef), run_time=0.7)
        self.wait(1.0)

        # ---------- φ และ n มาจากไหน
        self.say("φ ขึ้นกับแรงเคลื่อนแม่เหล็กที่จ่ายให้วงจรแม่เหล็ก (กระแสฟิลด์) · n ขึ้นกับต้นกำลังที่ขับเครื่อง", color=C_PHI)
        orig = card([("φ มาจากแรงเคลื่อนแม่เหล็ก (กระแสฟิลด์ If)", C_PHI), ("n มาจากต้นกำลังที่ขับให้อาร์เมเจอร์หมุน", YEL)], w=5.4, color=GRAYTXT, size=19)
        orig = fit_width(orig, 6.0).move_to([-3.9, -2.6, 0])
        self.play(FadeIn(orig, shift=UP * 0.2), Indicate(m.flux, color=C_PHI, scale_factor=1.1), Indicate(m.rot, color=YEL, scale_factor=1.1), run_time=1.2)
        self.wait(2.0)
        self.exam("คำถามท้ายบท 8-1: แรงเคลื่อนที่ถูกเหนี่ยวนำให้เกิดขึ้นในอาร์เมเจอร์ขึ้นอยู่กับตัวประกอบอะไรบ้าง",
                  "E = ZPφn/60a = kφn · Z (ตัวนำ), P (ขั้ว), a (เส้นทางขนาน) คงที่ → ขึ้นกับฟลักซ์ต่อขั้ว φ และความเร็วรอบ n")


# =============================================================== P27  หน้า 27
class P27_SeriesGenerator(Lesson):
    """8-15 เครื่องกำเนิดแบบอนุกรม: ไม่มีชันท์ฟิลด์ → สร้างแรงดันด้วยอำนาจแม่เหล็กตกค้าง + ป้อนกลับบวก; รูป 8-14"""

    def construct(self):
        self.head("8-15 เครื่องกำเนิดแบบอนุกรม · รูป 8-14", "หน้า 27 · 8-15, รูปที่ 8-14")
        XL, XR, YT, YB = -6.0, -1.3, 1.4, -1.4
        arm = arm_sym([XL, 0.0], r=0.45, letter="E")
        ser = coil_sym([-4.6, YT], [-2.6, YT], n=4, r=0.1, color=C_IS)
        ld = res_zig([XR, 0.7], [XR, -0.7], n=4, color=C_R)
        wires = VGroup(wire((XL, 0.45), (XL, YT), (-4.6, YT)), wire((-2.6, YT), (XR, YT), (XR, 0.7)),
                       wire((XR, -0.7), (XR, YB), (XL, YB), (XL, -0.45)))
        t_arm = Text("อาร์เมเจอร์", font_size=18, color=C_E).move_to([-5.05, 0.0, 0])
        t_ser = Text("เซรี่ฟิลด์ (ฟิลด์ชุดเดียว)", font_size=18, color=C_IS).move_to([-3.6, YT + 0.5, 0])
        t_ld = Text("โหลด", font_size=18, color=C_R).move_to([XR + 0.65, 0.0, 0])
        circ = VGroup(wires, ser, ld, arm, t_arm, t_ser, t_ld)
        a_i = Arrow([-4.6, 0.95, 0], [-3.2, 0.95, 0], buff=0, color=C_IL, stroke_width=4, tip_length=0.17)
        t_i = MathTex(r"I_a=I_s=I_L", font_size=28, color=C_IL).move_to([-2.2, 0.95, 0])
        path = wire((XL, 0.45), (XL, YT), (XR, YT), (XR, YB), (XL, YB), (XL, -0.45))
        c0 = card([("ไม่มีโหลด: ไม่มีกระแสผ่านเซรี่ฟิลด์", GRAYTXT), "Vt = E เล็กน้อยจากอำนาจแม่เหล็กตกค้างเท่านั้น"], w=5.6, color=GRAYTXT, size=18)
        c0 = fit_width(c0, 6.0).move_to([-3.65, -2.55, 0])

        self.say("เครื่องกำเนิดอนุกรมมีเซรี่ฟิลด์ชุดเดียว ไม่มีชันท์ฟิลด์ → กระแสโหลดทั้งหมดไหลผ่านเซรี่ฟิลด์ (Ia = Is = IL)", color=C_IS)
        self.play(Create(circ), run_time=1.6)
        self.play(Create(a_i), FadeIn(t_i), run_time=0.8)
        self.play(flow(path, C_IL, run=1.6))
        self.say("หมุนที่ความเร็วพิกัด: อำนาจแม่เหล็กตกค้างให้ E เล็กน้อย → ต่อโหลดแล้วมีกระแสค่าน้อยๆ ไหลผ่านเซรี่ฟิลด์", color=GRAYTXT)
        self.play(FadeIn(c0, shift=UP * 0.2), run_time=0.9)
        self.wait(0.8)

        names = [(r"I_L\uparrow", "กระแสโหลดเพิ่ม", C_IL), (r"\phi\uparrow", "ฟลักซ์เพิ่ม", C_PHI), (r"E\uparrow", "แรงเคลื่อนเพิ่ม", C_E), (r"V_t\uparrow", "แรงดันขั้วเพิ่ม", C_E)]
        chs = VGroup(*[chip(a, b, c, w=2.6) for a, b, c in names]).arrange(DOWN, buff=0.4).move_to([3.0, 0.45, 0])
        arrs = VGroup(*[Arrow(chs[i].get_bottom(), chs[i + 1].get_top(), buff=0.04, color=GRAYTXT, stroke_width=3, tip_length=0.14) for i in range(3)])
        pb = [chs[3].get_right() + RIGHT * 0.05, chs[3].get_right() + RIGHT * 0.75, chs[0].get_right() + RIGHT * 0.75]
        back = wire(*pb, color=YEL, width=3)
        back_tip = Arrow(chs[0].get_right() + RIGHT * 0.75, chs[0].get_right() + RIGHT * 0.05, buff=0, color=YEL, stroke_width=3, tip_length=0.18)
        t_loop = Text("วนซ้ำ", font_size=18, color=YEL).move_to([chs[0].get_right()[0] + 1.25, 0.45, 0])
        self.say("กระแสน้อยๆ นี้ทำให้ฟลักซ์เพิ่ม → E เพิ่ม → Vt เพิ่ม → IL เพิ่ม → ฟลักซ์เพิ่มอีก ... วนซ้ำเรื่อยๆ (ป้อนกลับบวก)", color=YEL)
        for i in range(4):
            self.play(FadeIn(chs[i], shift=DOWN * 0.15), *([Create(arrs[i - 1])] if i > 0 else []), run_time=0.8)
        self.play(Create(back), Create(back_tip), FadeIn(t_loop), run_time=0.9)
        self.play(flow(path, C_IL, run=1.4))

        sat = card([("จนวงจรแม่เหล็กอิ่มตัว", OK), "E และ IL ไม่เพิ่มอีก = จุดทำงานเสถียร"], w=4.9, color=OK, size=19)
        sat = fit_width(sat, 5.2).move_to([3.6, -2.55, 0])
        self.say("กระบวนการนี้ต่อเนื่องจนวงจรแม่เหล็กอิ่มตัว → E และ IL ไม่เพิ่มอีก = จุดทำงานเสถียรของเครื่องกำเนิด", color=OK)
        self.play(FadeIn(sat, shift=UP * 0.2), run_time=0.9)
        self.wait(1.6)

        # ---------- รูป 8-14
        self.say("รูป 8-14: เคอร์ฟ Vt–IL ของเครื่องอนุกรม — เริ่มจากแรงเคลื่อนที่เกิดขึ้นขณะไม่มีโหลด แล้วหักแรงดันตกทีละอย่าง", color=C_E)
        self.play(FadeOut(VGroup(circ, a_i, t_i, c0, chs, arrs, back, back_tip, t_loop, sat)), run_time=0.8)
        E0, V2, V3 = ser_funcs()
        g = make_axes(pos=[-6.2, -2.5], x_len=5.4, y_len=4.2, xmax=1.3, ymax=1.1, xl=r"I_L", yl=r"V_t")
        g.xlab.set_color(C_IL)
        ax = g.ax
        c_e = dotted(scv(ax, E0, C_E, 3), C_E, 3)
        c_2 = dotted(scv(ax, V2, YEL, 3), YEL, 3)
        c_3 = scv(ax, V3, WHITE, 6, 0.0, 1.16)
        t_e = Text("แรงเคลื่อนที่เกิดขึ้น\nขณะที่ไม่มีโหลด", font_size=19, color=C_E, line_spacing=0.9).move_to([-0.2, 0.85, 0])
        pa, pb2 = ax.c2p(1.06, E0(1.06)), ax.c2p(1.06, V2(1.06))
        pc = ax.c2p(1.06, float(V3(1.06)))
        arr_a = DoubleArrow(pa, pb2, buff=0, color=YEL, stroke_width=3, tip_length=0.13)
        arr_b = DoubleArrow(pb2, pc, buff=0, color=WARN, stroke_width=3, tip_length=0.13)
        t_a = Text("แรงดันลดลง เนื่องจากความต้านทาน\nของอาร์เมเจอร์และเซรี่ฟิลด์", font_size=18, color=YEL, line_spacing=0.9)
        t_a.move_to([pa[0] + 0.25 + t_a.width / 2, (pa[1] + pb2[1]) / 2 + 0.55, 0])
        t_b = Text("แรงดันลดลง เนื่องจาก\nอาร์เมเจอร์รีแอคชั่น", font_size=18, color=WARN, line_spacing=0.9)
        t_b.move_to([pb2[0] + 0.25 + t_b.width / 2, (pb2[1] + pc[1]) / 2 - 0.2, 0])
        self.play(Create(g), run_time=1.0)
        self.play(Create(c_e), FadeIn(t_e), run_time=1.4)
        self.say("หักแรงดันตกที่ความต้านทานของอาร์เมเจอร์และเซรี่ฟิลด์ (Ia·Ra + Is·Rs) → เส้นประล่าง", color=YEL)
        self.play(Create(c_2), Create(arr_a), FadeIn(t_a), run_time=1.5)
        self.say("แล้วหักอาร์เมเจอร์รีแอคชั่น (ฟลักซ์ลด เมื่อกระแสมาก) → เส้นทึบ = Vt จริง เพิ่มขึ้นแล้วชันลงจนเป็นศูนย์", color=WARN)
        self.play(Create(c_3), Create(arr_b), FadeIn(t_b), run_time=1.8)
        self.wait(1.8)
        self.exam("คำถามท้ายบท 8-20: จงอธิบายลักษณะสมบัติของเครื่องกำเนิดแบบอนุกรม",
                  "ไม่มีชันท์ฟิลด์ สร้างแรงดันจากอำนาจแม่เหล็กตกค้าง + ป้อนกลับบวกจนอิ่มตัว · Vt = E − แรงดันตก (Ra, Rs) − อาร์เมเจอร์รีแอคชั่น → เพิ่มขึ้นแล้วชันลง")


# =============================================================== P28  หน้า 28-29
QS = [("8-1", "แรงเคลื่อนเหนี่ยวนำขึ้นกับอะไรบ้าง", "P01"), ("8-2", "คงความเร็ว เปลี่ยนฟลักซ์ → E อย่างไร", "P01"),
      ("8-3", "เลยจุดอิ่มตัว เพิ่มแรงเคลื่อนแม่เหล็ก", "P02"), ("8-4", "คงฟลักซ์ เพิ่มความเร็ว → E อย่างไร", "P04"),
      ("8-5", "เส้นความต้านทานของฟิลด์คืออะไร", "P07"), ("8-6", "กระบวนการสร้างแรงเคลื่อน (ขนาน)", "P08-P10"),
      ("8-7", "ความต้านทานวิกฤตคืออะไร", "P11"), ("8-8", "ป้อนไฟนอกฟิลด์ 2-3 นาที (flashing)", "P11"),
      ("8-9", "สาเหตุที่เครื่องไม่สร้างแรงเคลื่อน", "P11-P12"), ("8-10", "สาเหตุที่ Vt ของเครื่องขนานลดลง", "P13"),
      ("8-11", "เคอร์ฟลักษณะสมบัติภายนอก (ขนาน)", "P14"), ("8-12", "โวลท์เตจเรกูเลชั่นคืออะไร", "P14-P15"),
      ("8-13", "ไดอะแกรม cumulative แบบ short-shunt", "P16"), ("8-14", "ไดอะแกรม cumulative แบบ long-shunt", "P16"),
      ("8-15", "cumulative กับ differential ต่างกัน", "P18"), ("8-16", "over compound (ผสมเกิน)", "P19"),
      ("8-17", "flat compound (ผสมพอดี)", "P21"), ("8-18", "under compound (ผสมขาด)", "P23"),
      ("8-19", "ไดเวอร์เตอร์คืออะไร", "P22"), ("8-20", "เครื่องกำเนิดแบบอนุกรม", "P27-P28")]


def qrow(num, txt, clip, x0):
    n = Text(num, font_size=17, color=YEL)
    t = fit_width(Text(txt, font_size=17, color=WHITE), 4.4)
    c = Text("→ " + clip, font_size=16, color=C_IL)
    n.move_to([x0 + n.width / 2, 0, 0])
    t.move_to([x0 + 0.85 + t.width / 2, 0, 0])
    c.move_to([x0 + 5.45 + c.width / 2, 0, 0])
    return VGroup(n, t, c)


class P28_SeriesUsesQuestions(Lesson):
    """หน้า 28: เครื่องอนุกรมใช้น้อย — แหล่งกำเนิดกระแส (ส่วนชันลง) / series booster (ส่วนเพิ่มขึ้น); หน้า 29: คำถามท้ายบท 8-1..8-20 + คลิปที่ตอบ"""

    def construct(self):
        self.head("เครื่องกำเนิดอนุกรม: การใช้งาน · คำถามท้ายบท", "หน้า 28 · รูปที่ 8-14")
        E0, V2, V3 = ser_funcs()
        g = make_axes(pos=[-6.2, -2.5], x_len=5.2, y_len=4.0, xmax=1.3, ymax=1.1, xl=r"I_L", yl=r"V_t")
        g.xlab.set_color(C_IL)
        ax = g.ax
        c_3 = scv(ax, V3, WHITE, 6, 0.0, 1.16)
        rise = scv(ax, V3, OK, 9, 0.0, 0.42)
        fall = scv(ax, V3, WARN, 9, 0.78, 1.14)
        t_sat = Text("เลยจุดอิ่มตัวของวงจรแม่เหล็ก", font_size=18, color=GRAYTXT).move_to(ax.c2p(0.78, 0.97) + UP * 0.1)
        self.say("เครื่องกำเนิดอนุกรมมักออกแบบให้อาร์เมเจอร์รีแอคชั่นค่อนข้างสูง → เลยจุดอิ่มตัวของวงจรแม่เหล็ก เคอร์ฟชันลงอย่างมาก", color=WARN)
        self.play(Create(g), run_time=0.9)
        self.play(Create(c_3), FadeIn(t_sat), run_time=1.4)
        self.wait(0.8)

        self.say("ในทางปฏิบัติใช้น้อยมาก แต่บางครั้งใช้เป็นแหล่งกำเนิดกระแส โดยใช้ส่วนที่ชันลงของเคอร์ฟ", color=WARN)
        cd1 = card([("ใช้เป็นแหล่งกำเนิดกระแส", WARN), "ใช้ส่วนที่ชันลงของเคอร์ฟ"], w=4.4, color=WARN, size=20).move_to([3.6, 1.55, 0])
        self.play(FadeOut(t_sat), Create(fall), FadeIn(cd1, shift=LEFT * 0.2), run_time=1.2)
        self.wait(1.0)

        self.say("และใช้เป็นบูสเตอร์อนุกรม (series booster) โดยใช้ส่วนที่เพิ่มขึ้นของเคอร์ฟ เพิ่มแรงดันในสายส่งไฟฟ้ากระแสตรงระยะไกล", color=OK)
        cd2 = card([("ใช้เป็นบูสเตอร์อนุกรม (series booster)", OK), "ใช้ส่วนที่เพิ่มขึ้นของเคอร์ฟ"], w=4.4, color=OK, size=20).move_to([3.6, 0.3, 0])
        cd2 = fit_width(cd2, 4.9).move_to([3.6, 0.3, 0])
        self.play(Create(rise), FadeIn(cd2, shift=LEFT * 0.2), run_time=1.2)
        # แผนผังบูสเตอร์ในสายส่ง
        XG, XR2, YTP, YBT = 0.55, 5.9, -1.55, -3.25
        gen = arm_sym([XG, (YTP + YBT) / 2], r=0.3, letter="G")
        rl = res_zig([1.3, YTP], [2.7, YTP], n=4, color=C_R)
        bo = Circle(radius=0.28, stroke_color=OK, stroke_width=3, fill_color="#1B3A2B", fill_opacity=0.9).move_to([3.8, YTP])
        bt = Text("B", font_size=22, color=OK).move_to(bo)
        ld = res_zig([XR2, YTP], [XR2, YBT], n=4, color=C_R)
        bwires = VGroup(wire((XG, (YTP + YBT) / 2 + 0.3), (XG, YTP), (1.3, YTP)), wire((2.7, YTP), (3.52, YTP)), wire((4.08, YTP), (XR2, YTP)),
                        wire((XR2, YBT), (XG, YBT), (XG, (YTP + YBT) / 2 - 0.3)))
        t_rl = Text("สายส่งไกล (R)", font_size=17, color=C_R).move_to([2.0, YTP + 0.42, 0])
        t_bo = Text("บูสเตอร์อนุกรม", font_size=17, color=OK).move_to([4.15, YTP + 0.55, 0])
        t_ld2 = Text("โหลด", font_size=17, color=C_R).move_to([XR2 + 0.55, (YTP + YBT) / 2, 0])
        dgm = VGroup(bwires, gen, rl, bo, bt, ld, t_rl, t_bo, t_ld2)
        self.play(Create(dgm), run_time=1.5)
        self.play(flow(wire((XG, (YTP + YBT) / 2 + 0.3), (XG, YTP), (XR2, YTP), (XR2, YBT), (XG, YBT), (XG, (YTP + YBT) / 2 - 0.3)), C_IL, run=1.6))
        note = fit_width(Text("กระแสมาก → แรงดันตกในสายมาก แต่ E ของบูสเตอร์ก็เพิ่มตามกระแส (ส่วนที่เพิ่มขึ้นของเคอร์ฟ) ช่วยชดเชย", font_size=17, color=GRAYTXT), 7.4)
        note.move_to([3.4, -0.85, 0])
        self.play(FadeIn(note), run_time=0.7)
        self.wait(2.2)

        # ---------- หน้า 29: คำถามท้ายบท
        self.newpage("หน้า 29 · คำถามท้ายบท")
        self.say("หน้า 29 เป็นรายการคำถามท้ายบท 8-1 ถึง 8-20 — ทบทวนด้วยการตอบเอง แล้วเปิดคลิปที่ระบุเทียบ", color=YEL)
        self.play(FadeOut(VGroup(g, c_3, rise, fall, cd1, cd2, dgm, note)), run_time=0.8)
        colA = VGroup(*[qrow(a, b, c, -6.9) for a, b, c in QS[:10]]).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        colB = VGroup(*[qrow(a, b, c, 0.4) for a, b, c in QS[10:]]).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        colA.move_to([-3.6, 0.0, 0])
        colB.move_to([3.6, 0.0, 0])
        colA.align_to([-6.9, 0, 0], LEFT)
        colB.align_to([0.4, 0, 0], LEFT)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in colA], lag_ratio=0.12), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in colB], lag_ratio=0.12), run_time=2.4)
        self.wait(3.0)
