"""
car_internal_systems.py — EV Internal Systems Architecture: From Pedal to Wheels
Scene Class: CarInternalSystems
Audience: Adult learner, zero automotive background.
Topic: Internal EV components, Signal Flow vs Energy Flow, Mechanical Torque, Closed-Loop Feedback.
"""

from manim import *
from mlib import *


class CarInternalSystems(SafeScene):
    """
    25-second 2D cutaway prototype demonstrating internal EV systems:
    Accelerator Pedal -> ECU -> Battery/Inverter -> Motor -> Reduction Gear -> Wheel,
    with sensor feedback returning to ECU and clear Signal vs Energy distinction.
    """

    def construct(self):
        # ----------------------------------------------------------------- Header
        main_title = title("ระบบกลไกภายในรถยนต์ไฟฟ้า (EV Internal Systems Architecture)", color=WHITE, size=27)
        self.add(main_title)

        # --------------------------------------------------------- Beat 1: 0 - 5s
        # 2D Transparent Car Silhouette & Component Layout
        cap1 = caption_top("1. โครงสร้างภายใน: ผ่าดูชิ้นส่วนหลักจากแป้นคันเร่งสู่ล้อขับเคลื่อน")
        self.play(FadeIn(cap1), run_time=0.8)

        # Ground line
        road = Line(LEFT * 6.5, RIGHT * 6.5, color="#455A64", stroke_width=3).shift(DOWN * 2.3)
        self.play(Create(road), run_time=0.6)

        # Transparent car silhouette outline
        car_outline = Polygon(
            [-4.8, -1.8, 0], [-4.9, -1.0, 0], [-4.2, -0.2, 0], [-2.8, -0.1, 0],
            [-1.8, 1.1, 0], [0.8, 1.1, 0], [2.4, 0.0, 0], [4.6, -0.2, 0],
            [4.8, -1.8, 0],
            color=METAL, stroke_width=2.5, fill_color=METAL, fill_opacity=0.08
        )
        self.play(FadeIn(car_outline), run_time=0.8)

        # Physical Components (2D Schematic Blocks)
        # Rear wheel (idle) and Front wheel (driven)
        r_wheel = Circle(radius=0.55, color=METAL, fill_color=BLACK, fill_opacity=0.85).move_to([-3.4, -1.75, 0])
        f_wheel = Circle(radius=0.55, color=METAL, fill_color=BLACK, fill_opacity=0.85).move_to([3.1, -1.75, 0])
        r_hub = Dot(r_wheel.get_center(), color=GRAY, radius=0.08)
        f_hub = Dot(f_wheel.get_center(), color=GRAY, radius=0.08)
        wheels_group = VGroup(r_wheel, r_hub, f_wheel, f_hub)

        # Accelerator Pedal
        pedal_base = Line([-1.6, -1.2, 0], [-1.3, -0.6, 0], color=WHITE, stroke_width=4)
        pedal_pad = Rectangle(width=0.18, height=0.35, color=WHITE, fill_color="#78909C", fill_opacity=0.8).move_to([-1.25, -0.55, 0]).rotate(25 * DEGREES)
        pedal = VGroup(pedal_base, pedal_pad)
        lbl_pedal = Text("คันเร่ง", font_size=15, color=WHITE).next_to(pedal, UP, buff=0.12)

        # ECU (Electronic Control Unit)
        ecu_box = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.7, color=BLUE_B, fill_color="#102027", fill_opacity=0.9).move_to([-0.2, -0.1, 0])
        lbl_ecu = Text("กล่อง ECU", font_size=15, color=BLUE_B).move_to(ecu_box.get_center())
        ecu = VGroup(ecu_box, lbl_ecu)

        # HV Battery (Traction Battery Pack on floor)
        bat_box = RoundedRectangle(corner_radius=0.1, width=2.4, height=0.55, color="#26A69A", fill_color="#004D40", fill_opacity=0.8).move_to([-0.8, -1.4, 0])
        lbl_bat = Text("แบตเตอรี่แรงสูง (HV)", font_size=14, color="#80CBC4").move_to(bat_box.get_center())
        battery = VGroup(bat_box, lbl_bat)

        # Inverter (Power Electronics)
        inv_box = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.65, color=TEAL_A, fill_color="#006064", fill_opacity=0.85).move_to([1.5, 0.1, 0])
        lbl_inv = Text("อินเวอร์เตอร์", font_size=14, color=TEAL_A).move_to(inv_box.get_center())
        inverter = VGroup(inv_box, lbl_inv)

        # Electric Motor
        motor_box = Circle(radius=0.45, color=GEAR_IN, fill_color="#01579B", fill_opacity=0.85).move_to([1.5, -0.85, 0])
        lbl_motor = Text("มอเตอร์", font_size=14, color=GEAR_IN).move_to(motor_box.get_center())
        motor = VGroup(motor_box, lbl_motor)

        # Reduction Gear
        gear_box = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.55, color=GEAR_OUT, fill_color="#E65100", fill_opacity=0.85).move_to([2.35, -1.15, 0])
        lbl_gear = Text("เกียร์ทด", font_size=13, color=GEAR_OUT).move_to(gear_box.get_center())
        gear = VGroup(gear_box, lbl_gear)

        components = VGroup(wheels_group, pedal, lbl_pedal, ecu, battery, inverter, motor, gear)
        self.play(FadeIn(components), run_time=1.4)
        self.wait(1.4)

        # -------------------------------------------------------- Beat 2: 5 - 10s
        # Signal Pulse: Pedal -> ECU
        cap2 = caption_top("2. กระแสสัญญาณ (Signal): คนขับกดคันเร่ง ส่งข้อมูลคำสั่งระดับมิลลิวัตต์เข้า ECU")
        self.play(ReplacementTransform(cap1, cap2), run_time=0.8)

        wire_pedal_ecu = Line(pedal_pad.get_center(), ecu_box.get_left(), color=YELLOW_D, stroke_width=2.5)
        self.play(Create(wire_pedal_ecu), run_time=0.6)

        sig_badge = Text("สัญญาณคำสั่ง (Signal)", font_size=15, color=YELLOW).move_to([-0.8, 0.7, 0])
        self.play(FadeIn(sig_badge), run_time=0.5)

        sig_pulse = Dot(color=YELLOW, radius=0.12)
        self.play(MoveAlongPath(sig_pulse, wire_pedal_ecu), run_time=1.8, rate_func=linear)
        self.play(Flash(ecu_box, color=YELLOW, flash_radius=0.4), FadeOut(sig_pulse), run_time=0.6)
        self.wait(0.7)

        # ------------------------------------------------------- Beat 3: 10 - 16s
        # ECU commands Inverter, High Energy flows: Battery -> Inverter -> Motor
        cap3 = caption_top("3. กระแสพลังงาน (Energy): ECU สั่งอินเวอร์เตอร์ ดึงไฟแรงสูงจากแบตเตอรี่จ่ายมอเตอร์")
        self.play(
            ReplacementTransform(cap2, cap3),
            FadeOut(sig_badge),
            run_time=0.8
        )

        wire_ecu_inv = Line(ecu_box.get_right(), inv_box.get_left(), color=YELLOW_D, stroke_width=2.5)
        bus_bat_inv = Line(bat_box.get_right() + UP * 0.1, inv_box.get_bottom() + LEFT * 0.2, color=TEAL_C, stroke_width=5)
        bus_inv_mot = Line(inv_box.get_bottom() + RIGHT * 0.2, motor_box.get_top(), color=TEAL_C, stroke_width=5)

        self.play(Create(wire_ecu_inv), Create(bus_bat_inv), Create(bus_inv_mot), run_time=1.0)

        # Signal triggers inverter
        pulse_trig = Dot(color=YELLOW, radius=0.1)
        self.play(MoveAlongPath(pulse_trig, wire_ecu_inv), run_time=0.8)
        self.play(Flash(inv_box, color=TEAL_A, flash_radius=0.45), FadeOut(pulse_trig), run_time=0.4)

        # High energy surging from Battery -> Inverter -> Motor
        energy_badge = Text("พลังงานขับเคลื่อนแรงดันสูง (High-Voltage Energy)", font_size=15, color=TEAL_A).move_to([1.8, 1.0, 0])
        self.play(FadeIn(energy_badge), run_time=0.5)

        nrg_pulse1 = Dot(color=TEAL_A, radius=0.18)
        nrg_pulse2 = Dot(color=TEAL_A, radius=0.18)
        self.play(MoveAlongPath(nrg_pulse1, bus_bat_inv), run_time=1.0, rate_func=linear)
        self.play(MoveAlongPath(nrg_pulse2, bus_inv_mot), run_time=0.9, rate_func=linear)
        self.play(Flash(motor_box, color=GEAR_IN, flash_radius=0.5), FadeOut(nrg_pulse1), FadeOut(nrg_pulse2), run_time=0.6)

        # ------------------------------------------------------- Beat 4: 16 - 21s
        # Mechanical Rotation: Motor -> Gear -> Axle -> Wheels
        cap4 = caption_top("4. การส่งถ่ายเชิงกล: มอเตอร์หมุนเกียร์ทดรอบ เพื่อขยายแรงบิดหมุนล้อขับเคลื่อน")
        self.play(
            ReplacementTransform(cap3, cap4),
            FadeOut(energy_badge),
            run_time=0.8
        )

        shaft_mot_gear = Line(motor_box.get_right() + DOWN * 0.15, gear_box.get_left(), color=WHITE, stroke_width=4)
        shaft_gear_wheel = Line(gear_box.get_right() + DOWN * 0.15, f_wheel.get_center(), color=WHITE, stroke_width=4)
        self.play(Create(shaft_mot_gear), Create(shaft_gear_wheel), run_time=0.6)

        torque_eq = MathTex(r"T_{\text{wheel}} = N \cdot T_{\text{motor}}", color=GEAR_OUT, font_size=24).move_to([2.3, 0.7, 0])
        self.play(FadeIn(torque_eq), run_time=0.5)

        # Rotation of motor and driven front wheel
        spoke_f = Line(f_wheel.get_top(), f_wheel.get_bottom(), color=GRAY, stroke_width=2.5)
        spoke_r = Line(r_wheel.get_top(), r_wheel.get_bottom(), color=GRAY, stroke_width=2.5)
        self.add(spoke_f, spoke_r)

        self.play(
            Rotate(motor_box, angle=-3 * PI, run_time=2.2, rate_func=linear),
            Rotate(f_wheel, angle=-1.5 * PI, run_time=2.2, rate_func=linear),
            Rotate(spoke_f, angle=-1.5 * PI, run_time=2.2, rate_func=linear),
            Rotate(r_wheel, angle=-1.5 * PI, run_time=2.2, rate_func=linear),
            Rotate(spoke_r, angle=-1.5 * PI, run_time=2.2, rate_func=linear)
        )
        self.wait(0.9)

        # ------------------------------------------------------- Beat 5: 21 - 25s
        # Sensor feedback pulse returns: Wheel -> ECU + Summary loss & EV architecture note
        cap5 = caption_top("5. ลูปป้อนกลับ (Closed Loop): เซนเซอร์ส่งความเร็วล้อกลับไปรายงาน ECU")
        self.play(
            ReplacementTransform(cap4, cap5),
            FadeOut(torque_eq),
            run_time=0.8
        )

        sensor_wire = Line(f_wheel.get_top(), ecu_box.get_top() + RIGHT * 0.2, color=YELLOW_D, stroke_width=2)
        self.play(Create(sensor_wire), run_time=0.6)

        fb_pulse = Dot(color=YELLOW, radius=0.11)
        self.play(MoveAlongPath(fb_pulse, sensor_wire), run_time=1.4, rate_func=linear)
        self.play(Flash(ecu_box, color=YELLOW, flash_radius=0.4), FadeOut(fb_pulse), run_time=0.4)

        # Final note cards
        note_ev = Text("นี่คือสายพานพลังงานของรถยนต์ไฟฟ้า (EV) · รถสันดาปจะมีกระบอกสูบและเกียร์หลายสปีด", font_size=14, color=GRAYTXT).move_to([0, 1.05, 0])
        note_loss = Text("พลังงานไฟฟ้าและกลมีการสูญเสียเป็นความร้อนเสมอ จึงจำเป็นต้องมีระบบหล่อเย็นคุมอุณหภูมิ", font_size=14, color=WARN).move_to([0, 0.72, 0])
        notes_bg = SurroundingRectangle(VGroup(note_ev, note_loss), color=METAL, fill_color=BLACK, fill_opacity=0.9, buff=0.18)

        self.play(FadeIn(notes_bg), FadeIn(note_ev), FadeIn(note_loss), run_time=0.8)
        self.wait(1.0)
