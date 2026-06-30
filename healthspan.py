from manim import *
import numpy as np

# ── Colour palette ───────────────────────────────────────────────────────────
BG     = "#0f0f1a"
C_BAD  = "#e74c3c"   # red   – unhealthy lifestyle
C_AVG  = "#f0a500"   # amber – average person
C_GOOD = "#27ae60"   # green – optimal health
C_LINE = "#95a5a6"   # grey  – morbidity threshold
THRESH = 40          # health % below which morbidity is "active"


# ── Health curve models ──────────────────────────────────────────────────────
def h_bad(age):
    """Unhealthy lifestyle: low peak, fast early decline."""
    if age <= 25:
        return 65 + (age - 20) * 0.6
    return max(65 * np.exp(-0.032 * (age - 25)), 0.0)


def h_avg(age):
    """Average person: slow decline, then steeper after 55."""
    if age <= 55:
        return 78 - (age - 20) * 0.12
    base = 78 - 35 * 0.12
    return max(base * np.exp(-0.038 * (age - 55)), 0.0)


def h_good(age):
    """Optimal health: high plateau, compression of morbidity after 72."""
    if age <= 72:
        return 93 - (age - 20) * 0.08
    base = 93 - 52 * 0.08
    return max(base * np.exp(-0.085 * (age - 72)), 0.0)


def cross_age(fn, lo=20.0, hi=90.0, step=0.2):
    """Return approximate age where fn first drops to or below THRESH."""
    a = lo
    while a < hi:
        if fn(a) <= THRESH:
            return a
        a += step
    return hi


# ── Scene ────────────────────────────────────────────────────────────────────
class HealthspanComparison(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._title()
        self._definitions()
        self._graph()
        self._stats()
        self._sources()

    # ── helpers ───────────────────────────────────────────────────────────
    def _clear(self, rt=0.9):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects.copy()], run_time=rt)

    # ── ACT 1 · Title ────────────────────────────────────────────────────
    def _title(self):
        t = Text("Lifespan  vs  Healthspan", font_size=52, weight=BOLD)
        s = Text(
            "How daily habits shape the quality\n"
            "— not just the length — of your life",
            font_size=24, color=GREY_A, line_spacing=1.5,
        )
        s.next_to(t, DOWN, buff=0.55)

        self.play(Write(t), run_time=1.8)
        self.play(FadeIn(s, shift=UP * 0.2))
        self.wait(2)
        self._clear()

    # ── ACT 2 · Definitions (bar-card visual) ────────────────────────────
    def _definitions(self):
        title = Text("Two Key Concepts", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title, run_time=1.0))

        BAR_W = 8.5   # total width = 100% (lifespan)
        BAR_H = 0.85
        LEFT_X = -BAR_W / 2   # left anchor in scene coords

        # ── Row 1: Lifespan (full bar, amber) ─────────────────────────────
        ls_bar = Rectangle(
            width=BAR_W, height=BAR_H,
            fill_color=C_AVG, fill_opacity=0.85, stroke_width=0,
        ).move_to([0, 1.3, 0])

        ls_lbl = Text("LIFESPAN", font_size=26, color=C_AVG, weight=BOLD)
        ls_lbl.next_to(ls_bar, LEFT, buff=0.25)

        ls_pct = Text("100%", font_size=24, color=WHITE, weight=BOLD)
        ls_pct.move_to(ls_bar.get_center())

        ls_def = Text("Total length of life  (birth → death)",
                      font_size=17, color=GREY_A)
        ls_def.next_to(ls_bar, DOWN, buff=0.14)

        self.play(FadeIn(ls_lbl), GrowFromEdge(ls_bar, LEFT), run_time=1.2)
        self.play(FadeIn(ls_pct), FadeIn(ls_def))
        self.wait(0.5)

        # ── Row 2: Healthspan (partial green) + Morbidity (red) ───────────
        tracker = ValueTracker(0.0)   # will animate to 0.75 then vary

        bar_y = -0.3    # y-centre of healthspan row
        left_x = LEFT_X  # constant; local copy for lambdas below

        def make_hs():
            v = tracker.get_value()
            w = max(BAR_W * v, 0.001)
            return Rectangle(
                width=w, height=BAR_H,
                fill_color=C_GOOD, fill_opacity=0.85, stroke_width=0,
            ).move_to([left_x + w / 2, bar_y, 0])

        def make_morb():
            v = tracker.get_value()
            w_hs = BAR_W * v
            w_m  = max(BAR_W - w_hs, 0.001)
            return Rectangle(
                width=w_m, height=BAR_H,
                fill_color=C_BAD, fill_opacity=0.45, stroke_width=0,
            ).move_to([left_x + w_hs + w_m / 2, bar_y, 0])

        def make_hs_pct():
            v = tracker.get_value()
            w = BAR_W * v
            return Text(f"{int(round(v * 100))}%",
                        font_size=24, color=WHITE, weight=BOLD,
                        ).move_to([left_x + w / 2, bar_y, 0])

        def make_morb_lbl():
            v = tracker.get_value()
            w_hs = BAR_W * v
            w_m  = BAR_W - w_hs
            txt = Text("Morbidity\nspan", font_size=14, color=WHITE,
                       line_spacing=1.2)
            txt.move_to([left_x + w_hs + w_m / 2, bar_y, 0])
            txt.set_opacity(min(1.0, w_m / 1.5))  # fade if bar too thin
            return txt

        hs_bar   = always_redraw(make_hs)
        morb_bar = always_redraw(make_morb)
        hs_pct   = always_redraw(make_hs_pct)
        morb_lbl = always_redraw(make_morb_lbl)

        hs_lbl = Text("HEALTHSPAN", font_size=26, color=C_GOOD, weight=BOLD)
        hs_lbl.next_to(ls_lbl, DOWN, buff=1.65)   # align with lifespan label

        hs_def = Text("Years lived in good physical and mental health",
                      font_size=17, color=GREY_A)
        hs_def.next_to([0, bar_y, 0], DOWN, buff=0.55)

        self.play(FadeIn(hs_lbl))
        self.add(hs_bar, morb_bar, hs_pct, morb_lbl)
        self.play(tracker.animate.set_value(0.75), run_time=1.8)
        self.play(FadeIn(hs_def))
        self.wait(0.8)

        # ── Animate healthspan "varying" ──────────────────────────────────
        vary_note = Text("Healthspan varies based on your lifestyle",
                         font_size=20, color=C_GOOD)
        vary_note.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(vary_note))

        self.play(tracker.animate.set_value(0.55), run_time=1.2)
        self.wait(0.4)
        self.play(tracker.animate.set_value(0.88), run_time=1.4)
        self.wait(0.4)
        self.play(tracker.animate.set_value(0.75), run_time=1.0)
        self.wait(1.5)

        self._clear()

    # ── ACT 3 · Graph ────────────────────────────────────────────────────
    def _graph(self):
        # Axes
        axes = Axes(
            x_range=[20, 91, 10],
            y_range=[0, 101, 20],
            x_length=10,
            y_length=5.0,
            axis_config={
                "color": GREY_C,
                "include_tip": False,
                "label_constructor": Text,
            },
            x_axis_config={"numbers_to_include": list(range(20, 91, 10))},
            y_axis_config={"numbers_to_include": [0, 20, 40, 60, 80, 100]},
        ).shift(DOWN * 0.4)

        xl = Text("Age (years)", font_size=20, color=GREY_B)
        xl.next_to(axes.x_axis, DOWN, buff=0.55)
        yl = Text("Health Function (%)", font_size=20, color=GREY_B)
        yl.rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.55)

        self.play(Create(axes, run_time=1.2), FadeIn(xl), FadeIn(yl))

        # Threshold dashed line
        thr_plot  = axes.plot(lambda a: THRESH, x_range=[20, 90], color=C_LINE)
        thr_dashed = DashedVMobject(thr_plot, num_dashes=25, dashed_ratio=0.55)
        thr_lbl = Text("Morbidity threshold (40%)", font_size=15, color=C_LINE)
        thr_lbl.next_to(axes.c2p(83, THRESH), UP, buff=0.1)

        self.play(Create(thr_dashed), FadeIn(thr_lbl))
        self.wait(0.4)

        # ── Average curve ─────────────────────────────────────────────────
        h_avg_label = Text("Average person", font_size=24, color=C_AVG, weight=BOLD)
        h_avg_label.to_corner(UL, buff=0.4)
        self.play(FadeIn(h_avg_label))

        c_avg = axes.plot(h_avg, x_range=[20, 90], color=C_AVG, stroke_width=3.5)
        lbl_avg = Text("Average", font_size=17, color=C_AVG, weight=BOLD)
        # position label near the middle of visible curve, above it
        lbl_avg.next_to(axes.c2p(40, h_avg(40)), UP, buff=0.18)

        self.play(Create(c_avg), run_time=2.2)
        self.play(FadeIn(lbl_avg))
        self.wait(0.6)
        self.play(FadeOut(h_avg_label))

        # ── Unhealthy curve ───────────────────────────────────────────────
        h_bad_label = Text("Unhealthy lifestyle", font_size=24, color=C_BAD, weight=BOLD)
        h_bad_label.to_corner(UL, buff=0.4)
        self.play(FadeIn(h_bad_label))

        c_bad = axes.plot(h_bad, x_range=[20, 90], color=C_BAD, stroke_width=3.5)
        lbl_bad = Text("Unhealthy", font_size=17, color=C_BAD, weight=BOLD)
        # position near peak of bad curve (age 25) but shifted right to avoid y-axis
        lbl_bad.next_to(axes.c2p(30, h_bad(30)), UP, buff=0.18)

        self.play(Create(c_bad), run_time=2.2)
        self.play(FadeIn(lbl_bad))
        self.wait(0.6)
        self.play(FadeOut(h_bad_label))

        # ── Optimal curve ─────────────────────────────────────────────────
        h_good_label = Text("Optimal health", font_size=24, color=C_GOOD, weight=BOLD)
        h_good_label.to_corner(UL, buff=0.4)
        self.play(FadeIn(h_good_label))

        c_good = axes.plot(h_good, x_range=[20, 90], color=C_GOOD, stroke_width=3.5)
        lbl_good = Text("Optimal", font_size=17, color=C_GOOD, weight=BOLD)
        # position at age 60 where good curve is clearly highest
        lbl_good.next_to(axes.c2p(60, h_good(60)), UP, buff=0.18)

        self.play(Create(c_good), run_time=2.2)
        self.play(FadeIn(lbl_good))
        self.wait(0.6)
        self.play(FadeOut(h_good_label))

        # ── Morbidity shaded areas ────────────────────────────────────────
        age_b = cross_age(h_bad)    # ≈ 40
        age_a = cross_age(h_avg)    # ≈ 71
        age_g = cross_age(h_good)   # ≈ 81

        a_bad  = axes.get_area(c_bad,  x_range=[age_b, 90], color=C_BAD,  opacity=0.18)
        a_avg  = axes.get_area(c_avg,  x_range=[age_a, 90], color=C_AVG,  opacity=0.18)
        a_good = axes.get_area(c_good, x_range=[age_g, 90], color=C_GOOD, opacity=0.18)

        self.play(FadeIn(a_bad), FadeIn(a_avg), FadeIn(a_good), run_time=1.2)

        # Summary box (bottom-left, away from curves)
        span_yrs_b = int(90 - age_b)
        span_yrs_a = int(90 - age_a)
        span_yrs_g = int(90 - age_g)

        span_box = VGroup(
            Text("Morbidity span:", font_size=17, color=GREY_A, weight=BOLD),
            Text(f"Unhealthy  ~{span_yrs_b} years", font_size=16, color=C_BAD),
            Text(f"Average    ~{span_yrs_a} years",  font_size=16, color=C_AVG),
            Text(f"Optimal    ~{span_yrs_g} years",  font_size=16, color=C_GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        span_box.to_corner(DL, buff=0.5)

        self.play(FadeIn(span_box, shift=RIGHT * 0.2))
        self.wait(3.5)
        self._clear()

    # ── ACT 4 · Statistics ───────────────────────────────────────────────
    def _stats(self):
        title = Text("What science says: lifestyle & healthspan",
                     font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.2)

        data = [
            (C_BAD,  "Smoking:",            "loses ~10 years of healthspan"),
            (C_BAD,  "Obesity:",            "loses 8-10 years of healthspan"),
            (C_BAD,  "Social isolation:",   "equivalent to smoking 15 cigarettes/day"),
            (C_BAD,  "Chronic stress:",     "accelerates telomere shortening"),
            (C_GOOD, "Regular exercise:",   "adds 7-10 years of healthspan"),
            (C_GOOD, "Quality sleep:",      "adds ~5-7 years; restores tissue & brain"),
            (C_GOOD, "Healthy diet:",       "cuts morbidity risk by up to 35%"),
            (C_GOOD, "Strong social ties:", "adds up to 15 years to healthy life"),
        ]

        rows = VGroup()
        for col, factor, effect in data:
            row = VGroup(
                Text("  ", font_size=20),  # spacer
                Text(factor, font_size=20, color=col, weight=BOLD),
                Text("  " + effect, font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.0, aligned_edge=DOWN)
            # replace spacer with colored bullet
            bullet = Dot(color=col, radius=0.07)
            bullet.next_to(row[1], LEFT, buff=0.2)
            rows.add(VGroup(bullet, row[1], row[2]))

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.next_to(title, DOWN, buff=0.45)
        rows.to_edge(LEFT, buff=0.8)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=0.4)

        self.wait(2.5)
        self._clear()

    # ── ACT 5 · Sources ──────────────────────────────────────────────────
    def _sources(self):
        title = Text("Sources", font_size=34, weight=BOLD, color=GREY_A)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        srcs = [
            "1.  Fries et al. (2011) — Compression of Morbidity.",
            "    The Milbank Quarterly, 89(2), 207-250.",
            "2.  Holt-Lunstad et al. (2015) — Loneliness and Social Isolation.",
            "    Perspectives on Psychological Science, 10(2), 227-237.",
            "3.  Lee et al. (2012) — Effect of physical inactivity on major NCDs",
            "    and life expectancy. The Lancet, 380(9838), 219-229.",
            "4.  WHO (2022) — Ageing and Health. WHO Fact Sheet.",
            "5.  Harvard Study of Adult Development (1938-ongoing); Vaillant (2012).",
            "6.  Epel et al. (2004) — Stress & telomere shortening. PNAS 101(49).",
        ]

        grp = VGroup(*[
            Text(s, font_size=16, color=GREY_B)
            for s in srcs
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        grp.next_to(title, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)

        self.play(FadeIn(grp, shift=UP * 0.3), run_time=1.5)
        self.wait(3.5)

        self.play(FadeOut(grp), FadeOut(title))

        outro = Text(
            "Every habit counts.",
            font_size=52, color=C_GOOD, weight=BOLD,
        )
        self.play(Write(outro), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(outro))
