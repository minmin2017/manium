# คู่มือโปรเจกต์ Animation 1Brown3Blue (Manim)

> โปรเจกต์นี้ใช้ทำวิดีโออนิเมชั่นคณิตศาสตร์แบบ 3Blue1Brown ด้วยไลบรารี Manim

---

## โครงสร้างโปรเจกต์

```
animation_1brown3blue/
├── manim/                  # manimgl (เวอร์ชัน 3b1b) — ติดตั้งแล้ว
├── manim-community/        # manim community edition — ติดตั้งแล้ว
├── videos/                 # ซอร์สโค้ดคลิปจริงของ 3Blue1Brown (ปี 2015-2026)
│   ├── _2019/clacks/       # กล่องชนกันคำนวณ π
│   ├── _2019/windmill.py   # โจทย์ IMO windmill
│   ├── _2023/convolutions2/
│   ├── _2026/hairy_ball/   # ทฤษฎีบทลูกบอลขนยุ่ง
│   └── ...                 # ครบทุกปี
├── *.py                    # ไฟล์ Min ทำเอง
│   ├── ck40b_overview.py   # เครื่อง CK40B (เรนเดอร์แล้ว)
│   ├── healthspan.py       # กราฟสุขภาพ (เรนเดอร์แล้ว)
│   └── breakfast_slide.py  # สไลด์กินข้าวเช้า (เรนเดอร์แล้ว)
└── media/videos/           # วิดีโอที่เรนเดอร์ออกมาแล้ว
```

---

## การติดตั้งที่ทำไปแล้ว (Ubuntu)

```bash
# manimgl (3b1b version)
pip install -e ~/Desktop/animation_1brown3blue/manim/

# LaTeX สำหรับวาดสมการ
sudo apt install texlive-latex-base texlive-fonts-recommended \
                 texlive-latex-extra texlive-fonts-extra \
                 texlive-science dvisvgm

# Python deps
pip install pywavefront
pip install "numpy<2"   # ต้อง <2 เพราะ manimgl ไม่รองรับ numpy 2.x
```

---

## วิธีใช้งาน (สร้างคลิป)

### เขียนไฟล์ Python ก่อน เช่น `my_scene.py`:
```python
from manimlib import *   # ใช้กับ manimgl (3b1b)
# หรือ
from manim import *      # ใช้กับ manim community

class MyScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.5)
        self.play(Create(circle))
        self.wait()
```

### เรนเดอร์เป็นวิดีโอ:
```bash
# manimgl (ต้องรันจากโฟลเดอร์ที่มีไฟล์)
manimgl my_scene.py MyScene -w          # คุณภาพสูง (1080p)
manimgl my_scene.py MyScene -w -l       # low quality (480p) เช็คเร็ว

# manim community
manim my_scene.py MyScene               # คุณภาพสูง
manim my_scene.py MyScene -ql           # low quality

# ดูตัวอย่างในเครื่อง:
vlc media/videos/MyScene/480p15/MyScene.mp4
```

### รันโค้ดจาก videos/ (คลิปจริงของ 3b1b):
```bash
cd ~/Desktop/animation_1brown3blue/videos
export PYTHONPATH="$(pwd)"
manimgl _2025/zeta/*.py <SceneName> -w -l
```

> **หมายเหตุ:** โค้ดเก่า (ก่อนปี 2022) บางไฟล์อาจพัง เพราะใช้ API รุ่นเก่า เช่น `MovingCameraScene`

---

## ฟีเจอร์ที่ทำได้

| ฟีเจอร์ | วิธีทำ |
|--------|--------|
| วาดรูปทรงเรขาคณิต | `Circle()`, `Square()`, `Triangle()`, `Line()` |
| เขียนสมการ LaTeX | `MathTex(r"\int e^x dx")` / `Tex("คำอธิบาย")` |
| กราฟ + แกน | `Axes()`, `NumberPlane()`, `FunctionGraph()` |
| แอนิเมต | `Create()`, `Write()`, `Transform()`, `FadeIn()`, `FadeOut()` |
| กล้องเคลื่อนที่ | `self.camera.frame.animate.move_to(...)` |
| 3D | สืบทอดจาก `ThreeDScene` |
| ข้อความ | `Text("สวัสดี")` (ไม่ต้อง LaTeX) |
| ตัวเลขนับ | `Integer()`, `DecimalNumber()` |
| อัปเดต real-time | `always_redraw()`, `ValueTracker()` |

---

## ตัวอย่างสิ่งที่ Min ทำไว้แล้ว

| ไฟล์ | เนื้อหา | ความยาว |
|------|---------|---------|
| `healthspan.py` | กราฟสุขภาพ 3 เส้น (แย่/ปานกลาง/ดี) ตามอายุ 20-90 ปี | 68 วิ |
| `ck40b_overview.py` | อนิเมชั่นอธิบายเครื่อง CK40B green/red zone | 49 วิ |
| `breakfast_slide.py` | สไลด์เรื่องกินข้าวเช้า + รูปประกอบ | ~60 วิ |
| `example1.py` | ตัวอย่างพื้นฐาน 3 ฉาก | 5 วิ/ฉาก |

---

---

## ก่อนสร้างวิดีโอของตัวเอง — อ่าน Knowledge Graph ก่อน

โปรเจกต์นี้มี knowledge graph สร้างไว้แล้วที่ `graphify-out/graph.json`  
(11,541 nodes · 25,187 edges ครอบคลุมทั้ง manim lib + scripts)

**วิธีใช้:** ถาม Claude ว่า "อ่าน graphify แล้วบอกว่าฉากแบบ X ใช้เทคนิคอะไร"  
Claude จะอ่าน graph แทนการเปิดไฟล์ทีละไฟล์ → ประหยัดโทเค็นมาก

**ทำไมต้องอ่าน graph ก่อน:**  
สคริปต์แต่ละปีใช้เทคนิคไม่เหมือนกัน — ถ้ารู้ก่อนจะเลือกเครื่องมือได้ถูกต้อง:

| ปี / ซีรีส์ | เทคนิคเด่น | คลาสที่ใช้ |
|------------|-----------|-----------|
| 2019 clacks (กล่องชนกัน) | Physics sim + real-time update | `add_updater`, `ValueTracker`, `add_sound` |
| 2019 bayes | Interactive diagram + probability bars | `ValueTracker`, `Brace`, `Rectangle` resize |
| 2019 diffyq | Vector field + phase space + pendulum ODE | `VectorField`, `ParametricCurve`, `TeacherStudentsScene` |
| 2019 spirals | Polar coordinates + dot patterns | `Axes`, `add_updater`, `ParametricCurve` |
| 2019 windmill | Geometry proof + camera pan | `MovingCameraScene`, `LaggedStart`, `ReplacementTransform` |
| 2019 hyperdarts | Probability + sound effects | `MovingCameraScene`, `add_sound`, `NumberPlane` |
| 2026 spheres_talk | 3D geometry + interactive | `InteractiveScene`, `MathTex`, LaTeX สมการ |

**Community หลักใน graph:**
- `Geometry & Shapes` — วาดรูปทรงพื้นฐาน
- `Animation Engine` — ระบบ animate/play
- `Coordinate Systems & Axes` — แกน + กราฟ
- `Rotation & Transform` — หมุน/แปลง object
- `Config & TeX Templates` — ตั้งค่า LaTeX

**คำสั่งถาม Claude:** `/graphify อ่านจาก graphify-out/graph.json แล้วบอกว่าจะวาด spiral จากจำนวนเฉพาะต้องใช้คลาสอะไรบ้าง`

---

## ใส่รูปภาพจากอินเทอร์เน็ต

Manim ไม่โหลด URL ตรงๆ — ต้องดาวน์โหลดก่อน แล้วค่อยใช้ `ImageMobject`:

```python
import urllib.request
from manimlib import *

class SceneWithImage(Scene):
    def construct(self):
        # ดาวน์โหลดรูปก่อน
        urllib.request.urlretrieve("https://example.com/image.png", "image.png")

        # ใส่รูปใน scene
        img = ImageMobject("image.png")
        img.scale(2)
        self.play(FadeIn(img))
        self.wait()
```

**สิ่งที่ทำได้กับรูป:**

| การกระทำ | โค้ด |
|---------|------|
| ย่อ/ขยาย | `img.scale(2)` |
| เลื่อนตำแหน่ง | `img.move_to(LEFT * 3)` |
| fade เข้า/ออก | `FadeIn(img)` / `FadeOut(img)` |
| หมุน | `img.rotate(PI/4)` |
| วางซ้อน text | `VGroup(img, Text("caption"))` |

> **Tip:** เก็บรูปไว้ใน folder `assets/` จะได้ไม่ต้องดาวน์โหลดทุกครั้ง

---

## Tips

- **ทดสอบเร็ว:** ใช้ `-l` (low quality 480p) ก่อนเสมอ ก่อนเรนเดอร์ `-w` จริง
- **Token ประหยัด:** Claude เขียน/แก้ไขไฟล์ .py → Manim เรนเดอร์บนเครื่อง (ไม่กิน token)
- **LaTeX slow:** ครั้งแรกช้าเพราะ compile TeX → ครั้งถัดไปมี cache เร็วขึ้น
- **videos/ เป็น reference:** ดูวิธีทำฉากซับซ้อนจากโค้ดจริงของ Grant Sanderson ได้เลย
