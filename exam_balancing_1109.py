"""
exam_balancing_1109.py -- Mechanics of Machinery, exam 9 Nov 2026, topic 5: two-plane balancing.

Source notes (numbers from here and from pages_balancing_w10/verify_balancing.py):
  Exam_Prep/Mechanics of Machinery/W10 ชีทสรุป Two-plane balancing.md
  Exam_Prep/Mechanics of Machinery/W10 บทเรียน — Balancing (สมดุลโรเตอร์ สอนทีละหน้า).md

B40_ExamBalancingWhyTwoPlanes -- static vs dynamic, the couple, why two planes, 4-step procedure
B41_ExamTwoPlaneTable         -- lecture example p.19-21, table method + couple/force polygons + check
B42_ExamTwoPlanePractice      -- self-made practice problem as a drill (r = 100 mm)

The table/polygon numbers are computed in-scene with exactly the formulas of verify_balancing.py
(same inputs -> same values as the note: B 0.9037 @ 75.27, A 0.8817 @ -81.35; practice
m_A 0.863 @ 241.42, m_B 2.218 @ 4.64).
"""

import numpy as np
from manim import *
from mlib import *

C1, C2, C3 = "#42A5F5", "#FFB74D", "#66BB6A"   # masses 1, 2, 3
CB, CA = "#EF5350", "#CE93D8"                 # correction planes B, A
MCOL = [C1, C2, C3]
SHAFT = METAL


def P2(x, y):
    return np.array([x, y, 0.0])


def U(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def T(txt, size=20, color=WHITE):
    return Text(txt, font_size=size, color=color)


def M(tex, size=30, color=WHITE):
    return MathTex(tex, font_size=size, color=color)


def vrow(*mobs, buff=0.25):
    return VGroup(*mobs).arrange(RIGHT, buff=buff)


def panel(*mobs, x0=0.35, top=2.15, gap=0.2, max_w=6.6):
    for mo in mobs:
        fit_width(mo, max_w)
    g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=gap)
    g.move_to([x0 + g.width / 2, top - g.height / 2, 0])
    return g


def vec(a, b, color, sw=5, tip=0.2):
    return Arrow(a, b, buff=0, color=color, stroke_width=sw, tip_length=tip,
                 max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=20)


KGM = r"\ \text{kg}\cdot\text{m}"


def ang_tex(x, y, s):
    a = float(np.degrees(np.arctan2(y, x)))
    base = float(np.degrees(np.arctan(abs(y) / abs(x))))
    sg = "(%s,%s)" % ("+" if x >= 0 else "-", "+" if y >= 0 else "-")
    frac = r"\tan^{-1}\frac{%.4f}{%.4f}" % (abs(y), abs(x))
    if x >= 0 and y >= 0:
        return r"%s\ \text{Q1}:\ \theta_%s = %s = %.2f^\circ" % (sg, s, frac, a), a
    if x < 0 <= y:
        return r"%s\ \text{Q2}:\ \theta_%s = 180^\circ - %.2f^\circ = %.2f^\circ" % (sg, s, base, a), a
    if x < 0 and y < 0:
        return r"%s\ \text{Q3}:\ \theta_%s = 180^\circ + %.2f^\circ = %.2f^\circ" % (sg, s, base, a + 360), a + 360
    return r"%s\ \text{Q4}:\ \theta_%s = -%.2f^\circ\ (= %.2f^\circ)" % (sg, s, base, 360 - base), a


def solve(D):
    """verify_balancing.two_plane() -- plane A at l = 0, plane B at lB"""
    ms = [tuple(float(v) for v in row) for row in D["ms"]]
    lB = float(D["lB"])
    rows = []
    for m, R, t, l in ms:
        Rx, Ry = R * np.cos(np.radians(t)), R * np.sin(np.radians(t))
        rows.append(dict(m=m, R=R, t=t, l=l, mRx=m * Rx, mRy=m * Ry, mRxl=m * Rx * l, mRyl=m * Ry * l))
    S = {k: sum(r[k] for r in rows) for k in ("mRx", "mRy", "mRxl", "mRyl")}
    Bx, By = -S["mRxl"] / lB, -S["mRyl"] / lB
    Ax, Ay = -S["mRx"] - Bx, -S["mRy"] - By
    allm = [(r["mRx"], r["mRy"], r["l"]) for r in rows] + [(Bx, By, lB), (Ax, Ay, 0.0)]
    res = max(abs(sum(a for a, b, l in allm)), abs(sum(b for a, b, l in allm)),
              abs(sum(a * l for a, b, l in allm)), abs(sum(b * l for a, b, l in allm)))
    return ms, lB, rows, S, (Bx, By), (Ax, Ay), res


class ExamScene(SafeScene):
    _cap = None
    PACE = 2.3   # reading time: every wait() is stretched (exam-cram clip, Min reads Thai captions)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * self.PACE, *args, **kwargs)

    def say(self, txt, size=21):
        new = caption_top(txt, size=size, max_w=13.0)
        if self._cap is not None:
            self.play(FadeOut(self._cap), run_time=0.3)
            self.play(FadeIn(new), run_time=0.4)
        else:
            self.play(FadeIn(new), run_time=0.6)
        self._cap = new
        super().wait(1.7)

    def glow(self, term, fig, color, rt=1.4):
        wide = term.width > 3.2 or isinstance(term, Text)
        anims = [Indicate(term, color=WHITE, scale_factor=1.0 if wide else 1.2),
                 Circumscribe(term, color=color, buff=0.04, stroke_width=3, fade_out=True)]
        if fig is not None:
            anims.append(Indicate(fig, color=WHITE, scale_factor=1.0))
        self.play(*anims, run_time=rt)

    def swap(self, old, new, rt=0.8):
        self.play(FadeOut(old), run_time=0.35)
        self.play(FadeIn(new), run_time=rt)

    # ---------------------------------------------------------------- shared figures
    def side_view(self, ms, lB, values, xA=-6.3, xB=-1.8, ys=1.3):
        """axial (side) view: planes A (l = 0) and B (l = lB), unbalance masses on discs,
        distances l_i measured from plane A."""
        k = (xB - xA) / lB
        Rmax = max(R for m, R, t, l in ms)
        g = {}
        g["shaft"] = Line(P2(xA - 0.4, ys), P2(xB + 0.4, ys), color=SHAFT, stroke_width=8)
        g["pA"] = DashedLine(P2(xA, ys - 0.75), P2(xA, ys + 0.72), color=CA, stroke_width=3)
        g["pB"] = DashedLine(P2(xB, ys - 0.75), P2(xB, ys + 0.72), color=CB, stroke_width=3)
        g["lA"] = M(r"A", 26, CA).next_to(g["pA"], UP, buff=0.06)
        g["lB"] = M(r"B", 26, CB).next_to(g["pB"], UP, buff=0.06)
        g["xA"], g["xB"], g["ys"] = xA, xB, ys
        g["discs"], g["dots"], g["mlabs"], g["dims"], g["dlabs"] = [VGroup() for _ in range(5)]
        for i, (m, R, t, l) in enumerate(ms):
            x = xA + k * l
            y = ys + 0.55 * R * np.sin(np.radians(t)) / Rmax
            g["discs"].add(Line(P2(x, ys - 0.6), P2(x, ys + 0.6), color=GRAYTXT, stroke_width=3))
            d = Dot(P2(x, y), radius=0.1, color=MCOL[i])
            g["dots"].add(d)
            g["mlabs"].add(M(r"m_%d" % (i + 1), 24, MCOL[i]).next_to(d, RIGHT, buff=0.08))
        rows = [(l, MCOL[i], r"l_%d" % (i + 1), values[i] if values else None)
                for i, (m, R, t, l) in enumerate(ms)]
        rows.append((lB, CB, r"l_B", values[-1] if values else None))
        for j, (l, col, sym, val) in enumerate(rows):
            yd = ys - 0.95 - 0.3 * j
            a = DoubleArrow(P2(xA, yd), P2(xA + k * l, yd), buff=0, color=col, stroke_width=2,
                            tip_length=0.12, max_tip_length_to_length_ratio=0.2)
            lab = M(sym if val is None else r"%s = %s" % (sym, val), 21, col)
            lab.next_to(a.get_end(), RIGHT, buff=0.08)
            g["dims"].add(a)
            g["dlabs"].add(lab)
        g["all"] = VGroup(g["shaft"], g["pA"], g["pB"], g["lA"], g["lB"], g["discs"], g["dots"],
                          g["mlabs"], g["dims"], g["dlabs"])
        return g

    def end_view(self, ms, O=P2(-3.75, -2.35), rad=1.3):
        Rmax = max(R for m, R, t, l in ms)
        g = {"O": O}
        g["disk"] = DashedVMobject(Circle(radius=rad, color=SHAFT, stroke_width=2).move_to(O), num_dashes=40)
        g["ax"] = VGroup(Arrow(O + LEFT * 1.5, O + RIGHT * 1.6, buff=0, color=GRAYTXT, stroke_width=2,
                               tip_length=0.14),
                         Arrow(O + DOWN * 1.45, O + UP * 1.42, buff=0, color=GRAYTXT, stroke_width=2,
                               tip_length=0.14))
        g["axl"] = VGroup(M("x", 22, GRAYTXT).next_to(O + RIGHT * 1.6, DOWN, buff=0.06),
                          M("y", 22, GRAYTXT).next_to(O + UP * 1.42, RIGHT, buff=0.08))
        g["vecs"], g["rlabs"], g["arcs"], g["tips"] = VGroup(), VGroup(), VGroup(), []
        for i, (m, R, t, l) in enumerate(ms):
            tip = O + 1.15 * R / Rmax * U(t)
            g["tips"].append(tip)
            g["vecs"].add(vec(O, tip, MCOL[i], sw=4, tip=0.16))
            g["rlabs"].add(M(r"R_%d" % (i + 1), 22, MCOL[i]).move_to(tip + 0.26 * U(t)))
            g["arcs"].add(Arc(radius=0.24 + 0.11 * i, start_angle=0, angle=np.radians(t), arc_center=O,
                              color=MCOL[i], stroke_width=2.5))
        g["all"] = VGroup(g["disk"], g["ax"], g["axl"], g["vecs"], g["rlabs"], g["arcs"])
        return g

    def projection(self, ev, ms, i=0):
        O, tip = ev["O"], ev["tips"][i]
        col = MCOL[i]
        px, py = P2(tip[0], O[1]), P2(O[0], tip[1])
        lx = DashedLine(tip, px, color=col, stroke_width=2, dash_length=0.06)
        ly = DashedLine(tip, py, color=col, stroke_width=2, dash_length=0.06)
        bx = Line(O, px, color=col, stroke_width=7, stroke_opacity=0.7)
        by = Line(O, py, color=col, stroke_width=7, stroke_opacity=0.7)
        tx = M(r"R_{%dx}" % (i + 1), 20, col).next_to(px, DOWN if tip[1] > O[1] else UP, buff=0.12)
        ty = M(r"R_{%dy}" % (i + 1), 20, col).next_to(py, LEFT if tip[0] > O[0] else RIGHT, buff=0.1)
        return VGroup(lx, ly, bx, by, tx, ty)

    def polygon(self, vecs, cols, labs, close_col, close_lab, box, ttl):
        pts = [np.zeros(2)]
        for v in vecs:
            pts.append(pts[-1] + np.asarray(v))
        A = np.array(pts)
        lo, hi = A.min(0), A.max(0)
        (x0, x1), (y0, y1) = box
        s = min((x1 - x0) / max(hi[0] - lo[0], 1e-9), (y1 - y0) / max(hi[1] - lo[1], 1e-9))
        cb, cp = np.array([(x0 + x1) / 2, (y0 + y1) / 2]), (lo + hi) / 2

        def to(p):
            q = cb + s * (np.asarray(p) - cp)
            return P2(q[0], q[1])

        cen = to(A[:-1].mean(0))
        arrows, labels = VGroup(), VGroup()
        segs = [(pts[i], pts[i + 1], cols[i], labs[i]) for i in range(len(vecs))]
        segs.append((pts[-1], pts[0], close_col, close_lab))
        placed = []

        def hits(c, w, h):
            for (pc, pw, ph) in placed:
                if abs(c[0] - pc[0]) < (w + pw) / 2 + 0.06 and abs(c[1] - pc[1]) < (h + ph) / 2 + 0.04:
                    return True
            return (c[0] - w / 2 < -7.0 or c[0] + w / 2 > -0.15 or c[1] - h / 2 < -3.95
                    or c[1] + h / 2 > y1 + 0.1)

        for a, b, col, lab in segs:
            pa, pb = to(a), to(b)
            arrows.add(vec(pa, pb, col, sw=5, tip=0.2))
            d = (pb - pa) / max(np.linalg.norm(pb - pa), 1e-9)
            n = np.array([-d[1], d[0], 0.0])
            if np.dot((pa + pb) / 2 - cen, n) < 0:
                n = -n
            t = M(lab, 21, col)
            best = None
            for frac in (0.5, 0.65, 0.35, 0.8, 0.2):
                p = pa + frac * (pb - pa)
                for sgn in (1, -1):
                    nn = n * sgn
                    ext = 0.5 * (abs(nn[0]) * t.width + abs(nn[1]) * t.height)
                    for k in range(5):
                        c = p + nn * (0.12 + ext + 0.22 * k)
                        if not hits(c, t.width, t.height):
                            best = c
                            break
                    if best is not None:
                        break
                if best is not None:
                    break
            if best is None:
                best = (pa + pb) / 2 + n * (0.12 + 0.5 * (abs(n[0]) * t.width + abs(n[1]) * t.height))
            t.move_to(best)
            placed.append((best, t.width, t.height))
            labels.add(t)
        start = Dot(to(pts[0]), radius=0.07, color=WHITE)
        head = T(ttl, 18, GRAYTXT)
        head.move_to([(x0 + x1) / 2, y1 + 0.32, 0])
        return arrows, labels, start, head

    # ---------------------------------------------------------------- full worked example
    def worked_example(self, D):
        ms, lB, rows, S, (Bx, By), (Ax, Ay), res = solve(D)
        n = len(ms)
        r_corr = D.get("r")
        sv = self.side_view(ms, lB, [mm[3] for mm in D["ms"]] + [D["lB"]])
        ev = self.end_view(ms)
        X0 = 0.0

        def table(heads, cells, widths, y_head, dy, row_cols, size=24, sum_gap=0.0):
            xs = [X0]
            for w in widths[:-1]:
                xs.append(xs[-1] + w)
            head = VGroup(*[fit_width(M(h, 24, GRAYTXT), widths[i] - 0.1).move_to(
                [xs[i] + widths[i] / 2, y_head, 0]) for i, h in enumerate(heads)])
            rws = []
            for r, rc in enumerate(cells):
                y = y_head - (r + 1) * dy - (sum_gap if (sum_gap and r == len(cells) - 1) else 0)
                rws.append(VGroup(*[fit_width(M(c, size, row_cols[r]), widths[i] - 0.1).move_to(
                    [xs[i] + widths[i] / 2, y, 0]) for i, c in enumerate(rc)]))
            hl = Line(P2(X0, y_head - dy / 2), P2(X0 + sum(widths), y_head - dy / 2), color=GRAYTXT,
                      stroke_width=1.5)
            return head, rws, hl

        # ---- step 1: understand -- figure + given data
        self.say(D["say0"])
        self.play(Create(sv["shaft"]), Create(sv["pA"]), Create(sv["pB"]), FadeIn(sv["lA"]),
                  FadeIn(sv["lB"]), run_time=1.2)
        self.play(Create(sv["discs"]), FadeIn(sv["dots"]), FadeIn(sv["mlabs"]), run_time=1.0)
        self.play(FadeIn(ev["disk"]), Create(ev["ax"]), FadeIn(ev["axl"]), run_time=0.8)
        self.play(*[GrowArrow(a) for a in ev["vecs"]], FadeIn(ev["rlabs"]), Create(ev["arcs"]), run_time=1.2)

        rc = "?" if r_corr is None else r_corr
        g_cells = [[str(i + 1)] + list(D["ms"][i][:3]) + [D["ms"][i][3]] for i in range(n)]
        g_cells = [[c[0], c[1], c[2], c[3] + r"^\circ", c[4]] for c in g_cells]
        g_cells += [["A", "?", rc, "?", "0"], ["B", "?", rc, "?", D["lB"]]]
        head1, rows1, hl1 = table([r"i", r"m\,(\text{kg})", r"R\,(\text{m})", r"\theta", r"l\,(\text{m})"],
                                  g_cells, [0.7, 1.45, 1.45, 1.45, 1.45], 2.0, 0.5,
                                  MCOL[:n] + [CA, CB])
        self.say(D["say1"])
        self.play(FadeIn(head1), Create(hl1))
        for i in range(n):
            self.play(FadeIn(rows1[i]), run_time=0.5)
            self.glow(rows1[i], VGroup(sv["dots"][i], sv["dims"][i], ev["vecs"][i], ev["arcs"][i]), MCOL[i],
                      rt=1.1)
        note1 = T(D["note1"], 19, GRAYTXT)
        self.play(FadeIn(rows1[n]), FadeIn(rows1[n + 1]))
        fit_width(note1, 6.9)
        note1.move_to([X0 + note1.width / 2, 2.0 - (n + 3) * 0.5 - 0.1, 0])
        self.play(FadeIn(note1))
        self.glow(rows1[n], VGroup(sv["pA"], sv["lA"]), CA, rt=1.1)
        self.glow(rows1[n + 1], VGroup(sv["pB"], sv["lB"], sv["dims"][n], sv["dlabs"][n]), CB, rt=1.1)
        self.play(FadeIn(sv["dims"]), FadeIn(sv["dlabs"]))
        self.wait(2.0)

        # ---- step 2: formula / table
        self.say("ขั้น 2 แตกเวกเตอร์ตามแกน x, y แล้วคูณ m (และ l) — θ วัดจากแกน x ทวนเข็ม")
        self.play(FadeOut(VGroup(head1, hl1, *rows1, note1)), run_time=0.4)
        fm = panel(M(r"R_x = R\cos\theta,\qquad R_y = R\sin\theta", 30),
                   M(r"mR_x,\ \ mR_y\ \ (\text{kg}\cdot\text{m}),\qquad mR_xl,\ \ mR_yl\ \ (\text{kg}\cdot\text{m}^2)", 28),
                   x0=X0, top=-0.6, gap=0.25, max_w=6.9)
        pi_ = D.get("proj", 0)
        pj = self.projection(ev, ms, pi_)
        self.play(FadeIn(fm[0]))
        self.play(Create(pj[:4]), FadeIn(pj[4:]), run_time=1.0)
        self.glow(fm[0], pj, MCOL[pi_])
        self.play(FadeIn(fm[1]))
        self.wait(1.5)

        def f4(v):
            return "%+.4f" % v if abs(v) >= 5e-5 else "0"

        c_cells = [[str(i + 1), f4(r["mRx"]), f4(r["mRy"]), f4(r["mRxl"]), f4(r["mRyl"])]
                   for i, r in enumerate(rows)]
        c_cells.append([r"\Sigma", f4(S["mRx"]), f4(S["mRy"]), f4(S["mRxl"]), f4(S["mRyl"])])
        head2, rows2, hl2 = table([r"i", r"mR_x", r"mR_y", r"mR_x\,l", r"mR_y\,l"], c_cells,
                                  [0.55, 1.6, 1.6, 1.6, 1.6], 2.05, 0.46, MCOL[:n] + [WHITE],
                                  size=25, sum_gap=0.12)
        sumline = Line(P2(X0, rows2[-1].get_y() + 0.27), P2(X0 + 6.95, rows2[-1].get_y() + 0.27),
                       color=GRAYTXT, stroke_width=1.5)
        self.say(D["say2"])
        self.play(FadeIn(head2), Create(hl2))
        for i in range(n):
            self.play(FadeIn(rows2[i]), run_time=0.5)
            self.glow(rows2[i], VGroup(ev["vecs"][i], sv["dots"][i], sv["dims"][i]), MCOL[i], rt=1.1)
            if i == pi_:
                self.play(FadeOut(pj), run_time=0.4)
        self.say("รวมแต่ละคอลัมน์ — ผลรวม 4 ตัวนี้คือทุกอย่างที่ต้องใช้ต่อ")
        self.play(Create(sumline), FadeIn(rows2[n]))
        self.glow(rows2[n], VGroup(*rows2[:n]), WHITE)
        self.play(FadeOut(fm), run_time=0.4)
        self.wait(1.0)

        # ---- step 3a: plane B first (moments about A)
        magB = float(np.hypot(Bx, By))
        angB_tex, angB = ang_tex(Bx, By, "B")
        pB = panel(
            T("ขั้น 3a — ระนาบ B ก่อน: โมเมนต์รอบระนาบ A = 0", 21, OK),
            M(r"m_BR_{Bx} = -\frac{\sum mR_xl}{l_B} = -\frac{(%.4f)}{%s} = %+.4f" % (S["mRxl"], D["lB"], Bx), 28, CB),
            M(r"m_BR_{By} = -\frac{\sum mR_yl}{l_B} = -\frac{(%.4f)}{%s} = %+.4f" % (S["mRyl"], D["lB"], By), 28, CB),
            M(r"m_BR_B = \sqrt{(%.4f)^2 + (%.4f)^2} = %.4f" % (Bx, By, magB) + KGM, 28, CB),
            M(angB_tex, 28, CB),
            x0=X0, top=-0.35, gap=0.13, max_w=6.9)
        self.say("ขั้น 3a หา B ก่อน: เอาโมเมนต์รอบระนาบ A — m_A อยู่ที่ l = 0 ไม่มีแขนโมเมนต์ จึงหายไปจากสมการ")
        SVS = 0.62
        self.play(FadeOut(ev["all"]), sv["all"].animate.scale(SVS, about_point=P2(-6.8, 2.37)), run_time=0.9)
        self.play(FadeIn(pB[0]))
        self.glow(pB[0], VGroup(sv["pA"], sv["lA"]), CA, rt=1.1)
        self.play(FadeIn(pB[1]))
        self.glow(pB[1], VGroup(rows2[n][3], sv["dims"][n], sv["dlabs"][n]), CB)
        self.play(FadeIn(pB[2]))
        self.glow(pB[2], VGroup(rows2[n][4], sv["dims"][n], sv["dlabs"][n]), CB)

        box = ((-6.3, -1.3), (-3.8, -0.3))
        cv = [(r["m"] * r["R"] * r["l"] * np.cos(np.radians(r["t"])),
               r["m"] * r["R"] * r["l"] * np.sin(np.radians(r["t"]))) for r in rows]
        clabs = [r"m_%dR_%dl_%d = %.3f" % (i + 1, i + 1, i + 1, r["m"] * r["R"] * r["l"]) for i, r in enumerate(rows)]
        ca, cl, cs, ch = self.polygon(cv, MCOL, clabs, CB, r"m_BR_Bl_B = %.3f" % (magB * lB), box,
                                      "Couple polygon: ต่อ mRl หัวต่อหาง (kg·m²)")
        self.say("ดูเป็นภาพ: couple polygon — ต่อเวกเตอร์ m R l ทีละตัวหัวต่อหาง เส้นที่ปิดกลับจุดเริ่ม = m_B R_B l_B")
        self.play(FadeIn(ch), FadeIn(cs))
        for i in range(n):
            self.play(GrowArrow(ca[i]), FadeIn(cl[i]), run_time=1.0)
        self.play(GrowArrow(ca[n]), FadeIn(cl[n]), run_time=1.3)
        self.play(FadeIn(pB[3]))
        self.glow(pB[3], VGroup(ca[n], cl[n]), CB)
        self.play(FadeIn(pB[4]))
        dB = Dot(P2(sv["pB"].get_x(), sv["shaft"].get_y() + 0.45 * SVS * np.sin(np.radians(angB))), radius=0.09, color=CB)
        mB = M(r"m_B", 19, CB).next_to(dB, RIGHT, buff=0.08)
        self.play(FadeIn(dB, scale=1.5), FadeIn(mB))
        self.glow(pB[4], VGroup(ca[n], dB), CB)
        self.wait(2.0)

        # ---- step 3b: plane A (force sum)
        magA = float(np.hypot(Ax, Ay))
        angA_tex, angA = ang_tex(Ax, Ay, "A")
        pA = panel(
            T("ขั้น 3b — ระนาบ A: แรงรวม = 0", 21, OK),
            M(r"m_BR_B = %.4f%s\ \text{@}\ %.2f^\circ\ \ (\text{from 3a})" % (magB, KGM, angB), 26, CB),
            M(r"m_AR_{Ax} = -\sum mR_x - m_BR_{Bx} = -(%.4f) - (%.4f) \approx %+.4f" % (S["mRx"], Bx, Ax), 28, CA),
            M(r"m_AR_{Ay} = -\sum mR_y - m_BR_{By} = -(%.4f) - (%.4f) \approx %+.4f" % (S["mRy"], By, Ay), 28, CA),
            M(r"m_AR_A = \sqrt{(%.4f)^2 + (%.4f)^2} = %.4f" % (Ax, Ay, magA) + KGM, 28, CA),
            M(angA_tex, 28, CA),
            x0=X0, top=-0.35, gap=0.13, max_w=6.9)
        self.say("ขั้น 3b หา A: แรงรวมต้องเป็นศูนย์ — รู้ m_B R_B แล้ว เหลือตัวไม่รู้แค่ m_A R_A")
        self.play(FadeOut(pB), FadeOut(VGroup(ca, cl, cs, ch)), run_time=0.4)
        self.play(FadeIn(pA[0]), FadeIn(pA[1]))
        fv = [(r["mRx"], r["mRy"]) for r in rows] + [(Bx, By)]
        flabs = [r"m_%dR_%d = %.3f" % (i + 1, i + 1, r["m"] * r["R"]) for i, r in enumerate(rows)]
        flabs.append(r"m_BR_B = %.3f" % magB)
        fa, fl, fs, fh = self.polygon(fv, MCOL + [CB], flabs, CA, r"m_AR_A = %.3f" % magA, box,
                                      "Force polygon: ต่อ mR หัวต่อหาง (kg·m)")
        self.say("force polygon: ต่อ m R ทั้งหมด + m_B R_B — เส้นที่ปิดรูปกลับจุดเริ่ม = m_A R_A")
        self.play(FadeIn(fh), FadeIn(fs))
        for i in range(n + 1):
            self.play(GrowArrow(fa[i]), FadeIn(fl[i]), run_time=0.9)
        self.play(GrowArrow(fa[n + 1]), FadeIn(fl[n + 1]), run_time=1.3)
        self.play(FadeIn(pA[2]))
        self.glow(pA[2], VGroup(rows2[n][1], fa[n]), CA)
        self.play(FadeIn(pA[3]))
        self.glow(pA[3], VGroup(rows2[n][2], fa[n]), CA)
        self.play(FadeIn(pA[4]))
        self.glow(pA[4], VGroup(fa[n + 1], fl[n + 1]), CA)
        self.play(FadeIn(pA[5]))
        dA = Dot(P2(sv["pA"].get_x(), sv["shaft"].get_y() + 0.45 * SVS * np.sin(np.radians(angA))), radius=0.09, color=CA)
        mA = M(r"m_A", 19, CA).next_to(dA, RIGHT, buff=0.08)
        self.play(FadeIn(dA, scale=1.5), FadeIn(mA))
        self.glow(pA[5], VGroup(fa[n + 1], dA), CA)
        self.say(D["say_quad"])
        self.wait(2.0)

        # ---- step 4: check + answers
        self.say("ขั้น 4 ตรวจ: ใส่ m_A, m_B กลับเข้าไป — แรงรวม = 0 และโมเมนต์รวม = 0 → สมดุลจริง")
        self.play(FadeOut(VGroup(head2, hl2, *rows2, sumline, pA)), run_time=0.4)
        lines = [
            T("ขั้น 4 — ตรวจ: มวล %d ก้อน + m_A + m_B" % n, 22, OK),
            M(r"\textstyle\sum m\vec R = 0\ \checkmark\qquad \sum m\vec R\,l = 0\ \checkmark", 32, OK),
            T("คำนวณซ้ำ (สคริปต์): แรงและโมเมนต์ที่เหลือ = 0 (เศษปัดของเครื่อง) — polygon ปิดพอดี", 19, GRAYTXT),
            M(r"\text{B: } m_BR_B = %.4f%s\ \text{@}\ %.2f^\circ" % (magB, KGM, angB), 30, CB),
            M(r"\text{A: } m_AR_A = %.4f%s\ \text{@}\ %s" % (magA, KGM, D["angA_str"]), 30, CA),
        ]
        if r_corr is not None:
            r = float(r_corr)
            lines += [M(r"m_B = \frac{%.4f}{%s} = %.3f\ \text{kg}\qquad m_A = \frac{%.4f}{%s} = %.3f\ \text{kg}"
                        % (magB, r_corr, magB / r, magA, r_corr, magA / r), 30, OK)]
        lines += [T(D["trap"], 19, WARN)]
        chk = panel(*lines, x0=X0, top=2.05, gap=0.24, max_w=6.9)
        self.play(FadeIn(chk[0]), FadeIn(chk[1]))
        self.glow(chk[1], VGroup(fa, dA, dB), OK)
        self.play(FadeIn(chk[2]))
        self.play(FadeIn(chk[3]))
        self.glow(chk[3], VGroup(dB, mB, fa[n]), CB)
        self.play(FadeIn(chk[4]))
        self.glow(chk[4], VGroup(dA, mA, fa[n + 1]), CA)
        ans = VGroup(chk[3], chk[4]) if r_corr is None else VGroup(chk[3], chk[4], chk[5])
        bx_ = SurroundingRectangle(ans, color=OK, buff=0.12)
        self.play(Create(bx_))
        if r_corr is not None:
            self.glow(chk[5], VGroup(dA, dB), OK)
        self.play(FadeIn(chk[-1]))
        self.wait(5.0)


# =====================================================================
# B40 -- why two planes
# =====================================================================
class B40_ExamBalancingWhyTwoPlanes(ExamScene):
    def construct(self):
        self.add(title("ทำไมต้องถ่วงสมดุล 2 ระนาบ (Two-plane balancing)", size=28),
                 page_ref("สไลด์หน้า 2-14"))

        # ---------------- part 1: static balance (one plane)
        O = P2(-3.9, -0.75)
        k = 1.45
        disk = Circle(radius=2.0, color=SHAFT, stroke_width=3, fill_color=SHAFT, fill_opacity=0.12).move_to(O)
        axes = VGroup(DashedLine(O + LEFT * 2.2, O + RIGHT * 2.2, color=GRAYTXT, stroke_width=1.5),
                      DashedLine(O + DOWN * 2.2, O + UP * 2.2, color=GRAYTXT, stroke_width=1.5))
        hub = Dot(O, radius=0.07, color=WHITE)
        data = [("1", 1.2, 1.135, 113.4, C1), ("2", 1.8, 0.822, 48.8, C2), ("b", 2.980, 0.806, 259.6, CB)]
        parts = []
        for s, m, R, t, col in data:
            u = U(t)
            perp = np.array([-u[1], u[0], 0.0])
            tip = O + k * R * u
            v = vec(O, tip, col, sw=4, tip=0.18)
            d = Dot(tip, radius=0.08 + 0.035 * m, color=col)
            ml = M(r"m_%s" % s, 26, col).move_to(tip + perp * 0.36)
            rl = M(r"R_%s" % s, 24, col).move_to((O + tip) / 2 - perp * 0.27)
            parts.append(VGroup(v, d, ml, rl))
        u1 = U(113.4)
        tip1 = O + k * 1.135 * u1
        F1 = vec(tip1 + u1 * 0.18, tip1 + u1 * 1.0, C1, sw=5, tip=0.2)
        F1l = M(r"F_1 = m_1R_1\omega^2", 22, C1).next_to(F1.get_end(), LEFT, buff=0.1)
        om = Arc(radius=0.6, start_angle=150 * DEGREES, angle=60 * DEGREES, arc_center=O, color=WHITE,
                 stroke_width=3)
        om.add_tip(tip_length=0.14, tip_width=0.14)
        oml = M(r"\omega", 28).move_to(O + 0.95 * LEFT)
        caption1 = T("แผ่นบาง: มวลทุกก้อนอยู่ระนาบเดียว (มองตามแกนเพลา)", 18, GRAYTXT).move_to([-3.9, -3.1, 0])

        self.say("เริ่มจาก static balance: แผ่นหมุนบาง มวลไม่สมดุลทุกก้อนอยู่ในระนาบเดียวกัน")
        self.play(FadeIn(disk), Create(axes), FadeIn(hub), FadeIn(caption1), run_time=1.0)
        self.play(*[GrowArrow(p[0]) for p in parts[:2]], *[FadeIn(p[1:]) for p in parts[:2]], run_time=1.2)
        self.play(Create(om), FadeIn(oml))

        p1 = panel(
            T("Static balance — มวลอยู่ระนาบเดียว", 22, OK),
            vrow(M(r"F = mR\omega^2", 32), T("แรงเหวี่ยง ทิศตามเวกเตอร์ R", 19, GRAYTXT)),
            M(r"\sum m_i\vec R_i = m_1\vec R_1 + m_2\vec R_2 + m_b\vec R_b = 0", 30),
            T("ω² ร่วมกันทุกเทอม → ตัดทิ้ง คิดแค่ mR (kg·m)", 19, GRAYTXT),
            T("ตัวอย่างสไลด์หน้า 7–9 (คำนวณซ้ำ):", 19),
            M(r"m_bR_b = 2.402\ \text{kg}\cdot\text{m}\ \text{@}\ 259.6^\circ", 30, CB),
            M(r"R_b = 0.806\ \text{m}\ \Rightarrow\ m_b = \frac{2.402}{0.806} = 2.980\ \text{kg}", 30, CB),
            T("ระวัง: สไลด์พิมพ์ m_b = 2.908 — ผิด ค่าที่ถูกคือ 2.980 kg", 19, WARN))
        self.play(FadeIn(p1[0]), FadeIn(p1[1]))
        self.play(GrowArrow(F1), FadeIn(F1l))
        self.glow(p1[1][0], VGroup(F1, F1l, parts[0][0], oml), C1)
        self.say("ถ่วงด้วยมวล m_b ก้อนเดียว ให้ผลรวมเวกเตอร์ mR เป็นศูนย์ → แรงเหวี่ยงรวมหักล้างกันหมด")
        self.play(GrowArrow(parts[2][0]), FadeIn(parts[2][1:]))
        self.play(FadeIn(p1[2]))
        self.glow(p1[2], VGroup(*[p[0] for p in parts]), WHITE)
        self.play(FadeIn(p1[3]))
        self.play(FadeIn(p1[4]), FadeIn(p1[5]))
        self.glow(p1[5], parts[2], CB)
        self.play(FadeIn(p1[6]))
        self.glow(p1[6], VGroup(parts[2][0], parts[2][3]), CB)
        self.play(FadeIn(p1[7]))
        self.wait(2.5)

        # ---------------- part 2: why static is not enough (slide p.12)
        fig1 = VGroup(disk, axes, hub, *parts, F1, F1l, om, oml, caption1)
        self.say("แต่ถ้ามวลอยู่คนละตำแหน่งตามแนวแกนเพลา (เพลายาว) static balance ไม่พอ — หน้า 12")
        self.play(FadeOut(fig1), FadeOut(p1), run_time=0.5)

        ys = -0.9
        z1, z2, r = -4.6, -2.9, 0.85
        shaft = Line(P2(-6.7, ys), P2(-0.8, ys), color=SHAFT, stroke_width=8)
        brg = VGroup(*[Triangle(color=GRAYTXT, fill_opacity=0.6).scale(0.2).move_to(P2(x, ys - 0.3))
                       for x in (-6.2, -1.3)])
        discs = VGroup(*[Line(P2(z, ys - 1.0), P2(z, ys + 1.0), color=GRAYTXT, stroke_width=3) for z in (z1, z2)])
        phi = ValueTracker(0.0)

        def mpos(z, sg):
            return P2(z, ys + sg * r * np.cos(phi.get_value()))

        d1 = always_redraw(lambda: Dot(mpos(z1, 1), radius=0.13, color=C1))
        d2 = always_redraw(lambda: Dot(mpos(z2, -1), radius=0.13, color=C2))
        l1 = always_redraw(lambda: M(r"m_1", 24, C1).next_to(mpos(z1, 1), LEFT, buff=0.15))
        l2 = always_redraw(lambda: M(r"m_2", 24, C2).next_to(mpos(z2, -1), RIGHT, buff=0.15))

        def farrow(z, sg, col, L=0.9, base_on_mass=True):
            def f():
                c = np.cos(phi.get_value())
                if abs(c) < 0.1:
                    return VMobject()
                b = mpos(z, sg) if base_on_mass else P2(z, ys)
                return vec(b, b + UP * L * sg * c, col, sw=5, tip=0.18)
            return always_redraw(f)

        f1 = farrow(z1, 1, C1)
        f2 = farrow(z2, -1, C2)
        rL = farrow(-6.2, -1, WARN, L=0.7, base_on_mass=False)
        rR = farrow(-1.3, 1, WARN, L=0.7, base_on_mass=False)
        f1l = M(r"m_1R_1\omega^2", 24, C1).next_to(P2(z1, ys + r + 0.9), RIGHT, buff=0.1)
        f2l = M(r"m_2R_2\omega^2", 24, C2).next_to(P2(z2, ys - r - 0.9), RIGHT, buff=0.1)
        dim = DoubleArrow(P2(z1, 1.25), P2(z2, 1.25), buff=0, color=WHITE, stroke_width=2, tip_length=0.12)
        ext = VGroup(*[DashedLine(P2(z, ys + 1.05), P2(z, 1.35), color=GRAYTXT, stroke_width=1.5) for z in (z1, z2)])
        dl = M("d", 26).next_to(dim, UP, buff=0.06)
        cpl = Arc(radius=0.5, start_angle=150 * DEGREES, angle=-120 * DEGREES, arc_center=P2((z1 + z2) / 2, ys),
                  color=WARN, stroke_width=4)
        cpl.add_tip(tip_length=0.15, tip_width=0.15)
        cl = M("C", 26, WARN).move_to(P2((z1 + z2) / 2, ys - 0.62))
        # end-view inset
        ci = P2(-5.75, 1.45)
        inset_c = Circle(radius=0.55, color=SHAFT, stroke_width=2).move_to(ci)

        def ipos(sg):
            a = phi.get_value()
            return ci + sg * 0.42 * np.array([-np.sin(a), np.cos(a), 0.0])

        i1 = always_redraw(lambda: Dot(ipos(1), radius=0.08, color=C1))
        i2 = always_redraw(lambda: Dot(ipos(-1), radius=0.08, color=C2))
        ilab = T("มองจากปลายเพลา", 16, GRAYTXT).next_to(inset_c, DOWN, buff=0.1)
        sv_lab = T("มองด้านข้าง", 16, GRAYTXT).move_to(P2(-3.75, -2.75))

        self.play(Create(shaft), FadeIn(brg), Create(discs), FadeIn(sv_lab), run_time=1.0)
        self.add(d1, d2, l1, l2)
        self.play(FadeIn(inset_c), FadeIn(ilab))
        self.add(i1, i2)
        p2 = panel(
            T("ทำไม static ไม่พอ (หน้า 12)", 22, OK),
            T("m₁R₁ = m₂R₂ ชี้ตรงข้ามกัน แต่อยู่คนละตำแหน่งตามแกน", 19),
            M(r"\sum F = m_1R_1\omega^2 - m_2R_2\omega^2 = 0\ \checkmark", 30, OK),
            M(r"C = (m_1R_1\omega^2)\,d \neq 0", 32, WARN),
            T("สมดุลแรง แต่ไม่สมดุลโมเมนต์ → เพลาส่าย", 20, WARN),
            T("แบริ่งรับแรงสลับทิศทุกรอบ (ลูกศรส้ม)", 19, GRAYTXT),
            T("มวลถ่วงก้อนเดียวแก้ couple ไม่ได้ → ต้องใช้ 2 ระนาบ", 19, GRAYTXT))
        self.play(FadeIn(p2[0]), FadeIn(p2[1]))
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(f1l), FadeIn(f2l))
        self.play(FadeIn(p2[2]))
        self.glow(p2[2], VGroup(f1, f2, inset_c), OK)
        self.play(Create(ext), GrowFromCenter(dim), FadeIn(dl), Create(cpl), FadeIn(cl))
        self.play(FadeIn(p2[3]))
        self.glow(p2[3], VGroup(dim, dl, cpl, cl, f1), WARN)
        self.play(FadeIn(p2[4]))
        self.say("ให้เพลาหมุน: แรงเหวี่ยงคู่นี้หมุนตามไปด้วย แบริ่งสองข้างโดนกระชากสลับทิศทุกรอบ")
        self.play(FadeOut(f1l), FadeOut(f2l), run_time=0.3)
        self.add(rL, rR)
        self.play(phi.animate.set_value(2 * TAU), run_time=7.0, rate_func=linear)
        self.play(FadeIn(p2[5]), FadeIn(p2[6]))
        self.wait(2.0)

        # ---------------- part 3: two planes
        fig2 = VGroup(shaft, brg, discs, ext, dim, dl, cpl, cl, inset_c, ilab, sv_lab)
        self.say("ทางแก้: เติมมวลถ่วงบน 2 ระนาบ A และ B — มวลไม่สมดุลกี่ก้อนก็ใช้ 2 ระนาบพอ (หน้า 13–14)")
        self.play(FadeOut(fig2), FadeOut(VGroup(d1, d2, l1, l2, f1, f2, rL, rR, i1, i2)), FadeOut(p2), run_time=0.5)
        self.remove(d1, d2, l1, l2, f1, f2, rL, rR, i1, i2)
        ms = [(1.2, 1.135, 113.4, 0.854), (1.8, 0.822, 48.8, 1.701), (2.4, 1.04, 251.4, 2.396)]
        sv = self.side_view(ms, 3.097, None)
        self.play(Create(sv["shaft"]), Create(sv["pA"]), Create(sv["pB"]), FadeIn(sv["lA"]), FadeIn(sv["lB"]),
                  Create(sv["discs"]), FadeIn(sv["dots"]), FadeIn(sv["mlabs"]), run_time=1.4)
        self.play(FadeIn(sv["dims"]), FadeIn(sv["dlabs"]))
        p3 = panel(
            T("Dynamic (two-plane) balance — 2 เงื่อนไข", 22, OK),
            vrow(M(r"l_A = 0", 28, CA), T("ทุกระยะ l วัดจากระนาบ A", 19)),
            T("1) แรงรวม = 0", 20),
            M(r"\sum m_i\vec R_i + m_A\vec R_A + m_B\vec R_B = 0", 30),
            T("2) โมเมนต์รอบระนาบ A = 0", 20),
            M(r"\sum m_i\vec R_i\,l_i + m_B\vec R_B\,l_B = 0", 30),
            vrow(M(r"m_A\vec R_A\,l_A = 0", 28, CA), T("หายจากสมการ 2 → หา B ก่อน แล้วค่อย A", 19, WARN)),
            x0=0.35, top=2.1)
        self.play(FadeIn(p3[0]), FadeIn(p3[1]))
        self.glow(p3[1][0], VGroup(sv["pA"], sv["lA"]), CA)
        self.play(FadeIn(p3[2]), FadeIn(p3[3]))
        self.glow(p3[3], VGroup(sv["dots"], sv["pA"], sv["pB"]), WHITE)
        self.play(FadeIn(p3[4]), FadeIn(p3[5]))
        self.glow(p3[5], VGroup(sv["dims"], sv["dlabs"]), WHITE)
        self.play(FadeIn(p3[6]))
        self.glow(p3[6][0], VGroup(sv["pA"], sv["lA"]), CA)
        self.wait(2.0)

        # ---------------- part 4: 4-step procedure
        ev = self.end_view(ms)
        pj = self.projection(ev, ms, 0)
        self.say("มุมมองตามแกน: แตก R เป็น R_x = R cos θ, R_y = R sin θ (θ วัดจากแกน x ทวนเข็ม)")
        self.play(FadeIn(ev["disk"]), Create(ev["ax"]), FadeIn(ev["axl"]), *[GrowArrow(a) for a in ev["vecs"]],
                  FadeIn(ev["rlabs"]), Create(ev["arcs"]), run_time=1.4)
        self.play(Create(pj[:4]), FadeIn(pj[4:]))
        self.wait(1.0)
        p4 = panel(
            T("4 ขั้นทำข้อสอบ two-plane", 22, OK),
            T("1 เข้าใจ: จด m, R, θ, l ทุกมวล — A ที่ l = 0, แปลง mm → m", 19),
            T("2 สูตร/ตาราง: mRx, mRy, mRx·l, mRy·l แล้วรวมคอลัมน์", 19),
            vrow(M(r"m_BR_{Bx} = -\frac{\sum m_iR_{ix}l_i}{l_B}", 30, CB), T("(แกน y: เปลี่ยน x → y)", 18, GRAYTXT)),
            vrow(M(r"m_AR_{Ax} = -\sum m_iR_{ix} - m_BR_{Bx}", 30, CA), T("(แกน y เหมือนกัน)", 18, GRAYTXT)),
            T("3 แทนค่า: B ก่อน (โมเมนต์รอบ A) แล้ว A (แรงรวม)", 19),
            M(r"mR = \sqrt{(mR_x)^2 + (mR_y)^2},\qquad \theta = \tan^{-1}\frac{mR_y}{mR_x}", 28),
            T("4 ตรวจ: แรงรวม = 0, โมเมนต์ = 0, quadrant ของมุม, หน่วย kg·m", 19),
            x0=0.35, top=2.1, gap=0.17)
        self.say("สรุป 4 ขั้นที่ใช้ทุกข้อ — คลิปถัดไปทำตัวอย่างสไลด์หน้า 19–21 ด้วยวิธีตาราง")
        self.play(FadeOut(p3), run_time=0.35)
        self.play(FadeIn(p4[0]), FadeIn(p4[1]))
        self.glow(p4[1], VGroup(sv["dims"], ev["arcs"]), WHITE)
        self.play(FadeIn(p4[2]))
        self.glow(p4[2], pj, C1)
        self.play(FadeIn(p4[3]))
        self.glow(p4[3], VGroup(sv["pB"], sv["lB"], sv["dims"][3], sv["dlabs"][3]), CB)
        self.play(FadeIn(p4[4]))
        self.glow(p4[4], VGroup(sv["pA"], sv["lA"]), CA)
        self.play(FadeIn(p4[5]))
        self.play(FadeIn(p4[6]))
        self.glow(p4[6], VGroup(ev["vecs"], ev["arcs"]), WHITE)
        self.play(FadeIn(p4[7]))
        self.wait(4.0)


# =====================================================================
# B41 -- lecture example p.19-21, table method
# =====================================================================
LECT = dict(
    ms=[("1.2", "1.135", "113.4", "0.854"), ("1.8", "0.822", "48.8", "1.701"), ("2.4", "1.04", "251.4", "2.396")],
    lB="3.097", r=None,
    say0="ตัวอย่างสไลด์หน้า 19: มวลไม่สมดุล 3 ก้อน — หา mR ที่ต้องเติมบนระนาบ A และ B",
    say1="ขั้น 1 เข้าใจโจทย์: จด m, R, θ, l ทุกมวล — A อยู่ที่ l = 0, B อยู่ที่ l_B = 3.097 m",
    note1="ไม่ให้รัศมีมวลถ่วง → ตอบเป็น mR (kg·m) ทั้งสองระนาบ",
    say2="ขั้น 2 ตาราง: ทีละแถว mR_x = m R cos θ, mR_y = m R sin θ แล้วคูณ l อีกที",
    say_quad="x บวก y ลบ → Quadrant 4: เครื่องคิดเลขให้ −81.35° (= 278.65°) ใช้ได้เลย",
    angA_str=r"-81.35^\circ\ (278.65^\circ)",
    trap="กับดัก: ลืมเครื่องหมายลบ → มวลถ่วงไปฝั่งผิด / tan⁻¹ ต้องเลือก quadrant เอง",
)

PRAC = dict(
    ms=[("2.0", "0.10", "0", "0.20"), ("3.0", "0.08", "120", "0.40"), ("2.5", "0.12", "210", "0.65")],
    lB="0.80", r="0.10", proj=1,
    say0="โจทย์ฝึก: วาดรูปก่อน — มุมมองข้าง (ระยะ l จากระนาบ A) และมุมมองตามแกน (มุม θ)",
    say1="ขั้น 1: แปลง mm → m ทุกตัว, A ที่ l = 0, B ที่ l_B = 0.80 m, มวลถ่วงที่รัศมี 0.10 m",
    note1="รู้รัศมีมวลถ่วง r = 0.10 m → ตอบเป็นมวล m = (mR)/r",
    say2="ขั้น 2 ตาราง: mR_x = m R cos θ, mR_y = m R sin θ แล้วคูณ l — ระวังเครื่องหมายของ cos/sin",
    say_quad="x ลบ y ลบ → Quadrant 3: tan⁻¹ ได้ 61.42° ต้องบวก 180° = 241.42°",
    angA_str=r"241.42^\circ",
    trap="กับดัก: tan⁻¹ ของเครื่องคิดเลขไม่รู้ quadrant — (−,−) ต้อง +180°",
)


class B41_ExamTwoPlaneTable(ExamScene):
    def construct(self):
        self.add(title("Two-plane balancing: วิธีตาราง (ตัวอย่างสไลด์)", size=28),
                 page_ref("สไลด์หน้า 19-21"))
        self.worked_example(LECT)


# =====================================================================
# B42 -- self-made practice problem as a drill
# =====================================================================
class B42_ExamTwoPlanePractice(ExamScene):
    def construct(self):
        self.add(title("Two-plane balancing: โจทย์ฝึกทำเอง", size=28),
                 page_ref("โจทย์ฝึกในโน้ต W10"))
        q = panel(
            T("โจทย์ฝึก (แต่งเอง) — ลองทำเองก่อนดูเฉลย", 24, OK),
            M(r"m_1 = 2.0\ \text{kg},\ \ r_1 = 100\ \text{mm}\ \text{@}\ 0^\circ,\ \ l_1 = 200\ \text{mm}", 32, C1),
            M(r"m_2 = 3.0\ \text{kg},\ \ r_2 = 80\ \text{mm}\ \text{@}\ 120^\circ,\ \ l_2 = 400\ \text{mm}", 32, C2),
            M(r"m_3 = 2.5\ \text{kg},\ \ r_3 = 120\ \text{mm}\ \text{@}\ 210^\circ,\ \ l_3 = 650\ \text{mm}", 32, C3),
            T("ระยะ l วัดจากระนาบ A, ระนาบ A–B ห่างกัน 800 mm", 21),
            T("ติดมวลถ่วงที่รัศมี 100 mm ทั้งสองระนาบ", 21),
            M(r"\text{find: } m_A,\ \theta_A,\ m_B,\ \theta_B", 34, WARN),
            T("หยุดคลิปตรงนี้ แล้วลองทำ 4 ขั้นเอง", 22, WARN),
            x0=-5.6, top=2.0, gap=0.3, max_w=11.0)
        self.say("โจทย์ฝึกแต่งเอง ตัวเลขไม่ซ้ำสไลด์ — ทำครบ 4 ขั้นแบบตอนสอบจริง")
        self.play(FadeIn(q), run_time=1.2)
        self.wait(5.0)
        self.play(FadeOut(q), run_time=0.4)
        self.worked_example(PRAC)
