import numpy as np


def _proj(x, y):
    return np.dot(x, y) / np.dot(y, y) * y


def _gram_schmidt(vec, others):
    ortho = np.append(others, [vec], axis=0)

    for i in range(1, len(vec)):
        for j in range(i):
            ortho[i] -= _proj(ortho[i], ortho[j])

    return ortho[-1]


def get_axis_vector(axis, normals):
    """Get a vector orthogonal to all normal vectors except the normal at row `axis`"""
    mask = [True] * normals.shape[0]
    mask[axis] = False

    v = _gram_schmidt(normals[axis], normals[mask])
    return v / np.linalg.norm(v)
