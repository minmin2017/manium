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
from hydraulic_circuits import pipe, elbow_pts, flow_dots, rotor_symbol, tank_symbol

# Font configuration
Text.set_default(font=os.environ.get("MANIM_THAI_FONT", "Leelawadee UI"))

# Module colors matching spec and mlib
COL_METAL = METAL       # #90A4AE
COL_FIELD = FIELD       # #42A5F5 (cool oil)
COL_WARN  = WARN        # #FF7043 (hot oil / alert)
COL_OK    = OK          # #26C6DA (conclusion / result)
COL_GRAY  = GRAYTXT     # #B0BEC5 (labels / auxiliary)
COL_CURR  = CURRENT     # #FFB300 (flow / duty)
COL_FORCE = FORCE       # #66BB6A (force vectors)
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
        fn1_t = Text("1. เก็บน้ำมันสำรอง (Reserve Oil)", font_size=17, color=COL_WARN).move_to([-3.8, 2.05, 0])
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
        fn2_t = Text("2. ระบายความร้อน (Heat Dissipation)", font_size=17, color=COL_WARN).next_to(fn1_t, DOWN, aligned_edge=LEFT, buff=0.15)
        self.hud(fn2_t)

        self.play(
            fn1_t.animate.set_color(WHITE),
            FadeIn(fn2_t, shift=UP * 0.2),
            oil_body.animate.set_color(COL_FIELD),
            run_time=2.5
        )
        self.wait(1.0)

        # ----------------------------------------------------------------------
        # BEAT 20.5–24.0: Function 3: แยกฟองอากาศ (De-aeration) — Bubbles Rising
        # ----------------------------------------------------------------------
        fn3_t = Text("3. แยกฟองอากาศ (De-aeration)", font_size=17, color=COL_WARN).next_to(fn2_t, DOWN, aligned_edge=LEFT, buff=0.15)
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
            fn2_t.animate.set_color(WHITE),
            FadeIn(fn3_t, shift=UP * 0.2),
            *[b.animate.shift(UP * 1.5) for b in bubbles],
            run_time=2.8,
            rate_func=linear
        )
        self.play(FadeOut(bubbles), run_time=0.4)

        # ----------------------------------------------------------------------
        # BEAT 24.0–27.5: Function 4: ตกตะกอน (Settling) — Particles Sinking
        # ----------------------------------------------------------------------
        fn4_t = Text("4. ให้สิ่งสกปรกตกตะกอน (Settling)", font_size=17, color=COL_WARN).next_to(fn3_t, DOWN, aligned_edge=LEFT, buff=0.15)
        self.hud(fn4_t)

        # Dark sediment color visually distinct from white bubbles
        COL_DIRT = "#3E2723"
        dirt_pts = [
            [-2.4, -0.45, 0.1], [-1.5, -0.42, -0.2], [-0.8, -0.48, 0.2],
            [+0.8, -0.48, -0.2], [+1.5, -0.42, 0.2], [+2.3, -0.45, -0.1]
        ]
        dirt_group = VGroup(*[
            Dot(point=pt, radius=0.08, color=COL_DIRT)
            for pt in dirt_pts
        ])

        # Step 1: Particles appear near surface and item 4 highlights in WARN
        self.play(
            fn3_t.animate.set_color(WHITE),
            FadeIn(fn4_t, shift=UP * 0.2),
            FadeIn(dirt_group),
            run_time=0.5
        )
        # Step 2: Particles visibly sink downward to the tank floor
        self.play(
            *[d.animate.shift(DOWN * 1.65) for d in dirt_group],
            run_time=2.4,
            rate_func=linear
        )
        self.play(
            fn4_t.animate.set_color(WHITE),
            run_time=0.3
        )
        self.wait(0.2)

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
            run_time=2.6,
            rate_func=linear
        )

        # ----------------------------------------------------------------------
        # BEAT 34.5–37.0: Consequence: Cavitation & Rapid Wear
        # ----------------------------------------------------------------------
        cav_card = RoundedRectangle(
            corner_radius=0.15, width=5.6, height=1.35,
            color=COL_WARN, stroke_width=2.5,
            fill_color="#0F172A", fill_opacity=1.0
        ).move_to([+2.4, 1.85, 0])
        cav_t1 = Text("เกิด Cavitation ในปั๊ม!", font_size=20, color=COL_WARN, weight=BOLD).move_to([+2.4, 2.18, 0])
        cav_t2 = Text("เสียงดังรุนแรง · กัดกร่อนใบพัด · สึกหรอเร็ว", font_size=16, color=WHITE).move_to([+2.4, 1.62, 0])
        cav_arr = arrow3([+2.4, 1.15, 0], [+2.6, 0.75, 0], color=COL_WARN, thickness=0.035)
        cav_grp = VGroup(cav_card, cav_t1, cav_t2, cav_arr)
        self.hud(cav_grp)

        self.play(
            Indicate(pump_full, color=COL_WARN, scale_factor=1.25),
            FadeIn(cav_grp, shift=DOWN * 0.15),
            run_time=0.5
        )
        self.wait(2.2)

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


# ==============================================================================
# Scene: H6_02_Conductors (ตัวนำไฮดรอลิก และขีดจำกัดความเร็ว)
# Lecture slides: hydraulic06.pdf page 5 ("Hydraulic Conductors")
# Duration: ~68s
# Pedagogical Objective:
# - Correct misconception: "ท่อดูดกับท่อจ่ายใช้ท่อขนาดเดียวกันก็ได้"
# - 4 Conductor types: Steel pipe, Steel tubing, Plastic tubing, Flexible hose
# - Continuity principle: Q = A * v (Q constant, constricting A spikes v)
# - Suction pipe velocity limit (1.2 m/s / 4 ft/s): prevents Delta P drop below
#   oil vapor pressure causing destructive cavitation implosion in pump
# - Discharge pipe velocity limit (6.1 m/s / 20 ft/s): high pressure line,
#   limited by friction loss and fluid heating, not cavitation
# - Sizing comparison (Q = 30 L/min): D_suc ≈ 23.0 mm vs D_dis ≈ 10.2 mm
#   D_suc / D_dis = sqrt(v_dis / v_suc) ≈ 2.25x (Area ratio 5.08x)
# ==============================================================================

class H6_02_Conductors(SafeScene):
    def clear_stage(self, keep=(), run_time=0.6):
        """Fade out active stage objects while preserving persistent title badges."""
        targets = [m for m in self.mobjects if m not in keep and m not in getattr(self, "keep_mobs", ())]
        if targets:
            self.play(FadeOut(Group(*targets)), run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # SETUP PERSISTENT ELEMENTS
        # ----------------------------------------------------------------------
        title_mob = title("ตัวนำไฮดรอลิก")
        page_ref_mob = page_ref("hydraulic06 น.5")
        self.keep_mobs = (title_mob, page_ref_mob)

        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title & Page Reference Entrance
        # ----------------------------------------------------------------------
        self.play(
            FadeIn(title_mob, shift=UP * 0.4),
            FadeIn(page_ref_mob),
            run_time=1.0
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–4.6: Question Hook & Thought Hold
        # ----------------------------------------------------------------------
        hook_q = caption_top("ท่อดูดกับท่อจ่าย ใช้ท่อขนาดเดียวกันได้ไหม?", color=COL_GRAY)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(hook_q), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 4.6–13.2: 4 Types of Hydraulic Conductors
        # ----------------------------------------------------------------------
        cap1 = caption_top("4 ชนิดของตัวนำไฮดรอลิก")
        self.play(FadeIn(cap1, shift=UP * 0.4), run_time=0.6)

        # 4 Showcase Cards across width
        xs = [-4.35, -1.45, 1.45, 4.35]
        card_w, card_h = 2.65, 4.25
        cy = -0.65

        # Card 1: Steel pipe
        c1_box = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h,
                                  color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[0], cy, 0])
        p1_body = Rectangle(width=1.65, height=0.36, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([xs[0], cy + 1.25, 0])
        p1_flange_l = Rectangle(width=0.14, height=0.62, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.90).move_to([xs[0] - 0.82, cy + 1.25, 0])
        p1_flange_r = Rectangle(width=0.14, height=0.62, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.90).move_to([xs[0] + 0.82, cy + 1.25, 0])
        icon1 = VGroup(p1_body, p1_flange_l, p1_flange_r)
        t1_title = Text("Steel pipe", font_size=18, color=WHITE).move_to([xs[0], cy + 0.35, 0])
        t1_th = Text("ท่อเหล็กแข็ง", font_size=15, color=COL_CURR).move_to([xs[0], cy - 0.05, 0])
        t1_d1 = Text("• แข็งแรง รับแรงดันสูง", font_size=13, color=COL_GRAY).move_to([xs[0], cy - 0.60, 0])
        t1_d2 = Text("• ราคาประหยัดสุด", font_size=13, color=COL_GRAY).move_to([xs[0], cy - 1.05, 0])
        t1_d3 = Text("• งานติดตั้งถาวร", font_size=13, color=COL_OK).move_to([xs[0], cy - 1.50, 0])
        card1 = VGroup(c1_box, icon1, t1_title, t1_th, t1_d1, t1_d2, t1_d3)

        # Card 2: Steel tubing
        c2_box = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h,
                                  color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[1], cy, 0])
        tube_pts = [
            [xs[1] - 0.75, cy + 0.95, 0],
            [xs[1], cy + 0.95, 0],
            [xs[1] + 0.55, cy + 1.50, 0],
            [xs[1] + 0.75, cy + 1.50, 0]
        ]
        icon2_line = VMobject(color=COL_METAL, stroke_width=6).set_points_as_corners(
            [np.asarray(p, dtype=float) for p in tube_pts]
        )
        icon2_f1 = Circle(radius=0.12, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.90).move_to([xs[1] - 0.75, cy + 0.95, 0])
        icon2_f2 = Circle(radius=0.12, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.90).move_to([xs[1] + 0.75, cy + 1.50, 0])
        icon2 = VGroup(icon2_line, icon2_f1, icon2_f2)
        t2_title = Text("Steel tubing", font_size=18, color=WHITE).move_to([xs[1], cy + 0.35, 0])
        t2_th = Text("ท่อเหล็กดัด", font_size=15, color=COL_CURR).move_to([xs[1], cy - 0.05, 0])
        t2_d1 = Text("• ดัดโค้งได้ แม่นยำ", font_size=13, color=COL_GRAY).move_to([xs[1], cy - 0.60, 0])
        t2_d2 = Text("• ข้อต่อน้อยลง รั่วยาก", font_size=13, color=COL_GRAY).move_to([xs[1], cy - 1.05, 0])
        t2_d3 = Text("• เดินท่อซับซ้อน", font_size=13, color=COL_OK).move_to([xs[1], cy - 1.50, 0])
        card2 = VGroup(c2_box, icon2, t2_title, t2_th, t2_d1, t2_d2, t2_d3)

        # Card 3: Plastic tubing
        c3_box = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h,
                                  color=COL_FIELD, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[2], cy, 0])
        p3_outer = Rectangle(width=1.65, height=0.34, color=COL_FIELD, stroke_width=2.5,
                             fill_color=COL_FIELD).set_fill(COL_FIELD, 0.25).move_to([xs[2], cy + 1.25, 0])
        p3_fluid = Line([xs[2] - 0.75, cy + 1.25, 0], [xs[2] + 0.75, cy + 1.25, 0],
                        color=COL_FIELD, stroke_width=4)
        icon3 = VGroup(p3_outer, p3_fluid)
        t3_title = Text("Plastic tubing", font_size=18, color=WHITE).move_to([xs[2], cy + 0.35, 0])
        t3_th = Text("ท่อพลาสติก", font_size=15, color=COL_CURR).move_to([xs[2], cy - 0.05, 0])
        t3_d1 = Text("• ใช้กับความดันต่ำ", font_size=13, color=COL_GRAY).move_to([xs[2], cy - 0.60, 0])
        t3_d2 = Text("• ราคาถูก น้ำหนักเบา", font_size=13, color=COL_GRAY).move_to([xs[2], cy - 1.05, 0])
        t3_d3 = Text("• สังเกตการไหลได้", font_size=13, color=COL_OK).move_to([xs[2], cy - 1.50, 0])
        card3 = VGroup(c3_box, icon3, t3_title, t3_th, t3_d1, t3_d2, t3_d3)

        # Card 4: Flexible hose
        c4_box = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h,
                                  color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[3], cy, 0])
        hose_curve = CubicBezier(
            [xs[3] - 0.75, cy + 1.05, 0],
            [xs[3] - 0.25, cy + 1.65, 0],
            [xs[3] + 0.25, cy + 0.85, 0],
            [xs[3] + 0.75, cy + 1.45, 0],
            color=COL_METAL, stroke_width=6
        )
        crimp_l = Rectangle(width=0.20, height=0.45, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.90).move_to([xs[3] - 0.75, cy + 1.05, 0])
        crimp_r = Rectangle(width=0.20, height=0.45, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.90).move_to([xs[3] + 0.75, cy + 1.45, 0])
        icon4 = VGroup(hose_curve, crimp_l, crimp_r)
        t4_title = Text("Flexible hose", font_size=18, color=WHITE).move_to([xs[3], cy + 0.35, 0])
        t4_th = Text("สายไฮดรอลิกถัก", font_size=15, color=COL_CURR).move_to([xs[3], cy - 0.05, 0])
        t4_d1 = Text("• ทนแรงสั่นสะเทือน", font_size=13, color=COL_GRAY).move_to([xs[3], cy - 0.60, 0])
        t4_d2 = Text("• ยืดหยุ่นสูง โค้งงอ", font_size=13, color=COL_GRAY).move_to([xs[3], cy - 1.05, 0])
        t4_d3 = Text("• ต่อชิ้นส่วนที่ขยับ", font_size=13, color=COL_OK).move_to([xs[3], cy - 1.50, 0])
        card4 = VGroup(c4_box, icon4, t4_title, t4_th, t4_d1, t4_d2, t4_d3)

        self.play(FadeIn(card1, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(1.1)
        self.play(FadeIn(card2, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(1.1)
        self.play(FadeIn(card3, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(1.1)
        self.play(FadeIn(card4, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(1.1)

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 13.2–20.6: Continuity Equation Q = A * v (Constriction Speedup)
        # ----------------------------------------------------------------------
        cap2 = caption_top("โซ่เหตุผล: Q คงที่ แต่ A เปลี่ยน")
        self.play(FadeIn(cap2, shift=UP * 0.4), run_time=0.6)

        lbl_Q_card = RoundedRectangle(corner_radius=0.12, width=5.2, height=1.1,
                                      color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([3.8, 1.4, 0])
        lbl_Q_t1 = Text("Q = 30 L/min (อัตราไหลคงที่)", font_size=16, color=COL_CURR).move_to([3.8, 1.65, 0])
        lbl_Q_t2 = Text("Q = A × v  →  v = Q / A", font_size=16, color=WHITE).move_to([3.8, 1.15, 0])
        grp_Q = VGroup(lbl_Q_card, lbl_Q_t1, lbl_Q_t2)

        # Straight wide pipe geometry (Y = -0.5)
        pipe_w_top = Line([-5.5, 0.0, 0], [5.5, 0.0, 0], color=COL_METAL, stroke_width=3.5)
        pipe_w_bot = Line([-5.5, -1.0, 0], [5.5, -1.0, 0], color=COL_METAL, stroke_width=3.5)
        pipe_fluid_rect = Rectangle(width=11.0, height=1.0, color=COL_FIELD,
                                    fill_color=COL_FIELD, stroke_width=0).set_fill(COL_FIELD, 0.22).move_to([0, -0.5, 0])
        pipe_wide_grp = VGroup(pipe_fluid_rect, pipe_w_top, pipe_w_bot)

        self.play(
            Create(pipe_wide_grp),
            FadeIn(grp_Q, shift=DOWN * 0.2),
            run_time=1.2
        )
        self.wait(1.0)

        # Exact physical velocity model for dots in constricted nozzle:
        # Segment 1 (wide left): x in [-5.5, -1.8], v1 = 2.4 units/s
        # Segment 2 (narrow mid): x in [-1.8, 1.8], v2 = 6.0 units/s (2.5x speedup!)
        # Segment 3 (wide right): x in [1.8, 5.5], v1 = 2.4 units/s
        t1_end = 3.7 / 2.4       # 1.5417 s
        t2_dur = 3.6 / 6.0       # 0.6000 s
        t2_end = t1_end + t2_dur # 2.1417 s
        t3_dur = 3.7 / 2.4       # 1.5417 s
        t_cycle = t1_end + t2_dur + t3_dur # 3.6833 s

        def get_pos_x(t_mod):
            if t_mod < t1_end:
                return -5.5 + 2.4 * t_mod
            elif t_mod < t2_end:
                return -1.8 + 6.0 * (t_mod - t1_end)
            else:
                return 1.8 + 2.4 * (t_mod - t2_end)

        pts_c_top = [
            [-5.5, 0.0, 0], [-2.2, 0.0, 0], [-1.6, -0.32, 0],
            [1.6, -0.32, 0], [2.2, 0.0, 0], [5.5, 0.0, 0]
        ]
        pts_c_bot = [
            [-5.5, -1.0, 0], [-2.2, -1.0, 0], [-1.6, -0.68, 0],
            [1.6, -0.68, 0], [2.2, -1.0, 0], [5.5, -1.0, 0]
        ]
        pipe_c_top = VMobject(color=COL_METAL, stroke_width=3.5).set_points_as_corners([np.asarray(p, dtype=float) for p in pts_c_top])
        pipe_c_bot = VMobject(color=COL_METAL, stroke_width=3.5).set_points_as_corners([np.asarray(p, dtype=float) for p in pts_c_bot])
        poly_pts = pts_c_top + pts_c_bot[::-1]
        pipe_c_fluid = Polygon(*poly_pts, color=COL_FIELD, fill_color=COL_FIELD, stroke_width=0).set_fill(COL_FIELD, 0.22)
        pipe_constrict_grp = VGroup(pipe_c_fluid, pipe_c_top, pipe_c_bot)

        # Dynamic velocity live indicator
        v_tracker = ValueTracker(1.2)
        v_row = live_row("v =", "m/s", lambda: v_tracker.get_value(), anchor=[-2.8, 1.4, 0],
                         num_color=COL_CURR, label_color=WHITE, unit_color=COL_CURR, decimals=1)

        sub_constrict = Text("บีบ A ให้เล็กลง → v ต้องพุ่งขึ้น (Q เท่าเดิม)", font_size=16, color=COL_CURR).move_to([0, -1.8, 0])

        time_tracker = ValueTracker(0.0)
        num_dots = 6
        dots_grp = VGroup()
        for i in range(num_dots):
            dt_offset = i * (t_cycle / num_dots)
            dot = Dot(radius=0.08, color=COL_CURR)
            def make_upd(off):
                return lambda m: m.move_to([get_pos_x((time_tracker.get_value() + off) % t_cycle), -0.5, 0])
            dot.add_updater(make_upd(dt_offset))
            dots_grp.add(dot)

        self.add(v_row, dots_grp)
        self.play(
            Transform(pipe_wide_grp, pipe_constrict_grp),
            v_tracker.animate.set_value(6.1),
            time_tracker.animate.set_value(3.2),
            FadeIn(sub_constrict, shift=UP * 0.2),
            run_time=3.2,
            rate_func=linear
        )

        dots_grp.clear_updaters()
        v_row.clear_updaters()
        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 20.6–33.5: Suction Pipe & Cavitation Danger (v <= 1.2 m/s)
        # ----------------------------------------------------------------------
        cap3 = caption_top("ทำไมท่อดูดจำกัดแค่ 1.2 m/s")
        self.play(FadeIn(cap3, shift=UP * 0.4), run_time=0.6)

        # Tank symbol (left), Pump rotor (right), Suction pipe in between
        tank_grp, t_ports = tank_symbol([-4.8, -0.65, 0], w=1.1, h=1.0, color=COL_METAL)
        t_lbl = Text("ถังพักน้ำมัน", font_size=13, color=COL_GRAY).next_to(tank_grp, DOWN, buff=0.12)

        pump_grp, p_ports = rotor_symbol([3.6, -0.65, 0], angle=0, r=0.45, color=COL_METAL, filled=True)
        p_lbl = Text("ปั๊มไฮดรอลิก", font_size=13, color=COL_GRAY).next_to(pump_grp, DOWN, buff=0.12)

        suction_pts = [
            [-4.25, -0.65, 0],
            [3.15, -0.65, 0]
        ]
        pipe_suction = pipe(suction_pts, color=COL_WARN, width=5.0)
        pipe_suc_lbl = Text("ท่อดูด (Suction Line): ความดันต่ำกว่าบรรยากาศ", font_size=15, color=COL_WARN).move_to([-0.5, -0.25, 0])

        self.play(
            FadeIn(tank_grp), FadeIn(t_lbl),
            FadeIn(pump_grp), FadeIn(p_lbl),
            Create(pipe_suction),
            FadeIn(pipe_suc_lbl),
            run_time=1.4
        )
        self.play(Indicate(pipe_suction, color=COL_WARN), run_time=1.2)

        # Pressure graph along suction pipe
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-0.2, 1.8, 0.5],
            x_length=6.2,
            y_length=2.0,
            axis_config={"color": COL_METAL, "stroke_width": 2}
        ).move_to([0.2, 1.25, 0])
        ax_lbl_x = Text("ระยะทางท่อ →", font_size=12, color=COL_GRAY).next_to(axes.x_axis, DOWN, buff=0.1)
        ax_lbl_y = Text("ความดัน P", font_size=12, color=COL_GRAY).next_to(axes.y_axis, LEFT, buff=0.1)

        p_vap_val = 0.55
        vapor_line = DashedLine(axes.c2p(0, p_vap_val), axes.c2p(6, p_vap_val),
                                color=COL_WARN, stroke_width=2.5, dash_length=0.10)
        lbl_vapor = Text("ความดันไอ P_vap", font_size=12, color=COL_WARN).next_to(vapor_line, RIGHT, buff=0.15)

        # Safe curve: P_safe(x) = 1.45 - 0.10 * x (stays above vapor_line everywhere)
        curve_safe = axes.plot(lambda x: 1.45 - 0.10 * x, x_range=[0, 6], color=COL_CURR, stroke_width=3)
        lbl_curve_safe = Text("ความดันปกติ (v ≤ 1.2 m/s)", font_size=12, color=COL_CURR).move_to(axes.c2p(2.2, 1.55))

        self.play(
            Create(axes), FadeIn(ax_lbl_x), FadeIn(ax_lbl_y),
            Create(vapor_line), FadeIn(lbl_vapor),
            Create(curve_safe), FadeIn(lbl_curve_safe),
            run_time=1.8
        )
        self.wait(1.2)

        # High velocity curve dips below vapor line:
        # P_steep(x) = 1.40 - 0.28 * x
        # 1.40 - 0.28 * x_cross = 0.55 => 0.28 * x_cross = 0.85 => x_cross = 3.0357
        x_cross = (1.40 - p_vap_val) / 0.28  # 3.035714...
        curve_steep = axes.plot(lambda x: 1.40 - 0.28 * x, x_range=[0, 6], color=COL_WARN, stroke_width=3)
        lbl_curve_steep = Text("v สูงเกินไป → ΔP ตกฮวบ จน P ≤ P_vap!", font_size=12, color=COL_WARN).move_to(axes.c2p(2.4, 1.55))

        pt_intersect = axes.c2p(x_cross, p_vap_val)
        dot_cross = Dot(pt_intersect, radius=0.09, color=WHITE)

        # Physical location in pipe below matching x_cross:
        frac_cross = x_cross / 6.0
        pipe_cross_x = -4.25 + frac_cross * (3.15 - (-4.25))

        bubble_list = []
        for bx in np.linspace(pipe_cross_x, 2.8, 12):
            b_r = 0.05 + 0.03 * np.sin(bx * 7.0)
            by = -0.65 + 0.12 * np.cos(bx * 9.0)
            b_dot = Circle(radius=b_r, color=WHITE, fill_color=WHITE, stroke_width=1).set_fill(WHITE, 0.85).move_to([bx, by, 0])
            bubble_list.append(b_dot)
        bubbles_grp = VGroup(*bubble_list)

        cap_cav = Text("น้ำมันเดือดเป็นฟองในของเหลว = Cavitation", font_size=16, color=COL_WARN).move_to([0, -1.8, 0])

        self.play(
            ReplacementTransform(curve_safe, curve_steep),
            ReplacementTransform(lbl_curve_safe, lbl_curve_steep),
            FadeIn(dot_cross),
            FadeIn(bubbles_grp, shift=UP * 0.1),
            FadeIn(cap_cav, shift=UP * 0.2),
            run_time=2.5
        )
        self.wait(1.0)

        # Bubbles travel into pump and implode -> pump vibration
        self.play(
            bubbles_grp.animate.shift(RIGHT * 1.0).set_opacity(0.0),
            Indicate(pump_grp, color=COL_WARN, scale_factor=1.28),
            run_time=2.0
        )
        warn_txt = Text("ฟองยุบตัวในปั๊ม → กัดกร่อนใบพัด เสียงดัง และพังเร็ว!", font_size=16, color=COL_WARN).move_to([0, -1.8, 0])
        self.play(ReplacementTransform(cap_cav, warn_txt), run_time=0.6)
        self.wait(0.6)

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 34.3–41.6: Discharge Pipe & Heat / Friction Limit (v <= 6.1 m/s)
        # ----------------------------------------------------------------------
        cap4 = caption_top("ท่อจ่ายปล่อยถึง 6.1 m/s ได้ยังไง")
        self.play(FadeIn(cap4, shift=UP * 0.4), run_time=0.6)

        pump_dis_grp, _ = rotor_symbol([-4.0, -0.65, 0], angle=0, r=0.45, color=COL_METAL, filled=True)
        dis_pts = [[-3.55, -0.65, 0], [4.5, -0.65, 0]]
        pipe_discharge = pipe(dis_pts, color=COL_FIELD, width=5.0)

        pipe_dis_lbl = Text("ท่อจ่าย (Discharge Line): ความดันสูงมาก (100–300 bar)", font_size=15, color=COL_FIELD).move_to([0, -0.25, 0])
        pipe_dis_safe = Text("ความดันสูงกว่า Vapor Pressure มหาศาล — ไม่มีทางเกิด Cavitation!", font_size=14, color=WHITE).move_to([0, -1.05, 0])

        self.play(
            FadeIn(pump_dis_grp),
            Create(pipe_discharge),
            FadeIn(pipe_dis_lbl),
            FadeIn(pipe_dis_safe),
            run_time=1.6
        )

        dots_dis, anims_dis = flow_dots(dis_pts, color=COL_FIELD, n=6, run_time=1.3)
        self.play(Indicate(pipe_discharge, color=COL_FIELD), *anims_dis, run_time=1.3)

        # Fade out discharge labels before heat dissipation arrows appear
        self.play(FadeOut(pipe_dis_lbl), FadeOut(pipe_dis_safe), run_time=0.4)

        # Heat dissipation arrows radiating from pipe wall
        heat_arrows = VGroup()
        for hx in np.linspace(-2.5, 3.5, 7):
            heat_arrows.add(Arrow([hx, -0.40, 0], [hx, 0.20, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.15))
            heat_arrows.add(Arrow([hx, -0.90, 0], [hx, -1.50, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.15))

        friction_card = RoundedRectangle(corner_radius=0.12, width=8.8, height=1.1,
                                         color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([0, 1.25, 0])
        f_t1 = Text("ตัวจำกัดความเร็วคือ ความร้อน & การสูญเสียแรงดัน (ΔP ∝ v²)", font_size=15, color=COL_WARN).move_to([0, 1.50, 0])
        f_t2 = Text("ไม่ใช่ Cavitation จึงยอมให้ไหลเร็วได้ถึง 6.1 m/s (20 ft/s)", font_size=14, color=WHITE).move_to([0, 1.05, 0])
        friction_grp = VGroup(friction_card, f_t1, f_t2, heat_arrows)

        self.play(FadeIn(friction_grp, shift=UP * 0.2), run_time=1.2)
        self.wait(1.6)

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 41.6–50.6: Worked Sizing Example (Q = 30 L/min)
        # ----------------------------------------------------------------------
        cap5 = caption_top("ตัวอย่างคำนวณ: Q = 30 L/min")
        self.play(FadeIn(cap5, shift=UP * 0.4), run_time=0.6)

        prob_box = RoundedRectangle(corner_radius=0.12, width=8.8, height=1.1,
                                    color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([0, 1.45, 0])
        pr_t1 = Text("โจทย์: อัตราการไหล Q = 30 L/min", font_size=16, color=COL_CURR).move_to([0, 1.70, 0])
        pr_t2 = Text("แปลงหน่วย SI: Q = 30 / (60 × 1000) = 0.0005 m³/s", font_size=15, color=WHITE).move_to([0, 1.25, 0])
        prob_grp = VGroup(prob_box, pr_t1, pr_t2)
        self.play(FadeIn(prob_grp, shift=DOWN * 0.2), run_time=0.6)
        self.wait(1.0)

        # Step 1: Suction pipe calculation (Left column, WARN)
        suc_box = RoundedRectangle(corner_radius=0.12, width=5.6, height=2.7,
                                   color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([-3.4, -0.65, 0])
        sc_h = Text("1. ท่อดูด (จำกัด v ≤ 1.2 m/s)", font_size=16, color=COL_WARN).move_to([-3.4, 0.35, 0])
        sc_l1 = Text("A_suc = Q / v = 0.0005 / 1.2", font_size=15, color=WHITE).move_to([-3.4, -0.10, 0])
        sc_l2 = Text("A_suc = 4.17 × 10⁻⁴ m²", font_size=15, color=WHITE).move_to([-3.4, -0.55, 0])
        sc_l3 = Text("D_suc = √(4A/π) ≈ 23.0 mm", font_size=16, color=COL_WARN).move_to([-3.4, -1.05, 0])
        suc_calc_grp = VGroup(suc_box, sc_h, sc_l1, sc_l2, sc_l3)

        self.play(FadeIn(suc_calc_grp, shift=RIGHT * 0.3), run_time=1.5)
        self.wait(1.5)

        # Step 2: Discharge pipe calculation (Right column, FIELD)
        dis_box = RoundedRectangle(corner_radius=0.12, width=5.6, height=2.7,
                                   color=COL_FIELD, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([3.4, -0.65, 0])
        dc_h = Text("2. ท่อจ่าย (จำกัด v ≤ 6.1 m/s)", font_size=16, color=COL_FIELD).move_to([3.4, 0.35, 0])
        dc_l1 = Text("A_dis = Q / v = 0.0005 / 6.1", font_size=15, color=WHITE).move_to([3.4, -0.10, 0])
        dc_l2 = Text("A_dis = 8.20 × 10⁻⁵ m²", font_size=15, color=WHITE).move_to([3.4, -0.55, 0])
        dc_l3 = Text("D_dis = √(4A/π) ≈ 10.2 mm", font_size=16, color=COL_FIELD).move_to([3.4, -1.05, 0])
        dis_calc_grp = VGroup(dis_box, dc_h, dc_l1, dc_l2, dc_l3)

        self.play(FadeIn(dis_calc_grp, shift=LEFT * 0.3), run_time=1.5)
        self.wait(1.5)

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 50.6–57.0: Visual Comparison — Bar Chart & Sized Cross-Sections
        # ----------------------------------------------------------------------
        cap_comp = caption_top("เปรียบเทียบขนาด: ท่อดูดต้องอ้วนกว่า ~2.25 เท่า")
        self.play(FadeIn(cap_comp, shift=UP * 0.4), run_time=0.6)

        # Exact mathematical radius ratio verification per High-Risk Check (c)
        D_SUC_MM = 23.0
        D_DIS_MM = 10.2
        RATIO_ACTUAL = D_SUC_MM / D_DIS_MM  # 2.25490196...

        r_dis = 0.65
        r_suc = r_dis * RATIO_ACTUAL  # 1.465686...
        assert abs((r_suc / r_dis) - (D_SUC_MM / D_DIS_MM)) < 1e-6, "Radii ratio must match 23.0/10.2 exactly!"

        # Bar chart on left
        base_line = Line([-5.5, -1.9, 0], [-1.0, -1.9, 0], color=COL_METAL, stroke_width=2.5)

        bar_h_dis = 1.15
        bar_h_suc = bar_h_dis * RATIO_ACTUAL  # 2.593...
        assert abs((bar_h_suc / bar_h_dis) - (D_SUC_MM / D_DIS_MM)) < 1e-6, "Bar heights ratio must match 23.0/10.2 exactly!"

        bar_suc = Rectangle(width=1.2, height=bar_h_suc, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.88).move_to([-4.4, -1.9 + bar_h_suc / 2, 0])
        bar_suc_lbl = Text("23.0 mm", font_size=15, color=COL_WARN).next_to(bar_suc, UP, buff=0.1)
        bar_suc_sub = Text("D ท่อดูด", font_size=13, color=COL_GRAY).next_to(bar_suc, DOWN, buff=0.15)

        bar_dis = Rectangle(width=1.2, height=bar_h_dis, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.88).move_to([-2.2, -1.9 + bar_h_dis / 2, 0])
        bar_dis_lbl = Text("10.2 mm", font_size=15, color=COL_FIELD).next_to(bar_dis, UP, buff=0.1)
        bar_dis_sub = Text("D ท่อจ่าย", font_size=13, color=COL_GRAY).next_to(bar_dis, DOWN, buff=0.15)

        # Cross section circles on right
        c_suc = Circle(radius=r_suc, color=COL_WARN, fill_color=COL_WARN, stroke_width=3).set_fill(COL_WARN, 0.35).move_to([1.5, -0.4, 0])
        c_suc_lbl = Text("หน้าตัดท่อดูด", font_size=14, color=COL_WARN).next_to(c_suc, UP, buff=0.15)
        c_suc_dim = Text("D ≈ 23.0 mm", font_size=15, color=WHITE).move_to(c_suc.get_center())

        c_dis = Circle(radius=r_dis, color=COL_FIELD, fill_color=COL_FIELD, stroke_width=3).set_fill(COL_FIELD, 0.35).move_to([4.6, -0.4, 0])
        c_dis_lbl = Text("หน้าตัดท่อจ่าย", font_size=14, color=COL_FIELD).next_to(c_dis, UP, buff=0.15)
        c_dis_dim = Text("D ≈ 10.2 mm", font_size=15, color=WHITE).move_to(c_dis.get_center())

        ratio_banner = Text("อัตราส่วนเส้นผ่านศูนย์กลาง = 23.0 / 10.2 ≈ 2.25 เท่า (พื้นที่ใหญ่กว่า 5.08 เท่า!)",
                            font_size=16, color=COL_OK).move_to([0, -2.5, 0])

        self.play(
            Create(base_line),
            GrowFromEdge(bar_suc, DOWN), FadeIn(bar_suc_lbl), FadeIn(bar_suc_sub),
            GrowFromEdge(bar_dis, DOWN), FadeIn(bar_dis_lbl), FadeIn(bar_dis_sub),
            Create(c_suc), FadeIn(c_suc_lbl), FadeIn(c_suc_dim),
            Create(c_dis), FadeIn(c_dis_lbl), FadeIn(c_dis_dim),
            FadeIn(ratio_banner, shift=UP * 0.2),
            run_time=4.5
        )
        self.wait(1.9)

        # Clear comparison objects before introducing theoretical formula
        self.clear_stage(run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 57.0–60.0: Theoretical Ratio Formula
        # ----------------------------------------------------------------------
        formula_box = RoundedRectangle(corner_radius=0.14, width=9.2, height=1.6,
                                       color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.4, 0])
        f_line1 = Text("D_suc / D_dis = √(v_dis / v_suc)", font_size=18, color=WHITE).move_to([0, 0.05, 0])
        f_line2 = Text("= √(6.1 / 1.2) = √5.08 ≈ 2.25", font_size=19, color=COL_OK).move_to([0, -0.45, 0])
        formula_grp = VGroup(formula_box, f_line1, f_line2)

        self.play(
            FadeIn(formula_grp, shift=UP * 0.3),
            run_time=1.8
        )
        self.wait(1.2)

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 60.6–63.0: Executive Summary Card
        # ----------------------------------------------------------------------
        cap_sum = caption_top("สรุปหลักการสำคัญ: ตัวนำไฮดรอลิก", color=COL_OK)
        self.play(FadeIn(cap_sum, shift=UP * 0.4), run_time=0.6)

        sum_box = RoundedRectangle(corner_radius=0.16, width=10.6, height=3.3,
                                   color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.45, 0])
        s1 = Text("1. 4 ชนิดตัวนำ: Steel pipe (ถาวร), Steel tubing (แม่นยำ), Plastic (เบา), Flexible hose (ขยับ)", font_size=15, color=WHITE).move_to([0, 0.65, 0])
        s2 = Text("2. ความต่อเนื่อง: Q = A × v  (เมื่อบีบ A ให้เล็กลง ความเร็ว v จะพุ่งสูงขึ้น)", font_size=15, color=COL_CURR).move_to([0, 0.15, 0])
        s3 = Text("3. ท่อดูด v ≤ 1.2 m/s: ความดันต่ำ เสี่ยง Cavitation (เดือดเป็นฟองกัดกร่อนปั๊ม)", font_size=15, color=COL_WARN).move_to([0, -0.35, 0])
        s4 = Text("4. ท่อจ่าย v ≤ 6.1 m/s: ความดันสูง ไม่เกิดฟอง ตัวจำกัดคือความร้อน & สูญเสียแรงดัน", font_size=15, color=COL_FIELD).move_to([0, -0.85, 0])
        s5 = Text("5. สัดส่วนขนาด: D ∝ √(1/v) → ท่อดูดต้องมีเส้นผ่านศูนย์กลางโตกว่าท่อจ่าย ~2.25 เท่า", font_size=15, color=COL_OK).move_to([0, -1.35, 0])
        sum_grp = VGroup(sum_box, s1, s2, s3, s4, s5)

        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(1.6)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        self.fade_out_all(run_time=0.8)


# ==============================================================================
# Scene: H6_03_PressureRating (ความดันที่ท่อรับได้)
# Lecture slides: hydraulic06.pdf page 6 ("Pressure Rating of Conductors")
# References:
# - Esposito, Anthony, "Fluid Power with Applications", 7th ed., Ch. 5 (Conductors and Fittings).
# - Tensile strength of mild steel ASTM A106 / AISI 1018: S ≈ 380 - 440 MPa.
# - Factor of Safety criteria: >2500 psi -> FS=4, 1000-2500 psi -> FS=6, <1000 psi -> FS=8.
# Duration: ~91s
# Pedagogical Objective:
# - Misconception: "พื้นที่รับแรงดันของท่อกลมคำนวณยังไง ผิวมันโค้งนี่นา"
# - Geometric proof: Radial pressure force components cancel horizontally in pairs,
#   leaving net vertical force = P * (Projected Area) = P * (L * Di).
# - Force balance: P * L * Di = 2 * (t * L) * σ  -->  σ = P * Di / (2t).
# - Burst Pressure (BP): when σ reaches tensile strength S  -->  BP = 2tS / Di.
# - Working Pressure (WP): WP = BP / FS.
# - Classic exam trap: Verify that computed WP remains in the selected FS range!
# ==============================================================================
class H6_03_PressureRating(SafeThreeDScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # Geometry and Camera Verification (§36)
        # ----------------------------------------------------------------------
        # Camera axial end-on angle: phi=0, theta=-90*DEGREES
        # Rotation matrix is exactly identity I(3x3)
        # Measured horizontal radius = 1.600, vertical radius = 1.600 (ratio 1.000126, 0.0126% diff)
        R_outer = 1.60
        R_inner = 1.40
        t_wall = 0.20
        L_pipe = 2.40
        C_pipe = np.array([0.0, -0.80, 0.0])

        assert np.isclose(R_outer - R_inner, t_wall), "Wall thickness must match Ro - Ri"
        assert L_pipe > 0, "Pipe length must be positive"

        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title & Page Reference Badge
        # ----------------------------------------------------------------------
        title_mob = title("ความดันที่ท่อรับได้")
        page_ref_mob = page_ref("hydraulic06 น.6")
        self.hud(title_mob, page_ref_mob)

        self.play(
            FadeIn(title_mob, shift=UP * 0.4),
            FadeIn(page_ref_mob),
            run_time=1.0
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–4.6: Hook Question
        # ----------------------------------------------------------------------
        hook_q = caption_top("ท่อกลม พื้นที่รับแรงดันคำนวณยังไง ผิวมันโค้งนะ?")
        self.hud(hook_q)

        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(hook_q), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 4.6–9.6: 3D Pipe Model & Ambient Rotation (Establishing Shot §36)
        # ----------------------------------------------------------------------
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES)

        cap1 = caption_top("ความดัน P ดันผนังท่อออกทุกทิศทางเท่ากัน")
        self.hud(cap1)

        pipe_3d = Cylinder(radius=R_outer, height=L_pipe, resolution=(10, 10),
                           fill_color=COL_METAL, stroke_width=0).move_to([0.0, -0.60, 0.0])
        pipe_3d.set_opacity(0.85)

        # 8 radial 3D pressure arrows radiating from central axis
        rad_angles_3d = np.linspace(0, TAU, 8, endpoint=False)
        rad_arrows_3d = VGroup(*[
            arrow3(
                start=np.array([0.0, -0.60, 0.0]) + 0.35 * np.array([np.cos(a), np.sin(a), 0.0]),
                end=np.array([0.0, -0.60, 0.0]) + 1.45 * np.array([np.cos(a), np.sin(a), 0.0]),
                color=COL_CURR
            )
            for a in rad_angles_3d
        ])

        self.play(
            FadeIn(pipe_3d, shift=UP * 0.3),
            FadeIn(cap1, shift=UP * 0.3),
            run_time=0.8
        )
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(
            LaggedStart(*[Create(a) for a in rad_arrows_3d], lag_ratio=0.15),
            run_time=2.4
        )
        self.wait(1.2)
        self.stop_ambient_camera_rotation()
        self.wait(0.6)

        # ----------------------------------------------------------------------
        # BEAT 9.6–13.0: Longitudinal Split (Half-Pipe & Length L Dimension)
        # ----------------------------------------------------------------------
        cap_split = caption_top("ผ่าครึ่งตามยาว ยาว L — จะพิสูจน์พื้นที่รับแรงตรงนี้")
        self.hud(cap_split)

        half_pipe_3d = Cylinder(radius=R_outer, height=L_pipe, v_range=(0, PI),
                                show_ends=False, resolution=(10, 10),
                                fill_color=COL_METAL, stroke_width=0).move_to([0.0, -0.60, 0.0])
        half_pipe_3d.set_opacity(0.85)

        dim_L_start = np.array([1.80, -0.60, -1.20])
        dim_L_end   = np.array([1.80, -0.60, +1.20])
        dim_L_line  = line3(dim_L_start, dim_L_end, color=COL_GRAY)
        lbl_L = Text("L (ความยาว)", font_size=18, color=COL_GRAY).move_to([2.30, -0.60, 0.0])
        self.world_text(lbl_L)

        self.play(
            ReplacementTransform(cap1, cap_split),
            FadeOut(rad_arrows_3d),
            ReplacementTransform(pipe_3d, half_pipe_3d),
            Create(dim_L_line),
            FadeIn(lbl_L),
            run_time=1.8
        )
        self.wait(1.6)

        # ----------------------------------------------------------------------
        # BEAT 13.0–15.3: Transition to Axial End-On View (Verification Shot §36)
        # ----------------------------------------------------------------------
        cap_endon = caption_top("มองตรงปลายท่อ — เห็นหน้าตัดเต็มๆ")
        self.hud(cap_endon)

        self.play(
            FadeOut(dim_L_line),
            FadeOut(lbl_L),
            ReplacementTransform(cap_split, cap_endon),
            run_time=0.6
        )
        # Smooth camera movement to pure axial view looking down Z-axis
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        self.wait(0.9)
        self.play(FadeOut(cap_endon), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 15.3–19.6: Semicircular Cross-Section & 8 Radial Pressure Vectors
        # ----------------------------------------------------------------------
        cap2 = caption_top("⚠️ ทำไมพื้นที่รับแรงถึงเป็น L×Di ทั้งที่ผิวโค้ง")
        self.hud(cap2)
        self.play(FadeIn(cap2, shift=UP * 0.4), run_time=0.6)

        # Draw precise 2D cross-section rim on front plane for visual clarity
        arc_inner = Arc(radius=R_inner, start_angle=0, angle=PI, arc_center=C_pipe,
                        color=COL_METAL, stroke_width=3.5)
        arc_outer = Arc(radius=R_outer, start_angle=0, angle=PI, arc_center=C_pipe,
                        color=COL_METAL, stroke_width=3.5)
        wall_cut_l = Line(C_pipe + np.array([-R_outer, 0, 0]), C_pipe + np.array([-R_inner, 0, 0]),
                          color=COL_METAL, stroke_width=3.5)
        wall_cut_r = Line(C_pipe + np.array([+R_inner, 0, 0]), C_pipe + np.array([+R_outer, 0, 0]),
                          color=COL_METAL, stroke_width=3.5)
        rim_grp = VGroup(arc_inner, arc_outer, wall_cut_l, wall_cut_r)

        # 4 symmetric pairs of radial arrows (8 arrows total)
        # Alpha angles measured away from vertical (+Y axis = 90 deg)
        alphas = [75 * DEGREES, 55 * DEGREES, 35 * DEGREES, 15 * DEGREES]
        pressure_arrows = []
        arrow_pairs_data = []

        for alpha in alphas:
            theta_r = 90 * DEGREES - alpha
            theta_l = 90 * DEGREES + alpha

            u_r = np.array([np.cos(theta_r), np.sin(theta_r), 0.0])
            u_l = np.array([np.cos(theta_l), np.sin(theta_l), 0.0])

            arr_r = Arrow(start=C_pipe + 0.35 * u_r, end=C_pipe + (R_inner - 0.02) * u_r,
                          color=COL_CURR, stroke_width=4.0, buff=0, max_tip_length_to_length_ratio=0.25)
            arr_l = Arrow(start=C_pipe + 0.35 * u_l, end=C_pipe + (R_inner - 0.02) * u_l,
                          color=COL_CURR, stroke_width=4.0, buff=0, max_tip_length_to_length_ratio=0.25)

            pressure_arrows.extend([arr_r, arr_l])
            arrow_pairs_data.append((arr_r, arr_l, alpha, u_r, u_l))

        cap_radial = caption_top("ความดันดันตั้งฉากกับผิวทุกจุด")
        self.hud(cap_radial)

        self.play(
            Create(rim_grp),
            ReplacementTransform(cap2, cap_radial),
            LaggedStart(*[Create(a) for a in pressure_arrows], lag_ratio=0.12),
            run_time=2.5
        )
        self.wait(0.6)

        # ----------------------------------------------------------------------
        # BEAT 19.6–24.0: Decompose Arrows into Horizontal & Vertical Components
        # ----------------------------------------------------------------------
        cap3 = caption_top("แตกแต่ละลูกศรเป็นแนวนอน + แนวตั้ง")
        self.hud(cap3)
        self.play(ReplacementTransform(cap_radial, cap3), run_time=0.8)

        # Construct H and V component arrows for each pair
        h_components = []
        v_components = []
        decomp_anims = []

        comp_scale = 0.95
        for arr_r, arr_l, alpha, u_r, u_l in arrow_pairs_data:
            tip_r = C_pipe + (R_inner - 0.02) * u_r
            tip_l = C_pipe + (R_inner - 0.02) * u_l

            L_h = comp_scale * np.sin(alpha)
            L_v = comp_scale * np.cos(alpha)

            # Horizontal arrows: right points RIGHT, left points LEFT
            h_r = Arrow(start=tip_r - np.array([L_h, 0, 0]), end=tip_r,
                        color=COL_GRAY, stroke_width=3.0, buff=0, max_tip_length_to_length_ratio=0.30)
            h_l = Arrow(start=tip_l + np.array([L_h, 0, 0]), end=tip_l,
                        color=COL_GRAY, stroke_width=3.0, buff=0, max_tip_length_to_length_ratio=0.30)

            # Vertical arrows: both point UP
            v_r = Arrow(start=tip_r - np.array([0, L_v, 0]), end=tip_r,
                        color=COL_FORCE, stroke_width=3.2, buff=0, max_tip_length_to_length_ratio=0.30)
            v_l = Arrow(start=tip_l - np.array([0, L_v, 0]), end=tip_l,
                        color=COL_FORCE, stroke_width=3.2, buff=0, max_tip_length_to_length_ratio=0.30)

            h_components.append((h_r, h_l))
            v_components.extend([v_r, v_l])

            decomp_anims.append(
                AnimationGroup(
                    Create(h_r), Create(h_l),
                    Create(v_r), Create(v_l)
                )
            )

        self.play(
            LaggedStart(*decomp_anims, lag_ratio=0.25),
            run_time=3.6
        )

        # ----------------------------------------------------------------------
        # BEAT 24.0–28.0: Core Proof — Pairwise Horizontal Cancellation (Outside-In)
        # ----------------------------------------------------------------------
        cap_cancel = caption_top("แนวนอนหักล้างกันหมดทีละคู่ ซ้าย=ขวา")
        self.hud(cap_cancel)

        # Pair 1 (alpha=75 deg, outermost) cancels first -> Pair 4 (15 deg, innermost) cancels last
        self.play(
            ReplacementTransform(cap3, cap_cancel),
            FadeOut(VGroup(h_components[0][0], h_components[0][1])),
            run_time=0.9
        )
        self.play(
            FadeOut(VGroup(h_components[1][0], h_components[1][1])),
            run_time=0.9
        )
        self.play(
            FadeOut(VGroup(h_components[2][0], h_components[2][1])),
            run_time=0.9
        )
        self.play(
            FadeOut(VGroup(h_components[3][0], h_components[3][1])),
            run_time=0.8
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 28.0–31.0: Sum of Vertical Components -> Single Force Arrow
        # ----------------------------------------------------------------------
        cap_res = caption_top("เหลือแรงแนวตั้งรวม = P × พื้นที่ฉาย")
        self.hud(cap_res)

        single_up_arrow = Arrow(start=C_pipe, end=C_pipe + np.array([0, 1.85, 0]),
                                color=COL_FORCE, stroke_width=6.0, buff=0,
                                max_tip_length_to_length_ratio=0.22)
        lbl_force = Text("F = P × (พื้นที่ฉาย)", font_size=22, color=COL_FORCE).next_to(single_up_arrow, RIGHT, buff=0.20)
        self.hud(lbl_force)

        self.play(
            ReplacementTransform(cap_cancel, cap_res),
            ReplacementTransform(VGroup(*v_components, *pressure_arrows), single_up_arrow),
            FadeIn(lbl_force),
            run_time=2.5
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 31.0–34.0: Projected Area = L * Di (Under Semicircle)
        # ----------------------------------------------------------------------
        cap_proj = caption_top("พื้นที่ฉาย = L × Di (ไม่ใช่พื้นที่ผิวโค้งจริง)")
        self.hud(cap_proj)

        projected_rect = Rectangle(width=2 * R_inner, height=0.24,
                                   color=COL_OK, fill_color=COL_OK).set_fill(COL_OK, 0.35).set_stroke(COL_OK, 2.0).move_to(C_pipe + np.array([0, -0.12, 0]))
        lbl_area = Text("พื้นที่ฉาย = L × Di", font_size=20, color=COL_OK).next_to(projected_rect, DOWN, buff=0.20)
        self.hud(lbl_area)

        self.play(
            ReplacementTransform(cap_res, cap_proj),
            Create(projected_rect),
            FadeIn(lbl_area),
            run_time=2.2
        )
        self.wait(0.8)

        # ----------------------------------------------------------------------
        # BEAT 34.0–35.6: Clear Proof Visuals & Transition to Force Balance
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(half_pipe_3d, rim_grp, single_up_arrow, lbl_force,
                           projected_rect, lbl_area, cap_proj)),
            run_time=0.8
        )

        cap4 = caption_top("สมดุลแรง: หาความเค้น σ")
        self.hud(cap4)
        self.play(FadeIn(cap4, shift=UP * 0.4), run_time=0.8)

        # ----------------------------------------------------------------------
        # BEAT 35.6–42.0: Derivation of Hoop Stress: σ = P·Di / (2t)
        # ----------------------------------------------------------------------
        eq_head = Text("แรงดันของไหลขึ้น = แรงผนังท่อต้านลง", font_size=24, color=WHITE).move_to([0.0, 1.40, 0.0])
        eq_step1 = Text("P · (L · Di) = 2 · (t · L) · σ", font_size=30).move_to([0.0, 0.60, 0.0])
        eq_sub1 = Text("(ผนัง 2 ข้าง ความหนา t ยาว L รับแรงดึงเท่ากัน)", font_size=18, color=COL_GRAY).move_to([0.0, -0.05, 0.0])

        self.hud(eq_head, eq_step1, eq_sub1)
        self.play(
            FadeIn(eq_head),
            FadeIn(eq_step1, shift=UP * 0.2),
            FadeIn(eq_sub1),
            run_time=3.0
        )
        self.wait(0.4)

        # Step 2: Cancel L on both sides -> Step 3: Rearrange for σ
        eq_step2 = Text("P · Di = 2 · t · σ", font_size=30).move_to([0.0, 0.60, 0.0])
        eq_final = Text("σ = P · Di / (2t)", font_size=36, color=COL_OK).move_to([0.0, -0.80, 0.0])
        box_final = SurroundingRectangle(eq_final, color=COL_OK, buff=0.18, corner_radius=0.1)

        cap_sigma = caption_top("σ = P · Di / (2t)")
        self.hud(cap_sigma, eq_step2, eq_final, box_final)

        self.play(
            ReplacementTransform(cap4, cap_sigma),
            ReplacementTransform(eq_step1, eq_step2),
            Create(box_final),
            FadeIn(eq_final, shift=UP * 0.2),
            run_time=2.8
        )
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 42.0–47.0: Burst Pressure — Pipe Expansion & Stress Limit
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(eq_head, eq_step2, eq_sub1, eq_final, box_final, cap_sigma)),
            run_time=0.8
        )

        cap5 = caption_top("Burst Pressure — ดันจนท่อแตก")
        self.hud(cap5)
        self.play(FadeIn(cap5, shift=UP * 0.4), run_time=0.8)

        # Camera back to 3D perspective to witness pipe expansion and color escalation
        self.move_camera(phi=65 * DEGREES, theta=-55 * DEGREES, run_time=0.6)

        pipe_burst = Cylinder(radius=1.55, height=L_pipe, resolution=(10, 10),
                              fill_color=COL_METAL, stroke_width=0).move_to([0.0, -0.75, 0.0])
        pipe_burst.set_opacity(0.85)

        p_display = Text("ความดัน P: 10 MPa → 76 MPa (ท่อขยายจนแตก)", font_size=18, color=COL_WARN).move_to([0.0, 1.85, 0.0])
        self.hud(p_display)

        burst_lbl = Text("ดันจน σ ถึงค่าความแข็งแรงดึง S ของวัสดุ → ท่อแตก!", font_size=18, color=COL_WARN).move_to([0.0, -2.40, 0.0])
        self.hud(burst_lbl)

        self.play(
            FadeIn(pipe_burst),
            FadeIn(p_display),
            run_time=0.6
        )
        # High-risk check (c): Pipe itself visibly changes color and scale!
        self.play(
            pipe_burst.animate.set_color(COL_WARN).scale(1.05),
            FadeIn(burst_lbl, shift=UP * 0.2),
            run_time=2.4
        )
        self.wait(0.4)

        # ----------------------------------------------------------------------
        # BEAT 47.0–50.8: Burst Pressure Formula (BP = 2tS / Di)
        # ----------------------------------------------------------------------
        eq_bp_head = Text("ที่จุดท่อแตก:  σ = S (Tensile Strength),  P = BP", font_size=22, color=WHITE).move_to([0.0, 0.65, 0.0])
        eq_bp = Text("BP = 2 · t · S / Di", font_size=36, color=COL_WARN).move_to([0.0, -0.15, 0.0])
        box_bp = SurroundingRectangle(eq_bp, color=COL_WARN, buff=0.18, corner_radius=0.1)

        cap_bp = caption_top("BP = 2tS / Di")
        self.hud(cap_bp, eq_bp_head, eq_bp, box_bp)

        self.play(
            FadeOut(p_display),
            FadeOut(burst_lbl),
            ReplacementTransform(cap5, cap_bp),
            FadeIn(eq_bp_head),
            FadeIn(eq_bp, shift=UP * 0.2),
            Create(box_bp),
            run_time=2.8
        )
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 50.8–54.0: Working Pressure & Safety Factor Concept
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(pipe_burst, eq_bp_head, eq_bp, box_bp, cap_bp)),
            run_time=0.8
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.4)

        cap6 = caption_top("Working Pressure — ใช้งานจริงต้องเผื่อ")
        self.hud(cap6)
        self.play(FadeIn(cap6, shift=UP * 0.4), run_time=0.8)

        formula_wp = Text("WP = BP / FS", font_size=32, color=COL_OK).move_to([0.0, 1.80, 0.0])
        box_wp = SurroundingRectangle(formula_wp, color=COL_OK, buff=0.15, corner_radius=0.1)
        sub_wp = Text("(Working Pressure = Burst Pressure / Factor of Safety)", font_size=16, color=COL_GRAY).move_to([0.0, 1.25, 0.0])

        self.hud(formula_wp, box_wp, sub_wp)
        self.play(
            FadeIn(formula_wp, shift=UP * 0.3),
            Create(box_wp),
            FadeIn(sub_wp),
            run_time=0.7
        )
        self.wait(1.7)

        # ----------------------------------------------------------------------
        # BEAT 54.0–59.0: Safety Factor (FS) Table
        # ----------------------------------------------------------------------
        fs_t_box = RoundedRectangle(corner_radius=0.12, width=7.2, height=1.9,
                                    color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        fs_row1 = Text("0 – 1,000 psi      →   FS = 8", font_size=18, color=WHITE).move_to([0.0, 0.38, 0.0])
        fs_row2 = Text("1,000 – 2,500 psi  →   FS = 6", font_size=18, color=WHITE).move_to([0.0, -0.15, 0.0])
        fs_row3 = Text("> 2,500 psi        →   FS = 4", font_size=18, color=COL_OK).move_to([0.0, -0.68, 0.0])

        fs_note = Text("ยิ่งความดันสูง ยิ่งต้องเผื่อน้อยลง (FS เล็กลง)\nเพื่อไม่ให้ท่อหนาเกินไป และผลิตด้วยความแม่นยำสูงกว่า",
                       font_size=15, color=COL_GRAY).move_to([0.0, -1.65, 0.0])

        self.hud(fs_t_box, fs_row1, fs_row2, fs_row3, fs_note)
        self.play(
            LaggedStart(
                FadeIn(fs_t_box),
                FadeIn(fs_row1, shift=UP * 0.15),
                FadeIn(fs_row2, shift=UP * 0.15),
                FadeIn(fs_row3, shift=UP * 0.15),
                lag_ratio=0.25
            ),
            FadeIn(fs_note),
            run_time=3.6
        )
        self.wait(1.4)

        # ----------------------------------------------------------------------
        # BEAT 59.0–63.8: Single Bar Meter (BP vs WP Visualization)
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(sub_wp, fs_t_box, fs_row1, fs_row2, fs_row3, fs_note)),
            run_time=0.6
        )

        meter_track = Rectangle(width=8.0, height=0.55, color=COL_METAL, stroke_width=1.5).move_to([0.0, -0.40, 0.0])
        meter_bp = Rectangle(width=8.0, height=0.55, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.35).set_stroke(width=0).move_to([0.0, -0.40, 0.0])
        meter_wp = Rectangle(width=2.0, height=0.55, color=COL_OK, fill_color=COL_OK).set_fill(COL_OK, 0.85).set_stroke(width=0).align_to(meter_track, LEFT)

        lbl_wp_bar = Text("WP (ใช้งาน 1/4)", font_size=16, color=COL_OK).next_to(meter_wp, UP, buff=0.15)
        lbl_bp_bar = Text("BP (แตก)", font_size=16, color=COL_WARN).next_to(meter_bp, RIGHT, buff=0.18)
        lbl_margin = Text("← เผื่อความปลอดภัย Safety Margin 3/4 →", font_size=14, color=COL_GRAY).move_to([0.90, -0.40, 0.0])

        self.hud(meter_track, meter_bp, meter_wp, lbl_wp_bar, lbl_bp_bar, lbl_margin)
        self.play(
            Create(meter_track),
            GrowFromEdge(meter_bp, LEFT),
            GrowFromEdge(meter_wp, LEFT),
            FadeIn(lbl_wp_bar),
            FadeIn(lbl_bp_bar),
            FadeIn(lbl_margin),
            run_time=3.2
        )
        self.wait(0.8)

        # ----------------------------------------------------------------------
        # BEAT 63.8–67.0: Worked Example (Given Parameters Panel)
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(formula_wp, box_wp, meter_track, meter_bp, meter_wp,
                           lbl_wp_bar, lbl_bp_bar, lbl_margin, cap6)),
            run_time=0.8
        )

        cap7 = caption_top("ตัวอย่าง: ท่อเหล็ก Di=20mm, t=2mm, S=380MPa")
        self.hud(cap7)
        self.play(FadeIn(cap7, shift=UP * 0.4), run_time=0.8)

        # Left box: Given problem specifications
        prob_box = RoundedRectangle(corner_radius=0.15, width=4.6, height=3.6,
                                    color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([-4.40, -0.30, 0.0])
        prob_head = Text("ข้อมูลกำหนด:", font_size=18, color=COL_OK).move_to([-4.40, 1.10, 0.0])
        prob_p1 = Text("• Di = 20 mm  (ID)", font_size=16, color=WHITE).move_to([-4.40, 0.55, 0.0])
        prob_p2 = Text("• t = 2 mm  (ความหนา)", font_size=16, color=WHITE).move_to([-4.40, 0.05, 0.0])
        prob_p3 = Text("• S = 380 MPa  (ความแข็งแรง)", font_size=16, color=WHITE).move_to([-4.40, -0.45, 0.0])
        prob_p4 = Text("(คำนวณจากสูตรสไลด์ น.6)", font_size=13, color=COL_GRAY).move_to([-4.40, -1.05, 0.0])

        prob_grp = VGroup(prob_box, prob_head, prob_p1, prob_p2, prob_p3, prob_p4)
        self.hud(prob_grp)
        self.play(FadeIn(prob_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(1.8)

        # ----------------------------------------------------------------------
        # BEAT 67.0–73.0: Step 1 — Burst Pressure Calculation & FS Selection
        # ----------------------------------------------------------------------
        calc_head1 = Text("ขั้นที่ 1: คำนวณ Burst Pressure (BP)", font_size=18, color=COL_WARN).move_to([1.80, 1.10, 0.0])
        bp_f1 = Text("BP = 2 · t · S / Di", font_size=20, color=COL_GRAY).move_to([1.80, 0.55, 0.0])
        bp_f2 = Text("= 2(2)(380) / 20", font_size=20, color=WHITE).move_to([1.80, 0.55, 0.0])
        bp_f3 = Text("= 76 MPa  (≈ 11,000 psi)", font_size=22, color=COL_WARN).move_to([1.80, 0.00, 0.0])

        self.hud(calc_head1, bp_f1, bp_f2, bp_f3)
        self.play(FadeIn(calc_head1), FadeIn(bp_f1), run_time=0.8)
        self.play(ReplacementTransform(bp_f1, bp_f2), run_time=1.0)
        self.play(FadeIn(bp_f3, shift=UP * 0.15), run_time=1.0)
        self.wait(0.2)

        fs_choose = Text("11,000 psi > 2,500 psi  →  เลือก FS = 4", font_size=18, color=COL_OK).move_to([1.80, -0.65, 0.0])
        self.hud(fs_choose)
        self.play(FadeIn(fs_choose, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(fs_choose, color=COL_OK), run_time=0.8)
        self.wait(1.4)

        # ----------------------------------------------------------------------
        # BEAT 73.0–76.8: Step 2 — Working Pressure Calculation
        # ----------------------------------------------------------------------
        calc_head2 = Text("ขั้นที่ 2: คำนวณ Working Pressure (WP)", font_size=18, color=COL_OK).move_to([1.80, 1.10, 0.0])
        wp_f1 = Text("WP = BP / FS = 76 / 4", font_size=20, color=WHITE).move_to([1.80, 0.50, 0.0])
        wp_f2 = Text("WP = 19 MPa", font_size=28, color=COL_OK).move_to([1.80, -0.05, 0.0])
        box_wp_res = SurroundingRectangle(wp_f2, color=COL_OK, buff=0.15, corner_radius=0.1)

        self.hud(calc_head2, wp_f1, wp_f2, box_wp_res)
        self.play(
            ReplacementTransform(calc_head1, calc_head2),
            ReplacementTransform(bp_f2, wp_f1),
            FadeOut(bp_f3),
            FadeOut(fs_choose),
            run_time=1.0
        )
        self.play(
            ReplacementTransform(wp_f1, wp_f2),
            Create(box_wp_res),
            run_time=1.2
        )
        self.wait(0.8)

        # ----------------------------------------------------------------------
        # BEAT 76.8–83.8: Exam Trap — Verify Selected FS Range
        # ----------------------------------------------------------------------
        cap8 = caption_top("⚠️ จุดที่คนพลาด — ต้องย้อนเช็ค FS ที่เลือก")
        self.hud(cap8)
        self.play(ReplacementTransform(cap7, cap8), run_time=0.8)

        chk1 = Text("แปลง WP กลับเป็น psi เพื่อตรวจเช็คช่วง:", font_size=16, color=COL_GRAY).move_to([1.80, -0.75, 0.0])
        chk2 = Text("19 MPa ≈ 2,760 psi > 2,500 psi  ✓", font_size=20, color=COL_OK).move_to([1.80, -1.25, 0.0])
        warn_note = Text("⚠️ ถ้า WP ตกไปอยู่ช่วง FS อื่น\nต้องเลือก FS ใหม่แล้วคำนวณ WP ซ้ำ", font_size=14, color=COL_WARN).move_to([1.80, -1.85, 0.0])

        self.hud(chk1, chk2, warn_note)
        self.play(
            FadeIn(chk1),
            FadeIn(chk2, shift=UP * 0.15),
            run_time=2.0
        )
        self.wait(1.0)
        self.play(FadeIn(warn_note, shift=UP * 0.2), run_time=0.6)
        self.wait(2.4)

        # ----------------------------------------------------------------------
        # BEAT 83.8–86.0: Summary Card
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(prob_grp, calc_head2, wp_f2, box_wp_res, chk1, chk2, warn_note, cap8)),
            run_time=0.8
        )

        sum_box = RoundedRectangle(corner_radius=0.15, width=11.4, height=3.8,
                                   color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.40, 0.0])
        sum_title = Text("สรุปความดันที่ท่อรับได้ (hydraulic06 น.6)", font_size=20, color=COL_OK).move_to([0.0, 1.10, 0.0])
        s1 = Text("1. ความเค้นดึงในผนังท่อ:   σ = P · Di / (2t)   (พื้นที่ฉาย = L × Di)", font_size=16, color=WHITE).move_to([0.0, 0.55, 0.0])
        s2 = Text("2. ความดันแตก (Burst Pressure):   BP = 2 · t · S / Di   (เมื่อ σ = S)", font_size=16, color=WHITE).move_to([0.0, 0.05, 0.0])
        s3 = Text("3. ความดันใช้งานจริง (Working Pressure):   WP = BP / FS", font_size=16, color=WHITE).move_to([0.0, -0.45, 0.0])
        s4 = Text("4. Safety Factor:  > 2,500 psi → FS=4  |  1,000–2,500 psi → FS=6  |  < 1,000 psi → FS=8", font_size=15, color=COL_WARN).move_to([0.0, -0.95, 0.0])
        s5 = Text("5. ต้องย้อนเช็คเสมอว่าค่า WP ที่ได้ ยังคงตกอยู่ในช่วง FS ที่เลือกจริง", font_size=15, color=COL_GRAY).move_to([0.0, -1.45, 0.0])

        sum_grp = VGroup(sum_box, sum_title, s1, s2, s3, s4, s5)
        self.hud(sum_grp)

        self.play(FadeIn(sum_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(1.4)

        # ----------------------------------------------------------------------
        # BEAT 86.0–91.0: Review Question Card & Outro
        # ----------------------------------------------------------------------
        self.play(FadeOut(sum_grp), run_time=0.6)

        q_box = RoundedRectangle(corner_radius=0.15, width=10.8, height=2.4,
                                 color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.45, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.30, 0.0])
        q_body = Text("ถ้าเพิ่มความหนาผนังท่อ t เป็น 2 เท่า โดยที่เส้นผ่านศูนย์กลาง Di เท่าเดิม\nความดันแตก (Burst Pressure) จะเปลี่ยนแปลงอย่างไร?",
                      font_size=16, color=WHITE).move_to([0.0, -0.20, 0.0])
        q_ans = Text("(คำตอบ: BP เพิ่มเป็น 2 เท่า เพราะ BP ∝ t ตามสูตร BP = 2tS / Di)",
                     font_size=15, color=COL_GRAY).move_to([0.0, -0.85, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)
        self.hud(q_grp)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)


# ==============================================================================
# SCENE 4: H6_04_SteelPipes (hydraulic06.pdf page 7)
# Duration: ~42 seconds | 2D SafeScene
# Pedagogical Focus: Pipe Schedule Number = Wall Thickness Rating
# AHA Moment: Same OD across schedules, but ID shrinks as wall thickness increases
# Connection: BP = 2tS / Di (from H6_03) yields ~1.51x higher BP for Sch 80 vs Sch 40
# ==============================================================================
class H6_04_SteelPipes(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–4.6: Title, Page Reference & Hook Question
        # ----------------------------------------------------------------------
        title_m = title("ท่อเหล็ก — Schedule Number")
        ref_m = page_ref("hydraulic06 น.7")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(ref_m), run_time=1.5)
        self.wait(0.5)

        hook_q = caption_top("ท่อ 2 นิ้วเหมือนกัน ทำไมน้ำหนัก/ราคาต่างกันได้ 4 แบบ?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 4.6–13.8: 4 Cross-Section Rings (Nominal 2" Pipe: Same OD, Shrinking ID)
        # ----------------------------------------------------------------------
        cap1 = caption_top("4 วงแหวนหน้าตัด — OD เท่ากันเป๊ะ (Nominal Size เดียวกัน)")
        self.play(FadeIn(cap1, shift=UP * 0.4), run_time=0.6)

        # Ring geometry parameters: Nominal 2" pipe (OD = 2.375")
        R_OD = 1.05
        # Inner radii proportional to real ID/OD from table:
        # Sch 40: ID = 2.067" -> R_ID = 1.05 * 2.067 / 2.375 = 0.9138
        # Sch 80: ID = 1.939" -> R_ID = 1.05 * 1.939 / 2.375 = 0.8572
        # Sch 160: ID = 1.689" -> R_ID = 1.05 * 1.689 / 2.375 = 0.7467
        # XXH: ID = 1.503" -> R_ID = 1.05 * 1.503 / 2.375 = 0.6645
        r_in_40  = R_OD * (2.067 / 2.375)
        r_in_80  = R_OD * (1.939 / 2.375)
        r_in_160 = R_OD * (1.689 / 2.375)
        r_in_xxh = R_OD * (1.503 / 2.375)

        x_coords = [-4.5, -1.5, 1.5, 4.5]
        y_ring = 0.35

        ring_40 = Annulus(inner_radius=r_in_40, outer_radius=R_OD).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2).move_to([x_coords[0], y_ring, 0])
        ring_80 = Annulus(inner_radius=r_in_80, outer_radius=R_OD).set_fill(COL_FIELD, 0.85).set_stroke(COL_FIELD, width=2).move_to([x_coords[1], y_ring, 0])
        ring_160 = Annulus(inner_radius=r_in_160, outer_radius=R_OD).set_fill(COL_CURR, 0.85).set_stroke(COL_CURR, width=2).move_to([x_coords[2], y_ring, 0])
        ring_xxh = Annulus(inner_radius=r_in_xxh, outer_radius=R_OD).set_fill(COL_WARN, 0.85).set_stroke(COL_WARN, width=2).move_to([x_coords[3], y_ring, 0])

        lbl_40 = VGroup(
            Text("Schedule 40", font_size=18, color=COL_METAL),
            Text("(Standard / STD)", font_size=13, color=COL_GRAY)
        ).arrange(DOWN, buff=0.1).move_to([x_coords[0], -1.35, 0])

        lbl_80 = VGroup(
            Text("Schedule 80", font_size=18, color=COL_FIELD),
            Text("(Extra Heavy / XH)", font_size=13, color=COL_GRAY)
        ).arrange(DOWN, buff=0.1).move_to([x_coords[1], -1.35, 0])

        lbl_160 = VGroup(
            Text("Schedule 160", font_size=18, color=COL_CURR),
            Text("(High Pressure)", font_size=13, color=COL_GRAY)
        ).arrange(DOWN, buff=0.1).move_to([x_coords[2], -1.35, 0])

        lbl_xxh = VGroup(
            Text("Double Extra Heavy", font_size=16, color=COL_WARN),
            Text("(XXH / XXS)", font_size=13, color=COL_GRAY)
        ).arrange(DOWN, buff=0.1).move_to([x_coords[3], -1.35, 0])

        ring_items = [
            VGroup(ring_40, lbl_40),
            VGroup(ring_80, lbl_80),
            VGroup(ring_160, lbl_160),
            VGroup(ring_xxh, lbl_xxh)
        ]

        self.play(
            LaggedStart(*[FadeIn(item, shift=UP * 0.2) for item in ring_items], lag_ratio=0.4),
            run_time=2.6
        )
        self.wait(0.8)

        # Highlight identical OD (9.0–10.4s)
        od_line_top = DashedLine(start=[-5.8, y_ring + R_OD, 0], end=[5.8, y_ring + R_OD, 0], color=COL_OK, stroke_width=2)
        od_line_bot = DashedLine(start=[-5.8, y_ring - R_OD, 0], end=[5.8, y_ring - R_OD, 0], color=COL_OK, stroke_width=2)
        lbl_od_same = Text("OD = 2.375 นิ้ว เท่ากันทุกวง (ขนาดระบุ 2 นิ้ว)", font_size=17, color=COL_OK).move_to([0.0, 1.90, 0])

        self.play(
            Create(od_line_top),
            Create(od_line_bot),
            FadeIn(lbl_od_same, shift=UP * 0.15),
            run_time=0.8
        )
        self.wait(0.6)

        # Highlight shrinking ID (10.4–13.0s)
        cap_id = caption_top("ID เล็กลงเรื่อยๆ — ยิ่ง Schedule สูง ผนังยิ่งหนา")

        id_items = []
        id_values_str = ['ID=2.067"', 'ID=1.939"', 'ID=1.689"', 'ID=1.503"']
        id_radii = [r_in_40, r_in_80, r_in_160, r_in_xxh]
        for i in range(4):
            val_txt = Text(id_values_str[i], font_size=14, color=WHITE).move_to([x_coords[i], y_ring, 0])
            w_half = val_txt.width / 2 + 0.05
            arr_l = Arrow(start=[x_coords[i] - w_half, y_ring, 0], end=[x_coords[i] - id_radii[i], y_ring, 0],
                          buff=0, color=COL_WARN, stroke_width=2, max_tip_length_to_length_ratio=0.35)
            arr_r = Arrow(start=[x_coords[i] + w_half, y_ring, 0], end=[x_coords[i] + id_radii[i], y_ring, 0],
                          buff=0, color=COL_WARN, stroke_width=2, max_tip_length_to_length_ratio=0.35)
            id_items.append(VGroup(val_txt, arr_l, arr_r))
        id_grp = VGroup(*id_items)

        self.play(
            ReplacementTransform(cap1, cap_id),
            FadeOut(od_line_top),
            FadeOut(od_line_bot),
            FadeOut(lbl_od_same),
            FadeIn(id_grp, shift=UP * 0.1),
            run_time=1.4
        )
        self.wait(1.2)

        # Clear beat 2
        self.play(
            FadeOut(VGroup(ring_40, ring_80, ring_160, ring_xxh, lbl_40, lbl_80, lbl_160, lbl_xxh, id_grp, cap_id)),
            run_time=0.8
        )

        # ----------------------------------------------------------------------
        # BEAT 13.8–24.8: Connection to H6_03 (BP = 2tS/Di) & Relative BP Ratio
        # ----------------------------------------------------------------------
        cap2 = caption_top("ย้อนกลับไปสูตร BP = 2tS/Di จากคลิปก่อน")
        self.play(FadeIn(cap2, shift=UP * 0.4), run_time=0.8)

        formula_bp = Text("BP = 2 · t · S / Di", font_size=24, color=COL_OK).move_to([0.0, 1.20, 0.0])
        formula_sub = Text("(ยิ่งความหนาผนัง t มาก ยิ่งรับความดันแตก BP ได้สูงขึ้น)", font_size=16, color=COL_GRAY).move_to([0.0, 0.65, 0.0])

        self.play(FadeIn(formula_bp, shift=UP * 0.2), FadeIn(formula_sub, shift=UP * 0.15), run_time=0.6)
        self.wait(1.8)

        # Wall thickness calculation (17.0–20.0s)
        t_head = Text("คำนวณความหนาผนัง t = (OD − ID) / 2  (สำหรับท่อ 2 นิ้ว, OD = 2.375 นิ้ว):", font_size=16, color=WHITE).move_to([0.0, 1.35, 0.0])
        t_40 = Text("• Sch 40:  t = (2.375 − 2.067) / 2 = 0.154 นิ้ว", font_size=17, color=COL_METAL).move_to([-3.2, 0.70, 0.0])
        t_80 = Text("• Sch 80:  t = (2.375 − 1.939) / 2 = 0.218 นิ้ว  (+41.6% หนาขึ้น)", font_size=17, color=COL_FIELD).move_to([-3.2, 0.15, 0.0])

        self.play(FadeOut(formula_sub), run_time=0.3)
        self.play(
            ReplacementTransform(formula_bp, t_head),
            FadeIn(t_40, shift=UP * 0.15),
            FadeIn(t_80, shift=UP * 0.15),
            run_time=2.5
        )
        self.wait(0.2)

        # BP ratio calculation & Bar Chart (20.0–24.0s)
        cap_ratio = caption_top("Sch 80 รับความดันได้มากกว่า Sch 40 ถึง ~1.51 เท่า (ที่ไซส์เดียวกัน)")

        calc_head = Text("อัตราส่วนความดันแตก (BP) วัสดุเดียวกัน (S เท่ากัน):", font_size=15, color=WHITE).move_to([-3.4, 1.35, 0.0])
        calc_r1 = Text("BP_80 / BP_40 = (t_80 / Di_80) / (t_40 / Di_40)", font_size=16, color=COL_OK).move_to([-3.4, 0.85, 0.0])
        calc_r2 = Text("= (0.218 / 1.939) / (0.154 / 2.067)", font_size=16, color=WHITE).move_to([-3.4, 0.35, 0.0])
        calc_r3 = Text("= 0.1124 / 0.0745", font_size=16, color=WHITE).move_to([-3.4, -0.15, 0.0])
        calc_res = Text("≈ 1.51 เท่า (+51%)", font_size=22, color=COL_OK).move_to([-3.4, -0.75, 0.0])
        box_res = SurroundingRectangle(calc_res, color=COL_OK, buff=0.12, corner_radius=0.1)
        calc_note = Text("*คำนวณต่อยอดจากสูตร H6_03 + ตารางสไลด์หน้า 7", font_size=12, color=COL_GRAY).move_to([-3.4, -1.35, 0.0])

        calc_grp = VGroup(calc_head, calc_r1, calc_r2, calc_r3, calc_res, box_res, calc_note)

        # Right Bar Chart (High-Risk Check b: EXACT ratio 1.0 : 1.509 = 1.51)
        y_base = -1.50
        chart_base = Line(start=[0.6, y_base, 0], end=[6.2, y_base, 0], color=COL_GRAY, stroke_width=2)
        chart_title = Text("ความดันแตกสัมพัทธ์ (Relative BP)", font_size=15, color=WHITE).move_to([3.4, 2.05, 0])

        h_bar40 = 2.000
        # Exact mathematical ratio from slide table data:
        # (t80/Di80) / (t40/Di40) = (0.218/1.939) / (0.154/2.067) = 1.50925
        h_bar80 = 2.000 * ((0.218 / 1.939) / (0.154 / 2.067))
        w_bar = 1.30

        x_bar40 = 2.00
        x_bar80 = 4.60

        bar40 = Rectangle(width=w_bar, height=h_bar40).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2).move_to([x_bar40, y_base + h_bar40 / 2, 0])
        bar80 = Rectangle(width=w_bar, height=h_bar80).set_fill(COL_FIELD, 0.85).set_stroke(COL_FIELD, width=2).move_to([x_bar80, y_base + h_bar80 / 2, 0])

        lbl_bar40_top = Text("1.00x", font_size=18, color=COL_METAL).move_to([x_bar40, y_base + h_bar40 + 0.25, 0])
        lbl_bar80_top = Text("1.51x", font_size=20, color=COL_OK).move_to([x_bar80, y_base + h_bar80 + 0.25, 0])

        lbl_bar40_bot = VGroup(
            Text("Sch 40", font_size=15, color=COL_METAL),
            Text("(มาตรฐาน)", font_size=12, color=COL_GRAY)
        ).arrange(DOWN, buff=0.08).move_to([x_bar40, y_base - 0.40, 0])

        lbl_bar80_bot = VGroup(
            Text("Sch 80", font_size=15, color=COL_FIELD),
            Text("(หนาพิเศษ)", font_size=12, color=COL_GRAY)
        ).arrange(DOWN, buff=0.08).move_to([x_bar80, y_base - 0.40, 0])

        chart_grp = VGroup(chart_base, chart_title, bar40, bar80, lbl_bar40_top, lbl_bar80_top, lbl_bar40_bot, lbl_bar80_bot)

        self.play(FadeOut(VGroup(t_head, t_40, t_80)), run_time=0.4)
        self.play(
            ReplacementTransform(cap2, cap_ratio),
            FadeIn(calc_grp, shift=UP * 0.2),
            Create(chart_base),
            FadeIn(chart_title),
            GrowFromEdge(bar40, DOWN),
            GrowFromEdge(bar80, DOWN),
            FadeIn(lbl_bar40_top, shift=UP * 0.1),
            FadeIn(lbl_bar80_top, shift=UP * 0.1),
            FadeIn(lbl_bar40_bot),
            FadeIn(lbl_bar80_bot),
            run_time=3.0
        )
        self.wait(0.6)

        # Clear beat 3
        self.play(
            FadeOut(calc_grp),
            FadeOut(chart_grp),
            FadeOut(cap_ratio),
            run_time=0.8
        )

        # ----------------------------------------------------------------------
        # BEAT 24.8–29.8: Double Extra Heavy vs Sch 40 Comparison
        # ----------------------------------------------------------------------
        cap3 = caption_top("Double Extra Heavy — ผนังหนาสุด รับความดันสูงสุด")
        self.play(FadeIn(cap3, shift=UP * 0.4), run_time=0.8)

        r_od_big = 1.35
        r_in_40_big  = r_od_big * (2.067 / 2.375)
        r_in_xxh_big = r_od_big * (1.503 / 2.375)

        ring_comp_40 = Annulus(inner_radius=r_in_40_big, outer_radius=r_od_big).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2).move_to([-3.0, 0.20, 0])
        ring_comp_xxh = Annulus(inner_radius=r_in_xxh_big, outer_radius=r_od_big).set_fill(COL_WARN, 0.85).set_stroke(COL_WARN, width=2).move_to([3.0, 0.20, 0])

        lbl_comp_40 = VGroup(
            Text("Schedule 40 (STD)", font_size=18, color=COL_METAL),
            Text("ความหนา t = 0.154 นิ้ว", font_size=15, color=WHITE),
            Text("ID = 2.067 นิ้ว (รูในกว้าง ไหลสะดวก)", font_size=14, color=COL_GRAY)
        ).arrange(DOWN, buff=0.10).move_to([-3.0, -1.80, 0])

        lbl_comp_xxh = VGroup(
            Text("Double Extra Heavy (XXH)", font_size=18, color=COL_WARN),
            Text("ความหนา t = 0.436 นิ้ว (หนาเกือบ 3 เท่า!)", font_size=15, color=COL_WARN),
            Text("ID = 1.503 นิ้ว (รูในแคบมาก รับแรงดันมหาศาล)", font_size=14, color=COL_GRAY)
        ).arrange(DOWN, buff=0.10).move_to([3.0, -1.80, 0])

        comp_top_note = Text("OD = 2.375 นิ้ว เท่ากันเป๊ะ แต่พื้นที่เนื้อเหล็กต่างกันอย่างสิ้นเชิง", font_size=16, color=COL_OK).move_to([0.0, 1.95, 0])

        self.play(
            FadeIn(ring_comp_40, shift=UP * 0.2),
            FadeIn(ring_comp_xxh, shift=UP * 0.2),
            FadeIn(lbl_comp_40, shift=UP * 0.15),
            FadeIn(lbl_comp_xxh, shift=UP * 0.15),
            FadeIn(comp_top_note),
            run_time=1.6
        )
        self.play(Indicate(ring_comp_xxh, color=COL_WARN), run_time=0.8)
        self.wait(1.0)

        # Clear beat 4
        self.play(
            FadeOut(VGroup(ring_comp_40, ring_comp_xxh, lbl_comp_40, lbl_comp_xxh, comp_top_note, cap3)),
            run_time=0.8
        )

        # ----------------------------------------------------------------------
        # BEAT 29.8–34.8: Schedule Number Misconception Card
        # ----------------------------------------------------------------------
        cap4 = caption_top("Schedule Number ไม่ใช่สูตรคำนวณ — เป็นรหัสมาตรฐาน")
        self.play(FadeIn(cap4, shift=UP * 0.4), run_time=0.8)

        card_box = RoundedRectangle(corner_radius=0.15, width=11.4, height=3.6,
                                    color=COL_GRAY, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.25, 0.0])
        card_head = Text("⚠️ ทำความเข้าใจ Schedule Number (ANSI / ASME B36.10M)", font_size=18, color=COL_WARN).move_to([0.0, 1.15, 0.0])
        card_l1 = Text("1. Schedule Number เป็นเพียง 'รหัสมาตรฐาน' ไม่ใช่ค่าที่นำไปคำนวณทางฟิสิกส์ตรงๆ", font_size=15, color=WHITE).move_to([0.0, 0.60, 0.0])
        card_l2 = Text("2. หลักจำง่ายๆ:  Schedule ยิ่งสูง = ผนังยิ่งหนา (t เพิ่ม) = รูในยิ่งแคบ (ID ลด)", font_size=15, color=COL_OK).move_to([0.0, 0.10, 0.0])
        card_l3 = Text("3. ท่อไซส์ระบุ (Nominal Size) เดียวกัน → จะมี 'OD เท่ากันเสมอ' ทุก Schedule", font_size=15, color=COL_FIELD).move_to([0.0, -0.40, 0.0])
        card_l4 = Text("4. ระวัง Head Loss: รูในแคบลงทำให้ความเร็วของไหล v สูงขึ้น เกิดความเสียดทานเพิ่ม", font_size=15, color=COL_WARN).move_to([0.0, -0.90, 0.0])
        card_l5 = Text("   (งานไฮดรอลิกจึงต้องเปิดตารางเช็คทั้งความทนแรงดันและอัตราการไหลควบคู่กัน)", font_size=13, color=COL_GRAY).move_to([0.0, -1.35, 0.0])

        card_grp = VGroup(card_box, card_head, card_l1, card_l2, card_l3, card_l4, card_l5)

        self.play(FadeIn(card_grp, shift=UP * 0.3), run_time=0.8)
        self.wait(2.6)

        self.play(FadeOut(card_grp), FadeOut(cap4), run_time=0.8)

        # ----------------------------------------------------------------------
        # BEAT 34.8–37.0: Summary Card
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(corner_radius=0.15, width=11.4, height=3.6,
                                   color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.25, 0.0])
        sum_title = Text("สรุปท่อเหล็กและ Schedule Number (hydraulic06 น.7)", font_size=19, color=COL_OK).move_to([0.0, 1.15, 0.0])
        s1 = Text("1. ท่อขนาดระบุ (Nominal Size) เดียวกัน → เส้นผ่านศูนย์กลางภายนอก (OD) เท่ากันทุกวง", font_size=15, color=WHITE).move_to([0.0, 0.60, 0.0])
        s2 = Text("2. Schedule สูงขึ้น (40 → 80 → 160 → XXH) → ผนังหนาขึ้น (t เพิ่ม) แต่รูในแคบลง (ID ลด)", font_size=15, color=WHITE).move_to([0.0, 0.10, 0.0])
        s3 = Text("3. เชื่อมสูตร H6_03: ท่อ 2 นิ้ว Sch 80 รับ Burst Pressure ได้ ~1.51 เท่าของ Sch 40", font_size=15, color=COL_OK).move_to([0.0, -0.40, 0.0])
        s4 = Text("4. ผนังหนาขึ้นรับความดันได้สูงขึ้น แต่ท่อหนักขึ้น แพงขึ้น และเกิด Head Loss เพิ่มขึ้น", font_size=15, color=COL_WARN).move_to([0.0, -0.90, 0.0])
        s5 = Text("(* อัตราส่วน 1.51 เท่าเป็นค่าคำนวณต่อยอดจากสูตร BP = 2tS/Di และตารางหน้า 7)", font_size=13, color=COL_GRAY).move_to([0.0, -1.35, 0.0])

        sum_grp = VGroup(sum_box, sum_title, s1, s2, s3, s4, s5)

        self.play(FadeIn(sum_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(sum_grp), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 37.0–42.0: Review Question Card & Outro
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(corner_radius=0.15, width=11.0, height=2.6,
                                 color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text("ท่อ Sch 160 มีความหนาผนังมากกว่า Sch 80 อีก (t เพิ่มขึ้น, ID ลดลง)\nคาดว่าความดันแตก (Burst Pressure) จะเปลี่ยนแปลงอย่างไรเทียบกับ Sch 80?",
                      font_size=15, color=WHITE).move_to([0.0, -0.05, 0.0])
        q_ans = Text("(คำตอบ: BP สูงขึ้นอีก เพราะตามสูตร BP = 2tS / Di ยิ่ง t มากขึ้น และ Di เล็กลง BP ก็ยิ่งสูง)",
                     font_size=14, color=COL_GRAY).move_to([0.0, -0.75, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.2)
        self.fade_out_all(run_time=0.8)



