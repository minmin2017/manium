"""Q2 — sliding-collar rod linkage (visual-for-teach package).
Geometry/values locked in Main_note/Claude_Specs/Manim — Q2 Sliding-Collar Rod-Linkage
Geometry Spec.md — do not re-derive numbers here, only reference that file.
"""
from mlib import *
import numpy as np

SCALE2 = 1.55
A_PT = np.array([-5.8, 1.7, 0])
DIRV = np.array([np.sin(PI / 3), -np.cos(PI / 3), 0])          # (0.8660, -0.5)
NRM = np.array([0.5, np.sin(PI / 3), 0])                        # perp to DIRV (rotate +90)
AC_LEN, AB_LEN, CD_LEN = 0.8660, 1.126, 0.5

A_PT_ = A_PT
C_PT = A_PT + SCALE2 * AC_LEN * DIRV
B_PT = A_PT + SCALE2 * AB_LEN * DIRV
D_PT = C_PT + np.array([0, -SCALE2 * CD_LEN, 0])

OMEGA_AB_COL = "#FFB300"
VCAB_COL = "#42A5F5"
VSLIP_COL = "#26C6DA"
VC_COL = "#66BB6A"
OMEGA_DC_COL = "#AB47BC"
TRAP_COL = "#FF5252"

# real m/s values from the spec (Method 1 == Method 2, both verified)
V_CAB = np.array([-1.299, -2.25, 0])          # v of the AB-material-point under the collar
V_CAB_DIR = np.array([-0.5, np.sin(PI / 3), 0])  # unit dir of V_CAB (perp to AB, rotated -90)
V_SLIP_DIR = -DIRV                             # s is negative -> points back toward A
V_C_DIR = np.array([-1, 0, 0])                 # final v_C: horizontal, left
V_C_MAG = 3 * np.sqrt(3)                       # 5.196 m/s
OMEGA_DC_MAG = 6 * np.sqrt(3)                  # 10.39 rad/s
NAIVE_MAG = 2.598                              # ω_AB * AC, the trap number


def fixed_support(center, up=True, size=0.22):
    d = 1 if up else -1
    tri = Polygon(center, center + [-size, d * size * 1.6, 0], center + [size, d * size * 1.6, 0],
                  color=METAL, fill_color=METAL, fill_opacity=0.5, stroke_width=2)
    ground = Line(center + [-size * 1.3, d * size * 1.6, 0], center + [size * 1.3, d * size * 1.6, 0],
                   color=METAL, stroke_width=3)
    pin_dot = Dot(center, radius=0.05, color=WHITE)
    return VGroup(tri, ground, pin_dot)


def build_diagram():
    rod_ab = Line(A_PT, B_PT, color=METAL, stroke_width=6)
    rod_cd = Line(C_PT, D_PT, color=METAL, stroke_width=6)
    a_sup = fixed_support(A_PT, up=True)
    d_sup = fixed_support(D_PT, up=False)
    c_dot = Dot(C_PT, radius=0.06, color=WHITE)
    b_dot = Dot(B_PT, radius=0.05, color=WHITE)

    a_lbl = Text("A", font_size=16, color=WHITE).next_to(A_PT, LEFT, buff=0.15)
    b_lbl = Text("B", font_size=16, color=WHITE).next_to(B_PT, RIGHT, buff=0.12)
    c_lbl = Text("C", font_size=16, color=WHITE).next_to(C_PT, UP, buff=0.12)
    d_lbl = Text("D", font_size=16, color=WHITE).next_to(D_PT, DOWN, buff=0.32)

    vert_dash = DashedLine(A_PT, A_PT + DOWN * 1.3, color=GRAYTXT, stroke_width=2)
    ang_arc = Arc(radius=0.55, start_angle=-90 * DEGREES, angle=60 * DEGREES,
                  arc_center=A_PT, color=GRAYTXT, stroke_width=2)
    ang_lbl = Text("60°", font_size=15, color=GRAYTXT).move_to(
        A_PT + np.array([0.42, -0.62, 0]))

    dim_v = DashedLine(A_PT, [C_PT[0], A_PT[1], 0], color=GRAYTXT, stroke_width=2)
    dim_h = DashedLine([C_PT[0], A_PT[1], 0], C_PT, color=GRAYTXT, stroke_width=2)
    dim_lbl = Text("0.75 m", font_size=14, color=GRAYTXT).next_to(dim_v, UP, buff=0.1)

    cd_lbl = Text("0.5 m", font_size=14, color=GRAYTXT).next_to(rod_cd, RIGHT, buff=0.15)

    omega_arc = Arc(radius=0.42, start_angle=110 * DEGREES, angle=-150 * DEGREES,
                     arc_center=A_PT, color=OMEGA_AB_COL, stroke_width=4)
    omega_arc.add_tip(tip_length=0.14, tip_width=0.11)
    omega_lbl = Text("omega_AB = 3 rad/s", font_size=14, color=OMEGA_AB_COL).move_to(
        A_PT + np.array([-1.55, 0.55, 0]))
    alpha_lbl = Text("alpha_AB = 5 rad/s^2 (ไม่ใช้ข้อนี้)", font_size=13, color=GRAYTXT).move_to(
        A_PT + np.array([-1.55, 0.25, 0]))

    grp = VGroup(rod_ab, rod_cd, a_sup, d_sup, c_dot, b_dot, a_lbl, b_lbl, c_lbl, d_lbl,
                 vert_dash, ang_arc, ang_lbl, dim_v, dim_h, dim_lbl, cd_lbl,
                 omega_arc, omega_lbl, alpha_lbl)
    return grp


class Q2_00_Setup(SafeScene):
    def construct(self):
        ttl = title("โจทย์ 2: ตั้งค่า")
        pref = page_ref("โจทย์ 2 · ตั้งค่า")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(Create(diagram), run_time=1.5)
        self.wait(1.2)

        cap0 = caption_top("แขน AB หมุนรอบหมุด A คงที่ · ปลอกที่ C ต่อกับก้าน DC หมุนรอบหมุด D คงที่")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.8)

        cap1 = caption_top("โจทย์ถาม: ความเร็วจุด C (v_C) และความเร็วเชิงมุมของแขน DC (omega_DC)")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.8)
        self.wait(2.0)

        self.fade_out_all(run_time=0.9)


class Q2_01_MotionClassification(SafeScene):
    def construct(self):
        ttl = title("จำแนกการเคลื่อนที่")
        pref = page_ref("โจทย์ 2 · ขั้น 1")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(FadeIn(diagram), run_time=1.0)

        cap0 = caption_top("AB: หมุนล้วน รอบหมุด A ที่อยู่กับที่")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.6)

        cap1 = caption_top("DC: หมุนล้วน รอบหมุด D ที่อยู่กับที่")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.6)

        cap2 = caption_top("จุด C ไม่ใช่หมุดร่วมธรรมดา — มันคือปลอก (collar) ที่ไถลไปตามแขน AB ได้")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.8)
        self.wait(2.0)

        cap3 = caption_top("เพราะงั้นต้องมองเป็น 2 จุดซ้อนกัน: จุดบน AB ตรงตำแหน่ง C กับตัวปลอกจริงที่ต่อกับ DC")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.9)
        self.wait(2.2)

        self.fade_out_all(run_time=0.9)


class Q2_02_Trap(SafeScene):
    def construct(self):
        ttl = title("กับดัก: ลืมว่า C เลื่อนได้")
        pref = page_ref("โจทย์ 2 · กับดัก")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(FadeIn(diagram), run_time=1.0)

        cap0 = caption_top("ที่มักพลาด: คิดว่า C ติดอยู่กับ AB ตายตัว แล้วใช้ v_C = omega_AB x AC ตรงๆ")
        self.play(FadeIn(cap0), run_time=0.8)
        self.wait(1.8)

        eq_trap = MathTex(r"v_C \overset{?}{=} \omega_{AB}\cdot AC = 3\times0.866 = 2.598\ \text{m/s}",
                           font_size=26, color=TRAP_COL).move_to([1.6, 0.4, 0])
        self.play(FadeIn(eq_trap), run_time=0.8)
        self.wait(1.6)

        cap1 = caption_top("ผิด — เพราะ C ไถลไปตามแขน AB ได้ คำตอบนี้ทิ้งความเร็วส่วนที่ไถลไปเลย")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.9)
        self.wait(1.8)

        eq_real = MathTex(r"v_C^{\text{real}} = 3\sqrt{3} \approx 5.196\ \text{m/s}",
                           font_size=26, color=VC_COL).move_to([1.6, -0.4, 0])
        self.play(FadeIn(eq_real), run_time=0.8)
        self.wait(2.0)

        self.fade_out_all(run_time=0.9)


class Q2_03_Step1(SafeScene):
    def construct(self):
        ttl = title("ขั้น 1: ความเร็วจุดบน AB ที่ตำแหน่ง C")
        pref = page_ref("โจทย์ 2 · ขั้น 3")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(FadeIn(diagram), run_time=1.0)

        cap0 = caption_top("สูตรทั่วไปก่อน: v_(C บน AB) = omega_AB x r_(C/A)")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.6)

        cap1 = caption_top("แทนค่า: omega_AB=3 rad/s, r_(C/A)=AC=0.866 m ⇒ ขนาด = 3x0.866 = 2.598 m/s")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.8)
        self.wait(1.8)

        v_cab = Arrow(C_PT, C_PT + V_CAB_DIR * 1.3, color=VCAB_COL, buff=0, stroke_width=6,
                      max_tip_length_to_length_ratio=0.25)
        v_cab_lbl = Text("v_(C บน AB) = 2.598 m/s", font_size=15, color=VCAB_COL).next_to(
            v_cab, RIGHT, buff=0.15)
        self.play(GrowArrow(v_cab), FadeIn(v_cab_lbl), run_time=0.9)

        cap2 = caption_top("ทิศ: ตั้งฉากกับ AB เสมอ (เพราะเป็นจุดหมุนรอบ A) — นี่คือความเร็ว 'ถ้า C ติดอยู่กับ AB'")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.9)
        self.wait(2.0)

        self.fade_out_all(run_time=0.9)


class Q2_04_Step2(SafeScene):
    def construct(self):
        ttl = title("ขั้น 2: ทิศของ v_C จริง")
        pref = page_ref("โจทย์ 2 · ขั้น 4")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(FadeIn(diagram), run_time=1.0)

        cap0 = caption_top("C เป็นจุดบนแขน DC ด้วย — DC หมุนรอบ D คงที่")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.6)

        cap1 = caption_top("ตอนนี้ DC อยู่แนวดิ่งพอดี ⇒ v_C ต้องตั้งฉากกับ DC เสมอ ⇒ v_C ต้องแนวนอน")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.9)
        self.wait(2.0)

        v_c_dir = Arrow(C_PT, C_PT + V_C_DIR * 1.2, color=VC_COL, buff=0, stroke_width=6,
                         max_tip_length_to_length_ratio=0.25)
        v_c_lbl = Text("v_C: แนวนอนแน่ (ขนาดยังไม่รู้)", font_size=14, color=VC_COL).next_to(
            v_c_dir, UP, buff=0.15)
        self.play(GrowArrow(v_c_dir), FadeIn(v_c_lbl), run_time=0.9)
        self.wait(1.8)

        self.fade_out_all(run_time=0.9)


class Q2_05_Step3(SafeScene):
    def construct(self):
        ttl = title("ขั้น 3: สมการความเร็วไถล")
        pref = page_ref("โจทย์ 2 · ขั้น 5")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(FadeIn(diagram), run_time=1.0)

        eq0 = MathTex(r"\vec{v}_C = \vec{v}_{(C\,on\,AB)} + \vec{v}_{slip}",
                       font_size=28, color=WHITE).move_to([2.1, 1.3, 0])
        self.play(FadeIn(eq0), run_time=0.8)
        self.wait(1.4)

        cap0 = caption_top("v_ไถล ต้องอยู่ตามแนวแขน AB เท่านั้น (เพราะปลอกเลื่อนไปตามแขนนี้)")
        self.play(FadeIn(cap0), run_time=0.8)
        self.wait(1.8)

        v_cab = Arrow(C_PT, C_PT + V_CAB_DIR * 1.3, color=VCAB_COL, buff=0, stroke_width=5,
                      max_tip_length_to_length_ratio=0.25)
        v_slip = Arrow(C_PT + V_CAB_DIR * 1.3, C_PT + V_CAB_DIR * 1.3 + V_SLIP_DIR * 1.7,
                       color=VSLIP_COL, buff=0, stroke_width=5,
                       max_tip_length_to_length_ratio=0.2)
        v_c = Arrow(C_PT, C_PT + V_C_DIR * V_C_MAG * 0.23, color=VC_COL, buff=0, stroke_width=6,
                    max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(v_cab), run_time=0.6)
        self.play(GrowArrow(v_slip), run_time=0.7)
        self.play(GrowArrow(v_c), run_time=0.7)
        self.wait(1.2)

        cap1 = caption_top("แก้ 2 สมการ (แกน x, y) พร้อมกัน: หา v_ไถล และ v_C ได้ทั้งคู่")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.9)
        self.wait(1.8)

        eq1 = MathTex(r"v_C = 3\sqrt{3} \approx 5.196\ \text{m/s (left)}",
                       font_size=24, color=VC_COL).move_to([2.1, -1.6, 0])
        eq2 = MathTex(r"\omega_{DC} = 6\sqrt{3} \approx 10.39\ \text{rad/s (CCW)}",
                       font_size=24, color=OMEGA_DC_COL).move_to([2.1, -2.15, 0])
        self.play(FadeIn(eq1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(eq2), run_time=0.8)
        self.wait(2.2)

        self.fade_out_all(run_time=0.9)


class Q2_06_CrossCheck(SafeScene):
    def construct(self):
        ttl = title("เช็คซ้ำ: โปรเจกต์ตั้งฉากกับ AB")
        pref = page_ref("โจทย์ 2 · เช็คซ้ำ")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        diagram = build_diagram()
        self.play(FadeIn(diagram), run_time=1.0)

        cap0 = caption_top("ทวนด้วยวิธีที่ 2: โปรเจกต์ทุกความเร็วลงบนแกนตั้งฉากกับ AB — v_ไถล จะหายไปเอง")
        self.play(FadeIn(cap0), run_time=0.8)
        self.wait(2.0)

        eq0 = MathTex(
            r"\vec{v}_C\cdot\hat n = \vec{v}_{(C\,\text{บน}\,AB)}\cdot\hat n \;=\; -2.598",
            font_size=24, color=WHITE).move_to([1.9, 0.9, 0])
        self.play(FadeIn(eq0), run_time=0.8)
        self.wait(1.6)

        cap1 = caption_top("เพราะ v_ไถล อยู่ตามแนว AB ⇒ ไม่มีองค์ประกอบตั้งฉากกับ AB เลย (โปรเจกต์แล้วเป็น 0)")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.9)
        self.wait(2.0)

        eq1 = MathTex(r"v_C\ \text{horizontal} \Rightarrow 0.5\,v_{Cx} = -2.598 \Rightarrow v_{Cx}=-5.196",
                       font_size=22, color=VC_COL).move_to([1.9, -0.4, 0])
        self.play(FadeIn(eq1), run_time=0.8)
        self.wait(1.8)

        cap2 = caption_top("ตรงกับวิธีที่ 1 เป๊ะ: v_C = 3√3 m/s ซ้าย, omega_DC = 6√3 rad/s ทวนเข็ม")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.9)
        self.wait(2.2)

        self.fade_out_all(run_time=0.9)


class Q2_07_Recipe(SafeScene):
    def construct(self):
        ttl = title("สรุปวิธี — ใช้กับโจทย์อื่นได้")
        pref = page_ref("โจทย์ 2 · สรุป")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        steps = [
            "1) เช็คก่อนว่าจุดร่วมเป็นหมุดตายตัว หรือเป็นปลอกที่ไถลได้ (ลองสมการดู ถ้าขัดแย้งกัน = ต้องไถล)",
            "2) หา v ของจุดบนแขนหมุน 'เสมือนติดอยู่กับแขนนั้น' จาก v = omega x r ก่อน",
            "3) v_จริง = v_เสมือนติด + v_ไถล (v_ไถล ต้องอยู่ตามแนวที่มันไถลได้เท่านั้น)",
            "4) ใช้เงื่อนไขทิศทางของอีกฝั่ง (เช่น อีกแขนหมุนรอบหมุดคงที่) ปิดสมการให้ครบ",
            "5) เช็คซ้ำด้วยการโปรเจกต์ตั้งฉากกับแนวไถล — v_ไถล จะหายไปเอง เหลือแค่สมการเดียว",
        ]
        group = VGroup(*[Text(s, font_size=17, color=WHITE) for s in steps])
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.8, 0])
        fit_width(group, 12.0)

        for line in group:
            self.play(FadeIn(line), run_time=0.6)
            self.wait(0.9)

        cap = caption_top("ใช้ได้กับกลไกแบบ 'ปลอกไถลบนแขนหมุน' ทุกแบบ ไม่ใช่แค่ตัวเลขชุดนี้")
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(2.0)

        self.fade_out_all(run_time=0.9)
