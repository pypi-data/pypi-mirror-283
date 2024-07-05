import pytest

from anarchy import Anarchy, AnarchyNode, AnarchyEdge


@pytest.fixture
def anarchy():
    return Anarchy()


def test_anarchy(anarchy):
    assert anarchy is not None


def test_anarchy_add(anarchy):
    """Should add a node to the graph."""
    node = AnarchyNode(1)
    anarchy.add(1, node)
    assert anarchy.get(1) == node


def test_anarchy_add_reciprocal(anarchy):
    """Should add reciprocal edges to the node and the graph."""
    node1 = AnarchyNode(1)
    anarchy.add(1, node1, reciprocal=True)
    assert node1.edges.get(1) == node1
    assert anarchy.get(1) == node1


def test_anarchy_remove(anarchy):
    """Should remove a node from the graph."""
    node = AnarchyNode(1)
    anarchy.add(1, node)
    anarchy.remove(1)
    assert anarchy.get(1) is None


def test_anarchy_remove_reciprocal(anarchy):
    """Should remove reciprocal edges from the node and the graph."""
    node1 = AnarchyNode(1)
    anarchy.add(1, node1, reciprocal=True)
    anarchy.remove(1)
    assert node1.edges.get(1) is None
    assert anarchy.get(1) is None


def test_anarchy_get(anarchy):
    """Should get an edge from the graph by node_id."""
    node1 = AnarchyNode(1)
    anarchy.add(1, node1)
    assert anarchy.get(1) == node1


def test_anarchy_types(anarchy):
    node1 = AnarchyNode(1)
    anarchy.add(1, node1)
    assert type(anarchy.get(1)) == AnarchyEdge
    assert type(anarchy.get(1).node) == AnarchyNode


def test_anarchy_edges(anarchy):
    node1 = AnarchyNode(1)
    node2 = AnarchyNode(2)
    assert len(anarchy.edges()) == 0
    anarchy.add(1, node1)
    assert len(anarchy.edges()) == 1
    anarchy.add(2, node2)
    assert len(anarchy.edges()) == 2
    assert 1 in anarchy.edges()
    assert 2 in anarchy.edges()
