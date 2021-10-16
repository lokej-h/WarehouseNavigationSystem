# =============================================================================
# from typing import Callable, Set, Dict,
# =============================================================================
from pathlib import Path
import os


class config:
    HOME_PATH = Path(os.getenv("WNS_PATH", "."))
    WAREHOUSE_DATA_DIR = os.getenv(
        "WAREHOUSE_DATA_DIR",
        (HOME_PATH / "input" / "qvBox-warehouse-data-f20-v01_1041763401.txt"),
    )
