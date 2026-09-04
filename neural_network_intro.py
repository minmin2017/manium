"""Deep Learning intro series, video 1: what a neural network is and how it
learns. Standalone personal-interest topic (not tied to Min's coursework),
first video in a potential new series. Kept 2D throughout -- a network
diagram is an abstract graph, not a physical object, and every reputable
source (including 3Blue1Brown's own neural-network series, the style this
whole pipeline is built to match) draws it flat.
"""

from mlib import *
import numpy as np

IN_COL = "#4FC3F7"      # input layer
HID_COL = "#AB47BC"     # hidden layer
OUT_COL = "#66BB6A"     # output layer
WEIGHT_COL = "#78909C"  # connection lines
ERR_COL = "#FF7043"     # prediction error


def layer_dots(n, x, color, spread=2.6):
    ys = np.linspace(spread / 2, -spread / 2, n) if n > 1 else [0]
    return VGroup(*[Dot(point=[x, y, 0], radius=0.14, color=color, fill_opacity=1) for y in ys])


def connect_layers(layer_a, layer_b, seed=0):
    rng = np.random.default_rng(seed)
    lines = VGroup()
    for a in layer_a:
        for b in layer_b:
            w = rng.uniform(0.25, 0.9)
            lines.add(Line(a.get_center(), b.get_center(), color=WEIGHT_COL,
                            stroke_width=2, stroke_opacity=w))
    return lines


class NN01_WhatIsANeuralNetwork(SafeScene):
    def construct(self):
        heading = title("Neural Network คืออะไร")
        self.play(FadeIn(heading, shift=UP * 0.4), run_time=0.6)

        # ---- segment 1: single neuron ----
        cap1 = caption_top("นิวรอนเดี่ยว: รับค่าเข้า x คูณน้ำหนัก w แล้วบวกรวมกัน")
        self.play(FadeIn(cap1, shift=UP * 0.3), run_time=0.5)

        inputs = VGroup(*[Dot(point=[-4.5, y, 0], radius=0.15, color=IN_COL, fill_opacity=1)
                           for y in (1.6, 0, -1.6)])
        in_labels = VGroup(*[MathTex(f"x_{i+1}", font_size=32).next_to(d, LEFT, buff=0.25)
                              for i, d in enumerate(inputs)])
        neuron = Circle(radius=0.55, color=HID_COL, fill_opacity=0.85, fill_color=HID_COL).move_to(ORIGIN)
        w_lines = VGroup(*[Line(d.get_center(), neuron.get_center(), color=WEIGHT_COL, stroke_width=3)
                            for d in inputs])
        w_labels = VGroup(*[MathTex(f"w_{i+1}", font_size=28, color=WEIGHT_COL)
                             .move_to(l.point_from_proportion(0.35)).shift(UP * 0.22)
                             for i, l in enumerate(w_lines)])

        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.3) for d in inputs], lag_ratio=0.2),
                   LaggedStart(*[FadeIn(t) for t in in_labels], lag_ratio=0.2), run_time=1.0)
        self.play(Create(w_lines), FadeIn(w_labels), FadeIn(neuron, shift=LEFT * 0.3), run_time=1.0)

        out_arrow = Arrow(neuron.get_right(), neuron.get_right() + RIGHT * 1.3, buff=0.1, color=OUT_COL)
        out_dot = Dot(out_arrow.get_end() + RIGHT * 0.2, radius=0.15, color=OUT_COL, fill_opacity=1)
        y_label = MathTex("y", font_size=32, color=OUT_COL).next_to(out_dot, RIGHT, buff=0.2)
        self.play(GrowArrow(out_arrow), FadeIn(out_dot, shift=RIGHT * 0.2), FadeIn(y_label), run_time=0.7)

        formula = MathTex(
            r"y = f(\,w_1 x_1 + w_2 x_2 + w_3 x_3 + b\,)",
            font_size=34,
        ).move_to([0, -2.6, 0])
        self.play(FadeIn(formula, shift=UP * 0.3), run_time=0.7)
        self.wait(0.8)

        f_note = caption_top("f = activation function -- ตัดสินว่านิวรอนนี้ \"ตื่น\" แค่ไหน")
        self.play(ReplacementTransform(cap1, f_note), run_time=0.7)
        self.wait(0.8)

        neuron_group = VGroup(inputs, in_labels, neuron, w_lines, w_labels, out_arrow, out_dot, y_label, formula)
        self.play(FadeOut(neuron_group), FadeOut(f_note), run_time=0.6)

        # ---- segment 2: stack into layers ----
        cap2 = caption_top("เอานิวรอนหลายตัวมาต่อกันเป็น \"ชั้น\" (layer)")
        self.play(FadeIn(cap2, shift=UP * 0.3), run_time=0.5)

        L_in = layer_dots(4, -4.0, IN_COL)
        L_hid = layer_dots(5, -0.5, HID_COL, spread=3.2)
        L_hid2 = layer_dots(5, 2.0, HID_COL, spread=3.2)
        L_out = layer_dots(2, 4.5, OUT_COL, spread=1.4)

        edges1 = connect_layers(L_in, L_hid, seed=1)
        edges2 = connect_layers(L_hid, L_hid2, seed=2)
        edges3 = connect_layers(L_hid2, L_out, seed=3)

        in_tag = Text("Input", font_size=22, color=IN_COL).next_to(L_in, DOWN, buff=0.35)
        hid_tag = Text("Hidden layers", font_size=22, color=HID_COL).move_to([0.75, -2.3, 0])
        out_tag = Text("Output", font_size=22, color=OUT_COL).next_to(L_out, DOWN, buff=0.35)

        self.play(LaggedStart(Create(edges1), Create(edges2), Create(edges3), lag_ratio=0.15), run_time=1.4)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.4) for d in [*L_in, *L_hid, *L_hid2, *L_out]], lag_ratio=0.03),
            run_time=1.2,
        )
        self.play(FadeIn(in_tag, shift=UP * 0.2), FadeIn(hid_tag, shift=UP * 0.2), FadeIn(out_tag, shift=UP * 0.2),
                   run_time=0.6)
        self.wait(0.6)

        depth_note = caption_top('ยิ่งมี "ชั้นซ้อน" เยอะ = ยิ่ง "ลึก" (Deep) -- ที่มาของชื่อ Deep Learning')
        self.play(ReplacementTransform(cap2, depth_note), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(depth_note), run_time=0.4)

        # ---- segment 3: forward pass ----
        cap3 = caption_top("ข้อมูลไหลผ่านทีละชั้น (forward pass)")
        self.play(FadeIn(cap3, shift=UP * 0.3), run_time=0.5)

        pulse_groups = [L_in, L_hid, L_hid2, L_out]
        for grp in pulse_groups:
            self.play(*[Indicate(d, color=WHITE, scale_factor=1.6) for d in grp], run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(cap3), run_time=0.4)

        # ---- segment 4: how it learns ----
        cap4 = caption_top("เรียนรู้ = ปรับ weight ให้ทำนายแม่นขึ้นเรื่อยๆ")
        self.play(FadeIn(cap4, shift=UP * 0.3), run_time=0.5)

        pred = DecimalNumber(0.31, num_decimal_places=2, color=OUT_COL, font_size=30)
        actual = DecimalNumber(0.90, num_decimal_places=2, color=WHITE, font_size=30)
        pred_row = VGroup(Text("ทำนาย:", font_size=26), pred).arrange(RIGHT, buff=0.2).move_to([-2.6, -2.7, 0])
        actual_row = VGroup(Text("คำตอบจริง:", font_size=26), actual).arrange(RIGHT, buff=0.2).move_to([2.6, -2.7, 0])
        err_brace = BraceBetweenPoints(pred_row.get_right() + RIGHT * 0.3, actual_row.get_left() - RIGHT * 0.3, UP)
        err_label = Text("error", font_size=22, color=ERR_COL).next_to(err_brace, UP, buff=0.1)

        self.play(FadeIn(pred_row, shift=UP * 0.2), FadeIn(actual_row, shift=UP * 0.2), run_time=0.6)
        self.play(Create(err_brace), FadeIn(err_label), run_time=0.5)
        self.wait(0.4)

        targets = [0.55, 0.74, 0.88]
        for t in targets:
            self.play(
                pred.animate.set_value(t),
                LaggedStart(*[e.animate.set_stroke(opacity=np.random.default_rng(int(t * 100) + i).uniform(0.25, 0.9))
                              for i, e in enumerate([*edges1, *edges2, *edges3])], lag_ratio=0.002),
                run_time=0.9,
            )
        self.play(FadeOut(err_brace), FadeOut(err_label), run_time=0.4)
        close_note = caption_top("ทำซ้ำหลายล้านรอบ -- เครือข่ายค่อยๆ \"ฉลาดขึ้น\" เอง")
        self.play(ReplacementTransform(cap4, close_note), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(VGroup(L_in, L_hid, L_hid2, L_out, edges1, edges2, edges3,
                            in_tag, hid_tag, out_tag, pred_row, actual_row, close_note, heading)),
            run_time=0.8,
        )
