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


def find_item(item):
    pass


def find_item_list_path(items):
    pass


##################################


def prep_data_for_computation(arr, shelves):
    # =============================================================================
    #     idk what data type you want to use to easily work with the warehouse
    #     so for now main is just passing Set[Shelf] whenever someone needs a Warehouse
    # =============================================================================
    for key in shelves:
        if shelves[key][1] > 9:
            arr[shelves[key][0]+1][shelves[key][1]+1] = 'X' + ' '
        else:
            arr[shelves[key][0]+1][shelves[key][1]+1] = 'X'

