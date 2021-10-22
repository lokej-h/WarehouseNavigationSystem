"""

Finds and applies configuration variables to each module’s “g” (globals) class. 
This keeps the namespace from being overly cluttered with variable names that have 
nothing to do with the current module. 

Also, this makes it incredibly easy to quickly refer to what globals are available 
in the module by simple checking its “g” class.

"""
from pathlib import Path
import os
from .Controller import warehouse_controller


class config:
    HOME_PATH = Path(os.getenv("WNS_PATH", "."))
    """home path for the module, this is the default space for the user
    to search for warehouse files"""
    WAREHOUSE_DATA_DIR = Path(
        os.getenv(
            "WAREHOUSE_DATA_DIR",
            (HOME_PATH / "input" / "qvBox-warehouse-data-f20-v01_1041763401.txt"),
        )
    )
    """the full path to the warehouse data directory on start,
    if unspecified we default to ./input/qvBox-warehouse-data-f20-v01_1041763401.txt"""

    @classmethod
    def apply(cls) -> None:
        """
        Applies all the attributes to the repective globals in each indivdual module
        
        This is much cleaner than regular python global variables as only the globals
            required by the module can be seen by the module"""
        warehouse_controller.g.warehouse_file_path = cls.WAREHOUSE_DATA_DIR


config.apply()
