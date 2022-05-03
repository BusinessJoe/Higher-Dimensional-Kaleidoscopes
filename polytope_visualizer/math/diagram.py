from typing import List
import numpy as np

from ..math.utils import get_axis_vector


class Polytope:
    def __init__(self, dimension: int = 3):
        self.dimension = dimension
        self.vertices = []
        self.edges = []
        self.faces = []


class ReflectionSequence:
    def __init__(self, all_normals, sequence, point):
        self.all_normals = all_normals
        self.sequence = sequence
        self.point = point

    def add_reflection(self, normal_idx):
        new_point = normal_reflection(self.point, self.all_normals[normal_idx])
        new_sequence = self.sequence + (self.all_normals[normal_idx],)

        return ReflectionSequence(self.all_normals, new_sequence, new_point)

    def reflect(self, point):
        for normal in self.sequence:
            point = normal_reflection(point, normal)
        return point

    def _point_eq(self, p1, p2):
        return np.all(np.isclose(p1, p2))

    def __eq__(self, other):
        return self._point_eq(self.point, other.point)

    def shares_edge_with(self, other):
        for normal in self.all_normals:
            new_point = normal_reflection(self.point, normal)
            if self._point_eq(new_point, other.point):
                return True
        return False


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
    return point - 2 * np.dot(point, normal) * normal


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


    def find_reflection_sequences(self, normals):
        start_point = _generate_start_point(normals, [1 for n in self.nodes])

        # Begin with only an empty sequence which represents no reflections
        sequences = [ReflectionSequence(normals, tuple(), start_point)]

        flag = True
        while flag:
            flag = False
            for idx in range(len(normals)):
                for s in sequences:
                    new_sequence = s.add_reflection(idx)
                    if all(new_sequence != s2 for s2 in sequences):
                        sequences.append(new_sequence)
                        flag = True

        return sequences

    def polytope(self, iterations=100):
        """Returns the vertices of the polytope defined by this diagram"""
        normals = self.mirror_normals()

        sequences = self.find_reflection_sequences(normals)
        print("Length:", len(sequences))

        start_point = _generate_start_point(normals, self.nodes)
        points = start_point.reshape(1, -1)

        for sequence in sequences:
            reflected_point = sequence.reflect(start_point).reshape(1, -1)
            points = np.concatenate((points, reflected_point))

        edges = []
        for idx1, s1 in enumerate(sequences):
            for idx2, s2 in enumerate(sequences):
                if idx2 > idx1 and s1.shares_edge_with(s2):
                    edges.append((s1.sequence, s2.sequence))

        print(points[0])

        return points, edges


        # reflect points across mirrors multiple times
        num_points_old = points.shape[0]
        for iteration in range(iterations):
            for d in range(self.dimension):
                for p in range(len(points)):
                    reflected_point = normal_reflection(points[p], normals[d])
                    points = np.concatenate((points, reflected_point))
                    edges.append((points[p], reflected_point))

                points = remove_doubles(points)
                if points.shape[0] > 1000:
                    raise ValueError('Too many generated points')

            # Break if no new points were created
            num_points = points.shape[0]
            if num_points_old == num_points:
                break
            num_points_old = num_points

        return points, edges


if __name__ == "__main__":
    # Poor numerical stability of algorithms creates many close points
    d = CoxeterDiagram([0, 0, 1], [5, 3])
    print(d.polytope())
    print(len(d.polytope()))
