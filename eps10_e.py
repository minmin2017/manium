"""EPS10 ชุด e — กลุ่มเวกเตอร์, ไม่สมมาตร, ออโต้, แปลงเฟส, หม้อแปลงวัด (หน้า 33-49)
P34_VectorGroups (33-37) · P38_Unbalanced (38-40) · P40_Auto (40-42) · P43_PhaseConv (42-45) · P46_InstrXf (45-49)
"""
from eps10_lib import *


def _ph(o, ang_deg, L, color, w=5):
    o = np.array([o[0], o[1], 0.0])
    a = ang_deg * DEGREES
    return Arrow(o, o + L * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=color, stroke_width=w, tip_length=0.2)


# =============================================================== P34  หน้า 33-37
class P34_VectorGroups(Lesson):
    def construct(self):
        self.head("กลุ่มเวกเตอร์ (Vector group): Yd5, Dd6, Yz11", "หน้า 33–37 · รูป 10-30, 10-31")
        self.say("ชื่อ 3 ส่วน: ตัวใหญ่ = ด้านแรงสูง (Y, D, Z)  ตัวเล็ก = ด้านแรงต่ำ (y, d, z)  ตัวเลข = มุม", color=OK)
        nm = MathTex(r"Y", r"d", r"5", font_size=90).move_to([-3.8, 0.6, 0])
        nm[0].set_color(C_P)
        nm[1].set_color(C_SEC)
        nm[2].set_color(YEL)
        self.play(Write(nm), run_time=1.0)
        t = VGroup(Text("Y = HV ต่อสตาร์", font_size=22, color=C_P), Text("d = LV ต่อเดลต้า", font_size=22, color=C_SEC),
                   Text("5 × 30° = 150° ล้าหลัง", font_size=22, color=YEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.6, -1.3, 0])
        for i in range(3):
            self.play(Indicate(nm[i], color=WHITE), FadeIn(t[i]), run_time=0.7)
        # นาฬิกา
        C = np.array([3.3, 0.0, 0])
        face = Circle(radius=1.9, color=GRAYTXT, stroke_width=3).move_to(C)
        nums = VGroup(*[Text(str(k), font_size=20, color=GRAYTXT).move_to(C + 2.2 * np.array([np.sin(k * PI / 6), np.cos(k * PI / 6), 0])) for k in range(1, 13)])
        hv = Arrow(C, C + UP * 1.7, buff=0, color=C_P, stroke_width=7, tip_length=0.25)
        self.play(Create(face), FadeIn(nums), GrowArrow(hv), run_time=1.0)
        self.say("คิดเป็นนาฬิกา: แรงสูง 1U ชี้ 12 นาฬิกา  แรงต่ำ 2U ชี้ที่ 'ตัวเลขกลุ่ม' (ทุกชั่วโมง = 30° ล้าหลัง)", color=YEL)
        k = ValueTracker(0.0)
        lv = always_redraw(lambda: Arrow(C, C + 1.15 * np.array([np.sin(k.get_value() * PI / 6), np.cos(k.get_value() * PI / 6), 0]), buff=0,
                                         color=C_SEC, stroke_width=7, tip_length=0.22))
        self.add(lv)
        for grp, lbl in ((5, "Yd5 → 150°"), (6, "Dd6 → 180°"), (11, "Yz11 → 330°")):
            self.play(k.animate.set_value(grp), run_time=1.4)
            tt = Text(lbl, font_size=28, color=YEL).move_to([0.2, -2.0, 0])
            self.play(FadeIn(tt), run_time=0.4)
            self.wait(0.8)
            self.play(FadeOut(tt), run_time=0.3)
        lv.clear_updaters()
        self.clear()
        # ---- อัตราส่วนแรงดันสาย
        self.newpage("หน้า 36–37 · รูป 10-31")
        self.say("อัตราส่วนแรงดันสาย ไม่ใช่แค่ w1/w2 — ขึ้นกับการต่อ", color=OK)
        self.say("ตัวอย่าง Yd: ขด HV รับแรงดันเฟส = VL/√3  ขด LV (เดลต้า) รับแรงดันสายเต็ม", color=OK)
        dv = MathTex(r"\frac{V_{L,HV}}{V_{L,LV}}", "=", r"\frac{\sqrt3\,V_{coil1}}{V_{coil2}}", "=", r"\frac{\sqrt3\,w_1}{w_2}", font_size=42).move_to([0, 1.3, 0])
        dv[4].set_color(YEL)
        self.play(Write(dv), run_time=1.4)
        self.glow(dv[4], None, color=YEL)
        rows = [("Dd0, Yy0, Dd6, Yy6", r"\frac{w_1}{w_2}", WHITE), ("Yd5, Yd11", r"\frac{\sqrt3\,w_1}{w_2}", C_P),
                ("Dy5, Dy11", r"\frac{w_1}{\sqrt3\,w_2}", C_SEC), ("Yz5, Yz11", r"\frac{2w_1}{\sqrt3\,w_2}", OK), ("Dz0, Dz6", r"\frac{2w_1}{3w_2}", GRAYTXT)]
        tab = VGroup(*[VGroup(Text(a, font_size=22, color=c), MathTex(b, font_size=32, color=c)).arrange(RIGHT, buff=0.4) for a, b, c in rows])
        tab.arrange_in_grid(rows=3, cols=2, buff=(0.8, 0.25), col_alignments="ll").move_to([0, -1.0, 0])
        self.play(FadeIn(tab, lag_ratio=0.2), run_time=1.6)
        self.wait(1.5)
        self.say("Z = ขดครึ่งรอบ 2 ส่วนอยู่คนละขา ต่ออนุกรม (ได้มุม 30° เพิ่ม)  /  ขนาน 3 เฟส ต้องกลุ่มเวกเตอร์เดียวกัน", color=GRAYTXT)
        self.wait(1.6)
        remember(self, "เลขกลุ่ม × 30° = มุมที่แรงต่ำล้าหลังแรงสูง (เหมือนเข็มนาฬิกา)",
                 "Yd → √3 w1/w2    Dy → w1/(√3 w2)    Yz → 2w1/(√3 w2)")


# =============================================================== P38  หน้า 38-40
class P38_Unbalanced(Lesson):
    def construct(self):
        self.head("โหลดไม่สมมาตร + ลำดับศูนย์ (Zero sequence)", "หน้า 38–40 · รูป 10-32, 10-33")
        self.say("ตัวอย่าง: หม้อแปลง Yy ไม่ต่อนิวทรัลปฐมภูมิ  มีโหลด 1 เฟสระหว่าง V กับนิวทรัลด้านทุติยภูมิ", color=OK)
        xs = [-1.5, 0.0, 1.5]
        names = ["U", "V", "W"]
        top = VGroup(*[ind_sym((x, 1.9), (x, 0.9), color=C_P) for x in xs])
        bot = VGroup(*[ind_sym((x, -0.3), (x, -1.3), color=C_SEC) for x in xs])
        tl = VGroup(*[Text("1" + n, font_size=18, color=C_P).move_to([x, 2.2, 0]) for x, n in zip(xs, names)])
        bl = VGroup(*[Text("2" + n, font_size=18, color=C_SEC).move_to([x, -1.6, 0]) for x, n in zip(xs, names)])
        ny = wire((-1.5, 0.9), (1.5, 0.9))
        ny2 = wire((-1.5, -0.3), (1.5, -0.3))
        self.play(Create(top), Create(bot), FadeIn(tl), FadeIn(bl), Create(ny), Create(ny2), run_time=1.2)
        sec = [MathTex(r"0", font_size=28, color=C_SEC), MathTex(r"I", font_size=28, color=C_IA), MathTex(r"0", font_size=28, color=C_SEC)]
        for x, m in zip(xs, sec):
            m.move_to([x + 0.42, -0.8, 0])
        self.play(*[FadeIn(m) for m in sec], run_time=0.6)
        self.say("แยกกระแส I: ลำดับศูนย์ I/3 ทุกเฟส + ลำดับบวก/ลบ — ปฐมภูมิ Y ไม่มีนิวทรัล ส่ง I/3 ลำดับศูนย์ไม่ได้", color=C_IA)
        pri = [MathTex(r"+\frac{I'}{3}", font_size=34, color=C_P), MathTex(r"-\frac{2I'}{3}", font_size=34, color=C_P), MathTex(r"+\frac{I'}{3}", font_size=34, color=C_P)]
        for x, m in zip(xs, pri):
            m.move_to([x + 0.55, 1.4, 0])
        self.play(*[FadeIn(m) for m in pri], run_time=0.8)
        self.say("ผล: ลำดับศูนย์ด้านทุติยภูมิไม่ถูกชดเชย → mmf เหลือทุกขา → ฟลักซ์ลำดับศูนย์", color=C_LOSS)
        zt = Text("ทุติยภูมิ: I/3 ทุกเฟส ไม่มีใครหักล้าง", font_size=22, color=C_LOSS).move_to([4.4, -0.8, 0])
        self.play(FadeIn(zt), run_time=0.6)
        self.wait(1.2)
        self.clear()
        # ---- จุดนิวทรัลเลื่อน
        self.newpage("หน้า 39 · รูป 10-33")
        self.say("จุดนิวทรัลเลื่อน (ΔU): แรงดันเฟสที่มีโหลดตก  เฟสอื่นสูงขึ้น/อิ่มตัว", color=OK)
        U, V, W = np.array([-2.6, 2.0, 0]), np.array([-0.4, -1.5, 0]), np.array([-4.8, -1.5, 0])
        tri = Polygon(U, V, W, color=GRAYTXT, stroke_width=3)
        lu = Text("1U", font_size=20).next_to(U, UP, buff=0.1)
        lvv = Text("1V", font_size=20).next_to(V, RIGHT, buff=0.1)
        lw = Text("1W", font_size=20).next_to(W, LEFT, buff=0.1)
        n0 = (U + V + W) / 3
        nt = ValueTracker(0.0)
        nd = always_redraw(lambda: Dot(n0 + nt.get_value() * np.array([0.6, 0.25, 0]), color=YEL, radius=0.09))
        sp = always_redraw(lambda: VGroup(*[Line(n0 + nt.get_value() * np.array([0.6, 0.25, 0]), P, color=C_PHI, stroke_width=3) for P in (U, V, W)]))
        self.play(Create(tri), FadeIn(lu), FadeIn(lvv), FadeIn(lw), run_time=0.8)
        self.add(sp, nd)
        self.play(nt.animate.set_value(1.0), run_time=2.0)
        du = MathTex(r"\Delta U", font_size=30, color=YEL).move_to(n0 + np.array([0.6, -0.45, 0]))
        self.play(FadeIn(du), run_time=0.5)
        rules = VGroup(Text("shell / 5 ขา / 1 เฟส 3 ตัว: หลีกเลี่ยงโหลดลำดับศูนย์", font_size=21, color=WHITE),
                       Text("core 3 ขา: จำกัด ≤ 10% ของกระแสพิกัด", font_size=21, color=WHITE),
                       Text("ทางแก้: ปฐมภูมิต่อ Δ  หรือ ทุติยภูมิต่อ z", font_size=21, color=OK),
                       Text("หรือ เพิ่มขดชดเชย Δ ระดับตติยภูมิ (tertiary)", font_size=21, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 0.2, 0])
        for r in rules:
            self.play(FadeIn(r, shift=LEFT * 0.2), run_time=0.6)
        for m in (nd, sp):
            m.clear_updaters()
        self.say("หมายเหตุหน้า 40: อิ่มตัว → กระแสแม่เหล็กมีฮาร์มอนิกที่ 3 (เป็นลำดับศูนย์) ต้องมี Δ ให้มันไหล ฟลักซ์จึงเป็นไซน์", color=GRAYTXT)
        self.wait(2.0)
        remember(self, "Y-y ไม่มีนิวทรัล + โหลด 1 เฟส → นิวทรัลเลื่อน",
                 "แก้ด้วย Δ (ปฐมภูมิ หรือ tertiary) หรือ ทุติยภูมิ z")


# =============================================================== P40  หน้า 40-42
class P40_Auto(Lesson):
    def construct(self):
        self.head("หม้อแปลงออโต้ (Autotransformer)", "หน้า 40–42 · รูป 10-34, 10-35")
        self.say("ขดเดียวต่อเนื่อง: ปฐมภูมิ w1 รอบ  ต่อขดเสริม w2+ อนุกรมด้านบน → ทุติยภูมิ w1 + w2+ รอบ", color=OK)
        x = -3.0
        c1 = ind_sym((x, 0.4), (x, -1.6), color=C_P, n=5)
        c2 = ind_sym((x, 2.0), (x, 0.4), color=C_SEC, n=3)
        win = VGroup(wire((-6.0, 0.4), (x, 0.4)), wire((x, 2.0), (0.0, 2.0)), wire((-6.0, -1.6), (0.0, -1.6)))
        dt = Dot([x, 0.4, 0], color=WHITE, radius=0.06)
        l1 = MathTex(r"w_1", font_size=28, color=C_P).move_to([x - 0.6, -0.6, 0])
        l2 = MathTex(r"w_{2+}", font_size=28, color=C_SEC).move_to([x - 0.65, 1.2, 0])
        v1 = MathTex(r"V_1", font_size=30, color=YEL).move_to([-5.6, -0.6, 0])
        v2 = MathTex(r"V_2", font_size=30, color=OK).move_to([-0.4, 0.2, 0])
        a1 = Arrow([-5.6, 0.3, 0], [-5.6, -1.5, 0], buff=0, color=YEL, stroke_width=3, tip_length=0.15)
        a2 = Arrow([-0.4, 1.9, 0], [-0.4, -1.5, 0], buff=0, color=OK, stroke_width=3, tip_length=0.15)
        self.play(Create(win), Create(c1), Create(c2), FadeIn(dt), FadeIn(l1), FadeIn(l2), run_time=1.4)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(v1), FadeIn(v2), run_time=0.8)
        al = MathTex(r"\alpha=\frac{w_{2+}}{w_1}", font_size=38, color=WHITE).move_to([3.5, 1.7, 0])
        f1 = MathTex(r"V_2", "=", r"(1+\alpha)", r"V_1", font_size=40).move_to([3.5, 0.6, 0])
        f2 = MathTex(r"I_1", "=", r"(1+\alpha)", r"I_2", font_size=40).move_to([3.5, -0.4, 0])
        f3 = MathTex(r"S=V_1I_1=V_2I_2", font_size=38, color=YEL).move_to([3.5, -1.4, 0])
        self.play(Write(al), run_time=0.8)
        self.play(Write(f1), run_time=0.9)
        self.glow(f1[2], VGroup(c1, c2), color=C_SEC)
        self.play(Write(f2), run_time=0.9)
        self.play(Write(f3), run_time=0.9)
        self.say("แต่กำลังที่ 'แปลงด้วยแม่เหล็กจริง' มีแค่ V2+ · I2 = V1 · I  ที่เหลือไหลผ่านลวดตรงๆ", color=YEL)
        self.play(flow(win[1], C_IA), flow(win[0], C_IA), run_time=1.2)
        self.wait(1.5)
        self.clear()
        # ---- ตัวอย่าง
        self.say("ตัวอย่าง (ตัวเลขสมมติ ไม่ได้มาจาก PDF): V1 = 200 V  α = 0.1  โหลด I2 = 50 A", color=YEL)
        bd = Board(self, x=-6.6, y=2.1, gap=0.12)
        bd.add(1, "แรงดัน", MathTex(r"V_2=(1+0.1)(200)=220\ V\qquad V_{2+}=20\ V", font_size=32, color=OK), hold=0.8)
        bd.add(2, "กระแส", MathTex(r"I_1=(1.1)(50)=55\ A\qquad I_{common}=\alpha I_2=5\ A", font_size=32, color=C_IA), hold=0.8)
        bd.add(3, "กำลัง", VGroup(MathTex(r"S=V_2I_2=220\times50=11\ kVA", font_size=32, color=YEL),
                                 MathTex(r"S_{magnetic}=V_{2+}I_2=20\times50=1\ kVA", font_size=32, color=C_SEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
               run=1.6, hold=0.8)
        bd.add(4, "ตรวจ", MathTex(r"\frac{1+\alpha}{\alpha}=\frac{1.1}{0.1}=11\ \text{times smaller core}", font_size=32, color=OK), hold=1.4)
        self.wait(0.8)
        self.clear()
        self.newpage("หน้า 42 · รูป 10-35")
        self.say("ข้อดี vs ข้อเสีย", color=OK)
        good = VGroup(Text("✓ เล็ก/เบากว่า (1+α)/α เท่า", font_size=23, color=OK),
                      Text("✓ สูญเสีย กระแสแม่เหล็ก รั่ว ต่ำกว่า", font_size=23, color=OK),
                      Text("ใช้: แรงดัน 2 ข้างต่างกันน้อย, ก๊อกปรับแรงดัน, สตาร์ทมอเตอร์", font_size=21, color=GRAYTXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.2, 0.3, 0])
        bad = VGroup(Text("✗ ไม่มีการแยกไฟฟ้าระหว่าง 2 ข้าง", font_size=23, color=C_LOSS),
                     Text("✗ รั่วน้อย → กระแสลัดวงจรสูง", font_size=23, color=C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        self.play(FadeIn(good, lag_ratio=0.3), run_time=1.2)
        self.play(FadeIn(bad, lag_ratio=0.3), run_time=1.0)
        self.wait(2.0)
        remember(self, "ออโต้: V2 = (1+α)V1   I1 = (1+α)I2   ขนาดเล็กลง (1+α)/α เท่า",
                 "แลกกับ: ไม่แยกไฟฟ้า + กระแสลัดวงจรสูง")


# =============================================================== P43  หน้า 42-45
class P43_PhaseConv(Lesson):
    def construct(self):
        self.head("แปลงจำนวนเฟส: 3→6 เฟส, สก็อต 3→2 เฟส, ก๊อกแรงดัน", "หน้า 42–45 · รูป 10-36, 10-37")
        self.say("3 → 6 เฟส: ทุติยภูมิ 2 ชุด ชุดที่สองกลับขั้ว → ได้ 6 เฟส ห่างกัน 60° (ใช้กับวงจรเรียงกระแส)", color=OK)
        O = np.array([-3.2, -0.2, 0])
        p3 = VGroup(*[_ph(O, a, 1.8, C_P) for a in (90, -30, 210)])
        self.play(*[GrowArrow(a) for a in p3], run_time=0.9)
        p6 = VGroup(*[_ph(O, a, 1.8, C_SEC) for a in (270, 150, 30)])
        self.play(*[GrowArrow(a) for a in p6], run_time=0.9)
        labs = VGroup(*[Text(t, font_size=18, color=GRAYTXT).move_to(O + 2.15 * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0]))
                        for t, a in (("a1", 90), ("a2", 30), ("a3", -30), ("a4", 270), ("a5", 210), ("a6", 150))])
        self.play(FadeIn(labs), run_time=0.6)
        t12 = Text("12 เฟส: เพิ่มชุดที่เลื่อนอีก 30° ด้วยการต่อ Δ", font_size=21, color=GRAYTXT).move_to([3.2, 1.5, 0])
        self.play(FadeIn(t12), run_time=0.5)
        self.wait(1.2)
        self.clear()
        # ---- สก็อต
        self.newpage("หน้า 43–45 · รูป 10-37")
        self.say("สก็อต (Scott): หม้อแปลง 1 เฟส 2 ตัว  ทุติยภูมิรอบเท่ากัน  ปฐมภูมิรอบ 1 : √3/2", color=OK)
        U, V, W = np.array([-3.0, 2.0, 0]), np.array([-1.2, -1.1, 0]), np.array([-4.8, -1.1, 0])
        o = (V + W) / 2
        tri = Polygon(U, V, W, color=GRAYTXT, stroke_width=2)
        vw = Line(W, V, color=C_SEC, stroke_width=7)
        ou = Line(o, U, color=C_P, stroke_width=7)
        lu = Text("U", font_size=22).next_to(U, UP, buff=0.1)
        lv = Text("V", font_size=22).next_to(V, RIGHT, buff=0.1)
        lw = Text("W", font_size=22).next_to(W, LEFT, buff=0.1)
        lo = Text("o (ก๊อกกลาง)", font_size=18, color=GRAYTXT).next_to(o, DOWN, buff=0.15)
        self.play(Create(tri), FadeIn(lu), FadeIn(lv), FadeIn(lw), run_time=0.8)
        self.play(Create(vw), FadeIn(lo), run_time=0.7)
        self.play(Create(ou), run_time=0.7)
        n1 = MathTex(r"V\!-\!W:\ \ w_1\ \text{turns}\ \ (\text{length } V_L)", font_size=28, color=C_SEC).move_to([3.0, 1.4, 0])
        n2 = MathTex(r"o\!-\!U:\ \ \tfrac{\sqrt3}{2}w_1\ \text{turns}\ \ (\text{length } \tfrac{\sqrt3}{2}V_L)", font_size=28, color=C_P).move_to([3.0, 0.6, 0])
        self.play(FadeIn(n1), run_time=0.6)
        self.play(FadeIn(n2), run_time=0.6)
        self.say("ความยาว o→U สั้นกว่า V→W เป็น √3/2 เท่า  รอบก็น้อยกว่า √3/2 เท่า → แรงดันต่อรอบเท่ากัน", color=YEL)
        self.glow(n2, ou, color=C_P)
        res = MathTex(r"V_B=-j\,V_A", font_size=42, color=OK).move_to([3.0, -0.6, 0])
        rt = Text("ได้ 2 เฟส ขนาดเท่ากัน ตั้งฉากกัน (90°)", font_size=22, color=OK).move_to([3.0, -1.4, 0])
        self.play(Write(res), FadeIn(rt), run_time=1.0)
        self.wait(1.5)
        self.clear()
        self.newpage("หน้า 45 · 10-15")
        self.say("หม้อแปลงควบคุมแรงดัน (tap changer): ก๊อกบนขด ชดเชยแรงดันตกในกริด ขั้นละ 2.5 %", color=OK)
        bars = VGroup(*[Rectangle(width=0.45, height=0.5 + 0.18 * i, stroke_color=YEL, fill_color=YEL, fill_opacity=0.25 + 0.08 * i).move_to([-2.0 + 0.6 * i, -0.6, 0], aligned_edge=DOWN) for i in range(7)])
        bl = Text("ขั้นละ 2.5 %", font_size=22, color=YEL).move_to([-0.2, -1.2, 0])
        self.play(FadeIn(bars, lag_ratio=0.15), FadeIn(bl), run_time=1.2)
        t2 = Text("ข้อควรระวัง: ค่าเหนี่ยวนำต้องคงที่ (แปรได้ 5–10 %)  และแรงบนขดต้องสมดุลทุกตำแหน่งก๊อก", font_size=20, color=GRAYTXT).move_to([0, -1.9, 0])
        self.play(FadeIn(t2), run_time=0.6)
        self.wait(1.6)
        remember(self, "สก็อต 3→2 เฟส: รอบปฐมภูมิ 1 : √3/2  ได้ VB = −j VA",
                 "3→6 เฟส: ชุดที่ 2 กลับขั้ว   ก๊อกปรับแรงดัน: ขั้นละ 2.5 %")


# =============================================================== P46  หน้า 45-49
class P46_InstrXf(Lesson):
    def construct(self):
        self.head("หม้อแปลงวัด: CT (กระแส) และ VT (แรงดัน)", "หน้า 46–49 · รูป 10-38 ถึง 10-41")
        self.say("หม้อแปลงวัด: 1 เฟส พิกัดต่ำ (< 1 kVA มักน้อยกว่า 100 VA) แยกเครื่องวัดออกจากแรงสูง", color=OK)
        core = Rectangle(width=2.2, height=2.0, stroke_color=METAL, stroke_width=16).move_to([-2.8, 0.2, 0])
        prim = VGroup(wire((-6.0, 0.45), (-4.2, 0.45), color=C_P, width=6), Ellipse(width=0.7, height=0.5, stroke_color=C_P, stroke_width=6).move_to([-3.9, 0.2, 0]),
                      wire((-4.2, -0.05), (-6.0, -0.05), color=C_P, width=6))
        i1 = MathTex(r"I_1", font_size=28, color=C_P).move_to([-5.4, 0.8, 0])
        sec = VGroup(*[Ellipse(width=0.55, height=0.13, stroke_color=C_SEC, stroke_width=3).move_to([-1.7, -0.5 + i * 0.18, 0]) for i in range(8)])
        am = meter((0.6, -1.4), "A", C_SEC)
        ws = VGroup(wire((-1.42, 0.76), (0.6, 0.76), (0.6, -1.13)), wire((-1.42, -0.5), (-1.0, -0.5), (-1.0, -1.4), (0.33, -1.4)))
        self.play(Create(core), Create(prim), FadeIn(i1), run_time=0.8)
        self.play(Create(sec), Create(ws), FadeIn(am), run_time=1.0)
        t1 = Text("ปฐมภูมิ: รอบน้อย (1 รอบ) อนุกรมกับสาย", font_size=20, color=C_P).move_to([-3.6, 1.75, 0])
        t2 = Text("ทุติยภูมิ: รอบมาก → แอมมิเตอร์ (เกือบลัดวงจร)", font_size=20, color=C_SEC).move_to([3.6, 0.6, 0])
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
        f = MathTex(r"I_2=I_1\frac{w_1}{w_2}", font_size=40, color=C_SEC).move_to([3.6, -0.3, 0])
        self.play(Write(f), run_time=0.8)
        self.say("ตัวอย่าง (ตัวเลขสมมติ): CT 100/5 A  แอมมิเตอร์อ่าน 4 A → กระแสสาย = 4 × 20 = 80 A", color=YEL)
        self.wait(1.6)
        self.say("⚠ ห้ามเปิดวงจรทุติยภูมิ CT ขณะสายมีกระแส: กระแสทั้งหมดกลายเป็นกระแสแม่เหล็ก → แรงดันสูงอันตราย", color=C_LOSS)
        x = Cross(am, stroke_color=C_LOSS, stroke_width=6)
        self.play(Create(x), Flash(am.get_center(), color=C_LOSS, flash_radius=0.6), run_time=1.0)
        self.wait(1.6)
        self.clear()
        self.newpage("หน้า 47 · สมการ 1.70 · ตาราง 10.1")
        self.say("ความผิดพลาดขนาด εi ≈ −(X + X2σ)/Xm2  → ต้อง Xm ใหญ่มาก (กระแสแม่เหล็กต่ำ)", color=OK)
        e = MathTex(r"\epsilon_i=\frac{I_2-I_1'}{I_1'}\approx-\frac{X+X_{2\sigma}}{X_{m2}}\qquad \tan\delta_i=\frac{R_2+R}{X_2+X}", font_size=34).move_to([0, 1.5, 0])
        self.play(Write(e), run_time=1.4)
        hdr = ["Class", "CT  ε %", "CT  δ (′)", "VT  ε %", "VT  δ (′)"]
        data = [["0.1", "0.1", "5", "0.1", "5"], ["0.5", "0.5", "30", "0.5", "20"], ["1", "1", "60", "1", "40"]]
        tb = VGroup()
        for r, row in enumerate([hdr] + data):
            for cidx, val in enumerate(row):
                tb.add(Text(val, font_size=22, color=(YEL if r == 0 else WHITE)).move_to([-4.0 + 2.0 * cidx, 0.4 - 0.55 * r, 0]))
        self.play(FadeIn(tb, lag_ratio=0.05), run_time=1.4)
        nt = Text("VT ใช้งานช่วง 0.8 – 1.2 V1n   (′ = arc minute)", font_size=20, color=GRAYTXT).move_to([0, -1.9, 0])
        self.play(FadeIn(nt), run_time=0.5)
        self.wait(1.5)
        self.clear()
        self.newpage("หน้า 48–49 · รูป 10-41")
        self.say("VT: ปฐมภูมิรอบมาก ต่อคร่อมสายแรงสูง  ทุติยภูมิรอบน้อย 100 หรือ 200 V → โวลต์มิเตอร์ (อิมพีแดนซ์สูง ≈ ไม่มีโหลด)", color=OK)
        d = xf_pic(0, 0.3, s=0.95, n1=r"w_1\ \text{(many)}", n2=r"w_2\ \text{(few)}", show_load=False)
        vm = meter((2.75, 0.3), "V", OK)
        vw = VGroup(wire((1.44, 0.73), (2.75, 0.73), (2.75, 0.57)), wire((1.44, -0.13), (2.75, -0.13), (2.75, 0.03)))
        self.play(FadeIn(d["all"]), FadeIn(vm), Create(vw), run_time=1.0)
        f2 = MathTex(r"V_2=V_1\frac{w_2}{w_1}", font_size=40, color=OK).move_to([0, -1.8, 0])
        self.play(Write(f2), run_time=0.8)
        self.wait(1.5)
        remember(self, "CT: อนุกรมกับสาย ทุติยภูมิห้ามเปิดวงจร   VT: ขนานกับสาย ทำงานเกือบไม่มีโหลด",
                 "Class = % ผิดพลาดขนาด (0.1 / 0.5 / 1)")
