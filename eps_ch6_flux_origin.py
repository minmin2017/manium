"""EPS บทที่ 6 (เสริม) — สนามอาร์เมเจอร์มาจากไหน: ทีละตัวนำจริงด้วยกฎมือขวา

คู่กับ EP08 (สนามสองสนามบวกกัน) — EP08 สรุปสนามอาร์เมเจอร์เป็น "ลูกศรเดียว
ชี้ดิ่ง 90°" แบบนามธรรม ตัวนี้ (EP08B) ไล่ย้อนกลับไปตอบว่าลูกศรนั้นมาจากไหน
จริงๆ: ตัวนำแต่ละเส้นในสล็อทอาร์เมเจอร์มีกระแสไหล → แต่ละเส้นสร้างสนามวงกลม
ของตัวเอง (กฎมือขวา/แอมแปร์) → สนามวงเล็กๆ หลายสิบวงรวมกัน (superposition)
ถึงจะได้ลูกศรเดียวที่เห็นใน EP08

หมายเหตุ: มีคลิปชื่อ EP09_RightHandRule_ArmatureFlux_StepByStep.mp4 ทำเรื่อง
เดียวกันนี้ไว้ก่อนแล้ว (จาก session อื่น, ไม่ได้ import mlib) แต่มีบั๊กจริง —
ข้อความในพาเนลขวาซ้อนทับกันอ่านไม่ออก (ไม่ผ่าน layout linter เพราะไม่ได้ใช้
SafeScene) คลิปนี้สร้างใหม่ด้วยเนื้อหา/สรุปเดียวกัน (ตรวจสอบว่าถูกต้องแล้ว)
แต่ผ่าน SafeScene ให้ข้อความไม่ทับกันจริง

ผิด: สนามอาร์เมเจอร์คือ "ลูกศรใหญ่" ที่มาจากไหนก็ไม่รู้
อ๋อ: มันคือผลรวมของสนามวงกลมเล็กๆ จากตัวนำจริงหลายสิบเส้น ตัวนำซีกบนกับซีก
     ล่างของอาร์เมเจอร์มีกระแสไหลคนละทิศ (⊙ กับ ⊗) กฎมือขวาให้สนามวงกลมคนละ
     ทิศหมุน แต่ตรงกึ่งกลาง (ที่ประเมิน) ทั้งสองวงชี้ทางเดียวกัน (ลง) พอดี —
     บวกกันเสริมแรง ไม่ใช่หักล้าง
"""

import numpy as np
from manim import *
from mlib import *

RING_R = 1.85
COND_R = 0.11
STAGE = np.array([-2.15, -0.05, 0.0])


def conductor(center, out_of_page, color=CURRENT):
    """ตัวนำ 1 เส้น — ⊙ กระแสพุ่งออก, ⊗ กระแสพุ่งเข้า"""
    body = Circle(radius=COND_R, color=color, fill_color=color,
                  fill_opacity=0.85, stroke_width=2).move_to(center)
    if out_of_page:
        mark = Dot(center, radius=COND_R * 0.34, color=WHITE)
    else:
        d = COND_R * 0.62
        mark = VGroup(
            Line(center + [-d, -d, 0], center + [d, d, 0], color=WHITE, stroke_width=2.4),
            Line(center + [-d, d, 0], center + [d, -d, 0], color=WHITE, stroke_width=2.4),
        )
    return VGroup(body, mark)


def rhr_circle(center, radius, ccw, color=FIELD, sw=3.2):
    """สนามวงกลมรอบตัวนำ (กฎมือขวา) — ccw=True หมุนทวนเข็ม"""
    ang = TAU * 0.82 * (1 if ccw else -1)
    arc = Arc(radius=radius, start_angle=-PI / 2, angle=ang,
             arc_center=center, color=color, stroke_width=sw)
    arc.add_tip(tip_length=0.14)
    return arc


class EP08B_ConductorRHRToFlux(SafeScene):
    def construct(self):
        ttl = title("สนามอาร์เมเจอร์มาจากไหน — ดูทีละเส้นลวดจริง", size=27)
        self.play(FadeIn(ttl, shift=DOWN * 0.2))

        c0 = caption("คลิปก่อนสรุปว่าสนามอาร์เมเจอร์เป็นลูกศรเดียวชี้ดิ่ง 90° — มันมาจากไหน?")
        self.play(FadeIn(c0), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(c0), run_time=0.3)

        # ---------- ฉาก 1: ซูมดูตัวนำ 2 เส้นตัวแทน ----------
        # แก้ 2026-08-31: เดิมวางตัวนำบน/ล่าง ซึ่งไม่ตรงกับกฎจริงของเครื่อง DC
        # (ตรวจแล้วทั้งหนังสือ Min และแหล่งอ้างอิงมาตรฐานภายนอกยืนยันตรงกัน:
        # ตัวนำใต้ขั้ว N กระแสเข้าจอ ใต้ขั้ว S กระแสออกจอ — แบ่งซ้าย/ขวา ไม่ใช่บน/ล่าง)
        left_c = STAGE + np.array([-1.55, 0, 0])
        right_c = STAGE + np.array([1.55, 0, 0])
        mid_c = STAGE

        left_cond = conductor(left_c, False)
        left_lbl = Text("ตัวนำใกล้ขั้ว N (⊗ พุ่งเข้า)", font_size=21, color=CURRENT)
        left_lbl.next_to(left_cond, LEFT, buff=0.85)

        c1 = caption("ตัวนำ 1 เส้น มีกระแสไหล → สร้างสนามวงกลมรอบตัวเอง (กฎมือขวา)")
        self.play(FadeIn(c1), FadeIn(left_cond), FadeIn(left_lbl), run_time=0.9)
        self.wait(0.6)

        left_circ = rhr_circle(left_c, 0.62, ccw=False)
        rule1 = Text("นิ้วโป้งชี้เข้าหาจอ → 4 นิ้วกำวนตามเข็มนาฬิกา", font_size=19,
                     color=GRAYTXT)
        rule1.next_to(left_cond, DOWN, buff=0.85)
        fit_width(rule1, 4.6)
        self.play(FadeOut(c1), run_time=0.3)
        self.play(Create(left_circ), FadeIn(rule1), run_time=1.0)
        self.wait(0.9)
        self.play(FadeOut(rule1), run_time=0.3)

        # ---------- ตัวนำที่ 2 ----------
        right_cond = conductor(right_c, True)
        right_lbl = Text("ตัวนำใกล้ขั้ว S (⊙ พุ่งออก)", font_size=21, color=CURRENT)
        right_lbl.next_to(right_cond, RIGHT, buff=0.85)

        c2 = caption("อีกฝั่งของขดเดียวกัน กระแสไหลกลับทิศ (⊙)")
        self.play(FadeIn(c2), FadeIn(right_cond), FadeIn(right_lbl), run_time=0.9)
        self.wait(0.6)

        right_circ = rhr_circle(right_c, 0.62, ccw=True)
        rule2 = Text("นิ้วโป้งชี้ออกจากจอ → 4 นิ้วกำวนทวนเข็มนาฬิกา", font_size=19,
                     color=GRAYTXT)
        rule2.next_to(right_cond, DOWN, buff=0.85)
        fit_width(rule2, 4.6)
        self.play(FadeOut(c2), run_time=0.3)
        self.play(Create(right_circ), FadeIn(rule2), run_time=1.0)
        self.wait(0.9)
        self.play(FadeOut(rule2), run_time=0.3)

        # ---------- ฉาก 2: ตรงกึ่งกลาง สองสนามชี้ทางเดียวกัน (จังหวะ "อ๋อ") ----------
        # ทั้งสองเส้น: ตรงจุดกึ่งกลาง สนามจาก RHR ชี้ "ลง" เหมือนกัน (ตัวนำซ้าย/⊗ อยู่
        # ทางซ้ายของจุดกึ่งกลาง วงหมุนตามเข็ม -> ที่ตำแหน่งขวาของมันชี้ลง;
        # ตัวนำขวา/⊙ อยู่ทางขวาของจุดกึ่งกลาง วงหมุนทวนเข็ม -> ที่ตำแหน่งซ้ายของมันชี้ลงเช่นกัน)
        a1 = Arrow(mid_c + [-0.20, 0.55, 0], mid_c + [-0.20, -0.35, 0], buff=0,
                  color=OK, stroke_width=6, tip_length=0.20)
        a2 = Arrow(mid_c + [0.20, 0.55, 0], mid_c + [0.20, -0.35, 0], buff=0,
                  color=OK, stroke_width=6, tip_length=0.20)

        c3 = caption("ตรงกึ่งกลาง — สนามจากตัวนำซ้ายกับขวา ชี้ทางเดียวกันพอดี (ลง)",
                     color=OK)
        fit_width(c3, 12.8)
        self.play(FadeIn(c3), run_time=0.5)
        self.play(GrowArrow(a1), run_time=0.6)
        self.play(GrowArrow(a2), run_time=0.6)
        self.wait(0.8)

        sum_lbl = Text("บวกเสริมแรง ไม่ใช่หักล้าง", font_size=22, color=OK)
        sum_lbl.next_to(VGroup(a1, a2), RIGHT, buff=0.9)
        self.play(FadeIn(sum_lbl), run_time=0.6)
        self.wait(1.0)

        # ---------- เก็บฉากซูม ----------
        self.play(*[FadeOut(m) for m in
                    (left_cond, left_lbl, left_circ, right_cond, right_lbl, right_circ,
                     a1, a2, sum_lbl, c3)], run_time=0.7)

        # ---------- ฉาก 3: ขยายเป็นวงจริง — ไม่ใช่แค่ 2 เส้น มีหลายสิบเส้น ----------
        c4 = caption("แต่จริงๆ อาร์เมเจอร์ไม่ได้มีแค่ 2 เส้น — มีหลายสิบเส้นรอบวง")
        self.play(FadeIn(c4), run_time=0.6)

        ring = Circle(radius=RING_R, color=METAL, stroke_width=3).move_to(STAGE)
        self.play(Create(ring), run_time=0.7)

        n_cond = 10
        conductors = VGroup()
        mini_circles = VGroup()
        for i in range(n_cond):
            a = PI / 2 + (i + 0.5) * TAU / n_cond
            pos = STAGE + RING_R * np.array([np.cos(a), np.sin(a), 0])
            out = np.cos(a) > 0  # ใกล้ขั้ว S (ขวา) = ออก (⊙), ใกล้ขั้ว N (ซ้าย) = เข้า (⊗)
            cd = conductor(pos, out, color=CURRENT)
            conductors.add(cd)
            mini_circles.add(rhr_circle(pos, 0.30, ccw=out, sw=2.2))

        self.play(LaggedStart(*[FadeIn(c) for c in conductors], lag_ratio=0.08),
                  run_time=1.3)
        self.wait(0.4)
        self.play(FadeOut(c4), run_time=0.3)

        c5 = caption("ทุกเส้นสร้างสนามวงเล็กของตัวเอง — ตามกฎมือขวาเดิม")
        fit_width(c5, 12.8)
        self.play(FadeIn(c5), LaggedStart(*[Create(c) for c in mini_circles],
                                          lag_ratio=0.08), run_time=1.6)
        self.wait(0.9)
        self.play(FadeOut(c5), run_time=0.3)

        # ---------- รวมเป็นลูกศรเดียว ----------
        big_arrow = Arrow(STAGE + [0, 1.35, 0], STAGE + [0, -1.35, 0], buff=0,
                          color=OK, stroke_width=9, tip_length=0.32)
        ba_lbl = Text("Bₐ — สนามอาร์เมเจอร์รวม", font_size=24, color=OK)
        ba_lbl.next_to(ring, RIGHT, buff=0.7)
        fit_width(ba_lbl, 4.3)

        c6 = caption("รวมทุกวงเล็ก (superposition) = ลูกศรเดียวที่เห็นใน EP08",
                     color=OK)
        fit_width(c6, 12.8)
        self.play(FadeOut(mini_circles), FadeOut(conductors), run_time=0.6)
        self.play(FadeIn(c6), GrowArrow(big_arrow), FadeIn(ba_lbl), run_time=1.2)
        self.wait(1.4)

        # ---------- สรุป ----------
        self.play(*[FadeOut(m) for m in (ring, big_arrow, ba_lbl, c6, ttl)],
                  run_time=0.8)
        s1 = Text("ลูกศรสนามอาร์เมเจอร์ = ผลรวมสนามวงกลมของตัวนำจริงทุกเส้น",
                  font_size=27, color=WHITE)
        fit_width(s1, 12.0)
        s2 = Text("แต่ละเส้นก็แค่กฎมือขวาธรรมดา — ไม่มีอะไรลึกลับ", font_size=24,
                  color=OK)
        card = VGroup(s1, s2).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)
