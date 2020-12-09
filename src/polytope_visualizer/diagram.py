from typing import List
import numpy as np


def _generate_start_point(normals, activation_values):
    """Places a point that is on each of the deactivated mirrors and
    off the activated mirrors"""
    gen_point = np.linalg.solve(normals, activation_values)
    print(gen_point)
    print(np.allclose(np.dot(normals, gen_point), activation_values))
    return np.array([gen_point])


def normal_reflection(point, normal):
    """Reflect a point through a mirror defined by a normal vector"""
    return [point - 2 * np.dot(point, normal) * normal]


def remove_doubles(point):
    """Remove duplicate points"""
    return np.unique(np.round(point, 5), axis=0)


class CoxeterDiagram:
    """A linear coxeter diagram"""
    def __init__(self, nodes: List[bool], edges: List[int]) -> None:
        """Each node is activated (True) or deactivated (False).
        The value at an edge corresponds to the dihedral angle between the connected nodes."""
        self.nodes = nodes
        self.edges = edges

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

    def polytope(self):
        """Returns the vertices of the polytope defined by this diagram"""
        normals = self.mirror_normals()

        points = _generate_start_point(normals, self.nodes)
        # points = np.array([[0, 1.414, 0.1]])

        # reflect points across mirrors multiple times
        for iteration in range(100):
            for d in range(self.dimension):
                for p in range(len(points)):
                    reflected_points = normal_reflection(points[p], normals[d])
                    points = np.concatenate((points, reflected_points))

                points = remove_doubles(points)
        return points


if __name__ == "__main__":
    d = CoxeterDiagram([1, 0, 0], [4, 3])
    print(d.polytope())