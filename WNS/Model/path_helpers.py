"""
Helpers for path creation
"""

from typing import Dict, Tuple, List, Set, Optional

class g:
    """
    path globals
    """
    shelves: Dict[str, List[int]]
    # shelf lookup table
    
def set_shelf_lookup(shelf_lookup: Dict[str, List[int]]):
    """
    Set global shelf lookup

    Parameters
    ----------
    shelf_lookup : Dict[str, List[int]]
        newly created shelf lookup table.

    Returns
    -------
    None.

    """
    g.shelves = shelf_lookup

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
