from typing import Iterable, Callable


def group_by[K, V](items: Iterable[V], key: Callable[[V], K]) -> dict[K, list[V]]:
    """
    Helper method to group an iterables into a dictionary.

    Usage
    -----
    For example, calling:
        group_by([("A", 1), ("B", 2), ("C", 3), ("A", 4), ("C", 5)], lambda x: x[0])
    produces:
        {"A": [("A", 1), ("A", 4)], "B": [("B", 2)], "C": [("C", 3), ("C", 5)]}

    Parameters
    -----------
    items: Iterable[V]
        a collection of values to be grouped
    key: Callable[[V], K]
        function mapping an item to a value used as a group label

    Returns
    -------
    grouped_collection: dict[K, list[V]]:
        elements from items grouped into a dictionary
    """
    result = {}
    for item in items:
        k = key(item)
        if k not in result:
            result[k] = [item]
        else:
            result[k].append(item)
    return result
