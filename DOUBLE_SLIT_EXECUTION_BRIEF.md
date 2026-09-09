# DOUBLE_SLIT_EXECUTION_BRIEF.md
## Master Execution Brief & Storyboard: Young's Double-Slit Wave Interference (3D Manim)
### Rebuild Revision: Duration Budget & Narration-to-Evidence Micro-Beats

---

### 1. Resource Inventory & Target Constraints
- **Target Worktree:** `C:\Users\wicha\Desktop\manium-double-slit`
- **Branch:** `codex/double-slit-3d-lesson`
- **Target Audience:** Zero-prerequisite learners (ผู้เรียนพื้นฐานศูนย์).
- **Target Total Duration:** 9 – 13 minutes (Planned: ~10m47s).
- **Presentation Paradigm:** Narration-led Hybrid (Observable physical 3D/2D event establishes ground truth $\rightarrow$ fixed 2D dashboard/equations confirm).
- **Render Environment:** GitHub Actions Cloud Render (`render_manim.yml`), Ubuntu Container (`manimcommunity/manim:latest`), `MANIM_THAI_FONT: Loma`.

---

### 2. Duration Budget per Scene (Micro-Beat Specification)

| Scene | Class Name | Target Range | Planned Duration | Micro-Beats Breakdown |
| :--- | :--- | :--- | :--- | :--- |
| **DS01** | `DS01_ParadoxHook` | 25 – 35s | **28s** | 4 beats: 3D establish & question (8s), apparatus & incident wave (8s), fringes & paradox question (7s), zoom into dark stripe bridge (5s) |
| **DS02** | `DS02_Wave101` | 65 – 90s | **72s** | 5 beats: Wave anatomy (14s), Wavelength $\lambda$ (12s), In-phase constructive superposition (18s), Out-of-phase destructive superposition (18s), Summary law (10s) |
| **DS03** | `DS03_ApparatusCoherence` | 60 – 85s | **68s** | 5 beats: 3D apparatus establish (15s), Components $S_1, S_2, d, L$ (13s), Incident plane wave arrival (16s), Synchronized secondary circular waves & clocks (14s), Coherence definition & Top-view transition (10s) |
| **DS04** | `DS04_PointPInvestigation` | 90 – 120s | **105s** | 5 beats: Geometry setup & center point $P_0$ (16s), Traveling packet arrival & bright flash (20s), First dark point $P_1$, extra path $\lambda/2$ & dark sum (22s), Live dashboard & phase dial (22s), Continuous sweep & intensity profile accumulation (25s) |
| **DS05** | `DS05_GeometryDerivation` | 80 – 110s | **92s** | 5 beats: Slit zoom & far-field condition $L \gg d$ (18s), Parallel rays & perpendicular $S_1 H$ construction (20s), Geometric angle proof for $\theta$ & $\Delta r \approx d\sin\theta$ (22s), Bright fringe condition $d\sin\theta = m\lambda$ (16s), Dark fringe condition $d\sin\theta = (m+\frac{1}{2})\lambda$ (16s) |
| **DS06** | `DS06_SmallAngleSpacing` | 70 – 95s | **78s** | 4 beats: Screen view & fringe orders $m$ (16s), Small-angle approximation $\sin\theta \approx \tan\theta \approx y/L$ (18s), Step-by-step derivation of $y_m$ & $\Delta y$ (20s), Screen brace measurement aligned with intensity plot peaks (24s) |
| **DS07** | `DS07_ParameterLab` | 90 – 120s | **98s** | 4 beats: Lab interface & baseline ghost fringes (18s), Exp 1: $\lambda$ up (Red light) with ghost comparison (24s), Exp 2: $L$ up (Distance) with ghost comparison (24s), Exp 3: $d$ up (Slit gap) with ghost comparison (32s) |
| **DS08** | `DS08_SlitEnvelope` | 70 – 95s | **82s** | 3 beats: Dimension $a$ vs $d$ color distinction & ideal profile (20s), Sinc^2 diffraction envelope construction (26s), Shutter sliding over $S_2$ and collapse to single slit (36s) |
| **DS09** | `DS09_CausalSummary` | 35 – 55s | **44s** | 3 beats: 4-step causal chain (16s), Sequential lighting cascade across apparatus (14s), 3 Prediction summary cards (14s) |
| **Total** | **9 Scenes** | **9 – 13 min** | **10m 47s** | **Full pedagogical cadence: zero idle waits, dedicated reading pauses** |

---

### 3. Reading Time & Micro-Beat Principles
- **Simple Thai Captions:** 2.5 – 3.0s display and hold time.
- **Dense Physics Explanations:** 3.5 – 5.0s display and hold time.
- **Mathematical Equations & Derivations:** 4.5 – 6.5s display and hold time.
- **Visual-Physical Sync:** Every named term flashes or gets a pointer arrow at mention; wave packets literally meet at the probe/screen in the same frame.
- **Proving Shots:** Strictly locked camera during geometric proofs and parameter comparisons.
