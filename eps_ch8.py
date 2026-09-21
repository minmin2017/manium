"""EPS บทที่ 8 — ลักษณะสมบัติของเครื่องกำเนิดไฟฟ้ากระแสตรงแต่ละชนิด

ซีรีส์ EP22-EP33 ต่อจาก EP01-EP21 (บทที่ 1-7)

  EP22  สูตร E = kφn, ชิ้นส่วน Z/P/a/Φ/n, โมเดล 3D + ป้ายชื่อ
  EP23  เคอร์ฟการอิ่มตัว (saturation curve), knee point, ฮิสเตอรีซิส, ตย.8-1,8-2
  EP24  เส้นความต้านทานฟิลด์ (field-resistance line), สโลป = R
  EP25  กระบวนการสร้างแรงเคลื่อน 5 ขั้น (voltage build-up) — คลิปสำคัญที่สุด
  EP26  ความต้านทานวิกฤต (critical resistance), เส้นสัมผัสเคอร์ฟ
  EP27  3 สาเหตุเครื่องไม่สร้างแรงเคลื่อน + flashing the field
  EP28  3 สาเหตุ Vt ตก, เคอร์ฟภายนอก + จุดเบรกดาวน์
  EP29  %VR สูตรและตัวอย่าง 8-3 (8.7%)
  EP30  Cumulative compound: short-shunt vs long-shunt, ตย.8-4 (-12% VR)
  EP31  Differential compound, งานเชื่อม/ชุบโลหะ
  EP32  Over/flat/under compound, ไดเวอร์เตอร์, ตย.8-7 (Rd = 0.0164 Ω)
  EP33  เครื่องกำเนิดแบบอนุกรม + series booster

สีประจำปริมาณ (Mayer signaling — ตามที่ eps_ch6/ch7 ตั้งไว้แล้วใน mlib.py):
  CURRENT  #FFB300   กระแส I / ขดลวดทองแดง
  FIELD    #42A5F5   สนามแม่เหล็ก B / ฟลักซ์ / แรงดันที่ตกลง
  EMF      #EF5350   แรงเคลื่อน E
  OK       #26C6DA   ผลลัพธ์ / ข้อสรุปที่ถูกต้อง
  WARN     #FF7043   จุดสำคัญ / ปัญหา / ค่าวิกฤต
  METAL    #90A4AE   ชิ้นส่วนโลหะ / โครงสร้าง
  GRAYTXT  #B0BEC5   ข้อความรอง

กฎบังคับ (จาก mlib.py / EPS_Ch8_Video_Plan.md):
  1. Subclass SafeScene (layout linter ทำงานอัตโนมัติทุก 0.25 วิ)
  2. arrow3()/line3() จาก mlib.py เท่านั้น สำหรับเส้น/ลูกศร 3D
  3. ข้อความไทยห้ามอยู่ใน MathTex \\text{} — ใช้ Text() + VGroup().arrange()
  4. caption_top() เป็นค่าเริ่มต้น (โซนบน y=2.72) ไม่ใช้ caption() (โซนล่างถูกบัง)
  5. กล้องนิ่ง static camera ตลอด (ไม่มี zoom_to / move_camera ในทุกคลิปชุดนี้)
  6. ตัวเลขตรวจแล้วทั้งหมด: 113V, 81.43V, 8.7%, -12%, 115A, 0.0164 Ω — ห้ามคำนวณใหม่
"""

import numpy as np
from manim import *
from mlib import (
    SafeScene, title, caption_top, page_ref,
    fit_width, CURRENT, FIELD, EMF, OK, WARN, METAL, GRAYTXT,
)

# exam_card and build_generator_model are defined in eps_ch7.py
from eps_ch7 import exam_card, build_generator_model, STAGE


# =================== helper เฉพาะซีรีส์ ch8 ===================

def ch8_exam_card(q, a, y=0.0):
    """การ์ดจุดออกสอบ — ใช้แบบเดียวกับ eps_ch7.py exam_card แต่ import ตรง"""
    head = Text(จุดออกสอบ, font_size=20, color="#FFD54F")
    qq = Text(q, font_size=22, color=WHITE)
    fit_width(qq, 11.5)
    aa = Text(a, font_size=20, color=OK)
    fit_width(aa, 11.5)
    card = VGroup(head, qq, aa).arrange(DOWN, buff=0.30)
    card.move_to([0, y, 0])
    return card


# ใช้ exam_card alias
exam_card = ch8_exam_card


def sat_curve_axes(x_range=(0, 3.5), y_range=(0, 3.0),
                   x_len=6.0, y_len=4.5, ox=-3.0, oy=-2.0):
    """แกน Voc vs If สำหรับ saturation curve — ใช้ซ้ำใน EP23/EP24/EP25/EP26"""
    ax = Axes(
        x_range=[x_range[0], x_range[1], 0.5],
        y_range=[y_range[0], y_range[1], 0.5],
        x_length=x_len,
        y_length=y_len,
        axis_config={"color": GRAYTXT, "stroke_width": 2,
                     "include_tip": True, "tip_length": 0.18},
        x_axis_config={"numbers_to_exclude": []},
        y_axis_config={"numbers_to_exclude": []},
    ).move_to([ox + x_len / 2, oy + y_len / 2, 0])
    return ax


def sat_curve_graph(ax, color=FIELD, stroke=3):
    """เส้นเคอร์ฟการอิ่มตัว (ประมาณ) — sigmoid-like ตามรูปที่ 8-1"""
    def sat(x):
        # เริ่มเกือบเส้นตรง จากนั้นอิ่มตัว — ปรับ scale ให้ดูดีในแกน x=[0,3.5], y=[0,3]
        return 2.6 * (1 - np.exp(-1.5 * x)) + 0.08 * x
    return ax.plot(sat, x_range=[0, 3.5, 0.02], color=color, stroke_width=stroke)


# ================================================================
# EP22 — สูตร EMF และชิ้นส่วนเครื่องกำเนิด
# ================================================================
class EP22_EMFEquation(SafeScene):
    """8-1, 8-2 — สูตร E = kφn, ชิ้นส่วน Z/P/a/Φ/n + โมเดลแสดงชิ้นส่วน

    beat-by-beat:
    t=0-1   FadeIn title + page_ref
    t=1-2   caption_top: บทนี้คือ ภาคต่อ บทที่ 5 — เจาะลึกพฤติกรรม
    t=2-5   Write สูตร E = ZPφn/(60a) + อธิบาย k = ZP/60a
    t=5-7   Indicate ตัวแปรคงที่ (Z,P,a) → รวบเป็น k
    t=7-9   caption_top: "แค่ 2 ตัวแปรจริง — φ และ n"
    t=9-12  โมเดล 2D เครื่องกำเนิด: วาด N/S pole + armature + commutator + brush
            ป้ายชื่อชิ้นส่วนกระพริบทีละชิ้น
    t=12-15 กฎจำ: เพิ่ม φ (ปรับ If) หรือ เพิ่ม n → E เปลี่ยน
    t=15-17 exam_card
    """

    def construct(self):
        ttl = title("EP22 — สูตร EMF เครื่องกำเนิด DC", size=27)
        ref = page_ref("หน้า 1-2 · 8-1, 8-2")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("บทที่ 8 คือภาคต่อของบทที่ 5 — เจาะพฤติกรรม Vt ของแต่ละชนิดเครื่องกำเนิด")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.9)

        # ---- สูตรเต็ม ----
        cap1 = caption_top("สูตรตัวแม่ของบท: E มาจากอะไรบ้าง?", color=EMF)
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.5)

        eq_full = MathTex(
            r"E = \frac{ZP}{60a}\,\phi\,n",
            font_size=52, color=EMF
        ).move_to([0, 0.9, 0])
        self.play(Write(eq_full), run_time=1.2)
        self.wait(0.5)

        # labels ใต้สูตร
        labels = VGroup(
            Text("Z = จำนวนตัวนำ", font_size=19, color=GRAYTXT),
            Text("P = จำนวนขั้ว", font_size=19, color=GRAYTXT),
            Text("a = ทางขนาน (parallel paths)", font_size=19, color=GRAYTXT),
            Text("φ = ฟลักซ์ต่อขั้ว  (Wb)", font_size=19, color=FIELD),
            Text("n = ความเร็วรอบ  (rpm)", font_size=19, color=CURRENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.0, -0.8, 0])
        fit_width(labels, 7.0)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in labels],
                              lag_ratio=0.18), run_time=1.5)
        self.wait(0.6)

        # ---- รวบ Z,P,a เป็น k ----
        bracket = SurroundingRectangle(VGroup(labels[0], labels[1], labels[2]),
                                       color=WARN, buff=0.12, stroke_width=2)
        k_note_eq = MathTex(r"k = \frac{ZP}{60a}", font_size=28, color=WARN)
        k_note_txt = Text(คงที่ประจำเครื่อง, font_size=18, color=WARN)
        k_note = VGroup(k_note_eq, k_note_txt).arrange(RIGHT, buff=0.2)
        k_note.next_to(bracket, RIGHT, buff=0.3)
        self.play(Create(bracket), run_time=0.7)
        self.play(FadeIn(k_note), run_time=0.7)
        self.wait(0.5)

        eq_simple = MathTex(r"E = k\,\phi\,n", font_size=56, color=EMF).move_to([3.6, 0.9, 0])
        self.play(TransformFromCopy(eq_full, eq_simple), run_time=1.0)
        self.wait(0.5)

        self.play(FadeOut(cap1), run_time=0.3)
        cap2 = caption_top("เหลือแค่ 2 ตัวแปรจริง — ปรับ φ (ปรับ If) หรือ ปรับ n (ปรับตัวขับ)", color=OK)
        self.play(FadeIn(cap2), run_time=0.5)
        self.wait(1.2)

        # ---- โมเดล 2D เครื่องกำเนิด ----
        self.play(
            FadeOut(eq_full), FadeOut(eq_simple), FadeOut(bracket),
            FadeOut(k_note), FadeOut(labels), FadeOut(cap2),
            run_time=0.6
        )

        cap3 = caption_top("โครงสร้างชิ้นส่วนเครื่องกำเนิด DC", color=METAL)
        self.play(FadeIn(cap3), run_time=0.5)

        # ขั้ว N/S
        pole_n = RoundedRectangle(width=1.3, height=2.6, corner_radius=0.1,
                                   fill_color=METAL, fill_opacity=0.55,
                                   stroke_color=METAL, stroke_width=2).move_to([-3.5, 0, 0])
        pole_s = RoundedRectangle(width=1.3, height=2.6, corner_radius=0.1,
                                   fill_color=METAL, fill_opacity=0.55,
                                   stroke_color=METAL, stroke_width=2).move_to([3.5, 0, 0])
        lab_n = Text("N", font_size=36, color=EMF).move_to(pole_n.get_center())
        lab_s = Text("S", font_size=36, color=FIELD).move_to(pole_s.get_center())
        pole_lbl = Text("ขั้วแม่เหล็ก (N/S Pole)", font_size=18, color=METAL)
        pole_lbl.next_to(pole_n, UP, buff=0.2)

        # Armature
        armature = Circle(radius=1.0, color=METAL, fill_color="#546E7A",
                          fill_opacity=0.75).move_to([0, 0, 0])
        arm_lbl = Text(อาร์เมเจอร์, font_size=18, color=METAL)
        arm_lbl.next_to(armature, UP, buff=0.1)

        # Commutator
        comm = Rectangle(width=0.6, height=0.5, color=CURRENT,
                         fill_color=CURRENT, fill_opacity=0.6).next_to(armature, RIGHT, buff=0.05)
        comm_lbl = Text(คอมมิวเตเตอร์, font_size=16, color=CURRENT)
        comm_lbl.next_to(comm, RIGHT, buff=0.1)

        # Brushes
        br_top = Rectangle(width=0.18, height=0.35, color="#F5F5F5",
                            fill_color="#F5F5F5", fill_opacity=0.9)
        br_top.next_to(comm, UP, buff=0.02)
        br_bot = Rectangle(width=0.18, height=0.35, color="#F5F5F5",
                            fill_color="#F5F5F5", fill_opacity=0.9)
        br_bot.next_to(comm, DOWN, buff=0.02)
        brush_lbl = Text("แปรงถ่าน (Brush)", font_size=16, color="#F5F5F5")
        brush_lbl.next_to(br_top, RIGHT, buff=0.15).shift(UP * 0.05)

        # Shunt field winding
        field_coil = Rectangle(width=0.35, height=2.5, color=CURRENT, stroke_width=4)
        field_coil.move_to(pole_n.get_center())
        field_lbl = Text(ขดลวดชันท์ฟิลด์, font_size=16, color=CURRENT)
        field_lbl.next_to(field_coil, DOWN, buff=0.2)

        self.play(FadeIn(pole_n), FadeIn(lab_n), FadeIn(pole_s), FadeIn(lab_s),
                  run_time=0.8)
        self.play(FadeIn(pole_lbl, shift=UP * 0.1), run_time=0.5)
        self.wait(0.3)

        self.play(FadeIn(armature), run_time=0.6)
        self.play(Indicate(armature, color=OK, scale_factor=1.08), run_time=0.5)
        self.play(FadeIn(arm_lbl, shift=UP * 0.1), run_time=0.4)
        self.wait(0.3)

        self.play(FadeIn(field_coil), run_time=0.5)
        self.play(Indicate(field_coil, color=CURRENT, scale_factor=1.1), run_time=0.5)
        self.play(FadeIn(field_lbl, shift=DOWN * 0.1), run_time=0.4)
        self.wait(0.3)

        self.play(FadeIn(comm), run_time=0.5)
        self.play(FadeIn(br_top), FadeIn(br_bot), run_time=0.4)
        self.play(Indicate(comm, color=CURRENT, scale_factor=1.1), run_time=0.4)
        self.play(FadeIn(comm_lbl), FadeIn(brush_lbl), run_time=0.4)
        self.wait(0.4)

        # ---- กฎจำ ----
        self.play(FadeOut(cap3), run_time=0.3)
        cap4 = caption_top("กฎจำ: เปลี่ยน E ได้ 2 ทาง — ปรับ φ (เพิ่ม/ลด If) หรือ ปรับ n (ตัวขับ)", color=EMF)
        self.play(FadeIn(cap4), run_time=0.5)
        self.wait(1.6)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-1: E ขึ้นกับตัวแปรอะไรที่ปรับได้ระหว่างใช้งาน?",
            "2 ตัวแปร — ฟลักซ์ φ (ปรับ If ผ่านรีโอสตาท) และ ความเร็วรอบ n (ปรับตัวขับ)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP23 — เคอร์ฟการอิ่มตัว + ฮิสเตอรีซิส + ตย.8-1, 8-2
# ================================================================
class EP23_SaturationCurve(SafeScene):
    """8-3 + ตย.8-1,8-2 — เคอร์ฟการอิ่มตัว, knee point, ฮิสเตอรีซิส

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: ตรึง n คงที่ ค่อยๆ เพิ่ม If → E ไม่เป็นเส้นตรง
    t=2-7   วาดแกน + เส้นเคอร์ฟ + ป้ายจุด 1-5 (knee, อิ่มตัว, ฮิสเตอรีซิส)
    t=7-9   อธิบายจุด 1 = residual magnetism
    t=9-12  อธิบาย knee + อิ่มตัว
    t=12-14 อธิบายวง ฮิสเตอรีซิส (ขาลงไม่ทับขาขึ้น)
    t=14-17 ตย.8-1: E∝n เส้นตรง → 113 V
    t=17-20 ตย.8-2: scale เคอร์ฟตาม n → 81.43 V
    t=20-22 exam_card
    """

    def construct(self):
        ttl = title("EP23 — เคอร์ฟการอิ่มตัว + ฮิสเตอรีซิส", size=26)
        ref = page_ref("หน้า 2-6 · รูปที่ 8-1 · ตย.8-1,8-2")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("ตรึง n คงที่ แล้วค่อยๆ เพิ่ม If -> E ขึ้นตามเคอร์ฟ ไม่ใช่เส้นตรง", color=FIELD)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.9)

        # ---- วาดแกน ----
        ax = sat_curve_axes(x_range=(0, 3.5), y_range=(0, 3.0),
                             x_len=5.5, y_len=3.8, ox=-3.5, oy=-2.3)
        x_label = Text("If (A)", font_size=18, color=GRAYTXT)
        y_label = Text("E, Vt (V)", font_size=18, color=GRAYTXT)
        x_label.next_to(ax.x_axis.get_right(), RIGHT, buff=0.1)
        y_label.next_to(ax.y_axis.get_top(), UP, buff=0.05)
        self.play(Create(ax), FadeIn(x_label), FadeIn(y_label), run_time=1.0)

        # เส้นเคอร์ฟขาขึ้น
        curve_up = sat_curve_graph(ax, color=FIELD, stroke=3)
        self.play(Create(curve_up), run_time=1.2)

        # ---- ป้ายจุด 1-5 ----
        def sat(x):
            return 2.6 * (1 - np.exp(-1.5 * x)) + 0.08 * x

        pts = {
            1: (0.0, sat(0.0)),
            2: (0.8, sat(0.8)),
            3: (1.4, sat(1.4)),
            4: (3.0, sat(3.0)),
            5: (0.0, sat(0.0) * 0.97),  # ขาลงสิ้นสุด (ฮิสเตอรีซิส)
        }
        colors_pts = {1: GRAYTXT, 2: FIELD, 3: WARN, 4: GRAYTXT, 5: GRAYTXT}
        dots_g = VGroup()
        labels_g = VGroup()
        for k, (xv, yv) in [(1, pts[1]), (2, pts[2]), (3, pts[3]), (4, pts[4])]:
            pos = ax.coords_to_point(xv, yv)
            d = Dot(pos, color=colors_pts[k], radius=0.1)
            lbl_txt = {
                1: "①  อำนาจตกค้าง",
                2: "②  ช่วงเส้นตรง",
                3: "③  Knee",
                4: "④  อิ่มตัว",
            }[k]
            lbl = Text(lbl_txt, font_size=17, color=colors_pts[k])
            lbl.next_to(d, RIGHT if k != 1 else DOWN, buff=0.15)
            dots_g.add(d)
            labels_g.add(lbl)

        self.play(FadeOut(cap0), run_time=0.3)
        cap1 = caption_top("จุด ① มาจากอำนาจแม่เหล็กตกค้าง (residual) — ยังไม่มี If เลย", color=GRAYTXT)
        self.play(FadeIn(cap1), run_time=0.5)
        self.play(FadeIn(dots_g[0]), FadeIn(labels_g[0]), run_time=0.6)
        self.wait(0.5)

        self.play(FadeOut(cap1), run_time=0.3)
        cap2 = caption_top("ช่วง ②→③ เพิ่ม If แล้ว E เพิ่มเกือบเส้นตรง — ยังไม่อิ่มตัว", color=FIELD)
        self.play(FadeIn(cap2), run_time=0.5)
        self.play(FadeIn(dots_g[1]), FadeIn(labels_g[1]),
                  FadeIn(dots_g[2]), FadeIn(labels_g[2]), run_time=0.7)
        self.wait(0.8)

        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = caption_top("จุด ④ อิ่มตัวเต็มที่ — เพิ่ม If อีกเท่าไหร่ E ก็แทบไม่ขยับ", color=WARN)
        self.play(FadeIn(cap3), run_time=0.5)
        self.play(FadeIn(dots_g[3]), FadeIn(labels_g[3]), run_time=0.6)
        self.wait(0.8)

        # ---- วงฮิสเตอรีซิส (ขาลงไม่ทับขาขึ้น) ----
        self.play(FadeOut(cap3), run_time=0.3)
        cap4 = caption_top("ขาลง ④→⑤ ไม่ทับขาขึ้น — วงฮิสเตอรีซิส แกนเหล็กจำอำนาจไว้บางส่วน", color=WARN)
        self.play(FadeIn(cap4), run_time=0.5)

        # เส้นขาลงที่อยู่เหนือเล็กน้อย
        def sat_down(x):
            return sat(x) * 1.04 + 0.05
        curve_down = ax.plot(sat_down, x_range=[0.0, 3.0, 0.02],
                             color=EMF, stroke_width=2.5, stroke_opacity=0.85)
        down_arrow = Arrow(
            ax.coords_to_point(2.5, sat_down(2.5)),
            ax.coords_to_point(1.0, sat_down(1.0)),
            color=EMF, buff=0, stroke_width=2.5, tip_length=0.18
        )
        self.play(Create(curve_down), GrowArrow(down_arrow), run_time=1.0)
        hist_lbl = Text("⑤ ขาลง\n(ฮิสเตอรีซิส)", font_size=16, color=EMF)
        hist_lbl.next_to(ax.coords_to_point(0.5, sat_down(0.5)), LEFT, buff=0.1)
        self.play(FadeIn(hist_lbl), run_time=0.4)
        self.wait(1.0)

        # ---- ตัวอย่าง 8-1: E ∝ n ----
        self.play(
            FadeOut(cap4), FadeOut(curve_down), FadeOut(down_arrow),
            FadeOut(hist_lbl), FadeOut(dots_g), FadeOut(labels_g),
            FadeOut(ax), FadeOut(x_label), FadeOut(y_label),
            FadeOut(curve_up), run_time=0.6
        )

        cap5 = caption_top("ตย.8-1 — ตรึงฟลักซ์คงที่ เปลี่ยน n เท่านั้น: E ∝ n เส้นตรงจริง", color=EMF)
        self.play(FadeIn(cap5), run_time=0.5)

        ex1 = VGroup(
            Text("n₁ = 1750 rpm → E₁ = 110 V", font_size=22, color=GRAYTXT),
            Text("n₂ = 1800 rpm → E₂ = ?", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.8, 0])
        self.play(FadeIn(ex1), run_time=0.7)

        eq1 = MathTex(
            r"E_2 = 110 \times \frac{1800}{1750} = \mathbf{113\ \text{V}}",
            font_size=38, color=EMF
        ).move_to([0, -0.6, 0])
        self.play(Write(eq1), run_time=1.0)
        self.wait(0.8)

        # ---- ตัวอย่าง 8-2: scale เคอร์ฟ ----
        self.play(FadeOut(cap5), FadeOut(ex1), FadeOut(eq1), run_time=0.4)
        cap6 = caption_top("ตย.8-2 — scale เคอร์ฟ 1400 rpm → 1000 rpm ทีละจุด: E ∝ n ต่อจุด", color=FIELD)
        self.play(FadeIn(cap6), run_time=0.5)

        ex2 = VGroup(
            Text("If = 0.4 A  →  E(1400) = 114 V", font_size=22, color=GRAYTXT),
        ).move_to([0, 0.9, 0])
        self.play(FadeIn(ex2), run_time=0.6)

        eq2 = MathTex(
            r"E_2 = 114 \times \frac{1000}{1400} = \mathbf{81.43\ \text{V}}",
            font_size=36, color=FIELD
        ).move_to([0, -0.3, 0])
        self.play(Write(eq2), run_time=1.0)

        note = Text("ทำแบบนี้ทุกจุดในตาราง → ได้เคอร์ฟที่ 1000 rpm (เตี้ยกว่า แต่รูปทรงเหมือน)",
                    font_size=19, color=GRAYTXT).move_to([0, -1.5, 0])
        fit_width(note, 11.5)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-2: ที่ If=0 ยังมี E อยู่เล็กน้อย เพราะอะไร?",
            "เพราะอำนาจแม่เหล็กตกค้าง (residual magnetism) ในแกนเหล็กจากการใช้งานครั้งก่อน")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP24 — เส้นความต้านทานฟิลด์ (Field-resistance line)
# ================================================================
class EP24_FieldResistanceLine(SafeScene):
    """8-4 — เส้นความต้านทานฟิลด์: กฎโอห์ม, สโลป = R

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: Vf = If × Rf → เส้นตรงผ่านจุดกำเนิด สโลป = Rf
    t=2-5   วาดแกน + เส้นเคอร์ฟ (อ้างอิง)
    t=5-9   วาดเส้น Rf 3 ค่า (max/mid/min) พร้อมป้ายสโลป
    t=9-12  อธิบาย: ความต้านทานมาก = เส้นชัน, น้อย = เส้นราบ
    t=12-14 อธิบาย: ทำไมต้องมีเส้นนี้ (จะไปซ้อนกับเคอร์ฟใน EP25)
    t=14-16 exam_card
    """

    def construct(self):
        ttl = title("EP24 — เส้นความต้านทานฟิลด์", size=27)
        ref = page_ref("หน้า 7-8 · 8-4 · รูปที่ 8-3")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("วงจรฟิลด์เป็นแค่ตัวต้านทาน: Vf = If × Rf → เส้นตรงผ่านจุดกำเนิด", color=CURRENT)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.8)

        # ---- แกนและเส้นเคอร์ฟ ----
        ax = sat_curve_axes(x_range=(0, 3.5), y_range=(0, 3.0),
                             x_len=5.5, y_len=3.8, ox=-3.5, oy=-2.3)
        x_label = Text("If (A)", font_size=18, color=GRAYTXT)
        y_label = Text("E, Vt (V)", font_size=18, color=GRAYTXT)
        x_label.next_to(ax.x_axis.get_right(), RIGHT, buff=0.1)
        y_label.next_to(ax.y_axis.get_top(), UP, buff=0.05)
        curve = sat_curve_graph(ax, color=FIELD, stroke=2.5)
        curve_lbl = Text(เคอร์ฟอิ่มตัว, font_size=16, color=FIELD)
        curve_lbl.move_to(ax.coords_to_point(3.2, 2.2)).shift(LEFT * 0.1)
        self.play(Create(ax), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        self.play(Create(curve), FadeIn(curve_lbl), run_time=0.9)

        # ---- เส้น Rf 3 ค่า ----
        self.play(FadeOut(cap0), run_time=0.3)
        cap1 = caption_top("สโลปของเส้น = ค่าความต้านทานรวมของวงจรฟิลด์ Rf", color=CURRENT)
        self.play(FadeIn(cap1), run_time=0.5)

        rf_data = [
            (0.55, "R_max (สูง)", WARN),
            (0.80, "R (กลาง)", OK),
            (1.30, "R_min (ต่ำ)", CURRENT),
        ]
        lines_g = VGroup()
        line_lbls = VGroup()
        for slope, name, clr in rf_data:
            # เส้น Rf: Vf = slope × If → y = slope × x
            rf_line = ax.plot(lambda x, s=slope: s * x,
                              x_range=[0, 3.0, 0.1], color=clr, stroke_width=2.5)
            lbl_pos = ax.coords_to_point(2.5, slope * 2.5)
            lbl = Text(name, font_size=16, color=clr).next_to(lbl_pos, RIGHT, buff=0.1)
            lines_g.add(rf_line)
            line_lbls.add(lbl)
            self.play(Create(rf_line), FadeIn(lbl), run_time=0.6)
            self.wait(0.2)
        self.wait(0.8)

        self.play(FadeOut(cap1), run_time=0.3)
        cap2 = caption_top("R มาก → เส้นชัน (ตัดเคอร์ฟต่ำ);  R น้อย → เส้นราบ (ตัดเคอร์ฟสูง)", color=OK)
        self.play(FadeIn(cap2), run_time=0.5)
        self.wait(0.9)

        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = caption_top("เส้นนี้จะไปซ้อนกับเคอร์ฟในคลิปถัดไป → หาจุดสมดุลแรงเคลื่อน", color=EMF)
        self.play(FadeIn(cap3), run_time=0.5)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-4: สโลปของเส้นความต้านทานฟิลด์คืออะไร?",
            "สโลป = Rf (ความต้านทานรวมของวงจรฟิลด์ รวมรีโอสตาท)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP25 — กระบวนการสร้างแรงเคลื่อน (Voltage Build-Up) 5 ขั้น
# ================================================================
class EP25_VoltageBuildUp(SafeScene):
    """8-5 — กระบวนการป้อนกลับบวก 5 ขั้น — คลิปสำคัญที่สุดของบท ⭐⭐⭐⭐⭐

    beat-by-beat:
    t=0-1   FadeIn title + ref (เน้นว่านี่คือคลิปหัวใจ)
    t=1-2   caption: โจทย์ปัญหา — ป้อนกลับตัวเองได้ยังไงตอนเริ่มต้น?
    t=2-5   วาดแกน + เคอร์ฟ + เส้น Rf
    t=5-7   ขั้น 1: residual → E₁ (จุดเริ่มต้น) — ป้ายเลข ①
    t=7-9   ขั้น 2: E₁ → If₁ — วิ่งไปเส้น Rf แนวนอน — ป้ายเลข ②
    t=9-11  ขั้น 3: If₁ → E₂ (สูงกว่า E₁) — วิ่งขึ้นไปเคอร์ฟ — ป้ายเลข ③
    t=11-13 ขั้น 4: E₂ → If₂ — วิ่งไปเส้น Rf อีกรอบ — ป้ายเลข ④
    t=13-15 ขั้น 5: If₂ → E₃ → … ไต่บันไดจนถึงจุดตัด — ป้ายเลข ⑤
    t=15-17 Indicate จุดตัด + caption: นี่คือจุดสมดุล steady state
    t=17-19 สรุป: "บันไดสั้นลงเรื่อยๆ จนแทบมองไม่เห็น"
    t=19-21 exam_card
    """

    def construct(self):
        ttl = title("EP25 — กระบวนการสร้างแรงเคลื่อน (Voltage Build-Up)", size=24)
        ref = page_ref("หน้า 9-12 · 8-5 · รูปที่ 8-5")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("หัวใจของบท — เครื่องกำเนิดแบบขนานป้อนกลับตัวเองสร้างแรงเคลื่อนได้ยังไง?", color=EMF)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.9)

        # ---- วาดแกน + เคอร์ฟ + เส้น Rf ----
        ax = sat_curve_axes(x_range=(0, 3.5), y_range=(0, 3.0),
                             x_len=5.8, y_len=4.0, ox=-3.6, oy=-2.35)
        x_label = Text("If (A)", font_size=18, color=GRAYTXT)
        y_label = Text("E, Vt (V)", font_size=18, color=GRAYTXT)
        x_label.next_to(ax.x_axis.get_right(), RIGHT, buff=0.1)
        y_label.next_to(ax.y_axis.get_top(), UP, buff=0.05)

        def sat(x):
            return 2.6 * (1 - np.exp(-1.5 * x)) + 0.08 * x

        curve = sat_curve_graph(ax, color=FIELD, stroke=3)
        # Rf line slope = 0.70 (ตัดเคอร์ฟประมาณที่ If=2.1, E=1.47)
        rf_slope = 0.70
        rf_line = ax.plot(lambda x: rf_slope * x, x_range=[0, 3.5, 0.05],
                          color=CURRENT, stroke_width=2.5)
        rf_lbl = Text("เส้น Rf", font_size=17, color=CURRENT)
        rf_lbl.move_to(ax.coords_to_point(3.2, rf_slope * 3.2)).shift(RIGHT * 0.3 + UP * 0.1)
        curve_lbl = Text(เคอร์ฟอิ่มตัว, font_size=17, color=FIELD)
        curve_lbl.move_to(ax.coords_to_point(3.3, sat(3.3))).shift(RIGHT * 0.2)

        self.play(FadeOut(cap0), run_time=0.3)
        self.play(Create(ax), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        self.play(Create(curve), FadeIn(curve_lbl),
                  Create(rf_line), FadeIn(rf_lbl), run_time=1.0)

        # ---- จุดตัด (steady state) ----
        # หา If* ที่ sat(x) = rf_slope * x
        from scipy.optimize import brentq
        if_star = brentq(lambda x: sat(x) - rf_slope * x, 0.1, 3.4)
        e_star = sat(if_star)
        eq_pt = ax.coords_to_point(if_star, e_star)

        # ---- บันไดขั้นที่ 1-5 ----
        # E₁ จาก residual: If=0 → E_res = sat(0) = 0
        # ใช้ค่าที่เห็นภาพชัด: เริ่มที่ If=0, Vres เล็กๆ
        steps = [
            (0.0, 0.05),            # ① residual (If=0, E_res~0.05)
            (0.05 / rf_slope, 0.05),  # ② วิ่งไปเส้น Rf แนวนอน
            (0.05 / rf_slope, sat(0.05 / rf_slope)),  # ③ วิ่งขึ้นเคอร์ฟ
            (sat(0.05 / rf_slope) / rf_slope, sat(0.05 / rf_slope)),  # ④ วิ่งไปเส้น Rf
            (sat(0.05 / rf_slope) / rf_slope,
             sat(sat(0.05 / rf_slope) / rf_slope)),   # ⑤ วิ่งขึ้นเคอร์ฟ
        ]
        # เพิ่ม 2 ขั้นสุดท้ายก่อนถึงจุดตัด
        x4 = steps[4][0]
        steps += [
            (sat(x4) / rf_slope, sat(x4)),            # ⑥ Rf
            (sat(x4) / rf_slope, sat(sat(x4) / rf_slope)),  # ⑦ curve
        ]

        step_labels = ["①", "②", "③", "④", "⑤"]
        step_captions = [
            "ขั้น ① — อำนาจแม่เหล็กตกค้างสร้าง E₁ เล็กๆ ขึ้นมาก่อน (ไม่มี If เลย)",
            "ขั้น ② — E₁ จ่ายให้วงจรฟิลด์ทันที เกิด If₁ ตามกฎโอห์ม",
            "ขั้น ③ — If₁ เพิ่มฟลักซ์ → เหนี่ยวนำ E₂ > E₁ บนเคอร์ฟ",
            "ขั้น ④ — E₂ จ่ายฟิลด์อีกรอบ → If₂ > If₁",
            "ขั้น ⑤ — วนซ้ำ (positive feedback) ไต่บันไดขึ้นเรื่อยๆ",
        ]

        # วาดบันได
        ladder_lines = VGroup()
        prev = ax.coords_to_point(0.0, 0.05)
        step_dot = Dot(prev, color=WARN, radius=0.12)
        step_num_lbl = Text("①", font_size=20, color=WARN).next_to(step_dot, LEFT, buff=0.12)

        self.play(FadeOut(cap0) if cap0 in self.mobjects else Wait(0),
                  FadeIn(step_dot), FadeIn(step_num_lbl), run_time=0.4)
        cap_step = caption_top(step_captions[0], color=WARN)
        self.play(FadeIn(cap_step), run_time=0.5)
        self.wait(1.0)

        for i, (x_next, y_next) in enumerate(steps[1:], start=1):
            next_pos = ax.coords_to_point(x_next, y_next)
            line = Line(prev, next_pos, color=WARN, stroke_width=2.5)
            ladder_lines.add(line)
            self.play(Create(line), run_time=0.7)
            prev = next_pos

            if i < len(step_labels):
                dot = Dot(prev, color=WARN, radius=0.10)
                num_lbl = Text(step_labels[i], font_size=19, color=WARN)
                num_lbl.next_to(dot, RIGHT if i % 2 == 0 else LEFT, buff=0.12)
                self.play(FadeIn(dot), FadeIn(num_lbl), run_time=0.4)
                new_cap = caption_top(step_captions[min(i, len(step_captions) - 1)], color=WARN)
                self.play(FadeOut(cap_step), run_time=0.3)
                cap_step = new_cap
                self.play(FadeIn(cap_step), run_time=0.4)
                self.wait(0.8)

        # ---- จุดสมดุล ----
        eq_dot = Dot(eq_pt, color=OK, radius=0.14)
        eq_lbl_txt = Text("จุดสมดุล\n(Steady State)", font_size=17, color=OK, line_spacing=0.9)
        eq_lbl_txt.next_to(eq_dot, UR, buff=0.15)
        self.play(FadeOut(cap_step), run_time=0.3)
        cap_eq = caption_top("บันไดสั้นลงเรื่อยๆ จนถึงจุดตัด — ไม่มีส่วนต่างให้ไต่ต่อแล้ว = สมดุล", color=OK)
        self.play(FadeIn(cap_eq), run_time=0.5)
        self.play(FadeIn(eq_dot), FadeIn(eq_lbl_txt), run_time=0.6)
        self.play(Indicate(eq_dot, color=WHITE, scale_factor=1.4), run_time=0.7)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-5: กระบวนการสร้างแรงเคลื่อนหยุดที่ไหน?",
            "หยุดที่จุดตัดของเคอร์ฟการอิ่มตัว กับ เส้นความต้านทานฟิลด์ — เพราะสองเส้นสมดุลกันพอดี")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP26 — ความต้านทานวิกฤต (Critical Resistance)
# ================================================================
class EP26_CriticalResistance(SafeScene):
    """8-6 — ความต้านทานวิกฤต: เส้นสัมผัส (tangent) กับช่วงเส้นตรงของเคอร์ฟ

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: ถ้าเพิ่ม Rf เรื่อยๆ → เส้นชันขึ้นเรื่อยๆ จนถึงค่าวิกฤต
    t=2-5   วาดแกน + เคอร์ฟ + เส้น Rf 3 ค่า (ต่ำกว่า/วิกฤต/สูงกว่า)
    t=5-8   Indicate เส้นวิกฤต (สัมผัสช่วงตรงของเคอร์ฟ)
    t=8-11  อธิบาย: Rf > Rc → แรงเคลื่อนตกเหลือแค่อำนาจตกค้าง
    t=11-14 อธิบาย: นี่คือกลไกที่รีโอสตาทสูงเกินทำให้เครื่องไม่สร้างแรงดัน
    t=14-16 exam_card
    """

    def construct(self):
        ttl = title("EP26 — ความต้านทานวิกฤต (Critical Resistance)", size=25)
        ref = page_ref("หน้า 12 · 8-6 · รูปที่ 8-6")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("เพิ่ม Rf เรื่อยๆ → เส้นชันขึ้น จนถึงค่าหนึ่งที่สัมผัสเคอร์ฟพอดี", color=WARN)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.8)

        ax = sat_curve_axes(x_range=(0, 3.5), y_range=(0, 3.0),
                             x_len=5.5, y_len=3.8, ox=-3.5, oy=-2.3)
        x_label = Text("If (A)", font_size=18, color=GRAYTXT)
        y_label = Text("E, Vt (V)", font_size=18, color=GRAYTXT)
        x_label.next_to(ax.x_axis.get_right(), RIGHT, buff=0.1)
        y_label.next_to(ax.y_axis.get_top(), UP, buff=0.05)
        curve = sat_curve_graph(ax, color=FIELD, stroke=2.5)
        self.play(Create(ax), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        self.play(Create(curve), run_time=0.7)

        # เส้น Rf ต่างๆ
        rf_low = ax.plot(lambda x: 0.6 * x, x_range=[0, 3.5, 0.05],
                         color=OK, stroke_width=2.5)
        rf_crit = ax.plot(lambda x: 1.05 * x, x_range=[0, 3.5, 0.05],
                          color=WARN, stroke_width=3)
        rf_high = ax.plot(lambda x: 1.7 * x, x_range=[0, 3.5, 0.05],
                          color=EMF, stroke_width=2.5)

        lbl_low = Text("R₃ (ต่ำ → V สูง)", font_size=16, color=OK)
        lbl_low.move_to(ax.coords_to_point(3.0, 0.6 * 3.0)).shift(RIGHT * 0.15 + DOWN * 0.2)
        lbl_crit = Text("Rc (วิกฤต)", font_size=17, color=WARN)
        lbl_crit.move_to(ax.coords_to_point(2.5, 1.05 * 2.5)).shift(RIGHT * 0.2 + UP * 0.15)
        lbl_high = Text("R₂ (สูงเกิน)", font_size=16, color=EMF)
        lbl_high.move_to(ax.coords_to_point(1.5, 1.7 * 1.5)).shift(LEFT * 0.5 + UP * 0.15)

        self.play(Create(rf_low), FadeIn(lbl_low), run_time=0.6)
        self.play(Create(rf_crit), FadeIn(lbl_crit), run_time=0.6)
        self.play(Indicate(rf_crit, color=WARN, scale_factor=1.05), run_time=0.5)
        self.play(Create(rf_high), FadeIn(lbl_high), run_time=0.6)
        self.wait(0.5)

        self.play(FadeOut(cap0), run_time=0.3)
        cap1 = caption_top("Rf < Rc → เส้นตัดเคอร์ฟที่จุดสูง → แรงดันดี", color=OK)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(0.9)

        self.play(FadeOut(cap1), run_time=0.3)
        cap2 = caption_top("Rf > Rc → เส้นแทบไม่ตัดเคอร์ฟ → แรงดันตกเหลือแค่อำนาจตกค้าง!", color=EMF)
        self.play(FadeIn(cap2), run_time=0.5)
        self.play(Indicate(rf_high, color=EMF, scale_factor=1.1), run_time=0.6)
        self.wait(1.0)

        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = caption_top("ดังนั้น: รีโอสตาทตั้งสูงเกินไป = ตั้ง Rf เกินวิกฤต = เครื่องไม่สร้างแรงดัน", color=WARN)
        self.play(FadeIn(cap3), run_time=0.5)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-6: ความต้านทานวิกฤตคืออะไร?",
            "ค่า Rf ที่ทำให้เส้นความต้านทานฟิลด์สัมผัส (tangent) กับช่วงเส้นตรงของเคอร์ฟการอิ่มตัวพอดี")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP27 — 3 สาเหตุเครื่องไม่สร้างแรงเคลื่อน
# ================================================================
class EP27_WhyNoVoltage(SafeScene):
    """8-7 — 3 สาเหตุเครื่องไม่สร้างแรงเคลื่อน + flashing the field

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: กลไกจาก EP25/EP26 พังได้ 3 สาเหตุ
    t=2-6   สาเหตุ 1: ไม่มีอำนาจตกค้าง → flashing the field (เน้นวิธีแก้)
    t=6-10  สาเหตุ 2: ต่อฟิลด์กลับขั้ว → ลูปป้อนกลับเป็นลบ (วิธีแก้: สลับขั้ว)
    t=10-14 สาเหตุ 3: Rf > Rc (รีโอสตาทสูงเกิน หรือวงจรขาด)
    t=14-16 exam_card
    """

    def construct(self):
        ttl = title("EP27 — 3 สาเหตุเครื่องไม่สร้างแรงเคลื่อน", size=26)
        ref = page_ref("หน้า 13-14 · 8-7")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("กลไกป้อนกลับจาก EP25 พังได้ 3 สาเหตุ — แต่ละสาเหตุแก้ต่างกัน", color=WARN)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.7)

        # สาเหตุ 3 ข้อ
        causes = VGroup()
        data = [
            ("①", ไม่มีอำนาจแม่เหล็กตกค้าง,
             "ไม่มี เมล็ดพันธุ์ E₁ → ลูปไม่มีจุดเริ่ม",
             "แก้: Flashing the field — ต่อไฟตรงภายนอกเข้าวงจรฟิลด์ 2-3 วิ แล้วปลด",
             EMF),
            ("②", ต่อฟิลด์กลับขั้ว,
             "ฟลักซ์จาก If ไปหักล้างฟลักซ์ตกค้าง (ลูปป้อนกลับกลายเป็น ลบ)",
             "แก้: สลับขั้วต่อของขดลวดฟิลด์ใหม่",
             WARN),
            ("③", "Rf > ความต้านทานวิกฤต",
             "เส้น Rf ชันเกินจนไม่ตัดเคอร์ฟ — อาจเกิดจากรีโอสตาทสูงเกิน หรือวงจรขาด",
             "แก้: ลด Rf หรือ ตรวจสอบหาจุดขาด (คอมมิวเตเตอร์สกปรก?)",
             CURRENT),
        ]
        for num, head, body, fix, clr in data:
            n_t = Text(num, font_size=24, color=clr)
            h_t = Text(head, font_size=22, color=WHITE)
            b_t = Text(body, font_size=18, color=GRAYTXT)
            f_t = Text(fix, font_size=17, color=clr)
            fit_width(b_t, 10.5)
            fit_width(f_t, 10.5)
            row = VGroup(VGroup(n_t, h_t).arrange(RIGHT, buff=0.25),
                         b_t, f_t).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            causes.add(row)

        causes.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit_width(causes, 11.5)
        causes.move_to([0, -0.1, 0])

        self.play(FadeOut(cap0), run_time=0.3)

        for i, row in enumerate(causes):
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(1.0)

        self.wait(0.8)

        # เน้น flashing the field
        flash_box = SurroundingRectangle(causes[0][2], color=EMF, buff=0.08, stroke_width=2)
        self.play(Create(flash_box), run_time=0.5)
        cap_flash = caption_top("Flashing the field — วิธีฟื้นอำนาจตกค้าง: ต่อไฟ DC ภายนอกเข้าฟิลด์ชั่วคราว", color=EMF)
        self.play(FadeIn(cap_flash), run_time=0.5)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-7: ถ้าต่อขดลวดฟิลด์กลับขั้ว จะเกิดอะไร?",
            "ฟลักซ์จาก If ไปหักล้างฟลักซ์ตกค้าง → ลูปป้อนกลับบวกกลายเป็นลบ → เครื่องไม่สร้างแรงเคลื่อน")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP28 — ลักษณะสมบัติภายนอก (External Characteristic) + จุดเบรกดาวน์
# ================================================================
class EP28_ExternalCharacteristic(SafeScene):
    """8-8, 8-9 — 3 สาเหตุ Vt ตก + เคอร์ฟภายนอก + จุดเบรกดาวน์

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-3   caption + 3 สาเหตุ Vt ตก (Ia Ra, อาร์เมเจอร์รีแอคชัน, If ลดตาม Vt)
    t=3-6   เน้นสาเหตุ 3 ผลลูกโซ่ — Vt ลด → If ลด → E ลด → Vt ลดอีก
    t=6-9   วาดเคอร์ฟ Vt-IL + จุดเบรกดาวน์
    t=9-12  อธิบายจุดเบรกดาวน์: หลังจากนี้เพิ่มโหลดแล้วกระแสไม่เพิ่ม กลับลด
    t=12-14 exam_card
    """

    def construct(self):
        ttl = title("EP28 — เคอร์ฟภายนอก + จุดเบรกดาวน์", size=27)
        ref = page_ref("หน้า 13-17 · 8-8, 8-9 · รูปที่ 8-7")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("พอจ่ายโหลดจริง Vt ลดลงด้วย 3 สาเหตุพร้อมกัน", color=FIELD)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.5)

        # ---- 3 สาเหตุ ----
        causes = VGroup(
            VGroup(
                Text("①", font_size=22, color=CURRENT),
                Text("แรงดันตกที่อาร์เมเจอร์  Ia × Ra", font_size=21, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("②", font_size=22, color=WARN),
                Text("อาร์เมเจอร์รีแอคชัน — สนาม Ia หักล้างสนามขั้ว → E ลดด้วย", font_size=21, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("③", font_size=22, color=EMF),
                Text("Vt ลด → If = Vt/Rf ลดตาม → ฟลักซ์ลด → E ลดอีก  (ผลลูกโซ่)", font_size=21, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.6, 0])
        fit_width(causes, 11.5)

        self.play(FadeOut(cap0), run_time=0.3)
        for c in causes:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.5)

        # เน้นสาเหตุ 3
        box3 = SurroundingRectangle(causes[2], color=EMF, buff=0.1, stroke_width=2)
        cap1 = caption_top("สาเหตุ ③ คือ ผลลูกโซ่ทบต้น ที่คนชอบลืม — ทำ Vt ตกเร็วกว่าแค่ Ia Ra", color=EMF)
        self.play(Create(box3), run_time=0.5)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(causes), FadeOut(box3), FadeOut(cap1), run_time=0.5)

        # ---- เคอร์ฟ Vt-IL ----
        cap2 = caption_top("รวม 3 สาเหตุ → เคอร์ฟ Vt-IL (External Characteristic)", color=FIELD)
        self.play(FadeIn(cap2), run_time=0.5)

        ax2 = Axes(
            x_range=[0, 5, 1], y_range=[0, 3.0, 0.5],
            x_length=6.0, y_length=3.8,
            axis_config={"color": GRAYTXT, "stroke_width": 2,
                         "include_tip": True, "tip_length": 0.18},
        ).move_to([0.2, -0.4, 0])
        xl2 = Text("IL →", font_size=17, color=GRAYTXT)
        yl2 = Text("Vt (V)", font_size=17, color=GRAYTXT)
        xl2.next_to(ax2.x_axis.get_right(), RIGHT, buff=0.1)
        yl2.next_to(ax2.y_axis.get_top(), UP, buff=0.05)
        self.play(Create(ax2), FadeIn(xl2), FadeIn(yl2), run_time=0.8)

        # เส้น Vt-IL: ลดลง แล้ววกกลับ (จุดเบรกดาวน์ประมาณ IL=3.5)
        def vt_ext(x):
            if x < 3.5:
                return 2.6 - 0.28 * x - 0.05 * x ** 2
            else:
                # วกกลับหลังจุดเบรกดาวน์
                return vt_ext(3.5) - 0.7 * (x - 3.5) - 0.15 * (x - 3.5) ** 2

        ext_curve = ax2.plot(vt_ext, x_range=[0, 4.8, 0.05], color=FIELD, stroke_width=3)
        self.play(Create(ext_curve), run_time=1.0)

        # จุดเบรกดาวน์
        bd_pos = ax2.coords_to_point(3.5, vt_ext(3.5))
        bd_dot = Dot(bd_pos, color=EMF, radius=0.13)
        bd_lbl_txt = Text(จุดเบรกดาวน์, font_size=17, color=EMF)
        bd_lbl_txt.next_to(bd_dot, DR, buff=0.1)
        self.play(FadeIn(bd_dot), FadeIn(bd_lbl_txt), run_time=0.6)
        self.play(Indicate(bd_dot, color=WHITE, scale_factor=1.5), run_time=0.6)

        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = caption_top("หลังจุดเบรกดาวน์ — เพิ่มโหลดต่อ: กระแสไม่เพิ่มแล้ว ทั้ง Vt และ IL วกร่วงไปด้วยกัน", color=EMF)
        self.play(FadeIn(cap3), run_time=0.5)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-9: สาเหตุอะไรทำให้ Vt ตกมากกว่าแค่ Ia Ra เพียงอย่างเดียว?",
            "ผลลูกโซ่: Vt↓ → If↓ → E↓ → Vt↓ อีก  (สาเหตุที่ 3 เป็นผลทบต้น)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP29 — Voltage Regulation + ตัวอย่าง 8-3
# ================================================================
class EP29_VoltageRegulation(SafeScene):
    """8-10 + ตย.8-3 — %VR สูตรและตัวอย่างคำนวณ (8.7%)

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: %VR วัด ความนิ่ง ของแรงดัน — ยิ่งน้อยยิ่งดี
    t=2-4   Write สูตร %VR + อธิบาย VNL กับ VFL
    t=4-7   ตย.8-3: VFL=230V, VNL=250V → %VR = 8.7%
    t=7-9   เน้น: VFL = ค่าพิกัดบนป้ายเครื่อง ห้ามสลับตัวหาร
    t=9-11  exam_card
    """

    def construct(self):
        ttl = title("EP29 — Voltage Regulation (%VR)", size=27)
        ref = page_ref("หน้า 15-17 · 8-10 · ตย.8-3")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("%VR วัดว่าแรงดันขั้วนิ่งแค่ไหนเมื่อโหลดเปลี่ยน — ยิ่งน้อยยิ่งดี", color=OK)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.8)

        # สูตร
        eq_vr = MathTex(
            r"\%VR = \frac{V_{NL} - V_{FL}}{V_{FL}} \times 100",
            font_size=46, color=OK
        ).move_to([0, 1.0, 0])
        self.play(Write(eq_vr), run_time=1.0)

        note_nl = Text("VNL = แรงดันขณะไม่มีโหลด (ปลดโหลดออก)", font_size=19, color=GRAYTXT)
        note_fl = Text("VFL = แรงดันขณะโหลดพิกัด (ค่าบนป้ายเครื่อง)", font_size=19, color=CURRENT)
        notes = VGroup(note_nl, note_fl).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        notes.move_to([0, -0.5, 0])
        fit_width(notes, 11.5)
        self.play(FadeIn(notes), run_time=0.7)
        self.wait(0.5)

        # ตัวอย่าง 8-3
        self.play(FadeOut(cap0), run_time=0.3)
        cap1 = caption_top("ตย.8-3: เครื่อง 10kW, 230V — ปลดโหลดแล้ว Vt ขึ้นเป็น 250V", color=EMF)
        self.play(FadeIn(cap1), run_time=0.5)
        self.play(
            eq_vr.animate.scale(0.7).to_corner(UR, buff=0.5),
            notes.animate.scale(0.75).to_corner(UL, buff=0.5).shift(DOWN * 0.2),
            run_time=0.8
        )

        ex = VGroup(
            MathTex(r"V_{FL} = 230\ \text{V},\quad V_{NL} = 250\ \text{V}", font_size=30, color=WHITE),
            MathTex(r"\%VR = \frac{250 - 230}{230} \times 100 = \mathbf{8.7\%}",
                    font_size=38, color=OK),
        ).arrange(DOWN, buff=0.45).move_to([0, 0.3, 0])
        self.play(FadeIn(ex[0], shift=RIGHT * 0.2), run_time=0.7)
        self.wait(0.4)
        self.play(FadeIn(ex[1], scale=1.15), run_time=0.9)
        self.wait(0.8)

        # คำเตือนตัวหาร
        self.play(FadeOut(cap1), run_time=0.3)
        warn_txt = Text("⚠️  ตัวหาร = VFL เสมอ  ห้ามสลับกับ VNL", font_size=22, color=EMF)
        warn_txt.move_to([0, -1.6, 0])
        self.play(FadeIn(warn_txt), run_time=0.5)
        self.play(Indicate(warn_txt, color=EMF, scale_factor=1.05), run_time=0.5)
        self.wait(1.0)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-10: VR คืออะไร และยิ่งน้อยหมายความว่าอะไร?",
            "VR = % ที่แรงดันเพี้ยนไปจาก VFL — ยิ่งน้อยยิ่งดี = แรงดันนิ่ง ไม่ขึ้นลงตามโหลด")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP30 — Cumulative Compound + Short-shunt vs Long-shunt + ตย.8-4
# ================================================================
class EP30_CumulativeCompound(SafeScene):
    """8-11 + ตย.8-4 — cumulative compound, short vs long shunt, %VR = -12%

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-3   caption: เซรี่ฟิลด์ช่วยชดเชย Vt ตก
    t=3-6   ตารางเปรียบ short-shunt vs long-shunt (สูตร Vt, Is)
    t=6-9   ตย.8-4: คำนวณ R สาย, ΔV, Vt ที่ขั้ว → VR = -12%
    t=9-12  อธิบาย %VR ติดลบ: Vt ที่ขั้วต้องสูงกว่าตอนไม่โหลด (ชดเชยสาย)
    t=12-14 exam_card
    """

    def construct(self):
        ttl = title("EP30 — Cumulative Compound Generator", size=26)
        ref = page_ref("หน้า 18-22 · 8-11 · ตย.8-4")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("เซรี่ฟิลด์ต่อร่วม — ฟลักซ์เสริมชันท์ฟิลด์ ช่วยชดเชย Vt ที่กำลังจะตก", color=CURRENT)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.7)

        # ---- ตารางเปรียบ ----
        self.play(FadeOut(cap0), run_time=0.3)
        cap1 = caption_top("ต่อได้ 2 แบบ — ตำแหน่งชันท์ฟิลด์ต่างกัน → สูตรกระแสต่างกัน", color=FIELD)
        self.play(FadeIn(cap1), run_time=0.5)

        tbl_header = ["", "Short-shunt", "Long-shunt"]
        tbl_rows = [
            (ชันท์ฟิลด์คร่อม, อาร์เมเจอร์อย่างเดียว, "ขั้วเอาต์พุต (รวมเซรี่ฟิลด์)"),
            ("Is  (กระแสเซรี่)", "= IL (กระแสโหลด)", "= Ia (กระแสอาร์เมเจอร์)"),
            ("สูตร Vt", "E - Ia Ra - IL Rs", "E - Ia Ra - Ia Rs  = E - Ia(Ra+Rs)"),
        ]
        all_cells = VGroup()
        for cell in tbl_header:
            t = Text(cell, font_size=19, color=GRAYTXT)
            all_cells.add(t)
        for row in tbl_rows:
            for j, cell in enumerate(row):
                clr = WHITE if j > 0 else GRAYTXT
                t = Text(cell, font_size=17 if j > 0 else 18, color=clr)
                fit_width(t, 4.2)
                all_cells.add(t)
        grid = all_cells.arrange_in_grid(rows=4, cols=3, buff=(0.55, 0.28))
        fit_width(grid, 12.0)
        grid.move_to([0, 0.3, 0])
        self.play(FadeIn(grid), run_time=1.0)
        self.wait(1.2)

        # ---- ตัวอย่าง 8-4 ----
        self.play(FadeOut(cap1), FadeOut(grid), run_time=0.5)
        cap2 = caption_top("ตย.8-4: โหลด 220V/200A ห่าง 990 ม. สาย 500MCM (R=0.025Ω/330m)", color=EMF)
        self.play(FadeIn(cap2), run_time=0.5)

        ex_steps = VGroup(
            MathTex(r"R_{line}=\frac{0.025}{330}\times990\times2=0.15\ \Omega", font_size=27, color=WHITE),
            MathTex(r"\Delta V = 200\times0.15 = 30\ \text{V}", font_size=27, color=CURRENT),
            MathTex(r"V_t(\text{FL}) = 220+30 = 250\ \text{V}", font_size=27, color=OK),
            MathTex(r"V_t(\text{NL}) = 220\ \text{V}\quad (\text{ไม่มีโหลด})", font_size=27, color=GRAYTXT),
            MathTex(r"\%VR = \frac{220-250}{250}\times100 = \mathbf{-12\%}", font_size=34, color=EMF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, 0.2, 0])
        fit_width(ex_steps, 11.0)

        for s in ex_steps:
            self.play(FadeIn(s, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.4)
        self.wait(0.5)

        self.play(FadeOut(cap2), run_time=0.3)
        cap3 = caption_top("VR ติดลบ! เพราะ Vt ที่ขั้วตอน FL (=250V) > ตอน NL (=220V) — ชดเชยสายส่ง", color=EMF)
        self.play(FadeIn(cap3), run_time=0.5)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-11: Short-shunt กับ Long-shunt ต่างกันที่ Is ตัวไหน?",
            "Short-shunt: Is = IL  |  Long-shunt: Is = Ia  (สำคัญ! กระทบลำดับคำนวณทั้งหมด)")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP31 — Differential Compound
# ================================================================
class EP31_DifferentialCompound(SafeScene):
    """8-12 — differential compound: ฟลักซ์หักล้าง, ใช้งานเชื่อม/ชุบโลหะ

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: แค่สลับขั้วต่อเซรี่ฟิลด์ → ฟลักซ์หักล้างแทนที่จะเสริม
    t=2-5   แผนผัง: เส้น Vt-IL ของ differential วกโค้งลงแรงกว่าแบบขนาน
    t=5-8   อธิบายพฤติกรรม: Vt ตกเร็ว แต่ IL คงที่ค่อนข้างดี
    t=8-11  ใช้งาน: งานเชื่อมไฟฟ้า, งานชุบโลหะ (กระแสคงที่สำคัญกว่าแรงดัน)
    t=11-13 exam_card
    """

    def construct(self):
        ttl = title("EP31 — Differential Compound Generator", size=26)
        ref = page_ref("หน้า 19-22 · 8-12 · รูปที่ 8-9")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("สลับขั้วต่อเซรี่ฟิลด์ → ฟลักซ์หักล้างชันท์ฟิลด์แทนที่จะเสริม", color=WARN)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.8)

        # ---- กราฟ Vt-IL เปรียบเทียบ 3 เส้น ----
        ax = Axes(
            x_range=[0, 5, 1], y_range=[0, 3.0, 0.5],
            x_length=5.8, y_length=3.8,
            axis_config={"color": GRAYTXT, "stroke_width": 2,
                         "include_tip": True, "tip_length": 0.18},
        ).move_to([-0.5, -0.4, 0])
        xl = Text("IL →", font_size=17, color=GRAYTXT).next_to(ax.x_axis.get_right(), RIGHT, buff=0.1)
        yl = Text("Vt", font_size=17, color=GRAYTXT).next_to(ax.y_axis.get_top(), UP, buff=0.05)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)

        # เส้น cumulative (ราบเกือบคงที่ หรือขึ้นเล็กน้อย)
        def vt_cumul(x):
            return 2.5 - 0.05 * x - 0.02 * x ** 2

        # เส้น shunt (ลดลงปานกลาง)
        def vt_shunt(x):
            return 2.5 - 0.25 * x - 0.04 * x ** 2

        # เส้น differential (ลงแรง)
        def vt_diff(x):
            return 2.5 - 0.55 * x - 0.06 * x ** 2 if x < 4.5 else 0.1

        c_cum = ax.plot(vt_cumul, x_range=[0, 4.8, 0.05], color=OK, stroke_width=2.5)
        c_shunt = ax.plot(vt_shunt, x_range=[0, 4.8, 0.05], color=FIELD, stroke_width=2.5)
        c_diff = ax.plot(vt_diff, x_range=[0, 4.5, 0.05], color=EMF, stroke_width=3)

        lbl_cum = Text("Cumulative (เสริม)", font_size=16, color=OK)
        lbl_cum.move_to(ax.coords_to_point(3.5, vt_cumul(3.5))).shift(RIGHT * 0.8)
        lbl_shunt = Text("Shunt (ขนาน)", font_size=16, color=FIELD)
        lbl_shunt.move_to(ax.coords_to_point(3.5, vt_shunt(3.5))).shift(RIGHT * 0.7)
        lbl_diff = Text("Differential (หักล้าง)", font_size=16, color=EMF)
        lbl_diff.move_to(ax.coords_to_point(2.5, vt_diff(2.5))).shift(RIGHT * 0.9 + DOWN * 0.15)

        self.play(FadeOut(cap0), run_time=0.3)
        self.play(Create(c_cum), FadeIn(lbl_cum), run_time=0.6)
        self.play(Create(c_shunt), FadeIn(lbl_shunt), run_time=0.6)
        self.play(Create(c_diff), FadeIn(lbl_diff), run_time=0.7)
        self.wait(0.5)

        cap1 = caption_top("Differential: Vt ร่วงเร็วที่สุด แต่ IL คงที่กว่า — กระแสสม่ำเสมอ", color=EMF)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(1.0)

        # ---- งานเฉพาะทาง ----
        self.play(FadeOut(cap1), run_time=0.3)
        use_cases = VGroup(
            VGroup(
                Text("งานเชื่อมไฟฟ้า (Arc Welding)", font_size=22, color=WHITE),
                Text("  — กระแสเกือบคงที่ตลอด แม้ระยะห่างขั้วจะเปลี่ยน", font_size=19, color=GRAYTXT),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("งานชุบโลหะ (Electroplating)", font_size=22, color=WHITE),
                Text("  — กระแสต้องนิ่งเพื่อให้ชั้นโลหะสม่ำเสมอ", font_size=19, color=GRAYTXT),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, 1.0, 0])
        fit_width(use_cases, 5.5)

        cap2 = caption_top("ใช้ในงานที่ต้องการ กระแสคงที่ มากกว่า แรงดันคงที่", color=FIELD)
        self.play(FadeIn(cap2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.2) for u in use_cases],
                              lag_ratio=0.3), run_time=1.0)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-12: Differential compound ใช้งานอะไรเป็นหลัก?",
            "งานเชื่อมไฟฟ้า และ งานชุบโลหะ — เพราะกระแสค่อนข้างคงที่แม้แรงดันจะเปลี่ยน")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP32 — ระดับการผสม + ไดเวอร์เตอร์ + ตย.8-7
# ================================================================
class EP32_DegreesOfCompounding(SafeScene):
    """8-13 + ตย.8-7 — over/flat/under compound, diverter, Rd = 0.0164 Ω

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-3   ตาราง: over/flat/under compound + ใช้งาน
    t=3-6   อธิบายไดเวอร์เตอร์: ต่อขนาน Ns ปรับกระแสเซรี่ฟิลด์
    t=6-10  ตย.8-7: สมดุลแอมป์-เทอร์น → Is=115A → Rd=0.0164Ω
    t=10-12 exam_card
    """

    def construct(self):
        ttl = title("EP32 — ระดับการผสม + ไดเวอร์เตอร์", size=27)
        ref = page_ref("หน้า 22-27 · 8-13 · ตย.8-7")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("Cumulative compound แบ่งย่อยได้ 3 ระดับ ตาม VFL เทียบ VNL", color=FIELD)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.6)

        # ตาราง 3 ระดับ
        tbl_cells = VGroup()
        headers = [ชนิด, "VFL เทียบ VNL", ใช้ทำอะไร]
        rows_data = [
            ("Over compound", "VFL > VNL  (V เพิ่มตามโหลด!)", "ส่งกำลังระยะไกล — ชดเชยแรงดันตกในสาย"),
            ("Flat compound", "VFL = VNL  (V คงที่เป๊ะ)", งานที่ต้องการแรงดันคงที่จริงจัง),
            ("Under compound", "VFL < VNL  (แต่ยังสูงกว่าแบบขนาน)", "กลางๆ ระหว่างสองแบบบน"),
        ]
        colors_row = [OK, FIELD, CURRENT]
        for h in headers:
            tbl_cells.add(Text(h, font_size=19, color=GRAYTXT))
        for (n, comp, use), clr in zip(rows_data, colors_row):
            t_n = Text(n, font_size=18, color=clr)
            t_c = Text(comp, font_size=17, color=WHITE)
            t_u = Text(use, font_size=16, color=GRAYTXT)
            fit_width(t_u, 4.5)
            tbl_cells.add(t_n, t_c, t_u)
        grid = tbl_cells.arrange_in_grid(rows=4, cols=3, buff=(0.55, 0.25))
        fit_width(grid, 12.5)
        grid.move_to([0, 0.7, 0])

        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(grid), run_time=0.9)
        self.wait(1.0)

        # ไดเวอร์เตอร์
        cap1 = caption_top("ปรับระดับ: ต่อไดเวอร์เตอร์ (Rd) ขนานกับเซรี่ฟิลด์ → ลดกระแสผ่านเซรี่ฟิลด์", color=CURRENT)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(0.8)

        # ตัวอย่าง 8-7
        self.play(FadeOut(cap1), FadeOut(grid), run_time=0.4)
        cap2 = caption_top("ตย.8-7: หา Rd ที่ทำให้ได้ระดับการผสมที่ต้องการ", color=EMF)
        self.play(FadeIn(cap2), run_time=0.5)

        ex = VGroup(
            Text("โจทย์: Nf=500 รอบ/ขั้ว, Ns=10 รอบ/ขั้ว, Rs=0.005Ω,", font_size=19, color=GRAYTXT),
            Text("If1=2.7A (NL), If2=5A (FL), IL=150A", font_size=19, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 1.2, 0])
        fit_width(ex, 12.0)
        self.play(FadeIn(ex), run_time=0.6)

        calc = VGroup(
            MathTex(r"N_f(I_{f2}-I_{f1}) = N_s I_s \implies 500(5-2.7)=10\,I_s",
                    font_size=26, color=WHITE),
            MathTex(r"I_s = \frac{500\times2.3}{10} = \mathbf{115\ \text{A}}",
                    font_size=30, color=CURRENT),
            MathTex(r"I_d = 150 - 115 = 35\ \text{A}", font_size=28, color=GRAYTXT),
            MathTex(r"R_d = \frac{I_s R_s}{I_d} = \frac{115\times0.005}{35} = \mathbf{0.0164\ \Omega}",
                    font_size=30, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.7, 0])
        fit_width(calc, 11.5)

        for c in calc:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.4)
        self.wait(0.8)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-13: ไดเวอร์เตอร์ทำงานอย่างไร?",
            "ต่อขนานกับเซรี่ฟิลด์ — กระแสบางส่วนเบี่ยงไปทาง Rd ทำให้ Is ผ่านเซรี่ฟิลด์น้อยลง → ฟลักซ์เสริมน้อยลง")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)


# ================================================================
# EP33 — Series Generator (เครื่องกำเนิดแบบอนุกรม)
# ================================================================
class EP33_SeriesGenerator(SafeScene):
    """8-14 — เครื่องกำเนิดแบบอนุกรม + series booster

    beat-by-beat:
    t=0-1   FadeIn title + ref
    t=1-2   caption: ไม่มีชันท์ฟิลด์เลย — กระแสฟิลด์ = กระแสโหลด
    t=2-5   อธิบายพฤติกรรม: NL ต่ำ → โหลดขึ้น E ขึ้น → อิ่มตัวแล้วกลับลง
    t=5-8   วาดเคอร์ฟ Vt-IL (โค้งขึ้นแล้วลง) + อธิบายแต่ละช่วง
    t=8-11  series booster: ต่อแบบ series เพื่อชดเชยแรงดันตกในสายส่งระยะไกล
    t=11-13 exam_card
    """

    def construct(self):
        ttl = title("EP33 — เครื่องกำเนิดแบบอนุกรม (Series Generator)", size=24)
        ref = page_ref("หน้า 28-29 · 8-14 · รูปที่ 8-14")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.7)

        cap0 = caption_top("ไม่มีชันท์ฟิลด์เลย — กระแสฟิลด์ = กระแสโหลดทั้งหมด", color=CURRENT)
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(0.8)

        # อธิบายพฤติกรรมทีละขั้น
        behaviors = VGroup(
            VGroup(
                Text("ไม่มีโหลด:", font_size=20, color=GRAYTXT),
                Text("กระแสฟิลด์ = 0 → Vt เหลือแค่อำนาจตกค้าง (น้อยมาก)", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("เริ่มมีโหลด:", font_size=20, color=CURRENT),
                Text("IL ไหลผ่านฟิลด์โดยตรง → ฟลักซ์เพิ่ม → E เพิ่ม → Vt เพิ่ม", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("โหลดมากขึ้น:", font_size=20, color=WARN),
                Text("แกนอิ่มตัว + Ia Ra + อาร์เมเจอร์รีแอคชัน ชนะ → เคอร์ฟวกกลับลง", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.9, 0])
        fit_width(behaviors, 12.0)

        self.play(FadeOut(cap0), run_time=0.3)
        for b in behaviors:
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.5)
        self.wait(0.5)

        # เคอร์ฟ Vt-IL
        self.play(behaviors.animate.scale(0.7).to_edge(LEFT, buff=0.5).shift(UP * 0.8), run_time=0.8)

        ax = Axes(
            x_range=[0, 5, 1], y_range=[0, 3.0, 0.5],
            x_length=5.2, y_length=3.5,
            axis_config={"color": GRAYTXT, "stroke_width": 2,
                         "include_tip": True, "tip_length": 0.18},
        ).move_to([3.0, -0.2, 0])
        xl = Text("IL →", font_size=16, color=GRAYTXT).next_to(ax.x_axis.get_right(), RIGHT, buff=0.08)
        yl = Text("Vt", font_size=16, color=GRAYTXT).next_to(ax.y_axis.get_top(), UP, buff=0.04)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.7)

        def vt_series(x):
            if x < 2.5:
                return 0.05 + 1.2 * x - 0.15 * x ** 2
            else:
                peak = 0.05 + 1.2 * 2.5 - 0.15 * 2.5 ** 2
                return peak - 0.7 * (x - 2.5) - 0.15 * (x - 2.5) ** 2

        c_series = ax.plot(vt_series, x_range=[0, 4.8, 0.05], color=CURRENT, stroke_width=3)
        self.play(Create(c_series), run_time=0.9)

        peak_pos = ax.coords_to_point(2.5, vt_series(2.5))
        peak_dot = Dot(peak_pos, color=WARN, radius=0.12)
        peak_lbl = Text("ค่าสูงสุด\n(จากนั้นลง)", font_size=16, color=WARN, line_spacing=0.9)
        peak_lbl.next_to(peak_dot, UR, buff=0.1)
        self.play(FadeIn(peak_dot), FadeIn(peak_lbl), run_time=0.5)
        self.wait(0.7)

        # Series booster
        cap1 = caption_top("ประยุกต์ใช้: Series Booster — ต่ออนุกรมในสายส่งเพื่อชดเชยแรงดันตกระยะไกล", color=OK)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(1.2)

        self.fade_out_all(run_time=0.6)
        card = exam_card(
            "จุดออกสอบ 8-14: ทำไมเครื่องกำเนิดแบบอนุกรมแทบไม่ใช้จ่ายกำลังทั่วไป?",
            "เพราะแรงดันขั้วขึ้นกับโหลดมาก ควบคุมไม่ได้ — ใช้ได้เฉพาะงาน series booster ในสายส่ง DC")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)
