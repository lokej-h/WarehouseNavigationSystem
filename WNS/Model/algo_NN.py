# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 20:32:39 2021

@author: Student
"""

from typing import Tuple
import logging
from .path_graph import PathGraph

LOGGER = logging.getLogger(__name__)

def NN(start_coord: Tuple[int, int], graph: PathGraph):
    # NN
    start_node = graph.get_node(start_coord)
    node_path = list()
    node_path.append(start_node)
    curr_node = start_node
    for _ in range(len(graph.nodes)-1):
        nearest_neighbor = min(graph.get_neighbors(curr_node).difference(
            node_path), key=lambda v: graph.cost(curr_node, v))
        node_path.append(nearest_neighbor)
        LOGGER.debug(f"\tCost: {graph.cost(curr_node, nearest_neighbor)}")
    
    node_path.append(start_node)
    return graph.get_warehouse_steps(node_path)