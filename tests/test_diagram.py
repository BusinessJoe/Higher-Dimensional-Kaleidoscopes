import pytest

from polytope_visualizer.math import diagram

def test_gen_53():
    d = diagram.CoxeterDiagram([1, 1, 1], [5, 3])
    print(d.polytope())

