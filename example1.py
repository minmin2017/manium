from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.5)
        square = Square(color=RED, fill_opacity=0.5)

        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(1)
        self.play(FadeOut(circle))


class WritingEquation(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0", font_size=96)
        self.play(Write(eq))
        self.wait(2)


class MovingDot(Scene):
    def construct(self):
        dot = Dot(color=YELLOW).shift(LEFT * 3)
        path = TracedPath(dot.get_center, stroke_color=YELLOW)
        self.add(path)
        self.play(dot.animate.shift(RIGHT * 6), run_time=2)
        self.play(dot.animate.shift(UP * 2), run_time=1)
        self.play(dot.animate.shift(LEFT * 6), run_time=2)
        self.wait()
