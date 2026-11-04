"""eps8_lib — ตัวช่วยร่วมของคลิป EPS8 (บทที่ 8: ลักษณะสมบัติเครื่องกำเนิดไฟฟ้ากระแสตรง)

ใช้คู่กับ mlib.py (SafeScene + [LAYOUT] linter).  ไฟล์ซีน: eps8_a.py (หน้า 1-7), eps8_b.py (8-12) ...
สีประจำปริมาณ (ซีรีส์นี้ ห้ามสลับ):  E=แดง  ฟลักซ์φ=ฟ้า  If=เขียว  Ia=เหลืองทอง  IL=ฟ้าเขียว  Is=ม่วง  เส้นR=เหลืองทอง
ตัวช่วยหลัก
  Lesson           ฐานซีน: head() หัวเรื่อง+ป้ายหน้า, say() คำบรรยายบน (สลับนุ่ม), newpage(), mark() บันทึกเวลาให้ eps8_make.py ทำ tile sheet
  Board            กระดานตัวอย่างคำนวณ ทีละขั้น (1 เข้าใจโจทย์ 2 สูตร 3 แทนค่า 4 ตรวจ)
  machine()        ภาพตัดเครื่องกำเนิด 2 ขั้ว (ขั้ว N/S, ขดลวดฟิลด์, อาร์เมเจอร์, เส้นฟลักซ์ที่ปรับความหนาตามระดับ)
  domains()        โมเลกุลแม่เหล็กในเนื้อเหล็ก (ลูกศรเล็ก หันตามกันเมื่อฟลักซ์เพิ่ม)
  curve_up/down    เคอร์ฟอิ่มตัว (ขาขึ้น/ขาลง ฮิสเตอรีซิส) แบบ normalized
  res_*            สัญลักษณ์วงจร (ตัวต้านทาน, ขดลวด, มิเตอร์, อาร์เมเจอร์) + wire()
กฎ: ห้ามใส่ภาษาไทยใน MathTex; ข้อความไทยใช้ Text; ตัวเลขต้องตรงกับ PDF บทที่ 8
"""
import json
import os
import numpy as np
from manim import *
from mlib import *

# ---------------------------------------------------------------- สี
C_E, C_PHI, C_IF, C_IA, C_IL, C_IS = EMF, FIELD, FORCE, CURRENT, OK, TORQUE
C_R = "#FFB300"          # เส้นความต้านทานฟิลด์ / ตัวต้านทาน
C_N = "#EF5350"          # ขั้ว N
C_S = "#42A5F5"          # ขั้ว S
YEL = "#FFD54F"
MARK_DIR = os.environ.get("EPS8_MARK_DIR") or ("D:/Desktop/manium/eps8_out/marks" if os.name == "nt" else "")


# ---------------------------------------------------------------- ฐานซีน
class Lesson(SafeScene):
    """หัวเรื่อง + ป้ายหน้า + คำบรรยายโซนบน (สลับนุ่ม) + บันทึกเวลาต้นจบของแต่ละท่อน"""

    def setup(self):
        self._cap = None
        self._marks = []
        self._ref = None

    def mark(self, label=""):
        self._marks.append([round(float(self.renderer.time), 2), label])

    def head(self, ttl, pg, size=28):
        self._ttl = title(ttl, size=size)
        self._ref = page_ref(pg)
        self.play(FadeIn(self._ttl), FadeIn(self._ref), run_time=0.5)

    def newpage(self, pg):
        self.mark("page")
        new = page_ref(pg)
        self.play(Transform(self._ref, new), run_time=0.4)

    def say(self, txt, color=GRAYTXT, hold=0.0, size=23):
        self.mark("beat")
        new = caption_top(txt, color=color, size=size)
        if self._cap is not None:
            self.play(FadeOut(self._cap), run_time=0.25)
        self.play(FadeIn(new), run_time=0.4)
        self._cap = new
        if hold:
            self.wait(hold)

    def tear_down(self):
        self.mark("end")
        # เรนเดอร์คลาวด์ไม่มีโฟลเดอร์ marks ฝั่งเครื่อง -> พิมพ์ลงล็อก (eps8_make.py marks <run_id> ดึงกลับมาทำ tile sheet)
        print("[EPS8_MARKS] " + type(self).__name__ + " " + json.dumps(self._marks), flush=True)
        if MARK_DIR:
            try:
                os.makedirs(MARK_DIR, exist_ok=True)
                with open(f"{MARK_DIR}/{type(self).__name__}.json", "w", encoding="utf-8") as f:
                    json.dump(self._marks, f)
            except Exception:
                pass
        super().tear_down()

    def glow(self, term, fig=None, color=WHITE, ring=None, run=0.9):
        """ไฮไลต์พจน์ในสูตร + ชิ้นส่วนในรูปพร้อมกัน (สีเดียวกัน)"""
        anims = [Indicate(term, color=WHITE, scale_factor=1.25),
                 Circumscribe(term, color=ring or color, run_time=run)]
        if fig is not None:
            anims.append(Indicate(fig, color=color, scale_factor=1.12))
        self.play(*anims, run_time=run)

    def exam(self, q, a, hold=2.2):
        self.fade_out_all(run_time=0.6)
        self._cap = None
        card = exam_card(q, a)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.wait(hold)


def exam_card(q, a, y=0.0):
    head = Text("จุดออกสอบ", font_size=22, color=YEL)
    qq = fit_width(Text(q, font_size=24, color=WHITE, line_spacing=0.9), 11.8)
    aa = fit_width(Text(a, font_size=22, color=OK, line_spacing=0.9), 11.8)
    return VGroup(head, qq, aa).arrange(DOWN, buff=0.35).move_to([0, y, 0])


def lab(tex, thai, color=WHITE, size=26, tex_color=None):
    """ป้าย  <สัญลักษณ์ MathTex> <คำอธิบายไทย>  (ไทยไม่อยู่ใน MathTex)"""
    a = MathTex(tex, font_size=size + 6, color=tex_color or color)
    b = Text(thai, font_size=size - 4, color=color)
    return VGroup(a, b).arrange(RIGHT, buff=0.2)


def tag(txt, color=GRAYTXT, size=20):
    return Text(txt, font_size=size, color=color)


def pointer(label_mob, target_pt, buff=0.08, color=GRAYTXT):
    """ลูกศรชี้จากป้ายไปชิ้นส่วน (ตั้งชื่อชิ้นส่วนตอนต้นคลิป)"""
    return Arrow(label_mob.get_bottom() if label_mob.get_center()[1] > target_pt[1] else label_mob.get_top(),
                 target_pt, buff=buff, color=color, stroke_width=3, tip_length=0.15,
                 max_tip_length_to_length_ratio=0.35)


# ---------------------------------------------------------------- กราฟ
def make_axes(x_len=5.6, y_len=3.6, xmax=1.0, ymax=1.0, xl=r"I_f", yl=r"E", pos=ORIGIN,
              xl_txt=None, yl_txt=None):
    """แกน E-If แบบไม่มีเลขขีด (รูปแนวคิด) วางให้ 'จุดกำเนิด' อยู่ที่ pos"""
    ax = Axes(x_range=[0, xmax, xmax], y_range=[0, ymax, ymax], x_length=x_len, y_length=y_len,
              axis_config={"color": GRAYTXT, "stroke_width": 2, "include_tip": True, "tip_length": 0.16,
                           "include_ticks": False, "tip_width": 0.14})
    pos = np.array([pos[0], pos[1], 0.0])
    ax.shift(pos - ax.c2p(0, 0))
    xlab = MathTex(xl, font_size=32, color=C_IF).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
    ylab = MathTex(yl, font_size=32, color=C_E).next_to(ax.y_axis.get_end(), LEFT, buff=0.15)
    g = VGroup(ax, xlab, ylab)
    g.ax, g.xlab, g.ylab = ax, xlab, ylab
    return g


def curve_up(x, er=0.06, k=2.6):
    """ขาขึ้นของเคอร์ฟอิ่มตัว (x ใน 0..~1.2 -> y ใน er..~1)"""
    return er + (1 - er) * np.tanh(k * x)


def curve_down(x, xm=1.2, g0=0.12, er=0.06, k=2.6):
    """ขาลง (ฮิสเตอรีซิส): สูงกว่าขาขึ้น เท่ากันที่ x=xm"""
    return curve_up(x, er, k) + g0 * np.clip(1 - x / xm, 0, 1) ** 2


# ---------------------------------------------------------------- ภาพตัดเครื่องกำเนิด
def machine(s=1.0, show_coil=True, label_poles=True):
    """เครื่องกำเนิด 2 ขั้ว (หน้าตัด) จุดศูนย์กลางที่ ORIGIN ขนาด 4.4s x 3.0s
    คืน VGroup ที่มี .flux (ลูกศร 5 เส้น) .coils .arm .poleN .poleS .rot (ลูกศรหมุน)"""
    yoke = RoundedRectangle(width=4.4 * s, height=3.1 * s, corner_radius=0.35 * s,
                            stroke_color=METAL, stroke_width=7, fill_color="#263238", fill_opacity=0.5)
    pn = Rectangle(width=0.8 * s, height=1.15 * s, stroke_color=METAL, stroke_width=2,
                   fill_color="#607D8B", fill_opacity=0.9).move_to([-1.62 * s, 0, 0])
    ps = pn.copy().move_to([1.62 * s, 0, 0])
    shn = Rectangle(width=0.26 * s, height=1.7 * s, stroke_color=METAL, stroke_width=2,
                    fill_color="#78909C", fill_opacity=0.95).move_to([-1.13 * s, 0, 0])
    shs = shn.copy().move_to([1.13 * s, 0, 0])
    coils = VGroup(*[Rectangle(width=0.66 * s, height=0.98 * s, stroke_color=C_IF, stroke_width=4,
                               fill_color=C_IF, fill_opacity=0.28).move_to(p.get_center())
                     for p in (pn, ps)])
    arm = Circle(radius=0.78 * s, stroke_color=METAL, stroke_width=3, fill_color="#455A64", fill_opacity=0.95)
    cond = VGroup(*[Dot(0.6 * s * np.array([np.cos(a), np.sin(a), 0]), radius=0.045 * s, color=C_IA)
                    for a in np.linspace(0, TAU, 12, endpoint=False)])
    flux = VGroup(*[Arrow([-1.0 * s, y * s, 0], [1.0 * s, y * s, 0], buff=0, color=C_PHI, stroke_width=4,
                          tip_length=0.2 * s, max_tip_length_to_length_ratio=0.2)
                    for y in (-0.55, -0.275, 0, 0.275, 0.55)])
    rot = Arc(radius=0.98 * s, start_angle=PI / 2 + 0.85, angle=-1.7, color=YEL, stroke_width=4).add_tip(tip_length=0.16 * s)
    parts = [yoke, pn, ps, shn, shs]
    if show_coil:
        parts.append(coils)
    parts += [arm, cond, flux, rot]
    if label_poles:
        parts += [Text("N", font_size=int(30 * s), color=WHITE, weight=BOLD).move_to(pn.get_center() + UP * 0.0),
                  Text("S", font_size=int(30 * s), color=WHITE, weight=BOLD).move_to(ps.get_center())]
    g = VGroup(*parts)
    g.flux, g.coils, g.arm, g.poleN, g.poleS, g.rot, g.cond = flux, coils, arm, pn, ps, rot, cond
    g.s = s
    return g


def flux_set(flux, level):
    """ปรับความหนา/ความสว่างของเส้นฟลักซ์ตามระดับ 0..1"""
    level = float(np.clip(level, 0, 1))
    for a in flux:
        a.set_stroke(width=1.0 + 8.0 * level, opacity=0.18 + 0.82 * level)
        a.set_fill(opacity=0.18 + 0.82 * level)
    return flux


def domains(level_getter, w=2.2, h=1.5, rows=3, cols=5, seed=3):
    """กรอบเหล็กขยาย: ลูกศรเล็ก = โมเลกุลแม่เหล็ก หันตามกันมากขึ้นเมื่อ level (0..1) สูงขึ้น"""
    rng = np.random.RandomState(seed)
    ang0 = rng.uniform(-PI, PI, rows * cols)
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=METAL, stroke_width=3,
                           fill_color="#1c2a30", fill_opacity=0.85)
    cells = [np.array([(-(cols - 1) / 2 + c) * (w - 0.5) / (cols - 1), ((rows - 1) / 2 - r) * (h - 0.5) / (rows - 1), 0])
             for r in range(rows) for c in range(cols)]

    def build():
        lv = float(np.clip(level_getter(), 0, 1))
        arrs = VGroup()
        for c, a0 in zip(cells, ang0):
            th = a0 * (1 - lv)
            d = 0.2 * np.array([np.cos(th), np.sin(th), 0])
            arrs.add(Arrow(c + box.get_center() - d, c + box.get_center() + d, buff=0, color=YEL,
                           stroke_width=3, tip_length=0.11, max_tip_length_to_length_ratio=0.9))
        return arrs

    arrs = always_redraw(build)
    return box, arrs


# ---------------------------------------------------------------- สัญลักษณ์วงจร
def wire(*pts, color=GRAYTXT, width=3):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    return m


def res_zig(p0, p1, n=6, amp=0.11, color=C_R, width=3):
    """สัญลักษณ์ตัวต้านทาน (ซิกแซก) จาก p0 ไป p1"""
    p0, p1 = np.array([*p0[:2], 0.0]), np.array([*p1[:2], 0.0])
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / L
    nrm = np.array([-u[1], u[0], 0.0])
    pts = [p0, p0 + u * 0.12 * L]
    seg = 0.76 * L / (2 * n)
    for i in range(2 * n):
        pts.append(p0 + u * (0.12 * L + seg * (i + 0.5)) + nrm * amp * (1 if i % 2 == 0 else -1))
    pts += [p0 + u * 0.88 * L, p1]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def coil_sym(p0, p1, n=4, r=0.11, color=C_IF, width=3):
    """สัญลักษณ์ขดลวด (ครึ่งวงกลมเรียงกัน) จาก p0 ไป p1"""
    p0, p1 = np.array([*p0[:2], 0.0]), np.array([*p1[:2], 0.0])
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / L
    ang = np.arctan2(u[1], u[0])
    lead = 0.14 * L
    pitch = (L - 2 * lead) / n
    g = VGroup(Line(p0, p0 + u * lead, color=color, stroke_width=width),
               Line(p1 - u * lead, p1, color=color, stroke_width=width))
    for i in range(n):
        a = Arc(radius=pitch / 2, start_angle=PI, angle=-PI, color=color, stroke_width=width)
        a.rotate(ang)
        a.move_to(p0 + u * (lead + pitch * (i + 0.5)) + np.array([-u[1], u[0], 0.0]) * pitch / 4, aligned_edge=ORIGIN)
        g.add(a)
    return g


def _p(p):
    return np.array([p[0], p[1], 0.0])


def meter(c, letter, color=WHITE, r=0.27):
    c = _p(c)
    ci = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color="#1c2a30", fill_opacity=0.9).move_to(c)
    t = Text(letter, font_size=22, color=color, weight=BOLD).move_to(c)
    return VGroup(ci, t)


def arm_sym(c, r=0.42, letter="E", color=C_E):
    """สัญลักษณ์อาร์เมเจอร์ (วงกลม + แปรงบน/ล่าง)"""
    c = _p(c)
    ci = Circle(radius=r, stroke_color=METAL, stroke_width=3, fill_color="#455A64", fill_opacity=0.95).move_to(c)
    t = MathTex(letter, font_size=36, color=color).move_to(c)
    b1 = Rectangle(width=0.16, height=0.1, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(c + UP * r)
    b2 = b1.copy().move_to(c + DOWN * r)
    return VGroup(ci, t, b1, b2)


def flow(path_mob, color, run=1.2, width=7):
    """แสงวิ่งตามเส้น = ทิศทางกระแส"""
    return ShowPassingFlash(path_mob.copy().set_stroke(color=color, width=width), time_width=0.45, run_time=run)


# ---------------------------------------------------------------- กระดานตัวอย่างคำนวณ
class Board:
    """แถวขั้นตอน: (วงกลมเลขขั้น + หัวข้อไทย) แล้วเนื้อ (MathTex/Text) เยื้องใต้หัวข้อ  วางไล่ลงมา"""

    def __init__(self, scene, x=-6.5, y=2.05, gap=0.22):
        self.sc, self.x, self.y, self.gap = scene, x, y, gap
        self.rows = []

    def add(self, num, head, body=None, color=OK, run=0.9, hold=0.4):
        badge = VGroup(Circle(radius=0.2, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.2),
                       Text(str(num), font_size=20, color=color))
        badge[1].move_to(badge[0])
        h = Text(head, font_size=23, color=color)
        top = VGroup(badge, h).arrange(RIGHT, buff=0.18)
        row = VGroup(top)
        if body is not None:
            body.next_to(top, DOWN, buff=0.1).align_to(top, LEFT).shift(RIGHT * 0.45)
            row.add(body)
        row.move_to([0, 0, 0])
        prev_bottom = self.rows[-1].get_bottom()[1] - self.gap if self.rows else self.y
        row.align_to([self.x, 0, 0], LEFT)
        row.shift(UP * (prev_bottom - row.get_top()[1]))
        self.rows.append(row)
        self.sc.mark("step")
        self.sc.play(FadeIn(top, shift=RIGHT * 0.25), run_time=0.5)
        if body is not None:
            self.sc.play(Write(body) if isinstance(body, MathTex) else FadeIn(body), run_time=run)
        if hold:
            self.sc.wait(hold)
        return row


def n_text(txt, size=26, color=WHITE):
    return Text(txt, font_size=size, color=color, line_spacing=0.9)


def num_axes(xmax, ymax, xt, yt, x_len=5.3, y_len=3.5, pos=ORIGIN, xl=r"I_f\ (A)", yl=r"E\ (V)", fs=17):
    """แกนที่มีเลขขีด (xt, yt = รายการค่าที่จะติดป้าย) วางให้จุดกำเนิดอยู่ที่ pos"""
    ax = Axes(x_range=[0, xmax, xmax], y_range=[0, ymax, ymax], x_length=x_len, y_length=y_len,
              axis_config={"color": GRAYTXT, "stroke_width": 2, "include_tip": True, "tip_length": 0.16,
                           "include_ticks": False, "tip_width": 0.14})
    pos = np.array([pos[0], pos[1], 0.0])
    ax.shift(pos - ax.c2p(0, 0))
    g = VGroup(ax)
    for v in xt:
        g.add(Line(ax.c2p(v, 0) + DOWN * 0.06, ax.c2p(v, 0) + UP * 0.06, color=GRAYTXT, stroke_width=2))
        g.add(Text(f"{v:g}", font_size=fs, color=GRAYTXT).next_to(ax.c2p(v, 0), DOWN, buff=0.1))
    for v in yt:
        g.add(Line(ax.c2p(0, v) + LEFT * 0.06, ax.c2p(0, v) + RIGHT * 0.06, color=GRAYTXT, stroke_width=2))
        g.add(Text(f"{v:g}", font_size=fs, color=GRAYTXT).next_to(ax.c2p(0, v), LEFT, buff=0.1))
    g.add(MathTex(xl, font_size=28, color=C_IF).move_to(ax.c2p(xmax, 0) + DOWN * 0.62 + LEFT * 0.15))
    g.add(MathTex(yl, font_size=28, color=C_E).next_to(ax.y_axis.get_end(), UP, buff=0.1))
    g.ax = ax
    return g


def poly(ax, xs, ys, color, width=4, dots=True, r=0.07):
    """เส้นตรงเชื่อมจุดข้อมูล (ตามตารางในโจทย์) + จุด"""
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
    g = VGroup(m)
    ds = VGroup(*[Dot(ax.c2p(x, y), radius=r, color=color) for x, y in zip(xs, ys)])
    if dots:
        g.add(ds)
    g.line, g.dots = m, ds
    return g


def band_path(ax, legs, color=EMF, width=4):
    """เส้นทางในแถบฮิสเตอรีซิส: legs=[(x,w),...] โดย w=0 อยู่บนเส้นขาขึ้น, w=1 อยู่บนเส้นขาลง"""
    pts = []
    for (x0, w0), (x1, w1) in zip(legs, legs[1:]):
        for t in np.linspace(0, 1, 26):
            xx = x0 + (x1 - x0) * t
            ww = w0 + (w1 - w0) * t
            pts.append(ax.c2p(xx, curve_up(xx) + ww * (curve_down(xx) - curve_up(xx))))
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def card(lines, w=3.2, color=GRAYTXT, size=21, fill=0.12):
    """กล่องข้อความหลายบรรทัด (Text) — lines = ["ข้อความ", ("ข้อความสี", สี), ...]"""
    rows = [Text(l[0], font_size=size, color=l[1]) if isinstance(l, tuple) else Text(l, font_size=size, color=WHITE)
            for l in lines]
    t = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    b = RoundedRectangle(width=max(w, t.width + 0.4), height=t.height + 0.35, corner_radius=0.12, stroke_color=color,
                         stroke_width=3, fill_color=color, fill_opacity=fill)
    t.move_to(b)
    return VGroup(b, t)


# ---------------------------------------------------------------- เคอร์ฟรุ่น S (ช่วงต้นโค้ง + ช่วงตรง + อิ่มตัว) ใช้กับ 8-4..8-7
_CC = dict(er=0.08, m=1.6, lam=0.08, x0=0.35, em=0.92, c=0.10)


def curve_c(x):
    """เคอร์ฟการเกิดอำนาจแม่เหล็กแบบรูป 8-5/8-6: เริ่มที่แรงเคลื่อนตกค้าง er ที่ If=0, ช่วงตรงสโลป m
    (เส้นความต้านทานวิกฤต = เส้นผ่านจุดกำเนิดสโลป m ทับช่วงตรง) แล้วค่อยๆ อิ่มตัว"""
    p = _CC
    x = np.asarray(x, float)
    base = p["m"] * x + p["er"] * np.exp(-x / p["lam"])
    e0 = p["m"] * p["x0"] + p["er"] * np.exp(-p["x0"] / p["lam"])
    me = p["m"] - (p["er"] / p["lam"]) * np.exp(-p["x0"] / p["lam"])
    d = p["em"] - e0
    sat = e0 + d * np.tanh(me * (x - p["x0"]) / d) + p["c"] * (x - p["x0"])
    out = np.where(x <= p["x0"], base, sat)
    return float(out) if out.ndim == 0 else out


def crit_cross(s, hi=1.45):
    """x ที่เส้นผ่านจุดกำเนิดสโลป s ตัดเคอร์ฟ curve_c (ตัดครั้งสุดท้าย = จุดทำงาน)"""
    xs = np.linspace(1e-4, hi, 6001)
    f = curve_c(xs) - s * xs
    idx = np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0]
    return float(xs[idx[-1]]) if len(idx) else float(xs[-1])


def stair_pts(ax, s, n=7):
    """จุดมุมของบันไดสร้างแรงเคลื่อน: (0,E1) -> (If1,E1) -> (If1,E2) -> (If2,E2) -> ...
    คืน (path_points, levels[E1..], currents[If1..])"""
    pts, Es, Is = [], [], []
    e = float(curve_c(0.0))
    pts.append(ax.c2p(0, e))
    for _ in range(n):
        i = e / s
        e2 = float(curve_c(i))
        pts += [ax.c2p(i, e), ax.c2p(i, e2)]
        Es.append(e)
        Is.append(i)
        e = e2
    Es.append(e)
    return pts, Es, Is
