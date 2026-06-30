from manim import *

BG     = "#0f0f1a"
C_BAD  = "#e74c3c"
C_GOOD = "#27ae60"
C_AVG  = "#f0a500"

IMG_BAD  = "/home/minmin/Downloads/notHave_Breakfast"
IMG_GOOD = "/home/minmin/Downloads/Eat_rice_in_time"


class BreakfastSlides(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self._two_lifestyles()
        self._nine_circles()
        self._achievements()

    def _clear(self, rt=0.9):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects.copy()], run_time=rt)

    # ── Scene 1: Two Lifestyles ───────────────────────────────────────────
    def _two_lifestyles(self):
        title = Text("Two Lifestyles", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title, run_time=0.9))

        # Images
        img_bad  = ImageMobject(IMG_BAD).scale_to_fit_height(4.2)
        img_good = ImageMobject(IMG_GOOD).scale_to_fit_height(4.2)
        img_bad.shift(LEFT * 3.4 + DOWN * 0.2)
        img_good.shift(RIGHT * 3.4 + DOWN * 0.2)

        # Divider + VS
        divider = Line(UP * 2.6, DOWN * 3.0, color=GREY_B, stroke_width=2)
        vs = Text("VS", font_size=38, weight=BOLD, color=GREY_A)
        vs.move_to(ORIGIN + DOWN * 0.2)

        # Labels
        lbl_bad = Text("Skip Breakfast", font_size=22, color=C_BAD, weight=BOLD)
        lbl_bad.next_to(img_bad, DOWN, buff=0.25)
        lbl_good = Text("Eat on Time", font_size=22, color=C_GOOD, weight=BOLD)
        lbl_good.next_to(img_good, DOWN, buff=0.25)

        # Outcome tags
        tag_bad  = Text("Shorter Healthspan", font_size=17, color=C_BAD)
        tag_bad.next_to(lbl_bad, DOWN, buff=0.12)
        tag_good = Text("Longer Healthspan", font_size=17, color=C_GOOD)
        tag_good.next_to(lbl_good, DOWN, buff=0.12)

        self.play(
            FadeIn(img_bad,  shift=RIGHT * 0.3),
            FadeIn(img_good, shift=LEFT  * 0.3),
            run_time=1.2,
        )
        self.play(Create(divider), FadeIn(vs))
        self.play(FadeIn(lbl_bad), FadeIn(lbl_good))
        self.play(FadeIn(tag_bad), FadeIn(tag_good))
        self.wait(3)
        self._clear()

    # ── Scene 2: 9 Circles – effects of skipping breakfast ────────────────
    def _nine_circles(self):
        title = Text("Skipping Breakfast: What Research Shows",
                     font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        src_note = Text("Sources: JACC 2019 · Harvard HSPH · Frontiers Endocrinology 2023 · PMC 2023",
                        font_size=13, color=GREY_C)
        src_note.to_edge(DOWN, buff=0.2)

        self.play(Write(title, run_time=1.0), FadeIn(src_note))

        # 9 data points (name, stat, detail)
        data = [
            ("Cardiovascular\nDisease Death",  "+87%",  "vs daily breakfast eaters"),
            ("Heart Attack\n(Men)",             "+27%",  "Harvard cohort study"),
            ("All-Cause\nMortality",            "+32%",  "pooled prospective studies"),
            ("Metabolic\nSyndrome",             "+10%",  "9 studies · 118,385 people"),
            ("Type 2\nDiabetes",               "Higher", "insulin resistance & glucose spike"),
            ("Obesity &\nOverweight",           "Higher", "leptin/ghrelin dysregulation"),
            ("GI & Colorectal\nCancer",        "Elevated","Kailuan cohort · 500K+ people"),
            ("Bone Fracture /\nOsteoporosis",  "+18%",  "skipping >3x per week"),
            ("Poor Focus\n& Mood",             "Daily",  "low glucose · cortisol surge"),
        ]

        RADIUS = 0.88
        circles = VGroup()
        for name, stat, detail in data:
            circ = Circle(
                radius=RADIUS,
                color=C_BAD, stroke_width=2.5,
                fill_color="#1e0a0a", fill_opacity=0.95,
            )
            name_txt = Text(name, font_size=13, color=WHITE, line_spacing=1.25)
            name_txt.move_to(circ.get_center() + UP * 0.3)
            stat_txt = Text(stat, font_size=18, color=C_BAD, weight=BOLD)
            stat_txt.move_to(circ.get_center() + DOWN * 0.25)
            group = VGroup(circ, name_txt, stat_txt)
            circles.add(group)

        circles.arrange_in_grid(rows=3, cols=3, buff=0.42)
        circles.next_to(title, DOWN, buff=0.45)

        # scale down if too tall
        # title is above src_note → title_bottom_y > src_note_top_y in Manim coords
        available_h = title.get_bottom()[1] - src_note.get_top()[1] - 0.9
        if circles.height > available_h > 0:
            circles.scale_to_fit_height(available_h)

        for circ in circles:
            self.play(GrowFromCenter(circ), run_time=0.28)

        self.wait(4)
        self._clear()

    # ── Scene 3: Achievement System ───────────────────────────────────────
    def _achievements(self):
        title = Text("Your Lifestyle Achievements", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title, run_time=1.0))

        R = 0.72  # fixed circle radius — all badges the same size

        def make_badge(label, color, fill):
            """Badge = circle + centred label. Fixed radius R."""
            circ = Circle(radius=R, color=color, stroke_width=2.5,
                          fill_color=fill, fill_opacity=0.92)
            lbl = Text(label, font_size=14, color=WHITE, line_spacing=1.25)
            lbl.move_to(circ.get_center())
            # wrap together using a fixed phantom rectangle so all bounding
            # boxes are identical (prevents arrange_in_grid size drift)
            phantom = Square(side_length=R * 2, stroke_width=0, fill_opacity=0)
            phantom.move_to(circ.get_center())
            return VGroup(phantom, circ, lbl)

        bad_labels = [
            "Heart\nDisease", "Type 2\nDiabetes", "Obesity",
            "Fatigue\nAll Day", "Poor\nFocus", "Bone\nFracture",
        ]
        good_labels = [
            "Sharp\nMind", "Full\nEnergy", "Strong\nHeart",
            "Healthy\nWeight", "Great\nMood", "Long\nHealthspan",
        ]

        bad_grid = VGroup(*[
            make_badge(lbl, C_BAD, "#2a0808") for lbl in bad_labels
        ]).arrange_in_grid(rows=2, cols=3, buff=0.28)

        good_grid = VGroup(*[
            make_badge(lbl, C_GOOD, "#082a10") for lbl in good_labels
        ]).arrange_in_grid(rows=2, cols=3, buff=0.28)

        bad_header = VGroup(
            Text("PATH: Skip Breakfast", font_size=20, color=C_BAD, weight=BOLD),
            Text("Achievements Unlocked:", font_size=15, color=GREY_A),
        ).arrange(DOWN, buff=0.08)

        good_header = VGroup(
            Text("PATH: Eat on Time", font_size=20, color=C_GOOD, weight=BOLD),
            Text("Achievements Unlocked:", font_size=15, color=GREY_A),
        ).arrange(DOWN, buff=0.08)

        # Stack header + grid per column
        bad_col  = VGroup(bad_header,  bad_grid ).arrange(DOWN, buff=0.35)
        good_col = VGroup(good_header, good_grid).arrange(DOWN, buff=0.35)

        # Place columns side by side, centred vertically
        cols = VGroup(bad_col, good_col).arrange(RIGHT, buff=1.2)
        cols.next_to(title, DOWN, buff=0.45)

        # Scale down if too tall for the frame
        max_h = 5.8
        if cols.height > max_h:
            cols.scale(max_h / cols.height)

        # Center divider between columns
        mid_x = (bad_col.get_right()[0] + good_col.get_left()[0]) / 2
        divider = Line(
            [mid_x, title.get_bottom()[1] - 0.2, 0],
            [mid_x, -3.6, 0],
            color=GREY_D, stroke_width=1.5,
        )

        conclusion = Text(
            "The choice is yours — what will you unlock?",
            font_size=22, color=C_AVG, weight=BOLD,
        )
        conclusion.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(bad_header, shift=RIGHT * 0.2),
                  FadeIn(good_header, shift=LEFT * 0.2))
        self.play(Create(divider))

        for b, g in zip(bad_grid, good_grid):
            self.play(GrowFromCenter(b), GrowFromCenter(g), run_time=0.32)

        self.play(FadeIn(conclusion, shift=UP * 0.2))
        self.wait(4)
        self._clear()
