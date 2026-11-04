"""EPS8 หน้า 1-7 (8-1 .. 8-4) — ดู eps8_lib.py"""
from eps8_lib import *


def chips(labels, w=1.75, h=0.7):
    """โซ่เหตุผล 3 ช่อง:  [สัญลักษณ์ ชื่อ] -> [..] -> [..]   labels = [(tex, ไทย, สี), ...]"""
    cs = VGroup()
    for tex, th, col in labels:
        sym = MathTex(tex, font_size=30, color=col)
        nm = Text(th, font_size=18, color=WHITE)
        inner = VGroup(sym, nm).arrange(RIGHT, buff=0.1)
        bw = max(w, inner.width + 0.4)     # กล่องขยายตามความกว้างตัวอักษรจริง (ฟอนต์ Loma บนคลาวด์กว้างกว่า Leelawadee ตัวอักษรล้นกล่อง/ทับลูกศร)
        box = RoundedRectangle(width=bw, height=h, corner_radius=0.12, stroke_color=col, stroke_width=3,
                               fill_color=col, fill_opacity=0.14)
        inner.move_to(box)
        cs.add(VGroup(box, inner))
    cs.arrange(RIGHT, buff=0.42)
    arrows = VGroup(*[Arrow(cs[i].get_right(), cs[i + 1].get_left(), buff=0.04, color=GRAYTXT, stroke_width=3,
                            tip_length=0.14) for i in range(len(cs) - 1)])
    g = VGroup(cs, arrows)
    g.cs, g.arrows = cs, arrows
    return g


# =============================================================== P02  หน้า 2
class P02_Concept(Lesson):
    """8-3 ภาพจริงก่อน: เพิ่ม If -> ฟลักซ์ -> E  (จุด 1-4 ของรูป 8-1 ข) + โมเลกุลแม่เหล็กอิ่มตัว"""

    def construct(self):
        self.head("8-3 เคอร์ฟการอิ่มตัว (ไม่มีโหลด)", "หน้า 2 · 8-3")
        x = ValueTracker(0.6)
        m = machine(0.85).move_to([-3.9, 0.45, 0])
        flux_set(m.flux, curve_up(0.6))
        m.flux.add_updater(lambda f: flux_set(f, curve_up(x.get_value())))
        self.play(FadeIn(m, shift=RIGHT * 0.3), run_time=0.8)

        # ---- 1) สูตรและพจน์ที่เกี่ยวข้อง
        self.say("สูตร E = kφn : ตรึงความเร็ว n ไว้ (k คงที่) → E ขึ้นกับฟลักซ์ φ เท่านั้น", hold=0.2)
        eq = MathTex(r"E", r"=", r"k", r"\phi", r"n", font_size=60).move_to([3.5, 1.55, 0])
        eq[0].set_color(C_E)
        eq[3].set_color(C_PHI)
        eq[4].set_color(YEL)
        self.play(Write(eq), run_time=1.0)
        self.glow(eq[3], m.flux, color=C_PHI)
        self.glow(eq[4], m.rot, color=YEL)
        self.wait(0.6)

        # ---- 2) ฟลักซ์มาจาก If
        self.say("ฟลักซ์ φ มาจากกระแสฟิลด์ If (ขดลวดสีเขียว) → ลองเพิ่ม If ทีละนิด แล้วดูว่า E ตามแค่ไหน")
        g = make_axes(pos=[0.9, -2.5], x_len=5.4, y_len=3.4, xmax=1.3, ymax=1.1)
        ax = g.ax
        ch = chips([(r"I_f", "กระแสฟิลด์", C_IF), (r"\phi", "ฟลักซ์", C_PHI), (r"E", "แรงเคลื่อน", C_E)])
        ch.move_to([3.55, 1.6, 0])
        self.play(FadeOut(eq), Indicate(m.coils, color=C_IF, scale_factor=1.12), run_time=0.9)
        self.play(x.animate.set_value(0.0), run_time=1.2)
        self.play(Create(g), FadeIn(ch), run_time=1.1)
        self.wait(0.8)

        # ---- 3) จุด 1 : อำนาจแม่เหล็กตกค้าง
        self.say("จุด 1 : If = 0 แต่ E ยังไม่เป็นศูนย์ — เพราะแกนเหล็กยังมีอำนาจแม่เหล็กตกค้าง", color=WARN)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), curve_up(x.get_value())), color=C_E, radius=0.1))
        trace = always_redraw(lambda: ax.plot(curve_up, x_range=[0, max(x.get_value(), 0.002), 0.02],
                                              color=C_PHI, stroke_width=5))
        l1 = Text("1", font_size=26, color=WHITE).next_to(ax.c2p(0, curve_up(0)), LEFT, buff=0.3)
        box, arrs = domains(lambda: curve_up(x.get_value()), w=2.5, h=1.3)
        box.move_to([-3.9, -2.2, 0])
        dl = Text("โมเลกุลแม่เหล็กในเนื้อเหล็ก (ขยาย)", font_size=17, color=GRAYTXT).move_to([-3.9, -1.3, 0])
        self.add(trace, dot)
        self.play(FadeIn(l1), FadeIn(box), FadeIn(arrs), FadeIn(dl), Indicate(dot, color=WHITE, scale_factor=1.8),
                  run_time=1.0)
        self.wait(1.8)

        # ---- 4) จุด 2 -> 3 : เส้นตรง
        self.say("จุด 2→3 : เพิ่ม If → ฟลักซ์เพิ่มตาม → E เพิ่มเป็นเส้นตรง (E ∝ If)", color=OK)
        self.play(x.animate.set_value(0.14), run_time=1.3, rate_func=linear)
        l2 = Text("2", font_size=26, color=WHITE).next_to(ax.c2p(0.14, curve_up(0.14)), DR, buff=0.1)
        self.play(FadeIn(l2), Indicate(ch.cs[0], color=C_IF), run_time=0.5)
        self.play(x.animate.set_value(0.4), run_time=1.5, rate_func=linear)
        l3 = Text("3", font_size=26, color=WHITE).next_to(ax.c2p(0.4, curve_up(0.4)), DR, buff=0.1)
        self.play(FadeIn(l3), Indicate(ch.cs[1], color=C_PHI), Indicate(ch.cs[2], color=C_E), run_time=0.7)
        self.wait(1.0)

        # ---- 5) เลยจุด 3 : อิ่มตัว
        self.say("เลยจุด 3 : เหล็กอิ่มตัว — เพิ่ม If มากแค่ไหน ฟลักซ์ก็แทบไม่เพิ่ม E เลยแทบไม่ขึ้น (3→4)", color=WARN)
        s0 = (1 - 0.06) * 2.6
        dash = DashedLine(ax.c2p(0, curve_up(0)), ax.c2p(1.0 / s0 * 1.0, 1.06), color=GRAYTXT, stroke_width=3)
        dlab = VGroup(DashedLine(ORIGIN, RIGHT * 0.55, color=GRAYTXT, stroke_width=3),
                      Text("ถ้าไม่อิ่มตัว E จะพุ่งเป็นเส้นตรงต่อ", font_size=18, color=GRAYTXT)).arrange(RIGHT, buff=0.15)
        dlab.move_to(ax.c2p(0.80, 0.22))
        self.play(Create(dash), FadeIn(dlab), run_time=0.9)
        self.play(x.animate.set_value(1.2), run_time=3.2, rate_func=linear)
        l4 = Text("4", font_size=26, color=WHITE).next_to(ax.c2p(1.2, curve_up(1.2)), UP, buff=0.12)
        self.play(FadeIn(l4), ch.cs[1][0].animate.set_stroke(color=WARN), ch.cs[2][0].animate.set_stroke(color=WARN),
                  run_time=0.6)
        self.wait(2.0)

        # ---- 6) สรุป
        self.say("เคอร์ฟนี้เรียกว่า เคอร์ฟการอิ่มตัว (E กับ If ที่ n คงที่) — ฐานของทั้งบทนี้", color=OK, hold=2.6)
        self.exam("จุดออกสอบ 8-3: เพิ่ม If มากๆ แล้ว E ไม่เพิ่มตามเป็นเส้นตรง เพราะอะไร",
                  "เพราะแกนเหล็กอิ่มตัว ฟลักซ์ φ เพิ่มไม่ได้อีก (E = kφn โดย n คงที่) — E จึงแบนราบ")


# =============================================================== P03  หน้า 3
class P03_TestCircuit(Lesson):
    """รูป 8-1: วงจรวัดเคอร์ฟ (กระตุ้นแยก, ไม่ต่อโหลด) + ขาขึ้น 1->4 กับขาลง 4->5 (ฮิสเตอรีซิส)"""

    def construct(self):
        self.head("รูป 8-1 วงจรวัดเคอร์ฟอิ่มตัว", "หน้า 3 · รูปที่ 8-1")
        x = ValueTracker(0.0)
        branch = {"b": "up"}

        def E_of(v):
            return curve_up(v) if branch["b"] == "up" else curve_down(v)

        YT, YB = 1.5, -0.9
        # ---- วงจรทีละชิ้น
        self.say("วงจรวัดเคอร์ฟ: ฟิลด์ได้ไฟจากแหล่งแยก ปรับ If ด้วยรีโอสตาท — เครื่องหมุนเร็วคงที่ ไม่ต่อโหลด")
        sup = VGroup(wire((-6.4, YB), (-6.4, YT)), wire((-6.4, YT), (-5.0, YT)), wire((-6.4, YB), (-1.7, YB)),
                     meter([-6.4, 0.3], "DC", r=0.3))
        rheo = res_zig([-5.0, YT], [-5.0, YB], n=7)
        s_lab = tag("แหล่งจ่ายไฟตรง", size=18).move_to([-5.9, -1.4, 0])
        r_lab = tag("รีโอสตาท", size=18, color=C_R).move_to([-4.4, -1.4, 0])
        self.play(Create(sup), run_time=1.0)
        self.play(Create(rheo), FadeIn(s_lab), FadeIn(r_lab), run_time=0.9)

        def slider_y():
            return YB + (YT - YB) * 0.97 * (x.get_value() / 1.2) + 0.05

        slider = always_redraw(lambda: Arrow([-4.45, slider_y(), 0], [-4.88, slider_y(), 0], buff=0, color=YEL,
                                             tip_length=0.17, stroke_width=4, max_tip_length_to_length_ratio=0.5))
        sw = always_redraw(lambda: wire((-4.45, slider_y()), (-3.6, slider_y()), (-3.6, YT), (-3.2, YT), color=C_IF))
        amm = meter([-2.7, YT], "A", color=C_IF)
        a_lab = tag("แอมมิเตอร์ (วัด If)", size=18, color=C_IF).move_to([-2.7, 2.0, 0])
        top = wire((-2.43, YT), (-1.7, YT), color=C_IF)
        coil = coil_sym([-1.7, YT], [-1.7, YB], n=5, r=0.1, color=C_IF)
        f1 = tag("F1", size=20).move_to([-2.05, 1.0, 0])
        f2 = tag("F2", size=20).move_to([-2.05, -0.4, 0])
        c_lab = tag("ขดลวดฟิลด์", size=18, color=C_IF).move_to([-0.75, 0.3, 0])
        self.play(Create(slider), Create(sw), run_time=0.6)
        self.play(FadeIn(amm), FadeIn(a_lab), Create(top), Create(coil), FadeIn(f1), FadeIn(f2), FadeIn(c_lab),
                  run_time=1.2)
        arm = arm_sym([0.3, 0.3], r=0.42)
        wA = VGroup(wire((0.3, 0.72), (0.3, YT), (1.1, YT)), wire((0.3, -0.12), (0.3, YB), (1.1, YB)),
                    wire((1.1, YT), (1.1, 0.58)), wire((1.1, YB), (1.1, 0.02)), meter([1.1, 0.3], "V", color=C_E, r=0.28))
        a1 = tag("A1", size=18).move_to([0.62, 1.15, 0])
        a2 = tag("A2", size=18).move_to([0.62, -0.55, 0])
        vt = MathTex(r"V_t", font_size=32, color=WHITE).move_to([1.65, 0.3, 0])
        arm_lab = tag("อาร์เมเจอร์", size=18, color=C_E).move_to([0.3, -1.4, 0])
        self.play(FadeIn(arm), Create(wA), FadeIn(a1), FadeIn(a2), FadeIn(vt), FadeIn(arm_lab), run_time=1.2)
        self.wait(1.0)

        # ---- ไม่มีโหลด -> Vt = E
        self.say("ไม่ต่อโหลด → Ia = 0 → ไม่มีแรงดันตกในอาร์เมเจอร์ → โวลต์มิเตอร์อ่านได้ Vt = E ตรงๆ", color=OK)
        eq = MathTex(r"V_t", r"=", r"E", r"-", r"I_a", r"R_a", r"=", r"E", font_size=44).move_to([-3.0, -2.35, 0])
        eq[2].set_color(C_E), eq[7].set_color(C_E), eq[4].set_color(C_IA)
        self.play(Write(eq), run_time=1.3)
        self.play(Indicate(eq[4], color=WHITE), Indicate(eq[5], color=WHITE), run_time=0.8)
        self.wait(1.0)

        # ---- กราฟ + ขาขึ้น
        self.say("เพิ่ม If ทางเดียว: เลื่อนรีโอสตาทขึ้น → E ไต่ตามเส้นล่าง จุด 1 → 2 → 3 → 4", color=C_PHI)
        g = make_axes(pos=[2.9, -2.6], x_len=3.7, y_len=3.3, xmax=1.3, ymax=1.15)
        ax = g.ax
        self.play(FadeOut(eq), FadeOut(s_lab), FadeOut(r_lab), FadeOut(c_lab), FadeOut(arm_lab), Create(g), run_time=1.0)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), E_of(x.get_value())), color=C_E, radius=0.1))
        tr_up = always_redraw(lambda: ax.plot(curve_up, x_range=[0, max(x.get_value(), 0.002), 0.02], color=C_PHI,
                                              stroke_width=5))
        pts = {}
        for n, xv in ((2, 0.14), (3, 0.4), (4, 1.2)):
            pts[n] = Text(str(n), font_size=24, color=WHITE).next_to(ax.c2p(xv, curve_up(xv)), DR if n < 4 else UP, buff=0.1)
        l1 = Text("1", font_size=24, color=WHITE).next_to(ax.c2p(0, curve_up(0)), DL, buff=0.08)
        self.add(tr_up, dot)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(x.animate.set_value(1.2), run_time=4.2, rate_func=linear)
        tr_up.clear_updaters()
        self.play(*[FadeIn(p) for p in pts.values()], run_time=0.6)
        self.wait(1.0)

        # ---- ขาลง
        self.say("แล้วค่อยๆ ลด If: E ไม่ย้อนทางเดิม แต่วิ่งตามเส้นบน (4→5) — เรียกว่าฮิสเตอรีซิส", color=WARN)
        branch["b"] = "down"
        tr_dn = always_redraw(lambda: ax.plot(curve_down, x_range=[max(x.get_value(), 0.002), 1.2, 0.02],
                                              color=C_R, stroke_width=5))
        self.add(tr_dn)
        self.play(x.animate.set_value(0.0), run_time=4.2, rate_func=linear)
        tr_dn.clear_updaters()
        l5 = Text("5", font_size=24, color=WHITE).next_to(ax.c2p(0, curve_down(0)), LEFT, buff=0.12)
        gap = Line(ax.c2p(0, curve_up(0)), ax.c2p(0, curve_down(0)), color=WARN, stroke_width=6)
        self.play(FadeIn(l5), Create(gap), run_time=0.7)
        self.wait(1.0)

        # ---- เหล็กจำไว้ (โมเลกุล)
        self.say("ที่ If = 0 เหมือนกัน แต่จุด 5 สูงกว่าจุด 1 — เพราะเหล็กที่เคยอิ่มตัว 'จำ' แม่เหล็กไว้บางส่วน", color=WARN)
        slider.clear_updaters(); sw.clear_updaters()
        self.play(FadeOut(VGroup(sup, rheo, slider, sw, amm, a_lab, top, coil, f1, f2, arm, wA, a1, a2, vt)),
                  run_time=0.7)
        b1, d1 = domains(lambda: 0.12, w=2.5, h=1.3)
        b2, d2 = domains(lambda: 0.40, w=2.5, h=1.3)
        b1.move_to([-5.0, -0.2, 0]); b2.move_to([-1.4, -0.2, 0])
        t1 = Text("จุด 1 : เหล็กยังไม่เคยถูกอัดแม่เหล็ก", font_size=19, color=GRAYTXT).next_to(b1, DOWN, buff=0.2)
        t2 = Text("จุด 5 : หลังอิ่มตัวแล้วลด If เป็น 0", font_size=19, color=WARN).next_to(b2, DOWN, buff=0.2)
        t3 = Text("โมเลกุลหันตามกันค้างอยู่มากกว่า", font_size=19, color=WARN).next_to(t2, DOWN, buff=0.1)
        self.play(FadeIn(b1), FadeIn(d1), FadeIn(b2), FadeIn(d2), FadeIn(t1), FadeIn(t2), FadeIn(t3), run_time=1.0)
        self.wait(2.4)

        self.exam("จุดออกสอบ 8-3: ทำไมเส้นขาลง (4→5) ไม่ทับเส้นขาขึ้น (1→4)",
                  "ฮิสเตอรีซิสของวงจรแม่เหล็ก — เหล็กเก็บอำนาจแม่เหล็กไว้บางส่วน ที่ If = 0 จึงยังมี E ค้าง (จุด 5 > จุด 1)")
