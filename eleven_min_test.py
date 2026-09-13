"""11-Minute Real-World Benchmark Scene for Manim GPU NVENC.
Total duration: exactly 11 minutes (660 seconds).
Includes 11 distinct 60-second sections with continuous animation and motion.
"""
from manim import *

class ElevenMinuteVideoTest(Scene):
    def construct(self):
        self.camera.background_color = "#101216"

        header = Text("GPU NVENC Benchmark — 11-Minute Continuous Video", font_size=24, color=YELLOW)
        header.to_edge(UP, buff=0.4)
        self.add(header)

        for minute in range(1, 12):
            sec_title = Text(f"Section {minute} / 11 : Minute {minute:02d}:00", font_size=28, color=TEAL)
            sec_title.shift(UP * 1.8)
            
            circle = Circle(radius=1.5, color=BLUE).shift(LEFT * 2.5)
            square = Square(side_length=2.5, color=RED).shift(RIGHT * 2.5)
            dot = Dot(color=YELLOW).move_to(circle.get_top())

            self.play(FadeIn(sec_title), Create(circle), Create(square), FadeIn(dot), run_time=2.0)

            for _ in range(7):
                self.play(
                    Rotate(circle, angle=PI, about_point=circle.get_center()),
                    Rotate(square, angle=PI/2, about_point=square.get_center()),
                    dot.animate.shift(DOWN * 1.5),
                    run_time=4.0,
                    rate_func=linear
                )
                self.play(
                    Rotate(circle, angle=PI, about_point=circle.get_center()),
                    Rotate(square, angle=-PI/2, about_point=square.get_center()),
                    dot.animate.shift(UP * 1.5),
                    run_time=4.0,
                    rate_func=linear
                )

            self.play(FadeOut(sec_title), FadeOut(circle), FadeOut(square), FadeOut(dot), run_time=2.0)
