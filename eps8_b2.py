"""EPS8 หน้า 9-12 (รูป 8-4 .. 8-7) — ดู eps8_lib.py"""
from eps8_lib import *
from eps8_a import chips


def _lvl(txt, color=C_E, size=24):
    return MathTex(txt, font_size=size, color=color)


# =============================================================== P09  หน้า 9
class P09_BuildUpGraph(Lesson):
    """รูป 8-4 (ก)(ข)(ค) + ข้อ 5: อ่านกราฟสลับเคอร์ฟ <-> เส้นความต้านทาน  E1 -> If1 -> E2 -> If2 -> E3"""
    S = 0.8

    def construct(self):
        self.head("รูป 8-4 สร้างแรงเคลื่อน (อ่านจากกราฟ)", "หน้า 9 · รูปที่ 8-4")
        s = self.S
        Y0, XL, YLN, XM, YM = -2.5, 3.9, 4.1, 1.3, 1.15
        gs = [make_axes(pos=[x0, Y0], x_len=XL, y_len=YLN, xmax=XM, ymax=YM, xl=r"I_f", yl=yl)
              for x0, yl in zip((-6.4, -1.95, 2.6), (r"E", r"V", r"E"))]
        A, B, C = [g.ax for g in gs]
        cur_a = A.plot(lambda x: curve_c(x), x_range=[0, 1.25, 0.01], color=C_PHI, stroke_width=4)
        lin_b = Line(B.c2p(0, 0), B.c2p(1.25, s * 1.25), color=C_R, stroke_width=4)
        ttl = [Text(t, font_size=19, color=c).move_to([x, Y0 - 0.72, 0]) for t, c, x in (
            ("(ก) เคอร์ฟอิ่มตัว (ไม่มีโหลด)", C_PHI, -4.45), ("(ข) เส้นความต้านทานฟิลด์", C_R, 0.0),
            ("(ค) แรงเคลื่อนที่ถูกสร้างขึ้น", C_E, 4.55))]
        E, I = [float(curve_c(0.0))], []
        for _ in range(3):
            I.append(E[-1] / s)
            E.append(float(curve_c(I[-1])))

        def hl(lv):
            return DashedLine(A.c2p(0, lv), C.c2p(1.25, lv), color=GRAYTXT, stroke_width=2, dash_length=0.1)

        def vl(ax, x, y):
            return DashedLine(ax.c2p(x, 0), ax.c2p(x, y), color=GRAYTXT, stroke_width=2, dash_length=0.1)

        def dt(ax, x, y, col):
            return Dot(ax.c2p(x, y), radius=0.09, color=col)

        self.say("รูป 8-4: วาง 3 กราฟเรียงกัน ใช้ระดับแรงดันแกนตั้งร่วมกัน")
        self.play(*[Create(g) for g in gs], run_time=1.2)
        self.play(Create(cur_a), Create(lin_b), *[FadeIn(t) for t in ttl], run_time=1.4)
        self.wait(0.6)

        # ขั้น 1 : E1
        self.say("ขั้น 1: ที่ If = 0 มี E1 จากอำนาจแม่เหล็กตกค้าง (จุดบนเคอร์ฟ ก)", color=C_E)
        h1 = hl(E[0])
        l1 = _lvl(r"E_1", size=22).next_to(A.c2p(0, E[0]), LEFT, buff=0.06)
        da, dc = dt(A, 0, E[0], C_E), dt(C, 0, E[0], C_E)
        self.play(FadeIn(da, scale=1.8), Create(h1), FadeIn(l1), run_time=1.0)
        self.play(FadeIn(dc, scale=1.8), run_time=0.5)
        self.wait(0.5)

        # ขั้น 2 : E1 -> If1 บนเส้นความต้านทาน
        self.say("ขั้น 2: E1 ถูกจ่ายให้ฟิลด์ → อ่านจากเส้นความต้านทาน (ข) ได้ If1", color=C_IF)
        db1 = dt(B, I[0], E[0], C_R)
        v_b1 = vl(B, I[0], E[0])
        t_i1 = _lvl(r"I_{f1}", C_IF, 20).next_to(B.c2p(I[0], 0), DOWN, buff=0.06).shift(LEFT * 0.2)
        self.play(Indicate(h1, color=WHITE), run_time=0.6)
        self.play(FadeIn(db1, scale=1.8), Create(v_b1), FadeIn(t_i1), run_time=1.0)
        self.wait(0.5)

        # ขั้น 3 : If1 -> E2 บนเคอร์ฟ
        self.say("ขั้น 3: เอา If1 ไปใส่เคอร์ฟ (ก) → ได้ E2 ที่สูงกว่า E1", color=C_E)
        v_a1, v_c1 = vl(A, I[0], E[1]), vl(C, I[0], E[1])
        h2 = hl(E[1])
        l2 = _lvl(r"E_2", size=22).next_to(A.c2p(0, E[1]), LEFT, buff=0.06)
        da2, dc2 = dt(A, I[0], E[1], C_E), dt(C, I[0], E[1], C_E)
        t_i1a = _lvl(r"I_{f1}", C_IF, 20).next_to(A.c2p(I[0], 0), DOWN, buff=0.06).shift(LEFT * 0.2)
        self.play(Create(v_a1), FadeIn(t_i1a), run_time=0.7)
        self.play(FadeIn(da2, scale=1.8), Create(h2), FadeIn(l2), run_time=0.9)
        self.play(Create(v_c1), FadeIn(dc2, scale=1.8), run_time=0.7)
        self.wait(0.5)

        # ขั้น 4 : E2 -> If2
        self.say("ขั้น 4: E2 จ่ายฟิลด์ → จาก (ข) ได้ If2 ที่มากกว่า If1", color=C_IF)
        db2 = dt(B, I[1], E[1], C_R)
        v_b2 = vl(B, I[1], E[1])
        t_i2 = _lvl(r"I_{f2}", C_IF, 20).next_to(B.c2p(I[1], 0), DOWN, buff=0.06).shift(RIGHT * 0.2)
        self.play(Indicate(h2, color=WHITE), run_time=0.6)
        self.play(FadeIn(db2, scale=1.8), Create(v_b2), FadeIn(t_i2), run_time=1.0)
        self.wait(0.5)

        # ขั้น 5 : If2 -> E3 และ (ค)
        self.say("ขั้น 5: If2 ไปที่เคอร์ฟ (ก) → ได้ E3 ที่สูงกว่า E2 (นี่คือ (ค))", color=C_E)
        v_a2, v_c2 = vl(A, I[1], E[2]), vl(C, I[1], E[2])
        h3 = hl(E[2])
        l3 = _lvl(r"E_3", size=22).next_to(A.c2p(0, E[2]), LEFT, buff=0.06)
        da3, dc3 = dt(A, I[1], E[2], C_E), dt(C, I[1], E[2], C_E)
        t_i2a = _lvl(r"I_{f2}", C_IF, 20).next_to(A.c2p(I[1], 0), DOWN, buff=0.06).shift(RIGHT * 0.2)
        self.play(Create(v_a2), FadeIn(t_i2a), run_time=0.7)
        self.play(FadeIn(da3, scale=1.8), Create(h3), FadeIn(l3), run_time=0.9)
        self.play(Create(v_c2), FadeIn(dc3, scale=1.8), run_time=0.7)
        part_c = C.plot(lambda x: curve_c(x), x_range=[0, I[1], 0.01], color=C_E, stroke_width=5)
        self.play(Create(part_c), run_time=1.0)
        self.wait(0.6)

        # วนต่อ
        self.say("วนซ้ำเรื่อยๆ จนแรงเคลื่อนที่เหนี่ยวนำ = ค่าที่จ่ายให้วงจรฟิลด์", color=OK)
        xf = crit_cross(s)
        full_c = C.plot(lambda x: curve_c(x), x_range=[I[1], xf, 0.01], color=C_E, stroke_width=5)
        end_c = dt(C, xf, float(curve_c(xf)), WHITE)
        self.play(Create(full_c), run_time=2.2, rate_func=linear)
        self.play(FadeIn(end_c, scale=2.0), run_time=0.9)
        self.wait(1.8)
        self.exam("จุดออกสอบ 8-5: อธิบายการสร้างแรงเคลื่อนด้วยกราฟ (ก) เคอร์ฟ และ (ข) เส้นความต้านทาน",
                  "E1 → If1 (จากเส้นความต้านทาน) → E2 (จากเคอร์ฟ) → If2 → E3 … ไต่ขึ้นจนถึงจุดตัดของเส้นกับเคอร์ฟ")


# =============================================================== P10  หน้า 10
class P10_Staircase(Lesson):
    """รูป 8-5: ซ้อนเคอร์ฟ+เส้นความต้านทานแกนเดียว บันไดไต่ถึงจุดตัด; 8-6 เริ่ม: ปรับ R เส้นเอียง จุดตัดเลื่อน"""
    S = 0.9

    def construct(self):
        self.head("รูป 8-5 บันไดไต่ถึงจุดตัด + 8-6 เริ่ม", "หน้า 10 · รูปที่ 8-5")
        s = self.S
        sl = ValueTracker(s)
        g = make_axes(pos=[-6.2, -2.55], x_len=7.6, y_len=4.2, xmax=1.6, ymax=1.15, xl=r"I_f", yl=r"E")
        ax = g.ax
        cur = ax.plot(lambda x: curve_c(x), x_range=[0, 1.55, 0.01], color=C_PHI, stroke_width=5)
        line = always_redraw(lambda: Line(ax.c2p(0, 0), ax.c2p(min(1.55, 1.1 / sl.get_value()), min(1.1, 1.55 * sl.get_value())),
                                          color=C_R, stroke_width=5))
        k_cur = VGroup(Line(ORIGIN, RIGHT * 0.5, color=C_PHI, stroke_width=5),
                       Text("เคอร์ฟ E–If (ไม่มีโหลด)", font_size=19, color=C_PHI)).arrange(RIGHT, buff=0.15)
        k_lin = VGroup(Line(ORIGIN, RIGHT * 0.5, color=C_R, stroke_width=5),
                       Text("เส้นความต้านทานฟิลด์ V = If·R", font_size=19, color=C_R)).arrange(RIGHT, buff=0.15)
        key = VGroup(k_cur, k_lin).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 1.6, 0])
        self.say("เอาเคอร์ฟ (ค) กับเส้นความต้านทาน (ข) มาวางบนแกนเดียวกัน")
        self.play(Create(g), run_time=0.8)
        self.play(Create(cur), FadeIn(line), FadeIn(key), run_time=1.3)
        self.wait(0.5)

        self.say("ไต่บันได: ขึ้นไปที่เคอร์ฟ → ข้ามไปที่เส้นความต้านทาน → ขึ้นเคอร์ฟอีก …", color=OK)
        pts, Es, Is = stair_pts(ax, s, n=6)
        path = VMobject(stroke_color=WHITE, stroke_width=3)
        path.set_points_as_corners(pts)
        d = Dot(pts[0], color=WHITE, radius=0.09)
        self.add(d)
        self.play(Create(path), MoveAlongPath(d, path), run_time=5.5, rate_func=linear)
        labs = VGroup(_lvl(r"E_1", size=22).next_to(ax.c2p(0, Es[0]), LEFT, buff=0.06),
                      _lvl(r"E_2", size=22).next_to(ax.c2p(0, Es[1]), LEFT, buff=0.06),
                      _lvl(r"E_3", size=22).next_to(ax.c2p(0, Es[2]), LEFT, buff=0.06),
                      _lvl(r"I_{f1}", C_IF, 20).next_to(ax.c2p(Is[0], 0), DOWN, buff=0.06).shift(LEFT * 0.2),
                      _lvl(r"I_{f2}", C_IF, 20).next_to(ax.c2p(Is[1], 0), DOWN, buff=0.06).shift(RIGHT * 0.2))
        self.play(FadeIn(labs), run_time=0.8)
        self.wait(0.6)

        self.say("ถึงจุดตัด: E ที่เครื่องสร้างได้ = V ที่ฟิลด์ต้องการ → ไม่มีส่วนต่างให้ไต่ต่อ (สมดุล)", color=C_E)
        xf = crit_cross(s)
        ef = float(curve_c(xf))
        pt = Dot(ax.c2p(xf, ef), radius=0.12, color=C_E)
        h = DashedLine(ax.c2p(0, ef), ax.c2p(xf, ef), color=GRAYTXT, stroke_width=2)
        v = DashedLine(ax.c2p(xf, 0), ax.c2p(xf, ef), color=GRAYTXT, stroke_width=2)
        tk = Text("จุดตัด = จุดทำงาน", font_size=20, color=C_E).next_to(pt, DOWN, buff=0.3)
        tk.set_x(pt.get_x() + 0.22 + tk.width / 2)      # ขอบซ้ายป้ายอยู่ทางขวาของเส้นประตั้ง ไม่ให้เส้นพาดผ่านตัวอักษร
        self.play(FadeOut(d), Create(h), Create(v), FadeIn(pt, scale=2.0), FadeIn(tk), run_time=1.2)
        self.wait(1.2)

        # 8-6 : ปรับรีโอสตาท
        self.say("8-6: ลดความต้านทานรีโอสตาท → เส้นราบลง → ตัดเคอร์ฟสูงขึ้น (แรงดันสูงขึ้น)", color=C_R)
        pt2 = always_redraw(lambda: Dot(ax.c2p(crit_cross(sl.get_value()), float(curve_c(crit_cross(sl.get_value())))),
                                        radius=0.12, color=YEL))
        self.play(FadeOut(pt), FadeOut(tk), FadeOut(h), FadeOut(v), FadeOut(path), FadeOut(labs), run_time=0.6)
        self.add(pt2)
        t_lo = Text("R ลด → เส้นราบ → จุดตัดสูงขึ้น", font_size=21, color=C_R).move_to([4.2, 0.2, 0])
        t_hi = Text("R เพิ่ม → เส้นชัน → จุดตัดต่ำลง", font_size=21, color=C_R).move_to([4.2, -0.6, 0])
        self.play(sl.animate.set_value(0.7), FadeIn(t_lo), run_time=2.0)
        self.wait(0.5)
        self.say("แต่ถ้าเพิ่มความต้านทาน เส้นจะชันขึ้น จุดตัดเลื่อนต่ำลง", color=C_R)
        self.play(sl.animate.set_value(1.35), FadeIn(t_hi), run_time=2.6)
        self.wait(1.4)
        self.exam("จุดออกสอบ 8-5/8-6: แรงเคลื่อนที่สร้างได้หยุดที่ไหน และปรับรีโอสตาทแล้วเป็นอย่างไร",
                  "หยุดที่จุดตัดของเส้นความต้านทานกับเคอร์ฟ · R ลด → เส้นราบ → E สูงขึ้น · R เพิ่ม → เส้นชัน → E ต่ำลง")


# =============================================================== P11  หน้า 11
class P11_CriticalR(Lesson):
    """รูป 8-6 ความต้านทานวิกฤต (เส้น R3 ทับช่วงตรงของเคอร์ฟ) + 8-7 เริ่ม: ไม่มีอำนาจตกค้าง / ต่อฟิลด์กลับ"""

    def construct(self):
        self.head("รูป 8-6 ความต้านทานวิกฤต · 8-7 เริ่ม", "หน้า 11 · รูปที่ 8-6, 8-7")
        sl = ValueTracker(0.8)
        g = make_axes(pos=[-6.2, -2.55], x_len=7.0, y_len=4.2, xmax=1.6, ymax=1.15, xl=r"I_f", yl=r"E")
        ax = g.ax
        cur = ax.plot(lambda x: curve_c(x), x_range=[0, 1.55, 0.01], color=C_PHI, stroke_width=5)
        lines = {}
        for nm, sv in (("R2", 0.8), ("R1", 1.1), ("R3", 1.6)):
            xe = min(1.55, 1.1 / sv)
            lines[nm] = Line(ax.c2p(0, 0), ax.c2p(xe, sv * xe), color=C_R, stroke_width=4)
        labs = {nm: Text(nm, font_size=24, color=C_R).next_to(ln.get_end(), UP, buff=0.1) for nm, ln in lines.items()}
        self.say("รูป 8-6: เส้นความต้านทานฟิลด์ 3 เส้น ตัดเคอร์ฟที่จุดต่างกัน")
        self.play(Create(g), run_time=0.8)
        self.play(Create(cur), run_time=1.0)
        self.play(*[Create(ln) for ln in lines.values()], *[FadeIn(t) for t in labs.values()], run_time=1.4)
        self.wait(0.4)

        self.say("เส้นชันสุด R3 ทับช่วงตรงของเคอร์ฟ = ความต้านทานวิกฤต", color=C_R)
        r3 = lines["R3"]
        crit = Text("ความต้านทานวิกฤต", font_size=21, color=YEL).move_to(ax.c2p(0, 0.96))
        crit.shift(RIGHT * (0.32 + crit.width / 2))     # อยู่ทางขวาของแกน E (เดิมพาดทับแกน) และซ้ายของเส้น R3
        ar = Arrow(crit.get_bottom() + RIGHT * 0.2, ax.c2p(0.3, 0.6), buff=0.05, color=YEL, stroke_width=3,
                   tip_length=0.15, max_tip_length_to_length_ratio=0.35)
        self.play(Indicate(r3, color=YEL, scale_factor=1.0), Circumscribe(labs["R3"], color=YEL), FadeIn(crit), Create(ar),
                  run_time=1.4)
        pts = VGroup(*[Dot(ax.c2p(crit_cross(sv), float(curve_c(crit_cross(sv)))), radius=0.09, color=C_E)
                       for sv in (0.8, 1.1, 1.6)])
        self.play(LaggedStart(*[FadeIn(p, scale=1.8) for p in pts], lag_ratio=0.35), run_time=1.4)
        self.wait(0.5)

        self.say("ความต้านทานน้อยกว่าวิกฤต (R1, R2) → ตัดสูง สร้างแรงเคลื่อนได้", color=OK)
        self.play(Indicate(labs["R1"], color=OK), Indicate(labs["R2"], color=OK), run_time=1.2)
        self.wait(0.5)

        self.say("มากกว่าวิกฤต (ชันกว่า R3) → ตัดต่ำแถวแรงเคลื่อนตกค้าง ไม่สร้างแรงเคลื่อน", color=WARN)
        dot = always_redraw(lambda: Dot(ax.c2p(crit_cross(sl.get_value()), float(curve_c(crit_cross(sl.get_value())))),
                                        radius=0.12, color=YEL))
        ln = always_redraw(lambda: Line(ax.c2p(0, 0), ax.c2p(min(1.55, 1.1 / sl.get_value()), min(1.1, 1.55 * sl.get_value())),
                                        color=WARN, stroke_width=5))
        self.play(FadeOut(pts), FadeOut(crit), FadeOut(ar), FadeOut(VGroup(*lines.values())),
                  FadeOut(VGroup(*labs.values())), run_time=0.5)
        self.add(ln, dot)
        self.play(sl.animate.set_value(1.6), run_time=2.4)
        self.play(sl.animate.set_value(2.4), run_time=1.6)
        note = Text("หมายเหตุ: เอกสารเขียนเส้นวิกฤตเป็น R1 แต่ลูกศรในรูป 8-6 ชี้ R3 — คลิปนี้ใช้ตามรูป", font_size=17,
                    color=GRAYTXT).move_to([3.0, -3.55, 0])     # ต่ำกว่าป้ายแกน If (เดิมชนตัว f)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.4)

        # ---------------- 8-7 สาเหตุ 1-2
        self.say("8-7: ทำไมเครื่องไม่สร้างแรงเคลื่อน — สาเหตุที่ 1: ไม่มีอำนาจแม่เหล็กตกค้าง", color=WARN)
        ln.clear_updaters()
        dot.clear_updaters()
        self.play(FadeOut(VGroup(g, cur, ln, dot, note)), run_time=0.6)
        m = machine(0.62).move_to([-4.6, 0.7, 0])
        flux_set(m.flux, 0.0)
        d_box, d_arrs = domains(lambda: 0.0, w=2.0, h=1.0)
        d_box.move_to([-4.6, -1.9, 0])
        t1 = Text("ไม่มีตกค้าง → E1 = 0 → If = 0 → ไม่เริ่มไต่", font_size=20, color=WARN).move_to([1.0, 1.7, 0])
        self.play(FadeIn(m), FadeIn(d_box), FadeIn(d_arrs), FadeIn(t1), run_time=0.9)
        self.wait(0.6)
        fix = Text("แก้: flashing the field", font_size=24, color=OK).move_to([2.2, 0.8, 0])
        fix2 = Text("ป้อนไฟตรงจากภายนอกเข้าฟิลด์ 2–3 วินาที แล้วปลดออก", font_size=19, color=OK).move_to([2.2, 0.3, 0])
        bat = meter([0.4, -1.3], "DC", color=YEL, r=0.32)
        wl = wire((0.72, -1.3), (2.6, -1.3), (2.6, -1.9), color=YEL)
        cl = coil_sym([2.6, -1.9], [2.6, -3.1], n=4, r=0.1, color=C_IF)
        self.play(FadeIn(fix), FadeIn(fix2), Create(bat), Create(wl), Create(cl), run_time=1.0)
        lv = ValueTracker(0.0)
        m.flux.add_updater(lambda f: flux_set(f, lv.get_value()))
        self.play(lv.animate.set_value(0.28), run_time=1.4)
        self.play(FadeOut(VGroup(bat, wl, cl)), run_time=0.6)
        self.wait(0.8)
        self.say("สาเหตุที่ 2: ต่อฟิลด์กลับทิศทาง → ฟลักซ์ที่ได้สวนกับฟลักซ์ตกค้าง E ลดลง", color=WARN)
        self.play(FadeOut(VGroup(fix, fix2, t1)), run_time=0.5)
        a_res = Arrow([0.4, 0.9, 0], [2.4, 0.9, 0], buff=0, color=C_PHI, stroke_width=6)
        a_fld = Arrow([2.4, 0.2, 0], [0.4, 0.2, 0], buff=0, color=C_E, stroke_width=6)
        l_res = Text("ฟลักซ์ตกค้าง", font_size=19, color=C_PHI).next_to(a_res, UP, buff=0.1)
        l_fld = Text("ฟลักซ์จากกระแสฟิลด์ (ต่อกลับ)", font_size=19, color=C_E).next_to(a_fld, DOWN, buff=0.1)
        self.play(Create(a_res), FadeIn(l_res), run_time=0.8)
        self.play(Create(a_fld), FadeIn(l_fld), run_time=0.8)
        self.play(lv.animate.set_value(0.04), run_time=1.4)
        fx = Text("แก้: สลับขั้วการต่อฟิลด์เมื่อเทียบกับอาร์เมเจอร์", font_size=21, color=OK).move_to([2.8, -1.5, 0])
        self.play(FadeIn(fx), run_time=0.6)
        self.wait(2.0)
        self.exam("จุดออกสอบ 8-6/8-7: ความต้านทานวิกฤตคืออะไร และเครื่องไม่สร้างแรงเคลื่อนเพราะอะไรได้บ้าง",
                  "Rc = ความต้านทานของเส้นที่ทับช่วงตรงของเคอร์ฟ · ไม่มีตกค้าง (flashing) · ต่อฟิลด์กลับ · R ฟิลด์สูงเกิน Rc")
