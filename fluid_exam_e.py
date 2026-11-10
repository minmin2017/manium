"""Fluid Power Control exam clips, batch E (2026-11-10, exam 11 Nov).

H6_05_PipeThreads (redo)  hydraulic06 page 8  Pipe Threads: tapered male + female,
interference seal, standard thread (flanks touch first, spiral clearance) vs dry-seal
(roots and crests touch first, no clearance).

Min on the old clip: "ภาพชนกัน ดูไม่รู้เรื่อง" (male/female outlines drawn on top of each
other). Rules used here:
  * pipe = blue, fitting = orange, fills only (no outline strokes), so two parts never
    share a drawn outline; a thin dark sliver separates them in the overview
  * the pipe is screwed in with a world-fixed thread phase (screw motion) and a real
    taper, so the clearance shrinks to the sliver only at the end and the teeth never cross
  * the close-up is a separate big drawing (one tooth pair region), labels sit inside the
    solid colour of each part or in the side gutters, arrows are short
  * one idea on screen at a time
"""
from mlib import *
import numpy as np

PIPE_C = "#4FC3F7"
PIPE_D = "#01579B"
FIT_C = "#FFB74D"
SEAL = "#66BB6A"
GAP_C = "#FF1744"
TAPE_C = "#FAFAFA"
YEL = "#FFD54F"
INK = "#1A1A1A"

# ---- overview geometry (fitting coords: x = 0 at the fitting mouth) ----
SC, OY = 1.3, -0.15
P_O, HD = 0.4, 0.11          # thread pitch, half depth
LT, LP = 2.4, 3.6            # male thread length, pipe length
RI, RO = 0.55, 1.1           # bore radius, pipe outer radius
S_END = 1.8                  # pipe end position (fitting coords) when tight
LTF, LF, RF = 2.0, 3.2, 1.6  # female thread length, fitting length, fitting half height
G = 0.05                     # visual sliver between the parts when tight
OX_F = -0.91                 # fitting mouth (world x) in the assembled view


def rp(u):
    """pitch radius along the pipe (u = 0 at the pipe end); taper drawn exaggerated"""
    return 0.80 - 0.07 * u


def wv(u):
    """thread wave, phase fixed to the fitting (u = x - S_END)"""
    q = ((u + LT) / P_O) % 1.0
    return -HD + 4 * HD * q if q < 0.5 else 3 * HD - 4 * HD * q


def bps(xa, xb):
    xs = [xa]
    k = int(np.floor((xa - (S_END - LT)) / (P_O / 2))) - 1
    while True:
        x = S_END - LT + k * P_O / 2
        if x >= xb - 1e-9:
            break
        if x > xa + 1e-9:
            xs.append(x)
        k += 1
    xs.append(xb)
    return xs


def _poly(pts, ox, fill):
    top = [np.array([ox + SC * x, OY + SC * y, 0.0]) for x, y in pts]
    bot = [np.array([ox + SC * x, OY - SC * y, 0.0]) for x, y in pts]
    a = Polygon(*top).set_fill(fill, 1).set_stroke(width=0)
    b = Polygon(*bot).set_fill(fill, 1).set_stroke(width=0)
    return VGroup(a, b)


def pipe_mob(pe, ox):
    e = (pe - ox) / SC
    pts = [(e - LP, RI), (e - LP, RO), (e - LT, RO)]
    pts += [(x, rp(x - e) + wv(x - S_END)) for x in bps(e - LT, e)]
    pts += [(e, RI)]
    return _poly(pts, ox, PIPE_C)


def fit_mob(ox):
    pts = [(0, RF), (LF, RF), (LF, RI), (LTF, RI)]
    pts += [(x, rp(x - S_END) + wv(x - S_END) + G) for x in reversed(bps(0, LTF))]
    return _poly(pts, ox, FIT_C)


# ---- close-up geometry (one tooth region, male crest at x = 0) ----
ZP = 2.6
ZH = 0.866 * ZP / 2
ZS = 4 * ZH / ZP
Y0, ZX, ZPAD = -0.45, 3.9, 0.95
ZTOP, ZBOT = Y0 + ZH + ZPAD, Y0 - ZH - ZPAD
TC_STD, TR_STD, T_DRY = 0.6, 0.12, 0.3


def zw(x):
    u = ((x + ZP / 2) % ZP) - ZP / 2
    return ZH - ZS * abs(u)


def zkinks(lo, hi):
    xs = {-ZX, ZX}
    for k in range(-3, 4):
        c = k * ZP
        t = c + ZP / 2
        for x in (c, t, c - (ZH - hi) / ZS, c + (ZH - hi) / ZS,
                  t - (lo + ZH) / ZS, t + (lo + ZH) / ZS):
            if -ZX < x < ZX:
                xs.add(round(x, 6))
    return sorted(xs)


def _zline(lo, hi):
    return [np.array([x, Y0 + min(max(zw(x), lo), hi), 0.0]) for x in zkinks(lo, hi)]


def z_male(tc, tr):
    pts = [np.array([-ZX, ZBOT, 0.0])] + _zline(-ZH + tr, ZH - tc) + [np.array([ZX, ZBOT, 0.0])]
    return Polygon(*pts).set_fill(PIPE_C, 1).set_stroke(width=0)


def z_fem(tc, tr):
    pts = [np.array([-ZX, ZTOP, 0.0])] + _zline(-ZH + tc, ZH - tr) + [np.array([ZX, ZTOP, 0.0])]
    return Polygon(*pts).set_fill(FIT_C, 1).set_stroke(width=0)


def z_gaps(tc, tr, color=GAP_C):
    d, dr = tc / ZS, tr / ZS
    g = VGroup()
    for c in (-ZP, 0.0, ZP):
        yb, yt = Y0 + ZH - tc, Y0 + ZH - tr
        g.add(Polygon([c - d, yb, 0], [c + d, yb, 0], [c + dr, yt, 0], [c - dr, yt, 0]))
    for t in (-1.5 * ZP, -0.5 * ZP, 0.5 * ZP, 1.5 * ZP):
        yb, yt = Y0 - ZH + tr, Y0 - ZH + tc
        xl, xr = max(t - d, -ZX), min(t + d, ZX)
        xlr, xrr = max(t - dr, -ZX), min(t + dr, ZX)
        g.add(Polygon([xlr, yb, 0], [xrr, yb, 0], [xr, yt, 0], [xl, yt, 0]))
    g.set_fill(color, 1).set_stroke(width=0)
    return g


def z_flanks(tc):
    g = VGroup()
    a, b = tc / ZS, (2 * ZH - tc) / ZS
    for c in (-ZP, 0.0, ZP):
        for s in (-1, 1):
            g.add(Line([c + s * a, Y0 + ZH - tc, 0], [c + s * b, Y0 - ZH + tc, 0],
                       color=SEAL, stroke_width=8))
    return g


def z_crests(t):
    g = VGroup()
    h = t / ZS
    for c in (-ZP, 0.0, ZP):
        g.add(Line([c - h, Y0 + ZH - t, 0], [c + h, Y0 + ZH - t, 0], color=SEAL, stroke_width=11))
    for tt in (-0.5 * ZP, 0.5 * ZP):
        g.add(Line([tt - h, Y0 - ZH + t, 0], [tt + h, Y0 - ZH + t, 0], color=SEAL, stroke_width=11))
    return g


def T(s, size=26, color=WHITE):
    return Text(s, font_size=size, color=color)


def side_label(lines, color, x, y, size=26, max_w=2.75):
    g = VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.14)
    fit_width(g, max_w)
    return g.move_to([x, y, 0])


class H6_05_PipeThreads(SafeScene):
    """hydraulic06 page 8, rebuilt for a zero-background viewer."""

    # ---------------------------------------------------------------- helpers
    def step(self, n, name):
        m = T(f"ขั้น {n} · {name}", 22, OK)
        fit_width(m, (-self.ttl.width / 2) - (-7.11 + 0.3) - 0.35)
        m.move_to([-7.11 + 0.3 + m.width / 2, TITLE_Y, 0])
        if self.step_m is not None:
            self.play(FadeOut(self.step_m, run_time=0.3))
        self.play(FadeIn(m, shift=0.2 * RIGHT), run_time=0.5)
        self.step_m = m

    def cap(self, txt, color=GRAYTXT, wait=2.4):
        m = caption_top(txt, color=color, size=26, max_w=12.9)
        if self.cap_m is not None:
            self.play(FadeOut(self.cap_m, run_time=0.3))
        self.play(FadeIn(m), run_time=0.6)
        self.cap_m = m
        if wait:
            self.wait(wait)
        return m

    def clear_cap(self):
        if self.cap_m is not None:
            self.play(FadeOut(self.cap_m, run_time=0.3))
            self.cap_m = None

    def zoom_parts(self, tc, tr):
        frame = Rectangle(width=2 * ZX, height=ZTOP - ZBOT, color=GRAYTXT, stroke_width=3)
        frame.move_to([0, (ZTOP + ZBOT) / 2, 0])
        male, fem = z_male(tc, tr), z_fem(tc, tr)
        lf = T("ข้อต่อ (เกลียวใน)", 26, INK).move_to([0, Y0 + ZH + 0.47, 0])
        lm = T("ท่อ (เกลียวนอก)", 26, INK).move_to([0, Y0 - ZH - 0.5, 0])
        return frame, male, fem, lf, lm

    # ---------------------------------------------------------------- scene
    def construct(self):
        self.step_m = None
        self.cap_m = None
        ttl = title("เกลียวท่อ (Pipe Threads)", size=28)
        self.ttl = ttl
        ref = page_ref("hydraulic06 · หน้า 8", size=18)
        self.play(FadeIn(ttl), FadeIn(ref))
        self.cap("ท่อน้ำมันขันเข้ากับข้อต่อด้วยเกลียว — ทำไมน้ำมันแรงดันสูงไม่รั่วออกมา?",
                 color=YEL, wait=2.6)

        # ===== 1. the pipe alone =====
        self.step(1, "ชิ้นที่ 1: ท่อ")
        pe = ValueTracker(-1.2)
        ox = ValueTracker(1.6)
        pipe = pipe_mob(pe.get_value(), ox.get_value())
        self.cap("ดูภาพตัดครึ่ง: ผนังท่อบน-ล่าง ตรงกลางเป็นรูให้น้ำมันไหล", wait=0)
        self.play(FadeIn(pipe, shift=0.3 * RIGHT), run_time=1.2)
        bore = T("รูน้ำมัน", 26, GRAYTXT).move_to([-3.6, OY, 0])
        self.play(FadeIn(bore), run_time=0.6)
        self.wait(1.6)

        e1 = (pe.get_value() - ox.get_value()) / SC
        xt_mid = ox.get_value() + SC * (e1 - LT / 2)
        lab_pipe = T("ท่อ (เกลียวนอก)", 30, PIPE_C).move_to([xt_mid, -2.75, 0])
        arr_pipe = Arrow([xt_mid, -2.45, 0], [xt_mid, OY - SC * 1.02 - 0.06, 0], buff=0,
                         color=PIPE_C, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        self.cap("ปลายท่อมีฟันเกลียวอยู่ที่ผิวด้านนอก = เกลียวนอก (ตัวผู้)", wait=0)
        self.play(FadeIn(lab_pipe), GrowArrow(arr_pipe), run_time=0.9)
        self.wait(2.2)

        # taper of the male thread
        x0w = ox.get_value() + SC * (e1 - LT)
        x1w = ox.get_value() + SC * e1
        y0w = OY + SC * (rp(-LT) + HD) + 0.07
        y1w = OY + SC * (rp(0) + HD) + 0.07
        tap = DashedLine([x0w, y0w, 0], [x1w, y1w, 0], color=YEL, stroke_width=4)
        ref_l = DashedLine([x0w, y0w, 0], [x1w, y0w, 0], color=GRAYTXT, stroke_width=2)
        lab_tap = T("เรียว (taper): ยิ่งไปทางปลาย ยิ่งเล็กลง", 26, YEL)
        lab_tap.move_to([(x0w + x1w) / 2 - 0.4, 1.85, 0])
        self.cap("เกลียวท่อไม่ตรง แต่ 'เรียว' (วาดเรียวเกินจริงให้เห็นชัด)", wait=0)
        self.play(Create(ref_l), Create(tap), FadeIn(lab_tap), run_time=1.2)
        self.wait(2.4)
        self.play(FadeOut(tap, ref_l, lab_tap), run_time=0.5)

        # ===== 2. the fitting alone =====
        self.step(2, "ชิ้นที่ 2: ข้อต่อ")
        fit = fit_mob(ox.get_value())
        self.cap("ข้อต่อ (หรือตัววาล์ว/ปั๊ม) มีรูเจาะเกลียวอยู่ผิวด้านใน", wait=0)
        self.play(FadeIn(fit, shift=0.3 * LEFT), run_time=1.2)
        lab_fit = T("ข้อต่อ (เกลียวใน)", 30, FIT_C).move_to([ox.get_value() + SC * LF / 2, -2.75, 0])
        xin = ox.get_value() + SC * 0.95
        lab_in = T("เกลียวใน", 24, FIT_C).move_to([xin, OY, 0])
        a_up = Arrow([xin, OY + 0.22, 0], [xin, OY + SC * 0.70, 0], buff=0, color=FIT_C,
                     stroke_width=4, max_tip_length_to_length_ratio=0.35)
        a_dn = Arrow([xin, OY - 0.22, 0], [xin, OY - SC * 0.70, 0], buff=0, color=FIT_C,
                     stroke_width=4, max_tip_length_to_length_ratio=0.35)
        self.play(FadeIn(lab_fit), FadeIn(lab_in), GrowArrow(a_up), GrowArrow(a_dn), run_time=0.9)
        self.wait(2.0)
        self.cap("เกลียวในก็เรียวเหมือนกัน: ปากรูกว้าง ลึกเข้าไปแคบลง — รับกับท่อพอดี", wait=2.6)

        # ===== 3. screw them together =====
        self.step(3, "ขันเข้าด้วยกัน")
        self.play(FadeOut(lab_pipe, arr_pipe, lab_fit, lab_in, a_up, a_dn, bore), run_time=0.5)
        self.remove(pipe, fit)
        pipe = always_redraw(lambda: pipe_mob(pe.get_value(), ox.get_value()))
        fit = always_redraw(lambda: fit_mob(ox.get_value()))
        self.add(fit, pipe)
        icon = Arc(radius=0.3, start_angle=0.3 * PI, angle=1.5 * PI, color=YEL, stroke_width=5)
        icon.add_tip(tip_length=0.16, tip_width=0.16)
        icon.move_to([-5.9, 1.9, 0])
        lab_rot = T("หมุนขัน", 24, YEL).next_to(icon, RIGHT, buff=0.2)
        self.cap("หมุนท่อขันเข้าไปช้าๆ — ตอนแรกยังหลวม มีช่องห่าง", wait=0)
        self.play(FadeIn(icon), FadeIn(lab_rot), run_time=0.5)
        pe_f = OX_F + SC * S_END
        e_mid = 0.9
        self.play(ox.animate.set_value(OX_F), pe.animate.set_value(OX_F + SC * e_mid),
                  Rotate(icon, -3 * PI), run_time=4.5, rate_func=linear)
        self.cap("ยิ่งขันลึก เกลียวเรียวยิ่งเบียดกันแน่นขึ้น", wait=0)
        self.play(pe.animate.set_value(pe_f), Rotate(icon, -2.5 * PI), run_time=3.5,
                  rate_func=rate_functions.ease_out_sine)
        self.play(FadeOut(icon, lab_rot), run_time=0.4)
        pipe.clear_updaters()
        fit.clear_updaters()
        self.cap("ขันแน่น: เกลียวบีบอัดกันเอง (interference) = ซีลด้วยเกลียว ไม่ต้องใช้ปะเก็น",
                 color=OK, wait=0)
        lab_p2 = T("ท่อ", 30, PIPE_C).move_to([OX_F + SC * (S_END - LP + 0.6), -1.95, 0])
        lab_f2 = T("ข้อต่อ", 30, FIT_C).move_to([OX_F + SC * LF / 2, -2.75, 0])
        self.play(FadeIn(lab_p2), FadeIn(lab_f2), run_time=0.6)
        self.wait(2.6)

        # zoom marker -> close-up
        zx = OX_F + SC * 0.9
        zy = OY + SC * rp(0.9 - S_END)
        mark = Square(side_length=0.8, color=YEL, stroke_width=5).move_to([zx, zy, 0])
        self.cap("ส่องใกล้ๆ ตรงกรอบเหลือง: ฟันเกลียวท่อ กับ ฟันเกลียวข้อต่อ", wait=0)
        self.play(Create(mark), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(pipe, fit, lab_p2, lab_f2), run_time=0.6)
        frame, zm, zf, lf, lm = self.zoom_parts(TC_STD, TR_STD)
        self.play(ReplacementTransform(mark, frame), run_time=1.0)
        self.play(FadeIn(zm), FadeIn(zf), run_time=0.8)
        self.play(FadeIn(lf), FadeIn(lm), run_time=0.6)
        self.wait(1.4)

        # flank contact
        fl = z_flanks(TC_STD)
        lab_fl = side_label(["หน้าข้างเกลียว", "(flank) แตะกัน", "= แนวซีล"], SEAL, -5.5, Y0 + 0.75)
        a_fl = Arrow([-4.12, Y0, 0], [-3.32, Y0, 0], buff=0, color=SEAL, stroke_width=6,
                     max_tip_length_to_length_ratio=0.4)
        self.cap("เกลียวมาตรฐาน: ด้านข้างของฟัน (flank) แตะกันก่อน — เส้นเขียว", wait=0)
        self.play(Create(fl), run_time=1.2)
        self.play(FadeIn(lab_fl), GrowArrow(a_fl), run_time=0.7)
        self.wait(2.4)

        # spiral clearance
        gaps = z_gaps(TC_STD, TR_STD)
        gy = Y0 + ZH - (TC_STD + TR_STD) / 2
        lab_gp = side_label(["ช่องเกลียวงู", "(spiral clearance)", "= ทางรั่ว"], GAP_C, 5.5, gy + 0.75)
        a_gp = Arrow([4.12, gy, 0], [ZP + 0.27, gy, 0], buff=0, color=GAP_C, stroke_width=6,
                     max_tip_length_to_length_ratio=0.3)
        self.cap("แต่ที่ยอดกับโคนฟัน ยังเหลือช่องว่าง (สีแดง)", wait=0)
        self.play(FadeIn(gaps), run_time=0.8)
        self.play(Indicate(gaps, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.play(FadeIn(lab_gp), GrowArrow(a_gp), run_time=0.7)
        self.wait(2.4)
        zoom_all = VGroup(frame, zm, zf, lf, lm, fl, gaps, lab_fl, a_fl, lab_gp, a_gp)
        self.play(FadeOut(zoom_all), run_time=0.6)

        # leak path: the gap winds round the pipe like a spring
        Y1, R = -0.35, 1.0
        body = Rectangle(width=7.0, height=2 * R, color=PIPE_C, stroke_width=0)
        body.set_fill(PIPE_C, 0.9).move_to([0, Y1, 0])
        crests = VGroup(*[Line([-3.0 + k + 0.5, Y1 - R, 0], [-3.0 + k + 1.0, Y1 + R, 0],
                               color=PIPE_D, stroke_width=5) for k in range(6)])
        groove = VGroup(*[Line([-3.0 + k, Y1 - R, 0], [-3.0 + k + 0.5, Y1 + R, 0],
                               color=GAP_C, stroke_width=7) for k in range(6)])
        path_pts = []
        for k in range(5, -1, -1):
            x = -3.0 + k
            path_pts += [[x + 1.0, Y1 - R, 0], [x + 0.5, Y1 + R, 0], [x, Y1 - R, 0]]
        dedup = [path_pts[0]]
        for p in path_pts[1:]:
            if p != dedup[-1]:
                dedup.append(p)
        path = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in dedup])
        lab_in2 = T("ด้านในข้อต่อ: น้ำมันแรงดันสูง", 26, WHITE).move_to([1.6, Y1 + R + 0.5, 0])
        lab_out = T("ซึมออกข้างนอก", 26, GAP_C).move_to([-1.3, Y1 - R - 0.75, 0])
        self.cap("มองทะลุข้อต่อ: ช่องแดงนี้วนรอบท่อเป็นเกลียวต่อกัน เหมือนสปริง", wait=0)
        self.play(FadeIn(body), Create(crests), run_time=0.9)
        self.play(Create(groove), run_time=1.4)
        self.play(FadeIn(lab_in2), run_time=0.5)
        self.wait(1.2)
        dot = Dot([3.0, Y1 - R, 0], radius=0.13, color=YEL)

        def _front(m):
            x = m.get_center()[0]
            frac = (x + 3.0) % 1.0
            m.set_opacity(1.0 if frac <= 0.5 + 1e-6 else 0.25)

        dot.add_updater(_front)
        self.cap("น้ำมันวิ่งวนตามช่องนี้ จนซึมออกมาข้างนอกได้", wait=0)
        self.play(FadeIn(dot), run_time=0.3)
        self.play(MoveAlongPath(dot, path), run_time=4.0, rate_func=linear)
        dot.clear_updaters()
        dot.set_opacity(1.0)
        self.play(dot.animate.shift(0.6 * DOWN), FadeIn(lab_out), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(body, crests, groove, dot, lab_in2, lab_out), run_time=0.6)

        # ===== 4. PTFE tape / sealant =====
        self.step(4, "เทป PTFE / น้ำยาซีล")
        frame, zm, zf, lf, lm = self.zoom_parts(TC_STD, TR_STD)
        gaps = z_gaps(TC_STD, TR_STD)
        self.cap("ทางแก้ของเกลียวมาตรฐาน: พันเทป PTFE หรือทาน้ำยาซีลก่อนขัน", wait=0)
        self.play(FadeIn(frame, zm, zf, lf, lm, gaps), run_time=0.8)
        self.wait(1.4)
        tape = z_gaps(TC_STD, TR_STD, TAPE_C)
        lab_tp = side_label(["เทป / น้ำยา", "เข้าไปเต็ม", "ช่องว่าง"], TAPE_C, 5.5, gy + 0.75)
        a_tp = Arrow([4.12, gy, 0], [ZP + 0.27, gy, 0], buff=0, color=TAPE_C, stroke_width=6,
                     max_tip_length_to_length_ratio=0.3)
        self.cap("ขันแล้ว เทป/น้ำยาถูกบีบเข้าไปอุดช่องแดงจนเต็ม", wait=0)
        self.play(Transform(gaps, tape), run_time=1.4)
        self.play(FadeIn(lab_tp), GrowArrow(a_tp), run_time=0.7)
        self.wait(1.2)
        self.cap("ช่องเกลียวงูถูกปิด → ไม่มีทางรั่ว", color=OK, wait=2.2)
        self.play(FadeOut(lab_tp, a_tp), run_time=0.4)

        # ===== 5. the two thread types on page 8, one at a time =====
        self.step(5, "เทียบ 2 แบบ")
        red = z_gaps(TC_STD, TR_STD)
        tagA = T("แบบที่ 1: เกลียวมาตรฐาน (Standard เช่น NPT)", 26, WHITE).move_to([0, 2.05, 0])
        self.cap("หน้า 8 มีเกลียวเรียว 2 แบบ — ดูทีละแบบ", wait=0)
        self.play(Transform(gaps, red), FadeIn(tagA), run_time=0.8)
        fl = z_flanks(TC_STD)
        lA = side_label(["แตะกันที่", "หน้าข้าง (flank)"], SEAL, -5.5, Y0 + 0.5)
        rA = side_label(["มีช่องเกลียวงู", "→ ต้องใช้", "เทป / น้ำยา"], GAP_C, 5.5, Y0 + 0.5)
        self.play(Create(fl), FadeIn(lA), run_time=0.8)
        self.play(FadeIn(rA), run_time=0.6)
        self.wait(2.6)

        tagB = T("แบบที่ 2: เกลียว Dry-seal (เช่น NPTF)", 26, WHITE).move_to([0, 2.05, 0])
        self.play(FadeOut(lA, rA, fl), run_time=0.4)
        self.play(FadeOut(gaps), FadeOut(tagA, run_time=0.3), run_time=0.5)
        self.play(FadeIn(tagB), run_time=0.4)
        self.cap("Dry-seal: ทำยอดกับโคนฟันให้พอดีกัน", wait=0)
        self.play(Transform(zm, z_male(T_DRY, T_DRY)), Transform(zf, z_fem(T_DRY, T_DRY)),
                  run_time=1.6)
        cr = z_crests(T_DRY)
        lB = side_label(["ยอด + โคนฟัน", "แตะกันก่อน"], SEAL, -5.5, Y0 + 0.5)
        rB = side_label(["ไม่มีช่องว่าง", "→ ไม่ต้องพึ่ง", "เทป / น้ำยา"], OK, 5.5, Y0 + 0.5)
        self.play(Create(cr), FadeIn(lB), run_time=0.9)
        self.play(Indicate(cr, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.play(FadeIn(rB), run_time=0.6)
        self.cap("ยอด-โคนบดแนบกันสนิท → ไม่เหลือช่องเกลียวงู ซีลได้แบบ 'แห้ง' (dry)",
                 color=OK, wait=2.8)
        self.play(FadeOut(frame, zm, zf, lf, lm, cr, lB, rB, tagB), run_time=0.6)

        # ---- comparison table, one row at a time ----
        self.clear_cap()
        cx = [-4.45, -0.05, 4.4]
        ys = [1.95, 1.1, 0.3, -0.5, -1.3, -2.15]
        cw = [3.5, 3.9, 3.9]
        hdr = [None, T("มาตรฐาน (เช่น NPT)", 26, GAP_C), T("Dry-seal (เช่น NPTF)", 26, SEAL)]
        rows = [
            ["รูปเกลียว", "เรียว (taper)", "เรียว (taper)"],
            ["แตะกันก่อนที่", "หน้าข้าง (flank)", "ยอด + โคน"],
            ["ช่องเกลียวงู", "มี → รั่วได้", "ไม่มี"],
            ["เทป / น้ำยาซีล", "ต้องใช้ช่วย", "ไม่ต้องใช้"],
        ]
        grid = VGroup()
        for yl in (1.52, 0.7, -0.1, -0.9, -1.7):
            grid.add(Line([-6.4, yl, 0], [6.6, yl, 0], color="#546E7A", stroke_width=2))
        for xl in (-2.15, 2.15):
            grid.add(Line([xl, 2.3, 0], [xl, -1.7, 0], color="#546E7A", stroke_width=2))
        for j in (1, 2):
            fit_width(hdr[j], cw[j]).move_to([cx[j], ys[0], 0])
        self.cap("สรุปเป็นตาราง (ทีละแถว)", wait=0)
        self.play(Create(grid), FadeIn(hdr[1]), FadeIn(hdr[2]), run_time=1.0)
        cells = VGroup()
        for i, r in enumerate(rows):
            row = VGroup()
            for j, s in enumerate(r):
                col = YEL if j == 0 else WHITE
                m = fit_width(T(s, 26, col), cw[j]).move_to([cx[j], ys[i + 1], 0])
                row.add(m)
            self.play(FadeIn(row, shift=0.15 * DOWN), run_time=0.6)
            self.wait(1.7)
            cells.add(row)
        last_l = fit_width(T("ซีลด้วยอะไร", 26, YEL), cw[0]).move_to([cx[0], ys[5], 0])
        last_r = fit_width(T("เกลียวบีบอัดกันเอง (ไม่ใช่ปะเก็น / O-ring) — ทั้ง 2 แบบ", 26, OK),
                           8.4).move_to([2.2, ys[5], 0])
        self.play(FadeIn(last_l, last_r, shift=0.15 * DOWN), run_time=0.6)
        self.wait(2.4)
        self.play(FadeOut(grid, hdr[1], hdr[2], cells, last_l, last_r, self.cap_m), run_time=0.6)
        self.cap_m = None

        # ===== 6. exam point + check =====
        self.step(6, "จุดออกสอบ")
        head = T("ข้อเสียของเกลียวเรียว", 32, WARN).move_to([0, 1.6, 0])
        d1 = T("1) ถอด-ประกอบบ่อยๆ → เกลียวเสีย", 30, WHITE).move_to([0, 0.5, 0])
        d2 = T("2) ขันแน่นเกินไป → ข้อต่อแตก", 30, WHITE).move_to([0, -0.5, 0])
        self.play(FadeIn(head), run_time=0.6)
        self.play(FadeIn(d1, shift=0.15 * DOWN), run_time=0.6)
        self.wait(1.8)
        self.play(FadeIn(d2, shift=0.15 * DOWN), run_time=0.6)
        self.wait(2.2)
        self.play(FadeOut(head, d1, d2), run_time=0.5)

        q = T("ถาม: เกลียวแบบไหนไม่ต้องพึ่งเทป/น้ำยา? เพราะอะไร?", 30, YEL).move_to([0, 1.1, 0])
        fit_width(q, 12.6)
        a1 = T("ตอบ: Dry-seal", 30, OK).move_to([0, 0.0, 0])
        a2 = T("ยอด+โคนแตะกันก่อน → ไม่มีช่องเกลียวงู", 28, WHITE).move_to([0, -0.9, 0])
        self.play(FadeIn(q), run_time=0.6)
        self.wait(2.6)
        self.play(FadeIn(a1), run_time=0.5)
        self.play(FadeIn(a2), run_time=0.5)
        self.wait(2.8)
        self.fade_out_all(run_time=0.8)
