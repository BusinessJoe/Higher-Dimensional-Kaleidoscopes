import numpy as np
import math

sample = np.array([[1, 1], [-1, -1]])


def rotate(point, angle, axis1, axis2, dimension):
    matrix = np.identity(dimension)

    matrix[axis1][axis1] = math.cos(angle)
    matrix[axis1][axis2] = math.sin(angle)
    matrix[axis2][axis1] = -math.sin(angle)
    matrix[axis2][axis2] = math.cos(angle)

    return np.matmul(point, matrix)


v_rotate = np.vectorize(rotate, signature='(i),(),(),(),()->(n)')

if __name__ == '__main__':
    print(v_rotate(sample, math.pi/4, 0, 1, 2))
