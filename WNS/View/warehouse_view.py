# -*- coding: utf-8 -*-
from typing import Set, List
from .menu import MenuDecision
from .view_helpers import int_to_cap_letter, coord_to_human


class g:
    """
    Global variables are set to this module level class when WNS is imported

    Other globals for this module are stored here as well.
    """

    warehouse_array: List[List[str]]


def display_start() -> str:
    val = input(
        "Enter what you would like to do on the warehouse application.\nThe following are your options\n1. Print the Warehouse view to see the products in the warehouse.\n2. Enter a product ID to see where in the warehouse you can find the product.\n3. Enter a product ID to find navigation steps to that product.\n4. Select a new file to load as warehouse.\n5. Quit navigation and end program\n"
    )
    return val


def warehouse_row_range():
    return range(len(g.warehouse_array))


def warehouse_col_range():
    return range(len(g.warehouse_array[0]))


def print_warehouse(highlight_positions=[]) -> None:
    # =============================================================================
    #     depending on whether you'd rather work with the warehouse data type
    #     Model team is working on, "warehouse" type may change
    # =============================================================================
    print(
        """
______________
|Legend      |
|X : Shelf   |
|. : Empty   |
|O : Product |
--------------
"""
    )
    print("  ", end=" ")
    print_column_header()

    print("")

    for i in warehouse_row_range():
        # print row number
        rowNumber = i + 1
        if rowNumber < 10:
            print(rowNumber, end="  ")
        else:
            print(rowNumber, end=" ")
        # print row data
        for j in warehouse_col_range():
            if (i, j) in highlight_positions:
                print("O", end=" ")
            else:
                print(g.warehouse_array[i][j], end=" ")
        print()


def print_column_header():
    for i in warehouse_col_range():
        # add 1 for user readability
        print(int_to_cap_letter(i + 1), end=" ")


# you should move these into a new module


def show_item_location(pid, shelves):
    try:
        print(
            f"The product with ID: {pid}, is at the following location: "
            + "({0}, {1})".format(*coord_to_human(shelves[pid]))
        )
        print(
            "The following is the map of the warehouse, with the product selected being denoted by an O"
        )
        print_warehouse(highlight_positions=[shelves[pid]])
        print()
    except (KeyError):
        print(str(pid) + " is not a product ID that exists in this warehouse.")


def init_array(shelves):
    shelf_set = set(shelves.values())

    # from the set of tuples, we want to find the max row and col
    # to do this we will use the "zip" function to transpose the matrix
    shelf_coords = list(shelf_set)
    x, y = list(zip(*shelf_coords))
    # this zip will repack the data from
    # =============================================================================
    #     [[1,2],
    #      [3,4]]
    #     to
    #     [[1,3],
    #      [2,4]]
    # =============================================================================
    # see https://book.pythontips.com/en/latest/zip.html

    # add 2 (+1 for left/right top/bottom each) to the max
    # for the extra space around the warehouse
    cols = max(y) + 2
    rows = max(x) + 2

    # add to the array row by row
    arr = list()
    # for each row
    for j in range(rows):
        row = list()
        # for each column in the row
        for i in range(cols):
            # check if the current coordinate is a shelf coordinate
            # if it is, "X" else "."
            if (j, i) in shelf_set:
                row.append("X")
            else:
                row.append(".")
        arr.append(row)
    g.warehouse_array = arr


def direction(a, b):
    if a[0] > b[0]:  # going up
        return "^"
    elif a[0] < b[0]:  # going down
        return "v"
    elif a[1] > b[1]:  # going right
        return "<"
    elif a[1] < b[1]:  # going left
        return ">"


def print_path(pid, shelves, path):

    try:
        # go through each coordinate, and look at next value until right before end
        for i in range(0, len(path) - 1):
            g.warehouse_array[path[i][0]][path[i][1]] = direction(path[i], path[i + 1])

    

        print(
            f"The product with ID: {pid}, is at the following location: "
            + "({0}, {1})".format(*coord_to_human(shelves[pid]))
        )
        print(
            "The following is the map of the warehouse, with the product selected being denoted by an O"
        )
        print_warehouse(highlight_positions=[shelves[pid]])
        for i in path:
            g.warehouse_array[i[0]][i[1]] = "."
        print()

    except (KeyError):
        print(str(pid) + " is not a product ID that exists in this warehouse.")
    pass


##################################
