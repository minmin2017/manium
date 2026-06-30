from manim import *

Text.set_default(font="Noto Sans Thai")

BLUE_LIGHT = "#4FC3F7"
GREEN_ZONE = "#66BB6A"
RED_ZONE = "#EF5350"
GRAY_DARK = "#546E7A"
GRAY_MID = "#90A4AE"
YELLOW_TOOL = "#FFD54F"
ORANGE_TOOL = "#FFA726"


class CK40BOverview(Scene):
    def construct(self):
        self.intro()
        self.part1_machine_setup()
        self.part2_tool_offsets()
        self.part3_green_zone()
        self.outro()

    # ── INTRO ────────────────────────────────────────────────
    def intro(self):
        title = Text("CK40B Simulator", font_size=56, color=WHITE)
        sub = Text("ภาพรวมการใช้งาน 3 ส่วนหลัก", font_size=32, color=GRAY_MID)
        VGroup(title, sub).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        parts = VGroup(
            Text("① ตั้งค่าเครื่อง  (Machine Setup)", font_size=26, color=BLUE_LIGHT),
            Text("② ตั้งค่าหัวมีด  (Tool Offsets)", font_size=26, color=YELLOW_TOOL),
            Text("③ Green Zone คืออะไร?", font_size=26, color=GREEN_ZONE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(DOWN * 1.2)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in parts], lag_ratio=0.4))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, sub, parts)))

    # ── PART 1 : Machine Setup ───────────────────────────────
    def part1_machine_setup(self):
        header = self._part_header("① ตั้งค่าเครื่อง", color=BLUE_LIGHT)
        self.play(FadeIn(header, shift=DOWN * 0.3))
        self.wait(0.5)

        # ---- diagram (centred, nothing bleeds off screen) ----
        # Chuck
        chuck = Rectangle(width=1.0, height=2.2, fill_color=GRAY_DARK,
                          fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        chuck.move_to(LEFT * 3.5 + UP * 0.3)
        chuck_lbl = Text("Chuck", font_size=21, color=WHITE).next_to(chuck, LEFT, buff=0.15)

        # Jaws
        jaw_top = Rectangle(width=0.32, height=0.45, fill_color=GRAY_MID,
                             fill_opacity=1, stroke_width=1).move_to(
                             chuck.get_right() + LEFT * 0.16 + UP * 0.6)
        jaw_bot = jaw_top.copy().move_to(
                             chuck.get_right() + LEFT * 0.16 + DOWN * 0.6)

        # Workpiece
        wp = Rectangle(width=3.0, height=0.9, fill_color=BLUE_LIGHT,
                       fill_opacity=0.55, stroke_color=BLUE_LIGHT, stroke_width=2)
        wp.next_to(chuck, RIGHT, buff=0.0).align_to(chuck, UP).shift(DOWN * 0.65)
        wp_lbl = Text("Workpiece", font_size=21, color=BLUE_LIGHT).move_to(wp.get_center())

        # Slide table
        slide = Rectangle(width=5.2, height=0.4, fill_color=ORANGE_TOOL,
                          fill_opacity=0.55, stroke_color=ORANGE_TOOL, stroke_width=2)
        slide.next_to(wp, DOWN, buff=0.55).align_to(chuck, LEFT).shift(RIGHT * 0.5)
        slide_lbl = Text("Slide Table", font_size=20, color=ORANGE_TOOL).next_to(slide, RIGHT, buff=0.2)

        # Spindle center line
        center_line = DashedLine(
            chuck.get_right() + LEFT * 0.05,
            wp.get_right() + RIGHT * 0.3,
            color=YELLOW, stroke_width=1.5,
        ).align_to(wp, UP).shift(DOWN * 0.45)

        # Axis arrows (bottom-left corner, clear of labels)
        origin_pt = LEFT * 5.0 + DOWN * 2.2
        z_arrow = Arrow(origin_pt, origin_pt + RIGHT * 1.5,
                        color=GREEN_A, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)
        z_lbl = Text("+Z", font_size=19, color=GREEN_A).next_to(z_arrow, RIGHT, buff=0.08)
        x_arrow = Arrow(origin_pt, origin_pt + DOWN * 1.0,
                        color=RED_A, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)
        x_lbl = Text("+X", font_size=19, color=RED_A).next_to(x_arrow, DOWN, buff=0.06)

        machine_grp = VGroup(chuck, jaw_top, jaw_bot, wp, slide,
                             chuck_lbl, wp_lbl, slide_lbl, center_line,
                             z_arrow, z_lbl, x_arrow, x_lbl)

        note = Text("ตั้ง: เส้นผ่าศูนย์กลาง + ความยาว chuck & workpiece",
                    font_size=21, color=GRAY_MID).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(chuck), FadeIn(jaw_top), FadeIn(jaw_bot), run_time=0.8)
        self.play(Write(chuck_lbl))
        self.play(FadeIn(wp), run_time=0.6)
        self.play(Write(wp_lbl))
        self.play(Create(center_line))
        self.play(FadeIn(slide), Write(slide_lbl), run_time=0.7)
        self.play(GrowArrow(z_arrow), Write(z_lbl),
                  GrowArrow(x_arrow), Write(x_lbl), run_time=0.8)
        self.play(Write(note))
        self.wait(2.5)
        self.play(FadeOut(VGroup(machine_grp, note, header)))

    # ── PART 2 : Tool Offsets ────────────────────────────────
    def part2_tool_offsets(self):
        header = self._part_header("② ตั้งค่าหัวมีด (Tool Offsets)", color=YELLOW_TOOL)
        self.play(FadeIn(header, shift=DOWN * 0.3))
        self.wait(0.5)

        # Slide rectangle
        slide_rect = Rectangle(width=7, height=1.2, fill_color="#37474F",
                                fill_opacity=0.7, stroke_color=ORANGE_TOOL, stroke_width=2)
        slide_rect.move_to(ORIGIN + DOWN * 0.6)

        # Three tool blocks on the slide
        tools_data = [
            ("T01\nRef", LEFT * 2.3, GREEN_ZONE),
            ("T02", ORIGIN, YELLOW_TOOL),
            ("T09", RIGHT * 2.3, BLUE_LIGHT),
        ]
        tool_blocks = VGroup()
        tool_labels = VGroup()
        for name, pos, col in tools_data:
            blk = Rectangle(width=0.9, height=0.9, fill_color=col,
                            fill_opacity=0.75, stroke_color=WHITE, stroke_width=1.5)
            blk.move_to(slide_rect.get_center() + pos + UP * 0.15)
            lbl = Text(name, font_size=18, color=WHITE).move_to(blk.get_center())
            tool_blocks.add(blk)
            tool_labels.add(lbl)

        # dX, dZ arrows
        ref_blk = tool_blocks[0]
        t2_blk = tool_blocks[1]
        dx_arrow = DoubleArrow(ref_blk.get_right(), t2_blk.get_left(),
                               color=YELLOW, stroke_width=2.5, buff=0.05,
                               max_tip_length_to_length_ratio=0.15)
        dx_arrow.shift(UP * 0.65)
        dx_lbl = Text("dZ offset", font_size=19, color=YELLOW).next_to(dx_arrow, UP, buff=0.08)

        dz_arrow = Arrow(ref_blk.get_bottom(), ref_blk.get_bottom() + DOWN * 0.7,
                         color=RED_A, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        dz_lbl = Text("dX (radius)", font_size=19, color=RED_A).next_to(dz_arrow, RIGHT, buff=0.1)

        note = Text("Reference tool ใช้ touch-off G54 — tool อื่นวัด offset จากตรงนี้",
                    font_size=21, color=GRAY_MID).to_edge(DOWN, buff=0.25)

        self.play(FadeIn(slide_rect))
        self.play(LaggedStart(*[FadeIn(b) for b in tool_blocks], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(l) for l in tool_labels], lag_ratio=0.3))
        self.play(GrowArrow(dx_arrow), Write(dx_lbl), run_time=0.9)
        self.play(GrowArrow(dz_arrow), Write(dz_lbl), run_time=0.9)
        self.play(Write(note))
        self.wait(2.5)
        self.play(FadeOut(VGroup(slide_rect, tool_blocks, tool_labels,
                                 dx_arrow, dx_lbl, dz_arrow, dz_lbl, note, header)))

    # ── PART 3 : Green Zone ──────────────────────────────────
    def part3_green_zone(self):
        header = self._part_header("③ Green Zone คืออะไร?", color=GREEN_ZONE)
        self.play(FadeIn(header, shift=DOWN * 0.3))
        self.wait(0.5)

        # X-Z axes
        ax = Axes(
            x_range=[-1, 12, 2],
            y_range=[-1, 8, 2],
            x_length=8,
            y_length=4.5,
            axis_config={"color": GRAY_MID, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 0.5 + DOWN * 0.5)

        x_lbl = Text("Z (mm)", font_size=20, color=GRAY_MID).next_to(ax.x_axis, RIGHT, buff=0.1)
        y_lbl = Text("X radius", font_size=20, color=GRAY_MID).next_to(ax.y_axis, UP, buff=0.1)

        # Obstacle zone (chuck + workpiece shadow)
        obs = Polygon(
            ax.c2p(0, 0), ax.c2p(5, 0), ax.c2p(5, 3), ax.c2p(0, 3),
            fill_color=RED_ZONE, fill_opacity=0.35, stroke_width=0,
        )
        obs_lbl = Text("Obstacle\n(chuck + WP)", font_size=18, color=RED_ZONE).move_to(ax.c2p(2.5, 1.5))

        # Green zone (safe mounting region)
        green = Polygon(
            ax.c2p(5, 3), ax.c2p(11, 3), ax.c2p(11, 7), ax.c2p(5, 7),
            fill_color=GREEN_ZONE, fill_opacity=0.35, stroke_width=0,
        )
        green_lbl = Text("Green Zone\n(safe to mount)", font_size=18, color=GREEN_ZONE
                         ).move_to(ax.c2p(8, 6.0))

        # Candidate tool marker (placed at bottom-right of green zone, label below)
        tool_dot = Dot(ax.c2p(9, 3.8), color=YELLOW_TOOL, radius=0.13)
        tool_lbl = Text("Candidate Tool", font_size=17, color=YELLOW_TOOL
                        ).next_to(tool_dot, DOWN, buff=0.12)

        note = Text("Run Analysis → คำนวณ zone ที่หัวมีดวางได้โดยไม่ชน",
                    font_size=21, color=GRAY_MID).to_edge(DOWN, buff=0.25)

        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=1.0)
        self.play(FadeIn(obs), Write(obs_lbl), run_time=0.8)
        self.play(FadeIn(green), Write(green_lbl), run_time=0.8)
        self.play(FadeIn(tool_dot), Write(tool_lbl))
        self.play(Write(note))
        self.wait(2.5)
        self.play(FadeOut(VGroup(ax, x_lbl, y_lbl, obs, obs_lbl,
                                 green, green_lbl, tool_dot, tool_lbl, note, header)))

    # ── OUTRO ────────────────────────────────────────────────
    def outro(self):
        msg = Text("พร้อมใช้งาน CK40B Simulator!", font_size=44, color=GREEN_ZONE)
        sub = Text("Load G-code → Setup → Run Analysis", font_size=28, color=GRAY_MID)
        VGroup(msg, sub).arrange(DOWN, buff=0.5)
        self.play(Write(msg))
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(2)
        self.play(FadeOut(VGroup(msg, sub)))

    # ── HELPER ───────────────────────────────────────────────
    def _part_header(self, text, color=WHITE):
        h = Text(text, font_size=34, color=color)
        h.to_edge(UP, buff=0.35)
        line = Line(LEFT * 6, RIGHT * 6, color=color, stroke_width=1.5).next_to(h, DOWN, buff=0.15)
        return VGroup(h, line)
