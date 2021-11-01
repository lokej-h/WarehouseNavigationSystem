from typing import Dict, List, Tuple, Set, Optional
import logging
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


def find_item(item: str, shelves: Dict[str, Tuple[int, int]]) -> Tuple[int, int]:
    """
    Lookup the item's coordinates from the shelf lookup table.

    Parameters
    ----------
    item : str
        Item PID to lookup.
    shelves : Dict[int, List[Tuple[int, int]]]
        Shelf lookup table.

    Returns
    -------
    Tuple[int, int]
        The item's shelf coordinates.

    """
    return (shelves[item][0], shelves[item][1] + 1)


def make_step(direction: int, start_coord: Tuple[int, int], i: int) -> Tuple[int, int]:
    """
    Make a new coordinate

    Parameters
    ----------
    direction : int
        Use the module globals HORIZ and VERT to describe horizontal or
        vertical movement.
    start_coord : Tuple[int, int]
        Coordinate to start movement.
    i : int
        The next horizontal or vertical index.

    Returns
    -------
    Tuple[int, int]
        The new coordinate.

    """
    next_step = list(range(2))
    next_step[(direction + 1) % 2] = start_coord[(direction + 1) % 2]
    next_step[direction] = i
    return tuple(next_step)


def safe_make_step(
    direction, start_coord: Tuple[int, int], i, shelf_lookup: Set[Tuple[int, int]]
) -> Optional[Tuple[int, int]]:
    """
    Make step as in above, but with a sheck to ensure there is no shelf in the
    way.

    Parameters
    ----------
    direction : int
        Use the module globals HORIZ and VERT to describe horizontal or
        vertical movement.
    start_coord : Tuple[int, int]
        Coordinate to start movement.
    i : int
        The next horizontal or vertical index.
    shelf_lookup : Set[Tuple[int, int]]
        The shelf lookup table.

    Returns
    -------
    step : Tuple[int, int]
        The new coordinate.

    """
    step = make_step(direction, start_coord, i)
    if step not in shelf_lookup:
        return step
    return None


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


##################################


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
