"""eps11_lib — ตัวช่วยร่วมของคลิป EPS11 ชุด 2 (หน้า 1-39) ใช้คู่กับ eps8_lib.py / mlib.py
กฎ: MathTex ห้ามมีภาษาไทย  ตัวเลขต้องตรงกับ PDF บทที่ 11 (ตัวเลข "สมมติ" ต้องติดป้ายบอกชัด)
"""
from eps8_lib import *

_BaseLesson = Lesson


class Lesson(_BaseLesson):
    """Lesson ของชุดนี้: เวลารอยืดขึ้น (คลิปต้องอ่านตามทัน) และ say() ค้างให้อ่านอย่างน้อย 1.6 วิ"""
    SLOW = 1.5

    def wait(self, duration=1.0, **kw):
        super().wait(duration * self.SLOW, **kw)

    def say(self, txt, color=GRAYTXT, hold=0.0, size=23):
        super().say(txt, color=color, hold=max(hold, 1.6), size=size)


C_B = "#B388FF"   # ค่าฐาน (base)
C_A = "#FFD54F"   # ค่าจริง (actual)


def M(tex, color=WHITE, size=26):
    return MathTex(tex, font_size=size, color=color)


def T(txt, size=22, color=WHITE):
    return Text(txt, font_size=size * 1.12, color=color, line_spacing=0.9)


def ebox(cx, cy, tex, color=WHITE, w=0.95, h=0.44, size=22):
    """กล่องอิมพีแดนซ์ (สี่เหลี่ยม + ป้ายสูตรข้างใน)"""
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.10).move_to([cx, cy, 0])
    t = MathTex(tex, font_size=size, color=color).move_to(r)
    return VGroup(r, t)


def src(cx, cy, tex, color=YEL, r=0.27):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to([cx, cy, 0])
    s = MathTex(r"\sim", font_size=26, color=color).move_to(c)
    return VGroup(c, s)


def xf_ideal(cx, cy, h=1.2, color=WHITE):
    """สัญลักษณ์หม้อแปลงอุดมคติ: ขดซ้ายนูนซ้าย ขดขวานูนขวา + แกน 2 เส้น (ปลายขดบน/ล่าง อยู่ที่ x=cx-0.17 / cx+0.17)"""
    l = coil_sym((cx - 0.17, cy - h / 2), (cx - 0.17, cy + h / 2), n=4, r=0.11, color=color)
    r = coil_sym((cx + 0.17, cy + h / 2), (cx + 0.17, cy - h / 2), n=4, r=0.11, color=color)
    b1 = Line([cx - 0.035, cy - h / 2 + 0.05, 0], [cx - 0.035, cy + h / 2 - 0.05, 0], color=color, stroke_width=3)
    b2 = Line([cx + 0.035, cy - h / 2 + 0.05, 0], [cx + 0.035, cy + h / 2 - 0.05, 0], color=color, stroke_width=3)
    return VGroup(l, r, b1, b2)


def varrow(x, y0, y1, color, tex=None, side=LEFT, size=24):
    a = Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
    g = VGroup(a)
    if tex:
        g.add(MathTex(tex, font_size=size, color=color).next_to(a, side, buff=0.12))
    return g


def harrow(x0, x1, y, color, tex=None, up=True, size=22):
    a = Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
    g = VGroup(a)
    if tex:
        g.add(MathTex(tex, font_size=size, color=color).next_to(a, UP if up else DOWN, buff=0.1))
    return g


def vcoil(x, y_top, y_bot, color=C_IF, n=3):
    return coil_sym((x, y_top), (x, y_bot), n=n, r=0.11, color=color)


def remember(sc, line, sub="", hold=2.6):
    """การ์ดท้ายคลิป: จำแบบนี้ (1 บรรทัดหลัก + บรรทัดรอง)"""
    sc.fade_out_all(run_time=0.6)
    sc._cap = None
    h = Text("จำแบบนี้", font_size=28, color=YEL)
    t = fit_width(Text(line, font_size=32, color=WHITE, line_spacing=0.9), 12.2)
    g = VGroup(h, t)
    if sub:
        g.add(fit_width(Text(sub, font_size=22, color=OK, line_spacing=0.9), 12.2))
    g.arrange(DOWN, buff=0.45).move_to(ORIGIN)
    sc.play(FadeIn(g, shift=UP * 0.2), run_time=0.8)
    sc.wait(hold)


def core_pic(cx, cy, w=2.4, h=1.8, src_on=True, load_on=True):
    """แกนเหล็ก + ขดปฐมภูมิ(ซ้าย) ทุติยภูมิ(ขวา) + แหล่งจ่าย + โหลด คืน dict ของชิ้นส่วน"""
    core = Rectangle(width=w, height=h, stroke_color=METAL, stroke_width=20).move_to([cx, cy, 0])
    L, R = cx - w / 2, cx + w / 2
    c1 = Rectangle(width=0.7, height=1.0, stroke_color=C_R, stroke_width=3, fill_color=C_R, fill_opacity=0.35).move_to([L, cy, 0])
    c2 = Rectangle(width=0.7, height=1.0, stroke_color=C_S, stroke_width=3, fill_color=C_S, fill_opacity=0.35).move_to([R, cy, 0])
    flux = Rectangle(width=w, height=h, stroke_color=C_PHI, stroke_width=3).move_to([cx, cy, 0])
    fa = Arrow([cx - 0.5, cy + h / 2, 0], [cx + 0.5, cy + h / 2, 0], buff=0, color=C_PHI, stroke_width=4, tip_length=0.18)
    fl = MathTex(r"\phi", font_size=28, color=C_PHI).move_to([cx, cy + h / 2 - 0.35, 0])
    s = src(L - 1.6, cy, "", YEL)
    w1 = wire((L - 1.6, cy + 0.27), (L - 1.6, cy + 0.5), (L - 0.35, cy + 0.5))
    w2 = wire((L - 1.6, cy - 0.27), (L - 1.6, cy - 0.5), (L - 0.35, cy - 0.5))
    ld = Rectangle(width=0.6, height=0.8, stroke_color=OK, stroke_width=3, fill_color=OK, fill_opacity=0.12).move_to([R + 1.6, cy, 0])
    w3 = wire((R + 0.35, cy + 0.5), (R + 1.6, cy + 0.5), (R + 1.6, cy + 0.4))
    w4 = wire((R + 0.35, cy - 0.5), (R + 1.6, cy - 0.5), (R + 1.6, cy - 0.4))
    d = dict(core=core, c1=c1, c2=c2, flux=VGroup(flux, fa, fl), src=s, load=ld, wires=VGroup(w1, w2, w3, w4))
    d["all"] = VGroup(core, c1, c2, d["flux"], s, ld, d["wires"])
    return d
