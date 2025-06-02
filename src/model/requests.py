from typing import Annotated
from pydantic import AfterValidator, BaseModel, Field
from src.model.grid import SudokuGrid
from src.solvers.solver_type import SudokuSolverType
import numpy as np


def ensure_puzzle_is_valid(puzzle: list[list[int]]) -> list[list[int]]:
    """
    Makes sure the list representation corresponds to a sudoku grid.
    Raises ValueError if there is a problem with the puzzle.

    Parameters
    ----------
    puzzle: list[list[int]]
        sudoku array represented as a list of lists (rows)

    Returns
    -------
    puzzle: list[list[int]]
        the input puzzle if it's valid
    """

    # TODO:
    # Implement the validator.
    # tips.
    # - check if list contains only nonnegative number
    # - then try to create a sudoku grid
    #
    # If everything is ok, return the same puzzle you get as the input
    pass
    return puzzle


SudokuAsList = Annotated[
    list[list[int]],
    AfterValidator(ensure_puzzle_is_valid),
    Field(..., description="2D list representing the sudoku grid"),
]
"""An annotated type representing a sudoku represented with lists
   Read more: https://docs.pydantic.dev/2.0/usage/validators/#annotated-validators
"""


class SolveRequest(BaseModel):
    """
    Represents a request to solve a given puzzle.
    """

    solver: SudokuSolverType = Field(
        default=SudokuSolverType.SAT, description="Solver to be used"
    )
    time_limit: float = Field(default=10.0, gt=0, description="Time limit in seconds")
    puzzle: SudokuAsList


class ValidateRequest(BaseModel):
    """
    Represents a request to validate a given puzzle.
    """

    puzzle: SudokuAsList
