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
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # 1. Orient Zero-Background Learner: Minimal Circuit Model (Left Side)
        # ----------------------------------------------------------------------
        cap2 = caption_top("1. ปกติ SCR นำกระแส 2 ตัวเสมอ: บน 1 ตัว (T1 เฟส a) + ล่าง 1 ตัว (T6 เฟส b)")
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)

        # 3-Phase Sources
        src_lbl = Text("แหล่งจ่าย 3 เฟส", font_size=14, color=WHITE).move_to([-5.5, 1.45, 0])
        dot_a = Dot([-5.8, 0.65, 0], color=PHASE_A, radius=0.08)
        dot_b = Dot([-5.8, -0.25, 0], color=PHASE_B, radius=0.08)
        dot_c = Dot([-5.8, -1.15, 0], color=PHASE_C, radius=0.08)
        lbl_a = Text("a", font_size=15, color=PHASE_A).next_to(dot_a, LEFT, buff=0.10)
        lbl_b = Text("b", font_size=15, color=PHASE_B).next_to(dot_b, LEFT, buff=0.10)
        lbl_c = Text("c", font_size=15, color=PHASE_C).next_to(dot_c, LEFT, buff=0.10)
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

        # SCR Symbols: T1 & T6 initially active (yellow)
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

        lbl_t1 = Text("T1", font_size=13, color=PATH_ACT).move_to([-4.3, 1.25, 0])
        lbl_t6 = Text("T6", font_size=13, color=PATH_ACT).move_to([-3.5, -1.80, 0])
        lbl_t2 = Text("T2", font_size=13, color=GRAYTXT).move_to([-2.7, -1.80, 0])

        # Active Conducting Path 1: T1 & T6
        path_act_top = VMobject(color=PATH_ACT, stroke_width=3.5).set_points_as_corners([
            [-5.8, 0.65, 0], [-4.3, 0.65, 0], [-4.3, 1.05, 0], [-1.8, 1.05, 0], [-1.8, 0.45, 0]
        ])
        path_act_bot1 = VMobject(color=PATH_ACT, stroke_width=3.5).set_points_as_corners([
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
            lbl_t1, lbl_t6, lbl_t2, path_act_top, path_act_bot1,
            arcs, lbl_L, wire_lr, res_box, lbl_R, wire_rb,
            arrow_id, lbl_id,
            sign_plus, sign_minus, lbl_vdc, ptr_vdc_top, ptr_vdc_bot
        )

        self.play(FadeIn(circuit_grp), run_time=1.2)
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # 2. Reference Case alpha = 30° with VISIBLE COMMUTATION (Correction 1)
        # ----------------------------------------------------------------------
        cap3 = caption_top("2. กรณีอ้างอิง alpha < 60°: พอถึง 150° คู่ใหม่ (T1, T2) ถูกยิง Gate มารับช่วงต่อทันที")
        self.play(ReplacementTransform(cap2, cap3), run_time=0.5)

        axes = Axes(
            x_range=[0, 7*PI/6, PI/6],
            y_range=[-0.55, 1.25, 0.5],
            x_length=5.3,
            y_length=2.8,
            tips=False
        ).move_to([3.5, -0.20, 0])

        zero_line = DashedLine(axes.c2p(0, 0), axes.c2p(7*PI/6, 0), color=GRAYTXT, stroke_width=1.5)
        lbl_0v = MathTex(r"0\text{ V}", font_size=16, color=GRAYTXT).next_to(axes.c2p(0, 0), LEFT, buff=0.12)
        lbl_wt = MathTex(r"\omega t", font_size=18, color=WHITE).next_to(axes.c2p(7*PI/6, 0), RIGHT, buff=0.12)

        tick_p3 = MathTex(r"\pi/3", font_size=15, color=GRAYTXT).next_to(axes.c2p(PI/3, 0), DOWN, buff=0.22)
        tick_5p6 = MathTex(r"5\pi/6", font_size=14, color=OK).next_to(axes.c2p(5*PI/6, 0), DOWN, buff=0.22)
        tick_pi = MathTex(r"\pi", font_size=15, color=WARN).next_to(axes.c2p(PI, 0), DOWN, buff=0.22)

        vab_curve = axes.plot(lambda t: np.sin(t), x_range=[0.05, 7*PI/6], color=PHASE_A, stroke_opacity=0.35, stroke_width=2)
        vac_curve = axes.plot(lambda t: np.sin(t - PI/3), x_range=[0.05, 7*PI/6], color=PHASE_C, stroke_opacity=0.25, stroke_width=1.5)
        lbl_vab = MathTex(r"v_{ab}", font_size=17, color=PHASE_A).move_to(axes.c2p(PI/2, 1.15))

        # Alpha = 30°: Segment vab from 90° (PI/2) to 150° (5PI/6)
        v_seg1 = axes.plot(lambda t: np.sin(t), x_range=[PI/2, 5*PI/6], color=OK, stroke_width=4)
        arrow_alpha1 = DoubleArrow(axes.c2p(PI/3, 0.45), axes.c2p(PI/2, 0.45), color=OK, buff=0, stroke_width=2.5)
        lbl_alpha1 = MathTex(r"\alpha = 30^\circ < 60^\circ", font_size=15, color=OK).next_to(arrow_alpha1, UP, buff=0.08)

        axes_grp_base = VGroup(
            axes, zero_line, lbl_0v, lbl_wt,
            tick_p3, tick_5p6, tick_pi,
            vab_curve, vac_curve, lbl_vab
        )

        self.play(Create(axes_grp_base), run_time=1.0)
        self.play(Create(arrow_alpha1), FadeIn(lbl_alpha1), Create(v_seg1), run_time=0.8)

        # ANIMATE VISIBLE COMMUTATION at 150° (5PI/6):
        # T2 receives Gate Pulse, turns yellow; T6 turns gray; path switches to Phase C!
        comm_pulse = Dot(t2.get_center(), color=YELLOW, radius=0.18)
        path_act_bot2 = VMobject(color=PATH_ACT, stroke_width=3.5).set_points_as_corners([
            [-1.8, -1.15, 0], [-1.8, -1.55, 0], [-2.7, -1.55, 0], [-2.7, -1.15, 0], [-5.8, -1.15, 0]
        ])

        v_seg1_next = axes.plot(lambda t: np.sin(t - PI/3), x_range=[5*PI/6, 7*PI/6], color=PHASE_C, stroke_width=4)
        lbl_comm = Text("ยิง Gate ให้ T2 รับช่วงต่อ!", font_size=13, color=YELLOW).move_to([-3.0, -2.15, 0])

        self.play(
            Flash(comm_pulse, color=YELLOW, flash_radius=0.3),
            FadeIn(lbl_comm),
            run_time=0.6
        )

        self.play(
            # T6 turns OFF (gray), T2 turns ON (yellow)
            t6.animate.set_fill(DIODE_OFF, opacity=0.5).set_stroke(WHITE, width=1.5),
            t6_bar.animate.set_color(WHITE).set_stroke(width=2),
            lbl_t6.animate.set_color(GRAYTXT),
            t2.animate.set_fill(PATH_ACT, opacity=0.9).set_stroke(PATH_ACT, width=2),
            t2_bar.animate.set_color(PATH_ACT).set_stroke(width=2.5),
            lbl_t2.animate.set_color(PATH_ACT),
            ReplacementTransform(path_act_bot1, path_act_bot2),
            lbl_vdc.animate.become(MathTex(r"v_{dc} = v_{ac}", font_size=19, color=PHASE_C).move_to([-0.75, -0.25, 0])),
            Create(v_seg1_next),
            run_time=1.0
        )
        self.wait(1.5)
        self.play(FadeOut(lbl_comm), run_time=0.4)

        # ----------------------------------------------------------------------
        # 3. Two-Column Direct Comparison at alpha = 75° (Correction 2)
        # ----------------------------------------------------------------------
        cap4 = caption_top("3. เมื่อ alpha = 75° (> 60°): เปรียบเทียบที่จุดตัด 0 V (180°) ระหว่าง 'ไม่มี L' vs 'มี L'")
        self.play(
            ReplacementTransform(cap3, cap4),
            FadeOut(circuit_grp),
            FadeOut(path_act_bot2),
            FadeOut(axes_grp_base),
            FadeOut(arrow_alpha1),
            FadeOut(lbl_alpha1),
            FadeOut(v_seg1),
            FadeOut(v_seg1_next),
            run_time=0.8
        )

        # Vertical Divider
        divider = DashedLine([0, 1.8, 0], [0, -2.4, 0], color=GRAYTXT, stroke_width=2)
        self.play(Create(divider), run_time=0.4)

        # --- LEFT PANEL: NO L (Pure R) ---
        col_l_title = Text("โหลดไม่มี L (ความต้านทาน R ล้วน)", font_size=15, color=WHITE).move_to([-3.4, 1.55, 0])
        ax_l = Axes(
            x_range=[PI/2, 7*PI/6, PI/6],
            y_range=[-0.5, 1.1, 0.5],
            x_length=5.0, y_length=2.2, tips=False
        ).move_to([-3.4, 0.35, 0])

        zline_l = DashedLine(ax_l.c2p(PI/2, 0), ax_l.c2p(7*PI/6, 0), color=GRAYTXT, stroke_width=1.2)
        pi_line_l = DashedLine(ax_l.c2p(PI, -0.4), ax_l.c2p(PI, 1.0), color=WARN, stroke_width=1.5)
        lbl_pi_l = MathTex(r"180^\circ", font_size=13, color=WARN).next_to(ax_l.c2p(PI, 0), DOWN, buff=0.15)
        lbl_0v_l = MathTex(r"0\text{ V}", font_size=13, color=GRAYTXT).next_to(ax_l.c2p(PI/2, 0), LEFT, buff=0.08)

        # Waveform R: conducts from 75° delay (3PI/4) to 180° (PI), then stays 0 V until 195°
        v_r_pos = ax_l.plot(lambda t: np.sin(t), x_range=[3*PI/4, PI], color=OK, stroke_width=3.5)
        v_r_zero = Line(ax_l.c2p(PI, 0), ax_l.c2p(13*PI/12, 0), color=GRAYTXT, stroke_width=4)

        # Current Id indicator for R: shrinks to 0 at 180°
        arr_id_r = Arrow([-4.8, -1.2, 0], [-3.8, -1.2, 0], color=CURRENT, buff=0, stroke_width=3.5)
        lbl_id_r = Text("กระแส Id ตกถึง 0 ทันที", font_size=12, color=CURRENT).next_to(arr_id_r, UP, buff=0.06)
        txt_r_res = Text("• พอแรงดันแตะ 0 V -> กระแส Id กลายเป็นศูนย์\n• SCR คู่เดิม (T1, T6) ดับทันที\n• vdc แบนราบที่ 0 V (ไม่มีทางติดลบ)", font_size=12, color=WHITE).move_to([-3.4, -1.85, 0])

        grp_left_col = VGroup(
            col_l_title, ax_l, zline_l, pi_line_l, lbl_pi_l, lbl_0v_l,
            v_r_pos, v_r_zero, arr_id_r, lbl_id_r, txt_r_res
        )

        # --- RIGHT PANEL: WITH L (RL Load) ---
        col_r_title = Text("โหลดมี L (Inductive Load RL)", font_size=15, color=WARN).move_to([3.4, 1.55, 0])
        ax_r = Axes(
            x_range=[PI/2, 7*PI/6, PI/6],
            y_range=[-0.5, 1.1, 0.5],
            x_length=5.0, y_length=2.2, tips=False
        ).move_to([3.4, 0.35, 0])

        zline_r = DashedLine(ax_r.c2p(PI/2, 0), ax_r.c2p(7*PI/6, 0), color=GRAYTXT, stroke_width=1.2)
        pi_line_r = DashedLine(ax_r.c2p(PI, -0.4), ax_r.c2p(PI, 1.0), color=WARN, stroke_width=1.5)
        lbl_pi_r = MathTex(r"180^\circ", font_size=13, color=WARN).next_to(ax_r.c2p(PI, 0), DOWN, buff=0.15)
        lbl_0v_r = MathTex(r"0\text{ V}", font_size=13, color=GRAYTXT).next_to(ax_r.c2p(PI/2, 0), LEFT, buff=0.08)

        # Waveform RL: conducts from 3PI/4, crosses 180° into negative until 13PI/12 (195°)
        v_rl_pos = ax_r.plot(lambda t: np.sin(t), x_range=[3*PI/4, PI], color=VDC_COL, stroke_width=3.5)
        v_rl_neg = ax_r.plot(lambda t: np.sin(t), x_range=[PI, 13*PI/12], color=WARN_NEG, stroke_width=4)

        thetas_neg = np.linspace(PI, 13*PI/12, 20)
        pts_neg = [ax_r.c2p(th, np.sin(th)) for th in thetas_neg]
        pts_axis = [ax_r.c2p(13*PI/12, 0), ax_r.c2p(PI, 0)]
        poly_neg = Polygon(*(pts_neg + pts_axis), color=WARN_NEG, fill_color=WARN_NEG, fill_opacity=0.5, stroke_width=0)

        tag_neg_col = MathTex(r"v_{dc}(t) < 0", font_size=15, color=WARN_NEG).next_to(ax_r.c2p(13*PI/12, -0.25), DOWN, buff=0.10)

        # Current Id indicator for RL: continues forward across 180°
        arr_id_rl = Arrow([2.0, -1.2, 0], [3.4, -1.2, 0], color=CURRENT, buff=0, stroke_width=3.5)
        lbl_id_rl = Text("Id ยังไหลทิศเดิมต่อเนื่อง!", font_size=12, color=CURRENT).next_to(arr_id_rl, UP, buff=0.06)
        txt_rl_res = Text("• L คายพลังงาน ดัน Id ไหลทิศเดิมไม่ยอมให้หยุด\n• บังคับ SCR คู่เดิม (T1, T6) เปิดค้างข้าม 180°\n• ดึงแรงดัน AC ช่วงลบมาออกโหลด -> vdc(t) < 0!", font_size=12, color=WHITE).move_to([3.4, -1.85, 0])

        grp_right_col = VGroup(
            col_r_title, ax_r, zline_r, pi_line_r, lbl_pi_r, lbl_0v_r,
            v_rl_pos, v_rl_neg, poly_neg, tag_neg_col,
            arr_id_rl, lbl_id_rl, txt_rl_res
        )

        self.play(FadeIn(grp_left_col), FadeIn(grp_right_col), run_time=1.5)

        # Flash the 180° boundary and contrast current behaviors
        dot_pi_l = Dot(ax_l.c2p(PI, 0), color=WARN, radius=0.08)
        dot_pi_r = Dot(ax_r.c2p(PI, 0), color=WARN, radius=0.08)

        self.play(
            Flash(dot_pi_l, color=WARN, flash_radius=0.3),
            Flash(dot_pi_r, color=WARN, flash_radius=0.3),
            # Left current shrinks to zero
            arr_id_r.animate.scale(0.1).set_color(GRAYTXT),
            # Right current stays strong
            Indicate(arr_id_rl, color=CURRENT, scale_factor=1.2),
            run_time=1.2
        )
        self.wait(2.5)

        # ----------------------------------------------------------------------
        # 4. Direct Cause Chain & Physics Clarification
        # ----------------------------------------------------------------------
        cap5 = caption_top("4. ห่วงโซ่สาเหตุ: L มีพลังงาน -> Id ไม่หยุด -> SCR คู่เดิมเปิดค้าง -> ลากสาย AC ที่ติดลบมาออกโหลด")
        self.play(
            ReplacementTransform(cap4, cap5),
            FadeOut(divider),
            FadeOut(grp_left_col),
            FadeOut(grp_right_col),
            FadeOut(dot_pi_l),
            FadeOut(dot_pi_r),
            run_time=0.8
        )

        # 4 Clean Flow Blocks
        box_chain = RoundedRectangle(width=12.6, height=1.0, corner_radius=0.12, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.65).move_to([0, 0.45, 0])

        c1 = Text("1. L มีพลังงานสะสม\n(E = ½ L Id²)", font_size=12, color=WHITE)
        c2 = Text("2. Id หยุดทันทีไม่ได้\n(ไหลทิศเดิมไปข้างหน้า)", font_size=12, color=CURRENT)
        c3 = Text("3. SCR คู่เดิมเปิดค้าง\n(T1, T6 ยังไม่ดับ)", font_size=12, color=PATH_ACT)
        c4 = Text("4. AC ตกข้าม 0 V สู่แดนลบ\n(vdc ติดลบชั่วขณะ)", font_size=12, color=WARN_NEG)

        arr1 = MathTex(r"\to", font_size=18, color=GRAYTXT)
        arr2 = MathTex(r"\to", font_size=18, color=GRAYTXT)
        arr3 = MathTex(r"\to", font_size=18, color=GRAYTXT)

        chain_flow = VGroup(c1, arr1, c2, arr2, c3, arr3, c4).arrange(RIGHT, buff=0.18).move_to(box_chain.get_center())

        note_id = Text("หัวใจสำคัญ: กระแส Id ยังคงไหลไปข้างหน้าทิศเดิมเสมอ ไม่ได้กลับทิศ!\n(กำลังไฟฟ้า p = vdc · Id < 0 หมายถึงพลังงานไหลย้อนกลับคืนสู่แหล่งจ่าย AC)", font_size=13, color=OK).move_to([0, -0.65, 0])

        self.play(FadeIn(box_chain), FadeIn(chain_flow), FadeIn(note_id), run_time=1.2)
        self.wait(2.5)

        # ----------------------------------------------------------------------
        # 5. Summary: Instantaneous vs Average & Formula (Correction 3)
        # ----------------------------------------------------------------------
        cap6 = caption_top("5. สรุป: vdc(t) ติดลบชั่วขณะ != ค่าเฉลี่ย Vdc ติดลบ (alpha < 90° ค่าเฉลี่ยยังเป็นบวก)")
        self.play(
            ReplacementTransform(cap5, cap6),
            FadeOut(box_chain),
            FadeOut(chain_flow),
            FadeOut(note_id),
            run_time=0.6
        )

        # Formula Card
        box_eq = RoundedRectangle(width=7.5, height=0.9, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.6).move_to([0, 1.55, 0])
        eq_vdc = MathTex(r"V_{dc} = \frac{3}{\pi} V_M \cos\alpha", font_size=30, color=OK).move_to(box_eq.get_center())

        # Side-by-Side Comparison Cards
        card_l = RoundedRectangle(width=5.8, height=1.75, corner_radius=0.12, color=WARN_NEG, fill_color=BLACK, fill_opacity=0.5).move_to([-3.2, 0.00, 0])
        hdr_l = Text("แรงดันขณะหนึ่ง vdc(t)", font_size=15, color=WARN_NEG).move_to(card_l.get_top() + DOWN * 0.24)
        txt_l = Text("• ติดลบสั้นๆ เมื่อ alpha > 60° และมี L\n• L บังคับ SCR นำข้ามจุดตัด 180°\n• Id ไหลไปข้างหน้าตามเดิม ไม่ได้กลับทิศ", font_size=12, color=WHITE).next_to(hdr_l, DOWN, buff=0.10)
        grp_l = VGroup(card_l, hdr_l, txt_l)

        card_r = RoundedRectangle(width=5.8, height=1.75, corner_radius=0.12, color=OK, fill_color=BLACK, fill_opacity=0.5).move_to([3.2, 0.00, 0])
        hdr_r = Text("แรงดันเฉลี่ย Vdc", font_size=15, color=OK).move_to(card_r.get_top() + DOWN * 0.24)
        txt_r = Text("• alpha < 90°: Vdc > 0 (Rectifier เฉลี่ยเป็นบวก)\n• alpha = 90°: Vdc = 0 (ขอบเขตเฉลี่ยศูนย์)\n• alpha > 90°: Inverter (ต้องมีไฟ DC ภายนอกหนุน)", font_size=12, color=WHITE).next_to(hdr_r, DOWN, buff=0.10)
        grp_r = VGroup(card_r, hdr_r, txt_r)

        # Alpha Range Bar
        bar_bg = RoundedRectangle(width=11.6, height=0.50, corner_radius=0.10, color=GRAYTXT, stroke_width=1.5, fill_color=BLACK, fill_opacity=0.6).move_to([0, -1.45, 0])
        t_z1 = Text("0° - 60°: vdc > 0 ทุกโหลด", font_size=12, color=OK).move_to([-3.8, -1.45, 0])
        t_z2 = Text("60° - 90°: มีช่วงลบสั้นๆ แต่เฉลี่ย > 0", font_size=12, color=WARN).move_to([0, -1.45, 0])
        t_z3 = Text("> 90°: Inverter (ต้องมีไฟ DC หนุน)", font_size=12, color=WARN_NEG).move_to([3.8, -1.45, 0])

        rule_box = Text("สรุปฟิสิกส์: ขดลวด L ไม่ได้สร้างพลังงานเอง และไม่ได้ทำให้ค่าเฉลี่ยติดลบ", font_size=13, color=GRAYTXT).move_to([0, -2.15, 0])

        self.play(
            FadeIn(box_eq), FadeIn(eq_vdc),
            FadeIn(grp_l), FadeIn(grp_r),
            FadeIn(bar_bg), FadeIn(t_z1), FadeIn(t_z2), FadeIn(t_z3),
            FadeIn(rule_box),
            run_time=1.2
        )
        self.wait(3.5)
        self.fade_out_all(run_time=0.8)
