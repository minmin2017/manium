"""EPS บทที่ 3 (companion) — ส่วนประกอบเครื่องกำเนิดไฟฟ้ากระแสตรง: ใครนิ่ง ใครหมุน?

คู่กับ EP05 (โครงสร้างจริงของเครื่องกำเนิดไฟฟ้า) — EP05 สอนสร้างทีละชิ้น
ตัวนี้ (EP05B) แก้ความเข้าใจผิดเฉพาะจุดที่ Min งง: จำชื่อชิ้นส่วนได้แต่แยกไม่ออก
ว่าอันไหน "นิ่ง" อันไหน "หมุน" (โดยเฉพาะคำว่า "สเตเตอร์" ที่ไม่ใช่ชิ้นเดียว
แต่เป็น "กลุ่ม" ของชิ้นส่วนนิ่งหลายชิ้นรวมกัน — และคอมมิวเตเตอร์ที่ดูเหมือนติด
กับแปรงถ่านแต่จริงๆ หมุนไปกับเพลา ไม่ใช่แปรงถ่าน)

ผิด: "สเตเตอร์" = ชิ้นส่วนชิ้นเดียว, คอมมิวเตเตอร์กับแปรงถ่านหมุนไปด้วยกัน
อ๋อ: สเตเตอร์ = กลุ่มของ (โครง+ขั้วแม่เหล็ก+ขดลวดสนาม+แปรงถ่าน) ที่นิ่งทั้งหมด
     ส่วนอาร์เมเจอร์ทั้งชุด (แกน+ขดลวด+คอมมิวเตเตอร์) หมุนไปด้วยกันบนเพลาเดียว
     แปรงถ่านแค่ "แตะ" ผิวคอมมิวเตเตอร์ที่หมุนผ่าน ไม่ได้หมุนตาม

สี (เฉพาะคลิปนี้ — กลุ่มนิ่ง vs กลุ่มหมุน, ไม่ใช่ปริมาณฟิสิกส์เดิมของซีรีส์):
  STAT_C  เขียวอมฟ้า  กลุ่มนิ่ง (สเตเตอร์): โครง / ขั้วแม่เหล็ก / ขดลวดสนาม / แปรงถ่าน
  ROT_C   ม่วง        กลุ่มหมุน (อาร์เมเจอร์/โรเตอร์): แกน / ขดลวดอาร์เมเจอร์ / คอมมิวเตเตอร์
"""

import numpy as np
from manim import *
from mlib import *

STAT_C = "#26A69A"   # กลุ่มนิ่ง
ROT_C = TORQUE        # กลุ่มหมุน (ม่วง — ใช้สีเดิมของ "แรงบิด/การหมุน" จาก mlib)

STAGE = np.array([0.0, -0.15, 0.0])
R_FRAME = 3.05
R_ARM = 1.25
POLE_LEN = 1.55
POLE_W = 0.85


def make_stator_group():
    frame = Circle(radius=R_FRAME, color=STAT_C, stroke_width=6,
                   fill_opacity=0.05).move_to(STAGE)

    def pole_with_coil(x_sign, letter):
        # แกนตามแนวขั้ว: t=0 ฝั่งโครง (outer) .. t=1 ฝั่งอาร์เมเจอร์ (inner, หน้าขั้ว)
        # คอยล์พันอยู่ครึ่งนอก (t เล็ก) ปล่อยครึ่งในว่างไว้ให้หน้าขั้ว+ป้าย N/S
        # ไม่ให้เส้นคอยล์พาดผ่านป้ายตัวอักษร
        px = STAGE + np.array([x_sign * (R_FRAME - POLE_LEN / 2 - 0.15), 0, 0])
        body = Rectangle(width=POLE_LEN, height=POLE_W, color=STAT_C,
                         fill_color=STAT_C, fill_opacity=0.5, stroke_width=3)
        body.move_to(px)

        outer_edge_x = px[0] + x_sign * POLE_LEN / 2

        def axis_x(t):
            return outer_edge_x - x_sign * POLE_LEN * t

        coil = VGroup(*[
            Line([axis_x(t), px[1] - POLE_W / 2 - 0.14, 0],
                 [axis_x(t), px[1] + POLE_W / 2 + 0.14, 0],
                 color=STAT_C, stroke_width=2.5)
            for t in np.linspace(0.08, 0.46, 6)
        ])
        lab = Text(letter, font_size=24, color=WHITE).move_to([axis_x(0.82), px[1], 0])
        return VGroup(body, coil, lab)

    pole_n = pole_with_coil(-1, "N")
    pole_s = pole_with_coil(1, "S")
    return VGroup(frame, pole_n, pole_s)


def make_brush():
    tip = STAGE + np.array([0, -R_ARM - 0.55, 0])
    body = Rectangle(width=0.28, height=0.45, color=STAT_C,
                     fill_color=STAT_C, fill_opacity=0.85, stroke_width=2)
    body.move_to(tip + np.array([0, -0.15, 0]))
    lead = Line(body.get_bottom(), body.get_bottom() + np.array([0, -0.35, 0]),
               color=STAT_C, stroke_width=3)
    return VGroup(body, lead)


def make_armature_group():
    core = Circle(radius=R_ARM, color=ROT_C, fill_color="#4A2F55",
                  fill_opacity=0.65, stroke_width=4).move_to(STAGE)
    shaft = Dot(STAGE, radius=0.09, color=WHITE)
    slots = VGroup(*[
        Line(STAGE + (R_ARM - 0.22) * np.array([np.cos(a), np.sin(a), 0]),
             STAGE + (R_ARM - 0.02) * np.array([np.cos(a), np.sin(a), 0]),
             color=ROT_C, stroke_width=3)
        for a in np.linspace(0, TAU, 10, endpoint=False)
    ])
    comm = Rectangle(width=0.5, height=0.22, color=ROT_C,
                     fill_color=ROT_C, fill_opacity=0.9, stroke_width=2)
    comm.move_to(STAGE + np.array([0, -R_ARM - 0.11, 0]))
    seg_lines = VGroup(*[
        Line(comm.get_top() + np.array([x, 0, 0]), comm.get_bottom() + np.array([x, 0, 0]),
             color="#1B1B1B", stroke_width=1.5)
        for x in np.linspace(-0.18, 0.18, 5)
    ])
    return VGroup(core, slots, shaft, comm, seg_lines)


class EP05B_MachinePartsIdentity(SafeScene):
    def construct(self):
        ttl = title("เครื่องกำเนิดไฟฟ้ากระแสตรง — ใครนิ่ง ใครหมุน?")
        self.play(Write(ttl))

        # 1) ความงงตั้งต้น — ศัพท์กระจัดกระจาย
        terms = VGroup(
            Text("แปรงถ่าน?", font_size=26, color=GRAYTXT).move_to([-4.3, 1.6, 0]),
            Text("สเตเตอร์?", font_size=26, color=GRAYTXT).move_to([4.3, 1.6, 0]),
            Text("อาร์เมเจอร์?", font_size=26, color=GRAYTXT).move_to([-4.3, -1.9, 0]),
            Text("คอมมิวเตเตอร์?", font_size=26, color=GRAYTXT).move_to([4.3, -1.9, 0]),
        )
        c0 = caption("อันไหนนิ่ง อันไหนหมุน กันแน่?")
        self.play(FadeIn(terms), FadeIn(c0))
        self.wait(1.3)
        self.play(FadeOut(terms), FadeOut(c0))

        # 2) กลุ่มนิ่ง — สเตเตอร์
        stator = make_stator_group()
        brush = make_brush()
        c1 = caption("กลุ่มนิ่ง (สเตเตอร์): โครง + ขั้วแม่เหล็ก + ขดลวดสนาม + แปรงถ่าน",
                     color=STAT_C)
        self.play(Create(stator), FadeIn(c1))
        self.play(FadeIn(brush))
        self.wait(0.8)
        self.play(FadeOut(c1))

        # 3) กลุ่มหมุน — อาร์เมเจอร์
        armature = make_armature_group()
        c2 = caption("กลุ่มหมุน (อาร์เมเจอร์): แกน + ขดลวดอาร์เมเจอร์ + คอมมิวเตเตอร์",
                     color=ROT_C)
        self.play(FadeIn(armature), FadeIn(c2))
        self.wait(0.8)
        self.play(FadeOut(c2))

        # 4) จุดที่งงบ่อยสุด — คอมมิวเตเตอร์หมุน แปรงถ่านนิ่ง
        c3 = caption("คอมมิวเตเตอร์หมุนไปกับเพลา — แปรงถ่านแค่ \"แตะ\" อยู่กับที่",
                     color=WARN)
        self.play(FadeIn(c3))
        self.play(Rotating(armature, angle=4.3 * PI, about_point=STAGE), run_time=3.5,
                  rate_func=smooth)
        self.wait(0.5)
        self.play(FadeOut(c3))

        # 5) สรุปจบ — สองคอลัมน์
        self.play(FadeOut(stator), FadeOut(brush), FadeOut(armature), FadeOut(ttl))

        end_title = title("สรุป: 2 กลุ่ม", color=WHITE)

        # จัดกึ่งกลาง (ไม่ใช่ชิดซ้าย) เพื่อให้ fit_width บีบทั้งกลุ่มได้แบบสมมาตร
        # รับประกันไม่หลุดขอบเฟรม ไม่ต้องเดาความกว้างจริงของฟอนต์
        stat_head = Text("นิ่ง (สเตเตอร์)", font_size=27, color=STAT_C)
        stat_rows = VGroup(
            Text("โครง (Frame)", font_size=21, color=GRAYTXT),
            Text("ขั้วแม่เหล็ก + ขดลวดสนาม", font_size=21, color=GRAYTXT),
            Text("แปรงถ่าน (Brush)", font_size=21, color=GRAYTXT),
        ).arrange(DOWN, buff=0.28)
        stat_col = VGroup(stat_head, stat_rows).arrange(DOWN, buff=0.35)
        fit_width(stat_col, 4.4)
        stat_col.move_to([-3.4, 0.2, 0])

        rot_head = Text("หมุน (อาร์เมเจอร์/โรเตอร์)", font_size=27, color=ROT_C)
        rot_rows = VGroup(
            Text("แกนอาร์เมเจอร์ (Core)", font_size=21, color=GRAYTXT),
            Text("ขดลวดอาร์เมเจอร์ (Winding)", font_size=21, color=GRAYTXT),
            Text("คอมมิวเตเตอร์ (Commutator)", font_size=21, color=GRAYTXT),
        ).arrange(DOWN, buff=0.28)
        rot_col = VGroup(rot_head, rot_rows).arrange(DOWN, buff=0.35)
        fit_width(rot_col, 4.4)
        rot_col.move_to([3.4, 0.2, 0])

        self.play(Write(end_title))
        self.play(FadeIn(stat_col), FadeIn(rot_col))
        self.wait(2.0)
