# Manim Project Rules (minmin2017/manium)

## 1. Safety & Local Execution Invariants
- **NEVER render scenes locally**: Do NOT execute `manim` render commands locally. Local rendering on CPU is too slow and exhausts local resources.
- **Local verification allowed ONLY via**:
  - `python -m py_compile <scene_file.py>`
  - `python -c "import <scene_module>"`
  (Activate `.venv_community` if dependencies are not in the global Python environment).
- **Subclassing**: Always subclass `SafeScene` (for 2D) or `SafeThreeDScene` (for 3D) from `mlib.py`. Never use bare `Scene` or `ThreeDScene`.
- **Text & HUD**: All text and labels in `SafeThreeDScene` must pass through `self.hud(...)` before displaying.

## 2. 3D Primitives & Performance Constraints
- **NEVER use `Arrow3D` or `Line3D`**: Always use `arrow3(...)` and `line3(...)` from `mlib.py` (flat 2D primitives in 3D space, ~62x faster).
- **Cylinder & Sphere Resolution Limits**:
  - Maximum resolution: `(10, 10)`. Never exceed `(12, 12)`.
  - Preferred resolution: `(6, 6)` for trunks/poles, `(8, 8)` for main columns.
- **Prefer Prisms and Flat Polygons**: Boxes (`Prism`) and flat 2D `Polygon` / `Rectangle` are vastly cheaper than curved meshes.
- **2D Shapes in 3D Space (`shade_in_3d`)**:
  - Any 2D `Polygon`, `Rectangle`, or flat patch placed in 3D space MUST have `mob.shade_in_3d = True` set explicitly.
  - Without `shade_in_3d = True`, Cairo depth sorting assigns distance `np.inf`, drawing flat shapes over all foreground geometry.
- **Static Geometry**: Build all static geometry ONCE during `construct()` initialization. Never rebuild meshes inside `always_redraw`.

## 3. Cloud Render Dispatch Protocol
- **Dispatch**:
  ```bash
  gh workflow run render_manim.yml --repo minmin2017/manium --ref <branch> \
    -f scene_file=<file.py> -f scene_names="<SceneName>" -f quality=h -f fps=60
  ```
- **Monitoring**: Retrieve run ID immediately (`gh run list ... --limit 1`). Do NOT block execution in a tight polling loop.
- **Verification**: Download completed artifacts to `out_<name>/`, extract >=8 keyframes with `ffmpeg`, and visually inspect using image viewing tools.
