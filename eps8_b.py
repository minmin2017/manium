"""EPS8 หน้า 7-12 (8-4 .. 8-7: เส้นความต้านทานฟิลด์, การสร้างแรงเคลื่อน, ความต้านทานวิกฤต) — ดู eps8_lib.py"""
from eps8_lib import *
from eps8_a import chips


# =============================================================== P07  หน้า 7
class P07_FieldLine(Lesson):
    """รูป 8-3: วงจรฟิลด์ (รีโอสตาท+ขดลวด) และเส้นความต้านทานฟิลด์ V = If x R (สโลป = R)"""

    def construct(self):
        self.head("รูป 8-3 เส้นความต้านทานฟิลด์", "หน้า 7 · รูปที่ 8-3")
        YT, YB = 0.9, -1.2
        self.say("วงจรฟิลด์ = ขดลวดฟิลด์ + รีโอสตาทต่ออนุกรม ต่อกับแหล่งไฟ (แยกจากอาร์เมเจอร์ที่ไปโหลด)")
        src = VGroup(wire((-6.3, YB), (-6.3, YT), (-5.3, YT)), wire((-6.3, YB), (-1.9, YB), (-1.9, YT)),
                     meter([-6.3, -0.15], "DC", r=0.3))
        rh = res_zig([-5.3, YT], [-3.9, YT], n=5)
        sl = Arrow([-4.6, YT + 0.62, 0], [-4.6, YT + 0.1, 0], buff=0, color=YEL, tip_length=0.17, stroke_width=4,
                   max_tip_length_to_length_ratio=0.5)
        cl = coil_sym([-3.9, YT], [-1.9, YT], n=5, r=0.1, color=C_IF)
        arm = arm_sym([-0.6, -0.15], r=0.42)
        ld = Arrow([0.0, -0.15, 0], [0.9, -0.15, 0], buff=0, color=GRAYTXT, stroke_width=3, tip_length=0.15)
        t_ld = tag("ไปโหลด", size=18).next_to(ld, UP, buff=0.05)
        t_r = tag("รีโอสตาท", size=18, color=C_R).move_to([-4.6, 1.75, 0])
        t_f = tag("ขดลวดฟิลด์", size=18, color=C_IF).move_to([-2.9, 1.5, 0])
        t_a = tag("อาร์เมเจอร์", size=18, color=C_E).move_to([-0.6, -0.95, 0])
        self.play(Create(src), run_time=0.8)
        self.play(Create(rh), Create(cl), FadeIn(sl), FadeIn(t_r), FadeIn(t_f), run_time=1.0)
        self.play(FadeIn(arm), FadeIn(ld), FadeIn(t_ld), FadeIn(t_a), run_time=0.8)
        self.wait(0.8)

        self.say("วงจรฟิลด์เป็นแค่ตัวต้านทาน → กฎของโอห์ม  V = If × R : เส้นตรงผ่านจุดกำเนิด สโลป = R", color=C_R)
        s = ValueTracker(1.5)
        g = make_axes(pos=[2.1, -2.55], x_len=4.4, y_len=3.3, xmax=1.0, ymax=1.0, xl=r"I_f", yl=r"V")
        ax = g.ax
        line = always_redraw(lambda: Line(ax.c2p(0, 0), ax.c2p(min(1.0, 1.0 / s.get_value()), min(1.0, s.get_value())),
                                          color=C_R, stroke_width=6))
        eq = MathTex(r"V", r"=", r"I_f", r"R", font_size=52).move_to([-3.0, -2.15, 0])
        eq[0].set_color(WHITE), eq[2].set_color(C_IF), eq[3].set_color(C_R)
        self.play(Create(g), run_time=0.8)
        self.add(line)
        self.play(Write(eq), run_time=0.9)
        self.glow(eq[3], rh, color=C_R)
        self.wait(0.6)

        self.say("ปรับรีโอสตาท R มาก → เส้นชัน    R น้อย → เส้นราบ   (สโลปคือค่า R รวมของวงจรฟิลด์)", color=C_R)
        # ป้าย max วางเหนือปลายเส้นชันสุด (เหนือยอดแกน V: ทุกเส้นอยู่ต่ำกว่าระดับนี้เสมอ จึงไม่ถูกเส้นที่กวาดพาดทับ และไม่ชนแกน)
        lmax = Text("max (R มาก)", font_size=18, color=C_R)
        lmax.move_to(ax.c2p(1.0 / 3.2, 1.0) + UP * 0.34 + RIGHT * (lmax.width / 2 - 0.1))
        lmin = Text("min (R น้อย)", font_size=18, color=C_R).move_to(ax.c2p(0.78, 0.46))
        self.play(s.animate.set_value(3.2), run_time=1.6)
        self.play(FadeIn(lmax), run_time=0.4)
        self.play(s.animate.set_value(0.85), run_time=2.2)
        self.play(FadeIn(lmin), run_time=0.4)
        self.play(s.animate.set_value(1.5), run_time=1.2)
        self.wait(0.8)

        self.say("แรงดันเท่ากัน: R มากกระแสน้อย  R น้อยกระแสมาก  (เส้นชันตัดที่ If น้อยกว่า)", color=OK)
        v0 = 0.62
        hz = DashedLine(ax.c2p(0, v0), ax.c2p(0.95, v0), color=GRAYTXT, stroke_width=2)
        lines = VGroup(*[Line(ax.c2p(0, 0), ax.c2p(min(1.0, 1.0 / sv), min(1.0, sv)), color=C_R, stroke_width=4,
                              stroke_opacity=0.6) for sv in (3.2, 0.85)])
        dots = VGroup(*[Dot(ax.c2p(v0 / sv, v0), radius=0.09, color=C_IF) for sv in (3.2, 1.5, 0.85)])
        self.play(Create(hz), FadeIn(lines), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in dots], lag_ratio=0.4), run_time=1.4)
        self.wait(2.0)
        self.exam("จุดออกสอบ 8-4: เส้นความต้านทานของฟิลด์คืออะไร สโลปบอกอะไร",
                  "กราฟกฎของโอห์ม V = If × R ของวงจรฟิลด์ — สโลป = ความต้านทานรวม (ขดลวด + รีโอสตาท) ปรับได้ด้วยรีโอสตาท")


# =============================================================== P08  หน้า 8
class P08_BuildUpSteps(Lesson):
    """8-5: เครื่องแบบขนานสร้างแรงเคลื่อนเอง ข้อ 1-4 — ภาพตัดเครื่อง + วงป้อนกลับ E -> If -> flux -> E"""

    def construct(self):
        self.head("8-5 สร้างแรงเคลื่อนในเครื่องแบบขนาน", "หน้า 8 · 8-5")
        lv = ValueTracker(0.10)
        C = np.array([-3.7, 0.1, 0.0])
        m = machine(0.8).move_to(C)
        m.flux.add_updater(lambda f: flux_set(f, lv.get_value()))
        flux_set(m.flux, 0.10)
        coil = m.coils[0]
        r_arm = 0.78 * 0.8
        xw = coil.get_left()[0]          # สายฟิลด์วิ่งตามขอบซ้ายของขดลวด ไม่ผ่านกลางขั้ว (กันทับตัวอักษร N)
        loop = wire((C[0], C[1] - r_arm), (C[0], C[1] - 1.85), (xw, C[1] - 1.85),
                    (xw, coil.get_bottom()[1]), (xw, coil.get_top()[1]),
                    (xw, C[1] + 1.85), (C[0], C[1] + 1.85), (C[0], C[1] + r_arm),
                    (C[0], C[1] - r_arm), color=C_IF, width=3)
        self.say("คำถาม: เครื่องแบบขนานเอาไฟของตัวเองมาป้อนฟิลด์ได้ยังไง ทั้งที่ตอนเริ่มยังไม่มีไฟ?", color=WARN)
        self.play(FadeIn(m, shift=RIGHT * 0.3), run_time=0.8)
        self.play(Create(loop), run_time=1.0)
        t_loop = tag("ขดลวดฟิลด์ต่อคร่อมขั้วอาร์เมเจอร์ของตัวเอง", size=18, color=C_IF).move_to([-3.7, -2.3, 0])
        self.play(FadeIn(t_loop), run_time=0.5)
        self.wait(1.2)

        bd = Board(self, x=0.4, y=2.05, gap=0.1)
        # ---- ขั้น 1
        self.say("ขั้น 1: เครื่องหมุนถึงความเร็วหนึ่ง → อำนาจแม่เหล็กตกค้างทำให้เกิด E1 เล็กๆ โดยยังไม่มี If เลย", color=C_E)
        e1 = MathTex(r"E_1", font_size=34, color=C_E).move_to(C + np.array([0.0, -1.35, 0]))
        e1.next_to(loop, DOWN, buff=0.0).shift(UP * 0.45 + RIGHT * 0.55)
        self.play(Indicate(m.flux, color=C_PHI, scale_factor=1.15), Indicate(m.rot, color=YEL), FadeIn(e1), run_time=1.0)
        bd.add(1, "ตกค้าง → E1 (ยังไม่มี If)", MathTex(r"E_1\ \ (I_f=0)", font_size=30, color=C_E), color=C_E)
        # ---- ขั้น 2
        self.say("ขั้น 2: E1 ถูกจ่ายคร่อมวงจรฟิลด์ → เกิดกระแสฟิลด์ If1 ไหลในขดลวด", color=C_IF)
        i1 = MathTex(r"I_{f1}", font_size=34, color=C_IF).next_to(coil, LEFT, buff=0.1).shift(DOWN * 0.7 + LEFT * 0.32)
        self.play(flow(loop, C_IF, run=1.6), FadeIn(i1), Indicate(coil, color=C_IF, scale_factor=1.12))
        bd.add(2, "E1 จ่ายฟิลด์ → If1", MathTex(r"E_1\ \longrightarrow\ I_{f1}", font_size=30, color=C_IF), color=C_IF)
        # ---- ขั้น 3
        self.say("ขั้น 3: If1 เสริมฟลักซ์ให้มากกว่าเดิม → เหนี่ยวนำ E2 ที่มากกว่า E1", color=C_PHI)
        e2 = MathTex(r"E_2", font_size=34, color=C_E).move_to(e1)
        self.play(lv.animate.set_value(0.30), Transform(e1, e2), run_time=1.6)
        bd.add(3, "If1 → ฟลักซ์เพิ่ม → E2 > E1", MathTex(r"I_{f1}\longrightarrow \phi\uparrow\longrightarrow E_2>E_1",
                                                         font_size=28, color=C_PHI), color=C_PHI)
        # ---- ขั้น 4
        self.say("ขั้น 4: E2 (ที่มากกว่า) ถูกจ่ายคร่อมฟิลด์ → ได้ If2 ที่มากกว่า If1", color=C_IF)
        i2 = MathTex(r"I_{f2}", font_size=34, color=C_IF).move_to(i1)
        self.play(flow(loop, C_IF, run=1.6), Transform(i1, i2))
        bd.add(4, "E2 จ่ายฟิลด์ → If2 > If1", MathTex(r"E_2\longrightarrow I_{f2}>I_{f1}", font_size=30, color=C_IF),
               color=C_IF)
        self.wait(0.6)

        # ---- วงป้อนกลับ
        self.say("ฟลักซ์เพิ่ม → E เพิ่ม → If เพิ่ม → ฟลักซ์เพิ่มอีก … วนซ้ำ = วงป้อนกลับบวก (positive feedback)", color=OK)
        self.play(lv.animate.set_value(0.65), run_time=2.4)
        ch = chips([(r"E", "แรงเคลื่อน", C_E), (r"I_f", "กระแสฟิลด์", C_IF), (r"\phi", "ฟลักซ์", C_PHI)])
        ch.scale(0.85).move_to([3.4, -2.35, 0])
        back = CurvedArrow(ch.cs[2].get_bottom() + DOWN * 0.02, ch.cs[0].get_bottom() + DOWN * 0.02, angle=-TAU / 4.2,
                           color=OK, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(ch), Create(back), run_time=1.2)
        self.play(*[Indicate(c, color=col) for c, col in zip(ch.cs, (C_E, C_IF, C_PHI))], run_time=1.4)
        self.wait(1.4)
        self.exam("จุดออกสอบ 8-5: เครื่องกำเนิดแบบขนานสร้างแรงเคลื่อนขึ้นเองได้อย่างไร",
                  "หมุน → อำนาจตกค้างให้ E1 → E1 ป้อนฟิลด์ได้ If1 → ฟลักซ์เพิ่ม → E2 > E1 → If2 > If1 … วนซ้ำ (ป้อนกลับบวก)")
