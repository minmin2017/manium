from manim import *

FONTS = [
    ("Prompt",    "#FF8A65"),
    ("Kanit",     "#4FC3F7"),
    ("Anuphan",   "#66BB6A"),
]

SAMPLE_TH = "ทำนายความเสียหาย ก่อนเกิดเหตุ"


class FontCompare(Scene):
    def construct(self):
        title = Text("ตัวกลม โมเดิร์น — เลือกได้เลย!", font="Prompt",
                     font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.35)
        self.add(title)

        rows = VGroup()
        for fname, color in FONTS:
            label = Text(f"◀  {fname}", font="Prompt", font_size=20, color=GRAY_B)
            th    = Text(SAMPLE_TH, font=fname, font_size=30, color=color)
            en    = Text("Predictive Maintenance  ①②③", font=fname, font_size=22, color=color)
            col   = VGroup(label, th, en).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            rows.add(col)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.52)
        rows.next_to(title, DOWN, buff=0.4)
        rows.to_edge(LEFT, buff=0.8)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.55)
            self.wait(0.3)
        self.wait(4)
