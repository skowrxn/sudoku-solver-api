import numpy as np
from src.solvers.solver import SudokuSolver
from src.model.grid import SudokuGrid
from src.utils.recursion_limit import recursion_limit_set_to  # noqa


class NaiveSudokuSolver(SudokuSolver):
    """
    A naive sudoku solver inspired by https://www.geeksforgeeks.org/sudoku-backtracking-7/.
    """

    def run_algorithm(self) -> SudokuGrid | None:
        with recursion_limit_set_to(self._puzzle.size**3):
            if self._dfs(0, 0):
                return self._puzzle
            return None

    def _increment_coordinates(self, row: int, col: int) -> tuple[int, int]:
        """
        Increments the coordinates (moves to the next cell).

        Parameters
        -----------
        row: int
            a row coordinate
        col: int
            a column coordinate

        Returns
        --------
        next_coords: tuple[int,int]
            coordinates (row, col) of the next cell
        """
        if col < self._puzzle.size - 1:
            return row, col + 1
        else:
            return row + 1, 0

    def _is_excluded(self, row: int, col: int, val: int) -> bool:
        """
        Checks whether a given value can be put in the specified cell.

        Parameters
        -----------
        row: int
            a row coordinate
        col: int
            a column coordinate
        val: int
            a value to be stored in the cell

        Returns
        --------
        excluded: bool
            - `True` if the value can**not** be put in the cell
            - `False` otherwise
        """
        if np.uint(val) in self._puzzle[row]:
            return True
        if val in self._puzzle[:, col]:
            return True
        block_index = self._puzzle.block_index(row, col)
        return val in self._puzzle.block(block_index)

    def _dfs(self, row: int, col: int) -> bool:
        """
        Performs a depth-first-search to solve the sudoku puzzle.
        Basically, it tries to put any acceptable value at the current cell
        and then moves to the next cell recursively.

        It may happen that it is impossible to find any
        acceptable value for the given cell.
        In such a case we check other values for the **previous**
        cells. This is called backtracking.

        - https://en.wikipedia.org/wiki/Backtracking
        - https://www.geeksforgeeks.org/introduction-to-backtracking-2/

        Parameters
        -----------
        row: int
            row coordinate of the currently considered cell
        col: int
            column coordinate of the currently considered cell

        Returns
        --------
        solved: bool
            `True` - if method found the solution
            `False` - otherwise
        """

        if row >= self._puzzle.size:
            return True

        if self._timeout():
            raise TimeoutError()

        if self._puzzle[row, col] > 0:
            new_row, new_col = self._increment_coordinates(row, col)
            return self._dfs(new_row, new_col)

        for val in range(self._puzzle.size + 1):
            if self._is_excluded(row, col, val):
                continue
            self._puzzle[row, col] = val
            new_row, new_col = self._increment_coordinates(row, col)
            if self._dfs(new_row, new_col):
                return True
            self._puzzle[row, col] = 0

        return False
