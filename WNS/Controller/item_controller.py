# -*- coding: utf-8 -*-
"""

Controller in charge of retrieving and parsing the user input for items.

"""

from typing import List


def get_one_item() -> str:
    """
    Retrieves 1 item from user.

    Returns
    -------
    str
        The product ID the user would like to select.

    """
    return input("Enter product ID of the product you are searching for: ")


def get_item_list() -> List[str]:
    """
    Retrieves a list of items from the user.

    Returns
    -------
    List[str]
        The list of product IDs the user would like to select.

    """
    return input("Enter item(s) to navigate to (separate items with a space): ").split()
