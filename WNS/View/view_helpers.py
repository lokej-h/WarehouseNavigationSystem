# -*- coding: utf-8 -*-
"""

Helper functions for the View package.

"""


def int_to_cap_letter(number: int) -> str:
    """
    Converts numbers to characters. 1 -> A, B -> 2 etc.
    
    Useful for user-firendly coordinate generation.

    Parameters
    ----------
    number : int
        A number.

    Returns
    -------
    str
        A character corresponding to the number.

    """
    return chr(ord("@") + number)
