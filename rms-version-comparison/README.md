# RMS Pulse Video Version Comparison Review

This is a standalone, local engineering review surface for comparing two genuine rendered versions of the Manim Power Electronics lesson:
**"RMS ของกระแสพัลส์: ทำไม I_rms = I_pk sqrt(D)"** (Course 01066556).

---

## 1. How to Open the Review Site Locally

The site requires **no web server** and **no internet connection**. All assets, video clips, and frame evidence are stored in the local relative directory `./assets/`.

1. Open File Explorer to:
   ```
   C:\Users\wicha\Desktop\manium-agy-pe-next\rms-version-comparison\
   ```
2. Double-click `index.html` (or right-click -> Open with Google Chrome / Edge / Firefox / Safari).
3. The page will load immediately with:
   - Synchronized dual HTML5 video players (Side-by-Side, Before only, After only).
   - Clickable 10-row director brief navigator.
   - High-contrast side-by-side frame inspector with Thai pedagogical notes.
   - 7-category evidence scorecard with visible justifications.
   - Asset audit table.

---

## 2. Compared Video Files & Verified Source Paths

### Version A (Baseline / Before Revision)
- **File Path:** `./assets/version_a_baseline_480p15.mp4`
- **Resolution / FPS:** 854x480 (480p), 15 fps
- **File Size:** 1,372,399 bytes (~1.31 MB)
- **Duration:** 47.79 seconds
- **Source Scene File:** `./assets/pe_pulse_rms_before.py`
- **Known Defects in Baseline:**
  - `lbl_eq` ("ความร้อนเฉลี่ยเท่ากัน!") in Shot 2 at `Y = -1.1` had close clearance to card borders.
  - `brk_ts` and `lbl_ts_b` (brace under axis) from Shot 3 were not faded out, lingering into Shot 8 & Shot 9 and colliding with the Duty Table (`tbl_rect`) and Right Misconception Card (`c_right`).

### Version B (Director Brief Final / After Revision)
- **File Path:** `./assets/version_b_final_1080p25.mp4`
- **Resolution / FPS:** 1920x1080 (1080p Full HD), 25 fps
- **File Size:** 2,753,381 bytes (~2.63 MB)
- **Duration:** 47.92 seconds
- **Source Scene File:** `C:\Users\wicha\Desktop\manium-agy-pe-next\pe_pulse_rms.py` (Git commit `40868e0` on branch `agy-pe-next`)
- **Cloud Render Target:** GitHub Actions Workflow `.github/workflows/render_manim.yml`, Run ID: **35363041207** (Status: `completed`, Conclusion: `success`)
- **Verified Fixes in Revision:**
  - `lbl_eq` moved to `Y = -0.9` with 0.4 units of clean breathing clearance above cards.
  - `FadeOut(brk_ts), FadeOut(lbl_ts_b)` added at Shot 3 cleanup; completely eliminates overlap in Shots 8 and 9.
  - Production-grade Thai font rendering via Loma on Ubuntu cloud container.

---

## 3. Evidence Extraction Pipeline

All comparison frames in `./assets/frames_a/` and `./assets/frames_b/` were extracted from the real rendered MP4 files using FFmpeg at the 10 director-brief beats:

```powershell
# Example frame extraction command:
ffmpeg -ss <timestamp> -i <video_file> -frames:v 1 -y <output_frame.png>
```

| Shot # | Brief Beat | Timestamp | Before Frame | After Frame |
|---|---|---|---|---|
| 1 | Circuit & Question | t = 2.5s | `shot01_question.png` | `shot01_question.png` |
| 2 | RMS Physical Meaning | t = 7.0s | `shot02_rms_meaning.png` | `shot02_rms_meaning.png` |
| 3 | Duty Definition & Waveform | t = 15.0s | `shot03_duty_def.png` | `shot03_duty_def.png` |
| 4 | Squaring Current (i²) | t = 20.0s | `shot04_squaring_curr.png` | `shot04_squaring_curr.png` |
| 5 | Mean over Ts Period | t = 26.0s | `shot05_mean_over_ts.png` | `shot05_mean_over_ts.png` |
| 6 | Root / RMS Payoff | t = 31.0s | `shot06_root_payoff.png` | `shot06_root_payoff.png` |
| 7 | 10 A 25% Numerical Example | t = 36.5s | `shot07_num_example.png` | `shot07_num_example.png` |
| 8 | Duty Variation Control | t = 40.0s | `shot08_duty_variation.png` | `shot08_duty_variation.png` |
| 9 | Iavg Trap Misconception | t = 43.5s | `shot09_iavg_trap.png` | `shot09_iavg_trap.png` |
| 10 | Recap & Active Retrieval | t = 46.5s | `shot10_recap_retrieval.png` | `shot10_recap_retrieval.png` |

---

## 4. Verification Check

- [x] Dual HTML5 video players load and play in sync.
- [x] Master scrubber controls both clips simultaneously.
- [x] 10/10 shots clickable and update the inspection panel.
- [x] All 20 frame PNG files exist locally and resolve with relative paths.
- [x] Zero network requests or CDN dependencies.
- [x] Responsive layout stacks cleanly on narrow viewports.
