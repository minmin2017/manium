"""A compact F1 engineering explainer: energy, aero, tyres, and braking."""

from mlib import *

BG = "#10131B"
CAR = "#E10600"
AIR = "#54C7FF"
ENERGY = "#FFD54F"
BRAKE = "#FF7043"
TYRE = "#ECEFF1"


def label(text, point, color=WHITE, size=19):
    return Text(text, font_size=size, color=color).move_to(point)


def f1_car(scale=1.0):
    """Simple top-view schematic; it teaches force flow, not exact body geometry."""
    floor = RoundedRectangle(width=7.0, height=0.9, corner_radius=0.23,
                             color=CAR, fill_opacity=1, stroke_width=0)
    nose = Polygon([3.45, 0.0, 0], [2.25, 0.34, 0], [2.25, -0.34, 0],
                   color=CAR, fill_opacity=1, stroke_width=0)
    cockpit = Ellipse(width=1.55, height=0.65, color="#263238",
                      fill_opacity=1, stroke_width=0).move_to([-0.35, 0, 0])
    rear = Rectangle(width=0.20, height=2.05, color=CAR, fill_opacity=1,
                     stroke_width=0).move_to([-3.10, 0, 0])
    front = Rectangle(width=0.18, height=2.35, color=CAR, fill_opacity=1,
                      stroke_width=0).move_to([3.05, 0, 0])
    wheels = VGroup(*[
        RoundedRectangle(width=0.52, height=0.93, corner_radius=0.16,
                         color=TYRE, fill_opacity=0.95, stroke_width=0)
        .move_to(p)
        for p in ((2.0, 1.0, 0), (2.0, -1.0, 0), (-2.25, 0.93, 0), (-2.25, -0.93, 0))
    ])
    car = VGroup(floor, nose, cockpit, rear, front, wheels)
    return car.scale(scale)


class F1EngineeringExplainer(SafeScene):
    def construct(self):
        self.camera.background_color = BG
        heading = title("How an F1 Car Works — Engineering", color=WHITE, size=32)
        sub = caption_top("It is an energy machine that turns airflow into tyre grip.", size=22)
        car = f1_car(0.82).move_to([-1.0, -0.25, 0])
        self.play(FadeIn(heading, shift=UP*0.35), FadeIn(sub, shift=UP*0.25),
                  FadeIn(car, shift=LEFT*0.4), run_time=0.8)
        self.wait(1.0)

        # 1. Power path
        engine = RoundedRectangle(width=1.35, height=0.72, corner_radius=0.12,
                                 color=CAR, fill_opacity=0.85).move_to([-1.75, -0.25, 0])
        battery = RoundedRectangle(width=1.05, height=0.72, corner_radius=0.12,
                                  color=ENERGY, fill_opacity=0.85).move_to([-0.35, -0.25, 0])
        gearbox = RoundedRectangle(width=1.15, height=0.72, corner_radius=0.12,
                                  color=OK, fill_opacity=0.85).move_to([1.1, -0.25, 0])
        e1 = label("V6 engine", engine.get_center(), BLACK, 18)
        e2 = label("ERS battery", battery.get_center(), BLACK, 18)
        e3 = label("gearbox", gearbox.get_center(), BLACK, 18)
        chain = VGroup(
            Arrow(engine.get_right(), battery.get_left(), buff=0.08, color=ENERGY, stroke_width=5),
            Arrow(battery.get_right(), gearbox.get_left(), buff=0.08, color=ENERGY, stroke_width=5),
            Arrow(gearbox.get_right(), [3.0, -0.25, 0], buff=0.06, color=ENERGY, stroke_width=5),
        )
        power_cap = caption_top("1) Combustion + electric energy combine at the drivetrain.", color=ENERGY, size=21)
        self.play(FadeOut(car), FadeOut(sub), FadeIn(engine, shift=LEFT*0.3), FadeIn(battery),
                  FadeIn(gearbox, shift=RIGHT*0.3), FadeIn(e1), FadeIn(e2), FadeIn(e3),
                  LaggedStart(*[GrowArrow(a) for a in chain], lag_ratio=0.18), FadeIn(power_cap), run_time=1.1)
        self.wait(1.2)

        # 2. Aero force
        self.play(FadeOut(Group(engine, battery, gearbox, e1, e2, e3, chain, power_cap)), run_time=0.45)
        car = f1_car(0.88).move_to([-1.2, -0.35, 0])
        airflow = VGroup(*[
            Arrow([x, y, 0], [x+1.05, y, 0], color=AIR, buff=0, stroke_width=3)
            for x in (-5.9, -4.3, -2.7, -1.1, 0.5, 2.1, 3.7)
            for y in (1.35, 0.68, -1.38)
        ])
        down = VGroup(
            Arrow([-1.9, 1.55, 0], [-1.9, 0.6, 0], color=FORCE, buff=0, stroke_width=6),
            Arrow([1.1, 1.55, 0], [1.1, 0.6, 0], color=FORCE, buff=0, stroke_width=6),
        )
        aero_formula = MathTex(r"F_{down} = \frac{1}{2}\rho v^2 A C_L", color=FORCE).scale(0.75).move_to([3.7, 0.2, 0])
        aero_words = label("wings + floor\nshape the flow", [3.7, -0.85, 0], AIR, 20)
        aero_cap = caption_top("2) Faster air makes more downforce — pressing the car into the track.", color=FORCE, size=20)
        self.play(FadeIn(car, shift=LEFT*0.35), LaggedStart(*[GrowArrow(a) for a in airflow], lag_ratio=0.04),
                  GrowArrow(down[0]), GrowArrow(down[1]), FadeIn(aero_formula, shift=RIGHT*0.25),
                  FadeIn(aero_words), FadeIn(aero_cap), run_time=1.3)
        self.wait(1.3)

        # 3. Tyres are the interface
        self.play(FadeOut(Group(airflow, down, aero_formula, aero_words, aero_cap)), run_time=0.45)
        contact = VGroup(*[Dot(w.get_bottom(), radius=0.09, color=ENERGY) for w in car[-1]])
        friction = VGroup(
            Arrow([-2.8, -2.0, 0], [-0.3, -2.0, 0], color=ENERGY, buff=0, stroke_width=6),
            Arrow([-2.8, -1.73, 0], [-0.3, -1.73, 0], color=ENERGY, buff=0, stroke_width=2),
        )
        grip_eq = MathTex(r"F_{grip} \leq \mu N", color=ENERGY).scale(0.9).move_to([3.8, 0.2, 0])
        grip_words = label("Downforce raises N\nso tyres can corner harder.", [3.75, -0.85, 0], TYRE, 20)
        grip_cap = caption_top("3) Tyres convert downforce into cornering, braking, and acceleration force.", color=ENERGY, size=20)
        self.play(FadeIn(contact), LaggedStart(*[GrowArrow(a) for a in friction], lag_ratio=0.15),
                  FadeIn(grip_eq), FadeIn(grip_words), FadeIn(grip_cap), run_time=1.0)
        self.wait(1.15)

        # 4. Braking energy recovery and active aero
        self.play(FadeOut(Group(contact, friction, grip_eq, grip_words, grip_cap)), run_time=0.4)
        brake_wheels = VGroup(*[
            Circle(radius=0.18, color=BRAKE, fill_opacity=0.8, stroke_width=0).move_to(w.get_center())
            for w in car[-1]
        ])
        regen = Arrow([-1.8, -1.45, 0], [-0.35, -1.45, 0], color=ENERGY, buff=0, stroke_width=6)
        regen_text = label("brake heat + wheel motion → electrical energy", [1.7, -1.45, 0], ENERGY, 18)
        wings = VGroup(
            Line([1.3, 1.65, 0], [2.5, 1.88, 0], color=AIR, stroke_width=7),
            Line([1.3, 1.42, 0], [2.5, 1.60, 0], color=AIR, stroke_width=7),
        )
        mode = label("Corner: high downforce\nStraight: low drag", [3.65, 0.65, 0], AIR, 19)
        close = caption_top("4) Braking recovers energy; active wings trade drag for cornering grip.", color=BRAKE, size=20)
        self.play(FadeIn(brake_wheels), GrowArrow(regen), FadeIn(regen_text),
                  Create(wings), FadeIn(mode), FadeIn(close), run_time=1.0)
        self.play(Indicate(brake_wheels, color=BRAKE, scale_factor=1.2),
                  wings.animate.rotate(-12*DEGREES, about_point=wings.get_center()), run_time=0.8)
        self.wait(1.0)

        # Summary
        self.play(FadeOut(Group(car, brake_wheels, regen, regen_text, wings, mode, close, heading)), run_time=0.55)
        final = Text("F1 performance = power + aero + tyres + control", font_size=31, color=WHITE)
        final.move_to([0, 0.45, 0])
        line = Text("Every system must work together for one fast lap.", font_size=23, color=GRAYTXT).next_to(final, DOWN, buff=0.36)
        self.play(FadeIn(final, shift=UP*0.3), FadeIn(line, shift=UP*0.2), run_time=0.75)
        self.wait(1.4)
