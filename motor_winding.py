"""motor_winding — ซีรีส์สอนพันขดลวดอาร์เมเจอร์ (เวฟ/แลป) + พันจริงมอเตอร์รถแข่งของ Min

โปรเจกต์: รถแข่งจับเวลา ไม่มีเกียร์ทด แบต 7.2V (Li-ion 3.6V x2 อนุกรม)
อาร์เมเจอร์จริงที่จะพัน = ชุดสำเร็จรูป 3 ขั้ว/คอมมิวเตเตอร์ 3 ซี่ (ดู HANDOFF/แชท motor maker)

ที่มา physics (verified ผ่าน WebSearch 2026-09-01 — electricaleasy.com "Armature Winding
of DC Machine", utk.edu/~tolbert ECE321 armature.pdf handout — ไม่ใช่คิดเองจาก scratch):
  - Lap winding:  commutator pitch Yc = 1 (ปลายขดต่อซี่ติดกัน) · เส้นทางขนาน a = P (จำนวนขั้ว)
  - Wave winding: commutator pitch Yc = (C ± 1) / (P/2)        · เส้นทางขนาน a = 2 เสมอ ไม่ว่ากี่ขั้ว
  - Coil span (pole pitch) ของทั้งสองแบบ ≈ C/P บาร์ — คนละปริมาณกับ commutator pitch
    (นี่คือจุดที่ Min สับสนตอนคุย จึงต้องมีซีนแยกสองระยะนี้ให้เห็นชัดก่อนสอนต่อ)
ตัวเลขสาธิต (8 บาร์ lap, 9 บาร์ wave) เป็นตัวอย่างเพื่อการสอน ไม่ใช่สเปกเครื่องจักรจริง
ระบุชัดในคลิปว่าเป็นตัวอย่างประกอบ (skill manim-teaching-video §18/§21.4)

ทุก Text/MathTex ใน SafeThreeDScene ต้องผ่าน self.hud(...) ตอนสร้าง (จัดตำแหน่งให้เสร็จก่อน
ค่อย hud) ไม่งั้นจะเอียงตามกล้องตอนมี zoom_to/ambient rotation — เจอบั๊กนี้จริงตอนเรนเดอร์รอบแรก
(รัน 33488089297 — [LAYOUT] แจ้ง "ไม่ได้ตรึงกับเฟรม" เกือบทุกข้อความในทุกซีน เพราะเดิม hud()
แค่ cap0 ตัวแรกของแต่ละซีน ไม่ได้ hud() ทุกครั้งที่มีข้อความใหม่ผ่าน ReplacementTransform)
"""
from manim import *
import numpy as np
from mlib import *

# ---------------------------------------------------------------- 3D stage
STAGE = np.array([-1.9, -0.65, 0.0])
R_ARM = 0.95
L_HALF = 0.80
POLE_X = 2.0
POLE_W = 0.85
POLE_H = 1.5

# คอมมิวเตเตอร์ติดอยู่หน้าอาร์เมเจอร์จริงๆ ในโมเดล 3D เดียวกัน (Min ขอหลังดู v5: "ผมอยากเห็น
# เป็น 3D มากกว่า ... เริ่มที่หน้าของ commutator แล้วไปเกี่ยวที่อาร์เมเจอร์" — เดิมวาดเป็น
# แผนผังลอยแยกไปไกลๆ ทางขวา เส้นลวดเลยลากยาวข้ามจอไม่สมจริง) วางไว้ตามแนวเพลา ถัดจาก
# หน้าอาร์เมเจอร์ (z=L_HALF) ก่อนถึงปลายเพลา (z=L_HALF+0.85) วงเล็กกว่าอาร์เมเจอร์เอง
# ตามสัดส่วนคอมมิวเตเตอร์จริง
COMM_Z = L_HALF + 0.40
R_SCHEM = R_ARM * 0.75
SCHEM_C = STAGE + np.array([0.0, 0.0, COMM_Z])

PATH_COLORS = [CURRENT, OK, FORCE, TORQUE, EMF, "#4FC3F7"]

# โซนข้อความรองที่ปลอดภัย — ไม่ใช่ CAP_Y (-3.15) ของ mlib เดิม เพราะพิสูจน์แล้วว่าโปรแกรม
# เล่นวิดิโอบางตัว (Windows Movies&TV) มีแถบควบคุมคลุมลึกกว่าที่คิด บังข้อความที่ -3.15 พอดี
# (เจอจริงตอน Min ดู v2 preview — ป้าย "pole pitch" อ่านไม่ออกเพราะโดนแถบเล่นทับ)
SAFE_LOW_Y = -2.5


# ============================================================== shared parts
def armature_core(n_slot, center=STAGE, r_arm=R_ARM, l_half=L_HALF):
    front = Circle(radius=r_arm, color=METAL, stroke_width=2.5).move_to(center + [0, 0, l_half])
    back = Circle(radius=r_arm, color=METAL, stroke_width=2.0).move_to(center + [0, 0, -l_half])
    back.set_opacity(0.42)
    ribs = VGroup(*[
        line3(center + r_arm * np.array([np.cos(a), np.sin(a), 0]) + [0, 0, -l_half],
              center + r_arm * np.array([np.cos(a), np.sin(a), 0]) + [0, 0, l_half],
              METAL, thickness=0.010).set_opacity(0.30)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    shaft = line3(center + [0, 0, -l_half - 0.45], center + [0, 0, l_half + 0.85],
                  METAL, thickness=0.045)
    return VGroup(front, back, ribs, shaft)


def pole_pieces(n_poles, center=STAGE, r_arm=R_ARM, pole_x=POLE_X,
                pole_w=POLE_W, pole_h=POLE_H):
    """คืน (แท่งขั้ว [กราฟิก], ป้าย N/S [ข้อความ — ผู้เรียกต้อง self.hud() เอง], ตำแหน่งโลก 3D จริงของแต่ละขั้ว)

    เหตุที่คืนตำแหน่งโลกแยกมาด้วย: ห้ามอ่าน .get_center() จากป้ายหลัง hud() แล้ว —
    fixed-in-frame mobject จะไม่ใช่พิกัดโลก 3D อีกต่อไป (เจอบั๊กจริง: ตอนเอา
    pole_labels[0].get_center() ไปเป็นจุดเริ่มลูกศรชี้ป้ายใน name_pointer หลัง hud()
    ไปแล้ว ทำให้ป้ายไปทับกับ 'N' เกือบสนิท 94% — ต้องอ่านตำแหน่งโลกจากตรงนี้เท่านั้น)
    """
    g = VGroup()
    labels = VGroup()
    positions = []
    offset = r_arm + pole_x * 0.55
    for i in range(n_poles):
        a = TAU * i / n_poles
        direction = np.array([np.cos(a), np.sin(a), 0])
        pos = center + direction * offset
        rect = Rectangle(width=pole_w, height=pole_h, color=METAL, fill_color=METAL,
                         fill_opacity=0.55, stroke_width=2)
        rect.move_to(pos)
        rect.rotate(a, about_point=pos)
        is_n = (i % 2 == 0)
        lab = Text("N" if is_n else "S", font_size=24, color=WHITE).move_to(pos)
        g.add(rect)
        labels.add(lab)
        positions.append(pos)
    return g, labels, positions


def slot_angles(n, start=PI / 2):
    return [start + i * TAU / n for i in range(n)]


def commutator_bars(n_bars, center=SCHEM_C, r=R_SCHEM, color=METAL):
    """คืน (บาร์ [กราฟิก], เลขกำกับ [ข้อความ — ผู้เรียกต้อง self.hud() เอง], มุมแต่ละบาร์)"""
    bars = VGroup()
    nums = VGroup()
    angs = slot_angles(n_bars)
    span = TAU / n_bars * 0.68
    for i, a in enumerate(angs):
        arc = Arc(radius=r, start_angle=a - span / 2, angle=span, color=color,
                  stroke_width=9, arc_center=center)
        bars.add(arc)
        num = Text(str(i + 1), font_size=15, color=GRAYTXT).move_to(
            center + (r + 0.30) * np.array([np.cos(a), np.sin(a), 0]))
        nums.add(num)
    return bars, nums, angs


def chord(center, r, a1, a2, color, sw=3.5):
    p1 = center + r * 0.84 * np.array([np.cos(a1), np.sin(a1), 0])
    p2 = center + r * 0.84 * np.array([np.cos(a2), np.sin(a2), 0])
    return Line(p1, p2, color=color, stroke_width=sw)


def coil_lead(wind_center, pole_dir, seg_point, color, thickness=0.03, dot_r=0.06,
             wrap_width=0.34):
    """เส้นทางตามที่ Min สั่งเป๊ะๆ (ข้อความเสียง): เริ่มที่ซี่คอมมิวเตเตอร์ -> ลากลงตรงตามแกน Z
    ล้วนๆ (x,y คงที่) ไปสุดที่ด้านหลังอาร์เมเจอร์ -> เปลี่ยนแกนให้ขนานกับ "Normal" ของฟัน
    (=ทิศสัมผัส coil_ring_axis) อ้อมไปอีกฝั่งหนึ่งของฟัน (สี่เหลี่ยมผืนผ้า) -> ขึ้นตามแกน Z
    ล้วนๆ กลับไปที่ปลายขดด้านหน้า — จำลองเส้นลวดพันอ้อมฟันจริง ไม่ใช่เส้นตรงเฉียงข้ามจอ
    Dot ธรรมดา (แบน) ไม่ใช่ Dot3D (ทรงกลม mesh จริง) — วงกลมแบนมองจากมุมไหนก็ยังอ่านง่ายเหมือนกัน
    ไม่ต้องแบกต้นทุนเรนเดอร์ตาข่าย 3D แบบเดียวกับที่ Arrow3D ช้ากว่า Arrow แบน 62 เท่า"""
    seg_point = np.asarray(seg_point, dtype=float)
    tangent = coil_ring_axis(pole_dir)
    down_pt = np.array([seg_point[0], seg_point[1], -L_HALF], dtype=float)
    across_pt = down_pt + tangent * wrap_width
    up_pt = np.array([across_pt[0], across_pt[1], L_HALF], dtype=float)
    return VGroup(
        Dot(seg_point, radius=dot_r, color=color),
        Dot(up_pt, radius=dot_r, color=color),
        line3(seg_point, down_pt, color, thickness),
        line3(down_pt, across_pt, color, thickness),
        line3(across_pt, up_pt, color, thickness),
    )


def tooth_shape(pole_dir, center=STAGE, r_arm=R_ARM, l_half=L_HALF, color=METAL):
    """ฟันยื่นแบบขั้วนูน (salient pole) บนแกนหมุน — Min ถามตรงๆ ว่าลวดต้องพันอ้อมไปหลัง
    แกนด้วยไหม (แกนจริงไม่ใช่ทรงกระบอกเรียบ มีฟันยื่น 3 ซี่ให้พันลวดรอบแต่ละซี่แบบพันหม้อแปลง)
    วาดเป็นแผ่นสี่เหลี่ยมยื่นจากใกล้เพลาออกไปใกล้ผิว ยาวเต็มความยาวแกน (-l_half ถึง +l_half)"""
    r_in, r_out = r_arm * 0.15, r_arm * 0.92
    pts = [center + pole_dir * r_in + [0, 0, -l_half],
           center + pole_dir * r_out + [0, 0, -l_half],
           center + pole_dir * r_out + [0, 0, l_half],
           center + pole_dir * r_in + [0, 0, l_half]]
    return Polygon(*pts, color=color, fill_color=color, fill_opacity=0.6, stroke_width=2)


def coil_winding(wind_center, pole_dir, n_turns=7, color=CURRENT,
                 axial_len=2 * L_HALF, thick=0.30, bundle=0.22):
    """ขดลวดพันรอบฟัน — ห่วงรี (แนวแกน Z x ทิศสัมผัส, ยาวคลุมทั้งความยาวฟัน) เรียงเหลื่อม
    กันตามแนวทิศสัมผัส (tangential) ให้เห็นว่าลวดพันซ้อนหลายรอบอ้อมฟันจากหน้าไปหลัง"""
    loops = VGroup()
    axis = coil_ring_axis(pole_dir)
    for k in range(n_turns):
        shift = (k - (n_turns - 1) / 2) * (bundle / n_turns)
        loop = Ellipse(width=thick, height=axial_len + 0.30, color=color, stroke_width=2.2)
        loop.move_to(wind_center + axis * shift)
        loop.rotate(PI / 2, axis=axis)
        loops.add(loop)
    return loops


def coil_ring_axis(pole_dir):
    """แกนหมุนที่ถูกต้องสำหรับพลิกวงแหวน (ปกติ normal=OUT) ให้ normal ชี้ตาม pole_dir
    pole_dir อยู่ในระนาบ XY เสมอ (z=0) จึงตั้งฉากกับ OUT เสมอ มุมหมุนคงที่ 90°
    แกนหมุนที่ถูกต้องคือทิศสัมผัส (tangential) ตั้งฉากกับ pole_dir ในระนาบ XY
    (ยืนยันด้วย Rodrigues' rotation formula: หมุน 90° รอบแกนนี้ -> normal ใหม่ = pole_dir เป๊ะ
    เดิมเคยลองหมุนรอบ pole_dir เอง ซึ่งผิด — normal ใหม่จะออกมาตั้งฉากกับ pole_dir แทน)"""
    return np.array([-pole_dir[1], pole_dir[0], 0.0])


def name_pointer(base_pos, dir_vec, label_txt, color=OK, dist=0.75, fsize=18):
    """ลูกศร+ป้าย ชี้ชิ้นส่วน — ใช้ตอนแนะนำโมเดลครั้งแรกในคลิป (skill §21.8)

    ทั้งลูกศรและป้ายอยู่ในโลก 3D จริงด้วยกัน (ไม่ hud() ป้าย) — เจอบั๊กจริงตอนลองหุ้ม
    ป้ายด้วย self.hud(): fixed-in-frame ในสภาพแวดล้อมนี้ใช้พิกัด (x,y) ดิบของมอเตอร์
    ตรงๆ เป็นพิกัดจอแบน ไม่ได้แปลงมุมกล้อง (phi/theta) ให้เลย ป้ายเลย "หลุด" ไปอยู่คนละ
    ที่กับวัตถุ 3D ที่มันควรจะชี้ (ยืนยันจากพิกเซลจริงในเฟรมที่เรนเดอร์ออกมา 2 รอบติด)
    ปล่อยให้อยู่ในโลก 3D เหมือนกันทั้งคู่แทน — ตราบใดที่กล้องนิ่งตอนแสดงป้ายพวกนี้
    (ทุกซีนในไฟล์นี้กล้องนิ่งตลอดช่วงที่มี naming pass) ก็ไม่เอียง ไม่ต้อง hud()"""
    end = base_pos + np.array(dir_vec, dtype=float) * dist
    arr = arrow3(base_pos, end, color, thickness=0.016)
    lab = Text(label_txt, font_size=fsize, color=color)
    lab.move_to(end + np.array(dir_vec, dtype=float) * 0.32)
    return VGroup(arr, lab)


def overlay_card(scene, lines, move_to=(0, -0.4, 0)):
    """การ์ดสรุปท้ายซีน (กล่อง+ข้อความ) — ตรึงทั้งกล่องทั้งข้อความเป็นภาพซ้อนหน้าจอเดียวกัน
    เพื่อไม่ให้กล่องกับตัวอักษรเยื้องกันถ้ากล้องขยับหลังจากนี้"""
    card = VGroup(*lines).arrange(DOWN, buff=0.20)
    box = SurroundingRectangle(card, color=OK, buff=0.32, corner_radius=0.14,
                               fill_color=BLACK, fill_opacity=0.9)
    summary = VGroup(box, card).move_to(np.array(move_to, dtype=float))
    return scene.hud(summary)


# ================================================================ SCENE W01
class W01_WhyManyCoils_PolePitchVsCommPitch(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-52 * DEGREES)

        ttl = self.hud(title("ทำไมต้องมีหลายขดลวด", size=27))
        ref = self.hud(page_ref("ซีรีส์พันมอเตอร์ · ตอน 1"))
        cap0 = self.hud(caption_top(
            "ทวนจากคลิป How a Motor Works ตอน 5 — ยิ่งซี่คอมมิวเตเตอร์ถี่ ทอร์กยิ่งเรียบ"))
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=1.0)
        self.wait(1.2)

        core = armature_core(8)
        poles, pole_labels, pole_pos = pole_pieces(4)
        self.play(FadeIn(core), FadeIn(poles), FadeIn(pole_labels), run_time=1.4)
        self.wait(1.0)

        # -------- naming pass (ครั้งแรกในซีรีส์นี้ — ชี้บอกชื่อทุกชิ้น) --------
        n1 = name_pointer(STAGE + [0, 0, L_HALF], [0, 0, 1], "แกนอาร์เมเจอร์ (หมุน)", OK)
        n2 = name_pointer(pole_pos[0], [1, 0, 0],
                          "ขั้วแม่เหล็กหลัก (อยู่กับที่)", METAL, dist=0.9)
        n3 = name_pointer(STAGE + [0, 0, L_HALF + 0.85], [0.6, 0.3, 0.3],
                          "เพลา", GRAYTXT, dist=0.7)
        cap_name = self.hud(caption_top("ก่อนอื่น รู้จักชิ้นส่วนก่อน", color=GRAYTXT))
        self.play(FadeIn(n1), FadeIn(n2), FadeIn(n3), ReplacementTransform(cap0, cap_name),
                  run_time=1.0)
        self.wait(1.4)
        self.play(FadeOut(VGroup(n1, n2, n3)), run_time=0.6)

        cap1 = self.hud(caption_top(
            "ขดเดียวมีจุดตายทุกครึ่งรอบ — มอเตอร์จริงจึงพันหลายขด รอบแกนเดียวกัน"))
        self.play(ReplacementTransform(cap_name, cap1), run_time=0.8)
        self.wait(1.6)

        cap2 = self.hud(caption_top(
            "แต่ละขดต้องมีปลายไปต่อกับซี่คอมมิวเตเตอร์ — คำถามคือต่อ 'ซี่ไหนกับซี่ไหน'"))
        self.play(ReplacementTransform(cap1, cap2), run_time=0.8)
        self.wait(1.8)

        # -------- ย้ายกล้อง/จาง armature ไปโฟกัสที่ระยะสองแบบบนวงแหวนคอมมิวเตเตอร์
        # (คอมมิวเตเตอร์ติดหน้าอาร์เมเจอร์ วงเล็ก ต้องซูมเข้าไปมากกว่าตอนวางลอยแยกไกลๆ)
        self.zoom_to(SCHEM_C, zoom=2.4, run_time=1.3)
        bars, nums, angs = commutator_bars(8)
        self.play(core.animate.set_opacity(0.25), poles.animate.set_opacity(0.15),
                  pole_labels.animate.set_opacity(0.15),
                  Create(bars), FadeIn(nums), run_time=1.4)
        self.wait(0.8)

        cap3 = self.hud(caption_top("มี 2 ระยะที่ต้องแยกให้ออก — คนละอย่างกัน แม้ชื่อจะคล้าย"))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.8)
        self.wait(1.4)

        # ระยะที่ ① pole pitch — ระยะข้ามขั้วของตัวขดลวดเอง (บาร์ 1 ถึงบาร์ 3 ห่าง C/P=2)
        pp_line = chord(SCHEM_C, R_SCHEM, angs[0], angs[2], WARN, sw=5)
        pp_tag = self.hud(Text("① pole pitch — ช่วงกว้างของขดลวดเอง (ข้ามขั้ว)",
                               font_size=19, color=WARN).move_to([0, SAFE_LOW_Y, 0]))
        self.play(Create(pp_line), FadeIn(pp_tag), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(pp_line), FadeOut(pp_tag), run_time=0.6)

        # ระยะที่ ② commutator pitch — ระยะที่ปลายสายไป "กระโดด" ไปต่อซี่ถัดไป
        cp_line = chord(SCHEM_C, R_SCHEM, angs[0], angs[1], OK, sw=5)
        cp_tag = self.hud(Text("② commutator pitch — ปลายสายกระโดดไปต่อซี่ไหน",
                               font_size=19, color=OK).move_to([0, SAFE_LOW_Y, 0]))
        self.play(Create(cp_line), FadeIn(cp_tag), run_time=1.0)
        self.wait(1.8)

        cap4 = self.hud(caption_top(
            "② นี่แหละ ที่ทำให้ 'แลป' กับ 'เวฟ' ต่างกัน — ไปดูทีละแบบกันต่อ", color=OK))
        self.play(ReplacementTransform(cap3, cap4), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(cp_line), FadeOut(cp_tag), run_time=0.5)
        self.fade_out_all()


# ================================================================ SCENE W02
class W02_LapWinding(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=58 * DEGREES, theta=-48 * DEGREES)
        n_bars, n_poles = 8, 4
        yc = 1  # commutator pitch แบบ progressive lap

        ttl = self.hud(title("พันแบบแลป (Lap)", size=29))
        ref = self.hud(page_ref("ซีรีส์พันมอเตอร์ · ตอน 2"))
        cap0 = self.hud(caption_top(
            "จากตอนที่แล้ว — ระยะ ② (commutator pitch) ของแลปคือ 1 (ซี่ติดกันเสมอ)"))
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=1.0)
        self.wait(1.4)

        core = armature_core(n_bars)
        poles, pole_labels, pole_pos = pole_pieces(n_poles)
        core.set_opacity(0.35)
        poles.set_opacity(0.22)
        pole_labels.set_opacity(0.22)
        bars, nums, angs = commutator_bars(n_bars)
        self.play(FadeIn(core), FadeIn(poles), FadeIn(pole_labels),
                  Create(bars), FadeIn(nums), run_time=1.4)
        self.wait(0.6)

        note = self.hud(Text(
            "ตัวอย่างสาธิต: 4 ขั้ว, 8 ขด/8 ซี่ (เลขตัวอย่างเพื่อสอน ไม่ใช่มอเตอร์จริงเครื่องใดเครื่องหนึ่ง)",
            font_size=15, color=GRAYTXT).move_to([0, SAFE_LOW_Y, 0]))
        self.play(FadeIn(note), run_time=0.6)

        cap1 = self.hud(caption_top("ขดที่ 1: ปลายเริ่มที่ซี่ 1 ปลายจบที่ซี่ 2 — ติดกันเป๊ะ"))
        self.play(ReplacementTransform(cap0, cap1), run_time=0.8)
        chords = VGroup()
        for i in range(n_bars):
            c = chord(SCHEM_C, R_SCHEM, angs[i], angs[(i + yc) % n_bars], CURRENT, sw=4)
            chords.add(c)
            self.play(Create(c), run_time=0.35)
        self.wait(1.0)

        cap2 = self.hud(caption_top(
            "วนต่อไปเรื่อยๆ ทุกขดต่อซี่ติดกันหมด จนครบกลับมาที่ซี่ 1 พอดี"))
        self.play(ReplacementTransform(cap1, cap2), run_time=0.8)
        self.wait(1.8)

        # แสดง parallel paths: แบ่งเป็น P กลุ่ม กลุ่มละ n_bars/P ซี่ ระบายสีต่างกัน
        cap3 = self.hud(caption_top(
            "ผลลัพธ์: ได้เส้นทางกระแสขนานกัน 4 เส้นทาง — เท่ากับจำนวนขั้ว (P)", color=OK))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.8)
        group_size = n_bars // n_poles
        for g in range(n_poles):
            col = PATH_COLORS[g % len(PATH_COLORS)]
            idxs = list(range(g * group_size, (g + 1) * group_size))
            grp = VGroup(*[chords[i] for i in idxs], *[bars[i] for i in idxs])
            self.play(grp.animate.set_color(col), run_time=0.5)
        self.wait(1.6)

        self.play(FadeOut(VGroup(note, core, poles, pole_labels, bars, nums, chords)),
                  run_time=0.6)
        summary = overlay_card(self, [
            Text("เส้นทางขนาน a = P (จำนวนขั้ว)", font_size=26, color=OK),
            Text("กระแสรวมแบ่งไหลหลายทาง → เหมาะไฟต่ำ กระแสสูง", font_size=21, color=GRAYTXT),
        ], move_to=(0, -0.3, 0))
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        self.wait(2.2)

        self.fade_out_all()


# ================================================================ SCENE W03
class W03_WaveWinding(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=58 * DEGREES, theta=-48 * DEGREES)
        n_bars, n_poles = 9, 4
        yc = 4  # (9-1)/(4/2) = 4  — progressive wave, gcd(4,9)=1 -> ผ่านครบทุกซี่ในเส้นทางเดียว

        ttl = self.hud(title("พันแบบเวฟ (Wave)", size=29))
        ref = self.hud(page_ref("ซีรีส์พันมอเตอร์ · ตอน 3"))
        cap0 = self.hud(caption_top(
            "ระยะ ② ของเวฟ ≈ 2 เท่าของ pole pitch — ปลายสาย 'กระโดดข้าม' เกือบสุดวง"))
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=1.0)
        self.wait(1.4)

        core = armature_core(n_bars)
        poles, pole_labels, pole_pos = pole_pieces(n_poles)
        core.set_opacity(0.35)
        poles.set_opacity(0.22)
        pole_labels.set_opacity(0.22)
        bars, nums, angs = commutator_bars(n_bars)
        self.play(FadeIn(core), FadeIn(poles), FadeIn(pole_labels),
                  Create(bars), FadeIn(nums), run_time=1.4)
        self.wait(0.6)

        note = self.hud(Text(
            "ตัวอย่างสาธิต: 4 ขั้ว, 9 ขด/9 ซี่ (เลขคี่ตั้งใจเลือก ให้เส้นทางเดียววนครบทุกซี่พอดี)",
            font_size=15, color=GRAYTXT).move_to([0, SAFE_LOW_Y, 0]))
        self.play(FadeIn(note), run_time=0.6)

        cap1 = self.hud(caption_top("ขดที่ 1: เริ่มซี่ 1 กระโดดไปจบที่ซี่ 5 — ข้ามเกือบสุดวง"))
        self.play(ReplacementTransform(cap0, cap1), run_time=0.8)
        chords = VGroup()
        cur = 0
        for i in range(n_bars):
            nxt = (cur + yc) % n_bars
            c = chord(SCHEM_C, R_SCHEM, angs[cur], angs[nxt], OK, sw=4)
            chords.add(c)
            self.play(Create(c), run_time=0.4)
            cur = nxt
        self.wait(1.0)

        cap2 = self.hud(caption_top(
            "สังเกต: เส้นทางเดียวซิกแซกไปเรื่อยๆ จนครบทุกซี่ทั้ง 9 แล้วค่อยกลับมาที่ซี่ 1"))
        self.play(ReplacementTransform(cap1, cap2), run_time=0.8)
        self.wait(2.0)

        cap3 = self.hud(caption_top(
            "ไม่ว่าจะมีกี่ขั้ว เส้นทางแบบนี้จะมีแค่ 2 ทิศ (ตามเข็ม/ทวนเข็ม) เสมอ", color=OK))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.8)
        # แยกสี 2 ทิศทาง (สลับตามลำดับคู่/คี่ของการ create เพื่อสื่อว่าเป็นเส้นทางเดียวยาว)
        for i, c in enumerate(chords):
            col = PATH_COLORS[0] if i % 2 == 0 else PATH_COLORS[1]
            self.play(c.animate.set_color(col), run_time=0.18)
        self.wait(1.4)

        self.play(FadeOut(VGroup(note, core, poles, pole_labels, bars, nums, chords)),
                  run_time=0.6)
        summary = overlay_card(self, [
            Text("เส้นทางขนาน a = 2 เสมอ (ไม่ขึ้นกับจำนวนขั้ว)", font_size=25, color=OK),
            Text("กระแสรวมไหลผ่านขดจำนวนมากต่ออนุกรมกัน → เหมาะไฟสูง กระแสต่ำ",
                 font_size=20, color=GRAYTXT),
        ], move_to=(0, -0.3, 0))
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        self.wait(2.2)

        self.fade_out_all()


# ================================================================ SCENE W04
class W04_Compare_ApplyToYourMotor(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)  # มองตรงหน้า เหมือน 2D
        ttl = self.hud(title("เทียบแลป vs เวฟ", size=28))
        ref = self.hud(page_ref("ซีรีส์พันมอเตอร์ · ตอน 4"))
        cap0 = self.hud(caption_top(
            "สรุปตัวเลขสำคัญที่ต่างกันจริง — แล้วมอเตอร์ของ Min เข้าทางไหน"))
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=1.0)
        self.wait(1.0)

        # ---------------- แผนภูมิแท่งเทียบเส้นทางขนาน (a) ----------------
        chart_c = np.array([-2.6, -0.55, 0])
        base_y = chart_c[1] - 1.3
        bar_w = 1.1
        lap_h, wave_h = 2.2, 1.1  # a=4 กับ a=2 (สัดส่วนภาพ)
        lap_bar = Rectangle(width=bar_w, height=lap_h, color=CURRENT, fill_color=CURRENT,
                            fill_opacity=0.85, stroke_width=1.5)
        lap_bar.move_to([chart_c[0] - 0.75, base_y + lap_h / 2, 0])
        wave_bar = Rectangle(width=bar_w, height=wave_h, color=OK, fill_color=OK,
                             fill_opacity=0.85, stroke_width=1.5)
        wave_bar.move_to([chart_c[0] + 0.75, base_y + wave_h / 2, 0])
        base_line = Line([chart_c[0] - 1.6, base_y, 0], [chart_c[0] + 1.6, base_y, 0],
                         color=GRAYTXT, stroke_width=2)
        lap_lab = self.hud(Text("แลป\na = P = 4", font_size=17, color=CURRENT,
                                line_spacing=0.9).next_to(lap_bar, DOWN, buff=0.14))
        wave_lab = self.hud(Text("เวฟ\na = 2", font_size=17, color=OK,
                                 line_spacing=0.9).next_to(wave_bar, DOWN, buff=0.14))
        chart_ttl = self.hud(Text("จำนวนเส้นทางกระแสขนาน (a) — ตัวอย่าง 4 ขั้ว",
                                  font_size=17, color=GRAYTXT).next_to(base_line, UP, buff=1.9))
        self.play(FadeIn(chart_ttl), Create(base_line), GrowFromEdge(lap_bar, DOWN),
                  GrowFromEdge(wave_bar, DOWN), FadeIn(lap_lab), FadeIn(wave_lab), run_time=1.4)
        self.wait(1.4)

        # ---------------- ตารางสรุปข้อความฝั่งขวา ----------------
        rows = self.hud(VGroup(
            Text("แลป — commutator pitch = 1 (ซี่ติดกัน)", font_size=18, color=CURRENT),
            Text("เวฟ — commutator pitch ≈ 2×pole pitch", font_size=18, color=OK),
            Text("แลป: กระแสสูง แรงดันต่ำ (มอเตอร์เล็ก/รถไฟฟ้า)", font_size=18, color=GRAYTXT),
            Text("เวฟ: แรงดันสูง กระแสต่ำ (เครื่องกำเนิดใหญ่)", font_size=18, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.0, 0.35, 0]))
        self.play(FadeIn(rows), run_time=1.0)
        self.wait(2.2)

        cap1 = self.hud(caption_top(
            "มอเตอร์ของ Min: 7.2V (ต่ำ) กระแสสูงตอนออกตัว → โดยหลักการเข้าทาง 'แลป'"))
        self.play(ReplacementTransform(cap0, cap1), run_time=0.9)
        self.wait(1.8)

        cap2 = self.hud(caption_top(
            "แต่ของจริงที่จะพัน = 3 ขั้ว/3 ซี่เท่านั้น — commutator pitch เหลือแค่ 1 ทางเดียว",
            color=WARN))
        self.play(FadeOut(VGroup(chart_ttl, base_line, lap_bar, wave_bar, lap_lab, wave_lab, rows)),
                  ReplacementTransform(cap1, cap2), run_time=1.0)
        self.wait(1.8)

        cap3 = self.hud(caption_top(
            "แลปกับเวฟเลยกลายเป็นแบบเดียวกันพอดี — หลักการเดียวกัน ไม่ต้องเลือก", color=WARN))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.9)
        self.wait(2.0)

        summary = overlay_card(self, [
            Text("สรุปสำหรับมอเตอร์ของ Min", font_size=26, color=OK),
            Text("3 ซี่ → พันแบบ 'progressive' ต่อซี่ติดกันไปเรื่อยๆ (=หลักการแลป)",
                 font_size=19, color=GRAYTXT),
            Text("ทฤษฎีเวฟ/แลปข้างบนจะกลับมามีความหมายจริงถ้าวันหลังพันอาร์เมเจอร์หลายขั้วขึ้น",
                 font_size=17, color=GRAYTXT),
        ], move_to=(0, -0.5, 0))
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        self.wait(2.6)

        self.fade_out_all()


# ================================================================ SCENE W05
# Min ขอเทียบ 2 มุมกล้อง (เสียง 2026-09-01): "1 คือมุมกล้องที่ตามตัวเส้นขดลวดไปทีละเส้น"
# vs "2 คือเข้าให้มอเตอร์อยู่ตรงกลางจอมากกว่านี้ แค่เอียงพอเห็นฝั่งที่พิจารณาอยู่"
# แยกเป็นคลาสฐานร่วม + 2 คลาสย่อยต่างกันแค่พฤติกรรมกล้อง จะได้ไม่ต้องก็อปโค้ดทั้งซีน
class _W05Base(SafeThreeDScene):
    CAM = "wide"  # ลูกคลาสเซ็ตทับเป็น "follow" หรือ "centered"

    def cam_focus(self, point, zoom=1.7, run_time=1.0):
        """ซูม/แพนกล้องไปโฟกัสจุดนี้ — ทำงานเฉพาะโหมด follow เท่านั้น"""
        if self.CAM == "follow":
            self.zoom_to(point, zoom=zoom, run_time=run_time)

    def cam_reset(self, run_time=1.0):
        if self.CAM == "follow":
            self.zoom_to(STAGE, zoom=1.0, run_time=run_time)

    def construct(self):
        if self.CAM == "centered":
            # มองเกือบตรงหน้า เอียงแค่นิดเดียวพอเห็นความลึก โมเดลอยู่กลางจอตลอด ไม่แพน/ไม่ซูม
            self.set_camera_orientation(phi=24 * DEGREES, theta=-98 * DEGREES)
        else:
            self.set_camera_orientation(phi=58 * DEGREES, theta=-48 * DEGREES)
        n_bars = n_poles = 3

        ttl = self.hud(title("พันจริง — อาร์เมเจอร์ 3 ขั้ว", size=27))
        ref = self.hud(page_ref("ซีรีส์พันมอเตอร์ · ตอน 5"))
        cap0 = self.hud(caption_top(
            "มอเตอร์รถแข่งของ Min — ใช้หลักการแลป/เวฟที่เพิ่งเห็น แต่ 3 ซี่ = ทางเดียว"))
        self.play(FadeIn(ttl), FadeIn(ref), FadeIn(cap0), run_time=1.0)
        self.wait(1.2)

        core = armature_core(n_bars)
        bars, nums, angs = commutator_bars(n_bars)
        # ฟันยื่น 3 ซี่บนแกนหมุน (salient pole) — Min ถามว่าลวดต้องพันอ้อมไปหลังแกนไหม
        # คำตอบคือใช่ เพราะแกนจริงมีฟันยื่นแบบนี้ ไม่ใช่ทรงกระบอกเรียบ ลวดพันรอบฟันแต่ละซี่
        teeth = VGroup(*[tooth_shape(np.array([np.cos(a), np.sin(a), 0])) for a in angs])
        # nums อยู่ในโลก 3D (ไม่ hud) — จะได้หมุนไปพร้อมบาร์จริงตอนม้วนสุดท้าย (rotor_group)
        self.play(FadeIn(core), FadeIn(teeth), Create(bars), FadeIn(nums), run_time=1.3)

        # naming pass เฉพาะคลิปนี้ (อาจมีคนดูข้ามมาจากคลิปอื่น — skill §21.8)
        a0v = np.array([np.cos(angs[0]), np.sin(angs[0]), 0])
        n1 = name_pointer(STAGE + a0v * R_ARM * 0.55, a0v, "ฟันยื่น (พันลวดรอบนี้)", CURRENT,
                          dist=0.85)
        n2 = name_pointer(SCHEM_C, [0.8, 0.6, 0], "คอมมิวเตเตอร์ 3 ซี่ (ติดหน้าแกน)", METAL,
                          dist=R_SCHEM + 0.7)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.9)
        self.wait(1.3)
        self.play(FadeOut(VGroup(n1, n2)), run_time=0.5)

        step_hdr = self.hud(Text("ขั้นตอนที่ 1 — พันขั้วที่ 1", font_size=17,
                                 color=WARN).move_to([0, SAFE_LOW_Y, 0]))
        self.play(FadeIn(step_hdr), run_time=0.5)

        cap1 = self.hud(caption_top("พันลวด 24 AWG รอบขั้ว 1 ทิศทางเดียวกันทุกรอบ แน่นและเรียงชิด"))
        self.play(ReplacementTransform(cap0, cap1), run_time=0.8)

        # พันลวดรอบฟันที่ 1 — ห่วงรียาวคลุมทั้งความยาวฟัน (อ้อมหน้า-ข้าง-หลัง-ข้าง-หน้า จริง)
        a0 = angs[0]
        pole_dir = np.array([np.cos(a0), np.sin(a0), 0])
        wind_center = STAGE + pole_dir * (R_ARM * 0.55)
        self.cam_focus(wind_center)
        coil_loops = coil_winding(wind_center, pole_dir, color=CURRENT)
        self.play(LaggedStart(*[Create(l) for l in coil_loops], lag_ratio=0.35), run_time=2.2)
        self.wait(0.8)

        lead1 = coil_lead(wind_center, pole_dir, SCHEM_C + R_SCHEM * 0.84 *
                         np.array([np.cos(angs[0]), np.sin(angs[0]), 0]), CURRENT)
        self.play(Create(lead1), run_time=0.8)
        cap2 = self.hud(caption_top("ปลายขดต่อเข้าซี่ 1 → พันขั้ว 2 ต่อ ทิศทางเดียวกันเสมอ"))
        self.play(ReplacementTransform(cap1, cap2), run_time=0.8)
        self.wait(1.2)

        step_hdr2 = self.hud(Text("ขั้นตอนที่ 2 — พันขั้วที่ 2 แล้วต่อซี่ 1→2", font_size=17,
                                  color=WARN).move_to([0, SAFE_LOW_Y, 0]))
        self.play(ReplacementTransform(step_hdr, step_hdr2), run_time=0.5)

        a1 = angs[1]
        pole_dir2 = np.array([np.cos(a1), np.sin(a1), 0])
        wind_center2 = STAGE + pole_dir2 * (R_ARM * 0.55)
        self.cam_focus(wind_center2)
        coil_loops2 = coil_winding(wind_center2, pole_dir2, color=OK)
        self.play(LaggedStart(*[Create(l) for l in coil_loops2], lag_ratio=0.35), run_time=2.0)
        lead2 = coil_lead(wind_center2, pole_dir2, SCHEM_C + R_SCHEM * 0.84 *
                         np.array([np.cos(angs[1]), np.sin(angs[1]), 0]), OK)
        self.play(Create(lead2), run_time=0.8)
        self.wait(1.0)

        step_hdr3 = self.hud(Text("ขั้นตอนที่ 3 — พันขั้วที่ 3 แล้วปิดวง 3→1", font_size=17,
                                  color=WARN).move_to([0, SAFE_LOW_Y, 0]))
        self.play(ReplacementTransform(step_hdr2, step_hdr3), run_time=0.5)

        a2 = angs[2]
        pole_dir3 = np.array([np.cos(a2), np.sin(a2), 0])
        wind_center3 = STAGE + pole_dir3 * (R_ARM * 0.55)
        self.cam_focus(wind_center3)
        coil_loops3 = coil_winding(wind_center3, pole_dir3, color=FORCE)
        self.play(LaggedStart(*[Create(l) for l in coil_loops3], lag_ratio=0.35), run_time=2.0)
        lead3 = coil_lead(wind_center3, pole_dir3, SCHEM_C + R_SCHEM * 0.84 *
                          np.array([np.cos(angs[2]), np.sin(angs[2]), 0]), FORCE)
        lead3b = chord(SCHEM_C, R_SCHEM, angs[2], angs[0], FORCE, sw=5)
        self.play(Create(lead3), Create(lead3b), run_time=1.0)
        self.cam_reset()

        cap3 = self.hud(caption_top("ครบวงพอดี — 3 ขด 3 ซี่ ต่อไล่กันไปจนกลับมาที่ซี่แรก", color=OK))
        self.play(ReplacementTransform(cap2, cap3), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(step_hdr3), run_time=0.4)

        # ------------------------------------------------- ประกอบ + ทดสอบ
        poles, pole_labels, pole_pos = pole_pieces(2, pole_x=1.6)
        cap4 = self.hud(caption_top(
            "ประกอบแม่เหล็กประกบ 2 ข้าง — อย่าลืมปลอกเหล็กอ่อนรอบนอก (โยคนำฟลักซ์กลับ)"))
        self.play(ReplacementTransform(cap3, cap4), FadeIn(poles), FadeIn(pole_labels), run_time=1.2)
        self.wait(2.0)

        cap5 = self.hud(caption_top(
            "ก่อนใส่จริง: วัดต่อเนื่อง (continuity) ด้วยมัลติมิเตอร์ทุกคู่ซี่ ต้องไม่ช็อต/ไม่ขาด",
            color=WARN))
        self.play(ReplacementTransform(cap4, cap5), run_time=0.9)
        self.wait(2.2)

        cap6 = self.hud(caption_top("หมุนด้วยมือก่อนต่อไฟ — ต้องหมุนลื่น ไม่สะดุด ไม่เสียดสีแม่เหล็ก"))
        self.play(ReplacementTransform(cap5, cap6), run_time=0.9)
        self.wait(2.0)

        cap7 = self.hud(caption_top("ต่อไฟจริง ปรับตำแหน่งแปรงถ่านเล็กน้อยจนรอบสูงสุด/นิ่งสุด", color=OK))
        self.play(ReplacementTransform(cap6, cap7), run_time=0.9)
        self.wait(2.0)

        rotor_group = VGroup(core, teeth, bars, nums, coil_loops, coil_loops2, coil_loops3,
                             lead1, lead2, lead3, lead3b)
        self.play(Rotating(rotor_group, angle=TAU * 3, axis=[0, 0, 1], about_point=STAGE,
                           run_time=3.0, rate_func=linear))
        self.wait(0.6)

        # เก็บโมเดลทั้งหมดก่อนขึ้นการ์ดสรุป — กันไม่ให้ N/S ของแม่เหล็ก (อยู่ใกล้กึ่งกลางจอ
        # พอดีสำหรับ config 2 ขั้ว) ไปทับข้อความการ์ด (เจอจริงตอนเรนเดอร์รอบ 2)
        self.play(FadeOut(VGroup(rotor_group, poles, pole_labels)), run_time=0.6)

        summary = overlay_card(self, [
            Text("เสร็จแล้ว — มอเตอร์ 3 ขั้วของ Min", font_size=26, color=OK),
            Text("ทดสอบจริงแล้ววัดรอบ/ความเร็วรถ — ส่งตัวเลขมาคำนวณปรับรอบกันต่อได้",
                 font_size=19, color=GRAYTXT),
        ], move_to=(0, -0.4, 0))
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        self.wait(2.6)

        self.fade_out_all()


class W05a_CameraFollow(_W05Base):
    """มุมกล้องแบบ 1 — กล้องซูม/แพนตามไปโฟกัสฟันที่กำลังพันอยู่ทีละซี่"""
    CAM = "follow"


class W05b_CameraCentered(_W05Base):
    """มุมกล้องแบบ 2 — โมเดลอยู่กลางจอตลอด เอียงแค่นิดเดียว ไม่แพน/ไม่ซูม"""
    CAM = "centered"
