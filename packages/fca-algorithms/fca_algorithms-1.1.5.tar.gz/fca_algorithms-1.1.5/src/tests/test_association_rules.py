import pytest

from src.fca.api_models import IncLattice, Context


def test_association_rules_generation():
    fc = Context(["1", "2", "3"], ["a", "b"], [[0, 1], [1, 0], [1, 1]])
    l = IncLattice(fc)
    ar = l.get_association_rules(["a"], min_confidence=0.2)
    assert len(ar) == 1
    assert [
        (
            round(x.get_confidence(), 2),
            round(x.get_support(), 2),
            x.get_base(),
            x.get_add(),
        )
        for x in ar
    ] == [(0.5, 0.33, ["a"], ["b"])]
