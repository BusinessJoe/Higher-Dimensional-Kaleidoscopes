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

    def is_close(self, other):
        return np.all(np.isclose(self.point, other.point))

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
    print('inters',intersections)

    v = np.matmul(intersections.T, activation_values)
    print(v)
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
        sequences = []
        sequence_queue = [ReflectionSequence(normals, tuple(), start_point)]

        while sequence_queue:
            seq = sequence_queue.pop(0)
            sequences.append(seq)
            for idx in range(len(normals)):
                new_sequence = seq.add_reflection(idx)
                if all(not new_sequence.is_close(s) for s in sequences) and all(not new_sequence.is_close(s) for s in sequence_queue):
                    sequence_queue.append(new_sequence)

        print(sequences)

        return sequences

    def polytope(self):
        """Returns the vertices of the polytope defined by this diagram"""
        normals = self.mirror_normals()

        sequences = self.find_reflection_sequences(normals)

        start_point = _generate_start_point(normals, self.nodes)
        points = np.array([], np.float32).reshape(0, start_point.shape[0])

        for sequence in sequences:
            reflected_point = sequence.reflect(start_point).reshape(1, -1)
            points = np.concatenate((points, reflected_point))

        # Begin with edges between the start point and its images
        edges = []
        edge_queue = []
        for idx in range(len(normals)):
            edge_queue.append((0, idx+1))
        # Reflect the edges over and over
        while edge_queue:
            edge = edge_queue.pop(0)
            edges.append(edge)
            # Loop over each mirror normal
            for idx in range(len(normals)):
                # and construct a new edge by reflecting over that mirror
                reflected_sequences = (sequences[edge[0]].add_reflection(idx), sequences[edge[1]].add_reflection(idx))
                for idx, seq in enumerate(sequences):
                    if seq.is_close(reflected_sequences[0]):
                        idx1 = idx
                    if seq.is_close(reflected_sequences[1]):
                        idx2 = idx
                new_edge = (idx1, idx2)
                new_edge2 = (idx2, idx1)
                if new_edge not in edges and new_edge not in edge_queue and new_edge2 not in edges and new_edge2 not in edge_queue:
                    edge_queue.append(new_edge)

        return points, edges

if __name__ == "__main__":
    # Poor numerical stability of algorithms creates many close points
    d = CoxeterDiagram([0, 0, 1], [5, 3])
    print(d.polytope())
    print(len(d.polytope()))
