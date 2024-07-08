from collections.abc import Iterable
from typing import Union

from spb import plot_list


def plot_points(x: Iterable, y: Iterable, rendering_options: Union[dict, None] = None, *args, **kwargs):
    kwargs.setdefault("is_point", True)
    if rendering_options is None:
        rendering_options = {}

    return plot_list((x, y, rendering_options), *args, **kwargs)
