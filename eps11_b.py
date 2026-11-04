"""EPS11 ชุด 2 (หน้า 1-39) ล็อต 1 — วงจรหม้อแปลง / วาด reactance diagram / พื้นฐาน per-unit
P10_PracticalModel (10) · P11_ModelCircuit (11-12) · P13_Collapse (13-14) · P24_ReactanceDraw (24-25)
P26_PerUnitDef (26-30) · P31_WhyBase (31-33) · P34_BaseDerive (34-39)   ตัวเลขทุกตัวมาจากสไลด์ (ยกเว้นที่ติดป้าย "สมมติ")
"""
from eps11_lib import *


# =============================================================== P10  หน้า 10
class P10_PracticalModel(Lesson):
    """แบบจำลองทางปฏิบัติ: ของจริง = อุดมคติ + R1,R2 + Ll1,Ll2 + Rc,Lm"""

    def construct(self):
        self.head("หม้อแปลงจริง ≠ อุดมคติ", "หน้า 10")
        self.say("ภาพก่อน: หม้อแปลงจริงมีอะไรที่อุดมคติไม่มี?", color=OK)
        p = core_pic(-0.5, 0.2)
        p["all"].scale(1.5, about_point=np.array([-0.5, 0.2, 0]))
        self.play(FadeIn(p["all"]), run_time=1.2)
        n1 = M(r"N_1", C_R, 26).next_to(p["c1"], LEFT, buff=0.1).shift(UP * 0.0)
        n2 = M(r"N_2", C_S, 26).next_to(p["c2"], RIGHT, buff=0.1)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.5)
        self.wait(1.0)
        # 1 ลวดมีความต้านทาน
        self.say("1) ลวดทองแดงมีความต้านทาน  →  R₁ , R₂", color=C_R)
        self.play(Indicate(p["c1"], color=C_R), Indicate(p["c2"], color=C_R), run_time=1.2)
        self.wait(1.2)
        # 2 ฟลักซ์รั่ว
        self.say("2) ฟลักซ์บางส่วนรั่วออกนอกแกน (ไม่คล้องอีกขด)  →  L_l1 , L_l2", color=C_IF)
        lk1 = DashedVMobject(Ellipse(width=1.9, height=2.3, color=C_IF, stroke_width=4)).move_to(p["c1"].get_center())
        lk2 = DashedVMobject(Ellipse(width=1.9, height=2.3, color=C_IF, stroke_width=4)).move_to(p["c2"].get_center())
        t1 = M(r"\phi_{l1}", C_IF, 24).next_to(lk1, UP, buff=0.12)
        t2 = M(r"\phi_{l2}", C_IF, 24).next_to(lk2, UP, buff=0.12)
        self.play(Create(lk1), Create(lk2), FadeIn(t1), FadeIn(t2), run_time=1.4)
        self.wait(1.2)
        # 3 แกน
        self.say("3) แกนเหล็กสูญเสียกำลัง และต้องมีกระแสสร้างฟลักซ์  →  R_c , L_m", color=C_E)
        self.play(Indicate(p["core"], color=C_E), Indicate(p["flux"], color=C_PHI), run_time=1.4)
        self.wait(1.2)
        # ---- เปลี่ยนเป็นวงจร
        self.say("แปลงเป็นวงจร: ใส่ทั้ง 6 ตัวนี้ + หม้อแปลงอุดมคติ  (ลายมือ Min: ต้องวาดได้!)", color=OK)
        self.play(FadeOut(VGroup(p["all"], n1, n2, lk1, lk2, t1, t2)), run_time=0.7)
        top, bot = 0.7, -1.3
        sx = -6.4
        r1 = res_zig((sx + 0.3, top), (sx + 1.4, top), color=C_R)
        ll1 = coil_sym((sx + 1.6, top), (sx + 2.7, top), n=3, color=C_IF)
        rc = res_zig((-3.7, top), (-3.7, bot), color=C_E)
        lm = vcoil(-3.0, top, bot, C_PHI)
        xf = xf_ideal(-1.6, -0.3, h=2.0)
        ll2 = coil_sym((-1.2, top), (-0.2, top), n=3, color=C_IF)
        r2 = res_zig((0.0, top), (1.1, top), color=C_R)
        wr = VGroup(wire((sx, top), (sx + 0.3, top)), wire((sx + 1.4, top), (sx + 1.6, top)), wire((sx + 2.7, top), (-1.77, top)),
                    wire((-3.7, top), (-3.0, top)), wire((sx, bot), (-1.77, bot)), wire((-3.7, bot), (-3.0, bot)),
                    wire((-1.43, top), (-1.2, top)), wire((-0.2, top), (0.0, top)), wire((1.1, top), (1.5, top)),
                    wire((-1.43, bot), (1.5, bot)))
        ter = VGroup(*[Circle(radius=0.07, stroke_color=GRAYTXT, stroke_width=3).move_to(q) for q in ([sx, top, 0], [sx, bot, 0], [1.5, top, 0], [1.5, bot, 0])])
        circ = VGroup(wr, r1, ll1, rc, lm, xf, ll2, r2, ter)
        labs = VGroup(M(r"R_1", C_R, 24).move_to([sx + 0.85, 1.15, 0]), M(r"L_{l1}", C_IF, 24).move_to([sx + 2.15, 1.15, 0]),
                      M(r"R_c", C_E, 24).move_to([-4.2, -0.3, 0]), M(r"L_m", C_PHI, 24).move_to([-2.5, -0.3, 0]),
                      M(r"L_{l2}", C_IF, 24).move_to([-0.7, 1.15, 0]), M(r"R_2", C_R, 24).move_to([0.55, 1.15, 0]),
                      M(r"N_1:N_2", WHITE, 24).move_to([-1.6, -1.85, 0]))
        self.play(Create(circ), run_time=1.6)
        self.play(FadeIn(labs), run_time=0.6)
        legend = [(r"R_1,\ R_2", "ความต้านทานขดลวด", C_R, [r1, r2], [0, 5]),
                  (r"L_{l1},\ L_{l2}", "ฟลักซ์รั่ว (leakage)", C_IF, [ll1, ll2], [1, 4]),
                  (r"R_c", "สูญเสียในแกน", C_E, [rc], [2]),
                  (r"L_m", "กระแสสร้างอำนาจแม่เหล็ก", C_PHI, [lm], [3])]
        y = 1.9
        for tex, th, col, els, li in legend:
            chip = VGroup(M(tex, col, 24), T(th, 20, col)).arrange(RIGHT, buff=0.25)
            chip.move_to([4.7, y, 0]).align_to([2.35, 0, 0], LEFT)
            self.play(FadeIn(chip, shift=LEFT * 0.2), *[Indicate(e, color=col, scale_factor=1.15) for e in els], run_time=0.9)
            self.wait(0.9)
            y -= 0.75
        self.wait(1.0)
        remember(self, "ของจริง = หม้อแปลงอุดมคติ + R₁R₂ + L_l1 L_l2 + R_c ∥ L_m", "เขียนวงจรนี้ได้ = ได้คะแนนพื้นฐานบทนี้")


# =============================================================== P11  หน้า 11-12
class P11_ModelCircuit(Lesson):
    """วงจรแบบจำลอง (r1 x1 | B G | N1:N2 | r2 x2) แล้วอ้างอิงทุติยภูมิมาปฐมภูมิ (a²r2, a²x2, aV2)"""

    def construct(self):
        self.head("วงจรหม้อแปลง + อ้างอิงมาด้านปฐมภูมิ", "หน้า 11–12")
        self.say("หน้า 11: เขียนเป็นวงจรแทน  ด้านซ้าย = ปฐมภูมิ  ด้านขวา = ทุติยภูมิ", color=OK)
        top, bot = 0.9, -1.3
        # ซ้าย
        v1 = varrow(-6.1, bot, top, C_A, r"V_1", LEFT)
        r1 = res_zig((-5.5, top), (-4.6, top), color=C_R)
        x1 = coil_sym((-4.4, top), (-3.5, top), n=3, color=C_IF)
        L = VGroup(wire((-6.1, top), (-5.5, top)), wire((-4.6, top), (-4.4, top)), wire((-3.5, top), (-2.6, top)),
                   wire((-6.1, bot), (-2.6, bot)), v1, r1, x1,
                   M(r"r_1", C_R, 22).move_to([-5.05, 1.35, 0]), M(r"x_1", C_IF, 22).move_to([-3.95, 1.35, 0]),
                   harrow(-5.4, -4.5, 1.85, C_E, r"I_1", True))
        # ชันต์ B (cuil) || G (zig)
        sb = vcoil(-2.6, top, bot, C_PHI)
        sg = res_zig((-1.9, top), (-1.9, bot), color=C_E)
        S = VGroup(wire((-2.6, top), (-1.9, top)), wire((-2.6, bot), (-1.9, bot)), sb, sg,
                   M(r"B", C_PHI, 24).move_to([-3.05, -0.2, 0]), M(r"G", C_E, 24).move_to([-1.45, -0.2, 0]),
                   varrow(-3.55, 0.55, -0.15, BLUE_C, r"I_E", LEFT, 22))
        # หม้อแปลงอุดมคติ + ฝั่งทุติยภูมิ
        X = VGroup(wire((-1.9, top), (-0.55, top)), wire((-1.9, bot), (-0.55, bot)), xf_ideal(-0.4, -0.2, h=2.2),
                   M(r"N_1:N_2", WHITE, 22).move_to([-0.4, -1.75, 0]))
        r2 = res_zig((0.5, top), (1.4, top), color=C_R)
        x2 = coil_sym((1.6, top), (2.5, top), n=3, color=C_IF)
        R = VGroup(wire((-0.23, top), (0.5, top)), wire((1.4, top), (1.6, top)), wire((2.5, top), (3.1, top)),
                   wire((-0.23, bot), (3.1, bot)), r2, x2,
                   M(r"r_2", C_R, 22).move_to([0.95, 1.35, 0]), M(r"x_2", C_IF, 22).move_to([2.05, 1.35, 0]),
                   varrow(3.1, bot, top, C_A, r"V_2", RIGHT), harrow(0.6, 1.5, 1.85, C_E, r"I_2", True))
        self.play(Create(VGroup(L, S, X, R)), run_time=2.0)
        self.wait(0.8)
        # chip อธิบาย
        c1 = fit_width(card([("r₁ x₁ r₂ x₂", YEL), "ต้านทาน / รีแอคแตนซ์รั่ว", "ของขดลวดแต่ละด้าน"], w=2.8, color=YEL, size=19), 3.0).move_to([5.45, 1.6, 0])
        c2 = fit_width(card([("B , G", C_PHI), "สาขาขนาน (I_E)", "สร้างฟลักซ์ + สูญเสียแกน"], w=2.8, color=C_PHI, size=19), 3.0).move_to([5.45, -0.4, 0])
        self.play(FadeIn(c1), Indicate(L[6], color=C_IF), Indicate(R[5], color=C_IF), run_time=1.0)
        self.wait(1.0)
        self.play(FadeIn(c2), Indicate(S[2], color=C_PHI), Indicate(S[3], color=C_E), run_time=1.0)
        self.wait(1.3)
        self.play(FadeOut(VGroup(c1, c2)), run_time=0.5)
        # ---------- หน้า 12
        self.newpage("หน้า 12")
        self.say("หน้า 12: อ้างอิงฝั่งทุติยภูมิมาไว้ฝั่งปฐมภูมิ  → ไม่ต้องมีหม้อแปลงอุดมคติอีกต่อไป", color=OK)
        self.play(FadeOut(VGroup(X, R)), run_time=0.7)
        a2r2 = res_zig((-1.4, top), (-0.5, top), color=C_R)
        a2x2 = coil_sym((-0.3, top), (0.6, top), n=3, color=C_IF)
        R2 = VGroup(wire((-1.9, top), (-1.4, top)), wire((-0.5, top), (-0.3, top)), wire((0.6, top), (1.3, top)),
                    wire((-1.9, bot), (1.3, bot)), a2r2, a2x2,
                    M(r"a^2 r_2", C_R, 22).move_to([-0.95, 1.4, 0]), M(r"a^2 x_2", C_IF, 22).move_to([0.15, 1.4, 0]),
                    varrow(1.3, bot, top, C_A, r"aV_2", RIGHT), harrow(-1.2, -0.3, 1.9, C_E, r"I_2", True))
        self.play(Create(R2), run_time=1.5)
        self.wait(0.8)
        f = VGroup(M(r"a", YEL, 34), M(r"=", WHITE, 30), M(r"\frac{N_1}{N_2}", YEL, 34)).arrange(RIGHT, buff=0.15).move_to([5.0, 1.5, 0])
        fl = T("อัตราส่วนจำนวนรอบ", 19, GRAYTXT).next_to(f, DOWN, buff=0.15)
        self.play(FadeIn(f), FadeIn(fl), run_time=0.8)
        rule = VGroup(M(r"Z_{sec\to pri}=a^{2}\,Z_{sec}", C_IF, 26), T("ค่าฝั่งทุติยภูมิ ×a²  ส่วนแรงดัน ×a", 19, GRAYTXT)).arrange(DOWN, buff=0.15).move_to([5.0, -0.2, 0])
        fit_width(rule, 3.9)
        self.play(FadeIn(rule), Indicate(R2[6], color=C_R), Indicate(R2[7], color=C_IF), run_time=1.2)
        self.wait(1.2)
        ie = T("I_E = กระแสสร้างอำนาจแม่เหล็ก (Magnetizing Current)", 20, C_PHI).move_to([-1.8, -2.45, 0])
        self.play(FadeIn(ie), Indicate(S[2], color=C_PHI), run_time=1.0)
        self.wait(1.2)
        # ตัวอย่างสมมติ
        ex = VGroup(T("ตัวอย่างสมมติ (ไม่ได้อยู่ในสไลด์ ใช้ดูภาพ)", 17, GRAYTXT),
                    VGroup(M(r"a=2,\ r_2=1\,\Omega\ \Rightarrow\ a^2 r_2=4\,\Omega", WHITE, 24)).arrange(RIGHT)).arrange(DOWN, buff=0.12)
        ex.move_to([3.0, -3.3, 0])
        self.play(FadeIn(ex), run_time=0.8)
        self.wait(2.0)
        remember(self, "อ้างอิงข้ามหม้อแปลง: อิมพีแดนซ์ × a²   แรงดัน × a   (a = N₁/N₂)", "ผลคือวงจรเดียว r₁ x₁ | B∥G | a²r₂ a²x₂ | aV₂")


# =============================================================== P13  หน้า 13-14
class P13_Collapse(Lesson):
    """ยุบวงจร: ตัด B-G -> R1 = r1 + a²r2, X1 = x1 + a²x2 -> ตัด R1 เหลือ X1"""

    def construct(self):
        self.head("ยุบวงจรหม้อแปลง → เหลือ jX เดียว", "หน้า 13–14")
        self.say("เริ่มจากวงจรหน้า 12 (อ้างมาฝั่งปฐมภูมิแล้ว)", color=OK)
        top, bot = 0.9, -1.2
        e = {}
        e["r1"] = res_zig((-5.6, top), (-4.8, top), color=C_R)
        e["x1"] = coil_sym((-4.6, top), (-3.8, top), n=3, color=C_IF)
        e["a2r2"] = res_zig((-2.0, top), (-1.2, top), color=C_R)
        e["a2x2"] = coil_sym((-1.0, top), (-0.2, top), n=3, color=C_IF)
        e["b"] = vcoil(-3.4, top, bot, C_PHI)
        e["g"] = res_zig((-2.8, top), (-2.8, bot), color=C_E)
        sh = VGroup(wire((-3.4, top), (-2.8, top)), wire((-3.4, bot), (-2.8, bot)), e["b"], e["g"],
                    M(r"B", C_PHI, 22).move_to([-3.8, -0.15, 0]), M(r"G", C_E, 22).move_to([-2.35, -0.15, 0]))
        rails = VGroup(wire((-6.2, top), (-5.6, top)), wire((-4.8, top), (-4.6, top)), wire((-3.8, top), (-3.4, top)),
                       wire((-2.8, top), (-2.0, top)), wire((-1.2, top), (-1.0, top)), wire((-0.2, top), (0.5, top)),
                       wire((-6.2, bot), (0.5, bot)))
        labs = VGroup(M(r"r_1", C_R, 22).move_to([-5.2, 1.35, 0]), M(r"x_1", C_IF, 22).move_to([-4.2, 1.35, 0]),
                      M(r"a^2 r_2", C_R, 22).move_to([-1.6, 1.35, 0]), M(r"a^2 x_2", C_IF, 22).move_to([-0.6, 1.35, 0]))
        ends = VGroup(varrow(-6.2, bot, top, C_A, r"V_1", LEFT), varrow(0.5, bot, top, C_A, r"aV_2", RIGHT))
        circ = VGroup(rails, e["r1"], e["x1"], e["a2r2"], e["a2x2"], sh, labs, ends)
        self.play(Create(circ), run_time=1.6)
        self.wait(0.8)
        # ---- ตัด B-G
        self.say("1) กระแสสร้างอำนาจแม่เหล็กน้อยมาก → ตัดสาขา B–G ทิ้งได้", color=C_PHI)
        self.play(Indicate(sh[2], color=C_PHI), Indicate(sh[3], color=C_E), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(sh), run_time=0.9)
        # ---- อนุกรมรวมกัน
        self.say("2) เหลือ 4 ตัวต่ออนุกรมกัน → บวกกันได้เลย:  R₁ = r₁ + a²r₂ ,  X₁ = x₁ + a²x₂", color=OK)
        box1 = SurroundingRectangle(VGroup(e["r1"], e["a2r2"]), color=C_R, buff=0.18)
        self.play(Create(box1), run_time=0.6)
        f1 = M(r"R_1=r_1+a^2 r_2", C_R, 32).move_to([3.4, 2.0, 0])
        self.play(Write(f1), run_time=1.2)
        self.play(FadeOut(box1), run_time=0.3)
        box2 = SurroundingRectangle(VGroup(e["x1"], e["a2x2"]), color=C_IF, buff=0.18)
        self.play(Create(box2), run_time=0.6)
        f2 = M(r"X_1=x_1+a^2 x_2", C_IF, 32).move_to([3.4, 1.2, 0])
        self.play(Write(f2), run_time=1.2)
        self.play(FadeOut(box2), run_time=0.3)
        self.wait(0.8)
        # วงจรยุบ
        self.play(FadeOut(VGroup(e["r1"], e["x1"], e["a2r2"], e["a2x2"], labs, rails, ends)), run_time=0.7)
        R1 = res_zig((-3.6, top), (-2.4, top), color=C_R)
        X1 = coil_sym((-2.2, top), (-1.0, top), n=4, color=C_IF)
        c2 = VGroup(wire((-5.0, top), (-3.6, top)), wire((-2.4, top), (-2.2, top)), wire((-1.0, top), (0.4, top)),
                    wire((-5.0, bot), (0.4, bot)), R1, X1,
                    M(r"R_1", C_R, 26).move_to([-3.0, 1.4, 0]), M(r"X_1", C_IF, 26).move_to([-1.6, 1.4, 0]),
                    varrow(-5.0, bot, top, C_A, r"V_1", LEFT), varrow(0.4, bot, top, C_A, r"aV_2", RIGHT))
        self.play(Create(c2), run_time=1.2)
        self.wait(1.0)
        # ---- ตัด R1
        self.say("3) หน้า 14: X₁ มากกว่า R₁ เป็นจำนวนมาก → ตัด R₁ ได้", color=C_E)
        bars = VGroup(Rectangle(width=0.5, height=1.9, fill_color=C_IF, fill_opacity=0.8, stroke_width=0),
                      Rectangle(width=0.5, height=0.2, fill_color=C_R, fill_opacity=0.8, stroke_width=0)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        bars.move_to([3.4, -1.4, 0])
        bl = VGroup(M(r"X_1", C_IF, 22).next_to(bars[0], DOWN, buff=0.1), M(r"R_1", C_R, 22).next_to(bars[1], DOWN, buff=0.1))
        bn = T("ภาพเปรียบเทียบขนาด (ประกอบ)", 16, GRAYTXT).next_to(bars, UP, buff=0.2)
        self.play(FadeIn(bars), FadeIn(bl), FadeIn(bn), run_time=1.0)
        self.play(Indicate(bars[1], color=C_R), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(VGroup(R1, c2[6], bars, bl, bn, f1, f2)), run_time=0.9)
        w = wire((-3.6, top), (-2.2, top))
        self.play(Create(w), run_time=0.5)
        lk = T("รีแอคแตนซ์รั่ว (leakage reactance)", 22, C_IF).move_to([-1.0, 1.9, 0])
        self.play(FadeIn(lk), Indicate(X1, color=C_IF), run_time=1.0)
        self.wait(1.6)
        remember(self, "หม้อแปลงในแผนภาพ reactance = jX อย่างเดียว  (X₁ = x₁ + a²x₂)", "ตัด B–G (กระแสสร้างฟลักซ์น้อย) และตัด R₁ (X₁ ≫ R₁)")


# =============================================================== P24  หน้า 24-25
class P24_ReactanceDraw(Lesson):
    """วาด reactance diagram จาก single-line (G1-T1 / G2-T2 / T3-G3 + บัส a b c d + สายส่ง 5 เส้น)"""

    def construct(self):
        self.head("วาด reactance diagram จาก single-line", "หน้า 24–25")
        self.say("โจทย์: เขียนแผนภาพรีแอคแตนซ์จากแผนภาพเส้นเดี่ยว  กติกา: คิดเฉพาะรีแอคแตนซ์ของอุปกรณ์", color=OK)

        def gen(cx, cy, name):
            c = Circle(radius=0.28, stroke_color=YEL, stroke_width=3, fill_color=YEL, fill_opacity=0.18).move_to([cx, cy, 0])
            return VGroup(c, MathTex(name, font_size=22, color=YEL).move_to(c))

        def xt(cx, cy, vertical=False):
            a = Circle(radius=0.24, stroke_color=WHITE, stroke_width=3)
            b = a.copy()
            if vertical:
                a.move_to([cx, cy + 0.15, 0]); b.move_to([cx, cy - 0.15, 0])
            else:
                a.move_to([cx - 0.15, cy, 0]); b.move_to([cx + 0.15, cy, 0])
            return VGroup(a, b)

        # ---------------- single line (ซ้าย)
        bus = lambda x0, y0, x1, y1: Line([x0, y0, 0], [x1, y1, 0], color=WHITE, stroke_width=7)
        ba, bc = bus(-4.4, -0.3, -4.4, 1.3), bus(-1.0, -0.3, -1.0, 1.3)
        bb, bd = bus(-3.4, 2.0, -2.0, 2.0), bus(-3.4, -0.9, -2.0, -0.9)
        G1, T1 = gen(-6.5, 0.5, "G_1"), xt(-5.45, 0.5)
        G2, T2 = gen(0.6, 0.5, "G_2"), xt(-0.15, 0.5)
        T3, G3 = xt(-2.7, -1.5, True), gen(-2.7, -2.4, "G_3")
        lines = VGroup(wire((-4.4, 1.1), (-3.2, 1.1), (-3.2, 2.0)), wire((-1.0, 1.1), (-2.2, 1.1), (-2.2, 2.0)),
                       wire((-4.4, -0.1), (-3.2, -0.1), (-3.2, -0.9)), wire((-1.0, -0.1), (-2.2, -0.1), (-2.2, -0.9)),
                       wire((-2.7, 2.0), (-2.7, -0.9)),
                       wire((-6.22, 0.5), (-5.69, 0.5)), wire((-5.21, 0.5), (-4.4, 0.5)),
                       wire((0.32, 0.5), (0.09, 0.5)), wire((-0.39, 0.5), (-1.0, 0.5)),
                       wire((-2.7, -0.9), (-2.7, -1.35)), wire((-2.7, -1.65), (-2.7, -2.12)))
        names = VGroup(*[T(s, 16, GRAYTXT).move_to(p) for s, p in
                         (("a", [-4.7, 1.45, 0]), ("b", [-3.7, 2.3, 0]), ("c", [-0.7, 1.45, 0]), ("d", [-3.7, -1.2, 0]))])
        sl = VGroup(ba, bc, bb, bd, G1, T1, G2, T2, T3, G3, lines, names)
        lab = VGroup(M(r"T_1", WHITE, 18).move_to([-5.45, 0.95, 0]), M(r"T_2", WHITE, 18).move_to([-0.15, 0.95, 0]),
                     M(r"T_3", WHITE, 18).move_to([-3.1, -1.5, 0]))
        sl.add(lab)
        self.play(FadeIn(sl), run_time=1.4)
        self.wait(1.2)
        # ---------------- reactance diagram (ขวา) ทีละขั้น
        dx = 7.0
        ax_, cx_, d_y = -4.4 + dx, -1.0 + dx, -0.9
        # 1) อุปกรณ์ทุกตัว -> jX
        self.say("ขั้น 1: อุปกรณ์ทุกตัวกลายเป็น jX  (G → jX_G , T → jX_T)", color=YEL)
        bx = {}
        for k, (cx, cy, tx, col) in {"T1": (ax_, -0.8, r"jX_{T1}", WHITE), "G1": (ax_, -1.45, r"jX_{G1}", YEL),
                                      "T2": (cx_, -0.8, r"jX_{T2}", WHITE), "G2": (cx_, -1.45, r"jX_{G2}", YEL),
                                      "T3": (-2.7 + dx, -1.4, r"jX_{T3}", WHITE), "G3": (-2.7 + dx, -2.0, r"jX_{G3}", YEL)}.items():
            bx[k] = ebox(cx, cy, tx, col, w=1.05, h=0.4, size=18)
        self.play(*[Indicate(m, color=YEL) for m in (G1, T1, G2, T2, T3, G3)], run_time=1.0)
        self.play(*[FadeIn(v, shift=LEFT * 0.3) for v in bx.values()], run_time=1.2)
        self.wait(0.8)
        # 2) แหล่งกำเนิด E ต่อเข้านิวทรัล
        self.say("ขั้น 2: เครื่องกำเนิดแต่ละตัว = แหล่ง E ต่ออนุกรม jX_G  แล้วลงนิวทรัล", color=YEL)
        NY = -3.05
        srcs = {k: src(x, y, "", YEL, r=0.25) for k, (x, y) in {"E1": (ax_, -2.25), "E2": (cx_, -2.25), "E3": (-2.7 + dx, -2.7)}.items()}
        sl_ = VGroup(*[MathTex(k[0] + "_" + k[1], font_size=20, color=YEL).next_to(srcs[k], RIGHT, buff=0.12) for k in srcs])
        br = VGroup(wire((ax_, -0.1), (ax_, -0.6)), wire((ax_, -1.0), (ax_, -1.25)), wire((ax_, -1.65), (ax_, -2.0)), wire((ax_, -2.5), (ax_, NY)),
                    wire((cx_, -0.1), (cx_, -0.6)), wire((cx_, -1.0), (cx_, -1.25)), wire((cx_, -1.65), (cx_, -2.0)), wire((cx_, -2.5), (cx_, NY)),
                    wire((-2.7 + dx, d_y), (-2.7 + dx, -1.2)), wire((-2.7 + dx, -1.6), (-2.7 + dx, -1.8)), wire((-2.7 + dx, -2.2), (-2.7 + dx, -2.45)),
                    wire((-2.7 + dx, -2.95), (-2.7 + dx, NY)), wire((ax_, NY), (cx_, NY)))
        nt = T("นิวทรัล (จุดอ้างอิงร่วม)", 17, GRAYTXT).move_to([ax_ + 1.7, NY - 0.3, 0])
        self.play(Create(br), FadeIn(VGroup(*srcs.values())), FadeIn(sl_), FadeIn(nt), run_time=1.6)
        self.wait(0.8)
        # 3) บัส + สายส่ง
        self.say("ขั้น 3: บัสเป็นจุดต่อ  สายส่งทั้ง 5 เส้นเป็น jX_L  ตามที่ต่อในแผนภาพเส้นเดี่ยว", color=C_IL)
        xs = lambda p: [p[0] + dx, p[1], 0]
        nodes = VGroup(wire((ax_, -0.1), (ax_, 1.1), color=WHITE, width=6), wire((cx_, -0.1), (cx_, 1.1), color=WHITE, width=6),
                       wire((-3.4 + dx, 2.0), (-2.0 + dx, 2.0), color=WHITE, width=6), wire((-3.4 + dx, d_y), (-2.0 + dx, d_y), color=WHITE, width=6))
        jl = []
        segs = [((-4.4, 1.1), (-3.2, 1.1), (-3.2, 2.0), 0.35), ((-1.0, 1.1), (-2.2, 1.1), (-2.2, 2.0), -0.35),
                ((-4.4, -0.1), (-3.2, -0.1), (-3.2, d_y), 0.35), ((-1.0, -0.1), (-2.2, -0.1), (-2.2, d_y), -0.35)]
        for p0, p1, p2, s in segs:
            mx = (p0[0] + p1[0]) / 2 + dx
            half = 0.36
            sgn = 1 if p1[0] > p0[0] else -1
            jl.append(VGroup(wire(xs(p0), (mx - sgn * half, p0[1])), wire((mx + sgn * half, p0[1]), xs(p1), xs(p2)),
                             ebox(mx, p0[1], r"jX_L", C_IL, w=0.72, h=0.36, size=17)))
        jl.append(VGroup(wire((-2.7 + dx, 2.0), (-2.7 + dx, 1.25)), wire((-2.7 + dx, 0.75), (-2.7 + dx, d_y)),
                         ebox(-2.7 + dx, 1.0, r"jX_L", C_IL, w=0.72, h=0.36, size=17)))
        self.play(Create(nodes), run_time=0.7)
        self.play(*[FadeIn(j) for j in jl], run_time=1.6)
        self.wait(1.2)
        # ตรวจ
        self.say("เช็ค: ไม่มี R  ไม่มีชันต์  ไม่มีตัวเก็บประจุ  มีแต่ jX + แหล่ง E ต่อนิวทรัลร่วม", color=OK)
        self.play(*[Indicate(b[0], color=WHITE) for b in bx.values()], *[Indicate(j[2][0], color=C_IL) for j in jl], run_time=1.4)
        self.wait(2.0)
        remember(self, "reactance diagram: ทุกอุปกรณ์ = jX · บัส = จุดต่อ · เครื่องกำเนิดเริ่มจากนิวทรัล ผ่าน E → jX_G → jX_T",
                 "สายส่งทุกเส้น = jX_L (โจทย์นี้มี 5 เส้น)")


# =============================================================== P26  หน้า 26-30
class P26_PerUnitDef(Lesson):
    """นิยาม per-unit = ค่าจริง ÷ ค่าฐาน ไม่มีหน่วย + ตัวอย่าง Load Flow 1.03 p.u. + 4 ปริมาณ"""

    def construct(self):
        self.head("ค่าต่อหน่วย (Per-Unit) คืออะไร", "หน้า 26–30")
        self.say("เปอร์ยูนิต = ปริมาณจริง ÷ ปริมาณฐานอ้างอิง", color=OK)
        f = VGroup(T("เปอร์ยูนิต", 30, YEL), M(r"=", WHITE, 34), VGroup(T("ปริมาณจริง (Actual)", 26, C_A), Line(LEFT * 1.9, RIGHT * 1.9, color=WHITE, stroke_width=3),
                                                                   T("ปริมาณฐาน (Base)", 26, C_B)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=0.35)
        f.move_to([0, 0.6, 0])
        self.play(FadeIn(f[0]), FadeIn(f[1]), run_time=0.8)
        self.play(FadeIn(f[2][0]), Create(f[2][1]), FadeIn(f[2][2]), run_time=1.2)
        self.wait(1.2)
        self.say("คำตอบไม่มีหน่วย (ไม่ใช่ V ไม่ใช่ A) — เป็นแค่ 'กี่เท่าของฐาน'", color=GRAYTXT)
        self.play(Indicate(f[2][0], color=C_A), Indicate(f[2][2], color=C_B), run_time=1.0)
        self.wait(1.5)
        # ภาพ: แท่ง
        self.play(f.animate.scale(0.7).move_to([-3.8, 1.5, 0]), run_time=0.8)
        base = Rectangle(width=1.2, height=2.2, fill_color=C_B, fill_opacity=0.5, stroke_color=C_B).move_to([3.4, -1.1, 0])
        act = Rectangle(width=1.2, height=2.2 * 1.03, fill_color=C_A, fill_opacity=0.5, stroke_color=C_A).next_to(base, LEFT, buff=0.7).align_to(base, DOWN)
        bl = T("ฐาน = 1.00", 20, C_B).next_to(base, DOWN, buff=0.15)
        al = T("จริง = 1.03", 20, C_A).next_to(act, DOWN, buff=0.15)
        self.play(FadeIn(base), FadeIn(bl), run_time=0.7)
        self.play(FadeIn(act), FadeIn(al), run_time=0.9)
        self.wait(1.0)
        # หน้า 29
        self.newpage("หน้า 29")
        self.say("หน้า 29: โปรแกรม Load Flow รายงานแรงดันบัส  u = 1.03 p.u. = สูงกว่าฐาน 3 %", color=OK)
        card1 = card([("ผลจากโปรแกรม (สไลด์)", YEL), "Ul = 235.92 kV", "u = 1.03 p.u.", "phiu = 153.71 deg"], w=3.4, color=YEL, size=20).move_to([-4.3, -1.3, 0])
        self.play(FadeIn(card1), run_time=0.8)
        ck = VGroup(T("เช็คเอง (ไม่ได้อยู่ในสไลด์):", 17, GRAYTXT), M(r"235.92/1.03\approx 229\ kV\ \approx\ 230\ kV\ (base)", GRAYTXT, 22)).arrange(DOWN, buff=0.12).move_to([-3.2, -2.9, 0])
        fit_width(ck, 6.2)
        self.play(FadeIn(ck), Indicate(act, color=C_A), run_time=1.0)
        self.wait(2.0)
        # หน้า 30: 4 ปริมาณ
        self.newpage("หน้า 30")
        self.say("หน้า 30: ต้องทำเป็นเปอร์ยูนิตทั้ง 4 ปริมาณ", color=OK)
        self.play(FadeOut(VGroup(f, base, act, bl, al, card1, ck)), run_time=0.7)
        items = [("Z", "อิมพีแดนซ์", C_E), ("V", "แรงดัน", C_IL), ("I", "กระแส", C_IA), ("P,Q,S", "กำลังไฟฟ้า", C_B)]
        cards = VGroup(*[VGroup(M(a, c, 40), T(b, 24, c)).arrange(DOWN, buff=0.2) for a, b, c in items])
        for c, x in zip(cards, (-5.25, -1.75, 1.75, 5.25)):
            c.move_to([x, 0, 0])
        frames = VGroup(*[RoundedRectangle(width=3.0, height=2.0, corner_radius=0.12, stroke_color=c[0].get_color(), stroke_width=3).move_to(c) for c in cards])
        for c, fr in zip(cards, frames):
            self.play(FadeIn(c), Create(fr), run_time=0.7)
        self.wait(1.2)
        remember(self, "per-unit = ค่าจริง ÷ ค่าฐาน (ไม่มีหน่วย)  ทำครบ Z · V · I · S", "ใช้ได้ทั้งคำนวณลัดวงจรและ Load Flow")


# =============================================================== P31  หน้า 31-33
class P31_WhyBase(Lesson):
    """ทำไมต้องแปลงฐาน: 115kV -> T(350kVA,10%) -> 12kV -> 600 ohm ห้ามคิด I = E/(jXt+600)"""

    def construct(self):
        self.head("ทำไมต้องใช้ฐาน (Base) เดียวกัน", "หน้า 31–33")
        self.say("ปัญหา: จะหากระแสในวงจรที่มีหม้อแปลงคั่น ลองคิดตรงๆ ดู", color=OK)
        # single line
        Y = 1.4
        lin1 = wire((-6.3, Y), (-4.1, Y))
        tr = VGroup(Circle(radius=0.3, stroke_color=WHITE, stroke_width=3).move_to([-3.95, Y, 0]),
                    Circle(radius=0.3, stroke_color=WHITE, stroke_width=3).move_to([-3.65, Y, 0]))
        lin2 = wire((-3.35, Y), (-1.4, Y))
        ld = Rectangle(width=0.8, height=0.9, stroke_color=C_IA, stroke_width=3, fill_color=C_IA, fill_opacity=0.3).move_to([-1.0, Y, 0])
        tl = VGroup(T("115 kV", 20, C_E).move_to([-5.3, Y + 0.4, 0]), T("12 kV", 20, C_IL).move_to([-2.4, Y + 0.4, 0]),
                    T("350 kVA\nX = 10 %", 17, GRAYTXT).move_to([-3.8, Y - 0.95, 0]), M(r"600\ \Omega", C_IA, 22).move_to([0.1, Y, 0]))
        self.play(Create(VGroup(lin1, tr, lin2, ld)), FadeIn(tl), run_time=1.5)
        self.wait(0.8)
        # วงจรแทน
        top, bot = -0.5, -2.6
        e = src(-5.4, (top + bot) / 2, "", C_E, r=0.3)
        el = VGroup(MathTex(r"E=115\,kV", font_size=22, color=C_E).next_to(e, DOWN, buff=0.15))
        xt_ = coil_sym((-4.2, top), (-2.9, top), n=3, color=C_IF)
        rl = res_zig((-1.2, top), (-1.2, bot), color=C_IA)
        eq = VGroup(wire((-5.4, (top + bot) / 2 + 0.3), (-5.4, top), (-4.2, top)),
                    wire((-2.9, top), (-1.2, top)), wire((-5.4, (top + bot) / 2 - 0.3), (-5.4, bot), (-1.2, bot)),
                    xt_, rl, el, M(r"jX_t", C_IF, 22).move_to([-3.55, top + 0.4, 0]), M(r"600\,\Omega", C_IA, 22).move_to([-0.5, (top + bot) / 2, 0]))
        eq.add(e)
        self.play(Create(eq), run_time=1.4)
        f = M(r"I\ \neq\ \frac{E}{jX_t+600}\ \ [A]", WHITE, 34).move_to([3.7, -1.5, 0])
        self.play(Write(f), run_time=1.3)
        cross = Cross(f, stroke_color=C_E, stroke_width=6)
        self.play(Create(cross), run_time=0.7)
        self.wait(0.8)
        self.say("เพราะ: แรงดันคนละระดับ (115 kV กับ 12 kV) เนื่องจากต่อหม้อแปลง → ห้ามบวก/หารข้ามกัน", color=C_E)
        self.play(Indicate(tl[0], color=C_E), Indicate(tl[1], color=C_IL), run_time=1.4)
        self.wait(1.0)
        fix = card([("ต้องแปลงค่าให้อยู่ในฐานเดียวกันก่อน", YEL)], w=5.0, color=YEL, size=24).move_to([3.7, 0.3, 0])
        self.play(FadeIn(fix), run_time=0.8)
        self.wait(1.5)
        # หน้า 32-33
        self.newpage("หน้า 32–33")
        self.say("เลยต้องรู้จัก 2 ค่า: ค่าจริง (actual) กับ ค่าฐาน (base)", color=OK)
        self.play(FadeOut(VGroup(lin1, tr, lin2, ld, tl, eq, f, cross, fix)), run_time=0.8)
        ca = card([("ค่าจริง (actual)", C_A), "วัดได้ หรือคำนวณจากคุณสมบัติอุปกรณ์", "มักระบุในสเปก / แผ่นป้าย (name plate)"], w=5.6, color=C_A, size=20).move_to([-3.2, -0.3, 0])
        cb = card([("ค่าฐาน (base)", C_B), "ค่าที่ 'กำหนดขึ้น' เป็นเกณฑ์เทียบ", "มักกำหนดจากพิกัดอุปกรณ์ตัวใดตัวหนึ่ง", ("โดยมากใช้พิกัดเครื่องกำเนิดไฟฟ้า", YEL)], w=5.6, color=C_B, size=20).move_to([3.6, -0.3, 0])
        self.play(FadeIn(ca), run_time=0.9)
        self.wait(1.4)
        self.play(FadeIn(cb), run_time=0.9)
        self.wait(2.0)
        remember(self, "ข้ามหม้อแปลง = คนละระดับแรงดัน → แปลงทุกค่าให้อยู่ฐานเดียวกันก่อนคำนวณ", "ฐานเลือกจากพิกัดเครื่องกำเนิด (Generator Rating)")


# =============================================================== P34  หน้า 34-39
class P34_BaseDerive(Lesson):
    """เลือกฐาน 2 ตัว (กำลัง+แรงดัน) -> Ib = VA/V -> Zb = V/Ib = V^2/VA -> หน่วย kV, MVA"""

    def construct(self):
        self.head("หาปริมาณฐานทางไฟฟ้า (1 เฟส)", "หน้า 34–39")
        self.say("ปริมาณฐานมี 4 ตัว — แต่ 'เลือกเอง' แค่ 2 ตัว ที่เหลือหาจากสูตร", color=OK)
        four = [("V", "แรงดัน (V, kV)", C_IL), ("I", "กระแส (A)", C_IA), ("Z", "อิมพีแดนซ์ (Ω)", C_E), ("S", "กำลัง (kVA, MVA)", C_B)]
        cs = VGroup(*[VGroup(M(a + "_{b}", c, 34), T(b, 19, c)).arrange(DOWN, buff=0.15) for a, b, c in four]).arrange(RIGHT, buff=0.9).move_to([0, 0.6, 0])
        self.play(FadeIn(cs), run_time=1.0)
        self.wait(0.8)
        fr = VGroup(*[RoundedRectangle(width=2.6, height=1.5, corner_radius=0.1, stroke_color=c[0].get_color(), stroke_width=3).move_to(c) for c in cs])
        self.play(Create(fr[0]), Create(fr[3]), run_time=0.8)
        pick = T("เลือก 2 ตัว: กำลังฐาน + แรงดันฐาน", 24, YEL).move_to([0, -1.2, 0])
        self.play(FadeIn(pick), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(VGroup(cs, fr, pick)), run_time=0.7)
        # หน้า 35
        self.newpage("หน้า 35")
        self.say("เริ่มจากพิกัดเครื่องกำเนิด 1 เฟส:  V_LN (แรงดัน)  กับ  VA₁φ (กำลัง)", color=OK)
        bd = Board(self, x=-6.6, y=1.9, gap=0.12)
        bd.add(1, "ฐานที่เลือก", VGroup(M(r"V_{LN}\ [V]\ =\ V_{base}", C_IL, 28), M(r"VA_{1\phi}\ [VA]\ =\ S_{base}", C_B, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.1), color=OK, hold=1.3)
        # หน้า 36
        self.newpage("หน้า 36")
        self.say("กระแสฐาน: จาก I = S / V", color=C_IA)
        bd.add(2, "กระแสฐาน", M(r"I_{base}=\frac{S_{base}}{V_{base}}=\frac{VA_{1\phi}}{V_{LN}}", C_IA, 30), color=C_IA, hold=1.4)
        # หน้า 37-38
        self.newpage("หน้า 37–38")
        self.say("อิมพีแดนซ์ฐาน: จาก Z = V / I  แล้วแทน I จากข้อ 2", color=C_E)
        bd.add(3, "อิมพีแดนซ์ฐาน", VGroup(M(r"Z_{base}=\frac{V_{LN}}{I_{base}}=\frac{V_{LN}}{VA_{1\phi}/V_{LN}}", C_E, 28),
                                         M(r"Z_{base}=\frac{(V_{LN})^{2}}{VA_{1\phi}}", C_E, 34)).arrange(DOWN, aligned_edge=LEFT, buff=0.15), color=C_E, hold=1.6)
        # หน้า 39
        self.newpage("หน้า 39")
        self.say("ใช้งานจริง: V เป็น kV  กำลังเป็น MVA  → ได้ Z_base หน่วย Ω", color=OK)
        res = VGroup(M(r"Z_{base}=\frac{(kV_{LN})^{2}}{MVA_{1\phi}}\ \ [\Omega]", OK, 34)).move_to([3.3, -1.0, 0])
        box = SurroundingRectangle(res, color=OK, buff=0.25)
        self.play(Write(res), run_time=1.3)
        self.play(Create(box), run_time=0.6)
        self.wait(1.0)
        # โซ่
        chain = VGroup(M(r"V_b", C_IL, 30), M(r"\rightarrow", WHITE, 26), M(r"I_b", C_IA, 30), M(r"\rightarrow", WHITE, 26), M(r"Z_b", C_E, 30)).arrange(RIGHT, buff=0.3).move_to([3.3, 1.3, 0])
        ch2 = VGroup(M(r"S_b", C_B, 30)).next_to(chain[2], UP, buff=0.3)
        self.play(FadeIn(chain), FadeIn(ch2), run_time=1.0)
        self.play(Indicate(chain[0], color=C_IL), Indicate(ch2, color=C_B), run_time=0.8)
        self.play(Indicate(chain[2], color=C_IA), Indicate(chain[4], color=C_E), run_time=0.8)
        self.wait(2.0)
        remember(self, "เลือก S_b กับ V_b → I_b = S/V → Z_b = V²/S  (kV² / MVA = Ω)", "นี่คือค่าฐาน 1 เฟส · 3 เฟสดูคลิปหน้า 40–46")
