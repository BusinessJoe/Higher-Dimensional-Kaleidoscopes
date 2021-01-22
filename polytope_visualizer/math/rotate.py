import numpy as np
import math


def rotate(point, angle, axis1, axis2):
    """Rotates the point with the plane defined by the two axes"""
    dimension = len(point)
    matrix = np.identity(dimension)

    matrix[axis1][axis1] = math.cos(angle)
    matrix[axis1][axis2] = math.sin(angle)
    matrix[axis2][axis1] = -math.sin(angle)
    matrix[axis2][axis2] = math.cos(angle)

    return np.matmul(point, matrix)


v_rotate = np.vectorize(rotate, signature='(i),(),(),()->(n)')


def reflect(vector, normal):
    return vector - 2 * np.dot(vector, np.atleast_2d(normal).T) / np.dot(normal, normal) * normal


class Rotor:
    def __init__(self, axis1, axis2, angle=0.0):
        self.axes = [axis1, axis2]
        self.angle = angle

    def rotate(self, points):
        dimension = points.shape[1]
        a = np.zeros((dimension,))
        a[self.axes[0]] = 1

        R = np.eye(dimension)
        s, c = np.sin(self.angle/2), np.cos(self.angle/2)
        R[self.axes[0], self.axes[0]] = c
        R[self.axes[0], self.axes[1]] = -s
        R[self.axes[1], self.axes[0]] = s
        R[self.axes[1], self.axes[1]] = c

        b = R.dot(a)

        return reflect(reflect(points, a), b)

