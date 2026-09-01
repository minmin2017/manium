"""EPS บทที่ 7 — การสูญเสียและประสิทธิภาพของเครื่องกำเนิดไฟฟ้ากระแสตรง

ซีรีส์ EP11-EP14 ต่อจาก EP07-EP10 (บทที่ 6)

  EP11  ผิด: กำลังอินพุทหายไปเป็นก้อนเดียว
        อ๋อ: หายไป 2 จุดคนละลักษณะ — ก่อนถึงอาร์เมเจอร์ (rotational, คงที่)
             กับหลังอาร์เมเจอร์ (copper, ขึ้นกับโหลด) ตามลำดับกำลังไหล

  EP12  ผิด: copper loss คือค่าคงที่ประจำเครื่อง
        อ๋อ: R เปลี่ยนตามอุณหภูมิ (~1%/2.5C) และสายเล็กระบายความร้อนได้ดีกว่า
             (พื้นที่ผิวต่อปริมาตรสูงกว่า) จึงยอมให้ความหนาแน่นกระแสสูงกว่าได้

  EP13  ผิด: eddy current กับ hysteresis loss แก้ด้วยวิธีเดียวกัน
        อ๋อ: eddy แก้ด้วย "รูปทรง" (แบ่งเป็นแผ่นบาง ลดเหลือ 1/4 เมื่อหั่นครึ่ง)
             hysteresis แก้ด้วย "วัสดุ" (เหล็กซิลิกอน)

  EP14  ผิด: โหลดยิ่งน้อย เครื่องยิ่งประหยัด (loss น้อยลงตามสัดส่วน)
        อ๋อ: loss มี 2 กลุ่ม — variable (ลดตามโหลด) กับ fixed (ไม่ลด)
             โหลดลดครึ่ง แต่ fixed loss เท่าเดิม -> ประสิทธิภาพลดลง ไม่ใช่เพิ่ม

สีประจำปริมาณ (Mayer signaling):
  CURRENT เหลือง  copper loss / กระแส (ขึ้นกับโหลด)
  WARN    ส้ม     rotational loss / ปัญหา (คงที่)
  FIELD   ฟ้า     กำลังเอาท์พุท / สนาม
  OK      ฟ้าเขียว ผลลัพธ์ / ประสิทธิภาพ
  EMF     แดง     คำเตือน / จุดที่พลาดบ่อย
"""

import numpy as np
from manim import *
from mlib import *

STAGE = np.array([0.0, 0.15, 0.0])


# ------------------------------------------------------------------ EP11
class EP11_LossOverview(SafeScene):
    def construct(self):
        # ---------- roadmap เปิดเรื่องทั้ง 10 ซีน (ตามแบบ eps_ch6_master.py S1) ----------
        rttl = title("บทที่ 7 — เราจะเดินทางไปทางไหน", size=28)
        self.play(FadeIn(rttl, shift=DOWN * 0.15), run_time=0.8)

        steps = [
            ("1", "การสูญเสีย 2 ชนิด + กำลังไหล", "หน้า 1-3"),
            ("2", "Copper loss: I²R + อุณหภูมิ + cmil/A", "หน้า 2-3"),
            ("3", "Eddy current vs Hysteresis", "หน้า 4-6"),
            ("4", "ประสิทธิภาพ + ตัวอย่างคำนวณเต็มข้อ", "หน้า 7-12"),
            ("5", "Long-shunt vs Short-shunt", "หน้า 13-16"),
        ]
        rows = VGroup()
        for num, name, pg in steps:
            n = Text(num, font_size=22, color=OK)
            t = Text(name, font_size=22, color=GRAYTXT)
            p = Text(pg, font_size=17, color="#607D8B")
            row = VGroup(n, t, p).arrange(RIGHT, buff=0.32)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        fit_width(rows, 9.8)
        rows.move_to([0, -0.3, 0])

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in rows],
                              lag_ratio=0.22), run_time=2.2)
        self.wait(1.3)
        self.play(FadeOut(rows), FadeOut(rttl), run_time=0.6)

        # ---------- เนื้อหาเดิม ----------
        self.add(title("การสูญเสีย 2 ชนิด — คนละลักษณะ คนละตำแหน่ง"))
        self.add(page_ref("หน้า 1 · 7-1 ถึง 7-3"))

        # -- ต้นไม้การสูญเสีย (ซ้าย)
        cu_head = Text("Copper loss", font_size=26, color=CURRENT).move_to([-4.3, 2.35, 0])
        cu_sub = Text("(ขึ้นกับโหลด, ~I^2)", font_size=18, color=GRAYTXT).next_to(cu_head, DOWN, buff=0.12)
        cu_a = Text("- อาร์เมเจอร์  Ia^2 Ra", font_size=19, color=GRAYTXT).next_to(cu_sub, DOWN, buff=0.28).align_to(cu_sub, LEFT)
        cu_f = Text("- สนามแม่เหล็ก  If^2 Rf", font_size=19, color=GRAYTXT).next_to(cu_a, DOWN, buff=0.16).align_to(cu_a, LEFT)

        rot_head = Text("Rotational loss", font_size=26, color=WARN).move_to([-4.3, -0.15, 0])
        rot_sub = Text("(คงที่ ไม่ขึ้นกับโหลด)", font_size=18, color=GRAYTXT).next_to(rot_head, DOWN, buff=0.12)
        rot_c = Text("- Core: eddy + hysteresis", font_size=19, color=GRAYTXT).next_to(rot_sub, DOWN, buff=0.28).align_to(rot_sub, LEFT)
        rot_m = Text("- Mechanical: windage+friction", font_size=19, color=GRAYTXT).next_to(rot_c, DOWN, buff=0.16).align_to(rot_c, LEFT)

        self.play(FadeIn(cu_head), FadeIn(cu_sub))
        self.play(FadeIn(cu_a), FadeIn(cu_f))
        self.wait(0.3)
        self.play(FadeIn(rot_head), FadeIn(rot_sub))
        self.play(FadeIn(rot_c), FadeIn(rot_m))
        self.wait(0.5)

        left_group = VGroup(cu_head, cu_sub, cu_a, cu_f, rot_head, rot_sub, rot_c, rot_m)
        self.play(left_group.animate.scale(0.72).to_edge(LEFT, buff=0.5).shift(UP * 0.3))

        # -- แผนผังกำลังไหล (ขวา) : Pin -> (-Prot) -> E.Ia -> (-Pcu) -> Pout
        cap = caption("กำลังไหลจากซ้ายไปขวา หักออกทีละก้อนตามตำแหน่งจริง")
        self.play(FadeIn(cap))

        def box(txt, color):
            b = RoundedRectangle(width=2.15, height=0.85, corner_radius=0.1,
                                  stroke_color=color, stroke_width=2.5,
                                  fill_color=color, fill_opacity=0.12)
            t = Text(txt, font_size=17, color=WHITE).move_to(b.get_center())
            return VGroup(b, t)

        b_in = box("P_in\n(กำลังกล)", METAL).move_to([0.75, 1.85, 0])
        b_dev = box("E x Ia\n(สร้างในอาร์ม)", FIELD).move_to([3.75, 1.85, 0])
        b_out = box("P_out\n= Vt x IL", OK).move_to([3.75, -1.55, 0])

        arr1 = Arrow(b_in.get_right(), b_dev.get_left(), buff=0.08, color=WARN, stroke_width=4)
        lab1 = Text("- P_rot", font_size=16, color=WARN).next_to(arr1, UP, buff=0.32)

        arr2 = Arrow(b_dev.get_bottom(), b_out.get_top(), buff=0.08, color=CURRENT, stroke_width=4)
        lab2 = Text("- P_cu", font_size=17, color=CURRENT).next_to(arr2, RIGHT, buff=0.08)

        self.play(FadeIn(b_in))
        self.play(GrowArrow(arr1), FadeIn(lab1))
        self.play(FadeIn(b_dev))
        self.play(GrowArrow(arr2), FadeIn(lab2))
        self.play(FadeIn(b_out))
        self.wait(0.6)

        self.play(FadeOut(cap))
        cap2 = caption("เช็คคำตอบทุกข้อ: E x Ia = P_out + P_cu ต้องตรงกันเป๊ะ")
        self.play(FadeIn(cap2))
        self.wait(1.8)

        self.fade_out_all(run_time=0.7)
        card = exam_card(
            "จุดออกสอบ 7-7: rotational loss ประกอบด้วยอะไรบ้าง",
            "(1) การสูญเสียในแกนเหล็ก (iron/core loss)  (2) การสูญเสียทางกล (mechanical loss)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP12
class EP12_CopperLoss(SafeScene):
    def construct(self):
        self.add(title("Copper loss — ทำไมสายเล็กระบายความร้อนดีกว่า"))
        self.add(page_ref("หน้า 2-3 · 7-3"))

        formula = MathTex(r"P_{cu} = I^2 R", font_size=52, color=CURRENT).move_to([-3.4, 1.9, 0])
        self.play(Write(formula))
        cap = caption("R เปลี่ยนตามอุณหภูมิ ~1% ต่อทุก 2.5C ที่ร้อนขึ้น")
        self.play(FadeIn(cap))
        self.wait(0.4)

        # ตัวอย่างตัวเลข: 20C -> 70C
        rows = VGroup(
            Text("dT = 70 - 20 = 50C", font_size=20, color=GRAYTXT),
            Text("%R เพิ่ม = 50 / 2.5 = 20%", font_size=20, color=GRAYTXT),
            Text("Ra(ร้อน) = 1.2 x 0.05 = 0.06", font_size=20, color=GRAYTXT),
            Text("Pa = 100^2 x 0.06 = 600 W", font_size=22, color=CURRENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-3.4, -0.7, 0])

        for r in rows:
            self.play(FadeIn(r))
            self.wait(0.15)
        self.wait(0.5)

        self.play(FadeOut(VGroup(formula, rows)))
        self.play(FadeOut(cap))

        # -- เปรียบเทียบสาย 2 ขนาด: พื้นที่ผิวต่อปริมาตร
        cap2 = caption("สายเล็ก = พื้นที่ผิวต่อปริมาตรสูงกว่า -> ระบายความร้อนดีกว่า")
        self.play(FadeIn(cap2))

        big = Circle(radius=1.05, color=METAL, fill_color=METAL, fill_opacity=0.5).move_to([-2.6, 0.7, 0])
        small = Circle(radius=0.28, color=CURRENT, fill_color=CURRENT, fill_opacity=0.5).move_to([2.6, 0.7, 0])
        big_lab = Text("D = 1 cm\n4/D = 4", font_size=19, color=GRAYTXT).next_to(big, DOWN, buff=0.3)
        small_lab = Text("D = 0.1 cm\n4/D = 40", font_size=19, color=OK).next_to(small, DOWN, buff=0.3)

        self.play(FadeIn(big), FadeIn(small))
        self.play(FadeIn(big_lab), FadeIn(small_lab))
        self.wait(0.5)

        concl = Text("สาย 0.1 cm ระบายความร้อนได้ 10 เท่าของสาย 1 cm", font_size=21, color=OK).move_to([0, -1.9, 0])
        self.play(FadeIn(concl))
        self.wait(1.8)

        self.fade_out_all(run_time=0.7)
        card = exam_card(
            "จุดออกสอบ 7-4: ทำไมเครื่องความเร็วรอบสูงใช้ cmil/A ต่ำกว่า",
            "หมุนเร็ว → ลมพัดผ่านมาก → ระบายความร้อนดีกว่า → ยอมให้ความหนาแน่นกระแสสูงขึ้นได้")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP13
class EP13_EddyHysteresis(SafeScene):
    def construct(self):
        # หัวเรื่องยาวเกินไปชนป้าย page_ref มุมขวาบน (เจอจริงจากเรนเดอร์คลาวด์
        # 2026-08-31 — รูปแบบเดียวกับที่เจอใน EP17 มาก่อน) ตัดให้สั้นลง
        self.add(title("Eddy current vs Hysteresis"))
        self.add(page_ref("หน้า 4-6 · รูปที่ 7-1"))

        pole_n = pole_box("N", -3.2)
        pole_s = pole_box("S", 3.2)
        self.play(FadeIn(pole_n), FadeIn(pole_s))

        # แกนตัน + กระแสไหลวน
        solid = Circle(radius=1.15, color=METAL, fill_color="#546E7A", fill_opacity=0.75).move_to(STAGE)
        loop = Circle(radius=0.55, color=CURRENT, stroke_width=3).move_to(STAGE)
        loop_arrow = Arrow(loop.point_from_proportion(0.24), loop.point_from_proportion(0.26),
                            buff=0, color=CURRENT, stroke_width=3, tip_length=0.18)
        cap = caption("แกนตัน หมุนตัดสนาม -> เกิด eddy current ไหลวนในเนื้อแกน -> ร้อน")
        self.play(FadeIn(solid))
        self.play(Create(loop), FadeIn(loop_arrow))
        self.play(FadeIn(cap))
        self.wait(0.5)

        p_solid = Text("P = 100 W", font_size=24, color=WARN).move_to([0, -1.9, 0])
        self.play(FadeIn(p_solid))
        self.wait(0.5)

        self.play(FadeOut(VGroup(loop, loop_arrow, cap, p_solid)))

        # แบ่งเป็น 2 ส่วน
        half_top = Circle(radius=1.15, color=METAL, fill_color="#546E7A", fill_opacity=0.75)
        half_top.move_to(STAGE).shift(UP * 0.02)
        gap_line = Line(STAGE + LEFT * 1.15, STAGE + RIGHT * 1.15, color=BLACK, stroke_width=6)
        self.play(FadeOut(solid), FadeIn(half_top))
        cap2 = caption("แบ่งเป็น 2 ส่วน: E เหลือครึ่ง, R เพิ่ม 2 เท่า -> P ต่อส่วน = 12.5W")
        self.play(FadeIn(cap2), Create(gap_line))
        p_half = Text("P รวม = 12.5 x 2 = 25 W  (เหลือ 1/4)", font_size=22, color=OK).move_to([0, -1.9, 0])
        self.play(FadeIn(p_half))
        self.wait(0.6)

        self.play(FadeOut(VGroup(half_top, gap_line, cap2, p_half)))

        # แผ่นบางหลายแผ่น (lamination)
        lam = VGroup(*[
            Rectangle(width=2.1, height=0.09, color=METAL, fill_color="#546E7A",
                      fill_opacity=0.8, stroke_width=1).move_to(STAGE + np.array([0, y, 0]))
            for y in np.linspace(-1.05, 1.05, 14)
        ])
        cap3 = caption("แบ่งหลายแผ่นบาง (lamination) -> eddy loss ลดจนตัดทิ้งได้")
        self.play(FadeIn(lam))
        self.play(FadeIn(cap3))
        self.wait(0.6)
        self.play(FadeOut(VGroup(lam, cap3, pole_n, pole_s)))

        # -- Hysteresis ฝั่งขวา (แนวคิดวัสดุ)
        title2 = Text("Hysteresis loss: โมเลกุลแม่เหล็กพลิกทิศ 1 รอบ/รอบหมุน", font_size=22, color=WARN).move_to([0, 1.6, 0])
        dots = VGroup(*[Dot(point=[x, 0.2, 0], radius=0.09, color=CURRENT) for x in np.linspace(-2.4, 2.4, 7)])
        arrows_up = VGroup(*[Arrow(d.get_center(), d.get_center() + UP * 0.4, buff=0, color=FIELD, stroke_width=3) for d in dots])
        self.play(FadeIn(title2))
        self.play(FadeIn(dots), FadeIn(arrows_up))
        self.wait(0.3)
        arrows_down = VGroup(*[Arrow(d.get_center(), d.get_center() + DOWN * 0.4, buff=0, color=EMF, stroke_width=3) for d in dots])
        self.play(Transform(arrows_up, arrows_down))
        cap4 = caption("พลิกทิศ -> ความฝืดในเนื้อเหล็ก -> ร้อน  (แก้ด้วยเหล็กซิลิกอน)")
        self.play(FadeIn(cap4))
        self.wait(0.5)

        table = VGroup(
            Text("Eddy: แก้ด้วย 'รูปทรง' (แผ่นบาง)", font_size=20, color=OK),
            Text("Hysteresis: แก้ด้วย 'วัสดุ' (silicon steel)", font_size=20, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.5, 0])
        self.play(FadeOut(VGroup(title2, dots, arrows_up, cap4)))
        self.play(FadeIn(table))
        self.wait(1.8)

        self.fade_out_all(run_time=0.7)
        card = exam_card(
            "จุดออกสอบ 7-8: การสูญเสียในแกนเหล็กมีกี่ชนิด",
            "2 ชนิด — eddy current loss (แก้ด้วยรูปทรง) และ hysteresis loss (แก้ด้วยวัสดุ)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


def exam_card(q, a, y=0.0):
    """การ์ด 'จุดออกสอบ' — คำถามจริงจากท้ายบท + คำตอบย่อ (ตามแบบ eps_ch6_master.py)"""
    head = Text("จุดออกสอบ", font_size=20, color="#FFD54F")
    qq = Text(q, font_size=22, color=WHITE)
    fit_width(qq, 11.5)
    aa = Text(a, font_size=20, color=OK)
    fit_width(aa, 11.5)
    card = VGroup(head, qq, aa).arrange(DOWN, buff=0.30)
    card.move_to([0, y, 0])
    return card


def pole_box(sign, x):
    body = RoundedRectangle(width=1.3, height=2.6, corner_radius=0.1,
                             fill_color=METAL, fill_opacity=0.55,
                             stroke_color=METAL, stroke_width=2)
    body.move_to(STAGE + np.array([x, 0, 0]))
    lab = Text(sign, font_size=34, color=WHITE).move_to(body.get_center())
    return VGroup(body, lab)


# ------------------------------------------------------------------ EP14
class EP14_Efficiency(SafeScene):
    def construct(self):
        # เหตุผลเดียวกับ EP13 — ตัดหัวเรื่องให้สั้นลงไม่ให้ชนป้าย page_ref
        self.add(title("ประสิทธิภาพสูงสุด — variable = fixed loss", size=26))
        self.add(page_ref("หน้า 7, 11 · 7-5 · ตัวอย่างที่ 7-4"))

        formula = MathTex(r"\eta = \frac{P_{out}}{P_{out}+P_{loss}}", font_size=46, color=OK).move_to([0, 2.0, 0])
        self.play(Write(formula))
        self.wait(0.4)
        self.play(formula.animate.scale(0.6).to_corner(UR, buff=0.4))

        # แผนภูมิแท่ง เปรียบเทียบโหลดเต็ม vs ครึ่งโหลด
        cap = caption("โหลดเต็ม vs ครึ่งโหลด: Pa (variable) ลดฮวบ แต่ Pf+Prot (fixed) เท่าเดิม")
        self.play(FadeIn(cap))

        axes_y = -1.6
        full_x, half_x = -2.6, 1.6
        scale = 0.0022

        def stacked_bar(x, pa, fixed, label):
            fixed_h = fixed * scale
            pa_h = pa * scale
            fixed_bar = Rectangle(width=1.3, height=fixed_h, color=WARN,
                                   fill_color=WARN, fill_opacity=0.75, stroke_width=1)
            fixed_bar.move_to([x, axes_y + fixed_h / 2, 0])
            pa_bar = Rectangle(width=1.3, height=pa_h, color=CURRENT,
                                fill_color=CURRENT, fill_opacity=0.85, stroke_width=1)
            pa_bar.move_to([x, axes_y + fixed_h + pa_h / 2, 0])
            lab = Text(label, font_size=18, color=GRAYTXT).next_to(fixed_bar, DOWN, buff=0.15)
            return VGroup(fixed_bar, pa_bar, lab)

        base_line = Line([-4.2, axes_y, 0], [4.2, axes_y, 0], color=GRAYTXT, stroke_width=2)
        self.play(Create(base_line))

        bar_full = stacked_bar(full_x, 530.45, 1260, "โหลดเต็ม (12kW)")
        bar_half = stacked_bar(half_x, 140.45, 1260, "ครึ่งโหลด (6kW)")
        self.play(FadeIn(bar_full))
        self.play(FadeIn(bar_half))

        legend = VGroup(
            VGroup(Square(0.18, fill_color=CURRENT, fill_opacity=0.85, stroke_width=0), Text("Pa (variable)", font_size=16, color=GRAYTXT)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.18, fill_color=WARN, fill_opacity=0.75, stroke_width=0), Text("Pf+Prot (fixed)", font_size=16, color=GRAYTXT)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.6).shift(DOWN * 0.3)
        self.play(FadeIn(legend))
        self.wait(0.5)

        eta_full = Text("eta = 87.02%", font_size=24, color=OK).next_to(bar_full, UP, buff=0.25)
        eta_half = Text("eta = 81.08%", font_size=24, color=WARN).next_to(bar_half, UP, buff=0.25)
        self.play(FadeIn(eta_full))
        self.play(FadeIn(eta_half))
        self.wait(0.6)

        self.play(FadeOut(cap))
        cap2 = caption("โหลดลด แต่ fixed loss ไม่ลด -> สัดส่วน loss ต่อเอาต์พุตสูงขึ้น -> eta ลดลง")
        self.play(FadeIn(cap2))
        self.wait(1.8)

        self.fade_out_all(run_time=0.7)
        card = exam_card(
            "หลักการที่ต้องจำ",
            "ประสิทธิภาพสูงสุดเกิดเมื่อ variable loss = fixed loss — ไม่ใช่ที่โหลดเต็มที่เสมอไป")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP15
class EP15_Example72_FullWalkthrough(SafeScene):
    """หน้า 9 · ตัวอย่างที่ 7-2 — ข้อครบวงจรที่สุด: ลำดับ IL->If->Ia->Pa,Pf->E->EIa->eta
    ใช้ได้กับทุกข้อของเครื่องแบบขนาน (ต่อยอดจากบทที่ 5)"""

    def construct(self):
        ttl = title("ตัวอย่างที่ 7-2 — ข้อครบวงจรที่สุดของเครื่องแบบขนาน", size=25)
        ref = page_ref("หน้า 9 · ตัวอย่างที่ 7-2")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top(
            "เครื่องกำเนิดแบบขนาน พิกัด 125V, 25kW — Ra=0.08 Ω, Rf=25 Ω")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.9)

        # ---------- ลำดับกระแส: IL -> If -> Ia ----------
        cap1 = caption_top("ขั้น 1 — หาลำดับกระแสก่อน: IL -> If -> Ia", color=CURRENT)
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.5)

        rows = VGroup(
            MathTex(r"I_L=\frac{P_{out}}{V_t}=\frac{25{,}000}{125}=200\ \text{A}",
                   font_size=30, color=WHITE),
            MathTex(r"I_f=\frac{V_t}{R_f}=\frac{125}{25}=5\ \text{A}",
                   font_size=30, color=WHITE),
            MathTex(r"I_a=I_L+I_f=200+5=205\ \text{A}", font_size=30, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.6, 0])
        fit_width(rows, 10.5)

        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.1)

        self.play(rows.animate.scale(0.55).to_edge(LEFT, buff=0.7).shift(UP * 0.5),
                  run_time=0.9)

        # ---------- copper loss ----------
        cap2 = caption_top("ขั้น 2 — copper loss ที่อาร์เมเจอร์ กับ ชันท์ฟิลด์", color=CURRENT)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.5)

        rows2 = VGroup(
            MathTex(r"P_a=I_a^2R_a=205^2(0.08)=3{,}362\ \text{W}",
                   font_size=28, color=CURRENT),
            MathTex(r"P_f=V_tI_f=125\times5=625\ \text{W}",
                   font_size=28, color=CURRENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([2.3, 0.6, 0])
        fit_width(rows2, 6.6)
        for r in rows2:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.1)

        self.play(rows2.animate.scale(0.6).next_to(rows, DOWN, buff=0.45,
                                                    aligned_edge=LEFT), run_time=0.9)

        # ---------- E, EIa ----------
        cap3 = caption_top("ขั้น 3 — แรงเคลื่อน E แล้วหากำลังที่สร้างในอาร์เมเจอร์", color=OK)
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.5)

        rows3 = VGroup(
            MathTex(r"E=V_t+I_aR_a=125+205(0.08)=141.4\ \text{V}",
                   font_size=28, color=OK),
            MathTex(r"P_{dev}=E\,I_a=141.4\times205=28{,}987\ \text{W}",
                   font_size=28, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([1.5, -1.3, 0])
        fit_width(rows3, 8.0)
        for r in rows3:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.1)

        check = Text("เช็ค: 28,987 = Pout+Pcu = 25,000+3,362+625 ✓",
                     font_size=20, color=GRAYTXT).next_to(rows3, DOWN, buff=0.35)
        fit_width(check, 9.5)
        self.play(FadeIn(check), run_time=0.7)
        self.wait(1.2)

        self.play(*[FadeOut(m) for m in (rows, rows2, rows3, check, cap3)], run_time=0.7)

        # ---------- efficiency ----------
        cap4 = caption_top("ขั้น 4 — ประสิทธิภาพที่พิกัดโหลด (rotational loss = 750 W)", color=OK)
        self.play(FadeIn(cap4), run_time=0.6)

        eta_calc = VGroup(
            MathTex(r"P_{loss}=3{,}362+625+750=4{,}737\ \text{W}", font_size=30, color=WHITE),
            MathTex(r"\eta=\frac{25{,}000}{25{,}000+4{,}737}\times100=\mathbf{84.07\%}",
                   font_size=36, color=OK),
        ).arrange(DOWN, buff=0.40).move_to([0, 0.3, 0])
        fit_width(eta_calc, 11.0)
        self.play(FadeIn(eta_calc[0]), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(eta_calc[1], scale=1.2), run_time=0.9)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in (eta_calc, cap4, ttl, ref)], run_time=0.7)
        card = exam_card(
            "แม่แบบของทั้งบท: ลำดับคำนวณคืออะไร",
            "IL -> If -> Ia -> Pa,Pf -> E -> E·Ia -> η  (ใช้ได้ทุกข้อแบบขนาน)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP16
class EP16_NoLoadComparison_Example75(SafeScene):
    """หน้า 12 · ตัวอย่างที่ 7-5 — กำลังที่ต้องใช้หมุนเครื่องขณะไม่มีโหลด
    เปรียบเทียบ 3 กรณี: กระตุ้นตามปกติ / กระตุ้นแยกต่างหาก / ไม่มีการกระตุ้น"""

    def construct(self):
        ttl = title("ไม่มีโหลด — ใครเป็นคนจ่ายกำลังให้ฟิลด์?", size=26)
        ref = page_ref("หน้า 12 · ตัวอย่างที่ 7-5")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top(
            "mechanical loss=500W, core loss=300W, If=3.6A, Ra=0.19 Ω — ไม่มีโหลด")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)

        cap1 = caption_top(
            "กระตุ้นตามปกติ: ฟิลด์กินไฟจากตัวเครื่องเอง — อาร์เมเจอร์ต้องแบก If ด้วย",
            color=CURRENT)
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.6)

        base_y = -1.7
        scale = 0.0016

        def bar(x, val, color, label, sub):
            h = val * scale
            r = Rectangle(width=1.7, height=h, color=color, fill_color=color,
                          fill_opacity=0.8, stroke_width=1)
            r.move_to([x, base_y + h / 2, 0])
            lab = Text(label, font_size=17, color=WHITE).next_to(r, UP, buff=0.15)
            subl = Text(sub, font_size=15, color=GRAYTXT).next_to(r, DOWN, buff=0.15)
            fit_width(subl, 2.0)
            return VGroup(r, lab, subl)

        base_line = Line([-4.6, base_y, 0], [4.6, base_y, 0], color=GRAYTXT, stroke_width=2)
        self.play(Create(base_line), run_time=0.5)

        b1 = bar(-3.0, 1252.46, CURRENT, "1,252.46 W", "กระตุ้นตามปกติ")
        self.play(FadeIn(b1, shift=UP * 0.2), run_time=0.9)
        self.wait(1.0)

        cap2 = caption_top(
            "กระตุ้นแยกต่างหาก: ฟิลด์กินไฟจากแหล่งภายนอก — Ia=0 เลย", color=OK)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.5)
        b2 = bar(0.0, 800, OK, "800 W", "กระตุ้นแยกต่างหาก")
        self.play(FadeIn(b2, shift=UP * 0.2), run_time=0.9)
        self.wait(1.0)

        cap3 = caption_top(
            "ไม่มีการกระตุ้น: ไม่มีฟลักซ์เลย -> ไม่มี core loss (eddy+hysteresis ต้องมีฟลักซ์)",
            color=WARN)
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.5)
        b3 = bar(3.0, 500, WARN, "500 W", "ไม่มีการกระตุ้น")
        self.play(FadeIn(b3, shift=UP * 0.2), run_time=0.9)
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in (b1, b2, b3, base_line, cap3)], run_time=0.6)

        cap3b = caption_top("แต่ละกรณีมี loss ครบทุกชนิดไหม — เช็คทีละก้อน", color=GRAYTXT)
        self.play(FadeIn(cap3b), run_time=0.6)

        head_row = ["กรณี", "mech", "core", "armature I²R", "field"]
        data_rows = [
            ["(ก) กระตุ้นตามปกติ", "✓", "✓", "✓ (Ia=If)", "✓"],
            ["(ข) กระตุ้นแยกต่างหาก", "✓", "✓", "✗ (Ia=0)", "✗ (จากนอก)"],
            ["(ค) ไม่มีการกระตุ้น", "✓", "✗ (ไม่มีฟลักซ์)", "✗", "✗"],
        ]
        colors = [CURRENT, OK, WARN]
        tbl = VGroup()
        for cell in head_row:
            tbl.add(Text(cell, font_size=15, color=GRAYTXT))
        for row, c in zip(data_rows, colors):
            for j, cell in enumerate(row):
                tcolor = c if j == 0 else WHITE
                t = Text(cell, font_size=14, color=tcolor)
                fit_width(t, 2.5)
                tbl.add(t)
        grid = tbl.arrange_in_grid(rows=4, cols=5, buff=(0.35, 0.18))
        fit_width(grid, 12.0)
        grid.move_to([0, -0.4, 0])
        self.play(FadeIn(grid), run_time=1.0)
        self.wait(1.8)

        self.play(FadeOut(grid), FadeOut(cap3b), run_time=0.5)

        cap4 = caption_top(
            "(ก)−(ข)=452.46≈field+armature loss · (ข)−(ค)=300=core loss พอดี", color=GRAYTXT)
        self.play(FadeIn(cap4), run_time=0.6)
        self.wait(1.6)

        self.play(*[FadeOut(m) for m in (cap4, ttl, ref)], run_time=0.7)
        card = exam_card(
            "ทำไมไม่มีการกระตุ้นแล้ว core loss หายไป",
            "eddy + hysteresis ต้องอาศัยฟลักซ์แม่เหล็กทั้งคู่ — ไม่กระตุ้น = ไม่มีฟลักซ์")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP17
class EP17_LongVsShortShunt(SafeScene):
    """หน้า 13-16 · ตัวอย่างที่ 7-6 (long-shunt) vs 7-7 (short-shunt)
    ลำดับคำนวณคนละแบบ — จุดที่ผิดกันบ่อยที่สุดของบท"""

    def construct(self):
        # หัวเรื่องยาวเกินไปตอน size=25 ชนกับป้าย page_ref มุมขวาบน (เจอจริงจาก
        # เรนเดอร์คลาวด์ 2026-08-31, layout linter จับได้ 21% overlap) ตัดให้สั้นลง
        ttl = title("Long-shunt vs Short-shunt", size=25)
        ref = page_ref("หน้า 13-16 · ตัวอย่างที่ 7-6, 7-7")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("ชันท์ฟิลด์ต่อจุดไหน ตัดสินว่าต้องหาอะไรก่อน")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.9)

        # ---------- ซ้าย: long-shunt ----------
        lx = -3.5
        l_head = Text("Long-shunt", font_size=24, color=CURRENT).move_to([lx, 1.85, 0])
        l_sub = Text("ชันท์ฟิลด์คร่อมขั้วจ่ายไฟตรงๆ", font_size=16, color=GRAYTXT)
        l_sub.next_to(l_head, DOWN, buff=0.15)
        l_diag = Text("Rf ---(คร่อม Vt)\nRa+Rs อนุกรมกัน\nIs = Ia", font_size=17,
                     color=WHITE, line_spacing=1.0).next_to(l_sub, DOWN, buff=0.30)
        # หมายเหตุ: ห้ามใส่ข้อความไทยใน \text{} ของ MathTex (ทำให้ latex build พัง —
        # ดู memory feedback-manim-verify-frames.md) แยกเป็น MathTex + Text คนละก้อน
        l_form_eq = MathTex(r"I_f=\frac{V_t}{R_f}", font_size=24, color=CURRENT)
        l_form_note = Text("(ตรงๆ)", font_size=18, color=CURRENT)
        l_form = VGroup(l_form_eq, l_form_note).arrange(RIGHT, buff=0.18)
        l_form.next_to(l_diag, DOWN, buff=0.30)

        # ---------- ขวา: short-shunt ----------
        rx = 3.5
        r_head = Text("Short-shunt", font_size=24, color=WARN).move_to([rx, 1.85, 0])
        r_sub = Text("ชันท์ฟิลด์คร่อมอาร์เมเจอร์เท่านั้น", font_size=16, color=GRAYTXT)
        r_sub.next_to(r_head, DOWN, buff=0.15)
        r_diag = Text("Rf ---(คร่อมอาร์เมเจอร์)\nRs อยู่ในสายจ่ายไฟ\nIs = IL", font_size=17,
                     color=WHITE, line_spacing=1.0).next_to(r_sub, DOWN, buff=0.30)
        r_form_eq = MathTex(r"I_f=\frac{V_t+I_LR_s}{R_f}", font_size=22, color=WARN)
        r_form_note = Text("(ต้องหา IL ก่อน)", font_size=17, color=WARN)
        r_form = VGroup(r_form_eq, r_form_note).arrange(DOWN, buff=0.12)
        fit_width(r_form, 3.6)
        r_form.next_to(r_diag, DOWN, buff=0.30)

        divider = Line([0, 2.3, 0], [0, -0.6, 0], color=GRAYTXT, stroke_width=1.5)

        self.play(FadeIn(l_head), FadeIn(l_sub), FadeIn(r_head), FadeIn(r_sub),
                  Create(divider), run_time=1.0)
        self.play(FadeIn(l_diag), FadeIn(r_diag), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(l_form), FadeIn(r_form), run_time=0.9)
        self.wait(1.4)

        self.play(FadeOut(cap0), run_time=0.3)
        cap1 = caption_top(
            "long: If หาได้ทันที -> Ia -> จบ | short: ต้องหา IL ก่อน ค่อยหา If",
            color=EMF)
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.6)

        self.play(*[FadeOut(m) for m in (l_head, l_sub, l_diag, l_form, r_head, r_sub,
                                         r_diag, r_form, divider, cap1)], run_time=0.7)

        # ---------- ผลลัพธ์ตัวเลขจริง ----------
        cap2 = caption_top("ผลลัพธ์จริง — 7-6 (10kW) กับ 7-7 (25kW)")
        self.play(FadeIn(cap2), run_time=0.6)

        tbl = VGroup(
            Text("", font_size=20),
            Text("Long-shunt (7-6)", font_size=20, color=CURRENT),
            Text("Short-shunt (7-7)", font_size=20, color=WARN),
            Text("Ia", font_size=19, color=GRAYTXT),
            Text("45.78 A", font_size=19, color=WHITE),
            Text("105.87 A", font_size=19, color=WHITE),
            Text("E", font_size=19, color=GRAYTXT),
            Text("241.44 V", font_size=19, color=WHITE),
            Text("266.21 V", font_size=19, color=WHITE),
            Text("η", font_size=19, color=GRAYTXT),
            Text("82.00 %", font_size=19, color=OK),
            Text("82.61 %", font_size=19, color=OK),
        )
        grid = VGroup(*tbl).arrange_in_grid(rows=4, cols=3, buff=(0.9, 0.35))
        fit_width(grid, 11.5)
        grid.move_to([0, 0.2, 0])
        self.play(FadeIn(grid), run_time=1.1)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in (grid, cap2, ttl, ref)], run_time=0.7)
        card = exam_card(
            "เอกลักษณ์ที่ต้องจำ",
            "Long-shunt: Is = Ia   |   Short-shunt: Is = IL")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP18
class EP18_ChapterSummary(SafeScene):
    """สรุปทั้งบท 7 — flashcards หลัก"""

    def construct(self):
        ttl = title("สรุปบทที่ 7 — การสูญเสียและประสิทธิภาพ", size=27)
        self.add(page_ref("หน้า 17 · คำถามท้ายบท"))
        self.play(FadeIn(ttl), run_time=0.8)
        self.wait(0.6)

        pts = [
            ("การสูญเสีย 2 ชนิด", "Copper loss (ขึ้นกับโหลด) + Rotational loss (คงที่)", CURRENT),
            ("ความต้านทาน", "เพิ่ม 1% ทุกๆ 2.5°C ที่ร้อนขึ้น — ห้ามใช้ค่าเย็นตรงๆ ถ้าโจทย์ให้อุณหภูมิ", METAL),
            ("Eddy current loss", "∝ (ความหนาแผ่น)² × (ความเร็ว)² × (ฟลักซ์)² — แก้ด้วยแผ่นบาง", "#546E7A"),
            ("ตรวจคำตอบทุกข้อ", "E·Ia = Pout + Pcu ต้องตรงกันเป๊ะ", OK),
            ("ประสิทธิภาพสูงสุด", "เกิดเมื่อ variable loss = fixed loss", WARN),
            ("Long vs Short-shunt", "Is=Ia (long) ต่างจาก Is=IL (short)", EMF),
        ]
        rows = VGroup()
        for head, body, c in pts:
            h = Text(head, font_size=22, color=c)
            b = Text(body, font_size=17, color=GRAYTXT)
            fit_width(b, 10.5)
            row = VGroup(h, b).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit_width(rows, 11.0)
        rows.move_to([0, -0.15, 0])

        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.25), run_time=0.55)
            self.wait(0.35)
        self.wait(1.4)

        self.play(FadeOut(rows), run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 7-10: ประสิทธิภาพคืออะไร",
            "อัตราส่วนกำลังเอาท์พุทต่อกำลังอินพุท  η = Pout/Pin = Pout/(Pout+Ploss)", y=-0.1)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)

        self.play(FadeOut(card), FadeOut(ttl), run_time=0.7)
        closer = Text("ครบทั้งบทที่ 7 แล้ว — ไปต่อบทถัดไปได้เลย", font_size=26, color=OK)
        self.play(FadeIn(closer, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP19
class EP19_Example76_LongShuntWalkthrough(SafeScene):
    """หน้า 13-14 · ตัวอย่างที่ 7-6 — เดินเลขเต็มข้อของ long-shunt compound
    (EP17 เทียบแค่แนวคิด/สูตร ตัวนี้ทำตัวเลขจริงให้ดูครบ)"""

    def construct(self):
        ttl = title("ตัวอย่างที่ 7-6 (Long-shunt)", size=27)
        ref = page_ref("หน้า 13-14 · รูปที่ 7-7")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top(
            "compound 10kW, 230V — Ra=0.15Ω, Rs=0.1Ω (เซรี่), Rf=100Ω (ชันท์)")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)

        cap1 = caption_top("ขั้น 1 — long-shunt: ชันท์คร่อม Vt ตรงๆ หา If ได้ทันที",
                           color=CURRENT)
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.5)

        rows = VGroup(
            MathTex(r"I_L=\frac{10{,}000}{230}=43.478\ \text{A}", font_size=28, color=WHITE),
            MathTex(r"I_f=\frac{230}{100}=2.3\ \text{A}", font_size=28, color=WHITE),
            MathTex(r"I_a=I_s=I_L+I_f=45.78\ \text{A}", font_size=28, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.6, 0])
        fit_width(rows, 10.5)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.0)
        self.play(rows.animate.scale(0.55).to_edge(LEFT, buff=0.7).shift(UP * 0.5),
                  run_time=0.8)

        cap2 = caption_top("ขั้น 2 — แรงดันตกในวงจรอาร์เมเจอร์ (Ra+Rs อนุกรมกัน) แล้วหา E",
                           color=OK)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.5)

        rows2 = VGroup(
            MathTex(r"V_{drop}=I_a(R_a+R_s)=45.78(0.25)=11.44\ \text{V}",
                   font_size=26, color=OK),
            MathTex(r"E=V_t+V_{drop}=230+11.44=241.44\ \text{V}", font_size=28, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([1.6, 0.6, 0])
        fit_width(rows2, 8.5)
        for r in rows2:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.1)
        self.play(rows2.animate.scale(0.6).next_to(rows, DOWN, buff=0.40,
                                                    aligned_edge=LEFT), run_time=0.8)

        cap3 = caption_top("ขั้น 3 — copper loss ทั้ง 3 ก้อน (Ra, Rs, Rf)", color=CURRENT)
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.5)

        rows3 = VGroup(
            MathTex(r"P_a=45.78^2(0.15)=314.3\ \text{W}", font_size=26, color=CURRENT),
            MathTex(r"P_s=45.78^2(0.1)=209.6\ \text{W}", font_size=26, color=CURRENT),
            MathTex(r"P_f=2.3^2(100)=529.0\ \text{W}", font_size=26, color=CURRENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([1.5, -1.4, 0])
        fit_width(rows3, 8.0)
        for r in rows3:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.2)

        self.fade_out_all(run_time=0.7)

        cap4 = caption_top("ขั้น 4 — ประสิทธิภาพ (core=400W, mechanical=742W)", color=OK)
        self.play(FadeIn(cap4), run_time=0.6)

        eta_calc = VGroup(
            MathTex(r"P_{cu}=314.3+209.6+529.0=1{,}052.9\ \text{W}", font_size=26,
                   color=WHITE),
            MathTex(r"P_{loss}=1{,}052.9+400+742=2{,}194.9\ \text{W}", font_size=26,
                   color=WHITE),
            MathTex(r"\eta=\frac{10{,}000}{12{,}194.9}\times100=\mathbf{82.00\%}",
                   font_size=34, color=OK),
        ).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
        fit_width(eta_calc, 11.0)
        self.play(FadeIn(eta_calc[0]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(eta_calc[1]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(eta_calc[2], scale=1.2), run_time=0.9)
        self.wait(1.5)

        self.play(FadeOut(eta_calc), FadeOut(cap4), FadeOut(ttl), FadeOut(ref),
                  run_time=0.7)
        card = exam_card(
            "เอกลักษณ์ของ long-shunt",
            "Is = Ia (เซรี่ฟิลด์แบกกระแสเดียวกับอาร์เมเจอร์) — If หาได้ทันทีจาก Vt/Rf")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP20
class EP20_Example77_ShortShuntWalkthrough(SafeScene):
    """หน้า 15-16 · ตัวอย่างที่ 7-7 — เดินเลขเต็มข้อของ short-shunt compound
    จุดต่างจาก long-shunt: ต้องหา IL ก่อนถึงจะหา If ได้"""

    def construct(self):
        ttl = title("ตัวอย่างที่ 7-7 (Short-shunt)", size=27)
        ref = page_ref("หน้า 15-16 · รูปที่ 7-8")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top(
            "compound 25kW, 240V — Ra=0.1Ω, Rs=0.15Ω (เซรี่), Rf=150Ω (ชันท์)")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)

        cap1 = caption_top(
            "ขั้น 1 — short-shunt: เซรี่อยู่ในสายจ่ายไฟ ⇒ ต้องหา IL ก่อนเสมอ",
            color=WARN)
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.5)

        rows = VGroup(
            MathTex(r"I_L=I_s=\frac{25{,}000}{240}=104.167\ \text{A}",
                   font_size=27, color=WARN),
            MathTex(r"V_{sh}=V_t+I_LR_s=240+104.167(0.15)=255.625\ \text{V}",
                   font_size=25, color=WHITE),
            MathTex(r"I_f=\frac{255.625}{150}=1.704\ \text{A}", font_size=27, color=WHITE),
            MathTex(r"I_a=I_L+I_f=104.167+1.704=105.87\ \text{A}",
                   font_size=27, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, 0.5, 0])
        fit_width(rows, 11.0)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.2)
        self.play(rows.animate.scale(0.5).to_edge(LEFT, buff=0.6).shift(UP * 0.6),
                  run_time=0.8)

        cap2 = caption_top("ขั้น 2 — แรงเคลื่อน E และ copper loss ทั้ง 3 ก้อน", color=OK)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.5)

        rows2 = VGroup(
            MathTex(r"E=V_{sh}+I_aR_a=255.625+10.59=266.21\ \text{V}",
                   font_size=25, color=OK),
            MathTex(r"P_a=105.87^2(0.1)=1{,}120.9\ \text{W}", font_size=24, color=CURRENT),
            MathTex(r"P_s=104.167^2(0.15)=1{,}627.6\ \text{W}", font_size=24, color=CURRENT),
            MathTex(r"P_f=1.704^2(150)=435.6\ \text{W}", font_size=24, color=CURRENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([1.6, -0.4, 0])
        fit_width(rows2, 8.5)
        for r in rows2:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.3)

        self.fade_out_all(run_time=0.7)

        cap3 = caption_top("ขั้น 3 — ประสิทธิภาพ (core=845W, mechanical=1,235W)", color=OK)
        self.play(FadeIn(cap3), run_time=0.6)

        eta_calc = VGroup(
            MathTex(r"P_{cu}=1{,}120.9+1{,}627.6+435.6=3{,}184.1\ \text{W}",
                   font_size=25, color=WHITE),
            MathTex(r"P_{loss}=3{,}184.1+845+1{,}235=5{,}264.1\ \text{W}",
                   font_size=25, color=WHITE),
            MathTex(r"\eta=\frac{25{,}000}{30{,}264.1}\times100=\mathbf{82.61\%}",
                   font_size=34, color=OK),
        ).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
        fit_width(eta_calc, 11.0)
        self.play(FadeIn(eta_calc[0]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(eta_calc[1]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(eta_calc[2], scale=1.2), run_time=0.9)
        self.wait(1.5)

        self.play(FadeOut(eta_calc), FadeOut(cap3), FadeOut(ttl), FadeOut(ref),
                  run_time=0.7)
        card = exam_card(
            "จุดที่ผิดกันบ่อยที่สุด",
            "short-shunt: If ≠ Vt/Rf ตรงๆ — ต้องบวกแรงดันตกที่เซรี่ฟิลด์ (ILRs) เข้าไปก่อน")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP21
class EP21_Example71_Walkthrough(SafeScene):
    """หน้า 8 · ตัวอย่างที่ 7-1 — ข้อแรกของบท เดินเลขเต็มทุกขั้น (เครื่องเล็กที่สุดในบท)"""

    def construct(self):
        ttl = title("ตัวอย่างที่ 7-1 (ข้อแรกของบท)", size=27)
        ref = page_ref("หน้า 8 · รูปที่ 6-2")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("เครื่องกำเนิดแบบขนาน 120V — Ra=0.4Ω, Rf=60Ω, IL=30A")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)

        cap1 = caption_top(
            "ขั้น 1-2 — เครื่องขนาน: ชันท์ฟิลด์คร่อม Vt ตรงๆ หา If แล้วบวกเข้ากับ IL",
            color=CURRENT)
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.5)

        rows = VGroup(
            MathTex(r"I_f=\frac{V_t}{R_f}=\frac{120}{60}=2\ \text{A}", font_size=30,
                   color=WHITE),
            MathTex(r"I_a=I_L+I_f=30+2=32\ \text{A}", font_size=30, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.7, 0])
        fit_width(rows, 9.0)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.1)
        self.play(rows.animate.scale(0.55).to_edge(LEFT, buff=0.7).shift(UP * 0.6),
                  run_time=0.8)

        cap2 = caption_top("ขั้น 3 — copper loss ที่อาร์เมเจอร์และชันท์ฟิลด์", color=CURRENT)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.5)

        rows2 = VGroup(
            MathTex(r"P_a=32^2(0.4)=409.6\ \text{W}", font_size=28, color=CURRENT),
            MathTex(r"P_f=2^2(60)=240\ \text{W}", font_size=28, color=CURRENT),
            MathTex(r"P_{cu}=409.6+240=649.6\ \text{W}", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([1.6, 0.4, 0])
        fit_width(rows2, 8.0)
        for r in rows2:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.2)

        self.fade_out_all(run_time=0.7)

        cap3 = caption_top("ขั้น 4 — ประสิทธิภาพ (rotational loss = 350W)", color=OK)
        self.play(FadeIn(cap3), run_time=0.6)

        eta_calc = VGroup(
            MathTex(r"P_{out}=V_tI_L=120\times30=3{,}600\ \text{W}", font_size=28,
                   color=WHITE),
            MathTex(r"P_{loss}=649.6+350=999.6\ \text{W}", font_size=28, color=WHITE),
            MathTex(r"\eta=\frac{3{,}600}{3{,}600+999.6}\times100=\mathbf{78.27\%}",
                   font_size=34, color=OK),
        ).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
        fit_width(eta_calc, 11.0)
        self.play(FadeIn(eta_calc[0]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(eta_calc[1]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(eta_calc[2], scale=1.2), run_time=0.9)
        self.wait(1.5)

        self.play(FadeOut(eta_calc), FadeOut(cap3), FadeOut(ttl), FadeOut(ref),
                  run_time=0.7)
        card = exam_card(
            "สังเกต",
            "เครื่องเล็ก (3.6kW) → η ต่ำสุดในบท (78.27%) — ยิ่งเครื่องใหญ่ ยิ่งมีประสิทธิภาพสูง")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ------------------------------------------------------------------ EP18B
def pole_box3(sign, x, color):
    """เสาแม่เหล็ก N/S ในโมเดล 3D — ป้ายชื่อเป็น world_text (ติดกับตัวเสาจริง
    ไม่ใช่ HUD) ต้องเรียก scene.world_text(label) เองหลังสร้าง"""
    body = RoundedRectangle(width=1.1, height=2.0, corner_radius=0.08,
                             fill_color=METAL, fill_opacity=0.55,
                             stroke_color=METAL, stroke_width=2)
    body.move_to(STAGE + np.array([x, 0, 0]))
    label = Text(sign, font_size=30, color=color).move_to(body.get_center())
    return VGroup(body, label), label


def coil_wrap(center, w, h, color):
    """ขดลวดพันรอบชิ้นส่วน — สี่เหลี่ยมเส้นขอบใหญ่กว่าตัวชิ้นส่วนเล็กน้อย
    แทนขดลวดทองแดง (ไม่วาดเป็นวงจริงเพื่อความเร็วเรนเดอร์ — แนวคิดเดียวกับ
    ลูกศรแบนแทนลูกศร 3D ใน [[project-manim-video-pipeline]] §2)"""
    return Rectangle(width=w, height=h, color=color, stroke_width=4).move_to(center)


class EP18B_ChapterSummary3D(SafeThreeDScene):
    """สรุปทั้งบท 7 — โมเดล 3D เครื่องกำเนิดตัวเดียว เดินกล้องต่อเนื่องแทนการ์ด
    ข้อความแยกๆ แบบ EP18 เดิม สร้างตามกฎ Min §21 (2026-09-01):
      1) โมเดล 3D มีชิ้นส่วนจริงที่เกี่ยวข้องครบ (เสา N/S, แกนอาร์เมเจอร์, ขดลวด
         สนาม, ตัวนำอาร์เมเจอร์, เพลา, สายเซรี่ฟิลด์) ไม่ใช่แค่ลูกศร/ข้อความลอย
      2) แต่ละจุดสรุปต่อเนื่องจากจุดก่อนหน้า — ซูมจากขดลวดที่เพิ่งไฮไลต์ไปแกนที่
         อยู่ติดกัน ไม่ตัดฉากไปเรื่องใหม่ที่ไม่เกี่ยวกัน
      3) ข้อความทั้งหมดอยู่โซนบน (caption_top/title) ปล่อยครึ่งล่างให้โมเดล 3D
      4) เนื้อหาเช็คกับเว็บแล้ว (2026-09-01): eddy loss ∝ thickness²×speed²×flux²
         (allaboutcircuits.com, sciencedirect.com) และ long-shunt Is=Ia /
         short-shunt Is=IL (electrical4u.com, testbook.com) — ตรงกับที่โน้ต
         W06-07 บทที่7 เขียนไว้แล้วทุกจุด ไม่มีจุดไหนขัดกัน
      5) กล้อง zoom_to()/move_camera ใช้ API จริงของ ThreeDScene ใน Manim
         Community ตาม docs.manim.community (ยืนยันแล้วใน §19 ของสกิล ไม่ใช่
         ManimGL) — ไม่ใช่กล้องที่ประดิษฐ์เอง
      ซูมทุกจุดจำกัดไว้ที่ ≤1.8 เท่า และจุดซูมอยู่ใกล้ระดับ y=0 เพื่อไม่ให้เนื้อหา
      ที่ขยายแล้วไปชนโซนข้อความบน (บทเรียน §19 — linter ตรวจไม่เจอเรื่องนี้)
    """

    def construct(self):
        self.set_camera_orientation(phi=58 * DEGREES, theta=-52 * DEGREES, distance=8.5)

        ttl = self.hud(title("สรุปบทที่ 7 (3D)", size=25))
        pref = self.hud(page_ref("หน้า 17 · คำถามท้ายบท"))
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.8)

        # ---------- โมเดลเครื่องกำเนิด DC ตัวเดียวที่ใช้ตลอดทั้งคลิป ----------
        pole_n, label_n = pole_box3("N", -2.5, EMF)
        pole_s, label_s = pole_box3("S", 2.5, FIELD)
        self.world_text(label_n, label_s)

        core = Circle(radius=0.95, color=METAL, fill_color="#546E7A",
                      fill_opacity=0.75).move_to(STAGE)
        conductors = VGroup(*[
            Text("x" if i % 2 == 0 else "o", font_size=15, color=WHITE)
            .move_to(STAGE + np.array([0.95 * np.cos(a), 0.95 * np.sin(a), 0]))
            for i, a in enumerate(np.linspace(0, 2 * np.pi, 8, endpoint=False))
        ])
        self.world_text(conductors)

        field_coil_n = coil_wrap(pole_n[0].get_center(), 1.3, 2.25, CURRENT)
        field_coil_s = coil_wrap(pole_s[0].get_center(), 1.3, 2.25, CURRENT)

        shaft = line3(STAGE + RIGHT * 0.95, STAGE + RIGHT * 3.6, METAL, thickness=0.05)
        brush_pt = STAGE + RIGHT * 1.35
        load_pt = STAGE + RIGHT * 3.4

        self.play(FadeIn(pole_n), FadeIn(pole_s), FadeIn(core),
                  FadeIn(conductors), FadeIn(shaft), run_time=1.2)
        self.wait(0.4)

        # ========== จุดที่ 1: การสูญเสีย 2 ชนิด ==========
        cap1 = self.hud(caption_top(
            "จุดที่ 1 — การสูญเสีย 2 ชนิด: ทองแดง (เหลือง, ขึ้นกับโหลด)"
            " vs แกนเหล็ก+กล (ส้ม, คงที่)"))
        self.play(FadeIn(cap1), run_time=0.8)
        self.play(FadeIn(field_coil_n), FadeIn(field_coil_s), run_time=0.9)
        self.play(core.animate.set_fill(WARN, opacity=0.8), run_time=0.8)
        self.wait(1.0)

        # ========== จุดที่ 2: ความต้านทาน/อุณหภูมิ — ต่อจากขดลวดที่เพิ่งเห็น ==========
        self.play(FadeOut(cap1), run_time=0.4)
        cap2 = self.hud(caption_top(
            "จากขดลวดทองแดงที่เพิ่งไฮไลต์ — R เพิ่ม 1% ทุก 2.5°C ที่ร้อนขึ้น"))
        self.play(FadeIn(cap2), run_time=0.6)
        self.zoom_to(field_coil_n.get_center(), zoom=1.7, run_time=1.4)
        temp_eq = MathTex(r"20^\circ\text{C}\to70^\circ\text{C}:\ \ R\times1.2",
                           font_size=28, color=CURRENT).move_to([0, 1.7, 0])
        self.hud(temp_eq)
        self.play(FadeIn(temp_eq), run_time=0.7)
        self.wait(1.3)
        self.play(FadeOut(temp_eq), run_time=0.4)

        # ========== จุดที่ 3: eddy current — ซูมต่อไปแกนที่ติดกัน ==========
        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = self.hud(caption_top(
            "ติดกับขดลวดคือแกนเหล็กสีส้มเดียวกัน — หมุนตัดสนาม เกิด eddy current"))
        self.play(FadeIn(cap3), run_time=0.6)
        self.zoom_to(STAGE, zoom=1.6, run_time=1.3)
        p_solid = Text("P = 100 W", font_size=24, color=WARN).move_to([0, 1.7, 0])
        self.hud(p_solid)
        self.play(FadeOut(conductors), FadeIn(p_solid), run_time=0.7)
        self.wait(0.8)

        lam = VGroup(*[
            Rectangle(width=1.75, height=0.075, color=METAL,
                      fill_color="#546E7A", fill_opacity=0.8, stroke_width=1)
            .move_to(STAGE + np.array([0, y, 0]))
            for y in np.linspace(-0.9, 0.9, 12)
        ])
        cap3b = self.hud(caption_top(
            "แบ่งเป็นแผ่นบาง (lamination) — P ∝ ความหนา² -> เหลือ 1/4 เมื่อหั่นครึ่ง",
            color=OK))
        self.play(FadeOut(core), FadeIn(lam), run_time=0.7)
        self.play(FadeOut(cap3), run_time=0.3)
        self.play(FadeIn(cap3b), run_time=0.4)
        p_lam = Text("P = 25 W  (เหลือ 1/4)", font_size=22, color=OK).move_to([0, 1.7, 0])
        self.hud(p_lam)
        self.play(FadeOut(p_solid), run_time=0.3)
        self.play(FadeIn(p_lam), run_time=0.4)
        self.wait(1.2)

        # ========== กลับสู่ภาพรวม — จุดที่ 4: ตรวจคำตอบด้วยสมการไหลกำลัง ==========
        self.play(FadeOut(cap3b), FadeOut(p_lam), run_time=0.4)
        self.zoom_to(ORIGIN, zoom=1.0, run_time=1.3)
        self.play(FadeOut(lam), FadeIn(core), FadeIn(conductors), run_time=0.5)
        cap4 = self.hud(caption_top(
            "จุดที่ 4 — ทุกก้อนที่เพิ่งเห็นรวมกันในสมการตรวจคำตอบทุกข้อ"))
        self.play(FadeIn(cap4), run_time=0.7)

        p_in = arrow3(STAGE + LEFT * 3.6, STAGE + LEFT * 0.95, WARN, thickness=0.05)
        p_out = arrow3(load_pt, load_pt + RIGHT * 0.9, OK, thickness=0.05)
        eq = MathTex(r"E\,I_a=P_{out}+P_{cu}", font_size=30, color=WHITE).move_to([0, 1.6, 0])
        self.hud(eq)
        self.play(FadeIn(p_in), FadeIn(p_out), run_time=0.8)
        self.play(FadeIn(eq), run_time=0.7)
        self.wait(1.3)

        # ========== จุดที่ 5: ประสิทธิภาพสูงสุด — เฟรมเดิม ไม่ตัดฉาก ==========
        # เก็บลูกศร/สมการของจุดที่ 4 ก่อน — ปล่อยค้างไว้จะไปทับป้าย long/short-shunt
        # ของจุดที่ 6 ตอนซูมเข้า (เจอจริงจากเฟรมที่แตกออกมาตรวจ ที่ t=33s)
        self.play(FadeOut(cap4), FadeOut(eq), FadeOut(p_in), FadeOut(p_out), run_time=0.4)
        cap5 = self.hud(caption_top(
            "จุดที่ 5 — โหลดลดครึ่ง: ตัวนำอาร์เมเจอร์ (เหลือง) หรี่ลง"
            " แต่ขดลวด+แกน (คงที่) ไม่หรี่"))
        self.play(FadeIn(cap5), run_time=0.7)
        self.play(conductors.animate.set_opacity(0.35), run_time=1.0)
        eta_row = VGroup(
            Text("η เต็มโหลด 87.02%", font_size=22, color=WHITE),
            Text("η ครึ่งโหลด 81.08%", font_size=22, color=WARN),
        ).arrange(RIGHT, buff=0.6).move_to([0, 1.6, 0])
        self.hud(eta_row)
        self.play(FadeIn(eta_row), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(eta_row), FadeOut(cap5),
                  conductors.animate.set_opacity(1.0), run_time=0.5)

        # ========== จุดที่ 6: long-shunt vs short-shunt — ซูมไปจุดต่อเซรี่ฟิลด์ ==========
        cap6 = self.hud(caption_top(
            "จุดที่ 6 — เซรี่ฟิลด์ตัวเดียวกัน ต่อคนละจุดบนสายเส้นเดียวกันนี้"))
        self.play(FadeIn(cap6), run_time=0.7)
        # เก็บเสา N/S + ขดลวดก่อนซูม — ไม่งั้นตอนซูม 1.7x เสา N (ซ้ายสุด) จะพองขึ้นไป
        # ชนโซนคำบรรยายบน (บทเรียน §19: zoom_to() ที่ linter ตรวจไม่เจอ — เจอจริงจาก
        # เฟรมที่แตกออกมาตรวจที่ t=30s/33s) เสา/ขดลวดก็ไม่ใช่จุดสนใจของช่วงนี้อยู่แล้ว
        self.play(FadeOut(pole_n), FadeOut(pole_s),
                  FadeOut(field_coil_n), FadeOut(field_coil_s), run_time=0.5)
        self.zoom_to((brush_pt + load_pt) / 2, zoom=1.7, run_time=1.4)

        series_coil = Circle(radius=0.28, color=CURRENT, stroke_width=5).move_to(brush_pt)
        tag_long = Text("long-shunt: Is = Ia", font_size=22, color=CURRENT).move_to([0, 1.7, 0])
        self.hud(tag_long)
        self.play(Create(series_coil), FadeIn(tag_long), run_time=0.9)
        self.wait(1.0)

        tag_short = Text("short-shunt: Is = IL", font_size=22, color=OK).move_to([0, 1.7, 0])
        self.hud(tag_short)
        self.play(series_coil.animate.move_to(load_pt), run_time=1.0)
        self.play(FadeOut(tag_long), run_time=0.3)
        self.play(FadeIn(tag_short), run_time=0.3)
        self.wait(1.1)

        # ---------- ปิดคลิป ----------
        self.play(FadeOut(cap6), FadeOut(tag_short), run_time=0.4)
        self.zoom_to(ORIGIN, zoom=1.0, run_time=1.2)
        self.fade_out_all(run_time=0.7)

        closer = Text(
            "ครบทั้งบทที่ 7 แล้ว — เครื่องเดียวกันตลอดคลิป ไปต่อบทถัดไปได้เลย",
            font_size=24, color=OK)
        fit_width(closer, 11.5)
        closer.move_to([0, 1.6, 0])
        self.hud(closer)
        self.play(FadeIn(closer, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)
