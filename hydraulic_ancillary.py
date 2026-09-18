"""
Fluid Power Control — W06 Hydraulic Ancillary Devices (hydraulic06.pdf)
Scene: H6_01_Reservoir (ถังพักน้ำมันไฮดรอลิก และแผ่นกั้น Baffle Plate)
Lecture slides: hydraulic06.pdf pages 2-4

Pedagogical Objective:
- Correct the misconception: 'ถังก็แค่ที่เก็บน้ำมัน'
- Reveal the critical function of the Baffle Plate: forced circuitous flow,
  cooling (heat dissipation), de-aeration, and settling of contaminants.
- Explain why direct short-circuit flow causes pump cavitation.
- Demonstrate sizing rule: Reservoir size (gal or m3) = 3 x Pump flow rate.
"""

import os
import numpy as np
from manim import *
from mlib import *
from hydraulic_valves import SUPPLY, RETURN, BLOCKED, SECONDARY

# Font configuration
Text.set_default(font=os.environ.get("MANIM_THAI_FONT", "Leelawadee UI"))

# Module colors matching spec and mlib
COL_METAL = METAL       # #90A4AE
COL_FIELD = FIELD       # #42A5F5 (cool oil)
COL_WARN  = WARN        # #FF7043 (hot oil / alert)
COL_OK    = OK          # #26C6DA (conclusion / result)
COL_GRAY  = GRAYTXT     # #B0BEC5 (labels / auxiliary)
COL_CURR  = CURRENT     # #FFB300 (flow / duty)
COL_BG_BOX = "#1E293B"  # Dark slate card background


class H6_01_Reservoir(SafeThreeDScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # Coordinates & Waypoint Setup (Geometry Spec Section 3)
        # ----------------------------------------------------------------------
        path_direct = [
            np.array([-2.60, -1.55, 0.0]),   # return pipe discharge
            np.array([+2.32, -1.75, 0.0])    # suction strainer inlet
        ]

        path_baffled = [
            np.array([-2.60, -1.55, 0.0]),   # W0: return pipe discharge
            np.array([-3.25, -1.85, 0.0]),   # W1: outer wall impingement zone
            np.array([ 0.00, -1.95, 0.0]),   # W2: under-baffle passage slot
            np.array([+2.32, -1.75, 0.0])    # W3: suction strainer inlet
        ]

        # Geometry assertions as required by spec Section 4
        tank_bottom_y = -2.25
        tank_top_y = +0.95
        baffle_bottom_y = -1.65
        baffle_top_y = +0.15
        assert baffle_bottom_y > tank_bottom_y, "Baffle must leave bottom clearance slot"
        assert baffle_top_y > -0.35, "Baffle must extend above oil surface to block foam"
        assert path_baffled[2][1] < baffle_bottom_y, "Waypoint 2 must pass UNDER the baffle plate"
        assert path_baffled[2][1] > tank_bottom_y, "Waypoint 2 must remain inside tank bottom"

        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title and Page Reference Badge
        # ----------------------------------------------------------------------
        title_mob = title("ถังพักน้ำมันไฮดรอลิก")
        page_ref_mob = page_ref("hydraulic06 น.2-4")
        self.hud(title_mob, page_ref_mob)

        self.play(
            FadeIn(title_mob, shift=UP * 0.4),
            FadeIn(page_ref_mob),
            run_time=1.0
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–6.5: 3D Reservoir Model Showcase & Ambient Rotation
        # ----------------------------------------------------------------------
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES)

        cap1 = caption_top("ถังพักน้ำมัน — มากกว่าที่เก็บน้ำมัน")
        self.hud(cap1)

        # 3D Tank components
        tank_shell = Prism(dimensions=[7.2, 3.2, 2.4], fill_color=COL_METAL, stroke_width=1.2).move_to([0, -0.65, 0])
        tank_shell.set_opacity(0.95)

        oil_body = Prism(dimensions=[7.0, 1.9, 2.3], fill_color=COL_FIELD, stroke_width=0).move_to([0, -1.30, 0])
        oil_body.set_opacity(0.52)

        baffle_plate = Prism(dimensions=[0.12, 1.8, 2.3], fill_color=COL_METAL, stroke_width=1.5).move_to([0, -0.75, 0])
        baffle_plate.set_opacity(0.95)

        # Return and suction pipes
        p_ret = Cylinder(radius=0.12, height=2.4, resolution=(10, 10), fill_color=COL_METAL).move_to([-2.60, -0.35, 0])
        p_ret.set_opacity(0.85)

        p_suc = Cylinder(radius=0.12, height=2.4, resolution=(10, 10), fill_color=COL_METAL).move_to([+2.60, -0.35, 0])
        p_suc.set_opacity(0.85)

        # Strainer wire mesh cage at suction
        strainer_mesh = Cube(side_length=0.45, fill_color=COL_METAL, stroke_width=1.2).move_to([+2.60, -1.75, 0])
        strainer_mesh.set_opacity(0.70)

        # Ancillary items: breather on top, sight glass on right wall, drain plug at bottom
        c_breather = Cylinder(radius=0.25, height=0.35, resolution=(10, 10), fill_color=COL_METAL).move_to([-1.40, +1.15, 0])
        c_breather.set_opacity(0.90)

        c_sight = Prism(dimensions=[0.15, 1.0, 0.30], fill_color=COL_OK, stroke_width=1.0).move_to([+3.62, -0.85, 0])
        c_sight.set_opacity(0.85)

        c_drain = Cylinder(radius=0.20, height=0.25, resolution=(10, 10), fill_color=COL_METAL).move_to([0.0, -2.35, 0])
        c_drain.set_opacity(0.90)

        tank_group = VGroup(tank_shell, oil_body, baffle_plate, p_ret, p_suc, strainer_mesh, c_breather, c_sight, c_drain)

        self.play(
            FadeIn(tank_group, shift=UP * 0.3),
            FadeIn(cap1),
            run_time=1.2
        )

        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(2.3)
        self.stop_ambient_camera_rotation()

        # Stabilize camera angle for inspection
        self.move_camera(phi=65 * DEGREES, theta=-65 * DEGREES, run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 6.5–7.0: Lower Shell Opacity for Internal Inspection
        # ----------------------------------------------------------------------
        self.play(tank_shell.animate.set_opacity(0.28), run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 7.0–8.5: Name Part 1: Return Line
        # ----------------------------------------------------------------------
        arr_return = arrow3([-2.60, 2.0, 0], [-2.60, 1.40, 0], color=COL_METAL)
        lbl_return = Text("Return line (ท่อไหลกลับ)", font_size=19, color=COL_GRAY).move_to([-3.4, 2.2, 0])
        self.hud(lbl_return)

        self.play(Create(arr_return), FadeIn(lbl_return, shift=RIGHT * 0.2), run_time=0.5)
        self.wait(1.0)

        # ----------------------------------------------------------------------
        # BEAT 8.5–10.0: Name Part 2: Pump Suction + Strainer
        # ----------------------------------------------------------------------
        arr_suction = arrow3([+2.60, 2.0, 0], [+2.60, 1.40, 0], color=COL_METAL)
        lbl_suction = Text("Pump suction + Strainer (ท่อดูดปั๊ม + ตะแกรง)", font_size=19, color=COL_GRAY).move_to([+2.6, 2.2, 0])
        self.hud(lbl_suction)

        self.play(FadeOut(arr_return), FadeOut(lbl_return), run_time=0.3)
        self.play(
            Create(arr_suction), FadeIn(lbl_suction),
            Indicate(strainer_mesh, color=COL_OK, scale_factor=1.15),
            run_time=0.6
        )
        self.wait(0.9)

        # ----------------------------------------------------------------------
        # BEAT 10.0–11.5: Name Part 3: Baffle Plate (HERO Component)
        # ----------------------------------------------------------------------
        arr_baffle = arrow3([0.0, 1.8, 0], [0.0, 0.40, 0], color=COL_WARN)
        lbl_baffle = Text("Baffle plate (แผ่นกั้นถังพัก — พระเอกของคลิป)", font_size=20, color=COL_WARN).move_to([0.0, 2.15, 0])
        self.hud(lbl_baffle)

        self.play(FadeOut(arr_suction), FadeOut(lbl_suction), run_time=0.3)
        self.play(
            Indicate(baffle_plate, color=COL_WARN, scale_factor=1.15),
            Create(arr_baffle), FadeIn(lbl_baffle),
            run_time=0.6
        )
        self.wait(0.9)

        # ----------------------------------------------------------------------
        # BEAT 11.5–13.0: Name Part 4: Breather, Sight Glass, Drain Plug
        # ----------------------------------------------------------------------
        arr_br = arrow3([-1.40, 1.8, 0], [-1.40, 1.35, 0], color=COL_GRAY)
        lbl_br = Text("Air breather / Filler", font_size=16, color=COL_GRAY).move_to([-3.4, 1.85, 0])

        arr_sg = arrow3([+4.4, -0.85, 0], [+3.75, -0.85, 0], color=COL_GRAY)
        lbl_sg = Text("Sight glass & Temp", font_size=16, color=COL_GRAY).move_to([+4.8, -0.45, 0])

        arr_dp = arrow3([0.0, -2.95, 0], [0.0, -2.45, 0], color=COL_GRAY)
        lbl_dp = Text("Drain plug (รูถ่ายน้ำมัน)", font_size=16, color=COL_GRAY).move_to([0.0, -3.15, 0])

        self.hud(lbl_br, lbl_sg, lbl_dp)

        self.play(FadeOut(arr_baffle), FadeOut(lbl_baffle), run_time=0.3)
        self.play(
            Create(arr_br), FadeIn(lbl_br),
            Create(arr_sg), FadeIn(lbl_sg),
            Create(arr_dp), FadeIn(lbl_dp),
            run_time=0.6
        )
        self.wait(0.9)

        # ----------------------------------------------------------------------
        # BEAT 13.0–14.0: Clear Labels & Transition to 4 Core Functions
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(arr_br), FadeOut(lbl_br),
            FadeOut(arr_sg), FadeOut(lbl_sg),
            FadeOut(arr_dp), FadeOut(lbl_dp),
            run_time=0.5
        )

        cap2 = caption_top("4 หน้าที่หลักของถังพักน้ำมันไฮดรอลิก")
        self.hud(cap2)
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 14.0–17.0: Function 1: เก็บน้ำมันสำรอง (Reserve Storage)
        # ----------------------------------------------------------------------
        fn1_t = Text("1. เก็บน้ำมันสำรอง (Reserve Oil)", font_size=18, color=WHITE).move_to([-3.8, 1.90, 0])
        self.hud(fn1_t)

        self.play(
            Indicate(tank_shell, color=COL_OK, scale_factor=1.04),
            FadeIn(fn1_t, shift=UP * 0.2),
            run_time=0.6
        )
        self.wait(2.4)

        # ----------------------------------------------------------------------
        # BEAT 17.0–20.5: Function 2: ระบายความร้อน (Cooling) — Live Color Change
        # ----------------------------------------------------------------------
        fn2_t = Text("2. ระบายความร้อน (Heat Dissipation)", font_size=18, color=COL_WARN).next_to(fn1_t, DOWN, aligned_edge=LEFT, buff=0.18)
        self.hud(fn2_t)

        self.play(
            FadeIn(fn2_t, shift=UP * 0.2),
            oil_body.animate.set_color(COL_FIELD),
            run_time=2.5
        )
        self.wait(1.0)

        # ----------------------------------------------------------------------
        # BEAT 20.5–24.0: Function 3: แยกฟองอากาศ (De-aeration) — Bubbles Rising
        # ----------------------------------------------------------------------
        fn3_t = Text("3. แยกฟองอากาศ (De-aeration)", font_size=18, color=WHITE).next_to(fn2_t, DOWN, aligned_edge=LEFT, buff=0.18)
        self.hud(fn3_t)

        bubble_pts = [
            [-2.4, -2.0, 0.2], [-1.8, -1.9, -0.3], [-0.8, -2.1, 0.4],
            [+0.8, -2.0, -0.2], [+1.8, -1.9, 0.3], [+2.4, -2.1, 0.1]
        ]
        bubbles = VGroup(*[
            Circle(radius=0.06, color=WHITE, fill_color=WHITE, fill_opacity=0.65).move_to(pt)
            for pt in bubble_pts
        ])

        self.play(
            FadeIn(fn3_t, shift=UP * 0.2),
            *[b.animate.shift(UP * 1.5) for b in bubbles],
            run_time=2.8,
            rate_func=linear
        )
        self.play(FadeOut(bubbles), run_time=0.4)

        # ----------------------------------------------------------------------
        # BEAT 24.0–27.5: Function 4: ตกตะกอน (Settling) — Particles Sinking
        # ----------------------------------------------------------------------
        fn4_t = Text("4. ให้สิ่งสกปรกตกตะกอน (Settling)", font_size=18, color=COL_GRAY).next_to(fn3_t, DOWN, aligned_edge=LEFT, buff=0.18)
        self.hud(fn4_t)

        dirt_pts = [
            [-2.2, -0.6, 0.1], [-1.2, -0.5, -0.2],
            [+1.0, -0.6, 0.2], [+2.0, -0.5, -0.1]
        ]
        dirt_group = VGroup(*[
            Dot(point=pt, radius=0.055, color=DARK_GRAY)
            for pt in dirt_pts
        ])

        self.play(
            FadeIn(fn4_t, shift=UP * 0.2),
            *[d.animate.shift(DOWN * 1.4) for d in dirt_group],
            run_time=2.8,
            rate_func=linear
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 27.5–29.5: Clear Stage & Pose Misconception Question
        # ----------------------------------------------------------------------
        self.fade_out_all(run_time=0.8)
        self.wait(0.3)

        cap3 = caption_top("ถ้าไม่มีแผ่นกั้น (Baffle) จะเกิดอะไรขึ้น?", color=COL_WARN)
        self.hud(title_mob, page_ref_mob, cap3)

        self.play(
            FadeIn(title_mob),
            FadeIn(page_ref_mob),
            FadeIn(cap3, shift=UP * 0.3),
            run_time=0.6
        )
        self.wait(0.4)

        # ----------------------------------------------------------------------
        # BEAT 29.5–34.5: Unbaffled Tank — Direct Short-Circuit Flow & Danger
        # ----------------------------------------------------------------------
        # Recreate tank WITHOUT baffle plate
        tank_shell_nobaffle = Prism(dimensions=[7.2, 3.2, 2.4], fill_color=COL_METAL, stroke_width=1.2).move_to([0, -0.65, 0])
        tank_shell_nobaffle.set_opacity(0.28)

        oil_nobaffle = Prism(dimensions=[7.0, 1.9, 2.3], fill_color=COL_FIELD, stroke_width=0).move_to([0, -1.30, 0])
        oil_nobaffle.set_opacity(0.40)

        p_ret2 = Cylinder(radius=0.12, height=2.4, resolution=(10, 10), fill_color=COL_METAL).move_to([-2.60, -0.35, 0])
        p_ret2.set_opacity(0.85)

        p_suc2 = Cylinder(radius=0.12, height=2.4, resolution=(10, 10), fill_color=COL_METAL).move_to([+2.60, -0.35, 0])
        p_suc2.set_opacity(0.85)

        strainer2 = Cube(side_length=0.45, fill_color=COL_METAL, stroke_width=1.2).move_to([+2.60, -1.75, 0])
        strainer2.set_opacity(0.70)

        # Compact pump symbol mounted on suction line
        pump_sym = Circle(radius=0.34, color=COL_WARN, fill_color=COL_BG_BOX, fill_opacity=0.9).move_to([+2.60, 0.40, 0])
        pump_tri = Triangle(color=COL_WARN, fill_color=COL_WARN, fill_opacity=1).scale(0.12).move_to([+2.60, 0.52, 0])
        pump_full = VGroup(pump_sym, pump_tri)

        tank_nobaffle_grp = VGroup(tank_shell_nobaffle, oil_nobaffle, p_ret2, p_suc2, strainer2, pump_full)

        self.play(FadeIn(tank_nobaffle_grp), run_time=1.0)

        # Direct path defined explicitly by points (Geometry Spec Section 3A)
        line_direct = Line(path_direct[0], path_direct[1], color=COL_WARN, stroke_width=3.5)
        dot_direct = Dot(path_direct[0], radius=0.12, color=COL_WARN)
        bubble_direct = Circle(radius=0.065, color=WHITE, fill_color=WHITE, fill_opacity=0.8).move_to(path_direct[0] + UP * 0.12)

        cap4 = caption_top("น้ำมันร้อน + มีฟองอากาศ วิ่งลัดวงจรตรงเข้าปั๊มทันที!", color=COL_WARN)
        self.hud(cap4)

        self.play(ReplacementTransform(cap3, cap4), run_time=0.4)
        self.play(
            Create(line_direct),
            MoveAlongPath(dot_direct, Line(path_direct[0], path_direct[1])),
            MoveAlongPath(bubble_direct, Line(path_direct[0], path_direct[1])),
            run_time=3.0,
            rate_func=linear
        )

        # ----------------------------------------------------------------------
        # BEAT 34.5–37.0: Consequence: Cavitation & Rapid Wear
        # ----------------------------------------------------------------------
        cav_card = RoundedRectangle(corner_radius=0.12, width=5.2, height=1.15, color=COL_WARN, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([+1.8, 1.25, 0])
        cav_t1 = Text("เกิด Cavitation ในปั๊ม!", font_size=18, color=COL_WARN).move_to([+1.8, 1.45, 0])
        cav_t2 = Text("เสียงดังรุนแรง · กัดกร่อนใบพัด · สึกหรอเร็ว", font_size=15, color=WHITE).move_to([+1.8, 1.05, 0])
        cav_grp = VGroup(cav_card, cav_t1, cav_t2)
        self.hud(cav_grp)

        self.play(
            Indicate(pump_full, color=COL_WARN, scale_factor=1.25),
            FadeIn(cav_grp),
            run_time=0.8
        )
        self.wait(1.7)

        # ----------------------------------------------------------------------
        # BEAT 37.0–39.5: Insert Baffle Plate Back
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(line_direct), FadeOut(dot_direct), FadeOut(bubble_direct), FadeOut(cav_grp),
            run_time=0.6
        )
        self.wait(0.4)

        cap5 = caption_top("ใส่แผ่นกั้น (Baffle) กลับ: บังคับเส้นทางไหลอ้อม", color=COL_OK)
        self.hud(cap5)

        # Re-introduce baffle plate cleanly
        baffle_plate2 = Prism(dimensions=[0.12, 1.8, 2.3], fill_color=COL_METAL, stroke_width=1.5).move_to([0, -0.75, 0])
        baffle_plate2.set_opacity(0.95)

        self.play(
            ReplacementTransform(cap4, cap5),
            FadeIn(baffle_plate2, shift=DOWN * 0.4),
            run_time=0.8
        )
        self.wait(0.7)

        # ----------------------------------------------------------------------
        # BEAT 39.5–46.5: Baffled Circuitous Flow & Progressive Cooling
        # ----------------------------------------------------------------------
        # 3 Segments derived from path_baffled waypoints
        seg1 = Line(path_baffled[0], path_baffled[1], color=COL_WARN, stroke_width=3.5)
        seg2 = Line(path_baffled[1], path_baffled[2], color=COL_CURR, stroke_width=3.5)
        seg3 = Line(path_baffled[2], path_baffled[3], color=COL_FIELD, stroke_width=3.5)
        baffled_lines = VGroup(seg1, seg2, seg3)

        # Dynamic color changing dot tracking progress along path
        dot_flow = Dot(path_baffled[0], radius=0.12, color=COL_WARN)
        bubble_flow = Circle(radius=0.065, color=WHITE, fill_color=WHITE, fill_opacity=0.8).move_to(path_baffled[0] + UP * 0.12)

        # Step annotations
        st_1 = Text("① ชนผนังกระจายตัว", font_size=16, color=COL_WARN).move_to([-3.4, 1.25, 0])
        st_2 = Text("② ลอดใต้แผ่นกั้น", font_size=16, color=COL_CURR).move_to([0.0, 1.25, 0])
        st_3 = Text("③ เย็นลง + ไร้ฟองอากาศ", font_size=16, color=COL_OK).move_to([+3.4, 1.25, 0])
        self.hud(st_1, st_2, st_3)

        # Segment 1: Return to wall
        self.play(
            Create(seg1),
            MoveAlongPath(dot_flow, Line(path_baffled[0], path_baffled[1])),
            MoveAlongPath(bubble_flow, Line(path_baffled[0], path_baffled[1])),
            FadeIn(st_1),
            run_time=1.8,
            rate_func=linear
        )

        # Bubble separates and rises to surface between W1 and W2
        bubble_rise = Line(path_baffled[1] + UP * 0.12, [-3.25, -0.40, 0])
        self.play(
            Create(seg2),
            MoveAlongPath(dot_flow, Line(path_baffled[1], path_baffled[2])),
            MoveAlongPath(bubble_flow, bubble_rise),
            dot_flow.animate.set_color(COL_CURR),
            FadeIn(st_2),
            run_time=2.2,
            rate_func=linear
        )
        self.play(FadeOut(bubble_flow), run_time=0.2)

        # Segment 3: Under baffle slot to pump suction strainer
        self.play(
            Create(seg3),
            MoveAlongPath(dot_flow, Line(path_baffled[2], path_baffled[3])),
            dot_flow.animate.set_color(COL_FIELD),
            FadeIn(st_3),
            run_time=2.0,
            rate_func=linear
        )

        # Hero payoff check: Indicate dot at destination
        self.play(Indicate(dot_flow, color=COL_OK, scale_factor=1.35), run_time=0.5)
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 46.5–52.5: Clear 3D & Transition to Reservoir Sizing Formula
        # ----------------------------------------------------------------------
        self.fade_out_all(run_time=0.8)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        cap6 = caption_top("สูตรคำนวณขนาดถังพักน้ำมัน (Reservoir Sizing)", color=WHITE)
        self.hud(title_mob, page_ref_mob, cap6)

        form_box = RoundedRectangle(corner_radius=0.15, width=9.2, height=2.2, color=COL_OK, fill_color=COL_BG_BOX, fill_opacity=0.92).move_to([0, 0.8, 0])
        f_gal = Text("ขนาดถัง (gal) = 3 × อัตราการไหลปั๊ม (gpm)", font_size=20, color=COL_OK).move_to([0, 1.40, 0])
        f_si  = Text("ขนาดถัง (m³) = 3 × อัตราการไหลปั๊ม (m³/min)", font_size=20, color=WHITE).move_to([0, 0.85, 0])
        why_txt = Text("ทำไมต้อง 3 เท่า? → ให้น้ำมันมีเวลาพัก ระบายความร้อน และปล่อยฟองอากาศ", font_size=15, color=COL_GRAY).move_to([0, 0.28, 0])
        self.hud(form_box, f_gal, f_si, why_txt)

        self.play(
            FadeIn(title_mob), FadeIn(page_ref_mob),
            FadeIn(cap6),
            FadeIn(form_box, shift=UP * 0.4),
            FadeIn(f_gal, shift=UP * 0.3),
            run_time=0.8
        )
        self.play(FadeIn(f_si, shift=UP * 0.3), run_time=0.5)
        self.wait(1.0)
        self.play(FadeIn(why_txt, shift=UP * 0.3), run_time=0.6)
        self.wait(2.0)

        # ----------------------------------------------------------------------
        # BEAT 52.5–62.5: Worked Example & 3x Bar Chart Comparison
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(form_box), FadeOut(f_gal), FadeOut(f_si), FadeOut(why_txt),
            run_time=0.5
        )

        cap7 = caption_top("ตัวอย่างการคำนวณ: อัตราไหลปั๊ม 10 gpm → ถัง 30 gal", color=WHITE)
        self.hud(cap7)
        self.play(ReplacementTransform(cap6, cap7), run_time=0.5)

        # Example Card (Left side)
        ex_card = RoundedRectangle(corner_radius=0.15, width=5.2, height=3.4, color=COL_METAL, fill_color=COL_BG_BOX, fill_opacity=0.92).move_to([-3.4, -0.55, 0])
        ex_h = Text("ตัวอย่างคำนวณตามสูตร", font_size=17, color=COL_CURR).move_to([-3.4, 0.75, 0])
        ex_l1 = Text("ปั๊มจ่าย: Q = 10 gpm", font_size=16, color=WHITE).move_to([-3.4, 0.25, 0])
        ex_l2 = Text("ขนาดถัง = 3 × 10 = 30 gal", font_size=17, color=COL_OK).move_to([-3.4, -0.25, 0])
        ex_l3 = Text("หน่วย SI: 0.06 m³/min → 0.18 m³", font_size=15, color=COL_GRAY).move_to([-3.4, -0.75, 0])
        ex_note = Text("(*ตัวเลขสมมติตามสูตรสไลด์ น.4)", font_size=13, color=COL_GRAY).move_to([-3.4, -1.25, 0])
        ex_grp = VGroup(ex_card, ex_h, ex_l1, ex_l2, ex_l3, ex_note)
        self.hud(ex_grp)

        # Bar chart comparison (Right side)
        base_line = Line([0.8, -2.25, 0], [5.6, -2.25, 0], color=COL_METAL, stroke_width=2.5)

        bar_q = Rectangle(width=1.0, height=0.90, color=COL_CURR, fill_color=COL_CURR, fill_opacity=0.88).move_to([2.1, -1.80, 0])
        lbl_q_val = Text("10 gpm", font_size=15, color=COL_CURR).next_to(bar_q, UP, buff=0.12)
        lbl_q_sub = Text("อัตราไหล/นาที", font_size=13, color=COL_GRAY).next_to(bar_q, DOWN, buff=0.15)

        bar_v = Rectangle(width=1.0, height=2.70, color=COL_OK, fill_color=COL_OK, fill_opacity=0.88).move_to([4.3, -0.90, 0])
        lbl_v_val = Text("30 gal (3×)", font_size=15, color=COL_OK).next_to(bar_v, UP, buff=0.12)
        lbl_v_sub = Text("ขนาดถังพัก", font_size=13, color=COL_GRAY).next_to(bar_v, DOWN, buff=0.15)

        bar_grp = VGroup(base_line, bar_q, lbl_q_val, lbl_q_sub, bar_v, lbl_v_val, lbl_v_sub)
        self.hud(bar_grp)

        self.play(FadeIn(ex_grp, shift=UP * 0.3), Create(base_line), run_time=0.8)
        self.play(
            GrowFromEdge(bar_q, DOWN),
            FadeIn(lbl_q_val), FadeIn(lbl_q_sub),
            run_time=0.9
        )
        self.play(
            GrowFromEdge(bar_v, DOWN),
            FadeIn(lbl_v_val), FadeIn(lbl_v_sub),
            run_time=1.1
        )
        self.wait(2.2)

        # ----------------------------------------------------------------------
        # BEAT 62.5–64.5: Executive Summary Card
        # ----------------------------------------------------------------------
        self.play(FadeOut(ex_grp), FadeOut(bar_grp), run_time=0.5)

        cap8 = caption_top("สรุปหลักการสำคัญ: ถังพักน้ำมันไฮดรอลิก", color=COL_OK)
        self.hud(cap8)
        self.play(ReplacementTransform(cap7, cap8), run_time=0.5)

        sum_box = RoundedRectangle(corner_radius=0.16, width=9.6, height=3.0, color=COL_OK, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([0, -0.45, 0])
        s1 = Text("1. หน้าที่ 4 ข้อ: เก็บน้ำมัน, ระบายความร้อน, แยกฟองอากาศ, ตกตะกอน", font_size=16, color=WHITE).move_to([0, 0.45, 0])
        s2 = Text("2. แผ่นกั้น (Baffle): พระเอกบังคับทางไหลอ้อม ไม่ให้น้ำมันร้อนวนเข้าปั๊ม", font_size=16, color=COL_WARN).move_to([0, -0.05, 0])
        s3 = Text("3. ป้องกัน Cavitation: ปั๊มไม่สั่น ไม่เสียงดัง และยืดอายุการใช้งาน", font_size=16, color=COL_OK).move_to([0, -0.55, 0])
        s4 = Text("4. กฎการออกแบบ: ขนาดถังพัก = 3 × อัตราการไหลปั๊ม (ทั้ง US & SI)", font_size=16, color=COL_CURR).move_to([0, -1.05, 0])
        sum_grp = VGroup(sum_box, s1, s2, s3, s4)
        self.hud(sum_grp)

        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(2.0)

        # ----------------------------------------------------------------------
        # BEAT 64.5–69.0: Review Question Card (Quiet Hold for Retrieval)
        # ----------------------------------------------------------------------
        self.play(FadeOut(sum_grp), run_time=0.5)

        q_box = RoundedRectangle(corner_radius=0.15, width=9.6, height=2.2, color=COL_WARN, fill_color=COL_BG_BOX, fill_opacity=0.95).move_to([0, -0.45, 0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=19, color=COL_WARN).move_to([0, 0.20, 0])
        q_body = Text("ปั๊มไฮดรอลิกจ่ายอัตราไหล 25 gpm ควรออกแบบขนาดถังพักกี่แกลลอน?", font_size=17, color=WHITE).move_to([0, -0.30, 0])
        q_hint = Text("(คิดในใจตามสูตร: ขนาดถัง = 3 × อัตราไหล)", font_size=14, color=COL_GRAY).move_to([0, -0.75, 0])
        q_grp = VGroup(q_box, q_head, q_body, q_hint)
        self.hud(q_grp)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.7)
        # Hold quietly for 3.0s — answer (75 gal) is NOT revealed in video
        self.wait(3.0)

        self.fade_out_all(run_time=0.8)
