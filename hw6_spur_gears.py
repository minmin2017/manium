import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mlib import *

# Palette for Spur Gears and Gear Trains
GEAR2_COL = GEAR_IN     # "#4FC3F7" (Driver)
GEAR3_COL = GEAR_OUT    # "#FFB74D" (Driven)
IDLER_COL = GEAR_MID    # "#81C784" (Idler)
WORM_COL  = "#BA68C8"   # Purple (Worm)
PITCH_COL = OK          # "#26C6DA"
BASE_COL  = "#AB47BC"
LOA_COL   = "#EF5350"
ACTION_COL= "#FFD54F"


# ==============================================================================
# PAGE 1: Spur Gears & Plane Gear Train (Q1 - Q7)
# ==============================================================================
class HW6Page01Scene(SafeScene):
    def construct(self):
        pref = page_ref("การบ้าน 6 · หน้า 1 (Q1 – Q7)")
        ttl = title("เรขาคณิตเฟืองตรง & ชุดเฟืองระนาบ")
        cap = caption_top("สรุป 7 ข้อสำคัญ: อินโวลูต, ฟันแหลม, แร็ค, ช่วงการขบ Z, สัดส่วนมาตรฐาน, ชุดเฟือง")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        # ------------------------------------------------------------
        # Part 1: Involute & Pointed Tooth (Q1 & Q2)
        # ------------------------------------------------------------
        cap1 = caption_top("Q1-Q2: เส้นอินโวลูตขยายจนตัดกันเกิดฟันแหลม (Pointed Tooth)")
        self.play(FadeIn(cap1), run_time=0.5)

        base_circ = Circle(radius=2.2, color=BASE_COL, stroke_width=2.5).move_to([-3.2, -0.6, 0])
        base_lbl = Text("Base Circle rb=95.8 mm", font_size=15, color=BASE_COL).next_to(base_circ, DOWN, buff=0.15)

        # Involute curves
        thetas = np.linspace(0, 0.65, 50)
        pts_left = [base_circ.get_center() + np.array([2.2*(np.cos(th) + th*np.sin(th)), 2.2*(np.sin(th) - th*np.cos(th)), 0]) for th in thetas]
        pts_right= [base_circ.get_center() + np.array([2.2*(np.cos(-th) - th*np.sin(-th)), 2.2*(-np.sin(-th) - th*np.cos(-th)), 0]) for th in thetas]
        
        # Shift to form tooth symmetric around x-axis
        curve1 = VMobject(color=OK, stroke_width=3.5).set_points_smoothly(pts_left)
        curve2 = VMobject(color=OK, stroke_width=3.5).set_points_smoothly([np.array([p[0], -p[1] + 2*base_circ.get_center()[1], 0]) for p in pts_left])
        
        point_dot = Dot(color=WARN, radius=0.1).move_to([-3.2 + 2.8, -0.6, 0])
        point_lbl = Text("Pointed Tooth (t=0)\nr=109.46 mm", font_size=16, color=WARN).next_to(point_dot, RIGHT, buff=0.2)
        
        p1_grp = VGroup(base_circ, base_lbl, curve1, curve2, point_dot, point_lbl)

        # Equations panel on the right
        eq_q1 = VGroup(
            Text("Q1: รัศมีฟันแหลม (Pointed Tooth)", font_size=18, color=WHITE),
            MathTex(r"\text{inv}\,\phi_2 = \text{inv}\,\phi_1 + \frac{t_1}{2r_1} = 0.047502", color=ACTION_COL, font_size=18),
            MathTex(r"\phi_2 = 28.88^\circ \implies r_2 = \frac{r_b}{\cos\phi_2} = \mathbf{109.46\text{ mm}}", color=OK, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        eq_q2 = VGroup(
            Text("Q2: ความหนาฟันที่วงกลมโคน (Base Circle)", font_size=18, color=WHITE),
            MathTex(r"t_b = r_b\left(\frac{t_1}{r_1} + 2\,\text{inv}\,\phi_1\right)", color=ACTION_COL, font_size=18),
            MathTex(r"t_b = 47.74(0.0980 + 0.0298) = \mathbf{6.10\text{ mm}}", color=OK, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        right_panel1 = VGroup(eq_q1, eq_q2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, -0.6, 0])

        self.play(Create(base_circ), FadeIn(base_lbl), Create(curve1), Create(curve2), FadeIn(point_dot), FadeIn(point_lbl), run_time=1.2)
        self.play(FadeIn(right_panel1, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(p1_grp), FadeOut(right_panel1), FadeOut(cap1), run_time=0.6)

        # ------------------------------------------------------------
        # Part 2: Pinion & Rack / Length of Action (Q3, Q4, Q5)
        # ------------------------------------------------------------
        cap2 = caption_top("Q3-Q5: แนวแรงขบ (Line of Action) และช่วงการสัมผัส Z")
        self.play(FadeIn(cap2), run_time=0.5)

        # Center stage: Pinion & Rack diagram
        p_c = np.array([-3.2, 0.8, 0])
        pitch_circle = Circle(radius=1.8, color=PITCH_COL, stroke_width=2.5).move_to(p_c)
        base_circle_p = Circle(radius=1.8 * np.cos(np.radians(20)), color=BASE_COL, stroke_width=2).move_to(p_c)
        add_circle_p  = Circle(radius=1.8 + 0.35, color=WHITE, stroke_width=1.5).move_to(p_c)

        pitch_pt = p_c + np.array([0, -1.8, 0])
        rack_pitch_line = Line([-5.5, pitch_pt[1], 0], [-0.5, pitch_pt[1], 0], color=PITCH_COL, stroke_width=2.5)
        rack_add_line   = Line([-5.5, pitch_pt[1] + 0.35, 0], [-0.5, pitch_pt[1] + 0.35, 0], color=WHITE, stroke_width=1.5)

        # Line of Action: passes through pitch_pt at 20 deg to horizontal
        loa_dir = np.array([np.cos(np.radians(20)), -np.sin(np.radians(20)), 0])
        loa_line = Line(pitch_pt - loa_dir * 1.5, pitch_pt + loa_dir * 1.5, color=LOA_COL, stroke_width=3)
        contact_seg = Line(pitch_pt - loa_dir * 0.75, pitch_pt + loa_dir * 0.65, color=ACTION_COL, stroke_width=5)

        lbl_P = Dot(pitch_pt, color=PITCH_COL, radius=0.08)
        txt_P = Text("P", font_size=15, color=PITCH_COL).next_to(lbl_P, DOWN, buff=0.1)
        lbl_A = Dot(pitch_pt - loa_dir * 0.75, color=WARN, radius=0.08)
        txt_A = Text("A (เริ่มขบ)", font_size=14, color=WARN).next_to(lbl_A, LEFT, buff=0.1)
        lbl_B = Dot(pitch_pt + loa_dir * 0.65, color=OK, radius=0.08)
        txt_B = Text("B (สิ้นสุด)", font_size=14, color=OK).next_to(lbl_B, RIGHT, buff=0.1)

        rack_grp = VGroup(pitch_circle, base_circle_p, add_circle_p, rack_pitch_line, rack_add_line, loa_line, contact_seg, lbl_P, txt_P, lbl_A, txt_A, lbl_B, txt_B)

        eq_q35 = VGroup(
            Text("Q3: Pinion & Rack Contact", font_size=17, color=WHITE),
            MathTex(r"AP = \frac{a_r}{\sin 20^\circ} = \mathbf{14.62\text{ mm}}", color=ACTION_COL, font_size=17),
            MathTex(r"PB = \sqrt{R_a^2-R_b^2}-R_p\sin 20^\circ = \mathbf{11.49\text{ mm}}", color=ACTION_COL, font_size=17),
            MathTex(r"Z = AP + PB = \mathbf{26.11\text{ mm}}", color=OK, font_size=17),
            Text("Q4: Contact Ratio mp (48T ขบ 48T)", font_size=17, color=WHITE),
            MathTex(r"m_p = \frac{Z}{p_b} = \frac{20.64}{11.81} = \mathbf{1.75}", color=OK, font_size=17),
            Text("Q5: Max Rack Addendum (No Interference)", font_size=17, color=WHITE),
            MathTex(r"a_{r,\max} = R_p \sin^2(20^\circ) = 38\sin^2 20^\circ = \mathbf{4.45\text{ mm}}", color=OK, font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, -0.6, 0])

        self.play(FadeIn(rack_grp), run_time=1.2)
        self.play(FadeIn(eq_q35, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(rack_grp), FadeOut(eq_q35), FadeOut(cap2), run_time=0.6)

        # ------------------------------------------------------------
        # Part 3: Gear Train with Idler (Q7)
        # ------------------------------------------------------------
        cap3 = caption_top("Q7: ชุดเฟืองระนาบพร้อมเฟืองสะพาน (Idler Gear ไม่เปลี่ยนอัตราทด)")
        self.play(FadeIn(cap3), run_time=0.5)

        # Draw gear train chain
        g2 = Circle(radius=0.5, color=GEAR2_COL, stroke_width=3).move_to([-5.2, -0.6, 0])
        g3 = Circle(radius=1.1, color=GEAR3_COL, stroke_width=3).move_to([-3.6, -0.6, 0])
        g4 = Circle(radius=0.45, color=GEAR2_COL, stroke_width=3).move_to([-3.6, -0.6, 0])
        g5 = Circle(radius=0.9, color=GEAR3_COL, stroke_width=3).move_to([-2.25, -0.6, 0])
        g6 = Circle(radius=0.5, color=GEAR2_COL, stroke_width=3).move_to([-2.25, -0.6, 0])
        g7 = Circle(radius=0.7, color=IDLER_COL, stroke_width=3).move_to([-1.05, -0.6, 0])
        g8 = Circle(radius=1.2, color=GEAR3_COL, stroke_width=3).move_to([0.85, -0.6, 0])

        t2 = Text("2:18T\nCW", font_size=12, color=WHITE).move_to(g2)
        t3 = Text("3:44T", font_size=12, color=WHITE).move_to(g3.get_top() + DOWN*0.25)
        t5 = Text("5:33T", font_size=12, color=WHITE).move_to(g5.get_top() + DOWN*0.25)
        t7 = Text("7:25T\n(Idler)", font_size=12, color=IDLER_COL).move_to(g7)
        t8 = Text("8:48T\nCW", font_size=14, color=OK).move_to(g8)

        # Arrows indicating direction
        ar2 = MathTex(r"\curvearrowright", color=GEAR2_COL, font_size=24).next_to(g2, UP, buff=0.05)
        ar7 = MathTex(r"\curvearrowleft", color=IDLER_COL, font_size=24).next_to(g7, UP, buff=0.05)
        ar8 = MathTex(r"\curvearrowright", color=OK, font_size=28).next_to(g8, UP, buff=0.05)

        train_grp = VGroup(g2, g3, g4, g5, g6, g7, g8, t2, t3, t5, t7, t8, ar2, ar7, ar8)

        eq_q7 = VGroup(
            Text("สูตรอัตราทดชุดเฟือง (Train Value):", font_size=17, color=WHITE),
            MathTex(r"e = \frac{N_2 \times N_4 \times N_6 \times N_7}{N_3 \times N_5 \times N_7 \times N_8} = \frac{N_2 N_4 N_6}{N_3 N_5 N_8}", color=ACTION_COL, font_size=17),
            MathTex(r"e = \frac{18 \times 15 \times 18}{44 \times 33 \times 48} = \frac{135}{1936} \approx 0.06973", color=WHITE, font_size=17),
            MathTex(r"\omega_8 = 800 \times \frac{135}{1936} = \mathbf{55.79\text{ rpm}}", color=OK, font_size=19),
            Text("ทิศทาง: CW -> CCW -> CW -> CCW -> CW (ตามเข็ม)", font_size=15, color=OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.8, 1.5, 0])

        self.play(FadeIn(train_grp), run_time=1.2)
        self.play(FadeIn(eq_q7, shift=UP * 0.2), run_time=1.0)
        self.wait(3.0)
        self.fade_out_all(run_time=0.6)


# ==============================================================================
# PAGE 2: 3D Complex Gear Train (Q8)
# ==============================================================================
class HW6Page02Scene(SafeScene):
    def construct(self):
        pref = page_ref("การบ้าน 6 · หน้า 2 (Q8)")
        ttl = title("ชุดเฟืองผสม 4 ระบบ: สายพาน + ดอกจอก + เฟืองตรง + เฟืองตัวหนอน")
        cap = caption_top("โจทย์ Q8: คำนวณความเร็วรอบและทิศทางการหมุน 3 มิติของล้อหนอน 9")
        self.play(FadeIn(pref), FadeIn(ttl), FadeIn(cap), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.4)

        # Stage blocks breakdown
        cap1 = caption_top("สายส่งกำลัง 4 สเตจ: จากมอเตอร์ 1200 rpm สู่เอาต์พุตล้อหนอน 11.84 rpm")
        self.play(FadeIn(cap1), run_time=0.5)

        s1 = VGroup(
            Text("สเตจ 1: สายพาน V-Belt (เปิด)", font_size=17, color=WHITE),
            MathTex(r"n_3 = n_2 \left(\frac{D_2}{D_3}\right) = 1200 \left(\frac{150}{250}\right) = \mathbf{720\text{ rpm}}", color=ACTION_COL, font_size=17),
            Text("สายพานเปิด หมุนทิศเดิม (CW)", font_size=14, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        s2 = VGroup(
            Text("สเตจ 2: เฟืองดอกจอก Bevel 90°", font_size=17, color=WHITE),
            MathTex(r"n_5 = n_4 \left(\frac{N_4}{N_5}\right) = 720 \left(\frac{18}{38}\right) = \mathbf{341.05\text{ rpm}}", color=ACTION_COL, font_size=17),
            Text("เปลี่ยนระนาบ เพลาตั้งหมุน CW (มองจากบน)", font_size=14, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        s3 = VGroup(
            Text("สเตจ 3: เฟืองตรง Spur Gears", font_size=17, color=WHITE),
            MathTex(r"n_7 = n_6 \left(\frac{N_6}{N_7}\right) = 341.05 \left(\frac{20}{48}\right) = \mathbf{142.11\text{ rpm}}", color=ACTION_COL, font_size=17),
            Text("ขบภายนอก สลับทิศเป็น CCW (มองจากบน)", font_size=14, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        s4 = VGroup(
            Text("สเตจ 4: หนอนและล้อหนอน Worm 3T R.H.", font_size=17, color=WHITE),
            MathTex(r"n_9 = n_8 \left(\frac{N_8}{N_9}\right) = 142.11 \left(\frac{3}{36}\right) = \mathbf{11.84\text{ rpm}}", color=OK, font_size=17),
            Text("หนอน 3 ปาก ล้อ 36 ฟัน ทดรอบ 1:12", font_size=14, color=GRAYTXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        stages_grp = VGroup(s1, s2, s3, s4).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.2, -0.3, 0])

        total_box = VGroup(
            Text("สูตรรวมอัตราทดทั้งระบบ:", font_size=18, color=WHITE),
            MathTex(r"\frac{n_9}{n_2} = \frac{D_2}{D_3} \times \frac{N_4}{N_5} \times \frac{N_6}{N_7} \times \frac{N_8}{N_9} = \frac{3}{304}", color=ACTION_COL, font_size=18),
            MathTex(r"n_9 = 1200 \times \frac{3}{304} = \frac{225}{19} \approx \mathbf{11.84\text{ rpm}}", color=OK, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 0.5, 0])

        self.play(FadeIn(stages_grp, shift=RIGHT * 0.2), run_time=1.2)
        self.play(FadeIn(total_box, shift=UP * 0.2), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(stages_grp), FadeOut(total_box), FadeOut(cap1), run_time=0.6)

        # Right-Hand Rule demonstration for Worm Gear
        cap2 = caption_top("การหาทิศทาง 3 มิติ: กฎมือขวาสำหรับเกลียวหนอน (Right-Hand Rule)")
        self.play(FadeIn(cap2), run_time=0.5)

        worm_rect = Rectangle(width=1.0, height=2.0, color=WORM_COL, fill_opacity=0.3, fill_color=WORM_COL).move_to([-2.5, -0.5, 0])
        worm_lbl = Text("Worm 8\n(3T R.H.)", font_size=14, color=WHITE).move_to(worm_rect)
        worm_shaft = Line([-2.5, 1.2, 0], [-2.5, -2.2, 0], color=METAL, stroke_width=4)

        gear_circ = Circle(radius=1.3, color=GEAR3_COL, fill_opacity=0.25, fill_color=GEAR3_COL).move_to([-0.7, -0.5, 0])
        gear_lbl = Text("Worm Gear 9\n(36T)", font_size=14, color=WHITE).move_to(gear_circ)

        mesh_dot = Dot([-1.7, -0.5, 0], color=WARN, radius=0.12)
        force_arrow = Arrow([-1.7, -0.1, 0], [-1.7, -1.1, 0], color=WARN, buff=0, stroke_width=5)
        force_lbl = Text("แรงกดลงด้านล่าง", font_size=14, color=WARN).next_to(force_arrow, LEFT, buff=0.1)

        rot_arrow = MathTex(r"\curvearrowleft", color=OK, font_size=40).next_to(gear_circ, UP, buff=0.1)
        rot_lbl = Text("หมุนทวนเข็ม (CCW)\nมองจากด้านหน้า", font_size=15, color=OK).next_to(gear_circ, RIGHT, buff=0.2)

        worm_diagram = VGroup(worm_shaft, worm_rect, worm_lbl, gear_circ, gear_lbl, mesh_dot, force_arrow, force_lbl, rot_arrow, rot_lbl)

        rh_steps = VGroup(
            Text("ขั้นตอนพิสูจน์กฎมือขวา (เกลียวขวา R.H.):", font_size=18, color=WHITE),
            Text("1. หนอน 8 หมุนทวนเข็มนาฬิกา (CCW) เมื่อมองจากบน", font_size=16, color=GRAYTXT),
            Text("2. กำมือขวาตามทิศหมุน -> หัวแม่มือชี้ขึ้น (UP)", font_size=16, color=GRAYTXT),
            Text("3. หนอนถูกล็อคแนวแกน -> ฟันหนอนส่งแรงกดลง (DOWN)", font_size=16, color=WARN),
            Text("4. แรงกดลงที่ฝั่งซ้ายของล้อหนอน 9 ทำให้ล้อหมุนทวนเข็ม", font_size=16, color=OK),
            VGroup(Text("ทิศทาง:", font_size=17, color=OK), MathTex(r"\boxed{\text{Counter-Clockwise (CCW)}}", color=OK, font_size=19)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.0, 0])

        self.play(FadeIn(worm_diagram), run_time=1.2)
        self.play(FadeIn(rh_steps, shift=LEFT * 0.3), run_time=1.0)
        self.wait(3.5)
        self.fade_out_all(run_time=0.6)
