import numpy as np


def reshape_to_tris(coords):
    return np.reshape(coords, (-1, 3, 3))


def calculate_normals(tris):
    normals = np.empty(tris.shape, tris.dtype)
    for i, tri in enumerate(tris):
        v1 = tri[1] - tri[0]
        v2 = tri[2] - tri[0]
        normal = np.cross(v2, v1)
        normals[i][0] = normal
        normals[i][1] = normal
        normals[i][2] = normal
    return normals


def add_normals(vertices):
    tris = reshape_to_tris(vertices)
    normals = calculate_normals(tris)

    vertices = np.concatenate((tris, normals), axis=-1)
    vertices = np.reshape(vertices, (-1,))
    return vertices


if __name__ == '__main__':
    vertices = np.array([
        -0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, 0.5, -0.5,
        0.5, 0.5, -0.5,
        -0.5, 0.5, -0.5,
        -0.5, -0.5, -0.5,

        -0.5, -0.5, 0.5,
        0.5, -0.5, 0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5,
        -0.5, -0.5, 0.5,

        -0.5, 0.5, 0.5,
        -0.5, 0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5, 0.5,
        -0.5, 0.5, 0.5,

        0.5, 0.5, 0.5,
        0.5, 0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, 0.5,
        0.5, 0.5, 0.5,

        -0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, 0.5,
        0.5, -0.5, 0.5,
        -0.5, -0.5, 0.5,
        -0.5, -0.5, -0.5,

        -0.5, 0.5, -0.5,
        0.5, 0.5, -0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5,
        -0.5, 0.5, -0.5
    ], np.float32)

    vertices = add_normals(vertices)

    print(vertices.dtype)
