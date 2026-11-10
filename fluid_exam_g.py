"""Fluid Power Control exam clips, batch G (2026-11-10, exam 11 Nov).

Lesson note: W09 บทเรียน — Pneumatic 02 (Pneumatic System Components & Sizing).md
FXG1_CompressorSystem  p3-11, 17-26  system layout, compressor types, stages, cut-in/out, FRL
FXG2_FreeAir           p12, p41      Q1 = Q2 (P2/P1)(T1/T2): 30 cfm -> 275 cfm free air ;
                                     cylinder 44.5 x 152 mm, 30 /min -> 0.00709 -> 0.0539 std m3/min
FXG3_HPReceiver        p13-15        100 scfm @100 psig, eta 75% -> 18.0 / 24.0 HP ;
                                     receiver 20 scfm, 6 min, 100->80 psi -> 660 gal / 495 gal
FXG4_ValvePipe         p38, 42-45    Cv: 50 scfm, dP 12 psi -> 1.46 ; pipe drop formula, ring vs branch

All numbers rechecked with python. Two note values were wrong and are corrected on screen:
p38 Cv = 50/34.29 = 1.46 (note 1.38) ; p41 Q2 = 0.00709 (note 0.00728) -> Q1 = 0.0539 (note 0.0555).
Layout follows fluid_exam_d.py: title + step tag + page_ref top row, caption_top under it,
figure on the left stage, equations in the right panel.
"""
from mlib import *
import numpy as np

AIR = "#42A5F5"    # free / atmospheric air
HIGH = WARN        # compressed air
YEL = "#FFD54F"
DARK = "#37474F"
PX, PMW = 4.15, 5.2


def T(s, size=24, color=WHITE):
    return Text(s, font_size=size, color=color)


def M(*parts, size=34, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def harrow(x0, x1, y, color, sw=5):
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25)


def varrow(x, y0, y1, color, sw=4):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25)


def dim(p0, p1, color=GRAYTXT):
    return DoubleArrow([p0[0], p0[1], 0], [p1[0], p1[1], 0], buff=0, color=color,
                       stroke_width=3, tip_length=0.13)


def block(top, sub, w=2.7, h=1.0, color=METAL, pos=(0, 0, 0), top_size=21, sub_size=16):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, color=color,
                         stroke_width=3, fill_color=DARK, fill_opacity=0.6)
    t1 = fit_width(T(top, top_size, WHITE), w - 0.25)
    if sub:
        t2 = fit_width(T(sub, sub_size, GRAYTXT), w - 0.25)
        g = VGroup(t1, t2).arrange(DOWN, buff=0.08)
    else:
        g = VGroup(t1)
    g.move_to(r)
    g.set_z_index(3)
    return VGroup(r, g).move_to(np.array(pos, dtype=float))


def hspring(x0, x1, y, amp=0.4, n=6, color=METAL):
    pts = [[x0, y, 0]]
    for i in range(1, 2 * n):
        xx = x0 + (x1 - x0) * i / (2 * n)
        pts.append([xx, y + (amp if i % 2 else -amp), 0])
    pts.append([x1, y, 0])
    return VMobject(color=color, stroke_width=3).set_points_as_corners(
        [np.array(p, dtype=float) for p in pts])


class ExamScene(SafeScene):
    def head(self, ttl, ref):
        self.ttl = fit_width(title(ttl, size=28), 7.0)
        self.ref = page_ref(ref, size=18)
        self.cap_m = None
        self.step_m = None
        self.play(FadeIn(self.ttl), FadeIn(self.ref))

    def step(self, n, name):
        m = T(f"ขั้น {n} · {name}", 22, OK)
        room = (-self.ttl.width / 2) - (-7.11 + 0.3) - 0.3
        fit_width(m, room)
        m.move_to([-7.11 + 0.3 + m.width / 2, TITLE_Y, 0])
        if self.step_m is not None:
            self.play(FadeOut(self.step_m, run_time=0.3))
        self.play(FadeIn(m, shift=0.2 * RIGHT), run_time=0.5)
        self.step_m = m

    def cap(self, txt, color=GRAYTXT, wait=2.4):
        m = caption_top(txt, color=color, size=25, max_w=12.8)
        if self.cap_m is not None:
            self.play(FadeOut(self.cap_m, run_time=0.3))
        self.play(FadeIn(m), run_time=0.6)
        self.cap_m = m
        if wait:
            self.wait(wait)
        return m

    def glow(self, term, fig=None, color=YEL, rt=1.3):
        sf = 1.0 if (term.width > 3.2 or isinstance(term, Text)) else 1.2
        an = [Indicate(term, color=WHITE, scale_factor=sf),
              Circumscribe(term, color=color, buff=0.04, stroke_width=3, fade_out=True)]
        if fig is not None:
            an.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*an, run_time=rt)

    def rows(self, rows, y0, gap=1.0, x=PX, max_w=PMW):
        for i, r in enumerate(rows):
            fit_width(r, max_w)
            r.move_to([x, y0 - i * gap, 0])
        return VGroup(*rows)

    def relabel_m(self, old, tex, size, color):
        new = M(tex, size=size, color=color).move_to(old.get_center())
        self.play(Transform(old, new))

    def clear_stage(self):
        keep = {self.ttl, self.ref, self.step_m, self.cap_m}
        ms = [m for m in self.mobjects if m not in keep]
        for m in ms:
            m.clear_updaters()
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=0.6)


# ======================================================================
class FXG1_CompressorSystem(ExamScene):
    """p3 layout, p5-10 compressor types, p7 stages, p11 cut-in/out, p17-19 + p24-26 air treatment."""

    def construct(self):
        self.head("ระบบลมอัด: จากคอมเพรสเซอร์ถึง FRL", "W09 · หน้า 3-26")

        # ---------------- step 1: system layout (page 3)
        xs = [-5.3, -1.77, 1.77, 5.3]
        y1, y2 = 1.0, -1.55
        n1 = [("กรองลมเข้า", "Intake filter"), ("คอมเพรสเซอร์", "Compressor"),
              ("ระบายความร้อน", "Aftercooler"), ("แยกน้ำ", "Separator")]
        n2 = [("ถังพักลม", "Air receiver"), ("เครื่องทำลมแห้ง", "Air dryer"),
              ("ท่อหลักวงแหวน", "Ring main"), ("FRL → เครื่องจักร", "Service unit")]
        rx = xs[::-1]
        chain = [block(a, b, pos=[x, y1, 0]) for (a, b), x in zip(n1, xs)]
        chain += [block(a, b, pos=[x, y2, 0]) for (a, b), x in zip(n2, rx)]
        arrows = [harrow(xs[i] + 1.38, xs[i + 1] - 1.38, y1, AIR, 4) for i in range(3)]
        arrows.append(varrow(5.3, y1 - 0.53, y2 + 0.53, AIR, 4))
        arrows += [harrow(rx[i] - 1.38, rx[i + 1] + 1.38, y2, AIR, 4) for i in range(3)]

        t_hot = T("ร้อน 250-350°F", 19, WARN).move_to([xs[1], 0.15, 0])
        t_cool = T("เย็นลง 80-100°F", 19, AIR).move_to([xs[2], 0.15, 0])
        t_cond = T("ไอน้ำควบแน่น 70-85%", 18, AIR).move_to([xs[2], -0.32, 0])
        t_dry1 = T("แช่เย็น: 35-40°F", 18, AIR).move_to([rx[1], -2.35, 0])
        t_dry2 = T("สารดูดความชื้น: -40 ถึง -100°F", 18, AIR).move_to([rx[1], -2.8, 0])
        t_ring = T("ลมเข้าได้ 2 ทาง", 18, AIR).move_to([rx[2], -2.35, 0])
        t_frl = T("ติดทุกจุดใช้งาน", 18, AIR).move_to([rx[3], -2.35, 0])
        drain = varrow(5.3, -2.1, -2.6, AIR, 4)
        t_drain = T("วาล์วระบายน้ำ (drain)", 17, AIR).move_to([5.3, -2.9, 0])

        self.step(1, "ผังระบบลมอัด")
        self.cap("ลมจากรอบตัวเดินผ่านอุปกรณ์ตามลำดับนี้ (หน้า 3)", wait=1.2)
        texts = ["1) กรองฝุ่นออกก่อน แล้วลมจึงเข้าคอมเพรสเซอร์",
                 "2) คอมเพรสเซอร์อัดลม → ลมออกมาร้อนมาก 250-350°F",
                 "3) Aftercooler ทำให้ลมเย็นลง → ไอน้ำกลายเป็นหยดน้ำ 70-85%",
                 "4) Separator แยกหยดน้ำทิ้ง",
                 "5) ถังพักลม: เก็บลม รักษาความดันให้นิ่ง และดักน้ำซ้ำ",
                 "6) Dryer ทำลมให้แห้งก่อนส่งเข้าท่อหลัก (2 แบบ ดูใต้กล่อง)",
                 "7) ท่อหลักแบบวงแหวน: ลมเข้าแต่ละจุดได้ 2 ทาง แรงดันตกน้อย",
                 "8) ชุด FRL ติดก่อนเข้าเครื่องจักรทุกจุด"]
        extras = {1: [t_hot], 2: [t_cool, t_cond], 5: [t_dry1, t_dry2], 6: [t_ring], 7: [t_frl]}
        for i, b in enumerate(chain):
            an = [FadeIn(b, shift=0.15 * RIGHT)]
            if i > 0:
                an.insert(0, GrowArrow(arrows[i - 1]))
            self.play(*an, run_time=0.7)
            if i in extras:
                self.play(FadeIn(VGroup(*extras[i])), run_time=0.5)
            self.cap(texts[i], wait=2.2)
        self.play(GrowArrow(drain), FadeIn(t_drain))
        self.cap("จุดที่มีน้ำควบแน่น มีวาล์วระบายน้ำอัตโนมัติ (drain trap)", wait=2.2)
        self.play(*[ShowPassingFlash(a.copy().set_color(YEL), time_width=0.6) for a in arrows],
                  run_time=1.5)
        self.cap("จำลำดับ: กรอง → อัด → เย็น → แยกน้ำ → ถัง → แห้ง → ท่อ → FRL",
                 color=WHITE, wait=3.0)
        self.clear_stage()

        # ---------------- step 2: compressor types (page 5-10)
        self.step(2, "ชนิดคอมเพรสเซอร์")
        root = block("คอมเพรสเซอร์", "Compressor", w=3.0, h=0.9, pos=[0, 1.75, 0], color=OK)
        pd = block("แทนที่ปริมาตร", "Positive displacement", w=3.4, h=0.9,
                   pos=[-3.6, 0.5, 0], color=AIR)
        dy = block("ไดนามิก (เร่งความเร็ว)", "Dynamic", w=3.4, h=0.9,
                   pos=[3.6, 0.5, 0], color=YEL)
        rec = block("ลูกสูบชัก", "Reciprocating", w=2.6, h=0.85, pos=[-5.3, -0.85, 0], color=AIR)
        rot = block("แบบหมุน", "Rotary", w=2.6, h=0.85, pos=[-1.9, -0.85, 0], color=AIR)
        dyn = block("ใบพัดเหวี่ยง", "Centrifugal / Axial", w=3.0, h=0.85,
                    pos=[3.6, -0.85, 0], color=YEL)
        leaf_rec = VGroup(T("Piston ลูกสูบ", 19), T("Diaphragm ไดอะแฟรม", 19)).arrange(
            DOWN, buff=0.15).move_to([-5.3, -2.05, 0])
        leaf_rot = VGroup(T("Screw สกรู", 19), T("Lobe โลบ", 19), T("Vane ใบเลื่อน", 19)).arrange(
            DOWN, buff=0.15).move_to([-1.9, -2.25, 0])
        leaf_dyn = T("> 1,000 scfm โรงงานใหญ่", 19, GRAYTXT).move_to([3.6, -1.75, 0])

        def link(a, b):
            return Line(a[0].get_bottom(), b[0].get_top(), color=METAL, stroke_width=3)

        self.play(FadeIn(root))
        self.play(Create(link(root, pd)), Create(link(root, dy)), FadeIn(pd), FadeIn(dy))
        self.cap("แบ่งเป็น 2 กลุ่มตามหลักการอัดลม (หน้า 5)", wait=1.6)
        self.glow(pd[1], pd[0], AIR)
        self.cap("แทนที่ปริมาตร: ขังลมในห้องปิด แล้วบีบให้ปริมาตรเล็กลง → ความดันขึ้น")
        self.glow(dy[1], dy[0], YEL)
        self.cap("ไดนามิก: ใบพัดเร่งลมให้เร็ว แล้วเปลี่ยนความเร็วเป็นความดัน")
        self.play(Create(link(pd, rec)), FadeIn(rec), FadeIn(leaf_rec))
        self.cap("ลูกสูบ: ได้ความดันสูงมาก · ไดอะแฟรม: ลมไม่มีน้ำมัน 100% (ยา/อาหาร)")
        self.play(Create(link(pd, rot)), FadeIn(rot), FadeIn(leaf_rot))
        self.glow(leaf_rot[0])
        self.cap("สกรู: ลมไหลต่อเนื่อง เงียบ ไม่กระแทก เหมาะเดิน 24 ชม.")
        self.glow(leaf_rot[1])
        self.cap("โลบ: ลมปริมาณมาก แต่ความดันต่ำ · เวน: โรเตอร์เยื้องศูนย์ ลมเรียบ")
        self.play(Create(link(dy, dyn)), FadeIn(dyn), FadeIn(leaf_dyn))
        self.cap("Centrifugal: หมุนหลายหมื่นรอบ/นาที สำหรับโรงงานใหญ่มาก > 1,000 scfm")
        self.clear_stage()

        # ---------------- step 3: stages (page 7) + pressure switch (page 11)
        self.step(3, "ขั้นอัด + สวิตช์ความดัน")
        hdr = VGroup(T("จำนวนขั้นอัด", 20, GRAYTXT).move_to([-5.6, 1.7, 0]),
                     T("ความดันสูงสุด", 20, GRAYTXT).move_to([-3.0, 1.7, 0]))
        hline = Line([-6.6, 1.38, 0], [-1.6, 1.38, 0], color=METAL, stroke_width=2)
        data = [("1 ขั้น", "150 psi (≈10 bar)"), ("2 ขั้น", "500 psi (≈35 bar)"),
                ("3 ขั้น", "2,500 psi (≈170 bar)"), ("4 ขั้น", "5,000 psi (≈350 bar)")]
        trows = VGroup()
        for i, (a, b) in enumerate(data):
            y = 1.0 - 0.7 * i
            trows.add(VGroup(T(a, 22).move_to([-5.6, y, 0]),
                             fit_width(T(b, 22, YEL), 2.9).move_to([-3.0, y, 0])))
        t_ic = fit_width(T("อัดหลายขั้น + intercooler ระบายร้อนระหว่างขั้น", 19, AIR), 4.8)
        t_ic.move_to([-4.1, -1.9, 0])

        ax = Axes(x_range=[0, 10, 2], y_range=[70, 110, 10], x_length=5.0, y_length=3.4,
                  tips=False, axis_config={"color": METAL, "include_ticks": False})
        ax.move_to([3.9, -0.3, 0])
        ylab = T("P ในถัง (psi)", 18, GRAYTXT)
        ylab.move_to(ax.c2p(0, 110) + np.array([ylab.width / 2, 0.25, 0]))
        xlab = T("เวลา", 18, GRAYTXT).move_to(ax.c2p(10, 70) + np.array([-0.3, -0.3, 0]))
        l100 = DashedLine(ax.c2p(0, 100), ax.c2p(10, 100), color=WARN, stroke_width=2)
        l80 = DashedLine(ax.c2p(0, 80), ax.c2p(10, 80), color=AIR, stroke_width=2)
        lb100 = T("cut-out 100 psi (หยุด)", 18, WARN).move_to(ax.c2p(2.6, 105))
        lb80 = T("cut-in 80 psi (เริ่มอัด)", 18, AIR).move_to(ax.c2p(2.6, 75))
        pts = [(0, 100), (3, 80), (4.2, 100), (7.2, 80), (8.4, 100), (10, 89.3)]
        saw = VMobject(color=YEL, stroke_width=4).set_points_as_corners(
            [ax.c2p(a, b) for a, b in pts])
        stat_pos = np.array([4.9, 1.95, 0])
        st_off = T("คอมเพรสเซอร์: หยุด (OFF)", 20, AIR).move_to(stat_pos)
        st_on = T("คอมเพรสเซอร์: เดิน (ON)", 20, WARN).move_to(stat_pos)
        dot = Dot(ax.c2p(0, 100), color=WHITE, radius=0.08)

        self.play(FadeIn(hdr), Create(hline))
        self.play(LaggedStart(*[FadeIn(r, shift=0.1 * DOWN) for r in trows], lag_ratio=0.3))
        self.cap("อัดทีเดียวให้สูงมาก ลมร้อนเกินกว่าน้ำมันหล่อลื่นทน → แบ่งอัดหลายขั้น")
        self.play(FadeIn(t_ic))
        self.glow(trows[1])
        self.cap("ยิ่งต้องการความดันสูง ยิ่งต้องใช้หลายขั้น (หน้า 7)")
        self.play(Create(ax), FadeIn(ylab), FadeIn(xlab))
        self.play(Create(l100), Create(l80), FadeIn(lb100), FadeIn(lb80))
        self.cap("คอมเพรสเซอร์ไม่ได้อัดตลอด: Pressure switch สั่งเดิน/หยุดตามความดันในถัง",
                 wait=1.8)
        self.play(Create(saw), run_time=1.5)
        self.play(FadeIn(dot), FadeIn(st_off))
        cur = st_off
        for k in range(len(pts) - 1):
            rising = pts[k + 1][1] > pts[k][1]
            want = st_on if rising else st_off
            if want is not cur:
                nxt = want.copy()
                self.play(FadeOut(cur, run_time=0.25))
                self.play(FadeIn(nxt, run_time=0.25))
                cur = nxt
            self.play(dot.animate.move_to(ax.c2p(*pts[k + 1])), run_time=1.0, rate_func=linear)
        self.cap("ลดถึง 80 psi (cut-in) → เริ่มอัด · ขึ้นถึง 100 psi (cut-out) → หยุด")
        self.glow(lb80, l80, AIR)
        self.glow(lb100, l100, WARN)
        self.cap("Unloader: ระบายความดันค้างหัวสูบตอนสตาร์ท → มอเตอร์สตาร์ทตัวเปล่า ไม่โอเวอร์โหลด",
                 wait=2.8)
        self.clear_stage()

        # ---------------- step 4: FRL (page 24-26)
        self.step(4, "ทำลมให้สะอาด: FRL")
        fx = [-4.4, 0.0, 4.4]
        heads = [("F · Filter", "กรองลม", AIR), ("R · Regulator", "ปรับความดัน", YEL),
                 ("L · Lubricator", "เติมน้ำมันหล่อลื่น", OK)]
        bxs = [block(a, b, w=3.4, h=1.2, pos=[x, 0.9, 0], color=c, top_size=24, sub_size=20)
               for (a, b, c), x in zip(heads, fx)]
        dsc = [["เหวี่ยงน้ำ+ฝุ่นลงก้นถ้วย", "ไส้กรอง 5-40 ไมครอน"],
               ["ลด 100 psi → 60-80 psi", "คงที่ด้วยไดอะแฟรม + สปริง"],
               ["Venturi ดูดน้ำมันขึ้นมา", "พ่นเป็นละอองไปกับลม"]]
        descs = [VGroup(*[fit_width(T(s, 20, GRAYTXT), 3.9) for s in d]).arrange(
            DOWN, buff=0.22).move_to([x, -0.55, 0]) for d, x in zip(dsc, fx)]
        fa = [harrow(-2.65, -1.75, 0.9, AIR, 4), harrow(1.75, 2.65, 0.9, AIR, 4)]
        t_in = T("ลมจากท่อหลัก", 19, AIR).move_to([-4.4, 1.95, 0])
        t_out = T("→ เข้าเครื่องจักร", 19, AIR).move_to([4.4, 1.95, 0])
        t_order = T("ลำดับ F → R → L เสมอ", 28, YEL).move_to([0, -2.2, 0])

        self.play(FadeIn(bxs[0]), FadeIn(t_in))
        self.play(GrowArrow(fa[0]), FadeIn(bxs[1]))
        self.play(GrowArrow(fa[1]), FadeIn(bxs[2]), FadeIn(t_out))
        self.cap("ก่อนลมเข้าเครื่องจักร ต้องผ่านชุด FRL 3 ชิ้นเรียงกัน (หน้า 24-26)", wait=1.8)
        self.play(FadeIn(descs[0]))
        self.glow(bxs[0][1], bxs[0][0], AIR)
        self.cap("F กรอง: ใบพัดเหวี่ยงน้ำและฝุ่นใหญ่ลงก้นถ้วย ไส้กรองดักฝุ่นละเอียด")
        self.play(FadeIn(descs[1]))
        self.glow(bxs[1][1], bxs[1][0], YEL)
        self.cap("R ปรับความดัน: ลดจากท่อหลักให้คงที่พอดีงาน เช่น 100 → 60-80 psi")
        self.play(FadeIn(descs[2]))
        self.glow(bxs[2][1], bxs[2][0], OK)
        self.cap("L หล่อลื่น: Venturi ดูดน้ำมันเป็นละอองฝอย ไปหล่อลื่นซีลในวาล์ว/กระบอกสูบ")
        self.play(Write(t_order))
        self.cap("จำว่า F-R-L: กรองก่อน → ปรับความดัน → เติมน้ำมันสุดท้าย", color=WHITE, wait=2.8)
        self.clear_stage()

        # ---------------- step 5: quick check
        self.step(5, "ทบทวน")
        qa = [("1) ต้องการลม 500 psi ใช้ลูกสูบอย่างน้อยกี่ขั้น?", "→ 2 ขั้น (1 ขั้นได้แค่ 150 psi)"),
              ("2) โรงงานยา/อาหาร ต้องการลมไม่มีน้ำมันเลย ใช้แบบไหน?", "→ ไดอะแฟรม (oil-free 100%)"),
              ("3) ความดันถังลดลงถึง cut-in 80 psi เกิดอะไรขึ้น?",
               "→ คอมเพรสเซอร์เริ่มอัด จนถึง 100 psi จึงหยุด")]
        self.cap("ทบทวน 3 ข้อ: ลองตอบในใจก่อนดูเฉลย", wait=1.0)
        for i, (q, a) in enumerate(qa):
            y = 1.6 - 1.5 * i
            qm = fit_width(T(q, 25), 12.5).move_to([0, y, 0])
            am = fit_width(T(a, 25, OK), 12.5).move_to([0, y - 0.6, 0])
            self.play(FadeIn(qm, shift=0.1 * UP))
            self.wait(2.6)
            self.play(FadeIn(am, shift=0.1 * UP))
            self.wait(1.6)
        self.wait(1.5)


# ======================================================================
class FXG2_FreeAir(ExamScene):
    """p12: 30 cfm @125 psig 90F -> 275 cfm free air ; p41: cylinder 0.00709 -> 0.0539 std m3/min."""

    def construct(self):
        self.head("ลมอิสระ (free air) กับอัตรากินลม", "W09 · หน้า 12, 41")

        big = Square(1.8, color=AIR, fill_color=AIR, fill_opacity=0.3, stroke_width=3)
        big.move_to([-5.4, 0.5, 0])
        big_l = T("ลม 1 ก้อน", 18, AIR).move_to(big)
        comp = block("คอมเพรสเซอร์", "", w=1.7, h=1.0, pos=[-3.15, 0.5, 0], top_size=18)
        tank = RoundedRectangle(corner_radius=0.35, width=1.3, height=2.3, color=METAL,
                                stroke_width=4, fill_color=DARK, fill_opacity=0.6)
        tank.move_to([-1.0, 0.5, 0])
        small = Square(0.62, color=HIGH, fill_color=HIGH, fill_opacity=0.55,
                       stroke_width=3).move_to(tank)
        a_in = harrow(-4.45, -4.0, 0.5, AIR, 4)
        a_mid = harrow(-2.3, -1.65, 0.5, HIGH, 4)
        a_out = harrow(-0.35, 1.25, -0.3, HIGH, 5)
        q2_l = fit_width(M(r"Q_2 = 30\ \text{cfm}", size=28, color=HIGH), 1.55)
        q2_l.move_to([0.5, 0.05, 0])
        s1 = VGroup(T("สถานะ 1: อากาศรอบตัว", 19, AIR),
                    M(r"P_1 = 14.7\ \text{psia}", size=28, color=AIR),
                    M(r"T_1 = 70^\circ\text{F}", size=28, color=AIR),
                    M(r"Q_1 = \ ?", size=28, color=AIR)).arrange(DOWN, buff=0.16)
        s1.move_to([-5.4, -1.65, 0])
        s2 = VGroup(T("สถานะ 2: ในถัง", 19, HIGH),
                    M(r"P_2 = 125\ \text{psig}", size=28, color=HIGH),
                    M(r"T_2 = 90^\circ\text{F}", size=28, color=HIGH)).arrange(DOWN, buff=0.16)
        s2.move_to([-1.0, -1.5, 0])

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(FadeIn(big), FadeIn(big_l))
        self.cap("free air = ปริมาตรของลม ถ้าวัดที่สภาพอากาศรอบตัว (ยังไม่ถูกอัด)")
        self.play(GrowArrow(a_in), FadeIn(comp))
        self.play(GrowArrow(a_mid), FadeIn(tank))
        parcel = big.copy()
        self.play(FadeOut(big_l, run_time=0.3))
        self.play(Transform(parcel, small, path_arc=-1.8), run_time=2.0)
        self.add(small)
        self.remove(parcel)
        self.play(FadeIn(big_l, run_time=0.3))
        self.cap("ลมก้อนเดียวกัน (มวลเท่ากัน): ข้างนอกตัวใหญ่ · ในถังถูกอัดจนเล็ก")
        self.play(FadeIn(s1), FadeIn(s2))
        self.play(GrowArrow(a_out), FadeIn(q2_l))
        self.cap("โจทย์ (หน้า 12): ระบบใช้ลม 30 cfm จากถัง 125 psig, 90°F", color=WHITE)
        self.glow(q2_l, a_out, HIGH)
        self.glow(s2[1])
        self.cap("อากาศรอบตัว 14.7 psia, 70°F → คอมเพรสเซอร์ต้องดูดลมกี่ cfm?", color=WHITE)
        self.glow(s1[3], big, AIR)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"\frac{P_1 Q_1}{T_1}", r"=", r"\frac{P_2 Q_2}{T_2}", size=40)
        e2 = M(r"Q_1", r"=", r"Q_2", r"\left(\frac{P_2}{P_1}\right)",
               r"\left(\frac{T_1}{T_2}\right)", size=40)
        e2[0].set_color(AIR); e2[2].set_color(HIGH)
        e3 = T("P และ T ต้องเป็นค่าสัมบูรณ์!", 24, WARN)
        e4 = M(r"\text{psia} = \text{psig} + 14.7", size=32)
        e5 = M(r"^\circ\text{R} = ^\circ\text{F} + 460", size=32)
        self.rows([e1, e2, e3, e4, e5], 1.85, 1.15)
        self.play(FadeIn(e1))
        self.cap("กฎแก๊ส: ลมก้อนเดียวกันต่อ 1 นาที → P·Q/T เท่ากันทั้งสองฝั่ง")
        self.play(FadeIn(e2))
        self.cap("ย้ายข้างหา Q1 = Q2 คูณอัตราส่วนความดัน คูณอัตราส่วนอุณหภูมิ", wait=1.0)
        self.glow(e2[0], big, AIR)
        self.glow(e2[2], a_out, HIGH)
        self.glow(e2[3], VGroup(s1[1], s2[1]))
        self.glow(e2[4], VGroup(s1[2], s2[2]))
        self.play(FadeIn(e3))
        self.play(FadeIn(e4), FadeIn(e5))
        self.cap("กับดัก: ใช้ psig หรือ °F ตรงๆ = ผิดทันที ต้องแปลงก่อน", color=WARN)

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e3, e4, e5)))
        self.play(e2.animate.move_to([PX, 1.85, 0]))
        a1 = M(r"P_2 = 125 + 14.7 = 139.7\ \text{psia}", size=32, color=HIGH)
        a2 = M(r"T_1 = 70 + 460 = 530^\circ\text{R}", size=32, color=AIR)
        a3 = M(r"T_2 = 90 + 460 = 550^\circ\text{R}", size=32, color=HIGH)
        self.rows([a1, a2, a3], 0.75, 0.85)
        self.play(FadeIn(a1))
        self.glow(a1, s2[1], HIGH)
        self.relabel_m(s2[1], r"P_2 = 139.7\ \text{psia}", 28, HIGH)
        self.cap("ความดันในถังเป็น gage → บวก 14.7 ได้ 139.7 psia (P1 = 14.7 psia อยู่แล้ว)")
        self.play(FadeIn(a2), FadeIn(a3))
        self.relabel_m(s1[2], r"T_1 = 530^\circ\text{R}", 28, AIR)
        self.relabel_m(s2[2], r"T_2 = 550^\circ\text{R}", 28, HIGH)
        self.cap("°F + 460 = °R (Rankine): 530 °R กับ 550 °R")
        self.play(FadeOut(VGroup(a1, a2, a3)))
        b1 = M(r"Q_1 = 30\left(\frac{139.7}{14.7}\right)\left(\frac{530}{550}\right)", size=34)
        b2 = M(r"= 30 \times 9.503 \times 0.9636", size=34)
        b3 = M(r"Q_1 = 275\ \text{cfm free air}", size=40, color=OK)
        self.rows([b1, b2, b3], 0.65, 1.1)
        box = SurroundingRectangle(b3, color=OK, buff=0.15)
        self.play(FadeIn(b1))
        self.cap("แทน Q2 = 30 และค่าสัมบูรณ์ทั้งหมด")
        self.play(FadeIn(b2))
        self.cap("อัตราส่วนความดัน 9.503 · อัตราส่วนอุณหภูมิ 0.9636")
        self.play(Write(b3), Create(box))
        self.relabel_m(s1[3], r"Q_1 = 275\ \text{cfm}", 28, AIR)
        self.cap("คำตอบ: คอมเพรสเซอร์ต้องดูดลมอิสระ 275 cfm", color=OK)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = T("275 ÷ 30 ≈ 9.2 ใกล้อัตราส่วนความดัน 9.5 ✓", 23, OK)
        c2 = T("Q1 > Q2 เสมอ เพราะลมข้างนอกยังไม่ถูกอัด ✓", 23, OK)
        self.rows([c1, c2], -2.55, 0.65)
        self.play(FadeIn(c1, shift=0.1 * UP))
        self.cap("ลมถูกอัดราว 9.5 เท่า อุณหภูมิในถังสูงกว่านิดหน่อย → ได้ราว 9.2 เท่า")
        self.play(FadeIn(c2, shift=0.1 * UP))
        self.glow(big, None, AIR)
        self.cap("ใช้ซ้ำได้ทุกโจทย์ ‘ลมอิสระ’ หรือ ‘standard’: แปลงด้วยสูตรนี้เสมอ", wait=2.0)
        self.clear_stage()

        # ================= problem 2: cylinder air consumption (page 41)
        bx0, bx1, yc, hh = -6.3, -2.3, 0.5, 1.2
        barrel = Rectangle(width=bx1 - bx0, height=hh, color=METAL, stroke_width=4)
        barrel.move_to([(bx0 + bx1) / 2, yc, 0])
        xp = ValueTracker(-6.0)
        fill = always_redraw(lambda: Rectangle(
            width=max(xp.get_value() - 0.11 - bx0, 0.02), height=hh - 0.06, stroke_width=0,
            fill_color=HIGH, fill_opacity=0.45).move_to(
            [(bx0 + xp.get_value() - 0.11) / 2, yc, 0]))
        piston = always_redraw(lambda: Rectangle(width=0.22, height=hh - 0.06, stroke_width=0,
                                                 fill_color=METAL, fill_opacity=1).move_to(
            [xp.get_value(), yc, 0]))
        rod = always_redraw(lambda: Rectangle(width=4.4, height=0.22, stroke_width=0,
                                              fill_color=METAL, fill_opacity=1).move_to(
            [xp.get_value() + 2.2, yc, 0]))
        spring = always_redraw(lambda: hspring(xp.get_value() + 0.11, bx1, yc, 0.42, 6))
        port = varrow(-6.15, -1.0, yc - hh / 2, HIGH, 4)
        ddim = dim((-6.6, yc - hh / 2), (-6.6, yc + hh / 2), YEL)
        dlab = M(r"D", size=30, color=YEL).move_to([-6.88, yc, 0])
        ldim = dim((-6.0, 1.45), (-4.0, 1.45), YEL)
        llab = M(r"L = 152\ \text{mm}", size=28, color=YEL).move_to([-5.0, 1.85, 0])
        r1 = M(r"D = 44.5\ \text{mm},\ L = 152\ \text{mm},\ N = 30/\text{min}", size=28, color=YEL)
        r2 = T("single-acting: ลมดันออก สปริงดันกลับ", 19, GRAYTXT)
        r3 = M(r"P_2 = 687\ \text{kPa gage},\ T_2 = 27^\circ\text{C}", size=28, color=HIGH)
        r4 = M(r"\text{std: } P_1 = 101.3\ \text{kPa abs},\ T_1 = 20^\circ\text{C}", size=28,
               color=AIR)
        info = VGroup(r1, r2, r3, r4)
        for i, r in enumerate(info):
            fit_width(r, 5.6)
            r.move_to([-4.0, -1.5 - 0.55 * i, 0])

        def cycle(n=1):
            for _ in range(n):
                self.play(xp.animate.set_value(-4.0), run_time=1.0)
                self.play(xp.animate.set_value(-6.0), run_time=0.8)

        self.step(1, "โจทย์ 2 เข้าใจ")
        self.play(Create(barrel), FadeIn(piston), FadeIn(rod), FadeIn(spring), FadeIn(fill))
        self.play(GrowArrow(port))
        self.cap("โจทย์ 2 (หน้า 41): กระบอกสูบทางเดียว ใช้ลมกี่ m³/min ที่สภาพมาตรฐาน?",
                 color=WHITE, wait=1.0)
        cycle(2)
        self.play(FadeIn(ddim), FadeIn(dlab), FadeIn(ldim), FadeIn(llab))
        self.play(FadeIn(info))
        self.cap("1 รอบ: ลมอัดเต็มกระบอก 1 ช่วงชัก แล้วสปริงดันกลับ (ลมทิ้ง)")
        self.glow(r1, VGroup(ddim, ldim), YEL)
        self.cap("ลมในกระบอกเป็นลมอัด (สถานะ 2) · ต้องตอบเป็นลมมาตรฐาน (สถานะ 1)")
        self.glow(r3)
        self.glow(r4)

        self.step(2, "สูตร")
        f1 = M(r"Q_2", r"=", r"\frac{\pi}{4}D^2", r"\times L", r"\times N", size=40)
        f2 = M(r"Q_1", r"=", r"Q_2", r"\left(\frac{P_2}{P_1}\right)",
               r"\left(\frac{T_1}{T_2}\right)", size=40)
        f1[0].set_color(HIGH); f2[0].set_color(AIR); f2[2].set_color(HIGH)
        self.rows([f1, f2], 1.85, 1.2)
        self.play(FadeIn(f1))
        self.cap("ลมอัดที่ใช้ต่อนาที = พื้นที่ลูกสูบ × ช่วงชัก × จำนวนรอบต่อนาที", wait=1.0)
        self.glow(f1[2], ddim, YEL)
        self.glow(f1[3], ldim, YEL)
        self.play(f1[4].animate.set_color(YEL))
        cycle(1)
        self.play(FadeIn(f2))
        self.cap("แล้วแปลงเป็นลมมาตรฐานด้วยสูตรเดียวกับโจทย์ 1")

        self.step(3, "แทนค่า")
        g1 = M(r"Q_2 = \frac{\pi}{4}(0.0445)^2(0.152)(30)", size=34)
        g2 = M(r"Q_2 = 0.00709\ \text{m}^3/\text{min}", size=36, color=HIGH)
        self.rows([g1, g2], -0.55, 1.05)
        self.play(FadeIn(g1))
        self.cap("แปลง mm → m ก่อน: 44.5 mm = 0.0445 m · 152 mm = 0.152 m")
        self.play(FadeIn(g2))
        self.cap("หมายเหตุ: โน้ตเขียน 0.00728 แต่กดเครื่องคิดเลขใหม่ได้ 0.00709 (ใช้ค่านี้)",
                 color=WARN, wait=2.8)
        self.play(FadeOut(VGroup(f1, g1)))
        self.play(f2.animate.move_to([PX, 1.85, 0]), g2.animate.move_to([PX, 0.75, 0]))
        g3 = M(r"P_2 = 687 + 101.3 = 788.3\ \text{kPa abs}", size=32, color=HIGH)
        g4 = M(r"T_1 = 293\ \text{K},\quad T_2 = 300\ \text{K}", size=32)
        self.rows([g3, g4], -0.3, 0.85)
        self.play(FadeIn(g3))
        self.glow(g3, r3, HIGH)
        self.play(FadeIn(g4))
        self.cap("ค่าสัมบูรณ์: บวก 101.3 kPa · °C + 273 = K")
        self.play(FadeOut(VGroup(g3, g4)))
        h1 = M(r"Q_1 = 0.00709\left(\frac{788.3}{101.3}\right)\left(\frac{293}{300}\right)",
               size=34)
        h2 = M(r"= 0.00709 \times 7.782 \times 0.9767", size=34)
        h3 = M(r"Q_1 = 0.0539\ \text{std m}^3/\text{min}", size=38, color=OK)
        self.rows([h1, h2, h3], -0.4, 1.05)
        box2 = SurroundingRectangle(h3, color=OK, buff=0.15)
        self.play(FadeIn(h1))
        self.play(FadeIn(h2))
        self.cap("อัตราส่วนความดัน 7.782 · อัตราส่วนอุณหภูมิ 0.9767")
        self.play(Write(h3), Create(box2))
        self.cap("คำตอบ: 0.0539 std m³/min (โน้ตได้ 0.0555 เพราะยกค่า 0.00728 มาคูณ)",
                 color=OK, wait=2.8)

        self.step(4, "ตรวจ")
        k1 = T("0.0539 ÷ 0.00709 ≈ 7.6 เท่า ใกล้ 788.3/101.3 ✓", 22, OK)
        self.rows([k1], -3.35)
        self.play(FadeIn(k1, shift=0.1 * UP))
        cycle(1)
        self.cap("ลมอัด 1 ลิตร = ลมรอบตัวราว 7.6 ลิตร → ตอบเป็น std ต้องมากกว่าเสมอ ✓", wait=2.5)


# ======================================================================
class FXG3_HPReceiver(ExamScene):
    """p13: 100 scfm @100 psig, eta 0.75 -> 18.0 / 24.0 HP ; p14-15: receiver 660 / 495 gal."""

    def construct(self):
        self.head("กำลังคอมเพรสเซอร์ + ขนาดถังพักลม", "W09 · หน้า 13-15")

        motor = block("มอเตอร์", "", w=1.8, h=1.1, pos=[-5.7, 0.6, 0], top_size=20)
        shaft = Line([-4.8, 0.6, 0], [-4.3, 0.6, 0], color=METAL, stroke_width=7)
        comp = block("คอมเพรสเซอร์", "", w=2.0, h=1.3, pos=[-3.3, 0.6, 0], top_size=20)
        a_in = varrow(-3.3, -1.0, -0.05, AIR, 4)
        in_l = M(r"P_{in} = 14.7\ \text{psia}", size=28, color=AIR).move_to([-3.3, -1.35, 0])
        a_out = harrow(-2.3, -0.2, 0.6, HIGH, 5)
        out_l = M(r"P_{out} = 100\ \text{psig}", size=28, color=HIGH).move_to([-0.95, 1.15, 0])
        q_l = M(r"Q = 100\ \text{scfm}", size=28, color=HIGH).move_to([-1.1, 0.1, 0])
        hp_l = M(r"HP = \ ?", size=30, color=YEL).move_to([-5.7, 1.55, 0])
        eta_l = M(r"\eta_o = 75\%", size=28, color=YEL).move_to([-5.7, -0.35, 0])

        # ---------------- step 1
        self.step(1, "โจทย์ 1 เข้าใจ")
        self.play(FadeIn(motor), Create(shaft), FadeIn(comp))
        self.play(GrowArrow(a_in), FadeIn(in_l), GrowArrow(a_out), FadeIn(out_l), FadeIn(q_l))
        self.play(FadeIn(hp_l), FadeIn(eta_l))
        self.cap("โจทย์ (หน้า 13): จ่ายลม 100 scfm ที่ 100 psig ประสิทธิภาพรวม 75%", color=WHITE)
        self.glow(q_l, a_out, HIGH)
        self.glow(out_l)
        self.cap("ต้องใช้มอเตอร์กี่แรงม้า? งาน = ดันลมจาก 14.7 psia ขึ้นไปเป็นความดันสูง",
                 color=WHITE)
        self.glow(hp_l, motor, YEL)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"HP_{theo}", r"=", r"\frac{P_{in}\,Q}{65.4}",
               r"\left[\left(\frac{P_{out}}{P_{in}}\right)^{0.286}-1\right]", size=34)
        e2 = M(r"HP_{act}", r"=", r"\frac{HP_{theo}}{\eta_o}", size=38)
        e3 = M(r"0.286 = \frac{k-1}{k},\quad k = 1.4", size=30)
        e4 = T("P = psia · Q = scfm", 22, GRAYTXT)
        self.rows([e1, e2, e3, e4], 1.85, 1.15)
        self.play(FadeIn(e1))
        self.cap("สูตรกำลังอัดแบบไอเซนโทรปิก หน่วยอังกฤษ (หน้า 13)", wait=1.0)
        self.glow(e1[2], VGroup(a_in, q_l), AIR)
        self.cap("ส่วนแรก: ความดันขาเข้า × อัตราไหล ÷ 65.4", wait=1.6)
        self.glow(e1[3], VGroup(out_l, in_l), HIGH)
        self.cap("ในวงเล็บ: อัตราส่วนอัด ยกกำลัง 0.286 แล้วลบ 1", wait=1.6)
        self.play(FadeIn(e2))
        self.glow(e2[2], VGroup(motor, eta_l), YEL)
        self.cap("กำลังจริง = กำลังทฤษฎี ÷ ประสิทธิภาพรวม")
        self.play(FadeIn(e3), FadeIn(e4))
        self.cap("SI: ใช้ 17.1 แทน 65.4 (P เป็น kPa abs, Q เป็น m³/min) ได้ kW", wait=2.6)

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e2, e3, e4)))
        self.relabel_m(out_l, r"P_{out} = 114.7\ \text{psia}", 28, HIGH)
        self.cap("แปลงเป็นค่าสัมบูรณ์ก่อน: 100 + 14.7 = 114.7 psia")
        s1 = M(r"\frac{14.7 \times 100}{65.4} = 22.48", size=34)
        s2 = M(r"\left(\frac{114.7}{14.7}\right)^{0.286} = 1.7997", size=34)
        s3 = M(r"HP_{theo} = 22.48\,(1.7997 - 1) = 18.0\ \text{HP}", size=34)
        s4 = M(r"HP_{act} = \frac{18.0}{0.75} = 24.0\ \text{HP}", size=40, color=OK)
        self.rows([s1, s2, s3, s4], 1.85, 1.1)
        box = SurroundingRectangle(s4, color=OK, buff=0.15)
        self.play(FadeIn(s1))
        self.glow(s1, VGroup(in_l, q_l), AIR)
        self.play(FadeIn(s2))
        self.glow(s2, out_l, HIGH)
        self.cap("อัตราส่วนอัด 114.7 / 14.7 = 7.80 → ยกกำลัง 0.286 = 1.7997")
        self.play(FadeIn(s3))
        self.cap("กำลังทฤษฎี = 22.48 × 0.7997 = 18.0 HP")
        self.play(Write(s4), Create(box))
        self.relabel_m(hp_l, r"HP = 24.0", 30, OK)
        self.cap("คำตอบ: ต้องใช้มอเตอร์ 24.0 HP", color=OK)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = T("กำลังจริง 24.0 > ทฤษฎี 18.0 เพราะมีการสูญเสีย ✓", 22, OK)
        self.rows([c1], -2.4)
        self.play(FadeIn(c1, shift=0.1 * UP))
        self.cap("กับดัก: ลืมแปลง 100 psig เป็น 114.7 psia → ได้คำตอบผิด", color=WARN)
        self.clear_stage()

        # ================= problem 2: receiver sizing (page 14-15)
        comp2 = block("คอมเพรสเซอร์", "", w=1.6, h=1.0, pos=[-6.15, 0.2, 0], top_size=17)
        tank = RoundedRectangle(corner_radius=0.5, width=2.0, height=3.0, color=METAL,
                                stroke_width=4)
        tank.move_to([-3.0, 0.0, 0])
        pt = ValueTracker(100.0)
        tank_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.45, width=1.9, height=2.9, stroke_width=0, fill_color=HIGH,
            fill_opacity=0.12 + 0.5 * (pt.get_value() - 70) / 40).move_to([-3.0, 0.0, 0]))
        vr_l = M(r"V_r = \ ?", size=32, color=WHITE).move_to([-3.0, 0.0, 0]).set_z_index(3)
        a_c = harrow(-5.35, -4.0, 0.2, AIR, 4)
        qc_l = M(r"Q_c", size=30, color=AIR).move_to([-4.67, 0.95, 0])
        gc = np.array([-1.0, 0.9, 0])
        gauge = Circle(radius=0.55, color=METAL, stroke_width=3, fill_color=DARK,
                       fill_opacity=1).move_to(gc)
        stem = Line([-2.0, 0.9, 0], [-1.55, 0.9, 0], color=METAL, stroke_width=4)

        def gang(p):
            return PI * (1.25 - 1.5 * (p - 70) / 40)

        def rim(p, r):
            a = gang(p)
            return gc + r * np.array([np.cos(a), np.sin(a), 0])

        ticks = VGroup(Line(rim(80, 0.4), rim(80, 0.55), color=AIR, stroke_width=3),
                       Line(rim(100, 0.4), rim(100, 0.55), color=WARN, stroke_width=3))
        tk80 = T("80", 17, AIR).move_to(rim(80, 0.82))
        tk100 = T("100", 17, WARN).move_to(rim(100, 0.85))
        needle = always_redraw(lambda: Line(gc, rim(pt.get_value(), 0.45), color=YEL,
                                            stroke_width=4))
        pmax_l = M(r"P_{max} = 100\ \text{psi}", size=28, color=WARN).move_to([-0.55, -0.05, 0])
        pmin_l = M(r"P_{min} = 80\ \text{psi}", size=28, color=AIR).move_to([-0.55, -0.55, 0])
        a_r = harrow(-2.0, 1.2, -1.1, HIGH, 5)
        qr_l = M(r"Q_r = 20\ \text{scfm}", size=28, color=HIGH).move_to([-0.4, -1.5, 0])
        t_l = M(r"t = 6\ \text{min}", size=30, color=YEL).move_to([-3.0, -1.95, 0])

        self.step(1, "โจทย์ 2 เข้าใจ")
        self.play(FadeIn(comp2), Create(tank), FadeIn(tank_fill), FadeIn(vr_l))
        self.play(GrowArrow(a_c), FadeIn(qc_l))
        self.play(Create(stem), FadeIn(gauge), FadeIn(ticks), FadeIn(tk80), FadeIn(tk100),
                  FadeIn(needle))
        self.cap("ถังพักลม = แบตเตอรี่ของลม: จ่ายลมแทนคอมเพรสเซอร์ได้ช่วงหนึ่ง (หน้า 14)")
        self.play(GrowArrow(a_r), FadeIn(qr_l), FadeIn(t_l), FadeIn(pmax_l), FadeIn(pmin_l))
        self.cap("โจทย์ (หน้า 15): ระบบใช้ลม 20 scfm นาน 6 นาที ถังลดจาก 100 เหลือ 80 psi",
                 color=WHITE, wait=1.0)
        self.play(pt.animate.set_value(80), run_time=3.0, rate_func=linear)
        self.cap("(a) คอมเพรสเซอร์หยุด Qc = 0 · (b) คอมเพรสเซอร์ช่วยจ่าย Qc = 5 scfm",
                 color=WHITE)
        self.play(pt.animate.set_value(100), run_time=1.0)

        self.step(2, "สูตร")
        e1 = M(r"V_r\,\frac{P_{max}-P_{min}}{14.7}", r"=", r"t\,(Q_r-Q_c)", size=36)
        e2 = M(r"V_r", r"=", r"\frac{", r"t", r"\,(", r"Q_r", r"-", r"Q_c", r")\times 14.7",
               r"}{", r"P_{max}-P_{min}", r"}", size=40)
        e3 = T("ได้ ft³ · 1 gal = 0.1337 ft³", 22, GRAYTXT)
        e4 = T("SI: ใช้ 101.3 kPa แทน 14.7 ได้ m³", 22, GRAYTXT)
        self.rows([e1, e2, e3, e4], 1.85, 1.2)
        self.play(FadeIn(e1))
        self.cap("ซ้าย: ลมที่ถังปล่อยออก (คิดเป็น free air) · ขวา: ลมที่ระบบใช้เกินคอมเพรสเซอร์ให้",
                 wait=2.8)
        self.glow(e1[0], VGroup(tank, gauge), HIGH)
        self.glow(e1[2], VGroup(a_r, a_c), AIR)
        self.play(FadeIn(e2))
        self.cap("ย้ายข้างหา V_r", wait=1.0)
        self.glow(e2[3], t_l, YEL)
        self.glow(e2[5], VGroup(a_r, qr_l), HIGH)
        self.glow(e2[7], VGroup(a_c, qc_l), AIR)
        self.glow(e2[10], VGroup(pmax_l, pmin_l, gauge), WARN)
        self.play(FadeIn(e3), FadeIn(e4))
        self.cap("ΔP ใช้ psi ได้เลย (ผลต่าง gage = ผลต่าง abs)")

        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e3, e4)))
        self.play(e2.animate.move_to([PX, 1.85, 0]))
        self.relabel_m(qc_l, r"Q_c = 0", 30, AIR)
        s1 = M(r"V_r = \frac{6\,(20-0)(14.7)}{100-80}", size=34)
        s2 = M(r"= \frac{1764}{20} = 88.2\ \text{ft}^3", size=34)
        s3 = M(r"\frac{88.2}{0.1337} \approx 660\ \text{gal}", size=38, color=OK)
        self.rows([s1, s2, s3], 0.7, 1.1)
        self.play(FadeIn(s1))
        self.cap("(a) คอมเพรสเซอร์หยุด → Qc = 0")
        self.play(FadeIn(s2))
        self.play(FadeIn(s3))
        bxa = SurroundingRectangle(s3, color=OK, buff=0.12)
        self.play(Create(bxa))
        self.cap("(a) ถังต้องใหญ่ 88.2 ft³ ≈ 660 แกลลอน", color=OK)
        self.play(FadeOut(VGroup(e2, s1, s2)))
        self.play(VGroup(s3, bxa).animate.move_to([PX, 1.85, 0]))
        self.relabel_m(qc_l, r"Q_c = 5", 30, AIR)
        self.play(ShowPassingFlash(a_c.copy().set_color(YEL), time_width=0.7), run_time=1.0)
        u1 = M(r"V_r = \frac{6\,(20-5)(14.7)}{100-80}", size=34)
        u2 = M(r"= \frac{1323}{20} = 66.2\ \text{ft}^3", size=34)
        u3 = M(r"\frac{66.2}{0.1337} \approx 495\ \text{gal}", size=38, color=OK)
        self.rows([u1, u2, u3], 0.7, 1.1)
        self.play(FadeIn(u1))
        self.cap("(b) คอมเพรสเซอร์ยังช่วยจ่าย 5 scfm → ถังขาดแค่ 20 - 5 = 15 scfm")
        self.play(FadeIn(u2))
        self.play(FadeIn(u3))
        bxb = SurroundingRectangle(u3, color=OK, buff=0.12)
        self.play(Create(bxb))
        self.relabel_m(vr_l, r"V_r \approx 495", 30, WHITE)
        self.cap("(b) ถังเล็กลงเหลือ 66.2 ft³ ≈ 495 แกลลอน", color=OK)

        self.step(4, "ตรวจ")
        c1 = T("(b) เล็กกว่า (a) เพราะคอมเพรสเซอร์ช่วยจ่าย ✓", 22, OK)
        c2 = T("งานจริงเผื่อ +25% โหลดเกิน และ +25% ขยายโรงงาน", 22, YEL)
        self.rows([c1, c2], -2.4, 0.62)
        self.play(FadeIn(c1, shift=0.1 * UP))
        self.play(pt.animate.set_value(80), run_time=2.0, rate_func=linear)
        self.play(FadeIn(c2, shift=0.1 * UP))
        self.cap("เผื่อขนาดถังตามกฎหน้า 15 แล้วเลือกถังขนาดมาตรฐานที่ใหญ่กว่า", wait=2.5)


# ======================================================================
class FXG4_ValvePipe(ExamScene):
    """p38: Cv = 1.46 (note 1.38) ; p44-45 pipe pressure drop ; p42-43 + p4 piping layout."""

    def construct(self):
        self.head("ขนาดวาล์ว Cv + ความดันตกในท่อลม", "W09 · หน้า 38, 42-45")

        yt, yb = 0.55, 0.05
        walls = VGroup(Line([-6.7, yt, 0], [-4.05, yt, 0]), Line([-6.7, yb, 0], [-4.05, yb, 0]),
                       Line([-2.95, yt, 0], [-0.3, yt, 0]), Line([-2.95, yb, 0], [-0.3, yb, 0]))
        walls.set_color(METAL).set_stroke(width=4)
        flow = VGroup(Rectangle(width=2.65, height=0.46, stroke_width=0, fill_color=HIGH,
                                fill_opacity=0.5).move_to([-5.375, 0.3, 0]),
                      Rectangle(width=2.65, height=0.46, stroke_width=0, fill_color=HIGH,
                                fill_opacity=0.3).move_to([-1.625, 0.3, 0]))
        vbox = Square(1.1, color=OK, stroke_width=4, fill_color=DARK, fill_opacity=1)
        vbox.move_to([-3.5, 0.3, 0])
        bow = VGroup(Polygon([-3.85, 0.6, 0], [-3.85, 0.0, 0], [-3.5, 0.3, 0]),
                     Polygon([-3.15, 0.6, 0], [-3.15, 0.0, 0], [-3.5, 0.3, 0]))
        bow.set_stroke(OK, 3).set_fill(OK, 0.4)
        valve = VGroup(vbox, bow)
        g1c, g2c = np.array([-5.3, 1.55, 0]), np.array([-1.7, 1.55, 0])
        gauges = VGroup(
            Line([-5.3, yt, 0], g1c + [0, -0.38, 0], color=METAL, stroke_width=3),
            Circle(radius=0.38, color=METAL, stroke_width=3, fill_color=DARK,
                   fill_opacity=1).move_to(g1c),
            Line([-1.7, yt, 0], g2c + [0, -0.38, 0], color=METAL, stroke_width=3),
            Circle(radius=0.38, color=METAL, stroke_width=3, fill_color=DARK,
                   fill_opacity=1).move_to(g2c))
        gl1 = M(r"P_1", size=28, color=HIGH).move_to(g1c).set_z_index(3)
        gl2 = M(r"P_2", size=28, color=HIGH).move_to(g2c).set_z_index(3)
        p1_l = M(r"P_1 = 100\ \text{psig}", size=28, color=HIGH).move_to([-5.3, -0.45, 0])
        p2_l = M(r"P_2 = \ ?", size=28, color=HIGH).move_to([-1.7, -0.45, 0])
        t1_l = M(r"T_1 = 80^\circ\text{F}", size=28, color=YEL).move_to([-5.3, -1.05, 0])
        dp_l = M(r"\Delta P = 12\ \text{psi}", size=30, color=YEL).move_to([-3.5, -1.65, 0])
        a_q = harrow(-4.6, -2.4, -2.3, HIGH, 5)
        q_l = M(r"Q = 50\ \text{scfm}", size=28, color=HIGH).move_to([-3.5, -2.75, 0])
        cv_l = M(r"C_v = \ ?", size=30, color=OK).move_to([-3.5, 1.25, 0])

        # ---------------- step 1
        self.step(1, "เข้าใจโจทย์")
        self.play(Create(walls), FadeIn(flow), FadeIn(valve))
        self.play(FadeIn(cv_l))
        self.cap("Cv = ตัวเลขบอกว่าวาล์วยอมให้ลมผ่านได้มากแค่ไหน (ยิ่งมาก ยิ่งไหลง่าย)")
        self.play(FadeIn(gauges), FadeIn(gl1), FadeIn(gl2), FadeIn(p1_l), FadeIn(p2_l),
                  FadeIn(t1_l))
        self.play(GrowArrow(a_q), FadeIn(q_l), FadeIn(dp_l))
        self.cap("โจทย์ (หน้า 38): ต้องการลม 50 scfm ที่ 100 psig อุณหภูมิ 80°F", color=WHITE)
        self.glow(q_l, a_q, HIGH)
        self.cap("ยอมให้ความดันตกคร่อมวาล์วไม่เกิน 12 psi → เลือก Cv ต่ำสุดเท่าไร?",
                 color=WHITE)
        self.glow(dp_l, valve, YEL)

        # ---------------- step 2
        self.step(2, "สูตร")
        e1 = M(r"Q", r"=", r"22.7\,", r"C_v", r"\sqrt{\frac{", r"P_2", r"\,(", r"P_1-P_2",
               r")}{", r"T_1", r"}}", size=40)
        e2 = M(r"C_v = \frac{Q}{22.7\sqrt{P_2\,(P_1-P_2)/T_1}}", size=36, color=OK)
        e3 = T("Q = scfm · P = psia · T = °R", 22, GRAYTXT)
        e4 = T("ถ้า P2 < 0.53·P1 → choked: ลมที่คอวาล์วเร็วเท่าเสียง Q ไม่เพิ่มอีก", 22, WARN)
        self.rows([e1, e2, e3, e4], 1.85, 1.2)
        self.play(FadeIn(e1))
        self.cap("ลมยุบตัวได้ → อัตราไหลขึ้นกับ P2, ความดันตก และอุณหภูมิ", wait=1.0)
        self.glow(e1[0], a_q, HIGH)
        self.glow(e1[3], valve, OK)
        self.glow(e1[5], VGroup(gauges[3], gl2), HIGH)
        self.glow(e1[7], dp_l, YEL)
        self.glow(e1[9], t1_l, YEL)
        self.play(FadeIn(e2))
        self.cap("ย้ายข้างหา Cv")
        self.play(FadeIn(e3), FadeIn(e4))
        self.cap("ทุกค่าเป็นค่าสัมบูรณ์ · ตรวจ choked ทุกครั้ง", color=WARN)

        # ---------------- step 3
        self.step(3, "แทนค่า")
        self.play(FadeOut(VGroup(e1, e3, e4)))
        self.play(e2.animate.move_to([PX, 1.85, 0]))
        s1 = M(r"P_1 = 100 + 14.7 = 114.7\ \text{psia}", size=32, color=HIGH)
        s2 = M(r"P_2 = 114.7 - 12 = 102.7\ \text{psia}", size=32, color=HIGH)
        s3 = M(r"T_1 = 80 + 460 = 540^\circ\text{R}", size=32, color=YEL)
        self.rows([s1, s2, s3], 0.75, 0.85)
        self.play(FadeIn(s1))
        self.relabel_m(p1_l, r"P_1 = 114.7\ \text{psia}", 28, HIGH)
        self.play(FadeIn(s2))
        self.relabel_m(p2_l, r"P_2 = 102.7\ \text{psia}", 28, HIGH)
        self.cap("ความดันขาออก = ขาเข้า ลบ ความดันตกที่ยอมได้ 12 psi")
        self.play(FadeIn(s3))
        self.relabel_m(t1_l, r"T_1 = 540^\circ\text{R}", 28, YEL)
        self.play(FadeOut(VGroup(s1, s2, s3)))
        u1 = M(r"\sqrt{\frac{102.7 \times 12}{540}} = \sqrt{2.282} = 1.511", size=34)
        u2 = M(r"C_v = \frac{50}{22.7 \times 1.511} = \frac{50}{34.29}", size=34)
        u3 = M(r"C_v = 1.46", size=44, color=OK)
        self.rows([u1, u2, u3], 0.6, 1.15)
        box = SurroundingRectangle(u3, color=OK, buff=0.15)
        self.play(FadeIn(u1))
        self.cap("ในรากที่สอง: 102.7 × 12 ÷ 540 = 2.282 → ราก = 1.511")
        self.play(FadeIn(u2))
        self.play(Write(u3), Create(box))
        self.relabel_m(cv_l, r"C_v = 1.46", 30, OK)
        self.cap("หมายเหตุ: โน้ตเขียน 1.38 แต่ 50 ÷ 34.29 = 1.46 (คิดใหม่แล้ว ใช้ค่านี้)",
                 color=WARN, wait=2.8)

        # ---------------- step 4
        self.step(4, "ตรวจ")
        c1 = T("P2/P1 = 102.7/114.7 = 0.895 > 0.53 → ไม่ choked ✓", 22, OK)
        c2 = T("เลือกวาล์ว Cv ≥ 1.46 (เล็กกว่านี้ ความดันตกเกิน 12 psi)", 22, OK)
        self.rows([c1, c2], -2.65, 0.62)
        self.play(FadeIn(c1, shift=0.1 * UP))
        self.glow(c1, VGroup(gauges[1], gauges[3]), OK)
        self.play(FadeIn(c2, shift=0.1 * UP))
        self.cap("สูตรใช้ได้เพราะไม่ choked · ค่าที่ได้คือ Cv ต่ำสุดที่ยอมรับได้", wait=2.4)
        self.clear_stage()

        # ================= pipe pressure drop (page 44-45)
        self.step(1, "ความดันตกในท่อลม")
        pw = VGroup(Line([-6.5, 0.9, 0], [0.8, 0.9, 0]), Line([-6.5, 0.1, 0], [0.8, 0.1, 0]))
        pw.set_color(METAL).set_stroke(width=5)
        pfill = Rectangle(width=7.3, height=0.76, stroke_width=0, fill_color=HIGH,
                          fill_opacity=0.35).move_to([-2.85, 0.5, 0])
        qa = harrow(-5.5, -2.5, 0.5, HIGH, 5)
        qlab = M(r"Q\ (\text{scfm})", size=28, color=HIGH).move_to([-4.6, 1.3, 0])
        ld = dim((-6.5, -0.35), (0.8, -0.35), YEL)
        llab = M(r"L\ (\text{ft})", size=28, color=YEL).move_to([-2.85, -0.75, 0])
        dd = dim((0.55, 0.12), (0.55, 0.88), OK)
        dlab = M(r"d\ (\text{in})", size=26, color=OK).move_to([0.55, 1.3, 0])
        gcc = np.array([-2.4, 1.65, 0])
        cg = VGroup(Line([-2.4, 0.9, 0], gcc + [0, -0.33, 0], color=METAL, stroke_width=3),
                    Circle(radius=0.33, color=METAL, stroke_width=3, fill_color=DARK,
                           fill_opacity=1).move_to(gcc))
        crlab = M(r"CR = \frac{P_{pipe}}{14.7}", size=26, color=WARN)
        crlab.move_to(gcc + np.array([0.45 + crlab.width / 2, 0, 0]))
        if crlab.get_right()[0] > dlab.get_left()[0] - 0.1:
            crlab.shift(LEFT * (crlab.get_right()[0] - dlab.get_left()[0] + 0.15))

        self.play(Create(pw), FadeIn(pfill))
        self.play(GrowArrow(qa), FadeIn(qlab), FadeIn(ld), FadeIn(llab))
        self.play(FadeIn(dd), FadeIn(dlab), FadeIn(cg), FadeIn(crlab))
        self.cap("ลมไหลในท่อยาว → ความดันตกตามทาง (หน้า 44: ท่อเหล็ก Schedule 40)")
        f1 = M(r"P_f", r"=", r"\frac{0.1025\,", r"L", r"\,", r"Q", r"^2}{3600\,", r"CR",
               r"\,", r"d", r"^{5.31}}", size=42)
        f1[0].set_color(WARN)
        self.rows([f1], 1.75)
        self.play(FadeIn(f1))
        self.cap("P_f = ความดันตก (psi)", wait=1.0)
        self.glow(f1[3], ld, YEL)
        self.cap("ท่อยาว L มาก → ตกมาก", wait=1.2)
        self.glow(f1[5], qa, HIGH)
        self.cap("Q อยู่บนเศษ ยกกำลังสอง → ลมไหลมาก ตกมากแบบทวีคูณ", wait=1.6)
        self.glow(f1[7], cg, WARN)
        self.cap("CR = ความดันในท่อ (psia) ÷ 14.7 · ลมยิ่งอัดแน่น ยิ่งตกน้อย", wait=1.8)
        self.glow(f1[9], dd, OK)
        self.cap("d อยู่ใต้เศษ ยกกำลัง 5.31 → ขยายท่อนิดเดียว ความดันตกลดลงมาก", wait=1.8)

        self.step(2, "ผลที่ต้องจำ")
        g1 = M(r"Q \times 2 \;\Rightarrow\; P_f \times 4", size=36, color=HIGH)
        g2 = M(r"d \times 2 \;\Rightarrow\; P_f \div 2^{5.31} \approx \div 40", size=36, color=OK)
        g3 = T("เกณฑ์: ความดันตกทั้งแนวท่อ ≤ 10% (0.3-0.5 bar)", 22, YEL)
        self.rows([g1, g2, g3], 0.55, 1.0)
        self.play(FadeIn(g1))
        self.cap("Q เพิ่ม 2 เท่า → 2² = 4 เท่า")
        self.play(FadeIn(g2))
        self.cap("ท่อโต 2 เท่า → ความดันตกเหลือราว 1/40")
        self.play(FadeIn(g3))
        self.cap("หน้า 45: โนโมกราฟวางไม้บรรทัดผ่าน Q, ความดัน, ขนาดท่อ → อ่านความดันตกต่อ 100 ft",
                 wait=2.8)
        self.clear_stage()

        # ================= piping layout (page 4, 42-43)
        self.step(3, "เดินท่อแบบไหนดี")
        tb = T("Branch line (ปลายตัน)", 22, WARN).move_to([-3.6, 1.6, 0])
        cb = block("คอมฯ", "", w=1.0, h=0.6, pos=[-6.2, 0.6, 0], top_size=17)
        mb = Line([-5.7, 0.6, 0], [-1.2, 0.6, 0], color=HIGH, stroke_width=5)
        drops_b = VGroup()
        for i, x in enumerate([-4.6, -3.2, -1.8]):
            op = 0.9 - 0.3 * i
            drops_b.add(Line([x, 0.6, 0], [x, -0.3, 0], color=HIGH, stroke_width=4))
            drops_b.add(Circle(radius=0.14, color=HIGH, fill_color=HIGH, fill_opacity=op,
                               stroke_width=2).move_to([x, -0.44, 0]))
        lb1 = T("ปลายสายแรงดันตกมาก", 19, WARN).move_to([-3.6, -1.2, 0])
        lb2 = T("ท่อต้นทางเสีย → หยุดทั้งระบบ", 19, WARN).move_to([-3.6, -1.75, 0])
        tr = T("Ring main (วงแหวน)", 22, OK).move_to([4.2, 1.75, 0])
        cr = block("คอมฯ", "", w=1.0, h=0.6, pos=[1.4, 0.5, 0], top_size=17)
        loop = Rectangle(width=4.2, height=1.4, color=HIGH, stroke_width=5).move_to([4.4, 0.5, 0])
        feed = Line([1.9, 0.5, 0], [2.3, 0.5, 0], color=HIGH, stroke_width=5)
        drops_r = VGroup()
        for x in [3.2, 4.4, 5.6]:
            drops_r.add(Line([x, -0.2, 0], [x, -0.7, 0], color=HIGH, stroke_width=4))
            drops_r.add(Circle(radius=0.14, color=HIGH, fill_color=HIGH, fill_opacity=0.9,
                               stroke_width=2).move_to([x, -0.84, 0]))
        lr1 = T("ลมเข้าได้ 2 ทาง แรงดันสม่ำเสมอ", 19, OK).move_to([4.2, -1.4, 0])
        lr2 = T("ปิดวาล์วซ่อมทีละส่วนได้", 19, OK).move_to([4.2, -1.95, 0])

        self.play(FadeIn(tb), FadeIn(cb), Create(mb), FadeIn(drops_b))
        self.play(ShowPassingFlash(mb.copy().set_color(YEL), time_width=0.5), run_time=1.2)
        self.play(FadeIn(lb1), FadeIn(lb2))
        self.cap("Branch: ท่อแยกเป็นกิ่งปลายตัน (หน้า 42) จุดไกลสุดแรงดันเหลือน้อย")
        self.play(FadeIn(tr), FadeIn(cr), Create(feed), Create(loop), FadeIn(drops_r))
        up = Line([2.3, 0.5, 0], [2.3, 1.2, 0]).append_vectorized_mobject(
            Line([2.3, 1.2, 0], [6.5, 1.2, 0]))
        dn = Line([2.3, 0.5, 0], [2.3, -0.2, 0]).append_vectorized_mobject(
            Line([2.3, -0.2, 0], [6.5, -0.2, 0]))
        self.play(ShowPassingFlash(up.set_color(YEL).set_stroke(width=6), time_width=0.5),
                  ShowPassingFlash(dn.set_color(YEL).set_stroke(width=6), time_width=0.5),
                  run_time=1.6)
        self.play(FadeIn(lr1), FadeIn(lr2))
        self.cap("Ring: ท่อวนเป็นวง ลมไปถึงทุกจุดได้ 2 ทาง → นิยมใช้ในโรงงาน (หน้า 4, 43)")

        # gooseneck (page 4)
        gp = VGroup(Line([-3.0, -2.95, 0], [3.0, -2.95, 0]), Line([-3.0, -3.4, 0], [3.0, -3.4, 0]))
        gp.set_color(METAL).set_stroke(width=4)
        water = Rectangle(width=6.0, height=0.12, stroke_width=0, fill_color=AIR,
                          fill_opacity=0.8).move_to([0, -3.33, 0])
        tap = VMobject(color=OK, stroke_width=5).set_points_as_corners(
            [np.array(p, dtype=float) for p in
             [[1.0, -2.95, 0], [1.0, -2.45, 0], [1.6, -2.45, 0], [1.6, -2.75, 0]]])
        gl = T("ท่อแยกต่อจากด้านบน (gooseneck)", 18, OK).move_to([-1.0, -2.6, 0])
        wl = T("น้ำนอนก้นท่อ", 17, AIR).move_to([2.3, -3.7, 0])
        self.play(Create(gp), FadeIn(water))
        self.play(Create(tap), FadeIn(gl), FadeIn(wl))
        self.cap("ท่อหลักเอียง 1-2% ให้น้ำไหลไปจุดต่ำสุดที่มี drain")
        self.glow(gl, tap, OK)
        self.cap("ท่อแยกเข้าเครื่องต่อจาก 'ด้านบน' ท่อหลักเสมอ → น้ำก้นท่อไม่ไหลเข้าเครื่อง",
                 color=WHITE, wait=3.0)
