# DOUBLE_SLIT_EXECUTION_BRIEF.md
## Master Execution Brief & Storyboard: Young's Double-Slit Wave Interference (3D Manim)

---

### 1. Resource Inventory & Constraints
- **Target Worktree:** `C:\Users\wicha\Desktop\manium-double-slit`
- **Branch:** `codex/double-slit-3d-lesson`
- **Target Audience:** Zero-prerequisite learners (ผู้เรียนพื้นฐานศูนย์).
- **Presentation Paradigm:** Narration-led Hybrid (Physical 3D/2D model establishes ground truth $\rightarrow$ fixed 2D dashboard/equations confirm).
- **Render Environment:** GitHub Actions Cloud Render (`render_manim.yml`), Ubuntu Container (`manimcommunity/manim:latest`), `MANIM_THAI_FONT: Loma`.
- **Code Constraints:**
  - `from mlib import *` using `SafeScene` and `SafeThreeDScene`.
  - All Thai text via `Text("...", font=THAI_FONT)` or default font (Loma on cloud, Leelawadee UI on Windows).
  - All formulas in `MathTex` ASCII only — strictly no Thai characters inside `MathTex`/`Tex`.
  - No `Arrow3D`, no dense 3D `Surface` meshes, no imported OBJ, no uncontrolled `wave_field_dots`. Flat `arrow3()` and `line3()` for 3D vectors.
  - Top captions (`caption_top()`), fixed HUD in 3D (`self.hud()`).
  - No ambient camera movement during key proofs.

---

### 2. Settled Source Ledger (Official Physics References)
1. **OpenStax College Physics 17.1 (Understanding Diffraction and Interference):**
   - Wave superposition principle, constructive/destructive interference, path difference.
2. **OpenStax University Physics Vol. 3 Chapter 3.2 (Mathematics of Interference):**
   - Exact angular intensity: $I(\theta) = 4I_0 \cos^2\left(\frac{\pi d\sin\theta}{\lambda}\right)$.
   - Far-field condition: $L \gg d$, path difference $\Delta r \approx d\sin\theta$.
   - Maxima: $d\sin\theta = m\lambda$; Minima: $d\sin\theta = (m + \frac{1}{2})\lambda$.
   - Small-angle approximation: $\sin\theta \approx \tan\theta \approx \frac{y}{L}$, yielding $y_m \approx m\frac{\lambda L}{d}$ and $\Delta y \approx \frac{\lambda L}{d}$.
   - Small-angle intensity approximation: $I(y) \approx 4I_0 \cos^2\left(\frac{\pi d y}{\lambda L}\right)$ (labeled with $\approx$).
3. **OpenStax University Physics Vol. 3 Chapter 4.3 (Double-Slit Diffraction):**
   - Combined real pattern: $I_{\text{real}}(\theta) = 4I_0 \cos^2\left(\frac{\pi d\sin\theta}{\lambda}\right) \cdot \left(\frac{\sin\beta}{\beta}\right)^2$, where $\beta = \frac{\pi a\sin\theta}{\lambda}$.
   - Distinction between $d$ (center-to-center slit spacing) and $a$ (individual slit width).
4. **MIT OCW 8.02 Physics II (Experiment Notes: Two-Slit Interference):**
   - Coherence requirement from a single incident front; spatial redistribution of radiant energy without destruction.

---

### 3. Detailed Timestamped Storyboard & Proving Shot Log

#### Module 1: `double_slit_01_intro_wave.py`
##### Beat 1: `DS01_ParadoxHook` (~25s)
- **Time:** 00:00 – 00:25
- **Camera & Framing:** 3/4 Isometric 3D View (`phi=68*DEGREES, theta=-55*DEGREES`), locked after a brief 3s establishing pan.
- **Narration Claim:** "ถ้าคลื่นแสงเคลื่อนที่ผ่านช่องเปิด 2 ช่องบนแผ่นกั้น... เราอาจคาดเดาว่าจะเห็นเพียงแถบสว่าง 2 แถบบนฉากด้านหลัง แต่เหตุใดผลการทดลองจริงจึงปรากฏริ้วสว่างและมืดสลับกันหลายแถบ? แสงมาเจอกันแล้วกลายเป็นความมืดได้อย่างไร?"
- **Physical Model Event:** Plane wavefronts travel from source and illuminate two slits. On the screen, an alternating multi-fringe pattern emerges.
- **Dashboard / HUD:** Question banner top: "แสง + แสง = ความมืด?" with pointers to the two slits and the screen fringes.
- **Visible Proof:** Center of screen has alternating bright/dark bands while both slits remain visibly open and emitting.
- **Transition Link:** Camera pushes smoothly forward, zooming straight into the first dark stripe ($m=0.5$), transitioning without blackout into the wave interior.

##### Beat 2: `DS02_Wave101` (~65s)
- **Time:** 00:25 – 01:30
- **Camera & Framing:** 2D Orthographic Side-View, locked 100%.
- **Narration Claim:** "เพื่อไขปริศนานี้ เราต้องเข้าใจธรรมชาติของคลื่น เส้นโค้งนี้แทนการกระจัดหรือแอมพลิจูดของสนามคลื่น ไม่ใช่อนุภาควิ่งตามเส้น จุดสูงสุดคือสันคลื่น และจุดต่ำสุดคือท้องคลื่น ระยะห่างระหว่างสันคือความยาวคลื่น $\lambda$ และเมื่อสองคลื่นมาถึงจุดเดียวกัน: สันชนสันจะเสริมกันเป็นสองเท่า แต่ถ้าสันมาพบกับท้องพอดี ทั้งสองจะหักล้างกันจนนิ่งสนิท"
- **Physical Model Event:** Single wave rail with moving sine wave. Crest, trough, and $\lambda$ brace labeled. Then two identical waves travel toward a probe. First, in-phase: crests arrive simultaneously $\rightarrow$ probe oscillates with doubled amplitude ($2A$). Second, the lower wave shifts by half a cycle ($\lambda/2$): crest meets trough at the probe $\rightarrow$ probe stays completely stationary at zero.
- **Dashboard / HUD:** Phase dial (นาฬิกาเฟส) showing 0 vs 180° (half-cycle shift), equation $y_{\text{sum}} = y_1 + y_2$.
- **Visible Proof:** Physical probe marker visibly doubles in excursion under constructive interference and freezes completely at $0$ under destructive interference.
- **Transition Link:** Probe shifts from abstract 1D rail to the real observation point on the double-slit screen.

---

#### Module 2: `double_slit_02_apparatus_paths.py`
##### Beat 3: `DS03_ApparatusCoherence` (~65s)
- **Time:** 01:30 – 02:35
- **Camera & Framing:** 3/4 Perspective establish (8s) $\rightarrow$ Smooth transition to locked Top-Down Orthographic View.
- **Narration Claim:** "นี่คือแท่นทดลองในอุดมคติ: แหล่งกำเนิดแสงเดี่ยว, แผ่นกั้นที่มีช่องสลิตแคบมากสองช่อง $S_1$ และ $S_2$ ห่างกันระยะ $d$, และฉากรับภาพที่ระยะ $L$ แหล่งกำเนิดเดี่ยวรับประกันว่าคลื่นที่ออกจากสองช่องจะเริ่มก้าวพร้อมกันทุกประการ หรือเป็น 'คลื่นอาพันธ์'"
- **Physical Model Event:** 3D barrier with two physical apertures. Plane wave arrives at the barrier. Only after the incident wave reaches the apertures do secondary circular wavefronts begin expanding from $S_1$ and $S_2$.
- **Dashboard / HUD:** Pointers with labels: "แหล่งกำเนิด (Source)", "แผ่นกั้น (Barrier)", "ช่องสลิต $S_1, S_2$", "ระยะห่าง $d$", "ฉากรับภาพ (Screen)", "ระยะฉาก $L$". Synchronized phase clocks at $S_1$ and $S_2$.
- **Visible Proof:** No outgoing waves exist behind the barrier until the incident front hits $S_1$ and $S_2$; circular wave radii from both slits expand in exact lockstep.
- **Transition Link:** Two light rays extend from $S_1$ and $S_2$ to an arbitrary observation point $P$ on the screen.

##### Beat 4: `DS04_PointPInvestigation` (~100s)
- **Time:** 02:35 – 04:15
- **Camera & Framing:** Full-screen locked Top-Down View for the first 60s (no insets to prevent split attention). Front-on screen inset opens only for the sweeping build.
- **Narration Claim:** "เราเลือกสังเกตที่จุด $P$ ใดๆ แสงเดินทางจากแต่ละช่องเป็นระยะ $r_1$ และ $r_2$ ที่กึ่งกลางฉาก ระยะทางเท่ากันพอดี $r_1 = r_2$ สันชนสันเกิดแถบสว่างกลาง แต่เมื่อเลื่อน $P$ ขึ้นไป ช่องล่างต้องเดินทางไกลกว่า เมื่อส่วนต่างทางเดินยาวเท่ากับครึ่งความยาวคลื่น สันจะชนท้อง หักล้างกันเกิดแถบมืดแรก!"
- **Physical Model Event:** `ValueTracker` controls point $P$.
  - At $y=0$: $r_1 = r_2$, traveling wave packets arrive in-phase at the same frame $\rightarrow$ point $P$ flashes bright green/white.
  - At $y=y_{\text{dark}}$: $r_2 - r_1 = \lambda/2$, blue packet crest arrives alongside orange packet trough at the exact same frame $\rightarrow$ point $P$ turns completely dark.
- **Dashboard / HUD:** Live path ruler showing $r_1$, $r_2$, and $\Delta r = |r_2 - r_1|$. Live phase dial. Once both states are demonstrated, front-screen inset opens and $P$ sweeps continuously, depositing intensity into the $I(y)$ profile.
- **Visible Proof:** Blue crest and orange trough literally meet at point $P$ in the exact same video frame, and the resulting field amplitude sums to zero.
- **Transition Link:** Freeze the geometry at point $P$ and prepare to derive the universal geometric relationship.

---

#### Module 3: `double_slit_03_geometry_spacing.py`
##### Beat 5: `DS05_GeometryDerivation` (~90s)
- **Time:** 04:15 – 05:45
- **Camera & Framing:** Locked Top-Down View; camera zooms in on the two slits $S_1, S_2$ and freezes completely before explanation.
- **Narration Claim:** "เนื่องจากระยะฉาก $L$ อยู่ไกลกว่าระยะห่างสลิต $d$ อย่างมหาศาล รังสีทั้งสองจึงเดินทางแทบจะขนานกันทำมุม $\theta$ เมื่อลากเส้นตั้งฉากจาก $S_1$ ไปยังรังสีที่สอง จะเกิดสามเหลี่ยมมุมฉากจิ๋ว โดยมีผลต่างทางเดินประมาณ $d\sin\theta$ ภายใต้โมเดลฟรอนโฮเฟอร์"
- **Physical Model Event:** Two parallel rays leave $S_1$ and $S_2$ at angle $\theta$. Perpendicular line drops from $S_1$ to point $H$ on $S_2 P$. Triangle $\Delta S_1 S_2 H$ highlights. Angle tracing steps show $(90^\circ - \theta)$, proving the apex angle is $\theta$.
- **Dashboard / HUD:** Extra path segment labeled $\Delta r \approx d\sin\theta$. Blocks of whole $\lambda$ (สว่าง: $d\sin\theta = m\lambda$) versus $(m + \frac{1}{2})\lambda$ (มืด: $d\sin\theta = (m + \frac{1}{2})\lambda$).
- **Visible Proof:** Physical perpendicular line $S_1 H$ forms an exact right angle, and the geometric angle chain demonstrates the top angle equals $\theta$.
- **Transition Link:** Connect angle $\theta$ to the linear height $y$ measured on the real screen.

##### Beat 6: `DS06_SmallAngleSpacing` (~80s)
- **Time:** 05:45 – 07:05
- **Camera & Framing:** Locked Front-on View of the screen with a small top-down geometry inset.
- **Narration Claim:** "จากเรขาคณิต $y = L\tan\theta$ และเนื่องจากมุม $\theta$ มีขนาดเล็กมาก เราจึงประมาณ $\sin\theta \approx \tan\theta \approx y/L$ ทำให้ได้ตำแหน่งแถบสว่าง $y_m \approx m\frac{\lambda L}{d}$ และระยะห่างระหว่างแถบที่ติดกันคงที่คือ $\Delta y \approx \frac{\lambda L}{d}$"
- **Physical Model Event:** Screen displays bright fringes at $m = 0, \pm 1, \pm 2$. Dimension brace $\Delta y$ spans adjacent bright fringes, perfectly aligning with the peaks of the intensity plot.
- **Dashboard / HUD:**
  - Exact angular formula: $I(\theta) = 4I_0 \cos^2\left(\frac{\pi d\sin\theta}{\lambda}\right)$.
  - Approximate spatial formula: $I(y) \approx 4I_0 \cos^2\left(\frac{\pi d y}{\lambda L}\right)$ (strictly using $\approx$).
- **Visible Proof:** The dimension brace $\Delta y$ measured between physical screen stripes matches peak-to-peak distance on the graph.
- **Transition Link:** Move into the interactive laboratory to test how changing $\lambda, L, d$ influences $\Delta y$.

---

#### Module 4: `double_slit_04_lab_real.py`
##### Beat 7: `DS07_ParameterLab` (~100s)
- **Time:** 07:05 – 08:45
- **Camera & Framing:** Locked Front-on View of the screen with parameter sliders below and mini-apparatus inset.
- **Narration Claim:** "มาทดลองเปลี่ยนตัวแปรทีละตัวในห้องแล็บ: เพิ่มความยาวคลื่น $\lambda$ (แสงสีแดงมีริ้วกว้างกว่าแสงสีน้ำเงิน), เพิ่มระยะฉาก $L$ (ยิ่งไกล ริ้อยิ่งบานออก), แต่เมื่อเพิ่มระยะห่างสลิต $d$ (สลิตยิ่งห่าง ริ้อยิ่งบีบชิดเข้าหากัน) ทั้งหมดเป็นไปตามสูตร $\Delta y \approx \frac{\lambda L}{d}$"
- **Physical Model Event:**
  - Test 1 ($\lambda \uparrow$): Baseline frozen with dashed gray ghost fringes. Red wavelength increases $\Delta y$, spreading fringes wider than ghost markers. Reset.
  - Test 2 ($L \uparrow$): Screen moves further back; fringes expand proportionally. Reset.
  - Test 3 ($d \uparrow$): Slits move further apart; fringes compress tightly together.
- **Dashboard / HUD:** Interactive sliders for $\lambda, L, d$ linked to master ValueTracker. Formula terms dynamically highlight in matching colors (e.g. green for $\lambda$, blue for $L$, amber for $d$).
- **Visible Proof:** Persistent dashed gray ghost markers allow direct visual verification of widening and narrowing.
- **Transition Link:** Introduce the physical dimension of each individual slit: slit width $a$.

##### Beat 8: `DS08_SlitEnvelope` (~75s)
- **Time:** 08:45 – 10:00
- **Camera & Framing:** Locked Front-on Screen View.
- **Narration Claim:** "ในโลกความเป็นจริง ช่องสลิตแต่ละช่องไม่ได้แคบเป็นศูนย์ แต่มีความกว้าง $a$ ทำให้เกิดการเลี้ยวเบนของสลิตเดี่ยวมาเป็นกรอบโค้ง (Envelope) ครอบกดทับริ้วแทรกสอด และถ้าเลื่อนแผ่นทึบมาปิดสลิตหนึ่งช่อง ริ้วแทรกสอดจะหายไปทันที เหลือเพียงแถบมัวๆ ของสลิตเดี่ยว!"
- **Physical Model Event:** Slit width $a$ (shown in amber/orange) expands from 0. A dashed sinc-squared envelope curve appears, modulating fringe brightness so outer fringes fade away. Then, a physical shutter slides down, covering slit $S_2$.
- **Dashboard / HUD:**
  - Real double-slit equation: $I_{\text{real}}(\theta) = 4I_0 \cos^2\left(\frac{\pi d\sin\theta}{\lambda}\right) \cdot \left(\frac{\sin\beta}{\beta}\right)^2$, where $\beta = \frac{\pi a\sin\theta}{\lambda}$.
  - Separate color keys: $d$ (slit separation) vs $a$ (slit width).
- **Visible Proof:** The moment the shutter physically blocks slit $S_2$, the sharp multi-stripe interference modulation collapses immediately, leaving only a broad, smooth single-slit diffraction profile.
- **Transition Link:** Pull camera back to the complete 3D apparatus for the final causal summary.

##### Beat 9: `DS09_CausalSummary` (~40s)
- **Time:** 10:00 – 10:40
- **Camera & Framing:** 3/4 Isometric Perspective view of the complete apparatus.
- **Narration Claim:** "สรุปหัวใจสำคัญ: หนึ่งแหล่งกำเนิดสร้างสองคลื่นอาพันธ์ $\rightarrow$ ผลต่างเส้นทางเดินสร้างผลต่างเฟส $\rightarrow$ รวมกันแบบแทรกสอด $\rightarrow$ พลังงานกระจายตัวใหม่ในปริภูมิเกิดเป็นริ้วสว่างและมืดบนฉาก แถบมืดไม่ได้แปลว่าพลังงานถูกทำลาย แต่ถูกส่งไปเสริมกันที่แถบสว่าง!"
- **Physical Model Event:** A sequential lighting pulse cascades along the causal chain: Source $\rightarrow$ Slits ($S_1, S_2$) $\rightarrow$ Paths $r_1, r_2$ $\rightarrow$ Screen fringes. The scene freezes into a clear summary infographic with 3 interactive prediction review prompts.
- **Dashboard / HUD:** 4-step causal chain diagram: $\Delta r \rightarrow \Delta \phi \rightarrow \text{Superposition} \rightarrow I(y)$. Prediction cards for $\lambda, L, d$.
- **Visible Proof:** Light cascades sequentially through all four stages in real time, sealing the physical intuition.
- **Transition Link:** Fade to clear, crisp pedagogical conclusion.
