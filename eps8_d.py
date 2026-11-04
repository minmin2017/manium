"""EPS8 หน้า 15-17 (เฉลย ตย.8-3, 8-11 cumulative, รูป 8-8 short/long-shunt, สมการ 8-5) — ดู eps8_lib.py"""
from eps8_lib import *
from eps8_a import chips


def _lv(txt, color=C_E, size=24):
    return MathTex(txt, font_size=size, color=color)


# =============================================================== P15  หน้า 15
class P15_Ex83Compound(Lesson):
    """เฉลย ตย.8-3 (VR = 8.7 %), ใช้ VR เทียบเครื่อง, 8-11 เริ่ม: ขนานใช้ได้เฉพาะโหลดใกล้ -> ต้องการแรงดันคงที่"""

    def construct(self):
        self.head("เฉลย ตย.8-3 · 8-11 แบบผสม cumulative เริ่ม", "หน้า 15 · ตย.8-3, 8-11")
        self.say("เฉลยตัวอย่าง 8-3: เครื่องกำเนิดขนาน เต็มพิกัด 230 V ปลดโหลดได้ 250 V", color=OK)
        bd = Board(self, x=-6.6, y=2.0, gap=0.12)
        bd.add(1, "โจทย์ให้", VGroup(n_text("เต็มพิกัด  V_FL = 230 V", size=20), n_text("ปลดโหลด  V_NL = 250 V", size=20)
                                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), color=OK, hold=0.1)
        bar_l = Rectangle(width=0.7, height=3.5, stroke_width=0, fill_color=C_E, fill_opacity=0.7).move_to([3.2, -0.45, 0])
        bar_r = Rectangle(width=0.7, height=3.22, stroke_width=0, fill_color=C_E, fill_opacity=0.45).move_to([5.4, -0.59, 0])
        bar_r.align_to(bar_l, DOWN)
        l_nl = _lv(r"V_{NL}=250\,\mathrm{V}", C_E, 22).next_to(bar_l, DOWN, buff=0.12)
        l_fl = _lv(r"V_{FL}=230\,\mathrm{V}", C_E, 22).next_to(bar_r, DOWN, buff=0.12)
        self.play(FadeIn(bar_l), FadeIn(bar_r), FadeIn(l_nl), FadeIn(l_fl), run_time=0.9)
        bd.add(2, "สูตร (8-4)", MathTex(r"VR=\frac{V_{NL}-V_{FL}}{V_{FL}}\times100", font_size=30), color=OK, hold=0.1)
        bd.add(3, "แทนค่า", MathTex(r"VR=\frac{250-230}{230}\times100", font_size=30), color=OK, hold=0.1)
        res = VGroup(MathTex(r"VR=8.7\,\%", font_size=34, color=OK),
                     n_text("(20/230 = 0.087) เป็นบวก ✓", size=18, color=GRAYTXT)).arrange(RIGHT, buff=0.3)
        bd.add(4, "ได้ / ตรวจ", res, color=OK, hold=0.1)
        dl = DashedLine([3.55, bar_l.get_top()[1], 0], [5.75, bar_l.get_top()[1], 0], color=GRAYTXT, stroke_width=2)
        gap = DoubleArrow([5.4, bar_l.get_top()[1], 0], [5.4, bar_r.get_top()[1], 0], buff=0, color=WARN, stroke_width=3,
                          tip_length=0.1)
        t_gap = _lv(r"20\,\mathrm{V}", WARN, 24).next_to(gap, RIGHT, buff=0.15)
        self.play(Create(dl), Create(gap), FadeIn(t_gap), Indicate(res[0], color=WHITE), run_time=1.0)
        self.wait(1.0)

        # ---- ใช้ VR เปรียบเทียบ
        self.say("VR ใช้เปรียบเทียบเครื่องกำเนิด: VR น้อย = แรงดันขั้วเปลี่ยนน้อย = น่าใช้กว่า", color=C_IL)
        self.play(FadeOut(VGroup(bar_l, bar_r, l_nl, l_fl, dl, gap, t_gap)), *[FadeOut(r) for r in bd.rows], run_time=0.6)
        g = make_axes(pos=[-5.0, -2.4], x_len=6.2, y_len=3.9, xmax=1.3, ymax=1.15, xl=r"I_L", yl=r"V_t")
        ax = g.ax
        la = Line(ax.c2p(0, 1.0), ax.c2p(1.0, 0.97), color=C_IL, stroke_width=5)
        lb = Line(ax.c2p(0, 1.0), ax.c2p(1.0, 0.78), color=WARN, stroke_width=5)
        ta = Text("เครื่อง A: VR น้อย", font_size=20, color=C_IL).next_to(la.get_end(), RIGHT, buff=0.12).shift(UP * 0.15)
        tb = Text("เครื่อง B: VR มาก", font_size=20, color=WARN).next_to(lb.get_end(), RIGHT, buff=0.12).shift(DOWN * 0.1)
        rated = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 1.0), color=GRAYTXT, stroke_width=2, dash_length=0.1)
        t_rat = Text("เต็มพิกัด", font_size=18, color=GRAYTXT).next_to(ax.c2p(1.0, 0), DOWN, buff=0.45)
        self.play(Create(g), run_time=0.8)
        self.play(Create(rated), FadeIn(t_rat), Create(la), Create(lb), FadeIn(ta), FadeIn(tb), run_time=1.6)
        pick = Text("เลือกเครื่อง A (VR น้อยที่สุด) มาใช้งาน", font_size=22, color=OK).move_to([3.4, -0.9, 0])  # ต่ำกว่าป้ายเครื่อง A/B (เดิมอยู่บรรทัดเดียวกันจนชน)
        self.play(FadeIn(pick), Circumscribe(ta, color=OK), run_time=1.2)
        self.wait(1.0)

        # ---- 8-11 เริ่ม
        self.say("8-11: เครื่องแบบขนานเหมาะกับโหลดที่อยู่ใกล้ — โหลดไกลต้องเจอแรงดันตกในสายด้วย", color=WARN)
        self.play(FadeOut(VGroup(g, la, lb, ta, tb, rated, t_rat, pick)), run_time=0.6)
        gen = arm_sym([-5.6, 0.0], r=0.5, letter="G")
        rt, rb = 0.9, -0.9
        w1 = wire((-5.6, 0.5), (-5.6, rt), (-3.6, rt))
        w2 = wire((-5.6, -0.5), (-5.6, rb), (4.4, rb))
        rl1 = res_zig([-3.6, rt], [0.2, rt], n=7, color=C_R)
        w1b = wire((0.2, rt), (4.4, rt))
        lamp = VGroup(Circle(radius=0.32, stroke_color=YEL, stroke_width=3, fill_color=YEL, fill_opacity=0.15),
                      Line([-0.22, -0.22, 0], [0.22, 0.22, 0], color=YEL, stroke_width=2),
                      Line([-0.22, 0.22, 0], [0.22, -0.22, 0], color=YEL, stroke_width=2)).move_to([4.4, 0.0, 0])
        lw = VGroup(wire((4.4, rt), (4.4, 0.32)), wire((4.4, -0.32), (4.4, rb)))
        t_line = Text("สายส่งยาว (มีความต้านทาน)", font_size=19, color=C_R).move_to([-1.7, rt + 0.45, 0])
        t_ld = Text("โหลดอยู่ไกล", font_size=19, color=YEL).move_to([4.4, -1.35, 0])
        self.play(Create(VGroup(gen, w1, w2, rl1, w1b, lw, lamp)), FadeIn(t_line), FadeIn(t_ld), run_time=1.4)
        # แท่งแรงดัน: ที่เครื่อง (ลดเล็กน้อย) / ที่โหลด (ลดมากกว่า)
        bx1 = Rectangle(width=0.5, height=1.6, stroke_color=GRAYTXT, stroke_width=2).move_to([-4.3, -2.35, 0])
        bx2 = Rectangle(width=0.5, height=1.6, stroke_color=GRAYTXT, stroke_width=2).move_to([-2.7, -2.35, 0])
        f1 = Rectangle(width=0.5, height=1.5, stroke_width=0, fill_color=C_E, fill_opacity=0.85).move_to(bx1.get_bottom() + UP * 0.75)
        f2 = Rectangle(width=0.5, height=1.5, stroke_width=0, fill_color=YEL, fill_opacity=0.85).move_to(bx2.get_bottom() + UP * 0.75)
        k1 = Text("Vt ที่เครื่อง", font_size=17, color=C_E).next_to(bx1, DOWN, buff=0.1)
        k2 = Text("V ที่โหลดไกล", font_size=17, color=YEL).next_to(bx2, DOWN, buff=0.1)
        self.play(Create(bx1), Create(bx2), FadeIn(f1), FadeIn(f2), FadeIn(k1), FadeIn(k2), run_time=0.9)
        self.play(f1.animate.stretch_to_fit_height(1.2, about_edge=DOWN), f2.animate.stretch_to_fit_height(0.7, about_edge=DOWN),
                  run_time=2.4)
        goal = card([("จึงต้องทำให้ Vt คงที่ หรือเพิ่มขึ้นตามโหลด", OK), "เครื่องกำเนิดแบบผสมชนิด cumulative ทำได้"], color=OK, w=5.2)
        goal.move_to([2.6, -2.35, 0])
        self.play(FadeIn(goal, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)
        self.exam("จุดออกสอบ 8-10/8-11: VR บอกอะไร และทำไมโหลดไกลถึงไม่เหมาะกับเครื่องแบบขนาน",
                  "VR = (V_NL − V_FL)/V_FL × 100 (ยิ่งน้อยยิ่งดี) · ขนาน: Vt ลดตามโหลด + แรงดันตกในสาย → ต้องใช้ผสม cumulative")


# =============================================================== P16  หน้า 16
class P16_ShortLong(Lesson):
    """รูป 8-8: short-shunt (ชันท์ฟิลด์ต่อคร่อมอาร์เมเจอร์) vs long-shunt (ชันท์ฟิลด์ต่อคร่อมขั้ว) — ย้ายจุดต่อข้ามเซรี่ฟิลด์"""

    def construct(self):
        self.head("รูป 8-8 การต่อแบบผสม: short-shunt / long-shunt", "หน้า 16 · รูปที่ 8-8")
        XA, XS = -2.6, -5.0
        YT, YB = 1.3, -2.0
        arm = arm_sym([XA, -0.3], r=0.45)
        t_a1 = Text("A1", font_size=17, color=GRAYTXT).move_to([XA + 0.45, 0.2, 0])
        t_a2 = Text("A2", font_size=17, color=GRAYTXT).move_to([XA + 0.45, -0.8, 0])
        t_arm = tag("อาร์เมเจอร์", size=17, color=C_E)
        t_arm.move_to([XA - 0.14 - t_arm.width / 2, -1.2, 0])   # ซ้ายสายล่างของอาร์เมเจอร์ (เดิมสายพาดกลางตัวอักษร)
        w_a = wire((XA, 0.15), (XA, YT), (-1.9, YT))
        ser = coil_sym([-1.9, YT], [0.1, YT], n=4, r=0.1, color=C_IS)
        w_s = wire((0.1, YT), (0.7, YT), (2.5, YT))
        t_ser = tag("เซรี่ฟิลด์ (S1–S2)", size=17, color=C_IS).move_to([-0.9, YT + 0.4, 0])
        w_b = wire((XA, -0.75), (XA, YB), (2.5, YB))
        term_p = Dot([2.5, YT, 0], radius=0.09, color=WHITE)
        term_n = Dot([2.5, YB, 0], radius=0.09, color=WHITE)
        t_p = Text("+", font_size=24, color=WHITE).next_to(term_p, RIGHT, buff=0.12)
        t_n = Text("−", font_size=24, color=WHITE).next_to(term_n, RIGHT, buff=0.12)
        rh = res_zig([XS, YT], [XS, 0.4], n=4)
        sh = coil_sym([XS, 0.4], [XS, -1.2], n=4, r=0.1, color=C_IF)
        sh_b = wire((XS, -1.2), (XS, YB), (XA, YB))
        t_rh = tag("รีโอสตาท", size=17, color=C_R).move_to([XS - 0.85, 0.85, 0])
        t_sh = tag("ชันท์ฟิลด์ (F1–F2)", size=17, color=C_IF).move_to([XS - 1.05, -0.4, 0])
        top_short = wire((XS, YT), (XA, YT), color=C_IF, width=4)
        top_long = wire((XS, YT), (XS, 2.0), (0.7, 2.0), (0.7, YT), color=C_IF, width=4)
        j1 = Dot([XA, YT, 0], radius=0.08, color=C_IF)
        j2 = Dot([0.7, YT, 0], radius=0.08, color=C_IF)
        ia = Arrow([XA + 0.75, -0.6, 0], [XA + 0.75, 0.5, 0], buff=0, color=C_IA, stroke_width=4, tip_length=0.16)
        t_ia = _lv(r"I_a", C_IA, 24).next_to(ia, RIGHT, buff=0.05)
        ifa = Arrow([XS + 0.35, 0.2, 0], [XS + 0.35, -0.6, 0], buff=0, color=C_IF, stroke_width=4, tip_length=0.16)
        t_if = _lv(r"I_f", C_IF, 24).next_to(ifa, RIGHT, buff=0.05)
        il = Arrow([1.1, YT - 0.4, 0], [1.9, YT - 0.4, 0], buff=0, color=C_IL, stroke_width=4, tip_length=0.16)
        t_il = _lv(r"I_L", C_IL, 24).next_to(il, DOWN, buff=0.05)
        base = VGroup(arm, t_a1, t_a2, t_arm, w_a, ser, w_s, t_ser, w_b, term_p, term_n, t_p, t_n, rh, sh, sh_b, t_rh, t_sh)
        for m in (base, top_short, top_long, j1, j2, ia, t_ia, ifa, t_if, il, t_il):
            m.shift(RIGHT * 0.5)      # ขยับวงจรไปขวา: ป้ายชันท์ฟิลด์ทางซ้ายเดิมชิดขอบเฟรมเมื่อใช้ฟอนต์ Loma

        self.say("สร้างเครื่องแบบผสม = เครื่องแบบขนาน + ขดลวดเซรี่ฟิลด์ (S1–S2) ต่ออนุกรมกับโหลด")
        self.play(Create(base), run_time=1.6)
        self.wait(0.4)

        self.say("(ก) short-shunt: ชันท์ฟิลด์ต่อคร่อมอาร์เมเจอร์โดยตรง — กระแสโหลดผ่านเซรี่", color=C_IF)
        self.play(Create(top_short), FadeIn(j1, scale=1.8), run_time=1.0)
        self.play(FadeIn(ia), FadeIn(t_ia), FadeIn(ifa), FadeIn(t_if), FadeIn(il), FadeIn(t_il), run_time=0.9)
        card_s = card([("short-shunt", C_IF), "Is = IL", "Ia = If + IL"], color=C_IF, w=3.0).move_to([5.25, 0.6, 0])
        self.play(FadeIn(card_s, shift=LEFT * 0.2), run_time=0.8)
        self.play(flow(top_short, C_IF, run=1.2), Indicate(ser, color=C_IS, scale_factor=1.15))
        self.wait(1.0)

        self.say("(ข) long-shunt: ย้ายจุดต่อชันท์ฟิลด์ไปที่ขั้วโหลด — เซรี่ฟิลด์อยู่ทางอาร์เมเจอร์", color=C_IF)
        t_ia2 = _lv(r"I_a=I_s", C_IA, 24).next_to(il, DOWN, buff=0.05)
        card_l = card([("long-shunt", C_IF), "Is = Ia", "Ia = If + IL"], color=C_IF, w=3.0).move_to([5.25, 0.6, 0])
        self.play(FadeOut(top_short), FadeOut(j1), FadeOut(card_s), run_time=0.5)
        self.play(Create(top_long), FadeIn(j2, scale=1.8), run_time=1.4)
        self.play(FadeIn(card_l, shift=LEFT * 0.2), Transform(t_il, t_ia2), run_time=0.9)
        self.play(flow(top_long, C_IF, run=1.4))
        self.wait(0.6)

        note = Text("หมายเหตุ: รูป 8-8(ข) ในเอกสารเขียน Ia = IL แต่ข้อความหน้า 17 ระบุ Ia = If + IL — ใช้ตามข้อความ",
                    font_size=16, color=GRAYTXT).move_to([0.3, -3.05, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.say("ลักษณะสมบัติของสองแบบแทบเหมือนกัน — ต่อแบบไหนก็ได้ ไม่ใช่ประเด็นสำคัญ", color=OK)
        self.wait(1.8)
        self.exam("จุดออกสอบ 8-11: short-shunt กับ long-shunt ต่างกันที่จุดไหน",
                  "short: ชันท์ฟิลด์ต่อคร่อมอาร์เมเจอร์ (Is = IL) · long: ชันท์ฟิลด์ต่อคร่อมขั้วเครื่อง (Is = Ia) · ลักษณะสมบัติเกือบเหมือนกัน")


# =============================================================== P17  หน้า 17
class P17_Eq85SeriesField(Lesson):
    """สมการ 8-5 Vt = E - IaRa - IsRs (ทั้งสองแบบ) + ขดลวดเซรี่ (ลวดโต รอบน้อย) เสริมฟลักซ์ชันท์เมื่อมีโหลด"""

    def construct(self):
        self.head("สมการ 8-5 และขดลวดเซรี่ฟิลด์", "หน้า 17 · 8-5, 8-11")
        # ---- วงจรสมมูล
        ex, ey = -4.6, 0.0
        src = meter([ex, ey], "E", color=C_E, r=0.4)
        ra = res_zig([ex, ey + 0.4], [ex, ey + 1.5], n=3, color=C_IA)
        top1 = wire((ex, ey + 1.5), (ex, ey + 1.9), (ex + 1.5, ey + 1.9))
        rs = res_zig([ex + 1.5, ey + 1.9], [ex + 3.0, ey + 1.9], n=4, color=C_IS)
        top2 = wire((ex + 3.0, ey + 1.9), (ex + 3.5, ey + 1.9))
        bot = wire((ex, ey - 0.4), (ex, ey - 1.5), (ex + 3.5, ey - 1.5))
        vt = Arrow([ex + 3.5, ey - 1.5, 0], [ex + 3.5, ey + 1.9, 0], buff=0, color=C_E, stroke_width=3, tip_length=0.2)
        t_vt = _lv(r"V_t", C_E, 30).next_to(vt, RIGHT, buff=0.1)
        t_ra = _lv(r"R_a", C_IA, 26).next_to(ra, LEFT, buff=0.12)
        t_rs = _lv(r"R_s", C_IS, 26).next_to(rs, UP, buff=0.12)
        self.say("เครื่องแบบผสม (short หรือ long ก็ได้): Vt = E − IaRa − IsRs")
        self.play(Create(VGroup(src, ra, top1, rs, top2, bot, vt)), FadeIn(t_vt), FadeIn(t_ra), FadeIn(t_rs), run_time=1.4)
        eq = MathTex(r"V_t", r"=", r"E", r"-", r"I_aR_a", r"-", r"I_sR_s", font_size=50).move_to([2.2, 1.5, 0])
        eq[0].set_color(C_E), eq[2].set_color(C_E), eq[4].set_color(C_IA), eq[6].set_color(C_IS)
        self.play(Write(eq), run_time=1.4)
        self.glow(eq[4], ra, color=C_IA)
        self.glow(eq[6], rs, color=C_IS)
        defs = VGroup(*[VGroup(_lv(a, c, 22), Text(b, font_size=17, color=GRAYTXT)).arrange(RIGHT, buff=0.2)
                        for a, b, c in ((r"I_a", "กระแสไหลในอาร์เมเจอร์", C_IA), (r"R_a", "ความต้านทานวงจรอาร์เมเจอร์", C_IA),
                                        (r"I_s", "กระแสไหลในเซรี่ฟิลด์", C_IS), (r"R_s", "ความต้านทานในเซรี่ฟิลด์", C_IS))]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.0, -0.5, 0])
        self.play(FadeIn(defs, shift=UP * 0.2), run_time=0.9)
        self.wait(0.6)
        # Is หมายถึงกระแสคนละตัวในแต่ละการต่อ (ข้อความหน้า 17 + รูป 8-8)
        isn = card([("Is ต่างกันตามการต่อ", C_IS), "short-shunt: Is = IL   |   long-shunt: Is = Ia"], color=C_IS, w=5.6)
        isn.move_to([3.0, -2.35, 0])
        self.play(FadeIn(isn, shift=UP * 0.2), run_time=0.8)
        self.wait(1.4)

        # ---- ขดลวดเซรี่ + ฟลักซ์เสริม
        self.say("ขดลวดเซรี่: ลวดเส้นโต รอบน้อย เพราะกระแสโหลดไหลผ่าน → สร้างฟลักซ์เสริมฟลักซ์ชันท์", color=C_IS)
        self.play(FadeOut(VGroup(src, ra, top1, rs, top2, bot, vt, t_vt, t_ra, t_rs, eq, defs, isn)), run_time=0.6)
        yoke = Rectangle(width=2.6, height=3.9, stroke_color=METAL, stroke_width=6, fill_color="#263238", fill_opacity=0.5).move_to([-3.4, 0.1, 0])
        core = Rectangle(width=0.9, height=3.0, stroke_color=METAL, stroke_width=2, fill_color="#607D8B", fill_opacity=0.9).move_to([-3.4, 0.1, 0])
        shc = VGroup(*[Line([-3.95, 1.45 - 0.12 * i, 0], [-2.85, 1.45 - 0.12 * i, 0], color=C_IF, stroke_width=2) for i in range(12)])
        src_ = VGroup(*[Line([-3.98, -0.1 - 0.3 * i, 0], [-2.82, -0.1 - 0.3 * i, 0], color=C_IS, stroke_width=7) for i in range(4)])
        t_shc = Text("ชันท์ฟิลด์: เส้นเล็ก รอบมาก", font_size=18, color=C_IF).move_to([-0.1, 1.2, 0])
        t_src = Text("เซรี่ฟิลด์: เส้นโต รอบน้อย", font_size=18, color=C_IS).move_to([-0.1, -0.55, 0])
        a1 = Arrow([-3.55, -1.2, 0], [-3.55, 1.5, 0], buff=0, color=C_PHI, stroke_width=8, tip_length=0.25)
        self.play(FadeIn(yoke), FadeIn(core), Create(shc), Create(src_), FadeIn(t_shc), FadeIn(t_src), run_time=1.4)
        t_ph1 = Text("ฟลักซ์ชันท์", font_size=18, color=C_PHI).move_to([-0.9, 0.35, 0])
        self.play(Create(a1), FadeIn(t_ph1), run_time=0.8)
        a2 = Arrow([-3.2, -1.2, 0], [-3.2, -0.5, 0], buff=0, color=C_IS, stroke_width=8, tip_length=0.2)
        a2b = Arrow([-3.2, -1.2, 0], [-3.2, 1.3, 0], buff=0, color=C_IS, stroke_width=8, tip_length=0.2)
        t_ph2 = Text("ฟลักซ์เซรี่ (เพิ่มตามโหลด)", font_size=18, color=C_IS).move_to([0.2, -1.5, 0])
        self.play(Create(a2), FadeIn(t_ph2), run_time=0.8)
        self.play(Transform(a2, a2b), run_time=1.6)
        self.say("ไม่มีโหลด Is = 0 → เหมือนเครื่องแบบขนาน | มีโหลด ฟลักซ์เซรี่เสริมเพิ่มขึ้น", color=OK)
        tot = card([("ฟลักซ์รวม = ฟลักซ์ชันท์ + ฟลักซ์เซรี่", OK), "(cumulative = เสริมกัน)"], color=OK, w=5.2).move_to([3.7, -2.65, 0])
        self.play(FadeIn(tot, shift=UP * 0.2), run_time=0.9)
        self.wait(2.0)
        self.exam("จุดออกสอบ 8-11: เขียนสมการแรงดันขั้วของเครื่องกำเนิดแบบผสม และบอกหน้าที่ขดลวดเซรี่",
                  "Vt = E − IaRa − IsRs · เซรี่ (ลวดโต รอบน้อย) ให้ฟลักซ์เสริมฟลักซ์ชันท์ เมื่อโหลดเพิ่ม")
