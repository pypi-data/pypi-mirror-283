"""
The Graph class is a dict-like object to contain nodes of a decentralized network.

A selection of example graphs are provided within the module.

Sample Graphs
-------------
Complete Graph
Sparse Graph
Isolated Graph
Star Graph
Tree Graph
Binary Tree Graph
Cycle Graph
Path Graph
Wheel Graph
Grid Graph
BiPartite Graph
Complete BiPartite Graph
Directed Acyclic Graph
Random Graph
"""

import json
import random
from typing import Optional, Union

from anarchy.node import AnarchyNode
from anarchy.util import configure_cytoscape, convert_to_cytoscape_json

__all__ = [
    "Graph",
    "CompleteGraph",
    "SparseGraph",
    "IsolatedGraph",
    "StarGraph",
    "TreeGraph",
    "BinaryTreeGraph",
    "CycleGraph",
    "PathGraph",
    "WheelGraph",
    "GridGraph",
    "BiPartiteGraph",
    "CompleteBiPartiteGraph",
    "DirectedAcyclicGraph",
    "RandomGraph",
]


class AnarchyGraph(dict):
    """
    Dict-like object to contain nodes of a decentralized network.

    Intended to be an example of how to use the Anarchy component
    to create a graph.

    Can be subclassed to create other types of graphs.

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    graph_type : str
        The type of graph to create.

    TODO
    ----
    - Improve the draw method to not export the graph to a JSON file and then
      import it into cytoscape.
    """

    def __init__(
        self, node_count: int = 100, graph_type: Optional[str] = None
    ) -> None:
        super().__init__()
        self.node_count = node_count
        if graph_type:
            for node in range(node_count):
                self[node] = AnarchyNode(node)
            # self._build_graph(graph_type)

    def _build_graph(self, graph_type: str, node_count: int):
        #! Finish this to work. Need to separate out graph methods.
        """Builds the graph."""
        if graph_type == "complete":
            CompleteGraph(node_count)
        elif graph_type == "sparse":
            SparseGraph(node_count)
        elif graph_type == "isolated":
            IsolatedGraph(node_count)
        elif graph_type == "star":
            StarGraph(node_count)
        elif graph_type == "tree":
            TreeGraph(node_count)
        elif graph_type == "binary_tree":
            BinaryTreeGraph(node_count)
        elif graph_type == "cycle":
            CycleGraph(node_count)
        elif graph_type == "path":
            PathGraph(node_count)
        elif graph_type == "wheel":
            WheelGraph(node_count)
        elif graph_type == "grid":
            GridGraph(node_count)
        elif graph_type == "bipartite":
            BiPartiteGraph(node_count)
        elif graph_type == "complete_bipartite":
            CompleteBiPartiteGraph(node_count)
        elif graph_type == "directed_acyclic":
            DirectedAcyclicGraph(node_count)
        elif graph_type == "random":
            RandomGraph(node_count)
        else:
            raise ValueError(f"Graph type {graph_type} not found.")

    def add_node(self, node_id: Union[int, str], node: "AnarchyNode") -> None:
        """
        Adds a node to the graph indexed by its ID.

        Parameters
        ----------
        node_id : int
            The ID of the node.
        node : Node
            The node to add to the graph.
        """
        self[node_id] = node

    def remove_node(self, node_id: Union[int, str]) -> None:
        """
        Removes a node from the graph from its ID.

        Parameters
        ----------
        node_id : int
            The ID of the node to remove.
        """
        del self[node_id]

    def get_node(self, node_id: Union[int, str]) -> "AnarchyNode":
        """
        Returns a node from the graph by its ID.

        Parameters
        ----------
        node_id : int
            The ID of the node to get.
        """
        return self[node_id]

    def random(self) -> "AnarchyNode":
        """Returns a random node from the graph."""
        return random.choice(list(self.values()))

    @classmethod
    def from_dict(cls, data: dict) -> "AnarchyGraph":
        """Creates a Graph from a dictionary representation."""

        def add_nodes_and_edges(graph, current_node_id, neighbors):
            if current_node_id not in graph:
                graph[current_node_id] = AnarchyNode(current_node_id)
            for neighbor_id, nested_neighbors in neighbors.items():
                if neighbor_id not in graph:
                    graph[neighbor_id] = AnarchyNode(neighbor_id)
                graph.add_edge(current_node_id, neighbor_id)
                add_nodes_and_edges(graph, neighbor_id, nested_neighbors)

        graph = cls(node_count=0)  # Initialize an empty graph
        for node_id, neighbors in data.items():
            add_nodes_and_edges(graph, node_id, neighbors)
        return graph

    def to_dict(self, schema: str = "cytoscape") -> dict:
        """Returns the graph as a dictionary."""
        nodes = []
        edges = []
        for node in self.values():
            nodes.append({"id": node.node_id, "data": node.data})
            for edge in node.edges.values():
                edges.append(
                    {"id": edge.edge_id, "source": node.node_id, "target": edge.node_id}
                )
        return {"elements": {"nodes": nodes, "edges": edges}}

    def to_json(self, schema: str = "cytoscape") -> str:
        """Returns the graph as a JSON string."""
        return json.dumps(self.to_dict(schema))

    def to_adjacency_matrix(self) -> list[list[int]]:
        """Returns the graph as an adjacency matrix."""
        return [
            [int(edge in node.edges) for node in self.values()]
            for edge in self.values()
        ]

    def to_adjacency_list(self) -> dict:
        """Returns the graph as an adjacency list."""
        return {
            node.node_id: [edge.node_id for edge in node.edges.values()]
            for node in self.values()
        }

    def to_edge_list(self) -> list[tuple[int, int]]:
        """Returns the graph as an edge list."""
        return [(edge.node_id, edge.node_id) for edge in self.values()]

    def export(self, filename: str) -> None:
        """Exports the graph to a JSON file."""
        graph_data = self.to_dict()["elements"]
        cytoscape_json = convert_to_cytoscape_json(graph_data)
        with open(filename, "w") as f:
            f.write(cytoscape_json)

    def draw(self):
        """
        Draws the graph using cytoscape.
        """
        self.export("cytoscape_graph.json")
        cytoscapeobj = configure_cytoscape("cytoscape_graph.json")
        return cytoscapeobj

    def has_node(self, node_id: int) -> bool:
        """Returns True if the graph has a node with the given ID, False otherwise."""
        return node_id in self

    @property
    def nodes(self) -> list["AnarchyNode"]:
        """Returns the list of nodes in the graph."""
        return list(self.values())

    @property
    def num_nodes(self) -> int:
        """Returns the number of nodes in the graph."""
        return len(self)

    @property
    def density(self) -> float:
        """
        Returns the density of the graph.

        The density of a graph is the ratio of the number of edges to the maximum
        possible number of edges.
        """
        #! Update formula
        # return len(self.edges) / (len(self.nodes) * (len(self.nodes) - 1))
        return 0


class CompleteGraph(AnarchyGraph):
    """
    Creates a complete graph with n nodes.

    Inherits from Graph class.

    A complete graph is one where all nodes are connected to all other nodes.

        A --- B
        | \ / |
        C --- D

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_complete_graph()

    def _create_complete_graph(self):
        """Creates a complete graph structure."""
        for i in range(self.node_count):
            for j in range(i + 1, self.node_count):
                self[i].edges.add(self[j], edge_type=self.edge_type)
                if self.edge_type == "undirected":
                    self[j].edges.add(self[i], edge_type=self.edge_type)


class SparseGraph(AnarchyGraph):
    """
    Creates a sparse graph with n nodes.

    Inherits from Graph class.

    A sparse graph is one where the number of edges is close to 0 and the number
    of edges is less than the maximum possible number of edges.

        A --- B
        |     |
        C     D
        |
        E

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    sparsity : float
        The sparsity factor of the graph, between 0 and 1. 1 indicates no edges,
        0 indicates all edges.
    """

    def __init__(self, node_count: int, sparsity: float = 0.1) -> None:
        super().__init__(node_count)
        self.sparsity = sparsity
        self._create_sparse_edges()

    def _create_sparse_edges(self):
        """Create sparse edges based on the sparsity factor."""
        max_edges = self.node_count * (self.node_count - 1) // 2
        num_edges = int(max_edges * self.sparsity)
        edges_added = set()

        while len(edges_added) < num_edges:
            node1, node2 = random.sample(self.nodes, 2)
            if (
                node1.node_id != node2.node_id
                and (node1.node_id, node2.node_id) not in edges_added
            ):
                node1.edges.add(node2, edge_type="undirected")
                edges_added.add((node1.node_id, node2.node_id))
                edges_added.add((node2.node_id, node1.node_id))


class IsolatedGraph(AnarchyGraph):
    """
    Creates an isolated graph with n nodes. There are no edges between nodes.

    Inherits from Graph class.

    A isolated graph is one where all nodes are isolated, meaning that there are
    no edges between nodes.

    A   B

    C   D

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)


class StarGraph(AnarchyGraph):
    """
    Creates a star graph with n nodes.

    Inherits from Graph class.

    A star graph is one where all nodes are connected to a single node, the center
    node.

         C
         |
    A -- B -- D
         |
         E

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_star_graph()

    def _create_star_graph(self):
        """Creates a star graph structure."""
        if self.node_count < 2:
            return

        center_node = self[0]
        for node in self.values():
            if node != center_node:
                center_node.edges.add(node, edge_type="directed")
                node.edges.add(center_node, edge_type="directed")


class TreeGraph(AnarchyGraph):
    """
    Creates a tree graph with n nodes.

    Inherits from Graph class.

    A tree graph is one where all nodes are connected to a single node, the center
    node.
    
        A
       / \
      B   C
     /   / \
    D   E   F

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_tree_graph()

    def _create_tree_graph(self):
        """Creates a tree graph structure."""
        if self.node_count < 2:
            return

        for i in range(1, self.node_count):
            parent_id = (i - 1) // 2
            self[i].edges.add(self[parent_id], edge_type="directed")
            self[parent_id].edges.add(self[i], edge_type="directed")


class BinaryTreeGraph(AnarchyGraph):
    """
    Creates a binary tree graph with n nodes.

    Inherits from Graph class.

    A binary tree graph is one where each node has at most two children.
    
          A
         / \
        B   C
       / \ / \
      D  E F  G

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_binary_tree_graph()

    def _create_binary_tree_graph(self):
        """Creates a binary tree graph structure."""
        if self.node_count < 2:
            return

        for i in range(self.node_count):
            left_child_id = 2 * i + 1
            right_child_id = 2 * i + 2

            if left_child_id < self.node_count:
                self[i].edges.add(self[left_child_id], edge_type="directed")
                self[left_child_id].edges.add(self[i], edge_type="directed")

            if right_child_id < self.node_count:
                self[i].edges.add(self[right_child_id], edge_type="directed")
                self[right_child_id].edges.add(self[i], edge_type="directed")


class CycleGraph(AnarchyGraph):
    """
    Creates a cycle graph with n nodes.

    Inherits from Graph class.

    A cycle graph is one where each node is connected to the next node in the cycle,
    and the last node is connected to the first node.

    A --- B
    |     |
    D --- C

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_cycle_graph()

    def _create_cycle_graph(self):
        """Creates a cycle graph structure."""
        if self.node_count < 2:
            return

        for i in range(self.node_count):
            next_node_id = (i + 1) % self.node_count
            self[i].edges.add(self[next_node_id], edge_type="directed")
            self[next_node_id].edges.add(self[i], edge_type="directed")


class PathGraph(AnarchyGraph):
    """
    Creates a path graph with n nodes.

    Inherits from Graph class.

    A path graph is one where each node is connected to the next node in the path.

    A --- B --- C --- D --- E

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_path_graph()

    def _create_path_graph(self):
        """Creates a path graph structure."""
        if self.node_count < 2:
            return

        for i in range(self.node_count - 1):
            self[i].edges.add(self[i + 1], edge_type="directed")
            self[i + 1].edges.add(self[i], edge_type="directed")


class WheelGraph(AnarchyGraph):
    """
    Creates a wheel graph with n nodes.

    Inherits from Graph class.

    A wheel graph is one where each node is connected to the next node in the cycle,
    and the last node is connected to the first node.
    
          A
         /|\
        B-C-D
         \|/
          E
          
    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_wheel_graph()

    def _create_wheel_graph(self):
        """Creates a wheel graph structure."""
        if self.node_count < 4:
            return

        # Connect the central node (node 0) to all other nodes
        for i in range(1, self.node_count):
            self[0].edges.add(self[i], edge_type="directed")
            self[i].edges.add(self[0], edge_type="directed")

        # Connect the outer nodes in a cycle
        for i in range(1, self.node_count):
            next_node_id = (i % (self.node_count - 1)) + 1
            self[i].edges.add(self[next_node_id], edge_type="directed")
            self[next_node_id].edges.add(self[i], edge_type="directed")


class GridGraph(AnarchyGraph):
    """
    Creates a grid graph with n nodes.

    Inherits from Graph class.

    A grid graph is one where each node is connected to the next node in the grid,
    and the last node is connected to the first node.

    A --- B --- C --- D
    |     |     |     |
    E --- F --- G --- H

    Parameters
    ----------
    rows : int
        The number of rows in the grid.
    cols : int
        The number of columns in the grid.
    """

    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        node_count = rows * cols
        super().__init__(node_count)
        self._create_grid_graph()

    def _create_grid_graph(self):
        """Creates a grid graph structure."""
        for row in range(self.rows):
            for col in range(self.cols):
                node_id = row * self.cols + col
                if col < self.cols - 1:
                    right_node_id = node_id + 1
                    self[node_id].edges.add(self[right_node_id], edge_type="directed")
                    self[right_node_id].edges.add(self[node_id], edge_type="directed")
                if row < self.rows - 1:
                    bottom_node_id = node_id + self.cols
                    self[node_id].edges.add(self[bottom_node_id], edge_type="directed")
                    self[bottom_node_id].edges.add(self[node_id], edge_type="directed")


class BiPartiteGraph(AnarchyGraph):
    """
    Creates a bi-partite graph with n nodes.

    Inherits from Graph class.

    A bi-partite graph is one where the nodes are divided into two sets, U and V,
    such that every edge connects a node in U to one in V.

    Set 1: A, B
    Set 2: C, D

    A - C
    A - D
    B - C
    B - D

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_bipartite_graph()

    def _create_bipartite_graph(self):
        """Creates a bi-partite graph structure."""
        mid = self.node_count // 2
        for i in range(mid):
            for j in range(mid, self.node_count):
                self[i].edges.add(self[j], edge_type="directed")
                self[j].edges.add(self[i], edge_type="directed")


class CompleteBiPartiteGraph(AnarchyGraph):
    """
    Creates a complete bi-partite graph with n nodes.

    Inherits from Graph class.

    A complete bi-partite graph is one where all nodes are connected to all other nodes.

    Set 1: A, B
    Set 2: C, D, E

    A - C
    A - D
    A - E
    B - C
    B - D
    B - E

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_complete_bipartite_graph()

    def _create_complete_bipartite_graph(self):
        """Creates a complete bi-partite graph structure."""
        mid = self.node_count // 2
        for i in range(mid):
            for j in range(mid, self.node_count):
                self[i].edges.add(self[j], edge_type="directed")
                self[j].edges.add(self[i], edge_type="directed")


class DirectedAcyclicGraph(AnarchyGraph):
    """
    Creates a directed acyclic graph with n nodes.

    Inherits from Graph class.

    A directed acyclic graph is one where all nodes are connected to all other nodes,
    but there are no cycles.

    A → B → D
    ↓
    C → E

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    """

    def __init__(self, node_count: int) -> None:
        super().__init__(node_count)
        self._create_dag()

    def _create_dag(self):
        """Creates a directed acyclic graph structure."""
        for i in range(self.node_count):
            for j in range(i + 1, self.node_count):
                self[i].edges.add(self[j], edge_type="directed")


class RandomGraph(AnarchyGraph):
    """
    Creates a random graph with n nodes.

    Inherits from Graph class.

    The graph is created by connecting nodes randomly, but with a probability of
    sparsity that a node is isolated.

    Parameters
    ----------
    node_count : int
        The number of nodes in the graph.
    edge_density : float
        The probability of an edge between any two nodes.
    sparsity : float
        The probability of a node being isolated.
    """

    def __init__(
        self, node_count: int = 10, edge_density: float = 0.2, sparsity: float = 0.1
    ) -> None:
        super().__init__(node_count)

        eligible_count = int(node_count * (1 - sparsity))
        max_edges = int((node_count * (node_count - 1)) * edge_density)
        eligible_nodes = random.sample(list(self.values()), eligible_count)
        count = 0
        while count <= max_edges:
            node1, node2 = random.sample(eligible_nodes, 2)
            node1.edges.add(node2, edge_type="directed")
            count += 1
