"""eps10_lib — ตัวช่วยร่วมของคลิป EPS10 (บทที่ 10 หม้อแปลงไฟฟ้า, 52 หน้า) ใช้คู่กับ eps11_lib / eps8_lib / mlib
กฎ: MathTex ห้ามมีภาษาไทย ; ตัวเลขต้องตรงกับ PDF บทที่ 10 (ตัวเลขสมมติต้องติดป้าย "สมมติ")
สี: แรงดัน/แหล่งจ่าย = เหลือง YEL ; ฟลักซ์ = C_PHI ; ขดปฐมภูมิ = C_R (ส้ม) ; ขดทุติยภูมิ = C_S (ฟ้า) ; กระแส = C_IA
"""
from eps11_lib import *

_L11 = Lesson
C_P = C_R      # ขดปฐมภูมิ
C_SEC = C_S    # ขดทุติยภูมิ
C_LOSS = "#EF5350"
C_MAG = "#AB47BC"


class Lesson(_L11):
    def head(self, ttl, pg, size=28):
        """หัวเรื่อง + ป้ายหน้า: ถ้าหัวเรื่องยาวจนชนป้ายหน้า ให้เลื่อน/ย่อหัวเรื่องเข้าช่องว่างด้านซ้ายของป้าย"""
        self._ttl = title(ttl, size=size)
        self._ref = page_ref(pg)
        right = self._ref.get_left()[0] - 0.3
        if self._ttl.get_right()[0] > right:
            avail = right - (-6.9)
            if self._ttl.width > avail:
                self._ttl.scale_to_fit_width(avail)
            self._ttl.move_to([(-6.9 + right) / 2, self._ttl.get_center()[1], 0])
        self.play(FadeIn(self._ttl), FadeIn(self._ref), run_time=0.5)

    def newpage(self, pg):
        self.mark("page")
        new = page_ref(pg)
        gap = new.get_left()[0] - (self._ttl.get_right()[0] + 0.25)
        if gap < 0:
            new.scale_to_fit_width(max(new.width + gap, 1.0))
            new.move_to([X_MAX - new.width / 2 - 0.28, new.get_center()[1], 0])
        self.play(Transform(self._ref, new), run_time=0.4)

    def clear(self, run_time=0.6):
        """เก็บทุกอย่างบนเวที ยกเว้นหัวเรื่อง ป้ายหน้า"""
        keep = {id(self._ttl), id(self._ref)}
        mobs = [m for m in self.mobjects if id(m) not in keep]
        for m in mobs:
            m.clear_updaters()
        if mobs:
            self.play(FadeOut(Group(*mobs)), run_time=run_time)
        self._cap = None

    def keytext(self, txt, color=YEL, y=-3.05, size=24, hold=1.5):
        """ประโยคสำคัญของหน้า (ข้อความไทยล่างจอ)"""
        k = fit_width(Text(txt, font_size=size, color=color), 12.6).move_to([0, y, 0])
        bg = SurroundingRectangle(k, buff=0.12, color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6, corner_radius=0.08)
        g = VGroup(bg, k)
        self.play(FadeIn(g), run_time=0.5)
        self.wait(hold)
        return g


def xf_pic(cx, cy, s=1.0, n1="N_1", n2="N_2", show_src=True, show_load=True):
    """หม้อแปลงแกนเหล็ก (ขดซ้าย = ปฐมภูมิ, ขวา = ทุติยภูมิ) + แหล่งจ่าย + โหลด  คืน dict ชิ้นส่วน
    ขนาดรวมประมาณ 6.2s x 2.3s"""
    w, h = 2.4 * s, 1.8 * s
    core = Rectangle(width=w, height=h, stroke_color=METAL, stroke_width=18 * s).move_to([cx, cy, 0])
    L, R = cx - w / 2, cx + w / 2

    def coil(x, color, k=5):
        g = VGroup()
        for i in range(k):
            y = cy - 0.45 * s + i * 0.9 * s / (k - 1)
            g.add(Ellipse(width=0.62 * s, height=0.16 * s, stroke_color=color, stroke_width=4).move_to([x, y, 0]))
        return g
    c1, c2 = coil(L, C_P), coil(R, C_SEC)
    fl = Rectangle(width=w, height=h, stroke_color=C_PHI, stroke_width=3).move_to([cx, cy, 0])
    fa = Arrow([cx - 0.4 * s, cy + h / 2, 0], [cx + 0.4 * s, cy + h / 2, 0], buff=0, color=C_PHI, stroke_width=4, tip_length=0.16)
    fsym = MathTex(r"\phi_m", font_size=26, color=C_PHI).move_to([cx, cy + h / 2 - 0.32 * s, 0])
    l1 = MathTex(n1, font_size=26, color=C_P).move_to([L, cy - h / 2 - 0.4, 0])
    l2 = MathTex(n2, font_size=26, color=C_SEC).move_to([R, cy - h / 2 - 0.4, 0])
    d = dict(core=core, c1=c1, c2=c2, flux=VGroup(fl, fa, fsym), fline=fl, l1=l1, l2=l2)
    parts = [core, c1, c2, l1, l2]
    if show_src:
        sx = L - 1.45 * s
        sv = src(sx, cy, "", YEL, r=0.27 * s)
        w1 = wire((sx, cy + 0.27 * s), (sx, cy + 0.45 * s), (L - 0.31 * s, cy + 0.45 * s))
        w2 = wire((sx, cy - 0.27 * s), (sx, cy - 0.45 * s), (L - 0.31 * s, cy - 0.45 * s))
        d["src"] = sv
        d["w1"] = VGroup(w1, w2)
        parts += [sv, d["w1"]]
    if show_load:
        lx = R + 1.45 * s
        ld = Rectangle(width=0.5 * s, height=0.75 * s, stroke_color=OK, stroke_width=3, fill_color=OK, fill_opacity=0.12).move_to([lx, cy, 0])
        w3 = wire((R + 0.31 * s, cy + 0.45 * s), (lx, cy + 0.45 * s), (lx, cy + 0.375 * s))
        w4 = wire((R + 0.31 * s, cy - 0.45 * s), (lx, cy - 0.45 * s), (lx, cy - 0.375 * s))
        d["load"] = ld
        d["w2"] = VGroup(w3, w4)
        parts += [ld, d["w2"]]
    d["all"] = VGroup(*parts)
    return d


def flux_flow(sc, d, cycles=2, run=1.0):
    for _ in range(cycles):
        sc.play(flow(d["fline"], C_PHI, run=run, width=8), run_time=run)


def ind_sym(p0, p1, color=WHITE, n=3):
    return coil_sym(p0, p1, n=n, r=0.1, color=color, width=3)


NAMES = ["R_1", "jX_1", "jX_2'", "R_2'", "V_1", "V_2'", "jX_m", "R_c"]


def tee_circuit(x0=-5.6, y_top=0.9, y_bot=-1.1, color=WHITE, labels=True, size=24, mag=True, w=11.2, names=None):
    """วงจรสมมูล T (อ้างอิงปฐมภูมิ): R1 - jX1 - [jXm || Rm] - jX2' - R2'  คืน VGroup + dict ชิ้นส่วน"""
    x = lambda f: x0 + f * w
    yT, yB = y_top, y_bot
    parts = {}
    r1 = res_zig((x(0.07), yT), (x(0.19), yT), color=C_P)
    x1 = ind_sym((x(0.23), yT), (x(0.36), yT), color=C_P)
    x2 = ind_sym((x(0.64), yT), (x(0.77), yT), color=C_SEC)
    r2 = res_zig((x(0.81), yT), (x(0.93), yT), color=C_SEC)
    top = VGroup(wire((x(0), yT), (x(0.07), yT)), wire((x(0.19), yT), (x(0.23), yT)), wire((x(0.36), yT), (x(0.64), yT)),
                 wire((x(0.77), yT), (x(0.81), yT)), wire((x(0.93), yT), (x(1), yT)))
    bot = wire((x(0), yB), (x(1), yB))
    g = VGroup(top, bot, r1, x1, x2, r2)
    parts.update(r1=r1, x1=x1, x2=x2, r2=r2, top=top, bot=bot)
    if mag:
        mx1, mx2 = x(0.44), x(0.56)
        xm = ind_sym((mx1, yT - 0.35), (mx1, yB + 0.35), color=C_MAG)
        rm = res_zig((mx2, yT - 0.35), (mx2, yB + 0.35), color=C_LOSS)
        br = VGroup(wire((mx1, yT), (mx2, yT)), wire((mx1, yB), (mx2, yB)),
                    wire((mx1, yT), (mx1, yT - 0.35)), wire((mx1, yB + 0.35), (mx1, yB)),
                    wire((mx2, yT), (mx2, yT - 0.35)), wire((mx2, yB + 0.35), (mx2, yB)))
        g.add(xm, rm, br)
        parts.update(xm=xm, rm=rm, br=br)
    tl = VGroup(Dot([x(0), yT, 0], radius=0.05), Dot([x(0), yB, 0], radius=0.05),
                Dot([x(1), yT, 0], radius=0.05), Dot([x(1), yB, 0], radius=0.05))
    g.add(tl)
    if labels:
        nm = names or NAMES
        lab = VGroup(
            MathTex(nm[0], font_size=size, color=C_P).move_to([x(0.13), yT + 0.38, 0]),
            MathTex(nm[1], font_size=size, color=C_P).move_to([x(0.295), yT + 0.38, 0]),
            MathTex(nm[2], font_size=size, color=C_SEC).move_to([x(0.705), yT + 0.4, 0]),
            MathTex(nm[3], font_size=size, color=C_SEC).move_to([x(0.87), yT + 0.4, 0]),
            MathTex(nm[4], font_size=size + 2, color=YEL).move_to([x(0) - 0.35, (yT + yB) / 2, 0]),
            MathTex(nm[5], font_size=size + 2, color=OK).move_to([x(1) + 0.4, (yT + yB) / 2, 0]),
        )
        if mag:
            lab.add(MathTex(nm[6], font_size=size, color=C_MAG).next_to(parts["xm"], LEFT, buff=0.12),
                    MathTex(nm[7], font_size=size, color=C_LOSS).next_to(parts["rm"], RIGHT, buff=0.12))
        parts["lab"] = lab
        g.add(lab)
    g.parts = parts
    return g


def phasor_ix(origin, v_len, ic_len, im_len, color_v=YEL, size=24):
    """เฟสเซอร์ไม่มีโหลด: V แนวตั้ง, Ic ขนาน V, Im ตั้งฉาก (ล้าหลัง 90 องศา = ไปทางขวา ถ้า V ชี้ขึ้น)"""
    o = np.array([origin[0], origin[1], 0.0])
    v = Arrow(o, o + UP * v_len, buff=0, color=color_v, stroke_width=4, tip_length=0.18)
    ic = Arrow(o, o + UP * ic_len, buff=0, color=C_LOSS, stroke_width=5, tip_length=0.14, max_tip_length_to_length_ratio=0.5)
    im = Arrow(o + UP * ic_len, o + UP * ic_len + RIGHT * im_len, buff=0, color=C_MAG, stroke_width=4, tip_length=0.18)
    iphi = Arrow(o, o + UP * ic_len + RIGHT * im_len, buff=0, color=C_IA, stroke_width=4, tip_length=0.18)
    return v, ic, im, iphi
