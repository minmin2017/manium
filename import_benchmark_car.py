"""Scaling test: how does the Polyhedron .obj-import cost (see
import_benchmark.py, ~20x slower than native Cube() for a 6-face cube)
change for a genuinely bigger mesh? test_car.obj is a synthetic low-poly
car (512 verts / 290 faces -- chassis, cabin, bumpers, lights, mirrors,
exhausts, 4 wheels) generated as a stand-in for "a real car model", since
downloading an untrusted external .obj isn't worth the risk for a pure
performance measurement.

Kept deliberately short (self.wait(1) = 25 frames, not 150) to bound the
cloud-render cost while the per-frame scaling is still unknown -- extrapolate
from this before committing to a full-length clip at this face count.
"""

from mlib import *
import os

OBJ_PATH = os.path.join(os.path.dirname(__file__), "test_car.obj")


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


class ImportedCarTest(SafeThreeDScene):
    """290-face imported car via Polyhedron -- scaling data point vs the
    6-face cube already measured in import_benchmark.py."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        verts, faces = load_obj(OBJ_PATH)
        model = Polyhedron(
            vertex_coords=verts,
            faces_list=faces,
            faces_config={"fill_color": "#E53935", "fill_opacity": 0.9, "stroke_color": WHITE},
        )
        model.scale(1.0)
        heading = title(f"Import test: car .obj ({len(faces)} faces)")
        self.hud(heading)
        self.add(heading, model)
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(1)
        self.stop_ambient_camera_rotation()
