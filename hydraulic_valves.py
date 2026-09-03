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
    shuttle_arc.tip.scale(0.35, about_point=shuttle_arc.get_end())
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


# =====================================================================
# Batch 2: remaining pages of hydraulic04.pdf, Directional Control section
# (pages 1,2,3,4,7,8,9,10,11,12 — 5,6,13,15 already have clips)
# =====================================================================

SUPPLY = "#EF5350"   # pressurized path (matches the book's own red pipes p.8)
RETURN = "#42A5F5"   # tank-return path (matches the book's own blue pipes p.8)


class HV01_Title(SafeScene):
    """Page 1 — cover slide."""

    def construct(self):
        pref = page_ref("หน้า 1 · Hydraulic Valves")
        t = Text("Hydraulic Valves", font_size=48, color=WHITE)
        sub = fit_width(Text("บทนำ: วาล์ว 3 กลุ่มหลัก — Directional / Pressure / Flow Control",
                              font_size=20, color=GRAYTXT), 11.0)
        sub.next_to(t, DOWN, buff=0.6)
        self.play(FadeIn(pref), Write(t), run_time=1.3)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(1.6)
        self.fade_out_all(run_time=0.8)


class HV03_Title(SafeScene):
    """Page 3 — section divider."""

    def construct(self):
        pref = page_ref("หน้า 3 · Hydraulic Valves")
        t = Text("Directional Control Valves", font_size=40, color=WHITE)
        sub = fit_width(Text("บังคับว่าน้ำมันจะไหลไปทางไหน — two/three/four-way, check, shuttle",
                              font_size=18, color=GRAYTXT), 11.0)
        sub.next_to(t, DOWN, buff=0.6)
        self.play(FadeIn(pref), Write(t), run_time=1.3)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(1.6)
        self.fade_out_all(run_time=0.8)


class HV02_Classification(SafeScene):
    """Page 2 — Valve Classification table (3 columns)."""

    def construct(self):
        ttl = title("Valve Classification")
        pref = page_ref("หน้า 2 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        cap = caption_top("แผนที่ทั้งบท — วาล์วแบ่งตาม \"ตัวแปรที่ควบคุม\" 3 กลุ่ม")
        self.play(FadeIn(cap), run_time=0.6)

        cols = [
            ("Directional control", ["Two way", "Check", "Shuttle", "Three way",
                                      "Four way", "Limit switches",
                                      "Proportional electrohydraulic", "Servo"], PRIMARY),
            ("Pressure control", ["Pressure relief", "Hydraulic fuse", "Pressure reducing",
                                   "Sequencing", "Unloading", "Counterbalance",
                                   "Pressure switches"], WARN),
            ("Flow control", ["Fixed", "Variable", "Compensated", "Deceleration",
                               "Flow divider", "Electrohydraulic", "Servo"], OK),
        ]
        starred = {"Check", "Shuttle", "Pressure reducing", "Unloading"}
        col_groups = VGroup()
        for name, items, color in cols:
            head = Text(name, font_size=20, color=color)
            rows = VGroup(*[
                Text(("⭐ " if it in starred else "") + it, font_size=16,
                     color=WARN if it in starred else GRAYTXT)
                for it in items
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            group = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            col_groups.add(group)
        col_groups.arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, -0.9, 0])

        self.play(LaggedStart(*[FadeIn(c) for c in col_groups], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        note = caption_top("⭐ = สัญลักษณ์ที่ข้อสอบเก่าเคยออกให้วาด (ดูรายละเอียดหน้า 5,6,17,18)")
        self.play(FadeOut(cap), run_time=0.3)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.8)
        self.fade_out_all(run_time=0.9)


class HV04_TwoWayOnOff(SafeScene):
    """Page 4 — Two Way On-Off Valve."""

    def construct(self):
        ttl = title("Two Way On-Off Valve")
        pref = page_ref("หน้า 4 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        body_top = Rectangle(width=1.4, height=0.35, fill_color=METAL, fill_opacity=0.35,
                              stroke_color=METAL, stroke_width=2).move_to([0, -1.0, 0])
        body_bot = Rectangle(width=1.4, height=0.35, fill_color=METAL, fill_opacity=0.35,
                              stroke_color=METAL, stroke_width=2).move_to([0, -2.4, 0])
        pipe_L = Rectangle(width=2.6, height=0.4, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([-2.6, -1.7, 0])
        pipe_R = Rectangle(width=2.6, height=0.4, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([2.6, -1.7, 0])
        seat = Line([-0.5, -1.85, 0], [0.5, -1.85, 0], color=METAL, stroke_width=5)
        housing = VGroup(body_top, body_bot, pipe_L, pipe_R, seat)

        stem = Line([0, -0.85, 0], [0, -1.85, 0], color=WHITE, stroke_width=4)
        disc = Triangle(color=WHITE, fill_color=METAL, fill_opacity=0.9, stroke_width=2)
        disc.scale(0.22).rotate(PI).move_to([0, -1.85, 0])
        disc_group = VGroup(stem, disc)

        in_arrow = Arrow([-4.3, -1.7, 0], [-3.35, -1.7, 0], color=PRIMARY, buff=0,
                          stroke_width=6, max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([3.35, -1.7, 0], [4.3, -1.7, 0], color=OK, buff=0,
                           stroke_width=6, max_tip_length_to_length_ratio=0.28)
        in_lbl = Text("Inlet", font_size=15, color=PRIMARY).move_to([-3.9, -2.7, 0])
        out_lbl = Text("Outlet", font_size=15, color=OK).move_to([3.9, -2.7, 0])

        self.play(Create(housing), GrowArrow(in_arrow), GrowArrow(out_arrow),
                   FadeIn(in_lbl), FadeIn(out_lbl), run_time=1.4)
        self.play(FadeIn(disc_group), run_time=0.6)

        cap1 = caption_top("หมุนแฮนด์กดดิสก์ลงชนซีท (seat) — ปิดกั้นทางไหลสนิท")
        self.play(FadeIn(cap1), disc_group.animate.shift(DOWN * 0.02), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("คลายแฮนด์ ยกดิสก์ขึ้นจากซีท — เปิดให้น้ำมันไหลผ่าน")
        self.play(FadeIn(cap2), disc_group.animate.shift(UP * 0.7), run_time=1.0)
        dots = VGroup(*[Dot(radius=0.06, color=PRIMARY) for _ in range(4)])
        path = VMobject().set_points_as_corners([[-3.2, -1.7, 0], [3.2, -1.7, 0]])
        anims = [MoveAlongPath(d, path, rate_func=linear, run_time=1.6) for d in dots]
        self.play(LaggedStart(*anims, lag_ratio=0.25))
        self.play(FadeOut(dots), run_time=0.3)

        cap3 = caption_top("แบบโซลินอยด์: ใช้แรงดันไพลอตช่วยดันสปูลแทนแรงคน — กลไกละเอียดดูหน้า 11")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.6)
        self.fade_out_all(run_time=0.9)


class HV07_ThreeWay(SafeScene):
    """Page 7 — Three-Way Valve."""

    def construct(self):
        ttl = title("Three-Way Valve")
        pref = page_ref("หน้า 7 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        y = -1.8
        top_wall_L = Rectangle(width=1.5, height=0.3, fill_color=METAL, fill_opacity=0.35,
                                stroke_color=METAL, stroke_width=2).move_to([-1.15, y + 0.4, 0])
        top_wall_R = Rectangle(width=1.5, height=0.3, fill_color=METAL, fill_opacity=0.35,
                                stroke_color=METAL, stroke_width=2).move_to([1.15, y + 0.4, 0])
        bottom_wall = Rectangle(width=5.2, height=0.3, fill_color=METAL, fill_opacity=0.35,
                                 stroke_color=METAL, stroke_width=2).move_to([0, y - 0.7, 0])
        stem_L = Rectangle(width=0.2, height=1.3, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([-0.4, y + 1.05, 0])
        stem_R = Rectangle(width=0.2, height=1.3, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([0.4, y + 1.05, 0])
        housing = VGroup(top_wall_L, top_wall_R, bottom_wall, stem_L, stem_R)

        a_arrow = Arrow([0, y + 1.7, 0], [0, y + 2.5, 0], color=OK, buff=0, stroke_width=6,
                         max_tip_length_to_length_ratio=0.28)
        a_lbl = Text("A", font_size=18, color=OK).next_to(a_arrow, UP, buff=0.1)
        p_arrow = Arrow([-4.4, y, 0], [-2.75, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                         max_tip_length_to_length_ratio=0.28)
        p_lbl = Text("P", font_size=16, color=SUPPLY).move_to([-3.9, y - 1.0, 0])
        t_arrow = Arrow([2.75, y, 0], [4.4, y, 0], color=RETURN, buff=0, stroke_width=6,
                         max_tip_length_to_length_ratio=0.28)
        t_lbl = Text("T", font_size=16, color=RETURN).move_to([3.9, y - 1.0, 0])

        spool = Rectangle(width=1.6, height=0.42, fill_color=METAL, fill_opacity=0.9,
                           stroke_color=WHITE, stroke_width=2)
        spool.move_to([-0.9, y, 0])

        self.play(Create(housing), GrowArrow(a_arrow), FadeIn(a_lbl),
                   GrowArrow(p_arrow), FadeIn(p_lbl), GrowArrow(t_arrow), FadeIn(t_lbl),
                   run_time=1.5)
        self.play(FadeIn(spool), run_time=0.6)

        cap1 = caption_top("ตำแหน่ง 1: ร่องสปูลเปิดทาง P→A ให้น้ำมันไหลขึ้น — T ถูกบล็อก")
        self.play(FadeIn(cap1), run_time=0.6)
        dots = VGroup(*[Dot(radius=0.06, color=SUPPLY) for _ in range(4)])
        path1 = VMobject().set_points_as_corners([[-3.5, y, 0], [0, y, 0], [0, y + 2.3, 0]])
        anims = [MoveAlongPath(d, path1, rate_func=linear, run_time=1.6) for d in dots]
        self.play(LaggedStart(*anims, lag_ratio=0.25))
        self.play(FadeOut(dots), FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("เลื่อนสปูลไปตำแหน่ง 2: P ถูกบล็อกแทน — A ต่อกับ T ให้น้ำมันไหลกลับถัง")
        self.play(FadeIn(cap2), spool.animate.move_to([0.9, y, 0]), run_time=1.4)
        dots2 = VGroup(*[Dot(radius=0.06, color=RETURN) for _ in range(4)])
        path2 = VMobject().set_points_as_corners([[0, y + 2.3, 0], [0, y, 0], [3.5, y, 0]])
        anims2 = [MoveAlongPath(d, path2, rate_func=linear, run_time=1.6) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.25))
        self.play(FadeOut(dots2), run_time=0.3)

        cap3 = caption_top("ใช้กับ single-acting cylinder — มีทางเข้า-ออกทางเดียว")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.4)
        self.fade_out_all(run_time=0.9)


def four_way_housing(y=-1.8):
    """Shared 4-port sleeve (A,P,B,T along one bore) used by pages 8-11.
    Port order along the bore: A(top,-1.8) P(bottom,-0.6) B(top,0.6) T(bottom,1.8)."""
    top_1 = Rectangle(width=1.1, height=0.3, fill_color=METAL, fill_opacity=0.35,
                       stroke_color=METAL, stroke_width=2).move_to([-2.25, y + 0.4, 0])
    top_2 = Rectangle(width=1.0, height=0.3, fill_color=METAL, fill_opacity=0.35,
                       stroke_color=METAL, stroke_width=2).move_to([-0.65, y + 0.4, 0])
    top_3 = Rectangle(width=1.0, height=0.3, fill_color=METAL, fill_opacity=0.35,
                       stroke_color=METAL, stroke_width=2).move_to([1.15, y + 0.4, 0])
    bot_1 = Rectangle(width=1.4, height=0.3, fill_color=METAL, fill_opacity=0.35,
                       stroke_color=METAL, stroke_width=2).move_to([-1.45, y - 0.7, 0])
    bot_2 = Rectangle(width=1.0, height=0.3, fill_color=METAL, fill_opacity=0.35,
                       stroke_color=METAL, stroke_width=2).move_to([0.15, y - 0.7, 0])
    bot_3 = Rectangle(width=0.9, height=0.3, fill_color=METAL, fill_opacity=0.35,
                       stroke_color=METAL, stroke_width=2).move_to([2.45, y - 0.7, 0])
    stem_A = Rectangle(width=0.2, height=1.3, fill_color=METAL, fill_opacity=0.35,
                        stroke_color=METAL, stroke_width=2).move_to([-1.8, y + 1.05, 0])
    stem_B = Rectangle(width=0.2, height=1.3, fill_color=METAL, fill_opacity=0.35,
                        stroke_color=METAL, stroke_width=2).move_to([0.6, y + 1.05, 0])
    stem_P = Rectangle(width=0.2, height=0.6, fill_color=METAL, fill_opacity=0.35,
                        stroke_color=METAL, stroke_width=2).move_to([-0.6, y - 1.1, 0])
    stem_T = Rectangle(width=0.2, height=0.6, fill_color=METAL, fill_opacity=0.35,
                        stroke_color=METAL, stroke_width=2).move_to([1.8, y - 1.1, 0])
    housing = VGroup(top_1, top_2, top_3, bot_1, bot_2, bot_3, stem_A, stem_B, stem_P, stem_T)

    a_top = Arrow([-1.8, y + 1.65, 0], [-1.8, y + 2.4, 0], color=OK, buff=0, stroke_width=5,
                  max_tip_length_to_length_ratio=0.3)
    b_top = Arrow([0.6, y + 1.65, 0], [0.6, y + 2.4, 0], color=OK, buff=0, stroke_width=5,
                  max_tip_length_to_length_ratio=0.3)
    p_bot = Arrow([-0.6, y - 1.85, 0], [-0.6, y - 1.35, 0], color=SUPPLY, buff=0, stroke_width=5,
                  max_tip_length_to_length_ratio=0.3)
    t_bot = Arrow([1.8, y - 1.35, 0], [1.8, y - 1.85, 0], color=RETURN, buff=0, stroke_width=5,
                  max_tip_length_to_length_ratio=0.3)
    a_lbl = Text("A", font_size=16, color=OK).next_to(a_top, UP, buff=0.08)
    b_lbl = Text("B", font_size=16, color=OK).next_to(b_top, UP, buff=0.08)
    p_lbl = Text("P", font_size=16, color=SUPPLY).next_to(p_bot, DOWN, buff=0.08)
    t_lbl = Text("T", font_size=16, color=RETURN).next_to(t_bot, DOWN, buff=0.08)
    ports = VGroup(a_top, b_top, p_bot, t_bot, a_lbl, b_lbl, p_lbl, t_lbl)

    return housing, ports


class HV08_FourWayTwoPos(SafeScene):
    """Page 8 — Four-Way Two-Position Valve."""

    def construct(self):
        ttl = title("Four-Way Two-Position Valve")
        pref = page_ref("หน้า 8 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.8
        housing, ports = four_way_housing(y)
        self.play(Create(housing), FadeIn(ports), run_time=1.4)

        spool = Rectangle(width=2.6, height=0.42, fill_color=METAL, fill_opacity=0.9,
                           stroke_color=WHITE, stroke_width=2).move_to([-0.6, y, 0])
        self.play(FadeIn(spool), run_time=0.6)

        cap1 = caption_top("ตำแหน่ง 1: P → B (ยืดกระบอกสูบ), A → T (น้ำมันฝั่งตรงข้ามไหลกลับ)")
        self.play(FadeIn(cap1), run_time=0.6)
        pathA = VMobject().set_points_as_corners([[-0.6, y - 0.9, 0], [-0.6, y, 0], [-1.8, y, 0], [-1.8, y + 1.5, 0]])
        pathB = VMobject().set_points_as_corners([[-0.6, y - 0.9, 0], [-0.6, y, 0], [0.6, y, 0], [0.6, y + 1.5, 0]])
        dotsA = VGroup(*[Dot(radius=0.05, color=RETURN) for _ in range(3)])
        dotsB = VGroup(*[Dot(radius=0.05, color=SUPPLY) for _ in range(3)])
        anims = ([MoveAlongPath(d, pathA, rate_func=linear, run_time=1.6) for d in dotsA] +
                  [MoveAlongPath(d, pathB, rate_func=linear, run_time=1.6) for d in dotsB])
        self.play(LaggedStart(*anims, lag_ratio=0.2))
        self.play(FadeOut(dotsA), FadeOut(dotsB), FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("สลับตำแหน่ง 2: P → A (หดกระบอกสูบกลับ), B → T")
        self.play(FadeIn(cap2), spool.animate.move_to([0.6, y, 0]), run_time=1.4)
        pathA2 = VMobject().set_points_as_corners([[-0.6, y - 0.9, 0], [-0.6, y, 0], [-1.8, y, 0], [-1.8, y + 1.5, 0]])
        pathT2 = VMobject().set_points_as_corners([[0.6, y + 1.5, 0], [0.6, y, 0], [1.8, y, 0], [1.8, y - 0.9, 0]])
        dotsA2 = VGroup(*[Dot(radius=0.05, color=SUPPLY) for _ in range(3)])
        dotsT2 = VGroup(*[Dot(radius=0.05, color=RETURN) for _ in range(3)])
        anims2 = ([MoveAlongPath(d, pathA2, rate_func=linear, run_time=1.6) for d in dotsA2] +
                   [MoveAlongPath(d, pathT2, rate_func=linear, run_time=1.6) for d in dotsT2])
        self.play(LaggedStart(*anims2, lag_ratio=0.2))
        self.play(FadeOut(dotsA2), FadeOut(dotsT2), run_time=0.3)

        cap3 = caption_top("มาตรฐานสำหรับคุม double-acting cylinder — สลับได้ครบ 2 ทิศ")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.4)
        self.fade_out_all(run_time=0.9)


class HV09_FourWayThreePosManual(SafeScene):
    """Page 9 — Four-Way Three-Position Valve (manual, spring centered)."""

    def construct(self):
        ttl = title("Four-Way Three-Position Valve")
        pref = page_ref("หน้า 9 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.8
        housing, ports = four_way_housing(y)
        self.play(Create(housing), FadeIn(ports), run_time=1.4)

        spring_L = spring_zigzag(-4.0, -1.4, y, coils=5, amp=0.12)
        spring_R = spring_zigzag(1.4, 4.0, y, coils=5, amp=0.12)
        spool = Rectangle(width=2.6, height=0.42, fill_color=METAL, fill_opacity=0.9,
                           stroke_color=WHITE, stroke_width=2).move_to([0, y, 0])
        self.play(FadeIn(spool), Create(spring_L), Create(spring_R), run_time=0.7)

        cap0 = caption_top("เพิ่มตำแหน่งกลาง (neutral) จากแบบ 2 ตำแหน่งในหน้าที่แล้ว")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)
        cap1 = caption_top("Spring centered: ปล่อยมือ สปริงทั้ง 2 ข้างดันสปูลกลับกลาง — ปิดกั้นทุกพอร์ต (closed center)")
        self.play(FadeOut(cap0), run_time=0.3)
        self.play(FadeIn(cap1), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("ดันคันโยกไปข้างหนึ่ง สปริงฝั่งขวาถูกอัด — P→B, A→T (เหมือนหน้า 8)")
        self.play(FadeIn(cap2), spool.animate.move_to([0.8, y, 0]), run_time=1.3)
        self.wait(1.2)

        cap3 = caption_top("ประเภท center (open/closed/tandem) — ดูรายละเอียดหน้า 13")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.4)
        self.fade_out_all(run_time=0.9)


class HV10_FourWayThreePosPilot(SafeScene):
    """Page 10 — Four-Way Three-Position Valve (air-pilot / solenoid actuated)."""

    def construct(self):
        ttl = title("Four-Way Three-Position Valve")
        pref = page_ref("หน้า 10 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.8
        housing, ports = four_way_housing(y)
        self.play(Create(housing), FadeIn(ports), run_time=1.3)

        spring_R = spring_zigzag(1.4, 4.0, y, coils=5, amp=0.12)
        spool = Rectangle(width=2.6, height=0.42, fill_color=METAL, fill_opacity=0.9,
                           stroke_color=WHITE, stroke_width=2).move_to([0, y, 0])
        coil = Rectangle(width=0.7, height=0.6, fill_color=WARN, fill_opacity=0.5,
                          stroke_color=WARN, stroke_width=2).move_to([-3.4, y, 0])
        coil_lbl = Text("โซลินอยด์", font_size=14, color=WARN).next_to(coil, DOWN, buff=0.12)
        self.play(FadeIn(spool), Create(spring_R), FadeIn(coil), FadeIn(coil_lbl), run_time=0.8)

        cap1 = caption_top("กลไกกึ่งกลางเหมือนหน้าที่แล้ว แต่เปลี่ยนตัวขับจากคันโยกเป็นโซลินอยด์")
        self.play(FadeIn(cap1), run_time=0.6)
        self.wait(1.0)

        cap2 = caption_top("โซลินอยด์ดันสปูล (ค้างตำแหน่ง) — คลายไฟ สปริงดันกลับกลางเอง")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), coil.animate.set_fill(opacity=1.0),
                   spool.animate.move_to([0.8, y, 0]), run_time=1.2)
        self.wait(0.8)
        self.play(coil.animate.set_fill(opacity=0.5), spool.animate.move_to([0, y, 0]), run_time=1.0)

        cap3 = caption_top("แบบ air-pilot: ใช้ลมอัดดันแทนโซลินอยด์ทั้งสองฝั่ง (ดูหน้า 10 ต้นฉบับ)")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.4)
        self.fade_out_all(run_time=0.9)


class HV11_SolenoidPilotOperated(SafeScene):
    """Page 11 — Solenoid Controlled Pilot Operated Four-Way Valve (2-stage)."""

    def construct(self):
        ttl = title("Solenoid Pilot Operated 4-Way Valve")
        pref = page_ref("หน้า 11 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.8
        housing, ports = four_way_housing(y)
        main_spool = Rectangle(width=2.6, height=0.42, fill_color=METAL, fill_opacity=0.9,
                                stroke_color=WHITE, stroke_width=2).move_to([0, y, 0])
        self.play(Create(housing), FadeIn(ports), FadeIn(main_spool), run_time=1.3)
        cap_main = caption_top("ด้านล่าง: Main stage — สปูลใหญ่ที่คุมการไหลจริง (เหมือนหน้า 8-10)")
        self.play(FadeIn(cap_main), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap_main), run_time=0.4)

        py = 1.6
        pilot_body = Rectangle(width=1.6, height=0.35, fill_color=METAL, fill_opacity=0.5,
                                stroke_color=METAL, stroke_width=2).move_to([0, py, 0])
        pilot_spool = Rectangle(width=0.7, height=0.3, fill_color=METAL, fill_opacity=0.9,
                                 stroke_color=WHITE, stroke_width=1.5).move_to([-0.3, py, 0])
        coil = Rectangle(width=0.5, height=0.45, fill_color=WARN, fill_opacity=0.5,
                          stroke_color=WARN, stroke_width=2).move_to([-1.5, py, 0])
        pilot_lbl = Text("Pilot stage (สปูลเล็ก โซลินอยด์ดันไหว)", font_size=14, color=GRAYTXT)
        pilot_lbl.move_to([0, py + 0.55, 0])
        self.play(FadeIn(pilot_body), FadeIn(pilot_spool), FadeIn(coil), FadeIn(pilot_lbl), run_time=0.9)

        cap1 = caption_top("สปูลใหญ่ต้องใช้แรงเยอะเกินกว่าโซลินอยด์จะดันตรงๆ ไหว จึงมี 2 ชั้น")
        self.play(FadeIn(cap1), run_time=0.6)
        self.wait(1.0)

        cap2 = caption_top("ขั้น 1: โซลินอยด์ดันสปูลไพลอต (เล็ก) ก่อน")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), coil.animate.set_fill(opacity=1.0),
                   pilot_spool.animate.move_to([0.3, py, 0]), run_time=1.0)

        pilot_line = Line([0.3, py - 0.18, 0], [0.9, y + 0.21, 0], color=WARN, stroke_width=3)
        cap3 = caption_top("ขั้น 2: แรงดันไพลอตวิ่งไปดันปลายสปูลใหญ่ — บังคับให้เลื่อน")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), Create(pilot_line), run_time=0.9)
        self.play(main_spool.animate.move_to([0.8, y, 0]), run_time=1.2)
        self.wait(0.8)

        cap4 = caption_top("สปูลใหญ่เลื่อนแล้ว → เปลี่ยนทางไหล P/A/B/T เหมือนหน้า 8-10")
        self.play(FadeOut(cap3), run_time=0.3)
        self.play(FadeIn(cap4), run_time=0.7)
        self.wait(0.8)

        cap5 = caption_top("มี manual override ไว้ดันสปูลไพลอตด้วยมือตอนซ่อม/เทสต์")
        self.play(FadeOut(cap4), run_time=0.3)
        self.play(FadeIn(cap5), run_time=0.6)
        self.wait(1.2)
        self.fade_out_all(run_time=0.9)


class HV12_SolenoidDesign(SafeScene):
    """Page 12 — Solenoid Design (air gap vs wet armature)."""

    def construct(self):
        ttl = title("Solenoid Design")
        pref = page_ref("หน้า 12 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        cap0 = caption_top("จากโซลินอยด์ที่เพิ่งเห็นในหน้าที่แล้ว — ข้างในสร้างแรงผลักยังไง?")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap0), run_time=0.4)

        def solenoid_diagram(cx, seal_kind):
            frame = Rectangle(width=1.6, height=1.3, fill_color=METAL, fill_opacity=0.3,
                               stroke_color=METAL, stroke_width=2).move_to([cx, -1.6, 0])
            coil = Rectangle(width=0.6, height=0.9, fill_color=WARN, fill_opacity=0.4,
                              stroke_color=WARN, stroke_width=2).move_to([cx + 0.35, -1.6, 0])
            armature = Rectangle(width=0.7, height=0.35, fill_color=METAL, fill_opacity=0.9,
                                  stroke_color=WHITE, stroke_width=2).move_to([cx - 0.15, -1.6, 0])
            fluid_extent = 0.55 if seal_kind == "static" else 0.15
            fluid = Rectangle(width=fluid_extent * 2, height=1.1, fill_color=PRIMARY,
                               fill_opacity=0.25, stroke_width=0).move_to([cx - 0.9 + fluid_extent, -1.6, 0])
            seal_x = cx - 0.9 + fluid_extent * 2
            seal = Line([seal_x, -1.95, 0], [seal_x, -1.25, 0], color=OK, stroke_width=4)
            seal_lbl = Text("Dynamic seal" if seal_kind == "dynamic" else "Static seal",
                             font_size=13, color=OK).move_to([cx, -2.35, 0])
            return VGroup(frame, coil, armature, fluid, seal, seal_lbl)

        left = solenoid_diagram(-3.0, "dynamic")
        right = solenoid_diagram(3.0, "static")
        left_title = Text("Air gap design", font_size=17, color=WHITE).move_to([-3.0, -0.55, 0])
        right_title = Text("Wet armature design", font_size=17, color=WHITE).move_to([3.0, -0.55, 0])

        self.play(FadeIn(left), FadeIn(left_title), run_time=0.9)
        self.play(FadeIn(right), FadeIn(right_title), run_time=0.9)

        cap1 = caption_top("Air gap: dynamic seal เคลื่อนที่ได้ (จุดสึกหรอ) — น้ำมันเข้าไม่ถึงคอยล์")
        self.play(FadeIn(cap1), run_time=0.6)
        self.wait(1.3)
        cap2 = caption_top("Wet armature: static seal อยู่กับที่ (รั่วยากกว่า) — อาร์เมเจอร์แช่น้ำมันเต็มตัว")
        self.play(FadeOut(cap1), run_time=0.3)
        self.play(FadeIn(cap2), run_time=0.6)
        self.wait(1.6)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# Batch 3: Pressure Control section (pages 14,16,17,18,19,20 — 15 already done)
# =====================================================================

RESIST = "#FF7043"  # oil forced through a throttled/resisting path (counterbalance)


class HV14_Title(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 14 · Hydraulic Valves")
        t = Text("Pressure Control Valves", font_size=40, color=WHITE)
        sub = fit_width(Text("จำกัด/ปรับ \"ระดับความดัน\" — relief, reducing, sequence, unloading, counterbalance",
                              font_size=18, color=GRAYTXT), 11.0)
        sub.next_to(t, DOWN, buff=0.6)
        self.play(FadeIn(pref), Write(t), run_time=1.3)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(1.6)
        self.fade_out_all(run_time=0.8)


def branch_t_body(y=-1.8, branch="down"):
    """T-body: horizontal bore (inlet left / outlet right) + a branch stem
    (up or down) at center — shared shape for the relief/unloading/sequence family."""
    top_wall_L = Rectangle(width=2.95, height=0.3, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([-1.825, y + 0.4, 0])
    top_wall_R = Rectangle(width=2.95, height=0.3, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([1.825, y + 0.4, 0])
    bottom_wall_L = Rectangle(width=2.95, height=0.3, fill_color=METAL, fill_opacity=0.35,
                               stroke_color=METAL, stroke_width=2).move_to([-1.825, y - 0.4, 0])
    bottom_wall_R = Rectangle(width=2.95, height=0.3, fill_color=METAL, fill_opacity=0.35,
                               stroke_color=METAL, stroke_width=2).move_to([1.825, y - 0.4, 0])
    if branch == "up":
        stem_L = Rectangle(width=0.2, height=1.3, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([-0.45, y + 1.05, 0])
        stem_R = Rectangle(width=0.2, height=1.3, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([0.45, y + 1.05, 0])
        top_wall_L.stretch_to_fit_width(2.95 - 0.2).move_to([-1.575, y + 0.4, 0])
        top_wall_R.stretch_to_fit_width(2.95 - 0.2).move_to([1.575, y + 0.4, 0])
        walls = VGroup(top_wall_L, top_wall_R, bottom_wall_L, bottom_wall_R, stem_L, stem_R)
    else:
        stem_L = Rectangle(width=0.2, height=0.7, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([-0.45, y - 0.75, 0])
        stem_R = Rectangle(width=0.2, height=0.7, fill_color=METAL, fill_opacity=0.35,
                            stroke_color=METAL, stroke_width=2).move_to([0.45, y - 0.75, 0])
        bottom_wall_L.stretch_to_fit_width(2.95 - 0.2).move_to([-1.575, y - 0.4, 0])
        bottom_wall_R.stretch_to_fit_width(2.95 - 0.2).move_to([1.575, y - 0.4, 0])
        walls = VGroup(top_wall_L, top_wall_R, bottom_wall_L, bottom_wall_R, stem_L, stem_R)
    return walls


class HV16_PilotOperatedRelief(SafeScene):
    """Page 16 — Pilot Operated Pressure Relief Valve (2-stage)."""

    def construct(self):
        ttl = title("Pilot Operated Relief Valve")
        pref = page_ref("หน้า 16 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.7
        housing = branch_t_body(y, branch="down")
        self.play(Create(housing), run_time=1.1)

        in_arrow = Arrow([-4.4, y, 0], [-2.9, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.9, y, 0], [4.4, y, 0], color=OK, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        tank_arrow = Arrow([0, y - 1.1, 0], [0, y - 1.6, 0], color=RETURN, buff=0, stroke_width=6,
                            max_tip_length_to_length_ratio=0.28)
        in_lbl = Text("Inlet (จากปั๊ม)", font_size=14, color=SUPPLY).move_to([-3.7, y - 0.6, 0])
        out_lbl = Text("Outlet (ไปวงจร)", font_size=14, color=OK).move_to([3.7, y - 0.6, 0])
        tank_lbl = Text("Tank", font_size=14, color=RETURN).move_to([0, y - 1.78, 0])
        self.play(GrowArrow(in_arrow), GrowArrow(out_arrow), GrowArrow(tank_arrow),
                   FadeIn(in_lbl), FadeIn(out_lbl), FadeIn(tank_lbl), run_time=1.1)

        piston = Rectangle(width=0.9, height=0.36, fill_color=METAL, fill_opacity=0.9,
                            stroke_color=WHITE, stroke_width=2).move_to([0, y - 0.75, 0])
        pilot_box = Rectangle(width=0.6, height=0.4, fill_color=METAL, fill_opacity=0.3,
                               stroke_color=METAL, stroke_width=2).move_to([0, y + 1.1, 0])
        pilot_poppet = Triangle(color=WHITE, fill_color=METAL, fill_opacity=0.9,
                                 stroke_width=2).scale(0.13).rotate(PI).move_to([0, y + 1.1, 0])
        pilot_lbl = Text("ไพลอตสปูลเล็ก", font_size=13, color=GRAYTXT).move_to([0, y + 1.55, 0])
        self.play(FadeIn(piston), FadeIn(pilot_box), FadeIn(pilot_poppet), FadeIn(pilot_lbl), run_time=0.8)

        cap0 = caption_top("2 ชั้นเหมือนวาล์วทิศทางหน้า 11 — แต่ตัวกระตุ้นคือความดันเอง ไม่ใช่โซลินอยด์")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(cap0), run_time=0.4)

        capA = caption_top("A. Closed: สปริงกดลูกสูบปิดกั้นทางลงถัง — inlet ไหลตรงไป outlet ปกติ")
        self.play(FadeIn(capA), run_time=0.6)
        dots = VGroup(*[Dot(radius=0.06, color=SUPPLY) for _ in range(3)])
        path = VMobject().set_points_as_corners([[-2.7, y, 0], [2.7, y, 0]])
        anims = [MoveAlongPath(d, path, rate_func=linear, run_time=1.3) for d in dots]
        self.play(LaggedStart(*anims, lag_ratio=0.3))
        self.play(FadeOut(dots), FadeOut(capA), run_time=0.4)

        capB = caption_top("B. Cracked: ถึงค่าตั้ง — ไพลอตสปูลเล็กเปิดก่อน ระบายความดันเหนือลูกสูบ")
        self.play(FadeIn(capB), pilot_poppet.animate.shift(UP * 0.12), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(capB), run_time=0.4)

        capC = caption_top("C. Relieving: ลูกสูบใหญ่เลื่อนขึ้น เปิดทางถ่ายปั๊มตรงไปถังทั้งหมด")
        self.play(FadeIn(capC), piston.animate.move_to([0, y - 0.45, 0]), run_time=1.1)
        dots2 = VGroup(*[Dot(radius=0.06, color=RETURN) for _ in range(3)])
        path2 = VMobject().set_points_as_corners([[-2.7, y, 0], [0, y, 0], [0, y - 1.6, 0]])
        anims2 = [MoveAlongPath(d, path2, rate_func=linear, run_time=1.4) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.3))
        self.play(FadeOut(dots2), run_time=0.3)

        cap_end = caption_top("ข้อดี: สปูลไพลอตเล็กคุมลูกสูบใหญ่ได้ — รับ flow มากๆ โดยสปริงไม่ต้องแข็งมาก")
        self.play(FadeOut(capC), run_time=0.3)
        self.play(FadeIn(cap_end), run_time=0.6)
        self.wait(1.5)
        self.fade_out_all(run_time=0.9)


class HV17_PressureReducing(SafeScene):
    """Page 17 — Pressure Reducing Valve (direct acting)."""

    def construct(self):
        ttl = title("Pressure Reducing Valve")
        pref = page_ref("หน้า 17 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.8

        body = Rectangle(width=5.2, height=1.1, fill_color=METAL, fill_opacity=0.3,
                          stroke_color=METAL, stroke_width=2).move_to([0, y, 0])
        self.play(Create(body), run_time=0.9)

        in_arrow = Arrow([-4.4, y, 0], [-2.6, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.6, y, 0], [4.4, y, 0], color=OK, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        in_lbl = Text("Inlet (main system)", font_size=14, color=SUPPLY).move_to([-3.5, y - 0.85, 0])
        out_lbl = Text("Outlet (reduced pressure)", font_size=14, color=OK).move_to([3.5, y - 0.85, 0])
        self.play(GrowArrow(in_arrow), GrowArrow(out_arrow), FadeIn(in_lbl), FadeIn(out_lbl), run_time=1.0)

        spring = spring_zigzag(1.3, 2.4, y, coils=5, amp=0.14)
        spool = Rectangle(width=1.8, height=0.35, fill_color=METAL, fill_opacity=0.9,
                           stroke_color=WHITE, stroke_width=2).move_to([-0.4, y, 0])
        gap_lbl = Text("ช่องเปิดกว้าง", font_size=13, color=OK).move_to([-0.4, y + 0.75, 0])
        self.play(FadeIn(spool), Create(spring), FadeIn(gap_lbl), run_time=0.8)

        cap1 = caption_top("ปกติ: สปริงดันสปูลเปิดค้างไว้เต็มที่ — ตรงข้ามกับ relief วาล์วที่ปกติปิด!")
        self.play(FadeIn(cap1), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(cap1), FadeOut(gap_lbl), run_time=0.5)

        cap2 = caption_top("outlet ความดันขึ้นถึงค่าตั้ง (feedback ป้อนกลับ) — สปูลเริ่มบีบตัวเองแคบลง")
        self.play(FadeIn(cap2), spool.animate.move_to([0.9, y, 0]).stretch(0.4, 0),
                   run_time=1.3)
        throttled_lbl = Text("ช่องแคบลง — จำกัดความดัน outlet ไม่ให้เกิน", font_size=14, color=WARN)
        throttled_lbl.move_to([0, y + 0.75, 0])
        self.play(FadeIn(throttled_lbl), run_time=0.5)
        self.wait(1.4)

        cap3 = caption_top("Reducing คุม outlet / Relief คุม inlet — ทิศทางลอจิกตรงข้ามกันเพราะคนละตัวแปร")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.6)
        self.fade_out_all(run_time=0.9)


class HV18_UnloadingValve(SafeScene):
    """Page 18 — Unloading Valve."""

    def construct(self):
        ttl = title("Unloading Valve")
        pref = page_ref("หน้า 18 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.7
        housing = branch_t_body(y, branch="down")
        self.play(Create(housing), run_time=1.0)

        in_arrow = Arrow([-4.4, y, 0], [-2.9, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.9, y, 0], [4.4, y, 0], color=OK, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        tank_arrow = Arrow([0, y - 1.1, 0], [0, y - 1.6, 0], color=RETURN, buff=0, stroke_width=6,
                            max_tip_length_to_length_ratio=0.28)
        in_lbl = Text("Primary (จากปั๊ม)", font_size=14, color=SUPPLY).move_to([-3.7, y - 0.6, 0])
        out_lbl = Text("ไปวงจรหลัก", font_size=14, color=OK).move_to([3.7, y - 0.6, 0])
        tank_lbl = Text("Tank", font_size=14, color=RETURN).move_to([0, y - 1.78, 0])
        piston = Rectangle(width=0.9, height=0.36, fill_color=METAL, fill_opacity=0.9,
                            stroke_color=WHITE, stroke_width=2).move_to([0, y - 0.75, 0])
        self.play(GrowArrow(in_arrow), GrowArrow(out_arrow), GrowArrow(tank_arrow),
                   FadeIn(in_lbl), FadeIn(out_lbl), FadeIn(tank_lbl), FadeIn(piston), run_time=1.2)

        remote_line = Line([3.9, y + 0.9, 0], [3.9, y + 2.4, 0], color=WARN, stroke_width=3)
        remote_line2 = Line([3.9, y + 2.4, 0], [0.3, y + 2.4, 0], color=WARN, stroke_width=3)
        remote_lbl = fit_width(Text("สัญญาณไพลอตจากระยะไกล (remote connection) — คนละจุดกับ inlet ตัวเอง",
                                     font_size=13, color=WARN), 8.5)
        remote_lbl.move_to([1.2, y + 2.75, 0])
        self.play(Create(remote_line), Create(remote_line2), FadeIn(remote_lbl), run_time=0.8)

        cap1 = caption_top("A. Closed: ไม่มีสัญญาณ — น้ำมันไหลผ่านฝั่ง primary ตามปกติ")
        self.play(FadeIn(cap1), run_time=0.6)
        dots = VGroup(*[Dot(radius=0.06, color=SUPPLY) for _ in range(3)])
        path = VMobject().set_points_as_corners([[-2.7, y, 0], [2.7, y, 0]])
        anims = [MoveAlongPath(d, path, rate_func=linear, run_time=1.2) for d in dots]
        self.play(LaggedStart(*anims, lag_ratio=0.3))
        self.play(FadeOut(dots), FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("B. Unloading: สัญญาณไพลอตเกินค่าตั้ง — เปิดเต็มที่ทันที (ไม่ค่อยๆ cracking แบบ relief)")
        self.play(FadeIn(cap2), piston.animate.move_to([0, y - 0.45, 0]), run_time=0.5)
        dots2 = VGroup(*[Dot(radius=0.06, color=RETURN) for _ in range(4)])
        path2 = VMobject().set_points_as_corners([[-2.7, y, 0], [0, y, 0], [0, y - 1.6, 0]])
        anims2 = [MoveAlongPath(d, path2, rate_func=linear, run_time=1.1) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.15))
        self.play(FadeOut(dots2), run_time=0.3)

        cap3 = caption_top("ต่างจาก relief ตรงที่กระตุ้นด้วยสัญญาณภายนอก ไม่ใช่ความดันตัวเอง — ประหยัดพลังงาน")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.5)
        self.fade_out_all(run_time=0.9)


class HV19_SequenceValve(SafeScene):
    """Page 19 — Sequence Valve."""

    def construct(self):
        ttl = title("Sequence Valve")
        pref = page_ref("หน้า 19 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.7
        housing = branch_t_body(y, branch="down")
        self.play(Create(housing), run_time=1.0)

        in_arrow = Arrow([-4.4, y, 0], [-2.9, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.9, y, 0], [4.4, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        sec_arrow = Arrow([0, y - 1.1, 0], [0, y - 1.6, 0], color=SECONDARY, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        in_lbl = Text("Primary line", font_size=14, color=SUPPLY).move_to([-3.7, y - 0.6, 0])
        out_lbl = Text("Primary (ต่อตรง)", font_size=13, color=SUPPLY).move_to([3.7, y - 0.6, 0])
        sec_lbl = Text("To Secondary system", font_size=13, color=SECONDARY).move_to([0.9, y - 1.78, 0])
        piston = Rectangle(width=0.9, height=0.36, fill_color=METAL, fill_opacity=0.9,
                            stroke_color=WHITE, stroke_width=2).move_to([0, y - 0.75, 0])
        self.play(GrowArrow(in_arrow), GrowArrow(out_arrow), GrowArrow(sec_arrow),
                   FadeIn(in_lbl), FadeIn(out_lbl), FadeIn(sec_lbl), FadeIn(piston), run_time=1.2)

        cap1 = caption_top("A. Closed: primary ยังไม่ถึงค่าตั้ง — ส่ง flow ไปแค่ primary เท่านั้น")
        self.play(FadeIn(cap1), run_time=0.6)
        dots = VGroup(*[Dot(radius=0.06, color=SUPPLY) for _ in range(3)])
        path = VMobject().set_points_as_corners([[-2.7, y, 0], [2.7, y, 0]])
        anims = [MoveAlongPath(d, path, rate_func=linear, run_time=1.3) for d in dots]
        self.play(LaggedStart(*anims, lag_ratio=0.3))
        self.play(FadeOut(dots), FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("B. Open: primary ถึงความดันตั้ง (งาน 1 เสร็จ/ชนสุด) — เปิดให้ไหลต่อไปยัง secondary")
        self.play(FadeIn(cap2), piston.animate.move_to([0, y - 0.45, 0]), run_time=1.0)
        dots2 = VGroup(*[Dot(radius=0.06, color=SECONDARY) for _ in range(3)])
        path2 = VMobject().set_points_as_corners([[-2.7, y, 0], [0, y, 0], [0, y - 1.6, 0]])
        anims2 = [MoveAlongPath(d, path2, rate_func=linear, run_time=1.4) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.3))
        self.play(FadeOut(dots2), run_time=0.3)

        cap3 = caption_top("ต่างจาก unloading หน้าที่แล้ว: sequence สัมผัสความดัน primary ของตัวเอง ไม่ใช่สัญญาณนอก")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.7)
        self.wait(1.6)
        self.fade_out_all(run_time=0.9)


class HV20_Counterbalance(SafeScene):
    """Page 20 — Counterbalance Valve."""

    def construct(self):
        ttl = title("Counterbalance Valve")
        pref = page_ref("หน้า 20 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        cyl = Rectangle(width=1.0, height=1.8, fill_color=METAL, fill_opacity=0.3,
                         stroke_color=METAL, stroke_width=2).move_to([2.6, 0.1, 0])
        piston_rod = Rectangle(width=0.35, height=1.0, fill_color=METAL, fill_opacity=0.9,
                                stroke_color=WHITE, stroke_width=2).move_to([2.6, -1.3, 0])
        load = Text("โหลด", font_size=14, color=GRAYTXT).move_to([2.6, -2.0, 0])
        valve_body = Rectangle(width=1.6, height=1.4, fill_color=METAL, fill_opacity=0.3,
                                stroke_color=METAL, stroke_width=2).move_to([-1.2, -0.9, 0])
        check = Circle(radius=0.12, color=WHITE, stroke_width=2).move_to([-1.55, -0.9, 0])
        spring2 = spring_zigzag(-0.9, -0.5, -0.9, coils=4, amp=0.1)
        spool2 = Rectangle(width=0.35, height=0.4, fill_color=METAL, fill_opacity=0.9,
                            stroke_color=WHITE, stroke_width=2).move_to([-0.7, -0.9, 0])

        to_valve = Arrow([-4.4, -0.9, 0], [-2.0, -0.9, 0], color=GRAYTXT, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.25)
        to_valve_lbl = Text("ไป/มาจาก directional valve", font_size=13, color=GRAYTXT).move_to([-3.3, -1.6, 0])
        up_pipe = Line([-1.2, -0.2, 0], [-1.2, 0.4, 0], color=METAL, stroke_width=3)
        to_cyl = Line([-1.2, 0.4, 0], [2.1, 0.4, 0], color=METAL, stroke_width=3)

        self.play(Create(cyl), FadeIn(piston_rod), FadeIn(load),
                   Create(valve_body), Create(check), Create(spring2), FadeIn(spool2),
                   Create(up_pipe), Create(to_cyl), GrowArrow(to_valve), FadeIn(to_valve_lbl),
                   run_time=1.6)

        cap0 = caption_top("กันโหลดหนักตกกระแทกตอนกระบอกสูบแนวตั้งลดโหลดลง")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap0), run_time=0.4)

        cap1 = caption_top("Raising: check valve เปิดอิสระ — น้ำมันไหลเข้ากระบอกสูบไม่มีแรงต้าน")
        self.play(FadeIn(cap1), run_time=0.6)
        dotsR = VGroup(*[Dot(radius=0.06, color=OK) for _ in range(3)])
        pathR = VMobject().set_points_as_corners([[-3.9, -0.9, 0], [-1.55, -0.9, 0], [-1.2, -0.2, 0], [-1.2, 0.4, 0], [2.1, 0.4, 0], [2.6, 0.4, 0]])
        animsR = [MoveAlongPath(d, pathR, rate_func=linear, run_time=1.6) for d in dotsR]
        self.play(LaggedStart(*animsR, lag_ratio=0.25))
        self.play(FadeOut(dotsR), FadeOut(cap1), run_time=0.4)

        cap2 = caption_top("Lowering: check valve ปิด — น้ำมันขาออกต้องดันผ่านวาล์วปรับ back-pressure ก่อน")
        self.play(FadeIn(cap2), run_time=0.6)
        dotsL = VGroup(*[Dot(radius=0.06, color=RESIST) for _ in range(3)])
        pathL = VMobject().set_points_as_corners([[2.6, 0.4, 0], [-1.2, 0.4, 0], [-1.2, -0.2, 0], [-0.7, -0.9, 0], [-3.9, -0.9, 0]])
        animsL = [MoveAlongPath(d, pathL, rate_func=linear, run_time=1.8) for d in dotsL]
        self.play(LaggedStart(*animsL, lag_ratio=0.25))
        self.play(FadeOut(dotsL), run_time=0.3)

        cap3 = caption_top("แรงต้านนี้ค้ำโหลดไว้ไม่ให้ตกเร็วเกิน — เทียบได้กับ cylinder cushion ใน W05")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.6)
        self.fade_out_all(run_time=0.9)


# =====================================================================
# Batch 4: Flow Control section (pages 21,22,23,24,25 — final pages)
# =====================================================================


class HV21_Title(SafeScene):
    def construct(self):
        pref = page_ref("หน้า 21 · Hydraulic Valves")
        t = Text("Flow Control Valves", font_size=40, color=WHITE)
        sub = fit_width(Text("คุม \"อัตราการไหล\" = คุมความเร็ว — needle, one-way, pressure/temp compensated",
                              font_size=18, color=GRAYTXT), 11.0)
        sub.next_to(t, DOWN, buff=0.6)
        self.play(FadeIn(pref), Write(t), run_time=1.3)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(1.6)
        self.fade_out_all(run_time=0.8)


def needle_body(cx=0, y=-1.8, gap=0.5):
    """Adjustable orifice: horizontal bore with a tapered needle descending
    into the passage from the top — gap controls how far it has narrowed."""
    body = Rectangle(width=5.0, height=0.9, fill_color=METAL, fill_opacity=0.25,
                      stroke_color=METAL, stroke_width=2).move_to([cx, y, 0])
    stem_housing = Rectangle(width=0.35, height=1.2, fill_color=METAL, fill_opacity=0.35,
                              stroke_color=METAL, stroke_width=2).move_to([cx, y + 1.0, 0])
    needle = Triangle(color=WHITE, fill_color=METAL, fill_opacity=0.9, stroke_width=2)
    needle.scale(0.22).rotate(PI).move_to([cx, y + (0.5 - gap), 0])
    return VGroup(body, stem_housing), needle


class HV22_NeedleValve(SafeScene):
    """Page 22 — Needle Valve, Q = Cv sqrt(dP/SG)."""

    def construct(self):
        ttl = title("Needle Valve")
        pref = page_ref("หน้า 22 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)

        y = -1.9
        body, needle = needle_body(0, y, gap=0.55)
        in_arrow = Arrow([-4.3, y, 0], [-2.6, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.6, y, 0], [4.3, y, 0], color=OK, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        self.play(Create(body), GrowArrow(in_arrow), GrowArrow(out_arrow), run_time=1.1)
        self.play(FadeIn(needle), run_time=0.5)

        cap0 = caption_top("เข็มปรับ (needle) เลื่อนเข้า-ออก เปลี่ยนพื้นที่ช่องแคบที่น้ำมันไหลผ่าน")
        self.play(FadeIn(cap0), run_time=0.6)
        dots1 = VGroup(*[Dot(radius=0.06, color=SUPPLY) for _ in range(4)])
        path1 = VMobject().set_points_as_corners([[-2.5, y, 0], [2.5, y, 0]])
        anims1 = [MoveAlongPath(d, path1, rate_func=linear, run_time=1.1) for d in dots1]
        self.play(LaggedStart(*anims1, lag_ratio=0.2))
        self.play(FadeOut(dots1), run_time=0.3)
        self.play(FadeOut(cap0), run_time=0.3)

        cap1 = caption_top("หมุนเข็มลงลึก — ช่องแคบลง น้ำมันไหลช้าลงชัดเจน")
        self.play(FadeIn(cap1), run_time=0.6)
        self.play(needle.animate.move_to([0, y + (0.5 - 0.15), 0]), run_time=1.0)
        dots2 = VGroup(*[Dot(radius=0.06, color=SUPPLY) for _ in range(4)])
        path2 = VMobject().set_points_as_corners([[-2.5, y, 0], [2.5, y, 0]])
        anims2 = [MoveAlongPath(d, path2, rate_func=linear, run_time=2.6) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.25))
        self.play(FadeOut(dots2), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        formula = MathTex(r"Q = C_v \sqrt{\dfrac{\Delta P}{SG_{oil}}}", font_size=34, color=WHITE)
        formula.move_to([-3.6, 0.9, 0])
        self.play(FadeIn(formula), run_time=0.7)

        axes = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=3.2, y_length=2.0,
                    axis_config={"stroke_color": GRAYTXT, "stroke_width": 2},
                    tips=False).move_to([3.1, 0.6, 0])
        curve = axes.plot(lambda x: np.sqrt(x), color=OK, x_range=[0.01, 4])
        x_lbl = Text("ΔP", font_size=14, color=GRAYTXT).next_to(axes.c2p(4, 0), RIGHT, buff=0.1)
        y_lbl = Text("Q", font_size=14, color=GRAYTXT).next_to(axes.c2p(0, 2), LEFT, buff=0.12)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.play(Create(curve), run_time=1.0)

        cap2 = caption_top("Q ไม่เป็นเส้นตรงกับ ΔP (เป็น √ΔP) — โหลดเปลี่ยน ความเร็วกระบอกสูบเปลี่ยนตาม")
        self.play(FadeIn(cap2), run_time=0.7)
        self.wait(1.8)
        self.fade_out_all(run_time=0.9)


class HV23_OneWayFlowControl(SafeScene):
    """Page 23 — One-Way Flow Control Valve (needle + check combined)."""

    def construct(self):
        ttl = title("One-Way Flow Control Valve")
        pref = page_ref("หน้า 23 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        cap0 = caption_top("รวม needle valve หน้าที่แล้ว + check valve จากหน้า 5 ไว้ในตัวเดียว")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap0), run_time=0.4)

        yN, yC = -1.1, -2.6
        body_top = Rectangle(width=5.0, height=0.55, fill_color=METAL, fill_opacity=0.25,
                              stroke_color=METAL, stroke_width=2).move_to([0, yN, 0])
        body_bot = Rectangle(width=5.0, height=0.55, fill_color=METAL, fill_opacity=0.25,
                              stroke_color=METAL, stroke_width=2).move_to([0, yC, 0])
        needle = Triangle(color=WHITE, fill_color=METAL, fill_opacity=0.9, stroke_width=2)
        needle.scale(0.16).rotate(PI).move_to([0, yN + 0.15, 0])
        check = Circle(radius=0.14, color=WHITE, stroke_width=2).move_to([0, yC, 0])
        top_lbl = Text("ทางที่ปรับความเร็วได้ (throttled)", font_size=14, color=WARN).move_to([0, yN + 0.55, 0])
        bot_lbl = Text("ทางไหลอิสระ (free flow ผ่าน check)", font_size=14, color=OK).move_to([0, yC - 0.55, 0])

        left_join = Line([-3.0, 0, 0], [-3.0, -3.4, 0], color=METAL, stroke_width=3)
        right_join = Line([3.0, 0, 0], [3.0, -3.4, 0], color=METAL, stroke_width=3)
        left_cap = Line([-3.0, yN, 0], [-2.5, yN, 0], color=METAL, stroke_width=3)
        right_cap = Line([2.5, yN, 0], [3.0, yN, 0], color=METAL, stroke_width=3)

        self.play(Create(body_top), Create(body_bot), Create(left_join), Create(right_join),
                   FadeIn(needle), Create(check), FadeIn(top_lbl), FadeIn(bot_lbl), run_time=1.5)

        cap1 = caption_top("ทิศทางหนึ่ง: ผ่านช่องแคบที่ปรับได้ — คุมความเร็วได้")
        self.play(FadeIn(cap1), run_time=0.6)
        dotsA = VGroup(*[Dot(radius=0.05, color=WARN) for _ in range(3)])
        pathA = VMobject().set_points_as_corners([[-3.0, -0.6, 0], [-3.0, yN, 0], [3.0, yN, 0], [3.0, -0.6, 0]])
        animsA = [MoveAlongPath(d, pathA, rate_func=linear, run_time=1.8) for d in dotsA]
        self.play(LaggedStart(*animsA, lag_ratio=0.3))
        self.play(FadeOut(dotsA), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("อีกทิศทาง: check valve เปิดอิสระเต็มที่ — ไหลเร็วเต็มที่ ไม่ถูกจำกัด")
        self.play(FadeIn(cap2), run_time=0.6)
        dotsB = VGroup(*[Dot(radius=0.05, color=OK) for _ in range(3)])
        pathB = VMobject().set_points_as_corners([[3.0, -3.0, 0], [3.0, yC, 0], [-3.0, yC, 0], [-3.0, -3.0, 0]])
        animsB = [MoveAlongPath(d, pathB, rate_func=linear, run_time=0.9) for d in dotsB]
        self.play(LaggedStart(*animsB, lag_ratio=0.25))
        self.play(FadeOut(dotsB), run_time=0.3)

        cap3 = caption_top("เช่น คุมความเร็วตอนยืดออก แต่หดกลับได้เร็วเต็มที่")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.6)
        self.wait(1.5)
        self.fade_out_all(run_time=0.9)


class HV24_PressureCompensated(SafeScene):
    """Page 24 — Pressure Compensated Flow Control Valve."""

    def construct(self):
        ttl = title("Pressure Compensated Flow Control")
        pref = page_ref("หน้า 24 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        y = -1.9

        comp = Rectangle(width=1.1, height=0.75, fill_color=METAL, fill_opacity=0.35,
                          stroke_color=METAL, stroke_width=2).move_to([-1.6, y, 0])
        comp_spring = spring_zigzag(-2.5, -2.15, y, coils=3, amp=0.09)
        throttle_gap = Triangle(color=WHITE, fill_color=METAL, fill_opacity=0.9, stroke_width=2)
        throttle_gap.scale(0.16).rotate(PI).move_to([0.5, y + 0.2, 0])
        throttle_body = Rectangle(width=1.3, height=0.75, fill_color=METAL, fill_opacity=0.2,
                                   stroke_color=METAL, stroke_width=2).move_to([0.5, y, 0])

        in_arrow = Arrow([-4.3, y, 0], [-2.6, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.7, y, 0], [4.3, y, 0], color=OK, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)
        sense_line = VMobject(color=WARN, stroke_width=2).set_points_as_corners(
            [[2.7, y, 0], [2.7, y + 1.3, 0], [-1.6, y + 1.3, 0], [-1.6, y + 0.55, 0]])
        sense_lbl = Text("sensing line (ป้อนความดันหลัง throttle กลับมา)", font_size=13, color=WARN)
        sense_lbl.move_to([0.5, y + 1.55, 0])

        self.play(Create(comp), Create(comp_spring), Create(throttle_body), FadeIn(throttle_gap),
                   GrowArrow(in_arrow), GrowArrow(out_arrow), run_time=1.4)
        self.play(Create(sense_line), FadeIn(sense_lbl), run_time=0.9)

        cap0 = caption_top("compensator spool คอยรักษา ΔP คร่อม throttle ให้คงที่เสมอ ไม่ว่าโหลดเปลี่ยนแค่ไหน")
        self.play(FadeIn(cap0), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(cap0), run_time=0.4)

        cap1 = caption_top("โหลดเบา: แรงต้านน้อย — compensator เลื่อนแคบชดเชย ให้ ΔP ที่ throttle เท่าเดิม")
        self.play(FadeIn(cap1), run_time=0.6)
        dots1 = VGroup(*[Dot(radius=0.06, color=OK) for _ in range(4)])
        path1 = VMobject().set_points_as_corners([[-2.5, y, 0], [2.5, y, 0]])
        anims1 = [MoveAlongPath(d, path1, rate_func=linear, run_time=1.6) for d in dots1]
        self.play(LaggedStart(*anims1, lag_ratio=0.2))
        self.play(FadeOut(dots1), run_time=0.3)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("โหลดหนัก: แรงต้านมาก — compensator เลื่อนเปิดกว้างขึ้นชดเชย Q เท่าเดิม!")
        self.play(FadeIn(cap2), comp.animate.stretch(1.3, 0), run_time=1.0)
        dots2 = VGroup(*[Dot(radius=0.06, color=OK) for _ in range(4)])
        path2 = VMobject().set_points_as_corners([[-2.5, y, 0], [2.5, y, 0]])
        anims2 = [MoveAlongPath(d, path2, rate_func=linear, run_time=1.6) for d in dots2]
        self.play(LaggedStart(*anims2, lag_ratio=0.2))
        self.play(FadeOut(dots2), run_time=0.3)

        cap3 = caption_top("ผลลัพธ์: ความเร็วกระบอกสูบไม่ขึ้นกับโหลดอีกต่อไป (ต่างจาก needle ธรรมดาหน้า 22)")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.7)
        self.wait(1.6)
        self.fade_out_all(run_time=0.9)


class HV25_PressureTempCompensated(SafeScene):
    """Page 25 — Pressure and Temperature Compensated Flow Control Valve."""

    def construct(self):
        ttl = title("P&T Compensated Flow Control", size=26)
        pref = page_ref("หน้า 25 · Hydraulic Valves")
        self.play(FadeIn(ttl), FadeIn(pref), run_time=0.7)
        cap0 = caption_top("เพิ่มการชดเชยอุณหภูมิจากกลไกหน้าที่แล้ว")
        self.play(FadeIn(cap0), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap0), run_time=0.4)

        y = -1.9
        comp = Rectangle(width=1.1, height=0.75, fill_color=METAL, fill_opacity=0.35,
                          stroke_color=METAL, stroke_width=2).move_to([-1.9, y, 0])
        throttle_body = Rectangle(width=1.3, height=0.75, fill_color=METAL, fill_opacity=0.2,
                                   stroke_color=METAL, stroke_width=2).move_to([0.1, y, 0])
        throttle_gap = Triangle(color=WHITE, fill_color=METAL, fill_opacity=0.9, stroke_width=2)
        throttle_gap.scale(0.16).rotate(PI).move_to([0.1, y + 0.2, 0])
        rod = Rectangle(width=0.18, height=1.1, fill_color=PRIMARY, fill_opacity=0.9,
                         stroke_color=WHITE, stroke_width=1.5).move_to([1.0, y + 0.9, 0])
        rod_lbl = Text("แท่งชดเชยอุณหภูมิ", font_size=13, color=GRAYTXT).move_to([1.0, y + 1.6, 0])

        in_arrow = Arrow([-4.3, y, 0], [-2.8, y, 0], color=SUPPLY, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.28)
        out_arrow = Arrow([2.9, y, 0], [4.3, y, 0], color=OK, buff=0, stroke_width=6,
                           max_tip_length_to_length_ratio=0.28)

        self.play(Create(comp), Create(throttle_body), FadeIn(throttle_gap),
                   GrowArrow(in_arrow), GrowArrow(out_arrow), run_time=1.3)
        self.play(FadeIn(rod), FadeIn(rod_lbl), run_time=0.6)

        cap1 = caption_top("น้ำมันเย็น: แท่งหดตัว (สีฟ้า) — หนืดมาก ไหลยาก")
        self.play(FadeIn(cap1), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(cap1), run_time=0.3)

        cap2 = caption_top("น้ำมันร้อนขึ้น: แท่งขยายตัว (สีแดง) ดันตำแหน่ง throttle ชดเชยความหนืดที่ลดลง")
        self.play(FadeIn(cap2), rod.animate.set_color(WARN).stretch(1.15, 1), run_time=1.2)
        self.wait(1.3)

        cap3 = caption_top("ผลลัพธ์: ความเร็วกระบอกสูบคงที่ ไม่ว่าโหลดจะเปลี่ยน หรืออุณหภูมิน้ำมันจะเปลี่ยน")
        self.play(FadeOut(cap2), run_time=0.3)
        self.play(FadeIn(cap3), run_time=0.7)
        self.wait(1.8)
        self.fade_out_all(run_time=0.9)
