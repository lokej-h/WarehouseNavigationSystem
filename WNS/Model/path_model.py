from typing import Dict, List, Tuple, Set, Optional
import itertools
import random
import logging

# =============================================================================
# You should probably put these in seperate files for your own sanity
# =============================================================================
LOGGER = logging.getLogger(__name__)
HORI = 0
VERT = 1


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


def muck_about(
    last_coord: Tuple[int, int], shelf_lookup: Set[Tuple[int, int]]
) -> Tuple[int, int]:
    """
    Randomly go in one of the 4 (or less) available directions.
    This function is safe and will not go into a shelf.

    Parameters
    ----------
    last_coord : Tuple[int, int]
        Coordinate to start movement.
    shelf_lookup: Set[Tuple[int, int]]
        The shelf lookup table.

    Raises
    ------
    Exception
        If we ended up with shelves all around, something incredibly wrong
        has happened. Raise an exception as we have completely failed.

    Returns
    -------
    step : Tuple[int, int]
        Return a randomly chosen valid step from the given coordinates.

    """
    dirs = [HORI, VERT]
    deltas = [1, -1]
    # randomly go in a valid direction
    for each in [dirs, deltas]:
        random.shuffle(each)
    LOGGER.debug("\tmuck about")
    for direction, value in itertools.product(dirs, deltas):
        step = safe_make_step(
            direction, last_coord, last_coord[direction] + value, shelf_lookup
        )
        LOGGER.debug(f"trying to go to {step}")
        if step:
            return step
    raise Exception("how'd you get yourself stuck?")


def go_until_end(
    direction: int,
    start_coord: Tuple[int, int],
    end_coords: Tuple[int, int],
    shelf_lookup: Set[Tuple[int, int]],
    path: List[Tuple[int, int]],
) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    """
    Function to either go horizontally or vertically until we hit the matching
    end coordinate.

    Parameters
    ----------
    direction : int
        Use the module globals HORIZ and VERT to describe horizontal or
        vertical movement.
    start_coord : Tuple[int, int]
        Coordinate to start movement.
    end_coords : Tuple[int, int]
        Coordinate to end movement.
    shelf_lookup : Set[Tuple[int, int]]
        The shelf lookup table.
    path : List[Tuple[int, int]]
        The path build so far.

    Returns
    -------
    path : List[Tuple[int, int]]
        The path built so far (with the steps found added on).
    last_coord: Tuple[int, int]]
        The last coordinate in the path.

    """
    # =============================================================================
    #     if direction == 0:
    #         LOGGER.debug("horizontal")
    #     else:
    #         LOGGER.debug("vertical")
    #     LOGGER.debug(f"starting at {start_coord}")
    #     LOGGER.debug(f"going from {start_coord[direction]} to {end_coords[direction]}")
    # =============================================================================
    # until we match the target coord x or y
    for i in range(start_coord[direction] + 1, end_coords[direction] + 1):
        # go 1 step horizontally, vertically
        next_step = make_step(direction, start_coord, i)
        LOGGER.debug(f"going to {next_step}")
        # if we will try to go in a shelf
        if next_step in shelf_lookup:
            # abort
            LOGGER.debug("in shelf! abort!")
            return path, path[-1]
        # no shelf ahead, add to path
        # LOGGER.debug(f"appending {next_step}")
        path.append(next_step)

    # it's possible that we have already matched the x/y
    # without adding anything to the path
    if len(path) == 0:
        # so just return what we got
        LOGGER.debug("path was zero len")
        return path, start_coord
    LOGGER.debug(f"finished matching, path is {path},\n\tlast index is {path[-1]}")
    return path, path[-1]


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
    shelf_lookup = set([(x[0] + 1, x[1] + 1) for x in shelves.values()])

    # get where the item is
    end_coords = find_item(item, shelves)
    LOGGER.debug(f"shelf access {end_coords[0]+1}, {chr(ord('@')+end_coords[1]+1)}")
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
    LOGGER.debug(
        f"can access shelf from {end_coords[0]+1}, {chr(ord('@')+end_coords[1]+1)}"
    )

    # make a basic path

    path = list()
    path.append(start_coord)
    last_coord = start_coord
    while end_coords != last_coord:
        path, last_coord = go_until_end(
            VERT, last_coord, end_coords, shelf_lookup, path
        )
        horiz = last_coord
        path, last_coord = go_until_end(
            HORI, last_coord, end_coords, shelf_lookup, path
        )
        if horiz == last_coord:
            # this means we got stuck on something
            LOGGER.debug("we are stuck!")
            LOGGER.debug("try randomly walking around")
            path.append(muck_about(last_coord, shelf_lookup))
            path.append(muck_about(path[-1], shelf_lookup))
            path.append(muck_about(path[-1], shelf_lookup))
            path.append(muck_about(path[-1], shelf_lookup))
            last_coord = path[-1]
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
