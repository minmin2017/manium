import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Color palette for 3-Phase Converter
PHASE_A   = "#EF5350"   # Red (Phase a)
PHASE_B   = "#42A5F5"   # Blue (Phase b)
PHASE_C   = "#66BB6A"   # Green (Phase c)
VDC_COL   = "#FF9800"   # Orange (vdc output)
PATH_ACT  = "#FFD54F"   # Yellow (Active SCR / conducting path)
WARN_NEG  = "#E91E63"   # Magenta-red (Negative voltage segment)
DIODE_OFF = "#78909C"   # Muted gray (SCR OFF)


class Page14NegativeVdcScene(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # Header & Navigation
        # ----------------------------------------------------------------------
        pref = page_ref("หน้า 14 · ทำไม vdc ติดลบชั่วขณะ?")
        ttl = title("Why vdc Briefly Becomes Negative", size=25)
        cap1 = caption_top("เมื่อโหลดมี L และ alpha > 60°: แรงดัน vdc มุดลงใต้แกน 0 V ชั่วขณะ เกิดจากอะไร?")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)
        self.wait(1.8)

        # ----------------------------------------------------------------------
        # 1. Orient Zero-Background Learner: Minimal Circuit Model (Left Side)
        # ----------------------------------------------------------------------
        cap2 = caption_top("1. วงจรบริดจ์ SCR: คู่ T1, T6 กำลังนำกระแส Id ไหลผ่านขดลวด L ทิศเดิมเสมอ")
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)

        # 3-Phase Sources
        src_lbl = Text("แหล่งจ่าย 3 เฟส", font_size=15, color=WHITE).move_to([-5.5, 1.45, 0])
        dot_a = Dot([-5.8, 0.65, 0], color=PHASE_A, radius=0.08)
        dot_b = Dot([-5.8, -0.25, 0], color=PHASE_B, radius=0.08)
        dot_c = Dot([-5.8, -1.15, 0], color=PHASE_C, radius=0.08)
        lbl_a = Text("a", font_size=16, color=PHASE_A).next_to(dot_a, LEFT, buff=0.10)
        lbl_b = Text("b", font_size=16, color=PHASE_B).next_to(dot_b, LEFT, buff=0.10)
        lbl_c = Text("c", font_size=16, color=PHASE_C).next_to(dot_c, LEFT, buff=0.10)
        sources = VGroup(src_lbl, dot_a, dot_b, dot_c, lbl_a, lbl_b, lbl_c)

        # DC Rails
        rail_top = Line([-4.7, 1.05, 0], [-1.8, 1.05, 0], color=EMF, stroke_width=3)
        rail_bot = Line([-4.7, -1.55, 0], [-1.8, -1.55, 0], color=FIELD, stroke_width=3)
        lbl_vplus = MathTex("v^+", font_size=18, color=EMF).next_to(rail_top.get_left(), UP, buff=0.08)
        lbl_vminus = MathTex("v^-", font_size=18, color=FIELD).next_to(rail_bot.get_left(), DOWN, buff=0.08)

        # Limbs & Inactive Wires
        w_a = Line([-5.8, 0.65, 0], [-4.3, 0.65, 0], color=PHASE_A, stroke_width=2)
        w_b = Line([-5.8, -0.25, 0], [-3.5, -0.25, 0], color=PHASE_B, stroke_width=2)
        w_c = Line([-5.8, -1.15, 0], [-2.7, -1.15, 0], color=PHASE_C, stroke_width=2)
        l_wire1 = Line([-4.3, 1.05, 0], [-4.3, -1.55, 0], color=GRAYTXT, stroke_width=1.5)
        l_wire2 = Line([-3.5, 1.05, 0], [-3.5, -1.55, 0], color=GRAYTXT, stroke_width=1.5)
        l_wire3 = Line([-2.7, 1.05, 0], [-2.7, -1.55, 0], color=GRAYTXT, stroke_width=1.5)

        # SCR Symbols (T1 & T6 active, others off)
        t1 = Triangle(fill_opacity=0.9, fill_color=PATH_ACT, stroke_color=PATH_ACT, stroke_width=2).scale(0.13).move_to([-4.3, 0.55, 0])
        t1_bar = Line([-4.42, 0.68, 0], [-4.18, 0.68, 0], color=PATH_ACT, stroke_width=2.5)
        t3 = Triangle(fill_opacity=0.5, fill_color=DIODE_OFF, stroke_color=WHITE, stroke_width=1.5).scale(0.13).move_to([-3.5, 0.55, 0])
        t3_bar = Line([-3.62, 0.68, 0], [-3.38, 0.68, 0], color=WHITE, stroke_width=2)
        t5 = Triangle(fill_opacity=0.5, fill_color=DIODE_OFF, stroke_color=WHITE, stroke_width=1.5).scale(0.13).move_to([-2.7, 0.55, 0])
        t5_bar = Line([-2.82, 0.68, 0], [-2.58, 0.68, 0], color=WHITE, stroke_width=2)

        t4 = Triangle(fill_opacity=0.5, fill_color=DIODE_OFF, stroke_color=WHITE, stroke_width=1.5).scale(0.13).move_to([-4.3, -1.05, 0])
        t4_bar = Line([-4.42, -0.92, 0], [-4.18, -0.92, 0], color=WHITE, stroke_width=2)
        t6 = Triangle(fill_opacity=0.9, fill_color=PATH_ACT, stroke_color=PATH_ACT, stroke_width=2).scale(0.13).move_to([-3.5, -1.05, 0])
        t6_bar = Line([-3.62, -0.92, 0], [-3.38, -0.92, 0], color=PATH_ACT, stroke_width=2.5)
        t2 = Triangle(fill_opacity=0.5, fill_color=DIODE_OFF, stroke_color=WHITE, stroke_width=1.5).scale(0.13).move_to([-2.7, -1.05, 0])
        t2_bar = Line([-2.82, -0.92, 0], [-2.58, -0.92, 0], color=WHITE, stroke_width=2)

        lbl_t1 = Text("T1 (นำขั้วบวก)", font_size=13, color=PATH_ACT).move_to([-4.3, 1.30, 0])
        lbl_t6 = Text("T6 (นำขั้วลบ)", font_size=13, color=PATH_ACT).move_to([-3.5, -1.82, 0])

        # Active Conducting Path (highlighted loop)
        path_act_top = VMobject(color=PATH_ACT, stroke_width=3.5).set_points_as_corners([
            [-5.8, 0.65, 0], [-4.3, 0.65, 0], [-4.3, 1.05, 0], [-1.8, 1.05, 0], [-1.8, 0.45, 0]
        ])
        path_act_bot = VMobject(color=PATH_ACT, stroke_width=3.5).set_points_as_corners([
            [-1.8, -1.15, 0], [-1.8, -1.55, 0], [-3.5, -1.55, 0], [-3.5, -0.25, 0], [-5.8, -0.25, 0]
        ])

        # Inductive Load at x = -1.8
        arcs = VGroup()
        for y_c in [0.30, 0.15, 0.00, -0.15]:
            arc = Arc(radius=0.08, start_angle=-PI/2, angle=PI, color=CURRENT, stroke_width=3.5).move_to([-1.72, y_c, 0])
            arcs.add(arc)
        lbl_L = MathTex("L", font_size=20, color=CURRENT).move_to([-1.35, 0.08, 0])

        wire_lr = Line([-1.8, -0.15, 0], [-1.8, -0.45, 0], color=CURRENT, stroke_width=2.5)
        res_box = Rectangle(width=0.22, height=0.45, color=WHITE, fill_color=METAL, fill_opacity=0.3, stroke_width=2).move_to([-1.8, -0.68, 0])
        lbl_R = MathTex("R", font_size=18, color=WHITE).move_to([-1.35, -0.68, 0])
        wire_rb = Line([-1.8, -0.91, 0], [-1.8, -1.15, 0], color=CURRENT, stroke_width=2.5)

        # Current Arrow Id
        arrow_id = Arrow([-2.25, 0.45, 0], [-2.25, -0.65, 0], color=CURRENT, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.28)
        lbl_id = MathTex("I_d", color=CURRENT, font_size=22).next_to(arrow_id, LEFT, buff=0.10)
        lbl_id_dir = Text("ทิศเดิมเสมอ", font_size=12, color=CURRENT).next_to(lbl_id, DOWN, buff=0.06)

        # Load Voltage vdc Indicator
        sign_plus = MathTex("+", font_size=20, color=EMF).move_to([-0.75, 0.75, 0])
        sign_minus = MathTex("-", font_size=20, color=FIELD).move_to([-0.75, -1.25, 0])
        lbl_vdc = MathTex(r"v_{dc} = v_{ab}", font_size=19, color=VDC_COL).move_to([-0.75, -0.25, 0])
        ptr_vdc_top = Line([-0.75, 0.55, 0], [-0.75, 0.00, 0], color=VDC_COL, stroke_width=1.5)
        ptr_vdc_bot = Line([-0.75, -0.50, 0], [-0.75, -1.05, 0], color=VDC_COL, stroke_width=1.5)

        circuit_grp = VGroup(
            sources, rail_top, rail_bot, lbl_vplus, lbl_vminus,
            w_a, w_b, w_c, l_wire1, l_wire2, l_wire3,
            t1, t1_bar, t3, t3_bar, t5, t5_bar,
            t4, t4_bar, t6, t6_bar, t2, t2_bar,
            lbl_t1, lbl_t6, path_act_top, path_act_bot,
            arcs, lbl_L, wire_lr, res_box, lbl_R, wire_rb,
            arrow_id, lbl_id, lbl_id_dir,
            sign_plus, sign_minus, lbl_vdc, ptr_vdc_top, ptr_vdc_bot
        )

        self.play(FadeIn(circuit_grp), run_time=1.2)
        self.wait(1.8)

        # ----------------------------------------------------------------------
        # 2. Selected Waveform & Reference Case alpha < pi/3 (Right Side)
        # ----------------------------------------------------------------------
        cap3 = caption_top("2. กรณีอ้างอิง alpha < 60°: คู่ใหม่ถูกยิงมารับช่วงต่อที่ 150° ก่อนคลื่นเดิมตกถึง 0 V")
        self.play(ReplacementTransform(cap2, cap3), run_time=0.5)

        axes = Axes(
            x_range=[0, 7*PI/6, PI/6],
            y_range=[-0.55, 1.25, 0.5],
            x_length=5.3,
            y_length=2.8,
            tips=False
        ).move_to([3.5, -0.20, 0])

        zero_line = DashedLine(axes.c2p(0, 0), axes.c2p(7*PI/6, 0), color=GRAYTXT, stroke_width=1.5)
        lbl_0v = MathTex(r"0	ext{ V}", font_size=16, color=GRAYTXT).next_to(axes.c2p(0, 0), LEFT, buff=0.12)
        lbl_wt = MathTex(r"\omega t", font_size=18, color=WHITE).next_to(axes.c2p(7*PI/6, 0), RIGHT, buff=0.12)

        tick_p3 = MathTex(r"\pi/3", font_size=15, color=GRAYTXT).next_to(axes.c2p(PI/3, 0), DOWN, buff=0.22)
        tick_2p3 = MathTex(r"2\pi/3", font_size=15, color=GRAYTXT).next_to(axes.c2p(2*PI/3, 0), DOWN, buff=0.22)
        tick_pi = MathTex(r"\pi", font_size=15, color=WARN).next_to(axes.c2p(PI, 0), DOWN, buff=0.22)

        dot_zero = Dot(axes.c2p(PI, 0), color=WARN, radius=0.08)
        lbl_zero = Text("จุดตัด 0 V", font_size=13, color=WARN).next_to(dot_zero, UP, buff=0.22)

        vab_curve = axes.plot(lambda t: np.sin(t), x_range=[0.05, 7*PI/6], color=PHASE_A, stroke_opacity=0.35, stroke_width=2)
        lbl_vab = MathTex(r"v_{ab}", font_size=18, color=PHASE_A).move_to(axes.c2p(PI/2, 1.15))

        # Alpha = 30 deg (< 60 deg): interval [90 deg, 150 deg]
        v_seg1 = axes.plot(lambda t: np.sin(t), x_range=[PI/2, 5*PI/6], color=OK, stroke_width=4)
        arrow_alpha1 = DoubleArrow(axes.c2p(PI/3, 0.45), axes.c2p(PI/2, 0.45), color=OK, buff=0, stroke_width=2.5)
        lbl_alpha1 = MathTex(r"\alpha = 30^\circ < 60^\circ", font_size=15, color=OK).next_to(arrow_alpha1, UP, buff=0.08)
        note_c1 = Text("vdc(t) > 0 ตลอดเวลา ไม่ติดลบ", font_size=14, color=OK).move_to([3.5, -1.85, 0])

        axes_grp_base = VGroup(
            axes, zero_line, lbl_0v, lbl_wt,
            tick_p3, tick_2p3, tick_pi, dot_zero, lbl_zero,
            vab_curve, lbl_vab
        )

        self.play(Create(axes_grp_base), run_time=1.2)
        self.play(Create(arrow_alpha1), FadeIn(lbl_alpha1), Create(v_seg1), FadeIn(note_c1), run_time=1.0)
        self.wait(2.2)

        # ----------------------------------------------------------------------
        # 3. Transform to alpha = 75 deg (> 60 deg) & Current Persists Past 0 V
        # ----------------------------------------------------------------------
        cap4 = caption_top("3. เมื่อ alpha = 75° (> 60°): ยิงคู่ใหม่ช้าเกินไป จนคลื่นเดิมเลยจุดตัด 0 V (180°)")
        self.play(
            ReplacementTransform(cap3, cap4),
            FadeOut(v_seg1), FadeOut(note_c1),
            run_time=0.5
        )

        arrow_alpha2 = DoubleArrow(axes.c2p(PI/3, 0.45), axes.c2p(3*PI/4, 0.45), color=WARN, buff=0, stroke_width=2.5)
        lbl_alpha2 = MathTex(r"\alpha = 75^\circ > 60^\circ", font_size=15, color=WARN).next_to(arrow_alpha2, UP, buff=0.08)

        self.play(
            ReplacementTransform(arrow_alpha1, arrow_alpha2),
            ReplacementTransform(lbl_alpha1, lbl_alpha2),
            run_time=0.8
        )

        self.play(
            Flash(dot_zero, color=WARN, flash_radius=0.35),
            Indicate(arrow_id, color=CURRENT, scale_factor=1.25),
            Indicate(arcs, color=CURRENT, scale_factor=1.25),
            run_time=1.0
        )

        # ----------------------------------------------------------------------
        # 4. Waveform Dips Below Zero & Direct Cause Chain
        # ----------------------------------------------------------------------
        cap5 = caption_top("4. L สะสมพลังงาน บังคับ Id ไหลต่อ -> ดึง SCR เดิมนำข้าม 0 V ทำให้ vdc(t) ติดลบชั่วขณะ")
        self.play(ReplacementTransform(cap4, cap5), run_time=0.5)

        v_seg2_pos = axes.plot(lambda t: np.sin(t), x_range=[3*PI/4, PI], color=VDC_COL, stroke_width=4)
        v_seg2_neg = axes.plot(lambda t: np.sin(t), x_range=[PI, 13*PI/12], color=WARN_NEG, stroke_width=4.5)

        thetas_neg = np.linspace(PI, 13*PI/12, 25)
        pts_neg = [axes.c2p(th, np.sin(th)) for th in thetas_neg]
        pts_axis = [axes.c2p(13*PI/12, 0), axes.c2p(PI, 0)]
        neg_polygon = Polygon(*(pts_neg + pts_axis), color=WARN_NEG, fill_color=WARN_NEG, fill_opacity=0.5, stroke_width=0)

        jump_line = DashedLine(axes.c2p(13*PI/12, np.sin(13*PI/12)), axes.c2p(13*PI/12, np.sin(5*PI/12)), color=OK, stroke_width=2)
        tag_neg = MathTex(r"v_{dc}(t) < 0 	ext{ (instantaneous)}", font_size=16, color=WARN_NEG).next_to(axes.c2p(13*PI/12, np.sin(13*PI/12)), DOWN, buff=0.25)

        self.play(Create(v_seg2_pos), run_time=0.6)
        self.play(Create(v_seg2_neg), FadeIn(neg_polygon), Create(jump_line), FadeIn(tag_neg), run_time=1.1)
        self.wait(1.5)

        # Direct cause chain in Thai (4 clean blocks)
        box_chain = RoundedRectangle(width=12.6, height=0.95, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.65).move_to([0, -2.35, 0])

        c1 = Text("1. L มีพลังงานสะสม\n(E = ½ L Id²)", font_size=12, color=WHITE)
        c2 = Text("2. Id หยุดทันทีไม่ได้\n(ไหลพุ่งไปข้างหน้าต่อ)", font_size=12, color=CURRENT)
        c3 = Text("3. SCR เดิมเปิดค้าง\n(T1, T6 ล็อกโหลดกับ AC)", font_size=12, color=PATH_ACT)
        c4 = Text("4. AC ตกข้าม 0 V สู่แดนลบ\n(vdc ติดลบตามสาย AC)", font_size=12, color=WARN_NEG)

        arr1 = MathTex(r"\to", font_size=18, color=GRAYTXT)
        arr2 = MathTex(r"\to", font_size=18, color=GRAYTXT)
        arr3 = MathTex(r"\to", font_size=18, color=GRAYTXT)

        chain_flow = VGroup(c1, arr1, c2, arr2, c3, arr3, c4).arrange(RIGHT, buff=0.18).move_to(box_chain.get_center())

        note_id = Text("สำคัญ: กระแส Id ยังไหลทิศเดิมเสมอ ไม่ได้กลับทิศ! (กำลัง p = vdc · Id < 0 ส่งพลังงานคืนสู่ AC)", font_size=14, color=OK).move_to([0, -3.05, 0])

        self.play(FadeIn(box_chain), FadeIn(chain_flow), FadeIn(note_id), run_time=1.2)
        self.wait(3.0)

        # ----------------------------------------------------------------------
        # 5. Contrast Instantaneous vs Average & Dial/Formula Boundary
        # ----------------------------------------------------------------------
        cap6 = caption_top("5. สรุป: vdc(t) ติดลบชั่วขณะ != Vdc เฉลี่ยติดลบ (alpha < 90° ค่าเฉลี่ยยังเป็นบวก)")
        axes_all = VGroup(
            axes_grp_base, arrow_alpha2, lbl_alpha2,
            v_seg2_pos, v_seg2_neg, neg_polygon, jump_line, tag_neg
        )

        self.play(
            ReplacementTransform(cap5, cap6),
            FadeOut(circuit_grp),
            FadeOut(axes_all),
            FadeOut(box_chain),
            FadeOut(chain_flow),
            FadeOut(note_id),
            run_time=0.8
        )

        # Formula Card
        box_eq = RoundedRectangle(width=7.5, height=1.0, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.6).move_to([0, 1.45, 0])
        eq_vdc = MathTex(r"V_{dc} = \frac{3}{\pi} V_M \cos\alpha", font_size=32, color=OK).move_to(box_eq.get_center())

        # Side-by-Side Comparison Cards
        card_l = RoundedRectangle(width=5.8, height=1.75, corner_radius=0.12, color=WARN_NEG, fill_color=BLACK, fill_opacity=0.5).move_to([-3.2, -0.15, 0])
        hdr_l = Text("แรงดันขณะหนึ่ง vdc(t)", font_size=16, color=WARN_NEG).move_to(card_l.get_top() + DOWN * 0.26)
        txt_l = Text("• เกิดรอยหยักติดลบชั่วขณะเมื่อ alpha > 60°\n• L ยื้อ Id บังคับ SCR นำข้ามจุดตัด 0 V\n• กระแส Id ยังไหลไปข้างหน้า ไม่ได้กลับทิศ", font_size=13, color=WHITE).next_to(hdr_l, DOWN, buff=0.12)
        grp_l = VGroup(card_l, hdr_l, txt_l)

        card_r = RoundedRectangle(width=5.8, height=1.75, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.5).move_to([3.2, -0.15, 0])
        hdr_r = Text("แรงดันเฉลี่ย Vdc", font_size=16, color=OK).move_to(card_r.get_top() + DOWN * 0.26)
        txt_r = Text("• alpha < 90°: Vdc > 0 (Rectifier เฉลี่ยเป็นบวก)\n• alpha = 90°: Vdc = 0 (ขอบเขตเฉลี่ยศูนย์)\n• alpha > 90°: Inverter (ต้องมีไฟ DC ภายนอกหนุน)", font_size=13, color=WHITE).next_to(hdr_r, DOWN, buff=0.12)
        grp_r = VGroup(card_r, hdr_r, txt_r)

        # Alpha Range Bar
        bar_bg = RoundedRectangle(width=11.6, height=0.55, corner_radius=0.10, color=GRAYTXT, stroke_width=1.5, fill_color=BLACK, fill_opacity=0.6).move_to([0, -1.65, 0])
        t_z1 = Text("0° - 60°: vdc > 0 ทุกโหลด", font_size=12, color=OK).move_to([-3.8, -1.65, 0])
        t_z2 = Text("60° - 90°: มีช่วงลบสั้นๆ แต่เฉลี่ย > 0", font_size=12, color=WARN).move_to([0, -1.65, 0])
        t_z3 = Text("> 90°: Inverter (ต้องมีไฟ DC หนุน)", font_size=12, color=WARN_NEG).move_to([3.8, -1.65, 0])

        rule_box = Text("สรุปฟิสิกส์: ขดลวด L ไม่ได้สร้างพลังงานเอง และไม่ได้ทำให้ค่าเฉลี่ยติดลบ", font_size=14, color=GRAYTXT).move_to([0, -2.40, 0])

        self.play(
            FadeIn(box_eq), FadeIn(eq_vdc),
            FadeIn(grp_l), FadeIn(grp_r),
            FadeIn(bar_bg), FadeIn(t_z1), FadeIn(t_z2), FadeIn(t_z3),
            FadeIn(rule_box),
            run_time=1.2
        )
        self.wait(3.5)
        self.fade_out_all(run_time=0.8)
