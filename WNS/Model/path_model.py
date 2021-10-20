from typing import Dict, List, Tuple
import itertools
import random

# =============================================================================
# You should probably put these in seperate files for your own sanity
# =============================================================================
HORI = 0
VERT = 1


class POIGraph:
    pass


class Warehouse:
    pois = POIGraph()
    pass


def find_item(item: int, shelves: Dict[int, List[int]]) -> Tuple[int, int]:
    return (shelves[item][0], shelves[item][1] + 1)


def make_step(direction, start_coord, i):
    next_step = list(range(2))
    next_step[(direction + 1) % 2] = start_coord[(direction + 1) % 2]
    next_step[direction] = i
    return tuple(next_step)


def safe_make_step(direction, start_coord, i, shelf_lookup):
    step = make_step(direction, start_coord, i)
    if step not in shelf_lookup:
        return step
    return None


def muck_about(last_coord, shelf_lookup):
    dirs = [HORI, VERT]
    deltas = [1, -1]
    # randomly go in a valid direction
    for l in [dirs, deltas]:
        random.shuffle(l)
    print("\tmuck about")
    for direction, value in itertools.product(dirs, deltas):
        step = safe_make_step(
            direction, last_coord, last_coord[direction] + value, shelf_lookup
        )
        print(f"trying to go to {step}")
        if step:
            return step
    raise Exception("how'd you get yourself stuck?")


def go_until_end(direction, start_coord, end_coords, shelf_lookup, path):
    """function to either go horizontally or vertically"""
    # =============================================================================
    #     if direction == 0:
    #         print("horizontal")
    #     else:
    #         print("vertical")
    #     print(f"starting at {start_coord}")
    #     print(f"going from {start_coord[direction]} to {end_coords[direction]}")
    # =============================================================================
    # until we match the target coord x or y
    for i in range(start_coord[direction] + 1, end_coords[direction] + 1):
        # go 1 step horizontally, vertically
        next_step = make_step(direction, start_coord, i)
        # print(f"going to {next_step}")
        # if we will try to go in a shelf
        if next_step in shelf_lookup:
            # abort
            # print("in shelf! abort!")
            return path, path[-1]
        # no shelf ahead, add to path
        # print(f"appending {next_step}")
        path.append(next_step)

    # it's possible that we have already matched the x/y
    # without adding anything to the path
    if len(path) == 0:
        # so just return what we got
        # print("path was zero len")
        return path, start_coord
    # print(f"finished matching, path is {path},\n\tlast index is {path[-1]}")
    return path, path[-1]


def find_item_list_path(
    start_coord: Tuple[int, int], items: List[int], shelves: Dict[int, List[int]],
) -> List[Tuple[int, int]]:
    # ignore list, we are only grabbing the first item
    item = items[0]

    # make a shelf lookup table, remembering to increment the shelves by 1
    # for the outside border
    shelf_lookup = set([(x[0] + 1, x[1] + 1) for x in shelves.values()])

    # get where the item is
    end_coords = find_item(item, shelves)
    # print(f"shelf access {end_coords[0]+1}, {chr(ord('@')+end_coords[1]+1)}")
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
    # print(f"can access shelf from {end_coords[0]+1}, {chr(ord('@')+end_coords[1]+1)}")

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
            # print("we are stuck!")
            # print("try randomly walking around")
            path.append(muck_about(last_coord, shelf_lookup))
            path.append(muck_about(path[-1], shelf_lookup))
            path.append(muck_about(path[-1], shelf_lookup))
            path.append(muck_about(path[-1], shelf_lookup))
            last_coord = path[-1]
    return path


##################################


def prep_data_for_computation(arr, shelves):
    # =============================================================================
    #     idk what data type you want to use to easily work with the warehouse
    #     so for now main is just passing Set[Shelf] whenever someone needs a Warehouse
    # =============================================================================
    for key in shelves:
        arr[shelves[key][0] + 1][shelves[key][1] + 1] = "X"
