import pytest
from hypothesis import given
from hypothesis import strategies as st

from anarchy import AnarchyGraph, AnarchyNode


class TestGraph:

    # Simple pytest tests
    def test_graph_initialization(self):
        g = AnarchyGraph(5)
        assert len(g) == 5
        assert all(isinstance(node, AnarchyNode) for node in g.values())

    def test_random_node(self):
        g = AnarchyGraph(5)
        node = g.random()
        assert isinstance(node, AnarchyNode)
        assert node in g.values()

    def test_to_dict(self):
        g = AnarchyGraph(5)
        graph_dict = g.to_dict()
        assert isinstance(graph_dict, dict)
        assert "nodes" in graph_dict["elements"]
        assert "edges" in graph_dict["elements"]

    def test_to_json(self):
        g = AnarchyGraph(5)
        graph_json = g.to_json()
        assert isinstance(graph_json, str)
        assert graph_json.startswith("{") and graph_json.endswith("}")

    # Property-based tests using hypothesis
    @given(st.integers(min_value=0, max_value=100))
    def test_graph_size(self, node_count):
        g = AnarchyGraph(node_count)
        assert len(g) == node_count

    def test_add_node(self):
        node = AnarchyNode(10)
        g = AnarchyGraph(5)
        g.add_node(10, node)
        assert len(g) == 6
        assert node in g.values()

    def test_remove_node(self):
        g = AnarchyGraph(5)
        g.remove_node(0)
        assert len(g) == 4
        assert 0 not in g

    def test_get_node(self):
        g = AnarchyGraph(5)
        node = g.get_node(0)
        assert node in g.values()

    def test_has_node(self):
        g = AnarchyGraph(5)
        assert g.has_node(0)
        assert not g.has_node(10)

    def test_num_nodes(self):
        g = AnarchyGraph(5)
        assert g.num_nodes == 5

    def test_density(self):
        g = AnarchyGraph(5)
        assert g.density == 0
