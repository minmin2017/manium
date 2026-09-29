"""involute_geom.py -- เรขาคณิตเฟืองอินโวลูทจริง (numpy ล้วน ไม่พึ่ง manim ทดสอบได้เร็ว)

ใช้กับ G20B_MeshingTeeth ใน spur_gears.py (2026-09-29, Min อยากเห็น "เนื้อฟัน" ขบกันจริง)
- gear_outline(): โครงฟันทั้งเฟือง (ฟันซี่ 0 อยู่กึ่งกลางที่มุม 0)
- mesh_frame(): เฟือง 1 (ขับ, ซ้าย) กับ 2 (ตาม, ขวา) เส้นศูนย์กลางแนวนอน; จุดเริ่มสัมผัส A ที่ theta=0
  เฟือง 1 หมุนทวนเข็ม theta (rad) เฟือง 2 หมุนตามเข็ม theta*Rb1/Rb2 (กลิ้งแบบ base circle)
  จุดสัมผัสอยู่ที่ E1 + rho(theta)*d บน line of action โดย rho = rho_A + Rb1*theta
พิสูจน์ด้วยตัวเลข: `python involute_geom.py` เช็คว่าจุดสัมผัสอยู่บนผิวฟันทั้งสองเฟืองทุก theta
"""
import numpy as np


def inv(a):
    return np.tan(a) - a


def gear_outline(N, m, phi, nf=24, nt=4, nr=6):
    R = N * m / 2.0
    Rb, Ra, Rd = R * np.cos(phi), R + m, R - 1.25 * m
    db = np.pi / (2 * N) + inv(phi)                      # ครึ่งมุมฟันที่ base circle

    def half(r):                                          # ครึ่งมุมฟันที่รัศมี r (r >= Rb)
        return db - inv(np.arccos(min(1.0, Rb / r)))

    def P(r, a):
        return (r * np.cos(a), r * np.sin(a))

    rs = np.linspace(Rb, Ra, nf)
    pts = []
    for k in range(N):
        a = 2 * np.pi * k / N
        pts.append(P(Rd, a - db))                         # โคนฟัน -> ขึ้นเส้นรัศมีถึง base circle
        for r in rs:                                      # ผิวอินโวลูทด้านมุมน้อย ขึ้นไปยอดฟัน
            pts.append(P(r, a - half(r)))
        for t in np.linspace(-1, 1, nt)[1:-1]:            # ยอดฟัน (top land) เป็นส่วนโค้งบน addendum circle
            pts.append(P(Ra, a + t * half(Ra)))
        for r in rs[::-1]:                                # ผิวอินโวลูทด้านมุมมาก ลงมา base circle
            pts.append(P(r, a + half(r)))
        pts.append(P(Rd, a + db))                         # ลงเส้นรัศมีถึงโคนฟัน
        a_next = 2 * np.pi * (k + 1) / N - db
        for t in np.linspace(0, 1, nr)[1:-1]:             # ก้นร่องระหว่างฟัน (root arc)
            pts.append(P(Rd, a + db + t * (a_next - (a + db))))
    return np.array(pts), dict(R=R, Rb=Rb, Ra=Ra, Rd=Rd, db=db)


def mesh_frame(N1, N2, m, phi, P0=(0.0, 0.0)):
    P0 = np.array([P0[0], P0[1]], float)
    R1, R2 = N1 * m / 2.0, N2 * m / 2.0
    Rb1, Rb2 = R1 * np.cos(phi), R2 * np.cos(phi)
    Ra1, Ra2 = R1 + m, R2 + m
    db1 = np.pi / (2 * N1) + inv(phi)
    db2 = np.pi / (2 * N2) + inv(phi)
    d = np.array([np.sin(phi), np.cos(phi)])              # ทิศ E1 -> E2 (ขึ้นขวา)
    O1, O2 = P0 + [-R1, 0.0], P0 + [R2, 0.0]
    E1, E2 = P0 - R1 * np.sin(phi) * d, P0 + R2 * np.sin(phi) * d
    E1E2 = float(np.linalg.norm(E2 - E1))
    E1B = float(np.sqrt(Ra1 ** 2 - Rb1 ** 2))
    E2A = float(np.sqrt(Ra2 ** 2 - Rb2 ** 2))
    rho_A = E1E2 - E2A                                    # ระยะ E1 -> A
    rho_B = E1B
    A, B = E1 + rho_A * d, E1 + rho_B * d
    ang = lambda v: float(np.arctan2(v[1], v[0]))
    e1, e2 = ang(E1 - O1), ang(E2 - O2)
    alpha1 = rho_A / Rb1 + e1 - db1                        # มุมกึ่งกลางฟันซี่ 0 เฟือง 1 ที่ theta=0
    alpha2 = e2 - db2 + E2A / Rb2                          # เฟือง 2 (หมุนตามเข็มเมื่อ theta เพิ่ม)
    return dict(N1=N1, N2=N2, m=m, phi=phi, R1=R1, R2=R2, Rb1=Rb1, Rb2=Rb2, Ra1=Ra1, Ra2=Ra2,
                Rd1=R1 - 1.25 * m, Rd2=R2 - 1.25 * m, d=d, P=P0, O1=O1, O2=O2, E1=E1, E2=E2,
                A=A, B=B, E1E2=E1E2, E1B=E1B, E2A=E2A, rho_A=rho_A, rho_B=rho_B,
                E1P=float(np.dot(P0 - E1, d)), Z=E1B + E2A - E1E2,
                alpha1=alpha1, alpha2=alpha2, ratio=Rb1 / Rb2,
                theta_P=(float(np.dot(P0 - E1, d)) - rho_A) / Rb1,
                theta_B=(rho_B - rho_A) / Rb1)


def placed(pts, O, alpha):                                 # โครงฟันที่หมุน alpha รอบ O
    c, s = np.cos(alpha), np.sin(alpha)
    return np.column_stack([O[0] + pts[:, 0] * c - pts[:, 1] * s, O[1] + pts[:, 0] * s + pts[:, 1] * c])


def contact_point(fr, theta):
    return fr["E1"] + (fr["rho_A"] + fr["Rb1"] * theta) * fr["d"]


def check(fr, o1, o2, thetas=(0.0, None, None), tol=0.03):
    """จุดสัมผัสต้องอยู่บนผิวฟันทั้งสองเฟืองที่ทุก theta (ระยะถึงจุดยอดโครงฟันที่ใกล้สุด < tol)"""
    out = []
    for th in (0.0, fr["theta_P"], fr["theta_B"], fr["theta_B"] * 0.5):
        g1 = placed(o1, fr["O1"], fr["alpha1"] + th)
        g2 = placed(o2, fr["O2"], fr["alpha2"] - th * fr["ratio"])
        c = contact_point(fr, th)
        d1 = float(np.min(np.linalg.norm(g1 - c, axis=1)))
        d2 = float(np.min(np.linalg.norm(g2 - c, axis=1)))
        out.append((round(th, 3), round(d1, 4), round(d2, 4)))
        assert d1 < tol and d2 < tol, (th, d1, d2)
    return out


if __name__ == "__main__":
    phi = np.deg2rad(20.0)
    m = 2.0 / 9.0                                          # R = 2.0 หน่วยฉากที่ N=18
    fr = mesh_frame(18, 18, m, phi, (0.0, 0.0))
    o1, _ = gear_outline(18, m, phi)
    o2, _ = gear_outline(18, m, phi)
    print("Z =", round(fr["Z"], 4), " E1A =", round(fr["rho_A"], 4), " E1B =", round(fr["E1B"], 4),
          " theta_B(deg) =", round(np.degrees(fr["theta_B"]), 2))
    print("contact-on-both-flanks check (theta, d1, d2):", check(fr, o1, o2))
    print("OK")
