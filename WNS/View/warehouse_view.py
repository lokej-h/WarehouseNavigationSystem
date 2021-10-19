# -*- coding: utf-8 -*-
from typing import Set
from ..SharedTypes.Shelf import Shelf
from .menu import MenuDecision


def display_start() -> int:
    val = input("Enter what you would like to do on the warehouse application.\nThe following are your options\n1. Print the Warehouse view to see the products in the warehouse.\n2. Enter a product ID to see where in the warehouse you can find the product.\n3. Enter a product ID to find navigation steps to that product.\n4. Quit navigation and end program\n")
    return val


def print_warehouse(arr) -> None:
    # =============================================================================
    #     depending on whether you'd rather work with the warehouse data type
    #     Model team is working on, "warehouse" type may change
    # =============================================================================

    print("  ", end = " ")
    for i in range(ord('A'), ord('W') + 1):
        print(chr(i), end = " ")

    print("")



    for i in range(len(arr)):
        if i < 10:
            print(i, end = "  ")
        else:
            print(i, end = " ")
        for j in range(len(arr[i])):
            print(arr[i][j], end=" ")
        print()
    pass


# you should move these into a new module
def show_item_location(arr, shelves):
    pid = input("Enter product ID of the product you are searching for: ")
    try:
        print("The product with ID: ", pid, "is at the following location: (", shelves[pid][0] + 1, chr(shelves[pid][1] + 98), ')')
        arr[shelves[pid][0]+1][shelves[pid][1]+1] = 'O'
        print("The following is the map of the warehouse, with the product selected being denoted by an O")
        print_warehouse(arr)
        arr[shelves[pid][0]+1][shelves[pid][1]+1] = 'X'
        print()
    except(KeyError):
        print(str(pid) + " is not a product ID that exists in this warehouse.")


def init_array(shelves):
    find_max_x = []
    find_max_y = []
    for key in shelves:
        find_max_x.append(shelves[key][0])
        find_max_y.append(shelves[key][1])
    print(max(find_max_x))
    print(max(find_max_y))
    rows, cols = (max(find_max_x) + 3, max(find_max_y) + 3)
    arr = [['.' for i in range(cols)] for j in range(rows)]
    return arr

def show_path(path):
    pass


##################################
