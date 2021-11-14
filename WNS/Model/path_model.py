from typing import Dict, List, Tuple
import logging
from .path_helpers import find_item
from .algo_go_until import make_go_until_path
from ..View.view_helpers import coord_to_human

# =============================================================================
# You should probably put these in seperate files for your own sanity
# =============================================================================
LOGGER = logging.getLogger(__name__)


class POIGraph:
    pass


class Warehouse:
    pois = POIGraph()
    pass


def find_item_list_path(
    start_coord: Tuple[int, int], items: List[int], shelves: Dict[str, List[int]],
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
    # ignore list, we are only grabbing the first item
    item = items[0]

    # make a shelf lookup table, remembering to increment the shelves by 1
    # for the outside border
    shelf_lookup = set(shelves.values())

    # get where the item is
    end_coords = find_item(item, shelves)
    LOGGER.debug(f"shelf access {coord_to_human(end_coords)}")
    # and check if a shelf is to the right
    if (end_coords[0] + 1, end_coords[1]) not in shelf_lookup:
        end_coords = (end_coords[0] + 1, end_coords[1])
    # check if a shelf is above?
    elif (end_coords[0], end_coords[1] + 1) not in shelf_lookup:
        end_coords = (end_coords[0], end_coords[1] + 1)
    # and also left and down
    elif (end_coords[0] - 1, end_coords[1]) not in shelf_lookup:
        end_coords = (end_coords[0] - 1, end_coords[1])
    elif (end_coords[0], end_coords[1] - 1) not in shelf_lookup:
        end_coords = (end_coords[0], end_coords[1] - 1)
    else:
        raise Exception("We can't access this shelf!")
    LOGGER.debug(f"can access shelf from {coord_to_human(end_coords)}")

    # make a basic path

    path = make_go_until_path(start_coord, shelf_lookup, end_coords)
    return path



def prep_data_for_computation(
    arr: List[List[str]], shelves: Dict[str, Tuple[int, int]]
) -> None:
    # =============================================================================
    #     idk what data type you want to use to easily work with the warehouse
    #     so for now main is just passing Set[Shelf] whenever someone needs a Warehouse
    # =============================================================================
    for key in shelves:
        arr[shelves[key][0] + 1][shelves[key][1] + 1] = "X"
    # =============================================================================
    for key in shelves:
        arr[shelves[key][0] + 1][shelves[key][1] + 1] = "X"
