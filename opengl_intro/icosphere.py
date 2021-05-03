import numpy as np


class Icosahedron:
    X = .525731112119133606
    Z = .850650808352039932
    N = 0

    coords = np.array([
        [-X, N, Z], [X, N, Z], [-X, N, -Z], [X, N, -Z],
        [N, Z, X], [N, Z, -X], [N, -Z, X], [N, -Z, -X],
        [Z, X, N], [-Z, X, N], [Z, -X, N], [-Z, -X, N]
    ])

    triangles = np.array([
        [0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8], [4, 8, 1],
        [8, 10, 1], [8, 3, 10], [5, 3, 8], [5, 2, 3], [2, 7, 3],
        [7, 10, 3], [7, 6, 10], [7, 11, 6], [11, 0, 6], [0, 1, 6],
        [6, 1, 10], [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]
    ])

    def __init__(self):
        self.vertices = []
        for tri in self.triangles:
            for idx in tri:
                self.vertices.append(self.coords[idx])
        self.vertices = np.array(self.vertices, np.float32)
        self.vertices = np.reshape(self.vertices, (-1,))
        print(self.vertices.size)
        print(self.triangles.size)


Icosahedron()
