# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:34:03 2021

@author: Student
"""
import itertools
import random
from typing import List, Tuple, Set
import logging
from .path_helpers import safe_make_step
from ..View.view_helpers import coord_to_human

LOGGER = logging.getLogger(__name__)
HORI = 0
VERT = 1


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
        next_step = safe_make_step(direction, start_coord, i, shelf_lookup)
        LOGGER.debug(f"going to {coord_to_human(next_step)}")
        # if we will try to go in a shelf
        if next_step in shelf_lookup:
            # abort
            LOGGER.debug("in shelf! abort!")
            return path, path[-1]
        # no shelf ahead, add to path
        # LOGGER.debug(f"appending {coord_to_human(next_step)}")
        path.append(next_step)

    # it's possible that we have already matched the x/y
    # without adding anything to the path
    if len(path) == 0:
        # so just return what we got
        LOGGER.debug("path was zero len")
        return path, start_coord
    LOGGER.debug(f"finished matching, path is {path},\n\tlast index is {path[-1]}")
    return path, path[-1]


def make_go_until_path(start_coord, shelf_lookup, end_coords):
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
