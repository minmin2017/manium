from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = "#0f0f1a"
C_SLEEP = "#6c5ce7"
C_NUT   = "#00b894"
C_STR   = "#e17055"
C_SMK   = "#636e72"
C_EXR   = "#fdcb6e"
C_REL   = "#fd79a8"
C_GOLD  = "#f0a500"
WHITE_A = "#dfe6e9"


def _chapter_badge(text, color):
    rect = RoundedRectangle(
        corner_radius=0.18, width=3.2, height=0.56,
        fill_color=color, fill_opacity=0.25,
        stroke_color=color, stroke_width=1.5,
    )
    lbl = Text(text, font_size=18, color=color, weight=BOLD)
    lbl.move_to(rect)
    return VGroup(rect, lbl)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ═══════════════════════════════════════════════════════════════════════════════
class Slide01Sleep(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        arc = Arc(radius=1.6, start_angle=PI * 0.15, angle=PI * 1.7,
                  color=C_SLEEP, stroke_width=4)
        arc.shift(UP * 0.55)

        stars = VGroup()
        for px, py in [(-2.8,2.3),(2.5,2.6),(-1.5,3.1),(3.2,1.2),
                       (-3.5,1.0),(1.0,3.4),(-4.0,2.8),(4.2,2.2),
                       (-0.5,3.6),(2.9,0.8),(-2.2,1.6)]:
            stars.add(Dot(radius=0.05, color=WHITE, fill_opacity=0.75).move_to([px,py,0]))

        main_title = Text("เรื่องของการนอน", font_size=62, weight=BOLD, color=C_SLEEP)
        main_title.move_to(ORIGIN)

        subtitle = Text(
            "Sleep · Nutrition · Stress · Toxins · Exercise · Relationships",
            font_size=21, color=WHITE_A,
        )
        subtitle.next_to(main_title, DOWN, buff=0.55)

        tagline = Text("6 ปัจจัยที่กำหนดคุณภาพชีวิตของคุณ",
                       font_size=24, color=C_GOLD)
        tagline.next_to(subtitle, DOWN, buff=0.32)

        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in stars],
                               lag_ratio=0.06, run_time=1.4))
        self.play(Create(arc), run_time=1.2)
        self.play(Write(main_title, run_time=1.8))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.play(FadeIn(tagline, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — โภชนาการ
# ═══════════════════════════════════════════════════════════════════════════════
class Slide02Nutrition(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        badge = _chapter_badge("02 / โภชนาการ", C_NUT)
        badge.to_corner(UL, buff=0.4)
        title = Text("โภชนาการกับการนอนหลับ", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(FadeIn(badge), Write(title, run_time=1.0))

        items = [
            ("ผักใบเขียว",   0.88, C_NUT),
            ("ธัญพืชไม่ขัด", 0.75, C_NUT),
            ("ปลาน้ำเงิน",   0.82, C_NUT),
            ("น้ำตาลสูง",    0.25, C_STR),
            ("แอลกอฮอล์",   0.20, C_STR),
            ("คาเฟอีน >3PM", 0.15, C_STR),
        ]

        bar_w = 0.80
        gap   = 0.28
        max_h = 3.2
        base_y = -1.55
        start_x = -(len(items) * (bar_w + gap) - gap) / 2 + bar_w / 2

        bars = VGroup()
        lbls = VGroup()
        vals = VGroup()

        for i, (name, ratio, color) in enumerate(items):
            h = ratio * max_h
            x = start_x + i * (bar_w + gap)
            bar = Rectangle(
                width=bar_w, height=h,
                fill_color=color, fill_opacity=0.85, stroke_width=0,
            ).move_to([x, base_y + h / 2, 0])
            lname = Text(name, font_size=14, color=WHITE_A)
            lname.next_to(bar, DOWN, buff=0.14)
            pct = Text(f"{int(ratio*100)}%", font_size=15, color=color, weight=BOLD)
            pct.next_to(bar, UP, buff=0.10)
            bars.add(bar); lbls.add(lname); vals.add(pct)

        baseline = Line(LEFT*4.2, RIGHT*4.2, color=GREY_C, stroke_width=1.5)
        baseline.move_to([0, base_y, 0])
        axis_lbl = Text("คุณภาพการนอน →", font_size=14, color=GREY_B)
        axis_lbl.next_to(baseline, LEFT, buff=0.1).rotate(PI/2).shift(LEFT*0.1)

        self.play(Create(baseline), FadeIn(axis_lbl), run_time=0.6)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                               lag_ratio=0.12, run_time=2.2))
        self.play(
            LaggedStart(*[FadeIn(l) for l in lbls], lag_ratio=0.06),
            LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.06),
            run_time=0.9,
        )

        note = Text("✦  กินอาหารหนักก่อนนอน < 3 ชม. ลด sleep latency ได้ 30%",
                    font_size=18, color=C_NUT)
        note.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(note, shift=UP*0.15))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — ความเครียด
# ═══════════════════════════════════════════════════════════════════════════════
class Slide03Stress(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        badge = _chapter_badge("03 / ความเครียด", C_STR)
        badge.to_corner(UL, buff=0.4)
        title = Text("ความเครียดฆ่าการนอน", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(FadeIn(badge), Write(title, run_time=1.0))

        axes = Axes(
            x_range=[0, 24, 4], y_range=[0, 1.4, 0.4],
            x_length=10, y_length=3.6,
            axis_config={"color": GREY_C, "include_tip": False,
                         "label_constructor": Text},
            x_axis_config={"numbers_to_include": list(range(0, 25, 4))},
            y_axis_config={"numbers_to_include": []},
        ).shift(DOWN * 0.4)

        xl = Text("ชั่วโมงของวัน (0 = เที่ยงคืน)", font_size=15, color=GREY_B)
        xl.next_to(axes.x_axis, DOWN, buff=0.42)
        yl = Text("ระดับคอร์ติซอล", font_size=15, color=GREY_B)
        yl.rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.42)

        self.play(Create(axes, run_time=0.9), FadeIn(xl), FadeIn(yl))

        def c_normal(t):
            return 0.85 * np.exp(-0.5 * ((t-8)/3.5)**2) + 0.08

        def c_stressed(t):
            return (0.85 * np.exp(-0.5*((t-8)/3.5)**2)
                  + 0.55 * np.exp(-0.5*((t-15)/2.5)**2)
                  + 0.48 * np.exp(-0.5*((t-22)/2.0)**2)
                  + 0.12)

        curve_n = axes.plot(c_normal,  x_range=[0,24], color=C_NUT, stroke_width=3.5)
        curve_s = axes.plot(c_stressed, x_range=[0,24], color=C_STR, stroke_width=3.5)

        lbl_n = Text("ปกติ", font_size=19, color=C_NUT, weight=BOLD)
        lbl_n.next_to(axes.c2p(8, 0.85), UP, buff=0.16)
        lbl_s = Text("เครียดเรื้อรัง", font_size=19, color=C_STR, weight=BOLD)
        lbl_s.next_to(axes.c2p(22, c_stressed(22)), UP, buff=0.16)

        sleep_area = axes.get_area(
            axes.plot(lambda t: 0.32, x_range=[21,24]),
            x_range=[21,24], color=C_SLEEP, opacity=0.20,
        )
        sleep_lbl = Text("ช่วงนอน", font_size=14, color=C_SLEEP)
        sleep_lbl.next_to(axes.c2p(22.5, 0.32), UP, buff=0.12)

        self.play(Create(curve_n), FadeIn(lbl_n), run_time=2.0)
        self.play(Create(curve_s), FadeIn(lbl_s), run_time=2.2)
        self.play(FadeIn(sleep_area), FadeIn(sleep_lbl))

        note = Text("✦  คอร์ติซอลสูงตอนกลางคืน → นอนไม่หลับ + ตื่นกลางดึก",
                    font_size=18, color=C_STR)
        note.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(note, shift=UP*0.15))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — บุหรี่ & สารพิษ
# ═══════════════════════════════════════════════════════════════════════════════
class Slide04Smoking(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        badge = _chapter_badge("04 / บุหรี่ & สารพิษ", C_SMK)
        badge.to_corner(UL, buff=0.4)
        title = Text("สารพิษขัดขวางการซ่อมแซมร่างกาย", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(FadeIn(badge), Write(title, run_time=1.0))

        def make_hyp(pts, color, y_off):
            verts = [[x*1.15 - 4.6, p*0.65 - 2.0 + y_off, 0] for x, p in pts]
            return VMobject(color=color, stroke_width=3.0).set_points_as_corners(verts)

        pts_norm = [(0,0),(0.3,3.5),(1.0,4.0),(1.5,2.5),(2.0,1.0),
                    (2.5,1.5),(3.0,4.0),(3.5,3.0),(4.0,2.0),(4.5,2.5),
                    (5.0,4.0),(5.5,3.5),(6.0,4.0),(6.5,2.5),(7.0,0)]
        pts_smk  = [(0,0),(0.5,1.5),(1.0,2.5),(1.5,2.0),(2.0,2.5),
                    (2.5,0),(3.0,2.0),(3.3,0),(3.7,1.5),(4.2,0),
                    (4.5,1.5),(5.0,2.5),(5.5,2.0),(6.0,2.5),(7.0,0)]

        hyp_n = make_hyp(pts_norm, C_NUT,  0.65)
        hyp_s = make_hyp(pts_smk,  C_STR, -1.25)

        stage_labels = VGroup(*[
            Text(s, font_size=13, color=GREY_B).move_to([-5.4, i*0.65-0.65, 0])
            for i, s in enumerate(["N3","N2","N1","REM","ตื่น"])
        ])

        lbl_n = Text("ปกติ", font_size=17, color=C_NUT, weight=BOLD)
        lbl_n.to_corner(UL, buff=0.4).shift(DOWN*1.3)
        lbl_s = Text("สูบบุหรี่ / แอลกอฮอล์", font_size=17, color=C_STR, weight=BOLD)
        lbl_s.to_corner(UL, buff=0.4).shift(DOWN*2.9)

        self.play(Create(hyp_n, run_time=2.2), FadeIn(lbl_n), FadeIn(stage_labels))
        self.play(Create(hyp_s, run_time=2.2), FadeIn(lbl_s))

        stats = VGroup(
            Text("↓ REM ลดลง 28%",             font_size=20, color=C_STR, weight=BOLD),
            Text("↑ ตื่นกลางดึก เพิ่มขึ้น 2×", font_size=20, color=C_STR, weight=BOLD),
            Text("↓ SWS ฟื้นฟูร่างกาย ลด 40%", font_size=20, color=C_STR, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        stats.to_edge(RIGHT, buff=0.55).shift(DOWN*0.25)
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT*0.2) for s in stats],
                               lag_ratio=0.25, run_time=1.6))

        note = Text("✦  เลิกบุหรี่ 1 สัปดาห์ → REM กลับมาใกล้ปกติ",
                    font_size=18, color=C_GOLD)
        note.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(note, shift=UP*0.15))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — การออกกำลังกาย
# ═══════════════════════════════════════════════════════════════════════════════
class Slide05Exercise(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        badge = _chapter_badge("05 / การออกกำลังกาย", C_EXR)
        badge.to_corner(UL, buff=0.4)
        title = Text("ออกกำลังกาย = ยานอนหลับธรรมชาติ", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(FadeIn(badge), Write(title, run_time=1.0))

        benefits = [
            ("🏃", "Aerobic\n30 นาที/วัน",  "+65%\nSWS",          C_EXR),
            ("🏋", "Weight\nTraining",        "+25%\nSleep time",   C_EXR),
            ("🧘", "Yoga /\nStretching",      "↓ cortisol\n35%",   C_NUT),
            ("⚠️",  "ออกก่อนนอน\n< 1 ชม.",  "อาจนอนยาก\n↑ HR",   C_STR),
        ]

        cards = VGroup()
        for icon, label, value, color in benefits:
            bg = RoundedRectangle(
                corner_radius=0.24, width=2.95, height=2.65,
                fill_color=color, fill_opacity=0.13,
                stroke_color=color, stroke_width=1.8,
            )
            ic  = Text(icon,  font_size=32).move_to(bg).shift(UP*0.72)
            lbl = Text(label, font_size=17, color=WHITE_A, line_spacing=1.3)
            lbl.move_to(bg).shift(UP*0.06)
            val = Text(value, font_size=21, color=color, weight=BOLD, line_spacing=1.2)
            val.move_to(bg).shift(DOWN*0.72)
            cards.add(VGroup(bg, ic, lbl, val))

        cards.arrange(RIGHT, buff=0.36).shift(DOWN*0.38)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.3, scale=0.88) for c in cards],
                               lag_ratio=0.18, run_time=2.4))

        note = Text("✦  ออกกำลังกาย 150 นาที/สัปดาห์ ลดความเสี่ยง Insomnia ได้ 55%",
                    font_size=18, color=C_EXR)
        note.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(note, shift=UP*0.15))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — ความสัมพันธ์
# ═══════════════════════════════════════════════════════════════════════════════
class Slide06Relationships(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        badge = _chapter_badge("06 / ความสัมพันธ์", C_REL)
        badge.to_corner(UL, buff=0.4)
        title = Text("ความสัมพันธ์ที่ดี = นอนหลับดีขึ้น", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(FadeIn(badge), Write(title, run_time=1.0))

        topics = [
            ("ครอบครัว",     C_REL, UP*1.95 + LEFT*0.5),
            ("เพื่อน",       C_REL, UP*1.1  + RIGHT*2.5),
            ("คู่รัก",       C_GOLD, RIGHT*3.0 + DOWN*0.2),
            ("ชุมชน",        C_NUT,  DOWN*1.75 + RIGHT*1.5),
            ("สัตว์เลี้ยง",  C_EXR,  DOWN*1.75 + LEFT*1.5),
            ("เพื่อนร่วมงาน",C_REL,  LEFT*3.0 + DOWN*0.2),
        ]

        center = Dot(radius=0.32, color=WHITE, fill_opacity=0.14,
                     stroke_color=WHITE, stroke_width=2.2)
        center.move_to(DOWN*0.15)
        ctxt = Text("คุณ", font_size=18, color=WHITE, weight=BOLD)
        ctxt.move_to(center)

        nodes = VGroup(); lines = VGroup(); node_lbs = VGroup()
        for name, color, offset in topics:
            nd = Dot(radius=0.20, color=color, fill_opacity=0.88)
            nd.move_to(DOWN*0.15 + offset*0.85)
            ln = Line(center.get_center(), nd.get_center(),
                      color=color, stroke_width=2.0, stroke_opacity=0.55)
            lb = Text(name, font_size=17, color=color, weight=BOLD)
            lb.next_to(nd, normalize(offset), buff=0.16)
            nodes.add(nd); lines.add(ln); node_lbs.add(lb)

        self.play(FadeIn(center), FadeIn(ctxt))
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1, run_time=1.4))
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.1),
            LaggedStart(*[FadeIn(l) for l in node_lbs], lag_ratio=0.1),
            run_time=1.2,
        )

        stats = VGroup(
            Text("♥  ความเหงา ≈ สูบบุหรี่ 15 มวน/วัน",     font_size=17, color=C_REL),
            Text("♥  Oxytocin จากความอบอุ่น → หลับเร็วขึ้น", font_size=17, color=C_REL),
            Text("♥  Social support ลด cortisol กลางคืน 29%",font_size=17, color=C_REL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        stats.to_edge(DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.15) for s in stats],
                               lag_ratio=0.2, run_time=1.5))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
