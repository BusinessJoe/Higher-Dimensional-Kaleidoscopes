import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("norm cannot be zero")
    return v / norm


def translate(m, v):
    """Python implementation of glm::translate"""
    result = np.copy(m)
    result[3] = m[0] * v[0] + m[1] * v[1] + m[2] * v[2] + m[3]
    return result


def rotate(m, angle, v):
    """Python implementation of glm::rotate"""
    a = angle
    c = np.cos(a)
    s = np.sin(a)

    axis = normalize(v)
    temp = (1 - c) * axis

    rotate = np.empty((4, 4), np.float32)
    rotate[0][0] = c + temp[0] * axis[0]
    rotate[0][1] = temp[0] * axis[1] + s * axis[2]
    rotate[0][2] = temp[0] * axis[2] - s * axis[1]

    rotate[1][0] = temp[1] * axis[0] - s * axis[2]
    rotate[1][1] = c + temp[1] * axis[1]
    rotate[1][2] = temp[1] * axis[2] + s * axis[0]

    rotate[2][0] = temp[2] * axis[0] + s * axis[1]
    rotate[2][1] = temp[2] * axis[1] - s * axis[0]
    rotate[2][2] = c + temp[2] * axis[2]

    result = np.empty((4, 4), np.float32)
    result[0] = m[0] * rotate[0][0] + m[1] * rotate[0][1] + m[2] * rotate[0][2]
    result[1] = m[0] * rotate[1][0] + m[1] * rotate[1][1] + m[2] * rotate[1][2]
    result[2] = m[0] * rotate[2][0] + m[1] * rotate[2][1] + m[2] * rotate[2][2]
    result[3] = m[3]
    return result


def perspective(fovy, aspect, z_near, z_far):
    """Python implementation of glm::perspective"""
    if aspect == 0:
        raise ValueError("aspect cannot be 0")
    if z_far == z_near:
        raise ValueError("z_far cannot be equal to z_near")

    rad = fovy

    tan_half_fovy = np.tan(rad / 2)

    result = np.zeros((4, 4), np.float32)
    result[0][0] = 1 / (aspect * tan_half_fovy)
    result[1][1] = 1 / tan_half_fovy
    result[2][2] = - (z_far + z_near) / (z_far - z_near)
    result[2][3] = -1
    result[3][2] = - (2 * z_far * z_near) / (z_far - z_near)
    return result


def scale(m, v):
    result = np.empty((4, 4))
    result[0] = m[0] * v[0]
    result[1] = m[1] * v[1]
    result[2] = m[2] * v[2]
    result[3] = m[3]
    return result
