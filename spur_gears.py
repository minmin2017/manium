"""
spur_gears.py -- Mechanics of Machinery W06, "Spur Gears" (source ch.4), pages 1-39.

Source note: Exam_Prep/Mechanics of Machinery/
  "W06 บทเรียนละเอียด -- เฟืองตรง (Spur Gears) หน้าต่อหน้า (บทที่ 4).md"
Formulas cross-checked 2026-09-04 against Wikipedia "Involute gear",
gearsolutions.com "Calculating the Inverse of an Involute", tec-science.com's
involute-gear articles -- see Claude_Specs/Spur Gear Series Geometry Spec.md
for the derived coordinate frame every meshing-pair scene below uses.

Pages 5 and 6 (G05A, G05B, G06) were already built in gear_law_similar.py in an
earlier session -- NOT duplicated here. This file picks up from page 7.

Naming: G<page>_<ShortName>, matching the page-number convention already
established by gear_law_similar.py (G05A/G05B/G06), not a flat sequential index.

Batch in this file: G01 (pages 1-2), G02 (page 3), G03 (page 4),
G07 (page 7), G08 (page 8), G09 (page 9), G10 (page 10), G11 (page 11),
G12 (page 12), G13 (page 13).
"""

import numpy as np
from manim import *
from mlib import *
from gear_law_similar import seg, pt, tag, ra_mark

# ----------------------------------------------------------------- palette
GEAR2 = GEAR_IN            # "#4FC3F7" -- gear/body 2 (driver), matches mlib convention
GEAR3 = GEAR_OUT           # "#FFB74D" -- gear/body 3 (follower)
PITCH_C = OK               # "#26C6DA" -- pitch circle / pitch point
BASE_C = "#AB47BC"         # base circle (reuses TORQUE hue, own constant for clarity)
LOA_C = "#EF5350"          # line of action / contact normal (matches gear_law_similar's C_NORM)
INVOL_C = "#66BB6A"        # involute curve itself (matches FORCE hue)


# ============================================================= shared geometry
def loa_frame(phi, R1, R2, sign=1.0):
    """เฟรมเรขาคณิตเฟืองคู่ขบกัน (ดู Claude_Specs/Spur Gear Series Geometry Spec.md ข้อ 1)
    คืน dict: O1, O2, P, Rb1, Rb2, C, d (ทิศ line of action), E1, E2 (จุดสัมผัส)
    พิสูจน์แล้วว่า E1, E2 อยู่บน base circle จริงด้วย assert ก่อนคืนค่า"""
    O1 = np.array([0.0, 0.0, 0.0])
    P = np.array([R1, 0.0, 0.0])
    O2 = np.array([R1 + R2, 0.0, 0.0])
    Rb1, Rb2 = R1 * np.cos(phi), R2 * np.cos(phi)
    d = np.array([sign * np.sin(phi), np.cos(phi), 0.0])
    E1 = P + float(np.dot(O1 - P, d)) * d
    E2 = P + float(np.dot(O2 - P, d)) * d
    assert abs(np.linalg.norm(E1 - O1) - Rb1) < 1e-9
    assert abs(np.linalg.norm(E2 - O2) - Rb2) < 1e-9
    return dict(O1=O1, O2=O2, P=P, Rb1=Rb1, Rb2=Rb2, C=R1 + R2, d=d, E1=E1, E2=E2,
                R1=R1, R2=R2, phi=phi)


def far_arc(O, r, angA, angB, away_from):
    """เลือกส่วนโค้งด้านที่ 'ไกลจาก' away_from (สำหรับสายพานไขว้ที่ต้องอ้อมหลังพูลเลย์)
    คืน (start_angle, signed_span) ให้ Arc(...) ใช้ได้ตรง"""
    span_ccw = (angB - angA) % TAU
    span_cw = span_ccw - TAU
    mid_ccw = O + r * np.array([np.cos(angA + span_ccw / 2), np.sin(angA + span_ccw / 2), 0])
    mid_cw = O + r * np.array([np.cos(angA + span_cw / 2), np.sin(angA + span_cw / 2), 0])
    if np.linalg.norm(mid_ccw - away_from) > np.linalg.norm(mid_cw - away_from):
        return angA, span_ccw
    return angA, span_cw


def ang_of(p, center):
    v = p - center
    return float(np.arctan2(v[1], v[0]))


# =====================================================================
# G01 -- หน้า 1-2: ปกบท + สารบัญ
# =====================================================================
class G01_CoverAndToc(SafeScene):
    def construct(self):
        head = Text("บทที่ 4 -- เฟืองตรง (Spur Gears)", font_size=38, color=WHITE)
        sub = Text("ส่งกำลังระหว่างเพลาขนานกัน 2 เพลา", font_size=24, color=GRAYTXT)
        VGroup(head, sub).arrange(DOWN, buff=0.35).move_to(UP * 1.6)
        self.play(FadeIn(head, shift=UP * 0.4))
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(0.6)

        cap = caption_top("6 หัวข้อของบทนี้", size=24)
        self.play(FadeIn(cap))

        items = [
            "1. Introduction, fundamentals of gear motion",
            "2. Involute gear teeth, \"Involutometry\"",
            "3. Motion and tooth shape for mating gears",
            "4. Interference and undercutting",
            "5. Standard gears and machining methods",
            "6. Backlash",
        ]
        rows = VGroup(*[Text(t, font_size=24, color=WHITE) for t in items])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(DOWN * 0.55)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.45)
        self.wait(1.4)

        note = Text("คลิปชุดนี้ตามหน้าสไลด์ 1-39 ทีละหน้า -- เริ่มจากหัวข้อ 1-2",
                     font_size=19, color=WARN)
        note.move_to([0, -3.15, 0])
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(1.6)


# =====================================================================
# G02 -- หน้า 3: เฟืองตรงคืออะไร + อัตราทดเฉลี่ย vs ขณะหนึ่ง
# =====================================================================
class G02_WhatIsSpurGear(SafeScene):
    def construct(self):
        self.add(title("เฟืองตรงคืออะไร", size=30))
        self.add(page_ref("หน้า 3"))

        cap = caption_top("เฟืองแบบง่ายที่สุด -- ส่งกำลังระหว่างเพลาขนานกัน 2 เพลา", size=23)
        self.play(FadeIn(cap))

        g1 = gear_shape(0.85, 12, GEAR2).move_to(LEFT * 2.6 + DOWN * 0.3)
        g2 = gear_shape(1.35, 20, GEAR3).move_to(
            g1.get_center() + RIGHT * (0.85 + 0.10 + 1.35))
        l1 = Text("เฟือง 1 (N=12)", font_size=19, color=GEAR2).next_to(g1, DOWN, buff=0.3)
        l2 = Text("เฟือง 2 (N=20)", font_size=19, color=GEAR3).next_to(g2, DOWN, buff=0.3)
        self.play(FadeIn(g1, shift=UP * 0.3), FadeIn(g2, shift=UP * 0.3),
                   FadeIn(l1), FadeIn(l2))
        spin(g1, 2.0)
        spin(g2, -2.0 * (0.85 / 1.35))
        self.wait(1.0)

        goal = Text("โจทย์ออกแบบ: angular velocity ratio ต้องคงที่ตลอดการหมุน",
                     font_size=21, color=WHITE).next_to(VGroup(g1, g2), UP, buff=0.65)
        formula = MathTex(r"\frac{\omega_1}{\omega_2}=\frac{N_2}{N_1}",
                            font_size=32, color=WHITE).next_to(goal, RIGHT, buff=0.6)
        self.play(FadeIn(goal, shift=UP * 0.15), FadeIn(formula, shift=UP * 0.15))
        self.wait(1.2)

        g1.clear_updaters(); g2.clear_updaters()
        self.play(FadeOut(VGroup(g1, g2, l1, l2, goal, formula, cap)))

        # --- แยก 2 คำ: average vs instantaneous ------------------------------
        cap2 = caption_top("แยกให้ออก 2 คำนี้ -- ออกสอบเป็นข้อความ", size=23)
        self.play(FadeIn(cap2))

        axes = Axes(x_range=[0, TAU, PI / 2], y_range=[0, 3.0, 1.0],
                    x_length=8.6, y_length=3.6,
                    axis_config={"color": GRAYTXT, "stroke_width": 2,
                                 "include_tip": False})
        axes.move_to(DOWN * 0.75)
        xlab = Text("เวลา (1 รอบขบฟัน)", font_size=17, color=GRAYTXT).next_to(
            axes.c2p(TAU, 0), DOWN, buff=0.35)
        ylab = Text("อัตราทด ณ ขณะนั้น", font_size=17, color=GRAYTXT).next_to(
            axes, LEFT, buff=0.25).rotate(PI / 2)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab))

        avg_line = axes.plot(lambda x: 1.667, color=PITCH_C, stroke_width=4)
        avg_lbl = Text("เฉลี่ย = N2/N1 (คงที่เสมอ)", font_size=18, color=PITCH_C).next_to(
            axes.c2p(TAU * 0.62, 1.667), UP, buff=0.18)
        self.play(Create(avg_line), FadeIn(avg_lbl))
        self.wait(0.8)

        bad_curve = axes.plot(lambda x: 1.667 + 0.55 * np.sin(3 * x), color=WARN,
                               stroke_width=4)
        bad_lbl = Text("ขณะหนึ่ง (ถ้ารูปฟันไม่ดี) -- กระตุก", font_size=18,
                        color=WARN).next_to(axes.c2p(TAU * 0.22, 2.35), UP, buff=0.12)
        illus = Text("(กราฟนี้คือภาพประกอบแนวคิด ไม่ใช่ข้อมูลจริง)", font_size=15,
                      color=GRAYTXT).next_to(bad_lbl, DOWN, buff=0.08)
        self.play(Create(bad_curve), FadeIn(bad_lbl), FadeIn(illus))
        self.wait(1.6)

        concl = Text("ฟันจำนวนเท่ากันให้อัตราทดเฉลี่ยเท่ากันเสมอ -- "
                      "แต่รูปฟันผิดจะทำให้ขณะหนึ่งกระตุก = สั่น เสียงดัง ฟันสึก",
                      font_size=19, color=OK).move_to([0, -3.15, 0])
        self.play(FadeIn(concl, shift=UP * 0.15))
        self.wait(2.0)


# =====================================================================
# G03 -- หน้า 4: คำถามตั้งต้นของทั้งบท
# =====================================================================
class G03_CentralQuestion(SafeScene):
    def construct(self):
        self.add(page_ref("หน้า 4"))
        q = Text('"What shape should a gear tooth have?"',
                  font_size=34, color=WHITE)
        q.move_to(UP * 1.0)
        self.play(FadeIn(q, shift=UP * 0.4))
        self.wait(1.0)

        # ไอคอนฟันที่ยังไม่รู้รูปร่าง -- เส้นประร่างฟันคลุมเครือ + เครื่องหมายคำถาม
        blob = VMobject(color=GRAYTXT, stroke_width=3)
        blob.set_points_smoothly([
            [-0.6, -0.9, 0], [-0.5, -0.2, 0], [-0.15, 0.55, 0],
            [0.2, 0.6, 0], [0.55, -0.1, 0], [0.6, -0.9, 0],
        ])
        qmark = Text("?", font_size=52, color=WARN).move_to(blob.get_center() + UP * 0.1)
        icon = VGroup(blob, qmark).move_to(DOWN * 1.4)
        self.play(Create(blob), run_time=0.9)
        self.play(FadeIn(qmark, shift=UP * 0.2))
        self.wait(1.0)

        cap = Text("หน้า 5-8 ตอบคำถามนี้ทีละก้าว -- ไม่ใช่ท่องว่า \"ใช้อินโวลูท\" เฉยๆ",
                    font_size=21, color=OK).move_to([0, -3.15, 0])
        self.play(FadeIn(cap, shift=UP * 0.15))
        self.wait(1.8)


# =====================================================================
# G07 -- หน้า 7: Kennedy's Theorem + pitch circle / pitch point
# =====================================================================
class G07_KennedyPitchPoint(SafeScene):
    def construct(self):
        self.add(title("Kennedy's Theorem + Pitch Point / Pitch Circle", size=25))
        self.add(page_ref("หน้า 7"))

        R1, R2 = 1.6, 1.05
        O1 = LEFT * 1.8
        O2 = O1 + RIGHT * (R1 + R2)
        P = O1 + RIGHT * R1

        cap = caption_top("จากบทที่แล้ว: จุดสัมผัสไถล -> IC ทั้งคู่อยู่บน line of centers", size=21)
        self.play(FadeIn(cap))

        c1 = Circle(radius=R1, color=GEAR2, stroke_width=4).move_to(O1)
        c2 = Circle(radius=R2, color=GEAR3, stroke_width=4).move_to(O2)
        loc = DashedLine(O1 + LEFT * 0.5, O2 + RIGHT * 0.5, color=GRAYTXT, stroke_width=2.5)
        lA = tag("A", O1, UP, GEAR2, 24)
        lB = tag("B", O2, UP, GEAR3, 24)
        self.play(Create(loc), FadeIn(lA), FadeIn(lB))
        self.play(Create(c1), Create(c2))
        self.wait(0.6)

        dP = pt(P, WHITE, 0.09)
        tP = tag("P", P, DOWN, WHITE, 26, 0.14)
        self.play(FadeIn(dP), Flash(P, color=WHITE, flash_radius=0.4), FadeIn(tP))
        self.wait(0.6)

        cap2 = caption_top("Kennedy: IC12(=A), IC13(=B), IC23 ต้อง collinear บนเส้นนี้", size=21)
        self.play(FadeOut(cap), FadeIn(cap2))
        self.wait(0.8)

        cap3 = caption_top("หน้าที่แล้วพิสูจน์แล้วว่า contact normal ตัดเส้นนี้ที่ P พอดี "
                             "=> IC23 = P", size=21)
        self.play(FadeOut(cap2), FadeIn(cap3))
        self.wait(1.0)

        # ---- ตารางศัพท์ -----------------------------------------------------
        self.play(FadeOut(cap3))
        table = VGroup(
            Text("Pitch point (P) = IC23", font_size=20, color=WHITE),
            Text("Pitch circle = วงกลมรัศมี AP, BP", font_size=20, color=PITCH_C),
            Text("Line of action = เส้น contact normal", font_size=20, color=LOA_C),
            Text("Rolling point = อีกชื่อของ pitch point", font_size=20, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        table.to_edge(RIGHT, buff=0.7).shift(UP * 0.3)
        for row in table:
            self.play(FadeIn(row, shift=LEFT * 0.2), run_time=0.5)
        self.wait(1.2)

        # ---- pitch circles กลิ้งบนกัน ----------------------------------------
        cap4 = caption_top("ถ้า P นิ่ง -> เฟืองสองตัวประพฤติเหมือนลูกกลิ้ง 2 อันกลิ้งบนกัน", size=21)
        self.play(FadeIn(cap4))
        tick1 = Line(O1, O1 + UP * R1, color=GEAR2, stroke_width=3)
        tick2 = Line(O2, O2 + UP * R2, color=GEAR3, stroke_width=3)
        self.play(Create(tick1), Create(tick2))
        spin(VGroup(tick1), -1.6)
        spin(VGroup(tick2), 1.6 * (R1 / R2))
        self.wait(1.8)

        formula = MathTex(
            r"\frac{\omega_1}{\omega_2}=\frac{R_2}{R_1}=\frac{N_2}{N_1}",
            font_size=30, color=WHITE).move_to([0, -3.15, 0])
        self.play(FadeOut(cap4), FadeIn(formula, shift=UP * 0.15))
        self.wait(1.8)

        tick1.clear_updaters(); tick2.clear_updaters()


# =====================================================================
# G08 -- หน้า 8: Conjugate profiles
# =====================================================================
class G08_ConjugateProfiles(SafeScene):
    def construct(self):
        self.add(title("Conjugate Profiles", size=30))
        self.add(page_ref("หน้า 8"))

        O1 = LEFT * 1.8
        O2 = RIGHT * 0.85
        P = ORIGIN + LEFT * 0.475  # แสดงสัญลักษณ์อย่างเดียว ไม่ต้องตรงระยะจริงกับ G07

        loc = DashedLine(O1 + LEFT * 0.6, O2 + RIGHT * 0.6, color=GRAYTXT, stroke_width=2.5)
        dP = pt(P, WHITE, 0.09)
        tPl = tag("P (นิ่งตลอดเวลา)", P, DOWN, WHITE, 20, 0.16)
        cap = caption_top("เพื่อให้เคลื่อนที่เรียบ contact normal ต้องผ่านจุด P เสมอ", size=22)
        self.play(FadeIn(cap))
        self.play(Create(loc), FadeIn(dP), FadeIn(tPl))
        self.wait(0.8)

        # 3 สแนปช็อตของจุดสัมผัส Q ที่ตำแหน่งต่างกัน แต่เส้นปกติทุกเส้นผ่าน P เสมอ
        offsets = [np.array([0.35, 1.05, 0]), np.array([-0.15, 0.35, 0]),
                    np.array([0.15, -0.95, 0])]
        colors = [GEAR2, OK, GEAR3]
        labels = ["t1", "t2", "t3"]
        groups = VGroup()
        for i, (off, c, lb) in enumerate(zip(offsets, colors, labels)):
            Q = P + off
            direction = (Q - P) / np.linalg.norm(Q - P)
            n_line = Line(P - direction * 0.4, Q + direction * 0.75, color=c, stroke_width=3.5)
            dQ = pt(Q, c, 0.07)
            tQ = tag(lb, Q, direction, c, 18, 0.18)
            # ขีดสั้นตั้งฉากที่ Q แทนผิวสัมผัสสองชิ้น ณ ขณะนั้น (สัมผัสกันที่ Q)
            perp = np.array([-direction[1], direction[0], 0]) * 0.28
            flank = Line(Q - perp, Q + perp, color=GRAYTXT, stroke_width=3)
            grp = VGroup(n_line, dQ, tQ, flank)
            groups.add(grp)
            cap2 = caption_top(f"ขณะ {lb}: จุดสัมผัสอยู่ที่ Q -- ลาก normal ผ่าน Q กับ P", size=20)
            self.play(FadeOut(cap) if i == 0 else FadeOut(cap2_prev), FadeIn(cap2))
            self.play(Create(n_line), FadeIn(dQ), FadeIn(tQ), Create(flank))
            self.wait(0.7)
            cap2_prev = cap2

        cap3 = caption_top("ทุกขณะ normal ทิศต่างกัน แต่ 'ผ่าน P' เหมือนกันหมด", size=21)
        self.play(FadeOut(cap2_prev), FadeIn(cap3))
        self.wait(1.2)

        cap4 = caption_top("รู้รูปฟันตัวหนึ่ง -> ออกแบบรูปฟันอีกตัวให้เงื่อนไขนี้จริงได้เสมอ = conjugate",
                            size=20)
        self.play(FadeOut(cap3), FadeIn(cap4))
        self.wait(1.2)

        box_txt = MathTex(r"\text{conjugate teeth} \Rightarrow \text{constant angular velocity ratio}",
                           font_size=26, color=WHITE).move_to(UP * 2.6)
        box = SurroundingRectangle(box_txt, color=OK, buff=0.2)
        self.play(FadeIn(box_txt, shift=DOWN * 0.15), Create(box))
        self.wait(2.0)


# =====================================================================
# G09 -- หน้า 9: ทำไมเลือกอินโวลูท + อุปมาสายพานไขว้
# =====================================================================
class G09_WhyInvolute(SafeScene):
    def construct(self):
        self.add(title("ทำไมเลือก \"อินโวลูท\"", size=30))
        self.add(page_ref("หน้า 9"))

        PHI0 = 20 * DEGREES
        R1_0, R2_0 = 1.75, 1.15
        fr = loa_frame(PHI0, R1_0, R2_0, sign=1.0)
        Rb1, Rb2 = fr["Rb1"], fr["Rb2"]
        shift = LEFT * 1.5  # จัดให้อยู่กลางเวทีมากขึ้น
        O1_0, O2_0 = fr["O1"] + shift, fr["O2"] + shift

        cap = caption_top("อินโวลูทคือ conjugate profile ที่นิยมที่สุด", size=22)
        self.play(FadeIn(cap))
        adv = Text("ข้อได้เปรียบเด็ด: อัตราทดคงที่แม้ระยะศูนย์กลาง (C) เปลี่ยนไป",
                    font_size=20, color=OK).move_to([0, -3.15, 0])
        self.play(FadeIn(adv, shift=UP * 0.15))
        self.wait(1.2)

        cap2 = caption_top("อุปมา: พูลเลย์ 2 ตัว (= base circle) มีสายพานไขว้พันอยู่", size=22)
        self.play(FadeOut(cap), FadeIn(cap2))

        c1 = Circle(radius=Rb1, color=GEAR2, stroke_width=4).move_to(O1_0)
        c2 = Circle(radius=Rb2, color=GEAR3, stroke_width=4).move_to(O2_0)
        l1 = tag("base circle 1", O1_0 + DOWN * (Rb1 + 0.3), DOWN, GEAR2, 17)
        l2 = tag("base circle 2", O2_0 + DOWN * (Rb2 + 0.3), DOWN, GEAR3, 17)
        self.play(Create(c1), Create(c2), FadeIn(l1), FadeIn(l2))
        self.wait(0.5)

        # เส้นสัมผัสไขว้ (crossed belt) -- ใช้ 2 เส้นสัมผัสภายใน + โค้งอ้อมหลังพูลเลย์
        d_plus = np.array([np.sin(PHI0), np.cos(PHI0), 0.0])
        d_minus = np.array([-np.sin(PHI0), np.cos(PHI0), 0.0])
        Pp = fr["P"] + shift
        E1p = Pp + float(np.dot(O1_0 - Pp, d_plus)) * d_plus
        E2p = Pp + float(np.dot(O2_0 - Pp, d_plus)) * d_plus
        E1m = Pp + float(np.dot(O1_0 - Pp, d_minus)) * d_minus
        E2m = Pp + float(np.dot(O2_0 - Pp, d_minus)) * d_minus

        a1p, a1m = ang_of(E1p, O1_0), ang_of(E1m, O1_0)
        a2p, a2m = ang_of(E2p, O2_0), ang_of(E2m, O2_0)
        s1a, s1s = far_arc(O1_0, Rb1, a1p, a1m, O2_0)
        s2a, s2s = far_arc(O2_0, Rb2, a2p, a2m, O1_0)

        belt_line1 = Line(E1p, E2p, color=WHITE, stroke_width=3.5)
        belt_line2 = Line(E1m, E2m, color=WHITE, stroke_width=3.5)
        belt_arc1 = Arc(radius=Rb1, start_angle=s1a, angle=s1s, arc_center=O1_0,
                        color=WHITE, stroke_width=3.5)
        belt_arc2 = Arc(radius=Rb2, start_angle=s2a, angle=s2s, arc_center=O2_0,
                        color=WHITE, stroke_width=3.5)
        belt = VGroup(belt_line1, belt_arc1, belt_line2, belt_arc2)
        cap3 = caption_top("สายพาน = line of action -- ตรึงอยู่กับที่เสมอ", size=22)
        self.play(FadeOut(cap2), FadeIn(cap3))
        self.play(Create(belt), run_time=1.6)
        self.wait(1.0)

        loc_tag = tag("line of action", (E1p + E2p) / 2, UP, WHITE, 17, 0.15)
        self.play(FadeIn(loc_tag))
        self.wait(1.0)

        # ---- แสดงว่าอัตราทดคงที่แม้ C เปลี่ยน -----------------------------------
        self.play(FadeOut(VGroup(cap3, loc_tag, l1, l2, adv)))
        cap4 = caption_top("ลองยืดระยะศูนย์กลาง C ออก -- ดูว่าอัตราทดเปลี่ยนไหม", size=22)
        self.play(FadeIn(cap4))

        Ct = ValueTracker(fr["C"])
        O1_fix = O1_0

        def get_O2():
            return O1_fix + RIGHT * Ct.get_value()

        def get_P():
            return O1_fix + RIGHT * (Ct.get_value() * Rb1 / (Rb1 + Rb2))

        def get_phi():
            return float(np.arccos((Rb1 + Rb2) / Ct.get_value()))

        c2_dyn = always_redraw(lambda: Circle(radius=Rb2, color=GEAR3, stroke_width=4)
                                .move_to(get_O2()))
        loa_dyn = always_redraw(lambda: Line(
            get_P() - np.array([np.sin(get_phi()), np.cos(get_phi()), 0]) * 1.6,
            get_P() + np.array([np.sin(get_phi()), np.cos(get_phi()), 0]) * 1.6,
            color=LOA_C, stroke_width=4))
        p_dyn = always_redraw(lambda: Dot(get_P(), color=WHITE, radius=0.08))

        self.remove(c2)
        self.play(FadeIn(c2_dyn), FadeIn(loa_dyn), FadeIn(p_dyn), FadeOut(belt))

        ratio_row = live_row("R1'/R2' =", "(= Rb1/Rb2 เสมอ)",
                              lambda: (Ct.get_value() * Rb1 / (Rb1 + Rb2)) /
                                      (Ct.get_value() * Rb2 / (Rb1 + Rb2)),
                              anchor=[-4.3, 2.3, 0], decimals=3, num_color=OK)
        phi_row = live_row("pressure angle phi' =", "deg",
                            lambda: get_phi() / DEGREES,
                            anchor=[-4.3, 1.75, 0], decimals=1, num_color=WARN)
        self.play(FadeIn(ratio_row), FadeIn(phi_row))
        self.wait(0.8)

        self.play(Ct.animate.set_value(fr["C"] * 1.35), run_time=3.0, rate_func=smooth)
        self.wait(1.0)

        concl = Text("Rb ไม่เปลี่ยน -> อัตราทด = Rb2/Rb1 ไม่เปลี่ยน แม้ C และ phi' เปลี่ยนไป",
                      font_size=20, color=OK).move_to([0, -3.15, 0])
        self.play(FadeOut(cap4), FadeIn(concl, shift=UP * 0.15))
        self.wait(2.2)


# =====================================================================
# G10 -- หน้า 10: เส้นโค้งอินโวลูทเกิดขึ้นได้อย่างไร
# =====================================================================
class G10_InvoluteGenesis(SafeScene):
    def construct(self):
        self.add(title("เส้นโค้งอินโวลูทเกิดขึ้นได้อย่างไร", size=27))
        self.add(page_ref("หน้า 10"))

        Rb = 1.2
        O = DOWN * 0.4
        cap = caption_top("อินโวลูท = เส้นทางของจุดบนสายพานที่ถูกคลี่ออกจากพูลเลย์", size=21)
        self.play(FadeIn(cap))

        circ = Circle(radius=Rb, color=BASE_C, stroke_width=4).move_to(O)
        lO = tag("O", O, DOWN, WHITE, 20, 0.15)
        self.play(Create(circ), FadeIn(lO))
        self.wait(0.5)

        def inv_point(t):
            return O + Rb * np.array([np.cos(t) + t * np.sin(t),
                                       np.sin(t) - t * np.cos(t), 0.0])

        t_tracker = ValueTracker(0.05)
        string_line = always_redraw(lambda: Line(
            O + Rb * np.array([np.cos(t_tracker.get_value()), np.sin(t_tracker.get_value()), 0]),
            inv_point(t_tracker.get_value()), color=WHITE, stroke_width=3))
        tip_dot = always_redraw(lambda: Dot(inv_point(t_tracker.get_value()),
                                             color=INVOL_C, radius=0.07))
        traced = TracedPath(lambda: inv_point(t_tracker.get_value()),
                             stroke_color=INVOL_C, stroke_width=4)

        self.add(traced)
        self.play(FadeIn(string_line), FadeIn(tip_dot))
        cap2 = caption_top("ปลายสายพาน (จุดสีเขียว) คลี่ออกทีละนิด -> ลากรอยทาง = อินโวลูท", size=20)
        self.play(FadeOut(cap), FadeIn(cap2))
        self.play(t_tracker.animate.set_value(2.0), run_time=4.5, rate_func=linear)
        self.wait(0.8)

        rho_note = Text("รูปร่างของอินโวลูทขึ้นกับขนาดของ base circle เท่านั้น",
                          font_size=20, color=OK).move_to([0, -3.15, 0])
        self.play(FadeOut(cap2), FadeIn(rho_note, shift=UP * 0.15))
        self.wait(1.4)

        string_line.clear_updaters(); tip_dot.clear_updaters()
        self.play(FadeOut(VGroup(string_line, tip_dot, traced, circ, lO, rho_note)))

        # ---- กับดัก: base circle เล็ก vs ใหญ่อนันต์ -----------------------------
        cap3 = caption_top("กับดักข้อสอบ: ขนาด base circle มีผลต่อความโค้งของฟันโดยตรง", size=21)
        self.play(FadeIn(cap3))

        # เล็ก -> โค้งมาก
        small_R = 0.55
        small_O = LEFT * 3.4 + DOWN * 0.3
        small_c = Circle(radius=small_R, color=BASE_C, stroke_width=3).move_to(small_O)
        small_curve = ParametricFunction(
            lambda t: small_O + small_R * np.array(
                [np.cos(t) + t * np.sin(t), np.sin(t) - t * np.cos(t), 0.0]),
            t_range=[0.05, 2.6], color=INVOL_C, stroke_width=4)
        small_lbl = Text("base circle เล็ก\n=> ฟันโค้งมากขึ้น", font_size=18, color=GRAYTXT,
                          line_spacing=0.9).next_to(small_O, DOWN, buff=1.1)

        # ใหญ่ (จำลองด้วยรัศมีใหญ่กว่ามาก) -> เกือบเป็นเส้นตรง = rack
        big_R = 7.0
        big_O = RIGHT * 3.0 + DOWN * (big_R - 1.3)
        big_curve = ParametricFunction(
            lambda t: big_O + big_R * np.array(
                [np.cos(t) + t * np.sin(t), np.sin(t) - t * np.cos(t), 0.0]),
            t_range=[0.05, 0.62], color=INVOL_C, stroke_width=4)
        big_lbl = Text("base circle ใหญ่อนันต์\n=> อินโวลูทเป็นเส้นตรง = ฟัน rack",
                        font_size=18, color=GRAYTXT, line_spacing=0.9).move_to(RIGHT * 3.0 + DOWN * 1.1)

        self.play(Create(small_c), Create(small_curve), FadeIn(small_lbl, shift=UP * 0.15))
        self.wait(0.8)
        self.play(Create(big_curve), FadeIn(big_lbl, shift=UP * 0.15))
        self.wait(2.0)


# =====================================================================
# G11 -- หน้า 11: Involutometry -- สมการหาจุดใดๆ บนอินโวลูท
# =====================================================================
class G11_Involutometry(SafeScene):
    def construct(self):
        self.add(title("Involutometry -- สมการของจุดบนอินโวลูท", size=26))
        self.add(page_ref("หน้า 11"))

        Rb = 1.2
        O = DOWN * 0.4 + LEFT * 1.2
        R_A = 1.9
        phi_A = float(np.arccos(Rb / R_A))
        rho_A = Rb * np.tan(phi_A)
        theta_A = np.tan(phi_A) - phi_A
        t_A = np.tan(phi_A)  # = theta_A + phi_A, พารามิเตอร์บนเส้นโค้งเดียวกับ G10

        def inv_pt(t):
            return O + Rb * np.array([np.cos(t) + t * np.sin(t),
                                       np.sin(t) - t * np.cos(t), 0.0])

        cap = caption_top("ต่อจากคลิปที่แล้ว -- เอาเส้นโค้งเดิมมาวัดตำแหน่งจุด A ให้แม่นยำ", size=20)
        self.play(FadeIn(cap))

        circ = Circle(radius=Rb, color=BASE_C, stroke_width=4).move_to(O)
        curve = ParametricFunction(inv_pt, t_range=[0.02, t_A + 0.35],
                                    color=INVOL_C, stroke_width=4)
        self.play(Create(circ), Create(curve), run_time=1.2)
        lO = tag("O", O, DOWN, WHITE, 20, 0.15)
        self.play(FadeIn(lO))
        self.wait(0.5)

        C_pt = O + Rb * np.array([np.cos(t_A), np.sin(t_A), 0.0])  # จุดสัมผัสบน base circle
        A_pt = inv_pt(t_A)
        B_pt = O + Rb * np.array([1.0, 0.0, 0.0])  # จุดเริ่มต้นของอินโวลูท (t=0)

        dA = pt(A_pt, INVOL_C, 0.08)
        tA = tag("A", A_pt, UR, INVOL_C, 24, 0.14)
        self.play(FadeOut(cap))
        cap2 = caption_top("A = จุดบนอินโวลูทที่รัศมี R_A จากศูนย์กลาง O", size=20)
        self.play(FadeIn(cap2), FadeIn(dA), FadeIn(tA))
        self.wait(0.6)

        line_OA = seg(O, A_pt, GRAYTXT, 3)
        self.play(Create(line_OA))
        self.wait(0.4)

        dC = pt(C_pt, BASE_C, 0.07)
        tC = tag("C", C_pt, LEFT, BASE_C, 20, 0.12)
        line_OC = seg(O, C_pt, BASE_C, 3)
        line_CA = seg(C_pt, A_pt, WARN, 4)
        cap3 = caption_top("C = จุดสัมผัสของเส้นสัมผัส CA กับ base circle (มุมฉากที่ C)", size=20)
        self.play(FadeOut(cap2), FadeIn(cap3))
        self.play(FadeIn(dC), FadeIn(tC), Create(line_OC), Create(line_CA))
        ra = ra_mark(C_pt, O - C_pt, A_pt - C_pt, GRAYTXT, 0.22)
        self.play(Create(ra))
        self.wait(0.8)

        ang_phi = Angle(Line(O, A_pt), Line(O, C_pt), radius=0.55, color=WARN, stroke_width=4)
        lbl_phi = MathTex(r"\phi_A", font_size=26, color=WARN).move_to(
            O + normalize(normalize(A_pt - O) + normalize(C_pt - O)) * 0.85)
        cap4 = caption_top(r"phi_A = มุม AOC: cos(phi_A) = Rb/R_A", size=20)
        self.play(FadeOut(cap3), FadeIn(cap4))
        self.play(Create(ang_phi), FadeIn(lbl_phi))
        self.wait(1.0)

        lbl_CA = tag("rho_A = CA = Rb tan(phi_A)", C_pt + (A_pt - C_pt) * 0.5,
                     RIGHT, WARN, 17, 0.15)
        self.play(FadeIn(lbl_CA))
        self.wait(0.8)

        # ---- ส่วนโค้ง BC บน base circle -----------------------------------------
        dB = pt(B_pt, GRAYTXT, 0.06)
        tB = tag("B", B_pt, DOWN, GRAYTXT, 18, 0.12)
        arc_BC = Arc(radius=Rb, start_angle=0, angle=t_A, arc_center=O,
                     color=OK, stroke_width=5)
        cap5 = caption_top("B = จุดเริ่มอินโวลูท (t=0) -- ส่วนโค้ง BC ยาวเท่ากับสายพานที่คลี่ (rho_A)", size=19)
        self.play(FadeOut(cap4), FadeIn(cap5))
        self.play(FadeIn(dB), FadeIn(tB), Create(arc_BC))
        self.wait(1.0)

        ang_theta = Angle(Line(O, B_pt), Line(O, C_pt), radius=0.42, color=OK, stroke_width=3,
                          other_angle=False)
        lbl_theta = MathTex(r"\theta_A", font_size=22, color=OK).move_to(
            O + normalize(normalize(B_pt - O) + normalize(C_pt - O)) * 0.62)
        self.play(Create(ang_theta), FadeIn(lbl_theta))
        self.wait(1.0)

        cap6 = caption_top("สายพานไม่ยืด: ส่วนโค้ง BC = ความยาวที่คลี่ออก CA พอดี", size=20)
        self.play(FadeOut(cap5), FadeIn(cap6))
        self.wait(1.0)

        eqs = VGroup(
            MathTex(r"\rho_A = R_b\tan\phi_A", font_size=26, color=WHITE),
            MathTex(r"\rho_A = R_b(\theta_A+\phi_A)", font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        self.play(FadeIn(eqs[0], shift=RIGHT * 0.2))
        self.wait(0.6)
        self.play(FadeIn(eqs[1], shift=RIGHT * 0.2))
        self.wait(1.0)

        result = MathTex(r"\theta_A=\tan\phi_A-\phi_A \equiv \operatorname{inv}\phi_A",
                          font_size=28, color=OK).next_to(eqs, DOWN, buff=0.4)
        box = SurroundingRectangle(result, color=OK, buff=0.18)
        self.play(FadeOut(cap6), FadeIn(result, shift=UP * 0.15), Create(box))
        self.wait(1.2)

        result2 = MathTex(r"\phi_A=\cos^{-1}\frac{R_b}{R_A}",
                           font_size=26, color=OK).next_to(result, DOWN, buff=0.35)
        self.play(FadeIn(result2, shift=UP * 0.1))
        self.wait(2.0)


# =====================================================================
# G12 -- หน้า 12: ความหนาฟันที่รัศมีใดๆ (Involutometry ภาค 2)
# =====================================================================
class G12_ToothThickness(SafeScene):
    def construct(self):
        self.add(title("ความหนาฟันที่รัศมีใดๆ", size=28))
        self.add(page_ref("หน้า 12"))

        cap = caption_top("ยิ่งออกไปไกลจากศูนย์กลาง ฟันยิ่ง 'บาง' ลง เพราะผิวโค้งบิดออกทีละนิด", size=21)
        self.play(FadeIn(cap))

        O = DOWN * 0.3
        Rb, R_B, R_A = 0.9, 1.5, 2.3

        c_base = Circle(radius=Rb, color=BASE_C, stroke_width=2.5)
        c_b = Circle(radius=R_B, color=GEAR2, stroke_width=2.5)
        c_a = Circle(radius=R_A, color=GEAR3, stroke_width=2.5)
        for c in (c_base, c_b, c_a):
            c.move_to(O)
        self.play(Create(c_base), Create(c_b), Create(c_a))
        lbls = VGroup(
            tag("base circle", O + UP * Rb, UP, BASE_C, 15, 0.1),
            tag("รัศมี B (ใกล้)", O + UP * R_B, UP, GEAR2, 16, 0.1),
            tag("รัศมี A (ไกล)", O + UP * R_A, UP, GEAR3, 16, 0.1),
        )
        self.play(FadeIn(lbls))
        self.wait(0.8)

        # ครึ่งมุมฟันที่รัศมี B (กว้าง) เทียบกับที่รัศมี A (แคบกว่า เพราะบิดไป theta)
        delta_B = 24 * DEGREES
        delta_A = 15 * DEGREES  # เพียงตัวอย่างประกอบภาพ (แคบกว่าเพราะ +theta_A)
        wedge_B = VGroup(
            Line(O, O + R_B * np.array([np.cos(delta_B), np.sin(delta_B), 0]),
                 color=GEAR2, stroke_width=3),
            Line(O, O + R_B * np.array([np.cos(-delta_B), np.sin(-delta_B), 0]),
                 color=GEAR2, stroke_width=3),
        )
        wedge_A = VGroup(
            Line(O, O + R_A * np.array([np.cos(delta_A), np.sin(delta_A), 0]),
                 color=GEAR3, stroke_width=3),
            Line(O, O + R_A * np.array([np.cos(-delta_A), np.sin(-delta_A), 0]),
                 color=GEAR3, stroke_width=3),
        )
        arc_tB = Arc(radius=R_B, start_angle=-delta_B, angle=2 * delta_B, arc_center=O,
                     color=GEAR2, stroke_width=6)
        arc_tA = Arc(radius=R_A, start_angle=-delta_A, angle=2 * delta_A, arc_center=O,
                     color=GEAR3, stroke_width=6)
        self.play(Create(wedge_B), Create(arc_tB))
        t_b_lbl = tag("t_b (ความหนาที่ B)", O + R_B * RIGHT, RIGHT, GEAR2, 16, 0.12)
        self.play(FadeIn(t_b_lbl))
        self.wait(0.8)
        self.play(Create(wedge_A), Create(arc_tA))
        t_a_lbl = tag("t_A (ความหนาที่ A -- แคบกว่า)", O + R_A * RIGHT, RIGHT, GEAR3, 16, 0.12)
        self.play(FadeIn(t_a_lbl))
        self.wait(1.2)

        cap2 = caption_top("ครึ่งมุมฟัน delta_A = t_A/(2 R_A) = t_b/(2 R_b) - theta_A", size=20)
        self.play(FadeOut(cap), FadeIn(cap2))
        self.wait(1.0)

        theta_row = VGroup(
            MathTex(r"\theta_A=\tan\phi_A-\phi_A", font_size=22, color=GRAYTXT),
            Text("(แทนค่าจากคลิปก่อน)", font_size=18, color=GRAYTXT),
        ).arrange(RIGHT, buff=0.25)
        deriv = VGroup(
            MathTex(r"\delta_A=\frac{t_A}{2R_A}=\frac{t_b}{2R_b}-\theta_A",
                    font_size=26, color=WHITE),
            theta_row,
            MathTex(r"t_A=2R_A\!\left(\frac{t_B}{2R_B}-\tan\phi_A+\phi_A+\tan\phi_B-\phi_B\right)",
                    font_size=24, color=OK),
        ).arrange(DOWN, buff=0.32).to_edge(DOWN, buff=0.55).shift(UP*0.3)
        box = SurroundingRectangle(deriv[2], color=OK, buff=0.15)
        self.play(FadeOut(cap2))
        for row in deriv:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.7)
            self.wait(0.7)
        self.play(Create(box))
        self.wait(1.2)

        warn = Text("phi_A, phi_B ในวงเล็บต้องเป็นเรเดียน (บวกกับ theta ที่เป็นมุมส่วนโค้ง)",
                     font_size=18, color=WARN).move_to([0, -3.15, 0])
        self.play(FadeIn(warn, shift=UP * 0.15))
        self.wait(2.0)


# =====================================================================
# G13 -- หน้า 13: เฟืองคู่ที่ขบกัน -- line of action, path of contact, pressure angle
# =====================================================================
class G13_LineOfAction(SafeScene):
    def construct(self):
        self.add(title("Line of Action, Path of Contact, Pressure Angle", size=24))
        self.add(page_ref("หน้า 13"))

        PHI0 = 20 * DEGREES
        fr = loa_frame(PHI0, 1.75, 1.15, sign=1.0)
        shift = LEFT * 1.3
        O1, O2, P = fr["O1"] + shift, fr["O2"] + shift, fr["P"] + shift
        E1, E2 = fr["E1"] + shift, fr["E2"] + shift
        Rb1, Rb2 = fr["Rb1"], fr["Rb2"]
        R1, R2 = fr["R1"], fr["R2"]

        cap = caption_top("3 ข้อสรุปที่ต้องจำ -- มาดูทีละข้อบนรูปเดียวกัน", size=21)
        self.play(FadeIn(cap))

        pitch1 = Circle(radius=R1, color=PITCH_C, stroke_width=2.5).move_to(O1)
        pitch2 = Circle(radius=R2, color=PITCH_C, stroke_width=2.5).move_to(O2)
        base1 = Circle(radius=Rb1, color=BASE_C, stroke_width=3.5).move_to(O1)
        base2 = Circle(radius=Rb2, color=BASE_C, stroke_width=3.5).move_to(O2)
        loc = DashedLine(O1 + LEFT * 0.5, O2 + RIGHT * 0.5, color=GRAYTXT, stroke_width=2)
        self.play(Create(pitch1), Create(pitch2), FadeIn(
            tag("pitch circles", O1 + UP * R1, UP, PITCH_C, 15, 0.08)))
        self.play(Create(loc))
        self.wait(0.4)
        self.play(Create(base1), Create(base2), FadeIn(
            tag("base circles", O2 + DOWN * (Rb2 + 0.25), DOWN, BASE_C, 15, 0.08)))
        self.wait(0.6)

        cap2 = caption_top("1) Line of action ถูกกำหนดโดย base circle ทั้งสอง + ระยะศูนย์กลาง C", size=19)
        self.play(FadeOut(cap), FadeIn(cap2))
        loa = Line(E1 - (E2 - E1) * 0.25, E2 + (E2 - E1) * 0.25, color=LOA_C, stroke_width=4)
        self.play(Create(loa))
        self.wait(0.8)

        cap3 = caption_top("2) Path of contact อยู่ตาม line of action = common tangent ของ base circle ทั้งสอง", size=19)
        self.play(FadeOut(cap2), FadeIn(cap3))
        dE1 = pt(E1, BASE_C, 0.07)
        dE2 = pt(E2, BASE_C, 0.07)
        tE1 = tag("E1", E1, LEFT, BASE_C, 18, 0.12)
        tE2 = tag("E2", E2, RIGHT, BASE_C, 18, 0.12)
        self.play(FadeIn(dE1), FadeIn(dE2), FadeIn(tE1), FadeIn(tE2))
        self.wait(0.8)

        cap4 = caption_top("3) Pressure angle (phi) = มุมระหว่าง line of action กับเส้นตั้งฉากของ line of centers", size=19)
        self.play(FadeOut(cap3), FadeIn(cap4))
        vert = DashedLine(P + UP * 0.9, P + DOWN * 0.9, color=GRAYTXT, stroke_width=2)
        self.play(Create(vert))
        ang = Angle(vert, loa, radius=0.5, color=WARN, stroke_width=4)
        lbl_phi = MathTex(r"\phi", font_size=28, color=WARN).move_to(
            P + normalize(normalize(UP) + normalize(fr["d"])) * 0.85)
        self.play(Create(ang), FadeIn(lbl_phi))
        self.wait(1.0)

        formula = MathTex(r"R_b = R\cos\phi", font_size=28, color=WHITE).move_to([3.2, 1.9, 0])
        box = SurroundingRectangle(formula, color=OK, buff=0.15)
        self.play(FadeOut(cap4), FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(1.4)

        note = Text("phi ใหญ่ -> แรงกดเข้าแบริ่งมากขึ้น แต่ฟันแข็งแรงขึ้น (ตัดฟันน้อยได้ -- ดูหน้า 37)",
                     font_size=18, color=GRAYTXT).move_to([0, -3.15, 0])
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(2.2)
