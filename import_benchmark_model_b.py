"""Scaling test, real internet model B: Khronos glTF-Sample-Assets
"BarramundiFish" (CC0), decimated with trimesh from 3,864 to 1,799 faces
(969 verts) and re-exported to plain .obj -- a different shape/topology
from model A's car, to see whether the Polyhedron-import cost tracks face
count regardless of the mesh's shape.

Same caution as model A: rendered for only 5 frames (self.wait(0.2) at
25fps) until the real per-frame cost at this face count is known.
"""

from mlib import *
import os

OBJ_PATH = os.path.join(os.path.dirname(__file__), "model_b.obj")


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


class ImportedModelB(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        verts, faces = load_obj(OBJ_PATH)
        model = Polyhedron(
            vertex_coords=verts,
            faces_list=faces,
            faces_config={"fill_color": "#42A5F5", "fill_opacity": 0.9, "stroke_color": WHITE},
        )
        model.scale(1.0)
        heading = title(f"Real model B: BarramundiFish ({len(faces)} faces)")
        self.hud(heading)
        self.add(heading, model)
        self.wait(0.2)
