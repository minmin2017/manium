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
STATUS_WARN  = "#FFA726"   # Orange status (verifying)
STATUS_OK    = "#00E676"   # Bright green (confirmed)
CARD_BG      = "#212121"   # Dark card background


class BoosterLandingVerification(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # 1. Header & Establishing Descent (0 - 6s)
        # ----------------------------------------------------------------------
        pref = page_ref("Illustrative Verification Model")
        ttl = title("Booster Landing Verification", size=24)
        cap1 = caption_top("ขาแตะพื้นแล้ว แปลว่าลงจอดสำเร็จเลยไหม? (Touchdown != Confirmed)")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # Ground Pad at bottom y = -2.6
        pad_line = Line([-6.5, -2.6, 0], [6.5, -2.6, 0], color=PAD_COLOR, stroke_width=4)
        pad_target = Circle(radius=0.65, color=PAD_COLOR, stroke_width=2).move_to([-3.5, -2.6, 0])
        pad_target.stretch(0.25, dim=1)  # perspective ellipse
        pad_x = Text("X", font_size=18, color=GRAYTXT).move_to([-3.5, -2.6, 0])
        pad_grp = VGroup(pad_line, pad_target, pad_x)

        # 2D Booster Model at Left (x = -3.5)
        body = RoundedRectangle(width=0.72, height=3.0, corner_radius=0.12, color=WHITE, fill_color=BOOSTER_BODY, fill_opacity=0.95, stroke_width=2)
        nose = Polygon([-0.36, 1.5, 0], [0.36, 1.5, 0], [0, 1.95, 0], color=WHITE, fill_color=BOOSTER_BODY, fill_opacity=0.95, stroke_width=2)
        
        # Grid fins
        fin_l = Rectangle(width=0.28, height=0.14, color=WHITE, fill_color=METAL, fill_opacity=0.8, stroke_width=1.5).move_to([-0.45, 1.30, 0])
        fin_r = Rectangle(width=0.28, height=0.14, color=WHITE, fill_color=METAL, fill_opacity=0.8, stroke_width=1.5).move_to([0.45, 1.30, 0])

        # Engine nozzle at base
        engine_nozzle = Polygon([-0.22, -1.5, 0], [0.22, -1.5, 0], [0.28, -1.75, 0], [-0.28, -1.75, 0], color=METAL, fill_color=METAL, fill_opacity=0.9, stroke_width=1.5)

        # 4 Landing Legs (2 visible in 2D profile)
        leg_l = Line([-0.32, -1.4, 0], [-0.85, -2.0, 0], color=METAL, stroke_width=4)
        foot_l = Line([-0.95, -2.0, 0], [-0.75, -2.0, 0], color=WHITE, stroke_width=3)
        leg_r = Line([0.32, -1.4, 0], [0.85, -2.0, 0], color=METAL, stroke_width=4)
        foot_r = Line([0.75, -2.0, 0], [0.95, -2.0, 0], color=WHITE, stroke_width=3)

        # Active Engine Flame
        plume_outer = Polygon([-0.26, -1.75, 0], [0.26, -1.75, 0], [0, -2.55, 0], color=PLUME_OUTER, fill_color=PLUME_OUTER, fill_opacity=0.85, stroke_width=0)
        plume_core = Polygon([-0.14, -1.75, 0], [0.14, -1.75, 0], [0, -2.35, 0], color=PLUME_CORE, fill_color=PLUME_CORE, fill_opacity=0.95, stroke_width=0)
        flame_grp = VGroup(plume_outer, plume_core)

        booster = VGroup(
            body, nose, fin_l, fin_r, engine_nozzle,
            leg_l, foot_l, leg_r, foot_r, flame_grp
        ).move_to([-3.5, 0.4, 0])

        # Initial Status Badge (Top Right x = 3.5, y = 2.15)
        badge_box = RoundedRectangle(width=5.8, height=0.62, corner_radius=0.10, color=STATUS_WARN, fill_color=BLACK, fill_opacity=0.75, stroke_width=2).move_to([3.5, 2.15, 0])
        badge_txt = Text("STATUS: TOUCHDOWN VERIFYING", font_size=15, color=STATUS_WARN).move_to(badge_box.get_center())
        status_badge = VGroup(badge_box, badge_txt)

        self.play(FadeIn(pad_grp), FadeIn(status_badge), run_time=0.6)

        # Descent Animation: Rocket drops from y = 0.4 to resting y = -0.6
        # When resting, foot_l and foot_r hit y = -2.6 exactly
        self.play(
            booster.animate.shift(DOWN * 1.0),
            run_time=2.2,
            rate_func=slow_into
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # 2. Freeze-Frame / Physical Sensor Callouts (6 - 11s)
        # ----------------------------------------------------------------------
        cap2 = caption_top("คอมพิวเตอร์การบินตรวจเช็ก 4 เซนเซอร์หลัก (Illustrative Sensor Model)")
        self.play(ReplacementTransform(cap1, cap2), run_time=0.4)

        # Pointers to 4 sensor areas on frozen booster
        # Sensor 1: Radar/Lidar Altimeter at base
        ptr_alt = Arrow([-2.0, -2.1, 0], [-3.15, -2.1, 0], color=FIELD, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        lbl_s_alt = Text("Altimeter / Lidar", font_size=12, color=FIELD).next_to(ptr_alt, RIGHT, buff=0.08)

        # Sensor 2: IMU / Gyro in Core
        ptr_imu = Arrow([-2.0, -0.4, 0], [-3.05, -0.4, 0], color=TORQUE, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        lbl_s_imu = Text("IMU (มุมเอียง/หมุน)", font_size=12, color=TORQUE).next_to(ptr_imu, RIGHT, buff=0.08)

        # Sensor 3: Leg Load Switches
        ptr_leg = Arrow([-2.0, -1.4, 0], [-2.65, -2.4, 0], color=CURRENT, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        lbl_s_leg = Text("Leg Load (น้ำหนักกดขา)", font_size=12, color=CURRENT).next_to(ptr_leg, RIGHT, buff=0.08)

        # Sensor 4: Engine State at Base
        ptr_eng = Arrow([-2.0, -1.85, 0], [-3.25, -2.25, 0], color=WARN, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        lbl_s_eng = Text("Chamber Pressure (เครื่องยนต์)", font_size=12, color=WARN).next_to(ptr_eng, RIGHT, buff=0.08)

        sensor_ptrs = VGroup(
            ptr_alt, lbl_s_alt, ptr_imu, lbl_s_imu,
            ptr_leg, lbl_s_leg, ptr_eng, lbl_s_eng
        )

        self.play(FadeIn(sensor_ptrs), run_time=1.0)
        self.wait(2.2)

        # ----------------------------------------------------------------------
        # 3. Four Synchronized Interlock Gates (11 - 31s)
        # ----------------------------------------------------------------------
        self.play(FadeOut(sensor_ptrs), run_time=0.4)

        # Build 4 Dashboard Cards on Right (x = 3.5, stacked at y = 1.35, 0.50, -0.35, -1.20)
        def make_card(y_pos, title_str, metric_str):
            bg = RoundedRectangle(width=5.8, height=0.72, corner_radius=0.10, color=GRAYTXT, fill_color=CARD_BG, fill_opacity=0.85, stroke_width=1.5).move_to([3.5, y_pos, 0])
            t_title = Text(title_str, font_size=13, color=WHITE).move_to([1.8, y_pos + 0.15, 0])
            t_metric = Text(metric_str, font_size=12, color=GRAYTXT).move_to([1.8, y_pos - 0.15, 0])
            stat_box = RoundedRectangle(width=1.3, height=0.45, corner_radius=0.08, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.6, stroke_width=1).move_to([5.6, y_pos, 0])
            stat_txt = Text("WAIT", font_size=11, color=GRAYTXT).move_to(stat_box.get_center())
            return VGroup(bg, t_title, t_metric, stat_box, stat_txt)

        c1 = make_card(1.35, "1. Vertical Speed (ความเร็วแนวดิ่ง)", "Target: vz -> 0.0 m/s")
        c2 = make_card(0.50, "2. Attitude Tilt (ความตั้งตรง)", "Target: Tilt theta < 2°")
        c3 = make_card(-0.35, "3. Weight-on-Legs (ขารับน้ำหนัก)", "Target: 4/4 Legs Loaded")
        c4 = make_card(-1.20, "4. Engine Cutoff (ดับเครื่องยนต์)", "Target: Thrust -> 0 / Cutoff")

        dash_cards = VGroup(c1, c2, c3, c4)
        self.play(FadeIn(dash_cards), run_time=1.0)
        self.wait(0.5)

        # BEAT 1: Gate 1 - Vertical Speed
        cap3 = caption_top("เกณฑ์ที่ 1: ความเร็วแนวดิ่งลดลงแตะ 0 m/s (วัดด้วย Altimeter/Lidar)")
        beam_v = DashedLine([-3.5, -2.25, 0], [-3.5, -2.6, 0], color=STATUS_OK, stroke_width=3)

        self.play(
            ReplacementTransform(cap2, cap3),
            Create(beam_v),
            c1[0].animate.set_color(STATUS_OK),
            c1[2].animate.become(Text("vz = 0.0 m/s [SAFE]", font_size=12, color=STATUS_OK).move_to([1.8, 1.35 - 0.15, 0])),
            c1[3].animate.set_color(STATUS_OK),
            c1[4].animate.become(Text("PASS", font_size=12, color=STATUS_OK).move_to(c1[3].get_center())),
            run_time=1.2
        )
        self.wait(1.5)

        # BEAT 2: Gate 2 - Attitude Tilt
        cap4 = caption_top("เกณฑ์ที่ 2: ลำตัวจรวดตั้งตรง ไม่เอียงเสี่ยงคว่ำ (Tilt < 2° ตรวจด้วย IMU)")
        cone_l = Line([-3.5, 0.4, 0], [-3.75, -2.55, 0], color=STATUS_OK, stroke_width=1.5)
        cone_r = Line([-3.5, 0.4, 0], [-3.25, -2.55, 0], color=STATUS_OK, stroke_width=1.5)
        safe_cone = VGroup(cone_l, cone_r)

        self.play(
            ReplacementTransform(cap3, cap4),
            FadeIn(safe_cone),
            c2[0].animate.set_color(STATUS_OK),
            c2[2].animate.become(Text("Tilt = 0.4° [UPRIGHT]", font_size=12, color=STATUS_OK).move_to([1.8, 0.50 - 0.15, 0])),
            c2[3].animate.set_color(STATUS_OK),
            c2[4].animate.become(Text("PASS", font_size=12, color=STATUS_OK).move_to(c2[3].get_center())),
            run_time=1.2
        )
        self.wait(1.5)

        # BEAT 3: Gate 3 - Weight on Legs
        cap5 = caption_top("เกณฑ์ที่ 3: ขาลงจอดทั้ง 4 ด้านรับน้ำหนักจรวดจริง ไม่ใช่แค่เฉียดสัมผัส")
        arr_load_l = Arrow([-4.35, -2.6, 0], [-4.35, -2.0, 0], color=STATUS_OK, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        arr_load_r = Arrow([-2.65, -2.6, 0], [-2.65, -2.0, 0], color=STATUS_OK, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        load_arrows = VGroup(arr_load_l, arr_load_r)

        self.play(
            ReplacementTransform(cap4, cap5),
            FadeIn(load_arrows),
            c3[0].animate.set_color(STATUS_OK),
            c3[2].animate.become(Text("Load = 100% Booster Weight", font_size=12, color=STATUS_OK).move_to([1.8, -0.35 - 0.15, 0])),
            c3[3].animate.set_color(STATUS_OK),
            c3[4].animate.become(Text("PASS", font_size=12, color=STATUS_OK).move_to(c3[3].get_center())),
            run_time=1.2
        )
        self.wait(1.5)

        # BEAT 4: Gate 4 - Engine Cutoff (Flame extinguishes at the EXACT same instant)
        cap6 = caption_top("เกณฑ์ที่ 4: สั่งดับเครื่องยนต์ทันที เพื่อไม่ให้แรงขับดันจรวดลอยซ้ำหรือดีดตัว")
        
        self.play(
            ReplacementTransform(cap5, cap6),
            # Physical evidence: flame disappears
            FadeOut(flame_grp),
            # Dashboard evidence: card turns green and indicates engine shutdown
            c4[0].animate.set_color(STATUS_OK),
            c4[2].animate.become(Text("Thrust = 0 kN [CUTOFF]", font_size=12, color=STATUS_OK).move_to([1.8, -1.20 - 0.15, 0])),
            c4[3].animate.set_color(STATUS_OK),
            c4[4].animate.become(Text("PASS", font_size=12, color=STATUS_OK).move_to(c4[3].get_center())),
            run_time=1.0
        )
        self.wait(1.8)

        # ----------------------------------------------------------------------
        # 4. AND-Gate Resolution & Landing Confirmed (31 - 40s)
        # ----------------------------------------------------------------------
        cap7 = caption_top("รวม 4 สัญญาณผ่าน Logic Gate -> คอมพิวเตอร์จึงยืนยันการลงจอดสำเร็จ")
        self.play(
            ReplacementTransform(cap6, cap7),
            FadeOut(beam_v), FadeOut(safe_cone), FadeOut(load_arrows),
            run_time=0.5
        )

        # Animated Logic Lines connecting all 4 cards to the top status badge
        lines_and = VGroup(
            Line([5.6, 1.35, 0], [5.6, 2.15, 0], color=STATUS_OK, stroke_width=2),
            Line([5.6, 0.50, 0], [5.6, 2.15, 0], color=STATUS_OK, stroke_width=2),
            Line([5.6, -0.35, 0], [5.6, 2.15, 0], color=STATUS_OK, stroke_width=2),
            Line([5.6, -1.20, 0], [5.6, 2.15, 0], color=STATUS_OK, stroke_width=2)
        )

        self.play(Create(lines_and), run_time=0.8)

        # Status Badge transitions to LANDING CONFIRMED (Solid Green)
        badge_box_ok = RoundedRectangle(width=5.8, height=0.62, corner_radius=0.10, color=STATUS_OK, fill_color=BLACK, fill_opacity=0.85, stroke_width=2.5).move_to([3.5, 2.15, 0])
        badge_txt_ok = Text("STATUS: LANDING CONFIRMED", font_size=15, color=STATUS_OK).move_to(badge_box_ok.get_center())
        status_ok = VGroup(badge_box_ok, badge_txt_ok)

        self.play(
            ReplacementTransform(status_badge, status_ok),
            Flash(badge_box_ok, color=STATUS_OK, flash_radius=0.4),
            FadeOut(lines_and),
            run_time=1.0
        )
        self.wait(2.2)

        # ----------------------------------------------------------------------
        # 5. Compact Close: Rule Summary (40 - 45s)
        # ----------------------------------------------------------------------
        cap8 = caption_top("สรุปหัวใจวิศวกรรม: แตะพื้น != ลงจอดยืนยัน (ต้องครบ 4 เงื่อนไขในระบบจริง)")
        self.play(
            ReplacementTransform(cap7, cap8),
            FadeOut(dash_cards),
            FadeOut(status_ok),
            run_time=0.6
        )

        # 4-Item Chain Summary Card on Right
        sum_box = RoundedRectangle(width=6.0, height=2.8, corner_radius=0.12, color=STATUS_OK, fill_color=BLACK, fill_opacity=0.7, stroke_width=1.8).move_to([3.5, -0.2, 0])
        
        s_title = Text("4 เงื่อนไขยืนยันความปลอดภัย", font_size=15, color=STATUS_OK).move_to([3.5, 0.85, 0])
        s_line1 = Text("1. ความเร็วแนวดิ่งเป็นศูนย์ (vz = 0)", font_size=13, color=WHITE).move_to([3.5, 0.40, 0])
        s_line2 = Text("2. ลำตัวจรวดตั้งตรงเสถียร (Tilt < 2°)", font_size=13, color=WHITE).move_to([3.5, 0.05, 0])
        s_line3 = Text("3. ขารับน้ำหนักเต็มพิกัด (Weight-on-Legs)", font_size=13, color=WHITE).move_to([3.5, -0.30, 0])
        s_line4 = Text("4. ดับเครื่องยนต์ตัดแรงขับ (Thrust = 0)", font_size=13, color=WHITE).move_to([3.5, -0.65, 0])
        s_note  = Text("หมายเหตุ: ระบบการบินจริงมี Redundancy ตรวจซ้ำซ้อนเพื่อความปลอดภัย", font_size=11, color=GRAYTXT).move_to([3.5, -1.15, 0])

        sum_grp = VGroup(sum_box, s_title, s_line1, s_line2, s_line3, s_line4, s_note)

        self.play(FadeIn(sum_grp), run_time=1.0)
        self.wait(3.5)

        self.fade_out_all(run_time=0.8)
