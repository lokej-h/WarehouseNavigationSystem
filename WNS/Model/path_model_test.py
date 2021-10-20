# -*- coding: utf-8 -*-

import pytest
from . import path_model


@pytest.fixture
def shelves():
    raw_shelves = [
        (0, 1),
        (0, 2),
        (0, 3),
        (2, 1),
        (2, 2),
        (2, 3),
    ]

    shelves = dict()
    for i in range(len(raw_shelves)):
        shelves[i] = raw_shelves[i]
    return shelves

@pytest.fixture
def shelves2():
    raw_shelves = [
        (3, 1),
    ]

    shelves = dict()
    for i in range(len(raw_shelves)):
        shelves[i] = raw_shelves[i]
    return shelves

def test_make_step():
    assert path_model.make_step(0, (0,0), 1) == (1,0)
    assert path_model.make_step(1, (0,0), 1) == (0,1)
    assert path_model.make_step(0, (0,1), 2) == (2,1)
    assert path_model.make_step(1, (1,0), 2) == (1,2)

def test_find_item_list_path(shelves):
    path = path_model.find_item_list_path((0, 0), [1], shelves)
    assert path == [(0, 0), (1, 0), (1, 1), (1, 2)]
    assert all([step not in shelves.values() for step in path])

# =============================================================================
# def test_find_item_list_path2(shelves2):
#     path = path_model.find_item_list_path((0, 0), [0], shelves)
#     assert path == [(0, 0), (1, 0), (1, 1), (1, 2)]
#     assert all([step not in shelves.values() for step in path])
# =============================================================================
