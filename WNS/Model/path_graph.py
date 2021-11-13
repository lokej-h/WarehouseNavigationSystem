# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 19:30:24 2021

@author: Student
"""
from typing import Tuple, Set, Dict, List
from collections import defaultdict

from .algo_bfs_flood import find_item_list_path_bfs


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
            self.cost = cost

    class Node:
        """
        Node in the PathGraph
        Represents a shelf position
        """
        position: Tuple[int, int]

        def __init__(self, coordinate: Tuple[int, int]):
            self.position = coordinate
            
        def __hash__(self):
            return hash(self.position)
        
        def __eq__(self, other):
            if isinstance(other, PathGraph.Node):
                return self.position == other.position
            return NotImplemented

    # set of all nodes
    nodes: Set[Node]
    # edge lookup by start and end. Sparse due to symmetry.
    _edges: Dict[Node, Dict[Node, Edge]]
    
    def __init__(self):
        self.nodes = set()
        self._edges = dict() #defaultdict(defaultdict)

    def _get_edge_swappable(self, a: Node, b: Node) -> Edge:
        if self._edges.get(a) is not None and self._edges.get(a).get(b) is not None:
            return self._edges.get(a).get(b)
        # if it was from the opposite side, reverse path
        edge = self._edges.get(b).get(a)
        edge.path.reverse()
        return edge

    def cost(self, u: Node, v: Node) -> int:
        edge = self._get_edge_swappable(u, v)
        return edge.cost

    @classmethod
    def get_node(cls, coord: Tuple[int, int]) -> Node:
        return PathGraph.Node(coord)

    def add_node(self, coordinate: Tuple[int, int]) -> None:
        start = self.Node(coordinate)
        if len(self.nodes) != 0:
            self._edges[start] = dict()
            for node in self.nodes:
                # find path and cost to node from all current nodes
                path, cost = find_item_list_path_bfs(start.position,
                                                     node.position)
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
            full_path.append(inter_path)
        return full_path

    def get_neighbors(self, u: Node) -> Set[Node]:
        # difference a tuple as it is faster that diff'ing a set
        return self.nodes.difference((u,))
