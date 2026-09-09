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
GHOST_WARN   = "#FF5722"   # Red-orange risk


class BoosterLandingScriptFirst(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # Header & Script Question (0 - 8s)
        # ----------------------------------------------------------------------
        pref = page_ref("Script-First Model")
        ttl = title("Booster Landing: Script-First", size=24)
        cap1 = caption_top("คำถามหลัก: ขาแตะพื้น = ลงจอดสำเร็จแล้วไหม? (Contact != Confirmed)")

        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap1), run_time=0.8)

        # Counterexample visual: Rocket touching pad but tipping over / bouncing
        pad_mini = Line([-2.5, -0.6, 0], [2.5, -0.6, 0], color=PAD_COLOR, stroke_width=3)
        danger_rocket = RoundedRectangle(width=0.6, height=2.2, corner_radius=0.10, color=GHOST_WARN, fill_color=GHOST_WARN, fill_opacity=0.3, stroke_width=2).rotate(18 * DEGREES).move_to([0, 0.4, 0])
        danger_plume = Polygon([-0.18, -0.8, 0], [0.18, -0.8, 0], [0, -1.3, 0], color=PLUME_OUTER, fill_color=PLUME_OUTER, fill_opacity=0.8).rotate(18 * DEGREES, about_point=[0, 0.4, 0])
        danger_txt = Text("หากแตะพื้นแต่ไม่ดับเครื่อง หรือขารับน้ำหนักไม่จริง -> เสี่ยงคว่ำทันที!", font_size=13, color=GHOST_WARN).move_to([0, 1.8, 0])
        danger_grp = VGroup(pad_mini, danger_rocket, danger_plume, danger_txt)

        self.play(FadeIn(danger_grp), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(danger_grp), run_time=0.5)

        # ----------------------------------------------------------------------
        # Prove Each Statement (8 - 26s)
        # ----------------------------------------------------------------------
        # 4 Statement Cards stacked vertically at Center
        def make_stmt_card(y_pos, num_str, text_str):
            bg = RoundedRectangle(width=8.2, height=0.72, corner_radius=0.10, color=GRAYTXT, fill_color=CARD_BG, fill_opacity=0.85, stroke_width=1.5).move_to([0, y_pos, 0])
            t_num = Text(num_str, font_size=14, color=WHITE).move_to([-3.2, y_pos, 0])
            t_main = Text(text_str, font_size=13, color=GRAYTXT).move_to([0.2, y_pos, 0])
            stat_box = RoundedRectangle(width=1.3, height=0.45, corner_radius=0.08, color=GRAYTXT, fill_color=BLACK, fill_opacity=0.6, stroke_width=1).move_to([3.4, y_pos, 0])
            stat_txt = Text("WAIT", font_size=11, color=GRAYTXT).move_to(stat_box.get_center())
            return VGroup(bg, t_num, t_main, stat_box, stat_txt)

        card1 = make_stmt_card(1.35, "ประโยคที่ 1:", "ความเร็วแนวดิ่งต้องชะลอจนหยุดนิ่ง (vz -> 0 m/s)")
        card2 = make_stmt_card(0.45, "ประโยคที่ 2:", "ลำตัวจรวดต้องตั้งตรงเสถียร (Tilt theta < 2°)")
        card3 = make_stmt_card(-0.45, "ประโยคที่ 3:", "ขาทั้ง 4 ด้านต้องรับน้ำหนักจริง (Weight-on-Legs)")
        card4 = make_stmt_card(-1.35, "ประโยคที่ 4:", "เครื่องยนต์ต้องดับสนิททันที (Thrust -> 0)")

        cards_grp = VGroup(card1, card2, card3, card4)
        self.play(FadeIn(cards_grp), run_time=0.8)

        # STATEMENT 1
        cap2 = caption_top("ประโยคที่ 1: ความเร็วแนวดิ่งต้องชะลอจนเป็นศูนย์ ป้องกันการกระแทก")
        self.play(
            ReplacementTransform(cap1, cap2),
            card1[0].animate.set_color(STATUS_OK),
            card1[2].animate.set_color(WHITE),
            card1[3].animate.set_color(STATUS_OK),
            card1[4].animate.become(Text("PASS", font_size=11, color=STATUS_OK).move_to(card1[3].get_center())),
            run_time=1.0
        )
        self.wait(1.0)

        # STATEMENT 2
        cap3 = caption_top("ประโยคที่ 2: ลำตัวต้องตั้งตรง ไม่เอียงเกินพิกัดเพื่อความมั่นคง")
        self.play(
            ReplacementTransform(cap2, cap3),
            card2[0].animate.set_color(STATUS_OK),
            card2[2].animate.set_color(WHITE),
            card2[3].animate.set_color(STATUS_OK),
            card2[4].animate.become(Text("PASS", font_size=11, color=STATUS_OK).move_to(card2[3].get_center())),
            run_time=1.0
        )
        self.wait(1.0)

        # STATEMENT 3
        cap4 = caption_top("ประโยคที่ 3: ขาลงจอดต้องรับน้ำหนักโครงสร้างจรวดจริงเต็ม 100%")
        self.play(
            ReplacementTransform(cap3, cap4),
            card3[0].animate.set_color(STATUS_OK),
            card3[2].animate.set_color(WHITE),
            card3[3].animate.set_color(STATUS_OK),
            card3[4].animate.become(Text("PASS", font_size=11, color=STATUS_OK).move_to(card3[3].get_center())),
            run_time=1.0
        )
        self.wait(1.0)

        # STATEMENT 4
        cap5 = caption_top("ประโยคที่ 4: สั่งตัดแรงขับเครื่องยนต์ทันที เพื่อไม่ให้จรวดดีดตัวกลับ")
        self.play(
            ReplacementTransform(cap4, cap5),
            card4[0].animate.set_color(STATUS_OK),
            card4[2].animate.set_color(WHITE),
            card4[3].animate.set_color(STATUS_OK),
            card4[4].animate.become(Text("PASS", font_size=11, color=STATUS_OK).move_to(card4[3].get_center())),
            run_time=1.0
        )
        self.wait(1.8)

        # ----------------------------------------------------------------------
        # Final Payoff: Physical Landing Event (26 - 36s)
        # ----------------------------------------------------------------------
        cap6 = caption_top("บทพิสูจน์สุดท้าย: เมื่อผ่านครบทุกประโยค -> จึงยืนยันการลงจอดสำเร็จ!")
        self.play(
            ReplacementTransform(cap5, cap6),
            FadeOut(cards_grp),
            run_time=0.6
        )

        # Ground pad and resting booster appear as final proof
        pad_line = Line([-6.5, -2.6, 0], [6.5, -2.6, 0], color=PAD_COLOR, stroke_width=4)
        pad_target = Circle(radius=0.75, color=PAD_COLOR, stroke_width=2).move_to([0, -2.6, 0])
        pad_target.stretch(0.25, dim=1)
        pad_x = Text("X", font_size=18, color=GRAYTXT).move_to([0, -2.6, 0])
        final_pad = VGroup(pad_line, pad_target, pad_x)

        body = RoundedRectangle(width=0.75, height=3.0, corner_radius=0.12, color=WHITE, fill_color=BOOSTER_BODY, fill_opacity=0.95, stroke_width=2)
        nose = Polygon([-0.375, 1.5, 0], [0.375, 1.5, 0], [0, 1.95, 0], color=WHITE, fill_color=BOOSTER_BODY, fill_opacity=0.95, stroke_width=2)
        fin_l = Rectangle(width=0.28, height=0.14, color=WHITE, fill_color=METAL, fill_opacity=0.8, stroke_width=1.5).move_to([-0.48, 1.30, 0])
        fin_r = Rectangle(width=0.28, height=0.14, color=WHITE, fill_color=METAL, fill_opacity=0.8, stroke_width=1.5).move_to([0.48, 1.30, 0])
        engine_nozzle = Polygon([-0.24, -1.5, 0], [0.24, -1.5, 0], [0.30, -1.75, 0], [-0.30, -1.75, 0], color=METAL, fill_color=METAL, fill_opacity=0.9, stroke_width=1.5)
        leg_l = Line([-0.34, -1.4, 0], [-0.90, -2.0, 0], color=METAL, stroke_width=4)
        foot_l = Line([-1.00, -2.0, 0], [-0.80, -2.0, 0], color=WHITE, stroke_width=3)
        leg_r = Line([0.34, -1.4, 0], [0.90, -2.0, 0], color=METAL, stroke_width=4)
        foot_r = Line([0.80, -2.0, 0], [1.00, -2.0, 0], color=WHITE, stroke_width=3)

        final_booster = VGroup(
            body, nose, fin_l, fin_r, engine_nozzle,
            leg_l, foot_l, leg_r, foot_r
        ).move_to([0, -0.6, 0])

        badge_box = RoundedRectangle(width=7.2, height=0.85, corner_radius=0.12, color=STATUS_OK, fill_color=BLACK, fill_opacity=0.85, stroke_width=2.5).move_to([0, 1.4, 0])
        badge_txt = Text("STATUS: LANDING CONFIRMED", font_size=19, color=STATUS_OK).move_to(badge_box.get_center())
        conf_badge = VGroup(badge_box, badge_txt)

        self.play(FadeIn(final_pad), FadeIn(final_booster), FadeIn(conf_badge), run_time=1.0)
        self.play(Flash(badge_box, color=STATUS_OK, flash_radius=0.5), run_time=0.8)
        self.wait(2.2)

        # Close Note
        rule_note = Text("Script-First: พิสูจน์ความจริงทีละประโยคก่อนเห็นผลลัพธ์สุดท้าย", font_size=13, color=GRAYTXT).move_to([0, -1.8, 0])
        sub_note = Text("(Illustrative Model · ระบบจริงมี Redundancy เซนเซอร์ตรวจซ้ำซ้อนหลายชุด)", font_size=11, color=GRAYTXT).next_to(rule_note, DOWN, buff=0.08)
        
        self.play(FadeIn(rule_note), FadeIn(sub_note), run_time=0.8)
        self.wait(3.0)

        self.fade_out_all(run_time=0.8)
