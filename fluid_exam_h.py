"""Fluid Power Control exam clips, batch H (2026-11-10, exam 11 Nov).

FXH1_Cascade3      cascade, 3 groups: A+ B+ B- A- C+ C-     (W10 Pneumatic 03 p2-9)
FXH2_ShiftRegister stuck-signal trap + shift register A+ A- B+ B-  (W10 p10)
FXH3_RelayLatch    NO/NC, relay latch, single LS, on-delay timer   (W11 Pneumatic 04 p2,5,6,7)
FXH4_TwoCylLadder  ladder A+ B+ A- B-, A+ A- B+ B- trap, PLC I/O   (W11 p9,10,17)

Every number and name on screen comes from the lesson notes.
Layout: title + step tag + page_ref on top row, caption_top under it,
figure on the left stage, text rows in the right/lower panel.
"""
from mlib import *
import numpy as np

LIVE = "#42A5F5"
DEAD = "#546E7A"
SIG = WARN
YEL = "#FFD54F"
SUPC = "#90CAF9"


def T(s, size=24, color=WHITE):
    return Text(s, font_size=size, color=color)


def M(*parts, size=34, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def pipe(points, color=DEAD, width=3):
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [np.array([p[0], p[1], 0.0]) for p in points])


def cyl(xc, yc, name, col, w=1.6, rod_out=1.05):
    x0 = xc - w / 2
    barrel = Rectangle(width=w, height=0.5, color=col).move_to([xc, yc, 0])
    pist = Rectangle(width=0.12, height=0.46, stroke_width=0, fill_color=col,
                     fill_opacity=1).move_to([x0 + 0.2, yc, 0])
    rl = (xc + rod_out) - (x0 + 0.2)
    rod = Rectangle(width=rl, height=0.11, stroke_width=0, fill_color="#CFD8DC",
                    fill_opacity=1).move_to([x0 + 0.2 + rl / 2, yc, 0])
    nm = T(name, 24, col).move_to([xc - 0.25, yc + 0.47, 0])
    return barrel, VGroup(pist, rod), nm


def marker(x, y, name, col):
    tri = Triangle(color=col, fill_color=col, fill_opacity=1).scale(0.09).rotate(PI)
    tri.move_to([x, y + 0.26, 0])
    lb = T(name, 19, col).move_to([x, y + 0.5, 0])
    return VGroup(tri, lb)


def valve2(xc, yv, col):
    return VGroup(Square(0.5, color=col).move_to([xc - 0.25, yv, 0]),
                  Square(0.5, color=col).move_to([xc + 0.25, yv, 0]))


def feeds(xc, yv, yc, w=1.6):
    yb, yh = yc - 0.25, yc - 0.48
    return VGroup(
        pipe([(xc - 0.25, yv + 0.25), (xc - 0.25, yh), (xc - w / 2 + 0.08, yh),
              (xc - w / 2 + 0.08, yb)], METAL, 2),
        pipe([(xc + 0.25, yv + 0.25), (xc + 0.25, yh), (xc + w / 2 - 0.15, yh),
              (xc + w / 2 - 0.15, yb)], METAL, 2))


def shift_valve(v, side, col):
    on, off = (v[0], v[1]) if side == "L" else (v[1], v[0])
    return AnimationGroup(on.animate.set_fill(col, 0.45), off.animate.set_fill(col, 0.0))


def sbox(x, y, name, w=None, size=17):
    w = w or (0.5 if len(name) <= 2 else 0.12 * len(name) + 0.2)
    b = Rectangle(width=w, height=0.36, color=WHITE, fill_color=BLACK,
                  fill_opacity=1).move_to([x, y, 0])
    return VGroup(b, T(name, size, WHITE).move_to(b)).set_z_index(3)


class ExamScene(SafeScene):
    def head(self, ttl, ref):
        self.ref = page_ref(ref, size=18)
        self.ttl = fit_width(title(ttl, size=30), min(6.4, 2 * (self.ref.get_left()[0] - 0.3)))
        self.cap_m = None
        self.step_m = None
        self.play(FadeIn(self.ttl), FadeIn(self.ref))

    def step(self, n, name):
        m = T(f"ขั้น {n} · {name}", 22, OK)
        fit_width(m, (-self.ttl.width / 2 - 0.25) - (-6.81))
        m.move_to([-7.11 + 0.3 + m.width / 2, TITLE_Y, 0])
        if self.step_m is not None:
            self.play(FadeOut(self.step_m, run_time=0.3))
        self.play(FadeIn(m, shift=0.2 * RIGHT), run_time=0.5)
        self.step_m = m

    def cap(self, txt, color=GRAYTXT, wait=2.6):
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

    def rows(self, rows, x, y0, gap, max_w):
        for i, r in enumerate(rows):
            fit_width(r, max_w)
            r.move_to([x, y0 - i * gap, 0])
        return VGroup(*rows)

    def swap(self, old, new):
        if old is not None:
            self.play(FadeOut(old, run_time=0.35))
        self.play(FadeIn(new), run_time=0.5)
        return new

    def hit(self, mk, box, pipe_):
        self.play(Indicate(mk, color=WHITE, scale_factor=1.0),
                  Indicate(box, color=SIG, scale_factor=1.0),
                  pipe_.animate.set_color(SIG), run_time=0.9)


# ======================================================================
class FXH1_Cascade3(ExamScene):
    """3-group cascade A+ B+ / B- A- C+ / C-: 3 lines, 2 cascade valves."""

    def construct(self):
        self.head("Cascade 3 กรุ๊ป · 6 สเต็ป", "W10 · Pneumatic 03 หน้า 2-9")
        yc, yv = 1.5, 0.45
        YL = {1: -0.75, 2: -1.3, 3: -1.85}
        LC = {1: "#7986CB", 2: "#66BB6A", 3: "#BA68C8"}
        XC = {"A": -5.8, "B": -2.8, "C": 0.2}
        CC = {"A": "#4FC3F7", "B": "#FFB74D", "C": "#F06292"}
        cy, mk, vv, pl, figs = {}, {}, {}, {}, []
        for n in "ABC":
            xc, lo = XC[n], n.lower()
            b, m, nm = cyl(xc, yc, n, CC[n])
            cy[n] = m
            mk[lo + "0"] = marker(xc + 1.05, yc, lo + "0", CC[n])
            mk[lo + "1"] = marker(xc + 1.85, yc, lo + "1", CC[n])
            vv[n] = valve2(xc, yv, CC[n])
            pl[n + "+"] = T(n + "+", 18).move_to([xc - 0.68, yv + 0.29, 0])
            pl[n + "-"] = T(n + "−", 18).move_to([xc + 0.68, yv + 0.29, 0])
            figs += [b, m, nm, mk[lo + "0"], mk[lo + "1"], vv[n], feeds(xc, yv, yc),
                     pl[n + "+"], pl[n + "-"]]
        fig = VGroup(*figs)
        PX = 4.95

        # ---------------- 1 understand
        self.step(1, "เข้าใจโจทย์")
        self.play(FadeIn(fig), run_time=1.2)
        self.cap("กระบอกสูบ 3 ตัว A B C · ลิมิตวาล์ว a0 a1 b0 b1 c0 c1 อยู่ที่ปลายก้าน")
        seq = M("A+", "B+", "B-", "A-", "C+", "C-", size=40)
        seq.arrange(RIGHT, buff=0.34)
        fit_width(seq, 3.9)
        seq.move_to([PX, 1.85, 0])
        self.play(FadeIn(seq))
        self.cap("ต้องทำงาน 6 สเต็ปตามลำดับนี้ (Step Motion Diagram รูปที่ 227)")
        moves = [("A", 1), ("B", 1), ("B", -1), ("A", -1), ("C", 1), ("C", -1)]
        for i, (n, d) in enumerate(moves):
            self.play(cy[n].animate.shift(0.8 * d * RIGHT),
                      shift_valve(vv[n], "L" if d > 0 else "R", CC[n]),
                      Indicate(seq[i], color=YEL), run_time=0.9)
        self.cap("ปัญหา: ถ้าต่อลิมิตวาล์วสั่งตรงๆ จะมีสัญญาณลมค้างชนกัน → แก้ด้วยวงจรคาสเคด")

        # ---------------- 2 grouping
        self.step(2, "แบ่งกรุ๊ป + สูตร")
        rule = T("ตัวอักษรเดียวกัน ห้ามอยู่กรุ๊ปเดียวกัน", 21, YEL)
        self.rows([rule], PX, 0.6, 0.8, 3.9)
        self.play(FadeIn(rule))
        self.glow(rule)
        self.cap("วิธีตัด: ไล่จากซ้ายไปขวา เจอตัวอักษรซ้ำเมื่อไร ตัดกรุ๊ปตรงนั้น")
        cut1 = Line(UP * 0.28, DOWN * 0.28, color=WARN, stroke_width=5).move_to(
            (seq[1].get_right() + seq[2].get_left()) / 2)
        cut2 = Line(UP * 0.28, DOWN * 0.28, color=WARN, stroke_width=5).move_to(
            (seq[4].get_right() + seq[5].get_left()) / 2)
        self.play(Indicate(seq[1], color=WARN), Indicate(seq[2], color=WARN))
        self.play(Create(cut1))
        self.cap("A+ B+ แล้วเจอ B− (B ซ้ำ) → ตัด")
        self.play(Indicate(seq[4], color=WARN), Indicate(seq[5], color=WARN))
        self.play(Create(cut2))
        self.cap("B− A− C+ แล้วเจอ C− (C ซ้ำ) → ตัด · C− อยู่กรุ๊ป 3")
        grp_idx = {1: (0, 1), 2: (2, 4), 3: (5, 5)}
        braces = VGroup()
        for g, (i0, i1) in grp_idx.items():
            br = Brace(VGroup(*seq[i0:i1 + 1]), DOWN, buff=0.08, color=LC[g])
            lb = T(f"G{g}", 18, LC[g]).next_to(br, DOWN, buff=0.04)
            braces.add(VGroup(br, lb))
        self.play(FadeIn(braces))
        cnt1 = T("3 กรุ๊ป → เส้นลม 3 เส้น (L1 L2 L3)", 21)
        cnt2 = T("วาล์วคาสเคด = กรุ๊ป − 1 = 3 − 1 = 2 ตัว", 21)
        self.rows([cnt1, cnt2], PX, -0.15, 0.55, 3.9)
        self.play(FadeIn(cnt1))
        self.play(FadeIn(cnt2))
        self.cap("สูตร: จำนวนเส้นลม = จำนวนกรุ๊ป = 3 · วาล์วคาสเคด = กรุ๊ป − 1 = 2 ตัว", color=YEL)

        # ---------------- 3 build
        self.step(3, "วางวงจร")
        lines = {k: Line([-6.85, YL[k], 0], [2.3, YL[k], 0], color=DEAD, stroke_width=5)
                 for k in (1, 2, 3)}
        llb = {k: T(f"L{k}", 20, LC[k]).move_to([2.6, YL[k], 0]) for k in (1, 2, 3)}
        self.play(*[Create(l) for l in lines.values()], FadeIn(*llb.values()), run_time=1.0)
        self.glow(cnt1, VGroup(*lines.values()))
        cv2 = VGroup(Square(0.5, color=WHITE).move_to([-3.25, -2.5, 0]),
                     Square(0.5, color=WHITE).move_to([-2.75, -2.5, 0]))
        cv1 = VGroup(Square(0.5, color=WHITE).move_to([-0.25, -3.3, 0]),
                     Square(0.5, color=WHITE).move_to([0.25, -3.3, 0]))
        cv2_lb = T("CV2", 18).move_to([-1.6, -2.5, 0])
        cv1_lb = T("CV1", 18).move_to([-1.15, -3.64, 0])
        sup = Arrow([0, -3.97, 0], [0, -3.55, 0], buff=0, color=LIVE, stroke_width=4,
                    max_tip_length_to_length_ratio=0.35)
        sup_lb = T("ลมหลัก", 18, LIVE).move_to([0.95, -3.75, 0])
        o3 = pipe([(0.25, -3.05), (0.25, YL[3])], DEAD, 3)
        osup = pipe([(-0.25, -3.05), (-0.25, -2.95), (-3.0, -2.95), (-3.0, -2.75)], DEAD, 3)
        o1 = pipe([(-3.25, -2.25), (-3.25, YL[1])], DEAD, 3)
        o2 = pipe([(-2.75, -2.25), (-2.75, YL[2])], DEAD, 3)
        cdots = VGroup(*[Dot([x, y, 0], radius=0.06, color=WHITE)
                         for x, y in ((0.25, YL[3]), (-3.25, YL[1]), (-2.75, YL[2]))])
        self.play(FadeIn(cv1, cv2, cv1_lb, cv2_lb), GrowArrow(sup), FadeIn(sup_lb),
                  Create(o3), Create(osup), Create(o1), Create(o2), FadeIn(cdots), run_time=1.4)
        self.glow(cnt2, VGroup(cv1, cv2))
        self.cap("วาล์วคาสเคด 2 ตัวต่อเป็นลูกโซ่: CV1 เลือก L3 หรือส่งต่อให้ CV2 · CV2 เลือก L1 หรือ L2")

        def air(n):
            an = [lines[k].animate.set_color(LC[k] if k == n else DEAD) for k in (1, 2, 3)]
            an += [cv1[0].animate.set_fill(SUPC, 0.45 if n in (1, 2) else 0),
                   cv1[1].animate.set_fill(LC[3], 0.45 if n == 3 else 0)]
            if n == 1:
                an += [cv2[0].animate.set_fill(LC[1], 0.45), cv2[1].animate.set_fill(LC[2], 0)]
            elif n == 2:
                an += [cv2[0].animate.set_fill(LC[1], 0), cv2[1].animate.set_fill(LC[2], 0.45)]
            else:
                an += [cv2[0].animate.set_fill(METAL, 0.3), cv2[1].animate.set_fill(LC[2], 0)]
            an += [osup.animate.set_color(SUPC if n in (1, 2) else DEAD),
                   o1.animate.set_color(LC[1] if n == 1 else DEAD),
                   o2.animate.set_color(LC[2] if n == 2 else DEAD),
                   o3.animate.set_color(LC[3] if n == 3 else DEAD)]
            return an
        self.play(*air(3), run_time=1.0)
        self.cap("สภาวะเริ่มต้น: ลมหลักค้างอยู่ที่ L3 (เส้นสุดท้าย) · L1 L2 ไม่มีลม")

        rA1 = pipe([(-6.7, YL[1]), (-6.7, yv), (-6.3, yv)])
        rB2 = pipe([(-1.9, YL[2]), (-1.9, yv), (-2.3, yv)])
        rC3 = pipe([(1.1, YL[3]), (1.1, yv), (0.7, yv)])
        ddots = VGroup(*[Dot([x, y, 0], radius=0.06, color=WHITE)
                         for x, y in ((-6.7, YL[1]), (-1.9, YL[2]), (1.1, YL[3]))])
        self.play(Create(rA1), Create(rB2), Create(rC3), FadeIn(ddots), run_time=1.2)
        self.cap("กฎ 1: สเต็ปแรกของแต่ละกรุ๊ป ต่อตรงจากเส้นกรุ๊ปนั้น · L1→A+  L2→B−  L3→C−")
        s_a1 = sbox(-3.7, YL[1], "a1")
        r_a1 = pipe([(-3.7, YL[1] + 0.18), (-3.7, yv), (-3.3, yv)])
        s_b0 = sbox(-4.9, YL[2], "b0")
        r_b0 = pipe([(-4.9, YL[2] + 0.18), (-4.9, yv), (-5.3, yv)])
        s_a0 = sbox(-0.7, YL[2], "a0")
        r_a0 = pipe([(-0.7, YL[2] + 0.18), (-0.7, yv), (-0.3, yv)])
        self.play(Create(r_a1), Create(r_b0), Create(r_a0), FadeIn(s_a1, s_b0, s_a0), run_time=1.2)
        self.cap("กฎ 2: สเต็ปอื่นในกรุ๊ป ใช้ลิมิตวาล์วที่รับลมจากเส้นกรุ๊ปเดียวกัน · a1(L1)→B+  b0(L2)→A−  a0(L2)→C+")
        s_b1 = sbox(-2.25, YL[1], "b1")
        r_b1 = pipe([(-2.25, YL[1] - 0.18), (-2.25, -2.5), (-2.5, -2.5)])
        s_c1 = sbox(1.7, YL[2], "c1")
        r_c1 = pipe([(1.7, YL[2] - 0.18), (1.7, -3.3), (0.5, -3.3)])
        self.play(Create(r_b1), Create(r_c1), FadeIn(s_b1, s_c1), run_time=1.2)
        self.cap("กฎ 3: ลิมิตวาล์วตัวสุดท้ายของกรุ๊ป ไปสั่งวาล์วคาสเคดให้เปลี่ยนเส้น · b1→CV2  c1→CV1")
        s_st = sbox(-4.75, YL[3], "START")
        r_st = pipe([(-4.75, YL[3] - 0.18), (-4.75, -3.3), (-0.5, -3.3)])
        r_rs = pipe([(-3.95, YL[3]), (-3.95, -2.5), (-3.5, -2.5)])
        rdot = Dot([-3.95, YL[3], 0], radius=0.06, color=WHITE)
        self.play(Create(r_st), FadeIn(s_st), Create(r_rs), FadeIn(rdot), run_time=1.2)
        self.cap("ปุ่ม START รับลมจาก L3 ไปสั่ง CV1 · ลม L3 ดัน CV2 กลับตำแหน่ง L1 รอไว้")

        # ---------------- 4 step-through
        self.step(4, "เดินทีละสเต็ป")
        self.play(FadeOut(rule, run_time=0.35))
        self.play(FadeOut(cnt1, cnt2, run_time=0.35))
        self.st = T("ลมอยู่ที่: L3", 23, LC[3]).move_to([PX, 0.8, 0])
        self.play(FadeIn(self.st))
        tbl = VGroup(*[T(s, 21, WHITE) for s in (
            "1) START → CV1 → L1 มีลม → A+",
            "2) a1 (จาก L1) → B+",
            "3) b1 → CV2 → L2 มีลม → B−",
            "4) b0 (จาก L2) → A−",
            "5) a0 (จาก L2) → C+",
            "6) c1 → CV1 → L3 มีลม → C−",
            "จบ: L3 ค้าง รอ START รอบใหม่")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        fit_width(tbl, 3.95)
        tbl.move_to([PX, -1.45, 0])

        def say(n):
            new = T(f"ลมอยู่ที่: L{n}", 23, LC[n]).move_to([PX, 0.8, 0])
            self.play(FadeOut(self.st, run_time=0.3))
            self.play(FadeIn(new, run_time=0.4))
            self.st = new

        def move(n, d):
            self.play(shift_valve(vv[n], "L" if d > 0 else "R", CC[n]),
                      cy[n].animate.shift(0.8 * d * RIGHT), run_time=1.3)

        # 1
        self.play(FadeIn(tbl[0]))
        self.play(r_st.animate.set_color(SIG), Indicate(s_st, color=SIG, scale_factor=1.0))
        self.play(*air(1), r_st.animate.set_color(DEAD), run_time=1.0)
        say(1)
        self.cap("กด START → CV1 สลับ → ลมหลักผ่าน CV2 ไปเข้า L1", wait=1.8)
        self.play(rA1.animate.set_color(SIG), Indicate(pl["A+"], color=SIG))
        move("A", 1)
        self.cap("L1 ต่อตรงเข้า A+ → A ยืดออก")
        # 2
        self.play(FadeIn(tbl[1]))
        self.hit(mk["a1"], s_a1, r_a1)
        move("B", 1)
        self.cap("A ชน a1 → a1 รับลมจาก L1 ส่งไป B+ → B ยืดออก (ยังอยู่กรุ๊ป 1)")
        # 3
        self.play(FadeIn(tbl[2]))
        self.hit(mk["b1"], s_b1, r_b1)
        self.cap("B ชน b1 · สเต็ปถัดไป B− อยู่คนละกรุ๊ป → b1 ไปสั่ง CV2 ไม่สั่ง B− ตรงๆ", wait=2.2)
        self.play(*air(2), rA1.animate.set_color(DEAD), r_a1.animate.set_color(DEAD),
                  r_b1.animate.set_color(DEAD), run_time=1.2)
        say(2)
        self.glow(pl["B+"], r_a1, WARN)
        self.cap("กับดักสัญญาณค้าง: a1 ยังถูกกดอยู่ แต่ L1 หมดลมแล้ว → สาย B+ ไม่มีลมค้าง", color=OK)
        self.play(rB2.animate.set_color(SIG), Indicate(pl["B-"], color=SIG))
        move("B", -1)
        self.cap("L2 ต่อตรงเข้า B− → B หดกลับได้ทันที ไม่มีลมต้านอีกฝั่ง")
        # 4
        self.play(FadeIn(tbl[3]))
        self.hit(mk["b0"], s_b0, r_b0)
        move("A", -1)
        self.cap("B ชน b0 → b0 รับลมจาก L2 ส่งไป A− → A หดกลับ")
        # 5
        self.play(FadeIn(tbl[4]))
        self.hit(mk["a0"], s_a0, r_a0)
        move("C", 1)
        self.cap("A ชน a0 → a0 รับลมจาก L2 ส่งไป C+ → C ยืดออก")
        # 6
        self.play(FadeIn(tbl[5]))
        self.hit(mk["c1"], s_c1, r_c1)
        self.cap("C ชน c1 · C− อยู่กรุ๊ป 3 → c1 ไปสั่ง CV1 สลับกลับ", wait=1.8)
        self.play(*air(3), rB2.animate.set_color(DEAD), r_b0.animate.set_color(DEAD),
                  r_a0.animate.set_color(DEAD), r_c1.animate.set_color(DEAD), run_time=1.2)
        say(3)
        self.glow(pl["C+"], r_a0, WARN)
        self.cap("a0 ยังถูกกดอยู่ (A อยู่บ้าน) แต่ L2 หมดลมแล้ว → สาย C+ ไม่ค้าง", color=OK)
        self.play(rC3.animate.set_color(SIG), r_rs.animate.set_color(SIG),
                  Indicate(pl["C-"], color=SIG))
        move("C", -1)
        self.cap("L3 ต่อตรงเข้า C− → C หดกลับ · ลม L3 ดัน CV2 กลับตำแหน่งเริ่มด้วย")
        self.play(FadeIn(tbl[6]))
        self.cap("ครบรอบ: L3 ค้างลมไว้ รอกด START รอบใหม่")

        # ---------------- 5 check
        self.step(5, "ตรวจ")
        self.glow(tbl[2], s_b1, OK)
        self.glow(tbl[5], s_c1, OK)
        self.cap("ตรวจ: ทุกขณะมีลมแค่เส้นเดียว · เปลี่ยนกรุ๊ป = ตัดลมกรุ๊ปเก่า → ไม่มีสัญญาณค้าง",
                 color=OK, wait=3.2)
        self.cap("สูตรสอบ: เส้นลม = จำนวนกรุ๊ป = 3 · วาล์วคาสเคด = กรุ๊ป − 1 = 2 ตัว",
                 color=YEL, wait=4.0)
        self.wait(1.0)


# ======================================================================
class FXH2_ShiftRegister(ExamScene):
    """A+ A- B+ B-: direct wiring sticks at B-, shift register fixes it."""

    def construct(self):
        self.head("กับดักสัญญาณค้าง + Shift Register", "W10 · Pneumatic 03 หน้า 2, 10")
        yc, yv, ym = 1.5, 0.45, -1.4
        XC = {"A": -5.4, "B": -2.0}
        CC = {"A": "#4FC3F7", "B": "#FFB74D"}
        cy, mk, vv, pl, figs = {}, {}, {}, {}, []
        for n in "AB":
            xc, lo = XC[n], n.lower()
            b, m, nm = cyl(xc, yc, n, CC[n])
            cy[n] = m
            mk[lo + "0"] = marker(xc + 1.05, yc, lo + "0", CC[n])
            mk[lo + "1"] = marker(xc + 1.85, yc, lo + "1", CC[n])
            vv[n] = valve2(xc, yv, CC[n])
            pl[n + "+"] = T(n + "+", 18).move_to([xc - 0.68, yv + 0.29, 0])
            pl[n + "-"] = T(n + "−", 18).move_to([xc + 0.68, yv + 0.29, 0])
            figs += [b, m, nm, mk[lo + "0"], mk[lo + "1"], vv[n], feeds(xc, yv, yc),
                     pl[n + "+"], pl[n + "-"]]
        for n in "AB":
            vv[n][1].set_fill(CC[n], 0.45)
        fig = VGroup(*figs)
        PX = 4.7
        MX = [-6.3, -4.5, -2.9, -1.1]
        VS = [-5.9, -4.9, -2.5, -1.5]
        PIL = ["A+", "A-", "B+", "B-"]
        LIM = ["START·b0", "a1", "a0", "b1"]
        MKN = [None, "a1", "a0", "b1"]
        outs = [pipe([(MX[i], ym + 0.4), (MX[i], yv), (VS[i], yv)]) for i in range(4)]
        boxes = [sbox(MX[i], ym + 0.22, LIM[i], size=16) for i in range(4)]

        def move(n, d):
            self.play(shift_valve(vv[n], "L" if d > 0 else "R", CC[n]),
                      cy[n].animate.shift(0.8 * d * RIGHT), run_time=1.3)

        # ---------------- 1 the trap
        self.step(1, "เข้าใจโจทย์ + กับดัก")
        self.play(FadeIn(fig), run_time=1.2)
        seq = M("A+", "A-", "B+", "B-", size=42).arrange(RIGHT, buff=0.4)
        fit_width(seq, 3.8)
        seq.move_to([PX, 1.85, 0])
        self.play(FadeIn(seq))
        self.cap("ลำดับตัวอย่างหน้า 10: A+ A− B+ B− · ลองต่อลิมิตวาล์วสั่งตรงๆ ก่อน")
        self.play(*[Create(o) for o in outs], *[FadeIn(b) for b in boxes], run_time=1.4)
        drows = VGroup(*[T(s, 22) for s in ("START → A+", "a1 → A−", "a0 → B+", "b1 → B−")])
        drows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([PX, 0.3, 0])
        self.play(FadeIn(drows))
        self.cap("ต่อตรง: ลิมิตวาล์วของสเต็ปก่อน สั่งสเต็ปถัดไปทันที")
        self.play(Indicate(boxes[0], color=SIG, scale_factor=1.0), outs[0].animate.set_color(SIG))
        move("A", 1)
        self.play(outs[0].animate.set_color(DEAD))
        self.cap("กด START → A+ (ปล่อยปุ่มแล้ว สาย A+ หมดลม)", wait=1.8)
        self.hit(mk["a1"], boxes[1], outs[1])
        move("A", -1)
        self.play(outs[1].animate.set_color(DEAD))
        self.cap("A ชน a1 → A− → A หดกลับ (ออกจาก a1 แล้ว สาย A− หมดลม)", wait=1.8)
        self.hit(mk["a0"], boxes[2], outs[2])
        move("B", 1)
        self.cap("A กลับมาชน a0 → B+ → B ยืดออก · แต่ a0 ยังถูกกดค้างอยู่!", color=WARN)
        self.hit(mk["b1"], boxes[3], outs[3])
        bang = T("ลมชน 2 ฝั่ง!", 22, WARN).move_to([-2.0, -0.35, 0])
        self.play(FadeIn(bang), Indicate(vv["B"], color=WARN, scale_factor=1.0),
                  Indicate(outs[2], color=WARN, scale_factor=1.0))
        self.cap("b1 สั่ง B− แต่สาย B+ ยังมีลมจาก a0 → วาล์ว B ไม่ขยับ = สัญญาณค้าง (Signal Overlap)",
                 color=WARN, wait=3.2)
        trap = T("a0 กดค้างตลอดที่ B ทำงาน → B+ ค้าง", 21, WARN)
        self.rows([trap], PX, -1.05, 0.6, 4.2)
        self.play(FadeIn(trap))
        self.glow(trap, mk["a0"], WARN)

        # ---------------- 2 two fixes
        self.step(2, "ทางแก้ 2 แบบ")
        self.play(FadeOut(bang, run_time=0.35))
        self.play(outs[2].animate.set_color(DEAD), outs[3].animate.set_color(DEAD), run_time=0.5)
        move("B", -1)
        self.play(FadeOut(drows, run_time=0.35))
        self.play(FadeOut(trap, run_time=0.35))
        fx = VGroup(T("แก้ 1: Cascade", 22, YEL),
                    M(r"A+\ |\ A-\ B+\ |\ B-", size=34),
                    T("3 กรุ๊ป → 3 เส้น, วาล์วคาสเคด 3−1 = 2 ตัว", 20),
                    T("แก้ 2: Shift Register", 22, YEL),
                    T("1 สเต็ป = 1 โมดูล → 4 โมดูล", 20))
        self.rows(list(fx), PX, 1.05, 0.6, 4.2)
        self.play(FadeIn(fx[0]), FadeIn(fx[1]))
        self.cap("Cascade: ตัดกรุ๊ปตามกฎตัวอักษรซ้ำ → A+ | A− B+ | B− = 3 กรุ๊ป")
        self.play(FadeIn(fx[2]))
        self.wait(1.5)
        self.play(FadeIn(fx[3]), FadeIn(fx[4]))
        self.cap("Shift Register: ไม่ต้องแบ่งกรุ๊ป · ทุกสเต็ปมีโมดูลประจำของตัวเอง")

        # ---------------- 3 module
        self.step(3, "โมดูลทำงานยังไง")
        self.play(*[b.animate.move_to([MX[i], -2.75, 0]) for i, b in enumerate(boxes)], run_time=1.0)
        mods = VGroup(*[VGroup(Rectangle(width=0.9, height=0.8, color=WHITE),
                               T(f"M{i + 1}", 22).move_to([MX[i], ym, 0])).move_to([MX[i], ym, 0])
                        for i in range(4)])
        ins = VGroup(*[Arrow([MX[i], -2.57, 0], [MX[i], ym - 0.4, 0], buff=0, color=METAL,
                             stroke_width=3, max_tip_length_to_length_ratio=0.25) for i in range(4)])
        arms = VGroup(*[Arrow([MX[i] + 0.45, ym + 0.18, 0], [MX[i + 1] - 0.45, ym + 0.18, 0],
                              buff=0, color=DEAD, stroke_width=3,
                              max_tip_length_to_length_ratio=0.3) for i in range(3)])
        rsts = VGroup(*[Arrow([MX[i + 1] - 0.45, ym - 0.18, 0], [MX[i] + 0.45, ym - 0.18, 0],
                              buff=0, color=DEAD, stroke_width=3,
                              max_tip_length_to_length_ratio=0.3) for i in range(3)])
        self.play(FadeIn(mods), GrowFromEdge(ins, DOWN), run_time=1.2)
        self.play(*[GrowArrow(a) for a in arms], *[GrowArrow(r) for r in rsts], run_time=1.0)
        self.play(FadeOut(fx, run_time=0.35))
        mr = VGroup(T("โมดูล = หน่วยจำ (Bistable 3/2) + AND", 21, YEL),
                    T("set: โมดูลก่อนเปิดทาง AND ลิมิตวาล์ว", 20, OK),
                    T("ออก: สั่งลูกสูบ + เปิดทางโมดูลถัดไป", 20, OK),
                    T("reset: โมดูลถัดไปทำงาน → ตัดโมดูลก่อน", 20, WARN))
        self.rows(list(mr), PX, 1.0, 0.62, 4.2)
        for i, r in enumerate(mr):
            self.play(FadeIn(r), run_time=0.5)
            if i == 1:
                self.glow(r, VGroup(arms[0], ins[1]), OK)
            elif i == 3:
                self.glow(r, rsts[0], WARN)
        self.cap("ลูกศรบน = เปิดทาง (arm) ไปโมดูลถัดไป · ลูกศรล่าง = reset ย้อนกลับไปตัดโมดูลก่อน", wait=3.0)

        # ---------------- 4 step-through
        self.step(4, "เดินทีละสเต็ป")
        self.play(FadeOut(mr, run_time=0.35))
        tbl = VGroup(*[T(s, 21) for s in (
            "1) START·b0 → M1 → A+",
            "2) a1·M1 → M2 → A− · reset M1",
            "3) a0·M2 → M3 → B+ · reset M2",
            "4) b1·M3 → M4 → B− · reset M3",
            "จบ: b0 = B กลับบ้าน รอ START")]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        fit_width(tbl, 4.2)
        tbl.move_to([PX, 0.2, 0])
        MC = [CC["A"], CC["A"], CC["B"], CC["B"]]

        def set_mod(i, prev=None):
            an = [mods[i][0].animate.set_fill(MC[i], 0.45), outs[i].animate.set_color(SIG)]
            if i < 3:
                an.append(arms[i].animate.set_color(OK))
            if prev is not None:
                an += [mods[prev][0].animate.set_fill(MC[prev], 0),
                       outs[prev].animate.set_color(DEAD),
                       rsts[prev].animate.set_color(WARN), arms[prev].animate.set_color(DEAD)]
            return an

        self.play(FadeIn(tbl[0]))
        self.play(Indicate(boxes[0], color=SIG, scale_factor=1.0), ins[0].animate.set_color(SIG))
        self.play(*set_mod(0), ins[0].animate.set_color(METAL), run_time=1.0)
        move("A", 1)
        self.cap("START (และ b0 ยืนยันว่า B อยู่บ้าน) → M1 จำไว้ → สั่ง A+ และเปิดทางให้ M2")
        self.play(FadeIn(tbl[1]))
        self.hit(mk["a1"], boxes[1], ins[1])
        self.play(*set_mod(1, 0), ins[1].animate.set_color(METAL), run_time=1.0)
        move("A", -1)
        self.cap("a1 AND M1 → M2 ทำงาน → A− · พร้อม reset M1 → สาย A+ หมดลม")
        self.play(FadeIn(tbl[2]))
        self.play(rsts[0].animate.set_color(DEAD))
        self.hit(mk["a0"], boxes[2], ins[2])
        self.play(*set_mod(2, 1), ins[2].animate.set_color(METAL), run_time=1.0)
        move("B", 1)
        self.cap("a0 AND M2 → M3 → B+ · reset M2")
        self.play(FadeIn(tbl[3]))
        self.play(rsts[1].animate.set_color(DEAD))
        self.hit(mk["b1"], boxes[3], ins[3])
        self.play(*set_mod(3, 2), ins[3].animate.set_color(METAL), run_time=1.0)
        self.glow(pl["B+"], outs[2], OK)
        self.cap("จุดที่ต่อตรงแล้วค้าง: a0 ยังกดอยู่ แต่ B+ มาจาก M3 ซึ่งถูก M4 reset แล้ว → ไม่มีลมค้าง",
                 color=OK, wait=3.0)
        move("B", -1)
        self.cap("M4 → B− → B หดกลับได้")
        self.play(FadeIn(tbl[4]), rsts[2].animate.set_color(DEAD))
        self.cap("b0 ถูกกด = พร้อมเริ่มรอบใหม่ · M4 ค้างไว้จน M1 ของรอบใหม่ reset")

        # ---------------- 5 check
        self.step(5, "ตรวจ + สรุป")
        self.play(FadeOut(tbl, run_time=0.35))
        sm = VGroup(T("ทุกขณะ มีโมดูลทำงานแค่ตัวเดียว", 21, OK),
                    T("สเต็ปเยอะ = แค่เพิ่มโมดูล ไม่ต้องคิดกรุ๊ป", 20),
                    T("หาจุดเสียง่าย: ไฟลมโชว์ทีละสเต็ป", 20),
                    T("START ผ่าน Shuttle (OR) เลือก Manual/Auto", 20),
                    T("+ Interlock b0 ยืนยันว่าอยู่จุดเริ่ม", 20))
        self.rows(list(sm), PX, 1.0, 0.6, 4.2)
        self.play(FadeIn(sm[0]))
        self.glow(sm[0], mods, OK)
        self.play(FadeIn(sm[1]), FadeIn(sm[2]))
        self.cap("ข้อดีเหนือ Cascade (ตามชีท): ออกแบบง่ายเมื่อสเต็ปเยอะ + Troubleshoot ง่าย", color=YEL)
        self.play(FadeIn(sm[3]), FadeIn(sm[4]))
        self.cap("สรุป: สัญญาณค้างเกิดเมื่อลิมิตวาล์วยังถูกกดค้าง → ต้องมีตัวตัดลม (กรุ๊ป หรือ โมดูล)",
                 color=YEL, wait=4.0)
        self.wait(1.0)


# ======================================================================
# ladder helpers
XL, XR = -6.6, -0.9


def wire(points, color=DEAD):
    return pipe(points, color, 3)


def contact(x, y, name, nc=False, lab_up=True, size=17):
    p = VGroup(Line([x - 0.12, y - 0.2, 0], [x - 0.12, y + 0.2, 0], stroke_width=4, color=WHITE),
               Line([x + 0.12, y - 0.2, 0], [x + 0.12, y + 0.2, 0], stroke_width=4, color=WHITE))
    bridge = Line([x - 0.12, y, 0], [x + 0.12, y, 0], stroke_width=5, color=WHITE)
    bridge.set_stroke(opacity=1.0 if nc else 0.0)
    slash = Line([x - 0.2, y - 0.2, 0], [x + 0.2, y + 0.2, 0], stroke_width=3, color=WHITE)
    lb = T(name, size, GRAYTXT).move_to([x, y + (0.42 if lab_up else -0.42), 0])
    g = VGroup(p, slash, lb) if nc else VGroup(p, lb)
    return g, bridge


def coil(x, y, name, size=17, inside=False):
    c = Circle(radius=0.25, color=WHITE, stroke_width=3).move_to([x, y, 0])
    lb = T(name, size, GRAYTXT).move_to([x, y, 0] if inside else [x, y + 0.45, 0])
    return c, lb


def bridge_on(b, on=True):
    return b.animate.set_stroke(opacity=1.0 if on else 0.0)


def paint(objs, on):
    return [o.animate.set_color(CURRENT if on else DEAD) for o in objs]


class FXH3_RelayLatch(ExamScene):
    """NO/NC, relay latch, single limit switch return, on-delay timer."""

    def construct(self):
        self.head("รีเลย์ + วงจรแลตช์ + ลิมิตสวิตช์", "W11 · Pneumatic 04 หน้า 2, 5, 6, 7")
        PX, PW = 3.25, 6.8
        y1, yb, y2, y3 = 1.25, 0.5, -0.6, -1.9

        # ---------------- 1 parts
        self.step(1, "อุปกรณ์")
        no_s, _ = contact(0, 0, "NO")
        nc_s, nc_b = contact(0, 0, "NC", nc=True)
        co_s = Circle(radius=0.25, color=WHITE, stroke_width=3)
        leg = VGroup()
        for sym, txt in ((VGroup(no_s[0]), "NO ปกติเปิด: กดแล้วต่อ ปล่อยแล้วดับ → ปุ่ม START"),
                         (VGroup(nc_s[0], nc_s[1], nc_b), "NC ปกติปิด: กดแล้วตัด → ปุ่ม STOP"),
                         (co_s, "คอยล์รีเลย์ 1CR: ได้ไฟ → หน้าสัมผัส 1CR-x ทุกตัวสลับพร้อมกัน")):
            t = T(txt, 21)
            fit_width(t, 5.6)
            leg.add(VGroup(sym.copy(), t).arrange(RIGHT, buff=0.35))
        leg.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, 0.2, 0])
        for i, r in enumerate(leg):
            self.play(FadeIn(r), run_time=0.6)
            self.cap(["หน้าสัมผัส NO (Normally Open) · ใช้เป็นปุ่ม START",
                      "หน้าสัมผัส NC (Normally Closed) มีขีดเฉียง · ใช้เป็นปุ่ม STOP",
                      "รีเลย์ = คอยล์ + แกนเหล็ก + สปริง + หน้าสัมผัส NO/NC (ชื่อเดียวกับคอยล์)"][i],
                     wait=2.4)
        self.cap("ลิมิตสวิตช์ (LS) ก็มีหน้าสัมผัส NO/NC · ก้านลูกกลิ้งถูกแคมที่ก้านสูบกดเมื่อถึงตำแหน่ง")
        self.play(FadeOut(leg, run_time=0.4))

        # ---------------- 2 latch
        self.step(2, "วงจรแลตช์ (จำสภาวะ)")
        rails = VGroup(Line([XL, 1.85, 0], [XL, -2.6, 0], color=WHITE, stroke_width=4),
                       Line([XR, 1.85, 0], [XR, -2.6, 0], color=WHITE, stroke_width=4))
        rl = VGroup(T("+24V", 18, CURRENT).move_to([XL, 2.07, 0]),
                    T("0V", 18, GRAYTXT).move_to([XR, 2.07, 0]))
        stop, b_stop = contact(-5.8, y1, "STOP", nc=True)
        start, b_start = contact(-4.5, y1, "START")
        cr1c, cr1l = coil(-1.75, y1, "1CR")
        w1 = wire([(XL, y1), (-5.92, y1)])
        w2 = wire([(-5.68, y1), (-5.15, y1)])
        w3 = wire([(-5.15, y1), (-4.62, y1)])
        w4 = wire([(-4.38, y1), (-3.85, y1)])
        w5 = wire([(-3.85, y1), (-3.32, y1)])
        jmp = wire([(-3.32, y1), (-3.08, y1)])
        w6 = wire([(-3.08, y1), (-2.0, y1)])
        w7 = wire([(-1.5, y1), (XR, y1)])
        self.play(Create(rails), FadeIn(rl), run_time=0.8)
        self.play(FadeIn(stop, b_stop, start, b_start, cr1c, cr1l),
                  Create(VGroup(w1, w2, w3, w4, w5, jmp, w6, w7)), run_time=1.2)
        self.cap("แลดเดอร์: ไฟไหลจากราง +24V ผ่านหน้าสัมผัสไปคอยล์ แล้วลงราง 0V")
        r1_start = [w1, w2, w3, w4, w5, jmp, w6, w7]
        self.play(bridge_on(b_start), *paint(r1_start, True), cr1c.animate.set_fill(CURRENT, 0.6))
        self.cap("กด START → ไฟครบวง → คอยล์ 1CR ทำงาน", wait=1.8)
        self.play(bridge_on(b_start, False), *paint(r1_start, False), cr1c.animate.set_fill(CURRENT, 0))
        self.cap("ปล่อยมือ → ดับทันที เพราะปุ่มกดเป็นแบบกดติดปล่อยดับ (Momentary)", color=WARN)
        br1 = wire([(-5.15, y1), (-5.15, yb), (-4.62, yb)])
        br2 = wire([(-4.38, yb), (-3.85, yb), (-3.85, y1)])
        hold, b_hold = contact(-4.5, yb, "1CR-1", lab_up=False)
        nd = VGroup(Dot([-5.15, y1, 0], radius=0.06), Dot([-3.85, y1, 0], radius=0.06))
        self.play(Create(br1), Create(br2), FadeIn(hold, b_hold, nd), run_time=1.0)
        self.cap("แก้: ต่อหน้าสัมผัส NO ของรีเลย์ (1CR-1) ขนานกับปุ่ม START")
        self.play(bridge_on(b_start), *paint(r1_start, True), cr1c.animate.set_fill(CURRENT, 0.6))
        self.play(bridge_on(b_hold), run_time=0.6)
        self.cap("1) กด START → 1CR ทำงาน  2) 1CR-1 ปิดทันที", wait=1.8)
        r1_hold = [w1, w2, br1, br2, w5, jmp, w6, w7]
        self.play(bridge_on(b_start, False), w3.animate.set_color(DEAD), w4.animate.set_color(DEAD),
                  *paint([br1, br2], True))
        self.glow(hold[1], br1)
        self.cap("3) ปล่อย START → ไฟไหลผ่าน 1CR-1 แทน → คอยล์ยังติด = แลตช์ (Holding)", color=OK)
        self.play(bridge_on(b_stop, False), *paint(r1_hold, False),
                  cr1c.animate.set_fill(CURRENT, 0))
        self.play(bridge_on(b_hold, False))
        self.cap("4) กด STOP (NC) → ตัดวง → 1CR ดับ → 1CR-1 เปิด → ปลดแลตช์")
        self.play(bridge_on(b_stop, True))

        # ---------------- 3 cylinder + single LS
        self.step(3, "สั่งกระบอกสูบ + ลิมิตสวิตช์")
        xc, yc, yv = 2.6, 1.45, 0.45
        bar, mv, nm = cyl(xc, yc, "A", "#4FC3F7", w=2.0, rod_out=1.3)
        ls_mk = marker(xc + 2.3, yc, "1LS", WARN)
        va = valve2(xc, yv, "#4FC3F7")
        va[1].set_fill("#4FC3F7", 0.45)
        sol = Rectangle(width=0.36, height=0.36, color=WHITE).move_to([xc - 0.68, yv, 0])
        sol_lb = T("SOL A", 17, GRAYTXT).move_to([xc - 1.45, yv, 0])
        spr = pipe([(xc + 0.5, yv), (xc + 0.58, yv + 0.12), (xc + 0.68, yv - 0.12),
                    (xc + 0.78, yv + 0.12), (xc + 0.88, yv - 0.12), (xc + 0.96, yv)], WHITE, 2)
        spr_lb = T("สปริง", 17, GRAYTXT).move_to([xc + 1.45, yv, 0])
        cylfig = VGroup(bar, mv, nm, ls_mk, va, sol, sol_lb, spr, spr_lb, feeds(xc, yv, yc, 2.0))
        self.play(FadeIn(cylfig), run_time=1.0)
        self.cap("วาล์ว 5/2 โซลินอยด์เดี่ยว สปริงคืน: SOL A ได้ไฟ → A+ · ไฟดับ → สปริงดัน A−")
        cr2, b_cr2 = contact(-3.2, y2, "1CR-2")
        solc, soll = coil(-1.75, y2, "SOL A")
        v1 = wire([(XL, y2), (-3.32, y2)])
        v2 = wire([(-3.08, y2), (-2.0, y2)])
        v3 = wire([(-1.5, y2), (XR, y2)])
        self.play(FadeIn(cr2, b_cr2, solc, soll), Create(VGroup(v1, v2, v3)), run_time=1.0)
        self.cap("ขั้นบันไดที่ 2: หน้าสัมผัส 1CR-2 ส่งไฟไปคอยล์ SOL A")
        ls1, b_ls1 = contact(-3.2, y1, "1LS", nc=True)
        self.play(FadeOut(jmp, run_time=0.3))
        self.play(FadeIn(ls1, b_ls1))
        self.glow(ls1[2], ls_mk, WARN)
        self.cap("ใส่หน้าสัมผัส NC ของ 1LS อนุกรมในขั้นแรก · 1LS อยู่ที่ปลายช่วงยืดของก้านสูบ")
        r1_hold = [w1, w2, br1, br2, w5, w6, w7]
        r2 = [v1, v2, v3]
        self.play(bridge_on(b_start), *paint(r1_start[:5] + [w6, w7], True),
                  cr1c.animate.set_fill(CURRENT, 0.6))
        self.play(bridge_on(b_hold), bridge_on(b_cr2), *paint(r2, True),
                  solc.animate.set_fill(CURRENT, 0.6), sol.animate.set_fill(CURRENT, 0.6))
        self.play(bridge_on(b_start, False), w3.animate.set_color(DEAD), w4.animate.set_color(DEAD),
                  *paint([br1, br2], True), shift_valve(va, "L", "#4FC3F7"),
                  mv.animate.shift(1.0 * RIGHT), run_time=1.6)
        self.cap("กด START → 1CR แลตช์ → 1CR-2 ปิด → SOL A ได้ไฟ → A ยืดออก (A+)")
        self.play(Indicate(ls_mk, color=WARN, scale_factor=1.0), bridge_on(b_ls1, False))
        self.play(*paint(r1_hold, False), cr1c.animate.set_fill(CURRENT, 0))
        self.play(bridge_on(b_hold, False), bridge_on(b_cr2, False), *paint(r2, False),
                  solc.animate.set_fill(CURRENT, 0), sol.animate.set_fill(CURRENT, 0))
        self.cap("ก้านชน 1LS → NC เปิด → ตัดไฟ 1CR → 1CR-1 และ 1CR-2 เปิด → SOL A ดับ", color=WARN)
        self.play(shift_valve(va, "R", "#4FC3F7"), mv.animate.shift(1.0 * LEFT), run_time=1.4)
        self.play(bridge_on(b_ls1, True))
        self.cap("สปริงดีดสปูลกลับ → A หดกลับ (A−) · 1LS ปล่อยแล้ว แต่แลตช์หลุดไปแล้ว จึงหยุดรอ START")

        # ---------------- 4 on-delay timer
        self.step(4, "ไทม์เมอร์ On-Delay")
        t1, b_t1 = contact(-3.2, y1, "T1", nc=True)
        self.play(FadeOut(ls1, b_ls1, run_time=0.35))
        self.play(FadeIn(t1, b_t1))
        ls3, b_ls3 = contact(-3.2, y3, "1LS")
        tmc, tml = coil(-1.75, y3, "T1 (TON 5 s)")
        u1 = wire([(XL, y3), (-3.32, y3)])
        u2 = wire([(-3.08, y3), (-2.0, y3)])
        u3 = wire([(-1.5, y3), (XR, y3)])
        tval = DecimalNumber(0.0, num_decimal_places=1, font_size=26, color=YEL)
        tval.move_to([-2.65, y3 - 0.45, 0])
        tunit = T("s", 20, YEL).next_to(tval, RIGHT, buff=0.08)
        self.play(FadeIn(ls3, b_ls3, tmc, tml, tval, tunit), Create(VGroup(u1, u2, u3)))
        self.cap("อยากให้ A หนีบชิ้นงานค้าง 5 วินาทีก่อนถอย: 1LS (NO) สั่งคอยล์ไทม์เมอร์ T1")
        self.play(bridge_on(b_start), *paint(r1_start[:5] + [w6, w7], True),
                  cr1c.animate.set_fill(CURRENT, 0.6))
        self.play(bridge_on(b_hold), bridge_on(b_cr2), *paint(r2, True),
                  solc.animate.set_fill(CURRENT, 0.6), sol.animate.set_fill(CURRENT, 0.6))
        self.play(bridge_on(b_start, False), w3.animate.set_color(DEAD), w4.animate.set_color(DEAD),
                  *paint([br1, br2], True), shift_valve(va, "L", "#4FC3F7"),
                  mv.animate.shift(1.0 * RIGHT), run_time=1.6)
        self.play(Indicate(ls_mk, color=WARN, scale_factor=1.0), bridge_on(b_ls3),
                  *paint([u1, u2, u3], True), tmc.animate.set_fill(YEL, 0.5))
        self.cap("A ยืดชน 1LS → T1 ได้ไฟ เริ่มนับเวลา · หน้าสัมผัสยังไม่เปลี่ยน", wait=0.5)
        self.play(ChangeDecimalToValue(tval, 5.0), run_time=3.0, rate_func=linear)
        self.play(bridge_on(b_t1, False))
        self.play(*paint(r1_hold, False), cr1c.animate.set_fill(CURRENT, 0))
        self.play(bridge_on(b_hold, False), bridge_on(b_cr2, False), *paint(r2, False),
                  solc.animate.set_fill(CURRENT, 0), sol.animate.set_fill(CURRENT, 0))
        self.cap("ครบ 5 s → T1 (NC) เปิด → 1CR ดับ → SOL A ดับ", color=WARN, wait=1.6)
        self.play(shift_valve(va, "R", "#4FC3F7"), mv.animate.shift(1.0 * LEFT),
                  bridge_on(b_ls3, False), *paint([u1, u2, u3], False),
                  tmc.animate.set_fill(YEL, 0), run_time=1.4)
        self.play(ChangeDecimalToValue(tval, 0.0), bridge_on(b_t1, True), run_time=0.6)
        self.cap("A หดกลับ → 1LS ปล่อย → T1 ดับ รีเซ็ตเวลา · หน้าสัมผัส T1 กลับปิด")

        # ---------------- 5 check
        self.step(5, "ตรวจ + สรุป")
        sm = VGroup(T("แลตช์ = 1CR-1 (NO) ขนานปุ่ม START · STOP (NC) อนุกรม", 21, OK),
                    T("On-Delay (TON): ได้ไฟ → รอครบเวลา → หน้าสัมผัสจึงสลับ", 21),
                    T("Off-Delay (TOF): ได้ไฟ → สลับทันที · ตัดไฟ → ค้างต่อตามเวลา", 21))
        self.rows(list(sm), PX, -2.65, 0.5, PW)
        self.play(FadeIn(sm[0]))
        self.glow(sm[0], VGroup(hold, stop))
        self.play(FadeIn(sm[1]))
        self.play(FadeIn(sm[2]))
        self.cap("สรุป: ปุ่มกดติดปล่อยดับ → ต้องแลตช์ · ลิมิตสวิตช์/ไทม์เมอร์ใช้ตัดแลตช์เพื่อสั่งถอย",
                 color=YEL, wait=4.0)
        self.wait(1.0)


# ======================================================================
class FXH4_TwoCylLadder(ExamScene):
    """Ladder for A+ B+ A- B- with limit switches, A+ A- B+ B- trap, PLC I/O."""

    def construct(self):
        self.head("แลดเดอร์ 2 กระบอกสูบ A+ B+ A− B−", "W11 · Pneumatic 04 หน้า 9, 10, 17")
        PX = 3.45
        CC = {"A": "#4FC3F7", "B": "#FFB74D"}
        XC = {"A": 1.4, "B": 4.6}
        yc, yv = 1.5, 0.45
        cy, mk, vv, sols, figs = {}, {}, {}, {}, []
        for n in "AB":
            xc, lo = XC[n], n.lower()
            b, m, nm = cyl(xc, yc, n, CC[n])
            cy[n] = m
            mk[lo + "0"] = marker(xc + 1.05, yc, lo + "0", CC[n])
            mk[lo + "1"] = marker(xc + 1.85, yc, lo + "1", CC[n])
            vv[n] = valve2(xc, yv, CC[n])
            vv[n][1].set_fill(CC[n], 0.45)
            sp = Rectangle(width=0.3, height=0.36, color=WHITE).move_to([xc - 0.65, yv, 0])
            sm_ = Rectangle(width=0.3, height=0.36, color=WHITE).move_to([xc + 0.65, yv, 0])
            sols[n + "+"], sols[n + "-"] = sp, sm_
            lp = T(n + "+", 17, GRAYTXT).move_to([xc - 0.65, yv - 0.4, 0])
            lm = T(n + "−", 17, GRAYTXT).move_to([xc + 0.65, yv - 0.4, 0])
            figs += [b, m, nm, mk[lo + "0"], mk[lo + "1"], vv[n], feeds(xc, yv, yc), sp, sm_, lp, lm]
        fig = VGroup(*figs)

        def move(n, d):
            self.play(shift_valve(vv[n], "L" if d > 0 else "R", CC[n]),
                      cy[n].animate.shift(0.8 * d * RIGHT), run_time=1.3)

        # ---------------- 1 understand
        self.step(1, "เข้าใจโจทย์")
        self.play(FadeIn(fig), run_time=1.2)
        seq = M(r"\text{START}", r"\to A+", r"\to B+", r"\to A-", r"\to B-", size=36)
        fit_width(seq, 6.4)
        seq.move_to([PX, -0.55, 0])
        self.play(FadeIn(seq))
        self.cap("ลำดับหน้า 9: START → A+ → B+ → A− → B− · ลิมิตสวิตช์ a0 a1 b0 b1 ที่ปลายก้าน")
        self.cap("วาล์ว 5/2 โซลินอยด์คู่ (A+/A−): จ่ายไฟแวบเดียวก็พอ วาล์วจำตำแหน่งไว้เอง")

        # ---------------- 2 ladder
        self.step(2, "เขียนแลดเดอร์")
        rails = VGroup(Line([XL, 1.85, 0], [XL, -2.4, 0], color=WHITE, stroke_width=4),
                       Line([XR, 1.85, 0], [XR, -2.4, 0], color=WHITE, stroke_width=4))
        rl = VGroup(T("+24V", 18, CURRENT).move_to([XL, 2.07, 0]),
                    T("0V", 18, GRAYTXT).move_to([XR, 2.07, 0]))
        self.play(Create(rails), FadeIn(rl), run_time=0.8)
        self.cap("หลัก: ลิมิตสวิตช์ที่สเต็ปก่อนชน → สั่งโซลินอยด์ของสเต็ปถัดไป")
        YR = [1.2, 0.2, -0.8, -1.8]
        spec = [(["START", "b0"], "A+", "A", "START กับ b0 (B อยู่บ้าน) → SOL A+"),
                (["a1"], "B+", "B", "A ยืดสุดชน a1 → SOL B+"),
                (["b1"], "A-", "A", "B ยืดสุดชน b1 → SOL A−"),
                (["a0"], "B-", "B", "A หดสุดชน a0 → SOL B−")]
        rung = []
        for i, (cts, cn, cyn, txt) in enumerate(spec):
            y = YR[i]
            xs = [-5.3, -4.1][:len(cts)] if len(cts) == 2 else [-4.1]
            parts, brs, ws = VGroup(), [], []
            xprev = XL
            for x, nmx in zip(xs, cts):
                g, bb = contact(x, y, nmx)
                parts.add(g, bb)
                brs.append(bb)
                ws.append(wire([(xprev, y), (x - 0.12, y)]))
                xprev = x + 0.12
            cc, cl = coil(-1.75, y, cn.replace("-", "−"), size=18, inside=True)
            ws.append(wire([(xprev, y), (-2.0, y)]))
            ws.append(wire([(-1.5, y), (XR, y)]))
            parts.add(cc, cl, *ws)
            rung.append(dict(brs=brs, ws=ws, coil=cc, cts=parts, cn=cn))
            self.play(FadeIn(parts), run_time=0.8)
            mkey = cts[-1] if cts[-1] != "START" else "b0"
            self.glow(parts[2 * (len(cts) - 1)][-1], mk[mkey], CC[cyn])
            self.cap(f"ขั้นที่ {i + 1}: {txt}", wait=1.8)

        def energize(i, on, extra=()):
            r = rung[i]
            an = [bridge_on(b, on) for b in r["brs"]] + paint(r["ws"], on)
            an += [r["coil"].animate.set_fill(CURRENT, 0.6 if on else 0),
                   sols[r["cn"]].animate.set_fill(CURRENT, 0.6 if on else 0)]
            return an + list(extra)

        # ---------------- 3 step-through
        self.step(3, "เดินทีละสเต็ป")
        r4_partial = [bridge_on(rung[3]["brs"][0])] + paint(rung[3]["ws"], True) + [
            rung[3]["coil"].animate.set_fill(CURRENT, 0.6), sols["B-"].animate.set_fill(CURRENT, 0.6)]
        self.play(bridge_on(rung[0]["brs"][1]), *r4_partial)
        self.cap("ก่อนเริ่ม: a0 และ b0 ถูกกด (อยู่บ้าน) → SOL B− ติดอยู่ ไม่เป็นไร B หดอยู่แล้ว")
        self.play(*energize(0, True))
        self.play(*energize(3, False), *[] , run_time=0.6)
        move("A", 1)
        self.play(*energize(0, False))
        self.play(bridge_on(rung[0]["brs"][1]))
        self.cap("1) กด START (b0 ถูกกด) → SOL A+ → A ยืด · A ออกจาก a0 → SOL B− ดับ")
        self.play(Indicate(mk["a1"], color=WHITE, scale_factor=1.0), *energize(1, True))
        move("B", 1)
        self.play(bridge_on(rung[0]["brs"][1], False))
        self.cap("2) A ชน a1 → SOL B+ → B ยืด · B ออกจาก b0")
        self.play(Indicate(mk["b1"], color=WHITE, scale_factor=1.0), *energize(2, True))
        move("A", -1)
        self.play(*energize(1, False))
        self.cap("3) B ชน b1 → SOL A− → A หด (SOL A+ ดับแล้วเพราะปล่อย START) · A ออกจาก a1 → B+ ดับ")
        self.play(Indicate(mk["a0"], color=WHITE, scale_factor=1.0), *energize(3, True))
        move("B", -1)
        self.play(*energize(2, False), bridge_on(rung[0]["brs"][1]))
        self.cap("4) A ชน a0 → SOL B− → B หด · B ออกจาก b1 → A− ดับ · ชน b0 = พร้อมรอบใหม่")

        # ---------------- 4 check + trap + PLC
        self.step(4, "ตรวจ + กับดัก + PLC")
        self.play(FadeOut(seq, run_time=0.35))
        ck = VGroup(T("ตรวจ: ตอนสั่งแต่ละสเต็ป คอยล์ฝั่งตรงข้ามดับเสมอ → ไม่ชน", 21, OK),
                    T("A+ A− B+ B− (หน้า 10): a0 กดค้างตลอดที่ B ทำงาน", 21, WARN),
                    T("→ B+ กับ B− ได้ไฟพร้อมกัน → ต้องใช้รีเลย์แบ่งสเต็ป", 21, WARN))
        self.rows(list(ck), PX, -0.45, 0.55, 6.6)
        self.play(FadeIn(ck[0]))
        self.cap("ลำดับ A+ B+ A− B− ต่อตรงได้ เพราะลิมิตสวิตช์ของคำสั่งเก่าถูกปล่อยก่อนเสมอ", color=OK)
        self.play(FadeIn(ck[1]), FadeIn(ck[2]))
        self.glow(ck[1], mk["a0"], WARN)
        self.cap("กับดัก: ลำดับ A+ A− B+ B− ใช้วิธีนี้ไม่ได้ → ใช้ Stepping Relays (เหมือน Shift Register)",
                 color=WARN, wait=3.0)
        io = VGroup(T("PLC (หน้า 17): X004 = START · X000 = a0 · X001 = a1", 21),
                    T("X002 = b0 · X003 = b1 · Y001 = Sol A · Y002 = Sol B", 21),
                    T("เปลี่ยนลำดับ = แก้โปรแกรม ไม่ต้องรื้อสายไฟ/สายลม", 21, YEL))
        self.rows(list(io), PX, -2.25, 0.5, 6.6)
        self.play(FadeIn(io[0]), FadeIn(io[1]))
        self.cap("PLC: ลิมิตสวิตช์/ปุ่มเข้าขา X (Input) · โซลินอยด์ต่อขา Y (Output)")
        self.play(FadeIn(io[2]))
        self.glow(io[2])
        self.cap("สรุป: แลดเดอร์ = ลิมิตสวิตช์สเต็ปก่อน สั่งโซลินอยด์สเต็ปถัดไป · ระวังลิมิตที่กดค้าง",
                 color=YEL, wait=4.0)
        self.wait(1.0)
