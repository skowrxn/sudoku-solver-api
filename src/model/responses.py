from pydantic import BaseModel


class SolveResponse(BaseModel):
    """
    Represent a response to the solve request.
    """

    solution: list[list[int]]
    """Solved sudoku represented as a list of lists"""


class ValidateResponse(BaseModel):
    """
    Represent a response to the validate request.
    """

    valid: bool
    """Whether the sudoku is valid"""
