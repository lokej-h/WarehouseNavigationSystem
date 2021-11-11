# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 03:27:50 2021

@author: Student
"""

from typing import Tuple, List
from queue import Queue

from ..View.warehouse_view import g as view

def find_item_list_path_bfs(
    start_coord: Tuple[int, int], pickup_item: Tuple[int, int], 
) -> Tuple[List[Tuple[int, int]], int]:
    """
    Find a path from the start coordinates to each item in the list.

    Parameters
    ----------
    start_coord : Tuple[int, int]
        The coordinates to start pathing.
    pickup_item: Tuple[int, int]
        item id to pickup
    shelves : Dict[str, List[int]]
        Shelf lookup table to avoid walking into shelves.

    Returns
    -------
    path: List[Tuple[int, int]], int
        Returns a path from the start coordinates to item passed in. Also returns number of steps taken to get to item. 

    """

    visited = []
    for i in range(0, len(view.warehouse_array)):
        new = []
        for j in range(0, len(view.warehouse_array[0])):
            new.append(False)
        visited.append(new)

    visited[start_coord[0]][start_coord[1]] = True
    nodes_left_in_layer = 1
    nodes_in_next_layer = 0
    move_count = 0
    dr = [-1, +1, 0, 0]
    dc = [0, 0, +1, -1]
    reached_end = False

    p = []
    p.append(start_coord)
    q = Queue()
    q.put((start_coord[0], start_coord[1], p))

    while q.qsize() > 0:
        r = q.get()
        # print("r: ", r, " c: ", c)
        if(r[0] == pickup_item[0] and r[1] == pickup_item[1]):
            reached_end = True
            break
        # explore neighbors starts
        for i in range(0, 4):
            rr = r[0] + dr[i]
            cc = r[1] + dc[i]

            if rr < 0 or cc < 0:
                continue
            if rr >= len(view.warehouse_array) or cc >= len(view.warehouse_array[0]):
                continue

            if visited[rr][cc] == True:
                continue
            if view.warehouse_array[rr][cc] == "X" and (rr != pickup_item[0] or cc != pickup_item[1]):
                continue

            nl = []
            for i in range(len(r[2])):
                nl.append(r[2][i])
            nl.append((rr, cc))
            q.put((rr, cc, nl))
            # print("apended: ", rr, " and ", cc)
            visited[rr][cc] = True
            nodes_in_next_layer = nodes_in_next_layer + 1
        # explore neighbors ends

        nodes_left_in_layer = nodes_left_in_layer - 1
        if nodes_left_in_layer == 0:
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count = move_count + 1
    if reached_end:
        print(r[2])
        # return r[2], move_count
        return r[2], len(r[2])

    return -1