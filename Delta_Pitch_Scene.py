"""Delta Academy 2026 Lean Canvas Pitch Video:
"Automated Closed-Loop Remanufacturing & 2nd-Life BESS Line"
Investor & Competition Pitch Flow.
"""

from manim import *
import numpy as np
from mlib import (
    SafeScene, SafeThreeDScene, fit_width, title, caption_top, page_ref,
    BG, METAL, CURRENT, FIELD, WARN, OK, ACCENT
)

def pitch_card(title_txt, q_txt, a_txt, width=11.5, height=2.8):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15,
                           fill_color=BG, fill_opacity=0.92,
                           stroke_color=OK, stroke_width=2.5)
    title_mob = Text(title_txt, font_size=20, color=OK)
    q_mob = Text(q_txt, font_size=18, color=WHITE)
    a_mob = Text(a_txt, font_size=16, color=CURRENT)
    txt = VGroup(title_mob, q_mob, a_mob).arrange(DOWN, buff=0.25)
    fit_width(txt, width - 0.6)
    txt.move_to(box.get_center())
    return VGroup(box, txt)

class Delta_Circular_Harvesting_Pitch(SafeThreeDScene):
    """Lean Canvas Investor Pitch Video for Delta Academy KMITL 2026"""

    def construct(self):
        self.set_camera_orientation(phi=55 * DEGREES, theta=-45 * DEGREES, distance=8.5)
        
        # Header
        ttl = self.hud(title("Delta Academy 2026 -- Lean Canvas: Closed-Loop Harvesting", size=22))
        pref = self.hud(page_ref("KMITL x Delta 2026 . Lean Pitch"))
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.8)

        # -------------------------------------------------------------
        # BEAT 1: PROBLEM (The 90% Waste Trap)
        # -------------------------------------------------------------
        cap1 = self.hud(caption_top(
            "1. Problem: เสียหายจริงแค่ 5-10% แต่คนขี้เกียจเช็ค -> ทิ้งของดี 90% เป็นขยะ!", color=WARN))
        self.play(FadeIn(cap1), run_time=0.6)

        # 3D Battery & Inverter Pack
        pack_box = RoundedRectangle(width=3.2, height=1.8, corner_radius=0.15,
                                    fill_color=METAL, fill_opacity=0.6,
                                    stroke_color=METAL, stroke_width=2).move_to([0, 0.2, 0])
        cell_grid = VGroup(*[
            Rectangle(width=0.6, height=0.35, fill_color=ACCENT, fill_opacity=0.8,
                      stroke_color=WHITE, stroke_width=1).move_to([x, y, 0])
            for x in np.linspace(-1.0, 1.0, 4)
            for y in np.linspace(-0.5, 0.5, 3)
        ]).move_to([0, 0.2, 0])
        
        hud_box = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.1,
                                   fill_color=BG, fill_opacity=0.85,
                                   stroke_color=CURRENT, stroke_width=1.5).move_to([3.6, 1.2, 0])
        hud_txt = VGroup(
            Text("จุดเสีย: คาปาซิเตอร์แห้ง 1 ตัว (5%)", font_size=15, color=WARN),
            Text("ชิ้นส่วนที่ยังสมบูรณ์: 90% (ทิ้งสูญเปล่า)", font_size=15, color=OK),
            Text("วิธีตรวจเดิม: ช้า เสี่ยงไฟ 800V", font_size=15, color=WARN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(hud_box.get_center())
        hud_group = VGroup(hud_box, hud_txt)
        self.hud(hud_group)

        self.play(FadeIn(pack_box), FadeIn(cell_grid), FadeIn(hud_group), run_time=1.0)
        self.wait(1.6)

        # -------------------------------------------------------------
        # BEAT 2: SOLUTION & UNIQUE VALUE PROP (4-Device Automation)
        # -------------------------------------------------------------
        self.play(FadeOut(cap1), run_time=0.3)
        cap2 = self.hud(caption_top(
            "2. Solution: ระบบ 4-Device อัตโนมัติ สแกน-ถอด-วัด SOH ใน 5 วิ ปลอดภัย 100%", color=CURRENT))
        self.play(FadeIn(cap2), run_time=0.6)

        # Scanning Line
        scan_line = Line([-2.0, 0.2, 0], [2.0, 0.2, 0], color=CURRENT, stroke_width=4)
        self.play(scan_line.animate.shift(UP * 0.9), run_time=0.6)
        self.play(scan_line.animate.shift(DOWN * 1.8), run_time=0.6)
        self.play(FadeOut(scan_line), run_time=0.2)

        # 4 Device Badges
        dev_badges = VGroup(
            VGroup(Square(0.3, fill_color=CURRENT, fill_opacity=0.9), Text("Vision (DMV2000)", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=OK, fill_opacity=0.9), Text("Servo (ASD-A3)", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=FIELD, fill_opacity=0.9), Text("PLC (AS320T)", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=WARN, fill_opacity=0.9), Text("VFD (MS300)", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.4).move_to([0, -1.8, 0])
        fit_width(dev_badges, 11.5)
        self.hud(dev_badges)
        self.play(FadeIn(dev_badges), run_time=0.8)
        self.wait(1.5)

        # Clear 3D objects
        self.play(FadeOut(pack_box), FadeOut(cell_grid), FadeOut(hud_group),
                  FadeOut(dev_badges), FadeOut(cap2), run_time=0.6)

        # -------------------------------------------------------------
        # BEAT 3: REVENUE STREAMS & CUSTOMER SEGMENTS
        # -------------------------------------------------------------
        cap3 = self.hud(caption_top(
            "3. Revenue Streams: 3 ช่องทางสร้างกำไรใหม่จากของที่เคยถูกทิ้ง", color=OK))
        self.play(FadeIn(cap3), run_time=0.6)

        rev_card1 = VGroup(
            RoundedRectangle(width=3.6, height=3.0, corner_radius=0.15,
                             fill_color=BG, fill_opacity=0.9, stroke_color=OK, stroke_width=2),
            VGroup(
                Text("เกรด A: Delta BESS", font_size=18, color=OK),
                Text("• ลูกค้า: อาคารเขียว / โซลาร์ฟาร์ม", font_size=14, color=WHITE),
                Text("• ประกอบเป็นชุดกักเก็บพลังงาน", font_size=14, color=WHITE),
                Text("• กำไร 200,000-400,000 บ./ลูก", font_size=14, color=OK),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 0, 0])
        )
        rev_card1.move_to([-4.0, -0.4, 0])

        rev_card2 = VGroup(
            RoundedRectangle(width=3.6, height=3.0, corner_radius=0.15,
                             fill_color=BG, fill_opacity=0.9, stroke_color=CURRENT, stroke_width=2),
            VGroup(
                Text("เกรด B: Spare Parts", font_size=18, color=CURRENT),
                Text("• ลูกค้า: โรงงาน Predictive Maint.", font_size=14, color=WHITE),
                Text("• สแตนด์บายอะไหล่ Zero Downtime", font_size=14, color=WHITE),
                Text("• ลดต้นทุนอะไหล่ 50% (Win-Win)", font_size=14, color=CURRENT),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 0, 0])
        )
        rev_card2.move_to([0, -0.4, 0])

        rev_card3 = VGroup(
            RoundedRectangle(width=3.6, height=3.0, corner_radius=0.15,
                             fill_color=BG, fill_opacity=0.9, stroke_color=WARN, stroke_width=2),
            VGroup(
                Text("เกรด C: สกัดแร่บริสุทธิ์", font_size=18, color=WARN),
                Text("• ลูกค้า: โรงหลอมแร่ / รีไซเคิล", font_size=14, color=WHITE),
                Text("• สกัดทองแดง 100% + แม่เหล็ก NdFeB", font_size=14, color=WHITE),
                Text("• ขายราคาสูงกว่าเศษเหล็ก 3 เท่า", font_size=14, color=WARN),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 0, 0])
        )
        rev_card3.move_to([4.0, -0.4, 0])

        all_cards = VGroup(rev_card1, rev_card2, rev_card3)
        fit_width(all_cards, 12.0)
        self.hud(all_cards)

        self.play(FadeIn(rev_card1, shift=UP*0.2),
                  FadeIn(rev_card2, shift=UP*0.2),
                  FadeIn(rev_card3, shift=UP*0.2), run_time=1.1)
        self.wait(2.2)

        # -------------------------------------------------------------
        # BEAT 4: KEY METRICS & INVESTOR ROI
        # -------------------------------------------------------------
        self.play(FadeOut(all_cards), FadeOut(cap3), run_time=0.4)
        cap4 = self.hud(caption_top(
            "4. Key Metrics & ROI: คืนทุนไวใน 0.96 ปี และเพิ่ม Throughput 1,400%", color=OK))
        self.play(FadeIn(cap4), run_time=0.6)

        roi_box = VGroup(
            MathTex(r"\text{CAPEX (Automation Line)} \approx 1{,}200{,}000\ \text{THB}", font_size=28, color=WHITE),
            MathTex(r"\text{Annual Revenue (BESS + Parts + Cu)} \approx 1{,}500{,}000\ \text{THB/Year}", font_size=28, color=OK),
            MathTex(r"\text{Payback Period} = \frac{1{,}200{,}000}{1{,}500{,}000} \approx \mathbf{0.96\ \text{Years}}\quad (\mathbf{\text{ROI } 125\%})", font_size=32, color=OK),
            MathTex(r"\text{Testing Time: } 45\ \text{min} \to \mathbf{3\ \text{min/pack}}\quad (\mathbf{+1{,}400\%\ \text{Throughput}})", font_size=28, color=CURRENT)
        ).arrange(DOWN, buff=0.30).move_to([0, 0.35, 0])
        fit_width(roi_box, 11.2)
        self.hud(roi_box)
        self.play(FadeIn(roi_box), run_time=1.0)
        self.wait(2.2)

        # Final pitch card
        self.fade_out_all(run_time=0.7)
        card = pitch_card(
            "Delta Academy 2026: Closed-Loop Harvesting Ecosystem",
            "เปลี่ยน 90% Waste ให้เป็น 3 New Revenue Streams ตอบโจทย์ Net Zero",
            "คืนทุนเร็วภายใน 0.96 ปี (ROI 125%) พร้อมผลักดันอุตสาหกรรมสู่อนาคต")
        self.hud(card)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(2.2)
