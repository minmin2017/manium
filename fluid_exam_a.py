"""
fluid_exam_a.py -- Fluid Power Control, exam 11 Nov 2026, batch A (take-home 1 + ch 7 motor homework).

Every number comes from the python-verified notes:
  Exam_Prep/Fluid Power Control/W04-06 การบ้าน take-home 1 — เฉลย.md
  Exam_Prep/Fluid Power Control/W05 การบ้าน บท 6-7 — เฉลย.md

FX01_TakeHomeFlowPressure -- take-home 1 items 1-4 (Q, P_RE, P_HE, P_pump)
FX02_TakeHomePumpPower    -- take-home 1 items 5-9 (V_D, T_A, kW, eta_hyd, eta_total)
FX03_MotorEfficiency      -- 7-34M, 7-36M, 7-37E (hydraulic motor efficiencies)
FX04_Hydrostatic          -- 7-40M hydrostatic transmission (in^3 vs cm^3 doubt shown)

fx_graph.png = figure 2 of the take-home with the two pixel-measured readings marked.
"""

import os
import numpy as np
from manim import *
from mlib import *

HERE = os.path.dirname(os.path.abspath(__file__))

Q_C = "#FFB74D"      # supply oil / flow
RET_C = "#4FC3F7"    # return oil / rod-end side
VAL_C = "#FFF176"    # valve pressure drop
PIPE_C = "#BCAAA4"   # pipe friction loss
W_C = "#66BB6A"      # weight / force
V_C = "#FFD54F"      # velocity
AREA_C = "#CE93D8"   # areas
SHAFT_C = "#B0BEC5"  # shaft
TQ_C = "#BA68C8"     # torque
N_C = "#80DEEA"      # speed
EL_C = "#FFEE58"     # electric
PX = 0.75            # left edge of the right-hand panel
NM = r"\ \text{N}\!\cdot\!\text{m}"


def P2(x, y):
    return np.array([x, y, 0.0])


def T(txt, size=22, color=WHITE):
    return Text(txt, font_size=size, color=color)


def M(tex, size=34, color=WHITE):
    return MathTex(tex, font_size=size, color=color)


def MP(*parts, size=34, color=WHITE, colors=None):
    m = MathTex(*parts, font_size=size, color=color)
    if colors:
        for i, c in colors.items():
            m[i].set_color(c)
    return m


def place_left(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


_CUR = [2.2]


def prow(mob, i, y0=None, dy=0.64, x=PX, max_w=6.1, gap=0.18):
    """right-panel row, left-aligned at PX. Without y0 rows stack top-down (i == 0 starts a new panel),
    so tall fractions never collide with the next row."""
    fit_width(mob, max_w)
    if y0 is not None:
        return place_left(mob, x, y0 - dy * i)
    if i == 0:
        _CUR[0] = 2.2
    mob.move_to([x + mob.width / 2, _CUR[0] - mob.height / 2, 0])
    _CUR[0] = mob.get_bottom()[1] - gap
    return mob


def boxed(mob, color=OK):
    return VGroup(mob, SurroundingRectangle(mob, color=color, buff=0.09, stroke_width=3))


def lab(mob, x, y):
    """figure label, left-aligned at x."""
    return place_left(mob, x, y)


class ExamScene(SafeScene):
    _cap = None
    SAY_HOLD = 2.0
    PACE = 1.3

    def setup(self):
        super().setup()
        self.rows = Group()

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * self.PACE, *args, **kwargs)

    def say(self, txt, size=22):
        new = caption_top(txt, size=size, max_w=13.2)
        if self._cap is not None:
            self.play(FadeOut(self._cap), run_time=0.3)
            self.play(FadeIn(new), run_time=0.4)
        else:
            self.play(FadeIn(new), run_time=0.6)
        self._cap = new
        super().wait(self.SAY_HOLD)

    def glow(self, term, fig, color, rt=1.4):
        wide = term.width > 3.2 or isinstance(term, Text)
        anims = [Indicate(term, color=WHITE, scale_factor=1.0 if wide else 1.2),
                 Circumscribe(term, color=color, buff=0.04, stroke_width=3, fade_out=True)]
        if fig is not None:
            anims.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*anims, run_time=rt)

    def show(self, *mobs, rt=0.8):
        for m in mobs:
            self.rows.add(m)
        self.play(*[FadeIn(m, shift=LEFT * 0.15) for m in mobs], run_time=rt)

    def clear_panel(self):
        if len(self.rows):
            self.play(FadeOut(self.rows), run_time=0.5)
        self.rows = Group()

    def header(self, ttl, ref):
        self.add(fit_width(title(ttl, size=28), 8.3), page_ref(ref))


# =====================================================================
# take-home 1 figure: vertical cylinder, pump, DCV, tank
# =====================================================================
CX, IW = -3.6, 1.7
XL, XR = CX - IW / 2, CX + IW / 2
BOT, TOP = -3.3, 0.3
PY0 = -1.9
RW = 0.85
Y_HE, Y_RE = -3.0, -0.05
PUMP = P2(-6.4, Y_HE)
VS, VR = P2(-5.5, Y_HE), P2(-5.5, Y_RE)


def th1_figure():
    walls = VGroup(
        Line(P2(XL - 0.06, BOT - 0.06), P2(XL - 0.06, TOP + 0.06), color=METAL, stroke_width=8),
        Line(P2(XR + 0.06, BOT - 0.06), P2(XR + 0.06, TOP + 0.06), color=METAL, stroke_width=8),
        Line(P2(XL - 0.1, BOT - 0.06), P2(XR + 0.1, BOT - 0.06), color=METAL, stroke_width=8),
        Line(P2(XL - 0.1, TOP + 0.06), P2(CX - RW / 2 - 0.04, TOP + 0.06), color=METAL, stroke_width=8),
        Line(P2(CX + RW / 2 + 0.04, TOP + 0.06), P2(XR + 0.1, TOP + 0.06), color=METAL, stroke_width=8))
    piston = Rectangle(width=IW, height=0.3, color=WHITE, stroke_width=2,
                       fill_color=METAL, fill_opacity=1).move_to(P2(CX, PY0))
    rtop = 1.0
    rod = Rectangle(width=RW, height=rtop - (PY0 + 0.15), color=WHITE, stroke_width=2,
                    fill_color="#78909C", fill_opacity=1).move_to(P2(CX, (rtop + PY0 + 0.15) / 2))
    wbox = Rectangle(width=1.6, height=0.7, color=W_C, stroke_width=3,
                     fill_color="#2E7D32", fill_opacity=0.6).move_to(P2(CX, rtop + 0.35))
    wtxt = M("W", 32, WHITE).move_to(wbox)
    varr = Arrow(P2(XR + 0.35, rtop), P2(XR + 0.35, rtop + 0.75), buff=0, color=V_C, stroke_width=5,
                 tip_length=0.18)
    vlab = lab(M(r"v=0.10\ \text{m/s}", 26, V_C), XR + 0.55, rtop + 0.37)
    mover = VGroup(piston, rod, wbox, wtxt, varr, vlab)

    he_oil = always_redraw(lambda: Rectangle(
        width=IW, height=max(piston.get_bottom()[1] - BOT, 0.01), stroke_width=0,
        fill_color=Q_C, fill_opacity=0.45).align_to(P2(XL, BOT), DL))
    w_ann = (IW - RW) / 2

    def re_oil():
        h = max(TOP - piston.get_top()[1], 0.01)
        return VGroup(*[Rectangle(width=w_ann, height=h, stroke_width=0, fill_color=RET_C,
                                  fill_opacity=0.45).align_to(P2(x0, TOP), UL) for x0 in (XL, CX + RW / 2)])
    re_oil_m = always_redraw(re_oil)

    pump = VGroup(Circle(radius=0.28, color=WHITE, stroke_width=3).move_to(PUMP),
                  Triangle(color=WHITE, fill_opacity=1).scale(0.1).move_to(PUMP + P2(0, 0.12)))
    tank = VGroup(VMobject(color=WHITE, stroke_width=3).set_points_as_corners(
        [P2(-6.75, 1.15), P2(-6.75, 0.75), P2(-6.05, 0.75), P2(-6.05, 1.15)]),
        Rectangle(width=0.66, height=0.25, stroke_width=0, fill_color=RET_C, fill_opacity=0.5).move_to(P2(-6.4, 0.89)))
    sup = Line(PUMP + P2(0.28, 0), P2(XL - 0.06, Y_HE), color=Q_C, stroke_width=6)
    ret = VMobject(color=RET_C, stroke_width=6).set_points_as_corners(
        [P2(XL - 0.06, Y_RE), P2(-6.4, Y_RE), P2(-6.4, 0.75)])
    sup_pipe = Line(VS + P2(0.21, 0), P2(XL - 0.06, Y_HE), color=PIPE_C, stroke_width=10)
    ret_pipe = Line(VR + P2(0.21, 0), P2(XL - 0.06, Y_RE), color=PIPE_C, stroke_width=10)
    vsup = Square(0.42, color=VAL_C, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(VS)
    vret = Square(0.42, color=VAL_C, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(VR)
    a_sup = Arrow(P2(-5.2, Y_HE), P2(-4.75, Y_HE), buff=0, color=Q_C, stroke_width=5, tip_length=0.16)
    a_ret = Arrow(P2(-4.75, Y_RE), P2(-5.2, Y_RE), buff=0, color=RET_C, stroke_width=5, tip_length=0.16)
    labels = dict(
        pump=T("ปั๊ม", 20).move_to(PUMP + P2(0, 0.48)),
        pa=T("P→A", 19, VAL_C).move_to(VS + P2(0, 0.42)),
        bt=T("B→T", 19, VAL_C).move_to(VR + P2(0, -0.44)),
        sp=T("ท่อส่ง 15 m", 18, PIPE_C).move_to(P2(-5.15, -3.45)),
        rp=T("ท่อกลับ 20 m", 18, PIPE_C).move_to(P2(-5.25, 0.37)),
        tank=T("ถัง 0 bar", 20, RET_C).move_to(P2(-6.35, 1.5)),
        re=lab(T("RE ด้านก้าน (บน)", 20, RET_C), XR + 0.3, -0.6),
        he=lab(T("HE ด้านหัว (ล่าง)", 20, Q_C), XR + 0.3, -2.75),
    )
    dims = VGroup(
        DoubleArrow(P2(XL + 0.04, -3.05), P2(XR - 0.04, -3.05), buff=0, color=AREA_C, stroke_width=3,
                    tip_length=0.14),
        M(r"D_{bore}=3\ \text{in}", 22, AREA_C).move_to(P2(CX, -2.68)),
        DoubleArrow(P2(CX - RW / 2, 0.65), P2(CX + RW / 2, 0.65), buff=0, color=AREA_C, stroke_width=3,
                    tip_length=0.12),
        lab(M(r"D_{rod}=1.5\ \text{in}", 22, AREA_C), XR + 0.3, 0.62))
    return dict(walls=walls, piston=piston, rod=rod, wbox=wbox, mover=mover, varr=varr, vlab=vlab,
                he_oil=he_oil, re_oil=re_oil_m, pump=pump, tank=tank, sup=sup, ret=ret,
                sup_pipe=sup_pipe, ret_pipe=ret_pipe, vsup=vsup, vret=vret, a_sup=a_sup, a_ret=a_ret,
                labels=labels, dims=dims)


def ann_box(f):
    """static outline of the rod-end annulus at the piston's current height (for glow)."""
    pt = f["piston"].get_top()[1]
    w = (IW - RW) / 2
    return VGroup(*[Rectangle(width=w, height=TOP - pt, color=WHITE, stroke_width=3).align_to(P2(x0, TOP), UL)
                    for x0 in (XL, CX + RW / 2)])


class FX01_TakeHomeFlowPressure(ExamScene):
    def construct(self):
        self.header("Take-home 1 ข้อ 1–4: อัตราไหล และความดัน", "take-home 1 · รูป 1-2")
        f = th1_figure()
        L = f["labels"]
        self.say("ระบบยกของ: ปั๊มดันน้ำมันเข้ากระบอกสูบด้านล่าง ลูกสูบดันก้านยกน้ำหนัก 3 ตัน ขึ้นช้าๆ")
        self.play(Create(f["walls"]), FadeIn(f["he_oil"]), FadeIn(f["re_oil"]), FadeIn(f["mover"][:4]),
                  run_time=1.5)
        self.play(Create(f["sup"]), Create(f["ret"]), FadeIn(f["pump"]), FadeIn(f["tank"]),
                  FadeIn(f["vsup"]), FadeIn(f["vret"]), run_time=1.4)
        self.play(FadeIn(L["pump"]), FadeIn(L["pa"]), FadeIn(L["bt"]), FadeIn(L["tank"]))
        self.say("ส้ม = น้ำมันจากปั๊ม เข้าด้าน HE (ด้านหัว ไม่มีก้าน) · ฟ้า = น้ำมันด้าน RE (ด้านก้าน) ถูกบีบกลับถัง")
        self.play(FadeIn(L["he"]), GrowArrow(f["a_sup"]))
        self.play(FadeIn(L["re"]), GrowArrow(f["a_ret"]))
        self.wait(1.0)
        self.play(FadeIn(f["dims"]), GrowArrow(f["varr"]), FadeIn(f["vlab"]))
        self.say("ข้อมูล: ลูกสูบโต 3 in (เส้นผ่านศูนย์กลาง ไม่ใช่รัศมี) · ก้านโต 1.5 in · v = 10 cm/s · W = 3 ตัน")
        self.wait(1.5)

        # ---------------- item 1: Q
        self.say("ข้อ 1 · ขั้น 1 เข้าใจ: ลูกสูบขึ้น 10 cm ทุก 1 วินาที → ใต้ลูกสูบต้องเติมน้ำมันเป็นแท่งยาว 10 cm ต่อวินาที")
        slug = Rectangle(width=IW, height=0.5, color=WHITE, stroke_width=3).align_to(P2(XL, PY0 - 0.15), DL)
        slab = lab(T("แท่งน้ำมันที่เติมใน 1 วินาที", 19, Q_C), XR + 0.3, -1.85)
        self.play(f["mover"].animate.shift(UP * 0.5), run_time=2.0, rate_func=linear)
        self.play(Create(slug), FadeIn(slab))
        self.wait(1.0)
        t0 = prow(T("ข้อ 1  หา Q (อัตราไหลน้ำมัน)", 26, OK), 0)
        e1 = prow(MP("Q", "=", "A_{bore}", r"\cdot", "v", size=44,
                     colors={0: Q_C, 2: AREA_C, 4: V_C}), 1.1)
        self.say("ขั้น 2 สูตร: ปริมาตรต่อวินาที = พื้นที่หน้าลูกสูบ × ระยะที่ขึ้นต่อวินาที")
        self.show(t0, e1)
        self.glow(e1[0], slug, Q_C)
        self.glow(e1[2], f["dims"][:2], AREA_C)
        self.glow(e1[4], VGroup(f["varr"], f["vlab"]), V_C)
        self.say("ขั้น 3 แทนค่า: แปลง in → m ก่อน (1 in = 0.0254 m) แล้วหาพื้นที่วงกลม πD²/4")
        r2 = prow(M(r"D_{bore}=3(0.0254)=0.0762\ \text{m}", 32, AREA_C), 2.3)
        r3 = prow(M(r"A_{bore}=\frac{\pi(0.0762)^2}{4}=4.560\times10^{-3}\ \text{m}^2", 32, AREA_C), 3.4)
        r4 = prow(M(r"Q=(4.560\times10^{-3})(0.10)=4.560\times10^{-4}\ \text{m}^3/\text{s}", 32), 4.5)
        r5 = prow(boxed(M(r"Q=27.36\ \text{L/min}=0.456\ \text{L/s}", 36, Q_C)), 5.6)
        self.show(r2)
        self.show(r3)
        self.wait(1.0)
        self.show(r4)
        self.wait(1.0)
        self.say("คูณ 1000 (m³ → L) และคูณ 60 (วินาที → นาที)  ได้ 27.36 L/min")
        self.show(r5)
        self.glow(r5, slug, Q_C)
        r6 = prow(T("ขั้น 4 ตรวจ: ทางอังกฤษ 7.069 in² × 3.937 in/s → 7.23 gpm ตรงกัน ✓", 20), 6.6)
        self.show(r6)
        self.wait(2.0)
        self.clear_panel()

        # ---------------- annulus flow (used in item 2)
        self.say("ด้านบนลูกสูบมีก้านกินที่ไป → น้ำมันฟ้าอยู่ในพื้นที่ 'วงแหวน' เท่านั้น")
        a0 = prow(T("ต่อข้อ 2: น้ำมันที่ออกจากด้านก้าน", 26, OK), 0)
        a1 = prow(MP("A_{ann}", "=", "A_{bore}", "-", "A_{rod}", size=42,
                     colors={0: RET_C, 2: AREA_C, 4: AREA_C}), 1.1)
        self.show(a0, a1)
        hl = ann_box(f)
        self.glow(a1[0], hl, RET_C)
        self.remove(hl)
        self.glow(a1[4], f["rod"], AREA_C)
        a2 = prow(M(r"A_{ann}=4.560-1.140=3.420\times10^{-3}\ \text{m}^2", 32, RET_C), 2.3)
        a3 = prow(T("ทริก: ก้านโตครึ่งหนึ่ง → พื้นที่ก้าน = 1/4 → A_ann = 0.75 A_bore", 20), 3.3)
        a4 = prow(boxed(M(r"Q_{RE}=A_{ann}\,v=0.342\ \text{L/s}=20.52\ \text{L/min}", 34, RET_C)), 4.4)
        self.show(a2)
        self.show(a3)
        self.wait(1.0)
        self.show(a4)
        self.glow(a4, f["a_ret"], RET_C)
        self.wait(1.5)
        self.clear_panel()
        self.play(FadeOut(slug), FadeOut(slab), FadeOut(f["dims"]))

        # ---------------- reading figure 2
        self.say("ความดันที่เสียในวาล์ว อ่านจากรูป 2 ของโจทย์ (กราฟ Δp กับ Q)")
        img = ImageMobject(os.path.join(HERE, "fx_graph.png"))
        img.width = 5.9
        img.move_to(P2(PX + 3.05, -0.35))
        hpx, wpx = img.pixel_array.shape[:2]

        def ipt(px, py):
            return img.get_corner(UL) + RIGHT * px / wpx * img.width + DOWN * py / hpx * img.height
        self.play(FadeIn(img))
        self.rows.add(img)
        self.wait(1.0)
        warn1 = prow(T("ข้อสมมติ (บอกตรงๆ): แกน Q ในโจทย์เขียน l/min (0–2.5)", 20, WARN), 0, y0=2.25)
        warn2 = prow(T("แต่ Q จริง 27.4 L/min เลยกราฟไปมาก → อ่านแกนเป็น L/s", 20, WARN), 0,
                     y0=-2.95)
        self.say("ปัญหา: แกนกราฟเขียน l/min แต่ 27.36 L/min อยู่นอกกราฟ อ่านตามป้ายไม่ได้")
        self.show(warn1, warn2)
        self.wait(2.5)
        self.say("จึงอ่านแกนเป็น L/s: 0.456 และ 0.342 L/s อยู่ในช่วงพอดี (ถ้าอาจารย์บอกหน่วยอื่น ใช้วิธีเดิมแทนค่าใหม่)")
        ring_a = Circle(radius=0.16, color=RED, stroke_width=5).move_to(ipt(176, 783))
        ring_b = Circle(radius=0.16, color=BLUE, stroke_width=5).move_to(ipt(215, 734))
        self.play(Create(ring_a))
        self.say("เส้น A (B→T) ที่ Q_RE = 0.342 → Δp = 1.65 bar   (น้ำมันด้านก้านไหลผ่านวาล์ว B→T)")
        self.glow(ring_a, f["vret"], RED)
        self.play(Create(ring_b))
        self.say("เส้น B (P→A) ที่ Q = 0.456 → Δp = 5.67 bar   (น้ำมันทั้งหมดของปั๊มผ่าน P→A)")
        self.glow(ring_b, f["vsup"], BLUE)
        self.wait(1.0)
        self.play(FadeOut(ring_a), FadeOut(ring_b))
        self.clear_panel()

        # ---------------- item 2: P_RE
        self.say("ข้อ 2 · ขั้น 1: น้ำมันด้าน RE ต้องผ่านวาล์ว B→T และท่อกลับ 20 m ไปถัง (0 bar) → ความดันต้นทาง = ผลรวมที่เสีย")
        self.play(FadeIn(L["rp"]))
        b0 = prow(T("ข้อ 2  หา P_RE (ความดันด้านก้าน)", 26, OK), 0)
        b1 = prow(MP("P_{RE}", "=", r"\Delta p_{B\to T}", "+", r"SG\,\rho_w\,g\,h_L", size=40,
                     colors={0: RET_C, 2: VAL_C, 4: PIPE_C}), 1.1)
        self.say("ขั้น 2 สูตร: ρgh = ความดันของน้ำมันสูง h · หัวสูญเสีย h_L = 20 m ของน้ำมัน (SG = 0.9)")
        self.show(b0, b1)
        hl = ann_box(f)
        self.glow(b1[0], hl, RET_C)
        self.remove(hl)
        self.glow(b1[2], VGroup(f["vret"], L["bt"]), VAL_C)
        self.glow(b1[4], VGroup(f["ret_pipe"], L["rp"]), PIPE_C)
        self.say("ขั้น 3 แทนค่า")
        b2 = prow(M(r"\Delta p_{B\to T}=1.65\ \text{bar}\ \ (\text{curve A})", 32, VAL_C), 2.3)
        b3 = prow(M(r"SG\rho_w g h_L=0.9(1000)(9.81)(20)=176{,}580\ \text{Pa}", 32, PIPE_C), 3.4)
        b4 = prow(M(r"=1.766\ \text{bar}", 32, PIPE_C), 4.4)
        b5 = prow(boxed(M(r"P_{RE}=1.65+1.766=3.42\ \text{bar}", 36, RET_C)), 5.5)
        self.show(b2)
        self.show(b3, b4)
        self.wait(1.0)
        self.show(b5)
        pre = lab(M(r"P_{RE}=3.42\ \text{bar}", 24, RET_C), XR + 0.3, -1.0)
        self.play(FadeIn(pre))
        self.glow(b5, pre, RET_C)
        b6 = prow(T("ขั้น 4 ตรวจ: kg/m³·m/s²·m = N/m² = Pa ✓ ด้านกลับความดันต่ำ ✓", 20), 6.5)
        self.show(b6)
        self.wait(1.5)
        self.clear_panel()

        # ---------------- item 3: force balance
        self.say("ข้อ 3 · ขั้น 1: ลูกสูบขึ้นด้วยความเร็วคงที่ → แรงขึ้น = แรงลง (นิวตันข้อ 1, ไม่มีความเร่ง)")
        pc = f["piston"].get_center()
        up = Arrow(P2(CX, BOT + 0.1), P2(CX, pc[1] - 0.17), buff=0, color=Q_C, stroke_width=8,
                   tip_length=0.25)
        wtop = f["wbox"].get_left()
        wdn = Arrow(wtop + P2(-0.35, 0.35), wtop + P2(-0.35, -0.6), buff=0, color=W_C, stroke_width=7,
                    tip_length=0.22)
        ptop = f["piston"].get_top()[1]
        pdn = VGroup(*[Arrow(P2(x, ptop + 0.75), P2(x, ptop + 0.03), buff=0, color=RET_C, stroke_width=6,
                             tip_length=0.18) for x in (XL + 0.21, XR - 0.21)])
        c0 = prow(T("ข้อ 3  หา P_HE (ความดันด้านหัว)", 26, OK), 0)
        c1 = prow(MP("P_{HE}A_{bore}", "=", "W", "+", "P_{RE}A_{ann}", size=42,
                     colors={0: Q_C, 2: W_C, 4: RET_C}), 1.1)
        self.say("ขั้น 2 สูตร: แรงขึ้น = น้ำมัน HE ดันใต้ลูกสูบ · แรงลง = น้ำหนัก + น้ำมัน RE ดันบนวงแหวน")
        self.show(c0, c1)
        self.play(GrowArrow(up))
        self.glow(c1[0], up, Q_C)
        self.play(GrowArrow(wdn))
        self.glow(c1[2], VGroup(wdn, f["wbox"]), W_C)
        self.play(*[GrowArrow(a) for a in pdn])
        self.glow(c1[4], pdn, RET_C)
        self.say("ขั้น 3 แทนค่า: 3 ตัน = 3000 kg ต้องคูณ g ก่อนถึงเป็นแรง (N)")
        c2 = prow(M(r"W=mg=3000(9.81)=29{,}430\ \text{N}", 32, W_C), 2.3)
        c3 = prow(M(r"P_{RE}A_{ann}=341{,}580(3.420\times10^{-3})=1168\ \text{N}", 32, RET_C), 3.3)
        c4 = prow(M(r"P_{HE}=\frac{29{,}430+1168}{4.560\times10^{-3}}", 32, Q_C), 4.45)
        c5 = prow(boxed(M(r"P_{HE}=6.710\times10^{6}\ \text{Pa}=67.1\ \text{bar}", 36, Q_C)), 5.65)
        self.show(c2)
        self.show(c3)
        self.wait(1.0)
        self.show(c4)
        self.show(c5)
        phe = lab(M(r"P_{HE}=67.1\ \text{bar}", 24, Q_C), XR + 0.3, -2.25)
        self.play(FadeIn(phe))
        self.glow(c5, phe, Q_C)
        c6 = prow(T("ขั้น 4 ตรวจ: ถ้าไม่มีแรงด้านก้าน W/A = 64.5 bar → ของเรา 67.1 สูงกว่านิดเดียว ✓", 20), 6.65)
        self.show(c6)
        self.wait(1.5)
        self.clear_panel()
        self.play(FadeOut(up), FadeOut(wdn), FadeOut(pdn))

        # ---------------- item 4: P_pump
        self.say("ข้อ 4 · ขั้น 1: ปั๊มต้องดันให้น้ำมันถึง HE แล้วยังเหลือ P_HE ระหว่างทางเสียที่วาล์ว P→A + ท่อส่ง 15 m")
        self.play(FadeIn(L["sp"]))
        ppl = M(r"P_{pump}", 24, Q_C).move_to(PUMP + P2(0, -0.5))
        self.play(FadeIn(ppl))
        d0 = prow(T("ข้อ 4  หา P_pump (ความดันทางออกปั๊ม)", 26, OK), 0)
        d1 = prow(MP("P_{pump}", "=", "P_{HE}", "+", r"\Delta p_{P\to A}", "+", r"SG\rho_w g h_L", size=40,
                     colors={0: Q_C, 2: Q_C, 4: VAL_C, 6: PIPE_C}), 1.1)
        self.say("ขั้น 2 สูตร: ความดันที่ปั๊ม = ความดันที่ต้องเหลือ + ทุกอย่างที่เสียระหว่างทาง")
        self.show(d0, d1)
        self.glow(d1[0], VGroup(f["pump"], ppl), Q_C)
        self.glow(d1[2], phe, Q_C)
        self.glow(d1[4], VGroup(f["vsup"], L["pa"]), VAL_C)
        self.glow(d1[6], VGroup(f["sup_pipe"], L["sp"]), PIPE_C)
        self.say("ขั้น 3 แทนค่า (ข้อสมมติ: ข้อ 4 โจทย์เขียน 'ท่อกลับ 15 m' ซ้ำ → ตีความเป็นท่อส่ง)")
        d2 = prow(M(r"\Delta p_{P\to A}=5.67\ \text{bar}\ \ (\text{curve B})", 32, VAL_C), 2.3)
        d3 = prow(M(r"SG\rho_w g h_L=0.9(1000)(9.81)(15)=1.324\ \text{bar}", 32, PIPE_C), 3.35)
        d4 = prow(boxed(M(r"P_{pump}=67.10+5.67+1.32=74.1\ \text{bar}", 36, Q_C)), 4.5)
        self.show(d2)
        self.show(d3)
        self.wait(1.0)
        self.show(d4)
        self.glow(d4, VGroup(f["pump"], ppl), Q_C)
        d5 = prow(T("ขั้น 4 ตรวจ: ปั๊ม 74.1 > HE 67.1 > RE 3.42 > ถัง 0 ✓", 21), 5.6)
        d6 = prow(T("น้ำมันไหลจากความดันสูงไปต่ำเสมอ", 21, GRAYTXT), 6.4)
        self.show(d5, d6)
        self.wait(2.0)
        self.clear_panel()

        self.say("สรุปข้อ 1–4 (ค่าจากกราฟอ่านตามข้อสมมติ L/s)")
        s = [prow(M(r"1)\ Q=27.36\ \text{L/min}", 36, Q_C), 0),
             prow(M(r"2)\ P_{RE}=3.42\ \text{bar}", 36, RET_C), 1.3),
             prow(M(r"3)\ P_{HE}=67.1\ \text{bar}", 36, Q_C), 2.3),
             prow(M(r"4)\ P_{pump}=74.1\ \text{bar}", 36, Q_C), 3.3)]
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in s], lag_ratio=0.3), run_time=2.0)
        self.rows.add(*s)
        self.wait(3.0)


# =====================================================================
# FX02 -- pump + motor + energy chain
# =====================================================================
MOT = P2(-5.6, 1.3)
PMP = P2(-3.0, 1.3)


class FX02_TakeHomePumpPower(ExamScene):
    def construct(self):
        self.header("Take-home 1 ข้อ 5–9: ปั๊ม แรงบิด กำลัง ประสิทธิภาพ", "take-home 1 · ข้อ 5–9")
        motor = VGroup(RoundedRectangle(width=1.5, height=1.0, corner_radius=0.12, color=EL_C, stroke_width=3,
                                        fill_color="#424242", fill_opacity=1).move_to(MOT),
                       T("มอเตอร์", 20).move_to(MOT))
        plug = Line(P2(-6.95, 1.3), MOT + P2(-0.75, 0), color=EL_C, stroke_width=4)
        shaft = Line(MOT + P2(0.75, 0), PMP + P2(-0.6, 0), color=SHAFT_C, stroke_width=10)
        rot = Arc(radius=0.3, start_angle=-60 * DEGREES, angle=300 * DEGREES, arc_center=P2(-4.2, 1.3),
                  color=N_C, stroke_width=3)
        rot.add_tip(tip_length=0.12, tip_width=0.12)
        pump = VGroup(Circle(radius=0.6, color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(PMP),
                      Triangle(color=WHITE, fill_opacity=1).scale(0.18).rotate(PI).move_to(PMP + P2(0, -0.28)))
        pipe = Line(PMP + P2(0, -0.6), P2(-3.0, -1.8), color=Q_C, stroke_width=7)
        a_pipe = Arrow(P2(-3.0, -0.6), P2(-3.0, -1.2), buff=0, color=Q_C, stroke_width=5, tip_length=0.18)
        leak = CurvedArrow(P2(-3.12, -0.2), P2(-3.55, 0.95), angle=-1.6, color=WARN, stroke_width=3,
                           tip_length=0.14)
        cyl = VGroup(Rectangle(width=2.0, height=0.9, color=WHITE, stroke_width=3).move_to(P2(-3.0, -2.25)),
                     T("กระบอกสูบ", 20).move_to(P2(-3.0, -2.25)))
        lb = dict(
        mot_eta=M(r"\eta_{motor}=0.85", 24, EL_C).move_to(MOT + P2(0, -0.8)),
            N=M(r"N=1455\ \text{rpm}", 24, N_C).move_to(P2(-4.2, 1.95)),
            TA=M(r"T_A", 26, TQ_C).move_to(P2(-4.2, 0.75)),
            pump=lab(T("ปั๊ม", 20), -2.2, 1.65),
            ev=lab(M(r"\eta_v=0.87", 24), -2.2, 1.15),
            em=lab(M(r"\eta_m=0.89", 24), -2.2, 0.65),
            QA=lab(M(r"Q_A=27.36\ \text{L/min}", 24, Q_C), -2.75, -0.35),
            P=lab(M(r"P=74.1\ \text{bar}", 24, Q_C), -2.75, -0.85),
            leak=T("รั่วกลับ 13%", 19, WARN).move_to(P2(-4.75, -0.25)),
            W=lab(M(r"W=29{,}430\ \text{N}", 24, W_C), -1.85, -2.0),
            v=lab(M(r"v=0.10\ \text{m/s}", 24, V_C), -1.85, -2.5),
        )
        self.say("ต่อจากข้อ 1–4: มอเตอร์ไฟฟ้าหมุนเพลา → ปั๊มดันน้ำมัน 74.1 bar, 27.36 L/min → กระบอกสูบยกของ")
        self.play(FadeIn(motor), Create(plug), Create(shaft), FadeIn(pump), run_time=1.4)
        self.play(Create(rot), FadeIn(lb["N"]), FadeIn(lb["mot_eta"]), FadeIn(lb["pump"]))
        self.play(Create(pipe), GrowArrow(a_pipe), FadeIn(cyl), FadeIn(lb["QA"]), FadeIn(lb["P"]))
        self.play(FadeIn(lb["W"]), FadeIn(lb["v"]))
        self.wait(1.0)
        self.say("ปั๊มจริงไม่สมบูรณ์ 2 อย่าง: η_v = 0.87 (น้ำมันรั่วกลับในปั๊ม) · η_m = 0.89 (เสียดทาน ต้องบิดเพลาแรงขึ้น)")
        self.play(FadeIn(lb["ev"]), Create(leak), FadeIn(lb["leak"]))
        self.play(FadeIn(lb["em"]), FadeIn(lb["TA"]))
        self.wait(1.5)

        # ---------------- item 5
        self.say("ข้อ 5 · ขั้น 1: ทฤษฎีปั๊มดัน V_D ต่อรอบ แต่รั่วกลับ → ส่งจริงได้แค่ 87% ของทฤษฎี และต้องส่งจริง 27.36 L/min")
        t0 = prow(T("ข้อ 5  ความจุปั๊ม V_D (ต่อรอบ)", 26, OK), 0)
        e1 = prow(MP(r"\eta_v", "=", r"\frac{Q_A}{Q_T}", r",\qquad", "Q_T", "=", "V_D", "N", size=36,
                     colors={0: WHITE, 2: Q_C, 4: GRAYTXT, 7: N_C}), 1.15)
        self.say("ขั้น 2 สูตร (ปั๊ม): η_v = จริง/ทฤษฎี · ทฤษฎี = ความจุต่อรอบ × รอบต่อนาที")
        self.show(t0, e1)
        self.glow(e1[0], VGroup(leak, lb["leak"], lb["ev"]), WARN)
        self.glow(e1[2], VGroup(pipe, lb["QA"]), Q_C)
        self.glow(e1[7], VGroup(rot, lb["N"]), N_C)
        e2 = prow(MP("V_D", "=", r"\frac{Q_A}{\eta_v N}", size=36), 2.45)
        self.show(e2)
        self.say("ขั้น 3 แทนค่า")
        e3 = prow(M(r"Q_T=\frac{27.36}{0.87}=31.45\ \text{L/min}", 32), 3.7)
        e4 = prow(M(r"V_D=\frac{31.45\ \text{L/min}}{1455\ \text{rev/min}}=0.02162\ \text{L/rev}", 32), 4.95)
        e5 = prow(boxed(M(r"V_D=21.6\ \text{cm}^3/\text{rev}", 38, OK)), 6.1)
        self.show(e3)
        self.show(e4)
        self.show(e5)
        self.glow(e5, pump, OK)
        self.say("ขั้น 4 ตรวจ: (L/min)/(rev/min) = L/rev ✓ · ปั๊มเฟือง ~20 cc ต่อรอบ เป็นขนาดทั่วไป ✓")
        self.wait(1.0)
        self.clear_panel()

        # ---------------- item 6
        self.say("ข้อ 6 · ขั้น 1: ถ้าไม่มีเสียดทาน ต้องการแรงบิดทฤษฎี T_T แต่จริงมีเสียดทาน → มอเตอร์ต้องบิดแรงกว่า")
        f0 = prow(T("ข้อ 6  แรงบิดจริงที่เพลา T_A", 26, OK), 0)
        f1 = prow(MP("T_T", "=", r"\frac{P\,V_D}{2\pi}", r",\qquad", "T_A", "=", r"\frac{T_T}{\eta_m}", size=40,
                     colors={0: TQ_C, 4: TQ_C}), 1.15)
        f2 = prow(T("ที่มา: งานต่อ 1 รอบ  T·2π (เพลา) = P·V_D (น้ำมัน)", 20, GRAYTXT), 2.3)
        self.say("ขั้น 2 สูตร: P = ความดันที่ปั๊มเพิ่ม = 74.09 bar (ทางดูด 0 bar)")
        self.show(f0, f1, f2)
        self.glow(f1[2], VGroup(lb["P"], pump), Q_C)
        self.glow(f1[4], VGroup(lb["TA"], shaft), TQ_C)
        self.glow(f1[6], lb["em"], WHITE)
        self.say("ขั้น 3 แทนค่า: แปลงเป็น SI ก่อน (Pa และ m³)")
        f3 = prow(M(r"T_T=\frac{(7.409\times10^6)(2.162\times10^{-5})}{2\pi}=25.49" + NM, 32), 3.5)
        f4 = prow(boxed(M(r"T_A=\frac{25.49}{0.89}=28.6" + NM, 38, TQ_C)), 4.85)
        self.show(f3)
        self.show(f4)
        self.glow(f4, VGroup(lb["TA"], shaft), TQ_C)
        f5 = prow(T("ขั้น 4 ตรวจ: T_A > T_T ✓ · หน่วย Pa·m³ = N·m ✓", 21), 6.0)
        self.show(f5)
        self.wait(1.5)
        self.clear_panel()

        # ---------------- item 7
        self.say("ข้อ 7 · ขั้น 1: กำลังที่เพลา = แรงบิด × ความเร็วเชิงมุม · มอเตอร์ไฟฟ้า η = 0.85 → กินไฟมากกว่ากำลังเพลา")
        g0 = prow(T("ข้อ 7  กำลังไฟฟ้าเข้ามอเตอร์ (kW)", 26, OK), 0)
        g1 = prow(M(r"\omega=\frac{2\pi N}{60}=\frac{2\pi(1455)}{60}=152.4\ \text{rad/s}", 34, N_C), 1.15)
        g2 = prow(MP("P_{shaft}", "=", "T_A", r"\,\omega", "=", r"28.64(152.4)=4364\ \text{W}", size=34,
                     colors={2: TQ_C, 3: N_C}), 2.35)
        g3 = prow(MP("P_{el}", "=", r"\frac{P_{shaft}}{\eta_{motor}}", "=", r"\frac{4364}{0.85}", size=36,
                     colors={0: EL_C}), 3.55)
        g4 = prow(boxed(M(r"P_{el}=5134\ \text{W}=5.13\ \text{kW}", 38, EL_C)), 4.8)
        self.show(g0, g1)
        self.glow(g1, VGroup(rot, lb["N"]), N_C)
        self.show(g2)
        self.glow(g2[2], lb["TA"], TQ_C)
        self.glow(g2[0], shaft, SHAFT_C)
        self.show(g3)
        self.glow(g3[2], lb["mot_eta"], EL_C)
        pel = M(r"P_{el}", 26, EL_C).move_to(P2(-6.6, 2.1))
        self.play(FadeIn(pel))
        self.show(g4)
        self.glow(g4, VGroup(plug, pel), EL_C)
        g5 = prow(T("ขั้น 4 ตรวจวิธีที่ 2: P·Q_A = 3379 W ÷ (0.87×0.89) = 4364 W ✓", 20), 5.9)
        self.show(g5)
        self.wait(1.5)
        self.clear_panel()

        # ---------------- items 8-9
        self.say("ข้อ 8–9 · ขั้น 1: ประสิทธิภาพ = กำลังที่ได้ (ยกของ = W·v) ÷ กำลังที่ใส่")
        h0 = prow(T("ข้อ 8  ระบบไฮดรอลิก (ไม่รวมมอเตอร์ไฟฟ้า)", 24, OK), 0)
        h1 = prow(M(r"W v=29{,}430(0.10)=2943\ \text{W}", 34, W_C), 1.0)
        h2 = prow(MP(r"\eta_{hyd}", "=", r"\frac{W v}{P_{shaft}}", "=", r"\frac{2943}{4364}", "=", r"67.4\%",
                     size=38, colors={6: OK}), 2.2)
        self.show(h0, h1)
        self.glow(h1, VGroup(cyl, lb["W"], lb["v"]), W_C)
        self.show(h2)
        self.glow(h2[2], VGroup(shaft, cyl), WHITE)
        self.play(Create(SurroundingRectangle(h2[6], color=OK, buff=0.08)))
        h3 = prow(T("ข้อ 9  ทั้งระบบ (รวมมอเตอร์ไฟฟ้า)", 24, OK), 3.35)
        h4 = prow(MP(r"\eta_{total}", "=", r"\frac{W v}{P_{el}}", "=", r"\frac{2943}{5134}", "=", r"57.3\%",
                     size=38, colors={6: OK}), 4.5)
        self.show(h3, h4)
        self.glow(h4[2], VGroup(plug, pel, cyl), WHITE)
        box9 = SurroundingRectangle(h4[6], color=OK, buff=0.08)
        self.play(Create(box9))
        h5 = prow(T("ขั้น 4 ตรวจ: 0.774 × 0.871 = 0.674 ✓   0.674 × 0.85 = 0.573 ✓", 20), 5.6)
        self.show(h5)
        self.wait(1.5)
        fig = VGroup(motor, plug, shaft, rot, pump, pipe, a_pipe, leak, cyl, pel, *lb.values())
        self.play(FadeOut(fig), run_time=0.6)
        self.clear_panel()

        # ---------------- energy chain bars
        self.say("สายพลังงาน: ไฟ 100 ส่วน ได้งานยกของจริงแค่ 57 ส่วน ที่เหลือกลายเป็นความร้อน")
        vals = [(5134, "ไฟฟ้าเข้า P_el", EL_C, None), (4364, "เพลา P_shaft = T_A ω", TQ_C, "มอเตอร์ 85%"),
                (3379, "น้ำมันออกปั๊ม P·Q_A", Q_C, "ปั๊ม 77.4%"), (2943, "ยกของ W·v", W_C, "วาล์ว+ท่อ 87.1%")]
        x0, wmax = -6.2, 7.0
        bars = VGroup()
        for i, (v, name, c, eff) in enumerate(vals):
            y = 1.7 - i * 1.25
            bar = Rectangle(width=wmax * v / 5134, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
            place_left(bar, x0, y)
            txt = lab(T(f"{name} = {v:,} W", 21, c), x0, y + 0.42)
            g = VGroup(bar, txt)
            if eff:
                g.add(lab(T("× " + eff, 20, GRAYTXT), x0 + wmax + 0.35, y + 0.62))
            bars.add(g)
        for g in bars:
            self.play(GrowFromEdge(g[0], LEFT), FadeIn(g[1:]), run_time=1.0)
            self.wait(0.6)
        fin = VGroup(M(r"\eta_{hyd}=67.4\%", 38, OK), M(r"\eta_{total}=57.3\%", 38, OK)).arrange(RIGHT, buff=1.2)
        fin.move_to(P2(-1.0, -3.25))
        self.play(FadeIn(fin))
        self.wait(3.0)


# =====================================================================
# FX03 -- hydraulic motor efficiency
# =====================================================================
HM = P2(-4.4, 0.0)


def motor_figure():
    body = VGroup(Circle(radius=0.85, color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(HM),
                  Triangle(color=Q_C, fill_opacity=1).scale(0.2).rotate(PI).move_to(HM + P2(0, 0.5)))
    inl = Line(HM + P2(0, 2.0), HM + P2(0, 0.85), color=Q_C, stroke_width=7)
    a_in = Arrow(HM + P2(0, 1.95), HM + P2(0, 1.35), buff=0, color=Q_C, stroke_width=5, tip_length=0.18)
    out = Line(HM + P2(0, -0.85), HM + P2(0, -2.0), color=RET_C, stroke_width=7)
    a_out = Arrow(HM + P2(0, -1.3), HM + P2(0, -1.9), buff=0, color=RET_C, stroke_width=5, tip_length=0.18)
    shaft = Line(HM + P2(0.85, 0), HM + P2(3.0, 0), color=SHAFT_C, stroke_width=10)
    rot = Arc(radius=0.3, start_angle=-60 * DEGREES, angle=300 * DEGREES, arc_center=HM + P2(2.0, 0),
              color=N_C, stroke_width=3)
    rot.add_tip(tip_length=0.12, tip_width=0.12)
    vd = M("V_D", 24).move_to(HM + P2(0, -0.2))
    lb = dict(
        inl=lab(M(r"p,\ Q_A", 28, Q_C), HM[0] + 0.3, HM[1] + 1.65),
        out=lab(T("ไปถัง", 20, RET_C), HM[0] + 0.3, HM[1] - 1.6),
        name=lab(T("มอเตอร์ไฮดรอลิก", 20), HM[0] - 2.45, HM[1] + 1.15),
        sh=M(r"T_A,\ N", 28, TQ_C).move_to(HM + P2(2.0, 0.65)),
    )
    return dict(body=body, inl=inl, a_in=a_in, out=out, a_out=a_out, shaft=shaft, rot=rot, vd=vd, lb=lb)


class FX03_MotorEfficiency(ExamScene):
    def given(self, *lines):
        g = VGroup(*[T(s, 20, GRAYTXT) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        return place_left(g, -6.9, -2.75)

    def construct(self):
        self.header("มอเตอร์ไฮดรอลิก: η_v  η_m  η_o  กำลัง แรงบิด", "การบ้าน 7-34M · 7-36M · 7-37E")
        f = motor_figure()
        lb = f["lb"]
        self.say("มอเตอร์ไฮดรอลิก = ปั๊มกลับด้าน: น้ำมันความดันสูงไหลเข้า (p, Q) → เพลาหมุนออก (T, N)")
        self.play(FadeIn(f["body"]), Create(f["inl"]), Create(f["out"]), Create(f["shaft"]), run_time=1.3)
        self.play(GrowArrow(f["a_in"]), GrowArrow(f["a_out"]), Create(f["rot"]), FadeIn(f["vd"]),
                  *[FadeIn(m) for m in lb.values()])
        self.wait(1.0)

        # ---------------- pump vs motor table
        t0 = prow(T("สูตร η กลับเศษ-ส่วน จากปั๊ม", 26, OK), 0)
        hdr = VGroup(T("ปั๊ม", 22), T("มอเตอร์", 22, Q_C))
        r_v = VGroup(M(r"\eta_v", 34), M(r"Q_A/Q_T", 34), M(r"Q_T/Q_A", 34, Q_C))
        r_m = VGroup(M(r"\eta_m", 34), M(r"T_T/T_A", 34), M(r"T_A/T_T", 34, Q_C))
        r_o = VGroup(M(r"\eta_o", 34), M(r"\eta_v\eta_m", 34), M(r"\eta_v\eta_m", 34, Q_C))
        cols = [PX + 0.45, PX + 2.2, PX + 4.4]
        for j, m in enumerate(hdr):
            m.move_to(P2(cols[j + 1], 1.2))
        for i, r in enumerate((r_v, r_m, r_o)):
            for j, m in enumerate(r):
                m.move_to(P2(cols[j], 0.45 - 0.8 * i))
        self.say("ตารางนี้ต้องจำ: ปั๊ม 'จริง/ทฤษฎี' กับน้ำมัน · มอเตอร์กลับกัน")
        self.show(t0, hdr, r_v, r_m, r_o, rt=1.2)
        self.say("Q_A = น้ำมันที่เข้ามอเตอร์จริง (ท่อเข้า) · T_A = แรงบิดที่เพลาได้จริง")
        self.glow(r_v[2], VGroup(f["inl"], lb["inl"]), Q_C)
        self.glow(r_m[2], VGroup(f["shaft"], lb["sh"]), TQ_C)
        rule = prow(T("จำ: ค่าจริงแย่กว่าทฤษฎีเสมอ → มอเตอร์กินน้ำมันมากกว่า (รั่ว)", 20), 0, y0=-2.2)
        rule2 = prow(T("และได้แรงบิดน้อยกว่า (เสียดทาน) → η ทุกตัว < 1", 20), 0, y0=-2.8)
        self.show(rule, rule2)
        self.wait(2.0)
        self.clear_panel()

        # ---------------- 7-34M
        g = self.given("7-34M: p = 12,000 kPa", "Q = 72 L/min, N = 800 rpm", "เสียเป็นความร้อน 3 kW")
        self.say("7-34M · ขั้น 1: น้ำมันเข้า = กำลังเข้า · เสียไป 3 kW เป็นความร้อน · ที่เหลือออกที่เพลา")
        self.play(FadeIn(g))
        heat = VGroup(*[FunctionGraph(lambda x, k=k: 0.08 * np.sin(9 * x), x_range=[0, 0.7], color=WARN,
                                      stroke_width=3).rotate(PI / 2).move_to(HM + P2(-1.15 - 0.22 * k, 0.1))
                        for k in range(3)])
        hl = T("ความร้อน 3 kW", 19, WARN).move_to(HM + P2(-1.4, -0.75))
        self.play(Create(heat), FadeIn(hl))
        a0 = prow(T("7-34M  หา T_A และ η_o", 26, OK), 0)
        a1 = prow(MP("P_{in}", "=", "p", "Q", r",\quad", "P_{out}", "=", "P_{in}", "-", "P_{loss}", size=36,
                     colors={0: Q_C, 2: Q_C, 3: Q_C, 5: TQ_C, 9: WARN}), 1.1)
        self.say("ขั้น 2 สูตร: กำลังน้ำมัน = p·Q (Pa × m³/s = W) · T = P/ω · η_o = ออก/เข้า")
        self.show(a0, a1)
        self.glow(a1[2], VGroup(f["inl"], lb["inl"]), Q_C)
        self.glow(a1[9], VGroup(heat, hl), WARN)
        self.glow(a1[5], f["shaft"], TQ_C)
        self.say("ขั้น 3 แทนค่า: 72 L/min ÷ (1000×60) = 1.2×10⁻³ m³/s")
        a2 = prow(M(r"P_{in}=(12\times10^6)(1.2\times10^{-3})=14{,}400\ \text{W}", 32, Q_C), 2.2)
        a3 = prow(M(r"P_{out}=14.4-3=11.4\ \text{kW}", 32, TQ_C), 3.2)
        a4 = prow(M(r"\omega=\frac{2\pi(800)}{60}=83.78\ \text{rad/s}", 32, N_C), 4.25)
        a5 = prow(boxed(M(r"T_A=\frac{11{,}400}{83.78}=136.1" + NM, 34, TQ_C)), 5.45)
        a6 = prow(boxed(M(r"\eta_o=\frac{11.4}{14.4}=79.2\%", 34, OK)), 6.6)
        self.show(a2)
        self.show(a3)
        self.show(a4)
        self.glow(a4, f["rot"], N_C)
        self.show(a5)
        self.glow(a5, VGroup(f["shaft"], lb["sh"]), TQ_C)
        self.show(a6)
        self.say("ขั้น 4 ตรวจ: W ÷ (rad/s) = N·m ✓ · η_o ต่ำกว่า 100% ✓")
        self.wait(1.0)
        self.clear_panel()
        self.play(FadeOut(g), FadeOut(heat), FadeOut(hl))

        # ---------------- 7-36M
        g = self.given("7-36M: V_D = 130 cm³, p = 105 bar", "N = 2000 rpm", "Q_A = 0.005 m³/s, T_A = 200 N·m")
        self.say("7-36M · ขั้น 1: รู้ทั้งค่าทฤษฎี (จาก V_D, p, N) และค่าจริง (Q_A, T_A) → เทียบกันเป็น η")
        self.play(FadeIn(g))
        b0 = prow(T("7-36M  หา η_v, η_m, η_o, kW", 26, OK), 0)
        b1 = prow(MP(r"\eta_v", "=", r"\frac{Q_T}{Q_A}", r",\quad", r"\eta_m", "=", r"\frac{T_A}{T_T}", size=38,
                     colors={2: Q_C, 6: TQ_C}), 1.15)
        self.say("ขั้น 2 สูตร (มอเตอร์): Q_T = V_D N , T_T = p V_D / 2π")
        self.show(b0, b1)
        self.glow(b1[2], VGroup(f["inl"], lb["inl"], f["vd"]), Q_C)
        self.glow(b1[6], VGroup(f["shaft"], lb["sh"]), TQ_C)
        self.say("ขั้น 3 แทนค่า: V_D = 130 cm³ = 1.30×10⁻⁴ m³ · p = 105 bar = 10.5×10⁶ Pa")
        b2 = prow(M(r"Q_T=1.30\times10^{-4}\cdot\frac{2000}{60}=4.333\times10^{-3}\ \text{m}^3/\text{s}", 32), 2.4)
        b3 = prow(boxed(M(r"(a)\ \eta_v=\frac{4.333}{5.000}=86.7\%", 32, OK)), 3.5)
        b4 = prow(M(r"T_T=\frac{(10.5\times10^6)(1.30\times10^{-4})}{2\pi}=217.2" + NM, 32), 4.65)
        b5 = prow(boxed(M(r"(b)\ \eta_m=\frac{200}{217.2}=92.1\%", 32, OK)), 5.85)
        self.show(b2)
        self.show(b3)
        self.glow(b3, f["inl"], Q_C)
        self.show(b4)
        self.show(b5)
        self.glow(b5, f["shaft"], TQ_C)
        self.wait(1.0)
        self.clear_panel()
        c0 = prow(T("7-36M (ต่อ)", 26, OK), 0)
        c1 = prow(boxed(M(r"(c)\ \eta_o=\eta_v\eta_m=0.867(0.921)=79.8\%", 32, OK)), 1.15)
        c2 = prow(M(r"\omega=\frac{2\pi(2000)}{60}=209.4\ \text{rad/s}", 32, N_C), 2.4)
        c3 = prow(boxed(M(r"(d)\ P=T_A\omega=200(209.4)=41{,}890\ \text{W}=41.9\ \text{kW}", 32, OK)), 3.6)
        c4 = prow(T("ขั้น 4 ตรวจวิธีที่ 2: p·Q_A = 52.5 kW × 0.798 = 41.9 kW ✓", 20), 4.7)
        self.show(c0, c1)
        self.show(c2)
        self.show(c3)
        self.glow(c3, VGroup(f["shaft"], f["rot"]), TQ_C)
        self.show(c4)
        self.wait(1.5)
        self.clear_panel()
        self.play(FadeOut(g))

        # ---------------- 7-37E
        g = self.given("7-37E: p = 1000 psi, Q = 75 gpm", "T = 1300 in·lb, N = 1750 rpm", "η_v = 90%")
        self.say("7-37E · ขั้น 1: หน่วยอังกฤษ → ใช้สูตรลัด hp · η_o = กำลังเพลาออก ÷ กำลังน้ำมันเข้า")
        self.play(FadeIn(g))
        d0 = prow(T("7-37E  หา η_o (หน่วยอังกฤษ)", 26, OK), 0)
        d1 = prow(MP(r"HP_{in}", "=", r"\frac{p\,Q}{1714}", r",\quad", r"HP_{out}", "=", r"\frac{T\,N}{63025}",
                     size=38, colors={2: Q_C, 6: TQ_C}), 1.15)
        self.say("ขั้น 2 สูตรลัด: p (psi)·Q (gpm)/1714 และ T (in·lb)·N (rpm)/63025 ได้หน่วย hp")
        self.show(d0, d1)
        self.glow(d1[2], VGroup(f["inl"], lb["inl"]), Q_C)
        self.glow(d1[6], VGroup(f["shaft"], lb["sh"]), TQ_C)
        self.say("ขั้น 3 แทนค่า")
        d2 = prow(M(r"HP_{in}=\frac{1000(75)}{1714}=43.76\ \text{hp}", 32, Q_C), 2.45)
        d3 = prow(M(r"HP_{out}=\frac{1300(1750)}{63025}=36.10\ \text{hp}", 32, TQ_C), 3.7)
        d4 = prow(boxed(M(r"\eta_o=\frac{36.10}{43.76}=82.5\%", 34, OK)), 4.9)
        self.show(d2)
        self.show(d3)
        self.show(d4)
        warn = prow(T("η_v = 90% ไม่ต้องใช้หา η_o (ใช้หา η_m = 0.825/0.90 = 91.7%)", 20, WARN), 5.95)
        self.show(warn)
        self.glow(warn, g[2], WARN)
        d5 = prow(T("ขั้น 4 ตรวจ (SI): 26.92 kW / 32.62 kW = 82.5% ✓ เฉลยตำรา 82.4% ✓", 20), 6.6)
        self.show(d5)
        self.wait(2.0)
        self.clear_panel()
        self.play(FadeOut(g))
        self.say("สรุป: 7-34M T = 136.1 N·m, η_o = 79.2% · 7-36M 86.7 / 92.1 / 79.8%, 41.9 kW · 7-37E η_o = 82.5%")
        self.wait(3.0)


# =====================================================================
# FX04 -- hydrostatic transmission
# =====================================================================
HP_ = P2(-5.4, 0.35)
HMM = P2(-1.6, 0.35)


class FX04_Hydrostatic(ExamScene):
    def construct(self):
        self.header("7-40M: Hydrostatic transmission (ปั๊มขับมอเตอร์)", "การบ้าน 7-40M")
        r = 0.65
        pump = VGroup(Circle(radius=r, color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(HP_),
                      Triangle(color=WHITE, fill_opacity=1).scale(0.17).move_to(HP_ + P2(0, 0.36)))
        mot = VGroup(Circle(radius=r, color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(HMM),
                     Triangle(color=Q_C, fill_opacity=1).scale(0.17).rotate(PI).move_to(HMM + P2(0, 0.38)))
        top = VMobject(color=Q_C, stroke_width=7).set_points_as_corners(
            [HP_ + P2(0, r), HP_ + P2(0, 1.35), HMM + P2(0, 1.35), HMM + P2(0, r)])
        bot = VMobject(color=RET_C, stroke_width=7).set_points_as_corners(
            [HMM + P2(0, -r), HMM + P2(0, -1.3), HP_ + P2(0, -1.3), HP_ + P2(0, -r)])
        sin = Line(P2(-6.95, HP_[1]), HP_ + P2(-r, 0), color=SHAFT_C, stroke_width=10)
        sout = Line(HMM + P2(r, 0), P2(0.3, HMM[1]), color=SHAFT_C, stroke_width=10)
        a_top = Arrow(P2(-3.8, HP_[1] + 1.35), P2(-3.1, HP_[1] + 1.35), buff=0, color=Q_C, stroke_width=5,
                      tip_length=0.18)
        a_bot = Arrow(P2(-3.1, HP_[1] - 1.3), P2(-3.8, HP_[1] - 1.3), buff=0, color=RET_C, stroke_width=5,
                      tip_length=0.18)
        lp = VGroup(T("ปั๊ม", 21), M(r"V_{D,p}=100,\ N_p=1000\ \text{rpm}", 26, N_C),
                    M(r"\eta_{v,p}=0.85,\ \eta_{m,p}=0.90", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place_left(lp, -6.9, -1.95)
        lm = VGroup(T("มอเตอร์", 21, Q_C), M(r"V_{D,m}=\ ?,\ N_m=600\ \text{rpm}", 26, N_C),
                    M(r"\eta_{v,m}=0.94,\ \eta_{m,m}=0.92", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place_left(lm, -2.75, -1.95)
        plab = M(r"p=105\ \text{bar}", 26, Q_C).move_to(P2(-3.5, HP_[1] + 1.75))
        qlab = M(r"Q_A", 28, Q_C).move_to(P2(-3.5, HP_[1] + 0.9))
        tlab = M(r"T=\ ?", 28, TQ_C).move_to(P2(-0.4, HMM[1] + 0.45))
        self.say("Hydrostatic transmission = ปั๊มกับมอเตอร์ต่อกันเป็นวงจร ใช้แทนเกียร์ (ปรับความเร็ว/แรงบิดด้วยน้ำมัน)")
        self.play(FadeIn(pump), FadeIn(mot), Create(sin), Create(sout), run_time=1.2)
        self.play(Create(top), Create(bot), GrowArrow(a_top), GrowArrow(a_bot), run_time=1.4)
        self.play(FadeIn(lp), FadeIn(lm), FadeIn(plab), FadeIn(qlab), FadeIn(tlab))
        loop = VMobject().set_points_as_corners(
            [HP_ + P2(0, r), HP_ + P2(0, 1.35), HMM + P2(0, 1.35), HMM + P2(0, r)])
        dots = VGroup(*[Dot(radius=0.07, color=Q_C) for _ in range(4)])
        self.play(LaggedStart(*[MoveAlongPath(d, loop, rate_func=linear) for d in dots], lag_ratio=0.25),
                  run_time=3.0)
        self.remove(dots)
        self.say("ขั้น 1 เข้าใจ: น้ำมันที่ปั๊ม 'ส่งได้จริง' ทั้งหมดไหลเข้ามอเตอร์ · ปั๊มรั่ว 15% · มอเตอร์รั่วอีก 6%")
        self.wait(1.0)

        t0 = prow(T("7-40M (a) หา V_D ของมอเตอร์", 26, OK), 0)
        e1 = prow(MP("Q_A", "=", "V_{D,p}", "N_p", r"\eta_{v,p}", size=40,
                     colors={0: Q_C, 3: N_C}), 1.1)
        e2 = prow(MP(r"Q_{T,m}", "=", "Q_A", r"\eta_{v,m}", "=", "V_{D,m}", "N_m", size=40,
                     colors={2: Q_C, 6: N_C}), 2.25)
        self.say("ขั้น 2 สูตร: ปั๊มส่งจริง = ทฤษฎี × η_v,p · มอเตอร์ใช้เป็น 'ทฤษฎี' ได้แค่ Q_A × η_v,m (ที่เหลือรั่ว)")
        self.show(t0, e1)
        self.glow(e1[0], VGroup(top, qlab), Q_C)
        self.glow(VGroup(e1[2], e1[3], e1[4]), VGroup(pump, lp), WHITE)
        self.show(e2)
        self.glow(VGroup(e2[5], e2[6]), VGroup(mot, lm), Q_C)
        self.say("ขั้น 3 แทนค่า (หน่วยของ V_D,m เหมือนของ V_D,p)")
        e3 = prow(M(r"Q_A=100(1000)(0.85)=85{,}000\ \text{per min}", 32, Q_C), 3.35)
        e4 = prow(boxed(M(r"V_{D,m}=\frac{85{,}000(0.94)}{600}=133.2", 36, OK)), 4.55)
        self.show(e3)
        self.show(e4)
        vdm = place_left(M(r"V_{D,m}=133.2,\ N_m=600\ \text{rpm}", 26, OK), lm[1].get_left()[0], lm[1].get_y())
        self.play(FadeOut(lm[1], run_time=0.3))
        self.play(FadeIn(vdm))
        self.glow(e4, VGroup(mot, vdm), OK)
        e5 = prow(T("ตรวจ: มอเตอร์ช้ากว่าปั๊ม (600 < 1000 rpm) → ต้องจุมากกว่า ✓", 20), 5.6)
        self.show(e5)
        self.wait(1.5)
        self.clear_panel()

        f0 = prow(T("7-40M (b) หาแรงบิดมอเตอร์", 26, OK), 0)
        f1 = prow(MP("T", "=", r"\frac{p\,V_{D,m}}{2\pi}", r"\eta_{m,m}", size=40, colors={0: TQ_C}), 1.15)
        self.say("ขั้น 2 สูตร: แรงบิดทฤษฎี p V_D / 2π แล้วคูณ η_m ของมอเตอร์ (มอเตอร์ได้น้อยกว่าทฤษฎี)")
        self.show(f0, f1)
        self.glow(f1[0], VGroup(sout, tlab), TQ_C)
        self.glow(f1[2], VGroup(plab, vdm), Q_C)
        warn = VGroup(T("ข้อสงสัย: ข้อนี้เป็นข้อ M (เมตริก) แต่ตำราพิมพ์ V_D,p = 100 in³", 20, WARN),
                      T("น่าจะพิมพ์ผิดจาก cm³ → คิดให้ทั้ง 2 แบบ", 20, WARN)).arrange(DOWN, aligned_edge=LEFT,
                                                                             buff=0.12)
        prow(warn, 2.45)
        self.say("ข้อสงสัยเรื่องหน่วย: ตำราพิมพ์ 100 in³ ทั้งที่เป็นข้อเมตริก (ต้นฉบับหน้า 268 ก็พิมพ์ in³)")
        self.show(warn)
        self.wait(2.0)
        g1 = prow(T("แบบที่พิมพ์ (in³): 133.2 × 16.387 = 2182 cm³", 21), 3.55)
        g2 = prow(boxed(M(r"T=\frac{(10.5\times10^6)(2.182\times10^{-3})}{2\pi}(0.92)=3355" + NM, 30, TQ_C)), 4.6)
        g3 = prow(T("ถ้าตั้งใจ cm³: V_D,m = 133.2 cm³ = 1.332×10⁻⁴ m³", 21), 5.65)
        g4 = prow(boxed(M(r"T=204.7" + NM, 32, TQ_C)), 6.5)
        self.say("ขั้น 3 แทนค่า: แปลง V_D เป็น m³ ก่อนเสมอ")
        self.show(g1)
        self.show(g2)
        self.wait(1.0)
        self.show(g3)
        self.show(g4)
        self.glow(VGroup(g2, g4), VGroup(sout, tlab), TQ_C)
        self.say("ในห้องสอบ: เขียนกำกับให้ชัดว่าใช้หน่วยไหน · η_m ของปั๊ม (0.90) ไม่ต้องใช้ในข้อนี้")
        self.wait(1.5)
        self.clear_panel()
        h0 = prow(T("ขั้น 4 ตรวจวิธี: ข้อพี่น้อง 7-39E (V_D = 6 in³, 1500 psi)", 22, OK), 0)
        h1 = prow(M(r"V_{D,m}=\frac{6(1000)(0.85)(0.94)}{600}=7.99\ \text{in}^3", 32), 1.15)
        h2 = prow(M(r"T=\frac{1500(7.99)(0.92)}{2\pi}=1755\ \text{in}\cdot\text{lb}", 32), 2.4)
        h3 = prow(T("เฉลยตำรา 8.01 in³ และ 1756 in·lb → วิธีถูก ✓", 22, OK), 3.5)
        self.say("ตรวจวิธีกับข้อพี่น้องที่มีเฉลยท้ายเล่ม: ใช้วิธีเดียวกันได้ตรงกัน")
        self.show(h0, h1)
        self.show(h2)
        self.show(h3)
        self.wait(2.0)
        self.say("สรุป 7-40M: V_D,m = 133.2 (หน่วยเดียวกับปั๊ม) · T = 3355 N·m (in³) หรือ 204.7 N·m (cm³)")
        self.wait(3.0)
