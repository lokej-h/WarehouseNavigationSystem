"""

Controller in charge of retrieving and parsing the warehouse data file.

"""

from pathlib import Path
from typing import Dict, List, Tuple


class g:
    """Global variables are set to this module level class when WNS is imported"""

    warehouse_file_path: Path
    """The file path containing warehouse data"""


class InvalidWarehouseData(Exception):
    def __init__(self, message="The warehouse data file is invalid."):
        self.message = message
        super().__init__(self.message)


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
    # ensure we have a valid warehouse path in case the ENV VAR is bad
    try:
        check_warehouse_data_file(g.warehouse_file_path)
    except InvalidWarehouseData:
        change_warehouse_shelves()
        
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
        print("File Loaded Successfully\n")
        return product_dict


def check_warehouse_data_file(file: Path) -> bool:
    """
    Checks a file if it matches the warehouse data filespec.

    Parameters
    ----------
    file : Path
        The file to check. It is assumed this is a valid file.

    Returns
    -------
    bool
        Whether or not the check succeeds.
        Does not return false, rather it throws an InvalidWarehouseData exception.

    """
    if not file.is_file():
        raise InvalidWarehouseData(f"File {file} does not exist!")
    # check is .txt
    if file.suffix != ".txt":
        print("bad suffix")
        raise InvalidWarehouseData("File is not a 'txt' file.")
    with open(file) as data_file:
        # check firstline is col names that match specs
        cols = data_file.readline().split()
        col_spec = ["ProductID","xLocation","yLocation"]
        if cols != col_spec:
            raise InvalidWarehouseData(f"Column names {cols} do not match the specification {col_spec}.")
        # keep track of line numbers for error
        line_number = 1
        # Check each consecutive line
        for line in data_file.readlines():
            numbers = line.split()
            # must have 3 columns
            if len(numbers) != 3:
                raise InvalidWarehouseData(f"Line {line_number}: \'{line.rstrip()}\' does not have exactly 3 columns.")
            # each column must be float values
            # remove 1 '.' and check the string is made only of digits
            if not all([num.replace('.', '', 1).isdigit() for num in numbers]):
                raise InvalidWarehouseData(f"Line {line_number}: \n\t{numbers}\n are not all floats.")
            line_number += 1
    return True
        


def change_warehouse_shelves() -> None:
    """
    Change warehouse data path
    
    """
    def get_user_path() -> Path:
        path_str = input("Please input the exact path for the file you want to load as your warehouse\n")
        file_path = Path(path_str.strip('\"\''))
        return file_path
    while True:
        file_path = get_user_path()
        try:
            if check_warehouse_data_file(file_path):
                break
        except InvalidWarehouseData as e:
            print("\n\n\t", e, "\n\n")
        
    g.warehouse_file_path = file_path
