from ctypes import CDLL, c_int, Array
from multiprocessing import Queue, Process
from pathlib import Path

import numpy as np
from src.solvers.solver import SudokuSolver
from src.model.grid import SudokuGrid


class DancingLinksSudokuSolver(SudokuSolver):
    """
    This solver uses the famous Knuth's Algorithm X.
    It outsources work to the existing implementation in C:
        https://github.com/nstagman/exact_cover_sudoku
    """

    def run_algorithm(self) -> SudokuGrid | None:
        queue: Queue = Queue()
        task = Process(target=self._communicate_with_external_solver, args=[queue])
        task.start()

        try:
            return queue.get(timeout=self._time_limit)
        except Exception:
            if task.is_alive():
                task.terminate()
            raise TimeoutError()

    def _communicate_with_external_solver(self, queue: Queue) -> None:
        """
        Calls the external solver and returns result via the queue.

        Parameters
        -----------
        queue: Queue
            queue used to return the result
        """

        try:
            result = self._run_algorithm()
            queue.put_nowait(result)
        except Exception:
            queue.put_nowait(None)

    def _get_lib(self) -> CDLL:
        """
        Loads the library containing the solver.

        Returns
        --------
        library: CDLL
            a library containing the algorithm implementation
        """
        LIB_PATH = Path("lib").joinpath("ss.so")
        return CDLL(LIB_PATH)

    def _c_args(self) -> tuple[Array[c_int], c_int, Array[c_int]]:
        """
        Translates sudoku puzzle to the arguments used by the solver.

        Returns
        --------
        size: c_int
            a c_int object with size of the puzzle, `9` for the classical one
        puzzle_array: Array[c_int]
            a flat array containing the initial state of the puzzle
        solution_array: Array[c_int]
            a flat array of the same same as puzzle_array, but containing only zeros
        """

        size = c_int(self._puzzle.size)
        puzzle_list = self._puzzle.flatten().tolist()
        puzzle_array = (c_int * len(puzzle_list))(*puzzle_list)
        solution_array = (c_int * len(puzzle_list))(*([0] * len(puzzle_list)))
        return (puzzle_array, size, solution_array)

    def _grid_from_array(self, solution: Array[c_int]) -> SudokuGrid:
        """
        Translates the C array into a sudoku grid.

        Parameters
        ----------
        solution: Array[c_int]
            an array containing the solution

        Returns
        --------
        grid: SudokuGrid
            a sudoku grid corresponding to the array
        """

        array = np.array(solution).reshape((self._puzzle.size, self._puzzle.size))
        return SudokuGrid(array)

    def _run_algorithm(self) -> SudokuGrid | None:
        """
        Runs the algorithm.

        Returns
        --------
        grid: SudokuGrid | None
            `None` if the algorithm failed, otherwise a solution
        """
        dll = self._get_lib()

        puzzle_array, size, solution_array = self._c_args()
        result = dll.solve_puzzle(puzzle_array, size, solution_array)
        if result == 0:
            return None

        return self._grid_from_array(solution_array)
