from typing import Dict, List, Tuple
import logging
from .path_graph import PathGraph
from .algo_NN import NN

# =============================================================================
# You should probably put these in seperate files for your own sanity
# =============================================================================
LOGGER = logging.getLogger(__name__)


def find_item_list_path(
    start_coord: Tuple[int, int], items: List[int], shelves: Dict[str, Tuple[int, int]],
) -> List[Tuple[int, int]]:
    """
    Find a path from the start coordinates to each item in the list.

    Parameters
    ----------
    start_coord : Tuple[int, int]
        The coordinates to start pathing.
    items : List[int]
        The list of items to navigate.
    shelves : Dict[str, List[int]]
        Shelf lookup table to avoid walking into shelves.

    Raises
    ------
    Exception
        Passes up exception from 'muck_about'.

    Returns
    -------
    path: List[Tuple[int, int]]
        Returns a path from the start coordinates to each item in the list.

    """
    graph = PathGraph()

    # add start node
    graph.add_node(start_coord)
    # add all other item's shelf coordinate as a node
    for item in items:
        graph.add_node(shelves[item])

    # run algorithm

    return NN(start_coord, graph)


def prep_data_for_computation(
    arr: List[List[str]], shelves: Dict[str, Tuple[int, int]]
) -> None:
    # =============================================================================
    #     idk what data type you want to use to easily work with the warehouse
    #     so for now main is just passing Set[Shelf] whenever someone needs a Warehouse
    # =============================================================================
    for key in shelves:
        arr[shelves[key][0] + 1][shelves[key][1] + 1] = "X"
