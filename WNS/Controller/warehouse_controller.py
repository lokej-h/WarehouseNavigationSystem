from pathlib import Path
from typing import Dict, List, Tuple
from ..SharedTypes.Shelf import Shelf


# =============================================================================
# TODO: Move these functions out
# =============================================================================
def get_one_item() -> int:
    return input("Enter product ID of the product you are searching for: ")


def get_item_list() -> List[int]:
    return [input("Enter item to navigate to (only 1 in alpha release): ")]


##################################


def get_warehouse_shelves(file_path: Path) -> Dict[int, List[Tuple[int, int]]]:
    # with open(file_path) as file:
    #     colnames = file.readline().split()
    #     shelves = set()
    #     for line in file.readlines():
    #         shelves.add(Shelf(*line.split()))
    #     return shelves
    with open(file_path) as file:
        colnames = file.readline().split()
        shelves = set()

        product_dict = dict()

        for line in file.readlines():
            l = line.split()
            x = int(float(l[1]))
            y = int(float(l[2]))
            product_dict[l[0]] = [x, y]
        return product_dict


def get_warehouse_shelves_2d(file_path: Path):
    with open(file_path) as file:
        colnames = file.readline().split()
        shelves = set()

        product_dict = dict()

        for line in file.readlines():
            x = line.split()
            product_dict[x[0]] = [x[0], x[1]]
        return product_dict
