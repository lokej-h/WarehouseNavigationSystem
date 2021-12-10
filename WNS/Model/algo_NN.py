# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 20:11:23 2021

@author: Student
"""
import time
from collections import deque, defaultdict
from functools import cached_property
from itertools import chain, permutations
from typings import Dict, Tuple, List, Set
from ..View.warehouse_view import find_item_list_path_bfs

Coordinate = Tuple[int, int]


def get_paths_and_costs(
    items_to_visit: List[int], shelves: Dict[str, Coordinate]
) -> Tuple[
    Dict[Tuple[Coordinate, Coordinate], List[Coordinate]],
    Dict[Set[Tuple[Coordinate, Coordinate]], int],
]:
    """
    from main.py
    creates a cost_table
        key: set {A, B} where A and B are the two nodes the path starts/ends
        value: cost of the path between A and B

        Why a set as a key?
        The set allows us to map both A,B and B,A to the same value which will
        save some space.
        We could do something similar with path map, but that would take
        adding a check to reverse the path before returning.

    and a path mapping
        key: tuple (A, B) where A is the start and B is the end
        value: list of tuple coordinates to tell how to get from A to B
    """
    path_map = dict()
    cost_table = dict()

    # we use the permutations function to go through every permutation of
    # shelves i.e. AB and BA, the two is to limit each output to 2 items
    for start, end in permutations(items_to_visit, 2):
        path, cost = find_item_list_path_bfs(shelves[str(start)], end, shelves)
        key = (start, end)
        path_map[key] = path
        cost_table[set(key)] = cost
    return path_map, cost_table


def get_all_items_where_we_are(location: Coordinate, shelves: Dict[str, Coordinate]):
    """returns list of all PIDs at a location"""
    inverted_shelves = get_inverted_dict(shelves)
    return inverted_shelves[location]


def get_nearest_neighbor(
    node: Coordinate,
    available_neighbors: Set[Coordinate],
    cost_table: Dict[Set[Tuple[Coordinate, Coordinate]], int],
):
    """gets the nearest neighbor to node"""
    return min(available_neighbors, key=lambda v: cost_table[node, v])


def get_lowest_cost_path():
    pass


# this is only computed once thanks to @cache
@cached_property
def get_inverted_dict(d):
    """get the inverted dictionary of d, if values of d have duplicates,
    appended to list"""
    inverted = defaultdict(list)
    for k, v in d.items():
        inverted[v].append(k)
    return inverted


def raise_if_timeout(start_time: float, t_o: int):
    end_time = time.perf_counter()
    if end_time - start_time > t_o:
        print("nearest neighbor timed out")
        raise Exception("Timeout!")


def get_NN_path(
    start: Coordinate,
    true_start: Coordinate,
    true_end: Coordinate,
    shelves: Dict[str, Coordinate],
    the_places_youll_go: Set[Coordinate],
    timeout: float,
    path_map: Dict[Tuple[Coordinate, Coordinate], List[Coordinate]],
    cost_table: Dict[Set[Tuple[Coordinate, Coordinate]], int],
) -> Tuple[List[Coordinate], int]:
    """
    returns a single NN path given a start and end
    this is where we force start to come after end (see nearest_neighbor)
    """

    the_places_you_can_go = the_places_youll_go - {start}

    the_places_youve_been = [start]

    where_you_are = start
    cost = 0

    for _ in range(len(the_places_you_can_go)):
        nearest_neighbor = get_nearest_neighbor(
            where_you_are,
            the_places_you_can_go - set(the_places_youve_been),
            cost_table,
        )

        cost += cost_table[{where_you_are, nearest_neighbor}]

        where_you_are = nearest_neighbor

        the_places_youve_been.append(where_you_are)

        # force start to be after end, cost doesn't matter here since it
        # does not affect minimum cost (constant applied to all paths)
        # and should not be factored in the output of the cost
        if where_you_are is true_end:
            where_you_are = true_start
            the_places_youve_been.append(where_you_are)
    # add the last leg home
    # we don't need to add the start back to the places youve been because
    # that would end up with a duplicate node which we'd only remove later
    cost += cost_table[{where_you_are, start}]
    return the_places_youve_been, cost


def get_rotated_NN_path(
    start: Coordinate,
    true_start: Coordinate,
    true_end: Coordinate,
    shelves: Dict[str, Coordinate],
    shelves_to_visit: Set[Coordinate],
    timeout: float,
    path_map: Dict[Tuple[Coordinate, Coordinate], List[Coordinate]],
    cost_table: Dict[Set[Tuple[Coordinate, Coordinate]], int],
    start_node: Coordinate,
) -> Tuple[List[Coordinate], int]:
    """
    gets the NN path and returns the rotated version for you
    requires the true start node for rotation
    """
    path, cost = get_NN_path(
        start,
        true_start,
        true_end,
        shelves,
        shelves_to_visit,
        timeout,
        path_map,
        cost_table,
    )
    route = deque(path)
    route.rotate(-route.index(start_node))
    return list(route), cost


def get_shelves_to_visit(
    shelves: Dict[str, Coordinate], items_to_visit: List[int]
) -> Set[Coordinate]:
    """
    get the coordinates of shelves to visit
    """
    return {shelves[item] for item in items_to_visit}


def nearest_neighbor(
    shelves: Dict[str, Coordinate],
    items_to_visit: List[int],
    timeout: float,
    start_node: Coordinate,
    end_node: Coordinate,
) -> Tuple[List[Coordinate], List[Tuple[List[Coordinate], str]], List[int], int]:
    """
    given the items to visit and the shelves in the warehouse, find the shortest
    tour given by NN

    Define:
        node: start/end or shelves with items to pick up

    Need helper functions to:
        find nearest neighbor to any node
        find path and cost to any node from any node
        find lowest cost of the nearest neighbor paths
        calculate nearest neighbor path from every node
        force start to come after any instance of end:
            to do this, we include end in our avaliable node to nearest neighbor
            if the nearest nighbor is end, we force start to be the next node
        rotate found paths so they start at 'start' and end at 'end'
        get all items on a shelf
    """
    start_time = time.perf_counter()
    path_map, cost_table = get_paths_and_costs(items_to_visit, shelves)

    shelves_to_visit = get_shelves_to_visit(shelves, items_to_visit)
    places_to_start = {start_node, end_node} | shelves_to_visit

    for starting_position in places_to_start:
        coordinate_path, cost = get_rotated_NN_path(
            starting_position,
            start_node,
            end_node,
            shelves,
            shelves_to_visit,
            timeout,
            path_map,
            cost_table,
            start_node,
        )
