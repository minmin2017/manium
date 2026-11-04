"""EPSX (ข้อสอบเก่า EPS): Q01-Q05 = ข้อสอบปลายภาค 2/2564 (ข้อ 1-5), M14/M15 = มิดเทอม 1/2564 ข้อ 14-15,
PR01-PR05 = ข้อฝึกบทที่ 11 (Claude เขียนเอง ไม่ใช่ข้อสอบจริง)  ดู epsx_lib.py   กฎ: MathTex ห้ามมีภาษาไทย
"""
from epsx_lib import *


# =============================================================== Q01 ข้อสอบปลายภาค 2/2564 ข้อ 1
class Q01_F64_LongShunt(Solve):
    def construct(self):
        self.head("ข้อสอบปลายภาค 2/2564 ข้อ 1 · compound long-shunt", "final 2/2564 · ข้อ 1 · รูปที่ 1")
        self.say("เครื่องกำเนิดผสม long-shunt 10 kW 125 V · สูญเสียหมุน 580 W · จ่ายเต็มพิกัด", color=OK)
        fig = cg_fig("long", r"R_f=62.5\,\Omega", r"R_a=0.12\,\Omega", r"R_{se}=0.022\,\Omega", r"V_t=125\,V", r"10\,kW")
        self.play(Create(fig), run_time=2.0)
        self.wait(2.0)
        self.say("ใจความ: long-shunt = ชันท์ต่อคร่อมขั้ว Vt  ดังนั้น Ia = Is = IL + If", color=YEL)
        self.play(flow(fig.sh_top, C_IF, run=1.4), Indicate(fig.ser, color=C_IS, scale_factor=1.12))
        self.wait(1.2)
        self.say("ทำทีละขั้น: เข้าใจโจทย์ → สูตร → แทนค่า → ตรวจ", color=GRAYTXT)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("ให้ Vt = 125 V , P = 10 kW , สูญเสียหมุน 580 W", 21),
                           T("หา (ก) Ia (ข) E (ค) Cu loss (ง) ประสิทธิภาพ", 21)], OK),
            ("กระแสโหลด และกระแสชันท์", [M(r"I_L=\frac{10000}{125}=80\,A", color=C_IL),
                                    M(r"I_f=\frac{V_t}{R_f}=\frac{125}{62.5}=2\,A", color=C_IF)], OK),
            ("(ก) กระแสอาร์เมเจอร์", M(r"I_a=", r"I_L", r"+", r"I_f", r"=80+2=82\,A"), C_IA),
        ])
        b = r[2][1]
        self.glow(b[1], fig.il, color=C_IL)
        self.glow(b[3], fig.if_, color=C_IF)
        self.play(Indicate(fig.ia, color=C_IA), Indicate(fig.is_, color=C_IS), run_time=1.0)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("(ข) แรงเคลื่อน E", [M(r"E=", r"V_t", r"+", r"I_a", r"(R_a+R_{se})"),
                              M(r"E=125+82(0.12+0.022)=136.64\,V", color=C_E)], C_E),
            ("(ค) Cu loss ทั้งหมด", [M(r"I_a^2R_a=82^2(0.12)=806.9\,W", color=C_IA),
                                 M(r"I_a^2R_{se}=82^2(0.022)=147.9\,W", color=C_IS),
                                 M(r"I_f^2R_f=2^2(62.5)=250\,W", color=C_IF),
                                 M(r"P_{cu}=806.9+147.9+250=1204.8\,W", color=OK)], OK),
        ], start=4)
        self.glow(r[0][1][0][4], VGroup(fig.ra_l, fig.rs_l), color=C_IA)
        self.wait(1.5)
        self.clear(bd)
        bd, r = self.rows([
            ("(ง) ประสิทธิภาพ", [M(r"P_{in}=P_{out}+P_{cu}+P_{rot}"),
                              M(r"P_{in}=10000+1204.8+580=11784.8\,W"),
                              M(r"\eta=\frac{10000}{11784.8}=84.86\,\%", color=OK)], OK),
            ("ตรวจ", [M(r"E\,I_a=136.64(82)=11204.8\,W"), M(r"11204.8+580=11784.8=P_{in}"),
                    T("ตรงกับ Pin  ✓", 22, OK)], GRAYTXT),
        ], start=6)
        self.wait(2.5)
        self.final([M(r"I_a=82\,A\qquad E=136.64\,V", color=OK, size=34),
                    M(r"P_{cu}=1204.8\,W\qquad \eta=84.86\,\%", color=OK, size=34)],
                   "long-shunt: Ia = IL + If · E = Vt + Ia(Ra + Rse) · η = Pout ÷ (Pout + Cu + หมุน)",
                   "บทที่ 7 ตย.7-6 long-shunt (คลิป EP19) · บทที่ 8 หน้า 16-17 รูป 8-8")


# =============================================================== Q02 ไดเวอร์เตอร์
class Q02_F64_Diverter(Solve):
    def construct(self):
        self.head("ข้อสอบปลายภาค 2/2564 ข้อ 2 · ไดเวอร์เตอร์", "final 2/2564 · ข้อ 2")
        self.say("ผสม 100 kW 600 V · อยากได้ 625 V ที่ 135 A · ชันท์ต้องเพิ่มอีก 2.3 A · ชันท์ 400 รอบ · เซรี่ 7.5 รอบ", color=OK)
        nl, nr = (1.6, 0.15), (6.0, 0.15)
        w_in = wire((0.7, 0.15), nl)
        w_out = wire(nr, (6.9, 0.15))
        w_t = wire(nl, (1.6, 1.05), (2.1, 1.05))
        ser = coil_sym([2.1, 1.05], [5.5, 1.05], n=5, r=0.1, color=C_IS)
        w_t2 = wire((5.5, 1.05), (6.0, 1.05), nr)
        w_b = wire(nl, (1.6, -0.75), (2.1, -0.75))
        rd = res_zig([2.1, -0.75], [5.5, -0.75], n=5, color=C_R)
        w_b2 = wire((5.5, -0.75), (6.0, -0.75), nr)
        d1, d2 = Dot([*nl, 0], radius=0.08, color=WHITE), Dot([*nr, 0], radius=0.08, color=WHITE)
        i_in = cur([0.75, 0.5], [1.45, 0.5], r"135\,A", C_IA, UP, size=20)
        i_s = cur([2.9, 1.45], [3.9, 1.45], r"I_s=?", C_IS, UP, size=22)
        i_d = cur([2.9, -1.1], [3.9, -1.1], r"I_d=?", C_IL, DOWN, size=22)
        l_se = MathTex(r"R_{se}=0.009\,\Omega", font_size=18, color=C_IS).move_to([3.8, 0.55, 0])
        l_d = MathTex(r"R_d=?", font_size=20, color=C_R).move_to([3.8, -0.3, 0])
        fig = VGroup(w_in, w_out, w_t, ser, w_t2, w_b, rd, w_b2, d1, d2, i_in, i_s, i_d, l_se, l_d)
        self.play(Create(fig), run_time=1.8)
        t1 = fit_width(T("ชันท์เพิ่ม 2.3 A × 400 รอบ = 920 AT", 18, C_IF), 5.6).move_to([3.7, -1.95, 0])
        bar1 = Rectangle(width=4.4, height=0.3, stroke_color=C_IF, stroke_width=3, fill_color=C_IF, fill_opacity=0.35)
        bar1.move_to([3.7, -2.35, 0])
        t2 = fit_width(T("เซรี่ต้องให้เท่ากัน = 7.5 รอบ × Is", 18, C_IS), 5.6).move_to([3.7, -2.85, 0])
        bar2 = Rectangle(width=4.4, height=0.3, stroke_color=C_IS, stroke_width=3, fill_color=C_IS, fill_opacity=0.35)
        bar2.move_to([3.7, -3.2, 0])
        self.say("ไอเดีย: ให้เซรี่ฟิลด์สร้างแอมแปร์-เทิร์นเท่ากับที่ชันท์จะต้องเพิ่ม  แล้วเอาไดเวอร์เตอร์แบ่งกระแสส่วนเกิน", color=YEL)
        self.play(FadeIn(t1), GrowFromEdge(bar1, LEFT), run_time=1.0)
        self.play(FadeIn(t2), GrowFromEdge(bar2, LEFT), run_time=1.0)
        self.wait(1.2)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("ชันท์ 400 รอบ , เซรี่ 7.5 รอบ , ชันท์ต้องเพิ่ม 2.3 A", 21), T("กระแสโหลด 135 A , Rse = 0.009 โอห์ม", 21),
                           T("หา Rd ของไดเวอร์เตอร์", 21)], OK),
            ("แอมแปร์-เทิร์นต้องเท่ากัน", [M(r"N_s", r"I_s", r"=", r"N_f", r"\Delta I_f"),
                                      M(r"7.5\,I_s=400(2.3)=920"),
                                      M(r"I_s=\frac{920}{7.5}=122.67\,A", color=C_IS)], C_IS),
        ])
        self.glow(r[1][1][0][1], i_s, color=C_IS)
        self.glow(r[1][1][0][3], VGroup(t1, bar1), color=C_IF)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("กระแสที่ไดเวอร์เตอร์รับ", [M(r"I_d=I-I_s=135-122.67=12.33\,A", color=C_IL)], C_IL),
            ("ขนานกัน แรงดันตกเท่ากัน", [M(r"I_d", r"R_d", r"=", r"I_s", r"R_{se}"),
                                    M(r"R_d=\frac{122.67(0.009)}{12.33}=0.0895\,\Omega", color=C_R)], C_R),
            ("ตรวจ", [M(r"I_d<I_s\ \Rightarrow\ R_d>R_{se}"), M(r"0.0895>0.009"), T("สอดคล้อง  ✓", 22, OK)], GRAYTXT),
        ], start=3)
        self.glow(r[1][1][0][1], l_d, color=C_R)
        self.glow(r[1][1][0][4], l_se, color=C_IS)
        self.wait(2.0)
        self.final([M(r"I_s=122.67\,A\qquad I_d=12.33\,A", color=OK, size=34),
                    M(r"R_d=0.0895\,\Omega", color=OK, size=36)],
                   "หา Is จาก Ns·Is = Nf·ΔIf  →  Id = I − Is  →  Rd = Is·Rse ÷ Id",
                   "บทที่ 8 หน้า 25-26 (สมการ 8-6 + ตย.8-7 คลิป EPS8_P25, P26)")


# =============================================================== Q03 แรงดันเพิ่มขึ้น (over-compound) + voltage regulation
class Q03_F64_OverCompoundVR(Solve):
    def construct(self):
        self.head("ข้อสอบปลายภาค 2/2564 ข้อ 3 · ผสมเกิน + voltage regulation", "final 2/2564 · ข้อ 3")
        self.say("ผสมแบบแรงดันเพิ่มขึ้น: ขั้ว 130 V ตอนจ่ายโหลดไกล · สายตก 10 V · ปลดโหลดแล้วขั้วเหลือ 120 V", color=OK)
        g = VGroup(Circle(radius=0.38, stroke_color=C_E, stroke_width=3, fill_color=C_E, fill_opacity=0.15).move_to([1.0, 0.95, 0]),
                   Text("G", font_size=22, color=C_E).move_to([1.0, 0.95, 0]))
        w1 = wire((1.38, 0.95), (1.9, 0.95))
        line = res_zig([1.9, 0.95], [4.1, 0.95], n=4, color=WARN)
        w2 = wire((4.1, 0.95), (5.2, 0.95))
        load = VGroup(Rectangle(width=0.8, height=0.8, stroke_color=GRAYTXT, stroke_width=3, fill_color=GRAYTXT,
                                fill_opacity=0.15).move_to([5.6, 0.95, 0]), Text("โหลด", font_size=17, color=WHITE).move_to([5.6, 0.95, 0]))
        l_line = T("สายตก 10 V", 17, WARN).move_to([3.0, 0.45, 0])
        vg1 = M(r"V_G=130\,V", color=C_E, size=24).move_to([1.0, 1.75, 0])
        vl1 = M(r"V_{load}=?", color=C_IL, size=24).move_to([5.6, 1.75, 0])
        self.play(Create(VGroup(g, w1, line, w2)), FadeIn(load), FadeIn(l_line), run_time=1.4)
        self.play(FadeIn(vg1), FadeIn(vl1), run_time=0.7)
        self.wait(1.5)
        self.say("ผสมเกิน: โหลดมาก → ฟลักซ์เซรี่ช่วยมาก → Vt ขั้ว สูงขึ้น  (ชดเชยแรงดันตกในสายส่ง)", color=YEL)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("เต็มโหลด: Vt ขั้ว = 130 V , สายตก = 10 V", 21), T("ไม่มีโหลด: Vt ขั้ว = 120 V", 21),
                           T("หา (ก) V ที่โหลด (ข) V ขั้วตอนไม่มีโหลด (ค) VR %", 21)], OK),
            ("(ก) แรงดันที่โหลด", [M(r"V_{load}=V_{G}-V_{drop}", color=WHITE), M(r"V_{load}=130-10=120\,V", color=C_IL)], C_IL),
        ])
        vl2 = M(r"V_{load}=120\,V", color=C_IL, size=24).move_to(vl1)
        self.play(ReplacementTransform(vl1, vl2), run_time=0.7)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("(ข) แรงดันขั้วตอนไม่มีโหลด", [T("โจทย์ให้ตรง ๆ: ปลดโหลดแล้วขั้วเหลือ 120 V", 21),
                                     M(r"V_{NL}=120\,V", color=C_E)], C_E),
        ], start=3)
        self.play(FadeOut(load), Indicate(vg1, color=WHITE), run_time=0.8)
        vg2 = M(r"V_G=120\,V", color=C_E, size=24).move_to(vg1)
        self.play(ReplacementTransform(vg1, vg2), run_time=0.8)
        self.wait(1.0)
        base_y, k = -2.6, 0.07

        def vbar(x, v, col):
            h = (v - 100) * k
            rr = Rectangle(width=0.9, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35)
            rr.move_to([x, base_y + h / 2, 0])
            return VGroup(rr, M(str(v) + r"\,V", color=col, size=22).next_to(rr, UP, buff=0.08))

        axis = Line([0.7, base_y, 0], [6.9, base_y, 0], color=GRAYTXT, stroke_width=3)
        b1, b2, b3 = vbar(1.6, 120, C_E), vbar(3.8, 130, C_E), vbar(6.0, 120, C_IL)
        lb = [T("ไม่มีโหลด\n(ขั้ว G)", 15, GRAYTXT).move_to([1.6, base_y - 0.45, 0]),
              T("เต็มโหลด\n(ขั้ว G)", 15, GRAYTXT).move_to([3.8, base_y - 0.45, 0]),
              T("เต็มโหลด\n(ที่โหลด)", 15, GRAYTXT).move_to([6.0, base_y - 0.45, 0])]
        self.play(Create(axis), FadeIn(b1), FadeIn(b2), FadeIn(b3), *[FadeIn(x) for x in lb], run_time=1.4)
        self.wait(1.5)
        self.clear(bd)
        bd, r = self.rows([
            ("(ค) voltage regulation", [M(r"VR=\frac{V_{NL}-V_{FL}}{V_{FL}}\times100"),
                                    M(r"VR=\frac{120-130}{130}\times100=-7.69\,\%", color=OK)], OK),
            ("ความหมาย", [T("ติดลบ = ผสมเกิน (โหลดมาก Vt ขั้วสูงขึ้น)", 21),
                         T("ที่ปลายโหลด: (120−120)÷120 = 0 %  คือชดเชยสายพอดี", 21, GRAYTXT)], GRAYTXT),
        ], start=4)
        self.glow(r[0][1][1], b2, color=C_E)
        self.wait(2.5)
        self.final([M(r"V_{load}=120\,V\qquad V_{NL}=120\,V", color=OK, size=34),
                    M(r"VR=-7.69\,\%\ (\text{over-compound})", color=OK, size=34)],
                   "VR = (ไม่มีโหลด − เต็มโหลด) ÷ เต็มโหลด · ผสมเกิน VR ติดลบ",
                   "บทที่ 8 หน้า 18-19 (ผสมเกิน/ผสมพอดี/ผสมขาด) · บทที่ 9 นิยาม voltage regulation")


# =============================================================== Q04 short-shunt
class Q04_F64_ShortShunt(Solve):
    def construct(self):
        self.head("ข้อสอบปลายภาค 2/2564 ข้อ 4 · compound short-shunt", "final 2/2564 · ข้อ 4 · รูปที่ 2")
        self.say("short-shunt จ่าย 50 A ที่ 500 V · Ra 0.162 โอห์ม · Rse 0.08 โอห์ม · Rf 200 โอห์ม · สูญเสียหมุน 520 W", color=OK)
        fig = cg_fig("short", r"R_f=200\,\Omega", r"R_a=0.162\,\Omega", r"R_{se}=0.08\,\Omega", r"V_t=500\,V", r"Load",
                     il_t=r"I_L=50\,A")
        self.play(Create(fig), run_time=2.0)
        self.wait(1.8)
        self.say("ใจความ: short-shunt = ชันท์คร่อมอาร์เมเจอร์อย่างเดียว  → Ise = IL  และ Vชันท์ = Vt + Ise·Rse", color=YEL)
        self.play(flow(fig.sh_top, C_IF, run=1.4), Indicate(fig.ser, color=C_IS, scale_factor=1.12))
        self.wait(1.2)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("Vt = 500 V , IL = 50 A , สูญเสียหมุน 520 W", 21),
                           T("หา (ก) Ia (ข) E (ค) Cu loss (ง) η", 21)], OK),
            ("แรงดันคร่อมชันท์", [M(r"V_{sh}=", r"V_t", r"+", r"I_L", r"R_{se}"), M(r"V_{sh}=500+50(0.08)=504\,V", color=C_IF)], C_IF),
            ("(ก) กระแสอาร์เมเจอร์", [M(r"I_f=\frac{504}{200}=2.52\,A", color=C_IF),
                                 M(r"I_a=I_L+I_f=50+2.52=52.52\,A", color=C_IA)], C_IA),
        ])
        self.glow(r[1][1][0][3], fig.il, color=C_IL)
        self.glow(r[1][1][0][4], fig.rs_l, color=C_IS)
        self.play(Indicate(fig.ia, color=C_IA), run_time=0.9)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("(ข) แรงเคลื่อน E", [M(r"E=", r"V_{sh}", r"+", r"I_a", r"R_a"),
                              M(r"E=504+52.52(0.162)=512.51\,V", color=C_E)], C_E),
            ("(ค) Cu loss ทั้งหมด", [M(r"I_a^2R_a=52.52^2(0.162)=446.9\,W", color=C_IA),
                                 M(r"I_L^2R_{se}=50^2(0.08)=200\,W", color=C_IS),
                                 M(r"I_f^2R_f=2.52^2(200)=1270.1\,W", color=C_IF),
                                 M(r"P_{cu}=446.9+200+1270.1=1916.9\,W", color=OK)], OK),
        ], start=4)
        self.glow(r[0][1][0][4], fig.ra_l, color=C_IA)
        self.wait(1.5)
        self.clear(bd)
        bd, r = self.rows([
            ("(ง) ประสิทธิภาพ", [M(r"P_{out}=V_tI_L=500(50)=25000\,W"),
                              M(r"P_{in}=25000+1916.9+520=27436.9\,W"),
                              M(r"\eta=\frac{25000}{27436.9}=91.12\,\%", color=OK)], OK),
            ("ตรวจ", [M(r"E\,I_a=512.51(52.52)=26916.9\,W"), M(r"26916.9+520=27436.9=P_{in}"),
                    T("ตรงกับ Pin  ✓", 22, OK)], GRAYTXT),
        ], start=6)
        self.wait(2.5)
        self.final([M(r"I_a=52.52\,A\qquad E=512.51\,V", color=OK, size=34),
                    M(r"P_{cu}=1916.9\,W\qquad \eta=91.12\,\%", color=OK, size=34)],
                   "short-shunt: Vชันท์ = Vt + IL·Rse · Ia = IL + If · E = Vชันท์ + Ia·Ra",
                   "บทที่ 7 ตย.7-7 short-shunt (คลิป EP20) · บทที่ 8 หน้า 16-17 รูป 8-8")


# =============================================================== Q05 ต่อขนานเครื่องผสม cumulative + equalizer
def _sw(x, y0, y1, label):
    mid = (y0 + y1) / 2
    w1 = wire((x, y0), (x, mid - 0.15))
    w2 = wire((x, mid + 0.15), (x, y1))
    blade = Line([x, mid - 0.15, 0], [x + 0.3, mid + 0.2, 0], color=WHITE, stroke_width=4)
    closed = Line([x, mid - 0.15, 0], [x, mid + 0.15, 0], color=WHITE, stroke_width=4)
    lab = MathTex(label, font_size=22, color=WHITE).move_to([x + 0.55, mid, 0])
    g = VGroup(w1, w2, blade, lab, Dot([x, mid - 0.15, 0], radius=0.05), Dot([x, mid + 0.15, 0], radius=0.05))
    g.blade, g.closed = blade, closed
    return g


class Q05_F64_ParallelEqualizer(Solve):
    def construct(self):
        self.head("ข้อสอบปลายภาค 2/2564 ข้อ 5 · ผสม cumulative 2 เครื่องขนานกัน", "final 2/2564 · ข้อ 5")
        self.say("โจทย์: เขียนไดอะแกรมต่อเครื่องกำเนิดผสมชนิด cumulative 2 เครื่องขนานกัน โดยใช้สวิตช์ 2 ตัว", color=OK)
        a1 = arm_sym([1.7, -0.9], r=0.42, letter="G_1")
        a2 = arm_sym([5.0, -0.9], r=0.42, letter="G_2")
        up1, up2 = wire((1.7, -0.45), (1.7, 0.5)), wire((5.0, -0.45), (5.0, 0.5))
        dn1, dn2 = wire((1.7, -1.35), (1.7, -2.6)), wire((5.0, -1.35), (5.0, -2.6))
        s1 = coil_sym([1.7, 0.5], [2.9, 0.5], n=4, r=0.1, color=C_IS)
        s2 = coil_sym([5.0, 0.5], [3.7, 0.5], n=4, r=0.1, color=C_IS)
        sh1 = VGroup(wire((0.75, 0.5), (1.7, 0.5), color=C_IF), coil_sym([0.75, 0.5], [0.75, -2.6], n=6, r=0.1, color=C_IF))
        sh2 = VGroup(wire((5.0, 0.5), (5.95, 0.5), color=C_IF), coil_sym([5.95, 0.5], [5.95, -2.6], n=6, r=0.1, color=C_IF))
        sw1 = _sw(2.9, 0.5, 1.9, "S_1")
        sw2 = _sw(3.7, 0.5, 1.9, "S_2")
        bus_t = wire((2.9, 2.0), (6.6, 2.0))
        j1, j2 = wire((2.9, 1.9), (2.9, 2.0)), wire((3.7, 1.9), (3.7, 2.0))
        bus_b = wire((0.75, -2.6), (6.6, -2.6))
        load = Rectangle(width=0.6, height=1.2, stroke_color=GRAYTXT, stroke_width=3, fill_color=GRAYTXT, fill_opacity=0.15).move_to([6.6, -0.3, 0])
        w_l = VGroup(wire((6.6, 2.0), (6.6, 0.3)), wire((6.6, -0.9), (6.6, -2.6)), load)
        pl = VGroup(Text("+", font_size=26, color=WHITE).move_to([4.6, 2.3, 0]), Text("−", font_size=26, color=WHITE).move_to([3.7, -2.95, 0]))
        eq = wire((1.7, 0.0), (5.0, 0.0), color=YEL, width=5)
        eqd = VGroup(Dot([1.7, 0.0, 0], radius=0.08, color=YEL), Dot([5.0, 0.0, 0], radius=0.08, color=YEL))
        eql = T("equalizer", 18, YEL).move_to([3.35, -0.38, 0])
        leg = fit_width(T("ชันท์ฟิลด์ = เขียว    เซรี่ฟิลด์ = ม่วง    equalizer = เหลือง", 17, GRAYTXT), 6.6).move_to([3.7, -3.4, 0])
        base = VGroup(a1, a2, up1, up2, dn1, dn2, s1, s2, sh1, sh2, sw1, sw2, bus_t, j1, j2, bus_b, w_l, pl)
        self.play(Create(base), run_time=2.2)
        self.play(FadeIn(leg), run_time=0.5)
        self.wait(1.2)
        self.say("cumulative = ฟลักซ์เซรี่ ช่วย ฟลักซ์ชันท์  → เซรี่ฟิลด์ต่ออนุกรมสายบวกของแต่ละเครื่อง", color=YEL)
        self.play(Indicate(s1, color=C_IS, scale_factor=1.12), Indicate(s2, color=C_IS, scale_factor=1.12), run_time=1.2)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("วาดเครื่องผสม cumulative 2 เครื่อง", 21), T("ต่อขนานกัน ใช้สวิตช์ 2 ตัว (S1, S2)", 21)], OK),
            ("วาดทีละขั้น", [T("ก ชันท์ฟิลด์ คร่อมอาร์เมเจอร์แต่ละเครื่อง", 20, C_IF),
                           T("ข เซรี่ฟิลด์ อนุกรมสายบวก (cumulative)", 20, C_IS),
                           T("ค S1, S2 ที่สายบวกเข้าบัสร่วม", 20, WHITE),
                           T("ง equalizer ต่อจุดอาร์เมเจอร์–เซรี่ ของ 2 เครื่อง", 20, YEL)], OK),
        ])
        self.play(Create(eq), FadeIn(eqd), FadeIn(eql), run_time=1.4)
        self.play(flow(eq, YEL, run=1.4))
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("ทำไมต้องมี equalizer", [T("ถ้าไม่มี: เครื่องหนึ่งรับกระแสเพิ่ม", 20), T("→ เซรี่แรงขึ้น → E สูงขึ้น → รับเพิ่มอีก", 20),
                                  T("→ เครื่องนั้นแบกโหลดหมด  ไม่เสถียร", 20, WARN),
                                  T("มี equalizer: เซรี่ฟิลด์ขนานกัน", 20, YEL), T("แบ่งกระแสตามขนาดเครื่อง เสถียร", 20, YEL)], WARN),
            ("ลำดับปิดสวิตช์", [T("ปิด S1 แล้ว S2 (equalizer ต่ออยู่ก่อน)", 20)], OK),
        ], start=3)
        self.play(Transform(sw1.blade, sw1.closed), Transform(sw2.blade, sw2.closed), run_time=1.2)
        self.play(flow(bus_t, C_IA, run=1.2))
        self.wait(2.0)
        self.final([T("ชันท์คร่อมอาร์เมเจอร์ + เซรี่ในสายบวก ทั้ง 2 เครื่อง", 24, OK),
                    T("S1 และ S2 อยู่สายบวกของแต่ละเครื่อง เข้าบัสร่วม", 24, OK),
                    T("equalizer เชื่อมจุดอาร์เมเจอร์–เซรี่ ของ 2 เครื่อง", 24, YEL)],
                   "เครื่องผสมขนานกัน = ต้องมี equalizer ไม่งั้นไม่เสถียร",
                   "บทที่ 8 หน้า 17-19 (ผสมแบบ cumulative)  ·  ข้อนี้เป็นการวาดไดอะแกรม ไม่มีตัวเลข")


# =============================================================== M14 / M15  มิดเทอม 1/2564
class M14_Mid64_LongShunt(Solve):
    def construct(self):
        self.head("มิดเทอม 1/2564 ข้อ 14 · compound long-shunt 30 kW", "มิดเทอม 1/2564 · ข้อ 14")
        self.say("ผสม 30 kW 240 V long-shunt · Rsh 75 โอห์ม · Ra 0.03 โอห์ม · Rse 0.012 โอห์ม · จ่ายเต็มโหลด", color=OK)
        fig = cg_fig("long", r"R_{sh}=75\,\Omega", r"R_a=0.03\,\Omega", r"R_{se}=0.012\,\Omega", r"V_t=240\,V", r"30\,kW")
        self.play(Create(fig), run_time=2.0)
        self.wait(1.5)
        self.say("ใจความ: long-shunt = ชันท์คร่อมขั้ว  Ia = Ise = IL + Ish  และ E = Vt + Va + Vse", color=YEL)
        self.play(flow(fig.sh_top, C_IF, run=1.4), Indicate(fig.ser, color=C_IS, scale_factor=1.12))
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("หา (ก) IL (ข) Ish (ค) Ia (ง) Vse (จ) Va (ฉ) E", 21)], OK),
            ("(ก) กระแสโหลด (ข) กระแสชันท์", [M(r"I_L=\frac{30000}{240}=125\,A", color=C_IL),
                                         M(r"I_{sh}=\frac{V_t}{R_{sh}}=\frac{240}{75}=3.2\,A", color=C_IF)], OK),
            ("(ค) กระแสอาร์เมเจอร์", M(r"I_a=", r"I_L", r"+", r"I_{sh}", r"=125+3.2=128.2\,A"), C_IA),
        ])
        self.glow(r[2][1][1], fig.il, color=C_IL)
        self.glow(r[2][1][3], fig.if_, color=C_IF)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("(ง) แรงดันตกเซรี่", [M(r"V_{se}=I_aR_{se}=128.2(0.012)=1.54\,V", color=C_IS)], C_IS),
            ("(จ) แรงดันตกอาร์เมเจอร์", [M(r"V_a=I_aR_a=128.2(0.03)=3.85\,V", color=C_IA)], C_IA),
            ("(ฉ) แรงเคลื่อน E", [M(r"E=V_t+V_a+V_{se}"), M(r"E=240+3.85+1.54=245.38\,V", color=C_E)], C_E),
            ("ตรวจ", [M(r"E-V_t=5.38\,V=I_a(R_a+R_{se})=128.2(0.042)"), T("ตรงกัน  ✓", 22, OK)], GRAYTXT),
        ], start=4)
        self.wait(2.5)
        self.final([M(r"I_L=125\,A\quad I_{sh}=3.2\,A\quad I_a=128.2\,A", color=OK, size=32),
                    M(r"V_{se}=1.54\,V\quad V_a=3.85\,V\quad E=245.38\,V", color=OK, size=32)],
                   "long-shunt: Ish = Vt ÷ Rsh · Ia = IL + Ish · E = Vt + Ia(Ra + Rse)",
                   "บทที่ 5 (ชนิดเครื่องกำเนิด) · บทที่ 7 ตย.7-6 · ข้อสอบเก่าจริง 2564 ข้อ 14")


class M15_Mid64_ShortShunt(Solve):
    def construct(self):
        self.head("มิดเทอม 1/2564 ข้อ 15 · compound short-shunt", "มิดเทอม 1/2564 · ข้อ 15")
        self.say("short-shunt: Vt 240 V · IL 50 A · Rse 0.04 โอห์ม · กระแสชันท์ If = 2 A (โจทย์ให้มาตรง ๆ)", color=OK)
        fig = cg_fig("short", r"R_{sh}", r"R_a", r"R_{se}=0.04\,\Omega", r"V_t=240\,V", r"Load", il_t=r"I_L=50\,A",
                     if_t=r"I_{sh}=2\,A", is_t=r"I_{se}")
        self.play(Create(fig), run_time=2.0)
        self.wait(1.5)
        self.say("ใจความ: short-shunt = ชันท์คร่อมอาร์เมเจอร์  เซรี่อยู่ในสายโหลด  Ise = IL", color=YEL)
        self.play(flow(fig.sh_top, C_IF, run=1.4), Indicate(fig.ser, color=C_IS, scale_factor=1.12))
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("หา (ก) Ise (ข) Vse (ค) Vชันท์ (ง) Ia", 21)], OK),
            ("(ก) กระแสเซรี่", [M(r"I_{se}=I_L=50\,A", color=C_IS), T("เพราะเซรี่อนุกรมกับโหลด", 20, GRAYTXT)], C_IS),
            ("(ข) แรงดันตกเซรี่", [M(r"V_{se}=I_{se}R_{se}=50(0.04)=2\,V", color=C_IS)], C_IS),
        ])
        self.glow(r[2][1][0], fig.rs_l, color=C_IS)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("(ค) แรงดันคร่อมชันท์", [M(r"V_{sh}=V_t+V_{se}=240+2=242\,V", color=C_IF),
                                 T("ชันท์คร่อมอาร์เมเจอร์ สูงกว่า Vt เท่ากับแรงดันตกเซรี่", 19, GRAYTXT)], C_IF),
            ("(ง) กระแสอาร์เมเจอร์", [M(r"I_a=", r"I_{se}", r"+", r"I_{sh}", r"=50+2=52\,A")], C_IA),
            ("ตรวจ", [M(r"R_{sh}=\frac{242}{2}=121\,\Omega"), T("ค่าสมเหตุสมผล (ชันท์ R สูง)  ✓", 21, OK)], GRAYTXT),
        ], start=4)
        self.glow(r[1][1][0][1], fig.is_, color=C_IS)
        self.wait(2.5)
        self.final([M(r"I_{se}=50\,A\quad V_{se}=2\,V\quad V_{sh}=242\,V\quad I_a=52\,A", color=OK, size=32)],
                   "short-shunt: Ise = IL · Vชันท์ = Vt + Vse · Ia = Ise + Ish",
                   "บทที่ 5 (ชนิดเครื่องกำเนิด) · บทที่ 7 ตย.7-7 · ข้อสอบเก่าจริง 2564 ข้อ 15")


# =============================================================== PR01-PR05  ข้อฝึกบทที่ 11 (Claude เขียนเอง)
def _prtag():
    return Text("ข้อฝึก Claude เขียนเอง · ไม่ใช่ข้อสอบจริง", font_size=16, color=WARN).move_to([0, -3.55, 0])


class PR01_Practice_BaseValues(Solve):
    def construct(self):
        self.head("ข้อฝึก 1 · ค่าฐาน 3 เฟส และ p.u.", "ข้อฝึกบทที่ 11 · ใช้สูตรหน้า 40-46")
        tg = _prtag()
        self.add(tg)
        self.say("ฐาน 100 MVA (3 เฟส) 138 kV (สาย) · สายส่ง X = 47.61 โอห์ม · บัส 131.1 kV · โหลด 60 MVA", color=OK)
        lg = T("เต็มแถบ = ฐาน = 1.0 p.u.   หมุดสี = ค่าจริง ÷ ฐาน", 19, GRAYTXT).move_to([3.6, 2.2, 0])
        bars = []
        specs = [(1.3, 131.1 / 138, r"V:\ \frac{131.1}{138}=0.95", C_E), (0.0, 0.6, r"S:\ \frac{60}{100}=0.6", C_IA),
                 (-1.3, 0.25, r"X:\ \frac{47.61}{190.44}=0.25", C_IL)]
        self.play(FadeIn(lg), run_time=0.5)
        for y, fr, tex, col in specs:
            b = pu_bar(y, fr, "", "", col, w=4.6, x0=1.2)
            lab = M(tex, color=col, size=24).move_to([3.5, y + 0.55, 0])
            bars.append((b, lab))
            self.play(FadeIn(b[0:3]), FadeIn(lab), Create(b[3]), FadeIn(b[4]), run_time=1.0)
        self.wait(1.0)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("ฐาน 100 MVA , 138 kV · X = 47.61 โอห์ม", 21), T("บัส 131.1 kV · โหลด 60 MVA", 21),
                           T("หา Zb , Ib , p.u. ของ V , S , X และกระแสโหลดจริง", 21)], OK),
            ("ค่าฐาน (3 เฟส)", [M(r"Z_b=\frac{V_{LL}^2}{VA_{3\phi}}=\frac{138^2}{100}=190.44\,\Omega", color=C_E),
                             M(r"I_b=\frac{VA_{3\phi}}{\sqrt{3}\,V_{LL}}=\frac{100\times10^6}{\sqrt{3}(138\times10^3)}=418.4\,A", color=C_IA)], OK),
        ])
        self.glow(r[1][1][0], bars[2][0][4], color=C_IL)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("p.u. = ค่าจริง ÷ ค่าฐาน", [M(r"V_{pu}=131.1/138=0.95", color=C_E), M(r"S_{pu}=60/100=0.6", color=C_IA),
                                      M(r"X_{pu}=47.61/190.44=0.25", color=C_IL)], OK),
            ("กระแสโหลด", [M(r"I_{pu}=\frac{S_{pu}}{V_{pu}}=\frac{0.6}{0.95}=0.6316"),
                         M(r"I=0.6316\times418.4=264.2\,A", color=C_IA)], C_IA),
            ("ตรวจด้วยสูตรตรง", [M(r"I=\frac{60\times10^6}{\sqrt{3}(131.1\times10^3)}=264.2\,A"), T("ตรงกัน  ✓", 22, OK)], GRAYTXT),
        ], start=3)
        self.wait(2.5)
        self.final([M(r"Z_b=190.44\,\Omega\quad I_b=418.4\,A", color=OK, size=34),
                    M(r"V=0.95\quad S=0.6\quad X=0.25\ \text{p.u.}\quad I=264.2\,A", color=OK, size=32)],
                   "เลือกฐานแค่ 2 ตัว (MVA กับ kV สาย) แล้ว Zb = kV² ÷ MVA · Ib = MVA ÷ (sqrt3·kV)",
                   "บทที่ 11 หน้า 40-46 (คลิป EPS11_P44_BaseQuantities)  ·  ข้อฝึก ไม่ใช่ข้อสอบจริง")


class PR02_Practice_ChangeBase(Solve):
    def construct(self):
        self.head("ข้อฝึก 2 · เปลี่ยนฐาน p.u.", "ข้อฝึกบทที่ 11 · ใช้สูตรหน้า 48-49")
        tg = _prtag()
        self.add(tg)
        self.say("เครื่องกำเนิดกับหม้อแปลง บอก p.u. ที่ฐานของตัวเอง → ต้องแปลงเป็นฐานระบบ 100 MVA 13.8 kV", color=OK)
        cA = card([("เครื่องกำเนิด G", C_E), "50 MVA , 13.8 kV", "X = 0.18 p.u."], w=2.8, color=C_E, size=18).move_to([1.7, 1.3, 0])
        cB = card([("หม้อแปลง T", WHITE), "80 MVA , 13.2 kV", "X = 0.12 p.u."], w=2.8, color=WHITE, size=18).move_to([1.7, -0.9, 0])
        nA = card([("ฐานระบบ", YEL), "100 MVA , 13.8 kV", "X = ?"], w=2.8, color=YEL, size=18).move_to([5.4, 1.3, 0])
        nB = card([("ฐานระบบ", YEL), "100 MVA , 13.8 kV", "X = ?"], w=2.8, color=YEL, size=18).move_to([5.4, -0.9, 0])
        aA = Arrow(cA.get_right(), nA.get_left(), buff=0.06, color=GRAYTXT, stroke_width=4, tip_length=0.18)
        aB = Arrow(cB.get_right(), nB.get_left(), buff=0.06, color=GRAYTXT, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(cA), FadeIn(cB), run_time=0.8)
        self.play(Create(aA), Create(aB), FadeIn(nA), FadeIn(nB), run_time=1.0)
        f = MathTex(r"X_{new}", r"=", r"X_{given}", r"\left(\frac{kV_{given}}{kV_{new}}\right)^{2}", r"\frac{MVA_{new}}{MVA_{given}}",
                    font_size=34, color=WHITE).move_to([3.6, -2.6, 0])
        f[3].set_color(C_S)
        f[4].set_color(YEL)
        self.say("kV กลับด้านแล้วยกกำลังสอง · MVA ใหม่ ÷ MVA เดิม", color=YEL)
        self.play(Write(f), run_time=1.4)
        self.wait(1.0)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("เปลี่ยน X ของ G และ T มาที่ 100 MVA , 13.8 kV", 21)], OK),
            ("เครื่องกำเนิด G", [M(r"X_G=0.18\left(\frac{13.8}{13.8}\right)^2\frac{100}{50}", color=C_E),
                              M(r"X_G=0.18(1)(2)=0.36", color=C_E)], C_E),
        ])
        self.glow(f[4], nA, color=YEL)
        nA2 = card([("ฐานระบบ", YEL), "100 MVA , 13.8 kV", "X = 0.36"], w=2.8, color=C_E, size=18).move_to(nA)
        self.play(Transform(nA, nA2), run_time=0.8)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("หม้อแปลง T", [M(r"X_T=0.12\left(\frac{13.2}{13.8}\right)^2\frac{100}{80}"),
                         M(r"X_T=0.12(0.9149)(1.25)=0.1372", color=OK)], OK),
            ("ตรวจทิศทาง", [T("MVA ฐานใหญ่ขึ้น (80→100)  X ต้องมากขึ้น", 20), T("kV ฐานใหญ่กว่าพิกัด  X ต้องน้อยลง", 20),
                          M(r"0.12\to0.1372\ (\text{net up})"), T("สอดคล้อง  ✓", 22, OK)], GRAYTXT),
        ], start=3)
        self.glow(f[3], nB, color=C_S)
        nB2 = card([("ฐานระบบ", YEL), "100 MVA , 13.8 kV", "X = 0.1372"], w=2.8, color=OK, size=18).move_to(nB)
        self.play(Transform(nB, nB2), run_time=0.8)
        self.wait(2.5)
        self.final([M(r"X_G=0.36\ \text{p.u.}", color=OK, size=36), M(r"X_T=0.1372\ \text{p.u.}", color=OK, size=36)],
                   "Znew = Zgiven · (kV เดิม ÷ kV ใหม่)² · (MVA ใหม่ ÷ MVA เดิม)",
                   "บทที่ 11 หน้า 48-49 (คลิป EPS11_P49_ChangeOfBase)  ·  ข้อฝึก ไม่ใช่ข้อสอบจริง")


def _xf(cx, cy, color=WHITE):
    a = Circle(radius=0.28, stroke_color=color, stroke_width=3).move_to([cx - 0.17, cy, 0])
    b = Circle(radius=0.28, stroke_color=color, stroke_width=3).move_to([cx + 0.17, cy, 0])
    return VGroup(a, b)


def _mc(cx, cy, letter, color):
    c = Circle(radius=0.33, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    return VGroup(c, Text(letter, font_size=22, color=color).move_to(c))


class PR03_Practice_BaseZones(Solve):
    def construct(self):
        self.head("ข้อฝึก 3 · แรงดันฐานแต่ละโซน + Zb + Ib", "ข้อฝึกบทที่ 11 · ใช้วิธีหน้า 61-69")
        tg = _prtag()
        self.add(tg)
        self.say("G 50 MVA 11 kV → T1 11/110 kV → สายส่ง j60.5 โอห์ม → T2 110/33 kV → โหลด · ฐาน = 50 MVA , 11 kV (ที่ G)", color=OK)
        Y = 0.9
        g, t1, t2 = _mc(0.8, Y, "G", YEL), _xf(2.1, Y), _xf(4.4, Y)
        w1, w2, w3 = wire((1.13, Y), (1.65, Y)), wire((2.55, Y), (3.0, Y)), wire((3.0, Y), (3.95, Y))
        ln = res_zig([2.55, Y], [3.95, Y], n=3, color=C_IL)
        w4 = wire((4.85, Y), (5.6, Y))
        ld = Rectangle(width=0.7, height=0.7, stroke_color=GRAYTXT, stroke_width=3, fill_color=GRAYTXT, fill_opacity=0.15).move_to([5.95, Y, 0])
        self.play(Create(VGroup(w1, w4)), FadeIn(g), Create(t1), Create(t2), Create(ln), FadeIn(ld), run_time=1.6)
        zl = VGroup(Line([0.4, -0.3, 0], [1.75, -0.3, 0], color=YEL, stroke_width=5), Line([2.5, -0.3, 0], [4.05, -0.3, 0], color=OK, stroke_width=5),
                    Line([4.75, -0.3, 0], [6.4, -0.3, 0], color=C_S, stroke_width=5))
        zt = VGroup(M(r"11\,kV", color=YEL, size=24).move_to([1.1, -0.75, 0]), M(r"110\,kV", color=OK, size=24).move_to([3.3, -0.75, 0]),
                    M(r"33\,kV", color=C_S, size=24).move_to([5.6, -0.75, 0]))
        self.play(Create(zl), FadeIn(zt), run_time=1.0)
        self.wait(1.0)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("ฐาน 50 MVA , 11 kV ที่ G  (MVA ฐานเท่าเดิมทุกโซน)", 20), T("หา kV ฐานทุกโซน , Zb , Ib และ X สายส่ง (p.u.)", 20)], OK),
            ("kV ฐาน: ข้ามหม้อแปลง", [M(r"110=11\times\frac{110}{11}", color=OK), M(r"33=110\times\frac{33}{110}", color=C_S)], OK),
        ])
        self.play(Indicate(t1, color=OK), Indicate(t2, color=C_S), run_time=1.2)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("Zb = kV² ÷ MVA", [M(r"Z_{b1}=\frac{11^2}{50}=2.42\,\Omega", color=YEL), M(r"Z_{b2}=\frac{110^2}{50}=242\,\Omega", color=OK),
                             M(r"Z_{b3}=\frac{33^2}{50}=21.78\,\Omega", color=C_S)], OK),
            ("Ib = MVA ÷ (sqrt3 · kV)", [M(r"I_{b1}=\frac{50\times10^6}{\sqrt{3}(11\times10^3)}=2624.3\,A", color=YEL),
                                   M(r"I_{b2}=262.4\,A\qquad I_{b3}=874.8\,A", color=OK)], OK),
        ], start=3)
        self.glow(r[0][1][1], ln, color=C_IL)
        self.wait(1.0)
        self.clear(bd)
        bd, r = self.rows([
            ("X สายส่ง (โซน 110 kV)", [M(r"X_{line}=\frac{60.5}{242}=0.25\ \text{p.u.}", color=C_IL)], C_IL),
            ("ตรวจ", [T("สายส่งอยู่โซน 110 kV  ใช้ Zb2 = 242 โอห์ม ไม่ใช่ 2.42", 20), T("Ib คูณ kV คงที่: 2624.3×11 = 262.4×110  ✓", 20, OK)], GRAYTXT),
        ], start=5)
        self.wait(2.5)
        self.final([M(r"11\to110\to33\,kV\quad Z_b=2.42\,/\,242\,/\,21.78\,\Omega", color=OK, size=30),
                    M(r"I_b=2624.3\,/\,262.4\,/\,874.8\,A\quad X_{line}=0.25", color=OK, size=30)],
                   "ข้ามหม้อแปลง คูณอัตราส่วนแรงดันสาย · MVA ฐานเท่าเดิม · Zb = kV² ÷ MVA ของโซนนั้น",
                   "บทที่ 11 หน้า 61-69 (คลิป EPS11_P61_Ex_BaseZones)  ·  ข้อฝึก ไม่ใช่ข้อสอบจริง")


def _rb(cx, cy, name, val, color=WHITE, w=0.84, h=0.7):
    rr = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08).move_to([cx, cy, 0])
    n = Text(name, font_size=17, color=GRAYTXT).move_to([cx, cy + 0.16, 0])
    v = Text(val, font_size=16, color=color).move_to([cx, cy - 0.15, 0])
    return VGroup(rr, n, v)


def _sr(cx, cy, label, color):
    c = Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    return VGroup(c, Text(label, font_size=14, color=color).move_to(c))


class PR04_Practice_ReactanceDiagram(Solve):
    def construct(self):
        self.head("ข้อฝึก 4 · วาด reactance diagram + p.u.", "ข้อฝึกบทที่ 11 · วิธีหน้า 61-73")
        tg = _prtag()
        self.add(tg)
        self.say("G 30 MVA 13.8 kV X=0.20 · T1 30 MVA 13.8/138 kV X=0.10 · สาย j80 โอห์ม · T2 25 MVA 138/6.6 kV X=0.08 · M 20 MVA 6.6 kV X=0.25", color=OK, size=20)
        RY, NY = 1.0, -0.7
        xs = [1.55, 2.6, 3.65, 4.7, 5.75]
        eg, em = _sr(0.6, RY, "Eg", YEL), _sr(6.7, RY, "Em", C_S)
        names = [("G", YEL), ("T1", WHITE), ("Line", C_IL), ("T2", WHITE), ("M", C_S)]
        bx = [_rb(x, RY, n, "?", c) for x, (n, c) in zip(xs, names)]
        W = [wire((0.88, RY), (xs[0] - 0.42, RY))]
        for i in range(4):
            W.append(wire((xs[i] + 0.42, RY), (xs[i + 1] - 0.42, RY)))
        W.append(wire((xs[4] + 0.42, RY), (6.42, RY)))
        W += [wire((0.6, RY - 0.28), (0.6, NY), (6.7, NY), (6.7, RY - 0.28))]
        tn = Text("neutral", font_size=15, color=GRAYTXT).move_to([3.65, NY - 0.3, 0])
        self.play(Create(VGroup(*W)), FadeIn(eg), FadeIn(em), *[FadeIn(b) for b in bx], FadeIn(tn), run_time=1.6)
        zone = VGroup(Line([0.4, -1.7, 0], [1.9, -1.7, 0], color=YEL, stroke_width=5), Line([2.1, -1.7, 0], [4.9, -1.7, 0], color=OK, stroke_width=5),
                      Line([5.1, -1.7, 0], [7.0, -1.7, 0], color=C_S, stroke_width=5))
        zt = VGroup(M(r"13.8\,kV", color=YEL, size=22).move_to([1.15, -2.05, 0]), M(r"138\,kV", color=OK, size=22).move_to([3.5, -2.05, 0]),
                    M(r"6.6\,kV", color=C_S, size=22).move_to([6.05, -2.05, 0]))
        base = T("ฐาน 30 MVA · โซน 13.8 / 138 / 6.6 kV", 20, YEL).move_to([3.7, -2.7, 0])
        self.play(Create(zone), FadeIn(zt), FadeIn(base), run_time=1.0)

        def put(i, v, col):
            nv = Text(v, font_size=16, color=col).move_to(bx[i][2])
            self.play(ReplacementTransform(bx[i][2], nv), Indicate(bx[i][0], color=col), run_time=0.7)
            bx[i].remove(bx[i][2])
            bx[i].add(nv)

        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("ฐาน = พิกัด G (30 MVA , 13.8 kV)", 20), T("ข้ามหม้อแปลงได้ 138 kV แล้ว 6.6 kV", 20)], OK),
            ("G และ T1 (ฐานตรงแล้ว)", [M(r"X_G=0.20\qquad X_{T1}=0.10\left(\frac{13.8}{13.8}\right)^2\frac{30}{30}=0.10")], OK),
        ])
        put(0, "j0.20", YEL)
        put(1, "j0.10", WHITE)
        self.wait(0.8)
        self.clear(bd)
        bd, r = self.rows([
            ("สายส่ง (โซน 138 kV)", [M(r"Z_b=\frac{138^2}{30}=634.8\,\Omega", color=C_IL), M(r"X_{line}=\frac{80}{634.8}=0.1260", color=C_IL)], C_IL),
            ("T2 (ฐาน kV ตรง, MVA ต่าง)", [M(r"X_{T2}=0.08\left(\frac{138}{138}\right)^2\frac{30}{25}=0.096", color=WHITE)], WHITE),
            ("มอเตอร์ M", [M(r"X_M=0.25\left(\frac{6.6}{6.6}\right)^2\frac{30}{20}=0.375", color=C_S)], C_S),
        ], start=3)
        put(2, "j0.126", C_IL)
        put(3, "j0.096", WHITE)
        put(4, "j0.375", C_S)
        self.say("ได้ reactance diagram ครบ: มีแต่ jX  ไม่มี R ชันท์ ความจุ", color=OK)
        self.play(*[Indicate(b[0], color=WHITE) for b in bx], run_time=1.2)
        self.wait(2.0)
        self.final([M(r"X_G=0.20\ X_{T1}=0.10\ X_{line}=0.1260", color=OK, size=32),
                    M(r"X_{T2}=0.096\quad X_M=0.375\quad (\text{all } j)", color=OK, size=32)],
                   "เลือกฐานจาก G → หา kV ทุกโซน → เปลี่ยนฐานทุกชิ้น (kV กลับด้านกำลังสอง · MVA ใหม่ ÷ เดิม)",
                   "บทที่ 11 หน้า 61-73 (คลิป EPS11_P61, P70)  ·  ข้อฝึก ไม่ใช่ข้อสอบจริง")


class PR05_Practice_TransformerBank(Solve):
    def construct(self):
        self.head("ข้อฝึก 5 · หม้อแปลง 1 เฟส 3 ตัว → 3 เฟส", "ข้อฝึกบทที่ 11 · ใช้วิธีหน้า 50-55, 67")
        tg = _prtag()
        self.add(tg)
        self.say("หม้อแปลง 1 เฟส 3 ตัว ต่อ Y-Y · ตัวละ 10 MVA 76.2/12.7 kV X = 8 % · ฐานระบบ 100 MVA , 22 kV (ด้านต่ำ)", color=OK)
        xf = VGroup(*[_xf(x, 1.2) for x in (1.4, 2.8, 4.2)])
        lab1 = fit_width(T("1 เฟส ตัวละ  10 MVA  76.2/12.7 kV", 18, GRAYTXT), 4.2).move_to([2.8, 0.45, 0])
        br = Brace(xf, DOWN, buff=1.0, color=YEL)
        brt = T("ธนาคาร 3 เฟส", 20, YEL).next_to(br, DOWN, buff=0.1)
        self.play(Create(xf), FadeIn(lab1), run_time=1.2)
        self.play(GrowFromCenter(br), FadeIn(brt), run_time=0.9)
        rule = VGroup(T("กำลัง ×3", 22, C_IA), T("แรงดันสาย × sqrt3 (ต่อ Y)", 22, C_IL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -2.3, 0])
        self.play(FadeIn(rule), run_time=0.7)
        self.wait(1.0)
        bd, r = self.rows([
            ("เข้าใจโจทย์", [T("หาพิกัด 3 เฟส · X ที่ฐาน 100 MVA 22 kV", 20), T("และ Z จริงฝั่งแรงสูง/ต่ำ  ตรวจอัตรา", 20)], OK),
            ("พิกัดรวม 3 เฟส", [M(r"S=3\times10=30\,MVA", color=C_IA),
                             M(r"V_{HV}=\sqrt{3}(76.2)=132\,kV", color=C_IL), M(r"V_{LV}=\sqrt{3}(12.7)=22\,kV", color=C_IL)], OK),
        ])
        self.glow(r[1][1][0], rule[0], color=C_IA)
        self.glow(r[1][1][1], rule[1], color=C_IL)
        self.wait(0.8)
        self.clear(bd)
        bd, r = self.rows([
            ("X ที่ฐานระบบ", [M(r"X_{new}=0.08\left(\frac{22}{22}\right)^2\frac{100}{30}"), M(r"X_{new}=0.2667\ \text{p.u.}", color=OK)], OK),
            ("Z จริง จาก p.u. ของตัวเอง", [M(r"Z_{HV}=0.08\frac{132^2}{30}=46.46\,\Omega", color=C_IL),
                                      M(r"Z_{LV}=0.08\frac{22^2}{30}=1.2907\,\Omega", color=C_S)], OK),
            ("ตรวจ", [M(r"\frac{Z_{HV}}{Z_{LV}}=\frac{46.46}{1.2907}=36=\left(\frac{132}{22}\right)^2"), T("ตรงกัน  ✓", 22, OK)], GRAYTXT),
        ], start=3)
        self.wait(2.5)
        self.final([M(r"S=30\,MVA\quad 132/22\,kV\quad X_{new}=0.2667", color=OK, size=32),
                    M(r"Z_{HV}=46.46\,\Omega\quad Z_{LV}=1.2907\,\Omega", color=OK, size=32)],
                   "1 เฟส 3 ตัว: MVA ×3 · kV สาย ×sqrt3 · Z ข้ามฝั่งคูณ (kV สูง ÷ kV ต่ำ)²",
                   "บทที่ 11 หน้า 50-55, 67-68 (คลิป EPS11_P49)  ·  ข้อฝึก ไม่ใช่ข้อสอบจริง")
