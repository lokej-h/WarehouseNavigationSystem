# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 19:30:24 2021

@author: Student
"""
from typing import Tuple, Set, Dict, List


class PathGraph:
    """
    Graph representation of the warehouse for TSP algorithms.
    """
    class Edge:
        """
        Edge in the PathGraph
        """
        path: List[Tuple[int, int]]
        cost: int
        
        def __init__(self, path, cost):
            self.path = path
            self.const = cost

    class Node:
        """
        Node in the PathGraph
        Represents a shelf position
        """
        position: Tuple[int, int]

        def __init__(self, coordinate: Tuple[int, int]):
            self.position = coordinate

    # set of all nodes
    nodes: Set[Node]
    # edge lookup by start and end. Sparse due to symmetry.
    _edges: Dict[Node, Dict[Node, Edge]]

    def _get_edge_swappable(self, a: Node, b: Node) -> Edge:
        if self._edges.get(a).get(b) is not None:
            return self._edges.get(a).get(b)
        return self._edges.get(b).get(a)

    def cost(self, u: Node, v: Node) -> int:
        edge = self._get_edge_swappable(u, v)
        return edge.cost
    
    @classmethod
    def get_node(coord: Tuple[int, int]) -> Node:
        return PathGraph.Node(coord)

    def add_node(self, coordinate: Tuple[int, int]) -> None:
        start = self.Node(coordinate)
        self._edges[start] = dict()
        for node in self.nodes:
            # find path and cost to node from all current nodes
            path = list()
            cost = 0
            self._edges[start][node] = self.Edge(path, cost)
        self.nodes.add(start)
        
    def get_warehouse_steps(self, path: List[Node]) -> List[Tuple[int, int]]:
        # need to get the intermediate steps between two nodes
        pathiter = iter(path)
        curr_node = next(pathiter)
        next_node = next(pathiter)
        full_path = list()
        for curr_node, next_node in zip(path, [node for node in path[1:]]):
            inter_path = self._get_edge_swappable(curr_node, next_node).path
            full_path.extend(inter_path)
            
    def get_neighbors(self, u: Node) -> Set[Node]:
        # difference a tuple as it is faster that diff'ing a set
        return self.nodes.difference((u,))
