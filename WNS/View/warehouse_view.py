# -*- coding: utf-8 -*-
from typing import Set
from ..SharedTypes.Shelf import Shelf
from .menu import MenuDecision


def display_start() -> MenuDecision:
    pass


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
def show_item_location(item):
    pass


def show_path(path):
    pass


##################################
