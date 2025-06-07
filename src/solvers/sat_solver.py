from __future__ import annotations
from dataclasses import dataclass
import itertools  # noqa
from threading import Timer  # noqa
from typing import Iterable
from src.solvers.solver import SudokuSolver
from src.model.grid import SudokuGrid
from pysat.formula import CNF  # type: ignore[import-untyped]
from pysat.solvers import Solver  # type: ignore[import-untyped] #noqa
from src.utils.group_by import group_by


@dataclass(frozen=True)
class Coordinates:
    """
    Represent coordinates of a sudoku variable (empty cell).
    """

    row: int
    col: int
    block: int


@dataclass(frozen=True)
class Proposition:
    """
    A single proposition:
    "Sudoku cell at coordinates: `coords` has value `val`"
    """

    coords: Coordinates
    val: int
    id: int


@dataclass
class SudokuCNF:
    """
    Represents a sudoku puzzle using a `Conjunctive Normal Form`:
    - https://en.wikipedia.org/wiki/Conjunctive_normal_form
    - https://equaeghe.github.io/ecyglpki/cnfsat.html

    Usage
    -----
    Given a sudoku `grid: SudokuGrid` one should use static method `encode`
    to create a CNF representation:

        `sudoku_cnf = SudokuCNF.encode(grid)`

    To pass the representation into a SAT solver, one should use the `cnf` property:

        `with Solver(bootstrap_with=sudoku_cnf.cnf) as solver`

    Given a solution from a SAT solver (e.g. `solution = solver.get_model()`)
    one can translate it to a SudokuGrid via the `decode` method:

        `solution_grid =  sudoku_cnf.decode()`

    """

    cnf: CNF
    """a `Conjunctive Normal Form` encoding as used by a SAT solver"""
    propositions: dict[int, Proposition]
    """mapping from propositions identifiers (as used in the CNF)
       to the propositions themselves"""
    puzzle: SudokuGrid
    """a puzzle encoded in the CNF"""

    def __post_init__(self) -> None:
        self._every_cell_has_a_single_value()
        self._every_row_contains_unique_values()
        self._every_col_contains_unique_values()
        self._every_block_contains_unique_values()

    def _at_least_one(self, propositions: Iterable[Proposition]) -> None:
        self.cnf.append([p.id for p in propositions])

    def _at_most_one(self, propositions: Iterable[Proposition]) -> None:
        for p, q in itertools.combinations(propositions, 2):
            self.cnf.append([-p.id, -q.id])

    def _exactly_one(self, propositions: Iterable[Proposition]) -> None:
        self._at_most_one(propositions)
        self._at_least_one(propositions)

    def _every_cell_has_a_single_value(self):
        for cell_propositions in group_by(
            self.propositions.values(), lambda p: p.coords
        ).values():
            self._exactly_one(cell_propositions)

    def _every_row_contains_unique_values(self):
        for row_val_proposition in group_by(
                self.propositions.values(),
                lambda p: (p.coords.row, p.val)
        ).values():
            self._at_most_one(row_val_proposition)

    def _every_col_contains_unique_values(self):
        for col_val_proposition in group_by(self.propositions.values(),
                                            lambda p: (p.coords.col, p.val)).values():
            self._at_most_one(col_val_proposition)

    def _every_block_contains_unique_values(self):
        for block_val_proposition in group_by(self.propositions.values(),
                                              lambda p: (self.puzzle.block_index(p.coords.row, p.coords.col), p.val)).values():
            self._at_most_one(block_val_proposition)

    @staticmethod
    def encode(puzzle: SudokuGrid) -> SudokuCNF:
        """
        Encodes a given sudoku puzzle into its Conjunctive Normal Form
        suitable for SAT solvers.

        Parameters
        ----------
        puzzle: SudokuGrid
            a sudoku puzzle to be encoded

        Returns
        -------
        encoding: SudokuCNF
            Conjunctive Normal Form encoding of the specified puzzle
        """
        cnf = CNF()
        propositions = SudokuCNF._possible_propositions(puzzle)
        return SudokuCNF(cnf, propositions, puzzle)

    def decode(self, results: list[int]) -> SudokuGrid:
        """
        Decodes a SAT solution into a filled sudoku grid.

        Parameters
        ----------
        results: list[int]
            list of true propositions (their identifiers, to be exact)
            [1,-2,3,-4,5] would mean, that propositions 1,3,5 are true
            and 2 and 5 are false.

        Returns
        -------
        solution: SudokuGrid
            a sudoku grid filled according the SAT results
        """
        valid_ids = [prop_id for prop_id in results if prop_id >= 0]
        valid_propositions = [self.propositions[valid_prop_id] for valid_prop_id in valid_ids]
        solved_puzzle = self.puzzle.copy()

        for valid_proposition in valid_propositions:
            solved_puzzle[valid_proposition.coords.row, valid_proposition.coords.col] = valid_proposition.val

        return solved_puzzle

    @staticmethod
    def _possible_propositions(puzzle: SudokuGrid) -> dict[int, Proposition]:
        raise NotImplementedError("copy from the previous lab")


class SatSudokuSolver(SudokuSolver):
    """
    A SAT-based sudoku solver using the python-sat library:
    - what is a SAT-solver: https://en.wikipedia.org/wiki/SAT_solver

    - python-sat basic usage: https://pysathq.github.io/usage/\n
      look especially at an example starting with `formula = CNF()`

    - python-sat docs: https://pysathq.github.io/docs/html/index.html#supplementary-examples-package
    """

    def __init__(self, puzzle, time_limit):
        super().__init__(puzzle, time_limit)

    def run_algorithm(self) -> SudokuGrid | None:
        raise NotImplementedError("copy from the previous lab")


@dataclass
class SatSudokuValidator:
    """
    Class responsible for checking if the given sudoku puzzle
    has only a single unique solution.
    """

    _puzzle: SudokuGrid
    """a puzzle to be validated"""

    def has_unique_solution(self) -> bool:
        """
        Checks whether the puzzle has only single solution.

        Returns
        -------
        has_one_solution: bool
            `True` if there is a single solution to the puzzle
            `False` otherwise
        """
        # TODO:
        # Use SAT solver to check the uniqueness of the solution.
        # tips:
        # - this time we ignore timeout so the code will be simpler
        # - instead of the `solve_limited` us `enum_model`:
        #   https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.enum_models
        raise NotImplementedError("not implemented yet")
