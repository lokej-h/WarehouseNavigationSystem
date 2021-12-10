# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 20:11:23 2021

@author: Student
"""
import time
from collections import deque, defaultdict
from functools import lru_cache, partial
from itertools import permutations, chain, tee
from typing import Dict, Tuple, List, Set, Callable
from ..View.warehouse_view import find_item_list_path_bfs

Coordinate = Tuple[int, int]


class g:
    """internal globals"""

    # the start time of NN
    start_time: float

    # the timeout in seconds
    timeout: float


# https://docs.python.org/3.8/library/itertools.html?highlight=flatten#itertools-recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


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
    for start, end in permutations(items_to_visit + ["start", "end"], 2):
        path, cost = go_to_next_without_shelf(shelves[str(start)], end, shelves)
        key = (shelves[str(start)], shelves[str(end)])
        path_map[key] = path
        cost_table[frozenset(key)] = cost
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
    return min(available_neighbors, key=lambda v: cost_table[frozenset((node, v))])


def get_lowest_cost_path(
    pathmaker: Callable[[Coordinate], Tuple[List[Coordinate], int]],
    starting_places: Set[Coordinate],
):
    """
    get the lowest cost path
    we do this as efficiently as we can using iterators
    create a starmap to map function calls to arguments
    then run an argmin on the iterator
    """
    pathcosts = map(pathmaker, starting_places)
    try:
        return min(pathcosts, key=lambda pathcost: pathcost[1])
    except TimeoutError as e:
        print(e.message)
        # in the very unlikely event we timeout here we have to return something
        return next(pathcosts)


# this is only computed once thanks to @cache
# @lru_cache
def get_inverted_dict(d):
    """get the inverted dictionary of d, if values of d have duplicates,
    appended to list"""
    inverted = defaultdict(list)
    for k, v in d.items():
        inverted[v].append(k)
    return inverted


def raise_if_timeout():
    end_time = time.perf_counter()
    if end_time - g.start_time > g.timeout:
        raise TimeoutError("Nearest Neighbor timed out, returning best found.")


def get_NN_path(
    start: Coordinate,
    true_start: Coordinate,
    true_end: Coordinate,
    shelves: Dict[str, Coordinate],
    the_places_youll_go: Set[Coordinate],
    path_map: Dict[Tuple[Coordinate, Coordinate], List[Coordinate]],
    cost_table: Dict[Set[Tuple[Coordinate, Coordinate]], int],
) -> Tuple[List[Coordinate], int]:
    """
    returns a single NN path given a start and end
    this is where we force start to come after end (see nearest_neighbor)
    """
    the_places_you_can_go = the_places_youll_go - {start, true_start} | {true_end}
    the_places_youve_been = [start]

    where_you_are = start
    cost = 0

    # -1 since we don't need all the iterations if start is at our end
    for _ in range(len(the_places_you_can_go) - (1 if start == true_end else 0)):
        nearest_neighbor = get_nearest_neighbor(
            where_you_are,
            the_places_you_can_go - set(the_places_youve_been),
            cost_table,
        )

        cost += cost_table[frozenset((where_you_are, nearest_neighbor))]

        where_you_are = nearest_neighbor

        the_places_youve_been.append(where_you_are)

        # force start to be after end, cost doesn't matter here since it
        # does not affect minimum cost (constant applied to all paths)
        # and should not be factored in the output of the cost
        if where_you_are is true_end:
            where_you_are = true_start
            the_places_youve_been.append(where_you_are)
        raise_if_timeout()
    # add the last leg home
    # we don't need to add the start back to the places youve been because
    # that would end up with a duplicate node which we'd only remove later
    cost += cost_table[frozenset((where_you_are, start))]
    return the_places_youve_been, cost


def get_rotated_NN_path(
    start: Coordinate,
    true_start: Coordinate,
    true_end: Coordinate,
    shelves: Dict[str, Coordinate],
    shelves_to_visit: Set[Coordinate],
    path_map: Dict[Tuple[Coordinate, Coordinate], List[Coordinate]],
    cost_table: Dict[Set[Tuple[Coordinate, Coordinate]], int],
) -> Tuple[List[Coordinate], int]:
    """
    gets the NN path and returns the rotated version for you
    requires the true start node for rotation
    """
    path, cost = get_NN_path(
        start, true_start, true_end, shelves, shelves_to_visit, path_map, cost_table,
    )
    route = deque(path)
    # needs if just in case start and end are same to ensure correct rotation
    route.rotate(-route.index(true_start) - (1 if true_start == true_end else 0))
    return list(route), cost


def get_shelves_to_visit(
    shelves: Dict[str, Coordinate], items_to_visit: List[int]
) -> Set[Coordinate]:
    """
    get the coordinates of shelves to visit
    """
    return {shelves[str(item)] for item in items_to_visit}


def go_to_next_without_shelf(start, endPID, shelves):
    """going into the shelf deletes it"""
    # find path and cost to item
    p, c = find_item_list_path_bfs(start, endPID, shelves)
    # we don't want to go into the shelf
    p.pop()
    # we don't walk into the shelf
    c = c - 1
    return p, c


def get_path_from_ordered_coordinate_list(
    path_steps: List[Coordinate],
    shelves: Dict[str, Coordinate],
    path_map: Dict[Tuple[Coordinate, Coordinate], List[Coordinate]],
) -> Tuple[List[Coordinate], List[Tuple[List[Coordinate], str]], List[int]]:
    """
    recover the steps in order to walk in the warehouse
    we need 3 versions:
        flat version
        piecewise + a PID of the shelf we are targeting
        list of ordered PID
    """
    inverted_shelves = get_inverted_dict(shelves)

    flat_path = list()
    piecewise_with_target = list()
    ordered_PIDs = list()

    # because of the way we handle 4 side pickup, a path_map is always invalid
    current = path_steps[0]
    # don't include end in the pairwise iteration as we have a special case
    for next_node in path_steps[1:-2]:
        # path_to = path_map[current, next_node]
        path_to, _ = go_to_next_without_shelf(
            current, inverted_shelves[next_node][0], shelves
        )
        current = path_to[-1]
        PIDs_targeted = inverted_shelves[next_node]

        flat_path.extend(path_to)
        piecewise_with_target.append((path_to, PIDs_targeted[0]))
        ordered_PIDs.extend(PIDs_targeted)
    # go to end
    path_to, _ = go_to_next_without_shelf(current, "end", shelves)
    # using -1 flag for end as in main.py
    flat_path.extend(path_to)
    piecewise_with_target.append((path_to, -1))

    return flat_path, piecewise_with_target, ordered_PIDs


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
    g.start_time = time.perf_counter()
    g.timeout = timeout
    path_map, cost_table = get_paths_and_costs(items_to_visit, shelves)

    shelves_to_visit = get_shelves_to_visit(shelves, items_to_visit)
    places_to_start = {start_node, end_node} | shelves_to_visit

    # create a much simpler version of the function for easier calls
    get_started_rotated_NN_path = partial(
        get_rotated_NN_path,
        true_start=start_node,
        true_end=end_node,
        shelves=shelves,
        shelves_to_visit=shelves_to_visit,
        path_map=path_map,
        cost_table=cost_table,
    )

    min_path, min_cost = get_lowest_cost_path(
        get_started_rotated_NN_path, places_to_start
    )

    # recover actual path
    return (
        *get_path_from_ordered_coordinate_list(min_path, shelves, path_map),
        min_cost,
    )
