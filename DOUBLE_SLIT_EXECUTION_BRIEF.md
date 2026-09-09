# DOUBLE_SLIT_EXECUTION_BRIEF.md
## Master Execution Brief & Storyboard: Young's Double-Slit Wave Interference (3D Manim)
### Objective Duration Ledger Revision (Verified via AST Animation & Wait Timing)

---

### 1. Resource Inventory & Target Constraints
- **Target Worktree:** `C:\Users\wicha\Desktop\manium-double-slit`
- **Branch:** `codex/double-slit-3d-lesson`
- **Target Audience:** Zero-prerequisite learners (ผู้เรียนพื้นฐานศูนย์).
- **Target Total Duration:** >= 655s (10m55s), acceptable 10 – 13 minutes.
- **Actual AST Animation/Wait Ledger Total:** **693.80s (11 minutes 34 seconds)**.
- **Presentation Paradigm:** Narration-led Hybrid (Observable physical 3D/2D event establishes ground truth $\rightarrow$ fixed 2D dashboard/equations confirm).
- **Render Environment:** GitHub Actions Cloud Render (`render_manim.yml`), Ubuntu Container (`manimcommunity/manim:latest`), `MANIM_THAI_FONT: Loma`.

---

### 2. AST Duration Ledger & Micro-Beat Specification

| Scene | Class Name | Minimum Target | Actual AST Duration | Events Count | Pedagogical Micro-Beats & Observable Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DS01** | `DS01_ParadoxHook` | $\ge$ 25s | **33.00s** | 13 | 4 hook events: 3D apparatus establish, novice 2-stripe expectation, multi-fringe wave reality discovery, dark-stripe paradox question & push zoom |
| **DS02** | `DS02_Wave101` | $\ge$ 70s | **71.50s** | 25 | 5 beats: Field amplitude & equilibrium axis, Crest (+A) & Trough (-A), Wavelength $\lambda$ & Amplitude $A$, In-phase constructive ($2A$), Out-of-phase destructive ($0$), Phase dial (after demo) & master rule |
| **DS03** | `DS03_ApparatusCoherence` | $\ge$ 65s | **68.70s** | 26 | 4 beats: Component identification (Source, Barrier $S_1/S_2/d$, Screen $L$) with flash pointers, Incident wavefront arrival before emission, Coherent locked clocks & secondary circular waves, Top-view camera transition |
| **DS04** | `DS04_PointPInvestigation` | $\ge$ 105s | **107.40s** | 35 | 6 beats: Center $P_0$ path equality ($r_1 = r_2$), Packets arrive together & bright flash, First dark $P_1$ ($\Delta r = \lambda/2$) & destructive cancellation, First side maximum $P_2$ ($\Delta r = 1\lambda$), Live dashboard, Full sweep & intensity profile |
| **DS05** | `DS05_GeometryDerivation` | $\ge$ 90s | **91.20s** | 29 | 6 beats: Far-field condition $L \gg d$, Parallel rays at angle $\theta$, Perpendicular $S_1 H$ construction, Geometric triangle angle proof ($\theta$ at apex), Triangle projection ($\Delta r \approx d\sin\theta$), Whole/half wavelength wave packet arrivals ($m\lambda$ vs $(m+\frac{1}{2})\lambda$) |
| **DS06** | `DS06_SmallAngleSpacing` | $\ge$ 80s | **80.90s** | 24 | 4 beats: Screen view & fringe orders $m$, Small-angle approximation ($\sin\theta \approx \tan\theta \approx y/L$) with numerical validation, Adjacent order subtraction ($y_{m+1} - y_m \approx \frac{\lambda L}{d}$), Screen brace aligned with intensity peaks |
| **DS07** | `DS07_ParameterLab` | $\ge$ 100s | **100.80s** | 38 | 4 beats: Baseline setup with locked ghost markers, 3 full Prediction/Change/Ghost/Confirm cycles: Cycle 1 ($\lambda \uparrow \implies \Delta y \uparrow$), Cycle 2 ($L \uparrow \implies \Delta y \uparrow$), Cycle 3 ($d \uparrow \implies \Delta y \downarrow$) with denominator warning and master table |
| **DS08** | `DS08_SlitEnvelope` | $\ge$ 80s | **80.60s** | 25 | 3 beats: Dimension $a$ (width) vs $d$ (separation) distinction & ideal equal-height profile, Sinc$^2$ diffraction envelope construction & product formula $I_{\text{real}} = I_{\text{interf}} \times I_{\text{diff}}$, Mechanical shutter sliding over $S_2$ and single-slit collapse |
| **DS09** | `DS09_CausalSummary` | $\ge$ 40s | **59.70s** | 26 | 3 beats: 4-step causal chain & spatial redistribution of energy (no energy lost), 3D sequential lighting cascade across apparatus, 3 interactive Question / Pause / Reveal prediction cycles |
| **Total** | **9 Scenes** | **$\ge$ 655s** | **693.80s** | **241 events** | **11 minutes 34 seconds: Every single scene strictly exceeds its minimum target with real, observable teaching beats** |

---

### 3. Reading Time & Micro-Beat Principles
- **Simple Thai Captions:** 3.5 – 5.0s readable hold time.
- **Dense Physics Explanations:** 4.5 – 6.5s display and hold time.
- **Mathematical Equations & Derivations:** 5.0 – 8.0s display and hold time.
- **Visual-Physical Sync:** Every named term flashes or gets a pointer arrow at mention; wave packets literally meet at the probe/screen in the same frame.
- **Proving Shots:** Strictly locked camera during geometric proofs and parameter comparisons.
