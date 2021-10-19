from typing import Set
from ..Controller.warehouse_controller import Shelf



# =============================================================================
# You should probably put these in seperate files for your own sanity
# =============================================================================


class POIGraph:
    pass


class Warehouse:
    pois = POIGraph()
    pass


def find_item(item, shelves) -> tuple(int, int):
    return shelves[item]


def find_item_list_path(items: List[int], shelves):
    # ignore list, we are only grabbing the first item


##################################


def prep_data_for_computation(arr, shelves):
    # =============================================================================
    #     idk what data type you want to use to easily work with the warehouse
    #     so for now main is just passing Set[Shelf] whenever someone needs a Warehouse
    # =============================================================================
    for key in shelves:
        arr[shelves[key][0]][shelves[key][1]] = 'X'

