"""Scaling test, real internet model A: Kenney Car Kit "sedan.obj" (CC0,
kenney.nl/assets/car-kit), stripped of materials/UVs/normals down to plain
v/f geometry, 1,956 verts / 2,032 faces (~7x the 290-face synthetic car,
~340x the 6-face cube already measured).

Deliberately rendered for only 5 frames (self.wait(0.2) at 25fps) -- if
per-frame cost scaled linearly from the cube's 0.159 s/frame, 2,032 faces
would be ~54 s/frame, so even 5 frames could take several minutes. Measure
this small, safe sample first; do not scale up to a full clip until the
real per-frame number is known.
"""

from mlib import *
import os

OBJ_PATH = os.path.join(os.path.dirname(__file__), "model_a.obj")


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


class ImportedModelA(SafeThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        verts, faces = load_obj(OBJ_PATH)
        model = Polyhedron(
            vertex_coords=verts,
            faces_list=faces,
            faces_config={"fill_color": "#E53935", "fill_opacity": 0.9, "stroke_color": WHITE},
        )
        model.scale(1.0)
        heading = title(f"Real model A: sedan.obj ({len(faces)} faces)")
        self.hud(heading)
        self.add(heading, model)
        self.wait(0.2)
