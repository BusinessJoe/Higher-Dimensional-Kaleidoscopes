import pytest

from polytope_visualizer.math import diagram

def test_gen_cube():
    diag = diagram.CoxeterDiagram([1, 0, 0], [3, 3])
    p, e = diag.polytope()
    print(p)
    print(e)
    print(len(e))

