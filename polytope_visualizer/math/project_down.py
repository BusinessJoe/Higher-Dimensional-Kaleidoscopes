import numpy as np

sample = np.array([[6, 8, 0]])


def project(p, screen_dist, eye_dist):
    dimension = len(p)
    for iteration in range(dimension-2):
        height_ratio = (eye_dist - screen_dist) / (eye_dist - p[-1])
        p = height_ratio * p[:-1]

    return p, height_ratio


def project_3d(points):
    """Projects the points orthographically to 3d"""
    dimension = points.shape[1]
    if dimension >= 3:
        return points[:, :3]
    else:
        zeros = np.zeros((points.shape[0], dimension + 1))
        zeros[:, :-1] = points
        return zeros


v_project = np.vectorize(project, signature='(i),(),()->(n),()')
