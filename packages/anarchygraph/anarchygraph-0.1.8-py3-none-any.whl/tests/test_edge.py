import pytest
from hypothesis import given
from hypothesis import strategies as st

from anarchy import Anarchy, AnarchyEdge, AnarchyNode


class TestEdge:

    @pytest.fixture
    def node1(self):
        return AnarchyNode(1)

    @pytest.fixture
    def node2(self):
        return AnarchyNode(2)

    @pytest.fixture
    def anarchy(self):
        return Anarchy()

    def test_edge_initialization(self, node1):
        edge = AnarchyEdge(node1.node_id, node1, edge_type="undirected")
        assert edge.node_id == node1.node_id
        assert edge.edge_type == "undirected"
        assert edge.node == node1

    def test_edge_finalizer(self):
        node1 = AnarchyNode(1)
        anarchy = Anarchy()
        edge = AnarchyEdge(node1.node_id, node1, edge_holder=anarchy)
        anarchy[node1.node_id] = edge
        assert node1.node_id in anarchy
        del node1
        assert anarchy == {}

    def test_edge_attributes(self, node1):
        edge = AnarchyEdge(node1.node_id, node1, custom_attr="custom_value")
        assert edge.node_id == node1.node_id
        assert edge.edge_type == "directed"
        assert edge.custom_attr == "custom_value"

    def test_edge_repr(self, node1):
        edge = AnarchyEdge(node1.node_id, node1)
        assert repr(edge) == f"Edge(node: {node1.node_id}, type: directed)"

    def test_multiple_edges(self, node1, node2):
        edge1 = AnarchyEdge(node1.node_id, node1, edge_type="undirected")
        edge2 = AnarchyEdge(node2.node_id, node2, edge_type="directed")
        assert edge1.node_id == node1.node_id
        assert edge1.edge_type == "undirected"
        assert edge2.node_id == node2.node_id
        assert edge2.edge_type == "directed"

    @given(st.integers(), st.text())
    def test_edge_weakref(self, node_id, edge_type):
        node = AnarchyNode(node_id)
        anarchy = Anarchy()
        edge = AnarchyEdge(node.node_id, node, edge_type=edge_type, edge_holder=anarchy)
        anarchy[node.node_id] = edge
        assert edge.node == node
        del node
        assert edge.node is None
        assert node_id not in anarchy.edges()

    def test_edge_removal(self, node1, anarchy):
        edge = AnarchyEdge(node1.node_id, node1, edge_holder=anarchy)
        anarchy[node1.node_id] = edge
        assert node1.node_id in anarchy.edges()
        edge._remove_edge()
        assert node1.node_id not in anarchy.edges()

    def test_edge_optional_parameters(self, node1):
        edge = AnarchyEdge(node1.node_id, node1, weight=5, color="blue")
        assert edge.weight == 5
        assert edge.color == "blue"

    def test_edge_node(self, node1, anarchy):
        edge = AnarchyEdge(node1.node_id, node1, edge_holder=anarchy)
        assert edge.node == node1

    def test_edge_is_reciprocal(self, node1):
        edge = AnarchyEdge(node1.node_id, node1, reciprocal=True)
        assert edge.is_reciprocal is True
        edge2 = AnarchyEdge(node1.node_id, node1, reciprocal=False)
        assert edge2.is_reciprocal is False
