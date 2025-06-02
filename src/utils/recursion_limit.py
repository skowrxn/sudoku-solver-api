import sys
from typing import Literal


class recursion_limit_set_to:
    """
    A context manager temporarily overriding the recursion limit.
    For more details read: https://note.nkmk.me/en/python-sys-recursionlimit/

    Attributes:
    -----------
    original_limit: int
        the recursion limit before the override
    limit: int
        a desired recursion limit
    """

    original_limit: int
    limit: int

    def __init__(self, limit: int) -> None:
        """
        Initialize the context manager.

        Parameters
        -----------
        limit: int
            a desired recursion limit
        """
        self.limit = limit
        self.original_limit = sys.getrecursionlimit()

    def __enter__(self, *args, **kwargs) -> None:
        sys.setrecursionlimit(self.limit)
        return None

    def __exit__(self, *args) -> Literal[False]:
        sys.setrecursionlimit(self.original_limit)
        return False
