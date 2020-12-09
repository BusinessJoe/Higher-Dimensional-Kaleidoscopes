"""Module for generating polytope vertices from Coxeter diagrams"""
import numpy as np


# For some reason, with these settings the correct output isn't made? Maybe?

# The coxeter diagram encoded as numbers
# The first column represents the dihedral angle
# The second column represents which nodes are "active"


def generate_normals(diag, dim):
    """Creates normals to mirrors given a Coxeter diagram"""
    output = np.zeros((dim, dim))
    output[0][0] = 1

    for i in range(1, dim):
        for j in range(i + 1):
            if j + 2 <= i:
                output[i][j] = 0
            elif j + 1 <= i:
                output[i][j] = np.cos(np.pi / diag[i - 1][0]) / output[i - 1][j]
            else:
                output[i][j] = np.sqrt(1 - np.square(output[i][j - 1]))
    return output


def normal_reflection(point, normal):
    """Reflect a point through a mirror defined by a normal vector"""
    return [point - 2 * np.dot(point, normal) * normal]


def remove_doubles(point):
    """Remove duplicate points"""
    return np.unique(np.round(point, 5), axis=0)


def generate_start_point(normal_values, activation_values):
    """Places a point that is on each of the deactivated mirrors and
    off the activated mirrors"""
    print(normal_values)
    print(activation_values)
    genPoint = np.linalg.solve(normal_values, activation_values)
    print(genPoint)
    print(np.allclose(np.dot(normal_values, genPoint), activation_values))
    return np.array([genPoint])


def generate_points_from_diagram(diagram, dimension, iterations):
    """Returns the vertices of a polytope defined by the Coxeter diagram"""
    normals = generate_normals(diagram, dimension)

    points = generate_start_point(normals, np.array(diagram)[:, 1])
    # points = np.array([[0, 1.414, 0.1]])

    # reflect points across mirrors multiple times
    for iteration in range(iterations):
        for d in range(dimension):
            for p in range(len(points)):
                reflected_points = normal_reflection(points[p], normals[d])
                points = np.concatenate((points, reflected_points))

            points = remove_doubles(points)
    return points
