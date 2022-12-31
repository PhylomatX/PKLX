import networkx as nx
from collections import deque
from typing import Callable


def bfs(graph: nx.Graph, source: str, stop_condition: Callable = None) -> nx.Graph:
    visited = set([source])
    if stop_condition is None:
        stop_condition = lambda node: False
    undirected_graph = graph.to_undirected()
    neighbors = undirected_graph.neighbors(source)
    queue = deque([neighbor for neighbor in neighbors])
    while queue:
        node = queue.pop()
        visited.add(node)
        if not stop_condition(node):
            neighbors = undirected_graph.neighbors(node)
            queue.extendleft([neighbor for neighbor in neighbors if neighbor not in visited])
    return graph.subgraph(visited)
