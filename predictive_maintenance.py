from manim import *
import numpy as np
from scipy.optimize import curve_fit

Text.set_default(font="Noto Sans Thai")

# ── Color Palette ─────────────────────────────────────────────────────────────
OK_GREEN    = "#66BB6A"
FAIL_RED    = "#EF5350"
WARN_YELLOW = "#FFD54F"
GRAY_MID    = "#90A4AE"
GRAY_DARK   = "#546E7A"
BLUE_LIGHT  = "#4FC3F7"
ORANGE      = "#FFA726"

# ── Raw failure rate per 10-min wear bin (AI4I 2020 dataset) ──────────────────
RAW_DATA = [
    (5,   0.024), (15,  0.021), (25,  0.026), (35,  0.017),
    (45,  0.022), (55,  0.013), (65,  0.035), (75,  0.017),
    (85,  0.022), (95,  0.024), (105, 0.026), (115, 0.028),
    (125, 0.018), (135, 0.013), (145, 0.028), (155, 0.018),
    (165, 0.025), (175, 0.021), (185, 0.031), (195, 0.038),
    (205, 0.123), (215, 0.154), (225, 0.208), (235, 0.323),
]

# ── Raw crossing wear (interpolated from actual data) ─────────────────────────
def raw_cross_wear(level):
    for (w1, r1), (w2, r2) in zip(RAW_DATA, RAW_DATA[1:]):
        if r1 <= level <= r2:
            return w1 + (level - r1) / (r2 - r1) * (w2 - w1)
    return None

RAW_W17 = raw_cross_wear(0.17)  # ≈ 218 min (has 205, 215 in rising zone)
RAW_W20 = raw_cross_wear(0.20)  # ≈ 223 min
RAW_W25 = raw_cross_wear(0.25)  # ≈ 229 min

# ── Fit logistic to data from wear=0 up to each threshold ────────────────────
def _logistic(w, L, k, w0):
    return L / (1.0 + np.exp(-k * (w - w0)))

def fit_ode_up_to(wear_limit):
    """Fit logistic using all raw data with wear <= wear_limit."""
    sub = [(w, r) for w, r in RAW_DATA if w <= wear_limit]
    ws = np.array([w for w, r in sub])
    rs = np.array([r for w, r in sub])
    try:
        popt, _ = curve_fit(_logistic, ws, rs, p0=[0.5, 0.06, 215], maxfev=10000)
    except Exception:
        popt = [0.5, 0.06, 215]
    return popt  # (L, k, w0)

PARAMS_17 = fit_ode_up_to(RAW_W17)
PARAMS_20 = fit_ode_up_to(RAW_W20)
PARAMS_25 = fit_ode_up_to(RAW_W25)

def ode_line(params, start_wear, end_wear=252, step=2):
    L, k, w0 = params
    return [(w, min(_logistic(w, L, k, w0), 0.48))
            for w in np.arange(start_wear, end_wear, step)]


class PredictiveMaintenance(Scene):
    def construct(self):
        self.intro()
        self.show_axes_and_data()
        self.mark_threshold()
        self.ode_prediction()
        self.outro()

    # ── helpers ───────────────────────────────────────────────────────────────
    def _header(self, text, color=WHITE):
        h = Text(text, font_size=32, color=color)
        h.to_edge(UP, buff=0.3)
        line = Line(LEFT * 6.5, RIGHT * 6.5, color=color,
                    stroke_width=1.2).next_to(h, DOWN, buff=0.12)
        return VGroup(h, line)

    def _make_axes(self):
        ax = Axes(
            x_range=[0, 255, 50],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=4.5,
            axis_config={"color": GRAY_MID, "stroke_width": 2,
                         "include_tip": True, "tip_length": 0.18},
            x_axis_config={"numbers_to_include": [0, 50, 100, 150, 200, 250]},
            y_axis_config={"numbers_to_include": [0, 0.1, 0.2, 0.3, 0.4, 0.5]},
        ).shift(DOWN * 0.5)
        x_lbl = Text("Tool Wear (min)", font_size=22, color=GRAY_MID)
        x_lbl.next_to(ax.x_axis, DOWN, buff=0.35)
        y_lbl = Text("Failure Rate", font_size=22, color=GRAY_MID)
        y_lbl.next_to(ax.y_axis, LEFT, buff=0.15).rotate(PI / 2)
        return ax, x_lbl, y_lbl

    def _make_line(self, ax, data, color, stroke_width=3):
        pts = [ax.c2p(w, min(r, 0.48)) for w, r in data]
        curve = VMobject(color=color, stroke_width=stroke_width)
        curve.set_points_smoothly(pts)
        dots = VGroup(*[Dot(p, color=color, radius=0.06) for p in pts])
        return curve, dots

    def _h_dashed(self, ax, level, color, lbl_text, stroke_width=2, dash_length=0.12):
        line = DashedLine(ax.c2p(0, level), ax.c2p(260, level),
                          color=color, stroke_width=stroke_width,
                          dash_length=dash_length)
        lbl = Text(lbl_text, font_size=18, color=color)
        lbl.next_to(ax.c2p(255, level), RIGHT, buff=0.05)
        return line, lbl

    # ── Scene 1 : Intro ───────────────────────────────────────────────────────
    def intro(self):
        title = Text("Predictive Maintenance", font_size=52, color=WHITE)
        sub   = Text("AI4I Dataset — Tool Wear vs Failure Rate", font_size=28,
                     color=GRAY_MID)
        VGroup(title, sub).arrange(DOWN, buff=0.4)

        bullets = VGroup(
            Text("① แสดงข้อมูลจริงจาก Dataset", font_size=24, color=BLUE_LIGHT),
            Text("② หยุดที่จุด 10% failure", font_size=24, color=WARN_YELLOW),
            Text("③ ODE ทำนายตั้งแต่เริ่มต้น — ทีละ threshold", font_size=24, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 1.3)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bullets],
                               lag_ratio=0.4))
        self.wait(2)
        self.play(FadeOut(VGroup(title, sub, bullets)))

    # ── Scene 2 : Axes + Known Data ───────────────────────────────────────────
    def show_axes_and_data(self):
        self.hdr = self._header("① ข้อมูลจริงจาก AI4I Dataset", color=BLUE_LIGHT)
        self.play(FadeIn(self.hdr, shift=DOWN * 0.2))

        ax, xl, yl = self._make_axes()
        self.ax = ax
        self.play(Create(ax), Write(xl), Write(yl), run_time=1.2)
        self.xl, self.yl = xl, yl

        ds_note = Text("10,000 records · CNC Milling · Synthetic (UCI AI4I 2020)",
                       font_size=17, color=GRAY_DARK).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(ds_note))

        line, dots = self._make_line(ax, RAW_DATA, OK_GREEN)
        self.play(Create(line), run_time=3.0)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.04), run_time=1.2)
        self.bars_known = VGroup(line, dots)
        self.ds_note = ds_note
        self.wait(1)

    # ── Scene 3 : 10% Threshold ───────────────────────────────────────────────
    def mark_threshold(self):
        ax = self.ax
        self.play(FadeOut(self.hdr))
        self.hdr = self._header("② threshold — สัญญาณเตือน", color=WARN_YELLOW)
        self.play(FadeIn(self.hdr, shift=DOWN * 0.2))

        # Horizontal lines at 17%, 20%, 25%
        thresh_line, thresh_lbl = self._h_dashed(ax, 0.17, WARN_YELLOW, "17%")
        line_20, lbl_20 = self._h_dashed(ax, 0.20, GRAY_MID, "20%",
                                          stroke_width=1.2, dash_length=0.10)
        line_25, lbl_25 = self._h_dashed(ax, 0.25, GRAY_MID, "25%",
                                          stroke_width=1.2, dash_length=0.10)

        self.play(Create(thresh_line), Write(thresh_lbl))
        self.play(Create(line_20), Write(lbl_20), Create(line_25), Write(lbl_25))
        self.ref_lines = VGroup(line_20, lbl_20, line_25, lbl_25)

        # 17% crossing — vertical + dot
        now_line = DashedLine(
            ax.c2p(RAW_W17, 0), ax.c2p(RAW_W17, 0.45),
            color=WHITE, stroke_width=1.5, dash_length=0.15,
        )
        now_lbl = Text(f"wear ≈ {RAW_W17:.0f} min\n(ข้อมูลที่รู้)", font_size=18, color=WHITE)
        now_lbl.next_to(ax.c2p(RAW_W17, 0.45), UP, buff=0.08)

        cross_dot = Dot(ax.c2p(RAW_W17, 0.17), color=WARN_YELLOW, radius=0.12)

        self.play(Create(now_line), Write(now_lbl))
        self.play(FadeIn(cross_dot, scale=1.5))

        call = Text(f"⚠  wear ≈ {RAW_W17:.0f} min\n    fail rate ข้าม 17%!",
                    font_size=20, color=WARN_YELLOW)
        call.move_to(ax.c2p(100, 0.40))
        self.play(FadeIn(call, scale=0.8))
        self.wait(2)
        self.play(FadeOut(call))

        self.thresh_line = thresh_line
        self.thresh_lbl  = thresh_lbl
        self.now_line    = now_line
        self.now_lbl     = now_lbl
        self.cross_dot   = cross_dot

    # ── Scene 4 : 3 Adaptive ODE curves ──────────────────────────────────────
    def ode_prediction(self):
        ax = self.ax
        self.play(FadeOut(self.hdr))
        self.hdr = self._header("③ Adaptive ODE — ยิ่งมีข้อมูลมาก ยิ่งแม่น", color=ORANGE)
        self.play(FadeIn(self.hdr, shift=DOWN * 0.2))

        all_curves = VGroup()

        def make_dashed(params, start_wear, color):
            pts = [ax.c2p(w, r) for w, r in ode_line(params, start_wear)]
            if len(pts) < 2:
                return None
            curve = VMobject(color=color, stroke_width=3)
            curve.set_points_smoothly(pts)
            return DashedVMobject(curve, num_dashes=30, dashed_ratio=0.55)

        def show_ode(params, start_w, level, color, lbl_text, lbl_pos):
            d = make_dashed(params, start_w, color)
            if d is None:
                return d
            lbl = Text(lbl_text, font_size=17, color=color)
            lbl.move_to(lbl_pos)

            # dot + drop at crossing level from actual data
            cross_w = raw_cross_wear(level)
            dot  = Dot(ax.c2p(cross_w, level), color=color, radius=0.10)
            drop = DashedLine(ax.c2p(cross_w, 0), ax.c2p(cross_w, level),
                              color=color, stroke_width=1.4, dash_length=0.09)
            w_lbl = Text(f"wear≈{cross_w:.0f}min", font_size=15, color=color)
            w_lbl.next_to(dot, UP, buff=0.13)

            self.play(Create(d), run_time=1.8)
            self.play(Write(lbl), Create(drop), FadeIn(dot, scale=1.4))
            self.play(Write(w_lbl))
            self.wait(5)
            self.play(FadeOut(VGroup(lbl, drop, dot, w_lbl)))
            all_curves.add(d)
            return d

        c10 = show_ode(PARAMS_17, RAW_W17, 0.17, WARN_YELLOW,
                       "ODE① fit wear 0→17%",
                       ax.c2p(230, 0.46))
        c20 = show_ode(PARAMS_20, RAW_W20, 0.20, ORANGE,
                       "ODE② fit wear 0→20%",
                       ax.c2p(235, 0.40))
        c25 = show_ode(PARAMS_25, RAW_W25, 0.25, FAIL_RED,
                       "ODE③ fit wear 0→25%",
                       ax.c2p(235, 0.34))

        # Show all 3 together with legend
        legend = VGroup(
            Text("① ODE fit ถึง 17%", font_size=17, color=WARN_YELLOW),
            Text("② ODE fit ถึง 20%", font_size=17, color=ORANGE),
            Text("③ ODE fit ถึง 25%", font_size=17, color=FAIL_RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.move_to(ax.c2p(65, 0.42))
        self.play(FadeIn(legend))

        call = Text("ยิ่ง fit ข้อมูลมาก → slope แม่นขึ้น → predict แม่นขึ้น",
                    font_size=19, color=WHITE)
        call.move_to(ax.c2p(100, 0.12))
        self.play(FadeIn(call, scale=0.8))
        self.wait(3)
        self.play(FadeOut(call), FadeOut(legend))

        self.dashed_pred = all_curves
        self.ode_lbl     = VGroup()

    # ── Scene 5 : Outro ───────────────────────────────────────────────────────
    def outro(self):
        self.play(FadeOut(VGroup(
            self.hdr, self.ax, self.xl, self.yl,
            self.bars_known, self.thresh_line, self.thresh_lbl,
            self.ref_lines, self.now_line, self.now_lbl, self.cross_dot,
            self.dashed_pred, self.ode_lbl, self.ds_note,
        )))

        msg = Text("Predictive Maintenance", font_size=46, color=WHITE)
        pts = VGroup(
            Text("✅ Failure rate แบนราบ ~2-4% จนถึง wear≈202 min", font_size=22,
                 color=OK_GREEN),
            Text("⚠  wear > 200 min → cliff พุ่งขึ้นทันที (12-32%)", font_size=22,
                 color=WARN_YELLOW),
            Text("📈 ODE ทาย trend ได้ แต่จริงชันกว่าที่ model คาด", font_size=22,
                 color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(DOWN * 0.6)

        self.play(Write(msg))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pts], lag_ratio=0.5))
        self.wait(3)
        self.play(FadeOut(VGroup(msg, pts)))
