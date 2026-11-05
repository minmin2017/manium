"""EPS10 ชุด d — ลัดวงจร, แรงดันเปลี่ยนตามโหลด, ขนาน, โครงสร้าง (หน้า 22-33)
P22_ShortCirc (22-24) · P24_Regulation (24-26) · P26_Parallel (26-29) · P30_Construction (30-33)
"""
from eps10_lib import *


# =============================================================== P22  หน้า 22-24
class P22_ShortCirc(Lesson):
    def construct(self):
        self.head("การทดสอบลัดวงจร (Short-circuit test)", "หน้า 22–24 · สมการ 1.53–1.58")
        self.say("ลัดวงจรทุติยภูมิ แล้วค่อยๆ เพิ่มแรงดันปฐมภูมิจนกระแส = กระแสพิกัด", color=OK)
        c = tee_circuit(x0=-5.6, y_top=1.3, y_bot=-0.7, labels=True, size=24, names=["R_1", "jX_{1\\sigma}", "jX_{2\\sigma}'", "R_2'", "V_{k}", "0", "jX_m", "R_c"])
        self.play(Create(c), run_time=1.6)
        p = c.parts
        sh = Line([5.6, 1.3, 0], [5.6, -0.7, 0], color=C_LOSS, stroke_width=8)
        self.play(Create(sh), run_time=0.6)
        self.say("แรงดันที่ใช้แค่ไม่กี่ % → ฟลักซ์น้อยมาก → ขาแม่เหล็กแทบไม่มีกระแส ตัดทิ้งได้", color=C_MAG)
        self.play(VGroup(p["xm"], p["rm"], p["br"], p["lab"][6], p["lab"][7]).animate.set_opacity(0.15), run_time=1.0)
        f = MathTex(r"Z_{k1}", r"\approx", r"(R_1+R_2')", "+", r"j\,(X_{1\sigma}+X_{2\sigma}')", font_size=40).move_to([0, -1.75, 0])
        f[2].set_color(C_LOSS)
        f[4].set_color(C_P)
        self.play(Write(f), run_time=1.2)
        self.glow(f[2], VGroup(p["r1"], p["r2"]), color=C_LOSS)
        self.glow(f[4], VGroup(p["x1"], p["x2"]), color=C_P)
        self.wait(1.0)
        self.clear()
        self.newpage("หน้า 23")
        self.say("แรงดันลัดวงจรแบบสัดส่วน vk% = แรงดันที่ทำให้กระแสพิกัดไหล เทียบแรงดันพิกัด", color=OK)
        v = MathTex(r"v_k\%=100\cdot\frac{Z_{k1}I_{n1}}{V_{1n}}\ =\ 100\,z_k", font_size=42, color=YEL).move_to([0, 1.3, 0])
        self.play(Write(v), run_time=1.0)
        tab = VGroup(Text("5 – 100 kVA :  vk = 3 – 5 %", font_size=26, color=WHITE),
                     Text("มากกว่า 1 MVA :  vk = 5 – 15 %", font_size=26, color=WHITE),
                     Text("เล็กมาก 50 – 500 VA :  vk = 5 – 15 % (ส่วน R สำคัญขึ้น)", font_size=24, color=GRAYTXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -0.3, 0])
        self.play(FadeIn(tab), run_time=1.0)
        self.wait(1.5)
        self.clear()
        self.say("ตัวอย่าง (ตัวเลขสมมติ ไม่ได้มาจาก PDF): ป้อนด้านแรงสูง กระแสพิกัด 10 A วัดได้ 60 V, 300 W", color=YEL)
        bd = Board(self, x=-6.6, y=2.1, gap=0.12)
        bd.add(1, "เข้าใจ: วัตต์มิเตอร์อ่านสูญเสียทองแดง", n_text("แกนแทบไม่มีฟลักซ์ → P ที่วัด = I²(R1 + R2')", size=22), hold=0.9)
        bd.add(2, "อิมพีแดนซ์รวม", MathTex(r"Z_{eq}=V/I=60/10=6\ \Omega", font_size=32), hold=0.8)
        bd.add(3, "แยก R, X", VGroup(MathTex(r"R_{eq}=P/I^2=300/10^2=3\ \Omega", font_size=32, color=C_LOSS),
                                   MathTex(r"X_{eq}=\sqrt{6^2-3^2}=5.2\ \Omega", font_size=32, color=C_P)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
               run=1.6, hold=0.9)
        bd.add(4, "แบ่งให้ 2 ขด (หน้า 24)", n_text("แยกจริงไม่ได้ → แบ่งครึ่ง: R1 = R2' = 1.5 Ω , X1 = X2' = 2.6 Ω", size=22, color=OK), hold=1.4)
        self.wait(1.0)
        remember(self, "3 การทดสอบ: วัด DC (ได้ R) · ไม่มีโหลด (Rc, Xm) · ลัดวงจร (Req, Xeq)",
                 "ลัดวงจร: Z = V/I   R = P/I²   X = sqrt(Z² − R²)")


# =============================================================== P24  หน้า 24-26
class P24_Regulation(Lesson):
    def construct(self):
        self.head("แรงดันเปลี่ยนเมื่อมีโหลด (Voltage regulation)", "หน้า 24–26 · รูป 10-18, 10-19")
        self.say("มองจากโหลด: แหล่ง V20 (แรงดันไม่มีโหลด) อนุกรม Zk = Rk + jXk", color=OK)
        O = np.array([-5.4, -1.2, 0])
        S = 7.0
        rk, xk = 0.04, 0.12     # ขนาดแสดงผล (ขยายให้เห็น)
        ph = ValueTracker(37 * DEGREES)

        def build():
            p = ph.get_value()
            v2 = O + RIGHT * S * 1.0
            i = np.array([np.cos(-p), np.sin(-p), 0])
            ri = rk * S * i
            xi = xk * S * np.array([-i[1], i[0], 0])
            a_v2 = Arrow(O, v2, buff=0, color=OK, stroke_width=5, tip_length=0.2)
            a_i = Arrow(O, O + 1.6 * i, buff=0, color=C_IA, stroke_width=4, tip_length=0.16)
            a_r = Arrow(v2, v2 + ri, buff=0, color=C_LOSS, stroke_width=4, tip_length=0.12, max_tip_length_to_length_ratio=0.5)
            a_x = Arrow(v2 + ri, v2 + ri + xi, buff=0, color=C_P, stroke_width=4, tip_length=0.15, max_tip_length_to_length_ratio=0.4)
            a_v20 = Arrow(O, v2 + ri + xi, buff=0, color=YEL, stroke_width=5, tip_length=0.2)
            return VGroup(a_v2, a_i, a_r, a_x, a_v20)
        dia = always_redraw(build)
        self.add(dia)
        lv2 = MathTex("V_2", font_size=30, color=OK).move_to(O + RIGHT * 3.5 + DOWN * 0.3)
        li = MathTex("I", font_size=30, color=C_IA).move_to(O + RIGHT * 0.7 + DOWN * 1.05)
        lv20 = MathTex("V_{20}", font_size=30, color=YEL).move_to(O + RIGHT * 3.4 + UP * 0.75)
        lrx = MathTex(r"R_kI\ ,\ jX_kI", font_size=26, color=C_P).move_to(O + RIGHT * 7.95 + UP * 1.4)
        self.play(FadeIn(lv2), FadeIn(li), FadeIn(lv20), FadeIn(lrx), run_time=0.8)
        rd = always_redraw(lambda: MathTex(r"|V_{20}|-|V_2|=%+.2f\ \text{(scaled)}" % (
            np.linalg.norm(np.array([1 + rk * np.cos(ph.get_value()) + xk * np.sin(ph.get_value()),
                                     -rk * np.sin(ph.get_value()) + xk * np.cos(ph.get_value())])) - 1), font_size=30, color=WHITE).move_to([2.6, 1.9, 0]))
        tg = always_redraw(lambda: Text("โหลดอินดักทีฟ (ล้าหลัง) → V2 ตก" if ph.get_value() > 0.05 else
                                        ("โหลดคาปาซิทีฟ (นำหน้า) → V2 สูงขึ้น" if ph.get_value() < -0.05 else "โหลด R ล้วน"),
                                        font_size=24, color=C_IA).move_to([2.6, 1.3, 0]))
        self.add(rd, tg)
        self.say("โหลดอินดักทีฟ: jXk I ชี้ขึ้นแรง → V20 ยาวกว่า V2 มาก = แรงดันตก", color=C_IA)
        self.wait(2.0)
        self.say("ค่อยๆ เปลี่ยนเป็นโหลดคาปาซิทีฟ: jXk I เอียงลง → V2 อาจสูงกว่า V20", color=C_IA)
        self.play(ph.animate.set_value(-37 * DEGREES), run_time=4.0)
        self.wait(1.5)
        for m in (dia, rd, tg):
            m.clear_updaters()
        self.clear()
        # ---- สูตร + ตัวอย่าง
        self.newpage("หน้า 25–26 · สมการ 1.62")
        self.say("สูตรต่อหน่วย (ใช้ได้เมื่อ zk < 0.05):  I = iw + j ib  (ib < 0 สำหรับโหลดล้าหลัง)", color=OK)
        f = MathTex(r"\Delta v_2", "=", r"(r_k i_w - x_k i_b)", "+", r"\tfrac12(x_k i_w + r_k i_b)^2", font_size=40).move_to([0, 1.6, 0])
        f[2].set_color(C_LOSS)
        f[4].set_color(C_P)
        self.play(Write(f), run_time=1.4)
        self.glow(f[2], None, color=C_LOSS)
        self.say("ตัวอย่าง (ตัวเลขสมมติ): rk = 0.01  xk = 0.05  กระแสพิกัด PF 0.8 ล้าหลัง", color=YEL)
        bd = Board(self, x=-6.6, y=0.95, gap=0.1)
        bd.add(1, "แยกกระแส", MathTex(r"i_w=0.8\qquad i_b=-0.6", font_size=32), hold=0.7)
        bd.add(2, "แทนค่า", VGroup(MathTex(r"a=0.01(0.8)-0.05(-0.6)=0.038", font_size=30, color=C_LOSS),
                                  MathTex(r"b=0.05(0.8)+0.01(-0.6)=0.034\ \Rightarrow\ \tfrac12b^2=0.00058", font_size=30, color=C_P)
                                  ).arrange(DOWN, aligned_edge=LEFT, buff=0.1), run=1.8, hold=0.8)
        bd.add(3, "ผล + ตรวจ", n_text("Δv = 0.0386 → แรงดันตก 3.86 %   (PF 0.8 นำหน้า: ib = +0.6 → Δv = −2.09 % แรงดันขึ้น)", size=21, color=OK), hold=1.6)
        self.say("กรณีพิเศษ: มุมโหลด = มุมลัดวงจร (φ2 = φk) และกระแสพิกัด → Δv = zk", color=YEL)
        self.wait(1.5)
        remember(self, "อินดักทีฟ → แรงดันตก   คาปาซิทีฟ → แรงดันขึ้นได้",
                 "Δv ≈ (rk iw − xk ib) + ½(xk iw + rk ib)²")


# =============================================================== P26  หน้า 26-29
class P26_Parallel(Lesson):
    def construct(self):
        self.head("หม้อแปลงต่อขนาน", "หน้า 26–29 · รูป 10-20 ถึง 10-24")
        self.say("หม้อแปลง A และ B รับไฟจากบัสเดียวกัน จ่ายโหลดเดียวกัน", color=OK)
        top = Line([-5.5, 2.0, 0], [-0.5, 2.0, 0], color=WHITE, stroke_width=5)
        bot = Line([-5.5, -1.6, 0], [-0.5, -1.6, 0], color=WHITE, stroke_width=5)
        xa = VGroup(Circle(radius=0.4, color=WHITE).move_to([-4.2, 0.45, 0]), Circle(radius=0.4, color=WHITE).move_to([-4.2, -0.05, 0]))
        xb = VGroup(Circle(radius=0.4, color=WHITE).move_to([-1.8, 0.45, 0]), Circle(radius=0.4, color=WHITE).move_to([-1.8, -0.05, 0]))
        ws = VGroup(wire((-4.2, 2.0), (-4.2, 0.85)), wire((-4.2, -0.45), (-4.2, -1.6)), wire((-1.8, 2.0), (-1.8, 0.85)), wire((-1.8, -0.45), (-1.8, -1.6)))
        ta = Text("A", font_size=26, color=C_P).move_to([-4.95, 0.2, 0])
        tb = Text("B", font_size=26, color=C_SEC).move_to([-1.05, 0.2, 0])
        self.play(Create(top), Create(bot), Create(ws), FadeIn(xa), FadeIn(xb), FadeIn(ta), FadeIn(tb), run_time=1.2)
        f = MathTex(r"I_{2LA}", "=", r"\frac{V_{20A}-V_{20B}}{Z_{kA}+Z_{kB}}", "+", r"I_L\frac{Z_{kB}}{Z_{kA}+Z_{kB}}", font_size=34).move_to([3.4, 1.0, 0])
        f[2].set_color(C_LOSS)
        f[4].set_color(OK)
        self.play(Write(f), run_time=1.4)
        t1 = Text("กระแสหมุนเวียน (ไม่ต้องการ)", font_size=19, color=C_LOSS).next_to(f[2], DOWN, buff=0.25)
        t2 = Text("ส่วนแบ่งโหลด", font_size=19, color=OK).next_to(f[4], DOWN, buff=0.25)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
        self.say("เงื่อนไข 1: อัตราส่วนรอบเท่ากัน → V20A = V20B → กระแสหมุนเวียน = 0", color=C_LOSS)
        self.glow(f[2], VGroup(xa, xb), color=C_LOSS)
        self.say("เงื่อนไข 2: โหลดแบ่งตามส่วนกลับ Zk → ตัวที่ Zk เล็กกว่ารับโหลดมากกว่า", color=OK)
        self.glow(f[4], None, color=OK)
        self.wait(1.0)
        self.clear()
        self.say("ตัวอย่าง (ตัวเลขสมมติ): พิกัดเท่ากัน  zkA = 0.04  zkB = 0.06 p.u.  มุมเท่ากัน", color=YEL)
        bd = Board(self, x=-6.6, y=2.1, gap=0.12)
        bd.add(1, "ส่วนแบ่งของ A", MathTex(r"\frac{z_{kB}}{z_{kA}+z_{kB}}=\frac{0.06}{0.10}=60\%", font_size=34, color=C_P), hold=0.7)
        bd.add(2, "ส่วนแบ่งของ B", MathTex(r"\frac{0.04}{0.10}=40\%", font_size=34, color=C_SEC), hold=0.7)
        ba = Rectangle(width=0.8, height=2.4, stroke_color=C_P, fill_color=C_P, fill_opacity=0.6).move_to([3.0, -0.6, 0], aligned_edge=DOWN)
        bb = Rectangle(width=0.8, height=1.6, stroke_color=C_SEC, fill_color=C_SEC, fill_opacity=0.6).move_to([4.6, -0.6, 0], aligned_edge=DOWN)
        lim = DashedLine([2.3, 1.4, 0], [5.3, 1.4, 0], color=GRAYTXT)
        la = Text("A 60%", font_size=20, color=C_P).next_to(ba, DOWN, buff=0.15)
        lb = Text("B 40%", font_size=20, color=C_SEC).next_to(bb, DOWN, buff=0.15)
        self.play(GrowFromEdge(ba, DOWN), GrowFromEdge(bb, DOWN), FadeIn(la), FadeIn(lb), run_time=1.0)
        bd.add(3, "ตรวจ", n_text("A รับเกิน 50% → ถ้าโหลดเต็ม 2 เท่าพิกัด A จะเกินพิกัดก่อน\nแก้: zk (p.u.) ต้องเท่ากัน จึงแบ่งตามพิกัดได้", size=20, color=OK), hold=1.6)
        self.wait(1.0)
        self.say("เงื่อนไข 3: มุมของ Zk เท่ากัน ไม่งั้นกระแส 2 ตัวรวมแบบเวกเตอร์ ขนาดรวมเกิน IL สูญเสียเพิ่ม (รูป 10-24)", color=GRAYTXT)
        self.wait(1.6)
        remember(self, "ขนานได้ดี: อัตราส่วนเท่ากัน + zk p.u. เท่ากัน + มุม zk เท่ากัน",
                 "(3 เฟสเพิ่ม: กลุ่มเวกเตอร์และลำดับเฟสต้องตรงกัน)  พิกัดไม่ควรต่างกันมาก")


# =============================================================== P30  หน้า 30-33
class P30_Construction(Lesson):
    def construct(self):
        self.head("โครงสร้าง: core vs shell, แกน 3 เฟส, ชนิดขดลวด", "หน้า 30–33 · รูป 10-25 ถึง 10-29")
        self.say("1 เฟสแบบ core: ขดล้อมแกน 2 ขา  |  แบบ shell: แกนล้อมขด ขดอยู่ขากลาง", color=OK)
        cc = Rectangle(width=2.6, height=2.4, stroke_color=METAL, stroke_width=16).move_to([-3.6, 0.1, 0])
        ccl = VGroup(*[Rectangle(width=0.35, height=1.4, stroke_color=c, fill_color=c, fill_opacity=0.6).move_to([x, 0.1, 0])
                       for x, c in ((-5.15, C_P), (-4.65, C_SEC), (-2.55, C_SEC), (-2.05, C_P))])
        sh = VGroup(Rectangle(width=3.0, height=2.4, stroke_color=METAL, stroke_width=16).move_to([3.4, 0.1, 0]),
                    Line([3.4, 1.3, 0], [3.4, -1.1, 0], color=METAL, stroke_width=26))
        shc = VGroup(*[Rectangle(width=0.32, height=1.4, stroke_color=c, fill_color=c, fill_opacity=0.6).move_to([x, 0.1, 0])
                       for x, c in ((2.85, C_SEC), (3.0, C_P), (3.8, C_P), (3.95, C_SEC))])
        l1 = Text("core type", font_size=24, color=GRAYTXT).move_to([-3.6, -1.65, 0])
        l2 = Text("shell type", font_size=24, color=GRAYTXT).move_to([3.4, -1.65, 0])
        self.play(Create(cc), FadeIn(ccl), FadeIn(l1), run_time=1.0)
        self.play(Create(sh), FadeIn(shc), FadeIn(l2), run_time=1.0)
        self.wait(1.2)
        self.clear()
        self.newpage("หน้า 30–31 · รูป 10-26, 10-27")
        self.say("3 เฟส: เอาหม้อแปลง 1 เฟส 3 ตัวมารวมขา → ฟลักซ์ 3 เฟสรวมกัน = 0 → ตัดขารวมทิ้งได้", color=OK)
        cols = (C_LOSS, OK, C_S)
        legs = VGroup(*[Rectangle(width=0.4, height=2.4, stroke_color=METAL, fill_color=METAL, fill_opacity=0.4).move_to([x, 0.0, 0]) for x in (-2.0, 0.0, 2.0)])
        yk = VGroup(Rectangle(width=4.4, height=0.35, stroke_color=METAL, fill_color=METAL, fill_opacity=0.4).move_to([0, 1.37, 0]),
                    Rectangle(width=4.4, height=0.35, stroke_color=METAL, fill_color=METAL, fill_opacity=0.4).move_to([0, -1.37, 0]))
        cl = VGroup(*[Rectangle(width=0.75, height=1.5, stroke_color=c, fill_color=c, fill_opacity=0.35).move_to([x, 0.0, 0]) for x, c in zip((-2.0, 0.0, 2.0), cols)])
        self.play(FadeIn(legs), FadeIn(yk), FadeIn(cl), run_time=1.0)
        fs = MathTex(r"\varphi_U+\varphi_V+\varphi_W=0", font_size=36, color=C_PHI).move_to([0, -2.1, 0])
        self.play(Write(fs), run_time=1.0)
        t = Text("core 3 ขา (ขากลางทางแม่เหล็กสั้นกว่าเล็กน้อย)", font_size=21, color=GRAYTXT).move_to([0, 2.05, 0])
        self.play(FadeIn(t), run_time=0.5)
        self.wait(1.2)
        self.say("แบบ 5 ขา / shell 3 เฟส: มีขากลับในเหล็ก ให้ฟลักซ์ที่ผลรวมไม่เป็นศูนย์ (ไม่สมมาตร) วิ่งได้", color=OK)
        ex = VGroup(Rectangle(width=0.3, height=2.4, stroke_color=YEL, fill_color=YEL, fill_opacity=0.3).move_to([-3.3, 0, 0]),
                    Rectangle(width=0.3, height=2.4, stroke_color=YEL, fill_color=YEL, fill_opacity=0.3).move_to([3.3, 0, 0]))
        self.play(FadeIn(ex), run_time=0.8)
        self.wait(1.2)
        self.clear()
        self.newpage("หน้า 32–33 · รูป 10-28, 10-29")
        self.say("ชนิดขดลวด: ทรงกระบอก (LV)  ดิสก์/แพนเค้ก (HV พิกัดสูง)  ฟอยล์ (LV)", color=OK)
        cy = VGroup(Rectangle(width=0.5, height=2.4, stroke_color=C_SEC, fill_color=C_SEC, fill_opacity=0.5).move_to([-4.6, 0, 0]),
                    Rectangle(width=0.5, height=2.4, stroke_color=C_P, fill_color=C_P, fill_opacity=0.5).move_to([-3.9, 0, 0]))
        dk = VGroup(*[Rectangle(width=1.1, height=0.24, stroke_color=(C_P if i % 2 else C_SEC), fill_color=(C_P if i % 2 else C_SEC), fill_opacity=0.6).move_to([0, -1.0 + i * 0.33, 0]) for i in range(7)])
        fo = VGroup(*[Circle(radius=0.25 + 0.12 * i, stroke_color=(C_P if i % 2 else METAL), stroke_width=3).move_to([4.2, 0, 0]) for i in range(6)])
        n1 = Text("ทรงกระบอก (LV)", font_size=21, color=GRAYTXT).move_to([-4.25, -1.65, 0])
        n2 = Text("ดิสก์ (HV)", font_size=21, color=GRAYTXT).move_to([0, -1.65, 0])
        n3 = Text("ฟอยล์ (LV)", font_size=21, color=GRAYTXT).move_to([4.2, -1.65, 0])
        self.play(FadeIn(cy), FadeIn(n1), run_time=0.7)
        self.play(FadeIn(dk), FadeIn(n2), run_time=0.7)
        self.play(Create(fo), FadeIn(n3), run_time=0.9)
        self.say("ดิสก์สลับปฐมภูมิ–ทุติยภูมิ: ปรับค่ารั่วได้ และทนแรงดันเกินจากฟ้าผ่าดีกว่า", color=GRAYTXT)
        self.wait(1.6)
        remember(self, "core = ขดล้อมแกน   shell = แกนล้อมขด   3 ขา: φU + φV + φW = 0",
                 "LV ใช้ขดทรงกระบอก/ฟอยล์   HV ใช้ขดดิสก์")
