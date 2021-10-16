# -*- coding: utf-8 -*-
from enum import IntEnum, unique


@unique
class MenuDecision(IntEnum):
    QUIT = 0
    FIND_ITEM = 1
    FIND_ITEM_PATH = 2
