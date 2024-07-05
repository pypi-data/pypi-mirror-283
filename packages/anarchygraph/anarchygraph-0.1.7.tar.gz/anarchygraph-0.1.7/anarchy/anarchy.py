"""
Anarchy is the primary data structure for managing decentralized edges within a
node.
"""

from typing import TYPE_CHECKING, Dict, Union

from anarchy.edge import AnarchyEdge

if TYPE_CHECKING:
    from anarchy.node import AnarchyNode


class Anarchy(dict):
    """
    Container of decentralized directed edges.

    A dict-like object storing the edges of a node indexed by its node_id.

    Intended to be a component within a Node to manage and contain its
    connections with other Nodes. Nodes can have multiple Anarchy components
    with different names and purposes.

    Parameters
    ----------
    anarchy_name : str, optional
        The name of the anarchy. Defaults to "edges".

    Methods
    -------
    add(node: "AnarchyNode", edge_type: str = "directed") -> None
        Adds an edge to the node.
    remove(node_id: Union[int, str]) -> None
        Removes an edge from the node.
    get(node_id: Union[int, str]) -> "AnarchyEdge":
        Returns the edge of the node by node_id.
    edges() -> Dict[int, "Anarchy"]
        Returns the edges of the node.

    TODO
    ----
    -  Access nodes by traversing edges (by [] or by method)
    """

    def __init__(self, anarchy_name: str = "edges") -> None:
        super().__init__()
        self.name = anarchy_name

    def add(
        self,
        node_id: Union[int, str],
        node: "AnarchyNode",
        edge_type: str = "directed",
        reciprocal: bool = False,
        **kwargs
    ) -> None:
        """
        Adds an edge to the node.

        A reciprocal edge is an edge that is shared with the target node. By
        default edges are non-reciprocal, meaning that the edge is only from
        the source node to the target node.

        Parameters
        ----------
        node_id : Union[int, str]
            The node_id to connect to.
        node : Node
            The node to connect to.
        edge_type : str, optional
            The type of the edge. Defaults to "directed".
        reciprocal : bool, optional
            Whether to add a reciprocal edge. Defaults to False.
        """

        if node_id not in self:
            edge = AnarchyEdge(
                node_id,
                node,
                edge_type=edge_type,
                edge_holder=self,
                reciprocal=reciprocal,
                **kwargs
            )
            self[node_id] = edge

            if reciprocal:
                getattr(node, self.name).add(node_id, node, edge_type, **kwargs)

    def remove(self, node_id: Union[int, str]) -> None:
        """
        Removes an edge from the node.

        Parameters
        ----------
        node_id : Union[int, str]
            The node_id to disconnect from.
        """
        if node_id in self:
            edge = self[node_id]
            if edge.is_reciprocal:
                getattr(edge.node, self.name).remove(edge.node_id)
            del self[node_id]

    def get(self, node_id: Union[int, str]) -> "AnarchyEdge":
        """
        Returns the edge of the node.
        """
        if node_id in self:
            return self[node_id]
        else:
            return None

    def edges(self) -> Dict[int, "Anarchy"]:
        """
        Returns the edges of the node.

        Returns
        -------
        dict
            The edges of the node.
        """
        return {
            node_id: edge for node_id, edge in self.items() if edge.node is not None
        }

    def __call__(self) -> Dict[int, "Anarchy"]:
        return self.edges()
