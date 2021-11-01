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
    # TODO: handle numbers > 26 and < 1
    return chr(ord("@") + number)


def coord_to_human(coord):
    """
    Converts calculation coordinates to more human-readable coordinates

    Parameters
    ----------
    coord : tuple[int,int]
        The coordinate to convert.

    Returns
    -------
    tuple[int, str]
        The converted coordinate.

    """
    return (coord[0] + 1, int_to_cap_letter(coord[1] + 1))
