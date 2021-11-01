"""

Controller in charge of retrieving and parsing the warehouse data file.

"""

from pathlib import Path
from typing import Dict, List, Tuple


class g:
    """Global variables are set to this module level class when WNS is imported"""

    warehouse_file_path: Path
    """The file path containing warehouse data"""


def get_warehouse_shelves() -> Dict[str, Tuple[int, int]]:
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
    with open(g.warehouse_file_path) as file:
        # read out column names from buffer
        file.readline().split()

        product_dict = dict()

        for line in file.readlines():
            l = line.split()
            x = int(float(l[1]))
            y = int(float(l[2]))
            # the coordinates start at 0,0
            # this 0,0 transalates to 2,B or 2,2
            # we will tackle in two steps
            # +1 during load, we +1 for calculations (empty space in 0th row col)
            # +1 for view coordinates for user
            # add 1 to each coordinate to add the space for the walkway
            # around the border of the warehouse
            product_dict[l[0]] = (x + 1, y + 1)
        return product_dict


def change_warehouse_shelves(file_path) -> Dict[str, Tuple[int, int]]:
    """
    Change warehouse data and read from user specified file.
    
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
    with open(file_path) as file:
        # read out column names from buffer
        file.readline().split()

        product_dict = dict()

        for line in file.readlines():
            l = line.split()
            x = int(float(l[1]))
            y = int(float(l[2]))
            # the coordinates start at 0,0
            # this 0,0 transalates to 2,B or 2,2
            # we will tackle in two steps
            # +1 during load, we +1 for calculations (empty space in 0th row col)
            # +1 for view coordinates for user
            # add 1 to each coordinate to add the space for the walkway
            # around the border of the warehouse
            product_dict[l[0]] = (x + 1, y + 1)
        return product_dict