from typing import Dict, List, Tuple


# =============================================================================
# You should probably put these in seperate files for your own sanity
# =============================================================================


class POIGraph:
    pass


class Warehouse:
    pois = POIGraph()
    pass


def find_item(
    item: List[int], shelves: Dict[int, List[Tuple[int, int]]]
) -> Tuple[int, int]:
    return shelves[item]


def go_right_until_end(start_coord, end_coords, shelf_lookup, path):
    for x in range(start_coord[0], end_coords[0]):
        next_step = tuple(x, start_coord[1])
        if next_step in shelf_lookup:
            return path, path[-1]
        path.append(tuple(x, start_coord[1]))
    return path, path[-1]


def go_up_until_end(start_coord, end_coords, shelf_lookup, path):
    for y in range(start_coord[1], end_coords[1]):
        next_step = tuple(start_coord[0], y)
        if next_step in shelf_lookup:
            return path, path[-1]
        path.append(tuple(start_coord[0], y))
    return path, path[-1]


def find_item_list_path(
    start_coord: tuple[int, int],
    items: List[int],
    shelves: Dict[int, List[Tuple[int, int]]],
) -> List[Tuple[int, int]]:
    # ignore list, we are only grabbing the first item
    item = items[0]

    # get where the item is
    end_coords = find_item(item, shelves)

    # make a basic path
    shelf_lookup = set([tuple(x) for x in shelves.values()])

    path = list()
    last_coord = start_coord
    while end_coords not in [
        (last_coord[0], last_coord[1] + 1),
        (last_coord[0], last_coord[1] - 1),
        (last_coord[0] + 1, last_coord[1]),
        (last_coord[0] - 1, last_coord[1]),
    ]:
        path, last_coord = go_right_until_end(
            last_coord, end_coords, shelf_lookup, path
        )
        path, last_coord = go_up_until_end(last_coord, end_coords, shelf_lookup, path)
    return path


##################################


def prep_data_for_computation(arr, shelves):
    # =============================================================================
    #     idk what data type you want to use to easily work with the warehouse
    #     so for now main is just passing Set[Shelf] whenever someone needs a Warehouse
    # =============================================================================
    for key in shelves:
        arr[shelves[key][0]][shelves[key][1]] = "X"
