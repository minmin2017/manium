"""
Transformer teaching clip — power flow through primary → flux → secondary
Demonstrates voltage step-up/down and current relationships
"""

from mlib import *

class TransformerPrimary(SafeScene):
    """Clip 1: Electrical power at primary coil"""

    def construct(self):
        # Transformer outline
        primary_coil = self.draw_coil(LEFT * 2.5, n_turns=5, color=RED)
        secondary_coil = self.draw_coil(RIGHT * 2.5, n_turns=8, color=RED)
        secondary_coil.set_opacity(0.3)
        core = Line(DOWN * 2, UP * 2, color=GRAY, stroke_width=8)

        transformer = VGroup(primary_coil, secondary_coil, core)
        self.add(transformer)

        # Primary labels
        v1_label = MathTex("V_1", color=RED).next_to(primary_coil, UP, buff=0.3)
        i1_label = MathTex("I_1", color=YELLOW).next_to(primary_coil, DOWN, buff=0.3)

        self.play(FadeIn(v1_label), FadeIn(i1_label))
        self.wait(0.5)

        # Power equation
        power_eq = MathTex(
            r"P_1 = V_1 \times I_1",
            color=WHITE,
            font_size=48
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(power_eq, shift=DOWN * 0.3))
        self.wait(2)

        # Show actual values (illustrative)
        v1_val = DecimalNumber(230, num_decimal_places=0, color=RED).next_to(v1_label, DOWN, buff=0.2)
        i1_val = DecimalNumber(10, num_decimal_places=0, color=YELLOW).next_to(i1_label, UP, buff=0.2)
        unit_v = Text("V", font_size=20, color=RED).next_to(v1_val, RIGHT, buff=0.1)
        unit_i = Text("A", font_size=20, color=YELLOW).next_to(i1_val, RIGHT, buff=0.1)

        self.play(FadeIn(v1_val), FadeIn(i1_val), FadeIn(unit_v), FadeIn(unit_i))
        self.wait(1)

        # Calculate and show power
        p1_result = MathTex(r"P_1 = 2300 \, W", color=WHITE, font_size=40).to_edge(DOWN, buff=1)
        self.play(FadeIn(p1_result, shift=UP * 0.3))
        self.wait(2)

    def draw_coil(self, center, n_turns=5, color=RED, radius=0.4):
        """Draw a multi-turn coil"""
        coil = VGroup()
        for i in range(n_turns):
            y_offset = (i - n_turns/2 + 0.5) * 0.3
            circle = Circle(radius=radius, color=color)
            circle.move_to(center + UP * y_offset)
            coil.add(circle)
        return coil


class TransformerFlux(SafeScene):
    """Clip 2: Magnetic flux through the core"""

    def construct(self):
        # Full transformer (faded)
        primary_coil = self.draw_coil(LEFT * 2.5, n_turns=5, color=RED)
        primary_coil.set_opacity(0.3)
        secondary_coil = self.draw_coil(RIGHT * 2.5, n_turns=8, color=RED)
        secondary_coil.set_opacity(0.3)
        core = Line(DOWN * 2, UP * 2, color=GRAY, stroke_width=8)
        core.set_opacity(0.3)

        transformer = VGroup(primary_coil, secondary_coil, core)
        self.add(transformer)

        # Highlight core
        core_bright = Line(DOWN * 2.2, UP * 2.2, color=GRAY, stroke_width=10)
        self.play(FadeIn(core_bright))

        # Flux arrow through core
        flux_arrow = arrow3(DOWN * 1.8, UP * 1.8, color=BLUE)
        self.play(FadeIn(flux_arrow))
        self.wait(0.5)

        # Flux equation
        flux_eq = MathTex(
            r"\Phi = \text{Φ through core (unchanged)}",
            color=BLUE,
            font_size=44
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(flux_eq, shift=DOWN * 0.3))
        self.wait(2)

        # Faraday's law
        faraday = MathTex(
            r"V \propto \frac{d\Phi}{dt}",
            color=WHITE,
            font_size=40
        ).to_edge(DOWN, buff=1)

        self.play(FadeIn(faraday, shift=UP * 0.3))
        self.wait(2)

    def draw_coil(self, center, n_turns=5, color=RED, radius=0.4):
        """Draw a multi-turn coil"""
        coil = VGroup()
        for i in range(n_turns):
            y_offset = (i - n_turns/2 + 0.5) * 0.3
            circle = Circle(radius=radius, color=color)
            circle.move_to(center + UP * y_offset)
            coil.add(circle)
        return coil


class TransformerVoltageRatio(SafeScene):
    """Clip 3: Voltage step-down relationship"""

    def construct(self):
        # Secondary coil highlight
        secondary_coil = self.draw_coil(ORIGIN, n_turns=8, color=RED, opacity=1.0)
        self.add(secondary_coil)

        # Turn ratio
        n_ratio = MathTex(
            r"\frac{N_1}{N_2} = \frac{5}{8}",
            color=WHITE,
            font_size=48
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(n_ratio))
        self.wait(1)

        # Voltage relationship
        voltage_rel = MathTex(
            r"V_2 = \frac{N_2}{N_1} \times V_1",
            color=RED,
            font_size=44
        ).shift(UP * 1.5)

        self.play(FadeIn(voltage_rel, shift=DOWN * 0.3))
        self.wait(1)

        # Numerical example
        v1_example = MathTex(r"V_1 = 230 \, V", color=RED, font_size=40).shift(DOWN * 0.5)
        v2_example = MathTex(r"V_2 = \frac{8}{5} \times 230 = 368 \, V", color=RED, font_size=40).shift(DOWN * 1.5)

        self.play(FadeIn(v1_example))
        self.wait(0.5)
        self.play(FadeIn(v2_example))
        self.wait(2)

    def draw_coil(self, center, n_turns=5, color=RED, radius=0.4):
        """Draw a multi-turn coil"""
        coil = VGroup()
        for i in range(n_turns):
            y_offset = (i - n_turns/2 + 0.5) * 0.3
            circle = Circle(radius=radius, color=color)
            circle.move_to(center + UP * y_offset)
            coil.add(circle)
        return coil


class TransformerCurrentInverse(SafeScene):
    """Clip 4: Current relationship (power conservation)"""

    def construct(self):
        # Simple representation
        title = MathTex(r"\text{Power Conservation: } P_1 = P_2", color=WHITE, font_size=48).to_edge(UP, buff=0.5)
        self.add(title)

        # Power at primary
        p1 = MathTex(r"P_1 = V_1 \times I_1 = 230 \times 10 = 2300 \, W", color=WHITE, font_size=40).shift(UP * 1)
        self.play(FadeIn(p1))
        self.wait(1)

        # Power at secondary
        p2_eq = MathTex(r"P_2 = V_2 \times I_2 = 368 \times I_2", color=WHITE, font_size=40).shift(DOWN * 0.5)
        self.play(FadeIn(p2_eq))
        self.wait(1)

        # Set equal
        equal = MathTex(r"2300 = 368 \times I_2", color=YELLOW, font_size=40).shift(DOWN * 2)
        self.play(FadeIn(equal))
        self.wait(0.5)

        # Solve for I2
        i2_result = MathTex(r"I_2 = \frac{2300}{368} \approx 6.25 \, A", color=YELLOW, font_size=40).shift(DOWN * 3)
        self.play(FadeIn(i2_result))
        self.wait(2)

        # Current ratio summary
        summary = MathTex(r"\frac{I_1}{I_2} = \frac{N_2}{N_1}", color=YELLOW, font_size=44).to_edge(DOWN, buff=1)
        self.play(FadeIn(summary, shift=UP * 0.3))
        self.wait(2)
