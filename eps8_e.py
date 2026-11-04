"""EPS8 หน้า 18-22 (รูป 8-9 เทียบแรงดันขั้ว, 8-12 differential, 8-13 over compound รูป 8-10, ตย.8-4 รูป 8-11, flat compound, ไดเวอร์เตอร์ รูป 8-12) — ดู eps8_lib.py
ข้อกำหนดจากบทเรียนเรนเดอร์คลาวด์ (ฟอนต์ Loma กว้างกว่า Leelawadee ~25-30%): เว้นขอบเฟรม >= 0.4, ป้ายอย่าวางทับสาย/แกน/เส้นประ, ข้อความยาวใช้ fit_width"""
from scipy.interpolate import PchipInterpolator
from eps8_lib import *
from eps8_a import chips
from eps8_c import _lv

# สีของชนิดเครื่อง (เส้นกราฟ Vt-IL ไม่ใช่ปริมาณฟิสิกส์ จึงไม่ใช้แดง E / น้ำเงินฟลักซ์ / เขียน If / ม่วง Is)
K_OVER = OK              # ผสมเกิน / cumulative
K_FLAT = YEL             # ผสมพอดี
K_UNDER = "#F48FB1"      # ผสมขาด
K_SHUNT = WHITE          # แบบขนาน
K_DIFF = WARN            # differential

# รูป 8-10 / 8-13(ก): Vt ที่ไม่มีโหลดเท่ากัน (แกน x = IL/Irated, y = Vt/V_NL)
FAM_A = {
    "over": [(0, 1.0), (0.3, 1.035), (0.6, 1.06), (1.0, 1.075), (1.25, 1.075)],
    "flat": [(0, 1.0), (0.3, 1.02), (0.6, 1.015), (1.0, 1.0), (1.25, 0.955)],
    "under": [(0, 1.0), (0.3, 0.985), (0.6, 0.95), (1.0, 0.905), (1.25, 0.845)],
    "shunt": [(0, 1.0), (0.3, 0.955), (0.6, 0.89), (1.0, 0.79), (1.25, 0.67)],
    "diff": [(0, 1.0), (0.2, 0.9), (0.4, 0.74), (0.55, 0.55), (0.62, 0.35), (0.58, 0.15), (0.48, 0.0)],
}


def cv(ax, pts, col, w=5):
    m = VMobject(stroke_color=col, stroke_width=w)
    m.set_points_smoothly([ax.c2p(x, y) for x, y in pts])
    return m


def legend_item(col, txt, size=19):
    ln = Line(ORIGIN, RIGHT * 0.55, color=col, stroke_width=5)
    t = Text(txt, font_size=size, color=col)
    return VGroup(ln, t).arrange(RIGHT, buff=0.18)


def flux_row(sub):
    """แถบฟลักซ์: ชันท์ ± เซรี่ = รวม  (sub=False เสริมกัน / True หักล้างกัน)"""
    def bar(w, col, txt):
        r = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.9)
        t = Text(txt, font_size=15, color=WHITE).move_to(r)
        return VGroup(r, t)
    sh, se = 1.0, 0.6
    tot = sh - se if sub else sh + se
    b1, b2, b3 = bar(sh, C_PHI, "ชันท์"), bar(se, C_IS, "เซรี่"), bar(tot, "#1565C0" if sub else "#42A5F5", "รวม")
    op = MathTex(r"-" if sub else r"+", font_size=34, color=WHITE)
    eq = MathTex(r"=", font_size=34, color=WHITE)
    return VGroup(b1, op, b2, eq, b3).arrange(RIGHT, buff=0.18)


def fig811():
    """รูป 8-11: เครื่องกำเนิด - สายส่งไกล 990 m - โหลด  (พิกัดฐาน กว้าง ~7.4, สูง ~5.2) คืน VGroup ที่มีชิ้นส่วนเป็นแอตทริบิวต์"""
    XG, XL, YT, YB = -5.9, -0.6, 1.5, -2.1
    gen = arm_sym([XG, -0.3], r=0.45, letter="E")
    a1 = Text("A1", font_size=16, color=GRAYTXT).move_to([XG + 0.52, 0.2, 0])
    a2 = Text("A2", font_size=16, color=GRAYTXT).move_to([XG + 0.52, -0.8, 0])
    pl = Text("+", font_size=24, color=WHITE).move_to([XG - 0.5, 0.25, 0])
    mi = Text("−", font_size=24, color=WHITE).move_to([XG - 0.5, -0.85, 0])
    top = VGroup(wire((XG, 0.15), (XG, YT), (-4.2, YT)), wire((-2.1, YT), (XL, YT), (XL, 0.25)))
    bot = VGroup(wire((XG, -0.75), (XG, YB), (-4.2, YB)), wire((-2.1, YB), (XL, YB), (XL, -0.85)))
    rz_t = res_zig([-4.2, YT], [-2.1, YT], n=5, color=C_R)
    rz_b = res_zig([-4.2, YB], [-2.1, YB], n=5, color=C_R)
    load = Rectangle(width=0.3, height=1.1, stroke_color=WHITE, stroke_width=3, fill_color="#455A64", fill_opacity=1).move_to([XL, -0.3, 0])
    t_load = Text("โหลด", font_size=20, color=YEL).next_to(load, RIGHT, buff=0.18)
    vt = Arrow([-4.65, YB, 0], [-4.65, YT, 0], buff=0, color=C_E, stroke_width=3, tip_length=0.2)
    vl = Arrow([-1.65, YB, 0], [-1.65, YT, 0], buff=0, color=OK, stroke_width=3, tip_length=0.2)
    t_vt = _lv(r"V_t", C_E, 30).next_to(vt, RIGHT, buff=0.1)
    t_vl = _lv(r"V_L", OK, 30).next_to(vl, LEFT, buff=0.1)
    il = Arrow([-3.9, 1.95, 0], [-2.5, 1.95, 0], buff=0, color=C_IL, stroke_width=4, tip_length=0.18)
    t_il = _lv(r"I_L", C_IL, 28).next_to(il, RIGHT, buff=0.12)
    t_rl = Text("R สาย", font_size=17, color=C_R).move_to([-3.15, YT - 0.45, 0])
    dim = DoubleArrow([XG, -2.55, 0], [XL, -2.55, 0], buff=0, color=GRAYTXT, stroke_width=3, tip_length=0.15)
    t_dim = Text("990 m", font_size=20, color=GRAYTXT).next_to(dim, DOWN, buff=0.1)
    g = VGroup(gen, a1, a2, pl, mi, top, bot, rz_t, rz_b, load, t_load, vt, vl, t_vt, t_vl, il, t_il, t_rl, dim, t_dim)
    g.gen, g.top, g.bot, g.rz_t, g.rz_b, g.load, g.vt, g.vl, g.t_vt, g.t_vl = gen, top, bot, rz_t, rz_b, load, vt, vl, t_vt, t_vl
    g.il, g.t_il, g.t_rl, g.dimarr, g.t_dim, g.t_load = il, t_il, t_rl, dim, t_dim, t_load
    g.path = wire((XG, 0.15), (XG, YT), (XL, YT), (XL, -0.8), (XL, YB), (XG, YB), (XG, -0.75))   # วงกระแสโหลด (ใช้ทำแสงวิ่ง)
    return g


def vt_plot(pos, x_len=5.4, y_len=4.1, ymax=1.2):
    """แกน Vt-IL แบบรูป 8-9/8-10/8-13(ก): เส้นประ Vt ไม่มีโหลด + เส้นประกระแสพิกัด + ป้ายซ้าย/ล่าง"""
    g = make_axes(pos=pos, x_len=x_len, y_len=y_len, xmax=1.3, ymax=ymax, xl=r"I_L", yl=r"V_t")
    ax = g.ax
    nl = DashedLine(ax.c2p(0, 1.0), ax.c2p(1.25, 1.0), color=GRAYTXT, stroke_width=2, dash_length=0.1)
    rated = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, ymax * 0.97), color=GRAYTXT, stroke_width=2, dash_length=0.1)
    t_nl = Text("แรงดันที่ขั้ว\nขณะไม่มีโหลด", font_size=16, color=GRAYTXT, line_spacing=0.9).next_to(ax.c2p(0, 1.0), LEFT, buff=0.12)
    t_rated = Text("กระแสพิกัด", font_size=18, color=GRAYTXT).next_to(ax.c2p(1.0, 0), DOWN, buff=0.45)
    g.xlab.set_color(C_IL)
    return g, ax, nl, rated, t_nl, t_rated


# =============================================================== P18  หน้า 18
class P18_CompareCurves(Lesson):
    """รูป 8-9: cumulative / ขนาน / differential (Vt ไม่มีโหลดเท่ากัน) + 8-12 differential = เซรี่กลับทิศ ฟลักซ์หักล้าง"""

    def construct(self):
        self.head("รูป 8-9 เทียบแรงดันขั้ว · 8-12 differential", "หน้า 18 · รูปที่ 8-9, 8-12")
        g, ax, nl, rated, t_nl, t_rated = vt_plot([-5.2, -2.7])
        c_sh = cv(ax, [(0, 1.0), (0.4, 0.935), (0.8, 0.85), (1.0, 0.79), (1.25, 0.68)], K_SHUNT)
        c_cu = cv(ax, [(0, 1.0), (0.4, 0.97), (0.8, 0.93), (1.0, 0.905), (1.25, 0.85)], K_OVER)
        c_df = cv(ax, FAM_A["diff"], K_DIFF)
        lg = VGroup(legend_item(K_OVER, "ผสมชนิด cumulative"), legend_item(K_SHUNT, "แบบขนาน"),
                    legend_item(K_DIFF, "ผสมชนิด differential")).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lg.move_to([2.05, -2.15, 0], aligned_edge=LEFT)
        capA = fit_width(Text("cumulative: ฟลักซ์เสริมกัน", font_size=19, color=K_OVER), 4.6).move_to([2.0, 1.85, 0], aligned_edge=LEFT)
        rowA = flux_row(False).move_to([2.0, 1.35, 0], aligned_edge=LEFT)
        effA = fit_width(Text("→ ฟลักซ์รวมมาก → E มาก → Vt สูงกว่าแบบขนาน", font_size=17, color=GRAYTXT), 4.7).move_to([2.0, 0.85, 0], aligned_edge=LEFT)
        capB = fit_width(Text("differential: ฟลักซ์หักล้างกัน", font_size=19, color=K_DIFF), 4.6).move_to([2.0, 0.1, 0], aligned_edge=LEFT)
        rowB = flux_row(True).move_to([2.0, -0.4, 0], aligned_edge=LEFT)
        effB = fit_width(Text("→ ฟลักซ์รวมน้อย → E น้อย → Vt ตกเร็วกว่าขนาน", font_size=17, color=GRAYTXT), 4.7).move_to([2.0, -0.9, 0], aligned_edge=LEFT)

        self.say("เครื่องแบบผสม = ฟลักซ์ชันท์ + ฟลักซ์เซรี่ → E มากกว่าแบบขนาน → Vt สูงกว่าที่ทุกโหลด (รูป 8-9)", color=OK)
        self.play(Create(g), Create(nl), Create(rated), FadeIn(t_nl), FadeIn(t_rated), run_time=1.2)
        self.play(Create(c_sh), FadeIn(lg[1]), run_time=1.0)
        self.play(Create(c_cu), FadeIn(lg[0]), run_time=1.0)
        gp = DoubleArrow(ax.c2p(1.05, 0.79), ax.c2p(1.05, 0.905), buff=0, color=OK, stroke_width=3, tip_length=0.1)
        self.play(FadeIn(capA), FadeIn(rowA), FadeIn(effA), Create(gp), run_time=1.0)
        self.wait(1.0)

        self.say("8-12 differential: กลับทิศกระแสเซรี่ → ฟลักซ์เซรี่หักล้างชันท์ → ฟลักซ์รวมลดลงตามโหลด", color=WARN)
        self.play(FadeOut(gp), Create(c_df), FadeIn(lg[2]), FadeIn(capB), FadeIn(rowB), FadeIn(effB), run_time=1.6)
        self.wait(1.0)
        self.say("ที่โหลดเท่ากัน: cumulative สูงสุด · ขนานกลาง · differential ต่ำสุดและวกกลับ", color=OK)
        self.play(Indicate(c_cu, color=K_OVER, scale_factor=1.0), run_time=0.9)
        self.play(Indicate(c_sh, color=K_SHUNT, scale_factor=1.0), run_time=0.9)
        self.play(Indicate(c_df, color=K_DIFF, scale_factor=1.0), run_time=0.9)
        self.wait(1.4)
        self.exam("คำถามท้ายบท 8-15: เครื่องกำเนิดแบบผสมชนิด cumulative และ differential เหมือนหรือต่างกันอย่างไร",
                  "cumulative: เซรี่เสริมชันท์ → Vt สูงกว่าแบบขนาน · differential: กลับขั้วต่อเซรี่ ฟลักซ์หักล้าง → Vt ตกเร็วกว่าและวกกลับ")


# =============================================================== P19  หน้า 19
def kind_chip(num, th, en, col, w=3.9):
    box = RoundedRectangle(width=w, height=0.62, corner_radius=0.12, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.14)
    t = Text(f"{num}  {th} ({en})", font_size=20, color=WHITE)
    t = fit_width(t, w - 0.3).move_to(box)
    return VGroup(box, t)


class P19_OverCompound(Lesson):
    """8-12 จบ (differential ใช้งานเชื่อม/ชุบโลหะ) + 8-13 ขั้นของการผสม 3 ระดับ + over compound (รูป 8-10)"""

    def construct(self):
        self.head("8-12 ใช้งาน · 8-13 ขั้นของการผสม", "หน้า 19 · 8-12, 8-13, รูปที่ 8-10")
        # ---- ก) differential: กระแสค่อนข้างคงที่ -> งานเชื่อม / ชุบโลหะ
        g, ax, nl, rated, t_nl, t_rated = vt_plot([-5.2, -2.7])
        c_df = cv(ax, FAM_A["diff"], K_DIFF)
        zone = Rectangle(width=ax.c2p(0.7, 0)[0] - ax.c2p(0.42, 0)[0], height=ax.c2p(0, 0.62)[1] - ax.c2p(0, 0.05)[1],
                         stroke_color=YEL, stroke_width=2, fill_color=YEL, fill_opacity=0.10).move_to(ax.c2p(0.56, 0.335))
        t_const = Text("IL แทบคงที่\nแม้ Vt เปลี่ยนมาก", font_size=17, color=YEL, line_spacing=0.9).next_to(zone, RIGHT, buff=0.15)
        weld = VGroup(Line([-0.25, 0.3, 0], [0.15, -0.1, 0], color=METAL, stroke_width=6),
                      *[Line(0.14 * np.array([np.cos(a), np.sin(a), 0]), 0.3 * np.array([np.cos(a), np.sin(a), 0]), color=YEL, stroke_width=3)
                        for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to([0, 0, 0])
        weld[1:].shift(np.array([0.15, -0.1, 0]))
        tank = VGroup(RoundedRectangle(width=0.9, height=0.55, corner_radius=0.06, stroke_color=METAL, stroke_width=3, fill_color=OK, fill_opacity=0.25),
                      Line([-0.18, 0.5, 0], [-0.18, -0.05, 0], color=C_R, stroke_width=5), Line([0.18, 0.5, 0], [0.18, -0.05, 0], color=C_IF, stroke_width=5))
        c1 = card([("งานเชื่อมไฟฟ้า", K_DIFF), "ต้องการกระแสคงที่"], w=3.6, color=K_DIFF)
        c2 = card([("งานชุบโลหะด้วยไฟฟ้า", K_DIFF), "ต้องการกระแสคงที่"], w=3.6, color=K_DIFF)
        c1.move_to([4.7, 1.15, 0])
        c2.move_to([4.7, -0.55, 0])
        weld.scale(0.9).next_to(c1, LEFT, buff=0.2).shift(LEFT * 0.0)
        tank.next_to(c2, LEFT, buff=0.3)
        self.say("differential ไม่ใช้ส่งกำลัง: กระแสค่อนข้างคงที่ขณะใช้งาน → ใช้กับงานเชื่อม และงานชุบโลหะด้วยไฟฟ้า", color=K_DIFF)
        self.play(Create(g), Create(nl), FadeIn(t_nl), run_time=0.9)
        self.play(Create(c_df), run_time=1.0)
        self.play(FadeIn(zone), FadeIn(t_const), run_time=0.8)
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(weld), run_time=0.8)
        self.play(FadeIn(c2, shift=LEFT * 0.2), FadeIn(tank), run_time=0.8)
        self.wait(1.4)

        # ---- ข) 8-13 สามขั้น
        self.say("8-13: เครื่องผสม cumulative แบ่งเป็น 3 ขั้น (ระดับ) ของการผสม", color=OK)
        self.play(FadeOut(VGroup(g, nl, t_nl, c_df, zone, t_const, c1, c2, weld, tank)), run_time=0.6)
        chips3 = VGroup(kind_chip(1, "ผสมเกิน", "over compound", K_OVER), kind_chip(2, "ผสมพอดี", "flat compound", K_FLAT),
                        kind_chip(3, "ผสมขาด", "under compound", K_UNDER)).arrange(DOWN, buff=0.28).move_to([0, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips3], lag_ratio=0.45), run_time=1.8)
        self.wait(1.0)
        self.play(chips3.animate.scale(0.82).move_to([4.45, 1.45, 0]), run_time=0.9)

        # ---- ค) over compound รูป 8-10
        self.say("ผสมเกิน (over compound): Vt ที่ขั้วสูงกว่าแบบขนาน และเพิ่มขึ้นเมื่อเพิ่มโหลด (รูป 8-10)", color=K_OVER)
        g2, ax2, nl2, rated2, t_nl2, t_rated2 = vt_plot([-5.2, -2.7])
        c_sh = cv(ax2, FAM_A["shunt"], K_SHUNT)
        c_ov = cv(ax2, FAM_A["over"], K_OVER, 6)
        lg2 = VGroup(legend_item(K_OVER, "ผสมเกิน (cumulative)"), legend_item(K_SHUNT, "แบบขนาน")).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lg2.move_to([2.4, -0.55, 0], aligned_edge=LEFT)
        why = fit_width(card([("แอมแปร์-เทอร์นเซรี่เสริมฟลักซ์ชันท์", K_OVER), "โหลดเพิ่ม → ฟลักซ์รวม ↑ → E ↑", "→ Vt ที่ขั้ว ↑ (สูงกว่าตอนไม่มีโหลด)"],
                   w=4.2, color=K_OVER, size=19), 4.4).move_to([4.5, -1.95, 0])
        self.play(Create(g2), Create(nl2), Create(rated2), FadeIn(t_nl2), FadeIn(t_rated2), run_time=1.0)
        self.play(Create(c_sh), FadeIn(lg2[1]), Indicate(chips3[0], color=K_OVER), run_time=1.0)
        self.play(Create(c_ov), FadeIn(lg2[0]), run_time=1.4)
        self.play(FadeIn(why, shift=UP * 0.2), run_time=0.9)
        self.wait(2.0)
        self.exam("คำถามท้ายบท 8-16: จงอธิบายลักษณะสมบัติของเครื่องกำเนิดแบบผสมชนิดผสมเกิน",
                  "Vt สูงกว่าแบบขนาน และเพิ่มขึ้นตามโหลด เพราะแอมแปร์-เทอร์นเซรี่เสริมฟลักซ์ชันท์ → ฟลักซ์รวม ↑ → E ↑")


# =============================================================== P20  หน้า 20
class P20_Ex84Setup(Lesson):
    """over compound เหมาะส่งกำลังไกล (ชดเชยแรงดันตกในสาย) + ตย.8-4 โจทย์ + รูป 8-11"""

    def construct(self):
        self.head("over compound เหมาะส่งไกล · ตย.8-4 โจทย์", "หน้า 20 · ตย.8-4, รูปที่ 8-11")
        f = fig811()
        f.shift(LEFT * 0.0)
        self.say("ส่งกำลังไกล: สายยาว → ความต้านทานสายมาก → โหลดยิ่งมาก แรงดันตกคร่อมสายยิ่งมาก", color=WARN)
        self.play(Create(VGroup(f.gen, f.top, f.bot, f.rz_t, f.rz_b, f.load)), run_time=1.4)
        self.play(FadeIn(VGroup(*f[1:5])), FadeIn(f.t_load), FadeIn(f.t_rl), Create(f.dimarr), FadeIn(f.t_dim), run_time=0.9)
        self.play(Create(f.vt), Create(f.vl), FadeIn(f.t_vt), FadeIn(f.t_vl), Create(f.il), FadeIn(f.t_il), run_time=1.0)
        self.play(flow(f.path, C_IL, run=1.4), Indicate(f.rz_t, color=C_R), Indicate(f.rz_b, color=C_R))
        gapt = card([("Vt > VL", WARN), "ส่วนต่างคือแรงดันตกในสาย"], w=4.2, color=WARN, size=21).move_to([3.7, 0.1, 0])
        self.play(FadeIn(gapt), run_time=0.7)
        self.wait(1.0)

        self.say("over compound: โหลดเพิ่ม → Vt ที่ขั้วเพิ่ม ชดเชยแรงดันตก → VL ที่โหลดคงที่ (VR ติดลบ)", color=OK)
        self.play(FadeOut(gapt), f.vt.animate.set_color(OK), f.t_vt.animate.set_color(OK), run_time=0.5)
        self.play(Indicate(f.vt, color=C_E, scale_factor=1.0), Indicate(f.vl, color=OK, scale_factor=1.0), run_time=1.2)
        self.wait(0.6)

        self.say("ตัวอย่าง 8-4: โหลด DC 220 V ต้องการ 200 A อยู่ไกลจากเครื่องกำเนิด 990 m สายเคเบิ้ล 500 MCM", color=C_R)
        self.play(f.animate.scale(0.8).move_to([-3.55, -0.35, 0]), run_time=0.9)
        bd = Board(self, x=0.7, y=2.15, gap=0.2)
        bd.add(1, "โจทย์ให้", VGroup(n_text("โหลด 220 V ต้องการกระแส 200 A", size=19), n_text("ห่างเครื่องกำเนิด 990 m สายเคเบิ้ล 500 MCM", size=19),
                                      n_text("R สาย = 0.025 Ω ต่อ 330 m", size=19)).arrange(DOWN, aligned_edge=LEFT, buff=0.07), color=OK, hold=0.2)
        bd.add(2, "ให้หา", VGroup(n_text("(ก) Vt ที่ทำให้ VL = 220 V เมื่อโหลดเต็ม", size=19), n_text("(ข) Vt เมื่อกระแสโหลดเป็นศูนย์", size=19),
                                   n_text("(ค) โวลท์เตจเรกูเลชั่น", size=19)).arrange(DOWN, aligned_edge=LEFT, buff=0.07), color=C_R, hold=0.2)
        note = fit_width(Text("หมายเหตุ: ข้อ (ก) ในโจทย์ PDF พิมพ์ 220 A แต่เฉลยหน้า 21 ใช้ 200 A — คลิปนี้ใช้ 200 A", font_size=16, color=GRAYTXT), 11.5).move_to([0.3, -3.35, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.6)
        self.exam("ตัวอย่าง 8-4: ทำไมการส่งกำลังไกลจึงเลือกเครื่องกำเนิดผสมเกิน",
                  "สายยาว R มาก โหลดเพิ่ม → แรงดันตกในสายเพิ่ม · ผสมเกิน: โหลดเพิ่ม Vt ขั้วเพิ่ม → ชดเชย → VL คงที่ (VR ติดลบ)")


# =============================================================== P21  หน้า 21
class P21_Ex84Solution(Lesson):
    """เฉลย ตย.8-4: R=0.15, ΔV=30, Vt=250/220, VR=-12 % + ผสมพอดี (flat compound) เริ่ม"""

    def construct(self):
        self.head("เฉลย ตย.8-4 · ผสมพอดี (flat compound)", "หน้า 21 · ตย.8-4, 8-13")
        f = fig811()
        f.scale(0.8).move_to([-3.55, -0.2, 0])
        self.add(f)
        self.say("(ก) ความต้านทานสายทั้งหมด: กระแสวิ่งไปแล้วกลับ จึงคูณ 2", color=C_R)
        bd = Board(self, x=0.5, y=2.15, gap=0.16)
        bd.add(1, "ความต้านทานสาย", MathTex(r"R=\frac{0.025\,\Omega}{330}\times 990\times 2=0.15\,\Omega", font_size=30), color=C_R, hold=0.1)
        self.play(Indicate(f.rz_t, color=WHITE), Indicate(f.rz_b, color=WHITE), run_time=0.8)
        rv = _lv(r"R=0.15\,\Omega", C_R, 26).move_to(f.t_rl.get_center() + DOWN * 0.02)
        self.play(Transform(f.t_rl, rv), run_time=0.6)
        bd.add(2, "แรงดันตกในสาย", MathTex(r"200\,\mathrm{A}\times 0.15\,\Omega=30\,\mathrm{V}", font_size=30), color=C_R, hold=0.1)
        bd.add(3, "Vt = VL + แรงดันตก", MathTex(r"V_t=220\,\mathrm{V}+30\,\mathrm{V}=250\,\mathrm{V}", font_size=30), color=C_E, hold=0.1)
        t250 = _lv(r"V_t=250\,\mathrm{V}", C_E, 26).move_to(f.t_vt.get_center() + RIGHT * 0.42)
        self.play(Transform(f.t_vt, t250), run_time=0.7)
        self.wait(0.8)

        self.say("(ข) ไม่มีโหลด: กระแส = 0 → ไม่มีแรงดันตกในสาย → Vt เท่ากับ VL", color=C_IL)
        self.play(*[FadeOut(r) for r in bd.rows], FadeOut(f.il), FadeOut(f.t_il), run_time=0.6)
        bd2 = Board(self, x=0.5, y=2.15, gap=0.16)
        bd2.add(1, "(ข) ตอนไม่มีโหลด", MathTex(r"V_t=220\,\mathrm{V}+0\,\mathrm{V}=220\,\mathrm{V}", font_size=30), color=C_IL, hold=0.1)
        t220 = _lv(r"V_t=220\,\mathrm{V}", C_E, 26).move_to(f.t_vt.get_center())
        self.play(Transform(f.t_vt, t220), run_time=0.6)
        self.wait(0.6)

        self.say("(ค) โวลท์เตจเรกูเลชั่น: VNL = 220 V และ VFL = 250 V", color=OK)
        bd2.add(2, "(ค) VR", MathTex(r"VR=\frac{V_{NL}-V_{FL}}{V_{FL}}\times 100=\frac{220-250}{250}\times 100", font_size=28), color=OK, hold=0.1)
        res = VGroup(MathTex(r"VR=-12\,\%", font_size=40, color=OK), n_text("ติดลบ = Vt ตอนมีโหลด สูงกว่าตอนไม่มีโหลด", size=18, color=GRAYTXT)).arrange(RIGHT, buff=0.3)
        res.move_to([3.4, -1.6, 0])
        res = fit_width(res, 6.2).move_to([3.5, -1.6, 0])
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.9)
        self.play(Indicate(res[0], color=WHITE), run_time=0.7)
        self.wait(1.2)

        self.say("ผสมพอดี (flat compound): Vt เต็มโหลด = Vt ไม่มีโหลด — แก้จากผสมเกินที่แรงดันอาจสูงเกินไป", color=YEL)
        self.play(FadeOut(VGroup(f, *bd2.rows, res)), run_time=0.7)
        gg, ax, nl, rated, t_nl, t_rated = vt_plot([-4.2, -2.7])
        c_ov = cv(ax, FAM_A["over"], K_OVER)
        c_fl = cv(ax, FAM_A["flat"], K_FLAT, 6)
        lg = VGroup(legend_item(K_OVER, "ผสมเกิน"), legend_item(K_FLAT, "ผสมพอดี")).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, 1.0, 0], aligned_edge=LEFT)
        dot = Dot(ax.c2p(1.0, 1.0), radius=0.1, color=K_FLAT)
        t_eq = fit_width(Text("ที่กระแสพิกัด\nVt = Vt ไม่มีโหลด", font_size=19, color=K_FLAT, line_spacing=0.9), 3.2).move_to([3.4, -0.55, 0], aligned_edge=LEFT)
        self.play(Create(gg), Create(nl), Create(rated), FadeIn(t_nl), FadeIn(t_rated), run_time=1.0)
        self.play(Create(c_ov), FadeIn(lg[0]), run_time=1.0)
        self.play(Create(c_fl), FadeIn(lg[1]), run_time=1.2)
        self.play(FadeIn(dot, scale=2.0), FadeIn(t_eq), run_time=0.8)
        self.wait(1.6)
        self.exam("ตัวอย่าง 8-4 / คำถามท้ายบท 8-17: หา Vt ที่ขั้วและ VR · ผสมพอดีคืออะไร",
                  "R = 0.15 Ω · แรงดันตก 30 V · Vt = 250 V / 220 V · VR = −12 % · ผสมพอดี: Vt เท่ากัน")


# =============================================================== P22  หน้า 22
def fig812():
    """รูป 8-12: short-shunt + ไดเวอร์เตอร์ขนานกับเซรี่ฟิลด์ (ชิ้นส่วนเป็นแอตทริบิวต์)"""
    XJ, YTOP, YDIV, YB = -0.6, 1.75, 0.7, -2.55
    XR, XF = -3.9, -2.5
    arm = arm_sym([XJ, -1.0], r=0.45, letter="G")
    a1 = Text("A1", font_size=16, color=GRAYTXT).move_to([XJ + 0.5, -0.5, 0])
    a2 = Text("A2", font_size=16, color=GRAYTXT).move_to([XJ + 0.5, -1.5, 0])
    w_a1 = wire((XJ, -0.55), (XJ, YTOP))
    w_top_l = wire((XJ, YTOP), (0.7, YTOP))
    ser = coil_sym([0.7, YTOP], [2.5, YTOP], n=4, r=0.1, color=C_IS)
    w_top_r = wire((2.5, YTOP), (4.3, YTOP))
    w_d_l = wire((XJ, YDIV), (0.7, YDIV))
    div = res_zig([0.7, YDIV], [2.5, YDIV], n=4, color=YEL)
    w_d_r = wire((2.5, YDIV), (3.1, YDIV), (3.1, YTOP))
    w_b = wire((XJ, -1.45), (XJ, YB), (4.3, YB))
    w_rh = wire((XJ, YTOP), (XR, YTOP))
    rh = res_zig([XR, YTOP], [XR, 0.3], n=4, color=C_R)
    w_wip = wire((XR, 0.3), (XF, 0.3), (XF, -0.2))
    sh = coil_sym([XF, -0.2], [XF, -2.0], n=4, r=0.1, color=C_IF)
    w_sh_b = wire((XF, -2.0), (XF, YB), (XJ, YB))
    dots = VGroup(*[Dot([x, y, 0], radius=0.08, color=WHITE) for x, y in ((XJ, YTOP), (XJ, YDIV), (XJ, YB), (4.3, YTOP), (4.3, YB))])
    t_p = Text("+", font_size=24, color=WHITE).move_to([4.6, YTOP, 0])
    t_n = Text("−", font_size=24, color=WHITE).move_to([4.6, YB, 0])
    t_s = Text("เซรี่ฟิลด์ (S1–S2)", font_size=17, color=C_IS).move_to([1.6, 1.22, 0])
    t_rh = Text("รีโอสตาท", font_size=17, color=C_R).move_to([XR - 0.85, 1.0, 0])
    t_sh = Text("ชันท์ฟิลด์ (F1–F2)", font_size=17, color=C_IF)
    t_sh.move_to([XF - 0.2 - t_sh.width / 2, -1.1, 0])
    t_arm = Text("อาร์เมเจอร์", font_size=17, color=C_E).move_to([XJ + 0.62 + 0.62, -1.0, 0])
    base = VGroup(arm, a1, a2, w_a1, w_top_l, ser, w_top_r, w_b, w_rh, rh, w_wip, sh, w_sh_b, dots, t_p, t_n, t_s, t_rh, t_sh, t_arm)
    divg = VGroup(w_d_l, div, w_d_r)
    t_d = Text("ไดเวอร์เตอร์", font_size=17, color=YEL).move_to([1.6, -0.05, 0])
    g = VGroup(base, divg, t_d)
    g.base, g.divg, g.t_d, g.ser, g.div = base, divg, t_d, ser, div
    g.path_s = wire((XJ, YTOP), (4.3, YTOP))
    g.path_d = wire((XJ, YDIV), (3.1, YDIV), (3.1, YTOP), (4.3, YTOP))
    return g


class P22_Diverter(Lesson):
    """ไดเวอร์เตอร์ (รูป 8-12): ต่อขนานเซรี่ฟิลด์ เบี่ยงกระแส → ปรับขั้นการผสม over → flat (→ under)"""

    def construct(self):
        self.head("ไดเวอร์เตอร์ ปรับ over → flat compound", "หน้า 22 · รูปที่ 8-12")
        f = fig812()
        t = ValueTracker(0.0)
        # มาตรวัด Vt ที่โหลดเต็ม เทียบเส้น Vt ไม่มีโหลด
        BX, BY0, BH = 5.95, -2.2, 3.4
        frame = Rectangle(width=0.7, height=BH, stroke_color=GRAYTXT, stroke_width=2).move_to([BX, BY0 + BH / 2, 0])
        y_nl = BY0 + 1.9
        dash = DashedLine([BX - 0.55, y_nl, 0], [BX + 0.55, y_nl, 0], color=YEL, stroke_width=3, dash_length=0.1)
        t_nlv = _lv(r"V_{NL}", YEL, 24).next_to(dash, RIGHT, buff=0.04)
        t_gauge = fit_width(Text("Vt ที่โหลดเต็ม", font_size=17, color=GRAYTXT), 1.7).move_to([BX, BY0 - 0.35, 0])
        bar = always_redraw(lambda: Rectangle(width=0.7, height=2.45 - 0.55 * t.get_value(), stroke_width=0, fill_color=C_E,
                                              fill_opacity=0.85).move_to([BX, BY0 + (2.45 - 0.55 * t.get_value()) / 2, 0]))
        arr_s = always_redraw(lambda: Arrow([0.9, 2.1, 0], [0.9 + 1.5 - 0.75 * t.get_value(), 2.1, 0], buff=0, color=C_IS, stroke_width=4, tip_length=0.18))
        arr_d = always_redraw(lambda: Arrow([0.9, 0.38, 0], [0.9 + 0.4 + 1.1 * t.get_value(), 0.38, 0], buff=0, color=YEL, stroke_width=4, tip_length=0.18))
        lab_s = _lv(r"I_s", C_IS, 24).move_to([2.95, 2.1, 0])
        lab_d = _lv(r"I_d", YEL, 24).move_to([2.95, 0.38, 0])
        kind = Text("ผสมเกิน", font_size=21, color=K_OVER)
        kind.move_to([BX, BY0 + BH + 0.4, 0])

        self.say("ผสมเกินให้ Vt สูงเกินสำหรับบางงาน → ต้องลดแอมแปร์-เทอร์นเซรี่ แต่ลดจำนวนรอบไม่ได้ ถ้าไม่ถอดเครื่อง", color=WARN)
        self.play(Create(f.base), run_time=1.6)
        no_turn = fit_width(Text("จำนวนรอบเซรี่: แตะต้องไม่ได้", font_size=17, color=WARN), 3.4).move_to([1.6, 2.15, 0])
        self.play(FadeIn(no_turn), Indicate(f.ser, color=WARN), run_time=1.0)
        self.wait(0.6)

        self.say("วิธีง่ายสุด: ต่อความต้านทานต่ำ \"ไดเวอร์เตอร์\" ขนานกับเซรี่ฟิลด์ → เบี่ยงกระแสออกจากเซรี่", color=YEL)
        self.play(FadeOut(no_turn), Create(f.divg), FadeIn(f.t_d), run_time=1.2)
        self.play(FadeIn(frame), FadeIn(dash), FadeIn(t_nlv), FadeIn(t_gauge), run_time=0.7)
        self.add(arr_s, arr_d, bar)
        self.play(FadeIn(lab_s), FadeIn(lab_d), FadeIn(kind), run_time=0.7)
        self.play(flow(f.path_s, C_IS, run=1.2), flow(f.path_d, YEL, run=1.2))
        self.wait(0.4)

        self.say("ปรับ R ของไดเวอร์เตอร์ → ปรับกระแสเซรี่ได้ละเอียด → ตั้งให้ Vt เต็มโหลด = Vt ไม่มีโหลด (ผสมพอดี)", color=OK)
        self.play(t.animate.set_value(1.0), run_time=3.0)
        flat = Text("ผสมพอดี", font_size=21, color=K_FLAT).move_to(kind)
        self.play(Transform(kind, flat), run_time=0.5)
        self.play(Indicate(bar, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.wait(1.2)
        self.say("ผสมขาด (under compound): ผลของเซรี่ทำให้ Vt ที่โหลดเต็มต่ำกว่า Vt ที่ไม่มีโหลด — ปรับไดเวอร์เตอร์ได้เหมือนกัน (หน้า 23)", color=K_UNDER)
        und = card([("ผสมขาด (under compound)", K_UNDER), "Vt เต็มโหลด < Vt ไม่มีโหลด"], w=3.4, color=K_UNDER).move_to([-5.0, -2.45, 0])
        self.play(FadeIn(und, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        self.exam("คำถามท้ายบท 8-19: ไดเวอร์เตอร์คืออะไร",
                  "ความต้านทานต่ำต่อขนานกับขดลวดเซรี่ฟิลด์ · เบี่ยงกระแสออกจากเซรี่ เพื่อปรับขั้นของการผสม (ผสมเกิน → ผสมพอดี)")


# =============================================================== P23  หน้า 23
def fam_f(name):
    pts = FAM_A[name]
    return PchipInterpolator([q[0] for q in pts], [q[1] for q in pts])


F_OVER, F_FLAT, F_UNDER, F_SHUNT = fam_f("over"), fam_f("flat"), fam_f("under"), fam_f("shunt")


def fcv(ax, f, col, w=5, x1=1.25, n=30):
    m = VMobject(stroke_color=col, stroke_width=w)
    m.set_points_smoothly([ax.c2p(float(x), float(f(x))) for x in np.linspace(0.0, x1, n)])
    return m


def dotted(m, col, w=3, n=40):
    d = DashedVMobject(m, num_dashes=n, dashed_ratio=0.5)
    d.set_stroke(color=col, width=w)
    return d


class P23_UnderCompound(Lesson):
    """ไดเวอร์เตอร์ลด Rd จากค่าผสมพอดี → กระแสเซรี่ลด → Vt ต่ำลง = ผสมขาด; Rd = 0 → แบบขนาน; รูป 8-13(ก)"""

    def construct(self):
        self.head("ผสมขาด (under compound) · รูป 8-13(ก)", "หน้า 23 · รูปที่ 8-13(ก)")
        t = ValueTracker(0.0)        # 0 = ตั้งผสมพอดี, 1 = Rd = 0 (ลัดวงจรเซรี่ฟิลด์)
        XA, XB, YS, YD, YM = -5.5, -2.0, 0.55, -0.95, -0.2
        ser = coil_sym([-4.85, YS], [-2.65, YS], n=4, r=0.1, color=C_IS)
        div = res_zig([-4.85, YD], [-2.65, YD], n=4, color=YEL)
        base = VGroup(wire((-6.5, YM), (XA, YM)), wire((XB, YM), (-1.25, YM)), wire((XA, YS), (XA, YD)), wire((XB, YS), (XB, YD)),
                      ser, wire((XA, YS), (-4.85, YS)), wire((-2.65, YS), (XB, YS)),
                      div, wire((XA, YD), (-4.85, YD)), wire((-2.65, YD), (XB, YD)),
                      Text("เซรี่ฟิลด์", font_size=18, color=C_IS).move_to([-3.75, YS - 0.42, 0]),
                      Text("ไดเวอร์เตอร์", font_size=18, color=YEL).move_to([-3.75, YD + 0.45, 0]),
                      _lv(r"I_L", C_IL, 26).move_to([-6.05, YM + 0.35, 0]))

        def branch_arrow(y, cur):
            ln = cur()
            if ln < 0.2:
                return Dot([-4.8, y, 0], radius=0.02, color=BLACK)
            col = C_IS if y > 0 else YEL
            return Arrow([-4.8, y, 0], [-4.8 + ln, y, 0], buff=0, color=col, stroke_width=4, tip_length=0.17)

        arr_s = always_redraw(lambda: branch_arrow(1.2, lambda: 1.4 * (1 - t.get_value())))
        arr_d = always_redraw(lambda: branch_arrow(-1.55, lambda: 0.3 + 1.1 * t.get_value()))
        lab_is = _lv(r"I_s", C_IS, 26).move_to([-2.85, 1.2, 0])
        lab_id = _lv(r"I_d", YEL, 26).move_to([-2.85, -1.55, 0])
        SX0, SX1, SY = -5.9, -1.6, -2.5
        bar = Line([SX0, SY, 0], [SX1, SY, 0], color=GRAYTXT, stroke_width=4)
        knob = always_redraw(lambda: Circle(radius=0.14, stroke_color=WHITE, stroke_width=2, fill_color=K_UNDER, fill_opacity=1).move_to(
            [SX0 + (SX1 - SX0) * t.get_value(), SY, 0]))
        l0 = Text("Rd ค่าผสมพอดี", font_size=17, color=YEL).move_to([SX0 + 0.55, SY - 0.42, 0])
        l1 = Text("Rd = 0", font_size=17, color=K_SHUNT).move_to([SX1 - 0.3, SY - 0.42, 0])

        g, ax, nl, rated, t_nl, t_rated = vt_plot([0.7, -2.3], x_len=4.8, y_len=3.9)
        ref_f = dotted(fcv(ax, F_FLAT, K_FLAT), K_FLAT)
        ref_s = dotted(fcv(ax, F_SHUNT, K_SHUNT), K_SHUNT)
        e_f = Text("ผสมพอดี", font_size=17, color=K_FLAT).next_to(ax.c2p(1.25, float(F_FLAT(1.25))), RIGHT, buff=0.1)
        e_s = Text("แบบขนาน", font_size=17, color=K_SHUNT).next_to(ax.c2p(1.25, float(F_SHUNT(1.25))), RIGHT, buff=0.1)
        mv = always_redraw(lambda: fcv(ax, lambda x: (1 - t.get_value()) * float(F_FLAT(x)) + t.get_value() * float(F_SHUNT(x)), K_UNDER, 6))

        def status():
            v = t.get_value()
            if v < 0.03:
                txt, col = "ตั้งเป็นผสมพอดี", K_FLAT
            elif v > 0.97:
                txt, col = "Rd = 0 → เหมือนแบบขนาน", K_SHUNT
            else:
                txt, col = "ผสมขาด (under compound)", K_UNDER
            return Text(txt, font_size=22, color=col).move_to([3.1, 2.0, 0])
        st = always_redraw(status)

        self.say("ลดความต้านทานไดเวอร์เตอร์ลงจากค่าผสมพอดี → กระแสไหลผ่านเซรี่ฟิลด์ลดลง → Vt ที่ขั้วต่ำลง", color=K_UNDER)
        self.play(Create(base), run_time=1.3)
        self.play(Create(g), Create(nl), Create(rated), FadeIn(t_nl), FadeIn(t_rated), run_time=1.0)
        self.add(arr_s, arr_d, mv, st, knob)
        self.play(FadeIn(lab_is), FadeIn(lab_id), Create(bar), FadeIn(l0), FadeIn(l1), FadeIn(ref_f), FadeIn(ref_s), FadeIn(e_f), FadeIn(e_s), run_time=1.0)
        self.wait(0.6)
        self.play(t.animate.set_value(0.45), run_time=2.6)
        self.wait(0.5)

        self.say("ลดจน Rd = 0 → ไม่มีกระแสผ่านเซรี่ฟิลด์เลย ไม่เป็น cumulative อีกต่อไป ทำงานเหมือนเครื่องกำเนิดแบบขนาน", color=K_SHUNT)
        self.play(t.animate.set_value(1.0), run_time=2.6)
        self.wait(0.8)

        self.say("Rd อยู่ระหว่างค่าผสมพอดีกับ 0 → Vt สูงกว่าแบบขนาน แต่ต่ำกว่าผสมพอดี = ผสมขาด", color=K_UNDER)
        self.play(t.animate.set_value(0.45), run_time=1.8)
        band = Polygon(*[ax.c2p(float(x), float(F_FLAT(x))) for x in np.linspace(0, 1.25, 12)],
                       *[ax.c2p(float(x), float(F_SHUNT(x))) for x in np.linspace(1.25, 0, 12)],
                       stroke_width=0, fill_color=K_UNDER, fill_opacity=0.16)
        zone = Text("ผสมขาด", font_size=20, color=K_UNDER).move_to([(SX0 + SX1) / 2, SY + 0.4, 0])
        zl = Line([SX0 + 0.14, SY, 0], [SX1 - 0.14, SY, 0], color=K_UNDER, stroke_width=8)
        self.play(FadeIn(band), FadeIn(zone), Create(zl), run_time=1.0)
        self.wait(1.2)

        # ---- รูป 8-13(ก): เทียบทุกชนิด (Vt ไม่มีโหลดเท่ากัน)
        self.say("รูป 8-13(ก): ตั้ง Vt ตอนไม่มีโหลดให้เท่ากัน แล้วเทียบเคอร์ฟทุกชนิดบนกราฟเดียว", color=OK)
        for m in (arr_s, arr_d, knob, st, mv):
            m.clear_updaters()
        self.play(FadeOut(VGroup(base, arr_s, arr_d, lab_is, lab_id, bar, knob, zone, zl, l0, l1, st, ref_f, ref_s, e_f, e_s, band)), run_time=0.8)
        c_ov = fcv(ax, F_OVER, K_OVER, 5)
        c_df = cv(ax, FAM_A["diff"], K_DIFF, 5)
        lg = VGroup(legend_item(K_OVER, "ผสมเกิน (cumulative)", 20), legend_item(K_FLAT, "ผสมพอดี (cumulative)", 20),
                    legend_item(K_UNDER, "ผสมขาด (cumulative)", 20), legend_item(K_SHUNT, "แบบขนาน", 20),
                    legend_item(K_DIFF, "differential", 20)).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-4.0, 0.0, 0])
        c_fl = fcv(ax, F_FLAT, K_FLAT, 5)
        c_sh = fcv(ax, F_SHUNT, K_SHUNT, 5)
        self.play(Create(c_ov), FadeIn(lg[0]), run_time=1.0)
        self.play(Create(c_fl), FadeIn(lg[1]), run_time=0.9)
        self.play(FadeIn(lg[2]), run_time=0.5)
        self.play(Create(c_sh), FadeIn(lg[3]), run_time=0.9)
        self.play(Create(c_df), FadeIn(lg[4]), run_time=1.1)
        self.wait(1.4)
        self.exam("คำถามท้ายบท 8-18: จงอธิบายลักษณะสมบัติของเครื่องกำเนิดแบบผสมชนิดผสมขาด",
                  "Rd ต่ำกว่าค่าผสมพอดี (แต่ไม่ถึง 0) → กระแสเซรี่ลด → Vt เต็มโหลดต่ำกว่า Vt ไม่มีโหลด แต่สูงกว่าแบบขนาน")


# =============================================================== P24  หน้า 24
FAM_B_DIFF = [(0, 1.31), (0.25, 1.14), (0.45, 0.93), (0.6, 0.68), (0.68, 0.42), (0.66, 0.2), (0.58, 0.0)]


class P24_CompareAllTypes(Lesson):
    """รูป 8-13(ก) → (ข): เลื่อนทุกเส้นให้ Vt เต็มโหลดเท่ากัน + อ่านย้อนจากเต็มโหลดไปไม่มีโหลด + 8-14 เริ่ม"""

    def construct(self):
        self.head("รูป 8-13 เทียบทุกชนิด · 8-14 เริ่ม", "หน้า 24 · รูปที่ 8-13(ข), 8-14")
        k = ValueTracker(0.0)        # 0 = รูป (ก) Vt ไม่มีโหลดเท่ากัน, 1 = รูป (ข) Vt เต็มโหลดเท่ากัน
        g, ax, nl, rated, t_nl, t_rated = vt_plot([-4.6, -2.45], x_len=6.0, y_len=4.2, ymax=1.45)

        def mk(name, col, w=5):
            f = {"over": F_OVER, "flat": F_FLAT, "under": F_UNDER, "shunt": F_SHUNT}[name]
            return always_redraw(lambda: fcv(ax, lambda x: float(f(x)) + k.get_value() * (1.0 - float(f(1.0))), col, w))

        def diff_now():
            kv = k.get_value()
            pts = [((1 - kv) * a[0] + kv * b[0], (1 - kv) * a[1] + kv * b[1]) for a, b in zip(FAM_A["diff"], FAM_B_DIFF)]
            return cv(ax, pts, K_DIFF, 5)

        c_ov, c_fl, c_un, c_sh = mk("over", K_OVER), mk("flat", K_FLAT), mk("under", K_UNDER), mk("shunt", K_SHUNT)
        c_df = always_redraw(diff_now)
        lg = VGroup(legend_item(K_OVER, "ผสมเกิน", 19), legend_item(K_FLAT, "ผสมพอดี", 19), legend_item(K_UNDER, "ผสมขาด", 19),
                    legend_item(K_SHUNT, "แบบขนาน", 19), legend_item(K_DIFF, "differential", 19)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lg.move_to([4.7, 0.95, 0])
        t_leg = Text("ชนิดของเครื่องกำเนิด", font_size=18, color=GRAYTXT).next_to(lg, UP, buff=0.2)

        self.say("รูป 8-13(ก): ตั้ง Vt ตอนไม่มีโหลดให้เท่ากัน → ผสมเกินสูงขึ้นตามโหลด · ผสมพอดีเกือบคงที่ · ที่เหลือลดลง", color=OK)
        self.play(Create(g), Create(nl), Create(rated), FadeIn(t_nl), FadeIn(t_rated), FadeIn(t_leg), FadeIn(lg), run_time=1.2)
        self.add(c_ov, c_fl, c_un, c_sh, c_df)
        self.wait(1.8)

        self.say("รูป 8-13(ข): ตั้งใหม่ให้ Vt ตอนโหลดเต็มพิกัดเท่ากัน — เลื่อนทุกเส้นให้ผ่านจุดแรงดันพิกัดที่กระแสพิกัด", color=C_PHI)
        self.play(k.animate.set_value(1.0), FadeOut(t_nl), run_time=3.2)
        t_vr = Text("แรงดันพิกัด", font_size=17, color=GRAYTXT).next_to(ax.c2p(0, 1.0), LEFT, buff=0.12)
        pt = Dot(ax.c2p(1.0, 1.0), radius=0.1, color=WHITE)
        self.play(FadeIn(t_vr), FadeIn(pt, scale=2.2), run_time=0.8)
        self.wait(1.2)

        self.say("อ่านย้อนจากเต็มโหลดกลับไปไม่มีโหลด: เครื่องที่ Vt เพิ่มตามโหลด จะมี Vt ลดลงเมื่อโหลดลด (และกลับกัน)", color=YEL)
        for m in (c_ov, c_fl, c_un, c_sh, c_df):
            m.clear_updaters()
        self.play(FadeOut(VGroup(lg, t_leg)), run_time=0.5)
        cd1 = card([("ผสมเกิน", K_OVER), "โหลด ↑ → Vt ↑", "ย้อนกลับ: โหลด ↓ → Vt ↓"], w=3.8, color=K_OVER).move_to([4.7, 1.2, 0])
        cd2 = card([("แบบขนาน / ผสมขาด", K_UNDER), "โหลด ↑ → Vt ↓", "ย้อนกลับ: โหลด ↓ → Vt ↑"], w=3.8, color=K_UNDER).move_to([4.7, -0.7, 0])
        self.play(FadeIn(cd1, shift=LEFT * 0.2), Indicate(c_ov, color=K_OVER, scale_factor=1.0), run_time=1.1)
        self.play(FadeIn(cd2, shift=LEFT * 0.2), Indicate(c_sh, color=K_SHUNT, scale_factor=1.0), Indicate(c_un, color=K_UNDER, scale_factor=1.0), run_time=1.1)
        self.wait(1.6)

        self.say("8-14 แอมแปร์-เทอร์นของเซรี่ฟิลด์: ตั้งระดับการผสมที่ต้องการได้อย่างไร (ต่อหน้า 25)", color=C_IS)
        self.play(FadeOut(VGroup(cd1, cd2)), run_time=0.5)
        nx = card([("8-14 แอมแปร์-เทอร์นของเซรี่ฟิลด์", C_IS), "หาแอมแปร์-เทอร์นของเซรี่", "ให้ได้ระดับการผสมที่ต้องการ", "ที่กระแสโหลดเต็มพิกัด (สมการ 8-6)"], w=4.2, color=C_IS, size=19)
        nx = fit_width(nx, 4.4).move_to([4.5, 0.5, 0])
        self.play(FadeIn(nx, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)
        self.exam("คำถามท้ายบท 8-16 ถึง 8-18: เทียบผสมเกิน · ผสมพอดี · ผสมขาด (รูป 8-13)",
                  "เกิน: Vt เต็มโหลด > Vt ไม่มีโหลด · พอดี: เท่ากัน · ขาด: ต่ำกว่า (แต่สูงกว่าแบบขนาน)")


# =============================================================== P25  หน้า 25
class P25_AmpereTurn(Lesson):
    """8-14: ทำไมต้องมีแอมแปร์-เทอร์นจากเซรี่เพิ่ม → สมการ 8-6  Nf(If2 - If1) = Ns Is"""

    def construct(self):
        self.head("8-14 แอมแปร์-เทอร์นของเซรี่ฟิลด์ · สมการ 8-6", "หน้า 25 · 8-14, สมการ 8-6")
        # ---------- ท่อน 1: เหตุผล
        g = make_axes(pos=[-5.6, -2.0], x_len=4.8, y_len=3.5, xmax=1.3, ymax=1.2, xl=r"I_L", yl=r"V_t")
        g.xlab.set_color(C_IL)
        ax = g.ax
        c_sh = fcv(ax, F_SHUNT, K_SHUNT, 5)
        tgt = DashedLine(ax.c2p(0, 1.0), ax.c2p(1.25, 1.0), color=OK, stroke_width=2, dash_length=0.1)
        rate = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 1.15), color=GRAYTXT, stroke_width=2, dash_length=0.1)
        t_tgt = Text("Vt ที่ต้องการ", font_size=17, color=OK).next_to(ax.c2p(0, 1.0), UP, buff=0.1).shift(RIGHT * 0.95)
        t_rate = Text("กระแสพิกัด", font_size=17, color=GRAYTXT).next_to(ax.c2p(1.0, 0), DOWN, buff=0.45)
        dot = Dot(ax.c2p(1.0, float(F_SHUNT(1.0))), radius=0.1, color=K_SHUNT)
        gap = DoubleArrow(ax.c2p(1.0, float(F_SHUNT(1.0))), ax.c2p(1.0, 1.0), buff=0.04, color=WARN, stroke_width=3, tip_length=0.12)
        t_gap = Text("ต่ำเกินไป", font_size=17, color=WARN).next_to(gap, RIGHT, buff=0.1)
        t_shn = Text("ทำงานแบบขนาน", font_size=17, color=K_SHUNT).next_to(dot, DL, buff=0.12)

        self.say("ให้เครื่องทำงานแบบขนานและจ่ายกระแสพิกัด (วัด IL และ If ด้วยแอมมิเตอร์): Vt ต่ำกว่าค่าที่ต้องการ", color=K_SHUNT)
        self.play(Create(g), FadeIn(t_rate), Create(rate), run_time=1.0)
        self.play(Create(c_sh), FadeIn(t_shn), Create(tgt), FadeIn(t_tgt), run_time=1.2)
        self.play(FadeIn(dot, scale=2.0), Create(gap), FadeIn(t_gap), run_time=0.9)
        self.wait(0.8)

        ch1 = chips([(r"I_f\uparrow", "ลดรีโอสตาท", C_IF), (r"\phi\uparrow", "ฟลักซ์เพิ่ม", C_PHI), (r"V_t\uparrow", "แรงดันขั้ว", C_E)], w=1.9)
        ch1 = fit_width(ch1, 6.9).move_to([3.4, 1.35, 0])
        ch2 = chips([(r"I_L\uparrow", "โหลดดึงกระแสเพิ่ม", C_IL), (r"R_L\uparrow", "เพิ่ม R โหลด", WHITE), (r"I_L", "คงที่ที่พิกัด", C_IL)], w=1.9)
        ch2 = fit_width(ch2, 6.9).move_to([3.4, -0.25, 0])
        self.say("ต้องเพิ่ม Vt → เพิ่มกระแสฟิลด์ (ลดรีโอสตาท) แต่ Vt เพิ่มทำให้ IL เพิ่มตาม จึงต้องเพิ่ม R โหลดให้ IL คงที่ที่พิกัด", color=C_PHI)
        self.play(FadeIn(ch1, shift=LEFT * 0.2), run_time=1.0)
        self.play(FadeIn(ch2, shift=LEFT * 0.2), run_time=1.0)
        self.wait(0.8)
        need = card([("สรุป", C_IS), "ที่กระแสพิกัดและ Vt ตามต้องการ", "แอมแปร์-เทอร์นของฟิลด์ต้องมากกว่าตอนทำงานแบบขนาน", "ส่วนที่เพิ่ม ได้จากเซรี่ฟิลด์ (อัตโนมัติตามโหลด)"], w=6.3, color=C_IS, size=19)
        need = fit_width(need, 6.9).move_to([3.4, -1.95, 0])
        self.play(FadeIn(need, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)

        # ---------- ท่อน 2: แท่งแอมแปร์-เทอร์น + สมการ
        self.say("ตัวอย่างขนาดแท่ง (เลขจาก ตย.8-7): ชันท์ให้ Nf·If1 · ที่ต้องการ Nf·If2 · ส่วนที่ขาดเซรี่เติมให้ Ns·Is", color=C_IS)
        self.play(FadeOut(VGroup(g, c_sh, tgt, rate, t_tgt, t_rate, dot, gap, t_gap, t_shn, ch1, ch2, need)), run_time=0.7)
        U, Y0 = 0.5, -2.2
        b1 = Rectangle(width=1.0, height=2.7 * U, stroke_width=0, fill_color=C_IF, fill_opacity=0.85).move_to([-5.4, Y0 + 2.7 * U / 2, 0])
        b2a = Rectangle(width=1.0, height=2.7 * U, stroke_width=0, fill_color=C_IF, fill_opacity=0.85).move_to([-3.4, Y0 + 2.7 * U / 2, 0])
        b2b = Rectangle(width=1.0, height=2.3 * U, stroke_width=0, fill_color=C_IS, fill_opacity=0.85).move_to([-3.4, Y0 + 2.7 * U + 2.3 * U / 2, 0])
        base_ln = Line([-6.3, Y0, 0], [-2.2, Y0, 0], color=GRAYTXT, stroke_width=3)
        l1 = MathTex(r"N_f I_{f1}", font_size=32, color=C_IF).next_to(b1, UP, buff=0.12)
        l1s = Text("ชันท์ ขณะทำงาน\nแบบขนาน", font_size=16, color=GRAYTXT, line_spacing=0.9).next_to(b1, DOWN, buff=0.3)
        l2 = MathTex(r"N_f I_{f2}", font_size=32, color=WHITE).move_to([-3.4, Y0 + 5.0 * U + 0.32, 0])
        l2s = Text("ที่ต้องการ\nที่พิกัดโหลด", font_size=16, color=GRAYTXT, line_spacing=0.9).next_to(b2a, DOWN, buff=0.3)
        brc = Brace(b2b, RIGHT, buff=0.1, color=C_IS)
        l3 = MathTex(r"N_s I_s", font_size=32, color=C_IS).next_to(brc, RIGHT, buff=0.1)
        outline = Rectangle(width=1.0, height=5.0 * U, stroke_color=WHITE, stroke_width=3).move_to([-3.4, Y0 + 5.0 * U / 2, 0])
        self.play(Create(base_ln), FadeIn(b1), FadeIn(l1), FadeIn(l1s), run_time=1.0)
        self.play(FadeIn(b2a), Create(outline), FadeIn(l2), FadeIn(l2s), run_time=1.0)
        self.play(FadeIn(b2b, shift=DOWN * 0.3), Create(brc), FadeIn(l3), run_time=1.1)
        self.wait(0.6)

        eq = MathTex(r"N_f", r"(", r"I_{f2}", r"-", r"I_{f1}", r")", r"=", r"N_s", r"I_s", font_size=46)
        for i in (0, 2, 4):
            eq[i].set_color(C_IF)
        eq[7].set_color(C_IS)
        eq[8].set_color(C_IS)
        t86 = Text("(8-6)", font_size=20, color=GRAYTXT)
        eqg = VGroup(eq, t86).arrange(RIGHT, buff=0.35).move_to([2.6, 1.7, 0])
        self.say("เขียนเป็นสมการ 8-6: แอมแปร์-เทอร์นที่เพิ่ม (ซ้าย) = แอมแปร์-เทอร์นที่เซรี่ฟิลด์ให้ (ขวา)", color=OK)
        self.play(Write(eq), FadeIn(t86), run_time=1.4)
        self.glow(eq[7:], VGroup(b2b, l3), color=C_IS)
        defs = VGroup(lab(r"N_f", "จำนวนรอบของชันท์ฟิลด์", WHITE, 21, C_IF), lab(r"I_{f1}", "กระแสชันท์ที่พิกัดโหลด (ทำงานแบบขนาน)", WHITE, 21, C_IF),
                      lab(r"I_{f2}", "กระแสฟิลด์ที่ต้องใช้ให้ได้ Vt ตามต้องการ", WHITE, 21, C_IF), lab(r"N_s", "จำนวนรอบของเซรี่ฟิลด์", WHITE, 21, C_IS),
                      lab(r"I_s", "กระแสในเซรี่ฟิลด์ที่พิกัดโหลด", WHITE, 21, C_IS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        defs = fit_width(defs, 7.0).move_to([3.3, -0.55, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.15) for d in defs], lag_ratio=0.35), run_time=2.2)
        note = fit_width(Text("หมายเหตุ: PDF เรียก If2 ว่า \"ค่าเพิ่มขึ้นของกระแสชันท์\" แต่ ตย.8-7 ใช้ If2 = 5 A\nเป็นกระแสฟิลด์ที่ต้องใช้ทั้งหมด (ส่วนเพิ่ม = If2 − If1)",
                              font_size=17, color=GRAYTXT, line_spacing=0.9), 12.2).move_to([0.2, -3.4, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.0)
        self.exam("สมการ 8-6: เซรี่ฟิลด์ต้องเติมแอมแปร์-เทอร์นเท่าไร",
                  "Nf (If2 − If1) = Ns Is · ซ้าย = แอมแปร์-เทอร์นที่ต้องเพิ่ม · ขวา = ที่เซรี่ฟิลด์ให้ → หา Is")


# =============================================================== P26  หน้า 26
class P26_Ex87Diverter(Lesson):
    """ตย.8-7: Is = 115 A, Id = 35 A, Rd = 0.0164 ohm (ไดเวอร์เตอร์ขนานเซรี่ฟิลด์)"""

    def construct(self):
        self.head("ตัวอย่าง 8-7 หาความต้านทานไดเวอร์เตอร์", "หน้า 26 · ตย.8-7, สมการ 8-6")
        XA, XB, YS, YD, YM = -5.6, -2.1, 1.35, -0.4, 0.475
        ser = coil_sym([-4.95, YS], [-2.75, YS], n=4, r=0.1, color=C_IS)
        div = res_zig([-4.95, YD], [-2.75, YD], n=4, color=YEL)
        cir = VGroup(wire((-6.6, YM), (XA, YM)), wire((XB, YM), (-1.0, YM)), wire((XA, YS), (XA, YD)), wire((XB, YS), (XB, YD)),
                     ser, wire((XA, YS), (-4.95, YS)), wire((-2.75, YS), (XB, YS)),
                     div, wire((XA, YD), (-4.95, YD)), wire((-2.75, YD), (XB, YD)))
        t_ser = Text("เซรี่ฟิลด์ Rs = 0.005 Ω", font_size=17, color=C_IS).move_to([-3.85, YS + 0.5, 0])
        t_div = Text("ไดเวอร์เตอร์ Rd = ?", font_size=17, color=YEL).move_to([-3.85, YD - 0.45, 0])
        a_in = Arrow([-6.6, YM + 0.35, 0], [-5.9, YM + 0.35, 0], buff=0, color=C_IL, stroke_width=4, tip_length=0.16)
        t_in = Text("150 A", font_size=18, color=C_IL).next_to(a_in, UP, buff=0.05)
        a_s = Arrow([-4.8, 0.88, 0], [-3.3, 0.88, 0], buff=0, color=C_IS, stroke_width=4, tip_length=0.16)
        t_is = _lv(r"I_s", C_IS, 26).next_to(a_s, RIGHT, buff=0.1)
        a_d = Arrow([-4.8, 0.08, 0], [-4.1, 0.08, 0], buff=0, color=YEL, stroke_width=4, tip_length=0.16)
        t_id = _lv(r"I_d", YEL, 26).next_to(a_d, RIGHT, buff=0.1)
        given = card([("โจทย์ให้", OK), "ชันท์ Nf = 500 รอบ/ขั้ว · เซรี่ Ns = 10 รอบ/ขั้ว", "If1 = 2.7 A · ต้องการ If2 = 5 A", "กระแสพิกัด 150 A · Rs = 0.005 Ω"], w=5.5, color=OK, size=19)
        given = fit_width(given, 5.6).move_to([-3.7, -2.15, 0])
        self.say("ตย.8-7: เครื่องกำเนิดขนาน 250 kW 250 V 4 ขั้ว → หา Rd ของไดเวอร์เตอร์ (cumulative)", color=OK)
        self.play(Create(cir), FadeIn(t_ser), FadeIn(t_div), FadeIn(a_in), FadeIn(t_in), run_time=1.4)
        self.play(FadeIn(given, shift=UP * 0.2), run_time=0.9)
        self.wait(0.6)

        bd = Board(self, x=0.0, y=2.1, gap=0.14)
        self.say("ขั้นที่ 1: สมการ 8-6 หากระแสเซรี่ฟิลด์ที่ต้องการ", color=C_IS)
        bd.add(1, "สมการ 8-6 หา Is", VGroup(MathTex(r"N_f(I_{f2}-I_{f1})=N_sI_s", font_size=28),
                                           MathTex(r"500(5-2.7)=10\,I_s\ \Rightarrow\ I_s=115\,\mathrm{A}", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
               color=C_IS, hold=0.2)
        self.play(Create(a_s), FadeIn(t_is), Indicate(ser, color=C_IS), run_time=1.0)
        self.say("ขั้นที่ 2: กระแสพิกัด 150 A ที่เหลือ ต้องเบี่ยงผ่านไดเวอร์เตอร์", color=YEL)
        bd.add(2, "กระแสไดเวอร์เตอร์", MathTex(r"I_d=150-115=35\,\mathrm{A}", font_size=28), color=YEL, hold=0.2)
        self.play(Create(a_d), FadeIn(t_id), Indicate(div, color=YEL), run_time=1.0)
        self.say("ขั้นที่ 3: ไดเวอร์เตอร์ขนานกับเซรี่ → แรงดันตกคร่อมเท่ากัน  Id·Rd = Is·Rs", color=OK)
        bd.add(3, "ขนาน แรงดันตกเท่ากัน", MathTex(r"R_d=\frac{I_sR_s}{I_d}=\frac{115\times0.005}{35}=0.0164\,\Omega", font_size=28), color=OK, hold=0.2)
        res = VGroup(Text("ไดเวอร์เตอร์", font_size=17, color=YEL), MathTex(r"R_d=0.0164\,\Omega", font_size=24, color=OK)).arrange(RIGHT, buff=0.15).move_to(t_div.get_center())
        self.play(FadeOut(t_div, shift=DOWN * 0.1), FadeIn(res, shift=DOWN * 0.1), run_time=0.8)
        self.say("ตรวจ: แรงดันคร่อมเซรี่ฟิลด์ = คร่อมไดเวอร์เตอร์", color=C_IL)
        bd.add(4, "ตรวจ", MathTex(r"115\times0.005=0.575\ \mathrm{V}\ ;\ 35\times0.0164=0.574\ \mathrm{V}\ \checkmark", font_size=26), color=C_IL, hold=0.3)
        note = fit_width(Text("หมายเหตุ: PDF พิมพ์ (115 A)(0.005 A) — หน่วยของ 0.005 ต้องเป็น Ω (ความต้านทานเซรี่ฟิลด์)", font_size=16, color=GRAYTXT), 12.2).move_to([0.2, -3.55, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.8)
        self.exam("ตัวอย่าง 8-7: หาความต้านทานไดเวอร์เตอร์ (Is, Id, Rd)",
                  "Is = 500(5−2.7)/10 = 115 A · Id = 150 − 115 = 35 A · Rd = Is·Rs/Id = 115×0.005/35 = 0.0164 Ω")
