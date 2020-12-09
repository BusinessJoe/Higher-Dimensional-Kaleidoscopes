import numpy as np

sample = np.array([[6, 8, 0]])


def project(p, screen_dist, eye_dist):
    dimension = len(p)
    for iteration in range(dimension-2):
        height_ratio = (eye_dist - screen_dist) / (eye_dist - p[-1])
        p = height_ratio * p[:-1]

    return p, height_ratio


v_project = np.vectorize(project, signature='(i),(),()->(n),()')
