"""epsx_lib — ตัวช่วยร่วมของคลิปข้อสอบเก่า EPSX (Q = ข้อสอบจริง, PR = ข้อฝึก Claude เขียนเอง)
ใช้ต่อจาก eps8_lib (Lesson/Board/glow ฯลฯ) กฎ: MathTex ห้ามมีภาษาไทย  สี: E แดง · If เขียว · Ia ทอง · IL ฟ้าเขียว · Is ม่วง
"""
from eps8_lib import *


def M(*t, color=WHITE, size=28):
    return MathTex(*t, font_size=size, color=color)


def T(txt, size=21, color=WHITE):
    return Text(txt, font_size=size, color=color, line_spacing=0.9)


class Solve(Lesson):
    """ฐานคลิปเฉลยข้อสอบ: rows() = กระดานเป็นขั้น ๆ, final() = การ์ดคำตอบ + จำแบบนี้ + เรียนที่ไหน"""

    def rows(self, spec, start=1, y=2.0, hold=1.2, gap=0.12, maxw=5.9):
        bd = Board(self, x=-6.6, y=y, gap=gap)
        out = []
        for k, (head, body, col) in enumerate(spec, start):
            if isinstance(body, (list, tuple)):
                body = VGroup(*body).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if body is not None:
                fit_width(body, maxw)
            out.append(bd.add(k, head, body, color=col, hold=hold))
        return bd, out

    def clear(self, bd, run=0.5):
        self.play(*[FadeOut(r) for r in bd.rows], run_time=run)

    def final(self, ans, remember, where, hold=4.0):
        self.fade_out_all(run_time=0.6)
        self._cap = None
        hd = Text("คำตอบ", font_size=24, color=YEL)
        am = VGroup(*ans).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fit_width(am, 10.6)
        box = RoundedRectangle(width=am.width + 0.7, height=am.height + 0.5, corner_radius=0.14, stroke_color=OK,
                               stroke_width=3, fill_color=OK, fill_opacity=0.08)
        am.move_to(box)
        rem = fit_width(Text("จำแบบนี้: " + remember, font_size=24, color=YEL, line_spacing=0.9), 11.8)
        wh = fit_width(Text("เรียนที่: " + where, font_size=20, color=GRAYTXT), 11.8)
        allg = VGroup(hd, VGroup(box, am), rem, wh).arrange(DOWN, buff=0.35).move_to([0, 0.1, 0])
        self.play(FadeIn(allg, shift=UP * 0.2), run_time=0.8)
        self.wait(hold)


# ------------------------------------------------------------------ วงจรเครื่องกำเนิดผสม (long / short shunt)
XSH, XA, XJ, XL = 0.35, 1.95, 4.25, 6.15
YT, YB, YM = 1.2, -2.1, -0.45


def cur(p0, p1, tex, color, where=UP, size=22, buff=0.06):
    a = Arrow([p0[0], p0[1], 0], [p1[0], p1[1], 0], buff=0, color=color, stroke_width=4, tip_length=0.15,
              max_tip_length_to_length_ratio=0.5)
    t = MathTex(tex, font_size=size, color=color).next_to(a, where, buff=buff)
    return VGroup(a, t)


def cg_fig(kind, rf_t, ra_t, rse_t, vt_t, load_t, ia_t="I_a", if_t="I_f", is_t="I_s", il_t="I_L", ls=20):
    """วงจรเครื่องกำเนิดผสม kind='long'|'short' ตามรูปข้อสอบ: ชันท์ซ้าย, อาร์เมเจอร์กลาง, เซรี่บน, โหลดขวา"""
    arm = arm_sym([XA, YM], r=0.42)
    w_a = wire((XA, YM + 0.45), (XA, YT), (XA + 0.2, YT))
    ser = coil_sym([XA + 0.2, YT], [XJ - 0.3, YT], n=4, r=0.1, color=C_IS)
    w_t = wire((XJ - 0.3, YT), (XL, YT), (XL, YM + 0.65))
    w_b = wire((XA, YM - 0.45), (XA, YB), (XL, YB))
    w_b2 = wire((XSH, YB), (XA, YB))
    w_l = wire((XL, YM - 0.65), (XL, YB))
    load = Rectangle(width=0.8, height=1.3, stroke_color=GRAYTXT, stroke_width=3, fill_color=GRAYTXT,
                     fill_opacity=0.15).move_to([XL, YM, 0])
    load_lab = MathTex(load_t, font_size=ls, color=WHITE).move_to(load)
    sh = res_zig([XSH, YT], [XSH, YB], n=6, color=C_IF)
    if kind == "long":
        sh_top = wire((XSH, YT), (XSH, 1.95), (XJ, 1.95), (XJ, YT), color=C_IF, width=4)
        dot = Dot([XJ, YT, 0], radius=0.08, color=C_IF)
    else:
        sh_top = wire((XSH, YT), (XA, YT), color=C_IF, width=4)
        dot = Dot([XA, YT, 0], radius=0.08, color=C_IF)
    dot2 = Dot([XA, YB, 0], radius=0.07, color=GRAYTXT)
    tp = Dot([XJ, YT, 0], radius=0.07, color=WHITE)
    tn = Dot([XJ, YB, 0], radius=0.07, color=WHITE)
    vt = cur([XJ + 0.28, YB + 0.15], [XJ + 0.28, YT - 0.15], vt_t, C_E, RIGHT, size=ls + 2)
    vt[1].move_to([XJ + 0.28 + 0.12 + vt[1].width / 2, YM - 0.9, 0])
    rf_l = MathTex(rf_t, font_size=ls - 2, color=C_IF).move_to([XSH + 0.18 + 0.6, -1.45, 0])
    ra_l = MathTex(ra_t, font_size=ls - 2, color=C_IA).next_to(arm, RIGHT, buff=0.12)
    rs_l = MathTex(rse_t, font_size=ls - 2, color=C_IS).move_to([(XA + XJ) / 2 + 0.1, 1.58, 0])
    ia = cur([XA + 0.3, 0.0], [XA + 0.3, 0.7], ia_t, C_IA, RIGHT)
    if_ = cur([XSH + 0.4, 0.85], [XSH + 0.4, 0.2], if_t, C_IF, RIGHT)
    is_ = cur([XA + 0.75, 0.82], [XA + 1.55, 0.82], is_t, C_IS, DOWN)
    il = cur([XJ + 0.5, YT + 0.35], [XJ + 1.3, YT + 0.35], il_t, C_IL, UP)
    g = VGroup(w_a, w_t, w_b, w_b2, w_l, load, load_lab, sh, sh_top, ser, arm, dot, dot2, tp, tn, vt, rf_l, ra_l, rs_l,
               ia, if_, is_, il)
    g.arm, g.ser, g.sh, g.sh_top, g.load = arm, ser, sh, sh_top, load
    g.ia, g.if_, g.is_, g.il, g.vt = ia, if_, is_, il, vt
    g.rf_l, g.ra_l, g.rs_l = rf_l, ra_l, rs_l
    return g


def pu_bar(y, frac, label_l, label_r, color, w=4.6, x0=1.2):
    """แถบ p.u.: เต็มความยาว = ฐาน (1.0 p.u.), หมุด = ค่าจริง/ฐาน"""
    base = Line([x0, y, 0], [x0 + w, y, 0], color=GRAYTXT, stroke_width=6)
    tick0 = Line([x0, y - 0.12, 0], [x0, y + 0.12, 0], color=GRAYTXT, stroke_width=3)
    tick1 = Line([x0 + w, y - 0.12, 0], [x0 + w, y + 0.12, 0], color=GRAYTXT, stroke_width=3)
    seg = Line([x0, y, 0], [x0 + w * frac, y, 0], color=color, stroke_width=10)
    pin = Dot([x0 + w * frac, y, 0], radius=0.11, color=color)
    return VGroup(base, tick0, tick1, seg, pin)
