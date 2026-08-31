"""EPS บทที่ 6 — ชุดวิดีโอสอนทั้งบท (ระนาบเป็นกลาง · อาร์เมเจอร์รีแอคชั่น · คอมมิวเตชั่น)

สร้างตามคำขอของ Min (2026-08-31): ดูทั้งบทก่อนแล้วค่อยแตกเป็นซีนย่อย เรียงตาม
เนื้อหาไฟล์ "บทที่ 6 ปี3.pdf" หน้า 1-14 ตรงตามลำดับหนังสือ

กติกาการนำเสนอที่ Min กำหนดไว้ (ต่างจากคลิปชุดก่อน):
  * ข้อความทั้งหมดอยู่ "โซนบน" (caption_top) ไม่ใช่ล่าง — แถบควบคุมของโปรแกรม
    เล่นวิดีโอบังข้อความล่างเสมอ ครึ่งล่างของเฟรมปล่อยว่างให้ภาพ
  * ป้ายอ้างอิงหน้า/รูปในหนังสือ (page_ref) มุมขวาบนทุกช่วง เทียบกับสไลด์จริงได้
  * สร้างเป็น 3D จริงตั้งแต่ต้น แต่เปิดฉากด้วยกล้องมองตรงระนาบเดียวจนดูเหมือน 2D
    แล้วค่อย "หมุนกล้องเผยมิติ" — เปลี่ยนฉากด้วยการเลื่อน/หมุน ไม่ใช่ตัดคลิป
  * เปิดเรื่องด้วยแผนที่ทั้งบท กันหลงทางเพราะเนื้อหายาว
  * ปิดท้ายแต่ละช่วงด้วยคำถามข้อสอบจริงของบท (6-1 ถึง 6-15)

ลำดับซีน (เรนเดอร์ขนานได้ ไม่ผูกกัน):
  S1  หน้า 1-2   กายวิภาค: อาร์เมเจอร์/คอมมิวเตเตอร์/แปรงถ่าน ต่อกันยังไง  [3D reveal]
  S2  หน้า 1-2   ระนาบเป็นกลางคืออะไร ทำไมแปรงถ่านต้องอยู่ตรงนั้น         [3D]
  S3  หน้า 3-4   สนาม 2 สนามบวกกัน -> สนามหลักเบี่ยง (รูป 6-2 ก/ข/ค)      [3D]
  S4  หน้า 5-7   แยกผลเสีย BB (แรงดันตก) กับ AA (สปาร์ค) (รูป 6-3)        [3D]
  S5  หน้า 7-8   คอมมิวเตชั่น: ส่งไม้ผลัดกระแส 100 A (รูป 6-4)             [2D]
  S6  หน้า 9-10  การเหนี่ยวนำในตัวเอง -> ระนาบเลื่อนซ้ำ (รูป 6-5, 6-6)      [2D]
  S7  หน้า 11-12 ขั้วแม่เหล็กเสริม interpole (รูป 6-7)                     [3D]
  S8  หน้า 13-14 ชุดขดลวดชดเชย + ตารางเทียบ + สรุป (รูป 6-8)               [2D]

สีประจำปริมาณ (Mayer signaling — ห้ามสลับข้ามซีน):
  FIELD   ฟ้า      สนามแม่เหล็กหลัก
  CURRENT เหลือง   กระแส / สนามที่เกิดจากกระแสอาร์เมเจอร์
  WARN    ส้ม      ตำแหน่งใหม่ของระนาบ / ปัญหา
  EMF     แดง      แรงเคลื่อนเหนี่ยวนำ / สปาร์ค
  OK      ฟ้าเขียว ข้อสรุป / ตัวแก้ปัญหา
  METAL   เทา      โครงสร้างโลหะ
"""

import numpy as np
from manim import *
from mlib import *

# ---------------------------------------------------------------- geometry
R_ARM = 1.45          # รัศมีอาร์เมเจอร์
L_HALF = 1.05         # ครึ่งความยาวแกนอาร์เมเจอร์ (ตามแกน z = แกนหมุน)
POLE_X = 3.30         # ระยะขั้วหลักจากศูนย์กลาง
POLE_W = 1.30         # ความหนาแท่งขั้ว (แนว x)
POLE_H = 2.60         # ความสูงหน้าขั้ว (แนว y)
N_SLOT = 12           # จำนวนตัวนำรอบวง
R_COMM = 0.60         # รัศมีคอมมิวเตเตอร์
COMM_Z = L_HALF + 0.55

STAGE = np.array([0.0, -0.45, 0.0])   # ศูนย์กลางเวที (เยื้องลงเพราะข้อความอยู่บน)

EXAMC = "#FFD54F"     # สีป้าย "จุดออกสอบ"


# ---------------------------------------------------------------- ชิ้นส่วนร่วม
def conductor_mark(pos, out_of_page, r=0.115, color=CURRENT):
    """สัญลักษณ์ตัวนำบนหน้าตัด: ⊙ = กระแสพุ่งออก, ⊗ = กระแสพุ่งเข้า"""
    body = Circle(radius=r, color=color, fill_color=BLACK,
                  fill_opacity=1.0, stroke_width=2.4).move_to(pos)
    if out_of_page:
        mark = Dot(pos, radius=r * 0.34, color=color)
    else:
        d = r * 0.58
        mark = VGroup(
            Line(pos + [-d, -d, 0], pos + [d, d, 0], color=color, stroke_width=2.2),
            Line(pos + [-d, d, 0], pos + [d, -d, 0], color=color, stroke_width=2.2),
        )
    return VGroup(body, mark)


def slot_angles(n=N_SLOT):
    """มุมของตัวนำรอบวง — เว้นให้สมมาตรกับแกนตั้ง (แนวแปรงถ่าน)"""
    return [PI / 2 + (i + 0.5) * TAU / n for i in range(n)]


def face_marks(n=N_SLOT, z=L_HALF, brush_angle=0.0, center=STAGE):
    """⊙/⊗ บนหน้าตัดด้านหน้า — แบ่งซีกซ้าย/ขวาของ 'แนวแปรงถ่าน' (ไม่ใช่บน/ล่าง)

    brush_angle = มุมเอียงของแนวแปรงถ่าน (0 = แนวตั้ง) กระแสกลับทิศตรงแนวนี้
    เพราะคอมมิวเตเตอร์สลับซี่ตรงนั้นพอดี (โยงกับ S1)

    เดิม axis ใช้ทิศ "ตามแนวแปรงถ่าน" เอง (แบ่งบน/ล่าง) — เทียบกับรูปที่ 6-2(ข)
    ในหนังสือแล้วผิด หนังสือแบ่งซ้าย/ขวาของเส้นแปรงถ่าน (⊗ ทั้งซีกซ้าย ⊙ ทั้งซีกขวา
    ตอนแปรงถ่านแนวตั้ง) ต้องใช้ axis ที่ตั้งฉากกับแนวแปรงถ่านแทน (พบ 2026-08-31
    ตอน Min ถามเรื่องสนามแต่ละขดลวดตอนหมุน — S9 ใช้สูตรถูกอยู่แล้ว จุดนี้ผิดจุดเดียว)
    """
    g = VGroup()
    axis = np.array([np.cos(brush_angle), np.sin(brush_angle), 0.0])
    for a in slot_angles(n):
        p = center + R_ARM * np.array([np.cos(a), np.sin(a), 0]) + np.array([0, 0, z])
        out = float(np.dot(np.array([np.cos(a), np.sin(a), 0.0]), axis)) > 0
        g.add(conductor_mark(p, out))
    return g


def armature_cage(n=N_SLOT, center=STAGE):
    """โครงลวดอาร์เมเจอร์ 3 มิติ: หน้าตัดหน้า-หลัง + แท่งตัวนำตามแนวแกน"""
    front = Circle(radius=R_ARM, color=METAL, stroke_width=3)
    front.move_to(center + np.array([0, 0, L_HALF]))
    back = Circle(radius=R_ARM, color=METAL, stroke_width=2)
    back.move_to(center + np.array([0, 0, -L_HALF]))
    back.set_stroke(opacity=0.45)

    bars = VGroup()
    for a in slot_angles(n):
        u = np.array([np.cos(a), np.sin(a), 0.0])
        bars.add(line3(center + R_ARM * u + np.array([0, 0, -L_HALF]),
                       center + R_ARM * u + np.array([0, 0, L_HALF]),
                       CURRENT, thickness=0.016))
    return front, back, bars


def shaft(center=STAGE, extra=1.15):
    return line3(center + np.array([0, 0, -L_HALF - extra]),
                 center + np.array([0, 0, COMM_Z + 0.45]),
                 GRAYTXT, thickness=0.020)


def commutator(n_seg=8, center=STAGE):
    """คอมมิวเตเตอร์: วงแหวนซี่ทองแดงที่ปลายเพลาด้านหน้า (หมุนไปกับอาร์เมเจอร์)"""
    z0, z1 = COMM_Z - 0.28, COMM_Z + 0.28
    ring_f = Circle(radius=R_COMM, color=CURRENT, stroke_width=3)
    ring_f.move_to(center + np.array([0, 0, z1]))
    ring_b = Circle(radius=R_COMM, color=CURRENT, stroke_width=2)
    ring_b.move_to(center + np.array([0, 0, z0]))
    ring_b.set_stroke(opacity=0.5)
    segs = VGroup()
    for i in range(n_seg):
        a = PI / 2 + i * TAU / n_seg
        u = np.array([np.cos(a), np.sin(a), 0.0])
        segs.add(line3(center + R_COMM * u + np.array([0, 0, z0]),
                       center + R_COMM * u + np.array([0, 0, z1]),
                       CURRENT, thickness=0.013))
    return VGroup(ring_b, segs, ring_f)


def brush_pair(center=STAGE, color=WARN):
    """แปรงถ่าน + และ − แตะผิวคอมมิวเตเตอร์ (อยู่กับที่ ไม่หมุน)"""
    g = VGroup()
    for sgn in (+1, -1):
        b = Rectangle(width=0.34, height=0.30, color=color,
                      fill_color=color, fill_opacity=0.95, stroke_width=0)
        b.move_to(center + np.array([0, sgn * (R_COMM + 0.17), COMM_Z]))
        g.add(b)
    return g


def pole_piece(x_sign, letter, center=STAGE, color=METAL, opacity=0.30):
    """แท่งขั้วแม่เหล็กหลัก — โครงลวดกล่อง 3 มิติ + หน้าขั้วโปร่งแสง"""
    cx = center[0] + x_sign * (POLE_X - POLE_W / 2)
    cy = center[1]

    def face(z):
        r = Rectangle(width=POLE_W, height=POLE_H, color=color, stroke_width=2.5,
                      fill_color=color, fill_opacity=opacity if z > 0 else 0.0)
        r.move_to([cx, cy, z])
        return r

    f, b = face(L_HALF), face(-L_HALF)
    b.set_stroke(opacity=0.45)
    edges = VGroup()
    for dx in (-POLE_W / 2, POLE_W / 2):
        for dy in (-POLE_H / 2, POLE_H / 2):
            edges.add(line3([cx + dx, cy + dy, -L_HALF], [cx + dx, cy + dy, L_HALF],
                            color, thickness=0.012))
    return VGroup(b, edges, f)


def main_field(tilt=0.0, center=STAGE, n=5, color=FIELD, opacity=0.9, z=0.0):
    """เส้นแรงสนามหลัก N -> S (เอียงได้ตามมุมที่ให้)"""
    g = VGroup()
    for k in range(n):
        y = (k - (n - 1) / 2) * 0.60
        a = center + np.array([-POLE_X + POLE_W + 0.05, y, z])
        b = center + np.array([POLE_X - POLE_W - 0.05, y, z])
        arr = Arrow(a, b, buff=0, color=color, stroke_width=3.4,
                    tip_length=0.20, max_tip_length_to_length_ratio=0.5)
        arr.set_opacity(opacity)
        g.add(arr)
    if tilt:
        g.rotate(tilt, about_point=center)
    return g


def plane_line(angle, color, length=2.55, width=5, center=STAGE, dashed=False):
    """เส้นระนาบเป็นกลาง (ตั้งฉากกับสนาม)"""
    v = np.array([-np.sin(angle), np.cos(angle), 0.0])
    if dashed:
        return DashedLine(center - v * length, center + v * length,
                          color=color, stroke_width=width, dash_length=0.14)
    return Line(center - v * length, center + v * length,
                color=color, stroke_width=width)


def exam_card(q, a, y=0.35):
    """การ์ด 'จุดออกสอบ' — คำถามจริงจากท้ายบท + คำตอบย่อ"""
    head = Text("จุดออกสอบ", font_size=20, color=EXAMC)
    qq = Text(q, font_size=23, color=WHITE)
    fit_width(qq, 11.5)
    aa = Text(a, font_size=21, color=OK)
    fit_width(aa, 11.5)
    card = VGroup(head, qq, aa).arrange(DOWN, buff=0.32)
    card.move_to([0, y, 0])
    return card


# ================================================================ S1
class S1_Anatomy(SafeThreeDScene):
    """หน้า 1-2 · กายวิภาค: อะไรคืออาร์เมเจอร์/คอมมิวเตเตอร์ ต่อกันยังไง"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        # ---------- A. แผนที่ทั้งบท ----------
        ttl = self.hud(title("บทที่ 6 — เราจะเดินทางไปทางไหน", size=29))
        self.play(FadeIn(ttl, shift=DOWN * 0.15), run_time=0.9)

        steps = [
            ("1", "ระนาบเป็นกลางคืออะไร", "หน้า 1-2"),
            ("2", "สนาม 2 สนามบวกกัน → สนามเบี่ยง", "หน้า 3-4"),
            ("3", "ผลเสีย: แรงดันตก / สปาร์ค", "หน้า 5-7"),
            ("4", "คอมมิวเตชั่น + เหนี่ยวนำในตัวเอง", "หน้า 7-10"),
            ("5", "ตัวแก้: interpole / ขดลวดชดเชย", "หน้า 11-14"),
        ]
        rows = VGroup()
        for num, name, pg in steps:
            n = Text(num, font_size=22, color=OK)
            t = Text(name, font_size=23, color=GRAYTXT)
            p = Text(pg, font_size=18, color="#607D8B")
            row = VGroup(n, t, p).arrange(RIGHT, buff=0.34)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.40)
        fit_width(rows, 9.5)
        rows.move_to([0, -0.35, 0])
        self.hud(rows)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in rows],
                              lag_ratio=0.22), run_time=2.4)
        self.wait(1.4)
        self.play(FadeOut(rows), FadeOut(ttl), run_time=0.7)

        # ---------- B. มองตรงหน้าตัด (ดูเหมือน 2D) ----------
        ttl2 = self.hud(title("ก่อนอื่น — เครื่องนี้ประกอบด้วยอะไรบ้าง", size=29))
        ref = self.hud(page_ref("หน้า 1-2 · 6-1, 6-2"))
        cap = self.hud(caption_top("ภาพตัดขวางแบบในหนังสือ — มองจากด้านหน้าตรงๆ"))
        self.play(FadeIn(ttl2), FadeIn(ref), FadeIn(cap), run_time=0.8)

        n_pole = pole_piece(-1, "N")
        s_pole = pole_piece(+1, "S")
        n_lab = self.hud(Text("N", font_size=34, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0]))
        s_lab = self.hud(Text("S", font_size=34, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0]))

        front, back, bars = armature_cage()
        marks = face_marks()

        self.play(FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab), FadeIn(s_lab),
                  run_time=0.9)
        self.play(Create(front), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.05),
                  run_time=1.2)
        self.wait(0.8)

        cap2 = self.hud(caption_top("⊙ = กระแสพุ่งออกจากจอ · ⊗ = กระแสพุ่งเข้าจอ"))
        self.play(FadeOut(cap), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.6)
        self.wait(1.2)

        # ---------- C. หมุนกล้องเผยว่าจริงๆ เป็น 3 มิติ ----------
        cap3 = self.hud(caption_top(
            "แต่ ⊙/⊗ ไม่ใช่จุด — มันคือ \"แท่งตัวนำ\" ที่ยาวเข้าไปในกระดาษ", color=OK))
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)

        # ป้าย N/S ตรึงกับจอ (hud) ถ้าปล่อยไว้ตอนหมุนกล้อง มันจะค้างอยู่ที่เดิม
        # ขณะที่แท่งขั้วเคลื่อนไป -> ดูเหมือนป้ายหลุดจากตัวขั้ว จึงซ่อนระหว่างหมุน
        self.play(FadeOut(n_lab), FadeOut(s_lab), run_time=0.5)

        # phi ต้องน้อย! ถ้าเอียงมาก (เคยลอง 68°) แกนเพลาจะตั้งขึ้นบนจอ ดูเหมือน
        # เอาเครื่องตั้งขึ้น ซึ่งผิดจากความจริง (แกนหมุนควรพุ่งเข้าไปในกระดาษ)
        # เอียงน้อยๆ = ยังเป็นภาพตัดขวางแบบหนังสือ แค่เผยความลึกให้เห็น
        self.add(back, bars)
        self.move_camera(phi=34 * DEGREES, theta=-84 * DEGREES, run_time=3.4)
        self.wait(1.0)

        # ---------- D. คอมมิวเตเตอร์ + แปรงถ่าน ----------
        cap4 = self.hud(caption_top("ปลายเพลาด้านหน้า = คอมมิวเตเตอร์ (หมุนไปกับอาร์เมเจอร์)"))
        self.play(FadeOut(cap3), run_time=0.3)
        self.play(FadeIn(cap4), run_time=0.6)

        sh = shaft()
        comm = commutator()
        self.play(Create(sh), run_time=0.8)
        self.play(FadeIn(comm), run_time=1.1)
        self.wait(0.7)

        cap5 = self.hud(caption_top(
            "แปรงถ่านอยู่กับที่ — แค่ \"แตะ\" ผิวคอมมิวเตเตอร์ที่หมุนผ่าน", color=WARN))
        self.play(FadeOut(cap4), run_time=0.3)
        self.play(FadeIn(cap5), run_time=0.6)
        br = brush_pair()
        self.play(FadeIn(br, scale=1.3), run_time=0.9)
        self.wait(1.0)

        # ---------- E. หมุนให้เห็นรอบตัว ----------
        cap6 = self.hud(caption_top(
            "ตัวนำทุกเส้น + คอมมิวเตเตอร์ = ชุดเดียวกัน หมุนพร้อมกันบนเพลาเดียว"))
        self.play(FadeOut(cap5), run_time=0.3)
        self.play(FadeIn(cap6), run_time=0.6)
        self.move_camera(theta=-100 * DEGREES, phi=40 * DEGREES, run_time=3.0)
        self.wait(0.8)

        # ---------- F. กลับมามองตรง เตรียมเข้าเนื้อหา ----------
        cap7 = self.hud(caption_top("กลับมามองตรงหน้าตัด — เพื่อดูสนามแม่เหล็ก", color=OK))
        self.play(FadeOut(cap6), run_time=0.3)
        self.play(FadeIn(cap7), run_time=0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2.6)
        self.play(FadeIn(n_lab), FadeIn(s_lab), run_time=0.5)
        self.wait(0.9)

        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, front, back,
                                         bars, marks, sh, comm, br, cap7, ttl2, ref)],
                  run_time=0.9)

        card = VGroup(
            Text("อาร์เมเจอร์ + คอมมิวเตเตอร์ = หมุน", font_size=27, color=CURRENT),
            Text("ขั้วแม่เหล็ก + แปรงถ่าน = อยู่กับที่", font_size=27, color=WARN),
        ).arrange(DOWN, buff=0.45).move_to([0, 0.2, 0])
        self.hud(card)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ================================================================ S2
class S2_NeutralPlane(SafeThreeDScene):
    """หน้า 1-2 · ระนาบเป็นกลางคืออะไร ทำไมแปรงถ่านต้องอยู่ตรงนั้น (รูป 6-1)"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        ttl = self.hud(title("ระนาบเป็นกลาง — เส้นที่ emf = 0", size=29))
        ref = self.hud(page_ref("หน้า 1-2 · รูปที่ 6-1"))
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.8)

        n_pole, s_pole = pole_piece(-1, "N"), pole_piece(+1, "S")
        n_lab = self.hud(Text("N", font_size=34, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0]))
        s_lab = self.hud(Text("S", font_size=34, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0]))
        front, _, _ = armature_cage()
        fld = main_field(0.0)

        cap1 = self.hud(caption_top("สนามหลักวิ่งจาก N ไป S · ตัวนำหมุนตัดเส้นแรง"))
        self.play(FadeIn(cap1), FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab),
                  FadeIn(s_lab), Create(front), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in fld], lag_ratio=0.10),
                  run_time=1.3)
        self.wait(0.6)

        # ---------- ตัวนำวิ่งรอบวง + emf สด ----------
        theta = ValueTracker(0.0)

        def coil_pos():
            a = theta.get_value()
            return STAGE + R_ARM * np.array([np.sin(a), np.cos(a), 0.0])

        coil = Dot(coil_pos(), radius=0.13, color=CURRENT)
        coil.add_updater(lambda m: m.move_to(coil_pos()))

        emf_row = live_row("emf", "", lambda: abs(np.sin(theta.get_value())),
                           [-4.35, 1.75, 0], decimals=2, num_color=EMF)
        self.hud(emf_row)

        cap2 = self.hud(caption_top(
            "ตัดเส้นแรงมาก → emf มาก · ขนานกับเส้นแรง → emf = 0"))
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), FadeIn(coil), FadeIn(emf_row),
                  run_time=0.9)
        self.play(theta.animate.set_value(2 * PI), run_time=4.6, rate_func=linear)
        self.wait(0.4)

        # ---------- ทำไม emf = 0 ตรงนั้น (จุดที่ Min เคยเข้าใจผิดว่าเพราะ B = 0) ----------
        coil.clear_updaters()
        emf_row[1].clear_updaters()
        self.play(FadeOut(coil), FadeOut(emf_row), run_time=0.5)

        self.play(FadeOut(cap2), run_time=0.3)
        cap2b = self.hud(caption_top(
            "คิดภาพ: เส้นแรง = เส้นเชือกขึงตึงจาก N ไป S · ตัวนำ = ใบมีด", color=EXAMC))
        self.play(FadeIn(cap2b), run_time=0.5)

        eqA = MathTex(r"e = B\,l\,v\,\sin\theta", font_size=40, color=EMF)
        eqA.move_to([4.35, 1.55, 0])
        self.hud(eqA)
        self.play(FadeIn(eqA), run_time=0.6)

        # --- ใบมีดที่ 1: ใต้ขั้ว วิ่งดิ่งลง = ฟันขวางเชือก 90°
        bx = STAGE[0] - 1.55
        blade = Line([bx - 0.26, STAGE[1] + 1.30, 0], [bx + 0.26, STAGE[1] + 1.30, 0],
                     color=WARN, stroke_width=8)
        varr = Arrow([bx + 0.55, STAGE[1] + 1.15, 0], [bx + 0.55, STAGE[1] + 0.35, 0],
                     buff=0, color=WARN, stroke_width=5, tip_length=0.18)
        self.play(FadeIn(blade), GrowArrow(varr), run_time=0.6)
        self.play(blade.animate.shift(DOWN * 2.55), varr.animate.shift(DOWN * 2.55),
                  run_time=2.2, rate_func=linear)

        r1 = self.hud(Text("ฟันขวางเชือก 90° → ตัดเต็มที่ → emf สูงสุด",
                           font_size=22, color=WARN).move_to([0, -2.55, 0]))
        s90 = self.hud(MathTex(r"\sin 90^\circ = 1", font_size=34, color=WARN)
                       .move_to([4.35, 0.85, 0]))
        self.play(FadeIn(r1), FadeIn(s90), run_time=0.8)
        self.wait(1.3)

        # --- ใบมีดที่ 2: ที่ระนาบเป็นกลาง วิ่งแนวนอน = ลู่ไปตามเชือก
        self.play(FadeOut(blade), FadeOut(varr), FadeOut(r1), FadeOut(s90),
                  run_time=0.5)
        self.play(FadeOut(cap2b), run_time=0.3)
        cap2c = self.hud(caption_top(
            "แต่ตรงบนสุด ตัวนำวิ่ง \"แนวนอน\" — ลู่ไปตามเชือก ไม่ได้ฟันโดนสักเส้น",
            color=OK))
        self.play(FadeIn(cap2c), run_time=0.5)

        ty = STAGE[1] + R_ARM
        blade2 = Line([STAGE[0] - 1.45, ty - 0.26, 0], [STAGE[0] - 1.45, ty + 0.26, 0],
                      color=OK, stroke_width=8)
        varr2 = Arrow([STAGE[0] - 1.30, ty + 0.55, 0], [STAGE[0] - 0.50, ty + 0.55, 0],
                      buff=0, color=OK, stroke_width=5, tip_length=0.18)
        self.play(FadeIn(blade2), GrowArrow(varr2), run_time=0.6)
        self.play(blade2.animate.shift(RIGHT * 2.90), varr2.animate.shift(RIGHT * 2.90),
                  run_time=2.2, rate_func=linear)

        s0 = self.hud(MathTex(r"\sin 0^\circ = 0", font_size=34, color=OK)
                      .move_to([4.35, 0.85, 0]))
        r2 = self.hud(Text("ไม่ได้ตัดสักเส้น → emf = 0", font_size=23, color=OK)
                      .move_to([0, -2.55, 0]))
        self.play(FadeIn(s0), FadeIn(r2), run_time=0.8)
        self.wait(1.2)

        # --- ตอกย้ำจุดที่มักเข้าใจผิด
        self.play(FadeOut(cap2c), run_time=0.3)
        cap2d = self.hud(caption_top(
            "สำคัญ: เชือกยังอยู่หนาแน่นเท่าเดิม — B ไม่ได้เป็นศูนย์ แค่ไม่ได้ตัดมัน",
            color=EXAMC))
        self.play(FadeIn(cap2d), run_time=0.5)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in (blade2, varr2, eqA, s0, r2)], run_time=0.6)
        cap2 = cap2d

        # ---------- ปักเส้นระนาบเป็นกลาง ----------
        npl = plane_line(0.0, OK)
        # ย้ายไปด้านข้าง: ถ้าวางไว้กลาง-บน จะชนแถบคำบรรยาย (CAP_TOP_Y = 2.72)
        np_lab = self.hud(Text("ระนาบเป็นกลาง", font_size=21, color=OK)
                          .move_to([2.75, 1.75, 0]))
        cap3 = self.hud(caption_top("จุดบน-ล่างคือที่ emf = 0 → ลากเป็นเส้น = ระนาบเป็นกลาง",
                                    color=OK))
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), Create(npl), FadeIn(np_lab),
                  run_time=1.2)
        self.wait(1.0)

        # ---------- ทำไมแปรงถ่านต้องอยู่ตรงนี้ ----------
        coil.clear_updaters()
        emf_row[1].clear_updaters()
        self.play(FadeOut(coil), FadeOut(emf_row), run_time=0.5)

        comm = commutator()
        br = brush_pair()
        cap4 = self.hud(caption_top(
            "แปรงถ่านลัดวงจรขดลวดตรงนี้ — ถ้ายังมี emf ค้าง กระแสจะพุ่ง ขดไหม้", color=WARN))
        self.play(FadeOut(cap3), run_time=0.3)
        self.play(FadeIn(cap4), FadeIn(comm), FadeIn(br), run_time=1.0)
        self.wait(1.3)

        # ---------- ชื่อเรียก + ปิดท้าย ----------
        cap5 = self.hud(caption_top("ชื่อทางการ: ระนาบเป็นกลางทางกล / ทางเรขาคณิต"))
        self.play(FadeOut(cap4), run_time=0.3)
        self.play(FadeIn(cap5), run_time=0.6)
        self.wait(1.2)

        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, front, fld,
                                         npl, np_lab, comm, br, cap5, ttl, ref)],
                  run_time=0.9)

        card = exam_card(
            "คำถาม 6-1: ระนาบเป็นกลางคืออะไร",
            "ตำแหน่งที่ขดลวดเคลื่อนผ่านแล้วแรงเคลื่อนเหนี่ยวนำเป็นศูนย์")
        self.hud(card)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.6)

        tease = self.hud(Text("แต่ในทางปฏิบัติ มันไม่อยู่นิ่ง — มันเลื่อน",
                              font_size=26, color=WARN).move_to([0, -1.75, 0]))
        self.play(FadeIn(tease), run_time=0.8)
        self.wait(1.6)


# ================================================================ S3
class S3_TwoFields(SafeThreeDScene):
    """หน้า 3-4 · สนาม 2 สนามบวกกัน -> สนามหลักเบี่ยงเบน (รูป 6-2 ก/ข/ค)"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        ttl = self.hud(title("อาร์เมเจอร์รีแอคชั่น — สนามสองสนามบวกกัน", size=28))
        ref = self.hud(page_ref("หน้า 3-4 · รูปที่ 6-2 (ก)"))
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.8)

        n_pole, s_pole = pole_piece(-1, "N"), pole_piece(+1, "S")
        n_lab = self.hud(Text("N", font_size=34, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0]))
        s_lab = self.hud(Text("S", font_size=34, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0]))
        front, _, _ = armature_cage()

        # ---------- (ก) สนามหลักอย่างเดียว ----------
        fld = main_field(0.0)
        npl0 = plane_line(0.0, OK, dashed=True)
        cap1 = self.hud(caption_top("(ก) สนามจากขดลวดสนามแม่เหล็กอย่างเดียว → ระนาบตั้งตรง"))
        self.play(FadeIn(cap1), FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab),
                  FadeIn(s_lab), Create(front), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in fld], lag_ratio=0.10),
                  Create(npl0), run_time=1.4)
        self.wait(1.0)

        # ---------- (ข) สนามอาร์เมเจอร์อย่างเดียว — ตั้งฉาก ----------
        ref2 = self.hud(page_ref("หน้า 4 · รูปที่ 6-2 (ข)"))
        cap2 = self.hud(caption_top("(ข) สนามจากขดลวดอาร์เมเจอร์อย่างเดียว — แกนตั้งฉาก 90°"))
        marks = face_marks(z=0.0)
        self.play(FadeOut(cap1), FadeOut(ref), run_time=0.3)
        self.play(FadeIn(cap2), FadeIn(ref2),
                  FadeOut(fld), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.05),
                  run_time=1.2)

        ba = Arrow(STAGE + np.array([0, 1.30, 0]), STAGE + np.array([0, -1.30, 0]),
                   buff=0, color=CURRENT, stroke_width=8, tip_length=0.28,
                   max_tip_length_to_length_ratio=0.4)
        ba_lab = self.hud(Text("Bₐ (สนามอาร์เมเจอร์)", font_size=21, color=CURRENT)
                          .move_to([3.9, STAGE[1] + 1.15, 0]))
        self.play(GrowArrow(ba), FadeIn(ba_lab), run_time=1.0)
        self.wait(0.6)

        cap3 = self.hud(caption_top(
            "ทำไม 90°? เพราะกระแสกลับทิศตรง \"แนวแปรงถ่าน\" พอดี ไม่ใช่ตรงหน้าขั้ว"))
        brush_axis = plane_line(0.0, WARN, length=2.2, width=3)
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.play(Create(brush_axis), run_time=0.8)
        self.wait(1.4)

        # ---------- (ค) บวกเวกเตอร์ -> เบี่ยง ----------
        ref3 = self.hud(page_ref("หน้า 4 · รูปที่ 6-2 (ค)"))
        cap4 = self.hud(caption_top("(ค) สองสนามบวกกันแบบเวกเตอร์ → สนามรวมเอียง"))
        self.play(FadeOut(cap3), FadeOut(ref2), run_time=0.3)
        self.play(FadeIn(cap4), FadeIn(ref3),
                  FadeOut(marks), FadeOut(brush_axis), run_time=0.7)

        self.play(FadeIn(fld), run_time=0.7)
        origin = STAGE + np.array([0, 0, 0])
        v_main = Arrow(origin, origin + np.array([2.05, 0, 0]), buff=0, color=FIELD,
                       stroke_width=8, tip_length=0.26,
                       max_tip_length_to_length_ratio=0.4)
        v_arm = Arrow(origin, origin + np.array([0, -1.25, 0]), buff=0, color=CURRENT,
                      stroke_width=8, tip_length=0.26,
                      max_tip_length_to_length_ratio=0.4)
        v_sum = Arrow(origin, origin + np.array([2.05, -1.25, 0]), buff=0, color=WARN,
                      stroke_width=9, tip_length=0.28,
                      max_tip_length_to_length_ratio=0.4)
        dash = DashedLine(origin + np.array([2.05, 0, 0]),
                          origin + np.array([2.05, -1.25, 0]),
                          color=CURRENT, stroke_width=2.5, dash_length=0.10)
        sum_lab = self.hud(Text("สนามรวม", font_size=21, color=WARN)
                           .move_to([3.55, STAGE[1] - 1.55, 0]))

        self.play(FadeOut(ba), FadeOut(ba_lab), run_time=0.4)
        self.play(GrowArrow(v_main), run_time=0.7)
        self.play(GrowArrow(v_arm), run_time=0.7)
        self.play(Create(dash), GrowArrow(v_sum), FadeIn(sum_lab), run_time=1.1)
        self.wait(1.2)

        # ---------- เสริม vs หักล้าง (Min ขอให้อธิบาย) ----------
        cap5 = self.hud(caption_top(
            "ทิศเดียวกัน = เสริมกัน (แรงขึ้น) · ทิศตรงข้าม = หักล้างกัน (อ่อนลง)",
            color=OK))
        self.play(FadeOut(cap4), run_time=0.3)
        self.play(FadeIn(cap5), run_time=0.6)
        self.wait(1.6)

        # ---------- โหลดมากขึ้น -> เอียงมากขึ้น (ตัวเลขวิ่งจริง) ----------
        self.play(FadeOut(cap5), run_time=0.3)
        cap5b = self.hud(caption_top("โหลดมากขึ้น → Bₐ แรงขึ้น → สนามรวมยิ่งเอียง"))
        self.play(FadeIn(cap5b), run_time=0.5)

        load = ValueTracker(0.61)      # = 1.25/2.05 ให้ต่อเนื่องจากรูปสามเหลี่ยมเดิม

        def _tip():
            return origin + np.array([2.05, -2.05 * load.get_value(), 0])

        dyn_arm = always_redraw(lambda: Arrow(
            origin + np.array([2.05, 0, 0]), _tip(), buff=0, color=CURRENT,
            stroke_width=7, tip_length=0.24, max_tip_length_to_length_ratio=0.4))
        dyn_sum = always_redraw(lambda: Arrow(
            origin, _tip(), buff=0, color=WARN, stroke_width=9, tip_length=0.28,
            max_tip_length_to_length_ratio=0.4))

        cur_row = live_row("กระแสโหลด", "A", lambda: 65 * load.get_value(),
                           [-5.95, 1.95, 0], decimals=0, num_color=CURRENT)
        ang_row = live_row("มุมเอียง", "°",
                           lambda: np.degrees(np.arctan(load.get_value())),
                           [1.35, 1.95, 0], decimals=1, num_color=WARN)
        self.hud(cur_row, ang_row)

        self.play(FadeOut(v_arm), FadeOut(v_sum), FadeOut(dash), run_time=0.4)
        self.play(FadeIn(dyn_arm), FadeIn(dyn_sum), FadeIn(cur_row), FadeIn(ang_row),
                  run_time=0.7)
        self.play(load.animate.set_value(1.30), run_time=2.4)
        self.wait(0.5)
        self.play(load.animate.set_value(0.22), run_time=1.9)
        self.wait(0.4)
        self.play(load.animate.set_value(0.85), run_time=1.5)
        self.wait(0.8)

        dyn_arm.clear_updaters()
        dyn_sum.clear_updaters()
        cur_row[1].clear_updaters()
        ang_row[1].clear_updaters()
        self.play(FadeOut(dyn_arm), FadeOut(dyn_sum), FadeOut(cur_row),
                  FadeOut(ang_row), run_time=0.6)
        # ไม่ FadeOut(cap5b) ตรงนี้ — ปล่อยให้บล็อกถัดไปสลับให้ (ถ้าเอาออกก่อน
        # FadeOut ซ้ำจะดึงมันกลับเข้าฉากแล้วกระพริบ)
        cap5 = cap5b

        # ---------- ระนาบเลื่อนตาม ----------
        tilt = 27 * DEGREES
        npl1 = plane_line(tilt, WARN, width=6)
        rot = CurvedArrow(STAGE + np.array([-0.9, 2.15, 0]),
                          STAGE + np.array([1.1, 1.95, 0]),
                          color=WARN, stroke_width=3, tip_length=0.18)
        cap6 = self.hud(caption_top("สนามเอียง → จุดที่ emf = 0 เลื่อนตามทิศหมุน", color=WARN))
        self.play(FadeOut(cap5), run_time=0.3)
        self.play(FadeIn(cap6), run_time=0.6)
        self.play(Transform(fld, main_field(tilt)), Create(npl1), Create(rot),
                  run_time=1.8)
        self.wait(1.4)

        # v_arm / v_sum / dash ถูกเอาออกไปแล้วตอนสลับเป็นลูกศรแบบไดนามิก
        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, front, fld,
                                         npl0, npl1, rot, v_main,
                                         sum_lab, cap6, ttl, ref3)], run_time=0.9)

        card = exam_card(
            "คำถาม 6-3: อะไรทำให้ระนาบเป็นกลางเลื่อน",
            "(1) อาร์เมเจอร์รีแอคชั่น  (2) การเหนี่ยวนำในตัวเองขณะคอมมิวเตชั่น")
        self.hud(card)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)


# ================================================================ S4
class S4_BB_AA(SafeThreeDScene):
    """หน้า 5-7 · แยกผลเสีย 2 อย่าง: BB แรงดันตก / AA สปาร์ค (รูป 6-3)"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        ttl = self.hud(title("ผลเสีย 2 อย่าง — คนละกลุ่มตัวนำ คนละปัญหา", size=28))
        ref = self.hud(page_ref("หน้า 5-7 · รูปที่ 6-3"))
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.6)

        # ---------- สะพานเชื่อมจาก S3: ต้อง "เอียงก่อน" ถึงจะแยกได้ ----------
        # หนังสือหน้า 5 เขียนลำดับชัดเจน: ระนาบเลื่อน -> สนามอาร์เมเจอร์เอียงตามทิศหมุน
        # -> "แล้วสนามนี้ถูกแยกออกเป็น 2 ส่วน" การเอียงคือสาเหตุที่ทำให้แยกได้ ไม่ใช่ว่า
        # BB/AA มีอยู่แยกกันเองตั้งแต่ต้น
        capA = self.hud(caption_top("ทวนจาก S3: สนามหลัก + สนามอาร์เมเจอร์ (90°) → สนามรวมเอียง"))
        self.play(FadeIn(capA), run_time=0.6)

        bo = STAGE + np.array([0, 0.15, 0])
        bf = Arrow(bo, bo + np.array([1.85, 0, 0]), buff=0, color=FIELD,
                  stroke_width=7, tip_length=0.24)
        ba = Arrow(bo, bo + np.array([0, -1.15, 0]), buff=0, color=CURRENT,
                  stroke_width=7, tip_length=0.24)
        bres = Arrow(bo, bo + np.array([1.85, -1.15, 0]), buff=0, color=WARN,
                    stroke_width=8, tip_length=0.26)
        bdash = DashedLine(bo + np.array([1.85, 0, 0]), bo + np.array([1.85, -1.15, 0]),
                           color=CURRENT, stroke_width=2, dash_length=0.09)
        self.play(GrowArrow(bf), run_time=0.5)
        self.play(GrowArrow(ba), run_time=0.5)
        self.play(Create(bdash), GrowArrow(bres), run_time=0.8)
        self.wait(0.7)

        capB = self.hud(caption_top(
            "เอียงแล้วนี่แหละ — ถึงค่อยแยกวิเคราะห์ผลได้เป็น 2 องค์ประกอบ", color=EXAMC))
        self.play(FadeOut(capA), run_time=0.3)
        self.play(FadeIn(capB), run_time=0.5)

        # หมายเหตุ: เคยใช้ TransformFromCopy(bres, ...) ตรงนี้ แล้วเจอบั๊กจริงที่ป้าย
        # aa_tag โผล่จางๆ ก่อนถึงคิว (สลับลำดับ hud() แล้วก็ยังเป็น แปลว่าไม่ใช่ปัญหา
        # จังหวะ hud() แต่เป็นปฏิสัมพันธ์กับ TransformFromCopy เอง) เปลี่ยนมาใช้
        # GrowArrow + FadeIn ธรรมดาแทน — แพทเทิร์นเดียวกับที่พิสูจน์แล้วว่าปลอดภัยทั่ว
        # ทั้งไฟล์นี้ (เช่นบล็อก BB/AA ด้านล่าง)
        bb_arrow = Arrow(bo, bo + np.array([1.85, 0, 0]), buff=0, color=WARN,
                         stroke_width=5, tip_length=0.20).shift(DOWN * 1.55)
        bb_tag = self.hud(Text("BB (ขนานสนามหลัก)", font_size=17, color=WARN)
                          .next_to(bb_arrow, DOWN, buff=0.12))
        aa_arrow = Arrow(bo, bo + np.array([0, -1.15, 0]), buff=0, color=WARN,
                         stroke_width=5, tip_length=0.20).shift(RIGHT * 2.55)
        aa_tag = self.hud(Text("AA (ตั้งฉากสนามหลัก)", font_size=17, color=WARN)
                          .next_to(aa_arrow, RIGHT, buff=0.18))
        self.play(GrowArrow(bb_arrow), FadeIn(bb_tag), run_time=0.8)
        self.play(GrowArrow(aa_arrow), FadeIn(aa_tag), run_time=0.8)
        self.wait(1.1)

        self.play(*[FadeOut(m) for m in (bf, ba, bres, bdash, bb_arrow, bb_tag,
                                         aa_arrow, aa_tag, capB)], run_time=0.7)

        cap0 = self.hud(caption_top("มาดูว่ากลุ่มตัวนำไหนสร้างแต่ละองค์ประกอบ"))
        self.play(FadeIn(cap0), run_time=0.5)

        n_pole, s_pole = pole_piece(-1, "N"), pole_piece(+1, "S")
        n_lab = self.hud(Text("N", font_size=34, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0]))
        s_lab = self.hud(Text("S", font_size=34, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0]))
        front, _, _ = armature_cage()
        self.play(FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab), FadeIn(s_lab),
                  Create(front), run_time=1.0)

        # ---------- กลุ่ม BB: ตัวนำบน-ล่าง (ใต้หน้าขั้ว) ----------
        # แบ่งกลุ่มตามหนังสือหน้า 5 เป๊ะ:
        #   BB = ตัวนำ "ด้านบน-ล่าง" ของอาร์เมเจอร์ -> สนามต่อต้าน -> แรงดันตก
        #   AA = ตัวนำ "ด้านซ้าย-ขวา" ของอาร์เมเจอร์ -> สนามขวาง -> เบี่ยง -> สปาร์ค
        bb_marks = VGroup()
        aa_marks = VGroup()
        for a in slot_angles():
            u = np.array([np.cos(a), np.sin(a), 0.0])
            p = STAGE + R_ARM * u
            # ทิศ ⊙/⊗ แบ่งซ้าย/ขวาของแนวแปรงถ่าน (แก้ตาม face_marks() — เดิมใช้แกน
            # ผิดเป็นบน/ล่าง) ส่วนเกณฑ์ BB/AA (|sin(a)|>0.55) ยังคงเดิม เพราะยึดตาม
            # คำบรรยายในหนังสือ (BB=ตัวนำบน-ล่าง, AA=ตัวนำซ้าย-ขวา) ซึ่งถูกอยู่แล้ว
            out = np.dot(u, np.array([1.0, 0.0, 0.0])) > 0
            m = conductor_mark(p, out)
            (bb_marks if abs(np.sin(a)) > 0.55 else aa_marks).add(m)

        cap1 = self.hud(caption_top(
            "กลุ่ม BB — ตัวนำ \"ด้านบนและด้านล่าง\" ของอาร์เมเจอร์", color=WARN))
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m) for m in bb_marks], lag_ratio=0.08),
                  run_time=1.2)

        b_main = Arrow(STAGE + np.array([-1.0, 2.05, 0]), STAGE + np.array([1.0, 2.05, 0]),
                       buff=0, color=FIELD, stroke_width=6, tip_length=0.22)
        b_opp = Arrow(STAGE + np.array([1.0, 1.62, 0]), STAGE + np.array([-1.0, 1.62, 0]),
                      buff=0, color=CURRENT, stroke_width=6, tip_length=0.22)
        bb_txt = self.hud(Text("ทิศตรงข้ามสนามหลัก → หักล้าง", font_size=20, color=WARN)
                          .move_to([0, STAGE[1] + 2.60, 0]))
        self.play(GrowArrow(b_main), GrowArrow(b_opp), FadeIn(bb_txt), run_time=1.1)
        self.wait(0.5)

        cap2 = self.hud(caption_top("สนามหลักอ่อนลง ⇒ แรงดันที่ขั้วตก", color=WARN))
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.6)
        self.wait(1.3)

        # ---------- กลุ่ม AA: ตัวนำบน-ล่าง (ช่องว่างระหว่างขั้ว) ----------
        self.play(FadeOut(b_main), FadeOut(b_opp), FadeOut(bb_txt),
                  bb_marks.animate.set_opacity(0.22), run_time=0.7)

        cap3 = self.hud(caption_top(
            "กลุ่ม AA — ตัวนำ \"ด้านซ้ายและด้านขวา\" ของอาร์เมเจอร์", color=OK))
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m) for m in aa_marks], lag_ratio=0.10),
                  run_time=1.1)

        a_main = Arrow(STAGE + np.array([-1.0, 2.05, 0]), STAGE + np.array([1.0, 2.05, 0]),
                       buff=0, color=FIELD, stroke_width=6, tip_length=0.22)
        a_cross = Arrow(STAGE + np.array([1.55, 1.45, 0]), STAGE + np.array([1.55, 2.65, 0]),
                        buff=0, color=CURRENT, stroke_width=6, tip_length=0.22)
        aa_txt = self.hud(Text("ตั้งฉากกับสนามหลัก → ดันให้เบี่ยง", font_size=20, color=OK)
                          .move_to([-1.9, STAGE[1] + 2.60, 0]))
        self.play(GrowArrow(a_main), GrowArrow(a_cross), FadeIn(aa_txt), run_time=1.1)
        self.wait(0.5)

        cap4 = self.hud(caption_top("สนามหลักเบี่ยง ⇒ ระนาบเลื่อน ⇒ แปรงถ่านผิดที่ ⇒ สปาร์ค",
                                    color=EMF))
        self.play(FadeOut(cap3), run_time=0.3)
        self.play(FadeIn(cap4), run_time=0.6)
        spark = Star(n=7, outer_radius=0.24, inner_radius=0.10, color=EMF,
                     fill_opacity=1.0, stroke_width=0)
        spark.move_to(STAGE + np.array([0, R_ARM + 0.30, 0]))
        self.play(FadeIn(spark, scale=1.8), run_time=0.7)
        self.play(Indicate(spark, color=EMF, scale_factor=1.4), run_time=0.8)
        self.wait(1.2)

        # ---------- เตือนเรื่องตัวอักษรในรูปหนังสือ (โน้ตหน้า 6 กำกับไว้) ----------
        cap5 = self.hud(caption_top(
            "ระวัง: ตัวอักษร A/B ในรูปหนังสือใช้ไม่ตรงกัน — ให้ยึดชื่อผลเสีย ไม่ใช่ตัวอักษร",
            color=EXAMC))
        self.play(FadeOut(cap4), run_time=0.3)
        self.play(FadeIn(cap5), run_time=0.6)
        self.wait(1.6)

        # ---------- สรุป ----------
        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, front, bb_marks,
                                         aa_marks, a_main, a_cross, aa_txt, spark,
                                         cap5, ttl, ref)], run_time=0.9)

        s1 = Text("BB → แรงดันตก      AA → สปาร์ค", font_size=30, color=WHITE)
        s2 = Text("ระยะเอียงแปรผันตรงกับกระแสโหลด", font_size=25, color=OK)
        summary = VGroup(s1, s2).arrange(DOWN, buff=0.40).move_to([0, 1.1, 0])
        self.hud(summary)
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        self.wait(1.2)

        card = exam_card(
            "คำถาม 6-5: ผลเสียของอาร์เมเจอร์รีแอคชั่นมีอะไรบ้าง",
            "(1) แรงดันที่ขั้วลดลง   (2) อาร์ค/สปาร์คที่คอมมิวเตเตอร์กับแปรงถ่าน",
            y=-1.35)
        self.hud(card)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.8)


# ================================================================ S5
class S5_Commutation(SafeScene):
    """หน้า 7-8 · คอมมิวเตชั่น: ส่งไม้ผลัดกระแส 100 A (รูปที่ 6-4)"""

    def construct(self):
        ttl = title("คอมมิวเตชั่น — การส่งไม้ผลัดของกระแส", size=29)
        ref = page_ref("หน้า 7-8 · รูปที่ 6-4")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.8)

        d0 = caption_top("คอมมิวเตชั่น = กลับทิศกระแสในขดลวด แล้วส่งไฟตรงออกวงจรภายนอก")
        self.play(FadeIn(d0), run_time=0.7)
        self.wait(1.2)

        # ---------- เวที: คลี่อาร์เมเจอร์ออกเป็นแนวตรง ----------
        bar_w, bar_h, gap = 1.25, 0.62, 0.10
        bar_y = -0.75
        bars, blabels = VGroup(), VGroup()
        for i, name in enumerate(["", "1", "2", ""]):
            x = (i - 1.5) * (bar_w + gap)
            r = Rectangle(width=bar_w, height=bar_h, fill_color="#455A64",
                          fill_opacity=0.9, stroke_color=METAL, stroke_width=2)
            r.move_to([x, bar_y, 0])
            bars.add(r)
            if name:
                blabels.add(Text(name, font_size=23, color=WHITE)
                            .move_to(r.get_center()))

        coils, clabels = VGroup(), VGroup()
        for i, nm in enumerate(["A", "B", "C"]):
            x = (i - 1.0) * (bar_w + gap)
            arc = Arc(radius=0.40, start_angle=0, angle=PI, color=CURRENT,
                      stroke_width=5)
            arc.move_to([x, bar_y + bar_h / 2 + 0.52, 0])
            coils.add(arc)
            clabels.add(Text(nm, font_size=22, color=CURRENT)
                        .move_to([x, bar_y + bar_h / 2 + 1.32, 0]))

        brush_pos = ValueTracker(-0.68)
        brush = Rectangle(width=1.45, height=0.48, fill_color=WARN,
                          fill_opacity=0.95, stroke_width=0)
        brush.add_updater(lambda m: m.move_to(
            [brush_pos.get_value(), bar_y - bar_h / 2 - 0.30, 0]))
        bplus = Text("+", font_size=28, color=BLACK)
        bplus.add_updater(lambda m: m.move_to(brush.get_center()))

        d1 = caption_top("แปรงถ่านบวกแตะซี่คอมมิวเตเตอร์ 2 ซี่พร้อมกัน")
        self.play(FadeOut(d0), run_time=0.3)
        self.play(FadeIn(d1), FadeIn(bars), FadeIn(blabels),
                  FadeIn(brush), FadeIn(bplus), run_time=1.0)
        self.play(LaggedStart(*[Create(a) for a in coils], lag_ratio=0.2),
                  FadeIn(clabels), run_time=1.1)

        # ---------- กระแสแบ่ง 2 เส้นทาง ----------
        prog = ValueTracker(0.0)
        i1 = live_row("ซี่ที่ 1", "A", lambda: 50 + 50 * prog.get_value(),
                      [-4.55, 1.72, 0], decimals=0, num_color=CURRENT)
        i2 = live_row("ซี่ที่ 2", "A", lambda: 50 - 50 * prog.get_value(),
                      [1.15, 1.72, 0], decimals=0, num_color=CURRENT)

        d2 = caption_top("โหลด 100 A แบ่ง 2 เส้นทางขนาน → เส้นทางละ 50 A")
        self.play(FadeOut(d1), run_time=0.3)
        self.play(FadeIn(d2), FadeIn(i1), FadeIn(i2), run_time=1.0)
        self.wait(1.2)

        # ---------- ขด B ถูกลัดวงจร emf = 0 ----------
        hl = SurroundingRectangle(coils[1], color=OK, buff=0.13, stroke_width=4)
        bnote = Text("ขด B ถูกลัดวงจร · emf = 0 · ไม่มีกระแส", font_size=21, color=OK)
        bnote.move_to([0, bar_y + 2.15, 0])
        d3 = caption_top("ขดที่กำลังถูกลัดวงจรต้องมี emf = 0 พอดี ไม่งั้นกระแสพุ่ง", color=OK)
        self.play(FadeOut(d2), run_time=0.3)
        self.play(FadeIn(d3), Create(hl), FadeIn(bnote), run_time=1.1)
        self.wait(1.4)

        # ---------- ส่งไม้ผลัด ----------
        d4 = caption_top("แปรงถ่านเลื่อน → ซี่ 1 รับเพิ่ม 50→100 A · ซี่ 2 ปล่อย 50→0 A")
        self.play(FadeOut(d3), run_time=0.3)
        self.play(FadeIn(d4), run_time=0.6)
        self.play(prog.animate.set_value(1.0),
                  brush_pos.animate.set_value(-1.42), run_time=3.2)
        self.wait(0.7)

        done = Text("ซี่ที่ 2 หลุดจากแปรงถ่าน → คอมมิวเตชั่นสมบูรณ์", font_size=23, color=OK)
        done.move_to([0, -2.45, 0])
        self.play(FadeIn(done, scale=1.05), run_time=0.8)
        self.wait(1.4)

        i1[1].clear_updaters()
        i2[1].clear_updaters()
        brush.clear_updaters()
        bplus.clear_updaters()
        self.play(*[FadeOut(m) for m in (bars, blabels, coils, clabels, brush, bplus,
                                         i1, i2, hl, bnote, done, d4, ttl, ref)],
                  run_time=0.9)

        card = exam_card(
            "คำถาม 6-8: คอมมิวเตชั่นคืออะไร",
            "การกลับทิศกระแสในขดลวดอาร์เมเจอร์ย่อย แล้วนำไฟตรงออกสู่วงจรภายนอก")
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.9)


# ================================================================ S6
class S6_SelfInduction(SafeScene):
    """หน้า 9-10 · การเหนี่ยวนำในตัวเอง -> ระนาบเลื่อนซ้ำ (รูปที่ 6-5, 6-6)"""

    def construct(self):
        ttl = title("การเหนี่ยวนำในตัวเอง — ทำไมยังสปาร์คอยู่ดี", size=28)
        ref = page_ref("หน้า 9 · รูปที่ 6-5")
        self.play(FadeIn(ttl), FadeIn(ref), run_time=0.8)

        # ---------- ขด A กระแสลดลงเป็นศูนย์ ----------
        cx = -3.05
        coil = Arc(radius=0.72, start_angle=0, angle=PI, color=CURRENT,
                   stroke_width=7).move_to([cx, 0.35, 0])
        # วางป้ายไว้นอกวงสนาม (รัศมีใหญ่สุด 1.65) ไม่งั้นเส้นวงพาดทับตัวอักษร
        clab = Text("ขด A", font_size=22, color=CURRENT).move_to([cx - 2.35, 0.35, 0])

        # วางแถวตัวเลขไว้ "ฝั่งขวา" ให้พ้นวงสนาม (วงรัศมี 1.65 รอบ cx กินพื้นที่ซ้าย
        # ถึง x=-1.4) ไม่งั้นหน่วย "A" ไปทับเส้นวงพอดี
        cur = ValueTracker(50.0)
        crow = live_row("กระแสในขด A", "A", lambda: cur.get_value(),
                        [1.95, 1.95, 0], decimals=0, num_color=CURRENT)

        d1 = caption_top("ขด A เคลื่อนเข้าหาระนาบเป็นกลาง → กระแสในตัวมันลดลงเป็นศูนย์")
        self.play(FadeIn(d1), Create(coil), FadeIn(clab), FadeIn(crow), run_time=1.2)

        rings = VGroup(*[Circle(radius=r, color=FIELD, stroke_width=3)
                         .move_to([cx, 0.35, 0]).set_stroke(opacity=0.75)
                         for r in (1.05, 1.35, 1.65)])
        rlab = Text("สนามรอบขด A", font_size=19, color=FIELD).move_to([cx, -1.65, 0])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15),
                  FadeIn(rlab), run_time=1.3)
        self.wait(0.6)

        d2 = caption_top("กระแสลด → สนามรอบตัวมันยุบตัวลง", color=WARN)
        self.play(FadeOut(d1), run_time=0.3)
        self.play(FadeIn(d2), run_time=0.6)
        self.play(cur.animate.set_value(0.0),
                  rings.animate.scale(0.18, about_point=np.array([cx, 0.35, 0]))
                  .set_stroke(opacity=0.15),
                  run_time=2.4)
        self.wait(0.5)

        # ---------- กฎเลนซ์ -> emf ต้าน ----------
        d3 = caption_top("กฎเลนซ์: สนามยุบ → เกิด emf พยายามรักษากระแสให้ไหลต่อ", color=EMF)
        lenz = Arrow([cx - 0.85, -0.75, 0], [cx + 0.85, -0.75, 0], buff=0,
                     color=EMF, stroke_width=6, tip_length=0.22)
        llab = Text("emf เหนี่ยวนำในตัวเอง", font_size=20, color=EMF)
        llab.move_to([cx, -1.65, 0])
        self.play(FadeOut(d2), run_time=0.3)
        self.play(FadeIn(d3), FadeOut(rlab), run_time=0.6)
        self.play(GrowArrow(lenz), FadeIn(llab), run_time=1.0)
        self.wait(1.2)

        # ---------- ทำไมกระแสยังพุ่ง ----------
        crow[1].clear_updaters()
        self.play(*[FadeOut(m) for m in (coil, clab, rings, lenz, llab, crow, d3)],
                  run_time=0.7)

        d4 = caption_top("จุดที่หลายคนพลาด — emf เล็ก แต่ความต้านทานก็เล็กกว่า")
        eq1 = MathTex(r"e = L\,\frac{di}{dt}", font_size=44, color=EMF)
        eq2 = Text("เล็กมาก", font_size=22, color=GRAYTXT)
        g1 = VGroup(eq1, eq2).arrange(DOWN, buff=0.30).move_to([-3.35, 0.45, 0])

        eq3 = MathTex(r"I = \frac{V}{R}", font_size=44, color=CURRENT)
        eq4 = Text("แต่ R ของแปรงถ่าน+ซี่ ก็เล็กกว่า", font_size=21, color=GRAYTXT)
        fit_width(eq4, 4.5)
        g2 = VGroup(eq3, eq4).arrange(DOWN, buff=0.30).move_to([1.35, 0.45, 0])

        arrow = Arrow([-1.30, 0.45, 0], [-0.35, 0.45, 0], buff=0, color=GRAYTXT,
                      stroke_width=4, tip_length=0.20)
        concl = Text("⇒ กระแสยังไหลได้มาก ⇒ อาร์ค/สปาร์ค", font_size=26, color=EMF)
        concl.move_to([0, -1.85, 0])

        self.play(FadeIn(d4), run_time=0.5)
        self.play(FadeIn(g1), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(g2), run_time=0.9)
        self.play(FadeIn(concl, scale=1.06), run_time=0.9)
        self.wait(1.6)

        self.play(*[FadeOut(m) for m in (g1, g2, arrow, concl, d4, ref)], run_time=0.7)

        # ---------- รูป 6-6: ระนาบเลื่อน 2 ขยัก ----------
        ref2 = page_ref("หน้า 10 · รูปที่ 6-6")
        d5 = caption_top("ผลรวม: ระนาบเป็นกลางเลื่อน 2 ขยัก ไปทางเดียวกัน (ทิศหมุน)")
        self.play(FadeIn(ref2), FadeIn(d5), run_time=0.7)

        sc = np.array([0.0, -0.55, 0.0])
        ring = Circle(radius=1.25, color=METAL, stroke_width=3).move_to(sc)
        self.play(Create(ring), run_time=0.7)

        def pl(angle, color, w=5, dashed=False, length=1.95):
            v = np.array([-np.sin(angle), np.cos(angle), 0.0])
            if dashed:
                return DashedLine(sc - v * length, sc + v * length, color=color,
                                  stroke_width=w, dash_length=0.13)
            return Line(sc - v * length, sc + v * length, color=color, stroke_width=w)

        l0 = pl(0.0, "#64B5F6", dashed=True)
        t0 = Text("ทางกล", font_size=19, color="#64B5F6").move_to([-1.45, 1.72, 0])
        self.play(Create(l0), FadeIn(t0), run_time=0.8)

        a1 = 20 * DEGREES
        l1 = pl(a1, CURRENT, w=4)
        t1 = Text("+ อาร์เมเจอร์รีแอคชั่น", font_size=19, color=CURRENT)
        t1.move_to([1.75, 1.72, 0])
        self.play(Create(l1), FadeIn(t1), run_time=1.0)
        self.wait(0.5)

        a2 = 34 * DEGREES
        l2 = pl(a2, WARN, w=6)
        t2 = Text("+ เหนี่ยวนำในตัวเอง", font_size=19, color=WARN)
        t2.move_to([4.15, 0.62, 0])
        fit_width(t2, 2.7)
        self.play(Create(l2), FadeIn(t2), run_time=1.0)
        self.wait(0.8)

        final = Text("= ระนาบเป็นกลางทางไฟฟ้า (ระนาบสำหรับคอมมิวเตชั่น)",
                     font_size=25, color=OK).move_to([0, -2.75, 0])
        fit_width(final, 11.5)
        self.play(FadeIn(final, scale=1.05), run_time=0.9)
        self.wait(1.7)

        # ---------- ข้อจำกัด ----------
        self.play(*[FadeOut(m) for m in (ring, l0, l1, l2, t0, t1, t2, final, d5,
                                         ttl, ref2)], run_time=0.9)

        lim = VGroup(
            Text("ระยะเลื่อนแปรผันตรงกับกระแสโหลด", font_size=27, color=WHITE),
            Text("โหลดเปลี่ยน → ต้องขยับแปรงถ่านใหม่ทุกครั้ง ⇒ ไม่เวิร์กจริง",
                 font_size=23, color=WARN),
        ).arrange(DOWN, buff=0.38).move_to([0, 1.35, 0])
        fit_width(lim, 11.5)
        self.play(FadeIn(lim, shift=UP * 0.2), run_time=1.0)
        self.wait(1.4)

        card = exam_card(
            "คำถาม 6-11: ตำแหน่งใหม่ของระนาบเรียกว่าอะไร",
            "ระนาบเป็นกลางทางไฟฟ้า (electrical / commutating plane)", y=-1.45)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(1.9)

        # ---------- คู่คำถามที่ข้อสอบชอบถามเทียบกัน (6-12 vs 6-13) ----------
        self.play(FadeOut(lim), FadeOut(card), run_time=0.7)

        head = Text("คู่ที่ข้อสอบชอบถามเทียบกัน", font_size=21, color=EXAMC)
        q12 = VGroup(
            Text("6-12  วางแปรงถ่านที่ระนาบ \"ทางกล\"", font_size=23, color=WHITE),
            Text("→ คอมมิวเตชั่นไม่สมบูรณ์ เกิดสปาร์ค (ระนาบจริงเลื่อนไปแล้ว)",
                 font_size=21, color=WARN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        q13 = VGroup(
            Text("6-13  วางแปรงถ่านที่ระนาบ \"ทางไฟฟ้า\"", font_size=23, color=WHITE),
            Text("→ สมบูรณ์ ไม่สปาร์ค — แต่เฉพาะที่กระแสโหลดค่านั้นเท่านั้น",
                 font_size=21, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        pair = VGroup(head, q12, q13).arrange(DOWN, aligned_edge=LEFT, buff=0.52)
        fit_width(pair, 11.8)
        pair.move_to([0, 0.35, 0])

        self.play(FadeIn(head), run_time=0.5)
        self.play(FadeIn(q12, shift=RIGHT * 0.2), run_time=0.9)
        self.wait(1.2)
        self.play(FadeIn(q13, shift=RIGHT * 0.2), run_time=0.9)
        self.wait(2.2)


# ================================================================ S7
class S7_Interpole(SafeThreeDScene):
    """หน้า 11-12 · ขั้วแม่เหล็กเสริม interpole (รูปที่ 6-7)"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        ttl = self.hud(title("ตัวแก้ที่ 1 — ขั้วแม่เหล็กเสริม (Interpole)", size=28))
        ref = self.hud(page_ref("หน้า 11-12 · รูปที่ 6-7"))
        cap0 = self.hud(caption_top("ปัญหา: ต้องขยับแปรงถ่านทุกครั้งที่โหลดเปลี่ยน — แก้ยังไง"))
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=0.9)

        n_pole, s_pole = pole_piece(-1, "N"), pole_piece(+1, "S")
        n_lab = self.hud(Text("N", font_size=32, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0]))
        s_lab = self.hud(Text("S", font_size=32, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0]))
        front, _, _ = armature_cage()
        self.play(FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab), FadeIn(s_lab),
                  Create(front), run_time=1.0)

        # ---------- ติดตั้ง interpole ที่ระนาบเป็นกลางทางกล ----------
        cap1 = self.hud(caption_top(
            "แท่งขั้วเล็กๆ ติดตรง \"ระนาบเป็นกลางทางกล\" = ระหว่างขั้วหลัก", color=OK))
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.6)

        ips = VGroup()
        for sgn in (+1, -1):
            b = Rectangle(width=0.95, height=0.62, color=OK, fill_color=OK,
                          fill_opacity=0.45, stroke_width=2.5)
            b.move_to(STAGE + np.array([0, sgn * (R_ARM + 0.68), 0]))
            ips.add(b)
        ip_n = self.hud(Text("S", font_size=24, color=WHITE)
                        .move_to(STAGE + np.array([0, R_ARM + 0.68, 0])))
        ip_s = self.hud(Text("N", font_size=24, color=WHITE)
                        .move_to(STAGE + np.array([0, -R_ARM - 0.68, 0])))
        self.play(FadeIn(ips), FadeIn(ip_n), FadeIn(ip_s), run_time=1.0)
        self.wait(0.8)

        # ---------- ต่ออนุกรมกับอาร์เมเจอร์ ----------
        cap2 = self.hud(caption_top("ต่ออนุกรมกับอาร์เมเจอร์ → กระแสโหลดไหลผ่านมันด้วย"))
        wire = VGroup(
            line3(STAGE + np.array([0.48, R_ARM + 0.68, 0]),
                  STAGE + np.array([2.05, R_ARM + 0.68, 0]), CURRENT, 0.012),
            line3(STAGE + np.array([2.05, R_ARM + 0.68, 0]),
                  STAGE + np.array([2.05, -R_ARM - 0.68, 0]), CURRENT, 0.012),
            line3(STAGE + np.array([2.05, -R_ARM - 0.68, 0]),
                  STAGE + np.array([0.48, -R_ARM - 0.68, 0]), CURRENT, 0.012),
        )
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), Create(wire), run_time=1.2)
        self.wait(1.0)

        # ---------- หักล้างสนามอาร์เมเจอร์ตรงระนาบ ----------
        cap3 = self.hud(caption_top("สนามของมันมีทิศ \"ตรงข้าม\" สนามอาร์เมเจอร์ตรงจุดนั้น"))
        v_arm = Arrow(STAGE + np.array([-1.75, 0.62, 0]),
                      STAGE + np.array([-1.75, -0.62, 0]), buff=0, color=CURRENT,
                      stroke_width=7, tip_length=0.24)
        v_ip = Arrow(STAGE + np.array([-1.15, -0.62, 0]),
                     STAGE + np.array([-1.15, 0.62, 0]), buff=0, color=OK,
                     stroke_width=7, tip_length=0.24)
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.play(GrowArrow(v_arm), GrowArrow(v_ip), run_time=1.0)
        self.wait(0.7)

        cap4 = self.hud(caption_top("ทิศตรงข้าม = หักล้างกัน ⇒ ไม่เหลือสนามให้ยุบตัว", color=OK))
        self.play(FadeOut(cap3), run_time=0.3)
        self.play(FadeIn(cap4), run_time=0.6)
        self.play(FadeOut(v_arm), FadeOut(v_ip), run_time=1.0)
        self.wait(0.9)

        cap5 = self.hud(caption_top("ไม่มีสนามยุบ ⇒ ไม่มี emf เหนี่ยวนำในตัวเอง ⇒ ระนาบไม่เลื่อน",
                                    color=OK))
        self.play(FadeOut(cap4), run_time=0.3)
        self.play(FadeIn(cap5), run_time=0.6)
        self.wait(1.5)

        # ---------- กฎขั้ว + ปรับตัวเอง ----------
        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, front, ips,
                                         ip_n, ip_s, wire, cap5, ref)], run_time=0.9)

        rules = VGroup(
            Text("กฎขั้ว: ขั้วของ interpole = ขั้วหลักตัวถัดไปในทิศหมุน",
                 font_size=24, color=WHITE),
            Text("ต่ออนุกรม ⇒ โหลดขึ้น สนามก็เข้มขึ้นตาม ⇒ ปรับตัวเองอัตโนมัติ",
                 font_size=24, color=OK),
        ).arrange(DOWN, buff=0.40).move_to([0, 1.45, 0])
        fit_width(rules, 11.8)
        self.hud(rules)
        self.play(FadeIn(rules, shift=UP * 0.2), run_time=1.0)
        self.wait(1.6)

        lim = VGroup(
            Text("✅ แก้การเหนี่ยวนำในตัวเอง — ได้สมบูรณ์", font_size=23, color=OK),
            Text("⚠️ แก้อาร์เมเจอร์รีแอคชั่น — ได้บางส่วน (ติดอยู่จุดเดียว แต่ปัญหาเกิดทั้งวง)",
                 font_size=23, color=WARN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.55, 0])
        fit_width(lim, 11.8)
        self.hud(lim)
        self.play(FadeIn(lim, shift=UP * 0.15), run_time=1.0)
        self.wait(1.9)


# ================================================================ S8
class S8_Compensating(SafeScene):
    """หน้า 13-14 · ชุดขดลวดชดเชย + ตารางเทียบ + สรุปบท (รูปที่ 6-8)"""

    def construct(self):
        ttl = title("ตัวแก้ที่ 2 — ชุดขดลวดชดเชย (Compensating winding)", size=27)
        ref = page_ref("หน้า 13 · รูปที่ 6-8")
        cap0 = caption_top("interpole แก้ได้จุดเดียว — แต่ปัญหาเกิดรอบอาร์เมเจอร์ทั้งวง")
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=0.9)

        sc = np.array([0.0, -0.55, 0.0])
        ring = Circle(radius=1.35, color=METAL, stroke_width=3).move_to(sc)

        poles = VGroup()
        for sgn, lab in ((-1, "N"), (+1, "S")):
            r = Rectangle(width=1.05, height=2.30, color=METAL, fill_color=METAL,
                          fill_opacity=0.28, stroke_width=2.5)
            r.move_to(sc + np.array([sgn * 2.45, 0, 0]))
            poles.add(VGroup(r, Text(lab, font_size=30, color=WHITE)
                             .move_to(r.get_center())))

        self.play(Create(ring), FadeIn(poles), run_time=1.0)

        # ---------- ขดลวดอาร์เมเจอร์บนวง ----------
        arm_marks = VGroup()
        for i in range(10):
            a = PI / 2 + (i + 0.5) * TAU / 10
            p = sc + 1.35 * np.array([np.cos(a), np.sin(a), 0])
            # ⊙ ใกล้ขั้ว S (ขวา, cos a > 0), ⊗ ใกล้ขั้ว N (ซ้าย) — แก้จากบั๊กบน/ล่างเดิม
            arm_marks.add(conductor_mark(p, np.cos(a) > 0, r=0.10))

        cap1 = caption_top("ขดลวดชดเชย = ขดเล็กๆ ฝังใน \"ผิวหน้า\" ของแท่งขั้วหลัก")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1),
                  LaggedStart(*[FadeIn(m) for m in arm_marks], lag_ratio=0.06),
                  run_time=1.4)

        comp = VGroup()
        for sgn in (-1, +1):
            face_x = sc[0] + sgn * (2.45 - sgn * 0.0) - sgn * 0.52
            for k in (-1, 0, 1):
                p = np.array([face_x, sc[1] + k * 0.72, 0])
                comp.add(conductor_mark(p, sgn < 0, r=0.10, color=OK))
        self.play(LaggedStart(*[FadeIn(m) for m in comp], lag_ratio=0.10),
                  run_time=1.3)
        self.wait(0.8)

        # ---------- กระแสตรงข้าม -> สนามตรงข้าม -> หักล้าง ----------
        cap2 = caption_top("กระแสในนั้นทิศตรงข้ามกับตัวนำอาร์เมเจอร์ที่อยู่ใกล้ๆ", color=OK)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.6)
        self.wait(1.2)

        steps = VGroup(
            Text("กระแสตรงข้าม", font_size=22, color=CURRENT),
            Text("→  สนามตรงข้าม", font_size=22, color=FIELD),
            Text("→  หักล้างสนามอาร์เมเจอร์ทั้งวง", font_size=22, color=OK),
        ).arrange(RIGHT, buff=0.42).move_to([0, 1.62, 0])
        fit_width(steps, 11.5)
        cap3 = caption_top("ต่ออนุกรมกับอาร์เมเจอร์เหมือนกัน ⇒ ปรับตัวเองตามโหลด")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in steps],
                              lag_ratio=0.3), run_time=1.6)
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in (ring, poles, arm_marks, comp, steps, cap3,
                                         ttl, ref)], run_time=0.9)

        # ---------- ตารางเทียบ ----------
        ttl2 = title("เทียบกัน — ใครแก้อะไรได้", size=29)
        ref2 = page_ref("หน้า 13-14")
        self.play(FadeIn(ttl2), FadeIn(ref2), run_time=0.7)

        hdr = VGroup(
            Text("", font_size=21),
            Text("Interpole", font_size=23, color=OK),
            Text("ขดลวดชดเชย", font_size=23, color=CURRENT),
        )
        rows_txt = [
            ("ติดตั้งที่ไหน", "ระหว่างขั้วหลัก", "ฝังในผิวหน้าขั้ว"),
            ("ครอบคลุม", "เฉพาะจุดระนาบ", "รอบอาร์เมเจอร์ทั้งวง"),
            ("แก้เหนี่ยวนำในตัวเอง", "ได้สมบูรณ์", "ไม่สมบูรณ์"),
            ("แก้อาร์เมเจอร์รีแอคชั่น", "ได้บางส่วน", "ได้"),
        ]
        col_x = (-4.30, -0.35, 3.40)
        top_y = 1.72
        gap_y = 0.86

        tbl = VGroup()
        for j, m in enumerate(hdr):
            m.move_to([col_x[j], top_y, 0])
            tbl.add(m)
        for i, row in enumerate(rows_txt):
            for j, cell in enumerate(row):
                col = GRAYTXT if j == 0 else (OK if j == 1 else CURRENT)
                m = Text(cell, font_size=20, color=col)
                fit_width(m, 3.45)
                m.move_to([col_x[j], top_y - (i + 1) * gap_y, 0])
                tbl.add(m)

        self.play(LaggedStart(*[FadeIn(m) for m in tbl], lag_ratio=0.05),
                  run_time=2.2)
        self.wait(2.0)

        mem = Text("จำง่าย: interpole = หมอเฉพาะทาง · ขดลวดชดเชย = หมอทั่วไป",
                   font_size=23, color=EXAMC).move_to([0, -2.85, 0])
        fit_width(mem, 11.5)
        self.play(FadeIn(mem), run_time=0.8)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in (tbl, mem, ttl2, ref2)], run_time=0.8)

        # ---------- สรุปบท ----------
        ttl3 = title("สรุปบทที่ 6", size=30)
        ref3 = page_ref("หน้า 14")
        chain = VGroup(
            Text("จ่ายโหลด → สนามอาร์เมเจอร์เกิดขึ้น (ตั้งฉาก 90°)", font_size=23,
                 color=CURRENT),
            Text("→ บวกกับสนามหลัก → สนามเบี่ยง → ระนาบเลื่อน (ขยักที่ 1)",
                 font_size=23, color=WARN),
            Text("→ คอมมิวเตชั่น + เหนี่ยวนำในตัวเอง → เลื่อนอีก (ขยักที่ 2)",
                 font_size=23, color=EMF),
            Text("→ แก้ด้วย interpole + ขดลวดชดเชย → เกือบไม่เลื่อนเลย",
                 font_size=23, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.46).move_to([0, 0.55, 0])
        fit_width(chain, 12.0)

        self.play(FadeIn(ttl3), FadeIn(ref3), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.25) for c in chain],
                              lag_ratio=0.28), run_time=2.6)
        self.wait(2.2)

        last = Text("ใช้ทั้งคู่พร้อมกัน = ลดการเลื่อนได้เกือบทั้งหมด แม้โหลดเปลี่ยน",
                    font_size=25, color=OK).move_to([0, -2.55, 0])
        fit_width(last, 11.8)
        self.play(FadeIn(last, scale=1.04), run_time=0.9)
        self.wait(2.2)


# ================================================================ S9 (bonus)
class S9_Bonus_RotatingConductorEMF(SafeScene):
    """โบนัส (นอกลำดับหน้าหนังสือ) — อาร์เมเจอร์หมุนจริง แต่ละตัวนำ emf เปลี่ยนต่อเนื่อง

    Min ขอ (2026-08-31): "อยากเห็นวิดีโอของอาร์เมเจอร์มันหมุน แบบพอมันหมุนแล้วสนามแต่ละจุด
    เปลี่ยนแปลงยังไง ทำลูกศรเป็นเวกเตอร์ให้ดูหน่อย"

    ระวัง — คนละปริมาณกับ ⊙/⊗ คงที่ที่เห็นใน S1/S4/S8:
    ที่นี่คือ "แรงเคลื่อนเหนี่ยวนำดิบ" ในตัวนำแต่ละเส้น ณ ขณะที่ยังไม่ผ่านคอมมิวเตเตอร์
    (เหมือนต่อขดลวดเดี่ยวเข้าสลิปริง) มันแกว่งขึ้นลงต่อเนื่องเป็น cos(มุม) ตามตำแหน่ง
    ส่วน ⊙/⊗ ในคลิปอื่นคือกระแส "หลัง" คอมมิวเตเตอร์จัดให้เป็น DC แล้ว (คงที่ตามตำแหน่ง
    ซ้าย-ขวาของแนวแปรงถ่าน ไม่ใช่แกว่งตามมุม) — สองอย่างนี้ไม่ขัดแย้งกัน แค่คนละขั้นตอน

    ฟิสิกส์: แกนขั้ว = แนวนอน (N ซ้าย/S ขวา), แกนแปรงถ่าน = แนวตั้ง
    ตัวนำที่มุม a มีความเร็วเชิงสัมผัส ทิศ (a+90°); สนาม B ทิศ 0° (จาก N ไป S)
    e(a) ∝ sin(มุมระหว่าง v กับ B) = sin(a+90°) = cos(a)
    -> สูงสุดตรงหน้าขั้ว (a=0°,180°), ศูนย์ตรงระนาบเป็นกลาง (a=90°,270°)
    ตรงกับสูตรเดียวกับที่ EP07/S2 ใช้ติดตามขดเดียว แค่ขยายมาดูทั้งวงพร้อมกัน
    """

    N_C = 12

    def construct(self):
        ttl = title("โบนัส — อาร์เมเจอร์หมุน แต่ละจุด emf เปลี่ยนยังไง", size=26)
        self.play(FadeIn(ttl, shift=DOWN * 0.15), run_time=0.8)

        cap0 = caption_top(
            "emf ดิบในตัวนำแต่ละเส้น ก่อนผ่านคอมมิวเตเตอร์ — คนละเรื่องกับ ⊙/⊗ คงที่ก่อนหน้า",
            color=EXAMC)
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.4)

        n_pole, s_pole = pole_piece(-1, "N"), pole_piece(+1, "S")
        n_lab = Text("N", font_size=32, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0])
        s_lab = Text("S", font_size=32, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0])
        ring = Circle(radius=R_ARM, color=METAL, stroke_width=3).move_to(STAGE)
        fld = main_field(0.0, n=3, opacity=0.55)

        cap1 = caption_top("ลูกศร: ยาว = emf มากตอนนั้น · แดง = ออกจากจอ · ฟ้า = เข้าจอ")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab), FadeIn(s_lab),
                  FadeIn(fld), Create(ring), FadeIn(cap1), run_time=1.2)

        theta = ValueTracker(0.0)
        base_angles = slot_angles(self.N_C)

        def build_vectors():
            g = VGroup()
            for a0 in base_angles:
                a = a0 + theta.get_value()
                u = np.array([np.cos(a), np.sin(a), 0.0])
                e = np.cos(a)
                length = 0.16 + 0.62 * abs(e)
                start = STAGE + R_ARM * u
                end = start + length * u
                color = EMF if e > 0 else FIELD
                g.add(Arrow(start, end, buff=0, color=color, stroke_width=5,
                           tip_length=0.13, max_tip_length_to_length_ratio=0.5))
            return g

        vecs = always_redraw(build_vectors)
        self.add(vecs)
        self.wait(0.3)

        cap2 = caption_top(
            "หมุนดูสด — ตรงหน้าขั้ว emf สูงสุด · ตรงระนาบเป็นกลาง (บน-ล่าง) emf = 0")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.5)
        self.play(theta.animate.set_value(2 * TAU), run_time=8.0, rate_func=linear)
        self.wait(0.5)

        vecs.clear_updaters()
        self.play(FadeOut(vecs), FadeOut(cap2), run_time=0.6)

        cap3 = caption_top(
            "พอผ่านคอมมิวเตเตอร์ มันถูกจัดใหม่เป็นกระแส DC คงที่ตามตำแหน่ง — แบบที่เห็นใน S1/S4/S8",
            color=OK)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, ring, fld,
                                         cap3, ttl)], run_time=0.9)

        s1 = Text("emf ในตัวนำ = cos(มุมจากขั้ว) เสมอ ไม่ว่าจะหมุนไปกี่รอบ",
                  font_size=25, color=WHITE)
        s2 = Text("คอมมิวเตเตอร์คือตัวที่แปลงมันให้เป็นไฟตรงที่ใช้ได้จริง",
                  font_size=23, color=OK)
        card = VGroup(s1, s2).arrange(DOWN, buff=0.40).move_to([0, 0.3, 0])
        fit_width(card, 12.0)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)


# ================================================================ S10 (bonus)
class S10_Bonus_SpinningArmatureFixedNeutral(SafeScene):
    """โบนัส 2 — สนามหลัก + อาร์เมเจอร์หมุนจริง: ระนาบเป็นกลางไม่หมุนตามล้อ

    Min ขอ (2026-08-31): อยากเห็นสนามหลัก+สนามอาร์เมเจอร์หมุนไปด้วยกัน จะได้รู้ว่า
    ต้องคิดสรุปภาพรวมยังไง โดยเฉพาะ "ระนาบเป็นกลางเป็นยังไงตอนอาร์เมเจอร์หมุน"

    คำตอบที่ซีนนี้แสดง: ⊙/⊗ ของตัวนำแต่ละเส้น "สลับ" ตอนมันหมุนผ่านแนวแปรงถ่าน
    (คอมมิวเตชั่นเกิดสดๆ ให้เห็น) แต่ตัวแนวแปรงถ่าน/ทิศของ Bₐ เอง**ไม่หมุนตามล้อ**
    — มันค้างอยู่กับที่ตลอด เพราะคอมมิวเตเตอร์คอยจัดกระแสให้คงที่ตามตำแหน่ง

    ใช้ face_marks()/main_field() ที่แก้แล้ว (แบ่งซ้าย-ขวา ตรงกับหนังสือ+แหล่งอ้างอิง
    มาตรฐาน: ตัวนำใกล้ N=⊗, ใกล้ S=⊙)
    """

    N_C = 12

    def construct(self):
        ttl = title("โบนัส 2 — หมุนทั้งระบบ: ระนาบเป็นกลางหมุนตามไหม?", size=25)
        self.play(FadeIn(ttl, shift=DOWN * 0.15), run_time=0.8)

        cap0 = caption_top("สนามหลัก (นิ่ง) + อาร์เมเจอร์ (หมุนจริง) — จับตาแนวแปรงถ่าน")
        self.play(FadeIn(cap0), run_time=0.7)

        n_pole, s_pole = pole_piece(-1, "N"), pole_piece(+1, "S")
        n_lab = Text("N", font_size=32, color=WHITE).move_to(
            [STAGE[0] - (POLE_X - POLE_W / 2), STAGE[1], 0])
        s_lab = Text("S", font_size=32, color=WHITE).move_to(
            [STAGE[0] + (POLE_X - POLE_W / 2), STAGE[1], 0])
        ring = Circle(radius=R_ARM, color=METAL, stroke_width=3).move_to(STAGE)
        fld = main_field(0.0, n=3, opacity=0.5)

        brush_axis = plane_line(0.0, WARN, length=R_ARM + 0.35, width=4)
        axis_lbl = Text("แนวแปรงถ่าน (นิ่งเสมอ)", font_size=18, color=WARN)
        axis_lbl.next_to(brush_axis, UP, buff=0.15)

        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(n_pole), FadeIn(s_pole), FadeIn(n_lab), FadeIn(s_lab),
                  FadeIn(fld), Create(ring), run_time=1.0)
        self.play(Create(brush_axis), FadeIn(axis_lbl), run_time=0.8)
        self.wait(0.6)

        theta = ValueTracker(0.0)
        base_angles = slot_angles(self.N_C)

        def build_marks():
            g = VGroup()
            for a0 in base_angles:
                a = a0 + theta.get_value()
                u = np.array([np.cos(a), np.sin(a), 0.0])
                p = STAGE + R_ARM * u
                out = np.cos(a) > 0  # ⊙ ใกล้ S(ขวา), ⊗ ใกล้ N(ซ้าย) — แนวแปรงถ่าน "นิ่ง"
                g.add(conductor_mark(p, out))
            return g

        marks = always_redraw(build_marks)

        ba = Arrow(STAGE + [0, R_ARM - 0.15, 0], STAGE + [0, -(R_ARM - 0.15), 0],
                  buff=0, color=OK, stroke_width=7, tip_length=0.26)
        ba_lbl = Text("Bₐ (ทิศคงที่)", font_size=19, color=OK)
        ba_lbl.next_to(ba, LEFT, buff=0.2)

        cap1 = caption_top("ตัวนำแต่ละเส้นสลับ ⊙⇄⊗ ตอนหมุนผ่านแนวแปรงถ่าน — นี่คือคอมมิวเตชั่น")
        self.play(FadeIn(marks), FadeIn(ba), FadeIn(ba_lbl), FadeIn(cap1), run_time=1.0)
        self.play(theta.animate.set_value(2 * TAU), run_time=9.0, rate_func=linear)
        self.wait(0.5)

        marks.clear_updaters()
        cap2 = caption_top(
            "แต่แนวแปรงถ่านกับทิศ Bₐ ไม่หมุนตามล้อเลย — อยู่นิ่งตลอดเวลา", color=OK)
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.6)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in (n_pole, s_pole, n_lab, s_lab, ring, fld,
                                         brush_axis, axis_lbl, marks, ba, ba_lbl,
                                         cap2, ttl)], run_time=0.9)

        s1 = Text("ตัวนำหมุนไปเรื่อยๆ สลับ ⊙⇄⊗ ตลอด", font_size=25, color=CURRENT)
        s2 = Text("แต่ระนาบเป็นกลาง + ทิศ Bₐ คงที่ — คอมมิวเตเตอร์คอยจัดให้", font_size=23,
                  color=OK)
        card = VGroup(s1, s2).arrange(DOWN, buff=0.40).move_to([0, 0.3, 0])
        fit_width(card, 12.0)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
