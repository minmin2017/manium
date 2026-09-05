"""
gear_law_similar.py — Mechanics of Machinery (W06) หน้า 5-6
"To find angular velocity ratio for contact between 2 rotating bodies"

ที่มาของรูป: Exam_Prep/Mechanics of Machinery/pages_gear/page-05.jpg, page-06.jpg

โจทย์จาก Min: "ผมไม่เห็นภาพว่าสามเหลี่ยมมันอยู่ตรงไหน"
 -> วาดทีละจุด ทีละเส้น แล้วยกสามเหลี่ยมออกมาขยายทีละรูป บอกว่าแต่ละด้านคือเส้นอะไร
 -> สีของเส้นในรูป = สีของตัวอักษรในสมการ (Min สั่ง "แบ่งสีเส้นตามสมการด้วย")

ซีน
  G05A_PointsAndLines   หน้า 5 (1/2) สร้างรูปทีละจุด ทีละเส้น
  G05B_SimilarTriangles หน้า 5 (2/2) สามเหลี่ยมคล้าย 2 คู่ (ยกออกมาขยาย)
  G06_PitchPoint        หน้า 6 จุด P บนเส้นศูนย์กลาง -> w2/w3 = BP/AP
"""

import numpy as np
from manim import *
from mlib import *

# ----------------------------------------------------------------- สีตามสมการ
C_AQ  = "#4FC3F7"   # AQ   แขนรัศมีชิ้นที่ 2
C_AR  = "#1E88E5"   # AR   ระยะตั้งฉากจาก A ลงเส้น normal
C_VQ2 = "#B3E5FC"   # EQ   ความเร็ว v_Q2
C_BQ  = "#FFB74D"   # BQ   แขนรัศมีชิ้นที่ 3
C_BS  = "#F4511E"   # BS   ระยะตั้งฉากจาก B ลงเส้น normal
C_VQ3 = "#FFE082"   # FQ   ความเร็ว v_Q3
C_VN  = "#26C6DA"   # PQ   องค์ประกอบตามแนว normal (ตัวร่วมของทั้งสองสมการ)
C_NORM = "#EF5350"  # เส้น contact normal (แดง ตามสไลด์)
C_LOC  = "#90A4AE"  # line of centers
C_TAN  = "#78909C"  # ด้านที่เหลือ (องค์ประกอบตามแนวสัมผัส)
C_BODY = "#607D8B"  # ผิวของชิ้นงาน

# ------------------------------------------------------- เรขาคณิต (โลคอล, P = origin)
# 2026-09-05 rebuild: จุดทั้งหมดมาจากการเทรซหน้าจริงของ Min ใน Fusion 360
# (D:\Downloads\ai_tew.dxf) ยืนยันจุดต่อจุดในแชทแล้วว่า "ถูกต้องทั้งหมด" -- สเปกเต็ม
# + ตาราง raw DXF coords อยู่ที่ C:\Users\wicha\Desktop\Main_note\Claude_Specs\
# "Spur Gear Pages 5-6 — Velocity Ratio Geometry Spec.md" (อ่านก่อนแก้ไฟล์นี้อีกที)
#
# ระยะจาก P (raw DXF units, "ไม่ได้เลือกเอง" -- คำนวณตรงจากตารางที่ยืนยันแล้ว):
#   |PA| = 422.313   |PB| = 350.067   |PQ| = 123.038   (Q อยู่ฝั่ง A -> ลบ)
RAW_PA = 422.313
RAW_PB = 350.067
RAW_PQ = 123.038

# มุม pressure angle "จริง": fit เส้นตรงผ่าน R,Q,P,S (4 จุดที่เกือบเรียงเส้นตรง
# เดียวกันจริงในตาราง = เส้น contact normal) ด้วย least-squares -> เอียงจากแนวราบ
# (tangent ที่ P) ประมาณ 23.5° -- เลขนี้มาจากรูปในหนังสือจริง ไม่ใช่เลือกเอง
PHI_REAL = 23.5 * DEGREES

# ปัญหา (ตรวจด้วยเลขจริงจากตาราง ไม่ใช่เดา): ที่ PHI_REAL สามเหลี่ยม A-R-Q มีมุม
# ที่ A แคบมากแค่ ~6.7° -- รูปแบนจนดูเหมือนเส้นตรง (ตรงกับปัญหาเดิมของสไลด์ที่มา:
# "มุมที่ A แค่ ~5 องศา") แก้ด้วยการขยายแค่ตัว "มุม" PHI (ไม่แตะ A_LEN/B_LEN/T_Q
# ซึ่งมาจากตารางจริงตรงๆ) -- นี่คือการขยาย "มุม" ตามที่สเปกอธิบาย ไม่ใช่คิดตัวเลข
# ใหม่อิสระจากของจริง ทิศทาง/ลำดับจุดของ R,Q,S ยังตรงกับตารางที่ยืนยันแล้วทุกจุด
# EXAG=1.8x (23.5° -> ~42.2°) เลือกจากการลองหลายค่า (1.6x..2.0x): ทำให้มุมที่ A
# ขึ้นมาเป็น ~27° (สามเหลี่ยมอ่านออกชัดเจน) และมุมที่ B (สามเหลี่ยม B-S-Q) ยังคง
# เป็นรูปที่อ่านง่าย (~54°, ไม่ผิดธรรมชาติ) -- เดิมสามเหลี่ยมฝั่ง B ไม่ได้แบนขนาด
# ฝั่ง A อยู่แล้วในข้อมูลจริง (มุมที่ B จริง ~39° ก็อ่านได้พอสมควรแล้ว)
PHI_EXAG = 1.8
PHI = PHI_REAL * PHI_EXAG

A_LEN = RAW_PA           # AP -- ค่าจริงจากตาราง ไม่ใช่เลขเลือกเอง
B_LEN = RAW_PB           # BP -- ค่าจริงจากตาราง (สังเกต: B_LEN < A_LEN จริง
                          # ตรงข้ามกับสัดส่วนเดิมของโค้ดรุ่นก่อน 2026-09-05)
T_Q   = -RAW_PQ          # ตำแหน่งของ Q บนเส้น normal วัดจาก P (ลบ = อยู่ฝั่ง A) -- ค่าจริง

U = np.array([np.cos(PHI), -np.sin(PHI), 0.0])          # ทิศ contact normal
T = np.array([-np.sin(PHI), -np.cos(PHI), 0.0])         # ตั้งฉากกับ normal


def _perp_ccw(v):
    return np.array([-v[1], v[0], 0.0])


def _perp_cw(v):
    return np.array([v[1], -v[0], 0.0])


_P = np.array([0.0, 0.0, 0.0])
_A = np.array([0.0,  A_LEN, 0.0])
_B = np.array([0.0, -B_LEN, 0.0])
_Q = _P + T_Q * U
_R = _P + float(np.dot(_A - _P, U)) * U      # เท้าของฉากจาก A ลงเส้น normal
_S = _P + float(np.dot(_B - _P, U)) * U      # เท้าของฉากจาก B ลงเส้น normal

_VN = float(np.linalg.norm(_P - _Q))         # องค์ประกอบตามแนว normal ที่ใช้ร่วมกัน
_AR = float(np.linalg.norm(_A - _R))
_BS = float(np.linalg.norm(_B - _S))
W2 = _VN / _AR                               # w2 ที่ทำให้ v_Q2 ฉายลงตรงจุด P พอดี
W3 = _VN / _BS

_E = _Q + W2 * _perp_ccw(_Q - _A)            # ปลายเวกเตอร์ v_Q2 (ชิ้น 2 หมุนทวนเข็ม)
_F = _Q + W3 * _perp_cw(_Q - _B)             # ปลายเวกเตอร์ v_Q3 (ชิ้น 3 หมุนตามเข็ม)

# ตรวจว่าฉายลงเส้น normal ได้ระยะเท่ากันจริง (ถ้าผิดจะพังตั้งแต่ import)
assert abs(float(np.dot(_E - _Q, U)) - _VN) < 1e-9
assert abs(float(np.dot(_F - _Q, U)) - _VN) < 1e-9

# SC: สเกลจาก raw DXF units (หลักร้อย) ลงมาเป็นหน่วยฉาก -- เลือกให้ AB รวม
# (772.38 raw) ออกมา ~4.3 หน่วยฉาก คือขนาดที่โค้งพอดีเฟรม+เหลือที่ให้ป้ายกำกับ
# ใกล้เคียงกับที่โค้งรุ่นก่อน 2026-09-05 เคยพอดีมาก่อนแล้ว (ไม่ใช่ 1/480-1/500
# ตรงๆ ตามตัวเลขคร่าวๆ ที่เคยเสนอไว้ -- ค่านั้นให้ AB แค่ ~1.6 หน่วย เล็กเกินไป
# เทียบกับ arc/formula/legend อื่นในซีนที่ผูกกับสัดส่วนเดิม)
SC = 4.3 / (RAW_PA + RAW_PB)
OFF = np.array([-4.0, -0.55, 0.0]) - SC * np.array([
    (_Q[0] + _S[0]) / 2, (_A[1] + _B[1]) / 2, 0.0])


def xf(p):
    return SC * np.asarray(p, dtype=float) + OFF


A, B, P, Q, R, S, E, F = (xf(p) for p in (_A, _B, _P, _Q, _R, _S, _E, _F))
UN = U                     # ทิศ normal ไม่เปลี่ยนเมื่อสเกล/เลื่อน


# ------------------------------------------------------------------- ตัวช่วยวาด
def seg(p, q, color, w=5):
    return Line(p, q, color=color, stroke_width=w)


def pt(p, color=WHITE, r=0.065):
    return Dot(p, color=color, radius=r)


def tag(txt, p, direction, color=WHITE, size=24, buff=0.16):
    return Text(txt, font_size=size, color=color).next_to(p, direction, buff=buff)


def gap_dir(point, avoid_points):
    """หาทิศจาก point ที่ "ห่างจากทุกทิศในลิสต์ avoid_points มากที่สุด" (ช่องว่าง
    เชิงมุมกว้างสุด) -- ใช้ตอนจุดหนึ่งมีเส้น/ลูกศรหลายเส้นมาบรรจบพร้อมกัน (เช่น Q
    ในซีนนี้ที่มีเส้นออกจากตัวเองถึง 6 ทิศ) ซึ่งการเดาทิศจาก 2 เส้นแล้วหาเส้นแบ่งครึ่ง
    (วิธีเดิม) พลาดเส้นอื่นที่ไม่ได้เอามารวมคำนวณด้วยได้ง่าย (เจอจริงจาก [LAYOUT]
    log 2026-09-05 rebuild หลายรอบติด -- ทิศที่เลี่ยงแค่ 2 เส้นดันขนาน/ใกล้เส้นที่ 3
    ที่ลืมนับ) avoid_points = จุดอ้างอิงจริง (ปลายเส้น/จุดบนเส้นที่ใกล้ point ที่สุด)
    ไม่ใช่เวกเตอร์ทิศ -- ฟังก์ชันคำนวณทิศจาก point เอง"""
    vecs = [np.asarray(pp, float) - np.asarray(point, float) for pp in avoid_points]
    angs = sorted(float(np.degrees(np.arctan2(v[1], v[0])) % 360) for v in vecs)
    n = len(angs)
    best_gap, best_mid = -1.0, 0.0
    for i in range(n):
        a = angs[i]
        b = angs[(i + 1) % n] + (360.0 if i == n - 1 else 0.0)
        gap = b - a
        if gap > best_gap:
            best_gap, best_mid = gap, (a + b) / 2
    rad = (best_mid % 360.0) * DEGREES
    return np.array([np.cos(rad), np.sin(rad), 0.0])


def ra_mark(corner, d1, d2, color=GRAYTXT, size=0.22):
    """เครื่องหมายมุมฉากที่จุด corner ระหว่างทิศ d1 กับ d2"""
    d1 = np.asarray(d1, float) / np.linalg.norm(d1)
    d2 = np.asarray(d2, float) / np.linalg.norm(d2)
    a = corner + d1 * size
    b = corner + d2 * size
    return VMobject().set_points_as_corners(
        [a, a + d2 * size, b]).set_stroke(color, 3)


def frac2(num, den, c_num, c_den, size=34):
    """เศษส่วนที่ระบายสีเศษกับส่วนคนละสีได้ (เลี่ยงการยุ่งกับ substring ของ MathTex)"""
    n = MathTex(num, color=c_num, font_size=size)
    d = MathTex(den, color=c_den, font_size=size)
    bar = Line(LEFT, RIGHT).set_stroke(WHITE, 2.5)
    bar.set_length(max(n.width, d.width) + 0.22)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.15)


def eq_row(*parts, buff=0.22):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def body_arc(center_side, radius, span=52 * DEGREES, color=C_BODY):
    """ผิวโค้งของชิ้นงานที่สัมผัสกันที่ Q — จุดศูนย์กลางความโค้งอยู่บนเส้น normal"""
    c = Q + center_side * radius * UN
    base = np.arctan2(*(Q - c)[1::-1])
    return Arc(radius=radius, start_angle=base - span, angle=2 * span,
               arc_center=c, color=color, stroke_width=3.5)


def ground(p, up=True):
    """สัญลักษณ์จุดหมุนยึดกับพื้น"""
    s = 0.30
    y = 0.16 if up else -0.16
    base = Line(p + LEFT * s + UP * y * 0, p + RIGHT * s, color=METAL, stroke_width=3)
    base.move_to(p + np.array([s * 0.55, 0, 0]))
    ticks = VGroup(*[
        Line(base.get_start() + RIGHT * (i * s * 0.5),
             base.get_start() + RIGHT * (i * s * 0.5) + np.array([-0.13, -0.16, 0]),
             color=METAL, stroke_width=2.5) for i in range(4)])
    return VGroup(base, ticks)


def upright_tri(pa, pb, pc, names, colors, center, height):
    """
    ยกสามเหลี่ยมออกมาวางใหม่ให้ 'ตั้งตรง': ด้าน pa->pb นอนเป็นแนวนอน
    คืน (group, dict ของจุดยอดที่ตำแหน่งใหม่, dict ของด้าน)
    colors = (สี pa->pb, สี pa->pc, สี pb->pc)
    """
    pa, pb, pc = (np.asarray(x, float) for x in (pa, pb, pc))
    th = np.arctan2(*(pb - pa)[1::-1])
    rot = np.array([[np.cos(-th), -np.sin(-th)], [np.sin(-th), np.cos(-th)]])
    loc = [rot @ (p - pa)[:2] for p in (pa, pb, pc)]
    loc = [np.array([v[0], v[1], 0.0]) for v in loc]
    ctr = (np.min(loc, axis=0) + np.max(loc, axis=0)) / 2
    ext = np.max(loc, axis=0) - np.min(loc, axis=0)
    k = height / max(ext[1], 1e-6)
    if ext[0] * k > 4.6:                     # กันล้นความกว้างพาเนล
        k = 4.6 / ext[0]
    va, vb, vc = [(p - ctr) * k + np.asarray(center, float) for p in loc]

    sides = {
        "ab": seg(va, vb, colors[0], 6),
        "ac": seg(va, vc, colors[1], 6),
        "bc": seg(vb, vc, colors[2], 6),
    }
    # ทิศป้ายกำกับ = ออกจากจุดศูนย์ถ่วงของสามเหลี่ยม ผ่านมุมนั้นแล้วออกไปเรื่อยๆ
    # (การันตีว่าไม่มีทางย้อนเข้าไปทับด้านของสามเหลี่ยมตัวเอง ต่างจากสูตรเดิม
    # ที่ผสมทิศขอบ+ทิศเข้าหา c ซึ่งพลิกทิศผิดได้เมื่อรูปทรงเบี้ยว)
    centroid = (va + vb + vc) / 3
    # buff 0.30 (เดิม 0.18) -- แต่ละมุมมีวงเล็บมุม/Angle รัศมี ~0.44 มาวาดทับซ้ำทีหลัง
    # (ang1/ang2/ang3/ang4 ในคลิปที่เรียกใช้ helper นี้) buff เดิมแคบไปหน่อย ทำให้
    # ป้ายชื่อจุดเฉียดขอบ Angle arc ได้ในบางเฟรม
    labels = VGroup(
        tag(names[0], va, normalize(va - centroid), colors[1], 24, 0.30),
        tag(names[1], vb, normalize(vb - centroid), colors[0], 24, 0.30),
        tag(names[2], vc, normalize(vc - centroid), colors[2], 24, 0.30),
    )
    dots = VGroup(pt(va, WHITE, 0.055), pt(vb, WHITE, 0.055), pt(vc, WHITE, 0.055))
    g = VGroup(sides["ab"], sides["ac"], sides["bc"], dots, labels)
    return g, {"a": va, "b": vb, "c": vc}, sides


# =====================================================================
# ซีน 1 — หน้า 5 (1/2): วาดทีละจุด ทีละเส้น
# =====================================================================
class G05A_PointsAndLines(SafeScene):
    def construct(self):
        self.add(title("วาดทีละจุด ทีละเส้น", size=30))
        self.add(page_ref("หน้า 5 · Law of Gearing"))

        cap = caption_top("สองชิ้นงานหมุนคนละแกน มาแตะกันที่จุดเดียว", size=23)
        self.play(FadeIn(cap))

        # --- ผิวสัมผัสของสองชิ้น -------------------------------------------
        # รัศมีโค้ง (ตกแต่ง แสดงผิวชิ้นงาน ไม่ใช่ค่าจากตารางจุดที่ยืนยัน) คงสัดส่วน
        # เดิมเทียบกับ AB span เก่า (รัศมี/AB = 1.17/4.53, 0.945/4.53) มาปรับกับ
        # AB span ใหม่ (4.3) เดิม SC=0.90 คูณตรงๆ ใช้ไม่ได้แล้วเพราะ SC ตอนนี้
        # หมายถึงสเกล raw-DXF->ฉาก (เล็กมาก ~1/180) คนละความหมายกับ SC เดิม
        ARC2_R = 1.11
        ARC3_R = 0.90
        arc2 = body_arc(-1, ARC2_R)
        arc3 = body_arc(+1, ARC3_R)
        lb2 = tag("ชิ้นที่ 2", arc2.point_from_proportion(0.06), LEFT, C_BODY, 20)
        # RIGHT เดิมพาป้ายข้ามเส้น line of centers (loc อยู่ที่ x=OFF[0], จุดยึด
        # ของ arc3 ที่มุมนี้อยู่ทางซ้ายของ loc ไปแล้วเพราะ PHI ใหม่ชันกว่าเดิมมาก
        # (42° เทียบ 20°) -- เจอจริงจาก [LAYOUT] log 2026-09-05 rebuild
        # (ทับ DashedLine) เปลี่ยนเป็น LEFT (ทิศออกจากศูนย์กลางส่วนโค้งเอง ตรงข้าม
        # กับ loc แน่นอน)
        lb3 = tag("ชิ้นที่ 3", arc3.point_from_proportion(0.94), LEFT, C_BODY, 20)
        self.play(Create(arc2), Create(arc3), FadeIn(lb2), FadeIn(lb3), run_time=1.4)
        self.wait(0.6)

        # --- A -------------------------------------------------------------
        cap2 = caption_top("จุด A คือแกนหมุนของชิ้นที่ 2", size=23)
        dA, tA = pt(A, C_AQ, 0.085), tag("A", A, UP, C_AQ, 26)
        gA = ground(A)
        self.play(FadeOut(cap))
        self.play(FadeIn(cap2), FadeIn(dA), FadeIn(tA), Create(gA))
        self.wait(0.7)

        # --- B -------------------------------------------------------------
        cap3 = caption_top("จุด B คือแกนหมุนของชิ้นที่ 3", size=23)
        dB, tB = pt(B, C_BQ, 0.085), tag("B", B, DOWN, C_BQ, 26)
        gB = ground(B)
        self.play(FadeOut(cap2))
        self.play(FadeIn(cap3), FadeIn(dB), FadeIn(tB), Create(gB))
        self.wait(0.7)

        # --- line of centers ------------------------------------------------
        cap4 = caption_top("ลากเส้นเชื่อมสองแกนหมุน = line of centers", size=23)
        loc = DashedLine(A, B, color=C_LOC, stroke_width=3, dash_length=0.13)
        # แปะป้ายใกล้ B (t=0.72) แทนกึ่งกลางหรือใกล้ A -- ทั้งสองจุดนั้นมีเส้น/จุดอื่น
        # (l_AR, dots ต่างๆ) มาพาดทับป้ายที่ค้างอยู่ทั้งคลิป (เจอจริงจาก [LAYOUT] log
        # 2026-09-05: ทับทั้ง Dot และ DashedLine) -- buff ก็เพิ่มเป็น 0.5 กันชนเผื่อ
        # 0.72 (ใกล้ B) ตอนนี้ไปชนป้าย "BS" ที่เพิ่งย้ายมาทาง RIGHT ใกล้ B เหมือนกัน
        # (เจอจริงจาก [LAYOUT] log 2026-09-05: 'lineofcenters'<->'BS' ทับกัน 47%)
        # ย้ายไปใกล้ A แทน (t=0.28, ไกลจากทั้งคลัสเตอร์ B/S/R/Q ตรงกลาง-ล่าง)
        t_loc = tag("line of centers", A + (B - A) * 0.28, RIGHT, C_LOC, 17, 0.5)
        self.play(FadeOut(cap3))
        self.play(FadeIn(cap4), Create(loc), FadeIn(t_loc))
        self.wait(0.8)

        # --- Q ---------------------------------------------------------------
        cap5 = caption_top("จุด Q คือจุดที่ผิวสองชิ้นแตะกัน", size=23)
        # Q ค้างอยู่บนจอทั้งซีน มีเส้นที่ออกจากตัว Q เองพาดผ่านถึง 6 ทิศ (ไป A, ไป B,
        # เส้น normal 2 ทาง (+U/-U, สั้นและยาว), ลูกศรไป E, ลูกศรไป F) -- ลอง UL
        # (รอบแรก) แล้ว UP (รอบสอง) แล้วค่าเฉลี่ยจาก A/B แค่ 2 ทิศ (รอบสาม) ก็ยังชน
        # ทุกรอบเพราะลืมนับเส้น normal ทั้งสองทาง (เจอจริงจากเฟรมจริง: 'Q' ทับเส้น
        # contact normal เห็นชัดในภาพ) ใช้ gap_dir() คำนวณจากทั้ง 6 ทิศพร้อมกัน
        _tQdir = gap_dir(Q, [A, B, E, F, Q + UN, Q - UN])
        dQ, tQ = pt(Q, WHITE, 0.09), tag("Q", Q, _tQdir, WHITE, 26, 0.22)
        self.play(FadeOut(cap4))
        self.play(FadeIn(cap5), FadeIn(dQ), FadeIn(tQ), Flash(Q, color=WHITE))
        self.wait(0.7)

        # --- contact normal ---------------------------------------------------
        cap6 = caption_top("ที่ Q ลากเส้นตั้งฉากกับผิวสัมผัส = contact normal", size=23)
        n_line = Line(Q - UN * 1.05, Q + UN * 3.30, color=C_NORM, stroke_width=4)
        t_n = tag("contact normal", n_line.get_end(), DR, C_NORM, 19, 0.12)
        self.play(FadeOut(cap5))
        self.play(FadeIn(cap6), Create(n_line), FadeIn(t_n), run_time=1.3)
        self.wait(0.8)
        self.play(FadeOut(lb2), FadeOut(lb3), FadeOut(arc2), FadeOut(arc3))

        # --- AQ + w2 ----------------------------------------------------------
        cap7 = caption_top("AQ = แขนรัศมีของชิ้นที่ 2 (จากแกน A ถึงจุดสัมผัส)", size=22)
        l_AQ = seg(A, Q, C_AQ, 5)
        t_AQ = tag("AQ", (A + Q) / 2, LEFT, C_AQ, 22, 0.12)
        f_w2 = eq_row(MathTex(r"\omega_2", font_size=34, color=C_AQ),
                      MathTex("=", font_size=34),
                      frac2("v_{Q_2}", "AQ", C_VQ2, C_AQ)).move_to([3.1, 1.60, 0])
        self.play(FadeOut(cap6))
        self.play(FadeIn(cap7), Create(l_AQ), FadeIn(t_AQ))
        self.play(FadeIn(f_w2))
        self.wait(0.8)

        # --- v_Q2 -> E ---------------------------------------------------------
        cap8 = caption_top("ความเร็วของ Q บนชิ้นที่ 2 ตั้งฉากกับ AQ · ปลายลูกศรคือจุด E", size=22)
        a_v2 = Arrow(Q, E, buff=0, color=C_VQ2, stroke_width=5,
                     max_tip_length_to_length_ratio=0.13)
        t_v2 = MathTex("v_{Q_2}", font_size=26, color=C_VQ2).next_to(a_v2.get_center(), DL, buff=0.10)
        # E, P, F เรียงเส้นตรงเดียวกันจริง -- ไม่ใช่บังเอิญ แต่เป็นผลพีชคณิตที่
        # หลีกเลี่ยงไม่ได้ของสูตร (dot(E-P,U)=dot(F-P,U)=0 เสมอ เพราะ E และ F ต่าง
        # ก็ฉายตั้งฉากลงเส้น normal ที่จุด P เดียวกันโดยนิยาม) ผลคือ P อยู่ที่มุม
        # ±90° จาก U พอดีเป๊ะเมื่อมองจาก E -- ลองหาทิศ "เลี่ยง P กับ F" มาแล้วสองวิธี
        # (ตั้งฉากกับ E-P ตรงๆ, ทิศกึ่งกลางระหว่างสองเส้น) ทั้งคู่ดันคำนวณกลับไปขนาน
        # กับ U (เส้น normal) พอดีทุกครั้ง เพราะ P/F สมมาตรรอบแกนตั้งฉากกับ U อยู่แล้ว
        # (เจอจริงจาก [LAYOUT] log ทั้งสองรอบ: ชน n_line ซ้ำ) ทางออกจริงคือเปลี่ยน
        # วิธีคิดใหม่ทั้งหมด: ไม่ต้องเลี่ยง P/F -- ป้ายปลายลูกศร a_v2 ควรอยู่ "ต่อ
        # จากหัวลูกศรไปทางเดิม" (ทิศเดียวกับที่ลูกศรวิ่งมา Q->E) ซึ่งเป็นวิธีมาตรฐาน
        # ของการติดป้ายที่ปลายลูกศร และพิสูจน์แล้วว่าห่างจาก P/F/Q/a_v3 ทุกตัว
        # อย่างน้อย ~63° (ตรวจด้วยเลขจริงจากพิกัดสุดท้าย)
        dE, tE = pt(E, C_VQ2, 0.075), tag("E", E, normalize(E - Q), C_VQ2, 24, 0.16)
        ra2 = ra_mark(Q, A - Q, E - Q, C_VQ2)
        self.play(FadeOut(cap7))
        self.play(FadeIn(cap8), GrowArrow(a_v2), FadeIn(t_v2), Create(ra2))
        self.play(FadeIn(dE), FadeIn(tE))
        self.wait(0.8)

        # --- BQ + w3 -----------------------------------------------------------
        cap9 = caption_top("BQ = แขนรัศมีของชิ้นที่ 3 (จากแกน B ถึงจุดสัมผัสจุดเดียวกัน)", size=22)
        l_BQ = seg(B, Q, C_BQ, 5)
        # จุดนี้อยู่ซ้ายของเส้น line of centers (x คงที่ที่ B) -- ป้ายต้องชี้ LEFT
        # (ออกห่างจากเส้น) ไม่ใช่ RIGHT (จะแกว่งกลับไปทับเส้น line of centers)
        t_BQ = tag("BQ", B + (Q - B) * 0.42, LEFT, C_BQ, 22, 0.18)
        f_w3 = eq_row(MathTex(r"\omega_3", font_size=34, color=C_BQ),
                      MathTex("=", font_size=34),
                      frac2("v_{Q_3}", "BQ", C_VQ3, C_BQ)).move_to([3.1, 0.05, 0])
        self.play(FadeOut(cap8))
        self.play(FadeIn(cap9), Create(l_BQ), FadeIn(t_BQ))
        self.play(FadeIn(f_w3))
        self.wait(0.8)

        # --- v_Q3 -> F ----------------------------------------------------------
        cap10 = caption_top("ความเร็วของ Q บนชิ้นที่ 3 ตั้งฉากกับ BQ · ปลายลูกศรคือจุด F", size=22)
        a_v3 = Arrow(Q, F, buff=0, color=C_VQ3, stroke_width=5,
                     max_tip_length_to_length_ratio=0.13)
        # UL เดิมพาป้ายไปทับ "AQ" ที่ยังค้างอยู่ใกล้ Q (เจอจริงจาก Gemini frame review
        # 2026-09-05 -- ไม่ถูกจับโดย [LAYOUT] linter อัตโนมัติ) เปลี่ยนเป็น DR (ทิศตาม
        # แขน a_v3 เอง ไปทาง F/B ซึ่งอยู่คนละฝั่งกับ A)
        t_v3 = MathTex("v_{Q_3}", font_size=26, color=C_VQ3).next_to(a_v3.get_center(), DR, buff=0.12)
        # ปัญหาโครงสร้างเดียวกับ E ข้างบน (F-P ตั้งฉากกับ U เสมอด้วยเหตุผลเดียวกัน)
        # ใช้วิธีแก้เดียวกัน: ป้ายต่อจากหัวลูกศร a_v3 ไปทางเดิม (ทิศ Q->F)
        dF, tF = pt(F, C_VQ3, 0.075), tag("F", F, normalize(F - Q), C_VQ3, 24, 0.16)
        ra3 = ra_mark(Q, B - Q, F - Q, C_VQ3)
        self.play(FadeOut(cap9))
        self.play(FadeIn(cap10), GrowArrow(a_v3), FadeIn(t_v3), Create(ra3))
        self.play(FadeIn(dF), FadeIn(tF))
        self.wait(0.8)

        # --- หัวใจ: ฉาย E และ F ลงเส้น normal ได้จุดเดียวกัน = P ------------------
        cap11 = caption_top("ลากฉากจาก E ลงเส้น normal", size=23)
        pr_E = DashedLine(E, P, color=C_TAN, stroke_width=3, dash_length=0.10)
        self.play(FadeOut(cap10))
        self.play(FadeIn(cap11), Create(pr_E))
        self.wait(0.5)

        cap12 = caption_top("ลากฉากจาก F ลงเส้น normal — ตกที่จุดเดิม!", size=23)
        pr_F = DashedLine(F, P, color=C_TAN, stroke_width=3, dash_length=0.10)
        dP, tP = pt(P, C_VN, 0.10), tag("P", P, DR, C_VN, 26, 0.13)
        self.play(FadeOut(cap11))
        self.play(FadeIn(cap12), Create(pr_F))
        self.play(FadeIn(dP), FadeIn(tP), Flash(P, color=C_VN, flash_radius=0.45))
        self.wait(0.8)

        cap13 = caption_top("QP คือองค์ประกอบตามแนว normal — สองชิ้นต้องเท่ากัน ไม่งั้นจะแทรกกัน", size=21)
        l_QP = seg(Q, P, C_VN, 8)
        # ไม่ใส่ป้าย "QP" แยก — R อยู่บนเส้น QP พอดี (Q,R,P เรียงกันบนเส้น normal)
        # ป้ายใดๆ บนเส้นนี้จะชนจุด R/เครื่องหมายมุมฉากที่ R เกือบแน่นอน
        self.play(FadeOut(cap12))
        self.play(FadeIn(cap13), Create(l_QP))
        self.wait(1.0)
        # เพิ่ม t_AQ เข้าไปในชุดที่เอาออก -- ป้าย "AQ" ที่ค้างอยู่ใกล้ (A+Q)/2 ไปชนกับ
        # ป้าย "AR" ที่กำลังจะโผล่ในโซนเดียวกัน (เจอจริงจาก [LAYOUT] log 2026-09-05,
        # ยังทับซ้ำแม้ขยับตำแหน่ง AR แล้ว) AQ ได้ทำหน้าที่ของมันจบไปแล้วตอนนี้ (v_Q2/w2
        # อธิบายไปแล้ว) เอาออกตรงนี้ปลอดภัยกว่าสู้แย่งพื้นที่ต่อ -- คงเส้น l_AQ ไว้
        # (ให้บริบทภาพว่า R มาจากไหน) เอาออกแค่ตัวหนังสือ
        self.play(FadeOut(pr_E), FadeOut(pr_F), FadeOut(a_v2), FadeOut(a_v3),
                  FadeOut(t_v2), FadeOut(t_v3), FadeOut(ra2), FadeOut(ra3),
                  FadeOut(f_w2), FadeOut(f_w3), FadeOut(t_AQ))

        # --- R ------------------------------------------------------------------
        cap14 = caption_top("จาก A ลากฉากลงเส้น normal — เท้าของฉากคือจุด R", size=22)
        l_AR = seg(A, R, C_AR, 5)
        # R มีเส้นหลายเส้นมาบรรจบ (l_AR เกือบขนานแนวดิ่ง, เส้น normal เกือบแนวนอน) --
        # ป้ายต้องชี้ทแยงออกจากทั้งคู่ (down-left) ไม่ใช่ DOWN ตรงๆ ซึ่งเกือบขนาน l_AR
        dR, tR = pt(R, C_AR, 0.075), tag("R", R, DL, C_AR, 20, 0.22)
        # ทิศของป้าย AR: ตั้งฉากกับเส้น A-R เอง (ไม่ใช่ UP ซึ่งเกือบขนานกับเส้นนั้น)
        _ar_perp = np.array([(R - A)[1], -(R - A)[0], 0.0])
        _ar_perp = _ar_perp / np.linalg.norm(_ar_perp)
        # กลับมาใช้ 0.45 (กึ่งกลาง A-R, ไกลจาก R/เส้น normal ที่แน่นกว่า) -- รอบก่อนขยับ
        # เข้าใกล้ R (0.68) กลับแย่ลง (ทับ Line ด้วย) เพราะ _ar_perp ขนานกับเส้น normal
        # เอง (AR ตั้งฉากกับเส้น normal โดยนิยาม) ยิ่งเข้าใกล้ R ยิ่งเสี่ยงชนของบนเส้นนั้น
        # -- fix จริงคือเอา t_AQ ออกไปแล้ว (ดูด้านบน) ไม่ต้องเสี่ยงต่อสู้พื้นที่ตรงนี้อีก
        t_AR = tag("AR", A + (R - A) * 0.45, _ar_perp, C_AR, 20, 0.22)
        raR = ra_mark(R, A - R, Q - R, C_AR)
        self.play(FadeOut(cap13))
        self.play(FadeIn(cap14), Create(l_AR), FadeIn(t_AR))
        self.play(FadeIn(dR), FadeIn(tR), Create(raR))
        self.wait(0.9)

        # --- S ------------------------------------------------------------------
        cap15 = caption_top("จาก B ลากฉากลงเส้น normal — เท้าของฉากคือจุด S", size=22)
        l_BS = seg(B, S, C_BS, 5)
        dS, tS = pt(S, C_BS, 0.075), tag("S", S, UR, C_BS, 20, 0.10)
        # buff เพิ่มเป็น 0.32 ไม่พอ -- คำนวณดูแล้วจุดยึด (กึ่งกลาง B-S) อยู่ที่ x=-3.43
        # ซึ่ง "ทางขวา" ของเส้น loc (x=-3.93 คงที่ตลอดแนว) ทิศ LEFT เดิมจึงพาป้ายข้าม
        # เส้น loc เสมอไม่ว่า buff จะเท่าไหร่ (เจอจริงจาก [LAYOUT] log 2026-09-05 ซ้ำ
        # หลังแก้รอบแรก) แก้ทิศเป็น RIGHT แทน (ตรงข้าม ห่างจาก loc แน่นอน)
        t_BS = tag("BS", B + (S - B) * 0.50, RIGHT, C_BS, 22, 0.2)
        raS = ra_mark(S, B - S, Q - S, C_BS)
        self.play(FadeOut(cap14))
        self.play(FadeIn(cap15), Create(l_BS), FadeIn(t_BS))
        self.play(FadeIn(dS), FadeIn(tS), Create(raS))
        self.wait(0.9)

        # --- สรุปจุดทั้งหมด ---------------------------------------------------------
        cap16 = caption_top("ครบแล้ว 8 จุด — คลิปหน้าเอาไปประกอบเป็นสามเหลี่ยม", size=23)
        legend = VGroup(
            Text("A, B = แกนหมุน", font_size=21, color=GRAYTXT),
            Text("Q = จุดสัมผัส", font_size=21, color=WHITE),
            Text("E, F = ปลายเวกเตอร์ความเร็ว", font_size=21, color=C_VQ2),
            Text("P = จุดฉายร่วมบนเส้น normal", font_size=21, color=C_VN),
            Text("R, S = เท้าของฉากจาก A และ B", font_size=21, color=C_AR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([3.0, 0.30, 0])
        self.play(FadeOut(cap15))
        self.play(FadeIn(cap16), FadeIn(legend, shift=UP * 0.2))
        self.wait(2.4)


# =====================================================================
# ซีน 2 — หน้า 5 (2/2): สามเหลี่ยมคล้าย 2 คู่
# =====================================================================
class G05B_SimilarTriangles(SafeScene):
    def base_figure(self):
        """รูปพื้นหลังแบบจาง ๆ ไว้อ้างอิงตำแหน่ง"""
        g = VGroup(
            DashedLine(A, B, color=C_LOC, stroke_width=2.5, dash_length=0.13),
            Line(Q - UN * 1.0, Q + UN * 3.2, color=C_NORM, stroke_width=3),
            seg(A, Q, C_AQ, 3), seg(B, Q, C_BQ, 3),
            seg(A, R, C_AR, 3), seg(B, S, C_BS, 3),
            seg(Q, E, C_VQ2, 3), seg(Q, F, C_VQ3, 3),
            seg(Q, P, C_VN, 4),
        )
        dots = VGroup(*[pt(p, c, 0.06) for p, c in
                        ((A, C_AQ), (B, C_BQ), (Q, WHITE), (P, C_VN),
                         (R, C_AR), (S, C_BS), (E, C_VQ2), (F, C_VQ3))])
        # ไม่ใส่ป้ายชื่อจุดที่นี่ — R/P/Q/E/F อยู่ใกล้กันมากจนป้ายชนกันแน่นอน
        # (เห็นชื่อครบแล้วจากคลิปก่อนหน้า และแต่ละสามเหลี่ยมที่ดึงออกมาขยาย
        # ด้านล่างนี้ก็มีป้ายกำกับจุดยอดของตัวเองชัดเจนอยู่แล้ว)
        return VGroup(g, dots)

    def construct(self):
        self.add(title("สามเหลี่ยมคล้ายอยู่ตรงไหน", size=30))
        self.add(page_ref("หน้า 5 · Law of Gearing"))

        fig = self.base_figure()
        self.play(FadeIn(fig), run_time=1.2)
        cap = caption_top("รูปเดิมจากคลิปที่แล้ว — คราวนี้ดึงสามเหลี่ยมออกมาทีละรูป", size=22)
        self.play(FadeIn(cap))
        self.wait(1.0)

        # ---------------- คู่ที่ 1 : สามเหลี่ยมของชิ้นที่ 2 -----------------------
        cap = self.swap_cap(cap, "รูปที่ 1 — สามเหลี่ยมความเร็วของชิ้นที่ 2: Q, E, P")
        tri1_in = Polygon(Q, E, P, color=C_VQ2, fill_opacity=0.30, stroke_width=4)
        self.play(FadeIn(tri1_in))
        self.wait(0.7)

        g1, v1, s1 = upright_tri(Q, P, E, ("Q", "P", "E"),
                                 (C_VN, C_VQ2, C_TAN), [2.2, 1.35, 0], 1.30)
        # FadeOut+FadeIn แทน TransformFromCopy — Polygon (1 ชิ้น) กับกลุ่มที่มี
        # เส้น 3 เส้น+จุด 3 จุด+ป้าย 3 ป้าย (9 ชิ้น) โครงสร้างไม่ตรงกัน manim จะ
        # จับคู่แบบเบี้ยว ทำให้ป้ายกลายเป็นรูปเปื้อนวิ่งผ่านตำแหน่งเดิมกลางอากาศ
        self.play(FadeOut(tri1_in))
        self.play(FadeIn(g1, shift=RIGHT * 0.3), run_time=1.0)
        # วางไว้ใต้สามเหลี่ยม ไม่ใช่ด้านขวา -- สามเหลี่ยมกว้างได้ถึง 4.6 หน่วยที่ x=2.2
        # ป้ายด้านขวายาว ๆ จะยื่นเลยขอบเฟรมขวา (X_MAX=7.11) ไปไกล
        note1 = VGroup(
            Text("QE = ความเร็ว v_Q2", font_size=18, color=C_VQ2),
            Text("QP = องค์ประกอบตามแนว normal", font_size=18, color=C_VN),
            Text("PE = ส่วนที่ลื่นไถลไปตามผิว", font_size=18, color=C_TAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g1, DOWN, buff=0.4)
        self.play(FadeIn(note1, shift=DOWN * 0.15))
        self.wait(2.2)
        self.play(FadeOut(note1))

        # ---------------- รูปที่ 2 : สามเหลี่ยมรูปทรงของชิ้นที่ 2 ------------------
        cap = self.swap_cap(cap, "รูปที่ 2 — สามเหลี่ยมรูปทรงของชิ้นที่ 2: A, R, Q")
        tri2_in = Polygon(A, R, Q, color=C_AQ, fill_opacity=0.30, stroke_width=4)
        self.play(FadeOut(tri1_in), FadeIn(tri2_in))
        self.wait(0.7)

        g2, v2, s2 = upright_tri(A, R, Q, ("A", "R", "Q"),
                                 (C_AR, C_AQ, C_TAN), [2.2, -1.35, 0], 1.30)
        self.play(FadeOut(tri2_in))
        self.play(FadeIn(g2, shift=RIGHT * 0.3), run_time=1.0)
        note2 = VGroup(
            Text("AQ = แขนรัศมีถึงจุดสัมผัส", font_size=18, color=C_AQ),
            Text("AR = ระยะตั้งฉากจาก A ลงเส้น normal", font_size=18, color=C_AR),
            Text("RQ = ระยะบนเส้น normal", font_size=18, color=C_TAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g2, DOWN, buff=0.4)
        self.play(FadeIn(note2, shift=DOWN * 0.15))
        self.wait(2.2)

        # ---------------- ทำไมสองรูปนี้ถึง "คล้ายกัน" --------------------------
        # เหตุผลจริง (AA): มีมุมฉากทั้งคู่ + อีกหนึ่งมุมเท่ากัน = 90° - alpha
        cap = self.swap_cap(cap, "แล้วสองรูปนี้คล้ายกันได้ยังไง? พิสูจน์ทีละขั้น", size=23)
        self.play(FadeOut(note2))
        self.wait(0.5)

        # ขั้น 1 — มุมฉากทั้งคู่
        cap = self.swap_cap(cap, "ขั้น 1: ทั้งสองรูปมีมุมฉาก (ที่ P และที่ R)", size=23)
        raq1 = ra_mark(v1["b"], v1["a"] - v1["b"], v1["c"] - v1["b"], C_VN, 0.24)
        raq2 = ra_mark(v2["b"], v2["a"] - v2["b"], v2["c"] - v2["b"], C_AR, 0.24)
        self.play(Create(raq1), Create(raq2))
        self.wait(1.6)

        # ขั้น 2 — นิยาม alpha บนรูปจริง
        cap = self.swap_cap(cap, "ขั้น 2: ให้ α = มุมระหว่างแขน AQ กับเส้น normal", size=23)
        ang_a = Angle(Line(Q, R), Line(Q, A), radius=0.48, color=WARN, stroke_width=4)
        lb_a = MathTex(r"\alpha", font_size=30, color=WARN).move_to(
            Q + normalize(normalize(R - Q) + normalize(A - Q)) * 0.72)
        self.play(Create(ang_a), FadeIn(lb_a))
        self.wait(1.6)

        # ขั้น 3 — มุมที่ A ในสามเหลี่ยมรูปทรง
        cap = self.swap_cap(cap, "ขั้น 3: ใน A-R-Q มุมที่ Q คือ α → มุมที่ A ต้องเป็น 90° − α", size=22)
        # radius เดิม 0.44 > buff ป้ายชื่อจุดยอด (upright_tri ใช้ 0.30) -- ทำให้ส่วนโค้ง
        # มุมไปทับป้าย "A" ได้ (เจอจริงจาก [LAYOUT] log 2026-09-05) ลดเหลือ 0.24 ให้ต่ำกว่า buff
        ang2 = Angle(s2["ab"], s2["ac"], radius=0.24, color=WARN, stroke_width=4)
        lb2a = MathTex(r"90^\circ-\alpha", font_size=24, color=WARN).next_to(
            v2["a"], UR, buff=0.30)
        self.play(Create(ang2), FadeIn(lb2a))
        self.wait(2.0)

        # ขั้น 4 — มุมที่ Q ในสามเหลี่ยมความเร็ว: ได้ 90 - alpha เหมือนกัน
        cap = self.swap_cap(cap, "ขั้น 4: v_Q2 ตั้งฉากกับ AQ → มุมที่ Q ในรูปความเร็วก็ 90° − α", size=22)
        # เหตุผลเดียวกับ ang2 ข้างบน -- ลด radius ให้ต่ำกว่า buff ป้ายชื่อจุดยอด (0.30)
        ang1 = Angle(s1["ab"], s1["ac"], radius=0.24, color=WARN, stroke_width=4)
        lb1a = MathTex(r"90^\circ-\alpha", font_size=24, color=WARN).next_to(
            v1["a"], UR, buff=0.30)
        self.play(Create(ang1), FadeIn(lb1a))
        self.wait(2.2)

        # ขั้น 5 — สรุป AA
        cap = self.swap_cap(cap, "มุมฉากตรงกัน + อีกมุมตรงกัน = คล้ายกันแน่นอน (แบบ มุม-มุม)", size=22)
        # scale_factor=1.0: เน้นด้วยสี ไม่ขยายขนาด -- กันไม่ให้มุม/ป้ายขยายเข้าไปชน
        # โซนคำบรรยายบนที่เพิ่งขึ้นบรรทัดนี้
        self.play(Indicate(VGroup(raq1, raq2), color=OK, scale_factor=1.0))
        self.play(Indicate(VGroup(ang1, ang2, lb1a, lb2a), color=OK, scale_factor=1.0))
        self.wait(1.4)

        cap = self.swap_cap(cap, "ด้านที่คู่กันจึงเป็นสัดส่วนกัน: QE คู่ AQ · QP คู่ AR", size=22)
        eq1 = eq_row(frac2("EQ", "PQ", C_VQ2, C_VN),
                     MathTex("=", font_size=34),
                     frac2("AQ", "AR", C_AQ, C_AR)).move_to([2.2, -3.15, 0])
        self.play(FadeIn(eq1, shift=UP * 0.2))
        self.wait(2.4)

        self.play(FadeOut(g1), FadeOut(g2), FadeOut(ang1), FadeOut(ang2),
                  FadeOut(lb1a), FadeOut(lb2a), FadeOut(raq1), FadeOut(raq2),
                  FadeOut(ang_a), FadeOut(lb_a), FadeOut(tri2_in), FadeOut(eq1))

        # ---------------- คู่ที่ 2 : ชิ้นที่ 3 ---------------------------------------
        cap = self.swap_cap(cap, "รูปที่ 3 — สามเหลี่ยมความเร็วของชิ้นที่ 3: Q, F, P")
        tri3_in = Polygon(Q, F, P, color=C_VQ3, fill_opacity=0.30, stroke_width=4)
        self.play(FadeIn(tri3_in))
        self.wait(0.6)
        g3, v3, s3 = upright_tri(Q, P, F, ("Q", "P", "F"),
                                 (C_VN, C_VQ3, C_TAN), [2.2, 1.35, 0], 1.30)
        self.play(FadeOut(tri3_in))
        self.play(FadeIn(g3, shift=RIGHT * 0.3), run_time=1.0)
        note3 = VGroup(
            Text("QF = ความเร็ว v_Q3", font_size=18, color=C_VQ3),
            Text("QP = ตัวเดิม! เท่ากับของชิ้นที่ 2", font_size=18, color=C_VN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g3, DOWN, buff=0.4)
        self.play(FadeIn(note3, shift=DOWN * 0.15))
        self.wait(2.0)
        self.play(FadeOut(note3))

        cap = self.swap_cap(cap, "รูปที่ 4 — สามเหลี่ยมรูปทรงของชิ้นที่ 3: B, S, Q")
        tri4_in = Polygon(B, S, Q, color=C_BQ, fill_opacity=0.30, stroke_width=4)
        self.play(FadeOut(tri3_in), FadeIn(tri4_in))
        self.wait(0.6)
        g4, v4, s4 = upright_tri(B, S, Q, ("B", "S", "Q"),
                                 (C_BS, C_BQ, C_TAN), [2.2, -1.35, 0], 1.30)
        self.play(FadeOut(tri4_in))
        self.play(FadeIn(g4, shift=RIGHT * 0.3), run_time=1.0)
        note4 = VGroup(
            Text("BQ = แขนรัศมีถึงจุดสัมผัส", font_size=18, color=C_BQ),
            Text("BS = ระยะตั้งฉากจาก B ลงเส้น normal", font_size=18, color=C_BS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g4, DOWN, buff=0.4)
        self.play(FadeIn(note4, shift=DOWN * 0.15))
        self.wait(2.0)

        # เหตุผลเดียวกับคู่แรก แค่เปลี่ยนจาก alpha เป็น beta
        cap = self.swap_cap(cap, "เหตุผลเดียวกับคู่แรก: ให้ β = มุมระหว่างแขน BQ กับเส้น normal", size=22)
        self.play(FadeOut(note4))
        ang_b = Angle(Line(Q, B), Line(Q, S), radius=0.48, color=WARN, stroke_width=4)
        lb_b = MathTex(r"\beta", font_size=30, color=WARN).move_to(
            Q + normalize(normalize(B - Q) + normalize(S - Q)) * 0.78)
        self.play(Create(ang_b), FadeIn(lb_b))
        self.wait(1.5)

        cap = self.swap_cap(cap, "มุมฉากที่ P และที่ S · อีกมุมเป็น 90° − β ทั้งคู่ → คล้ายกัน", size=22)
        rb1 = ra_mark(v3["b"], v3["a"] - v3["b"], v3["c"] - v3["b"], C_VN, 0.24)
        rb2 = ra_mark(v4["b"], v4["a"] - v4["b"], v4["c"] - v4["b"], C_BS, 0.24)
        ang3 = Angle(s3["ab"], s3["ac"], radius=0.44, color=WARN, stroke_width=4)
        ang4 = Angle(s4["ab"], s4["ac"], radius=0.44, color=WARN, stroke_width=4)
        self.play(Create(rb1), Create(rb2))
        self.play(Create(ang3), Create(ang4))
        self.wait(2.0)

        eq2 = eq_row(frac2("FQ", "PQ", C_VQ3, C_VN),
                     MathTex("=", font_size=34),
                     frac2("BQ", "BS", C_BQ, C_BS)).move_to([2.2, -3.15, 0])
        self.play(FadeIn(eq2, shift=UP * 0.2))
        self.wait(2.2)
        self.play(FadeOut(ang_b), FadeOut(lb_b), FadeOut(rb1), FadeOut(rb2),
                  FadeOut(ang3), FadeOut(ang4))

        # ---------------- รวมสองสมการ ----------------------------------------------
        self.play(FadeOut(g3), FadeOut(g4), FadeOut(tri4_in), FadeOut(eq2), FadeOut(fig))
        cap = self.swap_cap(cap, "เอาสองคู่มารวมกัน — v_n ตัวร่วมหายไป เหลือแค่ BS กับ AR", size=22)

        chain = VGroup(
            eq_row(frac2(r"\omega_2", r"\omega_3", C_AQ, C_BQ),
                   MathTex("=", font_size=34),
                   frac2("EQ", "AQ", C_VQ2, C_AQ),
                   frac2("BQ", "FQ", C_BQ, C_VQ3)),
            eq_row(MathTex("=", font_size=34),
                   frac2("PQ", "AR", C_VN, C_AR),
                   frac2("BS", "PQ", C_BS, C_VN)),
            eq_row(MathTex("=", font_size=38),
                   frac2("BS", "AR", C_BS, C_AR, size=40)),
        ).arrange(DOWN, buff=0.55).move_to([0, -0.35, 0])
        for row in chain:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.9)
            self.wait(1.1)

        box = SurroundingRectangle(chain[2], color=OK, buff=0.22, stroke_width=4)
        self.play(Create(box))
        self.wait(2.6)

    def swap_cap(self, old, txt, size=22):
        self.play(FadeOut(old))
        new = caption_top(txt, size=size)
        self.play(FadeIn(new))
        return new


# =====================================================================
# ซีน 3 — หน้า 6: จุด P บนเส้นศูนย์กลาง
# =====================================================================
class G06_PitchPoint(SafeScene):
    def construct(self):
        self.add(title("จุด P บนเส้นศูนย์กลาง", size=30))
        self.add(page_ref("หน้า 6 · Law of Gearing"))

        loc = DashedLine(A, B, color=C_LOC, stroke_width=3, dash_length=0.13)
        n_line = Line(Q - UN * 1.0, Q + UN * 3.2, color=C_NORM, stroke_width=4)
        # R มีเส้นหลายเส้น+รูปสามเหลี่ยม (t_APR วาดทีหลัง) มาบรรจบ -- ป้าย "R"/"AR"
        # ต้องชี้ทแยงออกจากกลุ่มเส้น ไม่ใช่ DOWN/UP ตรงๆ (เกือบขนานกับเส้น A-R เอง)
        _ar_perp6 = np.array([(R - A)[1], -(R - A)[0], 0.0])
        _ar_perp6 = _ar_perp6 / np.linalg.norm(_ar_perp6)
        # R, P (และ S, Q) ทั้งหมดอยู่ "บนเส้น normal เดียวกัน" (n_line) โดยนิยาม -- แก้
        # ครั้งแรกด้วย -UN/+UN นั้นยังผิดอยู่ดี เพราะ UN *คือ* ทิศของเส้น normal เอง
        # (แค่งงว่าไปคำนวณแล้วดันตรงกับทิศ R->P พอดี เพราะ R,P colinear บนเส้นนั้น) --
        # ป้ายที่ชี้ตาม UN จึงยื่นทับ n_line ตัวเอง (เจอจริงจาก [LAYOUT] log รอบสอง:
        # 'P' ทับ Line 25 จุด + 'R'<->'P' ยังทับ 32% เท่าเดิม) เปลี่ยนเป็นตั้งฉาก
        # (_perp_un) แต่ _perp_un ดันขนานกับเส้น A-R (l_AR) พอดีอีก (เพราะ AR ตั้งฉาก
        # กับเส้น normal โดยนิยาม -- perp ของ normal จึงขนาน AR) เจอจริงรอบสาม:
        # 'R' ทับ Line + 'P' ทับ Line + 'R' ทับ Polygon (t_APR ที่วาดทีหลัง) -- จุด R
        # มีเส้นตัดกัน 2 เส้นที่ตั้งฉากกันพอดี (normal line และ AR) ทิศไหนก็ขนานเส้นใด
        # เส้นหนึ่งเสมอ ทางออกคือชี้ "ทแยง 45 องศา" ระหว่างสองทิศนั้นแทน (ไม่ขนานสิ่งใดเลย)
        _perp_un = np.array([-UN[1], UN[0], 0.0])
        _diag_un = (UN + _perp_un)
        _diag_un = _diag_un / np.linalg.norm(_diag_un)
        base = VGroup(
            loc, n_line,
            seg(A, R, C_AR, 5), seg(B, S, C_BS, 5),
            pt(A, C_AQ, 0.08), pt(B, C_BQ, 0.08),
            pt(R, C_AR, 0.07), pt(S, C_BS, 0.07), pt(P, C_VN, 0.09),
            tag("A", A, UP, C_AQ, 24), tag("B", B, DOWN, C_BQ, 24),
            # R อยู่ทาง -U จาก P (ตรวจแล้วจากเลขจริง) -- ใช้ -diag สำหรับ R (ดันออกจาก
            # P เพิ่ม) และ +diag สำหรับ P (ดันออกจาก R เพิ่ม) แยกกันคนละทิศแน่นอน
            tag("R", R, -_diag_un, C_AR, 20, 0.4), tag("S", S, UR, C_BS, 20, 0.10),
            # +diag_un ยังทับ Line อยู่ (เจอจริงจาก [LAYOUT] log 2026-09-05 รอบสี่) --
            # คำนวณละเอียดอีกที: มีเส้น 4 เส้นตัดกันที่ P (loc=+-90deg, n_line=-20/160deg)
            # แบ่งเป็น 4 ช่อง 70/110/70/110 องศา -- ap1/ap2 (มุมรัศมี 0.40) ครองสอง
            # ช่อง 70 องศาไปแล้ว (90-160 กับ -90..-20) เหลือช่อง 110 องศาว่างสองช่อง
            # ใช้กึ่งกลางช่องแรก (-20..90 -> 35 องศา) ซึ่งห่างจากทั้ง loc และ n_line
            # อย่างน้อย 55 องศา (ไม่ขนานสิ่งใดเลย และไม่ชน ap1/ap2)
            tag("P", P, np.array([np.cos(35 * DEGREES), np.sin(35 * DEGREES), 0.0]),
                C_VN, 24, 0.5),
            tag("AR", A + (R - A) * 0.45, _ar_perp6, C_AR, 20, 0.22),
            # เหมือน bug ที่เจอใน G05A (LEFT พาป้ายข้ามเส้น loc เสมอเพราะจุดยึดอยู่
            # ทางขวาของ loc อยู่แล้ว) แก้เชิงรุกที่นี่ด้วยแม้ยังไม่เคยถูก Gemini/linter
            # จับได้ตรงๆ ในซีนนี้ -- จุด B, S เดียวกัน ความเสี่ยงเดียวกัน
            tag("BS", B + (S - B) * 0.50, RIGHT, C_BS, 21, 0.12),
            ra_mark(R, A - R, Q - R, C_AR),
            ra_mark(S, B - S, Q - S, C_BS),
        )
        self.play(FadeIn(base), run_time=1.3)

        cap = caption_top("P คือจุดที่ contact normal ตัดกับเส้นศูนย์กลาง", size=23)
        self.play(FadeIn(cap), Flash(P, color=C_VN, flash_radius=0.5))
        self.wait(1.2)

        # --- สามเหลี่ยม APR และ BPS ---------------------------------------------
        cap = self.swap_cap(cap, "ได้สามเหลี่ยมมุมฉาก 2 รูป: A-P-R และ B-P-S")
        t_APR = Polygon(A, P, R, color=C_AQ, fill_opacity=0.30, stroke_width=4)
        t_BPS = Polygon(B, P, S, color=C_BQ, fill_opacity=0.30, stroke_width=4)
        self.play(FadeIn(t_APR))
        self.wait(0.6)
        self.play(FadeIn(t_BPS))
        self.wait(0.9)

        # ---- ทำไมคู่นี้ถึงคล้ายกัน (AA อีกครั้ง แต่คนละเหตุผลกับหน้า 5) ----
        cap = self.swap_cap(cap, "ขั้น 1: มุมฉากที่ R และที่ S (เพราะ AR และ BS ตั้งฉากกับ normal)",
                            size=21)
        rr = ra_mark(R, A - R, Q - R, OK, 0.26)
        rs = ra_mark(S, B - S, Q - S, OK, 0.26)
        self.play(Create(rr), Create(rs))
        self.wait(1.6)

        cap = self.swap_cap(cap, "ขั้น 2: ที่ P มีเส้นตรง 2 เส้นตัดกัน — เส้นศูนย์กลาง กับ normal",
                            size=21)
        self.play(Indicate(loc, color=C_LOC, scale_factor=1.0),
                  Indicate(n_line, color=C_NORM, scale_factor=1.0))
        self.wait(1.2)

        cap = self.swap_cap(cap, "เส้นตรงตัดกัน → มุมตรงข้ามเท่ากันเสมอ", size=23)
        ap1 = Angle(Line(P, A), Line(P, R), radius=0.40, color=WARN, stroke_width=4)
        ap2 = Angle(Line(P, S), Line(P, B), radius=0.40, color=WARN, stroke_width=4)
        self.play(Create(ap1), Create(ap2))
        self.wait(1.8)

        cap = self.swap_cap(cap, "มุมฉาก + มุมตรงข้าม = คล้ายกันแบบ มุม-มุม (AA)", size=23)
        self.play(Indicate(VGroup(rr, rs, ap1, ap2), color=OK, scale_factor=1.1))
        self.wait(1.4)

        # สามเหลี่ยม A-R-P (และ B-S-P) เป็นทรง "บาง" มาก -- ด้าน R-P (และ S-P) สั้นกว่า
        # อีกสองด้านมาก (ตรวจด้วยเลขจริง: A-R=1.35, A-P=1.44, R-P=0.49 หน่วย) ทำให้หลัง
        # upright_tri() ยกออกมาวางใหม่ จุดยอด R กับ P (S กับ P) ยังอยู่ใกล้กันเกินกว่า
        # buff เริ่มต้น (0.30) ของป้ายชื่อจะกันชนไหว (เจอจริงจาก [LAYOUT] log 2026-09-05:
        # 'R'<->'P' ทับกัน 32% ซ้ำสองรอบ) แก้โดยดันป้าย R/P (S/P) ออกจากกันเพิ่มเติมตาม
        # แนวตั้งฉากกับเส้น R-P (S-P) ของตัวเอง หลังสร้าง g1/g2 เสร็จ
        def _separate_labels(vg, v, key_b, key_c, dist=0.3):
            lb, lc = vg[4][1], vg[4][2]
            d = v[key_c] - v[key_b]
            n = np.linalg.norm(d)
            perp = np.array([-d[1], d[0], 0.0]) / n if n > 1e-9 else np.array([0.0, 1.0, 0.0])
            lb.shift(-perp * dist)
            lc.shift(perp * dist)

        g1, v1u, _ = upright_tri(A, R, P, ("A", "R", "P"),
                               (C_AR, C_AQ, C_TAN), [3.0, 1.45, 0], 1.15)
        _separate_labels(g1, v1u, "b", "c")
        g2, v2u, _ = upright_tri(B, S, P, ("B", "S", "P"),
                               (C_BS, C_BQ, C_TAN), [3.0, -0.35, 0], 1.15)
        _separate_labels(g2, v2u, "b", "c")
        self.play(FadeOut(t_APR), FadeOut(t_BPS))
        self.play(FadeIn(g1, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(g2, shift=RIGHT * 0.3), run_time=1.0)
        self.wait(1.4)

        eq1 = eq_row(frac2("AP", "AR", C_AQ, C_AR),
                     MathTex("=", font_size=34),
                     frac2("BP", "BS", C_BQ, C_BS)).move_to([3.0, -2.15, 0])
        self.play(FadeIn(eq1, shift=UP * 0.15))
        self.wait(1.8)

        cap = self.swap_cap(cap, "จัดรูปใหม่ แล้วแทนผลจากหน้า 5 (ω₂/ω₃ = BS/AR)", size=22)
        eq2 = eq_row(frac2("BS", "AR", C_BS, C_AR),
                     MathTex("=", font_size=34),
                     frac2("BP", "AP", C_BQ, C_AQ)).move_to([3.0, -3.20, 0])
        self.play(FadeIn(eq2, shift=UP * 0.15))
        self.wait(2.0)

        self.play(FadeOut(g1), FadeOut(g2), FadeOut(eq1), FadeOut(eq2))
        final = eq_row(frac2(r"\omega_2", r"\omega_3", C_AQ, C_BQ, size=44),
                       MathTex("=", font_size=44),
                       frac2("BP", "AP", C_BQ, C_AQ, size=44)).move_to([3.0, 0.55, 0])
        box = SurroundingRectangle(final, color=OK, buff=0.30, stroke_width=4)
        self.play(FadeIn(final, shift=UP * 0.2), Create(box))
        self.wait(1.6)

        cap = self.swap_cap(cap, "อัตราทดขึ้นกับจุด P ล้วน ๆ — ถ้าอยากให้คงที่ P ต้องอยู่นิ่ง", size=22)
        self.play(Indicate(VGroup(final, box), color=OK, scale_factor=1.08))
        self.wait(2.6)

    def swap_cap(self, old, txt, size=23):
        self.play(FadeOut(old))
        new = caption_top(txt, size=size)
        self.play(FadeIn(new))
        return new
