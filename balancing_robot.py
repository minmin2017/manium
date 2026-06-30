"""
หุ่นยนต์ทรงตัวสองล้อ — ทำไม PID ถึงทำให้มันไม่ล้ม
สไตล์ 3Blue1Brown (manim community 0.19) ภาษาไทย

โครง 11 ฉาก:
  1  ปัญหา (Hook)           2  ทำไมมันล้มเอง
  3  ไอเดียป้อนกลับ          4  P = สปริง
  5  D = โช้คอัพ            6  I = เก็บ error ค้าง
  7  การทดลอง: เปลี่ยนมุมเริ่มต้น PID เท่าเดิม
  8  สรุปบทบาท P-I-D
  9  ตั้งสมการ  10 Linearize  11 Transfer Function

กฎเหล็ก: ตัวอักษรห้ามซ้อนกัน — แต่ละพาร์ทเคลียร์จอก่อนขึ้นใหม่
"""

from manim import *
import numpy as np

Text.set_default(font="Noto Sans Thai")

# ── palette ───────────────────────────────────────────────
BLUE_LIGHT = "#4FC3F7"
GREEN_OK   = "#66BB6A"
RED_FALL   = "#EF5350"
GRAY_MID   = "#90A4AE"
GRAY_DARK  = "#546E7A"
YELLOW_HI  = "#FFD54F"
ORANGE_HI  = "#FFA726"
PURPLE_I   = "#BA68C8"

# ── physics constants (ปรับให้ภาพสวย + สเกลเวลาเหมือนในไฟล์) ──
J_EQ  = 1.0     # (I + M L^2)
MGL   = 6.5     # M g L   → open-loop ล้มถึง 90° ใน ~0.7s จาก 15°
KP, KI, KD = 22.0, 15.0, 1.0   # ค่าจากไฟล์ Reference


def simulate(theta0_deg, T, kp=0.0, ki=0.0, kd=0.0, disturb=0.0, dt=0.01):
    """RK4 ของลูกตุ้มกลับหัว + PID feedback (setpoint = 0)
    state = [theta, omega, integral(theta)]
    J*theta'' = MGL*sin(theta) - u + disturb ,  u = kp*th + kd*om + ki*∫th
    คืน (t_array, theta_deg_array)
    """
    th = np.radians(theta0_deg)
    om = 0.0
    ith = 0.0
    n = int(T / dt)
    ts = np.zeros(n + 1)
    ths = np.zeros(n + 1)
    ths[0] = np.degrees(th)

    def deriv(s):
        th_, om_, ith_ = s
        u = kp * th_ + kd * om_ + ki * ith_
        dom = (MGL * np.sin(th_) - u + disturb) / J_EQ
        return np.array([om_, dom, th_])

    s = np.array([th, om, ith])
    for i in range(n):
        k1 = deriv(s)
        k2 = deriv(s + 0.5 * dt * k1)
        k3 = deriv(s + 0.5 * dt * k2)
        k4 = deriv(s + dt * k3)
        s = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        # หยุดที่ 90° (ล้มราบ) ไม่ให้หมุนเลยไป
        s[0] = np.clip(s[0], -np.pi / 2, np.pi / 2)
        ts[i + 1] = (i + 1) * dt
        ths[i + 1] = np.degrees(s[0])
    return ts, ths


def make_robot(theta_deg, base, scale=1.0, body_color=BLUE_LIGHT, wheel_color=GRAY_MID):
    """หุ่นทรงตัว มองด้านข้าง: ล้อ + ลำตัวเอียง theta จากแนวดิ่ง (บวก = เอียงขวา)"""
    th = np.radians(theta_deg)
    wheel_r = 0.32 * scale
    axle = np.array(base, dtype=float) + np.array([0, wheel_r, 0])

    wheel = Circle(radius=wheel_r, color=wheel_color, stroke_width=4,
                   fill_opacity=0.25).move_to(axle)
    hub = Dot(axle, radius=0.05 * scale, color=wheel_color)

    L_body = 1.9 * scale
    direction = np.array([np.sin(th), np.cos(th), 0])
    top = axle + L_body * direction
    body = Line(axle, top, color=body_color, stroke_width=11)
    # หัวหุ่น (กล่อง CG)
    head = Square(side_length=0.42 * scale, color=body_color,
                  fill_opacity=0.85, stroke_width=2)
    head.move_to(top).rotate(-th)

    return VGroup(wheel, hub, body, head)


def tilt_axes(x_max=3.0, y_max=95):
    ax = Axes(
        x_range=[0, x_max, 1], y_range=[0, y_max, 30],
        x_length=6.4, y_length=3.4,
        axis_config={"color": GRAY_MID, "stroke_width": 2,
                     "include_tip": True, "tip_width": 0.14, "tip_height": 0.14},
        tips=True,
    )
    return ax


def traj_curve(ax, ts, ths, color, width=4):
    pts = [ax.c2p(t, abs(a)) for t, a in zip(ts, ths)]
    c = VMobject(stroke_color=color, stroke_width=width)
    c.set_points_as_corners(pts)
    return c


class BalancingRobot(Scene):
    def construct(self):
        self.s01_hook()
        self.s02_why_fall()        # Open Loop explanation added
        self.s02b_before_after()   # C: Before/After split-screen
        self.s03_feedback()        # A: animated dot on loop
        self.s04_proportional()
        self.s05_derivative()
        self.s06_integral()
        self.s07_vary_initial()    # B: settle-time markers
        self.s08_summary_pid()
        self.s09_setup_eq()
        self.s10_linearize()
        self.s11_transfer()

    # ── helper: เคลียร์ทุกอย่างบนจอแบบนุ่ม ──
    def wipe(self, t=0.6):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=t)
        self.clear()

    def title_top(self, txt, color=WHITE, size=40):
        t = Text(txt, font_size=size, color=color).to_edge(UP, buff=0.45)
        return t

    # ════════════════════════════════════════════════════════
    # 1 — ปัญหา (Hook)
    # ════════════════════════════════════════════════════════
    def s01_hook(self):
        title = Text("หุ่นยนต์ทรงตัว", font_size=60, color=WHITE)
        sub = Text("ทำไม PID ถึงทำให้มันไม่ล้ม?", font_size=34, color=BLUE_LIGHT)
        sub.next_to(title, DOWN, buff=0.35)
        g = VGroup(title, sub).move_to(ORIGIN)
        self.play(Write(title))
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1.2)
        self.play(g.animate.scale(0.55).to_edge(UP, buff=0.4))

        ground = Line(LEFT * 6, RIGHT * 6, color=GRAY_DARK).shift(DOWN * 2.6)
        base = np.array([0, -2.6, 0])
        ts, ths = simulate(8, 1.6)   # ปล่อยล้ม
        tracker = ValueTracker(0)
        robot = always_redraw(
            lambda: make_robot(np.interp(tracker.get_value(), ts, ths), base)
        )
        self.play(Create(ground))
        self.add(robot)
        self.wait(0.6)
        self.play(tracker.animate.set_value(ts[-1]), run_time=1.8, rate_func=linear)
        fall = Text("ปล่อยเฉยๆ → ล้มทันที", font_size=30, color=RED_FALL)
        fall.next_to(ground, UP, buff=0.2).shift(RIGHT * 2.2)
        self.play(FadeIn(fall))
        self.wait(1.0)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 2 — ทำไมมันล้มเอง
    # ════════════════════════════════════════════════════════
    def s02_why_fall(self):
        title = self.title_top("ระบบไม่เสถียรโดยธรรมชาติ", RED_FALL)
        self.play(FadeIn(title))

        base = np.array([-4.2, -1.4, 0])
        robot = make_robot(18, base)
        # ลูกศรแรงโน้มถ่วงดึงล้ม
        th = np.radians(18)
        top = base + np.array([0, 0.32, 0]) + 1.9 * np.array([np.sin(th), np.cos(th), 0])
        g_arrow = Arrow(top, top + DOWN * 1.0, color=RED_FALL, buff=0,
                        stroke_width=6)
        g_lbl = Text("แรงโน้มถ่วง", font_size=22, color=RED_FALL).next_to(g_arrow, RIGHT, buff=0.1)
        theta_lbl = MathTex(r"\theta", color=YELLOW_HI, font_size=40).move_to(base + UP * 0.9 + RIGHT * 0.15)
        self.play(FadeIn(robot))
        self.play(GrowArrow(g_arrow), FadeIn(g_lbl), Write(theta_lbl))
        idea = Text("ยิ่งเอียง → ยิ่งล้มเร็ว", font_size=26, color=GRAY_MID)
        idea.next_to(robot, DOWN, buff=0.4)
        self.play(FadeIn(idea))
        self.wait(0.8)

        # กราฟ open-loop พุ่งชน 90
        ax = tilt_axes().to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        x_lbl = Text("เวลา (s)", font_size=20, color=GRAY_MID).next_to(ax.x_axis, DOWN, buff=0.15)
        y_lbl = Text("มุมเอียง (°)", font_size=20, color=GRAY_MID).next_to(ax.y_axis, UP, buff=0.1)
        floor = DashedLine(ax.c2p(0, 90), ax.c2p(3, 90), color=GRAY_DARK)
        floor_lbl = Text("ล้มราบ 90°", font_size=18, color=GRAY_MID).next_to(floor, UP, buff=0.05).shift(LEFT*1.5)
        ts, ths = simulate(15, 3.0)
        curve = traj_curve(ax, ts, ths, RED_FALL)
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(floor), FadeIn(floor_lbl))
        self.play(Create(curve), run_time=2.0, rate_func=linear)

        # ── อธิบาย Open Loop ──
        ol_box = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.4,
                                  color=RED_FALL, stroke_width=2,
                                  fill_color=RED_FALL, fill_opacity=0.08)
        ol_box.to_edge(RIGHT, buff=0.4).shift(UP * 2.5)
        ol_title = Text("Open Loop คืออะไร?", font_size=22, color=RED_FALL, weight=BOLD)
        ol_desc  = Text("ไม่มีการวัด/ป้อนกลับ\n→ ระบบทำตามคำสั่งเดิม\n  โดยไม่รู้ผลที่เกิดขึ้น", font_size=18, color=WHITE)
        VGroup(ol_title, ol_desc).arrange(DOWN, buff=0.15).move_to(ol_box)
        self.play(FadeIn(ol_box), FadeIn(ol_title), FadeIn(ol_desc))
        self.wait(1.5)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 2b — Before/After: Open Loop vs Closed Loop (C)
    # ════════════════════════════════════════════════════════
    def s02b_before_after(self):
        title = self.title_top("เปรียบเทียบ: Open Loop  vs  Closed Loop", WHITE, size=34)
        self.play(FadeIn(title))

        # divider
        div = Line(UP * 3.2, DOWN * 3.2, color=GRAY_DARK, stroke_width=2).move_to(ORIGIN)
        lbl_ol = Text("Open Loop", font_size=26, color=RED_FALL, weight=BOLD).move_to([-3.2, 2.6, 0])
        lbl_cl = Text("Closed Loop (PID)", font_size=26, color=GREEN_OK, weight=BOLD).move_to([3.2, 2.6, 0])
        self.play(Create(div), FadeIn(lbl_ol), FadeIn(lbl_cl))

        T = 2.5
        ts_ol, ths_ol = simulate(15, T)
        ts_cl, ths_cl = simulate(15, T, kp=KP, kd=KD, ki=KI)

        base_ol = np.array([-3.4, -1.7, 0])
        base_cl = np.array([ 3.4, -1.7, 0])
        ground_ol = Line([-6.4, -1.7 + 0.32 - 1.9 - 0.05, 0],
                         [-0.1, -1.7 + 0.32 - 1.9 - 0.05, 0], color=GRAY_DARK, stroke_width=2)
        ground_cl = Line([ 0.1, -1.7 + 0.32 - 1.9 - 0.05, 0],
                         [ 6.4, -1.7 + 0.32 - 1.9 - 0.05, 0], color=GRAY_DARK, stroke_width=2)
        tracker = ValueTracker(0)

        robot_ol = always_redraw(lambda: make_robot(
            np.interp(tracker.get_value(), ts_ol, ths_ol), base_ol,
            body_color=RED_FALL, wheel_color=GRAY_DARK))
        robot_cl = always_redraw(lambda: make_robot(
            np.interp(tracker.get_value(), ts_cl, ths_cl), base_cl,
            body_color=GREEN_OK, wheel_color=GRAY_DARK))

        desc_ol = Text("ไม่มีป้อนกลับ → ล้มทันที", font_size=20, color=RED_FALL).move_to([-3.2, -3.2, 0])
        desc_cl = Text("PID วัด+แก้ตลอดเวลา → ทรงตัว", font_size=20, color=GREEN_OK).move_to([3.2, -3.2, 0])

        self.play(Create(ground_ol), Create(ground_cl))
        self.add(robot_ol, robot_cl)
        self.play(FadeIn(desc_ol), FadeIn(desc_cl))
        self.play(tracker.animate.set_value(T), run_time=3.5, rate_func=linear)
        self.wait(1.2)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 3 — ไอเดียป้อนกลับ
    # ════════════════════════════════════════════════════════
    def s03_feedback(self):
        title = self.title_top("ระบบควบคุมแบบป้อนกลับ (Closed-Loop Control)",
                               BLUE_LIGHT, size=32)
        self.play(FadeIn(title))

        def block(th_txt, en_txt, color, w=2.2, h=1.1):
            box = Rectangle(width=w, height=h, color=color, stroke_width=3)
            t1 = Text(th_txt, font_size=22, color=WHITE)
            t2 = Text(en_txt, font_size=15, color=color)
            VGroup(t1, t2).arrange(DOWN, buff=0.07).move_to(box)
            return VGroup(box, t1, t2)

        ROW_Y = 0.45
        # — summing junction —
        sj = Circle(radius=0.34, color=WHITE, stroke_width=3).move_to([-4.4, ROW_Y, 0])
        sj_plus = Text("+", font_size=22, color=GREEN_OK).move_to(sj.get_center() + UP * 0.13 + LEFT * 0.16)
        sj_minus = Text("−", font_size=24, color=RED_FALL).move_to(sj.get_center() + DOWN * 0.16 + LEFT * 0.16)
        sum_node = VGroup(sj, sj_plus, sj_minus)

        controller = block("ตัวควบคุม", "PID Controller", GREEN_OK).move_to([-1.6, ROW_Y, 0])
        plant = block("หุ่นยนต์ทรงตัว", "Target System", BLUE_LIGHT, w=2.6).move_to([2.4, ROW_Y, 0])

        # — main-line arrows —
        a_ref = Arrow([-6.4, ROW_Y, 0], sj.get_left(), buff=0.05, color=GRAY_MID, stroke_width=4)
        a_err = Arrow(sj.get_right(), controller[0].get_left(), buff=0.05, color=GRAY_MID, stroke_width=4)
        a_ctrl = Arrow(controller[0].get_right(), plant[0].get_left(), buff=0.05, color=GRAY_MID, stroke_width=4)
        a_out = Arrow(plant[0].get_right(), [6.2, ROW_Y, 0], buff=0.05, color=GRAY_MID, stroke_width=4)

        l_ref = VGroup(Text("มุมเป้าหมาย", font_size=17, color=WHITE),
                       Text("0° (Reference)", font_size=13, color=GRAY_MID)
                       ).arrange(DOWN, buff=0.05).next_to(a_ref, UP, buff=0.12)
        l_err = Text("Error", font_size=16, color=YELLOW_HI).next_to(a_err, UP, buff=0.1)
        l_ctrl = Text("สั่งมอเตอร์", font_size=16, color=GRAY_MID).next_to(a_ctrl, UP, buff=0.1)
        l_out = VGroup(Text("มุมที่วัดได้", font_size=17, color=WHITE),
                       Text("Measured", font_size=13, color=GRAY_MID)
                       ).arrange(DOWN, buff=0.05).next_to(a_out, UP, buff=0.12)

        # — disturbance & noise (เข้าด้านบนของ plant) —
        dx, nx = plant.get_center()[0] - 0.6, plant.get_center()[0] + 0.6
        a_dist = Arrow([dx, 2.7, 0], [dx, plant.get_top()[1] + 0.02, 0], buff=0, color=ORANGE_HI, stroke_width=4)
        a_noise = Arrow([nx, 2.7, 0], [nx, plant.get_top()[1] + 0.02, 0], buff=0, color=RED_FALL, stroke_width=4)
        l_dist = Text("แรงรบกวน", font_size=15, color=ORANGE_HI).next_to(a_dist, UP, buff=0.08)
        l_noise = Text("Noise", font_size=15, color=RED_FALL).next_to(a_noise, UP, buff=0.08)

        # — feedback path ผ่าน transducer —
        transducer = block("เซนเซอร์", "Transducer", PURPLE_I, w=2.4, h=0.95).move_to([0.4, -2.2, 0])
        fb_y = -2.2
        a_fb1 = Line(a_out.get_start() + RIGHT * 0.0, [5.6, ROW_Y, 0], color=GRAY_MID, stroke_width=4)
        fb_corner1 = [5.6, fb_y, 0]
        a_fb_down = Line([5.6, ROW_Y, 0], fb_corner1, color=GRAY_MID, stroke_width=4)
        a_fb_toT = Arrow(fb_corner1, transducer[0].get_right(), buff=0.05, color=GRAY_MID, stroke_width=4)
        a_fb_fromT = Line(transducer[0].get_left(), [-4.4, fb_y, 0], color=GRAY_MID, stroke_width=4)
        a_fb_up = Arrow([-4.4, fb_y, 0], sj.get_bottom(), buff=0.03, color=GRAY_MID, stroke_width=4)
        l_fb = Text("ค่ามุมป้อนกลับ (Transduced Output)", font_size=15, color=GRAY_MID).next_to(transducer, DOWN, buff=0.12)

        # — build (ทยอยขึ้น ไม่ให้รก) —
        self.play(FadeIn(sum_node), FadeIn(controller), FadeIn(plant))
        self.play(GrowArrow(a_ref), FadeIn(l_ref))
        self.play(GrowArrow(a_err), FadeIn(l_err),
                  GrowArrow(a_ctrl), FadeIn(l_ctrl))
        self.play(GrowArrow(a_out), FadeIn(l_out))
        self.play(GrowArrow(a_dist), FadeIn(l_dist),
                  GrowArrow(a_noise), FadeIn(l_noise))
        self.play(Create(a_fb_down), Create(a_fb_toT), FadeIn(transducer))
        self.play(Create(a_fb_fromT), GrowArrow(a_fb_up), FadeIn(l_fb))
        self.wait(0.8)

        # ── A: animated dot วิ่งรอบ loop 1.5 รอบ ──
        dot = Dot(radius=0.13, color=YELLOW_HI).move_to([-6.4, ROW_Y, 0])
        self.add(dot)
        # waypoints ตามเส้น: ref → sj → ctrl → plant → out-corner → transducer → fb-up → sj
        path_pts = [
            [-6.4, ROW_Y, 0], sj.get_center(), controller[0].get_center(),
            plant[0].get_center(), [5.6, ROW_Y, 0], [5.6, fb_y, 0],
            transducer[0].get_center(), [-4.4, fb_y, 0], sj.get_center(),
        ]
        for i in range(len(path_pts) - 1):
            self.play(dot.animate.move_to(path_pts[i + 1]),
                      run_time=0.32, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)
        self.wait(0.6)
        self.wipe()

    # ── ตัวช่วยฉาก sim: หุ่น + กราฟ พร้อมกัน ──
    def run_sim_scene(self, title_txt, title_color, ts, ths, curve_color,
                      caption, run_time=3.0, y_max=95):
        title = self.title_top(title_txt, title_color)
        self.play(FadeIn(title))

        base = np.array([-4.3, -1.6, 0])
        tracker = ValueTracker(0)
        robot = always_redraw(
            lambda: make_robot(np.interp(tracker.get_value(), ts, ths), base,
                               body_color=curve_color)
        )
        ax = tilt_axes(x_max=ts[-1], y_max=y_max).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        x_lbl = Text("เวลา (s)", font_size=18, color=GRAY_MID).next_to(ax.x_axis, DOWN, buff=0.12)
        y_lbl = Text("มุม (°)", font_size=18, color=GRAY_MID).next_to(ax.y_axis, UP, buff=0.1)
        self.add(robot)
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl))

        moving_curve = always_redraw(
            lambda: traj_curve(
                ax,
                ts[ts <= tracker.get_value() + 1e-9],
                ths[: len(ts[ts <= tracker.get_value() + 1e-9])],
                curve_color,
            ) if tracker.get_value() > ts[1] else VMobject()
        )
        self.add(moving_curve)
        self.play(tracker.animate.set_value(ts[-1]), run_time=run_time, rate_func=linear)

        cap = Text(caption, font_size=26, color=title_color).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(1.0)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 4 — P = สปริง
    # ════════════════════════════════════════════════════════
    def s04_proportional(self):
        ts, ths = simulate(15, 4.0, kp=KP)   # P อย่างเดียว → แกว่ง
        self.run_sim_scene("P — เหมือน \"สปริง\"", BLUE_LIGHT, ts, ths, BLUE_LIGHT,
                           "ใช้ P อย่างเดียว → แกว่งไปมาไม่หยุด", run_time=4.0, y_max=40)

    # ════════════════════════════════════════════════════════
    # 5 — D = โช้คอัพ
    # ════════════════════════════════════════════════════════
    def s05_derivative(self):
        ts, ths = simulate(15, 4.0, kp=KP, kd=KD, disturb=2.0)  # P+D, มี bias
        self.run_sim_scene("P + D — เพิ่ม \"โช้คอัพ\"", ORANGE_HI, ts, ths, ORANGE_HI,
                           "แกว่งน้อยลง นิ่งเร็ว — แต่ยังค้างเล็กน้อย", run_time=4.0, y_max=40)

    # ════════════════════════════════════════════════════════
    # 6 — I = เก็บ error ค้าง
    # ════════════════════════════════════════════════════════
    def s06_integral(self):
        ts, ths = simulate(15, 4.0, kp=KP, kd=KD, ki=KI, disturb=2.0)  # PID เต็ม
        self.run_sim_scene("P + I + D — เก็บ error ค้าง", PURPLE_I, ts, ths, PURPLE_I,
                           "I กวาด error สะสม → กลับ 0° เป๊ะ", run_time=4.0, y_max=40)

    # ════════════════════════════════════════════════════════
    # 7 — การทดลอง: เปลี่ยนมุมเริ่มต้น PID เท่าเดิม
    # ════════════════════════════════════════════════════════
    def s07_vary_initial(self):
        title = self.title_top("PID ชุดเดิม — เปลี่ยนมุมเริ่มต้น", YELLOW_HI, size=34)
        sub = Text(f"Kp={KP:.0f}  Ki={KI:.0f}  Kd={KD:.0f}  (คงที่ทุกช่อง)",
                   font_size=22, color=GRAY_MID).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title), FadeIn(sub))

        # 5 ช่องซ้อนกัน: บนสุดมุมน้อย → ล่างสุดมุมมาก
        angles = [5, 15, 25, 35, 45]
        cols = [GREEN_OK, BLUE_LIGHT, YELLOW_HI, ORANGE_HI, RED_FALL]
        T = 4.0
        sims = [simulate(a, T, kp=KP, kd=KD, ki=KI) for a in angles]

        top_y = 1.55
        lane_h = 0.92
        tracker = ValueTracker(0)
        lanes = VGroup()
        robots = VGroup()
        for i, ((ts, ths), c, a) in enumerate(zip(sims, cols, angles)):
            cy = top_y - i * lane_h
            panel = RoundedRectangle(corner_radius=0.08, width=11.6, height=0.84,
                                     color=GRAY_DARK, stroke_width=1.5, stroke_opacity=0.55,
                                     fill_color=GRAY_DARK, fill_opacity=0.06).move_to([0.4, cy, 0])
            gy = cy - 0.34
            ground = Line([panel.get_left()[0] + 1.5, gy, 0],
                          [panel.get_right()[0] - 0.2, gy, 0],
                          color=GRAY_DARK, stroke_width=2)
            ang_lbl = Text(f"{a}°", font_size=24, color=c, weight=BOLD).move_to(
                [panel.get_left()[0] + 0.62, cy, 0])
            base = np.array([panel.get_left()[0] + 2.3, gy, 0])
            robots.add(always_redraw(
                lambda ts=ts, ths=ths, c=c, base=base:
                make_robot(np.interp(tracker.get_value(), ts, ths), base,
                           scale=0.32, body_color=c)))
            lanes.add(VGroup(panel, ground, ang_lbl))

        self.play(LaggedStart(*[FadeIn(l) for l in lanes], lag_ratio=0.12, run_time=1.2))
        self.add(robots)
        self.wait(0.4)
        self.play(tracker.animate.set_value(T), run_time=5.0, rate_func=linear)

        # ── B: settle-time markers (เส้นแนวตั้งในแต่ละช่องเมื่อหุ่นเข้า ±2°) ──
        settle_marks = VGroup()
        for i, ((ts_s, ths_s), c) in enumerate(zip(sims, cols)):
            settled = None
            for j in range(len(ts_s) - 1, -1, -1):
                if abs(ths_s[j]) > 2.0:
                    settled = ts_s[j + 1] if j + 1 < len(ts_s) else ts_s[-1]
                    break
            if settled is None:
                settled = ts_s[-1]
            cy = top_y - i * lane_h
            # x-position ในช่อง: จาก axle base ไปตาม ratio ของ panel width
            panel_left = lanes[i][0].get_left()[0] + 1.5   # เริ่มหลัง label
            panel_right = lanes[i][0].get_right()[0] - 0.2
            x_pct = settled / T
            x_pos = panel_left + x_pct * (panel_right - panel_left)
            mk = DashedLine([x_pos, cy + lane_h * 0.42, 0],
                            [x_pos, cy - lane_h * 0.42, 0],
                            color=c, stroke_width=3, dash_length=0.08)
            t_lbl = Text(f"{settled:.1f}s", font_size=14, color=c).next_to(mk, UP, buff=0.05)
            settle_marks.add(VGroup(mk, t_lbl))
        self.play(LaggedStart(*[FadeIn(m) for m in settle_marks], lag_ratio=0.15, run_time=1.2))

        cap = Text("มุมน้อย → กู้ไว   มุมมาก → แกว่งกว้าง ใช้เวลานานกว่า",
                   font_size=24, color=WHITE).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cap))
        self.wait(1.5)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 8 — สรุปบทบาท P-I-D
    # ════════════════════════════════════════════════════════
    def s08_summary_pid(self):
        title = self.title_top("สรุปบทบาท P · I · D", WHITE)
        self.play(FadeIn(title))
        rows = [
            ("P", "สปริง — ตอบสนองเร็วตามมุมปัจจุบัน", BLUE_LIGHT),
            ("I", "เก็บกวาด error สะสม — กำจัดมุมค้าง", PURPLE_I),
            ("D", "โช้คอัพ — กันแกว่ง/พุ่งเกิน", ORANGE_HI),
        ]
        cards = VGroup()
        for k, desc, c in rows:
            key = Text(k, font_size=46, color=c, weight=BOLD)
            box = Square(side_length=1.1, color=c, stroke_width=3).surround(key, buff=0.5)
            d = Text(desc, font_size=26, color=WHITE)
            row = VGroup(VGroup(box, key), d).arrange(RIGHT, buff=0.5)
            cards.add(row)
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(ORIGIN).shift(DOWN * 0.2)
        for row in cards:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(1.5)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 9 — ตั้งสมการ
    # ════════════════════════════════════════════════════════
    def s09_setup_eq(self):
        title = self.title_top("ตั้งสมการจากแรงจริง — แตกแรงโน้มถ่วง", GRAY_MID, size=34)
        self.play(FadeIn(title))

        # ── ลูกตุ้มกลับหัวฝั่งซ้าย (พระเอกของฉาก) ──
        pivot = np.array([-3.7, -1.9, 0])
        th = np.radians(30)
        L = 3.0
        r_dir = np.array([np.sin(th), np.cos(th), 0])          # ตามแกนคาน
        t_dir = np.array([np.cos(th), -np.sin(th), 0])         # ตั้งฉากคาน
        mass_pos = pivot + L * r_dir

        upref = DashedLine(pivot, pivot + UP * L, color=GRAY_DARK, stroke_width=2)
        rod = Line(pivot, mass_pos, color=BLUE_LIGHT, stroke_width=9)
        pivot_dot = Dot(pivot, radius=0.09, color=GRAY_MID)
        mass = Dot(mass_pos, radius=0.20, color=BLUE_LIGHT)
        arc = Arc(radius=0.85, start_angle=PI / 2, angle=-th, arc_center=pivot, color=YELLOW_HI, stroke_width=4)
        th_lbl = MathTex(r"\theta", color=YELLOW_HI, font_size=36).move_to(pivot + UP * 1.15 + RIGHT * 0.4)
        L_lbl = MathTex(r"L", color=GRAY_MID, font_size=30).move_to(pivot + 0.5 * L * r_dir + LEFT * 0.35 + UP * 0.1)

        scl = 1.7
        # แรงโน้มถ่วงเต็ม Mg (ลงตรงๆ)
        g_full = Arrow(mass_pos, mass_pos + DOWN * scl, color=WHITE, buff=0, stroke_width=6)
        g_lbl = MathTex(r"Mg", color=WHITE, font_size=34).next_to(g_full, DOWN, buff=0.08)
        # องค์ประกอบตามคาน (Mg cosθ) — ไม่ทำให้ล้ม
        comp_r = Arrow(mass_pos, mass_pos - np.cos(th) * scl * r_dir, color=GRAY_MID, buff=0, stroke_width=5)
        r_lbl = MathTex(r"Mg\cos\theta", color=GRAY_MID, font_size=26).next_to(comp_r.get_end(), LEFT, buff=0.1)
        # องค์ประกอบตั้งฉาก (Mg sinθ) — ตัวทำให้ล้ม
        comp_t = Arrow(mass_pos, mass_pos + np.sin(th) * scl * t_dir, color=RED_FALL, buff=0, stroke_width=6)
        t_lbl = MathTex(r"Mg\sin\theta", color=RED_FALL, font_size=28).next_to(comp_t.get_end(), RIGHT, buff=0.1)
        t_note = Text("→ ทำให้ล้ม", font_size=20, color=RED_FALL).next_to(t_lbl, DOWN, buff=0.1)

        self.play(Create(upref), Create(rod), FadeIn(pivot_dot), FadeIn(mass))
        self.play(Create(arc), Write(th_lbl), FadeIn(L_lbl))
        self.play(GrowArrow(g_full), Write(g_lbl))
        self.play(GrowArrow(comp_r), FadeIn(r_lbl))
        self.play(GrowArrow(comp_t), FadeIn(t_lbl), FadeIn(t_note))
        self.wait(0.6)

        # ── สมการฝั่งขวา ──
        l1 = MathTex(r"\sum \tau = J_{eq}\,\ddot{\theta}", font_size=40)
        l2 = MathTex(r"\tau_g = (Mg\sin\theta)\,L", color=RED_FALL, font_size=34)
        l3 = MathTex(r"\tau_m = u(t)", color=GREEN_OK, font_size=34)
        res = MathTex(r"(I+ML^2)\ddot{\theta} = MgL\sin\theta - u(t)", font_size=34)
        stack = VGroup(l1, l2, l3, Line(ORIGIN, RIGHT * 2.6, color=GRAY_DARK), res)
        stack.arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5).shift(UP * 0.1)
        self.play(Write(l1))
        self.play(FadeIn(l2, shift=UP * 0.15))
        self.play(FadeIn(l3, shift=UP * 0.15))
        self.play(Create(stack[3]), Write(res))
        self.wait(1.6)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 10 — Linearize
    # ════════════════════════════════════════════════════════
    def s10_linearize(self):
        title = self.title_top("ทำให้เป็นเชิงเส้น (มุมเล็ก)", YELLOW_HI)
        self.play(FadeIn(title))
        approx = MathTex(r"\sin\theta \approx \theta", color=YELLOW_HI, font_size=52)
        self.play(Write(approx))
        self.wait(0.8)
        self.play(approx.animate.scale(0.7).to_edge(UP, buff=1.4))
        lin = MathTex(r"(I+ML^2)\ddot{\theta} - MgL\,\theta = -u(t)", font_size=46)
        lin.move_to(ORIGIN)
        self.play(Write(lin))
        note = Text("ระบบเชิงเส้น — ออกแบบตัวควบคุมได้", font_size=26, color=GRAY_MID)
        note.next_to(lin, DOWN, buff=0.6)
        self.play(FadeIn(note))
        self.wait(1.5)
        self.wipe()

    # ════════════════════════════════════════════════════════
    # 11 — Transfer Function
    # ════════════════════════════════════════════════════════
    def s11_transfer(self):
        title = self.title_top("ฟังก์ชันถ่ายโอน (Transfer Function)", BLUE_LIGHT)
        self.play(FadeIn(title))
        tf = MathTex(r"G(s) = \frac{\Theta(s)}{U(s)} = \frac{-1}{(I+ML^2)s^2 - MgL}",
                     font_size=40)
        tf.to_edge(LEFT, buff=0.55).shift(UP * 1.1)
        self.play(Write(tf))
        self.wait(0.5)

        poles_eq = MathTex(r"s = \pm\sqrt{\dfrac{MgL}{I+ML^2}}", font_size=36)
        poles_eq.next_to(tf, DOWN, buff=0.7).align_to(tf, LEFT)
        self.play(Write(poles_eq))

        # ── ผัง s-plane ฝั่งขวา ──
        plane = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=3.6, y_length=3.6,
                     axis_config={"color": GRAY_MID, "stroke_width": 2, "include_tip": True,
                                  "tip_width": 0.12, "tip_height": 0.12}, tips=True
                     ).to_edge(RIGHT, buff=0.9).shift(DOWN * 0.1)
        re_lbl = MathTex(r"\mathrm{Re}", font_size=26, color=GRAY_MID).next_to(plane.x_axis, RIGHT, buff=0.1)
        im_lbl = MathTex(r"\mathrm{Im}", font_size=26, color=GRAY_MID).next_to(plane.y_axis, UP, buff=0.1)
        rhp = Rectangle(width=plane.x_length / 2, height=plane.y_length,
                        stroke_width=0, fill_color=RED_FALL, fill_opacity=0.12)
        rhp.move_to(plane.c2p(1, 0))
        pole_r = VGroup(Line(LEFT * 0.16, RIGHT * 0.16), Line(UP * 0.16, DOWN * 0.16)).set_color(RED_FALL).set_stroke(width=6).move_to(plane.c2p(1.3, 0))
        pole_l = VGroup(Line(LEFT * 0.16, RIGHT * 0.16), Line(UP * 0.16, DOWN * 0.16)).set_color(GRAY_MID).set_stroke(width=6).move_to(plane.c2p(-1.3, 0))
        rhp_lbl = Text("ฝั่งขวา = ไม่เสถียร", font_size=20, color=RED_FALL).next_to(plane, DOWN, buff=0.15)

        self.play(FadeIn(plane), FadeIn(re_lbl), FadeIn(im_lbl))
        self.play(FadeIn(rhp))
        self.play(Create(pole_l), Create(pole_r))
        self.play(FadeIn(rhp_lbl))
        self.wait(0.6)

        concl = Text("จึงต้องมี PID มาทำให้เสถียร", font_size=30, color=GREEN_OK)
        concl.to_edge(LEFT, buff=0.55).shift(DOWN * 1.7)
        self.play(FadeIn(concl))
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
