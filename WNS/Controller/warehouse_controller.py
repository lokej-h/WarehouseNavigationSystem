from pathlib import Path
from typing import Set


# =============================================================================
# TODO: Move these functions out
# =============================================================================
def get_one_item():
    pass


def get_item_list():
    pass


##################################


class Shelf:
    """Shelf type"""

    def __init__(self, pid, x, y):
        self.pids = pid
        self.x = x
        self.y = y

    def __str__(self):
        return f"Shelf at ({self.x}. {self.y}) containing items {self.pids}"

    def __repr__(self):
        return str(self)


def get_warehouse_shelves(file_path: Path) -> Set[Shelf]:
    with open(file_path) as file:
        colnames = file.readline().split()
        shelves = set()
        for line in file.readlines():
            shelves.add(Shelf(*line.split()))
        return shelves
