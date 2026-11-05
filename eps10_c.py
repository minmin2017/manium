"""EPS10 ชุด c — ต่อหน่วย, มาตราส่วน, แกน, วงจร T/L, ไม่มีโหลด (หน้า 9-21)
P10_PerUnitScale (9-13) · P14_Core (14-17) · P18_TLCircuit (18-20) · P21_NoLoad (21)
"""
from eps10_lib import *


# =============================================================== P10  หน้า 9-13
class P10_PerUnitScale(Lesson):
    def construct(self):
        self.head("ค่าต่อหน่วย + กฎมาตราส่วน (หม้อแปลงเล็ก vs ใหญ่)", "หน้า 9–13 · รูป 10-7, 10-8")
        self.say("ค่าต่อหน่วย (p.u.) = ค่าจริง ÷ ค่าพิกัด  → หม้อแปลงทุกขนาดเทียบกันได้", color=OK)
        f = VGroup(MathTex(r"S_n=V_{1n}I_{1n}=V_{2n}I_{2n}", font_size=36, color=YEL),
                   MathTex(r"Z_n=\frac{V_n}{I_n}\qquad z=\frac{Z}{Z_n}", font_size=36, color=WHITE)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
        self.play(Write(f), run_time=1.6)
        t = Text("ใน p.u. ค่าด้านปฐมภูมิ = ด้านทุติยภูมิ (ไม่ต้องคูณ a² แล้ว)", font_size=22, color=GRAYTXT).move_to([0, -0.4, 0])
        self.play(FadeIn(t), run_time=0.6)
        self.wait(1.5)
        self.clear()
        # ---- มาตราส่วน
        self.newpage("หน้า 10–12 · สมการ 1.26–1.35")
        self.say("ใช้เส้นผ่านศูนย์กลางขดเฉลี่ย D เป็นตัวแทน 'ขนาด' หม้อแปลง", color=OK)
        Dt = ValueTracker(0.2)
        cx, cy = -3.6, -0.2

        def coil():
            r = 0.35 + 1.0 * (Dt.get_value() - 0.2) / 1.8
            return VGroup(Circle(radius=r, stroke_color=C_P, stroke_width=6).move_to([cx, cy, 0]),
                          Square(side_length=r * 1.05, stroke_color=METAL, stroke_width=3, fill_color=METAL, fill_opacity=0.3).move_to([cx, cy, 0]))
        cl = always_redraw(coil)
        dl = always_redraw(lambda: MathTex(r"D=%.1f\ m" % Dt.get_value(), font_size=34, color=C_P).move_to([cx, 2.0, 0]))
        self.add(cl, dl)
        rows = [("กำลัง", r"S\sim D^4", YEL), ("ความต้านทาน p.u.", r"r\simeq 0.004/D", C_LOSS),
                ("รีแอกแตนซ์รั่ว p.u.", r"x_\sigma\sim D", C_P), ("กระแสแม่เหล็ก p.u.", r"i_m=(0.02\ldots0.002)/D", C_MAG)]
        tab = VGroup()
        for i, (th, tx, c) in enumerate(rows):
            r = VGroup(Text(th, font_size=21, color=GRAYTXT), MathTex(tx, font_size=32, color=c)).arrange(RIGHT, buff=0.3)
            tab.add(r)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([2.6, 0.5, 0])
        for r in tab:
            self.play(FadeIn(r, shift=LEFT * 0.2), run_time=0.6)
        rv = always_redraw(lambda: MathTex(r"r=0.004/%.1f=%.3f" % (Dt.get_value(), 0.004 / Dt.get_value()), font_size=32, color=C_LOSS).move_to([2.6, -1.6, 0]))
        self.add(rv)
        self.say("ขยาย D จาก 0.2 → 2 m : กำลังโต 10⁴ เท่า  แต่ r ต่อหน่วยลดจาก 0.02 → 0.002", color=YEL)
        self.play(Dt.animate.set_value(2.0), run_time=3.5, rate_func=linear)
        self.wait(1.2)
        k = self.keytext("หม้อแปลงใหญ่ประสิทธิภาพสูงกว่า เพราะ r ต่อหน่วยเล็ก (r ~ 1/D)", hold=1.8)
        for m in (cl, dl, rv):
            m.clear_updaters()
        self.clear()
        # ---- ค่าเฉลี่ย + ที่มา
        self.newpage("หน้า 11–12")
        self.say("ค่าเฉลี่ยในเอกสาร (D เป็นเมตร)", color=OK)
        vals = VGroup(MathTex(r"A_n=5\cdot10^4\,D\ \ [A/m]", font_size=34, color=C_IA),
                      MathTex(r"K_n=25\,D\ \ [V/m]", font_size=34, color=YEL),
                      MathTex(r"S_n=A_nK_n=1.25\cdot10^6\,D^2\ \ [VA/m^2]", font_size=34, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.9, 0])
        self.play(Write(vals), run_time=1.8)
        bd = Board(self, x=-6.6, y=-0.6, gap=0.1)
        bd.add(1, "ตัวอย่าง: r ที่ D = 0.2 m และ 2 m", VGroup(MathTex(r"r=0.004/0.2=0.02", font_size=30, color=C_LOSS),
                                                          MathTex(r"r=0.004/2=0.002", font_size=30, color=C_LOSS)).arrange(RIGHT, buff=0.8), hold=1.4)
        self.wait(1.0)
        self.clear()
        # ---- รูป 10-8 พลังงานรั่ว
        self.newpage("หน้า 12–13 · รูป 10-8")
        self.say("ฟลักซ์รั่วอยู่ในช่องว่าง Δ ระหว่างขด 1 กับขด 2 → เก็บพลังงาน Wσ", color=OK)
        bars = VGroup()
        for x, c in ((-3.0, C_LOSS), (-2.2, C_S), (2.2, C_S), (3.0, C_LOSS)):
            bars.add(Rectangle(width=0.4, height=2.6, stroke_color=c, fill_color=c, fill_opacity=0.7).move_to([x, 0.0, 0]))
        core = Rectangle(width=2.8, height=2.6, stroke_color=METAL, fill_color=METAL, fill_opacity=0.2).move_to([0, 0, 0])
        gl = MathTex(r"\Delta", font_size=32, color=YEL).move_to([2.6, 1.65, 0])
        gap = DoubleArrow([2.4, 1.4, 0], [2.8, 1.4, 0], buff=0, color=YEL, stroke_width=2, tip_length=0.1)
        lk = VGroup(*[Line([-2.6, y, 0], [-2.6, y + 0.3, 0], color=C_PHI, stroke_width=3) for y in np.linspace(-1.1, 0.8, 6)])
        self.play(FadeIn(core), FadeIn(bars), run_time=0.8)
        self.play(Create(gap), FadeIn(gl), Create(lk), run_time=0.8)
        w = MathTex(r"W_\sigma=\tfrac12 H_\sigma^2\cdot(\text{volume})\ \sim D^5\ \Rightarrow\ x_\sigma\sim\frac{D^5}{D^4}=D", font_size=32).move_to([0, -2.0, 0])
        self.play(Write(w), run_time=1.4)
        self.say("ค่ารั่วต่อหน่วยทั่วไป 2×0.01 ถึง 2×0.1  ต้องมีไว้บ้างเพื่อจำกัดกระแสลัดวงจร", color=C_P)
        self.wait(2.0)
        remember(self, "ใหญ่ขึ้น: S ~ D⁴   r ~ 1/D (ดีขึ้น)   xσ ~ D (รั่วมากขึ้น)",
                 "r ≈ 0.004/D  →  0.02 (D = 0.2 m) ถึง 0.002 (D = 2 m)")


# =============================================================== P14  หน้า 14-17
class P14_Core(Lesson):
    def construct(self):
        self.head("แกนเหล็ก: แผ่นบาง + ฟลักซ์ถูกกำหนดโดยแรงดัน", "หน้า 14–17 · รูป 10-9 ถึง 10-11")
        self.say("แกนตัน: ฟลักซ์สลับทำให้เกิดกระแสไหลวนวงใหญ่ → ร้อน สูญเสียมาก", color=C_LOSS)
        solid = Rectangle(width=2.6, height=2.6, stroke_color=METAL, fill_color=METAL, fill_opacity=0.35).move_to([-3.2, -0.2, 0])
        ed1 = Ellipse(width=2.0, height=2.0, stroke_color=C_LOSS, stroke_width=4).move_to(solid)
        self.play(FadeIn(solid), run_time=0.6)
        self.play(Create(ed1), run_time=0.8)
        self.play(flow(ed1, C_LOSS, run=1.0), run_time=1.0)
        self.say("แผ่นบาง ~0.3 มม. เคลือบฉนวน + ผสมซิลิคอน → วงกระแสถูกตัดเหลือวงเล็ก สูญเสียลดมาก", color=OK)
        lam = VGroup(*[Rectangle(width=0.36, height=2.6, stroke_color=METAL, fill_color=METAL, fill_opacity=0.35).move_to([1.85 + i * 0.4, -0.2, 0]) for i in range(7)])
        eds = VGroup(*[Ellipse(width=0.22, height=1.9, stroke_color=C_LOSS, stroke_width=2).move_to(r) for r in lam])
        self.play(FadeIn(lam), run_time=0.6)
        self.play(Create(eds), run_time=0.8)
        tl = Text("แกนตัน", font_size=22, color=GRAYTXT).move_to([-3.2, -1.95, 0])
        tr = Text("แผ่นบางซ้อนกัน", font_size=22, color=GRAYTXT).move_to([3.05, -1.95, 0])
        self.play(FadeIn(tl), FadeIn(tr), run_time=0.5)
        self.wait(1.2)
        self.say("มุมแกนต่อแบบสลับชั้น (step-lap) ลดช่องอากาศแอบแฝงที่รอยต่อ (รูป 10-10)", color=GRAYTXT)
        self.wait(1.2)
        self.clear()
        # ---- ฟลักซ์จากแรงดัน
        self.newpage("หน้า 15–16 · สมการ 1.38–1.41")
        self.say("R1 i1 และฟลักซ์รั่วเล็กมาก  →  v1 ≈ e1 = w1 dφm/dt", color=OK)
        a = MathTex(r"\varphi_m\cong\int\frac{1}{w_1}\,v_1\,dt", font_size=42, color=C_PHI).move_to([0, 1.4, 0])
        self.play(Write(a), run_time=1.0)
        k = self.keytext("แหล่งจ่ายแรงดันเป็นตัวกำหนดฟลักซ์  (ไม่ใช่กระแส)", y=0.45, hold=1.4)
        b = MathTex(r"\hat B_m", "=", r"\frac{\sqrt{2}\,V_1}{\omega\,w_1\,\Sigma_m}", "=", r"\frac{V_1}{\sqrt{2}\,\pi f N_1 A}", font_size=42).move_to([0, -0.7, 0])
        b[0].set_color(C_PHI)
        b[4].set_color(YEL)
        self.play(Write(b), run_time=1.4)
        self.say("นี่คือสูตร Bmax ในแบบฝึกหัดข้อ 3: 220 V, 264 รอบ, 25 ตร.ซม. → 1.5 T", color=YEL)
        self.glow(b[4], None, color=YEL)
        self.wait(1.5)
        self.clear()
        # ---- รูป 10-11
        self.newpage("หน้า 16–17 · รูป 10-11")
        self.say("เคอร์ฟ B–H อิ่มตัว: ฟลักซ์เป็นไซน์ แต่กระแสสร้างฟลักซ์ H(t) ยอดแหลม", color=OK)
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.1, 1.1, 1], x_length=4.2, y_length=3.0,
                  axis_config={"color": GRAYTXT, "include_ticks": False, "include_tip": False}).move_to([-3.4, 0.0, 0])
        bh = ax.plot(lambda h: np.tanh(h), x_range=[-3, 3], color=C_PHI, stroke_width=4)
        lb = MathTex("B", font_size=28, color=C_PHI).next_to(ax.y_axis.get_end(), UP, buff=0.08)
        lh = MathTex("H", font_size=28, color=C_MAG).next_to(ax.x_axis.get_end(), RIGHT, buff=0.08)
        ax2 = Axes(x_range=[0, 2 * PI, PI], y_range=[-3.2, 3.2, 1], x_length=4.6, y_length=3.0,
                   axis_config={"color": GRAYTXT, "include_ticks": False, "include_tip": False}).move_to([3.1, 0.0, 0])
        bt = ax2.plot(lambda t: 2.4 * np.sin(t) / 0.97 * 0.97, x_range=[0, 2 * PI], color=C_PHI, stroke_width=3)
        ht = ax2.plot(lambda t: np.arctanh(0.97 * np.sin(t)), x_range=[0, 2 * PI], color=C_MAG, stroke_width=4)
        l1 = MathTex(r"B(t)\ \text{sine}", font_size=26, color=C_PHI).move_to([3.1, 1.9, 0])
        l2 = MathTex(r"H(t)\sim i_m(t)\ \text{peaky}", font_size=26, color=C_MAG).move_to([3.1, -1.9, 0])
        self.play(Create(ax), Create(bh), FadeIn(lb), FadeIn(lh), run_time=1.2)
        self.play(Create(ax2), Create(bt), FadeIn(l1), run_time=1.0)
        self.play(Create(ht), FadeIn(l2), run_time=1.6)
        self.glow(ht, bh, color=C_MAG)
        self.say("กระแสแม่เหล็กต่อหน่วย im = 0.1 … 0.001 (D = 0.2 … 2 m) — หม้อแปลงใหญ่ใช้น้อยมาก", color=C_MAG)
        self.wait(2.0)
        remember(self, "แกนแผ่นบาง 0.3 มม. ลดกระแสไหลวน   แรงดันกำหนดฟลักซ์",
                 "Bmax = V1 / (√2 π f N1 A)   อิ่มตัว → กระแสแม่เหล็กยอดแหลม")


# =============================================================== P18  หน้า 18-20
class P18_TLCircuit(Lesson):
    def construct(self):
        self.head("วงจร T → วงจร L → ตัดขาแม่เหล็ก", "หน้า 18–20 · รูป 10-12 ถึง 10-17")
        self.say("ตัวเลขต่อหน่วยตัวอย่างในรูป 10-13b  (อนุกรมเล็กมาก  ขาแม่เหล็กใหญ่มาก)", color=OK)
        nm = ["0.005", "j0.025", "j0.025", "0.005", "v_1", "v_2", "j100", "1000"]
        c = tee_circuit(x0=-5.6, y_top=1.0, y_bot=-1.0, labels=True, size=26, names=nm)
        self.play(Create(c), run_time=2.0)
        p = c.parts
        self.glow(p["lab"][6], p["xm"], color=C_MAG)
        self.glow(p["lab"][1], p["x1"], color=C_P)
        cmp_ = MathTex(r"x_m=100\ \gg\ z_{series}\approx0.05", font_size=34, color=YEL).move_to([0, -1.75, 0])
        self.play(Write(cmp_), run_time=1.0)
        self.say("ขาแม่เหล็กใหญ่กว่าอนุกรม ~2000 เท่า → ย้ายไปไว้หน้าวงจรได้ ผิดน้อยมาก = วงจร L", color=YEL)
        self.wait(1.2)
        self.clear()
        # ---- วงจร L (รูป 10-14a)
        y1, y0 = 1.0, -1.0
        w = VGroup(wire((-5.0, y1), (-1.0, y1)), wire((1.4, y1), (5.0, y1)), wire((-5.0, y0), (5.0, y0)))
        xm = ind_sym((-3.9, y1 - 0.3), (-3.9, y0 + 0.3), color=C_MAG)
        rm = res_zig((-2.9, y1 - 0.3), (-2.9, y0 + 0.3), color=C_LOSS)
        brs = VGroup(wire((-3.9, y1), (-3.9, y1 - 0.3)), wire((-3.9, y0 + 0.3), (-3.9, y0)), wire((-2.9, y1), (-2.9, y1 - 0.3)), wire((-2.9, y0 + 0.3), (-2.9, y0)))
        zs = ebox(0.2, y1, r"(R_1+R_2')+j(X_{1\sigma}+X_{2\sigma}')", C_P, w=2.4, h=0.55, size=20)
        lab = VGroup(MathTex("jX_m", font_size=24, color=C_MAG).next_to(xm, LEFT, buff=0.12),
                     MathTex("R_c", font_size=24, color=C_LOSS).next_to(rm, RIGHT, buff=0.12))
        tt = Text("วงจร L (รูป 10-14): ขาแม่เหล็กอยู่ด้านแหล่งจ่าย → หากระแสแม่เหล็กได้ตรงๆ", font_size=21, color=GRAYTXT).move_to([0, -1.75, 0])
        self.play(Create(w), Create(xm), Create(rm), Create(brs), FadeIn(lab), FadeIn(zs), FadeIn(tt), run_time=1.6)
        self.wait(1.5)
        self.say("หม้อแปลงกำลังสูง: ตัดขาแม่เหล็กทิ้ง (+ ตัด R) เหลือ jX ตัวเดียว (รูป 10-15)", color=OK)
        self.play(FadeOut(VGroup(xm, rm, brs, lab)), run_time=0.8)
        zx = ebox(0.2, y1, r"j(X_{1\sigma}+X_{2\sigma}')", C_P, w=2.4, h=0.55, size=22)
        self.play(Transform(zs, zx), run_time=0.8)
        t2 = Text("นี่คือ jX ของหม้อแปลงใน reactance diagram บทที่ 11", font_size=21, color=YEL).move_to([0, -2.4, 0])
        self.play(FadeIn(t2), run_time=0.6)
        self.wait(1.5)
        self.clear()
        # ---- รูป 10-12 Xm เปลี่ยนตามแรงดัน
        self.newpage("หน้า 18 · รูป 10-12")
        self.say("Xm = ความชันเส้นจากจุดกำเนิดถึงจุดทำงานบนเคอร์ฟ E–Im", color=OK)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1.2, 1], x_length=5.0, y_length=3.2,
                  axis_config={"color": GRAYTXT, "include_ticks": False}).move_to([-2.4, -0.3, 0])
        cur = ax.plot(lambda x: np.tanh(1.6 * x), x_range=[0, 3], color=C_E, stroke_width=4)
        le = MathTex("E", font_size=28, color=C_E).next_to(ax.y_axis.get_end(), LEFT, buff=0.1)
        li = MathTex("I_m", font_size=28, color=C_MAG).next_to(ax.x_axis.get_end(), DOWN, buff=0.1)
        self.play(Create(ax), Create(cur), FadeIn(le), FadeIn(li), run_time=1.2)
        xt = ValueTracker(0.5)
        ln = always_redraw(lambda: Line(ax.c2p(0, 0), ax.c2p(xt.get_value(), np.tanh(1.6 * xt.get_value())), color=YEL, stroke_width=4))
        dt = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), np.tanh(1.6 * xt.get_value())), color=YEL, radius=0.07))
        xv = always_redraw(lambda: MathTex(r"X_m\propto\tan\alpha=%.2f" % (np.tanh(1.6 * xt.get_value()) / xt.get_value()), font_size=32, color=YEL).move_to([3.6, 0.6, 0]))
        self.add(ln, dt, xv)
        self.say("แรงดันสูงกว่าพิกัด → อิ่มตัวมากขึ้น → เส้นลาดน้อยลง → Xm เล็กลง", color=YEL)
        self.play(xt.animate.set_value(2.6), run_time=3.0)
        self.wait(1.2)
        for m in (ln, dt, xv):
            m.clear_updaters()
        self.say("สมมูลเทวินิน (รูป 10-16): มองจากโหลด = แหล่ง V20 (แรงดันไม่มีโหลด) อนุกรม Zk2", color=OK)
        self.wait(1.8)
        remember(self, "T (ครบ) → L (ย้ายขาแม่เหล็ก) → jX เดียว (ตัดขาแม่เหล็ก)",
                 "ทำได้เพราะ xm ≈ 100 ≫ อนุกรม ≈ 0.05 (p.u.)")


# =============================================================== P21  หน้า 20-21
class P21_NoLoad(Lesson):
    def construct(self):
        self.head("สมดุลกำลัง + การทดสอบไม่มีโหลด (Open-circuit test)", "หน้า 21 · สมการ 1.48–1.52")
        self.say("กำลังเข้า = กำลังออก + สูญเสียทองแดง 2 ขด + สูญเสียแกน", color=OK)
        c = tee_circuit(x0=-5.6, y_top=1.3, y_bot=-0.7, labels=True, size=24)
        self.play(Create(c), run_time=1.6)
        p = c.parts
        f = MathTex(r"P_1", "=", r"P_{2L}", "+", r"R_1I_1^2", "+", r"R_2'I_2'^2", "+", r"\frac{E_1^2}{R_{m1}}", font_size=38).move_to([0, -1.75, 0])
        f[0].set_color(YEL)
        f[2].set_color(OK)
        f[4].set_color(C_P)
        f[6].set_color(C_SEC)
        f[8].set_color(C_LOSS)
        self.play(Write(f), run_time=1.4)
        self.glow(f[4], p["r1"], color=C_P)
        self.glow(f[6], p["r2"], color=C_SEC)
        self.glow(f[8], p["rm"], color=C_LOSS)
        self.wait(1.0)
        self.say("ทดสอบไม่มีโหลด: เปิดวงจรทุติยภูมิ จ่ายแรงดันพิกัด วัด V, I, P", color=OK)
        cross = Cross(VGroup(p["x2"], p["r2"]), stroke_color=C_LOSS, stroke_width=5)
        self.play(Create(cross), run_time=0.6)
        self.say("กระแสน้อยมาก → ตกที่ R1, X1 ตัดทิ้งได้ → กระแสไหลเฉพาะขาแม่เหล็ก", color=C_MAG)
        self.play(Indicate(VGroup(p["xm"], p["rm"]), color=C_MAG), run_time=1.0)
        self.play(FadeOut(f), run_time=0.4)
        g = MathTex(r"I_{10}\approx\frac{V_1}{jX_1}+\frac{V_1}{R_{m1}}", font_size=40, color=WHITE).move_to([0, -1.75, 0])
        self.play(Write(g), run_time=1.0)
        self.wait(1.2)
        self.clear()
        # ---- ตัวอย่างสมมติ
        self.say("ตัวอย่าง (ตัวเลขสมมติ ไม่ได้มาจาก PDF): วัดได้ 240 V, 0.5 A, 60 W", color=YEL)
        bd = Board(self, x=-6.6, y=2.1, gap=0.12)
        bd.add(1, "เข้าใจ: วัตต์มิเตอร์อ่านสูญเสียแกน", n_text("S = V I = 240 × 0.5 = 120 VA   P = 60 W", size=22), hold=0.9)
        bd.add(2, "แยกกระแส", VGroup(MathTex(r"\cos\theta=P/S=60/120=0.5", font_size=30),
                                    MathTex(r"I_c=0.5\times0.5=0.25\,A\quad I_m=0.5\times0.866=0.433\,A", font_size=30, color=C_MAG)
                                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.1), run=1.6, hold=1.0)
        bd.add(3, "ค่าในวงจร", VGroup(MathTex(r"R_c=V/I_c=240/0.25=960\,\Omega", font_size=30, color=C_LOSS),
                                     MathTex(r"X_m=V/I_m=240/0.433=554\,\Omega", font_size=30, color=C_MAG)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
               run=1.6, hold=1.0)
        bd.add(4, "ตรวจ", MathTex(r"V^2/R_c=240^2/960=60\,W\ \checkmark", font_size=30, color=OK), hold=1.4)
        self.say("แรงดันทุติยภูมิไม่มีโหลด V20' ≈ V1 / (1 + σ1) ≈ V1 (เกือบเท่าอัตราส่วนรอบ)", color=GRAYTXT)
        self.wait(1.5)
        remember(self, "ไม่มีโหลด → ได้ Rc (สูญเสียแกน) และ Xm (สร้างฟลักซ์)",
                 "Rc = V/Ic    Xm = V/Im    P วัดได้ = สูญเสียแกน")
