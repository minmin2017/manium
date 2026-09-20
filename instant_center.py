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



def _ic02_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic02_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic02_caption_top(text, color=WHITE):
    return Text(text, font_size=13.5, color=color).move_to([0.0, 2.45, 0.0])


def _ic02_badge(text, color):
    lbl = Text(text, font_size=9.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.36, height=0.30, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _ic02_banner(text, color=COL_OK):
    bg = RoundedRectangle(
        width=11.8, height=0.52, corner_radius=0.1,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.90, 0.0])
    lbl = Text(text, font_size=11.5, color=color).move_to(bg.get_center())
    fit_width(lbl, 11.4)
    return VGroup(bg, lbl)


class IC02_RelativeMotionReview(SafeScene):
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
        # BEAT 0.0–1.6: Title & Page Reference
        # ======================================================================
        self.title_m = _ic02_title("ทบทวน Relative Motion + จุดเริ่มต้นของ IC")
        self.ref_m = _ic02_page_ref("W03 น.3-6")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.4)

        # ======================================================================
        # BEAT 1.6–4.6: Hook Question Card
        # ======================================================================
        hook_box = RoundedRectangle(
            width=10.2, height=2.3, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        hook_badge = _ic02_badge("คำถามชวนคิดก่อนเริ่ม (Misconception)", COL_WARN).move_to([0.0, 0.70, 0.0])
        hook_text = Text(
            "จุดสองจุดบนวัตถุแกร่งชิ้นเดียวกัน เคลื่อนที่ด้วยความเร็วเท่ากันเสมอไหม?",
            font_size=13.5, color=WHITE, weight=BOLD
        ).move_to([0.0, 0.12, 0.0])
        fit_width(hook_text, 9.6)
        hook_sub = Text(
            "(หลายคนคิดว่าเมื่อเป็นวัตถุชิ้นเดียวกัน ทุกจุดต้องวิ่งเร็วเท่ากันตลอดเวลา — จริงหรือไม่?)",
            font_size=10.5, color=COL_GRAY
        ).move_to([0.0, -0.42, 0.0])
        fit_width(hook_sub, 9.6)
        hook_card = VGroup(hook_box, hook_badge, hook_text, hook_sub)

        self.play(FadeIn(hook_card, shift=UP * 0.3), run_time=0.7)
        self.wait(1.9)
        self.play(FadeOut(hook_card), run_time=0.4)

        # ======================================================================
        # BEAT 4.6–13.6: Relative Motion Equation on Rigid Link AB
        # ======================================================================
        cap1 = _ic02_caption_top("สมการพื้นฐาน: v_B = v_A + v_(B/A) — โดย v_(B/A) = ω × r_(B/A) (A คือจุดฐาน)")
        fit_width(cap1, 11.8)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Rigid rod AB (Left side: center x = -3.4, y = -0.2)
        pt_A = np.array([-4.8, -1.1, 0.0])
        pt_B = np.array([-2.0, 0.7, 0.0])
        r_BA = pt_B - pt_A
        L_BA = np.linalg.norm(r_BA)
        u_BA = r_BA / L_BA
        n_BA = np.array([-u_BA[1], u_BA[0], 0.0])  # perpendicular CCW (+90 deg)

        rod_line = Line(start=pt_A, end=pt_B, stroke_width=7, color=COL_METAL)
        dot_A = Dot(pt_A, radius=0.09, color=WHITE)
        dot_B = Dot(pt_B, radius=0.09, color=WHITE)
        lbl_A = Text("A (Base Point)", font_size=10.5, color=WHITE).next_to(dot_A, DOWN + LEFT, buff=0.10)
        lbl_B = Text("B", font_size=11, color=WHITE).next_to(dot_B, UP, buff=0.15)
        rod_grp = VGroup(rod_line, dot_A, dot_B, lbl_A, lbl_B)

        # Vector v_A (horizontal green arrow at A)
        vA_vec = np.array([1.6, 0.0, 0.0])
        vA_arrow = Arrow(start=pt_A, end=pt_A + vA_vec, buff=0, color=COL_FORCE, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        vA_lbl = Text("v_A (รู้ค่าแล้ว)", font_size=10, color=COL_FORCE).next_to(vA_arrow, DOWN, buff=0.10).shift(RIGHT * 0.25)

        # Angular velocity arc at midpoint
        mid_pt = (pt_A + pt_B) / 2
        omega_arc = Arc(radius=0.42, start_angle=-0.5, angle=1.8, arc_center=mid_pt, color=COL_CURR)
        omega_arc.add_tip(tip_length=0.16)
        omega_lbl = Text("ω (⊥ ระนาบ 2D)", font_size=9.5, color=COL_CURR).next_to(mid_pt, UP + LEFT, buff=0.12)

        # Relative velocity v_(B/A) (perpendicular to AB at B, orange)
        vBA_vec = 1.45 * n_BA
        vBA_arrow = Arrow(start=pt_B, end=pt_B + vBA_vec, buff=0, color=COL_WARN, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        vBA_lbl = Text("v_(B/A) = ω × r_(B/A)", font_size=9.5, color=COL_WARN).next_to(vBA_arrow.get_end(), UP + RIGHT, buff=0.08)

        # Resultant v_B at point B (blue)
        vB_vec = vA_vec + vBA_vec
        vB_arrow = Arrow(start=pt_B, end=pt_B + vB_vec, buff=0, color=COL_FIELD, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        vB_lbl = Text("v_B (ความเร็วสัมบูรณ์)", font_size=10, color=COL_FIELD).next_to(vB_arrow.get_end(), RIGHT, buff=0.10)

        # Right side: Vector Addition Triangle Card
        c1_x, c1_y = 3.2, -0.25
        tri_card_box = RoundedRectangle(
            width=5.8, height=3.9, corner_radius=0.15,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([c1_x, c1_y, 0])
        tri_card_head = _ic02_badge("การบวกเวกเตอร์: Tip-to-Tail", COL_FIELD).move_to([c1_x, c1_y + 1.60, 0])

        t_ov = np.array([1.6, -0.95, 0.0])
        tri_vA = Arrow(start=t_ov, end=t_ov + np.array([1.7, 0, 0]), buff=0, color=COL_FORCE, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        tri_vA_lbl = Text("v_A", font_size=10.5, color=COL_FORCE).next_to(tri_vA, DOWN, buff=0.08)

        tri_vBA_start = t_ov + np.array([1.7, 0, 0])
        tri_vBA = Arrow(start=tri_vBA_start, end=tri_vBA_start + 1.55 * n_BA, buff=0, color=COL_WARN, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        tri_vBA_lbl = Text("v_(B/A)", font_size=10.5, color=COL_WARN).next_to(tri_vBA.get_center(), RIGHT, buff=0.10)

        tri_vB = Arrow(start=t_ov, end=tri_vBA_start + 1.55 * n_BA, buff=0, color=COL_FIELD, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        tri_vB_lbl = Text("v_B", font_size=11, color=COL_FIELD, weight=BOLD).next_to(tri_vB.get_center(), UP + LEFT, buff=0.08)

        tri_eq1 = Text("v_B = v_A + v_(B/A)", font_size=11.5, color=WHITE, weight=BOLD).move_to([c1_x, c1_y + 1.05, 0])
        tri_eq2 = Text("v_(B/A) = ω · r_(B/A)  (⊥ แนวเส้น AB)", font_size=10, color=COL_WARN).move_to([c1_x, c1_y + 0.70, 0])

        tri_card_grp = VGroup(tri_card_box, tri_card_head, tri_eq1, tri_eq2, tri_vA, tri_vA_lbl, tri_vBA, tri_vBA_lbl, tri_vB, tri_vB_lbl)

        banner1 = _ic02_banner("ความเร็วสัมพัทธ์ v_(B/A) เกิดจากการหมุนรอบจุด A: ทิศทางตั้งฉากกับแนวเส้น AB เสมอ", COL_OK)

        self.play(Create(rod_grp), run_time=0.6)
        self.play(GrowArrow(vA_arrow), FadeIn(vA_lbl), run_time=0.5)
        self.play(Create(omega_arc), FadeIn(omega_lbl), run_time=0.5)
        self.play(GrowArrow(vBA_arrow), FadeIn(vBA_lbl), run_time=0.6)
        self.play(FadeIn(tri_card_grp), GrowArrow(vB_arrow), FadeIn(vB_lbl), run_time=1.0)
        self.play(FadeIn(banner1), run_time=0.5)
        self.wait(3.7)

        self.clear_stage(run_time=0.6)
        self.wait(0.1)

        # ======================================================================
        # BEAT 13.6–20.1: Relative Angular Velocity Between 2 Links
        # ======================================================================
        cap2 = _ic02_caption_top("ลิงก์ 2 ชิ้นก็มีความเร็วเชิงมุมสัมพัทธ์กันได้: ω₂₃ = ω₂ − ω₃")
        fit_width(cap2, 11.8)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Fixed ground reference a-a (Link 1)
        g_y = -1.45
        line_aa = Line(start=[-5.8, g_y, 0], end=[-0.5, g_y, 0], color=COL_GRAY, stroke_width=2.5)
        lbl_aa = Text("เส้นอ้างอิงคงที่ a–a (Link 1: Fixed Ground)", font_size=9.5, color=COL_GRAY).next_to(line_aa, DOWN, buff=0.35)

        # Hatching slashes under line a-a
        hatches = VGroup(*[
            Line(start=[x, g_y, 0], end=[x - 0.18, g_y - 0.22, 0], color="#64748B", stroke_width=1.5)
            for x in np.linspace(-5.6, -0.7, 12)
        ])
        ref_ground = VGroup(line_aa, hatches, lbl_aa)

        # Link 2 (Light Blue)
        o2 = np.array([-4.6, g_y, 0])
        ang2 = np.radians(65)
        len2 = 2.1
        tip2 = o2 + np.array([len2 * np.cos(ang2), len2 * np.sin(ang2), 0])
        rod2 = Line(start=o2, end=tip2, stroke_width=6, color=COL_FIELD)
        dot_o2 = Dot(o2, radius=0.07, color=WHITE)
        dot_tip2 = Dot(tip2, radius=0.07, color=COL_FIELD)
        lbl_link2 = Text("Link 2", font_size=10.5, color=COL_FIELD, weight=BOLD).next_to(tip2, UP, buff=0.1)
        arc_w2 = Arc(radius=0.9, start_angle=0, angle=ang2, arc_center=o2, color=COL_FIELD)
        arc_w2.add_tip(tip_length=0.14)
        lbl_w2 = Text("ω₂", font_size=11, color=COL_FIELD).move_to(o2 + np.array([0.75, 0.45, 0]))
        link2_grp = VGroup(rod2, dot_o2, dot_tip2, lbl_link2, arc_w2, lbl_w2)

        # Link 3 (Purple/Violet)
        COL_L3 = "#BA68C8"
        o3 = np.array([-2.1, g_y, 0])
        ang3 = np.radians(35)
        len3 = 2.1
        tip3 = o3 + np.array([len3 * np.cos(ang3), len3 * np.sin(ang3), 0])
        rod3 = Line(start=o3, end=tip3, stroke_width=6, color=COL_L3)
        dot_o3 = Dot(o3, radius=0.07, color=WHITE)
        dot_tip3 = Dot(tip3, radius=0.07, color=COL_L3)
        lbl_link3 = Text("Link 3", font_size=10.5, color=COL_L3, weight=BOLD).next_to(tip3, UP + RIGHT, buff=0.08)
        arc_w3 = Arc(radius=1.2, start_angle=0, angle=ang3, arc_center=o3, color=COL_L3)
        arc_w3.add_tip(tip_length=0.14)
        lbl_w3 = Text("ω₃", font_size=11, color=COL_L3).move_to(o3 + np.array([1.05, 0.30, 0]))
        link3_grp = VGroup(rod3, dot_o3, dot_tip3, lbl_link3, arc_w3, lbl_w3)

        # Right side: Formula Card
        c2_x, c2_y = 3.2, -0.25
        card2_box = RoundedRectangle(
            width=5.8, height=3.9, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([c2_x, c2_y, 0])
        card2_head = _ic02_badge("Relative Angular Velocity (W03 น.5)", COL_WARN).move_to([c2_x, c2_y + 1.60, 0])

        d_w2 = Text("• ω₂ = ความเร็วเชิงมุม Link 2 เทียบเส้นคงที่ a–a", font_size=9.5, color=WHITE).move_to([c2_x, c2_y + 1.05, 0])
        fit_width(d_w2, 5.4)
        d_w3 = Text("• ω₃ = ความเร็วเชิงมุม Link 3 เทียบเส้นคงที่ a–a", font_size=9.5, color=WHITE).move_to([c2_x, c2_y + 0.65, 0])
        fit_width(d_w3, 5.4)

        # Highlight formula box
        f_box = RoundedRectangle(
            width=5.0, height=1.05, corner_radius=0.10,
            color=COL_OK, stroke_width=2.2, fill_color="#0F766E"
        ).set_fill("#0F766E", 0.35).move_to([c2_x, c2_y - 0.15, 0])
        f_text = Text("ω₂₃ = ω₂ − ω₃", font_size=15, color=YELLOW, weight=BOLD).move_to([c2_x, c2_y + 0.05, 0])
        f_sub = Text("(ความเร็วเชิงมุมของ Link 2 เทียบกับ Link 3)", font_size=9.5, color=COL_OK).move_to([c2_x, c2_y - 0.35, 0])
        f_grp = VGroup(f_box, f_text, f_sub)

        d_rule = Text("กำหนดทิศทาง: ทวนเข็มนาฬิกา (+), ตามเข็มนาฬิกา (-)", font_size=9.0, color=COL_GRAY).move_to([c2_x, c2_y - 1.15, 0])
        fit_width(d_rule, 5.4)

        card2_grp = VGroup(card2_box, card2_head, d_w2, d_w3, f_grp, d_rule)

        banner2 = _ic02_banner("ω₂ กับ ω₃ วัดเทียบกับเส้นอ้างอิงคงที่ a–a บนพื้น (Link 1) → ω₂₃ = ω₂ − ω₃", COL_OK)

        self.play(Create(ref_ground), FadeIn(link2_grp, shift=LEFT * 0.2), FadeIn(link3_grp, shift=RIGHT * 0.2), run_time=0.9)
        self.play(FadeIn(card2_grp, shift=UP * 0.25), run_time=0.8)
        self.play(FadeIn(banner2), run_time=0.5)
        self.wait(3.6)

        self.clear_stage(run_time=0.6)
        self.wait(0.1)

        # ======================================================================
        # BEAT 20.1–36.6: Rolling Disk Example (page-06.jpg)
        # ======================================================================
        cap3 = _ic02_caption_top("ตัวอย่าง: ล้อรัศมี r = 0.5 m กลิ้งไม่ลื่นไถล (No slip) ด้วย v_G = 10 m/s หา v_P ที่ θ = 45°")
        fit_width(cap3, 11.8)
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        # Rolling Disk on the left (Center G: x = -3.7, y = -0.55, R_vis = 1.45)
        d_x, d_y = -3.7, -0.55
        R_vis = 1.45
        pt_G = np.array([d_x, d_y, 0.0])
        pt_A_disk = np.array([d_x, d_y - R_vis, 0.0])

        disk_circle = Circle(radius=R_vis, color=COL_FIELD, stroke_width=3.5).move_to(pt_G)
        disk_fill = Circle(radius=R_vis, stroke_width=0, fill_color="#0F172A").set_fill("#0F172A", 0.6).move_to(pt_G)

        # Ground line under disk
        ground_disk = Line(start=[-5.8, d_y - R_vis, 0], end=[-1.5, d_y - R_vis, 0], color=COL_GRAY, stroke_width=2.5)
        ground_hatches = VGroup(*[
            Line(start=[x, d_y - R_vis, 0], end=[x - 0.15, d_y - R_vis - 0.18, 0], color="#64748B", stroke_width=1.5)
            for x in np.linspace(-5.6, -1.7, 10)
        ])

        # Point A (Contact Point, No slip)
        dot_A_disk = Dot(pt_A_disk, radius=0.08, color=COL_OK)
        lbl_A_disk = Text("A (No slip)", font_size=10, color=COL_OK, weight=BOLD).next_to(dot_A_disk, DOWN, buff=0.25)

        # Center G and horizontal velocity v_G
        dot_G = Dot(pt_G, radius=0.08, color=WHITE)
        lbl_G = Text("G", font_size=11, color=WHITE).next_to(dot_G, DOWN + LEFT, buff=0.08)
        vG_arrow = Arrow(start=pt_G, end=pt_G + np.array([1.35, 0, 0]), buff=0, color=COL_FORCE, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        vG_lbl = Text("v_G = 10 m/s", font_size=10, color=COL_FORCE).next_to(vG_arrow, UP, buff=0.10).shift(RIGHT * 0.15)

        # Clockwise rotation omega
        arc_w_disk = Arc(radius=0.55, start_angle=np.radians(200), angle=-np.radians(110), arc_center=pt_G, color=COL_CURR)
        arc_w_disk.add_tip(tip_length=0.14)
        lbl_w_disk = Text("ω = 20 rad/s", font_size=9.5, color=COL_CURR).next_to(arc_w_disk, LEFT, buff=0.10)

        # Vertical reference line from G to top
        top_ref_pt = pt_G + np.array([0, R_vis, 0])
        vert_line = DashedLine(start=pt_G, end=top_ref_pt, color=COL_GRAY, stroke_width=1.5)

        # Point P at theta = 45 deg from vertical top towards upper-left (polar 135 deg)
        ang_P = np.radians(135)
        pt_P = pt_G + np.array([R_vis * np.cos(ang_P), R_vis * np.sin(ang_P), 0])
        rad_GP = Line(start=pt_G, end=pt_P, color=COL_METAL, stroke_width=2.0)
        dot_P = Dot(pt_P, radius=0.08, color=WHITE)
        lbl_P = Text("P", font_size=11, color=WHITE).next_to(dot_P, UP + LEFT, buff=0.08)

        # Angle theta = 45 arc
        arc_theta = Arc(radius=0.60, start_angle=np.radians(90), angle=np.radians(45), arc_center=pt_G, color=COL_CURR)
        lbl_theta = Text("θ=45°", font_size=9, color=COL_CURR).move_to(pt_G + np.array([-0.30, 0.72, 0]))

        # Relative velocity v_(P/G) at P: perpendicular to GP, pointing up-right (+45 deg), length 1.35
        vPG_dir = np.array([np.cos(np.radians(45)), np.sin(np.radians(45)), 0])
        vPG_arrow = Arrow(start=pt_P, end=pt_P + 1.35 * vPG_dir, buff=0, color=COL_WARN, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        vPG_lbl = Text("v_(P/G) = 10 m/s", font_size=9.5, color=COL_WARN).next_to(vPG_arrow.get_end(), UP + RIGHT, buff=0.08)

        disk_mobs = VGroup(
            disk_fill, disk_circle, ground_disk, ground_hatches,
            dot_A_disk, lbl_A_disk, dot_G, lbl_G, vG_arrow, vG_lbl,
            arc_w_disk, lbl_w_disk, vert_line, rad_GP, dot_P, lbl_P,
            arc_theta, lbl_theta, vPG_arrow, vPG_lbl
        )

        # Right side: Vector Triangle Inset & Law of Cosines Card
        c3_x, c3_y = 3.1, -0.25
        card3_box = RoundedRectangle(
            width=6.0, height=4.2, corner_radius=0.15,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([c3_x, c3_y, 0])
        card3_head = _ic02_badge("Vector Triangle & Law of Cosines (น.6)", COL_FIELD).move_to([c3_x, c3_y + 1.75, 0])

        # Formulas at top of card
        calc_w = Text("ω = v_G / r = 10 / 0.5 = 20 rad/s (CW)", font_size=9.5, color=WHITE).move_to([c3_x, c3_y + 1.30, 0])
        calc_vPG = Text("v_(P/G) = ω · r_(P/G) = (20)(0.5) = 10 m/s (⊥ GP)", font_size=9.5, color=COL_WARN).move_to([c3_x, c3_y + 0.95, 0])

        # Vector Triangle Construction
        # O_v origin
        o_v = np.array([1.1, -0.85, 0.0])
        tri_vG = Arrow(start=o_v, end=o_v + np.array([1.6, 0, 0]), buff=0, color=COL_FORCE, stroke_width=3.6, max_tip_length_to_length_ratio=0.25)
        tri_vG_lbl = Text("v_G = 10", font_size=10, color=COL_FORCE).next_to(tri_vG, DOWN, buff=0.08)

        # Tip of v_G
        tip_vG = o_v + np.array([1.6, 0, 0])
        tri_vPG = Arrow(start=tip_vG, end=tip_vG + 1.6 * vPG_dir, buff=0, color=COL_WARN, stroke_width=3.6, max_tip_length_to_length_ratio=0.25)
        tri_vPG_lbl = Text("v_(P/G) = 10", font_size=10, color=COL_WARN).next_to(tri_vPG.get_center(), RIGHT, buff=0.12)

        # Horizontal dashed extension to show 45 deg angle
        tri_dash = DashedLine(start=tip_vG, end=tip_vG + np.array([0.9, 0, 0]), color=COL_GRAY, stroke_width=1.5)
        tri_arc45 = Arc(radius=0.45, start_angle=0, angle=np.radians(45), arc_center=tip_vG, color=COL_CURR)
        tri_lbl45 = Text("45°", font_size=9, color=COL_CURR).move_to(tip_vG + np.array([0.65, 0.18, 0]))

        # Resultant v_P from o_v to tip of tri_vPG
        tip_tri_vPG = tip_vG + 1.6 * vPG_dir
        tri_vP = Arrow(start=o_v, end=tip_tri_vPG, buff=0, color=COL_FIELD, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        tri_vP_lbl = Text("v_P", font_size=11, color=COL_FIELD, weight=BOLD).next_to(tri_vP.get_center(), UP + LEFT, buff=0.10)

        # Law of Cosines Equation Box (Opposite angle is 180 - 45 = 135 deg!)
        cos_eq_box = RoundedRectangle(
            width=5.4, height=0.92, corner_radius=0.08,
            color=COL_OK, stroke_width=2.0, fill_color="#0F766E"
        ).set_fill("#0F766E", 0.35).move_to([c3_x, c3_y - 1.45, 0])
        cos_eq1 = Text("v_P = √(10² + 10² − 2(10)(10) cos 135°)", font_size=10.5, color=YELLOW, weight=BOLD).move_to([c3_x, c3_y - 1.30, 0])
        fit_width(cos_eq1, 5.2)
        cos_eq2 = Text("v_P = √(200 − 200(−0.707)) = 18.5 m/s", font_size=11, color=WHITE, weight=BOLD).move_to([c3_x, c3_y - 1.60, 0])
        fit_width(cos_eq2, 5.2)
        cos_res_grp = VGroup(cos_eq_box, cos_eq1, cos_eq2)

        card3_grp = VGroup(
            card3_box, card3_head, calc_w, calc_vPG,
            tri_vG, tri_vG_lbl, tri_vPG, tri_vPG_lbl, tri_dash, tri_arc45, tri_lbl45,
            tri_vP, tri_vP_lbl, cos_res_grp
        )

        banner3 = _ic02_banner("สามเหลี่ยมเวกเตอร์: มุมภายใน = 180° − 45° = 135° → กฎโคไซน์ได้ v_P = 18.5 m/s", COL_OK)

        self.play(FadeIn(disk_fill), Create(disk_circle), Create(ground_disk), Create(ground_hatches), FadeIn(dot_A_disk), FadeIn(lbl_A_disk), run_time=0.8)
        self.play(FadeIn(dot_G), FadeIn(lbl_G), GrowArrow(vG_arrow), FadeIn(vG_lbl), Create(arc_w_disk), FadeIn(lbl_w_disk), run_time=0.8)
        self.play(Create(vert_line), Create(rad_GP), FadeIn(dot_P), FadeIn(lbl_P), Create(arc_theta), FadeIn(lbl_theta), run_time=0.8)
        self.play(GrowArrow(vPG_arrow), FadeIn(vPG_lbl), run_time=0.6)
        self.play(FadeIn(card3_grp), run_time=1.2)
        self.play(FadeIn(banner3), run_time=0.5)
        self.wait(5.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ======================================================================
        # BEAT 36.6–40.2: Rigid Body Rule Card
        # ======================================================================
        rule_box = RoundedRectangle(
            width=11.6, height=4.1, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        rule_head = Text(
            "กฎสำคัญของการเคลื่อนที่ของวัตถุแกร่ง (Rigid Body Motion Rules)",
            font_size=13.5, color=COL_OK, weight=BOLD
        ).move_to([0.0, 1.45, 0.0])

        b_r1 = _ic02_badge("กฎข้อที่ 1: การหมุน (Rotation)", COL_FIELD).move_to([-3.4, 0.85, 0.0])
        t_r1 = Text(
            "ทุกเส้นตรงบนวัตถุแกร่งชิ้นเดียวกัน หมุนด้วยความเร็วเชิงมุม ω เท่ากันทั้งหมด",
            font_size=11, color=WHITE
        ).move_to([0.0, 0.45, 0.0])
        fit_width(t_r1, 10.8)
        s_r1 = Text(
            "(Every line on a rigid body rotates with the exact same angular velocity ω)",
            font_size=9.5, color=COL_GRAY
        ).move_to([0.0, 0.18, 0.0])
        fit_width(s_r1, 10.8)

        b_r2 = _ic02_badge("กฎข้อที่ 2: ระยะห่างคงที่ (Rigidity)", COL_WARN).move_to([-3.4, -0.25, 0.0])
        t_r2 = Text(
            "ระยะห่างระหว่าง 2 จุดใดๆ บนวัตถุแกร่ง มีค่าคงที่เสมอ ไม่มีการยืดหดหรือเปลี่ยนรูป",
            font_size=11, color=WHITE
        ).move_to([0.0, -0.65, 0.0])
        fit_width(t_r2, 10.8)
        s_r2 = Text(
            "(Distance is fixed → ความเร็วสัมพัทธ์มีเฉพาะแนวตั้งฉาก: v_(B/A) = ω · r_(B/A) เสมอ)",
            font_size=9.5, color=COL_WARN
        ).move_to([0.0, -0.92, 0.0])
        fit_width(s_r2, 10.8)

        rule_card = VGroup(rule_box, rule_head, b_r1, t_r1, s_r1, b_r2, t_r2, s_r2)

        self.play(FadeIn(rule_card, shift=UP * 0.4), run_time=0.7)
        self.wait(2.5)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ======================================================================
        # BEAT 40.2–44.0: The Aha Moment (The First IC Discovered!)
        # ======================================================================
        # Recreate rolling disk on left (focused on point A)
        aha_d_x, aha_d_y = -3.5, -0.2
        aha_R = 1.5
        aha_G = np.array([aha_d_x, aha_d_y, 0.0])
        aha_A = np.array([aha_d_x, aha_d_y - aha_R, 0.0])
        aha_P = aha_G + np.array([aha_R * np.cos(np.radians(135)), aha_R * np.sin(np.radians(135)), 0])

        disk2_fill = Circle(radius=aha_R, stroke_width=0, fill_color="#0F172A").set_fill("#0F172A", 0.6).move_to(aha_G)
        disk2_circle = Circle(radius=aha_R, color=COL_METAL, stroke_width=2.8).move_to(aha_G)
        g_line2 = Line(start=[-5.6, aha_d_y - aha_R, 0], end=[-1.4, aha_d_y - aha_R, 0], color=COL_GRAY, stroke_width=2.5)

        # Prominent Point A with glow ring
        dot_A_aha = Dot(aha_A, radius=0.12, color=COL_OK)
        ring_A = Circle(radius=0.28, color=COL_OK, stroke_width=2.5).move_to(aha_A)
        lbl_A_aha = Text("จุด A (v_A = 0)", font_size=10.5, color=COL_OK, weight=BOLD).next_to(aha_A, DOWN, buff=0.42)

        # Center G and Point P
        dot_G2 = Dot(aha_G, radius=0.08, color=WHITE)
        lbl_G2 = Text("G", font_size=10, color=WHITE).next_to(dot_G2, DOWN + LEFT, buff=0.06)

        dot_P2 = Dot(aha_P, radius=0.08, color=WHITE)
        lbl_P2 = Text("P", font_size=10, color=WHITE).next_to(dot_P2, UP + LEFT, buff=0.06)

        # Line from G to P and line from A to P
        line_GP = DashedLine(start=aha_G, end=aha_P, color=COL_GRAY, stroke_width=1.5)
        line_AP = Line(start=aha_A, end=aha_P, color=COL_OK, stroke_width=2.5)
        lbl_AP = Text("r_(P/A) = 0.924 m", font_size=9, color=COL_OK).move_to((aha_A + aha_P) / 2 + np.array([-0.65, 0.05, 0]))

        # Arrow v_P at point P
        vP_aha_arrow = Arrow(start=aha_P, end=aha_P + 1.5 * np.array([0.947, 0.320, 0]), buff=0, color=COL_FIELD, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        lbl_vP_aha = Text("v_P = 18.5 m/s", font_size=10, color=COL_FIELD, weight=BOLD).next_to(vP_aha_arrow.get_end(), UP + RIGHT, buff=0.08)

        disk_aha_grp = VGroup(
            disk2_fill, disk2_circle, g_line2, dot_A_aha, ring_A, lbl_A_aha,
            dot_G2, lbl_G2, dot_P2, lbl_P2, line_GP, line_AP, lbl_AP,
            vP_aha_arrow, lbl_vP_aha
        )

        # Right side: Aha Moment Explanation Card
        c4_x, c4_y = 2.9, -0.2
        aha_card_box = RoundedRectangle(
            width=6.4, height=4.1, corner_radius=0.15,
            color=COL_OK, stroke_width=2.5, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([c4_x, c4_y, 0])
        aha_card_head = _ic02_badge("Aha Moment: การค้นพบจุดหมุนชั่วขณะ", COL_OK).move_to([c4_x, c4_y + 1.65, 0])

        aha_t1 = Text("1. จุด P หมุนรอบศูนย์กลาง G ด้วยความเร็วเชิงมุม ω", font_size=10.5, color=WHITE).move_to([c4_x, c4_y + 1.15, 0])
        fit_width(aha_t1, 5.9)
        aha_t2 = Text("2. จุด P ก็หมุนรอบจุดสัมผัส A ด้วย ω เดียวกันพอดี!", font_size=10.5, color=YELLOW, weight=BOLD).move_to([c4_x, c4_y + 0.75, 0])
        fit_width(aha_t2, 5.9)
        aha_t3 = Text("• เพราะจุดสัมผัสพื้น A หยุดนิ่งชั่วขณะ (v_A = 0)", font_size=10, color=COL_OK).move_to([c4_x, c4_y + 0.35, 0])
        fit_width(aha_t3, 5.9)

        # Highlight calculation from A:
        # Distance AP = r * sqrt(2 + sqrt(2)) = 0.5 * 1.84776 = 0.92388 m
        # v_P = omega * r_(P/A) = 20 * 0.92388 = 18.478 m/s = 18.5 m/s!
        aha_calc_box = RoundedRectangle(
            width=5.8, height=1.1, corner_radius=0.10,
            color=COL_FIELD, stroke_width=1.8, fill_color="#0F172A"
        ).set_fill("#0F172A", 0.9).move_to([c4_x, c4_y - 0.45, 0])
        aha_c1 = Text("คำนวณโดยตรงจากจุด A (จุดหมุนเสมือน):", font_size=9.5, color=COL_GRAY).move_to([c4_x, c4_y - 0.20, 0])
        aha_c2 = Text("v_P = ω · r_(P/A) = (20)(0.924) = 18.5 m/s", font_size=11.5, color=YELLOW, weight=BOLD).move_to([c4_x, c4_y - 0.50, 0])
        aha_c3 = Text("⭐ ได้ผลลัพธ์ 18.5 m/s ตรงกับวิธีเวกเตอร์โดยไม่ต้องตั้งสมการยาว!", font_size=9.0, color=COL_OK).move_to([c4_x, c4_y - 0.78, 0])
        fit_width(aha_c3, 5.6)
        aha_calc_grp = VGroup(aha_calc_box, aha_c1, aha_c2, aha_c3)

        aha_note = Text("นี่คือจุดแรกของ Instant Center (IC) ที่เราพบในวิชานี้!", font_size=10, color=WHITE, weight=BOLD).move_to([c4_x, c4_y - 1.40, 0])
        fit_width(aha_note, 5.8)

        aha_card_grp = VGroup(aha_card_box, aha_card_head, aha_t1, aha_t2, aha_t3, aha_calc_grp, aha_note)

        self.play(FadeIn(disk_aha_grp), FadeIn(aha_card_grp), run_time=1.0)
        self.play(Indicate(dot_A_aha, color=YELLOW, scale_factor=1.6), Indicate(ring_A, color=YELLOW), run_time=0.8)
        self.wait(2.0)

        self.fade_out_all(run_time=0.5)
        self.wait(0.1)

        # ======================================================================
        # BEAT 44.0–47.5: Review Question Card
        # ======================================================================
        q_box = RoundedRectangle(
            width=11.4, height=3.3, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=13.5, color=COL_WARN, weight=BOLD).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "จุด A บนล้อที่ 'หยุดนิ่งชั่วขณะ' (v = 0) และทำหน้าที่เป็นจุดหมุนของทุกจุดบนล้อนี้\nมีชื่อเรียกพิเศษทางกลศาสตร์ว่าอะไร?",
            font_size=12.0, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text(
            "(คลิปถัดไป IC03: เราจะนิยามจุดหมุนชั่วขณะนี้อย่างเป็นทางการในฐานะ Instant Center!\nพร้อมเรียนรู้กฎการหา IC เพื่อวิเคราะห์ความเร็วของกลไกทุกรูปแบบได้อย่างรวดเร็ว)",
            font_size=11.0, color=COL_GRAY
        ).move_to([0.0, -0.55, 0.0])
        fit_width(q_ans, 10.6)
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(2.2)

        self.fade_out_all(run_time=0.6)
        self.wait(0.5)



def _ic03_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic03_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic03_caption_top(text, color=WHITE):
    return Text(text, font_size=13.5, color=color).move_to([0.0, 2.45, 0.0])


def _ic03_badge(text, color):
    lbl = Text(text, font_size=9.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.36, height=0.30, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _ic03_banner(text, color=COL_OK):
    bg = RoundedRectangle(
        width=11.8, height=0.52, corner_radius=0.1,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.90, 0.0])
    lbl = Text(text, font_size=11.5, color=color).move_to(bg.get_center())
    fit_width(lbl, 11.4)
    return VGroup(bg, lbl)


def _ic03_step_badge(text, color):
    lbl = Text(text, font_size=10.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.40, height=0.36, corner_radius=0.08,
        color=color, stroke_width=2.0, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC03_DefinitionOfIC(SafeScene):
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
        # BEAT 0.0–1.8: Title & Page Reference
        # ======================================================================
        self.title_m = _ic03_title("นิยาม Instant Center (IC)")
        self.ref_m = _ic03_page_ref("W03 น.7")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.4)

        # ======================================================================
        # BEAT 1.8–4.8: Hook Question Card
        # ======================================================================
        hook_box = RoundedRectangle(
            width=10.4, height=2.3, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        hook_badge = _ic03_badge("คำถามชวนคิดก่อนเริ่ม (Misconception)", COL_WARN).move_to([0.0, 0.70, 0.0])
        hook_text = Text(
            "จุด 'ศูนย์กลางชั่วขณะของความเร็ว' (IC) นี้ อยู่ตำแหน่งเดิมตลอดไปไหม?",
            font_size=13.5, color=WHITE, weight=BOLD
        ).move_to([0.0, 0.12, 0.0])
        fit_width(hook_text, 9.8)
        hook_sub = Text(
            "(หลายคนคิดว่า IC เป็นจุดตรึงถาวรบนกลไกเหมือนจุดหมุนของบานพับ — จริงหรือไม่?)",
            font_size=10.5, color=COL_GRAY
        ).move_to([0.0, -0.42, 0.0])
        fit_width(hook_sub, 9.8)
        hook_card = VGroup(hook_box, hook_badge, hook_text, hook_sub)

        self.play(FadeIn(hook_card, shift=UP * 0.3), run_time=0.6)
        self.wait(1.8)
        self.play(FadeOut(hook_card), run_time=0.4)
        self.wait(0.2)

        # ======================================================================
        # BEAT 4.8–10.6: Definition & Geometric Reason (Connecting with IC02)
        # ======================================================================
        cap1 = _ic03_caption_top("นิยาม: ทุกขณะที่วัตถุแกร่งเคลื่อนที่บนระนาบ จะมีจุดหนึ่งที่ความเร็วเป็นศูนย์ชั่วขณะ (v = 0)")
        fit_width(cap1, 11.8)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Schematic connecting with IC02:
        # If C is IC, then v_X = omega x r_(X/C) is perpendicular to r_(X/C)
        pt_C_schem = np.array([-3.2, -0.4, 0.0])
        pt_X_schem = np.array([0.2, 0.5, 0.0])
        r_CX = pt_X_schem - pt_C_schem
        L_CX = np.linalg.norm(r_CX)
        u_CX = r_CX / L_CX
        n_CX = np.array([-u_CX[1], u_CX[0], 0.0])  # Perpendicular CCW (+90 deg)

        dot_C_schem = Dot(pt_C_schem, radius=0.10, color=COL_OK)
        lbl_C_schem = Text("C (IC: v_C = 0)", font_size=10.5, color=COL_OK, weight=BOLD).next_to(dot_C_schem, DOWN, buff=0.12)
        dot_X_schem = Dot(pt_X_schem, radius=0.08, color=WHITE)
        lbl_X_schem = Text("X (จุดใดๆ บนวัตถุ)", font_size=10.5, color=WHITE).next_to(dot_X_schem, UP + RIGHT, buff=0.10)

        r_line = Arrow(start=pt_C_schem, end=pt_X_schem, buff=0, color=COL_GRAY, stroke_width=3.0, max_tip_length_to_length_ratio=0.20)
        lbl_r = Text("r_(X/C)", font_size=10, color=COL_GRAY).next_to(r_line.get_center(), UP + LEFT, buff=0.08)

        vX_vec = 1.6 * n_CX
        vX_arrow = Arrow(start=pt_X_schem, end=pt_X_schem + vX_vec, buff=0, color=COL_FORCE, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_vX = Text("v_X = ω × r_(X/C) (⊥ r)", font_size=10, color=COL_FORCE, weight=BOLD).next_to(vX_arrow.get_end(), UP + LEFT, buff=0.08)

        # Right angle mark at X between r_line and vX_arrow
        sq_schem = Square(side_length=0.22, stroke_width=1.8, color=WHITE)
        sq_schem.rotate(np.arctan2(u_CX[1], u_CX[0]))
        sq_schem.move_to(pt_X_schem + 0.11 * u_CX + 0.11 * n_CX)

        schem_left = VGroup(dot_C_schem, lbl_C_schem, dot_X_schem, lbl_X_schem, r_line, lbl_r, vX_arrow, lbl_vX, sq_schem)

        # Right side: explanation card
        card_why_box = RoundedRectangle(
            width=5.4, height=3.0, corner_radius=0.12,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([3.4, -0.4, 0.0])
        card_why_head = _ic03_badge("เหตุผลเชิงเรขาคณิต (จาก IC02)", COL_FIELD).move_to([3.4, 0.80, 0.0])
        why_t1 = Text("• ความเร็วของทุกจุดเกิดจากการหมุนรอบ IC (C):", font_size=9.5, color=WHITE).move_to([3.4, 0.35, 0.0])
        fit_width(why_t1, 5.0)
        why_t2 = Text("  v = ω × r  →  ทิศทางตั้งฉากกับ r เสมอ", font_size=10.5, color=YELLOW, weight=BOLD).move_to([3.4, -0.05, 0.0])
        fit_width(why_t2, 5.0)
        why_t3 = Text("• สรุปกลับได้ว่า: จุด C (IC) ย่อมต้องอยู่บนแนวเส้น", font_size=9.5, color=WHITE).move_to([3.4, -0.50, 0.0])
        fit_width(why_t3, 5.0)
        why_t4 = Text("  'ที่ตั้งฉากกับเวกเตอร์ความเร็ว' เสมอ!", font_size=10.5, color=COL_OK, weight=BOLD).move_to([3.4, -0.85, 0.0])
        fit_width(why_t4, 5.0)
        card_why_grp = VGroup(card_why_box, card_why_head, why_t1, why_t2, why_t3, why_t4)

        banner1 = _ic03_banner("ถ้า v ตั้งฉากกับ r เสมอ → จุด IC ย่อมต้องอยู่บนเส้นตั้งฉากกับเวกเตอร์ความเร็ว!", COL_OK)

        self.play(FadeIn(schem_left), FadeIn(card_why_grp), FadeIn(banner1), run_time=1.0)
        self.wait(3.8)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 10.6–24.9: 3-Step Construction Procedure (page-07.jpg panel a)
        # ======================================================================
        cap2 = _ic03_caption_top("วิธีหาตำแหน่ง IC จากภาพ: ปฏิบัติตาม 3 ขั้นตอนหลัก")
        fit_width(cap2, 11.8)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Rigid Body Blob (smooth potato shape matching page-07.jpg)
        blob_center = np.array([-0.3, -0.55, 0.0])
        angles = np.linspace(0, 2 * np.pi, 24, endpoint=False)
        radii = 1.7 + 0.5 * np.cos(angles) - 0.3 * np.sin(2 * angles) + 0.2 * np.cos(3 * angles)
        blob_pts = [blob_center + np.array([r * np.cos(a), 0.72 * r * np.sin(a), 0.0]) for a, r in zip(angles, radii)]
        body_blob = Polygon(*blob_pts, color="#B08968", stroke_width=3.0, fill_color="#8D6E63").set_fill("#8D6E63", 0.45)

        # Instant Center C in panel (a)
        pt_C = np.array([0.3, 1.4, 0.0])

        # Point A and velocity v_A
        pt_A = np.array([-2.0, -0.8, 0.0])
        r_A = pt_A - pt_C
        vA_dir = np.array([0.6912, -0.7226, 0.0])  # Perpendicular to CA pointing down-right
        dot_A = Dot(pt_A, radius=0.08, color="#2E7D32")
        lbl_A = Text("A", font_size=11, color=WHITE, weight=BOLD).next_to(dot_A, LEFT, buff=0.10)
        vA_arrow = Arrow(start=pt_A, end=pt_A + 1.5 * vA_dir, buff=0, color=COL_FORCE, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_vA = Text("v_A", font_size=11, color=COL_FORCE, weight=BOLD).next_to(vA_arrow.get_end(), DOWN, buff=0.08)

        # Point B and velocity v_B
        pt_B = np.array([0.8, -0.3, 0.0])
        r_B = pt_B - pt_C
        vB_dir = np.array([0.9594, 0.2822, 0.0])   # Perpendicular to CB pointing right/up
        dot_B = Dot(pt_B, radius=0.08, color="#2E7D32")
        lbl_B = Text("B", font_size=11, color=WHITE, weight=BOLD).next_to(dot_B, DOWN + LEFT, buff=0.08)
        vB_arrow = Arrow(start=pt_B, end=pt_B + 1.4 * vB_dir, buff=0, color=COL_FORCE, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_vB = Text("v_B", font_size=11, color=COL_FORCE, weight=BOLD).next_to(vB_arrow.get_end(), RIGHT, buff=0.08)

        lbl_panel_a = Text("(a)", font_size=11, color=COL_GRAY).next_to(body_blob, DOWN, buff=0.20)

        banner2 = _ic03_banner("เมื่อรู้ทิศทางความเร็ว 2 จุดที่ไม่ขนานกัน (v_A และ v_B) สามารถหาจุด IC ได้ทันที", COL_OK)

        self.play(
            Create(body_blob), FadeIn(dot_A), FadeIn(lbl_A), FadeIn(dot_B), FadeIn(lbl_B),
            GrowArrow(vA_arrow), FadeIn(lbl_vA), GrowArrow(vB_arrow), FadeIn(lbl_vB),
            FadeIn(lbl_panel_a), FadeIn(banner2),
            run_time=1.2
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # STEP 1 (§48): Perpendicular line at Point A
        # ----------------------------------------------------------------------
        step_pos = np.array([-3.2, 1.95, 0.0])
        step1_badge = _ic03_step_badge("ขั้นที่ 1: ลากเส้นตั้งฉากกับ v_A ที่จุด A", COL_WARN).move_to(step_pos)

        # Red dashed line extending through C
        perp_dir_A = (pt_C - pt_A) / np.linalg.norm(pt_C - pt_A)
        perp_A = DashedLine(start=pt_A, end=pt_C + 0.10 * perp_dir_A, color=COL_BAD, stroke_width=2.5, dash_length=0.12)

        # Right angle mark at A
        sq_A = Square(side_length=0.20, stroke_width=1.8, color=WHITE)
        sq_A.rotate(np.arctan2(perp_dir_A[1], perp_dir_A[0]))
        sq_A.move_to(pt_A + 0.10 * perp_dir_A + 0.10 * vA_dir)

        self.play(FadeIn(step1_badge, shift=UP * 0.2), run_time=0.4)
        self.play(Create(perp_A), FadeIn(sq_A), run_time=1.0)
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # STEP 2 (§48): Perpendicular line at Point B
        # ----------------------------------------------------------------------
        step2_badge = _ic03_step_badge("ขั้นที่ 2: ลากเส้นตั้งฉากกับ v_B ที่จุด B", COL_WARN).move_to(step_pos)

        perp_dir_B = (pt_C - pt_B) / np.linalg.norm(pt_C - pt_B)
        perp_B = DashedLine(start=pt_B, end=pt_C + 0.10 * perp_dir_B, color=COL_BAD, stroke_width=2.5, dash_length=0.12)

        # Right angle mark at B
        sq_B = Square(side_length=0.20, stroke_width=1.8, color=WHITE)
        sq_B.rotate(np.arctan2(perp_dir_B[1], perp_dir_B[0]))
        sq_B.move_to(pt_B + 0.10 * perp_dir_B + 0.10 * vB_dir)

        self.play(ReplacementTransform(step1_badge, step2_badge), run_time=0.4)
        self.play(Create(perp_B), FadeIn(sq_B), run_time=1.0)
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # STEP 3 (§48): Mark intersection Point C = IC
        # ----------------------------------------------------------------------
        step3_badge = _ic03_step_badge("ขั้นที่ 3: จุดตัดของเส้นทั้งสอง = Instant Center (IC)", COL_OK).move_to(step_pos)

        dot_C = Dot(pt_C, radius=0.11, color=COL_OK)
        ring_C = Circle(radius=0.25, color=COL_OK, stroke_width=2.0).move_to(pt_C)
        lbl_C = Text("C (Instant Center: v = 0)", font_size=10.5, color=COL_OK, weight=BOLD).next_to(ring_C, UP, buff=0.12)

        self.play(ReplacementTransform(step2_badge, step3_badge), run_time=0.4)
        self.play(FadeIn(dot_C), FadeIn(ring_C), FadeIn(lbl_C), run_time=0.6)
        self.play(Indicate(dot_C, color=YELLOW, scale_factor=1.6), Indicate(ring_C, color=YELLOW), run_time=0.8)
        self.wait(1.8)

        self.clear_stage(run_time=0.6)
        self.wait(0.1)

        # ======================================================================
        # BEAT 24.9–32.1: Panel (b) — IC Moves as Body Moves!
        # ======================================================================
        cap3 = _ic03_caption_top("แต่เมื่อวัตถุเคลื่อนที่ต่อไปอีกนิด... (ทำ 3 ขั้นตอนเดิมซ้ำ)")
        fit_width(cap3, 11.8)
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        # Ghost / Dim of old IC (C1)
        dot_C1_ghost = Dot(pt_C, radius=0.08, color=COL_GRAY)
        ring_C1_ghost = Circle(radius=0.20, color=COL_GRAY, stroke_width=1.5, stroke_opacity=0.6).move_to(pt_C)
        lbl_C1_ghost = Text("C (ขณะแรก)", font_size=9.5, color=COL_GRAY).next_to(ring_C1_ghost, UP + LEFT, buff=0.10)
        ghost_grp = VGroup(dot_C1_ghost, ring_C1_ghost, lbl_C1_ghost)

        # Panel (b) transformed body
        blob_center2 = np.array([0.2, -0.65, 0.0])
        angles2 = angles - np.radians(12)  # Rotated clockwise
        blob_pts2 = [blob_center2 + np.array([r * np.cos(a), 0.72 * r * np.sin(a), 0.0]) for a, r in zip(angles2, radii)]
        body_blob2 = Polygon(*blob_pts2, color="#B08968", stroke_width=3.0, fill_color="#8D6E63").set_fill("#8D6E63", 0.45)

        # New points in panel (b)
        pt_C2 = np.array([1.6, 1.3, 0.0])
        pt_A2 = np.array([-1.5, -1.0, 0.0])
        vA2_dir = np.array([0.5959, -0.8031, 0.0])
        dot_A2 = Dot(pt_A2, radius=0.08, color="#2E7D32")
        lbl_A2 = Text("A", font_size=11, color=WHITE, weight=BOLD).next_to(dot_A2, LEFT, buff=0.10)
        vA2_arrow = Arrow(start=pt_A2, end=pt_A2 + 1.4 * vA2_dir, buff=0, color=COL_FORCE, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_vA2 = Text("v_A", font_size=11, color=COL_FORCE, weight=BOLD).next_to(vA2_arrow.get_end(), DOWN, buff=0.08)

        pt_B2 = np.array([1.3, -0.5, 0.0])
        vB2_dir = np.array([0.9864, -0.1644, 0.0])
        dot_B2 = Dot(pt_B2, radius=0.08, color="#2E7D32")
        lbl_B2 = Text("B", font_size=11, color=WHITE, weight=BOLD).next_to(dot_B2, DOWN + LEFT, buff=0.08)
        vB2_arrow = Arrow(start=pt_B2, end=pt_B2 + 1.4 * vB2_dir, buff=0, color=COL_FORCE, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_vB2 = Text("v_B", font_size=11, color=COL_FORCE, weight=BOLD).next_to(vB2_arrow.get_end(), RIGHT, buff=0.08)

        lbl_panel_b = Text("(b)", font_size=11, color=COL_GRAY).next_to(body_blob2, DOWN, buff=0.20)

        # New perpendicular lines
        perp_dir_A2 = (pt_C2 - pt_A2) / np.linalg.norm(pt_C2 - pt_A2)
        perp_A2 = DashedLine(start=pt_A2, end=pt_C2 + 0.10 * perp_dir_A2, color=COL_BAD, stroke_width=2.5, dash_length=0.12)
        sq_A2 = Square(side_length=0.20, stroke_width=1.8, color=WHITE)
        sq_A2.rotate(np.arctan2(perp_dir_A2[1], perp_dir_A2[0]))
        sq_A2.move_to(pt_A2 + 0.10 * perp_dir_A2 + 0.10 * vA2_dir)

        perp_dir_B2 = (pt_C2 - pt_B2) / np.linalg.norm(pt_C2 - pt_B2)
        perp_B2 = DashedLine(start=pt_B2, end=pt_C2 + 0.10 * perp_dir_B2, color=COL_BAD, stroke_width=2.5, dash_length=0.12)
        sq_B2 = Square(side_length=0.20, stroke_width=1.8, color=WHITE)
        sq_B2.rotate(np.arctan2(perp_dir_B2[1], perp_dir_B2[0]))
        sq_B2.move_to(pt_B2 + 0.10 * perp_dir_B2 + 0.10 * vB2_dir)

        # New IC point C2
        dot_C2 = Dot(pt_C2, radius=0.11, color=COL_WARN)
        ring_C2 = Circle(radius=0.25, color=COL_WARN, stroke_width=2.0).move_to(pt_C2)
        lbl_C2 = Text("C' (IC ขณะใหม่)", font_size=10.5, color=COL_WARN, weight=BOLD).next_to(ring_C2, UP + RIGHT, buff=0.10)

        # Curved arrow showing movement from C1 to C2
        move_arr = CurvedArrow(start_point=pt_C + np.array([0.25, 0.1, 0]), end_point=pt_C2 + np.array([-0.25, 0.1, 0]), color=YELLOW)
        lbl_move = Text("ตำแหน่ง IC เปลี่ยนไป!", font_size=10, color=YELLOW, weight=BOLD).next_to(move_arr, UP, buff=0.10)

        panel_b_grp = VGroup(
            body_blob2, dot_A2, lbl_A2, dot_B2, lbl_B2,
            vA2_arrow, lbl_vA2, vB2_arrow, lbl_vB2, lbl_panel_b,
            perp_A2, sq_A2, perp_B2, sq_B2,
            dot_C2, ring_C2, lbl_C2, move_arr, lbl_move
        )

        banner3 = _ic03_banner("ตำแหน่งของ IC เปลี่ยนไปตามเวลาเรื่อยๆ จึงเรียกว่า 'Instant' (ชั่วขณะ) ไม่ใช่จุดคงที่", COL_WARN)

        self.play(FadeIn(ghost_grp), FadeIn(panel_b_grp), FadeIn(banner3), run_time=1.2)
        self.play(Indicate(dot_C2, color=YELLOW, scale_factor=1.6), Indicate(ring_C2, color=YELLOW), run_time=0.8)
        self.wait(3.5)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ======================================================================
        # BEAT 32.1–35.8: History Card (Johann Bernoulli, 1742)
        # ======================================================================
        cap4 = _ic03_caption_top("เพราะตำแหน่งเปลี่ยนได้ทุกขณะ จึงเรียกว่า Instant Center — ไม่ใช่จุดคงที่")
        self.play(FadeIn(cap4, shift=UP * 0.35), run_time=0.5)

        hist_box = RoundedRectangle(
            width=10.4, height=2.4, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.20, 0.0])
        hist_badge = _ic03_badge("ประวัติความเป็นมา (History)", COL_OK).move_to([0.0, 0.65, 0.0])
        hist_title = Text(
            "แนวคิด 'จุดศูนย์กลางชั่วขณะของความเร็ว' ค้นพบโดย Johann Bernoulli ในปี ค.ศ. 1742",
            font_size=12, color=WHITE, weight=BOLD
        ).move_to([0.0, 0.08, 0.0])
        fit_width(hist_title, 9.8)
        hist_sub = Text(
            "(Johann Bernoulli: นักคณิตศาสตร์ชาวสวิส ผู้บุกเบิกกลศาสตร์ระนาบและแคลคูลัส)",
            font_size=10.5, color=COL_GRAY
        ).move_to([0.0, -0.45, 0.0])
        fit_width(hist_sub, 9.8)
        hist_card = VGroup(hist_box, hist_badge, hist_title, hist_sub)

        self.play(FadeIn(hist_card, shift=UP * 0.3), run_time=0.6)
        self.wait(2.2)

        self.fade_out_all(run_time=0.5)
        self.wait(0.1)

        # ======================================================================
        # BEAT 35.8–38.0: Summary Card
        # ======================================================================
        sum_box = RoundedRectangle(
            width=11.4, height=3.3, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        sum_head = Text(
            "สรุป: นิยามและการหา Instant Center (IC)",
            font_size=13.5, color=COL_OK, weight=BOLD
        ).move_to([0.0, 1.10, 0.0])

        s_rows = [
            "1. นิยาม: จุดที่มีความเร็วสัมบูรณ์เป็นศูนย์ชั่วขณะ (v = 0) ในขณะใดขณะหนึ่งบนระนาบ",
            "2. การหา 3 ขั้นตอน: ลากเส้น ⊥ v_A ที่จุด A, ลากเส้น ⊥ v_B ที่จุด B, จุดตัดของเส้นทั้งสองคือ IC",
            "3. ธรรมชาติของ IC: ตำแหน่งเปลี่ยนไปเรื่อยๆ ตามการเคลื่อนที่ (เป็น Instant ไม่ใช่จุดคงที่ถาวร)"
        ]
        sum_lines = VGroup(*[Text(r, font_size=11, color=WHITE) for r in s_rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.0, -0.20, 0.0])
        fit_width(sum_lines, 10.6)

        summary_card = VGroup(sum_box, sum_head, sum_lines)

        self.play(FadeIn(summary_card, shift=UP * 0.4), run_time=0.6)
        self.wait(1.5)

        self.fade_out_all(run_time=0.5)
        self.wait(0.1)

        # ======================================================================
        # BEAT 38.0–40.8: Review Question (Teaser for IC04)
        # ======================================================================
        q_box = RoundedRectangle(
            width=11.4, height=3.2, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=13.5, color=COL_WARN, weight=BOLD).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "ถ้ามีวัตถุ 2 ชิ้นเคลื่อนที่พร้อมกันในกลไก จะมี IC ร่วมระหว่างวัตถุทั้งสองได้ไหม?",
            font_size=12.0, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text(
            "(คลิปถัดไป IC04: เราจะเรียนรู้สัญลักษณ์ I₁₂ และนิยาม Relative Instant Center\nซึ่งเป็นหัวใจสำคัญในการวิเคราะห์ความเร็วของกลไกหลายชิ้นส่วน!)",
            font_size=11.0, color=COL_GRAY
        ).move_to([0.0, -0.55, 0.0])
        fit_width(q_ans, 10.6)
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(2.0)

        self.fade_out_all(run_time=0.6)
        self.wait(0.2)

# ======================================================================
# Helper functions for IC04_NotationI12
# ======================================================================

def _ic04_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic04_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic04_caption_top(text, color=WHITE):
    return Text(text, font_size=13.5, color=color).move_to([0.0, 2.45, 0.0])


def _ic04_badge(text, color):
    lbl = Text(text, font_size=9.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.36, height=0.30, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC04_NotationI12(SafeScene):
    """
    IC04: สัญกรณ์ IC สัมพัทธ์ระหว่าง 2 วัตถุ (I12)
    ความยาว ~20.3 วินาที -- thin richness, fully static camera
    W03 Instant Center series, clip 4/11
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic04_title("สัญกรณ์ IC สัมพัทธ์: I12")
        page_ref_m = _ic04_page_ref("W03 น.9")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.0: Hook Question
        # ==================================================================
        hook_q = _ic04_caption_top(
            "กลไกหนึ่งชุด มี IC แค่ตัวเดียวเท่านั้นใช่ไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.8)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)

        # ==================================================================
        # BEAT 4.0-4.6: Clear & Brief Pause
        # ==================================================================
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.2)

        # ==================================================================
        # BEAT 4.6-5.3: Caption 1 -- Answer
        # ==================================================================
        cap1 = _ic04_caption_top(
            "จริงๆ มี IC สัมพัทธ์ระหว่างวัตถุทุกคู่ในกลไก "
            "สัญกรณ์ I12 (หรือ I21 -- สลับเลขได้ ความหมายเดียวกัน)"
        )
        fit_width(cap1, 11.8)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)
        self.wait(0.2)

        # ==================================================================
        # BEAT 5.3-15.0: Revolute-joint diagram
        #   Link 1 (fixed ground): gray rectangle + hatching below
        #   Link 2 (moving): light-blue polygon body
        #   Pin A0 kept SEPARATE from link2_body so Rotate() does NOT spin the pin label
        # ==================================================================
        A0_pt = np.array([-1.0, -0.8, 0.0])

        # --- Link 1: fixed ground (gray rectangle + hatching) ---
        gnd_rect = Rectangle(
            width=2.2, height=0.45, color=COL_METAL,
            fill_color=COL_METAL, stroke_width=2.0
        ).set_fill(COL_METAL, 0.55).move_to(A0_pt + np.array([0.0, -0.35, 0.0]))

        hatch_y = A0_pt[1] - 0.58
        hatches = VGroup(*[
            Line(
                start=[x, hatch_y, 0],
                end=[x - 0.14, hatch_y - 0.18, 0],
                color="#64748B", stroke_width=1.4
            )
            for x in np.linspace(A0_pt[0] - 0.9, A0_pt[0] + 0.9, 9)
        ])
        lbl_link1 = Text("1 (Fixed)", font_size=9.5, color=COL_METAL).next_to(
            gnd_rect, LEFT, buff=0.18)
        link1_fixed = VGroup(gnd_rect, hatches, lbl_link1)

        # --- Link 2: moving body (COL_FIELD blue, irregular polygon matching ref image) ---
        body_verts_rel = np.array([
            [0.0,   0.0,  0.0],
            [0.55, -0.25, 0.0],
            [1.15, -0.10, 0.0],
            [1.35,  0.55, 0.0],
            [1.10,  1.35, 0.0],
            [0.45,  1.80, 0.0],
            [-0.25, 1.75, 0.0],
            [-0.55, 1.10, 0.0],
            [-0.35,  0.30, 0.0],
        ])
        body_verts = body_verts_rel + A0_pt

        link2_body = Polygon(
            *body_verts,
            color=COL_FIELD, stroke_width=2.5,
            fill_color=COL_FIELD
        ).set_fill(COL_FIELD, 0.20)

        lbl_link2 = Text("2 (เคลื่อนที่)", font_size=9.5, color=COL_FIELD).next_to(
            link2_body, RIGHT, buff=0.15)

        # --- Pin A0 at pivot (SEPARATE VGroup -- NOT inside link2_body) ---
        pin_dot = Dot(A0_pt, radius=0.11, color=COL_OK)
        pin_ring = Circle(radius=0.22, color=COL_OK, stroke_width=2.2).move_to(A0_pt)
        label_A0 = Text("A0", font_size=11, color=COL_OK, weight=BOLD).next_to(
            pin_dot, DOWN + LEFT, buff=0.14)
        pin_A0 = VGroup(pin_dot, pin_ring, label_A0)

        self.play(FadeIn(link1_fixed), run_time=0.5)
        self.play(FadeIn(pin_A0), run_time=0.3)
        self.play(FadeIn(link2_body), FadeIn(lbl_link2), run_time=0.5)
        self.wait(0.5)

        # Rotate link2 body + its label around pin A0 -- pin_A0 stays fixed
        self.play(
            Rotate(link2_body, angle=0.28, about_point=A0_pt),
            Rotate(lbl_link2, angle=0.28, about_point=A0_pt),
            run_time=1.5
        )
        self.wait(0.5)

        # Caption below diagram
        cap_diag = Text(
            "จุด A0 (หมุดยึด) มีความเร็วเป็นศูนย์เท่ากันทั้ง 2 ชิ้น เพราะชิ้น 1 หยุดนิ่ง -> I12 = A0",
            font_size=11.5, color=WHITE
        ).move_to([0.0, -2.65, 0.0])
        fit_width(cap_diag, 12.0)
        self.play(FadeIn(cap_diag), run_time=0.5)

        # Indicate pin, then TransformFromCopy label_A0 -> label_I12
        self.play(Indicate(pin_A0, color=COL_OK, scale_factor=1.5), run_time=0.7)

        label_I12 = Text("I12 = A0", font_size=13, color=COL_OK, weight=BOLD).next_to(
            pin_dot, UP + RIGHT, buff=0.22)
        self.play(TransformFromCopy(label_A0, label_I12), run_time=0.6)

        self.wait(4.5)

        # ==================================================================
        # BEAT 15.0-15.6: Fade out all
        # ==================================================================
        self.fade_out_all(run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # BEAT 15.6-17.0: Summary Card
        # ==================================================================
        sum_box = RoundedRectangle(
            width=11.4, height=2.8, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.20, 0.0])
        sum_head = _ic04_badge("สรุป: สัญกรณ์ I12 / I21", COL_OK).move_to([0.0, 0.80, 0.0])
        sum_text = Text(
            "I12 = I21 = จุดที่ความเร็วสัมพัทธ์ระหว่างวัตถุ 2 ชิ้นเป็นศูนย์\n"
            "(สลับเลขได้ ความหมายเดียวกัน)",
            font_size=12.5, color=WHITE
        ).move_to([0.0, -0.05, 0.0])
        fit_width(sum_text, 10.8)
        sum_sub = Text(
            "ตัวอย่าง: ชิ้น 1 หยุดนิ่ง, ชิ้น 2 หมุนรอบหมุด A0 -> I12 = A0",
            font_size=11, color=COL_GRAY
        ).move_to([0.0, -0.72, 0.0])
        fit_width(sum_sub, 10.8)
        summary_card = VGroup(sum_box, sum_head, sum_text, sum_sub)

        self.play(FadeIn(summary_card, shift=UP * 0.4), run_time=0.5)
        self.wait(0.9)

        # ==================================================================
        # BEAT 17.0-19.3: Review Question Card (bridge to IC05)
        # ==================================================================
        self.play(FadeOut(summary_card), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.4, height=3.2, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text(
            "คำถามทบทวนประจำคลิป (Check Your Understanding)",
            font_size=13.5, color=COL_WARN, weight=BOLD
        ).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "ถ้าวัตถุ 2 ชิ้นไม่ได้ต่อกันด้วยหมุดตรงๆ\n"
            "(เช่น เลื่อนกัน หรือเป็นเฟือง) จะหา I12 ยังไง?",
            font_size=12.0, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text(
            "(คลิปต่อไป IC05: จะเฉลยทีละกรณีตามชนิดข้อต่อ: revolute, prismatic, rolling contact และอื่นๆ)",
            font_size=10.5, color=COL_GRAY
        ).move_to([0.0, -0.70, 0.0])
        fit_width(q_ans, 10.6)
        question_card = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_card, shift=UP * 0.3), run_time=0.5)
        self.wait(1.8)

        # ==================================================================
        # BEAT 19.3-20.3: Hold & Fade
        # ==================================================================
        self.fade_out_all(run_time=0.5)
        self.wait(0.5)


# ======================================================================
# Helper functions for IC05_JointTypes
# ======================================================================

def _ic05_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic05_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic05_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.45, 0.0])


def _ic05_badge(text, color):
    lbl = Text(text, font_size=9.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.36, height=0.30, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _ic05_type_label(text, color=COL_OK):
    lbl = Text(text, font_size=13, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.5, height=0.44, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl).move_to([-4.2, 1.9, 0.0])


def _ic05_reason(text, color=WHITE):
    t = Text(text, font_size=12, color=color).move_to([0.0, -2.55, 0.0])
    fit_width(t, 11.6)
    return t


class IC05_JointTypes(SafeScene):
    """
    W03 น.10-12 — ตำแหน่ง IC ของข้อต่อ (joint) 5 แบบ
    Plan: Main_note/Claude_Specs/Manim — IC05_JointTypes Plan.md
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic05_title("IC ของข้อต่อ (Joint) 5 แบบ")
        page_ref_m = _ic05_page_ref("W03 น.10-12")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.8: Hook Question
        # ==================================================================
        hook_q = _ic05_caption_top(
            "วิธีลากเส้นตั้งฉากที่เรียนไป ใช้ได้เหมือนกันหมดทุกชนิดข้อต่อไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.8)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)
        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 4.8-5.5: Answer caption
        # ==================================================================
        cap1 = _ic05_caption_top(
            "จริงๆ ตำแหน่ง IC ขึ้นกับชนิดข้อต่อ — 4 ใน 5 แบบ หาได้ทันทีจากรูปทรง ไม่ต้องรู้ทิศทางความเร็วเลย"
        )
        fit_width(cap1, 11.8)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # ==================================================================
        # CASE 1/5: Revolute joint (หมุด) — n.12 top-left
        # ==================================================================
        type1 = _ic05_type_label("1. Revolute joint (ข้อต่อหมุด)", COL_OK)
        self.play(FadeIn(type1, shift=UP * 0.2), run_time=0.4)

        pin1 = np.array([0.0, -0.6, 0.0])
        ang_B1 = np.radians(200)
        ang_C1 = np.radians(-20)
        body_B1 = Line(pin1, pin1 + 2.1 * np.array([np.cos(ang_B1), np.sin(ang_B1), 0]), stroke_width=7, color=COL_METAL)
        body_C1 = Line(pin1, pin1 + 2.3 * np.array([np.cos(ang_C1), np.sin(ang_C1), 0]), stroke_width=7, color=COL_FIELD)
        lbl_B1 = Text("Body B", font_size=11, color=COL_METAL).next_to(body_B1.get_end(), DOWN + LEFT, buff=0.1)
        lbl_C1 = Text("Body C", font_size=11, color=COL_FIELD).next_to(body_C1.get_end(), RIGHT, buff=0.1)

        self.play(Create(body_B1), FadeIn(lbl_B1), run_time=0.6)
        self.play(Create(body_C1), FadeIn(lbl_C1), run_time=0.6)

        pin1_dot = Dot(pin1, radius=0.09, color=WHITE)
        pin1_cross = VGroup(
            Line(pin1 + [-0.09, 0, 0], pin1 + [0.09, 0, 0], color=COL_BG_BOX, stroke_width=1.5),
            Line(pin1 + [0, -0.09, 0], pin1 + [0, 0.09, 0], color=COL_BG_BOX, stroke_width=1.5),
        )
        self.play(FadeIn(pin1_dot), FadeIn(pin1_cross), run_time=0.5)
        self.wait(0.3)

        self.play(Indicate(pin1_dot, color=COL_OK), run_time=0.6)
        label_IC1 = Text("I_BC, I_CB", font_size=13, color=COL_OK, weight=BOLD).next_to(pin1_dot, UP, buff=0.25)
        self.play(FadeIn(label_IC1), run_time=0.5)
        self.wait(0.3)

        reason1 = _ic05_reason("จุดหมุดมีความเร็วเท่ากัน ไม่ว่าจะมองจากชิ้นไหน → IC อยู่ตรงจุดหมุดเลย", COL_OK)
        self.play(FadeIn(reason1, shift=UP * 0.3), run_time=0.5)
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m, cap1)], run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # CASE 2/5: Prismatic joint (สไลด์เดอร์ตรง)
        # ==================================================================
        type2 = _ic05_type_label("2. Prismatic joint (สไลด์เดอร์ตรง)", COL_OK)
        self.play(FadeIn(type2), run_time=0.4)

        rail_y = -1.1
        rail_C2 = Line([-3.4, rail_y, 0], [3.4, rail_y, 0], stroke_width=7, color=COL_FIELD)
        lbl_rail = Text("Body C (ราง)", font_size=10.5, color=COL_FIELD).next_to(rail_C2.get_start(), DOWN, buff=0.2)
        self.play(Create(rail_C2), FadeIn(lbl_rail), run_time=0.5)

        block_B2 = RoundedRectangle(width=1.1, height=0.5, corner_radius=0.06, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.6).move_to([-0.3, rail_y + 0.45, 0])
        lbl_block = Text("Body B", font_size=10.5, color=COL_METAL).next_to(block_B2, LEFT, buff=0.15)
        self.play(FadeIn(block_B2), FadeIn(lbl_block), run_time=0.5)

        slide_arrow = Arrow(block_B2.get_center() + [1.0, 0, 0], block_B2.get_center() + [2.0, 0, 0], buff=0, color=COL_WARN, stroke_width=3.5, max_tip_length_to_length_ratio=0.3)
        slide_lbl = Text("ไถลตรง", font_size=9.5, color=COL_WARN).next_to(slide_arrow, UP, buff=0.08)
        self.play(GrowArrow(slide_arrow), FadeIn(slide_lbl), run_time=0.5)
        self.wait(0.3)

        px = block_B2.get_center()[0]
        perp_up = Arrow([px, rail_y + 0.45, 0], [px, rail_y + 2.2, 0], buff=0.25, color=COL_OK, stroke_width=3.0, max_tip_length_to_length_ratio=0.12)
        perp_down = Arrow([px, rail_y + 0.45, 0], [px, rail_y - 1.55, 0], buff=0.25, color=COL_OK, stroke_width=3.0, max_tip_length_to_length_ratio=0.12)
        self.play(GrowArrow(perp_up), GrowArrow(perp_down), run_time=0.7)
        label_inf = Text("I_BC, I_CB at ∞", font_size=12.5, color=COL_OK, weight=BOLD).next_to(perp_up, UP, buff=0.12)
        self.play(FadeIn(label_inf), run_time=0.5)

        reason2 = _ic05_reason("เส้นตรง = รัศมีความโค้ง ∞ → ω = v/r = v/∞ = 0 จริง แต่ตำแหน่งศูนย์กลางอยู่ที่ ∞ ⊥ ทิศไถล", COL_OK)
        self.play(FadeIn(reason2, shift=UP * 0.3), run_time=0.5)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m, cap1)], run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # CASE 3/5: Rolling contact (กลิ้งไม่ลื่นไถล) — callback IC02
        # ==================================================================
        type3 = _ic05_type_label("3. Rolling contact (กลิ้งไม่ลื่นไถล)", COL_OK)
        self.play(FadeIn(type3), run_time=0.4)

        P3 = np.array([0.0, -0.6, 0.0])
        blob_B3 = Circle(radius=1.3, color=COL_METAL, stroke_width=3.0).move_to(P3 + [-1.3, 0, 0])
        blob_B3.set_fill(COL_METAL, 0.15)
        blob_C3 = Circle(radius=1.0, color=COL_FIELD, stroke_width=3.0).move_to(P3 + [1.0, 0, 0])
        blob_C3.set_fill(COL_FIELD, 0.15)
        lbl_B3 = Text("Body B", font_size=10.5, color=COL_METAL).move_to(P3 + [-1.3, -1.6, 0])
        lbl_C3 = Text("Body C", font_size=10.5, color=COL_FIELD).move_to(P3 + [1.0, -1.35, 0])

        self.play(Create(blob_B3), FadeIn(lbl_B3), run_time=0.6)
        self.play(Create(blob_C3), FadeIn(lbl_C3), run_time=0.6)
        self.wait(0.3)

        dot_P3 = Dot(P3, radius=0.09, color=COL_OK)
        self.play(FadeIn(dot_P3), run_time=0.4)
        self.play(Indicate(dot_P3, color=COL_OK), run_time=0.6)
        label_IC3 = Text("P = I_BC, I_CB", font_size=12.5, color=COL_OK, weight=BOLD).move_to(P3 + [0.0, 1.65, 0.0])
        self.play(FadeIn(label_IC3), run_time=0.5)

        recap3 = Text("(callback: เหมือนล้อกลิ้งใน IC02!)", font_size=10, color=COL_GRAY).move_to([4.4, -2.3, 0.0])
        self.play(FadeIn(recap3, scale=0.8), run_time=0.5)

        reason3 = _ic05_reason("จุดสัมผัสไม่ลื่นไถล = จุดที่ v เท่ากันทั้งสองฝั่ง → IC อยู่ที่จุดสัมผัสเลย", COL_OK)
        self.play(FadeIn(reason3, shift=UP * 0.3), run_time=0.5)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m, cap1)], run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # CASE 4/5: Cam-pair contact — ⚠️ EXCEPTION, uses COL_WARN
        # ==================================================================
        type4 = _ic05_type_label("4. Cam-pair contact — ⚠️ ข้อยกเว้น!", COL_WARN)
        self.play(FadeIn(type4), run_time=0.4)

        P4 = np.array([0.0, -0.5, 0.0])
        OB4 = P4 + np.array([-1.5, -0.3, 0.0])
        OC4 = P4 + np.array([1.6, -0.2, 0.0])
        cam_B4 = Ellipse(width=2.6, height=1.7, color=COL_METAL, stroke_width=3.0).set_fill(COL_METAL, 0.15).move_to(OB4).rotate(np.radians(15))
        cam_C4 = Ellipse(width=2.2, height=1.5, color=COL_FIELD, stroke_width=3.0).set_fill(COL_FIELD, 0.15).move_to(OC4).rotate(np.radians(-20))
        lbl_B4 = Text("Body B", font_size=10.5, color=COL_METAL).move_to(OB4 + [0, -1.15, 0])
        lbl_C4 = Text("Body C", font_size=10.5, color=COL_FIELD).move_to(OC4 + [0, -1.05, 0])

        self.play(Create(cam_B4), FadeIn(lbl_B4), run_time=0.6)
        self.play(Create(cam_C4), FadeIn(lbl_C4), run_time=0.6)

        dot_OB4 = Dot(OB4, radius=0.06, color=COL_METAL)
        dot_OC4 = Dot(OC4, radius=0.06, color=COL_FIELD)
        dot_P4 = Dot(P4, radius=0.08, color=WHITE)
        self.play(FadeIn(dot_OB4), FadeIn(dot_OC4), FadeIn(dot_P4), run_time=0.4)
        self.wait(0.2)

        perp_line4 = DashedLine(P4 + [0, 1.5, 0], P4 + [0, -1.5, 0], color=COL_WARN, stroke_width=2.5)
        self.play(Create(perp_line4), run_time=1.0)
        self.wait(0.5)
        label_IC4 = Text("I_BC, I_CB อยู่บนเส้นนี้ (ยังไม่รู้จุดแน่ๆ)", font_size=11.5, color=COL_WARN, weight=BOLD).move_to([1.9, 1.35, 0.0])
        fit_width(label_IC4, 3.2)
        self.play(FadeIn(label_IC4), run_time=0.5)

        reason4 = _ic05_reason("ต่างจาก 3 แบบแรก! รู้แค่ 'แนวเส้น' — ต้องรู้ทิศทางความเร็วเพิ่ม ถึงจะบอกตำแหน่งแน่นอนได้", COL_WARN)
        self.play(FadeIn(reason4, shift=UP * 0.3), run_time=0.5)
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m, cap1)], run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # CASE 5/5: Curved slider
        # ==================================================================
        type5 = _ic05_type_label("5. Curved slider", COL_OK)
        self.play(FadeIn(type5), run_time=0.4)

        center_curv = np.array([0.0, -2.1, 0.0])
        rho_len = 2.3
        curve_C5 = Arc(radius=rho_len, start_angle=np.radians(55), angle=np.radians(70), arc_center=center_curv, color=COL_FIELD, stroke_width=4.0)
        lbl_C5 = Text("Body C", font_size=10.5, color=COL_FIELD).move_to(center_curv + [1.9, 1.7, 0])
        self.play(Create(curve_C5), FadeIn(lbl_C5), run_time=0.6)

        ang_P5 = np.radians(90)
        P5 = center_curv + rho_len * np.array([np.cos(ang_P5), np.sin(ang_P5), 0])
        block_B5 = RoundedRectangle(width=0.7, height=0.35, corner_radius=0.05, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.7)
        block_B5.move_to(P5 + [0, 0.22, 0])
        lbl_B5 = Text("Body B", font_size=10, color=COL_METAL).next_to(block_B5, UP, buff=0.1)
        self.play(FadeIn(block_B5), FadeIn(lbl_B5), run_time=0.5)

        rho_arrow = Arrow(P5, center_curv, buff=0.08, color=COL_OK, stroke_width=2.8, max_tip_length_to_length_ratio=0.08)
        rho_lbl = Text("ρ", font_size=13, color=COL_OK).move_to((P5 + center_curv) / 2 + [0.3, 0, 0])
        self.play(GrowArrow(rho_arrow), FadeIn(rho_lbl), run_time=0.6)

        dot_center5 = Dot(center_curv, radius=0.09, color=COL_OK)
        self.play(FadeIn(dot_center5), run_time=0.4)
        label_IC5 = Text("I_BC, I_CB (จุดศูนย์กลางความโค้ง)", font_size=11.5, color=COL_OK, weight=BOLD).next_to(dot_center5, DOWN, buff=0.18)
        fit_width(label_IC5, 6.0)
        self.play(FadeIn(label_IC5), run_time=0.5)
        self.wait(2.9)

        self.fade_out_all(run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Summary Card (5 types comparison)
        # ==================================================================
        sum_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        sum_head = _ic05_badge("สรุป: ตำแหน่ง IC ของข้อต่อ 5 แบบ", COL_OK).move_to([0.0, 1.45, 0.0])
        rows = [
            "Revolute = ตรงจุดหมุด",
            "Prismatic = ∞ ⊥ ทิศไถล",
            "Rolling contact = จุดสัมผัส",
            "Curved slider = จุดศูนย์กลางความโค้ง",
        ]
        s_rows = VGroup(*[Text(r, font_size=12, color=WHITE) for r in rows]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0.0, 0.35, 0.0])
        fit_width(s_rows, 10.8)
        s_warn = Text("Cam-pair = บนเส้น ⊥ ผิวสัมผัส (ต้องรู้ทิศ v เพิ่ม) ⚠️", font_size=12, color=COL_WARN, weight=BOLD).move_to([0.0, -1.15, 0.0])
        fit_width(s_warn, 10.8)
        summary_card = VGroup(sum_box, sum_head, s_rows, s_warn)

        self.play(FadeIn(summary_card, shift=UP * 0.4), run_time=0.6)
        self.wait(1.3)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Review Question (bridge to IC06)
        # ==================================================================
        q_box = RoundedRectangle(
            width=11.4, height=2.6, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_body = Text(
            "ถ้ากลไกมีมากกว่า 2 ชิ้น จะหา IC ระหว่างชิ้นที่ไม่ได้ต่อกันโดยตรงได้ยังไง?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.25, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text(
            "(คลิปต่อไป: Kennedy's Theorem)",
            font_size=11, color=COL_GRAY
        ).move_to([0.0, -0.5, 0.0])
        question_card = VGroup(q_box, q_body, q_ans)

        self.play(FadeIn(question_card, shift=UP * 0.3), run_time=0.5)
        self.wait(2.0)

        self.fade_out_all(run_time=0.6)
        self.wait(1.0)


# ======================================================================
# Helper functions for IC06_KennedysTheorem
# ======================================================================

def _ic06_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic06_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic06_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.45, 0.0])


def _ic06_badge(text, color):
    lbl = Text(text, font_size=9.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.36, height=0.30, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _ic06_step_badge(text, color=COL_WARN):
    lbl = Text(text, font_size=12.5, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.4, height=0.40, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC06_KennedysTheorem(SafeScene):
    """
    W03 น.13 — Kennedy's Theorem + Circle Diagram technique
    Plan: Main_note/Claude_Specs/Manim — IC06_KennedysTheorem Plan.md
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic06_title("Kennedy's Theorem + Circle Diagram")
        page_ref_m = _ic06_page_ref("W03 น.13")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.8: Hook Question
        # ==================================================================
        hook_q = _ic06_caption_top(
            "ถ้าวัตถุ 2 ชิ้นไม่ได้ต่อกันโดยตรง จะหา IC ระหว่างมันไม่ได้เลยใช่ไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.8)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)

        # ==================================================================
        # BEAT 4.8-5.6: Answer caption
        # ==================================================================
        cap1 = _ic06_caption_top(
            "จริงๆ ใช้ทฤษฎีบทเคนเนดี้หาได้ — ไม่ต้องรู้ทิศทางความเร็วเลย"
        )
        fit_width(cap1, 11.8)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # ==================================================================
        # PART A: The theorem (5.6-20.0), step-by-step per §48
        # ==================================================================
        stepA_pos = np.array([3.6, 1.85, 0.0])

        # Step A1: Body 1 (frame) + Body 2, pinned at I12
        stepA1 = _ic06_step_badge("ขั้นที่ 1: วัตถุ 1 (เฟรม) + วัตถุ 2 ต่อกันที่หมุด", COL_OK).move_to(stepA_pos)
        self.play(FadeIn(stepA1, shift=UP * 0.2), run_time=0.4)

        I12_pt = np.array([-2.6, -1.1, 0.0])
        body1_line = Line(I12_pt + [-1.6, -0.9, 0], I12_pt + [1.6, -0.9, 0], color=COL_METAL, stroke_width=6)
        hatch1 = VGroup(*[
            Line([x, I12_pt[1] - 0.9, 0], [x - 0.14, I12_pt[1] - 1.08, 0], color="#64748B", stroke_width=1.3)
            for x in np.linspace(I12_pt[0] - 1.4, I12_pt[0] + 1.4, 9)
        ])
        lbl_1 = Text("1 (Frame)", font_size=9.5, color=COL_METAL).next_to(body1_line, DOWN, buff=0.15)
        body2_link = Line(I12_pt, I12_pt + [-0.4, 1.9, 0], color=COL_FIELD, stroke_width=6)
        lbl_2 = Text("2", font_size=11, color=COL_FIELD, weight=BOLD).next_to(body2_link.get_end(), UP, buff=0.1)

        self.play(Create(body1_line), FadeIn(hatch1), FadeIn(lbl_1), run_time=0.6)
        self.play(Create(body2_link), FadeIn(lbl_2), run_time=0.6)
        dot_I12 = Dot(I12_pt, radius=0.08, color=COL_OK)
        lbl_I12 = Text("I_12", font_size=11, color=COL_OK, weight=BOLD).next_to(dot_I12, DOWN + LEFT, buff=0.12)
        self.play(FadeIn(dot_I12), FadeIn(lbl_I12), run_time=0.4)
        self.wait(0.6)

        # Step A2: Body 2 + Body 3, pinned at I23
        stepA2 = _ic06_step_badge("ขั้นที่ 2: วัตถุ 2 + วัตถุ 3 ต่อกันที่หมุด", COL_OK).move_to(stepA_pos)
        self.play(ReplacementTransform(stepA1, stepA2), run_time=0.4)

        I23_pt = I12_pt + [-0.4, 1.9, 0]
        body3_link = Line(I23_pt, I23_pt + [2.3, 1.1, 0], color="#BA68C8", stroke_width=6)
        lbl_3 = Text("3", font_size=11, color="#BA68C8", weight=BOLD).next_to(body3_link.get_end(), UP, buff=0.1)
        self.play(Create(body3_link), FadeIn(lbl_3), run_time=0.6)
        dot_I23 = Dot(I23_pt, radius=0.08, color=COL_OK)
        lbl_I23 = Text("I_23", font_size=11, color=COL_OK, weight=BOLD).next_to(dot_I23, UP + LEFT, buff=0.12)
        self.play(FadeIn(dot_I23), FadeIn(lbl_I23), run_time=0.4)
        self.wait(0.6)

        # Step A3: extend the dashed line through I12-I23
        stepA3 = _ic06_step_badge("ขั้นที่ 3: ลากเส้นผ่าน I_12–I_23 ยาวออกไป", COL_OK).move_to(stepA_pos)
        self.play(ReplacementTransform(stepA2, stepA3), run_time=0.4)

        dir_v = (I23_pt - I12_pt) / np.linalg.norm(I23_pt - I12_pt)
        line_ext = DashedLine(I12_pt - 0.6 * dir_v, I23_pt + 1.3 * dir_v, color=COL_WARN, stroke_width=2.5)
        self.play(Create(line_ext), run_time=1.0)
        self.wait(0.5)

        # Step A4: I13 must lie on this line (unknown exact spot)
        stepA4 = _ic06_step_badge("ขั้นที่ 4: I_13 ต้องอยู่บนเส้นนี้เท่านั้น", COL_WARN).move_to(stepA_pos)
        self.play(ReplacementTransform(stepA3, stepA4), run_time=0.4)

        I13_guess = I23_pt + 1.1 * dir_v
        dot_I13 = Dot(I13_guess, radius=0.09, color=COL_WARN)
        ring_I13 = Circle(radius=0.22, color=COL_WARN, stroke_width=2.2).move_to(I13_guess)
        lbl_I13 = Text("I_13 (อยู่บนเส้นนี้แน่ๆ)", font_size=10.5, color=COL_WARN, weight=BOLD).next_to(dot_I13, DOWN + RIGHT, buff=0.15)
        self.play(FadeIn(dot_I13), FadeIn(ring_I13), FadeIn(lbl_I13), run_time=0.6)

        theorem_text = Text(
            "IC สัมพัทธ์ 3 จุดของวัตถุ 3 ชิ้นใดๆ อยู่ในแนวเส้นตรงเดียวกันเสมอ (Kennedy, ปลาย ค.ศ.19)",
            font_size=12, color=WHITE
        ).move_to([0.0, -2.6, 0.0])
        fit_width(theorem_text, 11.8)
        self.play(FadeIn(theorem_text, shift=UP * 0.2), run_time=0.5)
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m)], run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 20.6-22.0: Formula
        # ==================================================================
        formula_box = RoundedRectangle(
            width=6.0, height=1.6, corner_radius=0.12,
            color=COL_OK, stroke_width=2.4, fill_color="#0F766E"
        ).set_fill("#0F766E", 0.3).move_to([0.0, 0.3, 0.0])
        formula_tex = Text("N_IC = n(n-1) / 2", font_size=22, color=YELLOW, weight=BOLD).move_to([0.0, 0.55, 0.0])
        formula_ex = Text("ตัวอย่าง n=4 → N_IC = 4×3/2 = 6 จุด", font_size=13, color=WHITE).move_to([0.0, 0.05, 0.0])
        formula_grp = VGroup(formula_box, formula_tex, formula_ex)
        self.play(FadeIn(formula_grp, shift=UP * 0.3), run_time=0.5)
        self.wait(1.4)
        self.play(FadeOut(formula_grp), run_time=0.4)

        # ==================================================================
        # PART B: Circle Diagram technique (22.0-43.0), 4-body example, §48 stepwise
        # ==================================================================
        cap2 = _ic06_caption_top("เทคนิค Circle Diagram: หา IC ทั้งหมดของกลไก 4 ชิ้นอย่างเป็นระบบ")
        fit_width(cap2, 11.8)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        stepB_pos = np.array([-4.6, 1.85, 0.0])
        cx, cy, r = 0.0, -0.6, 2.0
        node_ang = {1: 135, 2: 45, 3: -45, 4: -135}
        node_pos = {k: np.array([cx + r * np.cos(np.radians(a)), cy + r * np.sin(np.radians(a)), 0]) for k, a in node_ang.items()}

        # Step B1: draw circle + 4 labeled points
        stepB1 = _ic06_step_badge("ขั้นที่ 1: วาดวงกลม แบ่ง 4 จุด (จุด 1 = เฟรม)", COL_OK).move_to(stepB_pos)
        self.play(FadeIn(stepB1, shift=UP * 0.2), run_time=0.4)
        circle_b = Circle(radius=r, color=COL_GRAY, stroke_width=2.0).move_to([cx, cy, 0])
        node_dots = VGroup(*[Dot(node_pos[k], radius=0.09, color=WHITE) for k in [1, 2, 3, 4]])
        node_lbls = VGroup(*[
            Text(str(k), font_size=13, color=WHITE, weight=BOLD).next_to(node_pos[k], node_pos[k] - [cx, cy, 0], buff=0.18)
            for k in [1, 2, 3, 4]
        ])
        self.play(Create(circle_b), FadeIn(node_dots), FadeIn(node_lbls), run_time=0.8)
        self.wait(0.4)

        # Step B2: solid edges from real joints (square: 12,23,34,14)
        stepB2 = _ic06_step_badge("ขั้นที่ 2: ลากเส้นทึบจากข้อต่อจริง (12, 23, 34, 14)", COL_OK).move_to(stepB_pos)
        self.play(ReplacementTransform(stepB1, stepB2), run_time=0.4)
        e12 = Line(node_pos[1], node_pos[2], color=COL_OK, stroke_width=3.0)
        e23 = Line(node_pos[2], node_pos[3], color=COL_OK, stroke_width=3.0)
        e34 = Line(node_pos[3], node_pos[4], color=COL_OK, stroke_width=3.0)
        e14 = Line(node_pos[4], node_pos[1], color=COL_OK, stroke_width=3.0)
        self.play(Create(e12), run_time=0.35)
        self.play(Create(e23), run_time=0.35)
        self.play(Create(e34), run_time=0.35)
        self.play(Create(e14), run_time=0.35)
        self.wait(0.5)

        # Step B3: missing diagonals highlighted
        stepB3 = _ic06_step_badge("ขั้นที่ 3: เส้นทแยงที่ยังขาด (13, 24) — ต้องใช้ Kennedy", COL_WARN).move_to(stepB_pos)
        self.play(ReplacementTransform(stepB2, stepB3), run_time=0.4)
        missing13 = DashedLine(node_pos[1], node_pos[3], color=COL_WARN, stroke_width=1.5)
        missing24 = DashedLine(node_pos[2], node_pos[4], color=COL_WARN, stroke_width=1.5)
        self.play(FadeIn(missing13, scale=0.9), FadeIn(missing24, scale=0.9), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(missing13), FadeOut(missing24), run_time=0.4)

        # Step B4a: triangle 1-2-3 has 12,23 -> find 13
        stepB4a = _ic06_step_badge("ขั้นที่ 4ก: สามเหลี่ยม 1-2-3 มี 12,23 ครบ → หา 13 ได้", COL_OK).move_to(stepB_pos)
        self.play(ReplacementTransform(stepB3, stepB4a), run_time=0.4)
        tri123 = Polygon(node_pos[1], node_pos[2], node_pos[3], color=COL_OK, stroke_width=0, fill_color=COL_OK).set_fill(COL_OK, 0.15)
        self.play(FadeIn(tri123), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(tri123), run_time=0.3)

        # Step B4b: triangle 1-3-4 has 34,14 -> confirms 13
        stepB4b = _ic06_step_badge("ขั้นที่ 4ข: สามเหลี่ยม 1-3-4 มี 34,14 ครบ → ยืนยัน 13", COL_OK).move_to(stepB_pos)
        self.play(ReplacementTransform(stepB4a, stepB4b), run_time=0.4)
        tri134 = Polygon(node_pos[1], node_pos[3], node_pos[4], color=COL_OK, stroke_width=0, fill_color=COL_OK).set_fill(COL_OK, 0.15)
        self.play(FadeIn(tri134), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(tri134), run_time=0.3)

        e13 = DashedLine(node_pos[1], node_pos[3], color=COL_OK, stroke_width=3.0)
        self.play(Create(e13), run_time=0.7)
        self.wait(0.4)

        # Step B5: repeat the same logic for 24
        stepB5 = _ic06_step_badge("ขั้นที่ 5: ทำนองเดียวกัน หา 24 จากสามเหลี่ยม 1-2-4 และ 2-3-4", COL_OK).move_to(stepB_pos)
        self.play(ReplacementTransform(stepB4b, stepB5), run_time=0.4)
        e24 = DashedLine(node_pos[2], node_pos[4], color=COL_OK, stroke_width=3.0)
        self.play(Create(e24), run_time=0.7)
        done_lbl = Text("ครบ N_IC = 6 เส้นแล้ว!", font_size=13, color=COL_OK, weight=BOLD).move_to([0.0, -2.75, 0.0])
        self.play(FadeIn(done_lbl, shift=UP * 0.2), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Summary Card
        # ==================================================================
        sum_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        sum_head = _ic06_badge("สรุป: ขั้นตอน Circle Diagram", COL_OK).move_to([0.0, 1.45, 0.0])
        rows = [
            "1. วาดวงกลม แบ่ง n จุด (จุดที่ 1 = เฟรม)",
            "2. ลากเส้นทึบเชื่อมคู่ที่หา IC ได้ตรงจากข้อต่อจริง",
            "3. คู่ที่ยังไม่มีเส้น → หาสามเหลี่ยมที่มีเส้นทึบครบ 2 ใน 3 ด้าน → เส้นที่ 3 คือคำตอบ (เส้นประ)",
            "4. ทำซ้ำจนครบ N_IC = n(n-1)/2 เส้น",
        ]
        s_rows = VGroup(*[Text(r, font_size=12, color=WHITE) for r in rows]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([0.0, -0.1, 0.0])
        fit_width(s_rows, 10.8)
        summary_card = VGroup(sum_box, sum_head, s_rows)

        self.play(FadeIn(summary_card, shift=UP * 0.4), run_time=0.6)
        self.wait(1.3)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Review Question (bridge to IC07)
        # ==================================================================
        q_box = RoundedRectangle(
            width=11.4, height=2.4, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_body = Text(
            "ลองเอาเทคนิคนี้ไปใช้กับกลไก 4-bar จริงดูไหม?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.2, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text("(คลิปต่อไป: ตัวอย่างจริง)", font_size=11, color=COL_GRAY).move_to([0.0, -0.4, 0.0])
        question_card = VGroup(q_box, q_body, q_ans)

        self.play(FadeIn(question_card, shift=UP * 0.3), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.7)


# ======================================================================
# Helper functions for IC07_FourBarExamples
# ======================================================================

def _ic07_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic07_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic07_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.55, 0.0])


def _ic07_step_badge(text, color=COL_OK):
    lbl = Text(text, font_size=12, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.4, height=0.38, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _ic07_line_intersect(p1, p2, p3, p4):
    """Intersection point of infinite lines through p1-p2 and p3-p4 (2D, z=0)."""
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    x4, y4 = p4[0], p4[1]
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    return np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1), 0.0])


class IC07_FourBarExamples(SafeScene):
    """
    W03 น.14-15 — ประยุกต์ Circle Diagram กับกลไก 4-bar จริง (2 ตัวอย่าง)
    Plan: Main_note/Claude_Specs/Manim — IC07_FourBarExamples Plan.md
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic07_title("ตัวอย่างจริง: 4-bar linkage")
        page_ref_m = _ic07_page_ref("W03 น.14-15")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.5: Hook Question
        # ==================================================================
        hook_q = _ic07_caption_top(
            "เทคนิค circle diagram ใช้กับกลไกจริงได้จริงไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.5)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)

        # ==================================================================
        # BEAT 4.5-5.2: Answer
        # ==================================================================
        cap1 = _ic07_caption_top("ได้จริง ลองดู 2 ตัวอย่าง")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # ==================================================================
        # EXAMPLE 1: ordinary four-bar (5.2-20.0), step-by-step per §48
        # ==================================================================
        ex1_pos = np.array([3.6, 1.9, 0.0])
        ex1_badge = _ic07_step_badge("Example 1: four-bar ธรรมดา", COL_OK).move_to(ex1_pos)
        self.play(FadeIn(ex1_badge, shift=UP * 0.2), run_time=0.4)

        O2 = np.array([-3.4, -2.6, 0.0])
        O4 = np.array([1.3, -2.6, 0.0])
        A = np.array([-2.1, -0.8, 0.0])
        B = np.array([0.5, -0.2, 0.0])

        ground = Line(O2 + [-0.6, 0, 0], O4 + [0.6, 0, 0], color=COL_GRAY, stroke_width=2.0)
        hatches1 = VGroup(*[
            Line([x, O2[1], 0], [x - 0.13, O2[1] - 0.17, 0], color="#64748B", stroke_width=1.2)
            for x in np.linspace(O2[0] - 0.5, O2[0] + 0.5, 6)
        ])
        hatches4 = VGroup(*[
            Line([x, O4[1], 0], [x - 0.13, O4[1] - 0.17, 0], color="#64748B", stroke_width=1.2)
            for x in np.linspace(O4[0] - 0.5, O4[0] + 0.5, 6)
        ])
        link2 = Line(O2, A, color=COL_FIELD, stroke_width=5)
        link3 = Line(A, B, color="#BA68C8", stroke_width=5)
        link4 = Line(B, O4, color=COL_WARN, stroke_width=5)

        self.play(Create(ground), FadeIn(hatches1), FadeIn(hatches4), run_time=0.5)
        self.play(Create(link2), run_time=0.5)
        dot_I12 = Dot(O2, radius=0.08, color=COL_OK)
        lbl_I12 = Text("I_12", font_size=10, color=COL_OK).next_to(dot_I12, DOWN, buff=0.12)
        self.play(FadeIn(dot_I12), FadeIn(lbl_I12), run_time=0.35)

        self.play(Create(link3), run_time=0.5)
        dot_I23 = Dot(A, radius=0.08, color=COL_OK)
        lbl_I23 = Text("I_23", font_size=10, color=COL_OK).next_to(dot_I23, UP + LEFT, buff=0.1)
        self.play(FadeIn(dot_I23), FadeIn(lbl_I23), run_time=0.35)

        self.play(Create(link4), run_time=0.5)
        dot_I34 = Dot(B, radius=0.08, color=COL_OK)
        lbl_I34 = Text("I_34", font_size=10, color=COL_OK).next_to(dot_I34, RIGHT, buff=0.12)
        self.play(FadeIn(dot_I34), FadeIn(lbl_I34), run_time=0.35)

        dot_I14 = Dot(O4, radius=0.08, color=COL_OK)
        lbl_I14 = Text("I_14", font_size=10, color=COL_OK).next_to(dot_I14, DOWN, buff=0.12)
        self.play(FadeIn(dot_I14), FadeIn(lbl_I14), run_time=0.35)
        self.wait(0.5)

        ex1_badge2 = _ic07_step_badge("หา I_13: ต่อเส้น I_12–I_23 กับ I_34–I_14", COL_WARN).move_to(ex1_pos)
        self.play(ReplacementTransform(ex1_badge, ex1_badge2), run_time=0.4)

        I13 = _ic07_line_intersect(O2, A, B, O4)
        d1 = (A - O2) / np.linalg.norm(A - O2)
        d2 = (O4 - B) / np.linalg.norm(O4 - B)
        ln1 = DashedLine(O2 - 0.2 * d1, I13 + 0.15 * d1, color=COL_WARN, stroke_width=1.8)
        ln2 = DashedLine(B - 0.2 * d2, I13 + 0.15 * d2, color=COL_WARN, stroke_width=1.8)
        self.play(Create(ln1), Create(ln2), run_time=0.8)
        dot_I13 = Dot(I13, radius=0.08, color=COL_WARN)
        lbl_I13 = Text("I_13", font_size=11, color=COL_WARN, weight=BOLD).next_to(dot_I13, UP, buff=0.1)
        self.play(FadeIn(dot_I13), FadeIn(lbl_I13), run_time=0.4)
        self.wait(0.6)

        ex1_badge3 = _ic07_step_badge("I_24: หาแบบเดียวกัน (ต่อเส้น I_23–I_34 กับ I_12–I_14)", COL_WARN).move_to(ex1_pos)
        self.play(ReplacementTransform(ex1_badge2, ex1_badge3), run_time=0.4)

        note_I24 = Text(
            "I_24 หาได้แบบเดียวกัน แต่มักตกอยู่ไกลนอกกรอบรูปที่วาด (เส้นเกือบขนานกัน)",
            font_size=11.5, color=COL_WARN
        ).move_to([0.0, -3.3, 0.0])
        fit_width(note_I24, 11.6)
        self.play(FadeIn(note_I24, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m)], run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # EXAMPLE 2: four-bar with a slider (20.6-36.0), §48 stepwise
        # ==================================================================
        cap2 = _ic07_caption_top("Example 2: เหมือนเดิม แต่ลิงก์ 4 เป็นสไลด์เดอร์ (prismatic กับเฟรม)")
        fit_width(cap2, 11.6)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        ex2_badge = _ic07_step_badge("โครงสร้างเดิม: link1(เฟรม)-2-3, หมุดที่ O2, A, B", COL_OK).move_to([3.6, 1.9, 0.0])
        self.play(FadeIn(ex2_badge, shift=UP * 0.2), run_time=0.4)

        O2b = np.array([-3.2, -1.5, 0.0])
        Ab = np.array([-1.9, 0.1, 0.0])
        Bb = np.array([0.9, 0.5, 0.0])

        hatches1b = VGroup(*[
            Line([x, O2b[1], 0], [x - 0.13, O2b[1] - 0.17, 0], color="#64748B", stroke_width=1.2)
            for x in np.linspace(O2b[0] - 0.5, O2b[0] + 0.5, 6)
        ])
        link2b = Line(O2b, Ab, color=COL_FIELD, stroke_width=5)
        link3b = Line(Ab, Bb, color="#BA68C8", stroke_width=5)
        self.play(FadeIn(hatches1b), Create(link2b), Create(link3b), run_time=0.7)
        dot_I12b = Dot(O2b, radius=0.08, color=COL_OK)
        dot_I23b = Dot(Ab, radius=0.08, color=COL_OK)
        dot_I34b = Dot(Bb, radius=0.08, color=COL_OK)
        lbls_b = VGroup(
            Text("I_12", font_size=10, color=COL_OK).next_to(dot_I12b, DOWN, buff=0.12),
            Text("I_23", font_size=10, color=COL_OK).next_to(dot_I23b, UP + LEFT, buff=0.1),
            Text("I_34", font_size=10, color=COL_OK).next_to(dot_I34b, UP, buff=0.1),
        )
        self.play(FadeIn(dot_I12b), FadeIn(dot_I23b), FadeIn(dot_I34b), FadeIn(lbls_b), run_time=0.5)
        self.wait(0.5)

        ex2_badge2 = _ic07_step_badge("Link 4 เป็นสไลด์เดอร์ → I_14 ที่ ∞ ⊥ ทิศไถล", COL_WARN).move_to([3.6, 1.9, 0.0])
        self.play(ReplacementTransform(ex2_badge, ex2_badge2), run_time=0.4)

        slide_dir = np.array([1.0, 0.15, 0.0])
        slide_dir = slide_dir / np.linalg.norm(slide_dir)
        rail = Line(Bb - 1.4 * slide_dir, Bb + 1.4 * slide_dir, color=COL_GRAY, stroke_width=2.0)
        block4 = RoundedRectangle(width=0.7, height=0.35, corner_radius=0.05, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.6).move_to(Bb)
        self.play(Create(rail), run_time=0.4)
        self.play(FadeIn(block4), run_time=0.4)

        perp = np.array([-slide_dir[1], slide_dir[0], 0.0])
        arr_up = Arrow(Bb + 0.35 * perp, Bb + 1.6 * perp, buff=0, color=COL_WARN, stroke_width=2.6, max_tip_length_to_length_ratio=0.15)
        arr_dn = Arrow(Bb - 0.35 * perp, Bb - 1.6 * perp, buff=0, color=COL_WARN, stroke_width=2.6, max_tip_length_to_length_ratio=0.15)
        self.play(GrowArrow(arr_up), GrowArrow(arr_dn), run_time=0.6)
        lbl_inf = Text("I_14 at ∞", font_size=11, color=COL_WARN, weight=BOLD).next_to(arr_up, RIGHT, buff=0.15)
        self.play(FadeIn(lbl_inf), run_time=0.4)
        self.wait(0.6)

        ex2_badge3 = _ic07_step_badge("Kennedy ยังใช้ได้ปกติ — แค่เส้นหนึ่งไปบรรจบทิศ ∞ แทนจุดจริง", COL_OK).move_to([3.6, 1.9, 0.0])
        self.play(ReplacementTransform(ex2_badge2, ex2_badge3), run_time=0.4)
        self.wait(2.2)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Review Question (bridge to IC08)
        # ==================================================================
        q_box = RoundedRectangle(
            width=11.4, height=2.4, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_body = Text(
            "ถ้ากลไกมี 6 ชิ้น (15 จุด IC) จะยังใช้เทคนิคเดิมไหวไหม?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.2, 0.0])
        fit_width(q_body, 10.6)
        q_ans = Text("(คลิปต่อไป: ตัวอย่างกลไก 6 ชิ้น)", font_size=11, color=COL_GRAY).move_to([0.0, -0.4, 0.0])
        question_card = VGroup(q_box, q_body, q_ans)

        self.play(FadeIn(question_card, shift=UP * 0.3), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.7)


# ======================================================================
# Helper functions for IC08_SixLinkExample
# ======================================================================

def _ic08_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic08_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic08_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.55, 0.0])


def _ic08_step_badge(text, color=COL_OK):
    lbl = Text(text, font_size=12, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.4, height=0.38, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC08_SixLinkExample(SafeScene):
    """
    W03 น.16-20 — กลไก 6 ชิ้น สไลด์เดอร์ 2 ตัว (N_IC=15, 2 จุดที่ ∞)
    Plan: Main_note/Claude_Specs/Manim — IC08_SixLinkExample Plan.md
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic08_title("กลไก 6 ชิ้น: สไลด์เดอร์ 2 ตัว")
        page_ref_m = _ic08_page_ref("W03 น.16-20")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.5: Hook Question
        # ==================================================================
        hook_q = _ic08_caption_top(
            "เทคนิคเดิมใช้กับกลไกที่ซับซ้อนกว่านี้ได้ไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.5)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)

        # ==================================================================
        # BEAT 4.5-7.0: Answer + Formula
        # ==================================================================
        cap1 = _ic08_caption_top("ได้ — หลักการเดียวกัน แค่ N มากขึ้น: n=6 → N_IC = 6×5/2 = 15 จุด")
        fit_width(cap1, 11.6)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)
        self.wait(1.3)

        # ==================================================================
        # BEAT 7.0-22.0: Build mechanism step by step (§48)
        # ==================================================================
        pos_badge = np.array([3.6, 1.9, 0.0])
        step1 = _ic08_step_badge("สร้างกลไกทีละขั้น: เฟรม (ผนัง+พื้น)", COL_OK).move_to(pos_badge)
        self.play(FadeIn(step1, shift=UP * 0.2), run_time=0.4)

        wall = Line([-4.3, -2.2, 0], [-4.3, 1.3, 0], color=COL_GRAY, stroke_width=2.0)
        wall_hatch = VGroup(*[
            Line([-4.3, y, 0], [-4.5, y - 0.16, 0], color="#64748B", stroke_width=1.2)
            for y in np.linspace(-2.0, 1.1, 8)
        ])
        ground = Line([-4.3, -2.2, 0], [3.0, -2.2, 0], color=COL_GRAY, stroke_width=2.0)
        ground_hatch = VGroup(*[
            Line([x, -2.2, 0], [x - 0.16, -2.38, 0], color="#64748B", stroke_width=1.2)
            for x in np.linspace(-4.1, 2.8, 12)
        ])
        self.play(Create(wall), FadeIn(wall_hatch), Create(ground), FadeIn(ground_hatch), run_time=0.6)

        I12 = np.array([-4.3, 0.2, 0.0])
        A = np.array([-2.5, 0.9, 0.0])
        u3 = np.array([1.0, -0.28, 0.0]) / np.linalg.norm([1.0, -0.28, 0.0])
        A2 = A + 1.7 * u3
        B = np.array([0.3, -0.5, 0.0])
        C = np.array([2.2, -2.2, 0.0])

        step2 = _ic08_step_badge("Link 2: หมุดที่ I_12 (ผนัง)", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step1, step2), run_time=0.4)
        link2 = Line(I12, A, color=COL_FIELD, stroke_width=5)
        self.play(Create(link2), run_time=0.5)
        dot_I12 = Dot(I12, radius=0.08, color=COL_OK)
        lbl_I12 = Text("I_12", font_size=10, color=COL_OK).next_to(dot_I12, LEFT, buff=0.12)
        self.play(FadeIn(dot_I12), FadeIn(lbl_I12), run_time=0.35)

        step3 = _ic08_step_badge("Link 3: หมุดที่ I_23", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step2, step3), run_time=0.4)
        link3 = Line(A, A2 + 0.5 * u3, color="#BA68C8", stroke_width=5)
        self.play(Create(link3), run_time=0.5)
        dot_I23 = Dot(A, radius=0.08, color=COL_OK)
        lbl_I23 = Text("I_23", font_size=10, color=COL_OK).next_to(dot_I23, UP, buff=0.1)
        self.play(FadeIn(dot_I23), FadeIn(lbl_I23), run_time=0.35)

        step4 = _ic08_step_badge("Link 4: สไลเดอร์บน Link 3 → หมุดที่ I_45", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step3, step4), run_time=0.4)
        perp3 = np.array([-u3[1], u3[0], 0.0])
        block34 = RoundedRectangle(width=0.55, height=0.32, corner_radius=0.05, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.6)
        block34.rotate(np.arctan2(u3[1], u3[0])).move_to(A2)
        self.play(FadeIn(block34), run_time=0.4)
        link4 = Line(A2, B, color=COL_CURR, stroke_width=5)
        self.play(Create(link4), run_time=0.5)
        dot_I45 = Dot(B, radius=0.08, color=COL_OK)
        lbl_I45 = Text("I_45", font_size=10, color=COL_OK).next_to(dot_I45, DOWN, buff=0.12)
        self.play(FadeIn(dot_I45), FadeIn(lbl_I45), run_time=0.35)

        step5 = _ic08_step_badge("Link 5-6: หมุดที่ I_56 → บล็อกสไลด์บนพื้น", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step4, step5), run_time=0.4)
        link5 = Line(B, C, color=COL_FORCE, stroke_width=5)
        self.play(Create(link5), run_time=0.5)
        block56 = RoundedRectangle(width=0.6, height=0.3, corner_radius=0.05, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.6).move_to(C)
        self.play(FadeIn(block56), run_time=0.4)
        dot_I56 = Dot(C, radius=0.08, color=COL_OK)
        lbl_I56 = Text("I_56", font_size=10, color=COL_OK).next_to(dot_I56, UP, buff=0.16)
        self.play(FadeIn(dot_I56), FadeIn(lbl_I56), run_time=0.35)
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m)], run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 22.6-33.0: Two points at infinity
        # ==================================================================
        cap2 = _ic08_caption_top("จุดที่ ∞ (novel): สไลด์เดอร์ 2 ตัว → จุด ∞ 2 จุด คนละทิศกัน")
        fit_width(cap2, 11.6)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        self.play(Create(wall), FadeIn(wall_hatch), Create(ground), FadeIn(ground_hatch), run_time=0.5)
        self.play(Create(link2), Create(link3), Create(link4), Create(link5), run_time=0.6)
        self.play(FadeIn(block34), FadeIn(block56), FadeIn(dot_I12), FadeIn(dot_I45), FadeIn(dot_I56), run_time=0.5)

        step6 = _ic08_step_badge("ข้อต่อ 3-4 เป็นสไลด์เดอร์ → I_34 at ∞ ⊥ ทิศไถลของ link3", COL_WARN).move_to(pos_badge)
        self.play(FadeIn(step6, shift=UP * 0.2), run_time=0.4)
        arr34a = Arrow(A2 + 0.3 * perp3, A2 + 1.3 * perp3, buff=0, color=COL_WARN, stroke_width=2.6, max_tip_length_to_length_ratio=0.18)
        arr34b = Arrow(A2 - 0.3 * perp3, A2 - 1.3 * perp3, buff=0, color=COL_WARN, stroke_width=2.6, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(arr34a), GrowArrow(arr34b), run_time=0.6)
        lbl_I34 = Text("I_34 at ∞", font_size=10.5, color=COL_WARN, weight=BOLD).next_to(arr34a, RIGHT, buff=0.12)
        self.play(FadeIn(lbl_I34), run_time=0.4)
        self.wait(1.0)

        step7 = _ic08_step_badge("Link 6 สไลด์บนพื้น (แนวนอน) → I_16 at ∞ (แนวตั้ง)", COL_WARN).move_to(pos_badge)
        self.play(ReplacementTransform(step6, step7), run_time=0.4)
        arr16 = Arrow(C + [0, 0.3, 0], C + [0, 1.5, 0], buff=0, color=COL_WARN, stroke_width=2.6, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(arr16), run_time=0.5)
        lbl_I16 = Text("I_16 at ∞", font_size=10.5, color=COL_WARN, weight=BOLD).next_to(arr16, RIGHT, buff=0.12)
        self.play(FadeIn(lbl_I16), run_time=0.4)

        note_diff = Text(
            "I_34 กับ I_16 อยู่ที่ ∞ คนละทิศกัน — เป็นเส้นขนานคนละแนว ไม่ใช่จุดเดียวกัน",
            font_size=11.5, color=COL_WARN
        ).move_to([0.0, -2.9, 0.0])
        fit_width(note_diff, 11.6)
        self.play(FadeIn(note_diff, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title_m, page_ref_m)], run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 33.6-38.0: One Kennedy-derived example (I13)
        # ==================================================================
        cap3 = _ic08_caption_top("ตัวอย่าง Kennedy-derived 1 จุด: หา I_13 จากสามเหลี่ยม 1-2-3")
        fit_width(cap3, 11.6)
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        self.play(Create(wall), FadeIn(wall_hatch), Create(ground), FadeIn(ground_hatch), run_time=0.4)
        self.play(Create(link2), run_time=0.4)
        self.play(FadeIn(dot_I12), FadeIn(lbl_I12), FadeIn(dot_I23), FadeIn(lbl_I23), run_time=0.4)

        d1 = (A - I12) / np.linalg.norm(A - I12)
        I13 = I12 + 3.6 * d1
        ln13 = DashedLine(I12 - 0.3 * d1, I13, color=COL_WARN, stroke_width=1.8)
        self.play(Create(ln13), run_time=0.7)
        dot_I13 = Dot(I13, radius=0.08, color=COL_WARN)
        lbl_I13 = Text("I_13", font_size=11, color=COL_WARN, weight=BOLD).next_to(dot_I13, RIGHT, buff=0.1)
        self.play(FadeIn(dot_I13), FadeIn(lbl_I13), run_time=0.4)

        note_rest = Text(
            "อีก 11 จุดที่เหลือ ใช้หลักการเดียวกันนี้ทั้งหมด (ไม่ไล่ครบในคลิปนี้)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -2.9, 0.0])
        fit_width(note_rest, 11.6)
        self.play(FadeIn(note_rest, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Review Question (bridge to IC09)
        # ==================================================================
        q_box2 = RoundedRectangle(
            width=11.4, height=2.4, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_body2 = Text(
            "รู้ตำแหน่ง IC ครบแล้ว จะหาความเร็วจริงโดยไม่ต้องรู้ ω ได้ไหม?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.2, 0.0])
        fit_width(q_body2, 10.6)
        q_ans2 = Text("(คลิปต่อไป: สูตรอัตราส่วนความเร็วจาก IC)", font_size=11, color=COL_GRAY).move_to([0.0, -0.4, 0.0])
        question_card2 = VGroup(q_box2, q_body2, q_ans2)

        self.play(FadeIn(question_card2, shift=UP * 0.3), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.7)


# ======================================================================
# Helper functions for IC09_VelocityRatioFormula
# ======================================================================

def _ic09_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic09_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic09_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.55, 0.0])


def _ic09_step_badge(text, color=COL_OK):
    lbl = Text(text, font_size=12, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.4, height=0.38, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC09_VelocityRatioFormula(SafeScene):
    """
    W03 น.21 — สูตรความเร็วจาก IC (ไม่ต้องรู้ ω)
    Plan: Main_note/Claude_Specs/Manim — IC09_VelocityRatioFormula Plan.md
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic09_title("สูตรความเร็วจาก IC (ไม่ต้องรู้ ω)")
        page_ref_m = _ic09_page_ref("W03 น.21")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.5: Hook Question
        # ==================================================================
        hook_q = _ic09_caption_top(
            "ต้องรู้ ω ก่อนเสมอไหม ถึงจะหาความเร็วจุดอื่นบนลิงก์เดียวกันได้?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.5)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)

        # ==================================================================
        # BEAT 4.5-5.2: Answer
        # ==================================================================
        cap1 = _ic09_caption_top("ไม่จำเป็น ถ้ารู้ความเร็วจุดหนึ่งบนลิงก์เดียวกันอยู่แล้ว")
        fit_width(cap1, 11.6)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # ==================================================================
        # BEAT 5.2-20.0: Build the diagram step by step (§48)
        # ==================================================================
        pos_badge = np.array([3.6, 1.9, 0.0])
        step1 = _ic09_step_badge("วัตถุ 3 เกร็ง เคลื่อนที่ เทียบชิ้น 1 (หยุดนิ่ง)", COL_OK).move_to(pos_badge)
        self.play(FadeIn(step1, shift=UP * 0.2), run_time=0.4)

        blob_center = np.array([-1.6, -0.4, 0.0])
        angles = np.linspace(0, 2 * np.pi, 24, endpoint=False)
        radii = 1.3 + 0.35 * np.cos(angles) - 0.2 * np.sin(2 * angles) + 0.15 * np.cos(3 * angles)
        blob_pts = [blob_center + np.array([r * np.cos(a), 0.68 * r * np.sin(a), 0.0]) for a, r in zip(angles, radii)]
        body_blob = Polygon(*blob_pts, color="#B08968", stroke_width=3.0, fill_color="#8D6E63").set_fill("#8D6E63", 0.4)
        lbl_body = Text("ชิ้น 3", font_size=11, color="#D7B899").move_to(blob_center)
        self.play(Create(body_blob), FadeIn(lbl_body), run_time=0.6)
        self.wait(0.3)

        IC13 = np.array([2.2, -0.4, 0.0])
        dot_IC13 = Dot(IC13, radius=0.09, color=COL_OK)
        lbl_IC13 = Text("I_13", font_size=12, color=COL_OK, weight=BOLD).next_to(dot_IC13, RIGHT, buff=0.12)
        self.play(FadeIn(dot_IC13), FadeIn(lbl_IC13), run_time=0.4)
        self.wait(0.3)

        step2 = _ic09_step_badge("จุด P บนวัตถุ: v_P ⊥ r_(P/I13)", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step1, step2), run_time=0.4)
        P = blob_center + np.array([-0.75, 0.55, 0.0])
        r_P = P - IC13
        rP_dir = r_P / np.linalg.norm(r_P)
        vP_dir = np.array([-rP_dir[1], rP_dir[0], 0.0])
        line_rP = Line(IC13, P, color=COL_GRAY, stroke_width=1.6)
        dot_P = Dot(P, radius=0.07, color=WHITE)
        lbl_P = Text("P", font_size=11, color=WHITE).next_to(dot_P, UP, buff=0.1)
        self.play(Create(line_rP), FadeIn(dot_P), FadeIn(lbl_P), run_time=0.5)
        vP_arrow = Arrow(P, P + 1.1 * vP_dir, buff=0, color=COL_FORCE, stroke_width=3.6, max_tip_length_to_length_ratio=0.22)
        lbl_vP = Text("v_P", font_size=11, color=COL_FORCE).next_to(vP_arrow.get_end(), vP_dir, buff=0.15)
        self.play(GrowArrow(vP_arrow), FadeIn(lbl_vP), run_time=0.5)
        self.wait(0.4)

        step3 = _ic09_step_badge("จุด S บนวัตถุ: v_S ⊥ r_(S/I13)", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step2, step3), run_time=0.4)
        S = blob_center + np.array([0.15, -0.7, 0.0])
        r_S = S - IC13
        rS_dir = r_S / np.linalg.norm(r_S)
        vS_dir = np.array([-rS_dir[1], rS_dir[0], 0.0])
        line_rS = Line(IC13, S, color=COL_GRAY, stroke_width=1.6)
        dot_S = Dot(S, radius=0.07, color=WHITE)
        lbl_S = Text("S", font_size=11, color=WHITE).next_to(dot_S, DOWN, buff=0.1)
        self.play(Create(line_rS), FadeIn(dot_S), FadeIn(lbl_S), run_time=0.5)
        vS_arrow = Arrow(S, S + 0.75 * vS_dir, buff=0, color=COL_CURR, stroke_width=3.6, max_tip_length_to_length_ratio=0.22)
        lbl_vS = Text("v_S", font_size=11, color=COL_CURR).next_to(vS_arrow.get_end(), DOWN, buff=0.08)
        self.play(GrowArrow(vS_arrow), FadeIn(lbl_vS), run_time=0.5)
        self.wait(0.5)

        step4 = _ic09_step_badge("(a) |V_P|=r_(P/I13)·ω₃   (b) |V_S|=r_(S/I13)·ω₃", COL_WARN).move_to(pos_badge)
        self.play(ReplacementTransform(step3, step4), run_time=0.4)
        self.wait(2.0)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 20.6-24.0: Summary formula card
        # ==================================================================
        f_box = RoundedRectangle(
            width=8.5, height=1.8, corner_radius=0.12,
            color=COL_OK, stroke_width=2.4, fill_color="#0F766E"
        ).set_fill("#0F766E", 0.3).move_to([0.0, 0.1, 0.0])
        f_text = Text("|V_S| = |V_P| × (r_(S/IC) / r_(P/IC))", font_size=17, color=YELLOW, weight=BOLD).move_to([0.0, 0.4, 0.0])
        f_sub = Text("ω หายไปจากสมการพอดี — ไม่ต้องรู้ ω เลย ถ้ารู้ v ที่จุดหนึ่งบนลิงก์เดียวกัน", font_size=11.5, color=WHITE).move_to([0.0, -0.15, 0.0])
        fit_width(f_sub, 8.2)
        f_grp = VGroup(f_box, f_text, f_sub)
        self.play(FadeIn(f_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(2.3)

        self.play(FadeOut(f_grp), run_time=0.4)

        # ==================================================================
        # BEAT 24.0-30.0: Direction rule (exam-critical)
        # ==================================================================
        rule_box = RoundedRectangle(
            width=11.4, height=3.0, corner_radius=0.15,
            color=COL_BAD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        rule_head = Text("จุดออกสอบ ⭐⭐⭐ — หัวใจของการใช้ IC หาความเร็ว", font_size=14, color=COL_BAD, weight=BOLD).move_to([0.0, 1.0, 0.0])
        rule_body = Text(
            "ทิศทางของ V_S ตั้งฉากกับเส้น S–IC เสมอ (เหมือนหมุนรอบจุดหมุน)",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.35, 0.0])
        fit_width(rule_body, 10.6)
        rule_sub = Text(
            "ขนาดใช้สัดส่วนระยะทางจาก IC ได้เลย ไม่ต้องรู้ ω จริง ถ้ารู้ v จุดหนึ่งบนลิงก์เดียวกันอยู่แล้ว",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.35, 0.0])
        fit_width(rule_sub, 10.6)
        rule_grp = VGroup(rule_box, rule_head, rule_body, rule_sub)
        self.play(FadeIn(rule_grp, shift=UP * 0.4), run_time=0.6)
        self.wait(2.5)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Review Question (bridge to IC10)
        # ==================================================================
        q_box3 = RoundedRectangle(
            width=11.4, height=2.4, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_body3 = Text(
            "ลองใช้สูตรนี้กับโจทย์จริง (กลไก 6 ชิ้น) ดูไหม?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.2, 0.0])
        fit_width(q_body3, 10.6)
        q_ans3 = Text("(คลิปต่อไป: โจทย์ transfer point)", font_size=11, color=COL_GRAY).move_to([0.0, -0.4, 0.0])
        question_card3 = VGroup(q_box3, q_body3, q_ans3)

        self.play(FadeIn(question_card3, shift=UP * 0.3), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.7)


# ======================================================================
# Helper functions for IC10_TransferPointExample
# ======================================================================

def _ic10_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic10_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic10_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.55, 0.0])


def _ic10_step_badge(text, color=COL_OK):
    lbl = Text(text, font_size=12, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.4, height=0.38, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC10_TransferPointExample(SafeScene):
    """
    W03 น.22-24 — โจทย์ transfer point: หา v_B จาก v_A ในกลไก 6 ชิ้น
    Plan: Main_note/Claude_Specs/Manim — IC10_TransferPointExample Plan.md
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic10_title("โจทย์: หา v_B จาก v_A (Transfer Point)")
        page_ref_m = _ic10_page_ref("W03 น.22-24")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.5: Hook Question
        # ==================================================================
        hook_q = _ic10_caption_top(
            "รู้ v ที่ A แต่ B อยู่คนละลิงก์ที่ไม่ติดกัน จะหา v_B ได้ไหม?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.5)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)

        # ==================================================================
        # BEAT 4.5-5.2: Answer
        # ==================================================================
        cap1 = _ic10_caption_top("ได้ — ใช้ 'transfer point' เป็นสะพานเชื่อมข้ามลิงก์")
        fit_width(cap1, 11.6)
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # ==================================================================
        # BEAT 5.2-28.0: 6 standard steps (§48 stepwise), schematic mechanism
        # ==================================================================
        pos_badge = np.array([3.6, 1.9, 0.0])

        wall = Line([-4.3, -2.2, 0], [-4.3, 1.3, 0], color=COL_GRAY, stroke_width=2.0)
        wall_hatch = VGroup(*[
            Line([-4.3, y, 0], [-4.5, y - 0.16, 0], color="#64748B", stroke_width=1.2)
            for y in np.linspace(-2.0, 1.1, 7)
        ])
        I12 = np.array([-4.3, 0.2, 0.0])
        A = np.array([-2.0, 0.9, 0.0])
        I15 = np.array([-1.0, -1.6, 0.0])
        B = np.array([1.8, -0.3, 0.0])
        I25 = np.array([1.2, 1.6, 0.0])

        link2 = Line(I12, A, color=COL_FIELD, stroke_width=5)
        link5 = Line(I15, B, color=COL_FORCE, stroke_width=5)

        step1 = _ic10_step_badge("ขั้น 1: หา IC ที่จำเป็นแค่ 3 จุด: I_12, I_15, I_25", COL_OK).move_to(pos_badge)
        self.play(FadeIn(step1, shift=UP * 0.2), run_time=0.4)
        self.play(Create(wall), FadeIn(wall_hatch), run_time=0.5)
        self.wait(0.5)

        step2 = _ic10_step_badge("ขั้น 2: I_12 จาก revolute joint ตรงๆ", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step1, step2), run_time=0.4)
        self.play(Create(link2), run_time=0.5)
        dot_I12 = Dot(I12, radius=0.08, color=COL_OK)
        lbl_I12 = Text("I_12", font_size=10, color=COL_OK).next_to(dot_I12, LEFT, buff=0.12)
        lbl_A = Text("A", font_size=11, color=WHITE).next_to(A, UP, buff=0.1)
        dot_A = Dot(A, radius=0.07, color=WHITE)
        self.play(FadeIn(dot_I12), FadeIn(lbl_I12), FadeIn(dot_A), FadeIn(lbl_A), run_time=0.4)
        self.wait(0.4)

        step3 = _ic10_step_badge("ขั้น 3: หา I_13 ก่อน (ลากเส้น Kennedy ตัดกัน)", COL_WARN).move_to(pos_badge)
        self.play(ReplacementTransform(step2, step3), run_time=0.4)
        I13_ghost = np.array([-1.8, -0.6, 0.0])
        ln_a = DashedLine(I12, I13_ghost, color=COL_WARN, stroke_width=1.6)
        ln_b = DashedLine(A + [1.0, -0.3, 0], I13_ghost, color=COL_WARN, stroke_width=1.6)
        self.play(Create(ln_a), Create(ln_b), run_time=0.6)
        dot_I13 = Dot(I13_ghost, radius=0.07, color=COL_WARN)
        lbl_I13 = Text("I_13", font_size=10, color=COL_WARN).next_to(dot_I13, DOWN, buff=0.1)
        self.play(FadeIn(dot_I13), FadeIn(lbl_I13), run_time=0.4)
        self.wait(0.4)

        step4 = _ic10_step_badge("ขั้น 4: หา I_15 (Kennedy จาก I_13)", COL_WARN).move_to(pos_badge)
        self.play(ReplacementTransform(step3, step4), run_time=0.4)
        ln_c = DashedLine(I13_ghost, I15, color=COL_WARN, stroke_width=1.6)
        self.play(Create(ln_c), run_time=0.5)
        self.play(Create(link5), run_time=0.5)
        dot_I15 = Dot(I15, radius=0.08, color=COL_OK)
        lbl_I15 = Text("I_15", font_size=10, color=COL_OK).next_to(dot_I15, DOWN, buff=0.1)
        dot_B = Dot(B, radius=0.07, color=WHITE)
        lbl_B = Text("B", font_size=11, color=WHITE).next_to(B, RIGHT, buff=0.1)
        self.play(FadeIn(dot_I15), FadeIn(lbl_I15), FadeIn(dot_B), FadeIn(lbl_B), run_time=0.4)
        self.wait(0.4)

        step5 = _ic10_step_badge("ขั้น 5: หา I_25 = transfer point (Kennedy)", COL_WARN).move_to(pos_badge)
        self.play(ReplacementTransform(step4, step5), run_time=0.4)
        ln_d = DashedLine(A, I25, color=COL_CURR, stroke_width=1.6)
        ln_e = DashedLine(I15, I25, color=COL_CURR, stroke_width=1.6)
        self.play(Create(ln_d), Create(ln_e), run_time=0.6)
        dot_I25 = Dot(I25, radius=0.09, color=COL_CURR)
        diamond_I25 = Square(side_length=0.22, color=COL_CURR, stroke_width=2.2).rotate(np.radians(45)).move_to(I25)
        # label placed in open space below-right of the dot (away from the
        # top-right badge zone, the up-left transfer arrow, and the two
        # construction lines converging on the dot from the left) with a
        # short leader line back to the dot (§29/§30 pattern)
        lbl_I25_pos = I25 + np.array([1.15, -0.55, 0.0])
        lbl_I25 = Text("I_25 (transfer point)", font_size=10.5, color=COL_CURR, weight=BOLD).move_to(lbl_I25_pos)
        leader_I25 = DashedLine(lbl_I25.get_top(), dot_I25.get_center(), color=COL_CURR, stroke_width=1.2, dash_length=0.08)
        self.play(FadeIn(dot_I25), FadeIn(diamond_I25), FadeIn(lbl_I25), Create(leader_I25), run_time=0.5)
        self.wait(1.0)

        step6 = _ic10_step_badge("ขั้น 6: สร้างรูปสามเหลี่ยมความเร็ว (ดูขั้นต่อไป)", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step5, step6), run_time=0.4)
        self.wait(1.5)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 28.6-44.0: Step 6 in detail — the velocity triangle chain
        # ==================================================================
        cap2 = _ic10_caption_top("ขั้นที่ 6: v_A → v_I25 (ผ่าน I_12) → v_B (ผ่าน I_15)")
        fit_width(cap2, 11.6)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        self.play(Create(link2), Create(link5), run_time=0.5)
        self.play(FadeIn(dot_I12), FadeIn(lbl_I12), FadeIn(dot_A), FadeIn(lbl_A), run_time=0.3)
        self.play(FadeIn(dot_I15), FadeIn(lbl_I15), FadeIn(dot_B), FadeIn(lbl_B), run_time=0.3)
        self.play(FadeIn(dot_I25), FadeIn(diamond_I25), FadeIn(lbl_I25), Create(leader_I25), run_time=0.3)
        link_transfer = DashedLine(A, I25, color=COL_CURR, stroke_width=1.4)
        link_transfer2 = DashedLine(I15, I25, color=COL_CURR, stroke_width=1.4)
        self.play(Create(link_transfer), Create(link_transfer2), run_time=0.5)
        self.wait(0.3)

        # v_A: known, perpendicular to r(A/I12)
        rA_dir = (A - I12) / np.linalg.norm(A - I12)
        vA_dir = np.array([-rA_dir[1], rA_dir[0], 0.0])
        vA_arrow = Arrow(A, A + 1.0 * vA_dir, buff=0, color=COL_FORCE, stroke_width=3.6, max_tip_length_to_length_ratio=0.22)
        lbl_vA = Text("v_A (รู้ค่า)", font_size=10.5, color=COL_FORCE).next_to(vA_arrow.get_end(), vA_dir, buff=0.12)
        self.play(GrowArrow(vA_arrow), FadeIn(lbl_vA), run_time=0.6)
        self.wait(0.5)

        step_a = _ic10_step_badge("v_I25 = v_A × (r_(I25/I12) / r_(A/I12))", COL_WARN).move_to([3.6, 1.9, 0.0])
        self.play(FadeIn(step_a, shift=UP * 0.2), run_time=0.4)
        ratio1 = np.linalg.norm(I25 - I12) / np.linalg.norm(A - I12)
        rI25_dir = (I25 - I12) / np.linalg.norm(I25 - I12)
        vI25_dir = np.array([-rI25_dir[1], rI25_dir[0], 0.0])
        vI25_len = min(1.0 * ratio1, 0.55)
        vI25_arrow = Arrow(I25, I25 + vI25_len * vI25_dir, buff=0, color=COL_CURR, stroke_width=3.6, max_tip_length_to_length_ratio=0.2)
        lbl_vI25 = Text("v_I25", font_size=10.5, color=COL_CURR).next_to(vI25_arrow.get_end(), vI25_dir, buff=0.12)
        self.play(GrowArrow(vI25_arrow), FadeIn(lbl_vI25), run_time=0.6)
        self.wait(0.5)

        step_b = _ic10_step_badge("I_25 อยู่บนลิงก์ 5 ด้วย → ความเร็วเดียวกันนี้ 'ถ่ายโอน' ข้ามลิงก์", COL_CURR).move_to([3.6, 1.9, 0.0])
        self.play(ReplacementTransform(step_a, step_b), run_time=0.4)
        self.wait(1.2)

        step_c = _ic10_step_badge("v_B = v_I25 × (r_(B/I15) / r_(I25/I15)), ⊥ เส้น B–I_15", COL_OK).move_to([3.6, 1.9, 0.0])
        self.play(ReplacementTransform(step_b, step_c), run_time=0.4)
        ratio2 = np.linalg.norm(B - I15) / np.linalg.norm(I25 - I15)
        rB_dir = (B - I15) / np.linalg.norm(B - I15)
        vB_dir = np.array([-rB_dir[1], rB_dir[0], 0.0])
        vB_len = min(vI25_len * ratio2, 1.5)
        vB_arrow = Arrow(B, B + vB_len * vB_dir, buff=0, color=COL_OK, stroke_width=4.0, max_tip_length_to_length_ratio=0.2)
        lbl_vB = Text("v_B", font_size=12, color=COL_OK, weight=BOLD).next_to(vB_arrow.get_end(), vB_dir, buff=0.12)
        self.play(GrowArrow(vB_arrow), FadeIn(lbl_vB), run_time=0.6)
        self.wait(2.5)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT: Review Question (bridge to IC11)
        # ==================================================================
        q_box4 = RoundedRectangle(
            width=11.4, height=2.4, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_body4 = Text(
            "ถ้ามีทางเลือก transfer point หลายจุด จะได้คำตอบต่างกันไหม?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.2, 0.0])
        fit_width(q_body4, 10.6)
        q_ans4 = Text("(คลิปต่อไป: โจทย์สไลด์เดอร์หลายทาง)", font_size=11, color=COL_GRAY).move_to([0.0, -0.4, 0.0])
        question_card4 = VGroup(q_box4, q_body4, q_ans4)

        self.play(FadeIn(question_card4, shift=UP * 0.3), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.7)


# ======================================================================
# Helper functions for IC11_SliderMultiPath
# ======================================================================

def _ic11_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _ic11_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _ic11_caption_top(text, color=WHITE):
    return Text(text, font_size=13, color=color).move_to([0.0, 2.55, 0.0])


def _ic11_step_badge(text, color=COL_OK):
    lbl = Text(text, font_size=12, color=color, weight=BOLD)
    bg = RoundedRectangle(
        width=lbl.width + 0.4, height=0.38, corner_radius=0.10,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class IC11_SliderMultiPath(SafeScene):
    """
    W03 น.25-27 — Example 2: สไลด์เดอร์คร่อม 2 ก้าน, แก้ได้หลายเส้นทาง (คำตอบเดียวกัน)
    Plan: Main_note/Claude_Specs/Manim — IC11_SliderMultiPath Plan.md
    Last clip in the 11-clip W03 Instant Center series.
    """

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        pos_badge = np.array([3.6, 1.9, 0.0])

        # ==================================================================
        # BEAT 0.0-1.8: Title & Page Reference
        # ==================================================================
        title_m = _ic11_title("โจทย์: สไลด์เดอร์คร่อม 2 ก้าน — แก้ได้หลายทาง")
        page_ref_m = _ic11_page_ref("W03 น.25-27")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(page_ref_m), run_time=1.2)
        self.wait(0.4)

        # ==================================================================
        # BEAT 1.8-4.8: Hook question + answer
        # ==================================================================
        hook_q = _ic11_caption_top(
            "รู้ v_A=3 m/s หา v_C — มีตัวเลือกมองจุด/transfer point หลายแบบ วิธีไหน 'ถูก'?",
            color=COL_WARN
        )
        fit_width(hook_q, 11.6)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.5)
        self.wait(1.6)
        self.play(FadeOut(hook_q), run_time=0.4)

        cap0 = _ic11_caption_top("ทุกทางถูกหมด — IC เป็นสมบัติของกลไกทั้งระบบ", color=COL_OK)
        fit_width(cap0, 11.6)
        self.play(FadeIn(cap0, shift=UP * 0.35), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(cap0), run_time=0.4)

        # ==================================================================
        # BEAT 4.8-9.6: Mechanism setup (schematic, abbreviated like IC10)
        # ==================================================================
        wall = Line([-4.3, -2.2, 0], [-4.3, 1.3, 0], color=COL_GRAY, stroke_width=2.0)
        wall_hatch = VGroup(*[
            Line([-4.3, y, 0], [-4.5, y - 0.16, 0], color="#64748B", stroke_width=1.2)
            for y in np.linspace(-2.0, 1.1, 7)
        ])
        rail = Line([1.8, -1.8, 0], [4.3, -1.8, 0], color=COL_GRAY, stroke_width=3.0)
        rail_hatch = VGroup(*[
            Line([x, -1.8, 0], [x - 0.16, -2.0, 0], color="#64748B", stroke_width=1.2)
            for x in np.linspace(2.0, 4.2, 6)
        ])

        I13 = np.array([-4.0, 0.3, 0.0])
        A = np.array([-1.6, 1.2, 0.0])
        I35 = np.array([1.0, 1.5, 0.0])
        I15 = np.array([-0.8, -1.8, 0.0])
        C = np.array([3.2, -1.55, 0.0])  # slider block rides just above the rail line (avoid label/line overlap)

        link3 = Line(I13, A, color=COL_FIELD, stroke_width=5)
        link5 = Line(I15, C, color=COL_FORCE, stroke_width=5)

        self.play(Create(wall), FadeIn(wall_hatch), Create(rail), FadeIn(rail_hatch), run_time=0.6)
        self.play(Create(link3), Create(link5), run_time=0.6)

        dot_A = Dot(A, radius=0.07, color=WHITE)
        lbl_A = Text("A", font_size=11, color=WHITE).next_to(A, UP, buff=0.1)
        dot_C = Dot(C, radius=0.07, color=WHITE)
        lbl_C = Text("C", font_size=11, color=WHITE).next_to(C, UP, buff=0.12)
        self.play(FadeIn(dot_A), FadeIn(lbl_A), FadeIn(dot_C), FadeIn(lbl_C), run_time=0.4)

        setup_cap = _ic11_caption_top("รู้ v_A = 3 m/s (บนลิงก์ 3) → หา v_C (สไลด์เดอร์บนราง)")
        fit_width(setup_cap, 11.6)
        self.play(FadeIn(setup_cap, shift=UP * 0.3), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(setup_cap), run_time=0.4)

        # ==================================================================
        # BEAT 9.6-19.1: Method 1 — links 1, 3, 5
        # ==================================================================
        m1_cap = _ic11_caption_top("วิธี 1: พิจารณาลิงก์ 1, 3, 5", color=COL_FIELD)
        fit_width(m1_cap, 11.6)
        self.play(FadeIn(m1_cap, shift=UP * 0.3), run_time=0.5)

        step1 = _ic11_step_badge("ขั้น 1: หา I_13 (pivot)", COL_OK).move_to(pos_badge)
        self.play(FadeIn(step1, shift=UP * 0.2), run_time=0.4)
        ln_a = DashedLine([-4.3, 0.9, 0], I13, color=COL_OK, stroke_width=1.6)
        ln_b = DashedLine(A + np.array([0.0, -0.9, 0.0]), I13, color=COL_OK, stroke_width=1.6)
        self.play(Create(ln_a), Create(ln_b), run_time=0.6)
        dot_I13 = Dot(I13, radius=0.08, color=COL_OK)
        lbl_I13 = Text("I_13", font_size=10, color=COL_OK).next_to(dot_I13, DOWN, buff=0.1)
        self.play(FadeIn(dot_I13), FadeIn(lbl_I13), run_time=0.4)
        self.wait(0.5)

        step2 = _ic11_step_badge("ขั้น 2: หา I_15 (pivot อีกฝั่ง, จาก I_13)", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step1, step2), run_time=0.4)
        ln_c = DashedLine(I13, I15, color=COL_OK, stroke_width=1.6)
        ln_d = DashedLine([-4.3, -1.6, 0], I15, color=COL_OK, stroke_width=1.6)
        self.play(Create(ln_c), Create(ln_d), run_time=0.6)
        dot_I15 = Dot(I15, radius=0.08, color=COL_OK)
        lbl_I15 = Text("I_15", font_size=10, color=COL_OK).next_to(dot_I15, DOWN, buff=0.1)
        self.play(FadeIn(dot_I15), FadeIn(lbl_I15), run_time=0.4)
        self.wait(0.5)

        step3 = _ic11_step_badge("ขั้น 3: หา I_35 = transfer point (Kennedy)", COL_WARN).move_to(pos_badge)
        self.play(ReplacementTransform(step2, step3), run_time=0.4)
        ln_e = DashedLine(I13, I35, color=COL_CURR, stroke_width=1.6)
        ln_f = DashedLine(I15, I35, color=COL_CURR, stroke_width=1.6)
        self.play(Create(ln_e), Create(ln_f), run_time=0.6)
        dot_I35 = Dot(I35, radius=0.09, color=COL_CURR)
        diamond_I35 = Square(side_length=0.22, color=COL_CURR, stroke_width=2.2).rotate(np.radians(45)).move_to(I35)
        # open space below-right of the dot, away from the top-right badge
        # and the up-left-going velocity arrow that will appear next beat
        # (same leader-line fix pattern as IC10's I_25 label, §29/§30)
        lbl_I35_pos = I35 + np.array([1.1, -0.55, 0.0])
        lbl_I35 = Text("I_35 (transfer point)", font_size=10.5, color=COL_CURR, weight=BOLD).move_to(lbl_I35_pos)
        leader_I35 = DashedLine(lbl_I35.get_top(), dot_I35.get_center(), color=COL_CURR, stroke_width=1.2, dash_length=0.08)
        self.play(FadeIn(dot_I35), FadeIn(diamond_I35), FadeIn(lbl_I35), Create(leader_I35), run_time=0.5)
        self.wait(1.0)

        step4 = _ic11_step_badge("ขั้น 4: สร้างรูปสามเหลี่ยมความเร็ว (ดูขั้นต่อไป)", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step3, step4), run_time=0.4)
        self.wait(1.2)

        self.play(FadeOut(m1_cap), run_time=0.4)
        self.play(*[FadeOut(m) for m in [ln_a, ln_b, ln_c, ln_d, ln_e, ln_f, step4]], run_time=0.5)
        self.wait(0.1)

        # ==================================================================
        # BEAT 19.1-30.0: Step 4 in detail — velocity triangle chain
        # ==================================================================
        cap2 = _ic11_caption_top("ขั้นที่ 4: v_A → v_I35 (ผ่าน I_13) → v_C (ผ่าน I_15)")
        fit_width(cap2, 11.6)
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)
        self.wait(0.3)

        rA_dir = (A - I13) / np.linalg.norm(A - I13)
        vA_dir = np.array([-rA_dir[1], rA_dir[0], 0.0])
        vA_arrow = Arrow(A, A + 1.0 * vA_dir, buff=0, color=COL_FORCE, stroke_width=3.6, max_tip_length_to_length_ratio=0.22)
        lbl_vA = Text("v_A (รู้ค่า)", font_size=10.5, color=COL_FORCE).next_to(vA_arrow.get_end(), vA_dir, buff=0.12)
        self.play(GrowArrow(vA_arrow), FadeIn(lbl_vA), run_time=0.6)
        self.wait(0.5)

        step_a = _ic11_step_badge("v_I35 = v_A × (r_(I35/I13) / r_(A/I13))", COL_WARN).move_to(pos_badge)
        self.play(FadeIn(step_a, shift=UP * 0.2), run_time=0.4)
        ratio1 = np.linalg.norm(I35 - I13) / np.linalg.norm(A - I13)
        rI35_dir = (I35 - I13) / np.linalg.norm(I35 - I13)
        vI35_dir = np.array([-rI35_dir[1], rI35_dir[0], 0.0])
        vI35_len = min(1.0 * ratio1, 0.55)
        vI35_arrow = Arrow(I35, I35 + vI35_len * vI35_dir, buff=0, color=COL_CURR, stroke_width=3.6, max_tip_length_to_length_ratio=0.2)
        lbl_vI35 = Text("v_I35", font_size=10.5, color=COL_CURR).next_to(vI35_arrow.get_end(), vI35_dir, buff=0.12)
        self.play(GrowArrow(vI35_arrow), FadeIn(lbl_vI35), run_time=0.6)
        self.wait(0.6)

        step_b = _ic11_step_badge("I_35 อยู่บนลิงก์ 5 ด้วย → v ถ่ายโอนข้ามลิงก์", COL_CURR).move_to(pos_badge)
        self.play(ReplacementTransform(step_a, step_b), run_time=0.4)
        self.wait(1.2)

        step_c = _ic11_step_badge("v_C = v_I35 × (r_(C/I15) / r_(I35/I15))", COL_OK).move_to(pos_badge)
        self.play(ReplacementTransform(step_b, step_c), run_time=0.4)
        ratio2 = np.linalg.norm(C - I15) / np.linalg.norm(I35 - I15)
        vC_len = min(vI35_len * ratio2, 1.3)
        # C rides a slider on a horizontal rail (prismatic joint, §IC05) —
        # its velocity must lie along the rail even though the general IC
        # rule (perpendicular to the line to the IC) is what derives its
        # magnitude here; state both explicitly so they don't look like a
        # contradiction.
        vC_arrow = Arrow(C, C + np.array([vC_len, 0.0, 0.0]), buff=0, color=COL_OK, stroke_width=4.0, max_tip_length_to_length_ratio=0.2)
        lbl_vC = Text("v_C", font_size=12, color=COL_OK, weight=BOLD).next_to(vC_arrow.get_end(), RIGHT, buff=0.12)
        self.play(GrowArrow(vC_arrow), FadeIn(lbl_vC), run_time=0.6)
        self.wait(0.6)

        rail_note = Text(
            "v_C ต้องอยู่ในแนวราง (prismatic joint) — สอดคล้องกับทิศตั้งฉากกับเส้น C–I_15 พอดี",
            font_size=10.5, color=COL_GRAY
        ).move_to([0.0, -2.55, 0.0])
        fit_width(rail_note, 11.4)
        self.play(FadeIn(rail_note, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 30.6-38.0: Method 2 summary (abbreviated, per plan scope)
        # ==================================================================
        m2_cap = _ic11_caption_top("วิธี 2: พิจารณาลิงก์ 1, 2, 6 (สรุปเร็ว — คำตอบเดียวกัน)", color=COL_FIELD)
        fit_width(m2_cap, 11.6)
        self.play(FadeIn(m2_cap, shift=UP * 0.3), run_time=0.5)
        self.wait(0.3)

        chain_items = [
            ("I_12 (pivot, revolute ตรงๆ)", COL_OK),
            ("I_26 (transfer point)", COL_CURR),
            ("I_16 ที่ ∞ (ลิงก์ 6 เคลื่อนที่เชิงเส้นล้วน → v เท่ากันทุกจุด)", COL_WARN),
        ]
        chain_mobs = VGroup()
        y0 = 0.9
        for i, (txt, col) in enumerate(chain_items):
            box = RoundedRectangle(width=8.6, height=0.5, corner_radius=0.1, color=col, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95)
            lbl = Text(txt, font_size=12, color=col)
            fit_width(lbl, 8.2)
            lbl.move_to(box.get_center())
            row = VGroup(box, lbl).move_to([0.0, y0 - i * 0.75, 0.0])
            chain_mobs.add(row)
        arrows_chain = VGroup(*[
            Arrow(chain_mobs[i].get_bottom(), chain_mobs[i + 1].get_top(), buff=0.05, color=COL_GRAY, stroke_width=2.2, max_tip_length_to_length_ratio=0.3)
            for i in range(len(chain_mobs) - 1)
        ])
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.2) for row in chain_mobs], lag_ratio=0.4), run_time=1.4)
        self.play(Create(arrows_chain), run_time=0.6)
        self.wait(1.0)

        result_note = Text("v_C = ค่าเดียวกับวิธี 1 — เพราะ C อยู่บนลิงก์ 6 เดียวกับ I_26 ทั้งหมด", font_size=11, color=COL_OK).move_to([0.0, -1.9, 0.0])
        fit_width(result_note, 11.2)
        self.play(FadeIn(result_note, shift=UP * 0.2), run_time=0.5)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 38.0-42.5: Exam-point card + callback to HW4
        # ==================================================================
        tip_box = RoundedRectangle(width=11.6, height=2.6, corner_radius=0.15, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, 0.1, 0.0])
        tip_l1 = Text("จุดออกสอบ: IC เป็นสมบัติของกลไกทั้งระบบ ไม่ขึ้นกับว่ามองผ่านลิงก์ไหน", font_size=13, color=WHITE).move_to([0.0, 0.55, 0.0])
        fit_width(tip_l1, 11.0)
        tip_l2 = Text("ทุกเส้นทางที่ถูกต้องให้คำตอบตรงกันเสมอ — ใช้ตรวจคำตอบวิธีเวกเตอร์ได้ด้วย", font_size=12, color=COL_GRAY).move_to([0.0, 0.05, 0.0])
        fit_width(tip_l2, 11.0)
        tip_l3 = Text("(โจทย์นี้ตรงกับการบ้าน 4 ที่แก้ด้วยวิธีเวกเตอร์ — ลองเทียบคำตอบดู)", font_size=11, color=COL_FIELD).move_to([0.0, -0.45, 0.0])
        fit_width(tip_l3, 11.0)
        tip_card = VGroup(tip_box, tip_l1, tip_l2, tip_l3)
        self.play(FadeIn(tip_card, shift=UP * 0.3), run_time=0.5)
        self.wait(3.2)

        self.fade_out_all(run_time=0.6)
        self.wait(0.1)

        # ==================================================================
        # BEAT 42.5-45.0: Series closing card
        # ==================================================================
        end_txt = Text("จบซีรีส์ Instant Center — W03", font_size=22, color=WHITE, weight=BOLD).move_to([0.0, 0.2, 0.0])
        end_sub = Text("Mechanics of Machinery — 11 คลิป", font_size=13, color=COL_GRAY).move_to([0.0, -0.35, 0.0])
        self.play(FadeIn(end_txt, shift=UP * 0.3), FadeIn(end_sub, shift=UP * 0.2), run_time=0.7)
        self.wait(1.8)

        self.fade_out_all(run_time=0.6)
        self.wait(0.5)
