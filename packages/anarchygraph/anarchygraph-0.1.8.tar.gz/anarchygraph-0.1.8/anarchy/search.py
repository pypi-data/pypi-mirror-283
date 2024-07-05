"""
Since this is a decentralized graph approach, there are different considerations 
and results from common graph search algorithms.

If the graph is directed, the completeness of the returning subgraph does not 
consider incoming edges into a node, only edges originating from a node.

It's possible to work around this limitation by storing the state of the graph 
and performing a search from a holistic level

TODO
----
- different return types like node_count, edge_count, state, subgraph, etc.
- random walk algorithm
- a* algorithm
- dijkstra algorithm
"""

from collections import deque
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from anarchy.node import AnarchyNode


def explore(entry_node: "AnarchyNode", strategy: str = "bfs") -> dict:
    """
    Function to search through a decentralized graph through an entry point.

    By selected strategy until all connected nodes have been reached.

    Returns a dictionary of nodes and edges. {node_id: {neighbor_id: {}}}

    TODO
    ----
    - Add max hops
    - Add max depth
    """
    if strategy == "bfs":
        return bfs(entry_node)
    elif strategy == "dfs":
        return dfs(entry_node)
    else:
        raise ValueError("Invalid strategy")


def bfs(entry_node):
    """
    Breadth-first search through an entry point node.
    Returns the structure of the subgraph headed by the entry node.

    BFS explores all neighbors of a node before moving to the next level of nodes.
    Each node maintains a queue of neighbors to visit.
    """
    graph_structure = {entry_node.node_id: {}}
    visited = set(
        [entry_node.node_id]
    )  # Initialize the visited set with the entry node
    queue = deque([(entry_node, graph_structure[entry_node.node_id])])

    while queue:
        current_node, current_structure = queue.popleft()

        for edge in current_node.edges.values():
            neighbor = edge.node  # Access the node connected by the edge
            if neighbor.node_id not in visited:
                visited.add(neighbor.node_id)
                current_structure[neighbor.node_id] = {}
                queue.append((neighbor, current_structure[neighbor.node_id]))

    return graph_structure


def dfs(entry_node: "AnarchyNode") -> dict:
    """
    Depth-first search through an entry point node.
    Returns the structure of the subgraph headed by the entry node.

    DFS explores as far as possible along a branch before backtracking.
    """
    graph_structure = {entry_node.node_id: {}}
    visited = set()

    def dfs_helper(current_node, current_structure):
        visited.add(current_node.node_id)

        for edge in current_node.edges.values():
            neighbor = edge.node  # Access the node connected by the edge
            if neighbor.node_id not in visited:
                current_structure[neighbor.node_id] = {}
                dfs_helper(neighbor, current_structure[neighbor.node_id])

    dfs_helper(entry_node, graph_structure[entry_node.node_id])

    return graph_structure


def dijkstra(start_node: "AnarchyNode") -> dict:
    """
    Dijkstra's algorithm through an entry point node.
    Returns the shortest path to all connected nodes.

    Dijkstra's algorithm is a greedy algorithm in graph theory that finds the
    shortest path between two nodes. It uses a priority queue to select the
    node with the lowest distance from the start node.
    """
    raise NotImplementedError("Dijkstra is not implemented")


def a_star(
    start_node: "AnarchyNode", goal_node: "AnarchyNode", heuristic: Callable
) -> list["AnarchyNode"]:
    """
    A* algorithm through an entry point node.
    Returns the shortest path to all connected nodes.

    A* is a heuristic search algorithm that uses a priority queue to select the
    node with the lowest cost from the start node.
    """
    raise NotImplementedError("A* is not implemented")


def reconstruct_path(node: "AnarchyNode") -> list["AnarchyNode"]:
    """
    Reconstruct the path from the goal node to the start node.
    """
    raise NotImplementedError("Reconstruct path is not implemented")


def random_walk(start_node: "AnarchyNode", steps: int) -> list["AnarchyNode"]:
    """
    Random walk through an entry point node.
    Returns the path taken to all connected nodes.

    Random walk is a random search algorithm that explores the graph by
    randomly selecting a neighbor node.
    """
    raise NotImplementedError("Random walk is not implemented")
