"""Fresh 3-tooth brushed-DC armature winding lesson.

This is a new design and scene implementation.  It intentionally does not import or
reuse the old motor_winding.py scene code.  Only mlib.py is reused for the shared
palette, flat 3D lines/arrows, fixed-HUD handling, and timeline layout checks.

Verified content basis:
  * ROHM TechWeb: a common two-pole / three-slot brushed motor uses three commutator
    segments at 120 degrees.  Every segment joins ends from two neighbouring coils,
    so the three coils form a ring network.
  * Precision Microdrives: the three rotor windings form a triangle (delta) connected
    to the three commutator sections.
  * Purdue DC-machine animation: commutator segments rotate with the rotor while the
    brushes stay fixed and redirect armature current during rotation.
  * Nissan K11 service procedure: adjacent commutator segments should be continuous;
    a commutator bar must not be continuous to the shaft.

The four displayed turns are illustrative.  Actual gauge and turn count must come
from the original armature or a validated motor design.
"""

from manim import *
import numpy as np

from mlib import *


# ---------------------------------------------------------------------------
# Geometry truth (mirrors motor3_winding_geometry_spec.md)
CENTER = np.array([-0.85, -0.45, 0.0])
CORE_R = 0.42
TOOTH_R0 = 0.45
TOOTH_R1 = 1.28
TOOTH_W = 0.58
HALF_Z = 0.68
COMM_Z = 1.08
COMM_R = 0.50
WIRE_GAP = 0.075
N_TURNS_DEMO = 4

TOOTH_ANGLES = [PI / 2 - k * TAU / 3 for k in range(3)]
COIL_COLORS = [CURRENT, OK, FORCE]
COIL_NAMES = ["A", "B", "C"]

COPPER = "#D9792B"
COPPER_HI = "#FFB45A"
IRON = "#607782"
IRON_DARK = "#26363D"
INSULATION = "#F4D7A1"
BG = "#071014"

assert CORE_R < TOOTH_R0 < TOOTH_R1
assert HALF_Z < COMM_Z
assert len(TOOTH_ANGLES) == len(COIL_COLORS) == 3
assert [(i + 1) % 3 for i in range(3)] == [1, 2, 0]


def unit_vectors(angle):
    u = np.array([np.cos(angle), np.sin(angle), 0.0])
    v = np.array([-np.sin(angle), np.cos(angle), 0.0])
    return u, v


def set_solid_style(mob, color, opacity=1.0):
    mob.set_fill(color, opacity=opacity)
    mob.set_stroke(color=color, width=0.8, opacity=min(1.0, opacity + 0.15))
    return mob


def build_rotor(include_liners=True):
    """Native-solid rotor: hub + shaft + three derived radial teeth."""
    shaft = Cylinder(
        radius=0.12,
        height=3.05,
        direction=OUT,
        resolution=(8, 8),
    ).move_to(CENTER + OUT * 0.22)
    set_solid_style(shaft, METAL, 1.0)

    hub = Cylinder(
        radius=CORE_R,
        height=2 * HALF_Z,
        direction=OUT,
        resolution=(10, 10),
    ).move_to(CENTER)
    set_solid_style(hub, IRON_DARK, 1.0)

    teeth = VGroup()
    liners = VGroup()
    length = TOOTH_R1 - TOOTH_R0
    radial_c = (TOOTH_R1 + TOOTH_R0) / 2
    for angle in TOOTH_ANGLES:
        u, _ = unit_vectors(angle)
        tooth = Prism(dimensions=[length, TOOTH_W, 2 * HALF_Z])
        tooth.rotate(angle, axis=OUT)
        tooth.move_to(CENTER + u * radial_c)
        set_solid_style(tooth, IRON, 0.98)
        teeth.add(tooth)

        if include_liners:
            liner = Prism(dimensions=[length + 0.06, TOOTH_W + 0.10, 2 * HALF_Z + 0.06])
            liner.rotate(angle, axis=OUT)
            liner.move_to(CENTER + u * radial_c)
            set_solid_style(liner, INSULATION, 0.22)
            liners.add(liner)

    return VGroup(shaft, hub, liners, teeth), {
        "shaft": shaft,
        "hub": hub,
        "liners": liners,
        "teeth": teeth,
    }


def build_commutator():
    """Three copper arcs in the front plane, separated by visible insulation gaps."""
    bars = VGroup()
    labels = VGroup()
    span = TAU / 3 - 0.14
    for i, angle in enumerate(TOOTH_ANGLES):
        bar = Arc(
            radius=COMM_R,
            start_angle=angle - span / 2,
            angle=span,
            arc_center=CENTER + OUT * COMM_Z,
            color=COPPER,
            stroke_width=15,
        )
        bars.add(bar)
        p = CENTER + OUT * (COMM_Z + 0.02) + (COMM_R + 0.31) * np.array(
            [np.cos(angle), np.sin(angle), 0.0]
        )
        labels.add(Text(str(i + 1), font_size=19, color=COPPER_HI).move_to(p))
    return bars, labels


def comm_point(index, radial_scale=0.92):
    angle = TOOTH_ANGLES[index]
    u, _ = unit_vectors(angle)
    return CENTER + u * (COMM_R * radial_scale) + OUT * COMM_Z


def coil_points(tooth_index, turns=N_TURNS_DEMO):
    """Point-by-point physical path; same points drive both static and moving marks."""
    angle = TOOTH_ANGLES[tooth_index]
    u, v = unit_vectors(angle)
    start_bar = tooth_index
    end_bar = (tooth_index + 1) % 3
    points = [comm_point(start_bar)]

    for turn in range(turns):
        radial = 0.78 + (turn - (turns - 1) / 2) * WIRE_GAP
        half_wrap = TOOTH_W / 2 + 0.095
        front_left = CENTER + u * radial - v * half_wrap + OUT * HALF_Z
        back_left = CENTER + u * radial - v * half_wrap - OUT * HALF_Z
        back_right = CENTER + u * radial + v * half_wrap - OUT * HALF_Z
        front_right = CENTER + u * radial + v * half_wrap + OUT * HALF_Z
        points.extend([front_left, back_left, back_right, front_right])

    points.append(comm_point(end_bar))

    # Geometry assertions: each actual turn reaches exact front and back planes.
    for turn in range(turns):
        base = 1 + turn * 4
        assert np.isclose(points[base][2], HALF_Z)
        assert np.isclose(points[base + 1][2], -HALF_Z)
        assert np.isclose(points[base + 2][2], -HALF_Z)
        assert np.isclose(points[base + 3][2], HALF_Z)
    return points


def path_segments(points, color, thickness=0.026):
    return VGroup(
        *[
            line3(points[i], points[i + 1], color, thickness=thickness)
            for i in range(len(points) - 1)
        ]
    )


def build_coil(tooth_index, color=None, turns=N_TURNS_DEMO):
    color = color or COIL_COLORS[tooth_index]
    pts = coil_points(tooth_index, turns=turns)
    segs = path_segments(pts, color)
    endpoints = VGroup(
        Dot(pts[0], radius=0.07, color=color),
        Dot(pts[-1], radius=0.07, color=color),
    )
    return VGroup(segs, endpoints), segs, endpoints, pts


def triangle_schematic(scale=1.0, center=np.array([4.2, -0.45, 0.0])):
    """Fixed-frame delta/ring equivalent circuit with safe direct labels."""
    p = [
        center + scale * np.array([0.0, 1.35, 0.0]),
        center + scale * np.array([-1.15, -0.75, 0.0]),
        center + scale * np.array([1.15, -0.75, 0.0]),
    ]
    edges = VGroup(
        Line(p[0], p[1], color=COIL_COLORS[0], stroke_width=8),
        Line(p[1], p[2], color=COIL_COLORS[1], stroke_width=8),
        Line(p[2], p[0], color=COIL_COLORS[2], stroke_width=8),
    )
    coil_labs = VGroup(
        Text("ขด A", font_size=20, color=COIL_COLORS[0]).move_to(center + [-1.02, 0.38, 0]),
        Text("ขด B", font_size=20, color=COIL_COLORS[1]).move_to(center + [0.0, -1.10, 0]),
        Text("ขด C", font_size=20, color=COIL_COLORS[2]).move_to(center + [1.02, 0.38, 0]),
    )
    bar_labs = VGroup(
        Text("บาร์ 1", font_size=18, color=COPPER_HI).next_to(p[0], UP, buff=0.12),
        Text("บาร์ 2", font_size=18, color=COPPER_HI).next_to(p[1], DOWN + LEFT, buff=0.12),
        Text("บาร์ 3", font_size=18, color=COPPER_HI).next_to(p[2], DOWN + RIGHT, buff=0.12),
    )
    nodes = VGroup(*[Dot(q, radius=0.07, color=COPPER_HI) for q in p])
    return VGroup(edges, nodes, coil_labs, bar_labs), edges, nodes


def top_header(scene, episode, title_text, caption_text):
    ttl = scene.hud(title(title_text, size=27))
    ref = scene.hud(page_ref(episode, size=16))
    cap = scene.hud(caption_top(caption_text, size=21, max_w=10.8))
    scene.play(FadeIn(ttl, shift=DOWN * 0.22), FadeIn(ref), FadeIn(cap, shift=UP * 0.20), run_time=0.9)
    return ttl, ref, cap


def new_caption(scene, old, text, color=GRAYTXT, size=21):
    nxt = scene.hud(caption_top(text, color=color, size=size, max_w=10.8))
    scene.play(ReplacementTransform(old, nxt), run_time=0.7)
    return nxt


def screen_callout(scene, label, start, end, color=OK, size=17):
    arrow = Arrow(start, end, buff=0.08, color=color, stroke_width=4, tip_length=0.18)
    txt = Text(label, font_size=size, color=color).next_to(start, LEFT if start[0] < 0 else RIGHT, buff=0.12)
    group = VGroup(arrow, txt)
    scene.hud(group)
    return group


# ===========================================================================
# Scene 1 — identify the machine and the electrical map before touching wire.
class M3W01_Architecture(SafeThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.96)
        _, _, cap = top_header(
            self,
            "บท 1/5 · อ่านแผนก่อนพัน",
            "มอเตอร์ 3 ซี่ — ชิ้นส่วนไหนต่อถึงอะไร",
            "เริ่มจากแผนที่ก่อน: 3 ฟัน + 3 ขด + คอมมิวเตเตอร์ 3 บาร์",
        )

        rotor, parts = build_rotor(include_liners=True)
        bars, bar_nums = build_commutator()
        self.world_text(bar_nums)
        assembly = VGroup(rotor, bars, bar_nums)
        self.play(FadeIn(assembly, shift=IN * 0.16), run_time=1.4)
        self.wait(0.6)

        c1 = screen_callout(self, "ฟันอาร์เมเจอร์", [-5.45, 0.75, 0], [-2.55, 0.15, 0], CURRENT)
        c2 = screen_callout(self, "ฉนวนรองลวด", [-5.35, -0.20, 0], [-2.25, -0.65, 0], INSULATION)
        c3 = screen_callout(self, "คอมมิวเตเตอร์ 3 บาร์", [2.25, 1.15, 0], [0.30, 0.15, 0], COPPER_HI)
        c4 = screen_callout(self, "เพลา", [2.25, -1.20, 0], [0.05, -1.05, 0], METAL)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in (c1, c2, c3, c4)], lag_ratio=0.16), run_time=1.3)
        self.wait(1.4)
        self.play(FadeOut(VGroup(c1, c2, c3, c4)), run_time=0.5)

        cap = new_caption(self, cap, "แต่ละขดอยู่ระหว่างบาร์ที่ติดกัน: A = 1→2, B = 2→3, C = 3→1", OK)
        assembly.generate_target()
        assembly.target.scale(0.95).shift(LEFT * 1.75)
        self.play(MoveToTarget(assembly), run_time=1.0)

        tri, edges, nodes = triangle_schematic(scale=0.88, center=np.array([3.75, -0.35, 0]))
        self.hud(tri)
        self.play(Create(edges), FadeIn(nodes), run_time=1.0)
        self.play(FadeIn(VGroup(*tri[2:])), run_time=0.8)
        self.wait(1.2)

        cap = new_caption(self, cap, "สามขดปิดเป็นวงสามเหลี่ยม — ทุกบาร์จึงรับปลายสายจากขดข้างเคียง 2 เส้น", CURRENT)
        self.play(LaggedStart(*[Indicate(n, color=COPPER_HI, scale_factor=1.35) for n in nodes], lag_ratio=0.22), run_time=1.4)
        self.wait(1.7)

        note = self.hud(Text(
            "สี A/B/C ใช้เพื่อสอนเท่านั้น — ลวดจริงเป็นลวดทองแดงเคลือบเหมือนกัน",
            font_size=18,
            color=GRAYTXT,
        ).move_to([0, -2.82, 0]))
        self.play(FadeIn(note, shift=UP * 0.18), run_time=0.7)
        self.wait(2.0)


# ===========================================================================
# Scene 2 — one coil, literally drawn point by point around the tooth.
class M3W02_OneCoilPath(SafeThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=68 * DEGREES, theta=-38 * DEGREES, zoom=1.12)
        _, _, cap = top_header(
            self,
            "บท 2/5 · เส้นทางขด A",
            "หนึ่งรอบเดินสายอย่างไร",
            "ขด A เริ่มที่บาร์ 1 และจบที่บาร์ 2 — ทุกช่วงต้องตามได้ด้วยตา",
        )

        rotor, parts = build_rotor(include_liners=True)
        bars, bar_nums = build_commutator()
        self.world_text(bar_nums)
        other_teeth = VGroup(parts["teeth"][1], parts["teeth"][2])
        other_liners = VGroup(parts["liners"][1], parts["liners"][2])
        other_teeth.set_opacity(0.18)
        other_liners.set_opacity(0.08)
        parts["hub"].set_opacity(0.28)
        self.play(FadeIn(rotor), Create(bars), FadeIn(bar_nums), run_time=1.2)

        points = coil_points(0, turns=1)
        marks = VGroup(*[Dot(p, radius=0.055, color=CURRENT) for p in points])
        labels = VGroup()
        label_text = ["บาร์ 1", "หน้า-ซ้าย", "หลัง-ซ้าย", "หลัง-ขวา", "หน้า-ขวา", "บาร์ 2"]
        label_offsets = [UP, LEFT, LEFT, RIGHT, RIGHT, DOWN]
        for p, txt, direction in zip(points, label_text, label_offsets):
            lab = Text(txt, font_size=13, color=CURRENT).next_to(p, direction, buff=0.07)
            labels.add(lab)
        self.world_text(labels)

        self.play(LaggedStart(*[FadeIn(m, scale=1.8) for m in marks], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(labels), run_time=0.7)
        self.wait(0.8)

        one_turn = path_segments(points, CURRENT, thickness=0.035)
        phrases = [
            "1) ยึดต้นลวดที่บาร์ 1 แล้วพาเข้าด้านหน้าฟัน",
            "2) ลงตามแกนเพลาไปด้านหลัง — ไม่ลากเฉียงตัดกลางฟัน",
            "3) ข้ามด้านหลังไปอีกฝั่งของฟัน",
            "4) กลับขึ้นมาด้านหน้า จึงครบหนึ่งรอบ",
            "5) เมื่อได้จำนวนรอบที่ต้องการ จึงพาปลายไปบาร์ 2",
        ]
        for i, seg in enumerate(one_turn):
            cap = new_caption(self, cap, phrases[i], CURRENT if i in (0, 4) else GRAYTXT, size=20)
            self.play(Create(seg), Indicate(marks[i + 1], color=WARN, scale_factor=1.35), run_time=0.8)
            self.wait(0.35)

        self.play(FadeOut(VGroup(one_turn, marks, labels)), run_time=0.5)
        cap = new_caption(self, cap, "ทำซ้ำเส้นทางเดิม 4 รอบในภาพ — ของจริงต้องใช้จำนวนรอบตามแบบเดิม", WARN)
        coil, segs, ends, _ = build_coil(0, color=CURRENT, turns=N_TURNS_DEMO)
        self.play(FadeIn(ends[0], scale=1.8), run_time=0.35)
        self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.18), run_time=3.4)
        self.play(FadeIn(ends[1], scale=1.8), run_time=0.35)
        self.wait(1.0)

        cap = new_caption(self, cap, "กฎสำคัญ: ลวดเคลือบต้องไม่ถลอก และทุกขดต้องพันในทิศเดียวกัน", OK)
        self.play(Indicate(coil, color=OK, scale_factor=1.03), run_time=1.1)
        self.wait(2.0)


# ===========================================================================
# Scene 3 — repeat the same operation after each 120-degree index rotation.
class M3W03_RepeatThree(SafeThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=62 * DEGREES, theta=-44 * DEGREES, zoom=0.98)
        _, _, cap = top_header(
            self,
            "บท 3/5 · พันครบ 3 ขด",
            "หมุน 120° แล้วทำซ้ำ",
            "ใช้จำนวนรอบและทิศการพันเท่ากันทุกซี่ — ต่างกันแค่คู่บาร์ต้นและปลาย",
        )

        rotor, _ = build_rotor(include_liners=True)
        bars, bar_nums = build_commutator()
        self.world_text(bar_nums)
        machine = VGroup(rotor, bars, bar_nums)
        self.play(FadeIn(machine), run_time=1.1)

        rail = self.hud(VGroup(
            Text("A  1→2", font_size=20, color=COIL_COLORS[0]),
            Text("B  2→3", font_size=20, color=COIL_COLORS[1]),
            Text("C  3→1", font_size=20, color=COIL_COLORS[2]),
        ).arrange(RIGHT, buff=0.65).move_to([0, -2.80, 0]))
        self.play(FadeIn(rail, shift=UP * 0.15), run_time=0.6)

        for i in range(3):
            coil, segs, ends, _ = build_coil(i, color=COIL_COLORS[i])
            if i:
                coil.rotate(-i * TAU / 3, axis=OUT, about_point=CENTER)
            cap = new_caption(
                self,
                cap,
                f"ขด {COIL_NAMES[i]}: บาร์ {i + 1} → พันรอบฟัน → บาร์ {((i + 1) % 3) + 1}",
                COIL_COLORS[i],
            )
            self.play(Indicate(rail[i], color=COIL_COLORS[i], scale_factor=1.16), run_time=0.45)
            self.play(FadeIn(ends[0], scale=1.7), run_time=0.25)
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.14), run_time=2.6)
            self.play(FadeIn(ends[1], scale=1.7), run_time=0.25)
            machine.add(coil)
            self.wait(0.55)
            if i < 2:
                cap = new_caption(self, cap, "ล็อกขดเดิมไว้ แล้วหมุนโรเตอร์ 120° เพื่อนำซี่ถัดไปมาที่ตำแหน่งทำงาน", WARN)
                self.play(Rotating(machine, angle=-TAU / 3, axis=OUT, about_point=CENTER, run_time=1.35, rate_func=smooth))
                self.wait(0.35)

        cap = new_caption(self, cap, "ขด C จบที่บาร์ 1 — วง 1→2→3→1 ปิดครบพอดี", OK)
        self.play(Rotating(machine, angle=-TAU / 3, axis=OUT, about_point=CENTER, run_time=1.2, rate_func=smooth))
        self.wait(0.4)

        machine.generate_target()
        machine.target.scale(0.90).shift(LEFT * 1.82)
        self.play(MoveToTarget(machine), run_time=0.9)
        tri, edges, nodes = triangle_schematic(scale=0.88, center=np.array([3.75, -0.35, 0]))
        self.hud(tri)
        self.play(Create(edges), FadeIn(VGroup(nodes, tri[2], tri[3])), run_time=1.1)
        self.play(LaggedStart(*[Indicate(e, color=e.get_color(), scale_factor=1.04) for e in edges], lag_ratio=0.2), run_time=1.4)
        self.wait(2.0)


# ===========================================================================
# Scene 4 — the electrical and mechanical checks before power.
class M3W04_ElectricalChecks(SafeScene):
    def construct(self):
        self.camera.background_color = BG
        ttl = title("ตรวจให้ผ่านก่อนจ่ายไฟ", size=29)
        ref = page_ref("บท 4/5 · ตรวจงาน", size=16)
        cap = caption_top("ลวดดูสวยยังไม่พอ — ต้องพิสูจน์ว่าวงครบและไม่แตะแกนเหล็ก", size=21)
        self.play(FadeIn(ttl, shift=DOWN * 0.2), FadeIn(ref), FadeIn(cap, shift=UP * 0.2), run_time=0.9)

        center = np.array([-3.35, -0.45, 0.0])
        angles = [PI / 2 - k * TAU / 3 for k in range(3)]
        ring = VGroup()
        nums = VGroup()
        for i, angle in enumerate(angles):
            arc = Arc(radius=1.25, start_angle=angle - 0.90, angle=1.80, arc_center=center, color=COPPER, stroke_width=18)
            ring.add(arc)
            nums.add(Text(str(i + 1), font_size=22, color=COPPER_HI).move_to(center + 1.62 * np.array([np.cos(angle), np.sin(angle), 0])))
        shaft = Circle(radius=0.23, color=METAL, fill_color=METAL, fill_opacity=0.8).move_to(center)

        meter = RoundedRectangle(width=3.55, height=2.45, corner_radius=0.22, color=METAL, fill_color=IRON_DARK, fill_opacity=0.96).move_to([2.75, -0.25, 0])
        display = RoundedRectangle(width=2.65, height=0.70, corner_radius=0.10, color=OK, fill_color=BLACK, fill_opacity=0.92).move_to([2.75, 0.25, 0])
        reading = Text("R12 ≈ R23 ≈ R31", font_size=25, color=OK).move_to(display)
        self.play(Create(ring), FadeIn(nums), FadeIn(shaft), FadeIn(VGroup(meter, display, reading)), run_time=1.2)

        p0 = center + 1.25 * np.array([np.cos(angles[0]), np.sin(angles[0]), 0])
        p1 = center + 1.25 * np.array([np.cos(angles[1]), np.sin(angles[1]), 0])
        probes = VGroup(
            Line([0.95, -0.35, 0], p0, color=EMF, stroke_width=4),
            Line([0.95, -0.65, 0], p1, color=BLACK, stroke_width=5),
        )
        step1 = Text("1  คู่บาร์ทั้ง 3 คู่ต้องมีค่าต่ำและใกล้เคียงกัน", font_size=22, color=OK).move_to([2.55, -1.85, 0])
        self.play(Create(probes), FadeIn(step1, shift=UP * 0.16), run_time=0.9)
        self.wait(1.4)

        cap2 = caption_top("ถ้าคู่หนึ่งขาดหรือค่าต่างมาก ให้ย้อนดูจุดขูดเคลือบและรอยบัดกรี", color=WARN, size=21)
        self.play(ReplacementTransform(cap, cap2), run_time=0.7)
        self.wait(1.2)

        p2 = center + 1.25 * np.array([np.cos(angles[2]), np.sin(angles[2]), 0])
        probes2 = VGroup(
            Line([0.95, -0.35, 0], p2, color=EMF, stroke_width=4),
            Line([0.95, -0.65, 0], center, color=BLACK, stroke_width=5),
        )
        reading2 = Text("OL  /  ไม่ต่อ", font_size=28, color=FORCE).move_to(display)
        step2 = Text("2  บาร์ทุกอันต้องไม่ต่อถึงเพลาหรือแกนเหล็ก", font_size=22, color=FORCE).move_to([2.55, -2.35, 0])
        self.play(ReplacementTransform(probes, probes2), ReplacementTransform(reading, reading2), FadeIn(step2, shift=UP * 0.16), run_time=0.9)
        self.play(Indicate(shaft, color=WARN, scale_factor=1.35), run_time=0.7)
        self.wait(1.2)

        cap3 = caption_top("จากนั้นหมุนด้วยมือ: ต้องลื่น ไม่มีลวดขูดแม่เหล็กหรือโครง", size=21)
        self.play(ReplacementTransform(cap2, cap3), Rotate(ring, angle=TAU / 3, about_point=center, run_time=1.1), run_time=1.1)
        self.wait(1.0)

        cap4 = caption_top("ทดลองครั้งแรกด้วยแรงดันต่ำและจำกัดกระแส — หยุดทันทีถ้าร้อน กลิ่นไหม้ หรือกระแสพุ่ง", color=WARN, size=20)
        supply = VGroup(
            RoundedRectangle(width=3.2, height=1.25, corner_radius=0.18, color=WARN, fill_color="#2A1714", fill_opacity=0.95),
            Text("LOW V · CURRENT LIMIT", font_size=21, color=WARN),
        ).arrange(DOWN, buff=-0.42).move_to([2.75, -0.55, 0])
        self.play(ReplacementTransform(cap3, cap4), FadeOut(VGroup(meter, display, reading2)), FadeIn(supply, shift=UP * 0.2), run_time=0.9)
        self.wait(2.3)


# ===========================================================================
# Scene 5 — commutator/brush cause-and-effect, not just a finishing beauty shot.
class M3W05_Commutation(SafeScene):
    def construct(self):
        self.camera.background_color = BG
        ttl = title("ทำไมต่อ 1→2→3→1 แล้วมอเตอร์หมุน", size=27)
        ref = page_ref("บท 5/5 · การคอมมิวเตต", size=16)
        cap = caption_top("แปรงถ่านอยู่นิ่ง แต่คอมมิวเตเตอร์หมุนผ่านและเลือกคู่ขดใหม่", size=21)
        self.play(FadeIn(ttl, shift=DOWN * 0.2), FadeIn(ref), FadeIn(cap, shift=UP * 0.2), run_time=0.9)

        c = np.array([-1.25, -0.45, 0.0])
        stator_n = RoundedRectangle(width=1.15, height=4.1, corner_radius=0.18, color=EMF, fill_color=EMF, fill_opacity=0.72).move_to([-5.6, -0.45, 0])
        stator_s = RoundedRectangle(width=1.15, height=4.1, corner_radius=0.18, color=FIELD, fill_color=FIELD, fill_opacity=0.72).move_to([3.1, -0.45, 0])
        nlab = Text("N", font_size=48, color=WHITE).move_to(stator_n)
        slab = Text("S", font_size=48, color=WHITE).move_to(stator_s)

        field = VGroup(*[
            Arrow([-4.7, y, 0], [2.2, y, 0], buff=0, color=FIELD, stroke_width=3, tip_length=0.17).set_opacity(0.42)
            for y in np.linspace(-1.7, 0.8, 5)
        ])

        rotor_ring = Circle(radius=2.05, color=IRON, fill_color=IRON_DARK, fill_opacity=0.72, stroke_width=5).move_to(c)
        spokes = VGroup(*[
            Line(c + 0.35 * np.array([np.cos(a), np.sin(a), 0]), c + 1.78 * np.array([np.cos(a), np.sin(a), 0]), color=IRON, stroke_width=18)
            for a in TOOTH_ANGLES
        ])
        coils = VGroup(*[
            Arc(radius=1.55, start_angle=TOOTH_ANGLES[i] - 0.65, angle=1.30, arc_center=c, color=COIL_COLORS[i], stroke_width=13)
            for i in range(3)
        ])
        comm = VGroup(*[
            Arc(radius=0.56, start_angle=TOOTH_ANGLES[i] - 0.88, angle=1.76, arc_center=c, color=COPPER, stroke_width=16)
            for i in range(3)
        ])
        rotor = VGroup(rotor_ring, spokes, coils, comm)

        brush_l = RoundedRectangle(width=0.75, height=0.34, corner_radius=0.08, color=GRAYTXT, fill_color=GRAYTXT, fill_opacity=0.95).move_to(c + LEFT * 0.92)
        brush_r = brush_l.copy().move_to(c + RIGHT * 0.92)
        plus_c = brush_l.get_center() + LEFT * 0.58
        minus_c = brush_r.get_center() + RIGHT * 0.58
        plus = VGroup(
            Line(plus_c + LEFT * 0.10, plus_c + RIGHT * 0.10, color=EMF, stroke_width=4),
            Line(plus_c + DOWN * 0.10, plus_c + UP * 0.10, color=EMF, stroke_width=4),
        )
        minus = Line(minus_c + LEFT * 0.10, minus_c + RIGHT * 0.10, color=FIELD, stroke_width=4)

        self.play(FadeIn(VGroup(stator_n, stator_s, nlab, slab, field)), FadeIn(rotor), FadeIn(VGroup(brush_l, brush_r, plus, minus)), run_time=1.3)
        self.wait(0.7)

        legend = VGroup(
            Text("แปรง: อยู่นิ่ง", font_size=19, color=GRAYTXT),
            Text("คอมมิวเตเตอร์ + ขดลวด: หมุนไปกับเพลา", font_size=19, color=COPPER_HI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fit_width(legend, 2.95).move_to([5.30, 0.75, 0])
        self.play(FadeIn(legend, shift=LEFT * 0.2), run_time=0.7)
        self.play(Indicate(VGroup(brush_l, brush_r), color=WARN, scale_factor=1.18), run_time=0.8)

        for i in range(3):
            cap_next = caption_top(
                f"ตำแหน่ง {i + 1}: แปรงแตะบาร์คนละด้าน → คู่ขดที่รับกระแสเปลี่ยน แต่แรงบิดยังคงทิศเดิม",
                color=COIL_COLORS[i],
                size=20,
            )
            self.play(ReplacementTransform(cap, cap_next), Indicate(coils[i], color=COIL_COLORS[i], scale_factor=1.08), run_time=0.9)
            cap = cap_next
            self.wait(0.65)
            if i < 2:
                self.play(Rotate(rotor, angle=-TAU / 3, about_point=c, run_time=1.15, rate_func=smooth))

        torque = Arc(radius=2.45, start_angle=0.10, angle=-1.35, arc_center=c, color=TORQUE, stroke_width=8).add_tip(tip_length=0.25, tip_width=0.20)
        cap2 = caption_top("นี่คือหน้าที่ของคอมมิวเตเตอร์: สลับวงจรให้สนามโรเตอร์นำสนามแม่เหล็กอยู่เสมอ", color=OK, size=20)
        self.play(ReplacementTransform(cap, cap2), Create(torque), run_time=1.0)
        self.play(Rotate(rotor, angle=-TAU * 0.72, about_point=c, run_time=2.2, rate_func=linear))
        self.wait(0.6)

        recap = VGroup(
            Text("จำสั้น ๆ", font_size=32, color=WHITE),
            Text("1→2  ·  2→3  ·  3→1", font_size=34, color=COPPER_HI),
            Text("รอบเท่ากัน · ทิศเท่ากัน · ไม่ลงกราวด์ที่แกน", font_size=23, color=OK),
        ).arrange(DOWN, buff=0.22)
        fit_width(recap, 3.55).move_to([4.88, -1.28, 0])
        box = SurroundingRectangle(recap, color=OK, buff=0.28, corner_radius=0.18, fill_color=BLACK, fill_opacity=0.86)
        self.play(FadeOut(VGroup(stator_s, slab, legend)), run_time=0.4)
        self.play(FadeIn(VGroup(box, recap), shift=UP * 0.2), run_time=0.7)
        self.wait(2.4)
