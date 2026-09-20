from mlib import *


def armature_cross_section(r_out, r_hub, n_poles, pole_width_frac, color):
    """หน้าตัดขวางแกน armature n ขา (สร้างในระนาบ XY ก่อน rotate เข้าแกนเพลาเอง
    ทีหลัง) รูขนาด r_hub*0.55 กลางรูปคือรูใส่เพลา"""
    pts = []
    for i in range(n_poles):
        a0, a1 = TAU * i / n_poles, TAU * (i + 1) / n_poles
        mid = (a0 + a1) / 2
        half = (a1 - a0) * pole_width_frac / 2
        for r, a in ((r_hub, a0), (r_hub, mid - half), (r_out, mid - half),
                     (r_out, mid + half), (r_hub, mid + half)):
            pts.append([r * np.cos(a), r * np.sin(a), 0])
    body = Polygon(*pts, color=color, fill_opacity=1, stroke_width=1.5,
                   stroke_color=WHITE)
    hole = Circle(radius=r_hub * 0.55, color=BLACK, fill_opacity=1, stroke_width=0)
    return VGroup(body, hole)


class DCMotor_ArmatureCommutator(SafeThreeDScene):
    """คลิปเดี่ยว (ไม่อยู่ในซีรีส์ที่ track) — อธิบายให้ Min ดูก่อนประดิษฐ์มอเตอร์ DC
    เล็กแบบ armature 3 ขา: เพลาเดียวร้อย armature core + commutator, commutator
    แต่ละชิ้นต่อกับจุดต่อระหว่างขดลวด 2 ขดที่ติดกัน, แปรงถ่านอยู่นิ่งกดสัมผัส
    ผิวนอกที่หมุน = กลไกสวิตช์ไฟ (commutation)

    ข้อเท็จจริงที่ verify แล้ว (WebSearch, 2026-09-20 — ดู electrical4u.com/
    construction-of-dc-motor, electronics-lab.com forum thread "3 pole dc motor
    with commutator", + วิดีโอจริง youtube.com/watch?v=W534EUoxJ5k "how to wind
    armature of 3 pole DC motor"):
      - armature core + commutator อัดแน่นบนเพลาเดียวกัน มุมสัมพัทธ์ต้อง fix
        เพราะกำหนดจังหวะสวิตช์ไฟ
      - ขดลวด 3 ขด ต่อเป็นห่วงปิดต่อเนื่อง (ปลายขด1=หัวขด2=ปลายขด2=หัวขด3=...)
      - จุดต่อระหว่างขดลวด 2 ขด อยู่ที่ "ช่องว่างระหว่างขา" (เยื้อง 60° จากขา)
        ตรงกับตำแหน่งชิ้น commutator แต่ละชิ้นเป๊ะ — จึงต่อเป็นเส้นตรงขนานเพลาได้
      - แปรงถ่าน (brush) อยู่นิ่งกับโครงมอเตอร์ ไม่หมุนตามเพลา
    """

    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-50 * DEGREES)

        SHAFT_LEN, SHAFT_R = 6.0, 0.09
        ARM_X, ARM_ROUT, ARM_RHUB = -1.0, 1.0, 0.15
        COM_X, COM_ROUT, COM_RIN = 0.55, 0.42, 0.16
        POLE_ANGLES = [0, 120, 240]
        SEG_ANGLES = [60, 180, 300]

        def pt(x, r, ang_deg):
            a = ang_deg * DEGREES
            return np.array([x, r * np.sin(a), -r * np.cos(a)])

        # ---------------------------------------------------------- title
        ttl = self.hud(title("Armature 3 ขา ต่อกับ Commutator ยังไง", size=27))
        self.play(FadeIn(ttl, shift=UP * 0.3), run_time=0.6)
        self.wait(0.5)

        step_cap = [None]

        def set_step(txt):
            new = self.hud(caption_top(txt, size=21, max_w=12.5))
            anims = [FadeIn(new, shift=UP * 0.2)]
            if step_cap[0] is not None:
                anims.append(FadeOut(step_cap[0]))
            self.play(*anims, run_time=0.5)
            step_cap[0] = new

        # ---------------------------------------------------- step 1: shaft
        set_step("1) เพลา (shaft) — แกนกลางที่ทุกชิ้นร้อยผ่าน")
        shaft = Cylinder(radius=SHAFT_R, height=SHAFT_LEN, direction=RIGHT,
                         fill_color=METAL, fill_opacity=1, stroke_width=0,
                         checkerboard_colors=False, resolution=(16, 16))
        self.play(FadeIn(shaft), run_time=0.8)
        self.wait(1.0)

        # ------------------------------------------------ step 2: armature
        set_step("2) แกน armature 3 ขา (เหล็กลามิเนตอัดซ้อน) อัดแน่นเข้ากับเพลา")
        stack_xs = np.linspace(ARM_X - 0.22, ARM_X + 0.22, 5)
        arm_pieces = VGroup(*[
            armature_cross_section(ARM_ROUT, ARM_RHUB, 3, 0.55, METAL)
            .rotate(PI / 2, axis=UP, about_point=ORIGIN).shift(RIGHT * x)
            for x in stack_xs
        ])
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in arm_pieces],
                              lag_ratio=0.15), run_time=1.4)
        self.wait(0.8)

        # ---------------------------------------------------- step 3: coils
        set_step("3) ขดลวด 3 ขด พันรอบขาละ 1 ขด ต่อกันเป็นห่วงต่อเนื่อง (ไม่มีปลายลอย)")
        coil_r = ARM_ROUT * 0.62
        names = ["A", "B", "C"]
        coils = VGroup(*[
            Circle(radius=0.16, color=CURRENT, fill_opacity=0.85, stroke_width=2)
            .move_to(pt(ARM_X, coil_r, ang))
            for ang in POLE_ANGLES
        ])
        self.play(*[FadeIn(c, scale=0.4) for c in coils], run_time=0.8)
        coil_labels = VGroup()
        for name, ang in zip(names, POLE_ANGLES):
            lbl = Text(name, font_size=16, color=WHITE).move_to(pt(ARM_X, coil_r, ang))
            self.world_text(lbl)
            coil_labels.add(lbl)
        self.play(FadeIn(coil_labels), run_time=0.4)
        self.wait(1.2)

        # ------------------------------------------------ step 4: commutator
        set_step("4) Commutator 3 ชิ้น อัดเข้าเพลาเดียวกัน — เยื้อง 60° จากขา (อยู่ตรงช่องว่าง)")
        seg_span = 90 * DEGREES
        segs = VGroup()
        for ang in SEG_ANGLES:
            s = AnnularSector(inner_radius=COM_RIN, outer_radius=COM_ROUT,
                              angle=seg_span, start_angle=(ang - 45) * DEGREES,
                              color=METAL, fill_opacity=1, stroke_width=1.5)
            s.rotate(PI / 2, axis=UP, about_point=ORIGIN)
            s.shift(RIGHT * COM_X)
            segs.add(s)
        self.play(*[FadeIn(s, shift=RIGHT * 0.3) for s in segs], run_time=0.9)
        self.wait(1.0)

        # --------------------------------------------------- step 5: wiring
        set_step("5) จุดต่อขดลวดคู่ติดกัน (ตรงช่องว่างระหว่างขา) บัดกรีเข้า commutator ชิ้นมุมเดียวกัน")
        wires, junction_dots = VGroup(), VGroup()
        for ang in SEG_ANGLES:
            j_pt = pt(ARM_X + 0.22, ARM_ROUT * 0.98, ang)
            s_pt = pt(COM_X, COM_ROUT * 0.98, ang)
            junction_dots.add(Dot(j_pt, radius=0.05, color=CURRENT))
            wires.add(Line(j_pt, s_pt, color=CURRENT, stroke_width=3))
        self.play(FadeIn(junction_dots), run_time=0.4)
        self.play(LaggedStart(*[Create(w) for w in wires], lag_ratio=0.25),
                  run_time=1.2)
        self.wait(1.2)

        # -------------------------------------------------- step 6: brushes
        set_step("6) แปรงถ่าน 2 อัน กดสัมผัสผิว commutator จากภายนอก (อยู่นิ่ง ไม่หมุนตามเพลา)")
        b_top = Rectangle(width=0.30, height=0.12, color=GRAYTXT,
                          fill_opacity=1, stroke_width=1)
        b_top.move_to(pt(COM_X, COM_ROUT + 0.12, 90))
        b_bot = b_top.copy().move_to(pt(COM_X, COM_ROUT + 0.12, 270))
        lead_p = Line(b_top.get_center(), b_top.get_center() + UP * 0.9,
                      color=EMF, stroke_width=3)
        lead_m = Line(b_bot.get_center(), b_bot.get_center() + DOWN * 0.9,
                      color=EMF, stroke_width=3)
        self.play(FadeIn(b_top, b_bot), Create(lead_p), Create(lead_m), run_time=1.0)
        legend = self.hud(Text("แปรงถ่าน 2 อัน = ขั้ว + และ − จากไฟภายนอก",
                               font_size=18, color=GRAYTXT).move_to([0, -3.15, 0]))
        self.play(FadeIn(legend), run_time=0.4)
        self.wait(1.4)
        self.play(FadeOut(legend), run_time=0.3)

        # ---------------------------------------------- step 7: rotate demo
        set_step("7) เพลาหมุน → commutator เลื่อนผ่านแปรงถ่าน = สลับขดที่ต่อไฟ (commutation)")
        assembly = VGroup(shaft, arm_pieces, coils, coil_labels, segs, wires,
                          junction_dots)
        self.play(Rotating(assembly, angle=2 * TAU, axis=RIGHT, about_point=ORIGIN,
                           run_time=6, rate_func=linear))
        self.wait(0.5)

        # -------------------------------------------------------- summary
        self.fade_out_all()
        summary = self.hud(VGroup(
            title("สรุปการต่อ", color=OK, size=27),
            fit_width(Text("เพลาเดียวร้อย armature + commutator ให้มุมล็อกกัน (ห้ามคลาดเคลื่อน)",
                font_size=21), 12.5).shift(UP * 0.55),
            fit_width(Text("commutator แต่ละชิ้น = จุดต่อระหว่างขดลวด 2 ขดที่ติดกัน",
                font_size=21), 12.5),
            fit_width(Text("แปรงถ่านอยู่นิ่ง กดผิวนอกที่หมุน = สวิตช์ไฟอัตโนมัติตามมุมเพลา",
                font_size=21), 12.5).shift(DOWN * 0.55),
        ))
        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.6)
        self.wait(2.2)
        self.fade_out_all()
