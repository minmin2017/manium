from manim import *
import numpy as np

Text.set_default(font="Noto Sans Thai")

# ── palette (เข้ากับสไตล์โปรเจกต์) ─────────────────────────────
PRESSURE = "#29B6F6"   # ลมที่มีแรงดัน (สีฟ้า)
EXHAUST  = "#FF7043"   # ลมระบายออก (สีส้ม)
METAL    = "#546E7A"   # โลหะ
METAL_LT = "#90A4AE"
PISTON_C = "#FFD54F"   # ลูกสูบ
ROD_C    = "#ECEFF1"
GREENOK  = "#66BB6A"
GRAYTXT  = "#B0BEC5"
SUPPLY_C = "#26C6DA"


def tube(points, color=METAL_LT, width=6):
    """สร้างท่อ (เส้นต่อเนื่อง) ที่ใช้กับ MoveAlongPath ได้"""
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in points])
    m.set_stroke(color, width)
    return m


def silencer(point, direction):
    """สามเหลี่ยมระบายลม (exhaust) ชี้ออกตาม direction"""
    tip = np.array([point[0], point[1], 0]) + direction * 0.45
    base = np.array([point[0], point[1], 0])
    perp = np.array([-direction[1], direction[0], 0]) * 0.22
    tri = Polygon(base + perp, base - perp, tip,
                  stroke_color=METAL_LT, stroke_width=3, fill_opacity=0)
    return tri


class ValveLesson(Scene):
    def construct(self):
        self.intro()
        self.explain_cylinder()
        self.explain_valve()
        self.build_circuit()
        self.run_cycle()
        self.outro()

    # ── INTRO ────────────────────────────────────────────────
    def intro(self):
        title = Text("วาล์วควบคุมทิศทาง 5/2", font_size=56, color=PRESSURE)
        sub = Text("ทำงานยังไง? (อธิบายตั้งแต่ศูนย์)", font_size=30, color=GRAYTXT)
        VGroup(title, sub).arrange(DOWN, buff=0.4)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, sub)))

    # ── PART 1 : กระบอกสูบ ───────────────────────────────────
    def explain_cylinder(self):
        header = self._header("① กระบอกสูบ Double-Acting", PISTON_C)
        self.play(FadeIn(header, shift=DOWN * 0.3))

        cyl = self._make_cylinder()
        cyl["all"].move_to(ORIGIN + UP * 0.3)
        bw = 3.8
        cyl["portA"] = cyl["barrel"].get_bottom() + LEFT * (bw * 0.28)
        cyl["portB"] = cyl["barrel"].get_bottom() + RIGHT * (bw * 0.28)
        self.play(FadeIn(cyl["barrel"]), FadeIn(cyl["piston"]),
                  FadeIn(cyl["rod"]), run_time=0.8)

        # ป้ายอธิบาย 2 ช่องลม
        a_lbl = Text("ช่องซ้าย\n(ดันออก)", font_size=20, color=PRESSURE,
                     line_spacing=0.7).next_to(cyl["portA"], DOWN, buff=0.5)
        b_lbl = Text("ช่องขวา\n(ดันเข้า)", font_size=20, color=EXHAUST,
                     line_spacing=0.7).next_to(cyl["portB"], DOWN, buff=0.5)
        aA = Arrow(a_lbl.get_top(), cyl["portA"], buff=0.1,
                   color=PRESSURE, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        aB = Arrow(b_lbl.get_top(), cyl["portB"], buff=0.1,
                   color=EXHAUST, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        self.play(GrowArrow(aA), Write(a_lbl))
        self.play(GrowArrow(aB), Write(b_lbl))

        note = Text("ลมเข้าช่องไหน → ลูกสูบถูกดันไปอีกฝั่ง", font_size=22,
                    color=GRAYTXT).to_edge(DOWN, buff=0.35)
        self.play(Write(note))

        # โชว์การเลื่อน
        self.play(cyl["mover"].animate.shift(RIGHT * 1.2), run_time=1.0)
        self.play(cyl["mover"].animate.shift(LEFT * 1.2), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(cyl["all"], a_lbl, b_lbl, aA, aB, note, header)))

    # ── PART 2 : วาล์ว 5/2 ───────────────────────────────────
    def explain_valve(self):
        header = self._header("② วาล์ว 5/2 = 5 รู, 2 ตำแหน่ง", PRESSURE)
        self.play(FadeIn(header, shift=DOWN * 0.3))

        v = self._make_valve()
        v["all"].move_to(ORIGIN + DOWN * 0.2)
        box_a, box_b = v["box_a"], v["box_b"]
        v["p4"] = np.array([box_a.get_center()[0], box_a.get_top()[1], 0])
        v["p2"] = np.array([box_b.get_center()[0], box_b.get_top()[1], 0])
        v["p1"] = np.array([0, v["frame"].get_bottom()[1], 0])
        v["p5"] = box_a.get_left()
        v["p3"] = box_b.get_right()
        self.play(Create(v["frame"]), run_time=0.8)
        self.play(FadeIn(v["divider"]))

        # อธิบาย "2 ตำแหน่ง"
        pos_lbl = Text("2 ช่อง = 2 ตำแหน่งการทำงาน", font_size=22, color=GRAYTXT)
        pos_lbl.next_to(v["frame"], UP, buff=0.4)
        self.play(Write(pos_lbl))
        self.play(Indicate(v["box_a"], color=GREENOK, scale_factor=1.05),
                  Indicate(v["box_b"], color=GREENOK, scale_factor=1.05))
        self.wait(0.5)
        self.play(FadeOut(pos_lbl))

        # ป้าย 5 รู
        labels = [
            ("1 = ลมเข้า (Supply)", v["p1"], DOWN, SUPPLY_C),
            ("4 = ไปกระบอก", v["p4"], LEFT, PRESSURE),
            ("2 = ไปกระบอก", v["p2"], RIGHT, EXHAUST),
            ("5 = ระบายออก", v["p5"], LEFT, GRAYTXT),
            ("3 = ระบายออก", v["p3"], RIGHT, GRAYTXT),
        ]
        anims = []
        keep = VGroup()
        for txt, pt, d, col in labels:
            t = Text(txt, font_size=18, color=col).next_to(pt, d, buff=0.35)
            dot = Dot(pt, color=col, radius=0.07)
            keep.add(t, dot)
            anims.append(AnimationGroup(FadeIn(dot), Write(t)))
        self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=3.0)
        self.wait(1.5)

        note = Text("รู 1 จ่ายลม · รู 2,4 ไปกระบอก · รู 3,5 ทิ้งลม",
                    font_size=21, color=GRAYTXT).to_edge(DOWN, buff=0.35)
        self.play(Write(note))
        self.wait(1.5)
        self.play(FadeOut(VGroup(v["all"], keep, note, header)))

    # ── PART 3 : ประกอบวงจร ──────────────────────────────────
    def build_circuit(self):
        header = self._header("③ ประกอบเป็นวงจร", GREENOK)
        self.play(FadeIn(header, shift=DOWN * 0.3))
        self.circuit = self._make_full_circuit()
        c = self.circuit
        self.play(FadeIn(c["cyl"]["all"]), run_time=0.8)
        self.play(Create(c["valve"]["all"]), run_time=1.0)
        self.play(Create(c["tubeA"]), Create(c["tubeB"]), run_time=0.8)
        self.play(Create(c["supply_line"]), FadeIn(c["supply_tri"]),
                  Create(c["exh5"]), Create(c["exh3"]),
                  FadeIn(c["sil5"]), FadeIn(c["sil3"]), run_time=0.8)
        self.play(FadeIn(c["pilotL"]), FadeIn(c["pilotR"]),
                  FadeIn(c["pilotL_lbl"]), FadeIn(c["pilotR_lbl"]))
        self.wait(1.0)
        self.play(FadeOut(header))

    # ── PART 4 : เดินวงจร ────────────────────────────────────
    def run_cycle(self):
        c = self.circuit
        # รอบที่ 1: กด pilot ซ้าย → ยื่นออก
        self._do_extend(c)
        self.wait(0.6)
        # รอบที่ 2: กด pilot ขวา → หดเข้า
        self._do_retract(c)
        self.wait(0.6)
        # รอบที่ 3 เร็ว ๆ ให้เห็นภาพรวม
        self._do_extend(c, fast=True)
        self._do_retract(c, fast=True)
        self.wait(0.8)
        self.play(FadeOut(c["group"]))

    def _flash_pilot(self, pilot, side_text):
        msg = Text(side_text, font_size=22, color=GREENOK)
        msg.next_to(pilot, UP if pilot.get_center()[1] < 0 else DOWN, buff=0.3)
        self.play(pilot.animate.set_fill(GREENOK, opacity=0.9),
                  Flash(pilot.get_center(), color=GREENOK, flash_radius=0.4),
                  FadeIn(msg, scale=1.2), run_time=0.6)
        return msg

    def _air_flow(self, path, color, run_time=1.2):
        dots = VGroup(*[Dot(color=color, radius=0.09) for _ in range(3)])
        anims = []
        for i, d in enumerate(dots):
            d.move_to(path.get_start())
            anims.append(MoveAlongPath(d, path, run_time=run_time, rate_func=linear))
        self.add(dots)
        self.play(LaggedStart(*anims, lag_ratio=0.25))
        self.remove(dots)

    def _do_extend(self, c, fast=False):
        rt = 0.6 if fast else 1.0
        msg = self._flash_pilot(c["pilotL"], "กด pilot ซ้าย → จ่ายลมเข้าช่องซ้าย")
        # ลมมีแรงดัน: supply → port1 → (ผ่านวาล์ว) → port4 → tubeA → กระบอกช่องซ้าย
        press_path = tube(
            c["path_supply_to_4"], color=PRESSURE)
        self.play(c["supply_line"].animate.set_stroke(PRESSURE),
                  c["tubeA"].animate.set_stroke(PRESSURE),
                  c["valve"]["box_a"].animate.set_fill(PRESSURE, 0.18),
                  run_time=0.4)
        self._air_flow(press_path, PRESSURE, run_time=rt + 0.3)
        # ลูกสูบยื่นออก (เลื่อนขวา)
        self.play(c["cyl"]["mover"].animate.shift(RIGHT * c["stroke"]),
                  run_time=rt + 0.4)
        # ลมเก่าในช่องขวา ระบายออกทาง port2 → port3
        exh_path = tube(c["path_2_to_exh3"], color=EXHAUST)
        self.play(c["tubeB"].animate.set_stroke(EXHAUST),
                  c["exh3"].animate.set_stroke(EXHAUST), run_time=0.3)
        self._air_flow(exh_path, EXHAUST, run_time=rt)
        # reset สี
        self.play(c["supply_line"].animate.set_stroke(METAL_LT),
                  c["tubeA"].animate.set_stroke(METAL_LT),
                  c["tubeB"].animate.set_stroke(METAL_LT),
                  c["exh3"].animate.set_stroke(METAL_LT),
                  c["valve"]["box_a"].animate.set_fill(METAL, 0.0),
                  c["pilotL"].animate.set_fill(METAL, 0.4),
                  FadeOut(msg), run_time=0.4)

    def _do_retract(self, c, fast=False):
        rt = 0.6 if fast else 1.0
        msg = self._flash_pilot(c["pilotR"], "กด pilot ขวา → จ่ายลมเข้าช่องขวา")
        press_path = tube(c["path_supply_to_2"], color=PRESSURE)
        self.play(c["supply_line"].animate.set_stroke(PRESSURE),
                  c["tubeB"].animate.set_stroke(PRESSURE),
                  c["valve"]["box_b"].animate.set_fill(PRESSURE, 0.18),
                  run_time=0.4)
        self._air_flow(press_path, PRESSURE, run_time=rt + 0.3)
        self.play(c["cyl"]["mover"].animate.shift(LEFT * c["stroke"]),
                  run_time=rt + 0.4)
        exh_path = tube(c["path_4_to_exh5"], color=EXHAUST)
        self.play(c["tubeA"].animate.set_stroke(EXHAUST),
                  c["exh5"].animate.set_stroke(EXHAUST), run_time=0.3)
        self._air_flow(exh_path, EXHAUST, run_time=rt)
        self.play(c["supply_line"].animate.set_stroke(METAL_LT),
                  c["tubeB"].animate.set_stroke(METAL_LT),
                  c["tubeA"].animate.set_stroke(METAL_LT),
                  c["exh5"].animate.set_stroke(METAL_LT),
                  c["valve"]["box_b"].animate.set_fill(METAL, 0.0),
                  c["pilotR"].animate.set_fill(METAL, 0.4),
                  FadeOut(msg), run_time=0.4)

    # ── OUTRO ────────────────────────────────────────────────
    def outro(self):
        title = Text("สรุปหลักการ", font_size=44, color=GREENOK)
        lines = VGroup(
            Text("• วาล์ว 5/2 = สวิตช์ลม มี 2 ตำแหน่ง", font_size=26, color=GRAYTXT),
            Text("• ตำแหน่งหนึ่ง → ลมเข้าช่องซ้าย → ลูกสูบยื่นออก", font_size=26, color=PRESSURE),
            Text("• อีกตำแหน่ง → ลมเข้าช่องขวา → ลูกสูบหดเข้า", font_size=26, color=EXHAUST),
            Text("• ฝั่งตรงข้ามเปิดให้ลมเก่าระบายออกเสมอ", font_size=26, color=GRAYTXT),
            Text("• กด pilot สลับซ้าย-ขวา = สั่งกระบอกเข้า-ออก", font_size=26, color=GREENOK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        title.next_to(lines, UP, buff=0.5)
        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.3) for l in lines],
                              lag_ratio=0.4), run_time=3.0)
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, lines)))
        end = Text("จบแล้ว — เข้าใจวาล์ว 5/2 แล้วนะ! 🎉", font_size=34, color=GREENOK)
        self.play(Write(end))
        self.wait(2.0)
        self.play(FadeOut(end))

    # ════════════════════════════════════════════════════════
    #  builders
    # ════════════════════════════════════════════════════════
    def _make_cylinder(self, scale=1.0):
        bw, bh = 3.8 * scale, 1.3 * scale
        barrel = Rectangle(width=bw, height=bh, stroke_color=METAL_LT,
                           stroke_width=3, fill_color=METAL, fill_opacity=0.25)
        # ลูกสูบเริ่มที่ตำแหน่งหดเข้า (ซ้าย)
        piston = Rectangle(width=0.22, height=bh - 0.12, fill_color=PISTON_C,
                           fill_opacity=1, stroke_width=0)
        piston.move_to(barrel.get_left() + RIGHT * 0.9)
        rod = Line(piston.get_right(), barrel.get_right() + RIGHT * 1.2,
                   color=ROD_C, stroke_width=7)
        rod.set_y(piston.get_center()[1])
        mover = VGroup(piston, rod)
        portA = barrel.get_bottom() + LEFT * (bw * 0.28)
        portB = barrel.get_bottom() + RIGHT * (bw * 0.28)
        allg = VGroup(barrel, mover)
        return {"barrel": barrel, "piston": piston, "rod": rod, "mover": mover,
                "portA": portA, "portB": portB, "all": allg}

    def _make_valve(self):
        box_w, box_h = 1.5, 1.5
        box_a = Rectangle(width=box_w, height=box_h, stroke_color=METAL_LT,
                          stroke_width=3, fill_color=METAL, fill_opacity=0.0)
        box_b = box_a.copy()
        box_a.shift(LEFT * box_w / 2)
        box_b.shift(RIGHT * box_w / 2)
        frame = VGroup(box_a, box_b)
        divider = Line(box_a.get_top(), box_a.get_bottom(),
                       color=METAL_LT, stroke_width=3)
        divider.move_to(ORIGIN).set_y(box_a.get_center()[1])
        divider.move_to([0, box_a.get_center()[1], 0])

        # internal arrows ให้ดูเหมือนสัญลักษณ์จริง
        ar_a = self._valve_arrows(box_a, crossed=False)
        ar_b = self._valve_arrows(box_b, crossed=True)

        # ports (อิงกับ frame)
        p4 = frame.get_top() + LEFT * 0.9
        p2 = frame.get_top() + RIGHT * 0.9
        p4[1] = box_a.get_top()[1]
        p2[1] = box_a.get_top()[1]
        p1 = frame.get_bottom().copy(); p1[0] = 0
        p5 = box_a.get_left().copy()
        p3 = box_b.get_right().copy()

        allg = VGroup(frame, divider, ar_a, ar_b)
        return {"frame": frame, "divider": divider, "box_a": box_a, "box_b": box_b,
                "ar_a": ar_a, "ar_b": ar_b,
                "p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "all": allg}

    def _valve_arrows(self, box, crossed):
        c = box.get_center()
        g = VGroup()
        if not crossed:
            g.add(Line(c + DOWN * 0.5, c + UP * 0.5, color=METAL_LT, stroke_width=2)
                  .add_tip(tip_length=0.15))
        else:
            g.add(Line(c + DOWN * 0.5 + LEFT * 0.3, c + UP * 0.5 + RIGHT * 0.3,
                       color=METAL_LT, stroke_width=2).add_tip(tip_length=0.15))
            g.add(Line(c + DOWN * 0.5 + RIGHT * 0.3, c + UP * 0.5 + LEFT * 0.3,
                       color=METAL_LT, stroke_width=2))
        return g

    def _make_full_circuit(self):
        group = VGroup()
        # cylinder บน
        cyl = self._make_cylinder()
        cyl["all"].move_to(UP * 2.3)
        # ใหม่: portA/portB คำนวณใหม่หลังย้าย
        bw = 3.8
        portA = cyl["barrel"].get_bottom() + LEFT * (bw * 0.28)
        portB = cyl["barrel"].get_bottom() + RIGHT * (bw * 0.28)
        cyl["portA"], cyl["portB"] = portA, portB

        valve = self._make_valve()
        valve["all"].move_to(DOWN * 1.3)
        # recompute ports หลังย้าย
        box_a, box_b = valve["box_a"], valve["box_b"]
        p4 = np.array([box_a.get_center()[0], box_a.get_top()[1], 0])
        p2 = np.array([box_b.get_center()[0], box_b.get_top()[1], 0])
        p1 = np.array([0, valve["frame"].get_bottom()[1], 0])
        p5 = box_a.get_left()
        p3 = box_b.get_right()
        valve.update({"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5})

        # ท่อ A: portA(ซ้ายบน) → p4
        tubeA = tube([portA, [portA[0], (portA[1] + p4[1]) / 2],
                      [p4[0], (portA[1] + p4[1]) / 2], p4], color=METAL_LT)
        tubeB = tube([portB, [portB[0], (portB[1] + p2[1]) / 2],
                      [p2[0], (portB[1] + p2[1]) / 2], p2], color=METAL_LT)

        supply_tri = Polygon([-0.22, -3.1, 0], [0.22, -3.1, 0], [0, -2.7, 0],
                             stroke_color=SUPPLY_C, stroke_width=3, fill_opacity=0)
        supply_line = tube([[0, -2.7], [p1[0], p1[1]]], color=METAL_LT)

        exh5 = tube([p5, [p5[0] - 0.7, p5[1]]], color=METAL_LT)
        exh3 = tube([p3, [p3[0] + 0.7, p3[1]]], color=METAL_LT)
        sil5 = silencer([p5[0] - 0.7, p5[1], 0], LEFT)
        sil3 = silencer([p3[0] + 0.7, p3[1], 0], RIGHT)

        # pilot boxes (ปลายวาล์วซ้าย/ขวา)
        pilotL = Rectangle(width=0.35, height=valve["box_a"].height,
                           fill_color=METAL, fill_opacity=0.4,
                           stroke_color=METAL_LT, stroke_width=2)
        pilotL.next_to(valve["box_a"], LEFT, buff=0.0)
        pilotR = pilotL.copy().next_to(valve["box_b"], RIGHT, buff=0.0)
        pilotL_lbl = Text("14", font_size=18, color=GRAYTXT).next_to(pilotL, DOWN, buff=0.15)
        pilotR_lbl = Text("12", font_size=18, color=GRAYTXT).next_to(pilotR, DOWN, buff=0.15)

        # flow paths (สำหรับ dots)
        path_supply_to_4 = [[0, -2.7], list(p1[:2]),
                            [p4[0], p1[1] + 0.2], list(p4[:2]),
                            list(tubeA.get_start()[:2])]
        path_supply_to_2 = [[0, -2.7], list(p1[:2]),
                            [p2[0], p1[1] + 0.2], list(p2[:2]),
                            list(tubeB.get_start()[:2])]
        path_2_to_exh3 = [list(portB[:2]), list(p2[:2]),
                          [p3[0] - 0.2, p2[1]], list(p3[:2]),
                          [p3[0] + 0.7, p3[1]]]
        path_4_to_exh5 = [list(portA[:2]), list(p4[:2]),
                          [p5[0] + 0.2, p4[1]], list(p5[:2]),
                          [p5[0] - 0.7, p5[1]]]

        group.add(cyl["all"], valve["all"], tubeA, tubeB, supply_tri,
                  supply_line, exh5, exh3, sil5, sil3,
                  pilotL, pilotR, pilotL_lbl, pilotR_lbl)

        return {
            "cyl": cyl, "valve": valve, "tubeA": tubeA, "tubeB": tubeB,
            "supply_tri": supply_tri, "supply_line": supply_line,
            "exh5": exh5, "exh3": exh3, "sil5": sil5, "sil3": sil3,
            "pilotL": pilotL, "pilotR": pilotR,
            "pilotL_lbl": pilotL_lbl, "pilotR_lbl": pilotR_lbl,
            "path_supply_to_4": path_supply_to_4,
            "path_supply_to_2": path_supply_to_2,
            "path_2_to_exh3": path_2_to_exh3,
            "path_4_to_exh5": path_4_to_exh5,
            "stroke": 1.4, "group": group,
        }

    # ── HELPER ───────────────────────────────────────────────
    def _header(self, text, color=WHITE):
        h = Text(text, font_size=34, color=color).to_edge(UP, buff=0.35)
        line = Line(LEFT * 6, RIGHT * 6, color=color, stroke_width=1.5
                    ).next_to(h, DOWN, buff=0.15)
        return VGroup(h, line)
