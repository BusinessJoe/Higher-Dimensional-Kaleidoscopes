import numpy as np
from transformations import normalize


def icosahedron_tris():
    X = .525731112119133606
    Z = .850650808352039932
    N = 0

    coords = np.array([
        [-X, N, Z], [X, N, Z], [-X, N, -Z], [X, N, -Z],
        [N, Z, X], [N, Z, -X], [N, -Z, X], [N, -Z, -X],
        [Z, X, N], [-Z, X, N], [Z, -X, N], [-Z, -X, N]
    ])

    indices = np.array([
        [0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8], [4, 8, 1],
        [8, 10, 1], [8, 3, 10], [5, 3, 8], [5, 2, 3], [2, 7, 3],
        [7, 10, 3], [7, 6, 10], [7, 11, 6], [11, 0, 6], [0, 1, 6],
        [6, 1, 10], [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]
    ])

    tris = []
    for tri in indices:
        triangle = [coords[tri[0]], coords[tri[1]], coords[tri[2]]]
        tris.append(triangle)
    tris = np.array(tris, np.float32)

    return tris


class Icosphere:
    def __init__(self, subdivisions: int, smooth_shading: bool = False):
        self._triangles = icosahedron_tris()
        self.count = 180

        for _ in range(subdivisions):
            self._subdivide()

    def _subdivide(self):
        new_tris = []
        for tri in self._triangles:
            new_tris.extend(self._subdivide_tri(tri))
        self._triangles = np.array(new_tris, np.float32)
        self.count *= 4

    def _subdivide_tri(self, tri):
        a = tri[0]
        b = tri[1]
        c = tri[2]
        ab = normalize((a + b) / 2)
        ac = normalize((a + c) / 2)
        bc = normalize((b + c) / 2)

        new_tris = [
            [a, ab, ac],
            [ab, b, bc],
            [ab, bc, ac],
            [ac, bc, c],
        ]
        return new_tris

    def vertices(self):
        # TODO: add normals
        return np.reshape(self._triangles, (-1))


