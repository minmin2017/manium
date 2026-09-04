"""Benchmark: real 3D-model 'import' (Polyhedron parsed from a .obj file)
vs manim's native Cube(), same camera work, to measure the actual render-time
overhead instead of guessing (Min's standing rule: measure on this machine,
report real numbers). Both scenes render on the same GitHub Actions runner
via one workflow dispatch so timing is comparable within one run.
"""

from mlib import *
import os

OBJ_PATH = os.path.join(os.path.dirname(__file__), "test_cube.obj")


def load_obj(path):
    verts, faces = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("v "):
                verts.append([float(x) for x in line.split()[1:4]])
            elif line.startswith("f "):
                idx = [int(tok.split("/")[0]) - 1 for tok in line.split()[1:]]
                faces.append(idx)
    return verts, faces


class ImportedCubeTest(SafeThreeDScene):
    """The 'import a 3D model' path: parse a .obj, feed it into Polyhedron()."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        verts, faces = load_obj(OBJ_PATH)
        model = Polyhedron(
            vertex_coords=verts,
            faces_list=faces,
            faces_config={"fill_color": "#42A5F5", "fill_opacity": 0.85, "stroke_color": WHITE},
        )
        model.scale(1.6)
        heading = title("Import test: Polyhedron from .obj")
        self.hud(heading)
        self.add(heading, model)
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(6)
        self.stop_ambient_camera_rotation()


class BuiltinCubeTest(SafeThreeDScene):
    """Baseline: manim's own Cube(), identical camera work, for a fair comparison."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        model = Cube(side_length=3.2, fill_color="#42A5F5", fill_opacity=0.85, stroke_width=1)
        heading = title("Baseline: manim's built-in Cube()")
        self.hud(heading)
        self.add(heading, model)
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(6)
        self.stop_ambient_camera_rotation()
