"""EPS8 หน้า 4-6 (8-3 ตัวอย่าง 8-1/8-2, 8-4 เริ่ม) — ดู eps8_lib.py"""
from eps8_lib import *
from eps8_a import chips


# =============================================================== P04  หน้า 4
class P04_LabEx81(Lesson):
    """หน้า 4: วิธีวัดเคอร์ฟในแล็บ (ถูก/ผิด) + ตัวอย่าง 8-1  E ∝ n  (113 V)"""

    def construct(self):
        self.head("8-3 วิธีวัดเคอร์ฟ + ตัวอย่าง 8-1", "หน้า 4 · ตย.8-1")
        self.say("ในแล็บ: เพิ่ม If ทางเดียวจนสุด แล้วลดทางเดียวจนถึง 0 — ห้ามเพิ่มๆ ลดๆ สลับไปมา", color=OK)
        g = make_axes(pos=[1.2, -2.6], x_len=5.0, y_len=3.4, xmax=1.3, ymax=1.15)
        ax = g.ax
        up = ax.plot(curve_up, x_range=[0, 1.2, 0.02], color=C_PHI, stroke_width=3).set_stroke(opacity=0.55)
        dn = ax.plot(curve_down, x_range=[0, 1.2, 0.02], color=C_R, stroke_width=3).set_stroke(opacity=0.55)
        ok_c = card([("✓ วิธีที่ถูก", FORCE), "เพิ่ม If ทางเดียวจนสุด", "แล้วลดทางเดียวจนเป็น 0"], color=FORCE, w=3.6)
        ok_c.move_to([-4.0, 1.1, 0])
        bad_c = card([("✗ วิธีที่ผิด", EMF), "เพิ่มๆ ลดๆ สลับไปมา", "→ ค่าหลุดจากเคอร์ฟจริง"], color=EMF, w=3.6)
        bad_c.move_to([-4.0, -0.9, 0])
        self.play(Create(g), Create(up), Create(dn), FadeIn(ok_c), run_time=1.0)
        p_ok = band_path(ax, [(0, 0), (1.2, 0), (1.2, 1), (0, 1)], color=FORCE, width=5)
        d = Dot(p_ok.get_start(), color=WHITE, radius=0.1)
        self.add(d)
        self.play(Create(p_ok), MoveAlongPath(d, p_ok), run_time=3.4, rate_func=linear)
        self.wait(0.5)
        self.say("ถ้าสลับขึ้นๆ ลงๆ จะวนอยู่ในแถบฮิสเตอรีซิส — ได้จุดที่ไม่ใช่เคอร์ฟที่แท้จริง", color=WARN)
        p_bad = band_path(ax, [(0, 0), (0.6, 0), (0.25, 0.75), (0.85, 0.2), (0.4, 0.6), (0.0, 0.5)], color=EMF, width=5)
        d2 = Dot(p_bad.get_start(), color=WHITE, radius=0.1)
        self.play(FadeOut(p_ok), FadeOut(d), FadeIn(bad_c), FadeIn(d2), run_time=0.6)
        self.play(Create(p_bad), MoveAlongPath(d2, p_bad), run_time=4.0, rate_func=linear)
        self.wait(1.0)

        # ---- ตัวอย่าง 8-1
        self.say("ปัญหาอีกข้อ: ตัวขับหมุนไม่ตรงพิกัด → แก้ได้ เพราะ If เดิม ฟลักซ์เดิม E ∝ n (ตัวอย่าง 8-1)", color=OK)
        self.play(FadeOut(VGroup(g, up, dn, ok_c, bad_c, p_bad, d2)), run_time=0.7)
        bd = Board(self, x=-6.6, y=2.0)
        c1 = card([("ตอนทดสอบ  n = 1750 รอบ/นาที", GRAYTXT)], color=C_PHI, w=4.2).move_to([3.7, 1.6, 0])
        e1 = MathTex(r"E_2=110\ \mathrm{V}", font_size=44, color=C_PHI).next_to(c1, DOWN, buff=0.15)
        c2 = card([("ที่พิกัด  n = 1800 รอบ/นาที", GRAYTXT)], color=C_E, w=4.2).move_to([3.7, -1.05, 0])
        q = MathTex(r"E_1=\ ?", font_size=44, color=C_E).next_to(c2, DOWN, buff=0.15)
        mul = MathTex(r"\times\dfrac{1800}{1750}", font_size=34, color=YEL)
        mul.move_to([3.7, 0.0, 0])
        bd.add(1, "โจทย์ให้อะไร",
               VGroup(n_text("วัดได้ E = 110 V ที่ 1750 รอบ/นาที", size=20),
                      n_text("ถามหา E ที่พิกัด 1800 รอบ/นาที", size=20)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
               color=OK, hold=0.2)
        self.play(FadeIn(c1), FadeIn(e1), FadeIn(c2), FadeIn(q), run_time=0.8)
        eq = MathTex(r"\frac{E_1}{E_2}=\frac{k\phi\,n_1}{k\phi\,n_2}=\frac{n_1}{n_2}", font_size=34)
        bd.add(2, "สูตร (If เดิม → φ คงที่)", eq, color=OK)
        sub = MathTex(r"E_1=E_2\,\frac{n_1}{n_2}=110\times\frac{1800}{1750}", font_size=34)
        bd.add(3, "แทนค่า", sub, color=OK, hold=0.2)
        self.play(FadeIn(mul), run_time=0.5)
        res = VGroup(MathTex(r"E_1=113\ \mathrm{V}", font_size=36, color=OK),
                     n_text("(113.14) ความเร็วเพิ่ม E ต้องเพิ่ม ✓", size=19, color=GRAYTXT)).arrange(RIGHT, buff=0.3)
        bd.add(4, "ตรวจคำตอบ", res, color=OK, hold=0.1)
        ans = MathTex(r"E_1=113\ \mathrm{V}", font_size=44, color=OK).move_to(q)
        self.play(Transform(q, ans), run_time=0.9)
        self.wait(1.4)
        self.exam("จุดออกสอบ 8-1: เปลี่ยนความเร็วโดยไม่เปลี่ยน If แล้ว E เปลี่ยนอย่างไร",
                  "E ∝ n : E ใหม่ = E เดิม × n ใหม่ / n เดิม  (ตย.8-1: 110 × 1800/1750 = 113 V)")


# =============================================================== P05  หน้า 5
class P05_Ex82(Lesson):
    """หน้า 5: ตัวอย่าง 8-2 สร้างเคอร์ฟที่ 1000 rpm จากตารางที่ 1400 rpm (If เดิม, E ∝ n)"""

    IF = [0, 0.1, 0.2, 0.4, 0.6, 0.8]
    E14 = [6, 30, 38, 114, 153, 179]
    E10 = [6, 21.43, 27.14, 81.43, 109.29, 127.86]

    def construct(self):
        self.head("ตัวอย่าง 8-2 เคอร์ฟที่ความเร็วอื่น", "หน้า 5 · ตย.8-2")
        self.say("โจทย์: ทดสอบที่ 1400 รอบ/นาที ได้ตาราง E–If 6 จุด → อยากได้เคอร์ฟที่ 1000 รอบ/นาที", color=OK)
        lab1 = MathTex(r"E_{1400}\ (V)", font_size=26, color=C_E)
        lab2 = MathTex(r"I_f\ (A)", font_size=26, color=C_IF)
        lab3 = MathTex(r"E_{1000}\ (V)", font_size=26, color=YEL)
        rows = [(lab1, self.E14, C_E), (lab2, self.IF, C_IF), (lab3, self.E10, YEL)]
        cells = []
        for r, (lab_m, vals, col) in enumerate(rows):
            lab_m.move_to([-6.0, 1.85 - 0.55 * r, 0])
            row_c = []
            for c, v in enumerate(vals):
                t = Text(f"{v:g}", font_size=21, color=col).move_to([-4.5 + 0.98 * c, 1.85 - 0.55 * r, 0])
                row_c.append(t)
            cells.append(row_c)
        self.play(FadeIn(lab1), FadeIn(lab2), LaggedStart(*[FadeIn(t) for t in cells[0] + cells[1]], lag_ratio=0.08),
                  run_time=1.6)
        g = num_axes(1.0, 200, [0, 0.2, 0.4, 0.6, 0.8, 1.0], [50, 100, 150, 200], pos=[1.7, -2.55], x_len=4.8, y_len=3.7)
        ax = g.ax
        p14 = poly(ax, self.IF, self.E14, C_E)
        l14 = Text("n = 1400 รอบ/นาที", font_size=19, color=C_E).move_to(ax.c2p(0.42, 190))
        self.play(Create(g), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in p14.dots], lag_ratio=0.15), Create(p14.line),
                  FadeIn(l14), run_time=1.8)
        self.wait(0.8)

        self.say("ตรึง If ไว้ → ฟลักซ์ φ เท่าเดิม → E แปรตามความเร็ว  E ใหม่ = E เดิม × n ใหม่ / n เดิม", color=YEL)
        f = MathTex(r"E_{1000}", r"=", r"E_{1400}", r"\times", r"\frac{1000}{1400}", font_size=40)
        f[0].set_color(YEL), f[2].set_color(C_E)
        f.move_to([-3.4, 0.5, 0])
        self.play(Write(f), run_time=1.2)
        self.glow(f[4], None, color=YEL)
        self.wait(0.6)

        # ---- ทำทีละขั้นกับจุด If = 0.4
        self.say("ลองจุด If = 0.4 A ก่อน: ที่ 1400 รอบ/นาที E = 114 V → ที่ 1000 รอบ/นาที ได้เท่าไร", color=OK)
        self.play(FadeOut(f), run_time=0.4)
        bd = Board(self, x=-6.6, y=0.75, gap=0.12)
        hi = Dot(ax.c2p(0.4, 114), radius=0.12, color=WHITE)
        vline = DashedLine(ax.c2p(0.4, 0), ax.c2p(0.4, 114), color=GRAYTXT, stroke_width=2)
        self.play(Create(vline), FadeIn(hi), run_time=0.6)
        bd.add(1, "สูตร (If เดิม → E ∝ n)", MathTex(r"E_{1000}=E_{1400}\,\frac{n_2}{n_1}", font_size=32), color=OK, hold=0.2)
        bd.add(2, "แทนค่า", MathTex(r"E_{1000}=114\times\frac{1000}{1400}", font_size=32), color=OK, hold=0.2)
        r3 = bd.add(3, "ได้ / ตรวจ", VGroup(MathTex(r"=81.43\ \mathrm{V}", font_size=34, color=YEL),
                                           n_text("น้อยกว่า 114 ✓ (ช้าลง E ลด)", size=19, color=GRAYTXT)
                                           ).arrange(RIGHT, buff=0.3), color=OK, hold=0.2)
        n10 = Dot(ax.c2p(0.4, 81.43), radius=0.1, color=YEL)
        self.play(TransformFromCopy(hi, n10), run_time=0.9)
        self.wait(0.8)

        # ---- ทุกจุด
        self.say("ทำแบบเดียวกันทุกจุด → ได้ตารางใหม่ และเคอร์ฟ 1000 รอบ/นาที (รูปร่างเดิม แต่เตี้ยลงเท่ากันทุกจุด)", color=YEL)
        self.play(FadeOut(bd.rows[0]), FadeOut(bd.rows[1]), FadeOut(r3), FadeOut(hi), FadeOut(vline), FadeOut(n10),
                  run_time=0.5)
        p10 = poly(ax, self.IF, self.E10, YEL)
        l10 = Text("n = 1000 รอบ/นาที", font_size=19, color=YEL).move_to(ax.c2p(0.70, 80))
        self.play(FadeIn(lab3), LaggedStart(*[FadeIn(t) for t in cells[2]], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(d, scale=1.6) for d in p10.dots], lag_ratio=0.12), Create(p10.line),
                  FadeIn(l10), run_time=2.4)
        note = Text("* จุด If = 0 ต้นฉบับคงไว้ 6 V (ถ้าคูณตามสูตรเป๊ะจะได้ 4.29 V)", font_size=18, color=GRAYTXT)
        note.move_to([-2.6, -2.75, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.wait(2.0)
        self.exam("จุดออกสอบ 8-2: มีตาราง E–If ที่ความเร็วหนึ่ง จะหาเคอร์ฟที่ความเร็วอื่นอย่างไร",
                  "คูณ E ทุกจุดด้วย n ใหม่ / n เดิม (If ตัวเดิม) — ได้เคอร์ฟรูปเดิม ตัวเลขเปลี่ยนตามสัดส่วน")


# =============================================================== P06  หน้า 6
class P06_Fig82Field(Lesson):
    """หน้า 6: รูป 8-2 สองเคอร์ฟ + E=Vt ไม่มีโหลด + 8-4 เริ่ม: รีโอสตาทอนุกรมกับฟิลด์คุม If"""

    def construct(self):
        self.head("รูป 8-2 และ 8-4 รีโอสตาทคุม If", "หน้า 6 · รูปที่ 8-2, 8-4")
        self.say("รูป 8-2: เคอร์ฟ (ก) ที่ 1400 กับ (ข) ที่ 1000 รอบ/นาที — รูปร่างเดียวกัน (ข) เตี้ยกว่าตามสัดส่วน n", color=OK)
        g = num_axes(1.0, 200, [0, 0.2, 0.4, 0.6, 0.8, 1.0], [50, 100, 150, 200], pos=[-3.6, -2.4], x_len=5.2, y_len=3.7)
        ax = g.ax
        a = poly(ax, P05_Ex82.IF, P05_Ex82.E14, C_E, dots=False)
        b = poly(ax, P05_Ex82.IF, P05_Ex82.E10, YEL, dots=False)
        la = Text("(ก) n = 1400", font_size=19, color=C_E).move_to(ax.c2p(0.34, 150))
        lb = Text("(ข) n = 1000", font_size=19, color=YEL).move_to(ax.c2p(0.78, 70))
        self.play(Create(g), run_time=0.8)
        self.play(Create(a.line), FadeIn(la), run_time=1.0)
        self.play(Create(b.line), FadeIn(lb), run_time=1.0)
        self.wait(1.0)

        self.say("ข้อสังเกต: ไม่มีโหลด → Ia = 0 → ไม่มีแรงดันตกในอาร์เมเจอร์ → แรงเคลื่อน E = แรงดันที่ขั้ว Vt", color=WARN)
        eqa = MathTex(r"V_t", r"=", r"E", r"-", r"I_a R_a", font_size=46)
        eqb = MathTex(r"I_a=0", r"\;\Rightarrow\;", r"V_t=E", font_size=46)
        eqa[2].set_color(C_E), eqa[4].set_color(C_IA), eqb[0].set_color(C_IA), eqb[2].set_color(OK)
        eq = VGroup(eqa, eqb).arrange(DOWN, buff=0.4).move_to([4.2, 0.6, 0])
        self.play(Write(eqa), run_time=1.1)
        self.play(Indicate(eqa[4], color=WHITE), run_time=0.8)
        self.play(Write(eqb), run_time=1.1)
        self.wait(1.2)

        self.say("8-4: ปกติไม่ต้องให้ If = 0 แต่ต้องคุม If เพื่อคุม E — ต่อรีโอสตาทอนุกรมกับขดลวดฟิลด์", color=C_IF)
        self.play(FadeOut(VGroup(g, a, b, la, lb)), FadeOut(eq), run_time=0.7)
        YT, YB = 0.7, -1.3
        src = VGroup(wire((-5.6, YB), (-5.6, YT), (-4.6, YT)), wire((-5.6, YB), (-0.8, YB), (-0.8, YT)),
                     meter([-5.6, -0.3], "DC", r=0.3))
        rh = res_zig([-4.6, YT], [-2.9, YT], n=6)
        sl = Arrow([-3.75, YT + 0.62, 0], [-3.75, YT + 0.1, 0], buff=0, color=YEL, tip_length=0.17, stroke_width=4,
                   max_tip_length_to_length_ratio=0.5)
        cl = coil_sym([-2.9, YT], [-0.8, YT], n=5, r=0.11, color=C_IF)
        t_r = tag("รีโอสตาท Rr (ปรับได้)", size=19, color=C_R).move_to([-3.75, 1.8, 0])
        t_f = tag("ขดลวดฟิลด์ Rf", size=19, color=C_IF).move_to([-1.85, 1.4, 0])
        t_s = tag("แหล่งจ่ายไฟตรง V", size=19).move_to([-5.0, -1.9, 0])
        self.play(Create(src), run_time=0.8)
        self.play(Create(rh), Create(cl), FadeIn(sl), FadeIn(t_r), FadeIn(t_f), FadeIn(t_s), run_time=1.2)
        path = wire((-5.6, 0.0), (-5.6, YT), (-0.8, YT), (-0.8, YB), (-5.6, YB), (-5.6, -0.6))
        self.play(flow(path, C_IF, run=1.6))
        eq2 = MathTex(r"I_f", r"=", r"\frac{V}{R_f+R_r}", font_size=48).move_to([3.4, 0.3, 0])
        eq2[0].set_color(C_IF)
        self.play(Write(eq2), run_time=1.0)
        chain = chips([(r"R_r", "รีโอสตาท", C_R), (r"I_f", "กระแสฟิลด์", C_IF), (r"E", "แรงเคลื่อน", C_E)])
        chain.move_to([2.0, -2.4, 0])
        self.play(FadeIn(chain), run_time=0.8)
        self.play(Indicate(chain.cs[0], color=C_R), Indicate(chain.cs[1], color=C_IF), Indicate(chain.cs[2], color=C_E),
                  run_time=1.4)
        self.wait(1.5)
        self.exam("จุดออกสอบ 8-4: ทำไมต้องต่อรีโอสตาทอนุกรมกับขดลวดฟิลด์",
                  "เพื่อปรับกระแสฟิลด์ If = V/(Rf+Rr) → ปรับฟลักซ์ → คุม E ได้ในช่วงกว้าง")
