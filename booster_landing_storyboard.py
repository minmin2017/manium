import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Color palette
BOOSTER_BODY = "#ECEFF1"   # Clean white/silver booster body
PAD_COLOR    = "#546E7A"   # Ground / droneship pad
PLUME_CORE   = "#FFF176"   # Yellow core of flame
PLUME_OUTER  = "#FF7043"   # Orange outer exhaust
STATUS_WARN  = "#FFA726"   # Orange status
STATUS_OK    = "#00E676"   # Bright green
CARD_BG      = "#212121"   # Dark card background


class BoosterLandingStoryboard(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # Header & Navigation
        # ----------------------------------------------------------------------
        pref = page_ref("Storyboard-First Model")
        ttl = title("Booster Landing: Storyboard-First", size=24)
        cap1 = caption_top("เหตุการณ์จริง: บูสเตอร์ร่อนลง แตะพื้น ดับเครื่อง แล้วตั้งนิ่งบนฐาน")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # Ground Pad at Center bottom y = -2.6
        pad_line = Line([-6.5, -2.6, 0], [6.5, -2.6, 0], color=PAD_COLOR, stroke_width=4)
        pad_target = Circle(radius=0.75, color=PAD_COLOR, stroke_width=2).move_to([0, -2.6, 0])
        pad_target.stretch(0.25, dim=1)
        pad_x = Text("X", font_size=18, color=GRAYTXT).move_to([0, -2.6, 0])
        pad_grp = VGroup(pad_line, pad_target, pad_x)

        # Full 2D Booster Model at Center (x = 0)
        body = RoundedRectangle(width=0.75, height=3.0, corner_radius=0.12, color=WHITE, fill_color=BOOSTER_BODY, fill_opacity=0.95, stroke_width=2)
        nose = Polygon([-0.375, 1.5, 0], [0.375, 1.5, 0], [0, 1.95, 0], color=WHITE, fill_color=BOOSTER_BODY, fill_opacity=0.95, stroke_width=2)
        
        fin_l = Rectangle(width=0.28, height=0.14, color=WHITE, fill_color=METAL, fill_opacity=0.8, stroke_width=1.5).move_to([-0.48, 1.30, 0])
        fin_r = Rectangle(width=0.28, height=0.14, color=WHITE, fill_color=METAL, fill_opacity=0.8, stroke_width=1.5).move_to([0.48, 1.30, 0])
        engine_nozzle = Polygon([-0.24, -1.5, 0], [0.24, -1.5, 0], [0.30, -1.75, 0], [-0.30, -1.75, 0], color=METAL, fill_color=METAL, fill_opacity=0.9, stroke_width=1.5)

        leg_l = Line([-0.34, -1.4, 0], [-0.90, -2.0, 0], color=METAL, stroke_width=4)
        foot_l = Line([-1.00, -2.0, 0], [-0.80, -2.0, 0], color=WHITE, stroke_width=3)
        leg_r = Line([0.34, -1.4, 0], [0.90, -2.0, 0], color=METAL, stroke_width=4)
        foot_r = Line([0.80, -2.0, 0], [1.00, -2.0, 0], color=WHITE, stroke_width=3)

        plume_outer = Polygon([-0.28, -1.75, 0], [0.28, -1.75, 0], [0, -2.60, 0], color=PLUME_OUTER, fill_color=PLUME_OUTER, fill_opacity=0.85, stroke_width=0)
        plume_core = Polygon([-0.15, -1.75, 0], [0.15, -1.75, 0], [0, -2.38, 0], color=PLUME_CORE, fill_color=PLUME_CORE, fill_opacity=0.95, stroke_width=0)
        flame_grp = VGroup(plume_outer, plume_core)

        booster = VGroup(
            body, nose, fin_l, fin_r, engine_nozzle,
            leg_l, foot_l, leg_r, foot_r, flame_grp
        ).move_to([0, 0.4, 0])

        self.play(FadeIn(pad_grp), FadeIn(booster), run_time=0.6)

        # ----------------------------------------------------------------------
        # Phase 1: Full Cinematic Landing Event (0 - 10s)
        # ----------------------------------------------------------------------
        # Booster descends smoothly, touches down, and flame extinguishes
        self.play(
            booster.animate.shift(DOWN * 1.0),
            run_time=2.8,
            rate_func=slow_into
        )

        # Plume cuts off right at landing
        self.play(FadeOut(flame_grp), run_time=0.4)
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # Phase 2: Freeze & Replay with Sensor Callouts (10 - 26s)
        # ----------------------------------------------------------------------
        cap2 = caption_top("เบื้องหลังเหตุการณ์: คอมพิวเตอร์การบินตรวจเช็ก 4 ข้อมูลทางฟิสิกส์")
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)

        # Freeze indicator frame
        freeze_border = SurroundingRectangle(booster, color=FIELD, stroke_width=2, buff=0.15)
        freeze_tag = Text("FREEZE-FRAME ANALYSIS", font_size=12, color=FIELD).next_to(freeze_border, UP, buff=0.08)
        self.play(Create(freeze_border), FadeIn(freeze_tag), run_time=0.6)

        # Callout 1: Altimeter & Vertical Velocity (Bottom Left)
        ptr1 = Arrow([-2.4, -1.8, 0], [-0.5, -2.1, 0], color=STATUS_OK, buff=0, stroke_width=2.5)
        card1 = VGroup(
            RoundedRectangle(width=3.6, height=0.7, corner_radius=0.08, color=STATUS_OK, fill_color=CARD_BG, fill_opacity=0.9),
            Text("1. ความเร็วแนวดิ่ง: vz -> 0 m/s", font_size=12, color=WHITE),
            Text("[PASS] ตรวจด้วย Altimeter/Lidar", font_size=11, color=STATUS_OK)
        ).arrange(DOWN, buff=0.04).move_to([-3.8, -1.8, 0])

        self.play(Create(ptr1), FadeIn(card1), run_time=0.8)
        self.wait(1.2)

        # Callout 2: IMU Tilt (Top Left)
        ptr2 = Arrow([-2.4, 0.2, 0], [-0.4, 0.0, 0], color=STATUS_OK, buff=0, stroke_width=2.5)
        card2 = VGroup(
            RoundedRectangle(width=3.6, height=0.7, corner_radius=0.08, color=STATUS_OK, fill_color=CARD_BG, fill_opacity=0.9),
            Text("2. ลำตัวตั้งตรง: Tilt < 2°", font_size=12, color=WHITE),
            Text("[PASS] ตรวจด้วย IMU/Gyros", font_size=11, color=STATUS_OK)
        ).arrange(DOWN, buff=0.04).move_to([-3.8, 0.2, 0])

        self.play(Create(ptr2), FadeIn(card2), run_time=0.8)
        self.wait(1.2)

        # Callout 3: Leg Load (Bottom Right)
        ptr3 = Arrow([2.4, -1.8, 0], [0.9, -2.3, 0], color=STATUS_OK, buff=0, stroke_width=2.5)
        card3 = VGroup(
            RoundedRectangle(width=3.6, height=0.7, corner_radius=0.08, color=STATUS_OK, fill_color=CARD_BG, fill_opacity=0.9),
            Text("3. ขารับน้ำหนัก: Load = 100%", font_size=12, color=WHITE),
            Text("[PASS] ขาทั้ง 4 ด้านรับน้ำหนักจริง", font_size=11, color=STATUS_OK)
        ).arrange(DOWN, buff=0.04).move_to([3.8, -1.8, 0])

        self.play(Create(ptr3), FadeIn(card3), run_time=0.8)
        self.wait(1.2)

        # Callout 4: Engine Cutoff (Top Right)
        ptr4 = Arrow([2.4, -0.6, 0], [0.4, -1.4, 0], color=STATUS_OK, buff=0, stroke_width=2.5)
        card4 = VGroup(
            RoundedRectangle(width=3.6, height=0.7, corner_radius=0.08, color=STATUS_OK, fill_color=CARD_BG, fill_opacity=0.9),
            Text("4. ดับเครื่องยนต์: Thrust = 0", font_size=12, color=WHITE),
            Text("[PASS] แรงดันห้องเผาไหม้เป็นศูนย์", font_size=11, color=STATUS_OK)
        ).arrange(DOWN, buff=0.04).move_to([3.8, -0.6, 0])

        self.play(Create(ptr4), FadeIn(card4), run_time=0.8)
        self.wait(2.0)

        # ----------------------------------------------------------------------
        # Phase 3: Resolution & Final Payoff (26 - 36s)
        # ----------------------------------------------------------------------
        cap3 = caption_top("เมื่อข้อมูลทั้ง 4 จุดผ่านเกณฑ์พร้อมกัน -> ยืนยันการลงจอดสมบูรณ์!")
        self.play(
            ReplacementTransform(cap2, cap3),
            FadeOut(ptr1), FadeOut(card1),
            FadeOut(ptr2), FadeOut(card2),
            FadeOut(ptr3), FadeOut(card3),
            FadeOut(ptr4), FadeOut(card4),
            FadeOut(freeze_border), FadeOut(freeze_tag),
            run_time=0.8
        )

        # Big Confirmed Badge at Top
        badge_box = RoundedRectangle(width=7.2, height=0.85, corner_radius=0.12, color=STATUS_OK, fill_color=BLACK, fill_opacity=0.85, stroke_width=2.5).move_to([0, 1.4, 0])
        badge_txt = Text("STATUS: LANDING CONFIRMED", font_size=19, color=STATUS_OK).move_to(badge_box.get_center())
        conf_badge = VGroup(badge_box, badge_txt)

        self.play(FadeIn(conf_badge), Flash(badge_box, color=STATUS_OK, flash_radius=0.5), run_time=1.0)
        self.wait(2.5)

        # Compact Close Note
        rule_note = Text("Storyboard-First: สื่อสารเหตุการณ์เชิงประจักษ์ก่อน แล้วจึงอธิบายระบบเบื้องหลัง", font_size=13, color=GRAYTXT).move_to([0, -1.8, 0])
        sub_note = Text("(Illustrative Model · ระบบจริงมี Redundancy เซนเซอร์ตรวจซ้ำซ้อนหลายชุด)", font_size=11, color=GRAYTXT).next_to(rule_note, DOWN, buff=0.08)
        
        self.play(FadeIn(rule_note), FadeIn(sub_note), run_time=0.8)
        self.wait(3.0)

        self.fade_out_all(run_time=0.8)
