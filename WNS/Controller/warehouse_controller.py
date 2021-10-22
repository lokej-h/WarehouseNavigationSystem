"""

Controller in charge of retrieving and parsing the warehouse data file.

"""

from pathlib import Path
from typing import Dict, List, Tuple


class g:
    """Global variables are set to this module level class when WNS is imported"""

    warehouse_file_path: Path
    """The file path containing warehouse data"""


def get_warehouse_shelves() -> Dict[str, List[Tuple[int, int]]]:
    """
    Get and parse the warehouse data for reading.
    
    This program assumes that the file provided matches the specification:
        
    1. The first line must be the column names.
    2. Every consecutive line must have three numbers separated by whitespace
    in the order "ProductID, xLocation, yLocation"
    
    Example:
    
    Product 1 is at location (5,8)
    
        ProductID    xLocation    yLocation
        1 5 8 

    Returns
    -------
    Dict[str, List[Tuple[int, int]]]
    
    Returns a dictionary of items and corresponding shelves.
        
    Key: PID as string
        
    Value: (x,y) coordinate of item's shelf
    
    This means that dict.values() will have duplicates.

    """
    # with open(file_path) as file:
    #     colnames = file.readline().split()
    #     shelves = set()
    #     for line in file.readlines():
    #         shelves.add(Shelf(*line.split()))
    #     return shelves
    with open(g.warehouse_file_path) as file:
        colnames = file.readline().split()
        shelves = set()

        product_dict = dict()

        for line in file.readlines():
            l = line.split()
            x = int(float(l[1]))
            y = int(float(l[2]))
            product_dict[l[0]] = (x, y)
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
