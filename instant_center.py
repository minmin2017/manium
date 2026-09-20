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
