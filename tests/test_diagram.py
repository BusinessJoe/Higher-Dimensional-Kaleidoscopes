import pytest

from polytope_visualizer.math import diagram

def test_gen_start_point():
    d = diagram.CoxeterDiagram([True, True], [3])
    normals = d.mirror_normals()
    start_point = diagram._generate_start_point(normals, [1, 1])

    print(normals)
    print(start_point)

    assert False


def test_gen_cube():
    pass

