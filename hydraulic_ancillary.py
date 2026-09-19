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
COL_BAD   = "#DC2626"   # Wrong/elastomer-fails contrast color (H6_19+)


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


# ==============================================================================
# SCENE 5: H6_05_PipeThreads (hydraulic06.pdf page 8)
# Duration: ~45.5 seconds | 2D SafeScene
# Pedagogical Focus: Tapered Pipe Threads (NPT vs NPTF) = Self-Sealing Mechanism
# AHA Moment: Metal-to-metal interference provides the actual seal, not PTFE tape;
# Dry-Seal (NPTF) eliminates spiral clearance by root-and-crest engagement
# ==============================================================================
class H6_05_PipeThreads(SafeScene):
    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–4.8: Title, Page Reference & Hook Question
        # ----------------------------------------------------------------------
        title_m = title("เกลียวท่อ — ซีลในตัว")
        ref_m = page_ref("hydraulic06 น.8")
        self.play(FadeIn(title_m, shift=UP * 0.4), FadeIn(ref_m), run_time=1.5)
        self.wait(0.5)

        hook_q = caption_top("เกลียวแค่ยึดไว้ ต้องมีปะเก็นถึงจะกันรั่วได้ไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(hook_q), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 4.8–9.8: Tapered Pipe & Fitting (Male vs Female Taper)
        # ----------------------------------------------------------------------
        cap1 = caption_top("เกลียวท่อเป็นเกลียว 'เรียว' (Tapered) — ไม่ใช่เกลียวขนาน")
        self.play(FadeIn(cap1, shift=UP * 0.4), run_time=0.8)

        # Helper to build male pipe
        def create_male_pipe():
            top_pts = [
                [-5.0, 0.85, 0], [-2.4, 0.85, 0],
                [-2.4, 1.35, 0],
                [-2.25, 1.10, 0], [-2.05, 1.32, 0],
                [-1.90, 1.07, 0], [-1.70, 1.29, 0],
                [-1.55, 1.04, 0], [-1.35, 1.26, 0],
                [-1.20, 1.01, 0], [-1.00, 1.23, 0],
                [-0.85, 0.98, 0], [-0.65, 1.20, 0],
                [-0.65, 0.85, 0]
            ]
            top_wall = Polygon(*top_pts, color=COL_METAL).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2)

            bot_pts = [[p[0], -p[1], 0] for p in top_pts]
            bot_wall = Polygon(*bot_pts, color=COL_METAL).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2)
            return VGroup(top_wall, bot_wall)

        # Helper to build female fitting
        def create_female_fitting():
            top_pts = [
                [0.5, 1.6, 0], [4.5, 1.6, 0],
                [4.5, 0.85, 0], [2.3, 0.85, 0],
                [2.3, 1.03, 0], [2.1, 1.22, 0],
                [1.9, 1.06, 0], [1.7, 1.25, 0],
                [1.5, 1.09, 0], [1.3, 1.28, 0],
                [1.1, 1.12, 0], [0.9, 1.31, 0],
                [0.7, 1.15, 0], [0.5, 1.37, 0]
            ]
            top_block = Polygon(*top_pts, color=COL_GRAY).set_fill("#334155", 0.95).set_stroke(COL_GRAY, width=2)

            bot_pts = [[p[0], -p[1], 0] for p in top_pts]
            bot_block = Polygon(*bot_pts, color=COL_GRAY).set_fill("#334155", 0.95).set_stroke(COL_GRAY, width=2)
            return VGroup(top_block, bot_block)

        male_pipe = create_male_pipe()
        female_fitting = create_female_fitting()

        taper_male_top = DashedLine(start=[-2.5, 1.37, 0], end=[-0.5, 1.18, 0], color=COL_WARN, stroke_width=2.5)
        taper_fem_top  = DashedLine(start=[0.4, 1.38, 0], end=[2.4, 1.21, 0], color=COL_WARN, stroke_width=2.5)
        lbl_taper = Text("มุมเรียว 1° 47' (Tapered)", font_size=15, color=COL_WARN).move_to([-1.5, 1.85, 0])

        lbl_male = Text("เกลียวตัวผู้ (ท่อเหล็ก)", font_size=16, color=COL_METAL).move_to([-3.0, -1.8, 0])
        lbl_fem  = Text("เกลียวตัวเมีย (ข้อต่อ/วาล์ว)", font_size=16, color=COL_GRAY).move_to([2.5, -1.8, 0])

        self.play(
            FadeIn(male_pipe, shift=RIGHT * 0.3),
            FadeIn(female_fitting, shift=LEFT * 0.3),
            FadeIn(lbl_male),
            FadeIn(lbl_fem),
            Create(taper_male_top),
            Create(taper_fem_top),
            FadeIn(lbl_taper, shift=UP * 0.1),
            run_time=1.8
        )
        self.wait(1.6)

        # ----------------------------------------------------------------------
        # BEAT 9.8–15.0: Threading In (Male moves into Female, Metal-to-Metal)
        # ----------------------------------------------------------------------
        cap2 = caption_top("ขันเข้าไป — เนื้อโลหะเบียดอัดกันแน่นขึ้นเรื่อยๆ")
        self.play(
            ReplacementTransform(cap1, cap2),
            FadeOut(taper_male_top),
            FadeOut(taper_fem_top),
            FadeOut(lbl_taper),
            FadeOut(lbl_male),
            FadeOut(lbl_fem),
            run_time=0.8
        )

        # Threading in: male_pipe shifts into female_fitting
        # Check a: 10.8s vs 12.5s distance visibly changes
        self.play(
            male_pipe.animate.shift(RIGHT * 1.5),
            run_time=3.4,
            rate_func=linear
        )
        self.wait(0.8)

        # ----------------------------------------------------------------------
        # BEAT 15.0–19.8: Zoom into Contact Zone (Interference Sealing)
        # ----------------------------------------------------------------------
        cap_zoom = caption_top("เนื้อโลหะถูกบีบอัด (Interference) — ซีลเกิดขึ้นเองโดยไม่ต้องพึ่งปะเก็น")
        top_assembly = VGroup(male_pipe[0], female_fitting[0])
        bot_assembly = VGroup(male_pipe[1], female_fitting[1])
        contact_pt = np.array([0.7, 1.2, 0])

        contact_ellipse = Ellipse(width=1.6, height=0.9, color=COL_WARN).move_to([0.7, 0.4, 0])
        interf_txt = Text("เนื้อโลหะเบียดอัดกันแน่น (Metal-to-Metal Interference)\nป้องกันน้ำมันไฮดรอลิกรั่วซึมโดยอัตโนมัติ", font_size=16, color=COL_OK).move_to([0.0, -1.8, 0])

        self.play(
            ReplacementTransform(cap2, cap_zoom),
            FadeOut(bot_assembly),
            top_assembly.animate.scale(2.2, about_point=contact_pt).shift(DOWN * 0.8),
            run_time=1.4
        )
        self.play(
            Create(contact_ellipse),
            FadeIn(interf_txt, shift=UP * 0.15),
            run_time=0.8
        )
        self.play(Indicate(contact_ellipse, color=COL_WARN), run_time=0.8)
        self.wait(1.0)

        # Zoom out
        self.play(
            FadeOut(contact_ellipse),
            FadeOut(interf_txt),
            top_assembly.animate.shift(UP * 0.8).scale(1 / 2.2, about_point=contact_pt),
            FadeIn(bot_assembly),
            run_time=0.8
        )
        self.play(FadeOut(male_pipe), FadeOut(female_fitting), FadeOut(cap_zoom), run_time=0.8)

        # ----------------------------------------------------------------------
        # BEAT 20.6–25.8: PTFE Tape Role (Helper, Not Primary Seal)
        # ----------------------------------------------------------------------
        cap3 = caption_top("เทปพันเกลียว / น้ำยาซีล = ตัวช่วยเสริม ไม่ใช่ตัวซีลหลัก")
        self.play(FadeIn(cap3, shift=UP * 0.4), run_time=0.8)

        pipe_body_tape = Polygon(
            [-5.0, 0.75, 0], [-2.0, 0.75, 0], [-2.0, 1.25, 0], [-5.0, 1.25, 0],
            color=COL_METAL
        ).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2)
        pipe_bot_tape = Polygon(
            [-5.0, -1.25, 0], [-2.0, -1.25, 0], [-2.0, -0.75, 0], [-5.0, -0.75, 0],
            color=COL_METAL
        ).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2)

        tape_box_top = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.7, color="#FFF59D", fill_color="#FFF9C4").set_fill("#FFF9C4", 0.9).move_to([-2.8, 1.0, 0])
        tape_box_bot = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.7, color="#FFF59D", fill_color="#FFF9C4").set_fill("#FFF9C4", 0.9).move_to([-2.8, -1.0, 0])
        tape_lbl = Text("เทป PTFE (เทปพันเกลียว)", font_size=14, color=WHITE).move_to([-2.8, -1.8, 0])
        tape_demo_grp = VGroup(pipe_body_tape, pipe_bot_tape, tape_box_top, tape_box_bot, tape_lbl)

        tape_card_box = RoundedRectangle(corner_radius=0.15, width=6.6, height=3.4, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([2.6, 0.0, 0])
        tc_head = Text("หน้าที่จริงของเทปพันเกลียว", font_size=17, color=COL_OK).move_to([2.6, 1.25, 0])
        tc_l1 = Text("• หน้าที่หลัก: หล่อลื่นเกลียว (Lubricant)\n  ช่วยให้ขันได้ลึกขึ้น ป้องกันเกลียวติดตาย (Galling)", font_size=14, color=WHITE).move_to([2.6, 0.60, 0])
        tc_l2 = Text("• หน้าที่รอง: ช่วยอุดรอยขูดขีดตามผิวโลหะ", font_size=14, color=COL_FIELD).move_to([2.6, -0.10, 0])
        tc_l3 = Text("⚠️ ไม่ใช่ตัวรับแรงดันหลัก!\n  ตัวซีลจริงคือเนื้อโลหะที่เบียดอัดกันแน่น", font_size=14, color=COL_WARN).move_to([2.6, -0.85, 0])
        tape_info_grp = VGroup(tape_card_box, tc_head, tc_l1, tc_l2, tc_l3)

        self.play(
            FadeIn(tape_demo_grp, shift=RIGHT * 0.2),
            FadeIn(tape_info_grp, shift=LEFT * 0.2),
            run_time=0.8
        )
        self.wait(2.8)

        self.play(FadeOut(tape_demo_grp), FadeOut(tape_info_grp), FadeOut(cap3), run_time=0.8)

        # ----------------------------------------------------------------------
        # BEAT 25.8–31.8: Standard Pipe Thread (NPT) Cutaway — Flank Contact
        # ----------------------------------------------------------------------
        cap4 = caption_top("1. Standard Pipe Thread (NPT) — ด้านข้าง Flank ชนกันก่อน")
        self.play(FadeIn(cap4, shift=UP * 0.4), run_time=0.8)

        p = 1.3
        h_tooth = 1.0
        g_gap = 0.20

        m_pts = [[-2.5, -1.0, 0]]
        for i in range(3):
            x_b = -1.95 + i * p
            m_pts.extend([
                [x_b, -0.2 + g_gap, 0],
                [x_b + p * 0.4, -0.2 + h_tooth - g_gap, 0],
                [x_b + p * 0.6, -0.2 + h_tooth - g_gap, 0],
                [x_b + p, -0.2 + g_gap, 0]
            ])
        m_pts.append([2.5, -1.0, 0])
        std_male = Polygon(*m_pts, color=COL_METAL).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2)

        f_pts = [[-2.5, 1.2, 0]]
        for i in range(3):
            x_b = -1.95 + i * p
            f_pts.extend([
                [x_b, 0.8 - g_gap, 0],
                [x_b + p * 0.4, 0.8 - h_tooth + g_gap, 0],
                [x_b + p * 0.6, 0.8 - h_tooth + g_gap, 0],
                [x_b + p, 0.8 - g_gap, 0]
            ])
        f_pts.append([2.5, 1.2, 0])
        std_female = Polygon(*f_pts, color=COL_GRAY).set_fill("#334155", 0.9).set_stroke(COL_GRAY, width=2)

        gap_polys = []
        for i in range(3):
            x_b = -1.95 + i * p
            g_top = Polygon(
                [x_b + p * 0.38, -0.2 + h_tooth - g_gap, 0],
                [x_b + p * 0.62, -0.2 + h_tooth - g_gap, 0],
                [x_b + p * 0.65, 0.8 - g_gap, 0],
                [x_b + p * 0.35, 0.8 - g_gap, 0],
                color=COL_WARN
            ).set_fill(COL_WARN, 0.95).set_stroke(COL_WARN, width=1)
            g_bot = Polygon(
                [x_b - 0.05, -0.2 + g_gap, 0],
                [x_b + 0.05, -0.2 + g_gap, 0],
                [x_b + p * 0.42, 0.8 - h_tooth + g_gap, 0],
                [x_b - p * 0.42, 0.8 - h_tooth + g_gap, 0],
                color=COL_WARN
            ).set_fill(COL_WARN, 0.95).set_stroke(COL_WARN, width=1)
            gap_polys.extend([g_top, g_bot])

        std_gaps = VGroup(*gap_polys)

        flank_lines = []
        for i in range(3):
            x_b = -1.95 + i * p
            flank_lines.append(Line([x_b + p * 0.1, 0.0, 0], [x_b + p * 0.35, 0.5, 0], color=COL_OK, stroke_width=4))
        flanks_grp = VGroup(*flank_lines)

        lbl_flank = Text("หน้าข้าง (Flank) สัมผัสกันก่อน", font_size=15, color=COL_OK).move_to([-3.4, 1.8, 0])
        arr_flank = Arrow(start=[-2.2, 1.8, 0], end=[-1.5, 0.35, 0], color=COL_OK, buff=0.1, stroke_width=2)

        lbl_gap = Text("มีช่องว่างเกลียว (Spiral Clearance)\nของไหลอาจรั่ววนออกตามร่องได้", font_size=14, color=COL_WARN).move_to([3.4, 1.8, 0])
        arr_gap = Arrow(start=[2.2, 1.8, 0], end=[0.8, 0.7, 0], color=COL_WARN, buff=0.1, stroke_width=2)

        std_note = Text("→ เกลียว NPT ทั่วไปจึงต้องพึ่งเทป PTFE หรือน้ำยาซีลช่วยอุดร่องวนนี้", font_size=15, color=WHITE).move_to([0.0, -1.8, 0])

        std_scene_grp = VGroup(std_male, std_female, std_gaps, flanks_grp, lbl_flank, arr_flank, lbl_gap, arr_gap, std_note)

        self.play(FadeIn(std_scene_grp, shift=UP * 0.3), run_time=1.8)
        self.play(Indicate(flanks_grp, color=COL_OK), run_time=0.6)
        self.play(Indicate(std_gaps, color=COL_WARN), run_time=0.8)
        self.wait(1.4)

        self.play(FadeOut(std_scene_grp), FadeOut(cap4), run_time=0.8)

        # ----------------------------------------------------------------------
        # BEAT 31.8–37.8: Dry-Seal Thread (NPTF) Cutaway — Root & Crest Contact
        # ----------------------------------------------------------------------
        cap5 = caption_top("2. Dry-Seal Thread (NPTF) — ยอดและโคนฟันชนกันก่อน ปิดช่องว่างหมด")
        self.play(FadeIn(cap5, shift=UP * 0.4), run_time=0.8)

        m_pts_ds = [[-2.5, -1.0, 0]]
        for i in range(3):
            x_b = -1.95 + i * p
            m_pts_ds.extend([
                [x_b, 0.0, 0],
                [x_b + p * 0.42, 0.8, 0],
                [x_b + p * 0.58, 0.8, 0],
                [x_b + p, 0.0, 0]
            ])
        m_pts_ds.append([2.5, -1.0, 0])
        ds_male = Polygon(*m_pts_ds, color=COL_METAL).set_fill(COL_METAL, 0.85).set_stroke(COL_METAL, width=2)

        f_pts_ds = [[-2.5, 1.2, 0]]
        for i in range(3):
            x_b = -1.95 + i * p
            f_pts_ds.extend([
                [x_b, 0.8, 0],
                [x_b + p * 0.42, 0.0, 0],
                [x_b + p * 0.58, 0.0, 0],
                [x_b + p, 0.8, 0]
            ])
        f_pts_ds.append([2.5, 1.2, 0])
        ds_female = Polygon(*f_pts_ds, color=COL_GRAY).set_fill("#334155", 0.9).set_stroke(COL_GRAY, width=2)

        crush_lines = []
        for i in range(3):
            x_b = -1.95 + i * p
            crush_lines.append(Line([x_b + p * 0.42, 0.8, 0], [x_b + p * 0.58, 0.8, 0], color=COL_OK, stroke_width=6))
            crush_lines.append(Line([x_b + p * 0.92, 0.0, 0], [x_b + p * 1.08, 0.0, 0], color=COL_OK, stroke_width=6))
        crush_grp = VGroup(*crush_lines)

        lbl_crush = Text("ยอดและโคนฟัน (Roots & Crests) บดอัดชนกันสนิท\nกำจัด Spiral Clearance จนหมดสิ้น!", font_size=15, color=COL_OK).move_to([0.0, 1.85, 0])

        ds_note = Text("→ เนื้อโลหะซีลกันสนิทโดยตรง (Metal-to-Metal Crush)\nไม่ต้องใช้เทปพันเกลียวเลย! เหมาะกับงานที่ไม่ต้องการให้มีเศษเทปหลุดปนเปื้อน", font_size=14, color=COL_WARN).move_to([0.0, -1.8, 0])

        ds_scene_grp = VGroup(ds_male, ds_female, crush_grp, lbl_crush, ds_note)

        self.play(FadeIn(ds_scene_grp, shift=UP * 0.3), run_time=1.8)
        self.play(Indicate(crush_grp, color=COL_OK), run_time=0.8)
        self.wait(1.8)

        self.play(FadeOut(ds_scene_grp), FadeOut(cap5), run_time=0.8)

        # ----------------------------------------------------------------------
        # BEAT 37.8–40.5: Summary Card
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(corner_radius=0.15, width=11.4, height=3.6,
                                   color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.25, 0.0])
        sum_title = Text("สรุปเกลียวท่อไฮดรอลิก (hydraulic06 น.8)", font_size=19, color=COL_OK).move_to([0.0, 1.15, 0.0])
        s1 = Text("1. เกลียวท่อ (NPT) เป็น 'เกลียวเรียว' (Tapered) มุม 1° 47' ขันแน่นแล้วเกิด Interference", font_size=15, color=WHITE).move_to([0.0, 0.60, 0.0])
        s2 = Text("2. ซีลด้วยเนื้อโลหะเบียดอัดกันเอง ไม่ต้องพึ่งปะเก็น (เทปพันเกลียวเป็นเพียงตัวช่วยเสริม)", font_size=15, color=WHITE).move_to([0.0, 0.10, 0.0])
        s3 = Text("3. เกลียวธรรมดา (NPT): ด้านข้าง (Flanks) ชนก่อน → เกิดช่องว่างวน (Spiral Clearance) ที่โคน/ยอด", font_size=15, color=COL_WARN).move_to([0.0, -0.40, 0.0])
        s4 = Text("4. เกลียว Dry-Seal (NPTF): ยอดและโคนฟันชนกันก่อน → บดอัดแนบสนิท ไม่ต้องใช้เทปเลย", font_size=15, color=COL_OK).move_to([0.0, -0.90, 0.0])
        s5 = Text("(* อ้างอิงสไลด์หน้า 8: Standard vs Dry-Seal Tapered Pipe Threads)", font_size=13, color=COL_GRAY).move_to([0.0, -1.35, 0.0])

        sum_grp = VGroup(sum_box, sum_title, s1, s2, s3, s4, s5)

        self.play(FadeIn(sum_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(1.9)
        self.play(FadeOut(sum_grp), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 40.5–45.5: Review Question Card & Outro
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(corner_radius=0.15, width=11.0, height=2.6,
                                 color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text("ทำไม Dry-Seal Thread (NPTF) จึงไม่ต้องพันเทป PTFE เลย\nในขณะที่ Standard Pipe Thread (NPT) ยังจำเป็นต้องพันเทปอยู่เสมอ?",
                      font_size=15, color=WHITE).move_to([0.0, -0.05, 0.0])
        q_ans = Text("(คำตอบ: เพราะ Dry-Seal มียอดและโคนฟันบดอัดชนกันสนิท กำจัด Spiral Clearance จนหมด\nส่วน Standard จะเหลือช่องว่างวนที่ยอดและโคนฟัน จึงต้องใช้เทปช่วยอุด)",
                     font_size=13, color=COL_GRAY).move_to([0.0, -0.75, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(2.8)

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)


# ==============================================================================
# H6_06_PipeFittings — คำศัพท์ข้อต่อท่อไฮดรอลิก 11 ชนิด (hydraulic06.pdf น.9)
# ==============================================================================

class H6_06_PipeFittings(SafeScene):
    """
    Fluid Power Control — W06 Hydraulic Ancillary Devices (hydraulic06.pdf)
    Scene: H6_06_PipeFittings (ข้อต่อท่อ — คำศัพท์พื้นฐาน 11 ชนิด)
    Lecture slide: hydraulic06.pdf page 9 ("Pipe Fittings")
    Duration target: ~38 seconds (thin richness: pure vocabulary flashcard)
    
    Verified facts from source slide:
    - 11 pipe fittings: Pipe Plug, Nipple, Tee, 90° Elbow, Union,
      Reducing Bushing, Reducing Coupling, Straight Coupling, Cap,
      Street Elbow, Globe Valve.
    - Pedagogical purpose: distinguish fittings by their recognizable shape
      and single-line engineering purpose.
    """
    def clear_stage(self, keep=(), run_time=0.6):
        """Fade out active stage objects while preserving persistent title badges."""
        targets = [m for m in self.mobjects if m not in keep and m not in getattr(self, "keep_mobs", ())]
        if targets:
            self.play(FadeOut(Group(*targets)), run_time=run_time)

    # --------------------------------------------------------------------------
    # Fitting Icon Generators (2D Distinct Graphical Shapes)
    # --------------------------------------------------------------------------
    def make_plug_icon(self):
        head = Rectangle(width=0.68, height=0.20, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.95).move_to([0, 0.15, 0])
        plug = Polygon([-0.24, 0.05, 0], [0.24, 0.05, 0], [0.16, -0.34, 0], [-0.16, -0.34, 0],
                       color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.5)
        socket = Square(side_length=0.10, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([0, 0.15, 0])
        t1 = Line([-0.21, -0.06, 0], [0.21, -0.06, 0], color=COL_GRAY, stroke_width=1.5)
        t2 = Line([-0.19, -0.16, 0], [0.19, -0.16, 0], color=COL_GRAY, stroke_width=1.5)
        t3 = Line([-0.17, -0.26, 0], [0.17, -0.26, 0], color=COL_GRAY, stroke_width=1.5)
        return VGroup(head, plug, socket, t1, t2, t3)

    def make_nipple_icon(self):
        th_l = Rectangle(width=0.34, height=0.38, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([-0.29, 0, 0])
        th_r = Rectangle(width=0.34, height=0.38, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([0.29, 0, 0])
        hex_nut = Rectangle(width=0.22, height=0.54, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.95).move_to([0, 0, 0])
        l_ribs = VGroup(*[Line([-0.39 + i * 0.08, -0.19, 0], [-0.39 + i * 0.08, 0.19, 0], color=COL_GRAY, stroke_width=1.5) for i in range(3)])
        r_ribs = VGroup(*[Line([0.21 + i * 0.08, -0.19, 0], [0.21 + i * 0.08, 0.19, 0], color=COL_GRAY, stroke_width=1.5) for i in range(3)])
        return VGroup(th_l, th_r, hex_nut, l_ribs, r_ribs)

    def make_tee_icon(self):
        h_body = Rectangle(width=0.92, height=0.36, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.5).move_to([0, -0.08, 0])
        v_body = Rectangle(width=0.36, height=0.40, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.5).move_to([0, 0.16, 0])
        c_l = Rectangle(width=0.08, height=0.46, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9).move_to([-0.46, -0.08, 0])
        c_r = Rectangle(width=0.08, height=0.46, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9).move_to([0.46, -0.08, 0])
        c_t = Rectangle(width=0.46, height=0.08, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9).move_to([0, 0.36, 0])
        t_flow = VGroup(
            Line([-0.36, -0.08, 0], [0.36, -0.08, 0], color=COL_OK, stroke_width=2),
            Line([0, -0.08, 0], [0, 0.30, 0], color=COL_OK, stroke_width=2)
        )
        return VGroup(h_body, v_body, c_l, c_r, c_t, t_flow)

    def make_elbow_icon(self):
        h_part = Rectangle(width=0.48, height=0.36, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.5).move_to([-0.11, -0.11, 0])
        v_part = Rectangle(width=0.36, height=0.48, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.5).move_to([0.11, 0.11, 0])
        corner = Square(side_length=0.36, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.5).move_to([0.11, -0.11, 0])
        c_in = Rectangle(width=0.08, height=0.46, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9).move_to([-0.35, -0.11, 0])
        c_out = Rectangle(width=0.46, height=0.08, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9).move_to([0.11, 0.35, 0])
        flow_arc = Arc(radius=0.20, start_angle=-PI, angle=PI/2, color=COL_OK, stroke_width=2).move_to([0.02, -0.02, 0])
        return VGroup(h_part, v_part, corner, c_in, c_out, flow_arc)

    def make_union_icon(self):
        p_l = Rectangle(width=0.30, height=0.38, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([-0.26, 0, 0])
        p_r = Rectangle(width=0.30, height=0.38, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([0.26, 0, 0])
        u_nut = Rectangle(width=0.28, height=0.58, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.85).move_to([0, 0, 0])
        div_l = Line([-0.05, -0.29, 0], [-0.05, 0.29, 0], color=COL_BG_BOX, stroke_width=2)
        div_r = Line([0.05, -0.29, 0], [0.05, 0.29, 0], color=COL_BG_BOX, stroke_width=2)
        return VGroup(p_l, p_r, u_nut, div_l, div_r)

    def make_cap_icon(self):
        dome = RoundedRectangle(corner_radius=0.12, width=0.58, height=0.46, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.65).move_to([0.05, 0, 0])
        collar = Rectangle(width=0.09, height=0.54, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.95).move_to([-0.24, 0, 0])
        cavity = Rectangle(width=0.22, height=0.32, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([-0.13, 0, 0])
        stop_line = Line([0.06, -0.18, 0], [0.06, 0.18, 0], color=COL_WARN, stroke_width=3)
        return VGroup(dome, collar, cavity, stop_line)

    def make_bushing_icon(self):
        hex_shoulder = Rectangle(width=0.20, height=0.68, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.95).move_to([-0.26, 0, 0])
        male_body = Rectangle(width=0.44, height=0.52, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.5).move_to([0.06, 0, 0])
        inner_bore = Rectangle(width=0.58, height=0.28, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([0, 0, 0])
        ribs = VGroup(*[Line([-0.08 + i * 0.08, -0.26, 0], [-0.08 + i * 0.08, 0.26, 0], color=COL_GRAY, stroke_width=1.5) for i in range(3)])
        return VGroup(hex_shoulder, male_body, inner_bore, ribs)

    def make_red_coupling_icon(self):
        l_sleeve = Rectangle(width=0.30, height=0.60, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.6).move_to([-0.28, 0, 0])
        taper = Polygon([-0.13, 0.30, 0], [0.13, 0.19, 0], [0.13, -0.19, 0], [-0.13, -0.30, 0],
                        color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.6)
        r_sleeve = Rectangle(width=0.30, height=0.38, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.6).move_to([0.28, 0, 0])
        c_l = Rectangle(width=0.08, height=0.68, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.95).move_to([-0.43, 0, 0])
        c_r = Rectangle(width=0.08, height=0.46, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.95).move_to([0.43, 0, 0])
        return VGroup(l_sleeve, taper, r_sleeve, c_l, c_r)

    def make_str_coupling_icon(self):
        sleeve = Rectangle(width=0.82, height=0.48, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.55).move_to([0, 0, 0])
        c_l = Rectangle(width=0.08, height=0.58, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.95).move_to([-0.41, 0, 0])
        c_r = Rectangle(width=0.08, height=0.58, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.95).move_to([0.41, 0, 0])
        center_stop = Line([0, -0.24, 0], [0, 0.24, 0], color=COL_OK, stroke_width=3)
        return VGroup(sleeve, c_l, c_r, center_stop)

    def make_street_elbow_icon(self):
        h_part = Rectangle(width=0.42, height=0.36, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.5).move_to([-0.09, -0.11, 0])
        v_part = Rectangle(width=0.36, height=0.42, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.5).move_to([0.11, 0.09, 0])
        corner = Square(side_length=0.36, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.5).move_to([0.11, -0.11, 0])
        f_collar = Rectangle(width=0.46, height=0.09, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.95).move_to([0.11, 0.35, 0])
        m_spigot = Rectangle(width=0.28, height=0.30, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.4).move_to([-0.41, -0.11, 0])
        m_ribs = VGroup(*[Line([-0.48 + i * 0.07, -0.26, 0], [-0.48 + i * 0.07, 0.04, 0], color=COL_WARN, stroke_width=1.5) for i in range(3)])
        return VGroup(h_part, v_part, corner, f_collar, m_spigot, m_ribs)

    def make_globe_valve_icon(self):
        body = Circle(radius=0.26, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.35).move_to([0, -0.09, 0])
        fl_l = Rectangle(width=0.16, height=0.32, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.85).move_to([-0.35, -0.09, 0])
        fl_r = Rectangle(width=0.16, height=0.32, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.85).move_to([0.35, -0.09, 0])
        stem = Line([0, 0.17, 0], [0, 0.45, 0], color=COL_METAL, stroke_width=3.5)
        wheel = Ellipse(width=0.48, height=0.13, color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.85).move_to([0, 0.45, 0])
        baffle = Arc(radius=0.16, start_angle=-PI/3, angle=2*PI/3, color=COL_WARN, stroke_width=2.5).move_to([0, -0.09, 0])
        return VGroup(body, fl_l, fl_r, stem, wheel, baffle)

    def construct(self):
        # ----------------------------------------------------------------------
        # SETUP PERSISTENT BADGES (0.0–1.5s)
        # ----------------------------------------------------------------------
        title_mob = title("ข้อต่อท่อ — คำศัพท์พื้นฐาน")
        ref_mob = page_ref("hydraulic06 น.9")
        self.keep_mobs = (title_mob, ref_mob)

        self.play(
            FadeIn(title_mob, shift=UP * 0.4),
            FadeIn(ref_mob),
            run_time=1.5
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–6.5: 6 Most Common Pipe Fittings (6 ไอคอนเจอบ่อย)
        # ----------------------------------------------------------------------
        cap1 = caption_top("6 ชนิดที่เจอบ่อยที่สุด")
        self.play(FadeIn(cap1, shift=UP * 0.3), run_time=0.8)

        # 6 Cards: Top row (3) and Bottom row (3)
        # Coordinates: x in [-4.4, 0.0, 4.4], y in [1.05, -1.15]
        box_w, box_h = 3.8, 1.95
        xs = [-4.4, 0.0, 4.4]
        y_top, y_bot = 1.05, -1.15

        # Item 1: Pipe Plug
        icon_plug = self.make_plug_icon().move_to([xs[0], y_top + 0.35, 0])
        box1 = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[0], y_top, 0])
        t1_en = Text("Pipe Plug", font_size=15, color=WHITE).move_to([xs[0], y_top - 0.30, 0])
        t1_th = Text("ปลั๊กอุดท่อ (อุดรูเกลียวใน)", font_size=12, color=COL_CURR).move_to([xs[0], y_top - 0.60, 0])
        card1 = VGroup(box1, icon_plug, t1_en, t1_th)

        # Item 2: Nipple
        icon_nipple = self.make_nipple_icon().move_to([xs[1], y_top + 0.35, 0])
        box2 = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[1], y_top, 0])
        t2_en = Text("Nipple", font_size=15, color=WHITE).move_to([xs[1], y_top - 0.30, 0])
        t2_th = Text("นิปเปิ้ล (เกลียวนอก 2 ด้าน)", font_size=12, color=COL_CURR).move_to([xs[1], y_top - 0.60, 0])
        card2 = VGroup(box2, icon_nipple, t2_en, t2_th)

        # Item 3: Tee
        icon_tee = self.make_tee_icon().move_to([xs[2], y_top + 0.35, 0])
        box3 = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[2], y_top, 0])
        t3_en = Text("Tee", font_size=15, color=WHITE).move_to([xs[2], y_top - 0.30, 0])
        t3_th = Text("สามทาง (แยกการไหล)", font_size=12, color=COL_CURR).move_to([xs[2], y_top - 0.60, 0])
        card3 = VGroup(box3, icon_tee, t3_en, t3_th)

        # Item 4: 90° Elbow
        icon_elbow = self.make_elbow_icon().move_to([xs[0], y_bot + 0.35, 0])
        box4 = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[0], y_bot, 0])
        t4_en = Text("90° Elbow", font_size=15, color=WHITE).move_to([xs[0], y_bot - 0.30, 0])
        t4_th = Text("ข้องอ 90° (เปลี่ยนทิศ)", font_size=12, color=COL_CURR).move_to([xs[0], y_bot - 0.60, 0])
        card4 = VGroup(box4, icon_elbow, t4_en, t4_th)

        # Item 5: Union
        icon_union = self.make_union_icon().move_to([xs[1], y_bot + 0.35, 0])
        box5 = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[1], y_bot, 0])
        t5_en = Text("Union", font_size=15, color=WHITE).move_to([xs[1], y_bot - 0.30, 0])
        t5_th = Text("ยูเนียน (ถอดแยกได้อิสระ)", font_size=12, color=COL_CURR).move_to([xs[1], y_bot - 0.60, 0])
        card5 = VGroup(box5, icon_union, t5_en, t5_th)

        # Item 6: Cap
        icon_cap = self.make_cap_icon().move_to([xs[2], y_bot + 0.35, 0])
        box6 = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h,
                                color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[2], y_bot, 0])
        t6_en = Text("Cap", font_size=15, color=WHITE).move_to([xs[2], y_bot - 0.30, 0])
        t6_th = Text("ฝาครอบ (ปิดปลายเกลียวนอก)", font_size=12, color=COL_CURR).move_to([xs[2], y_bot - 0.60, 0])
        card6 = VGroup(box6, icon_cap, t6_en, t6_th)

        cards6 = [card1, card2, card3, card4, card5, card6]

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards6], lag_ratio=0.25),
            run_time=3.2
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 6.5–15.5: Sequential Highlight & Single-Line Function (6 รายการ)
        # ----------------------------------------------------------------------
        desc_box = RoundedRectangle(corner_radius=0.08, width=11.6, height=0.52,
                                    color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -2.65, 0])

        d1 = Text("Pipe Plug: อุดรูเกลียวหรือช่องต่อที่ไม่ใช้งาน เพื่อป้องกันน้ำมันรั่วไหล", font_size=14, color=COL_WARN).move_to([0, -2.65, 0])
        self.play(Indicate(icon_plug, color=COL_WARN), FadeIn(desc_box), FadeIn(d1), run_time=0.7)
        self.wait(0.8)

        d2 = Text("Nipple: ข้อต่อเกลียวนอกสองข้าง สำหรับเชื่อมต่อระยะสั้นระหว่างอุปกรณ์", font_size=14, color=COL_WARN).move_to([0, -2.65, 0])
        self.play(Indicate(icon_nipple, color=COL_WARN), ReplacementTransform(d1, d2), run_time=0.6)
        self.wait(0.9)

        d3 = Text("Tee: ข้อต่อ 3 ทาง ใช้แยกเส้นทางน้ำมันจากท่อหลักออกเป็น 2 ทิศทาง", font_size=14, color=COL_WARN).move_to([0, -2.65, 0])
        self.play(Indicate(icon_tee, color=COL_WARN), ReplacementTransform(d2, d3), run_time=0.6)
        self.wait(0.9)

        d4 = Text("90° Elbow: ข้อศอกเปลี่ยนทิศทางการไหล 90° (มีมุม 45° และ 60° ด้วย)", font_size=14, color=COL_WARN).move_to([0, -2.65, 0])
        self.play(Indicate(icon_elbow, color=COL_WARN), ReplacementTransform(d3, d4), run_time=0.6)
        self.wait(0.9)

        d5 = Text("Union: ข้อต่อยูเนียน ถอดประกอบซ่อมบำรุงได้สะดวก โดยไม่ต้องหมุนท่อทั้งเส้น", font_size=14, color=COL_WARN).move_to([0, -2.65, 0])
        self.play(Indicate(icon_union, color=COL_WARN), ReplacementTransform(d4, d5), run_time=0.6)
        self.wait(0.9)

        d6 = Text("Cap: ฝาครอบเกลียวใน ใช้ปิดผนึกปลายท่อด้านนอกให้สนิท", font_size=14, color=COL_WARN).move_to([0, -2.65, 0])
        self.play(Indicate(icon_cap, color=COL_WARN), ReplacementTransform(d5, d6), run_time=0.6)
        self.wait(0.9)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 16.3–24.8: Reducing & Coupling Group (กลุ่มเปลี่ยนขนาดและต่อตรง)
        # ----------------------------------------------------------------------
        cap2 = caption_top("กลุ่มเปลี่ยนขนาด/ต่อท่อตรง")
        self.play(FadeIn(cap2, shift=UP * 0.3), run_time=0.8)

        card_w2, card_h2 = 3.8, 2.4
        y_c2 = 0.15

        # Card 7: Reducing Bushing
        icon_bushing = self.make_bushing_icon().move_to([xs[0], y_c2 + 0.45, 0])
        box7 = RoundedRectangle(corner_radius=0.12, width=card_w2, height=card_h2,
                                color=COL_FIELD, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[0], y_c2, 0])
        t7_en = Text("Reducing Bushing", font_size=15, color=WHITE).move_to([xs[0], y_c2 - 0.25, 0])
        t7_th = Text("ปลอกลด (เกลียวนอก-ใน)", font_size=13, color=COL_FIELD).move_to([xs[0], y_c2 - 0.55, 0])
        t7_tag = Text("เกลียวนอกใหญ่ — เกลียวในเล็ก", font_size=11, color=COL_GRAY).move_to([xs[0], y_c2 - 0.85, 0])
        card7 = VGroup(box7, icon_bushing, t7_en, t7_th, t7_tag)

        # Card 8: Reducing Coupling
        icon_red_coup = self.make_red_coupling_icon().move_to([xs[1], y_c2 + 0.45, 0])
        box8 = RoundedRectangle(corner_radius=0.12, width=card_w2, height=card_h2,
                                color=COL_FIELD, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[1], y_c2, 0])
        t8_en = Text("Reducing Coupling", font_size=15, color=WHITE).move_to([xs[1], y_c2 - 0.25, 0])
        t8_th = Text("ข้อต่อลด (เกลียวใน 2 ด้าน)", font_size=13, color=COL_FIELD).move_to([xs[1], y_c2 - 0.55, 0])
        t8_tag = Text("เชื่อมท่อ 2 เส้นขนาดต่างกัน", font_size=11, color=COL_GRAY).move_to([xs[1], y_c2 - 0.85, 0])
        card8 = VGroup(box8, icon_red_coup, t8_en, t8_th, t8_tag)

        # Card 9: Straight Coupling
        icon_str_coup = self.make_str_coupling_icon().move_to([xs[2], y_c2 + 0.45, 0])
        box9 = RoundedRectangle(corner_radius=0.12, width=card_w2, height=card_h2,
                                color=COL_FIELD, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs[2], y_c2, 0])
        t9_en = Text("Straight Coupling", font_size=15, color=WHITE).move_to([xs[2], y_c2 - 0.25, 0])
        t9_th = Text("ข้อต่อตรง (เกลียวใน 2 ด้าน)", font_size=13, color=COL_FIELD).move_to([xs[2], y_c2 - 0.55, 0])
        t9_tag = Text("เชื่อมท่อไซส์เดียวกันเป็นเส้นยาว", font_size=11, color=COL_GRAY).move_to([xs[2], y_c2 - 0.85, 0])
        card9 = VGroup(box9, icon_str_coup, t9_en, t9_th, t9_tag)

        cards3 = [card7, card8, card9]

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards3], lag_ratio=0.3),
            run_time=1.8
        )
        self.wait(1.5)

        # Highlight 3 items
        desc_box2 = RoundedRectangle(corner_radius=0.08, width=11.6, height=0.52,
                                     color=COL_FIELD, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -2.2, 0])

        d7 = Text("Bushing: ปลอกลด เกลียวนอกใหญ่-เกลียวในเล็ก ประหยัดพื้นที่ติดตั้ง", font_size=14, color=COL_FIELD).move_to([0, -2.2, 0])
        self.play(Indicate(icon_bushing, color=COL_FIELD), FadeIn(desc_box2), FadeIn(d7), run_time=0.5)
        self.wait(0.7)

        d8 = Text("Reducing Coupling: ข้อต่อลดเกลียวใน ใช้เชื่อมท่อ 2 เส้นที่มีขนาดต่างกัน", font_size=14, color=COL_FIELD).move_to([0, -2.2, 0])
        self.play(Indicate(icon_red_coup, color=COL_FIELD), ReplacementTransform(d7, d8), run_time=0.5)
        self.wait(0.7)

        d9 = Text("Straight Coupling: ข้อต่อตรงเกลียวใน ใช้ต่อท่อขนาดเดียวกันเป็นเส้นยาว", font_size=14, color=COL_FIELD).move_to([0, -2.2, 0])
        self.play(Indicate(icon_str_coup, color=COL_FIELD), ReplacementTransform(d8, d9), run_time=0.5)
        self.wait(0.7)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 24.8–29.8: Street Elbow & Globe Valve (ข้องอนอก-ใน และโกลบวาล์ว)
        # ----------------------------------------------------------------------
        cap3 = caption_top("Street Elbow และ Globe Valve")
        self.play(FadeIn(cap3, shift=UP * 0.3), run_time=0.8)

        card_w3, card_h3 = 5.2, 2.5
        xs3 = [-3.2, 3.2]
        y_c3 = 0.15

        # Card 10: Street Elbow
        icon_street = self.make_street_elbow_icon().move_to([xs3[0], y_c3 + 0.45, 0])
        box10 = RoundedRectangle(corner_radius=0.12, width=card_w3, height=card_h3,
                                 color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs3[0], y_c3, 0])
        t10_en = Text("Street Elbow", font_size=16, color=WHITE).move_to([xs3[0], y_c3 - 0.25, 0])
        t10_th = Text("ข้องอนอก-ใน (เกลียวนอก 1 ข้าง, เกลียวใน 1 ข้าง)", font_size=12, color=COL_CURR).move_to([xs3[0], y_c3 - 0.55, 0])
        t10_tag = Text("ขันตรงเข้าอุปกรณ์ได้ทันที — ประหยัดนิปเปิ้ล", font_size=11, color=COL_GRAY).move_to([xs3[0], y_c3 - 0.85, 0])
        card10 = VGroup(box10, icon_street, t10_en, t10_th, t10_tag)

        # Card 11: Globe Valve
        icon_globe = self.make_globe_valve_icon().move_to([xs3[1], y_c3 + 0.45, 0])
        box11 = RoundedRectangle(corner_radius=0.12, width=card_w3, height=card_h3,
                                 color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.90).move_to([xs3[1], y_c3, 0])
        t11_en = Text("Globe Valve", font_size=16, color=WHITE).move_to([xs3[1], y_c3 - 0.25, 0])
        t11_th = Text("โกลบวาล์ว (วาล์วควบคุมการไหล)", font_size=12, color=COL_CURR).move_to([xs3[1], y_c3 - 0.55, 0])
        t11_tag = Text("ทางเดินคดเคี้ยว — เหมาะสำหรับปรับหรี่ (Throttling)", font_size=11, color=COL_GRAY).move_to([xs3[1], y_c3 - 0.85, 0])
        card11 = VGroup(box11, icon_globe, t11_en, t11_th, t11_tag)

        self.play(FadeIn(card10, shift=UP * 0.2), FadeIn(card11, shift=UP * 0.2), run_time=1.0)
        self.wait(0.8)

        desc_box3 = RoundedRectangle(corner_radius=0.08, width=11.6, height=0.52,
                                     color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -2.2, 0])

        d10 = Text("Street Elbow: มีเกลียวนอก 1 ข้าง เกลียวใน 1 ข้าง ขันตรงเข้าอุปกรณ์ได้โดยไม่ต้องใช้ Nipple", font_size=14, color=COL_CURR).move_to([0, -2.2, 0])
        self.play(Indicate(icon_street, color=COL_CURR), FadeIn(desc_box3), FadeIn(d10), run_time=0.6)
        self.wait(0.9)

        d11 = Text("Globe Valve: วาล์วแบบโกลบ ออกแบบช่องไหลคดเคี้ยว เหมาะสำหรับปรับหรี่อัตราไหล (Throttling)", font_size=14, color=COL_CURR).move_to([0, -2.2, 0])
        self.play(Indicate(icon_globe, color=COL_CURR), ReplacementTransform(d10, d11), run_time=0.6)
        self.wait(0.9)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 29.8–33.0: Summary Table (ตารางสรุป 11 ชนิด)
        # ----------------------------------------------------------------------
        table_box = RoundedRectangle(corner_radius=0.15, width=12.2, height=4.7,
                                     color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.15, 0])

        head_col1 = Text("ชนิดข้อต่อ (Pipe Fitting)", font_size=13, color=COL_OK).move_to([-3.6, 1.88, 0])
        head_col2 = Text("หน้าที่หลัก / ลักษณะการใช้งาน (Function)", font_size=13, color=COL_OK).move_to([1.8, 1.88, 0])
        h_sep = Line([-5.8, 1.68, 0], [5.8, 1.68, 0], color=COL_OK, stroke_width=1.5)

        items_summary = [
            ("Pipe Plug (ปลั๊กอุด)", "อุดรูเกลียวใน หรือพอร์ตอุปกรณ์ที่ไม่ใช้งาน"),
            ("Nipple (นิปเปิ้ล)", "ต่อเชื่อมระยะสั้นระหว่างอุปกรณ์ (เกลียวนอก 2 ด้าน)"),
            ("Tee (สามทาง)", "แยกเส้นทางการไหลจาก 1 ทางออกเป็น 2 ทิศทาง"),
            ("90° Elbow (ข้องอ 90°)", "เปลี่ยนทิศทางการเดินท่อ 90° (มี 45° และ 60° ด้วย)"),
            ("Union (ยูเนียน)", "ถอดประกอบซ่อมบำรุงได้สะดวก โดยไม่ต้องหมุนท่อทั้งเส้น"),
            ("Cap (ฝาครอบ)", "ปิดผนึกปลายท่อด้านนอกให้สนิท"),
            ("Reducing Bushing (ปลอกลด)", "ลดขนาดเกลียว (เกลียวนอกใหญ่ - เกลียวในเล็ก ประหยัดที่)"),
            ("Reducing Coupling (ข้อต่อลด)", "เชื่อมต่อท่อ 2 เส้นที่มีขนาดต่างกัน (เกลียวใน 2 ด้าน)"),
            ("Straight Coupling (ข้อต่อตรง)", "เชื่อมต่อท่อขนาดเดียวกันเป็นเส้นยาว (เกลียวใน 2 ด้าน)"),
            ("Street Elbow (ข้องอนอก-ใน)", "ข้องอที่มีเกลียวนอก 1 ข้าง เกลียวใน 1 ข้าง (ประหยัดนิปเปิ้ล)"),
            ("Globe Valve (โกลบวาล์ว)", "ควบคุมเปิด-ปิด และปรับหรี่อัตราการไหล (Throttling)")
        ]

        row_mobs = []
        y_start = 1.48
        dy = 0.36
        for i, (name_txt, func_txt) in enumerate(items_summary):
            y_r = y_start - i * dy
            t_name = Text(f"{i+1}. {name_txt}", font_size=12, color=WHITE).move_to([-3.6, y_r, 0])
            t_func = Text(func_txt, font_size=12, color=COL_GRAY).move_to([1.8, y_r, 0])
            row_mobs.extend([t_name, t_func])

        summary_table = VGroup(table_box, head_col1, head_col2, h_sep, *row_mobs)

        self.play(FadeIn(summary_table, shift=UP * 0.4), run_time=0.8)
        self.wait(2.4)

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 33.0–37.0: Review Question Card
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(corner_radius=0.15, width=11.2, height=2.6,
                                 color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text("ต้องการถอดข้อต่อออกบ่อยๆ เพื่อซ่อมบำรุง โดยไม่หมุนท่อทั้งเส้น\nควรเลือกใช้ข้อต่อชนิดใด?",
                      font_size=15, color=WHITE).move_to([0.0, 0.0, 0.0])
        q_ans = Text("(คำตอบ: Union — มีปลอกเกลียวหมุนขันแยกอิสระได้ โดยท่อทั้งสองข้างอยู่นิ่ง)",
                     font_size=13, color=COL_GRAY).move_to([0.0, -0.65, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        # ----------------------------------------------------------------------
        # BEAT 37.0–38.0: Outro & Fade Out
        # ----------------------------------------------------------------------
        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)


# ==============================================================================
# Scene: H6_07_SteelTubeSizes (ตารางไซส์ท่อเหล็กมาตรฐาน และการเชื่อมโยงสู่ของจริง)
# Lecture slides: hydraulic06.pdf page 10 ("Steel Tube Sizes")
# Duration: ~33s
# Pedagogical Objective:
# - Connect theoretical sizing (H6_02: D_suction ≈ 23.0 mm at Q=30 L/min)
#   to real commercial standards: Table row OD=28 mm, Wall=2.5 mm -> ID=23.0 mm.
# - Understand why a single OD has multiple wall thicknesses: outer diameter is
#   fixed for standard fittings while wall thickness varies with Working Pressure.
# - Distinguish between Imperial (inches) and Metric (mm) tubing standards.
# - Richness: Thin (clean reference table presentation, 2D SafeScene).
# ==============================================================================

class H6_07_SteelTubeSizes(SafeScene):
    def clear_stage(self, keep=(), run_time=0.6):
        """Fade out active stage objects while preserving persistent title badges."""
        targets = [m for m in self.mobjects if m not in keep and m not in getattr(self, "keep_mobs", ())]
        if targets:
            self.play(FadeOut(Group(*targets)), run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # SETUP PERSISTENT BADGES (0.0–1.5s)
        # ----------------------------------------------------------------------
        title_mob = title("ตารางไซส์ท่อเหล็ก")
        page_ref_mob = page_ref("hydraulic06 น.10")
        self.keep_mobs = (title_mob, page_ref_mob)

        self.play(
            FadeIn(title_mob, shift=UP * 0.4),
            FadeIn(page_ref_mob),
            run_time=1.0
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.0: Hook Question — Callback to H6_02 Suction Pipe
        # ----------------------------------------------------------------------
        hook_q = caption_top("จำได้ไหม H6_02 คำนวณ D ท่อดูด ≈ 23.0 mm — จะไปหาซื้อไซส์ไหนจริง?", color=COL_GRAY)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(hook_q), run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 5.0–15.0: Metric Table Excerpt (OD 20-30 mm) & Exact Match Highlight
        # ----------------------------------------------------------------------
        cap1 = caption_top("ตารางไซส์ท่อ (Steel Tube) หน่วย mm")
        partial_note = Text("(แสดงเฉพาะช่วง OD 20–30 mm จากตารางมาตรฐานหน้า 10)", font_size=12, color=COL_GRAY).move_to([0, 2.25, 0])
        self.play(FadeIn(cap1, shift=UP * 0.3), FadeIn(partial_note), run_time=0.8)

        # Table Container Box (width=9.8, height=3.8, center at y=-0.15)
        table_box = RoundedRectangle(
            corner_radius=0.12, width=9.8, height=3.8,
            color=COL_METAL, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.92).move_to([0, -0.15, 0])

        col_xs = [-2.8, 0.0, 2.8]
        h_y = 1.35
        h_od = Text("OD ท่อ (mm)", font_size=13, color=COL_OK).move_to([col_xs[0], h_y, 0])
        h_wall = Text("ความหนาผนัง (mm)", font_size=13, color=COL_OK).move_to([col_xs[1], h_y, 0])
        h_id = Text("ID ท่อ (mm)", font_size=13, color=COL_OK).move_to([col_xs[2], h_y, 0])
        h_div = Line([-4.5, 1.15, 0], [4.5, 1.15, 0], color=COL_METAL, stroke_width=1.5)

        # Real data rows from hydraulic06.pdf page 10 (OD 20-30mm)
        raw_rows = [
            (20, 2.0, 16.0),
            (20, 2.5, 15.0),
            (22, 1.5, 19.0),
            (25, 3.0, 19.0),
            (28, 2.0, 24.0),
            (28, 2.5, 23.0),  # Target match row!
            (30, 3.0, 24.0)
        ]

        row_groups = []
        target_row_idx = 5
        target_row_grp = None

        y_top_row = 0.92
        dy = 0.38
        for i, (od, wall, tid) in enumerate(raw_rows):
            cur_y = y_top_row - i * dy
            t_od = Text(f"{od}", font_size=13, color=WHITE).move_to([col_xs[0], cur_y, 0])
            t_wall = Text(f"{wall:.1f}", font_size=13, color=WHITE).move_to([col_xs[1], cur_y, 0])
            t_id = Text(f"{tid:.0f}" if tid.is_integer() else f"{tid:.1f}", font_size=13, color=WHITE).move_to([col_xs[2], cur_y, 0])
            r_grp = VGroup(t_od, t_wall, t_id)
            if i == target_row_idx:
                target_row_grp = r_grp
            row_groups.append(r_grp)

        # Target highlight background bar
        highlight_bar = RoundedRectangle(
            corner_radius=0.06, width=9.2, height=0.34,
            color=COL_WARN, fill_color=COL_WARN
        ).set_fill(COL_WARN, 0.25).set_stroke(COL_WARN, 1.5).move_to([0, y_top_row - target_row_idx * dy, 0])

        table_mobs = VGroup(table_box, h_od, h_wall, h_id, h_div, *row_groups)

        self.play(FadeIn(table_mobs, shift=UP * 0.3), run_time=1.0)
        self.wait(3.2)

        # 10.0–10.8s: Indicate target row (OD=28, Wall=2.5, ID=23)
        self.play(
            FadeIn(highlight_bar),
            Indicate(target_row_grp, color=COL_WARN, scale_factor=1.06),
            run_time=0.8
        )

        # 10.8–14.5s: Match banner callout
        match_box = RoundedRectangle(
            corner_radius=0.10, width=11.4, height=0.68,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0, -2.60, 0])
        match_txt = Text(
            "OD = 28 mm, Wall = 2.5 mm → ID = 23 mm (ตรงกับท่อดูดที่คำนวณใน H6_02 พอดี!)",
            font_size=13, color=COL_OK
        ).move_to([0, -2.60, 0])
        match_grp = VGroup(match_box, match_txt)

        self.play(FadeIn(match_grp, shift=UP * 0.25), run_time=0.8)
        self.wait(2.9)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 15.0–20.8: Same OD, Multiple Wall Thicknesses (ความหนาผนังกับความดัน)
        # ----------------------------------------------------------------------
        cap2 = caption_top("ทำไมต้องมีหลายความหนาในไซส์เดียวกัน?")
        sub2 = Text(
            "OD เท่ากัน (20 mm) เพื่อต่อกับข้อต่อขนาดเดียวกัน — ความหนาเพิ่มขึ้นเพื่อรับแรงดันสูงขึ้น",
            font_size=12, color=COL_GRAY
        ).move_to([0, 2.25, 0])
        self.play(FadeIn(cap2, shift=UP * 0.3), FadeIn(sub2), run_time=0.8)

        # 3 Cards for OD=20 mm (Wall=1.5, 2.0, 3.0 from slide)
        c_xs = [-4.0, 0.0, 4.0]
        c_y = -0.25
        card_w, card_h = 3.6, 3.3

        cards_od20 = []
        od20_data = [
            ("Wall = 1.5 mm", "ID = 17.0 mm", "แรงดันปานกลาง (Standard)", COL_FIELD, 1.5, 0.55),
            ("Wall = 2.0 mm", "ID = 16.0 mm", "แรงดันสูง (High Pressure)", COL_CURR, 2.0, 0.45),
            ("Wall = 3.0 mm", "ID = 14.0 mm", "แรงดันสูงพิเศษ (Heavy Duty)", COL_WARN, 3.0, 0.32)
        ]

        for idx, (w_str, id_str, duty_str, col_theme, wall_val, inner_r) in enumerate(od20_data):
            x_pos = c_xs[idx]
            bx = RoundedRectangle(
                corner_radius=0.12, width=card_w, height=card_h,
                color=col_theme, fill_color=COL_BG_BOX
            ).set_fill(COL_BG_BOX, 0.90).move_to([x_pos, c_y, 0])

            # Cross section graphic: fixed OD outer ring, variable ID inner bore
            outer_ring = Circle(radius=0.55, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.70).move_to([x_pos, c_y + 0.52, 0])
            inner_hole = Circle(radius=inner_r * 0.75, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([x_pos, c_y + 0.52, 0])
            dim_od = Text("OD 20 mm", font_size=11, color=COL_GRAY).move_to([x_pos, c_y + 1.22, 0])
            tube_gfx = VGroup(dim_od, outer_ring, inner_hole)

            t_w = Text(w_str, font_size=14, color=col_theme).move_to([x_pos, c_y - 0.28, 0])
            t_id = Text(id_str, font_size=13, color=WHITE).move_to([x_pos, c_y - 0.62, 0])
            t_duty = Text(duty_str, font_size=11, color=COL_GRAY).move_to([x_pos, c_y - 0.98, 0])

            cd = VGroup(bx, tube_gfx, t_w, t_id, t_duty)
            cards_od20.append(cd)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cards_od20], lag_ratio=0.2),
            run_time=1.0
        )
        self.wait(3.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 20.8–25.8: Imperial (Inch) vs Metric (mm) Standards
        # ----------------------------------------------------------------------
        cap3 = caption_top("มีทั้งมาตรฐานหน่วยนิ้ว (Inch) และ มิลลิเมตร (mm)")
        sub3 = Text(
            "ตารางหน้า 10 มี 2 มาตรฐาน: นิ้ว (US / SAE) และ mm (ISO) — ห้ามใช้สลับกัน",
            font_size=12, color=COL_GRAY
        ).move_to([0, 2.25, 0])
        self.play(FadeIn(cap3, shift=UP * 0.3), FadeIn(sub3), run_time=0.8)

        # Side by side cards
        card_w3, card_h3 = 5.8, 3.4
        xs3 = [-3.2, 3.2]
        y3 = -0.30

        # Left: Inch Table (from top table in slide 10)
        box_in = RoundedRectangle(
            corner_radius=0.12, width=card_w3, height=card_h3,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.90).move_to([xs3[0], y3, 0])
        head_in = Text("หน่วยนิ้ว (Fractional Inch)", font_size=13, color=COL_FIELD).move_to([xs3[0], y3 + 1.32, 0])
        col_in = Text("OD (in.)    Wall (in.)    ID (in.)", font_size=11, color=COL_GRAY).move_to([xs3[0], y3 + 0.95, 0])
        div_in = Line([-5.8, y3 + 0.76, 0], [-0.6, y3 + 0.76, 0], color=COL_FIELD, stroke_width=1.2)

        rows_in_txt = [
            ("1/4", "0.035", "0.180"),
            ("3/8", "0.049", "0.277"),
            ("1/2", "0.049", "0.402"),
            ("3/4", "0.065", "0.620"),
            ("1", "0.065", "0.870")
        ]
        in_mobs = []
        for idx, (od_i, w_i, id_i) in enumerate(rows_in_txt):
            r_y = y3 + 0.50 - idx * 0.32
            row_t = Text(f"{od_i:<6}      {w_i:<7}      {id_i:<6}", font_size=11, color=WHITE).move_to([xs3[0], r_y, 0])
            in_mobs.append(row_t)

        card_inch = VGroup(box_in, head_in, col_in, div_in, *in_mobs)

        # Right: Metric Table (from bottom table in slide 10)
        box_mm = RoundedRectangle(
            corner_radius=0.12, width=card_w3, height=card_h3,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.90).move_to([xs3[1], y3, 0])
        head_mm = Text("หน่วยมิลลิเมตร (Metric mm)", font_size=13, color=COL_OK).move_to([xs3[1], y3 + 1.32, 0])
        col_mm = Text("OD (mm)    Wall (mm)    ID (mm)", font_size=11, color=COL_GRAY).move_to([xs3[1], y3 + 0.95, 0])
        div_mm = Line([0.6, y3 + 0.76, 0], [5.8, y3 + 0.76, 0], color=COL_OK, stroke_width=1.2)

        rows_mm_txt = [
            ("6", "1.0", "4.0"),
            ("10", "1.5", "7.0"),
            ("12", "1.5", "9.0"),
            ("20", "2.0", "16.0"),
            ("28", "2.5", "23.0")
        ]
        mm_mobs = []
        for idx, (od_m, w_m, id_m) in enumerate(rows_mm_txt):
            r_y = y3 + 0.50 - idx * 0.32
            row_t = Text(f"{od_m:<6}      {w_m:<7}      {id_m:<6}", font_size=11, color=WHITE).move_to([xs3[1], r_y, 0])
            mm_mobs.append(row_t)

        card_mm = VGroup(box_mm, head_mm, col_mm, div_mm, *mm_mobs)

        self.play(FadeIn(card_inch, shift=UP * 0.25), FadeIn(card_mm, shift=UP * 0.25), run_time=1.0)
        self.wait(2.4)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 25.8–28.0: Summary Card (การ์ดสรุป 3 ข้อ)
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(
            corner_radius=0.15, width=11.4, height=3.5,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.25, 0])

        s_head = Text("สรุปสำคัญ: การเลือกขนาดท่อเหล็ก (Steel Tube Sizes)", font_size=16, color=COL_OK).move_to([0, 1.15, 0])
        s1 = Text("1. ค่าที่คำนวณจากสูตร (Q = A·v) ต้องนำมาเทียบกับตารางไซส์มาตรฐานที่มีจำหน่ายจริง", font_size=13, color=WHITE).move_to([0, 0.55, 0])
        s2 = Text("2. OD เดียวกันมีหลายความหนา — เลือกความหนาผนังตาม Working Pressure (สูตร σ = P·Di/2t)", font_size=13, color=WHITE).move_to([0, 0.05, 0])
        s3 = Text("3. มาตรฐานมีทั้งระบบนิ้ว (SAE) และมิลลิเมตร (ISO) — ห้ามใช้สลับกันเพราะเกลียวและขนาดต่างกัน", font_size=13, color=WHITE).move_to([0, -0.45, 0])
        s4 = Text("(เช่น ท่อดูด Q=30 L/min: คำนวณได้ D≈23 mm เลือกท่อมาตรฐาน OD=28 mm, Wall=2.5 mm, ID=23 mm)", font_size=12, color=COL_CURR).move_to([0, -0.95, 0])

        sum_grp = VGroup(sum_box, s_head, s1, s2, s3, s4)

        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(1.4)

        self.clear_stage(run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 28.0–33.0: Review Question Card
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(
            corner_radius=0.15, width=11.2, height=2.6,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text(
            "ถ้าคำนวณ D ท่อจ่าย ≈ 10.2 mm จาก H6_02 ควรมองหาแถวไหนในตารางนี้?\n(ใบ้: ดูช่วง OD ใกล้เคียง 12–15 mm)",
            font_size=14, color=WHITE
        ).move_to([0.0, 0.0, 0.0])
        q_ans = Text(
            "(ในตารางหน้า 10: ท่อ OD 12 mm Wall 1.0 mm ได้ ID = 10.0 mm หรือ OD 15 mm Wall 2.0 mm ได้ ID = 11.0 mm)",
            font_size=12, color=COL_GRAY
        ).move_to([0.0, -0.65, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)


# ==============================================================================
# Scene: H6_08_TubeFittings (ข้อต่อท่อ Tube: Flare Fitting & Compression Fitting)
# Lecture slides: hydraulic06.pdf page 11 ("Tube Fittings")
# Duration: ~38s
# Pedagogical Objective:
# - Explain why thin-walled tubes (1-3 mm wall from H6_07) cannot use cut threads:
#   thread cutting removes too much wall thickness, risking explosive burst.
# - Reveal Mechanism 1 (Flare Fitting): 37° flared tube end clamped between
#   conical nose and nut shoulder (metal-to-metal seal without cutting tube).
# - Reveal Mechanism 2 (Compression Fitting): Straight tube with separate
#   ferrule ring crimping radially into tube OD during nut tightening.
# - Explicit contrast with H6_05 (Pipe Thread): same metal-to-metal sealing goal,
#   completely different mechanical principle (no wall weakening).
# ==============================================================================

class H6_08_TubeFittings(SafeScene):
    def clear_stage(self, keep=(), run_time=0.6):
        """Fade out active stage objects while preserving persistent title badges."""
        targets = [m for m in self.mobjects if m not in keep and m not in getattr(self, "keep_mobs", ())]
        if targets:
            self.play(FadeOut(Group(*targets)), run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # SETUP PERSISTENT BADGES (0.0–1.5s)
        # ----------------------------------------------------------------------
        title_mob = title("ข้อต่อท่อทองแดง/สแตนเลส (Tube Fittings)")
        page_ref_mob = page_ref("hydraulic06 น.11")
        self.keep_mobs = (title_mob, page_ref_mob)

        self.play(
            FadeIn(title_mob, shift=UP * 0.4),
            FadeIn(page_ref_mob),
            run_time=1.0
        )
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.2: Hook Question — Callback to H6_07 Thin Wall
        # ----------------------------------------------------------------------
        hook_q = caption_top("Tube ผนังบางกว่า Pipe มาก (H6_07) — ตัดเกลียวเข้าไปได้ไหม?", color=COL_GRAY)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(hook_q), run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 5.2–10.8: Thread Cut Hazard on Thin-Walled Tube
        # ----------------------------------------------------------------------
        cap1 = caption_top("ตัดเกลียวเข้าผนังบาง = ผนังที่เหลือบางเกินไปจนพังง่าย")
        sub1 = Text(
            "ผนัง Tube หนาเพียง 1–3 mm (H6_07) — การต๊าปเกลียวจะกินเนื้อท่อจนเสี่ยงต่อการระเบิดแตก",
            font_size=12, color=COL_GRAY
        ).move_to([0, 2.25, 0])
        self.play(FadeIn(cap1, shift=UP * 0.3), FadeIn(sub1), run_time=0.8)

        # Container box
        box_hazard = RoundedRectangle(
            corner_radius=0.12, width=11.6, height=3.5,
            color=COL_METAL, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.92).move_to([0, -0.20, 0])

        # Left Panel: Pipe (Thick Wall, Safe)
        p_x = -3.2
        pipe_box = RoundedRectangle(corner_radius=0.08, width=5.2, height=3.0, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.5).move_to([p_x, -0.20, 0])
        p_head = Text("Pipe (ท่อเหล็กผนังหนา — H6_05)", font_size=13, color=COL_OK).move_to([p_x, 1.05, 0])

        # Graphic of thick pipe wall with thread
        pipe_outer = Rectangle(width=3.6, height=1.1, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.4).move_to([p_x, 0.15, 0])
        pipe_inner = Rectangle(width=3.6, height=0.45, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([p_x, 0.15, 0])
        # Thread teeth cutting into outer top
        teeth_pipe = VGroup(*[
            Polygon([-1.4 + i*0.35, 0.70, 0], [-1.22 + i*0.35, 0.48, 0], [-1.05 + i*0.35, 0.70, 0],
                    color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0)
            for i in range(7)
        ]).shift(RIGHT * p_x)
        p_stat = Text("ความหนาผนังคงเหลือ: หนาพอรับแรงดันได้สบาย", font_size=11, color=COL_OK).move_to([p_x, -0.65, 0])
        p_tag = Text("✓ ใช้เกลียว NPT ซีลได้ปลอดภัย", font_size=11, color=WHITE).move_to([p_x, -0.95, 0])
        grp_pipe = VGroup(pipe_box, p_head, pipe_outer, pipe_inner, teeth_pipe, p_stat, p_tag)

        # Right Panel: Tube (Thin Wall, Hazard)
        t_x = 3.2
        tube_box = RoundedRectangle(corner_radius=0.08, width=5.2, height=3.0, color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.5).move_to([t_x, -0.20, 0])
        t_head = Text("Tube (ท่อผนังบาง 1–3 mm — H6_07)", font_size=13, color=COL_WARN).move_to([t_x, 1.05, 0])

        # Graphic of thin tube wall with thread cut
        tube_outer = Rectangle(width=3.6, height=0.9, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.4).move_to([t_x, 0.15, 0])
        tube_inner = Rectangle(width=3.6, height=0.65, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([t_x, 0.15, 0])
        # Thread teeth cutting almost through the thin wall!
        teeth_tube = VGroup(*[
            Polygon([-1.4 + i*0.35, 0.60, 0], [-1.22 + i*0.35, 0.35, 0], [-1.05 + i*0.35, 0.60, 0],
                    color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.95)
            for i in range(7)
        ]).shift(RIGHT * t_x)
        t_stat = Text("ร่องเกลือกินลึก: ผนังที่เหลือบางเกินไป!", font_size=11, color=COL_WARN).move_to([t_x, -0.65, 0])
        t_tag = Text("✗ เสี่ยงต่อการปริแตกเมื่อเจอแรงดันสูง", font_size=11, color=WHITE).move_to([t_x, -0.95, 0])
        grp_tube = VGroup(tube_box, t_head, tube_outer, tube_inner, teeth_tube, t_stat, t_tag)

        hazard_stage = VGroup(box_hazard, grp_pipe, grp_tube)

        self.play(FadeIn(hazard_stage, shift=UP * 0.3), run_time=1.0)
        self.play(Indicate(teeth_tube, color=COL_WARN, scale_factor=1.1), run_time=0.8)
        self.wait(1.8)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 10.8–16.8: Solution 1 — Flare Fitting (37° Flared End)
        # ----------------------------------------------------------------------
        cap2 = caption_top("ทางแก้ 1: Flare Fitting (บานปลายท่อ 37°)")
        sub2 = Text(
            "ปลายท่อบานออกเป็นกรวย 37° แล้วขันอัดเข้ากับที่นั่งเรียว — ซีลโลหะชนโลหะ ไม่ตัดเนื้อท่อเลย",
            font_size=12, color=COL_GRAY
        ).move_to([0, 2.25, 0])
        self.play(FadeIn(cap2, shift=UP * 0.3), FadeIn(sub2), run_time=0.8)

        # Flare Diagram Box
        box_flare = RoundedRectangle(
            corner_radius=0.12, width=11.6, height=3.5,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.92).move_to([0, -0.15, 0])

        # 1. Fitting Body with 37° male cone nose
        body_block = Rectangle(width=2.4, height=1.6, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([-3.1, 0.15, 0])
        body_hex = Rectangle(width=0.4, height=1.9, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.85).move_to([-3.4, 0.15, 0])
        # Conical nose seat: chamfered at 37 deg
        cone_seat = Polygon([-1.9, 0.95, 0], [-1.0, 0.30, 0], [-1.0, 0.0, 0], [-1.9, -0.65, 0],
                            color=COL_OK, fill_color=COL_OK).set_fill(COL_OK, 0.65)
        body_bore = Rectangle(width=3.0, height=0.45, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([-2.5, 0.15, 0])
        body_grp = VGroup(body_block, body_hex, cone_seat, body_bore)

        # 2. Tube with 37° Flared End
        # Straight tube stem
        t_stem = Rectangle(width=3.2, height=0.76, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.45).move_to([1.8, 0.15, 0])
        t_bore = Rectangle(width=3.5, height=0.45, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([1.8, 0.15, 0])
        # Flared cone skirt (angled outward at 37°)
        flare_top = Polygon([0.2, 0.53, 0], [-0.85, 1.05, 0], [-0.95, 0.95, 0], [0.1, 0.43, 0],
                            color=COL_OK, fill_color=COL_OK).set_fill(COL_OK, 0.95)
        flare_bot = Polygon([0.2, -0.23, 0], [-0.85, -0.75, 0], [-0.95, -0.65, 0], [0.1, -0.13, 0],
                            color=COL_OK, fill_color=COL_OK).set_fill(COL_OK, 0.95)
        flared_tube = VGroup(t_stem, t_bore, flare_top, flare_bot)

        # 3. Clamping Nut / Sleeve
        nut_sleeve = Polygon([0.4, 1.15, 0], [-0.75, 1.15, 0], [0.2, 0.55, 0], [0.4, 0.55, 0],
                             color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.7)
        nut_sleeve_bot = Polygon([0.4, -0.85, 0], [-0.75, -0.85, 0], [0.2, -0.25, 0], [0.4, -0.25, 0],
                                 color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.7)
        nut_body = Rectangle(width=1.8, height=1.9, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.35).move_to([1.3, 0.15, 0])
        nut_grp = VGroup(nut_sleeve, nut_sleeve_bot, nut_body)

        # Contact line highlight
        contact_line = DashedLine([-0.95, 0.95, 0], [-0.95, -0.65, 0], color=COL_OK, stroke_width=3)
        contact_lbl = Text("รอยประกบซีล 37° (Metal-to-Metal)", font_size=12, color=COL_OK).move_to([-0.95, 1.35, 0])

        flare_callout = Text(
            "ปลายท่อถูกบานออก 37° แล้วอัดแน่นกับที่นั่งเรียว — ผนังท่อหนาเท่าเดิม 100% ปราศจากรอยตัด",
            font_size=12, color=WHITE
        ).move_to([0, -1.55, 0])

        flare_diagram = VGroup(box_flare, body_grp, flared_tube, nut_grp, contact_line, contact_lbl, flare_callout)

        self.play(FadeIn(flare_diagram, shift=UP * 0.3), run_time=1.0)
        self.play(Indicate(contact_line, color=COL_OK, scale_factor=1.15), run_time=0.8)
        self.wait(1.8)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 16.8–22.8: Solution 2 — Compression Fitting (Ferrule Crimping)
        # ----------------------------------------------------------------------
        cap3 = caption_top("ทางแก้ 2: Compression Fitting (เฟอร์รูลบีบรัด)")
        sub3 = Text(
            "ไม่ต้องบานปลายท่อ — ใช้วงแหวนเฟอร์รูล (Ferrule) สวมรอบท่อตรง แล้วขันนัตให้อัดกอดผิวท่อ",
            font_size=12, color=COL_GRAY
        ).move_to([0, 2.25, 0])
        self.play(FadeIn(cap3, shift=UP * 0.3), FadeIn(sub3), run_time=0.8)

        # Compression Diagram Box
        box_comp = RoundedRectangle(
            corner_radius=0.12, width=11.6, height=3.5,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.92).move_to([0, -0.15, 0])

        # 1. Straight Tube (Completely straight, unlike flared tube!)
        str_tube = Rectangle(width=5.0, height=0.76, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.45).move_to([0.6, 0.15, 0])
        str_bore = Rectangle(width=5.2, height=0.45, color=COL_BG_BOX, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 1.0).move_to([0.6, 0.15, 0])
        str_tube_grp = VGroup(str_tube, str_bore)

        # 2. Fitting Body with internal cam angle
        c_body = Rectangle(width=2.4, height=1.6, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.45).move_to([-2.9, 0.15, 0])
        c_hex = Rectangle(width=0.4, height=1.9, color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.85).move_to([-3.2, 0.15, 0])
        c_cam_top = Polygon([-1.7, 0.75, 0], [-1.2, 0.53, 0], [-1.2, 0.75, 0], color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9)
        c_cam_bot = Polygon([-1.7, -0.45, 0], [-1.2, -0.23, 0], [-1.2, -0.45, 0], color=COL_METAL, fill_color=COL_METAL).set_fill(COL_METAL, 0.9)
        c_body_grp = VGroup(c_body, c_hex, c_cam_top, c_cam_bot)

        # 3. Ferrule Ring (Distinct wedge-shaped sleeve around tube OD)
        ferrule_top = Polygon([-1.2, 0.53, 0], [-0.5, 0.72, 0], [-0.5, 0.53, 0], [-1.0, 0.48, 0],
                              color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.95)
        ferrule_bot = Polygon([-1.2, -0.23, 0], [-0.5, -0.42, 0], [-0.5, -0.23, 0], [-1.0, -0.18, 0],
                              color=COL_WARN, fill_color=COL_WARN).set_fill(COL_WARN, 0.95)
        ferrule_lbl = Text("ปลอกเฟอร์รูล (Ferrule)", font_size=12, color=COL_WARN).move_to([-0.8, 1.15, 0])
        ferrule_grp = VGroup(ferrule_top, ferrule_bot, ferrule_lbl)

        # 4. Compression Nut
        c_nut = Rectangle(width=1.6, height=1.8, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.4).move_to([0.6, 0.15, 0])
        nut_lbl = Text("นัตขันบีบอัด (Nut)", font_size=12, color=COL_FIELD).move_to([0.6, 1.35, 0])
        c_nut_grp = VGroup(c_nut, nut_lbl)

        # Bite crimp indicator
        crimp_arr_top = Arrow(start=[-0.9, 0.85, 0], end=[-1.0, 0.53, 0], color=COL_OK, stroke_width=2.5, max_tip_length_to_length_ratio=0.35)
        crimp_arr_bot = Arrow(start=[-0.9, -0.55, 0], end=[-1.0, -0.23, 0], color=COL_OK, stroke_width=2.5, max_tip_length_to_length_ratio=0.35)
        crimp_tag = Text("คมเฟอร์รูลจิกรัดผิวท่อ (Bite / Crimp) ล็อกและซีลสนิท", font_size=12, color=WHITE).move_to([0, -1.55, 0])

        comp_diagram = VGroup(box_comp, c_body_grp, str_tube_grp, ferrule_grp, c_nut_grp, crimp_arr_top, crimp_arr_bot, crimp_tag)

        self.play(FadeIn(comp_diagram, shift=UP * 0.3), run_time=1.0)
        self.play(Indicate(ferrule_grp, color=COL_OK, scale_factor=1.08), run_time=0.8)
        self.wait(1.8)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 22.8–28.8: Comparison Table (Pipe Thread vs Tube Fitting)
        # ----------------------------------------------------------------------
        cap4 = caption_top("เปรียบเทียบ: Pipe Thread (H6_05) vs Tube Fitting (คลิปนี้)")
        sub4 = Text(
            "ทั้งคู่ซีลได้โดยไม่พึ่งปะเก็น (Metal-to-Metal Seal) — แต่ใช้วิธีทางกลที่ต่างกันอย่างสิ้นเชิง",
            font_size=12, color=COL_GRAY
        ).move_to([0, 2.25, 0])
        self.play(FadeIn(cap4, shift=UP * 0.3), FadeIn(sub4), run_time=0.8)

        card_w, card_h = 5.8, 3.4
        c_y = -0.30

        # Left: Pipe Thread (H6_05)
        b_pipe = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h, color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.92).move_to([-3.2, c_y, 0])
        h_pipe = Text("Pipe Thread (ท่อ Pipe — H6_05)", font_size=13, color=COL_METAL).move_to([-3.2, c_y + 1.30, 0])
        div_p = Line([-5.8, c_y + 1.05, 0], [-0.6, c_y + 1.05, 0], color=COL_METAL, stroke_width=1.2)
        p1 = Text("• ท่อที่ใช้: ท่อเหล็กผนังหนา (Steel Pipe)", font_size=11, color=WHITE).move_to([-3.2, c_y + 0.75, 0])
        p2 = Text("• การแปรรูป: ต๊าปเกลียวเรียว (NPT) ตัดลึกเข้าผนัง", font_size=11, color=WHITE).move_to([-3.2, c_y + 0.30, 0])
        p3 = Text("• กลไกซีล: ยอด-รากเกลียวบดอัดกัน (Interference)", font_size=11, color=WHITE).move_to([-3.2, c_y - 0.15, 0])
        p4 = Text("• ข้อจำกัด: ผนังต้องหนามาก / ห้ามใช้กับท่อบาง", font_size=11, color=COL_WARN).move_to([-3.2, c_y - 0.60, 0])
        p5 = Text("• การใช้งาน: งานท่อเมนหลัก ทนแรงกระแทกสูง", font_size=11, color=COL_GRAY).move_to([-3.2, c_y - 1.05, 0])
        card_p = VGroup(b_pipe, h_pipe, div_p, p1, p2, p3, p4, p5)

        # Right: Tube Fitting (H6_08)
        b_tube = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.92).move_to([3.2, c_y, 0])
        h_tube = Text("Tube Fitting (ท่อ Tube — คลิปนี้)", font_size=13, color=COL_OK).move_to([3.2, c_y + 1.30, 0])
        div_t = Line([0.6, c_y + 1.05, 0], [5.8, c_y + 1.05, 0], color=COL_OK, stroke_width=1.2)
        u1 = Text("• ท่อที่ใช้: ท่อผนังบาง (เหล็ก, สแตนเลส, ทองแดง)", font_size=11, color=WHITE).move_to([3.2, c_y + 0.75, 0])
        u2 = Text("• การแปรรูป: บานปลาย 37° หรือสวม Ferrule", font_size=11, color=WHITE).move_to([3.2, c_y + 0.30, 0])
        u3 = Text("• กลไกซีล: ผิวโลหะประกบโลหะ (ไม่ตัดเนื้อท่อ)", font_size=11, color=WHITE).move_to([3.2, c_y - 0.15, 0])
        u4 = Text("• ข้อได้เปรียบ: คงความหนา 100% / ปลอดภัยต่อท่อบาง", font_size=11, color=COL_OK).move_to([3.2, c_y - 0.60, 0])
        u5 = Text("• การใช้งาน: เดินท่อประณีต, ดัดโค้งง่าย, ซ่อมบำรุงสะดวก", font_size=11, color=COL_GRAY).move_to([3.2, c_y - 1.05, 0])
        card_t = VGroup(b_tube, h_tube, div_t, u1, u2, u3, u4, u5)

        self.play(FadeIn(card_p, shift=UP * 0.25), FadeIn(card_t, shift=UP * 0.25), run_time=1.0)
        self.wait(3.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 28.8–33.0: Summary Card
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(
            corner_radius=0.15, width=11.4, height=3.5,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.25, 0])

        s_head = Text("สรุปสำคัญ: ข้อต่อท่อ Tube Fittings (hydraulic06 น.11)", font_size=16, color=COL_OK).move_to([0, 1.15, 0])
        s1 = Text("1. Tube ผนังบาง (1–3 mm) จึงเลี่ยงการตัดเกลียวเพื่อป้องกันท่อแตกจากความดัน", font_size=13, color=WHITE).move_to([0, 0.55, 0])
        s2 = Text("2. Flare Fitting: บานปลายท่อ 37° แล้วขันอัดเข้ากับที่นั่งเรียว (Metal-to-Metal Seal)", font_size=13, color=WHITE).move_to([0, 0.05, 0])
        s3 = Text("3. Compression Fitting: ปลอก Ferrule บีบรัดรอบผิวท่อตรง ยึดแน่นและซีลพร้อมกัน", font_size=13, color=WHITE).move_to([0, -0.45, 0])
        s4 = Text("4. ทั้งสองแบบซีลแรงดันสูงได้สนิทโดยไม่ต้องพึ่งปะเก็น และรักษาความแข็งแรงท่อ 100%", font_size=12, color=COL_CURR).move_to([0, -0.95, 0])

        sum_grp = VGroup(sum_box, s_head, s1, s2, s3, s4)

        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(3.0)

        self.clear_stage(run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 33.0–38.0: Review Question Card & Outro
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(
            corner_radius=0.15, width=11.2, height=2.6,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text(
            "ทำไม tube ถึงเลี่ยงการตัดเกลียว แต่ pipe (H6_05) กลับใช้เกลียวเป็นตัวซีลหลักได้สบายๆ?",
            font_size=14, color=WHITE
        ).move_to([0.0, 0.05, 0.0])
        q_ans = Text(
            "(คำตอบ: Pipe ผนังหนามาก ตัดเกลียวแล้วยังเหลือเนื้อรับแรงดัน แต่ Tube ผนังบาง 1–3 mm ถ้าตัดเกลียวจะเสี่ยงระเบิดแตก)",
            font_size=12, color=COL_GRAY
        ).move_to([0.0, -0.65, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)


# ==============================================================================
# SCENE 9: H6_09_FlexibleHoses1 (hydraulic06.pdf page 12)
# Duration: ~39.5 seconds | 2D SafeScene
# Pedagogical Focus: SAE 100R1-R5 Flexible Hose Construction & Reinforcement
# AHA Moment: SAE ratings differ by number/type of reinforcement layers —
#             more wire braid layers = higher working pressure (just like thicker wall in H6_04)
# High-Risk Check: R1 (1 wire braid layer) vs R2 (2 wire braid layers) visibly distinct & countable!
# Material Distinction: Wire braid (METAL) vs Textile yarn (OK) visually distinct!
# ==============================================================================
class H6_09_FlexibleHoses1(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [m for m in self.mobjects if m not in (self.title_m, self.ref_m)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def make_mesh_pattern(self, x_min, x_max, y_min, y_max, color, spacing=0.22, stroke_width=1.5):
        h = y_max - y_min
        lines = []
        if h <= 0 or x_max <= x_min:
            return VGroup()

        # Positive slope (+45 deg): line equation (x + t*h, y_min + t*h) for t in [0, 1]
        x = x_min - h
        while x <= x_max:
            t_start = max(0.0, (x_min - x) / h)
            t_end = min(1.0, (x_max - x) / h)
            if t_start < t_end:
                pt_a = np.array([x + t_start * h, y_min + t_start * h, 0])
                pt_b = np.array([x + t_end * h, y_min + t_end * h, 0])
                lines.append(Line(pt_a, pt_b, color=color, stroke_width=stroke_width))
            x += spacing

        # Negative slope (-45 deg): line equation (x - t*h, y_min + t*h) for t in [0, 1]
        x = x_min
        while x <= x_max + h:
            t_start = max(0.0, (x - x_max) / h)
            t_end = min(1.0, (x - x_min) / h)
            if t_start < t_end:
                pt_a = np.array([x - t_start * h, y_min + t_start * h, 0])
                pt_b = np.array([x - t_end * h, y_min + t_end * h, 0])
                lines.append(Line(pt_a, pt_b, color=color, stroke_width=stroke_width))
            x += spacing

        return VGroup(*lines)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = title("สายไฮดรอลิกยืดหยุ่น (SAE 100R1-R5)")
        self.ref_m = page_ref("hydraulic06 น.12")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.5)
        self.wait(0.5)

        # ----------------------------------------------------------------------
        # BEAT 2.0–4.6: Hook Question
        # ----------------------------------------------------------------------
        hook_q = caption_top("สาย SAE 100R1 กับ 100R2 เลขต่างกัน — ต่างกันตรงไหนจริงๆ?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.8)
        self.wait(1.3)
        self.play(FadeOut(hook_q), run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 4.6–10.5: 3-Layer Construction Cutaway
        # ----------------------------------------------------------------------
        cap1 = caption_top("โครงสร้างสายไฮดรอลิก 3 ชั้นหลัก")
        sub1 = Text(
            "ประกอบด้วย ท่อในยางทนน้ำมัน + ชั้นเสริมแรงรับแรงดัน + เปลือกนอกทนสภาพอากาศ",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap1, shift=UP * 0.3), FadeIn(sub1), run_time=0.7)

        y_c = -0.15
        # 1. Outer Cover (charcoal rubber)
        cov_w, cov_h = 3.2, 2.0
        cov_box = Rectangle(width=cov_w, height=cov_h, color=COL_GRAY, stroke_width=1.5).set_fill("#263238", 0.95).move_to([-3.4, y_c, 0])
        cov_lbl = VGroup(
            Text("1. เปลือกนอก (Outer Cover)", font_size=13, color=COL_GRAY),
            Text("ยางสังเคราะห์ทนสภาพอากาศ & รอยขีดข่วน", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.08).move_to([-3.4, -1.65, 0])
        cov_line = Line([-3.4, -1.05, 0], [-3.4, -1.35, 0], color=COL_GRAY, stroke_width=1.5)
        cov_grp = VGroup(cov_box, cov_line, cov_lbl)

        # 2. Reinforcement Layer (wire braid mesh)
        brd_w, brd_h = 3.0, 1.5
        brd_box = Rectangle(width=brd_w, height=brd_h, color=COL_METAL, stroke_width=1.5).set_fill("#37474F", 0.90).move_to([-0.3, y_c, 0])
        mesh_lines = self.make_mesh_pattern(-1.8, 1.2, y_c - brd_h / 2, y_c + brd_h / 2, color="#CFD8DC", spacing=0.20, stroke_width=1.8)
        brd_lbl = VGroup(
            Text("2. ชั้นเสริมแรง (Reinforcement)", font_size=13, color=COL_CURR),
            Text("ลวดเหล็กถัก / ผ้าถัก — ตัวกำหนดความดัน", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.08).move_to([-0.3, 1.45, 0])
        brd_line = Line([-0.3, 0.65, 0], [-0.3, 1.15, 0], color=COL_CURR, stroke_width=1.5)
        brd_grp = VGroup(brd_box, mesh_lines, brd_line, brd_lbl)

        # 3. Inner Tube (oil resistant rubber)
        inn_w, inn_h = 2.6, 1.0
        inn_box = Rectangle(width=inn_w, height=inn_h, color=COL_FIELD, stroke_width=1.5).set_fill("#1565C0", 0.90).move_to([2.5, y_c, 0])
        inn_lbl = VGroup(
            Text("3. ท่อใน (Inner Tube)", font_size=13, color=COL_FIELD),
            Text("ยางสังเคราะห์ทนการกัดกร่อนของน้ำมัน", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.08).move_to([2.5, -1.65, 0])
        inn_line = Line([2.5, -0.65, 0], [2.5, -1.35, 0], color=COL_FIELD, stroke_width=1.5)

        # Open Bore & Fluid Flow
        bore_end = Ellipse(width=0.25, height=0.6, color=SUPPLY).set_fill(SUPPLY, 0.85).move_to([3.8, y_c, 0])
        bore_lip = Arc(radius=0.5, start_angle=-PI / 2, angle=PI, color=COL_FIELD, stroke_width=2.0).move_to([3.8, y_c, 0])
        flow_arr = Arrow(start=[5.8, y_c, 0], end=[4.3, y_c, 0], color=SUPPLY, stroke_width=3.0, max_tip_length_to_length_ratio=0.3)
        flow_lbl = Text("น้ำมันไฮดรอลิก (Oil Flow)", font_size=11, color=SUPPLY).move_to([5.05, y_c + 0.35, 0])

        inn_grp = VGroup(inn_box, bore_end, bore_lip, flow_arr, flow_lbl, inn_line, inn_lbl)

        hose_3layer = VGroup(cov_grp, brd_grp, inn_grp)

        self.play(
            LaggedStart(
                FadeIn(inn_grp, shift=UP * 0.2),
                FadeIn(brd_grp, shift=UP * 0.2),
                FadeIn(cov_grp, shift=UP * 0.2),
                lag_ratio=0.35
            ),
            run_time=2.4
        )
        self.play(Indicate(brd_box, color=COL_CURR), run_time=0.8)
        self.wait(2.2)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 10.5–17.5: High-Risk Check — SAE 100R1 vs 100R2 Layer Count (§41/§44)
        # ----------------------------------------------------------------------
        cap2 = caption_top("SAE 100R1 → 100R2: เพิ่มชั้นลวดถัก = รับความดันได้มากขึ้น")
        sub2 = Text(
            "เลข SAE ไม่ใช่แค่ชื่อรุ่น แต่บอกโครงสร้างชั้นเสริมแรงอย่างเจาะจง",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap2, shift=UP * 0.3), FadeIn(sub2), run_time=0.7)

        # --------------------
        # SAE 100R1: 1 Wire Braid Layer (t = 13.5s Checkpoint)
        # --------------------
        badge_r1 = VGroup(
            Text("SAE 100R1 — ลวดถัก 1 ชั้น (1 Wire Braid)", font_size=16, color=COL_METAL),
            Text("ความดันใช้งาน: ปานกลาง (Medium Pressure)  |  นับชั้นลวดได้: 1 ชั้น", font_size=12, color=WHITE)
        ).arrange(DOWN, buff=0.1).move_to([0, 1.40, 0])
        box_badge_r1 = SurroundingRectangle(badge_r1, color=COL_METAL, buff=0.15, corner_radius=0.1)

        # Hose R1 model
        cov_r1 = Rectangle(width=3.2, height=1.9, color=COL_GRAY, stroke_width=1.5).set_fill("#263238", 0.95).move_to([-3.4, y_c, 0])
        brd_r1 = Rectangle(width=3.0, height=1.45, color=COL_METAL, stroke_width=1.5).set_fill("#37474F", 0.90).move_to([-0.3, y_c, 0])
        mesh_r1 = self.make_mesh_pattern(-1.8, 1.2, y_c - 1.45 / 2, y_c + 1.45 / 2, color="#CFD8DC", spacing=0.20, stroke_width=1.8)
        inn_r1 = Rectangle(width=2.6, height=1.0, color=COL_FIELD, stroke_width=1.5).set_fill("#1565C0", 0.90).move_to([2.5, y_c, 0])
        lip_r1 = Ellipse(width=0.25, height=0.6, color=SUPPLY).set_fill(SUPPLY, 0.85).move_to([3.8, y_c, 0])

        count_lbl_r1 = Text("ลวดถัก 1 ชั้น (Single Wire Braid)", font_size=13, color=COL_METAL).move_to([-0.3, -1.35, 0])
        count_arrow_r1 = Arrow(start=[-0.3, -1.05, 0], end=[-0.3, -0.65, 0], color=COL_METAL, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)

        grp_r1 = VGroup(cov_r1, brd_r1, mesh_r1, inn_r1, lip_r1, count_lbl_r1, count_arrow_r1, badge_r1, box_badge_r1)

        self.play(FadeIn(grp_r1, shift=UP * 0.25), run_time=1.0)
        self.wait(1.5)

        # Fade out R1 count label first before transforming to R2 to prevent overlap
        self.play(
            FadeOut(count_lbl_r1),
            FadeOut(count_arrow_r1),
            run_time=0.35
        )

        # --------------------
        # Transform to SAE 100R2: 2 Stepped Wire Braid Layers (t = 16.0s Checkpoint)
        # Countable layers: Layer 1 (inner) and Layer 2 (outer)!
        # --------------------
        badge_r2 = VGroup(
            Text("SAE 100R2 — ลวดถัก 2 ชั้น (2 Wire Braids)", font_size=16, color=COL_WARN),
            Text("ความดันใช้งาน: สูง (High Pressure)  |  รับแรงดันได้สูงขึ้น ~1.5–2 เท่า!", font_size=12, color=COL_OK)
        ).arrange(DOWN, buff=0.1).move_to([0, 1.40, 0])
        box_badge_r2 = SurroundingRectangle(badge_r2, color=COL_WARN, buff=0.15, corner_radius=0.1)

        # Hose R2 stepped model
        cov_r2 = Rectangle(width=2.6, height=2.05, color=COL_GRAY, stroke_width=1.5).set_fill("#263238", 0.95).move_to([-3.7, y_c, 0])

        # Layer 2 (Outer Wire Braid) - highlighted in WARN bronze
        brd_l2 = Rectangle(width=1.6, height=1.65, color=COL_WARN, stroke_width=1.5).set_fill("#4E342E", 0.90).move_to([-1.6, y_c, 0])
        mesh_l2 = self.make_mesh_pattern(-2.4, -0.8, y_c - 1.65 / 2, y_c + 1.65 / 2, color="#FFB74D", spacing=0.18, stroke_width=1.8)
        lbl_l2 = Text("ชั้นที่ 2 (นอก)", font_size=12, color=COL_WARN).move_to([-1.6, -1.35, 0])
        arr_l2 = Arrow(start=[-1.6, -1.05, 0], end=[-1.6, -0.65, 0], color=COL_WARN, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)

        # Layer 1 (Inner Wire Braid) - in standard steel METAL
        brd_l1 = Rectangle(width=2.0, height=1.35, color=COL_METAL, stroke_width=1.5).set_fill("#37474F", 0.90).move_to([0.2, y_c, 0])
        mesh_l1 = self.make_mesh_pattern(-0.8, 1.2, y_c - 1.35 / 2, y_c + 1.35 / 2, color="#CFD8DC", spacing=0.18, stroke_width=1.8)
        lbl_l1 = Text("ชั้นที่ 1 (ใน)", font_size=12, color=COL_METAL).move_to([0.2, -1.35, 0])
        arr_l1 = Arrow(start=[0.2, -1.05, 0], end=[0.2, -0.55, 0], color=COL_METAL, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)

        inn_r2 = Rectangle(width=2.6, height=1.0, color=COL_FIELD, stroke_width=1.5).set_fill("#1565C0", 0.90).move_to([2.5, y_c, 0])
        lip_r2 = Ellipse(width=0.25, height=0.6, color=SUPPLY).set_fill(SUPPLY, 0.85).move_to([3.8, y_c, 0])

        grp_r2_layers = VGroup(cov_r2, brd_l2, mesh_l2, lbl_l2, arr_l2, brd_l1, mesh_l1, lbl_l1, arr_l1, inn_r2, lip_r2)

        self.play(
            ReplacementTransform(badge_r1, badge_r2),
            ReplacementTransform(box_badge_r1, box_badge_r2),
            ReplacementTransform(cov_r1, cov_r2),
            ReplacementTransform(brd_r1, VGroup(brd_l2, brd_l1)),
            ReplacementTransform(mesh_r1, VGroup(mesh_l2, mesh_l1)),
            FadeIn(lbl_l2), FadeIn(arr_l2),
            FadeIn(lbl_l1), FadeIn(arr_l1),
            ReplacementTransform(inn_r1, inn_r2),
            ReplacementTransform(lip_r1, lip_r2),
            run_time=1.6
        )
        self.play(Indicate(brd_l2, color=COL_WARN), Indicate(lbl_l2, color=COL_WARN), run_time=0.8)
        self.wait(1.5)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 17.5–23.2: Material Distinction — SAE 100R3–R5 Textile Braid (§34/§45)
        # ----------------------------------------------------------------------
        cap3 = caption_top("SAE 100R3 – 100R5: เสริมแรงด้วยผ้าถัก (Textile Yarn)")
        sub3 = Text(
            "เปลี่ยนจากลวดโลหะ (Metal) เป็นเส้นใยผ้าถัก (Textile) เพื่อความยืดหยุ่นสูง",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap3, shift=UP * 0.3), FadeIn(sub3), run_time=0.7)

        # Hose model with Textile weave
        cov_r3 = Rectangle(width=3.2, height=1.9, color=COL_GRAY, stroke_width=1.5).set_fill("#263238", 0.95).move_to([-3.4, y_c, 0])
        brd_r3 = Rectangle(width=3.0, height=1.45, color=COL_OK, stroke_width=1.5).set_fill("#004D40", 0.90).move_to([-0.3, y_c, 0])
        # Dense fine fabric weave
        mesh_r3 = self.make_mesh_pattern(-1.8, 1.2, y_c - 1.45 / 2, y_c + 1.45 / 2, color=COL_OK, spacing=0.12, stroke_width=1.2)
        inn_r3 = Rectangle(width=2.6, height=1.0, color=COL_FIELD, stroke_width=1.5).set_fill("#1565C0", 0.90).move_to([2.5, y_c, 0])
        lip_r3 = Ellipse(width=0.25, height=0.6, color=SUPPLY).set_fill(SUPPLY, 0.85).move_to([3.8, y_c, 0])

        tag_textile = Text("เส้นใยผ้าถัก (Textile Yarn Braid)", font_size=13, color=COL_OK).move_to([-0.3, -1.35, 0])
        tag_arr = Arrow(start=[-0.3, -1.05, 0], end=[-0.3, -0.65, 0], color=COL_OK, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)

        hose_textile = VGroup(cov_r3, brd_r3, mesh_r3, inn_r3, lip_r3, tag_textile, tag_arr)

        # Feature badges
        badge_adv = VGroup(
            Text("✓ ข้อเด่น: อ่อนตัวสูง ดัดโค้งง่าย", font_size=14, color=COL_OK),
            Text("รัศมีดัดงอแคบ (Small Bend Radius) ไม่ล้าเมื่อขยับบ่อย", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.08).move_to([-3.2, 1.40, 0])
        box_adv = SurroundingRectangle(badge_adv, color=COL_OK, buff=0.12, corner_radius=0.08)

        badge_lim = VGroup(
            Text("⚠️ ข้อจำกัด: ทนความดันได้ต่ำกว่า", font_size=14, color=COL_WARN),
            Text("รับแรงดันได้น้อยกว่าลวดเหล็ก เหมาะกับระบบ Return / Low-Pressure", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.08).move_to([3.2, 1.40, 0])
        box_lim = SurroundingRectangle(badge_lim, color=COL_WARN, buff=0.12, corner_radius=0.08)

        self.play(FadeIn(hose_textile, shift=UP * 0.25), run_time=1.0)
        self.play(Indicate(brd_r3, color=COL_OK), run_time=0.7)
        self.play(
            FadeIn(badge_adv, shift=UP * 0.15), Create(box_adv),
            FadeIn(badge_lim, shift=UP * 0.15), Create(box_lim),
            run_time=1.2
        )
        self.wait(2.2)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 23.2–29.2: Callback to H6_04 (Schedule Number) Comparison Table
        # ----------------------------------------------------------------------
        cap4 = caption_top("หลักการเดียวกับ H6_04 (Pipe Schedule Number)")
        sub4 = Text(
            "วัสดุต่างกัน (ท่อเหล็กแข็ง vs สายยืดหยุ่น) แต่หลักการวิศวกรรมเหมือนกันทุกประการ",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap4, shift=UP * 0.3), FadeIn(sub4), run_time=0.8)

        card_w, card_h = 5.8, 3.4
        c_y = -0.30

        # Left: Rigid Steel Pipe (H6_04)
        b_rigid = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h, color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.92).move_to([-3.2, c_y, 0])
        h_rigid = Text("ท่อเหล็กแข็ง (Steel Pipe — H6_04)", font_size=13, color=COL_METAL).move_to([-3.2, c_y + 1.30, 0])
        div_r = Line([-5.8, c_y + 1.05, 0], [-0.6, c_y + 1.05, 0], color=COL_METAL, stroke_width=1.2)
        r1 = Text("• วิธีเสริมแรง: เพิ่มความหนาผนังท่อ t", font_size=11, color=WHITE).move_to([-3.2, c_y + 0.75, 0])
        r2 = Text("• ระดับมาตรฐาน: Schedule 40 → Sch 80 → Sch 160", font_size=11, color=WHITE).move_to([-3.2, c_y + 0.30, 0])
        r3 = Text("• การรับความดัน: BP = 2tS / Di (ยิ่งผนังหนา ยิ่งทนสูง)", font_size=11, color=WHITE).move_to([-3.2, c_y - 0.15, 0])
        r4 = Text("• ข้อจำกัด: ดัดงอไม่ได้ / แข็งเกร็ง / หนักขึ้นตาม Schedule", font_size=11, color=COL_WARN).move_to([-3.2, c_y - 0.60, 0])
        r5 = Text("• การใช้งาน: ท่อเมนหลัก โครงสร้างเครื่องจักรคงที่", font_size=11, color=COL_GRAY).move_to([-3.2, c_y - 1.05, 0])
        card_rigid = VGroup(b_rigid, h_rigid, div_r, r1, r2, r3, r4, r5)

        # Right: Flexible Hose (H6_09)
        b_flex = RoundedRectangle(corner_radius=0.12, width=card_w, height=card_h, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.92).move_to([3.2, c_y, 0])
        h_flex = Text("สายยืดหยุ่น (Flexible Hose — คลิปนี้)", font_size=13, color=COL_OK).move_to([3.2, c_y + 1.30, 0])
        div_f = Line([0.6, c_y + 1.05, 0], [5.8, c_y + 1.05, 0], color=COL_OK, stroke_width=1.2)
        f1 = Text("• วิธีเสริมแรง: เพิ่มจำนวนชั้นลวดถัก / ผ้าถัก", font_size=11, color=WHITE).move_to([3.2, c_y + 0.75, 0])
        f2 = Text("• ระดับมาตรฐาน: SAE 100R1 (1 ชั้น) → 100R2 (2 ชั้น)", font_size=11, color=WHITE).move_to([3.2, c_y + 0.30, 0])
        f3 = Text("• การรับความดัน: ชั้นลวดรับแรงดึงในแนวเส้นรอบวง", font_size=11, color=WHITE).move_to([3.2, c_y - 0.15, 0])
        f4 = Text("• ข้อได้เปรียบ: ดัดโค้งงอได้ ซับแรงสั่นสะเทือนได้ดีเยี่ยม", font_size=11, color=COL_OK).move_to([3.2, c_y - 0.60, 0])
        f5 = Text("• การใช้งาน: แขนกล กระบอกสูบที่เคลื่อนที่ อุปกรณ์ขยับ", font_size=11, color=COL_GRAY).move_to([3.2, c_y - 1.05, 0])
        card_flex = VGroup(b_flex, h_flex, div_f, f1, f2, f3, f4, f5)

        self.play(FadeIn(card_rigid, shift=UP * 0.25), FadeIn(card_flex, shift=UP * 0.25), run_time=1.0)
        self.wait(3.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 29.2–34.2: Summary Card
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(
            corner_radius=0.15, width=11.4, height=3.5,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.25, 0])

        s_head = Text("สรุปสำคัญ: สายไฮดรอลิกยืดหยุ่น (hydraulic06 น.12)", font_size=16, color=COL_OK).move_to([0, 1.15, 0])
        s1 = Text("1. โครงสร้างพื้นฐาน 3 ชั้น: ท่อในยางทนน้ำมัน + ชั้นเสริมแรง + เปลือกนอกทนสภาพอากาศ", font_size=13, color=WHITE).move_to([0, 0.55, 0])
        s2 = Text("2. SAE 100R1 vs 100R2: ต่างกันที่จำนวนชั้นลวดถัก (1 ชั้น vs 2 ชั้น — รับความดันต่างกัน ~1.5–2 เท่า)", font_size=13, color=WHITE).move_to([0, 0.05, 0])
        s3 = Text("3. SAE 100R3–R5: เสริมแรงด้วยผ้าถัก (Textile) ดัดโค้งรัศมีแคบได้ดี แต่นิยมใช้ในระบบความดันต่ำ", font_size=13, color=WHITE).move_to([0, -0.45, 0])
        s4 = Text("4. หลักการเดียวกับ H6_04: เสริมแรงมากขึ้น (ลวดมากขึ้น / ผนังหนาขึ้น) = รับความดันได้มากขึ้น", font_size=12, color=COL_CURR).move_to([0, -0.95, 0])

        sum_grp = VGroup(sum_box, s_head, s1, s2, s3, s4)

        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(3.2)

        self.clear_stage(run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 34.2–39.2: Review Question Card & Outro
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(
            corner_radius=0.15, width=11.2, height=2.6,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text(
            "งานที่ต้องขยับงอสายไปมาบ่อยๆ ความดันไม่สูงมาก ควรเลือกสายลวดถัก (R1/R2) หรือผ้าถัก (R3–R5) ดีกว่า?",
            font_size=14, color=WHITE
        ).move_to([0.0, 0.05, 0.0])
        q_ans = Text(
            "(คำตอบ: ควรเลือกสายผ้าถัก R3–R5 เพราะยืดหยุ่น ดัดโค้งรัศมีแคบได้ง่าย และทนต่อความล้าจากการเคลื่อนที่ต่อเนื่องได้ดีกว่า)",
            font_size=12, color=COL_GRAY
        ).move_to([0.0, -0.65, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)


# ==============================================================================
# SCENE 10: H6_10_FlexibleHoses2 (hydraulic06.pdf page 13)
# Duration: ~46.5 seconds | 2D SafeScene
# Pedagogical Focus: SAE 100R6-R12 Flexible Hoses & Spiral-Wound Wire Physics
# AHA Moment: R9-R12 wire plies are SPIRAL-wound (parallel diagonal), not braided (cross-hatch).
#             Under high pressure, single-direction spiral creates net axial torque causing twist.
#             Alternating winding directions (left vs right) cancels net torque, keeping hose straight!
# Animated Proof (§32):
#   - Beat 17.8-23.0s: Single-direction spiral hose under pressure -> net torque arrow -> hose end rotates 60° (twist!).
#   - Beat 23.8-29.0s: Alternating layers in same frame (slanted left vs right) -> opposing torques cancel (Στ=0) -> hose stays straight!
# High-Risk Check 1 (§41/§44): Hose end actually rotated between t=19.5s and t=21.5s (measured angle change).
# High-Risk Check 2 (§41/§44): Layer 1 (slanted left) and Layer 2 (slanted right) visibly slant in opposite directions in same frame at t=27.0s.
# ==============================================================================
class H6_10_FlexibleHoses2(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [m for m in self.mobjects if m not in (self.title_m, self.ref_m)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def make_mesh_pattern(self, x_min, x_max, y_min, y_max, color, spacing=0.20, stroke_width=1.5):
        h = y_max - y_min
        lines = []
        if h <= 0 or x_max <= x_min:
            return VGroup()
        x = x_min - h
        while x <= x_max:
            t0 = max(0.0, (x_min - x) / h)
            t1 = min(1.0, (x_max - x) / h)
            if t0 < t1:
                lines.append(Line([x + t0 * h, y_min + t0 * h, 0], [x + t1 * h, y_min + t1 * h, 0], color=color, stroke_width=stroke_width))
            x += spacing
        x = x_min
        while x <= x_max + h:
            t0 = max(0.0, (x - x_max) / h)
            t1 = min(1.0, (x - x_min) / h)
            if t0 < t1:
                lines.append(Line([x - t0 * h, y_min + t0 * h, 0], [x - t1 * h, y_min + t1 * h, 0], color=color, stroke_width=stroke_width))
            x += spacing
        return VGroup(*lines)

    def make_spiral_pattern(self, x_min, x_max, y_min, y_max, color, spacing=0.22, stroke_width=2.0, direction="right", slope_dx_ratio=1.25):
        h = y_max - y_min
        dx = h * slope_dx_ratio
        lines = []
        if h <= 0 or x_max <= x_min:
            return VGroup()
        if direction == "right":
            x0 = x_min - dx
            while x0 <= x_max:
                t0 = max(0.0, (x_min - x0) / dx)
                t1 = min(1.0, (x_max - x0) / dx)
                if t0 < t1:
                    lines.append(Line([x0 + t0 * dx, y_min + t0 * h, 0], [x0 + t1 * dx, y_min + t1 * h, 0], color=color, stroke_width=stroke_width))
                x0 += spacing
        else:
            x0 = x_min
            while x0 <= x_max + dx:
                t0 = max(0.0, (x0 - x_max) / dx)
                t1 = min(1.0, (x0 - x_min) / dx)
                if t0 < t1:
                    lines.append(Line([x0 - t0 * dx, y_min + t0 * h, 0], [x0 - t1 * dx, y_min + t1 * h, 0], color=color, stroke_width=stroke_width))
                x0 += spacing
        return VGroup(*lines)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title Header
        # ----------------------------------------------------------------------
        self.title_m = title("สายไฮดรอลิกยืดหยุ่น (SAE 100R6-R12)")
        self.ref_m = page_ref("hydraulic06 น.13")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.0)
        self.wait(1.0)  # Checkpoint 1.5s

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.0: SAE 100R6 (Textile Braid Recap)
        # ----------------------------------------------------------------------
        cap1 = caption_top("R6: ผ้าถัก 1 ชั้น (เหมือน R3-R5 ใน H6_09)")
        sub1 = Text(
            "สายผ้าถัก 1 ชั้น สำหรับระบบความดันต่ำ (Low Pressure / Return Line)",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap1, shift=UP * 0.3), FadeIn(sub1), run_time=0.8)

        # 3-Layer R6 Cutaway diagram
        y_c = -0.35
        # 1. Outer cover (rubber, charcoal)
        c_cov_r6 = Rectangle(width=2.4, height=1.6, color="#37474F", fill_color="#37474F").set_fill("#37474F", 0.92).set_stroke(COL_METAL, 1.2).move_to([-3.0, y_c, 0])
        lbl_cov_r6 = Text("เปลือกนอกยาง (Cover)", font_size=11, color=COL_GRAY).next_to(c_cov_r6, DOWN, buff=0.18)

        # 2. Reinforcement: 1 textile braid ply (COL_OK, mesh texture)
        c_brd_r6 = Rectangle(width=2.4, height=1.2, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.9).set_stroke(COL_OK, 1.5).move_to([-0.6, y_c, 0])
        mesh_r6 = self.make_mesh_pattern(-1.8, 0.6, y_c - 0.6, y_c + 0.6, color=COL_OK, spacing=0.18, stroke_width=1.4)
        lbl_brd_r6 = Text("ผ้าถัก 1 ชั้น (1 Textile Braid)", font_size=11, color=COL_OK).next_to(c_brd_r6, UP, buff=0.18)

        # 3. Inner tube (synthetic rubber, COL_FIELD)
        c_tube_r6 = Rectangle(width=2.4, height=0.8, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.85).set_stroke(WHITE, 1.0).move_to([1.8, y_c, 0])
        lbl_tube_r6 = Text("ท่อในยาง (Rubber Tube)", font_size=11, color=COL_FIELD).next_to(c_tube_r6, DOWN, buff=0.18)

        # 4. Fluid bore opening
        c_bore_r6 = Ellipse(width=0.35, height=0.5, color=SUPPLY, fill_color=SUPPLY).set_fill(SUPPLY, 0.95).move_to([3.0, y_c, 0])

        badge_r6 = VGroup(
            Text("SAE 100R6 Spec:", font_size=13, color=COL_OK),
            Text("• โครงสร้าง: ยางสังเคราะห์ + ผ้าถัก 1 ชั้น", font_size=11, color=WHITE),
            Text("• ความดันใช้งาน: ต่ำ (Low Working Pressure ~30–70 bar)", font_size=11, color=COL_GRAY)
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([0, -2.45, 0])
        box_r6 = SurroundingRectangle(badge_r6, color=COL_OK, buff=0.15, corner_radius=0.1)

        grp_r6 = VGroup(c_cov_r6, lbl_cov_r6, c_brd_r6, mesh_r6, lbl_brd_r6, c_tube_r6, lbl_tube_r6, c_bore_r6, badge_r6, box_r6)
        self.play(FadeIn(grp_r6, shift=UP * 0.25), run_time=1.0)
        self.wait(1.2)  # Checkpoint 3.5s

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 5.8–11.0: SAE 100R7/R8 (Thermoplastic Inner Tube)
        # ----------------------------------------------------------------------
        cap2 = caption_top("R7/R8: เปลี่ยนวัสดุท่อใน — เทอร์โมพลาสติก ไม่ใช่ยาง")
        sub2 = Text(
            "วัสดุสังเคราะห์พิเศษ (Thermoplastic): ทนสารเคมีและของเหลวสังเคราะห์ได้ดีกว่ายางธรรมดา",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap2, shift=UP * 0.3), FadeIn(sub2), run_time=0.8)

        # Cutaway diagram showing thermoplastic transformation
        c_cov_r7 = Rectangle(width=2.4, height=1.6, color=COL_CURR, fill_color="#263238").set_fill("#263238", 0.92).set_stroke(COL_CURR, 1.2).move_to([-3.0, y_c, 0])
        lbl_cov_r7 = Text("ปลอกเทอร์โมพลาสติก", font_size=11, color=COL_CURR).next_to(c_cov_r7, DOWN, buff=0.18)

        c_brd_r7 = Rectangle(width=2.4, height=1.2, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.9).set_stroke(COL_OK, 1.5).move_to([-0.6, y_c, 0])
        mesh_r7 = self.make_mesh_pattern(-1.8, 0.6, y_c - 0.6, y_c + 0.6, color=COL_OK, spacing=0.18, stroke_width=1.4)
        lbl_brd_r7 = Text("เส้นใยสังเคราะห์ (Synthetic Fiber)", font_size=11, color=COL_OK).next_to(c_brd_r7, UP, buff=0.18)

        # Start tube as rubber (FIELD) then transform to thermoplastic (CURR)
        c_tube_r7 = Rectangle(width=2.4, height=0.8, color=COL_FIELD, fill_color=COL_FIELD).set_fill(COL_FIELD, 0.85).set_stroke(WHITE, 1.0).move_to([1.8, y_c, 0])
        lbl_tube_r7 = Text("ท่อใน: ยางสังเคราะห์ (เดิม)", font_size=11, color=COL_FIELD).next_to(c_tube_r7, DOWN, buff=0.18)
        c_bore_r7 = Ellipse(width=0.35, height=0.5, color=SUPPLY, fill_color=SUPPLY).set_fill(SUPPLY, 0.95).move_to([3.0, y_c, 0])

        self.play(FadeIn(VGroup(c_cov_r7, lbl_cov_r7, c_brd_r7, mesh_r7, lbl_brd_r7, c_tube_r7, lbl_tube_r7, c_bore_r7), shift=UP * 0.25), run_time=0.9)
        self.wait(0.5)

        # Material transformation: rubber -> thermoplastic
        c_tube_tp = Rectangle(width=2.4, height=0.8, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 0.85).set_stroke(WHITE, 1.5).move_to([1.8, y_c, 0])
        lbl_tube_tp = Text("ท่อใน: เทอร์โมพลาสติก (Thermoplastic)", font_size=11, color=COL_CURR).next_to(c_tube_tp, DOWN, buff=0.18)

        card_tp_left = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.3, color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([-3.2, -2.45, 0])
        t_tp1 = Text("ท่อในเทอร์โมพลาสติก (Thermoplastic Tube):", font_size=12, color=COL_CURR).move_to([-3.2, -2.15, 0])
        t_tp2 = Text("• ทนของเหลวไฮดรอลิกสังเคราะห์ ทนสารเคมีกัดกร่อน", font_size=10.5, color=WHITE).move_to([-3.2, -2.45, 0])
        t_tp3 = Text("• ไม่บวมน้ำมัน น้ำหนักเบา ผิวในเรียบลื่น ลดความดันตก", font_size=10.5, color=COL_GRAY).move_to([-3.2, -2.75, 0])
        grp_tp_left = VGroup(card_tp_left, t_tp1, t_tp2, t_tp3)

        card_tp_right = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.3, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([3.2, -2.45, 0])
        t_tr1 = Text("ความแตกต่าง SAE 100R7 vs 100R8:", font_size=12, color=COL_OK).move_to([3.2, -2.15, 0])
        t_tr2 = Text("• R7: เสริมเส้นใยสังเคราะห์ 1–2 ชั้น (Medium Pressure)", font_size=10.5, color=WHITE).move_to([3.2, -2.45, 0])
        t_tr3 = Text("• R8: เสริมเส้นใยสังเคราะห์ความแข็งแรงสูง (High Pressure)", font_size=10.5, color=COL_GRAY).move_to([3.2, -2.75, 0])
        grp_tp_right = VGroup(card_tp_right, t_tr1, t_tr2, t_tr3)

        self.play(
            ReplacementTransform(c_tube_r7, c_tube_tp),
            ReplacementTransform(lbl_tube_r7, lbl_tube_tp),
            FadeIn(grp_tp_left, shift=UP * 0.2),
            FadeIn(grp_tp_right, shift=UP * 0.2),
            run_time=1.4
        )
        self.play(Indicate(c_tube_tp, color=COL_CURR), run_time=0.8)
        self.wait(1.4)  # Checkpoint 9.0s

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 11.8–17.0: SAE 100R9-R12 (Spiral Plies Introduction)
        # ----------------------------------------------------------------------
        cap3 = caption_top("R9-R12: ลวดพันเกลียว ไม่ใช่ถักไขว้")
        sub3 = Text(
            "Spiral Plies: เส้นลวดขนานเรียงตัวในทิศทางเดียว ไม่ขัดสานไขว้กันแบบลวดถัก (Braid)",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap3, shift=UP * 0.3), FadeIn(sub3), run_time=0.8)

        # Comparison side by side: Braid (left) vs Spiral (right)
        y_comp = 0.0
        # Left: Braided mesh (criss-cross)
        box_braid = RoundedRectangle(corner_radius=0.12, width=5.6, height=3.0, color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([-3.3, y_comp, 0])
        t_braid_h = Text("ลวดถักไขว้ (Braided Wire — R1/R2)", font_size=13, color=COL_METAL).move_to([-3.3, y_comp + 1.15, 0])
        hose_body_b = Rectangle(width=4.4, height=1.2, color=COL_METAL, fill_color="#263238").set_fill("#263238", 0.9).move_to([-3.3, y_comp + 0.15, 0])
        mesh_braid = self.make_mesh_pattern(-5.5, -1.1, y_comp + 0.15 - 0.6, y_comp + 0.15 + 0.6, color=COL_METAL, spacing=0.22, stroke_width=1.8)
        t_b1 = Text("• เส้นลวดขัดไขว้กันเป็นตาราง (Criss-Cross)", font_size=10.5, color=COL_GRAY)
        t_b2 = Text("• เกิดแรงเฉือนที่จุดตัดเมื่อรับแรงดันสูงมาก", font_size=10.5, color=COL_GRAY)
        t_braid_sub = VGroup(t_b1, t_b2).arrange(DOWN, buff=0.10, aligned_edge=LEFT).move_to([-3.3, y_comp - 0.85, 0])
        grp_braid_box = VGroup(box_braid, t_braid_h, hose_body_b, mesh_braid, t_braid_sub)

        # Right: Spiral plies (parallel diagonal, NO criss-cross)
        box_spiral = RoundedRectangle(corner_radius=0.12, width=5.6, height=3.0, color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([3.3, y_comp, 0])
        t_spiral_h = Text("ลวดพันเกลียว (Spiral Plies — R9-R12)", font_size=13, color=COL_CURR).move_to([3.3, y_comp + 1.15, 0])
        hose_body_s = Rectangle(width=4.4, height=1.2, color=COL_CURR, fill_color="#263238").set_fill("#263238", 0.9).move_to([3.3, y_comp + 0.15, 0])
        spiral_lines_single = self.make_spiral_pattern(1.1, 5.5, y_comp + 0.15 - 0.6, y_comp + 0.15 + 0.6, color=COL_CURR, spacing=0.24, stroke_width=2.2, direction="right")
        t_s1 = Text("• เส้นลวดขนานเรียงตัวแน่นในทิศทางเดียว (Parallel)", font_size=10.5, color=WHITE)
        t_s2 = Text("• ไม่มีจุดตัดขัดกัน จึงทนแรงกระแทกและแรงดันสูงจัดได้ดี", font_size=10.5, color=WHITE)
        t_spiral_sub = VGroup(t_s1, t_s2).arrange(DOWN, buff=0.10, aligned_edge=LEFT).move_to([3.3, y_comp - 0.85, 0])
        grp_spiral_box = VGroup(box_spiral, t_spiral_h, hose_body_s, spiral_lines_single, t_spiral_sub)

        self.play(FadeIn(grp_braid_box, shift=UP * 0.25), FadeIn(grp_spiral_box, shift=UP * 0.25), run_time=1.0)
        self.play(Indicate(spiral_lines_single, color=COL_WARN), run_time=0.8)
        self.wait(1.8)  # Checkpoint 15.0s

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 17.8–23.0: Animated Proof Part 1 — Single-Direction Spiral Twist (§32)
        # ----------------------------------------------------------------------
        cap4 = caption_top("⚠️ ปัญหา: พันทิศเดียวหมด สายจะบิดเอง (Twisting Issue)")
        sub4 = Text(
            "ความดันสูงดันผนังท่อออก → เส้นลวดเฉียงทิศเดียวเกิดแรงดึง → สร้างแรงบิดสุทธิหมุนรอบแกน",
            font_size=11, color=COL_WARN
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap4, shift=UP * 0.3), FadeIn(sub4), run_time=0.8)

        y_h = -0.20
        # Left fixed anchor
        anchor_rect = Rectangle(width=0.6, height=1.8, color=COL_METAL, fill_color="#37474F").set_fill("#37474F", 0.95).move_to([-3.7, y_h, 0])
        t_anchor = Text("ยึดแน่นคงที่", font_size=10, color=COL_GRAY).next_to(anchor_rect, DOWN, buff=0.15)

        # Hose body with single-direction spiral
        hose_tube_single = Rectangle(width=5.8, height=1.2, color=COL_METAL, fill_color="#1E262C").set_fill("#1E262C", 0.9).move_to([-0.5, y_h, 0])
        wires_single = self.make_spiral_pattern(-3.4, 2.4, y_h - 0.6, y_h + 0.6, color=COL_METAL, spacing=0.25, stroke_width=2.0, direction="right")

        # Internal radial pressure outward arrows
        p_arr1 = Arrow(start=[-2.0, y_h, 0], end=[-2.0, y_h + 0.5, 0], color=COL_CURR, stroke_width=2.5, buff=0)
        p_arr2 = Arrow(start=[-2.0, y_h, 0], end=[-2.0, y_h - 0.5, 0], color=COL_CURR, stroke_width=2.5, buff=0)
        p_arr3 = Arrow(start=[0.5, y_h, 0], end=[0.5, y_h + 0.5, 0], color=COL_CURR, stroke_width=2.5, buff=0)
        p_arr4 = Arrow(start=[0.5, y_h, 0], end=[0.5, y_h - 0.5, 0], color=COL_CURR, stroke_width=2.5, buff=0)
        lbl_p_in = Text("ความดัน P ดันออกทุกทิศทาง", font_size=12, color=COL_CURR).move_to([-0.75, y_h, 0])
        grp_pressure = VGroup(p_arr1, p_arr2, p_arr3, p_arr4, lbl_p_in)

        # Right rotatable fitting end (for measuring rotation angle)
        center_fitting = np.array([2.7, y_h, 0])
        flange_base = Rectangle(width=0.6, height=1.5, color=COL_METAL, fill_color="#455A64").set_fill("#455A64", 0.95).move_to(center_fitting)
        flange_ring = Circle(radius=0.65, color=WHITE, stroke_width=2.0).move_to(center_fitting)
        # Orientation marker: arrow pointing initially UP (0 deg twist)
        pointer_line = Line(center_fitting, center_fitting + np.array([0, 0.65, 0]), color=COL_WARN, stroke_width=3.5)
        pointer_tip = Dot(center_fitting + np.array([0, 0.65, 0]), radius=0.08, color=COL_WARN)
        lbl_pointer = Text("มาร์กเกอร์ (0°)", font_size=11, color=WHITE).next_to(flange_ring, RIGHT, buff=0.25)
        fitting_end = VGroup(flange_base, flange_ring, pointer_line, pointer_tip, lbl_pointer)

        # Curved net torque arrow on the hose body (centered at x = -0.5)
        arc_tau = Arc(radius=0.9, start_angle=-PI/3, angle=2*PI/3, color=COL_WARN, stroke_width=3.5, arc_center=[-0.5, y_h, 0])
        arc_tau.add_tip(tip_length=0.22)
        lbl_tau = Text("แรงบิดสุทธิ (Net Torque τ)", font_size=12, color=COL_WARN).next_to(arc_tau, UP, buff=0.15)

        self.play(
            FadeIn(anchor_rect), FadeIn(t_anchor),
            FadeIn(hose_tube_single), FadeIn(wires_single),
            FadeIn(grp_pressure),
            FadeIn(fitting_end),
            run_time=1.0
        )
        self.wait(0.5)  # t ~ 19.5s: orientation is 0°

        # Rotation animation: fitting end rotates PI/3 (60 degrees) under net torque!
        lbl_pointer_twisted = Text("บิดหมุน (+60°)", font_size=11, color=COL_WARN).next_to(flange_ring, RIGHT, buff=0.25)

        banner_twist = Text(
            "⚠️ ปลายสายบิดหมุนรอบแกน (Twist) → เกิดความเค้นเฉือน ข้อต่อคลายหลุด สายแตกระเบิด!",
            font_size=12, color=COL_WARN
        ).move_to([0, -2.45, 0])
        box_banner_tw = SurroundingRectangle(banner_twist, color=COL_WARN, buff=0.12, corner_radius=0.08)

        self.play(
            Create(arc_tau), FadeIn(lbl_tau),
            Rotating(VGroup(flange_base, flange_ring, pointer_line, pointer_tip), angle=PI/3, about_point=center_fitting, run_time=1.6),
            Transform(lbl_pointer, lbl_pointer_twisted),
            FadeIn(banner_twist, shift=UP * 0.2), Create(box_banner_tw),
            run_time=1.6
        )
        self.wait(1.2)  # t ~ 21.5s: rotated by 60° (Checkpoint 20.5s check)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 23.8–29.0: Animated Proof Part 2 — Alternating Layers Torque Cancellation (§32)
        # ----------------------------------------------------------------------
        cap5 = caption_top("ทางแก้: พันสลับทิศทุกชั้น (Alternating Directions)")
        sub5 = Text(
            "พันชั้นที่ 1 เฉียงซ้าย + ชั้นที่ 2 เฉียงขวา → แรงบิดหักล้างกันพอดี (Torque Cancellation)",
            font_size=11, color=COL_OK
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap5, shift=UP * 0.3), FadeIn(sub5), run_time=0.8)

        # Dual alternating layers in the SAME frame (§41 high-risk visual distinction!)
        y_alt = -0.15
        # Left layer (Layer 1): Slanted LEFT in COL_METAL
        box_lay1 = Rectangle(width=3.2, height=1.4, color=COL_METAL, fill_color="#1E262C").set_fill("#1E262C", 0.9).move_to([-2.0, y_alt, 0])
        wires_lay1 = self.make_spiral_pattern(-3.6, -0.4, y_alt - 0.7, y_alt + 0.7, color=COL_METAL, spacing=0.22, stroke_width=2.2, direction="left")
        lbl_lay1 = Text("ชั้นที่ 1: เฉียงซ้าย (Lay 1)", font_size=12, color=COL_METAL).next_to(box_lay1, UP, buff=0.18)

        # Right layer (Layer 2): Slanted RIGHT in COL_CURR
        box_lay2 = Rectangle(width=3.2, height=1.4, color=COL_CURR, fill_color="#1E262C").set_fill("#1E262C", 0.9).move_to([1.6, y_alt, 0])
        wires_lay2 = self.make_spiral_pattern(0.0, 3.2, y_alt - 0.7, y_alt + 0.7, color=COL_CURR, spacing=0.22, stroke_width=2.2, direction="right")
        lbl_lay2 = Text("ชั้นที่ 2: เฉียงขวา (Lay 2)", font_size=12, color=COL_CURR).next_to(box_lay2, UP, buff=0.18)

        # Two opposing torque curved arrows (radius 0.55 inside spiral window to ensure clean separation)
        tau1_arc = Arc(radius=0.55, start_angle=PI/6, angle=4*PI/3, color=COL_METAL, stroke_width=3.2, arc_center=[-2.0, y_alt, 0])
        tau1_arc.add_tip(tip_length=0.18)
        lbl_tau1 = Text("τ₁ (ทิศตามเข็ม)", font_size=11, color=COL_METAL).next_to(box_lay1, DOWN, buff=0.25)

        tau2_arc = Arc(radius=0.55, start_angle=7*PI/6, angle=4*PI/3, color=COL_CURR, stroke_width=3.2, arc_center=[1.6, y_alt, 0])
        tau2_arc.add_tip(tip_length=0.18)
        lbl_tau2 = Text("τ₂ (ทิศทวนเข็ม)", font_size=11, color=COL_CURR).next_to(box_lay2, DOWN, buff=0.25)

        # Stable fitting end at x = 3.6 (rock solid, 0° twist!)
        c_fit_stable = np.array([3.6, y_alt, 0])
        flange_stable = Rectangle(width=0.5, height=1.5, color=COL_OK, fill_color="#37474F").set_fill("#37474F", 0.95).move_to(c_fit_stable)
        ring_stable = Circle(radius=0.65, color=COL_OK, stroke_width=2.0).move_to(c_fit_stable)
        p_line_stable = Line(c_fit_stable, c_fit_stable + np.array([0, 0.65, 0]), color=COL_OK, stroke_width=3.5)
        p_dot_stable = Dot(c_fit_stable + np.array([0, 0.65, 0]), radius=0.08, color=COL_OK)
        lbl_stable = Text("ตรงนิ่ง (0°)", font_size=11, color=COL_OK).next_to(ring_stable, RIGHT, buff=0.20)
        grp_stable_fit = VGroup(flange_stable, ring_stable, p_line_stable, p_dot_stable, lbl_stable)

        self.play(
            FadeIn(VGroup(box_lay1, wires_lay1, lbl_lay1)),
            FadeIn(VGroup(box_lay2, wires_lay2, lbl_lay2)),
            FadeIn(VGroup(tau1_arc, lbl_tau1)),
            FadeIn(VGroup(tau2_arc, lbl_tau2)),
            FadeIn(grp_stable_fit),
            run_time=1.2
        )
        self.wait(1.0)  # Checkpoint 27.0s before cancellation (both opposite slant layers visible!)

        # Torque cancellation: tau1 and tau2 merge and cancel into net torque = 0
        eq_cancel = Text("Σ τ = τ₁ + (-τ₂) = 0  →  สมดุลแรงบิดสมบูรณ์ สายไม่บิดตัว", font_size=14, color=COL_OK).move_to([0, -1.75, 0])
        box_eq = SurroundingRectangle(eq_cancel, color=COL_OK, buff=0.25, corner_radius=0.1)

        banner_cancel = Text(
            "✅ หลักการเดียวกับการพันลวดสลิง: สลับทิศทางในแต่ละชั้นเพื่อกำจัดแรงบิดสุทธิ",
            font_size=11, color=WHITE
        ).move_to([0, -2.55, 0])

        self.play(
            FadeOut(VGroup(tau1_arc, lbl_tau1, tau2_arc, lbl_tau2)),
            FadeIn(eq_cancel, shift=UP * 0.15), Create(box_eq),
            FadeIn(banner_cancel, shift=UP * 0.15),
            run_time=1.2
        )
        self.play(Indicate(box_eq, color=COL_OK), run_time=0.8)
        self.wait(1.2)  # Checkpoint 27.0s after cancellation

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 29.8–35.0: R9 vs R10 vs R11 Specification Matrix
        # ----------------------------------------------------------------------
        cap6 = caption_top("R9 → R10 → R11: เพิ่มชั้น/ความหนา = ทนแรงดันสูงขึ้น")
        sub6 = Text(
            "ตระกูลลวดพันเกลียว (Spiral Plies): ยิ่งเพิ่มจำนวนชั้น + ลวดหนาขึ้น = รับความดันใช้งานได้สูงขึ้น",
            font_size=11, color=COL_GRAY
        ).move_to([0, 2.15, 0])
        self.play(FadeIn(cap6, shift=UP * 0.3), FadeIn(sub6), run_time=0.8)

        # Matrix card with 3 rows
        card_matrix = RoundedRectangle(corner_radius=0.15, width=11.6, height=3.6, color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.30, 0])
        h_mat = Text("ตารางเปรียบเทียบมาตรฐานสายไฮดรอลิกลวดพันเกลียว (SAE 100R9 – R11)", font_size=14, color=COL_OK).move_to([0, 1.15, 0])
        div_mat = Line([-5.4, 0.90, 0], [5.4, 0.90, 0], color=COL_METAL, stroke_width=1.2)

        # Row 1: R9
        r9_tag = Text("SAE 100R9", font_size=13, color=WHITE).move_to([-4.2, 0.45, 0])
        r9_desc = Text("4 ชั้นลวดเกลียว (4-Spiral Plies) — ขนาดลวดปกติ (Normal Wire)", font_size=11, color=COL_GRAY).move_to([0.2, 0.45, 0])
        r9_pres = Text("แรงดันสูง (~200–300 bar)", font_size=11, color=COL_METAL).move_to([4.3, 0.45, 0])
        row_r9 = VGroup(r9_tag, r9_desc, r9_pres)

        # Row 2: R10
        r10_tag = Text("SAE 100R10", font_size=13, color=COL_CURR).move_to([-4.2, -0.10, 0])
        r10_desc = Text("4 ชั้นลวดเกลียว (4-Spiral Plies) — ลวดหนาพิเศษ (Heavy Wire)", font_size=11, color=WHITE).move_to([0.2, -0.10, 0])
        r10_pres = Text("แรงดันสูงมาก (~250–350 bar)", font_size=11, color=COL_CURR).move_to([4.3, -0.10, 0])
        row_r10 = VGroup(r10_tag, r10_desc, r10_pres)

        # Row 3: R11
        r11_tag = Text("SAE 100R11", font_size=13, color=COL_WARN).move_to([-4.2, -0.65, 0])
        r11_desc = Text("6 ชั้นลวดเกลียว (6-Spiral Plies) — ลวดหนาพิเศษ (Heavy Wire)", font_size=11, color=WHITE).move_to([0.2, -0.65, 0])
        r11_pres = Text("แรงดันสูงสุด (~350–500 bar)", font_size=11, color=COL_WARN).move_to([4.3, -0.65, 0])
        row_r11 = VGroup(r11_tag, r11_desc, r11_pres)

        bot_note = Text(
            "*หมายเหตุ: SAE 100R12 คล้าย R10 (4 ชั้นลวดหนา) แต่ปรับปรุงรัศมีดัดโค้งและตำแหน่งชั้นเสริม",
            font_size=10, color=COL_GRAY
        ).move_to([0, -1.35, 0])

        grp_mat = VGroup(card_matrix, h_mat, div_mat, row_r9, row_r10, row_r11, bot_note)
        self.play(FadeIn(grp_mat, shift=UP * 0.25), run_time=1.0)
        self.play(Indicate(row_r11, color=COL_WARN), run_time=0.8)
        self.wait(1.8)  # Checkpoint 33.0s

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 35.8–40.0: Summary Card
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(
            corner_radius=0.15, width=11.4, height=3.5,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.25, 0])

        s_head = Text("สรุปสำคัญ: สายไฮดรอลิกยืดหยุ่น (hydraulic06 น.13)", font_size=16, color=COL_OK).move_to([0, 1.15, 0])
        s1 = Text("1. SAE 100R6: ผ้าถัก 1 ชั้น (Textile Braid) สำหรับระบบไหลกลับ / ความดันต่ำ", font_size=12, color=WHITE).move_to([0, 0.60, 0])
        s2 = Text("2. SAE 100R7/R8: ท่อในเทอร์โมพลาสติก (Thermoplastic) ทนสารเคมีและของเหลวสังเคราะห์ได้ดี", font_size=12, color=WHITE).move_to([0, 0.15, 0])
        s3 = Text("3. SAE 100R9–R12: ลวดพันเกลียว (Spiral Plies) ลวดขนานทิศเดียว รับแรงกระแทกและความดันสูงจัด", font_size=12, color=WHITE).move_to([0, -0.30, 0])
        s4 = Text("4. ทำไมต้องพันสลับทิศ: หักล้างแรงบิด (Torque Cancellation) ป้องกันสายบิดหมุนเกลียว (Twist) ตอนรับแรงดัน", font_size=12, color=COL_CURR).move_to([0, -0.75, 0])
        s5 = Text("5. ยิ่งเพิ่มจำนวนชั้น (4 → 6 ชั้น) และความหนาลวด (Heavy Wire) ยิ่งรับความดันใช้งานได้สูงขึ้น", font_size=12, color=COL_OK).move_to([0, -1.20, 0])

        sum_grp = VGroup(sum_box, s_head, s1, s2, s3, s4, s5)
        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(3.4)  # Checkpoint 38.0s

        self.clear_stage(run_time=0.5)

        # ----------------------------------------------------------------------
        # BEAT 40.0–44.0: Review Question Card & Outro
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(
            corner_radius=0.15, width=11.2, height=2.6,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text(
            "ถ้าลวดทุกชั้นของสายไฮดรอลิกพันไปในทิศทางเดียวกันหมด (ไม่สลับทิศ) จะเกิดอะไรขึ้นตอนใช้งานจริง?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.05, 0.0])
        q_ans = Text(
            "(คำตอบ: เมื่อความดันภายในสูงขึ้น ลวดจะสร้างแรงบิดสุทธิหมุนรอบแกน ทำให้สายบิดตัว (Twist/Corkscrew) ข้อต่อคลาย หรือสายฉีกขาดได้)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.65, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)
        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)  # Checkpoint 42.0s

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)
        self.wait(0.5)


# ==============================================================================
# SCENE 11: H6_11_HoseSizeFittings (hydraulic06.pdf page 14)
# Duration: ~39.2 seconds | 2D SafeScene
# Pedagogical Focus: Hose Minimum Bend Radius (R_min) & Verified Slide Table Specs
# AHA Moment: Hoses cannot be bent arbitrarily tight. Over-bending causes outer wire mesh rupture
#             and inner flow throat pinch. Double-wire braid has thicker walls and is stiffer,
#             requiring ~45% LARGER minimum bend radius than single-wire braid (9-1/2" vs 6-9/16").
# Animated Mechanism:
#   - Beat 5.2-11.0s: Normal bend hose (R >= R_min) -> acute over-bent kink (R < R_min).
#   - High-Risk Check (§41/§44, t=8.5s): Visibly ruptured wire mesh with jagged fragments + pinched throat (0.5 down to 0.12).
#   - Beat 11.0-17.2s: Table card with verified Slide 14 values for Size 12 (3/4" OD tube).
#   - Beat 17.2-23.2s: Side-by-side bend comparison (Single Braid R=6-9/16" vs Double Braid R=9-1/2").
#   - Beat 23.2-29.2s: 3 Standard fitting angles (Straight, 45° Elbow, 90° Elbow) to eliminate hose over-bending.
#   - Beat 29.2-39.2s: Summary & Review Question cards.
# ==============================================================================
class H6_11_HoseSizeFittings(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [m for m in self.mobjects if m not in (self.title_m, self.ref_m)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Persistent Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = title("ไซส์สายและรัศมีดัดโค้งขั้นต่ำ")
        self.ref_m = page_ref("hydraulic06 น.14")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.5)
        self.wait(0.5)  # Checkpoint 1.5s - 2.0s

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.2: Hook Question
        # ----------------------------------------------------------------------
        hook_q = caption_top("สายยืดหยุ่นดัดโค้งได้ — ดัดแคบแค่ไหนก็ได้จริงไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=1.0)
        self.wait(1.6)  # Checkpoint 3.6s
        self.play(FadeOut(hook_q), run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 5.2–11.0: Over-Bent Hose Damage & Flow Pinch Mechanism (§41/§44)
        # ----------------------------------------------------------------------
        cap1 = caption_top("ดัดแคบเกินไป — ชั้นเสริมแรงเสียหายและรูในตีบแคบ")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.6)

        # Normal Bend Hose (Safe state)
        c_norm = [0.0, 0.10, 0.0]
        r_out = 1.95
        r_wire = 1.83
        r_fluid = 1.55
        r_in = 1.25

        arc_out_norm = Arc(radius=r_out, start_angle=PI, angle=-PI, arc_center=c_norm, stroke_color="#334155", stroke_width=6)
        arc_wire_norm = Arc(radius=r_wire, start_angle=PI, angle=-PI, arc_center=c_norm, stroke_color=COL_METAL, stroke_width=3)
        arc_fluid_norm = Arc(radius=r_fluid, start_angle=PI, angle=-PI, arc_center=c_norm, stroke_color="#0284C7", stroke_width=22)
        arc_in_norm = Arc(radius=r_in, start_angle=PI, angle=-PI, arc_center=c_norm, stroke_color="#334155", stroke_width=6)

        # Stems extending down
        y_bot = -1.35
        stem_l_out = Line([-r_out, c_norm[1], 0], [-r_out, y_bot, 0], stroke_color="#334155", stroke_width=6)
        stem_l_wire = Line([-r_wire, c_norm[1], 0], [-r_wire, y_bot, 0], stroke_color=COL_METAL, stroke_width=3)
        stem_l_fluid = Line([-r_fluid, c_norm[1], 0], [-r_fluid, y_bot, 0], stroke_color="#0284C7", stroke_width=22)
        stem_l_in = Line([-r_in, c_norm[1], 0], [-r_in, y_bot, 0], stroke_color="#334155", stroke_width=6)

        stem_r_in = Line([r_in, c_norm[1], 0], [r_in, y_bot, 0], stroke_color="#334155", stroke_width=6)
        stem_r_fluid = Line([r_fluid, c_norm[1], 0], [r_fluid, y_bot, 0], stroke_color="#0284C7", stroke_width=22)
        stem_r_wire = Line([r_wire, c_norm[1], 0], [r_wire, y_bot, 0], stroke_color=COL_METAL, stroke_width=3)
        stem_r_out = Line([r_out, c_norm[1], 0], [r_out, y_bot, 0], stroke_color="#334155", stroke_width=6)

        crimp_l = Rectangle(width=0.75, height=0.35, color=COL_GRAY, fill_color="#475569", fill_opacity=0.9).move_to([-r_fluid, y_bot + 0.15, 0])
        crimp_r = Rectangle(width=0.75, height=0.35, color=COL_GRAY, fill_color="#475569", fill_opacity=0.9).move_to([r_fluid, y_bot + 0.15, 0])

        r_dot = Dot(c_norm, color=COL_OK, radius=0.06)
        r_arr = Arrow(start=c_norm, end=[c_norm[0] + 0.85, c_norm[1], 0], color=COL_OK, buff=0, stroke_width=2.5)
        r_lbl = Text("R ≥ R_min (ปลอดภัย)", font_size=12, color=COL_OK).move_to([c_norm[0] + 0.50, c_norm[1] + 0.30, 0])

        badge_norm = VGroup(
            RoundedRectangle(width=8.0, height=0.55, corner_radius=0.1, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.92).move_to([0.0, -1.75, 0.0]),
            Text("✅ รัศมีดัดโค้งปกติ: ลวดเสริมแรงไม่ล้า รูในกลมสม่ำเสมอ ของไหลไหลสะดวก", font_size=13, color=COL_OK).move_to([0.0, -1.75, 0.0])
        )

        normal_hose_grp = VGroup(
            arc_out_norm, arc_wire_norm, arc_fluid_norm, arc_in_norm,
            stem_l_out, stem_l_wire, stem_l_fluid, stem_l_in,
            stem_r_in, stem_r_fluid, stem_r_wire, stem_r_out,
            crimp_l, crimp_r, r_dot, r_arr, r_lbl, badge_norm
        )

        self.play(FadeIn(normal_hose_grp, shift=UP * 0.25), run_time=1.0)
        self.wait(0.8)

        # Over-Bent Kink Hose with Severe Visible Damage (§41/§44)
        p_apex_out_l = np.array([-0.32, 0.68, 0])
        p_apex_out_r = np.array([0.32, 0.68, 0])
        p_crease_in = np.array([0.0, 0.55, 0])

        # 1. Outer rubber walls (thick dark jacket #334155, stroke 6)
        ob_l_out = Line([-0.90, y_bot, 0], p_apex_out_l, stroke_color="#334155", stroke_width=6)
        ob_r_out = Line([0.90, y_bot, 0], p_apex_out_r, stroke_color="#334155", stroke_width=6)

        # Torn rubber jacket jagged edges (dark outer cover torn apart)
        tear_l_jacket = VMobject(stroke_color="#334155", stroke_width=6).set_points_as_corners([
            p_apex_out_l, [-0.28, 0.82, 0], [-0.24, 0.76, 0], [-0.18, 0.90, 0]
        ])
        tear_r_jacket = VMobject(stroke_color="#334155", stroke_width=6).set_points_as_corners([
            p_apex_out_r, [0.28, 0.82, 0], [0.24, 0.76, 0], [0.18, 0.90, 0]
        ])

        # Outer rubber jagged rupture crack lines (RED zigzag lightning with clear 0.36 GAP in middle)
        crack_l = VMobject(stroke_color=RED, stroke_width=4).set_points_as_corners([
            [-0.34, 0.66, 0], [-0.28, 0.84, 0], [-0.23, 0.77, 0], [-0.18, 0.92, 0], [-0.12, 0.82, 0]
        ])
        crack_r = VMobject(stroke_color=RED, stroke_width=4).set_points_as_corners([
            [0.34, 0.66, 0], [0.28, 0.84, 0], [0.23, 0.77, 0], [0.18, 0.92, 0], [0.12, 0.82, 0]
        ])

        # 2. Wire braid with frayed / jagged broken tips at the damage point (COL_METAL, stroke 3.5)
        wire_l_stem = Line([-0.80, y_bot, 0], [-0.26, 0.62, 0], stroke_color=COL_METAL, stroke_width=3.5)
        wire_l_strand1 = VMobject(stroke_color=COL_METAL, stroke_width=3.5).set_points_as_corners([
            [-0.26, 0.62, 0], [-0.20, 0.80, 0], [-0.15, 0.98, 0], [-0.10, 1.05, 0]
        ])
        wire_l_strand2 = VMobject(stroke_color=COL_METAL, stroke_width=3).set_points_as_corners([
            [-0.26, 0.62, 0], [-0.15, 0.72, 0], [-0.09, 0.80, 0], [-0.04, 0.77, 0]
        ])
        wire_l_strand3 = VMobject(stroke_color=COL_METAL, stroke_width=3).set_points_as_corners([
            [-0.26, 0.62, 0], [-0.20, 0.68, 0], [-0.14, 0.64, 0]
        ])
        ob_l_wire = VGroup(wire_l_stem, wire_l_strand1, wire_l_strand2, wire_l_strand3)

        wire_r_stem = Line([0.80, y_bot, 0], [0.26, 0.62, 0], stroke_color=COL_METAL, stroke_width=3.5)
        wire_r_strand1 = VMobject(stroke_color=COL_METAL, stroke_width=3.5).set_points_as_corners([
            [0.26, 0.62, 0], [0.20, 0.80, 0], [0.15, 0.98, 0], [0.10, 1.05, 0]
        ])
        wire_r_strand2 = VMobject(stroke_color=COL_METAL, stroke_width=3).set_points_as_corners([
            [0.26, 0.62, 0], [0.15, 0.72, 0], [0.09, 0.80, 0], [0.04, 0.77, 0]
        ])
        wire_r_strand3 = VMobject(stroke_color=COL_METAL, stroke_width=3).set_points_as_corners([
            [0.26, 0.62, 0], [0.20, 0.68, 0], [0.14, 0.64, 0]
        ])
        ob_r_wire = VGroup(wire_r_stem, wire_r_strand1, wire_r_strand2, wire_r_strand3)

        # Snapped wire flying shards hovering in the rupture gap
        shard1 = Line([-0.05, 0.90, 0], [-0.01, 0.96, 0], color=COL_METAL, stroke_width=3)
        shard2 = Line([0.02, 0.86, 0], [0.06, 0.93, 0], color="#F59E0B", stroke_width=3)
        spark1 = Dot([-0.10, 1.05, 0], radius=0.04, color="#FEF08A")
        spark2 = Dot([0.10, 1.05, 0], radius=0.04, color="#FEF08A")
        spark3 = Dot([-0.04, 0.77, 0], radius=0.035, color="#FEF08A")
        spark4 = Dot([0.04, 0.77, 0], radius=0.035, color="#FEF08A")

        rupture_grp = VGroup(
            tear_l_jacket, tear_r_jacket, crack_l, crack_r,
            shard1, shard2, spark1, spark2, spark3, spark4
        )

        # 3. Inner wall creasing sharply upward
        ob_l_in = Line([-0.42, y_bot, 0], p_crease_in, stroke_color="#334155", stroke_width=6)
        ob_r_in = Line([0.42, y_bot, 0], p_crease_in, stroke_color="#334155", stroke_width=6)

        # 4. Fluid channel: healthy wide channel (width 22), taper, and severely choked warning throat
        ob_l_fluid_main = Line([-0.62, y_bot, 0], [-0.38, 0.20, 0], stroke_color="#0284C7", stroke_width=22)
        ob_l_fluid_taper = Line([-0.38, 0.20, 0], [-0.20, 0.55, 0], stroke_color="#0284C7", stroke_width=13)
        ob_l_fluid = VGroup(ob_l_fluid_main, ob_l_fluid_taper)

        ob_r_fluid_main = Line([0.62, y_bot, 0], [0.38, 0.20, 0], stroke_color="#0284C7", stroke_width=22)
        ob_r_fluid_taper = Line([0.38, 0.20, 0], [0.20, 0.55, 0], stroke_color="#0284C7", stroke_width=13)
        ob_r_fluid = VGroup(ob_r_fluid_main, ob_r_fluid_taper)

        # Choked throat (severely pinched to width 4 in warning orange/red)
        ob_choke = VMobject(stroke_color="#F97316", stroke_width=4).set_points_as_corners([
            [-0.20, 0.55, 0], [-0.10, 0.62, 0], [0.0, 0.64, 0], [0.10, 0.62, 0], [0.20, 0.55, 0]
        ])

        # Squeeze force indicators directly on throat
        squeeze_top = Arrow(start=[0.0, 0.82, 0], end=[0.0, 0.68, 0], color=RED, buff=0, stroke_width=3, tip_length=0.14)
        squeeze_bot = Arrow(start=[0.0, 0.40, 0], end=[0.0, 0.52, 0], color=RED, buff=0, stroke_width=3, tip_length=0.14)
        squeeze_grp = VGroup(squeeze_top, squeeze_bot)

        # Direct geometry width-comparison indicators
        dim_norm_bar = Line([-0.90, -0.30, 0], [-0.90, -0.10, 0], color=COL_OK, stroke_width=2)
        tick_l1 = Line([-0.95, -0.30, 0], [-0.85, -0.30, 0], color=COL_OK, stroke_width=2)
        tick_l2 = Line([-0.95, -0.10, 0], [-0.85, -0.10, 0], color=COL_OK, stroke_width=2)
        lbl_norm = Text("ปกติ 100%", font_size=11, color=COL_OK).next_to(dim_norm_bar, LEFT, buff=0.08)
        dim_norm_grp = VGroup(dim_norm_bar, tick_l1, tick_l2, lbl_norm)

        dim_choke_bar = Line([0.42, 0.58, 0], [0.42, 0.68, 0], color="#F97316", stroke_width=2)
        tick_c1 = Line([0.38, 0.58, 0], [0.46, 0.58, 0], color="#F97316", stroke_width=2)
        tick_c2 = Line([0.38, 0.68, 0], [0.46, 0.68, 0], color="#F97316", stroke_width=2)
        lbl_choke = Text("ตีบตัน ~20%", font_size=11, color="#F97316").next_to(VGroup(dim_choke_bar, tick_c1, tick_c2), RIGHT, buff=0.12)
        dim_choke_grp = VGroup(dim_choke_bar, tick_c1, tick_c2, lbl_choke)

        # Crimps at bottom
        ob_crimp_l = Rectangle(width=0.75, height=0.35, color=COL_GRAY, fill_color="#475569", fill_opacity=0.9).move_to([-0.62, y_bot + 0.15, 0])
        ob_crimp_r = Rectangle(width=0.75, height=0.35, color=COL_GRAY, fill_color="#475569", fill_opacity=0.9).move_to([0.62, y_bot + 0.15, 0])

        # Callouts pointing to damage
        call_wire_txt = VGroup(
            Text("⚠️ ลวดเสริมแรงหักขาด / ฉีกขาด", font_size=13, color=COL_WARN),
            Text("(Wire Fatigue / Braid Rupture)", font_size=11, color=COL_GRAY)
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([3.45, 1.45, 0])
        call_wire_arr = Arrow(start=[2.0, 1.45, 0], end=[0.35, 0.98, 0], color=COL_WARN, buff=0.08, stroke_width=2.5, tip_length=0.18)
        call_wire = VGroup(call_wire_txt, call_wire_arr)

        call_pinch_txt = VGroup(
            Text("⚠️ รูในถูกบีบตีบแคบ (Flow Pinch)", font_size=13, color=COL_WARN),
            Text("(ทางไหลแคบลง 80% / ความดันตกฮวบ)", font_size=11, color=COL_GRAY)
        ).arrange(DOWN, buff=0.06, aligned_edge=RIGHT).move_to([-3.45, 0.45, 0])
        call_pinch_arr = Arrow(start=[-1.8, 0.45, 0], end=[-0.16, 0.64, 0], color=COL_WARN, buff=0.08, stroke_width=2.5, tip_length=0.18)
        call_pinch = VGroup(call_pinch_txt, call_pinch_arr)

        badge_danger = VGroup(
            RoundedRectangle(width=9.2, height=0.60, corner_radius=0.1, color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -1.75, 0.0]),
            Text("❌ ดัดแคบกว่า R_min: ลวดหักขาด + รูในตีบแคบ → เสี่ยงสายระเบิดและปั๊มพัง!", font_size=13, color=COL_WARN).move_to([0.0, -1.75, 0.0])
        )

        overbent_grp = VGroup(
            ob_l_out, ob_r_out, rupture_grp,
            ob_l_wire, ob_r_wire,
            ob_l_in, ob_r_in,
            ob_l_fluid, ob_r_fluid, ob_choke,
            squeeze_grp, dim_norm_grp, dim_choke_grp,
            ob_crimp_l, ob_crimp_r,
            call_wire, call_pinch, badge_danger
        )

        # Sequential fade to eliminate cross-fade badge text collision
        self.play(FadeOut(normal_hose_grp), run_time=0.4)
        self.play(FadeIn(overbent_grp, shift=DOWN * 0.1), run_time=0.8)
        self.play(Indicate(rupture_grp, color=RED, scale_factor=1.05), Indicate(ob_choke, color=COL_WARN, scale_factor=1.0), Indicate(squeeze_grp, color=RED, scale_factor=1.0), run_time=0.8)
        self.wait(1.5)  # Checkpoint 8.5s falls right here! Full damage visible!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 11.0–17.2: Verified Dimension Table (Slide Page 14)
        # ----------------------------------------------------------------------
        cap2 = caption_top("ตัวเลขจริง: Hose Size 12 (OD tube 3/4 นิ้ว) — hydraulic06 น.14")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.6)

        card_tab = RoundedRectangle(width=12.2, height=3.8, corner_radius=0.15, color=COL_METAL, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.30, 0])
        h_tab = Text("ตารางเปรียบเทียบสเปกสาย Hose Size 12 (ท่อ OD 3/4 นิ้ว) — hydraulic06 น.14", font_size=14, color=COL_OK).move_to([0, 1.25, 0])

        th_type = Text("ประเภทสาย (Type)", font_size=12, color=COL_GRAY).move_to([-4.4, 0.70, 0])
        th_id   = Text("รูใน (Hose ID)", font_size=12, color=COL_GRAY).move_to([-2.2, 0.70, 0])
        th_od   = Text("รูนอก (Hose OD)", font_size=12, color=COL_GRAY).move_to([-0.4, 0.70, 0])
        th_bend = Text("รัศมีดัดขั้นต่ำ (Min Bend)", font_size=12, color=COL_OK).move_to([1.9, 0.70, 0])
        th_note = Text("ผลต่อการติดตั้ง", font_size=12, color=COL_GRAY).move_to([4.4, 0.70, 0])
        div_th = Line([-5.8, 0.45, 0], [5.8, 0.45, 0], color=COL_METAL, stroke_width=1.2)

        # Row 1: Single-Wire Braid
        r1_type = Text("Single-Wire Braid\n(ลวดถัก 1 ชั้น)", font_size=12, color=COL_METAL).move_to([-4.4, 0.05, 0])
        r1_id   = Text("5/8 นิ้ว (15.9 mm)", font_size=12, color=WHITE).move_to([-2.2, 0.05, 0])
        r1_od   = Text("1-5/64 นิ้ว (27.4 mm)", font_size=12, color=WHITE).move_to([-0.4, 0.05, 0])
        r1_bend = Text("6-9/16 นิ้ว (167 mm)", font_size=13, color=COL_OK).move_to([1.9, 0.05, 0])
        r1_note = Text("โค้งแคบได้ดี\nประหยัดพื้นที่", font_size=11, color=COL_OK).move_to([4.4, 0.05, 0])
        div_r1  = Line([-5.8, -0.35, 0], [5.8, -0.35, 0], color=COL_METAL, stroke_width=0.8)
        row1_grp = VGroup(r1_type, r1_id, r1_od, r1_bend, r1_note)

        # Row 2: Double-Wire Braid
        r2_type = Text("Double-Wire Braid\n(ลวดถัก 2 ชั้น)", font_size=12, color=COL_WARN).move_to([-4.4, -0.75, 0])
        r2_id   = Text("3/4 นิ้ว (19.0 mm)", font_size=12, color=WHITE).move_to([-2.2, -0.75, 0])
        r2_od   = Text("1-1/4 นิ้ว (31.8 mm)", font_size=12, color=WHITE).move_to([-0.4, -0.75, 0])
        r2_bend = Text("9-1/2 นิ้ว (241 mm)", font_size=13, color=COL_WARN).move_to([1.9, -0.75, 0])
        r2_note = Text("ต้องเผื่อรัศมีกว้าง\n(+45% รัศมีเพิ่ม)", font_size=11, color=COL_WARN).move_to([4.4, -0.75, 0])
        row2_grp = VGroup(r2_type, r2_id, r2_od, r2_bend, r2_note)

        box_r1_bend = SurroundingRectangle(r1_bend, color=COL_OK, buff=0.1, corner_radius=0.08)
        box_r2_bend = SurroundingRectangle(r2_bend, color=COL_WARN, buff=0.1, corner_radius=0.08)

        div_r2  = Line([-5.8, -1.15, 0], [5.8, -1.15, 0], color=COL_METAL, stroke_width=0.8)
        tab_foot = Text("💡 ข้อสังเกตวิศวกรรม: ลวด 2 ชั้น ผนังหนาและแข็งกว่า (Stiffer) จึงต้องเผื่อรัศมีดัดโค้งกว้างกว่าถึง ~45%!", font_size=12, color=COL_CURR).move_to([0, -1.55, 0])

        grp_table = VGroup(card_tab, h_tab, th_type, th_id, th_od, th_bend, th_note, div_th, row1_grp, div_r1, row2_grp, div_r2, tab_foot)

        self.play(FadeIn(grp_table, shift=UP * 0.25), run_time=1.0)
        self.play(Create(box_r1_bend), run_time=0.6)
        self.play(Create(box_r2_bend), run_time=0.6)
        self.wait(2.2)  # Checkpoint 15.0s falls right here! Table specs clearly readable

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 17.2–23.2: Side-by-Side Bend Radius Comparison (1 vs 2 Braids)
        # ----------------------------------------------------------------------
        cap3 = caption_top("เชื่อมกับ H6_09/H6_10: ลวดเยอะ = แข็งกว่า = โค้งแคบไม่ได้เท่า")
        sub3 = Text("ไซส์เดียวกัน (Size 12): Single-Braid ดัดโค้งแคบได้ถึง 6-9/16\" ขณะที่ Double-Braid ต้องเผื่อถึง 9-1/2\"", font_size=12, color=COL_GRAY).move_to([0, 2.25, 0])
        self.play(FadeIn(cap3, shift=UP * 0.3), FadeIn(sub3), run_time=0.6)

        # Left Panel: Single-Wire Braid (Tighter loop R = 1.25)
        c_left = [-3.4, -0.40, 0]
        r_s_arc = 1.25
        arc_s_fluid = Arc(radius=r_s_arc, start_angle=PI, angle=-PI, arc_center=c_left, stroke_color="#0284C7", stroke_width=18)
        arc_s_wire = Arc(radius=r_s_arc + 0.16, start_angle=PI, angle=-PI, arc_center=c_left, stroke_color=COL_METAL, stroke_width=3)
        arc_s_out = Arc(radius=r_s_arc + 0.24, start_angle=PI, angle=-PI, arc_center=c_left, stroke_color="#334155", stroke_width=4)

        stem_s_l = Line([-3.4 - r_s_arc, c_left[1], 0], [-3.4 - r_s_arc, -1.05, 0], stroke_color="#0284C7", stroke_width=18)
        stem_s_r = Line([-3.4 + r_s_arc, c_left[1], 0], [-3.4 + r_s_arc, -1.05, 0], stroke_color="#0284C7", stroke_width=18)

        arr_s = Arrow(start=c_left, end=[-3.4, 0.15, 0], color=COL_OK, buff=0, stroke_width=2.2)
        lbl_s_r = Text("R = 6-9/16\" (167 mm)", font_size=10.5, color=COL_OK).move_to([-3.4, 0.40, 0])

        box_s = RoundedRectangle(width=5.4, height=1.2, corner_radius=0.1, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([-3.4, -1.65, 0])
        txt_s = VGroup(
            Text("Single-Wire Braid (ลวด 1 ชั้น)", font_size=13, color=COL_OK),
            Text("• รัศมีดัดขั้นต่ำ: 6-9/16 นิ้ว (167 mm)\n• โค้งได้แคบกว่า เหมาะกับพื้นที่จำกัดและช่องแคบ", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([-3.4, -1.65, 0])
        grp_s = VGroup(arc_s_fluid, arc_s_wire, arc_s_out, stem_s_l, stem_s_r, arr_s, lbl_s_r, box_s, txt_s)

        # Right Panel: Double-Wire Braid (Wider loop R = 1.75)
        c_right = [3.4, -0.40, 0]
        r_d_arc = 1.75
        arc_d_fluid = Arc(radius=r_d_arc, start_angle=PI, angle=-PI, arc_center=c_right, stroke_color="#0284C7", stroke_width=20)
        arc_d_wire1 = Arc(radius=r_d_arc + 0.16, start_angle=PI, angle=-PI, arc_center=c_right, stroke_color=COL_METAL, stroke_width=3)
        arc_d_wire2 = Arc(radius=r_d_arc + 0.25, start_angle=PI, angle=-PI, arc_center=c_right, stroke_color=COL_CURR, stroke_width=3)
        arc_d_out = Arc(radius=r_d_arc + 0.34, start_angle=PI, angle=-PI, arc_center=c_right, stroke_color="#334155", stroke_width=4)

        stem_d_l = Line([3.4 - r_d_arc, c_right[1], 0], [3.4 - r_d_arc, -1.05, 0], stroke_color="#0284C7", stroke_width=20)
        stem_d_r = Line([3.4 + r_d_arc, c_right[1], 0], [3.4 + r_d_arc, -1.05, 0], stroke_color="#0284C7", stroke_width=20)

        arr_d = Arrow(start=c_right, end=[3.4, 0.30, 0], color=COL_WARN, buff=0, stroke_width=2.2)
        lbl_d_r = Text("R = 9-1/2\" (241 mm)", font_size=10.5, color=COL_WARN).move_to([3.4, 0.65, 0])

        box_d = RoundedRectangle(width=5.4, height=1.2, corner_radius=0.1, color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([3.4, -1.65, 0])
        txt_d = VGroup(
            Text("Double-Wire Braid (ลวด 2 ชั้น)", font_size=13, color=COL_WARN),
            Text("• รัศมีดัดขั้นต่ำ: 9-1/2 นิ้ว (241 mm) — กว้างกว่า +45%!\n• แข็งแรงทนแรงดันสูง แต่กินพื้นที่ติดตั้งมากกว่า", font_size=11, color=WHITE)
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([3.4, -1.65, 0])
        grp_d = VGroup(arc_d_fluid, arc_d_wire1, arc_d_wire2, arc_d_out, stem_d_l, stem_d_r, arr_d, lbl_d_r, box_d, txt_d)

        self.play(FadeIn(grp_s, shift=RIGHT * 0.25), FadeIn(grp_d, shift=LEFT * 0.25), run_time=1.2)
        self.play(Indicate(lbl_s_r, color=COL_OK), Indicate(lbl_d_r, color=COL_WARN), run_time=0.8)
        self.wait(2.2)  # Checkpoint 21.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 23.2–29.2: 3 Standard Fitting Angles (Straight, 45°, 90° Elbow)
        # ----------------------------------------------------------------------
        cap4 = caption_top("ตัวอย่างข้อต่อสำเร็จรูป (Fittings) 3 แบบมาตรฐาน")
        sub4 = Text("เลือกมุมข้อต่อให้เหมาะกับทิศทางสาย — ลดจำนวนจุดโค้ง ป้องกันสายถูกดัดแคบเกินพิกัด", font_size=12, color=COL_GRAY).move_to([0, 2.15, 0])
        self.play(FadeIn(cap4, shift=UP * 0.3), FadeIn(sub4), run_time=0.6)

        # Panel 1: Straight (0°) at x = -4.3
        p1_base = Rectangle(width=1.8, height=0.30, color=COL_GRAY, fill_color="#1E293B", fill_opacity=0.9).move_to([-4.3, -0.70, 0])
        p1_fit = Rectangle(width=0.55, height=0.6, color=COL_METAL, fill_color="#64748B", fill_opacity=0.9).move_to([-4.3, -0.25, 0])
        p1_hose = Line([-4.3, 0.05, 0], [-4.3, 1.05, 0], color="#0284C7", stroke_width=16)
        p1_out_l = Line([-4.42, 0.05, 0], [-4.42, 1.05, 0], color="#334155", stroke_width=3)
        p1_out_r = Line([-4.18, 0.05, 0], [-4.18, 1.05, 0], color="#334155", stroke_width=3)
        p1_title = Text("1. ข้อต่อตรง (Straight / 0°)", font_size=13, color=COL_METAL).move_to([-4.3, 1.45, 0])
        p1_sub = Text("สำหรับทางเดินสายตรง\nต่อเข้าพอร์ตโดยตรง", font_size=11, color=COL_GRAY).move_to([-4.3, -1.15, 0])
        panel1 = VGroup(p1_base, p1_fit, p1_hose, p1_out_l, p1_out_r, p1_title, p1_sub)

        # Panel 2: 45° Elbow at x = 0.0
        p2_base = Rectangle(width=1.8, height=0.30, color=COL_GRAY, fill_color="#1E293B", fill_opacity=0.9).move_to([0.0, -0.70, 0])
        p2_fit_v = Rectangle(width=0.55, height=0.45, color=COL_FIELD, fill_color="#42A5F5", fill_opacity=0.85).move_to([0.0, -0.32, 0])
        p2_fit_elbow = Line([0.0, -0.10, 0], [0.35, 0.25, 0], color=COL_FIELD, stroke_width=16)
        p2_hose = Line([0.35, 0.25, 0], [1.05, 0.95, 0], color="#0284C7", stroke_width=16)
        p2_arc = Arc(radius=0.40, start_angle=PI/2, angle=-PI/4, arc_center=[0.0, -0.10, 0], color=COL_FIELD, stroke_width=2)
        p2_arc_lbl = Text("45°", font_size=11, color=COL_FIELD).move_to([0.35, 0.0, 0])
        p2_title = Text("2. ข้องอ 45° (45° Elbow)", font_size=13, color=COL_FIELD).move_to([0.0, 1.45, 0])
        p2_sub = Text("เปลี่ยนทิศทางเฉียง\nลดความเค้นดัดสาย", font_size=11, color=COL_GRAY).move_to([0.0, -1.15, 0])
        panel2 = VGroup(p2_base, p2_fit_v, p2_fit_elbow, p2_hose, p2_arc, p2_arc_lbl, p2_title, p2_sub)

        # Panel 3: 90° Elbow at x = +4.3
        p3_base = Rectangle(width=1.8, height=0.30, color=COL_GRAY, fill_color="#1E293B", fill_opacity=0.9).move_to([4.3, -0.70, 0])
        p3_fit_v = Rectangle(width=0.55, height=0.55, color=COL_OK, fill_color="#26C6DA", fill_opacity=0.85).move_to([4.3, -0.27, 0])
        p3_fit_h = Rectangle(width=0.55, height=0.55, color=COL_OK, fill_color="#26C6DA", fill_opacity=0.85).move_to([4.60, 0.0, 0])
        p3_hose = Line([4.88, 0.0, 0], [6.18, 0.0, 0], color="#0284C7", stroke_width=16)
        p3_out_t = Line([4.88, 0.12, 0], [6.18, 0.12, 0], color="#334155", stroke_width=3)
        p3_out_b = Line([4.88, -0.12, 0], [6.18, -0.12, 0], color="#334155", stroke_width=3)
        p3_corner = Square(side_length=0.22, color=COL_OK, stroke_width=1.5).move_to([4.19, 0.11, 0])
        p3_title = Text("3. ข้องอ 90° (90° Elbow)", font_size=13, color=COL_OK).move_to([4.3, 1.45, 0])
        p3_sub = Text("เลี้ยวฉากในตัวข้อต่อ\nสายไม่ต้องถูกดัดโค้ง!", font_size=11, color=COL_OK).move_to([4.3, -1.15, 0])
        panel3 = VGroup(p3_base, p3_fit_v, p3_fit_h, p3_hose, p3_out_t, p3_out_b, p3_corner, p3_title, p3_sub)

        fittings_banner = VGroup(
            RoundedRectangle(width=11.6, height=0.55, corner_radius=0.1, color=COL_CURR, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0, -1.75, 0]),
            Text("💡 การเลือกข้อต่อมุมที่ถูกต้อง ช่วยกำจัดการดัดสายที่แคบเกินพิกัด (เชื่อมโยง H6_12 การติดตั้งสาย)", font_size=12, color=COL_CURR).move_to([0, -1.75, 0])
        )

        fittings3 = [panel1, panel2, panel3]
        self.play(LaggedStart(*[FadeIn(fit, shift=UP * 0.2) for fit in fittings3], lag_ratio=0.35), FadeIn(fittings_banner), run_time=1.4)
        self.play(Indicate(p2_fit_elbow, color=COL_FIELD), Indicate(p3_fit_h, color=COL_OK), run_time=0.8)
        self.wait(2.0)  # Checkpoint 27.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 29.2–34.2: Summary Card
        # ----------------------------------------------------------------------
        sum_box = RoundedRectangle(
            corner_radius=0.15, width=11.6, height=3.6,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0, -0.25, 0])

        s_head = Text("สรุป: ไซส์สายและรัศมีดัดโค้งขั้นต่ำ (hydraulic06 น.14)", font_size=16, color=COL_OK).move_to([0, 1.20, 0])
        s1 = Text("1. รัศมีดัดโค้งขั้นต่ำ (Min Bend Radius: R_min): พิกัดสำคัญที่สุดในการติดตั้งสายไฮดรอลิก ห้ามดัดแคบกว่านี้", font_size=12.5, color=WHITE).move_to([0, 0.65, 0])
        s2 = Text("2. ผลเสียจากการดัดแคบเกินไป: ลวดถักล้าและฉีกขาด (Wire Fatigue/Rupture) และรูในถูกบีบตีบแคบ ขวางทางไหล", font_size=12.5, color=COL_WARN).move_to([0, 0.15, 0])
        s3 = Text("3. ตัวเลขจริง (Size 12): ลวด 1 ชั้น R_min = 6-9/16\" (167 mm) ส่วนลวด 2 ชั้น R_min = 9-1/2\" (241 mm, +45%)", font_size=12.5, color=COL_OK).move_to([0, -0.35, 0])
        s4 = Text("4. กฎฟิสิกส์: สายที่เสริมลวดมากขึ้นจะแข็งกว่า (Stiffer) จึงต้องเผื่อรัศมีดัดโค้งกว้างกว่าที่ไซส์เดียวกัน", font_size=12.5, color=WHITE).move_to([0, -0.85, 0])
        s5 = Text("5. ใช้ข้อต่อมุมสำเร็จรูป (Straight / 45° / 90° Elbow) ช่วยรับมุมเลี้ยว ป้องกันสายหักงอเกินพิกัด", font_size=12.5, color=COL_FIELD).move_to([0, -1.35, 0])

        sum_grp = VGroup(sum_box, s_head, s1, s2, s3, s4, s5)
        self.play(FadeIn(sum_grp, shift=UP * 0.35), run_time=0.8)
        self.wait(3.4)  # Checkpoint 32.0s falls right here!

        self.clear_stage(run_time=0.6)

        # ----------------------------------------------------------------------
        # BEAT 34.2–39.2: Review Question Card & Outro
        # ----------------------------------------------------------------------
        q_box = RoundedRectangle(
            corner_radius=0.15, width=11.2, height=2.6,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.35, 0.0])
        q_head = Text("คำถามทบทวนความเข้าใจ", font_size=18, color=COL_WARN).move_to([0.0, 0.50, 0.0])
        q_body = Text(
            "งานติดตั้งที่ต้องเดินสายผ่านช่องแคบมากๆ ซึ่งมีพื้นที่ดัดโค้งจำกัด\nควรเลือกใช้สาย Single-Wire Braid หรือ Double-Wire Braid?",
            font_size=13.5, color=WHITE
        ).move_to([0.0, 0.05, 0.0])
        q_ans = Text(
            "(คำตอบ: ควรเลือก Single-Wire Braid (หากความดันทนได้) เพราะมีรัศมีดัดโค้งขั้นต่ำแคบกว่าอย่างมาก\nตัวอย่าง Size 12: Single-Braid ดัดโค้งได้ถึง 6-9/16\" ขณะที่ Double-Braid ต้องเผื่อถึง 9-1/2\")",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.65, 0.0])

        q_grp = VGroup(q_box, q_head, q_body, q_ans)
        self.play(FadeIn(q_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)  # Checkpoint 36.0s falls right here!

        self.play(FadeOut(q_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)
        self.wait(0.5)


# ==============================================================================
# SCENE 12: H6_12_HoseInstallation (hydraulic06.pdf page 15)
# Duration: ~62.2 seconds | 2D SafeScene
# Pedagogical Focus: 6 Core Hose Installation Rules (Right vs Wrong)
# AHA Moment:
#   1. Routing: Use 90° elbow to eliminate meandering long runs & 4 kinks.
#   2. Heat: Avoid heat source (>100°C); use standoff clamps and thermal insulation sleeve.
#   3. Bend Radius: Keep R >= R_min; tight bends cause outer wire rupture and flow pinch.
#   4. Twisted Hose: 7" twist on large hose reduces pressure capability by up to 90%!
#   5. Movement Plane: Flexing must occur in same plane as bend to prevent neck twist.
#   6. Slack: Operating pressure changes length by +2% to -6%; adequate slack is mandatory.
# ==============================================================================

def _h6_12_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_12_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_12_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_12_badge(text, color):
    lbl = Text(text, font_size=11.5, color=color)
    bg = RoundedRectangle(width=lbl.width + 0.45, height=0.38, corner_radius=0.08, color=color, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_12_banner(text, color):
    bg = RoundedRectangle(width=11.8, height=0.55, corner_radius=0.1, color=color, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -1.85, 0.0])
    lbl = Text(text, font_size=12, color=color).move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_12_HoseInstallation(SafeScene):
    def clear_stage(self, run_time=0.5):
        """Fade out all scene mobjects except persistent header."""
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Persistent Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = _h6_12_title("ติดตั้งสายไฮดรอลิก: ถูก vs ผิด")
        self.ref_m = _h6_12_page_ref("hydraulic06 น.15")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)  # Checkpoint 1.5s

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.0: Hook Question
        # ----------------------------------------------------------------------
        hook_q = _h6_12_caption_top("เลือกสายถูกสเปคแล้ว ติดตั้งยังไงก็ได้เหมือนกันจริงไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)  # Checkpoint 3.6s
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 5.0–12.5: 1. Routing & Interference (เดินสายให้พอดี ไม่อ้อมเกะกะ)
        # ----------------------------------------------------------------------
        cap1 = _h6_12_caption_top("1. เดินสายให้พอดี ไม่อ้อมเกะกะ (Correct Routing)")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Obstacle
        obs_box = RoundedRectangle(width=1.6, height=2.2, corner_radius=0.1, color=COL_GRAY, fill_color="#334155", fill_opacity=0.9).move_to([0.0, 0.1, 0.0])
        obs_txt = Text("โครงเครื่องจักร\n(Obstacle)", font_size=11, color=COL_GRAY).move_to(obs_box.get_center())
        obstacle = VGroup(obs_box, obs_txt)

        port_a = Dot([-3.2, -0.8, 0.0], color=COL_METAL, radius=0.12)
        lbl_a = Text("Port A", font_size=10, color=COL_METAL).next_to(port_a, DOWN, buff=0.08)
        port_b = Dot([3.2, 0.9, 0.0], color=COL_METAL, radius=0.12)
        lbl_b = Text("Port B", font_size=10, color=COL_METAL).next_to(port_b, UP, buff=0.08)
        ports_grp = VGroup(obstacle, port_a, lbl_a, port_b, lbl_b)

        # Wrong 1: Meandering hose with 4 sharp kinks
        pts_w1 = [
            [-3.2, -0.8, 0], [-1.8, -0.8, 0], [-1.8, -1.25, 0],
            [1.8, -1.25, 0], [1.8, 0.9, 0], [3.2, 0.9, 0]
        ]
        hose_w1_out = VMobject(stroke_color="#334155", stroke_width=10).set_points_as_corners(pts_w1)
        hose_w1_in  = VMobject(stroke_color=COL_WARN, stroke_width=6).set_points_as_corners(pts_w1)
        badge_w1 = _h6_12_badge("✗ ผิด (อ้อมยาว 4 หักมุม)", COL_WARN).move_to([-1.8, 1.25, 0.0])
        call_w1 = Text("สายยาวเกะกะ + หักมุม 4 จุด → สั่นสะบัด/เสี่ยงถูกเกี่ยวขาด", font_size=11.5, color=COL_WARN).move_to([0.0, -1.45, 0.0])
        wrong1_grp = VGroup(ports_grp, hose_w1_out, hose_w1_in, badge_w1, call_w1)

        # Right 1: 90° elbow fitting, short direct clean L-run
        ports_grp_r = ports_grp.copy()
        pts_r1 = [
            [-3.2, -0.8, 0], [-3.2, 0.9, 0], [3.2, 0.9, 0]
        ]
        hose_r1_out = VMobject(stroke_color="#334155", stroke_width=10).set_points_as_corners(pts_r1)
        hose_r1_in  = VMobject(stroke_color=COL_OK, stroke_width=6).set_points_as_corners(pts_r1)
        elbow_fit = Square(side_length=0.32, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([-3.2, 0.9, 0.0])
        badge_r1 = _h6_12_badge("✓ ถูก (ใช้ข้อต่องอ 90°)", COL_OK).move_to([-1.8, 1.25, 0.0])
        call_r1 = Text("ใช้ข้อต่องอ 90° → สายสั้นกะทัดรัด ไม่เกะกะ ปลอดภัย", font_size=11.5, color=COL_OK).move_to([0.0, -1.45, 0.0])
        right1_grp = VGroup(ports_grp_r, hose_r1_out, hose_r1_in, elbow_fit, badge_r1, call_r1)

        banner1 = _h6_12_banner("ใช้ข้อต่องอลดความยาวส่วนเกิน ลดเสียดสี/กีดขวาง ซ่อมง่ายขึ้น", COL_OK)

        self.play(FadeIn(wrong1_grp, shift=RIGHT * 0.2), FadeIn(banner1), run_time=0.8)
        self.wait(1.2)  # Checkpoint 9.0s falls right here!
        self.play(FadeOut(wrong1_grp), run_time=0.4)
        self.play(FadeIn(right1_grp), run_time=0.6)
        self.wait(2.5)

        self.clear_stage(run_time=0.5)
        self.wait(0.1)

        # ----------------------------------------------------------------------
        # BEAT 13.1–20.0: 2. Heat Proximity (หลีกเลี่ยงผิวร้อน)
        # ----------------------------------------------------------------------
        cap2 = _h6_12_caption_top("2. หลีกเลี่ยงผิวร้อน (Avoid Heat Sources)")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Hot exhaust pipe on left side (x = -2.4)
        hot_pipe_body = RoundedRectangle(width=1.6, height=2.4, corner_radius=0.15, color="#F97316", fill_color="#EA580C", fill_opacity=0.85).move_to([-2.4, -0.15, 0.0])
        hot_pipe_txt  = Text("ท่อไอเสีย / ผิวร้อน\n(Heat Source > 100°C)", font_size=10.5, color="#FEF08A").next_to(hot_pipe_body, UP, buff=0.15)
        hot_pipe_inner = Text("120°C", font_size=13, color="#FEF08A").move_to([-2.4, -0.15, 0.0])
        hot_pipe_grp = VGroup(hot_pipe_body, hot_pipe_txt, hot_pipe_inner)

        # Wrong 2: Hose directly touching the hot pipe (contact gap = 0)
        hose_w2_out = Line([-1.55, -1.3, 0], [-1.55, 1.3, 0], stroke_color="#334155", stroke_width=10)
        hose_w2_in  = Line([-1.55, -1.3, 0], [-1.55, 1.3, 0], stroke_color=COL_WARN, stroke_width=6)
        contact_pt = Ellipse(width=0.25, height=1.2, color=RED, fill_color=RED, fill_opacity=0.45).move_to([-1.60, -0.15, 0.0])
        badge_w2 = _h6_12_badge("✗ ผิด (สัมผัสผิวร้อน)", COL_WARN).move_to([1.8, 1.15, 0.0])
        call_w2 = Text("⚠️ ระยะห่าง = 0 mm (แนบผิวร้อน) → ยางไหม้กรอบแตกลายงา ไส้แตก!", font_size=11.5, color=COL_WARN).move_to([1.8, 0.45, 0.0])
        wrong2_grp = VGroup(hot_pipe_grp, hose_w2_out, hose_w2_in, contact_pt, badge_w2, call_w2)

        # Right 2: Clamped away (wide air gap) + Thermal insulation sleeve
        hot_pipe_grp_r = hot_pipe_grp.copy()
        hose_r2_out = Line([0.8, -1.3, 0], [0.8, 1.3, 0], stroke_color="#334155", stroke_width=10)
        hose_r2_in  = Line([0.8, -1.3, 0], [0.8, 1.3, 0], stroke_color=COL_OK, stroke_width=6)
        clamp_bracket = Rectangle(width=0.45, height=0.25, color=COL_GRAY, fill_color="#475569", fill_opacity=1.0).move_to([0.8, -0.8, 0.0])
        sleeve = RoundedRectangle(width=0.45, height=1.7, corner_radius=0.08, color="#E2E8F0", fill_color="#94A3B8", fill_opacity=0.75).move_to([0.8, 0.1, 0.0])
        sleeve_lbl = Text("ปลอกฉนวนกันความร้อน\n(Insulation Sleeve)", font_size=10, color=WHITE).move_to([2.7, 0.1, 0.0])
        gap_dim = DoubleArrow([-1.60, -0.2, 0], [0.55, -0.2, 0], color=COL_OK, stroke_width=2)
        gap_lbl = Text("เว้นระยะห่างจากผิวร้อนชัดเจน", font_size=10, color=COL_OK).move_to([-0.5, 0.05, 0.0])
        badge_r2 = _h6_12_badge("✓ ถูก (เว้นระยะ + หุ้มฉนวน)", COL_OK).move_to([2.2, 1.15, 0.0])
        call_r2 = Text("✓ ดันสายห่างด้วยแคลมป์ + สวมปลอกฉนวนกันความร้อน", font_size=11.5, color=COL_OK).move_to([1.8, -1.35, 0.0])
        right2_grp = VGroup(hot_pipe_grp_r, hose_r2_out, hose_r2_in, clamp_bracket, sleeve, sleeve_lbl, gap_dim, gap_lbl, badge_r2, call_r2)

        banner2 = _h6_12_banner("ห้ามให้สายชิดผิวร้อน — ใช้แคลมป์ดันออกหรือหุ้มฉนวนกันความร้อนคั่นกลาง", COL_OK)

        self.play(FadeIn(wrong2_grp, shift=UP * 0.2), FadeIn(banner2), run_time=0.8)
        self.wait(1.2)  # Checkpoint 17.0s falls right here!
        self.play(FadeOut(wrong2_grp), run_time=0.4)
        self.play(FadeIn(right2_grp), run_time=0.6)
        self.wait(2.2)

        self.clear_stage(run_time=0.5)
        self.wait(0.1)

        # ----------------------------------------------------------------------
        # BEAT 20.6–29.0: 3. Bend Radius U-Loop (เผื่อรัศมีดัดโค้งให้พอ - เชื่อม H6_11)
        # ----------------------------------------------------------------------
        cap3 = _h6_12_caption_top("3. เผื่อรัศมีดัดโค้งให้พอ (ต่อจาก H6_11) — รัศมีแคบ vs กว้าง")
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        # Left Wrong U-Loop
        lw_arc_out = Arc(radius=0.40, start_angle=0, angle=PI, arc_center=[-3.2, 0.0, 0], stroke_color="#334155", stroke_width=10)
        lw_arc_in  = Arc(radius=0.40, start_angle=0, angle=PI, arc_center=[-3.2, 0.0, 0], stroke_color=COL_WARN, stroke_width=6)
        lw_stem_l = Line([-3.60, 0.0, 0], [-3.60, -1.15, 0], stroke_color="#334155", stroke_width=10)
        lw_stem_l_in = Line([-3.60, 0.0, 0], [-3.60, -1.15, 0], stroke_color=COL_WARN, stroke_width=6)
        lw_stem_r = Line([-2.80, 0.0, 0], [-2.80, -1.15, 0], stroke_color="#334155", stroke_width=10)
        lw_stem_r_in = Line([-2.80, 0.0, 0], [-2.80, -1.15, 0], stroke_color=COL_WARN, stroke_width=6)
        crimp_w1 = Rectangle(width=0.36, height=0.22, color=COL_GRAY, fill_color="#475569", fill_opacity=1.0).move_to([-3.60, -1.15, 0])
        crimp_w2 = Rectangle(width=0.36, height=0.22, color=COL_GRAY, fill_color="#475569", fill_opacity=1.0).move_to([-2.80, -1.15, 0])
        kink_mark = Text("⚡ จุดพับหักมุม", font_size=10, color=COL_WARN).next_to(lw_arc_out, UP, buff=0.08)
        r_dim_w = Text("R < R_min (แคบเกิน!)", font_size=10.5, color=COL_WARN).next_to(kink_mark, UP, buff=0.08)
        badge_w3 = _h6_12_badge("✗ ผิด (รัศมีแคบ)", COL_WARN).next_to(r_dim_w, UP, buff=0.10)
        call_w3 = Text("ลวดล้าหัก + รูในตีบแคบ", font_size=11, color=COL_WARN).move_to([-3.2, -1.35, 0.0])
        loop_wrong = VGroup(
            lw_arc_out, lw_arc_in, lw_stem_l, lw_stem_l_in, lw_stem_r, lw_stem_r_in,
            crimp_w1, crimp_w2, kink_mark, r_dim_w, badge_w3, call_w3
        )

        # Right Correct U-Loop
        lr_arc_out = Arc(radius=1.35, start_angle=0, angle=PI, arc_center=[3.2, -0.20, 0], stroke_color="#334155", stroke_width=10)
        lr_arc_in  = Arc(radius=1.35, start_angle=0, angle=PI, arc_center=[3.2, -0.20, 0], stroke_color=COL_OK, stroke_width=6)
        lr_stem_l = Line([1.85, -0.20, 0], [1.85, -1.15, 0], stroke_color="#334155", stroke_width=10)
        lr_stem_l_in = Line([1.85, -0.20, 0], [1.85, -1.15, 0], stroke_color=COL_OK, stroke_width=6)
        lr_stem_r = Line([4.55, -0.20, 0], [4.55, -1.15, 0], stroke_color="#334155", stroke_width=10)
        lr_stem_r_in = Line([4.55, -0.20, 0], [4.55, -1.15, 0], stroke_color=COL_OK, stroke_width=6)
        crimp_r1 = Rectangle(width=0.36, height=0.22, color=COL_GRAY, fill_color="#475569", fill_opacity=1.0).move_to([1.85, -1.15, 0])
        crimp_r2 = Rectangle(width=0.36, height=0.22, color=COL_GRAY, fill_color="#475569", fill_opacity=1.0).move_to([4.55, -1.15, 0])
        r_dim_r = Text("R ≥ R_min (กว้าง ปลอดภัย)", font_size=11, color=COL_OK).move_to([3.2, 0.20, 0])
        badge_r3 = _h6_12_badge("✓ ถูก (รัศมีกว้างพอ)", COL_OK).move_to([3.2, 1.40, 0.0])
        call_r3 = Text("ของไหลสะดวก ลวดไม่ล้า", font_size=11, color=COL_OK).move_to([3.2, -1.35, 0.0])
        loop_right = VGroup(
            lr_arc_out, lr_arc_in, lr_stem_l, lr_stem_l_in, lr_stem_r, lr_stem_r_in,
            crimp_r1, crimp_r2, r_dim_r, badge_r3, call_r3
        )

        banner3 = _h6_12_banner("รัศมีแคบเกินไป = เสียดทานของไหลเพิ่ม + เสี่ยงชั้นเสริมแรงล้า (ตัวเลขขั้นต่ำดูได้ที่ H6_11)", COL_WARN)

        self.play(FadeIn(VGroup(loop_wrong, loop_right), shift=UP * 0.25), FadeIn(banner3), run_time=1.0)
        self.play(Indicate(loop_wrong, color=COL_WARN, scale_factor=1.04), run_time=0.8)
        self.wait(5.0)  # Checkpoint 25.0s falls right here!

        self.clear_stage(run_time=0.5)
        self.wait(0.1)

        # ----------------------------------------------------------------------
        # BEAT 29.6–38.5: 4. Twisted Hose (ห้ามติดตั้งแบบสายบิด) — HIGHEST RISK BEAT
        # ----------------------------------------------------------------------
        cap4 = _h6_12_caption_top("4. ห้ามติดตั้งแบบสายบิด (Do Not Install in Twisted Position)")
        self.play(FadeIn(cap4, shift=UP * 0.35), run_time=0.5)

        # Common hose body & fittings
        hose_body_bg = Rectangle(width=7.2, height=0.62, color="#334155", fill_color="#1E293B", fill_opacity=0.98).move_to([0.0, 0.15, 0.0])
        crimp_nut_l = Rectangle(width=0.45, height=0.75, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([-3.8, 0.15, 0.0])
        crimp_nut_r = Rectangle(width=0.45, height=0.75, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([3.8, 0.15, 0.0])
        nut_label_l = Text("ฟิตติ้ง A", font_size=10, color=COL_METAL).next_to(crimp_nut_l, DOWN, buff=0.1)
        nut_label_r = Text("ฟิตติ้ง B", font_size=10, color=COL_METAL).next_to(crimp_nut_r, DOWN, buff=0.1)
        hose_base_grp = VGroup(hose_body_bg, crimp_nut_l, crimp_nut_r, nut_label_l, nut_label_r)

        # Right: Straight longitudinal layline perfectly parallel
        layline_straight = Line([-3.5, 0.05, 0], [3.5, 0.05, 0], color=COL_OK, stroke_width=4)
        layline_text = Text("━ ━ ━ SAE 100R2AT 3/4\" WP 3100 PSI (Layline ขนานตรง) ━ ━ ━", font_size=10.5, color=COL_OK).move_to([0.0, 0.25, 0.0])
        badge_r4 = _h6_12_badge("✓ ถูก (สายตรง ลายขนาน)", COL_OK).move_to([0.0, 1.15, 0.0])
        call_r4 = Text("เส้นพิมพ์บอกสเปก (Layline) ตรงขนานแนวแกน → ชั้นลวดรับแรงดันได้ 100%", font_size=12, color=COL_OK).move_to([0.0, -0.65, 0.0])
        straight_hose_grp = VGroup(hose_base_grp, layline_straight, layline_text, badge_r4, call_r4)

        # Wrong: Helical spiral stripes wrapping around the hose (≥2 full turns visible!)
        hose_base_grp_w = hose_base_grp.copy()
        sp_f1 = Line([-3.5, 0.44, 0], [-1.8, -0.14, 0], color=COL_WARN, stroke_width=5)
        sp_b1 = DashedLine([-1.8, -0.14, 0], [-1.4, 0.44, 0], color="#F87171", stroke_width=3)
        sp_f2 = Line([-1.4, 0.44, 0], [0.3, -0.14, 0], color=COL_WARN, stroke_width=5)
        sp_b2 = DashedLine([0.3, -0.14, 0], [0.7, 0.44, 0], color="#F87171", stroke_width=3)
        sp_f3 = Line([0.7, 0.44, 0], [2.4, -0.14, 0], color=COL_WARN, stroke_width=5)
        sp_b3 = DashedLine([2.4, -0.14, 0], [2.8, 0.44, 0], color="#F87171", stroke_width=3)
        sp_f4 = Line([2.8, 0.44, 0], [3.5, 0.15, 0], color=COL_WARN, stroke_width=5)
        spiral_stripes = VGroup(sp_f1, sp_b1, sp_f2, sp_b2, sp_f3, sp_b3, sp_f4)

        torque_arr = CurvedArrow([3.8, -0.3, 0], [3.8, 0.6, 0], radius=0.45, color=RED, stroke_width=3)
        torque_lbl = Text("แรงบิดจากการขัน!", font_size=10, color=RED).next_to(torque_arr, RIGHT, buff=0.1)
        badge_w4 = _h6_12_badge("✗ ผิด (สายบิดเป็นเกลียว)", COL_WARN).move_to([0.0, 1.15, 0.0])
        call_w4 = Text("⚠️ บิดสายแค่ 7 นิ้ว (7″) บนสายใหญ่ → ความสามารถทนแรงดันลดลงถึง 90%!", font_size=12.5, color=COL_WARN).move_to([0.0, -0.65, 0.0])
        call_w4_sub = Text("(โครงสร้างลวดถักคลายตัว + ข้อต่อพร้อมคลายหลุดเมื่อเจอแรงดันกระชาก)", font_size=11, color=COL_GRAY).move_to([0.0, -1.05, 0.0])
        twisted_hose_grp = VGroup(hose_base_grp_w, spiral_stripes, torque_arr, torque_lbl, badge_w4, call_w4, call_w4_sub)

        banner4 = _h6_12_banner("บิดสายแค่ 7 นิ้ว บนสายไซส์ใหญ่ ก็ลดแรงดันที่ทนได้ถึง 90%! ข้อต่อยังคลายง่ายขึ้นตอนแรงดันกระชากด้วย", COL_WARN)

        self.play(FadeIn(straight_hose_grp, shift=UP * 0.2), FadeIn(banner4), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(straight_hose_grp), run_time=0.4)
        self.play(FadeIn(twisted_hose_grp), run_time=0.6)
        self.play(Indicate(spiral_stripes, color=RED, scale_factor=1.04), run_time=0.8)
        self.wait(4.0)  # Checkpoint 34.0s falls right here!

        self.clear_stage(run_time=0.5)
        self.wait(0.1)

        # ----------------------------------------------------------------------
        # BEAT 39.1–46.5: 5. Movement Plane (ถ้าสายต้องขยับ ให้ขยับในระนาบเดียว)
        # ----------------------------------------------------------------------
        cap5 = _h6_12_caption_top("5. ถ้าสายต้องขยับ ให้ขยับในระนาบเดียว (Flexing in One Plane)")
        self.play(FadeIn(cap5, shift=UP * 0.35), run_time=0.5)

        base_manifold = Rectangle(width=0.9, height=0.4, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([-0.5, -1.05, 0.0])
        base_lbl = Text("จุดยึดฐาน", font_size=10, color=COL_METAL).next_to(base_manifold, LEFT, buff=0.10)
        actuator_block = Rectangle(width=0.9, height=0.4, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([-0.5, 0.85, 0.0])
        act_lbl = Text("ชิ้นส่วนเคลื่อนที่", font_size=10, color=COL_METAL).next_to(actuator_block, LEFT, buff=0.10)
        flex_mech = VGroup(base_manifold, base_lbl, actuator_block, act_lbl)

        # Right: Flex in single 2D plane with curve
        hose_r5_out = Arc(radius=0.95, start_angle=-PI/2, angle=PI, arc_center=[-0.5, -0.10, 0], stroke_color="#334155", stroke_width=10)
        hose_r5_in  = Arc(radius=0.95, start_angle=-PI/2, angle=PI, arc_center=[-0.5, -0.10, 0], stroke_color=COL_OK, stroke_width=6)
        arrow_r5 = DoubleArrow([0.8, 0.85, 0], [0.8, -0.10, 0], color=COL_OK, stroke_width=3.5, tip_length=0.16)
        arrow_r5_lbl = Text("ขยับขึ้น-ลงในระนาบเดียวกับโค้ง", font_size=11, color=COL_OK).next_to(arrow_r5, RIGHT, buff=0.15)
        badge_r5 = _h6_12_badge("✓ ถูก (ระนาบเดียวกับความโค้ง)", COL_OK).move_to([0.0, 1.35, 0.0])
        call_r5 = Text("การเคลื่อนที่อยู่ในระนาบเดียวกับส่วนโค้ง → สายไม่งัด ไม่เกิดแรงบิดลวด", font_size=11.5, color=COL_OK).move_to([0.0, -1.38, 0.0])
        right5_grp = VGroup(flex_mech, hose_r5_out, hose_r5_in, arrow_r5, arrow_r5_lbl, badge_r5, call_r5)

        # Wrong: Out-of-plane twist motion
        flex_mech_w = flex_mech.copy()
        pts_w5 = [[-0.5, -1.05, 0], [0.6, -0.65, 0], [0.9, 0.15, 0], [-0.5, 0.85, 0]]
        hose_w5_out = VMobject(stroke_color="#334155", stroke_width=10).set_points_as_corners(pts_w5)
        hose_w5_in  = VMobject(stroke_color=COL_WARN, stroke_width=6).set_points_as_corners(pts_w5)
        arrow_w5 = Arrow([0.5, 0.2, 0], [1.9, 0.85, 0], color=COL_WARN, stroke_width=3.5, tip_length=0.16)
        arrow_w5_lbl = Text("ขยับเฉียงตัดขวางระนาบโค้ง!", font_size=11, color=COL_WARN).next_to(arrow_w5, UP, buff=0.1)
        badge_w5 = _h6_12_badge("✗ ผิด (ขยับเฉียงตัดระนาบ)", COL_WARN).move_to([0.0, 1.35, 0.0])
        call_w5 = Text("⚠️ ขยับตัดระนาบ → ปลายสายถูกบิดและงัดที่คอข้อต่อ เสี่ยงฉีกขาดรวดเร็ว", font_size=11.5, color=COL_WARN).move_to([0.0, -1.38, 0.0])
        wrong5_grp = VGroup(flex_mech_w, hose_w5_out, hose_w5_in, arrow_w5, arrow_w5_lbl, badge_w5, call_w5)

        banner5 = _h6_12_banner("ให้การขยับอยู่ระนาบเดียวกับส่วนโค้งของสาย และไม่ให้รัศมีแคบกว่าขั้นต่ำระหว่างขยับ", COL_OK)

        self.play(FadeIn(right5_grp, shift=UP * 0.2), FadeIn(banner5), run_time=0.8)
        self.wait(1.2)  # Checkpoint 43.0s falls right here!
        self.play(FadeOut(right5_grp), run_time=0.4)
        self.play(FadeIn(wrong5_grp), run_time=0.6)
        self.wait(3.5)

        self.clear_stage(run_time=0.5)
        self.wait(0.1)

        # ----------------------------------------------------------------------
        # BEAT 47.1–55.5: 6. Slack & Length Change (เผื่อความยาว/สแลคให้พอ)
        # ----------------------------------------------------------------------
        cap6 = _h6_12_caption_top("6. เผื่อความยาว/สแลคให้พอ (Provide Adequate Slack)")
        self.play(FadeIn(cap6, shift=UP * 0.35), run_time=0.5)

        mount_l = Rectangle(width=0.45, height=0.75, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([-3.2, 0.0, 0.0])
        lbl_m_l = Text("จุดยึด 1", font_size=10, color=COL_METAL).next_to(mount_l, DOWN, buff=0.1)
        mount_r = Rectangle(width=0.45, height=0.75, color=COL_METAL, fill_color="#475569", fill_opacity=1.0).move_to([3.2, 0.0, 0.0])
        lbl_m_r = Text("จุดยึด 2", font_size=10, color=COL_METAL).next_to(mount_r, DOWN, buff=0.1)
        mounts_grp = VGroup(mount_l, lbl_m_l, mount_r, lbl_m_r)

        # Wrong 6: Dead-straight taut line (zero slack)
        hose_w6_out = Line([-2.95, 0.0, 0], [2.95, 0.0, 0], stroke_color="#334155", stroke_width=10)
        hose_w6_in  = Line([-2.95, 0.0, 0], [2.95, 0.0, 0], stroke_color=COL_WARN, stroke_width=6)
        tension_l = Arrow([-1.8, 0.0, 0], [-2.7, 0.0, 0], color=RED, stroke_width=3, tip_length=0.15)
        tension_r = Arrow([1.8, 0.0, 0], [2.7, 0.0, 0], color=RED, stroke_width=3, tip_length=0.15)
        dim_w6 = Text("ความยาวตึงเป๊ะ 100% (ไร้สแลค)", font_size=11, color=COL_WARN).move_to([0.0, 0.35, 0.0])
        badge_w6 = _h6_12_badge("✗ ผิด (สายตึงเกินไป)", COL_WARN).move_to([0.0, 1.15, 0.0])
        call_w6 = Text("⚠️ เมื่อจ่ายแรงดัน สายหดตัวสั้นลงได้ถึง −6% → ดึงกระชากข้อต่อหลุดกระเด็น!", font_size=12, color=COL_WARN).move_to([0.0, -0.65, 0.0])
        call_w6_sub = Text("(แถมตอนติดตั้ง สายสั้นจะถูกบิดตัวขันน็อตลำบาก)", font_size=11, color=COL_GRAY).move_to([0.0, -1.05, 0.0])
        wrong6_grp = VGroup(mounts_grp, hose_w6_out, hose_w6_in, tension_l, tension_r, dim_w6, badge_w6, call_w6, call_w6_sub)

        # Right 6: Gentle catenary droop (adequate slack)
        mounts_grp_r = mounts_grp.copy()
        catenary_pts = [
            [-2.95, 0.0, 0], [-2.0, -0.42, 0], [-1.0, -0.65, 0],
            [0.0, -0.72, 0], [1.0, -0.65, 0], [2.0, -0.42, 0], [2.95, 0.0, 0]
        ]
        hose_r6_out = VMobject(stroke_color="#334155", stroke_width=10).set_points_smoothly(catenary_pts)
        hose_r6_in  = VMobject(stroke_color=COL_OK, stroke_width=6).set_points_smoothly(catenary_pts)
        dim_r6 = Text("เผื่อความยาวสแลค (Slack) ให้เพียงพอ", font_size=11, color=COL_OK).move_to([0.0, 0.35, 0.0])
        badge_r6 = _h6_12_badge("✓ ถูก (เผื่อสแลคให้พอ)", COL_OK).move_to([0.0, 1.15, 0.0])
        call_r6 = Text("✓ เผื่อสแลครองรับการเปลี่ยนความยาว (+2% ถึง −6%) ได้อย่างอิสระ ไม่ดึงรั้งข้อต่อ", font_size=12, color=COL_OK).move_to([0.0, -1.25, 0.0])
        right6_grp = VGroup(mounts_grp_r, hose_r6_out, hose_r6_in, dim_r6, badge_r6, call_r6)

        banner6 = _h6_12_banner("แรงดันเปลี่ยนความยาวสายได้ถึง +2% ถึง −6% — สายสั้น/ตึงเกินไปจะถูกดึงบิดตอนติดตั้ง ต้องเผื่อสแลค", COL_OK)

        self.play(FadeIn(wrong6_grp, shift=UP * 0.2), FadeIn(banner6), run_time=0.8)
        self.wait(1.2)  # Checkpoint 51.0s falls right here!
        self.play(FadeOut(wrong6_grp), run_time=0.4)
        self.play(FadeIn(right6_grp), run_time=0.6)
        self.wait(4.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 56.3–61.0: Summary Card
        # ----------------------------------------------------------------------
        card_box = RoundedRectangle(width=11.6, height=3.6, corner_radius=0.15, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, 0.0, 0.0])
        s_head = Text("สรุป: 6 กฎทองการติดตั้งสายไฮดรอลิก (hydraulic06 น.15)", font_size=13.5, color=COL_OK).move_to([0.0, 1.45, 0.0])
        rows = [
            "1. เดินสายพอดี: ใช้ข้อต่องอลดความยาวส่วนเกินและจุดหักมุม (ลดเสียดสี)",
            "2. เลี่ยงผิวร้อน: ห่างผิวร้อนเสมอ หรือใช้แคลมป์ดัน + ปลอกฉนวนกันความร้อน",
            "3. รัศมีดัดโค้ง: ต้องกว้างกว่า R_min (ดูตัวเลขสเปกขั้นต่ำจาก H6_11)",
            "4. ห้ามบิดสาย: บิดแค่ 7 นิ้ว (7″) ทนแรงดันลดลงถึง 90%! (สังเกตแนว Layline)",
            "5. ขยับในระนาบเดียว: ทิศทางการเคลื่อนที่ต้องระนาบเดียวกับความโค้งสาย ไม่งัด",
            "6. เผื่อสแลค (Slack): แรงดันทำให้สายยาว +2% ถึง −6% อย่าขึงตึงเด็ดขาด"
        ]
        s_rows = VGroup(*[Text(r, font_size=11, color=WHITE) for r in rows]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([0.0, 0.0, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(3.9)  # Checkpoint 58.5s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 61.0–65.5: Review Question Card
        # ----------------------------------------------------------------------
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(width=11.2, height=3.2, corner_radius=0.15, color=COL_WARN, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([0.0, 0.0, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.15, 0.0])
        q_body = Text(
            "หากช่างตัดสายไฮดรอลิกสั้นเกินไปนิดเดียวตอนติดตั้ง\nจะเกิดความเสี่ยงร้ายแรงอะไรตามมาบ้าง (เชื่อมโยง 2 กฎในคลิปนี้)?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: 1. สายจะถูกดึงกระชากหลุดเมื่อแรงดันทำให้สายหดสั้นลงถึง −6%\n2. ตอนขันเกลียวติดตั้ง สายที่สั้นจะถูกบังคับบิดตัว (Twist) ซึ่งบิดแค่ 7″ ทนแรงดันลดฮวบ 90%)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.65, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.9)  # Checkpoint 63.0s falls right here!

        self.play(FadeOut(question_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)
        self.wait(0.5)


# ==============================================================================
# SCENE 13: H6_13_ConductorNomograph (hydraulic06.pdf page 16)
# Duration: ~38.0 seconds | 2D SafeScene
# Pedagogical Focus: Conductor Sizing Nomograph
# AHA Moment:
#   1. Nomograph allows reading the 3rd value by drawing a single straight line
#      through 2 known values instead of computing Q = A * V manually.
#   2. Slide example: Known Flow = 14 GPM, Pipe Size = 3/4" ID -> Velocity = 10 ft/s.
#   3. Connection to H6_02: Safe velocity limits determine line suitability:
#      - Intake / suction line: max recommended <= 4 ft/s -> 10 ft/s is DANGEROUS (cavitation risk!).
#      - Pressure line: max recommended <= 20 ft/s -> 10 ft/s is SAFE.
# ==============================================================================

def _h6_13_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_13_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_13_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_13_banner(text, color):
    lbl = Text(text, font_size=12, color=color)
    bg = RoundedRectangle(
        width=min(12.5, max(lbl.width + 0.6, 9.0)),
        height=0.55,
        corner_radius=0.1,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -1.85, 0.0])
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_13_ConductorNomograph(SafeScene):
    def clear_stage(self, run_time=0.5):
        """Fade out all scene mobjects except persistent header."""
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Persistent Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = _h6_13_title("โนโมกราฟเลือกขนาดท่อ")
        self.ref_m = _h6_13_page_ref("hydraulic06 น.16")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)  # Checkpoint 1.5s

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.2: Hook Question
        # ----------------------------------------------------------------------
        hook_q = _h6_13_caption_top("รู้ว่าท่อต้องไหล 14 GPM ผ่าน ID 3/4 นิ้ว จะไหลเร็วแค่ไหน — ต้องคำนวณเองไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.6)  # Checkpoint 3.6s
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 5.2–9.0: Nomograph Introduction (3 Vertical Scales + Formula)
        # ----------------------------------------------------------------------
        cap1 = _h6_13_caption_top("โนโมกราฟ: ลากเส้นตรงผ่าน 2 จุดที่รู้ อ่านจุดที่ 3 ได้เลย")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Formula badge floating at top
        formula_txt = Text("Area (sq. in.) = (GPM × 0.3208) / Velocity (ft/s)", font_size=11.5, color=COL_CURR)
        formula_bg = RoundedRectangle(
            width=formula_txt.width + 0.45,
            height=0.36,
            corner_radius=0.08,
            color=COL_CURR,
            fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, 1.95, 0.0])
        formula_txt.move_to(formula_bg.get_center())
        formula_grp = VGroup(formula_bg, formula_txt)

        # 3 Scales layout: x = -3.8 (Flow), x = 0.0 (Size), x = +3.8 (Velocity)
        x_flow = -3.8
        x_size = 0.0
        x_vel  = 3.8
        y_bot = -1.55
        y_top = 1.20

        # Helper to make ticks (no invented numbers! Only dashes)
        def make_scale_ticks(x_pos, tick_ys, tick_len=0.16):
            lines = []
            for y in tick_ys:
                lines.append(Line([x_pos - tick_len / 2, y, 0], [x_pos + tick_len / 2, y, 0], color=COL_GRAY, stroke_width=1.5))
            return VGroup(*lines)

        # 1. Flow scale
        axis_flow = Line([x_flow, y_bot, 0], [x_flow, y_top, 0], color=COL_GRAY, stroke_width=2.5)
        hdr_flow = Text("อัตราไหล (Flow)\n[GPM]", font_size=11, color=COL_METAL).next_to(axis_flow, UP, buff=0.12)
        ticks_flow = make_scale_ticks(x_flow, [-1.3, -0.8, -0.3, 0.15, 0.60, 1.05])
        # Exactly verified number: 14 GPM at y = 0.60
        y_flow_14 = 0.60
        dot_flow_14 = Dot([x_flow, y_flow_14, 0], radius=0.09, color=COL_OK)
        lbl_flow_14 = Text("14 GPM", font_size=12, color=COL_OK).next_to(dot_flow_14, LEFT, buff=0.15)
        scale_flow = VGroup(axis_flow, hdr_flow, ticks_flow, dot_flow_14, lbl_flow_14)

        # 2. Size scale (ID in inches)
        axis_size = Line([x_size, y_bot, 0], [x_size, y_top, 0], color=COL_GRAY, stroke_width=2.5)
        hdr_size = Text("ขนาดรูในท่อ (Size)\n[นิ้ว / ID]", font_size=11, color=COL_METAL).next_to(axis_size, UP, buff=0.12)
        ticks_size = make_scale_ticks(x_size, [-1.3, -0.8, -0.35, 0.10, 0.55, 1.05])
        # Exactly verified number: 3/4" ID at y = 0.10
        # Notice: y_size_34 = (y_flow_14 + y_vel_10) / 2 = (0.60 + (-0.40)) / 2 = 0.10!
        # This guarantees 100% mathematical collinearity without kink!
        y_size_34 = 0.10
        dot_size_34 = Dot([x_size, y_size_34, 0], radius=0.09, color=COL_OK)
        lbl_size_34 = Text("3/4\" ID", font_size=12, color=COL_OK).next_to(dot_size_34, UR, buff=0.12)
        scale_size = VGroup(axis_size, hdr_size, ticks_size, dot_size_34, lbl_size_34)

        # 3. Velocity scale (ft/s)
        axis_vel = Line([x_vel, y_bot, 0], [x_vel, y_top, 0], color=COL_GRAY, stroke_width=2.5)
        hdr_vel = Text("ความเร็ว (Velocity)\n[ft/s]", font_size=11, color=COL_METAL).next_to(axis_vel, UP, buff=0.12)
        ticks_vel = make_scale_ticks(x_vel, [-1.25, -0.85, -0.40, 0.05, 0.50, 0.85, 1.10])
        # Exactly verified number: 10 ft/s at y = -0.40
        y_vel_10 = -0.40
        dot_vel_10 = Dot([x_vel, y_vel_10, 0], radius=0.09, color=COL_OK)
        lbl_vel_10 = Text("10 ft/s", font_size=12, color=COL_OK).next_to(dot_vel_10, RIGHT, buff=0.15)
        scale_vel = VGroup(axis_vel, hdr_vel, ticks_vel, dot_vel_10, lbl_vel_10)

        nomograph_scales = VGroup(scale_flow, scale_size, scale_vel)

        self.play(
            FadeIn(nomograph_scales, shift=UP * 0.2),
            FadeIn(formula_grp, shift=DOWN * 0.15),
            run_time=1.2
        )
        self.wait(1.5)

        # ----------------------------------------------------------------------
        # BEAT 9.0–11.0: Step 1 (มาร์ก 14 GPM บนสเกล Flow)
        # ----------------------------------------------------------------------
        banner_s1 = _h6_13_banner("① จุดที่ 1: มาร์กอัตราไหลที่ต้องการ 14 GPM บนสเกล Flow", COL_OK)
        self.play(
            Indicate(dot_flow_14, color=YELLOW, scale_factor=1.3),
            FadeIn(banner_s1),
            run_time=0.8
        )
        self.wait(1.2)  # Checkpoint 9.5s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 11.0–13.2: Step 2 (มาร์ก ID 3/4" บนสเกล Size + ลากเส้น 1 ไป 2)
        # ----------------------------------------------------------------------
        banner_s2 = _h6_13_banner("② จุดที่ 2: วางทาบผ่านขนาดท่อที่เลือก ID 3/4 นิ้ว บนสเกล Size", COL_OK)
        line_1to2 = Line(
            [x_flow, y_flow_14, 0],
            [x_size, y_size_34, 0],
            color=COL_OK,
            stroke_width=3.5
        )
        self.play(FadeOut(banner_s1), run_time=0.3)
        self.play(
            Create(line_1to2),
            Indicate(dot_size_34, color=YELLOW, scale_factor=1.3),
            FadeIn(banner_s2),
            run_time=1.0
        )
        self.wait(1.2)  # Checkpoint 12.0s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 13.2–16.5: Step 3 (ลากเส้นตรงต่อไปยังสเกล Velocity อ่านได้ 10 ft/s)
        # ----------------------------------------------------------------------
        banner_s3 = _h6_13_banner("③ จุดที่ 3: ลากเส้นตรงทะลุไปอ่านค่าความเร็วได้ v = 10 ft/s ทันที!", COL_OK)
        line_2to3 = Line(
            [x_size, y_size_34, 0],
            [x_vel, y_vel_10, 0],
            color=COL_OK,
            stroke_width=3.5
        )
        self.play(FadeOut(banner_s2), run_time=0.3)
        self.play(
            Create(line_2to3),
            Indicate(dot_vel_10, color=YELLOW, scale_factor=1.3),
            FadeIn(banner_s3),
            run_time=1.0
        )
        self.wait(1.7)  # Checkpoint 15.0s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 16.5–25.5: Connect to H6_02 (Intake 4 ft/s vs Pressure 20 ft/s)
        # ----------------------------------------------------------------------
        # Fade out flow, size scales, lines, formula, step banner, and cap1
        self.play(
            FadeOut(scale_flow),
            FadeOut(scale_size),
            FadeOut(line_1to2),
            FadeOut(line_2to3),
            FadeOut(formula_grp),
            FadeOut(banner_s3),
            FadeOut(cap1),
            run_time=0.6
        )

        cap2 = _h6_13_caption_top("เชื่อมกับ H6_02: v = 10 ft/s นี้ปลอดภัยไหม? ขึ้นกับประเภทของท่อ")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.6)

        # Shift Velocity scale from x=3.8 to x=-2.2 to leave room on right
        vel_shift_vector = LEFT * 6.0
        self.play(
            scale_vel.animate.shift(vel_shift_vector),
            run_time=0.8
        )

        x_vel_new = x_vel - 6.0  # -2.2

        # 1. Intake line limit: 4 ft/s at y = -1.25 (well below 10 ft/s at -0.40)
        y_intake_4 = -1.25
        dot_intake_4 = Dot([x_vel_new, y_intake_4, 0], radius=0.09, color=COL_WARN)
        arr_intake = Arrow([x_vel_new + 0.65, y_intake_4, 0], [x_vel_new + 0.12, y_intake_4, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.12)
        lbl_intake_4 = Text("4 ft/s", font_size=11, color=COL_WARN).next_to(arr_intake, RIGHT, buff=0.10)
        mark_intake_4 = VGroup(dot_intake_4, arr_intake, lbl_intake_4)

        # 2. Pressure line limit: 20 ft/s at y = 0.85 (well above 10 ft/s at -0.40)
        y_pressure_20 = 0.85
        dot_pressure_20 = Dot([x_vel_new, y_pressure_20, 0], radius=0.09, color=COL_OK)
        arr_pressure = Arrow([x_vel_new + 0.65, y_pressure_20, 0], [x_vel_new + 0.12, y_pressure_20, 0], color=COL_OK, stroke_width=2.5, tip_length=0.12)
        lbl_pressure_20 = Text("20 ft/s", font_size=11, color=COL_OK).next_to(arr_pressure, RIGHT, buff=0.10)
        mark_pressure_20 = VGroup(dot_pressure_20, arr_pressure, lbl_pressure_20)

        # Callout card on right side explaining the comparison
        eval_card_bg = RoundedRectangle(width=5.8, height=2.2, corner_radius=0.12, color=COL_GRAY, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([3.4, -0.20, 0.0])
        eval_t1 = Text("ผลการประเมิน v = 10 ft/s จากตัวอย่าง:", font_size=11.5, color=WHITE).move_to([3.4, 0.55, 0.0])
        eval_t2 = Text("• ท่อแรงดัน (Pressure): 10 ft/s ปลอดภัย\n  (ไม่เกินขีดจำกัด 20 ft/s)", font_size=11, color=COL_OK).move_to([3.4, 0.05, 0.0])
        eval_t3 = Text("• ท่อดูด (Intake): 10 ft/s อันตราย\n  (เกินขีดจำกัด 4 ft/s เสี่ยงเกิด Cavitation!)", font_size=11, color=COL_WARN).move_to([3.4, -0.55, 0.0])
        eval_card = VGroup(eval_card_bg, eval_t1, eval_t2, eval_t3)

        self.play(
            FadeIn(mark_intake_4, shift=RIGHT * 0.2),
            run_time=0.6
        )
        self.wait(0.8)  # Checkpoint 21.0s falls right here!

        self.play(
            FadeIn(mark_pressure_20, shift=RIGHT * 0.2),
            run_time=0.6
        )
        self.wait(0.8)

        self.play(
            FadeIn(eval_card, shift=LEFT * 0.2),
            Indicate(lbl_vel_10, color=YELLOW, scale_factor=1.2),
            run_time=0.8
        )
        self.wait(3.5)  # Checkpoint 24.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 26.1–31.0: Summary Card
        # ----------------------------------------------------------------------
        card_box = RoundedRectangle(
            width=11.6, height=3.4, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: โนโมกราฟเลือกขนาดท่อ (hydraulic06 น.16)", font_size=14, color=COL_OK).move_to([0.0, 1.25, 0.0])
        rows = [
            "1. โนโมกราฟ: ลากเส้นตรงผ่าน 2 ค่าที่รู้ (Flow & Size) อ่านค่าที่ 3 (Velocity) ได้ทันที ไม่ต้องคำนวณมือ",
            "2. ท่อดูด (Intake Line): แนะนำความเร็วไม่เกิน 4 ft/s เพื่อป้องกัน Cavitation โพรงอากาศทำลายปั๊ม (H6_02)",
            "3. ท่อแรงดัน (Pressure Line): แนะนำความเร็วไม่เกิน 20 ft/s เพื่อไม่ให้เกิดแรงเสียดทานและความร้อนสะสมเกินพิกัด"
        ]
        s_rows = VGroup(*[Text(r, font_size=11.5, color=WHITE) for r in rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.0, -0.20, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(4.1)  # Checkpoint 29.0s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 31.0–36.0: Review Question Card
        # ----------------------------------------------------------------------
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "หากใช้โนโมกราฟแล้วอ่านความเร็วของไหลได้ v = 15 ft/s\nและท่อเส้นนี้คือท่อดูดเข้าปั๊ม (Intake Line) — ปลอดภัยหรือไม่?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: ไม่ปลอดภัย — เพราะท่อดูดแนะนำความเร็วไม่เกิน 4 ft/s\nความเร็ว 15 ft/s จะทำให้ความดันตกต่ำจนน้ำมันเดือดกลายเป็นโพรงไอ เกิด Cavitation รุนแรง)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(4.4)  # Checkpoint 33.5s falls right here!
        self.play(FadeOut(question_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)
        self.wait(0.5)


# ==============================================================================
# SCENE 14: H6_14_SealingDevicesOverview (hydraulic06.pdf page 17)
# Duration: ~37.0 seconds | 2D SafeScene
# Pedagogical Focus: Sealing Devices Overview (Static vs Dynamic Seals)
# AHA Moment:
#   1. Classification criterion is relative motion between sealed mating surfaces:
#      - Static seals: NO relative motion (e.g. flange gasket, static O-ring).
#      - Dynamic seals: HAS relative motion (sliding rod, rotating shaft).
#   2. O-rings appear in BOTH lists on slide 17! A seal's classification depends
#      on its installation location and relative movement, not its inherent shape.
#   3. Static flange joints: Basic Flange Joint (uses resilient gasket) vs
#      Metal-to-Metal Joint (precision ground faces direct contact, no gasket).
#   4. Roadmap scene: Names & groups only; detailed mechanisms covered in H6_15–H6_20.
# ==============================================================================

def _h6_14_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_14_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_14_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_14_banner(text, color):
    lbl = Text(text, font_size=11.5, color=color)
    bg = RoundedRectangle(
        width=min(12.6, max(lbl.width + 0.6, 9.5)),
        height=0.50,
        corner_radius=0.1,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.62, 0.0])
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_14_mini_badge(text, color):
    lbl = Text(text, font_size=10.5, color=color)
    bg = RoundedRectangle(
        width=lbl.width + 0.40,
        height=0.34,
        corner_radius=0.07,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_14_SealingDevicesOverview(SafeScene):
    def clear_stage(self, run_time=0.5):
        """Fade out all scene mobjects except persistent header."""
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = _h6_14_title("อุปกรณ์ผนึก (Sealing Devices): ภาพรวม")
        self.ref_m = _h6_14_page_ref("hydraulic06 น.17")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)  # Checkpoint 1.5s

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.0: Hook Question
        # ----------------------------------------------------------------------
        hook_q = _h6_14_caption_top("ซีลทุกจุดในระบบไฮดรอลิกเหมือนกันหมดไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)  # Checkpoint 3.6s
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 5.0–13.0: 2 Columns (Static vs Dynamic)
        # ----------------------------------------------------------------------
        cap1 = _h6_14_caption_top("แบ่ง 2 กลุ่มตามการเคลื่อนที่สัมพัทธ์ของผิวที่ปิดผนึก")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Column Layout Dimensions
        col_w = 5.8
        col_h = 4.1
        y_col = 0.05
        x_left = -3.25
        x_right = 3.25

        # --- LEFT COLUMN: STATIC SEALS (NO MOTION) ---
        box_static = RoundedRectangle(
            width=col_w, height=col_h, corner_radius=0.12,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.90).move_to([x_left, y_col, 0.0])

        hdr_static = Text("1. ซีลสถิต (Static Seals)", font_size=13.5, color=COL_FIELD).move_to([x_left, y_col + 1.70, 0.0])
        sub_static = Text("ไม่มีการเคลื่อนที่สัมพัทธ์ (No Relative Motion)", font_size=10, color=COL_GRAY).move_to([x_left, y_col + 1.38, 0.0])

        # Icon/Diagram: Flange Joint firmly bolted, NO motion arrows! (§34)
        f_top = Rectangle(width=2.5, height=0.26, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([x_left, y_col + 0.96, 0.0])
        f_gasket = Rectangle(width=2.5, height=0.12, color=COL_CURR, fill_color=COL_CURR).set_fill(COL_CURR, 1.0).move_to([x_left, y_col + 0.77, 0.0])
        f_bot = Rectangle(width=2.5, height=0.26, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([x_left, y_col + 0.58, 0.0])
        bolt_l = Line([x_left - 0.90, y_col + 1.15, 0], [x_left - 0.90, y_col + 0.39, 0], color=COL_GRAY, stroke_width=2.5)
        bolt_r = Line([x_left + 0.90, y_col + 1.15, 0], [x_left + 0.90, y_col + 0.39, 0], color=COL_GRAY, stroke_width=2.5)
        lbl_diag_static = Text("[หน้าแปลนประกบนิ่ง — ไม่มีส่วนเคลื่อนที่]", font_size=9.5, color=COL_GRAY).move_to([x_left, y_col + 0.28, 0.0])
        diag_static = VGroup(f_top, f_gasket, f_bot, bolt_l, bolt_r, lbl_diag_static)

        # List of static seals (directly from slide 17)
        item_s1 = Text("• Flange gasket (ปะเก็นหน้าแปลน)", font_size=11, color=WHITE).move_to([x_left - 0.20, y_col - 0.02, 0.0])
        item_s2 = Text("• O-rings (โอริง)", font_size=11.5, color=COL_OK).move_to([x_left - 0.90, y_col - 0.38, 0.0])
        note_s = Text("(ปิดผนึกชิ้นส่วนที่ขันแน่นอยู่กับที่)", font_size=10, color=COL_GRAY).move_to([x_left, y_col - 0.85, 0.0])

        col_static = VGroup(box_static, hdr_static, sub_static, diag_static, item_s1, item_s2, note_s)

        # --- RIGHT COLUMN: DYNAMIC SEALS (WITH MOTION) ---
        box_dynamic = RoundedRectangle(
            width=col_w, height=col_h, corner_radius=0.12,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.90).move_to([x_right, y_col, 0.0])

        hdr_dynamic = Text("2. ซีลพลวัต (Dynamic Seals)", font_size=13.5, color=COL_WARN).move_to([x_right, y_col + 1.70, 0.0])
        sub_dynamic = Text("มีการเคลื่อนที่สัมพัทธ์ (Relative Motion)", font_size=10, color=COL_GRAY).move_to([x_right, y_col + 1.38, 0.0])

        # Icon/Diagram: Rod sliding through housing + BIDIRECTIONAL MOTION ARROWS! (§34)
        housing_l = Rectangle(width=0.65, height=0.64, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([x_right - 0.85, y_col + 0.77, 0.0])
        housing_r = Rectangle(width=0.65, height=0.64, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([x_right + 0.85, y_col + 0.77, 0.0])
        rod = Rectangle(width=0.85, height=0.76, color=COL_FIELD, fill_color="#1E3A8A").set_fill("#1E3A8A", 0.85).move_to([x_right, y_col + 0.77, 0.0])
        # Visible bidirectional motion arrows on rod: up & down arrows
        arr_up = Arrow([x_right + 0.22, y_col + 0.55, 0], [x_right + 0.22, y_col + 1.00, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.10)
        arr_down = Arrow([x_right - 0.22, y_col + 1.00, 0], [x_right - 0.22, y_col + 0.55, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.10)
        lbl_diag_dynamic = Text("[ก้านสูบเลื่อนเข้า-ออก — มีผิวเสียดสีเคลื่อนที่]", font_size=9.5, color=COL_WARN).move_to([x_right, y_col + 0.28, 0.0])
        diag_dynamic = VGroup(housing_l, housing_r, rod, arr_up, arr_down, lbl_diag_dynamic)

        # List of dynamic seals (5 items directly from slide 17)
        item_d1 = Text("• O-rings (โอริง)", font_size=11.5, color=COL_OK).move_to([x_right - 1.15, y_col - 0.38, 0.0])
        item_d2 = Text("• Compression packings (V & U)", font_size=10.5, color=WHITE).move_to([x_right - 0.25, y_col - 0.68, 0.0])
        item_d3 = Text("• Piston cup packings", font_size=10.5, color=WHITE).move_to([x_right - 0.72, y_col - 0.98, 0.0])
        item_d4 = Text("• Piston rings", font_size=10.5, color=WHITE).move_to([x_right - 1.15, y_col - 1.28, 0.0])
        item_d5 = Text("• Wiper rings", font_size=10.5, color=WHITE).move_to([x_right - 1.20, y_col - 1.58, 0.0])

        col_dynamic = VGroup(box_dynamic, hdr_dynamic, sub_dynamic, diag_dynamic, item_d1, item_d2, item_d3, item_d4, item_d5)

        self.play(
            FadeIn(col_static, shift=RIGHT * 0.3),
            FadeIn(col_dynamic, shift=LEFT * 0.3),
            run_time=1.2
        )
        self.wait(5.0)  # Checkpoint 9.0s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 13.0–20.0: Aha Moment — O-rings appear in BOTH lists!
        # ----------------------------------------------------------------------
        cap2 = _h6_14_caption_top("สังเกต: 'O-rings' อยู่ทั้ง 2 ฝั่ง! เป็นได้ทั้งสถิตและพลวัต", color=YELLOW)
        # Avoid simultaneous cross-fade layout collision
        self.play(FadeOut(cap1), run_time=0.25)
        self.play(FadeIn(cap2, shift=UP * 0.25), run_time=0.45)

        # Highlight boxes around O-rings in both columns
        hl_box_s = SurroundingRectangle(item_s2, color=YELLOW, buff=0.08, corner_radius=0.06, stroke_width=2.5)
        hl_box_d = SurroundingRectangle(item_d1, color=YELLOW, buff=0.08, corner_radius=0.06, stroke_width=2.5)

        # Direct horizontal dashed link connecting the two highlighted boxes
        link_line = DashedLine(
            hl_box_s.get_right(), hl_box_d.get_left(),
            color=YELLOW, stroke_width=2.5, dash_length=0.15
        )

        banner_aha = _h6_14_banner(
            "การเป็นซีลสถิตหรือพลวัต ขึ้นกับจุดติดตั้งว่าขยับหรือไม่ — ไม่ใช่คุณสมบัติเฉพาะของตัวซีลเอง",
            COL_OK
        )

        self.play(
            Create(hl_box_s),
            Create(hl_box_d),
            Indicate(item_s2, color=YELLOW, scale_factor=1.15),
            Indicate(item_d1, color=YELLOW, scale_factor=1.15),
            Create(link_line),
            FadeIn(banner_aha, shift=UP * 0.2),
            run_time=1.0
        )
        self.wait(4.4)  # Checkpoint 16.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 20.6–27.0: Flange Joints Comparison (Static Seal Subtypes)
        # ----------------------------------------------------------------------
        cap3 = _h6_14_caption_top("ซีลสถิต: รอยต่อหน้าแปลน 2 แบบ (Flange Joints)")
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.6)

        card_w2 = 5.8
        card_h2 = 4.1
        y_joint = 0.05

        # 1. BASIC FLANGE JOINTS (WITH GASKET)
        box_j1 = RoundedRectangle(
            width=card_w2, height=card_h2, corner_radius=0.12,
            color=COL_CURR, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.90).move_to([x_left, y_joint, 0.0])
        hdr_j1 = Text("1. Basic Flange Joint", font_size=13.5, color=COL_CURR).move_to([x_left, y_joint + 1.70, 0.0])
        sub_j1 = Text("มีชั้นปะเก็น (Gasket) คั่นกลาง", font_size=11, color=WHITE).move_to([x_left, y_joint + 1.38, 0.0])

        # Large detailed diagram of gasket joint
        # Top flange
        flange1_top = Rectangle(
            width=3.2, height=0.42, color=COL_METAL, fill_color="#334155"
        ).set_fill("#334155", 0.95).move_to([x_left, y_joint + 0.88, 0.0])
        # VISIBLE GASKET LAYER (Yellow / Amber)
        gasket_layer = Rectangle(
            width=3.2, height=0.20, color=COL_CURR, fill_color=COL_CURR
        ).set_fill(COL_CURR, 1.0).move_to([x_left, y_joint + 0.57, 0.0])
        # Bottom flange
        flange1_bot = Rectangle(
            width=3.2, height=0.42, color=COL_METAL, fill_color="#334155"
        ).set_fill("#334155", 0.95).move_to([x_left, y_joint + 0.26, 0.0])

        # Clamping bolts
        bolt1_l = Line([x_left - 1.15, y_joint + 1.18, 0], [x_left - 1.15, y_joint - 0.04, 0], color=COL_GRAY, stroke_width=2.5)
        bolt1_r = Line([x_left + 1.15, y_joint + 1.18, 0], [x_left + 1.15, y_joint - 0.04, 0], color=COL_GRAY, stroke_width=2.5)

        badge_j1 = _h6_14_mini_badge("ชั้นปะเก็น (Gasket Layer) สีเหลืองคั่นกลาง", COL_CURR).move_to([x_left, y_joint - 0.35, 0.0])
        desc_j1 = Text("ปะเก็นถูกบีบอัดจนยุบตัวแทรกเต็มช่องว่าง\nป้องกันการรั่วซึมได้ดีแม้ผิวประกบไม่เรียบเนียนสนิท", font_size=10.5, color=WHITE).move_to([x_left, y_joint - 0.95, 0.0])

        joint_gasket = VGroup(box_j1, hdr_j1, sub_j1, flange1_top, gasket_layer, flange1_bot, bolt1_l, bolt1_r, badge_j1, desc_j1)

        # 2. METAL-TO-METAL JOINTS (WITHOUT GASKET)
        box_j2 = RoundedRectangle(
            width=card_w2, height=card_h2, corner_radius=0.12,
            color=COL_FIELD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.90).move_to([x_right, y_joint, 0.0])
        hdr_j2 = Text("2. Metal-to-Metal Joint", font_size=13.5, color=COL_FIELD).move_to([x_right, y_joint + 1.70, 0.0])
        sub_j2 = Text("ประกบโลหะชนโลหะ (ไม่ใช้ปะเก็น)", font_size=11, color=WHITE).move_to([x_right, y_joint + 1.38, 0.0])

        # Diagram of metal-to-metal (2 flanges pressed directly together, NO gasket layer!)
        flange2_top = Rectangle(
            width=3.2, height=0.42, color=COL_METAL, fill_color="#334155"
        ).set_fill("#334155", 0.95).move_to([x_right, y_joint + 0.78, 0.0])
        # Direct mating interface line (NO gap, NO layer)
        mating_line = Line([x_right - 1.6, y_joint + 0.57, 0], [x_right + 1.6, y_joint + 0.57, 0], color=COL_OK, stroke_width=2.5)
        flange2_bot = Rectangle(
            width=3.2, height=0.42, color=COL_METAL, fill_color="#334155"
        ).set_fill("#334155", 0.95).move_to([x_right, y_joint + 0.36, 0.0])

        bolt2_l = Line([x_right - 1.15, y_joint + 1.08, 0], [x_right - 1.15, y_joint + 0.06, 0], color=COL_GRAY, stroke_width=2.5)
        bolt2_r = Line([x_right + 1.15, y_joint + 1.08, 0], [x_right + 1.15, y_joint + 0.06, 0], color=COL_GRAY, stroke_width=2.5)

        badge_j2 = _h6_14_mini_badge("ผิวโลหะประกบแนบสนิท ไร้ปะเก็น", COL_OK).move_to([x_right, y_joint - 0.35, 0.0])
        desc_j2 = Text("อาศัยการกลึงเจียระไนผิวเรียบละเอียดระดับไมครอน\nขันอัดโลหะแนบกันตรงๆ โดยไม่ต้องพึ่งพาปะเก็น", font_size=10.5, color=WHITE).move_to([x_right, y_joint - 0.95, 0.0])

        joint_metal = VGroup(box_j2, hdr_j2, sub_j2, flange2_top, mating_line, flange2_bot, bolt2_l, bolt2_r, badge_j2, desc_j2)

        banner_joints = _h6_14_banner(
            "หน้าแปลนทั่วไปใช้ Gasket คั่น / หากผิวเรียบละเอียดสูงมาก สามารถใช้ Metal-to-Metal ได้",
            COL_OK
        )

        self.play(
            FadeIn(joint_gasket, shift=UP * 0.25),
            FadeIn(joint_metal, shift=UP * 0.25),
            FadeIn(banner_joints, shift=UP * 0.2),
            run_time=1.0
        )
        self.wait(4.6)  # Checkpoint 24.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 27.6–32.0: Summary Card
        # ----------------------------------------------------------------------
        card_box = RoundedRectangle(
            width=11.6, height=3.4, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: ภาพรวมอุปกรณ์ผนึก (hydraulic06 น.17)", font_size=14, color=COL_OK).move_to([0.0, 1.25, 0.0])
        rows = [
            "1. เกณฑ์จำแนก: มีการเคลื่อนที่สัมพัทธ์ของผิวสัมผัสหรือไม่ (สถิต = ไม่ขยับ, พลวัต = ขยับ)",
            "2. O-rings เป็นได้ทั้งสองแบบ: ติดตั้งฝาประกบ = ซีลสถิต / ติดตั้งรอบก้านสูบเลื่อน = ซีลพลวัต",
            "3. การเจาะลึกกลไก: O-rings, Packings, Piston Cups, Rings, Wiper ติดตามต่อใน H6_15–H6_20"
        ]
        s_rows = VGroup(*[Text(r, font_size=11.5, color=WHITE) for r in rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.0, -0.20, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(3.6)  # Checkpoint 29.0s falls right here!

        # ----------------------------------------------------------------------
        # BEAT 32.0–36.0: Review Question Card
        # ----------------------------------------------------------------------
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "ซีลรอบก้านสูบไฮดรอลิกที่เลื่อนเข้าออกตลอดเวลา\nควรจัดเป็นซีลสถิต (Static) หรือซีลพลวัต (Dynamic)?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: ซีลพลวัต (Dynamic Seal) — เพราะก้านสูบกับร่องเสื้อสูบมีการเคลื่อนที่สัมพัทธ์กันตลอดเวลา)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.4)  # Checkpoint 33.5s falls right here!

        self.play(FadeOut(question_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)
        self.wait(0.5)


# ==============================================================================
# SCENE 15: H6_15_ORings (O-Ring: ซีลแบบ Self-Energizing)
# hydraulic06.pdf page 18
# ==============================================================================

COL_ORING_H6_15 = "#1E293B"  # Dark rubber ring with distinct border
COL_FLUID_H6_15 = "#EF4444"  # Red hydraulic fluid under pressure


def _h6_15_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_15_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_15_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_15_banner(text, color):
    lbl = Text(text, font_size=11.5, color=color)
    bg = RoundedRectangle(
        width=min(12.6, max(lbl.width + 0.6, 9.5)),
        height=0.50,
        corner_radius=0.1,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.62, 0.0])
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_15_badge(text, color):
    lbl = Text(text, font_size=11, color=color)
    bg = RoundedRectangle(
        width=lbl.width + 0.40,
        height=0.36,
        corner_radius=0.08,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_15_ORings(SafeScene):
    def clear_stage(self, run_time=0.5):
        """Fade out all scene mobjects except persistent header."""
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = _h6_15_title("O-Ring: ซีลแบบ Self-Energizing")
        self.ref_m = _h6_15_page_ref("hydraulic06 น.18")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)  # Checkpoint 1.5s falls here

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.5: Hook Question
        # ----------------------------------------------------------------------
        hook_q = _h6_15_caption_top("O-ring บีบแน่นแค่ตอนติดตั้ง แรงดันเพิ่มขึ้นไม่มีผลอะไรกับความแน่นของซีลจริงไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.9)  # Checkpoint 3.6s falls here
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 5.5–13.6: State 1 (Installed, Initial Squeeze, No Pressure)
        # ----------------------------------------------------------------------
        cap1 = _h6_15_caption_top("1. ติดตั้ง: บีบอัดใน Annular Groove ทั้ง 2 ด้าน (ยังไม่มีแรงดัน)")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Base Cross-Section Geometry: Groove in metal housing
        # Center of groove cavity is at [0.0, 0.0]
        # Groove cavity: width = 3.6 (-1.8 to +1.8), height = 2.0 (-1.0 to +1.0)
        # Upper metal block: y from +1.0 to +1.8
        metal_top = Rectangle(width=7.2, height=0.8, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([0.0, 1.40, 0.0])
        metal_bot_l = Rectangle(width=1.8, height=1.6, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([-2.7, 0.20, 0.0])
        metal_bot_floor = Rectangle(width=7.2, height=0.8, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([0.0, -1.40, 0.0])
        metal_bot_r = Rectangle(width=1.8, height=1.6, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([2.7, 0.20, 0.0])

        groove_housing = VGroup(metal_top, metal_bot_l, metal_bot_floor, metal_bot_r)

        # O-Ring State 1: Centered at x=0.0, squeezed vertically (width=2.1, height=1.92)
        # Natural O-ring would be circle diameter ~2.15, but squeezed between floor (-1.0) and roof (+1.0)
        # Visibly flattened at top and bottom contacts!
        oring_s1 = Ellipse(
            width=2.10, height=1.94,
            color="#38BDF8", stroke_width=3.5,
            fill_color="#0F172A", fill_opacity=0.95
        ).move_to([0.0, 0.0, 0.0])

        # Squeeze indicator arrows top and bottom
        arr_sq_top = Arrow([0.0, 1.8, 0], [0.0, 1.05, 0], color=COL_CURR, stroke_width=2.5, tip_length=0.10)
        arr_sq_bot = Arrow([0.0, -1.8, 0], [0.0, -1.05, 0], color=COL_CURR, stroke_width=2.5, tip_length=0.10)
        lbl_sq = Text("บีบอัดบน-ล่างตอนติดตั้ง (Initial Squeeze)", font_size=10.5, color=COL_CURR).move_to([0.0, -2.10, 0.0])
        squeeze_indicators = VGroup(arr_sq_top, arr_sq_bot, lbl_sq)

        lbl_gap_l = Text("ช่องว่างซ้าย", font_size=9.5, color=COL_GRAY).move_to([-1.35, 0.0, 0.0])
        lbl_gap_r = Text("ช่องว่างขวา", font_size=9.5, color=COL_GRAY).move_to([1.35, 0.0, 0.0])
        clearance_labels = VGroup(lbl_gap_l, lbl_gap_r)

        banner1 = _h6_15_banner("แม้ยังไม่มีแรงดันของไหล การบีบอัดตอนประกอบก็ปิดผนึกได้ระดับหนึ่งแล้ว", COL_OK)

        self.play(
            FadeIn(groove_housing, shift=UP * 0.2),
            FadeIn(oring_s1),
            FadeIn(squeeze_indicators),
            FadeIn(clearance_labels),
            FadeIn(banner1),
            run_time=1.0
        )
        self.wait(5.9)  # Checkpoint 10.0s falls here

        # ----------------------------------------------------------------------
        # BEAT 13.6–24.0: State 2 (Pressure Applied, Self-Energizing)
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(cap1),
            FadeOut(squeeze_indicators),
            FadeOut(clearance_labels),
            FadeOut(banner1),
            run_time=0.4
        )

        cap2 = _h6_15_caption_top("2. แรงดันของไหลเข้า — ยิ่งดันยิ่งซีลแน่น (Self-Energizing Action)")
        self.play(FadeIn(cap2, shift=UP * 0.25), run_time=0.4)

        # Red hydraulic fluid enters from the left
        fluid_rect = Rectangle(
            width=1.85, height=1.92,
            color=COL_FLUID_H6_15, fill_color=COL_FLUID_H6_15, fill_opacity=0.35, stroke_width=0
        ).move_to([-1.35, 0.0, 0.0])

        flow_a1 = Arrow([-2.1, 0.50, 0], [-1.0, 0.50, 0], color=COL_FLUID_H6_15, stroke_width=3, tip_length=0.12)
        flow_a2 = Arrow([-2.2, 0.00, 0], [-0.9, 0.00, 0], color=COL_FLUID_H6_15, stroke_width=3.5, tip_length=0.14)
        flow_a3 = Arrow([-2.1, -0.50, 0], [-1.0, -0.50, 0], color=COL_FLUID_H6_15, stroke_width=3, tip_length=0.12)
        badge_fluid_p = _h6_15_badge("แรงดันของไหล (P)", COL_FLUID_H6_15).move_to([-4.85, 0.0, 0.0])
        arr_fluid_in = Arrow([-3.65, 0.0, 0], [-2.35, 0.0, 0], color=COL_FLUID_H6_15, stroke_width=3.5, tip_length=0.14)
        flow_arrows = VGroup(flow_a1, flow_a2, flow_a3, badge_fluid_p, arr_fluid_in)

        # O-ring physically MOVES to the right wall (from x=0.0 to x=0.72)
        # Contacting right wall (x=+1.80)
        # Ellipse right edge at 0.72 + 2.10/2 = 1.77 -> firmly pressed against 1.80!
        oring_target_pos = np.array([0.72, 0.0, 0.0])

        # Sealing contact force arrows at the 3rd surface (right wall) + top + bottom
        f_right1 = Arrow([1.80, 0.40, 0], [1.35, 0.40, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.10)
        f_right2 = Arrow([1.80, 0.00, 0], [1.30, 0.00, 0], color=COL_WARN, stroke_width=3.0, tip_length=0.12)
        f_right3 = Arrow([1.80, -0.40, 0], [1.35, -0.40, 0], color=COL_WARN, stroke_width=2.5, tip_length=0.10)
        lbl_3rd = Text("ผิวที่ 3 (Third Surface)\nถูกอัดแน่นตามแรงดัน", font_size=10, color=COL_WARN).next_to(f_right2, RIGHT, buff=0.45)
        third_surface_grp = VGroup(f_right1, f_right2, f_right3, lbl_3rd)

        banner2 = _h6_15_banner(
            "แรงดันของไหลดัน O-ring แนบชิดผิวที่ 3 แน่นขึ้น — ยิ่งแรงดันสูง ยิ่งปิดผนึกแน่นสนิทเอง!",
            COL_OK
        )

        self.play(
            FadeIn(fluid_rect),
            FadeIn(flow_arrows),
            oring_s1.animate.move_to(oring_target_pos),
            FadeIn(banner2),
            run_time=1.0
        )
        self.play(FadeIn(third_surface_grp), run_time=0.6)
        self.wait(5.8)  # Checkpoint 20.0s falls here

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 24.6–34.0: State 3 (Excessive Pressure -> Extrusion Failure)
        # ----------------------------------------------------------------------
        cap3 = _h6_15_caption_top("3. ปัญหา: แรงดันสูงเกินไป → O-ring ทะลักเข้าช่องว่าง (Extrusion)", color=COL_WARN)
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.6)

        # Housing with CLEARANCE GAP on top-right (exaggerated for explanation)
        gap_metal_top = Rectangle(width=7.2, height=0.8, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([0.0, 1.40, 0.0])
        gap_metal_bot_l = Rectangle(width=1.8, height=1.6, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([-2.7, 0.20, 0.0])
        gap_metal_bot_floor = Rectangle(width=7.2, height=0.8, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([0.0, -1.40, 0.0])
        # Right shoulder: height 1.2 (top at y=0.60 instead of 1.00), leaving clear gap of 0.40 between 0.60 and 1.00
        gap_metal_bot_r = Rectangle(width=1.8, height=1.2, color=COL_METAL, fill_color="#334155").set_fill("#334155", 0.95).move_to([2.7, 0.00, 0.0])

        gap_housing = VGroup(gap_metal_top, gap_metal_bot_l, gap_metal_bot_floor, gap_metal_bot_r)

        # Clearance gap highlight / label placed cleanly in the open right margin
        gap_box = Rectangle(width=1.6, height=0.40, color=YELLOW, stroke_width=2, fill_opacity=0.15, fill_color=YELLOW).move_to([2.6, 0.80, 0.0])
        arr_gap = Arrow([4.3, 0.80, 0], [3.45, 0.80, 0], color=YELLOW, stroke_width=2.5, tip_length=0.10)
        lbl_gap = Text("Clearance Gap\n(ช่องว่างระหว่างชิ้นส่วน)", font_size=10.5, color=YELLOW).next_to(arr_gap, RIGHT, buff=0.15)
        gap_callout = VGroup(gap_box, arr_gap, lbl_gap)

        # Normal O-ring sitting in groove right side before extrusion
        oring_pre_ext = Ellipse(
            width=2.10, height=1.94,
            color="#38BDF8", stroke_width=3.5,
            fill_color="#0F172A", fill_opacity=0.95
        ).move_to([0.72, 0.0, 0.0])

        # Intense high-pressure fluid arrows and callout
        fluid_rect_high = Rectangle(
            width=2.5, height=1.92,
            color=COL_FLUID_H6_15, fill_color=COL_FLUID_H6_15, fill_opacity=0.45, stroke_width=0
        ).move_to([-1.0, 0.0, 0.0])
        h_arr1 = Arrow([-2.2, 0.45, 0], [-0.5, 0.45, 0], color=COL_FLUID_H6_15, stroke_width=4.5, tip_length=0.18)
        h_arr2 = Arrow([-2.2, -0.45, 0], [-0.5, -0.50, 0], color=COL_FLUID_H6_15, stroke_width=4.5, tip_length=0.18)
        badge_high_p = _h6_15_badge("แรงดันสูงมหาศาล!", COL_FLUID_H6_15).move_to([-4.85, 0.0, 0.0])
        arr_high_in = Arrow([-3.65, 0.0, 0], [-2.35, 0.0, 0], color=COL_FLUID_H6_15, stroke_width=4, tip_length=0.16)
        high_p_grp = VGroup(fluid_rect_high, h_arr1, h_arr2, badge_high_p, arr_high_in)

        # GENUINE SHAPE DEFORMATION: O-ring with a prominent extruded tongue poking into clearance gap!
        # Hand-crafted polygon with extruded lobe reaching into the gap (x=1.8 to 2.5, y=0.62 to 0.95)
        ext_pts = [
            [0.72 - 1.05, 0.0, 0],       # left center (-0.33, 0.0)
            [0.72 - 0.75, 0.75, 0],      # top left
            [0.72 + 0.30, 0.97, 0],      # top wall contact
            [1.80, 0.97, 0],             # entering clearance gap top
            [2.45, 0.95, 0],             # EXTRUDED TIP TOP (deep in gap!)
            [2.50, 0.78, 0],             # EXTRUDED TIP RIGHT END
            [2.40, 0.62, 0],             # EXTRUDED TIP BOTTOM
            [1.80, 0.62, 0],             # entering gap bottom edge
            [1.80, 0.20, 0],             # right wall contact
            [1.80, -0.50, 0],            # right wall bottom
            [1.40, -0.97, 0],            # bottom right
            [0.72, -0.97, 0],            # bottom floor contact
            [0.72 - 0.75, -0.75, 0],     # bottom left
        ]
        oring_extruded = Polygon(
            *ext_pts,
            color=COL_WARN, stroke_width=3.5,
            fill_color="#451A03", fill_opacity=0.95
        )

        arr_ext_warn = Arrow([4.3, 0.80, 0], [2.65, 0.80, 0], color=COL_WARN, stroke_width=3, tip_length=0.12)
        lbl_ext_warn = _h6_15_badge("เนื้อยางทะลัก (Extrusion) เสี่ยงฉีกขาด!", COL_WARN).next_to(arr_ext_warn, RIGHT, buff=0.12)
        ext_callout = VGroup(arr_ext_warn, lbl_ext_warn)

        banner3 = _h6_15_banner("ช่องว่างระหว่างชิ้นส่วนเป็นจุดอ่อน — แรงดันสูงดันให้ยางทะลักและฉีกขาด", COL_WARN)

        self.play(
            FadeIn(gap_housing),
            FadeIn(gap_callout),
            FadeIn(high_p_grp),
            FadeIn(oring_pre_ext),
            FadeIn(banner3),
            run_time=1.0
        )
        self.wait(0.8)
        self.play(FadeOut(gap_callout), run_time=0.4)

        # Real transform showing visible extrusion protrusion! Fade in extrusion alert
        self.play(
            Transform(oring_pre_ext, oring_extruded),
            FadeIn(ext_callout),
            run_time=1.0
        )
        self.wait(5.0)  # Checkpoint 30.0s falls here

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 34.6–44.0: State 4 (Solution: Back-Up Ring Blocks Gap)
        # ----------------------------------------------------------------------
        cap4 = _h6_15_caption_top("4. ทางแก้: ติดตั้ง Back-Up Ring บล็อกช่องว่าง ป้องกันการทะลัก")
        self.play(FadeIn(cap4, shift=UP * 0.35), run_time=0.6)

        # Same gap housing
        gap_housing_copy = gap_housing.copy()
        high_p_grp_copy = high_p_grp.copy()

        # Rigid Back-Up Ring: firm rectangular block placed on downstream side (x=1.35 to 1.80)
        # Blocking entrance to clearance gap!
        backup_ring = Rectangle(
            width=0.55, height=1.92, color=COL_OK
        ).set_fill("#334155", 0.95).set_stroke(COL_OK, 3.0).move_to([1.52, 0.0, 0.0])
        lbl_bu = Text("Back-Up Ring\n(แหวนกันทะลัก)", font_size=10.5, color=COL_OK).next_to(backup_ring, UP, buff=0.35)
        bu_grp = VGroup(backup_ring, lbl_bu)

        # O-Ring contained: healthy round/oval shape pressed against back-up ring (NOT extruded!)
        oring_contained = Ellipse(
            width=1.90, height=1.94,
            color="#38BDF8", stroke_width=3.5,
            fill_color="#0F172A", fill_opacity=0.95
        ).move_to([0.30, 0.0, 0.0])

        banner4 = _h6_15_banner("แหวนแข็ง Back-Up Ring ปิดกั้นช่องว่างฝั่งท้ายน้ำ — แรงดันสูงแค่ไหนก็ไม่ทะลัก!", COL_OK)

        self.play(
            FadeIn(gap_housing_copy),
            FadeIn(high_p_grp_copy),
            FadeIn(oring_pre_ext),
            run_time=0.8
        )
        self.wait(0.4)

        # Back-up ring slides in and O-ring returns to healthy contained shape
        self.play(
            FadeIn(bu_grp, shift=DOWN * 0.2),
            Transform(oring_pre_ext, oring_contained),
            FadeIn(banner4),
            run_time=1.0
        )
        self.play(
            Indicate(backup_ring, color=YELLOW, scale_factor=1.15),
            run_time=0.6
        )
        self.wait(4.6)  # Checkpoint t≈36.0s falls inside this hold period

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 44.6–50.0: Summary Card
        # ----------------------------------------------------------------------
        card_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: กลไก O-Ring และ Back-Up Ring (hydraulic06 น.18)", font_size=14, color=COL_OK).move_to([0.0, 1.35, 0.0])
        rows = [
            "1. ติดตั้ง (Initial Squeeze): บีบอัด O-ring บน-ล่างในร่องเพื่อปิดผนึกขั้นต้นเมื่อยังไม่มีแรงดัน",
            "2. Self-Energizing: เมื่อมีแรงดัน ของไหลจะผลัก O-ring อัดแน่นกับผิวที่ 3 ยิ่งแรงดันสูงยิ่งแน่น",
            "3. การทะลัก (Extrusion): แรงดันสูงเกินไปจะบี้ O-ring ให้ไหลปลิ้นเข้า Clearance Gap จนฉีกขาด",
            "4. Back-Up Ring: ใส่แหวนแข็งฝั่งแรงดันต่ำเพื่อปิดบล็อกช่องว่าง ป้องกัน O-ring ปลิ้นเสียหายได้อย่างสมบูรณ์"
        ]
        s_rows = VGroup(*[Text(r, font_size=11, color=WHITE) for r in rows]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0.0, -0.15, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(4.6)  # Checkpoint 47.0s falls here

        # ----------------------------------------------------------------------
        # BEAT 50.0–55.0: Review Question Card
        # ----------------------------------------------------------------------
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "ระบบไฮดรอลิกแรงดันสูงมากที่มีช่องว่าง Clearance Gap ระหว่างชิ้นส่วน\nควรเสริมอุปกรณ์ใดเข้าไปในร่องซีล เพื่อป้องกัน O-Ring เสียหาย?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: เสริม Back-Up Ring (แหวนกันทะลัก) ด้านท้ายน้ำ (Low-Pressure Side)\nเพื่อปิดบล็อกช่องว่าง ไม่ให้เนื้อยาง O-Ring ทะลัก (Extrude) เข้าไปจนฉีกขาด)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(4.4)  # Checkpoint 52.0s falls here

        self.play(FadeOut(question_grp), run_time=0.6)
        self.wait(0.4)
        self.fade_out_all(run_time=0.8)
        self.wait(0.5)


# ==============================================================================
# SCENE 16: H6_16_CompressionPackings1 (Compression Packing: ติดตั้งให้ถูกวิธี)
# hydraulic06.pdf page 19
# ==============================================================================

def _h6_16_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_16_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_16_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_16_banner(text, color):
    lbl = Text(text, font_size=11, color=color)
    bg = RoundedRectangle(
        width=min(12.6, max(lbl.width + 0.6, 9.5)),
        height=0.50,
        corner_radius=0.1,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.62, 0.0])
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_16_badge(text, color):
    lbl = Text(text, font_size=10.5, color=color)
    bg = RoundedRectangle(
        width=lbl.width + 0.35,
        height=0.34,
        corner_radius=0.08,
        color=color,
        fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_16_CompressionPackings1(SafeScene):
    def clear_stage(self, run_time=0.5):
        """Fade out all scene mobjects except persistent header."""
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        # ----------------------------------------------------------------------
        # BEAT 0.0–2.0: Title & Page Reference
        # ----------------------------------------------------------------------
        self.title_m = _h6_16_title("Compression Packing: ติดตั้งให้ถูกวิธี")
        self.ref_m = _h6_16_page_ref("hydraulic06 น.19")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)  # Checkpoint 1.5s falls here

        # ----------------------------------------------------------------------
        # BEAT 2.0–5.5: Hook Question
        # ----------------------------------------------------------------------
        hook_q = _h6_16_caption_top("ยัดแหวนซ้อนเข้าไปในร่อง หันทิศไหนก็ได้ใช่ไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.9)  # Checkpoint 3.6s falls here
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 5.5–14.0: Beat 1 (Lip Direction: Must Face Pressure)
        # ----------------------------------------------------------------------
        cap1 = _h6_16_caption_top("1. ปากซีล (Lips) ต้องหันเข้าหาแรงดันเสมอ")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Side-by-side comparison cards
        card_w, card_h = 5.6, 3.8
        x_left, x_right = -3.2, 3.2

        # --- LEFT: WRONG (Lips face AWAY from pressure) ---
        box_wrong = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.12,
            color=COL_WARN
        ).set_fill(COL_BG_BOX, 0.90).move_to([x_left, 0.0, 0.0])
        badge_wrong = _h6_16_badge("ผิด: ปากหันหนีแรงดัน (Wrong)", COL_WARN).move_to([x_left, 1.45, 0.0])

        # Housing walls top & bottom on left
        wall_w_top = Rectangle(width=3.6, height=0.4, color=COL_METAL).set_fill("#334155", 0.95).move_to([x_left + 0.3, 0.95, 0.0])
        wall_w_bot = Rectangle(width=3.6, height=0.4, color=COL_METAL).set_fill("#334155", 0.95).move_to([x_left + 0.3, -0.95, 0.0])

        # Pressure arrows entering from left
        p_arr_w1 = Arrow([x_left - 2.2, 0.40, 0], [x_left - 1.0, 0.40, 0], color=COL_FLUID_H6_15, stroke_width=3.5, tip_length=0.14)
        p_arr_w2 = Arrow([x_left - 2.2, -0.40, 0], [x_left - 1.0, -0.40, 0], color=COL_FLUID_H6_15, stroke_width=3.5, tip_length=0.14)
        p_lbl_w = Text("แรงดัน (P)", font_size=10, color=COL_FLUID_H6_15).move_to([x_left - 1.6, 0.0, 0.0])

        # V-ring polygon: point of V faces LEFT, lips open towards RIGHT (away from pressure)
        # Squeezed inward by pressure!
        pts_v_wrong = [
            [x_left - 0.7, 0.0, 0],      # Apex facing pressure
            [x_left + 0.5, 0.65, 0],     # Top lip (collapsed inward, leaving gap to wall 0.95)
            [x_left + 0.2, 0.65, 0],     # Inner top
            [x_left - 0.4, 0.0, 0],      # Inner apex
            [x_left + 0.2, -0.65, 0],    # Inner bot
            [x_left + 0.5, -0.65, 0],    # Bot lip (collapsed inward)
        ]
        poly_v_wrong = Polygon(*pts_v_wrong, color=COL_WARN).set_fill("#451A03", 0.95).set_stroke(COL_WARN, 3.0)

        # Red leak arrows slipping past collapsed lips!
        leak_arr1 = Arrow([x_left + 0.2, 0.85, 0], [x_left + 1.8, 0.85, 0], color=COL_FLUID_H6_15, stroke_width=2.5, tip_length=0.10)
        leak_arr2 = Arrow([x_left + 0.2, -0.85, 0], [x_left + 1.8, -0.85, 0], color=COL_FLUID_H6_15, stroke_width=2.5, tip_length=0.10)
        lbl_leak_warn = Text("แรงดันบีบปากหุบเข้า → รั่ว!", font_size=10.5, color=COL_WARN).move_to([x_left + 0.4, -1.45, 0.0])

        grp_wrong = VGroup(box_wrong, badge_wrong, wall_w_top, wall_w_bot, p_arr_w1, p_arr_w2, p_lbl_w,
                           poly_v_wrong, leak_arr1, leak_arr2, lbl_leak_warn)

        # --- RIGHT: CORRECT (Lips face TOWARD pressure) ---
        box_right = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.12,
            color=COL_OK
        ).set_fill(COL_BG_BOX, 0.90).move_to([x_right, 0.0, 0.0])
        badge_right = _h6_16_badge("ถูกต้อง: ปากหันสู้แรงดัน (Correct)", COL_OK).move_to([x_right, 1.45, 0.0])

        wall_r_top = Rectangle(width=3.6, height=0.4, color=COL_METAL).set_fill("#334155", 0.95).move_to([x_right - 0.3, 0.95, 0.0])
        wall_r_bot = Rectangle(width=3.6, height=0.4, color=COL_METAL).set_fill("#334155", 0.95).move_to([x_right - 0.3, -0.95, 0.0])

        p_arr_r1 = Arrow([x_right - 2.2, 0.40, 0], [x_right - 1.0, 0.40, 0], color=COL_FLUID_H6_15, stroke_width=3.5, tip_length=0.14)
        p_arr_r2 = Arrow([x_right - 2.2, -0.40, 0], [x_right - 1.0, -0.40, 0], color=COL_FLUID_H6_15, stroke_width=3.5, tip_length=0.14)
        p_lbl_r = Text("แรงดัน (P)", font_size=10, color=COL_FLUID_H6_15).move_to([x_right - 1.6, 0.0, 0.0])

        # V-ring polygon: lips open towards LEFT (facing pressure), apex points RIGHT!
        # Lips flare tightly against walls at y=0.75 and -0.75!
        pts_v_right = [
            [x_right + 0.7, 0.0, 0],     # Apex facing downstream
            [x_right - 0.5, 0.75, 0],    # Top lip flared firmly against top wall
            [x_right - 0.2, 0.75, 0],    # Inner top
            [x_right + 0.4, 0.0, 0],     # Inner apex
            [x_right - 0.2, -0.75, 0],   # Inner bot
            [x_right - 0.5, -0.75, 0],   # Bot lip flared firmly against bot wall
        ]
        poly_v_right = Polygon(*pts_v_right, color=COL_OK).set_fill("#064E3B", 0.95).set_stroke(COL_OK, 3.0)

        # Sealing force contact arrows pressing outward into walls
        f_press_top = Arrow([x_right - 0.1, 0.35, 0], [x_right - 0.3, 0.72, 0], color=COL_OK, stroke_width=2.5, tip_length=0.10)
        f_press_bot = Arrow([x_right - 0.1, -0.35, 0], [x_right - 0.3, -0.72, 0], color=COL_OK, stroke_width=2.5, tip_length=0.10)
        lbl_right_ok = Text("แรงดันดันปากบานออก → ซีลแน่น!", font_size=10.5, color=COL_OK).move_to([x_right + 0.3, -1.45, 0.0])

        grp_right = VGroup(box_right, badge_right, wall_r_top, wall_r_bot, p_arr_r1, p_arr_r2, p_lbl_r,
                            poly_v_right, f_press_top, f_press_bot, lbl_right_ok)

        banner1 = _h6_16_banner("แรงดันดันปากให้บานออกกดผนังแน่นขึ้นเอง (Self-Energizing) เหมือน O-Ring จาก H6_15!", COL_OK)

        self.play(
            FadeIn(grp_wrong, shift=UP * 0.25),
            FadeIn(grp_right, shift=UP * 0.25),
            FadeIn(banner1),
            run_time=1.0
        )
        # Sequential Indicate (never in same play as FadeIn per Lesson 5)
        self.play(Indicate(poly_v_wrong, color=COL_WARN), run_time=0.6)
        self.play(Indicate(poly_v_right, color=COL_OK), run_time=0.6)
        self.wait(5.0)  # Checkpoint 10.0s falls inside this hold

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 14.6–23.0: Beat 2 (Stagger Joints: 180° then 90°)
        # ----------------------------------------------------------------------
        cap2 = _h6_16_caption_top("2. รอยต่อแต่ละวงต้องเยื้องกัน (Stagger All Joints)")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Stuffing box housing cavity: width 6.0, height 2.6
        box_outer = RoundedRectangle(width=8.0, height=3.0, corner_radius=0.12, color=COL_METAL).set_fill("#334155", 0.95).move_to([0.0, 0.05, 0.0])
        box_cavity = Rectangle(width=6.0, height=2.2, color=BLACK).set_fill("#0F172A", 1.0).move_to([0.0, 0.05, 0.0])

        # 4 Horizontal Packing Rings stacked vertically
        y_rings = [0.72, 0.27, -0.18, -0.63]
        ring_h = 0.38

        # --- WRONG STATE: All 4 cut joints aligned at x = 0.0 ---
        rings_wrong_mobs = []
        cut_markers_wrong = []
        for y_r in y_rings:
            r_left = Rectangle(width=2.85, height=ring_h, color=COL_WARN).set_fill("#1E293B", 0.95).set_stroke(COL_WARN, 1.5).move_to([-1.45, y_r, 0.0])
            r_right = Rectangle(width=2.85, height=ring_h, color=COL_WARN).set_fill("#1E293B", 0.95).set_stroke(COL_WARN, 1.5).move_to([1.45, y_r, 0.0])
            cut_dot = Dot([0.0, y_r, 0.0], radius=0.08, color=RED)
            rings_wrong_mobs.extend([r_left, r_right])
            cut_markers_wrong.append(cut_dot)

        stack_wrong_grp = VGroup(*rings_wrong_mobs, *cut_markers_wrong)

        # Red leak path line cutting straight down through all 4 aligned joints!
        leak_path_line = Arrow([0.0, 1.50, 0.0], [0.0, -1.15, 0.0], color=RED, stroke_width=4.5, tip_length=0.16)
        lbl_leak_col = _h6_16_badge("รอยต่อตรงกัน = ช่องรั่วทะลุตลอดแนว!", COL_WARN).move_to([0.0, 1.85, 0.0])
        leak_alert_grp = VGroup(leak_path_line, lbl_leak_col)

        banner2_wrong = _h6_16_banner("หากรอยต่อทุกวงอยู่แนวเดียวกัน ของไหลจะไหลทะลุช่องรอยต่อได้ทันที!", COL_WARN)

        self.play(
            FadeIn(box_outer),
            FadeIn(box_cavity),
            FadeIn(stack_wrong_grp),
            FadeIn(banner2_wrong),
            run_time=0.8
        )
        self.play(FadeIn(leak_alert_grp, shift=DOWN * 0.2), run_time=0.6)
        self.wait(1.5)  # Checkpoint 18.0s first check (aligned state)

        # --- RIGHT STATE: Staggered joints (alternating -1.5, +1.5, -0.6, +0.6) ---
        x_staggers = [-1.6, 1.6, -0.7, 0.7]
        rings_right_mobs = []
        cut_markers_right = []
        for i, y_r in enumerate(y_rings):
            x_cut = x_staggers[i]
            w_l = (x_cut - (-2.9))
            w_r = (2.9 - x_cut)
            pos_l = -2.9 + w_l / 2.0
            pos_r = x_cut + w_r / 2.0
            r_l = Rectangle(width=w_l, height=ring_h, color=COL_OK).set_fill("#1E293B", 0.95).set_stroke(COL_OK, 1.5).move_to([pos_l, y_r, 0.0])
            r_r = Rectangle(width=w_r, height=ring_h, color=COL_OK).set_fill("#1E293B", 0.95).set_stroke(COL_OK, 1.5).move_to([pos_r, y_r, 0.0])
            cut_dot = Dot([x_cut, y_r, 0.0], radius=0.08, color=YELLOW)
            rings_right_mobs.extend([r_l, r_r])
            cut_markers_right.append(cut_dot)

        stack_right_grp = VGroup(*rings_right_mobs, *cut_markers_right)
        badge_stagger = _h6_16_badge("เยื้องสลับ 180° แล้ว 90° ปิดกั้นทางรั่วสนิท", COL_OK).move_to([0.0, 1.85, 0.0])
        banner2_right = _h6_16_banner("รอยต่อต้องเยื้องสลับกัน 180° แล้ว 90° — ปลายรอยต่อเกยกันเล็กน้อย ห้ามตัดแหวนขาด", COL_OK)

        self.play(
            FadeOut(leak_alert_grp),
            FadeOut(banner2_wrong),
            run_time=0.4
        )
        self.play(
            Transform(stack_wrong_grp, stack_right_grp),
            FadeIn(badge_stagger),
            FadeIn(banner2_right),
            run_time=1.0
        )
        self.wait(4.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 23.6–31.0: Beat 3 (Surface Finish: 32 RMS Static vs 16 RMS Dynamic)
        # ----------------------------------------------------------------------
        cap3 = _h6_16_caption_top("3. ผิวสัมผัส: ฝั่งเคลื่อนที่ต้องเรียบกว่าฝั่งนิ่ง (Surface Finish)")
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        card3_w, card3_h = 5.6, 3.8

        # --- LEFT: STATIC SURFACE (32 RMS) ---
        box_static = RoundedRectangle(width=card3_w, height=card3_h, corner_radius=0.12, color=COL_GRAY).set_fill(COL_BG_BOX, 0.90).move_to([x_left, 0.0, 0.0])
        badge_static = _h6_16_badge("Static Surface Finish — 32 RMS", COL_GRAY).move_to([x_left, 1.45, 0.0])
        lbl_static_desc = Text("ผนังเรือนสูบ (อยู่นิ่ง ไม่ขยับ)\nยอมให้มีความหยาบได้มากกว่า", font_size=11, color=WHITE).move_to([x_left, 0.85, 0.0])

        # Coarse zigzag profile (large amplitude 0.28, low frequency: 14 vertices across width 4.2)
        n_coarse = 14
        xs_c = np.linspace(x_left - 2.1, x_left + 2.1, n_coarse)
        pts_coarse = []
        for idx, x in enumerate(xs_c):
            y = 0.0 + (0.28 if idx % 2 == 0 else -0.28)
            pts_coarse.append([x, y, 0.0])
        line_static = VMobject(color=COL_GRAY, stroke_width=3.5).set_points_as_corners([np.array(p) for p in pts_coarse])
        lbl_rms32 = _h6_16_badge("32 RMS (ผิวหยาบกว่า)", COL_GRAY).move_to([x_left, -0.85, 0.0])

        grp_static = VGroup(box_static, badge_static, lbl_static_desc, line_static, lbl_rms32)

        # --- RIGHT: DYNAMIC SURFACE (16 RMS) ---
        box_dynamic = RoundedRectangle(width=card3_w, height=card3_h, corner_radius=0.12, color=COL_OK).set_fill(COL_BG_BOX, 0.90).move_to([x_right, 0.0, 0.0])
        badge_dynamic = _h6_16_badge("Dynamic Surface Finish — 16 RMS", COL_OK).move_to([x_right, 1.45, 0.0])
        lbl_dynamic_desc = Text("ผิวแกนก้านสูบ (เคลื่อนที่ตลอดเวลา)\nต้องเรียบเนียนเป็นพิเศษ ลดสึกหรอ", font_size=11, color=WHITE).move_to([x_right, 0.85, 0.0])

        # Fine zigzag profile (tiny amplitude 0.09, high frequency: 50 vertices across width 4.2)
        n_fine = 50
        xs_f = np.linspace(x_right - 2.1, x_right + 2.1, n_fine)
        pts_fine = []
        for idx, x in enumerate(xs_f):
            y = 0.0 + (0.09 if idx % 2 == 0 else -0.09)
            pts_fine.append([x, y, 0.0])
        line_dynamic = VMobject(color=COL_OK, stroke_width=3.0).set_points_as_corners([np.array(p) for p in pts_fine])
        lbl_rms16 = _h6_16_badge("16 RMS (เรียบเนียนกว่า 2 เท่า)", COL_OK).move_to([x_right, -0.85, 0.0])

        grp_dynamic = VGroup(box_dynamic, badge_dynamic, lbl_dynamic_desc, line_dynamic, lbl_rms16)

        banner3 = _h6_16_banner("ผิว Dynamic (16 RMS) ต้องเรียบกว่า Static (32 RMS) เพื่อลดการเสียดสีและการสึกหรอของซีล", COL_OK)

        self.play(
            FadeIn(grp_static, shift=UP * 0.25),
            FadeIn(grp_dynamic, shift=UP * 0.25),
            FadeIn(banner3),
            run_time=1.0
        )
        self.wait(5.8)  # Checkpoint 27.0s falls inside this hold

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 31.6–40.0: Beat 4 (Assembly Order & Shim Protection)
        # ----------------------------------------------------------------------
        cap4 = _h6_16_caption_top("4. ลำดับติดตั้ง + เสริม Shim กันปากซีลบี้แตก")
        self.play(FadeIn(cap4, shift=UP * 0.35), run_time=0.5)

        # Housing box cavity on left (x=-1.5)
        cavity_bg = Rectangle(width=3.2, height=3.6, color=COL_METAL).set_fill("#1E293B", 0.95).move_to([-1.5, 0.0, 0.0])

        # 1. Male / Bottom Adapter Ring (first!)
        adapter_bot = Rectangle(width=2.8, height=0.50, color=COL_OK).set_fill("#064E3B", 0.95).set_stroke(COL_OK, 2.5).move_to([-1.5, -1.35, 0.0])
        lbl_step1 = _h6_16_badge("① ใส่ Male Adapter ก่อน (ล่างสุด)", COL_OK).move_to([2.4, -1.35, 0.0])
        arr_s1 = Arrow([1.0, -1.35, 0], [-0.05, -1.35, 0], color=COL_OK, stroke_width=2.5, tip_length=0.10)
        grp_s1 = VGroup(adapter_bot, lbl_step1, arr_s1)

        # 2. Packing Rings Stack (middle)
        r1 = Rectangle(width=2.8, height=0.38, color=COL_CURR).set_fill("#334155", 0.95).set_stroke(COL_CURR, 2.0).move_to([-1.5, -0.80, 0.0])
        r2 = Rectangle(width=2.8, height=0.38, color=COL_CURR).set_fill("#334155", 0.95).set_stroke(COL_CURR, 2.0).move_to([-1.5, -0.35, 0.0])
        r3 = Rectangle(width=2.8, height=0.38, color=COL_CURR).set_fill("#334155", 0.95).set_stroke(COL_CURR, 2.0).move_to([-1.5, 0.10, 0.0])
        lbl_step2 = _h6_16_badge("② ใส่แหวน Packing ซ้อนตามลำดับ", COL_CURR).move_to([2.4, -0.35, 0.0])
        arr_s2 = Arrow([1.0, -0.35, 0], [-0.05, -0.35, 0], color=COL_CURR, stroke_width=2.5, tip_length=0.10)
        grp_s2 = VGroup(r1, r2, r3, lbl_step2, arr_s2)

        # 3. Female / Top Adapter Ring (last!)
        adapter_top = Rectangle(width=2.8, height=0.50, color=COL_OK).set_fill("#064E3B", 0.95).set_stroke(COL_OK, 2.5).move_to([-1.5, 0.65, 0.0])
        lbl_step3 = _h6_16_badge("③ ใส่ Female Adapter ปิดท้าย", COL_OK).move_to([2.4, 0.65, 0.0])
        arr_s3 = Arrow([1.0, 0.65, 0], [-0.05, 0.65, 0], color=COL_OK, stroke_width=2.5, tip_length=0.10)
        grp_s3 = VGroup(adapter_top, lbl_step3, arr_s3)

        # 4. Gland Follower & Yellow Shim (protective strip)
        # Shim: distinct visible yellow strip between gland and top adapter!
        shim_strip = Rectangle(width=2.8, height=0.18, color=YELLOW).set_fill(YELLOW, 0.95).set_stroke(YELLOW, 2.0).move_to([-1.5, 1.05, 0.0])
        gland_block = Rectangle(width=3.2, height=0.50, color=COL_METAL).set_fill("#475569", 0.95).set_stroke(COL_METAL, 2.5).move_to([-1.5, 1.45, 0.0])
        lbl_shim = _h6_16_badge("④ เสริม Shim กันปากซีลถูกบี้แตก", YELLOW).move_to([2.4, 1.35, 0.0])
        arr_s4 = Arrow([1.0, 1.35, 0], [-0.05, 1.25, 0], color=YELLOW, stroke_width=2.5, tip_length=0.10)
        grp_s4 = VGroup(shim_strip, gland_block, lbl_shim, arr_s4)

        banner4 = _h6_16_banner("Gland ต้องแนบพอดี — หากแน่นเกินไปให้เสริม Shim เพื่อป้องกันปากซีลถูกบี้แตกเสียหาย", COL_OK)

        self.play(FadeIn(cavity_bg), FadeIn(grp_s1), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(grp_s2), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(grp_s3), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(grp_s4), FadeIn(banner4), run_time=1.0)
        self.wait(2.8)  # Checkpoint 36.0s falls inside this hold

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ----------------------------------------------------------------------
        # BEAT 40.6–45.0: Summary Card
        # ----------------------------------------------------------------------
        card_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: กฎ 4 ข้อในการติดตั้ง Compression Packing (hydraulic06 น.19)", font_size=13.5, color=COL_OK).move_to([0.0, 1.35, 0.0])
        rows = [
            "1. ปากซีล (Lips): ต้องหันเข้าหาแรงดันเสมอ เพื่อให้แรงดันช่วยดันปากบานออก (Self-Energizing)",
            "2. รอยต่อ (Joints): จัดเยื้องสลับ 180° แล้ว 90° ปลายเกยกันเล็กน้อย ห้ามรอยต่อตรงกันเด็ดขาด",
            "3. ผิวสัมผัส (RMS): ผิวฝั่งเคลื่อนที่ (Dynamic, 16 RMS) ต้องเรียบกว่าฝั่งอยู่นิ่ง (Static, 32 RMS)",
            "4. ลำดับ + Shim: ใส่ Male ก่อน Female ปิดท้าย และเสริม Shim ป้องกัน Gland บี้ปากซีลแตกเสียหาย"
        ]
        s_rows = VGroup(*[Text(r, font_size=11, color=WHITE) for r in rows]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0.0, -0.15, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(3.6)  # Checkpoint 42.0s falls here

        # ----------------------------------------------------------------------
        # BEAT 45.0–49.5: Review Question Card
        # ----------------------------------------------------------------------
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "หากช่างติดตั้งแหวน Compression Packing โดยหันปากซีล (Lips)\nออกจากทิศทางแรงดันของไหล จะเกิดผลเสียอย่างไรต่อระบบ?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: แรงดันของไหลจะดันให้ปากซีลหุบเข้า เกิดช่องว่างและของไหลจะรั่วไหลทันที\nตรงข้ามกับการหันปากสู้แรงดัน ที่แรงดันจะช่วยถ่างปากซีลให้แนบสนิทขึ้น)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.5)  # Checkpoint 47.0s falls here

        self.play(FadeOut(question_grp), run_time=0.5)
        self.wait(0.2)
        self.fade_out_all(run_time=0.6)
        self.wait(0.5)


# ==============================================================================
# SCENE 17: H6_17_CompressionPackings2 (hydraulic06.pdf page 20)
# Duration: ~50.0 seconds | 2D SafeScene
# Pedagogical Focus: Gland Assembly Vocabulary & 3 Adjustment Mechanisms
# AHA Moment:
#   Compression packings wear and relax over time. An adjustment mechanism is
#   essential to re-compress the stack without disassembly:
#   1. Threaded Follower: Screws into housing directly; compact but manual check needed.
#   2. Flanged Follower: Multiple bolts around flange; uniform pressure distribution.
#   3. Spring Loaded: Constant mechanical coil spring; automatic self-adjusting preload.
#   Single Ring Dimensional Vocabulary: Nominal I.D., Nominal O.D., Stack Height,
#   Heel Clearance, Interference.
# ==============================================================================

def _h6_17_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_17_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_17_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_17_badge(text, color):
    lbl = Text(text, font_size=11, color=color)
    bg = RoundedRectangle(
        width=lbl.width + 0.48, height=0.38, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_17_banner(text, color):
    bg = RoundedRectangle(
        width=11.8, height=0.52, corner_radius=0.1,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -1.95, 0.0])
    lbl = Text(text, font_size=12, color=color).move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_17_CompressionPackings2(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ======================================================================
        # BEAT 0.0–2.0: Title & Page Reference
        # ======================================================================
        self.title_m = _h6_17_title("Compression Packing: กลไกปรับความแน่น")
        self.ref_m = _h6_17_page_ref("hydraulic06 น.20")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)  # Checkpoint 1.5s falls here

        # ======================================================================
        # BEAT 2.0–5.5: Hook Question
        # ======================================================================
        hook_q = _h6_17_caption_top("ขันแน่นตอนติดตั้งครั้งเดียว ก็ใช้ได้ตลอดไปไม่ต้องยุ่งอีกจริงไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)  # Checkpoint 3.6s falls here
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.5)

        # ======================================================================
        # BEAT 5.5–13.6: Gland Assembly Vocabulary (Cross Section)
        # ======================================================================
        cap1 = _h6_17_caption_top("ส่วนประกอบชุด Gland: ตัวรองรับ + ปะเก็น + ตัวกด")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Main Shaft / Rod through center
        rod = Rectangle(width=7.8, height=0.9, color=COL_METAL).set_fill("#475569", 0.95).move_to([-0.8, 0.0, 0.0])
        rod_axis = DashedLine([-4.7, 0.0, 0.0], [3.1, 0.0, 0.0], color="#94A3B8", stroke_width=1.5, dash_length=0.15)

        # Upper Stuffing Box Housing
        house_top = Polygon(
            [-4.2, 0.45, 0], [-4.2, 1.45, 0], [0.3, 1.45, 0], [0.3, 1.15, 0],
            [-0.7, 1.15, 0], [-0.7, 0.45, 0],
            color=COL_METAL, fill_color="#334155", fill_opacity=0.95
        )
        # Lower Stuffing Box Housing
        house_bot = Polygon(
            [-4.2, -0.45, 0], [-4.2, -1.45, 0], [0.3, -1.45, 0], [0.3, -1.15, 0],
            [-0.7, -1.15, 0], [-0.7, -0.45, 0],
            color=COL_METAL, fill_color="#334155", fill_opacity=0.95
        )
        housing_grp = VGroup(house_top, house_bot)

        # 1. Male Supporting Ring (left end of cavity, supporting back of packings)
        male_t = Polygon(
            [-3.6, 0.45, 0], [-3.6, 1.15, 0], [-3.25, 1.15, 0], [-3.05, 0.80, 0], [-3.25, 0.45, 0],
            color=COL_OK, fill_color="#064E3B", fill_opacity=0.95
        ).set_stroke(COL_OK, 1.8)
        male_b = Polygon(
            [-3.6, -0.45, 0], [-3.6, -1.15, 0], [-3.25, -1.15, 0], [-3.05, -0.80, 0], [-3.25, -0.45, 0],
            color=COL_OK, fill_color="#064E3B", fill_opacity=0.95
        ).set_stroke(COL_OK, 1.8)
        male_ring = VGroup(male_t, male_b)

        # 2. Packings (stack of 3 V-rings, chevron facing left < < <)
        pack_t_list, pack_b_list = [], []
        x_starts = [-3.15, -2.75, -2.35]
        for xs in x_starts:
            pt = Polygon(
                [xs, 0.45, 0], [xs + 0.20, 0.80, 0], [xs, 1.15, 0],
                [xs + 0.35, 1.15, 0], [xs + 0.55, 0.80, 0], [xs + 0.35, 0.45, 0],
                color=COL_FIELD, fill_color="#0284C7", fill_opacity=0.95
            ).set_stroke(COL_FIELD, 1.5)
            pb = Polygon(
                [xs, -0.45, 0], [xs + 0.20, -0.80, 0], [xs, -1.15, 0],
                [xs + 0.35, -1.15, 0], [xs + 0.55, -0.80, 0], [xs + 0.35, -0.45, 0],
                color=COL_FIELD, fill_color="#0284C7", fill_opacity=0.95
            ).set_stroke(COL_FIELD, 1.5)
            pack_t_list.append(pt)
            pack_b_list.append(pb)
        packings_grp = VGroup(*pack_t_list, *pack_b_list)

        # 3. Female Support Ring (outer adapter mating with V-groove)
        fem_t = Polygon(
            [-1.95, 0.45, 0], [-1.75, 0.80, 0], [-1.95, 1.15, 0],
            [-1.55, 1.15, 0], [-1.55, 0.45, 0],
            color="#A855F7", fill_color="#581C87", fill_opacity=0.95
        ).set_stroke("#A855F7", 1.8)
        fem_b = Polygon(
            [-1.95, -0.45, 0], [-1.75, -0.80, 0], [-1.95, -1.15, 0],
            [-1.55, -1.15, 0], [-1.55, -0.45, 0],
            color="#A855F7", fill_color="#581C87", fill_opacity=0.95
        ).set_stroke("#A855F7", 1.8)
        female_ring = VGroup(fem_t, fem_b)

        # 4. Shim (thin spacer strip at housing face, x from 0.3 to 0.45)
        shim_t = Rectangle(width=0.15, height=0.55, color=YELLOW).set_fill(YELLOW, 0.95).move_to([0.38, 1.42, 0.0])
        shim_b = Rectangle(width=0.15, height=0.55, color=YELLOW).set_fill(YELLOW, 0.95).move_to([0.38, -1.42, 0.0])
        shim_grp = VGroup(shim_t, shim_b)

        # 5. Gland Follower Ring (nose pushes against female ring, flange bolted outside)
        fol_nose_t = Rectangle(width=1.9, height=0.68, color=COL_METAL).set_fill("#64748B", 0.95).move_to([-0.50, 0.80, 0.0])
        fol_flange_t = Rectangle(width=0.40, height=0.75, color=COL_METAL).set_fill("#64748B", 0.95).move_to([0.65, 1.42, 0.0])
        fol_nose_b = Rectangle(width=1.9, height=0.68, color=COL_METAL).set_fill("#64748B", 0.95).move_to([-0.50, -0.80, 0.0])
        fol_flange_b = Rectangle(width=0.40, height=0.75, color=COL_METAL).set_fill("#64748B", 0.95).move_to([0.65, -1.42, 0.0])
        # Follower clamping studs & nuts
        stud_t = Rectangle(width=1.1, height=0.14, color=WHITE).set_fill("#E2E8F0", 1.0).move_to([0.45, 1.42, 0.0])
        nut_t = Rectangle(width=0.22, height=0.30, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([0.95, 1.42, 0.0])
        stud_b = Rectangle(width=1.1, height=0.14, color=WHITE).set_fill("#E2E8F0", 1.0).move_to([0.45, -1.42, 0.0])
        nut_b = Rectangle(width=0.22, height=0.30, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([0.95, -1.42, 0.0])
        follower_ring = VGroup(fol_nose_t, fol_flange_t, fol_nose_b, fol_flange_b, stud_t, nut_t, stud_b, nut_b)

        # Dimension: Gland Width (depth of cavity, from -3.6 to -0.7)
        dim_gw = DoubleArrow([-3.6, -1.35, 0], [-0.7, -1.35, 0], color=COL_OK, stroke_width=2.5, tip_length=0.12)
        lbl_gw = Text("GLAND WIDTH", font_size=10, color=COL_OK).next_to(dim_gw, DOWN, buff=0.08)
        gland_width_grp = VGroup(dim_gw, lbl_gw)

        # Callout Badges & Pointer Lines
        lbl_male = _h6_17_badge("Male Supporting Ring", COL_OK).move_to([-3.4, 1.85, 0.0])
        arr_male = Arrow([-3.4, 1.68, 0], [-3.35, 1.18, 0], color=COL_OK, stroke_width=2.0, tip_length=0.10)
        call_male = VGroup(lbl_male, arr_male)

        lbl_pack = _h6_17_badge("Packings", COL_FIELD).move_to([-1.8, 1.85, 0.0])
        arr_pack = Arrow([-1.8, 1.68, 0], [-2.35, 1.18, 0], color=COL_FIELD, stroke_width=2.0, tip_length=0.10)
        call_pack = VGroup(lbl_pack, arr_pack)

        lbl_shim = _h6_17_badge("Shim", YELLOW).move_to([0.4, 2.05, 0.0])
        arr_shim = Arrow([0.4, 1.88, 0], [0.38, 1.70, 0], color=YELLOW, stroke_width=2.0, tip_length=0.10)
        call_shim = VGroup(lbl_shim, arr_shim)

        lbl_fem = _h6_17_badge("Female Support Ring", "#A855F7").move_to([2.7, 0.75, 0.0])
        arr_fem = Arrow([1.7, 0.75, 0], [-1.55, 0.80, 0], color="#A855F7", stroke_width=2.0, tip_length=0.10)
        call_fem = VGroup(lbl_fem, arr_fem)

        lbl_fol = _h6_17_badge("Gland Follower Ring", COL_METAL).move_to([2.7, -0.65, 0.0])
        arr_fol = Arrow([1.7, -0.65, 0], [0.85, -0.80, 0], color=COL_METAL, stroke_width=2.0, tip_length=0.10)
        call_fol = VGroup(lbl_fol, arr_fol)

        assembly_mobs = VGroup(
            rod, rod_axis, housing_grp,
            male_ring, packings_grp, female_ring,
            shim_grp, follower_ring, gland_width_grp,
            call_male, call_pack, call_shim, call_fem, call_fol
        )

        banner1 = _h6_17_banner(
            "ชุด gland มีตัวรองรับ (support ring) ประกบปะเก็น packing ไว้ แล้วมี follower ring กดอัดจากนอก",
            COL_OK
        )

        self.play(FadeIn(assembly_mobs, shift=UP * 0.2), FadeIn(banner1), run_time=1.0)
        # Sequential indicate of the 5 distinct parts (Lesson 5: strictly sequenced after FadeIn)
        self.play(
            LaggedStart(
                Indicate(call_male, color=COL_OK, scale_factor=1.08),
                Indicate(call_pack, color=COL_FIELD, scale_factor=1.08),
                Indicate(call_fem, color="#A855F7", scale_factor=1.08),
                Indicate(call_shim, color=YELLOW, scale_factor=1.08),
                Indicate(call_fol, color=COL_METAL, scale_factor=1.08),
                lag_ratio=0.35
            ),
            run_time=2.2
        )
        self.wait(3.9)  # Checkpoint 10.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 13.6–20.0: Method 1 - Threaded Follower (Real Thread Lines!)
        # ======================================================================
        cap2 = _h6_17_caption_top("Packing สึกหรอ/คลายตัวตามเวลา — ต้องมีกลไกปรับเพิ่มได้ (3 วิธี)")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Cross section of Threaded Follower mechanism on the left (x=-2.6)
        m1_house_l = Rectangle(width=0.9, height=3.2, color=COL_METAL).set_fill("#334155", 0.95).move_to([-3.9, 0.05, 0.0])
        m1_house_r = Rectangle(width=0.9, height=3.2, color=COL_METAL).set_fill("#334155", 0.95).move_to([-1.3, 0.05, 0.0])
        m1_cavity_bg = Rectangle(width=1.7, height=3.2, color=BLACK).set_fill("#0F172A", 1.0).move_to([-2.6, 0.05, 0.0])

        # Packing rings at bottom of cavity
        m1_p1 = Rectangle(width=1.65, height=0.32, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -1.25, 0.0])
        m1_p2 = Rectangle(width=1.65, height=0.32, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -0.90, 0.0])
        m1_p3 = Rectangle(width=1.65, height=0.32, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -0.55, 0.0])
        m1_packings = VGroup(m1_p1, m1_p2, m1_p3)

        # Threaded Follower Body
        m1_fol_body = Rectangle(width=1.65, height=1.30, color=COL_OK).set_fill("#1E293B", 0.95).move_to([-2.6, 0.35, 0.0])
        m1_fol_cap = Rectangle(width=2.10, height=0.40, color=COL_OK).set_fill("#0F766E", 1.0).move_to([-2.6, 1.15, 0.0])
        m1_cap_txt = Text("HEX HEAD", font_size=9, color=WHITE).move_to(m1_fol_cap.get_center())

        # REAL THREAD LINES: Angled parallel helical lines along both flanks!
        thread_lines = []
        for y_t in np.linspace(-0.15, 0.85, 7):
            tl = Line([-3.45, y_t - 0.06, 0], [-2.75, y_t + 0.06, 0], color=COL_OK, stroke_width=2.5)
            tr = Line([-2.45, y_t - 0.06, 0], [-1.75, y_t + 0.06, 0], color=COL_OK, stroke_width=2.5)
            thread_lines.extend([tl, tr])
        m1_threads = VGroup(*thread_lines)

        m1_follower = VGroup(m1_fol_body, m1_fol_cap, m1_cap_txt, m1_threads)

        # Right explanatory panel (x = 2.4)
        m1_card = RoundedRectangle(width=5.8, height=3.3, corner_radius=0.12, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([2.5, 0.05, 0.0])
        m1_head = _h6_17_badge("1. Threaded Follower (ขันเกลียวกดอัด)", COL_OK).move_to([2.5, 1.35, 0.0])
        m1_points = VGroup(
            Text("• มีเกลียวสกรูรอบตัว Follower ขันเข้ากับเกลียวเรือนสูบ", font_size=11, color=WHITE),
            Text("• เมื่อเริ่มหลวม ช่างใช้ประแจขันหมุนให้ลึกขึ้นเพื่อเพิ่มแรงกด", font_size=11, color=WHITE),
            Text("• ข้อดี: กะทัดรัด ประหยัดพื้นที่ เหมาะกับกระบอกขนาดเล็ก", font_size=11, color=COL_OK),
            Text("• ข้อจำกัด: ต้องมีช่างคอยตรวจเช็คและขันกวดเป็นประจำ", font_size=11, color=COL_WARN),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([2.5, 0.05, 0.0])
        m1_panel = VGroup(m1_card, m1_head, m1_points)

        banner2 = _h6_17_banner(
            "1. Threaded Follower: ขันเกลียวให้ลึกขึ้นเพื่อเพิ่มแรงกด — ต้องมีคนคอยตรวจ/ขันเป็นระยะ",
            COL_OK
        )

        m1_all = VGroup(m1_house_l, m1_house_r, m1_cavity_bg, m1_packings, m1_follower, m1_panel)
        self.play(FadeIn(m1_all, shift=UP * 0.25), FadeIn(banner2), run_time=0.8)

        # Tightening animation: Follower shifts DOWN to re-compress packings
        down_arrow = Arrow([-2.6, 1.70, 0], [-2.6, 1.38, 0], color=COL_CURR, stroke_width=4.0, tip_length=0.12)
        rot_badge = _h6_17_badge("ขันเกลียวลง ↷", COL_CURR).move_to([-2.6, 1.95, 0.0])
        tighten_cue = VGroup(down_arrow, rot_badge)

        self.play(FadeIn(tighten_cue), run_time=0.4)
        self.play(
            m1_follower.animate.shift(DOWN * 0.16),
            m1_packings.animate.stretch(0.90, dim=1, about_point=[-2.6, -1.4, 0]),
            run_time=1.0
        )
        self.wait(3.5)  # Checkpoint 17.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 20.6–26.0: Method 2 - Flanged Follower (Distinct Bolt Shapes!)
        # ======================================================================
        cap_f = _h6_17_caption_top("2. Flanged Follower: ขันน็อตรอบหน้าแปลน (แรงกดสม่ำเสมอ)")
        self.play(FadeIn(cap_f, shift=UP * 0.35), run_time=0.5)

        # Mechanism on Left: Flanged stuffing box with distinct hex bolts (x = -2.6)
        m2_house_l = Rectangle(width=0.9, height=3.0, color=COL_METAL).set_fill("#334155", 0.95).move_to([-3.9, -0.15, 0.0])
        m2_house_r = Rectangle(width=0.9, height=3.0, color=COL_METAL).set_fill("#334155", 0.95).move_to([-1.3, -0.15, 0.0])
        m2_cavity_bg = Rectangle(width=1.7, height=3.0, color=BLACK).set_fill("#0F172A", 1.0).move_to([-2.6, -0.15, 0.0])

        # Packings at bottom
        m2_p1 = Rectangle(width=1.65, height=0.32, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -1.35, 0.0])
        m2_p2 = Rectangle(width=1.65, height=0.32, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -1.00, 0.0])
        m2_p3 = Rectangle(width=1.65, height=0.32, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -0.65, 0.0])
        m2_packings = VGroup(m2_p1, m2_p2, m2_p3)

        # Flanged Follower: T-shape with wide flange wings
        m2_stem = Rectangle(width=1.65, height=1.0, color=COL_OK).set_fill("#1E293B", 0.95).move_to([-2.6, -0.05, 0.0])
        m2_flange = Rectangle(width=3.60, height=0.38, color=COL_OK).set_fill("#0F766E", 1.0).move_to([-2.6, 0.60, 0.0])

        # DISTINCT BOLT SHAPES (Lesson 1: Must show multiple distinct bolt shapes!)
        # Bolt 1 (Left): Hex head, washer, threaded stud into housing
        b1_head = Polygon([-4.25, 0.80, 0], [-4.05, 1.05, 0], [-3.75, 1.05, 0], [-3.55, 0.80, 0], color=WHITE, fill_color="#E2E8F0", fill_opacity=1.0)
        b1_stud = Rectangle(width=0.18, height=1.10, color=WHITE).set_fill("#94A3B8", 1.0).move_to([-3.90, 0.35, 0.0])
        b1_lbl = Text("Bolt 1", font_size=9, color=YELLOW).next_to(b1_head, UP, buff=0.08)
        bolt1 = VGroup(b1_head, b1_stud, b1_lbl)

        # Bolt 2 (Right): Hex head, washer, threaded stud into housing
        b2_head = Polygon([-1.65, 0.80, 0], [-1.45, 1.05, 0], [-1.15, 1.05, 0], [-0.95, 0.80, 0], color=WHITE, fill_color="#E2E8F0", fill_opacity=1.0)
        b2_stud = Rectangle(width=0.18, height=1.10, color=WHITE).set_fill("#94A3B8", 1.0).move_to([-1.30, 0.35, 0.0])
        b2_lbl = Text("Bolt 2", font_size=9, color=YELLOW).next_to(b2_head, UP, buff=0.08)
        bolt2 = VGroup(b2_head, b2_stud, b2_lbl)

        # Flange Face Pattern (Top/Front circular view with 4 distinct perimeter bolts)
        flange_circle = Circle(radius=0.65, color=COL_OK).set_fill("#1E293B", 0.95).move_to([-2.6, 1.55, 0.0])
        rod_hole = Circle(radius=0.25, color=COL_METAL).set_fill("#0F172A", 1.0).move_to([-2.6, 1.55, 0.0])
        b_dots = []
        for ang in [0, 90, 180, 270]:
            bx = -2.6 + 0.45 * np.cos(ang * DEGREES)
            by = 1.55 + 0.45 * np.sin(ang * DEGREES)
            b_dots.append(Dot([bx, by, 0], radius=0.07, color=YELLOW))
        lbl_4bolts = Text("4 Bolts รอบหน้าแปลน", font_size=8.5, color=YELLOW).next_to(flange_circle, UP, buff=0.06)
        flange_face_view = VGroup(flange_circle, rod_hole, *b_dots, lbl_4bolts)

        m2_mech = VGroup(m2_house_l, m2_house_r, m2_cavity_bg, m2_packings, m2_stem, m2_flange, bolt1, bolt2, flange_face_view)

        # Right explanatory panel (x = 2.5)
        m2_card = RoundedRectangle(width=5.8, height=3.3, corner_radius=0.12, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([2.5, 0.05, 0.0])
        m2_head = _h6_17_badge("2. Flanged Follower (หน้าแปลนขันน็อต)", COL_OK).move_to([2.5, 1.35, 0.0])
        m2_points = VGroup(
            Text("• ใช้แผ่นหน้าแปลนยึดด้วยน็อตหลายตัวรอบขอบ (Bolted Flange)", font_size=11, color=WHITE),
            Text("• การขันน็อตกระจายแรงกดได้สม่ำเสมอทั่วหน้าตัดรอบทิศทาง", font_size=11, color=WHITE),
            Text("• ข้อดี: แรงกดสมดุล ไม่เกิดการเอียงเบียดแกนก้านสูบ", font_size=11, color=COL_OK),
            Text("• ข้อควรระวัง: ต้องขันน็อตทแยงสลับกันให้หน้าแปลนขนานพอดี", font_size=11, color=COL_WARN),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([2.5, 0.05, 0.0])
        m2_panel = VGroup(m2_card, m2_head, m2_points)

        banner3 = _h6_17_banner(
            "2. Flanged Follower: ขันน็อตรอบหน้าแปลนให้แน่นสม่ำเสมอ — กระจายแรงกดทั่วถึงกว่าแบบเกลียวเดี่ยว",
            COL_OK
        )

        self.play(FadeIn(m2_mech, shift=UP * 0.25), FadeIn(m2_panel), FadeIn(banner3), run_time=0.8)
        # Sequentially indicate the 4 perimeter bolts and the 2 cross-section bolts
        self.play(
            LaggedStart(
                Indicate(bolt1, color=YELLOW, scale_factor=1.12),
                Indicate(bolt2, color=YELLOW, scale_factor=1.12),
                Indicate(flange_face_view, color=YELLOW, scale_factor=1.08),
                lag_ratio=0.3
            ),
            run_time=1.2
        )
        self.wait(3.0)  # Checkpoint 23.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 26.6–33.0: Method 3 - Spring Loaded (Real Coiled Zigzag Spring!)
        # ======================================================================
        cap_s = _h6_17_caption_top("3. Spring Loaded: สปริงกดอัตโนมัติ (ชดเชยการสึกหรอตลอดเวลา)")
        self.play(FadeIn(cap_s, shift=UP * 0.35), run_time=0.5)

        # Mechanism on Left: Stuffing box with internal coil spring (x = -2.6)
        m3_house_l = Rectangle(width=0.9, height=3.4, color=COL_METAL).set_fill("#334155", 0.95).move_to([-3.9, 0.0, 0.0])
        m3_house_r = Rectangle(width=0.9, height=3.4, color=COL_METAL).set_fill("#334155", 0.95).move_to([-1.3, 0.0, 0.0])
        m3_cavity_bg = Rectangle(width=1.7, height=3.4, color=BLACK).set_fill("#0F172A", 1.0).move_to([-2.6, 0.0, 0.0])

        # Packings at bottom of cavity
        m3_p1 = Rectangle(width=1.65, height=0.30, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -1.45, 0.0])
        m3_p2 = Rectangle(width=1.65, height=0.30, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -1.12, 0.0])
        m3_p3 = Rectangle(width=1.65, height=0.30, color=COL_FIELD).set_fill("#0284C7", 0.95).move_to([-2.6, -0.79, 0.0])
        m3_packings = VGroup(m3_p1, m3_p2, m3_p3)

        # Pressure plate between spring and packings
        m3_plate = Rectangle(width=1.65, height=0.15, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([-2.6, -0.55, 0.0])

        # REAL COIL SPRING (Lesson 1: Must show real zigzag/coil shape!)
        n_coils = 12
        y_pts = np.linspace(-0.45, 0.85, n_coils)
        spring_coords = []
        for idx, y_val in enumerate(y_pts):
            x_val = -3.15 if idx % 2 == 0 else -2.05
            spring_coords.append([x_val, y_val, 0.0])
        spring_pts = [[-2.6, -0.47, 0.0]] + spring_coords + [[-2.6, 0.87, 0.0]]
        m3_spring = VMobject(color=YELLOW, stroke_width=4.0).set_points_as_corners([np.array(p) for p in spring_pts])

        # Gland Follower / Top Bushing holding spring in place
        m3_gland_cap = Rectangle(width=1.65, height=0.50, color=COL_OK).set_fill("#0F766E", 1.0).move_to([-2.6, 1.15, 0.0])
        m3_cap_txt = Text("GLAND", font_size=10, color=WHITE).move_to(m3_gland_cap.get_center())

        lbl_spring = _h6_17_badge("Coil Spring (สปริงกด)", YELLOW).move_to([-2.6, 1.65, 0.0])

        m3_mech = VGroup(m3_house_l, m3_house_r, m3_cavity_bg, m3_packings, m3_plate, m3_spring, m3_gland_cap, m3_cap_txt, lbl_spring)

        # Right explanatory panel (x = 2.5)
        m3_card = RoundedRectangle(width=5.8, height=3.3, corner_radius=0.12, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([2.5, 0.05, 0.0])
        m3_head = _h6_17_badge("3. Spring Loaded (สปริงกดอัตโนมัติ)", COL_OK).move_to([2.5, 1.35, 0.0])
        m3_points = VGroup(
            Text("• มีสปริงขดดันอัดรักษาแรงกดบนหน้าสัมผัสอย่างต่อเนื่อง", font_size=11, color=WHITE),
            Text("• เมื่อ Packing ค่อยๆ สึกหรอ สปริงจะยืดตัวชดเชยให้เองทันที", font_size=11, color=WHITE),
            Text("• ข้อดีเด่น: ปรับแรงกดอัตโนมัติ (Self-Adjusting) ไม่ต้องคอยขัน", font_size=11, color=COL_OK),
            Text("• เหมาะสมที่สุด: จุดที่เข้าถึงยาก หรืองานเดินเครื่องต่อเนื่อง", font_size=11, color=COL_CURR),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([2.5, 0.05, 0.0])
        m3_panel = VGroup(m3_card, m3_head, m3_points)

        banner4 = _h6_17_banner(
            "3. Spring Loaded: สปริงดันแรงกดให้อัตโนมัติตลอดเวลา แม้ packing สึกไปก็ยังคงแรงกดได้เอง ไม่ต้องคอยขัน",
            COL_OK
        )

        self.play(FadeIn(m3_mech, shift=UP * 0.25), FadeIn(m3_panel), FadeIn(banner4), run_time=0.8)

        # Dynamic compression and release animation of spring!
        force_arrow = Arrow([-2.6, 0.35, 0], [-2.6, -0.45, 0], color=YELLOW, stroke_width=4.0, tip_length=0.14)
        lbl_force = Text("F_spring", font_size=11, color=YELLOW).next_to(force_arrow, LEFT, buff=0.10)
        f_grp = VGroup(force_arrow, lbl_force)

        self.play(
            m3_spring.animate.stretch(0.85, dim=1, about_point=[-2.6, 0.85, 0]),
            FadeIn(f_grp),
            run_time=1.0
        )
        self.play(
            m3_spring.animate.stretch(1.0 / 0.85, dim=1, about_point=[-2.6, 0.85, 0]),
            run_time=0.8
        )
        self.wait(3.0)  # Checkpoint 29.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 33.6–40.0: Single Packing Ring Dimensional Vocabulary
        # ======================================================================
        cap3 = _h6_17_caption_top("ศัพท์มิติของแหวน Packing แต่ละวง (Ring Dimension Vocabulary)")
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        # Single V-Packing Ring Cross-Section (Bottom of slide 20)
        ring_l = Polygon(
            [-3.65, 0.40, 0], [-3.10, -0.30, 0], [-2.55, 0.40, 0],
            [-2.80, 0.40, 0], [-3.10, 0.05, 0], [-3.40, 0.40, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 2.0)

        ring_r = Polygon(
            [2.55, 0.40, 0], [3.10, -0.30, 0], [3.65, 0.40, 0],
            [3.40, 0.40, 0], [3.10, 0.05, 0], [2.80, 0.40, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 2.0)

        ring_body_top = Line([-2.80, 0.40, 0], [2.80, 0.40, 0], color="#64748B", stroke_width=1.5)
        ring_body_bot = Line([-3.10, -0.30, 0], [3.10, -0.30, 0], color="#64748B", stroke_width=1.5)
        ring_graphic = VGroup(ring_l, ring_r, ring_body_top, ring_body_bot)

        # FIVE DIMENSION CALLOUTS (Slide 20 bottom: NO NUMBERS, ONLY LABELS!)
        # 1. Nominal I.D. (Inside Diameter between inner lips)
        dim_id = DoubleArrow([-2.55, 0.95, 0], [2.55, 0.95, 0], color=WHITE, stroke_width=2.5, tip_length=0.12)
        id_ext_l = DashedLine([-2.55, 0.45, 0], [-2.55, 1.15, 0], color=COL_GRAY, stroke_width=1.0)
        id_ext_r = DashedLine([2.55, 0.45, 0], [2.55, 1.15, 0], color=COL_GRAY, stroke_width=1.0)
        lbl_id = _h6_17_badge("NOMINAL I.D. (เส้นผ่านศูนย์กลางใน)", WHITE).move_to([0.0, 1.30, 0.0])
        grp_id = VGroup(dim_id, id_ext_l, id_ext_r, lbl_id)

        # 2. Nominal O.D. (Outside Diameter between outer lip tips)
        dim_od = DoubleArrow([-3.65, -0.85, 0], [3.65, -0.85, 0], color=WHITE, stroke_width=2.5, tip_length=0.12)
        od_ext_l = DashedLine([-3.65, -0.35, 0], [-3.65, -1.05, 0], color=COL_GRAY, stroke_width=1.0)
        od_ext_r = DashedLine([3.65, -0.35, 0], [3.65, -1.05, 0], color=COL_GRAY, stroke_width=1.0)
        lbl_od = _h6_17_badge("NOMINAL O.D. (เส้นผ่านศูนย์กลางนอก)", WHITE).move_to([0.0, -1.25, 0.0])
        grp_od = VGroup(dim_od, od_ext_l, od_ext_r, lbl_od)

        # 3. Stack Height (Vertical dimension on far left)
        dim_sh = DoubleArrow([-4.30, -0.30, 0], [-4.30, 0.40, 0], color=COL_OK, stroke_width=2.5, tip_length=0.10)
        sh_ext_top = DashedLine([-3.65, 0.40, 0], [-4.45, 0.40, 0], color=COL_GRAY, stroke_width=1.0)
        sh_ext_bot = DashedLine([-3.10, -0.30, 0], [-4.45, -0.30, 0], color=COL_GRAY, stroke_width=1.0)
        lbl_sh = _h6_17_badge("STACK HEIGHT\n(ความสูงซ้อน)", COL_OK).next_to(dim_sh, LEFT, buff=0.15)
        grp_sh = VGroup(dim_sh, sh_ext_top, sh_ext_bot, lbl_sh)

        # 4. Heel Clearance & 5. Interference on Right side matching slide 20
        ext_lip = DashedLine([3.65, 0.40, 0], [3.65, -0.65, 0], color=COL_GRAY, stroke_width=1.0)
        ext_heel = DashedLine([3.10, -0.30, 0], [3.10, -0.65, 0], color=COL_GRAY, stroke_width=1.0)
        ext_bore = DashedLine([4.15, 0.40, 0], [4.15, -0.65, 0], color=COL_GRAY, stroke_width=1.0)

        # Interference arrow & badge (flared lip interference fit)
        dim_inf = DoubleArrow([3.10, -0.45, 0], [3.65, -0.45, 0], color=COL_WARN, stroke_width=2.0, tip_length=0.08)
        lbl_inf = _h6_17_badge("INTERFERENCE\n(ระยะเบียดอัดแน่น)", COL_WARN).move_to([5.3, 0.60, 0.0])
        arr_inf = Arrow([3.95, 0.60, 0], [3.65, 0.42, 0], color=COL_WARN, stroke_width=1.8, tip_length=0.08)
        grp_inf = VGroup(ext_lip, ext_heel, dim_inf, lbl_inf, arr_inf)

        # Heel clearance arrow & badge (clearance gap to prevent binding)
        dim_hc = DoubleArrow([3.65, -0.55, 0], [4.15, -0.55, 0], color=YELLOW, stroke_width=2.0, tip_length=0.08)
        lbl_hc = _h6_17_badge("HEEL CLEARANCE\n(ระยะเผื่อสันส้น)", YELLOW).move_to([5.3, -0.55, 0.0])
        arr_hc = Arrow([3.95, -0.55, 0], [3.10, -0.32, 0], color=YELLOW, stroke_width=1.8, tip_length=0.08)
        grp_hc = VGroup(ext_bore, dim_hc, lbl_hc, arr_hc)

        banner5 = _h6_17_banner(
            "มิติสำคัญของแหวนแต่ละวง: เส้นผ่านศูนย์กลางใน-นอก, ความสูง, ระยะเผื่อขอบ, ระยะเบียด",
            COL_OK
        )

        dim_labels = [grp_id, grp_od, grp_sh, grp_hc, grp_inf]

        self.play(FadeIn(ring_graphic, shift=UP * 0.25), FadeIn(banner5), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=UP * 0.15) for lbl in dim_labels], lag_ratio=0.3),
            run_time=1.5
        )
        self.wait(3.5)  # Checkpoint 37.0s falls right here!

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 40.6–45.0: Summary Card
        # ======================================================================
        card_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: กลไกปรับความแน่นและศัพท์มิติ Compression Packing (hydraulic06 น.20)", font_size=13.5, color=COL_OK).move_to([0.0, 1.35, 0.0])
        rows = [
            "1. ส่วนประกอบ Gland: Male Supporting Ring, Packings (V-rings), Female Support Ring, Follower, และ Shim",
            "2. วิธีปรับ 1: Threaded Follower ขันเกลียวโดยตรง ตัวกะทัดรัด แต่ต้องอาศัยช่างคอยตรวจขันกวดเป็นระยะ",
            "3. วิธีปรับ 2: Flanged Follower ขันน็อตรอบหน้าแปลน กระจายแรงกดทั่วถึงและสม่ำเสมอกว่าแบบเกลียวเดี่ยว",
            "4. วิธีปรับ 3: Spring Loaded สปริงดันแรงกดชดเชยการสึกหรออัตโนมัติตลอดเวลา เหมาะกับจุดที่เข้าถึงยาก",
            "5. ศัพท์มิติแหวน: Nominal I.D. / Nominal O.D. / Stack Height / Heel Clearance / Interference"
        ]
        s_rows = VGroup(*[Text(r, font_size=11, color=WHITE) for r in rows]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([0.0, -0.18, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(3.6)  # Checkpoint 42.0s falls here

        # ======================================================================
        # BEAT 45.0–49.5: Review Question Card
        # ======================================================================
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "งานที่เข้าถึงยาก ไม่สะดวกส่งคนไปตรวจและขันปรับความแน่นบ่อยๆ\nควรเลือกใช้กลไกปรับ Gland Follower แบบใด?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: Spring Loaded Follower เพราะสปริงจะยุบตัวสะสมแรงและคอยดันชดเชยการสึกหรอ\nของ Packing ให้อัตโนมัติตลอดเวลา โดยไม่ต้องพึ่งพาคนคอยขันกวด)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.5)  # Checkpoint 47.0s falls here

        self.play(FadeOut(question_grp), run_time=0.5)
        self.wait(0.2)
        self.fade_out_all(run_time=0.6)
        self.wait(0.5)


# ==============================================================================
# Scene: H6_18_PistonCupPackings (คัพซีลลูกสูบ Piston Cup Packings)
# Lecture slides: hydraulic06.pdf page 21
# Pedagogical Objective:
# - Single-acting uses 1 cup facing pressure; Double-acting uses 2 cups back-to-back
# - Pressure-actuated sealing mechanism (Self-energizing outward flare against cylinder barrel wall)
# - Clamping assembly: Backing plate (supports base against pressure) + Retainer plate
# ==============================================================================

def _h6_18_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_18_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_18_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_18_badge(text, color):
    lbl = Text(text, font_size=11, color=color)
    bg = RoundedRectangle(
        width=lbl.width + 0.48, height=0.38, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_18_banner(text, color):
    bg = RoundedRectangle(
        width=11.8, height=0.52, corner_radius=0.1,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.90, 0.0])
    lbl = Text(text, font_size=12, color=color).move_to(bg.get_center())
    return VGroup(bg, lbl)


class H6_18_PistonCupPackings(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ======================================================================
        # BEAT 0.0–2.0: Title & Page Reference
        # ======================================================================
        self.title_m = _h6_18_title("Piston Cup Packing: คัพซีลลูกสูบ")
        self.ref_m = _h6_18_page_ref("hydraulic06 น.21")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)

        # ======================================================================
        # BEAT 2.0–5.5: Hook Question
        # ======================================================================
        hook_q = _h6_18_caption_top("คัพซีลลูกสูบใช้แบบเดียวกันหมด ไม่ว่ากระบอกสูบจะดันทิศเดียวหรือสองทิศจริงไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.5)

        # ======================================================================
        # BEAT 5.5–16.0: Single-Acting (1 Cup) vs Double-Acting (2 Cups Back-to-Back)
        # ======================================================================
        cap1 = _h6_18_caption_top("1. เลือกจำนวนคัพตามทิศทางแรงดัน (Single vs Double Acting)")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # ----------------- LEFT: SINGLE-ACTING (x_center = -3.3) -----------------
        xs = -3.3
        # Cylinder barrel: top and bottom walls
        s_cyl_t = Rectangle(width=4.8, height=0.25, color=COL_METAL).set_fill("#334155", 0.95).move_to([xs, 1.25, 0.0])
        s_cyl_b = Rectangle(width=4.8, height=0.25, color=COL_METAL).set_fill("#334155", 0.95).move_to([xs, -1.25, 0.0])
        s_bore_bg = Rectangle(width=4.8, height=2.25, color=BLACK).set_fill("#0F172A", 1.0).move_to([xs, 0.0, 0.0])

        # Piston rod (entering from right, ending at nut on left)
        s_rod = Rectangle(width=2.5, height=0.55, color=COL_METAL).set_fill("#475569", 0.95).move_to([xs + 1.25, 0.0, 0.0])
        s_stud = Rectangle(width=0.7, height=0.32, color=WHITE).set_fill("#94A3B8", 1.0).move_to([xs - 0.35, 0.0, 0.0])
        s_nut = Rectangle(width=0.35, height=0.65, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([xs - 0.55, 0.0, 0.0])

        # Backing plate (behind the cup on right, supporting it)
        s_backing = Rectangle(width=0.45, height=2.0, color=COL_METAL).set_fill("#475569", 0.95).move_to([xs + 0.25, 0.0, 0.0])

        # SINGLE CUP (Elastomer, lips pointing LEFT <)
        # Upper half of cup: base at x=0.0 to 0.02, lip extends left to x=-0.50
        s_cup_t = Polygon(
            [xs + 0.02, 0.27, 0], [xs + 0.02, 0.95, 0], [xs - 0.50, 1.10, 0],
            [xs - 0.50, 0.92, 0], [xs - 0.16, 0.80, 0], [xs - 0.16, 0.27, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 1.8)
        # Lower half of cup:
        s_cup_b = Polygon(
            [xs + 0.02, -0.27, 0], [xs + 0.02, -0.95, 0], [xs - 0.50, -1.10, 0],
            [xs - 0.50, -0.92, 0], [xs - 0.16, -0.80, 0], [xs - 0.16, -0.27, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 1.8)
        s_cup = VGroup(s_cup_t, s_cup_b)

        # Retainer plate (clamps cup base against backing plate)
        s_retainer = Rectangle(width=0.20, height=1.55, color="#E2E8F0").set_fill("#94A3B8", 1.0).move_to([xs - 0.26, 0.0, 0.0])

        # Pressure arrow coming from left only
        s_p_arr = Arrow([xs - 2.1, 0.0, 0], [xs - 1.1, 0.0, 0], color=RED, stroke_width=4.5, tip_length=0.18)
        s_p_lbl = Text("PRESSURE", font_size=9, color=RED).next_to(s_p_arr, UP, buff=0.08)
        s_press_grp = VGroup(s_p_arr, s_p_lbl)

        s_badge = _h6_18_badge("Single-Acting (1 คัพ)", COL_OK).move_to([xs, 1.65, 0.0])
        s_sub = Text("แรงดันมาทิศเดียว — ใช้คัพเดียว ปากหันสู้แรงดัน", font_size=9.5, color=WHITE).move_to([xs, -1.55, 0.0])

        single_grp = VGroup(
            s_bore_bg, s_cyl_t, s_cyl_b, s_rod, s_backing,
            s_cup, s_retainer, s_stud, s_nut, s_press_grp, s_badge, s_sub
        )

        # ----------------- RIGHT: DOUBLE-ACTING (x_center = +3.3) -----------------
        xd = 3.3
        # Cylinder barrel
        d_cyl_t = Rectangle(width=4.8, height=0.25, color=COL_METAL).set_fill("#334155", 0.95).move_to([xd, 1.25, 0.0])
        d_cyl_b = Rectangle(width=4.8, height=0.25, color=COL_METAL).set_fill("#334155", 0.95).move_to([xd, -1.25, 0.0])
        d_bore_bg = Rectangle(width=4.8, height=2.25, color=BLACK).set_fill("#0F172A", 1.0).move_to([xd, 0.0, 0.0])

        # Piston rod through center
        d_rod = Rectangle(width=2.2, height=0.55, color=COL_METAL).set_fill("#475569", 0.95).move_to([xd + 1.40, 0.0, 0.0])
        d_stud = Rectangle(width=0.7, height=0.32, color=WHITE).set_fill("#94A3B8", 1.0).move_to([xd - 0.75, 0.0, 0.0])
        d_nut = Rectangle(width=0.35, height=0.65, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([xd - 0.95, 0.0, 0.0])

        # Central Backing Plate (Spacer between the 2 cups)
        d_center_plate = Rectangle(width=0.45, height=2.0, color=COL_METAL).set_fill("#475569", 0.95).move_to([xd, 0.0, 0.0])

        # CUP 1 (Left Cup): Lips pointing LEFT <
        d_cup1_t = Polygon(
            [xd - 0.23, 0.27, 0], [xd - 0.23, 0.95, 0], [xd - 0.70, 1.10, 0],
            [xd - 0.70, 0.92, 0], [xd - 0.40, 0.80, 0], [xd - 0.40, 0.27, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 1.8)
        d_cup1_b = Polygon(
            [xd - 0.23, -0.27, 0], [xd - 0.23, -0.95, 0], [xd - 0.70, -1.10, 0],
            [xd - 0.70, -0.92, 0], [xd - 0.40, -0.80, 0], [xd - 0.40, -0.27, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 1.8)
        d_cup1 = VGroup(d_cup1_t, d_cup1_b)

        # CUP 2 (Right Cup): Lips pointing RIGHT > (Back-to-Back with Cup 1!)
        d_cup2_t = Polygon(
            [xd + 0.23, 0.27, 0], [xd + 0.23, 0.95, 0], [xd + 0.70, 1.10, 0],
            [xd + 0.70, 0.92, 0], [xd + 0.40, 0.80, 0], [xd + 0.40, 0.27, 0],
            color=COL_WARN, fill_color="#EA580C", fill_opacity=0.95
        ).set_stroke(COL_WARN, 1.8)
        d_cup2_b = Polygon(
            [xd + 0.23, -0.27, 0], [xd + 0.23, -0.95, 0], [xd + 0.70, -1.10, 0],
            [xd + 0.70, -0.92, 0], [xd + 0.40, -0.80, 0], [xd + 0.40, -0.27, 0],
            color=COL_WARN, fill_color="#EA580C", fill_opacity=0.95
        ).set_stroke(COL_WARN, 1.8)
        d_cup2 = VGroup(d_cup2_t, d_cup2_b)

        # Retainers on both sides
        d_ret_l = Rectangle(width=0.18, height=1.55, color="#E2E8F0").set_fill("#94A3B8", 1.0).move_to([xd - 0.49, 0.0, 0.0])
        d_ret_r = Rectangle(width=0.18, height=1.55, color="#E2E8F0").set_fill("#94A3B8", 1.0).move_to([xd + 0.49, 0.0, 0.0])

        # Dual pressure arrows (from both sides)
        d_p_arr_l = Arrow([xd - 2.1, 0.0, 0], [xd - 1.2, 0.0, 0], color=RED, stroke_width=3.5, tip_length=0.14)
        d_p_lbl_l = Text("PRESSURE", font_size=8.5, color=RED).next_to(d_p_arr_l, UP, buff=0.06)
        d_p_arr_r = Arrow([xd + 2.1, 0.0, 0], [xd + 1.2, 0.0, 0], color=RED, stroke_width=3.5, tip_length=0.14)
        d_p_lbl_r = Text("PRESSURE", font_size=8.5, color=RED).next_to(d_p_arr_r, UP, buff=0.06)
        d_press_grp = VGroup(d_p_arr_l, d_p_lbl_l, d_p_arr_r, d_p_lbl_r)

        d_badge = _h6_18_badge("Double-Acting (2 คัพหันหลังชนกัน)", COL_WARN).move_to([xd, 1.65, 0.0])
        d_sub = Text("แรงดันสลับ 2 ทิศ — 2 คัพหันหลังชนกัน (Back-to-Back)", font_size=9.5, color=WHITE).move_to([xd, -1.55, 0.0])

        double_grp = VGroup(
            d_bore_bg, d_cyl_t, d_cyl_b, d_rod, d_center_plate,
            d_cup1, d_cup2, d_ret_l, d_ret_r, d_stud, d_nut, d_press_grp, d_badge, d_sub
        )

        banner1 = _h6_18_banner(
            "Single-Acting: แรงดันมาทิศเดียว ใช้คัพเดียว — Double-Acting: แรงดันสลับ 2 ทิศ ต้องใช้ 2 คัพหันหลังชนกัน",
            COL_OK
        )

        self.play(FadeIn(VGroup(single_grp, double_grp), shift=UP * 0.25), FadeIn(banner1), run_time=1.2)
        # Lesson 5: Sequence Indicate after FadeIn
        self.play(
            Indicate(s_badge, color=COL_OK, scale_factor=1.08),
            Indicate(s_cup, color=WHITE, scale_factor=1.05),
            run_time=0.9
        )
        self.play(
            Indicate(d_badge, color=COL_WARN, scale_factor=1.08),
            Indicate(d_cup1, color=WHITE, scale_factor=1.05),
            Indicate(d_cup2, color=WHITE, scale_factor=1.05),
            run_time=0.9
        )
        self.wait(5.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 16.6–27.0: Pressure-Actuated (Self-Energizing) Lip Flare
        # ======================================================================
        cap2 = _h6_18_caption_top("2. คัพซีลทำงานแบบ Pressure-Actuated (เชื่อม O-ring H6_15 + V-packing H6_16/17)")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Large detailed cross section of cylinder bore (focusing on single cup sealing against wall)
        cyl_wall_top = Rectangle(width=8.6, height=0.40, color=COL_METAL).set_fill("#334155", 0.95).move_to([-0.2, 1.45, 0.0])
        cyl_wall_bot = Rectangle(width=8.6, height=0.40, color=COL_METAL).set_fill("#334155", 0.95).move_to([-0.2, -1.45, 0.0])
        cyl_bore_bg  = Rectangle(width=8.6, height=2.50, color=BLACK).set_fill("#0F172A", 1.0).move_to([-0.2, 0.0, 0.0])
        lbl_barrel   = Text("CYLINDER BARREL (ผนังกระบอกสูบ)", font_size=10, color=COL_METAL).move_to([1.8, 1.80, 0.0])

        # Piston rod & backing plate on right side
        p_rod = Rectangle(width=4.0, height=0.65, color=COL_METAL).set_fill("#475569", 0.95).move_to([2.1, 0.0, 0.0])
        lbl_rod = Text("PISTON ROD", font_size=10, color=WHITE).move_to([2.1, 0.0, 0.0])
        p_backing = Rectangle(width=0.60, height=2.20, color=COL_METAL).set_fill("#64748B", 0.95).move_to([0.40, 0.0, 0.0])
        p_retainer = Rectangle(width=0.30, height=1.70, color="#CBD5E1").set_fill("#94A3B8", 1.0).move_to([-0.35, 0.0, 0.0])
        p_nut = Rectangle(width=0.40, height=0.80, color=WHITE).set_fill("#E2E8F0", 1.0).move_to([-0.70, 0.0, 0.0])

        # ----------------- NEUTRAL CUP (Relaxed Lip Angle, Small Clearance) -----------------
        # Upper lip: relaxes down to y = 1.15 (gap of 0.10 from barrel wall at 1.25)
        neutral_cup_t = Polygon(
            [0.10, 0.32, 0], [0.10, 1.05, 0], [-1.05, 1.15, 0],
            [-1.05, 0.98, 0], [-0.20, 0.88, 0], [-0.20, 0.32, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 2.0)
        # Lower lip: relaxes up to y = -1.15 (gap of 0.10 from barrel wall at -1.25)
        neutral_cup_b = Polygon(
            [0.10, -0.32, 0], [0.10, -1.05, 0], [-1.05, -1.15, 0],
            [-1.05, -0.98, 0], [-0.20, -0.88, 0], [-0.20, -0.32, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 2.0)
        cup_neutral = VGroup(neutral_cup_t, neutral_cup_b)

        # ----------------- ENERGIZED CUP (Lip Flares OUTWARD and Seals Hard Against Wall) -----------------
        # Upper lip: FLARED OUT to y = 1.25 (flush against wall, wider contact line)
        energized_cup_t = Polygon(
            [0.10, 0.32, 0], [0.10, 1.05, 0], [-1.15, 1.25, 0],
            [-1.15, 1.08, 0], [-0.20, 0.90, 0], [-0.20, 0.32, 0],
            color=COL_WARN, fill_color="#EA580C", fill_opacity=0.95
        ).set_stroke(COL_WARN, 2.5)
        # Lower lip: FLARED OUT to y = -1.25 (flush against wall)
        energized_cup_b = Polygon(
            [0.10, -0.32, 0], [0.10, -1.05, 0], [-1.15, -1.25, 0],
            [-1.15, -1.08, 0], [-0.20, -0.90, 0], [-0.20, -0.32, 0],
            color=COL_WARN, fill_color="#EA580C", fill_opacity=0.95
        ).set_stroke(COL_WARN, 2.5)
        cup_energized = VGroup(energized_cup_t, energized_cup_b)

        # Status badge for neutral state
        badge_state_n = _h6_18_badge("สภาวะปกติ (ยังไม่มีแรงดัน) — ปากคัพแนบหลวมๆ", COL_GRAY).move_to([-2.4, 1.80, 0.0])

        cylinder_assembly = VGroup(
            cyl_bore_bg, cyl_wall_top, cyl_wall_bot, lbl_barrel,
            p_rod, lbl_rod, p_backing, p_retainer, p_nut, cup_neutral, badge_state_n
        )

        banner2 = _h6_18_banner(
            "แรงดันดันปากคัพให้บานออกกดผนังกระบอกสูบ ยิ่งแรงดันสูงยิ่งซีลแน่น — self-energizing แบบเดียวกับ O-ring และ V-packing",
            COL_OK
        )

        self.play(FadeIn(cylinder_assembly, shift=UP * 0.25), FadeIn(banner2), run_time=0.8)
        self.wait(1.0)

        # Fluid Pressure injection from left (RED chamber)
        press_fluid_t = Rectangle(width=3.2, height=1.0, color=RED).set_fill(RED, 0.55).move_to([-2.7, 0.72, 0.0])
        press_fluid_b = Rectangle(width=3.2, height=1.0, color=RED).set_fill(RED, 0.55).move_to([-2.7, -0.72, 0.0])
        lbl_p_fluid = Text("PRESSURE (น้ำมันแรงดันสูง)", font_size=11, color=YELLOW).move_to([-2.7, 0.72, 0.0])
        press_zone = VGroup(press_fluid_t, press_fluid_b, lbl_p_fluid)

        # Pressure arrows driving INTO the cup pockets and pushing outward!
        arr_push_t = Arrow([-0.65, 0.65, 0], [-0.75, 1.20, 0], color=YELLOW, stroke_width=4.0, tip_length=0.14)
        arr_push_b = Arrow([-0.65, -0.65, 0], [-0.75, -1.20, 0], color=YELLOW, stroke_width=4.0, tip_length=0.14)
        press_arrows = VGroup(arr_push_t, arr_push_b)

        # Status badge for energized state
        badge_state_e = _h6_18_badge("แรงดันดันปากบานออก (Self-Energizing) แนบผนังแน่นสนิท!", COL_WARN).move_to([-2.4, 1.80, 0.0])

        # Sealing contact highlight lines along barrel
        seal_line_t = Line([-1.20, 1.25, 0], [-0.60, 1.25, 0], color=COL_OK, stroke_width=5.0)
        seal_line_b = Line([-1.20, -1.25, 0], [-0.60, -1.25, 0], color=COL_OK, stroke_width=5.0)
        seal_highlights = VGroup(seal_line_t, seal_line_b)

        # Real transform: Lip angle genuinely expands and presses wall!
        self.play(
            FadeIn(press_zone, shift=RIGHT * 0.3),
            FadeIn(press_arrows),
            Transform(badge_state_n, badge_state_e),
            Transform(cup_neutral, cup_energized),
            run_time=1.2
        )
        self.play(FadeIn(seal_highlights), run_time=0.4)
        self.wait(5.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 27.6–36.0: Backing Plate + Retainer Clamping Mechanism
        # ======================================================================
        cap3 = _h6_18_caption_top("3. Backing Plate + Retainer หนีบยึดคัพให้อยู่กับที่ (Clamping Assembly)")
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        # Assembly showcase on left side (x = -2.6)
        # 1. Piston Rod
        a_rod = Rectangle(width=3.5, height=0.60, color=COL_METAL).set_fill("#475569", 0.95).move_to([-0.7, 0.0, 0.0])
        a_rod_axis = DashedLine([-4.6, 0.0, 0.0], [1.1, 0.0, 0.0], color="#94A3B8", stroke_width=1.5, dash_length=0.15)

        # 2. Backing Plate (Distinct thick steel plate behind cup on right, x = -1.8)
        # Sits against rod shoulder, supports flat base of cup
        a_backing = Rectangle(width=0.50, height=2.6, color=COL_METAL).set_fill("#475569", 0.95).set_stroke(COL_METAL, 2.5).move_to([-1.8, 0.0, 0.0])

        # 3. Cup Seal (Elastomer, base at x = -2.2, lips facing left to x = -3.2)
        a_cup_t = Polygon(
            [-2.05, 0.30, 0], [-2.05, 1.20, 0], [-3.15, 1.30, 0],
            [-3.15, 1.10, 0], [-2.35, 0.95, 0], [-2.35, 0.30, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 2.2)
        a_cup_b = Polygon(
            [-2.05, -0.30, 0], [-2.05, -1.20, 0], [-3.15, -1.30, 0],
            [-3.15, -1.10, 0], [-2.35, -0.95, 0], [-2.35, -0.30, 0],
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.95
        ).set_stroke(COL_OK, 2.2)
        a_cup = VGroup(a_cup_t, a_cup_b)

        # 4. Retainer Plate (Fits inside cup cavity, clamps cup base, x = -2.5)
        a_retainer = Rectangle(width=0.30, height=1.9, color=YELLOW).set_fill("#CA8A04", 0.95).set_stroke(YELLOW, 2.2).move_to([-2.5, 0.0, 0.0])

        # 5. Threaded Stud and Clamp Nut on end of rod
        a_stud = Rectangle(width=0.9, height=0.36, color=WHITE).set_fill("#94A3B8", 1.0).move_to([-3.10, 0.0, 0.0])
        a_nut = Rectangle(width=0.45, height=0.85, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([-3.40, 0.0, 0.0])

        # Clamping pinch arrows: Retainer pushes right -> | <- Backing plate pushes left
        arr_clamp_r = Arrow([-2.9, 0.65, 0], [-2.55, 0.65, 0], color=YELLOW, stroke_width=3.5, tip_length=0.12)
        arr_clamp_l = Arrow([-1.4, 0.65, 0], [-1.75, 0.65, 0], color=COL_METAL, stroke_width=3.5, tip_length=0.12)
        clamp_arrows = VGroup(arr_clamp_r, arr_clamp_l)

        # Callout Badges
        lbl_c_cup = _h6_18_badge("Piston Cup Seal (คัพซีล)", COL_OK).move_to([-2.6, 1.85, 0.0])
        arr_c_cup = Arrow([-2.6, 1.68, 0], [-2.6, 1.32, 0], color=COL_OK, stroke_width=2.0, tip_length=0.10)
        call_cup = VGroup(lbl_c_cup, arr_c_cup)

        lbl_c_back = _h6_18_badge("Backing Plate (แผ่นรองหลัง)", COL_METAL).move_to([-0.2, 1.85, 0.0])
        arr_c_back = Arrow([-0.6, 1.68, 0], [-1.75, 1.32, 0], color=COL_METAL, stroke_width=2.0, tip_length=0.10)
        call_back = VGroup(lbl_c_back, arr_c_back)

        lbl_c_ret = _h6_18_badge("Retainer (ตัวล็อกหนีบ)", YELLOW).move_to([-2.6, -1.85, 0.0])
        arr_c_ret = Arrow([-2.6, -1.68, 0], [-2.5, -1.05, 0], color=YELLOW, stroke_width=2.0, tip_length=0.10)
        call_ret = VGroup(lbl_c_ret, arr_c_ret)

        a_assembly = VGroup(
            a_rod, a_rod_axis, a_backing, a_cup, a_retainer, a_stud, a_nut,
            clamp_arrows, call_cup, call_back, call_ret
        )

        # Right explanatory panel (x = 2.5)
        a_card = RoundedRectangle(width=5.8, height=3.3, corner_radius=0.12, color=COL_OK, fill_color=COL_BG_BOX).set_fill(COL_BG_BOX, 0.95).move_to([2.5, 0.05, 0.0])
        a_head = _h6_18_badge("หน้าที่ของชุดยึดคัพลูกสูบ", COL_OK).move_to([2.5, 1.35, 0.0])
        a_points = VGroup(
            Text("• Backing Plate: แผ่นเหล็กรองหลัง รับแรงดันมหาศาล", font_size=11, color=WHITE),
            Text("  ป้องกันฐานคัพยางโก่งงอหรือปลิ้นออกทางช่องว่าง", font_size=10.5, color=COL_GRAY),
            Text("• Retainer: แผ่นกดหนีบฐานคัพเข้ากับ Backing Plate", font_size=11, color=WHITE),
            Text("  ล็อกตำแหน่งให้แน่นสนิท ไม่ให้คัพหลุดเลื่อนตอนก้านสูบถอย", font_size=10.5, color=COL_OK),
            Text("• ควบคุมแรงบีบพอดี ป้องกันขอบคัพฉีกขาดจากแรงกดเกิน", font_size=11, color=COL_WARN),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([2.5, 0.0, 0.0])
        a_panel = VGroup(a_card, a_head, a_points)

        banner3 = _h6_18_banner(
            "แผ่นรองหลัง (Backing Plate) และตัวล็อก (Retainer) หนีบขอบคัพให้แน่น ป้องกันคัพเคลื่อน/บิดตอนใช้งาน",
            COL_OK
        )

        self.play(FadeIn(a_assembly, shift=UP * 0.25), FadeIn(a_panel), FadeIn(banner3), run_time=0.8)
        # Sequentially indicate backing plate and retainer (Lesson 5: after FadeIn)
        self.play(
            Indicate(call_back, color=COL_METAL, scale_factor=1.08),
            Indicate(call_ret, color=YELLOW, scale_factor=1.08),
            run_time=1.2
        )
        self.wait(4.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 36.6–41.0: Summary Card
        # ======================================================================
        card_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: คัพซีลลูกสูบ (Piston Cup Packings - hydraulic06 น.21)", font_size=13.5, color=COL_OK).move_to([0.0, 1.35, 0.0])
        rows = [
            "1. ทิศทางการทำงาน: Single-acting ใช้ 1 คัพ (หันปากสู้แรงดัน) / Double-acting ใช้ 2 คัพหันหลังชนกัน (Back-to-Back)",
            "2. กลไก Pressure-Actuated: แรงดันของไหลช่วยดันถ่างปากคัพให้แนบแน่นกับกระบอกสูบ (Self-Energizing)",
            "3. ความเชื่อมโยงของซีล: เป็นหลักการเดียวกับ O-ring (H6_15) และ V-packing (H6_16/17) ยิ่งแรงดันสูง ยิ่งซีลแน่น",
            "4. ชุดประกบยึดแน่น: Backing Plate + Retainer หนีบฐานคัพไว้แน่น ป้องกันการบิดเลื่อนและป้องกันการปลิ้นเสียหาย"
        ]
        s_rows = VGroup(*[Text(r, font_size=11, color=WHITE) for r in rows]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0.0, -0.15, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.8)
        self.wait(3.6)

        # ======================================================================
        # BEAT 41.0–45.5: Review Question Card
        # ======================================================================
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "กระบอกสูบที่ต้องรับแรงดันสลับทิศทั้งขาเข้าและขาออก (Double-Acting)\nควรติดตั้งคัพซีลกี่ตัว และจัดวางในลักษณะใด?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: ต้องใช้ 2 คัพ วางหันหลังชนกัน (Back-to-Back) โดยให้ปากคัพแต่ละตัวหันออกคนละทิศ\nเพื่อรับแรงดันของไหลที่สลับเข้ามาจากแต่ละฝั่งได้อย่างสมบูรณ์)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(3.5)

        self.play(FadeOut(question_grp), run_time=0.5)
        self.wait(0.2)
        self.fade_out_all(run_time=0.6)
        self.wait(0.5)


# ==============================================================================
# Scene: H6_19_PistonRings (แหวนลูกสูบ Piston Rings)
# Lecture slides: hydraulic06.pdf page 22
# Pedagogical Objective:
# - Piston Ring is a metallic ring with a visible end gap, not an elastomer O-ring
# - End gap enables installation into piston grooves and intentionally allows slight leakage
# - Cross-section comparison: Piston ring at OD (pressure side) vs O-ring at rod shoulder
# - Metallic rings withstand extreme temperatures far better than rubber/elastomers
# ==============================================================================

def _h6_19_title(text):
    return Text(text, font_size=20, color=WHITE).to_edge(UP, buff=0.35)


def _h6_19_page_ref(text):
    return Text(text, font_size=12, color=COL_GRAY).to_corner(UR, buff=0.35)


def _h6_19_caption_top(text, color=WHITE):
    return Text(text, font_size=14, color=color).move_to([0.0, 2.45, 0.0])


def _h6_19_badge(text, color):
    lbl = Text(text, font_size=11, color=color)
    bg = RoundedRectangle(
        width=lbl.width + 0.48, height=0.38, corner_radius=0.08,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95)
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_19_banner(text, color):
    bg = RoundedRectangle(
        width=11.8, height=0.52, corner_radius=0.1,
        color=color, fill_color=COL_BG_BOX
    ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -2.90, 0.0])
    lbl = Text(text, font_size=12, color=color).move_to(bg.get_center())
    return VGroup(bg, lbl)


def _h6_19_flame_icon(color=WARN, scale=0.25):
    pts_outer = [
        [0.0, 0.9, 0], [0.25, 0.35, 0], [0.45, 0.45, 0], [0.5, 0.0, 0],
        [0.4, -0.5, 0], [0.0, -0.7, 0], [-0.4, -0.5, 0], [-0.5, 0.0, 0],
        [-0.45, 0.45, 0], [-0.25, 0.35, 0]
    ]
    f_out = Polygon(*pts_outer, color=color, fill_color=color, fill_opacity=0.9).scale(scale)
    f_in = Polygon(*pts_outer, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95).scale(scale * 0.5).shift(DOWN * 0.05 * scale)
    return VGroup(f_out, f_in)


class H6_19_PistonRings(SafeScene):
    def clear_stage(self, run_time=0.5):
        mobs = [
            m for m in self.mobjects
            if m not in (getattr(self, "title_m", None), getattr(self, "ref_m", None))
        ]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def fade_out_all(self, run_time=0.5):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        # ======================================================================
        # BEAT 0.0–2.0: Title & Page Reference
        # ======================================================================
        self.title_m = _h6_19_title("Piston Rings: แหวนลูกสูบ")
        self.ref_m = _h6_19_page_ref("hydraulic06 น.22")
        self.play(FadeIn(self.title_m, shift=UP * 0.4), FadeIn(self.ref_m), run_time=1.2)
        self.wait(0.5)

        # ======================================================================
        # BEAT 2.0–5.5: Hook Question
        # ======================================================================
        hook_q = _h6_19_caption_top("ซีลในกระบอกสูบต้องเป็นยางเสมอ และห้ามรั่วซึมเลยจริงไหม?", color=COL_WARN)
        self.play(FadeIn(hook_q, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(hook_q), run_time=0.4)
        self.wait(0.5)

        # ======================================================================
        # BEAT 5.5–15.0: Closed Ring (O-ring) vs Split Ring (Piston Ring)
        # ======================================================================
        cap1 = _h6_19_caption_top("1. Piston Ring คือแหวนโลหะที่มีรอยผ่า ไม่ใช่ยางแบบ O-ring")
        self.play(FadeIn(cap1, shift=UP * 0.35), run_time=0.5)

        # Left Ring: Closed Ring (O-ring elastomer style) at x = -3.2
        xl = -3.2
        closed_ring = Annulus(
            inner_radius=1.00, outer_radius=1.38,
            color=COL_BAD, fill_color="#DC2626", fill_opacity=0.35,
            stroke_width=2.8, stroke_color=COL_BAD
        ).move_to([xl, -0.05, 0.0])
        closed_badge = _h6_19_badge("วงปิดสนิท (แบบ O-ring)", COL_BAD).move_to([xl, 1.85, 0.0])
        closed_sub = Text("เนื้อยางต่อเนื่อง ไม่มีรอยผ่า ซีลสนิท 100%", font_size=10, color=WHITE).move_to([xl, -1.85, 0.0])
        closed_grp = VGroup(closed_ring, closed_badge, closed_sub)

        # Right Ring: Split Ring (Piston Ring with visible end gap) at x = +3.2
        xr = 3.2
        # Visible gap at top (30° opening centered at 90°)
        split_ring = AnnularSector(
            inner_radius=1.00, outer_radius=1.38,
            start_angle=105 * DEGREES, angle=330 * DEGREES,
            color=COL_METAL, fill_color="#475569", fill_opacity=0.55,
            stroke_width=2.8, stroke_color=COL_METAL
        ).move_to([xr, -0.05, 0.0])

        # Gap Callout Arrow pointing directly into the opening
        gap_arr = Arrow([xr, 1.62, 0.0], [xr, 1.18, 0.0], color=COL_OK, stroke_width=3.0, tip_length=0.14)
        gap_lbl = _h6_19_badge("รอยผ่า (End Gap) ถ่างสวมเข้าร่องได้", COL_OK).move_to([xr, 1.85, 0.0])
        gap_callout = VGroup(gap_arr, gap_lbl)

        split_sub = Text("แหวนโลหะมีรอยผ่า ยอมให้รั่วซึมเล็กน้อยได้โดยตั้งใจ", font_size=10, color=WHITE).move_to([xr, -1.85, 0.0])
        split_grp = VGroup(split_ring, split_sub)

        banner1 = _h6_19_banner(
            "วงปิดสนิทแบบ O-ring vs แหวนโลหะที่มีรอยผ่า — รอยผ่านี้เองที่ทำให้สวมเข้าร่องลูกสูบได้",
            COL_OK
        )

        self.play(
            FadeIn(closed_grp, shift=UP * 0.25),
            FadeIn(split_grp, shift=UP * 0.25),
            FadeIn(banner1),
            run_time=1.0
        )
        # Lesson 5: Sequence Indicate after FadeIn
        self.play(Indicate(split_ring, color=COL_OK, scale_factor=1.08), run_time=0.8)
        self.play(FadeIn(gap_callout, shift=DOWN * 0.15), run_time=0.6)
        self.wait(5.0)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 15.6–26.0: Cross-Section: Piston Ring vs O-ring (hydraulic06 p.22)
        # ======================================================================
        cap2 = _h6_19_caption_top("2. ภาพเดียวกัน คนละตำแหน่ง คนละหน้าที่: Piston Ring vs O-ring")
        self.play(FadeIn(cap2, shift=UP * 0.35), run_time=0.5)

        # Full cross-section matching slide 22 (scaled vertically to prevent collision)
        # Cylinder barrel: top and bottom walls
        cyl_t = Rectangle(width=9.2, height=0.28, color=COL_METAL).set_fill("#334155", 0.95).move_to([0.0, 1.25, 0.0])
        cyl_b = Rectangle(width=9.2, height=0.28, color=COL_METAL).set_fill("#334155", 0.95).move_to([0.0, -1.25, 0.0])
        cyl_bg = Rectangle(width=9.2, height=2.22, color=BLACK).set_fill("#0F172A", 1.0).move_to([0.0, 0.0, 0.0])
        lbl_barrel = Text("CYLINDER BARREL (ผนังกระบอกสูบ)", font_size=9.0, color=COL_METAL).move_to([-2.6, 1.52, 0.0])

        # Red High-Pressure Chamber on RIGHT side of piston (x = 0.9 to 4.6)
        press_chamber = Rectangle(width=3.7, height=2.22, color=RED).set_fill(RED, 0.65).move_to([2.75, 0.0, 0.0])
        lbl_pressure = Text("PRESSURE\n(ห้องน้ำมันแรงดันสูง)", font_size=10.5, color=YELLOW).move_to([2.75, 0.0, 0.0])
        chamber_grp = VGroup(press_chamber, lbl_pressure)

        # Piston Rod: entering from left to piston step
        rod_main = Rectangle(width=3.2, height=0.65, color=COL_METAL).set_fill("#475569", 0.95).move_to([-3.0, 0.0, 0.0])
        rod_neck = Rectangle(width=1.7, height=0.42, color=WHITE).set_fill("#94A3B8", 1.0).move_to([-0.55, 0.0, 0.0])
        rod_nut = Rectangle(width=0.40, height=0.55, color=WHITE).set_fill("#CBD5E1", 1.0).move_to([0.50, 0.0, 0.0])
        rod_grp = VGroup(rod_main, rod_neck, rod_nut)

        # Piston Body: mounted around rod neck from x = -1.4 to 0.9
        piston_t = Rectangle(width=2.3, height=0.82, color=COL_METAL).set_fill("#64748B", 0.95).move_to([-0.25, 0.70, 0.0])
        piston_b = Rectangle(width=2.3, height=0.82, color=COL_METAL).set_fill("#64748B", 0.95).move_to([-0.25, -0.70, 0.0])
        lbl_piston = Text("PISTON (ลูกสูบ)", font_size=9.5, color=WHITE).move_to([-0.35, 0.68, 0.0])

        # 4 Ring Grooves on top OD and bottom OD (groove width = 0.16, depth = 0.16)
        grooves = []
        for gx in [-0.55, -0.30, -0.05, 0.20]:
            grooves.append(Rectangle(width=0.15, height=0.16, color=BLACK).set_fill("#0F172A", 1.0).move_to([gx, 1.03, 0.0]))
            grooves.append(Rectangle(width=0.15, height=0.16, color=BLACK).set_fill("#0F172A", 1.0).move_to([gx, -1.03, 0.0]))
        grooves_grp = VGroup(*grooves)

        # 1. PISTON RING MOB (OD corner, rightmost groove x = 0.20, facing pressure side)
        pr_block_t = Rectangle(width=0.15, height=0.16, color=COL_OK).set_fill(COL_OK, 1.0).move_to([0.20, 1.03, 0.0])
        pr_block_b = Rectangle(width=0.15, height=0.16, color=COL_OK).set_fill(COL_OK, 1.0).move_to([0.20, -1.03, 0.0])
        # §34 Geometry icon: distinct split ring with visible end gap
        pr_icon_ring = AnnularSector(
            inner_radius=0.18, outer_radius=0.28,
            start_angle=60 * DEGREES, angle=320 * DEGREES,
            color=COL_OK, fill_color="#0284C7", fill_opacity=0.9,
            stroke_width=1.8, stroke_color=COL_OK
        ).move_to([0.05, 1.78, 0.0])
        pr_badge = _h6_19_badge("PISTON RING: มีรอยผ่า (ฝั่งแรงดัน)", COL_OK).next_to(pr_icon_ring, RIGHT, buff=0.3)
        pr_arrow = Arrow([0.45, 1.62, 0.0], [0.22, 1.15, 0.0], color=COL_OK, stroke_width=2.2, tip_length=0.11)
        piston_ring_mob = VGroup(pr_block_t, pr_block_b, pr_icon_ring, pr_badge, pr_arrow)

        # 2. O-RING MOB (Inside piston-to-rod shoulder, left side at x = -1.25)
        or_dot_t = Circle(radius=0.09, color=COL_BAD, fill_color="#DC2626", fill_opacity=1.0).move_to([-1.25, 0.28, 0.0])
        or_dot_b = Circle(radius=0.09, color=COL_BAD, fill_color="#DC2626", fill_opacity=1.0).move_to([-1.25, -0.28, 0.0])
        or_icon_ring = Annulus(
            inner_radius=0.16, outer_radius=0.26,
            color=COL_BAD, fill_color="#DC2626", fill_opacity=0.9,
            stroke_width=1.8, stroke_color=COL_BAD
        ).move_to([-3.0, -1.78, 0.0])
        or_badge = _h6_19_badge("O-RING: วงปิดสนิท (ฝั่งก้านสูบ)", COL_BAD).move_to([-1.2, -1.78, 0.0])
        or_arrow = Arrow([-1.75, -1.62, 0.0], [-1.28, -0.40, 0.0], color=COL_BAD, stroke_width=2.2, tip_length=0.11)
        oring_mob = VGroup(or_dot_t, or_dot_b, or_icon_ring, or_badge, or_arrow)

        cross_section = VGroup(
            cyl_bg, cyl_t, cyl_b, lbl_barrel, chamber_grp,
            rod_grp, piston_t, piston_b, lbl_piston, grooves_grp
        )

        banner2 = _h6_19_banner(
            "Piston Ring: ฝั่งแรงดัน ซีลลูกสูบกับผนังกระบอกสูบ (ยอมรั่วซึมนิดหน่อยได้) — O-ring: ฝั่งก้านสูบ ซีลนิ่งสนิท 100%",
            COL_OK
        )

        self.play(FadeIn(cross_section, shift=UP * 0.25), FadeIn(banner2), run_time=1.0)
        # Sequentially Indicate piston ring (Lesson 5: after FadeIn)
        self.play(
            FadeIn(piston_ring_mob),
            run_time=0.6
        )
        self.play(
            Indicate(piston_ring_mob, color=COL_OK, scale_factor=1.06),
            run_time=0.8
        )
        self.wait(1.0)

        # Sequentially Indicate O-ring
        self.play(
            FadeIn(oring_mob),
            run_time=0.6
        )
        self.play(
            Indicate(oring_mob, color=COL_BAD, scale_factor=1.06),
            run_time=0.8
        )
        self.wait(3.5)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 26.6–33.5: Heat Resistance Comparison (Metal vs Elastomer)
        # ======================================================================
        cap3 = _h6_19_caption_top("3. โลหะทนความร้อนได้ดีกว่ายาง")
        self.play(FadeIn(cap3, shift=UP * 0.35), run_time=0.5)

        # Left Card: Elastomer / Rubber O-ring (Fails at high temp)
        c_el_box = RoundedRectangle(
            width=5.6, height=3.3, corner_radius=0.14,
            color=COL_BAD, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([-3.1, -0.05, 0.0])
        c_el_head = _h6_19_badge("ยางสังเคราะห์ (Elastomer / O-ring)", COL_BAD).move_to([-3.1, 1.25, 0.0])

        icon_cross = Text("✕", font_size=38, color=COL_BAD).move_to([-4.8, 0.45, 0.0])
        flame_el = _h6_19_flame_icon(color=COL_WARN, scale=0.28).move_to([-3.4, 0.45, 0.0])
        lbl_flame_el = Text("ความร้อนสูง", font_size=12, color=COL_WARN).next_to(flame_el, RIGHT, buff=0.15)
        icon_flame_el = VGroup(flame_el, lbl_flame_el)
        status_el = _h6_19_badge("เสื่อมสภาพที่อุณหภูมิสูง", COL_BAD).move_to([-3.1, -0.15, 0.0])
        points_el = VGroup(
            Text("• เนื้อยางจะแข็งกรอบ ละลาย หรือสูญเสียความยืดหยุ่น", font_size=10.5, color=WHITE),
            Text("• ไม่สามารถใช้งานในจุดที่มีความร้อนสะสมสูงจัดได้", font_size=10.5, color=COL_GRAY),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([-3.1, -0.90, 0.0])
        card_elastomer = VGroup(c_el_box, c_el_head, icon_cross, icon_flame_el, status_el, points_el)

        # Right Card: Metallic Piston Ring (Survives high temp)
        c_me_box = RoundedRectangle(
            width=5.6, height=3.3, corner_radius=0.14,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([3.1, -0.05, 0.0])
        c_me_head = _h6_19_badge("แหวนโลหะ (Metallic Piston Ring)", COL_METAL).move_to([3.1, 1.25, 0.0])

        icon_check = Text("✓", font_size=38, color=COL_OK).move_to([1.4, 0.45, 0.0])
        flame_me = _h6_19_flame_icon(color=COL_OK, scale=0.28).move_to([2.8, 0.45, 0.0])
        lbl_flame_me = Text("ความร้อนสูง", font_size=12, color=COL_OK).next_to(flame_me, RIGHT, buff=0.15)
        icon_flame_me = VGroup(flame_me, lbl_flame_me)
        status_me = _h6_19_badge("ทนความร้อนสูงได้ดีเยี่ยม", COL_OK).move_to([3.1, -0.15, 0.0])
        points_me = VGroup(
            Text("• ทนทานต่ออุณหภูมิสูงจัดได้ดี ไม่เสียรูปหรือละลาย", font_size=10.5, color=WHITE),
            Text("• จึงใช้ piston ring แทน O-ring ตรงจุดที่ร้อนจัด", font_size=10.5, color=COL_OK),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([3.1, -0.90, 0.0])
        card_metal = VGroup(c_me_box, c_me_head, icon_check, icon_flame_me, status_me, points_me)

        banner3 = _h6_19_banner(
            "อุณหภูมิสูงเกินไป: ยางเสื่อมสภาพ แต่โลหะยังทนอยู่ได้ — จึงใช้ piston ring แทน O-ring ตรงจุดที่ร้อนจัด",
            COL_OK
        )

        self.play(FadeIn(VGroup(card_elastomer, card_metal), shift=UP * 0.25), FadeIn(banner3), run_time=1.0)
        self.play(
            Indicate(icon_cross, color=COL_BAD, scale_factor=1.15),
            Indicate(icon_check, color=COL_OK, scale_factor=1.15),
            run_time=0.9
        )
        self.wait(4.5)

        self.clear_stage(run_time=0.6)
        self.wait(0.2)

        # ======================================================================
        # BEAT 34.1–37.5: Summary Card
        # ======================================================================
        card_box = RoundedRectangle(
            width=11.6, height=3.6, corner_radius=0.15,
            color=COL_OK, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        s_head = Text("สรุป: แหวนลูกสูบ (Piston Rings - hydraulic06 น.22)", font_size=13.5, color=COL_OK).move_to([0.0, 1.35, 0.0])
        rows = [
            "1. วัสดุเป็นโลหะ: ไม่ใช่ยางสังเคราะห์ (Elastomer) จึงทนทานต่อสภาวะแวดล้อมที่รุนแรงได้ดีกว่า",
            "2. มีรอยผ่า (End Gap): ทำหน้าที่ถ่างสวมเข้าร่องลูกสูบได้ และยอมให้มีการรั่วซึมเล็กน้อยได้โดยตั้งใจ",
            "3. ทนความร้อนสูงกว่ายาง: จึงถูกเลือกใช้แทน O-ring ในจุดของกระบอกสูบที่มีอุณหภูมิสูงจัด"
        ]
        s_rows = VGroup(*[Text(r, font_size=11, color=WHITE) for r in rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.0, -0.15, 0.0])
        summary_grp = VGroup(card_box, s_head, s_rows)

        self.play(FadeIn(summary_grp, shift=UP * 0.4), run_time=0.7)
        self.wait(2.7)

        # ======================================================================
        # BEAT 37.5–41.0: Review Question Card
        # ======================================================================
        self.play(FadeOut(summary_grp), run_time=0.4)

        q_box = RoundedRectangle(
            width=11.2, height=3.0, corner_radius=0.15,
            color=COL_WARN, fill_color=COL_BG_BOX
        ).set_fill(COL_BG_BOX, 0.95).move_to([0.0, -0.15, 0.0])
        q_head = Text("คำถามทบทวนประจำคลิป (Check Your Understanding)", font_size=14, color=COL_WARN).move_to([0.0, 1.05, 0.0])
        q_body = Text(
            "ทำไม piston ring ถึงยอมให้มีรอยรั่วเล็กน้อยได้ ทั้งที่ O-ring ในภาพเดียวกันต้องซีลสนิท 100%?",
            font_size=13, color=WHITE
        ).move_to([0.0, 0.20, 0.0])
        q_ans = Text(
            "(คำตอบ: เพราะ piston ring เป็นโลหะที่เน้นทนความร้อนสูง และจำเป็นต้องมีรอยผ่าเพื่อถ่างสวมเข้าร่อง\nขณะที่ O-ring เป็นยางที่ซีลสนิท 100% ตรงรอยต่อก้านสูบที่ไม่สัมผัสความร้อนสูงโดยตรง)",
            font_size=11.5, color=COL_GRAY
        ).move_to([0.0, -0.60, 0.0])
        question_grp = VGroup(q_box, q_head, q_body, q_ans)

        self.play(FadeIn(question_grp, shift=UP * 0.3), run_time=0.6)
        self.wait(2.9)

        self.play(FadeOut(question_grp), run_time=0.5)
        self.wait(0.2)
        self.fade_out_all(run_time=0.6)
        self.wait(0.5)
