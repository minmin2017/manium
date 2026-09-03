"""Fluid Power Control — W06 Hydraulic Valves (hydraulic04.pdf)
Page-by-page clips (skill rule: one clip per lecture-slide page).

Page 6 — Shuttle Valve. Source: hydraulic04.pdf p.6 (Esposito, "Fluid Power
with Applications") — both the cross-section mechanism and the ISO/JIC
symbol are reproduced directly from that page image (verified against the
scanned figure itself, plus cross-checked against a general web search on
ISO 1219 shuttle-valve symbols: "compares pressure of two lines, routes the
higher pressure to the output" — matches the mechanism animated below).
This valve is one of the 6 symbols flagged in the note as a past-exam
question (Midterm 1/2567: "วาดสัญลักษณ์วาล์ว 6 ตัว"), so the ISO symbol beat
gets equal weight to the mechanism beat, not just a footnote.
"""

from manim import *
import numpy as np
from mlib import (
    SafeScene, title, caption_top, page_ref, fit_width,
    METAL, GRAYTXT, WARN, OK, WHITE,
)

PRIMARY = "#42A5F5"    # primary supply oil
SECONDARY = "#FFB74D"  # secondary supply oil
BLOCKED = "#FF5252"    # port currently sealed by the piston

BORE_Y = -1.8
PISTON_W, PISTON_H = 0.9, 0.42
PISTON_LEFT_X = -2.55   # piston seated against PRIMARY port (blocks primary)
PISTON_RIGHT_X = 2.55   # piston seated against SECONDARY port (blocks secondary, book's default)


def spring_zigzag(x1, x2, y, coils=8, amp=0.13, color=METAL, stroke_width=2.5):
    """Coil spring between x1 and x2 on the horizontal centerline y — rebuilt
    every frame via an updater as the piston slides (mlib §16 Pattern B style:
    mob.become(...) since the shape itself, not just position, changes)."""
    length = x2 - x1
    if length <= 0.08:
        m = Line([x1, y, 0], [x2, y, 0], color=color, stroke_width=stroke_width)
        return m
    n = max(coils, 3)
    xs = np.linspace(x1, x2, n * 2 + 1)
    pts = []
    for i, x in enumerate(xs):
        if i == 0 or i == len(xs) - 1:
            yy = y
        else:
            yy = y + (amp if i % 2 == 1 else -amp)
        pts.append([x, yy, 0])
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


def build_shuttle_symbol(center=ORIGIN, box_w=2.8, box_h=1.6):
    """Reproduces the book's own 'Symbol' box (p.6) as closely as the scan
    allows: primary in from the left through a check-ball, a junction dot,
    secondary in from below, outlet out through an open chevron to the right."""
    cx, cy = center[0], center[1]
    box = Rectangle(width=box_w, height=box_h, color=WHITE, stroke_width=2.5)
    box.move_to([cx, cy, 0])

    y = cy
    left_line = Line([cx - box_w / 2, y, 0], [cx - 0.55, y, 0], color=WHITE, stroke_width=2.5)
    ball_tri = Polygon([cx - 0.55, y, 0], [cx - 0.75, y + 0.13, 0], [cx - 0.75, y - 0.13, 0],
                        color=WHITE, stroke_width=2.5, fill_opacity=0)
    circle = Circle(radius=0.22, color=WHITE, stroke_width=2.5).move_to([cx - 0.45, y, 0])
    shuttle_arc = CurvedArrow([cx - 0.63, y + 0.14, 0], [cx - 0.27, y + 0.14, 0],
                               angle=-TAU / 4, color=WHITE, stroke_width=2)
    mid_line = Line([cx - 0.23, y, 0], [cx + 0.05, y, 0], color=WHITE, stroke_width=2.5)
    dot = Dot([cx + 0.05, y, 0], radius=0.05, color=WHITE)
    down_line = Line([cx + 0.05, y, 0], [cx + 0.05, cy - box_h / 2, 0], color=WHITE, stroke_width=2.5)
    down_stub = Line([cx + 0.05, cy - box_h / 2, 0], [cx + 0.05, cy - box_h / 2 - 0.35, 0],
                      color=WHITE, stroke_width=2.5)
    to_chevron = Line([cx + 0.05, y, 0], [cx + 0.95, y, 0], color=WHITE, stroke_width=2.5)
    chevron = VGroup(
        Line([cx + 0.95, y + 0.12, 0], [cx + 1.15, y, 0], color=WHITE, stroke_width=2.5),
        Line([cx + 0.95, y - 0.12, 0], [cx + 1.15, y, 0], color=WHITE, stroke_width=2.5),
    )
    out_line = Line([cx + 1.15, y, 0], [cx + box_w / 2, y, 0], color=WHITE, stroke_width=2.5)

    return VGroup(box, left_line, ball_tri, circle, shuttle_arc, mid_line, dot,
                  down_line, down_stub, to_chevron, chevron, out_line)


class HV06_ShuttleValve(SafeScene):
    """Page 6 of hydraulic04.pdf — Shuttle Valve.
    Mechanism: two inlets (primary, secondary), one outlet. A free piston
    (light-spring-returned to the secondary side by default, per the book's
    own diagram) shuttles toward whichever inlet has LOWER pressure and
    seals it, letting the HIGHER-pressure inlet flow to the outlet."""

    def construct(self):
        ttl = title("Shuttle Valve")
        pref = page_ref("หน้า 6 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        # ---- housing (T-shaped cross section, 3 open ports) ---------------
        top_wall_L = Rectangle(width=2.95, height=0.3, fill_color=METAL, fill_opacity=0.35,
                                stroke_color=METAL, stroke_width=2).move_to([-1.825, -1.4, 0])
        top_wall_R = Rectangle(width=2.95, height=0.3, fill_color=METAL, fill_opacity=0.35,
                                stroke_color=METAL, stroke_width=2).move_to([1.825, -1.4, 0])
        bottom_wall = Rectangle(width=6.6, height=0.3, fill_color=METAL, fill_opacity=0.35,
                                 stroke_color=METAL, stroke_width=2).move_to([0, -2.2, 0])
        stem_wall_L = Rectangle(width=0.2, height=1.6, fill_color=METAL, fill_opacity=0.35,
                                 stroke_color=METAL, stroke_width=2).move_to([-0.45, -0.45, 0])
        stem_wall_R = Rectangle(width=0.2, height=1.6, fill_color=METAL, fill_opacity=0.35,
                                 stroke_color=METAL, stroke_width=2).move_to([0.45, -0.45, 0])
        housing = VGroup(top_wall_L, top_wall_R, bottom_wall, stem_wall_L, stem_wall_R)

        primary_arrow = Arrow([-4.4, BORE_Y, 0], [-3.35, BORE_Y, 0], color=PRIMARY,
                               buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.28)
        secondary_arrow = Arrow([4.4, BORE_Y, 0], [3.35, BORE_Y, 0], color=SECONDARY,
                                 buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.28)
        outlet_arrow = Arrow([0, 0.35, 0], [0, 1.25, 0], color=OK,
                              buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.28)

        primary_lbl = Text("Primary Supply", font_size=16, color=PRIMARY).move_to([-3.9, -2.65, 0])
        secondary_lbl = Text("Secondary Supply", font_size=16, color=SECONDARY).move_to([3.9, -2.65, 0])
        outlet_lbl = Text("Outlet", font_size=16, color=OK).next_to(outlet_arrow, UP, buff=0.12)

        self.play(
            Create(housing),
            GrowArrow(primary_arrow), GrowArrow(secondary_arrow), GrowArrow(outlet_arrow),
            FadeIn(primary_lbl), FadeIn(secondary_lbl), FadeIn(outlet_lbl),
            run_time=1.6,
        )

        # ---- piston + spring (default state: piston blocks SECONDARY) -----
        piston = Rectangle(width=PISTON_W, height=PISTON_H, fill_color=METAL,
                            fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        piston.move_to([PISTON_RIGHT_X, BORE_Y, 0])
        spring = spring_zigzag(-3.1, PISTON_RIGHT_X - PISTON_W / 2, BORE_Y)
        spring.add_updater(lambda m: m.become(
            spring_zigzag(-3.1, piston.get_x() - PISTON_W / 2, BORE_Y)))

        piston_lbl = caption_top("กลไกภายใน: ลูกสูบ + สปริงคืนตำแหน่งเบาๆ (Piston + Spring)")

        self.play(FadeIn(piston), Create(spring), run_time=0.8)
        self.play(FadeIn(piston_lbl), run_time=0.9)
        self.wait(0.6)
        self.play(FadeOut(piston_lbl), run_time=0.6)

        # ---- state A: default — secondary blocked, primary flows ---------
        cap1 = caption_top("สถานะปกติ: สปริงดันลูกสูบไปชิด Secondary — ปิดกั้นทางเข้า Secondary ไว้ก่อน")
        self.play(FadeIn(cap1), run_time=0.6)

        blocked_sec = Text("ปิดกั้น", font_size=15, color=BLOCKED).move_to([2.55, -0.85, 0])
        blocked_sec_leader = Line([2.55, -1.0, 0], [2.9, -1.6, 0], color=BLOCKED, stroke_width=2)
        self.play(FadeIn(blocked_sec), Create(blocked_sec_leader), run_time=0.5)

        primary_path = VMobject().set_points_as_corners(
            [[-3.2, BORE_Y, 0], [0, BORE_Y, 0], [0, 1.15, 0]])
        dots = VGroup(*[Dot(radius=0.06, color=PRIMARY) for _ in range(4)])
        anims = [MoveAlongPath(d, primary_path, rate_func=linear, run_time=1.8) for d in dots]
        self.play(LaggedStart(*anims, lag_ratio=0.25))
        self.play(FadeOut(dots), run_time=0.3)
        self.play(FadeOut(cap1), FadeOut(blocked_sec), FadeOut(blocked_sec_leader), run_time=0.5)

        # ---- state B: secondary pressure rises and wins -------------------
        cap2 = caption_top("ถ้าแรงดันฝั่ง Secondary เพิ่มขึ้นจนสูงกว่าฝั่ง Primary...")
        self.play(FadeIn(cap2), run_time=0.6)
        self.play(secondary_arrow.animate.set_stroke(width=10).scale(1.15, about_point=[3.9, BORE_Y, 0]),
                  run_time=0.8, rate_func=there_and_back)
        self.wait(0.3)
        self.play(FadeOut(cap2), run_time=0.4)

        cap3 = caption_top("...ลูกสูบจะถูกดันข้ามไปปิดกั้นฝั่ง Primary แทนโดยอัตโนมัติ")
        self.play(FadeIn(cap3), run_time=0.6)
        self.play(piston.animate.move_to([PISTON_LEFT_X, BORE_Y, 0]), run_time=1.8)

        blocked_pri = Text("ปิดกั้น", font_size=15, color=BLOCKED).move_to([-2.55, -0.85, 0])
        blocked_pri_leader = Line([-2.55, -1.0, 0], [-2.9, -1.6, 0], color=BLOCKED, stroke_width=2)
        self.play(FadeIn(blocked_pri), Create(blocked_pri_leader), run_time=0.5)

        secondary_path = VMobject().set_points_as_corners(
            [[3.2, BORE_Y, 0], [0, BORE_Y, 0], [0, 1.15, 0]])
        dots2 = VGroup(*[Dot(radius=0.06, color=SECONDARY) for _ in range(4)])
        anims2 = [MoveAlongPath(d, secondary_path, rate_func=linear, run_time=1.8) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.25))
        self.play(FadeOut(dots2), run_time=0.3)
        self.play(FadeOut(cap3), run_time=0.4)

        # ---- rule recap -----------------------------------------------
        cap4 = caption_top("กฎ: เลือกฝั่งความดันสูงกว่าเสมอ ปิดกั้นฝั่งความดันต่ำกว่า — ไม่ต้องมีวาล์วแยกทาง")
        self.play(FadeIn(cap4), run_time=0.7)
        self.wait(1.4)

        spring.clear_updaters()
        self.play(
            FadeOut(cap4), FadeOut(blocked_pri), FadeOut(blocked_pri_leader),
            FadeOut(housing), FadeOut(piston), FadeOut(spring),
            FadeOut(primary_arrow), FadeOut(secondary_arrow), FadeOut(outlet_arrow),
            FadeOut(primary_lbl), FadeOut(secondary_lbl), FadeOut(outlet_lbl),
            run_time=0.9,
        )

        # ---- ISO / JIC symbol (exam-critical: one of the 6 valve symbols
        # asked to be hand-drawn in Midterm 1/2567) -------------------------
        star = fit_width(Text("⭐⭐ ข้อสอบเก่าออกตรงๆ — ต้องวาดสัญลักษณ์นี้ได้",
                               font_size=20, color=WARN), 11.0)
        star.move_to([0, 0.05, 0])
        sym = build_shuttle_symbol(center=[0, -2.0, 0])
        sym_lbl = Text("สัญลักษณ์ Shuttle Valve (ตามหนังสือ)", font_size=18, color=WHITE)
        sym_lbl.move_to([0, -0.75, 0])

        self.play(FadeIn(star), run_time=0.5)
        self.play(Create(sym), FadeIn(sym_lbl), run_time=1.8)
        self.wait(1.8)

        self.fade_out_all(run_time=0.9)
