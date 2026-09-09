import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Palette for 3-Phase
PHASE_A  = "#42A5F5"   # ฟ้า
PHASE_B  = "#FFA726"   # ส้ม
PHASE_C  = "#66BB6A"   # เขียว
VDC_COL  = "#FFD54F"   # ทอง/เหลือง
DIODE_ON = "#26C6DA"   # เขียวอมฟ้า นำกระแส
DIODE_OFF= "#78909C"   # เทา ดับ


class Page01Scene(SafeScene):
    def construct(self):
        self.step_intro()
        self.step_bridge_preview()
        self.step_envelope_preview()
        self.step_summary()

    def step_intro(self):
        pref = page_ref("หน้า 1 · แผนที่การเรียนรู้")
        ttl = title("Three-Phase Bridge Rectifiers")
        cap = caption_top("ภาพรวมทั้งบท: เปลี่ยน AC 3 เฟส เป็น DC เรียบสูงด้วยไดโอด 6 ตัว")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

    def step_bridge_preview(self):
        cap = caption_top("โครงสร้าง 3 กิ่ง (Limbs) 6 ไดโอด: ผลัดกันนำกระแสคู่บน-ล่าง")
        self.play(FadeIn(cap), run_time=0.5)

        # แหล่งจ่าย 3 เฟส ด้านซ้าย
        src_center = np.array([-4.5, -0.3, 0])
        lbl_src = Text("แหล่งจ่าย 3 เฟส", font_size=18, color=WHITE).move_to(src_center + UP * 1.5)

        dot_a = Dot(src_center + UP * 0.7, color=PHASE_A, radius=0.12)
        dot_b = Dot(src_center, color=PHASE_B, radius=0.12)
        dot_c = Dot(src_center + DOWN * 0.7, color=PHASE_C, radius=0.12)

        txt_a = Text("a", font_size=18, color=PHASE_A).next_to(dot_a, LEFT, buff=0.12)
        txt_b = Text("b", font_size=18, color=PHASE_B).next_to(dot_b, LEFT, buff=0.12)
        txt_c = Text("c", font_size=18, color=PHASE_C).next_to(dot_c, LEFT, buff=0.12)

        sources = VGroup(lbl_src, dot_a, dot_b, dot_c, txt_a, txt_b, txt_c)

        # 3 Limbs กลางจอ: x = -1.8, -0.6, 0.6
        xs = [-1.8, -0.6, 0.6]
        top_y = 1.0
        bot_y = -1.6
        mid_y = -0.3

        # รางไฟ DC บน/ล่าง
        rail_top = Line([-2.3, top_y, 0], [2.2, top_y, 0], color=EMF, stroke_width=4)
        rail_bot = Line([-2.3, bot_y, 0], [2.2, bot_y, 0], color=FIELD, stroke_width=4)
        lbl_vplus = MathTex("v^+", color=EMF, font_size=24).next_to(rail_top, UP, buff=0.08)
        lbl_vminus = MathTex("v^-", color=FIELD, font_size=24).next_to(rail_bot, DOWN, buff=0.08)

        # กิ่งและไดโอด
        wires = VGroup()
        diodes = VGroup()

        colors = [PHASE_A, PHASE_B, PHASE_C]
        for i, x in enumerate(xs):
            y_in = 0.7 - i * 0.7
            w_in = Line(src_center + np.array([0, y_in, 0]), [x, y_in, 0], color=colors[i], stroke_width=2.5)
            w_vert = Line([x, top_y, 0], [x, bot_y, 0], color=GRAYTXT, stroke_width=2)
            wires.add(w_in, w_vert)

            # D top
            dt = Triangle(color=WHITE, fill_opacity=0.85, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([x, (top_y + mid_y)/2, 0])
            # D bot
            db = Triangle(color=WHITE, fill_opacity=0.85, fill_color=DIODE_ON).scale(0.16).rotate(PI/2).move_to([x, (mid_y + bot_y)/2, 0])
            diodes.add(dt, db)

        # โหลดด้านขวา
        load_box = Rectangle(width=0.7, height=1.3, color=WHITE, fill_color=METAL, fill_opacity=0.3).move_to([2.2, mid_y, 0])
        load_txt = Text("โหลด", font_size=17, color=WHITE).move_to(load_box)
        w_load_t = Line([2.2, top_y, 0], load_box.get_top(), color=EMF)
        w_load_b = Line([2.2, bot_y, 0], load_box.get_bottom(), color=FIELD)
        vdc_lbl = MathTex("v_{dc}", color=VDC_COL, font_size=26).next_to(load_box, RIGHT, buff=0.2)

        bridge_grp = VGroup(sources, rail_top, rail_bot, lbl_vplus, lbl_vminus,
                            wires, diodes, load_box, load_txt, w_load_t, w_load_b, vdc_lbl)

        self.play(FadeIn(bridge_grp), run_time=1.2)
        self.wait(1.5)

        self.play(FadeOut(cap), run_time=0.3)
        cap2 = caption_top("หลักการ: ขาบนเลือกเฟสสูงสุด, ขาล่างเลือกเฟสต่ำสุดเสมอ")
        self.play(FadeIn(cap2), run_time=0.4)
        self.wait(2.0)

        self.play(FadeOut(bridge_grp), FadeOut(cap2), run_time=0.6)

    def step_envelope_preview(self):
        cap = caption_top("ผลลัพธ์: แรงดัน Line-to-Line 6 พัลส์ต่อคาบ เรียบสูงมาก")
        self.play(FadeIn(cap), run_time=0.5)

        axes = Axes(
            x_range=[0, TAU + 0.1, PI/3],
            y_range=[-1.4, 1.4, 1],
            x_length=9.6,
            y_length=2.8,
            axis_config={"color": GRAYTXT, "include_tip": False},
            tips=False
        ).move_to([0, -0.5, 0])

        w_a = axes.plot(lambda t: np.sin(t), x_range=[0, TAU], color=PHASE_A, stroke_opacity=0.35)
        w_b = axes.plot(lambda t: np.sin(t - 2*PI/3), x_range=[0, TAU], color=PHASE_B, stroke_opacity=0.35)
        w_c = axes.plot(lambda t: np.sin(t - 4*PI/3), x_range=[0, TAU], color=PHASE_C, stroke_opacity=0.35)

        def vdc_func(t):
            t_mod = t % (PI / 3)
            return np.sqrt(3) * np.sin(t_mod + PI/3) * 0.7

        envelope = axes.plot(vdc_func, x_range=[0, TAU], color=VDC_COL, stroke_width=4.0, use_smoothing=False)
        env_label = Text("vdc: 6-Pulse Envelope", font_size=18, color=VDC_COL).next_to(axes.c2p(PI, 1.2), UP, buff=0.1)

        vdc_avg_y = (3 * np.sqrt(3) / PI) * 0.7
        line_avg = DashedLine(axes.c2p(0, vdc_avg_y), axes.c2p(TAU, vdc_avg_y), color=OK, stroke_width=2.5)
        avg_label = MathTex(r"V_{dc} = \frac{3 V_M}{\pi} \approx 0.955 V_M", color=OK, font_size=22).next_to(line_avg, DOWN, buff=0.15)

        graph_grp = VGroup(axes, w_a, w_b, w_c, envelope, env_label, line_avg, avg_label)
        self.play(Create(axes), Create(w_a), Create(w_b), Create(w_c), run_time=1.2)
        self.play(Create(envelope), FadeIn(env_label), run_time=1.2)
        self.play(Create(line_avg), FadeIn(avg_label), run_time=0.8)
        self.wait(2.2)

        self.play(FadeOut(graph_grp), FadeOut(cap), run_time=0.6)

    def step_summary(self):
        cap = caption_top("หัวใจสำคัญของวงจรเรียงกระแสบริดจ์ 3 เฟส")
        self.play(FadeIn(cap), run_time=0.4)

        card1 = VGroup(
            Text("1. ไดโอด 6 ตัว (3 กิ่ง)", font_size=21, color=WHITE),
            Text("นำกระแสตัวละ 120° แต่มีสลับ switching ทุก 60°", font_size=18, color=GRAYTXT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        card2 = VGroup(
            Text("2. เอาต์พุตคือแรงดันสาย (Line-to-Line Voltage)", font_size=21, color=WHITE),
            MathTex(r"v_{dc} = v^+ - v^- = v_{\text{line}}", color=VDC_COL, font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        card3 = VGroup(
            Text("3. แรงดัน DC เฉลี่ยสูงมาก และ Ripple ต่ำเพียง 4.2%", font_size=21, color=WHITE),
            MathTex(r"V_{dc} = \frac{3 V_M}{\pi} \quad (V_{rms} \approx V_{dc})", color=OK, font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        box_grp = VGroup(card1, card2, card3).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([0, -0.3, 0])

        self.play(FadeIn(box_grp, shift=UP * 0.2), run_time=1.0)
        self.wait(2.5)
        self.fade_out_all(run_time=0.6)
