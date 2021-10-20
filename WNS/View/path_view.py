# -*- coding: utf-8 -*-
from typing import List, Tuple
from . import view_helpers


def show_path(path: List[Tuple[int, int]]) -> List[Tuple[int, str]]:
    # need to increment x by 1 because user don't start from 0 meh meh meh
    pather = list()
    path_str = str()
    for x, y in path:
        step = (x + 1, view_helpers.int_to_cap_letter(y + 1))  # type: Tuple[int, str]
        pather.append(step)
        path_str += f"({step[0]}, " + step[1] + ") -> "
    path_str = path_str[:-4]
    print(path_str)
    return pather
