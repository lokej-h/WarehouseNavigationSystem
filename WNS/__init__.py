"""

All imports in __init__.py are exposed to the outside module, 
this helps keep the importing module’s namespace clean.

"""

from .View.warehouse_view import (
    display_start,
    show_item_location,
    init_array,
    print_warehouse,
    print_path,
    find_item_list_path_bfs,
    find_item_list_path_dfs,
)
from .View.path_view import show_path
from .Model.path_model import prep_data_for_computation, find_item, find_item_list_path
from ._config import config
from .View.menu import MenuDecision

# =============================================================================
# these imports are not final as importing each function from a better defined
# module would be best, this just makes it run
# =============================================================================
from .Controller.warehouse_controller import get_warehouse_shelves
from .Controller.warehouse_controller import change_warehouse_shelves
from .Controller.item_controller import (
    get_one_item,
    get_item_list,
)
from typing import Dict, Tuple
import time
import colorama


def init_WNS() -> Dict[str, Tuple[int, int]]:
    shelves = get_warehouse_shelves()
    row_m, col_m = init_array(shelves)
    return shelves, row_m, col_m
