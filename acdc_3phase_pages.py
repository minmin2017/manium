import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Palette for 3-Phase (Authoritative Visual Language)
PHASE_A  = "#EF5350"   # แดง (Phase a)
PHASE_B  = "#42A5F5"   # น้ำเงิน/ฟ้า (Phase b)
PHASE_C  = "#66BB6A"   # เขียว (Phase c)
VDC_COL  = "#FF9800"   # ส้ม (vdc / output)
PATH_ACT = "#FFD54F"   # เหลือง (Active current path)
WARN_NEG = "#E91E63"   # Magenta-red (Danger / Negative voltage)
DIODE_OFF= "#78909C"   # เทา ดับ
DIODE_ON = "#FFD54F"   # เหลือง นำกระแส


# ==============================================================================
# PAGE 1: Roadmap & Overview
# ==============================================================================
class Page01Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 1 · แผนที่การเรียนรู้")
        ttl = title("Three-Phase Bridge Rectifiers")
        cap = caption_top("ภาพรวมทั้งบท: เปลี่ยน AC 3 เฟส เป็น DC เรียบสูงด้วยไดโอด 6 ตัว")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        src_center = np.array([-4.5, -0.3, 0])
        lbl_src = Text("แหล่งจ่าย 3 เฟส", font_size=18, color=WHITE).move_to(src_center + UP * 1.5)
        dot_a = Dot(src_center + UP * 0.7, color=PHASE_A, radius=0.12)
        dot_b = Dot(src_center, color=PHASE_B, radius=0.12)
        dot_c = Dot(src_center + DOWN * 0.7, color=PHASE_C, radius=0.12)
        txt_a = Text("a", font_size=18, color=PHASE_A).next_to(dot_a, LEFT, buff=0.12)
        txt_b = Text("b", font_size=18, color=PHASE_B).next_to(dot_b, LEFT, buff=0.12)
        txt_c = Text("c", font_size=18, color=PHASE_C).next_to(dot_c, LEFT, buff=0.12)
        sources = VGroup(lbl_src, dot_a, dot_b, dot_c, txt_a, txt_b, txt_c)

        xs = [-1.8, -0.6, 0.6]
        top_y, bot_y, mid_y = 1.0, -1.6, -0.3
        rail_top = Line([-2.3, top_y, 0], [2.2, top_y, 0], color=EMF, stroke_width=4)
        rail_bot = Line([-2.3, bot_y, 0], [2.2, bot_y, 0], color=FIELD, stroke_width=4)
        lbl_vplus = MathTex("v^+", color=EMF, font_size=24).next_to(rail_top, UP, buff=0.08)
        lbl_vminus = MathTex("v^-", color=FIELD, font_size=24).next_to(rail_bot, DOWN, buff=0.08)

        wires, diodes = VGroup(), VGroup()
        colors = [PHASE_A, PHASE_B, PHASE_C]
        for i, x in enumerate(xs):
            y_in = 0.7 - i * 0.7
            w_in = Line(src_center + np.array([0, y_in, 0]), [x, y_in, 0], color=colors[i], stroke_width=2.5)
            w_vert = Line([x, top_y, 0], [x, bot_y, 0], color=GRAYTXT, stroke_width=2)
            wires.add(w_in, w_vert)
            dt = Triangle(color=WHITE, fill_opacity=0.85, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([x, (top_y + mid_y)/2, 0])
            db = Triangle(color=WHITE, fill_opacity=0.85, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([x, (mid_y + bot_y)/2, 0])
            diodes.add(dt, db)

        load_box = Rectangle(width=0.7, height=1.3, color=WHITE, fill_color=METAL, fill_opacity=0.3).move_to([2.2, mid_y, 0])
        load_txt = Text("โหลด", font_size=17, color=WHITE).move_to(load_box)
        w_load_t = Line([2.2, top_y, 0], load_box.get_top(), color=EMF)
        w_load_b = Line([2.2, bot_y, 0], load_box.get_bottom(), color=FIELD)
        vdc_lbl = MathTex("v_{dc}", color=VDC_COL, font_size=26).next_to(load_box, RIGHT, buff=0.2)
        bridge_grp = VGroup(sources, rail_top, rail_bot, lbl_vplus, lbl_vminus, wires, diodes, load_box, load_txt, w_load_t, w_load_b, vdc_lbl)

        cap2 = caption_top("โครงสร้าง 3 กิ่ง (Limbs) 6 ไดโอด: บนเลือกเฟสบวกสุด ล่างเลือกเฟสลบสุด")
        self.play(FadeIn(cap2), FadeIn(bridge_grp), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(bridge_grp), FadeOut(cap2), run_time=0.6)

        cap3 = caption_top("ผลลัพธ์: แรงดัน Line-to-Line 6 พัลส์ต่อคาบ เรียบสูงมาก")
        self.play(FadeIn(cap3), run_time=0.5)
        axes = Axes(x_range=[0, TAU + 0.1, PI/3], y_range=[-1.4, 1.4, 1], x_length=9.6, y_length=2.8, tips=False).move_to([0, -0.5, 0])
        w_a = axes.plot(lambda t: np.sin(t), x_range=[0, TAU], color=PHASE_A, stroke_opacity=0.35)
        w_b = axes.plot(lambda t: np.sin(t - 2*PI/3), x_range=[0, TAU], color=PHASE_B, stroke_opacity=0.35)
        w_c = axes.plot(lambda t: np.sin(t - 4*PI/3), x_range=[0, TAU], color=PHASE_C, stroke_opacity=0.35)
        def vdc_func(t):
            t_mod = t % (PI / 3)
            return np.sqrt(3) * np.sin(t_mod + PI/3) * 0.7
        envelope = axes.plot(vdc_func, x_range=[0, TAU], color=VDC_COL, stroke_width=4.0, use_smoothing=False)
        env_label = Text("vdc: 6-Pulse Envelope", font_size=18, color=VDC_COL).next_to(axes.c2p(PI, 1.2), UP, buff=0.1)
        graph_grp = VGroup(axes, w_a, w_b, w_c, envelope, env_label)
        self.play(Create(axes), Create(w_a), Create(w_b), Create(w_c), Create(envelope), FadeIn(env_label), run_time=1.5)
        self.wait(2.0)
        self.play(FadeOut(graph_grp), FadeOut(cap3), run_time=0.6)

        cap4 = caption_top("หัวใจสำคัญของวงจรเรียงกระแสบริดจ์ 3 เฟส")
        self.play(FadeIn(cap4), run_time=0.4)
        c1 = VGroup(Text("1. ไดโอด 6 ตัว (3 กิ่ง)", font_size=20, color=WHITE), Text("นำกระแสตัวละ 120° แต่สลับ switching ทุก 60°", font_size=17, color=GRAYTXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        c2 = VGroup(Text("2. เอาต์พุตคือแรงดันสาย (Line-to-Line)", font_size=20, color=WHITE), MathTex(r"v_{dc} = v^+ - v^- = v_{\text{line}}", color=VDC_COL, font_size=21)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        c3 = VGroup(Text("3. แรงดัน DC เฉลี่ยสูงและ Ripple ต่ำมาก", font_size=20, color=WHITE), MathTex(r"V_{dc} = \frac{3 V_M}{\pi} \approx 0.955 V_M", color=OK, font_size=21)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        box_grp = VGroup(c1, c2, c3).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0, -0.3, 0])
        self.play(FadeIn(box_grp, shift=UP * 0.2), run_time=1.0)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 2: Extra Limb & Top/Bottom Bank Selection
# ==============================================================================
class Page02Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 2 · เพิ่ม Limb อีกหนึ่งชุด")
        ttl = title("Three-Phase Diode Bridge Topology")
        cap = caption_top("มองเทียบกับ 1-phase bridge เดิม: เพิ่มอีก 1 กิ่ง (limb) เป็น 3 กิ่ง")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        xs = [-2.0, -0.6, 0.8]
        top_y, bot_y, mid_y = 1.1, -1.5, -0.2
        rail_top = Line([-2.8, top_y, 0], [2.2, top_y, 0], color=EMF, stroke_width=4)
        rail_bot = Line([-2.8, bot_y, 0], [2.2, bot_y, 0], color=FIELD, stroke_width=4)
        lbl_top_bank = Text("Top Bank (เลือกเฟสสูงสุด)", font_size=18, color=EMF).next_to(rail_top, UP, buff=0.15)
        lbl_bot_bank = Text("Bottom Bank (เลือกเฟสต่ำสุด)", font_size=18, color=FIELD).next_to(rail_bot, DOWN, buff=0.15)

        wires_1p = VGroup(
            Line([-2.0, top_y, 0], [-2.0, bot_y, 0], color=GRAYTXT, stroke_width=2),
            Line([-0.6, top_y, 0], [-0.6, bot_y, 0], color=GRAYTXT, stroke_width=2)
        )
        diodes_1p = VGroup(
            Triangle(color=WHITE, fill_opacity=0.8, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([-2.0, 0.45, 0]),
            Triangle(color=WHITE, fill_opacity=0.8, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([-2.0, -0.85, 0]),
            Triangle(color=WHITE, fill_opacity=0.8, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([-0.6, 0.45, 0]),
            Triangle(color=WHITE, fill_opacity=0.8, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([-0.6, -0.85, 0])
        )
        lbl_d1 = MathTex("D_1", font_size=20, color=WHITE).next_to(diodes_1p[0], RIGHT, buff=0.1)
        lbl_d4 = MathTex("D_4", font_size=20, color=WHITE).next_to(diodes_1p[1], RIGHT, buff=0.1)
        lbl_d2 = MathTex("D_2", font_size=20, color=WHITE).next_to(diodes_1p[2], RIGHT, buff=0.1)
        lbl_d5 = MathTex("D_5", font_size=20, color=WHITE).next_to(diodes_1p[3], RIGHT, buff=0.1)

        load_box = Rectangle(width=0.7, height=1.3, color=WHITE, fill_color=METAL, fill_opacity=0.3).move_to([2.2, mid_y, 0])
        load_txt = Text("Load", font_size=17, color=WHITE).move_to(load_box)
        w_lt = Line([2.2, top_y, 0], load_box.get_top(), color=EMF)
        w_lb = Line([2.2, bot_y, 0], load_box.get_bottom(), color=FIELD)
        vdc_arrow = Arrow([2.8, -1.0, 0], [2.8, 0.6, 0], color=VDC_COL, buff=0)
        vdc_txt = MathTex("v_{dc}", color=VDC_COL, font_size=24).next_to(vdc_arrow, RIGHT, buff=0.1)

        base_grp = VGroup(rail_top, rail_bot, lbl_top_bank, lbl_bot_bank, wires_1p, diodes_1p,
                          lbl_d1, lbl_d4, lbl_d2, lbl_d5, load_box, load_txt, w_lt, w_lb, vdc_arrow, vdc_txt)

        cap_limb = caption_top("เดิมใน 1-Phase มี 2 กิ่ง (4 ไดโอด) ขาบวกเลือกสูงสุด ขาลบเลือกต่ำสุด")
        self.play(FadeIn(cap_limb), FadeIn(base_grp), run_time=1.2)
        self.wait(1.8)

        self.play(FadeOut(cap_limb), run_time=0.3)
        cap_extra = caption_top("เพิ่ม limb ที่ 3 (ไดโอด D3, D6) รับเฟส c ทำให้วงจรรองรับระบบ 3 เฟสสมบูรณ์")
        w_3rd = Line([0.8, top_y, 0], [0.8, bot_y, 0], color=GRAYTXT, stroke_width=2)
        d_top3 = Triangle(color=WHITE, fill_opacity=0.9, fill_color=WARN).scale(0.16).rotate(PI/2).move_to([0.8, 0.45, 0])
        d_bot3 = Triangle(color=WHITE, fill_opacity=0.9, fill_color=WARN).scale(0.16).rotate(PI/2).move_to([0.8, -0.85, 0])
        lbl_d3 = MathTex("D_3", font_size=20, color=WARN).next_to(d_top3, RIGHT, buff=0.1)
        lbl_d6 = MathTex("D_6", font_size=20, color=WARN).next_to(d_bot3, RIGHT, buff=0.1)
        limb3_grp = VGroup(w_3rd, d_top3, d_bot3, lbl_d3, lbl_d6)

        self.play(FadeIn(cap_extra), FadeIn(limb3_grp, shift=RIGHT*0.2), run_time=1.2)
        self.wait(2.2)

        self.play(FadeOut(cap_extra), run_time=0.3)
        cap_rule = caption_top("กฎเหล็ก: Top bank (D1,D2,D3) ชนะที่แรงดันบวกสุด / Bottom bank ชนะที่ลบสุด")
        box_top = SurroundingRectangle(VGroup(diodes_1p[0], diodes_1p[2], d_top3), color=EMF, buff=0.15)
        box_bot = SurroundingRectangle(VGroup(diodes_1p[1], diodes_1p[3], d_bot3), color=FIELD, buff=0.15)
        self.play(FadeIn(cap_rule), Create(box_top), Create(box_bot), run_time=1.0)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 3: Conduction Sequence (120 deg conduction, 60 deg switching)
# ==============================================================================
class Page03Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 3 · ลำดับการนำกระแส")
        ttl = title("Diode Conduction Sequence")
        cap = caption_top("ลำดับการนำกระแส: ไดโอดบน D1,D2,D3 และ ไดโอดล่าง D4,D5,D6")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        cap_axes = caption_top("แต่ละช่วง 60° จะมีไดโอดบน 1 ตัว และไดโอดล่าง 1 ตัว นำกระแสพร้อมกันเสมอ")
        self.play(FadeIn(cap_axes), run_time=0.5)

        axes = Axes(x_range=[0, TAU + 0.1, PI/3], y_range=[-1.3, 1.3, 1], x_length=9.0, y_length=2.4, tips=False).move_to([0, 0.4, 0])
        wa = axes.plot(lambda t: np.sin(t), color=PHASE_A)
        wb = axes.plot(lambda t: np.sin(t - 2*PI/3), color=PHASE_B)
        wc = axes.plot(lambda t: np.sin(t - 4*PI/3), color=PHASE_C)
        lbl_va = Text("va", font_size=15, color=PHASE_A).next_to(axes.c2p(PI/2, 1.0), UP, buff=0.05)
        lbl_vb = Text("vb", font_size=15, color=PHASE_B).next_to(axes.c2p(PI/2 + 2*PI/3, 1.0), UP, buff=0.05)
        lbl_vc = Text("vc", font_size=15, color=PHASE_C).next_to(axes.c2p(PI/2 + 4*PI/3, 1.0), UP, buff=0.05)
        self.play(Create(axes), Create(wa), Create(wb), Create(wc), FadeIn(lbl_va), FadeIn(lbl_vb), FadeIn(lbl_vc), run_time=1.2)

        y_top_block = -1.3
        y_bot_block = -2.0
        dx = axes.c2p(PI/3, 0)[0] - axes.c2p(0, 0)[0]
        x0 = axes.c2p(PI/6, 0)[0]

        b_d1 = Rectangle(width=2*dx, height=0.5, color=WHITE, fill_color=PHASE_A, fill_opacity=0.4).move_to([x0 + dx, y_top_block, 0])
        txt_d1 = Text("D1 นำ 120°", font_size=16, color=WHITE).move_to(b_d1)
        b_d2 = Rectangle(width=2*dx, height=0.5, color=WHITE, fill_color=PHASE_B, fill_opacity=0.4).move_to([x0 + 3*dx, y_top_block, 0])
        txt_d2 = Text("D2 นำ 120°", font_size=16, color=WHITE).move_to(b_d2)

        b_d5 = Rectangle(width=dx, height=0.5, color=WHITE, fill_color=PHASE_B, fill_opacity=0.3).move_to([x0 + 0.5*dx, y_bot_block, 0])
        txt_d5 = Text("D5", font_size=16, color=WHITE).move_to(b_d5)
        b_d6 = Rectangle(width=2*dx, height=0.5, color=WHITE, fill_color=PHASE_C, fill_opacity=0.4).move_to([x0 + 2*dx, y_bot_block, 0])
        txt_d6 = Text("D6 นำ 120°", font_size=16, color=WHITE).move_to(b_d6)

        lbl_top_row = Text("Top:", font_size=16, color=EMF).next_to(b_d1, LEFT, buff=0.3)
        lbl_bot_row = Text("Bot:", font_size=16, color=FIELD).next_to(b_d5, LEFT, buff=0.3)

        gantt_grp = VGroup(b_d1, txt_d1, b_d2, txt_d2, b_d5, txt_d5, b_d6, txt_d6, lbl_top_row, lbl_bot_row)
        self.play(FadeIn(gantt_grp), run_time=1.2)
        self.wait(1.5)

        self.play(FadeOut(cap_axes), run_time=0.3)
        cap_insight = caption_top("จุดจำ: แต่ละตัวนำยาว 120° แต่ผลัดกันสลับ (switching) ทุกๆ 60°")
        self.play(FadeIn(cap_insight), run_time=0.4)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 4: Output Voltage Definition vdc = v+ - v-
# ==============================================================================
class Page04Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 4 · นิยามแรงดันเอาต์พุต")
        ttl = title("Load Voltage Definition: vdc = v+ - v-")
        cap = caption_top("Bridge ไม่ได้สร้างพลังงานใหม่ แต่เลือกผลต่างของสายที่บวกสุดกับลบสุด")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        eq_main = MathTex(r"v_{dc} = v^+ - v^-", font_size=38, color=VDC_COL).move_to([0, 1.2, 0])
        self.play(Write(eq_main), run_time=0.9)
        self.wait(1.0)

        cap_explain = caption_top("ขั้วบวกต่อกับเฟสสูงสุด v+ และขั้วลบต่อกับเฟสต่ำสุด v-")
        self.play(FadeIn(cap_explain), run_time=0.4)

        box_plus = RoundedRectangle(width=5.5, height=1.3, corner_radius=0.15, color=EMF, fill_color=EMF, fill_opacity=0.15).move_to([-3.0, -0.6, 0])
        txt_p1 = Text("v+ (Positive Rail)", font_size=20, color=EMF).move_to(box_plus.get_top() + DOWN * 0.3)
        txt_p2 = MathTex(r"= \max(v_a, v_b, v_c)", font_size=20, color=WHITE).next_to(txt_p1, DOWN, buff=0.15)
        grp_p = VGroup(box_plus, txt_p1, txt_p2)

        box_minus = RoundedRectangle(width=5.5, height=1.3, corner_radius=0.15, color=FIELD, fill_color=FIELD, fill_opacity=0.15).move_to([3.0, -0.6, 0])
        txt_m1 = Text("v- (Negative Rail)", font_size=20, color=FIELD).move_to(box_minus.get_top() + DOWN * 0.3)
        txt_m2 = MathTex(r"= \min(v_a, v_b, v_c)", font_size=20, color=WHITE).next_to(txt_m1, DOWN, buff=0.15)
        grp_m = VGroup(box_minus, txt_m1, txt_m2)

        self.play(FadeIn(grp_p), FadeIn(grp_m), run_time=1.0)
        self.wait(1.8)

        card_sub = VGroup(
            Text("ผลลัพธ์: โหลดเห็นแรงดันระหว่างสาย (Line-to-Line)", font_size=21, color=WHITE),
            MathTex(r"v_{dc} = v_{\text{line}} \in \{ v_{ab}, v_{ac}, v_{bc}, v_{ba}, v_{ca}, v_{cb} \}", font_size=22, color=OK)
        ).arrange(DOWN, buff=0.15).move_to([0, -2.1, 0])

        self.play(FadeIn(card_sub), run_time=0.8)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 5: Segment 1 - vdc = va - vb = vab (D1 and D5 conducting)
# ==============================================================================
class Page05Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 5 · ช่วงที่ได้ vdc = vab")
        ttl = title("Conduction Interval 1: vdc = vab")
        cap = caption_top("ช่วงที่ 1: เฟส a สูงสุด (D1 นำ) และเฟส b ต่ำสุด (D5 นำ)")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        src_c = np.array([-4.8, -0.4, 0])
        dot_a = Dot(src_c + UP * 0.7, color=PHASE_A, radius=0.1)
        dot_b = Dot(src_c, color=PHASE_B, radius=0.1)
        dot_c = Dot(src_c + DOWN * 0.7, color=PHASE_C, radius=0.1)
        t_a = Text("a", font_size=16, color=PHASE_A).next_to(dot_a, LEFT, buff=0.08)
        t_b = Text("b", font_size=16, color=PHASE_B).next_to(dot_b, LEFT, buff=0.08)
        t_c = Text("c", font_size=16, color=PHASE_C).next_to(dot_c, LEFT, buff=0.08)

        top_y, bot_y, mid_y = 1.0, -1.6, -0.3
        r_top = Line([-3.6, top_y, 0], [-0.2, top_y, 0], color=EMF, stroke_width=3.5)
        r_bot = Line([-3.6, bot_y, 0], [-0.2, bot_y, 0], color=FIELD, stroke_width=3.5)

        d1 = Triangle(color=WHITE, fill_opacity=1.0, fill_color=WARN).scale(0.15).rotate(PI/2).move_to([-3.2, (top_y+mid_y)/2, 0])
        d4 = Triangle(color=WHITE, fill_opacity=0.2, fill_color=GRAY).scale(0.15).rotate(PI/2).move_to([-3.2, (mid_y+bot_y)/2, 0])
        d2 = Triangle(color=WHITE, fill_opacity=0.2, fill_color=GRAY).scale(0.15).rotate(PI/2).move_to([-2.1, (top_y+mid_y)/2, 0])
        d5 = Triangle(color=WHITE, fill_opacity=1.0, fill_color=WARN).scale(0.15).rotate(PI/2).move_to([-2.1, (mid_y+bot_y)/2, 0])
        d3 = Triangle(color=WHITE, fill_opacity=0.2, fill_color=GRAY).scale(0.15).rotate(PI/2).move_to([-1.0, (top_y+mid_y)/2, 0])
        d6 = Triangle(color=WHITE, fill_opacity=0.2, fill_color=GRAY).scale(0.15).rotate(PI/2).move_to([-1.0, (mid_y+bot_y)/2, 0])

        w1 = Line([-3.2, top_y, 0], [-3.2, bot_y, 0], color=GRAYTXT, stroke_width=1.5)
        w2 = Line([-2.1, top_y, 0], [-2.1, bot_y, 0], color=GRAYTXT, stroke_width=1.5)
        w3 = Line([-1.0, top_y, 0], [-1.0, bot_y, 0], color=GRAYTXT, stroke_width=1.5)

        w_ina = Line(dot_a.get_center(), [-3.2, 0.3, 0], color=PHASE_A, stroke_width=2.5)
        w_inb = Line(dot_b.get_center(), [-2.1, -0.4, 0], color=PHASE_B, stroke_width=2.5)
        w_inc = Line(dot_c.get_center(), [-1.0, -1.1, 0], color=PHASE_C, stroke_width=1.5)

        l_box = Rectangle(width=0.5, height=1.1, color=WHITE, fill_color=METAL, fill_opacity=0.3).move_to([-0.2, mid_y, 0])
        w_lt = Line([-0.2, top_y, 0], l_box.get_top(), color=EMF)
        w_lb = Line([-0.2, bot_y, 0], l_box.get_bottom(), color=FIELD)

        lbl_d1 = MathTex("D_1", font_size=18, color=WARN).next_to(d1, RIGHT, buff=0.08)
        lbl_d5 = MathTex("D_5", font_size=18, color=WARN).next_to(d5, RIGHT, buff=0.08)

        br_grp = VGroup(dot_a, dot_b, dot_c, t_a, t_b, t_c, r_top, r_bot,
                        w1, w2, w3, w_ina, w_inb, w_inc, d1, d4, d2, d5, d3, d6,
                        l_box, w_lt, w_lb, lbl_d1, lbl_d5)

        axes = Axes(x_range=[0, TAU, PI/3], y_range=[-1.4, 1.4, 1], x_length=5.6, y_length=2.8, tips=False).move_to([3.4, -0.3, 0])
        wa = axes.plot(lambda t: np.sin(t), color=PHASE_A, stroke_opacity=0.6)
        wb = axes.plot(lambda t: np.sin(t - 2*PI/3), color=PHASE_B, stroke_opacity=0.6)
        wc = axes.plot(lambda t: np.sin(t - 4*PI/3), color=PHASE_C, stroke_opacity=0.3)

        shade = axes.get_area(wa, x_range=[PI/6, PI/2], bounded_graph=wb, color=YELLOW, opacity=0.35)
        lbl_shade = Text("ช่วงที่ 1 (60°)", font_size=16, color=YELLOW).next_to(axes.c2p(PI/3, 1.1), UP, buff=0.08)

        self.play(FadeIn(br_grp), Create(axes), Create(wa), Create(wb), Create(wc), run_time=1.2)
        self.play(FadeIn(shade), FadeIn(lbl_shade), run_time=0.8)

        cap_eq = caption_top("ขั้วบวกต่อกับ va, ขั้วลบต่อกับ vb -> vdc = va - vb = vab")
        eq = MathTex(r"v_{dc} = v_a - v_b = v_{ab}", font_size=26, color=VDC_COL).move_to([3.4, -2.1, 0])
        self.play(FadeIn(cap_eq), Write(eq), run_time=0.9)
        self.wait(2.2)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 6: Commutation to vac (D1 and D6 conducting)
# ==============================================================================
class Page06Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 6 · สลับไดโอดล่างเป็น D6")
        ttl = title("Switching to D6: vdc = vac")
        cap = caption_top("เมื่อเวลาผ่านไป 60°: เฟส c ตกต่ำกว่าเฟส b ไดโอด D6 จึงนำแทน D5")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        box_comm = RoundedRectangle(width=8.5, height=1.8, corner_radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=0.4).move_to([0, 0.8, 0])
        t_comm1 = Text("การสลับตัวนำกระแสฝั่ง Bottom Bank:", font_size=20, color=WARN).move_to(box_comm.get_top() + DOWN * 0.35)
        t_comm2 = Text("D1 ยังนำต่อ (Top Bank ไม่เปลี่ยน) | D6 เข้ามาแทน D5 (Bottom Bank สลับ)", font_size=18, color=GRAYTXT).next_to(t_comm1, DOWN, buff=0.15)
        grp_c = VGroup(box_comm, t_comm1, t_comm2)
        self.play(FadeIn(grp_c), run_time=0.9)

        cap_math = caption_top("ขั้วบวกยังคงต่อกับ va แต่ขั้วลบย้ายไปต่อกับ vc")
        self.play(FadeIn(cap_math), run_time=0.4)

        eq1 = MathTex(r"v^+ = v_a \quad (\text{via } D_1)", font_size=23, color=EMF).move_to([-3.0, -0.7, 0])
        eq2 = MathTex(r"v^- = v_c \quad (\text{via } D_6)", font_size=23, color=FIELD).move_to([3.0, -0.7, 0])
        eq_res = MathTex(r"v_{dc} = v_a - v_c = v_{ac}", font_size=30, color=VDC_COL).move_to([0, -1.6, 0])

        self.play(FadeIn(eq1), FadeIn(eq2), Write(eq_res), run_time=1.2)
        self.wait(1.8)

        card_rule = Text("ข้อสังเกต: ทุกครั้งที่มีการ switching จะเปลี่ยนเพียง 1 ตัวเสมอ!", font_size=19, color=OK).move_to([0, -2.4, 0])
        self.play(FadeIn(card_rule), run_time=0.6)
        self.wait(2.2)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 7: Switching Top Diode to D2 -> vdc = vbc
# ==============================================================================
class Page07Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 7 · สลับไดโอดบนเป็น D2")
        ttl = title("Switching to D2: vdc = vbc")
        cap = caption_top("เมื่อเฟส b ขึ้นสูงกว่าเฟส a: ไดโอด D2 นำแทน D1 ฝั่งบนสลับบ้าง")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        box_top_sw = RoundedRectangle(width=8.5, height=1.8, corner_radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=0.4).move_to([0, 0.8, 0])
        t_sw1 = Text("การสลับตัวนำกระแสฝั่ง Top Bank:", font_size=20, color=WARN).move_to(box_top_sw.get_top() + DOWN * 0.35)
        t_sw2 = Text("D2 เข้ามาแทน D1 (Top Bank สลับ) | D6 ยังคงนำต่อ (Bottom Bank ไม่เปลี่ยน)", font_size=18, color=GRAYTXT).next_to(t_sw1, DOWN, buff=0.15)
        grp_sw = VGroup(box_top_sw, t_sw1, t_sw2)
        self.play(FadeIn(grp_sw), run_time=0.9)

        cap_eq = caption_top("ขั้วบวกเปลี่ยนเป็น vb ขณะที่ขั้วลบยังคงเป็น vc")
        self.play(FadeIn(cap_eq), run_time=0.4)

        eq1 = MathTex(r"v^+ = v_b \quad (\text{via } D_2)", font_size=23, color=EMF).move_to([-3.0, -0.7, 0])
        eq2 = MathTex(r"v^- = v_c \quad (\text{via } D_6)", font_size=23, color=FIELD).move_to([3.0, -0.7, 0])
        eq_res = MathTex(r"v_{dc} = v_b - v_c = v_{bc}", font_size=30, color=VDC_COL).move_to([0, -1.6, 0])

        self.play(FadeIn(eq1), FadeIn(eq2), Write(eq_res), run_time=1.2)
        self.wait(1.8)

        summary_p7 = Text("ลำดับการทำงาน: สลับบน -> สลับล่าง -> สลับบน -> สลับล่าง ผลัดกันทีละ 60°", font_size=19, color=OK).move_to([0, -2.4, 0])
        self.play(FadeIn(summary_p7), run_time=0.6)
        self.wait(2.2)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 8: Six-Pulse Positive Envelope
# ==============================================================================
class Page08Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 8 · กราฟ 6 พัลส์สมบูรณ์")
        ttl = title("Six-Pulse Positive Envelope")
        cap = caption_top("รวมผลลัพธ์ทั้ง 6 ช่วง: vdc คือ positive envelope ของแรงดันสาย 6 เส้น")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        axes = Axes(x_range=[0, TAU + 0.1, PI/3], y_range=[-2.0, 2.0, 1], x_length=9.4, y_length=3.0, tips=False).move_to([0, 0.2, 0])

        v_lines = VGroup(
            axes.plot(lambda t: np.sqrt(3)*np.sin(t + PI/6), color="#EF5350", stroke_opacity=0.35),
            axes.plot(lambda t: np.sqrt(3)*np.sin(t + PI/6 - PI/3), color="#AB47BC", stroke_opacity=0.35),
            axes.plot(lambda t: np.sqrt(3)*np.sin(t + PI/6 - 2*PI/3), color="#42A5F5", stroke_opacity=0.35),
            axes.plot(lambda t: np.sqrt(3)*np.sin(t + PI/6 - 3*PI/3), color="#26C6DA", stroke_opacity=0.35),
            axes.plot(lambda t: np.sqrt(3)*np.sin(t + PI/6 - 4*PI/3), color="#66BB6A", stroke_opacity=0.35),
            axes.plot(lambda t: np.sqrt(3)*np.sin(t + PI/6 - 5*PI/3), color="#FFA726", stroke_opacity=0.35)
        )

        def env_func(t):
            t_mod = (t - PI/6) % (PI/3)
            return np.sqrt(3) * np.cos(t_mod - PI/6)

        envelope = axes.plot(env_func, x_range=[0, TAU], color=VDC_COL, stroke_width=4.5, use_smoothing=False)
        lbl_env = Text("vdc (Positive Envelope)", font_size=18, color=VDC_COL).next_to(axes.c2p(PI, 1.75), UP, buff=0.1)

        self.play(Create(axes), Create(v_lines), run_time=1.2)
        self.play(Create(envelope), FadeIn(lbl_env), run_time=1.5)

        cap_facts = caption_top("คุณสมบัติสำคัญ: Line voltage สูงกว่า Phase voltage อยู่ sqrt(3) เท่า")
        self.play(FadeIn(cap_facts), run_time=0.4)

        facts = VGroup(
            Text("1. แรงดัน Line-to-Line มีแอมพลิจูดสูงเป็น sqrt(3) เท่าของ Phase voltage", font_size=18, color=WHITE),
            Text("2. มุมเฟสของ Line voltage นำหน้า Phase voltage อยู่ 30°", font_size=18, color=WHITE),
            Text("3. vdc ประกอบจากส่วนยอดของทั้ง 6 เส้น เกิดเป็น 6-pulse DC ripple ความถี่ 6 เท่า", font_size=18, color=OK)
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([0, -2.1, 0])

        self.play(FadeIn(facts), run_time=1.0)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 9: Average DC Output Voltage Integration
# ==============================================================================
class Page09Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 9 · การหาค่าเฉลี่ย Vdc")
        ttl = title("Average Output Voltage: Vdc = 3VM/pi")
        cap = caption_top("เนื่องจากรูปคลื่นซ้ำกันทุก 60° (pi/3) จึงอินทิเกรตหาค่าเฉลี่ยเพียง 1 ช่วง")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        eq1 = MathTex(r"V_{dc} \cdot \frac{\pi}{3} = \int_{\pi/3}^{2\pi/3} V_M \sin(\omega t) \, d(\omega t)", font_size=28, color=WHITE).move_to([0, 1.2, 0])
        self.play(Write(eq1), run_time=1.0)
        self.wait(1.2)

        cap_step = caption_top("ผลการอินทิเกรต [ -cos(wt) ] จาก pi/3 ถึง 2pi/3 ได้ค่าเท่ากับ 1")
        self.play(FadeIn(cap_step), run_time=0.4)

        eq2 = MathTex(r"\int_{\pi/3}^{2\pi/3} \sin(\omega t) \, d(\omega t) = \left[ -\cos(\omega t) \right]_{\pi/3}^{2\pi/3} = -\left(-\frac{1}{2}\right) - \left(-\frac{1}{2}\right) = 1", font_size=24, color=GRAYTXT).move_to([0, 0.2, 0])
        self.play(FadeIn(eq2), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(cap_step), run_time=0.3)
        cap_final = caption_top("สูตรสำเร็จ: Vdc = 3VM/pi โดย VM คือ peak line-to-line voltage")
        self.play(FadeIn(cap_final), run_time=0.4)

        box_res = RoundedRectangle(width=8.0, height=1.6, corner_radius=0.15, color=OK, fill_color=BLACK, fill_opacity=0.5).move_to([0, -1.4, 0])
        eq_final = MathTex(r"V_{dc} = \frac{3}{\pi} V_M \approx 0.955 V_M", font_size=32, color=OK).move_to(box_res.get_center() + UP * 0.25)
        t_note = Text("หมายเหตุ: สำหรับวงจรนี้ Vrms แทบจะเท่ากับ Vdc (ต่างกันเพียง 0.2%)", font_size=17, color=WHITE).move_to(box_res.get_center() + DOWN * 0.35)
        grp_f = VGroup(box_res, eq_final, t_note)

        self.play(FadeIn(grp_f), run_time=1.0)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 10: Reference Diagrams - Waveforms and Currents
# ==============================================================================
class Page10Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 10 · แหล่งจ่าย -> ไดโอด -> vo -> ia", size=15)
        ttl = title("3-Phase Bridge: Causal Current Simulator", size=22)
        cap = caption_top("จำลองการทำงานจริง: van, vbn, vcn กำหนดไดโอด -> เกิด vo และ ia ทีละ 60°", size=17)
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.3)

        # -------------------------------------------------------------
        # 1. Left 38%: 6-Diode Bridge Circuit (x center ~ -4.3)
        # -------------------------------------------------------------
        top_y, bot_y, mid_y = 1.3, -2.1, -0.4
        r_top = Line([-6.4, top_y, 0], [-2.0, top_y, 0], color=EMF, stroke_width=3)
        r_bot = Line([-6.4, bot_y, 0], [-2.0, bot_y, 0], color=FIELD, stroke_width=3)
        lbl_vp = MathTex("v^+", color=EMF, font_size=18).next_to(r_top, UP, buff=0.05)
        lbl_vm = MathTex("v^-", color=FIELD, font_size=18).next_to(r_bot, DOWN, buff=0.05)

        xs = [-5.4, -4.2, -3.0]
        src_dots = [
            Dot([-6.2, 0.5, 0], color=PHASE_A, radius=0.09),
            Dot([-6.2, -0.4, 0], color=PHASE_B, radius=0.09),
            Dot([-6.2, -1.3, 0], color=PHASE_C, radius=0.09)
        ]
        lbl_a = Text("a", font_size=14, color=PHASE_A).next_to(src_dots[0], LEFT, buff=0.05)
        lbl_b = Text("b", font_size=14, color=PHASE_B).next_to(src_dots[1], LEFT, buff=0.05)
        lbl_c = Text("c", font_size=14, color=PHASE_C).next_to(src_dots[2], LEFT, buff=0.05)

        w_ina = Line(src_dots[0].get_center(), [xs[0], 0.5, 0], color=PHASE_A, stroke_width=2)
        w_inb = Line(src_dots[1].get_center(), [xs[1], -0.4, 0], color=PHASE_B, stroke_width=2)
        w_inc = Line(src_dots[2].get_center(), [xs[2], -1.3, 0], color=PHASE_C, stroke_width=2)

        wires = VGroup()
        for x in xs:
            wires.add(Line([x, top_y, 0], [x, bot_y, 0], color=GRAYTXT, stroke_width=1.5))

        d_t = [
            Triangle(color=WHITE, fill_opacity=0.3, fill_color=GRAY).scale(0.12).rotate(PI/2).move_to([xs[0], (top_y+0.5)/2, 0]),
            Triangle(color=WHITE, fill_opacity=0.3, fill_color=GRAY).scale(0.12).rotate(PI/2).move_to([xs[1], (top_y-0.4)/2, 0]),
            Triangle(color=WHITE, fill_opacity=0.3, fill_color=GRAY).scale(0.12).rotate(PI/2).move_to([xs[2], (top_y-1.3)/2, 0])
        ]
        d_b = [
            Triangle(color=WHITE, fill_opacity=0.3, fill_color=GRAY).scale(0.12).rotate(PI/2).move_to([xs[0], (0.5+bot_y)/2, 0]),
            Triangle(color=WHITE, fill_opacity=0.3, fill_color=GRAY).scale(0.12).rotate(PI/2).move_to([xs[1], (-0.4+bot_y)/2, 0]),
            Triangle(color=WHITE, fill_opacity=0.3, fill_color=GRAY).scale(0.12).rotate(PI/2).move_to([xs[2], (-1.3+bot_y)/2, 0])
        ]

        t_d1 = MathTex("D_1", font_size=15, color=WHITE).next_to(d_t[0], RIGHT, buff=0.04)
        t_d3 = MathTex("D_3", font_size=15, color=WHITE).next_to(d_t[1], RIGHT, buff=0.04)
        t_d5 = MathTex("D_5", font_size=15, color=WHITE).next_to(d_t[2], RIGHT, buff=0.04)
        t_d4 = MathTex("D_4", font_size=15, color=WHITE).next_to(d_b[0], RIGHT, buff=0.04)
        t_d6 = MathTex("D_6", font_size=15, color=WHITE).next_to(d_b[1], RIGHT, buff=0.04)
        t_d2 = MathTex("D_2", font_size=15, color=WHITE).next_to(d_b[2], RIGHT, buff=0.04)

        l_box = Rectangle(width=0.4, height=1.0, color=WHITE, fill_color=METAL, fill_opacity=0.3).move_to([-2.0, mid_y, 0])
        w_lt = Line([-2.0, top_y, 0], l_box.get_top(), color=EMF)
        w_lb = Line([-2.0, bot_y, 0], l_box.get_bottom(), color=FIELD)
        l_txt = Text("Load", font_size=13, color=WHITE).move_to(l_box)

        circuit_grp = VGroup(r_top, r_bot, lbl_vp, lbl_vm, *src_dots, lbl_a, lbl_b, lbl_c,
                              w_ina, w_inb, w_inc, wires, *d_t, *d_b,
                              t_d1, t_d3, t_d5, t_d4, t_d6, t_d2, l_box, w_lt, w_lb, l_txt)
        self.play(FadeIn(circuit_grp), run_time=0.8)

        # -------------------------------------------------------------
        # 2. Centre 32%: Synchronized Dual Waveform Strips (x ~ 0.5)
        # -------------------------------------------------------------
        ax_s = Axes(x_range=[PI/6, 13*PI/6, PI/3], y_range=[-1.2, 1.2, 1], x_length=3.8, y_length=1.4, tips=False).move_to([0.5, 1.15, 0])
        lbl_ax_s = Text("แรงดันแหล่งจ่าย van, vbn, vcn", font_size=13, color=WHITE).next_to(ax_s, UP, buff=0.06)

        c_van = ax_s.plot(lambda t: np.sin(t), x_range=[PI/6, 13*PI/6], color=PHASE_A, stroke_width=2.2)
        c_vbn = ax_s.plot(lambda t: np.sin(t - 2*PI/3), x_range=[PI/6, 13*PI/6], color=PHASE_B, stroke_width=2.2)
        c_vcn = ax_s.plot(lambda t: np.sin(t + 2*PI/3), x_range=[PI/6, 13*PI/6], color=PHASE_C, stroke_width=2.2)

        ax_v = Axes(x_range=[PI/6, 13*PI/6, PI/3], y_range=[0, 2.0, 1], x_length=3.8, y_length=1.4, tips=False).move_to([0.5, -0.95, 0])
        lbl_ax_v = MathTex(r"v_o = v^+ - v^- 	ext{ (Line Voltage)}", font_size=14, color=VDC_COL).next_to(ax_v, UP, buff=0.06)

        def vo_func(t):
            t_mod = (t - PI/6) % (PI/3)
            return np.sqrt(3) * np.sin(t_mod + PI/3) * 0.95
        c_vo = ax_v.plot(vo_func, x_range=[PI/6, 13*PI/6], color=VDC_COL, stroke_width=2.5, use_smoothing=False)

        cursor = DashedLine([ax_s.c2p(PI/3, 0)[0], ax_s.c2p(PI/3, 1.15)[1], 0],
                            [ax_v.c2p(PI/3, 0)[0], ax_v.c2p(PI/3, 0.05)[1], 0],
                            color=YELLOW, stroke_width=2.2)

        h_van = Dot(ax_s.c2p(PI/3, np.sin(PI/3)), color=PHASE_A, radius=0.08)
        h_vbn = Dot(ax_s.c2p(PI/3, np.sin(PI/3 - 2*PI/3)), color=PHASE_B, radius=0.08)
        h_vcn = Dot(ax_s.c2p(PI/3, np.sin(PI/3 + 2*PI/3)), color=PHASE_C, radius=0.08)

        self.play(Create(ax_s), FadeIn(lbl_ax_s), Create(c_van), Create(c_vbn), Create(c_vcn),
                  Create(ax_v), FadeIn(lbl_ax_v), Create(c_vo),
                  Create(cursor), FadeIn(h_van), FadeIn(h_vbn), FadeIn(h_vcn), run_time=1.0)

        # -------------------------------------------------------------
        # 3. Right 30%: Live Truth Panel (x ~ 4.9)
        # -------------------------------------------------------------
        p_box = RoundedRectangle(width=4.3, height=4.2, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.7).move_to([4.9, 0.1, 0])
        p_ttl = Text("ตารางสถานะจริง (Truth Panel)", font_size=15, color=WHITE).move_to(p_box.get_top() + DOWN * 0.28)
        self.play(FadeIn(p_box), FadeIn(p_ttl), run_time=0.5)

        steps_data = [
            {
                "deg": "30°–90°", "t_mid": PI/3,
                "max_p": "a", "max_c": PHASE_A, "d_top": "D1", "dt_idx": 0,
                "min_p": "b", "min_c": PHASE_B, "d_bot": "D6", "db_idx": 1,
                "mid_p": "c",
                "vo": r"v_{an} - v_{bn} = v_{ab}", "ia_txt": "+Io (จ่ายออกจากสาย a)",
                "path": [[xs[0], 0.5, 0], [xs[0], top_y, 0], [-2.0, top_y, 0], [-2.0, bot_y, 0], [xs[1], bot_y, 0], [xs[1], -0.4, 0]],
                "comm_note": "จุดตัด 90°: vcn ลดต่ำกว่า vbn -> Commutation สลับ D6 เป็น D2"
            },
            {
                "deg": "90°–150°", "t_mid": 2*PI/3,
                "max_p": "a", "max_c": PHASE_A, "d_top": "D1", "dt_idx": 0,
                "min_p": "c", "min_c": PHASE_C, "d_bot": "D2", "db_idx": 2,
                "mid_p": "b",
                "vo": r"v_{an} - v_{cn} = v_{ac}", "ia_txt": "+Io (ยังคงไหลผ่าน D1)",
                "path": [[xs[0], 0.5, 0], [xs[0], top_y, 0], [-2.0, top_y, 0], [-2.0, bot_y, 0], [xs[2], bot_y, 0], [xs[2], -1.3, 0]],
                "comm_note": "จุดตัด 150°: vbn สูงแซง van -> Commutation สลับ D1 เป็น D3"
            },
            {
                "deg": "150°–210°", "t_mid": PI,
                "max_p": "b", "max_c": PHASE_B, "d_top": "D3", "dt_idx": 1,
                "min_p": "c", "min_c": PHASE_C, "d_bot": "D2", "db_idx": 2,
                "mid_p": "a",
                "vo": r"v_{bn} - v_{cn} = v_{bc}", "ia_txt": "0 (D1 และ D4 ดับสนิท)",
                "path": [[xs[1], -0.4, 0], [xs[1], top_y, 0], [-2.0, top_y, 0], [-2.0, bot_y, 0], [xs[2], bot_y, 0], [xs[2], -1.3, 0]],
                "comm_note": "จุดตัด 210°: van ลดต่ำกว่า vcn -> Commutation สลับ D2 เป็น D4"
            },
            {
                "deg": "210°–270°", "t_mid": 4*PI/3,
                "max_p": "b", "max_c": PHASE_B, "d_top": "D3", "dt_idx": 1,
                "min_p": "a", "min_c": PHASE_A, "d_bot": "D4", "db_idx": 0,
                "mid_p": "c",
                "vo": r"v_{bn} - v_{an} = v_{ba}", "ia_txt": "-Io (ไหลกลับเข้าสาย a ผ่าน D4)",
                "path": [[xs[1], -0.4, 0], [xs[1], top_y, 0], [-2.0, top_y, 0], [-2.0, bot_y, 0], [xs[0], bot_y, 0], [xs[0], 0.5, 0]],
                "comm_note": "จุดตัด 270°: vcn สูงแซง vbn -> Commutation สลับ D3 เป็น D5"
            },
            {
                "deg": "270°–330°", "t_mid": 5*PI/3,
                "max_p": "c", "max_c": PHASE_C, "d_top": "D5", "dt_idx": 2,
                "min_p": "a", "min_c": PHASE_A, "d_bot": "D4", "db_idx": 0,
                "mid_p": "b",
                "vo": r"v_{cn} - v_{an} = v_{ca}", "ia_txt": "-Io (ยังคงไหลกลับเข้า D4)",
                "path": [[xs[2], -1.3, 0], [xs[2], top_y, 0], [-2.0, top_y, 0], [-2.0, bot_y, 0], [xs[0], bot_y, 0], [xs[0], 0.5, 0]],
                "comm_note": "จุดตัด 330°: vbn ลดต่ำกว่า van -> Commutation สลับ D4 เป็น D6"
            },
            {
                "deg": "330°–390°", "t_mid": 2*PI,
                "max_p": "c", "max_c": PHASE_C, "d_top": "D5", "dt_idx": 2,
                "min_p": "b", "min_c": PHASE_B, "d_bot": "D6", "db_idx": 1,
                "mid_p": "a",
                "vo": r"v_{cn} - v_{bn} = v_{cb}", "ia_txt": "0 (D1 และ D4 ดับสนิท)",
                "path": [[xs[2], -1.3, 0], [xs[2], top_y, 0], [-2.0, top_y, 0], [-2.0, bot_y, 0], [xs[1], bot_y, 0], [xs[1], -0.4, 0]],
                "comm_note": "จุดตัด 390° (30°): van สูงแซง vcn -> วนกลับมาเปิด D1"
            }
        ]

        active_path = VMobject()
        current_panel = VGroup()

        for idx, s in enumerate(steps_data, 1):
            t_x = s["t_mid"]
            cap_step = caption_top(f"ช่วงที่ {idx} ({s['deg']}): เฟส {s['max_p']} สูงสุด -> เปิด {s['d_top']} / เฟส {s['min_p']} ต่ำสุด -> เปิด {s['d_bot']}", size=17)
            self.play(FadeIn(cap_step), run_time=0.3)

            for d in d_t + d_b:
                d.set_fill(GRAY, opacity=0.3)
            d_t[s["dt_idx"]].set_fill(PATH_ACT, opacity=1.0)
            d_b[s["db_idx"]].set_fill(PATH_ACT, opacity=1.0)

            new_path = VMobject()
            new_path.set_points_as_corners(s["path"])
            new_path.set_color(PATH_ACT).set_stroke(width=4.0)

            cx = ax_s.c2p(t_x, 0)[0]
            new_cur = DashedLine([cx, 1.85, 0], [cx, -1.65, 0], color=YELLOW, stroke_width=2.2)
            new_h_van = Dot(ax_s.c2p(t_x, np.sin(t_x)), color=PHASE_A, radius=0.08)
            new_h_vbn = Dot(ax_s.c2p(t_x, np.sin(t_x - 2*PI/3)), color=PHASE_B, radius=0.08)
            new_h_vcn = Dot(ax_s.c2p(t_x, np.sin(t_x + 2*PI/3)), color=PHASE_C, radius=0.08)

            r1 = Text(f"ช่วงที่ {idx} ({s['deg']})", font_size=15, color=YELLOW).move_to([4.9, 1.4, 0])
            r2 = Text(f"• สูงสุด: เฟส {s['max_p']} -> เปิดบน {s['d_top']}", font_size=13, color=s['max_c']).move_to([4.9, 0.95, 0])
            r3 = Text(f"• ต่ำสุด: เฟส {s['min_p']} -> เปิดล่าง {s['d_bot']}", font_size=13, color=s['min_c']).move_to([4.9, 0.55, 0])
            r4 = Text(f"• กลาง: เฟส {s['mid_p']} (ไม่นำกระแส)", font_size=12, color=GRAYTXT).move_to([4.9, 0.15, 0])
            r5 = MathTex(s["vo"], font_size=16, color=VDC_COL).move_to([4.9, -0.35, 0])
            r6 = Text(f"กระแส ia: {s['ia_txt']}", font_size=12, color=WHITE).move_to([4.9, -0.85, 0])
            new_p = VGroup(r1, r2, r3, r4, r5, r6)

            self.play(
                Transform(active_path, new_path),
                Transform(cursor, new_cur),
                Transform(h_van, new_h_van),
                Transform(h_vbn, new_h_vbn),
                Transform(h_vcn, new_h_vcn),
                Transform(current_panel, new_p),
                run_time=0.7
            )
            self.wait(1.5)

            if idx <= 5:
                t_cross = (idx * PI/3) + PI/6
                cx_cross = ax_s.c2p(t_cross, 0)[0]
                cur_cross = DashedLine([cx_cross, 1.85, 0], [cx_cross, -1.65, 0], color=WARN_NEG, stroke_width=2.2)
                cap_cross = caption_top(s["comm_note"], size=16, color=WARN_NEG)
                self.play(Transform(cursor, cur_cross), Transform(cap_step, cap_cross), run_time=0.5)
                self.wait(1.2)

            self.play(FadeOut(cap_step), run_time=0.2)

        self.play(FadeOut(active_path), FadeOut(current_panel), FadeOut(p_box), FadeOut(p_ttl),
                  FadeOut(cursor), FadeOut(h_van), FadeOut(h_vbn), FadeOut(h_vcn),
                  FadeOut(ax_v), FadeOut(c_vo), FadeOut(lbl_ax_v), run_time=0.5)

        # -------------------------------------------------------------
        # 4. Deep-dive: ia Waveform Analysis (+Io / 0 / -Io)
        # -------------------------------------------------------------
        cap_ia = caption_top("วิเคราะห์กระแสสาย ia: สลับไหลออก (+Io), ศูนย์ (0), และไหลกลับ (-Io)", size=17)
        self.play(FadeIn(cap_ia), run_time=0.4)

        ax_ia = Axes(x_range=[PI/6, 13*PI/6, PI/3], y_range=[-1.2, 1.2, 1], x_length=3.8, y_length=1.4, tips=False).move_to([0.5, -0.95, 0])
        lbl_ax_ia = MathTex(r"i_a 	ext{ (Phase a Current)}", font_size=14, color=PHASE_A).next_to(ax_ia, UP, buff=0.06)

        p_ia = ax_ia.plot_line_graph(
            x_values=[PI/6, PI/6, 5*PI/6, 5*PI/6, 7*PI/6, 7*PI/6, 11*PI/6, 11*PI/6, 13*PI/6],
            y_values=[0, 0.7, 0.7, 0, 0, -0.7, -0.7, 0, 0],
            line_color=PHASE_A, add_vertex_dots=False
        )
        self.play(Create(ax_ia), Create(p_ia), FadeIn(lbl_ax_ia), run_time=0.8)

        c_box = RoundedRectangle(width=4.3, height=3.8, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.7).move_to([4.9, 0.1, 0])
        t1 = Text("นิยามเครื่องหมายกระแส ia:", font_size=15, color=YELLOW).move_to([4.9, 1.5, 0])
        t2 = Text("1. D1 นำ 120°: ia = +Io\n   กระแสไหลออกจากขั้ว a เข้าบริดจ์", font_size=13, color=WHITE).move_to([4.9, 0.9, 0])
        t3 = Text("2. ว่าง 60°: ia = 0\n   ทั้ง D1 และ D4 ดับสนิท", font_size=13, color=GRAYTXT).move_to([4.9, 0.2, 0])
        t4 = Text("3. D4 นำ 120°: ia = -Io\n   กระแสไหลจากบริดจ์กลับเข้าขั้ว a", font_size=13, color=WHITE).move_to([4.9, -0.5, 0])
        t5 = Text("โหลด R: รูปคลื่นหยักตาม vo\nโหลดกรอง L: รูปคลื่นเหลี่ยมเรียบ", font_size=12, color=OK).move_to([4.9, -1.2, 0])
        ia_card = VGroup(c_box, t1, t2, t3, t4, t5)
        self.play(FadeIn(ia_card), run_time=0.6)

        d_t[0].set_fill(PATH_ACT, opacity=1.0)
        box_d1 = SurroundingRectangle(d_t[0], color=WARN_NEG, buff=0.06)
        self.play(Create(box_d1), run_time=0.4)
        self.wait(1.5)

        d_t[0].set_fill(GRAY, opacity=0.3)
        self.play(FadeOut(box_d1), run_time=0.3)
        self.wait(1.2)

        d_b[0].set_fill(PATH_ACT, opacity=1.0)
        box_d4 = SurroundingRectangle(d_b[0], color=WARN_NEG, buff=0.06)
        self.play(Create(box_d4), run_time=0.4)
        self.wait(1.5)

        self.play(FadeOut(box_d4), FadeOut(ia_card), FadeOut(cap_ia), FadeOut(circuit_grp),
                  FadeOut(ax_s), FadeOut(lbl_ax_s), FadeOut(c_van), FadeOut(c_vbn), FadeOut(c_vcn),
                  FadeOut(ax_ia), FadeOut(lbl_ax_ia), FadeOut(p_ia), run_time=0.6)

        # -------------------------------------------------------------
        # 5. Recap Card & Retrieval Q&A
        # -------------------------------------------------------------
        cap_end = caption_top("สรุปจำแม่นยำ & คำถามเช็กความเข้าใจ", size=18)
        self.play(FadeIn(cap_end), run_time=0.4)

        card_recap = VGroup(
            Text("• D1 นำ -> ia เป็นบวก (+Io) : กระแสจ่ายออกจากสาย a", font_size=16, color=WHITE),
            Text("• D4 นำ -> ia เป็นลบ (-Io) : กระแสรับกลับเข้าสาย a", font_size=16, color=WHITE),
            Text("• ไม่ใช่ทั้ง D1/D4 -> ia เป็นศูนย์ (0) : ไดโอดกิ่ง a ดับสนิท", font_size=16, color=WHITE),
            Text("• แต่ละไดโอดนำ 120° แต่สลับผลัดกะกันทุก 60° เมื่อแรงดันเฟสตัดกัน", font_size=16, color=OK)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        q_box = RoundedRectangle(width=9.6, height=1.6, corner_radius=0.15, color=WARN, fill_color=BLACK, fill_opacity=0.5)
        q_txt = Text("คำถาม: ช่วงที่ D3 และ D4 นำพร้อมกัน vo เท่ากับเท่าไร และ ia มีค่าเป็นอย่างไร?", font_size=16, color=WARN).move_to(q_box.get_top() + DOWN * 0.35)
        a_txt = Text("เฉลย: vo = vba และ ia < 0 (ติดลบ) เพราะกระแสไหลกลับเข้าสาย a ผ่าน D4!", font_size=16, color=OK).next_to(q_txt, DOWN, buff=0.18)
        q_grp = VGroup(q_box, q_txt, a_txt)

        final_grp = VGroup(card_recap, q_grp).arrange(DOWN, buff=0.35).move_to([0, -0.3, 0])
        self.play(FadeIn(final_grp), run_time=1.0)
        self.wait(3.0)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 11: Thyristor (SCR) Bridge Rectifier Introduction
# ==============================================================================
class Page11Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 11 · วงจรคอนเวอร์เตอร์ไทริสเตอร์")
        ttl = title("Thyristor (SCR) Bridge Rectifier")
        cap = caption_top("เปลี่ยนไดโอดทั้ง 6 ตัว เป็น Thyristor (SCR) เพื่อควบคุมแรงดันขาออกได้")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        cap_comp = caption_top("ความต่างสำคัญ: Diode นำกระแสทันที vs Thyristor ต้องรอยิงเกต (Gate Pulse)")
        self.play(FadeIn(cap_comp), run_time=0.4)

        box_d = RoundedRectangle(width=5.8, height=2.4, corner_radius=0.15, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.4).move_to([-3.2, 0.1, 0])
        t_d1 = Text("Diode Bridge (Uncontrolled)", font_size=20, color=WHITE).move_to(box_d.get_top() + DOWN * 0.35)
        t_d2 = Text("• นำกระแสทันทีเมื่อ Forward-biased\n• ควบคุมแรงดันไม่ได้\n• Vdc มีค่าคงที่เสมอ", font_size=17, color=GRAYTXT).next_to(t_d1, DOWN, buff=0.2)
        grp_d = VGroup(box_d, t_d1, t_d2)

        box_t = RoundedRectangle(width=5.8, height=2.4, corner_radius=0.15, color=WARN, fill_color=BLACK, fill_opacity=0.4).move_to([3.2, 0.1, 0])
        t_t1 = Text("Thyristor Bridge (Controlled)", font_size=20, color=WARN).move_to(box_t.get_top() + DOWN * 0.35)
        t_t2 = Text("• ต้องได้รับสัญญาณ Gate ก่อนจึงจะนำ\n• หน่วงมุมจุดชนวน (alpha) ได้\n• ควบคุมระดับ Vdc เฉลี่ยได้อย่างอิสระ", font_size=17, color=WHITE).next_to(t_t1, DOWN, buff=0.2)
        grp_t = VGroup(box_t, t_t1, t_t2)

        self.play(FadeIn(grp_d), FadeIn(grp_t), run_time=1.2)
        self.wait(2.0)

        card_gate = Text("คีย์เวิร์ด: มุมหน่วงการยิงเกตเรียกว่า Firing Angle (alpha)", font_size=20, color=OK).move_to([0, -2.1, 0])
        self.play(FadeIn(card_gate), run_time=0.7)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 12: Firing Angle Alpha Definition
# ==============================================================================
class Page12Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 12 · นิยามมุมจุดชนวน alpha")
        ttl = title("Firing Angle alpha Measurement")
        cap = caption_top("ข้อควรระวังสำคัญที่สุด: วัด alpha จากจุดตัดธรรมชาติ (Natural Crossover)")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        axes = Axes(x_range=[0, PI, PI/6], y_range=[-0.5, 1.8, 1], x_length=8.5, y_length=2.8, tips=False).move_to([0, 0.4, 0])
        self.play(Create(axes), run_time=0.8)

        v_wave = axes.plot(lambda t: np.sin(t + PI/6), color=PHASE_A, stroke_opacity=0.4)
        crossover_x = PI/6
        dot_cross = Dot(axes.c2p(crossover_x, np.sin(crossover_x + PI/6)), color=WARN, radius=0.12)
        lbl_cross = Text("Natural Crossover (alpha = 0)", font_size=16, color=WARN).next_to(dot_cross, UP, buff=0.15)

        self.play(Create(v_wave), FadeIn(dot_cross), FadeIn(lbl_cross), run_time=1.0)

        alpha_x = PI/6 + PI/6
        arrow_alpha = DoubleArrow(axes.c2p(crossover_x, 0.4), axes.c2p(alpha_x, 0.4), color=EMF, buff=0)
        lbl_alpha = MathTex(r"\alpha", font_size=24, color=EMF).next_to(arrow_alpha, UP, buff=0.08)
        dot_fire = Dot(axes.c2p(alpha_x, np.sin(alpha_x + PI/6)), color=EMF, radius=0.12)
        lbl_fire = Text("SCR Fire", font_size=16, color=EMF).next_to(dot_fire, RIGHT, buff=0.1)

        self.play(Create(arrow_alpha), FadeIn(lbl_alpha), FadeIn(dot_fire), FadeIn(lbl_fire), run_time=1.0)
        self.wait(1.5)

        cap_warn = caption_top("ห้ามวัด alpha จากจุดกำเนิด (wt = 0) เด็ดขาด! ต้องวัดจากจุดที่ diode ควรเริ่มนำ")
        self.play(FadeIn(cap_warn), run_time=0.4)

        box_warn = RoundedRectangle(width=8.5, height=1.3, corner_radius=0.15, color=WARN, fill_color=BLACK, fill_opacity=0.5).move_to([0, -1.9, 0])
        t_w1 = Text("จุดหลอกข้อสอบ: alpha = 0° คือวงจรทำงานเหมือน Diode Bridge ทุกประการ", font_size=18, color=WHITE).move_to(box_warn.get_top() + DOWN * 0.35)
        t_w2 = Text("เมื่อเพิ่ม alpha รูปคลื่นแรงดัน output จะเลื่อนถอยหลังไปเท่ากับมุม alpha", font_size=17, color=GRAYTXT).next_to(t_w1, DOWN, buff=0.15)
        grp_w = VGroup(box_warn, t_w1, t_w2)

        self.play(FadeIn(grp_w), run_time=0.9)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 13: Average Voltage with Firing Angle (alpha < pi/3)
# ==============================================================================
class Page13Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 13 · ค่าเฉลี่ย Thyristor (alpha < pi/3)")
        ttl = title("Thyristor Average Voltage: Vdc = (3VM/pi) cos(alpha)")
        cap = caption_top("อินทิเกรตช่วงที่เลื่อนด้วย alpha: ได้สูตรกำลังคูณ cos(alpha)")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        eq_int = MathTex(r"V_{dc} \cdot \frac{\pi}{3} = \int_{\pi/3 + \alpha}^{2\pi/3 + \alpha} V_M \sin(\omega t) \, d(\omega t)", font_size=27, color=WHITE).move_to([0, 1.2, 0])
        self.play(Write(eq_int), run_time=1.0)
        self.wait(1.2)

        cap_solve = caption_top("แก้สมการตรีโกณมิติ: cos(A) - cos(B) = 2 sin... ได้ผลลัพธ์เป็น cos(alpha)")
        self.play(FadeIn(cap_solve), run_time=0.4)

        box_res = RoundedRectangle(width=8.2, height=1.6, corner_radius=0.15, color=OK, fill_color=BLACK, fill_opacity=0.5).move_to([0, -0.2, 0])
        eq_final = MathTex(r"V_{dc} = \frac{3}{\pi} V_M \cos\alpha", font_size=34, color=OK).move_to(box_res.get_center() + UP * 0.25)
        t_range = Text("ใช้ได้กับทุกโหลดเมื่อ alpha < pi/3 (60°)", font_size=18, color=WHITE).move_to(box_res.get_center() + DOWN * 0.35)
        grp_res = VGroup(box_res, eq_final, t_range)
        self.play(FadeIn(grp_res), run_time=1.0)
        self.wait(1.5)

        card_check = VGroup(
            Text("เช็กความสมเหตุสมผล:", font_size=18, color=WARN),
            Text("• ถ้า alpha = 0° -> cos(0) = 1 -> Vdc = 3VM/pi (ตรงกับ Diode bridge)", font_size=17, color=WHITE),
            Text("• ยิ่งเพิ่ม alpha -> cos(alpha) ลดลง -> ควบคุมแรงดัน DC ลดลงได้ตามต้องการ", font_size=17, color=GRAYTXT)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([0, -2.1, 0])

        self.play(FadeIn(card_check), run_time=0.9)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 14: Inductive Load with alpha > pi/3
# ==============================================================================
class Page14Scene(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 14 · โหลดมี L และ alpha > pi/3")
        ttl = title("Inductive Load: Negative Voltage Segments")
        cap = caption_top("เมื่อโหลดมีความเหนี่ยวนำ L: กระแสไหลต่อเนื่อง ดึงแรงดันติดลบได้")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        cap_graph = caption_top("พลังงานสะสมใน L บังคับกระแสไหลต่อ แม้ line-to-line จะเริ่มติดลบ")
        self.play(FadeIn(cap_graph), run_time=0.4)

        axes = Axes(x_range=[0, PI, PI/6], y_range=[-1.0, 1.6, 1], x_length=8.2, y_length=2.6, tips=False).move_to([0, 0.4, 0])
        zero_line = DashedLine(axes.c2p(0, 0), axes.c2p(PI, 0), color=GRAYTXT, stroke_width=2)
        self.play(Create(axes), Create(zero_line), run_time=0.8)

        pulse = axes.plot(lambda t: np.sin(t - PI/12), x_range=[PI/4, 3*PI/4 + 0.2], color=WARN, stroke_width=4)
        neg_area = axes.get_area(pulse, x_range=[PI + PI/12 - 0.2, 3*PI/4 + 0.2], color=EMF, opacity=0.4)
        lbl_neg = Text("ช่วงแรงดันติดลบ (vdc < 0)", font_size=16, color=EMF).next_to(axes.c2p(3*PI/4, -0.4), DOWN, buff=0.1)

        self.play(Create(pulse), FadeIn(lbl_neg), run_time=1.2)
        self.wait(1.5)

        self.play(FadeOut(cap_graph), run_time=0.3)
        cap_summary = caption_top("สูตรค่าเฉลี่ยยังคงเดิม แต่พลังงานบางส่วนจะถูกส่งคืนแหล่งจ่าย")
        self.play(FadeIn(cap_summary), run_time=0.4)

        box_final = RoundedRectangle(width=8.5, height=1.6, corner_radius=0.15, color=OK, fill_color=BLACK, fill_opacity=0.5).move_to([0, -1.8, 0])
        eq_f = MathTex(r"V_{dc} = \frac{3}{\pi} V_M \cos\alpha \quad (\text{Inductive Load, } \alpha > \pi/3)", font_size=25, color=OK).move_to(box_final.get_center() + UP * 0.25)
        t_inv = Text("หาก alpha > 90° (pi/2) ค่า Vdc จะติดลบ -> วงจรทำงานเป็น Inverter ส่งพลังงานกลับ AC", font_size=16, color=WHITE).move_to(box_final.get_center() + DOWN * 0.35)
        grp_final = VGroup(box_final, eq_f, t_inv)

        self.play(FadeIn(grp_final), run_time=1.0)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)
