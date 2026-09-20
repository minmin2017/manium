"""
Mechanics of Machinery — W03 Instant Center Method for Velocity Analysis
Scene: IC01_MethodsOverview (ภาพรวมวิธีวิเคราะห์ความเร็วของกลไก)
Lecture notes: W03 หน้า 1-2 (เกริ่นนำการจัดหมวดหมู่วิธีวิเคราะห์)

Pedagogical Objective:
- Correct the misconception: 'การวิเคราะห์ความเร็วของกลไกมีวิธีเดียว ต้องตั้งสมการเวกเตอร์เต็มรูปแบบเสมอ'
- Classify velocity analysis methods into 2 groups:
  1. Graphical: Vector Polygon vs Instant Center (IC - focus of this series)
  2. Analytical: Vector Equation (used for calculation) vs Vector Loop Closure (complex)
- Demonstrate the hybrid strategy: Use IC to find position/ratio relationships graphically,
  then use Vector Equations to compute exact velocity values quickly.
"""

import os
import numpy as np
from manim import *
from mlib import *

# Font configuration
Text.set_default(font=os.environ.get("MANIM_THAI_FONT", "Leelawadee UI"))

# Module colors matching project conventions
COL_METAL  = METAL       # #90A4AE
COL_FIELD  = FIELD       # #42A5F5
COL_WARN   = WARN        # #FF7043
COL_OK     = OK          # #26C6DA
COL_GRAY   = GRAYTXT     # #B0BEC5
COL_CURR   = CURRENT     # #FFB300
COL_FORCE  = FORCE       # #66BB6A
COL_BG_BOX = "#1E293B"   # Dark slate card background
COL_BAD    = "#DC2626"   # Red alert / failure color


def _ic01_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic01_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic01_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _ic01_badge(text, color):
    lbl = Text(text, font_size=9.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.40, height=0.32, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _ic01_banner(text, color):
    bg = RoundedRectangle(
        width=11.8, height=0.52, corner_radius=0.1,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.90, 0.0])
    lbl = Text(text, font_size=12, color=color).move_to(bg.get_center())
    fit_width(lbl, 11.4)
    return VGroup(bg, lbl)


class IC01_MethodsOverview(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ======================================================================
        # BEAT 0.0–1.5: Title & Page Reference
        # ======================================================================
        self.title_m = _ic01_title("Instant Center Method: ภาพรวมวิธีวิเคราะห์ความเร็ว")
        self.ref_m = _ic01_page_ref("W03 น.1-2")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)

        # ======================================================================
        # BEAT 1.5–5.5: Hook Question
        # ======================================================================
        hook_q = _ic01_caption_top(
            "การวิเคราะห์ความเร็วของกลไกมีวิธีเดียว ต้องตั้งสมการเวกเตอร์เต็มรูปแบบเสมอจริงไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 12.0)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(2.4)
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.6)

        # ======================================================================
        # BEAT 5.5–17.0: The Two Method Families (Graphical vs Analytical)
        # ======================================================================
        cap1 = _ic01_caption_top("1. มี 2 กลุ่มวิธี: Graphical (กราฟิก) และ Analytical (คำนวณ)")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Column 1: GRAPHICAL METHODS (Left: x = -3.2, y = -0.25)
        c1_x, c1_y = -3.2, -0.25
        col1_bg = RoundedRectangle(
            width=5.7, height=4.2, corner_radius=0.15,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([c1_x, c1_y, 0])

        col1_head = _ic01_badge("GRAPHICAL METHODS (วิธีทางกราฟิก)", COL_FIELD).move_to([c1_x, c1_y + 1.70, 0])

        # Method 1: Vector Polygon (Unused in this chapter - Gray / Muted)
        box_poly = RoundedRectangle(
            width=5.1, height=1.15, corner_radius=0.10,
            color=COL_GRAY, stroke_width=1.2, fill_color="#0F172A"
        ).set_fill("#0F172A", 0.9).move_to([c1_x, c1_y + 0.80, 0])
        t_poly = Text("1. Vector Polygon", font_size=11.5, color=COL_GRAY, weight=BOLD)
        b_poly = _ic01_badge("ไม่ได้เน้นในบทนี้", COL_GRAY)
        head_poly = VGroup(t_poly, b_poly).arrange(RIGHT, buff=0.25).move_to([c1_x, c1_y + 1.05, 0])
        d_poly = Text("(รูปหลายเหลี่ยมเวกเตอร์: ต้องใช้วงเวียน/ไม้บรรทัดวาดสเกล)", font_size=9.0, color="#64748B").move_to([c1_x, c1_y + 0.65, 0])
        vec_poly_grp = VGroup(box_poly, head_poly, d_poly)

        # Method 2: Instant Center (IC) (§34 Highlighted - Bright Green Border & Teal Fill!)
        ic_box = RoundedRectangle(
            width=5.1, height=1.45, corner_radius=0.12,
            color=COL_OK, stroke_width=2.6, fill_color="#0F766E"
        ).set_fill("#0F766E", 0.35).move_to([c1_x, c1_y - 0.70, 0])
        t_ic = Text("2. Instant Center (IC)", font_size=12.0, color=WHITE, weight=BOLD)
        b_ic = _ic01_badge("⭐ ใช้ในบทนี้เป็นหลัก", COL_OK)
        head_ic = VGroup(t_ic, b_ic).arrange(RIGHT, buff=0.25).move_to([c1_x, c1_y - 0.35, 0])
        d_ic1 = Text("• หาจุดหมุนที่ความเร็วสัมบูรณ์เป็นศูนย์ (Zero Velocity)", font_size=9.5, color=WHITE).move_to([c1_x, c1_y - 0.68, 0])
        d_ic2 = Text("• เทียบสัดส่วนระยะทาง หาความเร็วได้ทันที รวดเร็วมาก", font_size=9.5, color=COL_OK).move_to([c1_x, c1_y - 0.95, 0])
        ic_grp = VGroup(ic_box, head_ic, d_ic1, d_ic2)

        col_graphical = VGroup(col1_bg, col1_head, vec_poly_grp, ic_grp)

        # Column 2: ANALYTICAL METHODS (Right: x = +3.2, y = -0.25)
        c2_x, c2_y = 3.2, -0.25
        col2_bg = RoundedRectangle(
            width=5.7, height=4.2, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([c2_x, c2_y, 0])

        col2_head = _ic01_badge("ANALYTICAL METHODS (วิธีคำนวณ)", COL_WARN).move_to([c2_x, c2_y + 1.70, 0])

        # Method 1: Vector Equation (§34 Highlighted - Bright Green Border & Teal Fill!)
        vec_eq_box = RoundedRectangle(
            width=5.1, height=1.45, corner_radius=0.12,
            color=COL_OK, stroke_width=2.6, fill_color="#0F766E"
        ).set_fill("#0F766E", 0.35).move_to([c2_x, c2_y + 0.65, 0])
        t_ve = Text("1. Vector Equation", font_size=12.0, color=WHITE, weight=BOLD)
        b_ve = _ic01_badge("⭐ ใช้คำนวณตัวเลขจริง", COL_OK)
        head_ve = VGroup(t_ve, b_ve).arrange(RIGHT, buff=0.25).move_to([c2_x, c2_y + 0.97, 0])
        d_ve1 = Text("• ใช้สมการความเร็วสัมพัทธ์:  v_B = v_A + v_B/A", font_size=9.5, color=WHITE).move_to([c2_x, c2_y + 0.67, 0])
        d_ve2 = Text("• นำขนาดและทิศทางมาคำนวณ ได้ผลลัพธ์เป็นตัวเลขแม่นยำ", font_size=9.5, color=COL_OK).move_to([c2_x, c2_y + 0.40, 0])
        vec_eq_grp = VGroup(vec_eq_box, head_ve, d_ve1, d_ve2)

        # Method 2: Vector Loop Closure (Unused in this chapter - Gray / Muted)
        box_loop = RoundedRectangle(
            width=5.1, height=1.15, corner_radius=0.10,
            color=COL_GRAY, stroke_width=1.2, fill_color="#0F172A"
        ).set_fill("#0F172A", 0.9).move_to([c2_x, c2_y - 0.80, 0])
        t_loop = Text("2. Vector Loop Closure", font_size=11.5, color=COL_GRAY, weight=BOLD)
        b_loop = _ic01_badge("ซับซ้อนกว่า ไม่ใช้ในบทนี้", COL_GRAY)
        head_loop = VGroup(t_loop, b_loop).arrange(RIGHT, buff=0.25).move_to([c2_x, c2_y - 0.55, 0])
        d_loop = Text("(สมการวงปิดเวกเตอร์รูปจำนวนเชิงซ้อน e^(iθ) ซับซ้อนเกินไป)", font_size=9.0, color="#64748B").move_to([c2_x, c2_y - 0.95, 0])
        vec_loop_grp = VGroup(box_loop, head_loop, d_loop)

        col_analytical = VGroup(col2_bg, col2_head, vec_eq_grp, vec_loop_grp)

        banner1 = _ic01_banner(
            "Graphical: Vector Polygon กับ Instant Center (IC) — Analytical: Vector Equation กับ Vector Loop Closure — บทนี้ใช้ IC + Vector Equation",
            COL_OK
        )

        columns_grp = VGroup(col_graphical, col_analytical)

        self.play(FadeIn(columns_grp, shift=UP * 0.25), FadeIn(banner1), run_time=1.0)
        self.play(Indicate(ic_box, color=COL_OK), run_time=0.7)
        self.play(Indicate(vec_eq_box, color=COL_OK), run_time=0.7)
        self.wait(8.5)

        self.fade_out_all(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 17.6–23.5: Method Integration Workflow (Hybrid Strategy)
        # ======================================================================
        cap2 = _ic01_caption_top("2. บทนี้ผสม 2 วิธีเข้าด้วยกัน ไม่แยกกันเด็ดขาด")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Integration Flowchart: 4 horizontal nodes with arrows
        card_flow_box = RoundedRectangle(
            width=11.6, height=3.8, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.25, 0])

        card_flow_head = _ic01_badge("ขั้นตอนการวิเคราะห์: ผสมผสาน IC (กราฟิก) + Vector Equation (คำนวณ)", COL_OK).move_to([0.0, 1.35, 0])

        # Step 1: IC Box
        node1_box = RoundedRectangle(width=2.4, height=1.5, corner_radius=0.12, color=COL_FIELD, fill_color="#0F172A").set_fill("#0F172A", 1.0).move_to([-4.35, -0.35, 0])
        node1_title = Text("Instant Center (IC)", font_size=11, color=COL_FIELD, weight=BOLD).move_to([-4.35, 0.10, 0])
        node1_badge = _ic01_badge("วิธีทางกราฟิก", COL_FIELD).move_to([-4.35, -0.22, 0])
        node1_sub = Text("มองเห็นภาพรวม", font_size=9, color=COL_GRAY).move_to([-4.35, -0.65, 0])
        node1_grp = VGroup(node1_box, node1_title, node1_badge, node1_sub)

        # Arrow 1
        arr1 = Arrow(start=[-3.05, -0.35, 0], end=[-2.05, -0.35, 0], color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.35)

        # Step 2: Relation Box
        node2_box = RoundedRectangle(width=2.4, height=1.5, corner_radius=0.12, color=COL_CURR, fill_color="#0F172A").set_fill("#0F172A", 1.0).move_to([-1.05, -0.35, 0])
        node2_title = Text("1. หาความสัมพันธ์", font_size=11, color=COL_CURR, weight=BOLD).move_to([-1.05, 0.10, 0])
        node2_sub1 = Text("ระบุตำแหน่งจุดหมุน", font_size=9.5, color=WHITE).move_to([-1.05, -0.22, 0])
        node2_sub2 = Text("และสัดส่วนระยะทาง", font_size=9.5, color=COL_CURR).move_to([-1.05, -0.55, 0])
        node2_grp = VGroup(node2_box, node2_title, node2_sub1, node2_sub2)

        # Arrow 2
        arr2 = Arrow(start=[0.25, -0.35, 0], end=[1.25, -0.35, 0], color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.35)

        # Step 3: Vector Equation Box
        node3_box = RoundedRectangle(width=2.4, height=1.5, corner_radius=0.12, color=COL_WARN, fill_color="#0F172A").set_fill("#0F172A", 1.0).move_to([2.25, -0.35, 0])
        node3_title = Text("Vector Equation", font_size=11, color=COL_WARN, weight=BOLD).move_to([2.25, 0.10, 0])
        node3_badge = _ic01_badge("วิธีคำนวณ", COL_WARN).move_to([2.25, -0.22, 0])
        node3_sub = Text("สมการความเร็วสัมพัทธ์", font_size=9, color=COL_GRAY).move_to([2.25, -0.65, 0])
        node3_grp = VGroup(node3_box, node3_title, node3_badge, node3_sub)

        # Arrow 3
        arr3 = Arrow(start=[3.55, -0.35, 0], end=[4.55, -0.35, 0], color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.35)

        # Step 4: Final Speed Number Result
        node4_box = RoundedRectangle(width=2.4, height=1.5, corner_radius=0.12, color=COL_OK, fill_color="#0F766E").set_fill("#0F766E", 0.4).move_to([5.55, -0.35, 0])
        node4_title = Text("2. คำนวณตัวเลขจริง", font_size=11, color=COL_OK, weight=BOLD).move_to([5.55, 0.10, 0])
        node4_sub1 = Text("ได้ความเร็วแม่นยำ", font_size=9.5, color=WHITE).move_to([5.55, -0.22, 0])
        node4_sub2 = Text("v = ωr (รวดเร็วมาก)", font_size=9.5, color=YELLOW, weight=BOLD).move_to([5.55, -0.55, 0])
        node4_grp = VGroup(node4_box, node4_title, node4_sub1, node4_sub2)

        flow_nodes = VGroup(node1_grp, arr1, node2_grp, arr2, node3_grp, arr3, node4_grp)
        flow_nodes.move_to([0.0, -0.35, 0])

        flow_grp = VGroup(card_flow_box, card_flow_head, flow_nodes)

        banner2 = _ic01_banner(
            "ใช้ IC หาความสัมพันธ์ตำแหน่งก่อน แล้วใช้สมการเวกเตอร์คำนวณตัวเลขจริง — สองวิธีเสริมกัน ไม่ใช่แยกกัน",
            COL_OK
        )

        self.play(FadeIn(flow_grp, shift=UP * 0.25), FadeIn(banner2), run_time=1.0)
        self.wait(4.3)

        self.fade_out_all(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 24.1–26.0: Summary Card
        # ======================================================================
        card_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: ภาพรวมวิธีวิเคราะห์ความเร็ว (Mechanics of Machinery: W03 น.1-2)", font_size=13.0, color=COL_OK).move_to([0.0, 1.35, 0.0])
        rows = [
            "1. สองกลุ่มหลัก: Graphical (Vector Polygon, IC) และ Analytical (Vector Equation, Loop Closure)",
            "2. ยุทธศาสตร์บทนี้: ใช้ Instant Center (IC) จัดสัดส่วนตำแหน่ง แล้วนำ Vector Equation คำนวณตัวเลข",
            "3. จุดเด่นการผสมวิธี: เร็วกว่าตั้งสมการเต็มรูป เห็นภาพการเคลื่อนที่ชัดเจน และได้ผลลัพธ์แม่นยำ"
        ]
        s_rows = VGroup(*[Text(r, font_size=11.5, color=WHITE) for r in rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.0, -0.15, 0.0])
        fit_width(s_rows, 10.8)
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.6)
        self.wait(1.3)

        # ======================================================================
        # BEAT 26.0–27.5: Review Question Card
        # ======================================================================
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "ทำไมบทนี้ถึงไม่ใช้วิธี Vector Loop Closure ทั้งที่เป็นวิธี Analytical เหมือนกัน?",
            font_size=12.0, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text(
            "(คำตอบ: Vector Loop Closure ต้องตั้งสมการจำนวนเชิงซ้อนและแก้ระบบสมการไม่เชิงเส้นที่ซับซ้อนมาก\nขณะที่การใช้ IC ร่วมกับ Vector Equation ให้ผลลัพธ์รวดเร็ว ตรงไปตรงมา และเห็นภาพชัดเจนกว่า)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        fit_width(q_ans, 10.6)
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(question_grp), run_time=0.5)
        self.wait(0.2)
        self.fade_out_all(run_time=0.6)
        self.wait(0.5)
