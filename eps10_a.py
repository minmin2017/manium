"""EPS10 ชุด a — แบบฝึกหัดท้ายบท (หน้า 50-52) + บทนำ (หน้า 1-2)
P01_Intro (1-2) · P50_Ex1 (50-51 ข้อ 1) · P51_Ex2 (50-51 ข้อ 2) · P52_Ex3 (50,52 ข้อ 3)
ตัวเลขทุกตัวจาก PDF บทที่ 10 ; MathTex ห้ามมีภาษาไทย
"""
from eps10_lib import *


# =============================================================== P01  หน้า 1-2
class P01_Intro(Lesson):
    def construct(self):
        self.head("หม้อแปลง: ทำไมต้องมี + อัตราส่วนรอบ", "หน้า 1–2")
        self.say("ไฟฟ้าเดินทาง 3 ช่วง แต่ละช่วงใช้แรงดันคนละระดับ", color=OK)
        boxes = []
        data = [("โรงไฟฟ้า", "MV  ≤ 10 kV", YEL, -4.6), ("สายส่งระยะไกล", "HV  400–800 kV", C_LOSS, 0.0), ("บ้าน / โรงงาน", "LV  400 / 230 V", OK, 4.6)]
        for name, v, c, x in data:
            r = RoundedRectangle(width=3.3, height=1.3, corner_radius=0.15, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.08).move_to([x, 0.9, 0])
            t1 = Text(name, font_size=24, color=c).move_to([x, 1.15, 0])
            t2 = Text(v, font_size=22, color=WHITE).move_to([x, 0.62, 0])
            boxes.append(VGroup(r, t1, t2))
        a1 = Arrow([-2.9, 0.9, 0], [-1.7, 0.9, 0], buff=0, color=GRAYTXT, stroke_width=4)
        a2 = Arrow([1.7, 0.9, 0], [2.9, 0.9, 0], buff=0, color=GRAYTXT, stroke_width=4)
        x1 = Text("หม้อแปลงเพิ่ม", font_size=18, color=GRAYTXT).move_to([-2.3, 0.0, 0])
        x2 = Text("หม้อแปลงลด", font_size=18, color=GRAYTXT).move_to([2.3, 0.0, 0])
        for b in boxes:
            self.play(FadeIn(b, shift=UP * 0.2), run_time=0.6)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(x1), FadeIn(x2), run_time=0.8)
        self.wait(1.0)
        self.say("ส่งไกลต้องแรงดันสูง: กำลังเท่ากัน V สูง → I ต่ำ → สูญเสีย I²R ต่ำ", color=YEL)
        f = M(r"P=VI\quad\Rightarrow\quad V\uparrow\ \ I\downarrow\ \ I^2R\downarrow", YEL, 34).move_to([0, -1.3, 0])
        self.play(Write(f), run_time=1.2)
        self.wait(1.5)
        k = self.keytext("ไฟ DC เปลี่ยนแรงดันยาก  ไฟ AC เปลี่ยนง่ายด้วยหม้อแปลง โดยใช้สนามแม่เหล็กเป็นสื่อกลาง", hold=2.0)
        self.clear()
        # ---- รูปหม้อแปลง
        self.say("แกนเหล็ก + ขด 2 ขด: ปฐมภูมิ (รับไฟ) และทุติยภูมิ (จ่ายโหลด)", color=OK)
        d = xf_pic(0, 0.55, s=1.0)
        self.play(FadeIn(d["core"]), run_time=0.6)
        self.play(FadeIn(d["c1"]), FadeIn(d["l1"]), FadeIn(d["src"]), Create(d["w1"]), run_time=0.8)
        self.play(FadeIn(d["c2"]), FadeIn(d["l2"]), run_time=0.6)
        t1 = Text("ปฐมภูมิ", font_size=20, color=C_P).move_to([-1.2, 1.75, 0])
        t2 = Text("ทุติยภูมิ", font_size=20, color=C_SEC).move_to([1.2, 1.75, 0])
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.5)
        self.say("ไฟ AC ในขดปฐมภูมิ → ฟลักซ์สลับวิ่งในแกน → เหนี่ยวนำแรงดันในขดทุติยภูมิ", color=C_PHI)
        self.play(FadeIn(d["flux"]), run_time=0.6)
        flux_flow(self, d, 2, run=1.0)
        self.play(FadeIn(d["load"]), Create(d["w2"]), run_time=0.7)
        self.say("ต่อโหลด: กระแสทุติยภูมิต้านฟลักซ์ (เลนซ์) → ปฐมภูมิดึงกระแสเพิ่มมาชดเชย", color=C_IA)
        self.play(flow(d["w2"][0], C_IA), flow(d["w1"][0], C_IA), run_time=1.2)
        self.play(flow(d["w2"][0], C_IA), flow(d["w1"][0], C_IA), run_time=1.2)
        # ---- สูตร
        self.say("ฟลักซ์ตัวเดียวกันผ่านทั้ง 2 ขด → แรงดันต่อรอบเท่ากัน", color=OK)
        self.play(VGroup(d["all"], d["flux"], t1, t2).animate.scale(0.75).move_to([0, 0.95, 0]), run_time=0.8)
        f = MathTex(r"a", "=", r"\frac{V_1}{V_2}", r"\approx", r"\frac{E_1}{E_2}", "=", r"\frac{N_1}{N_2}", "=", r"\frac{I_2}{I_1}", font_size=44)
        f.move_to([0, -1.35, 0])
        f[2].set_color(YEL)
        f[6].set_color(C_P)
        f[8].set_color(C_IA)
        self.play(Write(f), run_time=1.6)
        self.glow(f[6], VGroup(d["c1"], d["c2"]), color=C_P)
        self.glow(f[2], VGroup(d["src"], d["load"]), color=YEL)
        self.glow(f[8], VGroup(d["w1"], d["w2"]), color=C_IA)
        k = self.keytext("แรงดันเป็นสัดส่วนกับจำนวนรอบ  กระแสเป็นส่วนกลับ (กำลังเข้า = กำลังออก)", hold=2.2)
        self.clear()
        # ---- หน้า 2 สัญลักษณ์
        self.newpage("หน้า 2 · รูป 10-1")
        self.say("สัญลักษณ์: วงกลม 2 วงซ้อน = หม้อแปลง  (1 เฟส หรือ 3 เฟส)", color=OK)
        c1 = Circle(radius=0.55, color=WHITE, stroke_width=3).move_to([-3.0, 0.75, 0])
        c2 = Circle(radius=0.55, color=WHITE, stroke_width=3).move_to([-3.0, -0.1, 0])
        s1 = Text("หม้อแปลง", font_size=20, color=GRAYTXT).move_to([-3.0, -1.2, 0])
        k1 = coil_sym((1.6, 1.2), (1.6, -0.6), n=4, r=0.12, color=C_P)
        k2 = coil_sym((2.6, -0.6), (2.6, 1.2), n=4, r=0.12, color=C_SEC)
        bars = VGroup(*[Line([2.06 + dx, 1.1, 0], [2.06 + dx, -0.5, 0], color=METAL, stroke_width=3) for dx in (-0.06, 0.06)])
        s2 = Text("ขด 2 ขด + แกนเหล็ก (เส้นคู่)", font_size=20, color=GRAYTXT).move_to([2.1, -1.2, 0])
        self.play(Create(c1), Create(c2), FadeIn(s1), run_time=0.8)
        self.play(Create(k1), Create(k2), Create(bars), FadeIn(s2), run_time=1.0)
        self.say("แกนเหล็ก μ สูงมาก → ฟลักซ์เกือบทั้งหมดอยู่ในเหล็ก → 2 ขดควบคู่ทางแม่เหล็กแน่น", color=C_PHI)
        self.wait(1.5)
        remember(self, "a = N1/N2 = V1/V2 = I2/I1", "แรงดันตามจำนวนรอบ  กระแสสวนจำนวนรอบ")


# =============================================================== P50  หน้า 50-51 ข้อ 1
class P50_Ex1(Lesson):
    def construct(self):
        self.head("แบบฝึกหัดข้อ 1: อัตราส่วนรอบ → V2 และ I1", "หน้า 50–51 ข้อ 1")
        self.say("โจทย์: N1 = 230 รอบ  V1 = 380 V  N2 = 450 รอบ  จ่ายโหลด 10 A  →  หา a, V2, I1", color=OK)
        d = xf_pic(3.75, 0.75, s=0.78, n1=r"N_1=230", n2=r"N_2=450")
        v1 = M(r"V_1=380\,V", YEL, 24).move_to([d["src"].get_center()[0], 1.55, 0])
        i2 = M(r"I_2=10\,A", C_IA, 24).move_to([d["load"].get_center()[0], 1.55, 0])
        self.play(FadeIn(d["all"]), FadeIn(v1), FadeIn(i2), run_time=1.0)
        self.play(FadeIn(d["flux"]), run_time=0.4)
        flux_flow(self, d, 1)
        bd = Board(self, x=-6.6, y=2.1, gap=0.14)
        bd.add(1, "เข้าใจโจทย์", n_text("N2 มากกว่า N1  →  หม้อแปลงเพิ่มแรงดัน\nคาดว่า V2 > 380 V และ I1 > 10 A", size=20), hold=1.4)
        self.glow(d["l2"], d["c2"], color=C_SEC)
        sf = M(r"a=\frac{N_1}{N_2}=\frac{V_1}{V_2}=\frac{I_2}{I_1}", WHITE, 30)
        bd.add(2, "สูตร", sf, hold=1.0)
        s3 = VGroup(M(r"a=230/450=0.511", C_P, 28),
                    M(r"V_2=V_1/a=380/0.511=743.5\ V", YEL, 28),
                    M(r"I_1=I_2/a=10/0.511=19.57\ A", C_IA, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bd.add(3, "แทนค่า", s3, run=2.4, hold=1.4)
        self.glow(s3[1], d["load"], color=YEL)
        bd.add(4, "ตรวจ: กำลังเข้า = กำลังออก", M(r"380\times19.57=743.5\times10=7435\ VA", OK, 26), hold=1.4)
        self.say("เฉลยลายมือปัด a = 0.51 ก่อน → ได้ 745 V และ 19.6 A (ใกล้กัน ใช้ได้)", color=GRAYTXT)
        self.wait(2.0)
        remember(self, "รอบมากฝั่งไหน แรงดันสูงฝั่งนั้น  กระแสต่ำฝั่งนั้น",
                 "V2 = V1/a = 743.5 V    I1 = I2/a = 19.57 A")


# =============================================================== P51  หน้า 50-51 ข้อ 2
def _simple_xf(cy=0.6, s=1.0):
    """ปฐมภูมิ (Rp, Xp) - หม้อแปลงอุดมคติ - ทุติยภูมิ (Rs, Xs)"""
    zp = ebox(-3.3, cy + 0.6, r"R_p+jX_p", C_P, w=1.7, h=0.5, size=22)
    zs = ebox(3.3, cy + 0.6, r"R_s+jX_s", C_SEC, w=1.7, h=0.5, size=22)
    xi = xf_ideal(0, cy, h=1.3)
    w = VGroup(wire((-5.4, cy + 0.6), (-4.15, cy + 0.6)), wire((-2.45, cy + 0.6), (-0.17, cy + 0.6), (-0.17, cy + 0.65)),
               wire((-5.4, cy - 0.6), (-0.17, cy - 0.6), (-0.17, cy - 0.65)),
               wire((0.17, cy + 0.65), (0.17, cy + 0.6), (2.45, cy + 0.6)), wire((4.15, cy + 0.6), (5.4, cy + 0.6)),
               wire((0.17, cy - 0.65), (0.17, cy - 0.6), (5.4, cy - 0.6)))
    v1 = M(r"V_1=2300\,V", YEL, 24).move_to([-5.4, cy - 1.05, 0])
    v2 = M(r"V_2=230\,V", OK, 24).move_to([5.4, cy - 1.05, 0])
    e1 = M(r"E_1", C_P, 26).move_to([-0.75, cy, 0])
    e2 = M(r"E_2", C_SEC, 26).move_to([0.75, cy, 0])
    g = VGroup(w, zp, zs, xi, v1, v2, e1, e2)
    g.zp, g.zs, g.xi, g.e1, g.e2 = zp, zs, xi, e1, e2
    return g


class P51_Ex2(Lesson):
    def construct(self):
        self.head("แบบฝึกหัดข้อ 2: กระแสพิกัด แรงดันตก แรงเคลื่อน E", "หน้า 50–51 ข้อ 2")
        self.say("โจทย์: 1 เฟส ลดแรงดัน 2300 → 230 V  พิกัด 750 kVA 50 Hz  ทำงานที่พิกัด", color=OK)
        c = _simple_xf(cy=0.55)
        self.play(FadeIn(c), run_time=1.2)
        vals = VGroup(M(r"R_p=0.039\,\Omega\ \ X_p=0.28\,\Omega", C_P, 24),
                      M(r"R_s=0.00039\,\Omega\ \ X_s=0.0028\,\Omega", C_SEC, 24)).arrange(RIGHT, buff=0.8).move_to([0, -1.35, 0])
        self.play(FadeIn(vals), run_time=0.8)
        self.say("แรงดันที่ขั้ว V ไม่ใช่แรงเคลื่อนในขด E : ต่างกันตรงแรงดันตกที่ R + jX ของขดลวด", color=YEL)
        self.glow(c.zp, None, color=C_P)
        self.glow(c.e1, None, color=C_P)
        self.wait(1.0)
        self.clear()
        # ---- กระดาน 1
        self.say("ขั้น 1–2: กระแสพิกัด I = S / V และ ขนาดอิมพีแดนซ์ Z = sqrt(R² + X²)", color=OK)
        bd = Board(self, x=-6.6, y=2.1, gap=0.14)
        bd.add(1, "เข้าใจโจทย์", n_text("a = 2300/230 = 10   (ลดแรงดัน 10 เท่า กระแสเพิ่ม 10 เท่า)", size=21), hold=1.2)
        bd.add(2, "กระแสพิกัด", VGroup(M(r"I_1=\frac{S}{V_1}=\frac{750\times10^3}{2300}=326\ A", C_IA, 28),
                                     M(r"I_2=\frac{S}{V_2}=\frac{750\times10^3}{230}=3261\ A", C_IA, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
               run=2.0, hold=1.2)
        bd.add(3, "อิมพีแดนซ์ขด", VGroup(M(r"Z_1=\sqrt{0.039^2+0.28^2}=0.283\ \Omega", C_P, 28),
                                        M(r"Z_2=\sqrt{0.00039^2+0.0028^2}=2.827\ m\Omega", C_SEC, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
               run=2.0, hold=1.4)
        self.wait(1.0)
        self.clear()
        # ---- กระดาน 2
        self.say("ขั้น 3–4: แรงดันตก = I × Z  แล้ว  E = V − I Z  (ตามเฉลย ลบขนาด ไม่คิดมุม)", color=OK)
        bd2 = Board(self, x=-6.6, y=2.1, gap=0.14)
        bd2.add(3, "แรงดันตกในขด", VGroup(M(r"I_1Z_1=(326)(0.283)=92.258\ V", C_P, 28),
                                         M(r"I_2Z_2=(3261)(2.83\times10^{-3})=9.229\ V", C_SEC, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                run=2.0, hold=1.2)
        bd2.add(4, "แรงเคลื่อนเหนี่ยวนำ", VGroup(M(r"E_1=V_1-I_1Z_1=2300-92.258=2207.742\ V", YEL, 28),
                                               M(r"E_2=V_2-I_2Z_2=230-9.229=220.771\ V", OK, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                run=2.0, hold=1.4)
        bd2.add(5, "ตรวจ", VGroup(M(r"E_1/E_2=2207.7/220.77=10.0=a", OK, 28),
                                 M(r"Z_2\,a^2=0.002827\times100=0.2827=Z_1", GRAYTXT, 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                run=1.6, hold=1.6)
        self.say("Z2 อ้างอิงมาปฐมภูมิ (× a²) เท่ากับ Z1 พอดี → ขด 2 ข้างถูกออกแบบให้สูญเสียเท่ากัน", color=GRAYTXT)
        self.wait(2.0)
        remember(self, "I = S/V    Z = sqrt(R² + X²)    E1 = V1 − I1 Z1",
                 "ตอบ: 326 A, 3261 A, 0.283 Ω, 2.827 mΩ, 92.258 V, 9.229 V, 2207.742 V, 220.771 V")


# =============================================================== P52  หน้า 50,52 ข้อ 3
class P52_Ex3(Lesson):
    def construct(self):
        self.head("แบบฝึกหัดข้อ 3: หม้อแปลงไม่มีโหลด", "หน้า 50, 52 ข้อ 3")
        self.say("โจทย์: N1 = 264 รอบ  220 V 50 Hz  หน้าตัดแกน 25 ตร.ซม.  ทุติยภูมิเปิดวงจร", color=OK)
        d = xf_pic(3.6, 0.8, s=0.8, n1=r"N_1=264", n2=r"N_2", show_load=False)
        v1 = M(r"220\,V\ \ 50\,Hz", YEL, 22).move_to([d["src"].get_center()[0], 1.75, 0])
        ar = M(r"A=25\,cm^2", METAL, 22).move_to([3.6, -0.6, 0])
        self.play(FadeIn(d["all"]), FadeIn(v1), run_time=1.0)
        self.play(FadeIn(d["flux"]), FadeIn(ar), run_time=0.6)
        flux_flow(self, d, 1)
        bd = Board(self, x=-6.6, y=2.1, gap=0.14)
        bd.add(1, "(ก) ฟลักซ์สูงสุดในแกน", M(r"B_{max}=\frac{V_1}{\sqrt{2}\,\pi f N_1 A}", C_PHI, 32), hold=1.0)
        self.glow(bd.rows[-1][1], d["flux"], color=C_PHI)
        bd.add(2, "แทนค่า (A = 25×10⁻⁴ m²)", M(r"=\frac{220}{\sqrt{2}\,\pi(50)(264)(25\times10^{-4})}=1.5\ T", C_PHI, 30),
               run=2.0, hold=1.6)
        self.say("ที่มา: E = 4.44 f N Φmax  →  แรงดันที่จ่ายเป็นตัวกำหนดฟลักซ์ (หน้า 15–16)", color=GRAYTXT)
        self.wait(1.5)
        self.clear()
        # ---- (ข)
        self.say("(ข) ไม่มีโหลด กระแสที่ไหลคือกระแสกระตุ้น Iφ = Ic (สูญเสียแกน) + Im (สร้างฟลักซ์)", color=OK)
        v, ic, im, iphi = phasor_ix((3.2, -1.9), 3.4, 0.55, 3.0)
        lv = M(r"V_1", YEL, 28).next_to(v.get_end(), LEFT, buff=0.12)
        lic = M(r"I_c", C_LOSS, 26).next_to(ic, LEFT, buff=0.12)
        lim = M(r"I_m", C_MAG, 26).next_to(im, UP, buff=0.12)
        lip = M(r"I_\phi", C_IA, 26).next_to(iphi.get_center(), DOWN + RIGHT, buff=0.08)
        th = Arc(radius=0.55, start_angle=np.arctan2(0.55, 3.0), angle=PI / 2 - np.arctan2(0.55, 3.0), arc_center=np.array([3.2, -1.9, 0]),
                 color=WHITE, stroke_width=2)
        lth = M(r"\theta", WHITE, 24).move_to([3.62, -1.05, 0])
        self.play(GrowArrow(v), FadeIn(lv), run_time=0.7)
        self.play(GrowArrow(iphi), FadeIn(lip), run_time=0.7)
        self.play(GrowArrow(ic), FadeIn(lic), GrowArrow(im), FadeIn(lim), Create(th), FadeIn(lth), run_time=1.0)
        bd = Board(self, x=-6.6, y=2.1, gap=0.12)
        bd.add(1, "กระแสกระตุ้น", M(r"I_\phi=\frac{S}{V_1}=\frac{500}{220}=2.273\ A", C_IA, 28), hold=0.8)
        self.glow(bd.rows[-1][1], iphi, color=C_IA)
        bd.add(2, "ตัวประกอบกำลัง", M(r"PF=\cos\theta=\frac{P_c}{S}=\frac{50}{500}=0.1", WHITE, 28), hold=0.8)
        bd.add(3, "แยก 2 ส่วน", VGroup(M(r"I_c=I_\phi\cos\theta=(2.273)(0.1)=0.227\ A", C_LOSS, 26),
                                     M(r"I_m=I_\phi\sin\theta=(2.273)(0.995)=2.26\ A", C_MAG, 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
               run=2.0, hold=0.8)
        self.glow(bd.rows[-1][1][0], ic, color=C_LOSS)
        self.glow(bd.rows[-1][1][1], im, color=C_MAG)
        self.say("Ic เล็กมาก (PF 0.1) : กระแสไม่มีโหลดเกือบทั้งหมดใช้สร้างฟลักซ์  (เฉลยใช้ sin = 0.99 ได้ 2.25 A)", color=GRAYTXT)
        self.wait(1.5)
        self.clear()
        # ---- (ค)
        self.say("(ค) วงจรสมมูลของแกน = Rc ขนาน Xm  แรงดัน V1 คร่อมทั้งคู่", color=OK)
        top, botm, xl, xr = 1.0, -1.4, 2.2, 4.6
        sv = src(0.9, -0.2, "", YEL)
        wr = VGroup(wire((0.9, 0.07), (0.9, top), (xr, top)), wire((0.9, -0.47), (0.9, botm), (xr, botm)),
                    wire((xl, top), (xl, 0.6)), wire((xl, -1.0), (xl, botm)), wire((xr, top), (xr, 0.6)), wire((xr, -1.0), (xr, botm)))
        rc = res_zig((xl, 0.6), (xl, -1.0), color=C_LOSS)
        xm = ind_sym((xr, 0.6), (xr, -1.0), color=C_MAG)
        lrc = M(r"R_c", C_LOSS, 28).next_to(rc, LEFT, buff=0.2)
        lxm = M(r"X_m", C_MAG, 28).next_to(xm, RIGHT, buff=0.2)
        lic = M(r"I_c", C_LOSS, 24).move_to([xl + 0.45, -1.2, 0])
        lim = M(r"I_m", C_MAG, 24).move_to([xr - 0.45, -1.2, 0])
        self.play(FadeIn(sv), Create(wr), Create(rc), Create(xm), FadeIn(lrc), FadeIn(lxm), FadeIn(lic), FadeIn(lim), run_time=1.2)
        bd = Board(self, x=-6.6, y=2.1, gap=0.14)
        bd.add(1, "สูตร", M(r"R_c=\frac{V_1}{I_c}\qquad X_m=\frac{V_1}{I_m}", WHITE, 30), hold=0.8)
        bd.add(2, "แทนค่า", VGroup(M(r"R_c=\frac{220}{0.2273}=968\ \Omega", C_LOSS, 28),
                                  M(r"X_m=\frac{220}{2.25}=97.78\ \Omega", C_MAG, 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
               run=2.0, hold=0.8)
        self.glow(bd.rows[-1][1][0], rc, color=C_LOSS)
        self.glow(bd.rows[-1][1][1], xm, color=C_MAG)
        bd.add(3, "ตรวจ", M(r"P_c=\frac{V_1^2}{R_c}=\frac{220^2}{968}=50\ W", OK, 28), hold=1.0)
        self.say("⚠ เฉลยลายมือเขียน Rc = 50/2.273² = 9.678 Ω  ผิด! ใช้ Iφ แทน Ic  ที่ถูก 50/0.2273² = 968 Ω", color=C_LOSS)
        self.wait(2.5)
        remember(self, "ไม่มีโหลด: Iφ = S/V  PF = P/S  Ic = Iφ cosθ  Im = Iφ sinθ",
                 "Rc = V/Ic = 968 Ω (ไม่ใช่ 9.678)    Xm = V/Im = 97.78 Ω    Bmax = 1.5 T")
