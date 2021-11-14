# -*- coding: utf-8 -*-
from typing import List, Tuple
from . import view_helpers

def show_path(path: List[Tuple[int, int]]) -> List[Tuple[int, str]]:
    # need to increment x by 1 because user don't start from 0 meh meh meh
    pather = list()
    path_str = str()
    bundledpath = bundle(path)
    # print(bundledpath)
    prevx = bundledpath[0][0]
    prevy = bundledpath[0][1]
    for x, y in bundledpath[1:]:
        if x > prevx:
            if x-prevx == 1:
                print("Move one step down")
            else:
                print("Move %d steps down" % (x-prevx))
        elif x < prevx:
            if prevx-x == 1:
                print("Move one step up")
            else:
                print("Move %d steps up" % (prevx-x))
        elif y > prevy:
            if prevy-y == 1:
                print("Move one step right")
            else:
                print("Move %d steps right" % (y-prevy))
        elif y < prevy:
            if prevy-y == 1:
                print("Move one step left")
            else:
                print("Move %d steps left" % (prevy-y))
        prevx = x
        prevy = y
        step = (x + 1, view_helpers.int_to_cap_letter(y + 1))  # type: Tuple[int, str]
        pather.append(step)
        path_str += f"({step[0]}, " + step[1] + ") -> "
    path_str = path_str[:-4]
    return pather

def bundle(path):
    bundledpath = []
    bundledpath.append(path[0])
    direction = "x"
    prevx = path[0][0]
    prevy = path[0][1]
    if path[1][0] == prevx:
        direction = "y"
    else:
        direction = "x"
    # print(direction)
    for x, y in path[1:]:
        if y == prevy and direction == "y":
            direction = "x"
            bundledpath.append((prevx,prevy))
        elif x == prevx and direction == "x":
            direction = "y"
            bundledpath.append((prevx,prevy))
        prevx = x
        prevy = y
    bundledpath.append(path[-1])
    return bundledpath