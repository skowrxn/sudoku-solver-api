import numpy as np  # noqa
import numpy.typing as npt


def all_different_except(array: npt.ArrayLike, excluded: set) -> bool:
    """
    Checks whether array contains unique elements except some excluded cases.

    Parameters
    ----------
    array: npt.ArrayLike
        an array-like collection
    excluded: set
        values that are allowed to repeat

    Returns
    -------
    result: bool
        `True` if no value (except excluded) is repeating
        `False` otherwise
    """
    uniq = np.unique_counts(array)
    for i in range(len(uniq.values)):
        if uniq.values[i] not in excluded:
            if uniq.counts[i] != 1:
                return False
    return True
    # TODO:
    # Implement the function as described in the docstring
    # tip. `np.unique_counts` may be useful, but feel free to improvise
    #      https://numpy.org/devdocs/reference/generated/numpy.unique_counts.html
    # raise NotImplementedError("not implemented yet")
