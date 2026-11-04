"""EPS8 หน้า 12-15 (8-7 จบ, 8-8, 8-9, 8-10 เริ่ม) — ดู eps8_lib.py"""
from eps8_lib import *
from eps8_a import chips


def _lv(txt, color=C_E, size=24):
    return MathTex(txt, font_size=size, color=color)


def ext_curves(ax):
    """เส้นลักษณะสมบัติภายนอก (รูป 8-7): คืน dict ของ VMobject และฟังก์ชันค่า Vt ที่ IL=1 (กระแสพิกัด)
    แกน x = IL/Irated (0..1.55), แกน y = Vt/Vnl (0..1.1)"""
    def pts(lst):
        m = VMobject()
        m.set_points_smoothly([ax.c2p(x, y) for x, y in lst])
        return m
    ideal = DashedLine(ax.c2p(0, 1.0), ax.c2p(1.45, 1.0), color=GRAYTXT, stroke_width=2, dash_length=0.1)
    c1 = pts([(0, 1.0), (0.4, 0.985), (0.8, 0.95), (1.0, 0.925), (1.3, 0.87), (1.45, 0.84)])
    c2 = pts([(0, 1.0), (0.4, 0.935), (0.8, 0.86), (1.0, 0.815), (1.3, 0.73), (1.45, 0.68)])
    c3 = pts([(0, 1.0), (0.4, 0.89), (0.8, 0.76), (1.0, 0.685), (1.2, 0.58), (1.36, 0.42), (1.4, 0.33), (1.36, 0.22),
              (1.22, 0.10), (1.05, 0.03), (0.92, 0.0)])
    lv = {"nl": 1.0, "ar": 0.925, "ra": 0.815, "fl": 0.685}
    return dict(ideal=ideal, c1=c1, c2=c2, c3=c3), lv


# =============================================================== P12  หน้า 12
class P12_HighRAndLoad(Lesson):
    """8-7 สาเหตุที่ 3: R ฟิลด์สูงเกิน Rc (วงจรขาด / คอมมิวเตเตอร์สกปรก) + 8-8 เริ่ม: โหลดขนาน แรงดันขั้วลด"""

    def construct(self):
        self.head("8-7 สาเหตุที่ 3 · 8-8 โหลดทำให้แรงดันขั้วลด", "หน้า 12 · 8-7, 8-8")
        YT, YB = 1.2, -1.2
        arm = arm_sym([-5.6, 0.0], r=0.42)
        coil = coil_sym([-4.4, YT], [-2.6, YT], n=4, r=0.1, color=C_IF)
        rh = res_zig([-2.6, YT], [-1.3, YT], n=4)
        w_top = wire((-5.6, 0.42), (-5.6, YT), (-4.4, YT))
        w_r = wire((-1.3, YT), (-0.8, YT), (-0.8, 0.3))
        w_mid = wire((-0.8, 0.3), (-0.8, -0.3))
        w_r2 = wire((-0.8, -0.3), (-0.8, YB), (-5.6, YB), (-5.6, -0.42))
        t_f = tag("ขดลวดฟิลด์", size=18, color=C_IF).move_to([-3.5, YT + 0.45, 0])
        t_r = tag("รีโอสตาท", size=18, color=C_R).move_to([-1.95, YT + 0.45, 0])
        t_a = tag("อาร์เมเจอร์", size=18, color=C_E)
        t_a.move_to([-5.6 - 0.16 - t_a.width / 2, -0.95, 0])     # อยู่ซ้ายสายต่อออกจากอาร์เมเจอร์ (เดิมสายพาดกลางตัวอักษร)
        circ = VGroup(arm, coil, rh, w_top, w_r, w_r2, t_f, t_r, t_a)
        # แถบ R รวมของฟิลด์
        X0, X1, BY = 1.3, 6.6, 0.4
        track = Rectangle(width=X1 - X0, height=0.5, stroke_color=GRAYTXT, stroke_width=2).move_to([(X0 + X1) / 2, BY, 0])
        s1 = Rectangle(width=1.3, height=0.5, stroke_width=0, fill_color=C_IF, fill_opacity=0.8).move_to([X0 + 0.65, BY, 0])
        s2 = Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=C_R, fill_opacity=0.8).move_to([X0 + 1.3 + 0.7, BY, 0])
        rc_x = X0 + 3.6
        rc = DashedLine([rc_x, BY - 0.55, 0], [rc_x, BY + 0.75, 0], color=YEL, stroke_width=3)
        rc_t = Text("Rc ความต้านทานวิกฤต", font_size=18, color=YEL).move_to([rc_x, BY + 1.0, 0])
        b_t = Text("R ของวงจรฟิลด์ (ขดลวด + รีโอสตาท + หน้าสัมผัส)", font_size=18, color=GRAYTXT).move_to([(X0 + X1) / 2, BY - 0.85, 0])
        lg = VGroup(Text("ขดลวด", font_size=16, color=C_IF).move_to([X0 + 0.65, BY - 0.0, 0]),
                    Text("รีโอสตาท", font_size=16, color=WHITE).move_to([X0 + 1.3 + 0.7, BY - 0.0, 0]))
        self.say("8-7 สาเหตุที่ 3: R ของวงจรฟิลด์มากกว่า Rc → ไม่สร้างแรงเคลื่อน")
        self.play(Create(circ), Create(w_mid), run_time=1.2)
        self.play(Create(track), FadeIn(s1), FadeIn(s2), FadeIn(lg), Create(rc), FadeIn(rc_t), FadeIn(b_t), run_time=1.4)
        self.wait(0.6)

        self.say("(ก) วงจรฟิลด์ขาด: เกิดวงจรเปิด → R = ∞ มากกว่า Rc แน่นอน", color=WARN)
        gap = VGroup(Line([-0.8, 0.3, 0], [-0.8, 0.12, 0], color=GRAYTXT, stroke_width=3),
                     Line([-0.8, -0.12, 0], [-0.8, -0.3, 0], color=GRAYTXT, stroke_width=3))
        spark = Line([-0.95, 0.1, 0], [-0.65, -0.1, 0], color=YEL, stroke_width=4)
        t_op = tag("ต่อขาด (วงจรเปิด)", size=18, color=WARN)
        t_op.move_to([-0.8 + 0.2 + t_op.width / 2, -0.75, 0])    # อยู่ขวาสายด้านล่าง (เดิมสายพาดผ่านตัวอักษร)
        inf = MathTex(r"R=\infty", font_size=34, color=WARN).move_to([X1 - 0.6, BY + 0.0, 0])
        self.play(FadeOut(w_mid), FadeIn(gap), FadeIn(spark), FadeIn(t_op), run_time=0.8)
        self.play(s2.animate.stretch_to_fit_width(X1 - X0 - 1.3 - 0.05, about_edge=LEFT).shift(RIGHT * 0.0),
                  FadeIn(inf), run_time=1.2)
        self.play(Indicate(inf, color=WHITE), run_time=0.7)
        self.wait(0.8)

        self.say("(ข) คอมมิวเตเตอร์สกปรก: หน้าสัมผัสแปรง-คอมมิวเตเตอร์แย่ → R เพิ่ม", color=WARN)
        self.play(FadeOut(gap), FadeOut(spark), FadeOut(t_op), FadeOut(inf), FadeIn(w_mid), run_time=0.5)
        s2n = Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=C_R, fill_opacity=0.8).move_to([X0 + 1.3 + 0.7, BY, 0])
        self.play(Transform(s2, s2n), run_time=0.4)
        dirt = VGroup(*[Dot([-5.6 + dx, 0.42 + dy, 0], radius=0.05, color="#8D6E63") for dx, dy in
                        ((-0.18, 0.12), (0.0, 0.2), (0.18, 0.1), (0.1, 0.28), (-0.1, 0.3))])
        dirt2 = dirt.copy().shift(DOWN * 0.84)
        t_d = tag("คอมมิวเตเตอร์สกปรก", size=18, color="#BCAAA4").move_to([-5.6, -1.65, 0])
        s3 = Rectangle(width=0.05, height=0.5, stroke_width=0, fill_color="#BCAAA4", fill_opacity=0.9).move_to([X0 + 2.7 + 0.025, BY, 0])
        t_cr = Text("R หน้าสัมผัส", font_size=16, color="#1c2a30").move_to([X0 + 4.4, BY - 0.0, 0])
        self.play(FadeIn(dirt), FadeIn(dirt2), FadeIn(t_d), FadeIn(s3), run_time=0.8)
        s3_big = Rectangle(width=2.4, height=0.5, stroke_width=0, fill_color="#BCAAA4", fill_opacity=0.9).move_to(
            [X0 + 2.7 + 1.2, BY, 0])
        self.play(Transform(s3, s3_big), run_time=1.6)
        warn = Text("R รวม > Rc → ไม่สร้างแรงเคลื่อน", font_size=22, color=WARN).move_to([3.9, -1.55, 0])
        self.play(track.animate.set_stroke(color=WARN, width=4), FadeIn(warn), FadeIn(t_cr), run_time=0.8)
        self.wait(1.6)

        # ---------------- 8-8
        self.say("8-8: โหลดต่อขนานกับขั้ว → เพิ่มโหลด กระแสเพิ่ม แรงดันที่ขั้วลดลง", color=C_IL)
        self.play(FadeOut(VGroup(circ, w_mid, track, s1, s2, s3, lg, rc, rc_t, b_t, dirt, dirt2, t_d, warn, t_cr)),
                  run_time=0.7)
        gen = arm_sym([-5.4, 0.0], r=0.5, letter="G")
        rt, rb = 1.4, -1.4
        w1 = wire((-5.4, 0.5), (-5.4, rt), (3.3, rt))
        w2 = wire((-5.4, -0.5), (-5.4, rb), (3.3, rb))
        loads = VGroup()
        sws = []
        for i, xx in enumerate((-2.6, -0.9, 0.8)):
            lamp = VGroup(Circle(radius=0.3, stroke_color=YEL, stroke_width=3, fill_color=YEL, fill_opacity=0.12),
                          Line([-0.2, -0.2, 0], [0.2, 0.2, 0], color=YEL, stroke_width=2),
                          Line([-0.2, 0.2, 0], [0.2, -0.2, 0], color=YEL, stroke_width=2)).move_to([xx, 0.0, 0])
            va, vb = wire((xx, rt), (xx, 0.3), color=GRAYTXT), wire((xx, -0.3), (xx, rb), color=GRAYTXT)
            loads.add(VGroup(lamp, va, vb))
        gen_t = tag("เครื่องกำเนิด", size=18, color=C_E)
        gen_t.move_to([-5.4 - 0.16 - gen_t.width / 2, -0.95, 0])  # ซ้ายสายลงล่าง ไม่ให้สายพาดทับตัวอักษร
        t_par = tag("โหลดต่อขนานกับขั้ว", size=19, color=GRAYTXT).move_to([-0.9, rt + 0.4, 0])
        # มาตรวัด: IL (ฟ้าเขียว) เพิ่ม / Vt ลด
        bi = Rectangle(width=0.5, height=2.4, stroke_color=GRAYTXT, stroke_width=2).move_to([4.5, 0.0, 0])
        bv = Rectangle(width=0.5, height=2.4, stroke_color=GRAYTXT, stroke_width=2).move_to([6.0, 0.0, 0])
        fi = Rectangle(width=0.5, height=0.5, stroke_width=0, fill_color=C_IL, fill_opacity=0.85).move_to(bi.get_bottom() + UP * 0.25)
        fv = Rectangle(width=0.5, height=2.2, stroke_width=0, fill_color=C_E, fill_opacity=0.85).move_to(bv.get_bottom() + UP * 1.1)
        li = _lv(r"I_L", C_IL, 26).next_to(bi, DOWN, buff=0.15)
        lvt = _lv(r"V_t", C_E, 26).next_to(bv, DOWN, buff=0.15)
        self.play(Create(VGroup(gen, w1, w2)), FadeIn(gen_t), FadeIn(t_par), Create(bi), Create(bv), FadeIn(fi), FadeIn(fv),
                  FadeIn(li), FadeIn(lvt), FadeIn(loads[0]), run_time=1.4)
        for k, (hi_i, hi_v) in enumerate(((1.1, 1.95), (1.8, 1.7))):
            self.play(FadeIn(loads[k + 1]), fi.animate.stretch_to_fit_height(hi_i, about_edge=DOWN),
                      fv.animate.stretch_to_fit_height(hi_v, about_edge=DOWN), run_time=1.2)
            self.wait(0.3)
        self.wait(0.6)

        self.say("แรงดันขั้วลดเพราะ 3 สาเหตุพร้อมกัน", color=WARN)
        self.play(FadeOut(VGroup(gen, w1, w2, gen_t, t_par, bi, bv, fi, fv, li, lvt, loads)), run_time=0.6)
        cards = VGroup(
            card([("① ความต้านทานในวงจรอาร์เมเจอร์", C_IA), "กระแสไหลผ่าน Ra → แรงดันตกคร่อม"], color=C_IA, w=8.0),
            card([("② อาร์เมเจอร์รีแอคชัน", C_PHI), "ฟลักซ์จากอาร์เมเจอร์ลดฟลักซ์ขั้ว → E ลด"], color=C_PHI, w=8.0),
            card([("③ กระแสฟิลด์ลดลง", C_IF), "ฟิลด์ต่อคร่อมขั้ว → Vt ลด → If ลด → ฟลักซ์ลด → E ลด"], color=C_IF, w=8.0)
        ).arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.5), run_time=2.4)
        self.wait(2.2)
        self.exam("จุดออกสอบ 8-8: แรงดันขั้วเครื่องกำเนิดแบบขนานลดลงเมื่อเพิ่มโหลดเพราะอะไรบ้าง",
                  "(1) แรงดันตกที่ Ra (2) อาร์เมเจอร์รีแอคชันทำให้ฟลักซ์ลด (3) Vt ลด → If ลด → ฟลักซ์ลด → E ลดอีก")


# =============================================================== P13  หน้า 13
class P13_VtEq_ExtChar(Lesson):
    """Vt = E - Ia Ra (8-3); อาร์เมเจอร์รีแอคชัน; กระแสฟิลด์ลด; 8-9 รูป 8-7 สร้างเส้นลักษณะสมบัติภายนอกทีละสาเหตุ"""

    def construct(self):
        self.head("สมการ 8-3 และลักษณะสมบัติภายนอก (รูป 8-7)", "หน้า 13 · 8-3 (สมการ), 8-9")
        # ---- วงจรสมมูล
        ex, ey = -3.8, 0.2
        src = meter([ex, ey], "E", color=C_E, r=0.4)
        ra = res_zig([ex, ey + 0.4], [ex, ey + 1.7], n=4)
        w_a = wire((ex, ey + 1.7), (ex + 0.0, ey + 1.7))
        ra_v = res_zig([ex, ey + 0.4], [ex, ey + 1.7], n=4, color=C_IA)
        ra_v.rotate(0)  # ตัวต้านทานแนวตั้ง
        top = wire((ex, ey + 1.7), (ex + 2.2, ey + 1.7))
        bot = wire((ex, ey - 0.4), (ex, ey - 1.5), (ex + 2.2, ey - 1.5))
        vt = Arrow([ex + 2.2, ey - 1.5, 0], [ex + 2.2, ey + 1.7, 0], buff=0, color=C_E, stroke_width=3, tip_length=0.2)
        t_vt = _lv(r"V_t", C_E, 30).next_to(vt, RIGHT, buff=0.12)
        t_ra = _lv(r"R_a", C_IA, 28).next_to(ra_v, LEFT, buff=0.15)
        t_e = _lv(r"E", C_E, 28).next_to(src, LEFT, buff=0.15)
        ia = Arrow([ex - 0.65, ey + 0.9, 0], [ex - 0.65, ey + 1.5, 0], buff=0, color=C_IA, stroke_width=4, tip_length=0.16)
        t_ia = _lv(r"I_a", C_IA, 26).next_to(ia, LEFT, buff=0.08)
        self.say("สมการ 8-3: แรงดันที่ขั้ว = แรงเคลื่อน ลบ แรงดันตกที่ความต้านทานอาร์เมเจอร์")
        self.play(Create(VGroup(src, ra_v, top, bot, vt)), FadeIn(t_vt), FadeIn(t_ra), FadeIn(t_e), run_time=1.4)
        eq = MathTex(r"V_t", r"=", r"E", r"-", r"I_a R_a", font_size=54).move_to([2.8, 1.4, 0])
        eq[0].set_color(C_E), eq[2].set_color(C_E), eq[4].set_color(C_IA)
        self.play(Write(eq), FadeIn(ia), FadeIn(t_ia), run_time=1.3)
        self.glow(eq[4], ra_v, color=C_IA)
        self.glow(eq[2], src, color=C_E)
        defs = VGroup(*[VGroup(_lv(a, c, 24), Text(b, font_size=18, color=GRAYTXT)).arrange(RIGHT, buff=0.2)
                        for a, b, c in ((r"V_t", "แรงดันที่ขั้วเครื่องกำเนิด", C_E), (r"E", "แรงเคลื่อนเหนี่ยวนำ", C_E),
                                        (r"I_a", "กระแสอาร์เมเจอร์ทั้งหมด", C_IA), (r"R_a", "ความต้านทานวงจรอาร์เมเจอร์", C_IA))]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, -0.6, 0])
        self.play(FadeIn(defs, shift=UP * 0.2), run_time=1.0)
        self.wait(1.2)

        # ---- อาร์เมเจอร์รีแอคชัน
        self.say("อาร์เมเจอร์รีแอคชัน: ฟลักซ์จากตัวนำอาร์เมเจอร์ไปลดฟลักซ์ขั้ว → E และ Vt ลด", color=C_PHI)
        self.play(FadeOut(VGroup(src, ra_v, top, bot, vt, t_vt, t_ra, t_e, ia, t_ia, eq, defs)), run_time=0.6)
        m = machine(0.8).move_to([-3.2, 0.2, 0])
        lv = ValueTracker(0.9)
        m.flux.add_updater(lambda f: flux_set(f, lv.get_value()))
        flux_set(m.flux, 0.9)
        self.play(FadeIn(m), run_time=0.7)
        ar = Arrow([-3.2, -0.9, 0], [-3.2, 0.9, 0], buff=0, color=TORQUE, stroke_width=7, tip_length=0.25)
        t_ar = Text("ฟลักซ์จากอาร์เมเจอร์", font_size=18, color=TORQUE).move_to([-3.2, -1.65, 0])
        self.play(Create(ar), FadeIn(t_ar), lv.animate.set_value(0.55), run_time=1.6)
        chain = chips([(r"\phi", "ฟลักซ์ขั้ว ↓", C_PHI), (r"E", "แรงเคลื่อน ↓", C_E), (r"V_t", "แรงดันขั้ว ↓", C_E)])
        chain.move_to([3.2, 0.6, 0])
        self.play(FadeIn(chain), run_time=0.8)
        self.play(*[Indicate(c, color=col) for c, col in zip(chain.cs, (C_PHI, C_E, C_E))], run_time=1.2)
        self.wait(0.6)

        # ---- กระแสฟิลด์ลด
        self.say("กระแสฟิลด์ลด: ฟิลด์ต่อคร่อมขั้ว → Vt ลด → If ลด → ฟลักซ์ลด → E ลดอีก", color=C_IF)
        chain2 = chips([(r"V_t", "แรงดันขั้ว ↓", C_E), (r"I_f", "กระแสฟิลด์ ↓", C_IF), (r"\phi", "ฟลักซ์ ↓", C_PHI)])
        chain2.move_to([3.2, -1.1, 0])
        self.play(FadeIn(chain2), run_time=0.8)
        self.play(*[Indicate(c, color=col) for c, col in zip(chain2.cs, (C_E, C_IF, C_PHI))], run_time=1.2)
        self.wait(0.8)

        # ---- 8-9 รูป 8-7
        self.say("8-9 รูป 8-7: เริ่มจาก Vt ขณะไม่มีโหลด แล้วหักแรงดันที่ลดลงทีละสาเหตุ", color=C_IL)
        lv.set_value(0.55)
        m.flux.clear_updaters()
        self.play(FadeOut(VGroup(m, ar, t_ar, chain, chain2)), run_time=0.7)
        g = make_axes(pos=[-5.4, -2.6], x_len=8.4, y_len=4.2, xmax=1.55, ymax=1.1, xl=r"I_L", yl=r"V_t")
        ax = g.ax
        cv, levels = ext_curves(ax)
        c_nl = Text("แรงดันขั้วขณะไม่มีโหลด", font_size=18, color=GRAYTXT).next_to(ax.c2p(0, 1.0), RIGHT, buff=0.0).shift(UP * 0.35 + RIGHT * 0.1)
        rated = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 1.05), color=GRAYTXT, stroke_width=2, dash_length=0.1)
        t_rated = Text("กระแสพิกัด", font_size=18, color=GRAYTXT).next_to(ax.c2p(1.0, 0), DOWN, buff=0.45)
        self.play(Create(g), Create(cv["ideal"]), FadeIn(c_nl), Create(rated), FadeIn(t_rated), run_time=1.4)
        self.say("① อาร์เมเจอร์รีแอคชัน: เส้นโค้งลงเล็กน้อย", color=C_PHI)
        self.play(Create(cv["c1"].set_color(C_PHI).set_stroke(width=4)), run_time=1.2)
        self.say("② ความต้านทานอาร์เมเจอร์ Ra: แรงดันตกเพิ่ม (IaRa)", color=C_IA)
        self.play(Create(cv["c2"].set_color(C_IA).set_stroke(width=4)), run_time=1.2)
        self.say("③ กระแสฟิลด์ลดลง: เส้นจริงตกลงเร็วขึ้นอีก", color=C_IF)
        self.play(Create(cv["c3"].set_color(C_IF).set_stroke(width=5)), run_time=2.0)
        # ลูกศรขนาด 3 สาเหตุที่กระแสพิกัด
        brs = VGroup()
        for lo, hi, col in ((levels["ar"], levels["nl"], C_PHI), (levels["ra"], levels["ar"], C_IA), (levels["fl"], levels["ra"], C_IF)):
            brs.add(DoubleArrow(ax.c2p(1.03, hi), ax.c2p(1.03, lo), buff=0, color=col, stroke_width=3, tip_length=0.12))
        tx = VGroup(*[VGroup(Rectangle(width=0.26, height=0.26, stroke_width=0, fill_color=col, fill_opacity=1),
                             Text(t, font_size=18, color=col)).arrange(RIGHT, buff=0.15)
                      for t, col in (("ลดเพราะอาร์เมเจอร์รีแอคชัน", C_PHI), ("ลดเพราะความต้านทานอาร์เมเจอร์", C_IA),
                                     ("ลดเพราะกระแสฟิลด์ลดลง", C_IF))]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.75, 0.9, 0])
        self.play(*[Create(b) for b in brs], FadeIn(tx), run_time=1.4)
        self.wait(2.0)
        self.exam("จุดออกสอบ 8-9: เส้นลักษณะสมบัติภายนอก Vt–IL ของเครื่องแบบขนานมีกี่ส่วนที่ทำให้ Vt ลด",
                  "3 ส่วน: อาร์เมเจอร์รีแอคชัน · IaRa ของอาร์เมเจอร์ · กระแสฟิลด์ลดลง (Vt = E − IaRa)")


# =============================================================== P14  หน้า 14
class P14_BreakdownVR(Lesson):
    """รูป 8-7: จุดเบรกดาวน์ (โหลดเพิ่มต่อเนื่องจน Vt -> 0) + 8-10 VR = (VNL-VFL)/VFL x100 + ตย.8-3 (230 -> 250 V)"""

    def construct(self):
        self.head("จุดเบรกดาวน์ + 8-10 โวลท์เตจเรกูเลชั่น", "หน้า 14 · 8-9, 8-10")
        g = make_axes(pos=[-6.4, -2.4], x_len=6.4, y_len=4.0, xmax=1.55, ymax=1.1, xl=r"I_L", yl=r"V_t")
        ax = g.ax
        cv, levels = ext_curves(ax)
        c3 = cv["c3"].set_color(C_IF).set_stroke(width=5)
        self.say("รูป 8-7: เพิ่มโหลดต่อเนื่อง → Vt ลดเรื่อยๆ จนถึงจุดเบรกดาวน์")
        self.play(Create(g), run_time=0.8)
        d = Dot(ax.c2p(0, 1.0), radius=0.1, color=WHITE)
        self.add(d)
        self.play(Create(c3), MoveAlongPath(d, c3), run_time=5.0, rate_func=linear)
        bd = Dot(ax.c2p(1.4, 0.33), radius=0.13, color=WARN)
        t_bd = Text("จุดเบรกดาวน์", font_size=20, color=WARN).next_to(bd, RIGHT, buff=0.15)
        self.play(FadeOut(d), FadeIn(bd, scale=2.0), FadeIn(t_bd), run_time=0.8)
        self.say("เลยจุดนี้ ถ้าเพิ่มโหลดต่อ Vt จะลดลงเป็นศูนย์อย่างรวดเร็ว (E ไม่ถูกสร้างขึ้นอีก)", color=WARN)
        self.wait(2.4)

        # ---- VR
        self.say("8-10 โวลท์เตจเรกูเลชั่น: แรงดันขั้วเปลี่ยนไปเท่าไรจากไม่มีโหลดถึงเต็มพิกัด", color=OK)
        self.play(FadeOut(bd), FadeOut(t_bd), run_time=0.4)
        rated = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 1.0), color=GRAYTXT, stroke_width=2, dash_length=0.1)
        p_nl = Dot(ax.c2p(0, 1.0), radius=0.1, color=C_E)
        p_fl = Dot(ax.c2p(1.0, levels["fl"]), radius=0.1, color=C_E)
        l_nl = _lv(r"V_{NL}", C_E, 26).next_to(p_nl, RIGHT, buff=0.15).shift(UP * 0.2)
        l_fl = _lv(r"V_{FL}", C_E, 26).next_to(p_fl, DOWN, buff=0.18).shift(RIGHT * 0.2)
        t_ratd = Text("กระแสเต็มพิกัด", font_size=18, color=GRAYTXT).next_to(ax.c2p(1.0, 0), DOWN, buff=0.4)
        gap = DoubleArrow(ax.c2p(0.12, 1.0), ax.c2p(0.12, levels["fl"]), buff=0, color=WARN, stroke_width=3, tip_length=0.12)
        self.play(Create(rated), FadeIn(p_nl), FadeIn(p_fl), FadeIn(l_nl), FadeIn(l_fl), FadeIn(t_ratd), Create(gap), run_time=1.6)
        eq = MathTex(r"VR\,(\%)", r"=", r"\frac{V_{NL}-V_{FL}}{V_{FL}}", r"\times 100", font_size=38).move_to([4.2, 1.6, 0])
        self.play(Write(eq), run_time=1.4)
        self.glow(eq[2], VGroup(p_nl, p_fl, gap), color=WARN)
        t_def = VGroup(VGroup(_lv(r"V_{NL}", C_E, 22), Text("แรงดันขั้ว ขณะไม่มีโหลด", font_size=17, color=GRAYTXT)).arrange(RIGHT, buff=0.2),
                       VGroup(_lv(r"V_{FL}", C_E, 22), Text("แรงดันขั้ว ขณะมีโหลดเต็มที่", font_size=17, color=GRAYTXT)).arrange(RIGHT, buff=0.2)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 0.6, 0])
        self.play(FadeIn(t_def), run_time=0.8)
        self.wait(0.8)

        # ---- ตัวอย่าง 8-3
        self.say("ตัวอย่าง 8-3: เครื่องกำเนิดแบบขนาน 10 kW 230 V เต็มพิกัด ปลดโหลด Vt เพิ่มเป็น 250 V", color=OK)
        bd2 = Board(self, x=1.2, y=0.05, gap=0.06)
        bd2.add(1, "โจทย์ให้", VGroup(n_text("เต็มพิกัด: V_FL = 230 V", size=19), n_text("ปลดโหลด: V_NL = 250 V", size=19)
                                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), color=OK, hold=0.1)
        # หน้า 14 ของ PDF มีแค่โจทย์ — เฉลยทีละขั้นอยู่คลิปหน้า 15 (กระดานเดิมยาวล้นขอบล่างและซ้ำกับ P15)
        res = VGroup(MathTex(r"VR=\,?\,\%", font_size=32, color=OK), n_text("(เฉลยทีละขั้นต่อหน้า 15)", size=17, color=GRAYTXT)
                     ).arrange(RIGHT, buff=0.3)
        bd2.add(2, "ให้หา", res, color=OK, hold=0.2)
        self.wait(1.6)
        self.exam("จุดออกสอบ 8-3: เครื่องกำเนิดขนาน 230 V เต็มพิกัด ปลดโหลดแรงดันเป็น 250 V หา VR",
                  "VR = (V_NL − V_FL)/V_FL × 100 = (250 − 230)/230 × 100 = 8.7 %")
