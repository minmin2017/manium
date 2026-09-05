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


# ============================================================= G19-G25 frame
# ที่มา: Claude_Specs/Spur Gear Series Geometry Spec.md ข้อ 5 (แก้ไข 2026-09-05 --
# เวอร์ชันเดิมของสเปกเขียนทิศ A/B ผิด ยื่นออกนอก E1E2 ตรวจด้วยเลขจริงแล้วพบว่า Z ที่ได้
# (4.216) ไม่ตรงกับคำตอบในโน้ต (0.6255 in) ที่ถูกต้องคือ A, B อยู่ "ระหว่าง" E1 กับ E2
CR_PHI = 20 * DEGREES
CR_N1, CR_N2 = 24, 60                       # pinion / gear จำนวนฟัน (ตัวอย่างหน้า 25)
CR_R1_IN, CR_R2_IN = 1.5, 3.75              # รัศมีพิตช์จริง (นิ้ว)
CR_RO1_IN, CR_RO2_IN = 1.625, 3.875         # รัศมี addendum จริง (นิ้ว)


def zab_points(fr, Ro1, Ro2):
    """A = จุดเริ่มสัมผัส (บน addendum circle เฟือง 2/gear), B = จุดสิ้นสุดสัมผัส (บน
    addendum circle เฟือง 1/pinion) -- ทั้งคู่อยู่ "ระหว่าง" E1 กับ E2 เสมอถ้าไม่มี
    interference (หน้า 34) ตรวจด้วย assert ว่า |AB| ตรงกับสูตรกล่อง Z พอดี ก่อนคืนค่า"""
    E1, E2 = fr["E1"], fr["E2"]
    Rb1, Rb2 = fr["Rb1"], fr["Rb2"]
    u = (E2 - E1) / np.linalg.norm(E2 - E1)     # ทิศเดียวกับ fr["d"]
    E1B = float(np.sqrt(max(Ro1 ** 2 - Rb1 ** 2, 0.0)))
    E2A = float(np.sqrt(max(Ro2 ** 2 - Rb2 ** 2, 0.0)))
    B = E1 + u * E1B
    A = E2 - u * E2A
    E1E2 = float(np.linalg.norm(E2 - E1))
    Z = E1B + E2A - E1E2
    assert abs(np.linalg.norm(A - B) - Z) < 1e-6, (np.linalg.norm(A - B), Z)
    return dict(A=A, B=B, E1B=E1B, E2A=E2A, E1E2=E1E2, Z=Z)


def cr_wide(shift=None):
    """มุมกว้าง (บริบทเต็ม) -- สเกลลงจากตัวเลขจริงหน้า 25 ให้พอดีเฟรม ใช้กับ G19/G25
    ที่ต้องโชว์เฟืองทั้งคู่เป็นวงกลมเต็ม (ป้ายกำกับยังพูดถึงค่านิ้วจริงเสมอ ไม่ใช่ค่า
    scaled -- อ่านจาก CR_R1_IN ฯลฯ ตรงๆ เวลาทำสูตร/ตัวเลข)"""
    if shift is None:
        shift = np.array([-3.4, -0.15, 0.0])
    scale = 0.65
    R1, R2 = CR_R1_IN * scale, CR_R2_IN * scale
    Ro1, Ro2 = CR_RO1_IN * scale, CR_RO2_IN * scale
    fr = loa_frame(CR_PHI, R1, R2, sign=1.0)
    ab = zab_points(fr, Ro1, Ro2)
    fr.update(ab)
    fr["Ro1"], fr["Ro2"] = Ro1, Ro2
    fr["scale"] = scale
    for k in ("O1", "O2", "P", "E1", "E2", "A", "B"):
        fr[k] = fr[k] + shift
    return fr


def cr_local(shift=None):
    """มุมใกล้ (สเกลจริง 1:1 นิ้ว) -- ใช้กับ G20/G21_22/G23 ที่เน้นสามเหลี่ยมมุมฉาก
    รอบจุด E1/E2/P/A/B โดยตรง ไม่ต้องวาดวงกลมเฟืองทั้งวง (O2 ไกลเกินจะวาดวงเต็มได้พอดี
    เฟรม แต่ไม่จำเป็น -- ใช้แค่จุด O1,O2,P,E1,E2,A,B ในการวาดเส้น/สามเหลี่ยม)"""
    if shift is None:
        shift = np.array([-2.5, -0.3, 0.0])
    fr = loa_frame(CR_PHI, CR_R1_IN, CR_R2_IN, sign=1.0)
    ab = zab_points(fr, CR_RO1_IN, CR_RO2_IN)
    fr.update(ab)
    fr["Ro1"], fr["Ro2"] = CR_RO1_IN, CR_RO2_IN
    for k in ("O1", "O2", "P", "E1", "E2", "A", "B"):
        fr[k] = fr[k] + shift
    return fr


# =====================================================================
# G01 -- หน้า 1-2: ปกบท + สารบัญ
# =====================================================================
class G01_CoverAndToc(SafeScene):
    def construct(self):
        head = Text("บทที่ 4 -- เฟืองตรง (Spur Gears)", font_size=38, color=WHITE)
        sub = Text("ส่งกำลังระหว่างเพลาขนานกัน 2 เพลา", font_size=24, color=GRAYTXT)
        VGroup(head, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        self.play(FadeIn(head, shift=UP * 0.4))
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.0)
        self.play(FadeOut(head), FadeOut(sub))

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
                    x_length=7.6, y_length=2.7,
                    axis_config={"color": GRAYTXT, "stroke_width": 2,
                                 "include_tip": False})
        axes.move_to(LEFT * 1.1 + DOWN * 0.55)
        xlab = Text("เวลา (1 รอบขบฟัน)", font_size=16, color=GRAYTXT).next_to(
            axes.c2p(TAU, 0), DOWN, buff=0.55)
        ylab = Text("อัตราทด ณ ขณะนั้น", font_size=16, color=GRAYTXT).next_to(
            axes, LEFT, buff=0.3).rotate(PI / 2)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab))

        avg_line = axes.plot(lambda x: 1.667, color=PITCH_C, stroke_width=4)
        bad_curve = axes.plot(lambda x: 1.667 + 0.55 * np.sin(3 * x), color=WARN,
                               stroke_width=4)
        self.play(Create(avg_line))
        self.play(Create(bad_curve))
        self.wait(0.4)

        legend = VGroup(
            Text("เฉลี่ย = N2/N1 (คงที่เสมอ)", font_size=18, color=PITCH_C),
            Text("ขณะหนึ่ง (ถ้ารูปฟันไม่ดี) -- กระตุก", font_size=18, color=WARN),
            Text("(กราฟนี้คือภาพประกอบแนวคิด ไม่ใช่ข้อมูลจริง)", font_size=14, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        self.play(FadeIn(legend, shift=LEFT * 0.15))
        self.wait(1.6)

        concl = Text("ฟันจำนวนเท่ากันให้อัตราทดเฉลี่ยเท่ากันเสมอ --",
                      font_size=18, color=OK)
        concl2 = Text("แต่รูปฟันผิดจะทำให้ขณะหนึ่งกระตุก = สั่น เสียงดัง ฟันสึก",
                       font_size=18, color=OK)
        concl_grp = VGroup(concl, concl2).arrange(DOWN, buff=0.1).move_to([0, -3.35, 0])
        self.play(FadeIn(concl_grp, shift=UP * 0.15))
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
        lA = tag("A", O1, DOWN, GEAR2, 24, 0.22)
        lB = tag("B", O2, DOWN, GEAR3, 24, 0.22)
        self.play(Create(loc), FadeIn(lA), FadeIn(lB))
        self.play(Create(c1), Create(c2))
        self.wait(0.6)

        dP = pt(P, WHITE, 0.09)
        # รอบแรกเปลี่ยน RIGHT->UP แก้ปัญหาขนานกับ loc ได้ แต่ P เป็นจุดสัมผัสของ c1/c2
        # พอดี (รัศมีแนวนอนของทั้งคู่ = แทนเจนต์ที่ P เป็นแนวตั้ง) UP จึงวิ่งขนานเส้น
        # สัมผัสของวงกลมทั้งสองวงแทน (เจอจริงจาก [LAYOUT] log 2026-09-05 รอบสอง:
        # 'P' ทับ Circle x2) และ buff เดิม 0.30 < flash_radius 0.4 ทำให้ป้ายเข้าไปทับ
        # เส้นรัศมีชั่วคราวของ Flash ด้วย -- แก้โดยใช้ทิศทแยง UR (ไม่ขนานสิ่งใดเลย)
        # และเพิ่ม buff ให้เกิน flash_radius
        tP = tag("P", P, UR, WHITE, 26, 0.45)
        self.play(FadeIn(dP), Flash(P, color=WHITE, flash_radius=0.4), FadeIn(tP))
        self.wait(0.6)

        cap2 = caption_top("Kennedy: IC12(=A), IC13(=B), IC23 ต้อง collinear บนเส้นนี้", size=21)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        self.wait(0.8)

        cap3 = caption_top("หน้าที่แล้วพิสูจน์แล้วว่า contact normal ตัดเส้นนี้ที่ P พอดี "
                             "=> IC23 = P", size=21)
        self.play(FadeOut(cap2))
        self.play(FadeIn(cap3))
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
        self.play(FadeOut(cap4))
        self.play(FadeIn(formula, shift=UP * 0.15))
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
        # รอบแรกลอง DOWN แล้ว LEFT ทั้งคู่ยังชนอยู่ดี -- P นั่งอยู่ "บน" เส้น loc แนวนอน
        # เอง (LEFT/RIGHT จึงวิ่งขนานทับ loc ทันที) และมี n_line 3 เส้นแผ่ออกจาก P ใน
        # ทิศต่างๆ รอบข้าง (DOWN ก็ชนเส้นที่ 3) -- ป้ายยาว "P (นิ่งตลอดเวลา)" กว้างพอที่
        # จะกวาดผ่านเส้นใดเส้นหนึ่งได้เกือบทุกทิศในระยะใกล้ (เจอจริงจาก [LAYOUT] log
        # 2026-09-05 ทั้งสองรอบ) แก้เด็ดขาดด้วยเส้นชี้ (leader) ไปวางป้ายที่มุมล่างซ้าย
        # ซึ่งไม่มีเส้นไหนใน 3 เส้น + loc ผ่านเลย (ตรวจแล้ว: ทุกเส้นอยู่ทางขวา/บนของ P)
        p_lbl_pos = P + LEFT * 2.0 + DOWN * 0.75
        # ปลายเส้นชี้เดิมหยุดห่างจากจุดศูนย์กลางป้ายแค่ 0.16 หน่วย -- ป้ายยาว
        # "P (นิ่งตลอดเวลา)" ครึ่งความกว้างมากกว่านั้นมาก เส้นเลยพุ่งเข้าไปในกรอบ
        # ข้อความเอง (เจอจริงจาก [LAYOUT] log 2026-09-05 รอบสาม) ขยับให้หยุดที่ขอบ
        # ขวาของป้ายจริง ๆ แทน (เผื่อระยะกว้างกว่าความกว้างจริงของป้ายไว้ก่อน)
        p_leader = Line(P + (LEFT * 0.6 + DOWN * 0.2), p_lbl_pos + RIGHT * 1.15,
                         color=WHITE, stroke_width=1.5)
        tPl = Text("P (นิ่งตลอดเวลา)", font_size=20, color=WHITE).move_to(p_lbl_pos)
        cap = caption_top("เพื่อให้เคลื่อนที่เรียบ contact normal ต้องผ่านจุด P เสมอ", size=22)
        self.play(FadeIn(cap))
        self.play(Create(loc), FadeIn(dP), Create(p_leader), FadeIn(tPl))
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
            n_line = Line(P, Q + direction * 0.75, color=c, stroke_width=3.5)
            dQ = pt(Q, c, 0.07)
            # ป้ายเดิมชี้ทิศเดียวกับ n_line เอง (ขนานกับเส้นที่ยื่นออกไปอีก 0.75) ทำให้
            # กรอบข้อความทับเส้นตัวเอง (เจอจริงจาก [LAYOUT] log: 't2' ทับ Line) --
            # เปลี่ยนเป็นทิศตั้งฉาก (perp) แทน ให้ป้ายห่างจากเส้นออกด้านข้าง
            lbl_perp = np.array([-direction[1], direction[0], 0.0])
            tQ = tag(lb, Q, lbl_perp, c, 18, 0.28)
            # ขีดสั้นตั้งฉากที่ Q แทนผิวสัมผัสสองชิ้น ณ ขณะนั้น (สัมผัสกันที่ Q)
            perp = lbl_perp * 0.28
            flank = Line(Q - perp, Q + perp, color=GRAYTXT, stroke_width=3)
            grp = VGroup(n_line, dQ, tQ, flank)
            groups.add(grp)
            cap2 = caption_top(f"ขณะ {lb}: จุดสัมผัสอยู่ที่ Q -- ลาก normal ผ่าน Q กับ P", size=20)
            self.play(FadeOut(cap) if i == 0 else FadeOut(cap2_prev))
            self.play(FadeIn(cap2))
            self.play(Create(n_line), FadeIn(dQ), FadeIn(tQ), Create(flank))
            self.wait(0.7)
            cap2_prev = cap2

        cap3 = caption_top("ทุกขณะ normal ทิศต่างกัน แต่ 'ผ่าน P' เหมือนกันหมด", size=21)
        self.play(FadeOut(cap2_prev))
        self.play(FadeIn(cap3))
        self.wait(1.2)

        cap4 = caption_top("รู้รูปฟันตัวหนึ่ง -> ออกแบบรูปฟันอีกตัวให้เงื่อนไขนี้จริงได้เสมอ = conjugate",
                            size=20)
        self.play(FadeOut(cap3))
        self.play(FadeIn(cap4))
        self.wait(1.2)
        self.play(FadeOut(cap4))
        self.play(FadeOut(VGroup(loc, dP, tPl, p_leader, groups)))

        box_txt = MathTex(r"\text{conjugate teeth} \Rightarrow \text{constant angular velocity ratio}",
                           font_size=26, color=WHITE).move_to(UP * 0.3)
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
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))

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
        self.play(FadeOut(cap2))
        self.play(FadeIn(cap3))
        self.play(Create(belt), run_time=1.6)
        self.wait(1.0)

        # ป้าย "line of action" วางไกลจากวงกลมทั้งสอง -- จุดกึ่งกลาง E1p-E2p อยู่ใน
        # ช่องแคบระหว่างวงกลม (ห่างจากขอบวงกลมแค่ ~0.1) จึงต่อเส้นประออกไปนอกวงกลม
        # ก่อนแล้วค่อยแปะป้ายตรงปลายเส้นประ (เช็คด้วยเลขจริงแล้วว่าห่างวงกลมทั้งคู่ >0.5)
        ext_dir = np.array([np.sin(PHI0), np.cos(PHI0), 0.0])
        ext_end = E2p + ext_dir * 1.2
        ext_line = DashedLine(E2p, ext_end, color=WHITE, stroke_width=2.5, dash_length=0.1)
        loc_tag = tag("line of action", ext_end, UR, WHITE, 17, 0.15)
        self.play(Create(ext_line), FadeIn(loc_tag))
        self.wait(1.0)

        # ---- แสดงว่าอัตราทดคงที่แม้ C เปลี่ยน -----------------------------------
        self.play(FadeOut(VGroup(cap3, loc_tag, ext_line, l1, l2, adv)))
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
        self.play(FadeOut(cap4))
        self.play(FadeIn(concl, shift=UP * 0.15))
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
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        self.play(t_tracker.animate.set_value(2.0), run_time=4.5, rate_func=linear)
        self.wait(0.8)

        rho_note = Text("รูปร่างของอินโวลูทขึ้นกับขนาดของ base circle เท่านั้น",
                          font_size=20, color=OK).move_to([0, -3.15, 0])
        self.play(FadeOut(cap2))
        self.play(FadeIn(rho_note, shift=UP * 0.15))
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
        # หยุดเส้นโค้งพอดีที่จุด A (ไม่ยืดเลยไปอีก) -- เพราะแทนเจนต์ของอินโวลูทที่ A
        # ทับแนวเดียวกับส่วน C-A พอดี ถ้ายืดเลย A ไปจะไปทับป้าย rho_A ที่แปะไว้บนแนวนั้น
        curve = ParametricFunction(inv_pt, t_range=[0.02, t_A],
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
        self.play(FadeOut(cap2))
        self.play(FadeIn(cap3))
        self.play(FadeIn(dC), FadeIn(tC), Create(line_OC), Create(line_CA))
        ra = ra_mark(C_pt, O - C_pt, A_pt - C_pt, GRAYTXT, 0.22)
        self.play(Create(ra))
        self.wait(0.8)

        ang_phi = Angle(Line(O, A_pt), Line(O, C_pt), radius=0.55, color=WARN, stroke_width=4)
        lbl_phi = MathTex(r"\phi_A", font_size=26, color=WARN).move_to(
            O + normalize(normalize(A_pt - O) + normalize(C_pt - O)) * 0.85)
        cap4 = caption_top(r"phi_A = มุม AOC: cos(phi_A) = Rb/R_A", size=20)
        self.play(FadeOut(cap3))
        self.play(FadeIn(cap4))
        self.play(Create(ang_phi), FadeIn(lbl_phi))
        self.wait(1.0)

        # วางป้ายสูตรไว้ที่มุมขวาล่างของเฟรม (พื้นที่ว่างในช่วงนี้ของฉาก) แทนการแปะ
        # ใกล้ส่วน CA โดยตรง -- แนว CA ชิดกับทั้งจุด A และเส้นโค้งอินโวลูท พื้นที่แคบมาก
        lbl_CA = Text("rho_A = CA = Rb tan(phi_A)", font_size=18, color=WARN)
        lbl_CA.move_to([4.3, -1.2, 0])
        self.play(FadeIn(lbl_CA, shift=UP * 0.15))
        self.wait(0.8)

        # ---- ส่วนโค้ง BC บน base circle -----------------------------------------
        dB = pt(B_pt, GRAYTXT, 0.06)
        tB = tag("B", B_pt, RIGHT, GRAYTXT, 18, 0.22)
        arc_BC = Arc(radius=Rb, start_angle=0, angle=t_A, arc_center=O,
                     color=OK, stroke_width=5)
        cap5 = caption_top("B = จุดเริ่มอินโวลูท (t=0) -- ส่วนโค้ง BC ยาวเท่ากับสายพานที่คลี่ (rho_A)", size=19)
        self.play(FadeOut(cap4))
        self.play(FadeIn(cap5))
        self.play(FadeIn(dB), FadeIn(tB), Create(arc_BC))
        self.wait(1.0)

        ang_theta = Angle(Line(O, B_pt), Line(O, C_pt), radius=0.42, color=OK, stroke_width=3,
                          other_angle=False)
        lbl_theta = MathTex(r"\theta_A", font_size=22, color=OK).move_to(
            O + normalize(normalize(B_pt - O) + normalize(C_pt - O)) * 0.62)
        self.play(Create(ang_theta), FadeIn(lbl_theta))
        self.wait(1.0)

        cap6 = caption_top("สายพานไม่ยืด: ส่วนโค้ง BC = ความยาวที่คลี่ออก CA พอดี", size=20)
        self.play(FadeOut(cap5))
        self.play(FadeIn(cap6))
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
        self.play(FadeOut(cap6))
        self.play(FadeIn(result, shift=UP * 0.15), Create(box))
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

        O = LEFT * 3.3 + DOWN * 0.3
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
        # ป้าย t_b/t_A: ปักหมุดจริงไว้ที่ขอบของแต่ละ arc (ang_b อยู่ในช่วง +-delta_B,
        # ang_a อยู่ในช่วง +-delta_A จริง) แล้วลากเส้นชี้ (leader) ออกไปแปะป้ายที่ตำแหน่ง
        # ปลอดภัย -- พ้นวงกลมใหญ่สุด (R_A) ทุกวง กันไม่ให้ป้ายทับ Circle/Arc หรือทับกันเอง
        ang_b_lbl, ang_a_lbl = 20 * DEGREES, -12 * DEGREES
        dir_b = np.array([np.cos(ang_b_lbl), np.sin(ang_b_lbl), 0.0])
        dir_a = np.array([np.cos(ang_a_lbl), np.sin(ang_a_lbl), 0.0])
        tip_b, tip_a = O + R_B * dir_b, O + R_A * dir_a
        out_b, out_a = O + (R_A + 0.55) * dir_b, O + (R_A + 0.85) * dir_a
        leader_b = Line(tip_b, out_b, color=GEAR2, stroke_width=1.5)
        leader_a = Line(tip_a, out_a, color=GEAR3, stroke_width=1.5)
        t_b_lbl = tag("t_b (ที่ B)", out_b, dir_b, GEAR2, 15, 0.1)
        # ป้ายเดิมยาวมาก ("...แคบกว่า") ยื่นไปตามทิศ dir_a (ทแยงขวาล่าง) ไกลถึง x~2.75
        # ทะลุเข้าไปในโซนสูตร deriv ทางขวาแม้จะย่อ fit_width ของสูตรนั้นแล้วก็ตาม (เจอ
        # จริงจาก [LAYOUT] log 2026-09-05 ทั้งสองรอบ) -- ตัดข้อความสั้นลง (คำอธิบาย
        # "แคบกว่า" อยู่ในคำบรรยายบนอยู่แล้วไม่จำเป็นต้องซ้ำในป้ายนี้)
        t_a_lbl = tag("t_A (ที่ A)", out_a, dir_a, GEAR3, 15, 0.1)
        self.play(Create(leader_b), FadeIn(t_b_lbl))
        self.wait(0.8)
        self.play(Create(wedge_A), Create(arc_tA))
        self.play(Create(leader_a), FadeIn(t_a_lbl))
        self.wait(1.2)

        cap2 = caption_top("ครึ่งมุมฟัน delta_A = t_A/(2 R_A) = t_b/(2 R_b) - theta_A", size=20)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        self.wait(1.0)

        theta_row = VGroup(
            MathTex(r"\theta_A=\tan\phi_A-\phi_A", font_size=22, color=GRAYTXT),
            Text("(แทนค่าจากคลิปก่อน)", font_size=18, color=GRAYTXT),
        ).arrange(RIGHT, buff=0.25)
        fit_width(theta_row, 5.3)
        last_formula = MathTex(
            r"t_A=2R_A\!\left(\frac{t_B}{2R_B}-\tan\phi_A+\phi_A+\tan\phi_B-\phi_B\right)",
            font_size=22, color=OK)
        # 6.8 เดิม (to_edge(RIGHT,buff=0.35)) ทำให้ขอบซ้ายของกล่องยื่นมาใกล้ป้าย t_A ทางซ้าย
        # ของภาพมากเกินไป (เจอจริงจาก [LAYOUT] log: t_A ทับ SurroundingRectangle) แคบลง
        fit_width(last_formula, 5.3)
        deriv = VGroup(
            MathTex(r"\delta_A=\frac{t_A}{2R_A}=\frac{t_b}{2R_b}-\theta_A",
                    font_size=26, color=WHITE),
            theta_row,
            last_formula,
        ).arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.35)
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
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        loa = Line(E1 - (E2 - E1) * 0.25, E2 + (E2 - E1) * 0.25, color=LOA_C, stroke_width=4)
        self.play(Create(loa))
        self.wait(0.8)

        cap3 = caption_top("2) Path of contact อยู่ตาม line of action = common tangent ของ base circle ทั้งสอง", size=19)
        self.play(FadeOut(cap2))
        self.play(FadeIn(cap3))
        dE1 = pt(E1, BASE_C, 0.07)
        dE2 = pt(E2, BASE_C, 0.07)
        # ป้าย E1/E2: ชี้ออกจาก P ไปตามแนวเส้น line of action เอง (ไม่ใช่ซ้าย/ขวาตรงๆ)
        # เพราะ E1, E2 อยู่ใกล้ P มาก (ใกล้กว่ารัศมีวงเล็บมุม phi ที่จะวาดทีหลัง) --
        # ป้ายทิศอื่นจะเข้าไปอยู่ในบริเวณที่ Angle(vert, loa) กวาดผ่านพอดี
        # ป้ายเดิมชี้ทิศ E-P (ทิศ line of action) ซึ่งไม่ใช่ทิศออกจากวงกลมของเฟือง
        # แต่ละตัว -- E1/E2 เป็นจุดสัมผัสอยู่บน/ใกล้ base+pitch circle ของตัวเองพอดี
        # (ช่องว่างระหว่าง Rb กับ R แคบมาก) เจอจริงจาก [LAYOUT] log: 'E2' ทับ Circle
        # -- รอบแรกลองชี้ออกจากศูนย์กลาง "ของตัวเอง" (O1 สำหรับ E1) แต่ E1/E2 อยู่ใกล้
        # จุด P มาก การชี้ออกจากศูนย์ตัวเองบางทีกลับพาไปใกล้วงกลมของ "อีกเฟือง" แทน
        # (เจอจริงรอบสอง: 'E1' ทับ Circle) แก้เด็ดขาดด้วยการชี้ออกจากศูนย์กลางของ "อีก
        # เฟือง" (ไม่ใช่ตัวเอง) แทน -- ทิศนี้เคลื่อนออกจากทั้งวงกลมของตัวเอง (เพราะ E
        # อยู่บนวงกลมตัวเองอยู่แล้ว ทิศไหนที่ไม่พุ่งเข้าหาศูนย์ตัวเองก็ปลอดภัย) และออก
        # จากวงกลมอีกฝั่งไปพร้อมกัน
        dir_E1 = (E1 - O2) / np.linalg.norm(E1 - O2)
        dir_E2 = (E2 - O1) / np.linalg.norm(E2 - O1)
        tE1 = tag("E1", E1, dir_E1, BASE_C, 18, 0.35)
        tE2 = tag("E2", E2, dir_E2, BASE_C, 18, 0.35)
        self.play(FadeIn(dE1), FadeIn(dE2), FadeIn(tE1), FadeIn(tE2))
        self.wait(0.8)

        cap4 = caption_top("3) Pressure angle (phi) = มุมระหว่าง line of action กับเส้นตั้งฉากของ line of centers", size=19)
        self.play(FadeOut(cap3))
        self.play(FadeIn(cap4))
        vert = DashedLine(P + UP * 0.9, P + DOWN * 0.9, color=GRAYTXT, stroke_width=2)
        self.play(Create(vert))
        ang = Angle(vert, loa, radius=0.5, color=WARN, stroke_width=4)
        lbl_phi = MathTex(r"\phi", font_size=28, color=WARN).move_to(
            P + normalize(normalize(UP) + normalize(fr["d"])) * 0.85)
        self.play(Create(ang), FadeIn(lbl_phi))
        self.wait(1.0)

        formula = MathTex(r"R_b = R\cos\phi", font_size=28, color=WHITE).move_to([3.2, 1.9, 0])
        box = SurroundingRectangle(formula, color=OK, buff=0.15)
        self.play(FadeOut(cap4))
        self.play(FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(1.4)

        note = Text("phi ใหญ่ -> แรงกดเข้าแบริ่งมากขึ้น แต่ฟันแข็งแรงขึ้น (ตัดฟันน้อยได้ -- ดูหน้า 37)",
                     font_size=18, color=GRAYTXT).move_to([0, -3.15, 0])
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(2.2)


# =====================================================================
# G14 -- หน้า 14: ศัพท์เรขาคณิตเฟือง
# =====================================================================
class G14_GearVocabulary(SafeScene):
    def construct(self):
        self.add(title("ศัพท์เรขาคณิตเฟือง", size=28))
        self.add(page_ref("หน้า 14"))

        O = LEFT * 1.3
        Ro, R, Rb, Ri = 2.35, 2.0, 1.78, 1.55
        cap = caption_top("4 วงกลมซ้อนกัน จากในสุดไปนอกสุด", size=21)
        self.play(FadeIn(cap))

        rings = [
            (Ri, GRAYTXT, "Dedendum circle  R_i", "โคนฟัน"),
            (Rb, BASE_C, "Base circle  R_b", "จุดเริ่มอินโวลูท"),
            (R, PITCH_C, "Pitch circle  R", "วงกลิ้ง -- อ้างอิงหลัก"),
            (Ro, GEAR3, "Addendum circle  R_o", "ยอดฟัน"),
        ]
        legend = VGroup()
        for i, (r, c, name, note_txt) in enumerate(rings):
            circ = Circle(radius=r, color=c, stroke_width=3.5).move_to(O)
            row = Text(name, font_size=18, color=c)
            legend.add(row)
            self.play(Create(circ), run_time=0.7)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.55).shift(UP * 0.6)
        self.play(FadeIn(legend, shift=RIGHT * 0.2))
        self.wait(1.0)

        # addendum/dedendum เป็นระยะรัศมี -- เดิมวัดแนวตั้ง (UP/DOWN) แล้วป้ายชี้ LEFT
        # ซึ่งกวาดย้อนกลับข้ามวงกลม R_o ที่ยอดสุด/R,R_b ที่ก้นสุด (เจอจริงจาก [LAYOUT]
        # log: a/b ทับ Circle) เปลี่ยนไปวัดแนวนอน (RIGHT/LEFT) แล้วป้ายชี้ตั้งฉาก
        # (UP/DOWN) แทน -- อยู่ในช่องว่างระหว่างวงแหวนพอดี ไม่กวาดข้ามเส้นรอบวงไหนเลย
        a_seg = seg(O + RIGHT * R, O + RIGHT * Ro, GEAR3, 5)
        b_seg = seg(O + LEFT * Ri, O + LEFT * R, GRAYTXT, 5)
        # ป้ายยาว "a (addendum)"/"b (dedendum)" กว้างเกินไป -- ปลายป้ายด้านที่ยื่นออก
        # จากศูนย์ไปทาง R_o/R_i ไปจ่อโดนขอบวงกลมพอดี (แม้จุดยึดตรงกลางจะห่างวงก็ตาม
        # เพราะวงกลมโค้งแคบลงตรงขอบ) เจอจริงจาก [LAYOUT] log 2026-09-05 ซ้ำสองรอบ --
        # cap2 ที่กำลังจะขึ้นอธิบาย a/b เต็มคำอยู่แล้ว ป้ายบนรูปจึงย่อเหลือตัวอักษรเดียว
        # พอ (แบบเดียวกับ G16 ที่ใช้ท่านี้แล้วผ่าน [LAYOUT] คลีนจริง)
        # ยังเหลือทับเล็กน้อยแม้ย่อเหลือตัวอักษรเดียวแล้ว (มุมของวงแคบลงตรงขอบพอดี) --
        # เพิ่ม buff อีกรอบ (เจอจริงจาก [LAYOUT] log 2026-09-05 รอบสาม เหลือแค่ 'b' 2 จุด)
        a_lbl = tag("a", O + RIGHT * (R + Ro) / 2, UP, GEAR3, 16, 0.45)
        b_lbl = tag("b", O + LEFT * (R + Ri) / 2, DOWN, GRAYTXT, 16, 0.45)
        cap2 = caption_top("addendum a = R_o - R (ฟันยื่นสูง) | dedendum b = R - R_i (โคนฟันลึก)", size=19)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        self.play(Create(a_seg), Create(b_seg), FadeIn(a_lbl), FadeIn(b_lbl))
        self.wait(1.4)

        order = MathTex(r"R_i < R_b < R < R_o", font_size=28, color=OK).move_to([0, -3.15, 0])
        self.play(FadeOut(cap2))
        self.play(FadeIn(order, shift=UP * 0.15))
        self.wait(1.2)

        warn = Text("ถ้าฟันน้อยมาก R_b อาจโผล่เหนือ R_i -- นี่คือที่มาของ undercut (หน้า 34-37)",
                     font_size=17, color=WARN).next_to(order, DOWN, buff=0.2)
        self.play(FadeIn(warn))
        self.wait(1.8)


# =====================================================================
# G15 -- หน้า 15: สูตรเรขาคณิตชุดหลัก
# =====================================================================
class G15_MainFormulas(SafeScene):
    def construct(self):
        self.add(title("สูตรเรขาคณิตชุดหลัก -- หน้าที่คุ้มที่สุดของบท", size=24))
        self.add(page_ref("หน้า 15"))

        N = 20
        # p_len=1.2 เดิมให้ R=1.2*20/(2pi)=3.82 -- ใหญ่เกินไป วงกลมพุ่งพ้นทั้งโซน
        # title/caption บนและขอบล่างเฟรม (เจอจริงจาก [LAYOUT] log 2026-09-05: title/
        # caption ทับ Circle x2 + ป้าย 'N=20 ตำแหน่งฟัน' หลุดขอบล่าง) ลดลงเหลือ 0.55
        # ให้ R=1.75 พอดีเฟรม (ใช้ค่าเดียวกับ G16 เพื่อความต่อเนื่อง)
        p_len = 0.55
        R = p_len * N / TAU
        O = LEFT * 2.0

        cap = caption_top("ที่มาของ R = pN/(2 pi): เส้นรอบวงต้องบรรจุฟัน N ตัวพอดี", size=21)
        self.play(FadeIn(cap))

        circ = Circle(radius=R, color=PITCH_C, stroke_width=3).move_to(O)
        self.play(Create(circ))
        ticks = VGroup()
        for i in range(N):
            ang = TAU * i / N
            p1 = O + R * np.array([np.cos(ang), np.sin(ang), 0])
            p2 = O + (R + 0.16) * np.array([np.cos(ang), np.sin(ang), 0])
            ticks.add(Line(p1, p2, color=GRAYTXT, stroke_width=2))
        self.play(Create(ticks), run_time=1.2)
        note1 = Text(f"N = {N} ตำแหน่งฟัน", font_size=18, color=GRAYTXT).next_to(
            circ, DOWN, buff=0.35)
        self.play(FadeIn(note1))
        self.wait(0.6)

        # เน้นช่วง p หนึ่งช่วง
        a0 = 0
        a1 = TAU / N
        seg_arc = Arc(radius=R, start_angle=a0, angle=a1, arc_center=O, color=WARN,
                      stroke_width=6)
        # จุดยึดอยู่ใกล้มุม 9 องศา (แทบไม่มีความชันจากแนวราบ) -- ป้ายชี้ UP เดิมเกือบขนาน
        # กับเส้นสัมผัสวงกลมตรงนั้น ยื่นย้อนเข้าไปทับ seg_arc (เจอจริงจาก [LAYOUT] log)
        # เปลี่ยนเป็นทิศรัศมีออกจากศูนย์กลาง O แทน รับประกันว่าห่างจาก circ/seg_arc เสมอ
        _p_mid_ang = a1 / 2
        _p_radial = np.array([np.cos(_p_mid_ang), np.sin(_p_mid_ang), 0.0])
        p_lbl = tag("p (circular pitch)", O + (R + 0.05) * _p_radial,
                    _p_radial, WARN, 15, 0.25)
        cap2 = caption_top("แต่ละช่วงกินระยะ p (ตามส่วนโค้ง) -- มี N ช่วงรอบวง", size=20)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        self.play(Create(seg_arc), FadeIn(p_lbl))
        self.wait(1.0)

        deriv = VGroup(
            MathTex(r"2\pi R = pN", font_size=28, color=WHITE),
            MathTex(r"R=\frac{pN}{2\pi}", font_size=30, color=OK),
        ).arrange(RIGHT, buff=0.7).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        box = SurroundingRectangle(deriv[1], color=OK, buff=0.15)
        self.play(FadeOut(cap2))
        self.play(FadeIn(deriv[0], shift=UP * 0.15))
        self.wait(0.6)
        self.play(FadeIn(deriv[1], shift=UP * 0.15), Create(box))
        self.wait(1.0)

        formulas = VGroup(
            MathTex(r"R_b=R\cos\phi", font_size=24, color=BASE_C),
            MathTex(r"R_o=R+a", font_size=24, color=GEAR3),
            MathTex(r"R_i=R-b", font_size=24, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(deriv, DOWN, buff=0.5)
        for f in formulas:
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.5)
        self.wait(2.0)


# =====================================================================
# G16 -- หน้า 16: ภาพรวมเรขาคณิตเฟือง (รูปประกอบ)
# =====================================================================
class G16_GeometryOverview(SafeScene):
    def construct(self):
        self.add(title("ภาพรวมเรขาคณิตเฟือง", size=28))
        self.add(page_ref("หน้า 16 -- ใช้เป็นภาพอ้างอิง"))

        N = 20
        # เดิม p_len=1.2 -> R=3.82, Ro=4.5 -- ใหญ่เกินเฟรมมาก (เจอจริงจาก [LAYOUT] log
        # 2026-09-05: title/caption/Arc ทับ Circle หลายจุด) ลดเหลือ 0.55 ให้ตรงกับ G15
        # (ต่อเนื่องกันด้วย ตามกฎ §21 ข้อ 2 ของ manim-teaching-video)
        p_len = 0.55
        R = p_len * N / TAU
        a, b = 0.18 * R, 0.22 * R
        Ro, Ri = R + a, R - b
        Rb = R * np.cos(20 * DEGREES)
        O = ORIGIN + DOWN * 0.2

        cap = caption_top("รวมทุกอย่างไว้ในรูปเดียว -- ใช้เทียบเวลาทำโจทย์", size=21)
        self.play(FadeIn(cap))

        rings = VGroup(*[
            Circle(radius=r, color=c, stroke_width=2.5).move_to(O)
            for r, c in [(Ri, GRAYTXT), (Rb, BASE_C), (R, PITCH_C), (Ro, GEAR3)]
        ])
        self.play(Create(rings), run_time=1.3)

        # p และ t บนวงกลิ้ง
        n_show = 3
        for i in range(n_show):
            a0 = TAU * i / N
            a1 = TAU * (i + 1) / N
            mid = (a0 + a1) / 2
            half_t = (a1 - a0) * 0.5 * 0.42  # t ~ ครึ่งหนึ่งของ p โดยประมาณ (ไม่ backlash)
            tooth_arc = Arc(radius=R, start_angle=mid - half_t, angle=2 * half_t,
                             arc_center=O, color=WARN, stroke_width=7)
            self.add(tooth_arc)
        p_a0, p_a1 = 0, TAU / N
        p_arc = Arc(radius=R + 0.35, start_angle=p_a0, angle=p_a1, arc_center=O,
                    color=GRAYTXT, stroke_width=2)
        # เดิม p_lbl ชี้ UP จากจุดใกล้มุม 9 องศา (เกือบขนานเส้นสัมผัสวงกลมตรงนั้น) และ
        # t_lbl ชี้ RIGHT จากจุดขวาสุดของวง R เข้าไปทับวง R_o/p_arc ที่ใหญ่กว่า (เจอจริง
        # จาก [LAYOUT] log: 't(ความหนาฟัน)' ทับ Circle/Arc + ทับป้าย legend) --
        # เปลี่ยนทั้งคู่เป็นทิศรัศมีออกจากศูนย์กลาง O และย้าย t_lbl ไปมุมว่างระหว่างฟัน
        _p_mid = p_a1 / 2
        _p_rad = np.array([np.cos(_p_mid), np.sin(_p_mid), 0.0])
        p_lbl = tag("p", O + (R + 0.6) * _p_rad, _p_rad, GRAYTXT, 18, 0.15)
        _t_ang = -32 * DEGREES
        _t_rad = np.array([np.cos(_t_ang), np.sin(_t_ang), 0.0])
        t_lbl = tag("t (ความหนาฟัน)", O + R * _t_rad, _t_rad, WARN, 14, 0.45)
        self.play(Create(p_arc), FadeIn(p_lbl), FadeIn(t_lbl))
        self.wait(0.8)

        # a_seg/b_seg เดิมวัดแนวตั้ง (UP/DOWN) แล้วป้ายชี้ LEFT กวาดย้อนข้ามวง R_o/R_i
        # (บั๊กเดียวกับที่เจอใน G14 -- แก้เชิงรุกที่นี่ด้วยแม้ log ไม่ได้ชี้จุดนี้ตรงๆ
        # เพราะโค้งเดียวกันเป๊ะ) เปลี่ยนเป็นแนวนอน (RIGHT/LEFT) + ป้ายชี้ตั้งฉาก (UP/DOWN)
        a_seg = seg(O + RIGHT * R, O + RIGHT * Ro, GEAR3, 4)
        b_seg = seg(O + LEFT * Ri, O + LEFT * R, GRAYTXT, 4)
        a_lbl = tag("a", O + RIGHT * (R + Ro) / 2, UP, GEAR3, 16, 0.1)
        b_lbl = tag("b", O + LEFT * (R + Ri) / 2, DOWN, GRAYTXT, 16, 0.1)
        self.play(Create(a_seg), Create(b_seg), FadeIn(a_lbl), FadeIn(b_lbl))
        self.wait(1.6)

        legend = VGroup(
            Text("เทา = dedendum (R_i)", font_size=16, color=GRAYTXT),
            Text("ม่วง = base (R_b)", font_size=16, color=BASE_C),
            Text("ฟ้าเขียว = pitch (R)", font_size=16, color=PITCH_C),
            Text("ส้ม = addendum (R_o)", font_size=16, color=GEAR3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.5).shift(UP*0.5)
        self.play(FadeOut(cap))
        self.play(FadeIn(legend, shift=RIGHT * 0.15))
        self.wait(2.2)


# =====================================================================
# G17 -- หน้า 17: Base pitch + ตัวอย่างเล็ก
# =====================================================================
class G17_BasePitch(SafeScene):
    def construct(self):
        self.add(title("Base Pitch (p_b)", size=30))
        self.add(page_ref("หน้า 17"))

        cap = caption_top("ระยะห่างฟันวัดบน base circle -- เท่ากับที่วัดตาม line of action ด้วย", size=21)
        self.play(FadeIn(cap))

        formula = MathTex(r"p_b=\frac{2\pi R_b}{N}=p\cos\phi", font_size=30,
                           color=WHITE).move_to(UP * 1.6)
        box = SurroundingRectangle(formula, color=OK, buff=0.18)
        self.play(FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(1.2)

        # ---- ตัวอย่าง: N=8, R=2in หา p --------------------------------------
        cap2 = caption_top("ตัวอย่าง: เฟือง 8 ฟัน, R = 2 นิ้ว -- หา circular pitch", size=21)
        self.play(FadeOut(cap))
        # เอากรอบสูตร p_b ออกก่อน -- เดิมค้างอยู่ทั้งคลิปแล้วไปทับ step1 ของคอลัมน์
        # ตัวอย่างด้านขวา (เจอจริงจาก [LAYOUT] log 2026-09-05: step1 ทับ SurroundingRectangle)
        self.play(FadeOut(formula), FadeOut(box))
        self.play(FadeIn(cap2))

        N, R = 8, 2.0
        O = DOWN * 0.4 + LEFT * 3.0
        circ = Circle(radius=1.15, color=PITCH_C, stroke_width=3).move_to(O)  # สเกลย่อเพื่อโชว์
        ticks = VGroup(*[
            Line(O + 1.15 * np.array([np.cos(TAU * i / N), np.sin(TAU * i / N), 0]),
                 O + 1.32 * np.array([np.cos(TAU * i / N), np.sin(TAU * i / N), 0]),
                 color=GRAYTXT, stroke_width=2) for i in range(N)
        ])
        self.play(Create(circ), Create(ticks))
        given = Text("N=8, R=2 in", font_size=18, color=GRAYTXT).next_to(circ, DOWN, buff=0.3)
        self.play(FadeIn(given))
        self.wait(0.6)

        # ขั้น 2 มีคำไทยปนสูตร -> แยกเป็น Text + MathTex คนละก้อน กัน LaTeX พัง
        # (เดิมมี steps=VGroup(...) ที่ยัด Thai เข้าไปใน MathTex \text{} ตรงๆ ทิ้งไว้
        # เป็นโค้ดตาย แต่ Python ยัง evaluate ตอน construct() ทำให้ LaTeX compile พังบน
        # cloud runner แม้จะไม่เคยถูกใช้แสดงผลจริงเลยก็ตาม -- ลบทิ้ง ใช้ step1-4 ด้านล่างแทน)
        step2 = VGroup(Text("ขั้น 2 -- สูตร:", font_size=19, color=WHITE),
                        MathTex(r"R=\frac{pN}{2\pi}", font_size=22, color=WHITE)
                        ).arrange(RIGHT, buff=0.2)
        step1 = Text("ขั้น 1 -- โจทย์ให้: N=8, R=2 in หา p", font_size=19, color=WHITE)
        step3 = VGroup(Text("ขั้น 3 -- แทนค่า:", font_size=19, color=WHITE),
                        MathTex(r"p=\frac{2\pi R}{N}=\frac{2\pi(2)}{8}=\frac{\pi}{2}\approx1.571\text{ in}",
                                font_size=20, color=OK)).arrange(RIGHT, buff=0.2)
        step4 = Text("ขั้น 4 -- ตรวจ: เส้นรอบวง = 2 pi(2) = 12.57 in / 8 ฟัน = 1.571 in/ฟัน (ตรง)",
                      font_size=18, color=OK)
        # step1/step4 เป็นบรรทัดยาวไม่มี fit_width มาก่อน ทำให้คอลัมน์ทั้งก้อนกว้างเกิน
        # ขอบซ้ายยื่นไปทับ circ/formula ด้านซ้าย (เจอจริงจาก [LAYOUT] log 2026-09-05)
        fit_width(step1, 5.2)
        fit_width(step4, 5.2)
        col = VGroup(step1, step2, step3, step4).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        col.to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        for row in col:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.6)
            self.wait(0.5)
        self.wait(1.8)


# =====================================================================
# G18 -- หน้า 18: ตัวอย่าง หา base circle radius และ addendum
# =====================================================================
class G18_ExampleBaseCircle(SafeScene):
    def construct(self):
        self.add(title("ตัวอย่าง: หา R_b และ addendum", size=27))
        self.add(page_ref("หน้า 18"))

        N, phi_deg, R, Ro = 24, 20, 1.5, 1.625
        phi = phi_deg * DEGREES
        Rb = R * np.cos(phi)
        a = Ro - R
        m_check = 2 * R / N

        # เดิม LEFT*3.3 -- วง c_Ro (รัศมีขยาย 2.0) ขอบขวาอยู่ที่ x=-1.3 ใกล้คอลัมน์
        # ขั้นตอนด้านขวามากไป ขยับซ้ายเพิ่มให้มีระยะกันชนมากขึ้น
        O = LEFT * 4.0 + DOWN * 0.3
        cap = caption_top("โจทย์: N=24, phi=20°, R=1.5in, R_o=1.625in -- หา (ก) R_b (ข) a", size=19)
        self.play(FadeIn(cap))

        c_R = Circle(radius=1.5, color=PITCH_C, stroke_width=3).move_to(O)
        c_Ro = Circle(radius=1.5 + (Ro - R) * 4, color=GEAR3, stroke_width=3).move_to(O)  # ขยาย a ให้เห็นชัด
        self.play(Create(c_R), Create(c_Ro))
        # ป้ายเดิมชี้ UP จากจุดเดียวกับที่ a_seg (เส้นแนวตั้ง) จะเริ่มต้น/สิ้นสุดพอดี --
        # กรอบข้อความเลยทับเส้นที่วาดทีหลัง (เจอจริงจาก [LAYOUT] log: 'R=1.5in' ทับ Line)
        # แก้โดยให้สองป้ายชี้คนละด้าน (LEFT/RIGHT) แทน หลบแนวตั้งที่ a_seg จะใช้
        # รอบก่อนแก้ทับ a_seg (แนวตั้ง) ได้แล้วด้วย LEFT/RIGHT แต่ยังทับส่วนโค้งของ
        # c_Ro อยู่ (จุดยึดอยู่ตรง "ยอด" ของวงในแนวตั้ง ขยับแนวนอนล้วนๆ ยังอยู่ในช่วง
        # ความสูงที่วงยังโค้งแคบอยู่) เจอจริงจาก [LAYOUT] log 2026-09-05 -- แก้เพิ่มด้วย
        # การขยับทแยง (UL/UR) ให้สูงพ้นทั้งแนวนอนและแนวตั้งไปพร้อมกัน ปลอดภัยกว่า
        # ยังเหลือทับเล็กน้อยกับ c_Ro (เจอจริงจาก [LAYOUT] log 2026-09-05 รอบสาม)
        # เพิ่ม buff อีกรอบให้พ้นส่วนโค้งแน่นอน
        lR = tag("R = 1.5 in", O + UP * 1.5, UL, PITCH_C, 15, 0.55)
        lRo = tag("R_o = 1.625 in", O + UP * (1.5 + (Ro - R) * 4), UR, GEAR3, 15, 0.55)
        self.play(FadeIn(lR), FadeIn(lRo))
        self.wait(0.8)

        cap2 = caption_top("ขั้น 1 -- เข้าใจโจทย์: a = R_o - R (ส่วนต่างของสองรัศมี)", size=20)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        a_seg = seg(O + UP * 1.5, O + UP * (1.5 + (Ro - R) * 4), GEAR3, 5)
        self.play(Create(a_seg))
        self.wait(0.8)

        step_a = Text("ขั้น 2 -- สูตร: R_b = R cos(phi), a = R_o - R", font_size=19, color=WHITE)
        step_d = Text(f"ขั้น 4 -- ตรวจ: R_b < R เสมอ (cos phi<1) และ a ~ m = 2R/N = {m_check:.3f} "
                       "-> ตรงพอดี = full-depth มาตรฐาน", font_size=17, color=OK)
        # เดิม fit_width เรียกทีหลัง .arrange()+.to_edge() -- scale() ของ manim ย่อรอบ
        # จุดศูนย์กลางตัวเอง ทำให้ตำแหน่งที่ arrange/to_edge คำนวณไว้ (จากความกว้างเดิม
        # ก่อนย่อ) ไม่ตรงกับขนาดจริงหลังย่อ = ซ้ายขวาเยื้องกัน (เจอจริงจาก [LAYOUT] log:
        # ขั้น2/ขั้น4 ทับ Circle ทั้งที่ fit_width ก็มีอยู่แล้ว) แก้โดยย่อ "ก่อน" arrange เสมอ
        fit_width(step_a, 5.0)
        fit_width(step_d, 5.0)
        steps = VGroup(
            step_a,
            MathTex(r"R_b=1.5\cos20^\circ=1.5(0.93969)=1.409\text{ in}",
                    font_size=21, color=BASE_C),
            MathTex(r"a=1.625-1.5=0.125\text{ in}", font_size=21, color=GEAR3),
            step_d,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        self.play(FadeOut(cap2))
        for row in steps:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.6)
            self.wait(0.7)
        self.wait(1.6)

        c_Rb = Circle(radius=Rb, color=BASE_C, stroke_width=3).move_to(O)
        self.play(Create(c_Rb))
        self.wait(1.6)


# =====================================================================
# G19 -- หน้า 19: Contact Ratio (m_p) คืออะไร
# =====================================================================
class G19_ContactRatioDef(SafeScene):
    def construct(self):
        self.add(title("Contact Ratio (m_p) คืออะไร", size=27))
        self.add(page_ref("หน้า 19"))

        fr = cr_wide()
        O1, O2, P = fr["O1"], fr["O2"], fr["P"]
        E1, E2, A, B = fr["E1"], fr["E2"], fr["A"], fr["B"]
        Rb1, Rb2, Ro1, Ro2 = fr["Rb1"], fr["Rb2"], fr["Ro1"], fr["Ro2"]

        cap = caption_top("ใช้เฟืองคู่เดียวกับตัวอย่างหน้า 25 ตลอดบล็อกนี้ (pinion 24 ฟัน ขับ gear 60 ฟัน)",
                           size=17)
        self.play(FadeIn(cap))

        base1 = Circle(radius=Rb1, color=BASE_C, stroke_width=3).move_to(O1)
        base2 = Circle(radius=Rb2, color=BASE_C, stroke_width=3).move_to(O2)
        add1 = DashedVMobject(Circle(radius=Ro1, color=GEAR2, stroke_width=2.5).move_to(O1),
                               num_dashes=30)
        add2 = DashedVMobject(Circle(radius=Ro2, color=GEAR3, stroke_width=2.5).move_to(O2),
                               num_dashes=48)
        self.play(Create(base1), Create(base2))
        self.play(Create(add1), Create(add2))
        lb1 = tag("pinion (24T)", O1 + DOWN * (Ro1 + 0.25), DOWN, GEAR2, 15, 0.08)
        lb2 = tag("gear (60T)", O2 + RIGHT * (Ro2 + 0.2), RIGHT, GEAR3, 15, 0.1)
        self.play(FadeIn(lb1), FadeIn(lb2))
        self.wait(0.6)

        loa_ext = Line(E1 - fr["d"] * 0.5, E2 + fr["d"] * 0.5, color=LOA_C, stroke_width=3)
        path = Line(A, B, color=WARN, stroke_width=7)
        self.play(FadeOut(cap))
        cap2 = caption_top("เส้น line of action เดิม -- ตรงกลางมีช่วงเล็ก ๆ ที่ฟันสัมผัสกันจริง",
                            size=18)
        self.play(FadeIn(cap2), Create(loa_ext))
        self.wait(0.5)
        self.play(Create(path))
        self.wait(0.6)

        # จุด E1/E2/A/B/P ทั้งหมดอยู่ในช่วงแคบมาก (สเกลลงมาก) ใส่ป้ายกำกับทุกจุดตรงนี้
        # จะชนกันหมด (เจอจริงจาก [LAYOUT] log 2026-09-05: 29 จุดต้องแก้ ส่วนใหญ่คือจุด
        # เหล่านี้ทับวงกลม/กันเอง) -- ย้ายไปอธิบายลำดับจุดในแผนภาพช่วยความจำแบบง่าย
        # (ไม่ยึดสเกลจริง) ด้านล่างแทน คล้ายที่ทำสำเร็จแล้วใน G34
        self.play(FadeOut(cap2))
        cap3 = caption_top("ลำดับจุดบนเส้นนี้ (แผนภาพช่วยจำ ไม่ยึดสเกลจริง)", size=19)
        self.play(FadeIn(cap3))

        y0 = -1.9
        schem = Line(LEFT * 5.0 + UP * y0, RIGHT * 5.0 + UP * y0, color=GRAYTXT, stroke_width=2)
        pts_schem = [(-3.6, "E1", BASE_C), (-1.6, "A", WARN), (0.0, "P", WHITE),
                     (1.6, "B", WARN), (3.6, "E2", BASE_C)]
        sdots = VGroup(); slbls = VGroup()
        for x, name, c in pts_schem:
            p = np.array([x, y0, 0])
            sdots.add(pt(p, c, 0.06))
            slbls.add(tag(name, p, UP, c, 17, 0.12))
        self.play(Create(schem), FadeIn(sdots), FadeIn(slbls))
        seg_ab = Line(np.array([-1.6, y0, 0]), np.array([1.6, y0, 0]), color=WARN, stroke_width=7)
        self.play(Create(seg_ab))
        note_schem = Text("A-B (ช่วงสัมผัสจริง) ซ้อนอยู่ใน E1-E2 เสมอถ้าไม่ interference",
                           font_size=15, color=GRAYTXT).next_to(schem, DOWN, buff=0.3)
        self.play(FadeIn(note_schem))
        self.wait(1.4)

        cap4 = caption_top("ก่อนถึง P (A->P) = angle of approach | หลัง P (P->B) = angle of recess", size=17)
        self.play(FadeOut(cap3))
        self.play(FadeIn(cap4))
        self.wait(1.2)

        self.play(FadeOut(VGroup(cap4, schem, sdots, slbls, seg_ab, note_schem)))

        formula = MathTex(r"m_p=\frac{Z}{p_b},\qquad Z=\overline{AB}", font_size=26, color=WHITE)
        fit_width(formula, 5.3)
        meaning = Text("ความหมาย: จำนวนคู่ฟันที่ขบกันอยู่โดยเฉลี่ยตลอดการหมุน",
                        font_size=16, color=GRAYTXT)
        fit_width(meaning, 5.3)
        row1 = Text("m_p > 1     -> ใช้งานได้ (มีฟันขบเสมอ)", font_size=15, color=WHITE)
        row2 = Text("m_p > 1.40 -> เดินเรียบ (เกณฑ์ออกแบบจริง)", font_size=15, color=OK)
        fit_width(row1, 5.3)
        fit_width(row2, 5.3)
        panel = VGroup(formula, meaning, row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        panel.to_edge(RIGHT, buff=0.6).shift(UP * 0.3)
        box = SurroundingRectangle(formula, color=OK, buff=0.18)
        self.play(FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(0.8)
        self.play(FadeIn(meaning, shift=UP * 0.1))
        self.wait(0.8)
        self.play(FadeIn(row1, shift=RIGHT * 0.15), run_time=0.5)
        self.play(FadeIn(row2, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(1.2)

        note = Text("ทำไมหารด้วย p_b ไม่ใช่ p -- เพราะ p_b วัดในระบบเดียวกับ Z (ตาม line of action)",
                     font_size=17, color=WARN).move_to([0, -3.15, 0])
        fit_width(note, 12.5)
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(2.0)


# =====================================================================
# G20 -- หน้า 20: ที่มาของ Z ขั้นที่ 1: นิยามจุด A และ B
# =====================================================================
class G20_ZDefinitionAB(SafeScene):
    def construct(self):
        self.add(title("ที่มาของ Z ขั้นที่ 1: นิยามจุด A และ B", size=24))
        self.add(page_ref("หน้า 20"))

        fr = cr_local()
        A, B, E1, E2, P = fr["A"], fr["B"], fr["E1"], fr["E2"], fr["P"]

        cap = caption_top("บนเส้น line of action เดียวกัน มี 5 จุดเรียงกัน: E1 - A - P - B - E2", size=18)
        self.play(FadeIn(cap))

        loa = Line(A - (B - A) * 0.9, B + (B - A) * 0.9, color=LOA_C, stroke_width=3)
        self.play(Create(loa))
        # E1 กับ A อยู่ใกล้กันมาก (~0.17 หน่วย) เช่นเดียวกับ P กับ B (~0.28 หน่วย) --
        # ทิศ UP/DOWN ตามความสูงเทียบกับ P เดิมทำให้ป้ายที่อยู่กลุ่มเดียวกันชนกันเอง/
        # ชนจุดอื่น (เจอจริงจาก [LAYOUT] log 2026-09-05: 3 จุดต้องแก้) แก้โดยจัดกลุ่ม
        # (E1,A) ไปด้านหนึ่งของเส้น, (P,B) ไปอีกด้าน แล้วถ่างระยะ (buff) ต่างกันในกลุ่ม
        # เดียวกันเพื่อไม่ให้ซ้อนกัน -- E2 อยู่ห่างจากกลุ่มอื่นมากอยู่แล้วใช้ UP ธรรมดาได้
        perp = np.array([-fr["d"][1], fr["d"][0], 0.0])
        pts = [(E1, BASE_C, "E1", -perp, 0.14), (A, WARN, "A", -perp, 0.5),
               (P, WHITE, "P", perp, 0.14), (B, WARN, "B", perp, 0.5),
               (E2, BASE_C, "E2", UP, 0.16)]
        dots = VGroup(); labels = VGroup()
        for p, c, name, direc, bf in pts:
            d = pt(p, c, 0.07)
            lb = tag(name, p, direc, c, 19, bf)
            dots.add(d); labels.add(lb)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15))
        self.wait(0.8)

        cap2 = caption_top("A = begin contact -- ตัด addendum circle ของเฟือง 2 (ตัวตาม)", size=18)
        self.play(FadeOut(cap)); self.play(FadeIn(cap2))
        self.play(Indicate(dots[1], color=WARN, scale_factor=1.6))
        self.wait(1.0)

        cap3 = caption_top("B = end contact -- ตัด addendum circle ของเฟือง 1 (ตัวขับ)", size=18)
        self.play(FadeOut(cap2)); self.play(FadeIn(cap3))
        self.play(Indicate(dots[3], color=WARN, scale_factor=1.6))
        self.wait(1.0)

        cap4 = caption_top("มองบนเส้นเดียวกันเป็นเวกเตอร์: AE2 - E2E1 + E1B = AB", size=18)
        self.play(FadeOut(cap3)); self.play(FadeIn(cap4))
        eq = MathTex(r"\overline{AE_2}-\overline{E_2E_1}+\overline{E_1B}=\overline{AB}",
                      font_size=26, color=WHITE).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_width(eq, 4.6)
        self.play(FadeIn(eq, shift=UP * 0.15))
        self.wait(1.4)

        result = MathTex(r"Z=E_1B+E_2A-E_1E_2", font_size=28, color=OK).next_to(eq, DOWN, buff=0.5)
        box = SurroundingRectangle(result, color=OK, buff=0.18)
        self.play(FadeOut(cap4))
        self.play(FadeIn(result, shift=UP * 0.15), Create(box))
        self.wait(1.4)

        mnemonic = Text("จำง่าย: ยื่นออกจาก base circle ทั้งสองข้าง แล้วลบส่วนที่นับซ้ำ (E1E2) ทิ้ง",
                         font_size=17, color=GRAYTXT).move_to([0, -3.15, 0])
        fit_width(mnemonic, 11.5)
        self.play(FadeIn(mnemonic, shift=UP * 0.15))
        self.wait(2.0)


# =====================================================================
# G21 -- หน้า 21-22: ที่มาของ Z ขั้นที่ 2 -- E1B และ E2A เป็นสามเหลี่ยมมุมฉาก
# =====================================================================
class G21_TriangleEnds(SafeScene):
    def construct(self):
        self.add(title("ที่มาของ Z ขั้นที่ 2: E1B และ E2A", size=24))
        self.add(page_ref("หน้า 21-22"))

        fr = cr_local()
        O1, O2, E1, E2, A, B = fr["O1"], fr["O2"], fr["E1"], fr["E2"], fr["A"], fr["B"]

        cap = caption_top("E1 คือจุดสัมผัสของ line of action กับ base circle ของเฟือง 1 (pinion)", size=18)
        self.play(FadeIn(cap))

        tri1 = Polygon(O1, E1, B, color=GEAR2, stroke_width=3, fill_opacity=0.12)
        self.play(FadeIn(tri1))
        lO1 = tag("O1", O1, LEFT, GEAR2, 20, 0.15)
        self.play(FadeIn(lO1))
        self.wait(0.6)

        ra1 = ra_mark(E1, O1 - E1, B - E1, GRAYTXT, 0.2)
        self.play(Create(ra1))
        cap2 = caption_top("O1E1 ตั้งฉากกับ line of action เสมอ (นิยามของจุดสัมผัส)", size=18)
        self.play(FadeOut(cap)); self.play(FadeIn(cap2))
        self.wait(1.0)

        lbl_Rb1 = tag("R_b1", (O1 + E1) / 2, DOWN, GEAR2, 17, 0.1)
        lbl_Ro1 = tag("R_o1", (O1 + B) / 2, UP, WARN, 17, 0.12)
        self.play(FadeIn(lbl_Rb1))
        self.wait(0.4)
        self.play(FadeIn(lbl_Ro1))
        self.wait(0.5)

        cap3 = caption_top("O1B = R_o1 (B อยู่บน addendum circle ของเฟือง 1 พอดี)", size=18)
        self.play(FadeOut(cap2)); self.play(FadeIn(cap3))
        self.wait(1.0)

        eq1 = MathTex(r"E_1B=\sqrt{R_{o1}^2-R_{b1}^2}", font_size=26, color=OK)
        eq1.to_edge(RIGHT, buff=0.4).shift(UP * 1.9)
        self.play(FadeOut(cap3))
        self.play(FadeIn(eq1, shift=UP * 0.15))
        self.wait(1.2)

        cap4 = caption_top("ทำแบบเดียวกันกับเฟือง 2 (gear): สามเหลี่ยม O2-E2-A", size=19)
        self.play(FadeIn(cap4))
        tri2 = Polygon(O2, E2, A, color=GEAR3, stroke_width=3, fill_opacity=0.12)
        self.play(FadeIn(tri2))
        lO2 = tag("O2", O2, RIGHT, GEAR3, 20, 0.15)
        self.play(FadeIn(lO2))
        ra2 = ra_mark(E2, O2 - E2, A - E2, GRAYTXT, 0.2)
        self.play(Create(ra2))
        lbl_Rb2 = tag("R_b2", (O2 + E2) / 2, UP, GEAR3, 17, 0.1)
        lbl_Ro2 = tag("R_o2", (O2 + A) / 2, DOWN, WARN, 17, 0.12)
        self.play(FadeIn(lbl_Rb2), FadeIn(lbl_Ro2))
        self.wait(0.8)

        eq2 = MathTex(r"E_2A=\sqrt{R_{o2}^2-R_{b2}^2}", font_size=26, color=OK)
        eq2.next_to(eq1, DOWN, buff=0.5)
        self.play(FadeOut(cap4))
        self.play(FadeIn(eq2, shift=UP * 0.15))
        self.wait(1.6)

        box = SurroundingRectangle(VGroup(eq1, eq2), color=OK, buff=0.2)
        self.play(Create(box))
        self.wait(2.0)


# =====================================================================
# G23 -- หน้า 23: ที่มาของ Z ขั้นที่ 3: E1E2 = C sin(phi)
# =====================================================================
class G23_E1E2Formula(SafeScene):
    def construct(self):
        self.add(title("ที่มาของ Z ขั้นที่ 3: E1E2 = C sin(phi)", size=24))
        self.add(page_ref("หน้า 23"))

        fr = cr_local()
        O1, O2, P, E1, E2 = fr["O1"], fr["O2"], fr["P"], fr["E1"], fr["E2"]

        cap = caption_top("E1P และ E2P คือสองท่อนของ E1E2 -- แยกคำนวณจากสามเหลี่ยม O1-P-E1 และ O2-P-E2",
                           size=17)
        self.play(FadeIn(cap))

        loc = DashedLine(O1 + LEFT * 0.3, O2 + RIGHT * 0.3, color=GRAYTXT, stroke_width=2.5)
        self.play(Create(loc))
        # O1/O2 นั่งอยู่ "บน" เส้น loc แนวนอนพอดี -- ทิศเดิม LEFT/RIGHT จึงขนานเส้นนั้น
        # (เจอจริงจาก [LAYOUT] log 2026-09-05: ทับ DashedLine ทั้งคู่) เปลี่ยนเป็นตั้งฉาก
        # (UP/DOWN) แทน -- เลือกฝั่งที่หลบสามเหลี่ยม tri1/tri2 ที่จะวาดทีหลังด้วย (tri1
        # อยู่ใต้ O1, tri2 อยู่เหนือ-ซ้าย O2 ตรวจจากตำแหน่งจริงของ E1/E2/P แล้ว)
        for p, c, name, direc in [(O1, GEAR2, "O1", UP), (O2, GEAR3, "O2", DOWN), (P, WHITE, "P", DOWN)]:
            self.play(FadeIn(pt(p, c, 0.07)), FadeIn(tag(name, p, direc, c, 18, 0.14)), run_time=0.4)
        self.wait(0.5)

        tri1 = Polygon(O1, P, E1, color=GEAR2, stroke_width=3, fill_opacity=0.12)
        tri2 = Polygon(O2, P, E2, color=GEAR3, stroke_width=3, fill_opacity=0.12)
        self.play(FadeIn(tri1), FadeIn(tri2))
        dE1 = pt(E1, BASE_C, 0.06); tE1 = tag("E1", E1, DOWN, BASE_C, 16, 0.14)
        dE2 = pt(E2, BASE_C, 0.06); tE2 = tag("E2", E2, UP, BASE_C, 16, 0.14)
        self.play(FadeIn(dE1), FadeIn(tE1), FadeIn(dE2), FadeIn(tE2))
        self.wait(0.6)

        # มุมที่ O1 (ระหว่าง O1P กับ O1E1) และที่ O2 (ระหว่าง O2P กับ O2E2) คือ phi พอดี
        # (cos(phi)=Rb/R ตามนิยามฐาน -- ตรวจเลขจริงแล้วว่าไม่ใช่มุมที่ P ซึ่งเป็น 90-phi)
        ang1 = Angle(Line(O1, P), Line(O1, E1), radius=0.45, color=WARN, stroke_width=3)
        ang2 = Angle(Line(O2, E2), Line(O2, P), radius=0.45, color=WARN, stroke_width=3)
        lbl_phi1 = MathTex(r"\phi", font_size=22, color=WARN).move_to(
            O1 + normalize(normalize(P - O1) + normalize(E1 - O1)) * 0.68)
        lbl_phi2 = MathTex(r"\phi", font_size=22, color=WARN).move_to(
            O2 + normalize(normalize(E2 - O2) + normalize(P - O2)) * 0.68)
        cap2 = caption_top("มุมที่ O1 และที่ O2 (ระหว่างเส้นศูนย์กลางกับรัศมีไปจุดสัมผัส) = pressure angle phi",
                            size=16)
        self.play(FadeOut(cap)); self.play(FadeIn(cap2))
        self.play(Create(ang1), Create(ang2), FadeIn(lbl_phi1), FadeIn(lbl_phi2))
        self.wait(1.2)

        cap3 = caption_top("E1P = O1P sin(phi)   ,   E2P = O2P sin(phi)", size=19)
        self.play(FadeOut(cap2)); self.play(FadeIn(cap3))
        self.wait(1.0)

        deriv_rows = [
            MathTex(r"E_1E_2=E_1P+E_2P", font_size=23, color=WHITE),
            MathTex(r"=O_1P\sin\phi+O_2P\sin\phi", font_size=23, color=WHITE),
            MathTex(r"=(O_1P+O_2P)\sin\phi", font_size=23, color=WHITE),
        ]
        # fit_width ทุกแถว "ก่อน" arrange เสมอ (บทเรียนจาก G17/G18 -- scale() ย่อรอบ
        # จุดศูนย์กลางตัวเอง ถ้าย่อทีหลังตำแหน่งที่ arrange/to_edge คำนวณไว้จะไม่ตรง)
        for row in deriv_rows:
            fit_width(row, 3.8)
        deriv = VGroup(*deriv_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        deriv.to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        self.play(FadeOut(cap3))
        for row in deriv:
            self.play(FadeIn(row, shift=UP * 0.12), run_time=0.6)
            self.wait(0.6)

        result = MathTex(r"E_1E_2=C\sin\phi", font_size=26, color=OK)
        fit_width(result, 3.8)
        result.next_to(deriv, DOWN, buff=0.4)
        box = SurroundingRectangle(result, color=OK, buff=0.18)
        note = Text("C = O1P + O2P = R1 + R2", font_size=14, color=GRAYTXT)
        fit_width(note, 3.6)
        note.next_to(result, DOWN, buff=0.25)
        self.play(FadeIn(result, shift=UP * 0.15), Create(box))
        self.play(FadeIn(note))
        self.wait(2.2)


# =====================================================================
# G24 -- หน้า 24: สูตร Z สำเร็จรูป + กรณี Rack & Pinion
# =====================================================================
class G24_ZFormulaFinal(SafeScene):
    def construct(self):
        self.add(title("สูตร Z สำเร็จรูป + กรณี Rack & Pinion", size=24))
        self.add(page_ref("หน้า 24"))

        cap = caption_top("รวม 3 ขั้นที่แล้วเข้าด้วยกัน", size=21)
        self.play(FadeIn(cap))

        formula = MathTex(
            r"Z=\sqrt{R_{o1}^2-R_{b1}^2}+\sqrt{R_{o2}^2-R_{b2}^2}-C\sin\phi",
            font_size=28, color=WHITE).move_to(UP * 1.7)
        fit_width(formula, 10.5)
        box = SurroundingRectangle(formula, color=OK, buff=0.2)
        self.play(FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(1.6)

        cap2 = caption_top("กรณี rack & pinion: เฟือง 2 กลายเป็น rack (R2 -> infinity)", size=20)
        self.play(FadeOut(cap))
        # เอากรอบสูตรรวมออกก่อน -- เดิมค้างอยู่ทั้งคลิปแล้วไปทับป้าย "rack (pitch line)"
        # ที่กำลังจะโผล่ (เจอจริงจาก [LAYOUT] log 2026-09-05) ใช้แนวเดียวกับที่แก้ G17/G24
        self.play(FadeOut(formula), FadeOut(box))
        self.play(FadeIn(cap2))
        self.wait(1.0)

        O1 = LEFT * 2.2 + DOWN * 1.4
        R1_r, phi_r = 1.3, 20 * DEGREES
        Rb1_r = R1_r * np.cos(phi_r)
        pinion_c = Circle(radius=R1_r, color=PITCH_C, stroke_width=2.5).move_to(O1)
        pinion_base = Circle(radius=Rb1_r, color=BASE_C, stroke_width=3).move_to(O1)
        rack_y = O1[1] + R1_r
        rack_line = Line(LEFT * 6.6 + UP * rack_y, RIGHT * 6.9 + UP * rack_y, color=GEAR3, stroke_width=4)
        rack_lbl = tag("rack (pitch line)", RIGHT * 4.0 + UP * rack_y, UP, GEAR3, 16, 0.15)
        self.play(Create(pinion_c), Create(pinion_base), Create(rack_line), FadeIn(rack_lbl))
        self.wait(0.8)

        cap3 = caption_top("rack ไม่มี base circle ให้คำนวณ sqrt(Ro^2-Rb^2) -- ใช้ addendum line แทน",
                            size=18)
        self.play(FadeOut(cap2)); self.play(FadeIn(cap3))
        add_y = rack_y + 0.35 * R1_r
        add_line = DashedLine(LEFT * 6.6 + UP * add_y, RIGHT * 6.9 + UP * add_y, color=WARN, stroke_width=2.5)
        a_lbl = tag("addendum line (สูง a จาก pitch line)", RIGHT * 3.4 + UP * add_y, UP, WARN, 14, 0.12)
        self.play(Create(add_line), FadeIn(a_lbl))
        self.wait(1.2)

        formula2 = MathTex(
            r"Z=\sqrt{R_o^2-R_b^2}-R\sin\phi+\frac{a}{\sin\phi}",
            font_size=26, color=OK)
        formula2.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        fit_width(formula2, 4.4)
        box2 = SurroundingRectangle(formula2, color=OK, buff=0.18)
        note2 = Text("R, Rb, Ro, a เป็นค่าของ pinion ทั้งหมด", font_size=15, color=GRAYTXT)
        note2.next_to(formula2, DOWN, buff=0.2)
        self.play(FadeOut(cap3))
        self.play(FadeIn(formula2, shift=UP * 0.15), Create(box2))
        self.play(FadeIn(note2))
        self.wait(1.6)

        why = Text("พจน์สุดท้ายเปลี่ยนเป็น +a/sin(phi) เพราะช่วงขบด้าน rack ถูกจำกัดด้วยความสูง a",
                    font_size=17, color=WARN).move_to([0, -3.15, 0])
        fit_width(why, 12.0)
        self.play(FadeIn(why, shift=UP * 0.15))
        self.wait(2.2)


# =====================================================================
# G25 -- หน้า 25: ตัวอย่างเต็ม -- หา Z และ m_p (หน่วยนิ้ว)
# =====================================================================
class G25_ExampleZmp(SafeScene):
    def construct(self):
        self.add(title("ตัวอย่างเต็ม: หา Z และ m_p", size=27))
        self.add(page_ref("หน้า 25"))

        fr = cr_wide()
        O1, O2 = fr["O1"], fr["O2"]
        Rb1, Rb2, Ro1, Ro2 = fr["Rb1"], fr["Rb2"], fr["Ro1"], fr["Ro2"]
        A, B, E1, E2 = fr["A"], fr["B"], fr["E1"], fr["E2"]

        Rb1_r = CR_R1_IN * np.cos(CR_PHI)
        Rb2_r = CR_R2_IN * np.cos(CR_PHI)
        C_r = CR_R1_IN + CR_R2_IN
        Z_r = np.sqrt(CR_RO1_IN ** 2 - Rb1_r ** 2) + np.sqrt(CR_RO2_IN ** 2 - Rb2_r ** 2) \
            - C_r * np.sin(CR_PHI)
        pb_r = 2 * np.pi * Rb1_r / CR_N1
        mp_r = Z_r / pb_r

        cap = caption_top("Pinion: N1=24, R1=1.5in, Ro1=1.625in | Gear: N2=60, R2=3.75in, Ro2=3.875in, phi=20°",
                           size=15)
        self.play(FadeIn(cap))

        base1 = Circle(radius=Rb1, color=BASE_C, stroke_width=3).move_to(O1)
        base2 = Circle(radius=Rb2, color=BASE_C, stroke_width=3).move_to(O2)
        add1 = DashedVMobject(Circle(radius=Ro1, color=GEAR2, stroke_width=2.5).move_to(O1), num_dashes=30)
        add2 = DashedVMobject(Circle(radius=Ro2, color=GEAR3, stroke_width=2.5).move_to(O2), num_dashes=48)
        self.play(Create(base1), Create(base2), Create(add1), Create(add2))
        self.wait(0.5)

        loa_ext = Line(E1 - fr["d"] * 0.5, E2 + fr["d"] * 0.5, color=LOA_C, stroke_width=3)
        path = Line(A, B, color=WARN, stroke_width=6)
        self.play(Create(loa_ext), Create(path))
        self.wait(0.6)

        cap2 = caption_top("ขั้น 1 -- โจทย์ให้ R, Ro ครบแล้ว ต้องหา Rb, C ก่อน", size=19)
        self.play(FadeOut(cap)); self.play(FadeIn(cap2))
        self.wait(1.0)

        steps = VGroup(
            Text("ขั้น 2 -- สูตร:", font_size=18, color=WHITE),
            MathTex(r"R_{b1}=1.5\cos20^\circ=1.409\text{ in}", font_size=19, color=BASE_C),
            MathTex(r"R_{b2}=3.75\cos20^\circ=3.524\text{ in}", font_size=19, color=BASE_C),
            MathTex(r"C=1.5+3.75=5.25\text{ in}", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for row in steps:
            fit_width(row, 4.6)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        steps.to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        self.play(FadeOut(cap2))
        for row in steps:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(1.2)

        cap3 = caption_top("ขั้น 3 -- แทนค่าหา Z", size=20)
        self.play(FadeIn(cap3))
        z_eq = VGroup(
            MathTex(r"Z=\sqrt{1.625^2-1.409^2}+\sqrt{3.875^2-3.524^2}-5.25\sin20^\circ",
                    font_size=17, color=WHITE),
            MathTex(rf"Z=0.8095+1.6116-1.7956=\mathbf{{{Z_r:.4f}}}\text{{ in}}",
                    font_size=19, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for row in z_eq:
            fit_width(row, 6.5)
        z_eq.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        z_eq.move_to([0, -2.55, 0])
        self.play(FadeIn(z_eq[0], shift=UP * 0.1))
        self.wait(0.8)
        self.play(FadeIn(z_eq[1], shift=UP * 0.1))
        self.wait(1.4)

        self.play(FadeOut(cap3))
        cap4 = caption_top("ขั้น 3 (ต่อ) -- หา p_b แล้วหา m_p", size=20)
        self.play(FadeIn(cap4))
        mp_eq = VGroup(
            MathTex(rf"p_b=\frac{{2\pi(1.409)}}{{24}}={pb_r:.4f}\text{{ in}}", font_size=19, color=WHITE),
            MathTex(rf"m_p=\frac{{{Z_r:.4f}}}{{{pb_r:.4f}}}=\mathbf{{{mp_r:.2f}}}", font_size=22, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for row in mp_eq:
            fit_width(row, 6.0)
        mp_eq.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        mp_eq.next_to(z_eq, DOWN, buff=0.35)
        box = SurroundingRectangle(mp_eq[1], color=OK, buff=0.15)
        self.play(FadeIn(mp_eq[0], shift=UP * 0.1))
        self.wait(0.8)
        self.play(FadeIn(mp_eq[1], shift=UP * 0.1), Create(box))
        self.wait(1.6)

        self.play(FadeOut(cap4))
        concl = Text(f"ขั้น 4 -- ตรวจ: m_p={mp_r:.2f} > 1.40 -> เดินเรียบ ผ่านเกณฑ์",
                     font_size=18, color=OK).move_to([0, -3.15, 0])
        self.play(FadeIn(concl, shift=UP * 0.15))
        self.wait(2.4)


# =====================================================================
# G26 -- หน้า 26: เงื่อนไขที่เฟืองสองตัวจะขบกันได้ + Module
# =====================================================================
class G26_MeshingCondition(SafeScene):
    def construct(self):
        self.add(title("เงื่อนไขที่เฟืองสองตัวขบกันได้ + Module", size=25))
        self.add(page_ref("หน้า 26"))

        cap = caption_top("ลองเอาเฟือง 2 คู่มาขบกัน -- คู่หนึ่งฟันขนาดเท่ากัน อีกคู่ไม่เท่ากัน", size=19)
        self.play(FadeIn(cap))

        # คู่บน: p เท่ากัน (ขบกันได้)
        g1a = gear_shape(0.7, 14, GEAR2).move_to(LEFT * 2.2 + UP * 1.3)
        g1b = gear_shape(0.7, 14, GEAR3).move_to(g1a.get_center() + RIGHT * 1.5)
        ok_lbl = tag("p เท่ากัน -> ขบได้", g1a.get_center() + LEFT * 1.1, LEFT, OK, 16, 0.15)
        # คู่ล่าง: p ไม่เท่ากัน (ฟันคนละขนาด -- ขบไม่สนิท)
        g2a = gear_shape(0.7, 10, GEAR2).move_to(LEFT * 2.2 + DOWN * 1.3)
        g2b = gear_shape(0.9, 22, WARN).move_to(g2a.get_center() + RIGHT * 1.7)
        bad_lbl = tag("p ไม่เท่ากัน -> ขบไม่สนิท", g2a.get_center() + LEFT * 1.1, LEFT, WARN, 16, 0.15)
        self.play(FadeIn(g1a, shift=UP * 0.2), FadeIn(g1b, shift=UP * 0.2), FadeIn(ok_lbl))
        self.play(FadeIn(g2a, shift=DOWN * 0.2), FadeIn(g2b, shift=DOWN * 0.2), FadeIn(bad_lbl))
        spin(g1a, 1.6); spin(g1b, -1.6)
        spin(g2a, 1.4); spin(g2b, -1.4 * (10 / 22))
        self.wait(1.6)
        g1a.clear_updaters(); g1b.clear_updaters()
        g2a.clear_updaters(); g2b.clear_updaters()
        self.play(FadeOut(cap))

        cond = VGroup(
            Text("เฟืองตรง 2 ตัวจะขบกันได้ถูกต้อง ก็ต่อเมื่อ:", font_size=20, color=WHITE),
            Text("มี circular pitch (p) เท่ากัน -- เงื่อนไขหลัก", font_size=18, color=OK),
            Text("1) center distance ถูกต้อง: C = R1 + R2 (ไม่มี backlash)", font_size=17, color=GRAYTXT),
            Text("2) ไม่เกิด interference: N > N_min = 2a/(m sin^2 phi)", font_size=17, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cond.to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        cap2 = caption_top("สรุปเป็นเงื่อนไขทางการ", size=20)
        self.play(FadeIn(cap2))
        for row in cond:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(1.6)

        self.play(FadeOut(cap2), FadeOut(cond))
        module_formula = MathTex(r"m=\frac{D}{N},\qquad D=2R\ \ (\text{pitch diameter})",
                                  font_size=28, color=WHITE).move_to(UP * 1.5)
        fit_width(module_formula, 9.0)
        box = SurroundingRectangle(module_formula, color=OK, buff=0.2)
        cap3 = caption_top("Module = 'ขนาดของฟัน'", size=22)
        self.play(FadeIn(cap3))
        self.play(FadeIn(module_formula, shift=UP * 0.15), Create(box))
        self.wait(1.4)

        why = Text("ทำไม 'pitch เท่ากัน' ถึงเป็นเงื่อนไขหลัก: p = pi m",
                    font_size=19, color=WHITE).move_to(DOWN * 0.6)
        why2 = Text("-> pitch เท่ากัน = module เท่ากัน = ฟันขนาดเดียวกัน",
                     font_size=19, color=OK).next_to(why, DOWN, buff=0.25)
        why3 = Text("ฟันคนละขนาดขบกันไม่ลง เหมือนเอาน็อตคนละเกลียวมาขัน",
                     font_size=17, color=GRAYTXT).next_to(why2, DOWN, buff=0.25)
        self.play(FadeOut(cap3))
        self.play(FadeIn(why, shift=UP * 0.1))
        self.wait(0.6)
        self.play(FadeIn(why2, shift=UP * 0.1))
        self.wait(0.6)
        self.play(FadeIn(why3, shift=UP * 0.1))
        self.wait(2.0)


# =====================================================================
# G27 -- หน้า 27: แนวคิดการผลิตเฟือง
# =====================================================================
class G27_ManufacturingConcept(SafeScene):
    def construct(self):
        self.add(title("แนวคิดการผลิตเฟือง", size=28))
        self.add(page_ref("หน้า 27"))

        cap = caption_top("แนวคิดพื้นฐาน: ใช้มีดตัดรูปร่างเหมือนเฟือง ไปตัดเฟืองอีกตัวหนึ่ง", size=20)
        self.play(FadeIn(cap))

        blank = Circle(radius=1.3, color=GRAYTXT, stroke_width=3).move_to(LEFT * 2.6)
        blank_lbl = tag("gear blank", blank.get_center() + DOWN * 1.55, DOWN, GRAYTXT, 16, 0.1)
        cutter = gear_shape(0.55, 10, WARN).move_to(LEFT * 2.6 + RIGHT * 1.85)
        cutter_lbl = tag("มีดตัด (rack/gear)", cutter.get_center() + UP * 0.85, UP, WARN, 16, 0.1)
        self.play(Create(blank), FadeIn(blank_lbl))
        self.play(FadeIn(cutter, shift=LEFT * 0.2), FadeIn(cutter_lbl))
        self.wait(1.2)

        table = VGroup(
            Text("วิธี", font_size=18, color=WHITE),
            Text("มีดตัดรูปร่างเหมือน", font_size=18, color=WHITE),
            Text("ตัดเฟืองในได้ไหม", font_size=18, color=WHITE),
        ).arrange(RIGHT, buff=0.6)
        row1 = VGroup(
            Text("Hobbing", font_size=18, color=PITCH_C),
            Text("rack", font_size=18, color=PITCH_C),
            Text("ไม่ได้", font_size=18, color=WARN),
        ).arrange(RIGHT, buff=0.9)
        row2 = VGroup(
            Text("Fellows method", font_size=18, color=GEAR3),
            Text("เฟือง", font_size=18, color=GEAR3),
            Text("ได้ (internal gear)", font_size=18, color=OK),
        ).arrange(RIGHT, buff=0.55)
        tbl = VGroup(table, row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        tbl.to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        cap2 = caption_top("2 วิธีหลักในการตัดเฟือง", size=21)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2))
        self.play(FadeIn(tbl, shift=RIGHT * 0.2))
        self.wait(2.4)


# =====================================================================
# G28 -- หน้า 28: Gear Rack และหลักการ hob
# =====================================================================
class G28_RackAndHob(SafeScene):
    def construct(self):
        self.add(title("Gear Rack และหลักการ Hob", size=27))
        self.add(page_ref("หน้า 28"))

        cap = caption_top("Rack = เฟืองที่ R_b = infinity -- อินโวลูทกลายเป็นเส้นตรง", size=21)
        self.play(FadeIn(cap))

        O = LEFT * 2.4 + DOWN * 1.5
        R1_r, phi_r = 1.3, 20 * DEGREES
        Rb1_r = R1_r * np.cos(phi_r)
        pinion_c = Circle(radius=R1_r, color=PITCH_C, stroke_width=2.5).move_to(O)
        pinion_base = Circle(radius=Rb1_r, color=BASE_C, stroke_width=3).move_to(O)
        rack_y = O[1] + R1_r
        rack_line = Line(LEFT * 6.6 + UP * rack_y, RIGHT * 6.9 + UP * rack_y, color=GEAR3, stroke_width=4)
        rack_lbl = tag("rack (มีดตัด / hob)", RIGHT * 3.6 + UP * rack_y, UP, GEAR3, 16, 0.15)
        self.play(Create(pinion_c), Create(pinion_base), Create(rack_line), FadeIn(rack_lbl))
        self.wait(1.0)

        note = Text("ผลิตมีดตัด (hob) หน้าตัดตรงได้ง่ายและแม่นยำมาก", font_size=18, color=OK)
        note.move_to([0, -3.15, 0])
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(1.2)

        self.play(FadeOut(cap), FadeOut(note))
        cap2 = caption_top("ผลที่ตามมาเวลาใช้ hob ตัดเฟือง", size=21)
        self.play(FadeIn(cap2))

        table = VGroup(
            Text("Circular pitch p  = pitch ของ rack (มีด)", font_size=17, color=WHITE),
            Text("Dedendum b  = addendum ของ rack", font_size=17, color=GEAR3),
            Text("Addendum a  = R_o - R -> ขึ้นกับขนาด gear blank", font_size=17, color=WARN),
            Text("R = pN/(2 pi) -> กำหนดโดยความเร็วหมุนที่จูนกับ hob", font_size=17, color=PITCH_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for row in table:
            fit_width(row, 6.0)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        table.to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        for row in table:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(2.4)


# =====================================================================
# G29 -- หน้า 29-30: ภาพวิธี Hobbing และ Fellows shaping
# =====================================================================
class G29_HobbingFellows(SafeScene):
    def construct(self):
        self.add(title("กระบวนการ Hobbing และ Fellows Shaping", size=25))
        self.add(page_ref("หน้า 29-30"))

        cap = caption_top("Hobbing -- hob (สกรูมีฟัน) หมุนกินเนื้อชิ้นงานทีละนิด", size=20)
        self.play(FadeIn(cap))

        blank1 = Circle(radius=1.1, color=GRAYTXT, stroke_width=3).move_to(LEFT * 2.8 + UP * 1.2)
        hob = gear_shape(0.45, 8, WARN).move_to(blank1.get_center() + RIGHT * 1.55)
        hob_lbl = tag("hob (หมุน+เลื่อน)", hob.get_center() + UP * 0.75, UP, WARN, 15, 0.1)
        blank1_lbl = tag("gear blank (หมุนช้าตาม)", blank1.get_center() + DOWN * 1.35, DOWN, GRAYTXT, 15, 0.1)
        self.play(Create(blank1), FadeIn(blank1_lbl))
        self.play(FadeIn(hob, shift=LEFT * 0.15), FadeIn(hob_lbl))
        spin(blank1, 0.5); spin(hob, -0.5 * (1.1 / 0.45))
        self.wait(1.8)
        blank1.clear_updaters(); hob.clear_updaters()

        self.play(FadeOut(cap))
        cap2 = caption_top("Fellows shaping -- ใช้เฟืองมีดชักขึ้น-ลง สลับกับหมุนทีละนิด", size=20)
        self.play(FadeIn(cap2))

        blank2 = Circle(radius=1.1, color=GRAYTXT, stroke_width=3).move_to(LEFT * 2.8 + DOWN * 1.2)
        shaper = gear_shape(0.65, 12, OK).move_to(blank2.get_center() + RIGHT * 1.75)
        shaper_lbl = tag("shaper cutter (ชักขึ้น-ลง)", shaper.get_center() + UP * 0.95, UP, OK, 15, 0.1)
        blank2_lbl = tag("gear blank", blank2.get_center() + DOWN * 1.35, DOWN, GRAYTXT, 15, 0.1)
        self.play(Create(blank2), FadeIn(blank2_lbl))
        self.play(FadeIn(shaper, shift=LEFT * 0.15), FadeIn(shaper_lbl))
        spin(blank2, 0.4); spin(shaper, -0.4 * (1.1 / 0.65))
        self.wait(1.6)
        blank2.clear_updaters(); shaper.clear_updaters()

        note = Text("ข้อดี Fellows: ใช้มีดรูปเฟือง (ไม่ใช่ rack) จึงตัด internal gear ได้",
                     font_size=17, color=OK).move_to([0, -3.15, 0])
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(2.0)


# =====================================================================
# G31 -- หน้า 31: สัดส่วนฟันมาตรฐาน (British vs German)
# =====================================================================
class G31_StandardProportions(SafeScene):
    def construct(self):
        self.add(title("สัดส่วนฟันมาตรฐาน", size=28))
        self.add(page_ref("หน้า 31"))

        cap = caption_top("4 พารามิเตอร์ที่กำหนดรูป/ขนาดฟัน", size=21)
        self.play(FadeIn(cap))

        headers = VGroup(
            Text("พารามิเตอร์", font_size=18, color=WHITE),
            Text("British", font_size=18, color=PITCH_C),
            Text("German", font_size=18, color=GEAR3),
        ).arrange(RIGHT, buff=1.1)
        rows_txt = [
            ("Module m", "m", "m"),
            ("Addendum a", "1.000 m", "1.000 m"),
            ("Dedendum b", "1.250 m", "1.157-1.167 m"),
            ("Pressure angle phi", "20 deg", "20 deg"),
        ]
        rows = VGroup()
        for name, br, ge in rows_txt:
            r = VGroup(
                Text(name, font_size=17, color=GRAYTXT),
                Text(br, font_size=17, color=PITCH_C),
                Text(ge, font_size=17, color=GEAR3),
            ).arrange(RIGHT, buff=0.5)
            rows.add(r)
        tbl = VGroup(headers, *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        tbl.move_to(UP * 0.5)
        self.play(FadeOut(cap))
        for r in tbl:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.5)
        self.wait(1.4)

        formula = MathTex(r"m=\frac{D}{N}=\frac{p}{\pi},\qquad t=\frac{p}{2}",
                           font_size=24, color=OK).next_to(tbl, DOWN, buff=0.5)
        fit_width(formula, 8.0)
        self.play(FadeIn(formula, shift=UP * 0.15))
        self.wait(1.2)

        why = Text("ทำไม b > a: ต้องเผื่อ clearance ที่โคนฟัน (b - a = 0.25m แบบ British)",
                    font_size=17, color=WARN).move_to([0, -3.15, 0])
        fit_width(why, 12.0)
        self.play(FadeIn(why, shift=UP * 0.15))
        self.wait(2.2)


# =====================================================================
# G32 -- หน้า 32: ระบบวัดขนาดฟัน US vs Metric
# =====================================================================
class G32_USvsMetric(SafeScene):
    def construct(self):
        self.add(title("ระบบวัดขนาดฟัน: US vs Metric", size=27))
        self.add(page_ref("หน้า 32"))

        cap = caption_top("สองระบบเป็นส่วนกลับกัน (reciprocal) -- กับดักข้อสอบยอดฮิต", size=20)
        self.play(FadeIn(cap))

        us_col = VGroup(
            Text("U.S. -- Diametral Pitch", font_size=20, color=PITCH_C),
            MathTex(r"P_d=\frac{N}{D}\ \ (\text{inch}^{-1})", font_size=24, color=PITCH_C),
            Text("P_d มาก -> ฟันเล็ก", font_size=17, color=GRAYTXT),
        ).arrange(DOWN, buff=0.3).move_to(LEFT * 3.2)
        metric_col = VGroup(
            Text("Metric -- Module", font_size=20, color=GEAR3),
            MathTex(r"m=\frac{D}{N}\ \ (\text{mm})", font_size=24, color=GEAR3),
            Text("m มาก -> ฟันใหญ่", font_size=17, color=GRAYTXT),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.2)
        self.play(FadeOut(cap))
        self.play(FadeIn(us_col, shift=UP * 0.15))
        self.wait(0.8)
        self.play(FadeIn(metric_col, shift=UP * 0.15))
        self.wait(1.2)

        formula = MathTex(r"m=\frac{1}{P_d}", font_size=32, color=OK).move_to(DOWN * 1.6)
        box = SurroundingRectangle(formula, color=OK, buff=0.2)
        self.play(FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(1.4)

        trap = Text("กับดัก: โจทย์อเมริกันชอบให้ '5 Pitch' มา = P_d=5 -> D=N/5 นิ้ว",
                     font_size=17, color=WARN).move_to([0, -3.15, 0])
        fit_width(trap, 12.0)
        self.play(FadeIn(trap, shift=UP * 0.15))
        self.wait(2.2)


# =====================================================================
# G33 -- หน้า 33: ตัวอย่างออกแบบเฟือง 13 ฟัน module 3
# =====================================================================
class G33_ExampleDesign13Teeth(SafeScene):
    def construct(self):
        self.add(title("ตัวอย่าง: ออกแบบเฟือง 13 ฟัน Module 3", size=25))
        self.add(page_ref("หน้า 33"))

        N, m, phi_deg = 13, 3.0, 20
        phi = phi_deg * DEGREES
        a, b = 1.000 * m, 1.250 * m
        p = np.pi * m
        t = p / 2
        R = m * N / 2
        Ro = R + a
        Ri = R - b
        Rb = R * np.cos(phi)
        D_blank = 2 * Ro

        cap = caption_top("โจทย์: 13 ฟัน module 3, British standard -- หาสัดส่วนทั้งหมด", size=18)
        self.play(FadeIn(cap))

        O = LEFT * 3.4 + DOWN * 0.2
        s = 0.35  # สเกลย่อวาด (ตัวเลขจริงหน่วย mm ใหญ่กว่าจอ)
        c_Ro = Circle(radius=Ro * s, color=GEAR3, stroke_width=2.5).move_to(O)
        c_R = Circle(radius=R * s, color=PITCH_C, stroke_width=3).move_to(O)
        c_Rb = Circle(radius=Rb * s, color=BASE_C, stroke_width=2.5).move_to(O)
        c_Ri = Circle(radius=Ri * s, color=GRAYTXT, stroke_width=2.5).move_to(O)
        self.play(Create(c_Ro), Create(c_R), Create(c_Rb), Create(c_Ri))
        self.wait(0.8)

        given = Text("British: a=1.000m, b=1.250m, phi=20 deg", font_size=16, color=GRAYTXT)
        given.next_to(O, DOWN, buff=Ro * s + 0.4)
        self.play(FadeOut(cap))
        cap2 = caption_top("ขั้น 1 -- ดึงค่ามาตรฐานออกมาก่อน (British)", size=20)
        self.play(FadeIn(cap2), FadeIn(given))
        self.wait(1.0)

        table = VGroup(
            Text(f"(ก) t = p/2 = {t:.3f} mm", font_size=17, color=WHITE),
            Text(f"(ข) R = mN/2 = {R:.1f} mm", font_size=17, color=PITCH_C),
            Text(f"(ค) gear blank D = 2R_o = {D_blank:.1f} mm", font_size=17, color=GEAR3),
            Text(f"(ง) R_i = R - b = {Ri:.2f} mm", font_size=17, color=GRAYTXT),
            Text(f"(จ) R_b = R cos(phi) = {Rb:.3f} mm", font_size=17, color=BASE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for row in table:
            fit_width(row, 5.2)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        table.to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        self.play(FadeOut(cap2))
        cap3 = caption_top("ขั้น 2-3 -- สูตร + แทนค่าทีละข้อ", size=20)
        self.play(FadeIn(cap3))
        for row in table:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(1.4)

        self.play(FadeOut(cap3), FadeOut(given))
        order = MathTex(
            rf"R_i({Ri:.2f}) < R_b({Rb:.2f}) < R({R:.1f}) < R_o({Ro:.1f})",
            font_size=22, color=OK)
        fit_width(order, 10.5)
        order.move_to(UP * 1.6)
        cap4 = caption_top("ขั้น 4 -- ตรวจ: ลำดับรัศมีถูกต้อง", size=20)
        self.play(FadeIn(cap4))
        self.play(FadeIn(order, shift=UP * 0.15))
        self.wait(1.4)

        # ---- กับดัก: undercut check ------------------------------------------
        self.play(FadeOut(cap4))
        Nmin = 2 * 1.0 / (np.sin(phi) ** 2)
        cap5 = caption_top(f"กับดัก: N=13 แต่ full-depth phi=20 ต้องการ N_min = {Nmin:.1f}", size=19)
        self.play(FadeIn(cap5))
        warn_txt = VGroup(
            Text(f"13 < {Nmin:.1f} -> เฟืองนี้จะถูก undercut ตอนตัดด้วย hob!",
                 font_size=19, color=WARN),
            Text("ฟันจะคอดที่โคน อ่อนแอ", font_size=17, color=WARN),
            Text("ทางแก้: เพิ่ม phi เป็น 25 deg (N_min=11.2 ผ่าน) หรือใช้ profile shift",
                 font_size=16, color=GRAYTXT),
        ).arrange(DOWN, buff=0.2)
        fit_width(warn_txt, 10.5)
        warn_txt.move_to(DOWN * 0.8)
        self.play(FadeIn(warn_txt, shift=UP * 0.15))
        self.wait(1.6)

        concl = Text("ถ้าข้อสอบถามว่า 'ผลิตได้ไหม' -> ตอบ 'ผลิตได้แต่จะ undercut' ไม่ใช่แค่เลข",
                      font_size=17, color=OK).move_to([0, -3.15, 0])
        fit_width(concl, 12.5)
        self.play(FadeIn(concl, shift=UP * 0.15))
        self.wait(2.4)


# =====================================================================
# G34 -- หน้า 34: Involute Interference คืออะไร
# =====================================================================
class G34_InterferenceDef(SafeScene):
    def construct(self):
        self.add(title("Involute Interference คืออะไร", size=26))
        self.add(page_ref("หน้า 34"))

        cap = caption_top("Interference = ฟันสัมผัสกันต่ำกว่า base circle (นอกช่วง E1E2)", size=20)
        self.play(FadeIn(cap))

        # แผนภาพช่วงปกติ (ไม่ scale ตามจริง -- เน้นให้เห็น "ลำดับจุด" บนเส้นเดียวกัน)
        y0 = 1.0
        line1 = Line(LEFT * 5.5 + UP * y0, RIGHT * 5.5 + UP * y0, color=LOA_C, stroke_width=3)
        pts_ok = [(-4.5, "E1"), (-2.0, "A"), (0.0, "P"), (2.0, "B"), (4.5, "E2")]
        ok_dots = VGroup(); ok_lbls = VGroup()
        for x, name in pts_ok:
            p = np.array([x, y0, 0])
            c = BASE_C if name in ("E1", "E2") else (WARN if name in ("A", "B") else WHITE)
            ok_dots.add(pt(p, c, 0.06))
            ok_lbls.add(tag(name, p, UP, c, 16, 0.12))
        lbl_ok = Text("ปกติ (ไม่ interference): A อยู่ระหว่าง E1-P, B อยู่ระหว่าง P-E2",
                       font_size=16, color=OK).next_to(line1, UP, buff=0.55)
        self.play(Create(line1), FadeIn(ok_dots), FadeIn(ok_lbls), FadeIn(lbl_ok))
        self.wait(1.2)

        self.play(FadeOut(cap))
        cap2 = caption_top("แต่ถ้าเฟือง 2 (ตัวตาม) มีฟันน้อยไป -- addendum circle ยื่นเลย E1 ออกไป", size=18)
        self.play(FadeIn(cap2))

        y1 = -1.4
        line2 = Line(LEFT * 5.5 + UP * y1, RIGHT * 5.5 + UP * y1, color=LOA_C, stroke_width=3)
        # ผิดปกติ: A อยู่เลย E1 ออกไป (ซ้ายกว่า E1) -- นี่คือ interference
        pts_bad = [(-2.0, "A", WARN), (-1.3, "E1", BASE_C), (0.0, "P", WHITE),
                   (2.0, "B", WARN), (4.5, "E2", BASE_C)]
        bad_dots = VGroup(); bad_lbls = VGroup()
        for x, name, c in pts_bad:
            p = np.array([x, y1, 0])
            bad_dots.add(pt(p, c, 0.06))
            direc = DOWN if name in ("A", "E1") else UP
            bad_lbls.add(tag(name, p, direc, c, 16, 0.14))
        overlap = Line(np.array([-2.0, y1, 0]), np.array([-1.3, y1, 0]), color=WARN, stroke_width=8)
        lbl_bad = Text("A อยู่เลย E1 ออกไป (ซ้ายกว่า) = interference!",
                        font_size=16, color=WARN).next_to(line2, DOWN, buff=0.55)
        self.play(Create(line2), FadeIn(bad_dots), FadeIn(bad_lbls))
        self.play(Create(overlap), FadeIn(lbl_bad))
        self.wait(1.4)

        self.play(FadeOut(cap2))
        cap3 = caption_top("เกิดขึ้นจริงเมื่อ: pinion ฟันน้อย (N1=13) ขบกับเฟืองใหญ่ (N2=60) module 3", size=17)
        self.play(FadeIn(cap3))

        # ตัวเลขจริง (ตรวจแล้วด้วยเลขจริง -- ไม่ใช่แค่ภาพประกอบลอยๆ)
        phi = 20 * DEGREES
        N1, N2, m = 13, 60, 3.0
        R1, R2 = m * N1 / 2, m * N2 / 2
        a_add = 1.000 * m
        Ro1, Ro2 = R1 + a_add, R2 + a_add
        Rb1, Rb2 = R1 * np.cos(phi), R2 * np.cos(phi)
        C = R1 + R2
        E1B = np.sqrt(Ro1 ** 2 - Rb1 ** 2)
        E2A = np.sqrt(Ro2 ** 2 - Rb2 ** 2)
        E1E2 = C * np.sin(phi)

        nums = VGroup(
            Text(f"E1B = sqrt(Ro1^2-Rb1^2) = {E1B:.2f} mm", font_size=17, color=BASE_C),
            Text(f"E2A = sqrt(Ro2^2-Rb2^2) = {E2A:.2f} mm", font_size=17, color=WARN),
            Text(f"E1E2 = C sin(phi) = {E1E2:.2f} mm", font_size=17, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for row in nums:
            fit_width(row, 5.5)
        nums.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        nums.to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        self.play(FadeOut(cap3))
        for row in nums:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(1.0)

        crit = MathTex(rf"E_2A({E2A:.2f}) > E_1E_2({E1E2:.2f})\ \Rightarrow\ \text{{interference}}",
                        font_size=22, color=WARN)
        fit_width(crit, 5.5)
        crit.next_to(nums, DOWN, buff=0.35)
        box = SurroundingRectangle(crit, color=WARN, buff=0.15)
        self.play(FadeIn(crit, shift=UP * 0.1), Create(box))
        self.wait(1.4)

        rule = Text("วิธีเช็คเร็วในข้อสอบ: หา E1B, E2A แล้วเทียบกับ E1E2 = C sin(phi)",
                     font_size=17, color=OK).move_to([0, -3.15, 0])
        fit_width(rule, 12.0)
        self.play(FadeIn(rule, shift=UP * 0.15))
        self.wait(2.2)


# =====================================================================
# G35 -- หน้า 35: ที่มาสูตร N_min จาก Rack & Pinion Interference
# =====================================================================
class G35_NminDerivation(SafeScene):
    def construct(self):
        self.add(title("ที่มาสูตร N_min จาก Rack & Pinion", size=25))
        self.add(page_ref("หน้า 35"))

        cap = caption_top("จุดวิกฤต E = จุดสัมผัสของ line of action กับ base circle ของ pinion", size=19)
        self.play(FadeIn(cap))

        O = LEFT * 2.6 + DOWN * 1.3
        R1_r, phi_r = 1.3, 20 * DEGREES
        Rb1_r = R1_r * np.cos(phi_r)
        pinion_c = Circle(radius=R1_r, color=PITCH_C, stroke_width=2.5).move_to(O)
        pinion_base = Circle(radius=Rb1_r, color=BASE_C, stroke_width=3).move_to(O)
        P = O + UP * R1_r
        rack_y = P[1]
        rack_line = Line(LEFT * 6.6 + UP * rack_y, RIGHT * 6.9 + UP * rack_y, color=GEAR3, stroke_width=4)
        self.play(Create(pinion_c), Create(pinion_base), Create(rack_line))
        dP = pt(P, WHITE, 0.06)
        tPp = tag("P", P, UL, WHITE, 18, 0.15)
        self.play(FadeIn(dP), FadeIn(tPp))
        self.wait(0.6)

        # เส้น line of action ผ่าน P ทำมุม phi กับแนวราบ (rack pitch line) -- ตรวจด้วย
        # เลขจริงก่อนใช้: มุม phi ต้องอยู่ "ที่ O" (ระหว่าง OP กับ OE) ไม่ใช่ที่ P เพราะ
        # Rb=Rcos(phi) นิยามมุมที่ O เสมอ (เหมือนบั๊กที่เจอและแก้แล้วใน G23) ทิศแรก
        # (sin,-cos) ให้มุมที่ O = 90-phi สลับ Rb กับ PE กัน (ตรวจได้ |O-E|=Rsin(phi)
        # ผิดจากที่ควรเป็น Rb) ที่ถูกต้องคือ (cos,-sin) -- ตรวจแล้ว |O-E|=Rb, |P-E|=Rsin(phi)
        d_loa = np.array([np.cos(phi_r), -np.sin(phi_r), 0.0])
        loa = Line(P - d_loa * 0.6, P + d_loa * 2.6, color=LOA_C, stroke_width=3)
        E_pt = P + float(np.dot(O - P, d_loa)) * d_loa
        dE = pt(E_pt, BASE_C, 0.06)
        tE = tag("E", E_pt, DL, BASE_C, 18, 0.18)
        cap2 = caption_top("E: จุดสัมผัสของ line of action กับ base circle -- ระยะ PE = R sin(phi)", size=18)
        self.play(FadeOut(cap)); self.play(FadeIn(cap2))
        self.play(Create(loa))
        self.play(FadeIn(dE), FadeIn(tE))
        seg_PE = seg(P, E_pt, WARN, 4)
        self.wait(0.8)

        eq1 = MathTex(r"\overline{PE}=R\sin\phi", font_size=26, color=WARN)
        eq1.to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
        self.play(FadeIn(eq1, shift=UP * 0.15))
        self.wait(1.2)

        cap3 = caption_top("addendum ของ rack ที่ตรงกับจุด E พอดี: a' = PE sin(phi)", size=19)
        self.play(FadeOut(cap2)); self.play(FadeIn(cap3))
        a_prime_y = E_pt[1]
        add_line = DashedLine(np.array([-6.6, a_prime_y, 0]), np.array([6.9, a_prime_y, 0]),
                               color=WARN, stroke_width=2.5)
        a_prime_lbl = tag("a' (addendum line ที่จุดวิกฤต)", RIGHT * 3.0 + UP * a_prime_y,
                           DOWN, WARN, 14, 0.15)
        self.play(Create(add_line), FadeIn(a_prime_lbl))
        self.wait(1.0)

        eq2 = MathTex(r"a'=\overline{PE}\sin\phi=R\sin^2\phi", font_size=24, color=WARN)
        eq2.next_to(eq1, DOWN, buff=0.5)
        self.play(FadeOut(cap3))
        self.play(FadeIn(eq2, shift=UP * 0.15))
        self.wait(1.4)

        cap4 = caption_top("เงื่อนไขไม่ interference: addendum จริง a ต้องน้อยกว่า a'", size=20)
        self.play(FadeIn(cap4))
        eq3 = MathTex(r"a<a'=R\sin^2\phi", font_size=26, color=OK)
        eq3.next_to(eq2, DOWN, buff=0.5)
        box1 = SurroundingRectangle(eq3, color=OK, buff=0.15)
        self.play(FadeOut(cap4))
        self.play(FadeIn(eq3, shift=UP * 0.15), Create(box1))
        self.wait(1.6)

        self.play(FadeOut(VGroup(eq1, eq2, eq3, box1)))
        cap5 = caption_top("แทน R = mN/2 แล้วจัดรูปหา N", size=21)
        self.play(FadeIn(cap5))
        deriv = VGroup(
            MathTex(r"a<\frac{mN\sin^2\phi}{2}", font_size=26, color=WHITE),
            MathTex(r"N>\frac{2a}{m\sin^2\phi}", font_size=28, color=OK),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        for row in deriv:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.7)
            self.wait(0.6)
        box2 = SurroundingRectangle(deriv[1], color=OK, buff=0.15)
        self.play(Create(box2))
        self.wait(1.2)

        self.play(FadeOut(cap5))
        cap6 = caption_top("แทน a = km (k=1 full-depth, k=0.8 stub)", size=21)
        self.play(FadeIn(cap6))
        final = MathTex(r"N_{min}=\frac{2k}{\sin^2\phi}", font_size=34, color=OK).move_to(DOWN * 1.6)
        box3 = SurroundingRectangle(final, color=OK, buff=0.2)
        self.play(FadeOut(cap6))
        self.play(FadeIn(final, shift=UP * 0.15), Create(box3))
        self.wait(1.6)

        golden = Text('"ถ้าเฟืองขบกับ rack ได้โดยไม่ interference แล้ว จะขบกับเฟืองอื่นได้ทุกตัว"',
                       font_size=16, color=WARN).move_to([0, -3.15, 0])
        fit_width(golden, 12.5)
        self.play(FadeIn(golden, shift=UP * 0.15))
        self.wait(2.4)


# =====================================================================
# G36 -- หน้า 36: Undercutting ตอนผลิตด้วย hob
# =====================================================================
class G36_Undercutting(SafeScene):
    def construct(self):
        self.add(title("Undercutting ตอนผลิตด้วย Hob", size=27))
        self.add(page_ref("หน้า 36"))

        cap = caption_top("N_min = จำนวนฟันเล็กสุดที่ตัดด้วย hob ได้โดยไม่ undercut", size=20)
        self.play(FadeIn(cap))

        formula = MathTex(r"N_{min}=\frac{2k}{\sin^2\phi}", font_size=34, color=OK).move_to(UP * 1.5)
        box = SurroundingRectangle(formula, color=OK, buff=0.2)
        self.play(FadeIn(formula, shift=UP * 0.15), Create(box))
        self.wait(1.2)

        table = VGroup(
            VGroup(Text("ระบบ", font_size=19, color=WHITE),
                   Text("k", font_size=19, color=WHITE)).arrange(RIGHT, buff=1.2),
            VGroup(Text("Full-depth", font_size=18, color=PITCH_C),
                   Text("1.0", font_size=18, color=PITCH_C)).arrange(RIGHT, buff=1.0),
            VGroup(Text("Stub", font_size=18, color=GEAR3),
                   Text("0.8", font_size=18, color=GEAR3)).arrange(RIGHT, buff=1.35),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        table.next_to(formula, DOWN, buff=0.6)
        self.play(FadeOut(cap))
        for row in table:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.5)
        self.wait(1.4)

        distinguish = VGroup(
            Text("แยกให้ออก:", font_size=19, color=WHITE),
            Text("Interference = ปัญหาตอนใช้งาน (เฟืองขบกันแล้วชน)", font_size=17, color=WARN),
            Text("Undercutting = ผลของ interference ตอนผลิต (มีดกินโคนฟัน)", font_size=17, color=GEAR3),
            Text("ต้นเหตุเดียวกัน: contact เลย base circle -- คนละสถานการณ์", font_size=16, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for row in distinguish:
            fit_width(row, 6.2)
        distinguish.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        distinguish.to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        cap2 = caption_top("Interference vs Undercutting -- คนละขั้นตอนกัน", size=20)
        self.play(FadeIn(cap2))
        for row in distinguish:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(2.4)


# =====================================================================
# G37 -- หน้า 37: ผลของการเพิ่ม Pressure Angle
# =====================================================================
class G37_PressureAngleEffect(SafeScene):
    def construct(self):
        self.add(title("ผลของการเพิ่ม Pressure Angle", size=27))
        self.add(page_ref("หน้า 37"))

        cap = caption_top("phi ใหญ่ขึ้น -> R_b = R cos(phi) เล็กลง -> ฟันโค้งมากขึ้น ตัดฟันน้อยได้", size=18)
        self.play(FadeIn(cap))

        rows_data = [
            ("20 deg, full-depth (k=1)", 20, 1.0, "18 ฟัน"),
            ("25 deg, full-depth (k=1)", 25, 1.0, "12 ฟัน"),
            ("20 deg, stub (k=0.8)", 20, 0.8, "14 ฟัน"),
        ]
        header = VGroup(
            Text("เงื่อนไข", font_size=17, color=WHITE),
            Text("N_min", font_size=17, color=WHITE),
            Text("ใช้จริง", font_size=17, color=WHITE),
        ).arrange(RIGHT, buff=0.8)
        rows = VGroup(header)
        for label, phi_deg, k, used in rows_data:
            nmin = 2 * k / (np.sin(phi_deg * DEGREES) ** 2)
            r = VGroup(
                Text(label, font_size=16, color=GRAYTXT),
                Text(f"{nmin:.2f}", font_size=16, color=OK),
                Text(used, font_size=16, color=WARN),
            ).arrange(RIGHT, buff=0.5)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to(UP * 0.6)
        self.play(FadeOut(cap))
        for r in rows:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.5)
        self.wait(1.6)

        # ---- แผนภาพเทียบ base circle เล็ก/ใหญ่ ---------------------------------
        cap2 = caption_top("phi มาก -> base circle เล็กลง (เทียบที่ R เท่ากัน)", size=20)
        self.play(FadeIn(cap2))
        R_demo = 1.3
        O1c = LEFT * 3.3 + DOWN * 1.7
        O2c = RIGHT * 2.0 + DOWN * 1.7
        c_R1 = Circle(radius=R_demo, color=PITCH_C, stroke_width=2).move_to(O1c)
        c_Rb1 = Circle(radius=R_demo * np.cos(20 * DEGREES), color=BASE_C, stroke_width=3).move_to(O1c)
        c_R2 = Circle(radius=R_demo, color=PITCH_C, stroke_width=2).move_to(O2c)
        c_Rb2 = Circle(radius=R_demo * np.cos(25 * DEGREES), color=BASE_C, stroke_width=3).move_to(O2c)
        l1 = tag("phi=20 deg", O1c + DOWN * (R_demo + 0.25), DOWN, PITCH_C, 15, 0.08)
        l2 = tag("phi=25 deg", O2c + DOWN * (R_demo + 0.25), DOWN, PITCH_C, 15, 0.08)
        self.play(Create(c_R1), Create(c_Rb1), FadeIn(l1))
        self.play(Create(c_R2), Create(c_Rb2), FadeIn(l2))
        self.wait(1.4)

        cost = Text("ราคาที่จ่าย: แรงกดตามแนว line of action เอียงมากขึ้น -> แรงเข้าแบริ่งสูงขึ้น",
                     font_size=17, color=WARN).move_to([0, -3.15, 0])
        fit_width(cost, 12.5)
        self.play(FadeOut(cap2))
        self.play(FadeIn(cost, shift=UP * 0.15))
        self.wait(2.4)


# =====================================================================
# G38 -- หน้า 38-39: ตัวอย่างใหญ่ (หน่วย mm) -- หา Z และ m_p เต็มขั้นตอน
# =====================================================================
class G38_BigExampleMM(SafeScene):
    def construct(self):
        self.add(title("ตัวอย่างใหญ่ (หน่วย mm): หา Z และ m_p", size=24))
        self.add(page_ref("หน้า 38-39"))

        N1, N2, m, phi_deg = 24, 60, 3.0, 20
        phi = phi_deg * DEGREES
        R1, R2 = m * N1 / 2, m * N2 / 2
        a = 1.000 * m
        Rb1, Rb2 = R1 * np.cos(phi), R2 * np.cos(phi)
        Ro1, Ro2 = R1 + a, R2 + a
        C = R1 + R2
        Z = np.sqrt(Ro1 ** 2 - Rb1 ** 2) + np.sqrt(Ro2 ** 2 - Rb2 ** 2) - C * np.sin(phi)
        pb = 2 * np.pi * Rb1 / N1
        mp = Z / pb

        cap = caption_top("โจทย์: pinion module 3, 24 ฟัน ขับเฟือง 60 ฟัน, phi=20 deg, ไม่มี backlash", size=17)
        self.play(FadeIn(cap))

        fr = cr_wide(shift=np.array([-3.4, -0.15, 0.0]))
        # ใช้เฟรมภาพเดียวกับ G19/G25 (เพื่อความต่อเนื่อง) แต่แทนที่ตัวเลขจริงในป้าย/
        # สูตรด้วยชุดตัวเลข mm ของหน้า 38-39 นี้ -- คนละตัวเลขจากตัวอย่างหน้า 25
        # (นิ้ว) แต่เป็นเฟืองคู่เดียวกันในทางฟิสิกส์ (24T/60T, phi=20, full-depth)
        O1, O2 = fr["O1"], fr["O2"]
        base1 = Circle(radius=fr["Rb1"], color=BASE_C, stroke_width=3).move_to(O1)
        base2 = Circle(radius=fr["Rb2"], color=BASE_C, stroke_width=3).move_to(O2)
        self.play(Create(base1), Create(base2))
        self.wait(0.5)

        self.play(FadeOut(cap))
        cap2 = caption_top("ขั้น 1 -- ต่างจากหน้า 25: ที่นี่ให้แค่ N, m, phi ต้องสร้าง R, Rb, a, Ro, C เอง", size=17)
        self.play(FadeIn(cap2))
        self.wait(1.2)

        step_a = Text("ขั้น 2 -- สูตร: R=mN/2, Rb=Rcos(phi), a=1.000m, Ro=R+a, C=R1+R2",
                       font_size=16, color=WHITE)
        fit_width(step_a, 5.2)
        tbl = VGroup(
            Text("Pinion (24T):", font_size=16, color=GEAR2),
            MathTex(rf"R_1={R1:.0f},\ R_{{b1}}={Rb1:.3f},\ R_{{o1}}={Ro1:.0f}\text{{ mm}}",
                    font_size=16, color=GEAR2),
            Text("Gear (60T):", font_size=16, color=GEAR3),
            MathTex(rf"R_2={R2:.0f},\ R_{{b2}}={Rb2:.3f},\ R_{{o2}}={Ro2:.0f}\text{{ mm}}",
                    font_size=16, color=GEAR3),
            MathTex(rf"C=R_1+R_2={C:.0f}\text{{ mm}}", font_size=17, color=WHITE),
        )
        for row in tbl:
            fit_width(row, 5.2)
        col = VGroup(step_a, *tbl).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        col.to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        self.play(FadeOut(cap2))
        for row in col:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(1.4)

        self.play(FadeOut(col))
        cap3 = caption_top("ขั้น 3 -- แทนค่าหา Z", size=20)
        self.play(FadeIn(cap3))
        z_lines = VGroup(
            MathTex(r"Z=\sqrt{39^2-33.829^2}+\sqrt{93^2-84.572^2}-126\sin20^\circ",
                    font_size=16, color=WHITE),
            MathTex(rf"Z=19.406+38.686-43.095=\mathbf{{{Z:.3f}}}\text{{ mm}}",
                    font_size=18, color=OK),
        )
        for row in z_lines:
            fit_width(row, 6.5)
        z_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        z_lines.move_to([0, -2.5, 0])
        self.play(FadeIn(z_lines[0], shift=UP * 0.1))
        self.wait(0.8)
        self.play(FadeIn(z_lines[1], shift=UP * 0.1))
        self.wait(1.4)

        self.play(FadeOut(cap3))
        cap4 = caption_top("ขั้น 3 (ต่อ) -- หา p_b แล้วหา m_p", size=20)
        self.play(FadeIn(cap4))
        mp_lines = VGroup(
            MathTex(rf"p_b=\frac{{2\pi(33.829)}}{{24}}={pb:.4f}\text{{ mm}}", font_size=18, color=WHITE),
            MathTex(rf"m_p=\frac{{{Z:.3f}}}{{{pb:.4f}}}=\mathbf{{{mp:.3f}}}", font_size=21, color=OK),
        )
        for row in mp_lines:
            fit_width(row, 6.0)
        mp_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        mp_lines.next_to(z_lines, DOWN, buff=0.35)
        box = SurroundingRectangle(mp_lines[1], color=OK, buff=0.15)
        self.play(FadeIn(mp_lines[0], shift=UP * 0.1))
        self.wait(0.8)
        self.play(FadeIn(mp_lines[1], shift=UP * 0.1), Create(box))
        self.wait(1.6)

        self.play(FadeOut(cap4))
        cap5 = caption_top("ขั้น 4 -- ตรวจ", size=20)
        self.play(FadeIn(cap5))
        checks = VGroup(
            Text(f"m_p={mp:.3f} > 1.40 -> เดินเรียบ", font_size=17, color=OK),
            Text(f"N1=24 > 17.09 -> ไม่ undercut", font_size=17, color=OK),
            Text("เช็คไขว้กับหน้า 25: เฟืองคู่เดียวกัน (24T/60T, phi=20) แค่คนละหน่วย",
                 font_size=16, color=GRAYTXT),
            Text(f"m_p={mp:.3f} ตรงกับหน้า 25 (1.693) เพราะ m_p ไม่มีหน่วย",
                 font_size=16, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for row in checks:
            fit_width(row, 6.0)
        checks.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        checks.move_to(DOWN * 1.3)
        self.play(FadeOut(cap5))
        for row in checks:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.5)
        self.wait(1.8)

        warn = Text("บนสไลด์จริง p_b/m_p พิมพ์เลขคลาดเคลื่อน (สลับหลัก) -- ค่าที่ถูกคือค่าข้างบนนี้",
                     font_size=16, color=WARN).move_to([0, -3.15, 0])
        fit_width(warn, 12.5)
        self.play(FadeIn(warn, shift=UP * 0.15))
        self.wait(2.4)
