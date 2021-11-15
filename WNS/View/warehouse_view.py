# # -*- coding: utf-8 -*-
# from typing import Set, List, Tuple, Dict
# from .menu import MenuDecision
# from .view_helpers import int_to_cap_letter, coord_to_human
# from queue import Queue
# from queue import LifoQueue


# class g:
#     """
#     Global variables are set to this module level class when WNS is imported

#     Other globals for this module are stored here as well.
#     """

#     warehouse_array: List[List[str]]


# def display_start() -> str:
#     val = input(
#         "Enter what you would like to do on the warehouse application.\nThe following are your options\n1. Print the Warehouse view to see the products in the warehouse.\n2. Enter a product ID to see where in the warehouse you can find the product.\n3. Enter a product ID to find navigation steps to that product.\n4. Select a new file to load as warehouse.\n5. Quit navigation and end program\n"
#     )
#     return val


# def warehouse_row_range():
#     return range(len(g.warehouse_array))


# def warehouse_col_range():
#     return range(len(g.warehouse_array[0]))


# def print_warehouse(highlight_positions=[]) -> None:
#     # =============================================================================
#     #     depending on whether you'd rather work with the warehouse data type
#     #     Model team is working on, "warehouse" type may change
#     # =============================================================================
#     print(
#         """
# ______________
# |Legend      |
# |X : Shelf   |
# |. : Empty   |
# |O : Product |
# --------------
# """
#     )
#     print("  ", end=" ")
#     print_column_header()

#     print("")

#     for i in warehouse_row_range():
#         # print row number
#         rowNumber = i + 1
#         if rowNumber < 10:
#             print(rowNumber, end="  ")
#         else:
#             print(rowNumber, end=" ")
#         # print row data
#         for j in warehouse_col_range():
#             if (i, j) in highlight_positions:
#                 print("O", end=" ")
#             else:
#                 print(g.warehouse_array[i][j], end=" ")
#         print()


# def print_column_header():
#     for i in warehouse_col_range():
#         # add 1 for user readability
#         print(int_to_cap_letter(i + 1), end=" ")


# # you should move these into a new module


# def show_item_location(pid, shelves):
#     try:
#         print(
#             f"The product with ID: {pid}, is at the following location: "
#             + "({0}, {1})".format(*coord_to_human(shelves[pid]))
#         )
#         print(
#             "The following is the map of the warehouse, with the product selected being denoted by an O"
#         )
#         print_warehouse(highlight_positions=[shelves[pid]])
#         print()
#     except (KeyError):
#         print(str(pid) + " is not a product ID that exists in this warehouse.")


# def init_array(shelves):
#     shelf_set = set(shelves.values())

#     # from the set of tuples, we want to find the max row and col
#     # to do this we will use the "zip" function to transpose the matrix
#     shelf_coords = list(shelf_set)
#     x, y = list(zip(*shelf_coords))
#     # this zip will repack the data from
#     # =============================================================================
#     #     [[1,2],
#     #      [3,4]]
#     #     to
#     #     [[1,3],
#     #      [2,4]]
#     # =============================================================================
#     # see https://book.pythontips.com/en/latest/zip.html

#     # add 2 (+1 for left/right top/bottom each) to the max
#     # for the extra space around the warehouse
#     cols = max(y) + 2
#     rows = max(x) + 2

#     # add to the array row by row
#     arr = list()
#     # for each row
#     for j in range(rows):
#         row = list()
#         # for each column in the row
#         for i in range(cols):
#             # check if the current coordinate is a shelf coordinate
#             # if it is, "X" else "."
#             if (j, i) in shelf_set:
#                 row.append("X")
#             else:
#                 row.append(".")
#         arr.append(row)
#     g.warehouse_array = arr


# def direction(a, b):
#     if a[0] > b[0]:  # going up
#         return "^"
#     elif a[0] < b[0]:  # going down
#         return "v"
#     elif a[1] > b[1]:  # going right
#         return "<"
#     elif a[1] < b[1]:  # going left
#         return ">"


# def print_path(pid, shelves, path):

#     try:
#         # go through each coordinate, and look at next value until right before end
#         for i in range(0, len(path) - 1):
#             g.warehouse_array[path[i][0]][path[i][1]] = direction(path[i], path[i + 1])

    

#         print(
#             f"The product with ID: {pid}, is at the following location: "
#             + "({0}, {1})".format(*coord_to_human(shelves[pid]))
#         )
#         print(
#             "The following is the map of the warehouse, with the product selected being denoted by an O"
#         )
#         print_warehouse(highlight_positions=[shelves[pid]])
#         for i in path:
#             g.warehouse_array[i[0]][i[1]] = "."
#         print()

#     except (KeyError):
#         print(str(pid) + " is not a product ID that exists in this warehouse.")
#     pass


# ##################################



# def find_item_list_path_bfs(
#     start_coord: Tuple[int, int], pickup_item: int, shelves: Dict[str, List[int]],
# ) -> List[Tuple[int, int]]:
#     """
#     Find a path from the start coordinates to each item in the list.

#     Parameters
#     ----------
#     start_coord : Tuple[int, int]
#         The coordinates to start pathing.
#     pickup_item: int
#         item id to pickup
#     shelves : Dict[str, List[int]]
#         Shelf lookup table to avoid walking into shelves.

#     Returns
#     -------
#     path: List[Tuple[int, int]], int
#         Returns a path from the start coordinates to item passed in. Also returns number of steps taken to get to item. 

#     """
#     item = str(pickup_item)

#     visited = []
#     for i in range(0, len(g.warehouse_array)):
#         new = []
#         for j in range(0, len(g.warehouse_array[0])):
#             new.append(False)
#         visited.append(new)


#     visited[start_coord[0]][start_coord[1]] = True
#     nodes_left_in_layer = 1
#     nodes_in_next_layer = 0
#     move_count = 0
#     dr = [-1, +1, 0, 0]
#     dc = [0, 0, +1, -1]
#     reached_end = False

#     p = []
#     p.append(start_coord)
#     q = Queue()
#     q.put((start_coord[0], start_coord[1], p))

#     while q.qsize() > 0:
#         r = q.get()
#         if(r[0] == shelves[item][0] and r[1] == shelves[item][1]):
#             reached_end = True
#             break
#         for i in range(0, 4):
#             rr = r[0] + dr[i]
#             cc = r[1] + dc[i]

#             if rr < 0 or cc < 0:
#                 continue
#             if rr >= len(g.warehouse_array) or cc >= len(g.warehouse_array[0]):
#                 continue

#             if visited[rr][cc] == True:
#                 continue
#             if g.warehouse_array[rr][cc] == "X" and (rr != shelves[item][0] or cc != shelves[item][1]):
#                 continue

#             nl = []
#             for i in range(len(r[2])):
#                 nl.append(r[2][i])
#             nl.append((rr,cc))
#             q.put((rr, cc, nl))
#             visited[rr][cc] = True
#             nodes_in_next_layer = nodes_in_next_layer + 1

#         nodes_left_in_layer = nodes_left_in_layer - 1;
#         if nodes_left_in_layer == 0:
#             nodes_left_in_layer = nodes_in_next_layer
#             nodes_in_next_layer = 0
#             move_count = move_count + 1
#     if reached_end:
#         return r[2], len(r[2])

#     return -1


# def find_item_list_path_dfs(
#     start_coord: Tuple[int, int], pickup_item: int, shelves: Dict[str, List[int]],
# ) -> List[Tuple[int, int]]:
#     """
#     Find a path from the start coordinates to each item in the list.

#     Parameters
#     ----------
#     start_coord : Tuple[int, int]
#         The coordinates to start pathing.
#     pickup_item: int
#         item id to pickup
#     shelves : Dict[str, List[int]]
#         Shelf lookup table to avoid walking into shelves.

#     Returns
#     -------
#     path: List[Tuple[int, int]], int
#         Returns a path from the start coordinates to item passed in. Also returns number of steps taken to get to item. 

#     """
#     item = str(pickup_item)

#     visited = []
#     for i in range(0, len(g.warehouse_array)):
#         new = []
#         for j in range(0, len(g.warehouse_array[0])):
#             new.append(False)
#         visited.append(new)


#     visited[start_coord[0]][start_coord[1]] = True
#     nodes_left_in_layer = 1
#     nodes_in_next_layer = 0
#     move_count = 0
#     dr = [-1, +1, 0, 0]
#     dc = [0, 0, +1, -1]
#     reached_end = False

#     p = []
#     p.append(start_coord)
#     q = LifoQueue()
#     q.put((start_coord[0], start_coord[1], p))

#     while q.qsize() > 0:
#         r = q.get()
#         if(r[0] == shelves[item][0] and r[1] == shelves[item][1]):
#             reached_end = True
#             break
#         for i in range(0, 4):
#             rr = r[0] + dr[i]
#             cc = r[1] + dc[i]

#             if rr < 0 or cc < 0:
#                 continue
#             if rr >= len(g.warehouse_array) or cc >= len(g.warehouse_array[0]):
#                 continue

#             if visited[rr][cc] == True:
#                 continue
#             if g.warehouse_array[rr][cc] == "X" and (rr != shelves[item][0] or cc != shelves[item][1]):
#                 continue

#             nl = []
#             for i in range(len(r[2])):
#                 nl.append(r[2][i])
#             nl.append((rr,cc))
#             q.put((rr, cc, nl))
#             visited[rr][cc] = True
#             nodes_in_next_layer = nodes_in_next_layer + 1

#         nodes_left_in_layer = nodes_left_in_layer - 1;
#         if nodes_left_in_layer == 0:
#             nodes_left_in_layer = nodes_in_next_layer
#             nodes_in_next_layer = 0
#             move_count = move_count + 1
#     if reached_end:
#         return r[2], len(r[2])

#     return -1










#dominic
# -*- coding: utf-8 -*-
from typing import Set, List
from .menu import MenuDecision
from .view_helpers import int_to_cap_letter, coord_to_human
import colorama
from colorama import Fore, Back, Style

from typing import Set, List, Tuple, Dict
from .menu import MenuDecision
from .view_helpers import int_to_cap_letter, coord_to_human
from queue import Queue
from queue import LifoQueue

colorama.init()

"""
Global definitions of colorized symbols/characters used to represent objects in the warehouse
"""
up=Fore.YELLOW+"^"+Style.RESET_ALL
down=Fore.YELLOW+"v"+Style.RESET_ALL
left=Fore.YELLOW+"<"+Style.RESET_ALL
right=Fore.YELLOW+">"+Style.RESET_ALL

empty=Fore.BLACK + Style.BRIGHT + "." + Style.RESET_ALL
shelf=Fore.RED+"X"+Style.RESET_ALL
product=Fore.BLUE+"0"+Style.RESET_ALL
start=Fore.GREEN+"S"+Style.RESET_ALL

class g:
    """
    Global variables are set to this module level class when WNS is imported
    Other globals for this module are stored here as well.
    """

    warehouse_array: List[List[str]]



def display_start() -> str:
    val = input(
        "Enter what you would like to do on the warehouse application.\nThe following are your options\n1. Print the Warehouse view to see the products in the warehouse.\n2. Enter a product ID to see where in the warehouse you can find the product.\n3. Enter a product ID to find navigation steps to that product.\n4. Select a new file to load as warehouse.\n5. Enter a list of Items to find a path to pickup every inputted item\n6. Quit navigation and end program\n"
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
|S : Start   |
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
                print(product, end=" ")
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
    if shelves==None: #error in which file was not found when trying to update file, do not try to update the array
        return

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
                row.append(shelf)
            else:
                row.append(empty)
        arr.append(row)
    g.warehouse_array = arr


def direction(a, b):
    if a[0] > b[0]:  # going up
        return up
    elif a[0] < b[0]:  # going down
        return down
    elif a[1] > b[1]:  # going right
        return left
    elif a[1] < b[1]:  # going left
        return right


def print_path(pid, shelves, path):

    try:
        # go through each coordinate, and look at next value until right before end
        for i in range(0, len(path) - 1):
            g.warehouse_array[path[i][0]][path[i][1]] = direction(path[i], path[i + 1])

        g.warehouse_array[path[0][0]][path[0][1]]=start #Label start as S
    
        if pid == str(-1):
            print(
                f"The product with ID: START, is at the following location: "
                + str(shelves[pid])
            )
        else:
            print(
                f"The product with ID: {pid}, is at the following location: "
                + "({0}, {1})".format(*coord_to_human(shelves[pid]))
            )
        print(
            "The following is the map of the warehouse, with the product selected being denoted by an O"
        )
        print_warehouse(highlight_positions=[shelves[pid]])
        for i in path:
            g.warehouse_array[i[0]][i[1]] = empty
        if pid!=str(-1):
            g.warehouse_array[path[-1][0]][path[-1][1]]=shelf #turn product location back into shelf
        print()

    except (KeyError):
        print(str(pid) + " is not a product ID that exists in this warehouse.")
    pass


def find_item_list_path_bfs(
    start_coord: Tuple[int, int], pickup_item: int, shelves: Dict[str, List[int]],
) -> List[Tuple[int, int]]:
    """
    Find a path from the start coordinates to each item in the list.

    Parameters
    ----------
    start_coord : Tuple[int, int]
        The coordinates to start pathing.
    pickup_item: int
        item id to pickup
    shelves : Dict[str, List[int]]
        Shelf lookup table to avoid walking into shelves.

    Returns
    -------
    path: List[Tuple[int, int]], int
        Returns a path from the start coordinates to item passed in. Also returns number of steps taken to get to item. 

    """
    # print(g.warehouse_array[3][2])
    item = str(pickup_item)
    # print(item)

    visited = []
    for i in range(0, len(g.warehouse_array)):
        new = []
        for j in range(0, len(g.warehouse_array[0])):
            new.append(False)
        visited.append(new)


    visited[start_coord[0]][start_coord[1]] = True
    nodes_left_in_layer = 1
    nodes_in_next_layer = 0
    move_count = 0
    dr = [-1, +1, 0, 0]
    dc = [0, 0, +1, -1]
    reached_end = False

    p = []
    p.append(start_coord)
    q = Queue()
    q.put((start_coord[0], start_coord[1], p))

    while q.qsize() > 0:
        r = q.get()
        # print(r)
        if(r[0] == shelves[item][0] and r[1] == shelves[item][1]):
            reached_end = True
            break
        for i in range(0, 4):
            rr = r[0] + dr[i]
            cc = r[1] + dc[i]

            # if r[0] == 3 and r[1] == 0:
            #     print("rr")
            #     print(rr)
            #     print("cc")
            #     print(cc)
            #     print(g.warehouse_array[rr][cc])


            if rr < 0 or cc < 0:
                continue
            if rr >= len(g.warehouse_array) or cc >= len(g.warehouse_array[0]):
                continue

            if visited[rr][cc] == True:
                continue
            if (g.warehouse_array[rr][cc] == "X" or g.warehouse_array[rr][cc] == 'X' or g.warehouse_array[rr][cc] == Fore.RED+"X"+Style.RESET_ALL):
                # print("x reached: ")
                # print(rr, cc)
                if (g.warehouse_array[rr][cc] == "X" or g.warehouse_array[rr][cc] == 'X' or g.warehouse_array[rr][cc] == Fore.RED+"X"+Style.RESET_ALL)  and (rr != shelves[item][0] or cc != shelves[item][1]):
                    continue
                # else:
                #     print("error5")

            nl = []
            for i in range(len(r[2])):
                nl.append(r[2][i])
            nl.append((rr,cc))
            q.put((rr, cc, nl))
            visited[rr][cc] = True
            nodes_in_next_layer = nodes_in_next_layer + 1

        nodes_left_in_layer = nodes_left_in_layer - 1;
        if nodes_left_in_layer == 0:
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count = move_count + 1
    if reached_end:
        return r[2], len(r[2])

    return -1


def find_item_list_path_dfs(
    start_coord: Tuple[int, int], pickup_item: int, shelves: Dict[str, List[int]],
) -> List[Tuple[int, int]]:
    """
    Find a path from the start coordinates to each item in the list.

    Parameters
    ----------
    start_coord : Tuple[int, int]
        The coordinates to start pathing.
    pickup_item: int
        item id to pickup
    shelves : Dict[str, List[int]]
        Shelf lookup table to avoid walking into shelves.

    Returns
    -------
    path: List[Tuple[int, int]], int
        Returns a path from the start coordinates to item passed in. Also returns number of steps taken to get to item. 

    """
    item = str(pickup_item)

    visited = []
    for i in range(0, len(g.warehouse_array)):
        new = []
        for j in range(0, len(g.warehouse_array[0])):
            new.append(False)
        visited.append(new)


    visited[start_coord[0]][start_coord[1]] = True
    nodes_left_in_layer = 1
    nodes_in_next_layer = 0
    move_count = 0
    dr = [-1, +1, 0, 0]
    dc = [0, 0, +1, -1]
    reached_end = False

    p = []
    p.append(start_coord)
    q = LifoQueue()
    q.put((start_coord[0], start_coord[1], p))

    while q.qsize() > 0:
        r = q.get()
        if(r[0] == shelves[item][0] and r[1] == shelves[item][1]):
            reached_end = True
            break
        for i in range(0, 4):
            rr = r[0] + dr[i]
            cc = r[1] + dc[i]

            if rr < 0 or cc < 0:
                continue
            if rr >= len(g.warehouse_array) or cc >= len(g.warehouse_array[0]):
                continue

            if visited[rr][cc] == True:
                continue
            if (g.warehouse_array[rr][cc] == "X" or g.warehouse_array[rr][cc] == 'X' or g.warehouse_array[rr][cc] == Fore.RED+"X"+Style.RESET_ALL) and (rr != shelves[item][0] or cc != shelves[item][1]):
                continue

            nl = []
            for i in range(len(r[2])):
                nl.append(r[2][i])
            nl.append((rr,cc))
            q.put((rr, cc, nl))
            visited[rr][cc] = True
            nodes_in_next_layer = nodes_in_next_layer + 1

        nodes_left_in_layer = nodes_left_in_layer - 1;
        if nodes_left_in_layer == 0:
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count = move_count + 1
    if reached_end:
        return r[2], len(r[2])

    return -1
##################################