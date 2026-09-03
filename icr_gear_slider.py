"""Teaching package (visual-for-teach): gear rolling on a fixed rack drives an
eccentric pin A, connected via rod AB to slider B in a horizontal rail.
Find v_B and omega_AB.

Geometry, physics, and colour key are ALL derived from the spec — do not
re-derive differently here:
  Desktop/Main_note/Claude_Specs/Manim - Q1 Gear-Rack-Slider Geometry Spec.md

Source figure geometry (O, A colinear vertically) was confirmed by pixel-grid
measurement of the photo, not assumed. Physics solved and cross-checked two
independent ways before any scene code was written (spec section 4).
"""

from manim import *
import numpy as np
from mlib import (
    SafeScene, title, caption_top, page_ref, fit_width,
    METAL, GRAYTXT, WARN, WHITE, gear_shape,
)

GIVEN_OMEGA = "#FFB300"
IC_COL = "#26C6DA"
VA_COL = "#42A5F5"
VB_COL = "#66BB6A"
OMEGA_AB_COL = "#AB47BC"
TRAP_COL = "#FF5252"

SCALE = 0.45
ORIGIN_X, ORIGIN_Y = -1.0, -1.3

O_CM = np.array([0.0, 0.0])
C_CM = np.array([0.0, -3.0])
A_CM = np.array([0.0, -2.0])
B_CM = A_CM + 8.0 * np.array([np.cos(PI / 3), np.sin(PI / 3)])  # 60 deg


def cm(x, y):
    return np.array([ORIGIN_X + x * SCALE, ORIGIN_Y + y * SCALE, 0.0])


def cmv(v):
    return cm(v[0], v[1])


def hatch_block(center, w=0.5, h=0.9, n=4):
    """Small fixed-support symbol: a block with diagonal hatch lines."""
    body = Rectangle(width=w, height=h, fill_color=METAL, fill_opacity=0.35,
                      stroke_color=METAL, stroke_width=2).move_to(center)
    hatches = VGroup()
    top, bot = center[1] + h / 2, center[1] - h / 2
    left = center[0] - w / 2
    for i in range(n + 1):
        x = left + (w / n) * i
        hatches.add(Line([x, bot, 0], [x - 0.15, bot - 0.15, 0], color=METAL, stroke_width=1.5))
    return VGroup(body, hatches)


def build_mechanism():
    """Full mechanism, built once in clip-0 coordinates (spec section 1-2).
    Returns (group, parts) where parts is a dict for isolated redraws later."""
    gear = gear_shape(radius=3 * SCALE, teeth=14, color=METAL, fill_opacity=0.55,
                       stroke_width=2).move_to(cm(*O_CM))

    rack_y = cm(*C_CM)[1]
    rack_base = Rectangle(width=7.0, height=0.35, fill_color=METAL, fill_opacity=0.3,
                           stroke_color=METAL, stroke_width=2).move_to([cm(*O_CM)[0], rack_y - 0.35, 0])
    rack_teeth = VGroup()
    for i in range(-7, 8):
        tx = cm(*O_CM)[0] + i * 0.32
        rack_teeth.add(Rectangle(width=0.22, height=0.22, fill_color=METAL, fill_opacity=0.3,
                                  stroke_color=METAL, stroke_width=1.5).move_to([tx, rack_y - 0.13, 0]))
    ground = Line([cm(*O_CM)[0] - 3.6, rack_y - 0.53, 0], [cm(*O_CM)[0] + 3.6, rack_y - 0.53, 0],
                  color=METAL, stroke_width=2)
    rack = VGroup(rack_base, rack_teeth, ground)

    o_dot = Dot(cm(*O_CM), radius=0.045, color=WHITE)
    a_hub = VGroup(
        Circle(radius=0.16, color=METAL, fill_color=METAL, fill_opacity=0.7, stroke_width=2),
        Circle(radius=0.06, color=WHITE, stroke_width=1.5),
    ).move_to(cm(*A_CM))
    b_collar = Rectangle(width=0.55, height=0.32, fill_color=METAL, fill_opacity=0.8,
                          stroke_color=METAL, stroke_width=2).move_to(cm(*B_CM))
    b_pin = Circle(radius=0.06, color=WHITE, stroke_width=1.5).move_to(cm(*B_CM))

    rod = Line(cm(*A_CM), cm(*B_CM), color=METAL, stroke_width=6)

    rail_y = cm(*B_CM)[1]
    rail = Line([cm(*O_CM)[0] - 2.6, rail_y, 0], [cm(*O_CM)[0] + 5.6, rail_y, 0],
                color=METAL, stroke_width=5)
    wall_l = hatch_block([cm(*O_CM)[0] - 2.6, rail_y, 0])
    wall_r = hatch_block([cm(*O_CM)[0] + 5.6, rail_y, 0])

    omega_arc = CurvedArrow(cm(-2.6, 1.2), cm(-2.6, -1.2), angle=-TAU / 5, color=GIVEN_OMEGA,
                             stroke_width=4)
    omega_arc.tip.scale(0.45, about_point=omega_arc.get_end())
    omega_lbl = Text("omega = 6 rad/s", font_size=15, color=GIVEN_OMEGA).move_to([-3.7, -0.5, 0])

    parts = dict(gear=gear, rack=rack, o_dot=o_dot, a_hub=a_hub, b_collar=b_collar,
                 b_pin=b_pin, rod=rod, rail=rail, wall_l=wall_l, wall_r=wall_r,
                 omega_arc=omega_arc, omega_lbl=omega_lbl)
    group = VGroup(rack, gear, rail, wall_l, wall_r, rod, a_hub, b_collar, b_pin, o_dot,
                    omega_arc, omega_lbl)
    return group, parts


def inset_of(full_group):
    """Persistent shrunk copy for the corner, per visual-for-teach's layout rule.
    Scale/position chosen from the mechanism's REAL bounding box (rack + both
    rail end-supports, not just the gear) -- an earlier 0.35/[-5.4,-0.6] version
    left only 0.07 units to the frame edge because the rail's supports extend
    well past the gear on both sides; the linter can't catch this (it only
    edge-checks text, not graphics), so it was verified by hand here instead."""
    inset = full_group.copy().scale(0.30, about_point=cm(*O_CM))
    inset.move_to([-5.2, -0.6, 0])
    return inset


class Q1_00_Setup(SafeScene):
    def construct(self):
        ttl = title("กลไกเฟือง-แร็ค-ก้านสไลด์")
        pref = page_ref("โจทย์ 1 · ICR")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        self.play(Create(p["rack"]), Create(p["gear"]), Create(p["rail"]),
                   FadeIn(p["wall_l"]), FadeIn(p["wall_r"]), Create(p["rod"]),
                   FadeIn(p["a_hub"]), FadeIn(p["b_collar"]), FadeIn(p["b_pin"]),
                   FadeIn(p["o_dot"]), run_time=1.8)
        self.play(Create(p["omega_arc"]), FadeIn(p["omega_lbl"]), run_time=0.8)

        # Name the parts, per visual-for-teach clip-0 contract. All four labels
        # sit in the one strip of the frame nothing else occupies (above the
        # rail, below caption_top) so leader lines can reach any part without
        # the label itself ever landing on the mechanism's own geometry.
        labels = [
            ("A = หมุดเยื้องศูนย์ (ติดกับเฟือง)", cm(*A_CM), [-4.9, 1.7, 0]),
            ("O = ศูนย์เฟือง (เคลื่อนที่ตามเฟือง)", cm(*O_CM), [-2.1, 1.7, 0]),
            ("จุดสัมผัสเฟือง-แร็ค", cm(*C_CM), [0.7, 1.7, 0]),
            ("B = สไลเดอร์ในรางแนวนอน", cm(*B_CM), [3.5, 1.7, 0]),
        ]
        leaders = VGroup()
        texts = VGroup()
        for txt, pt, lbl_pos in labels:
            t = fit_width(Text(txt, font_size=14, color=WHITE).move_to(lbl_pos), 2.9)
            leaders.add(Line(pt, t.get_bottom() + DOWN * 0.05, color=GRAYTXT, stroke_width=1.2))
            texts.add(t)
        self.play(Create(leaders), FadeIn(texts), run_time=1.2)
        self.wait(1.3)
        self.play(FadeOut(leaders), FadeOut(texts), run_time=0.5)

        cap0 = caption_top("กำหนดให้: R=3cm, OA=2cm, AB=8cm, omega=6 rad/s (ทวนเข็ม), มุม 60°")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(cap0), run_time=0.3)

        cap1 = caption_top("มี alpha = 12 rad/s^2 ให้ด้วย — แต่โจทย์ข้อนี้ถามแค่ v_B กับ omega_AB ยังไม่ต้องใช้")
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("คำถาม: หาความเร็วของจุด B และความเร็วเชิงมุมของแขน AB ณ จังหวะนี้")
        self.play(FadeIn(cap2), run_time=0.7)
        self.wait(1.8)
        self.fade_out_all(run_time=0.9)


class Q1_01_MotionClassification(SafeScene):
    def construct(self):
        ttl = title("จำแนกชนิดการเคลื่อนที่")
        pref = page_ref("โจทย์ 1 · ขั้น 1")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        self.play(FadeIn(mech), run_time=1.0)

        cap0 = caption_top("ก่อนคำนวณ ต้องรู้ก่อนว่าแต่ละชิ้นเคลื่อนที่แบบไหน")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap0), run_time=0.3)

        glow = SurroundingRectangle(p["gear"], color=GIVEN_OMEGA, stroke_width=3, buff=0.05)
        cap1 = caption_top("เฟือง: กลิ้งบนแร็ค = หมุน + เลื่อนไปพร้อมกัน (general plane motion)")
        self.play(Create(glow), FadeIn(cap1), run_time=0.8)
        self.wait(1.5)
        cap1b = caption_top("แต่ ณ จังหวะหนึ่งๆ มองเป็น \"หมุนรอบจุดสัมผัส\" ล้วนๆ ได้ (เดี๋ยวเห็นในขั้น 3)")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap1b), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(cap1b), FadeOut(glow), run_time=0.4)

        glow2 = SurroundingRectangle(p["rod"], color=OMEGA_AB_COL, stroke_width=3, buff=0.08)
        cap2 = caption_top("ก้าน AB: ปลาย A ติดเฟือง ปลาย B ไถลในราง — ไม่ได้ตรึงจุดไหนเลย")
        self.play(Create(glow2), FadeIn(cap2), run_time=0.8)
        self.wait(1.2)
        cap2b = caption_top("ก้านตรึงจุดไม่ได้ = general plane motion เหมือนกัน ต้องหา IC ของตัวเอง")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap2b), run_time=0.7)
        self.wait(1.3)
        self.play(FadeOut(cap2b), FadeOut(glow2), run_time=0.4)

        glow3 = SurroundingRectangle(VGroup(p["b_collar"], p["b_pin"]), color=VB_COL,
                                      stroke_width=3, buff=0.1)
        cap3 = caption_top("จุด B: ถูกรางบังคับให้ไปแนวนอนเท่านั้น = pure translation")
        self.play(Create(glow3), FadeIn(cap3), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(cap3), FadeOut(glow3), run_time=0.4)

        self.fade_out_all(run_time=0.9)


class Q1_02_Trap(SafeScene):
    def construct(self):
        ttl = title("กับดัก: O ไม่ใช่จุดตรึง")
        pref = page_ref("โจทย์ 1 · ขั้น 2")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        self.play(FadeIn(mech), run_time=1.0)

        cap0 = caption_top("วิธีที่คนมักคิดผิด: มอง O เหมือนแกนเฟืองที่ตรึงอยู่กับที่")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.3)

        wrong_line = Line(cm(*O_CM), cm(*A_CM), color=TRAP_COL, stroke_width=5)
        wrong_lbl = fit_width(Text("v_A = omega x OA = 6 x 2 = 12 cm/s ?", font_size=15,
                                    color=TRAP_COL), 4.5).move_to([0.5, 1.9, 0])
        self.play(Create(wrong_line), FadeIn(wrong_lbl), run_time=1.0)
        self.wait(1.6)

        cap1 = caption_top("ผิด! O เองก็เคลื่อนที่ (เฟืองกลิ้งไปทั้งลูก) O ไม่ใช่จุดตรึง")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.6)

        cross = VGroup(
            Line(wrong_lbl.get_left() + LEFT * 0.1, wrong_lbl.get_right() + RIGHT * 0.1,
                 color=TRAP_COL, stroke_width=3),
        )
        self.play(Create(cross), run_time=0.5)
        self.wait(0.6)

        cap2 = caption_top("ต้องหาจุดที่ความเร็ว = 0 บนเฟือง ณ จังหวะนี้ก่อน (IC จริง) แล้วค่อยวัดระยะจากจุดนั้น")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.7)
        self.wait(1.7)
        preview = fit_width(Text("คำตอบจริง: 6 cm/s (ครึ่งเดียวของ 12)", font_size=15,
                                  color=VA_COL), 4.5).move_to([0.5, 1.3, 0])
        self.play(FadeIn(preview), run_time=0.6)
        self.wait(1.5)

        self.fade_out_all(run_time=0.9)


class Q1_03_GearIC(SafeScene):
    def construct(self):
        ttl = title("ขั้น 1: หา IC ของเฟือง")
        pref = page_ref("โจทย์ 1 · ขั้น 3")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        inset = inset_of(mech)
        self.play(FadeIn(inset), run_time=0.8)

        gear2 = p["gear"].copy().move_to([0.5, -0.5, 0]).scale(1.7)
        rack2_y = gear2.get_bottom()[1]
        self.play(FadeIn(gear2), run_time=0.8)

        cap0 = caption_top("เฟืองกลิ้งบนแร็คโดยไม่ลื่นไถล — จุดสัมผัสขณะนั้นความเร็ว = 0 เสมอ")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.6)

        contact = Dot([0.5, rack2_y, 0], radius=0.09, color=IC_COL)
        ic_lbl = Text("IC ของเฟือง (v=0)", font_size=16, color=IC_COL).next_to(contact, DOWN, buff=0.25)
        self.play(FadeIn(contact), FadeIn(ic_lbl), run_time=0.7)
        self.wait(1.4)

        cap1 = caption_top("ทำไม? ถ้าจุดนั้นมีความเร็ว แร็คกับเฟืองจะไถลผ่านกัน ขัดกับ \"กลิ้งไม่ไถล\"")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.7)

        o2 = gear2.get_center()
        o_dot2 = Dot(o2, radius=0.06, color=WHITE)
        r_line = Line(o2, contact.get_center(), color=IC_COL, stroke_width=3)
        r_lbl = Text("R = 3 cm", font_size=15, color=IC_COL).next_to(r_line, RIGHT, buff=0.15)
        self.play(FadeIn(o_dot2), Create(r_line), FadeIn(r_lbl), run_time=0.9)
        self.wait(1.5)

        cap2 = caption_top("ระยะจาก O ถึง IC เท่ากับรัศมีเฟืองเสมอ (O อยู่เหนือจุดสัมผัสตรงๆ)")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.7)
        self.wait(1.6)

        self.fade_out_all(run_time=0.9)


class Q1_04_VelocityA(SafeScene):
    def construct(self):
        ttl = title("ขั้น 2: หาความเร็วจุด A")
        pref = page_ref("โจทย์ 1 · ขั้น 4")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        inset = inset_of(mech)
        self.play(FadeIn(inset), run_time=0.8)

        cx, gy = 0.5, -0.7
        gear2 = p["gear"].copy().move_to([cx, gy, 0]).scale(1.7)
        o2 = gear2.get_center()
        r_gear = 3 * SCALE * 1.7
        c2 = np.array([cx, gy - r_gear, 0])
        a2 = np.array([cx, gy - r_gear * (2 / 3), 0])  # OA=2, R=3 -> A is 2/3 of the way down
        self.play(FadeIn(gear2), run_time=0.6)

        o_dot2 = Dot(o2, radius=0.06, color=WHITE)
        contact = Dot(c2, radius=0.09, color=IC_COL)
        ic_lbl = Text("IC", font_size=16, color=IC_COL).next_to(contact, DOWN, buff=0.15)
        a_dot = Dot(a2, radius=0.07, color=WHITE)
        a_lbl = Text("A", font_size=16, color=WHITE).next_to(a_dot, RIGHT, buff=0.12)
        self.play(FadeIn(o_dot2), FadeIn(contact), FadeIn(ic_lbl), FadeIn(a_dot), FadeIn(a_lbl),
                   run_time=0.7)

        cap0 = caption_top("A อยู่บนเส้นตรงเดียวกับ O และ IC (วัดจากภาพจริง) — ระยะ IC ถึง A คือเท้าที่ต้องใช้")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.5)

        ac_line = Line(c2, a2, color=IC_COL, stroke_width=4)
        ac_lbl = Text("R - OA = 3 - 2 = 1 cm", font_size=15, color=IC_COL)
        ac_lbl.move_to([cx + 3.3, (c2[1] + a2[1]) / 2, 0])
        ac_leader = Line(ac_line.get_center(), ac_lbl.get_left() + LEFT * 0.1,
                          color=IC_COL, stroke_width=1.2)
        self.play(Create(ac_line), Create(ac_leader), FadeIn(ac_lbl), run_time=0.9)
        self.wait(1.6)

        cap1 = caption_top("v_A = omega x (ระยะ IC-A) = 6 x 1 = 6 cm/s")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.4)

        cap2 = caption_top("ทิศ: v_A ตั้งฉากกับเส้น IC-A เสมอ — เส้นนี้ตั้ง (ดิ่ง) ⇒ v_A ต้องแนวนอน")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.8)
        self.wait(1.7)

        v_a = Arrow(a2, a2 + LEFT * 1.3, color=VA_COL, buff=0, stroke_width=6,
                    max_tip_length_to_length_ratio=0.25)
        va_lbl = Text("v_A = 6 cm/s", font_size=16, color=VA_COL).next_to(v_a, UP, buff=0.15)
        self.play(GrowArrow(v_a), FadeIn(va_lbl), run_time=0.9)

        cap3 = caption_top("หมุนเส้น IC-A ไป 90° ตามทิศ omega (ทวนเข็ม) ⇒ ชี้ไปทางซ้าย")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.7)
        self.wait(1.8)

        self.fade_out_all(run_time=0.9)


class Q1_05_RodIC(SafeScene):
    def construct(self):
        ttl = title("ขั้น 3: IC ของก้าน AB")
        pref = page_ref("โจทย์ 1 · ขั้น 5")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        inset = inset_of(mech)
        self.play(FadeIn(inset), run_time=0.8)

        a2 = np.array([-1.6, -1.6, 0])
        b2 = a2 + 3.4 * np.array([np.cos(PI / 3), np.sin(PI / 3), 0])
        rod2 = Line(a2, b2, color=METAL, stroke_width=6)
        a_dot = Dot(a2, radius=0.07, color=WHITE)
        b_dot = Dot(b2, radius=0.07, color=WHITE)
        # Sideways, not DOWN/UP: the perpendicular construction lines added below
        # are vertical through these exact x-positions, so DOWN/UP placement
        # would sit the label right on top of its own line regardless of buff.
        # up-left of A: down/left is v_a's arrow path, straight up is perp_a
        a_lbl = Text("A", font_size=16, color=WHITE).move_to(a2 + np.array([-0.35, 0.3, 0]))
        b_lbl = Text("B", font_size=16, color=WHITE).next_to(b_dot, RIGHT, buff=0.15)
        self.play(Create(rod2), FadeIn(a_dot), FadeIn(b_dot), FadeIn(a_lbl), FadeIn(b_lbl),
                   run_time=0.9)

        v_a = Arrow(a2, a2 + LEFT * 1.1, color=VA_COL, buff=0, stroke_width=6,
                    max_tip_length_to_length_ratio=0.28)
        va_lbl = Text("v_A แนวนอน (เพิ่งหา)", font_size=14, color=VA_COL).move_to([-3.1, -1.9, 0])
        v_b_dir = Arrow(b2, b2 + LEFT * 1.1, color=GRAYTXT, buff=0, stroke_width=4,
                        max_tip_length_to_length_ratio=0.28)
        vb_lbl = Text("v_B แนวนอนแน่ (รางบังคับ)", font_size=14, color=GRAYTXT).move_to([1.7, 1.9, 0])
        self.play(GrowArrow(v_a), FadeIn(va_lbl), GrowArrow(v_b_dir), FadeIn(vb_lbl), run_time=1.0)

        cap0 = caption_top("หา IC ของ AB: ลากเส้นตั้งฉากกับความเร็วที่ A และที่ B แล้วดูจุดตัด")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.6)

        # perp_b's UP extent is capped at 0.9 (not the symmetric 1.6 perp_a uses)
        # because b2 already sits high (y=1.344) -- a symmetric +-1.6 would push
        # its top to y=2.94, past caption_top's zone at y=2.72.
        perp_a = DashedLine(a2 + UP * 1.6, a2 + DOWN * 1.6, color=IC_COL, stroke_width=3)
        perp_b = DashedLine(b2 + UP * 0.9, b2 + DOWN * 1.6, color=IC_COL, stroke_width=3)
        self.play(Create(perp_a), Create(perp_b), run_time=1.0)
        self.wait(1.0)

        cap1 = caption_top("v_A กับ v_B แนวนอนทั้งคู่ ⇒ เส้นตั้งฉากทั้งสองเป็นเส้นดิ่ง ขนานกัน")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.6)

        cap2 = caption_top("เส้นขนานไม่ตัดกัน ⇒ IC อยู่ที่ \"อนันต์\" ⇒ ก้านนี้ไม่ได้กำลังหมุน")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.8)
        self.wait(1.8)

        result = Text("omega_AB = 0 rad/s (เลื่อนตรง ณ จังหวะนี้)", font_size=18, color=OMEGA_AB_COL)
        result.move_to([1.8, -2.6, 0])
        box = SurroundingRectangle(result, color=OMEGA_AB_COL, buff=0.15)
        self.play(FadeIn(result), Create(box), run_time=0.9)
        self.wait(1.8)

        self.fade_out_all(run_time=0.9)


class Q1_06_VelocityB(SafeScene):
    def construct(self):
        ttl = title("ขั้น 4: หาความเร็วจุด B")
        pref = page_ref("โจทย์ 1 · ขั้น 6")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        mech, p = build_mechanism()
        inset = inset_of(mech)
        self.play(FadeIn(inset), run_time=0.8)

        a2 = np.array([-1.6, -1.6, 0])
        b2 = a2 + 3.4 * np.array([np.cos(PI / 3), np.sin(PI / 3), 0])
        rod2 = Line(a2, b2, color=METAL, stroke_width=6)
        a_dot = Dot(a2, radius=0.07, color=WHITE)
        b_dot = Dot(b2, radius=0.07, color=WHITE)
        self.play(Create(rod2), FadeIn(a_dot), FadeIn(b_dot), run_time=0.7)

        cap0 = caption_top("omega_AB = 0 ⇒ ก้านทั้งท่อนเคลื่อนที่แบบ \"เลื่อนขนาน\" ล้วนๆ")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.4)

        cap1 = caption_top("เลื่อนขนาน (translation) แปลว่าทุกจุดบนก้านมีความเร็วเท่ากันหมด ทั้งขนาดและทิศ")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.8)
        self.wait(1.7)

        v_a = Arrow(a2, a2 + LEFT * 1.1, color=VA_COL, buff=0, stroke_width=6,
                    max_tip_length_to_length_ratio=0.28)
        va_lbl = Text("v_A = 6 cm/s", font_size=14, color=VA_COL).next_to(v_a, DOWN, buff=0.12)
        self.play(GrowArrow(v_a), FadeIn(va_lbl), run_time=0.8)

        cap2 = caption_top("ดังนั้น v_B ต้องเท่ากับ v_A เป๊ะ — ทั้งขนาดและทิศทาง")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.7)
        self.wait(1.5)

        v_b = Arrow(b2, b2 + LEFT * 1.1, color=VB_COL, buff=0, stroke_width=6,
                    max_tip_length_to_length_ratio=0.28)
        vb_lbl = Text("v_B = 6 cm/s", font_size=16, color=VB_COL).next_to(v_b, UP, buff=0.15)
        self.play(GrowArrow(v_b), FadeIn(vb_lbl), run_time=0.9)
        self.wait(1.0)

        result = Text("v_B = 6 cm/s ไปทางซ้าย", font_size=18, color=VB_COL).move_to([1.8, -2.6, 0])
        box = SurroundingRectangle(result, color=VB_COL, buff=0.15)
        self.play(FadeIn(result), Create(box), run_time=0.9)
        self.wait(1.8)

        self.fade_out_all(run_time=0.9)


class Q1_07_CrossCheck(SafeScene):
    def construct(self):
        ttl = title("เช็คซ้ำด้วยสมการเวกเตอร์")
        pref = page_ref("โจทย์ 1 · เช็คซ้ำ")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        cap0 = caption_top("ทวนด้วยวิธีที่ 2: สมการความเร็วสัมพัทธ์ตรงๆ ไม่ผ่าน IC เลย")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.3)

        eq0 = MathTex(r"\vec{v}_B = \vec{v}_A + \vec{\omega}_{AB} \times \vec{r}_{B/A}",
                       font_size=32, color=WHITE).move_to([0, 0.9, 0])
        self.play(FadeIn(eq0), run_time=0.8)
        self.wait(1.2)

        cap1 = caption_top("ตั้งแกน x-y ที่ A: จาก 60° กับ AB=8cm ได้ r_B/A = (4, 6.93) cm")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.8)
        self.wait(1.5)

        r_diagram = VGroup()
        a3 = np.array([-2.2, -1.6, 0])
        b3 = a3 + 1.6 * np.array([np.cos(PI / 3), np.sin(PI / 3), 0])
        r_line = Line(a3, b3, color=WHITE, stroke_width=4)
        dx_line = DashedLine(a3, [b3[0], a3[1], 0], color=GRAYTXT, stroke_width=2)
        dy_line = DashedLine([b3[0], a3[1], 0], b3, color=GRAYTXT, stroke_width=2)
        dx_lbl = Text("4 cm", font_size=13, color=GRAYTXT).next_to(dx_line, DOWN, buff=0.1)
        dy_lbl = Text("6.93 cm", font_size=13, color=GRAYTXT).next_to(dy_line, RIGHT, buff=0.1)
        r_diagram.add(r_line, dx_line, dy_line, dx_lbl, dy_lbl)
        self.play(Create(r_diagram), run_time=1.0)
        self.wait(1.4)

        eq1 = MathTex(r"v_{B,y} = v_{A,y} + \omega_{AB}\,(4)", font_size=26, color=WHITE)
        eq1.move_to([2.3, -0.9, 0])
        self.play(FadeIn(eq1), run_time=0.7)
        self.wait(1.0)

        cap2 = caption_top("v_A ไม่มีองค์ประกอบดิ่ง (แนวนอนล้วน) และ v_B ก็ต้องไม่มีองค์ประกอบดิ่ง (รางบังคับ)")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.8)
        self.wait(1.6)

        eq2 = MathTex(r"0 = 0 + \omega_{AB}(4) \;\Rightarrow\; \omega_{AB} = 0",
                       font_size=28, color=OMEGA_AB_COL).move_to([2.3, -1.7, 0])
        self.play(FadeIn(eq2), run_time=0.8)
        self.wait(1.5)

        cap3 = caption_top("ตรงกับวิธี IC เป๊ะ: omega_AB = 0 แล้ว v_B = v_A = 6 cm/s ทั้งสองวิธี")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.8)
        self.wait(2.0)

        self.fade_out_all(run_time=0.9)


class Q1_08_Recipe(SafeScene):
    def construct(self):
        ttl = title("สรุปวิธี — ใช้กับโจทย์อื่นได้")
        pref = page_ref("โจทย์ 1 · สรุป")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        steps = [
            "1) วัตถุกลิ้งไม่ไถล ⇒ IC = จุดสัมผัส (v=0 ที่นั่นเสมอ)",
            "2) หา v ที่จุดเชื่อมต่อ จาก v = omega x (ระยะจาก IC)",
            "3) เช็คทิศทางที่ถูกบังคับของอีกจุด (ราง/หมุด) ก่อนสรุปว่าก้านหมุน",
            "4) ลากเส้นตั้งฉากกับความเร็ว 2 จุด — ถ้าขนานกัน = เลื่อนตรง ไม่ใช่ error",
            "5) ตัดกันจริง = นั่นคือ IC ของก้านนั้น ใช้หา omega ที่เหลือได้เลย",
        ]
        group = VGroup(*[Text(s, font_size=18, color=WHITE) for s in steps])
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.8, 0])
        fit_width(group, 11.5)

        for line in group:
            self.play(FadeIn(line), run_time=0.6)
            self.wait(0.9)

        cap = caption_top("ใช้สูตรนี้ได้กับกลไก gear-rack-slider แบบไหนก็ได้ ไม่ใช่แค่ตัวเลขชุดนี้")
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(2.0)

        self.fade_out_all(run_time=0.9)
