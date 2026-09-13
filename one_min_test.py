from manim import *
class OneMinTest(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        s = Square(color=RED)
        self.add(c, s)
        for _ in range(7):
            self.play(Rotate(c, PI), Rotate(s, PI/2), run_time=4.0, rate_func=linear)
            self.play(Rotate(c, PI), Rotate(s, -PI/2), run_time=4.0, rate_func=linear)
        self.wait(4)
