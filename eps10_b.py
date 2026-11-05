"""EPS10 ชุด b — สมการหม้อแปลง (หน้า 3-9)
P03_Flux (3-4) · P05_Induct (5-6) · P07_EqCircuit (7-8) · P08_Referred (8-9)
"""
from eps10_lib import *


def flux_pic(cx=3.4, cy=0.2, s=1.0):
    """แกน + ขด 2 ขด + ฟลักซ์หลัก (ในแกน) + ฟลักซ์รั่ว (วงนอกแกน รอบขดตัวเอง)"""
    w, h = 3.0 * s, 2.3 * s
    core = Rectangle(width=w, height=h, stroke_color=METAL, stroke_width=20 * s).move_to([cx, cy, 0])
    L, R = cx - w / 2, cx + w / 2

    def coil(x, color):
        return VGroup(*[Ellipse(width=0.62 * s, height=0.15 * s, stroke_color=color, stroke_width=4).move_to([x, cy - 0.5 * s + i * 0.25 * s, 0])
                        for i in range(5)])
    c1, c2 = coil(L, C_P), coil(R, C_SEC)
    main = Rectangle(width=w, height=h, stroke_color=C_PHI, stroke_width=4).move_to([cx, cy, 0])
    ma = Arrow([cx - 0.35, cy + h / 2, 0], [cx + 0.35, cy + h / 2, 0], buff=0, color=C_PHI, stroke_width=4, tip_length=0.16)
    lk1 = Ellipse(width=0.75 * s, height=1.5 * s, stroke_color=C_P, stroke_width=3).move_to([L - 0.05 * s, cy, 0])
    lk1 = DashedVMobject(lk1, num_dashes=18)
    lk2 = DashedVMobject(Ellipse(width=0.75 * s, height=1.5 * s, stroke_color=C_SEC, stroke_width=3).move_to([R + 0.05 * s, cy, 0]), num_dashes=18)
    lm = MathTex(r"\varphi_m", font_size=30, color=C_PHI).move_to([cx, cy + h / 2 - 0.4, 0])
    l1 = MathTex(r"\varphi_{1\sigma}", font_size=28, color=C_P).move_to([L - 0.85 * s, cy + 0.95 * s, 0])
    l2 = MathTex(r"\varphi_{2\sigma}", font_size=28, color=C_SEC).move_to([R + 0.85 * s, cy + 0.95 * s, 0])
    n1 = MathTex(r"w_1", font_size=26, color=C_P).move_to([L, cy - h / 2 - 0.4, 0])
    n2 = MathTex(r"w_2", font_size=26, color=C_SEC).move_to([R, cy - h / 2 - 0.4, 0])
    g = VGroup(core, c1, c2, n1, n2)
    g.core, g.c1, g.c2, g.main, g.ma, g.lk1, g.lk2, g.lm, g.l1, g.l2 = core, c1, c2, main, ma, lk1, lk2, lm, l1, l2
    return g


# =============================================================== P03  หน้า 3-4
class P03_Flux(Lesson):
    def construct(self):
        self.head("ฟลักซ์หลัก vs ฟลักซ์รั่ว", "หน้า 3–4 · รูป 10-2")
        self.say("จ่ายไฟให้ขดปฐมภูมิ → เกิดฟลักซ์ φ1 คล้องขด 1   ฟลักซ์คล้อง Ψ = (จำนวนรอบ) × φ", color=OK)
        g = flux_pic(3.4, 0.15)
        self.play(FadeIn(g), run_time=1.0)
        self.say("ฟลักซ์แบ่งเป็น 2 ส่วน: ฟลักซ์หลัก φm วิ่งในแกน คล้องทั้ง 2 ขด", color=C_PHI)
        self.play(Create(g.main), GrowArrow(g.ma), FadeIn(g.lm), run_time=1.0)
        self.play(flow(g.main, C_PHI, run=1.2, width=8), run_time=1.2)
        self.say("ฟลักซ์รั่ว φ1σ หลุดออกนอกแกน คล้องขดตัวเองขดเดียว (ไม่ถึงอีกขด)", color=C_P)
        self.play(Create(g.lk1), FadeIn(g.l1), run_time=1.0)
        self.play(Create(g.lk2), FadeIn(g.l2), run_time=0.8)
        f = MathTex(r"\Psi_1", "=", r"w_1\varphi_{1\sigma}", "+", r"w_1\varphi_m", font_size=40).move_to([-3.4, 1.0, 0])
        f[2].set_color(C_P)
        f[4].set_color(C_PHI)
        self.play(Write(f), run_time=1.2)
        self.glow(f[4], g.main, color=C_PHI)
        self.glow(f[2], g.lk1, color=C_P)
        f2 = MathTex(r"e_2", "=", r"w_2\,\frac{d\varphi_m}{dt}", font_size=40).move_to([-3.4, -0.4, 0])
        f2[2].set_color(C_PHI)
        self.say("ขดทุติยภูมิได้แรงดันจากฟลักซ์หลักเท่านั้น  ฟลักซ์รั่วเหนี่ยวนำแค่ขดตัวเอง", color=OK)
        self.play(Write(f2), run_time=1.0)
        self.glow(f2[2], VGroup(g.main, g.c2), color=C_PHI)
        self.wait(1.0)
        k = self.keytext("φ1 = φ1σ + φm   (รั่ว + หลัก)   หม้อแปลงดี: φm ใหญ่มาก φσ น้อย", hold=1.8)
        self.clear()
        # ---- หน้า 4
        self.newpage("หน้า 4 · สมการ 1.3–1.11")
        self.say("กฎแอมแปร์: แรงเคลื่อนแม่เหล็ก (mmf) รวมของ 2 ขด สร้างฟลักซ์หลัก", color=OK)
        a = MathTex(r"\varphi_m", r"\,\Re_m", "=", r"w_1i_1", "+", r"w_2i_2", font_size=42).move_to([0, 1.3, 0])
        a[0].set_color(C_PHI)
        a[1].set_color(METAL)
        a[3].set_color(C_P)
        a[5].set_color(C_SEC)
        self.play(Write(a), run_time=1.2)
        an = Text("เหมือนกฎของโอห์ม:  ฟลักซ์ × ความต้านทานแม่เหล็ก = mmf  (V = I R)", font_size=22, color=GRAYTXT).move_to([0, 0.4, 0])
        self.play(FadeIn(an), run_time=0.6)
        rm = MathTex(r"\Re_m=\frac{l_m}{\mu_0\mu_r\Sigma_m}\qquad \mu_0=4\pi\times10^{-7}\ H/m", font_size=32, color=METAL).move_to([0, -0.5, 0])
        self.play(Write(rm), run_time=1.0)
        self.glow(rm, None, color=METAL)
        self.wait(1.0)
        self.say("แรงดันที่จ่าย = ตกที่ความต้านทานขด + ตกที่ฟลักซ์รั่ว + แรงเคลื่อนจากฟลักซ์หลัก", color=YEL)
        self.play(FadeOut(VGroup(an, rm)), a.animate.scale(0.8).move_to([0, 1.55, 0]), run_time=0.6)
        v = MathTex(r"v_1", "=", r"R_1i_1", "+", r"w_1\frac{d\varphi_{1\sigma}}{dt}", "+", r"e_1", font_size=44).move_to([0, 0.2, 0])
        v[0].set_color(YEL)
        v[2].set_color(C_LOSS)
        v[4].set_color(C_P)
        v[6].set_color(C_PHI)
        self.play(Write(v), run_time=1.4)
        t1 = Text("ความต้านทานลวด", font_size=20, color=C_LOSS).next_to(v[2], DOWN, buff=0.45)
        t2 = Text("ฟลักซ์รั่ว", font_size=20, color=C_P).next_to(v[4], DOWN, buff=0.3)
        t3 = Text("ฟลักซ์หลัก", font_size=20, color=C_PHI).next_to(v[6], DOWN, buff=0.45)
        for term, t, c in ((v[2], t1, C_LOSS), (v[4], t2, C_P), (v[6], t3, C_PHI)):
            self.play(Indicate(term, color=WHITE), FadeIn(t), run_time=0.8)
        self.wait(1.2)
        remember(self, "ฟลักซ์หลัก = ส่งพลังงานข้ามขด   ฟลักซ์รั่ว = แค่ทำแรงดันตก",
                 "v1 = R1 i1 + (ตกที่ฟลักซ์รั่ว) + e1")


# =============================================================== P05  หน้า 5-6
class P05_Induct(Lesson):
    def construct(self):
        self.head("อัตราส่วนแรงดัน + กระแสแม่เหล็ก", "หน้า 5–6 · สมการ 1.12–1.21")
        self.say("ฟลักซ์หลักตัวเดียวกัน ผ่านขด w1 รอบ และ w2 รอบ", color=OK)
        g = flux_pic(3.6, 0.1, s=0.85)
        self.play(FadeIn(g), Create(g.main), GrowArrow(g.ma), FadeIn(g.lm), run_time=1.0)
        self.play(flow(g.main, C_PHI, run=1.2, width=8), run_time=1.2)
        e = VGroup(MathTex(r"e_1=w_1\frac{d\varphi_m}{dt}", font_size=36, color=C_P),
                   MathTex(r"e_2=w_2\frac{d\varphi_m}{dt}", font_size=36, color=C_SEC)).arrange(DOWN, buff=0.35).move_to([-3.4, 1.0, 0])
        self.play(Write(e), run_time=1.4)
        self.say("หารกัน: dφm/dt ตัดกันหมด เหลือแค่จำนวนรอบ", color=YEL)
        r = MathTex(r"\frac{e_1}{e_2}=\frac{w_1}{w_2}", font_size=48, color=YEL).move_to([-3.4, -1.0, 0])
        self.play(Write(r), run_time=1.0)
        self.glow(r, VGroup(g.c1, g.c2), color=YEL)
        self.wait(1.0)
        self.clear()
        self.say("ตัวเหนี่ยวนำ: L = (จำนวนรอบ)² × Λ  (Λ = ความซึมซาบของทางแม่เหล็ก)", color=OK)
        l = VGroup(MathTex(r"L_{1\sigma}=w_1^2\Lambda_{1\sigma}", font_size=34, color=C_P),
                   MathTex(r"L_{m1}=w_1^2\Lambda_m", font_size=34, color=C_PHI)).arrange(RIGHT, buff=1.2).move_to([0, 1.5, 0])
        self.play(Write(l), run_time=1.2)
        e1 = MathTex(r"e_1", "=", r"L_{m1}\frac{d}{dt}", r"\Big[\,i_1+\frac{w_2}{w_1}i_2\Big]", font_size=40).move_to([0, 0.35, 0])
        e1[3].set_color(C_IA)
        self.play(Write(e1), run_time=1.2)
        self.say("วงเล็บนี้คือ กระแสแม่เหล็ก im1 = กระแสที่เหลือไว้สร้างฟลักซ์จริงๆ", color=C_IA)
        self.glow(e1[3], None, color=C_IA)
        # ภาพ: i1 กับ (w2/w1) i2 หักล้างกัน เหลือ im เล็กนิดเดียว
        y = -1.2
        a1 = Arrow([-4.0, y, 0], [2.0, y, 0], buff=0, color=C_P, stroke_width=6, tip_length=0.22)
        a2 = Arrow([2.0, y - 0.45, 0], [-3.6, y - 0.45, 0], buff=0, color=C_SEC, stroke_width=6, tip_length=0.22)
        am = Arrow([-4.0, y - 0.95, 0], [-3.6, y - 0.95, 0], buff=0, color=C_IA, stroke_width=6, tip_length=0.15, max_tip_length_to_length_ratio=0.5)
        t1 = MathTex(r"i_1", font_size=30, color=C_P).next_to(a1, RIGHT, buff=0.15)
        t2 = MathTex(r"\frac{w_2}{w_1}i_2", font_size=30, color=C_SEC).next_to(a2.get_start(), RIGHT, buff=0.15)
        t3 = MathTex(r"i_{m1}\ \text{(small)}", font_size=28, color=C_IA).next_to(am, RIGHT, buff=0.2)
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.7)
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.7)
        self.play(GrowArrow(am), FadeIn(t3), run_time=0.7)
        self.say("หม้อแปลงดี im ≈ 0  →  i2 ≈ −(w1/w2) i1   กระแสเป็นส่วนกลับของรอบ (ทิศตรงข้าม)", color=YEL)
        self.wait(2.0)
        self.clear()
        self.newpage("หน้า 6 · สมการ 1.20–1.21")
        self.say("ไฟ AC ไซน์ → เขียนเป็นเฟสเซอร์ (d/dt กลายเป็น jω)", color=OK)
        ph = MathTex(r"V_1", "=", r"R_1I_1", "+", r"jX_{1\sigma}I_1", "+", r"E_1", font_size=46).move_to([0, 1.0, 0])
        ph[0].set_color(YEL)
        ph[2].set_color(C_LOSS)
        ph[4].set_color(C_P)
        ph[6].set_color(C_PHI)
        self.play(Write(ph), run_time=1.2)
        ph2 = MathTex(r"E_1=jX_{m1}\Big[I_1+\frac{w_2}{w_1}I_2\Big]\qquad E_2=\frac{w_2}{w_1}E_1", font_size=36).move_to([0, -0.3, 0])
        self.play(Write(ph2), run_time=1.2)
        xs = MathTex(r"X=\omega L\ ,\quad \omega=2\pi f", font_size=32, color=GRAYTXT).move_to([0, -1.4, 0])
        self.play(FadeIn(xs), run_time=0.6)
        self.wait(1.5)
        remember(self, "e1/e2 = w1/w2   และ   im1 = i1 + (w2/w1) i2 ≈ 0",
                 "แรงดันตามรอบ  กระแสสวนรอบ  เพราะฟลักซ์หลักตัวเดียวกัน")


# =============================================================== P07  หน้า 7-8
class P07_EqCircuit(Lesson):
    def construct(self):
        self.head("วงจรสมมูล = หม้อแปลงอุดมคติ + ชิ้นส่วนแฝง", "หน้า 7–8 · รูป 10-3, 10-4")
        self.say("สร้างวงจรทีละชิ้น จากสมการ V1 = R1 I1 + jX1σ I1 + E1", color=OK)
        c = tee_circuit(x0=-5.6, y_top=0.9, y_bot=-1.1, labels=True, size=26)
        p = c.parts
        lab = p["lab"]
        self.play(Create(p["top"]), Create(p["bot"]), FadeIn(c[-2]), run_time=0.8)
        self.play(FadeIn(lab[4]), FadeIn(lab[5]), run_time=0.4)
        steps = [("r1", 0, "R1: ความต้านทานลวดปฐมภูมิ → สูญเสียทองแดง I²R", C_LOSS),
                 ("x1", 1, "jX1σ: ฟลักซ์รั่วปฐมภูมิ → แรงดันตก (ไม่สูญเสียกำลังจริง)", C_P),
                 ("xm", 6, "jXm: สร้างฟลักซ์หลัก (กระแสแม่เหล็ก Im ล้าหลัง 90°)", C_MAG),
                 ("rm", 7, "Rc (Rm1): สูญเสียในแกน = กระแสไหลวน + ฮิสเตอรีซิส", C_LOSS),
                 ("x2", 2, "jX2σ: ฟลักซ์รั่วทุติยภูมิ", C_SEC),
                 ("r2", 3, "R2: ความต้านทานลวดทุติยภูมิ", C_SEC)]
        for key, li, txt, col in steps:
            self.say(txt, color=col)
            extra = [Create(p["br"])] if key == "xm" else []
            self.play(Create(p[key]), FadeIn(lab[li]), *extra, run_time=0.8)
            self.play(Indicate(p[key], color=col, scale_factor=1.15), run_time=0.6)
        ib = DashedVMobject(Rectangle(width=0.62, height=2.4, stroke_color=WHITE, stroke_width=2).move_to([-5.6 + 0.6 * 11.2, -0.1, 0]), num_dashes=24)
        it = Text("หม้อแปลงอุดมคติ w1 : w2 อยู่ตรงนี้ (รูป 10-3)", font_size=19, color=GRAYTXT).move_to([1.1, -1.65, 0])
        self.say("ตรงกลางคือหม้อแปลงอุดมคติ: E1/E2 = w1/w2  ไม่มีสูญเสียใดๆ", color=OK)
        self.play(Create(ib), FadeIn(it), run_time=0.8)
        self.wait(1.2)
        k = self.keytext("หม้อแปลงจริง = หม้อแปลงอุดมคติ + R, X รั่ว (อนุกรม) + ขาแม่เหล็ก Xm // Rc (ขนาน)", hold=2.0)
        self.clear()
        # ---- รูป 10-4 เฟสเซอร์ไม่มีโหลด
        self.newpage("หน้า 7–8 · รูป 10-4")
        self.say("ไม่มีโหลด: กระแส Io แยกเป็น Iv (เฟสเดียวกับ E1, สูญเสียแกน) + Im (ล้าหลัง 90°, สร้างฟลักซ์)", color=OK)
        v, ic, im, iphi = phasor_ix((0.6, -1.9), 3.6, 0.9, 3.0)
        lv = MathTex(r"E_1", font_size=30, color=YEL).next_to(v.get_end(), LEFT, buff=0.12)
        lic = MathTex(r"I_{v1}", font_size=28, color=C_LOSS).next_to(ic, LEFT, buff=0.12)
        lim = MathTex(r"I_{m1}", font_size=28, color=C_MAG).next_to(im, UP, buff=0.12)
        lip = MathTex(r"I_{o1}", font_size=28, color=C_IA).next_to(iphi.get_center(), DOWN + RIGHT, buff=0.06)
        self.play(GrowArrow(v), FadeIn(lv), run_time=0.7)
        self.play(GrowArrow(ic), FadeIn(lic), run_time=0.6)
        self.play(GrowArrow(im), FadeIn(lim), run_time=0.6)
        self.play(GrowArrow(iphi), FadeIn(lip), run_time=0.7)
        self.say("Io ล้าหลัง E1 น้อยกว่า 90° เพราะมีส่วนสูญเสีย Iv", color=C_IA)
        self.wait(1.2)
        self.say("สูญเสียแกน: กระแสไหลวน ∝ f²B²  (แก้ด้วยแผ่นเหล็กบางเคลือบ)  ฮิสเตอรีซิส ∝ f·B^β  β ≈ 1.6–2", color=C_LOSS)
        pd = MathTex(r"P_{dm}=\frac{E_1^2}{R_{m1}}", font_size=40, color=C_LOSS).move_to([-4.2, 0.2, 0])
        self.play(Write(pd), run_time=1.0)
        self.glow(pd, ic, color=C_LOSS)
        self.wait(1.5)
        remember(self, "อนุกรม = R + X รั่ว (ตก/ร้อนตามโหลด)   ขนาน = Xm // Rc (คงที่ ไม่ขึ้นกับโหลด)",
                 "Rc คิดสูญเสียแกน  Xm คิดกระแสสร้างฟลักซ์")


# =============================================================== P08  หน้า 8-9
class P08_Referred(Lesson):
    def construct(self):
        self.head("อ้างอิงค่าทุติยภูมิ → ปฐมภูมิ (Referred values)", "หน้า 8–9 · รูป 10-5, 10-6")
        self.say("ปัญหา: มีหม้อแปลงอุดมคติคั่นกลาง คำนวณวงจรยาก → ย้ายค่าทุกอย่างให้อยู่ด้านเดียว", color=OK)
        rules = VGroup(MathTex(r"V_2'", "=", r"a\,V_2", font_size=40),
                       MathTex(r"I_2'", "=", r"I_2/a", font_size=40),
                       MathTex(r"Z_2'", "=", r"a^2 Z_2", font_size=40)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-3.6, 0.4, 0])
        for r, c in zip(rules, (YEL, C_IA, C_SEC)):
            r[2].set_color(c)
        an = MathTex(r"a=\frac{w_1}{w_2}", font_size=40, color=WHITE).move_to([-3.6, -1.6, 0])
        self.play(Write(rules), FadeIn(an), run_time=1.6)
        self.say("ทำไม Z คูณ a² ?  เพราะกำลังสูญเสียต้องเท่าเดิม ไม่ว่าจะมองจากด้านไหน", color=YEL)
        chk = MathTex(r"I_2'^2 R_2'", "=", r"\Big(\frac{I_2}{a}\Big)^2", r"(a^2R_2)", "=", r"I_2^2R_2", font_size=40).move_to([2.9, 0.4, 0])
        chk[2].set_color(C_IA)
        chk[3].set_color(C_SEC)
        self.play(Write(chk), run_time=1.4)
        self.glow(chk[2], rules[1], color=C_IA)
        self.glow(chk[3], rules[2], color=C_SEC)
        cv = Text("a² ตัดกัน → กำลังเท่าเดิม ✓", font_size=22, color=OK).move_to([2.9, -0.5, 0])
        self.play(FadeIn(cv), run_time=0.6)
        self.wait(1.5)
        self.clear()
        # ---- ตัวอย่างจากข้อ 2
        self.say("ตัวอย่าง (ตัวเลขข้อ 2 หน้า 50): a = 2300/230 = 10  ย้าย Rs, Xs ไปด้านปฐมภูมิ", color=OK)
        bd = Board(self, x=-6.6, y=2.1, gap=0.14)
        bd.add(1, "เข้าใจ", n_text("ด้านทุติยภูมิ Rs = 0.00039 Ω  Xs = 0.0028 Ω   a = 10", size=22), hold=1.0)
        bd.add(2, "สูตร", MathTex(r"R_s'=a^2R_s\qquad X_s'=a^2X_s", font_size=34), hold=0.8)
        bd.add(3, "แทนค่า", VGroup(MathTex(r"R_s'=100\times0.00039=0.039\ \Omega", font_size=32, color=C_SEC),
                                  MathTex(r"X_s'=100\times0.0028=0.28\ \Omega", font_size=32, color=C_SEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
               run=1.8, hold=1.0)
        bd.add(4, "ตรวจ", n_text("ได้เท่ากับ Rp = 0.039 Ω และ Xp = 0.28 Ω พอดี → ขด 2 ข้างสมดุลกัน", size=22, color=OK), hold=1.6)
        self.wait(1.0)
        self.clear()
        # ---- รูป 10-6: ไม่มีหม้อแปลงอุดมคติแล้ว
        self.newpage("หน้า 9 · รูป 10-6")
        self.say("อ้างอิงแล้ว E2' = E1 → หม้อแปลงอุดมคติ 1:1 ตัดทิ้งได้ → วงจร T ต่อกันตรงๆ", color=OK)
        c = tee_circuit(x0=-5.6, y_top=0.9, y_bot=-1.1, labels=True, size=26)
        self.play(Create(c), run_time=2.0)
        self.glow(c.parts["lab"][3], VGroup(c.parts["r2"], c.parts["x2"]), color=C_SEC)
        pu = Text("ต่อหน่วย (10-4): ใช้ค่าพิกัดเป็นฐาน → ตัวเลขด้านปฐมภูมิ = ทุติยภูมิ ไม่ต้องคูณ a²", font_size=20, color=GRAYTXT).move_to([0, -2.0, 0])
        self.play(FadeIn(pu), run_time=0.6)
        self.wait(1.8)
        remember(self, "ข้ามไปฝั่งรอบมาก: V × a   I ÷ a   Z × a²",
                 "ตรวจได้เสมอ: กำลัง I²R เท่าเดิมทั้ง 2 ฝั่ง")
