# -*- coding: utf-8 -*-
from typing import List

def get_one_item() -> int:
    return input("Enter product ID of the product you are searching for: ")


def get_item_list() -> List[int]:
    return [input("Enter item to navigate to (only 1 in alpha release): ")]