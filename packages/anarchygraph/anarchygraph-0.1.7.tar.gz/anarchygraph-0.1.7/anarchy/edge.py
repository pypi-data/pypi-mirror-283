"""
Edge will contain the node reference and any other pertinent information.

An edge is a connection between two nodes and can be any type of edge.

A reciprocal edge is an edge that is shared with the target node. By default
edges are non-reciprocal, meaning that the edge is only from the source node
to the target node.
"""

import uuid
import weakref
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from anarchy.anarchy import Anarchy
    from anarchy.node import AnarchyNode


class AnarchyEdge:
    """
    An Edge is a connection between two nodes. Intended to be an object in an
    Anarchy component.

    A weakref is used to reference the node. This allows the node to be garbage
    collected when it is deleted, as well as any edges that reference it.

    Parameters
    ----------
    node_id : int, str
        The node_id of the node this edge is connected to.
    node : Node
        The node this edge is connected to.
    edge_type : str, optional
        The type of the edge. Defaults to "directed".
    edge_holder : Anarchy, optional
        An Anarchy component that contains this edge. Used to remove the edge
        from the dictionary when the node is deleted.
    **kwargs : dict
        Additional attributes to add to the edge.

    Attributes
    ----------
    node_ref : weakref.ref
        A weakref to the node. Deleting the node will remove the edge.
    edge_type : str
        See parameter.
    node_id : int
        The node_id of the node this edge is connected to.
    edge_holder : Anarchy
        See parameter.
    finalizer : weakref.finalizer
        A weakref finalizer that will remove the edge from the Anarchy component
        when the node is deleted.

    Properties
    ----------
    is_reciprocal : bool
        Whether the edge is reciprocal.
    """

    def __init__(
        self,
        node_id: Union[int, str],
        node: "AnarchyNode",
        edge_type: str = "directed",
        edge_holder: Optional["Anarchy"] = None,
        reciprocal: bool = False,
        **kwargs,
    ) -> None:
        self.node_ref = weakref.ref(node)
        self.edge_type = edge_type
        self.node_id = node_id
        self.edge_id = str(uuid.uuid4())
        self.edge_holder = edge_holder
        self.reciprocal = reciprocal
        if edge_holder is not None:
            self.finalizer = weakref.finalize(node, self._remove_edge)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _remove_edge(self) -> None:
        """
        Removes the edge from the edge collection when the node is deleted.
        """
        if self.edge_holder is not None:
            self.edge_holder.remove(self.node_id)

    @property
    def node(self) -> Optional["AnarchyNode"]:
        """
        Returns
        -------
        Node or None
            The node this edge is connected to.
        """
        return self.node_ref()

    @property
    def is_reciprocal(self) -> bool:
        """
        Returns
        -------
        bool
            Whether the edge is reciprocal.
        """
        return self.reciprocal

    def __repr__(self) -> str:
        return f"Edge(node: {self.node_id}, type: {self.edge_type})"
