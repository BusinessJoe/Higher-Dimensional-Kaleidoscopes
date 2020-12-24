from typing import List
import numpy as np

from ..math.utils import get_axis_vector


def _generate_start_point(normals, activation_values):
    """Places a point that is on each of the deactivated mirrors and
    off the activated mirrors"""

    # Find intersections of planes where each intersection is a vector
    intersections = np.empty(normals.shape)
    for idx in range(normals.shape[0]):
        intersections[idx] = get_axis_vector(idx, normals)

    # Flip intersection vectors so that they all point in the same direction
    for idx in range(1, intersections.shape[0]):
        if np.dot(intersections[idx], intersections[idx-1]) < 0:
            intersections[idx] *= -1

    v = np.matmul(intersections.T, activation_values)
    return v / np.linalg.norm(v)


def normal_reflection(point, normal):
    """Reflect a point through a mirror defined by a normal vector"""
    return [point - 2 * np.dot(point, normal) * normal]


def remove_doubles(points):
    """Remove duplicate points"""
    _, indices = np.unique(np.round(points, 5), axis=0, return_index=True)
    return points[indices]


class CoxeterDiagram:
    """A linear coxeter diagram"""
    def __init__(self, nodes: List[bool], edges: List[int]) -> None:
        """Each node is activated (True) or deactivated (False).
        The value at an edge corresponds to the dihedral angle between the connected nodes."""
        self.nodes: List[bool] = nodes
        self.edges: List[int] = edges

        # A linear diagram of with n nodes can be embedded in n-dimensions
        self.dimension = len(nodes)

    def mirror_normals(self):
        """Returns the normal vectors of the mirrors defined"""
        normals = np.zeros((self.dimension, self.dimension))

        # Set the first normal to (1, 0, 0, ...)
        normals[0][0] = 1

        for i in range(1, self.dimension):
            for j in range(i + 1):
                if j + 2 <= i:
                    normals[i][j] = 0
                elif j + 1 <= i:
                    normals[i][j] = np.cos(np.pi / self.edges[i - 1]) / normals[i - 1][j]
                else:
                    normals[i][j] = np.sqrt(1 - np.square(normals[i][j - 1]))

        return normals

    def polytope(self, iterations=100):
        """Returns the vertices of the polytope defined by this diagram"""
        normals = self.mirror_normals()

        points = _generate_start_point(normals, self.nodes).reshape(1, -1)

        # reflect points across mirrors multiple times
        for iteration in range(iterations):
            for d in range(self.dimension):
                for p in range(len(points)):
                    reflected_points = normal_reflection(points[p], normals[d])
                    points = np.concatenate((points, reflected_points))

                points = remove_doubles(points)
                if points.shape[0] > 1000:
                    raise ValueError('Too many generated points')
        return points


if __name__ == "__main__":
    # Poor numerical stability of algorithms creates many close points
    d = CoxeterDiagram([0, 0, 1], [5, 3])
    print(d.polytope())
    print(len(d.polytope()))
