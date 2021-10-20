# -*- coding: utf-8 -*-
from typing import List, Tuple
from . import view_helpers

def show_path(path: List[Tuple[int,int]]):
    # need to increment x by 1 because user don't start from 0 meh meh meh
    new_path = list()
    for x,y in path:
        new_path.append(tuple([x+1, view_helpers.int_to_cap_letter(y+1)]))
    return new_path
