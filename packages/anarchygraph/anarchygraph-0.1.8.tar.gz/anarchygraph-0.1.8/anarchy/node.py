"""
Node stores edges in a dictionary where the key is the other node's id and the 
value is the Edge object that has the reference to the node.
"""

from typing import Any


class AnarchyNode:
    """
    A node is a self-contained and decentralized entity in a graph that stores
    its own data and edges.

    Intended to be more of a placeholder node, ideally used as a base class with
    specific implementations of nodes.

    Attributes
    ----------
    node_id : int
        The unique identifier of the node.
    data : Any, optional
        The data to be stored in the node. Defaults to None.
    edges : dict[int, AnarchyEdge]
        The edges connected to the node.

    TODO
    ----
    - Improve the explore method
    """

    def __init__(self, node_id: int, data: Any = None) -> None:
        #! fix this
        from anarchy import Anarchy

        self.node_id = node_id
        self.data = data
        self.edges = Anarchy()

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        """
        return (
            f"Node({self.node_id}, Data: {self.data}, Edges: {list(self.edges.keys())})"
        )

    def __eq__(self, other_id: "AnarchyNode") -> bool:
        return self.node_id == other_id

    def __hash__(self) -> int:
        return hash(self.node_id)

    def __ne__(self, other_id: "AnarchyNode") -> bool:
        return self.node_id != other_id
