# -*- coding: utf-8 -*-
from . import path_view
import pytest


@pytest.fixture
def path():
    return [(0, 0), (1, 0), (2, 0), (3, 0)]


def test_show_path(path):
    assert path_view.show_path(path) == [(1, "A"), (2, "A"), (3, "A"), (4, "A")]
